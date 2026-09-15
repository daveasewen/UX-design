#!/usr/bin/env python3
"""#272 wrap — the insertions the mover cannot do (it moves and inserts; it does not re-label a
heading in place). Each edit asserts its target count BEFORE writing, so a missed anchor fails
loudly instead of writing nothing quietly.

  1. GOOD-MORNING.md  — ★ LATEST #271 heading → ★ PRIOR, then banner272 inserted before it.
  2. GOOD-MORNING.md  — stratum272 inserted directly under `### ⏱ SESSION STRATA`.
  3. _LIVE-STATE.md   — ⏱ LATEST DELTA #271 heading → ⏱ PRIOR DELTA, delta272 before it, and
                        the `*Last refreshed:` line gets #272's stamp with #271's demoted to
                        `Previous:` — a PREPEND, nothing deleted.
  4. _LIVE-STATE.md   — 2d chain trim, one boundary behind the delta roll (the #271 wrap moved
                        #267's segment for the delta it rolled at #269): #268's `Previous:`
                        segment is CUT from the header and appended VERBATIM to
                        `_LIVE-STATE-ARCHIVE.md` § Rolled 2026-09-15 #272, with a trim note left
                        in its place. Nothing is deleted — moved.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
read = lambda p: open(os.path.join(ROOT, p), encoding="utf-8").read()
write = lambda p, t: open(os.path.join(ROOT, p), "w", encoding="utf-8").write(t)
lane = lambda n: open(os.path.join(HERE, n), encoding="utf-8").read().rstrip("\n")

# ── 1 + 2 · GOOD-MORNING.md ───────────────────────────────────────────────────────────────────
gm = read("GOOD-MORNING.md")
OLD_LATEST = "> ## ★ LATEST — 2026-09-14 (Mon **#271**,"
NEW_PRIOR = "> ## ★ PRIOR — 2026-09-14 (Mon **#271**,"
assert gm.count(OLD_LATEST) == 1, gm.count(OLD_LATEST)
gm = gm.replace(OLD_LATEST, NEW_PRIOR, 1)
assert gm.count(NEW_PRIOR) == 1

banner = lane("banner272.txt")
assert "RESIDUAL-GENERATED-PLACEHOLDER" in banner
gm = gm.replace(NEW_PRIOR, banner + "\n\n" + NEW_PRIOR, 1)

STRATA = "### ⏱ SESSION STRATA\n"
assert gm.count(STRATA) == 1, gm.count(STRATA)
stratum = lane("stratum272.txt")
gm = gm.replace(STRATA, STRATA + "\n" + stratum + "\n", 1)
write("GOOD-MORNING.md", gm)
print("GM: ★ LATEST #271 → ★ PRIOR · banner272 inserted (%d ln) · stratum272 inserted (%d ln)"
      % (len(banner.split("\n")), len(stratum.split("\n"))))

# ── 3 · _LIVE-STATE.md ────────────────────────────────────────────────────────────────────────
ls = read("_LIVE-STATE.md")
OLD_D = "## ⏱ LATEST DELTA — 2026-09-14 (Mon from `date`) (**#271**,"
NEW_D = "## ⏱ PRIOR DELTA — 2026-09-14 (Mon from `date`) (**#271**,"
assert ls.count(OLD_D) == 1, ls.count(OLD_D)
ls = ls.replace(OLD_D, NEW_D, 1)
delta = lane("delta272.txt")
ls = ls.replace(NEW_D, delta + "\n\n" + NEW_D, 1)

PREFIX = "*Last refreshed: "
lines = ls.split("\n")
idx = [i for i, l in enumerate(lines) if l.startswith(PREFIX)]
assert len(idx) == 1, idx
i = idx[0]
stamp = lane("lastrefreshed272.txt")
lines[i] = PREFIX + stamp + "*  Previous: " + lines[i][len(PREFIX):]

# ── 4 · the 2d chain trim — #268's `Previous:` segment MOVED, not deleted ──────────────────────
hdr = lines[i]
OPEN = "*  Previous: 2026-09-13 (Sun from `date` — **#268 wrap**."
CLOSE = "*  *Last refreshed (#267 + dream pass 12, trimmed at the #270 wrap):"
a = hdr.find(OPEN)
b = hdr.find(CLOSE)
assert a != -1 and b != -1 and a < b, (a, b)
segment = hdr[a:b]
NOTE = ("*  *Last refreshed (#268, trimmed at the #272 wrap): #268's `Previous:` chain segment "
        "was moved VERBATIM to `_LIVE-STATE-ARCHIVE.md` § Rolled 2026-09-15 #272, in the same "
        "section as the #269 ⏱ delta block this wrap rolled. Nothing was deleted — moved.*")
lines[i] = hdr[:a] + NOTE + hdr[b:]
ls = "\n".join(lines)
write("_LIVE-STATE.md", ls)

arch = read("_LIVE-STATE-ARCHIVE.md")
KEY = "## Rolled 2026-09-15 #272 (2d, at the #272 wrap) — via the mover\n"
assert arch.count(KEY) == 1, arch.count(KEY)
BLOCK = ("\n### `Last refreshed` chain segment — #268, moved VERBATIM at the #272 wrap (2d "
         "boundary, one behind the delta roll). Nothing was deleted.\n\n"
         + segment.strip() + "\n")
arch = arch.replace(KEY, KEY + BLOCK, 1)
write("_LIVE-STATE-ARCHIVE.md", arch)

print("LS: ⏱ LATEST #271 → ⏱ PRIOR · delta272 inserted (%d ln) · Last refreshed PREPENDED, "
      "#271's demoted to Previous (nothing deleted) · #268's Previous segment MOVED to the "
      "archive (%d chars) and replaced by a trim note"
      % (len(delta.split("\n")), len(segment)))
