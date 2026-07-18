---
name: feedback-survey-before-build
description: "RULE: before building ANY component, survey knowledge/snippets/ + components/*.meta.json + existing tranches; declare mine-vs-fresh per component"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 2dfa173d-e98a-4a20-a372-c4ba279c0769
---

RULE (2026-07-17, from a real miss): before building any component, **survey what already exists in the repo** — `knowledge/snippets/*.reference.html`, `knowledge/components/*.meta.json`, and the existing `_proforma/Tranche-*.html` — and declare per component whether I'm *mining* an existing one or *building fresh*. Grep by pattern name AND by class/behaviour.

**Why:** in T8 (nav tail) I rebuilt **Tab-bar** and **Stepper** from scratch — both already existed. `Tab-bar.reference.html` + `tab-bar.meta.json` already had BOTH a standard bar AND the exact "pills / floating" variant Dave later sent me from Figma (Menu-as-separate-island, sliding-pill, inverting selected). The circular Stepper with responsive collapse-to-"Step N of M" already lived in `Tranche-1-interactive.html` (see [[circular-stepper-location]]). I built from the nav-catalog's "build order" (which framed them as gaps) without checking the canon inventory. Dave caught it.

**Key clarification (Dave 2026-07-17):** *"pro-forma" is just a descriptive name for **Apollo mono** — same thing.* So the gated snippets and the pro-forma tranches are ONE library, not a mono-vs-brand split. Duplicate components in it are genuine duplicates to reconcile, not intended re-expressions. Don't treat tranches as a separate greenfield surface.

**How to apply:** sharpens [[feedback-reuse-calibration]] (ask what Dave valued before mine-vs-fresh) with a concrete first step — the inventory grep is mandatory pre-work, not optional. When a duplicate is found, reconcile into ONE component (non-destructively, new file) and let Dave rule on promotion.
