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
  text, only horizontal positions relayout to container width. Pure enhancement, safe fallback to the
  baked SVG.
  **IN SCOPE — cartesian plots, HORIZONTAL BAR INCLUDED:** vertical bar · **horizontal bar** · line ·
  combo · scatter. Marked by `class="dv-svg dv-fit"` on the plot `<svg>`; gated by
  `_validate_dataviz.py::dv_fit_scope` (DV-D02-A, 2026-07-28).
  **OUT OF SCOPE — and the reason travels with the exclusion.** Dave's standing terms: *"I lean to
  correctness, standardisation with flexibility rather than expediency"* — a gate that encodes a rule
  without its principled exceptions is not standardisation, it is a future false positive.
  - **Donut / pie graphic — EXCLUDED: compressing a circle distorts it.** ⚠️ Status is
    **DAVE-HEDGED, not firm** (2026-07-28), and must not be hardened by a later reader: *"the chart
    graphic will probably never have to scale, but I'm not 100% sure. there may be a case to start and
    stop scaling between break points. this also need to tested, this is finessing though, and should
    probably happen while or after we work on the 12 column grid and breakpoints."* **Deferred to the
    12-column-grid + breakpoints task by his instruction — do not fold it into gate work.**
  - **The donut's LOCKUP with its legend is a separate question, and is NOT excluded.** Dave, #27:
    *"donut (graphics) probably not but their lockup with the legend will."* Responsiveness applies at
    **different levels of a composition**; DV-D02 today speaks only about plots. The composition level
    needs a slot/props model the registry has no concept of — same seam as the legend-as-molecule
    proposal and the templates/shells zero tier. **ADR-shaped, deliberately not gated here.**
  - **Sparkline — VACUOUSLY out of scope, not excluded.** It carries no text, so the
    non-scaling-text constraint has nothing to bind; its fit rides a separate CSS release
    (`figure.dv-fit-on .spark-standalone`), receipted in its registry `$note`. Recorded so a later
    reader does not "fix" it by adding `dv-fit`.
  **⚠️ AMENDED 2026-07-28 (#28) — DV-D02-A: the horizontal-bar exclusion was ROT, and the code never
  agreed with it.** Original text kept verbatim per the Memento discipline, so the correction can never
  read as drift: *"Cartesian charts only; horizontal bar + donut excluded (compressing a value-axis /
  circle distorts)."* Dave, asked directly and answering firmly: *"horizontal bars is fine, this must
  have been a rot problem or miscommunication. This earlier example was responsive and I was happy with
  it apart from the text cropping."* **MEASURED — and this is why it is a correction, not a reversal:**
  `Chart-bar.reference.html:387`, the very h-bar he was looking at, has carried `class="dv-svg dv-fit"`
  all along. The implementation has always treated horizontal bar as responsive; only this ledger line
  said otherwise. The exclusion was never enacted and was never his.
  ⚠️ **The owed in-browser resize check is now PART-MET:** Dave has seen horizontal bar responsive and
  approved it, with text cropping noted as a separate defect (brief finding 1,
  `notes/_briefs/2026-07-28-chart-encoding-gaps-carry-forward.md`). Donut and scatter remain unchecked.
  ⚠️ **Open tail, do not assume it settled — chart text and the T-D15 mini ramp.** Dave: *"we had a
  mini text scale for charts, 12-14-16: however we never tested it."* T-D15 IS minted and live
  (`.t-cm-ctl-12/14/16`, chart labels already at 12/500 = step 1 de-facto) — **but it was minted for
  the segmented control and is a FIXED ramp a class picks one rung from, not a responsive step-down.**
  Chart text dropping 14→12 at narrow widths would be a NEW application of T-D15, not the untested
  half of an existing one. Needs its own test before anyone gates or builds it.
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
  Edges: refines(dv-004, scope=mechanism-neutral-separation) · supersedes(dv-004, claim=stroke-only)

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
> **★ DV-D16c · CAP STACKED SEGMENTS AT 6 for now** *(~~DV-D18~~ RENUMBERED #76-D2, Dave — the id
> collided with #70's SOLO IS A SET SIZE ruling. This one moved because it has ZERO code references,
> no dossier and no graph node, while canon, `_verify_dv_legend_members.js`, DV-D19's `refines` edge
> and #70's dossier all already MEAN the solo ruling when they say DV-D18. `16c` not `20`: this ruling
> lives inside the DV-D16 wave, two lines under DV-D16b, and the file already uses that suffix form —
> minting a forward number for an older ruling would make the record read as if it were later.)* — Dave: *"Lets cap at 6 for now."* Aligns stacks
> with `dv-pie-009`'s existing donut cap; remainder buckets to **"Other"**.
> **★★ FLOATED, Dave's, for a later window — THE "OTHER" BUCKET MUST BE EXPANDABLE.** Verbatim:
> *"all bucketed 'other' segments should be expandable, through some mechanism we'll explore later."*
> **Not designed, not scoped, deliberately.** ⚠ **This binds the cap:** DV-D16c is only acceptable
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
  **✅ ENACTED IN TWO PASSES, AND THE SECOND ONE FOUND THE REVERSAL STILL BEING GENERATED — added
  2026-08-25 (#219), by ADDITION; nothing above is amended.**
  **(1) #218 — Chart-bar's `stacked-column`:** both remaining deltas built CSS-only (per-rect
  `--b1…--b(i−1)` + `--self`, three registered `@property` progress numbers on one shared
  `var(--grow-dur)` timeline, the float riding the CUMULATIVE ANIMATED height below). `s218-D5` then
  moved the two curved positions onto the house tokens `--grow-ease-in`/`--grow-ease-out` and delayed
  the on-segment keys by one full growth.
  **(2) #219 — the pro-forma's `stacked` figure, AT CAUSE in `_review/_gen_dataviz_charts.py`.**
  ⚠ **The generator was still emitting WORDING ①** — `animation-delay:seq*420ms` +
  `animation-duration:400ms` + the literal `ease-in`/`linear`/`ease-out` keywords, under a comment
  reading *"each waits for the one below"* — **eighteen sessions after the reversal**. Retired;
  wording ② + `s218-D5` enacted for a 4-deep stack (seg1 ease-in · seg2 linear · seg3 linear ·
  seg4 ease-out, the positional rule). Chart-bar's own inert 45ms/rect residue was stripped at the
  same time, which is the `#218` receipt's owed generator item discharged.
  ⚠ **The one-word correction the `#218` receipt filed against the SCOPE MEASURED paragraph above is
  now MOOT** — the stagger it named is gone from both surfaces. The paragraph is left untouched
  ([[header-wins-over-audit]]); this note is the correction's receipt.
  **The gate that keeps it gone:** `knowledge/_render/verify_dv_d16_render.py` is now **profiled over
  every stacked surface** (`--target snippet|proforma|all`) and carries a `WORDING-1` check —
  a stacked rect that declares its own `animation-delay` / `-duration` / `-timing-function` is RED by
  name, with a `wording-1` mutation arm on each profile. Both surfaces static + render GREEN at #219.
  ⬛ **STILL DAVE'S, and the reason DV-D16b is not finished:** `Chart-stacked-area` — the third and
  last stacked surface — animates by FADE, and converting it is a motion call, not a mechanical
  extension. Receipt: `notes/_subreports/2026-08-25-219-lane4-dv16.md` (row `W-175`).

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

- **★ DV-J1 — TABLE-IDIOM UNIFICATION · ★ DV-J2 — CHART-TABLE-TOGGLE ACCRETION** *(J = Job,
  sitting beside the DV-D decision series; keys minted 2026-07-28 #26 on Dave's word — "M stood
  for Memento… this is Apollo dataviz work, we need to fix this coding". The #20 two-lane ruling
  deliberately left re-keying to the job that picked them up; #26 is that job. Forward-looking
  surfaces carry DV-J1/DV-J2; historical rows keep ex-M4a/ex-M4b verbatim.)* Queue HERE; unblocked
  #25 (memento lane landed). Survey receipt (#20 ledger row): scatter = behaviour-group
  registration + `data-tip` contract adoption; sparkline = markup + CSS only (toggle JS already
  injected, dormant). Batch-2 #2 already rules the toolbar for every chart with a data table;
  DV-D02 checked — it protects no `<details>`.
  **★ 2026-07-28 #26 — the inert-payload half is RULED + MACHINERY LANDED:** the per-member
  opt-in schema question → **ADR-0015 § Amendment 2** (Dave, TENTATIVE: universal-default
  consumes-manifest, individual opt-out, fail-loud both ways; his read-back "universal automatic
  opt-in with the option to opt-out individually"). Machinery in `gen_component_partials.py`
  (7 bites + mutation-proven), zero declarations yet ⇒ zero behaviour change. **DV-J2's enactment
  = the first narrow declaration** (scatter joins `consumes:["dv-behaviour"]` + 28 `<title>`→
  `data-tip`; sparkline may shed its inert 16,330 B when ruled). **Drift corrected, measured:**
  scatter was NEVER a group member (`$members` + 0 markers) — the dv-legend `$description` aside
  claiming so was prose drift; the #20 receipt was right.
  **★★ 2026-07-28 #27 — DV-J2 SCATTER HALF ENACTED + RENDER-PROVEN. The manifest's first NARROW
  declaration is live.** `component-types.json` → `Chart-scatter` joins `$members` with
  `"consumes": ["dv-behaviour"]` + an extraContract naming only the table hooks it carries
  (`dv-tbl-toggle` · `dv-tablepanel`) — no legend hooks, because it does not consume dv-legend.
  **MEASURED RESULT: 13,251 B injected, dv-legend's 16,271 B refused entry** (no legend marker pair
  in the file) — the saving ADR-0015-A2 was built for, on its first live instance. Build `[72/72]`
  exit 0; `--check` clean.
  **The narrow path bites FOUR ways on a live instance** (mutation control, green at both ends —
  the ADR's seven bites were unit-only until now): (1) unknown name REFUSES · (2) empty list
  REFUSES · (3) **the declaration REMOVED refuses** — universal membership then demands the
  dv-legend markers scatter deliberately does not carry, so the declaration cannot be silently
  dropped; the file itself goes non-conforming *(this one refused where the author predicted it
  would pass — the reason is better than the prediction and is recorded as observed, not inferred)*
  · (4) declared-away markers present REFUSES.
  **⚠ THE QUEUE'S "28 `<title>`→`data-tip`" WAS TWO THINGS WRONG, both measured:** (a) 27 marks,
  not 28 — the 28th `<title>` is the document title in `<head>`; (b) it is **not a rename**. Canon
  (Chart-bar 52 tips, Chart-line 62) is a four-part contract — `tabindex="0" role="img"
  aria-label="…" data-tip="…"` on the element, **no `<title>` child** — and the svg is
  `role="group"`, not `role="img"`. Scatter shipped `role="img"` with `<title>` children: marks
  were **not in the a11y tree as separate nodes at all** and the tip was mouse-only, because
  `dv-behaviour.js:71` raises the popover on hover **AND keyboard focus** of `[data-tip]`. A literal
  rename would have dropped the accessible name and shipped a half-dead tooltip, and **nothing
  gates it** — `_validate_dataviz.py` has no aria-label/role check on marks. Enacted as the full
  contract: 27 marks now keyboard-reachable and individually announced.
  **Scope, Dave's word (session #27, plain-language option-select):** *interaction only* — tooltips
  + the show-the-table button. **DV-D07 axis/grid catch-up was FENCED and is logged as ds-020**;
  the CSV button (`button.dv-csv`, available in the consumed behaviour) was NOT adopted — out of
  the ruled scope, flagged not taken. ~~FIT (`svg.dv-fit`) not adopted either: scatter is deliberately
  fixed-geometry per DV-D02 static.~~
  **✗ THAT CLAIM WAS FALSE — CORRECTED SAME DAY (2026-07-28, Dave caught it by eye). Both beats kept
  per the Memento discipline.** DV-D02 reads *"Cartesian charts only; horizontal bar + donut
  excluded"* — **scatter is cartesian, so DV-D02 covers it and scatter does not comply.** The
  "deliberate" came from a CSS comment in the snippet (`/* DV-D02 static: fixed geometry, scroll */`)
  which describes the **safe fallback**, not an exemption: the agent inferred a ruling from prose
  instead of retrieving it — the [[trust-the-spine-not-the-prose]] violation, committed in the same
  session that correctly caught the queue doing the equivalent. **Scatter is MISSING `dv-fit` and
  that is a defect, not a decision** (measured: bar 5 · combo 1 · line 2 · donut 0 correctly ·
  scatter 0 wrongly). ~~⚠ And DV-D02's exclusion list is itself now in question — Dave, hedged and
  **not yet firm**: *"I think horizontal bars are fine to be fully responsive, donut (graphics)
  probably not but their lockup with the legend will."* Do not gate DV-D02 as written; amend first.~~
  **✅ RESOLVED 2026-07-28 #28 — DV-D02 AMENDED (DV-D02-A, see § Standing decisions).** Dave firmed the
  h-bar half — *"horizontal bars is fine, this must have been a rot problem or miscommunication"* — and
  the amendment is evidence-backed: `Chart-bar.reference.html:387` already carried `dv-fit`, so the
  implementation never agreed with the exclusion. The donut half stays **hedged and DEFERRED** to the
  12-column-grid + breakpoints task by his instruction, and the lockup half is ADR-shaped, not gate-shaped.
  Carry-forward brief: `notes/_briefs/2026-07-28-chart-encoding-gaps-carry-forward.md`.
  **✅ §C·2 ITEM 20 RULED 2026-07-28 #27 — "NARROWLY DISCHARGED" (Dave, his phrase, one word after a
  three-option read-back).** The 07-24 deferral *"Chart-scatter Layer-2 — deferred, stays Layer-1
  safe"* is discharged **for the tips + table spine only**; **DV-D11 legend interaction and
  brush/range-select (item 21) stay DEFERRED.** WHY the narrow form, and it is the point: scatter
  still ships a static `<ul class="dv-legend">` — finding 4 of Dave's same-day review — so it is
  *partly* Layer-2, not Layer-2. A flat "discharged" would have put an overstatement in the record as
  the next reader's starting fact. The agent did NOT edit this line when the work landed: it is
  Dave's batch item, and closing one's own open question by having done adjacent work is the
  derivation-governance failure this project gates against — the enactment stood on his SCOPE ruling
  while the batch line waited for his word on the line itself. Restored set 17–22 → 4 open of 6.
  Render-proof: `knowledge/_render/verify_dv_j2_render.py` (2 widths · licensed cut asserted ·
  toolbar 32px + 44px hit · toggle drives the panel · **keyboard focus raises the tip** · shadow
  compared AS A COLOUR → `rgba(0,0,0,0.2)`); `--bite` strips one `data-tip` and the proof FAILS as
  it must. Ledger row + enactment: 2026-07-28 #27.
- **★ NEW 2026-07-27 (Dave, session #6) — THREE FLAGS, CONTENTS NOW NAMED → see Batch 10 above.**
  **DV-D16** (stacked sequential animation) · **DV-D17** (isolate marker persistence) ·
  **ds-018** (Reset disabled renders as hover). All three are CAPTURED, **none enacted** — each carries
  a READ-BACK question that must be answered before any build. Nothing here has been render-verified.
- **★ CHART TEXT — CLIP + COLLISION · INSTRUMENTED 2026-07-28 (#29), REMEDY UNRULED.** Brief finding 1
  (`notes/_briefs/2026-07-28-chart-encoding-gaps-carry-forward.md`) is now measured by a render-proof,
  `knowledge/_render/verify_chart_text_render.py` — the ds-005 gate matches on CSS `text-box-edge` and
  structurally cannot see SVG `<text>`, so this belongs to the render-proof family, not a `_validate_*.py`.
  **Asserts, on ink not em box:** (A) every `<text>`'s ink sits inside the viewBox · (B) no two ink boxes
  intersect. **MEASURED on Chart-scatter, both widths, licensed cut:** `'Savings (£000)'` **1.38 units**
  above the ceiling · `'75'` × `'Savings (£000)'` overlap **13.96 × 3.50**.
  **⛔ RULED (Dave, #29): ink tolerance = 0.5 user units**, shown before it stood — the ceiling line cuts
  the caps of "Savings", the floor line only kisses "Monthly income"'s descenders (~0.5), so the latter
  PASSES and must not be "fixed".
  ⚠ **`getBBox()` IS THE EM BOX, NOT THE INK** — it over-reports this label by **4.62 units** (6.00 vs
  1.38). A containment check written on it fires 4.6 units early and fails compliant charts on run 1.
  Do not "simplify" this proof back onto `getBBox()` vertically.
  **OPEN:** the geometry itself. `--control` specifies `x=2→46` + `y=9→11` and goes GREEN, but the
  numbers are **Dave's to rule** (derivation governance). **Corpus-wide debt UNMEASURED** — the `--all`
  sweep's 78 findings are UNTRUSTED pending two named instrument fixes (ancestor transforms · ancestor
  visibility). Arc: `_DECISION-HISTORY/2026-07-28-chart-text-clip-collision-render-proof.md`.
- **Grouped column layout redesign** — awaiting Dave's reference images (Batch 1 #3).
- **DV-D02 responsive** — needs an in-browser resize check by Dave (built blind; safe fallback).
- **Two new Figma display types + 4px-grid type tokens** — land the real display scale, replace
  `--fs-display` placeholder (DV-D05).

## ★ #69 — ds-020 enact + lockup rulings (2026-08-01, Dave via review screenshots — export defect noted)

- **DV ds-020 ENACT — APPROVED (D1):** scatter axis/grid on DV-D07 two-channel roles, control-first
  (pre/post both modes, colours diffed as colours). `_DS-IMPROVEMENTS.md` ds-020 status block has the
  full receipt. DV-D02-A waiver PART-DISCHARGED — stays for the `data-fx` fit half (6 vs bar 175).
- **Header layout — APPROVED (D2):** `.dv-head` space-between = canon; scatter's flex-end was drift.
- **Legend lockup layout — NEEDS REWORK (D3):** the recovered 2026-07-25 ruling ("keys ranged LEFT /
  Reset right-inline", legend v5 review-edits brief line 12 — captured then never enacted) was enacted
  on scatter with a 520px wrap-centre placeholder; Dave rejected the built shape. Detail owed at the
  #70 opener before rework. The 25-07 ruling itself STANDS — it is the enactment that missed.
- **Swatch-during-isolate — UNRESOLVED COLLISION (D4):** Dave's #69 wording ("additive like a
  checkbox") vs ★ DV-D17 (swatch ENDS isolate). DISCUSS LIVE next session; **DV-D17 stands until
  ruled otherwise.** Do not change behaviour on the wording alone.
- **Queue AGREED (D5):** fit-hook adoption + four-theme cascade wiring for chart canvases, incl.
  **Mono/Console/Legacy/Supercharge switcher in review-doc controls** (asked twice #69).
- **Titles (from #68's placeholder row):** cd2 "Housing dominates the month's spend" (enacted via
  `data-lockup-title`); cs1 + cs2 placeholders RATIFIED as Dave's copy. ds-026 (insight slot) FLOATED.
- ⛔ **Review-overlay export DEFECT recurred from #66** — Dave ruled by screenshots; row + diagnosis
  owed in `_REVIEW-SIGNOFF.md`.
- **★ POST-WRAP ADDENDUM (#69, Dave in chat):** the REFERENCE for D3 + D4 is
  `reviews/LEGEND-ISOLATE-TOGGLE-PROTOTYPE-2026-07-24-v5.5.html` — Dave: *"has all the correct
  behaviours for the legend interaction and how the charts should behave."* #70 surveys it FIRST and
  diffs scatter against it. ⚠ The prototype is dated 07-24, three days BEFORE DV-D17 (07-27) — if its
  swatch-during-isolate is additive, D4 is a deliberate REVISIT of DV-D17 with the prototype as
  evidence, not a memory slip. Verify which way it behaves before assuming.

---

## ★ #70 — 2026-08-01 — DV-D18: SOLO IS A SET SIZE, NOT A SEED IDENTITY

Node: DV-D18

*Opus 5 solo Cowork conductor + 2× Sonnet subs, Dave live. Dossier (arc, dead-ends, method):
`_DECISION-HISTORY/2026-08-01-the-70-dv-d18-and-the-unwired-radios.md`.*

- **★ DV-D18 · RULED (Dave, 2026-08-01) — the additive focus set RETURNS; the stale marker is
  killed by SET SIZE instead.** `isSolo(st, id)` now requires the focus set to be a **singleton
  containing this id**; `toggleSwatch` runs ONE additive path for both modes (while isolated,
  `m` IS `st.focus`). **DV-D17's release-on-add branch is DELETED, not commented** — left in place
  it pre-empts the additive path on the very first click.
  **What DV-D18 supersedes:** DV-D17's *mechanism* (tearing the mode down on the second check-on).
  **What survives UNCHANGED:** DV-D17's *invariant* — Dave's verbatim *"the isolated key item stays
  active when I check others on"* — and its **bite (i)**, release restores `visible[]`, never all-on.
  Release is now the label re-click or Reset. Enacted `knowledge/canon/dv-legend.js`; injected into
  all five chart snippets by `gen_component_partials.py` (`--check` OK).

- **WHY DV-D17 OVERREACHED — the two behaviours were separable and it conflated them.** The additive
  focus set (DV-D11, Dave's own 2026-07-26 ruling) and the stale solo marker were independent;
  DV-D17 fixed the marker BY DELETING the additive model. It did not have to.

- **⚠ THE #69 REFERENCE COULD NOT BE ADOPTED WHOLE.** `reviews/LEGEND-ISOLATE-TOGGLE-PROTOTYPE-2026-07-24-v5.5.html`
  — Dave: *"has all the correct behaviours"* — carries `function isSolo(id){ return isolated === id; }`,
  i.e. **the exact defect DV-D17 was raised to kill.** DV-D18 takes its additive half and refuses its
  marker half. ⛔ **RECORD CORRECTED: the prototype is dated 2026-07-26 (mtime 19:10; its own `<title>`
  says so), ONE day before DV-D17, not three** — 07-24 is the series start. The #69 addendum and
  `_CHAIN.md` both carried the wrong figure; the error framed a current ruled state as a stale artefact.

- **★ D4 WAS NOT NEW — it was the #7 open item, 63 sessions later.** `_REVIEW-SIGNOFF.md:21`:
  *"★ NEW 2026-07-27 (#7) — TWO FELT CONSEQUENCES OF DV-D17, NEITHER RULED, BOTH NEED DAVE'S EYE
  LIVE."* Consequence (b) — the DV-D13 centre figure returning to 100% instead of growing — is
  answered by DV-D18. **A question parked for Dave's eye does not age out; it waits.**

- **⚠ a11y GATE BLINDSPOT, 43 sessions live.** `isolate()` announced *"check a blank swatch to add a
  series"* the whole time `toggleSwatch()` released instead. Gates asserted the BEHAVIOUR; nothing
  asserted the ANNOUNCEMENT told the truth about it. True again under DV-D18.

- **★★ METHOD — AN INVARIANT THAT SURVIVES A REVERSAL CANNOT DISCRIMINATE THE REVERSAL.**
  Mutation B (DV-D17's branch re-inserted, new `isSolo` kept) reported `restGhosted=[false]
  solo=false`: the `!soloRow()` clause — the very invariant DV-D17 existed to protect — **passes
  under BOTH rulings.** Check 20 only became capable of failing once it asserted what CHANGED
  (series outside the focus set STAY GHOSTED after the add). Sharper corollary of *"a green that
  can't fail is an assertion"*: when you rewrite a check across a reversal, **assert the delta, not
  the invariant** — the invariant is exactly the part that cannot tell the two apart.
  **Evidence:** 108/108 green · mutant A (seed identity) 4 red, `solo=true` · mutant B 97/108,
  checks 20/21/22 red. Both mutants via the suite's own `DVLEGEND` override — canon never mutated.

- **⛔ REVIEW-EXPORT DEFECT — ROOT-CAUSED AND FIXED. The radios were NEVER WIRED, in ANY review doc.**
  Not a #66 regression: `_review-overlay.html`'s `buildPrompt()` built from `comments[]` only, zero
  radio reads anywhere. #66's fix repaired comment-pin export under a `_RUNBOOK-review-doc.md`
  sentence claiming to make *"picks + comment pins capturable"* — **two problems conflated under one
  sentence, so the #69 recurrence was inevitable, not unlucky.** A working `picks{}` pattern had
  existed since 2026-07-30 in `reviews/MEMENTO-DECISION-PACK-2026-07-30-v1.html`, never reused.
  **Fixed:** `scanPicks()` reads every non-overlay radio group into the export, and **reports unruled
  groups explicitly as "(not ruled)" rather than omitting them** — a silent gap is how a decision goes
  missing; a declared one cannot. `isDecisionControl()` exempts native choice controls from the
  review-mode capture-phase `preventDefault()` that was swallowing the click AND popping a composer.
  ⚠ **UNPROVEN: Dave has not yet used it.** The fix is DOM-reasoned, not user-proven — #71's review
  doc is its first real test, and that is deliberate.

- **✅ PROBE THAT INVALIDATED ITS OWN WORRY (recorded because it did):** the snippet↔canon seam is
  **gated** — `gen_component_partials.py --check` at `_build_all.py:91` blocks on drift. A stale
  snippet would have gone red at the next push, not shipped silently.

- **⬛ STILL OPEN:** D3 lockup rework — **Dave's detail was owed at this opener and was not given**;
  carry it to #71. Review pair for DV-D18 **deferred by Dave's explicit budget ruling** (~140K of a
  200K line; a review build landed ~205K — declared and forked, not spent silently).

## ★ #75 — 2026-08-01 — DV-D19: ISOLATION AND CHECK ARE MODES, NOT A DERIVED MARKER

*Opus 5 solo Cowork conductor, Dave live. Session ran the edge-type ruling first (ADR-0012
§ Amendment #75), then returned to the legend on Dave's direction.*

- **★ DV-D19 · RULED (Dave, 2026-08-01, #75) — TWO MODES, MUTUALLY EXCLUSIVE, AND THE GESTURE
  DECIDES WHICH.** Verbatim: *"There are two modes isolation and check, as soon as the user checks
  a swatch the whole set change to check mode. check-mode and isolation-mode never occur at the
  same time."* And on the split: *"the legend items are simply spit in two, clicking on the label
  is isolation-mode and clicking on the swatch is check-mode."*
  - **Isolation mode** — filled swatch on the isolated series, empty on the rest; the isolated ROW
    carries the emphasis container (`.is-solo` → `border-color:var(--ink)` + `ink 6%` tint).
  - **Check mode** — filled swatch = checked, empty = unchecked; **no row carries emphasis at all.**
  - **The emphasis container is the SIGNATURE of isolation mode.** Entering check mode removes it
    for good — not merely while the set is larger than one.
  - **Nothing jumps on the transition** (Dave, #75): the focus set becomes the checked set. Reverting
    to the pre-isolation mix was put to him and refused — a check gesture must not yank back series
    the user deliberately dropped.

- **⛔ WHAT IS ACTUALLY BROKEN — the RETURN path, not the two states.** Both of Dave's reference
  images are what canon renders TODAY: isolate C → C emphasised, A/B empty (image 1); isolate D +
  check E → two filled swatches, no emphasis (image 2). Traced at source: `isSolo(st, id)` is
  **re-derived every render** as `st.isolated && st.focus[id] && count(st, st.focus) === 1`. So
  `isolate D → check E → uncheck E` returns the focus set to a singleton and **the emphasis on D
  comes back**, while the user is plainly in check mode. That is the "both modes at once" Dave saw.
  ★ **The predicate can become true again; a mode cannot.**

- **DV-D19 REFINES DV-D18, IT DOES NOT REVERSE IT.** DV-D18 (#70) was right to stop keying the
  marker off the SEED identity — it replaced seed identity with a set-size predicate, and a
  predicate is re-entrant. DV-D19 replaces the predicate with **sticky mode state**: entered by a
  label click, exited by any swatch check, never recomputed from set size. DV-D17's bite (i)
  (`visible[]` untouched, release restores the prior mix) survives untouched.

- **⚠ UNPROVEN, DECLARED — the fade request is NOT yet attributed.** Dave: *"I'd like the fade
  behavior on this chart"* + `reviews/LEGEND-ISOLATE-TOGGLE-PROTOTYPE-2026-07-24-v5.5.html`.
  **Static comparison found NO delta:** v5.5 and canon both define `.is-faded .24 / .is-ghost .12 /
  .is-peek .24`, and **both select by bare `[data-series-group="…"]`** (`dv-legend.js:40`,
  v5.5:529) — so the on-chart key letters (`text.dv-barkey`) ghost with their bars in BOTH. My
  first hypothesis (canon fades bars but not key letters) is **DEAD**. What this leaves: a
  RENDER-level comparison (~4 sandbox calls, `_RUNBOOK-render-verify.md`, `goto("file://…")`),
  or Dave meaning *preserve* this fade through the mode change rather than *add* it. **Not
  guessed, not built.** → §C, first item for #76.
  - ✅ **CLOSED #78 (2026-08-02, Dave, post-wrap; the *preserve* reading was right).** The v2
    specimen (`reviews/DV-D19-MODE-LATCH-2026-08-02-v2.html`) demonstrated the shipped ladder
    LIVE (computed opacities 1 / .24 / .12 read back on hover) and put the question straight,
    options deliberately not invented. Dave, watching it run: *"the fade levels are good btw"*;
    read back as "the live ladder (full / 24% hover / 12% ghost)" and confirmed verbatim:
    *"— is correct."* ⇒ **The ruling: the shipped fade ladder IS the intended behaviour —
    nothing missing, nothing to add or build; the #75 ask meant PRESERVE it through the DV-D19
    mode change, which canon already does.** No code change; the closure is the record.
    Ledger sibling: `notes/_MEMENTO-DECISIONS.md` § ★ #78 (post-wrap addendum).

- **⚠ RECORD DEFECT, FOUND NOT FIXED — `DV-D18` IS USED TWICE.** `_DATAVIZ-DECISIONS.md:422`
  *"CAP STACKED SEGMENTS AT 6"* and `:728` *"SOLO IS A SET SIZE"* are different rulings under one
  ID. Renumbering a ruling of Dave's is not an agent's move. ⬛ **His call at the #76 opener.**

- **CEILING, MEASURED not recalled:** `canon/dv-legend.js` = **17,035 B vs the 16,384 B ADR-0015
  per-source cap — 651 B OVER, `_validate_behaviour.py` RED.** The record said "54 B free"; that
  was true at `229cb14` (07-27, 16,330 B) and died at `2aa778f` (08-01, the DV-D18 enact wave).
  Group page budget is fine: 29,083 B of 32,768. **Recommended and put to Dave: SPLIT along the
  DV-D12 seam** — `sweepDonut` + `arcPath` + `pt` are ~4.1 KB and reference **zero** of the
  interaction model (`rec`/`render`/`highlight`/`toggleSwatch`/`isolate`/`centreData`/
  `updateCentre`/`hostOf`/`hiTarget` — all 0 hits; only INIT couples them). Lands dv-legend at
  ~12.9 KB. Group total unchanged, so the split buys **no** headroom — which is exactly what
  ADR-0015's amendment demands. ⬛ **Dave has not ruled it yet; nothing split.**

- **⚠ THE NEW GATE BIT ON THIS VERY ENTRY, AND IT IS TELLING THE TRUTH — DECLARED, NOT SILENCED.**
  `DV-D19 —refines→ DV-D18` raises `orphan-target`: **DV-D18 has no own-id home anywhere.** Its two
  appearances are a blockquoted bullet inside #69's batch (`:422`) and a SESSION heading that merely
  mentions it (`:728`, `## ★ #70 — … — DV-D18: …`), and #75's registration rule takes an id only when
  it OPENS its own heading — correctly, or a passing mention would mint a node. ★ **Deleting the edge
  to buy a green is the exact unearned-green pattern this session spent its morning removing.** The
  edge stays, the warn stays visible, and the cause is the ID collision above. **Clears when Dave
  rules the collision and DV-D18 gets a `Node:` line in its real home.**

Node: DV-D19
Edges: refines(DV-D18, claim=solo-derived-from-set-size) · relates(DV-D11) · relates(ADR-0015, scope=dv-legend-over-cap)

---

## ★ #76 — 2026-08-02 — THE DV-D12 SPLIT, THE DV-D18 COLLISION, AND A MOTION LAW WITH ONE HALF BUILT

*Opus 5 solo Cowork conductor, Dave live. Both rulings his, taken at the opener from measured options.*

Node: DV-D20
Edges: relates(DV-D12, scope=source-split) · relates(ADR-0015, scope=page-budget) · relates(DV-D16c)

- **★ #76-D1 RULED (Dave) — SPLIT `dv-legend.js` ALONG THE DV-D12 SEAM, AND SHIP THE SWEEP TO THE DONUT
  ALONE.** `canon/dv-legend.js` measured **17,035 B against ADR-0015's 16,384 B per-source cap** and
  `_validate_behaviour.py` was RED at build step 97. `sweepDonut` + `arcPath` + `pt` moved verbatim
  (4,247 B) into **`canon/dv-donut-sweep.js`**, the group's THIRD registered behaviour source.
  **Result, measured on the artefacts:** dv-legend **13,007 B** (3,377 B under cap) · dv-donut-sweep
  **5,857 B** · page budget **30,912 of 32,768 B across 3 sources**, all gates green.
- **WHY THIS SEAM:** the three functions hold **zero** references to the legend interaction model —
  all nine of `rec`/`render`/`highlight`/`toggleSwatch`/`isolate`/`centreData`/`updateCentre`/
  `hostOf`/`hiTarget` measured at 0 hits. The cut follows a boundary that already existed rather
  than one invented to make the numbers work.
- **WHY DONUT-ONLY, and it is a contract argument not a tidiness one.** The sweep selects
  `path.dv-series[data-a1]`, which only a donut carries, so bar/line/combo/scatter were shipping it
  as dead payload. Narrow scope is what lets `requires.declarations` be **honest** here —
  `data-a1="` is a hook its one member really carries. The wider all-five scope would have forced an
  **EMPTY** contract, repeating the `class="dv-legrow` promotion failure already recorded in the
  dv-legend registry entry, where a hook required of every member was one two members could never
  satisfy. **Measured after regeneration:** `sweepDonut` present in Chart-donut, **0** in the other five.
- **⛔ THE GATE READ GREEN ON THE BROKEN STATE, AND THAT GREEN WAS THE DEFECT.** In the window between
  writing the file and registering it, `_validate_behaviour.py` reported **PASS — 25,055 B across 2
  sources**, down from 29,083. Content had left the gate's view: **the exact "splitting buys headroom"
  failure the 2026-07-26 page budget exists to prevent, passing silently.** Reproduced on demand as
  MUTATION A (un-register → 30,912 → 25,055; re-register → restored), so the delta is attributed.
- **⚠ AND THE HOLE IT EXPOSES IS NOT CLOSED: nothing gates the PRESENCE of a registration.** The page
  budget can only sum what is registered, so an unregistered `canon/*.js` is invisible to it and the
  gate stays GREEN — un-registering did not turn it red, it just quietly shrank the total. A
  `canon/*.js` with no entry in `component-types.json` should be a loud named finding.
  **⬛ UNBUILT, Dave's — proposed, not enacted.** *(gate-the-presence-not-the-drift.)*
- **★ MUTATION-PROVEN, both arms, by re-enacting the old behaviour:** (A) un-register the source and
  the page budget silently drops 5,857 B — the false green, on demand · (B) rename `data-a1="` in
  Chart-donut and `gen_component_partials.py --check` fails **loud and named**
  (`X Chart-donut: required declaration 'data-a1=" missing`). Contract is real, not decorative.
  Gates after: behaviour 3/3 sources · partials `--check` contracts hold · dataviz 7 surfaces ·
  `_verify_dv_legend_members.js` **108/108**.
- **★ #76-D2 RULED (Dave) — THE DV-D18 COLLISION IS DISCHARGED BY MOVING THE CAP RULING.**
  `DV-D18` named two rulings: `:422` *cap stacked segments at 6* and `:728` *solo is a set size*.
  **The cap ruling moved and is now `DV-D16c`**; `DV-D18` is the solo ruling alone. Basis, measured:
  all **9** code references (2 in `canon/dv-legend.js`, 7 in `_verify_dv_legend_members.js`) mean the
  solo ruling, as do DV-D19's `refines` edge and #70's dossier; the cap ruling had **zero** code
  references, no dossier and no graph node. **`16c` not `20`** — it lives inside the DV-D16 wave two
  lines under DV-D16b and the file already uses that suffix form; a forward number would make an
  older ruling read as a later one. ⬛ **The form is reversible on one word from Dave.**
- **✅ #75's `orphan-target` CLOSED BY ADDITION, not by deleting the edge.** The #70 section carried no
  `Node:` line — live convention since #27, load-bearing since #75 — so `DV-D19 —refines→ DV-D18`
  resolved to nothing. `Node: DV-D18` added to its real home. **The edge was never a candidate for
  deletion; buying a green that way is the pattern #75 spent its morning removing.**

### ✅ DV-D19 ENACTED AND RATIFIED BY DAVE THE SAME SESSION

**Dave, #76, on the live prototype:** *"DV-D19 is correct, but obviously it isn't styled correctly
as this is a prototype."* ⇒ **the BEHAVIOUR is signed off; the review ARTEFACT is not.** Recorded as
two facts because they have different owners: the ruling is closed, the specimen is defective.

- **Enactment:** `st.mode` (`'rest'|'isolate'|'check'`) is LATCHED by the first swatch click and
  cannot un-latch. `isSolo()` is now a mode read, not a set-size derivation. `active()` reads the
  focus set in BOTH focus modes, so moving isolate → check moves no mark — *nothing jumps.*
- **★ THE SUITE COULD NOT DISCRIMINATE THE RULING.** 108/108 passed under DV-D18 *and* DV-D19.
  An invariant cannot discriminate a reversal, so check **24** asserts the DELTA directly:
  `isolate → check → UNcheck` must leave no row solo. **Mutation-proven** by re-enacting DV-D18's
  predicate — check 24 fails on all four members and **nothing else moves** (112/116,
  `afterIsolate=true afterCheck=false afterUncheck=true`). Restored 116/116.
- **⚠ A REGRESSION I INTRODUCED, REFUSED BY THE VERIFIER, kept because the near-miss is the useful
  part:** gating the RELEASE test on `mode === 'isolate'` meant that after `isolate a → check b`, a
  re-click on `a` fell to the ELSE branch and RE-ISOLATED instead of releasing — destroying DV-D17
  bite (i). Check 22 caught it on all four members. **The release test is seed-based and stays so.**
  DV-D19 reverses neither DV-D18 nor DV-D17.
- **⛔ THE REVIEW ARTEFACT IS DEFECTIVE AND IT IS MY DEFECT, NOT A PROTOTYPE'S LICENCE.**
  `reviews/DV-D19-MODE-LATCH-PROTOTYPE-2026-08-02-v1.html` **invented** an `.is-solo` treatment
  (grey fill + inset ring, 15px swatch) instead of using canon's — which is
  `border-color:var(--ink)` + `color-mix(in srgb, var(--ink) 6%, transparent)`, a 12px swatch and a
  44px hit target (`canon.css:3504–3518`). ★ **A specimen that re-invents the styling cannot be
  ruled on**, and Dave caught it on sight. **The repair is NOT a restyle of my approximation — it is
  a rebuild against the real `canon.css` and the real snippet markup, so what he judges is the
  product.** ⬛ **OWED AT #77.**
- **⬛ ONE THING DV-D19 DOES NOT SETTLE, put to Dave in the prototype and not yet answered:** at
  rest a swatch click still toggles `visible[]` and the mode stays `'rest'`. His wording — *"as soon
  as the user checks a swatch the whole set change to check mode"* — could also mean a swatch click
  **at rest** enters check mode with a focus set. **The narrow reading was taken deliberately**: the
  return path is what he reported, and widening it changes resting behaviour on every chart. His.
  - ✅ **CLOSED #79 (2026-08-02, Dave, at the opener; the NARROW reading is RULED).** Put to him on
    the v2 specimen (`reviews/DV-D19-MODE-LATCH-2026-08-02-v2.REVIEW.html` § Open decision 1), both
    options stated in the doc's own words, neither pre-selected, the shipped one badged. **Read back
    as SENSATION, not mechanism** — *"on a chart you haven't touched, clicking a swatch just dims
    that series; nothing latches. The set only goes into check mode if you started by isolating
    something with a label click"* — and ratified in his own words, unprompted by any option label:
    ***"DV-D19 — the mode latch, shown on real canon prototype is perfect as it is."*** ⇒ **The
    ruling: at rest a swatch click toggles `visible[]` and the mode stays `'rest'`; check mode only
    ever begins from isolation. Shipped behaviour stands — no code change, `dv-legend.js:166` is
    correct as written.** DV-D19 is now settled in both halves.
  - ★ **THE PROBE THAT PRICED THE ALTERNATIVE, recorded because it would have to be re-run if
    anyone reopens this.** The prior record priced the wide reading as *"changes resting behaviour
    on every chart"*. **Measured #79 on the source, not recalled: it is more than a latch
    condition.** `active()` (`dv-legend.js:51`) returns `st.visible` at rest and `st.focus` in
    check — so under the wide reading `visible[]` **freezes at the first swatch click** and every
    later show/hide lands in `focus`. `render()`'s Reset guard (`:147`) is
    `count(st, st.visible) === st.ids.length && st.mode === 'rest'` — **both halves break**: the
    mode leaves `rest` and (absent an isolate-release, `:187`) never returns, and the count reads
    the frozen set ⇒ **Reset would sit permanently enabled on every chart after any swatch click.**
    Blast radius: 1 canon source · 5 chart reference snippets · **14 legend-bearing surfaces**
    (grep, `showroom/ reviews/ projects/`). ⇒ **Wide was never a one-line change; it needs
    `visible[]`/`focus` reseated at rest and the Reset guard rebuilt.** Dave ruled narrow with that
    cost in front of him.
    Ledger sibling: `notes/_MEMENTO-DECISIONS.md` § ★ #79.

### ⚠ FOUND, NOT FIXED — THE INTRO-MOTION LAW IS SHARED AND ONLY THE DONUT HALF IS BUILT

**Dave, at the #76 opener, unprompted:** *"so yes the donut but the segmented bar has a similar
animation."* He is right, and it is stronger than similar — **it is the same ruled law.**

- **DV-D12 (donut, BUILT):** ease-**IN** across exactly the first segment's arc · **LINEAR** through the
  middle · ease-**OUT** across exactly the last's · cruise `V=(S+w1+wN)/dur` so accel+cruise+decel sum
  to `dur`. One timeline, trapezoidal angular velocity.
- **Stacked bar (Batch 4 #4, ② wording IN FORCE, NOT BUILT):** *"they all grow at the same time, so
  they are floating and growing, rather than growing and 'handing off' to the next"* — first (bottom)
  `ease-in` · last (top) `ease-out` · intermediates `linear` · **per-segment curves on ONE timeline.**
- ⇒ **Same trapezoidal profile, two geometries** — one drawn round a ring, one drawn up a column.
- **⛔ THE BAR HALF WAS NEVER WIRED — ABSENCE, NOT REGRESSION.** Measured: `animation-timing-function`
  appears **0 times** in `snippets/Chart-bar.reference.html`, and every `rect.dv-series` style attribute
  carries nothing but `animation-delay` (`0/45/90/135/180/225ms`) against one shared `--grow` bezier.
  **A fixed stagger is one of the three shapes the ② wording explicitly superseded.** Same class as the
  review radios: ruled, then never built, and green in every gate because no gate ever asked.
- **★ THEY SHARE A LAW AND CANNOT SHARE AN IMPLEMENTATION.** The bar half must stay CSS (DEF-003 forbids
  JS transforms, and `_validate_behaviour.py` bans them by pattern); the donut half must stay JS (an SVG
  arc's angular extent is not CSS-animatable — Batch 3 #7 records that choice). ⇒ **the durable artefact
  is a NAMED LAW both geometries answer to, not shared code.**
- ⬛ **DAVE'S, DEFERRED BY HIS OWN RULING AT #76** (*"split now, log the bar gap"*) — deliberately not
  fixed inside the split, because one sentence naming two problems is how the last three recurrences
  started. The fix is CSS-only and small; what it needs is his eye on the motion, live.

---

**★ #86 (2026-08-02, triage-bankruptcy — inscribed #87): two DataViz items are now STANDING
GOVERNING RECORDS**, close conditions ratified by Dave via the review export
(`reviews/TRIAGE-BANKRUPTCY-2026-08-02-v1.html`, 19/19; ledger `notes/_MEMENTO-DECISIONS.md`
§ ★ #86-D1; register `knowledge/_GOVERNING-RECORDS.md`):
- **G15** — the DV-D13 donut centre figure + the `st.visible[id] = true` release wiring (both
  agent's calls, see the ⚠ ONE-ENACTMENT-CALL entry at :567 above) → **closes at Dave's sign-off
  eye** (already on `_REVIEW-SIGNOFF.md`'s backlog).
- **G16** — that :567 enactment call itself → **closes when Dave ratifies or reverses it.**

---

**★ #95 (2026-08-05, chart wave 2 — 3 Sonnet lanes + conductor serials):** EIGHT new members
landed and registered: butterfly-h · butterfly-v · histogram (lane ①), boxplot · bullet ·
candlestick (lane ②), pie · stacked-area (lane ③; the queue's "promote grouped/stacked bars
(D-Q3)" was struck STALE at #94 — landed 07-24). Receipts:
`notes/_receipts/2026-08-05-wave2-lane{1,2,3}-*.md` (replayed against disk by the conductor
before any serial edit). Serials enacted: `component-types.json` +8 `$members` (hand JSON per
receipts; hooks measured on the artefacts, not copied from the receipts),
`MIGRATED_SNIPPETS` +8, `CATEGORIES` +8, dtype vocabulary +7 in `_validate_dataviz.py`
(all seven cartesian, placed in the DV-D02-A partition in the same change per its import-time
totality assertion). Conductor fixes at replay: lane-① AUTO-MARKUP pairs + token manifests
(landed absent), pie + stacked-area dv-legend marker pairs, lane-② manifest prose-in-token-keys
stripped, boxplot/candlestick `--data-grid` UNBOUND (binding the pre-DV-D07 value to
`data/grid/color` was a measured DRIFT — unbinding receipts the ds-020 gap instead of filling it).
Gates: dataviz · snippets · coverage · radius · behaviour · partials · blast-radius · no-hardcode
all GREEN. ⚠ DECLARED, not fixed: type-composites gate was ALREADY red at HEAD (1011 violations,
82/82 files); the wave adds ~45 of the SAME classes (body font-family / h2 / th font-weight,
reproduced from its exemplars). a11y gate red at HEAD too, 8 fails, none in wave files.
⬛ OWED: render-verify all 8 (07-24 precedent) + Dave's showroom eyeball; all 8 metas carry
`tokenValidation.result: UNPROVEN` honestly. Lane flags for Dave: bullet 580×200 proportion ·
bullet range-band greys (color-mix, un-minted — grey-tint check) · candlestick colour-direction
redundancy (dv-011 partial) · histogram `.dv-leg-static` canon-folding candidate ·
stacked-area `--stack-fill-alpha` dial · stacked-area `fitOne()` `.dv-band` gap ·
pie sweep-hook `data-ri` fallback.
