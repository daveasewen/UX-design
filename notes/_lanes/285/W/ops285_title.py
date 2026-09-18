#!/usr/bin/env python3
"""#285 wrap — step 4b: the FORWARD title into `GOOD-MORNING.md`, GENERATED not hand-written.

`python3 knowledge/_gen_titles.py --session 285` produced both lines and wrote its receipt to
`knowledge/_gen_titles_receipt.json`; `title_generation_check()` is BLOCKING and reads that
receipt. ⛔ The RENAME line is delivered IN CHAT and is NEVER written into this file (RULED #28,
enacted #30) — only the forward title goes here.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, HERE)
from run_ops import run

r = json.load(open(os.path.join(ROOT, "knowledge", "_gen_titles_receipt.json"), encoding="utf-8"))
nxt = r["next_title"]
assert nxt.startswith("NEXT SESSION TITLE → `") and nxt.endswith("`"), nxt
target = nxt[len("NEXT SESSION TITLE → `"):-1]
assert target.startswith("Apollo - #286:"), target

old = [l.rstrip("\n") for l in open(os.path.join(ROOT, "GOOD-MORNING.md"), encoding="utf-8")
       if l.startswith("> **TITLE THE NEXT CHAT →**")]
assert len(old) == 1, len(old)
new = f"> **TITLE THE NEXT CHAT →** `{target}`"
assert new != old[0], "REFUSED — identical, a lookup that failed while reading as success"
print("GENERATED:", target)

ops = [{"op": "replace", "file": "GOOD-MORNING.md", "find": [old[0]], "replace": [new]}]
sys.exit(run("title", ops, write="--write" in sys.argv, min_bytes=150))
