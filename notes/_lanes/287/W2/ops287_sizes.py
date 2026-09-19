#!/usr/bin/env python3
"""#287 wrap — fill `{{SIZES}}` in the #287 stratum, ITERATED TO A FIXED POINT.

⛔ THE LINE MEASURES A REGION THAT CONTAINS IT. Publishing a reading taken before the line was
   written is the #240 defect (one wrap, two figures); this substitutes, re-measures and repeats
   until the generator's own output stops moving, then lands THAT text through the mover.
"""
import json, os, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
GM = os.path.join(ROOT, "GOOD-MORNING.md")

def sizes():
    out = subprocess.run(["python3", os.path.join(ROOT, "knowledge", "_gm_usage.py"),
                          "--sizes", "--session", "287"],
                         capture_output=True, text=True, cwd=ROOT).stdout.strip().split("\n")[-1]
    assert out.startswith("> **section-sizes #287 (real):**"), out[:80]
    return out[len("> **section-sizes #287 (real):** "):]

text = open(GM, encoding="utf-8").read()
assert text.count("> **section-sizes #287 (real):** {{SIZES}}") == 1
cur, seen, n = sizes(), [], 0
while n < 8:
    n += 1
    trial = text.replace("{{SIZES}}", cur)
    open(GM, "w", encoding="utf-8").write(trial)
    nxt = sizes()
    print(f"  pass {n}: {'FIXED POINT' if nxt == cur else 'moved'}")
    if nxt == cur:
        break
    open(GM, "w", encoding="utf-8").write(text)   # restore the placeholder and try again
    cur = nxt
else:
    open(GM, "w", encoding="utf-8").write(text)
    sys.exit("REFUSED — section-sizes did not converge in 8 passes; nothing published.")
print("section-sizes #287 (fixed point):", cur[:160])
assert "{{SIZES}}" not in open(GM, encoding="utf-8").read()
