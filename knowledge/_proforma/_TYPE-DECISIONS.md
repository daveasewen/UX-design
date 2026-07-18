# _TYPE-DECISIONS — type-token rulings ledger

*Per-pillar decisions ledger for the Apollo type-token system (editorial + component sets).
Rulings + WHY, so iterative feedback doesn't evaporate. Source: Dave's review of
`reviews/TYPE-TOKENS-2026-07-17.html` (11 pinned comments, exported 2026-07-17).
Read before touching type tokens.*

## Source of truth
- Figma: **Digital Supercharge 0.5**, `scale-1` specimen, node `2320-70342` — adds the **display sizes**
  (`font-00`=52, `font-0`=40) and **confirmed weight numerics** the repo file lacked.
- Repo: `knowledge/tokens/typography.json` — native export, `font-1…7` across modes `scale-1/2/3` +
  `scale-1-200` (200% a11y text-zoom). This is the base to **reconcile + extend**, not replace.

## Rulings (2026-07-17)

- **D1 — scale naming = ROLE names + retained number** (Dave: "this, maybe paired with the number for
  people used to this convention"). Role names (display/heading/body/caption/label…) as the designer-facing
  layer, each carrying its `font-N` number as an alias for people used to the old convention. = the two-tier
  recommendation, expressed as name+number. FIRM.
- **D2 — structure = A · one primitive tier, two composite tiers** (Dave: "I think this"). Shared primitives;
  `editorial/*` + `component/*` reference them. WHY it's also the best call: Dave will build the same in
  **Figma** and wants parity — A maps cleanly (Figma **variables** = primitives, **text styles** = the two
  composite sets); B/C are harder to mirror. His D2-C musing ("might not change individual styles unless at
  theme level") weakens the anti-C worry but doesn't beat A on Figma parity + clarity — and A can still behave
  like C (crop is a tier property, changed at theme level). FIRM.
- **D3 — two SEPARATE sets, named "Editorial" vs "Component"** (Dave: "separate… Editorial vs component").
  NOT "interface" — renamed **Component**. Separate at the designer-facing level, shared primitives underneath
  (consistent with D2-A). Strategic note: **"get people off Figma and use Apollo"** — Apollo is to become the
  design tool, not just a Figma mirror. FIRM (label Component firm; role-name details open).
- **D4 — font-2 is wrong; fix + normalise** (Dave: "it's wrong"). Resolved: the `43` was font-2's **scale-3**
  value (mixed-mode read); scale-1 = **28**. PLUS Dave wants the **whole scale normalised to the 4px grid**
  ("normalised too our 4x rule, lets do both"). ⇒ propose a 4px-normalised scale for sign-off (changes brand
  values → Dave signs the numbers). FIRM (intent); numbers PENDING sign-off.
- **D5 — rename `highlight` → `emphasis`** (Dave: "highlight suggests an underscore or background colour").
  Pairing becomes `default` + `emphasis`. `-V2` name still OPEN (needs its purpose). FIRM on emphasis.
- **D6 — role styles → Component set** (Dave: "you are right"), BUT the Component set must span the **full
  scale incl. large sizes** — "we use **large figures** for some components" (KPI/stat numerals). So Component
  is not small-only; it needs display sizes too (watch tabular-figures for stats). FIRM + scope note.
- **§06 architecture — APPROVED** (Dave: "seems reasonable to me"), as modulated by the above.

## Constraints / notes to carry
- **Font availability (comment 1):** Dave has Univers Next installed locally + a **webfont pack**. ⇒ the
  "system-fallback" caveat is moot for product + specimen — we can use the **real font** via `@font-face`.
  ACTION: Dave to drop the webfont pack into the repo (e.g. `knowledge/assets/fonts/`) so specimens + renders
  use the real face. (My sandbox still lacks it until then.)
- **Crop needs companion spacing rules (comment 3):** the Component (leading-trimmed) styles remove the
  half-leading, so **descenders can clash** with objects below in vertical stacks / contours. Component
  composites must ship with **companion spacing rules** (min space-below / descender guard). Will surface in
  vertical stacks — design alongside the crop.
- **Normalisation (D4):** propose line-heights strictly on 4px grid + sizes rounded to even/4-steps, current
  vs proposed side by side, Dave signs the numbers before they hit `typography.json`.

## Rulings round 2 (2026-07-17, v2 review)
- **N1 — normalised numbers APPROVED** (Dave: "exactly as I would have done it"). scale-1: font-1 33→32,
  font-3 23→24 (LH 30→32), font-4 19→20 (LH 27→28). ⇒ carry the same logic across scale-2/3/200 (confirm).
- **N1 caveat — crop vs line-height (Dave's nagging Q, IMPORTANT):** the 4px **line-height** normalisation
  makes the **Editorial** set sit on the grid (line box = line-height). For the **Component** (leading-
  trimmed) set, cropping trims the box to **cap-height→baseline**, so line-height NO LONGER sets the visual
  box — box ≈ capHeight × font-size. Univers cap-height ≈ **0.723em** (measured from the Arabic instance;
  confirm on Latin), so e.g. 16px cropped ≈ 11.6px — NOT a 4px multiple. ⇒ **Component grid alignment comes
  from 4px SPACING tokens around the cropped box (the companion descender-guard rules), not from line-height.**
  This unifies with comment-3. Line-height normalisation still right (Editorial + multi-line internal rhythm).
  Exact Component spacing = metric-aware, computed once the **Latin webfont** is in.
- **R1 — role names ACCEPTED provisionally** (Dave: "go for what you suggested… component names might need a
  more flexible naming convention… adjust if we need"). FUTURE: revisit Component naming for flexibility.
  Tabular figures for big Component figures: not ruled — default to proposing lining/tabular; confirm later.
- **V1 — `-V2` = the DARK-MODE / low-contrast heavier register** (Dave: "useful in dark mode where light
  fonts look spidery"). Aligned with the guess. PROPOSAL: make it **theme-driven** (weights auto-step up in
  dark mode) rather than a manually-picked style — fits "governed by modes". Name TBD (`-strong`? or a
  weight-set token `standard`/`strong`). Not blocking the base build.

## Font metrics (measured from Latin desktop OTF, 2026-07-17)
- UPM 1000 · **cap-height 0.723em** · x-height 0.505em · typo asc/desc 0.767/−0.233.
- **`USE_TYPO_METRICS` is OFF**; hhea/win asc/desc = **1.068 / 0.232** → the font's natural line box is
  **~1.3em**, and the browser positions the baseline from these (not the typo metrics). Consequences:
  (a) always set **explicit line-heights** (don't rely on `normal` ≈ 1.3); (b) the Component crop trims a
  large 1.3em box down to the 0.723em cap — a big trim, so the descender-guard spacing matters; (c) weight
  numerics validated by the files: 250/300/350/400/500/700. Specimen crop diagram uses these metrics.
- LESSON: verify browser line-box metrics before drawing baseline diagrams (first crop diagram was ~5px off
  because it assumed typo ascent).

## Component grid alignment = the GRID-SLOT mechanism (Dave's Q, 2026-07-17)
Dave: can we adjust with sub-pixel padding to land cropped text on the grid? Answer: don't chase sub-pixel —
**seat the cropped (cap) box in a grid-aligned SLOT and optically centre it.** Cap height is fixed (0.723×size),
so instead of forcing it onto the grid, the slot height is a **4px multiple**; the slot's outer edges land on
the grid, the fractional remainder becomes internal padding. **The slot height = the Component line-height
token.** Its MINIMUM = `ceil(cap + 2·descender)` to 4px — which also guarantees descenders never clash
(= the descender-guard, now quantified). e.g. font-5 16px → min slot 20px; font-1 32px → min slot 40px.
Shown in specimen §04. This is the rule the Component composites encode. NOT anally retentive — it's the point.

## Blockers to writing clean canon tokens
1. **Latin "Univers Next for HSBC" WEBFONT — STILL OPEN. The blocker was RIGHT.**
   The dropped packs are the SCRIPT companions (Arabic / Japanese Tazugane / Chinese M Ying Hei /
   Armenian Helvetica), NOT the core Latin default. **Verified 2026-07-18: five webfont packs
   present, ten `.woff`/`.woff2` files each — and ZERO Latin.**

   ### ⚠️ I STRUCK THIS BLOCKER EARLIER TODAY AND WAS WRONG. Un-struck same session.
   I found the Latin **desktop** set (TTF + OTF, `_desktop/`, dated 2024-03-25) and concluded the
   blocker was false. **Desktop and webfont are different licence classes.** A desktop licence
   covers design work on a machine; a **webfont** licence covers embedding and serving. The blocker
   never claimed the desktop fonts were missing — it said the *webfont* was, and it was correct.
   **Dave caught it:** *"we really need the webfonts, this will hinder sharing material."*

   **What I got right, and it still stands:** the desktop files are present and readable, which
   legitimately unblocked (a) exact metric measurement — cap-height, sidebearings, kerning, the
   HSBC-vs-stock comparison in § T-D3 — and (b) local rendering for my own verification. Those
   were never webfont-licensed activities.

   **What I got wrong, and it had consequences:** I converted desktop TTFs to woff2 and base64-
   embedded them in a review sheet, treating a desktop licence as if it permitted web embedding.
   Monotype's Web Font User Guide sanctions base64 as an *obfuscation* method — **for fonts you
   hold a webfont licence for**. We do not, for Latin.

   **Monotype's own terms (Web Font User Guide 2024, p.10–11), now on file:**
   - Web fonts are licensed for **self-hosting**; WOFF/WOFF2 only; base64 serving is explicitly allowed.
   - *"Our fonts cannot be shared or distributed via open-source Git sharing platforms … it is your
     responsibility to ensure that Monotype fonts are not distributed via a **public** Git repository."*
   - Their prescribed remediation if fonts are already committed: `git rm`, then **BFG Repo Cleaner**
     to purge history.

   **Live exposure (2026-07-18):** four tracked files — `TYPE-SPECIMEN-2026-07-17` and
   `TYPE-COMPOSITES-2026-07-17`, plain + REVIEW — each carry six base64 woff2 payloads of
   `Univers Next HSBC` (~264KB of font data per file). They entered at commit `24accd0` and are
   pushed. **Mitigating: `github.com/daveasewen/UX-design` returns 404 unauthenticated, i.e. it is
   PRIVATE**, and Monotype's prohibition names *public* repositories. Exposure is low but non-zero —
   any repo collaborator without their own licence is still receiving the font.

   **ACTION (Dave):** request the **Latin "Univers Next for HSBC" webfont pack** (WOFF + WOFF2)
   from brand — the same deliverable already held for the five script companions. That single asset
   unblocks: shareable specimens, real-face review sheets, and any hosted prototype.
   **Until it lands:** font-embedded sheets stay gitignored (`reviews/*CONTACT*.html`), and anything
   shared outside goes as PDF, not HTML.

   **LESSON — the strike itself is the lesson.** A blocker that has stopped work for weeks is
   *exactly* the claim you want to be false, which is why disproving one deserves more scrutiny than
   confirming it, not less. I found *a* font, matched it against the word "font" in the blocker, and
   declared victory without reading which licence class the blocker actually named. Blockers should
   carry a re-test date **and** the precise artefact that would clear them.

   <details><summary>superseded text of my incorrect strike (kept for the audit trail)</summary>

   ~~STRUCK 2026-07-18 — this blocker was FALSE the whole time. The Latin desktop set is at
   `knowledge/assets/fonts/_desktop/` — **TTF and OTF, six weights plus italics, dated 2024-03-25**.
   It predates the blocker being written. The claim was inferred from the *web font* folders (which really
   are script-only) without checking `_desktop/`, and then trusted for a fortnight.
   **Consequences of the false blocker, all now reversed:** every specimen sheet since carried a
   "sandbox has no Univers — judge on your screen" caveat that was never true; renders "verified layout,
   never brand type" unnecessarily; and the crop/cap metrics were treated as provisional when they were
   measurable all along. Review sheets now embed the real face as base64 woff2
   (`gen_tracking_contact_sheet.py → embed_fonts()`).
   ~~LESSON — this is the §A failure mode in miniature: a confident negative, written once, believed by
   every later session because nobody re-checked a *blocker*.~~
   </details>
2. **Display-size values across modes** — only have `font-00`=52 / `font-0`=40 at **scale-1**; need their
   scale-2 / scale-3 / 200% values from Figma to populate all breakpoints.
3. ~~Confirm: apply 4px-normalisation across modes~~ — DONE (Dave 2026-07-17: "decide and infer, change later").
   Reconciled + normalised primitives written to `tokens/_proposals/typography-reconciled-2026-07-17.json`.
   200% = 2×scale-1; display font-00/font-0 at scale-2/3 INFERRED (×1.33/×1.73 from font-1, Figma only drew
   scale-1). PROPOSAL — promote to `tokens/typography.json` on Dave's sign-off (canon promotion = Dave).
   NEXT: build the editorial + component COMPOSITES (roles → primitives; component trim + grid-slot mixin).

## Vertical-stack spacing rule — DRAFTED (2026-07-17, task #7)
**Key insight (supersedes the earlier "min gap ≥ descender" sketch):** the descender guard is **already baked
into the Component slot**. Slot height = `ceil(cap + 2·descender)` → the cap box is optically centred with
descender + buffer below. Verified every role: bottom padding > descender depth (label 16px → 4.2px pad vs 3.7
desc; heading 32px → 8.45 vs 7.4; figure-1 52px → 13.2 vs 12.1). So descenders live **inside** the slot and
never reach the block below. ⇒ **Vertical stacking of Component blocks is PURE 4px rhythm — no per-gap descender
math.** The RULE:
1. **Component stacks** = gaps are **4px spacing tokens, slot-edge to slot-edge**. Use `gap/*` from spacing.json
   (semantic: content / subsection / section); the crop already handed rhythm to spacing, and the slot handled
   the descender. No bespoke per-size guard tokens needed.
2. **Editorial stacks** (untrimmed, `trim:none`) keep **`paragraph-spacing`** between paragraphs (full
   line-height already buffers); between Editorial headings/blocks use `gap/*`. Both line-heights are 4px-
   normalised, so Editorial boxes also slot cleanly.
3. **Mixed Editorial + Component stacks** align on **slot / line-box edges** (both are 4px multiples) → the whole
   column lands on a **4px baseline grid by construction**. This is the clean baseline-grid opportunity, now free.
4. **Enforcement:** covered by the existing 4px-grid gate (gaps are grid-governed props). No new tokens; no new
   gate. Guidance only — wire the "use gap/* tokens, never raw px" note into the component-composite usage docs.
FUTURE (optional): a `--stack-gap-*` alias set mapping the semantic gap tokens to stack contexts, if authoring
proves it useful; not needed for correctness.

## Rulings round 3 (2026-07-17, composites review)
- **Body weight floor (BRAND rule, Dave):** brand insists **no light(350)/ultra(250) on body sizes**
  (font-5/6/7). Min = **regular(400)**; regular reads fine in BOTH modes, so **body needs no dark step-up**.
  Light/thin/ultra remain on display+heading (font-00…font-4), where the dark `-V2` step-up still applies.
  APPLIED to composites + type.css. (Dave: author to double-check; hypothesis testable — regular in both.)
- **4px-grid enforcement (Dave: "a rule that forces all elements to adhere to the 4px grid"):** built
  **`knowledge/_validate_grid.py`** — a blocking gate. Grid-governed props (height/min-height/margin/padding/
  gap/top/bottom/line-height) must be whole 4px multiples; **font-size + letter-spacing + border + radius are
  EXEMPT** (glyph size ≠ layout). `--selftest` passes; type.css passes. TODO: wire into `_build_all.py` as
  **DEF-005 grid** + extend to scan component snippets/generated output. Pairs with grid-by-construction
  (only expose 4px spacing tokens) so it's grid-safe by default AND gated.

## Promotion to canon (2026-07-17, Dave: "lets crack on in your order")
- **PROMOTED.** `_proposals/typography-reconciled-2026-07-17.json` → **`tokens/typography.json`** (Apollo SDS
  primitives) and `_proposals/typography-composites-2026-07-17.json` → **`tokens/typography-composites.json`**;
  `knowledge/canon/type.css` settled as the rendered composite layer. Proposals parked at
  `tokens/_proposals/` (superseded; kept for provenance). Promotion done in the working tree — **Dave holds
  the final gate at push** (GitHub Desktop). Build **green, 26 steps**.
- **DEF-005 wired** (task #8 DONE). `_validate_grid.py` added to `_build_all.py` (step 22). No-arg build mode
  runs selftest + scans `canon/type.css` (the on-grid set today); `DEFAULT_TARGETS` grows as the retrofit
  (task #9) snaps canon.css + tranches clean. Passing.
- **Two HSBC type sets: incumbent + proposed standard** (RULED Dave 2026-07-17: *"the new ones are the Apollo
  SDS fonts… the old ones are used by HSBC in general"*, then *"Apollo will hopefully be adopted for HSBC so
  it's still very relevant to the company"*). Framing: **both sets are HSBC.** `tokens/_typography-hsbc-general.json`
  = the **incumbent** HSBC house type (pre-normalisation: font-1 33 / font-3 23 / font-4 19; weights thin=100 /
  light=300), **still live across HSBC generally**. `tokens/typography.json` = **Apollo SDS**, the 4px-normalised
  evolution **intended for HSBC adoption** (the moonshot) — the proposed future standard, not a peripheral fork.
  The two are governed as SIBLINGS by MODES (incumbent = candidate first-class `hsbc-general` token mode) so a
  migration can run mode-by-mode. Incumbent is underscore-prefixed ⇒ excluded from Apollo's `gen_canon_tokens` +
  blast-radius (out of Apollo canon.css) while it remains a distinct mode. WHY: non-destructive — Apollo advances
  its own normalised set without breaking incumbent HSBC-general consumers, and keeps a clean adoption path;
  fits "governed by modes, flexible, future-proof."
- **Faithful-promotion consequences (flagged, nothing gated breaks):**
  1. **Weight remap** in Apollo canon: thin 100→300, light 300→350, **+ ultra-light 250**; regular/medium/bold
     unchanged. Old numerics live on in the HSBC-general sibling.
  2. **6 flat vars dropped** from canon.css: `--typography-font-size/line-height-font-5/6/7` no longer emit
     (reconciled restructured font-5/6/7 to per-mode, no `$value`). Nothing gated consumed them; the composite
     classes in `type.css` carry the px. font-1..4 responsive sizes never surfaced as flat vars either (by design).
  3. **Generator quirk (pre-existing, LOGGED):** the weight name **"light" collides with the light/dark
     mode-leaf detection** in `gen_canon_tokens.py`, so it emits as bare `--typography-font-weight: 350` rather
     than `--typography-font-weight-light`. Harmless (unconsumed) but a trap — fix candidate in the retrofit:
     guard mode-leaf stripping to colour/semantic files, or rename the weight key path.

## Grid subdivisions + arrow asset (Dave 2026-07-17)
- **Sanctioned grid = 4n + 2px half-step** for spacing/layout. Applied to `_validate_grid.py` (2px allowed).
  **1px quarter-step NOT allowed as spacing** — 1px is a hairline/border value (border-width already exempt);
  allowing it as spacing would let every integer pass and neuter the gate. (Dave floated a quarter value
  "maybe" — parked; revisit only if a real spacing need appears that borders can't cover.)
- **Arrow paddings 5/6/7px = SUSPECT ASSET, not a sanctioned optical** (Dave: "maybe an issue with the actual
  asset"). Do NOT allowlist. INVESTIGATE the tooltip/popover arrow asset — if it were grid-aligned the padding
  would come out clean (4n/2). Icon-source discipline: fix the asset, don't paper over with odd padding.
- **canon.css off-grid = 123** (after 2px allowed). Dominant: 6px(21) 14px(22) 10px(20) 18px(17) 22px(9) —
  the between-steps = the real retrofit debt (snap decisions). canon.css is GENERATED → fix source snippets +
  spacing tokens + regenerate. Retrofit = task #9.

## Arrow asset RESOLVED — retire the legacy fixed-px chevron (2026-07-17, Dave approved "retire + park as legacy")
Investigation (tasks #6/#7): the off-grid `padding/arrow` (5/6/7px) + `icon/arrow/font-N` (fixed-px chevrons,
e.g. font-1 8.5×17) are the **legacy Figma fixed-pixel chevron** scheme — a fixed-size glyph placed by absolute
offsets, inherently off-grid. **They are consumed by NOTHING** (0 `var(--padding-arrow-*)` / `var(--icon-arrow-*)`
in any snippet/tranche). Every live component already draws the chevron the right way: **em-scaled +
flex-centred** — `.tip svg{width:.85em;height:.85em}` + `align-items:center` + `gap:4px` — which tracks the type
size and needs no fixed tokens. So "fix the asset" = reconcile the token store to what already shipped.
- **RETIRED + PARKED:** `padding/arrow` (from spacing.json → already in `_spacing-hsbc-general.json`) and
  `icon/arrow/font-N` dims (from icon-scale.json → new sibling `tokens/_icon-scale-hsbc-general.json`). Both
  deprecated/tombstoned, underscore-prefixed (out of gen + blast-radius). **Zero visual change** (unused).
- **Canon arrow pattern = em-scaled flex-centred chevron** (`.85em`, `align-items:center`, `gap:4px`). Rebound
  the 3 stale metas (links, hero, cards) from the old fixed-px sizing prose to this. Reconciled the 2 live
  `.arrow{gap:6px}` (hero) → `gap:4px` to match canon.
- **Unblocks:** arrow is no longer a held grid exception → the only residual off-grid in canon/snippets/proforma
  is now hairlines (1/3px), negative overlap offsets, and icon/avatar squares — all structurally exempt. Next:
  teach `_validate_grid.py` those exemptions, then expand DEF-005 to gate canon.css + snippets + proforma.

## Retrofit DONE (2026-07-17, task #9) — Dave approved the 3-rule snap policy
Review sheet `reviews/GRID-RETROFIT-2026-07-17.html` (+ REVIEW twin) rendered + presented; Dave: *"your
proposal looks pretty good… as long as we preserve the old as legacy."* Applied via `apply_grid_snap.py`.
- **Rules enacted:** (1) tie direction = **preserve density** (paddings DOWN, gaps/margins/heights UP);
  (2) hairlines **1/3px EXEMPT** (dividers/focus/optical); (3) `padding/arrow` 5/6/7 **HELD** for the
  asset investigation (not snapped, not allowlisted).
- **Preserve-old-as-legacy (Dave):** current spacing parked as sibling **`tokens/_spacing-hsbc-general.json`**
  (HSBC-general incumbent), matching the type sibling pattern. Apollo `spacing.json` snapped: padding/responsive
  **xxxsmall 6/8/10→4/8/8, xxsmall 9/13/17→8/12/16, xsmall 11/15/19→12/16/20** (xsmall now == small at these
  breakpoints — intentional collapse, noted in token). Arrow tokens untouched.
- **230 snaps applied**: canon.css 87 · snippets ~100 · proforma ~43. **Build green (26 steps).** Rendered
  Tranche-2 + Account-card in-sandbox (full chrome, recipe [[sandbox-html-rendering]]) — layouts clean, no
  distortion.
- **Residuals are all INTENTIONAL exemptions** (verified): hairlines 1/3px (rule 2) · negative overlap offsets
  (−6px) · arrow `gap:6px` in `.arrow` (rule 3 held) · **icon/avatar/glyph SQUARES** (`width:Npx;height:Npx`
  with N off-grid, e.g. 22/18/14/34/30/26).
- **Intrinsic squares — gate now handles it.** A square element's `height` (22/18/14…px) is an intrinsic
  icon/avatar size (like font-size), not layout rhythm. `apply_grid_snap.py` skips it; **`_validate_grid.py` now
  exempts it too** (height == a width in the same rule).
- **DEF-005 EXPANDED — DONE (2026-07-17).** Gate rewritten block-aware + HTML-safe (style-only, never `<script>`)
  with three structural exemptions: **hairline 1/3px** (rule 2), **negative** overlap/pull offsets, **square
  height** (== width). Residuals across the library categorised exactly: 24 hairline · 4 negative · 83 square ·
  **0 other**. `DEFAULT_TARGETS` now = **type.css + canon.css + 38 snippets + 9 tranches (50 files)** — all PASS;
  full build green. The 4px grid is now enforced library-wide, not just on type.css. (Enabled by the arrow
  retirement clearing the last held off-grids.)

## TYPE RETROFIT — rulings received 2026-07-18 (review sheet `reviews/TYPE-RETROFIT-2026-07-18.html`)
Sibling to the grid retrofit above: that one snapped **dimensions**, this one governs **text**. Gate written
FIRST (`_validate_type_composites.py`, DEF-006) per Dave's ruling — the gate defines "done", then fix to green.
Baseline at ruling time: **1183 violations / 50 of 50 files** (TYPE-001 ×50 · TYPE-002 ×721 · TYPE-003 ×412).

### §1 + §2 — all 17 row rulings returned "as proposed"
- **Sizes (316 decls → 15 rulings):** 13→14 · 15→16 · 11→12 · 22→24 · 13.5→14 · 19→20 · 18→20 · 17→16 ·
  12.5→12 · 33→32 · 10→12 · 57→52 · 30→32 · 10.5→12 · 26→24.
- **Weights (96 decls → 2 rulings):** **600→500** (×88) and **700→500** (×8).

### Rule 2 — COLLAPSE the weights, do not extend the ramp
`type.css` stays at **five weights (250/300/350/400/500)**. 96 declarations had **no composite to bind to at
all** — the library was using weights the canon does not contain. **WHY collapse:** 500 is the canon emphasis
step (the `.em` variant), and a narrower vocabulary is the entire point of a ramp; adding a 600 would widen the
vocabulary to accommodate drift rather than correct it.

### Rule 3 — avatars/badges are GATED AS TEXT. No intrinsic-scale carve-out. ⚠️ DELIBERATE DIVERGENCE
DEF-005 exempts an intrinsic square (`height` == `width`) as icon/avatar scale rather than layout rhythm — see
the grid retrofit entry above. **DEF-006 does NOT mirror that exemption.** Avatar initials and badge counts set
`font-size` to size a glyph in a fixed box, which is the same *shape* of argument, and Dave still ruled them in
scope. **WHY it matters:** a future reader will spot DEF-005 and DEF-006 disagreeing about the same elements and
try to "reconcile" them. Do not. The rules govern different things — a box's dimensions vs. the type inside it —
and the divergence is intended. Consequence: 22→24 and 18→20 visibly resize avatars and badges; renders required
before commit.

### Rule 4 — inline `style=""`: disaggregated first, then ruled three ways
The gate reported 18 violations; that is **12 elements** (a `font:` shorthand raises both TYPE-002 and TYPE-003).
Ruling a single call across all 12 would have been wrong — they are three different problems:
- **A · size-demo scaffolding (7)** — `Links` `.arrow.back` 14/20/28px, `Tags` `.tag.link` 13/16/20px. The inline
  style IS the demo. Root cause: **there is no sanctioned way to render a link at 20px**, so the hack is the only
  option. → build `.arrow--sm/md/lg` + Tags equivalent as **CANDIDATES in `_review/`, NOT promoted**. New variant
  sets on canon components are a **promotion, which is Dave's alone** (derivation governance) — the retrofit is
  not allowed to quietly grow the component API.
- **B · one-off content styling (3)** — `Cards` L170 `<p>`, `Eyebrow` L45/46. → bind to composites now. No judgement.
- **C · SVG `<text>` (3)** — `DataViz` `.dv-val`. → **DEFERRED to Dave's parked DataViz browser pass**, excluded
  from DEF-006 **with an expiry**, and logged as an open question.

### Rule 4C — the finding that changed the answer (verify, don't assume)
`.dv-svg { width:100%; height:auto }` plus a runtime `fit()` mapping the viewBox ⇒ **SVG text px is
viewBox-relative**: `22px` on `<text>` renders at 22 × (container width ÷ viewBox width), NOT 22 CSS px.
So snapping it to the CSS ramp would be **measuring the wrong thing**, and exempting it would hand a permanent
carve-out to *all future chart typography across the whole DataViz pillar* — not three elements.
**OPEN QUESTION for the DataViz pass:** should the type ramp gain a **viewBox-relative expression** so chart
type is governed in the units it actually renders in? Neither "snap" nor "exempt" is the right end-state.

### Method notes
- Off-ramp values collapsed **412 → 17 rulings** (15 sizes + 2 weights); presenting 412 rows would have been
  unreviewable. Group by value, not by occurrence.
- The review doc is generated by `reviews/gen_type_retrofit.py` from the gate's own `--inventory` output, so the
  doc **cannot drift from the gate**.
- Scope is component-only; demo-chrome (78 decls) deferred and logged as **ds-003** in `_DS-IMPROVEMENTS.md`
  rather than silently exempted — the carve-out is a selector-name convention and is recorded as debt.

## REVERSE TEXT ON CHROMA — rulings 2026-07-18 (specimen v1 → v2)

### Q1 ANSWERED — chroma is the driver, NOT lightness
The v1 §2 control pair sat at near-identical lightness (**0.43 vs 0.42**) and differed only in saturation
(**1.00 vs 0.72**). Dave: *"they are quite similar but these seems to dance the least. the bright red and the
white text is instantly straining."* The sheet was built to be able to return a null result — if lightness had
been the driver, the honest outcome was NO new rule, just a higher contrast floor. **It did not come back null.**
⇒ the effect is real, distinct from contrast, and cannot be folded into the contrast gate.

### It is NOT the vibrating-boundaries rule — verified against our own function
`vibration()` (`_validate_dataviz.py`, the `{#dv-019}` rule quantified from the Tuts+ article 07-16) scores
white-on-red **0/3 legs** and is RIGHT to: it needs two *saturated* near-complementary colours at near-equal
value; white has sat 0.00 and the value ratio is 5.22. A real chart pair scores 3/3. **Sibling phenomenon —
halation/irradiation, not vibration.**

### ⚠️ SUPERSEDED — the `#A8000B` badge ruling (made earlier the same day)
`#A8000B` is **sat 1.00** — the same maximum chroma as the `#DB0011` Dave called straining, only darker. It buys
*lightness* contrast, which was never the problem. Superseded by the chroma observation, which has the
controlled comparison behind it. **Badge moves to a sat-0.72 red.** Recorded because the two rulings are
hours apart and a future reader will otherwise see only the first.

### THE UNIFYING LEVER (2026-07-18) — two levers, one rule
White on `#000` = 21:1; on **`#1A1A1A`** = 17.4:1 — the edge step cut ~17%. That is **the same lever** as
dropping chroma 1.00→0.72 on a coloured ground: both **reduce the extremity of the edge** rather than adding
contrast. So the drafted rule has **two levers by ground type — CHROMA on coloured, LUMINANCE EXTREMITY on
neutral** — and `#1A1A1A` has been the neutral-ground instance for two weeks without being written down as such.

### 🔴 FINDING — `#1A1A1A` exists but is not governed
Dave asked whether the anti-halation black was stored. It is `_PROFORMA-RULES.md` rule 1. But: it is **in NO
token store** (a literal across 10 files + a line in a rules doc — nothing resolves or gates it); it is **still
marked open** (*"Open to confirm with Dave: (a) near-black shade (#1A1A1A)"*); and **the halation rationale was
never recorded** — the written rationale is about red already meaning destruction. *The value survived, the
reason did not.* This is the exact loss the decisions ledger exists to prevent, found by Dave's own recall.

### RAG PROMOTION — direction set, sheet built, NOT promoted
Dave: *"this and it's the other selected for rag during the session should be canon, red amber green and blue"* —
promote the **data/delta** family to canon RAG. Well-founded: delta is **saturation-normalised at 0.72 across all
four hues**; the incumbent `rag/*` has no consistent chroma (1.00/1.00/1.00/0.47). Delta was value-split AND
saturation-normalised during the 07-16 D2 vibration work — engineered for this problem before it was named.
- **R2 RULED — amber takes DARK text** (Dave). **But the ruling forces a second choice:** on delta amber
  `#C58720` the existing `rag/text/on-light` (`#333333`) scores **4.13:1 — FAILS**. Only `#1A1A1A` (5.69) or
  `#000000` (6.86) pass. So "black text on amber" **cannot mean the existing token**, and `#1A1A1A`'s
  promotion becomes a *dependency* of the RAG promotion, not a separate matter.
- Blast radius measured, not asserted: **21 files** consume `rag/*` tokens, **42** carry the literal hexes.
- Sheet: `reviews/RAG-PROMOTION-2026-07-18.html`. Promotion is Dave's alone — nothing applied.

### STILL OPEN (specimen v2 re-cut at the chosen chroma)
Q2 minimum weight · Q3 size floor · **Q-new: the saturation threshold** (without a number there is no gate,
only a preference — the equivalent of dv-019's 135°) · Q5 scope (badges vs every light-on-chroma surface).

## SPECIMEN V2 RULINGS — 2026-07-18. The rule is now QUANTIFIED.

### Q2 + Q3 ANSWERED — it is a SIZE×WEIGHT PAIR, not a flat weight minimum
| size | minimum weight |
|---|---|
| 10px | Medium — **excluded**: Dave *"I don't recommend using this size and it isn't in the font ramp"* (ramp starts at 12) |
| 12px | **Medium (500)** |
| 14px | **Medium (500)** |
| 16px | **Medium (500)** |
| 20px | **Light (300)** |
The minimum weight **falls as size rises** — larger type carries more stroke mass. Q3 = yes, size matters,
so the rule cannot be expressed as "reverse text must be ≥N".

### Q-new ANSWERED — the saturation ceiling is **≤ 0.72**
Dave picked `#B92F1E` (sat 0.72) as the first ladder row that reads clean; 0.78 / 0.84 / 1.00 do not.
**This is the gate's number** — the equivalent of `dv-019`'s 135° hue leg, and for the same reason: derived
from an observation, not from theory. The rule was un-gateable without it.

### ⚠️ TWO CORRECTIONS TO EARLIER CLAIMS IN THIS SESSION (mine, both)
1. **The `700→500` collapse did NOT cause the spidery badge.** The ruling puts the minimum at Medium (500)
   for 12–16px, so the badge weight was always sufficient. **The GROUND was the fault** — at sat 1.00 it
   strained at any weight; at sat 0.72 Medium holds. I attributed it to my own change and was wrong.
2. **`type25-008` was wrongly invoked.** "Emphasis = Univers Bold only" governs emphasising keywords within
   running text — not badge counts. It does not apply here, and I used it to argue for 700 when it had no
   bearing. The 600→500 half of rule 2 still stands on its own merits (600 is not a licensed weight and ships
   no font file); the 700→500 half needs no special justification after all.

### `#1A1A1A` PROMOTED — `surface/digital-black` (Dave: *"it can be called digital black or something,
that's probably how I'll remember it"*)
Placed in `semantic-colour.json`, **not** `colour.json` — the brand store holds published brand values and
`#1A1A1A` is Apollo-derived; putting it there would corrupt the brand source. Follows the `data/delta`
precedent (derived, no primitive alias, `$note` carries the anchors). The token carries `$substitutesFor`,
`$condition`, `$rule` and `$provenance` so the condition travels with the value.
- **Naming trade, recorded deliberately:** "digital black" favours **recall over precision** — it does not
  encode the condition, and reads like a second black free to pick. That is Dave's call (he is the one who
  must remember it), so the condition lives on the token and must never be stripped from it.
- **Still open:** the **10 literal `#1A1A1A` usages** need rebinding to the token; and
  `_PROFORMA-RULES.md` rule 1 still carries its stale *"Open to confirm: (a) near-black shade"* line.

### THE RULE, ASSEMBLED — "reduce the extremity of the edge"
Two levers by ground type, one principle: **never add contrast, which makes halation worse.**
- **Coloured ground → CHROMA**: saturation ≤ 0.72.
- **Neutral ground → LUMINANCE EXTREMITY**: `surface/digital-black` (#1A1A1A, 17.4:1) in place of `#000` (21:1).
- **Both grounds → SIZE×WEIGHT**: the table above.
Distinct from `{#dv-019}` and must not be merged with it (dv-019 scores this 0/3 and is right to).
**Gateable now, gated by nothing.** Q5 (scope — badges only vs every light-on-chroma surface) still open.

---

# SESSION 2026-07-18 (afternoon) — TRACKING / LETTER-SPACING

*Spun off from the TYPE-002 retrofit. Nothing here is promoted — five review sheets await Dave's
markup. What IS settled is the reasoning and the measurements, recorded so a cold session does not
re-derive them.*

## ⭐ T-D1 — Editorial and Component answer to DIFFERENT PHYSICS (Dave, ruled by observation)

Dave: *"we have editorial and component styles to take into account, I don't [think] there is any
impact on short labeling to reading speed … this isn't just about reading speed it's about halation
and blooming, so we may have different rules for the text roles."*

**This is the load-bearing idea of the session and it generalises beyond tracking.**

| | EDITORIAL | COMPONENT |
|---|---|---|
| what happens | **read** continuously | **recognised**, not read |
| mechanics | fixations, saccades, word-skipping, word-shape | letter identification at a glance |
| governed by | reading-speed evidence · optical sizing | crowding · halation / bloom |
| ground | almost always ordinary | often reversed on chroma or near-black |
| tracking direction | restraint — near zero, tighten at display | opens at label sizes, tightens at figures |

**Two consequences, both of which corrected live work:**
1. **Reading-speed evidence governs Editorial ONLY.** Nobody saccades through "Pending approval".
   I had used it to argue *against* opening tracking on component labels, where it was never in scope.
2. **Crowding evidence governs Component MORE than Editorial.** The Zorzi/dyslexia literature measures
   *letter identification* — which is precisely what recognising a short label is. It had been filed
   under the wrong tier.

**Independent corroboration:** Frutiger drew the same line. His stated reason for designing *Frutiger*
was that Univers was *"perfect for printed books"* but wrong for someone crossing an airport at 5 mph —
continuous reading vs glance recognition. **He put Univers on the Editorial side of Dave's split.**

**Structural consequence — the reason this matters beyond tracking:** the same 40px wants a different
value in each tier (Editorial −0.02em vs Component −0.01em). **Size alone cannot express the rule.**
So tracking must live ON the composites (11 Component + 9 Editorial), not as a token ramp indexed by
size. That is the strongest available argument that the D2/D3 role split is real rather than tidy.

## T-D2 — MEASURED font facts (from the licensed files, not literature)

Measured with fontTools from `knowledge/assets/fonts/_desktop/TTF/`. **Highest evidence tier we have** —
not what typographers say about Univers, what our actual files do.

- **Univers is LOOSE, not tight.** `n` sidebearing = **15.6% of x-height**; Arial 12.4%, Calibri 13.5%,
  Lato 13.4%. Only DejaVu Sans (drawn open for low-res screens) is looser at 15.7%. SB/stem **0.90**
  vs ~0.75 for the Helvetica lineage.
  ⚠️ **The folklore "Univers is tight" refers to APERTURES, not spacing.** Frutiger's complaint was
  *"too round and closed an effect for the easy recognition of word-signs"* — a counter property.
  **Tracking cannot open a counter**, so the face's known glance-reading weakness is NOT addressable by
  the lever we spent the day designing. Size, weight and ground must carry it.
- **Sidebearings barely move across weights; stems grow sevenfold.** ULt→Bd: sidebearing 92→68 (−26%),
  stem 20→146 (+630%). **SB/stem collapses 4.60 → 0.46.** At Bold there is under half a stem of air.
  **Medium — mandated by col26-020(c) for small reverse text — sits at 0.64, already tight-side.**
  ⇒ **Tracking may need a WEIGHT term, not just size and role.** Largest single effect measured;
  no current rule accounts for it. Ladder C6 on the contact sheet asks this and nothing else.
- **Kerning present in all six weights** (via GPOS extension lookups), values consistent.
- **Vertical metrics:** UPM 1000 · cap 723 · x-height 505 · hhea 1068/−232 · lineGap 0 ·
  `USE_TYPO_METRICS` OFF → natural line box **1.300em**.

## T-D3 — HSBC's cut ≡ stock Univers Next Pro, horizontally. SETTLED, never re-ask.

Dave supplied Univers Next Pro mid-session; both families measured against each other, six matched weights.

- **Sidebearings** (LSB *and* RSB): 75 glyphs × 6 weights → **1 glyph differs**.
- **Advance widths**: 82 glyphs × 6 weights → same 1 glyph.
- **Kerning**: 10 problem pairs × 6 weights = **60/60 exact matches**, value for value.
- **Cap-height / x-height**: identical to the unit at every weight.
- The one difference is the **ampersand**, redrawn for HSBC (ink 680×751 vs 664×738; RSB −1 vs 15).

**⇒ Published Univers Next guidance on SPACING applies to us directly.** Empirical, not assumed.
**⇒ The `Fo`-unkerned-in-Regular gap exists in STOCK too** — upstream Linotype/Monotype omission,
**not an HSBC error**. Do not raise it with brand. Logged in `_DS-IMPROVEMENTS.md` as ds-004.

**⇒ Where published advice WILL mislead us — vertical metrics:**

| | hhea asc/desc | lineGap | line box | baseline from top | glyphs |
|---|---|---|---|---|---|
| **HSBC cut** | 1068 / −232 | 0 | **1.300em** | ~82% | 835–1011 |
| stock Univers Next Pro | 750 / −250 | 200 | 1.200em | ~71% | 669 |

Line boxes are only **8%** apart — but the **baseline sits ~11 percentage points lower in the box** in
our cut, because HSBC folded the lineGap into ascent. **That is what the cap-trim and grid-slot work
depends on**, so stock-Univers line-height advice does not transfer.

## ⚠️ T-D4 — THREE CORRECTIONS I MADE TODAY (all mine; all "tidy first answer, wrong")

Recorded per the §A rule that corrections are inscribed as loudly as the original claim. **The pattern
matters more than the individual errors: in all three the first answer was neat and confirmed what I
half-expected.** That is the signal to run it twice.

1. **Invented a fork that the evidence had already closed.** I framed col26-020(c) as "universal weight
   floor vs conditional rung" and told Dave it blocked the retrofit. Reading the *rule text* off the KB
   page without returning to the *specimen that generated it*, I missed that the sheet only ever tested
   reverse text on extreme grounds — the universal reading was never a candidate. **Dave asked "am I
   right that this was decided?" and he was.** Q5 (scope) is genuinely open; my fork was not.
   → **Lesson: read the specimen, not the summary. The rule text is a Polaroid of the sheet.**
2. **Nearly recorded a font defect that does not exist.** First kerning parser reported "no kerning in
   any weight except Medium" — I was composing the write-up when I re-checked. The family uses **GPOS
   extension lookups (LookupType 9)**; the parser only counted direct type-2. Every weight kerns.
   → **Lesson: a finding that makes the vendor look careless deserves a second parser.**
3. **Nearly reported an 8% difference as 30%.** HSBC ascent 1068 vs stock 750 *looks* like 30%. It is 8%,
   because stock carries a 200-unit lineGap that HSBC zeroed. The ascent is the figure that looks
   decisive and is not.
   → **Lesson: compute the derived quantity, never eyeball the component that suggests it.**

## T-D5 — What the tracking rule would be, IF the sheets survive Dave

**Nothing below is promoted.** Recommendations on `reviews/TRACKING-CONTACT-2026-07-18.html`.

| role | context | recommend | confidence |
|---|---|---|---|
| Editorial | display 40px | −0.02em | medium-high |
| Editorial | body 16px | **no change** | **high** — the null result |
| Component | label 12px, ordinary | +0.005em | **low** — moved twice |
| Component | label 14px, reverse neutral | +0.015em | medium |
| Component | label 14px, reverse chroma | +0.015em | medium |
| Component | figure 40px | −0.01em | low-medium |
| both | reverse text luminance | #EBEBEB, **neutral grounds only** | medium |
| Component | **weight term** | **open — ladder C6** | — |

**Text-luminance asymmetry, computed not guessed:** on `surface/digital-black` there is enormous
headroom (`#EBEBEB` = 14.60:1). On the sat-0.72 chroma ground the lever runs out immediately —
`#E0E0E0` = 4.56:1 and `#D4D4D4` **FAILS** at 4.06:1. So text-dimming is a **neutral-ground lever**,
which mirrors col26-020's existing chroma/luminance split rather than cutting across it.

**Candidate extension to {#col26-020}:** the rule currently has two levers (ground chroma, ground
luminance). The literature supplies two more for reverse text — **open the tracking** and **dim the
ink off pure white**. Both are "reduce the extremity of the edge" without adding contrast.

## T-D6 — Open, carried forward

- **Q5** (col26-020 scope: badges only vs every light-on-chroma surface) — open since specimen v2,
  never marked. Now restated as R4 on the Component-Medium sheet.
- **The 100 Component `500`s** — is small-label Medium structural or drift? `COMPONENT-MEDIUM` sheet.
- **The weight term** (T-D2) — ladder C6.
- **Whether tracking becomes a composite property** — follows from T-D1's structural argument.
