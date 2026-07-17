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
1. **Latin "Univers Next for HSBC" webfont** — the dropped packs are the SCRIPT companions (Arabic /
   Japanese Tazugane / Chinese M Ying Hei / Armenian Helvetica), NOT the core Latin default. Need the Latin
   pack for true rendering + exact cap-height/crop metrics.
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
- **NEW gate finding — intrinsic squares.** The grid gate flags a square element's `height` (22/18/14…px) as
  off-grid, but that's an **intrinsic icon/avatar size governed by icon-scale, not layout rhythm** — like
  font-size, it should be EXEMPT. `apply_grid_snap.py` already skips `height` when it equals a `width` in the
  same rule (avoids distorting icons). GATE TODO: teach `_validate_grid.py` the same square-exemption + the
  rule-2 hairline exemption. Until then DEF-005 stays **type.css-only**.
- **DEF-005 expansion (deferred):** add canon.css + snippets + proforma to `DEFAULT_TARGETS` only AFTER the gate
  learns (a) hairline 1/3px exempt, (b) square-height exempt, and (c) the **arrow asset is fixed** (its held
  `gap/padding` off-grids clear). Bundle these into the arrow-asset session.
