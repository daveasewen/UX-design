import os, json
os.environ["LD_LIBRARY_PATH"] = "/sessions/zen-funny-hawking/pwlibs/prefix/usr/lib/aarch64-linux-gnu:" + os.environ.get("LD_LIBRARY_PATH", "")
from playwright.sync_api import sync_playwright
PAGE = "file:///sessions/zen-funny-hawking/mnt/UX-design/notes/_lanes/261-N-nav-review.html"
OUT = "/sessions/zen-funny-hawking/mnt/UX-design/notes/_lanes/261N4/"
rows = []
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1400, "height": 1000})
    errs = []
    pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
    pg.goto(PAGE); pg.wait_for_timeout(600)
    for th in ["mono", "legacy", "console", "supercharge"]:
        for md in ["light", "dark"]:
            pg.click(f'[data-theme-btn="{th}"]'); pg.click(f'[data-mode-btn="{md}"]')
            pg.wait_for_timeout(250)
            # read the AFTER sidebar frame: serif check + current-row fill + label box
            r = pg.evaluate("""()=>{
              const f=[...document.querySelectorAll('iframe[data-frame]')].find(x=>/Sidebar nav, after/.test(x.title));
              const d=f.contentDocument; const lab=d.querySelector('.nv-label');
              const cur=d.querySelector('.nv-item[aria-current="page"]');
              const cs=getComputedStyle(lab);
              return {family:cs.fontFamily.split(',')[0], boxH:lab.clientHeight,
                      edge:cs.textBoxEdge, curBg:getComputedStyle(cur).backgroundColor,
                      curW:getComputedStyle(cur.querySelector('.nv-label')).fontWeight,
                      bar:getComputedStyle(cur).boxShadow.slice(0,28)};
            }""")
            r.update(theme=th, mode=md); rows.append(r)
    pg.screenshot(path=OUT + "261-N4-review-supercharge-dark.png")
    pg.click('[data-theme-btn="mono"]'); pg.click('[data-mode-btn="light"]'); pg.wait_for_timeout(300)
    pg.screenshot(path=OUT + "261-N4-review-mono-light.png")
    b.close()
print(json.dumps(rows, indent=0))
print("console errors:", len(errs))
