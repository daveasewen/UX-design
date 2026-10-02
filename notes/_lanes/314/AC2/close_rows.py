"""#314 lane AC2 - add the borders sha to W-313e1's close (by addition) and close W-313e7 on the SW commit.
Goes through knowledge/_state.py's own load / check / save; no count is hand-edited."""
import os, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "knowledge"))
import _state as S  # noqa: E402

import argparse  # noqa: E402
_ap = argparse.ArgumentParser(description=__doc__)
_ap.add_argument("bd_sha"); _ap.add_argument("sw_sha")
_a = _ap.parse_args()
BD_SHA, SW_SHA = _a.bd_sha, _a.sw_sha
doc = S.load()
by = {i["id"]: i for i in doc["items"]}
e1 = by["W-313e1"]
assert e1["state"] == "done", e1["state"]
add = (" — evidence: commit %s (the borders, committed at the seat 2026-10-02 12:20 UTC by session_018fbsYopetrRuUadc5215i4 "
       "with lane BD's wording); s313-D58 stamped enacted at %s by #314 lane AC2" % (BD_SHA, BD_SHA))
if BD_SHA not in e1["closed_by"]:
    e1["closed_by"] = e1["closed_by"].rstrip() + add
e7 = by["W-313e7"]
if e7["state"] != "done":
    e7["state"] = "done"
    e7["closed_by"] = ("#314 lane SW, landed by lane AC2 in commit %s: switch, checkbox, radio and chip are four metas "
                       "(knowledge/components/{switch,checkbox,radio,chip}.meta.json), each with its own anatomy tree as Dave passed it "
                       "at call 7; selection-controls.meta.json carries the $split record naming the four; coverage gate 0 failures, "
                       "4 family members proven; integrity PASS 142/142. s313-D10 and s313-D56 stamped enacted at %s." % (SW_SHA, SW_SHA))
ok, fails, _ = S.check(doc)
if not ok:
    raise SystemExit("REFUSED by the store gate:\n  " + "\n  ".join(fails[:12]))
S.save(doc)
print("W-313e1 close + evidence %s; W-313e7 closed at %s; store gate OK" % (BD_SHA, SW_SHA))
