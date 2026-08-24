# #218 build brief — the build-verdict push

Opened under Dave's #218 crank. The record: **75 of 128 `_build_all.py` steps green (#62,
`18c7789`) — 53 steps have NEVER been in a green verdict**, and at this seat the run **aborts at
step [13]** (capture/provenance selftest — `_gen_chain.py --selftest` not green, pre-existing).
A single-process full run is SANDBOX-IMPOSSIBLE (~49s vs the ~45s call kill); CI delivers the
full verdict on push.

Job, in order: (1) diagnose and fix the step-[13] abort at its cause (the gates-wave changes to
`_capture_gate.py` argv are FRESH today — check interaction first). (2) Then work the never-green
53: classify each (broken step / missing env / never-run / genuinely red target), fix what is
mechanical, and produce a MEASURED ledger — step id, verdict, cause class, fixed-or-priced.
⚠ **DO NOT run `_build_all.py` as one process** — any partial run strands the tree in the
documented mid-build intermediate (step 1 rewrites wholesale; healed only by a COMPLETE pass —
docstring lines 5–21). Drive steps INDIVIDUALLY via the runner's per-step entry points if it has
them; if it does not, that gap is finding #1, priced. The known env-dependent red (state-contrast
selftest, missing browser env) is green with the render env set — the working recipe is in
`notes/_briefs/2026-08-24-218-photography-theme-settings-brief.md` § pitfalls.

Fence: no rulings, no constant/band changes, no gate loosening (a red target is fixed at the
TARGET or priced — never by widening the gate), no lane/GM/LS/memory edits, no commit/push.
The gates-wave dirt (6 files, uncommitted) is a co-tenant — do not revert or restage it.

Return: the measured ledger (all 128 steps), step-[13] verdict, fixes as file list, selftest
tails, residuals priced.
