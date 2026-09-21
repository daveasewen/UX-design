#!/usr/bin/env python3
"""#291 wrap — build `_CARRIES.md` § `## residual → #292` from § `## residual → #291`.

ONE programmatic pass, the #261…#290 shape:
  (a) every age bracket bumped by one — `[NEW — 0…]` → `[1…]`, `[N…]` → `[N+1…]`;
  (b) ONE STRIKE, naming its receipt (`s183-D1` strike form, `s188-D2` receipt);
  (c) SIX new items in front, newest first.
⛔ Nothing is dropped, re-worded, re-ordered or truncated. `s225-D2` clause (i).

THE ONE STRIKE, and why it is the only one:

  #291's item ② — "TWO WORKERS IN OVERALLS ON THE LINE — HIS LAST ASK, NOT STARTED, AND #291'S
  FIRST JOB" — is struck because its headline claim ("not started", "#291's first job") was
  settled: six versions were drawn by his eye and v6 is on deck v12's slide 4 with the robots
  kept on slide 5, at commit `b9ab75b0`, on his own "okay almost, but lets just get it in the
  slide". The brief names this strike and its receipt, and it is the ONLY strike the brief names.

  ⛔ Nothing else is struck. In particular #291's ④ — "DECK v11 EXISTS AND IS ONLY THE CATALOGUE
  SWAP — THE FOUR D2 FLAGS AND HIS SLIDE-BY-SLIDE READ ARE UNTOUCHED" — is NOT struck: v12 now
  exists, but the four D2 flags are still untouched and the slide-by-slide read has still not
  been given, so the headline is HALF true and `s183-D1` strikes a HEADLINE and never a clause.
  What changed is minted as new items instead: "a strike that is wrong is worse than an item
  that is merely stale" (`s271-D4`).
"""
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
CARRIES = os.path.join(ROOT, "_CARRIES.md")
sys.path.insert(0, os.path.join(ROOT, "knowledge"))
import _capture_gate as cg  # the ONE definition of "a carry"

text = open(CARRIES, encoding="utf-8").read()
src = [l for l in text.split("\n") if l.startswith("> **residual → #291:**")]
assert len(src) == 1, len(src)
src = src[0]
before = len(cg._carry_items(src))

# ---- (a) ages -------------------------------------------------------------------------------
n_new = len(re.findall(r"\[NEW — 0(?=[,\]])", src))
aged = re.sub(r"\[(\d+)(?=[,\]])", lambda m: "[%d" % (int(m.group(1)) + 1), src)
aged = re.sub(r"\[NEW — 0(?=[,\]])", "[1", aged)
assert "[NEW — 0" not in aged

# ---- (b) THE ONE STRIKE, headline only, receipt named -----------------------------------------
STRIKES = [
    ("⬛ **② TWO WORKERS IN OVERALLS ON THE LINE — HIS LAST ASK, NOT STARTED, AND #291'S FIRST JOB** [1, DAVE'S]",
     "⬛ ~~**② TWO WORKERS IN OVERALLS ON THE LINE — HIS LAST ASK, NOT STARTED, AND #291'S FIRST "
     "JOB** [1, DAVE'S]~~ ⛔ **STRUCK AT THE #291 WRAP — THE WORKERS WERE DRAWN SIX TIMES BY HIS "
     "EYE AND THE SIXTH IS ON THE DECK, AND THE STRIKE NAMES ITS RECEIPT (`s183-D1` strike form, "
     "`s188-D2` receipt).** Six versions in one day, each answered with a render while he waited "
     "— v2 on his four reference images (\"*one is a sketch of a man in overalls, one is a "
     "drawing of overalls the other two are human bodies drawn with a construction method*\"), v3 "
     "on the six tidy-up notes, v4 on \"*can we get the shoulders looking more natural, and "
     "rounded*\", v5 on the three notes about shoulders and the clash with the conveyor, v6 on "
     "the top oval facet, the torso corners and the box-hands — and then his acceptance: ***\"okay "
     "almost, but lets just get it in the slide\"***. ⇒ **v6 is on deck v12's slide 4 (`#lw`, print "
     "`#lwPrint`) and the robots are kept on slide 5, and the flat-page gearbox is displaced from "
     "slide 4.** Correction inscribed at commit `b9ab75b0`, "
     "`notes/_lanes/289/illustration/line-workers.html` (v6, with v1…v5 preserved beside it), "
     "`notes/_DEMO-SLIDES-apollo-2026-09-20-v12.html` slides 4 and 5, the six filed lane reports "
     "`notes/_subreports/2026-09-20-291-L*-*.md`, and "
     "`notes/_lanes/291/DAVE-RULINGS-2026-09-20.md` lines 11–36. ⚠ **WHAT IS NOT CLOSED BY THIS "
     "STRIKE IS CARRIED AS NEW ITEMS RATHER THAN LEFT INSIDE A STRUCK ONE: his *\"almost\"* is "
     "still attached and the acceptance is an ACCEPTANCE BY EYE and not an inscription (new ①), "
     "and slide 4's copy was written against the gearbox and now sits beside the workers (new "
     "⑤).** The original item, kept verbatim:"),
]

# ---- (c) the session's SIX new items ----------------------------------------------------------
# ⚠ ① IS LOAD-BEARING: `_gen_titles.py` derives NEXT-TITLE from the FIRST ⬛ bullet's bolded
#   clause on the banner's pointer line, and `title_generation_check()` is BLOCKING.
# ⚠ NO bare " · " inside an item (it is the carry set's own split token) and NO `[N]` bracket in
#   prose (it reads as a second age). Ages spelled in words.
NEWITEMS = [
 "⬛ **① SIX VERSIONS BY HIS EYE IN ONE DAY AND THE SIXTH IS ON THE DECK** [NEW — 0, DAVE'S] — "
 "**an ACCEPTANCE, not an inscription, and his *\"almost\"* is still attached.** Six consecutive "
 "passes on `notes/_lanes/289/illustration/line-workers.html`, each cut as its own Opus lane (L "
 "→ L6) and each answered with a rest render and an orbit render while he waited: the robots "
 "became human figures built by construction method on his four reference images, then the flat "
 "facet on the crown went, the second body stepped to the side of the conveyor, the arm stopped "
 "growing out of its body, the ankles became columns, the ball joints went, the shoulders were "
 "rounded and then set down the body, the first body stepped back off the conveyor, the flat "
 "facet on the shoulders went, and finally the top oval facet, the torso corners facing us and "
 "the box-hands. **His verdict is one sentence: *\"okay almost, but lets just get it in the "
 "slide\"*.** ⚠ **NOT INSCRIBED — he did not say *inscribe* and the rulings store stays at 622, "
 "verified at this seat by `json.load` with no `s291-` id present**, so this is a question put "
 "and not a state of the world (`s271-D4`). ⇒ **Whether six acceptances by eye and an *\"almost\"* "
 "on the deck are ever worth inscribing is his, and what the remaining *\"almost\"* is remains "
 "unasked.** Receipts: `notes/_lanes/291/DAVE-RULINGS-2026-09-20.md`, commit `b9ab75b0`, the six "
 "reports `notes/_subreports/2026-09-20-291-L*-*.md`.",

 "⬛ **② PARTS ON SLIDE 10 IS THE GEARBOX, READ FROM HIS SCREENSHOT, AND #290'S WORD PUT THE "
 "CATALOGUE THERE** [NEW — 0, DAVE'S] — his whole instruction was ***\"lets just have these the "
 "three on slide 10\"*** with a three-up screenshot attached, and the screenshot showed **Parts = "
 "the GEARBOX**, Knowledge and Proficiency. ⚠ **#290's own word had been *\"and the parts image "
 "on, slide 10\"*, which put the CATALOGUE in that cell, and v11 shipped it that way.** Measured "
 "at this seat in v12: `MAP` reads `an1→gbPrint`, `an2→bkPrint`, `an3→brPrint`, and the "
 "catalogue's `ctPrint` stays on slide 6. ⇒ **Two of his own instructions disagree about one "
 "cell, the later one was read out of an image rather than out of a sentence, and which he "
 "meant is HIS.** Receipts: `notes/_lanes/291/DAVE-RULINGS-2026-09-20.md` line 38, "
 "`notes/_subreports/2026-09-20-291-P2-slide10-three-up.md`, commit `b9ab75b0`.",

 "⬛ **③ SLIDE 10 IS THREE CELLS NOW AND THE ARM DRAWING HAS NO HOME IN THE DECK** [NEW — 0, "
 "DAVE'S] — slide 10 went from five cells to three on his screenshot: **Tools and Process were "
 "removed with their cells**, the headline became *\"Three things she is made of.\"*, and the "
 "three drawings were scaled to fill what was left (the image box 135px → `clamp(150px,25.5vh,"
 "240px)`, 229.5px at a 900px viewport, measured in the file at this seat). ⚠ **`amPrint` — the "
 "arm — is still baked off-screen and now has NO CONSUMER anywhere in the deck**, verified here "
 "by counting its occurrences against `ctPrint`'s. ⇒ **Whether the arm drawing gets a home, or "
 "is retired, is his; a drawing that bakes into nothing is an "
 "[[instrument-without-a-consumer]] in the deck rather than in the tooling.** Receipts: "
 "`notes/_subreports/2026-09-20-291-P2-slide10-three-up.md`, "
 "`notes/_subreports/2026-09-20-291-P3-slide10-bigger-images.md`, "
 "`notes/_lanes/289/illustration/arm.html`.",

 "⬛ **④ THE SEAM CHECK WAS OVERRIDDEN ONCE AND THEN OBEYED — THE FIRST HUMAN OVERRIDE ON "
 "RECORD** [NEW — 0, DAVE'S] — the seam read **FILL 220,302 real over 42 turns, OUTSIDE the "
 "220,000 tolerance, wrap** and was quoted to him; **his answer was ANOTHER NOTE** (*\"lets make "
 "better use of the space here, the images could be bigger\"*), the conductor took it as \"one "
 "more, not wrap yet\" and said so in chat, lane P3 ran, and the wrap came on his next word "
 "(*\"okay push and wrup\"*). ⇒ **#283 and #290 obeyed the instrument; #291 is the THIRD session "
 "where it fired and the FIRST where the human overrode it once before obeying it.** ⚠ **That is "
 "evidence about the tolerance arm and not a ruling on it: whether `s283-D1`'s arm becomes "
 "BLOCKING rather than advisory is still his, and an arm that CAN be overridden by a note is a "
 "different object from one that cannot.** Receipts: `notes/_lanes/291/WRAP-BRIEF.md` § Gauge, "
 "`notes/_lanes/291/DAVE-RULINGS-2026-09-20.md` lines 41–45.",

 "⚠ **⑤ SLIDE 4'S COPY WAS WRITTEN AGAINST THE GEARBOX AND NOW SITS BESIDE THE WORKERS** [NEW — "
 "0, DAVE'S] — the headline on slide 4 is still *\"An assembly line is only as fast as its parts "
 "bin, the skill of the assembly engineer, and the rigour of QC\"*, written when the slide "
 "carried the gearbox; **the gearbox was displaced to an off-screen `#gbHost` and the two "
 "workers took the canvas.** It reads fine to the conductor's eye and that is a reading, not a "
 "ruling. ⇒ **Whether the copy is re-cut for the drawing it now sits beside is his, and it rides "
 "with the slide-by-slide read he has not yet given.** Receipts: "
 "`notes/_subreports/2026-09-20-291-P-deck-v12.md`, "
 "`notes/_DEMO-SLIDES-apollo-2026-09-20-v12.html` slide 4.",

 "⚠ **⑥ THE MOUNT DEFECT BECAME TOTAL AND THE DELETE GRANT IS THE PREVENTION — CALL IT AT THE "
 "FIRST COMMIT** [NEW — 0] — **every git write this session stranded an un-unlinkable "
 "`.git/index.lock`**, so the commit script's per-path `git add` loop failed on its second path; "
 "three refusals were paid before one clean run (REUSED-MSGFILE with the T3 prefix on line 1 for "
 "the THIRD session running, the doc-row gate on eight unrowed reports, then the lock). **The "
 "fix is runbook step 0 — `mcp__cowork__allow_cowork_file_delete` on `.git/index.lock`, the "
 "per-session delete grant that [[git-lock-mv-not-rm]] names as the prevention — and it must be "
 "called at the FIRST commit, before any git write, not after the first refusal.** ⚠ **The grant "
 "is per-session and does not survive into the next window.** Receipts: "
 "`notes/_lanes/291/WRAP-BRIEF.md` § Declared by the conductor.",
]

# ---- assemble ---------------------------------------------------------------------------------
body = aged[len("> **residual → #291:** "):]
for old, new in STRIKES:
    assert body.count(old) == 1, f"STRIKE anchor not unique ({body.count(old)}): {old[:70]}"
    body = body.replace(old, new + " " + old, 1)

line = "> **residual → #292:** " + " · ".join(NEWITEMS) + " · " + body
after = len(cg._carry_items(line))

HEAD = "## residual → #292"
assert HEAD not in text, "§ residual → #292 already exists — refusing to write it twice"
anchor = "## residual → #291"
i = text.index(anchor)
new_text = text[:i] + HEAD + "\n\n" + line + "\n\n" + text[i:]

if "--write" in sys.argv:
    tmp = CARRIES + ".tmp"
    open(tmp, "w", encoding="utf-8").write(new_text)
    os.replace(tmp, CARRIES)
    print("WROTE _CARRIES.md")
print(f"probe {before} → {after}   (+{after - before}) · {n_new} `[NEW — 0]` aged to [1] · "
      f"{len(NEWITEMS)} new · {len(STRIKES)} struck")
print(f"line length {len(line):,} B · parts {len(line.split(' · ')):,}")
