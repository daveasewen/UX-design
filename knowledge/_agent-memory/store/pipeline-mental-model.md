---
name: pipeline-mental-model
description: "The shared 'one production line' frame for Promenaut — 4 stations, what's built vs not, the criteria-spine, and the walk-one-screen-by-hand proof direction"
metadata: 
  node_type: memory
  type: project
  originSessionId: f4c8b9bd-ad23-430f-8fe1-c7b8c6940507
---

Agreed framing (2026-06-20) for getting Promenaut back on track after divergent sprawl. The whole goal is **ONE pipeline**, not two projects: ingestion / scoping → standards-compliant hi-res prototypes. It only *felt* like two because the ends were built at different times under different names (build-chat vs strategy-chat).

**Production-line metaphor (the shared language now):**
- ① Order desk = scoping → criteria (requirements / assumptions / success criteria). The frontier; being designed.
- ② Moulding machines = generation. Build *materials* = the gated snippets now; **Sutherland React components later** (only the materials swap). Figma Make is a personal hand-tool (Dave-only access, NOT deployable at the bank) → final product = a model call behind the harness API, bound to canon.
- ③ QA + rulebook = the compliance gates / KB. **BUILT — the real asset.** "Verification = enforcement": gates withhold "done."
- ④ Finished product = the hi-res, standards-compliant prototype.
- Conveyor / foreman between stations = the **harness**. Barely built (untouched stubs since 31 May).

**The spine (key insight):** the spec written at ① *is* the rule enforced at ③ — same criteria, both ends. That continuity is what makes it one pipeline, not two.

**Genesis (why the snippets exist):** started building via AI inference over canon + meta → realised prototypes need a **Sutherland-independent fallback** → built hi-res, standards-compliant gated snippets as the materials → then realised the *input* matters as much → started designing the context-prep front-end (①).

**Direction:** prove the line by **walking ONE real screen end-to-end by hand** (Dave = the conveyor). Doing it by hand is how you spec the harness — each handoff is a future API contract. Runbook + checklist: `UX-design/RUNBOOK-end-to-end-proof.md` (worked example = "review & confirm a payment"). Success = the gate catches **≥1 real thing a human would've missed** (first signal from OUTSIDE the system). Stations ① and ③ are durable across the Sutherland swap. Links: [[promenaut-product-vision]], [[sutherland-figma-mapping]], [[procedural-debt-and-method]].

**Refinement 2026-06-21 (Dave) — after the A/B vs Figma Make (`runs/proof-002`):** The gates work, but the token-fidelity diff (teal #00847F vs generic green) is **too subtle for a demo**. Course-correct:
- **Don't build a bespoke composer to "beat Make."** Once Make is approved in the bank and ingests the proven (Sutherland) component library, it'll compose well — that'd be its first task. Generation is commodity. The IP is **components + criteria/gates**, and prototyping **in the absence of Make** (no procurement wait). The demo is NOT "mine vs Make"; it's "high-res compliant prototyping you can use today, in-house."
- **Demo goal = a dramatic VISUAL:** generate **high-res, component-compliant prototypes from inputs**. Gates are the quiet quality layer underneath, not the show. (Gate 2/2.1 stay as internal infra in `runs/proof-001`+`proof-002`.)
- **Next focus = the snippet-refinement program:** refine the 32 components to the **Tabs-bar exemplar standard** (interactive · full-state · motion + reduced-motion · complete AT · live theming · token-faithful) → rubric + runbook → run the loop (canon + 3–4 variants → dual critique → promote winner). These refined snippets ARE the prototyping material pre-Make and the finesse that feeds Sutherland. See [[gated-snippets-and-motion]].
