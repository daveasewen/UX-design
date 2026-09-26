# Cold run cand-r3 — Spider v1.0.14 candidate

Lane: on-canon (the pack's skills). Pack zip sha256 verified `2e827237…135d`. Frozen build: `out/` (entry `out/index.html`, references `../pack/` in place — the pack is not in the frozen folder).

## Pack files read, in order
`CLAUDE.md`, `AGENTS.md`, `FIRST-SESSION.md`, `README.md`; skills `grill-me` (+ its questions), `generate-from-canon`, `check-with-gates`, `check-against-design-system`, `usability-review`, `draft-a-new-pattern` (head). Then, as those sent me: `knowledge/_compose_slice.py` (help, one seed + five typed chart-intent seeds), `canon/dv-render.js` and partial headers, `_render/_bento_edit_rails.json`, metas (kpi-tile, stat-card, summary, data-grid, app-shell-top/side-nav, drawer, filter-toolbar-bar…), snippets (all 14 Chart-*, Template-dashboard-bento for grammar only, App-shell-side-nav, Kpi-tile, Summary, Status-indicator, Data-grid, Table, Pagination, Drawer, Modals, Toast, Tabs, Segmented-control, Alert, Filter-toolbar-bar, Input-fields, Textarea, Selection-controls, Dropdown, Button), targeted greps of `canon.css`, the icons manifest, and the docstrings of the receipt, screen, compose, composition and icon gates.

## What I built
One file, `index.html`, with ten hash-routed views (`#/overview`, `#/accounts`, `#/liquidity`, `#/payments`, `#/fx`, `#/risk`, `#/trade`, `#/reports`, `#/messages`, `#/settings`); records open as `#/<view>/<id>`. Theme Common (`data-apollo-theme="common"`), light and dark.
- Frame: App-shell-side-nav (its `when`: more than 7 destinations), masterbrand logos, skip link, footer.
- Every view is a Template-dashboard-bento wall (bento grammar only; the rails' bentoBg "grey" dial via the scope's `--wall-ground`; title area and page unchanged).
- Overview answers the three questions. Q1: four Kpi-tiles (cash, available liquidity, funding headroom, liquidity runway) with inline sparks, each linking to its view. Q2: Chart-bar stacked-column of exposure by region × currency; selecting a bar drills to Risk and limits filtered to that region, positions tab. Q3: two Summary cards (pending approvals, material exceptions) whose rows open the record.
- Components: Filter-toolbar-bar (search, entity, region, date, theme seg, export, chips, clear all), Kpi-tile, Summary, status chips, Data-grid markup (9 grids: sort, page, page size), Tabs, Drawer, Modals, Toast, Input-fields, Textarea, Dropdown, Selection-controls switch, Segmented-control, Button.
- Charts, all drawn by `dvRender` from one `DATA` model: column (with sort), bar, grouped-column, stacked-column, multiline, stacked-area, combo (target toggle), donut, pie, histogram, scatter, boxplot, bullet, butterfly-h, butterfly-v, candlestick, standalone sparkline (report drawer), inline KPI sparks — all 14 chart components.
- Workflows (simulated, persisted in localStorage, URL carries view/record/filters/tab): approve and reject payments (note required at £5m+, reason always), acknowledge exceptions with an audit note and owner, drawdown request (checked against internal limit), FX quote booking, trade amendment (raises a service request), new service request (validated, refuses card-number-like text), message replies, report runs and CSV exports, theme, settings, reset.

## Questions I would have asked (defaults taken; see `out/briefs/`)
Dashboard bento? — yes (stated). Ten destinations: top bar or side column? — side column (graph `when`). One page or ten files? — one page, ten views. Reporting date? — 25 Sep 2026, 30 daily points. Approval threshold for a note? — £5m. What makes an exception material? — ≥100% utilisation, or ≥90% at BBB+ or below.

## Proof
- Baseline, before any UI: `python3 ci-template/run-gates.py` → 35 pass · 6 FAIL · 0 could-not-ask (composition 2, grid 1, polarities 2, receipt 2 — needs a path, roles_resolve 1, token_forks 1). Kept: `out/proof/baseline-runner.txt`.
- After build: same command → identical verdict set, 35 · 6 · 0 (`after-runner.txt`). All six reds are inherited.
- Provenance: `gen_provenance_receipt.py --mint out/index.html` → 35 regions (17 chart figure templates, modal overlay, toast region, 16 AUTO-BEHAVIOUR blocks), `--check` exit 0. `_validate_receipt.py` → FAIL:BEHAVIOUR-ADDRESS-DISAGREES on the 17 chart regions, 18 ✅. Inherited: the pack's own `--compose` of one Chart-bar figure fails the same way (`inherited-receipt-check.txt`).
- Screen: `_validate_screen.py out/index.html` → receipt ❌ (inherited, above), compose ✅, composition UNPROVEN (C9 cannot read linked canon.css), icon-source ✅, a11y ✅.
- Driven (Playwright, seat render env, 1440×900 unless noted): filters 17/17, decisions and grids 19/19, workflows 19/19, navigation/theme/charts 22/22, geometry 32/32 at 1440 and 32/32 at 1920; zero console or page errors in every section; all ten views render every chart with marks (`smoke-*.json`). Geometry: no ragged rows, no tile overflow, no horizontal scroll, toolbar width equals section width, gutters equal (40 main, 4 sub, ground inset 40 all sides).
- Visual review: unavailable (vision disabled). No screenshot used as evidence.

## Gaps
1. App-shell-side-nav ships as a 640px-high framed specimen (`.sh{height:640px}`); used at its own size, so work scrolls inside the frame. No full-viewport shell exists for more than seven destinations.
2. Common theme: canon's bento role vars define main spacing for `legacy` but not `common`, so gutters resolve to mono's 40px, not Common's 24px. Not worked around.
3. Receipt mint and gate disagree on the chart script address (inherited).
4. Nested scopes: the bento template's bar-family chart CSS overrides donut, pie and standalone-sparkline sizing; donut/pie sit in a 580×260 canvas unfitted; the standalone sparkline is only in the report drawer.
5. Donut intro sweep does not run (figures are cloned after its parse-time init).
6. Measured slack: FX rates card 69px, requests donut 57px at 1920; KPI tile 157px vs 155px in the showroom.
7. At 1440 the wall is under 1100px, so it re-flows to canon's three-column band (every group full width).
8. Grids: sort, page, page size and search only — no column filters, resize, inline edit or grid keyboard model.
9. Not run to completion: `run-gates.py --browser` and `_validate_screen.py --render` (seat call limit, exit 124). Phone and tablet not tested. JS off shows empty views.
10. No production banking capability; all data, FX rates and outcomes are simulated; exports are CSV and browser print only.

Context at the build→proof seam: about 200K tokens (estimated).
