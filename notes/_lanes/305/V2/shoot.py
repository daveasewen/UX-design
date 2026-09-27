"""V2 (#305): the real v1.0.14 zip, unzipped, looked at cold beside v1.0.13.
Serves both unzipped packs over http and shoots the showroom index, kpi-tile, chart-line,
template-dashboard-bento, navigations and the logos foundation page at 1440x900 @1x, light and
dark (the showroom's own [data-mode] control). Records page errors, failed requests and broken
<img> elements. Writes only under notes/_lanes/305/V2/renders/."""
import functools, http.server, json, os, socketserver, sys, threading
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "renders"); os.makedirs(OUT, exist_ok=True)
from playwright.sync_api import sync_playwright
PACKS = {"v14": os.path.join(HERE, "cold/Apollo-Spider-v1.0.14"),
         "v13": os.path.join(HERE, "cold13/Apollo-Spider-v1.0.13")}
PAGES = ["showroom/index.html", "showroom/kpi-tile.html", "showroom/chart-line.html",
         "showroom/template-dashboard-bento.html", "showroom/navigations.html",
         "showroom/_foundations/logos.html"]
only = sys.argv[1:]  # optional: page substrings to shoot
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
srv = socketserver.TCPServer(("127.0.0.1", 0), functools.partial(Q, directory="/")); port = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
url = lambda p: "http://127.0.0.1:%d%s" % (port, p)
res = {}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ.get("RENDER_SHELL"), args=["--no-sandbox"])
    for tag, pack in PACKS.items():
        for page in PAGES:
            if only and not any(o in page for o in only): continue
            slug = page.replace("showroom/", "").replace("_foundations/", "").replace(".html", "")
            for mode in ("light", "dark"):
                ctx = b.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=1, reduced_motion="reduce")
                pg = ctx.new_page(); errs = []; failed = []
                pg.on("pageerror", lambda e: errs.append(str(e)[:200]))
                pg.on("requestfailed", lambda r: failed.append(r.url[-90:]))
                pg.on("response", lambda r: failed.append("%d %s" % (r.status, r.url[-90:])) if r.status >= 400 else None)
                pg.on("dialog", lambda x: x.dismiss())
                pg.goto(url(os.path.join(pack, page)), wait_until="load", timeout=45000); pg.wait_for_timeout(1500)
                if mode == "dark":
                    try: pg.click('[data-mode="dark"]', timeout=3000); pg.wait_for_timeout(900)
                    except Exception as e: errs.append("no dark control: " + str(e)[:80])
                broken = pg.evaluate("() => [...document.images].filter(i => i.complete && i.naturalWidth === 0).map(i => i.getAttribute('src'))")
                name = "%s-%s-1440-%s" % (tag, slug, mode)
                pg.screenshot(path=os.path.join(OUT, name + ".png"))
                pg.screenshot(path=os.path.join(OUT, name + "-full.png"), full_page=True)
                res[name] = {"pageerrors": errs, "http>=400/failed": failed, "broken_imgs": broken,
                             "html_attrs": pg.evaluate("() => [...document.documentElement.attributes].map(a => a.name + '=' + a.value).join(' ')"),
                             "doc_h": pg.evaluate("() => document.documentElement.scrollHeight")}
                ctx.close()
                print(name, json.dumps({k: v for k, v in res[name].items() if k != 'html_attrs'})[:300], flush=True)
    b.close()
old = {}
jp = os.path.join(OUT, "shots.json")
if os.path.exists(jp): old = json.load(open(jp))
old.update(res); json.dump(old, open(jp, "w"), indent=1)
