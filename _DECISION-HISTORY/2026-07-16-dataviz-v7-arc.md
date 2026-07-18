# DataViz research → V7 promotion arc (2026-07-16)

> STANDING: decision-history file — provenance record, never edited after landing.
> **Relocated VERBATIM from `_LIVE-STATE.md` (lines 423–506) on 2026-07-18**, per the ruled
> consolidation (`reviews/CONSOLIDATION-AUDIT-2026-07-18.html`). Spine summary: `_LIVE-STATE.md` → LIVE DataViz entries.
> **NOTE (Dave, 2026-07-18): much of this deserves a colleague presentation** — registered in `_FUTURE-STATE.md`. Rulings canonical in `knowledge/_proforma/_DATAVIZ-DECISIONS.md`.

---

- **🟠 OPEN (2026-07-16) — DataViz is the next big pillar (Dave's pick), in research.** Desk research DONE
  → `reviews/DATAVIZ-DESK-RESEARCH-2026-07-16.html` (+ review pair): digital + finance charting, cited; feeds a
  method dossier. KB already carries the HSBC rules (`guidelines/data-visualisation.md` + bar/pie/line companions:
  flat-fills-only/no-gradient/no-3D, ≥3:1 building blocks, palette-only, ≥2px block gap, per-type rules) and the
  **"supercharge" = supporting palette** (10 families × 5 steps, in `colour.json`; `tokens/_proposals/supporting-palette.proposals.json`).
  **Approach RECOMMENDED:** CSS-first **custom SVG + token layer** (reject canvas — can't tokenise/inspect/a11y),
  table-as-source for simple types, D3-scale/Observable-Plot for hard maths only, CSS-only motion. **RULINGS (Dave
  2026-07-16, from the dossier review):** (1) red/green gain-loss "not precious" — the never-red/green orthodoxy is
  overblown; USE it, pair with sign/arrow/position — but ⚠ this needs the HSBC KB **no-red-in-charts** rule
  ({#dv-017}) EXPLICITLY OVERRIDDEN (flagged, not yet done); (2) **texture sparingly + stylishly** — one chevron-style
  pattern max per chart, still flat; (3) **legends OK but with an alphabetic signifier** (bars A·B·C, legend shows
  colour+letter+name). **OPEN/NEXT:** method dossier · **V7 series-assignment** (which palette family/step = series-N
  per mode — unblock with real renders, respect per-mode `indicatorOK`) · **variant-complete inventory** (Dave: bar →
  butterfly/tornado/segmented/vertical-horizontal/waterfall… enumerate ALL sub-variants) · round-one kit
  (KPI stat card · line/spark · bar/column/stacked · donut). Tasks #13–16.
  **UPDATE 2026-07-16 eve — method dossier DRAFTED + V7 RENDERED, both awaiting Dave's markup.**
  (1) **Method dossier** → `reviews/DATAVIZ-METHOD-2026-07-16.html` (+ .REVIEW pair) + KB model doc
  `knowledge/_proforma/_DATAVIZ-METHOD.md` (typed relations, per rule 16): approach restated for RATIFICATION
  (semantic SVG + tokens + CSS motion + visually-hidden-table spine; canvas rejected), vocabulary model
  (family→type→variant; designers pick recipes), **variant-complete inventory (41 items, tiers R1/R2/M/X)**,
  the four rulings enacted incl. a DRAFT scoped override for gain/loss red (touches **col26-012** — the actual
  no-red-with-supporting-palette rule, NOT dv-017 as previously cited — plus the 07-14 red-once-per-screen rule:
  deltas = data semantics, not actions), gate mapping (new `_validate_dataviz.py` + indicator-contrast extension;
  gate lands WITH the first chart), round-one kit spec + build order. **8 numbered decisions in §08.**
  (2) **V7 decision sheet** → `reviews/DATAVIZ-SERIES-RENDERS-2026-07-16.html` (+ .REVIEW pair; generator
  `knowledge/_review/_gen_series_renders.py`): candidates **A** hue-spread mid-step (light=dark-families step 3,
  dark=light-families step 2; recommended) / **B** strong-step 1 / **C** mode-stable dual-legal (surfaces the
  **dv-014 ↔ col26-017 scope tension**), × both real surface tokens × 4 chart types, receipts RECOMPUTED from hex
  (all agree with proposals file); + delta options (1: RAG tokens, needs override — `rag/error/dark` IS #DB0011,
  4.02:1 = the ds-002 signature, OK for ≥3:1 indicators / 2: in-palette pair, no override). Render-verified in-sandbox
  (playwright headless-shell, memory recipe), 0 console errors; full build green after. **NOTHING PROMOTED —
  derivation-governance holds; V7 stays Dave's judgment gate.** NEXT = Dave marks up both REVIEW copies →
  enact picks (semantic-colour.json `data/series-N` + override wording into the guideline) → build round-one kit.
  **UPDATE 2026-07-16 late — Dave's markup ENACTED (sheet now REV 2) + range-mode architecture set.**
  RULED via markup (readback pending confirm): **C = DEFAULT** series assignment (mode-stable; resolves dv-014
  scope = ACROSS the theme switch; col26-017 divergence recorded consciously) · **A = HIGH-CONTRAST ALTERNATE**
  via a per-chart switch (`data-contrast` / `data-range` — token rebind, no chart forks) · B retired to the record.
  **Deltas REBUILT** per markup: rev-1 options (RAG reuse / raw palette pairs) retired; new values DERIVED from
  palette anchors (most-red burnt-orange/1 + most-green forest-green/1 + blue neutral midnight + amber sun-yellow),
  hue pulled to convention, lightness SOLVED against real surfaces; three options **D1 quiet / D2 convention-forward
  (rec) / D3 CVD-split** await pick; amber asymmetric (3:1 light graphic-grade / 6.5:1 dark). **Ranges direction
  (Dave, follow-ups):** we can CREATE ranges (colour-theory harmonies + "scientific" criteria), categorised by
  INTENT (harmony-led · contrast-led first two); range selection = a future **edit-mode harness dial**, so ranges
  LIVE IN TOKENS — enacted as generated holding pen `tokens/_proposals/dataviz-ranges.proposals.json` (range/default=C,
  range/high-contrast=A, 5 generated suggestions tagged by intent, delta d1–d3; statuses picked-pending-confirm /
  proposed; generator emits it alongside the sheet). Sheet §06 = the suggestion strips. Method dossier §05 synced.
  REMAINING PICKS: confirm C/A readback · delta D1/D2/D3 · promote-or-park §06 ranges. Then round-one kit.
  **UPDATE 2026-07-16 night — second markup batch (7 items) + the vibrating-boundaries article ENACTED (sheet REV 3).**
  🟢 **NEW RULE (Dave, via Tuts+ "Vibrating boundaries" article): avoid vibrating boundaries** — adjacent
  saturated near-complementary equal-value pairs shimmer; a11y hazard (astigmatism, sensory processing; equal-value
  pairs also vanish for CVD). QUANTIFIED: all 3 legs = risk (pair value-ratio <1.25 + hue-sep ≥135° + both HSL
  sats ≥0.5; hue leg set at 135° because Dave OBSERVED the dance on a 146° pair). Enacted as: vibration receipts on
  every candidate/delta/range (sheet + tokens `$vibration`) · advisory adjacent-pair check specced for
  `_validate_dataviz.py` (dossier §06 row; skip pairs separated by a dv-004 gap — the gap IS the classic defence) ·
  dossier ruling §04.5 (Apollo-added rule, not ingested-HSBC). **DELTAS: D2 = PICKED** (Dave), dark red/green
  "danced" → value-split BOTH pairs (receipts caught light mode had the same triple; light loss deepened 6.0:1,
  dark gain 6.2:1/loss 4.4:1 + dark red desat 0.60) — all pairs now ≤ moderate; **D1 kept-option** (same split);
  D3 retired-record (mechanism absorbed into the fix). **RANGES: palette-native ONLY** (Dave: "we can't invent
  anything — only safe in the RAG" = deltas are the sole derived-colour zone): all suggestion ranges rebuilt from
  existing palette primitives ($token paths carried), WIDENED across family step-ramps 1→5 (also the vibration
  defence); CVD-diverging range RETIRED (existing guideline rules = the mitigation). Sheet/tokens/dossier all
  regenerated; build green. REMAINING: confirm the rev-3 readback · promote-or-park ranges · confirm vibration
  thresholds (1.25/135°/0.5) as the gate's advisory start. Then round-one kit.
  **✅ UPDATE 2026-07-16 close — V7 CONFIRMED + ENACTED (Dave: "happy with my initial selection with your
  adjustments").** PROMOTED into `semantic-colour.json`: **`data/series/1–5`** (C, mode-stable, same hex both
  modes, $alias→supporting primitives) · **`data/series-high-contrast/1–5`** (A, per-chart rebind) ·
  **`data/delta/{gain,loss,neutral,warning}`** (D2, value-split pairs; derived — no primitive alias, $note carries
  anchors). **Override + new rule RECORDED in the guidelines as `{#dv-019}`** (`data-visualisation.md`, cross-ref
  annotation at col26-012 in `colour-standards-2026.md`): scoped gain/loss exception (delta indicators only, never
  series fills; doesn't count against red-once-per-screen) + the vibrating-boundaries rule (Apollo-added,
  advisory-derivable) — the rules-index gate rejected `{#dv-019-apollo}` (ID grammar = must end in the number),
  renamed to `{#dv-019}`, now indexed. Statuses flipped to `confirmed-2026-07-16` in
  `dataviz-ranges.proposals.json` + the sheet; `supporting-palette.proposals.json` $README marked V7 RESOLVED
  (semantic side = receipts now). Suggestion ranges stay `proposed`. Vibration thresholds = adopted as the
  advisory start. Full `_build_all.py` GREEN. **NEXT = round-one kit** (KPI card → bar/column → line → donut)
  against the live tokens, `_validate_dataviz.py` (incl. vibration check) landing WITH the first chart; dossier
  §08 items 1/5/6/7/8 (approach ratify, tiers, maths helper, chevron timing, gate plan) still open for markup.
  **✅ UPDATE 2026-07-16 final — METHOD DOSSIER RATIFIED (Dave's markup, 4 items).** §01 approach RATIFIED
  (semantic SVG + tokens + CSS motion + hidden-table spine; canvas rejected — now the build method) · §05
  confirmed · §06 gate plan APPROVED · §07 kit spec APPROVED (settles chevron-in-R1). Tiers (§03 boundaries) +
  maths helper (hand-rolled first) stand as DEFAULTS, unmarked — movable before they bite. Dossier §08 updated
  to resolved-status; KB model doc status updated. **DataViz has NO open blockers: next session = build the
  round-one kit** (KPI card → bar/column → line → donut, gate-first). Committed `966f0d1` (tokens batch) —
  this ratification batch needs its own commit.
