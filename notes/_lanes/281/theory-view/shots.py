#!/usr/bin/env python3
"""#281 lane TV — the Theory view: shots, the drawn/dark probe, and the driven INSPECT pass.

Lane FO's `notes/_lanes/281/file-owner/shots.py` with this lane's cells. NEVER DRIVEN for the
five picture cells: a fresh browser.new_context per shot, the colour scheme emulated, the chips
chosen by URL flag (`?layout=…&dim=…&fam=…`), never by a click. A SIXTH pass DRIVES `openEdge`
on one of the 14 `obeys`→`ux:` citation lines so the designer's own `$why` can be read out of the
modal rather than asserted from source.

`before` runs the same cells against HEAD's page, so the default-canvas md5 is compared by ONE
script at ONE viewport, not across lanes.

  source knowledge/_render/seat_env.sh
  python3 notes/_lanes/281/theory-view/shots.py before|after
"""
import json, os, sys, time, hashlib, subprocess, urllib.request
from playwright.sync_api import sync_playwright

REPO = os.environ.get('RENDER_REPO') or os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..'))
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'shots')
os.makedirs(OUT, exist_ok=True)

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
  const cited = EDGES.filter(e => e.cited);
  const held  = EDGES.filter(e => e.held);
  // the 4 principles the 14 lines land on, and their degree at THIS setting
  const ends = [...new Set(cited.map(e => e.t))].sort();
  return {
    version: KG.version,
    stats: document.getElementById('stats').innerText.replace(/\\s+/g, ' ').trim(),
    famOn: Object.fromEntries(Object.entries(famOn)),
    drawnByFam: fam, obeysDrawn: typ.obeys || 0,
    drawnTotal: Object.values(fam).reduce((a, b) => a + b, 0),
    darkByType: dark, darkTotal: Object.values(dark).reduce((a, b) => a + b, 0),
    citedEdges: cited.length, heldEdges: held.length,
    citedEnds: ends, citedEndDegree: Object.fromEntries(ends.map(i => [i, deg.get(i)])),
    viewNames: [...document.querySelectorAll('#legend .view h4')].map(h => h.innerText.replace(/\\s+/g,' ').trim()),
    bandNames: (KG.bands || []).map(b => b.name),
    plateNames: (KG.plates || []).map(b => b.name),
    ringNames: (KG.rings || []).map(b => b.name),
    shellNames: (KG.shells || []).map(b => b.name),
    canvas: g.width + 'x' + g.height, md5src: g.toDataURL('image/png'),
    ls: Object.keys(localStorage)
  };
}"""

CELLS = [
    ('default',  '?layout=force&dim=2d',                          1280, 800),
    ('citedon',  '?layout=force&dim=2d&fam=uxprinciples,uxcited', 1280, 800),
    ('uxonly',   '?layout=force&dim=2d&fam=uxprinciples',         1280, 800),
    ('strata',   '?layout=strata&dim=2d&fam=uxprinciples,uxcited', 1280, 800),
    ('allchips', '?layout=force&dim=2d&fam=uxprinciples,guidelines,guidelinerules,assets,uxcited', 1280, 800),
    ('phone',    '?layout=force&dim=2d&fam=uxprinciples,uxcited', 390, 844),
]


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
            for name, qs, w, h in CELLS:
                ctx = br.new_context(viewport={'width': w, 'height': h},
                                     color_scheme='light', device_scale_factor=1)
                pg = ctx.new_page(); errs = []
                pg.on('pageerror', lambda e: errs.append(str(e)))
                pg.on('console', lambda m: errs.append('console.' + m.type + ': ' + m.text) if m.type == 'error' else None)
                pg.goto(base + '/' + rel + qs, wait_until='load')
                pg.wait_for_timeout(2400)
                if name == 'phone':          # the sheet is closed at phone width: open it, once
                    try:
                        pg.click('#legend .ltog'); pg.wait_for_timeout(700)
                    except Exception as ex: errs.append('sheet: ' + str(ex))
                d = pg.evaluate(PROBE)
                d['canvasMd5'] = hashlib.md5(d.pop('md5src').encode()).hexdigest()
                d['errors'] = errs; d['url'] = rel + qs; d['viewport'] = f'{w}x{h} light'
                shot = os.path.join(OUT, f'tv-{tag}-{name}-{w}-light.png')
                pg.screenshot(path=shot); d['bytes'] = os.path.getsize(shot)
                if name == 'allchips':       # the legend alone, so the renamed boxes read
                    lg = os.path.join(OUT, f'tv-{tag}-legend-{w}-light.png')
                    try: pg.locator('#legend').screenshot(path=lg); d['legendBytes'] = os.path.getsize(lg)
                    except Exception as ex: errs.append('legend clip: ' + str(ex))
                res[name] = d
                print(f"{tag}/{name:9} v{d['version']:6} canvas={d['canvasMd5'][:12]} drawn={d['drawnTotal']:<6} "
                      f"obeys={d['obeysDrawn']:<4} cited={d['citedEdges']} held={d['heldEdges']} "
                      f"dark={d['darkTotal']:<4} errors={len(errs)} ls={d['ls']} {d['bytes']:,}B")
                print(f"    stats: {d['stats']}")
                print(f"    views: {d['viewNames']}")
                print(f"    bands: {d['bandNames']} · degree at the 4 ends: {d['citedEndDegree']}")
                ctx.close()

            # ---- DRIVEN: one of the 14 citation lines, in the edge's own INSPECT door
            ctx = br.new_context(viewport={'width': 1280, 'height': 900}, color_scheme='light',
                                 device_scale_factor=1)
            pg = ctx.new_page(); errs = []
            pg.on('pageerror', lambda e: errs.append(str(e)))
            pg.on('console', lambda m: errs.append('console.' + m.type + ': ' + m.text) if m.type == 'error' else None)
            pg.goto(base + '/' + rel + CELLS[1][1], wait_until='load')
            pg.wait_for_timeout(2000)
            opened = pg.evaluate("""() => {
              const e = EDGES.find(x => (x.cited || x.held) && x.type === 'obeys' && String(x.t||'').startsWith('ux:'));
              if (!e) return false; openEdge(e); return true; }""")
            pg.wait_for_timeout(900)
            rec = pg.evaluate("""() => {
              const dl = document.querySelector('#insp dl.rec'); if (!dl) return {open:false};
              const o = {}; const dts=[...dl.querySelectorAll('dt')], dds=[...dl.querySelectorAll('dd')];
              dts.forEach((dt,i)=>o[dt.innerText.trim()]=(dds[i]||{}).innerText.trim());
              return {open: document.getElementById('insp').classList.contains('on'),
                      head: document.querySelector('#insp .mhead h2').innerText.trim(),
                      id: document.querySelector('#insp .mhead .id').innerText.trim(),
                      record: o};
            }""")
            shot = os.path.join(OUT, f'tv-{tag}-inspect-edge-1280-light.png')
            pg.screenshot(path=shot)
            rec['errors'] = errs; rec['bytes'] = os.path.getsize(shot); rec['opened'] = opened
            res['inspect'] = rec
            print(f"{tag}/inspect  open={rec.get('open')} {rec.get('id')!r}")
            for k in ('FAMILY', 'HELD', 'CITED BY A DESIGN', 'WHY — THE DESIGNER’S OWN WORDS', 'NOTE'):
                if rec.get('record', {}).get(k): print(f"    {k}: {rec['record'][k]}")
            ctx.close(); br.close()
    finally:
        srv.terminate()
        try: srv.wait(timeout=5)
        except Exception: srv.kill()
    json.dump(res, open(os.path.join(OUT, f'shots-{tag}.json'), 'w'), indent=1)
    print('errors:', {k: v['errors'] for k, v in res.items() if v.get('errors')} or '[] everywhere')
