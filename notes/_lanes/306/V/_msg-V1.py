# #306 lane V - commit 1 message (python-written, no T3 prefix on line 1).
msg = """306 V: s306-D10 inscribed (the eleven limits adopted, each by its phase); phase 2 built - _ci_readback.py, one CI wait, the CI-owed arm

DECLARED not-a-wrap (#74-D1): #306 lane V, a mid-session commit.

Dave, chat #306, Mon 2026-09-28 16:58 BST, verbatim: "go on both" - to the conductor's "1. Adopt the proposed limits into the design? ..." and "2. Build phases 1 and 2 now ..." (both quoted in notes/_lanes/306/V/DAVE-WORDS-2026-09-28-1658.md).

- s306-D10 inscribed via _inscribe_ruling.py, dry run first, reconstruction proof passed (711 -> 712), status ruled: all eleven limits of notes/_subreports/2026-09-28-306-U-rulings-and-bloat.md section 3, read from the report, each named with its phase (2: limit 8; 3: 2, 6, 7, 11; 4: 9; 5: 10; 6: 1, 3, 4, 5).
- Phase 2 (s306-D7, stays ruled until tonight's wrap proves it): knowledge/_ci_readback.py (new; --sha, --owed, --poll, --selftest; a short run summary per sha, blocking lines parsed from a red job's log, never the log; token from the credential helper, never printed, never sent to the log redirect host). Its selftest is _build_all.py step 155 (ABORT route row, appended last; no step number moves).
- knowledge/_RUNBOOK-capture-ritual.md by addition: THE ORDER AFTER THE COMMIT - push, one CI wait, the summary to Dave, the 5b addendum with its CI owed line, the 5b pushed without waiting, 4c last, the next opener reads the owed CI. The old second wait written struck. knowledge/_RUNBOOK-git-commit.md step 5: the one timing exception to s203-D1, by addition.
- knowledge/_capture_gate.py: ci_owed_check, wrap mode, BLOCKING, from _HANDOFF-157 on; 9 selftest bites (new order passes, the old failure class fails). No existing arm required the second CI read.
- knowledge/_state.json by addition: W-305wr gains the 16:58 paragraph (phases 1 and 2 scheduled; stays open); W-306v born closed (s305-D40).
- Selftests: _ci_readback 16 bites PASS; _capture_gate --selftest rc 0; _build_all --selftest PASS over 155 steps; _inscribe_ruling --selftest green; _state.py rc 0; wrap gate 0 fail. Regen serial in order, gen_kg_titles.py --write included; every --check fresh.
- Held: notes/_lanes/306/V/backup/, and the other-seat tails already dirty before this lane (_REHEARSAL-LOG.jsonl, notes/_dream/*, the #293/#294/#297/#304/#305 leftovers).

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01KwUXkCvEuSmYAjrxYbPDh9
"""
open('notes/_lanes/306/V/_msg-V1.txt', 'w').write(msg)
print(len(msg.splitlines()[0]), 'chars line 1')
