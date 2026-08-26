---
name: usability-review
description: Run an expert usability inspection of a screen or flow against Nielsen's 10 heuristics, producing severity-rated, actionable findings. Use to evaluate interaction quality — distinct from design-system conformance, from the executable gates, and from accessibility auditing.
---

# Usability review (heuristic inspection)

Expert usability inspection against Nielsen & Molich's 10 heuristics. This is the
**craft-of-usability** check, and it is a different question from the other three:

- `check-with-gates` measures what is mechanically true — contrast, tokens, targets.
- `check-against-design-system` asks whether it conforms to the system.
- **This skill asks whether it actually works for the person using it.** A screen can be
  perfectly conformant and perfectly gated and still be confusing, and no gate will ever
  tell you that.

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

1. Inspect each screen or flow against all 10 heuristics — **one pass per heuristic**.
   Passing once with all ten in mind finds a fraction of what ten focused passes find.
2. For each issue record: the heuristic, the description, the location, and a
   **severity 0–4** — 0 none · 1 cosmetic · 2 minor · 3 major · 4 catastrophe.
3. Add a concrete recommendation per issue.
4. Summarise: counts by severity, worst first.

## What the pack gives you to inspect against

Three things sharpen a heuristic pass on Apollo work, and all three are in this pack.

- **Heuristic 4, consistency** — `showroom/index.json` and `showroom/<slug>.html` show
  how each of the 135 components behaves *as designed*. When a screen's pattern differs
  from the library's, that is a consistency finding with a citation, not an opinion.
- **Known traps** — `antiPatterns` in `knowledge/components/<slug>.meta.json` records
  the ways each component has been misused before. Many are usability findings already
  written down: an accordion whose title changes after the user acts, a lone accordion
  where an expand link belongs.
- **House guidance** — `knowledge/guidelines/` (59 notes) covers calls to action, forms,
  content and tone, platform conventions. `_rules-index.json` indexes **470 rules** out
  of them, each with an id, its source file and a destiny — BLOCKING / ADVISORY / REVIEW
  / TASTE. Search it by keyword and cite the id. Heuristics 5, 9 and 10 land much harder
  when the recommendation quotes the house rule than when it quotes Nielsen.

## Output

`findings` — heuristic · issue · location · severity · recommendation — plus a short
summary. **Surface the 3s and 4s first**: those drive the conversation, and burying them
under a list of cosmetics is the most common way a good review fails to land.

Where a finding is really a system gap rather than a screen defect, say so and route it
to `draft-a-new-pattern` — that's how a usability problem gets fixed once for everybody
instead of once per screen.

*Experimental.*
