# -*- coding: utf-8 -*-
"""#280 wrap — the ★ LATEST banner text, held in ONE place and MEASURED before it is written.

`s214-D6` commands SHORTER, never decide-what-to-drop: every item, carry, declared skip and
receipt name that belongs on a banner is here, written tight. The `s241-D2` cap is 10 substantive
lines / 1,200 tape and #279 closed at 1,154 over 10 — zero headroom — so this file prints its own
measurement and the wrap reads it before the mover is called.
"""
HEAD = ("> ## ★ LATEST — 2026-09-17 (Thu **#280**, Fable 5.1, 8 Opus lane seats, DELEGATED wrap "
        "— ★★ **THE LAYOUT MATRIX, AND THE EXPLORER BECOMES THE FRONT DOOR**)")

BULLETS = [
 "> - ⓪ ⚠ **DATE SPLIT** — opened 09-16 eve, ritual+commit 09-17, nothing re-dated (#241 shape). **17 unpushed** at open. ⛔ **`_HANDOFF-131` FIRST — IT OUTRANKS `_CHAIN.md`**; #130's items stand. His five sentences, verbatim: `notes/_lanes/280/DAVE-RULINGS-2026-09-17.md`.",
 "> - ★ ① TWO RULINGS 605→607, spans `19  0`+`18  0`, ZERO deletions, each by its own lane. **`s280-D1`** (`53a91bd`) **the layout matrix**: force · strata · shells × 2D·3D, six cells, force default, on his 20:30Z export. **`s280-D2`** (`9e04796`) **the explorer is the FRONT DOOR**: INSPECT opens the artefact; SERVED, not double-clicked.",
 "> - ★ ② explorer **1.16→1.20**, 8 lanes / **17 commits, every sha in the ⏱ DELTA** (pointer, not omission): LY 1.17 strata (default pixel-identical) · LS four sketches → his export · LM 1.18 six cells + contact sheet · EX3 1.19 legend + modal · EX4 1.20 renderers, edges, `_serve_explorer.py` · IN + IN2 **14/15 twins**, `_ICON-GAPS.md`, generator refuses on disagreement (22/22, mutants 32/32) · OC the census.",
 "> - ★ ③ METHOD: **ask with a picture, then build the answer** — one option → four sketches → his export → the matrix. EX3: 1.18's bottom-strip default was **worse in 4 of 6 cells**. EX4: md5 moved **BY DATA** (5 governance nodes moved the hatch), 2×2 in-report.",
 "> - ⛔ ④ HIS, OPEN, QUESTIONS PUT: **the census export** — 10 radios, **NOT RECEIVED** (**157 of 4,618** dark, 4 causes; the biggest is a **switch left off** whose flip puts a FAMILY NODE on the stage = HIS word) · **the eye-check of the six cells** (conductor expects Floors or Orbits to go — expectation, not finding) · **`jade-lifestyle` open by his word**, lean on the null · shells-3D cutaway + sandbox snippet scripts, lane-declared out.",
 "> - ⚙ ⑤ FILL **191,294 / 28** vs **185,127 / 25 DECLARED**, Δ **6,167**; ✅ **200,000 NOT breached**; ⛔ ruled **180,000 passed by 11,294** (TOLERATED). BOOT **75,740 n=1, NOT a re-base**. ★ **subs 1,833,788 (n=8), MEASURED**. `/sessions` **99%**. 8 reports. Rest: ⏱ DELTA.",
 "> - ⬛ ⑥ NOT DONE: **7 inherited gate fails** (`#243` form, 6th wrap; ⚠ **brief says 6 — both published**) · resolver **FAIL(6)** · lane-ownership **2/3** · showroom **138 vs 108** (HIS) · **`s277-D12` never started** · 2e NO-OP · ✅ **MEMORY WRITTEN FROM THIS SEAT**, limit FALSE twice, **unedited: Dave's**. Sizes: ⏱ DELTA.",
]
RESIDUAL = ("> **residual → #281:** ⬛ **① THE CENSUS EXPORT AND THE EYE-CHECK** [NEW — 0, DAVE'S] "
            "— his ten radios, unarrived; six cells unseen. "
            "`s225-D2`. **{COUNT} items, {NEW} new**, `_CARRIES.md` § `residual → #281` "
            "`carries:residual-281`. PROBE: `PYTHONPATH=knowledge python3 -c \"import "
            "_capture_gate as c;print(len(c._carry_items([l for l in open('_CARRIES.md') if "
            "'#281:**' in l][0])))\"` — agrees at {COUNT}. ⚠ **THE {NEW} NEW ITEMS ARE INVISIBLE "
            "TO THE PROBE, DECLARED, 3rd wrap** (`_AGE_RE` misses `[NEW — 0]`); 507→{COUNT} IS "
            "#279's eight ageing to `[1]`. **TWO STRUCK, `s183-D1`/`s188-D2`** — the layout "
            "question (ANSWERED, `s280-D1`) and the 15-base export (READ, 14 of 15); survivors "
            "re-minted.")
GEN = "> **residual (GENERATED #280):** {ROLLSTATE}"


def lines(count="515", new="6", rollstate="PENDING — written after 2c/2d/2f and the stratum"):
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
