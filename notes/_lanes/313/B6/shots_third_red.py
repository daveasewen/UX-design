"""#313 B6 — the third red (W-308ia): the candidates, drawn on the real part.

Loads the showroom pages over http from the repo root (showroom/notifications.html, alert.html,
banner.html), sets theme and mode the page's own way (its #theme=…&m=…&chrome=0 hash), and for
the candidates injects ONE override <style> into the part's own frame — the part's markup and
its own CSS are untouched, so each picture is the real part with one rule changed. Only the
error placements are kept in view (the other variants are hidden), so the red is the subject.
Writes img/*.png and measures.json beside this file. CLOUD render: Chromium with substituted
fonts (Univers is not on this box) — colours are exact, type is not; the seat re-renders.

Run from the repo root:  python3 notes/_lanes/313/B6/shots_third_red.py
"""
import functools, http.server, json, os, socketserver, threading
from playwright.sync_api import sync_playwright

ROOT = os.getcwd()
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img")
os.makedirs(OUT, exist_ok=True)

ERR_ONLY = """
.spec-h, h2, .note:not(.err), .inline:not(.err), br { display:none !important; }
.nwrap { padding-top:4px; }
.inline.err { display:flex !important; margin:12px 0 !important; }
"""
# B — fold into mono's reds by the rules on record (values are mono's own canon tokens):
#   contextual: accent var(--rag-error) #F6604C on var(--rag-error-tint)  (what mono's Alert paints)
#   global bar: fill #F6604C, type and icon #1A1A1A                      (s149-D1, what mono's Banner paints)
#   inline icon on the white page: var(--rag-error-ink) #DA1A00 light     (s151-D1 (2): red atoms on white)
#   dark: the snippet's own roundel policy keeps contextual and inline icons white; only the bar shows red
FOLD = """
[data-theme="light"]{ --err:#F6604C; --err-t:#FDD9D4; }
[data-theme="dark"] { --err:#F6604C; --err-t:#60302A; }
.err{ --gtext:#1A1A1A; }
.note.global.err .actions button:hover{ background:rgba(255,255,255,.08); }
.note.global.err .actions button:active{ background:rgba(255,255,255,.14); }
[data-theme="light"] .inline.err .ic{ color:#DA1A00; }
"""

def serve(root):
    class Q(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a, **k): pass
    h = socketserver.TCPServer(("127.0.0.1", 0), functools.partial(Q, directory=root))
    threading.Thread(target=h.serve_forever, daemon=True).start()
    return h, "http://127.0.0.1:%d" % h.server_address[1]

PROBE = """() => {
  const q = (s) => [...document.querySelectorAll(s)];
  const pick = (el, prop) => el ? getComputedStyle(el)[prop] : null;
  const g = document.querySelector('.note.global.err, .banner.err');
  const c = document.querySelector('.note.tint.err, .alert.err');
  const i = document.querySelector('.inline.err .ic');
  return {
    page: getComputedStyle(document.body).backgroundColor,
    bar_fill: pick(g, 'backgroundColor'), bar_text: pick(g, 'color'),
    ctx_fill: pick(c, 'backgroundColor'), ctx_icon: pick(c && c.querySelector('.ic, svg'), 'color'),
    inline_icon: pick(i, 'color')
  };
}"""

def shot(pg, base, page, theme, mode, css, name, measures):
    pg.goto("about:blank")   # a hash-only change is a same-document navigation: the frame would keep the last shot's style
    pg.goto(f"{base}/showroom/{page}#theme={theme}&m={mode}&chrome=0", wait_until="load")
    pg.wait_for_timeout(500)
    frame = pg.frames[1]
    frame.wait_for_load_state("load")
    frame.evaluate("([t,m])=>{document.documentElement.setAttribute('data-apollo-theme',t);"
                   "document.body.setAttribute('data-theme',m);}", [theme, mode])
    if css:
        frame.add_style_tag(content=css)
    frame.add_style_tag(content="*{transition:none!important;animation:none!important}")
    pg.wait_for_timeout(200)
    measures[name] = frame.evaluate(PROBE)
    h = frame.evaluate("()=>Math.ceil(document.querySelector('.nwrap, main, body').getBoundingClientRect().bottom)+24")
    pg.set_viewport_size({"width": 640, "height": max(200, min(h + 60, 1400))})
    pg.wait_for_timeout(150)
    pg.locator("#f").screenshot(path=os.path.join(OUT, name + ".png"))

def main():
    httpd, base = serve(ROOT)
    measures = {}
    with sync_playwright() as p:
        kw = {"args": ["--no-sandbox"]}
        if os.environ.get("RENDER_SHELL"):          # the seat's own Chromium (knowledge/_render/seat_env.sh)
            kw["executable_path"] = os.environ["RENDER_SHELL"]
        b = p.chromium.launch(**kw)
        pg = b.new_page(viewport={"width": 640, "height": 900}, device_scale_factor=1)
        for mode in ("light", "dark"):
            shot(pg, base, "notifications.html", "mono", mode, ERR_ONLY, f"A-mono-{mode}", measures)
            shot(pg, base, "notifications.html", "mono", mode, ERR_ONLY + FOLD, f"B-mono-{mode}", measures)
            shot(pg, base, "notifications.html", "legacy", mode, ERR_ONLY, f"ref-common-{mode}", measures)
            shot(pg, base, "alert.html", "mono", mode, ".alert:not(.err), h2, .spec-h{display:none!important}", f"C-mono-alert-{mode}", measures)
            shot(pg, base, "banner.html", "mono", mode, ".banner:not(.err), h2, .spec-h{display:none!important}", f"C-mono-banner-{mode}", measures)
        b.close()
    httpd.shutdown()
    json.dump(measures, open(os.path.join(os.path.dirname(OUT), "measures.json"), "w"), indent=1)
    print(json.dumps(measures, indent=1))

if __name__ == "__main__":
    main()
