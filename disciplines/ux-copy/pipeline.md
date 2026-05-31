# Pipeline — UX Copy (skeleton)

**Phase:** Develop → Deliver. **Status:** skeleton.

## Purpose
Produce interface copy — microcopy, error messages, empty states, CTAs,
onboarding — that is clear, on-voice, accessible and compliant.

## Proposed spokes
| Spoke | Responsibility | Output contract (TBD) |
|---|---|---|
| Copy generator | Draft copy from component context + voice guidelines | `copy_draft` |
| Voice/clarity critic | Score against voice, reading level, plain-language rules | `copy_review` |
| Compliance checker | Regulated-language + a11y (labels, alt text, error semantics) | `copy_compliance` |

## Gates
- Craft gate: voice + clarity + plain-language conformance (scored).
- HITL: content lead approves regulated/legal-sensitive strings.

## Knowledge access
RAG over voice/tone in `knowledge/guidelines/`; reads component metadata for
context (which strings a component expects). Runs in parallel with `ui-design`
reviews on the same artifact. The `design:ux-copy` skill can back the generator.

## Notes
Accessibility overlap: copy is in scope for WCAG (labels, link text, error
identification). Coordinate with the accessibility spoke to avoid double-judging.
