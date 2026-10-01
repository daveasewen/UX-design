# replay #310 — generated from `knowledge/_tests/wrap_views/310/STORY.md` + `knowledge/_tests/wrap_views/310/FACTS.json`

limits: 0 fail · 0 warn

| view | verdict | size gen / hand | figures missing | unsourced | words missing | headings |
|---|---|---|---|---|---|---|
| banner.md | GREEN (declared numbers: 436) | 750 / 741 (1.012) | 0 | 0 | 0 | same |
| delta.md | GREEN | 1,157 / 1,068 (1.083) | 0 | 0 | 0 | same |
| stratum.md | GREEN | 1,822 / 1,820 (1.001) | 0 | 0 | 0 | same |
| stamp.md | GREEN | 231 / 222 (1.041) | 0 | 0 | 0 | same |
| handoff.md | GREEN (declared numbers: 123, 7,947, 7,988, 8,105) | 4,685 / 4,623 (1.013) | 0 | 0 | 0 | same |
| prior-strikes.md | GREEN (declared rulings: s310-D7, s310-D8) | 618 / 385 (1.605) | 0 | 0 | 0 | same |
| dossier.md | GREEN | 1,422 / 1,385 (1.027) | 0 | 0 | 0 | same |
| report.md | GREEN (declared numbers: 436, 7,947, 7,988, 8,105; declared paths: facts-launch.json) | 1,773 / 2,236 (0.793) | 0 | 0 | 0 | same |
| WRAP-MEMORY-HOOK.md | GREEN | 1,099 / 1,147 (0.958) | 0 | 0 | 0 | same |
| new.txt | GREEN | 846 / 846 (1.0) | 0 | 0 | 0 | same |
| strike-1.txt | GREEN | 122 / 122 (1.0) | 0 | 0 | 0 | same |
| strike-2.txt | GREEN | 135 / 135 (1.0) | 0 | 0 | 0 | same |
| strike-3.txt | GREEN | 182 / 182 (1.0) | 0 | 0 | 0 | same |
| strike-4.txt | GREEN | 120 / 120 (1.0) | 0 | 0 | 0 | same |
| carries-delta.md | GREEN (reconstruction) | 1,483 / 0 (None) | 0 | 0 | 0 | same |
| rows.json | GREEN | 890 / 857 (1.039) | 0 | 0 | 0 | same |
| msg.txt | GREEN (declared numbers: 436, 7,824) | 468 / 473 (0.989) | 0 | 0 | 0 | same |
| SUMMARY.md | GREEN | 436 / 435 (1.002) | 0 | 0 | 0 | same |
| 5b.md | GREEN | 167 / 167 (1.0) | 0 | 0 | 0 | same |
| msg-5b.txt | GREEN (declared numbers: 7,988) | 247 / 284 (0.87) | 0 | 0 | 0 | same |

VERDICT: 20 of 20 graded views GREEN — the session replays GREEN; the residue is explained in the lane's report, view by view.

- declared `123`: a figure typed from the committer's log (run seconds, path counts, minutes to the summary, the previous wrap's chain) — FACTS.json carries no commit timing; a --gate-log/--commit-log reader would close it (E-build Found-not-fixed 4)
- declared `436`: the post-roll carries count — typed by the hand seat AFTER the roll; no tool measures it before the roll, the generated views name the probe (E-build § 2)
- declared `7,824`: a figure typed from the committer's log (run seconds, path counts, minutes to the summary, the previous wrap's chain) — FACTS.json carries no commit timing; a --gate-log/--commit-log reader would close it (E-build Found-not-fixed 4)
- declared `7,947`: a figure typed from the committer's log (run seconds, path counts, minutes to the summary, the previous wrap's chain) — FACTS.json carries no commit timing; a --gate-log/--commit-log reader would close it (E-build Found-not-fixed 4)
- declared `7,988`: _CHAIN.md after the 5b regen — typed by the hand seat after the regen that FOLLOWS the views; post.chain_tk_after_5b is null by the #241 rule
- declared `8,105`: _CHAIN.md after the 5b regen — typed by the hand seat after the regen that FOLLOWS the views; post.chain_tk_after_5b is null by the #241 rule
- declared `facts-launch.json`: the hand process's SECOND facts file (`_wrap_facts.py` run again to the launch); phase 3 carries the launch cut inside FACTS.json as `fill.launch` (★ E-replay), so there is no second file to name
- declared `s310-D7`: an id the hand seat put in its SECOND text of the strike (the prior handoff's addendum); the generated addendum is the strike receipt verbatim, and that receipt is proven byte for byte by the carries reconstruction
- declared `s310-D8`: an id the hand seat put in its SECOND text of the strike (the prior handoff's addendum); the generated addendum is the strike receipt verbatim, and that receipt is proven byte for byte by the carries reconstruction

Grading as run: (2026-10-01), the grading as run, each choice declared here and in REPLAY.md:; memory    graded at the WRAP stage against what the placer places — `memory_indexline_<n>.txt` + `memory_file_<n>.md`; (= front + body), NOT the hook's placer instructions (they name the hand process's five payload files, which; phase 3 replaces with one) and NOT an area-file payload (no story section carries one; Found-not-fixed).; Headings for memory are graded by LEVEL SEQUENCE inside the hook's `## BODY` (the #309 hand heading read; `### OPEN, DAVE'S —`, the template's constant is #310's `### OPEN —`).; report    headings are graded against the `s218-D7` form the generated report must carry (`## Found, not fixed`,; `## Ruling-shaped questions`, `REPLAY-THESE:`), not the hand file's (`## RULING-SHAPED QUESTIONS`): the; generated report IS the filed report (`s306-D5`).; DECLARED  one figure class is declared per session and reported, not hidden: the POST-ROLL carries count (429/436/442),; which no tool can measure before the roll — the generated views name the probe instead (E-build § 2). A; declared figure still prints in the per-view diff under `declared`.; prior-strikes  graded against the addendum at the foot of the previous handoff, on figures, words and headings; its; SIZE is not graded — the view is the strike receipt verbatim (`strike-<k>.txt` is graded byte for byte), where; the hand seats wrote a second, shorter line by hand.; carries-delta  graded by the `s183-D1` RECONSTRUCTION on the GENERATED block: `_CARRIES.md` from the FULL #n line down,; the block appended, #n+1 rendered, compared byte for byte with the hand-rolled FULL #n+1 line.
