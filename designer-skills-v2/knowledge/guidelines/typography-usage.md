# Typography (2025 standard) + creative headline — brand guidance (ingested)

*Source: create.hsbc → Foundations and identity → Typography
(`foundations-and-identity/typography.html` + subpages `creative-headline.html`,
`placement.html`, `latin-languages.html`, `app_type_scale.html`), captured 2026-07-02 via
Dave's authenticated session (login-walled; ADR-0005 clearance). Raw snapshots:
`guidelines/_sources/typography-2025/`. **UPGRADED to engine era 2026-07-02** — this file
replaces the 2026-06-18 legacy distillation; the 2026 refresh standard lives in
`typography-standards-2026.md`. The page opens with the "We're supercharging our brand"
banner: the 2025 standards below remain usable "until further notice" (parallel-valid).
The app_type_scale subpage is a word-for-word duplicate of the app-foundations page
(appf-001 receipt). Note for the record: "supercharge" — Dave's codename for the
brand-uplift rework — is HSBC's own banner language.*

## Scope note

The 2025 typography standard + the creative-headline system (the expressive-register
typographic vocabulary: big-and-light / small-and-bold / thin, hexagon interaction).
Canon compliance was spot-checked at ingestion: no italics, no text-shadow, text tokens
are black/grey/white only, weights match the licensed five exactly — every hard rule
below is already met (receipts marked). Hexagon composition rules are fenced to the
future composition/journey experimentation strand. 2025↔2026 deltas are logged on the
2026 side (type26-025/026/029).

## Core rules (main page)

- **Brand-approved fonts, weights and colours only.** Licensed portfolio: Univers Next
  for HSBC (+ M Ying Hei PRC/HK for Chinese, Tazuane Gothic for Japanese, Univers Arabic).
  [IN FORCE — single-stack canon; store matches] {#type25-001}
- **All text ≥4.5:1.** [IN FORCE — text-contrast gate; dual-source with the col26-007/
  icon-015 framework] {#type25-002}
- **Never red typography for headlines or body copy** — red only for text links (CTAs)
  and "specific digital toolkit use-cases". [BLOCKING-derivable — text-token colour-role
  check; receipt: our text/* tokens are #333/#545454/#FFF/#D7D8D6 only, cost 0. Same rule
  family as type26's black/grey/white-only] {#type25-003}
- **Five weights only: Thin, Light, Regular, Medium, Bold; never Condensed.** [IN FORCE —
  store carries exactly 100/300/400/500/700 ✓; see type26-023 for the refresh's "Ultra
  Light" question] {#type25-004}
- **Readability numbers: body line length 60–80 Latin characters (avg); headline length
  20–50 characters (avg); no orphans** (single word alone on the last line of a heading/
  paragraph)**; no widows** (word/short group starting a new column or page).
  [ADVISORY-derivable — line length pairs with webf-026 (dual-source); orphan/widow
  detection is a render-time visual-QA candidate] {#type25-005}
- **Sentence case only — never all-caps or title case.** [ENACTED — the type26-019
  blocking gate; this 2025 page is the second source] {#type25-006}
- **No italics** — not licensed, and harder to read, especially for people with dyslexia.
  [BLOCKING-derivable — `font-style:italic`/`<em>`/`<i>` scan; receipt: zero occurrences
  in canon, cost 0] {#type25-007}
- **Emphasis = Univers Bold only, keywords/phrases not sections.** No underline for
  emphasis (underline = links only — neuro-007 dual-source) · no shapes/graphic devices ·
  **no drop shadows on text** · no outlines or graphic styling on type. [BLOCKING-
  derivable — `text-shadow` scan; receipt: zero occurrences in canon, cost 0. Bold-scope
  leg pairs with neuro-022] {#type25-008}
- **Type colour: dark-on-light, light-on-dark; no highlighted type blocks; no long-form
  copy on red or coloured backgrounds; consider size/scale for headline type on coloured
  backgrounds.** [ADVISORY-derivable — long-form-on-coloured-surface check; kin of the
  parked text-on-gradient family] {#type25-009}
- **Left-align text wherever possible** — best readability. [IN FORCE — house style;
  pairs with type26's no-justify] {#type25-010}

## Creative headline system

- **Creative headline weights: Thin, Light, Bold ONLY** (no Regular/Medium at headline
  level). Two treatments: **big-and-light** (Univers Light; big, meaningful; may slightly
  overlap the Creative Hexagon; predominantly left-aligned) and **small-and-bold**
  (Univers Bold; smaller size; ALWAYS left-aligned). **Thin = large formats only**
  (billboards). Never combine big-and-light with small-and-bold; never split a headline
  along the same axis. Brand Effect Model scope: Prime/Engage/Connect only — digital
  product surfaces use the type scale, NOT creative headlines. [composition vocabulary —
  the expressive register's typographic dial; see type26-029 for the refresh's
  replacement constructs] {#type25-011}
- **Headlines get breathing space** — keep body copy apart from creative headline
  typography. [TASTE/composition] {#type25-012}
- **On photography:** never black-on-dark or white-on-light imagery; create contrast by
  colour-treating the ASSET (subtle, natural) — never by treating the TEXT (no drop
  shadows, stroke outlines, vignettes). Contrast targets: 3:1 large text AA · 4.5:1
  smaller AA · 7:1 AAA. ["fix the asset, not the text" — a portable generation
  principle; softened by the refresh to permit subtle overlays, see type26-026]
  {#type25-013}
- **"Don't overlay text on gradient backgrounds"** — verbatim in the 2025 standard too.
  SECOND SOURCE for the parked type26-015; the parked ruling (gradient surfaces
  text-free until the finessing pass) now rests on both standards. [receipt → type26-015]
  {#type25-014}
- **Hierarchy: lead with a short, instantly understandable headline** + concise body;
  sub-headings distinct from both; CTA sits away from body with more weight, without
  competing with the headline. [TASTE/structure — generation-time composition guidance]
  {#type25-015}
- **Creative headline kerning/leading: −30 optical tracking; leading = type size + 3pt**
  (53pt → 56pt). Accented/non-Latin sets: open the leading (source text garbled — "from
  +3 to +34 the type size" [sic]; the non-Latin worked example is 53pt → 62pt). Never
  alter kerning/tracking/leading otherwise. [numbers receipt — type26-016's headline leg
  (size+3pt) is now dual-sourced] {#type25-016}

## Hexagon placement (composition — fenced)

- **The Hexagon must stay visible and recognisable** when type interacts with it.
  Iconic/Open Hexagon: overlap permitted (big-and-light slightly; caps illustrated per
  style); anchor-point alignment (baselines to hexagon edges/corners/centre); NEVER
  centre-align creative headlines with hexagons (2025 rule — relaxed by the refresh,
  type26-025). Open Hexagon may CONTAIN short, simple text — never long-form. Cropped
  Hexagon: type NEVER overlaps it; type inside only when filled red/grey (and then
  **small-and-bold only on red** — big-and-light lacks contrast on red); never type
  inside when the hexagon sits on photography/cutouts. Size ratios (Hexagon:Typography)
  90:10 · 80:20 · 60:30 · 50:50 as comparison guides. [composition vocabulary — FENCED
  to the composition/journey experimentation strand; ingested for completeness, not for
  component generation] {#type25-017}

## Language support

- **Univers Next for HSBC language list captured** (139 entries; "LowerCase"/"UpperCase"
  appear in the source list — data artifacts [sic]). Non-covered languages route to the
  licensed portfolio (type25-001). [reference — no engine action until a non-Latin
  target exists] {#type25-018}

## Findings

1. **The 2025/2026 parallel-validity banner is explicit** ("can still be used until
   further notice") — same pattern as colour. When the refresh typography pages
   re-issue, this file gets the delta pass; deltas ≠ defects (three already logged:
   type26-025/026/029). [structure note] {#type25-019}
2. **Three cost-0 gate candidates surfaced:** no-italics scan (type25-007),
   no-text-shadow scan (type25-008), red-text-role check (type25-003) — all passed
   canon with zero occurrences. RULED by Dave 2026-07-03: **STRAIGHT TO BLOCKING**
   (his override of the advisory-first convention — zero occurrences + exact checks
   = the advisory step buys nothing). ENACTED as snippet-gate check 6
   (`_validate_snippets.py`), bite-tested ×3 in `_tests/test_gates.py`; red text
   stays legal via the rag/error role token (var(--error)) and CTA roles — the gate
   bans the raw-hex role bypass. [BLOCKING — enacted 2026-07-03] {#type25-020}
3. **Orphan/widow detection** (type25-005) is a NEW visual-QA-loop candidate — needs
   render, not parsing; belongs to the owned render path when it lands
   (`_ROBUSTNESS-PORTABILITY.md`). [structure note] {#type25-021}
4. **app_type_scale.html is a duplicate** of the app-foundations page — the type scale
   is published identically in two site sections (channel-invariance receipt,
   appf-005/006 pattern). [structure note] {#type25-022}

## Cross-references

`typography-standards-2026.md` (refresh counterpart; type26-015 ↔ type25-014 dual-source;
type26-016 ↔ type25-016; type26-019 ↔ type25-006; deltas type26-025/026/029) ·
`web-foundations.md` (webf-024 scale; webf-026 ↔ type25-005 line length) ·
`app-foundations.md` (appf-001/004 receipts) · `neurodiversity.md` (neuro-007
underline-links-only; neuro-022 bold-scope) · `tokens/typography.json` (weights receipt) ·
`_BRAND-REFRESH-DIRECTION.md` (hexagon composition fence) · `_ROBUSTNESS-PORTABILITY.md`
(render-path dependency for type25-021).
