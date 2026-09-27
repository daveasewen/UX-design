import re,glob,sys,hashlib
def blocks(pattern):
    out={}
    for f in sorted(glob.glob(pattern)):
        t=open(f,errors='replace').read()
        m=re.search(r"THE FULL FAILURE SET.*?\n\n(.*?)(?:\n\n=+|\nCOULD-NOT-ASK \(|\n— recorded|\Z)",t,re.S)
        if not m: continue
        cur=None
        for line in m.group(1).splitlines():
            mm=re.match(r"  \[(\d+)\] ",line)
            if mm: cur=int(mm.group(1)); out[cur]=[]; continue
            if cur and line.strip(): out[cur].append(re.sub(r"/sessions/[^/ ]+/(clone[^/ ]*|v4|c4a[^/ ]*)","<clone>",line.strip()))
    return out
a=blocks(sys.argv[1]); b=blocks(sys.argv[2])
print("A reds:",sorted(a)); print("B reds:",sorted(b))
for k in sorted(set(a)|set(b)):
    if k not in a or k not in b: print(k,"ONLY IN",'A' if k in a else 'B'); continue
    if a[k]==b[k]: print(k,"identical",len(a[k]),"lines")
    else:
        print(k,"DIFFERS"); 
        for x in a[k]:
            if x not in b[k]: print("   A:",x[:200])
        for x in b[k]:
            if x not in a[k]: print("   B:",x[:200])
