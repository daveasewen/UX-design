# RUN-REPORT — cand2-r1 (Spider v1.0.14 candidate-2, sha256 8a75ce32…e47e3 verified)

Lane declared: **on-canon**. Frozen build: `out/` (entry `out/index.html`; pages reference `../pack/` in place).

## Pack files read, in order
CLAUDE.md · AGENTS.md · FIRST-SESSION.md · README.md · skills/grill-me · skills/generate-from-canon · skills/check-with-gates · skills/check-against-design-system (draft-a-new-pattern and usability-review not opened) · showroom/index.json · `_compose_slice.py` seed · component metas (`when`, `behaviour`, antiPatterns for ~30) · template-dashboard-bento meta `$bentoGrammar` · `_render/_bento_edit_rails.json` · canon.css (targeted reads of scopes) · snippets: App-shell-side-nav, Template-dashboard-bento (grammar only), Kpi-tile, Stat-card, Data-grid, Filter-toolbar-bar, Dropdown, Segmented-control, Page-header-lockup, Section-heading-lockup, Drawer, Modals, Toast, Alert, Status-indicator, Summary, Tags, Tabs, Table, Button, Textarea, Input-fields, Selection-controls, Limits-meter, List-items, Pagination, Empty-state, Search-field, Timeline, 13 Chart-* · canon/dv-render.js + partial headers · gate help texts · assets/icons listing.

## What I built
Ten linked pages (separate files, shared `app.js`): overview, accounts and transactions, liquidity and funding, payments and approvals, FX and markets, risk and limits, trade finance, reports, HSBC messages and service requests, settings. Side-nav shell (10 destinations > 7 ⇒ side nav per the graph), page-header lockup, shared entity/region/date filters + light/dark switch, bento walls on a lightest-grey section. One in-page `const DATA` per page (fictional group, 8 entities, 4 regions, 10 currencies, illustrative FX, 30-day series; 240 transactions, 48 payments, 72 positions, 42 deals, 38 instruments…). Components: kpi-tile (as-link), data-grid (verbatim markup + verbatim script, rows re-bound from DATA), list-items, pagination, search-field, drawer, modals, toast, alert, summary, timeline, limits-meter, dropdown, segmented-control, textarea, input-fields, selection-controls, tags, status chips. Charts (all via `dvRender`, each with legend/table/CSV): column, bar, grouped-column, stacked-column, line/multiline, stacked-area, combo, donut, pie, bullet, candlestick, scatter, histogram, boxplot, butterfly-h, sparkline. Workflows: payment approve (two-step, notes, screening check) / reject / bulk approve; risk acknowledgement with audit note → timeline; service requests with validation; message replies; trade amendment → SR; CSV exports; drill from exposure chart to positions; persistence (URL + localStorage). Decision table: `out/USED-MISSING.md`.

## Questions I would have asked (defaults taken; also in `out/briefs/…-grill.md`)
Dashboard bento? → yes (prompt). Fourth lead KPI? → added "committed outflows, next 30 days" (lead row is four across). Headroom definition → liquidity − committed outflows − policy buffer. Approval authority → CEO approves ≥ £1m; notes required to reject and above £10m. Acknowledgement commitment → note ≥ 20 chars + confirm box. Exports → browser CSV.

## Proof (commands run at the seat; outputs in `out/_proof/`)
- **Baseline** `python3 ci-template/run-gates.py` before any UI: 35 pass · 8 FAIL · 0 could-not-ask (composition, geometry, grid, own_size, polarities, receipt, roles_resolve, token_forks — all inherited). **After build:** identical verdict lines (diffed) — 0 new.
- **Provenance** `gen_provenance_receipt.py --mint` on all 10 pages; `--check` current. `_validate_receipt.py`: PASS on 4 pages; **FAIL:BEHAVIOUR-NOT-LOADED on the 6 grid pages** — the `#script` resolver counts the grid snippet's APOLLO-DEMO-fenced script (1,447 B) as part of the component; the real script (23,876 B) is carried byte-identical. Copying the fenced script is forbidden (s258-D3), so this is a pack contradiction, reported not worked around.
- **Screen checks** `_validate_screen.py out/*.html` (private TMPDIR): compose ✅, icon-source ✅, a11y ✅ on all 10; composition UNPROVEN (C9 cannot read linked canon.css); receipt as above.
- **Own size** `_validate_own_size.py out/*.html` (advisory): 82 findings, all chart legend buttons 16.7 px vs 20 px and sparkline sr-only table headers — verified cause: the ancestor scope's `text-box-trim` (removing it restores 20 px). Not fixable without restyling (rule 3a).
- **Driven browser** (Playwright, seat Chromium, 1440×900): 84 checks, 84 pass, **0 console errors** on every page and journey — filters re-drive KPIs/charts/grids, URL + reload persistence, theme persistence, nav rail persistence, drill-through, drawer focus-in/trap/Escape/return, keyboard grid open, sort/page/search, validation refusals, approvals/rejections/bulk, acknowledgements + audit trail, SR submit, replies, CSV downloads, reset.
- **DOM geometry** at 1440 and 1920: 0 ragged rows, 0 tiles with > 8 px dead space, 0 horizontal overflow; gutters 4 px inner / 24 px outer (±0.5 sub-pixel); header→filters→ground→footer 24/24/24 px; filter controls share a bottom edge; KPI tiles equal height.
- **Visual review: unavailable** (vision disabled). No screenshot was used as evidence.

## Not run
`_validate_screen.py --render` (state contrast) and `run-gates.py --browser` both exceeded the 180 s call wall — not completed. No mobile/tablet widths driven. No screen reader.

## Gaps
1. App-shell-side-nav ships at a fixed **640 px specimen height**; at its own size the app lives in a 640 px frame with internal scroll (no full-viewport shell in the pack).
2. Dark mode: lightest-grey ground and tiles both resolve #1F1F1F — no tile definition (template marks the dark leg provisional).
3. Receipt gate vs APOLLO-DEMO fence contradiction (above).
4. Nested scopes' `text-box-trim` shrinks chart legends (own-size findings).
5. Data-grid pager renders every page number (no ellipsis) — overflows at 8 rows/page on the 240-row ledger; default set to 24.
6. Data-grid inline reference edits are not persisted; one grid per page (fixed ids).
7. JS off: charts and tables are empty (tbody left for the engine).
8. Legal footer links are placeholders (toast says so).
9. Illustrative data only; no live banking, no credentials, no production capability.
