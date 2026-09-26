# Run report — v1013-r3 (Spider v1.0.13, cold)

Lane declared: on-canon, through the pack's skills. Pack sha256 `5d4df132…b282c6` verified before unzip.

## Pack files read, in order
CLAUDE.md, AGENTS.md, FIRST-SESSION.md, README.md · skills/generate-from-canon, check-with-gates, grill-me (part), check-against-design-system · knowledge/_RUNBOOK-compose-from-canon.md · Template-dashboard-bento snippet (header, markup, CSS) · _bento_edit_rails.json (bentoBg, defaults) · showroom/index.json · snippets: App-shell-side-nav, Data-grid, Filter-toolbar-bar, Drawer, Modals, Toast, Input-fields, Textarea, Dropdown, Segmented-control, Tabs, Status-indicator, Button, Alert, Timeline, Stat-card, Summary, Selection-controls, Links, all 14 Chart-* (figure/canvas markup, spec calls) · canon/dv-render.js + type partials (registry, spec contract), dv-legend.js, dv-behaviour.js (tip, fit) · component metas (behaviour) · canon.css (scoped rules, tokens) · gate sources where a gate refused (receipt, screen, composition, compose).

## What I built
Ten linked pages (separate files) in `out/`: `index.html` (overview), accounts, liquidity, payments, fx, risk, trade, reports, messages, settings. Shared `data.js` (one seeded DATA model: 9 entities, 22 accounts, 320 transactions, 12 facilities, 72 payments, 64 positions, 13 limits, 10 exceptions, 44 trade instruments, 46 FX deals, 7 pairs × 30 days, 18 reports, 12 messages, 26 requests; illustrative FX fixed as at 25 Sep 2026) and `app.js` (wiring).
Composition: Template-dashboard-bento page grammar (masthead, header lock-up, status strip, bento wall, footer) on every page; Kpi-tile, Stat-card, Summary, Status-indicator, Filter-toolbar-bar (search, region, entity, date, export, chips, clear all), Data-grid (sort, search, paging, rows per page, empty state), Drawer, Modals, Toast, Input-fields, Textarea, Dropdown, Segmented-control (theme, view), Selection-controls, Timeline (audit trails), Alert. All 18 engine chart types, drawn by `dvRender` from DATA: column, bar, grouped-column, stacked-column, line, multiline, stacked-area, donut, pie, combo, bullet, butterfly-h, butterfly-v, boxplot, candlestick, histogram, scatter, sparkline — with legends (multi-series, donut, pie), tooltips, table view, CSV copy. Every filter re-drives KPIs, charts and grids. Workflows: approve/reject (note rules, material ≥ £5m confirm modal), risk acknowledgement (note ≥ 15 chars + review tick, audit trail), drawdown request, FX quote and book, trade amendment, service requests, message replies, report runs, exports (CSV/JSON files). Filters, theme, grid sort/page, and every workflow outcome persist (localStorage; filters, search and open record in the URL).

## Questions I would have asked — and the default taken
All six grill questions were answered by the prompt; recorded in `out/briefs/`. "Dashboard bento — is that right?" — answered yes by the prompt. Would have asked: (1) ten destinations do not fit the template's four-link masthead below ~1150px — took short nav labels, wide desktop only; (2) the rails' grey ground token resolves equal to the tile surface in dark — took the template's own `--wall-ground`; (3) whether single-series charts need a legend — followed the pack's snippets (none).

## Proof (commands and results)
- Baseline before building: `python3 ci-template/run-gates.py` → 34 pass · 7 FAIL · 0 could-not-ask (composition, grid, polarities, receipt, roles_resolve, token_forks, type_blast_radius). Kept at `_proof/baseline-gates.keep.txt`.
- After building: same command → 34 pass · 7 FAIL, identical gate-by-gate. All 7 inherited; the runner grades the pack, not `out/`.
- `--browser` runner: started, did not finish inside the 150 s call limit. Not run to completion.
- Provenance: `gen_provenance_receipt.py --mint` on all 10 pages (3 spliced regions each: footer, drawer scrim, toast region); `--check` clean; `_validate_receipt.py` PASS (+UNPROVEN retrievalSet / behaviour-address, pack-declared).
- Screen checks: `TMPDIR=<run tmp> _validate_screen.py out/<page>.html` → exit 0 on all 10 (receipt ✅, compose ✅, icon-source ✅, a11y ✅; composition C9 green, C1 gaps UNPROVEN — they live in linked canon.css).
- `_validate_screen.py --render`: state-contrast FAILS on the status-strip chips and KPI delta seats. The same check on the pack's own Template-dashboard-bento fails the same way (12) — inherited class. The dark leg on sub-pages reports the overview's chips; not investigated.
- Driven browser (Playwright, seat shell): 78 scripted checks, 78 pass, 0 console or page errors — filters (URL, chips, reload), theme, legend isolate/reset, tooltip, table view, drill-through, whole-card KPI, every workflow's refusals and success, modal focus, drawer focus/inert/Escape/focus return, sort, paging, page size, search, CSV downloads, persistence after reload.
- DOM geometry and computed spacing at 1440 light, 1440 dark, 1280: no horizontal scroll, every content column on x = 32, 4px KPI gutters, 40px outer wall gutter, 24px card padding, no chart label overlaps, no clipped text, drawer content inside the sheet.
- Visual review: unavailable (vision disabled). No screenshot was opened.

## Gaps
1. Masthead nav fits wide desktop only (fits at 1280; collides below ~1150).
2. Dark mode: bento ground equals page ground (template dark ground is open); state-contrast reds above are inherited.
3. Composition gate cannot read linked canon: I declared `--layout-bento-columns:6` and restated canon's four-column lead pin in harness CSS so C9 could read it.
4. Harness layering: a `.layer-top` wrapper puts the confirm modal above the drawer scrim; the pack gives modals no z-index.
5. The bento template's own footer region mints a behaviour address its meta denies (FAIL:BEHAVIOUR-ADDRESS-DISAGREES); I spliced the identical footer from App-shell-side-nav.
6. Pack small targets: breadcrumb links (10px tall) and legend swatches (12px), as given.
7. Charts stretch to the tallest tile in a row (canon's fill rule), so some are ~560px tall.
8. PDF/Excel export not provided (CSV/JSON only). No real banking connection; all rates, entities and outcomes are simulated. Keyboard grid cell navigation (Data-grid's roving focus) not implemented — native table with links.
