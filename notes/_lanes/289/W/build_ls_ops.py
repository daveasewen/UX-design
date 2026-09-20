#!/usr/bin/env python3
"""#289 wrap — build the `_LIVE-STATE.md` ops file (ritual step 1 + 2d).

FOUR things happen and every one is a MOVER op:
  (1) the #286 ⏱ PRIOR DELTA block MOVES verbatim to `_LIVE-STATE-ARCHIVE.md` (2d keeps
      LATEST + 2 PRIOR; adding #289 makes #286 the fourth);
  (2) the #288 delta heading is DEMOTED from ⏱ LATEST to ⏱ PRIOR;
  (3) the #289 ⏱ LATEST DELTA is inserted above it;
  (4) the `Last refreshed` chain line gains the #289 stamp and SHEDS its oldest segment
      (#285's), which is moved verbatim into the same archive section.

⚠ THE VERBATIM GUARANTEE ON (4) IS MECHANICAL, NOT EDITORIAL: the shed segment is a SLICE of
the old line located by marker SEARCH, never re-typed, and a post-condition asserts the slice is
absent from the projected replacement and present in the projected archive text. Every
pre-condition tests the INPUT (the #285 lesson: a guard that tests its own projection fires on
correct behaviour).
"""
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
LS = os.path.join(ROOT, "_LIVE-STATE.md")
DELTA = os.path.join(HERE, "delta289.md")

ls = open(LS, encoding="utf-8").read().split("\n")

# ---- locate the chain line -------------------------------------------------------------------
chain_idx = [i for i, l in enumerate(ls) if l.startswith("*Last refreshed: 2026-09-19 (Sat from `date` — **#288 wrap**")]
assert len(chain_idx) == 1, chain_idx
chain = ls[chain_idx[0]]

# the oldest full segment on the chain is #285's — it begins at this marker and runs to the
# first trim-note that follows it.
SEG_START = " Previous: *Last refreshed: 2026-09-18 (Fri from `date` — **#285 wrap**"
TRIM_MARK = " *Last refreshed (#284, trimmed at the #288 wrap)"
a = chain.index(SEG_START)
b = chain.index(TRIM_MARK)
assert a < b, (a, b)
segment = chain[a:b]
assert "#285 wrap" in segment and "#286 wrap" not in segment, "slice caught the wrong segment"
assert len(segment) > 4000, f"segment implausibly small ({len(segment)} B)"

TRIM_NOTE = (" *Last refreshed (#285, trimmed at the #289 wrap): #285's `Previous:` chain segment "
             "was moved VERBATIM to `_LIVE-STATE-ARCHIVE.md` § Rolled 2026-09-20 #289, in the same "
             "section as the #286 ⏱ delta block this wrap rolled. Nothing was deleted — moved.*")

STAMP = open(os.path.join(HERE, "stamp289.txt"), encoding="utf-8").read().strip()

new_chain = STAMP + " Previous: " + chain[:a] + TRIM_NOTE + chain[b:]
assert segment not in new_chain, "POST-CONDITION FAILED: the shed segment survived in the replacement"
assert chain[:a] in new_chain and chain[b:] in new_chain, "POST-CONDITION FAILED: a kept part was lost"

delta = open(DELTA, encoding="utf-8").read().rstrip("\n").split("\n")

ARCH_HEAD = "## Rolled 2026-09-20 #289 (2d, at the #289 wrap) — via the mover"

ops = [
    # (e) the archive section heading, newest-first, BEFORE #288's
    {"op": "insert", "file": "_LIVE-STATE-ARCHIVE.md",
     "at": "## Rolled 2026-09-19 #288 (2d, at the #288 wrap) — via the mover",
     "where": "before",
     "lines": [ARCH_HEAD, "",
               "### #285's `Previous:` chain segment — moved VERBATIM at the #289 wrap (`Last refreshed` trim)",
               "", segment.strip(), ""]},
    # (1) the #286 delta block moves under it
    {"op": "move", "src": "_LIVE-STATE.md",
     "start": "## ⏱ PRIOR DELTA — 2026-09-18 (Fri from `date`) (**#286**",
     "end": "## 🕓 OPEN — Latin Univers **WEBFONT**",
     "dst": "_LIVE-STATE-ARCHIVE.md", "at": ARCH_HEAD, "where": "after"},
    # (2) demote #288
    {"op": "replace", "file": "_LIVE-STATE.md",
     "find": [ls[[i for i, l in enumerate(ls) if l.startswith("## ⏱ LATEST DELTA — 2026-09-19")][0]]],
     "replace": [ls[[i for i, l in enumerate(ls) if l.startswith("## ⏱ LATEST DELTA — 2026-09-19")][0]]
                 .replace("## ⏱ LATEST DELTA —", "## ⏱ PRIOR DELTA —", 1)]},
    # (3) the new #289 delta above it
    {"op": "insert", "file": "_LIVE-STATE.md",
     "at": "## ⏱ PRIOR DELTA — 2026-09-19 (Sat from `date`) (**#288**", "where": "before",
     "lines": delta + [""]},
    # (4) the chain line
    {"op": "replace", "file": "_LIVE-STATE.md", "find": [chain], "replace": [new_chain]},
]

out = os.path.join(HERE, f"ops-289-ls-{int(time.time())}.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(ops, f, ensure_ascii=False, indent=1)
assert os.path.exists(out) and os.path.getsize(out) > 200
print(f"WROTE {out}  {os.path.getsize(out):,} B  {len(ops)} ops")
print(f"  shed segment {len(segment):,} B · new delta {len(delta)} lines")
