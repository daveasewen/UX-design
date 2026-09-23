#!/usr/bin/env python3
"""Lane B #300 — real (count_tokens) cost of each tool family in the conductor's boot.
Reads the key the way knowledge/_gauge_tokens.py::read_key does; never prints it; writes nothing but
notes/_lanes/300/B/real-counts.json. count_tokens is free (platform.claude.com token-counting docs)."""
import json, gzip, os, sys, time, urllib.request, urllib.error
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
HERE = os.path.dirname(os.path.abspath(__file__))
def read_key():
    for name in ("API-KEY.txt", ".env.local"):
        p = os.path.join(REPO, name)
        if not os.path.exists(p): continue
        for line in open(p, encoding="utf-8"):
            s = line.strip().strip('"').strip("'")
            if s.startswith("ANTHROPIC_API_KEY="):
                return s.split("=", 1)[1].strip().strip('"').strip("'")
            if s.startswith("sk-ant-"):   # API-KEY.txt holds a bare key line (read_key() in _gauge_tokens.py misses this form)
                return s
    return None
KEY = read_key()
if not KEY: sys.exit("no key")
def count(model, tools=None, system=None, text="x"):
    body = {"model": model, "messages": [{"role": "user", "content": text}]}
    if tools: body["tools"] = tools
    if system: body["system"] = system
    req = urllib.request.Request("https://api.anthropic.com/v1/messages/count_tokens", data=json.dumps(body).encode(),
        headers={"x-api-key": KEY, "anthropic-version": "2023-06-01", "content-type": "application/json"}, method="POST")
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read())["input_tokens"]
        except urllib.error.HTTPError as e:
            msg = e.read().decode()[:200]
            if e.code in (429, 529, 500): time.sleep(2 + 3*attempt); continue
            raise SystemExit(f"HTTP {e.code}: {msg}")
    raise SystemExit("retries exhausted")
tools = json.load(gzip.open(os.path.join(HERE, "tools-snapshot-300.json.gz")))["tools"]
def fam(n):
    for pre, f in (("mcp__widgets__","widgets"),("mcp__claude_ai__","claude_ai"),("mcp__claude-code-remote__","scheduled(claude-code-remote)"),
                   ("mcp__memory__","memory"),("mcp__remote-devices__","remote-devices")):
        if n.startswith(pre): return f
    if n == "Artifact": return "Artifact"
    if n == "Projects": return "Projects"
    return "core"
M = sys.argv[1] if len(sys.argv) > 1 else "claude-opus-5-5"
res = {"model": M, "when": time.strftime("%Y-%m-%dT%H:%M:%S%z")}
res["base_no_tools"] = count(M)
res["all_68_tools"] = count(M, tools)
fams = sorted(set(fam(t["name"]) for t in tools))
res["marginal_by_family"] = {}
for f in fams:
    rest = [t for t in tools if fam(t["name"]) != f]
    res["marginal_by_family"][f] = res["all_68_tools"] - count(M, rest)
bundles = {
  "chat_search_trio": {"mcp__claude_ai__conversation_search","mcp__claude_ai__read_conversation","mcp__claude_ai__recent_chats"},
  "all_42_loaded_mcp": {t["name"] for t in tools if fam(t["name"]) in ("widgets","claude_ai","scheduled(claude-code-remote)","memory","remote-devices")},
  "research_tool": {"mcp__claude_ai__launch_extended_search_task"},
  "image_search": {"mcp__claude_ai__image_search"},
  "cloud_only_core": {"SendUserFile","SendUserMessage","ShowOnboardingRolePicker","ReadNotifications","RefreshMcpTools","propose_skills","SuggestSkills","ListAgents","ScheduleWakeup","ReportFindings"},
}
res["marginal_bundles"] = {}
for b, names in bundles.items():
    rest = [t for t in tools if t["name"] not in names]
    res["marginal_bundles"][b] = res["all_68_tools"] - count(M, rest)
prose = {}
for f in ("AGENTS.md", "_CHAIN.md"):
    s = open(os.path.join(REPO, f), encoding="utf-8", errors="replace").read()
    prose[f] = count(M, system=s) - res["base_no_tools"]
res["prose_real"] = prose
json.dump(res, open(os.path.join(HERE, f"real-counts-{M}.json"), "w"), indent=1)
print(json.dumps(res, indent=1))
