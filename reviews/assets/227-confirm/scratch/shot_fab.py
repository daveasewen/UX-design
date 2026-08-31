from playwright.sync_api import sync_playwright
U="file:///sessions/serene-hopeful-pasteur/mnt/UX-design/reviews/FAB-READINGS-2026-08-30-v1.html"
with sync_playwright() as p:
    b=p.chromium.launch()
    pg=b.new_page(viewport={'width':1400,'height':1100},device_scale_factor=2)
    msgs=[]; pg.on('console', lambda m: msgs.append(m.type+':'+m.text[:120]))
    pg.goto(U); pg.wait_for_timeout(2500)
    try:
        pg.click('#hintToggle'); pg.wait_for_timeout(400)
    except Exception as e: print("hint click failed", e)
    # hover the corner of frame B
    box = pg.evaluate("""()=>{const w=document.getElementById('wrapB');const r=w.getBoundingClientRect();return {x:r.x,y:r.y,w:r.width,h:r.height};}""")
    print("wrapB box", box)
    pg.mouse.move(box['x']+box['w']-24, box['y']+box['h']-24)
    pg.wait_for_timeout(900)
    el=pg.query_selector('#wrapB').evaluate_handle("e=>e.closest('section.pane')")
    el.as_element().screenshot(path='l1l2-fab-corner-b.png')
    print("OK"); print("CONSOLE:", msgs[:6])
    b.close()
