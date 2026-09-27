import re,glob,sys
def blocks(pattern):
    out={}
    for f in sorted(glob.glob(pattern)):
        t=open(f,errors='replace').read()
        m=re.search(r"THE FULL FAILURE SET.*?\n\n(.*?)(?:\n\n=+|\nCOULD-NOT-ASK \(|\n— recorded|\Z)",t,re.S)
        if not m: continue
        cur=None
        for line in m.group(1).splitlines():
            mm=re.match(r"  \[(\d+)\] (.*)",line)
            if mm: cur=mm.group(2).strip()[:60]; out[cur]=[]; continue
            if cur and line.strip(): out[cur].append(re.sub(r"/sessions/[^/ ]+/(clone[^/ ]*|v4|v5|c4a[^/ ]*|w5a|w5c|f5s|w6s)","<clone>",line.strip()))
    return out
a=blocks(sys.argv[1]); b=blocks(sys.argv[2])
print("A reds:",len(a)); print("B reds:",len(b))
for k in sorted(set(a)|set(b)):
    if k not in a or k not in b: print("ONLY IN",'A' if k in a else 'B',":",k); continue
    if a[k]==b[k]: print("identical",len(a[k]),"lines :",k)
    else:
        print("DIFFERS :",k)
        for x in a[k]:
            if x not in b[k]: print("   A:",x[:220])
        for x in b[k]:
            if x not in a[k]: print("   B:",x[:220])
