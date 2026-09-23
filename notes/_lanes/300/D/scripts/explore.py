import json, collections
P='/root/.claude/projects/-home-claude/d75f51cc-494a-56b1-9272-190e7fc46cbb.jsonl'
types=collections.Counter(); att=collections.Counter(); keys=collections.Counter()
rows=[]
with open(P) as f:
    for i,line in enumerate(f):
        try: d=json.loads(line)
        except Exception as e: print('bad',i); continue
        types[d.get('type')]+=1
        for k in d.keys(): keys[k]+=1
        if d.get('type')=='attachment':
            a=d.get('attachment',{})
            att[a.get('type')]+=1
            if a.get('type')=='cowork_memory_context':
                rows.append((i, list(a.keys()), len(json.dumps(a)), d.get('timestamp'), d.get('parentUuid'), d.get('uuid')))
print('types',types.most_common())
print('keys',keys.most_common(40))
print('att',att.most_common())
for r in rows: print(r)
