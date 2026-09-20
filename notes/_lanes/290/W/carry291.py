#!/usr/bin/env python3
"""#290 wrap — build `_CARRIES.md` § `## residual → #291` from § `## residual → #290`.

ONE programmatic pass, the #261…#289 shape:
  (a) every age bracket bumped by one — `[NEW — 0…]` → `[1…]`, `[N…]` → `[N+1…]`;
  (b) ONE STRIKE, naming its receipt (`s183-D1` strike form, `s188-D2` receipt);
  (c) SIX new items in front, newest first.
⛔ Nothing is dropped, re-worded, re-ordered or truncated. `s225-D2` clause (i).

THE ONE STRIKE, and why it is the only one:

  #290's item ② — "THE CATALOGUE *PAGE* VARIANT IS OWED AND IS #290'S FIRST JOB" — is struck
  because the claim its HEADLINE makes was settled by Dave's eye rather than by the flat page
  being drawn. He ruled the OPEN BOOK four times in a row, took the result, and said
  "like it, that should be on the inventory page"; the book is on v11's slide 6 and in 10's
  Parts cell at commit `d96f08c7`. The variant is no longer owed and was never #290's job.

  ⛔ Nothing else is struck. In particular #290's ④ — "DECK v11 IS OWED AND THE FOUR D2 FLAGS
  ARE NOT ACTED ON" — is NOT struck: v11 exists but is ONLY the catalogue swap, the four flags
  are untouched and his slide-by-slide read has not been given, so the headline is HALF true and
  `s183-D1` strikes a HEADLINE and never a clause. What changed is minted as new item ④ instead:
  "a strike that is wrong is worse than an item that is merely stale" (`s271-D4`).
"""
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
CARRIES = os.path.join(ROOT, "_CARRIES.md")
sys.path.insert(0, os.path.join(ROOT, "knowledge"))
import _capture_gate as cg  # the ONE definition of "a carry"

text = open(CARRIES, encoding="utf-8").read()
src = [l for l in text.split("\n") if l.startswith("> **residual → #290:**")]
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
    ("⬛ **② THE CATALOGUE *PAGE* VARIANT IS OWED AND IS #290'S FIRST JOB** [1, DAVE'S]",
     "⬛ ~~**② THE CATALOGUE *PAGE* VARIANT IS OWED AND IS #290'S FIRST JOB** [1, DAVE'S]~~ ⛔ "
     "**STRUCK AT THE #290 WRAP — HE TOOK THE OPEN BOOK AND PUT IT ON THE INVENTORY PAGE, AND "
     "THE STRIKE NAMES ITS RECEIPT (`s183-D1` strike form, `s188-D2` receipt).** He ruled the "
     "drawing by eye four times in a row — ***\"can you fix the catalog diagram first, one page "
     "is upside down, and it would be better is it wasnt flat maybe a 60 degree angle\"***, "
     "***\"and the bookmark is placed accross a page it should come down the page from teh "
     "top\"***, ***\"place the text on the left, the pages seem to turn up in the middle, either "
     "this should be on the outer edges, or bent into the book at the middle\"***, ***\"and the "
     "book make should be in the middle\"*** — and then accepted it: ***\"like it, that should "
     "be on the inventory page\"***, followed by ***\"and the parts image on, slide 10\"***. ⇒ "
     "**The FLAT PAGE variant is not owed: the slot it was owed for is filled by the book.** "
     "Correction inscribed at commit `d96f08c7`, "
     "`notes/_lanes/289/illustration/catalogue.html` (v2, v1 preserved beside it), "
     "`notes/_DEMO-SLIDES-apollo-2026-09-20-v11.html` slide 6 and slide 10's Parts cell, and "
     "`notes/_lanes/290/DAVE-RULINGS-2026-09-20.md` lines 2–7. ⚠ **WHAT IS NOT CLOSED BY THIS "
     "STRIKE IS CARRIED AS NEW ITEMS RATHER THAN LEFT INSIDE A STRUCK ONE: his acceptance is an "
     "ACCEPTANCE BY EYE and not an inscription (new ①), and v11 is only the catalogue swap (new "
     "④).** The original item, kept verbatim:"),
]

# ---- (c) the session's SIX new items ----------------------------------------------------------
# ⚠ ① IS LOAD-BEARING: `_gen_titles.py` derives NEXT-TITLE from the FIRST ⬛ bullet's bolded
#   clause on the banner's pointer line, and `title_generation_check()` is BLOCKING.
# ⚠ NO bare " · " inside an item (it is the carry set's own split token) and NO `[N]` bracket in
#   prose (it reads as a second age). Ages spelled in words.
NEWITEMS = [
 "⬛ **① THE CATALOGUE WAS RULED BY EYE FOUR TIMES AND HE TOOK IT — AN ACCEPTANCE, NOT AN "
 "INSCRIPTION** [NEW — 0, DAVE'S] — **four consecutive notes, each a one-constant geometry "
 "change, each answered with a render while he waited**: the upside-down page (mirrored across "
 "the spine, not turned 180°), the 60° lean on a wedge stand with the tail edge on the plate, "
 "the bookmark down the middle from the head and hanging free off the tail, the leaves bent INTO "
 "the gutter with the captions left-aligned, and the book mark in the middle. **His verdict is "
 "two sentences: *\"like it, that should be on the inventory page\"* and *\"and the parts image "
 "on, slide 10\"*.** ⚠ **NOT INSCRIBED — he did not say *inscribe* and the rulings store stays "
 "at 622, verified at this seat by `json.load` with no `s290-` id present**, so this is a "
 "question put and not a state of the world (`s271-D4`). ⇒ **Whether an acceptance by eye of a "
 "drawing is ever worth inscribing is his.** Receipts: "
 "`notes/_lanes/290/DAVE-RULINGS-2026-09-20.md`, commit `d96f08c7`, "
 "`notes/_lanes/289/illustration/catalogue.html`.",

 "⬛ **② TWO WORKERS IN OVERALLS ON THE LINE — HIS LAST ASK, NOT STARTED, AND #291'S FIRST JOB** "
 "[NEW — 0, DAVE'S] — verbatim: ***\"the line slide - 4. could I have two workers in overalls in "
 "the place of the robots that are on slide 05. so two drawings one with humans and one with "
 "robots\"***. ⇒ **A SECOND line scene from `notes/_lanes/289/illustration/line.html`, same "
 "idiom and same maths, the two robot arms replaced by two human figures in overalls; slide 4 "
 "takes the humans and slide 5 keeps the robots.** ⛔ **NOT CUT AS A LANE, and the reason is on "
 "the record rather than implied: the seam check read the window past tolerance and he chose to "
 "wrap on the instrument.** Receipt: `notes/_lanes/290/DAVE-RULINGS-2026-09-20.md` line 8.",

 "⬛ **③ THE SEAM CHECK FIRED AND WAS OBEYED FOR THE SECOND TIME ON RECORD** [NEW — 0, DAVE'S] — "
 "the reading quoted to him in chat was **FILL 228,094 real over 48 turns, boot 74,165, OUTSIDE "
 "the 220,000 tolerance, no more lanes, wrap**, and his whole answer was ***\"okay, wrap\"***. ⇒ "
 "**An instrument fired, a human agreed with it, and a lane that was already specified was NOT "
 "cut — the first session to do that was #283 and this is the second.** ⛔ **Whether `s283-D1`'s "
 "tolerance arm should become BLOCKING rather than advisory is ruling-shaped and remains his** — "
 "two obediences are evidence that the instrument is trusted, not a rule that it must be. "
 "Receipt: `notes/_lanes/290/DAVE-RULINGS-2026-09-20.md` line 9 and "
 "`notes/_lanes/290/WRAP-BRIEF.md` § Gauge.",

 "⬛ **④ DECK v11 EXISTS AND IS ONLY THE CATALOGUE SWAP — THE FOUR D2 FLAGS AND HIS "
 "SLIDE-BY-SLIDE READ ARE UNTOUCHED** [NEW — 0, DAVE'S] — **measured at this seat: v11 carries "
 "the same TWELVE numbered slides inside THIRTEEN `section.slide` blocks as v10, which is "
 "itself untouched; s6's canvas id moves `#bk` → `#ct`, the books IIFE draws into an off-screen "
 "`#bkHost` so it still bakes 10's 02 Knowledge without animating, and 10's 01 Parts cell now "
 "takes `ctPrint`.** ⇒ **Nothing else in v11 moved: the five-white-cards rhythm, the callipers "
 "filling half their card, the gearbox scale bar riding into the s10 Parts cell and the heavier "
 "brain frame all stand, and the robots slide is not back on dark.** ⛔ **His slide-by-slide read "
 "has still not been given and it gates all four.** ⚠ **This is minted as a new item rather than "
 "used to strike the aged one, because the aged headline is half true and `s183-D1` strikes a "
 "headline and never a clause.** Receipts: `notes/_DEMO-SLIDES-apollo-2026-09-20-v11.html`, "
 "commit `d96f08c7`.",

 "⚠ **⑤ THE DRAWING EDITS WERE MADE IN SEAT AND THE DELEGATION RULE WAS DEPARTED FROM, "
 "DECLARED** [NEW — 0, DAVE'S] — **ZERO subs ran this session.** The conductor made three edit "
 "passes and five renders on `catalogue.html` and the v11 port himself, at his own seat, against "
 "`s204-D1` as restated at #284. ⛔ **The departure is PUBLISHED rather than smoothed away**, and "
 "the conductor's own reason is carried verbatim from the brief: each of Dave's notes was a "
 "one-constant geometry change with him waiting on the render, and the whole exchange cost less "
 "than one lane brief. ⇒ **Whether a *one-constant edit with Dave waiting* exception to the "
 "delegation rule exists is ruling-shaped and is HIS**, and until he says so the rule stands as "
 "written and this session is a recorded exception to it, not a precedent.",

 "⚠ **⑥ NO `subs` LINE COULD BE WRITTEN FOR #290, AND THE ABSENCE IS DECLARED RATHER THAN "
 "DEFAULTED** [NEW — 0] — **zero lanes ran, so there are no delegated sub figures to record; the "
 "one sub-transcript on disk beneath the conductor's session is this wrap seat itself.** The "
 "gauge-log clause is explicit that ABSENT IS LEGAL and that absence is never defaulted: no "
 "zero-line, no n/a line, and an UNKNOWN is never turned into a number "
 "[[feedback-measuring-tool-must-not-guess]]. ⇒ **The #290 stratum carries no `subs` line at "
 "all and says why in words.** ⚠ **And this wrap seat's OWN spend stays UNMEASURED**: a sub "
 "cannot read its own `message.usage` as a final total from inside itself, and a placeholder "
 "would be a guess wearing a measurement's clothes.",
]

# ---- assemble ---------------------------------------------------------------------------------
struck = aged
for old, new in STRIKES:
    assert struck.count(old) == 1, f"strike anchor not unique: {old[:70]} ({struck.count(old)})"
    struck = struck.replace(old, new, 1)

head = "> **residual → #291:** "
body = " · ".join(NEWITEMS) + " · " + struck[len("> **residual → #290:** "):]
line = head + body

after = len(cg._carry_items(line))
print(f"carries {before} → {after}  (+{after - before}) · {n_new} `[NEW — 0]` aged in · "
      f"{len(NEWITEMS)} new · {len(STRIKES)} struck")
print(f"invisible to the probe: {len(NEWITEMS)} new items (`_AGE_RE` misses `[NEW — 0]`)")

SECTION = "## residual → #291"
new_text = text.replace("## residual → #290", SECTION + "\n\n" + line + "\n\n## residual → #290", 1)
assert SECTION in new_text and new_text.count("## residual → #290") == 1

if "--write" in sys.argv:
    tmp = CARRIES + ".tmp"
    open(tmp, "w", encoding="utf-8").write(new_text)
    os.replace(tmp, CARRIES)
    chk = open(CARRIES, encoding="utf-8").read()
    l2 = [x for x in chk.split("\n") if x.startswith("> **residual → #291:**")]
    assert len(l2) == 1 and len(cg._carry_items(l2[0])) == after, "POST-CONDITION FAILED"
    print(f"WROTE {CARRIES} · § {SECTION} · {len(line):,} B · probe {after}")
else:
    print("DRY ONLY — pass --write to land it.")
