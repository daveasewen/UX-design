# Nio dashboard → Apollo Console — composition mapping

**Artefact:** `knowledge/_fitness-test/nio-dash-console-v1.canon.html`
**Generator:** `knowledge/_render/gen_nio_dash.py` (re-run it; never hand-edit the HTML)
**Reference:** `Nio-Dash.png` (repo root) — HSBC "Nio" business-banking overview
**Theme:** `data-apollo-theme="console"`, light + dark both wired
**Status:** ⬛ fitness test. NOT gated as canon, NOTHING RULED, awaiting Dave's eye.

Dave's constraint, verbatim: *"recreate this using console components, don't invent anything apart
from the header and footer."* — In the event **nothing at all was newly authored**: the library
already carries a top-nav shell and a footer, so both permitted inventions were spent on nothing.

**Verdict key** — EXACT = the component's own markup, used for the job it was designed for ·
CLOSEST = an existing component standing in for something the reference does differently ·
GAP = the library has no answer and the region is deliberately not reproduced.

**Counts: 24 EXACT · 11 CLOSEST · 5 GAP.**

---

## Chrome

| # | Reference region | Component used | Verdict | Note |
|---|---|---|---|---|
| 1 | Top nav bar: HSBC ∣ NIO, Overview/Spending/Payments/Authorisations, current-page rule | `.cn-app-shell-top-nav` — `.sh[data-form="inline"] > .sh-masthead`, `.sh-nav`, `.sh-logo`, `.sh-skip` | EXACT | The permitted "new header" was not needed. Three **layout-only** harness overrides on `.sh` are declared in the page comment: `min-height:0`, `border:0`, `border-radius:0` — the 560px/1px/20px specimen frame exists so the component reads as a card in the showroom; a real masthead is full-bleed. No colour, type or internal spacing touched. |
| 2 | "Nio assist: ask a question or search for something" | `.cn-search-field` — `.search.boxed` | EXACT | Reference's bold "Nio assist:" prefix inside the field is carried as placeholder text. |
| 3 | The `+` button beside the assist field | `.cn-icon-button` — `.iconbtn.tertiary` + library `add.svg` | EXACT | |
| 4 | `⋯` overflow, bell, avatar in the top-right | `.cn-app-shell-top-nav` `.sh-actions` + library `menu-more-horizontal.svg`, top-nav's own account glyph | CLOSEST | **No bell/notification glyph exists in `assets/icons`.** The notifications slot carries the library's `menu-more-horizontal` instead of an invented bell. Logged as an icon gap. |
| 5 | Legal/footer band | `.cn-footer` — `footer.ft.slim > .ft-inner > .ft-legal` | EXACT | The slim (app-chrome) form, which is what the reference's single legal strip is. The permitted "new footer" was not needed. |
| 6 | Magenta/pink brand gradient sweep behind the doormat, and the short red rule under each feature heading | — | **GAP** | No brand-gradient or brand-rule component exists, and both would be **authored colour**. Deliberately omitted; the two-red law `s151-D1` is untouched. |

## Balances

| # | Reference region | Component used | Verdict | Note |
|---|---|---|---|---|
| 7 | Panel surface + "Balances" title | `.cn-template-dashboard` — `.stat-card.tpl-panel` inside `.tpl-section` | EXACT | Console radius (surface 20px) arrives from the theme cascade, not from the page. |
| 8 | Four stat cards: label, big figure, delta, sparkline | `.cn-kpi-tile` — `.kpi-tile` + `.lbl16` + `.amt` + `.delta.up/.down` + `.kpi-spark > .spark-inline` | EXACT | Kpi-tile is the exact composite the reference draws: value + delta + twelve-point spark. |
| 9 | The red/green status dot in front of each card label | `.cn-status-indicator` — `.stat.ok / .stat.err` (inline dot + label) | EXACT | RAG arrives from `--rag-*` under Console. **The reference's HSBC red/green are not copied.** |
| 10 | The red ↓ / green ↑ arrow at the right of each card | `.cn-kpi-tile` `.delta.up/.down` arrow | CLOSEST | Kpi-tile puts the direction arrow **inside the delta line**, not floated to the card's right edge. Same signal, canon's placement. |
| 11 | Grouped bars by month + `1Y 6M 3M 1M` range switch | `.cn-chart-bar` `data-dv-type="grouped-column"` + `.cn-segmented-control` `.seg.sm` | EXACT | 12 groups × 2 series (Money in / Money out). |
| 12 | Two unlabelled icon buttons top-right of the chart | `.cn-chart-bar` `.dv-controls` — Copy data (CSV) + View as table | CLOSEST | Canon's chart tool cluster is labelled by rule; the reference's bare glyphs are not reproduced as glyphs. |

## Accounts

| # | Reference region | Component used | Verdict | Note |
|---|---|---|---|---|
| 13 | "Balance total 112,514.11 GBP" | `.cn-amount-display` — `.amount.amount--display.t-cm-figure-4` | CLOSEST | ⚠ **Currency order inverted against canon.** Amount-display's `copy-025` puts the code **before** the value, closed up (`GBP112,514.11`). The reference prints `112,514.11GBP`, and the KPI tiles do the same with `EUR`, so this screen follows the reference. **A question for Dave, flagged not settled.** |
| 14 | `All / Current / Cards` filter | `.cn-segmented-control` — `.seg.sm` | EXACT | |
| 15 | Two icon controls at the right of the filter row | `.cn-view-options` — `.seg` icon pair + library `settings.svg` / `sort.svg` | CLOSEST | Reference shows a "tune" slider glyph and an up/down chevron pair; the nearest library glyphs are used rather than drawn. |
| 16 | Account rows: name, `GB \| 001-011113-004`, balance, type tag | `.cn-list-items` — `.list > li > button.row > .body > .line` + list-items' own `.tag` | EXACT | The reference's 8th row is faded (an affordance for "more below"); not reproduced — list-items has no faded-tail state. |
| 17 | Search field at the foot of the list | `.cn-search-field` — `.search.boxed` | EXACT | |

## Spending

| # | Reference region | Component used | Verdict | Note |
|---|---|---|---|---|
| 18 | Donut with spider letters A–F and centre total | `.cn-chart-donut` `data-labelling="spider"` | EXACT | Arc geometry minted from the six printed figures. |
| 19 | Legend list `A. Payroll 8,500 …` with a **Total** row | `.cn-chart-donut` `.dv-leg.vert` **+** `.cn-summary` `dl.summary` with `.summary__row--total` | CLOSEST | Canon's chart legend carries **name only** (it is the isolate/filter control); values live in its "View as table" panel. To reproduce the reference's name→value list *and* keep the interactive legend, the two components sit side by side: legend = the filter, summary = the figures. **DS question: should the dataviz legend carry a value column?** |
| 20 | Bar/pie view-mode toggle above the donut | — | **GAP** | Canon's donut has no chart-type switcher; `.dv-controls` offers value/percent and table instead. Not invented. |
| 21 | "Spending Overview" single-series line + range switch | `.cn-chart-line` `data-dv-type="line"` + `.cn-segmented-control` | EXACT | |

## Payments

| # | Reference region | Component used | Verdict | Note |
|---|---|---|---|---|
| 22 | Left rail: Transfers / Bills / Standing Orders / Direct Debits / Payments / Term Deposit | `.cn-sidebar-nav` — `nav.sn > .sn-body > .sn-group > ul > li > a.sn-link` | EXACT | Glyphs are library glyphs re-used by meaning; the reference's bespoke payment-type glyphs have no library equivalents. |
| 23 | `✓ Payee — ② Details — ③ Review` stepper | `.cn-progress-tracker` — `ol.steps` dots form | EXACT | `style="--demo-width:100%"` releases the component's 520px **specimen** width, which otherwise trips its own `@container (max-width:520px)` collapse and hides the dots. Runtime var, gate-exempt. |
| 24 | Uploaded invoice row with a remove `⊗`, a PDF glyph and a validation tick | `.cn-document-row` `.dr-glyph` + `.cn-status-indicator` `.stat.ok` "Validated" | CLOSEST | `.cn-file-upload` owns the staged-file row *with* remove, but it only exists attached to a drop zone; Document-row is the closer standalone shape. The reference's `⊗` remove control is not reproduced. |
| 25 | "Paying to" payee card with a **Utility** chip | `.cn-tags` `.tag` inside a bordered block + `.cn-summary` for the invoice/issued/due lines | CLOSEST | ⚠ **`.cn-badge` is the wrong component here** — canon's `.badge` is `position:absolute` (a count badge pinned to a glyph); a category label is a **Tag**. Caught in render, corrected. There is no "payee card" component; the block is a harness border on canon radius tokens. |
| 26 | Account number / Sort code / Reference | `.cn-summary` — `dl.summary` | EXACT | |
| 27 | Collapsible "Gas Supply – total £1,247.85" with four charge lines | `.cn-accordion` `.acc > .item > button.head + .panel > .inner` wrapping `.cn-summary` | EXACT | Open by default (`max-height` inline, as the snippet does for its open item). |
| 28 | "Paying from — Operations, Current ···· 4417, £32,450 GBP" | `.cn-account-selector` — `.as` combobox + `.as-menu` listbox | EXACT | |
| 29 | Amount field, read-only, with a pencil | `.cn-amount-input` `.ai-group/.ai-box` + `.cn-icon-button` `.iconbtn.tertiary` + library `edit.svg` | CLOSEST | Amount-input has no read-only-with-edit-affordance state; composed from the input plus an icon button. |
| 30 | Payment type picker showing "Instant payment … £1,247.85 GBP" | `.cn-dropdown` — `.dd.boxed` combobox | CLOSEST | Canon's dropdown trigger carries one value slot; the reference's trigger carries a glyph, a two-line label **and** a trailing amount. The amount is dropped from the trigger (it is stated in the Amount field above it). |
| 31 | Back / Cancel / Continue | `.cn-button` — `.btn.tertiary` / `.btn.secondary` / `.btn.primary` | EXACT | |

## Predictive signals

| # | Reference region | Component used | Verdict | Note |
|---|---|---|---|---|
| 32 | Signal card: currency, title, big figure, sub-line | `.cn-template-dashboard` `.stat-card` surface + `.t-cm-figure-4` + `.t-cm-legal` | CLOSEST | There is no "signal card" component. Assembled from the dashboard panel surface and type composites only — no new appearance is declared. |
| 33 | Teal / amber / red confidence bar | `.cn-meter` — `.meter-track > .meter-fill` | **GAP** (partially) | **No meter, progress-bar, limits-meter or runway-bar carries a RAG tone variant** — every fill is ink on track by design (`s210`: progress is structure, not status). The bar therefore renders neutral, and the RAG reading is carried by `.cn-status-indicator` `.stat.ok/.warn/.err` on the "Confidence NN%" line beneath it. **DS-defect candidate: a RAG-toned meter fill.** |
| 34 | `⋯` per-card overflow menu | — | **GAP** | No kebab/overflow-menu affordance in the library, and `_validate_icons` flags shape-only kebabs by rule. Omitted rather than invented. |
| 35 | "Inspect XAI" + share glyph | `.cn-links` — `a.arrow` with `.lbl` + `.tip` | CLOSEST | The library's `share-ios.svg` exists, but the arrow-link is the canon idiom for "go and look at this"; the share glyph is not used as a navigation affordance. |

## Your spending · feedback · doormat

| # | Reference region | Component used | Verdict | Note |
|---|---|---|---|---|
| 36 | Four-series line chart, 12 months | `.cn-chart-line` `data-dv-type="multiline"` — circle / square / diamond / square markers + `.dv-leg.center` | EXACT | Shape + letter, so colour is never the only channel. Canon's marker rotation only defines three shapes; the 4th series reuses the square. **DS-defect candidate: no 4th marker shape.** |
| 37 | Grouped bars, six months | `.cn-chart-bar` `data-dv-type="grouped-column"` | EXACT | Reference draws an irregular 2/3/2/3/2/2 bars per month; reproduced as a regular 3-series grouping (see divergences). |
| 38 | "Your feedback is important to us / Tell us what you think about Nio" | `.cn-cta-lockup` — `.ctal.centered > .ctal-titleblock` | EXACT | |
| 39 | Three feedback chips with trailing glyphs | `.cn-button` `.btn.tertiary` + library `success` / `close` / `add` glyphs | CLOSEST | The reference's controls are pill "chips"; Tags' `.tag` is not a button and `.cn-selection-controls` is a form control, so the outlined button is the closest actionable form. The lightbulb glyph does not exist in the library — `add.svg` stands in. |
| 40 | "Learn more about Neo" 4-up feature cards with "Find out more" | `.cn-feature-grid-lockup` — `.fgl-grid.up-4 > article.card.feat` + `.cn-button` `.btn.primary` | EXACT | Two of the four glyphs (mandates, security device) map to library glyphs by meaning; the reference's document-stack and calculator glyphs have no equivalents. |

---

## Content notes and honest divergences

1. **The reference's own spending arithmetic does not close.** Its six rows (8,500 · 2,400 · 1,050 ·
   890 · 314 · 580) sum to **13,734**, but it prints **£12,684** in the donut centre and in its Total
   row. The rows are reproduced verbatim; the total shown is the **arithmetic sum**, because the donut
   arcs are derived from the rows. Not silently reconciled.
2. **The four chart panels print no numbers, only shapes.** Their series are **read off the drawn
   heights** against the reference's own printed 0–100 axis. That is a reading, not a measurement, and
   is declared as such in the generator.
3. **`Nio-Dash.png` labels its own months `May … Apr`** in every chart; that ordering is kept.
4. **Grouped bars, second chart:** the reference draws an irregular 2/3/2/3/2/2 bars per month with a
   different hue family per month. Reproduced as a regular 6 × 3 grouping with one hue per **series**,
   because a per-month hue would make colour carry no information — canon's series palette is
   series-indexed by rule.
5. **Donut centre value:** the baked SVG carries `£13,734`; the live `dv-legend` behaviour re-renders
   the centre from `data-total` and prints `13734` — no currency symbol, no thousands separator.
   **DS-defect candidate.**
6. **Sparkline scale.** Kpi-tile's spark is `aria-hidden` decoration at tile size; the reference's
   sparklines are the same, so the twelve points are minted to the shape of each tile's trend rather
   than to a shared axis.
7. **Everything the reference draws in HSBC red or green** — the dots, the arrows, the negative
   figures, the confidence bars — arrives here from `--rag-*` / `--data-series-*` / `.delta` under
   Console resolution. No colour value is authored anywhere on the page, and the page declares zero
   `font-size` and zero `font-weight`.
