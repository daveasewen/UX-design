# Accessibility for visual designers — VD standards (ingested)

*Source: create.hsbc → Processes and tools → accessibility → digital-accessibility-framework →
`accessibility-for-visual-designers.html`, captured 2026-07-03 via Dave's authenticated
session (login-walled; ADR-0005 provenance applies). Engine-era format. First of the 9 role
pages (axf-006). Source structure kept: VD-1…VD-8 are STANDARDS (binding), VD-3/VD-9 are
GUIDELINES (recommended); WCAG SC references preserved. Self-check is the designer's duty
before handoff — "check their own work… before passing it on" — the gate philosophy, stated
at source.*

## Colour (rules)

- **VD-1 — colour is never the only carrier of meaning** (SC 1.4.1 A): information conveyed
  with colour must also be identifiable from context, labelling or alternative forms —
  traffic-light buttons carry words, chart series get hatching/pattern as well as colour;
  prefer palettes differentiable under deuteranopia + protanopia; key data represented
  textually or via a detail link. [ADVISORY — our contrast gates don't check colour-ONLY
  meaning; the RAG roundel policy (icon+label carry meaning) and chart-palette work are
  the existing enactments; candidate composition check for data-vis] {#avd-001}
- **VD-2 — text contrast 4.5:1, large text 3:1** (SC 1.4.3 AA); incidental/decorative and
  logotypes exempt; **text over images needs a chosen-for-legibility image or a
  (semi-transparent) colour block behind the text**. [ADVISORY — already BLOCKING in our
  stack for token pairs + rendered states; the text-on-image scrim clause is the upstream
  anchor for the type26-015 interim (gradient surfaces text-free, scrim = the legal
  alternative)] {#avd-002}
- **VD-3 (guideline) — consider user-selectable text/background colours** (SC 1.4.8 AAA:
  user-selectable fg/bg · ≤80-char measure · no justified text · line-height ≥1.5 within
  paragraphs, paragraph spacing ≥1.5× line-height · 200% resize without horizontal
  scroll); ~10% of UK users prefer alternative combinations; **style-switchers need
  Global Marketing Digital Approvals contact first** — HSBC is investigating strategic
  alternatives. [RECORDED — our dual-theme canon is adjacent; the AAA typography numbers
  are useful retrieval for the finessing pass] {#avd-003}

## Text + components (rules)

- **VD-4 — no images of text** (SC 1.4.5 AA) wherever the technology can render real
  text; customisable/essential (logotypes) exempt; graphs/screenshots/diagrams with
  significant other visual content are out of the definition. [ADVISORY — snippet-side
  candidate check: flag raster text / svg <text> baked into assets; canon renders real
  text everywhere today] {#avd-004}
- **VD-5 — consistent identification + label-in-name** (SC 3.2.4 AA + 2.5.3 A): same
  function ⇒ same label/icon/alt everywhere, across web AND app versions (balanced with
  native-OS component conventions); **accessible name contains the visible text**;
  maintained via a shared component inventory/style guide. [ADVISORY — label-in-name is
  checkable against our snippets (aria-label ⊇ visible label); the "inventory" clause is
  the canon, blessed at source] {#avd-005}
- **VD-7 — every non-text element gets a purpose-alt** (SC 1.1.1 A): alt describes
  PURPOSE; actionable images describe the ACTION ("Play", not the picture); decorative
  images are AT-ignorable; **never "Image of…", "Link to…", "Picture of…", "Add
  button"**; verbose alts harm speech-output users; unclear-purpose images should be
  replaced with ones that tell the story (HSBC's text-heavy pages especially). Visual
  designers deliver alt-text WITH assets. [ADVISORY — cost-0 sweep candidate: banned
  alt/aria-label prefixes; joins nam-001/002 in the sweep queue] {#avd-006}

## Motion + journeys (rules)

- **VD-6 — flashing minimised** (SC 2.3.1 A): nothing flashes >3×/second (or below
  general + red flash thresholds); PEAT is the named checker. [RECORDED — canon motion
  is scale-physics + fades, nowhere near thresholds; keep on record for video/hero
  content] {#avd-007}
- **VD-8 — never prompt the same information twice in a journey** (SC 3.3.7, 2022/
  framework-2024): auto-populate or offer selection of previously-entered data;
  exceptions: essential re-entry, security, expired validity. [ADVISORY — composition-
  layer rule for multi-step journeys; the payments journey is the live test surface]
  {#avd-008}
- **VD-9 (guideline) — focus indicator thickness + change-contrast** (SC 2.4.13): visible
  focus indicator ≥ area of a 2-CSS-px perimeter of the unfocused component, and ≥3:1
  contrast between the same pixels focused vs unfocused; author-untouched user-agent
  defaults exempt. [ADVISORY — our rings are 2px solid ✓; the 3:1 is FOCUSED-vs-UNFOCUSED
  pixels, a different axis than ring-vs-surface — candidate extension to the
  state-contrast gate; pairs with ds-001's ring evidence] {#avd-009}

## Findings

- **F1 — three sweep candidates now queued from Tier 2:** nam-001 (possessive), nam-002
  (all-caps names), avd-006 (banned alt prefixes "Image of/Link to/Picture of/Add
  button") — all regex-cost-0, advisory-first pending Dave.
- **F2 — VD-9 names a gate axis we don't measure:** focused-vs-unfocused pixel contrast
  (≥3:1) — the state-contrast gate measures fg-vs-bg per state, not the DELTA between
  states. Same family as the wcag-state-contrast differentiation rule already in memory.
  Candidate render-gate extension.
- **F3 — self-check-before-handoff is the source's stated duty** (intro): the framework
  expects creators to run the checkpoints themselves before QA — verification-as-
  enforcement, human-shaped.
- **F4 — VD numbering skips VD-3→VD-4 order as published (VD-3 is a guideline listed
  among standards' summary); source's own numbering kept verbatim.**
