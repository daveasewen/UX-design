"""views.py — R4s (#304) supplementary drive: every destination of every cold run, same measures.
The R4c harness renders the v1.0.13 runs' ten linked FILES but only the candidate runs' first VIEW
(their ten destinations live in one file behind ?view= / #/ routing). This drives all ten destinations
of all six runs the same way, from the harness's own stage copies ($HOME/r4c/stage/cold-<run>/out),
so the comparison is like for like. Nothing in the frozen outputs is touched.
Per destination at 1440x1000 @1x: charts with marks (types), charts cut by something OTHER than the
App-shell's 640px frame, visible table rows, prompt keywords in rendered text, page errors, and a
screenshot with the 640px shell frame released (declared: .sh height auto) so the whole view is seen.
Overview extra: the as-shipped 1440x1000 viewport (frame NOT released), the run's OWN dark switch
clicked (not forced) + dark shot, and a 390 as-shipped shot.
usage: python3 views.py <run> [<run>…]   (seat env sourced in the same call)"""
import functools, http.server, json, os, re, socketserver, sys, threading, time, urllib.parse
HERE = os.path.dirname(os.path.abspath(__file__))
STAGE = os.path.join(os.environ["HOME"], "r4c", "stage")
VIEWS = ["overview", "accounts", "liquidity", "payments", "fx", "risk", "trade", "reports", "messages", "settings"]
PROF = json.load(open(os.path.join(HERE, "..", "R4c", "harness", "profiles", "ceo-common.json")))
RELEASE = ".sh{height:auto!important;max-height:none!important;overflow:visible!important}" \
          ".sh-body{min-height:auto!important}.sh-content{overflow:visible!important}"

def dest(run, v):
    if run.startswith("v1013"):
        return "index.html" if v == "overview" else v + ".html"
    if run == "cand-r1":
        return "index.html?view=" + v
    return "index.html#/" + v

class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass

MEASURE = r"""() => {
 const vis = el => { const s = getComputedStyle(el), r = el.getBoundingClientRect();
   return s.display!=='none' && s.visibility!=='hidden' && r.width>0 && r.height>0 && !el.closest('[hidden],template'); };
 const desc = el => (el.tagName.toLowerCase()+(el.id?'#'+el.id:'')+(typeof el.className==='string'&&el.className.trim()?'.'+el.className.trim().split(/\s+/).slice(0,3).join('.'):'')).slice(0,80);
 const figs = [...document.querySelectorAll('figure.dv, figure[data-dv-type]')].filter(vis);
 const charts = figs.map(f => { const svg = f.querySelector('svg'); let marks = 0;
   if (svg) for (const e of svg.querySelectorAll('rect,path,circle,line,polyline,polygon,ellipse')) {
     const cl = e.getAttribute('class')||''; if (/dv-grid|dv-axis|dv-base|dv-tick/.test(cl) || e.closest('.dv-grid,.dv-axis,defs,clipPath,mask')) continue;
     const b = e.getBoundingClientRect(); if (b.width>0||b.height>0) marks++; }
   const t = svg ? svg.getBoundingClientRect() : f.getBoundingClientRect(); let clip = null;
   for (let a = f.parentElement; a && a !== document.body; a = a.parentElement) {
     const s = getComputedStyle(a); if (!/(hidden|clip)/.test(s.overflowX+' '+s.overflowY)) continue;
     const ar = a.getBoundingClientRect(); const ex = Math.max(ar.left-t.left, t.right-ar.right, ar.top-t.top, t.bottom-ar.bottom);
     if (ex > 2) { clip = {by: desc(a), px: Math.round(ex)}; break; } }
   const fr = f.getBoundingClientRect();
   return {type: f.getAttribute('data-dv-type') || (f.className.match(/dv-([a-z-]+)/)||[])[1] || '?', marks, clip,
           w: Math.round(fr.width), h: Math.round(fr.height)}; });
 const rows = Math.max(0, ...[...document.querySelectorAll('table')].filter(vis).map(t => [...t.querySelectorAll('tbody tr')].filter(vis).length));
 const main = document.querySelector('main') || document.body;
 return {charts, rows, text: (main.innerText||'').slice(0, 60000), h: document.documentElement.scrollHeight,
         hover: Math.max(0, document.documentElement.scrollWidth - innerWidth),
         theme: document.documentElement.getAttribute('data-theme'), apollo: document.documentElement.getAttribute('data-apollo-theme')};
}"""

DARKCLICK = r"""() => {
 const cands = [...document.querySelectorAll('button,[role=radio],[role=switch],[role=tab],label,a,input[type=radio],input[type=checkbox],[role=menuitemradio]')];
 const vis = el => { const r = el.getBoundingClientRect(); const s = getComputedStyle(el); return r.width>0 && r.height>0 && s.visibility!=='hidden'; };
 let hit = cands.find(e => vis(e) && /^\s*dark\s*$/i.test(e.innerText||e.value||''));
 if (!hit) hit = cands.find(e => vis(e) && /dark/i.test((e.getAttribute('aria-label')||'')+' '+(e.title||'')));
 if (!hit) { const lab = [...document.querySelectorAll('label')].find(l => /^\s*dark\s*$/i.test(l.innerText)); if (lab) hit = lab; }
 if (!hit) return {found: null};
 const before = document.documentElement.getAttribute('data-theme'); hit.click();
 return {found: (hit.tagName + ' ' + (hit.innerText||hit.getAttribute('aria-label')||'')).trim().slice(0,60), before};
}"""

def run_one(p, port, run, budget_end):
    base = "/" + os.path.relpath(os.path.join(STAGE, "cold-" + run, "out"), "/")
    od = os.path.join(HERE, "views", run); os.makedirs(od, exist_ok=True)
    res = {"run": run, "stage": base, "release_css": RELEASE, "views": {}}
    b = p.chromium.launch(executable_path=os.environ.get("RENDER_SHELL"), args=["--no-sandbox"])
    for v in VIEWS:
        if time.time() > budget_end: res["views"][v] = {"not_reached": True}; continue
        ctx = b.new_context(viewport={"width": 1440, "height": 1000}, device_scale_factor=1)
        pg = ctx.new_page(); errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)[:200])); pg.on("dialog", lambda d: d.dismiss())
        u = "http://127.0.0.1:%d%s/%s" % (port, urllib.parse.quote(base), dest(run, v))
        pg.goto(u, wait_until="load", timeout=30000); pg.wait_for_timeout(1500)
        if v == "overview":
            pg.screenshot(path=os.path.join(od, "overview-asshipped-1440.png"))
        pg.add_style_tag(content=RELEASE); pg.wait_for_timeout(300)
        pg.evaluate("() => window.dispatchEvent(new Event('resize'))"); pg.wait_for_timeout(700)
        m = pg.evaluate(MEASURE)
        text = m.pop("text"); low = text.lower()
        m["kpi_words"] = {k: bool(re.search(x, low)) for k, x in PROF["kpis"].items()}
        m["question_words"] = {k: bool(re.search(x, low)) for k, x in PROF["questions"].items()}
        m["title_words"] = bool(re.search(PROF["view_patterns"]["trade finance" if v == "trade" else v], low))
        m["pageerrors"] = errs; m["url"] = dest(run, v)
        h = min(m["h"], 6000)
        if v == "overview":
            pg.screenshot(path=os.path.join(od, "overview-full-light-1440.png"), full_page=True)
            pg.evaluate("() => window.scrollTo(0,0)")
            dk = pg.evaluate(DARKCLICK); pg.wait_for_timeout(1200)
            dk["after"] = pg.evaluate("() => document.documentElement.getAttribute('data-theme')")
            dk["body_bg"] = pg.evaluate("() => getComputedStyle(document.body).backgroundColor")
            dk["flips"] = dk.get("after") == "dark"
            m["dark_switch"] = dk
            if dk["flips"]:
                pg.screenshot(path=os.path.join(od, "overview-full-dark-1440.png"), full_page=True)
        else:
            pg.screenshot(path=os.path.join(od, "%s-full-light-1440.jpg" % v), full_page=True, type="jpeg", quality=70)
        res["views"][v] = m
        ctx.close()
    # 390 as shipped, overview
    if time.time() < budget_end:
        ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=1); pg = ctx.new_page()
        pg.goto("http://127.0.0.1:%d%s/%s" % (port, urllib.parse.quote(base), dest(run, "overview")), wait_until="load"); pg.wait_for_timeout(1500)
        pg.screenshot(path=os.path.join(od, "overview-asshipped-390.png"))
        res["overview_390_hoverflow"] = pg.evaluate("() => Math.max(0, document.documentElement.scrollWidth - innerWidth)")
        ctx.close()
    b.close()
    json.dump(res, open(os.path.join(od, "views.json"), "w"), indent=1)
    V = res["views"]
    ch = sum(len([c for c in x.get("charts", []) if c["marks"] > 0]) for x in V.values())
    types = sorted({c["type"] for x in V.values() for c in x.get("charts", []) if c["marks"] > 0})
    print("VIEWS %s charts=%d types=%d dark=%s" % (run, ch, len(types), (V.get("overview") or {}).get("dark_switch")))

if __name__ == "__main__":
    from playwright.sync_api import sync_playwright
    srv = socketserver.ThreadingTCPServer(("127.0.0.1", 0), functools.partial(Q, directory="/")); srv.daemon_threads = True
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    end = time.time() + float(os.environ.get("R4S_BUDGET", "160"))
    with sync_playwright() as p:
        for r in sys.argv[1:]:
            run_one(p, srv.server_address[1], r, end)
    srv.shutdown()
