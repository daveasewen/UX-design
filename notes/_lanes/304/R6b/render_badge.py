"""R6b: the nav count badge at padding 7px (as shipped) and 8px (the 4px-grid move), photographed from the
REAL reference snippets (copy, never redraw). Font forced to HSBC_MtUnivers_Latin and asserted loaded.
Writes shots/badge-*.png and badge_measure.json. Run from repo root after ensure_env + seat_env, one call."""
import os, json
from playwright.sync_api import sync_playwright
ROOT = os.getcwd(); OUT = os.path.join(ROOT, 'notes/_lanes/304/R6b/shots'); os.makedirs(OUT, exist_ok=True)
SNIPS = ['Navigations', 'Sidebar-nav', 'Tab-bar']
FORCE = '*{font-family:"HSBC_MtUnivers_Latin","Univers Next for HSBC",sans-serif !important}'
EIGHT = True  # applied in JS: only chips whose computed padding is 7px move to 8px
res = {'font_forced': 'HSBC_MtUnivers_Latin', 'snippets': {}}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ['RENDER_SHELL'])
    for name in SNIPS:
        path = os.path.join(ROOT, 'knowledge/snippets/%s.reference.html' % name)
        r = {}
        for tag, eight in (('7px', False), ('8px', True)):
            ctx = b.new_context(viewport={'width': 1440, 'height': 900}, device_scale_factor=3)
            pg = ctx.new_page(); pg.goto('file://' + path); pg.add_style_tag(content=FORCE); pg.wait_for_timeout(900)
            pg.evaluate("""(eight)=>{document.querySelectorAll('.nv-count').forEach(e=>{const pl=getComputedStyle(e).paddingLeft; if(pl==='7px'){e.setAttribute('data-r6b','seven'); if(eight){e.style.paddingLeft='8px';e.style.paddingRight='8px';}}})}""", eight)
            ok = pg.evaluate("document.fonts.check('12px HSBC_MtUnivers_Latin')")
            loc = pg.locator('[data-r6b=seven]:visible').first
            n7 = pg.locator('[data-r6b=seven]').count()
            if loc.count() == 0:
                r[tag] = {'visible': False}; ctx.close(); continue
            item = loc.locator('xpath=ancestor::*[contains(concat(" ",normalize-space(@class)," ")," nv-item ")][1]')
            info = loc.evaluate("e=>{const cs=getComputedStyle(e);const r=e.getBoundingClientRect();return {text:e.textContent,w:+r.width.toFixed(2),h:+r.height.toFixed(2),pad:cs.paddingLeft+' '+cs.paddingRight,font:cs.fontFamily.split(',')[0],size:cs.fontSize}}")
            widths = {}
            for t in ('3', '12', '128'):
                widths[t] = loc.evaluate("(e,t)=>{const o=e.textContent;e.textContent=t;const w=e.getBoundingClientRect().width;e.textContent=o;return +w.toFixed(2)}", t)
            item.scroll_into_view_if_needed()
            item.screenshot(path=os.path.join(OUT, 'badge-%s-%s.png' % (name, tag)))
            loc.screenshot(path=os.path.join(OUT, 'badge-%s-%s-chip.png' % (name, tag)))
            r[tag] = {'chips_at_7px_in_snippet': n7, 'font_loaded': ok, 'shown': info, 'width_by_count': widths}
            ctx.close()
        res['snippets'][name] = r
    b.close()
json.dump(res, open(os.path.join(ROOT, 'notes/_lanes/304/R6b/badge_measure.json'), 'w'), indent=1)
print(json.dumps(res, indent=1))
