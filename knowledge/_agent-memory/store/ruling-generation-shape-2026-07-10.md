---
name: ruling-generation-shape-2026-07-10
description: Dave's stance after the deep-analysis report — rule-tuning + inference tiering leads; double-pass is a component, not the architecture
type: feedback
---
**Dave, 2026-07-10, responding to the deep-analysis report's H2-favoured framing:** the double pass was "not all that successful" in his eyes — it produced interesting insights and data, but is an interesting hypothesis, not the answer. His direction: **tuning the rules and tiering the inference is the way forward**, with more experimenting, and **a double pass forming PART of the process** (a stage, not the shape). Future state: **strict mode with a full component suite for the "factory"** (floor/churn work) will be great — though "arguably we could create this with less infrastructure."

Why: the restyle's earlier "pretty happy" reading overstated his verdict — his considered view is lukewarm on the two-pass artifact itself. He is the arbiter (derivation-governance: promotion/judgment = Dave only); the report's H2/H3 lean is analysis input, not a ruling.

How to apply: (1) don't present generate-then-normalise as the settled target shape — present it as one arm of the experiment; (2) the R1 controlled comparison should now have THREE arms: governed single-pass as-is · rule-tuned/tier-tuned single-pass (Dave's lead hypothesis) · two-pass — same contract, rendered, blind-judged; (3) factory/strict mode is affirmed as a product end-state — provenance-perfect single-pass IS the product there; the open question is only the ceiling/novel end; (4) keep infrastructure lean (his "less infrastructure" instinct aligns with report R6/R7). Supersedes the report §07's two-pass-first framing where they conflict.
