#!/usr/bin/env python3
"""#291 wrap — step 4b: write the FORWARD title into GOOD-MORNING.md through the mover,
COPIED out of `knowledge/_gen_titles_receipt.json` rather than retyped."""
import json, os, time
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
GM = os.path.join(ROOT, "GOOD-MORNING.md")
r = json.load(open(os.path.join(ROOT, "knowledge", "_gen_titles_receipt.json"), encoding="utf-8"))
print(json.dumps(r)[:400])
import re
nxt = re.search(r"`(.+)`", r["next_title"]).group(1)
assert nxt and "#292" in nxt, nxt
gm = open(GM, encoding="utf-8").read().split("\n")
cur = [l for l in gm if l.startswith("> **TITLE THE NEXT CHAT →**")]
assert len(cur) == 1, cur
new = "> **TITLE THE NEXT CHAT →** `%s`" % nxt
ops = [{"op": "replace", "file": "GOOD-MORNING.md", "find": [cur[0]], "replace": [new]}]
out = os.path.join(HERE, f"ops-291-title-{int(time.time())}.json")
json.dump(ops, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
assert os.path.exists(out) and os.path.getsize(out) > 200
print(f"WROTE {out}  {os.path.getsize(out):,} B  1 op\n  {new}")
