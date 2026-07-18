---
name: generation-mechanism-ideas
description: "Three PARKED ideas (noted, not to be worked on yet) for how generation should relate to the canon — incl. build-time option surfacing for unresolved tokens"
metadata:
  node_type: memory
  type: project
  originSessionId: b6d4d256-65cf-4438-9588-8f44138e09e2
---

Two ideas Dave raised 2026-07-01 and explicitly asked me to **note, not work on yet**. Both are about the generation mechanism (how "build something new" / ideation relates to the canon). Home when picked up = [[fixed-flex-charter]] + canon.

- **Idea 1 — a RULE to embed (governance).** Building something NEW is legitimate, *but inspiration MUST come from the canon rules and the components that already exist* — derive the new thing from the curbs (tokens, type ramp, a11y floor, existing patterns). The anti-pattern to kill: the pipeline trying to **force-fit every screen into the ~32/38 components we have**. So the rule cuts both ways — don't shoehorn into existing parts, AND don't invent free-hand; principled *extension* of the canon. (Sharpens the charter's existing "generate-new = gap-pattern pipeline at gen-time" line.)

- **Idea 2 — an ANGLE to evaluate (architecture).** What if **all ideation runs from pure inference** (let the model roam free, no retrieval constraint), then the output is passed through a **'converter'** that normalises / maps it back onto the canon (tokens, components, curbs)? Dave asked "is this legitimate?" — short answer *yes, plausible*: it inverts today's retrieve-first flow into **generate-then-normalise**, which is a real pattern. Key trade-off = converter fidelity vs. how much creative freedom survives the conversion; also where the a11y/brand floor gets enforced (at convert time). Parked for a proper evaluation.

- **Idea 3 — build-time option surfacing (Dave, 2026-07-02 desk pickup).** When a generation run needs an UNRESOLVED token role (e.g. detects a chart but `data/series-*` has no ruled assignment), don't guess and don't block — **emit the candidates as a build-time choice** (the V7 A/B/C assignments as multi-variant output, Dave picks in situ). Fits the charter's "undecided" dial + the existing multi-variant pipeline. Note only; V7 itself deferred pending renders.

See [[fixed-flex-charter]] [[promenaut-product-vision]] [[procedural-debt-and-method]].
