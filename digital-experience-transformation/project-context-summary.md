# The Apollo — project context summary

*Context fuel for the Digital Experience transformation work. Written 2026-06-29.*
*This file is safe to commit and share — it is a factual summary of an existing project, not a strategy proposal.*

---

## In one paragraph

The UX-design project (internally, **Apollo**) is a working prototype of a **new kind of design system**: not a library of files and documents that humans copy from, but a **governed, AI-driven engine** that takes a project from brief → researched, criteria-bound spec → multiple generated, gate-verified solutions → a human-tuned prototype and developer handoff. Its differentiating idea is simple and important: **judgment is spent once and then enforced automatically.** Senior taste is encoded into a certified component set ("canon"), quality standards are written as **executable checks** ("gates"), and an agentic harness runs the whole design discipline against them. It is the practical engine that makes a Design-Delivery-to-Digital-Experience transformation possible — and the proof that the team can build differentiated capability rather than simply absorb cuts.

## What it is

A **portable, model-agnostic harness** for running design-discipline work as **governed agentic pipelines**. Two layers:

1. **The harness (reusable, discipline-agnostic):** an orchestrator that owns state, routing, checkpoints, retries and error handling — but makes *no* quality judgments. It carries persistent state across runs (canon, memory, checkpoints), a typed-contract system, an explicit error taxonomy, and human-in-the-loop (HITL) gates placed deliberately where automated judgment is unreliable.
2. **The discipline pipelines (pluggable):** thin pipeline definitions for each design discipline — UX research, CX research, UX design, UI design, UX copy, CX design — plus Business Analyst / Product Owner as input providers. They share the harness and differ only in their spokes, contracts and gates. The flow follows a Double Diamond spine (Discover → Define → Develop → Deliver).

Everything is plain Markdown + typed data (JSON Schema contracts, DTCG tokens), versioned in Git, conforming to open agent standards (`AGENTS.md`, Agent Skills / `SKILL.md`, MCP). It runs the same under Claude, other frontier models, or the Apollo runtime without rewrites.

## The core ideas (this is the moat)

These are the principles that make it more than "AI that draws screens." They are also, not coincidentally, the operating principles of a transformed team.

- **Craft is scored; taste is judged.** Two distinct kinds of quality gate. Objective craft (accessibility, contrast, token-fidelity, state-completeness) is *measured and enforced automatically*. Subjective taste (is this the right experience? is it on-brand?) is *handed to a human* at a designed gate. The machine never pretends to have taste.
- **Automate everything *around* the taste call.** The goal is not to remove human judgment but to make it **cheap and rare**: compute the evidence, render the diff, line up the A/B, pre-reject anything that fails an objective gate, and hand a person a ~20-second decision. Each expensive human judgment is spent where it actually matters.
- **Criteria-as-executable-checks.** Borrowed from agentic coding (spec/eval-first development): the success and failure criteria are written *before* any design, as checks the system can run. **The criteria become the gates.** "Verification = enforcement."
- **Gated canon.** Judgment is spent *once* — designing and certifying a component (accessible, on-brand, token-faithful, all states handled) — and then **reused infinitely**. A certified component cannot drift, because the gates that certified it keep biting.
- **Tiered checks.** A few **hard objective gates** that block, many **cheap advisory signals** that annotate, and a *small* set of **true human taste calls**. This prevents the system from rebuilding the slow, subjective review it was meant to kill.

## How a run works (the proven slice)

The highest-impact, fully-specced slice is `ux-design → ui-design → build-&-review → handoff`:

> generate from the component library → **craft gate** (objective, blocking) → parallel **[heuristic review ∥ accessibility ∥ brand]** → **taste gate** (human) → handoff → final approval.

Senior judgment is encoded as the scarce input — a `taste` definition plus two human gates — and everything else is automated around it.

## Current status (as of mid-2026)

- **Proving the loop on one real banking journey** (a payments dashboard / overview) before scaling — a deliberate "minimum viable target," not big-design-up-front.
- A **gated component canon is built**: ~32 components refined to a single high-bar exemplar, with a composition layer (`canon.css`) that lets screens be assembled from certified parts with zero drift.
- The **build-&-review pipeline works**; the other disciplines exist as consistent skeletons ready to instantiate from the same harness.
- **Compliance bar:** engineered to WCAG 2.2 AA; EN 301 549 / WCAG 2.1 AA treated as the legal floor. The WCAG version is a config parameter.
- A parked **horizon-3 vision** notes the same engine could power a *contextual dashboard* at run-time (every element provably compliant, users only ever see what they are entitled to) — evidence the capability creates *new* value, not just efficiency.

## Why this is the engine of the team transformation

A Design Delivery team's traditional value is its capacity to **produce artifacts** by hand. This project demonstrates, in working form, the model that replaces that: the production labour is automated against encoded standards, and human time is redirected to the scarce, high-value work — **defining what "good" means, curating the certified canon, governing the gates, and owning the experience and research.** The Apollo is therefore two things at once: the **tool** that makes the transformed team possible, and the **proof** that this team can build a differentiated capability the rest of the organisation will want to use.

## Pointers (in the UX-design repo)

- `README.md`, `AGENTS.md` — what the project is and how any agent operates in it.
- `docs/architecture.md`, `docs/research-dossier.md` — the two-layer design and its rationale.
- `disciplines/README.md` — the full discipline / process map (the team-shaped view).
- `_STRATEGY-KICKOFF.md` — the product/strategy framing this transformation work sits alongside.
- `knowledge/canon/` — the gated component canon and composition layer.
