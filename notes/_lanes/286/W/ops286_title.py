#!/usr/bin/env python3
"""#286 wrap — step 4b: write the GENERATED forward title into GOOD-MORNING.md, through the mover.

⛔ The line is COPIED from `knowledge/_gen_titles_receipt.json`, never retyped — the receipt is
   the wrap gate's witness that both lines were generated this session.
"""
import json, os, time
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
r = json.load(open(os.path.join(ROOT, "knowledge", "_gen_titles_receipt.json"), encoding="utf-8"))
blob = json.dumps(r)
assert '"286"' in blob or "286" in blob
raw = r.get("next_title") or r.get("next") or r.get("NEXT-TITLE") or ""
# The receipt stores the whole delivered LINE; the title is the backticked span inside it.
import re as _re
m = _re.search(r"`(Apollo - #287[^`]*)`", raw) or _re.search(r"`(Apollo - #287[^`]*)`", blob)
assert m, raw or blob[:400]
nxt = m.group(1)
gm = open(os.path.join(ROOT, "GOOD-MORNING.md"), encoding="utf-8").read().split("\n")
cur = [l for l in gm if l.startswith("> **TITLE THE NEXT CHAT →**")]
assert len(cur) == 1, len(cur)
NEW = f"> **TITLE THE NEXT CHAT →** `{nxt}`"
assert NEW != cur[0], "title unchanged — a no-op is a lookup that failed"
ops = [{"op": "replace", "file": "GOOD-MORNING.md", "find": [cur[0]], "replace": [NEW]}]
OPSF = os.path.join(HERE, f"ops-286-title-{int(time.time())}.json")
json.dump(ops, open(OPSF, "w", encoding="utf-8"), ensure_ascii=False)
assert os.path.exists(OPSF) and os.path.getsize(OPSF) > 200
print(f"OPS {OPSF}  {os.path.getsize(OPSF):,} B · NEXT → {nxt}")
