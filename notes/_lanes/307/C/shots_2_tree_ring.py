"""Item 2 — the tree's selection mark and the day that is both today and chosen.
Real reference snippets, opened as files, mode switched by body[data-theme] (the snippets' own switch):
  knowledge/snippets/Calendar.reference.html   'The cell treatments, isolated' row (#states-table)
  knowledge/snippets/Date-picker.reference.html the live panel, opened on today's date typed in
  knowledge/snippets/Tree.reference.html        'The states, drawn' — the selected node
  knowledge/snippets/Sidebar-nav.reference.html the current-page row, for comparison
The 'old way' shots re-apply the pre-repair rule as a MUTATION (the #210 receipt's own control):
  .is-today[aria-selected=true]{box-shadow: inset 0 0 0 2px var(--border-active)}"""
import sys; sys.path.insert(0, __file__.rsplit('/',1)[0])
from _lib import *

OLD_CAL = ".cal-day.is-today[aria-selected=\"true\"]{box-shadow:inset 0 0 0 2px var(--border-active)!important}"
OLD_DP  = ".dp-day.is-today[aria-selected=\"true\"]{box-shadow:inset 0 0 0 2px var(--border-active)!important}"
PROPOSAL = ".cal-day.is-today[aria-selected=\"true\"]{box-shadow:inset 0 0 0 3px var(--text), inset 0 0 0 5px var(--page)!important}"
res = {}
def shot_pad(pg, loc, path, pad=14):
    """clip with the part's own page ground around it, so a ring drawn in the page colour is seen
    against that page colour and not against the review page"""
    # neighbouring cells sit 4px away; hide them for this one picture so only the cell's own
    # page ground surrounds it
    loc.evaluate("e => { const tr=e.closest('tr'); if(tr) tr.querySelectorAll('.cal-day').forEach(x => { if(x!==e) x.style.visibility='hidden'; }); }")
    bb = loc.bounding_box()
    pg.screenshot(path=path, clip={"x": bb["x"]-pad, "y": bb["y"]-pad, "width": bb["width"]+2*pad, "height": bb["height"]+2*pad})
    loc.evaluate("e => { const tr=e.closest('tr'); if(tr) tr.querySelectorAll('.cal-day').forEach(x => x.style.visibility=''); }")

def ringpx(el):
    return el.evaluate("e => { const cs=getComputedStyle(e); return {bg: cs.backgroundColor, shadow: cs.boxShadow, color: cs.color}; }")

with sync_playwright() as p:
    b = launch(p)
    for mode in ["light", "dark"]:
        # --- calendar cell row, 4x
        pg = b.new_page(viewport={"width": 1000, "height": 900}, device_scale_factor=4)
        pg.goto(url("knowledge/snippets/Calendar.reference.html")); fonts_ready(pg)
        pg.evaluate("m => document.body.setAttribute('data-theme', m)", mode); pg.wait_for_timeout(100)
        row = pg.locator("#states-table tr").first
        row.screenshot(path=str(OUT / f"2-cal-cells-{mode}.png"))
        c = pg.locator("#cell-today-selected")
        m = ringpx(c); res[f"cal-now-{mode}"] = m
        shot_pad(pg, c, str(OUT / f"2-cal-todaysel-now-{mode}.png"))
        shot_pad(pg, pg.locator("#states-table button[aria-label^='Selected']"), str(OUT / f"2-cal-selonly-{mode}.png"))
        shot_pad(pg, pg.locator("#states-table button[aria-label^='Today,']"), str(OUT / f"2-cal-todayonly-{mode}.png"))
        # A PROPOSAL, not canon: one line, the fill's own edge kept and the page-colour ring set inside it
        st = pg.add_style_tag(content=PROPOSAL); pg.wait_for_timeout(50)
        res[f"cal-proposal-{mode}"] = ringpx(c)
        shot_pad(pg, c, str(OUT / f"2-cal-todaysel-proposal-{mode}.png"))
        st.evaluate("e => e.remove()"); pg.wait_for_timeout(50)
        pg.add_style_tag(content=OLD_CAL); pg.wait_for_timeout(50)
        res[f"cal-old-{mode}"] = ringpx(c)
        shot_pad(pg, c, str(OUT / f"2-cal-todaysel-old-{mode}.png"))
        pg.close()
        # --- date picker live panel on today, 2x
        pg = b.new_page(viewport={"width": 900, "height": 1000}, device_scale_factor=2)
        pg.goto(url("knowledge/snippets/Date-picker.reference.html")); fonts_ready(pg)
        pg.evaluate("m => document.body.setAttribute('data-theme', m)", mode)
        today = pg.evaluate("() => { const d=new Date(); const p=n=>(n<10?'0':'')+n; return p(d.getDate())+'/'+p(d.getMonth()+1)+'/'+d.getFullYear(); }")
        pg.fill("#f-date", today); pg.press("#f-date", "Tab")
        pg.click("#dp-open"); pg.wait_for_timeout(200)
        # the panel moves focus onto the chosen day; the focus outline would sit over the ring we are
        # showing, so focus is taken off (blur); the panel is asserted still open
        pg.evaluate("() => { document.activeElement && document.activeElement.blur(); }")
        assert pg.locator("#dp-panel").is_visible(), "panel closed on blur"
        pg.wait_for_timeout(100)
        cell = pg.locator("#dp-grid .dp-day.is-today")
        res[f"dp-now-{mode}"] = dict(ringpx(cell), today=today, selected=cell.get_attribute("aria-selected"))
        pg.locator("#dp-panel").screenshot(path=str(OUT / f"2-dp-panel-{mode}.png"))
        pg.close()
        # --- tree selected node, 2x
        pg = b.new_page(viewport={"width": 1200, "height": 1000}, device_scale_factor=2)
        pg.goto(url("knowledge/snippets/Tree.reference.html")); fonts_ready(pg)
        pg.evaluate("m => document.body.setAttribute('data-theme', m)", mode); pg.wait_for_timeout(100)
        tree = pg.locator("ul.tr[aria-label='Tree states']")
        pg.locator(".tr-panel", has=tree).first.screenshot(path=str(OUT / f"2-tree-states-{mode}.png"))
        sel = tree.locator("li[aria-selected='true'] > .tr-row").first
        res[f"tree-sel-{mode}"] = ringpx(sel)
        lab = sel.evaluate("e => { const l=e.querySelector('[class*=label]')||e; return {ch:l.clientHeight, sh:l.scrollHeight}; }")
        res[f"tree-sel-{mode}"]["label_clip"] = lab
        pg.close()
        # --- sidebar nav current row, 2x
        pg = b.new_page(viewport={"width": 1200, "height": 1000}, device_scale_factor=2)
        pg.goto(url("knowledge/snippets/Sidebar-nav.reference.html")); fonts_ready(pg)
        pg.evaluate("m => document.body.setAttribute('data-theme', m)", mode); pg.wait_for_timeout(100)
        grp = pg.locator(".sn-group", has=pg.locator(".nv-item[aria-current='page']")).first
        grp.screenshot(path=str(OUT / f"2-nav-current-{mode}.png"))
        res[f"nav-cur-{mode}"] = ringpx(pg.locator(".sn .nv-item[aria-current='page']").first)
        pg.close()
    b.close()
save_json("2-tree-ring-measures.json", res)
for k, v in res.items(): print(k, v)
