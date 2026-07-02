# Data visualisation — brand guidance (ingested)

*Source: create.hsbc → Foundations → Data visualisation (`data-visualisation-foundations.html`),
captured 2026-07-02 via Dave's authenticated session (login-walled). Supplied by Dave alongside the
supporting palette. Structured for the engine: each rule carries an **enforcement destiny** —
[BLOCKING-derivable] statically checkable, could gate after bite-tests · [ADVISORY-derivable]
checkable with tolerances/LLM judge · [TASTE] human. Per ADR-0005 §5 everything enters advisory-first.*

## Terminology
Data set (a structured collection) · data variable (the changing value) · data chart (the diagram).

## Accuracy — "accuracy is key" (do/don't)
- Display the complete scale range; **don't truncate or alter scales** to over/understate trends. [ADVISORY-derivable — axis-min ≠ 0 detection on bar charts] {#dv-001}
- Display full charts with reasonable scales. [TASTE] {#dv-002}
- Show the full data set; **don't omit data to distort interpretation**. [TASTE — but the SME brief's figure-fidelity contract rule is the per-run version of this] {#dv-003}

## Chart types — four categories
- **Relationship** (multiple data sets): grouped bar, …
- **Distribution** (over time/category): bar, histogram, box plot
- **Composition** (part-to-whole): pie, doughnut
- **Comparison** (change over time): line, spark, bullet, candlestick
Choose by the data's needs; research beyond the common types where warranted. [TASTE] {#dv-015}

## Layout
- **Colour separation: don't rely on colour to separate values — minimum 2px separation
  between colour blocks.** [BLOCKING-derivable — gap/stroke check on chart markup] {#dv-004}
- **Tabular alternative** where possible + a link to the table view (digital). [ADVISORY-derivable — presence check] {#dv-005}
- Labelling: title must reflect the main insight; key; alphanumeric labels + key when category
  labels are long; tooltips repeat the data point's values on both axes; **direct labelling
  adjacent to segments in circular charts**; label current/past/projected states. [ADVISORY/TASTE] {#dv-006}
- Content ordering (digital): all data visible at smallest viewport, else explicit navigation
  instructions; adhere to the HSBC responsive grid; on resize, chart elements respond dynamically;
  titles must scale with text-resize (chart info may rely on device zoom). [ADVISORY-derivable] {#dv-007}
- Scrolling: horizontal scroll only as a last resort; the page can't also scroll vertically
  while the chart scrolls horizontally. [ADVISORY-derivable] {#dv-008}

## Content display
- **2-dimensional, flat colour fills only. No 3D styles, no gradient fills.** [BLOCKING-derivable] {#dv-009}
  ⚠ **Interaction with charter §4 (ratified 2026-07-02):** the expressive register's gradient
  unlock applies to surfaces/heroes — **data-chart fills stay flat in ALL registers.** The brand
  rule outranks the register licence inside charts.
- Uncluttered overlays; nothing that obscures data. [TASTE] {#dv-010}

## Colour treatment
- Don't rely on colour alone to carry the narrative. [ADVISORY] {#dv-011}
- **Chart building blocks** (titles, axis labels, axis/grid lines): black-or-grey on light,
  white-or-grey on dark, **≥3:1 (WCAG 2.1 AA)**. [BLOCKING-derivable — same class as the
  indicator-contrast gate; greys retrieved from the digital toolkits] {#dv-016}
- **Only palette colours** in charts (print/digital palette, or the programme toolkit). Now:
  the unified supporting palette. [BLOCKING-derivable — the compose gate's 0-rogue-hex, applied
  to chart fills] {#dv-017}
- Use colour to focus attention; **never as the chart's background**. [ADVISORY-derivable] {#dv-012}
- Segmented data: **different colour per data set variable** (bar), different colours within a
  single-variable circular chart, different colours per line. [ADVISORY-derivable — distinct-fill
  count check] {#dv-018}
- Combination charts (e.g. positive/negative): colour differentiates the data sets. [ADVISORY] {#dv-013}
- **Categorisation consistency:** same data = same colour across every chart in a user journey;
  never reuse one colour for different data in a journey; consistent within a single view.
  [ADVISORY-derivable — cross-chart fill map; needs journey scope] {#dv-014}

## Companions (ingested 2026-07-02, same session)
`data-visualisation-bar-charts.md` · `data-visualisation-pie-charts.md` ·
`data-visualisation-line-charts.md` — the per-type hard rules (zero baselines, 6-slice cap,
sum-to-total, straight lines, spark ratios). Note the deliberate asymmetry: bars REQUIRE a
zero baseline; lines make it optional — enforcement must be chart-type-aware.

## Related
**Ingested 2026-07-02 (day session):** `colour-standards-2026.md` — the colour standards page +
brand/supporting-palette subpages (the "detailed data visualisation colour implementation":
3:1 all chart colours, RAG ratios, no-red-in-charts, palette-half-per-mode, scope rules) ·
`illustration-standards.md` — pie-emphasis exception traced: the grant is **one-directional**
(exists only on the pie-charts page; the illustration standards carry no slice-emphasis content).
**Still open:** the data-vis accessibility deep page — the site's data-vis page links only to the
general accessibility hub (`about-us/Accessibility.html`); the digital-accessibility-standards
page is thin (confirms WCAG 2.2 AA basis, matching ADR-0004). Candidate: the Digital Accessibility
Framework (`processes-and-tools/accessibility/digital-accessibility-framework.html`) — needs
Dave's confirmation of which page he meant. Supporting-palette values + usage rules: already
penned (`tokens/_proposals/supporting-palette.proposals.json`).
