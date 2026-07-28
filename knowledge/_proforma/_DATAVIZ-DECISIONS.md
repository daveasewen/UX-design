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
  Edges: supersedes(DV:DOSSIER.s07)
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
  Edges: supersedes(DV:DOSSIER.chevron)
- **DV-D05 · Type = the KB scale (`typography.json`: font-5/6/7 = 16/14/12 + weights
  regular/medium/bold).** Display sizes (font-1..4) are the two new Figma display types still to land;
  they will be **4px-grid adjustments** only. `--fs-display` (40px) is a 4px-grid placeholder that maps
  cleanly when they arrive. So the type-token work is **no longer fully blocked** — use the KB scale now.
  Batch 2 #1 + Dave's clarification.
- **DV-D06 · Delta indicators** may use gain/loss colour with sign + arrow (dv-019 override), exempt
  from red-once-per-screen. *(From the ratified dossier; unchanged.)*
  Edges: bounds(dv-019)
- **DV-D07 · Chart chrome = two-channel roles: snapped colour + declared alpha slot (2026-07-23).**
  Mints `data/axis` + `data/grid` — closes worker-D's receipted quiet-ink gap (post-R-D16 homeless
  greys). Each role = per-mode COLOUR snapped to the neutral ramp (`$alias → color/neutral/*`;
  starting values axis 7 light / 9 dark · grid 12 light / 6 dark per the Q6 sheet — Dave may
  re-dial on it) **+ a declared ALPHA slot, default 1.0** (ADR-0010 posture: a flex slot only a
  theme pulling the alpha lever populates). Dave, verbatim: *"I still want to keep the flexibility
  of having alpha as the method for styling … store a null or 100% value plus the colour[;] going
  forward I need max flexibility so creating new themes has many levels to pull on."* Extends the
  ADR-0009 two-channel physics (colour substrate + optional opacity layer) beyond states to
  component chrome. Gate consequence at enactment: where a theme sets alpha < 1, dv-016 / DV-D03
  contrast computes from the COMPOSITE (colour × alpha × ground), never the stored hex alone.
  `data/target` deferred — mints only with the threshold feature (chart-revisit Q4). Enactment
  rides the chart-revisit pass: rebind the five snippets' `--axis-alpha`/`--grid-alpha` idiom onto
  the roles (the two-var CSS shape already matches). Decision sheet:
  `reviews/DATA-AXIS-GRID-2026-07-23-v1.html` (+.REVIEW copy).
  Edges: refines(ADR-0010, scope=dataviz-chrome-roles) · refines(ADR-0009, scope=two-channel-beyond-states)

- **DV-D08 · Chart text ladder: 12/500 floor + 700 emphasis; 600 stays off-brand (2026-07-23).**
  Settles the Q8 label-weight seam via the bar audit (B2, `reviews/BAR-CHART-AUDIT-2026-07-23-v1`).
  Dave: *"at 12 — medium is the floor."* At the 12px chart floor: labels · axis · legend text ·
  values = **12/500** (values keep tabular numerals). Emphasis channel = **700**: legend alphas
  (his donut reference image — the kit's 600 maps to 700; the weight set {100,300,400,500,700}
  stands, 600 admitted nowhere) and on-chart keys (kit 700 restored). Supersedes BOTH the kit's
  400-label/600-value pair AND the 07-22 uniform-500 snap (`99fcb6d`) — the flattening the audit
  surfaced. Enactment = composite mints + rebind, rides the chart-revisit lane (worker); retro-
  propagates as swaps. PARKED exploration (`_FUTURE-STATE`): a separate mini chart type ramp,
  floor 12 / ceiling 20 — *"we can explore later."*
  Edges: refines(DV-D05, scope=chart-floor-weight-ladder)

- **DV-D09 · Bar-family canon defaults are ORIENTATION-DISTINCT; hue is a placeholder until edit
  mode (2026-07-23).** Audit B3, Dave's reframe verbatim: *"I don't care what colour it is as long
  as the default for horizontal in the canon is different from the vertical. We have an edit mode
  planned[;] the designer can choose at [that] time, after the screen generation in Apollo."*
  Enact: column default = `series-1`, horizontal default = `series-3` (#577C78 — the kit's
  original, restored). Scope: dv-014 journey-consistency governs COMPOSED JOURNEYS (same data
  twice in one journey = same series) — worker D's correction survives as a journey rule; the
  canon pair showing distinct defaults is by design, not inconsistency. Product fact recorded:
  the planned Apollo EDIT MODE (post-generation designer choice) is the surface this defers to
  (`_FUTURE-STATE`).

- **D-Q3 RULED (2026-07-23, audit B1):** grouped + stacked column **PROMOTE** into canon in the
  chart-revisit wave (bar lane). The Batch-1 #3 grouped-layout-redesign open (reference images)
  stays open — promotion ≠ redesign.

- **DV-D10 · Series identity comes OFF the plot where a mark can't guarantee its own page-air;
  proximity + shape + name replace the on-chart letter (2026-07-24).** Dave, on the combo line-end
  key colliding with the dark bars under responsive reflow (his three render frames: on-dark /
  overlapping-the-axis / in-page-air): *"we can't guarantee that it will always sit on the bar."*
  Ruled by eye on `reviews/COMBO-LABELLING-SOLUTIONS-2026-07-24-v1.html` (four live panels, shared
  width slider). The split, by chart type:
  - **COMBO (bar + line):** the line-end letter key is REMOVED from the plot. Series identity moves
    to **axis-proximate legend lockups** — the bar set's lockup by the primary (left) axis, the line
    set's by the secondary (right) axis — each carrying a **swatch that MIRRORS the on-chart mark**
    (filled chip = the bar; short line + node = the line) + the **series name**. Proximity (which
    axis) + shape (which mark) + name carry identity; nothing rides a position the layout controls.
  - **LINE alone:** KEEP the direct end-label — **shape + letter** (belt-and-braces) — because a lone
    line's end sits in guaranteed page air (no bars to collide with). The **letter is the droppable
    channel** once shape + a named direct label are both present (WCAG 1.4.1 is already satisfied);
    Dave is confirming with his accessibility team before dropping it. Until then it stays.
  - **Standards basis (checked this session):** our dv-006 "values on both axes" is a **TOOLTIP**
    requirement, not permanent both-axis labels; dv-011 / §04.3 "colour never the only channel" is
    met by **shape AND text**; the `<table>` spine is the WCAG complex-image long description
    (dv-005). W3C: direct labelling is *preferred* over legends (lower cognitive load), and 1.4.1
    wants a non-colour channel — *"convey key info with text, don't rely solely on shape+colour."*
    The lockup keeps the name as text, so it clears the nuance.
  - **Relationship to O1:** this REMOVES the combo end-key from O1's scope. The scoped inverse-surface
    (ADR-0014, 2026-07-24 addendum) is reserved for text that genuinely MUST sit on a dark ground —
    dark page sections / cards, and the donut's on-segment keys — not the combo's labelling.
  Enactment rides the O1 build: rebuild Chart-combo's legend as the two axis-proximate lockups +
  strip the `.dv-endkey`; Chart-line keeps its end-key pending Dave's a11y check.
  Edges: refines(dv-011, scope=combo-series-id-non-colour-channels) · relates(ADR-0014, scope=O1-inverse-surface-boundary) · bounds(dv-006, scope=both-axes-is-tooltip-not-permanent-label)

- **DV-D11 · The LEGEND MODEL — dual gesture, two fade levels, additive isolate (2026-07-26).**
  Signed off by Dave on `reviews/LEGEND-ISOLATE-TOGGLE-PROTOTYPE-2026-07-24-v5.5.html` (*"good
  done, love this"*; fading interaction ruled done same session on v5.4: *"we're done with these
  as far as fading interaction goes"*). The model, in full:
  - **Two gestures per row:** SWATCH = checkbox (`role="checkbox"`, Space/Enter) · LABEL = isolate
    (exclusive toggle-button, `aria-pressed`, NOT a radiogroup — resting state is "all shown").
    Structure: swatch sits OUTSIDE the isolate button (a button can't nest an interactive checkbox).
  - **Two render levels — full / ghost(12%). Nothing ever fully disappears.** Unchecking a swatch
    ghosts that series to 12% (opacity, `pointer-events:none`; layout preserved). ⚠ ARC, both
    beats: v5.3 built a THREE-level ladder (full / ghost / gone-at-0%) with the checkbox fully
    removing — Dave reversed to two levels the next session ("retune — checkbox also ghosts").
    An unchecked series and an isolate-ghosted series are visually identical mid-chart; the
    legend row state (hollow swatch vs blank-in-isolate) disambiguates. Ruled, not residue.
  - **Isolate = ADDITIVE FOCUS MODE** (Dave's spec verbatim: *"On isolate mode the checkboxes
    should be blank, with a border, and the check should add segments in this mode"*). Entering
    isolate seeds a focus set {series}; the other checkboxes render BLANK (hollow + border);
    checking one ADDS that series at full. The outside-isolate checkbox mix is untouched during
    isolate, so release (click the active label again, or Reset) restores it exactly.
  - **Hover fires in BOTH modes** ("let's try 1"): hovering an active row fades the other ACTIVE
    series to 24% (ghosts stay 12%); hovering a GHOSTED row PEEKS it at 24% — an add-preview.
    Fade ladder: full ▸ 24% hover/peek ▸ 12% ghost. Hover ladder values: hover/peek `.is-faded`/
    `.is-peek` 24% (raised from 18%, Dave 2026-07-25) · ghost `.is-ghost` 12%.
  - **Chrome:** off/hidden row = RESTING (row keeps line border + ink text; only the swatch goes
    hollow + grey-primitive border) · Reset canon-disabled by default (the B-D4 pattern), enables
    on any ghost or isolate · square swatches · no strike-through, no "only" text · sr-only
    live region announces every state change · every control carries the 44 target via the
    invisible `::before` (swatch grows LEFT into the gutter, component-invariant per Dave's
    2026-07-25 swatch ruling).
  - Open edge (flagged at build, unruled): unchecking the SEED series while others sit in the
    focus set leaves the isolate ring on a blank row — kept simple; rule if it grates.
  Enactment: the donut+bar+combo wave bakes this into `dv-behaviour.js` (three-state paint +
  focus-set isolate), replacing the current hide-at-0% legend logic. Prototype = the reference
  implementation (v5.5); v5/v5.1–v5.4 retained on disk as the decision arc.
  Edges: refines(DV-D10, scope=legend-lockup-interaction-layer) · relates(B-D4, scope=reset-disabled-pattern)

- **DV-D12 · Donut sweep easing = trapezoidal velocity keyed to SEGMENT SPANS (2026-07-26).**
  Signed off within the same v5.x arc (built v5.2, 2026-07-25, restoring a finesse the v3→v5.1
  rebuild silently flattened to linear). Spec: the radial-sweep intro eases IN across exactly the
  FIRST segment's arc, runs LINEAR (constant angular speed) through the middle, eases OUT across
  exactly the LAST segment's arc. Cruise speed `V=(S+w1+wN)/dur`; accel `ta=2·w1/V`, decel
  `td=2·wN/V`; rest→rest, monotonic, flat cruise (verified numerically at build). Degenerate case
  (no interior): single ease-in-out. NOT a global bezier — the profile is data-keyed, so a long
  first segment gives a long ramp by design (segment A = 147° → ~441ms of 850ms; Dave saw it and
  signed off without a tune). Enactment: the wave carries `sweepDonut`'s profile into
  `dv-behaviour.js`, replacing the linear sweep.
  Edges: refines(DV-D01, scope=donut-intro-motion-spec)

- **DV-D13 · The Value⇄Percent seg drives EVERY numeric surface; the centre figure follows the
  SELECTION (2026-07-26).** Dave: the seg changing only the centre figure read as confusing —
  *"the tooltip should only have the number-type that you select"* + *"the figure in the middle
  should change dependent on what's selected."* Ruled model:
  - **Tooltip is TYPED:** it carries ONLY the seg-selected number-type — Value → `A · Housing:
    £950` · Percent → `A · Housing: 41%` — never both. Mechanism: marks carry
    `data-tip-value`/`data-tip-percent`; the seg rewrites `data-tip` (dv-behaviour reads it live
    at hover-time, no re-wire).
  - **Centre figure follows the LEGEND SELECTION:** value + percent recompute over the ACTIVE
    series (the isolate focus set, or the checkbox mix) — isolate Housing → 950 / 41%; percent =
    the active sum's share of the GRAND total.
  - **⚠ Deliberate a11y asymmetry (agent call, Dave-visible, unreversed):** `aria-label`s keep
    BOTH forms — a screen-reader user shouldn't lose data to a toggle they may not perceive.
    Confirm or retune at the wave's a11y pass.
  Enactment: wave bakes typed tips + selection-following centre into `dv-behaviour.js` +
  `Chart-donut.reference.html` (and any chart carrying the value⇄percent seg).
  Edges: refines(DV-D11, scope=seg-numeric-coherence) · bounds(dv-006, scope=tooltip-carries-selected-type-only)

- **DV-D14 · dv-004 separation is satisfied by GEOMETRY on gridded plots, not by a surface-coloured
  stroke (2026-07-27).** Dave ruled against the agent's recommendation, on the evidence. The agent
  had proposed reusing the donut's 2px `stroke="var(--page)"` mechanism; Dave: *"I prefer the geometry
  the border will obscure gridlines, may I know why you recommend borders?"* — and then supplied the
  governing fact: *"btw the gap is only 2px minimum, this is in the dataviz specifications in the KG."*
  - **Why the donut precedent does not transfer:** `cb5` carries **5 full-width `.dv-grid` lines behind
    the columns; the donut carries none.** An SVG stroke straddles its path, so a 2px page-coloured
    stroke puts 1px OUTSIDE each rect and paints over every gridline down both sides of all 4 columns.
    ⇒ **A surface-coloured stroke only simulates separation when the thing behind it IS the surface.**
  - **Ruled shape — variant A, both ends pinned:** baseline stays at `y=230` and each stack top stays at
    its TRUE total, so every column still reads correctly against the gridlines and the y-axis. The
    4px (2 boundaries × 2px) comes out of segment heights, proportionally. **Accepted cost, stated at
    ruling time: segments understate by 2.0–2.6%, worst on the shortest column.**
  - **2px is a FLOOR, not a target** (Dave, verbatim above) — a larger gap passes.
  - ⚠ **The finding this exposed, and it outranks the chart:** dv-004's rule text is mechanism-NEUTRAL
    (*"minimum 2px separation between colour blocks"*) but `_validate_dataviz.py` had implemented it as
    *"must carry a surface-coloured stroke >=2px"*. **The gate had silently narrowed the rule into one
    mechanism**, so the only "compliant" answer available to an agent reading the gate was the wrong one
    for this chart. The gate now accepts EITHER mechanism; unmeasurable geometry still demands the stroke
    (fails safe). Held open as a CLASS in `_FUTURE-STATE.md` (Dave's forcing-function idea).
  Enactment: `Chart-bar.reference.html` cb5 re-geometried; `_validate_dataviz.py` `_rect_stack_gap()`.
  Proof: `knowledge/_verify_dv_stacked_enactment.py` — **2.00px on all 8 boundaries**, licensed cut,
  snippet AND showroom pane, 1180 AND 760.
  Edges: refines(dv-004, scope=mechanism-neutral-separation) · supersedes-mechanism(dv-004-stroke-only)

- **DV-D15 · Type drawn ON a series fill gets its own semantic role — `data/text/on-series` MINTED
  (2026-07-27).** Dave's promotion (derivation governance). The stacked alpha keys had been declaring
  `var(--page)`, which renders white today only because of where the neutral ramp sits — **a coincidence,
  not an intent**; on a dark-page theme they would resolve dark and vanish into the fill. Dave:
  *"we have a declared token schema for light-mode with dark surface, can we use this… will it be hard
  coded"* — the `data/*` namespace held **no** text-on-fill role at all, so this is a mint, not a lookup.
  - **Shape:** `data/text/on-series` → `color/grey/white`, **pinned in BOTH modes**, modelled on the
    proven `rag/text/on-dark`. **Deliberately carries NO alpha channel**, unlike its `data/axis`,
    `data/grid` and `data/target` siblings: **DV-D07** requires contrast to compute from the composite
    (colour × alpha × ground), so an alpha slot here would be a route to a key that passes on the stored
    hex and fails on screen — the ds-013 shape. Full opacity is the contract.
  - **type26-013 does NOT collide,** contrary to the prior handoff's fear: the rule reads *"Black/dark-grey
    on light · white/light-grey on dark"* — white on a dark series fill sits inside the first clause; the
    "white-only" restriction is specific to RED grounds. Checked, not assumed.
  - **The blanket `text.dv-barkey{fill:var(--ink)}` is split by GROUND:** ink for cb4's keys on page air,
    `--data-text-on-series` for cb5's keys on fills, with an anti-false-fix comment. A CSS rule beats an
    SVG presentation attribute, which is how one blanket rule silently overrode all 24 keys' declared fills.
  Proof: `_verify_dv_stacked_enactment.py` — **5.26 / 5.04 / 4.61:1** vs AA's 4.5, all four render contexts.
  ⚠ **MEASURED worst case is 4.61:1 on series-3, margin 0.11** — the prior handoff predicted "≈5:1".
  Recorded as measured. **Series-3 cannot be lightened without breaking AA here.**
  Edges: refines(DV-D07, scope=composite-contrast-no-alpha-slot) · bounds(type26-013, scope=white-on-series-fill-permitted)

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

## Batch 9 — review 2026-07-16 (1 pin)

- **#1 Line + nodes now truly share one easing.** Root cause the node-easing didn't fix: the polyline's
  `stroke-dasharray` was a fixed 2400 while the real drawn path is only ~500 units, so the LINE finished
  drawing in the first ~20% of the timeline (then sat still) while the nodes ran the full duration —
  they looked like different easings because the line effectively wasn't easing across the timeline at
  all. Added `pathLength="2400"` to normalise the path so the dash-draw spans the whole animation (and
  it's immune to the responsive rescaling). Now the line and the eased node cadence share one timeline.

## Batch 10 — Dave's flags, 2026-07-27 (session #6) — RULED SAME SESSION, NOT YET ENACTED

*Captured at the moment of the ask, before any build, per **ds-017**; read back as explicit options and
**ruled by Dave in the same window**. Dave's words are quoted verbatim. ⚠ **RULED ≠ ENACTED — nothing
below has been built, and nothing below has been render-verified.***

> **★ THE RULINGS (Dave, 2026-07-27 session #6, option-select read-back then a same-session reversal):**
>
> **⚠⚠ DV-D16a — REVERSED WITHIN THE SAME WINDOW. BOTH WORDINGS KEPT, per the reversal rule
> ([[memento-framing]] — a reversal in the ledger can never read as agent drift).**
> **① FIRST WORDING, ruled then superseded ~20 minutes later — DO NOT BUILD THIS:** *"segment by
> segment — segment 2 starts when segment 1 lands. Serial, not staggered, not a single shared rise."*
> Selected by Dave from a three-option read-back.
> **② SECOND WORDING, IN FORCE — CONCURRENT GROWTH ON ONE SHARED TIMELINE.** Dave, verbatim:
> *"they all grow at the same time, so they are floating and growing, rather than growing and
> 'handing off' to the next."* **Every segment animates simultaneously.** Because a stack's upper
> segments are anchored to the top of the segment below, growing them all at once makes the upper
> ones **FLOAT upward while growing** — that float is the effect, and it is what *"sequentially from
> the bottom"* meant. The **easing shape from the original ask is unchanged and is the durable part**:
> first (bottom) `ease-in` · last (top) `ease-out` · all intermediates `linear` — **per-segment curves
> on ONE timeline**, not per-segment timelines.
>
> **⚠ WHY THE FIRST WORDING WAS WRONG, and it is a METHOD finding, not a Dave finding.** The
> read-back offered three shapes — serial · one-rise-revealing-in-order · fixed stagger — and
> **the correct answer was in none of them.** Dave picked the closest available option; twenty minutes
> later he described what he actually meant, and it rejected the option he had picked, in its own
> words (*"rather than growing and 'handing off' to the next"* is a direct rejection of the serial
> wording). ⇒ **An option-select read-back can only surface answers the asker thought of, and a
> selection from a wrong option set reads exactly like a ruling.** It is a *better* instrument than an
> open question — it produced the correction — but **it manufactures false confidence when the option
> set is incomplete.** ⇒ **Standing mitigation: when reading back a MOTION or FEEL decision, describe
> the resulting sensation, not just the mechanism** — *"the top blocks float as the bottom grows"*
> would have been recognised or rejected instantly; *"segment 2 starts when segment 1 lands"* was not.
> *(Sibling of [[feedback-clarify-reflect-back]]; the reflect-back happened and still under-determined
> the answer.)*
>
> **DV-D16b · scope = EVERY STACKED SURFACE**, not Chart-bar alone.
> **★ DV-D18 · CAP STACKED SEGMENTS AT 6 for now** — Dave: *"Lets cap at 6 for now."* Aligns stacks
> with `dv-pie-009`'s existing donut cap; remainder buckets to **"Other"**.
> **★★ FLOATED, Dave's, for a later window — THE "OTHER" BUCKET MUST BE EXPANDABLE.** Verbatim:
> *"all bucketed 'other' segments should be expandable, through some mechanism we'll explore later."*
> **Not designed, not scoped, deliberately.** ⚠ **This binds the cap:** DV-D18 is only acceptable
> *because* the bucketed data stays reachable — **shipping the cap without a route to the detail
> would be data loss dressed as legibility.** Applies to the donut's existing `dv-pie-009` cap too,
> which today buckets with no expansion route. Filed to `_FUTURE-STATE.md`.
> ⚠ **NOTE THE JUSTIFICATION SHIFT, recorded rather than quietly re-argued:** the ≤6 cap was offered
> as an answer to *duration scaling under serial motion*. **The reversal to concurrent motion dissolves
> that problem entirely** — a 9-segment stack on one shared timeline takes exactly as long as a
> 3-segment one. **The cap still stands on Dave's word, but it now rests on LEGIBILITY alone, not
> duration.** Re-test it on that basis rather than inheriting the original rationale.
> **DV-D17 · RELEASE ISOLATION ENTIRELY** on the second check-on (`st.isolated = null`).
>
> **⚠ FINDING AT RULING TIME — "every stacked surface" is TODAY A SET OF ONE.** Measured, not assumed:
> `stacked` appears **12×** in `snippets/Chart-bar.reference.html` and **0×** in `Chart-combo` and
> `Chart-line`; **stacked area does not exist yet** (chart-expansion lane 3, unbuilt) and the
> grouped/stacked promotion (D-Q3 / ruling-batch #14) is **ruled but not enacted**. ⇒ **The scope choice
> does not enlarge this window's build; it makes DV-D16 FORWARD-BINDING.** Every stacked surface that
> lands from here inherits it. **Carry it into the chart-expansion brief** (`GOOD-MORNING` §C·1a lane 3
> stacked area + the D-Q3 promotion) or the next wave will build stacked surfaces that don't animate.
>
> **✅ `prefers-reduced-motion` — CONFIRMED BY DAVE ("fine"): it ships WITH the first enactment**, not
> after. Accessibility floor, ADR-0004 / WCAG 2.2 AA. ⚠ **"Reduced" is not "none"** — the honest
> reduced-motion form of this is the final state rendered immediately, or a single opacity fade; do
> **not** ship a version that merely shortens the duration and call it satisfied.
> **⚠ THE DURATION QUESTION IS NOW MOOT — recorded because its disappearance is itself the evidence
> the reversal was real.** Under the superseded serial wording, total duration scaled with segment
> count and needed a ruling (fixed per-segment vs fixed total). **Under concurrent motion there is one
> timeline, so N does not affect duration at all.** No ruling needed; the question is closed by the
> reversal, not by an answer.

- **DV-D16 · Stacked chart animates SEQUENTIALLY FROM THE BOTTOM, with a shaped easing cadence.**
  Dave, verbatim: *"the stacked chart should animate sequentially from the bottom, same as the pie,
  ease-in for the first, ease-out for the last, and linear for everything in between."*
  **The easing rule is unambiguous and is the durable part:** first segment `ease-in` · last segment
  `ease-out` · all intermediate segments `linear`. Reads as one continuous gesture — the stack starts
  gently, runs at constant speed, settles gently — rather than N independently-eased segments, which is
  why the middle is linear. Sibling of the existing line/node shared-timeline ruling (Batch 9 tail).
  **RULED (2)** → **⚠ first "segment by segment", then REVERSED same session to CONCURRENT growth on
  one shared timeline — see the ⚠⚠ block above; wording ② is in force.** **RULED (3)** → **every
  stacked surface** (see the forward-binding note above).
  **✅ (1) ANSWERED 2026-07-27 (session #7), by reading the repo, not by asking Dave — AND IT IS A
  FINDING.** `sweepDonut()` (`snippets/Chart-donut.reference.html:889–945`) runs **ONE timeline**:
  a single `dur = 850`, one `t0`, one rAF loop, and **one sweeping angle** `angAt(t)` crossing the
  whole ring. Segments only *appear* to hand off because one angle crosses them in order. Its
  velocity envelope is explicit — accelerate through the first segment's arc (`ta`), cruise (`tc`),
  decelerate through the last (`td`) — i.e. **Dave's easing rule is ALREADY implemented there, as one
  continuous curve rather than N per-segment timelines.** `prefers-reduced-motion` is baked at
  `:901–906` (land on the final frame, never animate).
  ⇒ **"same as the pie" is TRUE OF THE EASING AND FALSE OF THE APPEARANCE under wording ②.** The
  donut is serial-*looking*; ② explicitly rejects that look for stacks. **What carries over is the
  architecture (one shared timeline), the easing envelope, and the reduced-motion answer** — reuse
  those, do **not** reuse the appearance, and do not cite the donut as a visual precedent for ②.
  **⚠ SCOPE MEASURED, and it re-prices DV-D16 DOWNWARD — re-derive before building, do not inherit
  this line.** `Chart-bar.reference.html:121–128`: stacked segments already run `scaleY(0)→1` from
  `transform-origin:bottom`, **all at once**, one `--grow:760ms`, CSS-only per DEF-003. **Concurrency
  already exists.** Exactly two deltas remain: **(a)** upper segments do not FLOAT — each grows from
  its own fixed anchor, so the stack gaps mid-animation instead of staying contiguous · **(b)** all
  share one `cubic-bezier(.22,.61,.36,1)`; there are no per-segment curves. Both are reachable in
  pure CSS (the cumulative height below each segment is static per chart ⇒ a per-rect custom property
  emitted at generation time), so **no JS enters physics** and B-D7 / DEF-003 hold.
  Edges: relates(DV-D14) — DV-D14 already moves segment geometry, so the animation must animate the
  ENACTED heights, not the true ones, or the two rulings will fight.

- **DV-D17 · The isolated key must NOT stay active once other series are checked back on.**
  Dave, verbatim: *"the legend behaviour, the isolated key item stays active when I check others on."*
  **Current behaviour, read from source (not inferred):** `canon/dv-legend.js:114` sets
  `solo = st.isolated === id` and `:119` toggles `.is-solo` from it; isolate mode keeps `st.isolated`
  pinned to the originally-isolated id while `st.focus` grows (`:129` — *"checking one ADDS it at
  full"*). So the first-isolated row keeps `.is-solo` — `border-color:var(--ink)` + a 6% ink fill
  (`canon.css:3506`) — even after the focus set is no longer a set of one. **That is the black-bordered
  "B Savings" in Dave's screenshot.** The marker claims *isolated* while three series are showing.
  **★ RULED — (a) RELEASE ISOLATION ENTIRELY.** The moment a second series is checked on,
  `st.isolated = null` and `st.focus = null`; the row returns to its resting treatment and the legend
  leaves isolate mode. **Accepted cost, stated at ruling time:** you cannot build a 2-of-5 comparison
  by isolating then adding — the second click ends isolation rather than growing a focus set. **The
  simplicity is the point**; a mode that persists invisibly is what produced the defect.
  **⚠ THREE THINGS THE ENACTMENT MUST NOT BREAK, and each is a bite:**
  **(i)** `dv-legend.js:129` currently leaves `visible[]` untouched during isolate specifically so
  release can restore it — **releasing on add must restore to `visible[]`, not to all-on**, or the
  ruling silently becomes a Reset. **(ii)** `:122` computes Reset's disabled state from
  `count(visible) === ids.length && !isolated` — with `isolated` now null, **Reset must not disable
  itself while the view is still filtered.** ⚠ This is the same expression ds-018 lives in; do not
  conflate the two fixes. **(iii)** the `dv-sr` live region (DV-D11 chrome clause) announces every state
  change — **"Isolation released" must fire on the add path too**, not only on the label re-click at
  `:140`, or screen-reader users get a silent mode change.

  **✅ ENACTED 2026-07-27 (session #7) — DOM-PROVEN, RENDER OWED.** `canon/dv-legend.js`
  `toggleSwatch()`: a blank swatch checked while isolated sets `st.isolated = null; st.focus = null`
  and leaves isolate mode; injected into all 5 registered consumers by `gen_component_partials.py`;
  build **60/60 GREEN exit 0**. **All three bites covered and each has its own failing control** —
  `_verify_dv_legend_members.js` **108/108** (checks 20–23) and `_verify_dv_legend.js` **27/27**
  (checks 12/13/20), with a `DVLEGEND` env override added to both so a neutered copy can be pointed
  at without ever mutating canon: full revert → 99/108 + 23/27 · release-to-all-on → 105/108 ·
  release-silently → 104/108 + 26/27. ⚠ **The donut suite CANNOT catch the all-on regression**
  (27/27 under that neutering) — its scenario starts all-visible, where `visible[]` and all-on are
  indistinguishable; only the members suite dims a spare **before** isolating. Do not treat the two
  suites as interchangeable proofs of bite (i).
  ~~⚠ **RENDER-VERIFY IN THE LICENSED CUT IS OWED, NOT DONE** (Dave's ruling: wrap and flush at ~55%).
  jsdom proves the state machine, not that `.is-solo` stops painting — and **ds-018 is a live
  counter-example on this same component.** Pair the two in one Green window: same page, same
  harness, same two widths, one spin-up.~~ **✅ DISCHARGED 2026-07-27 (session #10) — see below.**

  **✅✅ RENDER-PROVEN 2026-07-27 (session #10). DV-D17 IS NOW ENACTED · DOM-PROVEN · RENDER-PROVEN.**
  `knowledge/_render/verify_dv_d17_render.py`, licensed HSBC cut asserted in every frame before
  measuring, transitions killed **before the first gesture** (ds-019's lesson), **real pointer
  clicks** on the real gestures (LABEL = isolate · SWATCH = check on) — never `classList.add`.
  **Measured, identically, in six contexts** — snippet @1180/@760 · showroom **light** pane
  @1180/@760 · showroom **dark** pane @1180/@760 (genuinely dark: `--ink` `#FFFFFF`, `--line`
  `#808080`, so this is coverage, not the same pane counted twice):

  | state | `.is-solo` | `border-top-color` | `background-color` |
  |---|---|---|---|
  | baseline | false | `rgb(225,225,225)` = `--line` | `rgba(0, 0, 0, 0)` |
  | **isolated (POSITIVE CONTROL)** | **true** | **`rgb(26,26,26)` = `--ink`** ✓ | **`color(srgb 0.101961 0.101961 0.101961 / 0.06)` = 6% ink** ✓ |
  | **released (THE RULING)** | **false** | **`rgb(225,225,225)`** ✓ | **`rgba(0, 0, 0, 0)`** ✓ |

  **★ WHY THE OLD ACCEPTANCE TEST HAD TO BE REPLACED, AND THIS IS THE TRANSFERABLE PART.**
  As specified it was *"no `.dv-legrow` resolves the `.is-solo` treatment after isolate-then-check-on"* —
  **an assertion of an ABSENCE, and nothing else.** An absence is satisfied by a working fix, by a
  blind probe, by a mistyped selector, **and by a complete revert of the fix.** Session #8 ran it,
  printed `24 checks · 0 failures`, and was measuring nothing. **⇒ A one-sided proof of an absence is
  not a proof.** The replacement is two-sided in one gesture sequence: **step 1 proves the treatment
  CAN be seen** (isolate → it paints), **step 2 proves it stops** (check a second on → it does not).
  Step 1 is what makes step 2 mean anything.
  **BITE (`--bite`, on a NEUTERED COPY — canon never mutated, `git status` clean):** the 216-byte
  DV-D17 release branch deleted from a copy of the snippet ⇒ step 2 fails at **both** widths and
  **reproduces Dave's original screenshot exactly** — row 1 keeps `.is-solo`, `rgb(26,26,26)` border,
  6% ink fill, while three series show. Step 1 still passes under the neuter, which is the point:
  the probe is not blind, the behaviour is broken.
  **★ ONE CATCH THE PROBE MADE AGAINST ITSELF, banked because it is the live shape of a standing
  rule.** The first run went red: *"row 2 paints an ink border with no `.is-solo` class."* **The check
  was working. The cause was the instrument** — `canon.css` also carries `.dv-legrow:hover{border-color:
  var(--ink)}`, and a **real** pointer click leaves the cursor resting on the row it just clicked.
  Fix: park the pointer before reading, and carry an OBSERVED `hovered` field so a hovered row is
  **named and skipped**, never silently filtered. *(Exactly [[silent-lookup-failure-class]]'s ruling:
  a control that fires may be RIGHT — exhaust that before calling it broken. Here it was right about
  the pixels and wrong about the cause, and only an observed field could tell the two apart.)*
  ⚠ **ONE ENACTMENT CALL IS THE AGENT'S, NOT DAVE'S, AND IS UNRULED.** Release also sets
  `st.visible[id] = true`, so the clicked series is showing afterwards. The literal reading restores
  `visible[]` **alone** — both satisfy bite (i) (neither releases to all-on), and they differ only
  when a series dimmed *before* isolating is then the one clicked: the literal reading leaves it
  dimmed, so the click that ended the mode does nothing visible to what was clicked. **One line
  either way — Dave's to reverse.**
  ⚠ **CONSEQUENCE FOR DV-D13 THAT THE RULING DID NOT NAME — needs Dave's eye.** Under additive
  focus, isolating Housing (`950 / 41%`) then checking a second series **grew** the donut's centre
  readout to `1250 / 54%`. Under DV-D17 that click releases, so the selection becomes the whole
  visible set and the centre returns to `2320 / 100%`. **DV-D13 is intact — the centre still follows
  the SELECTION**; the selection is simply everything again. Recorded rather than absorbed, because
  the accepted-cost line named the lost 2-of-5 comparison and not this.
  **Arc + what the author flags against his own work:**
  `_DECISION-HISTORY/2026-07-27-the-suite-that-asserted-the-old-ruling.md`.

- **ds-018 · Reset's DISABLED state renders as the hover/active style.** Dave, verbatim: *"reset
  disabled style is set at the hover style."* Full record + the mechanism hypothesis in
  `knowledge/_DS-IMPROVEMENTS.md` § ds-018. Headline: disabled Reset shows an **ink border**, which is
  the hover treatment, where **B-D4 requires disabled to be visible-but-recessive** (#808080 class).

## STATUS — round-one kit PARKED, "good enough", NOT signed off (Dave 2026-07-16)

Dave's call: **move on now, but this is a REVISIT target — not DONE.** The round-one kit + its
interactions are accepted as good-enough to stop here; sign-off is deferred until a later pass. Mirrored
in `_LIVE-STATE.md` (🟡 PARKED entry) so the state machine doesn't read this as finished.

**Revisit backlog (when Dave returns):**
- More **controls**: filtering, **chart titles**, and other Layer-2 interaction controls.
- Finish the interactions that are only partially there; full sign-off after an **in-browser** pass
  (everything to date is gate + `node --check` verified only — never render-checked in a browser).
- Then flip the `_LIVE-STATE` entry from 🟡 PARKED to DONE.

## Open / pending

- **★ NEW 2026-07-28 (two-lane ruling, memento ledger § TWO LANES) — TABLE-IDIOM UNIFICATION
  (ex-M4a) + CHART-TABLE-TOGGLE ACCRETION (ex-M4b) queue HERE**, blocked until the memento lane
  lands. Survey receipt in that ledger row: scatter = behaviour-group registration + `data-tip`
  contract adoption + dv-legend's inert payload rides along (the per-member opt-in schema question,
  Dave's); sparkline = markup + CSS only (toggle JS already injected, dormant). Batch-2 #2 already
  rules the toolbar for every chart with a data table; DV-D02 checked — it protects no `<details>`.
- **★ NEW 2026-07-27 (Dave, session #6) — THREE FLAGS, CONTENTS NOW NAMED → see Batch 10 above.**
  **DV-D16** (stacked sequential animation) · **DV-D17** (isolate marker persistence) ·
  **ds-018** (Reset disabled renders as hover). All three are CAPTURED, **none enacted** — each carries
  a READ-BACK question that must be answered before any build. Nothing here has been render-verified.
- **Grouped column layout redesign** — awaiting Dave's reference images (Batch 1 #3).
- **DV-D02 responsive** — needs an in-browser resize check by Dave (built blind; safe fallback).
- **Two new Figma display types + 4px-grid type tokens** — land the real display scale, replace
  `--fs-display` placeholder (DV-D05).
