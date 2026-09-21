#!/usr/bin/env python3
"""#292 wrap — build `_CARRIES.md` § `## residual → #293` from § `## residual → #292`.

ONE programmatic pass, the #261…#291 shape:
  (a) every age bracket bumped by one — `[NEW — 0…]` → `[1…]`, `[N…]` → `[N+1…]`;
  (b) ⛔ ZERO STRIKES, AND THE ZERO IS A JUDGMENT WITH A REASON RATHER THAN AN OVERSIGHT;
  (c) NINE new items in front, newest first.
⛔ Nothing is dropped, re-worded, re-ordered or truncated. `s225-D2` clause (i).

★ WHY THERE IS NO STRIKE HERE, and it is not the same as there being nothing to strike.

  The brief names ONE strike for this wrap: #291's OWED item 6, the `_drive_chart_engine.py`
  re-drive that clears the release CI red. **That item lives in `_HANDOFF-142`'s OWED list, and
  it is struck THERE, in `_HANDOFF-143`, with its receipt.** It has no numbered carry of its own
  in this file: searched at this seat over all 611 items of § `residual → #292` for
  `_drive_chart_engine`, `re-drive`, `release CI red` and `release red` — the four hits are
  other carries' prose (an #260 strike body, #258's gate-report carry, a #260 scatter receipt)
  and NOT a carry whose HEADLINE is the re-drive. `s183-D1` strikes a HEADLINE and never a
  clause, so there is nothing in this file the strike may touch [[unmatched-grep-is-not-an-absence]].

  ⛔ AND THE OTHER TWO CANDIDATES ARE DELIBERATELY NOT STRUCK.
  · #291's OWED item 1 — his slide-by-slide read of v12 — is **HALF**: he has READ it
    (*"I've gone through it and I want to make changes"*) and his notes are NOT yet given, so
    the four D2 layout flags and the dark robots slide are still gated. A half-true headline is
    carried and the change is minted as a NEW item (①), never struck.
  · #291's OWED item 3 / this file's `residual → #292` item ② — Parts on slide 10 being the
    gearbox or the catalogue — got his answer *"The cogs are fine for now"*. ⛔ **THE `s188-D2`
    STRIKE FORM REQUIRES THE RETRACTION TO NAME WHERE THE CORRECTION IS INSCRIBED, AND NOTHING
    WAS INSCRIBED: `knowledge/_rulings.json` stays at 622 and he did not say *inscribe*.** An
    explicitly provisional acceptance by eye with no inscription to point at cannot satisfy that
    clause, so the item is CARRIED with his words recorded on the new item ⑦ instead.
    *"A strike that is wrong is worse than an item that is merely stale"* (`s271-D4`).
"""
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
CARRIES = os.path.join(ROOT, "_CARRIES.md")
sys.path.insert(0, os.path.join(ROOT, "knowledge"))
import _capture_gate as cg  # the ONE definition of "a carry"

text = open(CARRIES, encoding="utf-8").read()
src = [l for l in text.split("\n") if l.startswith("> **residual → #292:**")]
assert len(src) == 1, len(src)
src = src[0]
before = len(cg._carry_items(src))

# ---- (a) ages -------------------------------------------------------------------------------
n_new = len(re.findall(r"\[NEW — 0(?=[,\]])", src))
aged = re.sub(r"\[(\d+)(?=[,\]])", lambda m: "[%d" % (int(m.group(1)) + 1), src)
aged = re.sub(r"\[NEW — 0(?=[,\]])", "[1", aged)
assert "[NEW — 0" not in aged

# ---- (b) NO STRIKES — see the module docstring ------------------------------------------------
STRIKES = []

# ---- (c) the session's NINE new items ---------------------------------------------------------
# ⚠ ① IS LOAD-BEARING: `_gen_titles.py` derives NEXT-TITLE from the FIRST ⬛ bullet's bolded
#   clause on the banner's pointer line, and `title_generation_check()` is BLOCKING.
# ⚠ NO bare " · " inside an item (it is the carry set's own split token) and NO `[N]` bracket in
#   prose (it reads as a second age). Ages spelled in words.
NEWITEMS = [
 "⬛ **① HIS v12 AND v13 NOTES ARE PREPARED AND NOT YET GIVEN, AND THE FOUR D2 FLAGS AND THE "
 "DARK ROBOTS SLIDE ARE GATED ON THEM** [NEW — 0, DAVE'S] — his first sentence of the session "
 "was ***\"I've gone through it and I want to make changes\"***, and the changes were to come as "
 "notes he was preparing while the lanes ran. ⛔ **THE NOTES NEVER ARRIVED IN THIS WINDOW.** ⇒ "
 "**The slide-by-slide read is DONE and its OUTPUT is owed, which is a different state from "
 "#291's \"he has not read it\" — so #291's owed item 1 is HALF and was NOT struck.** The four "
 "D2 layout flags and the dark robots slide stay exactly as they were, untouched across v10, "
 "v11, v12 and now v13, **because they are gated on notes only he can give.** ⚠ **They are now "
 "owed against a deck that has moved twice since he read it: v13 carries the design-system map "
 "at `s10map` and v12 carried the workers and the three-up slide 10.** Receipts: "
 "`notes/_lanes/292/DAVE-RULINGS-2026-09-21.md` lines 3–8, "
 "`notes/_DEMO-SLIDES-apollo-2026-09-21-v13.html`.",

 "⬛ **② THE BRAIN IS INLINE WITH ITS TRAY AT MINUS FIFTY AND THE PLATE QUESTION IS OPEN** [NEW "
 "— 0, DAVE'S] — three more passes in one day, every one ruled by his eye alone: **lane B's rest "
 "angle (YAW0 10→35, PIT0 8→20) was REJECTED** — ***\"the cogs and books were fine as they "
 "were\"*** — **lane B2 turned the tray to the gearbox's angle with the back towards us** (YAW0 "
 "+35→−35, AOV 12→33) and offered a −50 alternate, **he took the ALTERNATE** — ***\"two up alt "
 "is better but we need to orientate the brain so its inline with the tray as it was before, but "
 "this is the right angle\"*** — **and lane B3 landed it with ONE constant, YAW0 −35→−50.** ⬛ "
 "**THE OPEN QUESTION IS THE PLATE: it no longer sits at the gearbox's literal −35, which was "
 "his own earlier ask, because \"inline\" and \"the alternate's body angle\" cannot both hold "
 "with the plate pinned — they are the same axis.** The alternate that keeps the plate at −35 is "
 "`notes/_lanes/292/B3/alt-body-23-tray-35.png` (tray −35, body −23.43, screen residual 0.01 "
 "degrees) and it costs an 11.6-degree plan split and a second view matrix. ⇒ **Dave: plate "
 "follows the body to −50 as shipped, or plate holds the cogs' −35 and the brain turns 11.6 "
 "degrees in its own axes?** ⚠ **NOT INSCRIBED — the rulings store stays at 622** (`s271-D4`). "
 "Receipts: `notes/_lanes/292/DAVE-RULINGS-2026-09-21.md`, commits `d5a0eb8c` and `34814ca5`, "
 "`notes/_subreports/2026-09-21-292-B-brain-rest-angle.md`, `…-292-B2-brain-tray-and-back.md`, "
 "`…-292-B3-brain-inline-with-tray.md`.",

 "⬛ **③ THE WORKERS NEED FINESSING AND HE SAID IT IS TO BE DONE TOGETHER, NOT BY A LANE ALONE** "
 "[NEW — 0, DAVE'S] — verbatim: ***\"The workers just need some finessing, we'll work on that "
 "together.\"*** ⇒ **This ANSWERS #291's open question about what the *\"almost\"* was, in the "
 "only way it could be answered — not by itemising it, but by saying the itemising is a joint "
 "act.** ⛔ **It is therefore NOT a lane brief and must not be turned into one: a lane cut "
 "against this sentence would be doing alone the thing he said would be done together.** ⚠ "
 "**NOT INSCRIBED and the store stays at 622, so this is a question put rather than a state of "
 "the world** (`s271-D4`). Receipt: `notes/_lanes/292/DAVE-RULINGS-2026-09-21.md` line 5.",

 "⬛ **④ THE DASHBOARD REVIEW IS DEFERRED AND THE NEXT ONE-SHOT RUNS ON THE DEMO'S COLD BRIEF, "
 "NOT THE AI-PLATFORM ONE** [NEW — 0, DAVE'S] — verbatim: ***\"We need time to go over the "
 "dashboard, next time can we use the cold brief we will be doing the demo with rather than the "
 "Ai platform one\"***. ⇒ **TWO things, and the second is a STANDING NOTE for #293 rather than a "
 "question**: the review of lane D's definition and first cold one-shot is his and is deferred, "
 "and **the NEXT one-shot is to be run against the brief the demo itself will use.** ⛔ **WHICH "
 "brief that is has not been named to the record and is not guessed at here** — the frozen demo "
 "prompt was declared NOT RECOVERABLE from the record at #288, so this note needs his pointer "
 "before a lane can obey it. Receipts: `notes/_lanes/292/DAVE-RULINGS-2026-09-21.md`, "
 "`notes/_subreports/2026-09-21-292-D-overview-dashboard.md`, "
 "`notes/_lanes/292/D/overview-dashboard-definition.html`, "
 "`notes/_lanes/292/D/overview-dashboard-oneshot-v1.html`.",

 "⬛ **⑤ THE RECEIPT FRESHNESS CHECK HAS NO RUNNER, SO A CANON EDIT STAYED INVISIBLE FOR FOUR "
 "SESSIONS** [NEW — 0, DAVE'S] — lane C cleared the release red and the root cause was **not a "
 "chart change at all**: `knowledge/canon/canon.css` moved at `71b3363c` after #288, against "
 "chart-engine receipts last measured at #268 — **13 hashes stale, and NOT ONE MEASUREMENT "
 "CHANGED when they were re-taken.** ⛔ **`_drive_chart_engine.py --check` is in neither "
 "`_build_all.STEPS` nor any CI step, so the FIRST thing that said the receipts were stale was "
 "the release job, four sessions later.** ⇒ **Dave: should `--check` be wired as a step, and if "
 "so BLOCKING or ADVISORY?** ⚠ **A second thing rides with it and is named rather than "
 "bundled: the re-drive silently moved the measuring browser from Chromium 151 to 153, a major "
 "bump, and nothing in the repo grades that — the receipt records the version and no gate reads "
 "it, while the receipt is evidence for a BLOCKING dv-004 verdict.** Receipts: "
 "`notes/_subreports/2026-09-21-292-C-chart-engine-redrive.md`, commit `bc7f3b79`, CI run "
 "`35588407818` on `6751fdeb`.",

 "⬛ **⑥ THE DESIGN-SYSTEM MAP IS A PLACEHOLDER BY HIS OWN WORD AND ITS TWO FADED TILES ARE "
 "UNEXPLAINED** [NEW — 0, DAVE'S] — from his hub-and-spoke reference (image READ, NOT FILED, the "
 "#289 precedent) lane H built the Swiss poster with **10 tiles HAVE and 2 COMING SOON**, and "
 "his verdict was ***\"the design system map is good for now as a placeholder, we'll refine "
 "later. we can slot it after slide 10\"***. ⬛ **The two faded tiles are the question: CX "
 "Principles has at least a parked item in `knowledge/_parked.json` pointing at it, so \"coming\" "
 "has footing, but for User Research and Insights there is NOTHING in the repo at all — it may "
 "be a genuine gap or something Apollo deliberately does not own, and the badge asserts intent "
 "either way.** ⚠ **Two more of lane H's are open with it: whether a badged tile carries a date "
 "or an owner (a badge with no date is a promise with no receipt), and whether \"Data and "
 "Insights\" means the system measuring itself, as the lane read it, or product analytics about "
 "users, which Apollo does NOT have and which would move the split to nine and three.** ⚠ **NOT "
 "INSCRIBED — accepted as a placeholder is not an inscription and the store stays at 622.** "
 "Receipts: `notes/_subreports/2026-09-21-292-H-design-system-map.md`, "
 "`notes/_lanes/292/H/design-system-map.html`.",

 "⬛ **⑦ SLIDE 10 PARTS IS THE GEARBOX *FOR NOW* — HIS ANSWER CAME AND IT IS NOT AN INSCRIPTION** "
 "[NEW — 0, DAVE'S] — **`residual → #292` item ② asked which of his two instructions he meant, "
 "and he answered: *\"The cogs are fine for now.\"*** ⇒ **The gearbox stands in the Parts cell "
 "and the catalogue stays on slide 6.** ⛔ **THE ITEM IS CARRIED RATHER THAN STRUCK, AND THE "
 "REASON IS THE STRIKE FORM ITSELF: `s188-D2` requires a retraction to name WHERE THE CORRECTION "
 "IS INSCRIBED, and nothing was inscribed — `knowledge/_rulings.json` stays at 622 and he did "
 "not say *inscribe*.** An explicitly provisional acceptance by eye has no inscription to point "
 "at, so it cannot satisfy that clause, and **a strike that is wrong is worse than an item that "
 "is merely stale** (`s271-D4`). ⇒ **Whether *\"for now\"* ever becomes a ruling is his.** "
 "Receipt: `notes/_lanes/292/DAVE-RULINGS-2026-09-21.md` line 6.",

 "⚠ **⑧ THE DECK IS THREE PASSES BEHIND ITS OWN BRAIN AND THE COUNTER READS TEN-A OF TWELVE ON "
 "THIRTEEN CARDS** [NEW — 0, DAVE'S] — measured at this seat in v13: the deck inlines the brain "
 "at `YAW0 = 10` / `PIT0 = 8` and `AOV = 12` while `notes/_lanes/289/illustration/brain.html` "
 "now rests at **−50 / 20 / 33**. ⛔ **v13 does NOT carry lane B3's brain, and that was not an "
 "oversight — moving a deck constant is a deck edit and no lane was cut for it.** ⚠ **And the "
 "new map card brought a counter question with it: the deck now has THIRTEEN cards and every "
 "existing one still reads NN of twelve while the new one reads ten-A of twelve, so either that "
 "stands or a mechanical sweep renumbers all thirteen — and if it does, whether the id `s10map` "
 "follows into the sequence or stays a name is the second half.** ⇒ **Both are his.** Receipts: "
 "`notes/_subreports/2026-09-21-292-P4-deck-v13-map-slide.md`, "
 "`notes/_subreports/2026-09-21-292-B3-brain-inline-with-tray.md`, "
 "`notes/_DEMO-SLIDES-apollo-2026-09-21-v13.html`.",

 "⚠ **⑨ THE SEAM CHECK WAS OVERRIDDEN ONCE AND THEN OBEYED FOR A SECOND CONSECUTIVE SESSION, AND "
 "NO RULE IS INVENTED FROM n EQUALS TWO** [NEW — 0, DAVE'S] — the reading **FILL 180,850 real "
 "over 18 turns, STOP LINE PASSED** was quoted to him, **his answer was one more note** (the "
 "brain inline with its tray), lane B3 ran, and the wrap came on ***\"wrap when you're "
 "ready\"***. ⇒ **#283 and #290 stopped ON the instrument; #291 and #292 each overrode it "
 "exactly once with a note and then obeyed — the SAME shape twice, which is an observation and "
 "not a pattern.** ⚠ **The override was CHEAP this time and that is part of the datum: #291's "
 "override cost 44,412 real and #292's cost 7,391.** ⛔ **This is evidence about `s283-D1`'s "
 "tolerance arm and NOT an argument for or against making it blocking — a blocking arm would "
 "have refused a lane Dave asked for, both times.** Receipt: this wrap's ⏱ LATEST DELTA and "
 "`notes/_subreports/2026-09-21-292-W-wrap.md`.",

 # ⑩ IS THIS WRAP'S 2d EXIT-CHECK CATCH, copied up BEFORE the #289 delta was allowed to roll.
 "⬛ **⑩ DREAM PASS 13 — SEVEN PROPOSALS FLOATED, ZERO RULED, AND IT HAD NO STANDING HOME UNTIL "
 "THIS LINE** [NEW — 0, DAVE'S] — put to Dave at the wrap call. The scheduled pass fired "
 "mid-session on 2026-09-20 at 11:42 BST (commit `dcf17ade`, *\"Dave absent\"*) while #289 was "
 "running: **seven proposals floated, zero ruled — the dreamer cannot rule and did not** — and "
 "**P1's stale B3 sidecar has printed at every session boot since.** ⛔★★ **THIS ITEM IS THIS "
 "WRAP'S 2d EXIT-CHECK CATCH AND IS COPIED UP HERE BEFORE THE #289 ⏱ DELTA WAS ALLOWED TO "
 "ROLL.** It had been carried on the #289, #290 and #291 ⏱ deltas — **all three of them rolling "
 "surfaces** — and probed at this seat against all 611 items of `residual → #292` for *dream "
 "pass 13*, *dream 13*, *dream-13* and *seven proposals*, it resolved to **none**; dream pass "
 "**12** has a carry (age twenty-five) and pass **11** has two, so the gap was pass 13's alone "
 "[[unmatched-grep-is-not-an-absence]]. ⇒ **Without this line the seven would have left live "
 "state the moment the #289 delta moved to the archive — the exact failure the EXIT CHECK "
 "exists to prevent** [[feedback-header-wins-over-audit]]. Bodies: `notes/_dream/` "
 "(`_GRADE-DECISIONS.jsonl`, the dated pass note), commit `dcf17ade`.",
]

# ---- assemble ---------------------------------------------------------------------------------
body = aged[len("> **residual → #292:** "):]
for old, new in STRIKES:
    assert body.count(old) == 1, f"STRIKE anchor not unique ({body.count(old)}): {old[:70]}"
    body = body.replace(old, new + " " + old, 1)

line = "> **residual → #293:** " + " · ".join(NEWITEMS) + " · " + body
after = len(cg._carry_items(line))

HEAD = "## residual → #293"
assert HEAD not in text, "§ residual → #293 already exists — refusing to write it twice"
anchor = "## residual → #292"
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
