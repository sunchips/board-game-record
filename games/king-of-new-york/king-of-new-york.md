# King of New York — Base

- **Players:** 2–6
- **Year published:** 2014
- **Designer:** Richard Garfield
- **Rulebook:** <https://cdn.1j1ju.com/medias/ca/8d/d2-king-of-new-york-rulebook.pdf>

Win condition is either/or:

1. Reach **20 Stars** on your own turn, **or**
2. Be the **last monster alive** (every opponent at 0 hearts).

## End state

| Key                 | Type     | Meaning                                                                                  |
| ------------------- | -------- | ---------------------------------------------------------------------------------------- |
| `vp`                | int 0–20 | Stars at game end — **authoritative score**. 20 triggers the VP-win condition.           |
| `hearts`            | int 0–10 | Remaining health. 0 = eliminated.                                                        |
| `energy`            | int      | Unspent energy tokens.                                                                   |
| `power_cards`       | int      | Keep cards held at game end.                                                             |
| `superstar`         | bool     | Holds the Superstar badge at game end.                                                   |
| `statue_of_liberty` | bool     | Holds the Statue of Liberty badge at game end.                                           |

Use the core `eliminated` flag for monsters knocked out before game end.

## Identity

Monsters: `captain-fish`, `drakonis`, `kong`, `meka-dragon`, `sheriff`, `the-king`.

## Scoring

No `x-score-formula` — Stars (`vp`) is the authoritative value. VP comes from Manhattan zone control, dice combos (three-of-a-kind), destroying buildings, the Superstar badge, and keep-card effects. When the game ends by elimination, the survivor wins regardless of VP total.
