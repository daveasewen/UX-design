# Run report — cand2-r2 (Spider v1.0.14 candidate 2)

Lane: on-canon. Pack zip sha256 8a75ce32…aee47e3 (matched). Entry: `out/index.html`; ten linked `.html` pages sharing one shell, filters and state.

## Pack files read, in order
CLAUDE.md · AGENTS.md · FIRST-SESSION.md · README.md · skills/grill-me (+ brief-template.md) · skills/generate-from-canon · skills/check-with-gates · skills/check-against-design-system · skills/usability-review · skills/draft-a-new-pattern (opening) · knowledge/_RUNBOOK-compose-from-canon.md · `_compose_slice.py --help` and its seed · gate `--help` texts · knowledge/_render/_bento_edit_rails.json · showroom/index.json · metas of the chosen parts · the snippets below · dv-render.js header · targeted canon.css greps.

## What I built
The ten linked views the prompt names. Common theme, light/dark switch, bento wall on the lightest-grey ground (`--surface-subtle`, 4px rim = inner gutter), title area and page untouched.

Components (copied from `knowledge/snippets/`, 24–33 receipted regions a page): App-shell-side-nav (10 destinations ⇒ side nav, per its `when`), Kpi-tile ×4, Data-grid, List-items, Drawer, Modals + Textarea (audit note), Toast, Dropdown, Segmented-control, Button, Section-heading-lockup + Badge, Search-field, Pagination, Tabs, Summary, Timeline, Alert, Selection-controls switch, Input-fields. Layout on canon's bento grammar (`cn-template-dashboard-bento`, lead/evidence/context groups, stat-card panels).

Charts, all drawn by `dvRender` from one `const DATA`, re-drawn on every filter: column, bar, grouped-column, stacked-column, line, multiline, stacked-area, donut, pie, combo, scatter, histogram, boxplot, bullet, butterfly-h, butterfly-v, candlestick, sparkline (all registered types).

Workflows: payment approve/reject (validated audit note), exception acknowledgement, trade amendment, new service request, message read/reply, report run and schedule, CSV export on every page, exposure drill-through to positions and limits, decision cards opening the record. State persists in localStorage and the URL.

## Questions I would have asked, and the default taken
1. Theme — answered (Common). 2. Modes — answered (both). 3. Density/width — answered (comfortable, wide desktop; checked at 1440 and 1920 only). 4. Brand — answered (masterbrand logos, bound by the shell). 5. Data — answered; I invented Northwind Group: 8 entities, 5 regions, 9 currencies, fixed FX shown on the FX page. 6. Off-limits — answered.
Dashboard bento — the prompt says bento; taken as yes. Discovery I would have asked: three KPIs don't fill the four-column lead row — took a fourth, "Net cash flow, period to date"; funding headroom defined as undrawn committed facilities, available liquidity as cash + headroom; the CEO approval limit taken as £50m. No `briefs/` file written — the pack is read-only to me; the answers are here.

## Proof (commands run from `pack/`, seat render env for browsers)
- Baseline, before any UI: `python3 ci-template/run-gates.py` → 35 pass · 8 FAIL · 0 could-not-ask. All inherited: grid, roles_resolve, token_forks are real pack reds; the other five refuse because the runner passes no page or argument.
- After the build: same command → the same 43 verdicts (`diff` shows none changed).
- Provenance: `gen_provenance_receipt.py --mint` on each page, then `build-tools/mint.py` sets each chart region's `script` to its meta's address. The pack mint writes `dv-behaviour.js`, but its own gate demands `dv-render.js` (FAIL:BEHAVIOUR-ADDRESS-DISAGREES without the fix).
- `_validate_receipt.py out/*.html` → 4 PASS; 6 FAIL:BEHAVIOUR-NOT-LOADED on the Data-grid pages. NEW red, pack cause: the resolver counts the Data-grid snippet's APOLLO-DEMO-fenced script as part of `#script`. A page can only pass by copying fenced harness, which s258-D3 forbids. The edited copy is detected (87% shared, the DATA literal → `window.CEO_ROWS`).
- `_validate_screen.py` each page → compose ✅, a11y ✅, composition UNPROVEN (C9 bands), icon-source ❌ 1 each. That one is a false positive: the regex runs from the word `<svg>` in a dv-render.js comment to a later `</svg>`.
- Browser (Chromium via seat env): `build-tools/smoke.py` → 10 pages × light/dark, every chart drawn, **0 console errors**. `build-tools/drive.py` 5 groups → **54/54 checks pass, 0 console errors**. Covered: filters re-driving KPIs/charts/grids/lists, URL and reload persistence, theme carry, drill-through, legend, tooltip, table view, sort/page/size/search, approve/reject validation + audit, acknowledge, tabs, service-request validation, list search/sort/page, exports, nav rail, skip link, drawer focus in and back on Escape.
- `build-tools/spacing.py` (DOM, 1440 and 1920) → inner gutters 4px (±0.3 subpixel), group gutter 24px, wall padding 4px, filter gap 16px, filter controls bottom-aligned, no sideways overflow, no ragged row bottoms.
- `_validate_geometry.py --widths 1440` → liquidity, reports, settings clean. G7 overlaps all fall on grid rows scrolled out of the Data-grid's own 380px box (`elementFromPoint` shows the hint on top). G8: canon's `.kpi-lbl` clips descenders (reproduced on a bare canon page); G6: engine zero-baseline bands.
- `_validate_own_size.py` → 59 advisories, one cause: the shell and bento scopes' leading-trim rules reach nested chart legend buttons and table headers (16.7px against 20px).

Not run: visual review (unavailable — vision disabled), `run-gates.py --browser`, 390px, screen reader, state-contrast on my pages.

## Gaps
- Dark mode: the lightest-grey section and white tiles both resolve to #1F1F1F (rails `page_rail.resolved`), so tiles lose definition.
- App-shell-side-nav is a fixed 640px frame; the app scrolls inside it (no full-viewport shell in the pack).
- Data-grid is hard-wired to five columns (date/payee/ref/type/amount): other record types are mapped onto it; sort announcements and column-filter chip names still say "Payee"; the pager lists every page (accounts defaults to 24 rows so it fits).
- Filter-toolbar-bar not used (its script is bound to its demo), so the filters are Dropdown + Segmented-control; no date-range picker.
- All banking is simulated, with no live connections or credentials. The over-limit approval path is never reached by this data.
- A drill-through also sets the shared region filter.
