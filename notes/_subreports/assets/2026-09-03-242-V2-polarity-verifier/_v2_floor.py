import json,os,re,shutil,sys,hashlib,importlib.util,io,contextlib
R="/sessions/eager-wizardly-lovelace/mnt/UX-design"; GP=os.path.join(R,"knowledge/_validate_polarities.py")
B=os.path.join(R,"knowledge/brain"); W="/dev/shm/v2floor"
shutil.rmtree(W,ignore_errors=True); os.makedirs(W)
spec=importlib.util.spec_from_file_location("vp",GP); vp=importlib.util.module_from_spec(spec); spec.loader.exec_module(vp)
def cp(t):
    d=os.path.join(W,t); shutil.copytree(B,d); return d
def mj(p,fn):
    o=json.load(open(p)); fn(o); json.dump(o,open(p,"w"),indent=1,ensure_ascii=False)
def drive(tag, mut):
    d=cp(tag); sp=os.path.join(d,"schema/polarity.schema.json"); mj(sp,mut)
    newsha=hashlib.sha256(open(sp,"rb").read()).hexdigest()
    old=vp.SCHEMA_SHA256; vp.SCHEMA_SHA256=newsha          # THE PIN IS MOVED, as an honest edit would
    buf=io.StringIO()
    with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
        rc=vp.gate(d)
    vp.SCHEMA_SHA256=old
    out=buf.getvalue(); names=sorted(set(re.findall(r"REFUSED \(([A-Za-z0-9-]+)\)",out)))
    print(f"{tag}: rc={rc} names={names}")
    if rc==0: print("   !! ESCAPED:", out.strip().splitlines()[-1][:160])
    else:
        for ln in out.splitlines():
            if "REFUSED (" in ln and "GATE REFUSED" not in ln: print("   ", ln.strip()[:200])
drive("F1-seed-maxWords-1to5", lambda s:s["properties"]["$seed"].__setitem__("maxWords",5))
drive("F2-seed-deleted",       lambda s:s["properties"].__delitem__("$seed"))
drive("F3-retiredBy-deleted",  lambda s:s["properties"].__delitem__("retiredBy"))
drive("F4-seed-pattern-open",  lambda s:s["properties"]["$seed"].__setitem__("pattern",".*"))
drive("F5-seed-type-any",      lambda s:s["properties"]["$seed"].__setitem__("type","object"))
drive("F6-sources-re-required",lambda s:s.__setitem__("required",s["required"]+["sources"]))
drive("F7-addProps-true",      lambda s:s.__setitem__("additionalProperties",True))
