import json,os,re,shutil,hashlib,importlib.util,io,contextlib,copy
R="/sessions/eager-wizardly-lovelace/mnt/UX-design"; GP=os.path.join(R,"knowledge/_validate_polarities.py")
B=os.path.join(R,"knowledge/brain"); W="/dev/shm/v2f6"
shutil.rmtree(W,ignore_errors=True); os.makedirs(W)
spec=importlib.util.spec_from_file_location("vp",GP); vp=importlib.util.module_from_spec(spec); spec.loader.exec_module(vp)
d=os.path.join(W,"t"); shutil.copytree(B,d)
sp=os.path.join(d,"schema/polarity.schema.json"); s=json.load(open(sp)); s["required"]=s["required"]+["sources"]
json.dump(s,open(sp,"w"),indent=1,ensure_ascii=False)
pp=os.path.join(d,"polarities.json"); o=json.load(open(pp))
parties=[{k:v for k,v in x.items() if k!="note"} for x in o["polarities"][0]["parties"]]
o["polarities"].append({"id":"pl-40","parties":copy.deepcopy(parties),"mediating_variable":"target count","links":[],"$seed":"s240-D3"})
json.dump(o,open(pp,"w"),indent=1,ensure_ascii=False)
vp.SCHEMA_SHA256=hashlib.sha256(open(sp,"rb").read()).hexdigest()
buf=io.StringIO()
with contextlib.redirect_stdout(buf),contextlib.redirect_stderr(buf): rc=vp.gate(d)
out=buf.getvalue()
print("rc=",rc,"names=",sorted(set(re.findall(r"REFUSED \(([A-Za-z0-9-]+)\)",out))))
for ln in out.splitlines():
    if "REFUSED (" in ln and "GATE REFUSED" not in ln: print("  ",ln.strip()[:190])
