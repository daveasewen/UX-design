#!/usr/bin/env python3
"""#267 wrap — step 2: demote the #266 ★ LATEST banner to ★ PRIOR and write #267's in front.

The counts on the residual pointer are the PROBE's own (`_capture_gate._carry_items`), taken
here rather than typed. `{{ROLLSTATE}}` is left for a second pass: `_roll_state.py` must read
the file as it will be committed, and it cannot do that until this banner is in it.
"""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
GM = os.path.join(ROOT, "GOOD-MORNING.md")
sys.path.insert(0, os.path.join(ROOT, "knowledge"))
import _capture_gate as cg  # noqa: E402

carries = io.open(os.path.join(ROOT, "_CARRIES.md"), encoding="utf-8").read().split("\n")
line268 = [l for l in carries if l.startswith("> **residual → #268:**")]
assert len(line268) == 1
count = len(cg._carry_items(line268[0]))

banner = io.open(os.path.join(HERE, "banner267.txt"), encoding="utf-8").read().rstrip("\n")
banner = (banner.replace("{{AGED}}", "552").replace("{{NEW}}", "8")
                .replace("{{COUNT}}", str(count)))
assert "{{AGED}}" not in banner and "{{COUNT}}" not in banner

lines = io.open(GM, encoding="utf-8").read().split("\n")
i = [k for k, l in enumerate(lines) if l.startswith("> ## ★ LATEST — ")]
assert len(i) == 1, i
assert "**#266**" in lines[i[0]], lines[i[0]][:120]
lines[i[0]] = lines[i[0]].replace("> ## ★ LATEST — ", "> ## ★ PRIOR — ", 1)
lines = lines[:i[0]] + banner.split("\n") + [""] + lines[i[0]:]

# the forward TITLE line — ritual step 4b
t = [k for k, l in enumerate(lines) if l.startswith("> **TITLE THE NEXT CHAT →**")]
assert len(t) == 1, t
lines[t[0]] = ("> **TITLE THE NEXT CHAT →** `Apollo - #268: rehearse the run-of-show, "
               "v1.0.11 canon, the islands`")

io.open(GM, "w", encoding="utf-8").write("\n".join(lines))
print("banner inserted at line %d · probe count %d · title line %d" % (i[0] + 1, count, t[0] + 1))
