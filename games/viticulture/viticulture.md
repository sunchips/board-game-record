# Viticulture — Base (Essential Edition)

- **Players:** 1–6
- **Year published:** 2013 (Essential Edition, 2015)
- **Designers:** Jamey Stegmaier, Alan Stone
- **Rulebook:** <https://stonemaiergames.com/games/viticulture/rules-and-resources/>

The year a player crosses **20 VP** at the end of any turn triggers game end; play finishes the current year, then whoever has the most VP wins.

## End state

| Key           | Type     | Meaning                                                                                       |
| ------------- | -------- | --------------------------------------------------------------------------------------------- |
| `vp`          | int      | Final VP — **authoritative score**. Trigger for game end: any player reaches 20 VP.           |
| `lira`        | int      | Coins in hand at game end.                                                                    |
| `workers`     | int 3–7  | Total workers on the player's mat (including the Grande worker; starts at 3, max 7).          |
| `residuals`   | int 0–5  | Position on the Residual Payment track (income per year).                                     |
| `structures`  | int 0–8  | Structures built (Trellis, Irrigation, Yoke, Windmill, Cottage, Tasting Room, Medium Cellar, Large Cellar). |
| `vine_cards`  | int      | Vine cards planted in fields at game end.                                                     |
| `wine_tokens` | int      | Wines aged in the cellar at game end (not yet used to fill orders).                           |
| `orders_filled` | int    | Wine-order cards completed over the game.                                                     |

## Identity

Player colours: `green`, `yellow`, `red`, `blue`, `purple`, `orange`. Mama & Papa cards determine starting assets but aren't a persistent identity — note them in `notes` when relevant.

## Scoring

No `x-score-formula` — `vp` is the authoritative score. VP comes from filling orders, hosting special-visitor cards, reaching residual milestones, and completing the Harvester / Organizer-style end-game triggers. Ties broken by `lira`.
