# Gaps — corporate international banking dashboard (`out/dashboard.html`)

Lane: **on-canon** (`ADS-generate-from-canon`). Each item says what the system did not supply and what the page did instead. Every workaround is declared here, never silently improvised.

## Not proven

- **not driven: no browser in this session.** The page was never loaded, so no console was read (rule 16) and no geometry was measured (step 8). Every control listed in `brief.md` §4 is wired by reading the code, not by driving it. The table there says what each control should change.
- **Not gated.** The session forbade running gates or validators, so none ran. Owed, in this order:
  ```
  python3 knowledge/gen_provenance_receipt.py --mint out/dashboard.html
  python3 knowledge/_validate_receipt.py out/dashboard.html
  python3 knowledge/_validate_screen.py out/dashboard.html
  python3 ci-template/run-gates.py          # + --browser for the playwright three
  ```
  The **receipt was not minted**, so `_validate_receipt.py` will stop at `FAIL:NO-RECEIPT` until it is. No baseline gate run was taken on the fresh pack either, so a later red cannot yet be split into "mine" and "pre-existing".
- **The JS was not even syntax-checked.** The only checker available is node-based, which the session forbade. It was reviewed by reading only.

## Contradictions in the skill and pack (reported, not resolved by me)

- **G-1 · The template scope is both prescribed and refused.** Rule 7a prescribes `<div class="cn-template-dashboard-bento">` as the scope that carries the per-theme gutters. Rule 1a says `knowledge/_validate_example_fence.py` "refuses a built page that wears a template's scope". I followed rule 7a's explicit grammar. If the fence gate reds on the scope, the skill needs one answer.
- **G-2 · The seed named a template.** Rule 1a says "the compose door never offers one (the seed cannot name it)". The first seed returned `component:template-dashboard-bento` (by text match, listed in `unresolved` with no role). I did not open its snippet or its meta.
- **G-3 · Rule 7a sends the builder into the fenced meta.** Rule 7a says the bento grammar is "described in `knowledge/components/template-dashboard-bento.meta.json` under `$bentoGrammar`", while rule 1a says a build opens neither the template's snippet nor its meta. I read the grammar from `canon.css` (the `.cn-template-dashboard-bento` block and `AUTO-BENTO`) and from the skill's own code block instead. Anything that lives only in `$bentoGrammar` was not seen.

## Snippet defects found while copying (fixed nothing at the part)

- **G-4 · `[hidden]` loses to the component's own display rules.** In `cn-filter-toolbar-bar`, `.ftb-msg{display:flex}` and `.tag{display:inline-flex}` beat the UA `[hidden]{display:none}`. As a result the empty-results message, and the chips past the third that the toolbar hides behind "+N more", would paint while telling AT they are gone. This is the #218 W3 F1 class that canon guards elsewhere (`.cn-navigations … [hidden]{display:none}`). The page restores `[hidden]` with one placement rule: `#ftbA [hidden], #consumer [hidden]{display:none;}`. It contains no hex, no size and no `.c-*`/`.cn-*` redefinition, but it is a page-side patch and the fix belongs in the part (s314-D28).
- **G-5 · Nested scopes collide on the chart.** The `cn-template-dashboard-bento` scope carries Chart-bar's `figure.dv` / `.dv-svg` / `.dv-chart-area` rules (fixed 580×260 until `.dv-fit-on`), which also reach the `cn-chart-line` figure nested inside it. They sit later in canon.css at equal specificity, so they win. With JS on, `.dv-fit-on` releases the width either way. With JS off, the line chart takes Chart-bar's fixed box. Not measured.
- **G-6 · No panel surface for a chart or a summary in a bento tile.** Chart-line's figure and Summary's `dl` paint no surface, and a bento tile paints none either. The dashboard-bento scope's own module recipe (`.stat-card` on the tile, rules 7–9 of that scope) is the only available panel surface, so the chart, summaries and lists sit in `c-bento__tile stat-card`. Metric keeps its own 1px frame, because the scope's frame-yield rule names only `.kpi-tile` / `.stat-card` as direct grid children, so the four metrics may show a double seam against the 4px gutter. Not measured.

## Graph gaps (undecided in the KG — not guessed)

- **G-7 · `edges.groupsWith` is null for chart-line, summary and list-items.** Grouping is "undecided … a Gap, not a guess" (rule 7b). Only Metric has a group rule (count ≥ 2 per group, self-edge). The page puts each of the other three questions in its own group: one Chart-line; two Summaries (same kind); one List-items. These are by analogy with the declared one-member carve-out (s245-D7 Q3(a), declared for chart-bar only). Membership and group count are the designer's product decision, and the brief skipped it.
- **G-8 · "span.cols" in the `when` clauses has no declared grid.** Chart-line and Summary both need `span.cols ≥ 6`. The page reads that on the 12-column board the Metric meta describes, where 3 of the wall's 6 columns = 6 of 12. That reading is what made the chart and summary groups 3 + 3 rather than 4 + 2. If `span.cols` means the 6-column wall, both `when`s are false at this width and the composition needs another answer.
- **G-11 · Ruling s313-D41 ("a bento wall keeps the four kinds of tile it accepts") was not readable.** The seed's `ruled` text stops before naming the four kinds. The ASK door refused at 3,464 tokens over a 1,000 budget (not raised, not worked around), and the template meta is fenced. Whether a List-items tile is one of the four accepted kinds is unknown.
- **G-12 · No `when` is authored for page-header-lockup, pagination, drawer, section-heading-lockup, segmented-control, tags, search-field or footer's role** (`unresolved` in the seed). They were chosen as the role's provider #1 or as a `hasPart` / `consumes` of a chosen part, not by a `when` test.
- **G-13 · Up-is-bad is not set on any metric.** s310-D2 / s309-D5 introduced an up-is-bad setting. "Payments sent" is neutral in direction (more payments is neither good nor bad), so all four tiles claim direction only, as the Metric snippet's own note describes. Whether the treasury reader wants judgement colour on any of them is the designer's call.

## Things the system does not have (so the page does not have them)

- **G-9 · Footer legal links go nowhere.** The shell's slim footer carries Terms, Privacy, Accessibility statement and Cookie settings with `href="#"`. The pack holds no legal content to link to. The footer is required (rule 17); its links are dead until real URLs exist.
- **G-10 · No "new payment" flow.** A corporate dashboard's natural primary action is "Make a payment". Building it would mean composing a whole create flow (amount-input, account-selector, review, confirmation) that the request did not ask for. A primary CTA that opens nothing is a Gap, not a button, so the header's primary action is "Export CSV". The payment approve/reject actions are absent for the same reason, although the data carries "Pending approval".
- **G-14 · No page-size control.** Rule 15 lists page size among persisted state, but the basic Pagination variant has no page-size selector. Its `dropdown` variant selects a page, not a size. Page sizes are fixed (10 payments, 8 accounts), and the page number persists in the URL.
- **G-15 · No custom date range.** Filter-toolbar-bar's "Custom range…" hands off to date-range-picker (`delegatesTo`), which was not composed. The option is dropped rather than shipped dead. The presets are 30 days, 90 days, 6 months and 12 months.
- **G-16 · Export options cut to CSV.** The toolbar's Export menu offers CSV / Excel / PDF. Excel and PDF cannot be produced honestly in-page without a library, so that menu is not carried. The page header's "Export CSV" downloads a real file.
- **G-17 · JS-off answer for the chart is an empty table.** Chart-line's meta `fallback` says the authored `<table>` is the JS-off answer. Rule 13 says no number may be typed twice into the HTML. The table head and caption ship and the body is empty, so the engine writes the rows. With JS off, the chart has no data. The metrics show "—" with JS off (never 0).
- **G-18 · Brand: no product name, no font files linked.** The brief skipped Q4. `type.css` names "Univers Next HSBC" with Helvetica/Arial fallbacks, and `knowledge/assets/fonts/` was not wired (no `@font-face` in the files read), so the page renders in the fallback face unless the font is installed.
- **G-19 · The shell has no full-height form for top-nav.** Rule 3a says an app takes `is-full` on `.sh`, but canon.css defines `.sh.is-full` only for doormat, multi-column and side-nav, not top-nav. The page uses the specimen frame (`min-height:560px`, 1px rule, grows with content) unchanged, and `is-full` is not added because it would select nothing.
- **G-20 · The sticky toolbar cannot stick.** `.ftb-outer` is `position:sticky`, but the shell's `.sh{overflow:hidden}` makes the shell its scroll container, so the bar scrolls away with the page. The off-canvas nav sheet is also absolute inside `.sh`, so after a long scroll it opens at the top of the page. Both are inherited from the shell as specimen-framed.

## Data (brief Q5 skipped)

- All figures are invented placeholder data: Arden Maritime Group, its entities, accounts, counterparties, references, IDs and FX rates are fictional. The BICs are formatted as real HSBC BICs only because the masthead brand is HSBC. They are not looked up, and must not be read as real routing data.
