# Pie charts — brand guidance (ingested)

*Source: create.hsbc → Data visualisation → Pie charts (`pie-charts.html`), captured 2026-07-02
via Dave's authenticated session. Companion to `data-visualisation.md` — same enforcement-destiny
tags.*

## Usage
Proportion of a set total only. **Not for comparing one group to another** — a pie shows
group size relative to the whole. [ADVISORY — chart-type-choice check]

## Types
- **Standard pie** — filled circle, proportional slices.
- **Doughnut** — inner circle punched out, used to emphasise the total value.

## Structure — the hard rules
- **Maximum 6 slices — both pie and doughnut.** More than 6 categories → combine the
  smallest into a single "Other" slice, or use a different chart type. [BLOCKING-derivable —
  a countable rule; the cleanest gate candidate in the whole guidance set]
- **Values must add up to the total sum; always include value indicators.**
  [BLOCKING-derivable — arithmetic; same correctness family as the SME brief's
  "scheduled total must equal the sum of the rows"]
- **Start at 12 o'clock; order slices largest → smallest** (unless categories have an
  inherent order — then plot that order, consistently across the journey).
  [ADVISORY-derivable — angle inspection]
- Label + exact proportional value per slice; indicator lines to connect value/label with
  closely-spaced segments; key when labels are alphanumeric. [ADVISORY-derivable]
- Doughnut centre: **total value + descriptor together** — never a descriptor without the
  value. [ADVISORY-derivable]
- Direct labelling adjacent to segments (from the parent guideline). [ADVISORY]

## Content display
- **Always indicate when values are rounded.** [ADVISORY-derivable — sum≠100 with no
  rounding note]
- Labels/values inside a slice only when there's space to stay readable. [TASTE]
- Slice-ordering direction (clockwise/anti-): check assistive-technology accessibility.
  [ADVISORY]
- **Never enlarge or pull out slices** to emphasise scale in user journeys.
  [ADVISORY-derivable] Exception, explicitly granted: infographic/illustration contexts may
  emphasise slices (see the illustration standards — not yet ingested).
- Gauge pattern: a series of single-value doughnuts for part-to-whole of single values.
