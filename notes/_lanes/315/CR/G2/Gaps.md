# Gaps — out/dashboard.html

Lane: on-canon. Theme: Console (brief Q1). Everything below is something the system could not supply, a call I made where the designer was not asked, or a claim I could not check. Nothing on this list was improvised into the page as a new component, variant, colour or icon.

## A. Not checked: read this first

1. **Not driven: no browser in this session** (SKILL step 7, no-eyes clause). The page has not been loaded, the console has not been read, no control has been worked, and nothing has been measured. Rule 16 (zero uncaught JS errors) is **unproven**. The authored JavaScript was not parsed or executed by any tool. It was written and re-read by hand only.
2. **Gates not run.** The session conditions forbid running any gate or validator during the build. So `python3 knowledge/gen_provenance_receipt.py --mint out/dashboard.html`, `python3 knowledge/_validate_receipt.py out/dashboard.html`, `python3 knowledge/_validate_screen.py out/dashboard.html` and `python3 ci-template/run-gates.py` were **not run**, and there is no gate verdict to report. Without a minted receipt the receipt gate would stop at `FAIL:NO-RECEIPT`. Under the design contract this screen is a draft, not a result. `skills/check-with-gates/SKILL.md` was not opened, because the conditions ruled out running what it ends in.
3. **No geometry readings** (step 8). I could not measure shared row edges, equal gutters, toolbar width against the wall, dead space under tiles, or each part's rendered height against its showroom page. Expected risk areas:
   - the Table part's own 760px width inside a full-width tile (see C4)
   - the toolbar's `position:sticky` sitting inside the shell's `overflow:hidden` frame, so it will most likely not stick
   - the chart tiles' heights against the 240px evidence row floor

## B. The system is missing it, so it was left out (not invented)

1. **A light/dark mode control.** No part offers one for the shell's action slot. Mode follows the OS; `?mode=light|dark` overrides it and is remembered (rule 15). An on-page toggle needs a part chosen by the designer (Switch or Segmented-control in the masthead is a judgement call I did not make).
2. **An account / profile menu.** The shell snippet draws a "Your profile" button, but no account-menu component has a meta, and a button that opens nothing is a Gap (rule 14). The button was **removed** from the masthead.
3. **"Custom range…" in the date-range trigger.** The toolbar meta delegates it to `date-range-picker` (edge `delegatesTo`). Wiring that picker into a popover is a composition nobody has drawn, so only the 7 / 30 / 90-day presets ship.
4. **PDF export.** No PDF writer is in the pack. CSV and Excel work (Excel as SpreadsheetML 2003, which opens as a workbook). PDF was removed from the export menu rather than left dead.
5. **A card view for the payments list.** List-items' meta names three containers (`simple-list`, `structured-list`, `card-list`), but only the bordered transaction list is drawn in the snippet or in `canon.css`. So the toolbar's view switch offers **List | Table** (its `drivesConsumer` edge names both), not the snippet's "Table | Cards".
6. **Compact density for the list rows.** List-items' compact values (64 / 10 / 8) exist only inside the snippet's `APOLLO-DEMO density-dial` fence, and rule 3a forbids setting heights or padding on a `.cn-*` part. The toolbar's density control therefore changes **the toolbar itself** (its own dial: 48→40px controls) and hands `data-apollo-density` to the consumer. The rows do not compact. A density dial published outside the fence would close this.
7. **Footer legal links** ("Terms and conditions", etc.) point at `#`. Their destinations are outside this product and no URLs were supplied (Q4/Q6 skipped).
8. **JS-off fallback for the charts and the list.** The engine fills the `<table class="dv-table">` spine at run time from `DATA`, so with JS off the chart tables are empty. The snippets ship hand-written rows; this page's data only exists in script. List, table and KPIs are likewise script-rendered. A server-rendered first paint is outside what a static composed page can do.

## C. Calls I made that the graph or the designer should own

1. **Group count and membership (rule 7b).** Only `metric` carries a grouping edge (the rails' derived self-group). For `chart-stacked-area`, `chart-bar`, `list-items`, `table` and `pagination`, `edges.groupsWith` is `null`: grouping is undecided. I composed four groups, one question each: lead = 4 metrics, evidence = liquidity chart, evidence = payments-out chart, context = payments list with pagination. The one-member carve-out (s245-D7 Q3(a)) is declared only on `chart-bar`. For `chart-stacked-area` and `list-items` it is my reading, not a ruling.
2. **The template scope.** SKILL rule 7a gives the bento grammar wrapped in `class="cn-template-dashboard-bento"` and says that scope "carries the per-theme gutters". Rule 1a says `_validate_example_fence.py` "refuses a built page that wears a template's scope". These two rules collide. I followed 7a's literal grammar, and only the scope's placement rules are used: wall ground, main/sub gutters, group row floors, group band. **No template snippet or template meta was opened** (rule 1a), so the page cannot share a template's body, but the fence validator may still refuse the scope. If it does, the fix belongs to the skill (a non-template home for the bento scope), not to this page.
3. **The chart-tile surface.** Charts paint no surface of their own, and a dashboard tile gets none from the bento grammar. I used the **Stat-card surface as a carrier** (`.cn-stat-card .stat-card` wrapping the chart scope), as s245-D7's ruled group note describes ("a Stat-card carrying Chart-bar's column specimen"). The tension: **s309-D3 moves stat-card pages to Metric**, and Metric has no chart-carrier form. The payments list and pager use the same carrier so their tile reads as one surface. A panel / tile-surface part is the missing piece.
4. **Table width.** Table's `.wrap` reads `--table-w:760px` as its own default. Rule 3a forbids resizing it, so in table view the table sits at 760px inside a full-width tile. A fluid default on the part is the fix.
5. **Chart colour identity under a currency filter.** The engine colours series by position (`data/series/1…5`). Both charts use the same currency order, so the two charts always agree in one view (dv-014). But filtering out USD moves EUR onto USD's colour. There is no per-series colour pin in the spec contract.
6. **The stacked column is engine-rendered.** Chart-bar's own stacked-column specimen stays baked because `_validate_dataviz.py` reads dv-004 off static rects. This page renders it with `dvRender` (rule 18: re-render on every filter), so that gate will not see static rects to measure.
7. **`table`, `pagination`, `drawer`, `section-heading-lockup`, `stat-card`: `when` is null** for each. They were chosen as the only provider of their role's job, by judgement, not by the graph's predicate (s251-D5).
8. **Metric deltas with no prior figure.** When the previous period has no value, the delta slot carries the Metric's own `metric-note` with the `metric-none` glyph rather than a fake "No change". The empty states (no matching accounts, no settled payments) use the snippet's `is-empty` reading.
9. **Status chips.** Settled → `ok`, Processing → `inf`, Awaiting approval → `warn`, Rejected → `err`; Scheduled carries the neutral `tag`. Amounts in rows and in the table stay in ink with a leading minus (rule 6 permits colour on money but does not require it; nothing else is coloured).
10. **Approvals persist per viewer** in `localStorage` (`apollo-treasury-approvals`), so an approved payment stays "Processing" after a reload. This is a demo convenience, not a back end.

## D. Rule notes

- `mustNot`: metric's "a chart making the identical claim in the same view". Total liquidity is a month-end level, and the stacked area is its 12-month composition. These are related claims, not identical, but a reviewer may disagree. Chart-bar's "a Stat-card making the identical claim": the carrier stat-card holds no value or label of its own and makes no claim.
- Rule 11 (sentence case): every heading, label and button is sentence case.
- Rule 17: the slim footer from the shell snippet closes the page.

---

## Behaviour manifest (controls → what each drives → where state persists)

The URL is the store (rule 15): `v` view · `q` query · `f` filters · `r` range · `lv` list view · `d` density · `s` sort · `p` page · `mode`. Defaults are left out of the URL.

| control | drives | persists in | script source |
|---|---|---|---|
| Primary nav (Overview / Liquidity / Payments), masthead and off-canvas sheet | recomposes the wall (which groups and spans), h1, breadcrumb current item, `document.title`, `aria-current` | URL `v` (pushState; Back/Forward restore) | page wiring (authored) |
| Breadcrumb "Home" / "Corporate banking" | goes to Overview | URL `v` | page wiring |
| Menu button (narrow container) | opens the off-canvas sheet; Esc, scrim and close all close it; focus returns | — | App-shell-top-nav, **verbatim** |
| Masthead search button | moves focus to the toolbar search | — | page wiring |
| Search field (+ clear) | payments list/table, all 4 KPIs, payments-out chart, result count | URL `q` | Search-field **verbatim** + driver |
| Add filter: Entity / Currency / Status / Rail (OR within a facet, AND across facets) | **Entity and Currency:** every panel, including the liquidity chart and the Total liquidity KPI. **Status and Rail:** payments list/table, the payments KPIs and the payments-out chart (balances have no status or rail) | URL `f` | Dropdown **verbatim** + driver (extended) |
| Applied-filter chips (dismiss, +N more, show fewer) | same as the filter they remove | URL `f` | Tags **verbatim** + driver |
| Clear all (toolbar and empty state) | resets query and filters | URL | driver |
| Date range (7 / 30 / 90 days) | payments list/table, payments KPIs and their comparison period, payments-out chart | URL `r` | Dropdown **verbatim** + driver |
| Sort: Newest / Largest | list/table order (page resets to 1) | URL `s` | Segmented-control **verbatim** + driver (extended: new control) |
| View: List / Table | swaps List-items ↔ Table for the same page of rows | URL `lv` | Segmented-control **verbatim** + driver |
| Density: Comfortable / Compact | the toolbar's own control height; `data-apollo-density` on the consumer (see B6) | URL `d` | Segmented-control **verbatim** + driver |
| Export: CSV / Excel | downloads the current filtered and sorted set (all pages) | — | Dropdown **verbatim** + page wiring |
| Pagination (prev, numbers, next; Space activates; arrows/Home/End move focus) | list/table page | URL `p` | Pagination, **extended** (delegated; page set rendered) |
| Payment row (List view) | opens the Drawer with that payment's Summary; Esc, scrim and Close all close it; focus returns to the row | — | Drawer, **extended** |
| Row keyboard: ArrowUp/Down, Home/End | roving focus through rows | — | List-items, **extended** (delegated) |
| Drawer primary: "Approve payment" (awaiting-approval rows) | sets the status to Processing, then re-asks through the toolbar so KPIs, charts, list and count all update | `localStorage` approvals | page wiring |
| Drawer primary: "Download payment advice" (all other rows) | downloads a text advice for the payment | — | page wiring |
| Chart: Copy data (CSV) · View as table | copies / discloses the engine-written table | — | dv-behaviour, **verbatim** |
| Chart legend: swatch toggles, name isolates, Reset | dims or isolates series | — (rebuilt when the series set changes) | dv-legend, **verbatim** |
| Chart marks (hover/focus) | value popover | — | dv-behaviour, **verbatim** |
| Light/dark | — (see B1) | URL `mode` / `localStorage` | page wiring |

Script addresses carried (`#behaviour-manifest` in the page): `knowledge/snippets/App-shell-top-nav.reference.html#script` (verbatim) · `knowledge/snippets/Filter-toolbar-bar.reference.html#script` (atoms verbatim, driver extended: expect `NOTE:AUTHORED-JS`) · `knowledge/canon/dv-render.js` + partials dv-behaviour, dv-legend, dv-render, dv-render-stacked-area, dv-render-bar (verbatim AUTO-BEHAVIOUR blocks) · Pagination, Drawer and List-items scripts extended · Metric, Summary, Table, Section-heading-lockup and Stat-card carry no script (`fallback` identical / passive).

**Drive result:** none. Not driven: no browser in this session.
**Gate verdict:** none. Gates not run (session condition).
