#!/usr/bin/env python3
"""#272 wrap — the DECLARE-LAST `size:` stamp, written after 2c/2d/2f and after the new stratum.

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
    "BYTE-IDENTICAL TO ITS STATE AT `781f7be` AND AT `5df4ead`** (`sha256 4311cce4…`, 198 lines "
    "between the `§A` and `§C` markers — the shape `_capture_gate.section_a_digest()` pins, so "
    "§A has not moved in four sessions; the gate reports it **EXEMPT by ruling — measured and "
    "reported, never charged**). ⚠ **AND THE #271 STAMP'S §A FIGURE IS NOT CARRIED FORWARD, "
    "BECAUSE IT DOES NOT REPRODUCE AT THIS SEAT:** #271, #270 and #269 all recorded `sha256 "
    "b9aef5f5…`, 169 lines. Running the gate's OWN pinned probe here returns `4311cce4…` over "
    "198 lines against the SAME commits those stamps describe — so the two figures are **two "
    "different probe shapes, not a change in §A**, and the digest written here is the one the "
    "gate would compute [[tape-unit-is-not-real-tokens]]. Which shape the stamp should quote is "
    "ruling-shaped and is NOT decided here. · LS **{lsk}K tape** ({ls} real) · corpus GM+LS "
    "**{ck}K tape** ({c} real, the RETRIEVAL surface, not the chain) · ⛔ **the chain's own size "
    "is NOT copied here — RETIRED #45; its ONE home is `_CHAIN.md`'s generated footer, exact by "
    "construction and `--check`-blocked** · measured 2026-09-15 at the #272 wrap, DECLARE-LAST — "
    "after 2c, 2d and 2f, and after the new stratum, so it grades the files this wrap actually "
    "leaves behind. ⚠ **THE DELTA IS THE FINDING, AND THIS WRAP MOVED THE TWO FILES IN OPPOSITE "
    "DIRECTIONS:** against #271's stamp (**36,053 / 60,536 tape**) GM is **{gmd} tape {gmdir}** "
    "and LS is **{lsd} tape {lsdir}**, corpus **{cd} {cdir}** — the #270 banner and the #271 "
    "stratum rolled OUT of GM while a long `Last refreshed` stamp and a 25-line delta went INTO "
    "LS (partly offset by the #269 delta and #268's `Previous:` segment rolling out), and the "
    "split is named rather than averaged into one number. ✅ **THE NEW ★ LATEST BANNER MEASURES "
    "1,199 tape against the `s241-D2` cap of 1,200, ON 10 SUBSTANTIVE LINES AGAINST THE SAME "
    "RULING'S 10-LINE CLAUSE — UNDER BOTH, AND BY ONE TOKEN.** ⚠ **THAT IS NOT HEADROOM AND IS "
    "NOT PRESENTED AS ANY: #271 measured 1,166 / 10 and this banner is 33 tape closer to the "
    "wall**, reached after four tightening passes and ONE STRUCTURAL MERGE — the sidequests and "
    "the DO-NOT-RULE list share a line, because eight bullets plus two residual lines is eleven "
    "and the cap is ten. ⛔ **Nothing was dropped to fit: every item, carry, declared skip, "
    "receipt name, measured figure and word of Dave's that belongs on the banner is on it, and "
    "the gauge / declared-skip / not-done detail lives where `s241-D2` says it must — the ⏱ "
    "LATEST DELTA.** ⚠ **THE NEXT WRAP HAS NO ROOM IN THIS IDIOM AND IS TOLD SO HERE.** ⛔ "
    "**NEITHER FILE SIZE IS A TRIM ORDER; all of these are measurements, and what to do about "
    "them is Dave's.**"
)


def render():
    gm = open(GM, encoding="utf-8").read()
    ls = open(LS, encoding="utf-8").read()
    g, l = tk(gm), tk(ls)
    c = g + l
    d = lambda now, then: (f"{abs(now - then):,}", "DOWN" if now < then else "UP")
    gmd, gmdir = d(g, 36053)
    lsd, lsdir = d(l, 60536)
    cd, cdir = d(c, 96589)
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
