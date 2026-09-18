#!/usr/bin/env python3
"""#286 lane W — the s218-D7 stub contract, MEASURED.

What did the nine lane replies cost the conductor's WINDOW? Each lane's reply
arrives in the conductor's transcript as a tool_result for its Agent/Task call.
Measured in cl100k (tiktoken) — the same unit #285 published, so the two are
comparable. ⛔ cl100k is a PROXY, never converted into a real-token claim.
"""
import json
import os
import sys

import tiktoken

CONDUCTOR = ("/sessions/nifty-eager-euler/mnt/.claude/projects/session/"
             "f00a81c6-812c-4fb9-b2e1-90eec24a3c47.jsonl")
assert os.path.exists(CONDUCTOR) and os.path.getsize(CONDUCTOR) > 10_000

enc = tiktoken.get_encoding("cl100k_base")

# Pass 1: find every Agent/Task tool_use id the conductor issued, with its depth.
spawns = {}          # tool_use id -> {"name","desc","model"}
for line in open(CONDUCTOR, encoding="utf-8"):
    line = line.strip()
    if not line:
        continue
    try:
        rec = json.loads(line)
    except json.JSONDecodeError:
        continue
    msg = rec.get("message") or {}
    for blk in (msg.get("content") or []):
        if not isinstance(blk, dict) or blk.get("type") != "tool_use":
            continue
        if blk.get("name") not in ("Agent", "Task"):
            continue
        inp = blk.get("input") or {}
        spawns[blk["id"]] = {"desc": inp.get("description", ""),
                             "subagent_type": inp.get("subagent_type", ""),
                             "model": inp.get("model", "(inherit)"),
                             "prompt_tk": len(enc.encode(inp.get("prompt", ""))),
                             "spawn_depth": rec.get("spawnDepth", rec.get("isSidechain")),
                             "tool": blk.get("name")}

# Pass 2: match each reply back to its call.
replies = {}
for line in open(CONDUCTOR, encoding="utf-8"):
    line = line.strip()
    if not line:
        continue
    try:
        rec = json.loads(line)
    except json.JSONDecodeError:
        continue
    msg = rec.get("message") or {}
    for blk in (msg.get("content") or []):
        if not isinstance(blk, dict) or blk.get("type") != "tool_result":
            continue
        tid = blk.get("tool_use_id")
        if tid not in spawns:
            continue
        c = blk.get("content")
        if isinstance(c, list):
            text = "".join(p.get("text", "") for p in c if isinstance(p, dict))
        else:
            text = str(c)
        replies[tid] = len(enc.encode(text))

rows = []
for tid, s in spawns.items():
    rows.append({**s, "reply_cl100k": replies.get(tid), "id": tid[-8:]})
rows.sort(key=lambda r: (r["reply_cl100k"] is None, -(r["reply_cl100k"] or 0)))

total = sum(r["reply_cl100k"] or 0 for r in rows)
print(json.dumps({"spawns": len(rows),
                  "replies_measured": sum(1 for r in rows if r["reply_cl100k"] is not None),
                  "total_reply_cl100k": total,
                  "total_prompt_cl100k": sum(r["prompt_tk"] for r in rows),
                  "rows": rows}, indent=1))
