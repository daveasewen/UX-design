# #260 lane F1 — core requests from the HISTOGRAM type partial

For the owner of `knowledge/canon/dv-render.js` and of `knowledge/_validate_dataviz.py`. A type
lane does not make these edits (brief, PARALLEL-SAFETY).

## 1 · A histogram's value axis wants a NAME, and the spec has nowhere to put one.

`{type, categories, series, format, unit, caption, categoryLabel, label}` names the CATEGORY axis
(`categoryLabel`) and nothing else. On a histogram the y axis is a frequency — "accounts",
"transactions", "customers" — and the series name is the only place that word can live, which is
why this partial reads `series[0].name` as the noun in the popover ("60 transactions") rather than
as a legend entry. That works, but it means one field is doing two jobs.

Requested change, verbatim: *"Add an optional `valueLabel` to the spec, beside `categoryLabel`.
The core would use it for the value-axis title the way `categoryLabel` is used for the category
axis, and a type partial would stop having to borrow the series name for it."*

**Workaround in place:** the series name IS the noun; the snippet and the test page name their one
series `transactions` / `accounts` (lower case, because it is read mid-sentence), and no value-axis
title is drawn.

## 2 · The core draws gridlines this type did not have, and cannot be told not to.

The baked histogram shipped with a baseline and NO gridlines and NO value tick labels — the
distribution's shape was the whole message. `dvRender` calls `furniture()` unconditionally, so the
engine-drawn version now carries four gridlines and four tick labels. That is arguably an
improvement (a count is easier to read off a gridded axis) and it is what every other cartesian
type does, so this lane did not fight it — but it is a visible change to a shipped component that
NO ONE chose, and it is the same seam the #259 donut lane asked about from the other side.

Requested change, verbatim: *"Honour a `fn.furniture` flag on a registered type function — `false`
to skip the `furniture(ctx, …)` call entirely, `'axis'` to draw the baseline and the tick labels
without the gridlines. The donut lane asked for the OFF switch because a radial chart pays for
furniture it discards; a histogram wants the dial in between."*

**Workaround in place:** none — the gridlines are drawn and the report names the change.

## 3 · Label thinning is frozen at first-render width (shared with the scatter request).

See `scatter.core-requests.md` §4. `dvRender` dispatches one `resize`, which re-FITS; it never
re-RENDERS, so the bin-label stride this partial computes from the plot width at draw time does not
change when the plot narrows. Measured: the 20-bin canvas labels 11 of 20 at a 1074px plot; after a
resize to a 654px plot the same 11 labels remain (and are proportionally tighter) rather than
thinning to 6.
