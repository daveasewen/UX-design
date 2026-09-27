# Jev link check — 2026-09-27

provenance: hand-run by `notes/_jev-link-check/jev_link_check.py` under `s305-D55` (Dave, #305 sitting call 52, "yes") · ADVISORY, never a gate, never in the build (`s294-D10`) · raw answers `notes/_jev-link-check/2026-09-27-raw.jsonl` · receipts `knowledge/_jev-receipts.jsonl`

**330 of 330 links asked** (obeys, providesRole, answersIntent, hasDataShape). **13 look wrong** (p < 0.2, listed below for you to rule) · 183 silent (p > 0.8) · 134 ignored (the middle) · 0 error(s).

The bands were measured on 50 edges at #304 (seat J): every link under 0.2 was a fake, every link over 0.8 was real. That is n = 50 on one day — a flag is a suggestion, and the graph changes only by your word.

## This link looks wrong (p < 0.2)

| # | link | p | the designer's reason on the edge |
|---|---|---|---|
| 1 | `component:reorder` —providesRole→ `role:input` (Reorder → input) | 0.03 | — |
| 2 | `component:amount-display` —providesRole→ `role:input` (Amount display → input) | 0.05 | — |
| 3 | `component:divider` —providesRole→ `role:arrangement` (Divider → arrangement) | 0.07 | — |
| 4 | `component:runway-bar` —answersIntent→ `intent:one-number` (Coverage / runway bar → one-number) | 0.08 | — |
| 5 | `component:legend` —answersIntent→ `intent:what-is-this` (Legend → what-is-this) | 0.09 | — |
| 6 | `component:stepper` —providesRole→ `role:input` (Stepper → input) | 0.11 | — |
| 7 | `component:summary` —providesRole→ `role:status-surface` (Summary → status-surface) | 0.12 | — |
| 8 | `component:action-bar` —providesRole→ `role:action` (Action bar → action) | 0.14 | — |
| 9 | `component:eyebrow` —providesRole→ `role:page-title` (Eyebrow → page-title) | 0.15 | — |
| 10 | `component:tree` —providesRole→ `role:record-list` (Tree → record-list) | 0.15 | — |
| 11 | `component:legend` —hasDataShape→ `shape:no-data × control` (Legend → no-data × control) | 0.16 | — |
| 12 | `component:chart-pie` —obeys→ `rule:dv-008` (Pie chart → dv-008) | 0.17 | Horizontal scroll only as a last resort, and here it IS the last resort: the ring has fixed geometry and cannot compress, so ".dv-stage scrolls if the container is narrower" is the fallback this rule fences rather than a layout choice - the clause that settled this cell for chart-pie. |
| 13 | `component:form-layout` —providesRole→ `role:input` (Form layout → input) | 0.17 | — |

## Counts by edge type

| type | links | asked | looks wrong | silent | ignored |
|---|---|---|---|---|---|
| obeys | 168 | 168 | 1 | 83 | 84 |
| providesRole | 108 | 108 | 9 | 57 | 42 |
| answersIntent | 28 | 28 | 2 | 21 | 5 |
| hasDataShape | 26 | 26 | 1 | 22 | 3 |

Latency median 346 ms (range 303–60432) over 330 call(s). This run: 126 call(s) in 47 s.
