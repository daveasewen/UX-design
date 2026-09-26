import os, sys, json
from playwright.sync_api import sync_playwright
W = os.path.expanduser('~/cold/v1013-r3/out')
URL = lambda n, q='': 'file://' + W + '/' + n + '.html' + q
LOG = []
def ok(name, cond, detail=''):
    LOG.append(('PASS' if cond else 'FAIL', name, str(detail)[:160])); print(('PASS ' if cond else 'FAIL ') + name + ('  — ' + str(detail)[:160] if detail else ''))
def start(p):
    b = p.chromium.launch(executable_path=os.environ['RENDER_SHELL'])
    ctx = b.new_context(viewport={'width': 1440, 'height': 900}, accept_downloads=True)
    errs = []
    def attach(pg):
        pg.on('pageerror', lambda e: errs.append('PAGEERROR ' + str(e)[:200]))
        pg.on('console', lambda m: errs.append('CONSOLE ' + m.text[:200]) if m.type == 'error' else None)
    ctx.on('page', attach)
    return b, ctx, errs
def pick(pg, dd, value):
    pg.click('#' + dd + 'T'); pg.wait_for_timeout(150)
    pg.click('#' + dd + 'M [data-value="' + value + '"]'); pg.wait_for_timeout(350)
def save(name):
    out = os.path.expanduser('~/cold/v1013-r3/proof/drive-' + name + '.json'); json.dump(LOG, open(out, 'w'), indent=0)
    print('== %s: %d pass, %d fail' % (name, sum(1 for l in LOG if l[0] == 'PASS'), sum(1 for l in LOG if l[0] == 'FAIL')))
