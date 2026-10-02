# Brief and decisions — corporate international banking dashboard

**Lane: on-canon.** `/generate-from-canon` resolved to `.github/prompts/generate-from-canon.prompt.md`, which hands over to `skills/generate-from-canon/SKILL.md` (`ADS-generate-from-canon`). The grill was `skills/grill-me/SKILL.md` (`ADS-grill-me`). No freestyle skill and no non-Apollo skill produced any design output.

Request, verbatim: *"build me a financial dashboard for corporate international banking. Please make the all the interactive elements work such as filtering and navigation."*

---

## 1 · Grill answers (also saved as `briefs/2026-10-02-corporate-banking-dashboard-grill.md`)

`briefs/` did not exist, so the grill ran. The designer called a full skip at question 1. Every answer is therefore *skipped / defaulted*. Each default below was stated in my first reply, before anything was built.

| # | question | answer | the default it causes |
|---|---|---|---|
| 1 | Theme | ***skipped / defaulted*** | **Mono**: `data-apollo-theme="mono"` on `<html>`. Every radius token resolves to 0, so **every corner is square by design**. Announced before the build. |
| 2 | Light, dark or both | ***skipped / defaulted*** | Fallback **both**, because every component ships both. The page carries a "Dark mode" toggle (`aria-pressed`) and opens in the OS preference. The choice persists in `localStorage`. |
| 3 | Density and width | ***skipped / defaulted*** | Fallback: **comfortable** (each component's own default density). Width runs **laptop to wide desktop**. It collapses through the shell's container bands (899 / 599) and the bento bands (1100 / 820 / 520) down to phone. |
| 4 | Brand assets | ***skipped / defaulted*** | The masthead carries the **HSBC masterbrand**: `masterbrand-light-colour.svg` on light chrome, `masterbrand-dark-colour.svg` on dark (s230-D2, rule 8a). Product name: none given, so the page uses the group name from DATA. No photography. |
| 5 | Real data or placeholder | ***skipped / defaulted*** | Fallback: **placeholder, invented and deep** (rule 13 / s258-D2). One fictional group (Arden Maritime Group) with 6 legal entities in 6 currencies (GBP, EUR, USD, HKD, SGD, JPY) and 16 accounts, each with 12 month-end balances. 871 payments over 24 months: 13 rails, 4 statuses (Completed, Pending approval, Processing, Rejected), in and out. FX to USD is fixed 2 Oct 2026 06:00 UTC. The 24 months exist so that every date range has a previous period to compare against. |
| 6 | Fixed and off-limits | ***skipped / defaulted*** | Fallback: no commitment beyond the system's own contract (never invent; WCAG 2.2 AA as the components carry it). |
| — | **"dashboard bento — is that right?"** | ***skipped = yes*** | The overview is laid out on canon's bento grammar (rule 7a). |
| — | Discovery | — | Discovery ended by the designer after 0 questions (full skip). |

The brief shaped the build in these ways: Q1 set the theme attribute and square corners. Q2 put the light/dark switch on the page. Q5 set the depth of `DATA`. The bento answer set the overview layout.

---

## 2 · Seed commands run (procedure step 1)

```
python3 knowledge/_compose_slice.py "Financial dashboard for corporate international banking: account balances and liquidity across currencies and entities, cash flow over time, payments list with filtering, sorting and paging, app shell with navigation, masthead and footer." --out out/seed.json --explain
python3 knowledge/_compose_slice.py "Filter the dashboard by legal entity, currency and payment status from a filter bar" --roles input --out out/seed-filters.json --explain
python3 knowledge/_compose_slice.py "List of cross-border payments to search, filter, sort and page; one row per payment with beneficiary, amount, currency, status, date" --roles record-list --out out/seed-payments.json --explain
python3 knowledge/_compose_slice.py --ask "what did Dave rule about component:template-dashboard-bento?" --budget 1000   # REFUSED: 3464 tokens > 1000 (not raised, not worked around)
```

The first seed resolved roles `record-list, page-frame, wayfinding, input, headline-metric, chart, page-title` with intent `change-over-time`. It left 16 rows `unresolved`, which I took as the work list. The two typed runs resolved the filter bar (`filter-toolbar-bar`, which only the second run named) and confirmed `list-items` over `data-grid` for the record list.

---

## 3 · Decision table (procedure step 2)

Questions the screen must answer → role → chosen part → the `when` that is true for this data → the rulings from `governs` that bind it.

| # | question the user came with | role | part chosen (snippet) | `when` true for this data | rulings that bind it |
|---|---|---|---|---|---|
| F1 | How do I move between the app's areas? | page-frame | **app-shell-top-nav**, inline form (`App-shell-top-nav.reference.html`) | `primaryNavigation = present AND platform = app` (the default frame, whatever the count) | s313-D22, s313-D21 (the nav family is frame, not a tile group), s230-D2 (masterbrand) |
| F2 | Where am I? | wayfinding | the shell's own masthead nav (Navigations geometry) and breadcrumb strip (Breadcrumbs atom), as the shell carries them | navigations: `scope = global`; breadcrumbs `depth >= 2` holds (Corporate banking / view) | s313-D22, s272-D72 |
| F3 | What page is this, and what can I do here? | page-title | **page-header-lockup**, arrangement 1: eyebrow, title, lede, actions (`Page-header-lockup.reference.html`) | provider #1 of page-title. The meta authors no `when` (`unresolved`). The tab foot is not used (no third level). | s313-D28, s313-D24 |
| Q0 | Narrow everything to the entities, currencies, statuses and rails I care about, over a period | (lock-up, drives consumers) | **filter-toolbar-bar** (`Filter-toolbar-bar.reference.html`) with its own search-field, dropdown (Add filter, Date range), segmented control (`seg l`, sort) and tags (chips) | `records >= 2 AND needs in (filter, sort)`. It sits directly above the thing it drives. | s263-D4 (the `data-apollo-filter-*` contract), s263-D5, s272-D67, s261-D6 (larger segmented control) |
| Q1 | How did the period go? | headline-metric | **metric** ×4, default variant with the trend slot (`Metric.reference.html`) | `shape = one-measure × value-and-delta AND delta != none`. The trend slot is filled because a series exists for each. Count rule: min 2 per group (self-edge). | s308-D42, s310-D1 (thin direction arrow), s314-D18 (no orphan in a KPI row) |
| Q2 | How has cash moved over time? | chart | **chart-line**, multi-series canvas (`Chart-line.reference.html`) | `answers = change-over-time AND 2 series on one time axis AND axes present AND units = same (USD m) AND span.cols ≥ 6` (3 of the wall's 6 = 6 of 12) | s305-D21, s249-D4 (the engine draws it), s116-D2 (table spine) |
| Q3 | Where is the cash held? | status-surface | **summary** ×2 (`Summary.reference.html`), by currency and by entity | `shape = rows × name-value-pairs AND rows >= 2 AND span.cols >= 6` (3 of 6 = 6 of 12) | s305-D60, s314-D10 |
| Q4 | What has moved, and which payment is that? | record-list | **list-items**, structured rows (`List-items.reference.html`) | `records >= 2 AND same kind, read across each row AND needs in (none, sort, filter)`. No bulk select or edit, so **data-grid's `when` is false**. | s274-D6, s313-D27 |
| Q4b | More than one screenful | wayfinding | **pagination**, basic (`Pagination.reference.html`) | no `when` authored. It is a `hasPart` of the record list per the seed. | s313-D15 |
| Q5 | Tell me everything about this one payment / account / me | overlay | **drawer** (`Drawer.reference.html`) holding a **summary** | consumed by app-shell-top-nav (`edges.consumes`). The summary holds ≥ 2 name-value rows. | s272-D52, s272-D53 |
| G | Which group is which? | (lock-up) | **section-heading-lockup**: arrangement A (label) and B (label + arrow link), placement `band` | `level = section AND h1 = absent` | s313-D29 (band is the default) |
| F4 | The page ends properly | (footer) | **footer**, slim form, as App-shell-top-nav carries it verbatim | `platform = app` | s261-D3, s305-D60 |

**Rejected, with the graph's reason:**
- **chart-stacked-area.** Its `when` was true (balances by currency share one total over time). But chart-line and stacked-area both carry `mustNotNeighbour` dv-014 ("a second chart re-using these series colours for different data in the same journey"), so one chart stays. The composition question went to Summary instead.
- **chart-combo.** False: the units are the same.
- **Chart-candlestick.** False: there is no OHLC data.
- **chart-sparkline as a panel.** It is a complement of the Metric, not a panel. It lives in the Metric's trend slot.
- **runway-bar and Chart-bullet.** False: there is no committed-vs-balance verdict and no target band.
- **data-grid.** False: needs ∉ {select, edit}.
- **app-shell-side-nav.** It is chosen by a workbench job and yields to top-nav.
- **Template-dashboard-bento / Template-dashboard.** Fenced examples (rule 1a). Neither the snippet nor the meta was opened.

**Bento composition (rule 7a / 7b).** The scope is `cn-template-dashboard-bento`, with `.tpl-page` › `.c-bento.tpl-wall[data-bento-role=dashboard]` on a 6-column wall. The rails' Mono dashboard defaults ship through the scope, and I set none of them: main 40, sub 4, keylines off, page ground grey, bento ground transparent.

| group (role word) | wall span | members | one question | grouping evidence |
|---|---|---|---|---|
| `tpl-group-lead` | 6 | header band + 4 × Metric | "How did the period go?" | metric `count` min 2 per group (self-edge, s245-D7) |
| `tpl-group-evidence` | 3 | header band + 1 × Chart-line | "How has cash moved?" | chart-line `edges.groupsWith` is **null**. One-member group: Gap G-7 |
| `tpl-group-context` | 3 | header band + 2 × Summary | "Where is the cash held?" | summary `groupsWith` is **null**. Gap G-7 |
| `tpl-group-evidence` | 6 | header band (with "View all payments") + List-items | "What moved most recently?" | list-items `groupsWith` is **null**. Gap G-7 |

Rows are 6 | 3+3 | 6, with no orphan at any band. The lead grid is pinned 4 across by the scope's own rule 10a, so the KPI row never orphans (s314-D18).

**Tokens, by intent.** The page declares no colour, size or spacing of its own. Every value paints from the scopes in `canon.css`. My `<style>` has two rules: which view is showing, and a `[hidden]` restore (Gap G-4).

**Type.** Every text element carries a composite from `type.css`, copied from the snippets: `.t-cm-heading`, `.t-cm-section-label`, `.t-cm-caption`, `.t-cm-figure-4/6`, `.t-cm-legal`, `.t-cm-button`, `.t-cm-label`, `.t-cm-chart-label`, `.t-ed-body`, `.t-ed-body-small`, `.t-ed-heading-4`.

**Colour is meaning (rule 6).** Amounts in the lists stay in default ink, with − / + signs and the currency code. The Metric delta colours its glyph only. Status chips carry their word (label + dot).

---

## 4 · Behaviour manifest — every control, what it drives, where its state lives

| control | drives | state persists in |
|---|---|---|
| Masthead nav: Overview / Accounts / Payments (and the same links in the off-canvas sheet under 900px) | switches the view panel, `aria-current`, breadcrumb, `<h1>`, lede, `document.title`, the noun in the toolbar count. Focus moves to the `<h1>`. | URL `?view=` (pushState; Back/Forward restore it via `popstate`) |
| Menu button (under 900px container) | opens the off-canvas nav sheet. Background goes inert. Esc / scrim / close button close it, and focus returns to the trigger. | — |
| Breadcrumb "Corporate banking" | back to Overview | URL |
| Masthead search button | goes to Payments (from Overview) and focuses the search field | URL |
| Masthead profile button | opens the drawer with the profile summary. Its primary action switches light/dark. | — |
| "Dark mode" toggle (page header, `aria-pressed`) | `data-theme` on `<html>`. Every scope repaints and the masterbrand swaps light/dark mark. | `localStorage` `apollo-dashboard-mode` (first visit: OS preference) |
| "Export CSV" (page header, primary) | downloads the current view's filtered, sorted rows (payments, or accounts on Accounts) as CSV | — |
| Search field (+ its clear ×) | filters payments (counterparty, reference, ID, account, entity, rail, currency) and accounts. Re-drives all 4 metrics, the chart, both summaries, the lists, the count and the pagers. | URL `q=` |
| Add filter (grouped: Entity, Currency, Status, Rail, Direction) | adds a chip. Values within one facet are ORed; facets are ANDed. Re-drives everything above. (Status, rail and direction describe payments, so they leave the accounts list alone.) | URL `f=facet:value,…` |
| Chip × / "+N more" / Clear all | removes one filter, expands the overflow chips, or clears everything | URL |
| Date range (30 days / 90 days / 6 months / 12 months) | the period for metrics 2–4 and their comparison period, the chart's buckets (5 / 13 / 6 / 12), the lists, the count | URL `range=` |
| Sort by Date / Amount (segmented) | sorts the recent list, the payments list (date desc / USD-equivalent desc) and the accounts list (entity+name / balance desc) | URL `sort=` |
| Payment row (overview and Payments view; Enter/click; ↑↓ Home End rove) | opens the drawer with that payment's Summary. "Download advice" downloads a text advice. Close / Esc / scrim return focus to the row. | — |
| Account row (Accounts view) | opens the drawer with the account Summary. "Show its payments" searches that account number and goes to Payments. | URL (via the search it sets) |
| "View all payments" (arrow link in the Recent payments band) | goes to the Payments view | URL |
| Pagination (Payments 10 per page, Accounts 8 per page; prev/next, numbers, ←→ Home End, Space) | pages the list. Prev/next disable at the bounds. Focus stays on the control, or moves to its opposite when it disables itself. | URL `pp=` / `ap=` |
| Chart: legend swatch (show/hide), legend name (isolate), Reset | dims, isolates or restores the inflow and outflow lines (dv-legend, carried verbatim) | — |
| Chart: Copy data (CSV), View as table | copies the chart's table / opens the table spine (dv-behaviour, carried verbatim) | — |
| Skip link | jumps to `<main>` | — |
| Footer legal links | **dead (`href="#"`)**: Gap G-9 | — |

Script provenance: the page's `#behaviour-manifest` block names each script source and says whether it was carried verbatim or extended. The chart engine (dv-behaviour, dv-legend, dv-render, dv-render-line) is byte-identical to Chart-line's AUTO-BEHAVIOUR blocks. The filter-toolbar, shell, drawer, pagination and list scripts were **extended**, so `NOTE:AUTHORED-JS` is expected, per s258-D1.

---

## 5 · Gate verdict and drive result

**None. The page was not gated and not driven.** The session conditions forbade running any gate, validator, browser or node check during the build. The provenance receipt was **not minted**. The exact commands still owed are in `GAPS.md` § "Not proven".
