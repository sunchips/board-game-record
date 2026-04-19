# Secret Hitler — Base

- **Players:** 5–10
- **Year published:** 2016
- **Designers:** Max Temkin, Mike Boxleiter, Tommy Maranges
- **Rulebook:** <https://www.secrethitler.com/assets/Secret_Hitler_Rules.pdf>

Four end conditions; first met wins the game for that side:

| Side     | Condition                                                                          |
| -------- | ---------------------------------------------------------------------------------- |
| Liberals | **5 liberal policies** enacted.                                                    |
| Liberals | **Hitler assassinated** via the Execution presidential power.                      |
| Fascists | **6 fascist policies** enacted.                                                    |
| Fascists | **Hitler elected Chancellor** after ≥ 3 fascist policies are on the board.         |

## End state

Game-state totals that apply to everyone at the table — **replicate across players**.

| Key                     | Type    | Meaning                                                                   |
| ----------------------- | ------- | ------------------------------------------------------------------------- |
| `policies_liberal`      | int 0–5 | Liberal policies enacted.                                                 |
| `policies_fascist`      | int 0–6 | Fascist policies enacted.                                                 |
| `hitler_chancellor_win` | bool    | Game ended because Hitler was elected Chancellor (fascist win).           |
| `hitler_assassinated`   | bool    | Game ended because Hitler was shot (liberal win).                         |

Use the core `eliminated` flag for players who were executed by the Execution power.

## Identity

Hidden roles: `liberal`, `fascist`, `hitler`.

## Team

Use the core `team` field: `1` = liberals, `2` = fascists (including Hitler).

## Scoring

No `x-score-formula` and no score key. `winners` is the entire winning team (all players with `team = 1` on a liberal win, or all players with `team = 2` on a fascist win). Per-night investigation results, presidential powers invoked, and vote logs belong in `notes`.
