# Research Dossier — Agentic Design Workflow for Promenaut

**Version:** 0.1 (planning & research)
**Date:** 2026-05-31
**Author:** Dave (Head of Design System) + Claude
**Status:** For review. No build committed yet — this document precedes implementation.

---

## 0. How to read this document

This is the rigorous research-and-recommendation pass you asked for *before* we
build anything. It does five things:

1. Abstracts your **HDS** pipeline into a reusable, discipline-agnostic harness pattern.
2. Reconciles it against published **best practice** for agentic harnesses.
3. Picks the **portable file standards** that keep everything model-agnostic (Claude → GPT‑5.5 → Promenaut).
4. Surveys **prior art** ("agency-in-a-box" systems) and extracts what to copy and what to avoid.
5. Recommends the **knowledge layer per stage**, the **UX methodology blend**, and the **compliance bar**, then proposes a concrete architecture and repo structure.

Every external claim is sourced in §11.

---

## 1. Context and constraints

**Promenaut** positions itself as *"the operating system for the digital
workforce"* — a harness to manage and deploy agentic workflows, working as an
intimate strategic partner to your company. Our deliverables target their
platform, which is likely to run on Claude.

**Your goal** is twofold and personal: prove the value of design expertise in an
agentic world (designer headcount is forecast to fall over the next ~24 months),
and ship something that impresses both Promenaut and your company. The strategic
move is therefore *not* "automate designers away" but "encode senior design
judgment as the scarce, defensible asset the system depends on." That framing
runs through every recommendation here.

**Hard constraints that shape the architecture:**

| Constraint | Architectural consequence |
|---|---|
| Files must move between home machine, agency machine, and Promenaut | Plain Markdown + structured data, Git as source of truth, no machine paths, no model-specific syntax in committed files |
| Frontier model + real company assets only reachable on the agency machine (Monday) | **Knowledge ingestion** must be cleanly separable from **workflow logic**. We design and dry-run logic here with synthetic/public data; ingestion runs where the assets live |
| Transfer via GitHub (whitelisted) | Repo-shaped deliverables, conventional commits, ADRs for decisions |
| Regulated financial-services context, mixed compliance surface | Adopt the **most stringent** accessibility/compliance bar (see §8) |
| Reusable as a template for other disciplines | Separate a discipline-agnostic *harness* layer from discipline-specific *pipeline* layers |

---

## 2. HDS as a reference architecture (the crown jewel)

Your HDS editorial pipeline is not just a content system — it is a **mature,
transferable harness pattern**. Before importing anyone else's best practice, we
should recognise that HDS already embodies most of it. Abstracting HDS gives us
ten reusable principles:

1. **Hub-and-spoke orchestration.** A *Managing Editor* orchestrator owns pipeline state, routing, checkpoints, retries and failure handling — and makes *no* quality judgments. Spokes are single-responsibility specialist agents.
2. **Single-responsibility agents.** Scout *finds*, Connector *connects*, Editor *assembles* — each does one thing and hands a structured contract downstream.
3. **Separation of craft vs taste gates.** The *Critic* scores craft against defined criteria (a logic gate). The *Chief Editor* judges taste against encoded preferences (`taste.md`). These are distinct failure modes with distinct recovery paths — a genuinely sophisticated distinction most systems miss.
4. **HITL gates as designed components, not fallbacks.** Two human decision points are first-class architecture, placed exactly where automated judgment is unreliable.
5. **Typed input/output contracts.** Every agent emits structured JSON with explicit schemas, enabling deterministic routing (e.g. the orchestrator reads the Critic's `pass` field).
6. **Persistent state across runs.** Three stores: an evolving *Persona Store* (model reads, orchestration writes), a human-owned *taste.md* north star, and *checkpoint files* for partial resumption.
7. **An explicit error taxonomy.** Four types — transient, input-validation, semantic/business-logic, policy-violation — each with one prescribed routing decision. Misclassification (esp. treating malformed input as transient) is called out as the expensive failure.
8. **Pre-flight policy hooks.** Deterministic hooks catch policy violations *before* an agent runs, because "a hook fires deterministically, a prompt instruction may not."
9. **Parallel dispatch where independent.** Editor and Essayist run in parallel once the theme is chosen.
10. **Deliberate simplicity, with recorded evolution paths.** The single-thesis model is a conscious choice; open questions and "next architectural steps" (e.g. splitting Scout from Connector) are documented rather than over-built.

**This dossier's first recommendation: promote these ten principles to a
discipline-agnostic `harness/` layer**, then instantiate each discipline
(UX/UI first) as a `disciplines/<name>/` pipeline that plugs into it. HDS
becomes the editorial *instance*; the design workflow becomes the UX *instance*;
both share the same harness contract.

---

## 3. Agentic harness best practice (and how HDS already aligns)

Anthropic's *Building Effective Agents* is the most authoritative published
guidance and maps almost one-to-one onto HDS.

**Workflows vs agents.** Anthropic distinguishes *workflows* (LLMs orchestrated
through predefined code paths) from *agents* (LLMs that dynamically direct their
own process). Their headline advice: *find the simplest solution; add agentic
complexity only when it demonstrably improves outcomes.* HDS is correctly a
**workflow with bounded agentic steps**, not a free-roaming agent — the right
choice for a regulated, auditable design pipeline.

**The five composable patterns**, and where each belongs in a design pipeline:

| Pattern | What it is | Use in design workflow |
|---|---|---|
| Prompt chaining | Sequential steps, each consuming the last, with gates between | Brief → IA → wireframe → hi-fi: a clean chain with validation gates |
| Routing | Classify input, send to a specialised path | Route by artifact type (new screen vs component variant vs flow) or by risk tier |
| Parallelization (sectioning/voting) | Independent subtasks in parallel; or multiple attempts for confidence | Generate N design directions in parallel; run a11y + heuristic + brand checks as parallel reviewers |
| **Orchestrator-workers** | Central LLM decomposes dynamically, delegates, synthesises | The Managing-Editor equivalent for design when the number of screens/components isn't known up front |
| **Evaluator-optimizer** | Generator + evaluator in a loop against clear criteria | The Critic loop: generate a design, evaluate against the design-system + heuristics, refine |

**Context engineering** is the discipline that replaced prompt engineering:
*curating and maintaining the optimal set of tokens during inference.* Anthropic
reports context editing alone gives a ~29% lift, ~39% combined with a memory
tool, and an 84% token reduction over a 100-turn task. **Subagents with isolated
context windows** that return condensed 1–2k-token summaries outperformed a
single agent by ~90% on Anthropic's internal research eval. Practical
consequence for us: each design spoke should run with a *narrow, curated*
context (just the relevant tokens, components, and rules) and return compact
structured summaries — not drag the whole design system into every call.

**Tool/agent-computer-interface (ACI) design** deserves as much prompt
engineering as the prompts themselves: clear tool docs, examples, poka-yoke
(make mistakes hard, e.g. absolute paths only). This matters acutely for design,
where the "tools" are Figma MCP, the component library, and token lookups.

**Where HDS is ahead of the generic advice:** its craft/taste gate split and its
four-type error taxonomy are more refined than most published examples. Keep them.

---

## 4. Portable file standards — the transferability spine

This is the cleanest part of the answer, and it directly serves your
cross-machine, cross-model requirement. Two open standards have converged in the
last year and both are plain Markdown:

**`AGENTS.md`** — an open, editor-agnostic Markdown format that tells *any*
coding/agent tool the project conventions, build steps, and operating rules.
Introduced by OpenAI in mid-2025, adopted by 60,000+ projects by year end, now
stewarded by the Agentic AI Foundation under the Linux Foundation. Think of it
as "a README for agents." It is model-neutral by design — exactly what we need
for Claude/GPT‑5.5/Promenaut parity.

**Agent Skills / `SKILL.md`** — Anthropic's open spec (released Dec 2025) for
packaging procedural knowledge: a folder with a `SKILL.md` (YAML frontmatter:
`name` + `description`, plus a Markdown body) that can bundle scripts,
references, and templates. By March 2026 ~32 tools read the same `SKILL.md` —
including OpenAI Codex/ChatGPT, Cursor, Gemini CLI, JetBrains Junie. This is the
unit of *reusable capability* and is genuinely portable across models.

**`MCP` (Model Context Protocol)** — the open protocol for giving agents live
access to external tools/data (Figma, the component library, token stores) at
runtime.

**Recommendation:** structure the whole repo around these three.

- One root **`AGENTS.md`** = the operating manual (how the harness runs, conventions, guardrails). Per-discipline `AGENTS.md` files can override locally.
- Each reusable capability (e.g. "audit a component for design-system compliance", "run a heuristic review", "generate a prototype from the library") becomes a **Skill** folder.
- Live design-system access is via **MCP** (Figma Dev Mode MCP + Code Connect), used only where runtime freshness is needed.
- Discipline pipelines and the harness spec are **plain Markdown** with typed JSON/YAML contracts.

This combination is the most widely-adopted, most model-portable option
available, and it is Git-native. It is the answer to "make all our mds and
harness files follow a well-known standard."

---

## 5. Prior art — "agency-in-a-box" and design-specific systems

**Multi-agent frameworks.** The landscape (CrewAI, AutoGen/AG2, LangGraph,
MetaGPT, OpenAI Agents SDK) yields three transferable lessons:

- **MetaGPT** encodes an SOP-driven software *team* and — most relevant to us —
  adds explicit **verifier/reviewer agents**, reported at +15.6% success. This
  validates HDS's Critic/Chief-Editor gates: review agents measurably improve output.
- **CrewAI** models role + goal + backstory per agent. Useful framing for
  defining design-discipline agents, but role-play is cosmetic without typed contracts.
- **LangGraph** treats workflows as stateful directed graphs — the right mental
  model if/when the design pipeline needs branching and resumable state beyond a linear chain.
- **The dominant 2025–26 lesson: simpler loops win.** The best systems converged
  on *fewer tools and better context management*, not elaborate reasoning chains.
  This reinforces Anthropic's "start simple" and your HDS "deliberate simplicity."

**Framework stance:** follow Anthropic's guidance — *don't* marry a heavyweight
framework. Author in portable Markdown/Skills/MCP; if an execution engine is
needed, treat LangGraph/CrewAI as a swappable runtime, not the source of truth.
This protects portability to Promenaut.

**Design-specific prior art (directly usable for your part):**

- **The "agentic design system" pattern** (TDP, May 2026) is the single most
  important external finding for the UX/UI pipeline. Its thesis: *a design
  system built for humans makes agents invent variants.* The fix is a
  machine-readable metadata layer per component capturing **props, relationships,
  tokens, and explicit anti-patterns** ("never two primary buttons side by side";
  "destructive variant requires a confirm step"). Components ship as a folder:
  implementation + `*.meta.json` + tokens + Storybook story + tests. Storybook
  stays the *human* source of truth; metadata becomes the *agent* source of truth.
  Reported ~10x feature throughput once a library is structured this way.
- **Figma MCP + Code Connect** lets agents read variables, tokens, components,
  variants and auto-layout, and map each Figma component to its code counterpart.
  Guidance: variables should describe **intent not implementation**
  (`emphasis`/`default`/`subtle`, not `primary`/`secondary`/`tertiary`), and
  every token needs a one-line "when to use" description.
- **Figma's native design agent** (beta, May 2026) runs on design-tuned models
  and reads your actual component library — relevant as a downstream consumer,
  not a dependency.

---

## 6. Knowledge layer — recommendation *per stage* (your KG hypothesis, tested)

You hypothesised ingesting standards and the design system into a **knowledge
graph**. The honest finding: a KG is *appropriate in part*, and the strongest
design is a **hybrid keyed to each stage**. Published guidance is consistent —
knowledge graphs/GraphRAG win where *relationships, traceability and multi-hop
reasoning* matter (compliance, finance), reducing hallucination ~6% and tokens
~80% in one 2025 study; vector/RAG wins for *unstructured semantic* lookup over
large prose; hybrids are increasingly the norm.

Mapped onto the design pipeline:

| Knowledge type | Best representation | Why |
|---|---|---|
| **Component library** (components, variants, composition rules, anti-patterns) | **Structured metadata = a lightweight knowledge graph** (components as nodes; "lives-inside", "must-not-neighbour", "consumes-token" as edges) | Relationships and anti-patterns are exactly what agents can't infer; this is the §5 agentic-design-system pattern, and it *is* a small KG |
| **Design tokens** | Typed token store (e.g. W3C DTCG JSON) + intent descriptions | Load-bearing primitives; need machine-readable + "when to use" prose |
| **Accessibility & compliance rules** (WCAG SCs, EN 301 549, internal policy) | **Knowledge graph** linking rule → component → check → severity → legal source | Traceability and multi-hop ("which components violate which SC, citing which clause") is precisely the KG strength, and audit-grade provenance matters in finance |
| **Brand/voice/written guidelines** (prose) | **RAG over structured Markdown** | Unstructured semantic content; retrieval is enough, a KG is overkill |
| **Live Figma + code library state** | **MCP at runtime** (Figma Dev Mode MCP + Code Connect) | Freshness; don't snapshot what changes hourly |

**So: KG yes — but scoped to the component graph and the compliance graph, not
the whole corpus.** The component metadata layer and the compliance-rule graph
are where the relationship-reasoning pays for its curation cost. Everything else
is structured Markdown + retrieval, or live MCP. Because the agency machine holds
the real assets, the *ingestion pipeline* that builds these graphs lives in
`knowledge/` and runs there; the *workflow logic* that queries them stays
portable.

---

## 7. UX methodology — recommended blend, mapped to the harness

You asked for a blend rather than one named method. Recommendation: a
**Double-Diamond spine, with Design-Sprint time-boxing inside the diamonds and a
Lean/Agile build-measure-learn loop at the delivery end** — and, critically,
**expert review (heuristic evaluation) and accessibility as designed gates**, the
direct analogue of HDS's Critic/Chief-Editor split.

The Double Diamond (Discover → Define → Develop → Deliver) is the natural fit
because it already alternates divergence/convergence the way HDS's two diamonds
do, and heuristic evaluation slots cleanly into both the Explore (Discover) and
Develop phases per the literature.

Mapping the blend onto agent roles (the UX *instance* of the HDS harness):

| Diamond phase | Agent role(s) | Gate |
|---|---|---|
| Discover (diverge) | Research spoke *(skeleton; not your build)* — synthesises inputs, surfaces problems | — |
| Define (converge) | Framing spoke — produces the brief / problem statement + success criteria | Human Gate: brief approved |
| Develop (diverge) | Generator spoke(s) — produce design directions / prototypes from the component library, in parallel | Craft gate (Critic): design-system + token compliance |
| Develop→Deliver (converge) | **Expert-review spoke** (Nielsen heuristics) + **Accessibility spoke** (WCAG 2.2 / EN 301 549) + **Brand spoke**, run in parallel | Taste gate (you, encoded in `taste.md` + escalation) |
| Deliver | Handoff spoke — dev handoff spec, Code-Connect mapping, prototype | Human Gate: final approval |

This preserves the genuinely valuable HDS insight — **craft is scored, taste is
judged** — and places *you* at the taste gate and the two human gates. That is
the design: senior judgment as the encoded, scarce input the pipeline orbits.

**Your working pipeline (the part to make real first): Build & Review** —
`brief → generate from component library → craft gate → parallel
heuristic+a11y+brand review → taste gate → handoff`. It is the highest-impact
slice (it's where headcount pressure is greatest and where your component
libraries already exist) and it depends on assets you own.

---

## 8. Compliance bar (most stringent, as requested)

**Recommendation: target WCAG 2.2 AA as the engineering bar, while treating
EN 301 549 / WCAG 2.1 AA as the current legal floor, and design the compliance
graph so the target SC version is a parameter.**

Rationale from the research:

- The **European Accessibility Act** has been enforceable since **28 June 2025**, explicitly covers **financial/banking services**, and carries fines up to **€500,000** (country-dependent).
- The harmonised technical standard **EN 301 549** currently incorporates **WCAG 2.1 AA**; it is being updated to fold in **WCAG 2.2**. So 2.1 AA is the legal floor *today*, but 2.2 AA is the forward-looking superset and the safe build target.
- For a regulated financial context with a mixed surface, building to 2.2 AA now avoids rework when EN 301 549 catches up, and gives audit-grade headroom.

The accessibility spoke should therefore enforce 2.2 AA, cite the specific
success criterion and the EN 301 549 clause for each finding (hence the
**compliance knowledge graph** in §6), and tag severity. Make the WCAG version a
config value so the same harness can target 2.1 or 2.2 per client.

---

## 9. Proposed architecture

**Two layers.** A discipline-agnostic **harness** (HDS abstracted) and
discipline-specific **pipelines** that plug into it.

```
HARNESS (reusable)                         DISCIPLINE PIPELINE (e.g. ui-design)
┌─────────────────────────────┐            ┌──────────────────────────────┐
│ Orchestrator                │            │ Spokes (single-responsibility)│
│  · state · routing          │◀──status──▶│  Framing → Generator →        │
│  · checkpoints · retries    │            │  Craft-Critic → [Heuristic ∥  │
│  · error taxonomy (4)       │            │  A11y ∥ Brand] → Handoff      │
│  · pre-flight policy hooks  │            ├──────────────────────────────┤
├─────────────────────────────┤            │ Gates                         │
│ Persistent state            │            │  Craft gate (scored)          │
│  · canon (KG: components,    │            │  Taste gate (you, taste.md)   │
│    compliance) [agency m/c]  │            │  HITL: brief + final approval │
│  · memory / persona store    │            ├──────────────────────────────┤
│  · checkpoints               │            │ Contracts: typed JSON I/O     │
├─────────────────────────────┤            ├──────────────────────────────┤
│ HITL gate framework          │            │ Knowledge access:             │
└─────────────────────────────┘            │  KG query · RAG · Figma MCP   │
                                            └──────────────────────────────┘
```

**Full process skeleton** (specced, not all built now): `ux-design/` + `ui-design/`
(working), with `ux-research/`, `cx-research/`, `cx-design/`, `ux-copy/` as
skeletons — each is a thin pipeline definition over the same harness, with its own
spokes, gates and contracts. This is the "template for other parts of the process"
you wanted.

**What we build first (this/next session, on this machine, with synthetic +
public data):** the `harness/` spec, the `ux-design/` + `ui-design/` pipeline definitions, the
component-metadata + compliance-graph schemas, the root `AGENTS.md`, and 1–2
Skills (e.g. `design-system-compliance-check`, `heuristic-review`) — all
dry-runnable without company assets. **What waits for the agency machine:**
ingesting the real design-system, Figma library and React components into the
knowledge layer, and wiring live Figma MCP.

---

## 10. Recommended repo structure (Git = source of truth)

```
promenaut-design-workflow/
├── README.md
├── AGENTS.md                       # root operating manual (open standard)
├── docs/
│   ├── research-dossier.md         # this file
│   ├── architecture.md
│   └── decisions/                  # ADR-0001-…md, one decision each
├── harness/
│   ├── orchestrator.md
│   ├── errors.md                   # 4-type taxonomy + routing
│   ├── hitl.md                     # gate framework
│   └── state/
│       ├── canon.md                # how the KG/RAG stores are structured
│       ├── memory.md               # persona/learning store + drift audit
│       └── checkpoints.md
├── disciplines/
│   ├── ux-design/                  # WORKING (Define → Develop)
│   │   └── pipeline.md
│   ├── ui-design/                  # WORKING (Develop → Deliver)
│   │   ├── AGENTS.md               # local overrides
│   │   ├── pipeline.md
│   │   ├── spokes.md               # framing, generator, critic, a11y, …
│   │   └── contracts/              # *.schema.json typed I/O
│   ├── ux-research/   (skeleton)
│   ├── cx-research/   (skeleton)
│   ├── cx-design/     (skeleton)
│   ├── ux-copy/       (skeleton)
│   └── inputs/        # BA/PO cross-cutting inputs
├── knowledge/                      # built on the agency machine
│   ├── components/                 # <component>/meta.json (the component KG)
│   ├── tokens/                     # DTCG token store
│   ├── compliance/                 # WCAG/EN301549 rule graph
│   └── guidelines/                 # prose canon for RAG
└── skills/                         # portable SKILL.md folders
    ├── design-system-compliance-check/
    ├── heuristic-review/
    └── prototype-from-library/
```

Conventions: conventional commits; every non-trivial decision recorded as an ADR
in `docs/decisions/`; no absolute or machine-specific paths in committed files;
no model-specific prompt syntax outside clearly-marked adapters.

---

## 11. Open questions and decisions to confirm

Carried forward (some echo HDS's own open questions, which transfer directly):

1. **Knowledge-store update policy** — automatic on review pass, or gated by orchestrator/human review? (HDS's Persona-Store question, reframed.)
2. **Retry budget** before HITL escalation — what N per error type?
3. **`taste.md` authorship** — you author/curate manually, informed by escalation patterns? (Recommended.)
4. **Execution runtime on Promenaut** — do they expose an orchestrator we target, or do we ship a portable runtime? (Affects how thin the orchestrator spec must be.)
5. **Prototype fidelity target** — production-grade React from the real library, or standards-compliant Figma Make as the fallback? (You prefer usable code; confirm per client.)
6. **WCAG target per client** — 2.2 AA default, 2.1 AA where contractually pinned.
7. **How much of `ux-research/`, `cx-research/`, `cx-design/`, `ux-copy/` to skeleton now** vs after the UX pipeline proves the harness.

---

## 12. Recommended next steps

1. **Confirm** the architecture (§9), repo structure (§10), and the open questions (§11).
2. **Scaffold the repo** here with the harness spec, the `ux-design` + `ui-design` pipeline definitions, contracts/schemas, root `AGENTS.md`, and 1–2 Skills — all dry-runnable with synthetic data.
3. **Dry-run** the UX build-&-review pipeline end-to-end on a synthetic component set + public standards to validate the contracts and gates.
4. **On the agency machine (Monday):** ingest the real design system, Figma library and React components into `knowledge/`; wire Figma MCP + Code Connect; re-run the pipeline against real assets.
5. **Hand to Promenaut:** the repo is already in their likely-native (Claude) idiom and conforms to open standards, so handoff is a pull, not a port.

---

## Sources

- [Building effective agents — Anthropic](https://www.anthropic.com/engineering/building-effective-agents)
- [Building Effective AI Agents (resources) — Anthropic](https://resources.anthropic.com/building-effective-ai-agents)
- [Multi-agent research system — Anthropic](https://www.anthropic.com/engineering/multi-agent-research-system)
- [Effective context engineering for AI agents — Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Equipping agents for the real world with Agent Skills — Anthropic](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- [AGENTS.md — open format](https://agents.md/)
- [AGENTS.md emerges as open standard — InfoQ](https://www.infoq.com/news/2025/08/agents-md/)
- [Agent Skills open standard — The New Stack](https://thenewstack.io/agent-skills-anthropics-next-bid-to-define-ai-standards/)
- [anthropics/skills — GitHub](https://github.com/anthropics/skills)
- [Best multi-agent frameworks 2026 (CrewAI/AutoGen/LangGraph)](https://gurusup.com/blog/best-multi-agent-frameworks-2026)
- [CrewAI vs MetaGPT vs AutoGen — Agent Framework Hub](https://www.agentframeworkhub.com/compare/multi/crewai-vs-metagpt-vs-autogen)
- [Agentic design system — The Design Project](https://designproject.io/blog/agentic-design-system/)
- [Design systems and AI: why MCP servers are the unlock — Figma](https://www.figma.com/blog/design-systems-ai-mcp/)
- [Agentic AI, design systems & Figma: a practical guide — UX Collective](https://uxdesign.cc/agentic-ai-design-systems-figma-a-practical-guide-6ab0b681718d)
- [Knowledge graph vs vector RAG — Neo4j](https://neo4j.com/blog/developer/knowledge-graph-vs-vector-rag/)
- [GraphRAG vs vector RAG — Meilisearch](https://www.meilisearch.com/blog/graph-rag-vs-vector-rag)
- [European Accessibility Act & WCAG 2.2 guide — Ergomania](https://ergomania.eu/european-accessibility-act-2025-wcag-guide/)
- [Understanding the EAA and WCAG 2.2 — OneTrust](https://www.onetrust.com/blog/understanding-the-european-accessibility-act-and-wcag-22/)
- [How to conduct a heuristic evaluation — NN/g](https://www.nngroup.com/articles/how-to-conduct-a-heuristic-evaluation/)
- [Double Diamond methodology — Aguayo](https://aguayo.co/en/blog-aguayo-user-experience/double-diamond-methodology-user-experience/)
- [Promenaut](https://www.promenaut.ai/)
