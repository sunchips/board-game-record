# Everdell — Base

- **Players:** 1–4
- **Year published:** 2018
- **Designer:** James A. Wilson
- **Rulebook:** <https://cdn.svc.asmodee.net/production-starlinggames/uploads/2021/05/Everdell-Rulebook-2021.pdf>

The game ends when every player has passed through Autumn. Each player totals VP from their city's cards, point tokens, claimed events, journey destinations, and prosperity bonuses.

## End state

| Key             | Type     | Meaning                                                                                        |
| --------------- | -------- | ---------------------------------------------------------------------------------------------- |
| `vp`            | int      | Final VP — **authoritative score** (prosperity cards scale non-linearly on tableau contents).  |
| `base_vp`       | int      | VP from the printed corner values of cards in the player's city.                               |
| `point_tokens`  | int      | VP tokens placed on cards or claimed from events/journey during play.                          |
| `event_vp`      | int      | VP from basic and special events claimed.                                                      |
| `journey_vp`    | int      | VP from journey destinations reached.                                                          |
| `prosperity_vp` | int      | VP from purple prosperity cards (Wife/Husband, King, Queen, Architect, Judge, etc.).           |
| `constructions` | int 0–15 | Construction cards in the player's city at game end.                                           |
| `critters`      | int 0–15 | Critter cards in the player's city at game end.                                                |

## Identity

Everdell's leaders (Rugwort etc.) are not part of base setup; omit `identity` unless playing _Bellfaire_.

## Scoring

No `x-score-formula` — `vp` is the authoritative score. A city holds at most 15 cards (constructions + critters). Ties broken by leftover resources (twigs + resin + pebbles + berries); record the tiebreaker in `notes` if it mattered.
