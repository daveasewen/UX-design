"""#312 lane F3 — renders for two of Dave's stalled calls, drawn on the real pages:
  item 1  container types (W-308iw): SECTION and PANEL drawn on the banking demo
          (dashboards/international-banking-dashboard.canon.html), light and dark.
  item 2  the #261 nav family as a dashboard tile group (s308-D33 held; R6e red): the family on
          the dashboard template (knowledge/snippets/Template-dashboard-bento.reference.html),
          counted both ways, plus the two family members that are not on the page.
Every page is a SCRATCH COPY taken from the committed sha (git show <sha>:path), canon.css and
type.css too, so the mount's dirty tree is never rendered. Nothing in the tree is edited; the
annotation layer (outlines + labels) is injected into the scratch copy only.
Usage (at the seat, one bash call):
  export TMPDIR=/dev/shm; bash knowledge/_render/ensure_env.sh; source knowledge/_render/seat_env.sh
  python3 notes/_lanes/312/F/F3/render_F3.py <sha> [sec|panel|nav|all]
Writes notes/_lanes/312/F/F3/img/*.png and img/F3-facts.json (merged per run)."""
import os, sys, json, subprocess
from playwright.sync_api import sync_playwright
R = os.getcwd(); OUT = "notes/_lanes/312/F/F3/img"; SH = "/dev/shm/f3_312"
os.makedirs(SH, exist_ok=True); os.makedirs(OUT, exist_ok=True)
SHA = sys.argv[1] if len(sys.argv) > 1 else "HEAD"
WHAT = sys.argv[2] if len(sys.argv) > 2 else "all"
sha = subprocess.run(["git", "rev-parse", SHA], capture_output=True, text=True, check=True).stdout.strip()
def show(p): return subprocess.run(["git", "show", f"{sha}:{p}"], capture_output=True, text=True, check=True).stdout
open(f"{SH}/canon.css", "w").write(show("knowledge/canon/canon.css"))
open(f"{SH}/type.css", "w").write(show("knowledge/canon/type.css"))
DEMO = "dashboards/international-banking-dashboard.canon.html"
d = show(DEMO).replace('../knowledge/canon/canon.css', f'file://{SH}/canon.css') \
    .replace('../knowledge/canon/type.css', f'file://{SH}/type.css').replace('../knowledge/', f'file://{R}/knowledge/')
open(f"{SH}/demo.html", "w").write(d)
TPL = "knowledge/snippets/Template-dashboard-bento.reference.html"
t = show(TPL).replace('../canon/type.css', f'file://{SH}/type.css').replace('../', f'file://{R}/knowledge/')
open(f"{SH}/tpl.html", "w").write(t)
for name in ("Sidebar-nav", "Tab-bar"):
    s = show(f"knowledge/snippets/{name}.reference.html").replace('../canon/type.css', f'file://{SH}/type.css') \
        .replace('../canon/canon.css', f'file://{SH}/canon.css').replace('../', f'file://{R}/knowledge/')
    open(f"{SH}/{name}.html", "w").write(s)
FACTS_P = f"{OUT}/F3-facts.json"
facts = json.load(open(FACTS_P)) if os.path.exists(FACTS_P) else {}
facts.update({"sha": sha, "demo": DEMO, "template": TPL, "canon": f"git show {sha[:8]}:knowledge/canon/canon.css"})

ANN_CSS = """
.f3-tag{background:#1F1F1F;color:#fff;font:700 12px/1 Helvetica,Arial,sans-serif;letter-spacing:.08em;padding:12px 24px;position:relative;z-index:3000}
.f3-notes{background:#FFF3B0;color:#1F1F1F;font:13px/1.45 Helvetica,Arial,sans-serif;padding:8px 24px;border-bottom:1px solid #C9A800;display:flex;gap:32px;position:relative;z-index:3000}
.f3-notes span{flex:1}
#f3ov{position:absolute;left:0;top:0;width:0;height:0;z-index:2900;pointer-events:none}
.f3-box{position:absolute;box-sizing:border-box;border:3px solid var(--c);border-radius:2px}
.f3-box.dash{border-style:dashed}
.f3-lab{position:absolute;left:-3px;top:-3px;transform:translateY(-100%);background:var(--c);color:#fff;
  font:700 12px/1 Helvetica,Arial,sans-serif;letter-spacing:.04em;padding:5px 8px;white-space:nowrap}
.f3-lab.in{transform:none}
.f3-lab.r{left:auto;right:-3px}
.f3-lab small{font-weight:400;letter-spacing:0;opacity:.92}
"""
ANN_JS = r"""([css, tag, notes, boxes]) => {
  if (tag) { const st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);
  const t = document.createElement('div'); t.className = 'f3-tag'; t.innerHTML = tag;
  const n = document.createElement('div'); n.className = 'f3-notes'; n.innerHTML = notes.map(x => '<span>' + x + '</span>').join('');
  document.body.insertBefore(n, document.body.firstChild); document.body.insertBefore(t, n); }
  let ov = document.getElementById('f3ov'); if (!ov) { ov = document.createElement('div'); ov.id = 'f3ov'; document.body.appendChild(ov); }
  const out = [];
  boxes.forEach(b => {
    const els = [...document.querySelectorAll(b.sel)]; const pick = b.nth != null ? [els[b.nth]] : els;
    pick.forEach((el, i) => { if (!el) return; const r = el.getBoundingClientRect(); const pad = b.pad || 0;
      const x = document.createElement('div'); x.className = 'f3-box' + (b.dash ? ' dash' : ''); x.style.setProperty('--c', b.c);
      x.style.left = (r.left + scrollX - pad) + 'px'; x.style.top = (r.top + scrollY - pad) + 'px';
      x.style.width = (r.width + 2 * pad) + 'px'; x.style.height = (r.height + 2 * pad) + 'px';
      const lab = (Array.isArray(b.label) ? b.label[i] : b.label); if (lab) { const l = document.createElement('div');
        l.className = 'f3-lab' + (b.inside ? ' in' : '') + (b.right ? ' r' : ''); l.innerHTML = lab; x.appendChild(l); }
      ov.appendChild(x); out.push({sel: b.sel, i, w: Math.round(r.width), h: Math.round(r.height)}); });
  });
  return out;
}"""
C_SEC = "#C2410C"; C_HOU = "#1D4ED8"; C_PAN = "#6D28D9"; C_FRM = "#374151"; C_GRP = "#047857"; C_NAV = "#B91C1C"

def page_for(b, url, w, h, theme_mode=None):
    pg = b.new_page(viewport={"width": w, "height": h}, reduced_motion="reduce")
    pg.goto(url); pg.wait_for_timeout(700)
    if theme_mode: pg.evaluate(f"document.body.setAttribute('data-theme','{theme_mode}')"); pg.wait_for_timeout(250)
    return pg

def sec(b):
    out = {}
    for mode in ("light", "dark"):
        pg = page_for(b, f"file://{SH}/demo.html", 1440, 900, mode)
        land = pg.evaluate("""() => {
          const named = s => s.hasAttribute('aria-label') || s.hasAttribute('aria-labelledby');
          const secs = [...document.querySelectorAll('section')];
          return {section_elements: secs.length, named_sections_ie_region_landmarks: secs.filter(named).length,
                  tiles_as_named_sections: secs.filter(s => s.classList.contains('c-bento__tile') && named(s)).length,
                  bento_groups_div_aria_label: [...document.querySelectorAll('div.c-bento[aria-label]')].length,
                  theme: document.documentElement.getAttribute('data-apollo-theme')}; }""")
        tiles = pg.evaluate("() => [...document.querySelectorAll('.c-bento__tile')].map(e => e.getAttribute('data-c')+'×'+e.getAttribute('data-r'))")
        groups = pg.evaluate("() => [...document.querySelectorAll('div.c-bento')].map(e => e.getAttribute('aria-label'))")
        boxes = [
            {"sel": ".cn-navigations", "c": C_FRM, "dash": True, "inside": True,
             "label": "FRAME · the banner landmark &lt;header&gt; · not a section"},
            {"sel": "section.dashboard-page-header", "c": C_SEC, "pad": 0, "inside": True, "right": True,
             "label": "SECTION · region landmark, named by its h1 “Global treasury overview”"},
            {"sel": "div.c-bento", "c": C_SEC, "pad": 6, "right": True,
             "label": [f"SECTION · region landmark, named “{g}”" for g in groups]},
            {"sel": ".c-bento__tile", "c": C_HOU, "inside": True,
             "label": [f"housing: tile · cell {x}" for x in tiles]},
        ]
        info = pg.evaluate(ANN_JS, [ANN_CSS,
            f"CONTAINER TYPES · 1 OF 2 · SECTION, DRAWN ON THE BANKING DEMO ({land['theme'].upper()}, {mode.upper()}) · A DRAWN OPTION, NOT A RULING",
            ["<b>Section</b> = a page region mapped to a landmark: it carries a name, and a screen reader lists it. Orange: the page header and each bento group as sections.",
             "<b>Housing</b> (s308-D44) = the surfaced thing in a <b>cell</b>: blue, one per tile. Cell = the grid position (written c×r).",
             f"Today the demo marks every tile as a named &lt;section&gt;: {land['tiles_as_named_sections']} of its {land['named_sections_ie_region_landmarks']} named sections are tiles, and the three groups are plain &lt;div&gt;s. With the word ruled, tiles stop being landmarks and the groups become them."],
            boxes])
        pg.wait_for_timeout(150)
        fn = f"{OUT}/F3-1-section-1440-{mode}.png"; pg.screenshot(path=fn, full_page=True)
        out[mode] = {"file": fn, "landmarks": land, "boxes": len(info)}
        pg.close()
    facts["sec"] = out

def panel(b):
    pg = page_for(b, f"file://{SH}/demo.html", 1440, 900, "light")
    pg.evaluate(ANN_JS, [ANN_CSS,
        "CONTAINER TYPES · 2 OF 2 · PANEL, DRAWN ON THE BANKING DEMO (CONSOLE, LIGHT) · A DRAWN OPTION, NOT A RULING",
        ["<b>Panel</b> (s308-D41, already defined) = a region of the <b>screen frame</b>: side panel, drawer, splitter pane. Purple: a side panel docked right under the top nav, built from the canon Drawer sheet; the page narrows beside it.",
         "A panel belongs to the frame, not to the page's flow: it stays put while the page scrolls, and it is never a bento group. A section (orange) is a region <b>of the page</b>.",
         "<b>Division</b> and <b>sector</b> are not drawn: neither names a thing that section, panel, housing or cell does not already name."], []])
    geo = pg.evaluate("""() => {
      document.querySelectorAll('section.dashboard-page-header, main').forEach(e => { e.style.setProperty('width', 'calc(100% - 400px)', 'important'); e.style.setProperty('max-width', 'calc(100% - 400px)', 'important'); e.style.setProperty('box-sizing', 'border-box', 'important'); });
      const m = document.querySelector('.cn-navigations').getBoundingClientRect(); const top = m.bottom + scrollY;
      const w = document.createElement('div'); w.className = 'cn-drawer';
      w.innerHTML = `<aside class="sheet open" role="complementary" aria-labelledby="f3p" style="position:absolute;top:${top}px;height:${900 - top}px;bottom:auto;border-radius:0">
        <div class="sheet-head"><h3 class="t-ed-heading-4 em" id="f3p">Payment details</h3>
        <button class="close" type="button" aria-label="Close panel"><svg viewBox="0 0 14 14" aria-hidden="true"><path d="M1 1l12 12M13 1L1 13" stroke="currentColor" stroke-width="1.6" fill="none"/></svg></button></div>
        <div class="sheet-body"><p class="t-ed-body">USD 1,240,000.00 to Meridian Logistics Inc., New York. Released 09:14 by A. Shah, second approval pending.</p>
        <p class="t-ed-body-small">Reference INV-20488 · Value date 28 Aug 2026 · Cut-off 16:30 New York</p></div>
        <div class="sheet-foot"><button class="dbtn primary t-cm-button t-cm-slot" type="button">Approve</button>
        <button class="dbtn secondary t-cm-button t-cm-slot" type="button">Close</button></div></aside>`;
      document.body.appendChild(w); return {top: Math.round(top), main_w: Math.round(document.querySelector('main').getBoundingClientRect().width), tag_w: Math.round(document.querySelector('.f3-tag').getBoundingClientRect().width)}; }""")
    pg.wait_for_timeout(400)
    info = pg.evaluate(ANN_JS, [ANN_CSS, None, [],
        [{"sel": ".cn-drawer .sheet", "c": C_PAN, "inside": True, "right": True, "label": "PANEL · complementary landmark &lt;aside&gt; · part of the frame"},
         {"sel": "section.dashboard-page-header", "c": C_SEC, "inside": True, "right": True, "label": "SECTION · page region"},
         {"sel": "div.c-bento", "c": C_SEC, "pad": 6, "label": "SECTION · page region", "inside": True, "right": True},
         {"sel": ".cn-navigations", "c": C_FRM, "dash": True, "inside": True, "label": "FRAME · banner"}]])
    fn = f"{OUT}/F3-1-panel-1440-light.png"; pg.screenshot(path=fn, full_page=False)
    facts["panel"] = {"file": fn, "boxes": len(info), "viewport": [1440, 900], "panel_width_px": 400, "panel_top_px": geo["top"],
                      "page_content_width_px_beside_panel": geo["main_w"], "strip_w": geo["tag_w"]}
    pg.close()

def dial(exclude_nav_family, resolve_alias):
    """The s245-D7 grouping dial, re-derived the way gen_bento_matrix_217.grouping_dial() derives it
    (connected components of edges.groupsWith + count{per:group} over the template's $composes),
    with two switches so the count can be read BOTH ways. Reads the metas on the mount."""
    cd = os.path.join(R, "knowledge", "components")
    def meta(stem):
        f = os.path.join(cd, stem + ".meta.json"); return json.load(open(f, encoding="utf-8")) if os.path.exists(f) else {}
    tpl = meta("template-dashboard-bento")
    members = [c.split(":", 1)[1] for c in tpl.get("$composes", []) if c.startswith("component:")]
    edges = []
    for stem in members:
        m = meta(stem); src = stem
        if resolve_alias and isinstance(m.get("aliasOf"), dict):
            src = m["aliasOf"]["component"].split(":", 1)[1]; m = meta(src)
        for e in m.get("edges", {}).get("groupsWith", []) or []:
            if e.get("ref") is None: continue
            if exclude_nav_family and src == "navigations": continue
            edges.append(("component:" + src, e["ref"]))
        for c in m.get("count", []) or []:
            if isinstance(c, dict) and c.get("per") == "group": edges.append(("component:" + src, "component:" + src))
    parent = {}
    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x: parent[x] = parent[parent[x]]; x = parent[x]
        return x
    for a, b2 in edges: parent[find(a)] = find(b2)
    comps = {}
    for a, b2 in edges: comps.setdefault(find(a), set()).update([a, b2])
    return sorted(sorted(v) for v in comps.values())

def nav(b):
    counts = {
        "as_HEAD_dial_reads_it": dial(False, False),
        "nav_family_not_a_tile_group": dial(True, False),
        "nav_family_not_a_tile_group_and_aliases_followed": dial(True, True),
        "nav_family_a_tile_group_and_aliases_followed": dial(False, True),
        "R6e_expects": [["component:kpi-tile"], ["component:stat-card"]],
    }
    facts["nav_dial"] = counts
    shots = {}
    for way in ("A", "B"):
        pg = page_for(b, f"file://{SH}/tpl.html", 1440, 1180)
        pg.evaluate("() => { const d = document.querySelector('.demo-bar'); if (d) d.style.display = 'none'; }")
        wall = pg.evaluate("() => [...document.querySelectorAll('section.tpl-group')].map(e => e.getAttribute('aria-label'))")
        boxes = [{"sel": "section.tpl-group", "c": C_GRP, "pad": 4,
                  "label": [f"TILE GROUP {i+1} · “{g}”" for i, g in enumerate(wall)]}]
        if way == "A":
            boxes.append({"sel": "header.sh-masthead", "c": C_FRM, "dash": True, "inside": True,
                          "label": "FRAME · the nav family (top nav here; sidebar nav, tab bar elsewhere) · NOT COUNTED"})
            tag = "THE NAV FAMILY ON THE DASHBOARD · COUNT 1 · THE FAMILY IS FRAME, NOT A TILE GROUP · RECOMMENDED · NOT A RULING"
            notes = [f"<b>{len(wall)} tile groups</b> on the wall, as the designer drew them. The top nav (one of the three family members) is frame and is not counted.",
                     "The grouping dial would read the family's #261 edges as a <b>same-answer family</b> (one question: where am I, where can I go), not as tiles that sit together.",
                     "Mechanically: the dial skips the family's edges. The selftest also needs re-basing: since #309 kpi-tile and stat-card are aliases of Metric, so its two expected self-groups become one, " + " + ".join(x.split(':')[1] for x in counts['nav_family_not_a_tile_group_and_aliases_followed'][0]) + ". Then it can be wired blocking (s308-D33)."]
        else:
            boxes.append({"sel": "header.sh-masthead", "c": C_NAV, "inside": True,
                          "label": f"TILE GROUP {len(wall)+1}? · navigations + sidebar-nav + tab-bar · mixed kind · COUNTED BY THE DIAL"})
            tag = "THE NAV FAMILY ON THE DASHBOARD · COUNT 2 · THE FAMILY IS A TILE GROUP · AS THE DIAL READS IT TODAY · NOT A RULING"
            notes = [f"The dial counts a group the designer never drew: <b>{len(wall)} + 1</b>. Two of its three members (sidebar nav, tab bar) are not on this page at all.",
                     "Today the dial's only derived group is this one: " + " + ".join(x.split(':')[1] for x in counts['as_HEAD_dial_reads_it'][0]) + ". The selftest expects kpi-tile and stat-card self-groups instead, so it is red.",
                     "If this is the answer, the template's grammar gains a frame-in-the-wall group, and every bento's option space moves with it."]
        pg.evaluate(ANN_JS, [ANN_CSS, tag, notes, boxes]); pg.wait_for_timeout(150)
        fn = f"{OUT}/F3-2-navfamily-count{'1' if way == 'A' else '2'}-1440.png"
        pg.screenshot(path=fn, full_page=False); shots[way] = {"file": fn, "wall_groups": wall}
        pg.close()
    # the two family members that are not on the page, from their own reference files (as committed)
    pg = page_for(b, f"file://{SH}/Sidebar-nav.html", 1440, 900)
    fn = f"{OUT}/F3-2-family-sidebar-nav-1440.png"; pg.screenshot(path=fn, clip={"x": 0, "y": 40, "width": 780, "height": 620}); shots["sidebar"] = fn; pg.close()
    pg = page_for(b, f"file://{SH}/Tab-bar.html", 390, 844)
    fn = f"{OUT}/F3-2-family-tab-bar-390.png"; pg.screenshot(path=fn, clip={"x": 0, "y": 56, "width": 390, "height": 264}); shots["tabbar"] = fn; pg.close()
    facts["nav"] = shots

with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ.get("RENDER_SHELL"))
    if WHAT in ("sec", "all"): sec(b)
    if WHAT in ("panel", "all"): panel(b)
    if WHAT in ("nav", "all"): nav(b)
    b.close()
json.dump(facts, open(FACTS_P, "w"), indent=1, ensure_ascii=False)
print(json.dumps(facts, indent=1, ensure_ascii=False)[:3000])
