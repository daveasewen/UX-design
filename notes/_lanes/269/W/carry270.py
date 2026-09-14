#!/usr/bin/env python3
"""#269 wrap — build `_CARRIES.md` § `## residual → #270` from § `## residual → #269`.

ONE programmatic pass, the #261…#268 shape:
  (a) every age bracket bumped by one — `[NEW — 0…]` → `[1…]`, `[N…]` → `[N+1…]`;
  (b) ⛔ ZERO surgical edits this wrap, and that is a MEASUREMENT, not an omission: #269
      discharged no carried claim and retracted none. Every #119 open stays open exactly as
      #119 phrased it (`_HANDOFF-120-the-graph-gets-its-atoms.md` § F), so there is nothing
      for `s183-D1`/`s188-D2` to strike. The list is asserted empty rather than left implicit.
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
src = [l for l in lines if l.startswith("> **residual → #269:**")]
assert len(src) == 1, len(src)
src = src[0]
before = len(cg._carry_items(src))

# ---- (a) ages -------------------------------------------------------------------------------
n_new = len(re.findall(r"\[NEW — 0(?=[,\]])", src))
n_num = len(re.findall(r"\[(\d+)(?=[,\]])", src))
aged = re.sub(r"\[(\d+)(?=[,\]])", lambda m: "[%d" % (int(m.group(1)) + 1), src)
aged = re.sub(r"\[NEW — 0(?=[,\]])", "[1", aged)
assert "[NEW — 0" not in aged

# ---- (b) the surgical edits — NONE, asserted ---------------------------------------------------
EDITS = []
assert not EDITS, "if an edit is added it must carry its s183-D1/s188-D2 receipt"

# ---- (c) this session's new items -------------------------------------------------------------
NEW = open(os.path.join(HERE, "carry270-new.txt"), encoding="utf-8").read().strip()
line = "> **residual → #270:** " + NEW + " · " + aged[len("> **residual → #269:** "):]
after = len(cg._carry_items(line))

SECTION = [
    "## residual → #270",
    "",
    "*Written straight here at the #269 wrap (✅ **NO DATE SPLIT — the wrap ritual and its commit "
    "are both 2026-09-14**; ⚠ the SESSION itself spans 2026-09-13 → 2026-09-14 and its commits "
    "carry their own true dates, which is a two-day session and not the #241 shape) under "
    "`s225-D2` clause (i). Ages +1, wording unchanged, nothing dropped for being old; ⛔ **ZERO "
    "carries struck, and that is measured rather than omitted** — #269 discharged no carried "
    "claim and retracted none, and every #119 open stays open exactly as #119 phrased it "
    "(`_HANDOFF-120-the-graph-gets-its-atoms.md` § F). ★★★ **Dave ruled TEN times at #269 in the "
    "`_rulings.json` sense: the store moved 453 → 463 (`s269-D1` … `s269-D10`), six of them "
    "quoting ONE sentence because he accepted the six KG-gap recommendations in one breath.***",
    "",
    "<!-- WRITTEN-FIRST: residual → #270 — the aged tail below the EIGHT new items is the #269 "
    "line put through ONE programmatic pass (`notes/_lanes/269/W/carry270.py`): %d age brackets "
    "bumped (%d of them `NEW — 0` → `1`), and ZERO surgical edits, asserted empty in the script "
    "rather than left implicit. Probe count at write time: %d. ⚠ DECLARED, NOT DISCOVERED: a "
    "wrap with no strike is the shape of a session that BUILT and PROPOSED rather than "
    "discharged, and the carry set grows accordingly. -->"
    % (n_new + n_num, n_new, after),
    "",
    line,
    "",
    "---",
    "",
]
i = lines.index("## residual → #269")
out = lines[:i] + SECTION + lines[i:]
open(CARRIES, "w", encoding="utf-8").write("\n".join(out))
print("ages bumped: %d (%d were NEW — 0) · probe %d → %d · section written above line %d"
      % (n_new + n_num, n_new, before, after, i + 1))
