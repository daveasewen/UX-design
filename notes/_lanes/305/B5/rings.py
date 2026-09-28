"""#305 B5: one ring view per candidate-2 run, re-rendered on the candidate-2 pack (sha 8a75ce32, the zip R4s2 scored)
at 1440 with the 640px shell frame released (R4s's RELEASE css, declared, as R4s2 did). Saves a clip the full width of
the content column at the ring's tile row, so the tile's share of the wall is visible, and measures that share.
Stage: $HOME/b5stage/cand2-r{1,2,3}/{out -> copy of notes/_lanes/304/R4c/cold/cand2-rN/out, pack -> ../pack (the zip)}.
usage (at the seat, env sourced): python3 notes/_lanes/305/B5/rings.py"""
import functools, http.server, json, os, socketserver, sys, threading, urllib.parse
from playwright.sync_api import sync_playwright
RELEASE = (".sh{height:auto!important;max-height:none!important;overflow:visible!important}"
           ".sh-body{min-height:auto!important}.sh-content{overflow:visible!important}")
ROOT = os.getcwd(); OUT = os.path.join(ROOT, 'notes/_lanes/305/B5/img'); ST = os.path.expanduser('~/b5stage')
VIEWS = [('r1', 'cand2-r1', 'index.html'), ('r2', 'cand2-r2', 'liquidity.html'), ('r3', 'cand2-r3', 'index.html')]
MEAS = r"""() => {
  const ring = document.querySelector('[data-dv-type="donut"],[data-dv-type="pie"]');
  if (!ring) return null;
  let tile = ring.closest('.c-bento__tile') || ring.closest('section,article,.card,.tile') || ring.parentElement;
  const main = document.querySelector('.sh-content main, main, .sh-content') || document.body;
  const mr = main.getBoundingClientRect(), tr = tile.getBoundingClientRect();
  const title = (tile.querySelector('h2,h3,h4,.title,figcaption') || {}).textContent || '';
  return {main_left: mr.left, main_width: mr.width, tile_left: tr.left, tile_top: tr.top + scrollY, tile_w: tr.width, tile_h: tr.height,
          share: tr.width / mr.width, title: title.replace(/\s+/g,' ').trim().slice(0,90), tile_cls: tile.className.toString().slice(0,60)};
}"""
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
srv = socketserver.TCPServer(("127.0.0.1", 0), functools.partial(Q, directory="/")); port = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
res = {}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ['RENDER_SHELL'], args=['--no-sandbox'])
    for lab, run, page in VIEWS:
        ctx = b.new_context(viewport={'width': 1440, 'height': 900}, device_scale_factor=1, reduced_motion='reduce')
        pg = ctx.new_page(); errs = []; pg.on('pageerror', lambda e: errs.append(str(e)[:160])); pg.on('dialog', lambda x: x.dismiss())
        u = 'http://127.0.0.1:%d%s' % (port, urllib.parse.quote(os.path.join(ST, run, 'out', page)))
        pg.goto(u, wait_until='load', timeout=30000); pg.wait_for_timeout(1500)
        pg.add_style_tag(content=RELEASE); pg.wait_for_timeout(300)
        pg.evaluate("() => window.dispatchEvent(new Event('resize'))"); pg.wait_for_timeout(900)
        m = pg.evaluate(MEAS); m['errors'] = errs; m['url_page'] = page; res[lab] = m
        pad = 16
        clip = {'x': max(0, m['main_left'] - pad), 'y': max(0, m['tile_top'] - pad), 'width': min(1440 - max(0, m['main_left'] - pad), m['main_width'] + 2 * pad), 'height': m['tile_h'] + 2 * pad}
        pg.screenshot(path=os.path.join(OUT, 'ring-cand2-%s.png' % lab), clip=clip, full_page=True)
        print(lab, json.dumps(m)[:400]); ctx.close()
    b.close()
json.dump(res, open(os.path.join(ROOT, 'notes/_lanes/305/B5/rings.json'), 'w'), indent=1)
