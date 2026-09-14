#!/usr/bin/env python3
"""#271 wrap — the three insertions the mover cannot do (it moves and inserts; it does not
re-label a heading in place). Each edit asserts its target count BEFORE writing, so a missed
anchor fails loudly instead of writing nothing quietly.

  1. GOOD-MORNING.md  — ★ LATEST #270 heading → ★ PRIOR, then banner271 inserted before it.
  2. GOOD-MORNING.md  — stratum271 inserted directly under `### ⏱ SESSION STRATA`.
  3. _LIVE-STATE.md   — ⏱ LATEST DELTA #270 heading → ⏱ PRIOR DELTA, delta271 before it, and
                        the `*Last refreshed:` line gets #271's stamp with #270's demoted to
                        `Previous:` — a PREPEND, nothing deleted.
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
OLD_LATEST = "> ## ★ LATEST — 2026-09-14 (Mon **#270**,"
NEW_PRIOR = "> ## ★ PRIOR — 2026-09-14 (Mon **#270**,"
assert gm.count(OLD_LATEST) == 1, gm.count(OLD_LATEST)
gm = gm.replace(OLD_LATEST, NEW_PRIOR, 1)
assert gm.count(NEW_PRIOR) == 1

banner = lane("banner271.txt")
assert gm.count(NEW_PRIOR) == 1
gm = gm.replace(NEW_PRIOR, banner + "\n\n" + NEW_PRIOR, 1)

STRATA = "### ⏱ SESSION STRATA\n"
assert gm.count(STRATA) == 1, gm.count(STRATA)
gm = gm.replace(STRATA, STRATA + "\n" + lane("stratum271.txt") + "\n", 1)
write("GOOD-MORNING.md", gm)
print("GM: ★ LATEST #270 → ★ PRIOR · banner271 inserted (%d ln) · stratum271 inserted (%d ln)"
      % (len(banner.split("\n")), len(lane("stratum271.txt").split("\n"))))

# ── 3 · _LIVE-STATE.md ────────────────────────────────────────────────────────────────────────
ls = read("_LIVE-STATE.md")
OLD_D = "## ⏱ LATEST DELTA — 2026-09-14 (Mon from `date`) (**#270**,"
NEW_D = "## ⏱ PRIOR DELTA — 2026-09-14 (Mon from `date`) (**#270**,"
assert ls.count(OLD_D) == 1, ls.count(OLD_D)
ls = ls.replace(OLD_D, NEW_D, 1)
delta = lane("delta271.txt")
ls = ls.replace(NEW_D, delta + "\n\n" + NEW_D, 1)

PREFIX = "*Last refreshed: "
lines = ls.split("\n")
idx = [i for i, l in enumerate(lines) if l.startswith(PREFIX)]
assert len(idx) == 1, idx
i = idx[0]
stamp = lane("lastrefreshed271.txt")
lines[i] = PREFIX + stamp + "*  Previous: " + lines[i][len(PREFIX):]
ls = "\n".join(lines)
write("_LIVE-STATE.md", ls)
print("LS: ⏱ LATEST #270 → ⏱ PRIOR · delta271 inserted (%d ln) · Last refreshed PREPENDED, "
      "#270's demoted to Previous (nothing deleted)" % len(delta.split("\n")))
