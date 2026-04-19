# Bunny Kingdom — Base

- **Players:** 2–4
- **Year published:** 2017
- **Designer:** Richard Garfield
- **Rulebook:** <https://cdn.1j1ju.com/medias/8f/ab/b6-bunny-kingdom-rulebook.pdf>

A game lasts four rounds. Between rounds 1–4 the map is scored; at the end of round 4, players also reveal and score their Golden Parchments. Highest VP wins.

## End state

| Key                 | Type | Meaning                                                                                               |
| ------------------- | ---- | ----------------------------------------------------------------------------------------------------- |
| `vp`                | int  | Final VP — **authoritative score** (fief scoring is multiplicative, so it isn't a linear formula).    |
| `fiefs`             | int  | Number of distinct fiefs (connected groups of controlled territories) at the final scoring.           |
| `cities`            | int  | Total cities on the map at game end.                                                                  |
| `towers`            | int  | Total towers (strongholds) placed.                                                                    |
| `fief_vp`           | int  | VP from the four round-end fief scorings (sum over rounds).                                           |
| `parchment_vp`      | int  | VP from Golden Parchments scored at the end of round 4.                                               |
| `golden_parchments` | int  | Count of Golden Parchments kept and scored.                                                           |

## Identity

Player colours: `red`, `blue`, `yellow`, `green`.

## Scoring

No `x-score-formula` — `vp` is the authoritative score. A fief scores `cities × resource_types`, summed across all a player's fiefs, summed across all four rounds; Golden Parchments add on top. Ties broken by `fiefs`, then by `cities`.
