---
name: feedback-capture-review-decisions
description: "RULE: per-pillar running decision-ledger md capturing review rulings + WHY, so iterative feedback doesn't evaporate; save to repo AND memory"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: daf81930-c8cd-4903-a26d-7f921cdca808
---

When a pillar goes through iterative review rounds (Dave marks up a REVIEW copy → exports pinned
change-requests), maintain a **running decision-ledger `.md` in the repo** capturing each ruling, its
WHY, and how it was enacted — not just the code change. Dave asked for this explicitly (2026-07-16):
"shouldn't we be adding all these corrections and insight to memory or a custom md set, like your own
knowledge graph, so we don't lose track."

**Why:** rapid review iteration generates many small rulings (chevron=gauge-only, marker-fill
exploration, responsive approach, type-scale source, donut label variants…) that override earlier
plans; without a durable log the WHY is lost and superseded decisions get accidentally rebuilt (the
T6-revert failure mode — see [[feedback-reuse-calibration]]). This fits the project's ADR-0007
decision-graph pattern.

**How to apply:** first review round on a pillar → create `_<PILLAR>-DECISIONS.md` next to its KB model
doc (pattern: `knowledge/_proforma/_DATAVIZ-DECISIONS.md`): frontmatter with typed relations, a
"Standing decisions" section (in-force rulings, DV-D## ids), then per-batch pins with ruling · why ·
enactment, and an Open/pending list. Link it from the method doc's `relations:` and update the pillar's
memory to point at it. Keep the repo log as the detailed record; keep memory as the pointer + the few
durable cross-session rulings. Related: [[dataviz-pillar-progress]], [[capture-ritual]].
