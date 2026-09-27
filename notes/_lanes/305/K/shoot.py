"""K (#305): the rebuilt v1.0.14 candidate, looked at.
(1) cand2-r3's generated pages RESTAGED on the rebuilt pack (R4s2's restage method: the pack beside out/
    is the unzipped v1.0.14 candidate; every inlined engine block is replaced by the pack's own dv-*.js),
    then shot exactly as R4s2/shots.py shot candidate 2 (1440x900 @1x, http, RELEASE css, the run's own
    dark control), so K's shots sit beside R4s2's cand2-r3-full-{light,dark}.png like for like;
(2) one chart view (cand2-r3 liquidity.html, same method, light);
(3) the pack's own showroom index at 1440, light and dark (data-theme set on <html>).
Writes only under notes/_lanes/305/K/ (restage/, renders/)."""
import functools, glob, http.server, json, os, re, shutil, socketserver, sys, threading
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "../../../.."))
sys.path.insert(0, os.path.join(REPO, "notes/_lanes/304/R4s"))
import views as R4S   # RELEASE, DARKCLICK (read-only import)
from playwright.sync_api import sync_playwright
PACK = os.path.join(HERE, "cold/Apollo-Spider-v1.0.14")
SRC = os.path.join(REPO, "notes/_lanes/304/R4c/cold/cand2-r3/out")
ST = os.path.join(HERE, "restage/cand2-r3"); OUT = os.path.join(HERE, "renders")
FRESH = not os.path.exists(ST)          # the mount refuses deletes: stage once, then reuse
if FRESH:
    os.makedirs(ST); shutil.copytree(SRC, ST + "/out"); os.symlink(PACK, ST + "/pack")
pat = re.compile(r'<script>\n/\* INJECTED from knowledge/canon/([\w-]+)\.js .*?\n</script>', re.S)
n = 0
for f in (glob.glob(ST + "/out/*.html") if FRESH else []):
    s = open(f).read()
    def rep(m):
        global n; n += 1
        body = open(os.path.join(PACK, "knowledge/canon", m.group(1) + ".js")).read()
        return "<script>\n/* INJECTED from knowledge/canon/%s.js (restaged by #305 K from the rebuilt v1.0.14 pack) */\n%s\n</script>" % (m.group(1), body)
    open(f, "w").write(pat.sub(rep, s))
print("inlined engine blocks replaced:", n)
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
srv = socketserver.TCPServer(("127.0.0.1", 0), functools.partial(Q, directory="/")); port = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
url = lambda p: "http://127.0.0.1:%d%s" % (port, p)
res = {}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ.get("RENDER_SHELL"), args=["--no-sandbox"])
    def page():
        ctx = b.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=1, reduced_motion="reduce")
        pg = ctx.new_page(); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)[:160])); pg.on("dialog", lambda x: x.dismiss())
        return ctx, pg, errs
    # (1) overview, as R4s2 shot it
    ctx, pg, errs = page()
    pg.goto(url(ST + "/out/index.html"), wait_until="load", timeout=30000); pg.wait_for_timeout(1800)
    pg.add_style_tag(content=R4S.RELEASE); pg.wait_for_timeout(300)
    pg.evaluate("() => window.dispatchEvent(new Event('resize'))"); pg.wait_for_timeout(900)
    pg.screenshot(path=OUT + "/v1014-cand2-r3-overview-full-light.png", full_page=True)
    pg.evaluate("() => window.scrollTo(0,0)")
    dk = pg.evaluate(R4S.DARKCLICK); pg.wait_for_timeout(1400)
    dk["after"] = pg.evaluate("() => document.documentElement.getAttribute('data-theme')")
    pg.screenshot(path=OUT + "/v1014-cand2-r3-overview-full-dark.png", full_page=True)
    res["overview"] = {"dark_switch": dk, "pageerrors": errs}; ctx.close()
    # (2) one chart view
    ctx, pg, errs = page()
    pg.goto(url(ST + "/out/liquidity.html"), wait_until="load", timeout=30000); pg.wait_for_timeout(1800)
    pg.add_style_tag(content=R4S.RELEASE); pg.wait_for_timeout(300)
    pg.evaluate("() => window.dispatchEvent(new Event('resize'))"); pg.wait_for_timeout(900)
    pg.screenshot(path=OUT + "/v1014-cand2-r3-liquidity-full-light.png", full_page=True)
    res["liquidity"] = {"pageerrors": errs}; ctx.close()
    # (3) the pack's own showroom index
    for mode in ("light", "dark"):
        ctx, pg, errs = page()
        pg.goto(url(PACK + "/showroom/index.html"), wait_until="load", timeout=30000); pg.wait_for_timeout(1200)
        if mode == "dark":
            pg.click('[data-mode="dark"]'); pg.wait_for_timeout(800)   # the showroom's own light/dark control
        pg.screenshot(path=OUT + "/v1014-showroom-index-1440-%s.png" % mode)
        res["showroom-" + mode] = {"pageerrors": errs, "attrs": pg.evaluate("() => [...document.documentElement.attributes].map(a => a.name + '=' + a.value).join(' ')")}
        ctx.close()
    b.close()
json.dump(res, open(OUT + "/shots.json", "w"), indent=1)
print(json.dumps(res)[:1500])
