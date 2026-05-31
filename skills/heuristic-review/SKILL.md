---
name: heuristic-review
description: Run an expert usability inspection of a UI design or prototype against Nielsen's 10 usability heuristics, producing severity-rated, actionable findings. Use when evaluating interaction quality during the Develop/Deliver phases, as the expert-review spoke in the UI-design pipeline.
---

# Heuristic review (expert usability inspection)

Encodes Nielsen & Molich's heuristic evaluation as a review spoke. This is the
*craft-of-usability* check, distinct from the design-system check and the
accessibility audit.

## The 10 heuristics
1. Visibility of system status
2. Match between system and the real world
3. User control and freedom
4. Consistency and standards
5. Error prevention
6. Recognition rather than recall
7. Flexibility and efficiency of use
8. Aesthetic and minimalist design
9. Help users recognise, diagnose and recover from errors
10. Help and documentation

## Procedure
1. Inspect each screen/flow against all 10 heuristics, one pass per heuristic.
2. For each issue: record the heuristic id, a description, the location, and a
   **severity (0–4)**: 0 = not a problem, 1 = cosmetic, 2 = minor, 3 = major,
   4 = catastrophe.
3. Add a concrete recommendation per issue.
4. Summarise: counts by severity; the top issues to fix first.

## Output
A `heuristic_review`: `{ findings: [{ heuristic, issue, location, severity, recommendation }], summary }`.

## Notes
- Run in parallel with the accessibility and brand reviews; the orchestrator
  joins all three at the taste gate.
- Severity prioritises the taste-gate conversation — surface 3s and 4s first.
- Can also be invoked standalone in the UX-design craft gate on flows/IA.
