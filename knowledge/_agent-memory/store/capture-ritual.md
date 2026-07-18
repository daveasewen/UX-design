---
name: capture-ritual
description: Run the 5-step end-of-session capture ritual at the close of every UX-design session that changes project state
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 6edd272b-3c99-4240-bfcd-19803afcb6eb
---

Run `knowledge/_RUNBOOK-capture-ritual.md` at the end of every UX-design session that changed
project state (decisions, rulings, code, docs) — not just when explicitly asked to "wrap up."

**Why:** stood up 2026-07-05 per `_SEAWORTHINESS-PLAN_2026-07-05.md`. The project's recurring
failure mode is "tracking rots silently" (the Sutherland manifest read "blocked" three weeks after
the blocker cleared; a suspected 39-vs-38 compliance-KG drift the same session turned out to be a
miscount). A fixed ritual, run without being asked, is the cheapest defence — waiting for the user to
say "update the docs" is exactly the gap that let tracking rot in the first place.

**How to apply:** the five steps are (1) refresh `_LIVE-STATE.md` (LIVE/DEAD/OPEN/PLANNED-TARGET +
bump "Last refreshed"), (2) refresh `GOOD-MORNING.md` (session-in-one-line/landed/on-desk/queue-next),
(3) update memory files + `MEMORY.md` pointer, (4) record new decision nodes with supersession
discipline (tombstone + propagation gap in the same pass), (5) commit in terminal + Dave pushes via
GitHub Desktop only ([[git-push-method]]). An enforcing script (`_capture_gate.py`) is deferred to
the PM-KG MVP build — until it exists, running the runbook by hand is the gate itself, so don't skip
it because "no script caught me." See [[pm-knowledge-graph-direction]] for the eventual automation.
