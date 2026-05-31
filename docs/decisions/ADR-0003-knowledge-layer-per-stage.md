# ADR-0003 — Knowledge representation chosen per stage (not one store)

**Status:** accepted · **Date:** 2026-05-31

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
