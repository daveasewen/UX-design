---
name: feedback-decisions-as-review-doc
description: "RULE — decision-heavy / material-referring choices go out as a review-template HTML, not AskUserQuestion"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 092f2ec3-f158-4442-b33b-7b5302f0d3f6
---

RULE (Dave, 2026-07-17): when a task involves **decisions that require referring to material** (specimens, tables, options with tradeoffs, anything he needs to look at to rule on), **publish it as a review-template HTML doc** — not the `AskUserQuestion` tool. AskUserQuestion is fine only for **simple** questions with no supporting material to weigh.

**Why:** the review doc is "way easier to provide feedback" — it lays the material and the options side by side, and its overlay lets him pin comments + Export a numbered prompt back. AskUserQuestion can't show the evidence he's deciding against.

**How to apply:**
- Build a Swiss-styled clean HTML in `reviews/` modelled on the `MASTHEAD-MODEL` review (numbered `<h2>` sections, `.decision` blocks with options + a `.rec` recommendation + a "Your call" line, tables/`.evidence`/`.note`/`.flag`).
- Then run `python3 knowledge/_review/_make_review.py <path>` to inject the comment overlay → co-located `*.REVIEW.html`. Present the `.REVIEW.html`.
- Never hand-edit the `.REVIEW.html` — regenerate after each edit to the clean source (per `_PROFORMA-RULES` rule 16: docs ship clean + review).
- Reflect back understanding + give a recommendation per decision (British-understatement, [[feedback-clarify-reflect-back]]); record rulings into the per-pillar decisions ledger once confirmed ([[feedback-capture-review-decisions]]).

Relates to [[review-preview-html]] (present live HTML for review) and [[capture-review-decisions]].
