# Wave lane ① — Chart-bar + Chart-scatter (chart-revisit fan-out)

*Cut 2026-07-24 by the conductor. Model/effort per the ratified divvy: **Fable · medium** (Dave sets
the knob at window-open). Role from Dave's opener. **Read first, in order:** `GOOD-MORNING.md` →
`snippets/Chart-line.reference.html` (THE pattern — port, don't reinvent) → the exemplar receipt
`notes/_receipts/2026-07-23-chart-line-exemplar-worker.md` (the SIX refinements + state model +
a11y constraint are CANON) → `_DATAVIZ-DECISIONS.md` DV-D07/08/09 · ADR-0015.*

## Scope

1. **Chart-bar → full Layer-2** (popover · fit · table-view popover · optional title · H-stack
   head). Single-series figures keep static legend keys.
2. **★ D-Q3 ENACT: promote grouped + stacked column** from `_proforma/DataViz-interactive.html`
   into Chart-bar as new figures — with legend-as-filter/isolate/highlight (multi-series), shaped
   +lettered swatches, AA hollow off-state, on-chart keys bound `t-cm-chart-key` (12/700, DV-D08).
   Grid gate will bite kit geometry on re-entry (stepper precedent) — correct, receipt it.
3. **★ DV-D09 ENACT:** h-bar default fill → `data/series/3` (column stays series-1). One-line CSS
   + meta note; cite DV-D09.
4. **Menu item 3/4 (ruled in): sort toggle** — original/asc/desc as BAKED VARIANT GROUPS
   (`data-dv-view` idiom from the exemplar — geometry generation-time, behaviour toggles only);
   table mirrors the active order.
5. **Chart-scatter → full Layer-2** + enlarged marker family (r5.5 / 11 / ±6.5 — exemplar canon,
   supersedes kit sizes) + line-end-letter equivalent = segment letters stay; add the letter-zone
   padding if clipped.
6. **★ B4 ENACT (your ONE permitted proforma edit):** wire `data-fx` fit into the proforma's
   scatter section so the gold-standard file meets its own bar. Nothing else in that file moves.
7. **Menu item 8 (brush/range-select): SPEC ONLY** — keyboard design proposal in your receipt
   (the ruling requires it designed before build). Do not build.

## Fences (three lanes live — narrow again)

**Yours:** `snippets/Chart-bar.reference.html` · `snippets/Chart-scatter.reference.html` · their
`components/*.meta.json` · the proforma scatter-section fit wiring (item 6 ONLY) · your receipt
`notes/_receipts/2026-07-24-wave-lane1-bar-scatter.md`.
**NOT yours (conductor serials):** `component-types.json` (hand `$members`/hook JSON via receipt) ·
`dv-behaviour.js` (if a hook is missing, RECEIPT the need — do not edit the source) · `_build_all` ·
`MIGRATED_SNIPPETS`/`CATEGORIES` · spine docs · git (NO commits).

## Bar checklist (the exemplar's, applied)

Build serially as you land; DataViz gate 0 blocking (gridline advisories are permanent-by-design);
parity scripts (chart↔table↔tips↔aria); render-verify ≥2 widths + dark + HC + filtered + JS-off
per `_RUNBOOK-render-verify.md`; census/radius/coverage green; a11y: controls NEVER dim-only
(hollow-swatch off-state recipe), data-layer dimming OK — the constraint is OPEN pending Dave's
adviser, so follow the exemplar recipe exactly rather than inventing.
