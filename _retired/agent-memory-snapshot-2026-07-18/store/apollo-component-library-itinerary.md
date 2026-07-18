---
name: apollo-component-library-itinerary
description: "The reviewable component build itinerary (124 items) + feasibility verdict; extend-not-restart; P1 slice of 23 is the fundable scope"
metadata:
  node_type: memory
  type: project
---

**Created 2026-07-14** (Dave side-quest: "feasibility of generating a whole new component library using Apollo, all gaps filled, high estimate ~300").

**Deliverables (committed + pushed to repo):**
- `reviews/ITINERARY-2026-07-14-apollo-component-library.html` — Swiss-styled, phase-grouped, live filter (All / Gaps+partial / P1 / Have). Also pinned as desktop artifact `apollo-component-library-itinerary`.
- `reviews/ITINERARY-2026-07-14-apollo-component-library.xlsx` — working finesse tool: 1 row per item (Component, Category, Layer, Status, Priority, Phase, Mine-from, Notes) + Summary tab.

**The numbers (grounded in `knowledge/_COMPONENT-LIBRARY-TARGET.md` + `component-build-plan.html`):** 124 itinerary items = 38 gated + 7 partial + 79 gaps; 23 P1 / 30 P2 / 33 P3; 96 Layer-1 bases + 28 Layer-2 (shells/templates/lock-ups). Per-component variant matrices multiply Layer-1×Layer-2 into the 200–300 catalogue ceiling.

**Feasibility verdict (my recommendation, for Dave to finesse):**
1. **Not bonkers — it's the scoped next step.** The target doc + Swiss build-plan already argued 38→200–300; what was missing was the flat reviewable list. Now built.
2. **EXTEND, don't restart.** A net-new library re-deriving the 38 gated components = weeks re-litigating settled work for zero functional gain. Itinerary defaults to extend framing (Partial = add a variant, not rebuild).
3. **300 is honest but misreads easily.** Only the ~23 P1s move the "engine stops inventing" needle. 300 is variant-multiplied, mostly *composed by Apollo*, not hand-built. Real human build ≈ 50 base gaps. Don't let sponsor read 300 as 300 units of effort.
4. **Sequence to the failure mode, not the alphabet:** prioritise what the fitness tests actually fabricated — amount/currency, charts, data grid, empty state. Weight effort to the **fintech layer** (amount / ledger row / mandate / runway bar) = the real moat generic kits lack.
5. **Caution:** own docs call this "a program, not a side-quest"; it competes with the seaworthiness plan. Don't let it jump ahead of finishing ingestion Phase 1 (the "foundations ahead of finished work" anti-pattern).

**Suggested pilot (unstarted):** run 2–3 P1 gaps through the existing gated pipeline (snippet→meta→gate→`.cn-*`) to get a real cost-per-component number before pitching — recommended: amount/currency input, charts, empty state. See [[review-session-progress]] for the parallel interaction-review track.
