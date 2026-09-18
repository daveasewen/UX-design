#!/usr/bin/env python3
"""#286 wrap — 2d part 2: demote #285's ⏱ LATEST DELTA to PRIOR and insert #286's.

The delta BODY is authored in `lsdelta286.md` and read from disk here, so the text that the
mover writes is the text a human reviewed — never re-typed into a JSON literal.
"""
import json
import os
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
LS = os.path.join(ROOT, "_LIVE-STATE.md")

body = open(os.path.join(HERE, "lsdelta286.md"), encoding="utf-8").read().rstrip("\n").split("\n")
assert body[0].startswith("## ⏱ LATEST DELTA — 2026-09-18 (Fri from `date`) (**#286**"), body[0][:80]
assert len(body) > 15, f"delta body implausibly short: {len(body)} lines"

text = open(LS, encoding="utf-8").read()
heads = [l for l in text.split("\n") if l.startswith("## ⏱ ")]
assert len(heads) == 2, f"expected 2 delta headings after the 2d roll, found {len(heads)}"
LATEST285 = heads[0]
assert "(**#285**" in LATEST285 and LATEST285.startswith("## ⏱ LATEST DELTA"), LATEST285[:90]
assert "(**#284**" in heads[1] and heads[1].startswith("## ⏱ PRIOR DELTA"), heads[1][:90]
assert "(**#286**" not in text, "a #286 delta already exists — refusing to run twice"

PRIOR285 = LATEST285.replace("## ⏱ LATEST DELTA", "## ⏱ PRIOR DELTA", 1)
assert PRIOR285 != LATEST285

ops = [
 {"op": "replace", "file": "_LIVE-STATE.md", "find": [LATEST285], "replace": [PRIOR285]},
 {"op": "insert", "file": "_LIVE-STATE.md", "at": PRIOR285, "where": "before",
  "lines": body + [""]},
]

OPSF = os.path.join(HERE, f"ops-286-lsdelta-{int(time.time())}.json")
json.dump(ops, open(OPSF, "w", encoding="utf-8"), ensure_ascii=False)
assert os.path.exists(OPSF)
sz = os.path.getsize(OPSF)
assert sz > 10_000, f"ops file implausibly small ({sz} B)"
print(f"OPS {OPSF}  {sz:,} B  {len(ops)} ops  · delta body {len(body)} ln")
