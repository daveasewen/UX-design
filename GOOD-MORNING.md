# Good morning, Dave ☕

*Briefing — written end of 2026-07-16 (late), session **"DataViz method dossier + V7 series decision."** Read this → `_LIVE-STATE.md` (LIVE + OPEN) → then build. Dense on purpose.*

## The session in one line
DataViz went from research to **fully decided in one evening**: method dossier written + **RATIFIED**, V7 series colours **decided on real renders and PROMOTED to live tokens**, a **new vibrating-boundaries a11y rule** (your article) quantified and recorded, deltas fixed for the shimmer you spotted, ranges parked as palette-native token proposals. **Nothing blocks the build.**

## ⏭ FIRST TASK — build the round-one chart kit, GATE-FIRST
The whole decision stack is closed. Order (per the ratified dossier §07):
1. **`_validate_dataviz.py` FIRST** — the gate lands WITH the first chart, never after (pro-forma tranche lesson). Blocking set: flat-fills/no-gradient (≤1 chevron `<pattern>`), palette-only fills bound to `data/*` tokens, ≥3:1 building blocks, ≥2px separation, zero baseline (bars ONLY — never fire on lines, dv-line-001 asymmetry), no negative horizontal bars, ≤6 slices, sum-to-total, straight lines (no C/S/Q in series paths). Advisory-first: table-presence, letters-on-elements, spark aspect, **vibration check** (adjacent pairs: value-ratio <1.25 AND hue-sep ≥135° AND sats ≥0.5 = fail-candidate; skip dv-004-gapped pairs; dv-019). Wire into `_build_all.py` + bite-test each check (a deliberately broken chart must fail).
2. **KPI stat card** (metric · +delta · +delta+spark) → 3. **bar/column** (+grouped/stacked; chevron proves itself on the stacked column) → 4. **line** (+multi/spark) → 5. **donut** (+centre total).
- **Done per component** (rule 16 + pro-forma contract): interactive MONO html in `knowledge/_proforma/` · clean+REVIEW dossier pair · KB model doc with typed relations · all gates green · render-verified both modes.
- Build per the ratified stack: data = real `<table>` (a11y spine + dv-005) · geometry = behaviour-only JS, **hand-rolled maths** (default stands; d3-scale only when time-axes demand) · one skeleton per type, variants via `data-*` · styling 100% tokens · CSS-only motion.

## Decided — do NOT re-open (all RULED/CONFIRMED Dave 2026-07-16)
- **Approach RATIFIED**: semantic SVG + tokens + CSS motion + hidden-table spine; canvas rejected.
- **Series tokens LIVE** in `semantic-colour.json`: `data/series/1–5` (candidate C, mode-stable — dv-014 held ACROSS the theme switch) · `data/series-high-contrast/1–5` (candidate A; per-chart `data-contrast`/`data-range` rebind — every chart carries the switch) · `data/delta/{gain,loss,neutral,warning}` (D2, both pairs value-split; derived = the ONLY invented-colour zone, "only safe in the RAG").
- **`{#dv-019}`** in `guidelines/data-visualisation.md`: scoped gain/loss override (delta indicators only, never series fills, exempt from red-once-per-screen) + the **vibrating-boundaries rule** (Apollo-added, from Dave's Tuts+ article; astigmatism/a11y; NB the rules-index ID grammar rejected `dv-019-apollo` — ids must end in the number).
- **Ranges = palette-native ONLY** (no invented series colours), parked as `proposed` in `tokens/_proposals/dataviz-ranges.proposals.json` — the future edit-mode harness dial. Suggestion ranges widened across step-ramps 1→5.
- **Standing defaults** (movable before they bite): inventory tier boundaries as drawn (dossier §03) · hand-rolled maths.

## Where everything lives
`reviews/DATAVIZ-METHOD-2026-07-16.html` (ratified method, 41-item inventory, gate map §06, kit spec §07) · `reviews/DATAVIZ-SERIES-RENDERS-2026-07-16.html` (REV 3 decision record, vibration receipts) · `knowledge/_proforma/_DATAVIZ-METHOD.md` (KB model doc) · generator `knowledge/_review/_gen_series_renders.py` (owns the sheet + ranges proposals; vibration metric lives here — lift it into the gate).

## On your desk
- **Push via GitHub Desktop** (if not already): `966f0d1` (tokens batch) + `b1fd725` (ratification) + this briefing refresh. Sandbox commits worked tonight via the mv-lock dance; locks parked in `_to_delete/gitlocks-20260716/` — delete that folder (and any `.git/objects/**/tmp_obj_*` scraps) from your side when convenient; the sandbox can't.
- Dossier §08 items 5/6 stand as defaults — flag any time.
- Playwright in-sandbox renders working (headless-shell recipe in memory); review surface = live HTML as always.

## Queue after round-one (from `_LIVE-STATE` OPEN)
- DataViz R2 tier (area/stacked-area · diverging · butterfly · waterfall · bullet · progress/gauge · in-table patterns) + Layer-2 interactions (drill-down, cross-filter).
- **Tranche 8** (BottomTabBar · InPageNav · FooterNav · RelatedLinks · Stepper) + Shell/footer template tier.
- **Type-token system** — still blocked on your Figma file.
- Sidequests (harvest later): research knowledge-graph · Swiss state-ledger viewer · component catalog.

> Opener: **"Title this chat: Round-one chart kit — gate first."** Then GOOD-MORNING → `_LIVE-STATE.md` → `reviews/DATAVIZ-METHOD-2026-07-16.html` §06+§07 → build.
