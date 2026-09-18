# -*- coding: utf-8 -*-
"""#282 wrap — the ★ LATEST banner text, held in ONE place and MEASURED before it is written.
`s214-D6` commands SHORTER, never decide-what-to-drop. `s241-D2` cap: 10 substantive lines /
1,200 tape. #281 closed at 1,199 — ONE tape of headroom — and its standing warning that the next
wrap has no room in this idiom is NOT withdrawn; this file prints its own measurement and the
wrap reads it before the mover is called."""
HEAD = ("> ## ★ LATEST — 2026-09-18 (Fri **#282**, Fable 5.1, 3 Opus lanes, DELEGATED wrap "
        "— ★★ **THE RULE NOTES LAND, THE LOGO IS RULED, THE GRAPH'S PHILOSOPHY IS PUT**)")

BULLETS = [
 "> - ⓪ ⚠ **DATE SPLIT** (09-17 → 09-18, nothing re-dated, #241 shape). **13 commits, pushed.** ⛔ **`_HANDOFF-133` FIRST — IT OUTRANKS `_CHAIN.md`**; #130/#131/#132 stand EXCEPT ✅ **eye-check CLOSED** (`6bac5e4`). Words + 2 exports: `notes/_lanes/282/`.",
 "> - ★ ① **SIX RULINGS 613→619**, by span (`34 0` `17 0` `18 0` `20 0` `33 0` `17 0`), **two amended-in-place `3 3` `2 2` BY DESIGN**: a rule NOTE becomes a rule EDIT when he says so · the red ban is on the PRIMARY red · logo size by RAW HEIGHT 24/28/32/36/40 · identifier lockup SCRAPPED · ONE logo guideline · clear space ¼ height + ¼ LOGOMARK width, up to 4px.",
 "> - ★ ② **11 GUIDELINE EDITS IN HIS OWN WORDS across 8 files** (`s282-D1`) · `_logo_nodes.json` **12→8 nodes, 27→33 edges** · explorer **1.25→1.26** · rules **470→473**, BLOCKING **59→61**, `restsOn` **73→75**. ⚠ **The brief DECLARES 474/62 and 14 commits; this seat MEASURES 473/61 and 13** — both published.",
 "> - ★ ③ METHOD, 3rd day: **ask with a page, take the answer whole.** 15 notes → a 15-row page → **14 of 15 on the recommendation** (19:10Z) · 12 lockups → a review page → **9 answered, 3 moot, 4 notes** (08:20Z). ⛔ **TWO rulings were WRONG FIRST, corrected one commit later — the superseded cut NAMED inside each, never erased.**",
 "> - ⛔ ④ HIS, OPEN (questions put): **40 per-size logo MASTERS — #283's first, specified** · **the THIRD DIAL** (layers is 1; the tone map offered as 2 and **REFUSED**; 3 unknown) · **THEORY DOOR + postures obey/weigh/argue** — *\"this all sounds great\"* is **enthusiasm, NOT a ruling** · **`col26-012` *\"Discuss first\"*** · `W-282a` `W-282b` `W-282ll`.",
 "> - ⚙ ⑤ FILL **337,559 real / 141** vs **326,763 / 137 DECLARED**, Δ **10,796** (same window). ⛔⛔ **256,000 HARD LINE BREACHED BY 81,559 — THIRD BREACH, bigger than #277+#281 together**, 157,559 past the ruled 180,000. ⛔ **The gauge was NOT READ between the logo landing and D6; two lanes cut past the wall.** BOOT **77,474 n=1**. ★ **subs 546,920 (n=3)**. **No pace panel.**",
 "> - ⬛ ⑥ INHERITED: **6 blocking gate fails, `#243` form, 8th wrap** (ceiling breach + 5 boot double-counts, another seat's testimony — **a wrap may not repair them**) · ✅ **a 7th, stale `_RULINGS.html`, HEALED (4d) — the SAME fail as #281** · resolver **FAIL(6)** · ownership **2/3** · showroom **138 vs 108** HIS · **`s277-D12` NEVER STARTED, 4th** · 2e NO-OP. Sizes, store write: ⏱ DELTA.",
]
RESIDUAL = ("> **residual → #283:** ⬛ **① THE LOGO MASTERS AND THE THIRD DIAL** [NEW — 0, DAVE'S] — 40 SVGs specified; dial 3 unnamed. "
            "`s225-D2`. **{COUNT} items, {NEW} new**, `_CARRIES.md` § `residual → #283` `carries:residual-283`. PROBE: `PYTHONPATH=knowledge python3 -c \"import _capture_gate as c;"
            "print(len(c._carry_items([l for l in open('_CARRIES.md') if '#283:**' in l][0])))\"` = {COUNT}. ⚠ **{NEW} NEW INVISIBLE TO THE PROBE, 5th wrap** (`_AGE_RE` misses `[NEW — 0]`); 521→{COUNT} = #282's eight ageing. "
            "**TWO STRUCK, `s183-D1`/`s188-D2`** — the 15 rule notes (ELEVEN inscribed) and the eye-check (**never open, his own word**); survivors re-minted ①–⑦.")
GEN = "> **residual (GENERATED #282):** {ROLLSTATE}"


def lines(count="529", new="7", rollstate="PENDING — written after 2c/2d/2f and the stratum"):
    return ([HEAD, ">"] + BULLETS
            + [RESIDUAL.replace("{COUNT}", count).replace("{NEW}", new),
               GEN.replace("{ROLLSTATE}", rollstate), ""])


if __name__ == "__main__":
    import os, sys
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "..", "..", "..", "..", "knowledge"))
    import _capture_gate as cg
    body = "\n".join(lines())
    tape = cg.measure_tokens(body)[0]
    sub = [l for l in lines() if l.strip() and l.strip() != ">"]
    print(f"BANNER MEASURE: {tape:,} tape · {len(sub)} substantive lines "
          f"(cap {cg.BANNER_LATEST_CAP_TK:,} tape / {cg.BANNER_LATEST_CAP_LINES} lines) — "
          f"{'OVER' if tape > cg.BANNER_LATEST_CAP_TK or len(sub) > cg.BANNER_LATEST_CAP_LINES else 'within'}")
