---
name: dataviz-pillar-progress
description: "DataViz pillar — round-one kit BUILT + 9 review rounds; PARKED 'good enough' NOT signed off (Dave 2026-07-16); REVISIT to add filtering/titles/controls; ledger _DATAVIZ-DECISIONS.md"
metadata: 
  node_type: memory
  type: project
  originSessionId: 481e11f6-31dc-47f9-9f76-d3467f232dab
---

DataViz = the next big pillar (Dave's pick, 2026-07-16). Progress as of 2026-07-16 eve:

- **Desk research DONE** (`reviews/DATAVIZ-DESK-RESEARCH-2026-07-16.html`, reviewed by Dave) → four rulings: red/green gain-loss usable with sign/arrow/position (needs a CONSCIOUS scoped override — the real rule is **col26-012** no-HSBC-Red-with-supporting-palette, NOT dv-017 as first cited, plus the 07-14 red-once-per-screen rule: deltas = data semantics, not actions); texture = ≤1 chevron pattern per chart; legends = colour+letter+name with letters on elements; inventory must be variant-complete.
- **Method dossier DRAFTED** (`reviews/DATAVIZ-METHOD-2026-07-16.html` + REVIEW pair + KB model doc `knowledge/_proforma/_DATAVIZ-METHOD.md`): semantic SVG + tokens + CSS motion + visually-hidden-table spine (canvas rejected); 41-item inventory in tiers R1/R2/M/X; gate map → new `_validate_dataviz.py` landing WITH the first chart; 8 numbered decisions in §08. NOT ratified.
- **V7 series assignment RENDERED** (`reviews/DATAVIZ-SERIES-RENDERS-2026-07-16.html`, generator `knowledge/_review/_gen_series_renders.py`): A hue-spread mid-step (recommended) / B strong-step / C mode-stable (exposes the dv-014 ↔ col26-017 scope tension); delta options RAG-tokens vs in-palette. Receipts recomputed from hex, all agree. **Still Dave's judgment gate — nothing promoted** (see [[dark-rag-token-gaps]] for the ds-002 4.02:1 signature that reappears on rag/error/dark).

- **07-16 late — markup ENACTED (sheet REV 2):** Dave picked **C = default** (mode-stable; dv-014 = across theme switch) + **A = high-contrast alternate** (per-chart `data-range`/`data-contrast` token rebind); B retired. Deltas rebuilt as DERIVED values from palette anchors (+ blue neutral + amber, asymmetric 3:1 light / 6.5:1 dark); D1/D2/D3 await pick. **Ranges ruling:** we may CREATE ranges (colour harmonies + scientific criteria), categorised by INTENT (harmony-led / contrast-led); range selection = future edit-mode harness dial → ranges live in TOKENS: generated holding pen `tokens/_proposals/dataviz-ranges.proposals.json` (emitted by the generator; statuses picked-pending-confirm / proposed).

- **07-16 night — REV 3 (second markup batch + article):** NEW Apollo rule from Dave's Tuts+ article: **avoid vibrating boundaries** (adjacent saturated near-complementary equal-value pairs; astigmatism/a11y). Quantified 3-leg check (value-ratio <1.25 + hue-sep ≥135° + sats ≥0.5 — 135° because Dave SAW the dance at 146°); receipts everywhere + advisory gate row; dv-004's ≥2px gap = the structural defence. **D2 = delta pick** with BOTH pairs value-split (receipts caught light mode too); D1 kept-option; D3 retired (mechanism = the fix). **Ranges palette-native only** — Dave: "can't invent anything, only safe in the RAG" (deltas = sole derived zone); ranges widened via family step-ramps 1→5; CVD-diverging retired.

- **07-16 close — V7 CONFIRMED + ENACTED** (Dave: "happy with my initial selection with your adjustments"): `data/series/*` (C) + `data/series-high-contrast/*` (A) + `data/delta/*` (D2) LIVE in `semantic-colour.json`; override + vibration rule recorded as guideline `{#dv-019}` (NB: rules-index ID grammar requires ids to END in the number — `dv-019-apollo` was rejected); statuses `confirmed-2026-07-16` in the holding pens; ranges stay `proposed`. Build green.

- **07-16 final — METHOD DOSSIER RATIFIED** (Dave's markup): approach ratified (SVG+tokens+CSS-motion+table spine, canvas rejected) · gate plan approved · kit spec approved (settles chevron-in-R1) · tiers + hand-rolled-maths stand as defaults. **DataViz has no open blockers.**

- **07-16 later — ROUND-ONE KIT BUILT + gate landed.** `_validate_dataviz.py` (9 blocking + 5 advisory, `--selftest` bite-tests incl. dv-bar-009-never-on-a-line) wired into `_build_all.py` step 22; build green 25/25. All types on ONE file `_proforma/DataViz-interactive.html` (Tranche-N convention; generator `_review/_gen_dataviz_charts.py` bakes static gate-visible SVG, hand-rolled maths). Review copy via `_make_review.py`.
- **07-16 — TWO review-markup rounds ENACTED (5 + 9 pins).** All rulings + WHY now logged in **`knowledge/_proforma/_DATAVIZ-DECISIONS.md`** (the running decision ledger — read it before touching charts). Key standing calls: chevron = GAUGE-ONLY (not stacked); responsive = JS `fit()` compress-width-fixed-text (built blind, needs Dave's in-browser resize check); donut has 3 label variants (letters-on-seg / spider / direct); real tooltips; type = KB `typography.json` scale now (display sizes = 2 new Figma types, 4px-grid). **OPEN:** grouped-column layout awaits Dave's images.

- **07-16 — PARKED, "good enough", NOT signed off (RULED Dave).** After 9 review rounds Dave chose to move on;
  the kit is a **REVISIT target, not DONE**. He will come back to add **filtering, chart titles, and other Layer-2
  controls**, finish the partial interactions, and sign off after an **in-browser** pass (all interactivity so far is
  gate + `node --check` only — never render-checked, no browser in sandbox). `_LIVE-STATE.md` carries the 🟡 PARKED
  entry; flip to DONE only after that sign-off. Commits c0d8db6·baf1f7b·f10b082·f93c2cc·de8cbcb (Dave pushes via Desktop).

**Why:** V7 was deferred 07-02 "for proper renders"; renders + markup rounds resolved the decision stack, then the kit was built gate-first and iterated over nine review rounds, then PARKED as good-enough pending a controls-and-sign-off revisit.
**How to apply:** the kit is BUILT + green. Edit via the generator `_review/_gen_dataviz_charts.py` (never hand-edit the HTML), regenerate, run `_build_all.py`, regenerate the review copy. **Read `_DATAVIZ-DECISIONS.md` first** — it's the running WHY. Full state in `_LIVE-STATE.md`.
