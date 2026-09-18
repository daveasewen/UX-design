#!/usr/bin/env python3
"""#285 wrap — step 1's `*Last refreshed:*` line, and its 2d-boundary trim.

The line is ONE line of ~44K chars carrying the current session's summary plus three
`Previous:` segments. At each wrap: a new segment goes in front, the head becomes `Previous:`,
and the segment that falls past the boundary MOVES VERBATIM to `_LIVE-STATE-ARCHIVE.md`,
replaced in place by a one-sentence trimmed pointer. #285 moves **#281's** segment, the same
section as the #282 ⏱ delta block this wrap rolled.

⛔ EVERY SPAN IS ASSERTED IN THIS PROCESS BEFORE ANYTHING IS WRITTEN — `os.path.exists`, a size
floor, an exact-once span match, a byte-identity re-assertion of the extracted text against what
lands in the archive, and a post-condition that the trimmed anchor is gone from the live file.
The write itself goes through `_gm_move.py`; this file only BUILDS the two op payloads.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, HERE)
from run_ops import run

LS = os.path.join(ROOT, "_LIVE-STATE.md")
assert os.path.exists(LS) and os.path.getsize(LS) > 100_000, "REFUSED — _LIVE-STATE.md missing or tiny"

lines = open(LS, encoding="utf-8").read().split("\n")
idx = [i for i, l in enumerate(lines) if l.startswith("*Last refreshed: ")]
assert len(idx) == 1, idx
old = lines[idx[0]]

# ---- the span that moves: #281's `Previous:` segment ---------------------------------------
START = "*Last refreshed (#280, trimmed at the #284 wrap):"
head = old.index("Previous: 2026-09-17 (Thu from `date` — **#281 wrap**.")
tail = old.index(START)
seg = old[head:tail]
assert old.count(seg) == 1, "REFUSED — the #281 segment does not appear exactly once"
assert len(seg) > 2_000, f"REFUSED — the #281 segment is only {len(seg)} chars"
assert "**#281 wrap**" in seg and "**#280 wrap**" not in seg, "REFUSED — wrong segment extent"

TRIM = ("*Last refreshed (#281, trimmed at the #285 wrap): #281's `Previous:` chain segment was "
        "moved VERBATIM to `_LIVE-STATE-ARCHIVE.md` § Rolled 2026-09-18 #285, in the same section "
        "as the #282 ⏱ delta block this wrap rolled. Nothing was deleted — moved.*  ")

# ---- the new #285 head, and the demotion of #284's ------------------------------------------
NEW = ("*Last refreshed: 2026-09-18 (Fri from `date` — **#285 wrap**. ✅ **NO DATE SPLIT: the "
       "session, its two commits, this ritual and its own commit are ALL 2026-09-18.** "
       "⛔★★★ **READ `_HANDOFF-136-the-b-is-straightened-and-the-connector-answer-comes-by-act.md` "
       "FIRST — IT IS NEWER THAN `_CHAIN.md` AND OUTRANKS IT**, and it does NOT replace "
       "`_HANDOFF-130`…`-135`, whose open items still stand. ⛔★★ **NO RULING WAS INSCRIBED AND "
       "`knowledge/_rulings.json` STAYS AT 620, verified at this seat by `json.load` over the "
       "`rulings` list rather than restated.** Three ruling-shaped things are on the table and "
       "**not one is inscribed, because inscribing is Dave's**: the wording of the eight DRAFT "
       "lines in `knowledge/_standing.md`, the registration of the masters in `_logo_nodes.json` "
       "behind the `gen_kg_icons.py` fence, and the `_gauge_tokens.py` 256,000 wording fix "
       "carried from #284. ⚠ **His *\"excellent work!\"* is ENTHUSIASM, NOT A RULING** "
       "(`s271-D4`). ★★★ **THE #284 MASTERS WERE DISTORTED AND DAVE REOPENED HIS OWN "
       "ACCEPTANCE** with a 4× crop — *\"see image the word mark is distorted, look at the B\"*. "
       "Lane LM2 found TWO causes in `snap_wordmark()`: per-node snapping inside curved glyphs "
       "with the control points left unsnapped, and a wordmark that was **never scaled "
       "uniformly** (`kx/ky` up to **1.0436** — at h=32 it was drawn 4.4% wider than tall). "
       "⚠ **#284's own probes counted anti-aliased pixels and stem runs and could not see an "
       "aspect error**, so that wrap published an acceptance as a measurement of the world. "
       "Rebuilt as ONE uniform scale `s = h/85` plus ONE translation over nodes AND control "
       "points; `snapped_nodes` is 0; the 20 `hexagon-*` masters are byte-identical to HEAD. "
       "**Dave: *\"2. accept\"*** — and ⛔ **registration in `_logo_nodes.json` is STILL OWED "
       "and still his word on HOW** (row `W-285lm` OPEN, `closes_when` UNCHANGED). ★★ **THE SEAM "
       "NOW RE-QUOTES THE STANDING CONSTRAINTS** on his *\"yes to the seam re-quoting the "
       "standing constraints\"*: `_seam.py` prints a FOURTH block LAST, after SCRATCH, at the "
       "recency end — the messy-middle answer, because everything read at an opener becomes the "
       "MIDDLE the moment work starts. **8 lines · 246 cl100k**, measured here. ⛔ "
       "**`knowledge/_standing.md` IS A DRAFT and the wording of the eight is HIS** (row "
       "`W-285sc`); the seam re-quotes, it never inscribes. ✅ **LANE V, ADVERSARIAL, 16/16 "
       "PASS** — max residual **5.4e-5 px** against the Figma source — **and the commit lane was "
       "cut on that pass, not on his enthusiasm.** ⛔★ **THE CONNECTOR QUESTION WAS ANSWERED BY "
       "AN ACT: he set the built-in Browser's SEVENTEEN tools to BLOCKED** in Tool permissions "
       "and the `mcp__Claude_Browser__*` server dropped out of the conductor's tool set in the "
       "same session ⇒ **#286 reads boot COLD at the opener against today's 80,863, ONE variable "
       "changed; skills untouched BY DESIGN.** ★★ **THE DELEGATION RULE #284 FOUND BROKEN WAS "
       "OBEYED FOR A WHOLE SESSION AND THE MEASUREMENT IS THE ARGUMENT: SEVEN lanes, every one "
       "an `Agent` at `spawnDepth 1`, model opus (LM2 · SC · V · C · C2 · P · W), NO lane work "
       "in seat, and the seven lane replies cost the conductor's window 3,382 cl100k IN TOTAL** "
       "against ≈738,851 real of sub FILL. ⛔ **His sentence is still ruling-shaped and NOT "
       "inscribed.** ⚙ **GAUGE, measured at this seat against the conductor's transcript "
       "`62add8e4-a016-4881-9b21-af4571354a1e.jsonl`: FILL 197,852 real / 31 turns against "
       "191,785 / 28 DECLARED, delta 6,067** — the hand-over's cost, not a disagreement. ⛔ "
       "**180,000 PASSED by 17,852**, ✅ **22,148 inside the 220,000 tolerance**, ✅ **256,000 "
       "clear, third session running** — and per his own #284 correction the 180,000 is the "
       "QUALITY line. **BOOT 80,863 n=1 — the TENTH post-diet reading over the 70,000 ceiling; "
       "NOT a re-base, the literal is SHRINK-ONLY.** **subs 738,851 (n=7).** ⛔ **SEVEN BLOCKING "
       "GATE FAILS AT THE OPEN, SIX AT THE CLOSE** — the six are inherited (the boot-drift "
       "CEILING BREACH + five boot double-counts) and carried in the `#243` DECLARED not-a-wrap "
       "form, the ELEVENTH consecutive wrap; **a wrap may not repair them.** ⚠ **The seventh was "
       "THIS SEAT'S OWN and is closed here:** `ds-021 (C)` fired on `knowledge/_seam.py`, which "
       "gained a cl100k counting site in this session's own commit `b99d092c` and was never "
       "registered — entered as **`estimate-only`**, the `_compose_slice.py` precedent, **a "
       "DECLARATION not a ruling.** ⚠ **A WRAP SUB DIED MID-RITUAL AND WROTE NOTHING** — five "
       "reads, 90,605 real, `ENOTFOUND` at 14:52:22Z; there was no half-state, **which is luck, "
       "not design**, and whether the ritual owes a RESUME contract is his. ⚠ **`_seam.py`'s "
       "SCRATCH arm deletes a lane's own `/tmp` working files mid-run, by design and not fixed "
       "here** (lane V's note); this wrap's defence was a convention — every ops file under "
       "`notes/_lanes/285/W/` — not a guard. **Two closures with receipts and nothing else "
       "struck:** the masters' re-acceptance and the showroom re-sync (`ff354475`, 108 pages, "
       "`:is(` → `:where(`, verified by decoding all 108; **138 = 137 generator-owned + "
       "`index.html`**, so 108 ⊂ 137 ⊂ 138). Carry set `_CARRIES.md` § `residual → #286` — **543 "
       "probeable, EIGHT new, TWO struck**; ⚠ all eight new are invisible to the probe, the "
       "EIGHTH wrap running. ")


# PRE-CONDITION on the LIVE line: #284's segment is the HEAD, not already a `Previous:`.
assert old.count("Previous: 2026-09-18 (Fri from `date` — **#284 wrap**") == 0, \
    "REFUSED — #284 is already demoted; this line has been trimmed once already"
assert old.startswith("*Last refreshed: 2026-09-18 (Fri from `date` — **#284 wrap**.")

newhead = NEW + "Previous: " + old[len("*Last refreshed: "):]
# the demoted #284 head keeps its own words; only its label changes:
assert newhead.startswith("*Last refreshed: 2026-09-18 (Fri from `date` — **#285 wrap**.")
assert "Previous: 2026-09-18 (Fri from `date` — **#284 wrap**." in newhead, "REFUSED — #284 was not demoted"

final = newhead.replace(seg, TRIM, 1)
assert final.count("**#281 wrap**") == 0, "REFUSED — the #281 segment survived the trim"
assert seg in newhead and seg not in final, "REFUSED — the trim did not remove exactly the span"

ops = [
    {"op": "insert", "file": "_LIVE-STATE-ARCHIVE.md",
     "at": "## Rolled 2026-09-18 #285 (2d, at the #285 wrap) — via the mover", "where": "after",
     "lines": ["",
               "### #281's `Previous:` chain segment — moved VERBATIM at the #285 wrap (`Last refreshed` trim)",
               "", seg.rstrip(), ""]},
    {"op": "replace", "file": "_LIVE-STATE.md", "find": [old], "replace": [final]},
]
print(f"#281 segment: {len(seg)} chars · new head: {len(NEW)} chars · final line: {len(final)} chars "
      f"(was {len(old)})")
sys.exit(run("lastrefreshed", ops, write="--write" in sys.argv, min_bytes=5_000))
