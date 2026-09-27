import ast,sys,json
src=open(sys.argv[1] if len(sys.argv)>1 else 'knowledge/_build_all.py').read()
t=ast.parse(src)
for n in t.body:
    if isinstance(n,ast.Assign) and any(getattr(x,'id',None)=='STEPS' for x in n.targets):
        steps=ast.literal_eval(n.value)
out=[(i+1,s[0],s[1],s[2] if len(s)>2 else []) for i,s in enumerate(steps)]
if '--json' in sys.argv: print(json.dumps(out))
else:
    for o in out: print(o)
