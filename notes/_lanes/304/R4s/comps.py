"""comps.py — R4s (#304): distinct canon component scopes (cn-<slug>, visible, rendered) across all ten
destinations of each run, so v1.0.13's ten files and the candidates' ten views are counted the same way."""
import functools, http.server, json, os, socketserver, sys, threading, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from views import VIEWS, dest, STAGE, HERE
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
JS = r"""() => { const s = new Set(); for (const e of document.querySelectorAll('[class*="cn-"]')) { const r = e.getBoundingClientRect(); if (!r.width || !r.height) continue;
  for (const c of e.classList) if (c.startsWith('cn-')) s.add(c.slice(3)); } return [...s].sort(); }"""
if __name__ == "__main__":
    from playwright.sync_api import sync_playwright
    srv = socketserver.ThreadingTCPServer(("127.0.0.1", 0), functools.partial(Q, directory="/")); srv.daemon_threads=True
    threading.Thread(target=srv.serve_forever, daemon=True).start(); port=srv.server_address[1]
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=os.environ.get("RENDER_SHELL"), args=["--no-sandbox"])
        for run in sys.argv[1:]:
            base = "/" + os.path.relpath(os.path.join(STAGE, "cold-"+run, "out"), "/"); per = {}
            for v in VIEWS:
                pg = b.new_page(viewport={"width":1440,"height":1000})
                pg.goto("http://127.0.0.1:%d%s/%s" % (port, urllib.parse.quote(base), dest(run, v)), wait_until="load"); pg.wait_for_timeout(900)
                per[v] = pg.evaluate(JS); pg.close()
            allc = sorted(set(x for l in per.values() for x in l))
            json.dump({"run": run, "per_view": per, "all": allc}, open(os.path.join(HERE, "views", run, "comps.json"), "w"), indent=1)
            print(run, len(allc), "overview", len(per["overview"]), allc)
        b.close()
