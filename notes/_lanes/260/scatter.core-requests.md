# #260 lane F1 — core requests from the SCATTER type partial

For the owner of `knowledge/canon/dv-render.js` and of `knowledge/_validate_dataviz.py`. A type
lane does not make these edits (brief, PARALLEL-SAFETY); each is written as the change it asks for,
verbatim, with the local workaround that stands in for it named so the workaround can be deleted
when the request lands.

## 1 · The spec has no NUMERIC X. This is the big one.

Every registered type reads `spec.categories` as a BAND axis — n equal slots, order only. A
scatter's x is a MEASUREMENT: the step from 28 to 35 has to be visibly shorter than the step from
122 to 140, or the chart is not a scatter, it is a dot plot with the x labels sorted.

Requested change, verbatim: *"Let a spec carry a numeric x. Either `categories` may be an array of
NUMBERS (validated as finite, ordered by the type that wants it), or the spec grows an optional
`x: [ ... ]` parallel to `series[].values`. The core would then own the x scale the way it already
owns the value scale — `nice()`, the tick list, and a `ctx.xf(n)` beside `ctx.vf(n)` — and the
axis-2 furniture (vertical gridlines + x tick labels) would be emitted by `furniture()` under a
third `fn.axis` value ('xy') instead of by every cartesian type that needs both axes."*

**Workaround in place:** `dv-render-scatter` parses a number out of each category string
(`parseFloat`) and, when EVERY category parses, builds its own x scale off `dvRender.util.nice`
and emits the vertical gridlines, the x tick labels and the left axis rule itself. When any
category does not parse it falls back to evenly spaced band centres. Cost: ~40 lines that belong
in the core, and one silent behaviour change — a scatter whose x values happen to be non-numeric
labels renders as an ordinal dot plot rather than refusing.

**Driven, so the workaround is not taken on trust:** the rendered point centres measure
7.143–7.167 px per £1k across all 12 points (constant slope), with adjacent gaps of 43.0px to
128.9px where an even band axis would have put every gap at 72.9px. Mutating one category to a
non-number collapses the gaps to 89.4–89.6px — the assertion discriminates.

## 2 · A multi-series scatter has to share its x values, and real segments do not.

`validate()` requires `series[i].values.length === categories.length`, so every series is sampled
at the SAME x positions. The baked specimen this type replaces plotted three segments at twelve
DIFFERENT incomes each — which the ruled spec cannot express.

Requested change, verbatim: *"Allow a series to be sparse — either a `null` in `values` meaning
'no observation at this x' (validated as null-or-finite rather than finite), or a per-series `x`
array. Without one of the two, a multi-series scatter is a matrix of shared x positions, which is
a legitimate chart but not the one the library used to draw."*

**Workaround in place:** the snippet's segment figure re-authors the three segments onto seven
SHARED income bands. The numbers are honest and the chart reads correctly; it is a different
sampling from the bake, and the report says so.

## 3 · `_validate_dataviz.ENGINE_TEST_PAGE` needs the two new mappings (INTEGRATION, not core).

`ENGINE_TEST_PAGE` in `knowledge/_validate_dataviz.py` maps a snippet basename to its driven test
page. dv-004's receipt route only fires for donut/pie/stacked, so **neither of this lane's types
needs the mapping to pass a gate today** — but the map is the reviewer-readable statement of which
snippet is exercised by which page, and it is now wrong by omission:

    "Chart-scatter.reference.html":    "scatter.html",
    "Chart-histogram.reference.html":  "histogram.html",

A gate is not a type lane's file to edit (brief), so this is filed rather than done.

## 4 · A re-render does not re-thin, and the resize hook cannot ask it to.

`dvRender` dispatches one `resize`, which re-FITS the existing marks; it never re-RENDERS. Any
decision a type partial makes from the plot WIDTH at render time — label thinning here, the
histogram's bin labels, a future collision-avoided tick set — is therefore frozen at the width the
chart was first drawn at. Requested change, verbatim: *"Give a type partial a way to be re-entered
on a width change: either the core listens for its own re-fit and re-calls `draw(ctx)` when the
plot width has moved by more than some fraction, or it exposes `dvRender.redraw(figure)` so a
consumer can wire the decision itself. Today the only honest answer a type partial has is to
compute for the width it was given and let the fit translate the result."*
