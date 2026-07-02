# Typography (2026) — brand guidance (ingested)

*Source: create.hsbc → Foundations → Brand refresh → Typography
(`brand-refresh/typography.html`), captured 2026-07-02 via Dave's authenticated session
(login-walled; ADR-0005 provenance applies). Engine-era format. 2026 refresh standard —
2025 standards remain usable "until further notice" (parallel-valid, same pattern as colour).
Subpages NOT yet ingested (queued): `typography/typefaces.html`,
`typography/creative-headlines.html`, and the typography **specification** page (minimum
sizes, colours, leading, kerning — the component-relevant numbers live there).*

## Typefaces

**Univers Next for HSBC** is the core typeface (digital + print), visually matched with
**MYing Hei** (Chinese) and **Univers Next Arabic** — one multilingual system. A complete
brand font collection is downloadable on the site (licensed — not fetched; the sandbox
renders with fallbacks regardless, see `_ROBUSTNESS-PORTABILITY.md`).

- **Token-store delta:** ✅ RESOLVED 2026-07-02 — the claimed delta doesn't exist; the
  review misread the store. Receipts: `tokens/typography.json` `font-family.default.$value`
  is already **"Univers Next for HSBC"** (since the Figma native re-base; fix #5 2026-06-19
  built `$webStack` around the same name) and all 45 snippet font-stack references match.
  Plain-"Univers" appears only in prose comments ("Univers Light renders too thin"), never
  as a token value. No 2026 mode needed for the typeface; store already targets the refresh.
  Residual (unverified here): Sutherland fixtures live outside this repo — spot-check the
  font stack at next Sutherland touch. {#type26-001}

## Key takeaways (rules)

- **Only use brand-approved fonts, weights and colours.** [BLOCKING-derivable — font-family
  whitelist; colour side already gated] {#type26-002}
- **All text legible and ≥4.5:1 contrast.** [BLOCKING-derivable — existing text-contrast
  gate, already enforced] {#type26-003}
- **Never use red typography except within specific digital toolkit use-cases.** Sharpens
  the col26 red-text rule: the exception scope is toolkit-defined (e.g. CTA links), not
  designer judgment. [BLOCKING-derivable — red-text check with toolkit-exception allowlist]
  {#type26-004}
- **"We don't use uppercase or italics lettering — use sentence case."** ⚑ This makes the
  house sentence-case rule (and the G5 all-caps advisory check) **source-backed at brand
  level** — and extends it: *italics are also out*. Informs the open all-caps scope ruling
  on Dave's desk: the source is brand-wide, favouring canon-wide over brief-scoped.
  [BLOCKING-derivable — the advisory all-caps rule has its promotion evidence; italics
  check is new] {#type26-005}
- Only use lighter font weights for creative headline treatments; favour lighter weights
  generally, bolder weights only for occasional emphasis (a word, a subheading).
  [ADVISORY-derivable — weight-usage distribution] {#type26-006}

## Principles

- **Expressive headlines** — emphasis, pace, personality without losing clarity; fewer
  words; never obscure or break a word into illegibility. [TASTE — matches refresh
  cheat-sheet; fenced to composition experiments per `_BRAND-REFRESH-DIRECTION.md`]
  {#type26-007}
- **Balanced bilingual** — Latin/Chinese/Arabic given comparable prominence, unified not
  "translated"; balance layout, hierarchy, spacing, line length. [TASTE — no bilingual
  content in the canon yet; becomes contract-relevant for multilingual briefs] {#type26-008}
- **Clear type hierarchy** — scale/weight/spacing/placement signal reading order; limit
  weight levels to the minimum; **max two main fonts with a bold option**.
  [ADVISORY-derivable — countable font/weight census per view] {#type26-009}

## Specification (`typography/specification.html`, ingested same session)

### Weights
- Headlines: lightest weights (**Ultra Light, Thin, Light**) at larger sizes; heavier only
  for a clear hierarchy shift or single emphasis point. **Never bold an entire headline** —
  one or two words at most. Body: light/regular. "If everything's bold, nothing is."
  [ADVISORY-derivable — weight-usage census] {#type26-010}
- Hierarchy depth: **3–4 levels** (L1 headline, L2, supporting, body). [ADVISORY-derivable]
  {#type26-011}

### Minimum sizes
- **Latin: 12pt minimum, print AND digital.** Captions/small legal copy may go to **6pt**
  minimum. **Ultra Light/Thin forbidden at small sizes** (line too thin to be legible).
  **Chinese (MYing Hei): 14pt body minimum.** Arabic: 12pt (as Latin).
  [BLOCKING-derivable — font-size floor per script + weight-at-size check] {#type26-012}

### Type colour (the strictest rule set on the page)
- **Black/dark-grey on light · white/light-grey on dark · NO other colours for typography,
  ever.** White-only on HSBC Red and supporting reds; no long-form copy on red or coloured
  backgrounds; **no highlighted type blocks**; over photography black or white only.
  [BLOCKING-derivable — text-colour whitelist; tightens col26-009's no-supporting-as-text
  to a black/grey/white-only rule] {#type26-013}
- Headline-on-photography contrast: **3:1 large AA · 4.5:1 small AA · 7:1 AAA.**
  [BLOCKING-derivable — existing contrast-gate class] {#type26-014}
- **"Don't overlay text on gradient backgrounds"** (+ digital: verify at viewpoints, no
  unreadable wrap). ⚠ Collides with charter §4's expressive gradient unlock for
  surfaces/heroes — heroes normally carry headlines. 📌 PARKED 2026-07-02 (Dave) → ruled at
  the component-finessing pass, alongside mot-007 ("too expressive" family). **Interim
  discipline: no gradient-hero generation; gradient surfaces are treated as text-free zones
  until ruled** (conservative reading holds by default). Candidate mechanisations noted for
  the pass: text-free-zone gate (no text node over gradient surface) vs worst-point contrast
  sampling (≥4.5:1 at the ramp's weakest point, render-based). [REVIEW] {#type26-015}

### Kerning and leading
- Latin headlines: **−15 to −30 tracking; leading = size +3pt** (50pt → 53pt). Latin body:
  **−5 to −10 tracking; leading "1.1×"** — ⚠ but the page's own example is 12pt → **16pt**
  (1.33×), and Chinese body says 1.1× with example 14pt → 18pt (1.29×). Stated ratio and
  worked examples disagree — likely "1.1×" should read differently or the examples embed
  channel-specific values. [REVIEW — source-internal inconsistency; our tokens keep their
  own leading values meanwhile] {#type26-016}
- Chinese headlines: leading **1.25×**; body 0 to +10 tracking. Fine-tune Chinese
  punctuation spacing; refine baselines when mixing scripts. [ADVISORY] {#type26-017}
- No wide kerning that breaks legibility; not too tight either. [TASTE] {#type26-018}

### Casing, alignment
- **Title case AND sentence case** are the brand-legal casings; **uppercase banned outside
  acronyms** (explicitly: harder to read, reduces word shapes, dyslexia/low-vision cost).
  Note: the house rule (sentence case ONLY, no title case) is *stricter* than brand — house
  wins locally, no conflict. ✅ ENACTED 2026-07-02 (Dave ruling): canon-wide sweep done —
  14 snippets + gallery chrome de-capped (caps tracking removed with it, Eyebrow precedent),
  canon.css regenerated, 0 signals; check PROMOTED advisory → blocking
  (`_validate_snippets.py` check 4, acronym-run exemption, bite-tested ×2 in
  `_tests/test_gates.py`). [BLOCKING — enforced] {#type26-019}
- **Left-aligned is primary**; centred sparingly (short headings/labels/callouts, small
  word counts); right rare ("Headline A of the magnetic type construct"); body copy stays
  horizontal. **Never justified** (rivers); avoid hyphenation — rebalance lines instead.
  [BLOCKING-derivable for justify/hyphens; ADVISORY for alignment choice] {#type26-020}

### Bilingual mechanics
- Size ratio **1.0× Latin : 0.85× Chinese** (perceived-height parity); **Chinese one weight
  step thicker than Latin** (Univers Ultra Light ↔ MYingHei Thin · Thin ↔ Light · Light ↔
  Regular · Regular ↔ Medium). [ADVISORY-derivable — becomes contract-relevant for
  multilingual briefs] {#type26-021}

## Usage contexts ([TASTE], register/contract framing)

Marketing/social: clean, scannable, mobile-legible. Digital: hierarchy reduces cognitive
load, journeys feel calmer. Documents/presentations: size/weight/spacing differences turn
dense content into a navigable path.

## Typefaces (`typography/typefaces.html`, ingested 2026-07-02)

*Raw snapshot: `_sources/typography-2026-subpages/`.*

- **The multilingual font system:** Univers Next for HSBC (Latin — Frutiger heritage,
  neo-grotesque); **MYingHei** (Traditional + Simplified Chinese, visually aligned to
  Univers in tone/stroke/proportion); **Univers Arabic for HSBC** (harmonised proportion/
  weight); Cyrillic/Japanese/Armenian = "a variety of other fonts that are visually
  similar to Univers". [IN FORCE — store receipt; further nail in dissolved type26-001.
  Vintage delta noted: 2025 named Tazuane Gothic for Japanese; 2026 names no specific
  Japanese cut — softened, not contradictory] {#type26-022}

## Creative headlines (`typography/creative-headlines.html`, ingested 2026-07-02)

- **Elegant weights: the LIGHTEST cuts (Ultra Light, Thin, Light) at large sizes** for
  headlines; heavier weights only for a clear hierarchy shift or a single point of
  emphasis; concise headlines, comfortable letter spacing, clean line breaks.
  ⚠ "Ultra Light" is not in the licensed five (Thin/Light/Regular/Medium/Bold,
  type25-004) and has no token-store weight (store: 100/300/400/500/700). [REVIEW —
  new weight or loose language? Check the font package / next export; don't add a
  weight token unilaterally] {#type26-023}
- **Balanced dual language** — Latin + Chinese + Arabic get comparable prominence,
  "unified, rather than 'translated' or secondary"; balance layout/hierarchy/spacing/
  line length. [TASTE — bilingual mechanics numbers live in the Specification section;
  no engine action until a bilingual target exists] {#type26-024}
- **Give imagery room to breathe:** type frames the focal point, sits in clean negative
  space or along natural composition lines; grids + rule of thirds; clear visual path —
  headline first, then the image's key detail. **Centre alignment is now legitimate** in
  named cases: ambient photography without a focal point (Iconic Hexagon central, with
  or without text), magnetic headlines centred. ⚠ DELTA vs 2025's "never centre-align
  creative headlines with hexagons" (type25-017). [REVIEW — 2025↔2026 delta; deltas ≠
  defects; the refresh reads as the forward direction, 2025 rule holds for 2025-standard
  work] {#type26-025}
- **Over-photography watch-outs:** legibility first — avoid busy areas, high-contrast
  edges, faces; safe placement, sufficient contrast, "(where needed) a subtle gradient/
  overlay, rather than heavy effects"; respect the subject — never cover focal points/
  faces/brand cues. ⚠ DELTA vs 2025's flat "no treatments — adjust the asset" (type25-013):
  the refresh PERMITS subtle overlays as a contrast aid. Interim reading: overlay-as-
  contrast-aid OK (it's also the dark-mode imagery mechanism, webf-008), decorative
  effects still banned. [REVIEW — fold into the finessing pass with the gradient family;
  affects hero generation once unparked] {#type26-026}
- **Open Hexagons as framing/flow devices:** anchor, emphasise, organise — never force
  type to follow hexagon edges (no squeezing/warping), mind angle "pinch points",
  breathing room for both; short simple text INSIDE is fine, long-form never; don't
  overlap the Cropped Hexagon edge; stay in safe areas. [composition vocabulary —
  fenced] {#type26-027}
- **Cropped Hexagon watch-outs:** no tangents (letterforms "kissing" the crop edge);
  protect readability near high-contrast crop intersections; alignment intentional —
  to the hexagon's dominant angles or a clean grid. [composition vocabulary — fenced]
  {#type26-028}
- **Magnetic headline (NEW construct):** an Iconic Hexagon sits at the CENTRE of the
  headline line as visual anchor/pivot; words "magnetised" around it; vertical alignment
  to the hexagon's 5 vertices, baselines to hexagon geometry; photography stays the hero
  (magnetic block moves to give the subject space; stacked/side variants; centred over
  ambient scenes); rule of thirds guides, not strict. This is the brand-campaign headline
  construct — the 2026 replacement register for 2025's big-and-light/small-and-bold
  pairing. ⚠ DELTA: 2025's "only Big-and-Light and Small-and-Bold" takeaway has no 2026
  equivalent; the refresh's named types are "over photography" and "magnetic". [REVIEW —
  2025↔2026 treatment-vocabulary delta; reconcile when the refresh settles; fenced to
  composition strand either way] {#type26-029}

## Cross-references

`typography-usage.md` (2025 standard + creative-headline system — UPGRADED to engine era
2026-07-02, type25-*; deltas: type26-025/026/029) · `colour-standards-2026.md` (red-text
family, col26-004/005) · `_ADVISORY-SIGNALS.md` + `_validate_advisory.py` (all-caps rule →
promoted 2026-07-02) · `tokens/typography.json` (already Univers Next — type26-001
resolved; weight receipt 100/300/400/500/700 ↔ type26-023's Ultra Light question) ·
`_BRAND-REFRESH-DIRECTION.md` (expressive headlines + hexagon composition, fenced) ·
`web-foundations.md` (webf-008 overlay mechanism ↔ type26-026).
