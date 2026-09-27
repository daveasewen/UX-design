"""shots.py — R4s2 (#304): overview shots for Dave's side-by-side, and the dark-ground measurement.
For each entry (label, stage out dir): at 1440x900 @1x over a local http server (localStorage works):
  asshipped-light.png   the viewport as shipped (the 640px shell frame NOT released)
  full-light.png        full length, frame released (declared: RELEASE css, as R4s views.py)
  full-dark.png         the run's OWN dark control clicked (R4s DARKCLICK), full length, frame released
and records in shots.json: the dark section ground and tile backgrounds, the shell frame height,
the bento wall gap. Nothing in the stage or the frozen outputs is written.
usage: python3 shots.py <label>=<abs out dir> ...   (seat env sourced in the same call)"""
import functools, http.server, json, os, socketserver, sys, threading, time, urllib.parse
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "R4s"))
import views as R4S   # RELEASE, DARKCLICK
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "shots"); os.makedirs(OUT, exist_ok=True)
PROBE = r"""() => {
 const bg = e => e ? getComputedStyle(e).backgroundColor : null;
 const ground = document.querySelector('.tpl-wall, .c-bento.tpl-wall') ;
 const sec = ground ? ground.closest('section,div[class*=ground],div[class*=subtle],main') : null;
 let groundEl = ground; for (let a = ground; a; a = a.parentElement) { const c = getComputedStyle(a).backgroundColor; if (c && c !== 'rgba(0, 0, 0, 0)') { groundEl = a; break; } }
 const tiles = [...document.querySelectorAll('.c-bento__tile')].filter(t => !t.classList.contains('c-bento'));
 const tileBgs = {}; tiles.forEach(t => { const c = bg(t); tileBgs[c] = (tileBgs[c]||0)+1; });
 const panel = document.querySelector('.stat-card, .c-bento__tile:not(.c-bento)');
 const sh = document.querySelector('.sh'); const wall = document.querySelector('.tpl-wall');
 return {theme: document.documentElement.getAttribute('data-theme'), ground_el: groundEl ? groundEl.tagName+'.'+[...groundEl.classList].slice(0,3).join('.') : null,
   ground_bg: bg(groundEl), wall_bg: bg(ground), tile_bgs: tileBgs, first_panel_bg: bg(panel),
   first_panel_border: panel ? getComputedStyle(panel).borderTopColor + ' ' + getComputedStyle(panel).borderTopWidth : null,
   shell_h: sh ? Math.round(sh.getBoundingClientRect().height) : null, wall_gap: wall ? getComputedStyle(wall).gap : null};
}"""
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
def main():
    entries = [a.split("=", 1) for a in sys.argv[1:]]
    h = functools.partial(Q, directory="/"); srv = socketserver.TCPServer(("127.0.0.1", 0), h); port = srv.server_address[1]
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    res = json.load(open(os.path.join(OUT, "shots.json"))) if os.path.exists(os.path.join(OUT, "shots.json")) else {}
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=os.environ.get("RENDER_SHELL"), args=["--no-sandbox"])
        for lab, d in entries:
            ctx = b.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=1, reduced_motion="reduce")
            pg = ctx.new_page(); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)[:160])); pg.on("dialog", lambda x: x.dismiss())
            u = "http://127.0.0.1:%d%s/index.html" % (port, urllib.parse.quote(d))
            pg.goto(u, wait_until="load", timeout=30000); pg.wait_for_timeout(1800)
            pg.screenshot(path=os.path.join(OUT, lab + "-asshipped-light.png"))
            r = {"url": u, "light": pg.evaluate(PROBE)}
            pg.add_style_tag(content=R4S.RELEASE); pg.wait_for_timeout(300)
            pg.evaluate("() => window.dispatchEvent(new Event('resize'))"); pg.wait_for_timeout(900)
            pg.screenshot(path=os.path.join(OUT, lab + "-full-light.png"), full_page=True)
            pg.evaluate("() => window.scrollTo(0,0)")
            dk = pg.evaluate(R4S.DARKCLICK); pg.wait_for_timeout(1400)
            dk["after"] = pg.evaluate("() => document.documentElement.getAttribute('data-theme')")
            r["dark_switch"] = dk; r["dark"] = pg.evaluate(PROBE)
            pg.screenshot(path=os.path.join(OUT, lab + "-full-dark.png"), full_page=True)
            r["pageerrors"] = errs; res[lab] = r; ctx.close()
            print(lab, json.dumps({k: r[k] for k in ("light", "dark")})[:600])
        b.close()
    json.dump(res, open(os.path.join(OUT, "shots.json"), "w"), indent=1)
main()
