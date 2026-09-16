#!/usr/bin/env python3
"""#277 wrap, step 1 + 2d boundary — rebuild `_LIVE-STATE.md`'s `Last refreshed` line.

The #275/#276 shape, unchanged:
(a) the #273 `Previous:` segment is MOVED VERBATIM to `_LIVE-STATE-ARCHIVE.md`
    § Rolled 2026-09-16 #277 (the 2d boundary, one behind the #274 delta roll);
(b) the new #277 stamp is written in front and the #276 stamp becomes `Previous:`;
(c) a trim note for #273 is written in front of the #272…#223 trim-note run, same form.
Nothing is deleted — moved. Textual span only, with a reconstruction proof.
"""
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
LS = os.path.join(ROOT, "_LIVE-STATE.md")
LSA = os.path.join(ROOT, "_LIVE-STATE-ARCHIVE.md")

text = open(LS, encoding="utf-8").read()
lines = text.split("\n")
idx = [i for i, l in enumerate(lines) if l.startswith("*Last refreshed: ")]
assert len(idx) == 1, idx
i = idx[0]
line = lines[i]

A = line.find("  Previous: 2026-09-15 (Tue from `date` — **#273 wrap**")
B = line.find("  *Last refreshed (#272, trimmed at the #276 wrap)")
assert A > 0 and B > A, (A, B)
seg = line[A + 2 : B]                      # "Previous: … )*"  — verbatim
assert seg.startswith("Previous: 2026-09-15") and seg.endswith(")*"), (seg[:30], seg[-10:])
assert "s273-D4" in seg, "wrong segment — #273's stamp names s273-D4"

NEW = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "stamp277.txt"), encoding="utf-8").read().strip()
TRIM = ("  *Last refreshed (#273, trimmed at the #277 wrap): #273's `Previous:` chain segment was "
        "moved VERBATIM to `_LIVE-STATE-ARCHIVE.md` § Rolled 2026-09-16 #277, in the same section "
        "as the #274 ⏱ delta block this wrap rolled. Nothing was deleted — moved.*")

rest = line[len("*Last refreshed: "):]     # the #276 stamp body onward, untouched
rest = rest[: A - len("*Last refreshed: ")] + rest[B - len("*Last refreshed: ") :]
newline = "*Last refreshed: " + NEW + "*  Previous: " + rest
k = newline.find("  *Last refreshed (#272, trimmed at the #276 wrap)")
assert k > 0
newline = newline[:k] + TRIM + newline[k:]

# reconstruction proof: the untouched remainder is byte-identical to the original either side
assert line[:A] + line[B:] == ("*Last refreshed: " + rest), "span reconstruction failed"

lines[i] = newline
open(LS, "w", encoding="utf-8").write("\n".join(lines))

# ---- the archive half, verbatim -------------------------------------------------------------
a = open(LSA, encoding="utf-8").read().split("\n")
j = [n for n, l in enumerate(a) if l.startswith("## Rolled 2026-09-16 #277")]
assert len(j) == 1, j
j = j[0]
block = ["",
         "### `Last refreshed` chain segment — #273, moved VERBATIM at the #277 wrap (2d boundary, "
         "one behind the delta roll). Nothing was deleted.",
         "",
         "*" + seg]
a[j + 1 : j + 1] = block
open(LSA, "w", encoding="utf-8").write("\n".join(a))
print("LS Last refreshed: #277 stamped · #273 segment MOVED verbatim (%d chars) · trim note written" % len(seg))
print("LS line %d: %d chars -> %d chars" % (i + 1, len(line), len(newline)))
