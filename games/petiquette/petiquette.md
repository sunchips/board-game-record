# Petiquette — Base

- **Players:** 2–6
- **Year published:** 2025
- **Designer:** Thomas Sellner
- **Publisher:** Oink Games
- **Rulebook:** <https://oinkgames.com/en/games/analog/petiquette/>

Each card combines one of three animals, one of three hats, and a number from 1 to 5. Each round a line-up of five random cards is revealed; players study it for a pattern and secretly choose the card they feel best "fits". There is no objectively correct answer — you score when another player picks the same card you did. A cooperative mode (everyone guesses one player's secret choice) also exists, but records use the competitive scoring below.

## End state

| Key       | Type | Meaning                                                                          |
| --------- | ---- | -------------------------------------------------------------------------------- |
| `score`   | int  | The player's final score. **Authoritative** — highest score wins.                |
| `matches` | int  | Rounds in which the player's chosen card matched at least one other player's.    |

## Identity

Petiquette has no factions, colours, or fixed roles. Leave `identity` unset.

## Scoring

No `x-score-formula` — scoring is match-based rather than a linear sum of components, so `score` is the authoritative final total. The highest scorer(s) appear in `winners`; ties list every tied player.
