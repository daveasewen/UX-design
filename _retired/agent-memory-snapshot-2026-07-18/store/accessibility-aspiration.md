---
name: accessibility-aspiration
description: "FOUNDATIONAL (Dave, 07-05): HSBC's aspiration is to be the most digitally accessible bank in the world — the compliance bar is set to LEAD not comply; WCAG 2.2 AA is the floor of that aspiration, not its ceiling; expected to ratchet upward"
metadata: 
  node_type: memory
  type: project
  originSessionId: bc7111a5-79d4-40ca-8ab0-04bd883a3e1d
---

**FOUNDATIONAL DRIVER (Dave, 2026-07-05, decision audit).** HSBC's aspiration is to be **the most
digitally accessible bank in the world.** This is the *primary* reason for the accessibility bar —
not fine-avoidance. The bar is set to **lead, not merely comply.**

**How to apply:** WCAG 2.2 AA (`ADR-0004`) is the **floor of the aspiration, not its ceiling** — the
engineering target sits above the legal minimum by design and is expected to **ratchet upward over
time** (AAA where feasible, WCAG 3.0 readiness). Treat the EAA / EN 301 549 legal floor as the
backstop *beneath* the aspiration, never as the goal. When judging a11y trade-offs, "is this the most
accessible we can be?" outranks "does this clear the legal minimum?". Recorded in `ADR-0004`
rationale (amended in the 07-05 audit). Relates to [[wcag-state-contrast]] and the a11y gate.
