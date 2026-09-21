#!/usr/bin/env python3
"""#292 wrap — build the `_LIVE-STATE.md` ops file (ritual step 1 + 2d).

FOUR things happen and every one is a MOVER op:
  (1) the #289 ⏱ PRIOR DELTA block MOVES verbatim to `_LIVE-STATE-ARCHIVE.md` (2d keeps
      LATEST + 2 PRIOR; adding #292 makes #289 the fourth);
  (2) the #291 delta heading is DEMOTED from ⏱ LATEST to ⏱ PRIOR;
  (3) the #292 ⏱ LATEST DELTA is inserted above it;
  (4) the `Last refreshed` chain line gains the #292 stamp and SHEDS its oldest segment
      (#288's), which is moved verbatim into the same archive section.

⚠ THE VERBATIM GUARANTEE ON (4) IS MECHANICAL, NOT EDITORIAL: the shed segment is a SLICE of
the old line located by marker SEARCH, never re-typed, and a post-condition asserts the slice is
absent from the projected replacement and present in the projected archive text. Every
pre-condition tests the INPUT (the #285 lesson).
"""
import json
import os
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
LS = os.path.join(ROOT, "_LIVE-STATE.md")
DELTA = os.path.join(HERE, "delta292.md")

ls = open(LS, encoding="utf-8").read().split("\n")

# ---- locate the chain line -------------------------------------------------------------------
chain_idx = [i for i, l in enumerate(ls)
             if l.startswith("*Last refreshed: 2026-09-21 (Mon from `date` — **#291 wrap**")]
assert len(chain_idx) == 1, chain_idx
chain = ls[chain_idx[0]]

# the oldest full segment on the chain is #287's — it begins at this marker and runs to the
# first trim-note that follows it.
SEG_START = " Previous: *Last refreshed: 2026-09-19 (Sat from `date` — **#288 wrap**"
TRIM_MARK = " *Last refreshed (#287, trimmed at the #291 wrap)"
a = chain.index(SEG_START)
b = chain.index(TRIM_MARK)
assert a < b, (a, b)
segment = chain[a:b]
assert "#288 wrap" in segment and "#289 wrap" not in segment, "slice caught the wrong segment"
assert len(segment) > 3000, f"segment implausibly small ({len(segment)} B)"

TRIM_NOTE = (" *Last refreshed (#288, trimmed at the #292 wrap): #288's `Previous:` chain segment "
             "was moved VERBATIM to `_LIVE-STATE-ARCHIVE.md` § Rolled 2026-09-21 #292, in the same "
             "section as the #289 ⏱ delta block this wrap rolled. Nothing was deleted — moved.*")

STAMP = open(os.path.join(HERE, "stamp292.txt"), encoding="utf-8").read().strip()

new_chain = STAMP + " Previous: " + chain[:a] + TRIM_NOTE + chain[b:]
assert segment not in new_chain, "POST-CONDITION FAILED: the shed segment survived in the replacement"
assert chain[:a] in new_chain and chain[b:] in new_chain, "POST-CONDITION FAILED: a kept part was lost"

delta = open(DELTA, encoding="utf-8").read().rstrip("\n").split("\n")

ARCH_HEAD = "## Rolled 2026-09-21 #292 (2d, at the #292 wrap) — via the mover"

latest = [l for l in ls if l.startswith("## ⏱ LATEST DELTA — 2026-09-21")]
assert len(latest) == 1, latest

ops = [
    # (e) the archive section heading, newest-first, BEFORE #290's
    {"op": "insert", "file": "_LIVE-STATE-ARCHIVE.md",
     "at": "## Rolled 2026-09-21 #291 (2d, at the #291 wrap) — via the mover",
     "where": "before",
     "lines": [ARCH_HEAD, "",
               "### #288's `Previous:` chain segment — moved VERBATIM at the #292 wrap (`Last refreshed` trim)",
               "", segment.strip(), ""]},
    # (1) the #288 delta block moves under it
    {"op": "move", "src": "_LIVE-STATE.md",
     "start": "## ⏱ PRIOR DELTA — 2026-09-20 (Sun from `date`) (**#289**",
     "end": "## 🕓 OPEN — Latin Univers **WEBFONT**",
     "dst": "_LIVE-STATE-ARCHIVE.md", "at": ARCH_HEAD, "where": "after"},
    # (2) demote #290
    {"op": "replace", "file": "_LIVE-STATE.md",
     "find": [latest[0]],
     "replace": [latest[0].replace("## ⏱ LATEST DELTA —", "## ⏱ PRIOR DELTA —", 1)]},
    # (3) the new #291 delta above it
    {"op": "insert", "file": "_LIVE-STATE.md",
     "at": "## ⏱ PRIOR DELTA — 2026-09-21 (Mon from `date`) (**#291**", "where": "before",
     "lines": delta + [""]},
    # (4) the chain line
    {"op": "replace", "file": "_LIVE-STATE.md", "find": [chain], "replace": [new_chain]},
]

out = os.path.join(HERE, f"ops-292-ls-{int(time.time())}.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(ops, f, ensure_ascii=False, indent=1)
assert os.path.exists(out) and os.path.getsize(out) > 200
print(f"WROTE {out}  {os.path.getsize(out):,} B  {len(ops)} ops")
print(f"  shed segment {len(segment):,} B · new delta {len(delta)} lines")
