#!/usr/bin/env python3
"""#289 wrap — the CORRECTION ops: three lines that asserted an eighth gate fail, plus the
GENERATED residual substitution.

WHY THIS FILE EXISTS, said plainly rather than smoothed away: this wrap measured #288's rolling
stratum with a `grep`-style count, read THREE mentions of the first-turn figure, and drafted the
delta, the stamp and the banner around *"an eighth fail was born and #288's prediction is
falsified"*. **Then the gate's OWN parser was run over the exact text the roll would append and
returned ONE row, and the post-roll check still read SIX double-counts.** The prediction HELD.
⇒ Every line that carried the wrong claim is corrected HERE, before the commit, through the
mover — not left standing and not quietly rewritten in a file the record would have kept.

The GENERATED line is substituted BYTE-IDENTICAL from `_roll_state.py` and anchored on a PAIR of
lines, because `> **residual (GENERATED #288):**` now matches TWICE (the #288 banner became
★ PRIOR and carries its own copy) — the #288 lesson, re-applied rather than re-learned.
"""
import json
import os
import subprocess
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))

gen = subprocess.run(["python3", os.path.join(ROOT, "knowledge", "_roll_state.py")],
                     capture_output=True, text=True, cwd=ROOT)
assert gen.returncode == 0, gen.stdout + gen.stderr
genline = gen.stdout.strip().split("\n")[-1]
assert "GENERATED #289" in genline, genline

ls = open(os.path.join(ROOT, "_LIVE-STATE.md"), encoding="utf-8").read().split("\n")
gm = open(os.path.join(ROOT, "GOOD-MORNING.md"), encoding="utf-8").read().split("\n")

fails_old = [l for l in ls if l.startswith("- ⛔ **SEVEN BLOCKING GATE FAILS STOOD AT THIS RITUAL'S OPEN")]
assert len(fails_old) == 1
stamp_old = [l for l in ls if l.startswith("*Last refreshed: 2026-09-20 (Sun from `date` — **#289 wrap**")]
assert len(stamp_old) == 1
banner_old = [l for l in gm if l.startswith("> - ⚙ ⑥ FILL **435,910")]
assert len(banner_old) == 1
pointer_old = [l for l in gm if l.startswith("> **residual → #290:**")]
assert len(pointer_old) == 1
gen_old = [l for l in gm if l.startswith("> **residual (GENERATED #288):**")]
assert len(gen_old) == 2, f"expected the pair, got {len(gen_old)}"

FAILS_NEW = (
    "- ⛔ **SEVEN BLOCKING GATE FAILS STOOD AT THIS RITUAL'S OPEN, ALL INHERITED, CARRIED IN THE "
    "`#243` DECLARED NOT-A-WRAP FORM — THE FIFTEENTH CONSECUTIVE WRAP.** The boot-drift CEILING "
    "BREACH plus six boot double-counts (#243 ×5, #264, #272, #273, #274, #287). **A wrap may not "
    "repair an inherited gate fail** and this one did not try. ✅★★ **AND NO EIGHTH WAS BORN BY "
    "THIS WRAP'S MANDATED 2f ROLL — #288'S PREDICTION HELD, AND IT WAS TESTED RATHER THAN "
    "TRUSTED.** #288 wrote *\"#289's roll should not add an eighth; that is a prediction and is "
    "labelled as one.\"* ⚠ **A RAW TEXT COUNT AT THIS SEAT LOOKED LIKE A FALSIFICATION AND WAS "
    "THE WRONG INSTRUMENT: #288's post-mortem half mentions its first-turn figure THREE times** — "
    "as the reading, as a comparison against `BOOT_CEILING_TK`, and inside a three-reading spread "
    "— **but `_parse_boot_samples` takes at most ONE reading per LINE, treats the `N over the "
    "band` shape as a COMPARISON, and requires the word boot adjacent to the number.** Run over "
    "the exact text the roll would append it returned **one row for #288**, and "
    "`boot_stratum_double_count_check` after the roll landed still reads **six**. ⇒ **Seven at "
    "the open, seven at the close.** ★ **The lesson is about method and is published because the "
    "draft of this very delta carried the wrong claim for an hour: a grep for a figure is not the "
    "gate's reading of it, and a wrap that publishes the grep inscribes a false alarm about "
    "another session's ratified testimony** [[measure-dont-convert-units]]."
)

stamp_new = stamp_old[0].replace(
    "— the FIFTEENTH consecutive wrap — AND AN EIGHTH WAS BORN BY THIS WRAP'S OWN MANDATED 2f "
    "ROLL, which falsifies #288's own prediction and is DECLARED rather than discovered.**",
    "— the FIFTEENTH consecutive wrap — AND NO EIGHTH WAS BORN BY THIS WRAP'S MANDATED 2f ROLL: "
    "#288's prediction was TESTED with the gate's own parser rather than trusted, and it HELD, "
    "seven at the open and seven at the close.**")
assert stamp_new != stamp_old[0], "the stamp's wrong clause did not match"

banner_new = banner_old[0].replace("⛔ **7 fails at open, 8 at close.**",
                                   "⛔ **7 fails at open, 7 at close, `#243` form, 15th.**")
assert banner_new != banner_old[0], "the banner's wrong clause did not match"

ops = [
    {"op": "replace", "file": "_LIVE-STATE.md", "find": [fails_old[0]], "replace": [FAILS_NEW]},
    {"op": "replace", "file": "_LIVE-STATE.md", "find": [stamp_old[0]], "replace": [stamp_new]},
    {"op": "replace", "file": "GOOD-MORNING.md", "find": [banner_old[0]], "replace": [banner_new]},
    # the GENERATED line — anchored on the PAIR (pointer line + generated line) so the ★ PRIOR
    # banner's identical copy cannot be hit
    {"op": "replace", "file": "GOOD-MORNING.md",
     "find": [pointer_old[0], gen_old[0]], "replace": [pointer_old[0], genline]},
]

out = os.path.join(HERE, f"ops-289-fix-{int(time.time())}.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(ops, f, ensure_ascii=False, indent=1)
assert os.path.exists(out) and os.path.getsize(out) > 200
print(f"WROTE {out}  {os.path.getsize(out):,} B  {len(ops)} ops")
print(f"  GENERATED line: {genline}")
