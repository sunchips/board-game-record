# Naming conventions

## Encoding

All JSON records and markdown files in this repo are **UTF-8**. Player names, notes, identity values, rules summaries — anything that's a free-form string — can use any Unicode script. A record with `"name": "たろう"` or `"notes": "近い勝負だった"` is fully supported.

## Slugs

`game` and `variants` entries are **ASCII-only, lowercase, hyphen-separated** slugs. Neither ever carries a year suffix — a game's publication year lives in the separate `year_published` field.

- `game` pattern: `^[a-z0-9]+(-[a-z0-9]+)*$`
- `variants` item pattern: `^[a-z0-9]+(-[a-z0-9]+)*$`

Slugs stay ASCII because they become filesystem paths, URLs, and grep-targets — portability beats representing the game's native title here. Capture the original title inside the game's `README.md` and `<slug>.md` rules summary instead.

### Slugification rules

Apply in order to the printed title:

1. **Replace `&` with the word `and`, surrounded by spaces** (so `Cities & Knights` → `Cities and Knights` before later steps run).
2. **Drop apostrophes** (don't turn them into hyphens): `It's` → `its`, not `it-s`.
3. **Transliterate non-ASCII** to the common Latin title when one exists: `街コロ` → `machi-koro`.
4. **Replace every other run of non-alphanumeric characters** (spaces, periods, colons, exclamation marks, slashes, dashes) with a single hyphen.
5. **Lowercase everything.**
6. **Collapse consecutive hyphens** and **trim** leading/trailing hyphens.

### Examples covering the edge cases

| Printed title                     | Slug                               | Why                                                                                                |
| --------------------------------- | ---------------------------------- | -------------------------------------------------------------------------------------------------- |
| Catan                             | `catan`                            | Trivial.                                                                                           |
| The King Is Dead                  | `the-king-is-dead`                 | Spaces → hyphens.                                                                                  |
| Cities & Knights                  | `cities-and-knights`               | `&` spelled out.                                                                                   |
| It's a Wonderful World            | `its-a-wonderful-world`            | Apostrophe dropped.                                                                                |
| Sushi Go!                         | `sushi-go`                         | `!` dropped.                                                                                       |
| Clank! In! Space!                 | `clank-in-space`                   | Multiple `!` dropped.                                                                              |
| St. Petersburg                    | `st-petersburg`                    | `. ` collapses to one hyphen.                                                                      |
| Dr. Eureka                        | `dr-eureka`                        | Same.                                                                                              |
| Codenames: Deep Undercover        | `codenames-deep-undercover`        | `: ` collapses to one hyphen.                                                                      |
| A Game of Thrones: The Board Game | `a-game-of-thrones-the-board-game` | Long title, same rules.                                                                            |
| Magic: The Gathering              | `magic-the-gathering`              | —                                                                                                  |
| 7 Wonders                         | `7-wonders`                        | Digits are fine.                                                                                   |
| T.I.M.E Stories                   | `t-i-m-e-stories`                  | Each letter is its own token because `.` separates them — mechanical rule, no pronunciation guess. |
| P.I.                              | `p-i`                              | Same.                                                                                              |
| M.U.L.E.                          | `m-u-l-e`                          | Same — even though it's pronounced "mule", the dots make each letter a separate token.             |
| D&D                               | `d-and-d`                          | `&` → `-and-`.                                                                                     |
| Machi Koro (街コロ)               | `machi-koro`                       | Transliterate to common Latin title.                                                               |
| HeroQuest                         | `heroquest`                        | Cover prints it as one word.                                                                       |

The mechanical rule (`.` always separates) is intentional — it avoids per-game judgment calls about how an acronym is pronounced.

## Game identifier

A record identifies its game with the `game` slug plus an optional `variants` list:

```json
"game": "catan",
"variants": ["seafarers"]
```

`variants` defaults to `[]` when the record is for the base game. Multiple variants can be listed; order doesn't matter.

`year_published` lives alongside as pure metadata, except when two games share a printed title — see [Disambiguation](#disambiguation).

## Disambiguation

Three real-world edge cases that need explicit resolution:

### Identical printed titles for different games

Some titles are reused across unrelated games — e.g. **Coup** (1988, Milton Bradley) and **Coup** (2012, Rikki Tahta) are different games with the same English title.

The `game` field stays as the bare slug (`coup`) in both records — slugs never carry years. Instead:

1. Both records set `year_published` to their game's original publication year.
2. At the filesystem, both games' folders take a `.YYYY` suffix (`games/coup.1988/` and `games/coup.2012/`) and the bare `games/coup/` folder does not exist. The folder name is a filesystem disambiguator, not a slug.

Records look like:

```json
{ "game": "coup", "year_published": 2012, "variants": [], ... }
{ "game": "coup", "year_published": 1988, "variants": [], ... }
```

Folder layout:

```
games/coup.1988/
├── coup.schema.json        # base
├── coup.md
└── <expansion>.schema.json

games/coup.2012/
├── coup.schema.json        # base
├── coup.md
└── reformation.schema.json
```

Note that the base schema inside each folder is still named `coup.schema.json` — the year only lives on the folder.

The validator resolves the folder as follows: try `games/<game>/`; if that doesn't exist and `year_published` is set, try `games/<game>.<year_published>/`. If neither resolves, the record fails validation.

Year is chosen over publisher or designer because it's objectively lookupable and stable over time (a game's publisher can change; its first publication year does not).

### Transliteration of non-Latin-script titles

Step 3 of slugification says "transliterate to the common Latin title". To keep that deterministic, follow the **title as listed on BoardGameGeek** whenever one exists — BGG has done the romanization call already, so contributors don't each pick their own convention. For games without a BGG entry, default to Hepburn (Japanese), Pinyin (Mandarin), and ALA-LC (Cyrillic/Greek).

### Spacing ambiguity in run-together titles

Use the title **exactly as printed in the rulebook** (prefer the rulebook over cover art, since marketing typography sometimes compresses or stylizes the canonical title). If the rulebook says `HeroQuest` as one word, the slug is `heroquest`. If it says `Hero Quest` as two words, the slug is `hero-quest`. Don't second-guess the publisher's spacing.

## Editions, expansions, and reprints

A "new edition" can mean many things — a reprint with updated art, a rules revision, or a standalone game sharing a brand name. Each maps to one of three patterns.

### 1. Cosmetic reprint or minor rule clarification

Same rules, tweaked wording, new art, updated components. E.g. _Catan 4th ed._ → _5th ed._, _Splendor_ core-rules reprint.

- No new schema, no new variant.
- Document the delta in a short "Edition notes" section of the base `<game>.md`.
- For a specific session under a specific edition, put the edition name in `record.notes`.

### 2. Meaningfully different rules within the same brand

The game is still sold as the same title, but scoring components, `end_state` keys, player-count bounds, or faction roster change. E.g. _Scythe Modular Board_, _Puerto Rico 2020 Anniversary_, _7 Wonders 2nd ed._

- **Add a new variant schema** in the existing game folder, scoped to the delta only:
  ```
  games/puerto-rico/
  ├── puerto-rico.schema.json   # base
  ├── puerto-rico.md
  ├── 2020.schema.json          # 2020 edition delta
  └── 2020.md
  ```
- Records list the edition in `variants`, e.g. `{ "game": "puerto-rico", "variants": ["2020"] }`.
- Pick the most durable edition slug: a year (`2020`), a publisher tag (`anniversary`), or a rules-version name (`definitive`). Year is usually most stable.

### 3. Standalone game that shares a brand

Different box, different player counts, incompatible rules — really a separate game. E.g. _Codenames Duet_, _Pandemic Legacy: Season 1_, _Dune: Imperium_ (vs. older _Dune_).

- **Its own top-level folder** with its own slug: `games/codenames-duet/`.
- Records use `{ "game": "codenames-duet" }` (empty `variants`).
- If the printed title is identical to an existing game's title, set `year_published` per [Disambiguation](#identical-printed-titles-for-different-games).

### Promotion rubric

Default to case 1 (just prose). Promote to case 2 (a new variant) if **any** of these apply:

1. `end_state` keys change (new scoring category added or removed).
2. `x-score-formula` multipliers change.
3. `player_count` bounds change.
4. `identity` enum changes (factions/colours/roles added or removed).

Promote to case 3 (separate game) when the box is sold as a distinct product with different core rules — typically when BGG lists it as its own game rather than an edition of the existing one.

## Expansion stacking

Variant schemas are **pure deltas** — each one describes only what it adds on top of the base. To record a session with multiple expansions active, list every one in `variants`:

```json
{
  "game": "catan",
  "variants": ["seafarers", "cities-and-knights"],
  ...
}
```

The validator loads `catan.schema.json`, `seafarers.schema.json`, and `cities-and-knights.schema.json` from the game folder and unions them: the combined `end_state` accepts keys from the base plus both expansions, `identity` enums are unioned, and `x-score-formula` multipliers are merged. If two schemas disagree on the type of a shared key or the multiplier of a shared formula entry, the validator errors and the conflict has to be resolved in the schemas.

There are no pre-generated stacked schema files — the union happens at validation time.

## Folder layout

```
games/<game>/                 # or games/<game>.<year>/ on disambiguation
├── README.md                 # overview, list of variants
├── <game>.schema.json        # base ruleset
├── <game>.md                 # base rules summary + rulebook link
├── <variant>.schema.json     # expansion/edition delta (zero or more)
└── <variant>.md
```

Session records live in a database, not under this repo — see the top-level [`README.md`](../README.md).
