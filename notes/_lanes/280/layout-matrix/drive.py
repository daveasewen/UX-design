#!/usr/bin/env python3
"""Lane LM (#280) — the DRIVEN gate, one pass per cell of the layout matrix.

Per cell: open it by URL flag, assert the cell's own driver (every node inside its band / on its
plate / on its shell), then DRIVE it — switch the Constitution chip on and off, dig a node, Escape,
scrub back and home, search "button" and fly to it, Escape — asserting the driver again after each
move and collecting page errors. Also drives the SWITCH itself: force → strata → shells → force in
both dimensions, and back to force-2D where every node must be at its `oy` again.

  source knowledge/_render/seat_env.sh
  python3 notes/_lanes/280/layout-matrix/drive.py [CELL ...]
"""
import json, os, sys
from playwright.sync_api import sync_playwright

REPO = os.environ.get('RENDER_REPO') or '/sessions/intelligent-serene-curie/mnt/UX-design'
OUT = os.path.join(REPO, 'notes/_lanes/280/layout-matrix/shots')
PAGE = 'file://' + os.path.join(REPO, 'notes/_KG-EXPLORER.html')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shots import PROBE, CELLS  # the same probe the screenshots use — one driver, never two

CHECK = "() => (" + PROBE + ")()"


def drive(pg, cell, log):
    l, d = cell
    def probe(tag):
        r = pg.evaluate(CHECK)
        log.append({'at': tag, 'layout': r['layout'], 'dim': r['dim'], 'outOfLayer': r['outOfLayer'],
                    'noLayer': r['noLayer'], 'worst': r['worst'], 'stats': r['stats']})
        return r
    probe('loaded')
    pg.evaluate("()=>{const c=[...document.querySelectorAll('.chip')].find(x=>x.dataset.fam==='governance');c.click()}")
    pg.wait_for_timeout(700); probe('constitution on')
    pg.evaluate("()=>{const c=[...document.querySelectorAll('.chip')].find(x=>x.dataset.fam==='governance');c.click()}")
    pg.wait_for_timeout(700); probe('constitution off')
    pg.evaluate("()=>{setFocus(byId.get('component:button'))}")
    pg.wait_for_timeout(900)
    r = probe('dug component:button')
    r['panel'] = pg.evaluate("()=>document.getElementById('panel').innerText.slice(0,90).replace(/\\s+/g,' ')")
    log[-1]['panel'] = r['panel']
    pg.keyboard.press('Escape'); pg.wait_for_timeout(900); probe('escaped')
    pg.evaluate("()=>setT(T-12)"); pg.wait_for_timeout(600)
    log.append({'at': 'scrubbed 12 days back', 'counts': pg.evaluate("()=>document.getElementById('scounts').innerText.replace(/\\s+/g,' ')")})
    pg.evaluate("()=>setT(SNAPS.length-1)"); pg.wait_for_timeout(600)
    log.append({'at': 'scrub home', 'counts': pg.evaluate("()=>document.getElementById('scounts').innerText.replace(/\\s+/g,' ')")})
    pg.fill('#q', 'button'); pg.wait_for_timeout(400)
    hits = pg.evaluate("()=>document.querySelectorAll('#hits .hit').length")
    pg.evaluate("()=>choose(0)"); pg.wait_for_timeout(1400)
    log.append({'at': 'searched+flew', 'hits': hits,
                'focus': pg.evaluate("()=>focus&&focus.id")})
    probe('after fly')
    pg.keyboard.press('Escape'); pg.wait_for_timeout(800)
    return probe('surfaced')


if __name__ == '__main__':
    want = [tuple(a.split('-')) for a in sys.argv[1:]] or CELLS
    kg = json.loads(open(os.path.join(REPO, 'notes/_KG-EXPLORER.html')).read()
                    .split('<script id="kg" type="application/json">')[1].split('</script>')[0]
                    .replace('<\\/script', '</script'))
    have = {'force': True, 'strata': bool(kg.get('bands')), 'shells': bool(kg.get('rings') or kg.get('shells'))}
    want = [c for c in want if have.get(c[0])]
    res = {}
    with sync_playwright() as p:
        br = p.chromium.launch(executable_path=os.environ['RENDER_SHELL'],
                               args=['--no-sandbox', '--force-device-scale-factor=1'])
        for cell in want:
            ctx = br.new_context(viewport={'width': 1280, 'height': 800}, color_scheme='light')
            pg = ctx.new_page(); errs = []
            pg.on('pageerror', lambda e: errs.append(str(e)))
            pg.on('console', lambda m: errs.append('console.' + m.type + ': ' + m.text) if m.type == 'error' else None)
            pg.goto(f"{PAGE}?layout={cell[0]}&dim={cell[1]}", wait_until='load'); pg.wait_for_timeout(1600)
            log = []
            drive(pg, cell, log)
            res['-'.join(cell)] = {'steps': log, 'errors': errs}
            bad = [s for s in log if s.get('outOfLayer') or s.get('noLayer')]
            print(f"{'-'.join(cell):12} steps={len(log)} out-of-layer steps={len(bad)} errors={len(errs)}"
                  + (f" {errs[:1]}" if errs else ''))
            ctx.close()
        # the SWITCH itself, in one context: every cell in turn, then home to force-2D
        ctx = br.new_context(viewport={'width': 1280, 'height': 800}, color_scheme='light')
        pg = ctx.new_page(); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.on('console', lambda m: errs.append('console.' + m.type + ': ' + m.text) if m.type == 'error' else None)
        pg.goto(PAGE, wait_until='load'); pg.wait_for_timeout(1600)
        walk = []
        for l, d in want:
            pg.evaluate(f"()=>{{setLayout('{l}');setDim({'true' if d=='3d' else 'false'})}}")
            pg.wait_for_timeout(900)
            r = pg.evaluate(CHECK)
            walk.append({'cell': f'{l}-{d}', 'buttons': r['buttons'], 'outOfLayer': r['outOfLayer'],
                         'noLayer': r['noLayer'], 'k': r['view']['k']})
        pg.evaluate("()=>{setLayout('force');setDim(false)}"); pg.wait_for_timeout(900)
        home = pg.evaluate("()=>{let m=0;for(const n of NODES){m=Math.max(m,Math.abs(n.x-n.ox),Math.abs(n.y-n.oy))}return +m.toFixed(3)}")
        walk.append({'cell': 'home force-2d', 'maxOffsetFromForce': home})
        res['switch-walk'] = {'steps': walk, 'errors': errs}
        print('switch walk:', json.dumps(walk))
        print('switch walk errors:', errs)
        ctx.close(); br.close()
    fp = os.path.join(OUT, 'drive.json')
    old = json.load(open(fp)) if os.path.exists(fp) else {}
    old.update(res); json.dump(old, open(fp, 'w'), indent=1)
