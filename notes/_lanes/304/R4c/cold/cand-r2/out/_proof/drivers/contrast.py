"""The pack's own state-contrast gate (knowledge/_validate_state_contrast.audit_page), driven per view.
The full-page --render run cannot finish inside one 180 s call, so each view is audited on its own page load."""
import os, sys, json, time
W = os.path.expanduser('~/cold/cand-r2'); URL = 'file://' + W + '/out/index.html'
sys.path.insert(0, W + '/pack/knowledge')
import _validate_state_contrast as SC
from playwright.sync_api import sync_playwright
views = sys.argv[1:]
res = {}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ['RENDER_SHELL'])
    for v in views:
        for theme in os.environ.get('THEMES', 'light dark').split():
            pg = b.new_page(viewport={'width': 1920, 'height': 1080})
            pg.goto(URL + '?theme=' + theme + '#/' + v); pg.wait_for_timeout(900)
            # harness only: the gate's "pressed" is a real click; block click ACTIONS (not :hover/:active) so the view under audit stays put
            pg.evaluate("() => document.addEventListener('click', e => { e.preventDefault(); e.stopImmediatePropagation(); }, true)")
            t0 = time.time(); sink = []
            SC.audit_page(pg, theme, sink)
            recs = [s[2] for s in sink]
            fails = [dict(state=s[1], **{k: s[2].get(k) for k in ('kind', 'where', 'ratio', 'need', 'fg', 'bg', 'text')}) for s in sink if s[2].get('kind') in ('text',)]
            icons = [s for s in sink if s[2].get('kind') == 'icon']
            still = pg.evaluate("() => document.querySelector('.app-view:not([hidden])').dataset.view")
            res['%s/%s' % (v, theme)] = {'view_after': still, 'secs': round(time.time() - t0, 1), 'records': len(sink), 'text_fails': fails[:12], 'n_text_fails': len(fails), 'icon_warn': len(icons), 'kinds': sorted(set(r.get('kind') for r in recs))}
            pg.close()
    b.close()
out = W + '/proof/contrast-%s.json' % '-'.join(views)
json.dump(res, open(out, 'w'), indent=1)
for k, r in res.items(): print(k, 'stayed on', r['view_after'], r['secs'], 's · text fails', r['n_text_fails'], '· icon warns', r['icon_warn'], '· kinds', r['kinds'], json.dumps(r['text_fails'][:3])[:400])
