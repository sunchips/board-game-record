# The King Is Dead — Base

- **Players:** 2–4
- **Year published:** 2015 (2nd edition, 2020)
- **Designer:** Peer Sylvester
- **Rulebook:** <https://osprey.nfshost.com/wp-content/uploads/2020/07/The-King-is-Dead-Rulebook.pdf>

Players alternate playing follower cards to shift cubes on the board. The game ends when the supply of cubes for the **last of the three factions** is exhausted. Then:

1. For each region, the faction with the most cubes **controls** it (ties resolved by region order).
2. The faction with **the most regions** becomes the next king's successor. The player with the most followers of that faction wins.
3. If the top-ranked faction is tied among players, fall through to the second-most-regions faction; if that ties too, the third. If still tied — **Normans invade**, everyone loses.

## End state

| Key                  | Type    | Meaning                                                                                |
| -------------------- | ------- | -------------------------------------------------------------------------------------- |
| `followers_welsh`    | int     | Welsh follower cards in hand at game end.                                              |
| `followers_scots`    | int     | Scots follower cards in hand at game end.                                              |
| `followers_english`  | int     | English follower cards in hand at game end.                                            |
| `supporters_placed`  | int 0–3 | Neutral supporter pieces placed into regions during the game (out of 3 per player).    |
| `regions_welsh`      | int 0–8 | Regions the Welsh faction controls at game end (game-state; replicate across players). |
| `regions_scots`      | int 0–8 | Regions the Scots faction controls at game end (game-state; replicate across players). |
| `regions_english`    | int 0–8 | Regions the English faction controls at game end (replicate across players).           |

## Identity

No assigned factions — every player holds cards of all three. Omit `identity`.

## Scoring

No `x-score-formula` and no dedicated score key. The winner is derived from followers vs region-control precedence, and on a total tie there is no winner — record that case by leaving `winners` with every player listed and explaining the Norman invasion in `notes` (or, if your tooling prefers a sole "no-winner" marker, use the convention from [SCHEMA.md](../../docs/SCHEMA.md)).
