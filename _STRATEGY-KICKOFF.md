# Promenaut — Strategy kickoff brief
*Seed doc for a fresh chat. Paste this in to start the vision/strategy deep-dive with clean context.*
*Written 2026-06-20 by Claude + Dave, off the back of the gated-KB build (see `knowledge/_NEXT-SESSION.md`).*

---

## How to use this
Open a **new chat**, attach this file, and say "let's work the strategy brief." The current chat is deep
into its context window with token-level KB detail that would anchor the strategy thinking toward the weeds.
Nothing below is settled — it's the framing + the research agenda, deliberately left open for the new session.

## The vision (Dave's words, tightened)
A tool that takes a project from **brief → researched, criteria-bound spec → multiple generated, gate-verified
solutions → human-tuned prototype**, for **many kinds of professional** (PO, designer, researcher, …), used
**solo or collaboratively**, eventually delivered as a **web interface over an API**. The differentiated IP is
the *gated knowledge + the discovery→criteria→enforcement loop*, not the editor or the web shell.

## Decisions locked this session
- **Pillar priority (1→4):** 1) Discovery → criteria loop · 2) Harness / pipeline architecture · 3) Checks/gates expansion · 4) Screen editor (last).
- **Near-term goal order:** 1) Prove the method on a real HSBC project · 2) Define the target (this strategy work) · 3) Build scaffolding.
  - **Refinement (agreed):** define *just enough target to run one real proof* — minimum viable target, not big-design-up-front. The first real project refines the rest.
- **User:** role-agnostic, many professions, solo **and** collaborative. Implications: adaptive intake (asks a PO different questions than a designer); "collaborative" needs shared state/artifacts, so a *slice* of the web/API layer comes earlier than "last" even though the **editor** stays last.

## Three strategic pushbacks (carry these in)
1. **Define the target by *sequencing*, not scoping all pillars at once.** The editor + web/API are the most expensive, least differentiated parts. Build the front of the pipeline + the harness contract first; treat the editor as last and possibly a wrapped open-source canvas, not bespoke.
2. **Don't "automate taste" — automate everything *around* the taste call.** LLM-as-aesthetic-judge is unreliable. Compute the evidence, render the diff, line up the A/B, pre-reject anything failing objective gates, and hand the human a ~20-second decision. Goal: make each taste-call **cheap and rare**, not absent.
3. **Beware gate sprawl.** If a11y + HReview + CX + N more all become *blocking*, you've rebuilt the slow review you're killing. **Tier the checks:** a few hard objective gates (block), many cheap advisory signals (annotate), a *small* set of true human taste calls.

## Multi-solution generation (reconciled with the gated-canon model)
Generate N variants at the **exploration tier (ungated)**, run *all* through the **objective gates** so every
variant is accessible + valid, then human/taste + user testing picks the winner. Constrain variants to
**meaningful axes** (density, hierarchy emphasis, motion character) — not random reshuffles. Use automated
judging to **filter** (kill the broken), never to **pick** (human + users pick).

## Discovery phase — 4 seed directions (to validate against real frameworks in the new chat)
1. **Double Diamond as a gated pipeline** — Discover/Define/Develop/Deliver; the *Define* gate **is** the success/failure criteria contract. `brainstorm` = Discover (divergent), `grill-me` = Define (convergent interrogation).
2. **Compressed Design Sprint** (GV: Map→Sketch→Decide→Prototype→Test) — async, agent-assisted; "Sketch" is where multi-solution generation lives; "Test" consumes the variants.
3. **JTBD + assumption mapping intake** — extract jobs, users, contexts, and *riskiest assumptions*; convert risky assumptions into testable criteria. Research ingestion plugs in here.
4. **Spec/eval-first (most novel, best fit)** — borrow from agentic coding (spec-kit, eval-driven dev): write the **evals — success/failure criteria as executable checks — before any design**. The criteria *become* the gates. Purest extension of the project's "verification = enforcement" principle, now upstream.

## Checks — tiered model + candidate additions
Tiers: **blocking objective gate** / **advisory signal** / **human taste call**. Current blocking gates (6):
contrast ×2, dark-surface, snippet token-fidelity, a11y, coverage, integrity (all bite-tested).
Candidate new checks (decide tier for each):
- **States-completeness** (highest-value, under-asked): does every screen handle empty / loading / error / zero-one-many / overflow / long-string? Very automatable.
- **Content / tone** (UX copy, tone-of-voice) — there's a `ux-copy` skill + `tone-of-voice` guideline to build on.
- **PII / data-masking** (banking-specific) — is sensitive data masked/handled correctly?
- **Responsive / reflow** (1.4.10) + zoom.
- **CX / journey heuristics** — Dave to add a `CX.md`; likely advisory, journey-level.

## Harness (pillar 2) — the open question to crack next
"Get the harness solid" needs a definition. The crux: **what is the unit-of-work and the definition-of-done at
each tier** — token → component → screen → journey → project? The component tier is well-defined (gated snippet
+ gates). The **screen/journey/project tiers are not**. The harness is the contract that says, at each tier,
what goes in, what "done" means (which gates), and how tiers compose. Define this before building anything.

## Research agenda for the new chat (do this properly there, with clean context)
**Design/process frameworks:** Double Diamond (Design Council), Google Ventures Design Sprint, d.school/IDEO
design thinking, Jobs-to-be-Done, assumption/risk mapping, Lean UX, continuous discovery (Teresa Torres).
**AI/agent workflow patterns:** spec-driven development (GitHub spec-kit), eval-driven development, LLM-as-judge
(and its failure modes for aesthetics), multi-agent critique/debate, human-in-the-loop review UX.
**Repos/sites to check:** the `superpowers` repo (`brainstorm`, `grill-me` skills — already cited), spec-kit,
eval frameworks (promptfoo / braintrust style), design-sprint kits, and AI design-tool prior art (v0, Galileo,
etc.) to see what the *editor*/*generation* space already solves so we don't rebuild it.

## Open decisions for Dave (park here, resolve in the new chat)
- What's the **one real HSBC project** we'd use to prove the method? (Picking it shapes the minimum viable target.)
- For the discovery phase: **questionnaire-led, ingestion-led, or hybrid** — and what existing research/data can we ingest (tickets, analytics, prior research)?
- Which candidate checks are **blocking** vs **advisory** in v1?
- How much of the **web/API/collaboration** slice is needed just to support solo+collaborative intake (vs deferring)?

### FLAGGED FROM BUILD CHAT 2026-06-20 — high-res snippet set as a prototyping fallback
**Proposal (Dave):** systematically refine all 32 components to the **Tabs bar** (Tabs = the agreed "solid" exemplar:
interactive, full-state, motion + reduced-motion, complete AT, live theming, token-faithful — see `knowledge/snippets/Tabs.reference.html`).
Method = the **multi-solution loop above**: canon + 3–4 *unconstrained* variants → dual critique → refine → promote winner.
Output = a **high-res interactive snippet set** serving as **one of two prototyping fallbacks while Sutherland is unavailable** (the other = **Figma Make**), and for teams wanting quick-and-dirty prototypes.
**Why it's a strategy call (not just build):** it commits a 32-component program and *positions* this set in the product's prototyping story (lane D). The build chat owns the rubric, the per-component refine loop, and promotion; it should NOT commit the rollout or the fallback positioning unilaterally.
**Decisions needed:** (1) commit the full rollout, or pilot-then-decide? (2) confirm the **two-fallback** model (high-res snippets + Figma Make) and when each is used; (3) does the refined set feed the **prototype lane** (one guided-JTBD lane) or sit beside it? (4) does "promote winner to canon" need a new gate/tier, or stay within the existing exploration→canon two-tier?
**Already in hand:** fitness-test pattern piloted (`knowledge/_FITNESS-TEST-tabs.md`); states-completeness probe measures one rubric dimension across all 32 (`knowledge/_STATES-COMPLETENESS.md`). **Agreed sequence: flag to strategy (this) → rubric + runbook → run the loop.** Build chat is holding phases 2–3 pending this decision.

## Pointers (don't duplicate)
- Current KB state + gates: `knowledge/_NEXT-SESSION.md`, `knowledge/_FINDINGS-INDEX.md`.
- What needs Dave's eyes: `knowledge/_VISUAL-CHECK-QUEUE.md`.
- Method runbooks: `knowledge/_RUNBOOK-gated-component.md`, `knowledge/_RUNBOOK-reconcile-dark-tokens.md`.
