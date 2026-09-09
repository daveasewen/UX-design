#!/usr/bin/env python3
"""#262 wrap — build `_CARRIES.md` § `## residual → #263` from § `## residual → #262`.

ONE programmatic pass, the #261 shape:
  (a) every age bracket bumped by one — `[NEW — 0…]` → `[1…]`, `[N…]` → `[N+1…]`;
  (b) TWO surgical edits, each asserted UNIQUE before it is made, both by ADDITION with an
      `s183-D1`/`s188-D2` receipt and the original wording left standing verbatim beneath;
  (c) the session's NEW items written in front.

⛔ Nothing is dropped, re-worded, re-ordered or truncated. `s225-D2` clause 1.
"""
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
CARRIES = os.path.join(ROOT, "_CARRIES.md")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "knowledge"))
import _capture_gate as cg  # noqa: E402  — the ONE definition of "a carry"

text = open(CARRIES, encoding="utf-8").read()
lines = text.split("\n")
src = [l for l in lines if l.startswith("> **residual → #262:**")]
assert len(src) == 1, len(src)
src = src[0]
before = len(cg._carry_items(src))

# ---- (a) ages -------------------------------------------------------------------------------
n_new = len(re.findall(r"\[NEW — 0(?=[,\]])", src))
n_num = len(re.findall(r"\[(\d+)(?=[,\]])", src))
aged = re.sub(r"\[(\d+)(?=[,\]])", lambda m: "[%d" % (int(m.group(1)) + 1), src)
aged = re.sub(r"\[NEW — 0(?=[,\]])", "[1", aged)
assert "[NEW — 0" not in aged

# ---- (b) the two strikes, each asserted UNIQUE ------------------------------------------------
EDITS = [
    # ① v1.0.9 + the push — BOTH halves discharged this session.
    ("⬛ **① CUT v1.0.9 — THE SIX DASHBOARD COMPONENTS SHIP, AND THE PUSH [1, DAVE'S]**",
     "⬛ **① ~~CUT v1.0.9 — THE SIX DASHBOARD COMPONENTS SHIP, AND THE PUSH~~ [1, DAVE'S] "
     "⛔ STRUCK AT #262 WITH ITS `s183-D1`/`s188-D2` RECEIPT: BOTH HALVES ARE DISCHARGED.** "
     "**v1.0.9 IS RELEASED** — Dave's word *\"Ratify v1.0.9\"* inscribed as `s262-D6` (`33a6608`), "
     "`RATIFY_IDS` keyed at `3cab7c3`, `--release` at `b94adff` baking "
     "`736d0fb034b71048e0ef7789206837afa7ef76c33330117fa0be3410c149c780` byte-identical to lane "
     "O2's twice-proved dry run, `--check` GREEN at `dd129e8efa79`, frozen ledger re-seeded at "
     "`c0538c1`, **9/9 release gates green**. **AND THE PUSH RAN AT THE OPENER on his word** — "
     "`7647aaf..886e7e5`, **42 commits**, ff-only, verified with `git ls-remote`. "
     "⛔ **ONE HALF IS NOT STRUCK AND IS RE-CARRIED AS `→ #263` ITEM ④: `s133-D2` AND `s207-D1` "
     "STILL POINT DIFFERENT WAYS AT THE SAME ACT** — the push was unblocked by asking, not by "
     "resolving them. Receipts: `notes/_subreports/2026-09-09-262-W-release-and-wrap.md` · "
     "`_DECISION-HISTORY/2026-09-09-262-cut-v109-and-the-push.md` §§1,3. "
     "The original wording stands verbatim below. —"),
    # ② the three weight-bearing questions — ANSWERED; the other two halves re-carried.
    ("⬛ **② ELEVEN LANE RECOMMENDATIONS WERE DEFAULTED BY THE CONDUCTOR, AND THREE "
     "WEIGHT-BEARING QUESTIONS PLUS THE STAT CARD ARROW SEAT WERE PUT TO HIM UNANSWERED "
     "[1, DAVE'S]**",
     "⬛ **② ~~ELEVEN LANE RECOMMENDATIONS WERE DEFAULTED BY THE CONDUCTOR, AND THREE "
     "WEIGHT-BEARING QUESTIONS PLUS THE STAT CARD ARROW SEAT WERE PUT TO HIM UNANSWERED~~ "
     "[1, DAVE'S] ⛔ STRUCK AT #262 WITH ITS `s183-D1`/`s188-D2` RECEIPT: ALL THREE "
     "WEIGHT-BEARING QUESTIONS ARE ANSWERED, AND THE THIRD WAS ALREADY RULED.** "
     "The tile affordance → **`s262-D1`** (*\"the whole card could be the affordance but it may "
     "contain a link, not an underline though\"*) · the nav current-location colour in Supercharge "
     "dark → **`s262-D2`** (*\"a is fine\"*, option A off "
     "`reviews/REVIEW-262-nav-supercharge-dark-v1.html`) · the 24px dense floor → he said "
     "*\"check the rulings\"* and the check found it **ALREADY RULED at `s201-D2`/`s202-D1`**, "
     "so ⛔ **NOTHING WAS INSCRIBED FOR IT** — re-inscribing a standing ruling because a later "
     "session forgot it gives one rule two homes. "
     "⛔ **TWO HALVES ARE NOT STRUCK AND ARE RE-CARRIED AS `→ #263` ITEMS ① AND ②: the ELEVEN "
     "lane recommendations are STILL PROPOSED, never ruled, and were not put to him again; and "
     "the STAT CARD ARROW SEAT is STILL UNASKED.** "
     "The original wording stands verbatim below. —"),
]
for find, repl in EDITS:
    assert aged.count(find) == 1, (aged.count(find), find[:80])
    aged = aged.replace(find, repl, 1)

# ---- (c) this session's new items -------------------------------------------------------------
NEW = open(os.path.join(HERE, "carry263-new.txt"), encoding="utf-8").read().strip()
line = "> **residual → #263:** " + NEW + " · " + aged[len("> **residual → #262:** "):]
after = len(cg._carry_items(line))

SECTION = [
    "## residual → #263",
    "",
    "*Written straight here at the #262 wrap (✅ **NO DATE SPLIT — session, ritual and commit are "
    "all 2026-09-09**) under `s225-D2` clause (i). Ages +1, wording unchanged, nothing dropped for "
    "being old; **two carries STRUCK, both by ADDITION and both with their `s183-D1`/`s188-D2` "
    "receipts**, the original wording standing verbatim beneath each, and **four halves of those "
    "two re-carried as new items rather than vanishing with the strike**.*",
    "",
    "<!-- WRITTEN-FIRST: residual → #263 — the aged tail below the SEVEN new items is the #262 "
    "line put through ONE programmatic pass (`notes/_lanes/262/carry263.py`): %d age brackets "
    "bumped (%d of them `NEW — 0` → `1`), then 2 surgical edits each asserted UNIQUE before it "
    "was made (both strikes: v1.0.9 + the push, discharged · the three weight-bearing questions, "
    "answered). Probe count at write time: %d. -->" % (n_new + n_num, n_new, after),
    "",
    line,
    "",
    "---",
    "",
]
i = lines.index("## residual → #262")
out = lines[:i] + SECTION + lines[i:]
open(CARRIES, "w", encoding="utf-8").write("\n".join(out))
print("ages bumped: %d (%d were NEW — 0) · probe %d → %d · section written above line %d"
      % (n_new + n_num, n_new, before, after, i + 1))
