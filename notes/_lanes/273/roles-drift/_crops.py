import os
from playwright.sync_api import sync_playwright
REPO=os.environ["RENDER_REPO"]
PAGE="file://"+os.path.join(REPO,"notes","_REVIEW-roles-drift-2026-09-15-v1.html")
OUT=os.path.join(REPO,"notes","_lanes","273","roles-drift")
secs=["headline","decisions","perrole","silent","fields","receipts"]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=os.environ["RENDER_SHELL"],args=["--no-sandbox"])
    for tag,w,scheme in [("1280-light",1280,"light"),("1280-dark",1280,"dark"),("400-light",400,"light")]:
        ctx=b.new_context(viewport={"width":w,"height":1000},color_scheme=scheme)
        pg=ctx.new_page(); pg.goto(PAGE,wait_until="load"); pg.wait_for_timeout(300)
        for s in secs:
            el=pg.query_selector("#"+s)
            box=el.bounding_box()
            clip={"x":0,"y":box["y"],"width":w,"height":min(box["height"],1400)}
            el.screenshot(path=os.path.join(OUT,"crop-%s-%s.png"%(tag,s)),
                          clip=None) if False else pg.screenshot(
                          path=os.path.join(OUT,"crop-%s-%s.png"%(tag,s)),clip=clip,full_page=True)
        ctx.close()
    b.close()
print("ok")
