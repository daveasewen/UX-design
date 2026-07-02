# Bar charts — brand guidance (ingested)

*Source: create.hsbc → Data visualisation → Bar charts (`bar-charts.html`), captured 2026-07-02
via Dave's authenticated session. Companion to `data-visualisation.md` — same enforcement-destiny
tags: [BLOCKING-derivable] / [ADVISORY-derivable] / [TASTE].*

## Usage
Rectangular bars, heights/lengths proportional to values; vertical or horizontal. For
distribution, composition of specific sets, or comparison — highest/lowest, most common,
change over a period.

## Types
- **Simple** — the most common; compares a range of single-category values.
- **Grouped** — two or more data sets side-by-side, grouped in categories.

## Structure — the hard rules
- **All bar charts must include a zero baseline for the Y-axis.** [BLOCKING-derivable —
  axis-min check. Note: this is BAR-specific; line charts explicitly relax it — see
  `data-visualisation-line-charts.md`.]
- Title: descriptive, reflects the main insight. [TASTE]
- **Always use axis titles unless the labels are obvious** (both axes). [ADVISORY-derivable]
- X-axis: categories (+ optional tick marks) with per-category labels; Y-axis: values with
  incremental labels. Grid lines aid scale comprehension. [ADVISORY-derivable — presence]
- Key: required when using alphanumeric labelling. [ADVISORY-derivable]
- Filtering/config tools (optional): above the chart. [ADVISORY]
- Grouped extras: optional separator line between groups; group category label
  (description); group key for alphanumeric group labels. [ADVISORY]

## Content display
- Arrangement: values/categories well spaced, evenly distributed. **Don't use too many
  categories** — split into multiple charts or switch chart type. [ADVISORY/TASTE — no
  numeric cap given (contrast: pies cap at 6)]
- **Positive + negative values: vertical bars only. Don't put negative values on a
  horizontal bar chart.** [BLOCKING-derivable — orientation × sign check]
- Projected states: always label past vs projected. [ADVISORY-derivable]
