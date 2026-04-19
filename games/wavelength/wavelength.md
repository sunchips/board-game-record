# Wavelength — Base

- **Players:** 2–12 (2 teams)
- **Year published:** 2019
- **Designers:** Wolfgang Warsch, Alex Hague, Justin Vickers
- **Rulebook:** <https://cdn.shopify.com/s/files/1/0260/2601/3992/files/Wavelength_Rulebook_2024.pdf>

Teams take turns delivering psychic clues and guessing targets on a spectrum. Per round: 4 points for a bullseye (centre zone), 3 for the inner zone, 2 for the outer zone. The off-team scores 1 bonus by guessing which side of the target the dial sits on. First team to **10 points** wins. A team can also win on the _Left-Right_ finale if the dial is in perfect centre after their guess.

## End state

Team-level scoring, replicated per player within a team.

| Key           | Type     | Meaning                                                              |
| ------------- | -------- | -------------------------------------------------------------------- |
| `team_score`  | int 0–10 | The player's team's final score. **Authoritative** — 10 wins.        |
| `bullseyes`   | int      | Bullseye (4-point) rounds for the player's team.                     |
| `rounds_psychic` | int   | Rounds this player served as Psychic for their team.                 |

## Identity

Wavelength has no factions. Use the core `team` field: `1` = left team, `2` = right team.

## Scoring

No `x-score-formula` — `team_score` is the authoritative team score. Individual player scoring doesn't exist; winning-team members are all listed in `winners`.
