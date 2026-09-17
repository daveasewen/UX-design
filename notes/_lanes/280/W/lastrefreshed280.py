#!/usr/bin/env python3
"""2d boundary at the #280 wrap: MOVE #276's `Previous:` chain segment VERBATIM out of
_LIVE-STATE.md into _LIVE-STATE-ARCHIVE.md § Rolled 2026-09-17 #280. Span reconstruction
ASSERTED in this process before anything is written. The #278/#279 shape, one session on."""
import os, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
LS = os.path.join(ROOT, "_LIVE-STATE.md")
AR = os.path.join(ROOT, "_LIVE-STATE-ARCHIVE.md")
orig = open(LS, encoding="utf-8").read()
START = "Previous: 2026-09-15 (Tue from `date` — **#276 wrap**."
END = "*Last refreshed (#275, trimmed at the #279 wrap)"
i, j = orig.find(START), orig.find(END)
assert i != -1 and j != -1 and j > i, ("anchors", i, j)
assert orig.count(START) == 1 and orig.count(END) == 1, "anchors must be unique"
span = orig[i:j]
new = orig[:i] + orig[j:]
assert new[:i] + span + new[i:] == orig, "REFUSED — span reconstruction failed"
if "--write" not in sys.argv:
    print(f"DRY: span {len(span)} chars, {i}..{j}; reconstruction PASSED"); sys.exit(0)
note = ("\n### `Last refreshed` chain segment — #276, moved VERBATIM at the #280 wrap "
        "(2d boundary, one behind the delta roll). Nothing was deleted.\n\n*" + span.rstrip() + "\n")
ar = open(AR, encoding="utf-8").read()
H = "## Rolled 2026-09-17 #280 (2d, at the #280 wrap) — via the mover\n"
k = ar.find(H)
assert k != -1, "archive section header missing — run the mover's insert op first"
ar = ar[:k + len(H)] + note + ar[k + len(H):]
open(AR, "w", encoding="utf-8").write(ar)
new = new.replace("*Last refreshed (#275, trimmed at the #279 wrap)",
  "*Last refreshed (#276, trimmed at the #280 wrap): #276's `Previous:` chain segment was moved "
  "VERBATIM to `_LIVE-STATE-ARCHIVE.md` § Rolled 2026-09-17 #280, in the same section as the #277 "
  "⏱ delta block this wrap rolled. Nothing was deleted — moved.*  "
  "*Last refreshed (#275, trimmed at the #279 wrap)", 1)
open(LS, "w", encoding="utf-8").write(new)
print(f"MOVED: {len(span)} chars verbatim; reconstruction PASSED before the write")
