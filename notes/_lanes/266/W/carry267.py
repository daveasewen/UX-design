#!/usr/bin/env python3
"""#266 wrap — build `_CARRIES.md` § `## residual → #267` from § `## residual → #266`.

ONE programmatic pass, the #261…#265 shape:
  (a) every age bracket bumped by one — `[NEW — 0…]` → `[1…]`, `[N…]` → `[N+1…]`;
  (b) ONE surgical edit, asserted UNIQUE before it is made, by ADDITION with an
      `s183-D1`/`s188-D2` receipt and the original wording left standing verbatim beneath;
  (c) the session's NINE NEW items written in front.

⛔ Nothing is dropped, re-worded, re-ordered or truncated. `s225-D2` clause 1.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
CARRIES = os.path.join(ROOT, "_CARRIES.md")
sys.path.insert(0, os.path.join(ROOT, "knowledge"))
import _capture_gate as cg  # noqa: E402  — the ONE definition of "a carry"

text = open(CARRIES, encoding="utf-8").read()
lines = text.split("\n")
src = [l for l in lines if l.startswith("> **residual → #266:**")]
assert len(src) == 1, len(src)
src = src[0]
before = len(cg._carry_items(src))

# ---- (a) ages -------------------------------------------------------------------------------
n_new = len(re.findall(r"\[NEW — 0(?=[,\]])", src))
n_num = len(re.findall(r"\[(\d+)(?=[,\]])", src))
aged = re.sub(r"\[(\d+)(?=[,\]])", lambda m: "[%d" % (int(m.group(1)) + 1), src)
aged = re.sub(r"\[NEW — 0(?=[,\]])", "[1", aged)
assert "[NEW — 0" not in aged

# ---- (b) the ONE strike, asserted UNIQUE -------------------------------------------------------
EDITS = [
    # the #266 lead — its "PROPOSED LEAD" half is RETRACTED by Dave's park; the glyphs themselves
    # are still ungraded and are re-carried in front as this session's item ⑨. Partial strike,
    # the #264 ⑥ / #265 ① precedent.
    ("⬛ **① THE FOUR UNGRADED `-active` GLYPHS ARE STILL UNGRADED, AND THEY ARE THE SESSION'S "
     "PROPOSED LEAD** [1, DAVE'S]",
     "⬛ **① THE FOUR UNGRADED `-active` GLYPHS ARE STILL UNGRADED, AND ~~THEY ARE THE SESSION'S "
     "PROPOSED LEAD~~** [1, DAVE'S] ⛔ **HALF STRUCK AT #266 WITH ITS `s183-D1`/`s188-D2` RECEIPT: "
     "THEY ARE NO LONGER THE LEAD, BY DAVE'S OWN WORD AT THE #266 OPENER — *\"forget about these "
     "for now the glyph work is for another time when I have capacity, our focus is Apollo and the "
     "demo/presentation\"*.** ⚠ **THE OTHER HALF IS UNTOUCHED AND TRUE: the four are STILL "
     "UNGRADED**, they still sit on `notes/_REVIEW-264-active-glyphs-2.html`, nothing entered the "
     "library at #266, and they are re-carried in front as #266's item ⑨ marked **PARKED — not "
     "ruled, not struck**. Where the correction is inscribed: `_LIVE-STATE.md` ⏱ LATEST DELTA "
     "#266, `_DECISION-HISTORY/2026-09-10-266-kg-explorer-and-the-demo-pivot.md` § 1, and the ★ "
     "LATEST #266 banner. The original wording stands verbatim below."),
]
for find, repl in EDITS:
    assert aged.count(find) == 1, (aged.count(find), find[:90])
    aged = aged.replace(find, repl, 1)

# ---- (c) this session's new items -------------------------------------------------------------
NEW = open(os.path.join(HERE, "carry267-new.txt"), encoding="utf-8").read().strip()
line = "> **residual → #267:** " + NEW + " · " + aged[len("> **residual → #266:** "):]
after = len(cg._carry_items(line))

SECTION = [
    "## residual → #267",
    "",
    "*Written straight here at the #266 wrap (✅ **NO DATE SPLIT — session, ritual and commit are "
    "all 2026-09-10**) under `s225-D2` clause (i). Ages +1, wording unchanged, nothing dropped for "
    "being old; **ONE carry STRUCK IN HALF, by ADDITION and with its `s183-D1`/`s188-D2` "
    "receipt**, the original wording standing verbatim beneath — the #266 LEAD, whose *proposed "
    "lead* half was retracted by Dave's own park at this session's opener while its "
    "four-ungraded-glyphs half is untouched, still true, and re-carried in front marked PARKED "
    "(the #264 ⑥ / #265 ① precedent). ⛔ **Dave ruled nothing in the `_rulings.json` sense at #266: "
    "the store stands at 441 entries and every open question stays open in his name.***",
    "",
    "<!-- WRITTEN-FIRST: residual → #267 — the aged tail below the NINE new items is the #266 "
    "line put through ONE programmatic pass (`notes/_lanes/266/W/carry267.py`): %d age brackets "
    "bumped (%d of them `NEW — 0` → `1`), then 1 surgical edit asserted UNIQUE before it was "
    "made (the half-strike above). Probe count at write time: %d. "
    "⚠ DECLARED, NOT DISCOVERED: the #266 item ① is struck in HALF — the strikethrough covers the "
    "*proposed lead* clause only and the four ungraded glyphs stand unstruck inside the same "
    "headline, because that half is still true and is re-carried as #266's item ⑨. -->"
    % (n_new + n_num, n_new, after),
    "",
    line,
    "",
    "---",
    "",
]
i = lines.index("## residual → #266")
out = lines[:i] + SECTION + lines[i:]
open(CARRIES, "w", encoding="utf-8").write("\n".join(out))
print("ages bumped: %d (%d were NEW — 0) · probe %d → %d · section written above line %d"
      % (n_new + n_num, n_new, before, after, i + 1))
