# #307 — the 78 were answered, and the picture page waits

provenance: 307 · 2026-09-28
status: observed

*The why and the how of session #307 (Mon 2026-09-28, 19:07 BST to the wrap at 22:27). The what is in `_HANDOFF-158-the-78-were-answered-and-the-picture-page-waits.md` and in `_LIVE-STATE.md`'s ⏱ LATEST DELTA (spine entry); the rulings are `s307-D1`..`s307-D78` in `knowledge/_rulings.json` (ledger), and the two stamps on `s306-D4` and `s306-D7`.*

## 1. Closing the proof before opening the next job

`_HANDOFF-157` put the 78 reopened questions first. He did not start there. His 19:58 message put the wrap redesign's first two phases ahead of them: *"Before the 78, close out the wrap redesign's first two phases properly. Be precise; don't round the claim."* The why is in his item 1: phase 2 made the next opener responsible for the follow-up commit's CI, so phase 2 is only half proven until an opener has done that read. The #307 opener had (run `36458753402`, green), which made it the first real proof.

The how was to fix the two things the #306 wrap had done by hand in the tools themselves, each with a selftest bite, rather than write the workaround into the runbook again: the titles step now lives inside `_wrap_regen.py` as step 0, and the placeholder fold lives inside `_wrap_ops.py`. His item 3 corrected the target rather than the result: the 5b follow-up needs its own rebuild because its line feeds `_CHAIN.md`, so "1 rebuild" became "1 per commit" by addition wherever it was written. His item 4 corrected a word: the opener had called the #306 wrap "last night", when it ran the same evening. Only then were the two rulings stamped (`4d647958`).

## 2. The 78, by hand

"okay the 78" (20:38) was the answer to #306's question about shape. Lane A built one sitting page grouped by theme, quickest first, with a recommendation on every card and lane S's verdicts from #306 carried onto them. He answered all 78 by hand in about 25 minutes (20:53 to 21:18) and took the recommendation on 76. The two he did not take are the ones where he wanted to look rather than rule: W-229, kept open with his note *"I want to check this visually"*, and W-151, *"Show me the five and the reasons"*.

Lane B turned the export into the record without building anything: 78 rulings in page order, each quoting his click and the card's question verbatim; 28 closes, 3 parks, and 46 answers that became 49 live work rows, each with its own closing condition. The 30 whose whole effect was the record change were stamped enacted in a second commit. That kept the rule that a ruling is enacted only when its effect exists.

## 3. Drawing what he asked to see

His answers asked, five times, to be shown something before he rules. Lane C drew each one on the real parts, light and dark, and found two things on the way: a card-level theme attribute brings back the light page ground under a dark body, and the today-and-chosen ring drawn in the page colour cannot be seen as a ring. The second came with a one-rule proposal, drawn as a mutation and kept out of canon. Lane E answered his cold-start question with one blind run on the current pack: 3/3/2/2, with one authored bug that a single look in a browser would have caught. Lane D took the 18 quick items and closed only what an existing ruling covered, leaving six questions for him.

## 4. The red nobody saw

The 21:44 push went red and the session did not read it, because the next thing it did was start three lanes. The wrap seat read it. The cause was simple: lane B's 49 new rows home to his export file, the file was on disk at the seat, and it was never committed. `_state.check()` resolves homes on disk, so every local check passed and CI, working from a clean clone, failed four steps with one cause. The fix is to commit the file, which the wrap commit does. The lesson for the next seat: a row and the file it homes to go in the same commit.

## Resolved, and still open

Resolved: the phase 1 and 2 proof (`s306-D7` enacted, `s306-D4` phase 1 proven); the 78 (`s307-D1`..`D78`). Still open, and his: the picture page's 16 calls; the build order for the 49 rows; lane D's six questions; phase 3 of the redesign; the Project-instructions sentence.
