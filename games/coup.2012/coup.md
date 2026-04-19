# Coup — Base

- **Players:** 2–6
- **Year published:** 2012
- **Designer:** Rikki Tahta
- **Rulebook:** <https://www.indieboardsandcards.com/wp-content/uploads/2024/05/Coup-Rules.pdf>

Each player starts with **2 influence** (two face-down character cards) and 2 coins. Players take actions that either cost coins or claim a character's power; any claim can be challenged, and any character-block can be challenged. Losing a challenge or an attack costs one influence (flip a card face-up). **Lose both and you're eliminated.** The last player with any influence remaining wins.

## End state

| Key                    | Type    | Meaning                                                                                |
| ---------------------- | ------- | -------------------------------------------------------------------------------------- |
| `coins`                | int 0–12 | Coins in hand at game end.                                                            |
| `influences_remaining` | int 0–2 | Face-down influence cards still held (0 = eliminated — also set the core `eliminated` flag). |

Use the core `eliminated` flag for players knocked out before the last hand. The winner is the player whose `influences_remaining > 0` when everyone else is eliminated.

## Identity

Coup uses hidden characters — a player's roles change as they exchange cards with the court deck. Omit `identity`.

## Scoring

No `x-score-formula` and no score key — Coup is pure elimination. `winners` lists the sole survivor (or, rarely, a settled draw; record the circumstance in `notes`).
