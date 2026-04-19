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
| `eliminated` | bool | yes | Whether the player was knocked out before the game ended. |
| `end_state` | object | yes | Map of everything the player holds at game end: VP, coins, resources, cards, buildings, units, tiles, employees, territories, etc. Keys constrained per variant; values are integers. |

There's no separate `score` field. For games where score matters, the variant defines a `vp` (or `coins` / `points`) key in `end_state`. For games where it doesn't (Coup, Secret Hitler, Codenames), nothing of the sort is required. Per-unit score breakdowns go in `notes`.

## Cross-field rules (enforced by the validator)

- `player_count == len(players)`
- Every entry in `winners` is a valid index: `0 <= w < len(players)`

## Variant schemas

A variant schema constrains `end_state` keys (and optionally `identity` values) to just the ones that game supports. It typically uses:

```json
"properties": {
  "players": {
    "items": {
      "properties": {
        "end_state": {
          "propertyNames": { "enum": ["vp", "settlements", "cities", "roads", ...] }
        },
        "identity": { "enum": ["red", "blue", "white", "orange"] }
      }
    }
  }
}
```

See individual `games/<slug>/<slug>.schema.json` files for examples once games are added.

## Example record

Here's a minimal valid record (validates against core only — will fail without a variant schema present; see per-game folders for real examples):

```json
{
  "game": "example",
  "variant": "base",
  "date": "2026-04-19",
  "player_count": 3,
  "winners": [1],
  "notes": "Close game — decided on final turn.",
  "players": [
    { "name": "Alex", "eliminated": false, "end_state": { "vp": 8 } },
    { "name": "Bea",  "eliminated": false, "end_state": { "vp": 10 } },
    { "name": "Cam",  "eliminated": false, "end_state": { "vp": 7 } }
  ]
}
```
