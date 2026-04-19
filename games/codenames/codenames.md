# Codenames — Base

- **Players:** 2–8+ (designed for 4+, two teams with one spymaster each)
- **Year published:** 2015
- **Designer:** Vlaada Chvátil
- **Rulebook:** <https://czechgames.com/files/rules/codenames-rules-en.pdf>

25 codename cards are laid out 5×5. The key card assigns each to Red team, Blue team, Bystander, or Assassin. The starting team has **9 agents** to contact, the other team **8**. A team wins by contacting all its agents first. A team loses immediately if its operatives touch the assassin.

## End state

Game-state values that apply to everyone on the same team — **replicate across teammates**.

| Key                | Type    | Meaning                                                                                              |
| ------------------ | ------- | ---------------------------------------------------------------------------------------------------- |
| `agents_remaining` | int 0–9 | This team's agents still face-down at game end. 0 on the winning team (unless assassin-ended).       |
| `assassin_hit`     | bool    | This team revealed the assassin (instant loss for them — the other team wins regardless).            |
| `starting_team`    | bool    | This team went first (had 9 agents; the other team had 8).                                           |

## Identity

Roles: `spymaster`, `operative`.

## Team

Use the core `team` field: `1` = red, `2` = blue.

## Scoring

No `x-score-formula` and no score key — Codenames is binary win/loss per team. `winners` lists every member of the winning team.
