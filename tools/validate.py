#!/usr/bin/env python3
"""Validate board-game session records against core + variant JSON Schemas.

Usage:
    python tools/validate.py                         # validate every record in games/*/records/
    python tools/validate.py path/to/rec.json ...    # validate specific files
    python tools/validate.py --show-scores ...       # also print derived scores

Exits non-zero if any record fails validation.
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
SCORE_FORMULA_KEY = "x-score-formula"


def load_json(path: Path) -> dict:
    with path.open() as f:
        return json.load(f)


def variant_schema_path(game: str, variant: str) -> Path:
    filename = f"{game}.schema.json" if variant == "base" else f"{variant}.schema.json"
    return GAMES_DIR / game / filename


def format_error(record_path: Path, err: ValidationError) -> str:
    pointer = "/" + "/".join(str(p) for p in err.absolute_path)
    return f"  {record_path}:{pointer}: {err.message}"


def compute_score(end_state: dict, formula: dict) -> int:
    return sum(end_state.get(k, 0) * m for k, m in formula.items())


def validate_record(
    record_path: Path, core_schema: dict
) -> tuple[list[str], dict | None, dict | None]:
    """Validate one record. Returns (errors, record, variant_schema).

    record and variant_schema are None when unrecoverable (parse error or missing schema).
    """
    try:
        record = load_json(record_path)
    except json.JSONDecodeError as e:
        return [f"  {record_path}: invalid JSON: {e}"], None, None

    errors: list[str] = []

    core_validator = Draft202012Validator(core_schema, format_checker=FormatChecker())
    errors.extend(
        format_error(record_path, e)
        for e in sorted(core_validator.iter_errors(record), key=lambda e: e.path)
    )

    variant_schema: dict | None = None
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
                errors.extend(
                    format_error(record_path, e)
                    for e in sorted(variant_validator.iter_errors(record), key=lambda e: e.path)
                )
            except json.JSONDecodeError as e:
                errors.append(f"  {variant_path}: invalid JSON: {e}")
                variant_schema = None
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

    return errors, record, variant_schema


def print_derived_scores(record: dict, variant_schema: dict) -> None:
    formula = variant_schema.get(SCORE_FORMULA_KEY)
    if not formula:
        return
    players = record.get("players") or []
    if not players:
        return
    print("  derived scores:")
    for i, p in enumerate(players):
        score = compute_score(p.get("end_state") or {}, formula)
        name = p.get("name", "?")
        print(f"    players[{i}] {name}: {score}")


def discover_records() -> list[Path]:
    if not GAMES_DIR.exists():
        return []
    return sorted(GAMES_DIR.glob("*/records/*.json"))


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "paths", nargs="*", help="Record files to validate. Defaults to games/*/records/*.json."
    )
    parser.add_argument(
        "--show-scores",
        action="store_true",
        help="Print scores derived from each variant's x-score-formula.",
    )
    args = parser.parse_args(argv[1:])

    if not CORE_SCHEMA_PATH.exists():
        print(f"error: core schema not found at {CORE_SCHEMA_PATH}", file=sys.stderr)
        return 2
    core_schema = load_json(CORE_SCHEMA_PATH)

    records = [Path(a).resolve() for a in args.paths] if args.paths else discover_records()

    if not records:
        print("0 records validated (no records found under games/*/records/)")
        return 0

    failed = 0
    for rec in records:
        errs, record, variant_schema = validate_record(rec, core_schema)
        display = rec.relative_to(REPO_ROOT) if rec.is_relative_to(REPO_ROOT) else rec
        if errs:
            failed += 1
            print(f"FAIL: {display}")
            for msg in errs:
                print(msg)
        elif args.show_scores:
            print(f"OK:   {display}")
        if args.show_scores and record is not None and variant_schema is not None and not errs:
            print_derived_scores(record, variant_schema)

    valid = len(records) - failed
    print(f"{valid}/{len(records)} records valid")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
