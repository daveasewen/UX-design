#!/usr/bin/env python3
"""#282 wrap — build `_CARRIES.md` § `## residual → #283` from § `## residual → #282`.

ONE programmatic pass, the #261…#281 shape:
  (a) every age bracket bumped by one — `[NEW — 0…]` → `[1…]`, `[N…]` → `[N+1…]`;
  (b) ★ TWO surgical edits, each carrying its `s183-D1`/`s188-D2` receipt:
      · #282's ① — the 15 rule notes, whose claim was *"nothing has been inscribed and no guideline
        file has been changed"*. `s282-D1` inscribed ELEVEN of them in his own words. Struck.
      · #281's ② — the eye-check of the six matrix cells, carried as *"asked and unanswered"*. It was
        never open: he had settled it at `s280-D1` and said so (*"sorry I though this was settled"*).
        Struck, and the strike names WHOSE item it actually was.
  (c) the session's SEVEN new items written in front, newest first.
⛔ Nothing is dropped, re-worded, re-ordered or truncated. `s225-D2` clause (i).
⚠ NOT re-minted, because the age bracket is what carries a repeat and never a second copy: the
  git-lock runbook line (#282's ⑦ → [1], and three lanes plus the conductor met it AGAIN today),
  `gen_kg_rules.py`'s footgun (#282's ⑥ → [1], now worth 75 lines not 73), the logo review (whose
  page was GIVEN — its successor is a NEW item, the masters), `s277-D12`, the `#243` not-a-wrap form,
  `jade-lifestyle`, the `_HANDOFF-130` four.
"""
import os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
CARRIES = os.path.join(ROOT, "_CARRIES.md")
sys.path.insert(0, os.path.join(ROOT, "knowledge"))
import _capture_gate as cg  # the ONE definition of "a carry"

text = open(CARRIES, encoding="utf-8").read()
src = [l for l in text.split("\n") if l.startswith("> **residual → #282:**")]
assert len(src) == 1, len(src)
src = src[0]
before = len(cg._carry_items(src))

# ---- (a) ages -----------------------------------------------------------------------------
n_new = len(re.findall(r"\[NEW — 0(?=[,\]])", src))
aged = re.sub(r"\[(\d+)(?=[,\]])", lambda m: "[%d" % (int(m.group(1)) + 1), src)
aged = re.sub(r"\[NEW — 0(?=[,\]])", "[1", aged)
assert "[NEW — 0" not in aged

# ---- (b) the TWO surgical edits ------------------------------------------------------------
OLD1 = "⬛ **① THE 15 RULE NOTES ARE HIS, AND THEY ARE #282'S FIRST MOVE** [1, DAVE'S]"
NEW1 = ("~~⬛ **① THE 15 RULE NOTES ARE HIS, AND THEY ARE #282'S FIRST MOVE** [1, DAVE'S]~~ "
        "⛔ **STRUCK AT THE #282 WRAP — THEY WERE PUT TO HIM ON A PAGE AND ELEVEN ARE NOW INSCRIBED; "
        "THE STRIKE CARRIES ITS RECEIPT (`s183-D1` strike, `s188-D2` receipt).** The claim below — that "
        "*\"nothing in that file has been inscribed and no guideline file has been changed\"* — was TRUE "
        "when written at the #281 wrap and is FALSE now. **The 15 notes became a 15-row decision page with "
        "a recommendation on every row** (`notes/_lanes/282/rule-notes/RULE-NOTES-2026-09-17.html`, "
        "conductor `256e4cf`), **his export at 19:10Z took 14 of 15 on the recommendation** "
        "(`notes/_lanes/282/rule-notes/DAVE-EXPORT-2026-09-17.json`), and **`s282-D1` (`56c5690`, lane RN) "
        "made ELEVEN GUIDELINE EDITS IN HIS OWN WORDS ACROSS EIGHT FILES** plus 2 second `restsOn` edges "
        "(73 → 75, verified by span at the wrap seat). A note on `col26-016` came back green. Correction "
        "inscribed at: `knowledge/_rulings.json` § `s282-D1` · "
        "`notes/_subreports/2026-09-17-282-RN-rule-notes-land.md` · "
        "`_HANDOFF-133-the-rule-notes-land-and-the-logo-is-ruled.md` · `knowledge/_REVIEW-SIGNOFF.md` "
        "(the row is struck there too, with the same receipt). ⚠ **WHAT SURVIVES THE STRIKE IS CARRIED AS "
        "A NEW ITEM RATHER THAN LEFT INSIDE A STRUCK ONE: `col26-012` is the ONE row he did not take — "
        "*\"Discuss first\"* — and it is item ④ below.**")

OLD2 = "⬛ **② THE EYE-CHECK OF THE SIX MATRIX CELLS IS ASKED AND UNANSWERED** [2, DAVE'S]"
NEW2 = ("~~⬛ **② THE EYE-CHECK OF THE SIX MATRIX CELLS IS ASKED AND UNANSWERED** [2, DAVE'S]~~ "
        "⛔ **STRUCK AT THE #282 WRAP — IT WAS NEVER OPEN, AND THE STRIKE CARRIES ITS RECEIPT "
        "(`s183-D1` strike, `s188-D2` receipt).** The claim below — that the eye-check was asked and "
        "unanswered — was FALSE from the day it was written. **He had already settled it at `s280-D1`**, "
        "which gave him all six cells with force as the default, and he said so in one sentence at #282: "
        "*\"sorry I though this was settled\"*. ⛔ **The carry was the CONDUCTOR'S expectation that a cell "
        "would be dropped on sight — never Dave's ask** — and it survived THREE wraps because the 2c EXIT "
        "CHECK tests PRESENCE (is the item homed?) and has no test for WHOSE item it is. ★ **THE LESSON, "
        "and it belongs beside `s271-D4`: an open item written as a question that was never asked is the "
        "sibling of an open item written as a state of the world.** Closed at `6bac5e4`; row `W-280lm` "
        "DONE. Correction inscribed at: `6bac5e4` · `_HANDOFF-133-the-rule-notes-land-and-the-logo-is-ruled.md` "
        "· `knowledge/_REVIEW-SIGNOFF.md` (struck there too, same receipt) · "
        "`_DECISION-HISTORY/2026-09-18-282-the-rule-notes-land-and-the-logo-is-ruled.md` § 2.")

for old in (OLD1, OLD2):
    assert aged.count(old) == 1, ("strike anchor", old[:60], aged.count(old))
aged = aged.replace(OLD1, NEW1, 1).replace(OLD2, NEW2, 1)

# ---- (c) the session's SEVEN new items -----------------------------------------------------
NEWITEMS = [
 "⬛ **① THE LOGO MASTERS AND THE THIRD DIAL** [NEW — 0, DAVE'S] — two things, and the first needs no "
 "conversation at all. **(a) THE PER-SIZE LOGO MASTERS ARE #283'S FIRST MOVE, FULLY SPECIFIED:** "
 "**8 lockups × 5 steps = 40 SVGs**, each drawn at its RAW PIXEL HEIGHT AND WIDTH with **no viewBox**, "
 "horizontals and stems snapped to the grid, built from the 8 surviving exports (`s282-D4` scrapped the "
 "identifier lockup and took `_logo_nodes.json` 12 → 8). The size steps are `s282-D3` as corrected at "
 "`c143a1b`: **x-small 24 · small 28 · medium 32 · large 36 · x-large 40**, by raw height. ⚠ **Two known "
 "and NOT blocking:** the two-inks light-mono, and the hexagon duplicate pair. ★ **This is the answer to "
 "his own question — *\"is it possible to 'hint' svgs so they are as sharp as possible?\"* — in the only "
 "form that answers it.** **(b) THE THIRD DIAL IS HIS AND IT IS UNKNOWN.** His frame, his words: *\"three "
 "dials we can use to tune the designers experience\"*. **Dial 1 is LAYERS** (foundations + a11y + "
 "regulation as the floor). **Dial 2 was offered as the tone-of-voice temperature map and REFUSED** — "
 "*\"no dial 2 isn't right. I'll take a look\"*. **Dial 3 is not named and no candidate is invented here**, "
 "because defaulting an absence into a number is exactly what `s214-D5` forbids, and it holds for prose. "
 "Receipts: `notes/_subreports/2026-09-18-282-LL-logo-land.md` · `notes/_lanes/282/DAVE-RULINGS-2026-09-17.md` "
 "· `notes/_lanes/282/logo-review/DAVE-EXPORT-2026-09-18.json`.",

 "⬛ **② THE THEORY DOOR AND THE THREE POSTURES — AN IDEA HE LIKED, AND THAT IS PRECISELY WHY IT IS NOT "
 "INSCRIBED** [NEW — 0, DAVE'S] — put to Dave at the wrap call and NOT ruled. Two of his sentences are the "
 "largest thing in #282 and neither is in `_rulings.json`. **(a)** *\"what harm is there to an agent having "
 "the principle as guidance … make it the hyper-designer I'm aiming for\"* — the **121 principles that no "
 "rule reaches**; the conductor's answer was to expose **all 145 with grade + misreadings** behind a THEORY "
 "DOOR, which finally gives **#130's thirteenth verb** (and `verbVia`) an actual consumer. **(b)** *\"other "
 "modes that aren't so strict … form opinions instead of simply following a rules decision tree\"* — the "
 "graph's philosophy; the conductor's counter was **strictness on the GRADE, not on the mode**: three "
 "postures **obey / weigh / argue**, where an agent opinion must CITE AN EDGE and is therefore gradeable. "
 "His reply: *\"this all sounds great, I really like this idea\"*. ⛔ **THAT IS ENTHUSIASM, NOT A RULING** "
 "[[premise-ages-faster-than-rule]] — the mirror of the `s271-D4` failure, an idea written into the record "
 "as a decision because he liked it. **ONE page when he asks for it, and not before.** Receipts: "
 "`notes/_lanes/282/DAVE-RULINGS-2026-09-17.md` · "
 "`_DECISION-HISTORY/2026-09-18-282-the-rule-notes-land-and-the-logo-is-ruled.md` § 4.",

 "⬛ **③ TWO MORE GENERATORS WOULD UNDO TODAY'S WORK IF RUN, AND ONE ALREADY DID IT TWICE** [NEW — 0] — "
 "named at the wrap, not fixed, and deliberately NOT a second copy of the `gen_kg_rules.py` item that ages "
 "to one bracket beside this one. **(a) `notes/_lanes/281/rests-on-land/land_rests_on.py` WOULD DROP LANE RN'S TWO "
 "NEW `restsOn` EDGES** — it is #281's lander and knows nothing of `s282-D1`'s two second edges; **the "
 "correct re-lander is `land_rule_notes.py`**. **(b) THE RATIFIED `gen_kg_icons.py` REWRITES "
 "`_icon_nodes.json` WITH OLDER WORDING WHEN RUN — and was REVERTED TWICE during #282 for exactly that.** "
 "⚠ **The class is now four deep** (`gen_kg_rules.py` · `gen_kg_edges.py` · `_build_all.py` · these two): "
 "**a ratified generator whose output is older than the hand-authored state it would overwrite.** ⛔ A "
 "standing-orders line naming the whole class, rather than one guard per generator, is **ruling-shaped and "
 "his** — the lanes can only keep naming them one at a time. Receipts: the #282 wrap brief § OPEN 5 · "
 "`notes/_subreports/2026-09-17-282-RN-rule-notes-land.md`.",

 "⬛ **④ `col26-012` IS THE ONE RULE NOTE HE DID NOT TAKE — *\"DISCUSS FIRST\"*** [NEW — 0, DAVE'S] — put "
 "to Dave at the wrap call. Of the fifteen rule notes on the decision page, **fourteen came back on the "
 "recommendation and this one came back asking for a conversation**. ⚠ **Do not read it as a rejection or "
 "as a deferral**: `s282-D2` separately closed the `col26-012` ASK from #281 (the red-text ban is on the "
 "PRIMARY red, the exception a SECONDARY red only, and the cross-reference he wanted was already present) — "
 "**what is open is the rule conversation he asked for, not the link**. ★ **AND IT IS THE SECOND OF ITS "
 "KIND IN TWO SESSIONS:** `aid-009`'s note at #281 was that the rule is *\"too boolean\"*, which is also a "
 "RULE conversation arriving through a LINK page. **Two rows in two sessions asking to talk about the rule "
 "is a fact about the rule corpus, not about the export mechanism**, and what to do about it is his. "
 "Receipts: `notes/_lanes/282/rule-notes/DAVE-EXPORT-2026-09-17.json` (19:10Z) · `knowledge/_rulings.json` "
 "§ `s282-D2` (`bb016c6`) · `notes/_subreports/2026-09-17-282-RN-rule-notes-land.md`.",

 "⬛ **⑤ WHAT SHOULD A SESSION DO AT THE HARD WALL? — THE THIRD BREACH, AND THE FAILURE MODE IS MIGRATING "
 "AWAY FROM THE INSTRUMENT** [NEW — 0, DAVE'S] — put to Dave at the wrap call, and this is the third wrap "
 "in a row to put it. **#282 closed at FILL 337,559 real over 141 turns — the 256,000 HARD LINE BREACHED BY "
 "81,559**, 157,559 past the ruled 180,000 stop line and 117,559 outside the ≤220,000 tolerance; larger than "
 "#277's and #281's breaches together. ⛔ **The arc across the three is the finding:** at #277 the wall was "
 "crossed under pressure · at **#281** the gauge was **read every turn and overruled every turn** (*an "
 "instrument that is read and then overruled is performing the function of a log, not of a gauge*) · at "
 "**#282 it was NOT READ AT ALL** between the logo review landing and the horizontal clear-space ruling, and "
 "**two Opus lanes were cut past the wall**. Dave's own words closed the day: *\"whats the context temp like, "
 "can we squeeze it in?\"* — answered no — then *\"ouch, better wrap\"*. ⚠ **`FILL_CEILING_BLOCKING` is "
 "ADVISORY by `s271-D2` and arming it is HIS**; a wrap may not arm it to make its own numbers look better. "
 "Receipts: `knowledge/_checkin.py` at the #282 wrap seat · `notes/_GAUGE-LOG.md` § post-mortem #282.",

 "⬛ **⑥ THREE BACKLOG ROWS WERE BORN IN #282 AND EACH IS ONE SENTENCE OF HIS** [NEW — 0, DAVE'S] — minted "
 "here rather than left in a lane report or a ruling body. **`W-282a` — THE UNIVERSAL ICON LIST** (born "
 "under `s282-D2`): which icons are universal enough to be named in a rule rather than illustrated in one. "
 "**`W-282b` — THE SC 2.2.2 CITATION ON `mot-005`** (same ruling): the rule is right and its WCAG pointer is "
 "missing, which is a one-line fix nobody is licensed to make unasked. **`W-282ll` — \"ASK CREATE\"**, and it "
 "is the largest of the three by a distance: *\"in the future we will re-integrate this material as an AI "
 "readable version of create, we might have something like 'Ask create' assistant bot\"*. ⚠ **That third one "
 "is a DIRECTION he stated, not a task he asked for** — it is carried so it is not lost, and **it is not a "
 "plan until he says it is**. Receipts: `knowledge/_rulings.json` § `s282-D2` · "
 "`notes/_lanes/282/DAVE-RULINGS-2026-09-17.md`.",

 "⬛ **⑦ THE TWO INSTRUMENTATION APPENDS ARE COMMITTED AND THE POLICY ON THEM IS STILL HIS** [NEW — 0, "
 "DAVE'S] — put to Dave at the wrap call. `notes/_REHEARSAL-LOG.jsonl` and "
 "`notes/_dream/_GRADE-DECISIONS.jsonl` are APPENDED TO BY THE INSTRUMENTS THEMSELVES every time "
 "`_checkin.py` or the wrap gate runs, so **a tree that was clean at the start of a ritual is dirty by the "
 "end of it, through no author's decision**. #282's conductor committed the day's two at `3f009cc` purely to "
 "clear the push gate, **and two more accrued during this very ritual**. ⚠ **The question is not whether the "
 "appends are harmless — they are — but whether an instrument may write into the tree the commit gate "
 "grades.** A candidate answer is already floated and is HIS to rule: **dream pass 6 P2**. ⛔ Until he rules "
 "it, every wrap commits them and says so, which is the honest form but not a policy. Receipts: the #282 "
 "wrap brief § DECLARED, last bullet · `3f009cc` · `notes/_dream/` pass 6 § P2.",
]

body = aged[len("> **residual → #282:** "):]
newline = "> **residual → #283:** " + " · ".join(NEWITEMS) + " · " + body
after = len(cg._carry_items(newline))
print("carries: before %d (of which %d were [NEW — 0]) → after %d ; new items %d"
      % (before, n_new, after, len(NEWITEMS)))

SECTION = "## residual → #283"
assert SECTION not in text, "section already exists"
anchor = "## residual → #282"
i = text.index(anchor)
if "--write" not in sys.argv:
    print("DRY — nothing written"); sys.exit(0)
text = text[:i] + SECTION + "\n\n" + newline + "\n\n" + text[i:]
open(CARRIES, "w", encoding="utf-8").write(text)
print("WROTE", CARRIES)
