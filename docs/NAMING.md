# Naming conventions

## Encoding

All JSON records and markdown files in this repo are **UTF-8**. Player names, notes, identity values, rules summaries — anything that's a free-form string — can use any Unicode script. A record with `"name": "たろう"` or `"notes": "近い勝負だった"` is fully supported.

## Slugs

- `game` and `variant` values are **ASCII-only, lowercase, hyphen-separated** slugs.
- Only `a-z`, `0-9`, and `-` are allowed; no leading/trailing/consecutive hyphens.
- Slugs stay ASCII because they become filesystem paths, URLs, and grep-targets — keeping them portable and searchable across platforms matters more than representing the game's native title here. Capture the native/original title inside the game's `README.md` and `<slug>.md` rules summary.
- Examples: `catan`, `scythe`, `the-king-is-dead`, `king-of-new-york`, `cities-and-knights`. A Japanese game like *Machi Koro* uses the transliterated slug `machi-koro` — not `街コロ`.

## Game identifier

A record identifies its game with two fields:

```json
"game": "catan",
"variant": "seafarers"
```

`variant` defaults to `"base"` when the record is for the base game.

The canonical display/filename form is:

```
<game>               # when variant == "base"
<game>.<variant>     # when variant is an expansion slug
```

Examples: `catan`, `catan.seafarers`, `scythe.invaders-from-afar`, `everdell.pearlbrook`.

### Why `.` rather than `+`

`+` is not a legal character in Windows filenames, so using it in repository paths (or any filename a user might export) would break cross-platform usability. `.` works everywhere. Slugs themselves never contain `.`, so there's no ambiguity — the first `.` separates the game slug from the variant slug.

## Standalone editions vs. expansions

- A variant that extends a base game → lives in the base game's folder as `<variant>.schema.json` + `<variant>.md`. Records use `{ "game": "<base>", "variant": "<variant>" }`.
- A standalone edition that is its own game → lives in its own top-level folder. Records use `{ "game": "<edition-slug>" }` (variant stays `"base"`).

For example, Codenames Duet is standalone (different rules, different box, different player count), so it lives at `games/codenames-duet/` — not as a variant of `codenames`.

Minor revisions of the same base game (e.g. Catan 5e) do **not** get their own variant. Capture the difference in the base `<game>.md` and, for a specific session, in `record.notes`.

## Expansion stacking

v1 supports exactly one variant per record — either `"base"` or a single expansion slug. Multi-expansion sessions are recorded against whichever single variant dominated (and the others noted in `notes`), or they go unrecorded until stacked-variant schemas are introduced on demand. The naming convention for those, when/if added:

```
<game>.<variant1>.<variant2>.schema.json
```

## Folder layout

```
games/<game>/
├── README.md              # overview, list of variants
├── <game>.schema.json     # base variant
├── <game>.md              # base rules summary + rulebook link
├── <variant>.schema.json  # expansion (zero or more)
├── <variant>.md
└── records/
    └── YYYY-MM-DD-NNN.json
```

Record filenames: `<date>-<sequence>.json`, where sequence is a zero-padded count of games played that day (`001`, `002`, …). The filename is cosmetic — the validator reads the JSON to determine game/variant.
