import json, subprocess, hashlib, os, collections, sys
head = json.loads(subprocess.run(["git","show","HEAD:knowledge/_logo_nodes.json"],capture_output=True,text=True).stdout)
work = json.load(open("knowledge/_logo_nodes.json"))
ok = True
def chk(label, cond, extra=""):
    global ok
    print(("PASS " if cond else "FAIL ")+label+(" :: "+str(extra) if extra else ""))
    if not cond: ok=False

hn, wn = head["nodes"], work["nodes"]
chk("node count 8==8", len(hn)==8 and len(wn)==8, f"head={len(hn)} work={len(wn)}")
hids = sorted(n["id"] for n in hn); wids = sorted(n["id"] for n in wn)
chk("node id sets identical", hids==wids)

def emult(d):
    return collections.Counter(json.dumps(e, sort_keys=True) for e in d["edges"])
he, we = emult(head), emult(work)
chk("edge multiset identical", he==we, f"head={sum(he.values())} work={sum(we.values())}")
gb = [e for e in work["edges"] if e.get("type")=="governedBy"]
chk("12 governedBy edges", len(gb)==12, len(gb))
hgb = [e for e in head["edges"] if e.get("type")=="governedBy"]
chk("governedBy byte-identical head/work", sorted(json.dumps(e,sort_keys=True) for e in hgb)==sorted(json.dumps(e,sort_keys=True) for e in gb))

for n in sorted(wn, key=lambda x: x["id"]):
    s = n.get("sizes")
    chk(f"{n['id']}: sizes map with 5 entries", isinstance(s,dict) and len(s)==5, None if isinstance(s,dict) else repr(s))
    if not isinstance(s,dict): continue
    for h,v in sorted(s.items(), key=lambda kv:int(kv[0])):
        p = os.path.join("knowledge", v["file"])
        if not os.path.exists(p):
            chk(f"  {n['id']}/{h}: file exists", False, p); continue
        d = hashlib.sha256(open(p,"rb").read()).hexdigest()
        chk(f"  {n['id']}/{h} sha256", d==v["sha256"], f"{p} disk={d[:12]} json={v['sha256'][:12]}")
tot = sum(len(n.get("sizes",{})) for n in wn)
chk("40 size entries total", tot==40, tot)
print("\nOVERALL:", "GREEN" if ok else "RED")
sys.exit(0 if ok else 1)
