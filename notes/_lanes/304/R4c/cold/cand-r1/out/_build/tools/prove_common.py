import os, json, time
from playwright.sync_api import sync_playwright
W=os.path.expanduser('~/cold/cand-r1'); URL='file://'+W+'/out/index.html'
class Run:
    def __init__(s, name): s.name=name; s.checks=[]; s.logs=[]
    def check(s, label, ok, detail=None):
        s.checks.append({'check':label,'pass':bool(ok),'detail':detail}); print(('PASS ' if ok else 'FAIL ')+label+(' — '+json.dumps(detail)[:220] if detail is not None else ''))
    def attach(s, pg):
        pg.on('console', lambda m: s.logs.append((m.type, m.text)) if m.type in ('error','warning') else None)
        pg.on('pageerror', lambda e: s.logs.append(('pageerror', str(e))))
    def save(s):
        s.check('zero console errors or uncaught exceptions across the whole run', not s.logs, s.logs[:5])
        json.dump({'run':s.name,'checks':s.checks,'console':s.logs}, open(W+'/out/proof/driven-'+s.name+'.json','w'), indent=1)
        print('SUMMARY', s.name, sum(c['pass'] for c in s.checks), '/', len(s.checks))
