# #187 — The promotion that carried a stale premise (and the lane that stopped at the seam)

provenance: local_6803541e-77c7-4970-8c4a-db3b5c3a3a81 · 2026-08-16
status: observed
spine: `_LIVE-STATE.md` ⏱ LATEST #187 · ledger rows `W-19`–`W-27` in `_state.json`

**Why this session went the way it did.** Dave asked one question — *"are there dependencies on the
order?"* — and the honest answer (read pass 8 before divvying) shaped everything after it. Pass 8's
P2 finding (a retracted claim carried verbatim because "WORDING UNCHANGED" cannot record a
retraction) primed the session to distrust carry-list wording; an hour later the same class surfaced
in a third place: **`s186-D2` promoted pass-7 P1 as Phase 2 work, but the liveness check it demands
had already run at #178** (`s178-D1`(b), GM:430, commit `2d2ff44`). The promotion was made from the
dream-pass backlog's own status line — *"P1 deferred"* — which was true at #177 and never updated.
A ruling can inherit staleness from the surface it was ruled against. `W-25` closed VERIFIED-MOOT
with the receipt, no work re-done.

**The second arc: a re-checker that had to learn what it may not touch.** `W-21` wanted enactment
verdicts on 21 frozen ruling statuses, but `_rulings.json` has exactly one writer and it appends —
so the verdicts live in a sidecar (`_119-sweep-recheck.json`), the B3 pattern. The probe grammar was
wrong twice, and both times the selftest's mutation arm caught it: first a quoted-string capture
matched `"dark"` (co-occurs with every dark-theme rule — cannot fail), then a bare-literal match let
`#fff` survive a simulated enactment of the background hex. The final grammar keys on the record's
own *"still reads X"* clause — probe the exact claimed residue, demote everything else to advisory.
Two dead-ends, both paid for by the mutation arm, which is the argument for mutation arms.

**The stop.** The lane-seam check-in read FILL 144,361 against the 150,929 stop line at the Lane B/C
decision — room 6,568. Lanes B and C were not started; they are store rows, not casualties. The wrap
ran in-window on room-to-WORKING 55,639 vs the 42–49K price.

**Open, stated:** the 2f cs-half question (stratum #186 carried no commit-state line; this wrap
authored `COMMIT STATE #186` from `git log` rather than moving a line that does not exist — where
the cs half canonically lives is a class question, declared on the residual) · `STALE_AFTER_SESSIONS
= 15` is picked, Dave's · `_recheck_119_sweep.py` is in no build route yet.
