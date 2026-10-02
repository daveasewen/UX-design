# Used / missing: corporate international banking dashboard

**Lane:** on-canon. Source: `skills/generate-from-canon/SKILL.md` (via `/generate-from-canon` → `.github/prompts/generate-from-canon.prompt.md`), after `skills/grill-me/SKILL.md`.
**Brief:** `out/brief.md`. Q1 was answered **Console**, and that answer shaped the build: `data-apollo-theme="console"`, rounded corners on controls and the bento container. Q2–Q6 were skipped. Their fallbacks shaped the build as follows: both modes; comfortable density at laptop to wide-desktop width; the HSBC masterbrand; invented, seeded data; canon's own a11y floor. The bento check was skipped, which counts as a yes.
**Output:** `out/dashboard.html`. It is one file with no sibling files. It links `../knowledge/canon/canon.css`, `../knowledge/canon/type.css` and `../knowledge/assets/logos/masterbrand-{light,dark}-colour.svg`, so it must stay inside this pack at `out/` for those paths to resolve.

---

## Seed commands run (step 1)

```
python3 knowledge/_compose_slice.py --help
python3 knowledge/_compose_slice.py "Financial dashboard for corporate international banking: cash positions across accounts and currencies, payments and their statuses, FX exposure trends, with working filters and navigation" --out <scratch>/seed.json --explain
python3 knowledge/_compose_slice.py "How has the group's total cash balance moved over the last 12 months, per region" --intent change-over-time --shape "time-series × 1–5-series" --out <scratch>/seed-chart-trend.json --explain
python3 knowledge/_compose_slice.py "How is today's cash split across currencies" --intent composition --shape "parts-of-whole" --out <scratch>/seed-chart-mix.json --explain
python3 knowledge/_compose_slice.py --ask "which components answer comparison?"
```
The seed left `role:chart` unresolved because the request named no intent. Typed runs resolved it with `change-over-time` and `composition`. The unresolved `role:input` co-providers were settled by Filter-toolbar-bar, which composes Search-field, Dropdown and Tags.

## Decision table (step 2)

| question | role | component chosen | the `when` that is true for this data | rulings that bind it (from `governs`) |
|---|---|---|---|---|
| Frame the app | page-frame | **app-shell-top-nav**, inline | `primaryNavigation = present AND platform = app`: the default frame whatever the count | s313-D22, s313-D24, s272-D72, s230-D2 |
| Move between destinations | wayfinding | **navigations**, the masthead row as the shell composes it | `shape = destination-set × links AND scope = global`. There are 3 destinations and none has children, so no flyout or mega menu (s313-D23). Breadcrumbs are out: depth is 1 and they need ≥ 2 | s313-D22, s313-D23, s314-D1, s262-D3, s261-D7, s230-D2, s305-D60 |
| Name the page | page-title | **page-header-lockup**, "simple" plus meta line | The seed's winner, section-heading-lockup, gates on `h1 = absent` (s272-D60), which is false for the page title, so the page `<h1>` goes to page-header-lockup | s272-D60; mustNot: never both naming one region (honoured: `h1` in the page header, `h2` per group) |
| Head each group | page-title (section) | **section-heading-lockup**: arrangement A (label); C (eyebrow + heading + count badge + two buttons) for payments | `level = section AND scope = one board/panel AND h1 = absent` | s313-D29 (band inside the group is the default), s272-D60 |
| Drive the screen (search, facets, period, export) | input | **filter-toolbar-bar**, variant "dashboard" | `records >= 2 AND needs in (filter, sort)`. One row of controls drives the record list *and the panels beside it*, placed directly above what it drives | s258-D1, s258-D2 (in its header); drivesConsumer contract |
| (a) Where does our cash stand? | headline-metric | **metric** ×4: total cash · payments sent · failed or returned (up-is-bad) · net FX exposure (up-is-bad) | `shape = one-measure × value-and-delta AND delta != none`. runway-bar's `when` (committed-vs-balance split) is false for these four | s309-D5, s310-D1, s310-D2, s309-D6, s314-D18 (four in a row, no orphan) |
| (b) How have balances moved, by currency? | chart (change-over-time) | **chart-line**, multiline | `answers = change-over-time AND series 1–5 AND one continuous time axis AND axes present AND span.cols ≥ 6 (3 of 6 here) AND units same (USD eq)`. It beats stacked-area because the claim is each currency's path, not a shared cumulative band | s305-D21, s249-D4, s277-D3, s277-D1 |
| (c) What is the currency mix? | chart (composition) | **chart-donut**, spider + legend | `answers = composition AND parts sum to a whole AND total printed in the centre AND span.cols ≤ 6`. It beats pie because the centre total is wanted | s305-D9, s305-D59, s313-D31, s313-D32, s277-D2 |
| (d) Do balances cover what is scheduled? | headline-metric | **runway-bar** (the seed's winner for the role) | `answers = one-number AND shape = one-measure × committed-vs-balance-split AND verdict != none`: a verdict with a date | (none returned for it); mustNot honoured: no Chart-bullet or bare Progress bar of the same figures |
| (e) What is driving that outflow? | record-list | **list-items**, structured transaction rows | `records >= 2 AND same kind, read across the row AND surface none AND needs none` | s274-D6, s274-D1, s274-D2, s274-D5, s313-D27 |
| (f) Which payments need action? | record-list | **data-grid** | `records >= 2 AND needs in (select, edit)`: bulk approval and edit-in-place of the reference. It does not yield to list-items, because needs go beyond sort and filter | s313-D27, s274-D6 (yieldsTo list-items not triggered) |
| Inspect one payment | overlay | **drawer**, "detail", holding **summary** and **status-indicator** | Adjacent detail; the page stays glanceable | s272-D52, s272-D53, s313-D20, ds-032; mustNot: one modal surface at a time (honoured) |
| End the page | (footer) | **footer**, default | `platform = app`: the body-level sibling after main, never inside the wall | s305-D60, s261-D3, s261-D8, s272-D58, s263-D7 |

Bento grammar (rule 7a). The page uses the scope `.cn-template-dashboard-bento`, then `.tpl-page`, then `.c-bento.tpl-wall[data-bento-role=dashboard]`, with groups as nested `.c-bento.tpl-group`. Console defaults come from `_bento_edit_rails.json`: mainSpacing 40, subSpacing 4, keylines off, bentoBg transparent. The page sets none of these itself. Spans: lead 6; trend 3 + mix 3; runway 3 + upcoming 3; payments 6. Role words: lead, evidence, context.

Tokens: the page binds none directly. Its single `<style>` rule is placement only: `.tpl-wall .tpl-group[hidden]{display:none}`. Every visual value arrives through the component scopes in `canon.css` and the composites in `type.css`.

## Behaviour manifest: what each control drives, and where its state persists

The same list is in the page as `#behaviour-manifest`.

| control | drives | persists in |
|---|---|---|
| Masthead nav (Overview · Liquidity · Payments), and the off-canvas sheet at narrow widths | Which groups are on the wall; the page title, lede and document title; re-renders the charts at their new width | `?view=` (pushState; Back and Forward work) |
| Masthead search button | Focuses and scrolls to the toolbar search | — |
| Toolbar search | Narrows accounts (by entity, account or currency words) and payments (by beneficiary, reference or id). Moves **all four KPIs, both charts, the runway, the upcoming list, the grid, the page meta and the count** | `?q=` |
| Toolbar "Add filter" (region, entity, currency) and its chips | Same reach as search: OR within a facet, AND across facets. A chip × removes the filter; "+N more" expands | `?f=region:emea,currency:EUR` |
| Toolbar period (3 / 6 / 12 months) | KPI windows and deltas, the spark length, the line chart's months, the donut's averaging window, the grid's date window | `?range=` |
| Toolbar export | Downloads a CSV of payments or of balances, for what is in view | — |
| Toolbar "Clear all" and the empty-state "Clear all filters" | Resets search and facets | URL cleared |
| Line legend (swatch = show/dim, name = isolate, Reset) | Dims or isolates currency lines | not persisted |
| Donut Value/Percent switch and legend | Changes the segment and centre readout, dims or isolates slices | not persisted |
| Chart "Copy data (CSV)" and "View as table" | Copies the chart's table and opens the table popover | — |
| Grid column sort (Value date, Beneficiary, Debit entity, Status, Amount; Reference is sort-disabled by design) | Row order | `?sort=key:dir` |
| Grid column filters and grid search chips | Narrow the grid only (status is filtered here, not globally) | `?gf=` (JSON) |
| Grid density (Comfortable / Compact) | Row density | `?density=` |
| Grid rows per page and pager | Paging | `?pp=`, `?pg=` |
| Grid row checkboxes and select-all | Selection; enables "Approve selected (n)" and "Clear selection" | not persisted |
| "Approve selected" | Pending approval → Scheduled for selected pending rows. Re-renders the badge, runway, upcoming list and grid; announces the result | in memory only |
| Grid beneficiary link (click, or Enter on the cell) and upcoming list rows | Opens the drawer for that payment | `?pay=` (reopens on reload) |
| Drawer "Approve payment" (pending only), "Close", ×, scrim, Escape | Approves and closes, or closes; focus returns to the opener | `?pay=` removed |
| Reference cell (double-click, Enter or F2) | Edits the reference in place | in memory only |
| Mode | Light or dark | `?mode=` plus `localStorage`; default follows `prefers-color-scheme` |

Script sources:
- Carried and extended (NOTE:AUTHORED-JS): App-shell-top-nav, Navigations, Filter-toolbar-bar, Data-grid, Drawer and List-items.
- Verbatim: Footer part (a), and the six `AUTO-BEHAVIOUR` engine blocks (`dv-behaviour`, `dv-render`, `dv-render-line`, `dv-render-donut`, `dv-legend`, `dv-donut-sweep`). They were copied byte for byte from `Chart-donut.reference.html` and `Chart-line.reference.html`, in the donut snippet's load order (legend and sweep after the first `dvRender` call).

## Gate verdict (step 7) and drive (step 8), as they actually stand

- **Gates: not run.** The session conditions forbid running any gate or validator. So `python3 knowledge/gen_provenance_receipt.py --mint`, `knowledge/_validate_receipt.py`, `knowledge/_validate_screen.py` and `python3 ci-template/run-gates.py` were not run. No receipt was minted. CLAUDE.md rule 3, "Check before you show", is therefore **unmet**, and this page is an unchecked draft.
- **not driven: no browser in this session.** No console was read and no control was exercised. Every row in the behaviour manifest above is wiring as written, not a tested result. Geometry was not measured.
- The only check run was my own lexical bracket and string balance scan of the app script (Python, in scratch). It passed. That is not a parse, a gate or a drive.

---

## Gaps

1. **Gates and drive not done** (above). Until someone with a browser runs them, the claims on this page are unverified.
2. **Template-scope tension in the skill itself.** Rule 7a says to wear `.cn-template-dashboard-bento` as the bento scope. Rule 1a says `_validate_example_fence.py` "refuses a built page that wears a template's scope". I followed 7a, the more specific instruction, so the fence gate may refuse this page. I did not open the template meta's `$bentoGrammar`, because 1a forbids opening a template. The grammar was taken from 7a's skeleton, `canon.css` and the rails file.
3. **No panel surface for non-metric modules.** In the wall, the charts, runway, list and grid have no tile ground of their own; they sit on `--wall-ground`. The template uses a stat-card as its panel. No "panel" part exists for a chart or grid tile, and I did not invent one.
4. **The shell has no `is-full` form.** Rule 3a mentions it, but `app-shell-top-nav` does not carry it (only doormat, multi-column and side-nav do). The shell keeps its 560px min-height plus its border and radius frame.
5. **The shell's slim legal bar (`.sh-foot`) is replaced by the Footer component (`.cn-footer .ft`).** The Footer `when` (`platform = app`) is true and its meta calls it the app footer. A reviewer should confirm that the shell's own footer slot should take it.
6. **No account or profile menu.** The shell's profile action has nothing composed to open, so it is omitted (rule 14: a CTA that opens nothing is a gap). The search action remains.
7. **No light/dark switch component** was found in the index. Mode follows `prefers-color-scheme`, `?mode=` pins it, and there is no on-screen control.
8. **Filter toolbar parts omitted.** "Custom range…" hands off to date-range-picker (`delegatesTo`), which was not composed. The view switch is omitted because there is no cards view of the payments. The density switch is omitted because the grid carries its own.
9. **Grouping edges.** Only Metric declares `groupsWith` (a self-edge). Chart-line, chart-donut, runway-bar, list-items and data-grid each sit in a one-member group with no declared edge, so each is undecided rather than ruled (s245-D7 Q3(a) makes one-member groups legal only as declared carve-outs). The group count is also a fallback, because discovery was skipped (rule 7b).
10. **runway-bar is PROPOSED, not gated or ruled**, and its provenance is a test fixture: "whether it should exist at all is Dave's first decision". It has no empty state, so its group is hidden when no account matches. `.rwy` caps itself at 480px, so a wide context tile may show space to its right.
11. **Metric is PROPOSED** (s182-D2 floated it and never ruled it). It has no script, so with JS off the tiles render empty.
12. **JS-off fallback versus rule 13.** DATA is the single source, so the chart `<table>` spines ship with headers only, and the metrics, runway, list and grid ship empty. dv-005 expects an authored table. The rules conflict here, and neither was bent.
13. **Stale dv-legend cache after a re-render.** This is the core request noted in Chart-donut's own call. I worked around it by rebuilding the legend rows and dropping the host's cached record (`__dv`), so a filter change resets the legend to show all. The donut's radial sweep runs once at load, not on re-render (by design).
14. **The chart engine forces a zero baseline on lines.** This is the core request noted in `dv-render-line.js`. The `unit` was left out of both chart specs because tick labels with "USD m" would clip at the 46px plot margin, so the unit lives in the headings and captions.
15. **Line markers cycle three shapes.** With five currencies, D and E reuse the circle and square shapes; the letters still differ.
16. **No toast after approval.** Feedback is the status change, the badge, the KPIs and the grid's polite live region. Toast exists but was not composed.
17. **Status-indicator "Cancelled"** uses the `neu` dot, which carries the known rag/neutral-tint token gap.
18. **`.ftb-outer` is sticky but cannot stick** inside the shell, because `.sh` has `overflow:hidden`.
19. **Showroom pages were not opened** to confirm the parts (step 3). That needs eyes this session does not have.
20. **The brief is at `out/brief.md`**, not `briefs/…-grill.md`, per the session's output rule.
