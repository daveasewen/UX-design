#!/usr/bin/env python3
"""#281 lane PH — the driven pass on INSPECT, for the two types this lane switched on.

Every string below is SCRAPED OUT OF THE RENDERED MODAL, never asserted from source: the page is
served (s280-D2), the Explanation chip is switched on by URL flag (`?fam=uxprinciples`, never a
click), a `ux:` node is inspected through its own `i` button, and the `inFamily` group, the
`evidencedBy` group and the two edge doors are read back.

  source knowledge/_render/seat_env.sh
  python3 notes/_lanes/281/principles-home/drive.py
"""
import json, os, sys, time, subprocess, urllib.request
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
OUT = os.path.join(HERE, 'inspect.json')

SCRAPE = """(id) => {
  openInspect(byId.get(id));
  const sheet = document.querySelector('#insp .sheet');
  const out = {title: (sheet.querySelector('h2') || {}).textContent,
               id: (sheet.querySelector('.id') || {}).textContent, groups: []};
  sheet.querySelectorAll('.egroup').forEach(g => {
    out.groups.push({
      head: g.querySelector('h4').textContent.replace(/\\s+/g, ' ').trim(),
      reads: [...g.querySelectorAll('.reads')].map(r => r.textContent.replace(/\\s+/g, ' ').trim()),
      firstRows: [...g.querySelectorAll('.rows > *')].slice(0, 2)
                   .map(r => r.textContent.replace(/\\s+/g, ' ').trim())});
  });
  closeInspect();
  return out;
}"""

EDGE = """(k) => {
  openEdge(EDGES[k]);
  const sheet = document.querySelector('#insp .sheet');
  const rows = {};
  sheet.querySelectorAll('dl dt').forEach(dt => {
    rows[dt.textContent.trim()] = (dt.nextElementSibling || {}).textContent
      ? dt.nextElementSibling.textContent.replace(/\\s+/g, ' ').trim() : '';
  });
  const out = {title: (sheet.querySelector('h2') || {}).textContent,
               id: (sheet.querySelector('.id') || {}).textContent,
               verbBadges: [...sheet.querySelectorAll('.verb')].map(v => v.textContent.trim()),
               rows};
  closeInspect();
  return out;
}"""

PICK = """() => ({
  inFamily: EDGES.findIndex(e => e.type === 'inFamily'),
  uxEvidence: EDGES.findIndex(e => e.type === 'evidencedBy' && e.fam === 'uxprinciples' && e.t),
  uxEvidenceNull: EDGES.findIndex(e => e.type === 'evidencedBy' && e.fam === 'uxprinciples' && !e.t),
  govEvidence: EDGES.findIndex(e => e.type === 'evidencedBy' && e.fam === 'governance' && e.t),
  familyNodes: NODES.filter(x => x.type === 'family').length,
  uxEvidenceNodes: NODES.filter(x => x.type === 'evidence' && x.fam === 'uxprinciples').length,
  govEvidenceNodes: NODES.filter(x => x.type === 'evidence' && x.fam === 'governance').length,
  familyChip: ALLTYPES.includes('family'),
  evidenceChip: ALLTYPES.includes('evidence'),
  inFamilyFam: FAMILY['inFamily'], evidencedByTypeFam: FAMILY['evidencedBy'],
  divergent: EDGES.filter(e => e.fam && e.fam !== FAMILY[e.type])
                  .map(e => [e.type, e.fam, FAMILY[e.type], e.t === null]).slice(0, 40)
})"""


def serve():
    p = subprocess.Popen([sys.executable, '-u', os.path.join(REPO, 'knowledge/_serve_explorer.py')],
                         cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    url, t0 = None, time.time()
    while time.time() - t0 < 25:
        line = p.stdout.readline()
        if not line:
            break
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
    srv, base = serve()
    res = {}
    try:
        with sync_playwright() as pw:
            br = pw.chromium.launch(executable_path=os.environ['RENDER_SHELL'], args=['--no-sandbox'])
            ctx = br.new_context(viewport={'width': 1440, 'height': 900}, color_scheme='light')
            pg = ctx.new_page()
            errs = []
            pg.on('pageerror', lambda e: errs.append(str(e)))
            pg.on('console', lambda m: errs.append('console.' + m.type + ': ' + m.text) if m.type == 'error' else None)
            pg.goto(base + '/notes/_KG-EXPLORER.html?fam=uxprinciples&layout=force&dim=2d', wait_until='load')
            pg.wait_for_timeout(2400)
            res['picked'] = pg.evaluate(PICK)
            res['node_ux'] = pg.evaluate(SCRAPE, 'ux:pr-fitts')
            res['node_family'] = pg.evaluate(SCRAPE, 'family:fam-laws-of-ux')
            for k in ('inFamily', 'uxEvidence', 'uxEvidenceNull', 'govEvidence'):
                i = res['picked'][k]
                res['edge_' + k] = pg.evaluate(EDGE, i) if i >= 0 else None
            res['errors'] = errs
            ctx.close(); br.close()
    finally:
        srv.terminate()
        try: srv.wait(timeout=5)
        except Exception: srv.kill()
    json.dump(res, open(OUT, 'w'), indent=1)
    print(json.dumps(res, indent=1)[:4000])
    print('errors:', res['errors'] or '[]')
