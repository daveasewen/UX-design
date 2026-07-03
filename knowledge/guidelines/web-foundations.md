# Web foundations — platform guidance (ingested)

*Source: create.hsbc → Platforms and channels → Web → Web foundations
(`platforms-and-channels/web/web-foundations/` — six subpages: dark-mode, Elevation,
responsive-forms, Responsive_grid, type_scale, spacing), captured 2026-07-02 via Dave's
authenticated session (login-walled; ADR-0005 clearance applies — agency machine).
Engine-era format. Capture notes: dark-mode page is dated **18 April 2021** (pre-refresh);
the other pages are undated but read as the same generation. Do/Don't figures are images —
their captions were captured, the visuals were not. The responsive-forms link now redirects
to a migration stub (see webf-017). Raw capture snapshots for all six pages:
`guidelines/_sources/web-foundations/` — review capture-vs-encoding there.*

## Scope note

These are the WEB channel foundations — the platform-specific layer that sits beneath our
components. Much of it is already enforced in the engine (dark-surface gate, dual-mode
tokens, breakpoint/scale modes); the value here is (a) receipts for what we already do,
(b) the elevation level taxonomy, and (c) four genuine tensions logged in Findings.

## Dark mode (browser) — 2021 page

- **Not a straight inversion.** Swap light backgrounds to dark; keep already-dark
  backgrounds dark; don't introduce new layers or unnecessary elements; don't invert
  already-dark to light. [IN FORCE — `_validate_dark_surfaces.py` bites on flat white;
  dual-mode tokens carry the rest] {#webf-001}
- **Dark surfaces come only from the dark-backgrounds palette** (or the programme
  toolkit). [IN FORCE — token discipline; store greys are the operative source] {#webf-002}
- **Limit colour, especially HSBC red, in dark mode** — replace some light-mode colour
  with white/grey; red kept strategic (primary CTA, hexagon). Every use of red evaluated.
  [TASTE at generation time; register-relevant — see Findings webf-029] {#webf-003}
- **Use adjusted (darker/desaturated) colour values in dark mode**; never the same
  bright/rich values across both modes (visual vibration). [IN FORCE for most tokens —
  but this is exactly what `dark-rag-token-gaps` records as BROKEN for success/warning,
  which don't darken. This page is the brand-side receipt for that fix] {#webf-004}
- **Dark elevation = lighter surfaces higher.** Depth in dark mode reverses: higher level
  = lighter surface. Overlays still work; shadows are weak alone and may need combining
  with a lighter surface. [IN FORCE — matches our dark-surface elevation approach]
  {#webf-005}
- **Light-bleed compensation.** Strong light-on-dark makes type/icon strokes look heavier;
  counteract with light grey, lowered white opacity, or lighter background — but contrast
  must still pass accessibility. [ADVISORY-derivable — a dark-mode text-tone check;
  kin of `text/on-inverse`] {#webf-006}
- Accessibility callout on colour adjustment: "Maintain a 3:1 contrast ratio" (callout
  truncates on-page; read within the settled framework — text 4.5, icons 4.5 (promoted),
  graphics/UI 3). [receipt for existing gates] {#webf-007}
- **Imagery in dark mode:** photography must complement the dark setting (no overly bright
  imagery; low-opacity dark overlay where asset-switching isn't viable); illustrations —
  consider edges/containment, swap assets contextually where possible, use dynamic assets
  (opacity zones, SVG colour-swaps); avoid PNG/GIF transparency choppy edges, prefer SVG.
  Hexagon on dark = SVG + alternative Masterbrand/white wordmark. [pattern-level; asset
  pipeline — mostly out of engine scope today] {#webf-008}
- **Behaviour: follow the system dark-mode preference**; optionally offer more granular
  in-platform override. [component-relevant — our theme mechanism honours data-theme;
  system-preference detection is a composition-layer concern] {#webf-009}
- **Dark mode needs more negative space** — dark backgrounds make the same layout feel
  more closed-in. [TASTE — interesting generation-time signal, dark variants may warrant
  looser spacing] {#webf-010}

## Elevation

- **Level taxonomy: 0 = base content** (body, imagery, cards, buttons — NEVER elevated) ·
  **1 = sticky content** (top navigation, drawer, tooltip) · **2 = modality** (partial
  modals, dialogs) · **3 = notifications** (snackbars). Elements contained within a level
  do not display further elevation. [BLOCKING-derivable — a component→level map is
  checkable at compose time; component-relevant for Headers (deferred), Modal, Tooltip,
  Notifications] {#webf-011}
- **Shadow = specified depth** (higher level → deeper shadow); **overlay = large,
  unspecified depth, used to focus**. Never display both on the same element/pattern.
  [ADVISORY-derivable] {#webf-012}
- **No purely aesthetic shadows** (inner or outer) — elevation is functional. [BLOCKING-
  derivable; kin of the refresh's flatness discipline — see Findings webf-030 for the
  token-name tension] {#webf-013}
- **No elevation on patterns that move within level-0 content** (e.g. an accordion pushing
  content down). [ADVISORY-derivable] {#webf-014}
- **Consistency: same pattern, same elevation, everywhere**; never use shadow to
  differentiate elements on the SAME level (overlap is fine for styling). {#webf-015}
- **Scroll-triggered elevation:** top nav defaults to no shadow, gains it when content
  scrolls beneath; bottom nav / sticky button container shows shadow only if the page is
  scrollable (conditional on load). [component-relevant behaviour spec — Headers/sticky
  patterns; triggers: on-appearance and on-scroll] {#webf-016}

## Responsive forms — MOVED (migration stub)

- The responsive-forms URL redirects to an "Elements and patterns (web and app)" stub:
  element/pattern standards (buttons, accordions, app tiles…) now live in the **Common
  Toolkit**; "the Design Toolkit remains the single source of truth" for interaction
  states, accessibility requirements, usage rules, specifications. ⚠ Source gap: forms
  standards are not reachable as a page; the Common Toolkit is an asset/toolkit
  destination, not an ingestable standard. PROBED 2026-07-03 (Dave's session):
  "Explore the Common Toolkit" → **Figma file `HSBC-Common-Library`
  (`SuVpEaqQcXDP3CYkFKBIeE`) — MCP refused: needs EDIT access** (Dave's HSBC
  enterprise seat is full, but per-file editor access is missing). The proven
  route REMAINS OPEN: the Common Toolkit "Gaps and edits" branch
  (`Cgbtrmfp15ruNFkIAClpkI`) is fully MCP-reachable (re-verified live, Logos page
  node 29:1009). NEXT: Dave checks whether HSBC-Common-Library is new content or
  a republish of his branch; if new, request editor access. [REVIEW — probe done;
  close when the Common-Library-vs-branch question is answered] {#webf-017}

## Responsive grid

- **Base unit 4px** for horizontal and vertical measurement — "normally express this unit
  in multiples of 8, however multiples of 4 can be used as a fallback". [BLOCKING-derivable
  spacing check kin — see Findings webf-032] {#webf-018}
- **12-column grid.** Standard max content width ≈1280px incl. 20px margins; keep 20px
  gutters to align with the standard HSBC header/footer; significantly wider content →
  24px or 32px gutters. [structure — matches `layout.json` (12 columns, breakpoints)]
  {#webf-019}
- **Final breakpoint behaviour:** beyond it, columns/gutters stop growing; margins alone
  grow; content stays fixed and centred. Adaptive beyond-1280 layouts = talk to Digital
  Standards. [structure] {#webf-020}
- **Content reflow:** mobile-first is common but medium/large need design intent too;
  weigh image significance across viewports; **responsive tables collapse columns into
  stacked label/data pairs per row**. [component-relevant — Table's responsive behaviour
  spec] {#webf-021}
- **Off-grid content:** modals, tooltips, overlaying content are independent of the grid;
  expanded margins on wide viewports may host otherwise-hidden tools (vertical nav,
  filters). [structure] {#webf-022}

## Web type scale

- **7 sizes anchored on a 16px baseline**, three viewport variants: **TScale:1 =
  320–959px · TScale:2 = 960–1599px · TScale:3 = 1600px+**. Default responsive = TScales
  1–2 (max content 1280); marketing sites >1280 may add TScale:3; **non-responsive
  TScale:1 only, for non-consumer high-density projects**. [structure — matches
  `layout.json` scale-1/2/3 mode mapping exactly] {#webf-023}
- **The size table** (font / leading / paragraph-spacing, px):

  | Size | TScale:1 | TScale:2 | TScale:3 |
  |---|---|---|---|
  | S1 | 33 / 40 / 20 | 44 / 50 / 25 | 57 / 66 / 33 |
  | S2 | 28 / 36 / 18 | 35 / 42 / 21 | 43 / 52 / 26 |
  | S3 | 23 / 30 / 15 | 28 / 36 / 18 | 32 / 42 / 21 |
  | S4 | 19 / 27 / 14 | 22 / 31 / 16 | 24 / 31 / 16 |
  | S5 (baseline) | 16 / 24 / 12 | 16 / 24 / 12 | 16 / 24 / 12 |
  | S6 | 14 / 20 / 10 | 14 / 20 / 10 | 14 / 20 / 10 |
  | S7 | 12 / 16 / 8 | 12 / 16 / 8 | 12 / 16 / 8 |

  S5–S7 are invariant across TScales — and match `typography.json` font-5/6/7 EXACTLY
  (sizes, line-heights, paragraph spacing). S1–S4 vary per TScale → they are the store's
  font-1..4, whose sizes must be TScale-mode-dependent (see Findings webf-033).
  [reference table] {#webf-024}
- **Hierarchy:** Light/Regular/Medium weights build hierarchy; titles/section headers/
  subtitles use S1–S4 (≥19px), applied as H1–H4 where semantically correct; page titles
  use light + regular; **16px recommended body on public-facing sites**; **12px reserved
  for T&Cs / disclaimers / legal**; medium weight for highlighting words/phrases, not long
  paragraphs. [ADVISORY-derivable — a type-role check at generation time] {#webf-025}
- **Line length 60–80 characters**; never full page width on wide layouts. [ADVISORY-
  derivable — measurable at render time; good candidate for the visual-QA loop] {#webf-026}

## Spacing

- **All spacing in multiples of 4**, mapping to grid margins/gutters; padding/margins
  follow the system (e.g. 16px gutters → 16px card side-padding). [BLOCKING-derivable —
  see webf-032] {#webf-027}
- **Two spacing types:** **responsive (RScale:1/2/3** — same breakpoints as TScale;
  RScale:3 marketing-only**)** for layout and larger patterns (tiles, image/text gaps,
  cards, tables, expanding containers); **fixed** for small elements where cross-viewport
  consistency matters (button padding, radio-to-label). Both may coexist on a page.
  [structure — see Findings webf-034: R-unit VALUES are a source gap] {#webf-028}

## Findings

1. **Pre-refresh vintage.** The dark-mode page is dated 2021 and the family reads
   pre-refresh. Its "limit red / replace colour with white-grey" conservatism sits oddly
   against the 2026 refresh's expressive direction (dual-live palettes, charter §4) — the
   living-standard caveat applies: deltas ≠ defects; reconcile when the web pages re-issue
   under the refresh. [REVIEW — vintage reconciliation, no action until re-issue]
   {#webf-029}
2. **"No purely aesthetic shadows" vs `elevation/decorative`.** webf-013 bans decoration-
   only shadows; our store carries `elevation/decorative` (blur 8) alongside
   `elevation/functional` (blur 16) — from the Figma export. Likely the toolkit means
   "decorative" as a lighter functional tier, not aesthetic-only, but the name collides
   with the standard's language. [REVIEW — naming/semantics check at next Figma re-base;
   don't rename unilaterally] {#webf-030}
3. **Body leading contradiction, cross-standard.** This page: S5 body = 16/24 = **1.5**
   leading (and our store matches). typography-standards-2026 (type26-016): Latin body
   leading "**1.1×**" with worked examples at 1.29–1.33×. Three sources, three ratios —
   strengthens the type26-016 suspicion that "1.1×" is a misprint or channel-specific.
   The web scale + our store agree at 1.5 for web body; operative. [REVIEW — fold into
   the type26-016 reconciliation] {#webf-031}
4. **`gap/fixed/content/xxsmall = 2px` breaks the 4px base unit.** The standard says
   multiples of 8, fallback 4; the toolkit export carries a 2px gap. Toolkit-wins stance
   (grey ramp, icon sizes) says keep it operative, but it's a real toolkit-vs-standard
   contradiction. [REVIEW — same class as icon-016; prune or exempt at refresh
   settlement] {#webf-032}
5. **font-1..4 sizes are TScale-mode-dependent — check the export carries them.**
   `typography.json` has fixed sizes only for font-5..7 (correct — S5–S7 are invariant);
   font-1..4 sizes/leading must vary by scale mode. If the semantic-scale export didn't
   carry per-mode type values, large-type generation at scale-2/3 is running on a gap.
   [REVIEW — verify at next token re-base; engine check: does anything resolve font-1..4
   sizes today?] {#webf-033}
6. **Responsive spacing values (R units) are a source gap.** `spacing.json` is fixed-only;
   the RScale VALUES per breakpoint aren't in the store or on this page (likely toolkit-
   internal). Generation currently has no responsive-spacing dimension. [REVIEW — pair
   with webf-033 at the next export/re-base] {#webf-034}
7. **Match receipts (provenance confirmation):** breakpoints 320/480/760/960/1280/1600 and
   scale-1/2/3 viewport mapping in `layout.json` = this page's TScale/RScale bands exactly;
   12 columns ✓; S5–S7 = font-5..7 ✓ (all nine numbers). The store and the standard are
   the same system where they overlap. [structure note] {#webf-035}

## Cross-references

`_DARK-MODE-AUDIT.md` + `_validate_dark_surfaces.py` (webf-001/005 enforced) ·
`dark-rag-token-gaps` memory + `_INDICATOR-CONTRAST-AUDIT.md` (webf-004's broken case) ·
`tokens/layout.json` (breakpoints/scales/columns) · `tokens/typography.json` (S5–S7) ·
`tokens/spacing.json` (fixed gaps; webf-032/f6) · `tokens/elevation.json` (webf-030) ·
`typography-standards-2026.md` (type26-016 ↔ webf-031) · `icons.md` (contrast framework) ·
Common Toolkit (webf-017 — access decision pending).
