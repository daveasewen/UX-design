---
name: icon-gap-download-active
description: "filled \"download-active\" glyph missing (HSBC lib + dynamic-weight); icon-link active-state deferred to label-only"
metadata: 
  node_type: memory
  type: reference
  originSessionId: b6d4d256-65cf-4438-9588-8f44138e09e2
---

GAP (2026-06-29, Dave-confirmed): no FILLED/active download glyph exists. The HSBC library has `download.svg` (line) but NO `download-active` — though 45 other `global-controls` glyphs DO have `-active` filled pairs (the convention = the filled silhouette of the resting line glyph; cf. `bookmark.svg` vs `bookmark-active.svg`). The dynamic-weight set renders download's active as a HEAVIER STROKE, not a fill, because download is a LINE-ONLY icon (arrow + tray, nothing enclosed to fill).

DECISION: the icon-link active state = the label's hover/pressed underline for now; the filled-icon swap is DEFERRED until a real filled download asset exists (authored-interim or official HSBC). Logged in `knowledge/_ICON-GAPS.md`. The icon gate byte-matches inline `<svg>` paths against `assets/icons/**/*.svg`, so any active glyph must be a real library file (can't inline-author one). Revisit: add the asset, then wire line→filled on hover/active. See [[icon-source-rule]] [[dynamic-weight-icons]] [[component-review-program]].
