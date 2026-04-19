# Schema

Session records are stored in a separate database — this repo defines the shape they must conform to. Every record validates against three layers:

1. **`schema/core.schema.json`** — cross-game fields (this document).
2. **`games/<game>/<game>.schema.json`** — base ruleset for the game (constrains `end_state` keys and optionally `identity` values).
3. **`games/<game>/<variant>.schema.json`** — one per slug in the record's `variants` list. Each variant declares only what it adds on top of the base.

The validator unions layers 2 and 3 (plus any further listed variants) into a single composite schema before validation, so the allowed `end_state` keys are the combination of everything active in the session. Every layer is JSON Schema draft 2020-12.

## Core fields

| Field            | Type              | Required       | Captures                                                                                                                                                                           |
| ---------------- | ----------------- | -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `game`           | string            | yes            | Lowercase-hyphenated slug of the printed title. E.g. `catan`, `the-king-is-dead`, `coup`. Never carries a year — use `year_published` for that.                                    |
| `variants`       | string[]          | no (default ∅) | Expansion/edition slugs active in this session. Each must have a `<slug>.schema.json` in the game folder. Order doesn't matter; duplicates rejected.                               |
| `year_published` | int               | no             | Original publication year of the game. Pure metadata when the title is unique. Required only when two games share a printed title — it then selects the right edition's folder.    |
| `date`           | string (ISO date) | yes            | Calendar date the session was played, `YYYY-MM-DD`.                                                                                                                                |
| `player_count`   | int               | yes            | Number of seated players. Must equal `len(players)`.                                                                                                                               |
| `winners`        | int[]             | yes            | 0-based indices into `players[]`. One entry = solo win; multiple = tie or team win (list every teammate who shared the win).                                                       |
| `notes`          | string            | no             | Free-form prose for anything the structured fields don't capture — elimination order, score breakdowns, house rules, what broke a tie, best-of-N round tallies, memorable moments. |
| `players`        | array             | yes            | One entry per player, in seating order. Position in array = player index.                                                                                                          |

## `players[]` fields

| Field        | Type           | Required | Captures                                                                                                                                                                                                                                                            |
| ------------ | -------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`       | string         | yes      | Player's name/handle. Non-unique is fine — `winners` references by index.                                                                                                                                                                                           |
| `email`      | string (email) | no       | Stable identifier for the player across sessions. Used for aggregations / stats over time (same person → same email, even if `name` varies).                                                                                                                        |
| `identity`   | string         | no       | Single field covering colour / faction / civ / mat / hidden role — whatever the game uses to distinguish players. Base + variant schemas may constrain via `enum`; the validator unions their enums. Examples: `"red"` (Catan), `"crimea"` (Scythe).                |
| `team`       | int            | no       | Team number for team games (e.g. `1` / `2`). Teammates share the value. Omit for free-for-all.                                                                                                                                                                      |
| `eliminated` | bool           | no       | Whether the player was knocked out before the game ended. Omit entirely for games without elimination (Catan, Codenames, etc.); only include when the game has an elimination mechanic (Coup, Risk).                                                                |
| `end_state`  | object         | yes      | Map of everything the player holds at game end: VP, coins, resources, cards, buildings, units, tiles, employees, territories, etc. Keys constrained by the union of the base schema and listed variant schemas. Values are integers for counts, booleans for flags. |

There's no separate `score` field. A player's score — when the game has one — is either:

- **derived** from `end_state` components, via a formula declared in the base or variant schemas (see below); or
- **recorded directly** as a dedicated key in `end_state` (e.g. `coins` for Scythe, `vp` for games with non-linear scoring) when the formula can't be expressed simply.

Games without a score at all (Coup, Secret Hitler, Codenames) declare no formula and no score key. Per-unit score breakdowns for complex scoring live in `notes`.

## Cross-field rules (enforced by the validator)

- `player_count == len(players)`
- Every entry in `winners` is a valid index: `0 <= w < len(players)`
- Every slug in `variants` has a corresponding `<slug>.schema.json` in the resolved game folder

The core schema additionally enforces `winners` is non-empty and has no duplicate entries (`minItems: 1`, `uniqueItems: true`), and `variants` entries are unique.

## Game folder resolution

The validator resolves the game folder from `game` (and optionally `year_published`):

1. If `games/<game>/` exists, use it. `year_published` is pure metadata.
2. Otherwise, if `year_published` is set and `games/<game>.<year_published>/` exists, use that. This is the disambiguation case — see [NAMING.md](NAMING.md#identical-printed-titles-for-different-games).
3. Otherwise, error.

Inside the resolved folder, schema files are always named by their slug alone (e.g. `coup.schema.json`, `reformation.schema.json`) — the folder name carries the year, the files don't repeat it.

## Variant schemas — pure deltas

Each variant schema declares **only what that variant adds or constrains**. It does not restate the base. The validator takes the base schema plus every schema listed in `variants`, and unions them:

- `end_state.propertyNames.enum` → set-union across layers (the combined allowed key set)
- `end_state.properties.<key>` → per-key type/shape definitions; if two schemas define the same key with different shapes, the validator errors
- `identity.enum` → set-union
- `x-score-formula` → merged `{key: multiplier}` map; if two schemas set different multipliers for the same key, the validator errors

A minimal Catan base schema:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Catan — Base",
  "x-score-formula": {
    "settlements": 1,
    "cities": 2,
    "longest_road": 2,
    "largest_army": 2,
    "dev_card_vp": 1
  },
  "properties": {
    "players": {
      "items": {
        "properties": {
          "identity": { "enum": ["red", "blue", "white", "orange"] },
          "end_state": {
            "propertyNames": {
              "enum": [
                "settlements",
                "cities",
                "roads",
                "longest_road",
                "largest_army",
                "dev_card_vp",
                "knights_played"
              ]
            },
            "properties": {
              "settlements": { "type": "integer", "minimum": 0 },
              "cities": { "type": "integer", "minimum": 0 },
              "roads": { "type": "integer", "minimum": 0 },
              "longest_road": { "type": "boolean" },
              "largest_army": { "type": "boolean" },
              "dev_card_vp": { "type": "integer", "minimum": 0 },
              "knights_played": { "type": "integer", "minimum": 0 }
            }
          }
        }
      }
    }
  }
}
```

A companion Seafarers variant schema only mentions what Seafarers adds (illustrative):

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Catan — Seafarers",
  "x-score-formula": { "gold": 0, "ships": 0, "settlements_on_islands": 2 },
  "properties": {
    "players": {
      "items": {
        "properties": {
          "end_state": {
            "propertyNames": {
              "enum": ["gold", "ships", "settlements_on_islands"]
            },
            "properties": {
              "gold": { "type": "integer", "minimum": 0 },
              "ships": { "type": "integer", "minimum": 0 },
              "settlements_on_islands": { "type": "integer", "minimum": 0 }
            }
          }
        }
      }
    }
  }
}
```

A record with `"variants": ["seafarers"]` gets the union: both base and Seafarers keys are allowed, and the combined `x-score-formula` has all multipliers.

### `x-score-formula` — deriving VP from components

When the merged formula is non-empty, a player's score is computed as:

```
score = sum( end_state.get(key, 0) * multiplier for key, multiplier in merged_formula.items() )
```

Boolean-style components (e.g. `longest_road`) are treated as `0` when `false` and `1` when `true`, so the multiplier carries the point value.

When the formula covers the score:

- Records **do not** carry a `vp` (or similar) key — it's reconstructed from components.
- Each schema's rules summary (`<variant>.md`) documents the formula in prose for humans.
- Downstream tooling (database views, reporting) reads the merged formula to compute scores on demand.

When a game's scoring isn't expressible as a simple linear sum (Scythe's popularity brackets, Everdell's unique-card tables), the base or variant schema **omits** `x-score-formula` and instead adds a dedicated score key like `coins` or `vp` to the `end_state` enum. The rules summary explains how that total was computed.

`x-score-formula` lives outside JSON Schema's standard vocabulary — the `x-` prefix marks it as an extension. JSON Schema validators ignore unknown top-level keywords, so schema validation is unaffected; only this repo's tooling reads the field.

## Example record

A Catan-style record, with scoring components only (no `vp` — derived from the base schema's `x-score-formula`):

```json
{
  "game": "catan",
  "variants": [],
  "year_published": 1995,
  "date": "2026-04-19",
  "player_count": 3,
  "winners": [1],
  "notes": "Bea locked in longest road on turn 14.",
  "players": [
    {
      "name": "Alex",
      "identity": "red",
      "end_state": {
        "settlements": 3,
        "cities": 1,
        "roads": 8,
        "longest_road": false,
        "largest_army": true,
        "dev_card_vp": 0
      }
    },
    {
      "name": "Bea",
      "identity": "blue",
      "end_state": {
        "settlements": 2,
        "cities": 3,
        "roads": 12,
        "longest_road": true,
        "largest_army": false,
        "dev_card_vp": 0
      }
    },
    {
      "name": "Cam",
      "identity": "white",
      "end_state": {
        "settlements": 4,
        "cities": 1,
        "roads": 7,
        "longest_road": false,
        "largest_army": false,
        "dev_card_vp": 1
      }
    }
  ]
}
```

Derived scores via the base formula (booleans counted as 0/1): Alex = 3·1 + 1·2 + false·2 + true·2 + 0·1 = **7**; Bea = 2·1 + 3·2 + true·2 + false·2 + 0·1 = **10**; Cam = 4·1 + 1·2 + false·2 + false·2 + 1·1 = **7**. Bea is in `winners`. Matches.
