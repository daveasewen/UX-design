import json,os,re,shutil,subprocess,sys,hashlib
R="/sessions/eager-wizardly-lovelace/mnt/UX-design"; G=os.path.join(R,"knowledge/_validate_polarities.py")
B=os.path.join(R,"knowledge/brain"); W="/dev/shm/v2hand"
shutil.rmtree(W,ignore_errors=True); os.makedirs(W)
def cp(t):
    d=os.path.join(W,t); shutil.copytree(B,d); return d
def gate(d,flag,gpath=G):
    p=subprocess.run([sys.executable,gpath,flag,"--brain",d],cwd=R,capture_output=True,text=True)
    return p.returncode,p.stdout+p.stderr
def nm(o): return sorted(set(re.findall(r"REFUSED \(([A-Za-z0-9-]+)\)",o)))
def mj(p,fn):
    o=json.load(open(p)); fn(o); json.dump(o,open(p,"w"),indent=1,ensure_ascii=False)

# V row 241 — principles statement rewritten
d=cp("r241"); mj(os.path.join(d,"principles.json"), lambda p:p["principles"][0].__setitem__("statement","Fitts is wrong and Apollo ignores it."))
rw=gate(d,"--write"); rc=gate(d,"--check"); print("241 write-rc",rw[0],"check-rc",rc[0],nm(rc[1]))
# V row 243 — resolvedBy AND challengedBy same ruling
d=cp("r243"); mj(os.path.join(d,"polarities.json"), lambda o:o["polarities"][15]["links"].append({"type":"challengedBy","ref":"s116-D1"}))
rw=gate(d,"--write"); rc=gate(d,"--check"); print("243 write-rc",rw[0],"check-rc",rc[0],nm(rc[1]))
# V row 245 — all links deleted
d=cp("r245"); mj(os.path.join(d,"polarities.json"), lambda o:[n.__setitem__("links",[]) for n in o["polarities"]])
rw=gate(d,"--write"); rc=gate(d,"--check"); print("245 write-rc",rw[0],"check-rc",rc[0],nm(rc[1]))
# V row 301 — grade flip in principles
d=cp("r301")
def flip(p):
    for x in p["principles"]:
        if x.get("id")=="pr-wcag-1-4-3": x["grade"]="C"
mj(os.path.join(d,"principles.json"),flip)
rw=gate(d,"--write"); rc=gate(d,"--check"); print("301 write-rc",rw[0],"check-rc",rc[0],nm(rc[1]))
# V row 310 — schema sources.items.additionalProperties true + a judgement key
d=cp("r310")
mj(os.path.join(d,"schema/polarity.schema.json"), lambda s:s["properties"]["sources"]["items"].__setitem__("additionalProperties",True))
mj(os.path.join(d,"polarities.json"), lambda o:o["polarities"][0]["sources"][0].__setitem__("judgement","Jakob wins in Apollo"))
rc=gate(d,"--check"); print("310 check-rc",rc[0],nm(rc[1]))
# V row 30 — resolvedBy a prose-superseded ruling
d=cp("r30"); mj(os.path.join(d,"polarities.json"), lambda o:o["polarities"][2]["links"].append({"type":"resolvedBy","ref":"s200-D2"}))
rc=gate(d,"--check"); print("30  check-rc",rc[0],nm(rc[1]))

# ---- THE FLOOR TEST: loosen the schema AND move the pin in a COPY of the gate --------------
d=cp("floor"); sp=os.path.join(d,"schema/polarity.schema.json")
mj(sp, lambda s:s["properties"]["$seed"].__setitem__("maxWords",5))
newsha=hashlib.sha256(open(sp,"rb").read()).hexdigest()
g2=os.path.join(W,"gate_pinmoved.py"); t=open(G).read()
old=re.search(r'SCHEMA_SHA256 = "([0-9a-f]{64})"',t).group(1)
open(g2,"w").write(t.replace(old,newsha))
rc=gate(d,"--check",gpath=g2); print("FLOOR (pin MOVED, $seed maxWords 1->5) check-rc",rc[0],nm(rc[1]))
# and: delete $seed from properties, pin moved
d=cp("floor2"); sp=os.path.join(d,"schema/polarity.schema.json")
mj(sp, lambda s:s["properties"].__delitem__("$seed"))
newsha=hashlib.sha256(open(sp,"rb").read()).hexdigest()
g3=os.path.join(W,"gate_pin2.py"); open(g3,"w").write(t.replace(old,newsha))
rc=gate(d,"--check",gpath=g3); print("FLOOR2 (pin MOVED, $seed DELETED from schema) check-rc",rc[0],nm(rc[1]))
# and: put `sources` back into required, pin moved -> is that a TIGHTENING (allowed) that BREAKS $seed nodes?
d=cp("floor3"); sp=os.path.join(d,"schema/polarity.schema.json")
mj(sp, lambda s:s.__setitem__("required",s["required"]+["sources"]))
newsha=hashlib.sha256(open(sp,"rb").read()).hexdigest()
g4=os.path.join(W,"gate_pin3.py"); open(g4,"w").write(t.replace(old,newsha))
rc=gate(d,"--check",gpath=g4); print("FLOOR3 (pin MOVED, `sources` re-required) check-rc",rc[0],nm(rc[1]))
