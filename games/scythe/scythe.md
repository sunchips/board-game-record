# Scythe — Base

- **Players:** 1–5
- **Year published:** 2016
- **Designer:** Jamey Stegmaier
- **Rulebook:** <https://stonemaiergames.com/games/scythe/rules-and-resources/>

The game ends the instant a player places their **sixth star**. Every player then totals coins.

## End state

| Key                    | Type     | Meaning                                                                                                |
| ---------------------- | -------- | ------------------------------------------------------------------------------------------------------ |
| `coins`                | int      | Final coin total — the **authoritative score** (Scythe's scoring is non-linear, so it isn't derived).  |
| `stars`                | int 0–6  | Stars placed on the Triumph Track. The 6th star ends the game.                                         |
| `popularity`           | int 0–18 | Popularity track value. Determines the scoring bracket (low 1–6, mid 7–12, high 13–18).                |
| `power`                | int 0–16 | Power-track value at game end.                                                                         |
| `territories`          | int      | Hexes controlled at game end (incl. lakes for factions that score them).                               |
| `resources`            | int      | Total resource tokens (wood + metal + oil + food) on the player's controlled territories at game end.  |
| `workers`              | int 2–8  | Workers on the board.                                                                                  |
| `mechs`                | int 0–4  | Mechs deployed.                                                                                        |
| `structures`           | int 0–4  | Structures built.                                                                                      |
| `recruits`             | int 0–4  | Recruits enlisted.                                                                                     |
| `upgrades`             | int 0–6  | Upgrades purchased.                                                                                    |
| `objectives_completed` | int 0–2  | Objective cards completed (each grants a star).                                                        |
| `factory_card`         | bool     | Holds the Factory card at game end (worth +3 coins, baked into `coins`).                               |

## Identity

Base factions: `saxony`, `nordic`, `crimea`, `rusviet`, `polania`.

Player mats (Industrial / Engineering / Patriotic / Mechanical / Agricultural and friends) aren't part of `identity`; record them in `notes` when they matter.

## Scoring

No `x-score-formula` — `coins` is the authoritative score. Final coins per player = (coins on hand) + (stars × popularity-bracket-rate) + (territories × bracket-rate) + (⌊resources/2⌋ × bracket-rate) + (structures × structure-bonus-card-rate) + (3 if `factory_card`). Bracket rates per Triumph track:

| Bracket          | per star | per territory | per resource pair |
| ---------------- | -------- | ------------- | ----------------- |
| Low (1–6)        | 3        | 2             | 1                 |
| Mid (7–12)       | 4        | 3             | 2                 |
| High (13–18)     | 5        | 4             | 3                 |

Highest coin total wins; ties broken by popularity, then by territories.
