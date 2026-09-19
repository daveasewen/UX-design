#!/usr/bin/env python3
"""#287 wrap — step 4b: write the FORWARD title into GOOD-MORNING.md, through the mover.

⛔ The line is COPIED OFF `knowledge/_gen_titles_receipt.json`, never retyped: a hand-typed
   title is a claim that the generator produced it, and `title_generation_check()` is BLOCKING.
⛔ The RETROSPECTIVE rename is NEVER written into this file (ruled Dave #28, enacted #30) — it
   is delivered in chat at the wrap.
"""
import json, os, time
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))

rec = json.load(open(os.path.join(ROOT, "knowledge", "_gen_titles_receipt.json"), encoding="utf-8"))
print("receipt keys:", list(rec))
line = rec["next_title"]                       # the generator's own line, verbatim
fwd = line.split("`")[1]                       # the LABEL inside the backticks, never retyped
assert fwd.startswith("Apollo - #288"), repr(fwd)
assert rec["meta"]["declared_session"] == 287 and rec["meta"]["next_session"] == 288

gm = open(os.path.join(ROOT, "GOOD-MORNING.md"), encoding="utf-8").read().split("\n")
old = [l for l in gm if l.startswith("> **TITLE THE NEXT CHAT →**")]
assert len(old) == 1, len(old)
new = "> **TITLE THE NEXT CHAT →** `%s`" % fwd
assert new != old[0]

ops = [{"op": "replace", "file": "GOOD-MORNING.md", "find": [old[0]], "replace": [new]}]
OPSF = os.path.join(HERE, f"ops-287-title-{int(time.time())}.json")
json.dump(ops, open(OPSF, "w", encoding="utf-8"), ensure_ascii=False)
assert os.path.exists(OPSF) and os.path.getsize(OPSF) > 200
print(f"OPS {OPSF}  {os.path.getsize(OPSF):,} B  {len(ops)} ops")
print("  forward title (copied off the receipt):", fwd)
