# s135-D2 enactment — Lane A — KG verdicts apply

Ruling: `knowledge/_rulings.json` → `s135-D2`. Verdicts:
`reviews/KG-REVIEW-VERDICTS-2026-08-08-s135-v1.json`.

## TOP-LINE FINDING — freshness gate blocks 3 of 4 sections

Before touching the corpus I empirically tested (on a throwaway edit, reverted
immediately, not left in the tree) what happens when a NEARMISS-merge-style
edit, a PROSE-promote-style edit, or a GOVERNED-attach-style edit is made
directly to a component meta's `edges` field. All three trip the SAME arm of
`knowledge/_validate_kg.py`: check (e), the freshness/idempotency check.

Root cause: `knowledge/gen_kg_edges.py` treats `edges` as a fully-disposable
DERIVED VIEW. On every run it calls `remove_existing_edges_field()` (strips
the *entire* `edges` object, all keys) then `build_edges_for_meta()`
(rebuilds `edges` from scratch, purely from `relationships` /
`subComponents` / `$consumes` / `$reuses` / `$partials` / `$family` — never
from the previous `edges` value). It has zero preservation path for:
- a manually-repointed ref (NEARMISS merge: context:X → component:Y) — the
  generator's own name-matcher is case/whitespace-only (`norm()`), it has no
  plural-stripping or fuzzy logic, so it will always regenerate the OLD
  (un-merged) ref from the untouched `relationships.livesInside` prose.
- a manually-resolved ref on `mustNotNeighbour`/`triggeredBy`/`hasPart`/
  `partial`/`family` (PROSE promote) — the generator hard-codes `ref: null`
  for every entry in these five edge types, unconditionally, by design
  (its own docstring: "ref:null + $note ... not invented as refs").
- `governedBy` at all (GOVERNED attach) — the generator's own docstring says
  governedBy is "reserved for the Dave's-eye batch ... not yet populated";
  `build_edges_for_meta()` never emits this key, so any live copy of it is
  wiped, not merged, on the next freshness re-run.

Empirical proof (3 throwaway edits, each reverted before the next):
1. Added `edges.governedBy: [{"ref":"ruling:ds-032"}]` to `button.meta.json`
   → freshness FAIL, `button.meta.json DRIFTED from a clean regeneration`.
2. Repointed one `usedInContext` ref from `context:card` to `component:cards`
   in `button.meta.json` → same freshness FAIL.
3. Set one `mustNotNeighbour` ref from `null` to `component:toast` in
   `alert.meta.json` (exactly the PROSE-promote shape) → same freshness FAIL.

All three are the *same* mechanism, not three different bugs, and it is not
attributable to a mistake in my specific edit — the baseline corpus is green,
and every edit of this shape reproduces the failure. This is systemic across
ALL 5 nearmiss MERGE rows, ALL 52 PROSE PROMOTE rows, and ALL 25 GOVERNED
ATTACH rows: none of them can be written into the live `edges` field and
leave `_validate_kg.py` green, because `gen_kg_edges.py`'s regeneration
contract has no mechanism to preserve any of the three edit shapes this
ruling calls for.

Fixing this at the root would mean teaching `gen_kg_edges.py` a new,
un-designed preservation/promotion mechanism for `governedBy` and for
sticky-resolved refs on the five prose edge types — exactly the "Dave's-eye
batch, not yet populated" mechanism its own schema comment defers to a
future pass. That is a generator/architecture decision, not a row-for-row
verdict application, so per the DO-NOT-RULE list ("do not decide anything
Dave-shaped") I did not build it. Per the hard rule ("never weaken the
validator... if red, revert the offending one and log it") I reverted every
test edit and did **not** apply NEARMISS, PROSE, or GOVERNED to the live
corpus. TOKENS is unaffected (it never touches `edges`) and is applied below.

**This needs a second pass, scoped by Dave**: either (a) rule a
`gen_kg_edges.py` amendment that makes `governedBy` and promoted-prose refs
"sticky" across regeneration, or (b) accept a scoped freshness-check carve-out
for these edge types, before this ruling's NEARMISS/PROSE/GOVERNED verdicts
can land without weakening `_validate_kg.py`.

## Counts

| Section  | Rows | Applied | Skipped (by verdict) | Exception (blocked/ambiguous) |
|----------|------|---------|-----------------------|--------------------------------|
| NEARMISS | 35   | 0       | 30 (LEAVE)            | 5 (MERGE — freshness-blocked) |
| PROSE    | 98   | 0       | 46 (STAY NULL)        | 52 (PROMOTE — freshness-blocked) |
| GOVERNED | 47   | 0       | 22 (SKIP)             | 25 (ATTACH — freshness-blocked) |
| TOKENS   | 24   | 9       | 0                     | 15 (no unambiguous value/prose boundary — see below) |

Nothing was invented; nothing ruled-LEAVE/STAY-NULL/SKIP was touched.

## TOKENS — method

`tokens` is never touched by `gen_kg_edges.py` / `_validate_kg.py`, so these
edits carry no freshness risk. For each row I grepped the `raw` preview
(the verdicts JSON truncates long values at ~200 chars — I located the row
via the truncated prefix, then read the FULL untruncated string from the
source file for the actual edit, so nothing is lost to the preview's cutoff).

Split rule applied (mechanical, stated once so it's auditable, not a
per-row judgment call): if the full string contains one clean value-then-
citation/rationale boundary (a top-level " — " em-dash, or — where there is
no dash — exactly one well-formed trailing parenthetical after a value that
itself names a resolvable token/class/measurement), split there: `value` =
the value-description (kept exactly as written, including its own internal
parens where those are part of the value, e.g. "(body up)"), `$note` = the
rest, verbatim. Nothing deleted — every character survives in one field or
the other. Where a row is a nested object (button's `primary`/`secondary`),
I split the specific leaf that actually carries the fusion, not the outer
key, and say so below.

Rows where NO leaf/string in the file has this shape, or where two
candidate boundaries exist that disagree (e.g. a semicolon suggesting one
split point and a dash suggesting another), or where the row is a
"RECEIPTED GAP" declaration (the whole point of which is that no value
exists — forcing one into `value` would misrepresent a declared absence as
an assignment) went to exceptions rather than a guess.

### Applied (9)

| # | File | Key (path) | value | $note |
|---|------|-----------|-------|-------|
| 1 | Chart-boxplot.meta.json | tokens.series | `data/series/1` | `box fill (the chart's one measure channel)` |
| 2 | Chart-candlestick.meta.json | tokens.delta | `data/delta/gain (body up) / data/delta/loss (body down)` | `ds-027 RULED binding (#100), consumed VERBATIM from canon.css (--data-delta-gain #16864E/#1AA05C, --data-delta-loss #B92F1E/#CC4333 light/dark), not re-derived. Owned by the RAG/delta colour workstream.` |
| 3 | Chart-candlestick.meta.json | tokens.wick | `ink (text/default) at .6 alpha, 1px` | `'wicks = ink at reduced weight'` |
| 4 | button.meta.json | tokens.type-style | `font-5/medium` | `(16px medium)` |
| 5 | button.meta.json | tokens.secondary.label (nested leaf — the outer `secondary` key is an object; only `.label` carried the fusion) | `text/on-inverse (NOT text/reverse)` | `secondary inverts to a light fill in dark, so flat-white text/reverse would be white-on-white; text/on-inverse is #FFF light / #333 dark (decision: Dave 2026-06-19)` |
| 6 | form-layout.meta.json | tokens.field | `form/background\|border sets` | `(Input-fields lock-step)` |
| 7 | form-layout.meta.json | tokens.success | `rag/success` | `(valid-state roundel)` |
| 8 | chart-donut.meta.json | tokens.separation | `stroke = background/default (page) at 2px on every segment` | `(dv-004 — gapless surfaces need surface-coloured separation)` |
| 9 | chart-donut.meta.json | tokens.leaders | `border/subtle hairlines` | `(decorative)` |

Each edit was targeted string surgery (exact old→new substring replace),
verified by `json.loads()` after write and by re-checking the touched
sub-object's shape; the file's schema validity was also spot-checked against
`meta.schema.json` via `jsonschema.Draft7Validator` (0 errors on all 5 files)
even though `_validate_kg.py` doesn't itself check `tokens`.

### Exceptions — TOKENS (15)

| Row idx | File / target | raw (truncated) | Why exception |
|---|---|---|---|
| 0 | Chart-boxplot.meta.json → tokens.font-family | "type composites via markup class — axis ticks/labels .t-cm-chart-label/-value · table .t-cm-legal" | Both sides of the dash are value-description (which classes apply where); no actual rationale/citation clause exists to move to $note. |
| 2 | Chart-boxplot.meta.json → tokens.marks | "whiskers/caps = ink 1px stroke · median = ink 2px stroke (...) · outliers = data/series/1 fill, page-colour 1.5px stroke" | No dash; 3-clause `=`-joined list, no single value/prose boundary. |
| 3 | Chart-boxplot.meta.json → tokens.axis | "⛔ ds-020 RECEIPTED GAP — this snippet inherits the PRE-DV-D07 ink-at-alpha idiom..." | This is a declared GAP (explicitly: no value exists). Putting the flag string in `value` would misrepresent an absence as an assignment. |
| 4 | (unresolved) key row after boxplot cluster | "value (prose-contaminated)" | Literal text not found anywhere in the corpus (verified by full-string grep across all component metas). Reads like a placeholder/marker from the review tool, not a real grep target. Cannot locate a source file — logged rather than guessed. |
| 5 | Chart-candlestick.meta.json → tokens.font-family | same text as row 0 | Same reasoning as row 0. |
| 8 | Chart-candlestick.meta.json → tokens.axis | "⛔ ds-020 RECEIPTED GAP — pre-DV-D07 ink-at-alpha idiom..." | Same reasoning as row 3 (declared GAP). |
| 9 | (unresolved) key row after candlestick cluster | "value (prose-contaminated)" | Same as row 4. |
| 11 | button.meta.json → tokens.font-family | "typography/font-family/default" | Already a bare value; no dash, no trailing parenthetical, no prose to move — nothing to split. |
| 12 | button.meta.json → tokens.primary | Python-repr preview of the whole nested object | Checked every leaf (label/icon/background-*/success/"depricate (on-light)") — none contains a dash or a trailing-parenthetical fusion. The object is already fully bare. |
| 14 | (unresolved) key row after button cluster | "value (prose-contaminated)" | Same as row 4. |
| 16 | form-layout.meta.json → tokens.error | "rag/error + rag/error-tint (R-D20); message TEXT stays text/default — colour is never the only channel" | Two candidate boundaries disagree: the semicolon reads as the natural clause break, but the em-dash sits later inside the second clause. Splitting at either produces a `value` that still contains an independent second assertion — ambiguous. |
| 18 | form-layout.meta.json → tokens.buttons | "button/primary/* + button/quaternary/* ladder" | No dash, no parenthetical anywhere in the string — nothing to split. |
| 19 | (unresolved) key row after form-layout cluster | "value (prose-contaminated)" | Same as row 4. |
| 20 | chart-donut.meta.json → tokens.font-family | "type composites via markup class — DV-D08 ladder: ..." | Same reasoning as row 0 (both sides are value-description, no rationale clause). |
| 21 | chart-donut.meta.json → tokens.series | "data/series/1–5 (mode-stable candidate C); measured 3.52–5.26:1 light / 3.31–4.95:1 dark vs the page (dv-016 clean)" | Compound: internal parenthetical + a semicolon-joined independent measurement clause before the final citation parenthetical — no single unambiguous value/prose boundary. |

The 4 "key" rows (idx 4, 9, 14, 19) are identical placeholder text
(`"value (prose-contaminated)"`) appearing once per file cluster in the
verdicts JSON. A corpus-wide exact-string grep found zero matches anywhere —
this looks like a review-tool marker/artefact rather than a literal
extractable value, but I did not guess a target for it.

## NEARMISS — exceptions (5, all blocked by the freshness finding above)

| context node | merges into | occurrences in corpus |
|---|---|---|
| context:card | component:cards | 11 files carry a `usedInContext` ref to `context:card` |
| context:header | component:headers | 1 file |
| context:link | component:links | 1 file |
| context:navigation | component:navigations | 1 file |
| context:tab | component:tabs (or tab-bar) | 1 file |

None applied. `_nodes-context.json` registry untouched (removal would follow
the ref repoint, which didn't happen).

## PROSE — exceptions (52, all blocked by the freshness finding above)

Full list (file | edge-group | note prefix | target):

- Chart-butterfly-h.meta.json | mustNotNeighbour | "A Stat-card making the identical claim..." → stat-card
- Chart-butterfly-v.meta.json | mustNotNeighbour | "A Stat-card making the identical claim..." → stat-card
- Chart-histogram.meta.json | mustNotNeighbour | "A Stat-card making the identical claim..." → stat-card
- alert.meta.json | mustNotNeighbour | "Toast (same message twice)" → toast
- alert.meta.json | mustNotNeighbour | "Banner carrying the identical message" → banner
- banner.meta.json | mustNotNeighbour | "A second banner..." → banner
- banner.meta.json | mustNotNeighbour | "Alert/Toast carrying the identical message" → toast
- chart-bar.meta.json | mustNotNeighbour | "A Stat-card making the identical claim..." → stat-card
- drawer.meta.json | mustNotNeighbour | "A second drawer or open modal..." → drawer
- empty-state.meta.json | mustNotNeighbour | "Skeleton loader..." → skeleton loader
- icon-button.meta.json | mustNotNeighbour | "Icon button (primary) x2..." → icon button
- loading-indicator.meta.json | mustNotNeighbour | "another Loading indicator..." → loading indicator
- modal-lightbox.meta.json | mustNotNeighbour | "An open Modals dialog or Drawer..." → drawer
- popover.meta.json | mustNotNeighbour | "Tooltip on the same trigger" → tooltip
- popover.meta.json | mustNotNeighbour | "A second open popover..." → popover
- skeleton-loader.meta.json | mustNotNeighbour | "Loading-indicator for the same region..." → loading-indicator
- tab-bar.meta.json | mustNotNeighbour | "Tabs (in-page)..." → tab bar
- toast.meta.json | mustNotNeighbour | "Alert carrying the identical message" → alert
- toast.meta.json | mustNotNeighbour | "A second toast for the same event" → toast
- icon-button.meta.json | mustNotNeighbour (2nd row) | "Icon button (primary) x2..." → icon button
- drawer.meta.json | triggeredBy | "table/list row activation" → table
- drawer.meta.json | triggeredBy | "filter buttons" → button
- popover.meta.json | triggeredBy | "labelled trigger button click" → button
- data-grid.meta.json | hasPart | "sort-header: Full-cell button..." → button
- data-grid.meta.json | hasPart | "selection-checkbox: 22×22 box..." → selection-controls
- data-grid.meta.json | hasPart | "filter-field: Search-field boxed chrome..." → search-field
- data-grid.meta.json | hasPart | "applied-chip: Dismissible Tags recipe..." → button
- data-grid.meta.json | hasPart | "pagination: Prev/next chevrons..." → pagination
- hero.meta.json | hasPart | "assets: [...]" → hero
- pagination.meta.json | hasPart | "page-size-dropdown..." → dropdown
- pagination.meta.json | hasPart | "go-button..." → button
- pagination.meta.json | hasPart | "arrow-button..." → button
- table.meta.json | hasPart | "header: Column/row header cell..." → table
- table.meta.json | hasPart | "sub-header: Secondary header..." → table
- tabs.meta.json | hasPart | "tab-track: Bottom rule..." → tabs
- tabs.meta.json | hasPart | "overflow-dropdown..." → dropdown
- tabs.meta.json | hasPart | "tab-dropdown-items..." → dropdown
- date-picker.meta.json | partial | "4 × .dp-nav..." → button
- date-range-picker.meta.json | partial | "4 × .dr-nav..." → button
- file-upload.meta.json | partial | "TWO button-family candidates..." → button
- stepper.meta.json | partial | ".st-nav button (Back/Next)..." → progress-tracker
- time-picker.meta.json | partial | "NONE — zero button-family candidates..." → input-fields
- headers.meta.json | family | "Covers the Headers family..." → headers
- input-fields.meta.json | family | "Covers the Input fields section..." → input fields
- links.meta.json | family | "Covers the Links canvas..." → links
- list-items.meta.json | family | "Covers the 'List items' canvas..." → list items
- modals.meta.json | family | "Covers the 'Modals' canvas..." → modals
- navigations.meta.json | family | "Covers the 'Navigations' canvas..." → navigations
- notifications.meta.json | family | "Covers the 'Notifications' canvas..." → notifications
- pagination.meta.json | family | "Covers the 'Pagination (browser)' canvas..." → pagination
- segmented-control.meta.json | family | "The single-select sliding-indicator switcher..." → view options
- selection-controls.meta.json | family | "Covers the 'Selection controls' canvas..." → selection controls

34 unique files touched by these 52 rows. Target-node-existence verification
(required by the ruling before promoting) was not separately run since none
of these were applied; this should be done as part of whatever second pass
lands them.

## GOVERNED — exceptions (25, all blocked by the freshness finding above)

20 unique components would receive a `governedBy` edge:
Chart-candlestick, action-bar, badge, banner, button, chart-bar, chart-combo,
chart-donut, chart-line, chart-pie, chart-sparkline, chart-stacked-area,
drawer, empty-state, form-layout, input-fields, modals, selection-controls,
stepper, tabs.

Rulings attributed (ruling id → components): ds-026 (button,
chart-stacked-area); ds-027 (Chart-candlestick); ds-031 (chart-donut,
chart-pie); ds-032 (modals, form-layout, button, stepper, drawer,
empty-state, action-bar); s114-D3 (input-fields, form-layout); s116-D2
(chart-donut, chart-combo, chart-bar, chart-sparkline, chart-line); s123-D4
(tabs, badge); s125-D1 (banner); s130-D4 (banner); s130-D5
(selection-controls); s131-D1 (banner).

None applied — same freshness-gate conflict.

## Validator output (last lines)

```
== _validate_kg.py — KG edge parse-gate (s131-D2 / s133-D1) ==
metas checked: 77
ref:null + $note (declared, awaiting Dave's-eye migration): 98

_validate_kg.py: OK — every ref parses+resolves, every null carries a note,
every meta has provenance, edges match schema, gen_kg_edges.py is
idempotent-clean.
```
Exit green. `ref:null + $note` count (98) is unchanged from baseline — expected,
since no `edges` field was touched this pass.

## Files touched (5, all TOKENS-only edits to the `tokens` field; no file's
`edges`, `relationships`, or any other field was changed)

- `knowledge/components/Chart-boxplot.meta.json`
- `knowledge/components/Chart-candlestick.meta.json`
- `knowledge/components/button.meta.json`
- `knowledge/components/form-layout.meta.json`
- `knowledge/components/chart-donut.meta.json`

No other files in the repo were modified. `knowledge/_rulings.json`,
`GOOD-MORNING.md`, `_LIVE-STATE.md`, `_CHAIN.md`, `_memento-index.json`,
`gen_kg_edges.py`, and `_validate_kg.py` were read/tested against but never
written to (the 3 throwaway test edits used to prove the freshness
conflict were reverted before this brief was written; `git diff` on the repo
at brief-time shows only the 5 files above).
