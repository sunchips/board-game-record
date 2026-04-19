#!/usr/bin/env python3
"""Validate board-game session records against core + variant JSON Schemas.

Usage:
    python tools/validate.py                 # validate every record in games/*/records/
    python tools/validate.py path/to/rec.json [path/to/other.json ...]

Exits non-zero if any record fails validation.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import ValidationError

REPO_ROOT = Path(__file__).resolve().parent.parent
CORE_SCHEMA_PATH = REPO_ROOT / "schema" / "core.schema.json"
GAMES_DIR = REPO_ROOT / "games"


def load_json(path: Path) -> dict:
    with path.open() as f:
        return json.load(f)


def variant_schema_path(game: str, variant: str) -> Path:
    filename = f"{game}.schema.json" if variant == "base" else f"{variant}.schema.json"
    return GAMES_DIR / game / filename


def format_error(record_path: Path, err: ValidationError) -> str:
    pointer = "/" + "/".join(str(p) for p in err.absolute_path)
    return f"  {record_path}:{pointer}: {err.message}"


def validate_record(record_path: Path, core_schema: dict) -> list[str]:
    """Return a list of error messages; empty list = record is valid."""
    try:
        record = load_json(record_path)
    except json.JSONDecodeError as e:
        return [f"  {record_path}: invalid JSON: {e}"]

    errors: list[str] = []

    core_validator = Draft202012Validator(core_schema, format_checker=FormatChecker())
    core_errors = sorted(core_validator.iter_errors(record), key=lambda e: e.path)
    errors.extend(format_error(record_path, e) for e in core_errors)

    game = record.get("game")
    variant = record.get("variant", "base")
    if isinstance(game, str) and isinstance(variant, str):
        variant_path = variant_schema_path(game, variant)
        if variant_path.exists():
            try:
                variant_schema = load_json(variant_path)
                variant_validator = Draft202012Validator(
                    variant_schema, format_checker=FormatChecker()
                )
                variant_errors = sorted(
                    variant_validator.iter_errors(record), key=lambda e: e.path
                )
                errors.extend(format_error(record_path, e) for e in variant_errors)
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


def discover_records() -> list[Path]:
    if not GAMES_DIR.exists():
        return []
    return sorted(GAMES_DIR.glob("*/records/*.json"))


def main(argv: list[str]) -> int:
    if not CORE_SCHEMA_PATH.exists():
        print(f"error: core schema not found at {CORE_SCHEMA_PATH}", file=sys.stderr)
        return 2
    core_schema = load_json(CORE_SCHEMA_PATH)

    if len(argv) > 1:
        records = [Path(a).resolve() for a in argv[1:]]
    else:
        records = discover_records()

    if not records:
        print("0 records validated (no records found under games/*/records/)")
        return 0

    failed = 0
    for rec in records:
        errs = validate_record(rec, core_schema)
        if errs:
            failed += 1
            display = rec.relative_to(REPO_ROOT) if rec.is_relative_to(REPO_ROOT) else rec
            print(f"FAIL: {display}")
            for msg in errs:
                print(msg)

    valid = len(records) - failed
    print(f"{valid}/{len(records)} records valid")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
