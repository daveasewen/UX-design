import re,glob,sys
def load(pfx):
    v,det={}, {}
    for f in sorted(glob.glob(pfx+"*.log")):
        txt=open(f).read()
        for m in re.finditer(r"^  (✅|❌|⊘|⏱) \[\s*(\d+)\]",txt,re.M): v[int(m.group(2))]=m.group(1)
        for m in re.finditer(r"^  \[(\d+)\] .*\n      python3 .*\n      (.*)$",txt,re.M): det[int(m.group(1))]=m.group(2)
    return v,det
for a,b in (("before_m_","after_m_"),("before_nm_","after_nm_")):
    va,da=load(a); vb,db=load(b)
    print(a,b,"steps",len(va),len(vb))
    for i in sorted(set(va)|set(vb)):
        if va.get(i)!=vb.get(i): print("  changed",i,va.get(i),"->",vb.get(i))
    for i in sorted(set(da)&set(db)):
        if da[i]!=db[i]: print("  detail differs",i,"\n   ",da[i][:150],"\n   ",db[i][:150])
    print("  green->red:",[i for i in vb if va.get(i)=="✅" and vb[i]!="✅"])
