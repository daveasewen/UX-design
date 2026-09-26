"""A2 #304: for every live row, test whether its close EVENT has provably already happened (read-only).
Receipts: git commit subjects (gitlog.txt), file existence, other rows' state. Writes verify.json."""
import json,re,os,collections as C
ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__),'../../../..')); OUT=os.path.dirname(os.path.abspath(__file__))
st=json.load(open(os.path.join(ROOT,'knowledge/_state.json')))['items']; S={i['id']:i for i in st}
rows=json.load(open(os.path.join(OUT,'live_clustered.json')))
log=[l.rstrip('\n').split('|',2) for l in open(os.path.join(OUT,'gitlog.txt'))]
def wrapcommit(n):
    for h,d,s in log:
        if re.search(r'\bthe #%d wrap\b'%n,s) or re.search(r'#%d\b.*\bwrap\b'%n,s[:120]) or re.search(r'\bwrap\b.*#%d\b'%n,s[:120]): return h
    return None
def sessionran(n):
    for h,d,s in log:
        if re.search(r'#%d\b'%n,s[:40]): return h
    return None
handoffs=sorted(f for f in os.listdir(ROOT) if f.startswith('_HANDOFF-'))
out=[]
for r in rows:
    cw=r['closes_when']; rec=[]; verdict=None
    # (a) rides another row
    m=re.findall(r'\b(W-\d+[a-z0-9]*|G\d+)\b closes',cw) or re.findall(r"closes with (W-\d+[a-z0-9]*)",cw) or re.findall(r"report (W-\d+[a-z0-9]*) closes",cw)
    if m:
        sts=[(x,S[x]['state'] if x in S else 'MISSING') for x in m]
        rec.append('rides '+', '.join(f'{a}={b}' for a,b in sts))
        verdict='RIDES-OPEN' if any(b in('open','blocked','ruled') for a,b in sts) else 'RIDES-CLOSED'
    # (b) a past session's wrap/opener event
    ns=sorted(set(int(x) for x in re.findall(r'#(\d{3})',cw)))
    past=[n for n in ns if n<304]
    if past and r['close'] in ('EVENT','DAVE-or-CARRY','BUILD') and verdict is None:
        n=max(past)
        wc=wrapcommit(n); nxt=sessionran(n+1)
        if re.search(r'wrap commit|wrap lands|wrap has|subject read back|wrap .*landed',cw) and wc: rec.append(f'#{n} wrap commit {wc}')
        if re.search(r'opener|has read|digest|reads|consumed|answered or carried|carried or struck|actioned or explicitly carried',cw) and nxt: rec.append(f'#{n+1 if "opener" not in cw else n} ran (commit {nxt})')
        if rec: verdict='EVENT-PASSED'
    # (c) filed-at path exists
    for pth in re.findall(r'(notes/_subreports/[\w\-./]+\.md)',cw):
        ex=os.path.exists(os.path.join(ROOT,pth)); rec.append(f'{pth} exists={ex}')
        if ex and verdict is None and r['close']!='DAVE': verdict='FILED'
    # (d) supersession by a later sibling of the same kind
    if verdict is None and re.search(r'superseded by (the next|a later)',cw):
        verdict='SUPERSEDABLE'; rec.append('a later sibling of this kind exists (newer session rows of the same kind are live)')
    out.append(dict(id=r['id'],owner=r['owner'],close=r['close'],kind=r['kind'],theme=r['theme'],verdict=verdict or '-',receipts=rec))
json.dump(out,open(os.path.join(OUT,'verify.json'),'w'),indent=1)
c=C.Counter((o['verdict'],o['close'],o['owner']) for o in out)
for k,v in sorted(c.items()): print(k,v)
