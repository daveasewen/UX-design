#!/usr/bin/env python3
"""#284 wrap — FIFTH compression pass; 1,203 → under the 1,200 cap. Girth only."""
import sys
from run_ops import run
OPS = [
 {"op": "replace", "file": "GOOD-MORNING.md",
  "find": ["> - ⛔★★ ③ **THE DISK LEVER #283 SAID DID NOT EXIST.** `_HANDOFF-134`'s *\"NOT fixable from his Mac\"* is **RETRACTED**: the VM is a bundle on his Mac; he trashed `claudevm.bundle` (keeping `warm`), **`/sessions` 98.7% → 0.1%**, 127 dead homes gone. ★ **The session SURVIVED the rebuild**; the file said it would not. **A finding + an act, not a ruling.** Carry STRUCK, receipted."],
  "replace": ["> - ⛔★★ ③ **THE DISK LEVER #283 SAID DID NOT EXIST.** `_HANDOFF-134`'s *\"NOT fixable from his Mac\"* is **RETRACTED**: the VM is a bundle on his Mac; he trashed `claudevm.bundle` (keeping `warm`), **`/sessions` 98.7% → 0.1%**, 127 dead homes gone. ★ **The session SURVIVED the rebuild**; the file said it would not. **A finding + an act, not a ruling.** Carry STRUCK + receipted."]},
 {"op": "replace", "file": "GOOD-MORNING.md",
  "find": ["> - ⬛★★ ⑤ **THE DELEGATION LAPSE, HIS WORDS:** *\"everything is Delegated … the lane is always an orchestrator and judgment layer … this seems to have been lost\"* (#57 / `s204-D1`). In-seat lane work ×4 — disk+spec ~15K · **six commit runs ~30K** · 2 screenshots · research — **only the drawing was a lane**; ★ **the lane cost the window ~300 tokens.** Fix PROPOSED, NOT BUILT."],
  "replace": ["> - ⬛★★ ⑤ **THE DELEGATION LAPSE, HIS WORDS:** *\"everything is Delegated … the lane is always an orchestrator and judgment layer … this seems to have been lost\"* (#57 / `s204-D1`). In-seat lane work ×4: disk+spec ~15K · **six commit runs ~30K** · 2 screenshots · research — **only the drawing was a lane**; ★ **the lane cost ~300 tokens.** Fix PROPOSED, NOT BUILT."]},
]
if __name__ == "__main__":
    sys.exit(run("bannertrim2", OPS, write="--write" in sys.argv, min_bytes=100))
