---
title: DataViz — review decisions ledger (running)
type: decision-log
status: LIVE — appended every review round; the durable record of what changed and WHY
captured: 2026-07-16
related: _DATAVIZ-METHOD.md, ../_validate_dataviz.py, ../_review/_gen_dataviz_charts.py, ../../reviews/DATAVIZ-METHOD-2026-07-16.html
relations:
  refines: dataviz-method                 # the method dossier is the WHAT; this log is the running WHY of each change
  governs: dataviz-round-one-kit          # every ruling here is enacted in _review/_gen_dataviz_charts.py
  gated_by: validate-dataviz
---

# DataViz — review decisions ledger

The running record of Dave's review rulings on the round-one chart kit, so decisions and their
rationale don't evaporate between sessions (ADR-0007 decision-graph, lightweight-first). Each entry:
the ruling · why · how it's enacted. The clean build is `_proforma/DataViz-interactive.html`
(generator `_review/_gen_dataviz_charts.py`); mark-up copy `_review/DataViz-interactive-REVIEW.html`.

Source of these rulings: the exported review comment-pins on the REVIEW copy (batches dated below).

---

## Standing decisions (in force across the kit)

- **DV-D01 · Consolidate to ONE file.** All chart types live on one interactive file
  (`DataViz-interactive.html`), Tranche-N convention — not one file per type. *(Supersedes the dossier
  §07 "one HTML per component".)*
- **DV-D02 · Responsive = compress width, never scale proportionally, and TEXT MUST NOT SCALE.**
  Enacted as a runtime `fit()` (the method's geometry node at runtime): fixed height + non-scaling
  text, only horizontal positions relayout to container width. Cartesian charts only; horizontal bar
  + donut excluded (compressing a value-axis / circle distorts). Pure enhancement, safe fallback to the
  baked SVG. ⚠️ built without an in-browser test (sandbox has no browser) — needs Dave's resize check.
- **DV-D03 · Gridline contrast = advisory; series-fill + axis/label = blocking ≥3:1**, computed from
  resolved hex in BOTH modes (the 9/9 declared-pairs blind-spot fix).
- **DV-D04 · Chevron/hash texture is reserved for GAUGE-type charts only** — NOT stacked series.
  *(Supersedes the dossier's "chevron proves itself on the stacked column"; capability kept in the
  generator, switched off.)* Batch 2 #5.
- **DV-D05 · Type = the KB scale (`typography.json`: font-5/6/7 = 16/14/12 + weights
  regular/medium/bold).** Display sizes (font-1..4) are the two new Figma display types still to land;
  they will be **4px-grid adjustments** only. `--fs-display` (40px) is a 4px-grid placeholder that maps
  cleanly when they arrive. So the type-token work is **no longer fully blocked** — use the KB scale now.
  Batch 2 #1 + Dave's clarification.
- **DV-D06 · Delta indicators** may use gain/loss colour with sign + arrow (dv-019 override), exempt
  from red-once-per-screen. *(From the ratified dossier; unchanged.)*

---

## Batch 1 — review 2026-07-16 (5 pins)

- **#1 Entry animations + interactions** — wanted, visible. Enacted: bars grow from baseline, lines
  draw, donut segments animate in; hover emphasis; **Replay** button.
- **#2 Responsive** — see DV-D02.
- **#3 Grouped column layout** — Dave to supply reference images. **OPEN — parked pending images.**
- **#4 Donut legend** — moved to the right as a vertical list.
- **#5 Donut labelling** — provide a legend version AND a direct-label version. *(Extended in Batch 2 #7.)*

## Batch 2 — review 2026-07-16 (9 pins)

- **#1 KPI type** — headline bigger + one weight thinner → see DV-D05 (KB scale; `--fs-display` 40px
  4px-grid placeholder; weight → regular 400).
- **#2 Chart toolbar** — a `.dv-toolbar` div ABOVE each chart holds the "View as table" control and is
  built to hold more controls later. Enacted for every chart with a data table.
- **#3 Grouped alphanumerics rise with the bars** — the A/B letters start at the baseline and travel up
  with the grow animation (per-element `--rise` + synced delay), instead of fading in after.
- **#4 Grouped legend centred** — applied to the multi-series legends (grouped/stacked/line) for consistency.
- **#5 Chevron** — see DV-D04 (removed from stacked; gauge-only).
- **#6 Line animation + markers** — (a) builds slower and **sequentially**: each series' line draws in
  turn (`--draw-slow` 1600ms), then its markers land. (b) Markers now carry the series colour as a
  **border** with a toggle to compare **white fill** vs **background fill** (adapts to theme; clearest
  in dark). "See both" = the Marker-fill toggle above the line charts.
- **#7 Donut needs on-chart alphabetic labels even with a legend** — three switchable variants to
  compare: **letters on segments** · **spider-leg letters** (letter on a short leader outside the ring)
  · **direct labels** (full name + value in place, no legend). Batch 1's plain-legend donut is retired
  in favour of these.
- **#8 Donut segments grow sequentially** (scale from the centre, staggered) rather than fade.
- **#9 Real tooltip** — hover/focus on any series element shows a styled tooltip with the figure +
  label (letter · series · category · value), not just a hover state. `data-tip` + a single fixed
  tooltip element; keyboard-focus supported.

---

## Batch 3 — review 2026-07-16 (8 pins + 2 mid-review)

- **#1 + #8 Table = right-hand DRAWER, chart compresses to fit.** The View-as-table control now opens a
  drawer on the right of the **chart** (not the page edge); the chart-area shrinks and `fitCharts()`
  relayouts it. Applies to every chart. `assemble()` wraps each figure as `[chart-area | drawer]`.
- **#2 Stacked = sequential TOP-to-BOTTOM** — top segment grows first, each waits for the one above
  (per-segment delay/duration ordered by stack position).
- **#3 Multi-line strictly sequential** — series line draws (700ms), then its symbols, THEN the next
  series starts (block-sequenced), for single- and multi-series lines.
- **#4 + #5 Marker rework** — CSS-driven from each marker's `--sc` (series colour). **White** = white
  fill + series-colour border at **line width (2.5)**; **Background** = series-colour fill + page-colour
  border. Toggle compares them (clearest in dark).
- **#6 Horizontal bar joins the fit system** — horizontal-only scaling, no type scaling; bar length =
  value fraction of plot width, value-axis + gridlines relayout. *(Supersedes Batch 2's exclusion.)*
- **#7 Donut = RADIAL sequential sweep** — segments grow their arc 0→extent one after another (JS,
  `requestAnimationFrame`; arc params on each segment; reduced-motion + no-JS leave the baked donut).
  Replaces the scale-from-centre pop; keeps the sequential concept Dave liked.
- **Responsive width SLIDER (mid-review)** — a preview-width control in the chrome, **starts at 1024**
  (min 360), drives a `.dv-frame` width + `fitCharts()` so responsive behaviour is previewable without
  resizing the window. Charts are full-size at 1024 and compress below.

## Batch 4 — review 2026-07-16 (6 pins)

- **#1 + #3 Table drawer = frosted OVERLAY, chart keeps its width.** *(Supersedes Batch 3 #1/#8's
  compress-to-fit.)* The drawer no longer pushes/compresses the chart — it overlays the right of the
  chart, sized to the table + padding (#1), with a **white background + backdrop blur** (#3). Dark text
  tokens (`--drawer-ink/-ink2/-line`) keep it legible on the white panel in both themes.
- **#2 Donut no flash.** Segments are baked `visibility:hidden` so the full arc never paints before the
  sweep; noscript + reduced-motion reveal them.
- **#4 Stacked order = bottom-up.** *(Supersedes Batch 3 #2's top-to-bottom.)* Series 0 (baseline)
  animates first, each waits for the one below.
- **#5 + #6 Lines + symbols build simultaneously.** *(Supersedes Batch 3 #3's strict sequencing.)* All
  series lines draw together; each symbol lands as the line reaches it (marker delay tracks draw progress).

## Batch 5 — review 2026-07-16 (3 pins)

- **#1 Donut flicker fixed (properly).** Root cause: each segment was revealed one frame before its arc
  collapsed, so the full arc painted for that frame. Now the collapse (`d`→zero) and reveal happen in
  the SAME synchronous tick per segment; pending segments stay hidden. No full-arc flash.
- **#2 Drawer doesn't scroll — extends beyond the chart.** Removed the panel's `max-height`/`overflow`;
  it sizes to the table and overflows the chart bounds if taller (e.g. sparkline).
- **#3 Drawer is solid white, no frost.** *(Supersedes Batch 4 #3's backdrop-blur.)* `--drawer-bg` opaque
  white, blur removed. Applied to all drawers for consistency (was pinned to the horizontal-bar one).

## Batch 6 — review 2026-07-16 (3 pins)

- **#1 Donut easing — first + last only.** Ease-out on the first segment, ease-in on the last, the
  middle segments linear (a gentle start and a soft stop, steady through the middle).
- **#2 Labels/legs sequenced.** For spider + direct (and letters-on-segment for consistency), each
  label and leader line fades in as its own segment grows (`.dv-anno[data-seq]` + JS `.show`).
- **#3 Line slower + gentler.** `--draw-slow` 1600→2400ms with a smoother easing; symbols still appear
  as the line reaches each point (marker timing tracks the slower draw), so the build isn't harsh.

## Batch 7 — review 2026-07-16 (3 pins)

- **#1 Donut easing swapped** — ease-**IN** on the first segment, ease-**OUT** on the last (reverse of
  batch 6), middle linear.
- **#2 Line symbols keep pace** — the symbol sequence runs for the same duration as the line draw
  (2400ms), the last symbol completing with the line (minus its fade), so symbols finish in sync.
- **#3 Stacked easing = donut's** — ease-in on the first (bottom) segment, ease-out on the last (top),
  middle linear (per-segment `animation-timing-function`).

## Batch 8 — review 2026-07-16 (1 pin)

- **#1 Line nodes follow the line's easing.** The symbols were on a linear cadence while the line eased,
  so they trickled in and read as slow. Node delays now follow the line's easing curve
  (`line_node_delays()` inverts the cubic-bezier) — each node lands as the drawing head passes it, fast
  through the middle, matching the line.

## Open / pending

- **Grouped column layout redesign** — awaiting Dave's reference images (Batch 1 #3).
- **DV-D02 responsive** — needs an in-browser resize check by Dave (built blind; safe fallback).
- **Two new Figma display types + 4px-grid type tokens** — land the real display scale, replace
  `--fs-display` placeholder (DV-D05).
