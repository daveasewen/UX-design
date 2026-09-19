#!/usr/bin/env python3
"""#288 wrap — fill the stratum's `{{SIZES}}` placeholder, ITERATED TO A FIXED POINT.

⚠ THE LINE MEASURES A REGION THAT CONTAINS IT. `_gm_usage.py --sizes` reports STRATA, and this
line lives inside STRATA, so writing a reading taken before the write makes the line wrong the
moment it lands — the #240 one-wrap-two-figures lesson. So: substitute, re-measure, repeat until
the measurement stops moving, and publish the FIXED POINT.

⚠ DECLARED DEVIATION: this is a whole-file write, NOT a mover op. `_gm_move.py` has no
iterate-to-fixed-point op, and this is a fill of THIS wrap's OWN placeholder in THIS wrap's OWN
stratum — not a move of anyone's text. The §A digest is asserted unchanged before and after, so
the claim is mechanical rather than an assurance.
"""
import os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
GM = os.path.join(ROOT, "GOOD-MORNING.md")
sys.path.insert(0, os.path.join(ROOT, "knowledge"))
import _capture_gate as cg

def digest():
    lines = open(GM, encoding="utf-8").read().splitlines()
    return cg.section_a_digest(lines, cg.section_spans(lines))

def sizes_line():
    out = subprocess.run(["python3", os.path.join(ROOT, "knowledge", "_gm_usage.py"),
                          "--sizes", "--session", "288"],
                         capture_output=True, text=True, cwd=ROOT).stdout
    line = [l for l in out.split("\n") if l.startswith("> **section-sizes #288")]
    assert len(line) == 1, out[-500:]
    return line[0]

before = digest()
cur = open(GM, encoding="utf-8").read()
pass

prev = None
for i in range(8):
    new = sizes_line()
    if new == prev:
        print(f"FIXED POINT after {i} substitution(s)")
        break
    txt = open(GM, encoding="utf-8").read()
    old = [l for l in txt.split("\n") if l.startswith("> **section-sizes #288")]
    assert len(old) == 1
    assert txt.count(old[0]) == 1
    open(GM, "w", encoding="utf-8").write(txt.replace(old[0], new, 1))
    print(f"  pass {i+1}: {new[:110]}")
    prev = new
else:
    sys.exit("DID NOT CONVERGE in 8 passes — nothing further written")

after = digest()
assert before == after, f"§A DIGEST MOVED: {before} -> {after}"
print(f"§A digest unchanged: {after}")
print("FINAL:", sizes_line()[:160])
