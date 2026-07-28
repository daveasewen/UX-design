# DataViz gate — report

Charts = semantic SVG + tokens + CSS motion + real-table spine. Blocking + advisory per dossier §06.
Gridline contrast is advisory (decorative, WCAG 1.4.11-exempt); series-fill + axis/label contrast is blocking.

## ✓ _proforma/DataViz-interactive.html — PASS
- ⚠ scatter — DV-D02-A: data-dv-type="scatter" is a cartesian plot, so DV-D02 covers it — its plot <svg class="dv-svg"> must also carry dv-fit (0 of 1 do). Responsive = compress width, never scale proportionally. WAIVED: ds-020 — scatter is the only cartesian member still on the pre-DV-D07 axis/grid idiom, FENCED by Dave's ruling (#27): adopting fit moves every gridline, so it ships with a paired before/after control or not at all. Scatter also lacks the data-pl/data-fx geometry hooks fit() reads (measured #28: bar 167 data-fx, scatter 0), so this is not a one-class fix. CLEARS WHEN: ds-020 is enacted with its control — then delete this waiver and the check goes blocking on scatter.
- ⚠ scatter — dv-016 [gridline]: var(--line2)=#EDEDED vs surface #FFFFFF = 1.17:1 (<3:1) in light mode.
- ⚠ scatter — dv-016 [gridline]: var(--line2)=#EDEDED vs surface #FFFFFF = 1.17:1 (<3:1) in light mode.
- ⚠ scatter — dv-016 [gridline]: var(--line2)=#EDEDED vs surface #FFFFFF = 1.17:1 (<3:1) in light mode.
- ⚠ scatter — dv-016 [gridline]: var(--line2)=#EDEDED vs surface #FFFFFF = 1.17:1 (<3:1) in light mode.
- ⚠ scatter — dv-016 [gridline]: var(--line2)=#EDEDED vs surface #FFFFFF = 1.17:1 (<3:1) in light mode.
- ⚠ scatter — dv-016 [gridline]: var(--line2)=#EDEDED vs surface #FFFFFF = 1.17:1 (<3:1) in light mode.
- ⚠ scatter — dv-016 [gridline]: var(--line2)=#EDEDED vs surface #FFFFFF = 1.17:1 (<3:1) in light mode.
- ⚠ scatter — dv-016 [gridline]: var(--line2)=#EDEDED vs surface #FFFFFF = 1.17:1 (<3:1) in light mode.
- ⚠ scatter — dv-016 [gridline]: var(--line2)=#3A3A3A vs surface #1A1A1A = 1.53:1 (<3:1) in dark mode.
- ⚠ scatter — dv-016 [gridline]: var(--line2)=#3A3A3A vs surface #1A1A1A = 1.53:1 (<3:1) in dark mode.
- ⚠ scatter — dv-016 [gridline]: var(--line2)=#3A3A3A vs surface #1A1A1A = 1.53:1 (<3:1) in dark mode.
- ⚠ scatter — dv-016 [gridline]: var(--line2)=#3A3A3A vs surface #1A1A1A = 1.53:1 (<3:1) in dark mode.
- ⚠ scatter — dv-016 [gridline]: var(--line2)=#3A3A3A vs surface #1A1A1A = 1.53:1 (<3:1) in dark mode.
- ⚠ scatter — dv-016 [gridline]: var(--line2)=#3A3A3A vs surface #1A1A1A = 1.53:1 (<3:1) in dark mode.
- ⚠ scatter — dv-016 [gridline]: var(--line2)=#3A3A3A vs surface #1A1A1A = 1.53:1 (<3:1) in dark mode.
- ⚠ scatter — dv-016 [gridline]: var(--line2)=#3A3A3A vs surface #1A1A1A = 1.53:1 (<3:1) in dark mode.

## ✓ snippets/Chart-bar.reference.html — PASS
- ⚠ column — dv-016 [gridline]: var(--data-grid)=#E1E1E1 vs surface #FFFFFF = 1.31:1 (<3:1) in light mode.
- ⚠ column — dv-016 [gridline]: var(--data-grid)=#E1E1E1 vs surface #FFFFFF = 1.31:1 (<3:1) in light mode.
- ⚠ column — dv-016 [gridline]: var(--data-grid)=#E1E1E1 vs surface #FFFFFF = 1.31:1 (<3:1) in light mode.
- ⚠ column — dv-016 [gridline]: var(--data-grid)=#E1E1E1 vs surface #FFFFFF = 1.31:1 (<3:1) in light mode.
- ⚠ column — dv-016 [gridline]: var(--data-grid)=#E1E1E1 vs surface #FFFFFF = 1.31:1 (<3:1) in light mode.
- ⚠ column — dv-016 [gridline]: var(--data-grid)=#484848 vs surface #1A1A1A = 1.90:1 (<3:1) in dark mode.
- ⚠ column — dv-016 [gridline]: var(--data-grid)=#484848 vs surface #1A1A1A = 1.90:1 (<3:1) in dark mode.
- ⚠ column — dv-016 [gridline]: var(--data-grid)=#484848 vs surface #1A1A1A = 1.90:1 (<3:1) in dark mode.
- ⚠ column — dv-016 [gridline]: var(--data-grid)=#484848 vs surface #1A1A1A = 1.90:1 (<3:1) in dark mode.
- ⚠ column — dv-016 [gridline]: var(--data-grid)=#484848 vs surface #1A1A1A = 1.90:1 (<3:1) in dark mode.
- ⚠ bar — dv-016 [gridline]: var(--data-grid)=#E1E1E1 vs surface #FFFFFF = 1.31:1 (<3:1) in light mode.
- ⚠ bar — dv-016 [gridline]: var(--data-grid)=#E1E1E1 vs surface #FFFFFF = 1.31:1 (<3:1) in light mode.
- ⚠ bar — dv-016 [gridline]: var(--data-grid)=#E1E1E1 vs surface #FFFFFF = 1.31:1 (<3:1) in light mode.
- ⚠ bar — dv-016 [gridline]: var(--data-grid)=#E1E1E1 vs surface #FFFFFF = 1.31:1 (<3:1) in light mode.
- ⚠ bar — dv-016 [gridline]: var(--data-grid)=#E1E1E1 vs surface #FFFFFF = 1.31:1 (<3:1) in light mode.
- ⚠ bar — dv-016 [gridline]: var(--data-grid)=#484848 vs surface #1A1A1A = 1.90:1 (<3:1) in dark mode.
- ⚠ bar — dv-016 [gridline]: var(--data-grid)=#484848 vs surface #1A1A1A = 1.90:1 (<3:1) in dark mode.
- ⚠ bar — dv-016 [gridline]: var(--data-grid)=#484848 vs surface #1A1A1A = 1.90:1 (<3:1) in dark mode.
- ⚠ bar — dv-016 [gridline]: var(--data-grid)=#484848 vs surface #1A1A1A = 1.90:1 (<3:1) in dark mode.
- ⚠ bar — dv-016 [gridline]: var(--data-grid)=#484848 vs surface #1A1A1A = 1.90:1 (<3:1) in dark mode.
- ⚠ column — dv-016 [gridline]: var(--data-grid)=#E1E1E1 vs surface #FFFFFF = 1.31:1 (<3:1) in light mode.
- ⚠ column — dv-016 [gridline]: var(--data-grid)=#E1E1E1 vs surface #FFFFFF = 1.31:1 (<3:1) in light mode.
- ⚠ column — dv-016 [gridline]: var(--data-grid)=#E1E1E1 vs surface #FFFFFF = 1.31:1 (<3:1) in light mode.
- ⚠ column — dv-016 [gridline]: var(--data-grid)=#E1E1E1 vs surface #FFFFFF = 1.31:1 (<3:1) in light mode.
- ⚠ column — dv-016 [gridline]: var(--data-grid)=#E1E1E1 vs surface #FFFFFF = 1.31:1 (<3:1) in light mode.
- ⚠ column — dv-016 [gridline]: var(--data-grid)=#484848 vs surface #1A1A1A = 1.90:1 (<3:1) in dark mode.
- ⚠ column — dv-016 [gridline]: var(--data-grid)=#484848 vs surface #1A1A1A = 1.90:1 (<3:1) in dark mode.
- ⚠ column — dv-016 [gridline]: var(--data-grid)=#484848 vs surface #1A1A1A = 1.90:1 (<3:1) in dark mode.
- ⚠ column — dv-016 [gridline]: var(--data-grid)=#484848 vs surface #1A1A1A = 1.90:1 (<3:1) in dark mode.
- ⚠ column — dv-016 [gridline]: var(--data-grid)=#484848 vs surface #1A1A1A = 1.90:1 (<3:1) in dark mode.
- ⚠ grouped-column — dv-016 [gridline]: var(--data-grid)=#E1E1E1 vs surface #FFFFFF = 1.31:1 (<3:1) in light mode.
- ⚠ grouped-column — dv-016 [gridline]: var(--data-grid)=#E1E1E1 vs surface #FFFFFF = 1.31:1 (<3:1) in light mode.
- ⚠ grouped-column — dv-016 [gridline]: var(--data-grid)=#E1E1E1 vs surface #FFFFFF = 1.31:1 (<3:1) in light mode.
- ⚠ grouped-column — dv-016 [gridline]: var(--data-grid)=#E1E1E1 vs surface #FFFFFF = 1.31:1 (<3:1) in light mode.
- ⚠ grouped-column — dv-016 [gridline]: var(--data-grid)=#E1E1E1 vs surface #FFFFFF = 1.31:1 (<3:1) in light mode.
- ⚠ grouped-column — dv-016 [gridline]: var(--data-grid)=#484848 vs surface #1A1A1A = 1.90:1 (<3:1) in dark mode.
- ⚠ grouped-column — dv-016 [gridline]: var(--data-grid)=#484848 vs surface #1A1A1A = 1.90:1 (<3:1) in dark mode.
- ⚠ grouped-column — dv-016 [gridline]: var(--data-grid)=#484848 vs surface #1A1A1A = 1.90:1 (<3:1) in dark mode.
- ⚠ grouped-column — dv-016 [gridline]: var(--data-grid)=#484848 vs surface #1A1A1A = 1.90:1 (<3:1) in dark mode.
- ⚠ grouped-column — dv-016 [gridline]: var(--data-grid)=#484848 vs surface #1A1A1A = 1.90:1 (<3:1) in dark mode.
- ⚠ stacked-column — dv-016 [gridline]: var(--data-grid)=#E1E1E1 vs surface #FFFFFF = 1.31:1 (<3:1) in light mode.
- ⚠ stacked-column — dv-016 [gridline]: var(--data-grid)=#E1E1E1 vs surface #FFFFFF = 1.31:1 (<3:1) in light mode.
- ⚠ stacked-column — dv-016 [gridline]: var(--data-grid)=#E1E1E1 vs surface #FFFFFF = 1.31:1 (<3:1) in light mode.
- ⚠ stacked-column — dv-016 [gridline]: var(--data-grid)=#E1E1E1 vs surface #FFFFFF = 1.31:1 (<3:1) in light mode.
- ⚠ stacked-column — dv-016 [gridline]: var(--data-grid)=#E1E1E1 vs surface #FFFFFF = 1.31:1 (<3:1) in light mode.
- ⚠ stacked-column — dv-016 [gridline]: var(--data-grid)=#484848 vs surface #1A1A1A = 1.90:1 (<3:1) in dark mode.
- ⚠ stacked-column — dv-016 [gridline]: var(--data-grid)=#484848 vs surface #1A1A1A = 1.90:1 (<3:1) in dark mode.
- ⚠ stacked-column — dv-016 [gridline]: var(--data-grid)=#484848 vs surface #1A1A1A = 1.90:1 (<3:1) in dark mode.
- ⚠ stacked-column — dv-016 [gridline]: var(--data-grid)=#484848 vs surface #1A1A1A = 1.90:1 (<3:1) in dark mode.
- ⚠ stacked-column — dv-016 [gridline]: var(--data-grid)=#484848 vs surface #1A1A1A = 1.90:1 (<3:1) in dark mode.

## ✓ snippets/Chart-combo.reference.html — PASS
- ⚠ combo — dv-016 [gridline]: var(--data-grid)=#E1E1E1 vs surface #FFFFFF = 1.31:1 (<3:1) in light mode.
- ⚠ combo — dv-016 [gridline]: var(--data-grid)=#E1E1E1 vs surface #FFFFFF = 1.31:1 (<3:1) in light mode.
- ⚠ combo — dv-016 [gridline]: var(--data-grid)=#E1E1E1 vs surface #FFFFFF = 1.31:1 (<3:1) in light mode.
- ⚠ combo — dv-016 [gridline]: var(--data-grid)=#E1E1E1 vs surface #FFFFFF = 1.31:1 (<3:1) in light mode.
- ⚠ combo — dv-016 [gridline]: var(--data-grid)=#E1E1E1 vs surface #FFFFFF = 1.31:1 (<3:1) in light mode.
- ⚠ combo — dv-016 [gridline]: var(--data-grid)=#484848 vs surface #1A1A1A = 1.90:1 (<3:1) in dark mode.
- ⚠ combo — dv-016 [gridline]: var(--data-grid)=#484848 vs surface #1A1A1A = 1.90:1 (<3:1) in dark mode.
- ⚠ combo — dv-016 [gridline]: var(--data-grid)=#484848 vs surface #1A1A1A = 1.90:1 (<3:1) in dark mode.
- ⚠ combo — dv-016 [gridline]: var(--data-grid)=#484848 vs surface #1A1A1A = 1.90:1 (<3:1) in dark mode.
- ⚠ combo — dv-016 [gridline]: var(--data-grid)=#484848 vs surface #1A1A1A = 1.90:1 (<3:1) in dark mode.

## ✓ snippets/Chart-donut.reference.html — PASS

## ✓ snippets/Chart-line.reference.html — PASS
- ⚠ line — dv-016 [gridline]: var(--data-grid)=#E1E1E1 vs surface #FFFFFF = 1.31:1 (<3:1) in light mode.
- ⚠ line — dv-016 [gridline]: var(--data-grid)=#E1E1E1 vs surface #FFFFFF = 1.31:1 (<3:1) in light mode.
- ⚠ line — dv-016 [gridline]: var(--data-grid)=#E1E1E1 vs surface #FFFFFF = 1.31:1 (<3:1) in light mode.
- ⚠ line — dv-016 [gridline]: var(--data-grid)=#E1E1E1 vs surface #FFFFFF = 1.31:1 (<3:1) in light mode.
- ⚠ line — dv-016 [gridline]: var(--data-grid)=#484848 vs surface #1A1A1A = 1.90:1 (<3:1) in dark mode.
- ⚠ line — dv-016 [gridline]: var(--data-grid)=#484848 vs surface #1A1A1A = 1.90:1 (<3:1) in dark mode.
- ⚠ line — dv-016 [gridline]: var(--data-grid)=#484848 vs surface #1A1A1A = 1.90:1 (<3:1) in dark mode.
- ⚠ line — dv-016 [gridline]: var(--data-grid)=#484848 vs surface #1A1A1A = 1.90:1 (<3:1) in dark mode.
- ⚠ multiline — dv-016 [gridline]: var(--data-grid)=#E1E1E1 vs surface #FFFFFF = 1.31:1 (<3:1) in light mode.
- ⚠ multiline — dv-016 [gridline]: var(--data-grid)=#E1E1E1 vs surface #FFFFFF = 1.31:1 (<3:1) in light mode.
- ⚠ multiline — dv-016 [gridline]: var(--data-grid)=#E1E1E1 vs surface #FFFFFF = 1.31:1 (<3:1) in light mode.
- ⚠ multiline — dv-016 [gridline]: var(--data-grid)=#E1E1E1 vs surface #FFFFFF = 1.31:1 (<3:1) in light mode.
- ⚠ multiline — dv-016 [gridline]: var(--data-grid)=#484848 vs surface #1A1A1A = 1.90:1 (<3:1) in dark mode.
- ⚠ multiline — dv-016 [gridline]: var(--data-grid)=#484848 vs surface #1A1A1A = 1.90:1 (<3:1) in dark mode.
- ⚠ multiline — dv-016 [gridline]: var(--data-grid)=#484848 vs surface #1A1A1A = 1.90:1 (<3:1) in dark mode.
- ⚠ multiline — dv-016 [gridline]: var(--data-grid)=#484848 vs surface #1A1A1A = 1.90:1 (<3:1) in dark mode.

## ✓ snippets/Chart-scatter.reference.html — PASS
- ⚠ scatter — DV-D02-A: data-dv-type="scatter" is a cartesian plot, so DV-D02 covers it — its plot <svg class="dv-svg"> must also carry dv-fit (0 of 1 do). Responsive = compress width, never scale proportionally. WAIVED: ds-020 — scatter is the only cartesian member still on the pre-DV-D07 axis/grid idiom, FENCED by Dave's ruling (#27): adopting fit moves every gridline, so it ships with a paired before/after control or not at all. Scatter also lacks the data-pl/data-fx geometry hooks fit() reads (measured #28: bar 167 data-fx, scatter 0), so this is not a one-class fix. CLEARS WHEN: ds-020 is enacted with its control — then delete this waiver and the check goes blocking on scatter.
- ⚠ scatter — DV-D02-A: data-dv-type="scatter" is a cartesian plot, so DV-D02 covers it — its plot <svg class="dv-svg"> must also carry dv-fit (0 of 1 do). Responsive = compress width, never scale proportionally. WAIVED: ds-020 — scatter is the only cartesian member still on the pre-DV-D07 axis/grid idiom, FENCED by Dave's ruling (#27): adopting fit moves every gridline, so it ships with a paired before/after control or not at all. Scatter also lacks the data-pl/data-fx geometry hooks fit() reads (measured #28: bar 167 data-fx, scatter 0), so this is not a one-class fix. CLEARS WHEN: ds-020 is enacted with its control — then delete this waiver and the check goes blocking on scatter.

## ✓ snippets/Chart-sparkline.reference.html — PASS

---
Method: `_proforma/_DATAVIZ-METHOD.md`. Dossier: `reviews/DATAVIZ-METHOD-2026-07-16.html` §06.
Advisory checks promote to blocking after a bite-test (ADR-0005 §5): `python3 knowledge/_validate_dataviz.py --selftest`.
