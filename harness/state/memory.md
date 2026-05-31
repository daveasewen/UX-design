# Memory — the learning store (read by spokes, proposed by reviews)

The evolving instruction layer. Analogue of HDS's *Persona Store*. Captures
accumulated improvements so the pipeline gets better across runs.

## Read / write rules

- **Read** by spokes at the start of a run (e.g. the generator reads accumulated "house" preferences).
- **Proposed** by review spokes (the Critic suggests refinements).
- **Committed** only via the configured update policy — never silently. Default: gated by orchestrator review or human review (see open question Q1 in the dossier).

## Format

A structured, machine-readable block (the operative instructions) followed by
prose context for human/agent readability. Same dual-format convention as HDS.

## Drift risk

Unbounded self-update causes drift. Mitigations:

- Update policy is gated, not automatic, by default.
- Periodic human audit of the memory store.
- `taste.md` (human-owned, in `harness/hitl.md`) is the north star that memory must not contradict.

## Memory vs taste.md vs canon

| Store | Owner | Writable by | Purpose |
|---|---|---|---|
| **Canon** | system of record | ingestion only | authoritative facts (components, rules, tokens) |
| **Memory** | the pipeline | gated proposals from reviews | learned preferences, refinements |
| **taste.md** | the design lead (human) | human | judgment north star; resolves ties memory can't |
