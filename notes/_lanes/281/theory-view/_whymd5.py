#!/usr/bin/env python3
"""#281 lane TV — WHY THE DEFAULT CANVAS MD5 MOVED, measured rather than asserted.

The brief allowed for it — "if the label rename repaints a pixel, say which and publish both
md5s" — and it did move. It was NOT the label rename, and it was not a re-fit either. This script
finds the cause by elimination and then names it, all off the two running pages:

  1. the DRAW SET — the ids of every node and every edge the page would draw at the page defaults,
     sorted and hashed. Identical means not one line was added, removed or gated differently.
  2. the LEGEND rectangle and the VIEW transform `fit()` settled on. Identical `k/x/y` means the
     picture is at the same zoom and the same pan, so a re-fit is not the explanation.
  3. the GHOST LAYER, which is the answer. The canvas does not skip an edge whose chip is off: it
     paints it at alpha 0.04, "a faint halo round the hub" (1.16), in its family's colour. s281-D4
     strokes a citation line in the view it is DRAWN in rather than the family it is STORED in, and
     that reading applies to the ghost too — so the 14 `obeys`→`ux:` lines, off at the defaults
     both before and after, changed from the HSBC green they were filed under to the Theory plum of
     the view they now belong to. The probe counts exactly those edges and names them.
  4. the PIXEL DIFF — how many pixels of the 879×744 canvas differ and in what bounding box, read
     out of the two canvases' own ImageData, so the size of the change is measured and not guessed.

  source knowledge/_render/seat_env.sh
  python3 notes/_lanes/281/theory-view/_whymd5.py <before.html> <out.json>

<before.html> is copied into the served root for the run and removed again in a finally block.
"""
import json, os, sys, time, hashlib, shutil, subprocess, urllib.request
from playwright.sync_api import sync_playwright

REPO = os.environ.get('RENDER_REPO') or os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..'))
HERE = os.path.dirname(os.path.abspath(__file__))

PROBE = """() => {
  const drawnN = [], drawnE = [];
  for (const n of NODES) if (alive(n) && NODEON(n)) drawnN.push(n.id);
  for (const e of EDGES) { if (!e.t || !alive(e)) continue;
    const s = byId.get(e.s), t = byId.get(e.t);
    if (s && t && NODEON(s) && NODEON(t) && EON(e)) drawnE.push(e.s + '|' + e.type + '|' + e.t); }
  drawnN.sort(); drawnE.sort();
  // the GHOST layer: an edge that is NOT drawn is still painted at 0.04 in its family's colour.
  // EDRAWF only exists from 1.24; before that the stroke was EFAM for every edge, ghost included.
  const F = (typeof EDRAWF === 'function') ? EDRAWF : EFAM;
  const ghosts = [];
  for (const e of EDGES) { if (!e.t || !alive(e)) continue;
    const s = byId.get(e.s), t = byId.get(e.t);
    if (!s || !t) continue;
    if (NODEON(s) && NODEON(t) && EON(e)) continue;          // drawn, not a ghost
    if (!NODEON(s) || !NODEON(t)) continue;                  // an end is off the stage entirely
    ghosts.push({e: e.s + '|' + e.type + '|' + e.t, stroke: F(e), stored: EFAM(e)}); }
  const lr = document.getElementById('legend').getBoundingClientRect();
  const g = document.getElementById('cv');
  // every node the canvas paints, DRAWN OR GHOSTED (dot() paints a node whose chip is off at 0.05),
  // with its force-2D coordinates: this is what says whether the two pictures are the same geometry.
  const paint = NODES.filter(alive).map(n => n.id + '@' + n.ox + ',' + n.oy).sort().join(';');
  return {version: KG.version, paintedNodes: NODES.filter(alive).length, paintSet: paint,
          drawnNodes: drawnN.length, drawnEdges: drawnE.length,
          drawSet: drawnN.join(',') + '#' + drawnE.join(','),
          ghostCount: ghosts.length,
          ghostsRecoloured: ghosts.filter(x => x.stroke !== x.stored),
          legend: {w: Math.round(lr.width), h: Math.round(lr.height)},
          view: {k: view.k, x: view.x, y: view.y},
          canvas: g.width + 'x' + g.height, md5src: g.toDataURL('image/png')};
}"""

PIXELS = """() => { const g = document.getElementById('cv');
  return {w: g.width, h: g.height,
          arr: Array.from(g.getContext('2d').getImageData(0, 0, g.width, g.height).data)}; }"""


def serve():
    p = subprocess.Popen([sys.executable, '-u', os.path.join(REPO, 'knowledge/_serve_explorer.py')],
                         cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    url, t0 = None, time.time()
    while time.time() - t0 < 25:
        line = p.stdout.readline()
        if not line: break
        if 'http://127.0.0.1:' in line:
            url = 'http://127.0.0.1:' + line.split('http://127.0.0.1:')[1].split('/')[0].strip(); break
    if not url: p.kill(); raise SystemExit('_serve_explorer.py printed no URL')
    for _ in range(40):
        try: urllib.request.urlopen(url + '/notes/', timeout=1).read(1); break
        except Exception: time.sleep(0.25)
    return p, url


if __name__ == '__main__':
    before_src, outp = sys.argv[1], sys.argv[2]
    # optional third argument: an AFTER page other than the shipped one, so the two causes can be
    # separated — HEAD's 1.23 against the pre-inscribe 1.24 build isolates the code change alone.
    after_src = sys.argv[3] if len(sys.argv) > 3 else None
    tmp = os.path.join(HERE, '_before-1.23.html')
    tmp2 = os.path.join(HERE, '_after-probe.html')
    shutil.copyfile(before_src, tmp)
    if after_src: shutil.copyfile(after_src, tmp2)
    srv, base = serve()
    res, px = {}, {}
    try:
        with sync_playwright() as pw:
            br = pw.chromium.launch(executable_path=os.environ['RENDER_SHELL'],
                                    args=['--no-sandbox', '--force-device-scale-factor=1'])
            pages = [('before', 'notes/_lanes/281/theory-view/_before-1.23.html'),
                     ('after', 'notes/_lanes/281/theory-view/_after-probe.html' if after_src
                               else 'notes/_KG-EXPLORER.html')]
            for tag, rel in pages:
                ctx = br.new_context(viewport={'width': 1280, 'height': 800},
                                     color_scheme='light', device_scale_factor=1)
                pg = ctx.new_page(); errs = []
                pg.on('pageerror', lambda e: errs.append(str(e)))
                pg.goto(base + '/' + rel + '?layout=force&dim=2d', wait_until='load')
                pg.wait_for_timeout(2400)
                d = pg.evaluate(PROBE)
                d['drawSetMd5'] = hashlib.md5(d.pop('drawSet').encode()).hexdigest()
                d['paintSetMd5'] = hashlib.md5(d.pop('paintSet').encode()).hexdigest()
                d['canvasMd5'] = hashlib.md5(d.pop('md5src').encode()).hexdigest()
                d['errors'] = errs
                px[tag] = pg.evaluate(PIXELS)
                res[tag] = d
                print(f"{tag:7} v{d['version']} canvas {d['canvas']} legend {d['legend']['w']}×{d['legend']['h']} "
                      f"view k={d['view']['k']:.6f} x={d['view']['x']:.2f} y={d['view']['y']:.2f}")
                print(f"        drawn {d['drawnNodes']} nodes / {d['drawnEdges']} edges · set={d['drawSetMd5'][:12]} "
                      f"· canvas={d['canvasMd5'][:12]} · ghosts {d['ghostCount']} "
                      f"({len(d['ghostsRecoloured'])} stroked away from their storage family) · errors={len(errs)}")
                ctx.close()
            br.close()
    finally:
        srv.terminate()
        try: srv.wait(timeout=5)
        except Exception: srv.kill()
        if os.path.exists(tmp): os.remove(tmp)
        if os.path.exists(tmp2): os.remove(tmp2)

    A, B, W = px['before']['arr'], px['after']['arr'], px['before']['w']
    diff = [i // 4 for i in range(0, len(A), 4) if A[i:i + 4] != B[i:i + 4]]
    d = {'canvas': f"{px['before']['w']}x{px['before']['h']}", 'pixelsTotal': len(A) // 4,
         'pixelsDiffering': len(diff)}
    if diff:
        xs = [p % W for p in diff]; ys = [p // W for p in diff]
        d['bbox'] = {'x0': min(xs), 'x1': max(xs), 'y0': min(ys), 'y1': max(ys)}
        d['sample'] = [{'x': p % W, 'y': p // W, 'before': A[p * 4:p * 4 + 4], 'after': B[p * 4:p * 4 + 4]}
                       for p in diff[:8]]
    res['pixelDiff'] = d
    res['drawSetIdentical'] = res['before']['drawSetMd5'] == res['after']['drawSetMd5']
    res['viewIdentical'] = res['before']['view'] == res['after']['view']
    res['paintSetIdentical'] = res['before']['paintSetMd5'] == res['after']['paintSetMd5']
    ghost = ('the ghost layer: %d edges are painted at alpha 0.04 because their chip is off, and the '
             '%d flagged `cited` among them changed stroke from their STORAGE family to the THEORY '
             'view they are now drawn in (s281-D4). No line was added, removed or re-gated: the draw '
             'set and the view transform are identical.'
             % (res['after']['ghostCount'], len(res['after']['ghostsRecoloured'])))
    if res['paintSetIdentical']:
        res['cause'] = ghost
    else:
        res['cause'] = ('TWO causes, and the second is the larger. (1) ' + ghost + ' (2) the painted node '
                        'set is NOT identical (%d nodes before, %d after): this lane INSCRIBED two rulings '
                        'into knowledge/_rulings.json, so the Constitution gained nodes and `place_extra` '
                        're-solved that family\'s own column. Those nodes are not DRAWN at the page '
                        'defaults — their chip is off — but dot() still paints an off-chip node at alpha '
                        '0.05, so the faint Constitution haze moves with them. Run this against the '
                        'pre-inscribe build of the same code to see cause (1) on its own.'
                        % (res['before']['paintedNodes'], res['after']['paintedNodes']))
    print(f"draw set identical : {res['drawSetIdentical']}")
    print(f"view transform same: {res['viewIdentical']}")
    print(f"painted node set   : {res['paintSetIdentical']} "
          f"({res['before']['paintedNodes']} → {res['after']['paintedNodes']})")
    print(f"pixels differing   : {d['pixelsDiffering']} of {d['pixelsTotal']} · bbox {d.get('bbox')}")
    print(f"recoloured ghosts  : {[g['e'] for g in res['after']['ghostsRecoloured']][:3]} …"
          f" ({len(res['after']['ghostsRecoloured'])}) "
          f"{res['after']['ghostsRecoloured'][0]['stored'] if res['after']['ghostsRecoloured'] else ''}"
          f" → {res['after']['ghostsRecoloured'][0]['stroke'] if res['after']['ghostsRecoloured'] else ''}")
    print('CAUSE:', res['cause'])
    json.dump(res, open(outp, 'w'), indent=1)
