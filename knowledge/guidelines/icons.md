# Icons — brand guidance (ingested, engine era)

*Sources, two layers: (1) create.hsbc → Foundations → Icons and pictograms
(`icons-and-pictograms.html` hub + `icons-and-pictograms/Icons.html` standard), captured
2026-07-02 via Dave's authenticated session (login-walled; ADR-0005 provenance applies);
(2) HSBC Common Toolkit Figma capture 2026-06-17 (retained below — toolkit-level facts the
site doesn't carry). Upgraded 2026-07-02 from the pre-engine-era distillation: every rule now
tagged + ID'd. Related: `tokens/icon-scale.json`, `semantic-colour.json` (icon/*),
`assets/icons/` + manifest, `_ICON-GAPS.md`, icon-source gate (`_validate_icons.py`).*

## Asset-class definitions (hub)

Three-tier graphic system: **icons** (utility-driven, interactive, small, digital-only) ·
**pictograms** (idea-driven, not interactive, larger, digital+physical — see `pictograms.md`) ·
**illustrations** (narrative, photographic support — see `illustration-standards.md`).

- Icons and pictograms are **not interchangeable**; don't scale icons up in place of
  pictograms. [ADVISORY] {#icon-001}
- **Don't use illustrations as icons** (site echoes our icon-source rule at brand level).
  [BLOCKING-derivable — the icon-source gate already enforces library-only provenance] {#icon-002}
- Don't substitute product/3rd-party logos with icons; utility app icons are a separate
  branding application (App tile guidelines). [ADVISORY] {#icon-003}
- Avoid icons without labels unless universally recognisable ('home', 'save', 'search') —
  and verify the universal meaning with user testing. [ADVISORY-derivable — icon-without-label
  detector, allowlist of universals] {#icon-004}

## Structure

Icon anatomy: **icon** (the metaphor) + **label** (descriptor; omittable only for universals) +
**modifier** (overlay indicating specific meaning) + **badge** (passive notifier — Badges
guidelines) + **tappable area**.

- **Functional icons need a minimum 44×44px target area.** [BLOCKING-derivable — hit-area
  check; our 24px expander pattern on Tags/Tooltip targets WCAG 2.5.8's 24px, the brand
  standard asks 44 — ⚠ gate delta, see Findings] {#icon-005}

## Sizing

- Designed on an **18×18px grid, 1.2px line weight** (72dpi). [structure fact]
- **Minimum 16px, maximum 48px; scale proportionately in 2px increments.**
  [BLOCKING-derivable — rendered-size check] {#icon-006}
- Rationalise a standardised size set (e.g. 18/24/36/48) per toolkit/journey; don't use
  uneven scales. [ADVISORY-derivable] {#icon-007}
- **Match icon size to the accompanying text size**; don't pair dramatically differing
  sizes (see Links guidelines). [ADVISORY-derivable — icon:font-size ratio check; our chip
  em-sizing already implements the spirit] {#icon-008}
- **Thicker-weight variants** (1.8px on the same grid — Figma layer) exist for use below
  16px, e.g. combined with text; chevrons + some status icons. **Only thicker chevrons
  alongside text links.** [ADVISORY-derivable] {#icon-009}
- Some icons ship **cropped** for text alignment (e.g. chevron-right 11×16 — spare canvas
  removed). [structure fact; relates to our leading-trim label alignment work]

## States

- Default state = simple lines; **active state = solid fill**; not all icons have active
  variants (manifest flags `active: true`). [structure fact]
- When icons indicate a function, **use the active version to differentiate default vs
  selected**; colour may support the distinction. [ADVISORY-derivable — states-completeness
  probe class; relates to `_ICON-GAPS.md` download-active gap] {#icon-010}

## Accessibility

- **Icons require 4.5:1 contrast in all instances** — "like text", labelled or not.
  [BLOCKING-derivable — ⚠ gate delta: our icon checks target 3:1 (WCAG 1.4.11); the brand
  standard is stricter. Enters advisory until Dave rules on promotion — see Findings]
  {#icon-011}
- Code: icon **with** label → `alt=""` (null); icon **without** label → `alt` = icon name.
  [BLOCKING-derivable — alt-attribute pattern check on snippets] {#icon-012}
- RAG-coloured notification/status icons: maintain contrast against actual background;
  **never colour alone** for status — supporting information required. [BLOCKING-derivable —
  1.4.1 gate + indicator-contrast gate already cover this] {#icon-013}

## Sourcing (Figma-capture layer, 2026-06-17 — still operative)

- **"Do not export SVGs from the HSBC Icon Library file or artwork files. Download the SVGs
  from the UI Centre for sharing with development."** Our Figma-exported catalogue
  (`assets/icons/`) is for internal knowledge-base prototyping only; dev handoff sources from
  the UI Centre. [ADVISORY — process rule] {#icon-014}
- Library groups: Miscellaneous, Social, Touch, Informative, Volume/audio, Media,
  Arrows/chevrons, Products and services, Global controls, Status. Site gallery adds per-
  category downloads (Status+notifications, Global controls, Products+services, Chevrons,
  Media, Video+audio, Informative, Touch).
- Toolkit tokens: sizes `icon-scale.json` — xsmall 12 / small 18 / medium 24 / large 36;
  colours `semantic-colour.json` icon/* (default #333333/#FFFFFF, disabled, default-reverse);
  catalogue uses `currentColor`.

## Findings (2026-07-02 upgrade)

1. **Icon contrast: 4.5:1 vs our 3:1.** The hub states icons need 4.5:1 "in all instances"
   because they're interactive and legibility-critical; pictograms 3:1 (+ descriptive alt).
   This RESOLVES the `col26-007` REVIEW item (brand page "text and icons 4.5:1" vs supporting
   page "graphics 3:1"): differentiated by asset class — **icons 4.5 · pictograms 3 ·
   chart/RAG indicators 3**. Gate impact: our text/icon contrast audit passes icons at 3:1;
   raising to 4.5 is a stricter-than-WCAG brand rule → advisory first, Dave rules on
   promotion. ◐ ADVISORY BUILT 2026-07-02 (Dave ruling: evidence before promotion) —
   `_build_icon_contrast_delta.py` (build step 12/18) → `_ICON-CONTRAST-DELTA.md`.
   Evidence: **0 declared icon pairs in the 3–4.5 dead zone** (all 18 pass 4.5 with
   headroom — promotion cost for true icon/* pairs is ZERO); 17 exhaustive upper-bound
   combos (all icon/disabled, allowlisted, or non-co-occurring).
   ✅ RAG CLASSIFICATION RULED 2026-07-02 (eve, Dave) — the roundel policy:
   **roundel vs surface ≥3:1** (indicator class) · **internal mark vs roundel fill
   ≥4.5:1** (small-text analogue) · **dark mode: roundel goes WHITE with a BLACK mark**
   (icon + label carry meaning; colour is not the channel). Consequences, computed:
   all dark dead-zones dissolve structurally (white/black = 21:1, white roundel on dark
   bg 21:1); light-mode audit — error knockout 7.13 ✓, info knockout 6.21 ✓, warning
   already dark-marked #333 = 7.47 ✓ (the "amber needs a dark mark" comment was this
   policy avant la lettre), **success tint-knockout 3.98 ✗ → mark must go white (4.56 ✓)**.
   ✅ AMBER EXEMPTION RULED 2026-07-02 (eve, Dave): the warning roundel's light-mode
   roundel-leg failure (1.69 on white, 1.60 on warning-tint) is an ACCEPTED CONVENTION —
   yellow-on-white is always problematic, but amber-means-warning is the established
   signal. Consistent with the policy's own logic (mirrors the dark-mode stance): the
   INTERNAL MARK's contrast is the priority (#333 mark = 7.47 ✓) and icon + label are
   sufficient for meaning; the roundel colour is not the channel. Inconsistent on the
   roundel leg, exempt by ruling. ✅ IMPLEMENTATION REVIEWED + PASSED 2026-07-02 (eve,
   Dave, live HTML): Notifications + Confirmation pass; Input-fields passed with three
   review fixes (interactive tail icons, dark error border → red, rest-state centring)
   and is flagged a **supercharge** (brand-uplift rework) candidate — expect change.
   Remaining tail: (a) formally promote the 4.5 icon threshold into the blocking gate
   (evidence says cost = 0) and (b) mechanise the mark-vs-roundel check once marks are
   tokenised — both sensibly deferred to supercharge. [REVIEW — gate promotion + mark
   tokenisation, deferred to supercharge] {#icon-015}
2. **Size floor tension.** Site: minimum 16px (thicker-weight set below that). Toolkit
   tokens: `xsmall = 12px`. Consistent only if xsmall implies the thicker-weight set —
   toolkit doesn't say. [REVIEW — check the design toolkits' icon sizing page] {#icon-016}
3. **Max-size tension.** Hub: "three sizes 18/24/36, never scaled larger." Standard page:
   max 48, example set includes 48. Deeper page wins provisionally (48), but the source
   disagrees with itself. [REVIEW — Create Direct query] {#icon-017}

## Cross-references

`pictograms.md` (companion class) · `illustration-standards.md` (illustration ≠ icon) ·
`colour-standards-2026.md` col26-007 (contrast resolution) · `_ICON-GAPS.md` +
`_ICON-SOURCE-AUDIT.md` (gate) · dynamic-weight icon exploration
(`assets/icons/dynamic-weight/`) — the thicker-weight-below-16px rule is the brand's own
precedent for weight-varies-with-size.
