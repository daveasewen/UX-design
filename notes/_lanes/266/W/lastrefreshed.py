#!/usr/bin/env python3
"""#266 wrap — 2d's second half: trim the `Previous:` chain at the LATEST+2 boundary.

The #263 `Previous:` segment is MOVED VERBATIM to `_LIVE-STATE-ARCHIVE.md` § Rolled 2026-09-10
#266 (the same section its ⏱ delta block went to), replaced in place by the standing trimmed
note, and the #265 summary is demoted from `*Last refreshed: ` to `Previous: `. Nothing is
deleted. Every anchor is asserted UNIQUE before it is used.
"""
import io
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
LS = os.path.join(ROOT, "_LIVE-STATE.md")
ARCH = os.path.join(ROOT, "_LIVE-STATE-ARCHIVE.md")

text = io.open(LS, encoding="utf-8").read()
lines = text.split("\n")
idx = [i for i, l in enumerate(lines) if l.startswith("*Last refreshed: ")]
assert len(idx) == 1, idx
i = idx[0]
line = lines[i]

START263 = "  Previous: 2026-09-09 (Wed from `date` — **#263 wrap**."
END263 = "  *Last refreshed (#262, trimmed at the #265 wrap):"
assert line.count(START263) == 1, line.count(START263)
assert line.count(END263) == 1, line.count(END263)
a = line.index(START263)
b = line.index(END263)
seg = line[a:b]
assert len(seg) > 2000, len(seg)

NOTE = ("  *Last refreshed (#263, trimmed at the #266 wrap): #263's `Previous:` chain segment was "
        "moved VERBATIM to `_LIVE-STATE-ARCHIVE.md` § Rolled 2026-09-10 #266, in the same section "
        "as its ⏱ delta block. Nothing was deleted — moved.*")

NEW = io.open(os.path.join(HERE, "lastrefreshed266.txt"), encoding="utf-8").read().strip()

rest = line[:a] + NOTE + line[b:]
assert rest.startswith("*Last refreshed: ")
rest = "  Previous: " + rest[len("*Last refreshed: "):]
lines[i] = "*Last refreshed: " + NEW + rest
io.open(LS, "w", encoding="utf-8").write("\n".join(lines))

# --- the moved segment lands in the archive, verbatim, in the #266 section -----------------------
at = io.open(ARCH, encoding="utf-8").read().split("\n")
anchor = "## Rolled 2026-09-10 #266 (2d, at the #266 wrap) — via the mover"
j = [k for k, l in enumerate(at) if l.startswith(anchor)]
assert len(j) == 1, j
blk = ["",
       "### `Previous:` chain segment for #263 — MOVED VERBATIM from `_LIVE-STATE.md`'s "
       "`Last refreshed` line at the #266 wrap (2d boundary, LATEST + 2 PRIOR). Nothing was "
       "deleted; the live line carries a trimmed note pointing here.",
       "",
       seg.strip(),
       ""]
at = at[:j[0] + 1] + blk + at[j[0] + 1:]
io.open(ARCH, "w", encoding="utf-8").write("\n".join(at))
print("moved %d chars of #263 Previous segment; new Last refreshed line %d chars"
      % (len(seg), len(lines[i])))
