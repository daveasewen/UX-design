"""#312 lane F4 — renders for four of Dave's stalled calls, in the four themes (mono, legacy,
supercharge, console), from the committed canon (git show <sha>), never the mount's dirty tree:
  donut   item 3  the ring 'set to fill' vs ds-030 'does not stretch' (s305-D59, W-305n2): his sketch —
                  a 4px-grid size with a lower and an upper band, the best size computed at build time.
  rails   item 7  the rails half of s305-D10 (W-305w2): the bento-editor ground word for surface/section.
  roundel item 9  the dark RAG roundels painted pure white by policy while icon/default softened (s311-D1).
  header  item 6  a header component for bento groups (W-305e4) and two linked subjects as one group (W-305e5).
Usage (at the seat, ONE bash call per item):
  export TMPDIR=/dev/shm; bash knowledge/_render/ensure_env.sh; source knowledge/_render/seat_env.sh
  python3 notes/_lanes/312/F/F4/render_F4.py <sha> <donut|rails|roundel|header>
Writes notes/_lanes/312/F/F4/img/F4-*.png and img/F4-facts.json (merged per run).
Every drawn option is a proposal for Dave's eye, not a ruling."""
import os, sys, json, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from f4_common import R, SH, OUT, THEMES, sha, show, body_of, sprite, page, compose, COLOR_JS
from playwright.sync_api import sync_playwright
REF = sys.argv[1] if len(sys.argv) > 1 else "HEAD"; WHAT = sys.argv[2] if len(sys.argv) > 2 else "roundel"
SHA = sha(REF)
FACTS_P = f"{OUT}/F4-facts.json"
facts = json.load(open(FACTS_P)) if os.path.exists(FACTS_P) else {}
facts.update({"sha": SHA, "canon": f"git show {SHA[:8]}:knowledge/canon/canon.css", "themes": THEMES})

def newpage(b, url, w=1440, h=900):
    pg = b.new_page(viewport={"width": w, "height": h}, reduced_motion="reduce")
    pg.goto(url); pg.wait_for_timeout(500); pg.evaluate(COLOR_JS); return pg

# ------------------------------------------------------------------ item 9 · the dark RAG roundels
def roundel(b):
    spr = sprite("Notifications.reference.html") + sprite("Input-fields.reference.html")
    kinds = [("err", "ic-error", "Payment rejected."), ("warn", "ic-warning", "Cut-off in 48 minutes."),
             ("ok", "ic-success", "File accepted."), ("info", "ic-info", "Rates refresh at 16:00.")]
    def col(cls, title):
        notes = "".join(f'<div class="note tint {k}" role="status"><span class="ic"><svg aria-hidden="true"><use href="#{i}"/></svg></span>'
                        f'<span class="main"><strong>{t}</strong> Message description.</span></div>' for k, i, t in kinds)
        inl = "".join(f'<span class="inline {k}"><span class="ic"><svg aria-hidden="true"><use href="#{i}"/></svg></span>Message to appear here</span>'
                      for k, i, _ in kinds)
        err = ('<div class="cn-input-fields"><div class="err-msg"><span class="ic" aria-hidden="true"><svg class="icn" viewBox="0 0 18 18">'
               '<use href="#ic-error"/></svg></span><p>Enter a valid amount.</p></div></div>')
        return (f'<div class="f4col {cls}"><h3 class="f4h">{title}</h3><div class="cn-notifications">{notes}'
                f'<div class="f4inl">{inl}</div></div>{err}</div>')
    css = ("<style>body{margin:0;padding:16px} .f4wrap{display:grid;grid-template-columns:1fr 1fr;gap:24px}"
           ".f4h{font:700 13px/1.2 Helvetica,Arial,sans-serif;letter-spacing:.06em;text-transform:uppercase;color:var(--text);margin:0 0 8px}"
           ".f4inl{margin-top:12px;display:flex;flex-direction:column;gap:6px}.f4wrap .note{margin:6px 0} .f4follow .ic{color:var(--icon-default) !important}</style>")
    body = spr + '<div class="f4wrap">' + col("f4built", "As built · pure white by policy") + col("f4follow", "Following the ink · icon/default") + "</div>"
    cells, meas = [], {}
    for th in THEMES:
        url = page(f"roundel-{th}", th, "dark", body, css)
        pg = newpage(b, url, 684, 420)
        m = pg.evaluate("""() => { const g = (sel) => [...document.querySelectorAll(sel)];
          const one = (root) => g(root + ' .note.tint').map(n => ({kind: n.className.split(' ').pop(),
              ic: f4hex(getComputedStyle(n.querySelector('.ic')).color), ground: f4hex(getComputedStyle(n).backgroundColor)}))
            .map(x => Object.assign(x, {cr: f4cr(x.ic, x.ground)}));
          return {built: one('.f4built'), follow: one('.f4follow'),
                  inline_built: g('.f4built .inline .ic').map(e => f4hex(getComputedStyle(e).color)),
                  errmsg_built: g('.f4built .err-msg .ic').map(e => f4hex(getComputedStyle(e).color)),
                  icon_default: f4hex(getComputedStyle(document.querySelector('.f4follow .ic')).color)}; }""")
        h = pg.evaluate("() => document.documentElement.scrollHeight")
        fn = f"{OUT}/F4-9-roundels-{th}-dark.png"; pg.screenshot(path=fn, full_page=True, clip={"x": 0, "y": 0, "width": 684, "height": h}); pg.close()
        meas[th] = m
        lo_b = min(x['cr'] for x in m['built']); lo_f = min(x['cr'] for x in m['follow'])
        cells.append((fn, f"<b>{th}</b>, dark · roundel {m['built'][0]['ic']} as built, {m['icon_default']} following the ink · lowest contrast on a tint {lo_b}:1 → {lo_f}:1"))
    css_txt = open(f"{SH}/canon.css").read()
    rules = re.findall(r'\[data-theme="dark"\] :where\(\.(cn-[a-z-]+)\)[^{]*\.ic\{color:#FFFFFF;\}', css_txt)
    nscope, nrule = len(set(rules)), len(rules)
    facts["roundel"] = meas; facts["roundel_white_rules"] = {"rules": nrule, "scopes": sorted(set(rules))}
    compose(b, f"{OUT}/F4-9-roundels-dark-4themes.png",
            "THE DARK RAG ROUNDELS · FOUR THEMES, DARK · AS BUILT (LEFT) AND FOLLOWING THE INK (RIGHT) · A DRAWN OPTION, NOT A RULING",
            ["In dark mode " + str(nscope) + " canon scopes (" + str(nrule) + " rules, components and templates) paint the status roundel <b>pure white</b> by the 2026-07-02 white-shape-black-mark policy, while s311-D1 softened icon/default to the ink.",
             "Right: the same notes with the roundel taking <b>icon/default</b>. The status still rides the shape and the tint ground; only the white softens.",
             "Measured per theme in the facts file: the roundel's colour and its contrast on each tint ground, both ways."],
            cells, cols=2)

# ------------------------------------------------------------------ item 7 · the rails ramp word
def tpl_body():
    bd = body_of("Template-dashboard-bento.reference.html")
    return re.sub(r'<div class="demo-bar">[\s\S]*?</div>', '', bd, count=1)

def tpl_scripts():
    s = show("knowledge/snippets/Template-dashboard-bento.reference.html")
    return "".join(x for x in re.findall(r'<script(?![^>]*application/json)[\s\S]*?</script>', s) if 'themeBtn' not in x)

def rails(b):
    body = '<div class="cn-template-dashboard-bento">' + tpl_body() + "</div>" + tpl_scripts()
    css_word = {"section": "", "grey": "<style>.cn-template-dashboard-bento .tpl-page{background:var(--surface-subtle) !important}</style>"}
    meas, sheets = {}, {}
    for md in ("light", "dark"):
        cells = []
        for th in THEMES:
            for word in ("grey", "section"):
                url = page(f"rails-{th}-{md}-{word}", th, md, body, css_word[word], body_cls="canon tpl-bento-body")
                pg = newpage(b, url, 1440, 1000); pg.wait_for_timeout(300)
                m = pg.evaluate("""() => { const bg = e => f4hex(getComputedStyle(e).backgroundColor);
                  const wall = document.querySelector('.tpl-page'), tile = document.querySelector('.kpi-tile');
                  const r = wall.getBoundingClientRect();
                  const o = {page: bg(document.body), header: bg(document.querySelector('.tpl-header')) , wall: bg(wall), tile: bg(tile), top: Math.round(r.top + scrollY)};
                  o.wall_vs_tile = f4cr(o.wall, o.tile); return o; }""")
                fn = f"{OUT}/F4-7-rails-{th}-{md}-{word}.png"
                pg.screenshot(path=fn, clip={"x": 0, "y": max(0, m["top"] - 120), "width": 1440, "height": 560}); pg.close()
                meas[f"{th}/{md}/{word}"] = m
                lab = "“grey” · surface/subtle · what the editor rails can record today" if word == "grey" else "the new word · surface/section · what canon paints today"
                cells.append((fn, f"<b>{th}</b>, {md} · {lab} · ground {m['wall']} under tiles {m['tile']} · contrast {m['wall_vs_tile']}:1"))
        fn = f"{OUT}/F4-7-rails-4themes-{md}.png"; sheets[md] = fn
        same = [th for th in THEMES if meas[f"{th}/{md}/grey"]["wall"] == meas[f"{th}/{md}/section"]["wall"]]
        if md == "light":
            n2 = (f"In light the two words paint the <b>same colour</b> in {len(same)} of 4 themes (" +
                  ", ".join(f"{th} {meas[f'{th}/light/section']['wall']}" for th in THEMES) + "): the word changes nothing here.")
        else:
            n2 = ("In dark they part by one step: " + "; ".join(f"{th} grey {meas[f'{th}/dark/grey']['wall']} vs section {meas[f'{th}/dark/section']['wall']}" for th in THEMES) +
                  f". Section equals the dark page ground ({meas['mono/dark/section']['page']} in mono), so the wall meets the page with no edge; the tiles keep theirs.")
        compose(b, fn, f"THE BENTO GROUND WORD · FOUR THEMES, {md.upper()} · LEFT: THE RAILS' “GREY” · RIGHT: SURFACE/SECTION · A DRAWN OPTION, NOT A RULING",
                ["s305-D10 put the dashboard's section ground on surface/section, and canon's template paints it (right). The bento editor's ground words are grey, white, dark grey and transparent; none is bound to surface/section, so the rails cannot record what canon draws (left: the nearest word, grey).",
                 n2,
                 "The call: a fifth ground word bound to surface/section (its name is his), and its scope: the dashboard only, or every bento type."],
                cells, cols=2)
    facts["rails"] = {"measured": meas, "sheets": sheets, "ground_words_today": ["grey=--surface-subtle", "white=--surface-raised", "darkgrey=--surface-digital-black", "transparent=(none)"],
                      "source": "knowledge/_render/gen_bento_matrix_217.py GROUND_RAMP"}

# ------------------------------------------------------------------ item 6 · a header for bento groups
ARROW = None
def group_header(label, action=True):
    global ARROW
    if ARROW is None:
        s = show("knowledge/snippets/Section-heading-lockup.reference.html")
        m = re.search(r'<a class="arrow"[\s\S]*?</a>', s); ARROW = m.group(0) if m else '<a class="arrow" href="#"><span class="lbl t-cm-button">View all</span></a>'
    act = ARROW if action else ""
    return (f'<div class="cn-section-heading-lockup f4-gh"><div class="l-row" data-justify="between" data-align="baseline">'
            f'<h2 class="t-cm-section-label">{label}</h2>{act}</div></div>')

def header(b):
    body = sprite("Section-heading-lockup.reference.html") + '<div class="cn-template-dashboard-bento">' + tpl_body() + "</div>" + tpl_scripts()
    css = ("<style>.f4-gh{padding:0 0 12px}.f4-gh h2{margin:0}"
           ".f4-band{background:var(--surface-raised);padding:16px 24px;margin-bottom:var(--bento-gutter,4px)}"
           ".f4-band .f4-gh{padding:0}</style>")
    JS = r"""([opt, hA, hB, hC]) => {
      const groups = [...document.querySelectorAll('section.tpl-group')];
      const H = {'This month': hA[0], 'Spending analysis': hA[1], 'Position': hA[2]};
      if (opt === 'A') groups.forEach(g => { const d = document.createElement('div'); d.innerHTML = H[g.getAttribute('aria-label')]; g.insertBefore(d.firstChild, g.firstChild); g.style.background = 'transparent'; });
      if (opt === 'B') groups.forEach(g => { const d = document.createElement('div'); d.className = 'f4-band'; d.innerHTML = H[g.getAttribute('aria-label')]; g.insertBefore(d, g.firstChild); });
      if (opt === 'C') {
        const d = document.createElement('div'); d.innerHTML = hA[0]; groups[0].insertBefore(d.firstChild, groups[0].firstChild);
        groups[0].style.background = 'transparent';
        // two linked subjects, one group: one header over both cells, the outer gutter between them closed to the inner one
        const wallGrid = groups[1].parentElement; const hd = document.createElement('div'); hd.innerHTML = hC;
        const h = hd.firstChild; h.style.gridColumn = '1 / -1'; h.style.marginBottom = 'calc(-1 * var(--bento-dashboard-main, 40px) + 0px)';
        wallGrid.insertBefore(h, groups[1]);
        const gap = getComputedStyle(wallGrid).columnGap; groups[2].style.marginInlineStart = 'calc(-1 * ' + gap + ' + var(--bento-dashboard-sub, 4px))';
        groups[1].style.background = groups[2].style.background = 'transparent';
      }
      return groups.map(g => g.getAttribute('aria-label')); }"""
    hA = [group_header("This month", False), group_header("Spending analysis"), group_header("Position")]
    hC = group_header("Spending and position · two linked subjects, one group")
    runs = [("A", th, "light") for th in THEMES] + [("A", "console", "dark"), ("B", "mono", "light"), ("C", "mono", "light")]
    shots = {}
    for opt, th, md in runs:
        url = page(f"hdr-{opt}-{th}-{md}", th, md, body, css, body_cls="canon tpl-bento-body")
        pg = newpage(b, url, 1440, 1100); pg.wait_for_timeout(300)
        pg.evaluate(JS, [opt, hA, None, hC]); pg.wait_for_timeout(300)
        top = pg.evaluate("() => Math.round(document.querySelector('.tpl-page').getBoundingClientRect().top + scrollY)")
        fn = f"{OUT}/F4-6-groupheader-{opt}-{th}-{md}.png"
        pg.screenshot(path=fn, clip={"x": 0, "y": max(0, top - 24), "width": 1440, "height": 760}); pg.close()
        shots[f"{opt}/{th}/{md}"] = fn
    facts["header"] = {"shots": shots, "component": "Section heading lock-up (knowledge/snippets/Section-heading-lockup.reference.html, arrangement B; arrangement A label-only for 'This month')"}
    compose(b, f"{OUT}/F4-6-groupheader-options.png",
            "A HEADER FOR BENTO GROUPS · THREE DRAWN OPTIONS (MONO, LIGHT) · A IS RECOMMENDED · NOT A RULING",
            ["<b>A</b> · the group's header is the Section heading lock-up, sitting on the wall above the group's tiles: a label, and a trailing action when the group has one.",
             "<b>B</b> · the same lock-up inside the group, as a full-width band on the tile surface. It reads as one more tile and costs a row.",
             "<b>C</b> · his second question: two linked subjects as ONE group — one header over both, the outer gutter between them closed to the inner one."],
            [(shots["A/mono/light"], "<b>A</b> · header on the wall, above the tiles (recommended)"),
             (shots["B/mono/light"], "<b>B</b> · header as a band inside the group"),
             (shots["C/mono/light"], "<b>C</b> · two linked subjects under one header, one group")], cols=1, cell_w=1100)
    compose(b, f"{OUT}/F4-6-groupheader-A-4themes.png",
            "A HEADER FOR BENTO GROUPS · OPTION A IN THE FOUR THEMES (LIGHT) AND CONSOLE DARK · NOT A RULING",
            ["The lock-up takes each theme's own type, ink and action style; nothing new is minted.",
             "The header sits in the group's cell, so it moves with the group when the wall re-flows.",
             "Labelled groups also give each group a visible name, which today lives only in its aria-label."],
            [(shots[f"A/{th}/light"], f"<b>{th}</b>, light") for th in THEMES] + [(shots["A/console/dark"], "<b>console</b>, dark")], cols=2)

# ------------------------------------------------------------------ item 3 · the ring's size bands
DATA = {"type": "donut", "categories": ["GBP", "USD", "EUR", "SGD", "AED"],
        "series": [{"name": "Cash", "values": [6140, 4820, 3210, 2380, 1870]}],
        "unit": "£k", "categoryLabel": "Currency", "caption": "Available cash by currency, thousands of pounds"}
WIDTHS = [320, 440, 560, 720]
HI = 280   # PROPOSED upper band, Dave's to set — not a measurement
def donut(b):
    js = show("knowledge/canon/dv-render.js") + "\n" + show("knowledge/canon/dv-render-donut.js")
    open(f"{SH}/dv.js", "w").write(js)
    keys = "ABCDE"
    leg = "".join(f'<li class="dv-legrow" data-series="{i+1}"><span class="dv-leg-sw" role="checkbox" aria-checked="true" tabindex="0" style="--sc:var(--data-series-{i+1})"></span>'
                  f'<button type="button" class="dv-leg-item t-cm-chart-label" data-series="{i+1}" aria-pressed="false"><span class="dv-key t-cm-chart-key">{keys[i]}</span>'
                  f'<span class="dv-leg-name">{c}</span></button></li>' for i, c in enumerate(DATA["categories"]))
    def fig(row, w):
        return (f'<div class="f4t" data-row="{row}" data-w="{w}" style="width:{w}px"><div class="cn-chart-donut"><figure class="dv" data-dv-type="donut" data-total="18420" '
                f'data-surface="page" data-labelling="spider" role="group" aria-label="Available cash by currency">'
                f'<div class="dv-stage"><div class="dv-donut-row"><svg class="dv-svg" data-h="260" width="300" height="260" viewBox="0 0 300 260" role="group"></svg>'
                f'<ul class="dv-leg vert t-cm-chart-label">{leg}</ul></div></div></figure></div><p class="f4cap"></p></div>')
    rows = "".join(f'<h3 class="f4h">{t}</h3><div class="f4row">' + "".join(fig(r, w) for w in WIDTHS) + "</div>"
                   for r, t in (("today", "Today · fixed 200 px ring in every tile (ds-030 as built)"),
                                ("band", f"His sketch · the ring sized at build time on the 4 px grid, between a lower and an upper band")))
    css = ("<style>body{margin:0;padding:24px;background:var(--surface-section) !important} .f4row{display:flex;gap:16px;align-items:flex-start;margin-bottom:32px}"
           ".f4t{background:var(--surface-raised);padding:24px;box-sizing:border-box;overflow:hidden;flex:none;outline:1px dashed var(--text);outline-offset:-1px}"
           ".f4h{font:700 13px/1.2 Helvetica,Arial,sans-serif;letter-spacing:.06em;text-transform:uppercase;color:var(--text);margin:0 0 12px}"
           ".f4cap{font:12px/1.4 Helvetica,Arial,sans-serif;color:var(--text);margin:12px 0 0;opacity:.8}"
           ".f4t .dv-donut-row.f4stack{flex-direction:column;align-items:flex-start}"
           ".f4t figure table, .f4t figure .dv-tablepanel, .f4t figure details, .f4t figure .dv-sr{display:none !important}</style>"
           f'<script src="file://{SH}/dv.js"></script>')
    JS = r"""([DATA, HI]) => {
      const draw = (f, d) => { const s = f.querySelector('svg.dv-svg'); const H = d + 60, W = d + 100;
        s.setAttribute('data-h', H); s.setAttribute('width', W); s.setAttribute('height', H); s.setAttribute('viewBox', `0 0 ${W} ${H}`);
        dvRender(f, JSON.parse(JSON.stringify(DATA))); };
      const tiles = [...document.querySelectorAll('.f4t')];
      // measure once: the total's width in the hole and the legend's width, at the as-built 200 px
      const p = tiles[0].querySelector('figure'); draw(p, 200);
      const tw = p.querySelector('text.dv-val').getBBox().width;
      const lw = tiles[0].querySelector('.dv-leg').getBoundingClientRect().width;
      const gap = parseFloat(getComputedStyle(tiles[0].querySelector('.dv-donut-row')).columnGap) || 0;
      const f4 = x => Math.floor(x / 4) * 4, c4 = x => Math.ceil(x / 4) * 4;
      const LO = c4((tw + 16) / 0.6);
      const out = [];
      tiles.forEach(t => { const w = +t.dataset.w, inner = w - 48, f = t.querySelector('figure'), row = t.querySelector('.dv-donut-row'), cap = t.querySelector('.f4cap');
        let d, why, stack = false;
        if (t.dataset.row === 'today') { d = 200; draw(f, d);
          const need = Math.round(300 + gap + lw); why = need > inner ? `the legend cannot sit beside it (needs ${need} px, the tile has ${inner})` : `${Math.round(inner - need)} px of the tile left empty beside it`; }
        else { let fit = f4(inner - lw - gap - 100);
          if (fit < LO) { stack = true; row.classList.add('f4stack'); fit = f4(inner - 100); }
          d = Math.max(LO, Math.min(HI, fit));
          why = (fit > HI ? 'held at the upper band' : fit < LO ? 'held at the lower band' : 'fits') + (stack ? ', legend under the ring' : ', legend beside');
          draw(f, d); }
        cap.textContent = `tile ${w} px → ring ${d} px · ${why}`;
        out.push({row: t.dataset.row, tile: w, ring: d, why, stacked: stack}); });
      return {tw: Math.round(tw * 10) / 10, lw: Math.round(lw), gap, LO, HI, tiles: out}; }"""
    meas, cells = {}, []
    for md in ("light", "dark"):
        for th in THEMES:
            url = page(f"donut-{th}-{md}", th, md, rows, css)
            pg = newpage(b, url, 2160, 1000); pg.wait_for_timeout(300)
            m = pg.evaluate(JS, [DATA, HI]); pg.wait_for_timeout(300)
            h = pg.evaluate("() => document.documentElement.scrollHeight")
            fn = f"{OUT}/F4-3-donut-bands-{th}-{md}.png"; pg.screenshot(path=fn, full_page=True, clip={"x": 0, "y": 0, "width": 2160, "height": h}); pg.close()
            meas[f"{th}/{md}"] = m; cells.append((fn, f"<b>{th}</b>, {md}"))
    facts["donut"] = {"measured": meas, "upper_band_px": HI, "upper_band_is": "PROPOSED, Dave's to set — not measured",
                      "lower_band_rule": "ceil4((width of the centre total + 16) / 0.6): the hole (ri = 0.6 ro, dv-render-donut.js) must hold the total",
                      "data": DATA, "tile_widths_px": WIDTHS}
    m0 = meas["mono/light"]
    for md in ("light", "dark"):
        compose(b, f"{OUT}/F4-3-donut-bands-4themes-{md}.png",
                f"THE RING'S SIZE · FOUR THEMES, {md.upper()} · TOP ROW TODAY, BOTTOM ROW HIS BANDED SKETCH · A DRAWN OPTION, NOT A RULING",
                [f"Today the ring is a fixed 200 px in every tile (ds-030): it overflows a narrow tile and floats in a wide one.",
                 f"His sketch, drawn: at build time the ring takes the largest size on the 4 px grid that fits beside its legend, held between a <b>lower band of {m0['LO']} px</b> (the hole must hold the total: measured {m0['tw']} px + 16, ÷ 0.6) and an <b>upper band of {HI} px</b> (proposed).",
                 "Below the lower band the legend drops under the ring rather than the ring shrinking. Edit mode could step the size by 4 px within the bands."],
                [c for c in cells if f", {md}" in c[1]], cols=1, cell_w=1392)

with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ["RENDER_SHELL"])
    {"roundel": roundel, "rails": rails, "header": header, "donut": donut}[WHAT](b)
    b.close()
json.dump(facts, open(FACTS_P, "w"), indent=1, ensure_ascii=False)
print(json.dumps({k: (v if k in ("sha",) else "…") for k, v in facts.items()}), WHAT, "done")
