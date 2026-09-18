import ast, sys, collections
def lits(p):
    t = ast.parse(open(p, encoding='utf-8').read())
    c = collections.Counter()
    for n in ast.walk(t):
        if isinstance(n, ast.Constant) and isinstance(n.value,(int,float)) and not isinstance(n.value,bool):
            c[repr(n.value)] += 1
    return c
a, b = lits(sys.argv[1]), lits(sys.argv[2])
diff = {k:(a.get(k,0), b.get(k,0)) for k in set(a)|set(b) if a.get(k,0)!=b.get(k,0)}
print(sys.argv[1], "vs", sys.argv[2], "| total HEAD", sum(a.values()), "WORK", sum(b.values()))
print("NUMERIC LITERAL MULTISET DIFF:", diff if diff else "IDENTICAL")
# module-level + class-level assignment constants
def consts(p):
    t = ast.parse(open(p,encoding='utf-8').read()); d={}
    for n in t.body:
        if isinstance(n,(ast.Assign,ast.AnnAssign)):
            tg = n.targets[0] if isinstance(n,ast.Assign) else n.target
            if isinstance(tg,ast.Name) and n.value is not None:
                try: d[tg.id]=ast.literal_eval(n.value)
                except Exception: d[tg.id]='<expr>'
    return d
ca, cb = consts(sys.argv[1]), consts(sys.argv[2])
cd = {k:(ca.get(k,'<absent>'), cb.get(k,'<absent>')) for k in set(ca)|set(cb) if ca.get(k,'<absent>')!=cb.get(k,'<absent>')}
print("MODULE CONSTANT DIFF:", cd if cd else "IDENTICAL")
