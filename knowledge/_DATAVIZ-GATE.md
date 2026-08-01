# DataViz gate — report

Charts = semantic SVG + tokens + CSS motion + real-table spine. Blocking + advisory per dossier §06.
Gridline contrast is advisory (decorative, WCAG 1.4.11-exempt); series-fill + axis/label contrast is blocking.

## ✓ _proforma/DataViz-interactive.html — PASS
- ⚠ scatter — DV-D02-A: data-dv-type="scatter" is a cartesian plot, so DV-D02 covers it — its plot <svg class="dv-svg"> must also carry dv-fit (0 of 1 do). Responsive = compress width, never scale proportionally. WAIVED: ds-020 — scatter is the only cartesian member still on the pre-DV-D07 axis/grid idiom, FENCED by Dave's ruling (#27): adopting fit moves every gridline, so it ships with a paired before/after control or not at all. Scatter also lacks the data-pl/data-fx geometry hooks fit() reads (measured #28: bar 167 data-fx, scatter 0), so this is not a one-class fix. CLEARS WHEN: ds-020 is enacted with its control — then delete this waiver and the check goes blocking on scatter. ★ PART-DISCHARGED #69 (2026-08-01): the ds-020 axis/grid COLOUR migration is ENACTED with its paired pre/post control (both modes, diffed as colours — knowledge/_DS-IMPROVEMENTS.md ds-020). The waiver STAYS because this clause named TWO conditions under one label: the check it demotes reads the data-fx fit hooks, and scatter carries 6 vs bar's 175 (re-measured #69) — deleting now would go blocking-red on work never scoped into ds-020. REMAINING clears-when: scatter adopts the dv-fit geometry hooks. ⚠ #71: THE SNIPPET HALF IS NOW DONE — Chart-scatter.reference.html carries dv-fit on both plot svgs + 57 data-fx / 27 data-x0, render-proven at 1180/600. The waiver STILL STANDS because the clears-when is surface-blind and a SECOND surface was never in scope: _proforma/DataViz-interactive.html's scatter is '0 of 1' on dv-fit (measured #71 by discharging the waiver and reading which file went blocking-red — the snippet passed, the proforma did not). Same shape as #69's own lesson, one layer out: a clears-when that names a CONDITION but not a SCOPE reads as met the moment any one surface meets it. REMAINING clears-when, now scoped: the proforma scatter adopts the hooks too.
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
- ⚠ scatter — dv-016 [gridline]: var(--data-grid)=#E1E1E1 vs surface #FFFFFF = 1.31:1 (<3:1) in light mode.
- ⚠ scatter — dv-016 [gridline]: var(--data-grid)=#E1E1E1 vs surface #FFFFFF = 1.31:1 (<3:1) in light mode.
- ⚠ scatter — dv-016 [gridline]: var(--data-grid)=#E1E1E1 vs surface #FFFFFF = 1.31:1 (<3:1) in light mode.
- ⚠ scatter — dv-016 [gridline]: var(--data-grid)=#E1E1E1 vs surface #FFFFFF = 1.31:1 (<3:1) in light mode.
- ⚠ scatter — dv-016 [gridline]: var(--data-grid)=#E1E1E1 vs surface #FFFFFF = 1.31:1 (<3:1) in light mode.
- ⚠ scatter — dv-016 [gridline]: var(--data-grid)=#E1E1E1 vs surface #FFFFFF = 1.31:1 (<3:1) in light mode.
- ⚠ scatter — dv-016 [gridline]: var(--data-grid)=#E1E1E1 vs surface #FFFFFF = 1.31:1 (<3:1) in light mode.
- ⚠ scatter — dv-016 [gridline]: var(--data-grid)=#E1E1E1 vs surface #FFFFFF = 1.31:1 (<3:1) in light mode.
- ⚠ scatter — dv-016 [gridline]: var(--data-grid)=#484848 vs surface #1A1A1A = 1.90:1 (<3:1) in dark mode.
- ⚠ scatter — dv-016 [gridline]: var(--data-grid)=#484848 vs surface #1A1A1A = 1.90:1 (<3:1) in dark mode.
- ⚠ scatter — dv-016 [gridline]: var(--data-grid)=#484848 vs surface #1A1A1A = 1.90:1 (<3:1) in dark mode.
- ⚠ scatter — dv-016 [gridline]: var(--data-grid)=#484848 vs surface #1A1A1A = 1.90:1 (<3:1) in dark mode.
- ⚠ scatter — dv-016 [gridline]: var(--data-grid)=#484848 vs surface #1A1A1A = 1.90:1 (<3:1) in dark mode.
- ⚠ scatter — dv-016 [gridline]: var(--data-grid)=#484848 vs surface #1A1A1A = 1.90:1 (<3:1) in dark mode.
- ⚠ scatter — dv-016 [gridline]: var(--data-grid)=#484848 vs surface #1A1A1A = 1.90:1 (<3:1) in dark mode.
- ⚠ scatter — dv-016 [gridline]: var(--data-grid)=#484848 vs surface #1A1A1A = 1.90:1 (<3:1) in dark mode.
- ⚠ scatter — dv-016 [gridline]: var(--data-grid)=#E1E1E1 vs surface #FFFFFF = 1.31:1 (<3:1) in light mode.
- ⚠ scatter — dv-016 [gridline]: var(--data-grid)=#E1E1E1 vs surface #FFFFFF = 1.31:1 (<3:1) in light mode.
- ⚠ scatter — dv-016 [gridline]: var(--data-grid)=#E1E1E1 vs surface #FFFFFF = 1.31:1 (<3:1) in light mode.
- ⚠ scatter — dv-016 [gridline]: var(--data-grid)=#E1E1E1 vs surface #FFFFFF = 1.31:1 (<3:1) in light mode.
- ⚠ scatter — dv-016 [gridline]: var(--data-grid)=#E1E1E1 vs surface #FFFFFF = 1.31:1 (<3:1) in light mode.
- ⚠ scatter — dv-016 [gridline]: var(--data-grid)=#E1E1E1 vs surface #FFFFFF = 1.31:1 (<3:1) in light mode.
- ⚠ scatter — dv-016 [gridline]: var(--data-grid)=#E1E1E1 vs surface #FFFFFF = 1.31:1 (<3:1) in light mode.
- ⚠ scatter — dv-016 [gridline]: var(--data-grid)=#E1E1E1 vs surface #FFFFFF = 1.31:1 (<3:1) in light mode.
- ⚠ scatter — dv-016 [gridline]: var(--data-grid)=#484848 vs surface #1A1A1A = 1.90:1 (<3:1) in dark mode.
- ⚠ scatter — dv-016 [gridline]: var(--data-grid)=#484848 vs surface #1A1A1A = 1.90:1 (<3:1) in dark mode.
- ⚠ scatter — dv-016 [gridline]: var(--data-grid)=#484848 vs surface #1A1A1A = 1.90:1 (<3:1) in dark mode.
- ⚠ scatter — dv-016 [gridline]: var(--data-grid)=#484848 vs surface #1A1A1A = 1.90:1 (<3:1) in dark mode.
- ⚠ scatter — dv-016 [gridline]: var(--data-grid)=#484848 vs surface #1A1A1A = 1.90:1 (<3:1) in dark mode.
- ⚠ scatter — dv-016 [gridline]: var(--data-grid)=#484848 vs surface #1A1A1A = 1.90:1 (<3:1) in dark mode.
- ⚠ scatter — dv-016 [gridline]: var(--data-grid)=#484848 vs surface #1A1A1A = 1.90:1 (<3:1) in dark mode.
- ⚠ scatter — dv-016 [gridline]: var(--data-grid)=#484848 vs surface #1A1A1A = 1.90:1 (<3:1) in dark mode.

## ✓ snippets/Chart-sparkline.reference.html — PASS

---
Method: `_proforma/_DATAVIZ-METHOD.md`. Dossier: `reviews/DATAVIZ-METHOD-2026-07-16.html` §06.
Advisory checks promote to blocking after a bite-test (ADR-0005 §5): `python3 knowledge/_validate_dataviz.py --selftest`.
