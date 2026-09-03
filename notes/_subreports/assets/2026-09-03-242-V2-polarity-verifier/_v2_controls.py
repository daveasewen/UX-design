import json,os,re,shutil,subprocess,sys,copy
R="/sessions/eager-wizardly-lovelace/mnt/UX-design"; G=os.path.join(R,"knowledge/_validate_polarities.py")
B=os.path.join(R,"knowledge/brain"); W="/dev/shm/v2ctrl"
shutil.rmtree(W,ignore_errors=True); os.makedirs(W)
def cp(t):
    d=os.path.join(W,t); shutil.copytree(B,d); return d
def gate(d,flag="--check"):
    p=subprocess.run([sys.executable,G,flag,"--brain",d],cwd=R,capture_output=True,text=True)
    return p.returncode,sorted(set(re.findall(r"REFUSED \(([A-Za-z0-9-]+)\)",p.stdout+p.stderr))),p.stdout+p.stderr
def mj(p,fn):
    o=json.load(open(p)); fn(o); json.dump(o,open(p,"w"),indent=1,ensure_ascii=False)
P0=json.load(open(os.path.join(B,"polarities.json")))["polarities"][0]
PAR=[{k:v for k,v in x.items() if k!="note"} for x in P0["parties"]]
def node(**o):
    n={"id":"pl-31","parties":copy.deepcopy(PAR),"mediating_variable":"target count","links":[]}; n.update(o); return n
def show(tag,rc,names): print(f"{tag:62} rc={rc} {names}")

# C100-literal: a NEW node citing a FICTIONAL R1 path
d=cp("c100L"); mj(os.path.join(d,"polarities.json"), lambda o:o["polarities"].append(node(sources=[{"path":"notes/_subreports/assets/nope.json","id":"tn-99"}])))
rc,n,_=gate(d); show("C100 literal (fictional source path)",rc,n)
# C100-legal: the same node with $seed
d=cp("c100G"); mj(os.path.join(d,"polarities.json"), lambda o:o["polarities"].append(node(**{"$seed":"s240-D3"})))
rc,n,_=gate(d,"--write"); rc2,n2,_=gate(d); show("C100 s240-D3 legal form ($seed) [write then check]",f"{rc}/{rc2}",n2)
# C225-literal: sources.path outside the repo
d=cp("c225L"); mj(os.path.join(d,"polarities.json"), lambda o:o["polarities"].append(node(sources=[{"path":"/etc/hostname","id":"tn-01"}])))
rc,n,_=gate(d); show("C225 literal (/etc/hostname)",rc,n)
# C248-literal: all-stub node, path 'x'
d=cp("c248L"); mj(os.path.join(d,"polarities.json"), lambda o:o["polarities"].append(node(sources=[{"path":"x","id":"y"}])))
rc,n,_=gate(d); show("C248 literal (path 'x')",rc,n)
# C321-literal: all 30 rows DELETED
d=cp("c321L"); mj(os.path.join(d,"polarities.json"), lambda o:o.__setitem__("polarities",[]))
rc,n,_=gate(d); show("C321 literal (30 rows DELETED)",rc,n)
# C321-legal: all 30 RETIRED then --write, then inspect EVERY generated file
d=cp("c321G"); mj(os.path.join(d,"polarities.json"), lambda o:[x.__setitem__("retiredBy","s240-D3") for x in o["polarities"]])
rcw,_,_=gate(d,"--write"); rc,n,_=gate(d); show("C321 s240-D3 legal (30 RETIRED, --write)",f"{rcw}/{rc}",n)
g=os.path.join(d,"_generated")
files=sorted(os.listdir(g)); print("   _generated/ contents:",files)
ids=set(x["id"] for x in json.load(open(os.path.join(d,"polarities.json")))["polarities"])
for fn in files:
    t=open(os.path.join(g,fn)).read()
    hits=sorted({i for i in ids if re.search(r"\b"+re.escape(i)+r"\b",t)})
    print(f"   RAW-TEXT scan {fn:28} retired ids present: {hits if hits else 'NONE'}")
print("   polarities.json rows kept:",len(ids))
