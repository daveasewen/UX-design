# Line charts — brand guidance (ingested)

*Source: create.hsbc → Data visualisation → Line charts (`line-chart.html`), captured
2026-07-02 via Dave's authenticated session. Companion to `data-visualisation.md` — same
enforcement-destiny tags.*

## Usage
Markers at regular intervals connected by straight lines; the standard type for change over
time and comparing data sets. One line per group. **Always horizontal orientation.**

## Types
- **Standard** — one line per data set; multiple lines per graph allowed.
- **Spark (sparkline)** — simplified high-level overview, minimal labelling.

## Structure — the hard rules
- **Straight lines between data points. Never gratuitous curves for aesthetics — they
  distort the data.** [BLOCKING-derivable — path/interpolation inspection; the line-chart
  counterpart of "no 3D/gradients"]
- **Zero y-axis is OPTIONAL here** — use it only when it aids interpretation. ⚠ Deliberate
  asymmetry with bar charts, where the zero baseline is mandatory. Record both; never let a
  bar rule bleed into line enforcement. [ADVISORY — needs the chart-type context]
- **Different-shaped markers per data set** (not colour alone — pairs with the parent
  "don't rely on colour" rule). Single data set: markers not required. [ADVISORY-derivable]
- Axis titles unless obvious; per-category X labels, incremental Y labels; grid lines for
  scale. [ADVISORY-derivable]
- Key required on complex charts (marker ↔ data set); data sets may be shown/hidden.
- Reference point + tooltip: tooltip repeats the data point's values on **both axes**
  without obscuring the chart. [ADVISORY-derivable]

## Content display
- Measurement intervals comparable, similar scale; single-axis grid for large intervals,
  double-axis for small; drop gridlines if they confuse. [TASTE]
- **Dual y-axes only for different measurement units, clearly labelled** — key states which
  axis each set refers to. [ADVISORY-derivable]
- Multi-set charts: include filter/focus functionality; consider show/hide toggles for
  lines and markers. [ADVISORY]
- End-line markers + key when markers would obscure small intervals; colours distinguish
  sets. Projected states: clear labelling; trends: end-line markers. [ADVISORY]

## Spark charts
- Structure (mostly optional): title; end value; change value + change indicator (+/−);
  optional x-axis as zero baseline; the line; reference point at the end value.
- **Aspect ratio: match the height of the surrounding content — never exaggerate the
  spark's proportions.** [ADVISORY-derivable — height ratio vs container]
- In tables: group all data related to the spark sequentially — never split it.
  [ADVISORY-derivable]
