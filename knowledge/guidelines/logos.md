---
title: Logos — the one logo guideline
source: MERGED under s282-D5 (Dave 2026-09-18, his own export of the #282 logo review) from
  TWO sources — (1) HSBC Common Toolkit (MCP) "Gaps and edits" branch, Foundations › Logos
  page (node 29:1009), captured 2026-06-17, the 2025-era sticker sheet this file already
  was; (2) the logo section of `brand-refresh-assets.md` (create.hsbc → Foundations and
  identity → Brand identity refresh, `brand-refresh/logos.html`, captured 2026-07-02),
  whose `logo26-001..007` bullets moved here byte-for-byte, together with `va25-015`,
  `va25-016` and `va25-017` from the 2025 Logos section of `visual-assets.md`.
type: foundation-guidance
captured: 2026-06-17
merged: 2026-09-18
precedence: |
  APOLLO'S DECISIONS OVERRIDE THE REFRESH WHERE THEY DIFFER — Dave, 2026-09-18: "our
  decisions here over-ride the refresh". Where a rule below carries an Apollo ruling id
  (s282-D3, s282-D4, s282-D5) and a moved brand bullet says otherwise, the Apollo rule
  governs. Each moved block is labelled with its vintage (2026 refresh / 2025 page) so the
  boundary bra26-003 protects is kept inside this file instead of across two files.
related_assets: knowledge/assets/logos/ (8 logo SVG variants, 12 before s282-D4 — EXPORTED 2026-06-17, vector; see _export-logos.py)
external_ref: https://create.hsbc/foundations-and-identity/Logos.html
note: |
  This is the SINGLE logo guideline (s282-D5, q5 (a) "Merge into one logo guideline").
  Photography and Creative Hexagons stay in `brand-refresh-assets.md`; `va25-014` (the
  PRINT clear space and the 105×20px minimum) stays in `visual-assets.md` — it is the print
  rule and this ruling did not name it. No design tokens.
---

# Logos

The one logo guideline: the artwork set, the Apollo decisions that govern it, and the brand
rules — 2026 refresh and 2025 page — that were moved here under `s282-D5`. Where the brand
standard and an Apollo decision differ, the Apollo decision governs (see `precedence`).

## Logo set

Two logo lockups (the *Masterbrand with identifier* lockup was SCRAPPED — s282-D4, Dave
2026-09-18: its four files moved to `_to_delete/logos-identifier-282/`, its nodes removed
from the graph), each available in **Colour** and **Monotone**, and in **On Light** and **On
Dark** treatments (the On-Dark artwork is the light/reverse version for dark surfaces):

1. **Hexagon** — the HSBC hexagon mark alone.
2. **Masterbrand** — hexagon + "HSBC" wordmark.
3. ~~Masterbrand with identifier~~ — SCRAPPED (s282-D4). The identifier lockup was an
   "Example identifier" placeholder; two of its four exports were the plain masterbrand on a
   wider canvas (#282 logo review, exporter defect). Dave's export answered q6 (b), "Retire
   the four identifier variants until a real identifier exists", and his forward note — the
   material may one day return as an AI-readable "Ask create" assistant — is FILED as a
   carry (W-282ll), not enacted.

That's **8 variants** (2 lockups × {Colour, Monotone} × {On Light, On Dark}) — was 12
before s282-D4. The `hexagon-dark-colour` / `hexagon-light-colour` pair is ONE drawing
exported twice (619 bytes each, diff = 1 float literal) and BOTH FILES AND BOTH NODES ARE
KEPT — s282-D5, q1 (a) "Keep both files and both nodes"; no alias, no `activeVariantOf`.

## Size — the Apollo scale (s282-D3)

Logo size is measured by **HEIGHT**, on five steps:

| step | height |
| --- | --- |
| x-small | 24px |
| small | 28px |
| medium | 32px |
| large | 36px |
| x-large | 40px |

The height is the artwork's **RAW pixel height, not a viewBox scaled to it** — Dave: "no
view boxes, just the raw height" · "and width obviously". Width follows the lockup's own
ratio and is never the measure. Whether any lockup may render UNDER x-small is NOT ruled.

## Apollo rules (s282-D5, 2026-09-18 — his own export)

- **The masthead logo is the FULL-COLOUR Masterbrand on BOTH grounds, in ALL FOUR
  THEMES** — `masterbrand-light-colour` on light, `masterbrand-dark-colour` on dark, in
  Apollo Legacy, Apollo Mono, Apollo Console and Apollo Supercharge alike. A monochrome
  theme does not make a monochrome masthead: mono is not the masthead lockup in any theme.
  `va25-015` says a Masterbrand appears in ALL digital mastheads; this names WHICH VARIANT.
  Dave answered "Full colour both grounds — masterbrand-light-colour on light,
  masterbrand-dark-colour on dark" on all four theme rows of his own export.
  (s282-D5, Dave 2026-09-18) [BLOCKING — masthead variant check; the Header/masthead
  component inherits it alongside va25-015's behaviour contract] {#logo26-008}
- **Digital clear space is a FLOOR, not the print rule: vertical clear space ≥ 0.25 × logo
  height, snapped UP to the 4px grid.** At the five `s282-D3` steps that is 24 → 8 · 28 → 8
  · 32 → 8 · 36 → 12 · 40 → 12 px. It is a floor, not a value: anything at or above it that
  itself sits on the 4px grid is legal. Dave's words: "The logo dimension based clear space
  is really for print, we have a rule of thumb for digital is half of this dimension, but it
  isn't a rule, maybe we have it set as a floor of 0.25 snap-up to the 4px grid, so at 24
  height we have 8px as the floor fer the vertical clearspace, as long as it snaps to 4px
  above that I'm comfortable". ⚠ HIS NOTE SAYS **VERTICAL**. **HORIZONTAL clear space is NOT
  STATED AND IS NOT RULED** — it is carried open (W-282ll), never completed by symmetry. The
  logo-dimension clear space (`va25-014`, 1× hexagon height on all sides, `visual-assets.md`)
  remains the PRINT rule and is untouched. (s282-D5, Dave 2026-09-18) [BLOCKING — vertical
  digital clear space only; the horizontal axis has no rule to check against] {#logo26-009}
- **Horizontal digital clear space is a floor of 0.25 × the LOGOMARK's width — the hexagon alone, never
  the hexagon-plus-wordmark — snapped UP to the 4px grid, and it is applied on the OPEN side only, by
  alignment:** centred → the same floor on both sides; right-aligned
  → the floor on the LEFT only, zero on the right (the flush edge); left-aligned → the floor on the RIGHT
  only, zero on the left. Dave: "lets do horizontal clearspace at quarter width snapped up to the 4px.
  but this is zero on the left or right depending on alignment, centre - same both sides. right - only
  on the left. left - only on the right". Dave, correcting the first cut the same morning: "so the clearspace is defined by the logomark
  dimensions only, so it would be the same for both, the wordmark and logomark dimensions combined aren't
  applicable here". The hexagon is 2 × its height wide (170:85), so at the five steps it is 48 · 56 · 64 ·
  72 · 80 px wide ⇒ horizontal floors 12 · 16 · 16 · 20 · 20 px — THE SAME for the hexagon and the
  masterbrand at a given height. (The vertical floor of `logo26-009` is on height, which the logomark and
  the lockup share.) This completes `logo26-009`'s vertical floor; `W-282ll`'s
  horizontal half closes here. (s282-D6, Dave 2026-09-18) [BLOCKING — horizontal digital clear space,
  measured on the open side(s) per alignment] {#logo26-011}
- **The hexagon alone may be used on the nav-rail head, the app tile and the favicon** —
  each conditional on Create Direct approval AND "HSBC" in view (`va25-016`'s two conditions
  stand, unrelaxed) — **and in responsive layouts at the smaller sizes, tablet-portrait and
  mobile, where the Masterbrand does not fit.** Dave's words: "The pure logomark can also be
  used in responsive layouts when we get to smaller sizes, tablet-portrait and mobile". This
  answers `s230-D2`'s declared residue — "App-shell-nav-rail deliberately NOT rebound (56px
  rail head, no lockup fits)": a lockup now fits, and it is the hexagon.
  (s282-D5, Dave 2026-09-18) [ADVISORY — every use is gated on a human approval (Create
  Direct) that this repo cannot check, so it advises rather than blocks] {#logo26-010}

## Logos (2026 refresh — moved here from `brand-refresh-assets.md` by s282-D5)

- **An HSBC logo appears at least once on every piece of communication or customer
  journey.** In a native app the journey's logon or splash screen satisfies the rule —
  "the user summoned an HSBC app, they know where the destination is".
  (s282-D1, Dave 2026-09-17) [BLOCKING-derivable at journey/screen level — a composition gate candidate
  for the journey tranche; the payments-journey proof is where this bites first]
  {#logo26-001}
- **Originals only** (Global Brand Design supplied); never recreate/edit; always in
  entirety; never alter sizing relationship or positioning; must remain legible; TMLA
  process for third parties. [IN FORCE by discipline — the icon-source rule's logo
  analogue: never draw a logo, use the asset] {#logo26-002}
- **Masterbrand variants + selection rules:** full colour (red/black/white — LIGHT
  backgrounds) · full colour negative (red/white — DARK backgrounds) · single-colour
  variants (legibility-driven; NO white infill) · mono reversed (print only, dark/red) ·
  mono black (print only, light; never on HSBC Red). Never full-colour on a red
  background (hexagon disappears). [component-relevant — Headers carries the logo; dark
  theme should use full colour negative. Receipt: webf-008's 2021 phrasing ("alternative
  Masterbrand + white wordmark") = this variant, name evolved] {#logo26-003}
- **Regional/bilingual versions** (Trad/Simp Chinese ± English) follow identical
  sizing/positioning rules; region-text lockups restricted to legal-requirement cases.
  [reference] {#logo26-004}
- **Proposition logos** (Asset Management, Private Bank, Life, Innovation Banking) —
  never create one outside Group Brand agreement. **Identifiers** signpost products/
  departments/programmes in support of the Masterbrand. [structure] {#logo26-005}
- **Brand Promise "opening up a world of opportunity" is MANDATORY at Prime and Engage
  stages** (lock-ups with Masterbrand and proposition logos). [composition-level rule —
  marketing stages, not product UI; relevant only if generation ever targets
  Prime/Engage surfaces] {#logo26-006}
- **Partnerships:** hexagon alone where HSBC is well known; full Masterbrand where less
  known. End frames (logo + Brand Promise + sonic) close video content. [reference]
  {#logo26-007}

## Logos (2025 page — moved here from `visual-assets.md` by s282-D5; refresh-contaminated, see visual-assets F1)

- **Masthead contract: the Masterbrand logo appears in ALL digital mastheads;
  clicking it always returns to the root of the CURRENT business line** — never
  cross-line, orientation over surprise. ENGINE-CRITICAL → the Header/masthead
  component (deferred but queued) inherits this behaviour contract.
  [ADVISORY-derivable — header contract rule, exact] {#va25-015}
- **Never-rules: no new lock-ups from text for departments/programmes/products;
  never distort, recolour, reorient or recreate; hexagon-only use needs Create
  Direct approval AND 'HSBC' context nearby (app tile, profile avatar, favicon);
  never the legacy Times New Roman logo; third-party use follows the TMLA process;
  Brand Promise lock-up never wraps lines.** [ADVISORY — receipts; the
  official-assets curb already fixes logo-placed-never-drawn] {#va25-016}
- **Variant selection on photographic backgrounds: primary (red hexagon/white
  infill/black type) on light; white-wordmark version on dark-where-red-reads; mono
  black on light print, mono-reversed white on dark or HSBC-red; white infill never
  on mono versions.** Expands logo26's dark = full-colour-negative rule with the
  legibility ladder. [ADVISORY — variant-selection table; xref logo26]
  {#va25-017}

## Exported assets

SVGs exported to `knowledge/assets/logos/<lockup>-<light|dark>-<colour|mono>.svg` via
`_export-logos.py` (Figma `file_content:read` token). All 12 (now 8) came through as
**vector** (hexagon in `#DB0011`/white; masterbrand wordmark and identifier as vector paths)
— no embedded raster.

> Per the icons sourcing rule, treat these exports as **internal prototype assets**; for
> production/dev handoff, source official logo artwork from create.hsbc / the UI Centre.

## Cross-references

`brand-refresh-assets.md` (Photography + Creative Hexagons stay there; its Logos section
moved here) · `visual-assets.md` (`va25-014`, the PRINT clear space and minimum size, stays
there) · `web-foundations.md` (webf-008 dark-logo receipt ↔ logo26-003) ·
`_PAYMENTS-JOURNEY-GAPS.md` (logo26-001 lands with Headers) · `icons.md` (icon-003, app
tiles as a separate branding application) · `hexagon-masks.md` / `imagery.md` (2025-era
record) · `knowledge/_logo_nodes.json` (the 8 logo nodes this file governs).
