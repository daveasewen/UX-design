#!/usr/bin/env python3
"""render_titles.py REPO_ROOT OUTDIR — #304 W5c: serve REPO_ROOT, open notes/_KG-EXPLORER.html at 1440,
and LOOK at the titles: the default canvas, a search, a ruling's panel and INSPECT, a session's INSPECT
(the 'What was ruled' tab now reads the id). Prints the page's own facts and every page error."""
import os, sys, json, threading, functools, http.server, socketserver
if any(a in ("-h", "--help") for a in sys.argv[1:]):
    print(__doc__); sys.exit(0)
from playwright.sync_api import sync_playwright
root, out = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2]); os.makedirs(out, exist_ok=True)
H = functools.partial(http.server.SimpleHTTPRequestHandler, directory=root)
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
srv = socketserver.TCPServer(("127.0.0.1", 0), functools.partial(Q, directory=root)); port = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
url = "http://127.0.0.1:%d/notes/_KG-EXPLORER.html" % port
F = {}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ["RENDER_SHELL"], headless=True,
                          args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"])
    pg = b.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
    errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(url); pg.wait_for_timeout(3000)
    F["version"] = pg.evaluate("KG.version")
    F["sample_labels"] = pg.evaluate("""() => ['ruling:s133-D1','ruling:s245-D10','rule:dv-line-008','rule:aca-007','session:165','sc:1.4.8']
        .map(i => { const n = KG.nodes.find(x => x.id === i); return n ? [i, n.label, n.titleFrom || ''] : [i, 'ABSENT'] })""")
    pg.screenshot(path=os.path.join(out, "kg-default-1440.png"))
    def search(s, shot):
        pg.fill("#q", ""); pg.type("#q", s, delay=20); pg.wait_for_timeout(600)
        hits = pg.evaluate("() => [...document.querySelectorAll('#hits .hit')].slice(0,12).map(h => h.innerText.replace(/\\s+/g,' ').trim())")
        pg.screenshot(path=os.path.join(out, shot)); return hits
    F["search_palette"] = search("palette", "kg-search-palette-1440.png")
    F["search_code_s133"] = search("s133", "kg-search-s133-1440.png")
    # choose the first RULING hit for "s133-D1"
    search("s133-D1", "kg-search-s133-D1-1440.png")
    pg.evaluate("() => { const hs=[...document.querySelectorAll('#hits .hit')]; const h=hs.find(x=>x.querySelector('small') && x.querySelector('small').textContent==='ruling'); h.click() }")
    pg.wait_for_timeout(2200)
    F["panel_head"] = pg.evaluate("() => { const a=document.querySelector('aside .head'); return a ? a.innerText.replace(/\\s+/g,' ').slice(0,300) : 'no aside head' }")
    F["panel_rel_rows"] = pg.evaluate("() => [...document.querySelectorAll('aside .rel .n')].slice(0,8).map(x=>x.innerText.replace(/\\s+/g,' '))")
    pg.screenshot(path=os.path.join(out, "kg-ruling-panel-s133-D1-1440.png"))
    pg.keyboard.press("i"); pg.wait_for_timeout(1800)
    F["inspect_ruling"] = pg.evaluate("() => { const m=document.getElementById('insp'); return m && m.classList.contains('on') ? m.innerText.replace(/\\s+/g,' ').slice(0,700) : 'modal not open' }")
    pg.screenshot(path=os.path.join(out, "kg-ruling-inspect-s133-D1-1440.png"))
    pg.keyboard.press("Escape"); pg.wait_for_timeout(400)
    search("#165", "kg-search-session-1440.png")
    pg.evaluate("() => { const hs=[...document.querySelectorAll('#hits .hit')]; const h=hs.find(x=>x.querySelector('small') && x.querySelector('small').textContent==='session'); h.click() }")
    pg.wait_for_timeout(2200)
    F["session_panel_head"] = pg.evaluate("() => { const a=document.querySelector('aside .head'); return a ? a.innerText.replace(/\\s+/g,' ').slice(0,200) : 'none' }")
    pg.keyboard.press("i"); pg.wait_for_timeout(2000)
    F["inspect_session"] = pg.evaluate("() => { const m=document.getElementById('insp'); return m && m.classList.contains('on') ? m.innerText.replace(/\\s+/g,' ').slice(0,900) : 'modal not open' }")
    F["session_tab_count"] = pg.evaluate("() => { const f=[...document.querySelectorAll('#insp .fnote')].map(x=>x.innerText).find(t=>/carry this session|names session/.test(t)); return f || 'no session tab note' }")
    pg.screenshot(path=os.path.join(out, "kg-session-inspect-165-1440.png"))
    F["pageerrors"] = errs
    b.close()
srv.shutdown()
print(json.dumps(F, ensure_ascii=False, indent=1))
