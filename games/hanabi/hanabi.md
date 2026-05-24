# Hanabi — Base

- **Players:** 2–5 (fully cooperative)
- **Year published:** 2010
- **Designer:** Antoine Bauza
- **Rulebook:** <https://www.ultraboardgames.com/hanabi/game-rules.php>

Players hold their hand facing outward — you see everyone's cards but your own. On your turn you give a hint (spends one hint token), play a card from your hand (legal if it's the next number in that color's firework, otherwise a fuse blows), or discard (recovers one hint token). The game ends when the third fuse blows (immediate loss, score is conventionally 0), when all five fireworks reach 5 (perfect 25), or one round after the deck runs out. Final score is the sum of the highest card played in each color — out of a maximum of 25.

## End state

Cooperative outcome — all players in a record share the same end state.

| Key                       | Type      | Meaning                                                              |
| ------------------------- | --------- | -------------------------------------------------------------------- |
| `score`                   | int 0–25  | Final score (sum of the highest card played per color). Authoritative. |
| `firework_red`            | int 0–5   | Highest red card played.                                             |
| `firework_yellow`         | int 0–5   | Highest yellow card played.                                          |
| `firework_green`          | int 0–5   | Highest green card played.                                           |
| `firework_blue`           | int 0–5   | Highest blue card played.                                            |
| `firework_white`          | int 0–5   | Highest white card played.                                           |
| `fuse_tokens_remaining`   | int 0–3   | Fuse tokens left when the game ended (0 = exploded).                 |
| `hint_tokens_remaining`   | int 0–8   | Hint tokens left when the game ended.                                |
| `perfect_score`           | bool      | True iff `score == 25`.                                              |
| `exploded`                | bool      | True iff the third fuse was spent (the show ended in disaster).      |

## Identity

Hanabi has no factions or roles. Players sit around the table; there is no identity field.

## Scoring

No `x-score-formula` — `score` is authoritative. Hanabi is fully cooperative, so `winners` follows the all-or-nothing convention from [SCHEMA.md](../../docs/SCHEMA.md#cooperative-games):

- **Team win** → list every player index, e.g. `"winners": [0, 1, 2, 3]` for a four-player game. The conventional bar is `score == 25`, but a group can choose to call any agreed outcome a "win" (e.g. "we counted 24 as a win") and document the threshold in `notes`.
- **Team loss** (typically `exploded == true`, or a sub-target score the group considers a loss) → `"winners": []`. The score still lives in `end_state.score` regardless.

Example loss-shape:

```json
{
  "game": "hanabi",
  "date": "2026-05-24",
  "player_count": 4,
  "winners": [],
  "notes": "Third fuse blew on the white 3 — we'd lost track of which white was still in hand.",
  "players": [
    { "name": "Alex", "end_state": { "score": 0, "exploded": true, "fuse_tokens_remaining": 0, "firework_red": 4, "firework_yellow": 2, "firework_green": 3, "firework_blue": 4, "firework_white": 2, "hint_tokens_remaining": 4, "perfect_score": false } }
  ]
}
```
