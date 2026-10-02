#!/usr/bin/env python3
"""Render the key-frame stills of both cuts at the seat (export mode, 1920x1080), plus a timing probe."""
import json, os, sys, time
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
cuts = sys.argv[1:] or ['a', 'b']
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ['RENDER_SHELL'])
    pg = b.new_page(viewport={'width': 1920, 'height': 1080})
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    for cut in cuts:
        pg.goto('file://' + os.path.join(HERE, f'button-film-{cut}.html') + '?export=1')
        pg.wait_for_function('window.__anim', timeout=20000)
        info = pg.evaluate('({d: window.__anim.duration, f: window.__anim.fontOk, keys: window.__anim.keys})')
        d = os.path.join(HERE, f'stills-{cut}')
        os.makedirs(d, exist_ok=True)
        t0 = time.time()
        for i, k in enumerate(info['keys']):
            pg.evaluate(f"window.__anim.renderAt({k['t']})")
            pg.screenshot(path=os.path.join(d, f'{i:02d}.png'))
            k['file'] = f'stills-{cut}/{i:02d}.png'
        # frame cost probe: 60 renders across the film
        ms = pg.evaluate("(()=>{const a=window.__anim;let s=performance.now();for(let i=0;i<60;i++)a.renderAt(a.duration*i/60);return (performance.now()-s)/60})()")
        json.dump({'duration': info['d'], 'fontOk': info['f'], 'ms_per_frame': ms, 'keys': info['keys']},
                  open(os.path.join(d, 'keys.json'), 'w'), indent=1)
        print(cut, 'duration', round(info['d'], 2), 's · font', info['f'], '· stills', len(info['keys']),
              '· %.1f ms/frame' % ms, '· %.1fs' % (time.time() - t0))
    print('page errors:', errs or 0)
    b.close()
