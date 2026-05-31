# Pipeline — UX Research (skeleton)

**Phase:** Discover → Define. **Status:** skeleton.

## Purpose
Understand users, tasks and contexts for a specific product/feature; turn
evidence into validated problem statements and design requirements.

## Proposed spokes
| Spoke | Responsibility | Output contract (TBD) |
|---|---|---|
| Study planner | Choose method, write protocol / discussion guide | `research_plan` |
| Evidence synthesiser | Theme transcripts, surveys, usability findings | `research_themes` |
| Requirements framer | Convert insights into prioritised requirements | `ux_requirements` |

## Gates
- Craft gate: method fit + evidence traceability (scored).
- HITL: research lead validates insights; PO confirms requirements.

## Knowledge access
RAG over research norms in `knowledge/guidelines/`; project evidence corpus.

## Notes
Directly upstream of `ux-design` (its requirements seed the framing spoke). The
existing `design:user-research` and `design:research-synthesis` skills can back
these spokes.
