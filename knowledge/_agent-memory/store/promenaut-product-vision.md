---
name: promenaut-product-vision
description: "The product-level vision for Promenaut — pipeline tool, pillar priorities, near-term goal order, and the strategic guardrails to hold"
metadata: 
  node_type: memory
  type: project
  originSessionId: b984ef19-8715-4451-a36d-b781e96d0089
---

Promenaut's north star (Dave, 2026-06-20): a tool taking a project **brief → researched, criteria-bound spec → multiple gate-verified solutions → human-tuned prototype**, for **role-agnostic** users (PO, designer, researcher…), **solo or collaborative**, eventually a **web UI over an API**. Differentiated IP = the gated knowledge + the discovery→criteria→enforcement loop (NOT the editor or web shell).

**Pillar priority (1→4):** 1) Discovery→criteria loop · 2) Harness/pipeline architecture · 3) Checks/gates expansion · 4) Screen editor (last; likely a wrapped open-source canvas, not bespoke).
**Near-term goal order:** 1) Prove the method on one real HSBC project · 2) Define the target (strategy work) · 3) Build scaffolding. **Refinement:** define *just enough target to run one real proof* — minimum viable target, not BDUF.

**Strategic guardrails (pushbacks Dave accepted):**
- Define the target by **sequencing**, not scoping all pillars at once. Editor/web-API are the costly, least-differentiated parts → last.
- **Don't "automate taste" — automate everything *around* the taste call** (evidence, diff, A/B, pre-reject fails). Make each human taste-call cheap + rare. LLM-as-aesthetic-judge is unreliable: use auto-judging to *filter*, never to *pick*.
- **Beware gate sprawl** — tier checks: few hard blocking gates, many cheap advisory signals, a small set of true human taste calls. (Ties to [[procedural-debt-and-method]] verification=enforcement.)
- **Multi-solution** = generate N at the *exploration tier* (ungated), run all through objective gates, human+user-testing picks. Constrain to meaningful axes (density/hierarchy/motion), not random.

Full framing + research agenda + discovery-phase seed ideas (Double Diamond gated / compressed Design Sprint / JTBD+assumption-mapping / **spec-eval-first** = favourite): `UX-design/_STRATEGY-KICKOFF.md`. Candidate new checks: states-completeness (top pick), content/tone, PII-masking, responsive/reflow, CX. Builds on [[gated-snippets-and-motion]] + [[promenaut-fitness-test-plan]]. Strategy deep-dive to run in a FRESH chat (this one is context-heavy).
