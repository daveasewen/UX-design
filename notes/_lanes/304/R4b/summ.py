import json,sys,collections
d=json.load(open(sys.argv[1])); d=d if isinstance(d,list) else [d]
n=int(sys.argv[2]) if len(sys.argv)>2 else 3
for r in d:
    print("==",r['page'],r['verdict'],'score',r['score'],r['runtime_ms'],'ms', {k:v for k,v in r['counts'].items() if v})
    seen=collections.Counter()
    for f in r['findings']:
        k=(f['clause'],f['width']); seen[k]+=1
        if seen[k]<=n: print('  ',f['clause'],f['width'],'|',f['where'][:80],'|',f['measured'][:140])
