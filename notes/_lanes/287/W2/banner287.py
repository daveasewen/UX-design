#!/usr/bin/env python3
"""#287 wrap — build the ★ LATEST banner and MEASURE it with the GATE'S OWN instrument.

`s241-D2` is BLOCKING at 10 substantive lines / 1,200 tape over the whole banner block.
The pre-check here calls `_capture_gate.measure_tokens` and counts lines exactly as
`check_budgets()` does (blank and `>`-only lines are free), so the pre-check and the gate
cannot disagree — and the GENERATED residual line is substituted from `_roll_state.py`
BEFORE measuring, because that line is inside the block the gate charges.

`--emit` writes `banner287.md` for the ops builder; without it this is a measurement only.
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "knowledge"))
import _capture_gate as cg

HEAD = ("> ## ★ LATEST — 2026-09-19 (Sat **#287**, Fable 5.1, 5 Opus lanes, DELEGATED wrap — "
        "★★ **THE RULINGS LAND AND THE STRAND MAP IS ORDERED**)")

BULLETS = [
 "> - ⓪ ✅ **NO DATE SPLIT** (09-19). **1 commit `75a490cd`, pushed and VERIFIED at lane C.** "
 "⛔ **`_HANDOFF-138` FIRST — IT OUTRANKS `_CHAIN.md`**; #130–#137 stand, **only the 4 below "
 "closed**. Words: `notes/_lanes/287/`.",

 "> - ★★★ ① **TWO RULINGS INSCRIBED, 620 → 622** — `json.load` here, no dupe. His whole reply: "
 "***\"1. inscribe · 2. keep `sizes` and rebuild. · 3. do it\"***. **`s287-D1`** (the 8 standing "
 "lines ratified AS WRITTEN, the 256,000 fix) · **`s287-D2`** (a master is a SIZE FIELD on the "
 "existing node). ★ **The JOIN is named on `s287-D1`'s face: #286's reading was the "
 "CONDUCTOR'S; *\"inscribe\"* is his.**",

 "> - ★★ ② **THE EXPLORER READS `sizes`** — builder **v1.27**, three new reads, a MASTERS tab. "
 "**8/8 logo nodes, 40 entries byte-identical to `_logo_nodes.json`, PARSED out of the built "
 "page, not eyeballed**; 8 nodes · 33 edges either side. ⚠ 2,256 coords moved — **the "
 "Constitution's growth, not the field's**.",

 "> - ★★ ③ **THE 256,000 WALL WORDING IS SWEPT on *\"do it\"* — 58 → 42, and ZERO of the 42 "
 "assert a wall.** ⛔ **NO NUMBER MOVED** (`BUDGET_HARD` still `256_000`). Dave's `says` fields "
 "UNTOUCHED; 6 records ANNOTATED by appended clause, never re-worded. Generated surfaces "
 "REGENERATED.",

 "> - ★★★ ④ **BOOT COLD 74,120 v 73,832, Δ +288 ⇒ THE −7,031 CONNECTOR LEVER IS A MEASURED "
 "EFFECT (n=2)**, meeting the acceptance test #286 wrote for itself (prior spread 11,526). "
 "⛔ **12th reading over the 70,000 ceiling — SHRINK-ONLY, NOT a re-base.**",

 "> - ⬛★★★ ⑤ **HIS WRAP CALL, AND #288 OPENS ON THE THIRD:** Mono's 0 **DOUBTED** — a proper "
 "review and **BUILD the `s219-D3` arm** (*\"the one-shot design to not disappoint\"*) · the "
 "template's **QUALITY** reviewed · **A STRAND MAP OF APOLLO AND A PATH TO FRIDAY THE 25th**. "
 "⛔ **2 carried unanswered: inline styles (88 raw), template status.**",

 "> - ⚙ ⑥ FILL **181,277 / 24** v **180,375 / 23 DECLARED**, Δ **902** — ⛔ **+1,277 on 180,000**; "
 "✅ 220,000 and 256,000 clear. **subs 573,531 (n=5)**, all `Agent`/opus/depth 1, none in seat; "
 "⚠ **`read_fill` reads 568,179 — two definitions, both published**. ⛔ **6 gate fails, `#243` "
 "form, 13th.** CI + ⏱ DELTA.",
]

RESIDUAL = (
 "> **residual → #288:** ⬛ **THE STRAND MAP AND THE PATH TO FRIDAY THE 25TH** [NEW — 0, DAVE'S] "
 "— his order at the wrap call. `s225-D2`. **{N} items, 12 new, 4 STRUCK**, `_CARRIES.md` § "
 "`residual → #288` `carries:residual-288`. PROBE `PYTHONPATH=knowledge python3 -c \"import "
 "_capture_gate as c;print(len(c._carry_items([l for l in open('_CARRIES.md') if '#288:**' in "
 "l][0])))\"` = {N}. ⚠ **ALL 12 NEW INVISIBLE TO THE PROBE, 10th wrap** (`_AGE_RE` misses "
 "`[NEW — 0]`); 551→{N} is #286's 9 ageing in. **4 STRIKES: the two sentences, the field key "
 "and the explorer, the 58 locations, the DRAFT line** — each receipted (`s183-D1`/`s188-D2`); "
 "⛔ **the connector-lever item is NOT struck** (its headline stays true).")


def build(n_carries: int, generated: str) -> str:
    res = RESIDUAL.replace("{N}", str(n_carries))
    return "\n".join([HEAD, ">"] + BULLETS + [res, generated])


def measure(text: str):
    tk = cg.measure_tokens(text)[0]
    ln = [l for l in text.splitlines() if l.strip() not in ("", ">")]
    return tk, len(ln)


if __name__ == "__main__":
    gen = subprocess.run(["python3", os.path.join(ROOT, "knowledge", "_roll_state.py")],
                         capture_output=True, text=True, cwd=ROOT).stdout.strip()
    assert gen.startswith("> **residual (GENERATED"), gen[:80]
    n = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 563
    text = build(n, gen)
    tk, ln = measure(text)
    cap_tk, cap_ln = cg.BANNER_LATEST_CAP_TK, cg.BANNER_LATEST_CAP_LINES
    print(f"banner: {tk:,} tape / {ln} substantive lines   "
          f"(cap {cap_tk:,} / {cap_ln})  -> {'OK' if tk <= cap_tk and ln <= cap_ln else 'OVER'}")
    print(f"  headroom: {cap_tk - tk:+,} tape · {cap_ln - ln:+d} lines")
    print(f"  GENERATED line (from _roll_state.py, byte-identical): {gen[:110]}")
    if "--emit" in sys.argv:
        open(os.path.join(HERE, "banner287.md"), "w", encoding="utf-8").write(text + "\n")
        print("WROTE banner287.md")
