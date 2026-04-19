# Hues and Cues — Base

- **Players:** 3–10
- **Year published:** 2020
- **Designer:** Scott Brady
- **Rulebook:** <https://cdn.shopify.com/s/files/1/0561/2260/6593/files/Hues_and_Cues_Rules.pdf>

Each round a cue giver selects a colour and gives a one-word cue; everyone else places a guess cone. A second two-word cue follows and a second cone is placed. Cones on the target swatch score 3 VP, on the inner ring 2 VP, on the outer ring 1 VP. The cue giver scores 1 VP per cone in the outer ring, 2 VP per cone in the inner ring, 3 VP per cone on the exact target.

Play continues until every player has given the configured number of cues (varies by player count). Highest VP wins — first to 30 is the commonly used target in the rulebook's longer variant.

## End state

| Key           | Type | Meaning                                                                   |
| ------------- | ---- | ------------------------------------------------------------------------- |
| `vp`          | int  | Final VP — **authoritative score**.                                       |
| `cues_given`  | int  | Rounds this player was the cue giver.                                     |
| `bullseyes`   | int  | Times this player's guess landed exactly on the target swatch.            |

## Identity

No factions. The ten cone colours are purely seat markers — omit `identity`.

## Scoring

No `x-score-formula` — `vp` is recorded directly. Ties broken by `bullseyes`, then by a one-round colour-guess-off per the rulebook.
