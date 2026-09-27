"""mech2.py <n> <page> — W6: per load, timeline of width transitions (run/end) on chart svgs and every viewBox write, reduced motion."""
import os, sys, json
from playwright.sync_api import sync_playwright
INIT = r"""
window.__tl = []; var T0 = 0;
['transitionrun','transitionend'].forEach(function(t){ document.addEventListener(t, function(e){
  var el = e.target; if (el.matches && el.matches('svg.dv-fit')) window.__tl.push(t.slice(10) + ':' + e.propertyName + '@' + Math.round(performance.now()));
}, true); });
new MutationObserver(function(ms){ ms.forEach(function(m){ if (m.target.matches && m.target.matches('svg.dv-fit') && m.target.closest('#ov-liq')) window.__tl.push('vb=' + m.target.getAttribute('viewBox').split(' ')[2] + '@' + Math.round(performance.now())); }); })
  .observe(document, {attributes: true, attributeFilter: ['viewBox'], subtree: true});
"""
n = int(sys.argv[1])
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ.get("RENDER_SHELL"))
    for i in range(n):
        pg = b.new_page(viewport={"width": 1440, "height": 900}, reduced_motion=os.environ.get("RM", "reduce"))
        pg.add_init_script(INIT); pg.goto("file://" + os.path.abspath(sys.argv[2])); pg.wait_for_timeout(1500)
        r = pg.evaluate("""() => ({tl: window.__tl.filter((x,i,a)=>true).slice(0,30), fit: [...document.querySelectorAll('svg.dv-fit')].map(s => s.viewBox.baseVal.width + '/' + Math.round(s.getBoundingClientRect().width)).join(' ')})""")
        print(r['fit'], ' | ', ' '.join(r['tl'])); pg.close()
    b.close()
