#!/usr/bin/env python3
"""X #300 — container-side replay of the adversary's transcript checks (read-only; prints aggregates).
Run in the CLOUD CONTAINER (the transcript lives there): python3 x_replay.py [<session>.jsonl]
 1  thinking retained across a USER turn: cache_read at the first message after a human turn equals
    the previous message's full input (if earlier turns' thinking were stripped, the cached prefix
    would break at msg 1's thinking, ~126K)
 2  the memory re-send: identical bytes, new version
 3  the interrupt (uVpTXJ->QwntDv): the prefix broke and the fill FELL while a turn was added
 4  thinking visible in the transcript vs output_tokens billed"""
import json,sys,hashlib
P=sys.argv[1] if len(sys.argv)>1 else '/root/.claude/projects/-home-claude/d75f51cc-494a-56b1-9272-190e7fc46cbb.jsonl'
R=[json.loads(l) for l in open(P)]
msgs=[];seen=set()
for i,r in enumerate(R):
    if r.get('type')=='assistant':
        m=r['message'];u=m['usage']
        if m['id'] in seen: continue
        seen.add(m['id'])
        msgs.append(dict(row=i,id=m['id'][-6:],fill=u['input_tokens']+u['cache_creation_input_tokens']+u['cache_read_input_tokens'],
                         cr=u['cache_read_input_tokens'],cc=u['cache_creation_input_tokens'],out=u['output_tokens']))
def human_turn_between(a,b):
    # a human message carries the harness's timezone reminder ("The user's timezone is ...")
    for r in R[a+1:b]:
        if r.get('type')=='user' and "The user's timezone is" in json.dumps(r['message'].get('content')): return True
    return False
print('== 1+3  boundaries (first message after a human turn)')
for p,q in zip(msgs,msgs[1:]):
    if human_turn_between(p['row'],q['row']):
        print(f"  {p['id']}->{q['id']}  prev fill {p['fill']:,} prev out {p['out']:,} | next cache_read {q['cr']:,} (prefix kept: {q['cr']>=p['fill']-2}) cc {q['cc']:,} next fill {q['fill']:,} (delta {q['fill']-p['fill']:+,})")
print('== 2  memory snapshots')
snaps=[(i,r['attachment']) for i,r in enumerate(R) if r.get('type')=='attachment' and r['attachment'].get('type')=='cowork_memory_context']
for i,a in snaps: print(f"  row {i} version {a['version'][:12]} sha256 {hashlib.sha256((a.get('content') or '').encode()).hexdigest()[:16]} chars {len(a.get('content') or '')}")
print('== 4  thinking visible vs billed')
vis=0
for r in R:
    if r.get('type')=='assistant':
        for c in r['message']['content']:
            if c['type']=='thinking': vis+=len(c.get('thinking',''))
print(f"  output_tokens billed (distinct msgs) {sum(m['out'] for m in msgs):,} · thinking text visible in transcript {vis:,} chars")
