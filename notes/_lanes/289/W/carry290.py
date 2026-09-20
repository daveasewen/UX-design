#!/usr/bin/env python3
"""#289 wrap — build `_CARRIES.md` § `## residual → #290` from § `## residual → #289`.

ONE programmatic pass, the #261…#288 shape:
  (a) every age bracket bumped by one — `[NEW — 0…]` → `[1…]`, `[N…]` → `[N+1…]`;
  (b) TWO STRIKES, each naming its receipt (`s183-D1` strike form, `s188-D2` receipt);
  (c) SIXTEEN new items in front, newest first.
⛔ Nothing is dropped, re-worded, re-ordered or truncated. `s225-D2` clause (i).

THE TWO STRIKES, and why they are the only two:

  #288's item ④ — "THE DECK'S NEW STRUCTURE IS HIS, AND WAVE 2 IS BLOCKED ON IT" — is struck
  because he GAVE the structure: the arc board on 09-19 and then the seven beats in his own
  words on 09-20. The blocked half is unblocked and the headline as a whole is no longer true.

  #288's item ⑤ — "WHICH EVENT FRIDAY 2026-09-25 IS" — is struck because he answered it in one
  sentence: "the 25th is the internal, but it is still very important".

  ⛔ Nothing else is struck. Every other carry is either untouched by this session or only
  HALF-discharged, and `s183-D1` strikes a HEADLINE and never a clause: "a strike that is wrong
  is worse than an item that is merely stale" (`s271-D4`).
"""
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
CARRIES = os.path.join(ROOT, "_CARRIES.md")
sys.path.insert(0, os.path.join(ROOT, "knowledge"))
import _capture_gate as cg  # the ONE definition of "a carry"

text = open(CARRIES, encoding="utf-8").read()
src = [l for l in text.split("\n") if l.startswith("> **residual → #289:**")]
assert len(src) == 1, len(src)
src = src[0]
before = len(cg._carry_items(src))

# ---- (a) ages -------------------------------------------------------------------------------
n_new = len(re.findall(r"\[NEW — 0(?=[,\]])", src))
aged = re.sub(r"\[(\d+)(?=[,\]])", lambda m: "[%d" % (int(m.group(1)) + 1), src)
aged = re.sub(r"\[NEW — 0(?=[,\]])", "[1", aged)
assert "[NEW — 0" not in aged

# ---- (b) TWO STRIKES, headline only, receipts named -------------------------------------------
STRIKES = [
    ("⬛ **④ THE DECK'S NEW STRUCTURE IS HIS, AND WAVE 2 IS BLOCKED ON IT** [1, DAVE'S]",
     "⬛ ~~**④ THE DECK'S NEW STRUCTURE IS HIS, AND WAVE 2 IS BLOCKED ON IT** [1, DAVE'S]~~ ⛔ "
     "**STRUCK AT THE #289 WRAP — HE GAVE THE STRUCTURE, AND THE STRIKE NAMES ITS RECEIPT "
     "(`s183-D1` strike form, `s188-D2` receipt).** He supplied the arc board "
     "`notes/_lanes/289/DAVE-ARC-BOARD-2026-09-19.png` with ***\"so this is the main arc, "
     "basically a set of problem statements (not literal) how they are broken down - light RCA, "
     "a solution and its constituent parts\"***, and then WROTE THE COPY HIMSELF in seven beats "
     "— ***\"The story is more like this\"***. ⇒ **The blocked half is unblocked: three deck "
     "recuts ran on it the same weekend and v10 carries his beats.** Correction inscribed at "
     "`notes/_lanes/289/DAVE-RULINGS-2026-09-19.md`, `notes/_lanes/289/DAVE-RULINGS-2026-09-20.md`, "
     "`notes/_DEMO-SLIDES-apollo-2026-09-20-v10.html` and "
     "`notes/_PROPOSAL-apollo-story-2026-09-20-v2.html`. ⚠ **WHAT SURVIVES THE STRIKE IS CARRIED "
     "AS NEW ITEMS RATHER THAN LEFT INSIDE A STRUCK ONE: his cross-communication question is "
     "still unanswered and rides in new item ⑯ below.** The original item, kept verbatim:"),

    ("⬛ **⑤ WHICH EVENT FRIDAY 2026-09-25 IS — SMALL INTERNAL DEMO OR DAVID RICE** [1, DAVE'S]",
     "⬛ ~~**⑤ WHICH EVENT FRIDAY 2026-09-25 IS — SMALL INTERNAL DEMO OR DAVID RICE** [1, "
     "DAVE'S]~~ ⛔ **STRUCK AT THE #289 WRAP — HE ANSWERED IT IN ONE SENTENCE, AND THE STRIKE "
     "NAMES ITS RECEIPT (`s183-D1` strike form, `s188-D2` receipt).** Verbatim, at the strand "
     "map's DATE band: ***\"the 25th is the internal, but it is still very important\"*** ⇒ "
     "**INTERNAL, and Rice-grade all the same** — the Thursday timed run and the recorded "
     "fallback both stand, and the one-shot runs live on the day. Correction inscribed at "
     "`notes/_lanes/289/DAVE-RULINGS-2026-09-19.md` § THE DATE and its machine copy. The "
     "original item, kept verbatim:"),
]

# ---- (c) the session's SIXTEEN new items ------------------------------------------------------
# ⚠ ① IS LOAD-BEARING: `_gen_titles.py` derives NEXT-TITLE from the FIRST ⬛ bullet's bolded
#   clause on the banner's pointer line, and `title_generation_check()` is BLOCKING.
# ⚠ NO bare " · " inside an item (it is the carry set's own split token) and NO `[N]` bracket in
#   prose (it reads as a second age). Ages spelled in words.
NEWITEMS = [
 "⬛ **① THE STORY IS HIS AND THE PLANT HAS SEVEN DRAWINGS** [NEW — 0, DAVE'S] — **he wrote the "
 "deck's copy himself, in seven beats, and the session's whole output hangs off it.** Verbatim: "
 "***\"The story is more like this — An assembly line is only as fast as its parts bin, the "
 "skill of the assembly engineer and the rigour of QC\"***, then the robots that tried to "
 "machine missing parts, the inventory built out, the engineer, the inspector, the build and the "
 "ask. ⇒ **The copy is HIS TEXT and is quoted, never paraphrased** — both files of his words are "
 "`notes/_lanes/289/DAVE-RULINGS-2026-09-19.md` and `…-2026-09-20.md`. **The plant's seven "
 "drawings are SIX NEW subjects plus the gearbox carried from v7**, measured at the wrap seat "
 "from `notes/_lanes/289/illustration/`: books, brain (six passes), arm, line scene, callipers "
 "and the open catalogue. ⚠ **NOT INSCRIBED — he did not say *inscribe* on either day and the "
 "rulings store stays at 622**, so this is a question put and not a state of the world "
 "(`s271-D4`). Receipts: `notes/_DEMO-SLIDES-apollo-2026-09-20-v10.html` and "
 "`notes/_PROPOSAL-apollo-story-2026-09-20-v2.html`.",

 "⬛ **② THE CATALOGUE *PAGE* VARIANT IS OWED AND IS #290'S FIRST JOB** [NEW — 0, DAVE'S] — his "
 "last drawing ask of the session, sent WHILE the catalogue lane was still running: ***\"The "
 "inventory slide (06) I think this should be an open book, like a catalogue\"*** and then ***\"or "
 "maybe just a page from a catalogue with a grid of the parts, image description etc\"***. ⇒ "
 "**The lane delivered the OPEN BOOK (`notes/_lanes/289/illustration/catalogue.html`) and the "
 "FLAT PAGE with a grid of parts is not drawn.** It replaces the books on v10's s6 when it "
 "lands. Receipt: `notes/_lanes/289/DAVE-RULINGS-2026-09-20.md` § While the catalogue lane ran.",

 "⬛ **③ PROPOSAL v3 IS OWED — THE PREMISE AS BEAT ZERO AND BOTH FRAMINGS SIDE BY SIDE** [NEW — "
 "0, DAVE'S] — the premise is HIS and is in no page yet: ***\"there is something at the start of "
 "this and its the bottleneck problem, we actually started with a premise, we noticed that the "
 "dev part of the process was speeding up, new philosophy, building fast and testing with real "
 "deliverable code, design became a bottleneck and the question we asked ourselves was how do we "
 "speed up design, this was the start of the first experiment. I'm not sure how to weave this "
 "in, but please note this.\"*** ⇒ **Noted, and OWED: beat zero, plus the seven beats, plus both "
 "framings, plus the record dated.** Receipt: `notes/_lanes/289/DAVE-RULINGS-2026-09-20.md` § "
 "The premise.",

 "⬛ **④ DECK v11 IS OWED AND THE FOUR D2 FLAGS ARE NOT ACTED ON** [NEW — 0, DAVE'S] — lane D2 "
 "declared them rather than fixing them: **s4 to s8 are five white cards in a row and the rhythm "
 "is flattened**, the **callipers fill half their card**, the **gearbox scale bar rides into the "
 "s10 Parts cell**, and the **brain frame is a hair heavier than the gearbox's**. ⇒ **A v11 is "
 "owed with the robots slide back on dark, and none of it moves before HIS slide-by-slide read "
 "of v10** — which he has not given. Receipts: `notes/_subreports/2026-09-20-289-D2-deck-v10.md` "
 "and `notes/_lanes/289/deck/BRIEF-v10.md`.",

 "⬛ **⑤ THREE ROLES OR FIVE CONSTITUENTS — HE RULED THAT BOTH BE EXPLORED AND PICKED NEITHER** "
 "[NEW — 0, DAVE'S] — verbatim: ***\"so i think theres two ideas going on here and maybe we are "
 "pulling in slightly different directions I'm seeing the visual metaphors as parts of the "
 "system whereas we are also describing the parts of the metaphor. Thre is no harm in exploring "
 "these both, when the assets are created we can use them as we like. I agree that the three "
 "parts are simpler, but the 5 explain more fully what the constituents are.\"*** ⇒ **THREE "
 "roles (inventory, assembly engineer, inspector) against FIVE constituents (knowledge/books, "
 "proficiency/brain, parts/gears, tools/arm, process/line), v10 carrying both, and WHICH ONE "
 "LEADS is his.** Receipt: `notes/_lanes/289/DAVE-RULINGS-2026-09-20.md` § On the two ideas.",

 "⬛ **⑥ THE ASK SLIDE IS A DRAFT SLOT AND THE RESEARCH STRAND IS ANOTHER GROUP'S** [NEW — 0, "
 "DAVE'S] — beat seven in his own words is one sentence: ***\"I need to work with mu colleagues "
 "on this request\"***, so the ask is a SLOT and not copy. And the research half is explicitly "
 "not ours to own: ***\"the research part is something another group is working on, i may be "
 "helping them with it but it is definitely a problem we have to solve\"*** ⇒ **it belongs ON the "
 "ask slide as owed, and the deck must not claim it.** Receipts: "
 "`notes/_lanes/289/DAVE-RULINGS-2026-09-20.md` § Beat 07 and `…-2026-09-19.md` § On the arc.",

 "⬛ **⑦ THE WEEK'S PLAN IS RULED AND NOT ONE DAY OF IT HAS RUN** [NEW — 0, DAVE'S] — his word on "
 "the strand map's path was ***\"this plan is fine , we will try and get ahead of it though\"***, "
 "and the path names Monday's overview-dashboard definition plus the first cold one-shot, "
 "Thursday's rehearsal and the recorded fallback. ⇒ **#289 spent both days on the story and the "
 "drawings, so the plan is intact and unstarted, with the internal Friday six days out from his "
 "order and now five.** ⚠ **Nothing here is a wrap's to schedule.** Receipts: "
 "`notes/_STRAND-MAP-2026-09-19.html` § THE PATH and "
 "`notes/_lanes/289/DAVE-RULINGS-2026-09-19.md`.",

 "⬛ **⑧ INDEX SHARDING BY STRAND AND AGE IS HIS PICK, NOT INSCRIBED AND NOT STARTED** [NEW — 0, "
 "DAVE'S] — he asked the question himself at the strand map's supporting strand — ***\"do we have "
 "any ideas how to solve this, could we split the index, categorise of something?\"*** — and then "
 "took the conductor's option: **shard by strand plus age** (hot equals the last ten sessions, "
 "cold beyond it, per-strand shards, the cloud archive rolling to the repo). ⛔ **A PICK IS NOT A "
 "RULING — he did not say *inscribe*, so it is carried as a question put** (`s271-D4`), and the "
 "memory-index cap it exists to relieve is still 49,152 B with the archive at 162 B of headroom. "
 "Receipt: `notes/_lanes/289/DAVE-RULINGS-2026-09-19.md` § Follow-up item three.",

 "⚠ **⑨ THE LIBRARY FIGURE HAS TWO READINGS AND HE RULED WHICH ONE THE STORY TELLS** [NEW — 0] — "
 "**his:** ***\"the count is 36 in the figma library, this is fine I think that the 36-137 is a "
 "good story with out confusing anything, 101 new components\"*** and ***\"137 - 125 components, "
 "12 templates and 8 foundations, and we see this growing\"***. **The repo's:** 32 real component "
 "metas at `87a71e4f` on 2026-06-18, and about 38 at the build-out proposal in "
 "`knowledge/_COMPONENT-LIBRARY-TARGET.md`. ⇒ **36 is the FIGMA count and is his story's figure; "
 "32 is what this repository can show; both stand and neither is rewritten** "
 "[[measure-dont-convert-units]]. ⚠ **A deck or proposal that cites 36 is citing HIM and should "
 "say so.** Receipts: `notes/_subreports/2026-09-19-289-H1-library-buildout-numbers.md` and "
 "`…-H2-library-buildout-story.md`.",

 "⚠ **⑩ THE GAUGE WAS NEVER READ AT THE CONDUCTOR'S SEAT AND THE WINDOW CLOSED AT 435,910 REAL** "
 "[NEW — 0] — **measured at this seat by importing `_checkin.read_fill` against the conductor's "
 "own transcript: FILL 435,910 real across 133 turns, peak the same, boot 74,174, zero "
 "compactions and zero drops.** ⛔ **The 180,000 quality line is passed by 255,910 and the "
 "256,000 tolerance by 179,910 — the largest overrun this record carries.** ⛔ **The cause is "
 "structural and is named rather than blamed: the boot `_checkin.py --no-block` output was never "
 "captured to a file, the conductor declared the gauge UNREAD in his own brief, and the wrap was "
 "called on Dave's sentence *\"btw you're getting hot I think\"* rather than on an instrument.** "
 "⇒ **The in-flight stop line cannot fire when nothing reads it** "
 "[[instrument-without-a-consumer]]. ⚠ **What to do about a seat that cannot see its own gauge "
 "is Dave's.**",

 "⚠ **⑪ THE `subs` FIGURE HAS A DECLARED SIDE AND A MEASURED SIDE AND FIVE LANES ARE "
 "UNACCOUNTED** [NEW — 0] — the conductor **DECLARED twenty lanes summing 2,813,762 real**, every "
 "one an `Agent` at `spawnDepth 1`, model opus, none in seat. **MEASURED here: sixteen "
 "sub-transcripts exist on disk beneath the conductor's session, one of which is this wrap seat, "
 "so FIFTEEN lane transcripts are readable and `_checkin.read_fill` sums them at 2,336,973.** ⛔ "
 "**The five-lane gap is NOT attributed and no third number is minted** — whether those seats "
 "were pruned, re-used or counted under a different convention is not establishable from this "
 "seat [[feedback-measuring-tool-must-not-guess]]. ⚠ **The `subs` line in the stratum carries the "
 "DECLARED figure and says so**, the convention the log has used since #284.",

 "⚠ **⑫ #288 PREDICTED THAT ITS OWN STRATUM WOULD NOT MANUFACTURE AN EIGHTH GATE FAIL, AND THE "
 "PREDICTION WAS TESTED RATHER THAN TRUSTED — IT HELD** [NEW — 0] — #288 labelled it a "
 "prediction: *\"#289's roll should not add an eighth.\"* **A raw text count at this seat looked "
 "like a falsification — #288's post-mortem half mentions its first-turn figure THREE times**, "
 "as the reading, as a comparison against `BOOT_CEILING_TK`, and inside a three-reading spread. "
 "⇒ **The raw count is the WRONG INSTRUMENT: `_parse_boot_samples` takes at most ONE reading per "
 "LINE, treats the `N over the band` shape as a COMPARISON, and requires the word boot adjacent "
 "to the number.** Run over the exact text the roll would append, it yielded **one row for #288, "
 "not three**, and the check after the roll landed still reads **six** double-counts. ✅ **The "
 "prediction held and the structural fails stayed at seven.** ★ **The lesson is about method: a "
 "grep for a figure is not the gate's reading of it, and a wrap that had published the grep "
 "would have inscribed a false alarm about another session's testimony** "
 "[[measure-dont-convert-units]].",

 "⚠ **⑬ ALL FOURTEEN FILED LANE REPORTS BREAK `s218-D7` CLAUSE 4, AGAINST #288'S FOUR OF FIVE** "
 "[NEW — 0] — measured at this seat by grep over all fourteen: **zero carry a `RULING-SHAPED "
 "QUESTIONS` heading, zero carry a `COUNTS:` line, zero carry a `REPLAY-THESE:` line.** ⛔ **The "
 "CONTENT is present in nearly every one**, under names like *What I wrote*, *What moved*, "
 "*Approach* and *Caveats* — **what is missing is the NAME the gate and the next reader look "
 "for**, and `subreport_citation_check` parses exactly those. ⛔ **NOT REPAIRED — a wrap does not "
 "edit another seat's filed report**, which is dated history (`ADR-0017` and `s192-D1`). ★ **Two "
 "consecutive wraps have measured this with the rate getting WORSE, which is evidence about the "
 "brief TEMPLATE rather than about the lanes.**",

 "⚠ **⑭ FIVE DRAWING AND DECK CAVEATS ARE CARRIED RATHER THAN BURIED** [NEW — 0] — declared by "
 "the lanes that drew them: the **brain's top and front views still read narrower than a real "
 "brain** (the traced profile is tall), the **line scene's far arm can read as floating at yaw "
 "extremes**, the **callipers' jaws read wedge-like**, the **deck's graph figures are stale** "
 "(2,837 on the slide against 4,820 today, carried from #288 and not fixed), and **his own "
 "verdict on the brain was *\"okay this is good for now\"*, which is an acceptance with a clock "
 "on it rather than a finished drawing.** ⚠ **None is a defect anyone has ruled** and none is "
 "fixed here. Receipts: the six `notes/_subreports/2026-09-20-289-I*` reports.",

 "⚠ **⑮ THE STRAY POLICY MET A FILE OUTSIDE THE REPOSITORY AND THE MOVE WAS DECLINED WITH ITS "
 "REASON** [NEW — 0] — `rm` and `git checkout --` are blocked on this mount, so the eight trial "
 "renders `notes/_lanes/289/illustration/var-*.png` went to `_to_delete/289-strays/` by `mv`, "
 "the #284 to #288 precedent. ⛔ **`crop.png` and four siblings were NOT moved: they live in the "
 "session OUTPUTS mount, outside the repository, were never tracked and are not staged, and "
 "moving them in would import scratch into the record to satisfy a sentence in a brief.** ⇒ "
 "**Declared deviation, published rather than quietly obeyed.** ⛔ **`_to_delete/` is still an "
 "accumulating squatter that step 4c does not reach and what to do about it is his.**",

 "⚠ **⑯ THE DECISIONS-AND-COMMENTS OVERLAY IS LIVE MACHINERY WITH NO HOME, AND HIS "
 "CROSS-COMMUNICATION QUESTION IS STILL UNANSWERED** [NEW — 0] — "
 "`notes/_lanes/289/decisions-overlay/inject.py` injects a per-section verdict and comment panel "
 "that EXPORTS `DAVE-RULINGS-<date>-<page>.md`, it was injected into four pages he rules from "
 "(the strand map, the #288 template quality review and both proposals), **and he used it three "
 "times — which is why both of this session's `DAVE-RULINGS` files are verbatim rather than "
 "transcribed.** ⛔ **It has no runbook line, no gate, no store row of its own and lives in a "
 "lane directory**, so the next session that wants a rulable page has to find it. ⚠ **And the "
 "question that survives #288's struck item ④ rides here: *\"can parallel agents cross "
 "communicate rather than having solo lanes that report to the orchestrator?\"* — put at #288, "
 "unanswered at #289.**",
]

for old, new in STRIKES:
    assert aged.count(old) == 1, f"headline did not match exactly once: {old[:70]!r}"
    aged = aged.replace(old, new + " " + old, 1)

head, body = aged.split(":**", 1)
assert head == "> **residual → #289", repr(head)
newline = "> **residual → #290:** " + " · ".join(NEWITEMS) + " · " + body.strip()

after = len(cg._carry_items(newline))
print(f"carries: #289 {before} items  ->  #290 {after} items   "
      f"(+{after - before}; {len(NEWITEMS)} new written, {len(STRIKES)} struck, "
      f"{n_new} items written NEW into the #289 section (by the #288 wrap) aged in)")

# ---- splice the new section in, NEWEST FIRST ---------------------------------------------------
ANCHOR = "## residual → #289"
assert text.count(ANCHOR) == 1
block = "## residual → #290\n\n" + newline + "\n\n" + ANCHOR
out = text.replace(ANCHOR, block, 1)
assert out.count("## residual → #290") == 1
assert src in out, "POST-CONDITION FAILED: the #289 line did not survive verbatim"

if "--write" in sys.argv:
    open(CARRIES, "w", encoding="utf-8").write(out)
    print("WROTE _CARRIES.md § residual → #290")
else:
    print("DRY — pass --write to land it")
