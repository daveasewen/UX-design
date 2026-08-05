# Wave-2 lane ③ — Chart-pie · Chart-stacked-area (donut + line families)

*Cut 2026-08-05 #94 by the conductor. Worker model: **Sonnet** (conductor replays your receipt).
**Read first, in order:** this brief → `snippets/Chart-donut.reference.html` (pie's pattern) +
`snippets/Chart-line.reference.html` (stacked-area's pattern + exemplar canon) →
`notes/_receipts/2026-07-24-wave-lane1-bar-scatter.md` → `_DATAVIZ-DECISIONS.md`
DV-D07/08/09 · ADR-0015 · dv-pie-009 · D-Q2.*

⛔ **The §C·1(a) queue text gave this lane a third item — "promote grouped/stacked bars
(D-Q3)". STRUCK by the conductor's survey #94: D-Q3 LANDED at the 07-24 wave
(`Chart-bar.reference.html:39`; receipt items 4–5). Do not rebuild it. Two items only.*

## Scope

1. **Chart-pie** (`snippets/Chart-pie.reference.html` + meta) — port the donut contract minus
   the centre figure (DV-D13's donut-centre wiring is donut-only; do NOT copy it across);
   **dv-pie-009: ≤6 segments** enforced in the reference data + noted in meta; **D-Q2
   labelling** rules the label placement — cite both. Legend-as-filter from the donut pattern.
2. **Chart-stacked-area** — line-family geometry with stacked fills; series fills at the
   ramp's stacked opacities (bind existing `data/series/*` tokens, receipt any tint you need
   but do NOT mint one — token minting is a serial/conductor act); in-fill letter keys follow
   the stacked-column recipe (`data/text/on-series`); table mirrors per-series + total.

## Fences

**Yours:** the two new `snippets/*.reference.html` · their `components/*.meta.json` · your
receipt `notes/_receipts/2026-08-05-wave2-lane3-pie-area.md`. **NOT yours:**
`component-types.json` (receipt the `$members`/hooks) · `dv-behaviour.js` (missing hook ⇒
RECEIPT) · `MIGRATED_SNIPPETS`/`CATEGORIES` · spine docs · existing snippets (donut/line stay
untouched) · git. **ds-020:** copy mark contract + toolbar, NOT the axis/grid CSS; receipt it.

## Checklist

Same as lanes ①/②: type composites only (gate-enforced) · DataViz gate 0 blocking · parity
scripts · render-verify ≥2 widths + dark + HC + filtered + JS-off (or declare OWED with
compensating evidence, 07-24 precedent) · census/radius/coverage green · controls never
dim-only (hollow-swatch recipe exactly). Receipt: landed / OWED / serial-file needs, named.
