# Parks — Base

- **Players:** 1–5
- **Year published:** 2019
- **Designer:** Henry Audubon
- **Rulebook:** <https://keymastergames.com/pages/parks-rules>

After four seasons (rounds) the game ends. Each player totals VP from visited parks, wildlife, photos, year bonuses, and leader goals.

## End state

| Key             | Type    | Meaning                                                                              |
| --------------- | ------- | ------------------------------------------------------------------------------------ |
| `vp`            | int     | Final VP — **authoritative score**.                                                  |
| `parks_visited` | int     | Park cards claimed.                                                                  |
| `park_vp`       | int     | VP from the face values of park cards (varies per park, 1–4 VP).                     |
| `photos`        | int     | Photograph tokens held at game end.                                                  |
| `wildlife`      | int     | Wildlife badges collected.                                                           |
| `year_bonus_vp` | int     | VP from year-bonus tokens taken at the end of each season.                           |
| `canteen`       | int 0–3 | Canteen upgrade level (number of upgrade slots filled).                              |
| `gear`          | int     | Gear cards owned at game end.                                                        |

## Identity

Hiker colours: `red`, `blue`, `green`, `yellow`, `orange`.

## Scoring

No `x-score-formula` — park cards have variable face values. Each photo is worth 1 VP, each wildlife badge 1 VP, plus park face values and year-bonus tokens. Ties broken by `photos`.
