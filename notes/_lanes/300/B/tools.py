import json, sys, collections, tiktoken
enc = tiktoken.get_encoding("cl100k_base")
def tk(s): return len(enc.encode(s, disallowed_special=()))
p = sys.argv[1]
lines = open(p).read().splitlines()
snap = None
for l in lines:
    d = json.loads(l)
    if d.get("type") == "attachment" and d["attachment"].get("type") == "prompt_snapshot" and "tools" in d["attachment"]:
        snap = d["attachment"]
def fam(n):
    if n.startswith("mcp__widgets__"): return "mcp__widgets__*"
    if n.startswith("mcp__claude_ai__"): return "mcp__claude_ai__*"
    if n.startswith("mcp__claude-code-remote__"): return "mcp__claude-code-remote__*"
    if n.startswith("mcp__memory__"): return "mcp__memory__*"
    if n.startswith("mcp__remote-devices__"): return "mcp__remote-devices__*"
    if n.startswith("mcp__visualize__"): return "mcp__visualize__*"
    if n.startswith("mcp__claude-in-chrome__"): return "mcp__claude-in-chrome__*"
    if n.startswith("Artifact"): return "Artifact*"
    if n == "Projects": return "Projects"
    if n.startswith("mcp__"): return "mcp-other"
    return "core"
rows = []
for t in snap["tools"]:
    ser = json.dumps({"name": t["name"], "description": t["description"], "input_schema": t["schema"]})
    rows.append((t["name"], fam(t["name"]), len(ser), tk(ser), tk(t["description"]), tk(json.dumps(t["schema"]))))
tot = sum(r[3] for r in rows)
print("TOTAL tools", len(rows), "chars", sum(r[2] for r in rows), "cl100k", tot)
g = collections.defaultdict(lambda: [0,0,[]])
for r in rows:
    g[r[1]][0] += r[3]; g[r[1]][1] += 1; g[r[1]][2].append(r[0])
for k, v in sorted(g.items(), key=lambda x: -x[1][0]):
    print(f"FAM {k:32s} n={v[1]:3d} cl100k={v[0]:7d}")
print("--- per tool (name, family, chars, cl100k total, desc, schema)")
for r in sorted(rows, key=lambda x: -x[3]):
    print(f"{r[0]:55s} {r[1]:28s} {r[2]:7d} {r[3]:6d} {r[4]:6d} {r[5]:6d}")
sp = snap["systemPrompt"]
print("systemPrompt parts cl100k", [tk(x) for x in sp], "sum", sum(tk(x) for x in sp))
print("cliPrefix", repr(snap.get("cliPrefix")))
