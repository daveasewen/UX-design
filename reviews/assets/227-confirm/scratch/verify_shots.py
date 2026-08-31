from playwright.sync_api import sync_playwright
U="file:///sessions/serene-hopeful-pasteur/mnt/UX-design/reviews/CONFIRM-PASS-2026-08-31-v1.html"
with sync_playwright() as p:
    b=p.chromium.launch()
    for scheme in ('light','dark'):
        ctx=b.new_context(viewport={'width':1000,'height':1200},device_scale_factor=1,color_scheme=scheme)
        pg=ctx.new_page(); pg.goto(U); pg.wait_for_timeout(800)
        pg.eval_on_selector('section.row[data-id="L3-l"]','e=>e.scrollIntoView({block:"start"})'); pg.wait_for_timeout(300)
        pg.screenshot(path=f'scratch/v-{scheme}-row7.png')
        pg.evaluate("window.scrollTo(0,0)"); pg.wait_for_timeout(300)
        pg.screenshot(path=f'scratch/v-{scheme}-top.png')
        ctx.close()
    ctx=b.new_context(viewport={'width':390,'height':900},device_scale_factor=2)
    pg=ctx.new_page(); pg.goto(U); pg.wait_for_timeout(800)
    print("mobile overflow:", pg.evaluate("()=>document.documentElement.scrollWidth>document.documentElement.clientWidth"))
    pg.eval_on_selector('section.row[data-id="L8"]','e=>e.scrollIntoView({block:"start"})'); pg.wait_for_timeout(300)
    pg.screenshot(path='scratch/v-mobile-row3.png')
    ctx.close(); b.close()
    print("OK")
