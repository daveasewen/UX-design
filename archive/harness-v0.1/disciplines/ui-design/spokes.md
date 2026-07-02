# UI Design — spoke specifications

Each spoke is single-responsibility, reads a narrow curated context, and emits a
typed contract. Mirrors HDS's per-agent rigour.

---

## 1. Generator
**Does:** renders an approved `flow_spec` into a component-level design and a
prototype, using **only** canon components and tokens.
**Reads:** `brief`, `flow_spec`; component graph (relevant nodes only); tokens.
**Emits:** `design_candidate` — component instances, token bindings, states
(default/hover/pressed/disabled/loading/error/empty), and a prototype reference.
**Must not:** invent components/variants; hard-code values; ignore `antiPatterns`.
**Failure modes:** missing component (→ raise gap, do not improvise); ambiguous
flow (→ semantic error upstream to ux-design).

## 2. Critic — craft gate
**Does:** scores `design_candidate` against design-system conformance, token
correctness, anti-pattern violations, state coverage, contract integrity.
**Emits:** `craft_review` = `{ pass: bool, score, violations[], recommendations[] }`.
**Trusted gate:** the orchestrator routes on `pass`; a pass is not re-scored for
craft downstream. Failures route back to the Generator (semantic) or escalate.
**Backed by:** `skills/design-system-compliance-check/`.

## 3. Heuristic reviewer (parallel)
**Does:** evaluates the candidate against **Nielsen's 10 usability heuristics**;
each issue gets a heuristic id + severity (0–4) + recommendation.
**Emits:** `heuristic_review`.
**Backed by:** `skills/heuristic-review/`, `design:design-critique`.

## 4. Accessibility reviewer (parallel)
**Does:** audits against **WCAG 2.2 AA** (version configurable). Each finding
cites the **success criterion**, the **EN 301 549 clause**, the affected
component, and severity. Checks colour contrast, focus order, keyboard operation,
target size, names/roles/values, error identification.
**Emits:** `a11y_review` = `{ findings[], pass: bool, wcag_version }`.
**Hard rule:** any AA failure blocks handoff unless waived at the taste gate with
a recorded reason.
**Backed by:** the compliance graph (`knowledge/compliance/`),
`design:accessibility-review`.

## 5. Brand reviewer (parallel)
**Does:** checks against brand/experience principles — for the first profile, the
**GTB Swiss brand system** (red-as-accent-only, type carries layout, white space
load-bearing, etc.).
**Emits:** `brand_review`.

## 6. Handoff
**Does:** assembles the approved design into a developer handoff spec — layout,
tokens, component props/states, responsive behaviour, interaction notes, edge
cases — plus the **Code Connect mapping** (Figma component → code component) and
the prototype artifact.
**Emits:** `handoff_spec` + prototype (React preferred; Figma Make fallback).
**Backed by:** `design:design-handoff`, Figma MCP + Code Connect.

---

## Join + gates
The three parallel reviews join into one package for the **taste gate** (HITL).
Approval advances to Handoff; redirect routes to the relevant spoke; a recorded
waiver may pass a specific a11y finding. **Gate B** is final approval before ship.
