Build an interactive international-banking prototype for the CEOs of HSBC corporate and institutional clients, with linked sub-pages and working simulated workflows. Use the Apollo skills and stay on-canon.

This is a new project, related to the existing group-treasurer dashboard but separate from it. Create new CEO screen files; do not overwrite the treasurer screen, canon, tokens or validators.

SETTINGS — already decided, do not ask
- Theme: Common. Light and dark, with a theme switch.
- Layout: bento, comfortable density, wide desktop. The section the bento sits in takes the lightest grey, so the white tiles have definition against it; the rest of the page and the title area stay as they are.
- Brand: the supplied HSBC masterbrand and Apollo tokens. No other assets.
- Data: realistic placeholder entities and currencies, GBP reporting with explicit illustrative FX rates, 30-day time series, and enough rows to sort, filter and page.
- Off-limits: Apollo accessibility defaults and existing patterns only. Invent no components, variants, colours or icons, and use each component as the pack gives it, at its own size. No live banking connections or real credentials.

DATA VISUALISATION
Be liberal with data visualisation. Wherever a figure moves over time, compares across entities, regions, currencies or products, or is a share of a whole, show it as an Apollo chart rather than a bare number or table, on the overview and on every sub-page. Use the full range of chart types the pack provides, each with its legend, tooltips and behaviour working.

THE OVERVIEW ANSWERS THREE QUESTIONS
1. Financial resilience — can we fund our plans? KPI tiles for cash, available liquidity and funding headroom.
2. Risk outlook — where are we exposed? A regional and currency exposure chart that drills through to the underlying positions and limits.
3. Decisions — what needs my attention? Summary cards for pending approvals and material risk exceptions, each linking to a record you can act on.

LINKED VIEWS
Overview · accounts and transactions · liquidity and funding · payments and approvals · FX and markets · risk and limits · trade finance · reports · HSBC messages and service requests · settings.

WORKING BEHAVIOUR
Make it fully interactive and as complete as possible across every sub-page: shared entity, region and date filters; searchable, sortable, paged records with detail views; validated simulated approvals and service requests; risk acknowledgements with audit notes; exports; messages; theme switching; navigation, filter and workflow state that persists. For each interaction, pick the lightest pattern that does the job.

PROOF
- Run and keep the pack baseline before building the UI, and tell inherited failures apart from new ones.
- Mint provenance, run the screen checks and the pack runner, then drive real browser interactions and check DOM geometry, computed spacing and console errors.
- Vision is disabled and there is no work-around; the usual errors are spacing, so double-check spacing. Report visual review as unavailable. A screenshot is not visual-validation evidence.
- Name anything unsupported or untested as a gap. Do not claim production banking capability or browser checks that were not run.
