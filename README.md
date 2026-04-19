# board-game-record

Schema and rules catalog for recording board game end-states. This repo defines the **contract** — the JSON Schema each record conforms to, per-game variant schemas, and the rules-summary knowledge base — while session records themselves live in a **separate database**, not in this repo.

A record captures the end-state of a session (final resources, VP/coins, assets, eliminations, winners) as JSON. Free-form fields (names, notes, identity) accept any Unicode; see [`docs/NAMING.md`](docs/NAMING.md) for the encoding policy.

## Layout

```
schema/core.schema.json     # cross-game fields
docs/SCHEMA.md              # field-by-field spec
docs/NAMING.md              # game/variant naming conventions
tools/validate.py           # validator (authoring / CI)
games/<game>/               # per-game folders (added one PR at a time)
  README.md                 # overview, list of variants
  <game>.schema.json        # base variant
  <game>.md                 # rules summary + rulebook link
  <variant>.schema.json     # expansion (zero or more)
  <variant>.md
```

No games are checked in yet — the spec lands first, then each game in its own PR.

## Recording a game

Records are stored in the database, not in this repo. The flow:

1. Find the game's folder under `games/`. If it doesn't exist, the game isn't supported yet — open a PR that adds the schema + rules summary.
2. Author a record that conforms to `schema/core.schema.json` plus the variant schema (see example in [`docs/SCHEMA.md`](docs/SCHEMA.md)).
3. Run `tools/validate.py` on the draft record to catch issues before ingest.
4. Submit it to the database. (Ingest tooling tracked separately — see open work.)

## Validating a draft record

```bash
pip install -r tools/requirements.txt
python tools/validate.py path/to/draft.json [more.json ...]
```

Prints `PASS` or `FAIL` per input. Failures include JSON Pointer paths to the offending fields. Exit code is 0 only if every input passes.

## Spec

See [`docs/SCHEMA.md`](docs/SCHEMA.md) for the core field reference and [`docs/NAMING.md`](docs/NAMING.md) for the game/variant naming conventions.
