# Canon — the knowledge stores (read by spokes)

Canon is the **authoritative knowledge** the pipeline queries: the design system,
tokens, compliance rules, and written guidelines. The model layer *reads* canon;
it does not write it. Canon is built in `knowledge/` (largely on the agency
machine, where the real assets live).

## Representation per knowledge type (the per-stage recommendation)

| Knowledge | Representation | Location | Why |
|---|---|---|---|
| Component library | **Component graph** — structured metadata per component (props, relationships, tokens, anti-patterns) | `knowledge/components/*.meta.json` | Relationships + anti-patterns are what agents can't infer; this is a lightweight knowledge graph |
| Design tokens | DTCG JSON + intent descriptions | `knowledge/tokens/` | Load-bearing primitives; machine-readable + "when to use" |
| Accessibility & compliance | **Compliance graph** — rule → component → check → severity → legal source | `knowledge/compliance/*.json` | Multi-hop reasoning + audit-grade provenance for a regulated context |
| Brand / voice / written guidelines | Structured Markdown for **RAG** | `knowledge/guidelines/` | Unstructured semantic; retrieval suffices, a graph is overkill |
| Live Figma + code state | **MCP at runtime** | (not stored) Figma Dev Mode MCP + Code Connect | Freshness; don't snapshot what changes hourly |

## Access pattern

Spokes query canon for *just* the nodes they need (a component and its
neighbours; the SCs that apply to a component type). They never load the whole
store into context. The orchestrator's context-assembly step enforces this.

## Provenance

Every canon record carries a source pointer (Figma node id, repo path, WCAG SC,
EN 301 549 clause). Findings cite provenance so reviews are auditable.

## Build vs query separation

`knowledge/` contains both the **schemas** (portable, authored here) and, after
the agency-machine ingestion, the **populated stores**. Logic that *queries*
canon is portable and dry-runnable against the synthetic examples committed here.
