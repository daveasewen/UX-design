#!/usr/bin/env python3
"""#270 wrap — demote the #269 ★ LATEST banner to ★ PRIOR and write #270's in front.

The count on the residual pointer is the PROBE's own (`_capture_gate._carry_items`), taken here
rather than typed, and asserted equal to the number already written into the banner text.
"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
GM = os.path.join(ROOT, "GOOD-MORNING.md")
sys.path.insert(0, os.path.join(ROOT, "knowledge"))
import _capture_gate as cg  # noqa: E402

carries = io.open(os.path.join(ROOT, "_CARRIES.md"), encoding="utf-8").read().split("\n")
line271 = [l for l in carries if l.startswith("> **residual → #271:**")]
assert len(line271) == 1
count = len(cg._carry_items(line271[0]))

banner = io.open(os.path.join(HERE, "banner270.txt"), encoding="utf-8").read().rstrip("\n")
assert ("**%d items, 9 new**" % count) in banner, count

lines = io.open(GM, encoding="utf-8").read().split("\n")
i = [k for k, l in enumerate(lines) if l.startswith("> ## ★ LATEST — ")]
assert len(i) == 1, i
assert "**#269**" in lines[i[0]], lines[i[0]][:120]
lines[i[0]] = lines[i[0]].replace("> ## ★ LATEST — ", "> ## ★ PRIOR — ", 1)
lines = lines[:i[0]] + banner.split("\n") + [""] + lines[i[0]:]

# the forward TITLE line — ritual step 4b.
t = [k for k, l in enumerate(lines) if l.startswith("> **TITLE THE NEXT CHAT →**")]
assert len(t) == 1, t
TITLE = "`Apollo - #271: ratify the atoms, widen the net`"
lines[t[0]] = "> **TITLE THE NEXT CHAT →** " + TITLE

io.open(GM, "w", encoding="utf-8").write("\n".join(lines))
print("banner inserted at line %d · probe count %d · title line %d"
      % (i[0] + 1, count, t[0] + 1))
