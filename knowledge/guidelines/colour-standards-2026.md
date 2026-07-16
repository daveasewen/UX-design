# Colour standards (2026) — brand guidance (ingested)

*Source: create.hsbc → Foundations → Brand refresh → Colour (`brand-refresh/colour.html` + subpages
`colour/brand-palette.html`, `colour/supporting-palette.html`), captured 2026-07-02 via Dave's
authenticated session (login-walled; ADR-0005 provenance item applies). Structured for the engine:
each rule carries an **enforcement destiny** — [BLOCKING-derivable] statically checkable, could gate
after bite-tests · [ADVISORY-derivable] checkable with tolerances/LLM judge · [TASTE] human. Per
ADR-0005 §5 everything enters advisory-first. These are the REFRESH (2026) standards; the 2025
standards remain usable "until further notice" — both live on the site in parallel.*

## Palette architecture

Two-part system: the **brand palette** (core + greys — identity, layout, typography) and the
**supporting palette** (50 values, 10 families — illustration, data visualisation, RAG **only**).
The refresh merges what were separate data / illustration / RAG palettes into the one supporting
palette. Values: brand core below; supporting values already penned with contrast receipts in
`tokens/_proposals/supporting-palette.proposals.json`.

## Brand palette — core

- **HSBC Red** — Pantone 1795C · C0 M100 Y100 K0 · R219 G0 B17 · **#DB0011**. Masterbrand colour:
  logo, illustrations and pictograms, CTA buttons, physical signage. A visual cue that guides the
  customer's journey.
- **Deep Red** *(new)* — Pantone 7622C · C0 M100 Y100 K42 · R155 G0 B0 · **#9B0000**. Deeper,
  richer red for a "more refined, premium style of communication" (the wealth signal). Created to
  complement — and clearly nod to — HSBC Red, **not replace it**.
- **White** #FFFFFF · **Black** #000000.
- **Grey palette** — named as part of the brand palette but "specifications … will be available
  soon". ⚠ Source gap: no values published as of capture. Our token store's grey ramp remains the
  operative source. [REVIEW — recheck the page when specs land] {#col26-001}
- Four reds reduced to two — simplification is deliberate; recognition over variety.

## Brand palette — rules

- Feature the core colour palette in all communications. [ADVISORY-derivable — presence check] {#col26-002}
- **Don't introduce colours outside the palettes.** [BLOCKING-derivable — this IS the compose
  gate's 0-rogue-hex rule; source now cites it at brand level, not just data-vis] {#col26-015}
- Use red **tactically** to highlight what matters most; don't overuse ("if everything competes
  for attention, nothing stands out"). To draw attention to a CTA, consider an image with less
  red rather than more red. [TASTE] {#col26-003}
- **Don't use red typography — red text is reserved for call to actions.** [BLOCKING-derivable —
  text-colour check: red foreground legal only on CTA elements] {#col26-016}
- **Don't use red backgrounds for text** — prolonged exposure causes visual fatigue and reduces
  legibility. [BLOCKING-derivable — background-behind-text check] {#col26-004}
- Don't apply large amounts of HSBC Red where prolonged exposure may cause visual fatigue.
  [ADVISORY-derivable — red-area-ratio threshold, needs tolerance] {#col26-005}
- Colour ratios across a composition vary by format/messaging/orientation; what matters is purpose
  and hierarchy. [TASTE] {#col26-006}
- **"Do ensure text and icons meet the 4.5:1 minimum contrast ratio."** ✅ RESOLVED 2026-07-02
  by the icons standard (`icons.md` icon-015): differentiated by asset class — **icons 4.5:1
  "in all instances" (interactive, legibility-critical) · pictograms 3:1 + descriptive alt ·
  chart/RAG graphic indicators 3:1.** No source contradiction. Remaining question is OURS:
  our icon checks pass at 3:1; the stricter brand 4.5:1 enters advisory pending Dave's
  promotion ruling. [REVIEW — gate delta, see icon-011/icon-015] {#col26-007}

## Supporting palette — rules

- Scope: **illustrations, data visualisations, status-driven interfaces (RAG, risk, gain/loss)
  only.** "Don't use the supporting palette outside of illustration, data visualisation or RAG
  applications." [BLOCKING-derivable — usage-scope check on fill contexts] {#col26-008}
- **Don't use the supporting palette as text.** [BLOCKING-derivable — text-colour whitelist] {#col26-009}
- Don't use the supporting palette to create sections or segmentations within content.
  [ADVISORY-derivable] {#col26-010}
- **Dark colours on light backgrounds; light colours on dark backgrounds** — never light-on-light
  or dark-on-dark. [BLOCKING-derivable — mode-aware palette-half selection; matches the 33/50
  light / 39/50 dark indicator-legality receipts in the proposals file] {#col26-017}
- **Data visualisation: every colour used must meet ≥3:1 against its background.**
  [BLOCKING-derivable — indicator-contrast gate class] {#col26-011}
- **RAG: text 4.5:1 · graphic elements (icons, chart indicators) 3:1** · surface/background use
  varies by scenario — refer to the specific standard. [BLOCKING-derivable for the two ratios;
  ADVISORY for surface scenarios] {#col26-018}
- **Don't combine HSBC Red with the supporting palette in data visualisations.**
  [BLOCKING-derivable — chart fill-set may contain brand red or supporting colours, not both] {#col26-012}
  ⚠ **SCOPED OVERRIDE (RULED+CONFIRMED Dave 2026-07-16):** gain/loss delta INDICATORS may carry
  red/green (`data/delta-*`, derived — not HSBC Red) in charts; series FILLS unaffected. Full wording
  + record: `data-visualisation.md` dv-019.
- **Distinguish HSBC with HSBC Red; use brand-palette neutrals for competitor data.**
  [ADVISORY-derivable — needs semantic knowledge of which series is "us"; contract-level rule] {#col26-013}
- Complementary combinations: the palette is built around complementary pairs; no rainbow-like
  treatments when two complementary hues achieve the same effect. [ADVISORY-derivable — already
  ingested in `data-visualisation.md`; V7's "B + usage rule" recommendation implements it] {#col26-019}
- Pair supporting colours with brand greys for balance. [TASTE] {#col26-014}
- Never rely on colour alone to convey meaning. [existing 1.4.1 rule —
  `digital-accessibility-standards.md`; gated]

## Usage contexts (all [TASTE], useful for register/contract framing)

- **Marketing** — red anchors key moments; clear hierarchy; adjust intensity per application.
- **Digital** — primary colour on key actions and navigation; supporting colours to organise
  content and highlight priorities; strong contrast, clear labels/icons, test across devices.
- **Documents/presentations** — colour organises information and reinforces hierarchy, never
  competes with content; restrained use, paired with labels or icons.

## Cross-references

`data-visualisation.md` (chart colour treatment — this file is the palette-side source it
anticipated) · `tokens/_proposals/supporting-palette.proposals.json` (values + receipts) ·
`illustration-standards.md` (supersession tension recorded there) · charter §4 (red-may-lead
in balanced/expressive; chart fills flat in all registers).
