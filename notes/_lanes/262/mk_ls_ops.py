#!/usr/bin/env python3
"""#262 wrap — generate the _LIVE-STATE.md 2d ops for `_gm_move.py`.

Ops, in order:
  1. insert the `## Rolled 2026-09-09 #262` heading into _LIVE-STATE-ARCHIVE.md (newest-first)
  2. replace the `Last refreshed` line: new #262 summary first, #261 demoted to `Previous:`,
     #259's `Previous:` segment CUT (it goes to the archive in op 3) and replaced by the
     standard trimmed-note sentence.
  3. insert #259's chain segment VERBATIM under the new archive heading
  4. move the `## ⏱ PRIOR DELTA … #259` block out of _LIVE-STATE.md into that section
  5. demote `## ⏱ LATEST DELTA … #261` to `## ⏱ PRIOR DELTA … #261`
  6. insert the new `## ⏱ LATEST DELTA … #262` block above it

Every string that must be verbatim is READ from the file, never retyped.
"""
import json
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
LS = os.path.join(ROOT, "_LIVE-STATE.md")
HERE = os.path.dirname(os.path.abspath(__file__))

lines = open(LS, encoding="utf-8").read().split("\n")

# --- locate the Last refreshed line (must be unique, and inside the 40-line header zone) -------
idx = [i for i, l in enumerate(lines[:40]) if l.startswith("*Last refreshed: ")]
assert len(idx) == 1, idx
LR = lines[idx[0]]

P259 = LR.find("Previous: 2026-09-08 (Tue from `date` — **#259 wrap**")
NOTE258 = LR.find("*Last refreshed (#258,")
assert 0 < P259 < NOTE258, (P259, NOTE258)

seg259 = LR[P259:NOTE258].rstrip()            # VERBATIM, incl. the leading "Previous: "
head = LR[len("*Last refreshed: "):P259]      # #261 body + "  Previous: " + #260 body
tail = LR[NOTE258:]                           # the stack of trimmed-notes, unchanged

new262 = open(os.path.join(HERE, "ls-lastrefreshed-262.txt"), encoding="utf-8").read().strip()
trimnote = ("*Last refreshed (#259, trimmed at the #262 wrap): #259's `Previous:` chain segment "
            "was moved VERBATIM to `_LIVE-STATE-ARCHIVE.md` § Rolled 2026-09-09 #262, in the same "
            "section as its ⏱ delta block. Nothing was deleted — moved.* ")

new_LR = "*Last refreshed: " + new262 + "  Previous: " + head + trimnote + tail
assert new_LR != LR

delta = open(os.path.join(HERE, "ls-delta-262.md"), encoding="utf-8").read().rstrip("\n").split("\n")

# --- the two heading lines, read from the file so the demote is exact -------------------------
lat = [l for l in lines if l.startswith("## ⏱ LATEST DELTA — 2026-09-09")]
assert len(lat) == 1, lat
lat261 = lat[0]
assert "**#261**" in lat261
prior261 = lat261.replace("## ⏱ LATEST DELTA —", "## ⏱ PRIOR DELTA —", 1)

ARCH_HEAD = "## Rolled 2026-09-09 #262 (2d, at the #262 wrap) — via the mover"

ops = [
    {"op": "insert", "file": "_LIVE-STATE-ARCHIVE.md",
     "at": "## Rolled 2026-09-09 #261 (2d, at the #261 wrap) — via the mover", "where": "before",
     "lines": [ARCH_HEAD, "",
               "*Chain segment trimmed from `_LIVE-STATE.md`'s `Last refreshed` line at the same "
               "2d boundary, VERBATIM:*", "", seg259, ""]},
    {"op": "replace", "file": "_LIVE-STATE.md", "find": [LR], "replace": [new_LR]},
    {"op": "move", "src": "_LIVE-STATE.md",
     "start": "## ⏱ PRIOR DELTA — 2026-09-08 (Tue from `date`) (**#259**",
     "end": "## 🕓 OPEN — Latin Univers",
     # BEFORE the #261 section, so the block lands under its OWN heading and after the chain
     # segment op 1 put there — an "after ARCH_HEAD" anchor would wedge it above that segment.
     "dst": "_LIVE-STATE-ARCHIVE.md",
     "at": "## Rolled 2026-09-09 #261 (2d, at the #261 wrap) — via the mover", "where": "before"},
    {"op": "replace", "file": "_LIVE-STATE.md", "find": [lat261], "replace": [prior261]},
    {"op": "insert", "file": "_LIVE-STATE.md", "at": prior261, "where": "before",
     "lines": delta + [""]},
]

json.dump(ops, open(os.path.join(HERE, "ls-ops.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
size = os.path.getsize(os.path.join(HERE, "ls-ops.json"))
assert size > 5000, size
print(f"wrote ls-ops.json  {size} bytes  {len(ops)} ops")
print(f"  seg259 {len(seg259)} chars · new_LR {len(new_LR)} chars (was {len(LR)})")
print(f"  delta block {len(delta)} lines")
