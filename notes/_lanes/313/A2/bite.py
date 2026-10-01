import os, json, re
from playwright.sync_api import sync_playwright
src = open('/tmp/a2_probe/probe.py').read()
GAPJS = re.search(r'GAPJS = r"""(.*?)"""', src, re.S).group(1)
K='/tmp/a2/knowledge/snippets/'
out = {}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ["RENDER_SHELL"])
    for arm, css in (("no-lift", 'path.dv-band, polyline.dv-band-line{--lift:0px !important}'),
                     ("origin-at-top", 'figure.dv-animate[data-dv-type="stacked-area"] path.dv-band{transform-origin:0 0 !important}'),
                     ("faded-back", 'figure.dv-animate[data-dv-type="stacked-area"] svg.dv-svg{animation:none !important}')):
        pg = b.new_page(viewport={"width": 1180, "height": 900}); pg.goto('file://' + K + 'Chart-stacked-area.reference.html')
        pg.add_style_tag(content=css); pg.wait_for_timeout(200)
        r = pg.evaluate(GAPJS, 0.5); out[arm] = {k: r[k] for k in ('f', 'minGap', 'maxGap', 'footDev', 'stackH')}; pg.close()
    b.close()
print(json.dumps(out))
json.dump(out, open('/tmp/a2_probe/bite.json', 'w'), indent=1)
