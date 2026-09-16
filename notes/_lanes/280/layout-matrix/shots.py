#!/usr/bin/env python3
"""Lane LM (#280) — the LAYOUT MATRIX's screenshots and its per-cell driver check.

Every shot is NEVER DRIVEN: a fresh browser.new_context per shot, the colour scheme emulated, the
cell selected by URL flag (`?layout=<force|strata|shells>&dim=<2d|3d>`) rather than by a click, and
`Object.keys(localStorage)` + page errors recorded for each one. The probe also answers the cell's
OWN driver: is every node inside its band / on its plate / on its shell.

  source knowledge/_render/seat_env.sh
  python3 notes/_lanes/280/layout-matrix/shots.py [CELL ...]      # default: every cell the file carries
  CONTROL=<path to the 1.17 page> ... adds the force-2D identity control
"""
import json, os, sys, hashlib
from playwright.sync_api import sync_playwright

REPO = os.environ.get('RENDER_REPO') or '/sessions/intelligent-serene-curie/mnt/UX-design'
OUT = os.path.join(REPO, 'notes/_lanes/280/layout-matrix/shots')
PAGE = 'file://' + os.path.join(REPO, 'notes/_KG-EXPLORER.html')
CONTROL = os.environ.get('CONTROL')
os.makedirs(OUT, exist_ok=True)

CELLS = [('force', '2d'), ('force', '3d'), ('strata', '2d'), ('strata', '3d'),
         ('shells', '2d'), ('shells', '3d')]

PROBE = """() => {
  const LY = (typeof LAYOUT === 'undefined') ? 'force' : LAYOUT;
  const D3 = (typeof three === 'undefined') ? false : three;
  const bands = KG.bands || [], plates = KG.plates || [], rings = KG.rings || [], shells = KG.shells || [];
  const byB = Object.fromEntries(bands.map(b => [b.id, b]));
  const byP = Object.fromEntries(plates.map(p => [p.id, p]));
  const byR = Object.fromEntries(rings.map(r => [r.id, r]));
  const byS = Object.fromEntries(shells.map(s => [s.id, s]));
  const TOL = 1.0;                        // world units; every placement is baked and rounded to 0.1
  let out = 0, noLayer = 0, worst = 0;
  for (const n of NODES) {
    // the node's RESTING place in the live cell, read the same way the canvas reads it
    const b = (typeof base === 'function') ? base(n) : [n.ox, n.oy, 0];
    const x = b[0], y = b[1], z = b[2] || 0;
    if (LY === 'force') continue;
    if (LY === 'strata' && !D3) { const g = byB[n.view]; if (!g) { noLayer++; continue; }
      const d = Math.max(g.y0 - y, y - g.y1); worst = Math.max(worst, d); if (d > TOL) out++; }
    else if (LY === 'strata' && D3) { const g = byP[n.view]; if (!g) { noLayer++; continue; }
      const d = Math.max(Math.abs(y - g.y), Math.abs(x - g.cx) - g.half, Math.abs(z) - g.half);
      worst = Math.max(worst, d); if (d > TOL) out++; }
    else if (LY === 'shells' && !D3) { const g = byR[n.view]; if (!g) { noLayer++; continue; }
      const r = Math.hypot(x, y); let a = Math.atan2(y, x); if (a < g.a0) a += 2 * Math.PI;
      const d = Math.max(g.r0 - r, r - g.r1, g.a0 - a, a - g.a1);
      worst = Math.max(worst, d); if (d > TOL) out++; }
    else if (LY === 'shells' && D3) { const g = byS[n.view]; if (!g) { noLayer++; continue; }
      const d = (g.plinthY != null) ? Math.max(Math.abs(y - g.plinthY), Math.hypot(x, z) - g.r)
                                    : Math.abs(Math.hypot(x, y, z) - g.r);
      worst = Math.max(worst, d); if (d > TOL) out++; }
  }
  const g = document.getElementById('cv');
  return {
    layout: LY, dim: D3 ? '3d' : '2d', outOfLayer: out, noLayer, worst: +worst.toFixed(2),
    nodes: NODES.length,
    view: {k: +view.k.toFixed(4), x: Math.round(view.x), y: Math.round(view.y)},
    stats: document.getElementById('stats').innerText.replace(/\\s+/g, ' ').trim(),
    buttons: [(document.getElementById('layout')||{}).textContent,
              (document.getElementById('three')||{}).textContent].join(' · '),
    canvas: g.width + 'x' + g.height, md5src: g.toDataURL('image/png'),
    ls: Object.keys(localStorage)
  };
}"""


def run(shots, width=1280, height=800, tag=''):
    res = {}
    with sync_playwright() as p:
        br = p.chromium.launch(executable_path=os.environ['RENDER_SHELL'],
                               args=['--no-sandbox', '--force-device-scale-factor=1'])
        for name, url, qs, scheme in shots:
            ctx = br.new_context(viewport={'width': width, 'height': height},
                                 color_scheme=scheme, device_scale_factor=1)
            pg = ctx.new_page()
            errs = []
            pg.on('pageerror', lambda e: errs.append(str(e)))
            pg.on('console', lambda m: errs.append('console.' + m.type + ': ' + m.text) if m.type == 'error' else None)
            pg.goto(url + qs, wait_until='load')
            pg.wait_for_timeout(1800)
            d = pg.evaluate(PROBE)
            d['canvasMd5'] = hashlib.md5(d.pop('md5src').encode()).hexdigest()
            d['errors'] = errs; d['url'] = qs or '(no flags)'; d['scheme'] = scheme
            d['viewport'] = f'{width}x{height}'
            pg.screenshot(path=os.path.join(OUT, name + '.png'))
            d['bytes'] = os.path.getsize(os.path.join(OUT, name + '.png'))
            res[name] = d
            print(f"{name:34} {d['layout']:6} {d['dim']}  outOfLayer={d['outOfLayer']:<4} worst={d['worst']:<8} "
                  f"k={d['view']['k']:<8} errors={len(errs)} ls={d['ls']} md5={d['canvasMd5'][:10]} {d['bytes']:,}B")
            ctx.close()
        br.close()
    return res


if __name__ == '__main__':
    want = [tuple(a.split('-')) for a in sys.argv[1:]] or CELLS
    kg = json.loads(open(os.path.join(REPO, 'notes/_KG-EXPLORER.html')).read()
                    .split('<script id="kg" type="application/json">')[1].split('</script>')[0]
                    .replace('<\\/script', '</script'))
    have = {'force': True, 'strata': bool(kg.get('bands')), 'shells': bool(kg.get('rings') or kg.get('shells'))}
    want = [c for c in want if have.get(c[0])]
    shots = [(f"kg-118-{l}-{d}-{s}", PAGE, f"?layout={l}&dim={d}", s)
             for (l, d) in want for s in ('light', 'dark')]
    if CONTROL:
        shots = [('kg-117-control-force-2d-light', 'file://' + CONTROL, '', 'light')] + shots
    res = run(shots)
    small = [(f"kg-118-{l}-{d}-390-light", PAGE, f"?layout={l}&dim={d}", 'light') for (l, d) in want if d == '2d']
    res.update(run(small, width=390, height=844))
    old = {}
    fp = os.path.join(OUT, 'shots.json')
    if os.path.exists(fp): old = json.load(open(fp))
    old.update(res)
    json.dump(old, open(fp, 'w'), indent=1)
    if CONTROL:
        a = res['kg-117-control-force-2d-light']['canvasMd5']; b = res['kg-118-force-2d-light']['canvasMd5']
        print('\nCANVAS IDENTITY 1.17-control vs 1.18 force-2D (light, page defaults):',
              'SAME' if a == b else f'DIFF {a[:10]} {b[:10]}')
    print('out-of-layer nodes, every cell:', {k: v['outOfLayer'] for k, v in res.items()})
