# #308-morning fix: the cold-run review has a way back and no dead link.
import os
from playwright.sync_api import sync_playwright
P="file://"+os.path.abspath("reviews/COLDRUN-307-2026-09-28-v1.html")
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=os.environ["RENDER_SHELL"]); pg=b.new_page(viewport={"width":390,"height":800}); errs=[]
    pg.on("pageerror",lambda e:errs.append(str(e))); pg.goto(P)
    print("back visible:",pg.locator("#rv-back").is_visible(),"| href:",pg.locator("#rv-back").get_attribute("href"),
          "| relative links:",pg.evaluate("[...document.links].map(a=>a.getAttribute('href')).filter(h=>h&&!/^(https?:|#|mailto)/.test(h))"),"| errors",errs)
    print("h-overflow", pg.evaluate("document.documentElement.scrollWidth-innerWidth")); pg.screenshot(path="notes/_lanes/307/C/check-coldrun-back-390.png"); b.close()
