#!/usr/bin/env python3
"""attribute_window.py -- #300 lane A: attribute a cloud conductor's context window.

Reads ONE Claude Code transcript (.jsonl) and prints aggregates only (never content):
  1. the boot, itemised: system prompt by section, every loaded tool by family, every
     first-turn attachment -- cl100k TAPE per item and a scaled REAL estimate;
  2. the reconciliation to the measured first-turn fill (usage fields = REAL);
  3. the message-by-message trace: fill, delta, what each step added;
  4. the ratio derivation (tape -> real), from the transcript's own usage fields.

UNITS: real tokens come only from `message.usage` (input + cache_creation + cache_read, per
distinct message.id). Every other figure is cl100k tape (tiktoken) -- an ESTIMATE -- and a
"scaled real" figure is tape x a ratio whose derivation is printed beside it.

Usage (in the cloud container that holds the transcript):
  pip install tiktoken --break-system-packages
  python3 attribute_window.py /root/.claude/projects/-home-claude/<session>.jsonl [--csv OUT_DIR]
The sub-seat transcripts are found at <transcript without .jsonl>/subagents/*.jsonl.
"""
import collections, glob, json, os, re, sys

import tiktoken
ENC = tiktoken.get_encoding("cl100k_base")
def T(s):
    return len(ENC.encode(s or ""))

def load(p):
    return [json.loads(l) for l in open(p)]

def render_tool(t):
    d = {"description": t.get("description", ""), "name": t["name"], "parameters": t.get("schema", {})}
    return "<function>" + json.dumps(d, ensure_ascii=False) + "</function>"

def snapshot_with_tools(rows):
    for r in rows:
        if r.get("type") == "attachment" and r["attachment"].get("type") == "prompt_snapshot" \
                and r["attachment"].get("tools"):
            return r["attachment"]
    return None

def messages(rows):
    seen, out = {}, []
    for i, r in enumerate(rows):
        if r.get("type") != "assistant":
            continue
        m = r["message"]; mid = m.get("id")
        if mid in seen:
            out[seen[mid]]["rows"].append(i); continue
        u = m.get("usage", {})
        seen[mid] = len(out)
        out.append(dict(id=mid, first=i, rows=[i], ts=r.get("timestamp", ""),
                        inp=u.get("input_tokens", 0), cc=u.get("cache_creation_input_tokens", 0),
                        cr=u.get("cache_read_input_tokens", 0), out=u.get("output_tokens", 0)))
    for m in out:
        m["fill"] = m["inp"] + m["cc"] + m["cr"]
    return out

FAMILY_CORE = {"Agent", "AskUserQuestion", "Bash", "Edit", "Glob", "Grep", "ListAgents", "Read",
               "ReadNotifications", "RefreshMcpTools", "ScheduleWakeup", "SendUserFile",
               "SendUserMessage", "Skill", "TaskCreate", "TaskUpdate", "ToolSearch", "WebFetch",
               "WebSearch", "Write", "SubagentHandback"}
def family(name):
    if name in FAMILY_CORE: return "core Claude Code tools"
    if name.startswith("Artifact"): return "Artifact*"
    if name == "Projects": return "Projects"
    for p in ("mcp__widgets__", "mcp__claude_ai__", "mcp__claude-code-remote__", "mcp__memory__",
              "mcp__remote-devices__"):
        if name.startswith(p): return p + "*"
    return "the rest (skills/onboarding/review UI)"

def xml_sections(text, maxdepth=1):
    """(depth, name, tape) for XML-ish sections, depth<=maxdepth."""
    stack, out = [], []
    for m in re.finditer(r"<(/?)([a-z_]+)>", text):
        close, name = m.group(1) == "/", m.group(2)
        if not close:
            stack.append((name, m.start()))
        else:
            for k in range(len(stack) - 1, -1, -1):
                if stack[k][0] == name:
                    st = stack[k][1]; depth = k; del stack[k:]
                    out.append((st, m.end(), name, depth)); break
    out.sort()
    return [(d, n, T(text[s:e]), s, e) for s, e, n, d in out if d <= maxdepth]

def system_sections(sp, cli):
    """Top-level sections of the conductor's 3-block system prompt (+ second level for the big ones)."""
    rows = []
    rows.append(("cliPrefix", 0, T(cli)))
    b0 = sp[0]
    secs = xml_sections(b0, 1)
    covered = 0
    for d, n, t, s, e in secs:
        rows.append((("  " * d) + n, d, t))
        if d == 0: covered += t
    rows.append(("(block 0 text outside tags)", 0, T(b0) - covered))
    rows.append(("Saving skills (block 1)", 0, T(sp[1])))
    b2 = sp[2]
    i_um = b2.find("<user_memory>")
    pre = b2[:i_um] if i_um >= 0 else b2
    heads = [(m.start(), m.group(0)) for m in re.finditer(r"(?m)^# [^\n]+", pre)]
    for k, (st, h) in enumerate(heads):
        en = heads[k + 1][0] if k + 1 < len(heads) else len(pre)
        rows.append((h.lstrip("# ").strip() + " (block 2)", 0, T(pre[st:en])))
    if i_um >= 0:
        rows.append(("<user_memory> guidance (block 2)", 0, T(b2[i_um:])))
    return rows

SR = lambda s: "<system-reminder>\n" + s + "\n</system-reminder>\n"

def render_attachment(a, env_extra):
    t = a.get("type")
    if t == "file":
        f = a["content"]["file"]
        return SR("Called the Read tool with the following input: " + json.dumps({"file_path": f["filePath"]})) + \
               SR("Result of calling the Read tool:\n" + f["content"])
    if t == "environment":
        s = a["snapshot"]
        txt = ("# Environment\nYou have been invoked in the following environment: \n"
               f" - Primary working directory: {s['workingDirectory']}\n - Is a git repository: {str(s['isGitRepo']).lower()}\n"
               f" - Platform: {s['platform']}\n - Shell: {s['shell']}\n - OS Version: {s['osVersion']}\n"
               f" - Scratchpad directory: {s.get('scratchpadDirectory','')} — always use it for temporary files (intermediate results, scripts, outputs that don't belong in the project) instead of `/tmp` or other system temp directories; it is session-specific, isolated from the project, and can generally be used without permission prompts. Only use `/tmp` if the user explicitly asks.\n"
               + env_extra)
        return SR(txt)
    if t == "model":
        return SR(a.get("text", ""))
    if t == "deferred_tools_delta":
        return SR("The following deferred tools are now available via ToolSearch. Their schemas are NOT loaded — calling them directly will fail with InputValidationError. Use ToolSearch with query \"select:<name>[,<name>...]\" to load tool schemas before calling them:\n" + "\n".join(a.get("addedLines", [])))
    if t == "agent_listing_delta":
        s = "Available agent types for the Agent tool:\n" + "\n".join(a.get("addedLines", []))
        if a.get("showConcurrencyNote"):
            s += "\n\nWhen you launch multiple agents for independent work, send them in a single message with multiple tool uses so they run concurrently."
        return SR(s)
    if t == "mcp_instructions_delta":
        return SR("# MCP Server Instructions\n\nThe following MCP servers have provided instructions for how to use their tools and resources:\n\n" + "\n\n".join(a.get("addedBlocks", [])))
    if t == "skill_listing":
        return SR("The following skills are available for use with the Skill tool:\n\n" + a.get("content", ""))
    if t == "total_tokens_reminder":
        return SR(a.get("text", ""))
    if t == "cowork_memory_context":
        return SR(a.get("content") or "")
    if t == "session_context":
        c = a.get("context", {})
        s = "As you answer the user's questions, you can use the following context:\n" + \
            "".join(f"# {k}\n{v}\n" for k, v in c.items()) + \
            "\n\nIMPORTANT: this context may or may not be relevant to your tasks. You should not respond to this context unless it is highly relevant to your task."
        return SR(s)
    if t == "date":
        return SR("Today's date is " + a.get("date", "") + ".")
    if t == "remote_session_change":
        s = ("Attribution for git commits and pull requests you create from here on (this replaces Claude Code's own earlier attribution guidance, such as a previous copy of this reminder; the user's own instructions about these lines, such as a CLAUDE.md or memory rule, take precedence over this reminder, but do not add attribution lines this reminder leaves out):\n"
             "- End git commit messages with:\n" + a.get("commit", "") + "\n- End pull request descriptions with:\n" + a.get("pr", ""))
        return SR(s)
    if t == "command_permissions":
        return ""
    if t == "prompt_snapshot":
        return None
    return SR(json.dumps({k: v for k, v in a.items() if k != "type"}, ensure_ascii=False))

ENV_PROXY = ("\n - Outbound HTTPS goes through a pre-configured agent proxy (CA bundle: /root/.ccr/ca-bundle.crt). If a tool fails TLS verification, gets 403/405/407 from the proxy, or a transfer is cut off (connection reset, unexpected disconnect, RPC failed), see /root/.ccr/README.md and run curl -sS \"$HTTPS_PROXY/__agentproxy/status\" for per-tool fixes and proxy state; never disable TLS verification or unset HTTPS_PROXY.")

def user_text(r):
    c = r["message"]["content"]
    if isinstance(c, str): return c
    parts = []
    for b in c:
        if b.get("type") == "text": parts.append(b["text"])
        elif b.get("type") == "tool_result":
            cc = b.get("content")
            if isinstance(cc, str): parts.append(cc)
            elif isinstance(cc, list):
                parts += [x.get("text", "") for x in cc if isinstance(x, dict)]
    return "\n".join(parts)

SKIP = {"queue-operation", "ai-title", "last-prompt", "atis-latch", "system"}

def between_items(rows, lo, hi):
    """user-side items the model was sent between two assistant messages."""
    items = []
    for i in range(lo + 1, hi):
        r = rows[i]; t = r.get("type")
        if t in SKIP or t == "assistant": continue
        if t == "user":
            txt = user_text(r)
            kind = "user text" if not isinstance(r["message"]["content"], list) or \
                any(b.get("type") == "text" for b in r["message"]["content"]) else "tool result"
            if r.get("isMeta"): kind += " (meta)"
            items.append((i, kind, T(txt)))
        elif t == "attachment":
            s = render_attachment(r["attachment"], ENV_PROXY)
            if s is None: continue
            items.append((i, "att:" + r["attachment"]["type"], T(s)))
    return items

def main():
    p = sys.argv[1]
    outdir = sys.argv[sys.argv.index("--csv") + 1] if "--csv" in sys.argv else None
    rows = load(p)
    snap = snapshot_with_tools(rows)
    sp, tools, cli = snap["systemPrompt"], snap["tools"], snap.get("cliPrefix", "")
    msgs = messages(rows)
    m1 = msgs[0]
    print(f"BOOT (message 1, REAL, usage): {m1['fill']:,} = input {m1['inp']} + cache_creation {m1['cc']:,} + cache_read {m1['cr']:,}")

    # ---- tape of the prefix
    sys_tape = sum(T(b) for b in sp) + T(cli)
    tool_tape = {t["name"]: T(render_tool(t)) for t in tools}
    tools_tape = sum(tool_tape.values())

    # ---- sub-seat solve for the ratios
    subdir = p[:-6] + "/subagents"
    subs = sorted(glob.glob(subdir + "/*.jsonl"))
    sub_prefix, sub_sys, sub_tools = None, None, None
    firsts = []
    for f in subs:
        R = load(f); M = messages(R)
        if not M: continue
        firsts.append(M[0]["cr"])
        if sub_sys is None:
            s2 = snapshot_with_tools(R)
            if s2:
                sub_sys = sum(T(b) for b in s2["systemPrompt"]) + T(s2.get("cliPrefix", ""))
                sub_tools = sum(T(render_tool(t)) for t in s2["tools"])
    nz = [x for x in firsts if x]
    if nz:
        sub_prefix = collections.Counter(nz).most_common(1)[0][0]
    # conductor: tools_tape*rt + sys_tape*rs = m1.cr ; sub: sub_tools*rt + sub_sys*rs = sub_prefix
    if sub_prefix:
        a1, b1, c1 = tools_tape, sys_tape, m1["cr"]
        a2, b2, c2 = sub_tools, sub_sys, sub_prefix
        det = a1 * b2 - a2 * b1
        rt = (c1 * b2 - c2 * b1) / det
        rs = (a1 * c2 - a2 * c1) / det
    else:
        rt, rs = 0.983, 1.453
    # ---- the memory re-send: byte-identical content, measured by difference
    mem_rows = [i for i, r in enumerate(rows) if r.get("type") == "attachment" and r["attachment"].get("type") == "cowork_memory_context" and r["attachment"].get("content")]
    resend = None
    if len(mem_rows) >= 2:
        a0, a1_ = rows[mem_rows[0]]["attachment"], rows[mem_rows[1]]["attachment"]
        k = next(j for j, m in enumerate(msgs) if m["first"] > mem_rows[1])
        items = between_items(rows, msgs[k - 1]["first"], msgs[k]["first"])
        others = sum(t for _, kind, t in items if kind != "att:cowork_memory_context")
        mem_t = T(render_attachment(a1_, ""))
        delta = msgs[k]["fill"] - msgs[k - 1]["fill"]
        mem_real = delta - msgs[k - 1]["out"] - others * rs
        resend = dict(msg=k + 1, delta=delta, prev_out=msgs[k - 1]["out"], other_tape=others,
                      mem_tape=mem_t, mem_real=mem_real, ratio=mem_real / mem_t,
                      identical=(a0["content"] == a1_["content"]), v0=a0["version"][:12], v1=a1_["version"][:12])
    print("\nRATIOS (tape -> real), derived from this transcript's usage fields:")
    print(f"  prefix split solve: conductor cache_read {m1['cr']:,} = tools {tools_tape:,} tape x rt + system {sys_tape:,} tape x rs")
    if sub_prefix:
        print(f"                      sub-seat cache_read {sub_prefix:,} = tools {sub_tools:,} tape x rt + system {sub_sys:,} tape x rs  ({len(subs)} sub transcripts)")
    print(f"  => rt (tool definitions) = {rt:.3f}   rs (prose) = {rs:.3f}")
    if resend:
        print(f"  memory re-send check: message {resend['msg']} delta {resend['delta']:,} - retained prior output {resend['prev_out']:,} - other items {resend['other_tape']} tape x rs"
              f" => snapshot {resend['mem_real']:,.0f} real for {resend['mem_tape']:,} tape = {resend['ratio']:.3f}  (content byte-identical to boot copy: {resend['identical']}; version {resend['v0']} -> {resend['v1']})")

    # ---- boot table
    table = []  # (band, group, item, tape, real_est, basis)
    for name, t in tool_tape.items():
        table.append(("HARNESS", "tool: " + family(name), name, t, t * rt, "rt"))
    for name, d, t in system_sections(sp, cli):
        if d == 0:
            table.append(("HARNESS", "system prompt", name.strip(), t, t * rs, "rs"))
    items = between_items(rows, -1, m1["first"])
    for i, kind, t in items:
        label = kind
        if kind.startswith("user"):
            label = "user turn: " + (rows[i]["message"]["content"][:40] if isinstance(rows[i]["message"]["content"], str) else "Dave's first message + timezone line")
        real = t * rs
        basis = "rs"
        if kind == "att:cowork_memory_context" and resend:
            real = t * resend["ratio"]; basis = "re-send ratio"
        band = "OPENER" if kind in ("att:session_context",) else "HARNESS"
        table.append((band, "first user turn", label, t, real, basis))
    boot_real_est = sum(x[4] for x in table)
    print(f"\nBOOT RECONCILIATION: measured {m1['fill']:,} real")
    grp = collections.OrderedDict()
    for band, g, item, t, r, b in table:
        k = g if not g.startswith("tool: ") else g
        grp.setdefault(k, [0, 0, 0])
        grp[k][0] += t; grp[k][1] += r; grp[k][2] += 1
    for k, (t, r, n) in grp.items():
        print(f"  {k:48s} n={n:3d} tape {t:7,d}  est real {r:9,.0f}")
    print(f"  {'SUM':48s}       tape {sum(x[3] for x in table):7,d}  est real {boot_real_est:9,.0f}")
    print(f"  residual (measured - estimated) = {m1['fill'] - boot_real_est:,.0f} real  ({(m1['fill'] - boot_real_est) / m1['fill'] * 100:.1f}%)")
    pre_est = sum(x[4] for x in table if x[1] != "first user turn")
    turn_est = sum(x[4] for x in table if x[1] == "first user turn")
    print(f"    of which prefix (tools+system): measured cache_read {m1['cr']:,} vs est {pre_est:,.0f}")
    print(f"    of which first user turn:       measured cache_creation+input {m1['cc'] + m1['inp']:,} vs est {turn_est:,.0f}")

    # ---- trace
    print("\nTRACE (REAL fill per distinct message; delta = what entered the window):")
    trace = []
    for k, m in enumerate(msgs):
        lo = msgs[k - 1]["first"] if k else -1
        its = between_items(rows, lo, m["first"])
        prev_out = msgs[k - 1]["out"] if k else 0
        delta = m["fill"] - (msgs[k - 1]["fill"] if k else 0)
        tools_called = []
        for i in m["rows"]:
            for b in rows[i]["message"]["content"]:
                if b.get("type") == "tool_use":
                    tools_called.append(b["name"].replace("mcp__remote-devices__", "rd:").replace("mcp__memory__", "mem:"))
        big = [(kind, t) for _, kind, t in its if t >= 100]
        user_tape = sum(t for _, _, t in its)
        trace.append(dict(n=k + 1, ts=m["ts"][11:19], fill=m["fill"], delta=delta, prev_out=prev_out,
                          user_tape=user_tape, user_real_est=round(user_tape * rs),
                          unexplained=round(delta - prev_out - user_tape * rs), out=m["out"],
                          called=tools_called, big_items=big))
        print(f"  {k + 1:2d} {m['ts'][11:19]} fill {m['fill']:7,d} delta {delta:+7,d} = prior output {prev_out:6,d} + user-side {user_tape:6,d} tape (~{user_tape * rs:7,.0f} real) | residual {delta - prev_out - user_tape * rs:+6,.0f} | then called {','.join(tools_called)}")
    if outdir:
        os.makedirs(outdir, exist_ok=True)
        import csv
        with open(os.path.join(outdir, "boot_items.csv"), "w", newline="") as fh:
            w = csv.writer(fh); w.writerow(["band", "group", "item", "tape_cl100k", "real_est", "ratio_basis"])
            for band, g, item, t, r, b in sorted(table, key=lambda x: -x[4]):
                w.writerow([band, g, item, t, round(r), b])
        json.dump(dict(boot=m1, rt=rt, rs=rs, resend=resend, trace=trace,
                       sub_prefix=sub_prefix, sub_tools_tape=sub_tools, sub_sys_tape=sub_sys,
                       tools_tape=tools_tape, sys_tape=sys_tape),
                  open(os.path.join(outdir, "attribution.json"), "w"), indent=1, default=str)
        print("\nwrote", os.path.join(outdir, "boot_items.csv"), "and attribution.json")

if __name__ == "__main__":
    main()
