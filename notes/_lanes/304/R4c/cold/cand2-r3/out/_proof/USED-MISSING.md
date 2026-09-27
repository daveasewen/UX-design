# Used / missing — CEO banking prototype (generate-from-canon Output)

Lane: on-canon (Apollo skills in `pack/skills/`). Brief: `../briefs/2026-09-27-ceo-banking-prototype-grill.md` (theme Common from SETTINGS; both modes; comfortable, wide desktop; masterbrand only; placeholder data; no invention).

## Seed runs (step 1)
- `python3 knowledge/_compose_slice.py "CEO international banking dashboard: KPI tiles ... modal forms" --out seed.json --explain` → `_seed/seed.json` (23 components, 75 governing rulings, 27 unresolved; chart-panel had no intent).
- Typed chart runs: `--intent change-over-time` (line, stacked-area, combo, candlestick, sparkline, kpi-tile) · `--intent comparison` (bar, butterfly-h/-v, bullet) · `--intent composition` (donut, pie, ...) · `--intent distribution` (histogram, boxplot) · `--intent relationship` (scatter). Files in `_seed/`.

## Decision table (question → role → part → `when` true for the data → rulings)
| question | role | part | why | rulings |
|---|---|---|---|---|
| Can we fund our plans? (cash, liquidity, headroom, net flow) | headline-metric | kpi-tile `.as-link` | series exists (30 days) → beats stat-card; links to the sub-page | s245-D7 (KPI self-group), s247-D3 |
| Where are we exposed — by region vs limit | chart-panel / comparison | chart-bar grouped-column (overview), chart-butterfly-h (risk) | categories × 2 series; drill-through on click/Enter | s249-D4 |
| Share of a whole (currency, facility type, status, instrument) | composition | chart-donut, chart-pie | parts of whole, ≤5 categories (top 4 + Other) | s249-D4 |
| Movement over 30 days | change-over-time | chart-line multiline, stacked-area, combo, candlestick, sparkline | time series × 1–5 series | s249-D4 |
| Utilisation against policy | comparison / target | chart-bullet | target is the point | s249-D4 |
| Distribution of values | distribution | chart-histogram, chart-boxplot | one measure, banded / five-number summary | s249-D4 |
| Exposure against utilisation | relationship | chart-scatter | two measures per position | s249-D4 |
| Import vs export by region | comparison | chart-butterfly-v | two series mirrored | s249-D4 |
| What needs my attention? | record-list | list-items in a stat-card panel + section-heading-lockup | each row a button to the record it summarises | s245-D6 (role words) |
| Records to search, sort, filter, page | record-list | data-grid (verbatim script) | seed winner for the task | — |
| Detail and act (approve, reject, acknowledge, amend, draw down) | overlay | drawer + summary + textarea | one modal surface at a time (`mustNot`) | — |
| Page frame, 10 destinations | page-frame | app-shell-side-nav parts | top-nav `when`: destinations ≤ 7 fails → side nav | s230-D1 |
| Wayfinding | wayfinding | the shell's own `.sn` nav + `.sh-crumbs` | navigations yields to sidebar-nav with the side-nav frame | — |
| Shared entity / region / period | input | dropdown (boxed) ×3 | lightest control; filter-toolbar-bar's facets are grid-bound | — |
| Theme switch | input | segmented-control | single select of two | — |
| Confirmation | feedback | toast | transient status | — |
| Service request form | input | input-fields, dropdown, textarea, button | — | — |
| Notification preferences | input | selection-controls checkbox | — | — |
| Layout | arrangement | bento grammar in `.cn-template-dashboard-bento`; `.l-row`/`.l-stack` | dashboard role, spans 6 and 3 | s217-D3, s219-D1, s245-D8, s248-D1 |

Tokens: every colour/space is a canon var; page CSS uses only `--surface-subtle` (rails bentoBg grey) and `--bento-dashboard-main` (theme's main spacing). Icons: shell/KPI/grid/toast sprites spliced; eight library glyphs copied byte-for-byte (dashboard, liquidity-management, fx, alert, trade-finance, document-report, contact-message, download).

## Behaviour manifest
| control | drives | state persists in |
|---|---|---|
| Entity / Region / Period dropdowns | every KPI, chart and grid on the page; nav and KPI links carry them | URL query + localStorage |
| Nav links, crumbs, collapse toggle | page; rail width 64px | URL; localStorage (rail) |
| Theme segmented (title row, settings) | `data-theme` on `<html>` | localStorage (+ `?theme=`) |
| Chart marks (click / Enter) | drill-through: region → risk page scoped; currency → risk grid column filter; status/type → grid filter | URL / grid state |
| Chart sort and value/percent segments | re-render from the same spec | — |
| Legend swatches / names | dim / isolate series (dv-legend) | — |
| Grid search, column filters, sort, rows per page, pager, density, select, edit reference | grid rows (Data-grid script, verbatim; fed via its globals; `renderPager` replaced with a windowed pager — authored) | localStorage per page |
| Grid row click / Enter | drawer detail | — |
| Drawer actions | approve / reject (audit note, limit and two-approver rules), acknowledge exception (≥15-char note), request amendment / drawdown (creates service request), mark resolved, download CSV | localStorage (decisions, acks, requests, audit) |
| Export CSV (title row, reports list) | Blob download of the filtered data behind the page | audit log |
| Service request form | validated; adds a request; updates charts and KPIs | localStorage |
| Inbox rows | message drawer; marks read; reply prefills the form | localStorage |
| Search / profile (app bar) | focus grid search or go to accounts / user summary drawer | — |
| Settings | default filters, notification checkboxes, reset data | localStorage |

Behaviour addresses: dataviz partials (AUTO-BEHAVIOUR blocks, verbatim); `Data-grid.reference.html#script` script[0] verbatim; `Textarea.reference.html#script` verbatim; everything else is the authored `#ceo-app` script.

## Gaps
See RUN-REPORT.md § Gaps (same list).
