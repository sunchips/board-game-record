#!/usr/bin/env python3
"""Validate a board-game session record against its schemas.

Usage:
    python tools/validate.py path/to/rec.json [more.json ...]

Each input file is checked against schema/core.schema.json plus the
variant schema resolved from its `game` and `variant` fields. Prints
PASS or FAIL per file; exits 0 only if every input passes.
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


def variant_schema_path(game: str, variant: str) -> Path:
    filename = f"{game}.schema.json" if variant == "base" else f"{variant}.schema.json"
    return GAMES_DIR / game / filename


def format_error(record_path: Path, err: ValidationError) -> str:
    pointer = "/" + "/".join(str(p) for p in err.absolute_path)
    return f"  {record_path}:{pointer}: {err.message}"


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
    variant = record.get("variant", "base")
    if isinstance(game, str) and isinstance(variant, str):
        variant_path = variant_schema_path(game, variant)
        try:
            variant_path.resolve().relative_to(GAMES_DIR.resolve())
        except ValueError:
            errors.append(
                f"  {record_path}:/game: slug resolves outside games/ directory"
            )
        else:
            if variant_path.exists():
                try:
                    variant_schema = load_json(variant_path)
                    variant_validator = Draft202012Validator(
                        variant_schema, format_checker=FormatChecker()
                    )
                    errors.extend(
                        format_error(record_path, e)
                        for e in sorted(variant_validator.iter_errors(record), key=lambda e: e.path)
                    )
                except json.JSONDecodeError as e:
                    errors.append(f"  {variant_path}: invalid JSON: {e}")
            else:
                errors.append(
                    f"  {record_path}: variant schema not found at {variant_path.relative_to(REPO_ROOT)}"
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
