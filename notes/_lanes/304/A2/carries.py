import json,re,collections as C,os
OUT=os.path.dirname(os.path.abspath(__file__))
it=json.load(open(os.path.join(OUT,'carries304.json')))
cls=C.Counter(); ex=C.defaultdict(list); rows=[]
SER=[('CI read-back owed (s203-D1)',r'CI READ-BACK|READ-BACK IS OWED|OWED CI VERDICT|VERDICT IS OWED|CI read-back'),
     ('boot-ceiling / boot breach reading',r'BOOT[^*]{0,40}(BREACH|CEILING|MEASURED|\d\d,\d\d\d)|CEILING ARM|BOOT DRIFT'),
     ('fill / window over a line',r'FILL|WALL|STOP LINE|ADVISORY|WINDOW CLOSED|256K|300K|190K|200,000'),
     ('memory unwritten / hook owed',r'MEMORY (WENT|HAS|WAS)|MEMORY HOOK|MEMORY SHARD|MEMORY\.md|RITUAL STEP 3|CLOUD MEMORY'),
     ('push / local commits unpushed',r'THE PUSH|UNPUSHED|LOCAL COMMITS'),
     ('recall probe not planted',r'RECALL PROBE'),
     ('index.lock / mount warts',r'index\.lock|LOCK|unlink|MOUNT|\.DS_Store|_to_delete'),
     ('boilerplate: what this wrap did not do / pitfalls',r'WHAT (THIS|THE #\d+) WRAP DID NOT DO|CONSEQUENCES AND PITFALLS'),
    ]
for age,t in it:
    head=(re.search(r'\*\*(.+?)\*\*',t) or re.search(r'(.{0,160})',t)).group(1)
    h=t[:600]
    k=None
    if not re.match(r'\s*[⬛⚠▫⛔✅⚙~]',t): k='fragment (splitter artefact)'
    elif re.match(r'\s*\S?\s*~~',t) or '~~' in head.strip()[:6] or re.match(r'\s*[⬛⚠▫⛔]\s*~~',t) or re.search(r'⛔ STRUCK|STRUCK AT #|STRUCK BY',h): k='struck but still carried'
    else:
        for name,rx in SER:
            if re.search(rx,head): k='series: '+name; break
    if not k and re.search(r'deck|slide|FRIDAY|Friday|BRAIN|CALLIPERS|WORKERS|CATALOGUE|PLATE|DEMO|PRESENTATION|THE ASK|RUN-OF-SHOW|DRAWING|PROPOSAL v3|ROBOT',head): k='deck / Friday / demo (event now past)'
    if not k: k='substantive'
    dav="DAVE'S" in h
    cls[k]+=1; ex[k].append((age,head[:110])); rows.append(dict(age=age,cls=k,dave=dav,head=head[:200]))
tot=len(it)
for k,v in cls.most_common(): 
    ages=sorted(a for a,_ in ex[k]); print(f"{k:55s} {v:4d}  ({100*v/tot:4.1f}%)  median age {ages[len(ages)//2]} wraps  dave-tagged {sum(1 for r in rows if r['cls']==k and r['dave'])}")
json.dump(rows,open(os.path.join(OUT,'carries_classified.json'),'w'),indent=1)
print('\nsubstantive by age:',C.Counter(('0-7' if r['age']<=7 else '8-30' if r['age']<=30 else '31-60' if r['age']<=60 else '61+') for r in rows if r['cls']=='substantive'))
print('\nsample substantive >60:'); [print('  ',a,h) for a,h in ex['substantive'] if a>60][:0]

