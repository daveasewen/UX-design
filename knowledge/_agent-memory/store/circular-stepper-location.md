---
name: circular-stepper-location
description: The circular-dots stepper that collapses to a Step-N-of-M line lives in Tranche-1; the canon dots version is in git history (273d18c~1)
metadata: 
  node_type: memory
  type: reference
  originSessionId: 2dfa173d-e98a-4a20-a372-c4ba279c0769
---

The circular-step stepper (dots, done=check, current=ringed number) that **collapses to a "Step N of M" progress line at narrow widths** — the one Dave remembered and couldn't find:

- **Live in the repo:** inside `knowledge/_proforma/Tranche-1-interactive.html` — classes `.dot` (36px circular markers) + `.stepper-mini`, collapse rule `@container (max-width:520px){ .stepper{display:none;} .stepper-mini{display:block;} }`. It's the T1 *display* stepper (not a standalone "stepper" file — that's why it's hard to find by name).
- **Canon version, git history only:** `Progress-tracker.reference.html` USED to be this circular-dots stepper but commit **`273d18c`** ("Progress-tracker -> canon 9/9: correct dots stepper to segmented track") changed it to a segmented track. Recover the dots version with `git show 273d18c~1:knowledge/snippets/Progress-tracker.reference.html`.

Reconciled candidate merging T1's circular+collapse with T8's interactivity built 2026-07-17 (non-destructive, in outputs as `Stepper-reconciled-2026-07-17.html`) — awaiting Dave's ruling on whether/where to promote. See [[feedback-survey-before-build]].
