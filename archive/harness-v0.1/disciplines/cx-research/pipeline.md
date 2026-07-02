# Pipeline — CX Research (skeleton)

**Phase:** Discover. **Status:** skeleton — structure defined, spokes not built.

## Purpose
Understand the end-to-end customer experience across touchpoints and channels;
surface pain points, moments of truth, and opportunities that frame downstream
design work.

## Proposed spokes
| Spoke | Responsibility | Output contract (TBD) |
|---|---|---|
| Harvester | Gather inputs (support tickets, NPS/CSAT, interviews, analytics) | `cx_evidence` |
| Synthesiser | Cluster evidence into themes, segments, journey stages | `cx_themes` |
| Journey mapper | Produce a service/journey map with pain points + opportunities | `cx_journey` |

## Gates
- Craft gate: evidence traceability + theme integrity (scored).
- HITL: research lead validates synthesis before it informs briefs.

## Knowledge access
RAG over `knowledge/guidelines/` (research norms) + project evidence corpus.

## Notes
Consumes BA/PO context. Feeds `ux-research` and `cx-design`. Build after the UX/UI
slice proves the harness.
