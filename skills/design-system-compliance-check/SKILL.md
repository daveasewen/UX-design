---
name: design-system-compliance-check
description: Score a UI design candidate against the design-system canon — flag invented components or variants, hard-coded values instead of tokens, anti-pattern violations, and missing states. Use when reviewing whether a generated design conforms to the component library before it advances. Backs the UI-design Critic / craft gate.
---

# Design-system compliance check

Acts as the **craft gate**. Deterministic where possible; the goal is to catch
the primary failure mode of agentic design — *inventing* components and variants.

## Inputs
- A `design_candidate` (see `disciplines/ui-design/contracts/design_candidate.schema.json`).
- The component graph (`knowledge/components/*.meta.json`) and tokens.

## Procedure
1. For each component instance, confirm `component` **exists** in canon. If not → violation `invented-component` (severity blocker).
2. Confirm `variant` is a defined variant. If not → `invented-variant` (blocker).
3. Confirm every visual value is a **token binding**, not a literal hex/px → else `hardcoded-value`.
4. Check the instance against the component's `antiPatterns` and `relationships.mustNotNeighbour` → `anti-pattern`.
5. Confirm required `states` are covered for interactive components → `missing-state`.
6. Validate the candidate against its JSON Schema → `contract` violation on failure.

## Output
A `craft_review` (see contract): `{ pass, score, violations[], recommendations[] }`.
`pass` is **false** if any `blocker` violation exists.

## Notes
- Trusted gate: a pass is not re-scored for craft downstream.
- Recommendations should be specific and actionable ("bind background to
  `color.action.primary`", not "fix colours").
- This is the design analogue of HDS's Critic.
