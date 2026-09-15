#!/usr/bin/env python3
"""#272 wrap — drive SIZES_BODY / CHAIN_BODY and the `size:` stamp to a JOINT fixed point.

The three readings are mutually dependent: `section-sizes` and the `s214-D6` chain figure are
written INTO `GOOD-MORNING.md`, and writing them moves the very file the `size:` stamp measures
and the chain slices. #271 declared its pre-roll reading superseded rather than converging; this
loop converges instead, and the superseded reading is still named in the line itself.

Each pass: measure → write both bodies → run stamp272.py (its own fixed point) → re-measure.
Stops when both bodies are unchanged by a pass. Nothing is forced.
"""
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
GM = os.path.join(ROOT, "GOOD-MORNING.md")


def run(*a):
    r = subprocess.run([sys.executable] + list(a), cwd=ROOT, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit("FAILED %s\n%s\n%s" % (a, r.stdout, r.stderr))
    return r.stdout


def sizes_body():
    out = run(os.path.join(ROOT, "knowledge", "_gm_usage.py"), "--sizes", "--session", "272")
    ln = [l for l in out.split("\n") if l.startswith("> **section-sizes #272 (real):**")]
    assert len(ln) == 1, out
    return ln[0].split("**", 2)[2].strip()


def chain_body():
    out = run(os.path.join(ROOT, "knowledge", "_gen_chain.py"))
    ln = [l for l in out.split("\n") if "_CHAIN.md:" in l and "FILE" in l]
    assert len(ln) == 1, out
    m = re.search(r"_CHAIN\.md: ([\d,]+) tiktoken cl100k_base · GM header\+LATEST (\d+) tk · "
                  r"LS LATEST delta only \(of (\d+) delta lines\) (\d+) tk · FILE ([\d,]+) "
                  r"tiktoken cl100k_base = slice ([\d,]+) \+ wrapper ([\d,]+) · fixed point in "
                  r"(\d+) pass", ln[0])
    assert m, ln[0]
    return ("`_CHAIN.md` measures **%s tape** — the FINAL reading, taken after the stamp "
            "converged (FILE = slice **%s** + wrapper **%s**; GM header+LATEST **%s tk** · LS "
            "LATEST delta **%s tk** of %s delta lines), `--check` **FRESH**, fixed point reached "
            "in %s pass(es)." % (m.group(1), m.group(6), m.group(7), m.group(2), m.group(4),
                                 m.group(3), m.group(8)))


prev = None
for i in range(1, 9):
    s, c = sizes_body(), chain_body()
    t = open(GM, encoding="utf-8").read()
    t = re.sub(r"(?<=\*\*section-sizes #272 \(real\):\*\* ).*?(?= ⚠ \*\*MEASURED AFTER)",
               lambda _m: s, t, count=1)
    t = re.sub(r"(?<=sits inside the chain slice:\*\* ).*?(?= ⚠ \*\*UP from #271)",
               lambda _m: c, t, count=1)
    open(GM, "w", encoding="utf-8").write(t)
    run(os.path.join(HERE, "stamp272.py"))
    if (s, c) == prev:
        print("JOINT FIXED POINT after %d pass(es)" % i)
        print("  sizes: %s" % s[:120])
        print("  chain: %s" % c[:160])
        break
    prev = (s, c)
else:
    raise SystemExit("sizes/chain did NOT converge in 8 passes — report, do not force")
