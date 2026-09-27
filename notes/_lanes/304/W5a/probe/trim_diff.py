"""trim_diff.py <before-page> <after-page> [...pairs] — W5a attribution: every element in the first 1440x900 layout whose box
height changed between two stagings of the same page (same DOM order), grouped by its nearest cn- scope + tag.class."""
import json, os, sys, collections
from playwright.sync_api import sync_playwright
JS = """() => [...document.body.querySelectorAll('*')].map(e => { const r = e.getBoundingClientRect(); let s = e.closest('[class*="cn-"]');
  const sc = s ? [...s.classList].find(c => c.startsWith('cn-')) : '-'; return [sc, e.tagName.toLowerCase() + '.' + ((e.getAttribute('class')||'').split(' ')[0]), Math.round(r.height*10)/10]; })"""
args = sys.argv[1:]
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ.get("RENDER_SHELL"))
    for i in range(0, len(args), 2):
        res = []
        for f in args[i:i+2]:
            pg = b.new_page(viewport={"width": 1440, "height": 900}, reduced_motion="reduce"); pg.goto("file://" + os.path.abspath(f)); pg.wait_for_timeout(1500)
            res.append(pg.evaluate(JS)); pg.close()
        A, B = res
        c = collections.Counter(); ex = {}
        if len(A) != len(B): print("DOM size differs", len(A), len(B))
        for x, y in zip(A, B):
            if abs(x[2] - y[2]) > 0.5:
                k = (x[0], x[1]); c[k] += 1; ex.setdefault(k, (x[2], y[2]))
        print("==", os.path.basename(args[i]), sum(c.values()), "elements changed height")
        for k, n in c.most_common(25): print("   %3d  %-28s %-40s %s -> %s" % (n, k[0], k[1][:40], ex[k][0], ex[k][1]))
    b.close()
