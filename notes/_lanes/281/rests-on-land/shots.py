#!/usr/bin/env python3
"""#281 lane RL — rests on, landed: shots, the drawn/dark census, the md5 forensics and two driven
INSPECT passes.

Lane TV's `notes/_lanes/281/theory-view/shots.py` with this lane's cells. NEVER DRIVEN for the
picture cells: a fresh browser.new_context per shot, the colour scheme emulated, the chips chosen by
URL flag (`?layout=…&dim=…&fam=…`), never by a click. Two DRIVEN passes open INSPECT on the two
rows the brief names — `col26-016`, which rests on TWO principles and carries his RAG-red caveat,
and `logo26-001`, the declared null that carries his native-app rationale — so both are read out of
the modal rather than asserted from source.

`--pages a,b,c` hashes the default canvas of several built pages in one run, which is how the
default-canvas md5 is decomposed (HEAD's 1.24 · 1.25 with no restsOn lines · 1.25 as shipped).

  source knowledge/_render/seat_env.sh
  python3 notes/_lanes/281/rests-on-land/shots.py after
  python3 notes/_lanes/281/rests-on-land/shots.py md5 --pages notes/_lanes/281/rests-on-land/_tmp/head.html,...
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
  const ro = EDGES.filter(e => e.type === 'restsOn');
  const roNull = ro.filter(e => !e.t);
  const srcs = [...new Set(ro.filter(e => e.t).map(e => e.s))];
  const two  = srcs.filter(s => ro.filter(e => e.t && e.s === s).length > 1);
  return {
    version: KG.version,
    stats: document.getElementById('stats').innerText.replace(/\\s+/g, ' ').trim(),
    famOn: Object.fromEntries(Object.entries(famOn)),
    drawnByFam: fam, drawnTotal: Object.values(fam).reduce((a, b) => a + b, 0),
    restsOnDrawn: typ.restsOn || 0, obeysDrawn: typ.obeys || 0,
    darkByType: dark, darkTotal: Object.values(dark).reduce((a, b) => a + b, 0),
    restsEdges: ro.length, restsNulls: roNull.length, restsRules: srcs.length, restsTwo: two.length,
    restsNotes: ro.filter(e => e.daveNote).length,
    citedEdges: EDGES.filter(e => e.cited).length, heldEdges: EDGES.filter(e => e.held).length,
    chipLabels: [...document.querySelectorAll('#legend .view .chip.edge')].map(c => c.innerText.replace(/\\s+/g,' ').trim()),
    viewNames: [...document.querySelectorAll('#legend .view h4')].map(h => h.innerText.replace(/\\s+/g,' ').trim()),
    canvas: g.width + 'x' + g.height, md5src: g.toDataURL('image/png'),
    ls: Object.keys(localStorage)
  };
}"""

RO_FAM = 'uxprinciples,guidelinerules,restson'
CELLS = [
    ('default',  '?layout=force&dim=2d',                                   1280, 800),
    ('restson',  '?layout=force&dim=2d&fam=' + RO_FAM,                     1280, 800),
    ('chipoff',  '?layout=force&dim=2d&fam=uxprinciples,guidelinerules',   1280, 800),
    ('strata',   '?layout=strata&dim=2d&fam=' + RO_FAM,                    1280, 800),
    ('allchips', '?layout=force&dim=2d&fam=uxprinciples,guidelines,guidelinerules,assets,uxcited,restson', 1280, 800),
    ('phone',    '?layout=force&dim=2d&fam=' + RO_FAM,                     390, 844),
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


def md5_mode(pages):
    """Hash the DEFAULT canvas of each page, same viewport, same script, one run."""
    srv, base = serve(); out = {}
    try:
        with sync_playwright() as pw:
            br = pw.chromium.launch(executable_path=os.environ['RENDER_SHELL'],
                                    args=['--no-sandbox', '--force-device-scale-factor=1'])
            for rel in pages:
                ctx = br.new_context(viewport={'width': 1280, 'height': 800}, color_scheme='light',
                                     device_scale_factor=1)
                pg = ctx.new_page(); errs = []
                pg.on('pageerror', lambda e: errs.append(str(e)))
                pg.goto(base + '/' + rel + '?layout=force&dim=2d', wait_until='load')
                pg.wait_for_timeout(2400)
                d = pg.evaluate("""() => {const g=document.getElementById('cv');
                  return {v:KG.version, n:NODES.length, e:EDGES.length,
                          drawn:SHOWNE.length, shown:SHOWN.length,
                          md5src:g.toDataURL('image/png'), canvas:g.width+'x'+g.height,
                          xy: NODES.slice(0,1).concat(NODES.filter(n=>n.id==='ux:pr-fitts')).map(n=>[n.id,n.x,n.y])};}""")
                d['canvasMd5'] = hashlib.md5(d.pop('md5src').encode()).hexdigest()
                d['errors'] = errs
                out[rel] = d
                print(f"  md5 {rel:70} v{d['v']} nodes={d['n']} edges={d['e']} "
                      f"canvas={d['canvasMd5']} errors={len(errs)}")
                ctx.close()
            br.close()
    finally:
        srv.terminate()
        try: srv.wait(timeout=5)
        except Exception: srv.kill()
    json.dump(out, open(os.path.join(OUT, 'md5.json'), 'w'), indent=1)
    return out


DRIVE = """(rid) => {
  const ro = EDGES.filter(e => e.type === 'restsOn' && e.s === rid);
  if (!ro.length) return {found:false};
  openEdge(ro[0]);
  return {found:true, n: ro.length, ends: ro.map(e => e.t)};
}"""

READ_MODAL = """() => {
  const dl = document.querySelector('#insp dl.rec'); if (!dl) return {open:false};
  const o = {}; const dts=[...dl.querySelectorAll('dt')], dds=[...dl.querySelectorAll('dd')];
  dts.forEach((dt,i)=>o[dt.innerText.trim()]=(dds[i]||{}).innerText.trim());
  return {open: document.getElementById('insp').classList.contains('on'),
          head: (document.querySelector('#insp .mhead h2')||{}).innerText,
          id: (document.querySelector('#insp .mhead .id')||{}).innerText,
          record: o};
}"""


if __name__ == '__main__':
    tag = sys.argv[1] if len(sys.argv) > 1 else 'after'
    if tag == 'md5':
        pages = sys.argv[sys.argv.index('--pages') + 1].split(',')
        md5_mode(pages); raise SystemExit(0)

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
                if name == 'phone':
                    try:
                        pg.click('#legend .ltog'); pg.wait_for_timeout(700)
                    except Exception as ex: errs.append('sheet: ' + str(ex))
                d = pg.evaluate(PROBE)
                d['canvasMd5'] = hashlib.md5(d.pop('md5src').encode()).hexdigest()
                d['errors'] = errs; d['url'] = rel + qs; d['viewport'] = f'{w}x{h} light'
                shot = os.path.join(OUT, f'rl-{tag}-{name}-{w}-light.png')
                pg.screenshot(path=shot); d['bytes'] = os.path.getsize(shot)
                if name == 'allchips':
                    lg = os.path.join(OUT, f'rl-{tag}-legend-{w}-light.png')
                    try: pg.locator('#legend').screenshot(path=lg); d['legendBytes'] = os.path.getsize(lg)
                    except Exception as ex: errs.append('legend clip: ' + str(ex))
                res[name] = d
                print(f"{tag}/{name:9} v{d['version']:6} canvas={d['canvasMd5'][:12]} drawn={d['drawnTotal']:<6} "
                      f"restsOn={d['restsOnDrawn']:<4} dark={d['darkTotal']:<4} errors={len(errs)} {d['bytes']:,}B")
                print(f"    stats: {d['stats']}")
                print(f"    chips: {d['chipLabels']}")
                ctx.close()

            # ---- DRIVEN: the two rows the brief names
            for rid, label in (('rule:col26-016', 'col26-016'), ('rule:logo26-001', 'logo26-001')):
                ctx = br.new_context(viewport={'width': 1280, 'height': 900}, color_scheme='light',
                                     device_scale_factor=1)
                pg = ctx.new_page(); errs = []
                pg.on('pageerror', lambda e: errs.append(str(e)))
                pg.on('console', lambda m: errs.append('console.' + m.type + ': ' + m.text) if m.type == 'error' else None)
                pg.goto(base + '/' + rel + CELLS[1][1], wait_until='load')
                pg.wait_for_timeout(2000)
                found = pg.evaluate(DRIVE, rid)
                pg.wait_for_timeout(900)
                rec = pg.evaluate(READ_MODAL)
                shot = os.path.join(OUT, f'rl-{tag}-inspect-{label}-1280-light.png')
                pg.screenshot(path=shot)
                rec['errors'] = errs; rec['bytes'] = os.path.getsize(shot); rec['found'] = found
                # and the NODE's own record, so both of col26-016's principles are seen in one place
                pg.evaluate("(rid)=>{const n=byId.get(rid); if(n) openInspect(n);}", rid)
                pg.wait_for_timeout(900)
                nshot = os.path.join(OUT, f'rl-{tag}-inspect-node-{label}-1280-light.png')
                pg.screenshot(path=nshot)
                rec['nodeGroups'] = pg.evaluate("""() => [...document.querySelectorAll('#insp .egroup h4')]
                    .map(h => h.innerText.replace(/\\s+/g,' ').trim())""")
                rec['nodeRows'] = pg.evaluate("""() => [...document.querySelectorAll('#insp .egroup')]
                    .filter(g => /restsOn/.test(g.innerText))
                    .map(g => g.innerText.replace(/\\s+/g,' ').trim().slice(0, 400))""")
                res['inspect-' + label] = rec
                print(f"{tag}/inspect {label}: found={found} open={rec.get('open')} {rec.get('id')!r}")
                for k, v in (rec.get('record') or {}).items():
                    print(f"    {k}: {v[:220]}")
                ctx.close()
            br.close()
    finally:
        srv.terminate()
        try: srv.wait(timeout=5)
        except Exception: srv.kill()
    json.dump(res, open(os.path.join(OUT, f'shots-{tag}.json'), 'w'), indent=1)
    print('errors:', {k: v['errors'] for k, v in res.items() if v.get('errors')} or '[] everywhere')
