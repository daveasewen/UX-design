"""views.py — the VIEWS phase of the eval harness (#304 W4b). Every view a run built, measured for ink.

WHY (W3b, #304, notes/_subreports/2026-09-27-304-W3b-why-quality-is-flat.md): the four-part rubric
saturates on the CEO prompt and the harness scored the candidates' FIRST view only. What Dave sees
first is ink: dead space, cut labels, colliding labels, parts off their own size, markers stamped on
every point. This phase finds every destination a run built, whatever its shape — ten linked page
files, `?view=` routes, `#/` routes, or views swapped in by script — and measures each one:

  DISCOVERY  the entry page's navigation (the drive's nav selector), clicked one item at a time in a
             FRESH context: a click that lands on a new URL, or changes the main text on the same URL,
             is a view. Duplicates (same URL, or same text on the entry URL) are dropped. Fixed order,
             capped at 14. Every view is MEASURED IN THE STATE THE CLICK LEFT IT, so a view that only
             script can reach is reached.
  INK        at 1440x900 (the geometry gate's own viewport), with the gate's own code
             (`knowledge/_validate_geometry.py`: page and inner-scroll walk, settle, COLLECT, judge) and
             the own-size gate's (`knowledge/_validate_own_size.py`: PARTS_JS, RefCache, judge):
               dead ink    G6 dead space + G12 chart lost in its box
               cut ink     G8 glyphs cut (a scroll box's start edge included)
               collisions  G7 text on text
               size drift  own-size S1/S2/S3 on any cn- part
               markers     G11 marks on every point of a dense series
             each as INSTANCES, AFFECTED UNITS and a WORST-CASE figure. A unit is a TILE for the four
             geometry classes (the gate's `tile` key; a finding outside any tile counts once per view as
             the page) and a KIND for size drift (component + clause + part, its text stripped).
  TEXT       the rendered text of every view (script-written text included) against the profile's KPI,
             question and view words — never the page source.
  THEME      the run's own switch, both directions, on the entry view: find the control that goes to
             dark (a "Dark" control, else a theme/appearance toggle), click, read <html>'s data-theme
             and the body ground; then the control back to light (a "Light" control, else the same
             toggle), click, and require the page to be back where it started.
  CHARTS     every figure.dv with marks, its type, and whether anything CUTS it: an overflow:hidden|clip
             ancestor, or a scroll box's START edge. A chart below a scroll shell's fold is reachable,
             not clipped (R4s harness defect 4).

Writes runs/<id>/views.json (resumable: finished views are kept, the rest are measured next call) and
runs/<id>/views/<n>.jpg (viewport shots). Needs the seat env in the same bash call.
"""
import hashlib, json, os, re, sys, time
from score import HERE, REPO, jload, jdump, meta_of, run_dir

sys.path.insert(0, os.path.join(REPO, "knowledge"))
MAX_VIEWS = 14
VW, VH = 1440, 900

NAV_JS = r"""() => {
  const vis = el => { const s = getComputedStyle(el); const r = el.getBoundingClientRect();
    return s.display !== 'none' && s.visibility !== 'hidden' && parseFloat(s.opacity || '1') > 0.01 && r.width > 0 && r.height > 0; };
  const txt = el => ((el.getAttribute('aria-label') || '') + ' ' + (el.innerText || el.value || '') + ' ' + (el.title || '')).replace(/\s+/g, ' ').trim().slice(0, 60);
  const navSel = 'nav a, nav button, [role="navigation"] a, [role="navigation"] button, .cn-sidebar-nav a, .cn-sidebar-nav button, .cn-navigations a, .sn a, aside a, [data-view]:is(a,button,[role="tab"],[role="link"])';
  const seen = new Set(), out = [];
  for (const e of document.querySelectorAll(navSel)) {
    if (seen.has(e) || !vis(e)) continue; seen.add(e);
    const t = txt(e);
    if (/theme|dark|light|skip to|sign out|log out/i.test(t) || e.closest('.cn-pagination,[aria-label*="page" i],[class*="breadcrumb"]')) continue;
    out.push({i: out.length, text: t, href: e.getAttribute('href') || '', view: e.getAttribute('data-view') || ''});
    e.setAttribute('data-w4b-nav', String(out.length - 1));
  }
  return out;
}"""

STATE_JS = r"""() => { const main = document.querySelector('main, [role="main"]') || document.body;
  let u = location.href; try { const h = decodeURIComponent(location.hash.slice(1)); if (h && document.getElementById(h)) u = u.split('#')[0]; } catch (e) {}
  if (u.endsWith('#')) u = u.slice(0, -1);
  return {url: u, head: ((main.querySelector('h1,h2') || {}).innerText || '').trim().slice(0, 80), sig: (main.innerText || '').replace(/\s+/g, ' ').slice(0, 4000)}; }"""

PAGE_JS = r"""(prof) => {
  const vis = el => { const s = getComputedStyle(el), r = el.getBoundingClientRect();
    return s.display !== 'none' && s.visibility !== 'hidden' && r.width > 0 && r.height > 0 && !el.closest('[hidden],template'); };
  const say = el => (el.tagName.toLowerCase() + (typeof el.className === 'string' && el.className.trim() ? '.' + el.className.trim().split(/\s+/).slice(0, 2).join('.') : '')).slice(0, 60);
  const figs = [...document.querySelectorAll('figure.dv, figure[data-dv-type]')].filter(vis);
  const main = document.querySelector('main, [role="main"]') || document.body;
  const mainW = main.getBoundingClientRect().width;
  const charts = figs.map(f => { const svg = f.querySelector('svg'); let marks = 0;
    if (svg) for (const e of svg.querySelectorAll('rect,path,circle,line,polyline,polygon,ellipse')) {
      const cl = e.getAttribute('class') || ''; if (/dv-grid|dv-axis|dv-base|dv-tick|dv-hit/.test(cl) || e.closest('.dv-grid,.dv-axis,defs,clipPath,mask')) continue;
      const b = e.getBoundingClientRect(); if (b.width > 0 || b.height > 0) marks++; }
    const t = (svg || f).getBoundingClientRect(); let clip = null;
    for (let a = f.parentElement; a && a !== document.body && !clip; a = a.parentElement) {
      const s = getComputedStyle(a), ar = a.getBoundingClientRect();
      if (/hidden|clip/.test(s.overflowX + ' ' + s.overflowY)) {
        const ex = Math.max(ar.left - t.left, t.right - ar.right, ar.top - t.top, t.bottom - ar.bottom);
        if (ex > 2) clip = {by: say(a), px: Math.round(ex)};
      } else if (/auto|scroll/.test(s.overflowX + ' ' + s.overflowY)) {
        // a scroll box cuts only past its START edges (the scroll origin): the rest is reachable
        const ox = ar.left + (parseFloat(s.borderLeftWidth) || 0) - a.scrollLeft, oy = ar.top + (parseFloat(s.borderTopWidth) || 0) - a.scrollTop;
        const ex = Math.max(ox - t.left, oy - t.top);
        if (ex > 2) clip = {by: say(a) + ' (scroll start edge)', px: Math.round(ex)};
        break;   // past a scroll box, outer boxes clip the SCROLL BOX, not what it scrolls
      } }
    const fr = f.getBoundingClientRect(); const tile = f.closest('.c-bento__tile') || f.parentElement;
    const type = f.getAttribute('data-dv-type') || ((f.className.baseVal !== undefined ? '' : f.className).match(/dv-(bar|boxplot|bullet|butterfly-h|butterfly-v|candlestick|combo|donut|histogram|line|pie|scatter|sparkline|stacked-area)\b/) || [])[1]
      || (((f.closest('[class*="cn-chart-"]') || {className: ''}).className.match(/cn-chart-([a-z-]+)/) || [])[1]) || '?';
    return {type, marks, clip, w: Math.round(fr.width), h: Math.round(fr.height), tile_w: Math.round(tile.getBoundingClientRect().width),
            tile_frac: mainW ? Math.round(100 * tile.getBoundingClientRect().width / mainW) / 100 : null}; });
  const rows = Math.max(0, ...[...document.querySelectorAll('table')].filter(vis).map(t => [...t.querySelectorAll('tbody tr')].filter(vis).length));
  const text = (document.body.innerText || '').toLowerCase();
  const kw = (o) => Object.fromEntries(Object.entries(o || {}).map(([k, x]) => [k, new RegExp(x, 'i').test(text)]));
  const comps = new Set(); for (const e of document.querySelectorAll('[class*="cn-"]')) for (const c of (typeof e.className === 'string' ? e.className : '').split(/\s+/)) if (/^cn-[a-z0-9-]+$/.test(c)) comps.add(c.slice(3));
  const heads = [...main.querySelectorAll('h1,h2,h3')].filter(vis).map(h => h.innerText.trim().replace(/\s+/g, ' ').slice(0, 70)).slice(0, 24);
  return {charts, rows, kpi_words: kw(prof.kpis), question_words: kw(prof.questions), view_words: kw(prof.view_patterns),
          components: [...comps].sort(), headings: heads, text_chars: text.length, doc_h: document.documentElement.scrollHeight,
          h_overflow: Math.max(0, document.documentElement.scrollWidth - innerWidth)};
}"""

THEME_STATE = r"""() => ({theme: document.documentElement.getAttribute('data-theme'), apollo: document.documentElement.getAttribute('data-apollo-theme'),
  body: getComputedStyle(document.body).backgroundColor, html: getComputedStyle(document.documentElement).backgroundColor})"""

THEME_FIND = r"""(want) => {
  const vis = el => { const r = el.getBoundingClientRect(); const s = getComputedStyle(el); return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none'; };
  const txt = el => ((el.innerText || el.value || '') + ' ' + (el.getAttribute('aria-label') || '') + ' ' + (el.title || '')).replace(/\s+/g, ' ').trim();
  const c = [...document.querySelectorAll('button,[role=radio],[role=switch],[role=tab],[role=menuitemradio],label,a,input[type=radio],input[type=checkbox]')].filter(vis);
  document.querySelectorAll('[data-w4b-theme]').forEach(e => e.removeAttribute('data-w4b-theme'));
  const exact = new RegExp('^\\s*' + want + '(\\s+(mode|theme))?\\s*$', 'i');
  let hit = c.find(e => exact.test(e.innerText || e.value || '')) || c.find(e => new RegExp('\\b' + want + '\\b', 'i').test((e.getAttribute('aria-label') || '') + ' ' + (e.title || '')));
  let how = hit ? 'named ' + want : null;
  if (!hit) { hit = c.find(e => /theme|appearance|dark mode|light mode|colour mode|color mode/i.test(txt(e)) || e.matches('[data-theme-toggle],[aria-label*="theme" i]')); how = hit ? 'toggle' : null; }
  if (!hit) return {found: null};
  hit.setAttribute('data-w4b-theme', '1');
  return {found: (hit.tagName.toLowerCase() + ' "' + txt(hit).slice(0, 40) + '"'), how};
}"""


def _sig(s):
    return hashlib.sha1(s.encode()).hexdigest()[:12]


def _num(pat, s, default=0.0):
    m = re.search(pat, s or "")
    return float(m.group(1)) if m else default


def ink_of(geo_findings, os_findings, tiles_n):
    """The five ink classes of one view: instances, affected tiles, worst case."""
    cls = {"dead": [], "cut": [], "collision": [], "size": [], "markers": []}
    for f in geo_findings:
        if f["width"] != VW:
            continue
        c = f["clause"]
        if c in ("G6", "G12"): cls["dead"].append(f)
        elif c == "G8": cls["cut"].append(f)
        elif c == "G7" and " over " in f["where"]: cls["collision"].append(f)
        elif c == "G11": cls["markers"].append(f)
    cls["size"] = list(os_findings)
    worst = {
        "dead": max([_num(r"([\d.]+)px of empty band", f["measured"]) for f in cls["dead"] if f["clause"] == "G6"] + [0]),
        "dead_ring_cover_pct": min([_num(r"covers (\d+)%", f["measured"], 100) for f in cls["dead"] if f["clause"] == "G12"] + [100]),
        "cut": max([max([float(x) for x in re.findall(r"(?:side|top|bottom) ([\d.]+)px", f["measured"])] + [0]) for f in cls["cut"]] + [0]),
        "collision": max([_num(r"overlap by (\d+)x", f["measured"]) for f in cls["collision"]] + [0]),
        "size": min([_num(r"([\d.]+)px", f["measured"], 999) / max(_num(r"([\d.]+)px", f["reference"], 1), 0.01) for f in cls["size"]] + [1.0]),
        "markers": max([_num(r"^(\d+) ", f["measured"]) for f in cls["markers"]] + [0]),
    }
    affected = {}
    for k, fs in cls.items():
        if k == "size":
            # one KIND of drift per view: the same part of the same component off its size the same way
            # (six legend keys at 16.7px against 20 are one defect, as a designer says it)
            affected[k] = len({(f.get("component"), f["clause"], re.sub(r"'[^']*'", "", f.get("part") or "").strip()) for f in fs})
        else:
            affected[k] = len({f.get("tile") or "page" for f in fs})
    return {"instances": {k: len(v) for k, v in cls.items()}, "affected": affected,
            "worst": {k: round(v, 2) for k, v in worst.items()}, "tiles": tiles_n,
            "sample": {k: [{"where": (f.get("where") or f.get("part") or "")[:110], "measured": f["measured"][:90]} for f in v[:4]] for k, v in cls.items()}}


def measure_here(pg, G, OS, refs, smap, prof):
    """Measure the page in the state it is in: the gate's own walk, settle and COLLECT; own-size's parts."""
    pg.evaluate("async () => { const h = document.documentElement.scrollHeight; for (let y = 0; y < h; y += 700) { window.scrollTo(0, y);"
                " await new Promise(r => requestAnimationFrame(() => r())); } window.scrollTo(0, 0); }")
    pg.evaluate(G.INNER_WALK_JS)
    # force one fit pass (the charts re-fit on resize) and then require THREE equal layout reads 250ms
    # apart: a single equal pair could land before a deferred fit had started (measured #304 W4b: one
    # v1013-r3 sub-page read a ring at 162px on one pass and full size on the next)
    pg.evaluate("() => window.dispatchEvent(new Event('resize'))")
    pg.wait_for_timeout(500)
    pg.evaluate(G.FINISH_ANIMATIONS_JS)
    prev, same = None, 0
    for _ in range(16):
        s = pg.evaluate(G.SETTLE_JS)
        same = same + 1 if s == prev else 0
        if same >= 2: break
        prev = s; pg.wait_for_timeout(250)
    m = pg.evaluate(G.COLLECT_JS, G.collect_opts())
    gf = G.judge(m, VW, (), G.spacing_stops())
    pm = pg.evaluate(OS.PARTS_JS, {"mode": "page", "slugs": sorted(smap), "only": None})
    of, matched, _un = OS.judge(pm["parts"], lambda c: refs.get(c, VW), VW)
    tiles_n = sum(1 for t in m["tiles"] if not t["group"]) + len(m.get("leaves") or [])
    page = pg.evaluate(PAGE_JS, prof)
    return m, gf, of, matched, tiles_n, page


def theme_test(pg):
    """Both directions, with the page's own controls. Nothing forced."""
    out = {"start": pg.evaluate(THEME_STATE)}
    f1 = pg.evaluate(THEME_FIND, "dark")
    out["to_dark_control"] = f1
    if not f1.get("found"):
        out.update({"to_dark": False, "back_to_light": False, "verdict": "NO SWITCH FOUND"}); return out
    pg.locator('[data-w4b-theme="1"]').first.click(timeout=2000); pg.wait_for_timeout(700)
    s1 = pg.evaluate(THEME_STATE); out["after_dark"] = s1
    out["to_dark"] = s1["theme"] == "dark" or (s1["body"] != out["start"]["body"] and s1["theme"] != out["start"]["theme"])
    out["on_html"] = s1["theme"] != out["start"]["theme"]
    f2 = pg.evaluate(THEME_FIND, "light")
    out["to_light_control"] = f2
    if f2.get("found"):
        pg.locator('[data-w4b-theme="1"]').first.click(timeout=2000); pg.wait_for_timeout(700)
    s2 = pg.evaluate(THEME_STATE); out["after_light"] = s2
    out["back_to_light"] = bool(f2.get("found")) and s2["theme"] == out["start"]["theme"] and s2["body"] == out["start"]["body"]
    out["verdict"] = "PASS" if (out["to_dark"] and out["back_to_light"] and out["on_html"]) else "FAIL"
    return out


def run(rid, budget):
    import _validate_geometry as G, _validate_own_size as OS
    OS.Harness.eval = OS._harness_eval
    m = meta_of(rid); rd = run_dir(rid)
    prof = jload(os.path.join(HERE, "profiles", m["profile"] + ".json"))
    vp = os.path.join(rd, "views.json")
    V = jload(vp) or {}
    if V.get("entry_sha256") and V["entry_sha256"] != m["page_sha256"]:
        V = {}
    V.update({"entry_sha256": m["page_sha256"], "viewport": "%dx%d @1x (the geometry gate's)" % (VW, VH),
              "gates": {"geometry": "knowledge/_validate_geometry.py", "own_size": "knowledge/_validate_own_size.py",
                        "geometry_sha256": hashlib.sha256(open(G.__file__, "rb").read()).hexdigest(),
                        "own_size_sha256": hashlib.sha256(open(OS.__file__, "rb").read()).hexdigest()}})
    V.setdefault("views", []); V.setdefault("nav", None)
    shots = os.path.join(rd, "views"); os.makedirs(shots, exist_ok=True)
    entry = "file://" + m["entry"]
    t0 = time.time()
    smap = OS.snippet_map()
    with G.Harness() as h:
        refs = OS.RefCache(h, smap)
        def fresh():
            ctx = h.b.new_context(viewport={"width": VW, "height": VH}, device_scale_factor=1)
            pg = ctx.new_page(); errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)[:200])); pg.on("dialog", lambda d: d.dismiss())
            pg.emulate_media(reduced_motion="reduce")
            pg.goto(entry, wait_until="load", timeout=45000)
            pg.evaluate("() => document.fonts ? document.fonts.ready.then(() => 1) : 1"); pg.wait_for_timeout(900)
            return ctx, pg, errs
        if V["nav"] is None:
            ctx, pg, errs = fresh()
            V["nav"] = pg.evaluate(NAV_JS)
            V["entry_state"] = pg.evaluate(STATE_JS)
            V["entry_state"]["sig"] = _sig(V["entry_state"]["sig"])
            V["theme_switch"] = theme_test(pg)
            ctx.close(); jdump(V, vp)
        done = {v["key"] for v in V["views"]}
        seen_urls = {v["url"] for v in V["views"] if v.get("kept")}
        seen_sigs = {v["sig"] for v in V["views"] if v.get("kept")}
        todo = [("entry", None)] + [("nav%d" % n["i"], n) for n in V["nav"]]
        for key, n in todo:
            if key in done: continue
            if sum(1 for v in V["views"] if v.get("kept")) >= MAX_VIEWS: break
            if time.time() - t0 > budget:
                V["truncated"] = True; jdump(V, vp); print("VIEWS %s: budget spent — run the phase again to finish" % rid); return V
            ctx, pg, errs = fresh()
            rec = {"key": key, "nav_text": n["text"] if n else "(entry)", "kept": False}
            try:
                if n:
                    pg.evaluate(NAV_JS)                   # re-mark the nav in this fresh page
                    loc = pg.locator('[data-w4b-nav="%d"]' % n["i"])
                    if loc.count() == 0: raise RuntimeError("nav item not present in a fresh page")
                    loc.first.click(timeout=3000)
                    try: pg.wait_for_load_state("load", timeout=5000)
                    except Exception: pass
                    pg.wait_for_timeout(900)
                st = pg.evaluate(STATE_JS)
                rec.update({"url": st["url"].replace("file://" + os.path.dirname(m["entry"]) + "/", ""), "head": st["head"], "sig": _sig(st["sig"])})
                same_url_as_entry = st["url"] == V["entry_state"]["url"]
                # IDENTITY: a nav item that is a real link (an href other than '#') names its destination
                # by URL — landing on a URL already measured is a duplicate even if some state on it moved
                # (v1013-r2's "Group CEO view" link back to the overview flipped a filter on one load in
                # two). A button or a bare '#' link has only the text to go on.
                linked = bool(n and n.get("href") and n["href"] != "#" and not n["href"].startswith("javascript"))
                url_seen = rec["url"] in seen_urls or same_url_as_entry
                if n and ((linked and url_seen) or (rec["url"] in seen_urls and not same_url_as_entry) or rec["sig"] in seen_sigs):
                    rec["dropped"] = "duplicate of a view already measured"
                elif n and same_url_as_entry and rec["sig"] == V["entry_state"]["sig"]:
                    rec["dropped"] = "the click changed nothing a reader sees"
                else:
                    model, gf, of, matched, tiles_n, page = measure_here(pg, G, OS, refs, smap, prof)
                    rec.update({"kept": True, "ink": ink_of(gf, of, tiles_n), "page": page, "font_ok": model.get("fontOk"),
                                "own_size_matched": matched, "pageerrors": errs[:6],
                                "geometry_counts": {c: sum(1 for f in gf if f["clause"] == c) for c in G.CLAUSES}})
                    idx = sum(1 for v in V["views"] if v.get("kept"))
                    fn = "%02d-%s.jpg" % (idx, re.sub(r"[^a-z0-9]+", "-", (rec["head"] or rec["nav_text"] or key).lower())[:30].strip("-"))
                    pg.screenshot(path=os.path.join(shots, fn), type="jpeg", quality=70)
                    rec["shot"] = "views/" + fn
                    seen_urls.add(rec["url"]); seen_sigs.add(rec["sig"])
            except Exception as e:
                rec["error"] = str(e)[:200]
            ctx.close()
            V["views"].append(rec); jdump(V, vp)
    V["truncated"] = False
    V["seconds_last_call"] = round(time.time() - t0, 1)
    jdump(V, vp)
    kept = [v for v in V["views"] if v.get("kept")]
    tot = {k: sum(v["ink"]["affected"][k] for v in kept) for k in ("dead", "cut", "collision", "size", "markers")}
    print("VIEWS %s: %d views measured (of %d nav items) · affected %s · theme %s (%ss)" % (
        rid, len(kept), len(V["nav"]), tot, V["theme_switch"].get("verdict"), V["seconds_last_call"]))
    return V


# ----------------------------------------------------------------------------- selftest (no stage needed)
def selftest():
    """Ink and views, tested hard: planted vs clean ink, view discovery on three routing shapes,
    script-written text, the theme switch both directions (and a one-way mutant), determinism."""
    import _validate_geometry as G, _validate_own_size as OS
    OS.Harness.eval = OS._harness_eval
    FX = os.path.join(HERE, "fixtures")
    GEO = os.path.join(REPO, "knowledge", "_tests", "geometry")
    prof = jload(os.path.join(HERE, "profiles", "ceo-common.json"))
    A = []
    def check(name, ok, detail):
        A.append({"assert": name, "ok": bool(ok), "detail": detail}); print("%s  %s — %s" % ("PASS" if ok else "FAIL", name, detail))
    smap = OS.snippet_map()
    with G.Harness() as h:
        refs = OS.RefCache(h, smap)
        def ink_page(path, frag=""):
            ctx = h.b.new_context(viewport={"width": VW, "height": VH}); pg = ctx.new_page(); pg.emulate_media(reduced_motion="reduce")
            pg.goto("file://" + path + frag); pg.wait_for_timeout(700)
            _, gf, of, _, tiles_n, page = measure_here(pg, G, OS, refs, smap, prof)
            ctx.close()
            return ink_of(gf, of, tiles_n), page
        pl, _ = ink_page(os.path.join(GEO, "geometry-planted.html"))
        cl, _ = ink_page(os.path.join(GEO, "geometry-clean.html"))
        for k in ("dead", "cut", "collision", "markers"):
            check("ink %-9s planted > 0, clean = 0" % k, pl["affected"][k] > 0 and cl["affected"][k] == 0, "%d vs %d" % (pl["affected"][k], cl["affected"][k]))
        sp, _ = ink_page(os.path.join(GEO, "own-size-planted.html"))
        sc, _ = ink_page(os.path.join(GEO, "own-size-clean.html"))
        check("ink size      planted > 0, clean = 0", sp["affected"]["size"] > 0 and sc["affected"]["size"] == 0, "%d vs %d" % (sp["affected"]["size"], sc["affected"]["size"]))
        pl2, _ = ink_page(os.path.join(GEO, "geometry-planted.html"))
        check("ink deterministic (planted measured twice)", json.dumps(pl, sort_keys=True) == json.dumps(pl2, sort_keys=True), "identical" if pl == pl2 else "DIFFER")
    # discovery, text and theme on the three routing shapes — through the real phase, on throwaway runs
    import score as S
    for fx, want in (("fx-views-hash.html", 3), ("fx-views-query.html", 3), ("fx-views-script.html", 3)):
        rid = "st-" + fx[:-5]
        a = type("A", (), {"run_id": rid, "pack": os.path.join(FX, "_nopack"), "copy_out": None, "page": os.path.join(FX, fx),
                           "label": rid, "kind": "selftest", "profile": "ceo-common"})()
        os.makedirs(a.pack, exist_ok=True)
        S.cmd_stage(a)
        jdump({}, os.path.join(run_dir(rid), "views.json"))       # the mount refuses deletes: reset in place
        V = run(rid, 120)
        kept = [v for v in V["views"] if v.get("kept")]
        check("%s: %d views found" % (fx, want), len(kept) == want, "%d (%s)" % (len(kept), ", ".join(v["head"] for v in kept)))
        kw = any(v["page"]["kpi_words"].get("headroom") for v in kept)
        check("%s: script-written text read ('headroom' is written by JS only)" % fx, kw, str(kw))
        th = V["theme_switch"]
        check("%s: theme to dark and back to light, on <html>" % fx, th.get("verdict") == "PASS", "%s → %s → %s" % (
            th["start"]["theme"], (th.get("after_dark") or {}).get("theme"), (th.get("after_light") or {}).get("theme")))
    rid = "st-fx-theme-oneway"
    a = type("A", (), {"run_id": rid, "pack": os.path.join(FX, "_nopack"), "copy_out": None, "page": os.path.join(FX, "fx-theme-oneway.html"),
                       "label": rid, "kind": "selftest", "profile": "ceo-common"})()
    S.cmd_stage(a)
    jdump({}, os.path.join(run_dir(rid), "views.json"))
    V = run(rid, 60)
    th = V["theme_switch"]
    check("mutant one-way switch: to dark PASSES, back to light FAILS, verdict FAIL",
          th.get("to_dark") and not th.get("back_to_light") and th.get("verdict") == "FAIL", "%s / %s" % (th.get("to_dark"), th.get("back_to_light")))
    ok = all(x["ok"] for x in A)
    jdump({"verdict": "PASS" if ok else "FAIL", "asserts": A}, os.path.join(S.RUNS, "selftest-views.json"))
    print("VIEWS SELFTEST", "PASS" if ok else "FAIL")
    return 0 if ok else 1
