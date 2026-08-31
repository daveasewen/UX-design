from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch()
    pg=b.new_page(viewport={'width':1280,'height':800},device_scale_factor=2)
    pg.goto('file:///sessions/serene-hopeful-pasteur/mnt/UX-design/reviews/SEGMENTED-RULING-2026-08-30-v1.html')
    pg.wait_for_timeout(600)
    print("TITLE:",pg.title()); print("RENDER OK")
    b.close()
