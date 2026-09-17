#!/usr/bin/env python3
"""#281 lane CM — the chip map's screenshots and its canvas-identity probe.

NEVER DRIVEN: a fresh browser.new_context per shot, the colour scheme emulated, the cell chosen by
URL flag (`?layout=…&dim=…`) and never by a click, and `Object.keys(localStorage)` + page errors
recorded for each one. The page is SERVED (s280-D2: a file:// explorer cannot read the artefacts it
exists to open), by `knowledge/_serve_explorer.py`, started by this script and stopped by it.

  source knowledge/_render/seat_env.sh
  python3 notes/_lanes/281/chip-map/shots.py <before.html under the repo> <after path under repo>

Both pages are served out of the same read-only root so the only variable is the page. Each shot
records the CANVAS md5 (`#cv`.toDataURL), which is what "the default canvas changed" means, plus the
header strip, the legend summary, the count of drawn edges by family and the held row's own text.
"""
import json, os, sys, time, hashlib, subprocess, urllib.request
from playwright.sync_api import sync_playwright

REPO = os.environ.get('RENDER_REPO') or os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..'))
OUT = os.path.join(REPO, 'notes/_lanes/281/chip-map/shots')
os.makedirs(OUT, exist_ok=True)

CELLS = [('force', '2d'), ('force', '3d'), ('strata', '2d'), ('strata', '3d'),
         ('shells', '2d'), ('shells', '3d')]

PROBE = """() => {
  const g = document.getElementById('cv');
  const fam = {};
  for (const e of EDGES) {
    if (!e.t || !alive(e)) continue;
    const s = byId.get(e.s), t = byId.get(e.t);
    if (!s || !t || !NODEON(s) || !NODEON(t) || !EON(e)) continue;
    const f = FAMILY[e.type] || '(none)';
    fam[f] = (fam[f] || 0) + 1;
  }
  const held = document.querySelector('.legend .held');
  return {
    version: KG.version,
    stats: document.getElementById('stats').innerText.replace(/\\s+/g, ' ').trim(),
    lsum: (document.querySelector('.legend .lsum') || {}).innerText || '',
    heldRow: held ? held.innerText.replace(/\\s+/g, ' ').trim() : null,
    heldEdges: EDGES.filter(e => e.held).length,
    drawnByFam: fam,
    drawnTotal: Object.values(fam).reduce((a, b) => a + b, 0),
    homeless: [...new Set(EDGES.map(e => e.type))].filter(t => !(t in FAMILY)),
    canvas: g.width + 'x' + g.height,
    md5src: g.toDataURL('image/png'),
    ls: Object.keys(localStorage)
  };
}"""


def serve():
    p = subprocess.Popen([sys.executable, '-u', os.path.join(REPO, 'knowledge/_serve_explorer.py')],
                         cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    url = None
    t0 = time.time()
    while time.time() - t0 < 25:
        line = p.stdout.readline()
        if not line:
            break
        sys.stdout.write('  serve| ' + line)
        if 'http://127.0.0.1:' in line:
            url = 'http://127.0.0.1:' + line.split('http://127.0.0.1:')[1].split('/')[0].strip()
            break
    if not url:
        p.kill()
        raise SystemExit('_serve_explorer.py printed no URL')
    for _ in range(40):
        try:
            urllib.request.urlopen(url + '/notes/', timeout=1).read(1)
            break
        except Exception:
            time.sleep(0.25)
    return p, url


def run(base, pages, width=1280, height=800):
    res = {}
    with sync_playwright() as pw:
        br = pw.chromium.launch(executable_path=os.environ['RENDER_SHELL'],
                                args=['--no-sandbox', '--force-device-scale-factor=1'])
        for name, rel, qs in pages:
            ctx = br.new_context(viewport={'width': width, 'height': height},
                                 color_scheme='light', device_scale_factor=1)
            pg = ctx.new_page()
            errs = []
            pg.on('pageerror', lambda e: errs.append(str(e)))
            pg.on('console', lambda m: errs.append('console.' + m.type + ': ' + m.text) if m.type == 'error' else None)
            pg.goto(base + '/' + rel + qs, wait_until='load')
            pg.wait_for_timeout(2200)
            d = pg.evaluate(PROBE)
            d['canvasMd5'] = hashlib.md5(d.pop('md5src').encode()).hexdigest()
            d['errors'] = errs
            d['url'] = rel + qs
            d['viewport'] = f'{width}x{height} light'
            shot = os.path.join(OUT, name + '.png')
            pg.screenshot(path=shot)
            d['bytes'] = os.path.getsize(shot)
            res[name] = d
            print(f"{name:34} v{d['version']:5} canvas={d['canvasMd5'][:12]} drawn={d['drawnTotal']:<6} "
                  f"held={d['heldEdges']} homeless={d['homeless']} errors={len(errs)} ls={d['ls']} {d['bytes']:,}B")
            ctx.close()
        br.close()
    return res


if __name__ == '__main__':
    before_rel, after_rel = sys.argv[1], sys.argv[2]
    srv, base = serve()
    try:
        pages = []
        for l, d in CELLS:
            qs = f'?layout={l}&dim={d}'
            pages.append((f'cm-before-{l}-{d}-1280-light', before_rel, qs))
            pages.append((f'cm-after-{l}-{d}-1280-light', after_rel, qs))
        res = run(base, pages)
    finally:
        srv.terminate()
        try:
            srv.wait(timeout=5)
        except Exception:
            srv.kill()
    json.dump(res, open(os.path.join(OUT, 'shots.json'), 'w'), indent=1)
    print('\nCANVAS md5, before → after, per cell:')
    for l, d in CELLS:
        a = res[f'cm-before-{l}-{d}-1280-light']['canvasMd5']
        b = res[f'cm-after-{l}-{d}-1280-light']['canvasMd5']
        print(f"  {l}-{d:<3} {a[:16]} → {b[:16]}  {'SAME' if a == b else 'CHANGED'}")
    print('errors, every shot:', {k: v['errors'] for k, v in res.items() if v['errors']} or '[] everywhere')
    print('localStorage, every shot:', {k: v['ls'] for k, v in res.items() if v['ls']} or 'empty everywhere')
