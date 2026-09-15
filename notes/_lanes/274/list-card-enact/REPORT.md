# REPORT — #274 lane LCE: ENACT s274-D1..D5 on the metas

**Files touched (2, both under `knowledge/components/`):** `list-items.meta.json`, `account-card.meta.json`.
**Method:** every edit is an INSERTION of an exact byte span into the existing file, proven by reconstruction — removing each span in reverse returns the ORIGINAL bytes (`==` on the raw string) and the result `json.loads`. No meta was ever `json.load`/`json.dump`-ed (`_inscribe_ruling.py` R2 discipline, the #179 defect). Enactment script kept in the lane scratch, not in the repo.
**Not committed** (lane rule). `notes/_REHEARSAL-LOG.jsonl` and `notes/_dream/_GRADE-DECISIONS.jsonl` show as modified in `git status` — they were **already dirty before this lane started**; not mine, not touched.

---

## 1. `knowledge/components/list-items.meta.json` — five spans

**S1 (b) `priority` + `when`** — inserted after the line `  "provides": "record-list",`:

```
  "priority": 60,
  "when": "records >= 2 AND the records are the same kind, each read ACROSS its own row AND surface in (none, bordered-per-record) — surface ALONE decides the container (s274-D1): unbordered ⇒ simple-list (one line per record) or structured-list (aligned fields); a bordered surface drawn around EACH record ⇒ card-list. Actions are a ROW property, allowed in any of the three, so they decide nothing. No field count, row count or column count gates this (s274-D4): the comparison test decides — if a field must be read DOWN a column across records, it is a table, not a list. A list-level heading is OPTIONAL on all three containers (s274-D5); a per-card title is a ROW field, distinct from the list heading. Beats table (roles.json when: \"default, read-mostly\") and data-grid (when: \"sort / filter / select / edit-in-place is required\") whenever each record is read across its own row; yields to timeline (when: \"time is the structure, records have happened\") and to tree (when: \"records nest\").",
```

**Why this gate.** Split on the FIRST em-dash, the GATE half is `records >= 2 AND the records are the same kind, each read ACROSS its own row AND surface in (none, bordered-per-record)`.
- `records >= 2` — legal field, `kind: count`; its `example` in `when-fields.json` is literally `records >= 2`. A list of one record is not a list.
- clause 2 carries **no operator**, so it is prose inside the gate and is not parsed (the V-B operator-token method the `$grammar` names). It is where the same-kind / read-across test sits.
- `surface in (none, bordered-per-record)` — legal field ("whether the arrangement paints a surface"), `in` is a legal operator. This is D1 **on the gate**: `surface` is the ONLY thing separating a list from a card, and because `list-items` now hosts all three containers it serves both values; the prose half says which value picks which variant.
- **No `actions` clause** — s274-D1 struck it ("actions might be allowable in a simple list in actuality"), so **no new `when` field was added**. `when-fields.json` is UNTOUCHED. Field counts after the change: `records 2 (list-items, timeline)`, `surface 2 (layout-utilities, list-items)`.
- The prose half carries D4's comparison test ("if a field must be read DOWN a column across records, it is a table, not a list") and D5's heading rule, plus the beats/yields sentence (s253-D1 R2 shape).

**Why `priority: 60`.** 60 is the band this repo uses for "the default of the role" (`button`, `layout-utilities`, `stat-card`, `app-shell-top-nav`, `navigations` all 60). **⚠ CONSEQUENCE, AND IT IS DAVE'S:** no other `record-list` provider carries a `priority`, so any number at all makes `list-items` the role's preferred term. The resolver now prints `preferred: role record-list PREFERRED TERM list-items (priority 60) — 7 co-provider(s)`, while `roles.json` still calls **table** the role's "default, read-mostly". The rulings did not settle that — see P2.

**S2 (c) `purpose` amendment BY ADDITION** — appended to the end of the existing `purpose` string, nothing rewritten. It ended `…a visual option of icon / avatar / image."`; after it, the same text plus:

> ` TWO LEVELS (s274-D2): the CONTAINERS are the variants simple-list, structured-list and card-list; the record ROWS (account, badge, item, review, review-detail, transaction) are parts any container holds, and card-list-row = simple-list-row — no separate row shape. `bullets` is typeset, not a record row.`

**S3 (a) row marks** — `,\n      "$level": "row"` inserted after the `use` value of each of the six record-row variants (account, badge, item, review, review-detail, transaction); `,\n      "$level": "typeset"` after `bullets`.

**Shape chosen, and why.** Checked how metas annotate before picking: across 137 metas the variant objects carry `name` (349) and `use` (349) and almost nothing else — `$displayName` 5, `$aliases` 5, `$since` 2, `$ruling` 1, `$why`/`$recipe`/`$semantics`/`$notFor` 1 each. So a `$`-prefixed annotation key on a variant is an **established, rare, additive** convention, and one new key reads machine-side where a sentence buried in `use` would not. No live schema constrains variant keys (the only `meta.schema.json` in the tree is under `_to_delete/`). `$level: "typeset"` for `bullets` is **my word, not Dave's** — his model names two levels and the brief says bullets is typeset rather than a record row; marked as a guess.

**S4 (a) three container variants** — inserted immediately before the `bullets` variant object, each `name` / `$level: "container"` / `use` / `$ruling: "s274-D2"`:
- `simple-list` — "a stack of same-kind records on ONE unbordered surface, one record per row, divided by a rule. List-level heading optional (s274-D5)."
- `structured-list` — Dave's name, replacing the proposal's "column-list"; fields align across records, still one unbordered surface; heading optional because in banking a structured row is self-describing; the D4 table test named.
- `card-list` — "the SAME rows, but the container draws a bordered surface around EACH record — that surface alone is what makes a record a card (s274-D1). card-list-row = simple-list-row; a per-card title is a ROW field, not the list heading (s274-D5)."

## 2. `knowledge/components/account-card.meta.json` — one span

`"$note"` inserted on its own line after `purpose`, by addition; `provides` NOT added, nothing else changed:

> `s274-D3 (Dave, #274, 2026-09-15): Account card STAYS $not-a-provider of record-list. A STACK of account cards is not this component turned into a provider — it is the card-list CONTAINER variant of list-items hosting account ROWS (s274-D2), and the composer reaches the stack through the record-list role. The bordered surface the container draws around each record is what makes it a card (s274-D1); nothing about this component changes and no provides is added.`

## 3. What I did NOT do, and why

- **`transaction-row` / `document-row` / `standing-order-mandate-row` — LEFT ALONE.** These are standalone metas and `record-list` providers in their own right; the ROWS in s274-D2 are the **variants of `list-items`**, which these three are not. A `$note` calling them "rows for a structured-list container" would assert a relation Dave did not rule, sitting next to their own `provides: record-list` saying the opposite. Declared, not silently skipped.
- **`when-fields.json` — UNTOUCHED.** No field addition was needed once D1 struck the `actions >= 1` clause. Zero lane additions under s273-D4.
- **`props.type` enum — NOT changed.** It carries an s142-D1 verdict. See P1.
- **`roles.json` — UNTOUCHED.** See P2/P3.
- **No commit, no `git stash/checkout/reset`, no `gen_kg_edges.py`, no `_build_all.py`.**

## 4. Proposals for Dave

- **P1 — `props.type` enum.** Today it is `account · badge · item · review · review-detail · transaction · bullets` — the ROWS only. If the three containers are variants, the prop selecting a variant is now a **two-level** selector. Options: (i) leave it — `type` stays the ROW selector, the container is chosen by a second prop (e.g. `container`, new); (ii) add the three container names to the same enum, flattening two levels onto one axis; (iii) split into `container` + `row`. **Recommendation: (iii), or (i) as the cheap hold.** Not enacted — props carry s142-D1 verdicts.
- **P2 — the `record-list` preferred term.** `priority: 60` on `list-items` makes it the role's preferred term over `table`, which `roles.json` still calls the default. Either `table` gets a higher number or `list-items` drops below it. **Dave's, one number.**
- **P3 — `roles.json`'s `when` for `list-items` is now contradicted by ruling.** It reads `"≤ 3 fields per item, tappable"`. s274-D4 says no field count gates anything; s274-D1 says the line is surface alone. Suggested one-line replacement: `"records read ACROSS their own row; surface decides simple/structured vs card"`. Not enacted — `roles.json` was outside this lane's write list.

## 5. Gates — verbatim

`python3 knowledge/_validate_roles_resolve.py` — the six FAILs are the INHERITED #261 `data-grid` `with`-slugs, unchanged in count and text; nothing of mine appears:
```
    records         2  list-items, timeline
    surface         2  layout-utilities, list-items
    preferred:  role record-list      PREFERRED TERM list-items (priority 60) — 7 co-provider(s)
data-grid: FAIL [with-resolves] — every `with` entry needs a `slug` string (s251-D6: the slug is REQUIRED, no ref:null seat), got 'selection-controls (the checkbox — CONSUMED byte-identically, not restated; #261 G3)'
data-grid: FAIL [with-resolves] — ... got 'filter-toolbar-bar'
data-grid: FAIL [with-resolves] — ... got 'pagination'
data-grid: FAIL [with-resolves] — ... got 'search-field'
data-grid: FAIL [with-resolves] — ... got 'tags'
data-grid: FAIL [with-resolves] — ... got 'skeleton-loader'
RESULT: FAIL (6)
```
`python3 knowledge/_roles_drift.py` — 108/108, 0 silent, 0 fields outside the registry; `when` metas 38 → 39:
```
ROLES DRIFT — measured at 04c51c6 2026-09-15 · corpus 137 metas · 12 roles
  memberships  roles.json 108 · metas agree 108 · metas silent 0 (of which 0 carry a roles.json `when`)
  contradictions 0 · dangling slugs 0 · meta→role not in json 0 · unknown role 0 · not-a-provider carrying provides 0
  roles at ZERO in the metas: none
  `when`: roles.json 81/108 · metas 39/137 · metas whose gate uses a field OUTSIDE when-fields.json: 0
```
`python3 knowledge/_validate_kg.py`:
```
_validate_kg.py: OK — every ref parses+resolves, every null carries a note, every meta has provenance, edges match schema, gen_kg_edges.py is idempotent-clean, and the s135-D4 resolutions input was consumed.
```
`python3 knowledge/_validate_compose.py` (0.27s):
```
RESULT: PASS ✅
```
`git diff --stat -- knowledge/`:
```
 knowledge/components/account-card.meta.json |  1 +
 knowledge/components/list-items.meta.json   | 43 +++++++++++++++++++++++------
 2 files changed, 36 insertions(+), 8 deletions(-)
```
Baseline before the lane was identical on every gate — `FAIL (6)`, 108/108, KG `OK`, compose `PASS` — so nothing here is new red.

## 6. Marked as guesses
`priority: 60` (the band is prior art; the number is mine) · `$level` as the key name and `"typeset"` as its third value · the `bordered-per-record` value word in `surface in (…)` (right-hand value vocabularies are explicitly NOT ruled and the resolver never parses them) · the beats/yields sentence's claims against `table`/`data-grid`, which restate their `roles.json` `when` strings rather than any ruling.
