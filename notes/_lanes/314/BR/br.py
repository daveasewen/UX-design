"""#314 BR — seat renders for s313-D58 (borders back all round on every floating surface but the
mega menu). Four themes x light/dark, real HSBC face, showroom pages over http (the #313 BV method).
Run from the repo root at the seat: python3 notes/_lanes/314/BR/br.py
Writes notes/_lanes/314/BR/img/*.png (each open panel clipped with a margin) and facts.json."""
import functools, http.server, json, os, socketserver, threading
from playwright.sync_api import sync_playwright
ROOT = os.getcwd(); HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "img")
os.makedirs(OUT, exist_ok=True)
THEMES = ["mono", "legacy", "supercharge", "console"]; MODES = ["light", "dark"]
NOANIM = "*{transition:none!important;animation:none!important;caret-color:transparent!important}"
CASES = [  # (slug, showroom page, trigger selector, panel id, width)
  ("mega", "navigations.html", 'button[aria-controls="navMegaPayments"]', "navMegaPayments", 1280),
  ("flyout", "navigations.html", 'button[aria-controls="navFlyCards"]', "navFlyCards", 1280),
  ("account", "navigations.html", '#navAcctTrig', "navAcctMenu", 1280),
  ("dropdown", "dropdown.html", 'button[aria-controls="ddMenu1"]', "ddMenu1", 960),
  ("split", "split-button.html", 'button[aria-controls="sbMenu1"]', "sbMenu1", 960),
]
def serve(root):
    class Q(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a, **k): pass
    h = socketserver.ThreadingTCPServer(("127.0.0.1", 0), functools.partial(Q, directory=root))
    h.daemon_threads = True; threading.Thread(target=h.serve_forever, daemon=True).start()
    return h, "http://127.0.0.1:%d" % h.server_address[1]
def main():
    httpd, base = serve(ROOT); facts = {}
    with sync_playwright() as p:
        br = p.chromium.launch(executable_path=os.environ["RENDER_SHELL"]); pg = br.new_page(device_scale_factor=2)
        for slug, page, trig, pid, w in CASES:
            for t in THEMES:
                for m in MODES:
                    name = f"{slug}-{t}-{m}"
                    pg.set_viewport_size({"width": w, "height": 900}); pg.goto("about:blank")
                    pg.goto(f"{base}/showroom/{page}#theme={t}&m={m}&chrome=0", wait_until="load"); pg.wait_for_timeout(450)
                    fr = pg.frames[1]; fr.wait_for_load_state("load")
                    fr.evaluate("([t,m])=>{document.documentElement.setAttribute('data-apollo-theme',t);document.body.setAttribute('data-theme',m);}", [t, m])
                    fr.add_style_tag(content=NOANIM)
                    try: fr.evaluate("()=>document.fonts.ready.then(()=>1)")
                    except Exception: pass
                    try:
                        fr.locator(trig).first.click(); pg.wait_for_timeout(300)
                        f = fr.evaluate("""(id)=>{const p=document.getElementById(id);if(!p)return {err:'no panel'};
                          const s=getComputedStyle(p),r=p.getBoundingClientRect();
                          return {top:s.borderTopWidth+' '+s.borderTopColor,right:s.borderRightWidth+' '+s.borderRightColor,
                                  bottom:s.borderBottomWidth+' '+s.borderBottomColor,left:s.borderLeftWidth+' '+s.borderLeftColor,
                                  shadow:s.boxShadow,rect:[r.x,r.y,r.width,r.height],font:getComputedStyle(document.body).fontFamily.slice(0,40)}}""", pid)
                    except Exception as e:
                        f = {"err": str(e)[:200]}
                    facts[name] = f
                    fb = pg.locator("#f").bounding_box()
                    if fb and "rect" in f:
                        x, y, ww, hh = f["rect"]; pad = 28
                        cx = max(0, fb["x"] + x - pad); cy = max(0, fb["y"] + y - pad)
                        cw = min(ww + 2 * pad, w - cx); ch = hh + 2 * pad
                        pg.set_viewport_size({"width": w, "height": int(max(900, cy + ch + 10))}); pg.wait_for_timeout(100)
                        pg.screenshot(path=os.path.join(OUT, name + ".png"), clip={"x": cx, "y": cy, "width": cw, "height": ch})
        br.close()
    httpd.shutdown()
    json.dump(facts, open(os.path.join(HERE, "facts.json"), "w"), indent=1)
    for k, v in facts.items(): print(k, v.get("err") or (v["top"].split()[0], v["right"].split()[0], v["bottom"], v["left"].split()[0]))
main()
