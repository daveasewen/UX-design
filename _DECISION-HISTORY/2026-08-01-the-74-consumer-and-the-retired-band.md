# #74 — the gate gets its consumer, and the % band leaves the code

provenance: local_5d32ceaf (session #74) · 2026-08-01
status: ruled · notes/_MEMENTO-DECISIONS.md § ★ #74

**Spine entry:** `_LIVE-STATE.md` ⏱ LATEST #74 · ledger `notes/_MEMENTO-DECISIONS.md` § ★ #74.

## The arc

Dave opened on fork 3 from #73's list — *"help me understand the implications and why we might
have to move it to wrap-gate"* — and the answer came from the artefacts, not memory: the wrap
gate was honest and consumed by nothing (#71/#72 committed through red), the commit seam is
where a red wrap becomes durable, but three of #73's four commits were legitimate mid-session
work that an unconditional block would have refused. The WARN/`--wrap` split fell out of
holding both truths at once; Dave ruled it in his own words ("the split is the best of both
worlds") and widened the session: fix the whole list before returning to Apollo.

## Findings, with the why

1. **A consumer can be proven without faking a verdict.** The mutation strategy split cleanly:
   an exit-code shim forces the gate's verdict at the real seam (proving the CONSUMER both
   ways), while the gate's own selftest keeps owning verdict honesty. The red-default arm then
   proved itself LIVE unplanned — the mid-session batch commit tripped a genuinely stale
   retrieval index and sailed through as a declared WARN, which is exactly the designed
   behaviour. A planned green + two shimmed arms + one live red = four arms, no fabricated red.
2. **Mid-session the gate is usually GREEN, not red.** The #73 framing ("it would block
   mid-session commits") overstated the friction: mid-session the gate grades the *previous*
   wrap. Red mid-session means inherited debris — visible, declared, and worth seeing.
3. **The premise died twice, and both deaths were cheaper than the fix.** The ~35k baseline
   row was already honestly reconciled at #14 (the planned edit would have been growth); and
   Half-2 was already rebuilt as `_checkin.py` (RULED #52) while the runbook's "currently
   broken — until rebuilt" warning sat stale from #3. The #74 re-probe confirmed
   `read_transcript` still strips tool results (receipt: `[assistant] (called
   mcp__workspace__bash)`, no payload) — so the retirement of the old design is permanent, and
   the correction was to the RECORD, not the instrument.
4. **A dormant enforcement is a live teacher of the wrong unit.** The retired % path's one
   remaining live surface was a wrap NOTE teaching the 45–60% band six sessions after #56
   re-denominated the gauge in real tokens. Retiring the code (D3) deleted ~9.3K chars of
   enforcement while the ruling history stayed in the ledger and runbook — Dave retired the
   code, not the record. The band's purposes (wrap inside the number, moving stop line, marked
   escape hatch) already lived in the token path.
5. **First-match grading needed attribution, not a better regex.** The (h) residual was fixed
   by scoping: a stamp is graded only if its `#N` tag matches the ★ LATEST banner's `**#N**`.
   Keying on the live banner form left the entire fixture corpus untouched — the #60/affe15d
   lesson (a new check must not orphan the fixtures it will be tested against) applied in
   advance for once.

## Dead ends and corrections

- The ops file's first `roll_2f` carried an invented `archive_where` argument — the mover
  refused loudly and nothing was written (the all-or-nothing layer working).
- The LS delta edit initially replaced #73's heading without re-adding it as PRIOR, leaving
  its bullets headless; caught on the re-read against the artefact (the declare-LAST rule
  earning its keep inside its own wrap).

## Resolved state

#74-D1/D2/D3 ruled and enacted (`c27d7b1`, `f8ff234`, `9cde313` + this wrap). Open: the #70
never-wrapped class stays invisible at the commit seam (declared; (f) title check owns it) ·
Dave's Apollo queue unchanged (legend scope, D3, edge types, radios, trigger index).
