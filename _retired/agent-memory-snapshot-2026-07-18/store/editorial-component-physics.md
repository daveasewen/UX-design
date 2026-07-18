---
name: editorial-component-physics
description: "Dave's ruling — Editorial and Component type tiers answer to DIFFERENT physics; consequence is that type properties belong on the composites, not on a size-indexed ramp"
metadata: 
  node_type: memory
  type: project
  originSessionId: 0ca1a754-0be4-4e9b-a84b-a28410f8f19e
---

**Dave, 2026-07-18:** *"we have editorial and component styles to take into account, I don't [think]
there is any impact on short labeling to reading speed … this isn't just about reading speed it's about
halation and blooming, so we may have different rules for the text roles."*

The two composite sets (D3, see [[proforma-programme]]) are not just naming conventions — **they answer
to different perceptual mechanics**:

| | EDITORIAL | COMPONENT |
|---|---|---|
| what happens | **read** continuously | **recognised**, not read |
| mechanics | fixations, saccades, word-skipping, word-shape | letter identification at a glance |
| governed by | reading-speed evidence · optical sizing | crowding · halation / bloom |
| ground | almost always ordinary | often reversed on chroma or near-black |

**Why it matters beyond tracking — this is the generalisable part.** Reading-speed research measures
*continuous reading*; it says nothing about a two-word label. Crowding research measures *letter
identification*; that IS what a label is. So the same body of evidence points in **opposite directions**
per tier. Any type rule sourced from literature must first be asked *which tier does this evidence
actually govern?* — I got this wrong once already, using reading-speed evidence to argue against opening
tracking on component labels where it was never in scope.

**The structural consequence (strongest argument on record for the role split being real, not tidy):**
the same 40px wants a different value in each tier — e.g. tracking −0.02em Editorial vs −0.01em
Component. **Size alone cannot express the rule.** Therefore type properties like tracking must live
**ON the composites** (11 Component + 9 Editorial), not as a token ramp indexed by size.

**Independent corroboration:** Frutiger designed *Frutiger* precisely because Univers was *"perfect for
printed books"* but wrong for someone crossing an airport at 5mph — continuous reading vs glance
recognition. **He drew the same line, and put Univers on the Editorial side.** See [[univers-measured-facts]].

Full write-up: `knowledge/_proforma/_TYPE-DECISIONS.md` § T-D1. Related: [[type-body-weight-rule]],
[[wcag-state-contrast]], [[feedback-capture-review-decisions]].
