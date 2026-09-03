import json, os, re, shutil, subprocess, sys, copy
REPO = "/sessions/eager-wizardly-lovelace/mnt/UX-design"
GATE = os.path.join(REPO, "knowledge/_validate_polarities.py")
BRAIN = os.path.join(REPO, "knowledge/brain")
ROOT = os.environ.get("V2ROOT", "/dev/shm/v2work")
shutil.rmtree(ROOT, ignore_errors=True); os.makedirs(ROOT)

def brain_copy(tag):
    d = os.path.join(ROOT, tag); shutil.copytree(BRAIN, d); return d
def run(d, write=False):
    p = subprocess.run([sys.executable, GATE, "--brain", d, "--write" if write else "--check"],
                       cwd=REPO, capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr
NAMES = re.compile(r"\b(R[1-5]-[A-Z-]+|S-[A-Z-]+|SCHEMA-[A-Z-]+|STALE-GENERATED|MISSING-GENERATED)\b")
def names(out):
    s=[]
    for m in NAMES.findall(out):
        if m not in s: s.append(m)
    return s
def mutpol(d, fn):
    p=os.path.join(d,"polarities.json"); o=json.load(open(p)); fn(o)
    open(p,"w").write(json.dumps(o,indent=1,ensure_ascii=False)+"\n")
def mutschema(d, fn):
    p=os.path.join(d,"schema/polarity.schema.json"); o=json.load(open(p)); fn(o)
    open(p,"w").write(json.dumps(o,indent=1,ensure_ascii=False)+"\n")
RES=[]
def arm(tag, expect, build, want=None, write=False):
    d=brain_copy(tag)
    try: build(d)
    except Exception as e:
        RES.append((tag,expect,"BUILD-CRASH",repr(e)[:160],"FAIL")); return
    rc,out=run(d,write=write); nm=names(out); tb="Traceback" in out
    ok = (rc==1 and (want is None or all(w in nm for w in ([want] if isinstance(want,str) else want)))) if expect=="red" else (rc==0)
    RES.append((tag,expect,rc,("names="+",".join(nm) if nm else "-")+(" TRACEBACK" if tb else ""),"OK" if ok else "FAIL"))
    if not ok: RES.append(("   ^tail","","",out[-600:].replace("\n"," | "),""))
R="s240-D3"
_p=json.load(open(os.path.join(BRAIN,"polarities.json")))["polarities"]
PARTIES=[{k:v for k,v in x.items() if k!="note"} for x in _p[0]["parties"]]
def newnode(**o):
    n={"id":"pl-40","parties":copy.deepcopy(PARTIES),"mediating_variable":"target count","links":[],"$seed":R}
    n.update(o); return n

arm("A1-both-on-new-node","red", lambda d: mutpol(d, lambda o: o["polarities"].append(
    newnode(sources=copy.deepcopy(o["polarities"][0]["sources"])))), "S-SOURCE")
arm("A2-both-sources-empty-array","red", lambda d: mutpol(d, lambda o: o["polarities"].append(newnode(sources=[]))))
arm("A3-seed-is-a-list-with-sources","red", lambda d: mutpol(d, lambda o: o["polarities"][0].__setitem__("$seed",[R])))
arm("A4-seed-empty-string","red", lambda d: mutpol(d, lambda o: o["polarities"].append(newnode(**{"$seed":""}))))
arm("A5-seed-wrong-case","red", lambda d: mutpol(d, lambda o: o["polarities"].append(newnode(**{"$seed":"S240-D3"}))), "R1-DANGLING")
arm("A6-seed-s240-D9-absent","red", lambda d: mutpol(d, lambda o: o["polarities"].append(newnode(**{"$seed":"s240-D9"}))), "R1-DANGLING")
arm("A7-seed-names-a-principle","red", lambda d: mutpol(d, lambda o: o["polarities"].append(newnode(**{"$seed":"pr-jakobs-law"}))), "R1-DANGLING")
arm("A8-retired-no-birth-receipt","red", lambda d: mutpol(d, lambda o: o["polarities"].append(
    {k:v for k,v in newnode(retiredBy=R).items() if k!="$seed"})), "S-SOURCE")
arm("A9-all-three-keys","red", lambda d: mutpol(d, lambda o: (o["polarities"][0].__setitem__("$seed",R),
    o["polarities"][0].__setitem__("retiredBy",R))), "S-SOURCE")
def a10(d):
    mutpol(d, lambda o:[n.__setitem__("retiredBy",R) for n in o["polarities"]])
    rc,out=run(d,write=True); open(os.path.join(ROOT,"a10-write.log"),"w").write(f"rc={rc}\n{out}")
arm("A10-retire-all-30-then-write","green", a10)
def a11(d):
    mutpol(d, lambda o:o["polarities"][-1].__setitem__("retiredBy",R)); run(d,write=True)
    p=os.path.join(d,"_generated/polarity-status.json"); o=json.load(open(p))
    o["delta_vs_237T"]["cause"]=str(o["delta_vs_237T"].get("cause",""))+" pl-30 leaked here"
    open(p,"w").write(json.dumps(o,indent=1,ensure_ascii=False)+"\n")
arm("A11-retired-id-in-prose-of-generated","red", a11)
arm("A12-schema-add-property","red", lambda d: mutschema(d, lambda s: s["properties"].__setitem__("judgement",{"type":"string"})), "SCHEMA-PIN-MISMATCH")
arm("A13-schema-delete-retiredBy","red", lambda d: mutschema(d, lambda s: s["properties"].__delitem__("retiredBy")), ["SCHEMA-LOOSENED","SCHEMA-PIN-MISMATCH"])
arm("A14-schema-loosen-seed-maxWords","red", lambda d: mutschema(d, lambda s: s["properties"]["$seed"].__setitem__("maxWords",5)), ["SCHEMA-LOOSENED","SCHEMA-PIN-MISMATCH"])
def a15(d):
    p=os.path.join(d,"schema/polarity.schema.json"); t=open(p).read()
    open(p,"w").write(t.replace('"title": "Polarity','"title": "polarity',1))
arm("A15-schema-one-byte-title","red", a15, "SCHEMA-PIN-MISMATCH")
arm("A16-green-seed-node-write","green", lambda d: mutpol(d, lambda o:o["polarities"].append(newnode())), write=True)
arm("A17-green-seed-node-also-retired","green", lambda d: mutpol(d, lambda o:o["polarities"].append(newnode(retiredBy=R))), write=True)
arm("A18-seed-names-SUPERSEDED-ruling","green", lambda d: mutpol(d, lambda o:o["polarities"].append(newnode(**{"$seed":"s129-D1"}))), write=True)
arm("A19-seed-names-NOT-RULED-id","green", lambda d: mutpol(d, lambda o:o["polarities"].append(newnode(**{"$seed":"ds-021"}))), write=True)
arm("A20-retiredBy-superseded","green", lambda d: mutpol(d, lambda o:o["polarities"][-1].__setitem__("retiredBy","s129-D1")), write=True)
def a21(d):
    mutpol(d, lambda o:(o["polarities"][0].__setitem__("retiredBy",R),
        o["polarities"][0]["links"].__setitem__(0,{"type":"resolvedBy","ref":"s151-D1","quote":"THIS QUOTE IS NOT VERBATIM ANYWHERE"})))
arm("A21-retired-node-bogus-quote","red", a21, "R3-QUOTE-NOT-VERBATIM")
arm("A22-stray-file-in-generated","red", lambda d: open(os.path.join(d,"_generated","polarity-extra.json"),"w").write("{}"), "R4-STRAY-FILE")
for r in RES: print(" | ".join(str(x) for x in r))
