# Wave-2 lane ② — Chart-boxplot · Chart-bullet · Chart-candlestick (statistical/gauge)

*Cut 2026-08-05 #94 by the conductor. Worker model: **Sonnet** (conductor replays your receipt).
**Read first, in order:** this brief → `snippets/Chart-bar.reference.html` +
`snippets/Chart-line.reference.html` (pattern + exemplar canon) →
`notes/_receipts/2026-07-24-wave-lane1-bar-scatter.md` → `_DATAVIZ-DECISIONS.md`
DV-D07/08/09 · ADR-0015.*

## Scope

1. **Chart-boxplot** (`snippets/Chart-boxplot.reference.html` + meta) — median/IQR/whiskers/
   outliers; outlier markers reuse the scatter marker family (r5.5/11/±6.5 exemplar canon);
   table view mirrors five-number summary per category.
2. **Chart-bullet** — measure bar + comparative marker + qualitative ranges; ranges are
   NEUTRAL surface tints (grey-tint check: surface any new grey to Dave via receipt, never
   auto-pick); measure = series-1, marker = ink.
3. **Chart-candlestick** — OHLC; **up/down = `data/delta/gain`·`data/delta/loss` tokens, RULED**
   (§C·1(a) names the binding — cite it in meta); wicks = ink at reduced weight; table mirrors
   OHLC columns.

## Fences

**Yours:** the three new `snippets/*.reference.html` · their `components/*.meta.json` · your
receipt `notes/_receipts/2026-08-05-wave2-lane2-statistical.md`. **NOT yours:**
`component-types.json` (receipt the `$members`/hooks) · `dv-behaviour.js` (missing hook ⇒
RECEIPT) · `MIGRATED_SNIPPETS`/`CATEGORIES` · spine docs · existing snippets · git.
**ds-020:** copy mark contract + toolbar, NOT the axis/grid CSS; receipt the inherited gap.

## Checklist

Same as lane ①: type composites only (gate-enforced) · DataViz gate 0 blocking · parity
scripts · render-verify ≥2 widths + dark + HC + filtered + JS-off (or declare OWED with
compensating evidence, 07-24 precedent) · census/radius/coverage green · controls never
dim-only (hollow-swatch recipe exactly). Receipt: landed / OWED / serial-file needs, named.
