# board-game-record

Stat tracking across board games. A session is recorded as a single JSON file capturing the **end-state** (final resources, VP/coins, assets, eliminations, winners). Records are validated against a shared core schema plus a per-game variant schema.

## Layout

```
schema/core.schema.json     # cross-game fields
docs/SCHEMA.md              # field-by-field spec
docs/NAMING.md              # game/variant naming conventions
tools/validate.py           # validator
games/<game>/               # per-game folders (added one PR at a time)
  <variant>.schema.json
  <variant>.md              # rules summary + rulebook link
  records/YYYY-MM-DD-NNN.json
```

No games are checked in yet — the spec lands first, then each game in its own PR.

## Recording a game

1. Find the game's folder under `games/`. If it doesn't exist, the game isn't supported yet — open a PR that adds the schema + rules summary.
2. Copy the example record from `games/<game>/records/` or from `docs/SCHEMA.md`.
3. Fill in `game`, `variant` (default `base`), `date`, `player_count`, `players[]`, and `winners` (list of player indices).
4. Put the file at `games/<game>/records/YYYY-MM-DD-NNN.json`.
5. Run the validator.

## Validating

```bash
pip install -r tools/requirements.txt
python tools/validate.py                 # validate every record
python tools/validate.py path/to/rec.json   # validate a single file
```

Exit code is non-zero if any record fails; errors are printed with JSON Pointer paths.

## Spec

See [`docs/SCHEMA.md`](docs/SCHEMA.md) for the core field reference and [`docs/NAMING.md`](docs/NAMING.md) for the game/variant naming conventions.
