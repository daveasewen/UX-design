import os,json
from playwright.sync_api import sync_playwright
REPO=os.getcwd()
PAGE="file://"+os.path.join(REPO,"notes","_PROPOSAL-list-vs-card-2026-09-15-v1.html")
IDS=["LC-1","LC-2","LC-3","LC-4"]
fails=[]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=os.environ["RENDER_SHELL"],args=["--no-sandbox"])
    ctx=b.new_context(viewport={"width":1280,"height":900}); pg=ctx.new_page()
    errs=[]
    pg.on("console",lambda m: errs.append(m.type+": "+m.text) if m.type=="error" else None)
    pg.on("pageerror",lambda e: errs.append("pageerror: "+str(e)))
    pg.goto(PAGE,wait_until="load"); pg.wait_for_timeout(300)
    # 1. every radio named + every decision has a,b,...,none
    groups=pg.evaluate("""()=>{var g={};document.querySelectorAll('input[type=radio]').forEach(function(i){(g[i.name]=g[i.name]||[]).push({v:i.value,id:i.id,lab:!!document.querySelector('label[for="'+i.id+'"]')});});return g;}""")
    print("radio groups:",json.dumps(groups,indent=0)[:900])
    for k in IDS:
        if k not in groups: fails.append("missing radio group "+k)
    for k,v in groups.items():
        if k not in IDS: fails.append("stray radio group "+k)
        for r in v:
            if not r["lab"]: fails.append("radio %s has no label"%r["id"])
    # 2. click a choice on each + type a note
    pg.check('#LC-1-a'); pg.check('#LC-2-c'); pg.check('#LC-3-b'); pg.check('#LC-4-none')
    pg.fill('textarea[data-id="LC-1"]','driver note one')
    pg.fill('textarea[data-id="LC-3"]','driver note three')
    pg.click('body')  # blur -> focusout flush
    pg.wait_for_timeout(200)
    # 3. export shape
    pg.click('#btnExport'); pg.wait_for_timeout(300)
    exp=json.loads(pg.inner_text('#exp'))
    print("\nEXPORT:",json.dumps(exp,indent=1))
    if set(exp)!={"page","at","decisions"}: fails.append("export top-level keys wrong: %s"%sorted(exp))
    if exp["page"]!="_PROPOSAL-list-vs-card-2026-09-15-v1.html": fails.append("export page wrong")
    if [d["id"] for d in exp["decisions"]]!=IDS: fails.append("export decision ids/order wrong")
    for d in exp["decisions"]:
        if set(d)!={"id","choice","note"}: fails.append("decision keys wrong: %s"%sorted(d))
    got={d["id"]:(d["choice"],d["note"]) for d in exp["decisions"]}
    want={"LC-1":("a","driver note one"),"LC-2":("c",""),"LC-3":("b","driver note three"),"LC-4":(None,"")}
    if got!=want: fails.append("export values wrong: %s"%got)
    # 4. reload -> restore
    pg.reload(wait_until="load"); pg.wait_for_timeout(300)
    st=pg.evaluate("""()=>({a:document.getElementById('LC-1-a').checked,c:document.getElementById('LC-2-c').checked,b:document.getElementById('LC-3-b').checked,n1:document.querySelector('textarea[data-id=\\"LC-1\\"]').value,n3:document.querySelector('textarea[data-id=\\"LC-3\\"]').value,said:document.getElementById('said').textContent})""")
    print("\nAFTER RELOAD:",st)
    if not(st["a"] and st["c"] and st["b"]): fails.append("radios did not restore")
    if st["n1"]!="driver note one" or st["n3"]!="driver note three": fails.append("notes did not restore")
    if not st["said"].startswith("3 of 4 decided"): fails.append("progress wrong: "+st["said"])
    # 5. clear
    pg.on("dialog",lambda d: d.accept())
    pg.click('#btnClear'); pg.wait_for_timeout(300)
    left=pg.evaluate("()=>[...document.querySelectorAll('input[type=radio]')].filter(i=>i.checked).length")
    if left: fails.append("clear left %d radios checked"%left)
    print("\nconsole errors:",errs or 0)
    if errs: fails.append("console errors: %s"%errs)
    ctx.close(); b.close()
print("\n"+("GATE 3 GREEN — all checks pass" if not fails else "GATE 3 RED:\n  "+"\n  ".join(fails)))
