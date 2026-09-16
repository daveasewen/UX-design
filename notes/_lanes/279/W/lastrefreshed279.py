#!/usr/bin/env python3
"""2d boundary at the #279 wrap: MOVE #275's `Previous:` chain segment VERBATIM out of
_LIVE-STATE.md into _LIVE-STATE-ARCHIVE.md § Rolled 2026-09-16 #279. Span reconstruction
ASSERTED in this process before anything is written. The #278 shape, one session on."""
import sys
LS, AR = "_LIVE-STATE.md", "_LIVE-STATE-ARCHIVE.md"
orig = open(LS, encoding="utf-8").read()
START = "Previous: 2026-09-15 (Tue from `date` — **#275 wrap**."
END   = "*Last refreshed (#274, trimmed at the #278 wrap)"
i, j = orig.find(START), orig.find(END)
assert i != -1 and j != -1 and j > i, ("anchors", i, j)
assert orig.count(START) == 1 and orig.count(END) == 1, "anchors must be unique"
span = orig[i:j]
new = orig[:i] + orig[j:]
assert new[:i] + span + new[i:] == orig, "REFUSED — span reconstruction failed"
if "--write" not in sys.argv:
    print(f"DRY: span {len(span)} chars, {i}..{j}; reconstruction PASSED"); sys.exit(0)
note = ("\n### `Last refreshed` chain segment — #275, moved VERBATIM at the #279 wrap "
        "(2d boundary, one behind the delta roll). Nothing was deleted.\n\n*" + span.rstrip() + "\n")
ar = open(AR, encoding="utf-8").read()
H = "## Rolled 2026-09-16 #279 (2d, at the #279 wrap) — via the mover\n"
k = ar.find(H); assert k != -1, "archive section header missing"
ar = ar[:k+len(H)] + note + ar[k+len(H):]
open(AR, "w", encoding="utf-8").write(ar)
new = new.replace("*Last refreshed (#274, trimmed at the #278 wrap)",
  "*Last refreshed (#275, trimmed at the #279 wrap): #275's `Previous:` chain segment was moved "
  "VERBATIM to `_LIVE-STATE-ARCHIVE.md` § Rolled 2026-09-16 #279, in the same section as the #276 "
  "⏱ delta block this wrap rolled. Nothing was deleted — moved.*  "
  "*Last refreshed (#274, trimmed at the #278 wrap)", 1)
open(LS, "w", encoding="utf-8").write(new)
print(f"MOVED: {len(span)} chars verbatim; reconstruction PASSED before the write")
