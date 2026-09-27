"""k3themes.py <dirA> <dirB> <page>... — V5's K3 measure (text-element box HEIGHT and WIDTH, >1px) before v after,
4 apollo themes x light/dark, 1440, reduced motion. Lists every non-chart element that moved."""
import os, sys, collections
from playwright.sync_api import sync_playwright
JS = """() => [...document.body.querySelectorAll('*')].filter(e => [...e.childNodes].some(n => n.nodeType===3 && n.textContent.trim())).map(e => { const r = e.getBoundingClientRect(); let s = e.closest('[class*="cn-"]');
  const sc = s ? [...s.classList].find(c => c.startsWith('cn-')) : '-'; return [sc, e.tagName.toLowerCase() + '.' + ((e.getAttribute('class')||'').split(' ')[0]), Math.round(r.height*10)/10, Math.round(r.width*10)/10, (e.textContent||'').trim().slice(0,24)]; })"""
A, B = sys.argv[1:3]
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ.get("RENDER_SHELL"))
    for name in sys.argv[3:]:
        for th in ("mono", "common", "console", "supercharge"):
            for m in ("light", "dark"):
                res = []
                for d in (A, B):
                    pg = b.new_page(viewport={"width": 1440, "height": 900}, reduced_motion="reduce"); pg.goto("file://" + os.path.abspath(os.path.join(d, name))); pg.wait_for_timeout(500)
                    pg.evaluate("([a,t])=>{document.documentElement.setAttribute('data-apollo-theme',a);document.documentElement.setAttribute('data-theme',t);document.querySelectorAll('[data-theme]').forEach(e=>e.setAttribute('data-theme',t));}", [th, m]); pg.wait_for_timeout(400)
                    res.append(pg.evaluate(JS)); pg.close()
                X, Y = res
                if len(X) != len(Y): print(name, th, m, "DOM differs", len(X), len(Y)); continue
                c = collections.Counter()
                for x, y in zip(X, Y):
                    if (abs(x[2]-y[2]) > 1.0 or abs(x[3]-y[3]) > 1.0) and not x[0].startswith("cn-chart"):
                        c["%s %s h%s->%s w%s->%s %r" % (x[0], x[1], x[2], y[2], x[3], y[3], x[4])] += 1
                print(name, th, m, len(X), "non-chart moved:", sum(c.values()), c.most_common(6))
    b.close()
