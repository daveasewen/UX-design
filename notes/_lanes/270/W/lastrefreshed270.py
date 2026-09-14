#!/usr/bin/env python3
"""#270 wrap — step 1 + 2d's second half. Sibling of notes/_lanes/269/W/lastrefreshed269.py.

(a) Demote `## ⏱ LATEST DELTA` (#269) to `## ⏱ PRIOR DELTA` and insert #270's block in front.
(b) Trim the `Previous:` chain at the LATEST+2 boundary. ⚠ TWO segments move as ONE unit here and
    the reason is written into the replacement note: the `dream pass 12` stamp sits immediately
    above #267's and its own text says "the #267 wrap stamp that follows stands verbatim", so
    moving #267's alone would leave a pointer at nothing.

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
assert "**#269**" in lines[li[0]], lines[li[0]][:120]
lines[li[0]] = lines[li[0]].replace("## ⏱ LATEST DELTA — ", "## ⏱ PRIOR DELTA — ", 1)

DELTA = io.open(os.path.join(HERE, "delta270.txt"), encoding="utf-8").read().rstrip("\n")
assert "{{" not in DELTA
lines = lines[:li[0]] + DELTA.split("\n") + [""] + lines[li[0]:]

# ---- (b) the Previous: chain --------------------------------------------------------------------
idx = [i for i, l in enumerate(lines) if l.startswith("*Last refreshed: ")]
assert len(idx) == 1, idx
i = idx[0]
line = lines[i]

WRAP269 = "*Last refreshed: 2026-09-14 (Mon from `date` — **#269 wrap**."
assert line.startswith(WRAP269), line[:140]

START = "  Previous: 2026-09-13 (Sun from `date` — **dream pass 12**"
END = "  *Last refreshed (#266, trimmed at the #269 wrap):"
assert line.count(START) == 1, line.count(START)
assert line.count(END) == 1, line.count(END)
a = line.index(START)
b = line.index(END)
assert a < b, (a, b)
seg = line[a:b]
assert len(seg) > 2000, len(seg)
assert "**#267 wrap**" in seg

NOTE = ("  *Last refreshed (#267 + dream pass 12, trimmed at the #270 wrap): #267's `Previous:` "
        "chain segment AND the `dream pass 12` stamp immediately above it were moved VERBATIM, "
        "as ONE unit, to `_LIVE-STATE-ARCHIVE.md` § Rolled 2026-09-14 #270, in the same section "
        "as #267's ⏱ delta block. They moved together because the dream-pass line's own text "
        "says \"the #267 wrap stamp that follows stands verbatim\" and would otherwise point at "
        "nothing. Nothing was deleted — moved.*")

NEW = io.open(os.path.join(HERE, "lastrefreshed270.txt"), encoding="utf-8").read().strip()

tail = line[:a] + NOTE + line[b:]                     # #269 stamp onwards, trimmed at #267
assert tail.startswith(WRAP269)
tail = "  Previous: " + tail[len("*Last refreshed: "):]
lines[i] = "*Last refreshed: " + NEW + tail
io.open(LS, "w", encoding="utf-8").write("\n".join(lines))

# --- the moved segment lands in the archive, verbatim, in the #270 section -----------------------
at = io.open(ARCH, encoding="utf-8").read().split("\n")
anchor = "## Rolled 2026-09-14 #270 (2d, at the #270 wrap) — via the mover"
j = [k for k, l in enumerate(at) if l.startswith(anchor)]
assert len(j) == 1, j
blk = ["",
       "### `Previous:` chain segments for the `dream pass 12` stamp and #267 — MOVED VERBATIM, "
       "AS ONE UNIT, from `_LIVE-STATE.md`'s `Last refreshed` line at the #270 wrap (2d boundary, "
       "LATEST + 2 PRIOR). They moved together because the dream-pass stamp's own text points at "
       "the #267 stamp that follows it. Nothing was deleted; the live line carries a trimmed note "
       "pointing here.",
       "",
       seg.strip(),
       ""]
at = at[:j[0] + 1] + blk + at[j[0] + 1:]
io.open(ARCH, "w", encoding="utf-8").write("\n".join(at))
print("delta #270 inserted at line %d; moved %d chars of dream-12 + #267 Previous segment; new "
      "Last refreshed line %d chars" % (li[0] + 1, len(seg), len(lines[i])))
