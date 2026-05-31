# Disciplines — the full process map

Each discipline is a thin **pipeline** definition over the shared `harness/`. They
share the same orchestrator, error taxonomy, HITL framework and state stores;
they differ in their spokes, contracts and gates.

> **This structure will flex.** The taxonomy below is the starting model, not a
> frozen org chart. Disciplines can be added, split or merged without touching
> the harness — that is the point of the two-layer design.

## The end-to-end flow (Double Diamond spine)

```
        DISCOVER ───────────► DEFINE ──────────► DEVELOP ──────────► DELIVER
        (diverge)            (converge)         (diverge)           (converge)

inputs  ┌─ cx-research ─┐    ┌─ framing ─┐      ┌─ ux-design ─┐     ┌─ handoff ─┐
BA/PO ─►│  ux-research  │──► │  briefs   │ ───► │  ui-design  │ ──► │ prototype │─► ship
        └───────────────┘    └───────────┘      │  ux-copy    │     │  +specs   │
                                                └─────────────┘     └───────────┘
              cx-design informs service/experience across the whole flow
```

## Disciplines

| Discipline | Diamond phase | Status | Folder |
|---|---|---|---|
| **CX research** | Discover | skeleton | `cx-research/` |
| **CX design** | cross-cutting (service/experience) | skeleton | `cx-design/` |
| **UX research** | Discover → Define | skeleton | `ux-research/` |
| **UX design** | Define → Develop | **working** | `ux-design/` |
| **UI design** | Develop → Deliver | **working** | `ui-design/` |
| **UX copy** | Develop → Deliver | skeleton | `ux-copy/` |

## Cross-cutting inputs

| Input | Role | Folder |
|---|---|---|
| **Business Analyst (BA)** | requirements, acceptance criteria, process/data constraints | `inputs/ba-po.md` |
| **Product Owner (PO)** | priorities, scope, success metrics, sign-off authority | `inputs/ba-po.md` |

BA and PO are modelled as **input providers and gate participants**, not full
generative pipelines — they shape briefs and approve gates rather than produce
design artifacts.

## Working slice (build first)

`ux-design` → `ui-design` → build-&-review → handoff is the highest-impact slice
and the one whose assets you own. It is specced in full; the others are
consistent skeletons ready to instantiate.
