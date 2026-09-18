#!/usr/bin/env python3
"""#284 wrap — re-read the `s214-D6` chain figure from `_CHAIN.md`'s footer AFTER the
correction pass and the re-taken `size:` stamp, and substitute the stale digits. The #241
clause in action: a wrap that edits its own delta after quoting the chain must quote it again."""
import os, sys
from run_ops import run
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
PAIRS = [("**`_CHAIN.md` regenerates at 9,224 tape** (slice 8,377 + generated wrapper 847), against "
          "#283's **9,324** — **100 SMALLER**",
          "**`_CHAIN.md` regenerates at 9,255 tape** (slice 8,408 + generated wrapper 847), against "
          "#283's **9,324** — **69 SMALLER**"),
         ("at **26.7% of GM's 34,533**", "at **26.6% of GM's 34,845**"),
         ("⚠ **The wrapper is 847 of those 9,224", "⚠ **The wrapper is 847 of those 9,255")]
lines = open(os.path.join(ROOT, "GOOD-MORNING.md"), encoding="utf-8").read().split("\n")
hits = [l for l in lines if PAIRS[0][0] in l]
assert len(hits) == 1, len(hits)
new = hits[0]
for a, b in PAIRS:
    assert a in new, a[:40]
    new = new.replace(a, b)
OPS = [{"op": "replace", "file": "GOOD-MORNING.md", "find": [hits[0]], "replace": [new]}]
if __name__ == "__main__":
    sys.exit(run("s214d6fix", OPS, write="--write" in sys.argv, min_bytes=500))
