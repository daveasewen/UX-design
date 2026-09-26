# RUN-REPORT — cand-r1 (Spider v1.0.14 candidate, zip sha256 2e827237…135d verified)

**Lane:** on-canon. **Entry:** `out/index.html` — one page, ten views addressed as `index.html?view=overview|accounts|liquidity|payments|fx|risk|trade|reports|messages|settings`. It references the pack in place (`../pack/knowledge/…`), so it renders only with `pack/` beside `out/`.

## Pack files read, in order
`CLAUDE.md` → `FIRST-SESSION.md` → `README.md` → `skills/generate-from-canon`, `check-with-gates`, `grill-me` (first part), `check-against-design-system`, `usability-review` → `knowledge/_RUNBOOK-compose-from-canon.md` (first half) → `_render/_bento_edit_rails.json` → `components/template-dashboard-bento.meta.json` ($bentoGrammar) → `canon/dv-render.js` header, `dv-behaviour.js`, `dv-legend.js` (parts) → the snippets and metas of every part used → `gen_provenance_receipt.py`, `_validate_receipt.py`, `_validate_screen.py`, `_validate_composition.py` (help and relevant functions) → `canon.css` (targeted greps).

## What I built
- **Shell:** App-shell-side-nav (app bar with masterbrand, collapsible nav, phone sheet, crumbs, legal footer); Page-header-lockup; one shared Filter-toolbar-bar (search, entity/region/currency facets, 7/30/90-day range, table/cards, density, CSV/Excel/print export).
- **Grammar:** `cn-template-dashboard-bento` › `.tpl-page` › `.c-bento.tpl-wall` › `tpl-group-lead|evidence|context` › tiles at `data-c` 1/3/6; ground `--surface-subtle`.
- **Components (43 verbatim spliced regions, receipted):** Kpi-tile, 16 chart figures, Cards, Table, List-items, Pagination, Dropdown, Segmented-control, Selection-controls, Drawer, Modals, Textarea, Toast, Alert, Empty-state, Summary, Timeline, Status-indicator (chip + filled cell), Limits-meter, Data-grid (live), Filter-toolbar-bar (live).
- **Charts (all 17 registered types via `dvRender` from `CEO_DATA`):** column, bar, grouped, stacked, line, multiline, stacked-area, donut, pie, combo, candlestick, bullet, butterfly-h, scatter, histogram, boxplot, sparkline — with legends, tooltips, table spine, CSV copy; re-rendered on every filter. Exposure column and currency donut drill through to Risk positions.
- **Workflows:** approve/reject (audit note mandatory ≥£10m and for rejections), exception acknowledgement (15/10-char note), service requests (validated), message replies, report generation + download, exports. State persists (URL + localStorage).
- Detail: `used-missing.md` (decision table), `#behaviour-manifest` in the page.

## Questions I would have asked → default taken
Recorded in `briefs/2026-09-26-ceo-banking-grill.md`: bento (yes, stated); entities (six placeholder "Aldergrove" entities); approval threshold (£5m routes to CEO, note ≥£10m); "material" (limit >100% plus named items); headroom definition (cash + undrawn committed − £400m buffer − 3-month maturities); three vs four KPIs (four — canon pins the lead row to four); views vs files (views); custom range (not offered).

## Proof
| step | command | result |
|---|---|---|
| Baseline (fresh pack) | `python3 ci-template/run-gates.py` | 35 pass · 6 FAIL · 0 could-not-ask (`proof/baseline-run-gates.txt`) |
| Provenance | `python3 knowledge/gen_provenance_receipt.py --mint ../out/index.html`; `--check` | minted; PASS in sync |
| Receipt gate | `python3 knowledge/_validate_receipt.py ../out/index.html` | **FAIL** — 17 chart regions `BEHAVIOUR-ADDRESS-DISAGREES`; all 26 other regions ✅ (Data-grid and Filter-bar LOADED-EXTENDED, Textarea LOADED) |
| Screen gate | `TMPDIR=$W/tmp python3 knowledge/_validate_screen.py ../out/index.html` | compose ✅ · icon-source ✅ · a11y ✅ · composition UNPROVEN (C9) · receipt ❌ → RESULT FAIL |
| Composition | `python3 knowledge/_validate_composition.py ../out/index.html` | exit 77 UNPROVEN (C9: page declares no column count/bands); C1/C4/C7/C8 0 |
| Pack runner after build | `python3 ci-template/run-gates.py` | 35 pass · 6 FAIL — the same six as baseline: **no new failures** |
| Driven browser (Playwright, seat shell) | `tools/prove_a.py`, `tools/prove_b.py` | 33/33 and 32/32 checks pass, zero console errors / uncaught exceptions |
| DOM geometry + computed spacing | `tools/geometry.py 1440 [dark]`, `1100`, `820` | 1440 light and dark: 0 issues (rows share top/bottom, gutters equal, no overflow, no dead space). 1100/820: KPI labels truncate |
| Size vs reference snippet | `tools/sizes.py` | 19/20 match; KPI spark 44 vs 40 px |

**Inherited vs new.** The six runner failures are inherited (identical before and after). The receipt FAIL is a pack defect my page exposes: the pack's own mint writes `dv-behaviour.js` for a chart region while the chart meta says `dv-render.js`; reproduced on a one-chart page built by the pack's own `--compose` (`_build/repro/`). An icon-source red appeared once as a false positive (the gate's regex read from a `<svg>` in a dv-render.js comment to a `</svg>` in a later script); I moved the engine blocks to the end of the body. That was the only change made to satisfy a gate.

**Visual review: unavailable** (vision disabled). Screenshots in `proof/screens/` are for the record only, not evidence.

## Gaps
1. **Receipt gate red** on all chart regions (pack mint/gate disagreement, above).
2. **C9 span legality unproven** statically; checked only by rendered geometry at 1440/1100/820.
3. **Shell height is the specimen's 640 px** (`.sh{height:640px}`); rule 3a forbids resizing it, so content scrolls inside the frame.
4. **Common gets mono's 40 px outer bento gutter.** canon's bento role vars exist for `legacy` but not `common`.
5. **Dark ground:** `--surface-subtle` equals the tile surface in dark, so the ground goes transparent in dark (a page choice, flagged for the designer).
6. **KPI spark 44 px, not 40:** the dashboard-bento template scope carries its own `.spark-inline` height.
7. KPI inline spark geometry is authored (no engine type for it). App shell mechanics are re-stated in page JS (its script binds by id at parse time).
8. Custom date range not wired (the Date-range-picker hand-off). "Excel" export is an Excel-readable HTML table (.xls). "PDF" export is the browser's print dialog, which was not driven.
9. JS off: only a notice renders (views are cloned from templates).
10. Not run: `run-gates.py --browser` (state-contrast), screen gate `--render`, keyboard-only full pass, screen readers, touch devices. No usability review was written up.
11. Everything is simulated: no live banking, no credentials, illustrative FX (`CEO_DATA.fx`).
