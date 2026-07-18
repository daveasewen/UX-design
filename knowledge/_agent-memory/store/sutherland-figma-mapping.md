---
name: sutherland-figma-mapping
description: Sutherland = the HSBC React component library; its tokens are being mapped back into the Figma variable library
metadata: 
  node_type: memory
  type: project
  originSessionId: 92c69cca-fca7-4999-a3d7-517fe5550c6c
---

**Sutherland** is the name of the HSBC React component library (the pre-built "full fat" component code referenced in [[promenaut-project-status]]). As of 2026-06-17, the team is **mapping the Sutherland tokens back into the Figma variable library** because the original Figma structure "wasn't quite right." This work is in progress and messy.

Concretely, the Figma variable collections carry **extra modes named after Sutherland** alongside the native HSBC modes (see [[token-collection-architecture]]):
- brand collection: modes `hsbc` and `Sutherland-core` — differ in only **6 of 133** primitives.
- semantic-color collection: modes `light`, `dark`, `Sutherland-light` — `Sutherland-light` differs from `light` in **83 of 258** tokens (the active remap deltas).

**How to apply:** Treat the HSBC modes (`hsbc`, `light`, `dark`, `scale-1/2/3`) as canon for the DTCG store. Treat the `Sutherland-*` modes as the React-library mapping layer — relevant to the eventual Code Connect / `source:"both"` handoff, NOT canon. The 6 brand + 83 semantic Sutherland-vs-HSBC diffs ARE the reconciliation worklist; expect them to change as Dave's team works. Don't assume a Sutherland value is a bug — it may be the intended new mapping. Flag diffs for Dave rather than "fixing" either side.

**Update 2026-07-05 (Dave — recorded to stop re-explaining in chat):** the full picture, stated plainly:
Sutherland is a **React code library that reflects the Common Toolkit**, and **the Figma library we
work from is also Sutherland's working file** (shared source of truth — not two separate artifacts).
So some of our work — **particularly the dark-mode reconciliation — actually contributes back into the
React library**, not just the local KB. **Ultimate desire: build directly using the Sutherland
library.** Portability caveat drives a two-output-mode requirement → see [[output-modes-portability]].

**Update 2026-06-20 (Dave):** Sutherland will **not** have the finesse Dave is adding to the gated component snippets (motion, focus, dark reconciliation, considered geometry). His refined components will **probably be rolled up INTO the Sutherland library**. Sutherland also **hasn't nailed all its tokens** — Dave's token reconciliation / contrast work will probably help **complete** that. So the KB / gated-snippet work has a real upstream destination: it feeds and improves Sutherland, not just the local prototyping fallback. This is the external-outcome path that de-risks the "productivity bubble" worry. See [[pipeline-mental-model]].
