# AGENTS.md — UI Design pipeline (local overrides)

> Inherits the root `AGENTS.md`. This file adds rules specific to UI design and
> the build-&-review slice.

## Mandate

Render approved UX (`flow_spec` + `brief`) into component-level designs and a
working prototype **built from the component library**, then pass it through
parallel expert + accessibility + brand review before dev handoff.

## Non-negotiables

1. **Never invent components or variants.** Use only what canon (`knowledge/components/`) defines. If a needed pattern is missing, raise it — do not improvise. Inventing variants is the primary failure mode of agentic design work.
2. **Tokens, not values.** Reference design tokens by intent (`color.action.primary`), never hard-coded hex/px.
3. **Respect anti-patterns.** Each component's `antiPatterns` are hard constraints, enforced by pre-flight hooks where possible.
4. **Accessibility is a gate, not a lint.** WCAG 2.2 AA findings block handoff unless explicitly waived at the taste gate with a recorded reason.
5. **Cite provenance.** Every design decision points to the component/token/SC it rests on.

## Prototype fidelity

Preference order: (1) production-grade **React** from the real component library;
(2) standards-compliant **Figma Make** prototype as fallback. Set per run config.

## Live access

Use Figma Dev Mode MCP + Code Connect for live component/token/variant data on
the agency machine. On this machine, query the synthetic `knowledge/` examples.
