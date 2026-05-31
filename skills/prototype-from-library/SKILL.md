---
name: prototype-from-library
description: Generate a working prototype for an approved UX flow using ONLY the component library and design tokens — never inventing components or variants. Produces production-grade React (preferred) or a standards-compliant Figma Make prototype. Use as the Generator spoke in the UI-design pipeline.
---

# Prototype from library

The **Generator** spoke. Renders an approved `flow_spec` + `brief` into a
component-level design and a working prototype, drawing strictly from canon.

## Hard rules (non-negotiable)
1. Use **only** components and variants defined in `knowledge/components/`. If a
   needed pattern is missing, add it to `open_gaps` and stop — **never improvise**.
2. Bind visual values to **tokens by intent**; never hard-code hex/px.
3. Honour each component's `antiPatterns` and `relationships`.
4. Cover all relevant **states** (default/hover/pressed/focus/disabled/loading/error/empty).
5. Carry **provenance** on every instance.

## Procedure
1. Read `brief` + `flow_spec`. Query canon for the components each screen needs
   (narrow context — just those nodes + their tokens).
2. Compose screens from canon instances; bind tokens; set states.
3. Generate the prototype:
   - **React** (preferred): wire the real library components.
   - **Figma Make** (fallback): standards-compliant frames.
4. Record any missing patterns in `open_gaps`.

## Output
A `design_candidate` (see contract). Passes to the craft gate
(`design-system-compliance-check`).

## Live data
On the agency machine, pull components/variants/tokens live via **Figma Dev Mode
MCP + Code Connect**. At home, use the synthetic `knowledge/` examples.

## Notes
Inventing variants is the documented primary failure of agentic design work —
this skill's whole job is to make that impossible by construction.
