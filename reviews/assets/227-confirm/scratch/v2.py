from playwright.sync_api import sync_playwright
U="file:///sessions/serene-hopeful-pasteur/mnt/UX-design/reviews/CONFIRM-PASS-2026-08-31-v1.html"
with sync_playwright() as p:
    b=p.chromium.launch()
    ctx=b.new_context(viewport={'width':1000,'height':1300},device_scale_factor=1,color_scheme='light')
    pg=ctx.new_page(); pg.goto(U); pg.wait_for_timeout(800)
    for sel,name in [('section.row[data-id="L1-L2"]','row4'),('section.row[data-id="W2"]','row9'),('section.row[data-id="W3"]','row11')]:
        pg.eval_on_selector(sel,'e=>e.scrollIntoView({block:"start"})'); pg.wait_for_timeout(300)
        pg.screenshot(path=f'scratch/v-light-{name}.png')
    b.close(); print("OK")
