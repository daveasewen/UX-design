---
name: check-against-design-system
description: Review a UI candidate against the design system and flag where it drifts — invented components or variants, hard-coded values instead of tokens, anti-pattern violations, and missing states. Use to check whether a design conforms before it advances.
---

# Check against the design system

Inspect a design or its code against the canon and report where it strays. The
primary things to catch:

- **invented-component** — an element that isn't a defined canon component.
- **invented-variant** — a variant that component doesn't define.
- **hard-coded value** — a raw hex/px where a token should be used.
- **invented-token** — a token name that isn't defined in the store (a
  plausible-looking name that doesn't exist is as risky as an invented component).
- **anti-pattern** — violates the component's `antiPatterns` or
  `relationships.mustNotNeighbour`.
- **missing-state** — an interactive component missing a required state.

## Procedure
1. For each element, confirm the **component exists** in `knowledge/components/`.
2. Confirm the **variant** is defined.
3. Confirm each visual value is a **token binding**, and that the token **exists**
   in `knowledge/tokens/`.
4. Check `antiPatterns` and `relationships`.
5. Confirm required **states** are covered.

## Output
A list of issues, each with a **severity** (blocker / warning) and a **specific,
actionable fix** — e.g. "bind the background to `color/action/primary`", not "fix
the colours". End with a one-line pass/fail (fail if any blocker).

> Honest note: the **authoritative** checks — real contrast maths, token
> fidelity, accessibility and icon provenance — are executable gates that run in
> CI on this repo. This skill applies the **same rules as guidance** inside your
> editor so you catch drift early; it doesn't replace the CI gate run.

*Experimental.*
