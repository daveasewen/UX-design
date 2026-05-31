# Architecture

A two-layer design: a reusable, discipline-agnostic **harness** and pluggable
discipline **pipelines**. Abstracted from the HDS editorial reference
architecture. Full rationale and sources in [`research-dossier.md`](research-dossier.md).

## Layers

```
┌──────────────────────────── HARNESS (reusable) ────────────────────────────┐
│ Orchestrator  · state · routing · checkpoints · retries · 4-type errors     │
│               · pre-flight policy hooks · heartbeat · context assembly       │
│ State stores  · canon (KG: components, compliance) · memory · checkpoints    │
│ HITL gates    · craft (scored) vs taste (judged) · approval gates           │
└──────────────────────────────────────────────────────────────────────────-─┘
        ▲ typed contracts (JSON Schema) ▲
┌──────────────────────── DISCIPLINE PIPELINES ──────────────────────────────┐
│ cx-research · cx-design · ux-research · ux-design* · ui-design* · ux-copy    │
│ inputs: BA, PO                                  (*= working; rest skeleton)  │
└──────────────────────────────────────────────────────────────────────────-─┘
        ▲ knowledge access ▲
   canon query (KG/RAG)  ·  Figma Dev Mode MCP + Code Connect (live)
```

## Invariants vs replaceables

- **Invariant (the value):** the contracts, the state stores, the gate model, the error taxonomy, the knowledge representation. These are portable across machines and models.
- **Replaceable (the engine):** the execution runtime. A thin custom loop today; mappable onto LangGraph/CrewAI/Promenaut. We own orchestration (ADR-0001).

## The working slice

`ux-design` → `ui-design` build-&-review → handoff. Generator → craft gate →
parallel [heuristic ∥ a11y ∥ brand] → taste gate (HITL) → handoff → final
approval. This is where senior judgment is encoded as the scarce input
(`taste.md` + the two human gates).

## Map of the repo
See root `README.md`. Start at the dossier, then this file, then `harness/`,
then `disciplines/ui-design/`.
