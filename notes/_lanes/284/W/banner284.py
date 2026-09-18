#!/usr/bin/env python3
"""#284 wrap — build and MEASURE the ★ LATEST banner against the `s241-D2` cap
(10 substantive lines / 1,200 tape, cl100k), using the gate's OWN measure.

`s214-D6`: compress GIRTH, never drop an item, a carry, a declared skip or a receipt.
The ⏱ LATEST DELTA is the sole home for gauge / declared-skip / not-done detail.
"""
import os, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "knowledge"))
from _capture_gate import measure_tokens, BANNER_LATEST_CAP_LINES, BANNER_LATEST_CAP_TK

HEAD = ("> ## ★ LATEST — 2026-09-18 (Fri **#284**, Fable 5.1, 1 Opus lane, DELEGATED wrap — "
        "★★ **THE MASTERS ARE ACCEPTED; THE DISK LEVER IS FOUND; DELEGATION IS RESTATED**)")

BULLETS = [
 "> - ⓪ ✅ **NO DATE SPLIT** (09-18). **1 commit `ade8a403`, UNPUSHED at open.** ⛔ "
 "**`_HANDOFF-135` FIRST — IT OUTRANKS `_CHAIN.md`**; #130–#134 stand, **nothing closed but the "
 "masters**. Words: `notes/_lanes/284/`.",

 "> - ⛔ ① **NO RULING INSCRIBED — `_rulings.json` STAYS 620**, `json.load` here. **④ and ⑤ are the "
 "two ruling-shaped things, written as QUESTIONS PUT and NOT inscribed: that is his.**",

 "> - ★★ ② **40 MASTERS DRAWN AND ACCEPTED BY EYE — `s282-D3` ENACTED.** LM: "
 "`_gen_masters.py` (`--check` rc 0) + 40 SVGs, 8 lockups × 24/28/32/36/40 raw height, raw px w+h, "
 "**no viewBox**, grid-snapped (hexagon on h/4, stems), widths 89/104/119/133/148. His: ***\"the "
 "sheet is good BTW\"***. ⚠ B's horizontals a pixel off the H at 24/40, the lane's flaw, accepted. "
 "⛔ **NOT in `_logo_nodes.json`** (fence) — `W-284lm`'s open half.",

 "> - ⛔★★ ③ **THE DISK LEVER #283 SAID DID NOT EXIST.** `_HANDOFF-134`'s *\"NOT fixable from his "
 "Mac\"* is **RETRACTED**: the VM is a bundle on his Mac; he trashed `claudevm.bundle` (keeping "
 "`warm`), **`/sessions` 98.7% → 0.1%**, 127 dead homes gone. ★ **The session SURVIVED the "
 "rebuild**; the file said it would not. **A finding + an act, not a ruling.** Carry STRUCK, "
 "receipted.",

 "> - ⛔★ ④ **THE WINDOW FINDING, AND HIS CORRECTION.** Anthropic: this model in Cowork = **1M**, "
 "auto-compaction near the limit, connectors *\"token-intensive\"*. Re-basing was proposed; "
 "**Dave: *\"we gauged this against the messy middle problem not the 1M context window\"*** ⇒ "
 "**180,000 is the QUALITY line and STANDS; no constant moved.** ⚠ 256,000 is **no wall here** ⇒ #277/#281/#282 were QUALITY breaches — a WORDING fix, HIS, not done.",

 "> - ⬛★★ ⑤ **THE DELEGATION LAPSE, HIS WORDS:** *\"everything is Delegated … the lane is always an "
 "orchestrator and judgment layer … this seems to have been lost\"* (#57 / `s204-D1`). In-seat lane "
 "work ×4 — disk+spec ~15K · **six commit runs ~30K** · 2 screenshots · research — **only the "
 "drawing was a lane**; ★ **the lane cost the window ~300 tokens.** Fix PROPOSED, NOT BUILT.",

 "> - ⚙ ⑥ FILL **217,359 / 48** v **195,366 / 36 DECLARED**, Δ **21,993** — ⛔ **+37,359 on "
 "180,000**, ✅ **−2,641 on 220,000**, ✅ **256,000 clear (2nd)**. BOOT **80,882 n=1, 9th over "
 "the 70,000 ceiling — CUT it**. **subs 159,965 (n=1)**, no pace panel. `/sessions` **1.6%** v "
 "**0.1%** declared, both stand. ⛔ **6 inherited fails, `#243` form, 10th wrap**; a 7th was ours (a stray), "
 "moved. ⏱ DELTA.",
]

RESIDUAL = ("> **residual → #285:** ⬛ **THE DELEGATION LAPSE — EVERYTHING IS DELEGATED** [NEW — 0, "
            "DAVE'S] — ruling-shaped, NOT inscribed. `s225-D2`. **539 items, 4 new, 1 STRUCK**, "
            "`_CARRIES.md` § `residual → #285` `carries:residual-285`. PROBE: "
            "`PYTHONPATH=knowledge python3 -c \"import _capture_gate as c;print(len(c._carry_items("
            "[l for l in open('_CARRIES.md') if '#285:**' in l][0])))\"` = 539. ⚠ **4 NEW INVISIBLE "
            "TO THE PROBE, 7th wrap** (`_AGE_RE` misses `[NEW — 0]`); 538→539. **1 STRIKE: #284's disk "
            "claim, receipted** (`s183-D1`/`s188-D2`).")

GENERATED = "> **residual (GENERATED #284):** {GEN}"


def banner(gen_line):
    return "\n".join([HEAD, ">"] + BULLETS + [RESIDUAL, GENERATED.replace("{GEN}", gen_line)])


if __name__ == "__main__":
    text = banner("2c OK (banners ?/?) · 2d OK (deltas ?/?) · 2f OK (strata ?, log #283) — _roll_state.py · 2026-09-18")
    tk = measure_tokens(text)[0]
    subst = [l for l in text.splitlines() if l.strip() not in ("", ">")]
    print("banner: %d tape of %d cap · %d substantive lines of %d"
          % (tk, BANNER_LATEST_CAP_TK, len(subst), BANNER_LATEST_CAP_LINES))
    for i, l in enumerate(subst):
        print("  %2d  %5d  %s" % (i, measure_tokens(l)[0], l[:70]))
