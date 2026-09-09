"""#261 N2 — drive the three nav surfaces against DAVE'S SIX SENTENCES, four themes x two modes.

goto file:// only (never set_content), per knowledge/_RUNBOOK-render-verify.md. Every assertion
below names the sentence it answers and MEASURES the thing rather than reading the CSS back:
the header is measured by asking whether the head still contains an <img>, the promotion by
clicking the toggle and reading the chip, the rail by clicking the rail toggle and reading the
group's aria-expanded and the chip's box RELATIVE TO THE GLYPH, the underscore by reading the
computed background of the current masthead item, the search alignment by comparing the field's
bottom edge with its container's content-box bottom, and the menu button by clicking it and
checking the island's current destination did NOT move.

Writes 261-N2-nav-<slug>-<theme>-<mode>.png next to this file; prints the receipt as JSON.
"""
import json, os, sys

ROOT = "/sessions/zen-funny-hawking/mnt/UX-design"
sys.path.insert(0, os.path.join(ROOT, "knowledge"))
sys.path.insert(0, os.path.join(ROOT, "knowledge", "canon"))
import gen_theme_cascade as cascade
from playwright.sync_api import sync_playwright

OUT = os.path.join(ROOT, "notes/_lanes")
SPECS = [
    ("sidebar-nav", "knowledge/snippets/Sidebar-nav.reference.html", 1180, 780),
    ("navigations", "knowledge/snippets/Navigations.reference.html", 1180, 300),
    ("tab-bar", "knowledge/snippets/Tab-bar.reference.html", 480, 420),
]
THEMES = ["mono", "legacy", "console", "supercharge"]
receipt = {"themes_x_modes": len(THEMES) * 2, "shots": [], "assertions": []}


def check(name, ok, detail):
    receipt["assertions"].append({"assertion": name, "pass": bool(ok), "measured": detail})


with sync_playwright() as p:
    b = p.chromium.launch()
    for slug, rel, w, h in SPECS:
        snip = os.path.join(ROOT, rel)
        src = open(snip).read()
        man = json.loads(src.split('<script type="application/json" id="token-manifest">')[1]
                         .split("</script>")[0])
        theme_css = cascade.snippet_theme_css(man["vars"], slug)
        pg = b.new_page(viewport={"width": w, "height": h})
        for theme in THEMES:
            for mode in ["light", "dark"]:
                pg.goto("file://" + snip)
                pg.add_style_tag(content=theme_css)
                pg.evaluate(
                    """([t,m]) => { if (t!=='mono') document.documentElement.setAttribute('data-apollo-theme', t);
                       else document.documentElement.removeAttribute('data-apollo-theme');
                       document.body.setAttribute('data-theme', m); }""", [theme, mode])
                pg.wait_for_timeout(140)
                shot = os.path.join(OUT, "261-N2-nav-%s-%s-%s.png" % (slug, theme, mode))
                pg.screenshot(path=shot, full_page=(slug != "sidebar-nav"))
                receipt["shots"].append(os.path.basename(shot))
        pg.close()

    # ---- SIDEBAR: three sentences -------------------------------------------------------
    pg = b.new_page(viewport={"width": 1180, "height": 780})
    pg.goto("file://" + os.path.join(ROOT, "knowledge/snippets/Sidebar-nav.reference.html"))
    pg.wait_for_timeout(120)
    imgs = pg.eval_on_selector_all(".sn-head img", "e=>e.length")
    brand = pg.eval_on_selector_all(".sn-head .sn-brand", "e=>e.map(x=>x.textContent.trim())")
    check("header: 'the original header is better' — no mark, the 7647aaf product row",
          imgs == 0 and brand == ["Business banking"] * 3, {"imgs": imgs, "brand": brand})

    # promotion: frame 1 is expanded; shut the Cards group and read the heading chip
    before = pg.eval_on_selector("#sn1-cards", "e=>!e.hidden")
    chip_before = pg.eval_on_selector("[aria-controls='sn1-cards'] [data-group-count]", "e=>!e.hidden")
    pg.click("[aria-controls='sn1-cards']")
    pg.wait_for_timeout(120)
    after = pg.evaluate("""() => {
      const b = document.querySelector("[aria-controls='sn1-cards']");
      const c = b.querySelector('[data-group-count]');
      return {expanded:b.getAttribute('aria-expanded'), subHidden:document.getElementById('sn1-cards').hidden,
              chipShown:!c.hidden, chipText:c.textContent, name:b.getAttribute('aria-label')}; }""")
    check("promotion: 'the badge should be promoted to the category heading when collapsed'",
          after["chipShown"] and after["chipText"] == "3" and after["subHidden"]
          and after["name"] == "Cards, 3" and chip_before is False and before is True, after)

    # rail: collapse the whole column, groups must shut and the chip must ATTACH to the glyph
    pg.reload(); pg.wait_for_timeout(120)
    pg.click("nav.sn:not(.is-rail) .sn-toggle")
    pg.wait_for_timeout(260)
    rail = pg.evaluate("""() => {
      const nav = document.querySelector('nav.sn');
      const btn = nav.querySelector("[aria-controls='sn1-cards']");
      const chip = btn.querySelector('[data-group-count]');
      const glyph = btn.querySelector('.nv-ic');
      const c = chip.getBoundingClientRect(), g = glyph.getBoundingClientRect();
      return {isRail:nav.classList.contains('is-rail'),
              expanded:btn.getAttribute('aria-expanded'),
              subHidden:document.getElementById('sn1-cards').hidden,
              chipShown:!chip.hidden, chipText:chip.textContent,
              gapX:Math.round(c.left - g.right), gapY:Math.round(g.top - c.bottom),
              overlapsGlyphColumn:c.left < g.right + 12 && c.bottom > g.top - 12}; }""")
    check("rail: 'the submenu should collapse too and the badge promoted to the category level'",
          rail["isRail"] and rail["expanded"] == "false" and rail["subHidden"]
          and rail["chipShown"] and rail["chipText"] == "3", rail)
    check("rail badge ATTACHED to the glyph, not floating below it (tab-bar idiom)",
          rail["overlapsGlyphColumn"] and rail["gapY"] <= 0, rail)
    # and the rail hands the disclosure back on the way out
    pg.click("nav.sn.is-rail .sn-toggle"); pg.wait_for_timeout(260)
    back = pg.evaluate("""() => { const b=document.querySelector("[aria-controls='sn1-cards']");
      return {expanded:b.getAttribute('aria-expanded'),
              chipShown:!b.querySelector('[data-group-count]').hidden}; }""")
    check("rail remembers: the group it shut is handed back on expand",
          back["expanded"] == "true" and back["chipShown"] is False, back)
    pg.close()

    # ---- TOP NAV: two sentences ----------------------------------------------------------
    pg = b.new_page(viewport={"width": 1180, "height": 300})
    pg.goto("file://" + os.path.join(ROOT, "knowledge/snippets/Navigations.reference.html"))
    pg.wait_for_timeout(120)
    cur = pg.eval_on_selector("nav.main .nv-item[aria-current='page']",
                              "e=>{const c=getComputedStyle(e);return {bg:c.backgroundColor, sh:c.boxShadow};}")
    check("top nav: 'the selected state should just have the underscore, no background'",
          cur["bg"] in ("rgba(0, 0, 0, 0)", "transparent") and "inset" in cur["sh"], cur)
    pg.click("#navSearchTrig")
    pg.wait_for_timeout(200)
    align = pg.evaluate("""() => {
      const bar = document.querySelector('.nav-searchbar'); if(!bar || bar.hidden) return {open:false};
      const f = bar.querySelector('.nav-search');
      const cs = getComputedStyle(bar);
      const br = bar.getBoundingClientRect(), fr = f.getBoundingClientRect();
      const contentBottom = br.bottom - parseFloat(cs.borderBottomWidth) - parseFloat(cs.paddingBottom);
      return {open:true, padBottom:cs.paddingBottom,
              gap:Math.round(contentBottom - fr.bottom)}; }""")
    check("top nav: 'align the bottom of the search bar with the bottom of its container'",
          align.get("open") and align["padBottom"] == "0px" and align["gap"] == 0, align)
    pg.close()

    # ---- TAB BAR: the island, and the menu button leaving the exclusive group -------------
    pg = b.new_page(viewport={"width": 480, "height": 420})
    pg.goto("file://" + os.path.join(ROOT, "knowledge/snippets/Tab-bar.reference.html"))
    pg.wait_for_timeout(200)
    glyph = pg.eval_on_selector(".seg .nv-item[aria-current='page'] .nv-ic",
                                "e=>getComputedStyle(e).color")
    fill = pg.eval_on_selector(".seg .ind", "e=>getComputedStyle(e).backgroundColor")
    check("island restored: the SELECTED glyph inherits text/on-inverse, not icon/default",
          glyph == "rgb(255, 255, 255)" and fill == "rgb(0, 0, 0)", {"glyph": glyph, "fill": fill})
    before_ind = pg.eval_on_selector(".seg .ind", "e=>Math.round(e.getBoundingClientRect().width)")
    before_cur = pg.eval_on_selector_all(".seg .nv-item[aria-current='page']",
                                         "e=>e.map(x=>x.getAttribute('aria-label'))")
    pg.click(".menu-fab"); pg.wait_for_timeout(300)
    after_menu = pg.evaluate("""() => ({
      fab: document.querySelector('.menu-fab').getAttribute('aria-expanded'),
      fabIsButton: document.querySelector('.menu-fab').tagName,
      indWidth: Math.round(document.querySelector('.seg .ind').getBoundingClientRect().width),
      current: [...document.querySelectorAll('.seg .nv-item[aria-current="page"]')].map(x=>x.getAttribute('aria-label'))
    })""")
    check("menu button OUT of the exclusive group: the island's current destination does not move",
          after_menu["fab"] == "true" and after_menu["fabIsButton"] == "BUTTON"
          and after_menu["current"] == before_cur == ["Home"]
          and after_menu["indWidth"] == before_ind and before_ind > 0, after_menu)
    pg.close()
    b.close()

receipt["failures"] = [a["assertion"] for a in receipt["assertions"] if not a["pass"]]
print(json.dumps(receipt, indent=2))
