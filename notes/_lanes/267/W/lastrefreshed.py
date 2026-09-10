#!/usr/bin/env python3
"""#267 wrap — step 1 + 2d's second half.

(a) Demote `## ⏱ LATEST DELTA` (#266) to `## ⏱ PRIOR DELTA` and insert #267's block in front.
(b) Trim the `Previous:` chain at the LATEST+2 boundary: the #264 segment is MOVED VERBATIM to
    `_LIVE-STATE-ARCHIVE.md` § Rolled 2026-09-10 #267 (the same section its ⏱ delta block went
    to), replaced in place by the standing trimmed note, and #266's summary is demoted from
    `*Last refreshed: ` to `Previous: `.

Nothing is deleted. Every anchor is asserted UNIQUE before it is used.
"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
LS = os.path.join(ROOT, "_LIVE-STATE.md")
ARCH = os.path.join(ROOT, "_LIVE-STATE-ARCHIVE.md")

text = io.open(LS, encoding="utf-8").read()
lines = text.split("\n")

# ---- (a) the delta ------------------------------------------------------------------------------
li = [i for i, l in enumerate(lines) if l.startswith("## ⏱ LATEST DELTA — ")]
assert len(li) == 1, li
assert "**#266**" in lines[li[0]], lines[li[0]][:120]
lines[li[0]] = lines[li[0]].replace("## ⏱ LATEST DELTA — ", "## ⏱ PRIOR DELTA — ", 1)

DELTA = io.open(os.path.join(HERE, "delta267.txt"), encoding="utf-8").read().rstrip("\n")
dofirst_tape = sys.argv[1]
dofirst_lines = sys.argv[2]
DELTA = DELTA.replace("{{DOFIRST_TAPE}}", dofirst_tape).replace("{{DOFIRST_LINES}}", dofirst_lines)
assert "{{" not in DELTA
lines = lines[:li[0]] + DELTA.split("\n") + [""] + lines[li[0]:]

# ---- (b) the Previous: chain --------------------------------------------------------------------
idx = [i for i, l in enumerate(lines) if l.startswith("*Last refreshed: ")]
assert len(idx) == 1, idx
i = idx[0]
line = lines[i]

START = "  Previous: 2026-09-09 (Wed from `date` — **#264 wrap**."
END = "  *Last refreshed (#263, trimmed at the #266 wrap):"
assert line.count(START) == 1, line.count(START)
assert line.count(END) == 1, line.count(END)
a = line.index(START)
b = line.index(END)
seg = line[a:b]
assert len(seg) > 2000, len(seg)

NOTE = ("  *Last refreshed (#264, trimmed at the #267 wrap): #264's `Previous:` chain segment was "
        "moved VERBATIM to `_LIVE-STATE-ARCHIVE.md` § Rolled 2026-09-10 #267, in the same section "
        "as its ⏱ delta block. Nothing was deleted — moved.*")

NEW = io.open(os.path.join(HERE, "lastrefreshed267.txt"), encoding="utf-8").read().strip()

rest = line[:a] + NOTE + line[b:]
assert rest.startswith("*Last refreshed: ")
rest = "  Previous: " + rest[len("*Last refreshed: "):]
lines[i] = "*Last refreshed: " + NEW + rest
io.open(LS, "w", encoding="utf-8").write("\n".join(lines))

# --- the moved segment lands in the archive, verbatim, in the #267 section -----------------------
at = io.open(ARCH, encoding="utf-8").read().split("\n")
anchor = "## Rolled 2026-09-10 #267 (2d, at the #267 wrap) — via the mover"
j = [k for k, l in enumerate(at) if l.startswith(anchor)]
assert len(j) == 1, j
blk = ["",
       "### `Previous:` chain segment for #264 — MOVED VERBATIM from `_LIVE-STATE.md`'s "
       "`Last refreshed` line at the #267 wrap (2d boundary, LATEST + 2 PRIOR). Nothing was "
       "deleted; the live line carries a trimmed note pointing here.",
       "",
       seg.strip(),
       ""]
at = at[:j[0] + 1] + blk + at[j[0] + 1:]
io.open(ARCH, "w", encoding="utf-8").write("\n".join(at))
print("delta #267 inserted; moved %d chars of #264 Previous segment; new Last refreshed line %d chars"
      % (len(seg), len(lines[i])))
