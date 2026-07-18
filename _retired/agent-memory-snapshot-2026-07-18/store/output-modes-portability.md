---
name: output-modes-portability
description: "Engine must produce TWO output tiers — 'dumber' portable HTML-component prototypes AND build-ready output from a prebuilt library (Sutherland the target); portability = not married to Sutherland, can ingest other libraries; RULED/stated by Dave 2026-07-05"
metadata:
  node_type: memory
  type: project
  originSessionId: 383e10dd-42d4-4e5e-8ef1-0dd5ddbeb367
---

**STATED 2026-07-05 (Dave) — a product-shape requirement for the engine's output.** The engine must be
able to produce at (at least) two fidelity tiers, and the choice must be a dial, not a fork:

1. **"Dumber" prototypes — portable HTML components.** Library-agnostic, no build toolchain required.
   The fast/throwaway/exploration tier; also the portability floor (runs anywhere, no Sutherland).
2. **Build-ready output — from a prebuilt library.** **Sutherland (the HSBC React lib,
   [[sutherland-figma-mapping]]) is the intended target** — "build directly using Sutherland." The
   high-fidelity, ships-to-production tier.

**Portability is the reason this is a requirement, not a nice-to-have.** To keep the *product*
portable (sellable/usable beyond one HSBC stack) the engine must **not be married to Sutherland** — it
should work in the dumber HTML mode, OR **ingest other component libraries**, OR whatever strategy we
land on. Sutherland is *a* build target, not *the* architecture.

**Why it matters / how to apply:** this maps onto the flexing engine's floor/ceiling
([[product-shape-flexing-engine]], ADR-0006) and is a hard case of [[robustness-portability]] (the tool
owns the plumbing; the user never sees the library binding). Treat "output mode / target library" as a
**first-class dial** alongside register ([[register-inference-ramp]]) and the harness modes
([[harness-two-modes]]). Note the two-way Sutherland relationship: our dark-mode work **feeds back into**
Sutherland while Sutherland is also our **build target** — the same artifact is upstream and downstream.
Unaudited decision node (extends ADR-0006); recorded in `_LIVE-STATE` LIVE. Relates
[[pipeline-mental-model]], [[composition-layer-canon-css]] (the HTML/canon path is the dumb-mode
substrate).
