#!/usr/bin/env python3
"""Lane OC (#280) — the orphan census page's gate + its one screenshot.

NEVER DRIVEN for the shot: a fresh context, light emulated, nothing clicked. A SECOND pass
drives the radios and the export to prove the envelope, in its own context, and its PNG is
not kept (99% disk).

  source knowledge/_render/seat_env.sh
  python3 notes/_lanes/280/orphan-census/shots.py
"""
import json, os
from playwright.sync_api import sync_playwright

REPO = os.environ.get('RENDER_REPO') or '/sessions/intelligent-serene-curie/mnt/UX-design'
HERE = os.path.join(REPO, 'notes/_lanes/280/orphan-census')
OUT = os.path.join(HERE, 'shots')
URL = 'file://' + os.path.join(HERE, 'ORPHANS-2026-09-17.html')
os.makedirs(OUT, exist_ok=True)

res = {}
with sync_playwright() as p:
    br = p.chromium.launch(args=['--no-sandbox', '--font-render-hinting=none'])

    # ---- pass 1: never driven, 1280 light
    for tag, w, h in [('1280-light', 1280, 900), ('390-light', 390, 844)]:
        ctx = br.new_context(viewport={'width': w, 'height': h}, color_scheme='light',
                             device_scale_factor=1)
        pg = ctx.new_page()
        errs, cons = [], []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.on('console', lambda m: cons.append(m.type + ': ' + m.text) if m.type == 'error' else None)
        pg.goto(URL, wait_until='load')
        pg.wait_for_timeout(500)
        probe = pg.evaluate("""() => ({
          hScroll: document.documentElement.scrollWidth > window.innerWidth + 1,
          scrollW: document.documentElement.scrollWidth, innerW: window.innerWidth,
          radios: document.querySelectorAll('input[type=radio]').length,
          groups: new Set([...document.querySelectorAll('input[type=radio]')].map(r=>r.name)).size,
          checked: document.querySelectorAll('input[type=radio]:checked').length,
          notes: document.querySelectorAll('.ask input[type=text]').length,
          blocks: document.querySelectorAll('section.dim').length,
          expHidden: document.getElementById('exp').hidden,
          ls: Object.keys(localStorage), headline: document.querySelector('.lede').innerText.trim()
        })""")
        if tag == '1280-light':
            pg.screenshot(path=os.path.join(OUT, 'orphans-1280-light-top.png'))
            pg.evaluate("window.scrollTo(0, document.querySelector('#ux-cloud').offsetTop - 40)")
            pg.wait_for_timeout(200)
            pg.screenshot(path=os.path.join(OUT, 'orphans-1280-light-set01.png'))
        res[tag] = dict(probe=probe, errors=errs, consoleErrors=cons)
        ctx.close()

    # ---- pass 2: driven — the envelope
    ctx = br.new_context(viewport={'width': 1280, 'height': 900}, color_scheme='light')
    pg = ctx.new_page()
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto(URL, wait_until='load')
    pg.evaluate("""() => {
      const names=[...new Set([...document.querySelectorAll('input[type=radio]')].map(r=>r.name))];
      names.forEach((n,i)=>{const rs=document.querySelectorAll('input[name="'+n+'"]');
        rs[i%rs.length].checked=true;});
      const t=document.querySelector('.ask input[type=text]'); t.value='driver note';
      document.dispatchEvent(new Event('change'));
    }""")
    pg.click('#cp')
    pg.wait_for_timeout(200)
    env = pg.evaluate("() => document.getElementById('exp').textContent")
    res['driven'] = dict(errors=errs, envelope=json.loads(env))
    ctx.close()
    br.close()

json.dump(res, open(os.path.join(OUT, 'shots.json'), 'w'), indent=1)
for k, v in res.items():
    print(k, 'errors', v['errors'], 'consoleErrors', v.get('consoleErrors'))
    if 'probe' in v:
        print('   ', json.dumps(v['probe'])[:400])
print('envelope keys', list(res['driven']['envelope']), 'answers',
      len(res['driven']['envelope']['answers']),
      'sample', json.dumps(list(res['driven']['envelope']['answers'].items())[:2]))
