#!/usr/bin/env python3
"""#286 wrap — build and MEASURE the ★ LATEST banner against the `s241-D2` cap.

⛔ THE CAP IS MEASURED HERE WITH THE GATE'S OWN INSTRUMENT (`_capture_gate.measure_tokens`),
   not with a second tokenizer, so this pre-check and the gate cannot disagree.
⛔ THE GENERATED RESIDUAL LINE IS SUBSTITUTED AT ITS REAL EXPECTED WIDTH, not as a short
   placeholder — #240's lesson, re-learned at #285: a figure taken before the step that writes
   it is a PREDICTION, not a measurement.

The clause commands SHORTER, never decide-what-to-drop (`s214-D6`).
"""
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "knowledge"))
import _capture_gate as cg

HEAD = ("> ## ★ LATEST — 2026-09-18 (Fri **#286**, Fable 5.1, 9 Opus lanes, DELEGATED wrap — "
        "★★ **THE CONNECTOR LEVER READS AND THE MASTERS ARE SIZED**)")

BULLETS = [
 "> - ⓪ ✅ **NO DATE SPLIT** (09-18). **3 commits `1caaa0b1` + `db0830f7` + `7ed49d37`, remote "
 "== `7ed49d37` at open.** ⛔ **`_HANDOFF-137` FIRST — IT OUTRANKS `_CHAIN.md`**; #130–#136 "
 "stand, **only the 2 below closed**. Words: `notes/_lanes/286/`.",

 "> - ⛔ ① **NO RULING INSCRIBED — `_rulings.json` STAYS 620**, `json.load` here, no `s286-` id. "
 "⚠ **His TWO sentences are RECORDED, NOT INSCRIBED** — *\"okay go on everything\"* and *\"okay "
 "size-on-the-existing-node\"*; **whether either becomes a ruling is HIS** (`s271-D4`).",

 "> - ★★★ ② **THE CONNECTOR LEVER READS: BOOT COLD 73,832 v 80,863, Δ −7,031, ONE VARIABLE** (the "
 "Browser's 17 tools BLOCKED; skills/computer-use/3 connectors held BY DESIGN). ⛔ **NOT A CAUSE — "
 "the last 7 readings span 11,526, WIDER than the delta**: direction yes, magnitude no. **11th "
 "over the 70,000 ceiling — SHRINK-ONLY.**",

 "> - ★★★ ③ **THE 40 MASTERS ARE SIZED ONTO THE 8 NODES** — ***\"okay size-on-the-existing-node\"*** "
 "refuses a node-per-master. `sizes` map, 5 heights each, merge-on-write; **8 nodes · 33 edges · "
 "8/8 `sizes` · 12 `governedBy`** verified here by `json.load`. **`W-285lm` CLOSED.** ⚠ **The KEY "
 "NAME is the lane's, not his**; ⛔ explorer NOT rebuilt.",

 "> - ★★ ④ **`_standing.md` IS OUT OF DRAFT** on ***\"okay go on everything\"*** — **8+/3−, ONE "
 "hunk, all above the rule, the eight lines BYTE-IDENTICAL**. **`W-285sc` CLOSED.** ⛔ **Reading it "
 "as ratification AS WRITTEN is the CONDUCTOR'S reading, not his sentence** — reversible by one "
 "word. ⚠ `_seam.py` still says DRAFT.",

 "> - ★★ ⑤ **#285'S MOVES 2 AND 3 ARE BUILT** — `_seam.py` `INSEAT` arm (+214/−6) counts the "
 "conductor's own in-seat output; `_git_commit.sh --quiet` (+60/−1). ⛔ **`INSEAT_WARN_TK` 10,000 "
 "is PICKED, not ruled.** ⛔ **256,000 fixed in the gauge, constants UNMOVED — 58 prose locations "
 "OWED, his.** ✅ **V 24/24.**",

 "> - ⚙ ⑥ FILL **162,555 / 22** v **161,544 / 20 DECLARED**, Δ **1,011** — ✅ **17,445 INSIDE "
 "180,000, first in five**; 256,000 clear (4th). **subs 1,113,248 (n=9)** — **9 lanes, all "
 "`Agent`/opus/depth 1, NONE in seat, replies 3,399 cl100k TOTAL**; ⛔ **his sentence STILL "
 "uninscribed**. ⛔ **6 gate fails, `#243` form, 12th wrap.** ⏱ DELTA.",
]

POINTER = ("> **residual → #287:** ⬛ **THE CONNECTOR LEVER READS −7,031 AND THE CEILING STILL "
           "STANDS** [NEW — 0, DAVE'S] — his act, the reading is ours. `s225-D2`. **551 items, 9 "
           "new, 2 STRUCK**, `_CARRIES.md` § `residual → #287` `carries:residual-287`. PROBE "
           "`PYTHONPATH=knowledge python3 -c \"import _capture_gate as c;print(len(c._carry_items("
           "[l for l in open('_CARRIES.md') if '#287:**' in l][0])))\"` = 551. ⚠ **ALL 9 NEW "
           "INVISIBLE TO THE PROBE, 9th wrap** (`_AGE_RE` misses `[NEW — 0]`); 543→551 is #285's 8 "
           "ageing in. **2 STRIKES: the masters' open half and the `_standing.md` DRAFT** — both "
           "receipted (`s183-D1`/`s188-D2`); ⛔ **2 the brief named are NOT struck** (each is half "
           "an item whose headline stays true).")

# ⛔ The GENERATED line at its REAL expected width — `_roll_state.py` writes this shape.
GENERATED = ("> **residual (GENERATED #286):** 2c OK (banners 2/2) · 2d OK (deltas 3/3) · 2f OK "
             "(strata 1, log #285) — _roll_state.py · 2026-09-18")

# Shape matched to #285's banner exactly: heading, one `>` spacer, bullets
# consecutive, then the pointer and the GENERATED line.
banner = [HEAD, ">"] + BULLETS + [POINTER, GENERATED]
text = "\n".join(banner)
tk = cg.measure_tokens(text)[0]
subst = [l for l in text.splitlines() if l.strip() not in ("", ">")]
print(f"BANNER  {tk:,} tape / cap {cg.BANNER_LATEST_CAP_TK:,}  ·  "
      f"{len(subst)} substantive lines / cap {cg.BANNER_LATEST_CAP_LINES}")
over = []
if tk > cg.BANNER_LATEST_CAP_TK:
    over.append(f"tape by {tk - cg.BANNER_LATEST_CAP_TK}")
if len(subst) > cg.BANNER_LATEST_CAP_LINES:
    over.append(f"lines by {len(subst) - cg.BANNER_LATEST_CAP_LINES}")
if over:
    sys.exit("⛔ OVER CAP by " + " and ".join(over) + " — compress, never drop (`s214-D6`).")
print("✅ INSIDE THE CAP — headroom", cg.BANNER_LATEST_CAP_TK - tk, "tape")

if "--emit" in sys.argv:
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "banner286.md")
    open(out, "w", encoding="utf-8").write(text + "\n")
    print("WROTE", out)
