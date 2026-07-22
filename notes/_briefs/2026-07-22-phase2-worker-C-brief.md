# Phase-2 Worker C brief — DATA-GRID lane (itinerary row 51, lane-sized on its own)

*Cut by the wave-1 conductor session, 2026-07-22 (date from `date`), per the wave-2 divvy
(`GOOD-MORNING.md` §C·1) + `_BUILDOUT-STRATEGY-2026-07-21.md`. You are a WORKER per
`knowledge/_RUNBOOK-parallel-conductor.md`: create only NEW files, NO git, NO writes to
`GOOD-MORNING.md`/`_LIVE-STATE.md`/`_FUTURE-STATE.md`/shared registries. Receipt at the end.
Model: Fable. Role comes from Dave's opener line only — this file is not a seat assignment.*

## The lane

**Data grid (sort / filter / select / edit)** — itinerary row 51, P1: "data-dense tables; drives
most fintech screens" (peer shapes: Carbon / Ant / AG-Grid). ONE lane, one component family —
big enough that it was deliberately held out of wave 1. Budget the whole window to it; if it
splits naturally (core grid → toolbar → edit-in-place), land them as ORDERED separate snippets
with the cut line in your receipt.

## Survey debt (run BEFORE building — survey-before-build, and this lane is ALL prior art)

- `python3 knowledge/_consult.py "data grid table sort filter selection"` first.
- **`snippets/Table.reference.html` is the gated BASE — mine it, do NOT edit it (fence).** The grid
  is Table + interaction; every visual decision Table already made (row chrome, density, type
  composites, radius roles) is SETTLED — consume, don't re-decide.
- Interaction mechanics to mine, never modify: `snippets/Dropdown` (filter menus + its 6 known
  manifest-dodging locals — do NOT copy those, they're queued as F5) · `snippets/Selection-controls`
  (row checkboxes, indeterminate header state) · `snippets/Search-field` (filter input) ·
  `snippets/Pagination` (footer paging) · `snippets/Icon-button` (toolbar affordances) ·
  `snippets/Tags` (applied-filter chips — note the tag-atom radius reconcile is queued, bind
  current canon) · Worker B's `snippets/Stat-card`/`Account-selector` for the newest receipt style.
- Sort-direction/chevron glyphs: real assets only (`assets/icons/` — wave-1 A verified the
  chevron run is library-matched). Any missing glyph = icon-gap proposal, not an invention.

## Per-component loop (definition of done — identical to wave 1)

1. CONSULT + survey (above). Extend, never restart.
2. Build NEW `knowledge/snippets/Data-grid.reference.html` (+ meta) — basename unused in BOTH
   snippets/ and _proforma/. Requirements: theme-blind semantic bindings via `#token-manifest`
   (never `color/mono/*` direct, never hexes) · radius = role tokens · type = `.t-cm-*` composites
   only · 4px grid · sentence case · weights 100/300/400/500/700 (no 600) · white type red-only
   (type26-013) · real icons only · AA + state contrast (active > hover, never colour-alone) ·
   full variant/state spread (sorted asc/desc · filtered · row-selected · header-indeterminate ·
   edit-cell · empty · loading-skeleton CONSUMING Worker B's Skeleton pattern by REFERENCE not
   copy — receipt any duplication you're forced into).
3. **Partials protocol (ADR-0013):** every pressable (sort headers, toolbar buttons, pagination
   controls) = NO local press physics; empty
   `/* ===== AUTO-PARTIAL press-physics START (button-family) ===== */` + `END` pair on your
   control selector, `--phys-size` declared (**multi-control member? propose an `:is()` selector
   list — the wave-1 convention, see the registry $description; mixed sizes = LOCAL `--phys-size`
   override on the smaller control**), manifest binds for `--press-travel`/`--press-darken`,
   `--spring`/`--press` byte-equal to Button's + `transform var(--spring)` in each control's
   transition (**wave-1 lesson: contracts fire on REGISTRATION — land these NOW so the conductor's
   pass is clean**). Exact `$members` JSON in your receipt.
4. **Field-family is NOT yet a registry group** (proposed to Dave, undecided): filter inputs
   consume Input-fields' field chrome BY COPY for now — name the copied block in your receipt
   (it feeds the accretion case, ruling 3).
5. `python3 knowledge/_build_all.py` green before each next snippet. Category proposal (likely
   "Data and content") in the receipt — don't edit `gen_showroom.py`.
6. Blocked/ambiguous → receipt, don't improvise canon. Live Dave rulings → receipt VERBATIM.

## Do NOT

Edit `component-types.json` · `_validate_radius.py` · `gen_showroom.py` · any existing snippet
(Table, Dropdown, Selection-controls, Search-field, Pagination, Tags incl.) · tokens (propose via
receipt) · mint a loader atom (§C·4b, was §C·3b) · touch git or handoff files. Don't drift into
the button-states finesse pass.

## Receipt (mandatory, last act)

`notes/_receipts/<date from date>-phase2-worker-C-datagrid.md` — landed + cut line · judgment
calls with retrievals · `$members` JSON · MIGRATED_SNIPPETS basenames · category proposal ·
icon gaps · field-chrome copies (accretion evidence) · open questions · NO commits made.
