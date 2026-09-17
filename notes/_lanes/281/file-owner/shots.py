#!/usr/bin/env python3
"""#281 lane FO — the file-owner screenshots, the drawn/dark probe, and the INSPECT record of a
tied node.

Lane PH's `notes/_lanes/281/principles-home/shots.py` with two differences: the cells are the ones
this lane's proof needs (defaults · the HSBC rule chip alone · every chip on · every chip on +
Constitution), and a FOURTH pass DRIVES `openInspect` on a re-homed guideline file so the declared
tie can be read in the modal.

NEVER DRIVEN for the three cells: a fresh browser.new_context per shot, the colour scheme emulated,
the chips chosen by URL flag (`?layout=…&dim=…&fam=…`), never by a click. `Object.keys(localStorage)`
and page errors are recorded for each shot. The page is SERVED (s280-D2), by
`knowledge/_serve_explorer.py`, started and stopped by this script.

  source knowledge/_render/seat_env.sh
  python3 notes/_lanes/281/file-owner/shots.py after
"""
import json, os, sys, time, hashlib, subprocess, urllib.request
from playwright.sync_api import sync_playwright

REPO = os.environ.get('RENDER_REPO') or os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..'))
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'shots')
os.makedirs(OUT, exist_ok=True)

TIED = 'artefact:knowledge/guidelines/data-visualisation.md'

PROBE = """() => {
  const fam = {}, typ = {};
  const deg = new Map(NODES.map(n => [n.id, 0]));
  for (const e of EDGES) {
    if (!e.t || !alive(e)) continue;
    const s = byId.get(e.s), t = byId.get(e.t);
    if (!s || !t || !NODEON(s) || !NODEON(t) || !EON(e)) continue;
    const f = (e.fam || FAMILY[e.type]) || '(none)';
    fam[f] = (fam[f] || 0) + 1; typ[e.type] = (typ[e.type] || 0) + 1;
    deg.set(e.s, deg.get(e.s) + 1); deg.set(e.t, deg.get(e.t) + 1);
  }
  const dark = {};
  for (const n of NODES) { if (!alive(n) || !famOK(n)) continue;
    if (deg.get(n.id) === 0) dark[n.type] = (dark[n.type] || 0) + 1; }
  const g = document.getElementById('cv');
  const tied = NODES.filter(n => n.claimedBy).map(n => n.id);
  return {
    version: KG.version,
    stats: document.getElementById('stats').innerText.replace(/\\s+/g, ' ').trim(),
    famOn: Object.fromEntries(Object.entries(famOn)),
    drawnByFam: fam, definedIn: typ.definedIn || 0,
    drawnTotal: Object.values(fam).reduce((a, b) => a + b, 0),
    darkByType: dark, darkTotal: Object.values(dark).reduce((a, b) => a + b, 0),
    tiedNodes: tied.length,
    canvas: g.width + 'x' + g.height, md5src: g.toDataURL('image/png'),
    ls: Object.keys(localStorage)
  };
}"""

CELLS = [('default', '?layout=force&dim=2d'),
         ('rulechip', '?layout=force&dim=2d&fam=guidelinerules'),
         ('allchips', '?layout=force&dim=2d&fam=uxprinciples,guidelines,guidelinerules,assets'),
         ('allconst', '?layout=force&dim=2d&fam=uxprinciples,guidelines,guidelinerules,assets,governance')]


def serve():
    p = subprocess.Popen([sys.executable, '-u', os.path.join(REPO, 'knowledge/_serve_explorer.py')],
                         cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    url, t0 = None, time.time()
    while time.time() - t0 < 25:
        line = p.stdout.readline()
        if not line: break
        sys.stdout.write('  serve| ' + line)
        if 'http://127.0.0.1:' in line:
            url = 'http://127.0.0.1:' + line.split('http://127.0.0.1:')[1].split('/')[0].strip(); break
    if not url:
        p.kill(); raise SystemExit('_serve_explorer.py printed no URL')
    for _ in range(40):
        try: urllib.request.urlopen(url + '/notes/', timeout=1).read(1); break
        except Exception: time.sleep(0.25)
    return p, url


if __name__ == '__main__':
    tag = sys.argv[1] if len(sys.argv) > 1 else 'after'
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
                pg = ctx.new_page(); errs = []
                pg.on('pageerror', lambda e: errs.append(str(e)))
                pg.on('console', lambda m: errs.append('console.' + m.type + ': ' + m.text) if m.type == 'error' else None)
                pg.goto(base + '/' + rel + qs, wait_until='load')
                pg.wait_for_timeout(2400)
                d = pg.evaluate(PROBE)
                d['canvasMd5'] = hashlib.md5(d.pop('md5src').encode()).hexdigest()
                d['errors'] = errs; d['url'] = rel + qs; d['viewport'] = '1280x800 light'
                shot = os.path.join(OUT, f'fo-{tag}-{name}-force-2d-1280-light.png')
                pg.screenshot(path=shot); d['bytes'] = os.path.getsize(shot)
                res[name] = d
                print(f"{tag}/{name:9} v{d['version']:6} canvas={d['canvasMd5'][:12]} drawn={d['drawnTotal']:<6} "
                      f"definedIn={d['definedIn']:<4} dark={d['darkTotal']:<4} tied={d['tiedNodes']} "
                      f"errors={len(errs)} ls={d['ls']} {d['bytes']:,}B")
                print(f"    stats: {d['stats']}")
                ctx.close()

            # ---- DRIVEN: the tie, read in the node's own INSPECT record
            ctx = br.new_context(viewport={'width': 1280, 'height': 900}, color_scheme='light',
                                 device_scale_factor=1)
            pg = ctx.new_page(); errs = []
            pg.on('pageerror', lambda e: errs.append(str(e)))
            pg.on('console', lambda m: errs.append('console.' + m.type + ': ' + m.text) if m.type == 'error' else None)
            pg.goto(base + '/' + rel + CELLS[2][1], wait_until='load')
            pg.wait_for_timeout(2000)
            pg.evaluate("id => openInspect(byId.get(id))", TIED)
            pg.wait_for_timeout(900)
            rec = pg.evaluate("""() => {
              const dl = document.querySelector('#insp dl.rec'); const o = {};
              const dts = [...dl.querySelectorAll('dt')], dds = [...dl.querySelectorAll('dd')];
              dts.forEach((dt, i) => o[dt.innerText.trim()] = (dds[i] || {}).innerText.trim());
              return {open: document.getElementById('insp').classList.contains('on'),
                      head: document.querySelector('#insp .mhead h2').innerText.trim(),
                      id: document.querySelector('#insp .mhead .id').innerText.trim(),
                      record: o,
                      relationGroups: [...document.querySelectorAll('#insp .egroup h4')].map(h => h.innerText.replace(/\\s+/g,' ').trim())};
            }""")
            shot = os.path.join(OUT, f'fo-{tag}-inspect-tied-1280-light.png')
            pg.screenshot(path=shot)
            rec['errors'] = errs; rec['bytes'] = os.path.getsize(shot); rec['node'] = TIED
            res['inspect'] = rec
            # the record's <dt>s are UPPERCASED by the page's own CSS, so innerText reads them so
            print(f"{tag}/inspect  open={rec['open']} family chip={rec['record'].get('FAMILY CHIP')!r}"
                  f" claimed by={rec['record'].get('CLAIMEDBY')!r} file kind={rec['record'].get('FILEKIND')!r}")
            print(f"    tie: {rec['record'].get('TIE')}")
            print(f"    relations: {rec['relationGroups']}")
            ctx.close(); br.close()
    finally:
        srv.terminate()
        try: srv.wait(timeout=5)
        except Exception: srv.kill()
    json.dump(res, open(os.path.join(OUT, f'shots-{tag}.json'), 'w'), indent=1)
    print('errors:', {k: v['errors'] for k, v in res.items() if v.get('errors')} or '[] everywhere')
