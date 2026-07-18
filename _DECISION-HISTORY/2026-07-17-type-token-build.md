# Type-token build detail + icon canvas step 0 (2026-07-17)

> STANDING: decision-history file — provenance record, never edited after landing.
> **Relocated VERBATIM from `_LIVE-STATE.md` (lines 197–212, 366–378) on 2026-07-18**, per the ruled
> consolidation (`reviews/CONSOLIDATION-AUDIT-2026-07-18.html`). Spine summary: `_LIVE-STATE.md` → LIVE type-token + icon entries.
> Rulings canonical in `knowledge/_proforma/_TYPE-DECISIONS.md`.

---

- **TYPE-TOKEN SYSTEM = built, proposals await promotion** (2026-07-17). From Figma *Digital Supercharge 0.5*
  (`scale-1`, node 2320-70342) reconciled with repo `typography.json`. **Primitives** (reconciled + 4px-normalised,
  weights confirmed 250/300/350/400/500/700 from the Latin desktop instances, display sizes font-00/font-0 added —
  scale-2/3 INFERRED) → `tokens/_proposals/typography-reconciled-2026-07-17.json`. **Composites** = TWO sets
  **Editorial** (full line-height) + **Component** (cap-trim + 4px grid-slot) → `tokens/_proposals/typography-composites-2026-07-17.json`
  + working mixin `knowledge/canon/type.css`. Key mechanism: Component text is **cap-trimmed** then **seated in a
  4px grid-slot** (slot = `ceil(cap+2·descender)`→4px = line-height token AND descender-guard); metrics measured
  (cap 0.723em, USE_TYPO_METRICS off → 1.3em natural box). **Gate** `knowledge/_validate_grid.py` (4n + 2px half-step;
  1px=borders only; font-size/letter/border/radius exempt) — passes selftest + type.css. RULINGS + WHY all in
  `knowledge/_proforma/_TYPE-DECISIONS.md` (D1–D6, N1, V1, body-weight brand rule, grid subdivisions). **Naming:**
  role names + font-N alias (D1); sets = Editorial vs Component (D3, "get people off Figma onto Apollo"); highlight→
  **emphasis** (D5); `-V2` = dark-mode weight step-up (V1). **BRAND RULE:** no light/ultra on body sizes (min regular);
  see memory [[type-body-weight-rule]]. OPEN: promote proposals→canon (Dave's sign-off; canon promotion = Dave only);
  wire grid gate as DEF-005 (task #8); vertical-stack spacing rule (task #7); retrofit ~123 off-grid values in canon.css
  + 69 across tranches — fix source snippets+tokens, regenerate (task #9); investigate arrow-padding 5/6/7 asset;
  webfont: Latin desktop OTF/TTF in `knowledge/assets/fonts/_desktop/` (product still needs webfont licence renewed).

---

- **✅ STEP 0 DONE (2026-07-17) — icon SOURCE canvas normalised to 18×18.** RULED Dave: **normalise the source
  assets** ("the errors happened either by the author or during ingest, they should definitely be aligned") —
  i.e. option A, we own this library, not emit-time patching. **69 files** were off-canvas (35× `19×18`,
  28× `18×19`, 6× `19×19`); measured with real path bboxes (`svgelements`), not a number-scrape:
  **53 had artwork already inside 0–18 → lossless viewBox retag** (these had been rendering ~5% SMALL, since a
  19-unit canvas scale-to-fits into a square box); **16 genuinely exceeded 18 → uniform scale-to-fit wrapper**
  `<g transform="scale(k)">` (k=0.947 for the six true 19×19 — lending/-active, overdraft, pay-company,
  premier-privileges-active, sell; k≈0.994–0.999 for ten rounding-noise cases) — **the wrapper preserves the
  original path data byte-intact** for provenance/diffing. **EXCLUDED (deliberate non-square utility marks,
  left alone):** `handle.svg`, `arrow-{up,down}-low`, `arrow-{left,right}-narrow` (`8×16`/`18×9`/`18×7`).
  Library now **652 × 18×18** + those 6. Only **3 glyphs were inlined downstream** (social-linkedin,
  social-youtube-2, stamp-active) — their `<symbol viewBox>` updated in Tranche-8 + the reconciled candidate.
  **Full build green (26/26) incl. the icon gate; before/after renders identical (no clip, no distortion).**
