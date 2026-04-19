# Catan — Base

- **Players:** 3–4
- **Year published:** 1995
- **Designer:** Klaus Teuber
- **Rulebook:** <https://www.catan.com/sites/default/files/2021-06/catan_base_rules_2020_200707.pdf>

## End state

| Key              | Type | Meaning                                                                 |
| ---------------- | ---- | ----------------------------------------------------------------------- |
| `settlements`    | int  | Settlements on the board (not yet upgraded to cities).                  |
| `cities`         | int  | Cities on the board.                                                    |
| `roads`          | int  | Roads built. Not scored directly.                                       |
| `longest_road`   | bool | Holds the Longest Road card.                                            |
| `largest_army`   | bool | Holds the Largest Army card.                                            |
| `dev_card_vp`    | int  | Victory Point dev cards revealed.                                       |
| `knights_played` | int  | Cumulative knights played. Not scored; useful for verifying Largest Army. |

## Identity

Player colours: `red`, `blue`, `white`, `orange`.

## Scoring

Derived from `x-score-formula`:

```
score = settlements·1 + cities·2 + longest_road·2 + largest_army·2 + dev_card_vp·1
```

Booleans count as 0/1. First player to reach 10 VP on their own turn wins; at most one player holds each of `longest_road` and `largest_army` at any time.
