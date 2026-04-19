# Jaipur — Base

- **Players:** 2
- **Year published:** 2009
- **Designer:** Sébastien Pauchon
- **Rulebook:** <https://cdn.1j1ju.com/medias/c1/a6/c1-jaipur-rulebook.pdf>

A match is a best-of-three. Each round ends when three good types are exhausted from the market; the player with the most rupees wins the round and takes a Seal of Excellence. First to **2 Seals** wins the match.

## End state

| Key            | Type    | Meaning                                                                                                |
| -------------- | ------- | ------------------------------------------------------------------------------------------------------ |
| `seals`        | int 0–2 | Seals of Excellence earned in the match. **Authoritative score** — 2 seals = match winner.             |
| `total_rupees` | int     | Total rupees accumulated across every round played (tiebreaker / performance stat, not the win cond.). |
| `bonus_tokens` | int     | Bonus tokens earned across the match (for selling 3+, 4, or 5 goods in a single sale).                 |
| `camel_wins`   | int 0–3 | Rounds in which this player held the largest Camel Herd and took the 5-rupee camel bonus.              |

## Identity

Jaipur has no factions or colours. Omit `identity`.

## Scoring

No `x-score-formula` — `seals` is the authoritative match score (and is discrete 0/1/2). Round-by-round rupee totals can be logged in `notes`.
