# Common Toolkit — FOUNDATIONS pages (delta pass, not a re-ingestion)

*Provenance: Figma file `mI8hvIkV98nquoqWzKh5Kn`, the 10 FOUNDATIONS pages,
captured 2026-07-03 (bridge text extraction, U+2028-safe). CRITICAL TRIAGE
FINDING: most of this tranche was ALREADY in the register — `dark-mode.md`,
`elevation.md`, `logos.md`, `hexagon-masks.md` were captured from these exact
pages 2026-06-17; `icons.md` is dual-sourced (toolkit 06-17 + create.hsbc
07-02); `web-foundations.md` / `app-foundations.md` / `typography-usage.md`
carry the grid/type/spacing doctrine from create.hsbc (which these pages'
Standard frames mirror). This file therefore records ONLY: source receipts for
existing rules, genuinely new numerics (masthead-flyout grid, email grid, app
grid, type-tier clauses), two dark-mode clauses the 06-17 summary apparently
dropped, and census/hygiene facts. Surfaces: Breakpoints page 471:15986 (Web
13967:90189 · Email 13967:90253 · App 13967:90228 components + 00 Standard
46059:40308) · Font 0:1 (2623:87015 + 2 Standards) · Spacing 475:16246 ·
Colour tokens 11:116 (5 collection frames + swatch-only semantic column) ·
Dark mode 46025:22918 (00 Standard 46025:22919) · Image 866:22335 · Icons
2107:29115 (guide 2408:94857 + CHANGE LOG 8242:4280 + 12 inventory frames,
~3,240 text nodes not re-extracted) · Elevation 873:34991 · Logos 29:1009 ·
Hexagon masks 960:26374. Fifth `ctk*` file — closes tranche 1.*

## Grids and breakpoints

- **Web breakpoint table receipted at source** — Extra Small 320–479 (12 col,
  16px margins/gutters, scale-1) · Small 480–759 (12/16/scale-1) · Medium Small
  760–959 (12/20/scale-2) · Medium 960–1279 (12/20/scale-2) · Large 1280–1599
  (12/40/scale-3) · Extra Large 1600+ FIXED (12/40/scale-3, marketing-only).
  Content fixed at 1280 for most sites beyond Large; XL needs design-lead
  sign-off. [IN FORCE — matches layout.json + webf-026/027 doctrine; the
  per-breakpoint margin/gutter values and the breakpoint→scale map are now
  receipted at component level] {#ctkf-001}
- **Masthead + footer ride a grid VARIANT: identical to the main grid but it
  stays FLUID beyond 1600px** (the main content area goes fixed at XL).
  [ADVISORY — composition-layer contract; NEW — not in webf; matters the moment
  the Headers/Navigation tranche composes a masthead] {#ctkf-002}
- **The masthead FLYOUT has its own grid: 4 columns at every breakpoint; margin
  0 with gutter 16px (XS/S) or 20px (MS/M); margin 40px with gutter 0 (L/XL);
  breakpoints and scales as main.** [ADVISORY — NEW numerics, nothing in the
  register covers flyout grids; direct input to the deferred Headers/Nav
  revisit] {#ctkf-003}
- **Email grid** (out-of-engine channel): Small 320–479 = 6 columns / 16px
  gutter / 22px margin / scale-1 · Medium 480–767 = 12 / 20 / 45 / scale-1 ·
  Large 768+ = content FIXED at 768px, background grows; scale-1 across all
  tiers. [RECORDED — email channel; the only 6-column grid in the estate;
  channels-batch kin] {#ctkf-004}
- **App grid: one tier — 320+px, 12 columns, 16px gutter/margins/padding,
  scale-1 always** ("non-responsive apps and emails only use scale-1 … helping
  to achieve dense or more compact layouts"). [RECORDED — app platform (Q2);
  explains why app comps look tighter than web at desktop sizes] {#ctkf-005}

## Type and spacing

- **The full font matrix is receipted at source**: font-1…4 responsive across
  scale-1/2/3 (e.g. font-1: 33/40 → 44/50 → 57/66 px size/line), font-5…7
  FIXED across scales (16/24 · 14/20 · 12/16), each with px AND em
  specifications (size/line/paragraph/letter-spacing) and light/regular/medium
  weights. Scales are markup-agnostic (a font-1 could be an H1, display number
  or quote). [IN FORCE — the token store (native export) carries these values;
  the em table + markup-agnostic doctrine are the source receipts; TScale
  naming (TScale:1 = 320–959 · :2 = 960–1599 · :3 = 1600+ marketing) already in
  webf] {#ctkf-006}
- **New type-tier clauses not yet in the register**: 12px (font-7) is RESERVED
  for terms and conditions, disclaimers and legal copy (eg site footer) ·
  S-sizes may be applied as H1–H4 only "if semantically correct to do so" ·
  medium weight may highlight words/phrases but NOT long paragraphs (and can
  mimic a subtitle without a size bump) · TScale:1-only is for
  NON-CONSUMER-FACING high-density projects. [ADVISORY — the 12px-legal
  reservation and medium-weight-paragraph ban are lintable; merge into
  typography-usage.md at its next touch] {#ctkf-007}
- **The spacing ramp is receipted at source**: space-0…space-12 across
  scale-1/2/3 with graded increments (+2 at the small end, +4 through the
  middle, +8 from space-10) — e.g. space-4: 16→20→24; space-12: 48→56→64.
  R-units for layout/large elements; FIXED spacing for small elements (buttons,
  tabs, inputs); the fixed-spacing example spec shows the Notification's
  9px/11px pads — the same values the Notifications set census surfaced
  (padding/responsive/xxsmall 9 · xsmall 11). [IN FORCE — token store carries
  the values; the ramp table + the cross-receipt with the component census are
  the news] {#ctkf-008}

## Dark mode — two clauses the 06-17 capture dropped

- **Light-bleed compensation**: strong light-on-dark contrast makes type and
  icon strokes appear HEAVIER (light spills into the dark background) —
  counteract by reducing contrast (light grey text, lowered white opacity, or
  lighter background) while still meeting contrast standards. **And: dark
  layouts feel more closed-in than light ones with identical negative space —
  introduce MORE negative space in dark mode.** [ADVISORY — neither clause
  found in dark-mode.md at grep (bleed/negative-space); suspected
  summarisation loss at the 06-17 pass — merge into dark-mode.md at its next
  touch; the bleed rule bears on dark-mode type rendering checks] {#ctkf-009}

## Elevation, icons, colour, image — receipts and census

- **The elevation LEVEL table with named assignments**: 0 = base content (never
  elevated) · 1 = sticky content (top nav, drawer, tooltip) · 2 = modality
  (partial modals, dialogs) · 3 = notifications (snackbars). Directly receipts
  ctkn-011 (snackbars above modals+nav = level 3 > 2 > 1). Overlays come as
  Overlay 50 and Overlay 85; scroll-conditional shadows (no scrollable content
  → no shadow). [IN FORCE — elevation.md already carries the doctrine; the
  numbered level→pattern assignments are the receipt] {#ctkf-010}
- **The icon library is LIVE while its guides are frozen**: the Icons page
  carries a full CHANGE LOG — ~50 additions/amendments dated 2024-05 through
  **2026-04-08** (ai · clickToPay · worldTrader · emoji · controlStop ·
  mastheadHide/Show · sidePanelLeft/RightOpen/Close · addAlert (pairs with the
  Add Alert component, ctkn-002) · a health/insurance vocabulary wave ·
  socialX renamed) — against guide vintages stuck at "0.0.0 | May 2023". The
  sharpest layered-vintage receipt yet (td-002 extension); the masthead/
  sidePanel icon vocabulary is directly relevant to the Headers/Nav tranche.
  [RECORDED — census fact + maintenance-cadence signal; icons.md icon-014
  (UI-Centre-only distribution) re-receipted verbatim on this page] {#ctkf-011}
- **Brand colour collection structure receipted**: Core / Data visualisation /
  RAG / Illustration frames, plus DARK-MODE-ONLY RAG TINTS
  (rag-dark-red-tint #260005 · amber #221701 · green #001615 · blue #000D1B) —
  and NO dark-mode SOLID RAG accents exist in the brand collection: the ds-001
  gap (dark rag/information aliasing a missing blue/400) is a SOURCE-side
  absence, not an export artefact. The "Colour tokens semantic" frame is
  swatch-only (ZERO text nodes — not text-capturable, td-015); the "Colours
  components" frame carries CSS-var naming debris ("var (--…"). [RECORDED —
  strengthens the ds-001 receipt chain; native variable export remains the
  operative source] {#ctkf-012}
- **Image + hexagon census**: a fixed-ratio `Image` component set exists
  (aspect ratios 1:1 / 4:3 / 16:9 / 21:9 / 3:1 × Keyline true/false) plus
  fixed-height left/centre/right crop patterns — canon has NO image component
  (vocabulary note; visual-assets ratio rules kin). Cropped Hexagon sets =
  Version (top/middle/bottom) × Side (left/right) at five aspect ratios —
  single-edge crops only, CONSISTENT with hex26-002 (3-/4-edge crops retired).
  [RECORDED — census facts; hexagon vintage check passes again] {#ctkf-013}
- **The toolkit flags its own divergence**: the Breakpoints page carries a
  "Please note" — "The breakpoints follow the Common Toolkit, but scale have
  applied differently compared to Common Toolkit" (sic) — a toolkit page
  declaring it applies scales differently from the toolkit it lives in
  (td-014). Also: the Icons guide claims thick-weight icons share an "18x8px
  grid" — suspected typo for 18x18 (icons.md carries the correct 1.8px-weight
  rule). [RECORDED — hygiene; provenance for future confusion] {#ctkf-014}

## Findings

- **F1 — the tranche was already two-thirds ingested**: the 06-17 Figma batch
  (dark-mode, elevation, logos, hexagons, icons) + the 07-02 create.hsbc
  ingests (web/app foundations, typography) had this covered. The honest
  output is receipts + deltas, not 10 pages of re-distillation — set-census
  discipline (td-010) applied to ourselves.
- **F2 — three NEW grids entered the register**: masthead/footer fluid-XL
  variant (ctkf-002), the masthead-flyout 4-column grid (ctkf-003), and the
  email 6-column grid (ctkf-004, RECORDED). The flyout grid is the one the
  Headers/Nav revisit will actually need.
- **F3 — capture-loss check works**: two real dark-mode rules (light-bleed
  compensation, extra negative space) never made it into dark-mode.md
  (ctkf-009). The 06-17 summaries were good but lossy — worth a one-pass
  re-grep of the other 06-17 files against their source pages at some point.
- **F4 — the ds-001 chain is now source-complete** (ctkf-012): dark solid RAG
  accents don't exist in the brand collection itself. Canon's interim dark
  treatment isn't diverging from the source; it's filling a hole the source
  acknowledges by omission.
- **F5 — living library, frozen guides** (ctkf-011): the icon change log ships
  monthly updates into 2026-04 while every guide reads "May 2023". The
  layered-vintage thesis (td-002) now has its cleanest exhibit — and the
  change log itself is a maintenance-cadence signal the reconciliation story
  can cite.
