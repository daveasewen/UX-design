#!/usr/bin/env python3
"""#269 wrap — step 1 + 2d's second half.

(a) Demote `## ⏱ LATEST DELTA` (#268) to `## ⏱ PRIOR DELTA` and insert #269's block in front.
(b) Trim the `Previous:` chain at the LATEST+2 boundary: the #266 segment is MOVED VERBATIM to
    `_LIVE-STATE-ARCHIVE.md` § Rolled 2026-09-14 #269 (the same section its ⏱ delta block goes
    to), replaced in place by the standing trimmed note; #268's summary is demoted from
    `*Last refreshed: ` to `Previous: `.

Nothing is deleted. Every anchor is asserted UNIQUE before it is used.
"""
import io
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
LS = os.path.join(ROOT, "_LIVE-STATE.md")
ARCH = os.path.join(ROOT, "_LIVE-STATE-ARCHIVE.md")

lines = io.open(LS, encoding="utf-8").read().split("\n")

# ---- (a) the delta ------------------------------------------------------------------------------
li = [i for i, l in enumerate(lines) if l.startswith("## ⏱ LATEST DELTA — ")]
assert len(li) == 1, li
assert "**#268**" in lines[li[0]], lines[li[0]][:120]
lines[li[0]] = lines[li[0]].replace("## ⏱ LATEST DELTA — ", "## ⏱ PRIOR DELTA — ", 1)

DELTA = io.open(os.path.join(HERE, "delta269.txt"), encoding="utf-8").read().rstrip("\n")
assert "{{" not in DELTA
lines = lines[:li[0]] + DELTA.split("\n") + [""] + lines[li[0]:]

# ---- (b) the Previous: chain --------------------------------------------------------------------
idx = [i for i, l in enumerate(lines) if l.startswith("*Last refreshed: ")]
assert len(idx) == 1, idx
i = idx[0]
line = lines[i]

WRAP268 = "*Last refreshed: 2026-09-13 (Sun from `date` — **#268 wrap**."
assert line.startswith(WRAP268), line[:140]

START = "  Previous: 2026-09-10 (Thu from `date` — **#266 wrap**."
END = "  *Last refreshed (#265, trimmed at the #268 wrap):"
assert line.count(START) == 1, line.count(START)
assert line.count(END) == 1, line.count(END)
a = line.index(START)
b = line.index(END)
assert a < b, (a, b)
seg = line[a:b]
assert len(seg) > 2000, len(seg)

NOTE = ("  *Last refreshed (#266, trimmed at the #269 wrap): #266's `Previous:` chain segment was "
        "moved VERBATIM to `_LIVE-STATE-ARCHIVE.md` § Rolled 2026-09-14 #269, in the same section "
        "as its ⏱ delta block. Nothing was deleted — moved.*")

NEW = io.open(os.path.join(HERE, "lastrefreshed269.txt"), encoding="utf-8").read().strip()

tail = line[:a] + NOTE + line[b:]                     # #268 stamp onwards, trimmed at #266
assert tail.startswith(WRAP268)
tail = "  Previous: " + tail[len("*Last refreshed: "):]
lines[i] = "*Last refreshed: " + NEW + tail
io.open(LS, "w", encoding="utf-8").write("\n".join(lines))

# --- the moved segment lands in the archive, verbatim, in the #269 section -----------------------
at = io.open(ARCH, encoding="utf-8").read().split("\n")
anchor = "## Rolled 2026-09-14 #269 (2d, at the #269 wrap) — via the mover"
j = [k for k, l in enumerate(at) if l.startswith(anchor)]
assert len(j) == 1, j
blk = ["",
       "### `Previous:` chain segment for #266 — MOVED VERBATIM from `_LIVE-STATE.md`'s "
       "`Last refreshed` line at the #269 wrap (2d boundary, LATEST + 2 PRIOR). Nothing was "
       "deleted; the live line carries a trimmed note pointing here.",
       "",
       seg.strip(),
       ""]
at = at[:j[0] + 1] + blk + at[j[0] + 1:]
io.open(ARCH, "w", encoding="utf-8").write("\n".join(at))
print("delta #269 inserted at line %d; moved %d chars of #266 Previous segment; new Last refreshed "
      "line %d chars" % (li[0] + 1, len(seg), len(lines[i])))
