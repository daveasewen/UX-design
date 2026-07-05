# ADR-0003 — Knowledge representation chosen per stage (not one store)

**Status:** accepted · **Date:** 2026-05-31

> **AUDIT — DEFERRED 2026-07-05 (Tier A batch 2, Dave). Validation state = `defer`, not vouched.**
> The per-stage hybrid was reasonable for 2026-05-31, but the founding instinct that the *whole*
> design-system corpus (component specs, foundations, tokens, snippets, create.hsbc guidelines) is
> **one interlinked knowledge graph** is being reopened — that cross-entity interlink is modelled
> only *inside* the compliance graph today. Root cause named by Dave: **ingestion was never
> completed** (attempted, curtailed). Spun off as a separate, structured work thread — "unified DS
> KG + ingestion, done right" — with its own audit-grade method. Do not treat this ADR as vouched.
> See `knowledge/_DECISION-AUDIT.md` + `_LIVE-STATE` OPEN.

## Context
The original hypothesis was to ingest all standards and the design system into a
single knowledge graph. Research shows KGs win for relationships/traceability;
vector RAG wins for unstructured semantic; hybrids are the norm.

## Decision
Use a **hybrid keyed to knowledge type**:
- **Component library → component graph** (structured metadata: props, relationships, tokens, anti-patterns). A lightweight KG.
- **Compliance rules → knowledge graph** (rule → component → check → SC → clause) for audit-grade multi-hop reasoning.
- **Tokens → DTCG JSON** with intent descriptions.
- **Guidelines/voice → RAG** over Markdown.
- **Live Figma/code → MCP** at runtime.

## Rationale
A graph earns its curation cost only where relationships and provenance matter —
the component and compliance stores. Elsewhere it is overhead. In a regulated
financial context, the compliance graph's traceability is a real asset.

## Consequence
Ingestion (agency machine) builds the populated stores from real assets; schemas
+ synthetic examples are authored at home so logic is dry-runnable.
