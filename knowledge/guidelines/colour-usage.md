# Colour (2025 standard) — application guidance + delta map (ingested)

*Source: create.hsbc → Foundations and identity → `colour.html` + 3 subpages
(`colour/brand-colours.html`, `colour/illustration.html`, `colour/data-visualisation.html`),
captured 2026-07-02 via Dave's authenticated session (fetch-all method). UPGRADED to
engine era 2026-07-02 — supersedes the 2026-06-18 RAG-era summary. Raw snapshots:
`guidelines/_sources/colour-2025/`. Page banner: "The below standards, from 2025, can
still be used until further notice" — **parallel-valid with `colour-standards-2026.md`**;
the dual-live-palettes desk ruling (2026-07-02) governs which vintage a composition
uses. This file's second job is the **2025→2026 delta map** (below) — deltas ≠ defects,
per the living-standard stance.*

## Scope note — why the old standard earns an engine-era file

Three reasons. (1) **The token store IS the 2025 standard**: every published value —
greys 1–8, dark-mode greys 1–6, all four RAG colours, HSBC Red — exists in
`tokens/colour.json` exactly (F2). Receipts for token provenance land here.
(2) **The 2025 greys are the operative published values** while the 2026 grey specs
remain "available soon" (col26-001). (3) It settles the **blue/400 mystery** with a
source receipt (F1) — the biggest single finding of this tranche.

## Key application rules

- **White and black are the base; HSBC Red is applied tactically** — in digital:
  navigation, signposting and CTAs — to draw the user's attention and drive the
  journey. Continuity receipt for col26-003 and the `color/primary` accent-only
  token rule; identical stance across both vintages. [ADVISORY — receipt; already
  encoded] {#col25-001}
- **Always check contrast when combining or layering colours** (text or icons on a
  background). [ADVISORY — receipt for the enacted contrast gates] {#col25-002}
- **Correct palette for the use case — never cross-use**: illustration palette only
  for illustrations, data-vis palette only for charts, RAG only for status. This is
  the rule the blue/400 illustration import violates (F1). [ADVISORY-derivable —
  palette-scope check on fill contexts; kin of col26-008] {#col25-003}
- **2025 palette architecture**: Brand (Core + Complementary Red + Complementary
  Grey) · Illustration + Complementary Illustration · Data Visualisation · RAG
  (red/amber/green + blue). The 2026 refresh merges the non-brand palettes into one
  50-value supporting palette. [RECORDED — architecture anchor for the delta map]
  {#col25-004}
- **Exceptions to the palettes need brand-design-team approval** — the palettes are
  closed sets ("Don't introduce colours outside of our colour palettes"). Brand-level
  receipt for the compose gate's 0-rogue-hex rule, now sourced in BOTH vintages
  (with col26-015). [ADVISORY — receipt; already gated blocking] {#col25-005}

## Core + Complementary Red (values receipted)

- **Core palette: HSBC Red #DB0011 (Pantone 1795C) · White #FFFFFF · Black #000000**
  — token store match. Core is used in all communications; colour ratios flex by
  format/Hexagon/context. [ADVISORY — value receipt] {#col25-006}
- **Complementary Red palette: Red 1 #E31E22 · Red 2 #BA1110 · Red 3 #730014**
  (Pantones 2033C/7627C/3523C). Used sparingly with the Core palette ("we're not
  just a 'red brand'"); ensure contrast between reds (Red 1 next to Red 3); never
  create new complementary reds; **never tints**. RETIRED by the 2026 refresh (four
  reds → HSBC Red + Deep Red #9B0000). [RECORDED — retired-by-refresh; kept for
  legacy-asset auditing] {#col25-007}
- **No black-and-white photography** (2025 Do/Don't). The 2026 photography standard
  (`brand-refresh-assets.md`) is silent on this. RULED interim by Dave 2026-07-03:
  **the ban CARRIES** — a live standard states it, the other is merely silent;
  silence ≠ withdrawal. Low stakes for the engine (photos are retrieved, never
  made). [REVIEW — interim-ruled 2026-07-03: ban operative; CLOSE when the refresh
  photography page speaks either way] {#col25-008}

## Greys — the operative published values

- **Complementary Grey palette: Grey 1 #F3F3F3 · Grey 2 #EDEDED · Grey 3 #D7D8D6 ·
  Grey 4 #B7B7B7 · Grey 5 #9B9B9B · Grey 6 #767676 · Grey 7 #545454 · Grey 8
  #333333** — token store match, all eight. While the 2026 grey specs stay
  "available soon" (col26-001), THESE are the operative published greys.
  [ADVISORY — value receipt feeding col26-001] {#col25-009}
- **Grey backgrounds: min 4.5:1 for text; source pairing table — text on Grey 1–5 =
  Grey 8 or Black; text on Grey 6–8 = White.** [ADVISORY-derivable — receipt for the
  surface-contrast audit's pairings] {#col25-010}
- **Typography in digital experiences: white or Grey 8 (#333333) ONLY — "don't use
  any grey for typography other than complimentary grey 8."** Contradicted the
  shipped design system: semantic `text/secondary` (light) = #545454 (Grey 7),
  a11y-clean at 7.5:1 on white. RULED by Dave 2026-07-03: **the token store
  governs** — the bank's own export post-dates the page; the page rule is treated
  as marketing-surface/stale guidance. Grey 7 stays as text/secondary; delta map
  notes the tension for the 2026 grey specs to settle definitively.
  [ADVISORY — ruled: token store governs; re-check when col26-001's grey specs
  publish] {#col25-011}
- **Grey usage: lighter greys as solid backgrounds; never the grey palette in
  isolation without brand-palette colours; greys as fallback background when other
  colours can't reach contrast.** [TASTE + the contrast part already gated]
  {#col25-012}
- **Dark Mode Grey palette: DM Grey 1 #656565 · 2 #474747 · 3 #404040 · 4 #212121 ·
  5 #1D1D1D · 6 #101010** — token store match. **Exclusively dark-mode, digital
  only** — never print, never light mode. [ADVISORY-derivable — mode-scope check;
  value receipt for the dark theme ramp] {#col25-013}

## Illustration palettes (values receipted, illustration-side)

- **Main Illustration palette: 5 families × 8 steps (Blue/Green/Pink/Yellow/Orange,
  step 4 = Base)** + **Complementary Illustration palette for skin and hair tones
  (Brown/Mid Brown/Tan/Cream × 8)** — all 72 values verbatim in
  `_sources/colour-2025/illustration-colours.txt`. Rules: essential illustration
  parts ≥3:1 against adjacent colours (AA); brand reds must feature ("don't have
  illustrations without brand reds"; HSBC Red heroes an object or backgrounds a
  Hexagon); no new colours or tints; the illustration palette must never dominate.
  [ADVISORY — illustration-side; engine consumes values by retrieval only; see F1
  for why these values matter to the UI tokens] {#col25-014}

## Data visualisation + RAG (2025)

- **Data-vis palette 2025: 20 values, 5 families × 4 (Blue/Purple/Pink/Orange/
  Green)** — verbatim in `_sources/colour-2025/data-visualisation-colours.txt`.
  Graphical data only; digital may use white OR black backgrounds, print white-only
  (3:1); similar data = neighbouring hues, contrasting data (loss/gain) = opposing
  colours. Superseded in 2026 by the supporting palette (50/10) — see delta map.
  [RECORDED — superseded values; sequence rules live on in
  `data-visualisation.md`] {#col25-015}
- **2025: the Core palette should NOT be used in app or web charts and graphs**
  (status meaning is reserved for RAG). DIRECT FLIP vs col26-013 ("distinguish HSBC
  with HSBC Red" in data-vis). RULED by Dave 2026-07-03: **2026 wins outright** —
  HSBC Red may distinguish own-data in ALL charts; the 2025 ban is superseded and
  recorded for legacy-asset auditing only. (col26-012 still bans MIXING HSBC Red
  with supporting-palette fills in one chart, and RAG semantics remain protected by
  the RAG-scope rules — the ambiguity risk is carried by those, not by this ban.)
  [RECORDED — superseded by ruling; col26-013 governs both vintages] {#col25-016}
- **RAG palette values: Red #A8000B · Amber #FFBB33 · Green #00847F · Blue #305A85**
  — token store match at `color/{red,amber,green,blue}/600`. Semantics, verbatim:
  red = strong negative (errors, unsuccessful outcomes) · amber = negative (alert,
  warning) · green = positive/confirmation · blue = useful information, usually no
  action required. **Digital-UX context ONLY** — "must not be used in any other
  context… This ensures that they remain distinct and meaningful." Source side of
  the RAG roundel policy (ruled + encoded 2026-07-02). [ADVISORY — value receipt +
  scope check; roundel policy already encoded] {#col25-017}
- **THE BLUE RECEIPT: `color/blue/400` (#4587A7) is `illustration/blue-5`, verbatim**
  — the suspected illustration-palette leak is now receipted at value level. The
  2025 standard publishes exactly ONE UI blue: RAG Blue #305A85 (= `color/blue/600`,
  sitting at /600 like its RAG siblings red/amber/green). `focus/ring` (dark) and
  dark `rag/information` alias blue/400 — i.e. they rest on an illustration colour
  that was never a published UI value and fails contrast in the dark combinations
  (the dark-RAG interim patch). Fix path per charter §6: DERIVE a dark-legible blue
  from #305A85 (brand-derived ramp), don't import from illustration.
  EVIDENCE PREPARED 2026-07-03 (Dave: HOLD for a render session). Derivation ladder
  at hue 210° / sat 47%: **#719ECC (L62%)** ≥3:1 on ALL dark surfaces (#101010 6.8 ·
  #1D1D1D 6.0 · #212121 5.7 · #404040 3.7 · #474747 3.3) · **#6293C6 (L58%)** passes
  all but #474747 (2.88), closer to current weight · current #4587A7 FAILS #404040
  (2.61) + #474747 (2.33). Both candidates accent-only (fills keep blue/600 + white
  via the existing driftAllow). BLAST RADIUS: 24 snippet manifests + notifications/
  tabs meta (inspect, don't blind-sed — hex may sit in historical findings) +
  canon.css regenerates. Surface note: #474747 is retired as dark tertiary-hover
  (→#212121, 2026-06-22) but STILL binds form/background/pressed, tabs/hover and
  two tab borders in dark — all real focus-ring adjacencies, so the #474747 column
  counts and #719ECC stays the recommendation. [RULED 2026-07-03 — rendered in
  `_fitness-test/blue400-review.html`, then routed to the DS-improvements register
  per the derivation-governance ruling (nothing derives-and-promotes on the engine's
  derivation alone; design-system errors are LOGGED with artifacts, not patched):
  `_DS-IMPROVEMENTS.md` ds-001. The value does NOT move; candidates stay unpromoted
  evidence. Sibling finding ds-002 (dark error text #DB0011 = 4.02:1 at rest) logged
  the same day.] {#col25-018}

## Pointers (recorded)

- **Business-segment colour guidance exists** (Ultra/High Net Worth · Mass Affluent ·
  Asset Management · Life) — Tier-3, ingest on demand. [RECORDED] {#col25-019}
- **Palette files downloadable in RGB + CMYK** —
  `assets/collections/hsbc_brand_colourpalettes.html`. [RECORDED — asset pointer]
  {#col25-020}

## Delta map — 2025 → 2026

| Topic | 2025 | 2026 | Status |
|---|---|---|---|
| Architecture | 4 separate palette groups | brand + supporting (50 values / 10 families) | supersession at composition level; dual-live ruling picks vintage |
| Reds | HSBC Red + Comp Red 1–3 (no tints) | HSBC Red + Deep Red #9B0000 | Comp Red RETIRED (col25-007); audit legacy assets |
| Greys | Grey 1–8 + DM Grey 1–6 PUBLISHED | "specs available soon" | 2025 values operative; token store matches (col25-009/013 → col26-001) |
| Typography grey | white or Grey 8 ONLY | silent (greys pending) | RULED 2026-07-03: token store governs (text/secondary = Grey 7 stays); re-check at 2026 grey specs (col25-011) |
| Red in charts | Core palette banned in app/web charts | HSBC Red distinguishes own data (col26-013) | RULED 2026-07-03: 2026 wins outright; 2025 ban superseded (col25-016) |
| B&W photography | banned | silent | RULED interim 2026-07-03: ban carries; close at refresh re-cut (col25-008) |
| Illustration | dedicated palettes incl. skin/hair families | folded into supporting palette | supersession recorded in `illustration-standards.md` |
| RAG | 4 values, digital-UX only | RAG inside supporting palette; text 4.5:1 / graphics 3:1 (col26-018) | value continuity confirmed via tokens (col25-017) |
| Contrast floors | 4.5:1 text on greys · 3:1 illustration/data-vis | same numbers restated | no delta — stable across vintages |

## Findings

- **F1 — blue/400 is an illustration import, receipted.** #4587A7 appears in the
  2025 standard ONLY as illustration Blue 5; the published UI blue is RAG #305A85
  (= blue/600). The dark-mode focus ring and dark rag/information stand on an
  unpublished, contrast-failing illustration value. col25-018 carries the fix path
  (derive from #305A85). This closes the "where did #4587A7 come from" question the
  dark-RAG gap logged — with the answer "the illustration palette, verbatim".
- **F2 — The token store is the 2025 standard, value-exact.** All 19 sampled
  published hexes (8 greys, 6 dark-mode greys, 4 RAG, HSBC Red) exist in
  `tokens/colour.json` at matching positions. Provenance receipt for the ADR-0005
  open item: the store's vintage is now documented, not assumed.
- **F3 — REVIEW items: three of four RULED next-day (2026-07-03).** col25-011:
  token store governs, Grey 7 stays (re-check at 2026 grey specs) · col25-016:
  2026 wins outright, 2025 chart-red ban superseded · col25-008: B&W ban carries
  interim, closes when the refresh photography page speaks. col25-018 RULED
  2026-07-03: routed to `_DS-IMPROVEMENTS.md` ds-001 (log-and-move-on; value stands).
- **F4 — Continuity receipts, both vintages agree:** tactical red (col25-001 ↔
  col26-003) · closed palettes / 0 rogue hex (col25-005 ↔ col26-015) · palette-scope
  discipline (col25-003 ↔ col26-008) · contrast floors stable. The compose gate's
  rules are now double-sourced.
- **F5 — Vintage markers.** "Supercharging our brand" banner names the refresh;
  Brand Effect Model funnel framing throughout brand-colours; source typos
  ('opportunitites', 'complimentary grey', Tan 3 'K:' with no value) captured
  faithfully — don't "fix" the snapshots.

## Cross-references

`colour-standards-2026.md` (the parallel-valid refresh standard; col26-001 grey gap) ·
`tokens/colour.json` + `semantic-colour.json` (the value matches, F2) ·
`focus-indicators.md` (focus/ring aliases blue/600 light + blue/400 dark — F1) ·
`dark-mode.md` (DM grey scope) · `data-visualisation.md` (chart treatment rules) ·
`illustration-standards.md` (2026 illustration supersession) · charter §6
(derive-from-fixed — the blue/400 fix mechanism) · dual-live palettes desk ruling
(2026-07-02).
