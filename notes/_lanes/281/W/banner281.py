# -*- coding: utf-8 -*-
"""#281 wrap — the ★ LATEST banner text, held in ONE place and MEASURED before it is written.
`s214-D6` commands SHORTER, never decide-what-to-drop. `s241-D2` cap: 10 substantive lines /
1,200 tape. #280 closed at 1,158 over 10 — 42 tape of headroom — so this file prints its own
measurement and the wrap reads it before the mover is called."""
HEAD = ("> ## ★ LATEST — 2026-09-17 (Thu **#281**, Fable 5.1, 6 Opus lanes, DELEGATED wrap "
        "— ★★ **THE ORPHAN PLAN, SIX RULINGS, AND THE BRAIN LEARNS WHY**)")

BULLETS = [
 "> - ⓪ ✅ **NO DATE SPLIT** (09-17). **9 unpushed**. ⛔ **`_HANDOFF-132` FIRST — IT OUTRANKS `_CHAIN.md`**; #130's four and #131's stand EXCEPT **census export CLOSED** (11:02Z, enacted); **the eye-check STILL NOT DONE**. Words + 3 exports: `notes/_lanes/281/`.",
 "> - ★ ① **SIX RULINGS 607→613**, by span, **ZERO deletions**, each by its lane (`22 0` `52 0` `47 0` `28 0`): research families are NODES · the guideline family owns a double-named file · **`restsOn` rule→ux is AUTHORED** · a design's citation draws in the third view · triad = SYSTEM · GOVERNANCE · THEORY · many-to-many, **a rule NOTE is not a rule EDIT**.",
 "> - ★ ② explorer **1.20→1.25**, 9 commits, dark **157→8**: CM families on six edge types · PH 32 family nodes, 145 `inFamily`, 134 `evidencedBy` · RO the 59-card page, **nothing landed by design** · FO 14 files tied, 5 re-homed, set 06 **24→0** · TV 14 citations + the triad + `$why`×168 · RL **65 `restsOn` + 8 nulls, 52 of 59 rules**. **Every sha in the ⏱ DELTA** — pointer, not omission.",
 "> - ★ ③ METHOD: **ask with a page, take the answer whole.** Census → **ORPHAN PLAN**; **his 11:02Z export took ALL ELEVEN**; five decisions 11:58Z all (a) — *\"these all look good to me\"* — then **59 cards 14:49Z**. ⇒ **the brain learns WHY, in his words.**",
 "> - ⛔ ④ HIS, OPEN (questions put): **15 rule notes** (`…/rests-on-land/RULE-NOTES-2026-09-17.md`) — **#282's first** · **the eye-check, from #131, STILL not done** · force by grade + ghost colour · FO's 2 untied artefacts + repo-tool family (`W-281fo`) · ASKs `col26-012` `aid-009` `type26-002`, `type26-003` unlanded · **the LOGO REVIEW, said TWICE today**, parked since #277.",
 "> - ⚙ ⑤ FILL **261,606 real / 56** vs **256,287 / 54 DECLARED**, Δ **5,319** (same window). ⛔⛔ **256,000 HARD LINE BREACHED BY 5,606**, 81,606 past the ruled 180,000, **41,606 outside tolerance** — declared from 232,843 on while lanes kept being cut. BOOT **77,400 n=1**. ★ **subs 1,273,123 (n=6)**. `/sessions` **99%**. **No pace panel.** 6 reports.",
 "> - ⬛ ⑥ INHERITED: **6 blocking gate fails, `#243` form, 7th wrap** (ceiling breach + 5 boot double-counts, another seat\'s testimony) · ✅ **a 7th, stale `_RULINGS.html`, RED here, HEALED (4d)** · resolver **FAIL(6)** · ownership **2/3** · showroom **138 vs 108** HIS · **`s277-D12` NEVER STARTED, 3rd** · 2e NO-OP. Sizes, store write: ⏱ DELTA.",
]
RESIDUAL = ("> **residual → #282:** ⬛ **① THE RULE NOTES AND THE EYE-CHECK** [NEW — 0, DAVE'S] — 15 notes uninscribed, six cells unseen. "
            "`s225-D2`. **{COUNT} items, {NEW} new**, `_CARRIES.md` § `residual → #282` `carries:residual-282`. PROBE: `PYTHONPATH=knowledge python3 -c \"import _capture_gate as c;"
            "print(len(c._carry_items([l for l in open('_CARRIES.md') if '#282:**' in l][0])))\"` = {COUNT}. ⚠ **{NEW} NEW INVISIBLE TO THE PROBE, 4th wrap** (`_AGE_RE` misses `[NEW — 0]`); 515→{COUNT} is #280's six ageing to `[1]`. "
            "**ONE STRUCK, `s183-D1`/`s188-D2`** — the census export (ARRIVED, ENACTED); survivors re-minted ①–⑦.")
GEN = "> **residual (GENERATED #281):** {ROLLSTATE}"


def lines(count="521", new="7", rollstate="PENDING — written after 2c/2d/2f and the stratum"):
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
