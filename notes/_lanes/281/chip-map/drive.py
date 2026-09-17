#!/usr/bin/env python3
"""#281 lane CM — the DRIVEN pass: INSPECT's edge door (↔) reads the six with their verbs.

Brief item 3's last sentence. For each of the six edge types that got a family in v1.21 this opens
THE EDGE ITSELF in the inspect modal (the same `openEdge` the ↔ button calls) and reads back what
the modal actually says — the verb badge, the direction sentence, the family, the split, and, for
the 14 obeys→ux lines, the HELD row. Nothing is asserted from the source: every string below is
scraped out of the rendered modal.

  source knowledge/_render/seat_env.sh
  python3 notes/_lanes/281/chip-map/drive.py
"""
import json, os, sys, time, subprocess, urllib.request
from playwright.sync_api import sync_playwright

REPO = os.environ.get('RENDER_REPO') or os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..'))
OUT = os.path.join(REPO, 'notes/_lanes/281/chip-map/inspect.json')
SIX = ['answersIntent', 'hasDataShape', 'providesRole', 'yieldsTo', 'defaultActive', 'obeys']

PROBE = """(types) => {
  const out = {};
  for (const ty of types) {
    const picks = [];
    const first = EDGES.find(e => e.type === ty && e.t);
    const anull = EDGES.find(e => e.type === ty && !e.t);
    const held  = EDGES.find(e => e.type === ty && e.held);
    if (first) picks.push(['resolved', first]);
    if (anull) picks.push(['declared null', anull]);
    if (held)  picks.push(['held', held]);
    out[ty] = {family: FAMILY[ty] || null, read: READ[ty] || null,
               verbs: (KG.verbs.of || {})[ty] || null,
               unread: (KG.verbs.unread || {})[ty] || null,
               stored: EDGES.filter(e => e.type === ty).length, doors: []};
    for (const [kind, e] of picks) {
      openEdge(e);
      const sheet = document.querySelector('#insp .sheet');
      const rows = {};
      sheet.querySelectorAll('dl dt').forEach(dt => {
        rows[dt.textContent.trim()] = (dt.nextElementSibling || {}).textContent
          ? dt.nextElementSibling.textContent.replace(/\\s+/g, ' ').trim() : '';
      });
      out[ty].doors.push({kind,
        title: (sheet.querySelector('h2') || {}).textContent,
        id: (sheet.querySelector('.id') || {}).textContent,
        verbBadges: [...sheet.querySelectorAll('.verb')].map(v => v.textContent.trim()),
        rows});
      closeInspect();
    }
  }
  return out;
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


if __name__ == '__main__':
    srv, base = serve()
    errs = []
    try:
        with sync_playwright() as pw:
            br = pw.chromium.launch(executable_path=os.environ['RENDER_SHELL'], args=['--no-sandbox'])
            ctx = br.new_context(viewport={'width': 1440, 'height': 900}, color_scheme='light')
            pg = ctx.new_page()
            pg.on('pageerror', lambda e: errs.append(str(e)))
            pg.on('console', lambda m: errs.append('console.' + m.type + ': ' + m.text) if m.type == 'error' else None)
            pg.goto(base + '/notes/_KG-EXPLORER.html', wait_until='load')
            pg.wait_for_timeout(2000)
            res = pg.evaluate(PROBE, SIX)
            br.close()
    finally:
        srv.terminate()
        try:
            srv.wait(timeout=5)
        except Exception:
            srv.kill()
    res['_errors'] = errs
    json.dump(res, open(OUT, 'w'), indent=1)
    for ty in SIX:
        r = res[ty]
        print(f"{ty:<14} fam={str(r['family']):<15} stored={r['stored']:<4} verbs={r['verbs']} read={r['read']}")
        for d in r['doors']:
            print(f"    [{d['kind']:<13}] {d['id']}")
            print(f"      badges  {d['verbBadges']}")
            for k in ('storage type', 'verb', 'this relation, read', 'the verb’s own sentence',
                      'split by', 'family', 'held', 'provenance', 'stored in'):
                if k in d['rows']:
                    print(f"      {k:<24} {d['rows'][k][:150]}")
    print('page errors:', errs or '[]')
    print('wrote', OUT)
