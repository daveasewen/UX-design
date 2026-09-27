"""k3all.py <dirA> <dirB> <out> <glob> [start end] — V5's K3 JS, light only, 1440, reduced motion: every page in dirA/glob v the same
name in dirB; counts text elements whose box height moved >1px, chart (cn-chart-*) v non-chart, lists non-chart groups."""
import os, sys, glob, collections, json
from playwright.sync_api import sync_playwright
JS = """() => [...document.body.querySelectorAll('*')].filter(e => [...e.childNodes].some(n => n.nodeType===3 && n.textContent.trim())).map(e => { const r = e.getBoundingClientRect(); let s = e.closest('[class*="cn-"]');
  const sc = s ? [...s.classList].find(c => c.startsWith('cn-')) : '-'; return [sc, e.tagName.toLowerCase() + '.' + ((e.getAttribute('class')||'').split(' ')[0]), Math.round(r.height*10)/10, (e.textContent||'').trim().slice(0,24)]; })"""
A, B, out, g = sys.argv[1:5]; files = sorted(glob.glob(os.path.join(A, g)))
if len(sys.argv) > 6: files = files[int(sys.argv[5]):int(sys.argv[6])]
rows = []
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ.get("RENDER_SHELL"))
    for fa in files:
        fb = os.path.join(B, os.path.relpath(fa, A)); res = []
        for f in (fa, fb):
            pg = b.new_page(viewport={"width":1440,"height":900}, reduced_motion="reduce"); pg.goto("file://" + os.path.abspath(f)); pg.wait_for_timeout(500)
            pg.evaluate("t=>document.documentElement.setAttribute('data-theme',t)", 'light'); pg.wait_for_timeout(300)
            res.append(pg.evaluate(JS)); pg.close()
        X, Y = res
        if len(X) != len(Y): rows.append([os.path.relpath(fa, A), 'DOM differs', len(X), len(Y)]); continue
        c = collections.Counter(); ch = non = 0
        for x, y in zip(X, Y):
            if abs(x[2]-y[2]) > 1.0:
                if x[0].startswith('cn-chart'): ch += 1
                else: non += 1; c['%s %s %s->%s %r' % (x[0], x[1], x[2], y[2], x[3])] += 1
        rows.append([os.path.relpath(fa, A), len(X), ch, non, c.most_common(8)])
    b.close()
with open(out, 'a') as fh:
    for r in rows: fh.write(json.dumps(r) + '\n')
for r in rows: print(r[:4] if len(r) > 4 else r, r[4] if len(r) > 4 and r[3] else '')
