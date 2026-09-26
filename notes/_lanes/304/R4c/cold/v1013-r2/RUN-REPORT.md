# Run report — v1013-r2 (Apollo Spider v1.0.13, cold)

**Output:** `out/` — ten linked HTML pages (not views): `index.html` (overview), `accounts`, `liquidity`, `payments`, `fx`, `risk`, `trade`, `reports`, `messages`, `settings`. They link `../pack/knowledge/canon/{canon,type}.css` and the logos in place, so the frozen copy renders only beside a `pack/` folder.

## Pack files read, in order
`CLAUDE.md`, `FIRST-SESSION.md`, `README.md`, `skills/generate-from-canon`, `check-with-gates`, `grill-me`, `check-against-design-system`, `usability-review` SKILL.md; `showroom/index.json`; `_RUNBOOK-compose-from-canon.md`; `_render/_bento_edit_rails.json`; snippets Template-dashboard-bento, App-shell-side-nav, Template-list-index, Template-wizard (field grammar), Kpi-tile, Chart-* (all 13), Drawer, Modals, Toast, Input-fields, Textarea, Selection-controls, Segmented-control, Status-indicator, Data-grid (read, not used); their metas; canon.css selectors; dv-* engine headers; receipt/screen gate help; `assets/icons/`.

## What was built
Frame: App-shell-side-nav (ten destinations, rail collapse; its script carried verbatim). Each page: Template-dashboard-bento header (title, actions, status strip, shared filters) over a bento wall on `--surface-subtle` (rails' "lightest grey"); white stat-card/kpi-tile modules; 40px wall gutter, 4px group gutter. Records use the Template-list-index table grammar (search, facets, sortable headers, pager, rows per page, bulk bar). Overlays: Drawer (record detail), Modals (decisions), Toast. One `const DATA` per page (8 entities, 7 currencies, 30-day series, 264 transactions, 56 payments, 48 positions, 40 trade instruments).

Charts (all via the pack's `dvRender`, engine spliced verbatim): stacked, grouped, vertical and horizontal bar; line and multiline; stacked area; combo; donut; pie; histogram; scatter; boxplot; bullet; candlestick; butterfly H and V; sparkline; plus KPI inline sparks. Legends, tooltips, table view and CSV copy work.

Workflows (simulated, stored in localStorage): payment approve/reject (single and bulk, audit note required when flagged or rejecting), exception acknowledgement with audit trail, trade discrepancy instructions, drawdown request, service requests (validated), message read/reply, report run and CSV export, FX converter, settings defaults, reset. Shared filters live in the URL and carry across nav links.

## Questions I would have asked, and the default I took
1. Grill-me (six questions). All answered by SETTINGS; no brief written to `briefs/` (pack is read-only for me).
2. "dashboard bento — is that right?" Taken as yes (SETTINGS).
3. KPI count: the lead row is four wide at every band, and three KPIs were asked for. I added **Liquidity coverage** as the fourth.
4. How funding headroom is defined. I used available liquidity less a £350m policy buffer, apportioned by cash share.

## Proof
- **Baseline** (`python3 ci-template/run-gates.py`, fresh unzip): 34 pass · 7 FAIL (composition, grid, polarities, receipt, roles_resolve, token_forks, type_blast_radius) · 0 could-not-ask. **After the build: identical verdicts.** The runner grades the pack, not `out/`, so it cannot show a new failure of mine.
- **Provenance:** `gen_provenance_receipt.py --mint` on all 10 pages. Receipted regions: the App-shell footer plus the chart-engine AUTO-BEHAVIOUR blocks (6–9 per page). `_validate_receipt.py`: PASS on all 10 (+2 UNPROVEN: retrievalSet; footer meta has no behaviour address).
- **Screen checks:** `_validate_screen.py out/*.html` (TMPDIR set to my folder): **PASS**. Receipt, compose, icon-source and a11y are green on all 10. Composition is UNPROVEN (C9): the pages declare no column count because the bento grammar lives in the linked canon.css.
- **`--render` (state contrast):** timed out on `index` at the 180s call cap. On `settings` it gave 3 ❌ "seatdecl" on the status-strip chips. The pack's own Template-dashboard-bento gives 12 of the same, so this is **inherited**.
- **Driven browser checks** (Playwright, 1600×1000; `proof/drive1-4.py`): **91 checks, 0 FAIL, 0 console errors.** Covered: theme, filters, persistence, tooltips, legends, drill-through, drawers, validation and every workflow, CSV downloads.
- **Geometry and spacing** (`proof/geom.py` at 1280, 1440, 1600, 1920): no document overflow and no clipped descendants at 1440 and above. Chart text overlaps went from 58 per chart to 0 after the fixes below. Computed spacing: wall padding 24/40 with 32 sides; stat-card padding 24; KPI padding 16; header rule 24px below the last control. At 1280, three wide tables scroll inside `.dg-scroll`.
- **Visual review: unavailable.** Vision was disabled and no screenshot was used as evidence.

## Fixes made during the proof (all mine)
- Added `data-pl-fit="text.dv-axis"` to cartesian canvases, so the tick gutter fits `£m` labels.
- Added authored JS that thins 30-day x labels, keeping the last day (the candlestick partial's own precedent).
- Set scatter `data-pb` to 44: the engine's x title collided with the centred tick.
- The drawer now steps aside while a dialog is open. The pack's Drawer and Modals do not stack, so the modal sat under the drawer's scrim.
- Moved the engine blocks to the end of `<body>`. The icon gate had paired a `<svg>` in an engine comment with my later markup.
- Dropped the filter bar's trailing margin (it measured 36px, off the rail).

## Gaps
1. **Inherited, Common theme:** the template's KPI labels and periods measure 3.71:1 and the sidebar group labels 3.75:1. Reproduced on a probe page using the pack's markup verbatim (Mono passes). Not fixed, because fixing it would mean restyling components.
2. The line-family engine labels every category, so the label thinning is authored page JS. The engine has no option for it.
3. Row links in tables and the "View all" links are text-height targets, under 24px. The template's own pattern.
4. The logo is copied with its asset path edited, so it is not receipted. The App-shell nav, figures and forms are composed to snippet structure but not spliced byte-for-byte.
5. With JavaScript off, chart tables are empty (rows are engine-written).
6. Not run: the runner's `--browser` gates, and `--render` beyond `settings`. Mobile widths untested. No live banking or credentials; every figure is illustrative.
