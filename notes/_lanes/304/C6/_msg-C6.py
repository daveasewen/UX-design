# #304 C6 verify-and-commit seat - wave six message file (written by python, line 1 without an 'after #N' prefix).
msg = """304 wave six: charts fit under reduced motion, dream pass 14's live-state row carried

DECLARED not-a-wrap (#74-D1): a mid-session wave commit by the #304 C6 verify-and-commit seat, not the wrap. The wrap gate's boot-ceiling arm and the NEW-TODAY date zones may read red on this path; declared here, not repaired.

W6 (the reduced-motion fit bug, fixed at its cause): under reduced motion canon.css's reset (.canon * transition-duration .01ms) turns the JS-on width release (.dv-fit-on: the baked 580px -> 100%) into a one-frame width transition, and the fit read the start width, so charts drew about 1.7x on most loads. knowledge/canon/dv-behaviour.js now re-runs the fit, through the same rAF-debounced path as the ONE resize listener, when a transition ends on a chart canvas or on an element that holds one; fitCharts/placeSegs walk with NodeList.forEach to pay for it (Chart-combo 34,768 -> 34,777 of 34,816 code-only bytes). 15 chart/bento snippets and 15 showroom pages regenerated, the behaviour ledger rewritten, the 27 chart-engine receipts re-driven (27/27 FRESH, 0 measurement values changed).

VERIFIED BEFORE COMMIT by the C6 seat, which built none of it (notes/_lanes/304/C6/verify/): cand2-r1 overview under reduced motion 9/10 unfitted loads at HEAD's engine -> 0/10 at W6's, motion 0/10 both; one extra fit pass under reduced motion, none with motion, 0 viewBox writes after 1.5 s (no loop); a transition on an element holding no chart costs 0 passes, one on a chart's holder one debounced pass. Fresh clone at 52049781 with W6's files and _LIVE-STATE.md overlaid: [117] green, survey chunks 31:70 71:100 101:127 differ from W6's survey by 0 steps.

CARRIED BY PRECEDENT, DECLARED: _LIVE-STATE.md carries dream pass 14's runbook-7b row - its Last-refreshed stamp (pass 13 -> 14) and one dated status row in the dream-pass section. Runbook step 7b writes them after the lane commit (ff382c0b), so the ritual never commits them; passes 12 and 13 rode the next commit the same way (96c2f454, 77a77eea). The memento index committed in 52049781 was built over this file, which is why CI's [117] read red; committing it makes the index and its input agree. No other dream-pass file rides: notes/_dream/_MEMORY-GRADES.json and _GRADE-DECISIONS.jsonl stay out (not index inputs; Dave's policy).

Reports: W6 with its lane folder; C5's FINAL copy and transcripts, which closes W-304c5; C6's interim copy with its verify receipts. Store rows minted before the first attempt: W-304w6, W-304c6 (no DOC_ROW_ACK). Regen serial run, every --check FRESH; notes/_RULINGS.html restored to HEAD (date line only).

Left out by name: notes/_dream/_MEMORY-GRADES.json, notes/_dream/_GRADE-DECISIONS.jsonl, notes/_lanes/293/J7-IDEA-jev-selects-over-the-kg.md, notes/_lanes/294/WRAP-MEMORY-HOOK.md, notes/_subreports/2026-09-22-297-A-plain-deck-brain-and-footnotes.md (other seats, declared in _HANDOFF-154); every untracked path outside W6, C5 and C6.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_0115rtjY4mpbeejFbJiuhaEL
"""
open('notes/_lanes/304/C6/_msg-C6.txt', 'w').write(msg)
print(len(msg.splitlines()[0]), 'chars line 1')
