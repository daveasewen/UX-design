#!/usr/bin/env python3
"""#281 lane PH — the principles-home screenshots and the canvas-identity probe.

Lane CM's `notes/_lanes/281/chip-map/shots.py` with one difference: this lane cannot serve TWO
pages at once (the seat refuses `unlink` under the mount, so a scratch copy of HEAD's page would
have to be committed to be removed), so the two halves are taken as two RUNS of the same script
against the one served page — once before the rebuild, once after — and the tag is an argument.

NEVER DRIVEN: a fresh browser.new_context per shot, the colour scheme emulated, the cell and the
family chips chosen by URL flag (`?layout=…&dim=…&fam=…`), never by a click. `Object.keys(localStorage)`
and page errors are recorded for each shot. The page is SERVED (s280-D2), by
`knowledge/_serve_explorer.py`, started and stopped by this script.

  source knowledge/_render/seat_env.sh
  python3 notes/_lanes/281/principles-home/shots.py before|after
"""
import json, os, sys, time, hashlib, subprocess, urllib.request
from playwright.sync_api import sync_playwright

REPO = os.environ.get('RENDER_REPO') or os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..'))
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'shots')
os.makedirs(OUT, exist_ok=True)

PROBE = """() => {
  const g = document.getElementById('cv');
  const fam = {}, typ = {};
  for (const e of EDGES) {
    if (!e.t || !alive(e)) continue;
    const s = byId.get(e.s), t = byId.get(e.t);
    if (!s || !t || !NODEON(s) || !NODEON(t) || !EON(e)) continue;
    const f = (e.fam || FAMILY[e.type]) || '(none)';
    fam[f] = (fam[f] || 0) + 1;
    typ[e.type] = (typ[e.type] || 0) + 1;
  }
  const dark = {};
  const deg = new Map(NODES.map(n => [n.id, 0]));
  for (const e of EDGES) {
    if (!e.t || !alive(e)) continue;
    const s = byId.get(e.s), t = byId.get(e.t);
    if (!s || !t || !NODEON(s) || !NODEON(t) || !EON(e)) continue;
    deg.set(e.s, deg.get(e.s) + 1); deg.set(e.t, deg.get(e.t) + 1);
  }
  for (const n of NODES) { if (!alive(n) || !famOK(n)) continue;
    if (deg.get(n.id) === 0) dark[n.type] = (dark[n.type] || 0) + 1; }
  return {
    version: KG.version,
    stats: document.getElementById('stats').innerText.replace(/\\s+/g, ' ').trim(),
    typeChips: ALLTYPES,
    famOn: Object.fromEntries(Object.entries(famOn)),
    drawnByFam: fam, drawnByType: typ,
    drawnTotal: Object.values(fam).reduce((a, b) => a + b, 0),
    darkByType: dark,
    homeless: [...new Set(EDGES.map(e => e.type))].filter(t => !(t in FAMILY)),
    canvas: g.width + 'x' + g.height,
    md5src: g.toDataURL('image/png'),
    ls: Object.keys(localStorage)
  };
}"""

CELLS = [('default', '?layout=force&dim=2d'),
         ('uxchip', '?layout=force&dim=2d&fam=uxprinciples'),
         ('allchips', '?layout=force&dim=2d&fam=uxprinciples,guidelines,guidelinerules,assets,governance')]


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
        p.kill(); raise SystemExit('_serve_explorer.py printed no URL')
    for _ in range(40):
        try:
            urllib.request.urlopen(url + '/notes/', timeout=1).read(1); break
        except Exception:
            time.sleep(0.25)
    return p, url


if __name__ == '__main__':
    tag = sys.argv[1]
    rel = 'notes/_KG-EXPLORER.html'
    srv, base = serve()
    res = {}
    try:
        with sync_playwright() as pw:
            br = pw.chromium.launch(executable_path=os.environ['RENDER_SHELL'],
                                    args=['--no-sandbox', '--force-device-scale-factor=1'])
            for name, qs in CELLS:
                ctx = br.new_context(viewport={'width': 1280, 'height': 800},
                                     color_scheme='light', device_scale_factor=1)
                pg = ctx.new_page()
                errs = []
                pg.on('pageerror', lambda e: errs.append(str(e)))
                pg.on('console', lambda m: errs.append('console.' + m.type + ': ' + m.text) if m.type == 'error' else None)
                pg.goto(base + '/' + rel + qs, wait_until='load')
                pg.wait_for_timeout(2400)
                d = pg.evaluate(PROBE)
                d['canvasMd5'] = hashlib.md5(d.pop('md5src').encode()).hexdigest()
                d['errors'] = errs
                d['url'] = rel + qs
                d['viewport'] = '1280x800 light'
                shot = os.path.join(OUT, f'ph-{tag}-{name}-force-2d-1280-light.png')
                pg.screenshot(path=shot)
                d['bytes'] = os.path.getsize(shot)
                res[name] = d
                print(f"{tag}/{name:9} v{d['version']:6} canvas={d['canvasMd5'][:12]} drawn={d['drawnTotal']:<6} "
                      f"dark={sum(d['darkByType'].values()):<4} errors={len(errs)} ls={d['ls']} {d['bytes']:,}B")
                print(f"    stats: {d['stats']}")
                ctx.close()
            br.close()
    finally:
        srv.terminate()
        try: srv.wait(timeout=5)
        except Exception: srv.kill()
    json.dump(res, open(os.path.join(OUT, f'shots-{tag}.json'), 'w'), indent=1)
    print('errors:', {k: v['errors'] for k, v in res.items() if v['errors']} or '[] everywhere')
