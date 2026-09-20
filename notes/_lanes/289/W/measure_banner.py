#!/usr/bin/env python3
"""#289 wrap — measure the ★ LATEST banner against `s241-D2` with the GATE'S OWN instrument.

The banner block = `banner289.md` + the two residual lines. The GENERATED residual line is
substituted from `_roll_state.py` BEFORE measuring, because that line sits inside the block the
cap charges (the #287/#288 lesson, re-applied rather than re-learned).
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "knowledge"))
import _capture_gate as cg


def block_lines():
    banner = open(os.path.join(HERE, "banner289.md"), encoding="utf-8").read().rstrip("\n").split("\n")
    pointer = open(os.path.join(HERE, "pointer289.md"), encoding="utf-8").read().rstrip("\n").split("\n")
    gen = subprocess.run(["python3", os.path.join(ROOT, "knowledge", "_roll_state.py")],
                         capture_output=True, text=True, cwd=ROOT)
    assert gen.returncode == 0, gen.stdout + gen.stderr
    genline = gen.stdout.strip().split("\n")[-1]
    return banner + pointer + [genline], genline


if __name__ == "__main__":
    lines, genline = block_lines()
    substantive = [l for l in lines if l.strip() not in ("", ">")]
    tk = cg.measure_tokens("\n".join(lines))[0]
    print(f"GENERATED line (substituted, never predicted): {genline}")
    print(f"banner: {tk} tk / {len(substantive)} substantive lines "
          f"against the s241-D2 cap {cg.BANNER_LATEST_CAP_TK} / {cg.BANNER_LATEST_CAP_LINES}")
    print("FITS" if (tk <= cg.BANNER_LATEST_CAP_TK
                     and len(substantive) <= cg.BANNER_LATEST_CAP_LINES) else "⛔ OVER")
