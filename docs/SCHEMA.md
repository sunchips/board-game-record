# Schema

Every session record validates against two schemas:

1. **`schema/core.schema.json`** — cross-game fields (this document).
2. **`games/<game>/<variant>.schema.json`** — constrains `end_state` keys (and optionally `identity` values) for that specific game/variant.

Both must pass. JSON Schema draft 2020-12.

## Core fields

| Field | Type | Required | Captures |
|---|---|---|---|
| `game` | string | yes | Lowercase-hyphenated game slug. E.g. `catan`, `the-king-is-dead`. |
| `variant` | string | no (default `"base"`) | `"base"` or an expansion slug. Picks which variant schema validates the record. |
| `date` | string (ISO date) | yes | Calendar date the session was played, `YYYY-MM-DD`. |
| `player_count` | int | yes | Number of seated players. Must equal `len(players)`. |
| `winners` | int[] | yes | 0-based indices into `players[]`. One entry = solo win; multiple = tie or team win (list every teammate who shared the win). |
| `notes` | string | no | Free-form prose for anything the structured fields don't capture — elimination order, score breakdowns, house rules, what broke a tie, best-of-N round tallies, memorable moments. |
| `players` | array | yes | One entry per player, in seating order. Position in array = player index. |

## `players[]` fields

| Field | Type | Required | Captures |
|---|---|---|---|
| `name` | string | yes | Player's name/handle. Non-unique is fine — `winners` references by index. |
| `identity` | string | no | Single field covering colour / faction / civ / mat / hidden role — whatever the game uses to distinguish players. Variant schemas may constrain via `enum`. Examples: `"red"` (Catan), `"crimea"` (Scythe), `"liberal"` (Secret Hitler). |
| `team` | int | no | Team number for team games (e.g. `1` / `2`). Teammates share the value. Omit for free-for-all. |
| `eliminated` | bool | no | Whether the player was knocked out before the game ended. Omit entirely for games without elimination (Catan, Codenames, etc.); only include when the game has an elimination mechanic (Coup, Risk). |
| `end_state` | object | yes | Map of everything the player holds at game end: VP, coins, resources, cards, buildings, units, tiles, employees, territories, etc. Keys constrained per variant; values are integers. |

There's no separate `score` field. A player's score — when the game has one — is either:

- **derived** from `end_state` components, via a formula declared in the variant schema (see below); or
- **recorded directly** as a dedicated key in `end_state` (e.g. `coins` for Scythe, `vp` for games with non-linear scoring) when the formula can't be expressed simply.

Games without a score at all (Coup, Secret Hitler, Codenames) declare no formula and no score key. Per-unit score breakdowns for complex scoring live in `notes`.

## Cross-field rules (enforced by the validator)

- `player_count == len(players)`
- Every entry in `winners` is a valid index: `0 <= w < len(players)`

## Variant schemas

A variant schema constrains `end_state` keys (and optionally `identity` values) to just the ones that game supports, and optionally declares a **score formula** for derivation.

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
          "identity": {
            "enum": ["red", "blue", "white", "orange"]
          },
          "end_state": {
            "propertyNames": {
              "enum": [
                "settlements", "cities", "roads",
                "longest_road", "largest_army",
                "dev_card_vp", "knights_played"
              ]
            },
            "properties": {
              "longest_road": { "enum": [0, 1] },
              "largest_army": { "enum": [0, 1] }
            }
          }
        }
      }
    }
  }
}
```

See individual `games/<slug>/<slug>.schema.json` files for concrete examples once games are added.

### `x-score-formula` — deriving VP from components

When a variant defines `x-score-formula`, a player's score is computed as:

```
score = sum( end_state.get(key, 0) * multiplier for key, multiplier in formula.items() )
```

The formula is a flat `{key: integer_multiplier}` map. Keys must appear in the variant's `end_state.propertyNames.enum`. Boolean-style components (e.g. `longest_road`, `largest_army`) use 0/1 values and let the multiplier carry the point value.

When the formula is present:

- Records **do not** carry a `vp` (or similar) key — it's reconstructed from components.
- The variant's rules summary (`<variant>.md`) documents the formula in prose for humans.
- Tooling (including `tools/validate.py --show-scores`) uses the formula to display derived scores.

When a game's scoring isn't expressible as a simple linear sum (Scythe's popularity brackets, Everdell's unique-card tables), the variant **omits** `x-score-formula` and instead adds a dedicated score key like `coins` or `vp` to the `end_state` enum. The rules summary explains how that total was computed.

`x-score-formula` lives outside JSON Schema's standard vocabulary — the `x-` prefix marks it as an extension. JSON Schema validators ignore unknown top-level keywords, so schema validation is unaffected; only this repo's tooling reads the field.

## Example record

A Catan-style record, with scoring components only (no `vp` — derived from the variant's `x-score-formula`):

```json
{
  "game": "catan",
  "variant": "base",
  "date": "2026-04-19",
  "player_count": 3,
  "winners": [1],
  "notes": "Bea locked in longest road on turn 14.",
  "players": [
    {
      "name": "Alex",
      "identity": "red",
      "end_state": {
        "settlements": 3, "cities": 1, "roads": 8,
        "longest_road": 0, "largest_army": 1, "dev_card_vp": 0
      }
    },
    {
      "name": "Bea",
      "identity": "blue",
      "end_state": {
        "settlements": 2, "cities": 3, "roads": 12,
        "longest_road": 1, "largest_army": 0, "dev_card_vp": 0
      }
    },
    {
      "name": "Cam",
      "identity": "white",
      "end_state": {
        "settlements": 4, "cities": 1, "roads": 7,
        "longest_road": 0, "largest_army": 0, "dev_card_vp": 1
      }
    }
  ]
}
```

Derived scores via the formula shown above: Alex = 3·1 + 1·2 + 0·2 + 1·2 + 0·1 = **7**; Bea = 2·1 + 3·2 + 1·2 + 0 + 0 = **10**; Cam = 4·1 + 1·2 + 0 + 0 + 1·1 = **7**. Bea is in `winners`. Matches.
