import json,re,collections as C,os
OUT=os.path.dirname(os.path.abspath(__file__))
r=json.load(open(os.path.join(OUT,'live_clustered.json')))
W={'one':1,'two':2,'three':3,'four':4,'five':5,'six':6,'seven':7,'eight':8,'nine':9,'ten':10,'eleven':11,'twelve':12,'thirteen':13,'fourteen':14,'fifteen':15}
ACT=[('release: ratify / cut / cold test', r'ratif|RATIFY|cold test|\bcut\b|bake|Copilot|second machine|pushed the release'),
     ('deck / presentation by eye', r'deck|slide|Friday|brain|callipers|workers|robots|catalogue|books|demo prompt'),
     ('export from a decision page', r'export|pastes|serialised|works the page|worked the'),
     ('look / sign-off by eye', r'\beye\b|seen|looked|opened|watched|render|sign(ed)? off|signs|by eye|viewed|read .* slide'),
     ('ruling-shaped questions on a filed report', r'ruling-shaped|RSQ|questions?|calls?\b|Q\d'),
     ('promote / park an instrument or gate', r'promot|blocking|advisory|wired|park'),
    ]
rows=[x for x in r if x['close'] in('DAVE','DAVE-or-CARRY')]
c=C.Counter(); qn=C.Counter(); by=C.defaultdict(list)
for x in rows:
    cw=x['closes_when']; a='other Dave word'
    for name,rx in ACT:
        if re.search(rx,cw): a=name;break
    x['dave_act']=a; c[(a,x['owner'])]+=1; by[a].append(x)
    n=0
    for m in re.finditer(r"\b(\d+|"+'|'.join(W)+r")\b (?:[a-z\-]+ ){0,3}(?:ruling-shaped|questions|calls|RSQs)",cw,re.I):
        t=m.group(1).lower(); n+=int(t) if t.isdigit() else W[t]
    x['q_count']=n; qn[a]+=n
for a in sorted(by): 
    ages=sorted(x['age_days'] for x in by[a] if x['age_days'] is not None)
    print(f"{a:45s} rows {len(by[a]):4d} (dave {c[(a,'dave')]}, claude {c[(a,'claude')]}) named-question count {qn[a]:4d} median age {ages[len(ages)//2] if ages else '-'}d")
print('rows with a stated question count',sum(1 for x in rows if x['q_count']),'sum',sum(x['q_count'] for x in rows))
old=[x for x in rows if x['age_days'] and x['age_days']>=14]; print('Dave-close rows >=14 days old',len(old),'of',len(rows))
json.dump(rows,open(os.path.join(OUT,'dave_queue.json'),'w'),indent=1)
