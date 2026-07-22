# Worker C receipt — Data-grid lane (Phase-2 wave 2, itinerary row 51)

*2026-07-22 evening BST (date from `date`). Brief: `notes/_briefs/2026-07-22-phase2-worker-C-brief.md`.
Role from Dave's opener line ("you are WORKER C"). Fences held: NEW files only · NO git · NO writes to
handoff files or shared registries (`component-types.json`, `gen_showroom.py`, `_type-bindings.json`,
`MIGRATED_SNIPPETS`, `CATEGORIES` all untouched). **NO COMMITS MADE.***

## Landed (complete lane — no cut)

**`knowledge/snippets/Data-grid.reference.html`** + **`knowledge/components/data-grid.meta.json`** —
ONE snippet holds the family (core grid + toolbar + edit-in-place landed together; the brief's
permission to split wasn't needed). Basename verified unused in snippets/ AND _proforma/.

Full spread as briefed: sorted asc/desc (aria-sort cycle, library sort/chevron glyphs) · filtered
(search field → Enter commits dismissible chips, AND-combined; live results count) · row-selected
(tint + 4px inset start bar + checked box — never colour alone) · header-indeterminate (page-scope
select-all) · edit-cell (Reference column; Enter/F2/dblclick; field-active chrome; commit/cancel
announced) · empty (filtered-to-zero + clear-filters recovery) · loading (aria-busy + Skeleton bones
by reference) · pagination footer (range read-out · rows-per-page · aria-current pages). APG grid
keyboard model: ONE tab stop, roving cell focus, widgets tabindex=-1, grid nav suspended in editor.
`showroom/data-grid.html` generated (sanctioned `gen_showroom.py` run — the build's own instruction;
generator NOT edited).

## Gate state at hand-off (attribution exact)

- **My file: green on every gate that bites it.** snippet gate 59/0 · radius **0 strict / 0 advisory**
  (role tokens from birth) · partials `--check` OK, ratchet 0 strict, **census 32→32 — zero
  press-shaped locals added** · grid gate PASS · a11y 0 fails, 0 warnings on Data-grid · icon gate
  clean (all 8 glyphs byte-matched library; 2 bespoke control glyphs annotated, Selection-controls
  precedent) · type-blast PASS after the .dgseg fix (below) · integrity: Data grid meta valid.
- **Build globally RED on OTHER lanes' in-flight files (not mine to fix, worker fence):**
  ① integrity error = **Bar chart** meta `provenance/source: 'proforma-promotion'` not in enum
  (worker D's promotion lane — enum extension or re-source is a conductor/D call; D's 'data/grid'
  token warning is also theirs, chart gridlines not my component). ② showroom `--check` stale =
  **time-picker.html** (worker A landed Time-picker mid-run — next regen picks it up).
  The tree was visibly BUSY: snippet count moved 54→58→59 across my three build runs.

## $members proposal (exact JSON — conductor registers, then injects + completes contracts)

```json
"Data-grid": { "selector": ":is(.dg .sort, .dg .fchip .x, .dg .clearbtn, .dg .pbtn)" }
```

Wave-1 conventions followed: `:is()` list (multi-control member) · empty AUTO-PARTIAL marker pair
byte-matches Empty-state's · `--spring`/`--press` byte-equal to Button's · `transform var(--spring)`
in all four pressables' transitions (contract lands clean on registration — the wave-1 lesson) ·
manifest binds `--press-travel`/`--press-darken` → `component-type/button-family/*`, declared `2`/`0.94`
both theme blocks. **`--phys-size`: root 120** (sort/clear ≈ text-button geometry) · **LOCAL 44 on
`.pbtn`** (icon-button geometry) · **LOCAL 24 on `.fchip .x`** (the Toast/Banner dismiss size).
**Sort headers carry `.full`** — cell-bound; hover grow would overflow the cell (Button's own
full-width guard, same reasoning).

## Judgment calls (with retrievals)

1. **Grid ≠ Table, by inscription:** Table meta rubric decision A (2026-06-22) verbatim — *"if a
   sortable table is ever needed it should be a distinct component."* This lane IS that component;
   Table consumed (row chrome table/header/background · table/border, 10×12 cell padding, headers
   500/data 400), never edited.
2. **Type via composites only, incl. the header-weight dodge:** headers ride `.t-cm-button` (16/500 —
   Table's header weight through a composite, sidestepping wave-1 A-Q1's `.t-cm-label` 400 question);
   data `.t-cm-label`; amounts `.t-cm-figure-5` (tabular); captions `.t-cm-caption`; editor/search
   `.t-cm-input`; current page = swaps `.t-cm-label`→`.t-cm-button` (500 by composite, not raw weight).
3. **Responsive = horizontal scroll + sticky header, NOT Table's card-collapse** — deliberate
   divergence, documented in snippet + meta: card-collapse orphans the columnheader/aria-sort AT
   relationships; peer shape Carbon/Ant/AG-Grid; reflow duty stays with the passive Table.
4. **Form controls get NO press physics** (checkboxes, search clear ×, page-size select) — the
   Account-selector precedent ("form control, not button-family") + Search-field's clear-as-furniture.
   Chip dismiss × IS a member (Toast/Banner dismiss idiom).
5. **Tags' tactile × motion deliberately NOT copied** (hover scale 1.4 = press-shaped, pre-B-D7 local
   physics — census material in Tags). My chips take partial-injected physics only. Same for
   Pagination's local `scale(.94)` press: colour press (pressed fill + reverse text) consumed, scale
   left to the partial.
6. **Selected-row tint binds `form/background/hover`, row hover binds `tertiary/background/hover`** —
   same hex in Mono, DISTINCT semantic sources so themes can split them (noted in manifest findings;
   selection reads structurally via bar + checkbox regardless, 1.4.1).
7. **Bespoke control glyphs:** tick + indeterminate dash copied exactly from Selection-controls
   (`data-bespoke` annotated, its gate convention); Figma-export clipPath wrappers dropped from
   filter/edit-derived symbols — paths byte-match the library files the manifest declares.
8. **tov-038 self-catch:** visible hint copy de-moused ("double-click" removed; F2/Enter documented;
   dblclick handler retained for mouse users).

## Field-chrome copies (accretion evidence — ADR-0013 ruling 3, feeds Dave's field-family question)

- **COPY 1, marked `FIELD-CHROME-COPY` in-file:** `.dgsearch` = Search-field boxed recipe (border
  `form/border/default` · hover `form/background/hover` · focus-within `form/border/active` + inset
  0 -4px stroke + page fill) — the full block.
- **COPY 2, partial:** `td.edit.editing` = the field ACTIVE stroke only (inset 0 -4px `form/border/active`
  + page fill).
- Cross-lane tally the conductor can now cite: **≥9 files** carry this chrome (Input-fields, Dropdown,
  Search-field, A's four, Account-selector, + Data-grid ×2 sites).

## Blast-radius catch worth inscribing

First build tripped the type-blast gate: my demo state switcher reused Table's `.seg` classname —
**ESCAPED** its acknowledged 5-file radius. Fixed by namespacing (`.dgseg`, the Account-selector
`.acchip` precedent), NOT `--update` (shared registry = conductor's). **Flag: Table's `.seg` demo
idiom is a live reuse trap** — any new file copying that harness chrome must namespace or the gate
fires (it did its job first try).

## Proposals for the conductor's serials

- **MIGRATED_SNIPPETS:** + `Data-grid` (radius strict from birth — already passes 0/0).
- **CATEGORIES:** "Data and content" bucket alongside Table (or B's proposed Data-display split if
  Dave rules for the re-bucket — either works, file sits with Table).
- **Registry:** the `$members` JSON above; injection + contract completion on registration.
- **Icon gaps: NONE** — sort, chevrons ×4, search, close, edit all library-matched. (View-column
  glyph noted as EXISTING for the deferred column show/hide feature.)

## Open questions (receipt, not improvised)

1. **Skeleton duplication:** by-reference consumption still forced a minimal `.bone` re-statement
   (self-contained snippets can't import). Skeleton-family = registry-group candidate alongside
   field-family; my copy is marked in-file.
2. **Error/validation state deliberately absent** — edit commits are free text pending the
   `input-error` null-slot ruling (wave-1 A-Q2). One slot declaration + a `rag/error` stroke variant
   retrofits it.
3. **Density toggle + column show/hide deferred** (View-options territory / view-column glyph ready).
4. **Bar-chart meta enum** ('proforma-promotion') — if the conductor extends the schema enum instead
   of re-sourcing, my meta is untouched either way.
5. Server-side/virtualised rows are out of reference-snippet scope (noted in meta).

## Sandbox lesson (receipted for the runbook if it recurs)

This sandbox does NOT persist `/tmp` or background processes BETWEEN bash calls (each call is a fresh
context) — build logs must be written inside the mount (`outputs/`) and polled in the same call.
Render-verify remains OWED project-wide (headless-shell refusal unchanged); verification here stood
on the gates + mechanical checks (markers byte-match, JS node-parses, showroom page generated).

**Files created (mine, complete list):** `knowledge/snippets/Data-grid.reference.html` ·
`knowledge/components/data-grid.meta.json` · `showroom/data-grid.html` + regenerated `showroom/index.html`
(generator output) · this receipt. **NO commits; nothing pushed.**
