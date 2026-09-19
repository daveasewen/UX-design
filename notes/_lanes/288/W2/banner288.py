#!/usr/bin/env python3
"""#288 wrap — build the ★ LATEST banner and MEASURE it with the GATE'S OWN instrument.

`s241-D2` is BLOCKING at 10 substantive lines / 1,200 tape over the whole banner block.
The pre-check here calls `_capture_gate.measure_tokens` and counts lines exactly as
`check_budgets()` does (blank and `>`-only lines are free), so the pre-check and the gate
cannot disagree — and the GENERATED residual line is substituted from `_roll_state.py`
BEFORE measuring, because that line is inside the block the gate charges.
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "knowledge"))
import _capture_gate as cg

HEAD = ("> ## ★ LATEST — 2026-09-19 (Sat **#288**, Fable 5.1, 5 Opus lanes, DELEGATED wrap — "
        "★★ **APOLLO COMPOSES, NOT TRACES — AND HE NAMES THE DEFECT CLASS**)")

BULLETS = [
 "> - ⓪ ✅ **NO DATE SPLIT** (09-19). ⛔ **NO LANE COMMITTED — this wrap is #288's ONLY commit** "
 "staging all 5 lanes + 3 inherited dirty paths. ⛔ **`_HANDOFF-139` FIRST — IT OUTRANKS "
 "`_CHAIN.md`**; #130–#138 stand, **NOTHING struck**. Words: `notes/_lanes/288/`.",

 "> - ⛔★★★ ① **NO RULING INSCRIBED — `_rulings.json` STAYS 622**, `json.load` here, no `s288-` "
 "id. **He did not say *inscribe* today**, so all TEN ruling-shaped things carry as QUESTIONS PUT "
 "(`s271-D4`), never as states of the world.",

 "> - ★★★ ② **HE CHALLENGED THE PREMISE, THEN RULED BY EYE THAT IT COMPOSES.** Template: "
 "***\"this isn't Apollo its a dot-to-dot book\"***. Probe: ***\"at least it's diverged from the "
 "tamplete\"*** and ***\"working the way I'd have expected\"***. ⛔ **METHOD endorsed, EXECUTION "
 "not — and HE names the class: *\"its all about alignment spacing and dimensions\"*.** He "
 "writes the test brief himself.",

 "> - ★★ ③ **THE `s219-D3` ARM IS BUILT** — lane A's `knowledge/canon/gen_bento_role_vars.py`, "
 "FIRST consumer of `_bento_edit_rails.json` (`$groundwork_only`, un-consumed since "
 "#219). Per-theme `--bento-dashboard-main/-sub` minted before `AUTO-THEMES START`; the "
 "snippet's `:802`/`:804` literals become `var()`; four-theme rendered proof. ⛔ **Mono's 0 is "
 "NOT ruled and no winner picked.**",

 "> - ★★ ④ **THREE MORE DELIVERABLES FOR HIS EYE, FILED.** **strand map** "
 "`notes/_STRAND-MAP-2026-09-19.html` — 13 sections, 41 cited paths exist, Friday's event "
 "NOT ESTABLISHED · **four-theme gutter sheet** `notes/_lanes/288/B/four-themes.html`, "
 "read at HEAD, 16 PNGs + 16 crops · **template quality review** — *the drawn page is "
 "sound, the paperwork is not*, 4 of the meta's 5 `$status` claims FALSE.",

 "> - ⚠★★ ⑤ **THE PROBE MEASURED WHAT NO GATE SEES.** 39 reads, 0 fenced, 10 gaps. Canon's "
 "instance-dial recipe **loses silently** — `.c-bento.wall-ops` (0,2,0) v the `:has()` rule "
 "(0,4,0), 0px not 40 · canon **clips with `pageErrors: []`** · **no gate reads a page LINKING "
 "`canon.css`**. ⛔ **The frozen demo prompt is NOT recoverable — the two probe pages answer "
 "DIFFERENT briefs, said on the sheet.**",

 "> - ⚙ ⑥ FILL **{FILL} / {TURNS}** v **180,585 / 27 DECLARED**, Δ **{DELTA}** — ⛔ **+17,234 on "
 "180,000**; ✅ 220,000 and 256,000 clear. BOOT **74,174**, to the token. **subs {SUBS} (n=5)** "
 "by the log's convention, **{SUBSRF} by `read_fill`** — 2 definitions, both published, gap "
 "{SUBSGAP} per-lane. ⛔ **6 gate fails, `#243` form, 14th.** CI + ⏱ DELTA.",
]

RESIDUAL = (
 "> **residual → #289:** ⬛ **APOLLO COMPOSES AND THE SLOPPINESS IS ALIGNMENT SPACING AND "
 "DIMENSIONS** [NEW — 0, DAVE'S] — his verdict by eye on the probe. `s225-D2`. **{N} items, 17 "
 "new, 0 STRUCK**, `_CARRIES.md` § `residual → #289` `carries:residual-289`. PROBE "
 "`PYTHONPATH=knowledge python3 -c \"import _capture_gate as c;print(len(c._carry_items([l for "
 "l in open('_CARRIES.md') if '#289:**' in l][0])))\"` = {N}. ⚠ **ALL 17 NEW INVISIBLE TO THE "
 "PROBE, 11th wrap** (`_AGE_RE` misses `[NEW — 0]`); 560→{N} is #288's 12 ageing in. ⛔ **ZERO "
 "STRIKES AND THE ZERO IS A JUDGMENT** — reason in new item ⑩ and the ⏱ DELTA (`s271-D4`).")

VALS = {
 "{FILL}": "197,234", "{TURNS}": "33", "{DELTA}": "16,649",
 "{SUBS}": "1,004,095", "{SUBSRF}": "998,602", "{SUBSGAP}": "5,493",
}


def build(n_carries: int, generated: str) -> str:
    out = [HEAD, ">"]
    for b in BULLETS:
        for k, v in VALS.items():
            b = b.replace(k, v)
        out.append(b)
    out.append(RESIDUAL.replace("{N}", str(n_carries)))
    out.append(generated)
    return "\n".join(out)


def measure(text: str):
    tk = cg.measure_tokens(text)[0]
    ln = [l for l in text.splitlines() if l.strip() not in ("", ">")]
    return tk, len(ln)


if __name__ == "__main__":
    gen = subprocess.run(["python3", os.path.join(ROOT, "knowledge", "_roll_state.py")],
                         capture_output=True, text=True, cwd=ROOT).stdout.strip()
    assert gen.startswith("> **residual (GENERATED"), gen[:120]
    n = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 572
    text = build(n, gen)
    tk, ln = measure(text)
    cap_tk, cap_ln = cg.BANNER_LATEST_CAP_TK, cg.BANNER_LATEST_CAP_LINES
    print(f"banner: {tk:,} tape / {ln} substantive lines   "
          f"(cap {cap_tk:,} / {cap_ln})  -> {'OK' if tk <= cap_tk and ln <= cap_ln else 'OVER'}")
    print(f"  headroom: {cap_tk - tk:+,} tape · {cap_ln - ln:+d} lines")
    print(f"  GENERATED line: {gen[:120]}")
