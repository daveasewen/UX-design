---
title: DataViz — the build method (SVG + tokens + CSS motion + table spine)
source: Synthesised 2026-07-16 from the desk research (reviews/DATAVIZ-DESK-RESEARCH-2026-07-16.html) + the ingested HSBC dataviz/colour rules + the supporting-palette proposals
type: pattern-model
status: RATIFIED 2026-07-16 (Dave's dossier markup — approach ratified · gate plan approved · round-one kit spec approved incl. chevron-in-R1; tiers + hand-rolled-maths standing as defaults) · V7 RESOLVED same day (C default + A high-contrast + D2 value-split deltas live in semantic-colour.json; override dv-019) · vibrating-boundaries rule ADDED (Apollo rule) · ranges = palette-native proposals · NOTHING BLOCKS the round-one kit
captured: 2026-07-16
related: _PROFORMA-RULES.md, ../guidelines/data-visualisation.md, ../tokens/_proposals/supporting-palette.proposals.json, ../../reviews/DATAVIZ-METHOD-2026-07-16.html, ../../reviews/DATAVIZ-SERIES-RENDERS-2026-07-16.html
relations:
  refines: dataviz-desk-research            # turns the research verdict into a build method
  informs: dataviz-round-one-kit            # KPI card · line/spark · bar/column/stacked · donut build against this
  governed_by: proforma-rules               # mono base / tokens-only / CSS-motion / real-icons / clean+review pairs all apply
  depends_on: v7-series-assignment          # RESOLVED 2026-07-16 — C default + A high-contrast + D2 deltas confirmed, live in semantic-colour.json
  binds: supporting-palette                 # fills = data/series-* from the V7 winner; RAG tokens candidate for deltas
  gated_by: validate-dataviz                # NEW gate, BUILT + wired into _build_all.py step 22 (lands WITH the first chart)
  realised_by: dataviz-round-one-kit-built  # 4 interactive files in _proforma/ — see "Round-one kit — BUILT" below
  decisions_in: dataviz-decisions           # running review-ruling ledger → _DATAVIZ-DECISIONS.md
dossier: ../../reviews/DATAVIZ-METHOD-2026-07-16.html
---

# DataViz — the build method

Charts are **semantic SVG in the DOM, styled entirely by tokens, animated entirely by CSS,
described by a real table**. Canvas is rejected: it forfeits token styling, per-element motion,
inspectability (= gate-ability) and the accessible tree. Full reviewable write-up:
`../../reviews/DATAVIZ-METHOD-2026-07-16.html`.

## The stack (graph nodes)

1. **Data** — a real `<table>` in the markup (visually hidden under the visual chart). One artefact,
   two obligations: the KB's tabular alternative (dv-005) AND the screen-reader surface.
2. **Geometry** — small behaviour-only JS (rule 14): data → coordinates → SVG + CSS custom
   properties. Maths helper hand-rolled first; vendoring d3-scale is decision 6.
3. **Skeleton** — one SVG skeleton per type, variants via `data-*` (the masthead move). One
   skeleton, N brand modes via token cascade (rule 15) — Apollo mono / HSBC / Apollo UI never fork charts.
4. **Style** — 100% tokens: `data/series-1…5` fills (V7 winner), mode-aware grey building blocks
   ≥3:1 (dv-016), flat fills only (dv-009), DEF-004 applies.
5. **Motion** — CSS keyframes/transitions only (DEF-003); `prefers-reduced-motion` honoured.
6. **A11y** — accessible name/desc; letters A·B·C on elements + in legends (Dave ruling 2026-07-16);
   marker shapes per line series (dv-line-002); `aria-live="polite"` for updates; colour never alone (dv-011).

## The vocabulary model

Intent family (comparison-time · distribution · composition · relationship · indicator) → type →
variant. A variant = a `data-*` reconfiguration, not a new component. Designers pick **recipes**
("Balance trend", "Spend by category", "Budget vs cap", "KPI with delta"), not variants — the
anti-god-chart guardrail. Variant-complete inventory (41 items, tiers R1/R2/M/X) lives in dossier §03.

## Dave's rulings 2026-07-16 (enactment status)

1. **Gain/loss**: use the convention + sign/arrow/position. Scoped override of col26-012 (+ the
   red-once-per-screen interplay) DRAFTED in dossier §04.1 — **wording awaits Dave's sign-off**.
   Delta colour options (RAG tokens vs in-palette pair) on the render sheet.
2. **Texture**: ≤1 chevron `<pattern>` per chart, flat, two-tone from the series token. Gate counts it.
3. **Legends**: [swatch] [letter] · [name]; letters repeat on elements. Kit rule + gate check.
4. **Variant-complete inventory**: enumerated + tiered (dossier §03); reconcile into the itinerary
   on next refresh.

## V7 — series assignment (OPEN, Dave's judgment gate)

Render sheet `../../reviews/DATAVIZ-SERIES-RENDERS-2026-07-16.html`: candidates A (hue-spread
mid-step, recommended) / B (strong-step) / C (mode-stable, carries the dv-014 ↔ col26-017 scope
tension) × both real surface tokens × four chart types; receipts recomputed from hex, all agree
with the proposals file. On sign-off: assignment → `semantic-colour.json` as `data/series-N` per
mode; proposals file's semantic side retires to receipts.

## Gate

`_validate_dataviz.py` (new) + extensions to the indicator-contrast gate; full rule→check→mode
table in dossier §06. Blocking from day one where the check class is proven (rogue-hex, contrast,
counts, gradients, baselines, slice caps, straight lines); advisory-first where genuinely new
(table-presence, letters, spark aspect, journey consistency), promoted after bite-tests
(ADR-0005 §5). **The gate lands WITH the first chart** — a new surface never ships ungated
(pro-forma tranche 6 lesson; icon-gate lesson).

## Round-one kit (build order)

KPI stat card → bar/column (+grouped/stacked) → line (+multi/spark) → donut. "Done" = interactive
mono HTML in `_proforma/` + clean/review dossier pair + KB model doc + all gates green +
render-verified both modes (rule 16 + pro-forma contract).

## Round-one kit — BUILT (2026-07-16, gate-first)

All four types on **one** interactive MONO pro-forma file (Tranche-N convention, per Dave 2026-07-16);
**`_validate_dataviz.py` landed WITH the first chart** and is wired into `_build_all.py` (step 22).
Full build green 25/25.

- `_proforma/DataViz-interactive.html` — the whole round-one kit (13 charts): **KPI stat card**
  (metric · +delta · +delta+spark; delta = sign **+** arrow **+** colour, dv-011 / dv-019 override) ·
  **column · horizontal bar · grouped** (2-series, letters A/B, toggle) · **stacked** (4-series,
  **chevron on one series** = the R1 texture proof, 2px surface-stroke separation dv-004) · **line ·
  multi-series** (per-series marker shape dv-line-002 + letter + colour) · **sparkline** (axis-free,
  wide aspect dv-line-009) · **donut + centre total** (≤6 slices dv-pie-009, sum-to-total dv-pie-010).
- Review copy (mark-up template): `_review/DataViz-interactive-REVIEW.html` — regenerate after edits
  with `python3 knowledge/_review/_make_review.py knowledge/_proforma/DataViz-interactive.html`.

**Geometry helper** (method decision 6 — hand-rolled maths, no d3): `_review/_gen_dataviz_charts.py`
computes nice-ticks / linear scale / stack layout / arc geometry and **bakes static SVG into the DOM**
so every chart is gate-visible (a canvas/JS-injected chart would be invisible to the gate). Runtime JS
is behaviour-only (theme/contrast/series toggle, table toggle); motion is CSS (DEF-003).

**Gate** `_validate_dataviz.py`: 9 blocking checks (dv-009 flat-fills/≤1-chevron · dv-017 palette-only
· dv-016 ≥3:1 **rendered** contrast both modes — the 9/9 declared-pairs blind-spot fix · dv-004
separation · dv-bar-009 zero-baseline bars-ONLY · dv-bar-007 no-negative-horizontal · dv-pie-009
≤6-slices · dv-pie-010 sum-to-total · dv-line-011 straight-lines) + 5 advisory (dv-005 table · §04.3
letters · dv-line-009 spark aspect · dv-014 journey consistency · vibrating-boundaries, metric lifted
from `_review/_gen_series_renders.py`). `--selftest` bite-tests every check (13 cases, incl. the
dv-bar-009-never-fires-on-a-line asymmetry) — a deliberately broken chart MUST fail.

**Standing default flagged for Dave:** gridline contrast is **advisory** (decorative, WCAG 1.4.11-exempt;
3:1 gridlines read heavy) while series-fill + axis/label contrast is **blocking**. Movable before it bites.

**Not done in this pass:** PNG render-verification (sandbox had no browser + the Playwright CDN was
blocked); contrast verified numerically from resolved hex instead (series C ≥3.17:1 both modes/surfaces,
HC set 5–12:1). Review surface = the live HTML.
