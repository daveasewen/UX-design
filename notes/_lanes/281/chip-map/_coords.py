import json,sys,re,hashlib
def kg(p):
    s=open(p,encoding='utf-8').read()
    tag='<script id="kg" type="application/json">'
    i=s.index(tag)+len(tag); j=s.index('</script>',i)
    return json.loads(s[i:j])
K=['x','y','x3','y3','z3','y2','xf','yf','zf','xo','yo','xs','ys','zs']
d=kg(sys.argv[1])
out={'coords':{n['id']:[n.get(k) for k in K] for n in d['nodes']},
     'plates':d.get('plates'),'rings':d.get('rings'),'shells':d.get('shells'),'bands':d.get('bands')}
b=json.dumps(out,sort_keys=True,separators=(',',':')).encode()
print(hashlib.md5(b).hexdigest(), len(d['nodes']), len(d['edges']))
open(sys.argv[2],'wb').write(b)
