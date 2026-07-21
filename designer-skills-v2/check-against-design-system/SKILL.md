---
name: check-against-design-system
description: Review a UI candidate against the design system and flag where it drifts — invented components or variants, hard-coded values instead of tokens, raw type instead of composites, theme leaks, anti-pattern violations, and missing states. Use to check whether a design conforms before it advances.
---

# Check against the design system

Inspect a design or its code against the canon and report where it strays. The
primary things to catch:

- **invented-component** — an element that isn't a defined canon component.
- **invented-variant** — a variant that component doesn't define.
- **hard-coded value** — a raw hex/px where a token should be used.
- **invented-token** — a token name that isn't defined in the store (a
  plausible-looking name that doesn't exist is as risky as an invented component).
- **raw-type** — font-size/weight/line-height set directly instead of a
  `knowledge/canon/type.css` composite (`.t-cm-*` / `.t-ed-*`).
- **theme-leak** — a colour that belongs to another theme on an Apollo Mono
  surface (see `knowledge/tokens/themes/_themes.json` `ownsHexes` — e.g. Legacy
  red `#DB0011` or teal `#00847F`). In Mono, colour is RAG status + data-vis
  only; the only red is `#B92F1E`, never on actions or navigation.
- **invented-icon** — a glyph that isn't in `knowledge/assets/icons/` (check the
  manifest).
- **case-drift** — headings/labels not in sentence case.
- **anti-pattern** — violates the component's `antiPatterns` or
  `relationships.mustNotNeighbour`.
- **missing-state** — an interactive component missing a required state.

## Procedure
1. For each element, confirm the **component exists** in `knowledge/components/`.
2. Confirm the **variant** is defined.
3. Confirm each visual value is a **token binding**, and that the token **exists**
   in `knowledge/tokens/`; confirm text uses a **type composite**.
4. Scan colours against the **theme registry** for leaks; icons against the
   **manifest**; text for **sentence case**.
5. Check `antiPatterns` and `relationships`.
6. Confirm required **states** are covered.

## Output
A list of issues, each with a **severity** (blocker / warning) and a **specific,
actionable fix** — e.g. "bind the background to `color/action/primary`", not "fix
the colours". End with a one-line pass/fail (fail if any blocker).

> Honest note: the **authoritative** checks — real contrast maths, token
> fidelity, accessibility and icon provenance — are executable gates that run in
> CI on this repo. This skill applies the **same rules as guidance** inside your
> editor so you catch drift early; it doesn't replace the CI gate run.

*Experimental.*
