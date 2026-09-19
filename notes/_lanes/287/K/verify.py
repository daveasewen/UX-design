import json,re,sys,os
def kg(p):
    h=open(p,encoding='utf-8').read()
    m=re.search(r'<script[^>]*id="kg"[^>]*>(.*?)</script>', h, re.S)
    return json.loads(m.group(1).replace('<\\/script','</script'))
A=kg('notes/_lanes/287/K/before-_KG-EXPLORER.html'); B=kg('notes/_KG-EXPLORER.html')
print('version', A.get('version'), '->', B.get('version'))
la=json.load(open('knowledge/_logo_nodes.json'))
src={n['id']:n for n in la['nodes']}
def logos(d): return {n['id']:n for n in d['nodes'] if n.get('type')=='logo'}
LA,LB=logos(A),logos(B)
print('logo nodes before/after:', len(LA), len(LB), '| source file:', len(src))
def logoedges(d):
    ids=set(logos(d))
    return [e for e in d['edges'] if e.get('s') in ids or e.get('t') in ids]
print('logo-touching edges before/after:', len(logoedges(A)), len(logoedges(B)), '| source file edges:', len(la['edges']))
ok=True
for i,n in LB.items():
    s=n.get('sizes')
    if not isinstance(s,dict) or len(s)!=5: ok=False; print('BAD sizes', i, s and len(s)); continue
    if set(s)!=set(src[i]['sizes']): ok=False; print('KEY MISMATCH', i)
    for h,v in s.items():
        if v!=src[i]['sizes'][h]: ok=False; print('VALUE MISMATCH', i, h)
print('all 8 logo nodes carry sizes with 5 keys, identical to _logo_nodes.json:', ok)
print('heights:', sorted({h for n in LB.values() for h in n['sizes']}, key=int))
print('sizes entries total:', sum(len(n['sizes']) for n in LB.values()))
print('sizes present in BEFORE build:', sum(1 for n in LA.values() if 'sizes' in n))
# master files exist on disk
miss=[v['file'] for n in LB.values() for v in n['sizes'].values() if not os.path.exists(os.path.join('knowledge',v['file']))]
print('master files missing on disk:', miss)
# coordinates
K=['x','y','x3','y3','z3','y2','xf','yf','zf','xo','yo','xs','ys','zs']
a={n['id']:[n.get(k) for k in K] for n in A['nodes']}
b={n['id']:[n.get(k) for k in K] for n in B['nodes']}
moved=[i for i in a if i in b and a[i]!=b[i]]
print('nodes total before/after:', len(A['nodes']), len(B['nodes']), '| edges:', len(A['edges']), len(B['edges']))
print('nodes with moved baked coordinates:', len(moved))
