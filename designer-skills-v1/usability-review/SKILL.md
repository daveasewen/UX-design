---
name: usability-review
description: Run an expert usability inspection of a screen or flow against Nielsen's 10 heuristics, producing severity-rated, actionable findings. Use to evaluate interaction quality — distinct from design-system conformance and accessibility.
---

# Usability review (heuristic inspection)

Expert usability inspection against Nielsen & Molich's 10 heuristics. This is the
**craft-of-usability** check — separate from `check-against-design-system`
(conformance) and from accessibility auditing.

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
1. Inspect each screen/flow against all 10 heuristics — one pass per heuristic.
2. For each issue record: the heuristic, a description, the location, and a
   **severity 0–4** (0 = none · 1 = cosmetic · 2 = minor · 3 = major · 4 = catastrophe).
3. Add a concrete recommendation per issue.
4. Summarise: counts by severity; the top issues first.

## Output
`findings` (heuristic · issue · location · severity · recommendation) + a short
summary. **Surface the 3s and 4s first** — those drive the conversation.

*Experimental.*
