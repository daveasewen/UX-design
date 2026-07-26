# Provenance cutover — §4.1 fields + gate LIVE from 2026-07-26

**Date:** 2026-07-26 (from `date`)
**Session:** Fable solo — Memento spin-off lane, cold run from its own record.

provenance: local_e607b66f-b9b9-4bb9-ba14-f73bcf09af4b · 2026-07-26
status: ruled · notes/_MEMENTO-DECISIONS.md

---

From today, every new dated file in `notes/` and `_DECISION-HISTORY/` carries two plain
header lines, written mechanically at authoring time (session-id from the session's own
path; date from `date`, never from belief — T-D12):

```
provenance: <session-id> · <YYYY-MM-DD>
status: observed | inferred | ruled | floated | standing
```

Enforced by `_capture_gate.py` (build mode, blocking, selftest wired) in `_build_all.py`.
`ruled` requires a ledger pointer after the value — promotion is Dave's alone. `standing`
(D2's fifth value) = long-lived Dave-owned hypothesis, neither floated-and-forgotten nor
ruled. Memory-side fields are ritual discipline at capture step 3 — deliberately unenforced
(D1a; the store is invisible to gates). Wrap-mode (`--wrap`) is the session-run capture
receipt, not a build step.

**No corpus retrofit** — files dated before today are out of scope (gate the flip, don't
chase history). Exception, lane-internal: the three 2026-07-26 Memento notes were
retrofitted with field lines + dated ruling pointers, bodies untouched.

**Spec + why:** scope v1 §3 (`2026-07-26-memento-dream-pass-scope.md`) · rulings
`notes/_MEMENTO-DECISIONS.md` · runbook `knowledge/_RUNBOOK-capture-ritual.md` (steps 1b/2/3
+ § "The gate").
