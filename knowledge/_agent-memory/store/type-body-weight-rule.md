---
name: type-body-weight-rule
description: BRAND rule — no light/ultra-light weights on body-size type; min regular(400); regular works in both light+dark
metadata: 
  node_type: memory
  type: project
  originSessionId: 092f2ec3-f158-4442-b33b-7b5302f0d3f6
---

BRAND rule (Dave 2026-07-17, from the composites review): **never use light (350) or ultra-light (250) on
body sizes** (font-5/6/7). Minimum weight on body = **regular (400)**. Regular reads fine in **both** light
and dark, so **body needs no dark-mode step-up**. Light/thin/ultra remain allowed on **display + heading**
sizes (font-00…font-4), where the dark `-V2` step-up applies (light weights go spidery on dark, so they bump).

**Status:** author to double-check; treat as firm-for-now, hypothesis testable. APPLIED to
`knowledge/tokens/_proposals/typography-composites-2026-07-17.json` + `knowledge/canon/type.css`.
Note the source Figma had font-5/default = light(350) — the brand rule OVERRIDES the source file here.

Relates to [[apollo-product-framing]] (`-V2` = dark register), [[accessibility-aspiration]] (regular is also
more legible), and the type work in `knowledge/_proforma/_TYPE-DECISIONS.md`.
