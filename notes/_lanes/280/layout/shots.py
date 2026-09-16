#!/usr/bin/env python3
"""Lane LY (#280) — the strata option's screenshots and its two drivers.

Every shot is NEVER DRIVEN: a fresh browser.new_context per shot, the colour scheme emulated, the
layer selected by URL flag (`?layout=strata`, `?fam=assets,governance`) rather than by a click, and
`Object.keys(localStorage)` and `page errors` recorded for each context.

  source knowledge/_render/seat_env.sh
  python3 notes/_lanes/280/layout/shots.py
"""
import json, os, sys, hashlib
from playwright.sync_api import sync_playwright

REPO = os.environ.get('RENDER_REPO') or '/sessions/intelligent-serene-curie/mnt/UX-design'
OUT = os.path.join(REPO, 'notes/_lanes/280/layout/shots')
V117 = 'file://' + os.path.join(REPO, 'notes/_KG-EXPLORER.html')
# argv[1] is the 1.16 CONTROL page: HEAD's builder, run against TODAY's data with only its ROOT
# redirected (see REPORT.md section 3). It is scratch and is not committed — rebuild it before a re-run.
V116 = 'file://' + (sys.argv[1] if len(sys.argv) > 1 else os.path.join(REPO, 'notes/_KG-EXPLORER.html'))
os.makedirs(OUT, exist_ok=True)

SHOTS = [
    ('kg-116-force-light',            V116, '',                                  'light'),
    ('kg-116-force-dark',             V116, '',                                  'dark'),
    ('kg-117-strata-light',           V117, '?layout=strata',                    'light'),
    ('kg-117-strata-dark',            V117, '?layout=strata',                    'dark'),
    ('kg-117-strata-assets-light',    V117, '?layout=strata&fam=assets',         'light'),
    ('kg-117-strata-assets-dark',     V117, '?layout=strata&fam=assets',         'dark'),
    ('kg-117-strata-const-light',     V117, '?layout=strata&fam=governance',     'light'),
    ('kg-117-strata-const-dark',      V117, '?layout=strata&fam=governance',     'dark'),
    ('kg-117-strata-all-light',       V117, '?layout=strata&fam=governance,guidelines,guidelinerules,uxprinciples,assets', 'light'),
    ('kg-117-force-light',            V117, '',                                  'light'),
]

PROBE = """() => {
  // the 1.16 control page knows neither LAYOUT nor the bands — it answers `force` and nothing else
  const LY = (typeof LAYOUT === 'undefined') ? 'force' : LAYOUT;
  const bands = KG.bands || [];
  const by = Object.fromEntries(bands.map(b => [b.id, b]));
  let out = 0, min = {}, max = {};
  for (const n of NODES) {
    const b = by[n.view];
    if (!b) { if (LY === 'strata') out++; continue; }
    const y = LY === 'strata' ? n.y : n.oy;           // the LIVE y the canvas is drawing
    if (LY === 'strata' && (y < b.y0 || y > b.y1 || y !== n.oy2)) out++;
    min[n.view] = Math.min(min[n.view] ?? 1e9, y); max[n.view] = Math.max(max[n.view] ?? -1e9, y);
  }
  const g = document.getElementById('cv');
  return {
    layout: LY, outOfBand: out, nodes: NODES.length, bands, min, max,
    view: {k: +view.k.toFixed(4), x: Math.round(view.x), y: Math.round(view.y)},
    stats: document.getElementById('stats').innerText.replace(/\\s+/g, ' ').trim(),
    button: (document.getElementById('layout')||{}).textContent || '(none — 1.16)',
    canvas: g.width + 'x' + g.height,
    md5src: g.toDataURL('image/png'),
    ls: Object.keys(localStorage)
  };
}"""

res = {}
with sync_playwright() as p:
    br = p.chromium.launch(executable_path=os.environ['RENDER_SHELL'],
                           args=['--no-sandbox', '--force-device-scale-factor=1'])
    for name, url, qs, scheme in SHOTS:
        ctx = br.new_context(viewport={'width': 1280, 'height': 800},
                             color_scheme=scheme, device_scale_factor=1)
        pg = ctx.new_page()
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.on('console', lambda m: errs.append('console.' + m.type + ': ' + m.text) if m.type == 'error' else None)
        pg.goto(url + qs, wait_until='load')
        pg.wait_for_timeout(1600)
        d = pg.evaluate(PROBE)
        d['canvasMd5'] = hashlib.md5(d.pop('md5src').encode()).hexdigest()
        d['errors'] = errs
        d['url'] = qs or '(no flags)'
        d['scheme'] = scheme
        pg.screenshot(path=os.path.join(OUT, name + '.png'))
        d['bytes'] = os.path.getsize(os.path.join(OUT, name + '.png'))
        res[name] = d
        print(f"{name:32} layout={d['layout']:7} outOfBand={d['outOfBand']:<4} k={d['view']['k']:<8} "
              f"errors={len(errs)} ls={d['ls']} md5={d['canvasMd5'][:10]} {d['bytes']:,}B")
        ctx.close()
    br.close()
json.dump(res, open(os.path.join(OUT, 'shots.json'), 'w'), indent=1)
print('\nCANVAS IDENTITY 1.16 vs 1.17-in-force (light, page defaults):',
      'SAME' if res['kg-116-force-light']['canvasMd5'] == res['kg-117-force-light']['canvasMd5'] else 'DIFF')
print('out-of-band nodes, every strata context:',
      {k: v['outOfBand'] for k, v in res.items() if v['layout'] == 'strata'})
