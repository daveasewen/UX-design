---
name: code-binding-hub-spoke
description: "How design components map to code libraries — hub-and-spoke; Figma node ID is the only identity, names are per-namespace"
metadata: 
  node_type: memory
  type: project
  originSessionId: 4c1b6f21-694d-42b1-81a9-55ae524d5ef0
---

LOCKED 2026-06-22 (Dave): component/variant naming and design→code mapping use a **hub-and-spoke** model. There is **no single "formal name."**

- **Hub** = the Figma node ID (`provenance.figma_node`) — the only library-independent identity; never renamed; everything reconciles through it.
- **Display name** = `$displayName`/`$aliases` per variant — ours, human-facing, stable across all libraries (e.g. "Link card").
- **Figma name** = the variant's `name` (e.g. `basic`) — authoritative for the Figma namespace only.
- **Each code library = a spoke** under a meta's `codeBindings` map, keyed by library id (`sutherland-react`, …); records that library's own component + variant→prop names, which MAY differ.

**Why:** one design component feeds many code libraries built by different people with different conventions; Code Connect binds by node ID, not by name, so names can diverge safely — but only if we map them through the node instead of guessing or normalising. This map is the migration-safety / cross-library Rosetta stone.

**How to apply:** never bind logic/gates/Code Connect on a display name; never normalise names across libraries; never guess a code name (populate spokes from `get_code_connect_map`, tag unverified with `$status`). Procedure = `knowledge/_RUNBOOK-onboard-code-library.md`. Contract = `codeBindings` field in `components/meta.schema.json`. First spoke = `components/cards.meta.json` (sutherland-react, unverified — Sutherland names not inspectable yet, see [[sutherland-figma-mapping]]). Relates to [[promenaut-discovery-decisions]] and [[token-collection-architecture]].
