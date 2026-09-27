# RUN-REPORT — cand2-r3 (pack Apollo-Spider v1.0.14 candidate-2, sha256 8a75ce32…e47e3 verified)

Lane: on-canon. Output: ten linked pages in `out/` (entry `out/index.html`), not views in one page. Pack referenced in place (`../pack/...`). Supporting: `out/briefs/` (grill brief), `out/_proof/` (all evidence, incl. `USED-MISSING.md` = decision table + behaviour manifest), `out/_seed/`, `out/_build/` (generator + page script).

## Pack files read, in order
CLAUDE.md · FIRST-SESSION.md · README.md · skills/generate-from-canon, check-with-gates, grill-me (+brief-template), check-against-design-system, usability-review SKILL.md · `_compose_slice.py --help` + seed runs · showroom/index.json · metas (shells, nav family, kpi-tile, stat-card, data-grid, filter-toolbar-bar, drawer, modals, dropdown, legend, cards, chart-line/-bar, template-dashboard-bento `$bentoGrammar`, every meta's `behaviour`) · `_render/_bento_edit_rails.json` · `canon/dv-render.js` header + partial headers · canon.css sections (bento, side-nav shell, kpi, textarea, dropdown) · `--help` of gen_provenance_receipt, _validate_receipt/_screen/_composition/_own_size/_geometry/_state_contrast · ~26 snippets (anatomy, regions, scripts). Not read: draft-a-new-pattern, AGENTS.md, memento-package, runbooks.

## What was built
Pages: Overview · Accounts and transactions · Liquidity and funding · Payments and approvals · FX and markets · Risk and limits · Trade finance · Reports · HSBC messages and service requests · Settings. Each: side-nav shell (app-shell-side-nav parts), shared filters, bento wall on a lightest-grey section, footer. Components (byte-identical splices, 378 regions across the 10 pages, all receipted): kpi-tile, 14 chart types (bar ×4 figures, line, donut ×2, pie, stacked-area, combo, bullet, candlestick, butterfly-h, butterfly-v, scatter, histogram, boxplot, sparkline ×3), data-grid, drawer, summary, textarea, dropdown, segmented-control, button, list-items, section-heading-lockup, input-fields, selection-controls, toast. One dataset `CEO_DATA` (named so because the verbatim Data-grid script owns global `DATA`). Workflows: approve/reject with limits and audit notes, exception acknowledgement, trade amendment and drawdown requests, service requests, message reading/reply, CSV exports, settings/reset.

## Questions I would have asked (defaults taken)
The six grill questions were answered by SETTINGS. Discovery: approval authority (default £25m; ≥£5m needs two approvers + note) · headroom definition (liquidity − scaled £600m buffer − facilities maturing in 60 days) · entities (fictional Meridian Holdings, 8 entities, 5 regions) · materiality (>100% breach, 92–100% near limit) · top vs side nav (side: 10 destinations > 7) · dark ground collapse (kept ruled token). "Dashboard bento — is that right?" → yes per SETTINGS.

## Proof
- Baseline before building: `python3 ci-template/run-gates.py` → **35 pass · 8 FAIL · 0 could-not-ask** (`_proof/baseline-run-gates.txt`). After: identical verdict lines (`after-run-gates.txt`); those gates grade the pack, not these pages.
- Provenance: `gen_provenance_receipt.py --mint` on all 10 pages; `--check` current on all.
- Receipt (`_validate_receipt.py`, each page, exit 1): hashes, regions, demo-chrome all clean; red only on two INHERITED classes — (a) BEHAVIOUR-ADDRESS-DISAGREES on every chart region: the pack's mint writes `dv-behaviour.js`, the metas say `dv-render.js`; reproduced on a page built only by `--compose` (`_proof/repro/`); (b) BEHAVIOUR-NOT-LOADED on Data-grid: the `#script` address includes the APOLLO-DEMO-fenced state-switcher script; not copied (rule 2).
- Screen checks (`_validate_screen.py`, each page): compose ✅, icon-source ✅, a11y ✅, composition UNPROVEN (C9 reads bento grammar only from inline CSS; page links canon), receipt ❌ as above. `--render` (index): state-contrast ❌ only on kpi-delta `data-carries` seats; `_validate_state_contrast.py Kpi-tile` rates the same markup 🟡 exit 0.
- `_validate_geometry.py` @1440, 10 pages: no ✖ except G8 KPI-label descender clip — reproduced on `Kpi-tile.reference.html` itself. Advisories: G6 dead bands, G11 marker on every point, G12 donut ink.
- `_validate_own_size.py` @1440: 146 advisories, all chart-legend buttons and sparkline table cells (canon.css leading-trim vs snippet; reproduced with the figure moved out of every page wrapper); grids, buttons, fields clean.
- Driven browser (Playwright, headless shell): **52/52 checks** (`drive-a/b/c.jsonl`): filters re-drive KPIs/charts/grid and persist in URL and reload; drill-through (region, currency, status, counterparty); decision cards open actionable records; drawer focus/inert/Esc/return; validation refusals; persistence of decisions; sort/search/page/size persistence; exports; legend isolate; tooltips; theme; nav rail; keyboard grid → Enter; zero console errors.
- DOM geometry (`geometry.txt`): 1280/1600 × light/dark × 10 pages: no page overflow, no ragged rows, no partial rows, no tile overflow; ground padding 24, group gutter 24, tile gutter 4. Own-size spot checks equal to showroom for 16 parts (`sizes.jsonl`).
- Visual review: **unavailable** (vision disabled). No screenshot used as evidence.

## Gaps
1. Two inherited receipt contradictions (above) keep every page red.
2. KPI labels clip descenders (inherited); KPI tile 4px taller inside the bento scope (template scope's `.spark-inline` 44px beats Kpi-tile's 40px).
3. Dark mode: grey ground (#1F1F1F) equals the tile surface, so chart/panel tiles lose their edge (rails dark leg is declared provisional).
4. Data-grid columns are fixed; each page maps records onto date/party/reference/type/£ and relabels them; pager extended from outside.
5. Shell's 640px specimen frame and off-canvas menu not used; narrow/phone widths untested and unsupported.
6. Dropdown has no error state; the missing request type is flagged by aria-invalid and toast only.
7. Charts ship snippet demo tables/legends until JS runs; no-JS state shows demo data.
8. Line markers on every point; donut canvas fixed at 300px.
9. Logo `<img>` authored with a page-relative path; filter-toolbar-bar not used.
10. No screen-reader, zoom or 390px testing; no real banking, credentials or market data; all figures illustrative.
