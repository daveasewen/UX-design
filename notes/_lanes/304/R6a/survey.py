"""R6a survey: full-page shots of candidate snippets, to pick specimen crops. Run from repo root."""
import os, sys, json
from playwright.sync_api import sync_playwright
ROOT=os.getcwd(); SN=os.path.join(ROOT,'knowledge/snippets'); OUT=os.path.join(ROOT,'notes/_lanes/304/R6a/survey')
names=sys.argv[1:]
res={}
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=os.environ['RENDER_SHELL'])
    ctx=b.new_context(viewport={'width':1280,'height':900},device_scale_factor=1)
    for n in names:
        pg=ctx.new_page(); pg.goto('file://'+os.path.join(SN,n+'.reference.html')); pg.wait_for_timeout(500)
        h=pg.evaluate('document.documentElement.scrollHeight')
        pg.screenshot(path=os.path.join(OUT,n+'.png'),full_page=True, clip={'x':0,'y':0,'width':1280,'height':min(h,5000)})
        res[n]=h; pg.close()
    b.close()
print(json.dumps(res))
