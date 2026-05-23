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

No `x-score-formula` — `score` is authoritative. Since the game is fully cooperative, either every player index appears in `winners` (positive outcome) or `winners` is empty for a loss / explosion. The current core schema requires `winners.minItems: 1`, so for a 0-point loss list a single representative index (typically `0`) and use `notes` to clarify.
