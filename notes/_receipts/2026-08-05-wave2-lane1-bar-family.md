# Wave-2 lane ① receipt — Chart-butterfly-h · Chart-butterfly-v · Chart-histogram

*Worker: Sonnet. Brief: `notes/_briefs/2026-08-05-chart-wave2-lane1-bar-family.md`. DIVVY:
`notes/_briefs/2026-08-05-chart-wave2-DIVVY.md`. No git touched by this worker.*

## Files created

- `knowledge/snippets/Chart-butterfly-h.reference.html` — mirrored horizontal bars, two series
  (2025 / 2026), legend-as-filter markup baked, table + tip + toolbar baked.
- `knowledge/snippets/Chart-butterfly-v.reference.html` — same contract rotated: mirrored columns
  above/below one shared baseline (Actual / Forecast by quarter). x-geometry reused verbatim from
  Chart-bar's column layout (same data-fx/data-fw fractions, same data-pl/data-pr).
- `knowledge/snippets/Chart-histogram.reference.html` — single-series contiguous bins (8 bins,
  transaction-value distribution), static non-interactive legend key.
- `knowledge/components/Chart-butterfly-h.meta.json`
- `knowledge/components/Chart-butterfly-v.meta.json`
- `knowledge/components/Chart-histogram.meta.json`
- This receipt.

All three meta files parse as valid JSON (checked). All three snippet files close their `</html>`
tag and carry their AUTO-BEHAVIOUR marker pairs (checked by grep — see "Owed to the conductor"
below for what's inside them).

## What landed

- **Mark contract** — copied from `Chart-bar.reference.html` verbatim: `rect.dv-series`
  presentation-attribute fill as the single source of series colour (ds-010 lesson, no CSS `fill`
  rule reintroduced); popover value == table value (one source, `data-tip`); bars carry
  `tabindex="0"` + `aria-label`; CSS-only entry motion (DEF-003); type composites only (DV-D08
  ladder: `.t-cm-chart-label`/`-value` 12/500, table `.t-cm-legal`).
- **Toolbar** — copied verbatim from Chart-bar: Copy CSV (icon⇄tick) + table-view popover dropdown,
  shared `--control-h` height.
- **Legend, butterfly pair** — DV-D11 chrome (checkbox swatch + isolate label, hollow off-state,
  additive focus set, sr-only live region) copied verbatim from Chart-bar's CSS. Two rows each
  (butterfly-h: 2025/2026 on data/series/1 and data/series/3; butterfly-v: Actual/Forecast on the
  same pair). On-chart letter keys (bar's `.dv-barkey`) **deliberately omitted** — direction
  (left/right, up/down) plus colour already disambiguate the two series without a third channel;
  this is a receipted delta from the bar contract, not an oversight, called out in both meta files'
  `accessibility.nonText`.
- **Legend, histogram** — single-series rule per the brief: a NEW, minimal, non-interactive
  `.dv-leg-static` pattern (swatch + "Transactions" label, `aria-hidden="true"`), ~10 lines of CSS.
  Not present anywhere in Chart-bar (its single-series column/bar variants carry no legend at all).
  Flagged in the histogram meta's `tokenValidation.$note` for the conductor to consider folding
  into a shared canon rule if other single-series charts want the same pattern.
- **DV-D09 citation** — butterfly-h's RIGHT series (positive-reading direction) binds
  `data/series/3`, citing DV-D09's h-bar default; the LEFT series binds `data/series/1`, the
  categorical default. Histogram binds `data/series/1` (column default) since it has no
  orientation choice.
- **Geometry** — hand-derived plotting math for all three (see each snippet's header comment for
  the full derivation): butterfly-h's mirrored-gutter baselines, butterfly-v's shared
  upper-middle baseline with SAME up/down scale (0.9 px/unit both directions, so the halves stay
  comparable), histogram's zero-gap bin width (`rect width == slot width`, no bar-style inset).
  Butterfly-v's x-positions are REUSED VERBATIM from Chart-bar's column layout (identical
  data-fx/data-fw fractions) — only the y math is new.
- **Type composites only** — no raw font shorthand anywhere in any of the three files (checked by
  read-back; all text uses `.t-cm-chart-label` / `.t-cm-chart-value` / `.t-cm-section-label` /
  `.t-cm-legal` classes from `type.css`).

## Fences honoured

- **ds-020 (DIVVY-instructed)** — copied the mark contract + toolbar, **not** the axis/grid CSS.
  Concretely: `.dv-grid`, `text.dv-axis`, `text.dv-label` (the `var(--axis-alpha)`-driven opacity
  ladder) are **absent** from all three files' `<style>` blocks — I did not port that CSS bundle.
  Axis/baseline lines carry colour via inline `stroke="var(--baseline)"` only (the same
  belt-and-braces presentation attribute Chart-bar itself uses, just without the CSS layer on top).
  No gridlines are drawn in any of the three charts. Declared in each file's header comment and
  each meta's `tokens.axis` field — inherited knowingly, not filled, not silently absorbed.
- **Worker fence** — did not touch `component-types.json`, `dv-behaviour.js`,
  `MIGRATED_SNIPPETS`/`CATEGORIES` (`_validate_radius.py`/`gen_showroom.py`), spine docs, or git.
  AUTO-BEHAVIOUR markers are EMPTY in all three files (dv-behaviour in all three; dv-legend in the
  two butterfly files — histogram has no dv-legend marker pair at all, since its legend is static
  and needs no behaviour source).

## Owed to the conductor (serial-file needs, named)

1. **`component-types.json` "$members"** — three new entries needed in the `dataviz` group:
   `Chart-butterfly-h`, `Chart-butterfly-v`, `Chart-histogram`, each pointing at its
   `snippets/*.reference.html`. Hook contract: butterfly-h and butterfly-v both need
   **dv-behaviour** (fit/tip/CSV/table-toggle) AND **dv-legend** (filter/isolate) injected between
   their two marker pairs. Histogram needs **dv-behaviour only** — no dv-legend marker pair exists
   in that file (static legend has nothing to drive).
2. **`_validate_radius.py` `MIGRATED_SNIPPETS`** — add all three filenames once registered.
3. **`gen_showroom.py` `CATEGORIES`** — bar-family category grouping; confirm butterfly-h/-v and
   histogram slot alongside Chart-bar/Chart-scatter or get their own subheading (Dave's call, not
   mine to pre-empt).
4. **Gate run** — DataViz gate 0 blocking, census/radius/coverage green, type-blast — none of this
   has been run against these three files; `tokenValidation.result` in all three meta files reads
   **UNPROVEN**, not PASS. Series fills reuse Chart-bar's already-validated tokens (`data/series/1`,
   `data/series/3`) so a pass is expected but not measured.
5. **Render-verify** — OWED, per the brief's 07-24 sandbox-kill precedent (compensating evidence:
   static geometry review only — coordinates hand-checked to fit within the 580×260 viewBox and
   plot margins for all three files, but no browser render, no ≥2-widths/dark/HC/filtered/JS-off
   pass was run this session).
6. **`.dv-leg-static` folding decision** — flagged in the histogram meta as a candidate for a
   shared canon rule if other single-series charts want the same static-key pattern; conductor's
   call, not enacted here.

## Deviations from the brief (declared, not silent)

- The brief's checklist item "controls NEVER dim-only (hollow-swatch off-state recipe, follow
  exactly)" applies to the butterfly pair's interactive legends (followed exactly, copied
  verbatim). It does not apply to the histogram's static key, which has no interactive state to
  dim — noted so the checklist item isn't read as unmet there.
- Each snippet is a SINGLE demonstration figure (one dataset per chart type), not a multi-variant
  gallery page the way `Chart-bar.reference.html` shows column/bar/status/grouped/stacked all in
  one file. The brief's scope line describes each chart type in the singular ("paired horizontal
  bars, mirrored axis, two series" / "same contract rotated" / "single-series column, contiguous
  bins") and DV-D09's citation only needed one h-bar demonstration, so I read this as in-scope; if
  the conductor wants additional baked variants (e.g. a status-ramp butterfly, or multiple bin
  counts for the histogram), that's a receipted gap, not something I inferred was wanted.
