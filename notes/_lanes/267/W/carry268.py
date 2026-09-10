#!/usr/bin/env python3
"""#267 wrap — build `_CARRIES.md` § `## residual → #268` from § `## residual → #267`.

ONE programmatic pass, the #261…#266 shape:
  (a) every age bracket bumped by one — `[NEW — 0…]` → `[1…]`, `[N…]` → `[N+1…]`;
  (b) ONE surgical edit, asserted UNIQUE before it is made, by ADDITION with an
      `s183-D1`/`s188-D2` receipt and the original wording left standing verbatim beneath;
  (c) the session's EIGHT NEW items written in front.

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
src = [l for l in lines if l.startswith("> **residual → #267:**")]
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
    # the #267 lead — all three of its items were DISCHARGED at #267, so the whole headline is
    # struck (not half, unlike #266's): the 3D dig defect was diagnosed and fixed, the run-of-show
    # page was written, and the sixth cold run was taken. What each one LEFT BEHIND is re-carried
    # in front as this session's items ① (a)/(b) and ②.
    ("⬛ **① THE 3D DIG DEFECT, THE RUN-OF-SHOW, THE SIXTH COLD RUN** [1, DAVE'S]",
     "⬛ **~~① THE 3D DIG DEFECT, THE RUN-OF-SHOW, THE SIXTH COLD RUN~~** [1, DAVE'S] ⛔ "
     "**STRUCK AT #267 WITH ITS `s183-D1`/`s188-D2` RECEIPT — ALL THREE WERE DISCHARGED THE "
     "SAME DAY, AND NONE OF THEM ENDED WHERE THIS CARRY EXPECTED.** **(a)** the 3D dig defect "
     "was **NOT a defect but a design decision seen from the other side**: *\"just on a flat "
     "plane, it wast before\"* names **v1.8's camera-plane ring**, which #266 introduced "
     "DELIBERATELY against occlusion; lane K restored the world-space sphere at **v1.9 "
     "`4bc5231`** and paid the occlusion cost with a 12px screen-space nudge, measuring the "
     "trade at **4 wrong-colour centres in 1,512 samples vs v1.8's 0**. ⚠ **The carry's "
     "instruction — *his screenshot first* — was right and was followed; what it could not "
     "know is that the screenshot would describe a deliberate change.** **(b)** the "
     "run-of-show page **EXISTS**: `notes/_RUN-OF-SHOW-david-rice-2026-09-10-v1.html` "
     "(`0f9ef72`), 18:00 stated, six measured risks, four ⬛ slots left as his — and lane S "
     "found that **the twelve plot points were NEVER INSCRIBED ANYWHERE**, so the page carries "
     "a fresh mapping, declared as such. **(c)** the sixth cold run was **TAKEN** "
     "(`notes/_subreports/2026-09-10-267-C6-cold-run-6.md`, 2/3/3/2 against the v1.0.9 ZIP) "
     "and found the packaging hole that produced **v1.0.10**. Where the correction is "
     "inscribed: `_LIVE-STATE.md` ⏱ LATEST DELTA #267, "
     "`_DECISION-HISTORY/2026-09-10-267-v1010-edges-run-of-show.md` §§ 1/3/6, and the ★ LATEST "
     "#267 banner. **What each item LEFT BEHIND is re-carried in front as #267's ① (a)/(b) and "
     "②.** The original wording stands verbatim below."),
]
for find, repl in EDITS:
    assert aged.count(find) == 1, (aged.count(find), find[:90])
    aged = aged.replace(find, repl, 1)

# ---- (c) this session's new items -------------------------------------------------------------
NEW = open(os.path.join(HERE, "carry268-new.txt"), encoding="utf-8").read().strip()
line = "> **residual → #268:** " + NEW + " · " + aged[len("> **residual → #267:** "):]
after = len(cg._carry_items(line))

SECTION = [
    "## residual → #268",
    "",
    "*Written straight here at the #267 wrap (✅ **NO DATE SPLIT — session, ritual and commit are "
    "all 2026-09-10**) under `s225-D2` clause (i). Ages +1, wording unchanged, nothing dropped for "
    "being old; **ONE carry STRUCK WHOLE, by ADDITION and with its `s183-D1`/`s188-D2` receipt**, "
    "the original wording standing verbatim beneath — the #267 LEAD, all three of whose items were "
    "discharged the same day, and none of them where the carry expected. ★★★ **Dave ruled FOUR "
    "times at #267 in the `_rulings.json` sense: the store moved 441 → 445 (`s267-D1` … "
    "`s267-D4`).***",
    "",
    "<!-- WRITTEN-FIRST: residual → #268 — the aged tail below the EIGHT new items is the #267 "
    "line put through ONE programmatic pass (`notes/_lanes/267/W/carry268.py`): %d age brackets "
    "bumped (%d of them `NEW — 0` → `1`), then 1 surgical edit asserted UNIQUE before it was "
    "made (the whole-headline strike above). Probe count at write time: %d. "
    "⚠ DECLARED, NOT DISCOVERED: the strike covers the #267 item ① headline in full, unlike "
    "#266's half-strike, because all three of its named items were discharged — what each left "
    "behind is re-carried in front rather than left inside a struck line. -->"
    % (n_new + n_num, n_new, after),
    "",
    line,
    "",
    "---",
    "",
]
i = lines.index("## residual → #267")
out = lines[:i] + SECTION + lines[i:]
open(CARRIES, "w", encoding="utf-8").write("\n".join(out))
print("ages bumped: %d (%d were NEW — 0) · probe %d → %d · section written above line %d"
      % (n_new + n_num, n_new, before, after, i + 1))
