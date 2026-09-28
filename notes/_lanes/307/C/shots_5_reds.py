"""Item 5 — the reds, seen. The catalogue pages (showroom/input-fields.html, showroom/notifications.html)
embed each part's approved reference with its per-theme blocks; the page's own Theme and Light/Dark
buttons are clicked, then the part's error state is photographed inside the frame and the red it
actually paints is read from the computed style. Nothing redrawn."""
import sys; sys.path.insert(0, __file__.rsplit('/',1)[0])
from _lib import *
THEMES = ["mono", "legacy", "console", "supercharge"]
res = {}
with sync_playwright() as p:
    b = launch(p)
    for page_name, sel, probe in [
        ("input-fields", ".field.is-error",
         "e => { const box=e.querySelector('.box'); const ic=e.querySelector('.err-msg .ic'); const cb=getComputedStyle(box);"
         " return {box_border_bottom: cb.borderBottomColor, box_shadow: cb.boxShadow, icon: ic ? getComputedStyle(ic).color : null,"
         " err_var: getComputedStyle(e).getPropertyValue('--error').trim()}; }"),
        ("notifications", ".note.tint.err",
         "e => { const cs=getComputedStyle(e); return {border_left: cs.borderLeftColor, border: cs.borderTopColor, bg: cs.backgroundColor,"
         " err_var: cs.getPropertyValue('--err').trim(), accent: cs.getPropertyValue('--accent').trim()}; }")]:
        pg = b.new_page(viewport={"width": 1200, "height": 900}, device_scale_factor=2)
        pg.goto(url(f"showroom/{page_name}.html")); pg.wait_for_timeout(600)
        for mode in ["light", "dark"]:
            for t in THEMES:
                pg.click(f"#themes button[data-theme='{t}']"); pg.click(f"#modes button[data-mode='{mode}']"); pg.wait_for_timeout(250)
                fr = pg.frame_locator("#f")
                got = pg.evaluate("() => { const d=document.getElementById('f').contentDocument; return [d.documentElement.getAttribute('data-apollo-theme'), d.body.getAttribute('data-theme')]; }")
                el = fr.locator(sel).first
                el.scroll_into_view_if_needed()
                m = el.evaluate(probe); m["applied"] = got
                res[f"{page_name}-{t}-{mode}"] = m
                el.screenshot(path=str(OUT / f"5-{page_name}-{t}-{mode}.png"))
        pg.close()
    b.close()
save_json("5-reds-measures.json", res)
for k, v in res.items(): print(k, v)
