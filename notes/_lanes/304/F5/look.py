"""look.py — F5: element screenshots of the corrected parts of the sitting page (calls 1, 4, 5 note, 6, 11, 23, 53, the slot), 1440 and 390."""
import os
from playwright.sync_api import sync_playwright
ROOT=os.getcwd(); PAGE=os.path.join(ROOT,'notes/_SITTING-304-tuesday-2026-09-29-v1.html'); O=os.path.join(ROOT,'notes/_lanes/304/F5/shots'); os.makedirs(O,exist_ok=True)
T={'call01':('#release .decide > li',0),'call04':('#release .decide > li',3),'call05':('#looks .decide > li',0),'call06':('#looks .decide > li',1),
   'call11':('#looks .decide > li',6),'call23':('#brain .decide > li',9),'call53':('#jev .decide > li',1),'slot':('.slot',0),'stats':('#answer .stats',0)}
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=os.environ['RENDER_SHELL'])
    for w in (1440,390):
        pg=b.new_page(viewport={'width':w,'height':1000}); pg.goto('file://'+PAGE); pg.wait_for_timeout(600)
        pg.evaluate("() => document.querySelectorAll('img[loading]').forEach(i => i.loading='eager')"); pg.wait_for_timeout(1500)
        for k,(sel,i) in T.items():
            el=pg.locator(sel).nth(i); el.scroll_into_view_if_needed(); pg.wait_for_timeout(300)
            el.screenshot(path=os.path.join(O,'%s-w%d.png'%(k,w)))
        print(w, pg.evaluate("() => [...document.querySelectorAll('.slotcalls .dd-label')].map(e=>e.textContent)"),
              pg.evaluate("() => [...document.querySelectorAll('.decide .dd-label')].slice(-3).map(e=>e.textContent)"))
        pg.close()
    b.close()
