"""#314 AC1 - seat renders for s313-D58 (borders back all round on every floating surface but the
mega menu). Each restored surface OPEN, four themes x light/dark, real HSBC face, showroom pages over
http from the repo root (the #313 BV / #314 BR method, page.goto, never set_content). Each shot is
clipped to the trigger + open panel with a margin; computed borders go to facts.json.
Run from the repo root at the seat:  python3 notes/_lanes/314/AC1/ac1_render.py [slug ...]
Writes notes/_lanes/314/AC1/renders/<slug>-<theme>-<mode>.png and notes/_lanes/314/AC1/facts.json."""
import functools, http.server, json, os, socketserver, sys, threading, time
from playwright.sync_api import sync_playwright
ROOT = os.getcwd(); HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "renders")
os.makedirs(OUT, exist_ok=True)
THEMES = ["mono", "legacy", "console", "supercharge"]; MODES = ["light", "dark"]
NOANIM = "*{transition:none!important;animation:none!important;caret-color:transparent!important}"
PAD = 28
# (slug, plain label, page, trigger selector, how to open, panel selector or None = trigger's aria-controls, width)
CASES = [
  ("mega", "Mega menu (bottom edge only, for contrast)", "navigations.html", 'button[aria-controls="navMegaPayments"]', "click", "#navMegaPayments", 1280),
  ("nav-flyout", "Top nav flyout (Cards)", "navigations.html", 'button[aria-controls="navFlyCards"]', "click", "#navFlyCards", 1280),
  ("nav-account", "Top nav account menu", "navigations.html", "#navAcctTrig", "click", "#navAcctMenu", 1280),
  ("dropdown", "Dropdown", "dropdown.html", "#ddTrigger1", "click", None, 960),
  ("account-selector", "Account selector", "account-selector.html", "#asTrigger", "click", None, 960),
  ("avatar-group", "Avatar group overflow", "avatar-group.html", "#avgMoreTrig", "click", None, 960),
  ("card-header", "Card header actions menu", "card-header-lockup.html", "#chTrig1", "click", None, 960),
  ("cascader", "Cascader", "cascader.html", "#cs1-field", "click", None, 960),
  ("combobox", "Combobox", "combobox.html", "#cb1-input", "focus-down", None, 960),
  ("multi-select", "Multi-select", "multi-select.html", "#ms1-input", "focus-down", None, 960),
  ("filter-toolbar", "Filter toolbar add-filter menu", "filter-toolbar-bar.html", "#ftbAddT", "click", None, 1100),
  ("headers", "Header more-options menu", "headers.html", "#hdrMoreTrig", "click", None, 1100),
  ("split-button", "Split button menu", "split-button.html", ".sb-caret", "click", None, 960),
  ("time-picker", "Time picker (open specimen)", "time-picker.html", None, "static", ".tp-menu.is-static", 960),
]
DASH = ("dashboard-account", "Banking dashboard account menu", "dashboards/international-banking-dashboard.canon.html", "#accountTrigger", "click", "#accountMenu", 1440)

MEASURE = """([psel, tsel]) => {
  const p = document.querySelector(psel); if (!p) return {err: 'no panel ' + psel};
  const s = getComputedStyle(p), r = p.getBoundingClientRect();
  let tr = null; if (tsel) { const t = document.querySelector(tsel); if (t) { const q = t.getBoundingClientRect(); tr = [q.x, q.y, q.width, q.height]; } }
  return {top: s.borderTopWidth + ' ' + s.borderTopColor, right: s.borderRightWidth + ' ' + s.borderRightColor,
          bottom: s.borderBottomWidth + ' ' + s.borderBottomColor, left: s.borderLeftWidth + ' ' + s.borderLeftColor,
          shadow: s.boxShadow, rect: [r.x, r.y, r.width, r.height], trig: tr, visible: r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.opacity !== '0',
          font: getComputedStyle(p).fontFamily.slice(0, 60),
          loaded: [...new Set([...document.fonts].filter(f => f.status === 'loaded').map(f => f.family.replace(/["']/g, '')))].slice(0, 4)};
}"""

def serve(root):
    class Q(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a, **k): pass
    h = socketserver.ThreadingTCPServer(("127.0.0.1", 0), functools.partial(Q, directory=root))
    h.daemon_threads = True; threading.Thread(target=h.serve_forever, daemon=True).start()
    return h, "http://127.0.0.1:%d" % h.server_address[1]

def open_it(pg, ctx, trig, how):
    if how == "click":
        ctx.locator(trig).first.click()
    elif how == "focus-down":
        ctx.locator(trig).first.focus(); pg.wait_for_timeout(100); pg.keyboard.press("ArrowDown")
    pg.wait_for_timeout(350)

def panel_sel(ctx, trig, psel):
    if psel: return psel
    pid = ctx.evaluate("(s)=>{const t=document.querySelector(s);return t&&t.getAttribute('aria-controls')}", trig)
    return "#" + pid if pid else None

def shoot(pg, ctx, name, psel, trig, w, offset):
    f = ctx.evaluate(MEASURE, [psel, trig])
    if "err" in f: return f
    x, y, ww, hh = f["rect"]
    x0, y0, x1, y1 = x, y, x + ww, y + hh
    if f.get("trig"):
        tx, ty, tw, th = f["trig"]; x0, y0, x1, y1 = min(x0, tx), min(y0, ty), max(x1, tx + tw), max(y1, ty + th)
    ox, oy = offset
    cx = max(0, ox + x0 - PAD); cy = max(0, oy + y0 - PAD)
    cw = min(x1 - x0 + 2 * PAD, w - cx); ch = y1 - y0 + 2 * PAD
    need = int(cy + ch + 10)
    if need > pg.viewport_size["height"]:
        pg.set_viewport_size({"width": w, "height": need}); pg.wait_for_timeout(150)
    pg.screenshot(path=os.path.join(OUT, name + ".png"), clip={"x": cx, "y": cy, "width": cw, "height": ch})
    return f

def showroom_case(pg, base, case, t, m):
    slug, label, page, trig, how, psel, w = case
    pg.set_viewport_size({"width": w, "height": 900}); pg.goto("about:blank")
    pg.goto(f"{base}/showroom/{page}#theme={t}&m={m}&chrome=0", wait_until="load"); pg.wait_for_timeout(450)
    fr = pg.frames[1]; fr.wait_for_load_state("load")
    fr.evaluate("([t,m])=>{document.documentElement.setAttribute('data-apollo-theme',t);document.body.setAttribute('data-theme',m);}", [t, m])
    fr.add_style_tag(content=NOANIM)
    try: fr.evaluate("()=>document.fonts.ready.then(()=>1)")
    except Exception: pass
    if trig: open_it(pg, fr, trig, how)
    ps = panel_sel(fr, trig, psel) if trig else psel
    if not ps: return {"err": "no panel id"}
    fb = pg.locator("#f").bounding_box()
    # grow the viewport first so the frame is tall enough, then re-measure
    h = fr.evaluate("()=>Math.ceil(Math.max(document.body.scrollHeight, document.documentElement.scrollHeight))")
    if h + 40 > 900:
        pg.set_viewport_size({"width": w, "height": min(h + 60, 2400)}); pg.wait_for_timeout(200); fb = pg.locator("#f").bounding_box()
    return shoot(pg, fr, f"{slug}-{t}-{m}", ps, trig, w, (fb["x"], fb["y"]))

def dash_case(pg, base, t, m):
    slug, label, path, trig, how, psel, w = DASH
    pg.set_viewport_size({"width": w, "height": 900}); pg.goto("about:blank")
    pg.goto(f"{base}/{path}", wait_until="load"); pg.wait_for_timeout(900)
    pg.evaluate("([t,m])=>{document.documentElement.setAttribute('data-apollo-theme',t);document.body.setAttribute('data-theme',m);}", [t, m])
    pg.add_style_tag(content=NOANIM)
    try: pg.evaluate("()=>document.fonts.ready.then(()=>1)")
    except Exception: pass
    pg.evaluate("()=>window.scrollTo(0,0)")
    open_it(pg, pg, trig, how)
    return shoot(pg, pg, f"{slug}-{t}-{m}", psel, trig, w, (0, 0))

def main(only):
    httpd, base = serve(ROOT); t0 = time.time()
    fp = os.path.join(HERE, "facts.json")
    facts = json.load(open(fp)) if os.path.exists(fp) else {}
    with sync_playwright() as p:
        kw = {"args": ["--no-sandbox"]}
        if os.environ.get("RENDER_SHELL"): kw["executable_path"] = os.environ["RENDER_SHELL"]
        b = p.chromium.launch(**kw)
        pg = b.new_page(viewport={"width": 960, "height": 900}, device_scale_factor=2, reduced_motion="reduce")
        for case in CASES + [DASH]:
            if only and case[0] not in only: continue
            for t in THEMES:
                for m in MODES:
                    name = f"{case[0]}-{t}-{m}"
                    try:
                        f = dash_case(pg, base, t, m) if case is DASH else showroom_case(pg, base, case, t, m)
                    except Exception as e:
                        f = {"err": str(e)[:200]}
                    facts[name] = f
        b.close()
    httpd.shutdown()
    json.dump(facts, open(fp, "w"), indent=1)
    print(len(facts), "facts", round(time.time() - t0), "s")
    for k, v in facts.items():
        if only and not any(k.startswith(o + "-") for o in only): continue
        print(k, v.get("err") or (v["top"].split()[0], v["right"].split()[0], v["bottom"].split()[0], v["left"].split()[0], v["bottom"].split(" ", 1)[1], "vis" if v.get("visible") else "HIDDEN", v.get("font", "")[:24]))

if __name__ == "__main__":
    main(sys.argv[1:])
