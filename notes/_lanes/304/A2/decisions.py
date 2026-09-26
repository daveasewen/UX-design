import json,re,os,collections as C
OUT=os.path.dirname(os.path.abspath(__file__))
r=json.load(open(os.path.join(OUT,'live_clustered.json'))); v={x['id']:x for x in json.load(open(os.path.join(OUT,'verify.json')))}
dq={x['id']:x for x in json.load(open(os.path.join(OUT,'dave_queue.json')))}
S=lambda f:[x for x in r if f(x)]
deckrx=r"deck|slide|Friday|\bthe brain\b|brain at|brain's|callipers|workers|robots|catalogue|books|press loop|demo prompt|the ask|v1[0-4]\b|proposal v3|arm is placed|run-of-show"
D={}
D['D1 deck finished']=S(lambda x: x['theme'].startswith('T1') or re.search(deckrx,x['closes_when']))
D['D2 park stale ruling-shaped questions (>=14d)']=S(lambda x: x['id'] in dq and dq[x['id']]['dave_act']=='ruling-shaped questions on a filed report' and (x['age_days'] or 0)>=14 and x not in D['D1 deck finished'])
rel=[]
for x in r:
    t=x['title']+' '+x['closes_when']; vs=[int(a) for a in re.findall(r'v1\.0\.(\d+)',t)]
    if vs and max(vs)<=12 and re.search(r'ratif|cut|bake|cold test|release|re-stage|re-cut|Copilot',x['closes_when'],re.I): rel.append(x)
D['D3 releases up to v1.0.12 superseded by v1.0.13; cut v1.0.14']=rel
D['D4 window and boot lines']=S(lambda x: re.search(r'boot|ceiling|256|300,000|stop line|tolerance|window|FILL|conditional-band',x['title']+' '+x['closes_when'],re.I) and x['owner']=='dave')
D['D5 the 14 legacy rows']=S(lambda x: x['close']=='UNCONDITIONED')
D['D6 Layer-2 / component waves proposed-not-ruled']=S(lambda x: x['id'] in ('W-63','W-71','W-72','W-73','W-74','W-62','W-86','W-99i','W-99zc','W-170','W-510','W-66'))
D['D7 Dave-owned rows whose close event has passed']=S(lambda x: v[x['id']]['verdict'] in('EVENT-PASSED','FILED') and x['owner']=='dave')
D['D8 export pages never returned']=S(lambda x: x['id'] in dq and dq[x['id']]['dave_act']=='export from a decision page')
seen=set(); tot=0
for k,L in D.items():
    ids=[x['id'] for x in L]; new=[i for i in ids if i not in seen]; seen|=set(ids)
    print(f"{k:60s} rows {len(ids):4d}  new (not counted above) {len(new):4d}")
print('union',len(seen),'of',len(r))
json.dump({k:[x['id'] for x in L] for k,L in D.items()},open(os.path.join(OUT,'decision_unblocks.json'),'w'),indent=1)
# autonomous close candidates
auto=[dict(id=x['id'],owner=x['owner'],verdict=v[x['id']]['verdict'],receipts=v[x['id']]['receipts'],closes_when=x['closes_when'][:200]) for x in r if v[x['id']]['verdict'] in('EVENT-PASSED','FILED') and x['owner']=='claude']
json.dump(auto,open(os.path.join(OUT,'autonomous_close_candidates.json'),'w'),indent=1)
print('autonomous close candidates (claude-owned, event passed with receipt):',len(auto))
