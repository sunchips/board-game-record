# Naming conventions

## Encoding

All JSON records and markdown files in this repo are **UTF-8**. Player names, notes, identity values, rules summaries — anything that's a free-form string — can use any Unicode script. A record with `"name": "たろう"` or `"notes": "近い勝負だった"` is fully supported.

## Slugs

`game` and `variant` values are **ASCII-only, lowercase, hyphen-separated** slugs matching `^[a-z0-9]+(-[a-z0-9]+)*$`.

Slugs stay ASCII because they become filesystem paths, URLs, and grep-targets — portability beats representing the game's native title here. Capture the original title inside the game's `README.md` and `<slug>.md` rules summary instead.

### Slugification rules

Apply in order to the printed title:

1. **Replace `&` with ` and `** (spelled out).
2. **Drop apostrophes** (don't turn them into hyphens): `It's` → `its`, not `it-s`.
3. **Transliterate non-ASCII** to the common Latin title when one exists: `街コロ` → `machi-koro`.
4. **Replace every other run of non-alphanumeric characters** (spaces, periods, colons, exclamation marks, slashes, dashes) with a single hyphen.
5. **Lowercase everything.**
6. **Collapse consecutive hyphens** and **trim** leading/trailing hyphens.

### Examples covering the edge cases

| Printed title | Slug | Why |
|---|---|---|
| Catan | `catan` | Trivial. |
| The King Is Dead | `the-king-is-dead` | Spaces → hyphens. |
| Cities & Knights | `cities-and-knights` | `&` spelled out. |
| It's a Wonderful World | `its-a-wonderful-world` | Apostrophe dropped. |
| Sushi Go! | `sushi-go` | `!` dropped. |
| Clank! In! Space! | `clank-in-space` | Multiple `!` dropped. |
| St. Petersburg | `st-petersburg` | `. ` collapses to one hyphen. |
| Dr. Eureka | `dr-eureka` | Same. |
| Codenames: Deep Undercover | `codenames-deep-undercover` | `: ` collapses to one hyphen. |
| A Game of Thrones: The Board Game | `a-game-of-thrones-the-board-game` | Long title, same rules. |
| Magic: The Gathering | `magic-the-gathering` | — |
| 7 Wonders | `7-wonders` | Digits are fine. |
| T.I.M.E Stories | `t-i-m-e-stories` | Each letter is its own token because `.` separates them — mechanical rule, no pronunciation guess. |
| P.I. | `p-i` | Same. |
| M.U.L.E. | `m-u-l-e` | Same — even though it's pronounced "mule", the dots make each letter a separate token. |
| D&D | `d-and-d` | `&` → `-and-`. |
| Machi Koro (街コロ) | `machi-koro` | Transliterate to common Latin title. |

The mechanical rule (`.` always separates) is intentional — it avoids per-game judgment calls about how an acronym is pronounced.

## Game identifier

A record identifies its game with two fields:

```json
"game": "catan",
"variant": "seafarers"
```

`variant` defaults to `"base"` when the record is for the base game.

The canonical display/filename form is:

```
<game>               # when variant == "base"
<game>.<variant>     # when variant is an expansion slug
```

Examples: `catan`, `catan.seafarers`, `scythe.invaders-from-afar`, `everdell.pearlbrook`. Since slugs can't contain `.` (the ASCII-slug rule above), the first `.` in a display name is always the variant separator.

## Standalone editions vs. expansions

- A variant that extends a base game → lives in the base game's folder as `<variant>.schema.json` + `<variant>.md`. Records use `{ "game": "<base>", "variant": "<variant>" }`.
- A standalone edition that is its own game → lives in its own top-level folder. Records use `{ "game": "<edition-slug>" }` (variant stays `"base"`).

For example, Codenames Duet is standalone (different rules, different box, different player count), so it lives at `games/codenames-duet/` — not as a variant of `codenames`.

Minor revisions of the same base game (e.g. Catan 5e) do **not** get their own variant. Capture the difference in the base `<game>.md` and, for a specific session, in `record.notes`.

## Expansion stacking

v1 supports exactly one variant per record — either `"base"` or a single expansion slug. Multi-expansion sessions are recorded against whichever single variant dominated (and the others noted in `notes`), or they go unrecorded until stacked-variant schemas are introduced on demand. The naming convention for those, when/if added:

```
<game>.<variant1>.<variant2>.schema.json
```

## Folder layout

```
games/<game>/
├── README.md              # overview, list of variants
├── <game>.schema.json     # base variant
├── <game>.md              # base rules summary + rulebook link
├── <variant>.schema.json  # expansion (zero or more)
├── <variant>.md
└── records/
    └── YYYY-MM-DD-NNN.json
```

Record filenames: `<date>-<sequence>.json`, where sequence is a zero-padded count of games played that day (`001`, `002`, …). The filename is cosmetic — the validator reads the JSON to determine game/variant.
