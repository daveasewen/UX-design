# Knowledge (canon) — schemas here, real data on the agency machine

This folder holds the **authoritative knowledge** the pipelines query. Committed
to Git: the **schemas** and **synthetic examples** (safe to author at home).
Added on the **agency machine**: the **populated stores** ingested from the real
design system, Figma library and React components.

## Layout

```
knowledge/
├── components/      # component graph — one *.meta.json per component (a lightweight KG)
│   ├── meta.schema.json
│   └── EXAMPLE-button.meta.json   (synthetic)
├── tokens/          # DTCG-style token store + intent descriptions
│   └── README.md
├── compliance/      # compliance graph — rule → component → check → SC → clause
│   ├── rule.schema.json
│   └── EXAMPLE-contrast-rule.json (synthetic)
└── guidelines/      # prose canon for RAG (brand, voice, patterns)
    └── README.md
```

## Per-stage representation (see `harness/state/canon.md`)

- **Component library → component graph** (structured metadata; relationships + anti-patterns).
- **Tokens → DTCG JSON** with intent descriptions.
- **Compliance → knowledge graph** (audit-grade, multi-hop).
- **Guidelines → RAG over Markdown.**
- **Live Figma/code → MCP at runtime** (not stored here).

## Ingestion (agency machine)

Ingestion scripts read the real assets (Figma via MCP/Code Connect; the React
library via source) and emit records conforming to the schemas here. The
schemas are the contract; the home-machine synthetic examples let the pipeline
dry-run without any real data.
