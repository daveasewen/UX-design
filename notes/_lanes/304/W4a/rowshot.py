"""rowshot.py <variant> <run> <file> <out.png> [narrow] — the outermost bento tile holding the first ring, 1440 light.
narrow = RENDER-ONLY mock: the ring's figure confined to half its tile's width (what a narrow column would give it)."""
import os, sys
from playwright.sync_api import sync_playwright
V, RUN, FILE, OUT = sys.argv[1:5]; MODE = sys.argv[5] if len(sys.argv) > 5 else ''
JS = r"""(mode) => { const f = document.querySelector('figure.dv[data-dv-type=donut], figure.dv[data-dv-type=pie]'); if (!f) return null;
  let t = f.closest('.c-bento__tile'), top = t; while (t) { top = t; t = t.parentElement && t.parentElement.closest('.c-bento__tile'); }
  if (mode === 'narrow') { f.parentElement.style.width = 'calc(50% - 12px)'; window.dispatchEvent(new Event('resize')); }
  top.setAttribute('data-w4a-row', '1'); return {tileH: Math.round(f.closest('.c-bento__tile').getBoundingClientRect().height), rowH: Math.round(top.getBoundingClientRect().height)}; }"""
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ["RENDER_SHELL"]); c = b.new_context(viewport={'width': 1440, 'height': 900}); pg = c.new_page()
    pg.goto('file://' + os.path.expanduser('~/w4a/st/%s/cold-%s/out/%s' % (V, RUN, FILE))); pg.wait_for_timeout(1500)
    print(pg.evaluate(JS, MODE)); pg.wait_for_timeout(1200)
    pg.locator('[data-w4a-row]').first.screenshot(path=OUT); b.close()
