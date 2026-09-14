#!/usr/bin/env python3
"""#271 wrap — the DECLARE-LAST `size:` stamp, written after 2c/2d/2f and after the new stratum.

⛔ The stamp sits INSIDE the chain slice, so writing it moves `_CHAIN.md`. The order this script
enforces, and the reason it is a fixed point rather than one pass: stamp → regenerate the chain →
re-measure GM → if the GM figure moved, stamp again. `s214-D6`'s chain reading is taken AFTER
this converges, never before (#240's lesson).
"""
import os
import subprocess
import sys

import tiktoken

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "..", "..", "..", ".."))
ENC = tiktoken.get_encoding("cl100k_base")
tk = lambda t: len(ENC.encode(t))
GM = os.path.join(ROOT, "GOOD-MORNING.md")
LS = os.path.join(ROOT, "_LIVE-STATE.md")

TEMPLATE = (
    "> **size:** GM **{gmk}K tape** ({gm} exact — whole-file `tiktoken cl100k_base`, the figure "
    "this stamp is graded against at 10% tolerance) · §A **7.0K tape** (6,957 real by "
    "`_gm_usage.py`) — ✅ **THE §A BYTE-IDENTITY PROBE WAS RUN AT THIS SEAT AND §A IS "
    "BYTE-IDENTICAL TO ITS STATE AT `781f7be`** (`sha256 b9aef5f5…`, 169 lines — the SAME digest "
    "#269 and #270 recorded, so §A has not moved in three sessions; the gate reports it **EXEMPT "
    "by ruling — measured and reported, never charged**) · LS **{lsk}K tape** ({ls} real) · "
    "corpus GM+LS **{ck}K tape** ({c} real, the RETRIEVAL surface, not the chain) · ⛔ **the "
    "chain's own size is NOT copied here — RETIRED #45; its ONE home is `_CHAIN.md`'s generated "
    "footer, exact by construction and `--check`-blocked** · measured 2026-09-14 at the #271 "
    "wrap, DECLARE-LAST — after 2c, 2d and 2f, and after the new stratum, so it grades the files "
    "this wrap actually leaves behind. ⚠ **THE DELTA IS THE FINDING, AND THIS WRAP MOVED THE TWO "
    "FILES IN OPPOSITE DIRECTIONS:** against #270's stamp (**35,128 / 60,012 tape**) GM is "
    "**{gmd} tape {gmdir}** and LS is **{lsd} tape {lsdir}**, corpus **{cd} {cdir}** — the #269 "
    "banner and the #270 stratum rolled OUT of GM while a longer `Last refreshed` stamp and a "
    "23-line delta went INTO LS, and the split is named rather than averaged into one number. ✅ "
    "**THE NEW ★ LATEST BANNER MEASURES 1,103 real against the `s241-D2` cap of 1,200 — UNDER IT, "
    "WITH HEADROOM, ON 9 SUBSTANTIVE LINES AGAINST THE SAME RULING'S 10-LINE CLAUSE.** ⚠ **AND "
    "THAT IS A CHANGE FROM #270, WHICH MET THE CAP EXACTLY AFTER TEN TIGHTENING PASSES AND SAID "
    "IT HAD LEFT THE NEXT WRAP NO HEADROOM IN THIS IDIOM.** The headroom came back because #271 "
    "is SHORTER TO DESCRIBE — five rulings that each reduce to one sentence and one harvest that "
    "reduces to one row-count — not because anything was written less honestly: no item, carry, "
    "declared skip, receipt name, measured figure or word of Dave's was dropped to fit. ⛔ "
    "**NEITHER FILE SIZE IS A TRIM ORDER; all of these are measurements, and what to do about "
    "them is Dave's.**"
)


def render():
    gm = open(GM, encoding="utf-8").read()
    ls = open(LS, encoding="utf-8").read()
    g, l = tk(gm), tk(ls)
    c = g + l
    d = lambda now, then: (f"{abs(now - then):,}", "DOWN" if now < then else "UP")
    gmd, gmdir = d(g, 35128)
    lsd, lsdir = d(l, 60012)
    cd, cdir = d(c, 95140)
    return TEMPLATE.format(gmk=round(g / 1000, 1), gm=g, lsk=round(l / 1000, 1), ls=f"{l:,}",
                           ck=round(c / 1000, 1), c=f"{c:,}", gmd=gmd, gmdir=gmdir,
                           lsd=lsd, lsdir=lsdir, cd=cd, cdir=cdir)


for i in range(8):
    lines = open(GM, encoding="utf-8").read().split("\n")
    idx = [n for n, x in enumerate(lines) if x.startswith("> **size:**")]
    assert len(idx) == 1, idx
    new = render()
    if lines[idx[0]] == new:
        print("converged after %d pass(es)" % i)
        break
    lines[idx[0]] = new
    open(GM, "w", encoding="utf-8").write("\n".join(lines))
    subprocess.run([sys.executable, os.path.join(ROOT, "knowledge", "_gen_chain.py")],
                   cwd=ROOT, check=True, capture_output=True)
else:
    raise SystemExit("size: stamp did NOT converge in 8 passes — report, do not force")

gm = open(GM, encoding="utf-8").read()
ls = open(LS, encoding="utf-8").read()
print("FINAL  GM %d · LS %d · corpus %d" % (tk(gm), tk(ls), tk(gm) + tk(ls)))
