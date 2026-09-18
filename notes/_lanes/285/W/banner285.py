#!/usr/bin/env python3
"""#285 wrap — 2c: roll the ★ PRIOR banner (#283) to `_GM-ARCHIVE.md`, demote #284's ★ LATEST
to ★ PRIOR, and write the new ★ LATEST #285 banner.

⛔ `s241-D6` BANNER DISCIPLINE: written toward a small `_CHAIN.md`. The clause commands SHORTER,
never decide-what-to-drop — tighter sentences and pointers instead of restatement, and NEVER the
omission of an item, a carry, a declared skip or a receipt name. Roll-to-archive keeps every
prior banner verbatim, so nothing is lost by writing this one tight.
⛔ `s241-D2` CAP, BLOCKING: 10 substantive lines / 1,200 cl100k for the ★ LATEST banner alone.
Measured here before the mover is called, so a refusal is not discovered by the gate.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "knowledge"))
from run_ops import run
import _gauge_tokens as G

GM = "GOOD-MORNING.md"
ARCH = "_GM-ARCHIVE.md"

PROBE = ("PYTHONPATH=knowledge python3 -c \"import _capture_gate as c;"
         "print(len(c._carry_items([l for l in open('_CARRIES.md') if '#286:**' in l][0])))\"")

BANNER = [
"> ## ★ LATEST — 2026-09-18 (Fri **#285**, Fable 5.1, 7 Opus lanes, DELEGATED wrap — ★★ **THE B IS STRAIGHTENED AND THE CONNECTOR ANSWER COMES BY ACT**)",
">",
"> - ⓪ ✅ **NO DATE SPLIT** (09-18). **2 commits `b99d092c` + `ff354475`, UNPUSHED at open.** ⛔ **`_HANDOFF-136` FIRST — IT OUTRANKS `_CHAIN.md`**; #130–#135 stand, **only the 2 below closed**. Words: `notes/_lanes/285/`.",
"> - ⛔ ① **NO RULING INSCRIBED — `_rulings.json` STAYS 620**, `json.load` here. ⚠ ***\"excellent work!\"* IS ENTHUSIASM, NOT A RULING** (`s271-D4`).",
"> - ★★★ ② **THE #284 MASTERS WERE DISTORTED; DAVE REOPENED HIS OWN ACCEPTANCE** — *\"the word mark is distorted, look at the B\"*. TWO causes: per-node snapping, controls left behind, **and `kx/ky` to 1.0436 — 4.4% wider than tall at h=32**. ⚠ #284's probes counted pixels and stems — **neither sees an aspect error**. Rebuilt: ONE scale `s=h/85` + ONE translation, nodes AND controls; `snapped_nodes` 0; hexagons byte-identical. **V: 16/16, residual 5.4e-5 px.** His: ***\"2. accept\"***. ⛔ **NOT in `_logo_nodes.json`** — `W-285lm` OPEN, HOW is his.",
"> - ★★ ③ **THE SEAM RE-QUOTES THE STANDING CONSTRAINTS** — *\"yes to the seam re-quoting the standing constraints\"*, the messy-middle answer. `_seam.py` prints a 4th block **LAST**, after SCRATCH — the recency end: **8 lines · 246 cl100k**. ⛔ **`_standing.md` IS A DRAFT, the wording HIS** (`W-285sc`) — it re-quotes, never inscribes.",
"> - ⛔★ ④ **THE CONNECTOR ANSWER CAME BY ACT: he BLOCKED the built-in Browser's 17 tools**, server dropped mid-session. ⇒ **#286 OPENS WITH A READING, NOT A LANE — boot COLD vs 80,863, ONE variable.** Skills untouched BY DESIGN.",
"> - ★★ ⑤ **THE DELEGATION RULE WAS OBEYED — MEASURED, NOT ASSERTED.** 7 lanes, all `Agent`/opus/depth 1 (LM2·SC·V·C·C2·P·W); **none in seat**. ★ **7 replies cost the window 3,382 cl100k TOTAL vs ≈738,851 of sub FILL.** ⛔ **His sentence still NOT inscribed.**",
"> - ⚙ ⑥ FILL **197,852 / 31** v **191,785 / 28 DECLARED**, Δ **6,067** — ⛔ **+17,852 on 180,000** (the QUALITY line), ✅ **−22,148 on 220,000**, ✅ **256,000 clear (3rd)**. BOOT **80,863 n=1, 10th over the 70,000 ceiling — CUT it**. **subs 738,851 (n=7)**. ⛔ **7 gate fails at open, 6 at close** — 6 inherited, `#243` form, **11th wrap**; the 7th ours (`ds-021`/`_seam.py`, now `estimate-only`). ⚠ **A wrap sub DIED mid-ritual (`ENOTFOUND`), wrote NOTHING — luck, not design.** ⏱ DELTA.",
]


def measure(lines):
    body = "\n".join(lines)
    n, tier = G.count(body)
    sub = [l for l in lines if l.strip() not in ("", ">")]
    return n, tier, len(sub)


def main():
    old_latest = [l.rstrip("\n") for l in open(os.path.join(ROOT, GM), encoding="utf-8")
                  if l.startswith("> ## ★ LATEST")]
    assert len(old_latest) == 1, len(old_latest)
    old_latest = old_latest[0]
    demoted = old_latest.replace("> ## ★ LATEST", "> ## ★ PRIOR", 1)

    residual = ("> **residual → #286:** ⬛ **THE CONNECTOR ANSWER CAME BY ACT — #286 MEASURES "
                "BOOT COLD** [NEW — 0, DAVE'S] — his act, not his sentence. `s225-D2`. **543 items, 8 new, 2 "
                "STRUCK**, `_CARRIES.md` § `residual → #286` `carries:residual-286`. PROBE "
                f"`{PROBE}` = 543. ⚠ **ALL 8 NEW INVISIBLE TO THE PROBE, 8th wrap** (`_AGE_RE` "
                "misses `[NEW — 0]`); 539→543 is #284's 4 ageing in. **2 STRIKES: the #284 "
                "masters acceptance he reopened, and the 108-page showroom staleness** — "
                "both receipted (`s183-D1`/`s188-D2`).")
    # ⛔ The GENERATED line is measured at its REAL expected width, not a short placeholder —
    #   the #240 lesson: a figure taken before the step that writes it is a prediction.
    gen = ("> **residual (GENERATED #285):** 2c OK (banners 2/2) · 2d OK (deltas 3/3) · "
           "2f OK (strata 1, log #284) — _roll_state.py · 2026-09-18")

    full = BANNER + [residual, gen]
    n, tier, subs = measure(full)
    print(f"★ LATEST banner: {n} cl100k ({tier}) / {subs} substantive lines "
          f"— cap 1,200 / 10 (`s241-D2`, BLOCKING)")
    if n > 1200 or subs > 10:
        print("⛔ OVER CAP — not writing"); return 1

    ops = [
        # 2c — roll the ★ PRIOR banner (#283) to the archive, newest-first, under a date+session key
        {"op": "insert", "file": ARCH, "at": "## Batch 2026-09-18 #284", "where": "before",
         "lines": ["## Batch 2026-09-18 #285", ""]},
        {"op": "move", "src": GM,
         "start": "> ## ★ PRIOR — 2026-09-18 (Fri **#283**",
         "end": "## ⬛ DO THIS FIRST",
         "dst": ARCH, "at": "## Batch 2026-09-18 #285", "where": "after"},
        # demote #284's ★ LATEST, then put #285's in front of it
        {"op": "replace", "file": GM, "find": [old_latest], "replace": [demoted]},
        {"op": "insert", "file": GM, "at": demoted, "where": "before", "lines": full + [""]},
    ]
    return run("banner", ops, write="--write" in sys.argv, min_bytes=1_000)


sys.exit(main())
