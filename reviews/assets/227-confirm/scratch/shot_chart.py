from playwright.sync_api import sync_playwright
U="file:///sessions/serene-hopeful-pasteur/mnt/UX-design/showroom/chart-line.html"
with sync_playwright() as p:
    b=p.chromium.launch()
    pg=b.new_page(viewport={'width':1400,'height':1000},device_scale_factor=2)
    pg.goto(U); pg.wait_for_timeout(900)
    pg.click('#themes button[data-theme="console"]'); pg.wait_for_timeout(1200)
    fr=pg.frame_locator('#f')
    el=fr.locator('.dv-controls').first
    print("count", fr.locator('.dv-controls').count())
    el.scroll_into_view_if_needed(); pg.wait_for_timeout(300)
    el.screenshot(path='w2-chart-toolbar.png')
    print("OK")
    b.close()
