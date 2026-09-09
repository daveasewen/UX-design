import os, sys, json
os.environ["LD_LIBRARY_PATH"] = "/sessions/zen-funny-hawking/pwlibs/prefix/usr/lib/aarch64-linux-gnu:" + os.environ.get("LD_LIBRARY_PATH", "")
from playwright.sync_api import sync_playwright
BASE = "/sessions/zen-funny-hawking/mnt/UX-design/knowledge/snippets/"
OUT = "/sessions/zen-funny-hawking/mnt/UX-design/notes/_lanes/261N4/"
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1280, "height": 900})
    for name, mode in [("Sidebar-nav", "light"), ("Sidebar-nav", "dark"), ("Navigations", "light"), ("Tab-bar", "light")]:
        pg.goto("file://" + BASE + name + ".reference.html")
        pg.evaluate("m=>{document.documentElement.setAttribute('data-theme',m);document.body.setAttribute('data-theme',m);}", mode)
        pg.wait_for_timeout(250)
        pg.screenshot(path=f"{OUT}261-N4-{name.lower()}-{mode}.png", full_page=False)
    # greek bar sanity + current-row computed background
    pg.goto("file://" + BASE + "Sidebar-nav.reference.html")
    print(json.dumps(pg.evaluate("""()=>({
      greek: [...document.querySelectorAll('.sn-canvas > span')].map(s=>s.clientHeight),
      current: [...document.querySelectorAll('.nv-item[aria-current=\"page\"]')].map(a=>({
        bg:getComputedStyle(a).backgroundColor, shadow:getComputedStyle(a).boxShadow,
        w:getComputedStyle(a.querySelector('.nv-label')||a).fontWeight})),
      hover_rule: getComputedStyle(document.querySelector('.nv-item')).backgroundColor
    })"""), indent=1))
    b.close()
