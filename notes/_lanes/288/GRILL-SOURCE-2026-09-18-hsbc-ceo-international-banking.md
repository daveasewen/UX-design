# Grill brief — HSBC CEO international banking

Date: 2026-09-18
Task: An interactive international banking prototype for CEOs of HSBC corporate and institutional clients, with linked sub-pages and simulated workflows.

Design lane: On-canon, using Apollo skills.
Project lane: New CEO project, related to but separate from the existing group-treasurer dashboard. Preserve the original brief and screen.
Extends: [2026-09-14-international-banking-dashboard-grill.md](2026-09-14-international-banking-dashboard-grill.md).

| # | question | answer |
| --- | --- | --- |
| 1 | Theme | Supercharge — explicitly requested on 2026-09-18; replaces Console for this project only |
| 2 | Light, dark or both | Both — inherited by extending the original brief |
| 3 | Density and width | Comfortable; wide desktop — inherited |
| 4 | Brand assets | Supplied HSBC masterbrand and Apollo tokens; no additional assets — inherited |
| 5 | Data | Realistic placeholder entities, currencies, 30-day time series, and enough rows for sorting, filtering and paging — inherited; all workflows simulated |
| 6 | Fixed and off-limits | Apollo accessibility defaults and existing patterns only; invent no components, variants, colours or icons — inherited; no live banking connections |

Skipped: none.
Defaults used: none; unchanged design settings are inherited, not new answers.

## Discovery

- Audience: CEO view for HSBC corporate and institutional clients — explicitly requested, replacing the original group-treasurer audience for this lane.
- Layout: “bento please” — explicitly confirmed.
- Project relationship: “extend the brief this is a new but related project in a different project lane”.
- Delivery: “fully interactive with all sub-pages, as complete as possible”.
- Simulation boundary: Designer confirmed an interactive prototype with linked sub-pages and working simulated workflows, not live banking services.
- Reporting basis: GBP over 30 days — inherited; original market-risk-first prioritisation is not treated as a CEO choice.
- Product grouping and linked views: Confirmed on 2026-09-18 — “yes this is good for now”.
- Brief exhausted for this prototype scope; further refinements remain possible after review.

## Confirmed scope

CEO overview organised around three questions:

1. **Financial resilience — can we fund our plans?** KPI tiles for cash, available liquidity and funding headroom.
2. **Risk outlook — where are we exposed?** Regional/currency exposure chart with drill-through to underlying positions and limits.
3. **Decisions — what needs my attention?** Summary cards for pending approvals and material risk exceptions, each linking to actionable records.

Linked views: overview; accounts and transactions; liquidity and funding; payments and approvals; FX and markets; risk and limits; trade finance; reports; HSBC messages and service requests; settings.

Proposed working behaviours: shared entity/region/date filters, GBP reporting with explicit illustrative FX rates, searchable/sortable/paged records, detail views, validated simulated approvals and requests, risk acknowledgements with audit notes, exports, messages, theme switching, and persisted navigation/filter/workflow state. No real credentials or banking integrations required.

## Preservation and proof

- Create new CEO screen files; do not overwrite the existing treasurer screen, canon, tokens, or validators.
- Run and retain the pack baseline before UI implementation; distinguish inherited failures from new regressions.
- Mint provenance, run screen checks and the pack runner, then drive actual browser interactions and inspect screenshots and console errors where available.
- Describe unsupported or untested behaviour as gaps; do not claim production banking capability or unperformed browser validation.

Verification direction, 2026-09-18: “vision is disabled there's no work-around, the usual errors are spacing so double check thsi”. No visual review or workaround. Use actual browser interactions, DOM geometry and computed spacing; explicitly report visual review as unavailable. A screenshot captured earlier is not visual-validation evidence.
