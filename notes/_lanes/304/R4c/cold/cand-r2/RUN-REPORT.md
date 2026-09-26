# RUN-REPORT — cand-r2 (Spider v1.0.14 candidate, sha256 2e827237…5135d verified)

Lane: on-canon. Entry: `out/index.html` — one page, ten hash-routed views (`#/overview`, `accounts`, `liquidity`, `payments`, `fx`, `risk`, `trade`, `reports`, `messages`, `settings`). Pack referenced in place (`../pack/knowledge/canon/*`).

## Pack files read, in order
CLAUDE.md · FIRST-SESSION.md · README.md · skills/grill-me · skills/generate-from-canon · skills/check-with-gates · skills/check-against-design-system (head) · usability-review / draft-a-new-pattern (heads) · `_compose_slice.py` seed · showroom/index.json · `_RUNBOOK-compose-from-canon.md` · `gen_provenance_receipt.py` / `_validate_receipt.py` / `_validate_screen.py` headers · `_bento_edit_rails.json` · template-dashboard-bento meta `$bentoGrammar` (grammar only) · `dv-render.js` header · canon.css (targeted greps) · snippets and metas of every part used · assets/icons.

## What I built
Shell: App-shell-side-nav (masterbrand, grouped side nav, rail toggle, off-canvas menu, breadcrumbs, legal footer). Shared: Page-header-lockup + theme Segmented-control + Export; Filter-toolbar-bar with Entity / Region / Period dropdowns, applied-filter Tags chips, Clear all. Overview: bento on the `--surface-subtle` ground, one wall per question under a Section-heading-lockup — four whole-tile-link Kpi-tiles (cash, available liquidity, funding headroom, liquidity coverage); stacked area + combo; horizontal bar (drills to Risk, region-filtered) + donut (drills to Risk, currency search) + pie; two Stat-card panels with Summary rows linking to payment and exception records. Sub-pages: a chart bento plus Data-grid records (search, sort, paging, rows-per-page, density, row selection, empty state), Drawer details, Timeline audit trails, Limits-meter, List-items inbox, Toast, Alert, Input-fields, Textarea, Dropdown, Selection-controls switches. Charts: all 13 engine types via `dvRender` from one `DATA` — column (sortable), bar, grouped column, line (daily/cumulative), multiline, donut, pie, stacked area, combo, scatter, bullet, candlestick, histogram, boxplot, butterfly, sparkline — legends rebuilt per series. Workflows (simulated, validated, persisted): approve/reject payment (reason ≥10 chars), acknowledge exception (audit note ≥20), drawdown (≤ undrawn, business day), book FX deal, new service request / trade amendment, message reply and read state, run report / download CSV, export view or selection, settings. State: view + filters + theme in the URL, grids/decisions/rail/settings in localStorage.

## Questions I would have asked (defaults taken)
Recorded in `out/briefs/2026-09-26-ceo-banking-prototype-grill.md`: placeholder group (Northwind, 8 entities, 5 regions); CEO as one of two approvers; single page vs files (single page); bento on sub-pages (yes, charts only); "dashboard bento — is that right?" (skip = yes).

## Proof
- Baseline before UI: `python3 ci-template/run-gates.py` → 35 pass · 6 FAIL · 0 could-not-ask (composition, grid, polarities, receipt, roles_resolve, token_forks). After build: identical verdicts, gate for gate (`_proof/runner-after.txt`) — the runner grades the pack, not my page, so no new reds and none inherited by me.
- Provenance: `gen_provenance_receipt.py --mint out/index.html` → 56 receipted regions (40 markup, 16 engine blocks). `_validate_receipt.py` → 40 ✅, **FAIL:BEHAVIOUR-ADDRESS-DISAGREES on the 16 chart regions — inherited**: the pack's own `--compose` of one donut (`_proof/repro/`) fails identically (mint writes `dv-behaviour.js`, metas say `dv-render.js`).
- Screen checks: `_validate_screen.py out/index.html` → compose ✅, icon-source ✅, a11y ✅, composition n/a (bento built at runtime), receipt ❌ (above). TMPDIR redirected so another run's ledger row was not clobbered.
- State contrast: `--render` cannot finish in one 180 s call; I drove the pack's `audit_page` per view × light/dark with click actions blocked (`_proof/contrast-*.json`). 0 text failures except (a) List-items pressed rows 1.94:1 — the List-items snippet fails identically; (b) Common primary button pressed 3.64:1 — a canon-only page reproduces it. Icon warnings in dark only.
- Browser drives (Chromium, 1920×1080): A 66/66 (filters re-drive KPIs/charts/grids, chips, URL, reload persistence, every nav view drawn, drill-through, search/sort/page/density/selection, CSV exports, all workflows incl. validation refusals, theme and rail persistence, zero console errors); B 92/93 geometry (row edges shared, 4px gutters, equal wall gaps, dead space ≤24px, no overflow light and dark, filter bar = header = content width, ground 24px on `rgb(240,240,240)`, component heights vs reference snippets); C 10/10 keyboard (skip link, menu arrows/Enter/Escape, drawer focus trap and return, focusable chart marks, 1440 band).
- Visual review: unavailable (vision disabled). `_proof/record-only-*.png` are records, not evidence.

## Gaps
1. Receipt gate red on chart regions — inherited mint/meta disagreement (reproduced).
2. App-shell-side-nav ships a fixed 640px frame; the page does not resize it, so content scrolls inside the frame on tall windows.
3. canon's bento role vars key `legacy` only; `common` falls back to mono's 40px wall gutter (rails say 24).
4. Kpi-tile spark renders 44px (canon) vs 40px (snippet) — the one failed size check.
5. Chart "View as table" panel lays out while closed and overflows its figure; views clip sideways (`overflow-x:clip`) instead of restyling.
6. Data-grid, Filter-toolbar-bar and Textarea are copied but not receipted (their `#script` addresses target demo ids); their behaviour is authored.
7. Dark ground: `--surface-subtle` and tile surface are near-identical in dark (canon's provisional dark leg).
8. At 1440 the ≤1100 band re-flows half tiles to full rows (canon behaviour).
9. No JS-off fallback: templates are inert, `<noscript>` explains.
10. Not run: `run-gates.py --browser` (killed at 110 s), `_validate_screen.py --render` whole-page, usability review, screen readers, real devices, any banking connection.
