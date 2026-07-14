# Orchestrator (the hub)

The discipline-agnostic coordinator. The design-workflow analogue of HDS's
*Managing Editor*. It owns mechanics, never quality.

## Responsibilities

- **State** — holds the run record: current step, status of every spoke, pointers to checkpoints and contracts.
- **Routing** — reads structured spoke outputs (especially gate `pass` fields) and decides the next step. Routing is deterministic given the contracts; the orchestrator does not interpret content.
- **Checkpointing** — writes the output of each completed step before proceeding (`harness/state/checkpoints.md`).
- **Failure handling** — classifies every failure into one of four error types and applies the prescribed recovery (`harness/errors.md`).
- **Retry logic** — bounded retries per error type; escalates to HITL on exhaustion.
- **Pre-flight hooks** — runs deterministic policy/validation hooks *before* a spoke executes.
- **Heartbeat** — records liveness so a stalled run is detectable and resumable.

## Explicitly NOT the orchestrator's job

Quality judgment of any kind. Craft scoring lives in the Critic spoke; taste
judgment lives at the taste gate (the human / `taste.md`). The orchestrator only
reads pass/fail and routes.

## Run lifecycle

```
trigger
  └─► load run config (discipline, inputs, knowledge bindings, WCAG target)
      └─► for each step in the discipline pipeline:
            1. pre-flight hooks (deterministic; may halt → policy error)
            2. assemble curated context for the spoke (narrow, see below)
            3. invoke spoke → receive typed output
            4. validate output against contract
                 ├─ invalid → input/semantic error path
                 └─ valid   → run gate (if any)
            5. gate result
                 ├─ pass     → write checkpoint, advance
                 ├─ fail     → recovery path (retry / upstream / escalate)
                 └─ escalate → HITL gate
            6. propose memory update (not auto-committed)
      └─► terminal: deliver artifact OR escalate OR halt
```

## Context assembly (context engineering)

Each spoke runs with a **narrow, curated context** — only the tokens, components,
rules and prior outputs it needs — not the whole design system. Prefer:

- Query the knowledge layer for *just* the relevant component/compliance nodes.
- Pass upstream results as **compact structured summaries**, not raw dumps.
- Use subagent-style isolation for parallel reviewers so each has a clean window.

This follows Anthropic's context-engineering findings (large token savings, higher
reliability over long runs).

## Portability note

This spec is runtime-agnostic. It can be executed by a thin custom loop, or
mapped onto LangGraph/CrewAI/Apollo as a *swappable engine*. The contracts and
state stores are the invariant; the engine is replaceable. See ADR-0001.

## Parallel dispatch

Where steps are independent (e.g. accessibility + heuristic + brand review), the
orchestrator dispatches them in parallel and joins on all results before the next
gate. Mirrors HDS's Editor∥Essayist parallel pattern.
