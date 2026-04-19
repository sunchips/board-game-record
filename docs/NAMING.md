# Naming conventions

## Encoding

All JSON records and markdown files in this repo are **UTF-8**. Player names, notes, identity values, rules summaries — anything that's a free-form string — can use any Unicode script. A record with `"name": "たろう"` or `"notes": "近い勝負だった"` is fully supported.

## Slugs

`game` and `variant` values are **ASCII-only, lowercase, hyphen-separated** slugs. The `game` slug may optionally carry a `.YYYY` year suffix to disambiguate distinct games sharing the same printed title (see [Disambiguation](#disambiguation)).

- `game` pattern: `^[a-z0-9]+(-[a-z0-9]+)*(\.[0-9]{4})?$`
- `variant` pattern: `^[a-z0-9]+(-[a-z0-9]+)*$` (no year suffix)

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
| Coup (1988, Milton Bradley) | `coup.1988` | Year-suffix disambiguates from 2012 Coup. |
| HeroQuest | `heroquest` | Cover prints it as one word. |

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

Examples: `catan`, `catan.seafarers`, `scythe.invaders-from-afar`, `everdell.pearlbrook`, `coup.1988`, `coup.1988.expansion-one`.

Parsing the display form: the `game` field is the whole slug before the variant, which may include a `.YYYY` year suffix. The variant (when present) follows the last `.` — but since the year is always exactly 4 digits and `variant` cannot be 4 digits alone, the split is unambiguous.

## Disambiguation

Three real-world edge cases that need explicit resolution:

### Identical printed titles for different games

Some titles are reused across unrelated games — e.g. **Coup** (1988, Milton Bradley) and **Coup** (2012, Rikki Tahta) are different games with the same English title.

Rule: the first game recorded in this repo keeps the bare slug. Any later game that collides with it gets a **`.YYYY` year suffix** using the game's original publication year.

- `coup` — the 2012 Tahta game (the common one)
- `coup.1988` — the earlier Milton Bradley game

The year suffix lives inside the `game` field itself:

```json
"game": "coup.1988",
"variant": "base"
```

Folder layout follows: `games/coup.1988/`, schema file `games/coup.1988/coup.1988.schema.json`, rules summary `games/coup.1988/coup.1988.md`. Variant files inside that folder use plain slugs (no year), e.g. `seafarers.schema.json`.

Year is chosen over publisher or designer because it's objectively lookupable and stable over time (a game's publisher can change; its first publication year does not).

### Transliteration of non-Latin-script titles

Step 3 of slugification says "transliterate to the common Latin title". To keep that deterministic, follow the **title as listed on BoardGameGeek** whenever one exists — BGG has done the romanization call already, so contributors don't each pick their own convention. For games without a BGG entry, default to Hepburn (Japanese), Pinyin (Mandarin), and ALA-LC (Cyrillic/Greek).

### Spacing ambiguity in run-together titles

Use the title **exactly as printed on the box/rulebook**. If the cover says `HeroQuest` as one word, the slug is `heroquest`. If it says `Hero Quest` as two words, the slug is `hero-quest`. Don't second-guess the publisher's spacing.

## Editions, expansions, and reprints

A "new edition" can mean many things — a reprint with updated art, a rules revision, or a standalone game sharing a brand name. Each maps to one of three patterns.

### 1. Cosmetic reprint or minor rule clarification

Same rules, tweaked wording, new art, updated components. E.g. *Catan 4th ed.* → *5th ed.*, *Splendor* core-rules reprint.

- No new schema, no new variant.
- Document the delta in a short "Edition notes" section of the base `<game>.md`.
- For a specific session under a specific edition, put the edition name in `record.notes`.

### 2. Meaningfully different rules within the same brand

The game is still sold as the same title, but scoring components, `end_state` keys, player-count bounds, or faction roster change. E.g. *Scythe Modular Board*, *Puerto Rico 2020 Anniversary*, *7 Wonders 2nd ed.*

- **Add a new variant file** in the existing game folder:
  ```
  games/puerto-rico/
  ├── puerto-rico.schema.json   # original base
  ├── puerto-rico.md
  ├── 2020.schema.json          # 2020 edition
  └── 2020.md
  ```
- Records use `{ "game": "puerto-rico", "variant": "2020" }`.
- Pick the most durable edition slug: a year (`2020`), a publisher tag (`anniversary`), or a rules-version name (`definitive`). Year is usually most stable.
- Inside the schema file, the informational `"type"` field is `"edition"` (sibling of `"base"` and `"expansion"`). Purely documentation — the validator doesn't read it.

### 3. Standalone game that shares a brand

Different box, different player counts, incompatible rules — really a separate game. E.g. *Codenames Duet*, *Pandemic Legacy: Season 1*, *Dune: Imperium* (vs. older *Dune*).

- **Its own top-level folder** with its own slug: `games/codenames-duet/`.
- Records use `{ "game": "codenames-duet" }` (variant stays `"base"`).
- If the printed title is identical to an existing game's title, add a `.YYYY` year suffix per [Disambiguation](#disambiguation).

### Promotion rubric

Default to case 1 (just prose). Promote to case 2 (a new variant) if **any** of these apply:

1. `end_state` keys change (new scoring category added or removed).
2. `x-score-formula` multipliers change.
3. `player_count` bounds change.
4. `identity` enum changes (factions/colours/roles added or removed).

Promote to case 3 (separate game) when the box is sold as a distinct product with different core rules — typically when BGG lists it as its own game rather than an edition of the existing one.

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
└── <variant>.md
```

Session records live in a database, not under this repo — see the top-level [`README.md`](../README.md).
