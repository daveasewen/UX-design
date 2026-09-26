"""Driven browser proof for the CEO prototype. Usage: python3 drive.py <section> [width]
Each section loads the page fresh (with an empty localStorage unless it is a persistence leg),
works real controls through Playwright, and records what changed. Console errors are collected
for every section."""
import os, json, sys, time
from playwright.sync_api import sync_playwright
W = os.path.expanduser('~/cold/cand-r3'); URL = 'file://' + W + '/out/index.html'
sec = sys.argv[1]; width = int(sys.argv[2]) if len(sys.argv) > 2 else 1440
R = {'section': sec, 'width': width, 'checks': [], 'errors': []}
def check(name, ok, detail=None):
    R['checks'].append({'check': name, 'ok': bool(ok), 'detail': detail}); print(('PASS ' if ok else 'FAIL ') + name + ('' if detail is None else '  :: ' + str(detail)[:300]))
def ev(pg, js, arg=None): return pg.evaluate(js, arg) if arg is not None else pg.evaluate(js)
def txt(pg, sel): return pg.locator(sel).first.inner_text()

with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ['RENDER_SHELL'])
    ctx = b.new_context(viewport={'width': width, 'height': 900}, accept_downloads=True)
    pg = ctx.new_page()
    pg.on('console', lambda m: R['errors'].append(['console.' + m.type, m.text]) if m.type in ('error', 'warning') else None)
    pg.on('pageerror', lambda e: R['errors'].append(['pageerror', str(e)]))
    pg.goto(URL + '#/overview'); pg.wait_for_timeout(1200)
    ev(pg, "() => { localStorage.clear(); }"); pg.goto(URL + '#/overview'); pg.reload(); pg.wait_for_timeout(1400)
    exec(open(W + '/tools/drive_%s.py' % sec).read())
    check('zero console errors or page errors during this section', len(R['errors']) == 0, R['errors'][:5])
    json.dump(R, open(W + '/proof/drive-%s-%d.json' % (sec, width), 'w'), indent=1)
    b.close()
