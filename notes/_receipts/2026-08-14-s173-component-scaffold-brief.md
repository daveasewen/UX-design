# Receipt — #173, component scaffold sub brief (Opus build sub)

**Date:** 2026-08-14 · **HEAD at authoring:** `e5ab8ee` · **Session:** #173

## What landed

- `_BRIEF-component-scaffold-2026-08-14-v1.md` (repo root, **342 lines**) — the brief a FUTURE build
  sub is handed to take the first new component through the existing route. Nine sections: goal in
  plain prose · verified state of "the scaffold" · first-component recommendation · a 10-step priced
  work plan with the seam each step creates · consequences/pitfalls · the `s172-D3` BOUNDED
  VERIFICATION block near-verbatim · six numbered Dave-gates · the carried DO-NOT-RULE list · the
  build sub's report contract.
- Discharges `residual → #173` item ⑧ *"THE COMPONENT SCAFFOLD SUB BRIEF IS NOT WRITTEN [NEW — 1]"*.

## Key finding — the inherited premise was partly stale

`_PLAN-172-…-v1.md` lane B item 4 reads as though the scaffold must be BUILT. Verified against the
repo: the **procedure** (`knowledge/_RUNBOOK-gated-component.md`, 54 lines), the **meta contract**
(`meta.schema.json` + 76 metas), the **snippet layer** (75 snippets), the **canon generator**, the
**theme cascade** (4 themes), the **showroom** (76 pages) and the **gate chain** (12 routed steps)
all EXIST. What does not exist is a *scaffolder*, a *standard per-theme render harness* (only 7
one-off `_render_*.py` scripts) and any *index/checklist over the metas*. That turns the next window
from an infrastructure build into a content build plus a friction log.

## Also found STALE (flagged in the brief, NOT corrected)

- `knowledge/_COMPONENT-LIBRARY-TARGET.md` — claims "~38 components, ~20 P1 gaps". Reality: 75
  snippets / 76 showroom pages; of its P1 list only **Brand mark / logo** is genuinely absent.
- `reviews/ITINERARY-2026-07-14-apollo-component-library.html` — 86 rows still marked Gap/Partial;
  the P1 half is almost entirely discharged.
- Correcting both is proposed as Gate 5, a separate small lane.

## What is open

- All six Dave-gates (below) are unanswered by design.
- No gate, generator or build step was EXECUTED while authoring — every "the gate does X" statement
  in the brief is read-from-source and is labelled as such. Re-verify at build time.
- The friction log the brief mandates does not exist yet; it is the future build sub's deliverable.

## Proposed Dave-gates

1. Which component goes first? — rec: **Progress bar, determinate, linear + circular**.
2. Build the component or a scaffolder first? — rec: **the component, with a friction log**.
3. Indeterminate variant included? — rec: **determinate-only for v1**.
4. Join a `component-type` family? — rec: **no; queue a `progress-family` as a proposal**.
5. Fix the stale inventory docs? — rec: **yes, separate small lane**.
6. Who builds it and at what price? — rec: **one Opus sub, one window, ~110–130K real tokens**.

## Files touched

- CREATED `_BRIEF-component-scaffold-2026-08-14-v1.md`
- CREATED `notes/_receipts/2026-08-14-s173-component-scaffold-brief.md` (this file)
- Nothing else written. `_build_all.py` NOT run, NOT touched. `_rulings.json`, `GOOD-MORNING.md`,
  `_LIVE-STATE.md`, `_FUTURE-STATE.md` untouched.

## Commit state

**NONE.** No commit, no stage, no push. Files handed up to the conductor.

## machinery

`machinery: 0 instrument / 0 feature` — the deliverable is prose (342 brief lines + this receipt).
No instrument, gate, test or script was built.

## Context gauge at authoring

`🟢 GREEN — ESTIMATE, ~45K real tokens spent in this sub's window at receipt time.` ⚠ ESTIMATE, not a
measurement: `_checkin.py` was not run in this sub, and a block run inside a sub measures the SUB's
transcript, never the conductor's. Retrieval was kept targeted — `GOOD-MORNING.md` (~61K) and
`_LIVE-STATE.md` (~69K) were **never opened**; orientation went through `_memento_search.py`,
`_CHAIN.md` head, and direct reads of the runbooks and generators named in the brief.
