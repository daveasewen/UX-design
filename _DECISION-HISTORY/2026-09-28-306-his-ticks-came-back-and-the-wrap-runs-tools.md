# #306 — his ticks came back, and the wrap runs tools

provenance: 306 · 2026-09-28
status: observed

*The why and the how of session #306 (Mon 2026-09-28, 12:55 BST to the wrap at 17:54). The what is in `_HANDOFF-157-his-ticks-came-back-and-the-wrap-runs-tools.md` and in `_LIVE-STATE.md`'s ⏱ LATEST DELTA (spine entry); the rulings are `s306-D1`..`s306-D10` in `knowledge/_rulings.json` (ledger).*

## 1. Checking before asking

The session opened on the 102 parked questions `_HANDOFF-156` put first. His first words were not a tick but a doubt: *"can you check these I think some of them have been superseded"* (12:59). The why: #305 parked the 102 with tripwires, and between #293 and #305 about 150 rulings had landed, so some questions were likely answered already. The how: four Opus readers (lane S) each took a quarter and read every row against the ruling store, giving a verdict with the ruling that answers it. 24 answered, 34 partly, 10 unsure, 34 live. The check page carried the verdicts; he asked for it to be surfaced (14:16), so it went into the review artifact, not a link, because links out of the artifact do not open for him (the #305 lesson).

His answer was broader than the recommendation: close the 24, yes, but keep all 78 others open, including the 34 partly answered. Partly answered is not answered. That is why item 1 for #307 is a question about shape (a sitting page by theme?) and not a plan.

## 2. The red that came from the handoff

The first push went red on one step: KG node titles stale. The cause was in the record, not in the code: `_HANDOFF-156`'s regen serial listed six steps and omitted `gen_kg_titles.py`, which new rulings need. The fix was one regen (`fe243c6c`). The lesson went into a tool rather than a sentence: `_wrap_regen.py` carries the step, so the next handoff cannot drop it by being retyped. This is the *instruction right, cause wrong* shape in reverse: the instruction itself was incomplete, and a copied serial carried the gap forward.

## 3. The redesign, from measurement to ruling

He asked at #305 for a faster wrap with fewer duplicate writes. Lane R measured #303–#305 before proposing anything: 46 to 60 minutes a wrap, about half of it waiting on CI twice; each fact hand-written in about seven places; `_CARRIES.md` at 37 MB because every wrap copies the whole list. Six calls went on one page, each with a recommendation. He took all six and added one worry: *"one thing to check is whether this bloats anything else, we used to have a running tally I think but it bloated the boot"*. Lane U answered it phase by phase, and found the risk sits in phases 3 and 6 (the generated handoff and the seam draft), the same shape as July's tally. Eleven guards were proposed; *"go on both"* adopted them (`s306-D10`) and started the build.

## 4. Phases 1 and 2, and this wrap as their test

Phase 1 turned the scripts each wrap seat wrote into six permanent tools (W1). Phase 2 cut the second CI wait and moved his summary to the push (V). Neither counts as enacted until a real wrap runs on them, so this wrap was the test, and its brief asked for counts: scripts written, move files, rebuilds, minutes to the first push. What the test found is in the wrap report; one small defect worth naming here: the placeholder lines already carry their `> `, and writing `> {{SECTION_SIZES}}` doubled it. A tool that fills a placeholder should say whether it fills a token or a line.

## 5. Where it stands

Resolved: the 24 closed, `W-222`/`W-272` settled, phases 1 and 2 built and run once. Open: the 78, phases 3 to 6, whether the proof counts, the Project-instructions sentence, the chain's warn and the uncounted handoff.
