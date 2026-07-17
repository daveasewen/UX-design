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

## Vertical-stack spacing (Dave flagged 2026-07-17) — NEXT (task #7)
Trimming removes the built-in leading, so **vertical rhythm is controlled entirely by spacing tokens** — the
crop hands the job to spacing (same theme as the descender-guard). Draft rule to design:
1. Gaps between Component blocks = **4px tokens, slot-edge to slot-edge** (predictable now boxes are trimmed).
2. **Min gap ≥ upper block's descender depth (0.232×size)** so descenders clear the next line's caps — reuse
   the per-size guard number.
3. **Editorial** (untrimmed) stacks keep **paragraph-spacing** — full line-height already buffers.
4. Opportunity: true **baseline-grid** alignment is now clean because boxes are trimmed to known metrics.
Emit as spacing tokens + guidance; wire into component composites.

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
