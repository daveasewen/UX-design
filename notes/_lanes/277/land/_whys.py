#!/usr/bin/env python3
"""_whys.py — THE 87 AUTHORED `$why` SENTENCES for #277 lane LA, and nothing else.

Data only, no I/O. `_splice.py` imports it to build the four proposed metas AND to
build WHYS.md, so the sentence a verifier grades and the sentence that lands are
one string, never two copies that can drift.

Each entry is (rule-id, $why, [anchor, ...]) where an ANCHOR is an EXACT SUBSTRING
of the LIVE meta this sentence is authored against. `_splice.py` greps every anchor
in the live bytes and REFUSES if one is missing — that is the whole discipline of
this lane: ⛔ a `$why` may only name a mechanism that is in the file.

A NEGATIVE anchor is written "!<needle>" and asserts the needle is ABSENT from the
live file. Two sentences rest on a declared absence (chart-line carries no
data-domain-min antiPattern; chart-bar declares no projected variant) and an absence
is checkable exactly as a presence is.

PROVENANCE OF THE 29 (`rule:dv-{line,pie,bar}-NNN`): lane CO authored them
(notes/_lanes/277/charts/), lane CP corrected two by addition, and the conductor's
Fable check (notes/_lanes/277/fable-check/CHECK.md) passed 27 and REDded two. Both
reds are replaced here, per s277-D1:
  · chart-bar -> dv-bar-001 — CO named an optional `title` PROP. There is none.
    Replaced with the CHECK's wording: the title is a TYPE ROLE.
  · chart-line -> dv-line-005 — CO borrowed DV-D02's viewBox pin as an interval
    reason. The ruling allowed drop-or-reword. KEPT, reworded, because the reworded
    sentence rests on two mechanisms that ARE in the file and are anchored here:
    the `when` clause "series 1-5 on ONE continuous time axis" and the `series`
    prop. The sentence says out loud that the binding is thin.

THE 47 (`rule:dv-NNN`, the family file) are s277-D3's reconciled matrix, re-derived
from notes/_lanes/277/page/_build_page.py: bar 17 / line 15 / pie 15. dv-013 and
dv-015 bind none. ⛔ The donut takes NO family rules (s277-D3 does not put them
there) — it takes the 11 pie-file rules and only those (s277-D2).
"""

# ---------------------------------------------------------------------------
# CHART-LINE — 9 line-file (s277-D1) + 15 family (s277-D3) = 24
# ---------------------------------------------------------------------------
LINE = [
    # --- the line file, lane CO's nine, dv-line-005 reworded -----------------
    ("rule:dv-line-001",
     "The zero y-axis is OPTIONAL for a line and MANDATORY for a bar, and this meta is the line side of that deliberate asymmetry - it carries no data-domain-min antiPattern, where chart-bar carries one.",
     ["antiPatterns", "!data-domain-min"]),
    ("rule:dv-line-002",
     "Shape per data set, not colour alone: the meta's `series` prop already names this rule and fixes the three marker geometries (circle r4.2 · square 8.4 · diamond ±4.9), so the rule IS the prop.",
     ["dv-line-002: circle r4.2 · square 8.4 · diamond ±4.9"]),
    ("rule:dv-line-003",
     "Axis titles, per-category X labels, incremental Y labels and gridlines are the parts DV-D07 mints tokens for (data/axis, data/grid) - the rule says which parts must exist, the meta says what colour they are.",
     ["DV-D07 ENACTED: axis text/ticks = data/axis", "gridlines = data/grid"]),
    ("rule:dv-line-004",
     "The reference point plus a tooltip repeating BOTH axis values is the dvTip popover in this meta's `motion.hover`, and the both-axes clause is why the popover cannot be a bare value.",
     ["Interactive value POPOVER (dvTip — behaviour partial)", "Values == table."]),
    ("rule:dv-line-005",
     "Comparable intervals and a gridline density the author may drop when it confuses is TASTE the meta hands to the author; the meta's `series` cap of 1–5 on ONE continuous time axis (`when`) is the only structural trace, and it is thin - this edge is the weakest of the nine.",
     ["series 1–5 on ONE continuous time axis", "\"name\": \"series\""]),
    ("rule:dv-line-006",
     "Dual y-axes only for different units is the rule this meta OBEYS BY YIELDING: its `when` hands the different-units case to chart-combo, so on this component the rule reads as a prohibition, and that is the binding worth recording.",
     ["yields to chart-combo (56, \\\"two measures in different units over one axis\\\") when units differ"]),
    ("rule:dv-line-007",
     "Filter/focus on multi-set charts is this meta's `legendFilter` prop - the rule is why that prop defaults to true rather than being an option.",
     ["\"name\": \"legendFilter\"", "data-series-toggle, aria-pressed"]),
    ("rule:dv-line-008",
     "End-line markers plus a key when intervals are tight, and explicit labelling of projected states, govern the multi-series variant this meta declares; nothing else in the meta supplies that labelling contract.",
     ["\"name\": \"multi-series\"", "2–5 measures; shapes + letters + legend names carry identity alongside colour."]),
    ("rule:dv-line-011",
     "Straight segments only, never gratuitous curves - the meta's first antiPattern cites this rule by id, so the edge makes an existing prose citation a graph edge.",
     ["Curved/smoothed series paths (dv-line-011 — straight segments only)"]),

    # --- the family file, 15 ------------------------------------------------
    ("rule:dv-001",
     "Don't alter the scale to over- or understate a trend: this meta's `responsive.rule` relayouts by baked fractions at a fixed height with the viewBox pinned 1:1, so a narrower container moves x positions and never re-stretches the y scale the trend is read off.",
     ["fixed height, TEXT NEVER SCALES (viewBox pinned 1:1)"]),
    ("rule:dv-002",
     "A full chart at a reasonable scale is enforced here by handoff, not by shrinking: the `when` yields \"to chart-sparkline (30, 'inline scale, no axes') when span.cols < 6\", so below six columns this component declines rather than drawing a cramped line.",
     ["to chart-sparkline (30, \\\"inline scale, no axes\\\") when span.cols < 6"]),
    ("rule:dv-003",
     "Never omit data to shift the interpretation: this meta makes completeness survive the loss of its own engine - with JS off \"The data is still complete and still labelled\", because the table is authored in the markup and not generated.",
     ["The data is still complete and still labelled"]),
    ("rule:dv-005",
     "The tabular alternative AND the link to it are two props here: `data` cites this rule by id as a real dv-table in the figure, and `tablePopover` is the 'View as table' toggle that links to it.",
     ["Real <table class=\\\"dv-table\\\"> in the figure (dv-005)", "'View as table' ⇄ 'Hide table' toggle top-right"]),
    ("rule:dv-006",
     "The title-reflects-the-main-insight limb of this rule is cited by id inside the meta's own `title` prop, and the tooltip limb is the dvTip popover whose values are pinned to the table's - the edge makes an existing prose citation a graph edge.",
     ["OPTIONAL visible title slot (.dv-title, dv-006: reflects the main insight)"]),
    ("rule:dv-007",
     "Chart elements must respond dynamically on resize while titles keep scaling with the user's text setting: this meta's fit does the first with a baked-fraction relayout on a single rAF-debounced resize, and refuses to do the second to the type by pinning the viewBox.",
     ["to the container width on a single rAF-debounced resize"]),
    ("rule:dv-008",
     "Horizontal scroll only as a last resort: on this meta scrolling is explicitly the FALLBACK and not the layout - the fit reflow is the answer, and the static 580×260 plus horizontal scroll is what is left when the engine cannot run.",
     ["JS-off falls back to the static answer: fixed 580×260 + horizontal scroll"]),
    ("rule:dv-009",
     "Flat colour only, no gradient and no 3D: every fill this meta declares is a single token value - marker fill is the series token, stroke is background/default at 2.5 - and the antiPattern guarding the same ground from the other side is \"Raw hex strokes (dv-017)\".",
     ["fill = the series token, stroke = background/default (page) at 2.5", "Raw hex strokes (dv-017)"]),
    ("rule:dv-010",
     "Nothing may obscure the data: this meta's one overlay is the dvTip popover and it edge-flips rather than covering the plot, which is why the flip is declared in `motion.hover` at all.",
     ["pointer + keyboard focus, edge-flips, role=status"]),
    ("rule:dv-011",
     "Don't let colour carry the narrative alone: the `series` prop cites this rule by id in the same breath as the marker shape and the letter key - \"colour is never the only channel (dv-011)\".",
     ["colour is never the only channel (dv-011)"]),
    ("rule:dv-012",
     "Colour focuses attention and is never the chart's background: this meta's `tokens.surface` is background/default, the page's own ground, and the only attention colour in the component is the series token on the stroke.",
     ["\"surface\": \"background/default (data-surface=\\\"page\\\")\""]),
    ("rule:dv-014",
     "Same data, same colour across a journey: this meta's `mustNotNeighbour` cites the rule by id and carries the rule's own scope word - \"in the same journey\".",
     ["A second chart re-using these series colours for DIFFERENT data in the same journey (dv-014)"]),
    ("rule:dv-016",
     "The 3:1 floor for chart building blocks is cited by id twice here and split exactly where the rule splits: series strokes are measured against the page in both modes as BLOCKING, and the gridline is declared decorative-exempt and advisory.",
     ["(dv-016 ≥3:1 BLOCKING clean)", "Gridline contrast decorative-exempt (dv-016 advisory by design)"]),
    ("rule:dv-017",
     "Only palette colours in a chart: the meta's antiPatterns cite this rule by id as \"Raw hex strokes (dv-017)\", and its `tokens.series` binds data/series/1–3 by role rather than by value, so there is no path by which a raw hex reaches a stroke.",
     ["Raw hex strokes (dv-017)", "data/series/1–3 bound here"]),
    ("rule:dv-018",
     "A different colour per line is the `series` prop's own contract - each series carries colour (data/series/N) plus a marker shape and a letter key - with `tokens.series` naming the bound set the 1–5 range draws from.",
     ["each series carries colour (data/series/N)", "data/series/1–3 bound here"]),
]

# ---------------------------------------------------------------------------
# CHART-PIE — 10 pie-file (s277-D1/D2, dv-pie-003 held off) + 15 family = 25
# ---------------------------------------------------------------------------
PIE = [
    # --- the pie file, ten (dv-pie-003 is the donut's alone, s277-D2) -------
    ("rule:dv-pie-001",
     "Start at 12 o'clock, largest to smallest unless the categories have an inherent order - the angle contract for the sweep this meta's motion.entry bakes (data-cx/-cy/-ro/-a1/-a2, no data-ri), which is where the start angle and the segment order are fixed, at generation time.",
     ["segments bake the sweep contract (data-cx/-cy/-ro/-a1/-a2, NO data-ri)"]),
    ("rule:dv-pie-002",
     "Label plus exact proportional value per slice, with indicator lines when segments crowd, is precisely this meta's `labelling` = spider default: the leader line IS the indicator line the rule asks for.",
     ["spider = letter on a short leader outside the ring + vertical legend [swatch][letter][name]"]),
    ("rule:dv-pie-004",
     "Direct labelling adjacent to segments is the meta's second declared variant ('direct labels'), so the rule names one of the two things this component can be.",
     ["\"name\": \"direct labels\"", "name + £value · % on each leader"]),
    ("rule:dv-pie-005",
     "Labels inside a slice only where they stay readable is the TASTE half of the labelling choice, and it is why this meta's antiPatterns ban white type on the fills and put labels outside the ring.",
     ["White letters on segment fills (type26-013", "never sit ON the fills"]),
    ("rule:dv-pie-006",
     "Slice-ordering direction has to be checked against assistive technology, and this meta makes every segment a focus stop with aria-label == data-tip == table - the order those stops are read in is what the rule is about.",
     ["Segments = focus stops (tabindex 0 → dvTip on focus)", "aria-label == data-tip == table"]),
    ("rule:dv-pie-007",
     "Never enlarge or pull out a slice to emphasise it: the meta has no exploded variant and its motion block moves segments only by a radial sweep that ends flush, so the rule is the reason no such variant exists.",
     ["Baked state = full wedges + visible annotations", "Recomputing arc geometry at runtime outside the sweep hook"]),
    ("rule:dv-pie-008",
     "Proportion of a set total ONLY, never group-to-group comparison - this is the `when` gate of the meta stated from the guidance side, and it is what sends comparison to chart-bar.",
     ["answers=composition AND parts ≤ 5 AND total=not printed"]),
    ("rule:dv-pie-009",
     "Maximum 6 slices, pie and doughnut alike: the meta's `slices` prop cites this rule by id and carries the 'combine the smallest into Other' remedy, so the edge records a binding the meta already states in prose.",
     ["Maximum 6 (dv-pie-009); more → combine smallest into 'Other'."]),
    ("rule:dv-pie-010",
     "Values must add up to the declared total: this meta prints NO centre figure, so data-total is the only place the total lives and the arithmetic is unverifiable by eye - the rule binds harder here than on the donut, not less.",
     ["Values must sum to the total carried on data-total (dv-pie-010) even though no centre figure displays it."]),
    ("rule:dv-pie-011",
     "Always indicate rounding: the value ⇄ percent toggle in this meta's `valueMode` prop is exactly where rounded percentages appear, and the rule is the contract that toggle has to honour.",
     ["\"name\": \"valueMode\"", "direct labels AND the table column mirror the active mode"]),

    # --- the family file, 15 ------------------------------------------------
    ("rule:dv-003",
     "Never omit data to distort the reading: with the engine off this meta still hands over the whole set - the five categories, their pounds and their percentage shares open and read with no script at all - because the table is authored in the markup, not generated.",
     ["the five categories, their pounds and their percentage shares open and read with no script at all"]),
    ("rule:dv-004",
     "Minimum 2px separation between colour blocks, never colour alone to separate values: this meta's `tokens.separation` cites the rule by id as a page-coloured 2px stroke on every segment, and its antiPatterns ban the gapless case.",
     ["stroke = background/default (page) at 2px on every segment (dv-004)", "Gapless segments without the 2px page stroke (dv-004)"]),
    ("rule:dv-005",
     "A tabular alternative, always: the meta's antiPatterns cite this rule by id - \"A pie without its real data table (dv-005)\" - and the behaviour block names the real dv-table inside a native details/summary as the thing that survives JS-off.",
     ["A pie without its real data table (dv-005)"]),
    ("rule:dv-006",
     "The circular-chart limb of this rule - direct labelling adjacent to segments - is this meta's `labelling` enum itself: direct is name + value in place, no legend, which is why the prop has two values and not one.",
     ["direct = name + value in place, no legend"]),
    ("rule:dv-007",
     "All the data visible at the smallest viewport, else explicit navigation: this meta cannot answer by compressing, because compressing a circle distorts, so its declared answer at narrow widths is the .dv-stage scroll - the rule's else-branch, chosen deliberately.",
     ["fixed geometry (compressing a circle distorts)"]),
    ("rule:dv-008",
     "Horizontal scroll only as a last resort, and here it IS the last resort: the ring has fixed geometry and cannot compress, so \".dv-stage scrolls if the container is narrower\" is the fallback this rule fences rather than a layout choice - the clause that settled this cell for chart-pie.",
     [".dv-stage scrolls if the container is narrower"]),
    ("rule:dv-009",
     "Flat two-dimensional fills only, no 3D and no gradient: every fill this meta declares is one token - data/series/1–5, the same series as the donut - carried on baked wedges with a page-coloured stroke, so there is no gradient, bevel or shadow layer anywhere in the component.",
     ["\"series\": \"data/series/1–5 (same series as the donut; identical measured contrast)\""]),
    ("rule:dv-010",
     "Nothing that obscures the data: the one thing this meta floats over the ring is the dvTip popover, and its emphasis mechanism is subtractive - legend/segment highlight dims the OTHER groups - so nothing is drawn on top to make a slice stand out.",
     ["legend/segment highlight dims the OTHER groups"]),
    ("rule:dv-011",
     "Colour may not carry the narrative alone, and this meta says so in its own words: identity = letter/name + position + table, never colour alone.",
     ["identity = letter/name + position + table, never colour alone (1.4.1)"]),
    ("rule:dv-012",
     "Colour focuses attention and is never the chart's background: this meta's `tokens.surface` is background/default, the page's own ground, and the only colour it spends is on the wedges themselves.",
     ["\"surface\": \"background/default (data-surface=\\\"page\\\")\""]),
    ("rule:dv-014",
     "Same data, same colour across the journey: this meta's `mustNotNeighbour` cites the rule by id - charts re-using these series colours for different data - which is the journey-scope half of the rule stated as a neighbour ban.",
     ["Charts re-using these series colours for different data (dv-014)"]),
    ("rule:dv-016",
     "Chart building blocks must clear 3:1: this meta states the floor for its fills (segment fills ≥3:1 vs the page both modes), and its `$survey` records why the rule's axis/gridline limb has nothing to bind to here - pie/donut carry NO axis or gridline CSS at all.",
     ["Segment fills ≥3:1 vs the page both modes", "pie/donut carry NO axis or gridline CSS at all"]),
    ("rule:dv-017",
     "Only palette colours in charts: every colour this meta names is a token role - series, separation, leaders, labels, surface - and the `$survey` records \"No new tokens minted\", so there is no path by which a raw hex reaches a wedge.",
     ["No new tokens minted."]),
    ("rule:dv-018",
     "Different colours within a single-variable circular chart: the `slices` slot accepts one capability, proportion-slices, and the series token spends a different colour on each part of that one variable.",
     ["proportion-slices", "\"series\": \"data/series/1–5 (same series as the donut; identical measured contrast)\""]),
    ("rule:dv-019",
     "Adjacent saturated near-complementary fills shimmer, and the rule names the dv-004 gap as its structural defence: on a ring EVERY pair is adjacent, and this meta already carries that defence as a 2px page stroke on every segment, with the gapless case banned in antiPatterns.",
     ["stroke = background/default (page) at 2px on every segment (dv-004)", "Gapless segments without the 2px page stroke (dv-004)"]),
]

# ---------------------------------------------------------------------------
# CHART-BAR — 10 bar-file (dv-bar-001 REPLACED) + 17 family = 27
# ---------------------------------------------------------------------------
BAR = [
    # --- the bar file, ten --------------------------------------------------
    ("rule:dv-bar-001",
     "A title that reflects the main insight is the slot `tokens.font-family` types as .t-cm-section-label; the rule is why that slot is typed at all rather than left to the author.",
     ["title .t-cm-section-label"]),
    ("rule:dv-bar-002",
     "Axis titles on both axes unless the labels are obvious - the meta's tokens.font-family composite routes labels, axis, legend and values through one type role, .t-cm-chart-label at 12/500, and tokens.axis mints data/axis (DV-D07) for them, so the get-out clause changes what is drawn and never which token pays for it.",
     [".t-cm-chart-label / .t-cm-chart-value = 12/500", "\"axis\": \"data/axis (DV-D07 two-channel role"]),
    ("rule:dv-bar-003",
     "Categorical X with per-category labels, incremental Y values, gridlines for scale: the structural parts DV-D07's data/axis and data/grid roles exist to colour.",
     ["\"gridlines\": \"data/grid (DV-D07 two-channel: color + alpha slot 1.0)", "\"axis\": \"data/axis (DV-D07 two-channel role"]),
    ("rule:dv-bar-004",
     "A key is required whenever labelling is alphanumeric, which is exactly this meta's on-chart letter keys (.dv-barkey) and its lettered legend swatches in the grouped and stacked variants.",
     [".dv-barkey", "shaped+lettered legend keys"]),
    ("rule:dv-bar-005",
     "Filtering and configuration tools sit ABOVE the chart - the placement contract for this meta's sort segmented control and its table-view dropdown.",
     ["switched by a seg control that CONSUMES the Segmented-control atom", "TABLE-VIEW POPOVER"]),
    ("rule:dv-bar-006",
     "Group separators, group category labels and a group key for alphanumeric group labels are the anatomy of this meta's 'grouped column' variant; no other rule supplies it.",
     ["\"name\": \"grouped column\"", "shaped+lettered swatches mirror on-chart keys"]),
    ("rule:dv-bar-007",
     "Negative values on a horizontal bar are banned - the meta's antiPatterns cite this rule by id, and its `orientation` prop's 'bar' value carries the positives-only note.",
     ["Negative values on a horizontal bar (dv-bar-007 — verticals only)", "bar = horizontal single-series (positives only, dv-bar-007)"]),
    ("rule:dv-bar-008",
     "Past versus projected must always be labelled. This meta declares no projected variant today, and the rule is what any future one would have to satisfy - a binding constraint, not a described feature.",
     ["\"variants\"", "!projected"]),
    ("rule:dv-bar-009",
     "The zero baseline is mandatory for every bar chart: the meta's antiPatterns cite this rule by id and name data-domain-min=\"0\" as the mechanism.",
     ["A non-zero baseline (dv-bar-009: data-domain-min=\\\"0\\\" always)"]),
    ("rule:dv-bar-010",
     "Well spaced, evenly distributed, and not too many categories - the arrangement rule the meta's span.cols 4–12 and its DV-D02 compress-never-scale responsive rule between them have to satisfy.",
     ["\"min\": 4", "\"max\": 12", "DV-D02: compress width, NEVER scale"]),

    # --- the family file, 17 ------------------------------------------------
    ("rule:dv-001",
     "Don't truncate or alter the scale to overstate a trend - the family rule whose own enforcement note names bar charts, and whose per-type enactment is this meta's antiPattern \"A non-zero baseline (dv-bar-009: data-domain-min='0' always)\". The edge records the family reason that antiPattern exists.",
     ["A non-zero baseline (dv-bar-009: data-domain-min=\\\"0\\\" always)"]),
    ("rule:dv-002",
     "A full chart at a reasonable scale is what this meta's `responsive.rule` protects: DV-D02 compresses width and NEVER scales, and the fit relayouts horizontal positions only, so narrowing the container can never shrink the chart into an unreadable one.",
     ["DV-D02: compress width, NEVER scale"]),
    ("rule:dv-003",
     "Show the full data set and never drop rows to shift the reading: this meta's `sort` prop re-orders and never omits - the table mirrors the active order via baked tbody data-dv-view variants, so a view is a permutation of the data, not a subset of it.",
     ["the table mirrors the active order via baked <tbody data-dv-view> variants"]),
    ("rule:dv-004",
     "Never let colour alone do the separating: on this meta the fills that actually abut are the stacked column variant's, and the channel it declares there is the in-segment letter key - the rule is why that key is ON the segment and not in the legend alone.",
     ["in-segment letter keys"]),
    ("rule:dv-005",
     "The tabular alternative is this meta's `data` prop verbatim - the a11y spine AND the tabular alternative, cited by id - surfaced by the table-view popover, with the antiPattern banning a chart without it.",
     ["the a11y spine AND the tabular alternative (dv-005)", "A chart without its real data table (dv-005)"]),
    ("rule:dv-006",
     "Labels and tooltips must repeat the data point's values without drifting from them, and this meta makes that structural: each bar carries aria-label + data-tip with the popover value == the table value, one source.",
     ["each bar carries aria-label + data-tip (popover value == table value, one source)"]),
    ("rule:dv-007",
     "Chart elements must respond dynamically on resize while titles keep scaling with text: this meta's responsive rule splits exactly there - fitCharts relayouts HORIZONTAL positions only, viewBox pinned 1:1 - so the geometry moves and the type is never shrunk with it.",
     ["dv-behaviour fitCharts relayouts HORIZONTAL positions only"]),
    ("rule:dv-008",
     "Horizontal scroll only as a last resort: the fit reflow is this meta's first answer and scrolling is what is left when it cannot run - \"JS-off keeps the static answer (fixed geometry + scroll)\".",
     ["JS-off keeps the static answer (fixed geometry + scroll)"]),
    ("rule:dv-009",
     "Flat two-dimensional fills only: the meta's antiPatterns cite this rule by id - \"Gradient/3D/shadow fills (dv-009 flat fills only)\" - so the edge makes an existing prose citation a graph edge.",
     ["Gradient/3D/shadow fills (dv-009 flat fills only)"]),
    ("rule:dv-010",
     "Nothing may obscure the data, and this meta floats two things over it - the table popover and the value tip - both built on one anchored-overlay recipe with Esc dismiss and a refocus, which is the rule's uncluttered-overlay contract turned into a recipe.",
     ["(anchored-overlay recipe)", "Esc dismiss → refocus"]),
    ("rule:dv-011",
     "Don't rely on colour alone to carry the narrative: this meta's `nonText` says it in the rule's own terms - multi-series adds shape (circle/square/diamond) + letter + name, colour never the only channel - and the status variant carries meaning in the label under each bar.",
     ["colour never the only channel", "status meaning carried by the label under each bar (R-D6 A′)"]),
    ("rule:dv-012",
     "Colour focuses attention and never becomes the chart's background: this meta's `tokens.surface` is background/default, the page's own ground, and the attention colour lives in `motion.hover` as a brightness lift instead.",
     ["\"surface\": \"background/default (data-surface=\\\"page\\\")\"", "brightness(1.12) light / (1.22) dark emphasis"]),
    ("rule:dv-014",
     "Same data, same colour across a user journey: the meta's `mustNotNeighbour` cites the rule by id - a second chart re-using these series colours for DIFFERENT data - which is the journey-scope half of the rule stated as a neighbour ban.",
     ["A second chart re-using these series colours for DIFFERENT data (dv-014)"]),
    ("rule:dv-016",
     "The 3:1 floor for chart building blocks is cited by id twice here and split where the rule splits: series fills ≥3:1 vs the page both modes as BLOCKING, and gridline contrast decorative-exempt, dv-016 advisory by design.",
     ["Series fills ≥3:1 vs the page both modes (dv-016 BLOCKING)", "dv-016 advisory by design, no grid contrastPair declared"]),
    ("rule:dv-017",
     "Only palette colours in a chart: the meta's antiPatterns cite this rule by id - \"Raw hex series fills (dv-017 — var() tokens only)\" - and every series value in `tokens` is a role name rather than a colour.",
     ["Raw hex series fills (dv-017 — var() tokens only)"]),
    ("rule:dv-018",
     "A different colour per data-set variable is what this meta's `series` prop enumerates - categorical on data/series/1–5, multi on series/1–3 with shaped+lettered legend keys - and the single-series variant's ONE colour is the same rule read from the other side.",
     ["multi = grouped/stacked use series/1–3 with shaped+lettered legend keys", "single series, ONE colour (dv-014)"]),
    ("rule:dv-019",
     "Vibration needs near-equal value plus wide hue separation, and this meta declares its categorical fills mode-stable isoluminant - equal value by construction - so the rule binds here hardest of the three: the separation is geometric (bars do not abut) plus the declared high-contrast remap onto data/series-high-contrast/1–3.",
     ["data/series/1–5 (mode-stable isoluminant, ≥3:1 both modes)", "high-contrast remap data/series-high-contrast/1–3 (data-contrast=\\\"high\\\")"]),
]

# ---------------------------------------------------------------------------
# CHART-DONUT — the 11 pie-file rules and ONLY those (s277-D2).
# ⛔ NOT the 47: s277-D3 does not put family rules on the donut. Do not widen.
# ---------------------------------------------------------------------------
DONUT = [
    ("rule:dv-pie-001",
     "Start at 12 o'clock and order slices largest to smallest unless the categories carry their own order: the angles are fixed at generation time here - segments bake the sweep contract (data-cx/-cy/-ro/-ri/-a1/-a2) - and the antiPattern against recomputing arc geometry at runtime is what keeps that order from drifting.",
     ["segments bake the sweep contract (data-cx/-cy/-ro/-ri/-a1/-a2)", "Recomputing arc geometry at runtime outside the sweep hook"]),
    ("rule:dv-pie-002",
     "Label plus exact proportional value on every slice, indicator lines where segments crowd, a key when the labels are letters: the meta's default `labelling` = spider is all three at once - a letter on a short leader outside the ring plus a vertical legend of swatch, letter and name - the leader IS the indicator line and the legend IS the key.",
     ["spider = letter on a short leader outside the ring + vertical legend [swatch][letter][name]"]),
    ("rule:dv-pie-003",
     "The centre must carry the total value AND its descriptor, never a descriptor without the value: this is the only component in the family with a `total` prop - the centre total typed .t-cm-figure-3 - and its `when` makes that printed centre figure the very thing that beats chart-pie. The rule binds here and nowhere else (s277-D2).",
     ["\"name\": \"total\"", "Centre total — .t-cm-figure-3 (24px/500", "total=printed as a centre figure"]),
    ("rule:dv-pie-004",
     "Direct labelling adjacent to segments is this meta's second declared variant: name + value + % on each leader, in place, rather than in a legend across the card.",
     ["\"name\": \"direct labels\"", "name + £value · % on each leader"]),
    ("rule:dv-pie-005",
     "Labels sit inside a slice only where they stay readable, and this meta answers by taking them off the fills entirely - spider letters and direct labels never sit ON the fills - with the kit's letters-on-segments variant HELD rather than promoted, for the same reason.",
     ["spider letters and direct labels never sit ON the fills", "is NOT promoted"]),
    ("rule:dv-pie-006",
     "The direction slices are ordered in must be checked against assistive technology, and this meta makes that order audible: segments are focus stops that raise dvTip on focus, and every segment's aria-label == data-tip == table, so the sweep order IS the reading order.",
     ["Segments = focus stops (tabindex 0 → dvTip on focus)", "aria-label == data-tip == table"]),
    ("rule:dv-pie-007",
     "Never enlarge or pull out a slice for emphasis: this meta has no exploded variant and structurally cannot grow one - geometry is generation-time; behaviour only toggles baked variants - and its emphasis channel is a brightness lift that dims the OTHER groups, not displacement.",
     ["geometry is generation-time; behaviour only toggles baked variants", "legend/segment highlight dims the OTHER groups"]),
    ("rule:dv-pie-008",
     "A ring shows a part's size relative to the whole and never compares one group to another: this meta's `when` demands answers=composition AND parts sum to a whole, which is the rule's usage gate stated from the routing side.",
     ["answers=composition AND parts sum to a whole"]),
    ("rule:dv-pie-009",
     "Maximum 6 slices for pie and doughnut alike: the meta's `slices` prop cites this rule by id and carries its remedy - more, and the smallest combine into 'Other' - and the antiPatterns repeat it, so the edge records a binding the file already states twice.",
     ["Maximum 6 (dv-pie-009); more → combine smallest into 'Other'.", "More than 6 slices (dv-pie-009 — combine into 'Other')"]),
    ("rule:dv-pie-010",
     "Values must add up to the total, and the value indicators must be there: here the total is ON SCREEN, so the arithmetic is checkable by eye - values must sum to the displayed centre total (dv-pie-010, data-total attr) - and tokenValidation records the measured proof, sum 2320 = data-total.",
     ["Values must sum to the displayed centre total (dv-pie-010, data-total attr)", "sum 2320 = data-total"]),
    ("rule:dv-pie-011",
     "Always indicate when values are rounded: the percent arm of this meta's `valueMode` is where rounded readings appear, and the meta's answer is that the exact one is never lost - tips/aria carry both readings always, and the centre total, the direct labels and the table column all mirror the active mode together.",
     ["Tips/aria carry both readings always.", "centre total, direct labels AND the table column mirror the active mode"]),
]

COMPONENTS = {
    "chart-line": LINE,
    "chart-pie": PIE,
    "chart-bar": BAR,
    "chart-donut": DONUT,
}

# The expected shape, asserted by _splice.py — s277-D1 + D2 + D3, counted.
EXPECTED = {
    "chart-line": (9, 15),    # line file (dv-line-005 KEPT, reworded) + family
    "chart-pie": (10, 15),    # pie file minus dv-pie-003 + family
    "chart-bar": (10, 17),    # bar file + family
    "chart-donut": (11, 0),   # pie file entire, NO family (s277-D3 does not widen)
}
