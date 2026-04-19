# Calico — Base

- **Players:** 1–4
- **Year published:** 2020
- **Designer:** Kevin Russ
- **Rulebook:** <https://cdn.1j1ju.com/medias/3f/f3/6c-calico-rulebook.pdf>

Game ends after every player has filled their 22-patch quilt. Score is the sum of three sources.

## End state

| Key              | Type | Meaning                                                                                      |
| ---------------- | ---- | -------------------------------------------------------------------------------------------- |
| `cats_vp`        | int  | VP from cats attracted to the quilt (each base-game cat scores 3/5/7/9/11 VP depending on which cat landed). |
| `buttons_vp`     | int  | VP from buttons: 3 VP per coloured button, plus 3 VP for the rainbow button bonus.           |
| `design_goal_vp` | int  | VP from the three design-goal tiles (partial satisfaction vs full satisfaction).             |

## Identity

Each player uses a randomly dealt quilt-back (different cat layouts and starting patches). It's a setup, not a persistent faction — omit `identity` and describe the quilt back in `notes` when relevant.

## Scoring

```
score = cats_vp + buttons_vp + design_goal_vp
```

Each component contributes with multiplier 1 (see the base schema's `x-score-formula`). Ties broken by buttons collected (not by button VP).
