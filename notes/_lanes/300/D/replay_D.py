#!/usr/bin/env python3
"""Lane D (#300) replay: the memory-store numbers, from the conductor transcript alone.
Run in the cloud container:  python3 replay_D.py [/root/.claude/projects/-home-claude/<session>.jsonl]
Prints aggregates only (no memory content)."""
import json, sys, hashlib, re, statistics as st
import tiktoken
enc = tiktoken.get_encoding('cl100k_base')
tk = lambda s: len(enc.encode(s, disallowed_special=()))
P = sys.argv[1] if len(sys.argv) > 1 else '/root/.claude/projects/-home-claude/d75f51cc-494a-56b1-9272-190e7fc46cbb.jsonl'
rows = [json.loads(l) for l in open(P) if l.strip()]
# 1. memory snapshots (boot + re-sends)
snaps = [(i, r['attachment']) for i, r in enumerate(rows) if r.get('type') == 'attachment' and r['attachment'].get('type') == 'cowork_memory_context']
for i, a in snaps:
    c = a['content']
    print(f"snapshot row {i}: version {a['version'][:12]} chars {len(c)} cl100k(text) {tk(c)} cl100k(ascii-json) {tk(json.dumps(a))} sha1 {hashlib.sha1(c.encode()).hexdigest()[:12]}")
if len(snaps) > 1:
    print('re-send identical to boot text:', snaps[0][1]['content'] == snaps[1][1]['content'])
L = snaps[0][1]['content'].split('\n')
a0 = L.index('<memory_listing>'); a1 = L.index('</memory_listing>')
entries = [l for l in L[a0 + 2:a1] if l.startswith('/')]
t = [tk(l) for l in entries]
print(f"listing entries {len(entries)} | truncation line: {L[a1-1][:60]!r} | per-line cl100k mean {st.mean(t):.1f} sum {sum(t)}")
# 2. fills per distinct assistant message
seen = set(); fills = []
for r in rows:
    m = r.get('message', {})
    if r.get('type') == 'assistant' and isinstance(m, dict) and m.get('id') not in seen:
        seen.add(m.get('id')); u = m.get('usage', {})
        fills.append(u.get('input_tokens', 0) + u.get('cache_creation_input_tokens', 0) + u.get('cache_read_input_tokens', 0))
print('fills (first 16):', fills[:16])
# 3. memory tool traffic (inputs+results, cl100k)
uses = {}; tin = tout = 0
for r in rows:
    m = r.get('message', {}); c = m.get('content') if isinstance(m, dict) else None
    if not isinstance(c, list): continue
    for b in c:
        if b.get('type') == 'tool_use' and 'mcp__memory__' in b.get('name', ''):
            uses[b['id']] = b['name']; tin += tk(json.dumps(b.get('input'), ensure_ascii=False))
        if b.get('type') == 'tool_result' and b.get('tool_use_id') in uses:
            cc = b.get('content'); s = cc if isinstance(cc, str) else '\n'.join(x.get('text', '') for x in (cc or []) if isinstance(x, dict))
            tout += tk(s)
print(f'memory tool traffic cl100k: inputs {tin} results {tout} total {tin+tout} over {len(uses)} calls')
# 4. memory-attributable boot blocks (system prompt <user_memory>, memory tool schemas, memory MCP instructions)
sp = tl = None
for r in rows:
    if r.get('type') == 'attachment' and r['attachment'].get('type') == 'prompt_snapshot':
        a = r['attachment']; sp = sp or a.get('systemPrompt'); tl = tl or a.get('tools')
txt = '\n'.join((x.get('text', '') if isinstance(x, dict) else str(x)) for x in sp) if isinstance(sp, list) else (sp or '')
if '<user_memory>' in txt:
    print('system prompt <user_memory> block cl100k', tk(txt[txt.index('<user_memory>'):txt.index('</user_memory>') + 14]))
tl = json.loads(tl) if isinstance(tl, str) else (tl or [])
print('memory tool schemas cl100k', sum(tk(json.dumps(x, ensure_ascii=False)) for x in tl if 'mcp__memory__' in x.get('name', '')))
for r in rows:
    if r.get('type') == 'attachment' and r['attachment'].get('type') == 'mcp_instructions_delta':
        for b in r['attachment'].get('addedBlocks', []):
            s = b if isinstance(b, str) else json.dumps(b, ensure_ascii=False)
            if s.lstrip().startswith('## memory'): print('memory MCP instructions block cl100k', tk(s))
