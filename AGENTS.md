# AGENTS.md — Promenaut Agentic Design Workflow

> Root operating manual for any agent (Claude, GPT‑5.5, Promenaut runtime) working
> in this repository. Conforms to the open [AGENTS.md](https://agents.md/) format.
> Per-discipline `AGENTS.md` files may override locally; the nearest file wins.

## What this project is

A portable, model-agnostic **harness** for running design-discipline work as
governed agentic pipelines, abstracted from the proven **HDS** editorial
reference architecture. One reusable harness layer; many discipline pipelines.
First working pipeline: **UX/UI design — build & review**.

## Core principles (inherited from HDS)

1. **Workflow, not free-roaming agent.** Predefined, auditable paths with bounded agentic steps. Add complexity only when it demonstrably improves outcomes.
2. **Hub-and-spoke.** A single orchestrator owns state, routing, checkpoints, retries and failure handling — and makes *no* quality judgments.
3. **Single-responsibility spokes.** Each agent does one thing and emits a typed contract.
4. **Craft is scored; taste is judged.** Two distinct gate types with distinct recovery paths.
5. **HITL gates are designed components**, placed where automated judgment is unreliable — not fallbacks.
6. **Typed contracts.** Every spoke I/O validates against a JSON Schema in `contracts/`.
7. **Persistent state across runs.** Canon (knowledge), memory (learning), checkpoints (resumption).
8. **Explicit error taxonomy** (4 types) — see `harness/errors.md`.
9. **Pre-flight policy hooks** fire deterministically before a spoke runs.
10. **Deliberate simplicity**, with evolution paths recorded as ADRs in `docs/decisions/`.

## Repository conventions

- **Source of truth is Git.** No machine-specific or absolute paths in committed files. No model-specific prompt syntax outside clearly-marked adapters.
- **Plain Markdown + typed data.** Specs in Markdown; contracts/schemas in JSON; tokens in DTCG JSON.
- **Capabilities are Skills.** Reusable procedures live in `skills/<name>/SKILL.md` (open Agent Skills format).
- **Live design-system access is via MCP** (Figma Dev Mode MCP + Code Connect), used only where runtime freshness is required.
- **Decisions are ADRs.** One decision per file in `docs/decisions/`.
- **Commits are conventional** (`feat:`, `fix:`, `docs:`, `chore:`).

## Orchestration ownership

**We control orchestration.** The orchestrator spec (`harness/orchestrator.md`)
is self-contained and portable; Promenaut is a *deployment target* we validate
against, not a dependency we inherit logic from. See `docs/decisions/ADR-0001`.

## Two-machine split (important)

- **This/home machine:** author and dry-run logic with **synthetic + public** data. Never assume company assets are present.
- **Agency machine:** ingest **real** design-system, Figma library and React components into `knowledge/`; wire live Figma MCP; re-run against real assets.

## Compliance bar

Build to **WCAG 2.2 AA** (engineering target); **EN 301 549 / WCAG 2.1 AA** is the
current legal floor. WCAG version is a config parameter. See `docs/decisions/ADR-0004`.

## Where to start

1. `docs/research-dossier.md` — why everything is the way it is.
2. `docs/architecture.md` — the harness + pipeline architecture.
3. `harness/` — the reusable layer.
4. `disciplines/ui-design/` and `disciplines/ux-design/` — the working pipeline.

## Definition of done (any spoke)

A spoke is done when: its output validates against its contract; the relevant
gate has passed (or escalated); a checkpoint is written; and any learning is
proposed to memory (not silently committed — see `harness/state/memory.md`).
