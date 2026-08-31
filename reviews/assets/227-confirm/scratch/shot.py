import sys, json
from playwright.sync_api import sync_playwright
jobs=json.load(open(sys.argv[1]))
with sync_playwright() as p:
    b=p.chromium.launch()
    for j in jobs:
        pg=b.new_page(viewport={'width':j.get('w',1200),'height':j.get('h',700)},device_scale_factor=2)
        pg.goto(j['url']); pg.wait_for_timeout(j.get('wait',700))
        if j.get('js'): pg.evaluate(j['js'])
        pg.wait_for_timeout(j.get('wait2',200))
        if j.get('sel'):
            el=pg.query_selector(j['sel'])
            if el is None: print("MISSING SEL",j['sel'],j['out']); pg.close(); continue
            el.screenshot(path=j['out'])
        elif j.get('clip'):
            pg.screenshot(path=j['out'], clip=j['clip'])
        else:
            pg.screenshot(path=j['out'], full_page=j.get('full',False))
        print("OK",j['out'])
        pg.close()
    b.close()
