import os, json
from playwright.sync_api import sync_playwright
REPO=os.environ["RENDER_REPO"]
PAGE="file://"+os.path.join(REPO,"notes","_REVIEW-roles-drift-2026-09-15-v1.html")
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=os.environ["RENDER_SHELL"],args=["--no-sandbox"])
    ctx=b.new_context(viewport={"width":1280,"height":900}); pg=ctx.new_page()
    errs=[]; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(PAGE,wait_until="load")
    # every radio has a name
    names=pg.eval_on_selector_all('input[type=radio]','els=>els.map(e=>e.name)')
    assert all(names), "radio without a name"
    print("radios:",len(names),"groups:",sorted(set(names)))
    pg.check('#RD-1-a'); pg.check('#RD-3-c')
    pg.fill('textarea[data-id="RD-2"]','scope pass 2 after the push')
    pg.click('#btnExport')
    pg.wait_for_timeout(300)
    out=json.loads(pg.inner_text('#exp'))
    print("export keys:",sorted(out.keys()))
    print(json.dumps(out["decisions"],indent=1))
    ls=pg.evaluate("localStorage.getItem('apollo-roles-drift-273-v1')")
    print("localStorage:", (ls or "")[:120])
    print("saidline:", pg.inner_text("#said"))
    # reload -> restore
    pg.reload(wait_until="load"); pg.wait_for_timeout(300)
    print("after reload RD-1-a checked:", pg.is_checked('#RD-1-a'),
          "| note:", pg.input_value('textarea[data-id="RD-2"]'))
    print("pageerrors:",errs)
    b.close()
