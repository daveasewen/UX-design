import os
from playwright.sync_api import sync_playwright
W=os.path.expanduser('~/cold/cand-r1'); URL='file://'+W+'/out/index.html'
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=os.environ['RENDER_SHELL']); pg=b.new_page(viewport={'width':1440,'height':900})
    for v in ['overview','accounts','liquidity','payments','fx','risk','trade','reports','messages','settings']:
        pg.goto(URL+'?view='+v); pg.wait_for_timeout(700); pg.screenshot(path=W+'/out/proof/screens/%s-1440-light.png'%v)
    pg.goto(URL+'?view=overview&theme=dark'); pg.wait_for_timeout(700); pg.screenshot(path=W+'/out/proof/screens/overview-1440-dark.png')
    b.close()
