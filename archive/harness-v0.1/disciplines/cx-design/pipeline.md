# Pipeline — CX Design (skeleton)

**Phase:** cross-cutting (service & experience). **Status:** skeleton.

## Purpose
Design the end-to-end service and experience — orchestration across touchpoints,
channels and back-stage processes — within which UX/UI artifacts live.

## Proposed spokes
| Spoke | Responsibility | Output contract (TBD) |
|---|---|---|
| Service blueprinter | Map front-stage / back-stage / support processes | `service_blueprint` |
| Experience architect | Define experience principles + channel strategy | `experience_principles` |
| Opportunity prioritiser | Rank interventions by value/effort/risk | `cx_priorities` |

## Gates
- Craft gate: blueprint completeness + consistency (scored).
- HITL: experience lead + PO sign-off on priorities.

## Knowledge access
RAG over guidelines; reads `cx-research` outputs; informs all downstream design.

## Notes
Cross-cutting: its principles are inputs to `ux-design`/`ui-design` gates (e.g.
brand/experience consistency checks).
