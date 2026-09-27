"""edge_pages.py <out.json> <page> ... — W5a: R4s2's probe_edge measure (visible svg text whose ink runs past its
chart's clip frame by >1px, left or right) on page FILES at 1440, light. Writes <out.json>."""
import json, os, sys
from playwright.sync_api import sync_playwright
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'R4s2'))
JS = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'R4s2', 'probe_edge.py')).read().split('JS = r"""', 1)[1].split('"""', 1)[0]
out = {}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ.get("RENDER_SHELL"))
    for f in sys.argv[2:]:
        pg = b.new_page(viewport={"width": 1440, "height": 900}, reduced_motion="reduce")
        errs = []; pg.on('pageerror', lambda e: errs.append(str(e)[:120]))
        pg.goto('file://' + os.path.abspath(f), wait_until='load'); pg.wait_for_timeout(1600)
        r = pg.evaluate(JS); out[f] = {'n': len(r), 'cut': r, 'errors': errs}; pg.close()
    b.close()
json.dump(out, open(sys.argv[1], 'w'), indent=1)
print(sum(v['n'] for v in out.values()), 'cut texts on', sum(1 for v in out.values() if v['n']), 'of', len(out), 'pages;',
      sum(len(v['errors']) for v in out.values()), 'page errors')
