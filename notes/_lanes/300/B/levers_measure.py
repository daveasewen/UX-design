#!/usr/bin/env python3
"""Lane B #300 — lever sizes from the conductor's own boot payload (prompt_snapshot + attachments).
Usage: python3 levers_measure.py [conductor.jsonl] [subagent.jsonl]
Prints tape (cl100k) and real (scaled) per lever. Scale = two-register fit on two measured boots
(conductor msg 1, a lane sub's msg 1), validated on the #300 memory re-send (+23,591 real)."""
import json, re, sys, tiktoken
enc = tiktoken.get_encoding("cl100k_base")
tk = lambda s: len(enc.encode(s, disallowed_special=()))
C = sys.argv[1] if len(sys.argv) > 1 else '/root/.claude/projects/-home-claude/d75f51cc-494a-56b1-9272-190e7fc46cbb.jsonl'
S = sys.argv[2] if len(sys.argv) > 2 else '/root/.claude/projects/-home-claude/d75f51cc-494a-56b1-9272-190e7fc46cbb/subagents/agent-a15bc00f2eaf18c75.jsonl'
def render(a):
    t = a["type"]
    if t == "deferred_tools_delta": return "\n".join(a["addedLines"]) + "\n" + "x " * 60
    if t == "skill_listing": return a["content"]
    if t == "session_context": return a["context"] if isinstance(a["context"], str) else json.dumps(a["context"])
    if t == "agent_listing_delta": return "\n".join(a["addedLines"])
    if t == "mcp_instructions_delta": return "\n\n".join(a["addedBlocks"])
    if t == "environment": return a["snapshot"] if isinstance(a["snapshot"], str) else json.dumps(a["snapshot"])
    if t == "model": return a.get("text", "")
    if t == "file": return a.get("content", "") if isinstance(a.get("content"), str) else json.dumps(a.get("content"))
    if t == "cowork_memory_context": return a["content"] if isinstance(a["content"], str) else json.dumps(a["content"])
    return json.dumps({k: v for k, v in a.items() if k != "type"})
def load(p):
    L = [json.loads(l) for l in open(p)]
    snap = [d["attachment"] for d in L if d.get("type") == "attachment" and d["attachment"]["type"] == "prompt_snapshot" and "tools" in d["attachment"]][0]
    return L, snap
def boot(p):
    L, snap = load(p)
    tools = {x["name"]: tk(json.dumps({"name": x["name"], "description": x["description"], "input_schema": x["schema"]})) for x in snap["tools"]}
    prose = {"systemPrompt": sum(tk(x) for x in snap["systemPrompt"])}
    for d in L:
        t = d.get("type")
        if t == "assistant":
            u = d["message"]["usage"]; real = u["input_tokens"] + u["cache_creation_input_tokens"] + u["cache_read_input_tokens"]; break
        if t == "attachment" and d["attachment"]["type"] != "prompt_snapshot":
            a = d["attachment"]; prose[a["type"]] = prose.get(a["type"], 0) + tk(render(a))
        if t == "user":
            c = d["message"]["content"]; s = c if isinstance(c, str) else " ".join(b.get("text", "") for b in c if isinstance(b, dict))
            prose["user"] = prose.get("user", 0) + tk(s)
    return real, tools, prose, L, snap
r1, t1, p1, _, _ = boot(S); r2, t2, p2, L, snap = boot(C)
T1, P1, T2, P2 = sum(t1.values()), sum(p1.values()), sum(t2.values()), sum(p2.values())
det = T1 * P2 - T2 * P1; A = (r1 * P2 - r2 * P1) / det; B = (T1 * r2 - T2 * r1) / det
print(f"BOOTS  sub real {r1:,} = tools {T1:,} + prose {P1:,} tape | conductor real {r2:,} = tools {T2:,} + prose {P2:,} tape")
print(f"SCALE  tools x{A:.3f} real/cl100k · prose x{B:.3f} real/cl100k (two-point fit)")
mem = [d["attachment"] for d in L if d.get("type") == "attachment" and d["attachment"]["type"] == "cowork_memory_context"]
rs_tape = 1882 + 234 + 17 + tk(render(mem[1]))
print(f"CHECK  re-send tape {rs_tape:,} -> predicted {rs_tape*B:,.0f} real vs measured 23,591 ({rs_tape*B/23591:.3f})")
sp0, sp1, sp2 = snap["systemPrompt"]
def tag(name):
    m = re.search(r'<%s>.*?</%s>' % (name, name), sp0, re.S); return tk(m.group(0)) if m else 0
def between(s, a, b=None):
    i = s.find(a); j = s.find(b, i + 1) if b else len(s)
    return tk(s[i:(j if j > 0 else len(s))]) if i >= 0 else 0
att = {d["attachment"]["type"]: d["attachment"] for d in L[:40] if d.get("type") == "attachment"}
dl = att["deferred_tools_delta"]["addedLines"]
def dnames(pred): return tk("\n".join(n for n in dl if pred(n)))
mcpi = dict(zip(att["mcp_instructions_delta"]["addedNames"], [tk(b) for b in att["mcp_instructions_delta"]["addedBlocks"]]))
skills = {}
for it in re.split(r'(?m)^- ', att["skill_listing"]["content"])[1:]:
    head = it.split(":", 2); nm = ":".join(head[:2]) if head[0] in ("anthropic-skills", "cowork-plugin-management") else head[0]
    skills[nm.strip()] = tk("- " + it)
def tsum(pred): return sum(v for k, v in t2.items() if pred(k))
F = lambda pre: (lambda k: k.startswith(pre))
levers = [
 ("Pause memory (Settings > Memory)", tsum(F("mcp__memory__")), between(sp2, "<user_memory>") + p2["cowork_memory_context"] + mcpi.get("memory", 0) + dnames(F("mcp__memory__"))),
 ("Chat search off (Settings > Memory)", sum(t2[k] for k in ("mcp__claude_ai__conversation_search", "mcp__claude_ai__read_conversation", "mcp__claude_ai__recent_chats")), 0),
 ("Computer use off (desktop Settings > General)", 0, dnames(lambda n: "remote-devices__computer_" in n) + tag("desktop_computer_use") + skills.get("anthropic-skills:computer-use", 0)),
 ("Claude in Chrome off (Settings > Connectors)", 0, dnames(F("mcp__claude-in-chrome__")) + between(sp2, "# Claude in Chrome browser automation", "# Your current remote execution environment") + mcpi.get("claude-in-chrome", 0) + skills.get("claude-in-chrome", 0) + skills.get("anthropic-skills:chrome-browser", 0)),
 ("Built-in browser (no off switch found)", 0, dnames(lambda n: "Claude_Browser" in n) + tag("browsers") + skills.get("anthropic-skills:built-in-browser", 0)),
 ("Tool access = On demand, upper bound (42 loaded MCP)", tsum(lambda k: k.startswith("mcp__")) , -42 * 14),
 ("  of which widgets family", tsum(F("mcp__widgets__")), -17 * 14),
 ("Artifacts (no Pro/Max switch; CC: enableArtifact=false)", t2.get("Artifact", 0), tag("artifacts") + sum(skills.get(k, 0) for k in ("artifact-design", "artifact-diagramming", "artifact-capabilities"))),
 ("Scheduled tasks (no switch found)", tsum(F("mcp__claude-code-remote__")), tag("scheduled_tasks")),
 ("Research tool (per-chat; schema always loaded)", t2.get("mcp__claude_ai__launch_extended_search_task", 0), 0),
 ("Computer link (only if repo leaves the Mac)", tsum(F("mcp__remote-devices__")), tag("device_bridge") + between(sp2, "## Working with the user's computer", "# Model identity") + tag("where_files_live") + dnames(lambda n: n == "mcp__remote-devices__get_device_info")),
 ("Leave the Project (Projects tool + instructions)", t2.get("Projects", 0), p2.get("session_context", 0)),
 ("Skills: browser/computer/chrome entries", 0, sum(skills.get(k, 0) for k in ("anthropic-skills:built-in-browser", "anthropic-skills:chrome-browser", "anthropic-skills:computer-use", "claude-in-chrome"))),
 ("Skills: office four (docx/pptx/xlsx/pdf) - NOT advised", 0, sum(skills.get("anthropic-skills:" + k, 0) for k in ("docx", "pptx", "xlsx", "pdf"))),
 ("Plugin cowork-plugin-management (2 skills)", 0, sum(v for k, v in skills.items() if k.startswith("cowork-plugin-management"))),
 ("Third-party connectors present at boot", 0, 0),
]
print(f"\n{'lever':58s} {'tools':>7s} {'prose':>7s} {'tape':>7s} {'REAL':>7s}")
for name, tt, pp in levers:
    print(f"{name:58s} {tt:7,d} {pp:7,d} {tt+pp:7,d} {tt*A+pp*B:7,.0f}")
print("\nfamilies (tape):", {f: sum(v for k, v in t2.items() if k.startswith(f)) for f in ("mcp__widgets__", "mcp__remote-devices__", "mcp__claude-code-remote__", "mcp__memory__", "mcp__claude_ai__")}, "Artifact", t2.get("Artifact"), "Projects", t2.get("Projects"))
print("core tools (tape):", sum(v for k, v in t2.items() if not k.startswith("mcp__") and k not in ("Artifact", "Projects")))
