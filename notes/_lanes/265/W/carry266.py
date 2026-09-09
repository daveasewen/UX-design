#!/usr/bin/env python3
"""#265 wrap — build `_CARRIES.md` § `## residual → #266` from § `## residual → #265`.

ONE programmatic pass, the #261…#264 shape:
  (a) every age bracket bumped by one — `[NEW — 0…]` → `[1…]`, `[N…]` → `[N+1…]`;
  (b) TWO surgical edits, each asserted UNIQUE before it is made, by ADDITION with an
      `s183-D1`/`s188-D2` receipt and the original wording left standing verbatim beneath;
  (c) the session's SEVEN NEW items written in front.

⛔ Nothing is dropped, re-worded, re-ordered or truncated. `s225-D2` clause 1.
"""
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
CARRIES = os.path.join(ROOT, "_CARRIES.md")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "knowledge"))
import _capture_gate as cg  # noqa: E402  — the ONE definition of "a carry"

text = open(CARRIES, encoding="utf-8").read()
lines = text.split("\n")
src = [l for l in lines if l.startswith("> **residual → #265:**")]
assert len(src) == 1, len(src)
src = src[0]
before = len(cg._carry_items(src))

# ---- (a) ages -------------------------------------------------------------------------------
n_new = len(re.findall(r"\[NEW — 0(?=[,\]])", src))
n_num = len(re.findall(r"\[(\d+)(?=[,\]])", src))
aged = re.sub(r"\[(\d+)(?=[,\]])", lambda m: "[%d" % (int(m.group(1)) + 1), src)
aged = re.sub(r"\[NEW — 0(?=[,\]])", "[1", aged)
assert "[NEW — 0" not in aged

# ---- (b) the TWO strikes, each asserted UNIQUE -------------------------------------------------
EDITS = [
    # ① the #265 lead — its /goal half is DISCHARGED; the four ungraded glyphs half is NOT and is
    #    re-carried in front as this session's item ①. Partial strike, the #264 ⑥ precedent.
    ("⬛ **① THE /goal BITE-TEST, AND THE FOUR UNGRADED GLYPHS** [1, DAVE'S]",
     "⬛ **① ~~THE /goal BITE-TEST~~, AND THE FOUR UNGRADED GLYPHS** [1, DAVE'S] ⛔ **HALF STRUCK AT "
     "#265 WITH ITS `s183-D1`/`s188-D2` RECEIPT: THE `/goal` BITE-TEST WAS BUILT, DRIVEN AND RULED. "
     "THE FOUR UNGRADED GLYPHS ARE UNTOUCHED AND ARE RE-CARRIED IN FRONT AS #265's ITEM ①.** "
     "`knowledge/_bite_goal.py` emits an INTACT `COPILOT-BOOT.md` and a MUTATED copy with option 3's "
     "five-line `/goal` clause stripped (the strip is ASSERTED), plus a 4-turn scenario; two blind "
     "Opus lanes each played the assistant from ONE boot and the grades read **INTACT GREEN (2/2), "
     "MUTATED RED (1/2)**. ⇒ **the clause is load-bearing on exactly one arm — G2, holding the goal "
     "against a drift** (with it, T2's *\"just build me a transactions list\"* was checked against "
     "*make rent* by name and re-shaped; without it the list was built and the drift was absorbed, "
     "never named). **G1 (confirm before build) is NOT this clause's — it is rule 7a's bento "
     "question and passed in BOTH arms**, and **G3 is un-regexable**. Receipts: commit `9a24af9` · "
     "`s265-D1` (STANDALONE instrument, not a `test_gates.py` CASE — Dave: *\"1. okay make it stand "
     "alone\"*) · `s265-D2` (G3 graded RUBRIC-ONLY — Dave: *\"2. okay yes\"*) · "
     "`notes/_subreports/2026-09-09-265-G-goal-bite-test.md`. ⚠ **Its stability is UNPROVEN and is "
     "carried as this session's item ⑤.** The original wording stands verbatim below."),
    # ② the fail-open venue — nothing tested that the pack holds a goal. It does now.
    ("⬛ **③ NOTHING TESTS THAT THE PACK HOLDS A GOAL ACROSS A SESSION — THE SIXTH VENUE OF THE "
     "FAIL-OPEN CLASS [3, DAVE'S]**",
     "⬛ **③ ~~NOTHING TESTS THAT THE PACK HOLDS A GOAL ACROSS A SESSION — THE SIXTH VENUE OF THE "
     "FAIL-OPEN CLASS~~ [3, DAVE'S] ⛔ STRUCK AT #265 WITH ITS `s183-D1`/`s188-D2` RECEIPT: "
     "SOMETHING TESTS IT NOW, AND WHAT IT FOUND IS NARROWER THAN THE CARRY ASSUMED.** "
     "`knowledge/_bite_goal.py` (commit `9a24af9`) is a mutation test on the CLAUSE, not on the "
     "feature: strip option 3's `/goal` span from `apollo-spider/cold-start/COPILOT-BOOT.md` and "
     "the pack stops holding the goal — **MUTATED RED on G2**, INTACT GREEN, two blind Opus drives "
     "filed as assets. ⇒ **the fail-open venue is CLOSED for the HOLD clause.** ⚠ **And the test "
     "narrowed the claim, which is the finding:** *confirm before build* passed in BOTH arms (it "
     "belongs to rule 7a, not to `s262-D5`), and *report against the goal* cannot be told apart by "
     "regex — both arms name the goal at T4 — so `s265-D2` grades it **RUBRIC-ONLY** and the G3 arm "
     "is ADVISORY and never counted. ★ **[[no-gate-parses-the-artefact]] holds even for a "
     "transcript — halfway.** The original wording stands verbatim below."),
]
for find, repl in EDITS:
    assert aged.count(find) == 1, (aged.count(find), find[:90])
    aged = aged.replace(find, repl, 1)

# ---- (c) this session's new items -------------------------------------------------------------
NEW = open(os.path.join(HERE, "carry266-new.txt"), encoding="utf-8").read().strip()
line = "> **residual → #266:** " + NEW + " · " + aged[len("> **residual → #265:** "):]
after = len(cg._carry_items(line))

SECTION = [
    "## residual → #266",
    "",
    "*Written straight here at the #265 wrap (✅ **NO DATE SPLIT — session, ritual and commit are "
    "all 2026-09-09**) under `s225-D2` clause (i). Ages +1, wording unchanged, nothing dropped for "
    "being old; **two carries STRUCK, both by ADDITION and each with its `s183-D1`/`s188-D2` "
    "receipt**, the original wording standing verbatim beneath each — the #265 LEAD, whose `/goal` "
    "half was built, driven and ruled while its four-ungraded-glyphs half is untouched and "
    "re-carried in front (a PARTIAL strike, the #264 ⑥ precedent), and the fail-open venue that "
    "said nothing tests whether the pack holds a goal, which something now does. ⛔ **Dave was "
    "asleep for this wrap: NOTHING was ruled at this seat and every open question stays open in "
    "his name.***",
    "",
    "<!-- WRITTEN-FIRST: residual → #266 — the aged tail below the SEVEN new items is the #265 "
    "line put through ONE programmatic pass (`notes/_lanes/265/W/carry266.py`): %d age brackets "
    "bumped (%d of them `NEW — 0` → `1`), then 2 surgical edits each asserted UNIQUE before it was "
    "made (the two strikes above). Probe count at write time: %d. "
    "⚠ DECLARED, NOT DISCOVERED: the #265 item ① is struck in HALF — the strikethrough covers the "
    "`/goal` bite-test clause only and the four ungraded glyphs stand unstruck inside the same "
    "headline, because that half is still open and is re-carried as #265's item ①. -->"
    % (n_new + n_num, n_new, after),
    "",
    line,
    "",
    "---",
    "",
]
i = lines.index("## residual → #265")
out = lines[:i] + SECTION + lines[i:]
open(CARRIES, "w", encoding="utf-8").write("\n".join(out))
print("ages bumped: %d (%d were NEW — 0) · probe %d → %d · section written above line %d"
      % (n_new + n_num, n_new, before, after, i + 1))
