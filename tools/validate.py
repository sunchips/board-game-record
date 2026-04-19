#!/usr/bin/env python3
"""Validate a board-game session record against its schemas.

Usage:
    python tools/validate.py path/to/rec.json [more.json ...]

Each input file is checked against schema/core.schema.json plus the
game's base schema and every listed variant schema, merged into one
composite. Prints PASS or FAIL per file; exits 0 only if every input
passes.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import ValidationError

REPO_ROOT = Path(__file__).resolve().parent.parent
CORE_SCHEMA_PATH = REPO_ROOT / "schema" / "core.schema.json"
GAMES_DIR = REPO_ROOT / "games"


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def format_error(record_path: Path, err: ValidationError) -> str:
    pointer = "/" + "/".join(str(p) for p in err.absolute_path)
    return f"  {record_path}:{pointer}: {err.message}"


def resolve_game_dir(game: str, year: int | None) -> tuple[Path | None, str | None]:
    """Return (game_dir, error_message). Exactly one is non-None."""
    bare = GAMES_DIR / game
    if bare.is_dir():
        return bare, None
    if year is not None:
        tagged = GAMES_DIR / f"{game}.{year}"
        if tagged.is_dir():
            return tagged, None
        return None, f"no folder at games/{game}/ or games/{game}.{year}/"
    return None, (
        f"no folder at games/{game}/; if this game shares a title with another, "
        "set year_published to select the right edition"
    )


def variant_player_props(schema: dict) -> dict:
    return (
        schema.get("properties", {})
        .get("players", {})
        .get("items", {})
        .get("properties", {})
    )


def merge_variant_schemas(schemas: list[tuple[str, dict]]) -> tuple[dict, list[str]]:
    """Union end_state / identity / x-score-formula across base + listed variants."""
    end_state_keys: set[str] = set()
    end_state_props: dict[str, dict] = {}
    end_state_props_owner: dict[str, str] = {}
    identity_values: set[str] = set()
    identity_constrained = False
    x_formula: dict[str, int] = {}
    x_formula_owner: dict[str, str] = {}
    conflicts: list[str] = []

    for label, schema in schemas:
        pprops = variant_player_props(schema)

        es = pprops.get("end_state", {})
        for key in es.get("propertyNames", {}).get("enum", []):
            end_state_keys.add(key)
        for key, spec in es.get("properties", {}).items():
            if key in end_state_props and end_state_props[key] != spec:
                conflicts.append(
                    f"end_state.{key}: incompatible definitions in "
                    f"'{end_state_props_owner[key]}' and '{label}'"
                )
            else:
                end_state_props[key] = spec
                end_state_props_owner[key] = label

        ident = pprops.get("identity", {})
        if "enum" in ident:
            identity_constrained = True
            identity_values.update(ident["enum"])

        formula = schema.get("x-score-formula", {})
        for key, mult in formula.items():
            if key in x_formula and x_formula[key] != mult:
                conflicts.append(
                    f"x-score-formula.{key}: {x_formula_owner[key]}={x_formula[key]} "
                    f"vs {label}={mult}"
                )
            else:
                x_formula[key] = mult
                x_formula_owner[key] = label

    player_props: dict = {
        "end_state": {
            "type": "object",
            "propertyNames": {"enum": sorted(end_state_keys)},
            "properties": end_state_props,
            "additionalProperties": {"type": ["integer", "boolean"]},
        }
    }
    if identity_constrained:
        player_props["identity"] = {"enum": sorted(identity_values)}

    merged = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "properties": {
            "players": {
                "type": "array",
                "items": {"type": "object", "properties": player_props},
            }
        },
    }
    return merged, conflicts


def validate_record(record_path: Path, core_schema: dict) -> list[str]:
    try:
        record = load_json(record_path)
    except json.JSONDecodeError as e:
        return [f"  {record_path}: invalid JSON: {e}"]

    errors: list[str] = []

    core_validator = Draft202012Validator(core_schema, format_checker=FormatChecker())
    errors.extend(
        format_error(record_path, e)
        for e in sorted(core_validator.iter_errors(record), key=lambda e: e.path)
    )

    if not isinstance(record, dict):
        return errors

    game = record.get("game")
    variants = record.get("variants", [])
    year = record.get("year_published")
    if not isinstance(game, str) or not isinstance(variants, list):
        return errors

    game_dir, dir_err = resolve_game_dir(game, year if isinstance(year, int) else None)
    if game_dir is None:
        errors.append(f"  {record_path}:/game: {dir_err}")
    else:
        try:
            game_dir.resolve().relative_to(GAMES_DIR.resolve())
        except ValueError:
            errors.append(f"  {record_path}:/game: slug resolves outside games/ directory")
            return errors

        schema_paths: list[tuple[str, Path]] = [(game, game_dir / f"{game}.schema.json")]
        for v in variants:
            if isinstance(v, str):
                schema_paths.append((v, game_dir / f"{v}.schema.json"))

        loaded: list[tuple[str, dict]] = []
        for label, path in schema_paths:
            if not path.exists():
                errors.append(
                    f"  {record_path}: schema not found at {path.relative_to(REPO_ROOT)}"
                )
                continue
            try:
                loaded.append((label, load_json(path)))
            except json.JSONDecodeError as e:
                errors.append(f"  {path}: invalid JSON: {e}")

        if loaded:
            merged, conflicts = merge_variant_schemas(loaded)
            for msg in conflicts:
                errors.append(f"  {record_path}: schema conflict — {msg}")
            merged_validator = Draft202012Validator(merged, format_checker=FormatChecker())
            errors.extend(
                format_error(record_path, e)
                for e in sorted(merged_validator.iter_errors(record), key=lambda e: e.path)
            )

    players = record.get("players")
    if isinstance(players, list):
        player_count = record.get("player_count")
        if isinstance(player_count, int) and player_count != len(players):
            errors.append(
                f"  {record_path}:/player_count: {player_count} does not match len(players)={len(players)}"
            )
        winners = record.get("winners")
        if isinstance(winners, list):
            for i, w in enumerate(winners):
                if isinstance(w, int) and w >= len(players):
                    errors.append(
                        f"  {record_path}:/winners/{i}: index {w} out of range (players has {len(players)} entries)"
                    )

    return errors


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("paths", nargs="+", help="Record files to validate.")
    args = parser.parse_args(argv[1:])

    if not CORE_SCHEMA_PATH.exists():
        print(f"error: core schema not found at {CORE_SCHEMA_PATH}", file=sys.stderr)
        return 2
    core_schema = load_json(CORE_SCHEMA_PATH)

    failed = 0
    for path in (Path(a).resolve() for a in args.paths):
        display = path.relative_to(REPO_ROOT) if path.is_relative_to(REPO_ROOT) else path
        errors = validate_record(path, core_schema)
        if errors:
            failed += 1
            print(f"FAIL: {display}")
            for msg in errors:
                print(msg)
        else:
            print(f"PASS: {display}")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
