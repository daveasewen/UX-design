"""browser.py — render + drive phases of the R4c eval harness. Imported by score.py.
Needs the seat env sourced in the SAME bash call (RENDER_SHELL, PYTHONPATH, fonts)."""
import functools, hashlib, http.server, json, os, re, socketserver, threading, time, urllib.parse
from score import HERE, jload, jdump, meta_of, run_dir

PROBE = open(os.path.join(HERE, "probe.js")).read()

class _Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass

def serve():
    h = functools.partial(_Quiet, directory="/")
    srv = socketserver.ThreadingTCPServer(("127.0.0.1", 0), h)
    srv.daemon_threads = True
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, srv.server_address[1]

def url(port, path):
    return "http://127.0.0.1:%d%s" % (port, urllib.parse.quote(path))

def theme_var_names(pack_root):
    css = open(os.path.join(pack_root, "knowledge", "canon", "canon.css"), encoding="utf-8", errors="replace").read()
    m = re.search(r'\[data-apollo-theme="common"\]\s*\{([^{}]*)\}', css)
    return sorted(set(re.findall(r"(--[a-z0-9-]+)\s*:", m.group(1)))) if m else []

def platform_fonts(page):
    """The REAL face used for a few text nodes (CDP) — a fallback render is not a size reading."""
    out = {}
    try:
        cdp = page.context.new_cdp_session(page)
        cdp.send("DOM.enable"); cdp.send("CSS.enable")
        doc = cdp.send("DOM.getDocument", {"depth": 1})
        for sel in ("h1", "h2", "[class*='t-cm-']", "td", "button", "body"):
            q = cdp.send("DOM.querySelector", {"nodeId": doc["root"]["nodeId"], "selector": sel})
            if not q.get("nodeId"): continue
            f = cdp.send("CSS.getPlatformFontsForNode", {"nodeId": q["nodeId"]})
            out[sel] = sorted({x["familyName"] for x in f.get("fonts", [])})
        cdp.detach()
    except Exception as e:
        out["error"] = str(e)[:200]
    fams = {x for v in out.values() if isinstance(v, list) for x in v}
    return {"nodes": out, "hsbc": any("HSBC" in x for x in fams), "families": sorted(fams)}

def launch(p):
    return p.chromium.launch(executable_path=os.environ.get("RENDER_SHELL"), args=["--no-sandbox"])

def settle(pg, ms=1400):
    pg.wait_for_timeout(ms)
    try: pg.evaluate("() => window.dispatchEvent(new Event('resize'))")
    except Exception: pass
    pg.wait_for_timeout(500)

# ------------------------------------------------------------------------------------ render
def render(rid, budget):
    from playwright.sync_api import sync_playwright
    m = meta_of(rid); rd = run_dir(rid)
    st = jload(os.path.join(rd, "static.json"), {}) or {}
    prof = jload(os.path.join(HERE, "profiles", m["profile"] + ".json"))
    shots = os.path.join(rd, "shots"); os.makedirs(shots, exist_ok=True)
    arg = {"themeVars": theme_var_names(m["pack_root_staged"]), "tokenNames": sorted(prof["theme"].get("tokens_light", {}).keys()) or
           ["--button-primary-background-default", "--border-radius-default"], "full": True}
    srv, port = serve(); t0 = time.time()
    out = {"viewport": "1440x1000 @1x", "entry": {}, "subpages": [], "subpages_not_reached": [], "shots": {}}
    base = os.path.dirname(m["entry"])
    with sync_playwright() as p:
        b = launch(p)
        ctx = b.new_context(viewport={"width": 1440, "height": 1000}, device_scale_factor=1)
        for mode in ("light", "dark"):
            pg = ctx.new_page(); errs, cons = [], []
            pg.on("pageerror", lambda e: errs.append(str(e)[:300]))
            pg.on("console", lambda msg: cons.append(msg.text[:300]) if msg.type == "error" else None)
            pg.on("dialog", lambda d: d.dismiss())
            pg.goto(url(port, m["entry"]), wait_until="load", timeout=45000)
            settle(pg)
            if mode == "dark":
                pg.evaluate("() => document.documentElement.setAttribute('data-theme','dark')")  # FORCED, declared
                settle(pg, 900)
            r = pg.evaluate(PROBE, dict(arg, full=(mode == "light")))
            r["pageerrors"], r["console_errors"] = errs, cons
            r["dark_forced_by_harness"] = (mode == "dark")
            if mode == "light":
                r["font"] = platform_fonts(pg)
                open(os.path.join(rd, "dom-light.html"), "w", encoding="utf-8").write(pg.content())  # for the rendered-DOM trace
            h = min(r.get("doc_h", 1000), 4000)
            fn = "%s-1440.png" % mode
            pg.screenshot(path=os.path.join(shots, fn), clip={"x": 0, "y": 0, "width": 1440, "height": h})
            out["shots"]["%s-1440" % mode] = "shots/" + fn
            out["entry"][mode] = r
            pg.close()
        for sp in (st.get("pages") or [])[1:]:
            if time.time() - t0 > budget - 12:
                out["subpages_not_reached"].append(sp["page"]); continue
            path = os.path.normpath(os.path.join(base, sp["page"]))
            pg = ctx.new_page(); errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)[:300]))
            pg.on("dialog", lambda d: d.dismiss())
            try:
                pg.goto(url(port, path), wait_until="load", timeout=30000); settle(pg, 1000)
                r = pg.evaluate(PROBE, dict(arg, full=False))
                for c in r.get("charts", []): c["page"] = sp["page"]
                r["page"], r["pageerrors"] = sp["page"], errs
                out["subpages"].append(r)
            except Exception as e:
                out["subpages"].append({"page": sp["page"], "error": str(e)[:300], "charts": []})
            pg.close()
        b.close()
    srv.shutdown()
    out["seconds"] = round(time.time() - t0, 1)
    jdump(out, os.path.join(rd, "render.json"))
    L = out["entry"]["light"]
    print("RENDER %s charts=%d clipped=%d hsbc=%s errors=%d subpages=%d (%ss)" % (rid, len(L["charts"]),
          sum(1 for c in L["charts"] if c["clipped"]), L["font"]["hsbc"], len(L["pageerrors"]), len(out["subpages"]), out["seconds"]))
    return out

# ------------------------------------------------------------------------------------ drive
INIT = """(() => { window.__mut = 0; const go = () => { try { new MutationObserver(ms => { window.__mut += ms.length; })
  .observe(document, {subtree:true, childList:true, attributes:true, characterData:true}); } catch(e) {} };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', go); else go(); })();"""

ENUM = r"""() => {
  const vis = el => { const s = getComputedStyle(el); const r = el.getBoundingClientRect();
    return s.display !== 'none' && s.visibility !== 'hidden' && parseFloat(s.opacity || '1') > 0.01 && r.width > 0 && r.height > 0; };
  const txt = el => ((el.getAttribute('aria-label') || '') + ' ' + (el.innerText || el.value || '') + ' ' + (el.title || '')).replace(/\s+/g, ' ').trim().slice(0, 60);
  document.querySelectorAll('[data-r4c]').forEach(e => e.removeAttribute('data-r4c'));
  const navSel = 'nav a, nav button, [role="navigation"] a, [role="navigation"] button, .cn-sidebar-nav a, .cn-sidebar-nav button, .cn-navigations a, .sn a, aside a';
  const nav = [...document.querySelectorAll(navSel)].filter(vis).filter(e => !/theme|dark|light|skip to/i.test(txt(e)) && !e.closest('.cn-pagination,[aria-label*="page" i],[class*="breadcrumb"]'));
  const all = [...document.querySelectorAll('button, a[href], select, input:not([type="hidden"]), textarea, [role="button"], [role="tab"], [role="switch"], [role="checkbox"], [role="combobox"], [aria-haspopup], th[aria-sort], [data-sort], tr[tabindex], [role="row"][tabindex]')];
  const fam = el => {
    const t = txt(el), tag = el.tagName.toLowerCase(), type = (el.getAttribute('type') || '').toLowerCase();
    if (/theme|dark mode|light mode|appearance|\bdark\b|\blight\b/i.test(t) || el.matches('[data-theme-toggle],[aria-label*="theme" i]')) return 'theme';
    if (/export|download|\bcsv\b|\bpdf\b/i.test(t)) return 'export';
    if (/approv|reject|authori[sz]|sign.?off|release|decline/i.test(t)) return 'approve';
    if (/acknowledg/i.test(t)) return 'ack';
    if (/message|reply|send|service request|new request|compose/i.test(t)) return 'message';
    if (tag === 'th' || el.matches('[data-sort], [aria-sort]') || el.closest('th') || /\bsort\b/i.test(t)) return 'sort';
    if (el.closest('.cn-pagination,[aria-label*="pagination" i],[class*="pager"]') || /^(next|previous|prev|›|‹|»|«|\d+)$/i.test(t) || /next page|previous page|rows per page/i.test(t)) return 'paging';
    if (type === 'search' || /search/i.test(el.getAttribute('placeholder') || '') || (tag === 'input' && /search/i.test(t))) return 'search';
    if (el.getAttribute('role') === 'tab') return 'tabs';
    if (tag === 'select' || el.matches('[role="combobox"], [aria-haspopup="listbox"], [aria-haspopup="menu"]') || el.closest('.cn-filter-toolbar-bar,.ftb-outer,[class*="filter"]') || /filter|entity|region|currency|period|date range|all entities|all regions/i.test(t)) return 'filter';
    if (el.matches('tr[tabindex], [role="row"][tabindex]') || el.closest('tbody') || /view|detail|open|more/i.test(t) || el.matches('[aria-haspopup="dialog"]')) return 'detail';
    if (el.matches('[aria-expanded]')) return 'disclosure';
    if (tag === 'input' || tag === 'textarea' || el.matches('[role="checkbox"], [role="switch"]')) return 'form';
    if (tag === 'a') return 'link';
    return 'other';
  };
  let i = 0; const navOut = [], ctlOut = [], per = {};
  for (const e of nav) { if (navOut.length >= 14) break; e.setAttribute('data-r4c', 'n' + i); navOut.push({ id: 'n' + i, text: txt(e), href: e.getAttribute('href') || '' }); i++; }
  for (const e of all) {
    if (e.hasAttribute('data-r4c') || !vis(e) || e.closest('figure.dv svg')) continue;
    const f = fam(e); per[f] = (per[f] || 0) + 1;
    if (per[f] > 6 || ctlOut.length >= 48) continue;
    e.setAttribute('data-r4c', 'c' + i);
    ctlOut.push({ id: 'c' + i, family: f, text: txt(e), tag: e.tagName.toLowerCase(), type: (e.getAttribute('type') || '').toLowerCase(), href: e.getAttribute('href') || '' });
    i++;
  }
  return { nav: navOut, controls: ctlOut, present: per };
}"""

STATE = r"""() => {
  const q = s => [...document.querySelectorAll(s)];
  const main = document.querySelector('main, [role="main"]') || document.body;
  const tEl = document.documentElement.hasAttribute('data-theme') ? document.documentElement : (document.querySelector('[data-theme]') || document.documentElement);
  // an in-page anchor jump (#id of an element on this page) is a scroll, not a view: drop that hash
  let u = location.href; try { const h = decodeURIComponent(location.hash.slice(1)); if (h && document.getElementById(h)) u = u.split('#')[0]; } catch (e) {}
  return { url: u,
    theme: (tEl === document.documentElement ? 'html' : tEl.tagName.toLowerCase()) + ':' + tEl.getAttribute('data-theme') + ':' + getComputedStyle(document.body).backgroundColor,
    nav: q('[aria-current]').map(e => (e.innerText || '').trim().slice(0, 40)).join('|'),
    view: ((main.querySelector('h1,h2') || {}).innerText || '').trim().slice(0, 60) + '#' + (u.split('#')[1] || ''),
    filter: q('select').map(s => s.value).join('|') + '/' + q('[role="combobox"],[aria-haspopup="listbox"]').map(e => (e.innerText || e.value || '').trim().slice(0, 30)).join('|'),
    sort: q('[aria-sort]').map(e => (e.innerText || '').trim().slice(0, 20) + '=' + e.getAttribute('aria-sort')).filter(x => !/=none$/.test(x)).join('|'),
    search: q('input[type="search"], input[placeholder*="earch"]').map(e => e.value).join('|'),
    storage: (() => { try { return Object.keys(localStorage).length + Object.keys(sessionStorage).length; } catch (e) { return -1; } })(),
    sig: (main.innerText || '').replace(/\s+/g, ' ').slice(0, 3000) };
}"""

DOMSIG = r"""() => { const parts = [document.body ? document.body.innerText : '', [...document.querySelectorAll('[data-theme],[data-apollo-theme]')].map(e => e.getAttribute('data-theme') + '/' + e.getAttribute('data-apollo-theme')).join(',')];
  for (const e of document.querySelectorAll('[aria-expanded],[aria-pressed],[aria-selected],[aria-checked],[aria-current],[aria-sort],[data-open],[open],[hidden],[aria-hidden="true"]'))
    parts.push([e.getAttribute('aria-expanded'), e.getAttribute('aria-pressed'), e.getAttribute('aria-selected'), e.getAttribute('aria-checked'),
                e.getAttribute('aria-current'), e.getAttribute('aria-sort'), e.getAttribute('data-open'), e.hasAttribute('open'), e.hidden].join(','));
  for (const e of document.querySelectorAll('input,select,textarea')) parts.push(e.type === 'checkbox' || e.type === 'radio' ? String(e.checked) : e.value);
  let h = 0; const s = parts.join('\u0001'); for (let i = 0; i < s.length; i++) h = (h * 31 + s.charCodeAt(i)) | 0; return h; }"""

def nurl(u):
    """A bare trailing '#' (href="#" dead links) is not a navigation."""
    return u[:-1] if u.endswith("#") else u

def sig(s):
    return hashlib.sha1(s.encode()).hexdigest()[:10]

def drive(rid, budget):
    from playwright.sync_api import sync_playwright
    m = meta_of(rid); rd = run_dir(rid)
    prof = jload(os.path.join(HERE, "profiles", m["profile"] + ".json"))
    srv, port = serve(); t0 = time.time()
    entry = url(port, m["entry"])
    out = {"pageerrors": [], "persistence": {}, "views": {}, "controls": {}, "tooltips": {}, "theme_switch": {}, "truncated": False}
    with sync_playwright() as p:
        b = launch(p)
        ev = {"download": 0, "dialog": 0, "popup": 0}
        box = {}
        def section():
            """A NEW browser context per drive section: storage never leaks from one section into the next."""
            if box.get("ctx"):
                try: box["ctx"].close()
                except Exception: pass
            ctx = b.new_context(viewport={"width": 1440, "height": 1000}, accept_downloads=True)
            ctx.add_init_script(INIT)
            pg = ctx.new_page()
            pg.on("pageerror", lambda e: out["pageerrors"].append(str(e)[:300]))
            pg.on("dialog", lambda d: (ev.__setitem__("dialog", ev["dialog"] + 1), d.accept()))
            pg.on("download", lambda d: ev.__setitem__("download", ev["download"] + 1))
            ctx.on("page", lambda np: (ev.__setitem__("popup", ev["popup"] + 1), np.close()) if np != pg else None)
            box["ctx"], box["pg"] = ctx, pg
            return pg
        pg = section()
        def fresh():
            pg = box["pg"]
            pg.goto(entry, wait_until="load", timeout=45000); settle(pg, 1100)
            return pg.evaluate(ENUM)
        def click(sel, kind="click"):
            el = box["pg"].locator(sel).first
            if kind == "select":
                opts = el.locator("option")
                if opts.count() > 1: el.select_option(index=1, timeout=1500)
                else: el.click(timeout=1500)
            elif kind == "fill":
                el.fill("pay", timeout=1500); el.press("Enter", timeout=800)
            else:
                el.click(timeout=1500)
        # ---------- 1. persistence
        E = fresh()
        idle0 = pg.evaluate("() => window.__mut"); pg.wait_for_timeout(500); idle = pg.evaluate("() => window.__mut") - idle0
        out["idle_mutations_per_500ms"] = idle
        S0 = pg.evaluate(STATE)
        acts = {}
        th = [c for c in E["controls"] if c["family"] == "theme"]
        if th:
            try:
                click('[data-r4c="%s"]' % th[0]["id"]); pg.wait_for_timeout(400)
                after = pg.evaluate(STATE)["theme"]
                on_html = pg.evaluate("() => document.documentElement.getAttribute('data-theme')")
                out["theme_switch"] = {"found": th[0]["text"], "before": S0["theme"], "after": after, "flips": after != S0["theme"],
                                       "html_data_theme_after": on_html, "on_html": after.startswith("html:")}
                acts["theme"] = True
            except Exception as e:
                out["theme_switch"] = {"found": th[0]["text"], "error": str(e)[:160], "flips": False}
        else:
            out["theme_switch"] = {"found": None, "flips": False}
        flt = [c for c in E["controls"] if c["family"] == "filter" and c["tag"] == "select"] or [c for c in E["controls"] if c["family"] == "filter"]
        if flt:
            try:
                c = flt[0]
                if c["tag"] == "select": click('[data-r4c="%s"]' % c["id"], "select")
                else:
                    click('[data-r4c="%s"]' % c["id"]); pg.wait_for_timeout(300)
                    opt = pg.locator('[role="option"]:visible, [role="menuitemradio"]:visible, [role="menuitem"]:visible')
                    if opt.count() > 1: opt.nth(1).click(timeout=1500)
                acts["filter"] = True; pg.wait_for_timeout(400)
            except Exception: pass
        srt = [c for c in E["controls"] if c["family"] == "sort"]
        if srt:
            try: click('[data-r4c="%s"]' % srt[0]["id"]); acts["sort"] = True; pg.wait_for_timeout(300)
            except Exception: pass
        sch = [c for c in E["controls"] if c["family"] == "search" and c["tag"] == "input"]
        if sch:
            try: click('[data-r4c="%s"]' % sch[0]["id"], "fill"); acts["search"] = True; pg.wait_for_timeout(300)
            except Exception: pass
        navs = [n for n in E["nav"] if n["href"] != "#" or True]
        if len(navs) > 1:
            try: click('[data-r4c="%s"]' % navs[1]["id"]); acts["nav"] = True; pg.wait_for_load_state("load"); settle(pg, 700)
            except Exception: pass
        S1 = pg.evaluate(STATE)
        pg.reload(wait_until="load"); settle(pg, 1100)
        S2 = pg.evaluate(STATE)
        fam = {}
        for k, key in (("theme", "theme"), ("filter", "filter"), ("sort", "sort"), ("search", "search"), ("nav", None)):
            if k == "nav":
                # where you are = url + aria-current + the view's heading; the text signature only proves a change
                a0, a1, a2 = ((nurl(X["url"]), X["nav"], X["view"].rstrip("#")) for X in (S0, S1, S2))
                txt_changed = sig(S1["sig"]) != sig(S0["sig"])
                changed = a1 != a0 or txt_changed
                persisted = changed and a2 == a1 and (a1 != a0 or sig(S2["sig"]) == sig(S1["sig"]))
            else:
                changed = S1[key] != S0[key]; persisted = changed and S2[key] == S1[key]
            fam[k] = {"attempted": bool(acts.get(k)), "changed": changed, "persisted": persisted}
        out["persistence"] = {"families": fam, "storage_keys": S1["storage"], "url_after": S1["url"].replace(entry, "<entry>"),
                              "s0": {k: v for k, v in S0.items() if k != "sig"}, "s1": {k: v for k, v in S1.items() if k != "sig"},
                              "s2": {k: v for k, v in S2.items() if k != "sig"}}
        # ---------- 2. views via nav
        pg = section(); E = fresh()
        sigs = {sig(pg.evaluate(STATE)["sig"])}
        vrec = []
        for n in E["nav"]:
            if time.time() - t0 > budget * 0.45: out["truncated"] = True; break
            try:
                if pg.locator('[data-r4c="%s"]' % n["id"]).count() == 0:
                    E = fresh()
                u0 = pg.url
                click('[data-r4c="%s"]' % n["id"]); pg.wait_for_timeout(350)
                try: pg.wait_for_load_state("load", timeout=4000)
                except Exception: pass
                s = pg.evaluate(STATE); h = sig(s["sig"])
                vrec.append({"text": n["text"], "href": n["href"], "url_changed": nurl(pg.url) != nurl(u0), "sig": h, "new": h not in sigs})
                sigs.add(h)
                if pg.url.split("#")[0] != entry.split("#")[0]:
                    E = fresh()
            except Exception as e:
                vrec.append({"text": n["text"], "error": str(e)[:120]})
        matched = {}
        for vname, pat in (prof.get("view_patterns") or {}).items():
            matched[vname] = any(re.search(pat, r.get("text", ""), re.I) and (r.get("new") or r.get("url_changed")) for r in vrec)
        out["views"] = {"nav_items": len(E["nav"]), "clicks": vrec, "live_distinct": len(sigs), "matched": matched,
                        "matched_n": sum(matched.values())}
        # ---------- 3. controls
        pg = section(); E = fresh()
        fams = {}
        driven = live = 0
        rec = []
        for c in E["controls"]:
            if time.time() - t0 > budget * 0.85: out["truncated"] = True; break
            f = fams.setdefault(c["family"], {"driven": 0, "live": 0, "blocked": 0})
            sel = '[data-r4c="%s"]' % c["id"]
            if pg.locator(sel).count() == 0:
                E2 = fresh()
                if pg.locator(sel).count() == 0: continue
            u0 = pg.url; m0 = pg.evaluate("() => window.__mut"); e0 = dict(ev); d0 = pg.evaluate(DOMSIG)
            ok = True
            try:
                kind = "select" if c["tag"] == "select" else ("fill" if c["tag"] in ("input", "textarea") and c["type"] not in ("checkbox", "radio", "button", "submit") else "click")
                click(sel, kind)
            except Exception as e:
                ok = False
            pg.wait_for_timeout(300)
            try:
                m1 = pg.evaluate("() => window.__mut"); d1 = pg.evaluate(DOMSIG)
            except Exception:
                m1 = m0 + 1; d1 = None  # navigated away mid-read
            nav_away = nurl(pg.url) != nurl(u0)
            dm = (m1 - m0) if not nav_away else None
            # LIVE = the click changed what a person can see or what the page states (text, aria state,
            # form values, theme), or navigated, or fired a download/dialog/popup. Raw mutation counts are
            # kept as information only: hover/focus scripts mutate class lists on any pointer move.
            is_live = ok and (nav_away or (d1 is not None and d1 != d0) or ev != e0)
            driven += 1; f["driven"] += 1
            if not ok: f["blocked"] += 1
            if is_live: live += 1; f["live"] += 1
            rec.append({"family": c["family"], "text": c["text"], "ok": ok, "live": bool(is_live), "mutations": dm, "nav_away": nav_away, "dom_changed": d1 is not None and d1 != d0,
                        "events": {k: ev[k] - e0[k] for k in ev if ev[k] != e0[k]}})
            if nav_away:
                E = fresh()
            else:
                try:
                    if pg.locator('[aria-modal="true"]:visible, dialog[open]').count(): pg.keyboard.press("Escape"); pg.wait_for_timeout(150)
                except Exception: pass
        out["controls"] = {"driven": driven, "live": live, "families": fams, "present": E.get("present"), "records": rec}
        # ---------- 4. tooltips
        pg = section(); E = fresh()
        tried = shown = 0
        n = pg.locator("figure.dv").count()
        for i in range(min(n, 6)):
            if time.time() - t0 > budget: out["truncated"] = True; break
            fig = pg.locator("figure.dv").nth(i)
            mk = fig.locator("svg .dv-series, svg rect.dv-bar, svg circle, svg path.dv-series, svg rect")
            if mk.count() == 0: continue
            tried += 1
            try:
                mk.first.hover(timeout=1500, force=True); pg.wait_for_timeout(250)
                vis = pg.evaluate("""() => [...document.querySelectorAll('.dv-tip, [role="tooltip"], .tooltip, [class*="tooltip"]')]
                    .some(t => { const s = getComputedStyle(t); const r = t.getBoundingClientRect();
                      return s.display !== 'none' && s.visibility !== 'hidden' && parseFloat(s.opacity) > 0.05 && r.width > 0 && (t.innerText || '').trim(); })""")
                shown += 1 if vis else 0
            except Exception: pass
        out["tooltips"] = {"charts_hovered": tried, "tooltip_shown": shown}
        b.close()
    srv.shutdown()
    out["seconds"] = round(time.time() - t0, 1)
    jdump(out, os.path.join(rd, "drive.json"))
    print("DRIVE %s persisted=%s views=%d controls %d/%d live tooltips %d/%d errors=%d truncated=%s (%ss)" % (
        rid, [k for k, v in out["persistence"]["families"].items() if v["persisted"]], out["views"]["live_distinct"],
        out["controls"]["live"], out["controls"]["driven"], shown, tried, len(out["pageerrors"]), out["truncated"], out["seconds"]))
    return out

def run(phase, rid, budget):
    return render(rid, budget) if phase == "render" else drive(rid, budget)
