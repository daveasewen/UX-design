# Pipeline — UX Design (working)

**Phase:** Define → Develop. **Status:** working (specced for dry-run).

Turns validated requirements into an interaction design: information
architecture, flows, and low/mid-fidelity structure — ready for `ui-design` to
render against the component library.

## Spokes

| # | Spoke | Responsibility | In | Out (contract) |
|---|---|---|---|---|
| 1 | **Framing** | Synthesise requirements (UX/CX research + BA/PO) into a brief + success criteria | `requirements`, `cx_journey?` | `brief` |
| 2 | **IA / structure** | Information architecture, content model, navigation | `brief` | `ia_model` |
| 3 | **Flow designer** | Task flows and states (happy path, edge, error, empty) | `brief`, `ia_model` | `flow_spec` |
| 4 | **UX critic** | Score structure against heuristics + requirements coverage | `flow_spec` | `ux_review` |

## Gates

- **Gate A (HITL):** brief approved by PO/design lead before structure work begins.
- **Craft gate:** UX critic scores IA/flows (coverage, consistency, heuristic alignment). Pass → hand to `ui-design`.
- **Taste gate (HITL):** design lead confirms the approach is worth rendering.

## Knowledge access
- RAG over `knowledge/guidelines/` (patterns, IA conventions).
- Reads `cx-design` experience principles for consistency.
- No component-library detail yet — that begins in `ui-design`.

## Handoff to ui-design
Emits `flow_spec` + approved `brief`. `ui-design` consumes both to generate
component-level designs from canon.

## Backing skills
`design:user-research`, `design:research-synthesis` (upstream), `design:ux-copy`
(coordination). The craft gate uses the same heuristic set as the UI heuristic
spoke (`skills/heuristic-review/`).
