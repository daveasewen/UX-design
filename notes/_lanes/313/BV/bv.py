"""#313 lane BV — seat renders of tonight's landed work in the four themes (mono, legacy=Common,
supercharge, console), light and dark, real HSBC face. Showroom pages over http from the repo root,
theme and mode set the page's own way (#theme=..&m=..&chrome=0) and asserted on the part's frame
(the B6 driver's method). Run from the repo root at the seat:
  python3 notes/_lanes/313/BV/bv.py <a|b|c|d>
Writes notes/_lanes/313/BV/img/*.png and facts-<batch>.json. Pictures only; nothing is fixed here."""
import functools, http.server, json, os, socketserver, sys, threading, time
from playwright.sync_api import sync_playwright
ROOT = os.getcwd(); HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "img")
os.makedirs(OUT, exist_ok=True)
THEMES = ["mono", "legacy", "supercharge", "console"]; MODES = ["light", "dark"]
NOANIM = "*{transition:none!important;animation:none!important;caret-color:transparent!important}"
FONTS = """() => { const b = getComputedStyle(document.body).fontFamily;
  const loaded = [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family.replace(/["']/g,''));
  return {family: b, loaded: [...new Set(loaded)].slice(0,6)}; }"""

def serve(root):
    class Q(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a, **k): pass
    h = socketserver.ThreadingTCPServer(("127.0.0.1", 0), functools.partial(Q, directory=root))
    h.daemon_threads = True
    threading.Thread(target=h.serve_forever, daemon=True).start()
    return h, "http://127.0.0.1:%d" % h.server_address[1]

facts = {}
def part(pg, base, page, theme, mode, name, w=960, act=None, maxh=1500):
    pg.set_viewport_size({"width": w, "height": 900})
    pg.goto("about:blank")
    pg.goto(f"{base}/showroom/{page}#theme={theme}&m={mode}&chrome=0", wait_until="load")
    pg.wait_for_timeout(450)
    fr = pg.frames[1]; fr.wait_for_load_state("load")
    fr.evaluate("([t,m])=>{document.documentElement.setAttribute('data-apollo-theme',t);document.body.setAttribute('data-theme',m);}", [theme, mode])
    fr.add_style_tag(content=NOANIM)
    try: fr.evaluate("()=>document.fonts.ready.then(()=>1)")
    except Exception: pass
    note = None
    if act:
        try: note = act(pg, fr)
        except Exception as e: note = "ACTION FAILED: " + str(e)[:160]
    pg.wait_for_timeout(200)
    h = fr.evaluate("()=>Math.ceil(Math.max(document.body.scrollHeight, document.documentElement.scrollHeight))")
    pg.set_viewport_size({"width": w, "height": max(240, min(h + 40, maxh))})
    pg.wait_for_timeout(150)
    fn = os.path.join(OUT, name + ".png")
    pg.locator("#f").screenshot(path=fn)
    f = fr.evaluate(FONTS); f.update({"theme_on_frame": fr.evaluate("()=>document.documentElement.getAttribute('data-apollo-theme')+'/'+document.body.getAttribute('data-theme')")})
    if note: f["action"] = note
    facts[name] = f

def sweep(pg, base, page, slug, **kw):
    for t in THEMES:
        for m in MODES:
            part(pg, base, page, t, m, f"{slug}-{t}-{m}", **kw)

def open_mega(pg, fr):
    fr.locator('button[aria-controls="navMegaPayments"]').click(); pg.wait_for_timeout(250)
    return fr.evaluate("()=>{const p=document.getElementById('navMegaPayments');if(!p)return 'no panel';const s=getComputedStyle(p);return 'mega hidden='+p.hidden+' borderTop='+s.borderTopWidth+' borderBottom='+s.borderBottom+' w='+Math.round(p.getBoundingClientRect().width)}")
def open_acct(pg, fr):
    fr.locator('#navAcctTrig').click(); pg.wait_for_timeout(250)
    return fr.evaluate("()=>{const p=document.getElementById('navAcctMenu');if(!p)return 'no menu';const s=getComputedStyle(p);return 'acct hidden='+p.hidden+' borderTop='+s.borderTopWidth+' borderBottom='+s.borderBottom}")
def open_dd(pg, fr):
    b = fr.locator('button[aria-expanded="false"]').first; b.click(); pg.wait_for_timeout(250)
    return fr.evaluate("()=>{const t=document.querySelector('[aria-expanded=\"true\"]');if(!t)return 'nothing expanded';const id=t.getAttribute('aria-controls');const p=id&&document.getElementById(id);if(!p)return 'expanded, no panel id';const s=getComputedStyle(p);return 'panel '+id+' borderTop='+s.borderTopWidth+' borderBottom='+s.borderBottom}")
def tab_focus(pg, fr):
    pg.mouse.click(5, 5); pg.keyboard.press("Tab"); pg.wait_for_timeout(150)
    return fr.evaluate("()=>{const a=document.activeElement;if(!a||a===document.body)return 'no focus in frame';const s=getComputedStyle(a);return 'focused '+a.tagName+'.'+a.className+' fv='+a.matches(':focus-visible')+' outline='+s.outlineStyle+' '+s.outlineWidth+' '+s.outlineColor+' offset='+s.outlineOffset+' shadow='+s.boxShadow}")
def click_focus(pg, fr):
    b = fr.locator('button:visible').first; b.click(); pg.wait_for_timeout(150)
    return fr.evaluate("()=>{const a=document.activeElement;if(!a||a===document.body)return 'no focus';const s=getComputedStyle(a);return 'clicked '+a.tagName+'.'+a.className+' fv='+a.matches(':focus-visible')+' outline='+s.outlineStyle+' '+s.outlineWidth+' shadow='+s.boxShadow}")

def whole(pg, base, path, theme, mode, name, w=1440, h=900, html_mode=False):
    pg.set_viewport_size({"width": w, "height": h}); pg.goto("about:blank")
    pg.goto(f"{base}/{path}", wait_until="load"); pg.wait_for_timeout(900)
    pg.evaluate("([t,m,hm])=>{document.documentElement.setAttribute('data-apollo-theme',t);(hm?document.documentElement:document.body).setAttribute('data-theme',m);if(hm)document.body.setAttribute('data-theme',m);}", [theme, mode, html_mode])
    pg.add_style_tag(content=NOANIM); pg.wait_for_timeout(500)
    pg.screenshot(path=os.path.join(OUT, name + ".png"))
    f = pg.evaluate(FONTS); facts[name] = f

def main(batch):
    httpd, base = serve(ROOT); t0 = time.time()
    with sync_playwright() as p:
        kw = {"args": ["--no-sandbox"]}
        if os.environ.get("RENDER_SHELL"): kw["executable_path"] = os.environ["RENDER_SHELL"]
        b = p.chromium.launch(**kw)
        pg = b.new_page(viewport={"width": 960, "height": 900}, device_scale_factor=1, reduced_motion="reduce")
        if batch == "a":
            for page, slug in [("notifications.html", "notifications"), ("hero.html", "hero"), ("button.html", "button"),
                               ("split-button.html", "split-button"), ("back-to-top.html", "back-to-top"), ("tree.html", "tree")]:
                sweep(pg, base, page, slug)
        elif batch == "b":
            for page, slug in [("calendar.html", "calendar"), ("date-picker.html", "date-picker"), ("slider.html", "slider"),
                               ("range-slider.html", "range-slider"), ("transfer-list.html", "transfer-list"), ("rating.html", "rating"),
                               ("tabs.html", "tabs"), ("qr-code.html", "qr-code")]:
                sweep(pg, base, page, slug)
        elif batch == "c":
            sweep(pg, base, "navigations.html", "nav-mega", w=1440, act=open_mega, maxh=900)
            sweep(pg, base, "navigations.html", "nav-account", w=1440, act=open_acct, maxh=700)
            sweep(pg, base, "dropdown.html", "dropdown-open", act=open_dd, maxh=900)
            for t in THEMES:
                part(pg, base, "button.html", t, "light", f"focus-tab-{t}-light", act=tab_focus, maxh=700)
                part(pg, base, "button.html", t, "light", f"focus-click-{t}-light", act=click_focus, maxh=700)
                part(pg, base, "button.html", t, "dark", f"focus-tab-{t}-dark", act=tab_focus, maxh=700)
        elif batch == "d":
            for t in THEMES:
                for m in MODES:
                    whole(pg, base, "dashboards/international-banking-dashboard.canon.html", t, m, f"demo-{t}-{m}")
                    whole(pg, base, "knowledge/_fitness-test/canon-gallery.canon.html", t, m, f"gallery-{t}-{m}", h=1800, html_mode=True)
        b.close()
    httpd.shutdown()
    json.dump(facts, open(os.path.join(HERE, f"facts-{batch}.json"), "w"), indent=1)
    print(batch, len(facts), "shots", round(time.time() - t0), "s")
    for k, v in facts.items():
        if "action" in v: print(k, "|", v["action"][:200])
    print("fonts sample:", json.dumps(next(iter(facts.values())))[:300])

if __name__ == "__main__":
    main(sys.argv[1])
