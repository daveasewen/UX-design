"""mech.py <page> — W6: log width-ish CSS transitions touching chart svgs + final fit state, reduced motion."""
import os, sys, json
from playwright.sync_api import sync_playwright
INIT = r"""
window.__tl = [];
['transitionrun','transitionend'].forEach(function(t){ document.addEventListener(t, function(e){
  var el = e.target; if (!el.matches) return;
  if (el.matches('svg.dv-fit, :has(svg.dv-fit)')) window.__tl.push([t, e.propertyName, el.tagName + '.' + (el.getAttribute('class')||'').split(' ')[0], Math.round(performance.now()), Math.round(el.getBoundingClientRect().width)]);
}, true); });
"""
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ.get("RENDER_SHELL"))
    pg = b.new_page(viewport={"width": 1440, "height": 900}, reduced_motion=os.environ.get("RM", "reduce"))
    pg.add_init_script(INIT); pg.goto("file://" + os.path.abspath(sys.argv[1])); pg.wait_for_timeout(1500)
    r = pg.evaluate("""() => ({tl: window.__tl.slice(0,40), n: window.__tl.length, svgs: [...document.querySelectorAll('svg.dv-fit')].map(s => [s.closest('figure') && s.closest('figure').id, s.viewBox.baseVal && s.viewBox.baseVal.width, Math.round(s.getBoundingClientRect().width)])})""")
    print(json.dumps(r, indent=0)); b.close()
