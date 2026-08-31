from playwright.sync_api import sync_playwright
U="file:///sessions/serene-hopeful-pasteur/mnt/UX-design/reviews/FAB-READINGS-2026-08-30-v1.html"
with sync_playwright() as p:
    b=p.chromium.launch()
    pg=b.new_page(viewport={'width':1400,'height':1100},device_scale_factor=2)
    pg.goto(U); pg.wait_for_timeout(2500)
    pg.click('#hintToggle'); pg.wait_for_timeout(400)
    box = pg.evaluate("()=>{const r=document.getElementById('wrapB').getBoundingClientRect();return {x:r.x,y:r.y,w:r.width,h:r.height};}")
    pg.mouse.move(box['x']+box['w']-30, box['y']+box['h']-30); pg.wait_for_timeout(1200)
    # what is in the corner?
    print(pg.evaluate("()=>{const w=document.getElementById('wrapB');const els=[...w.querySelectorAll('*')].map(e=>e.className&&(''+e.className)).filter(Boolean);return els.slice(0,20);}"))
    W,H=320,300
    clip={'x':box['x']+box['w']-W,'y':box['y']+box['h']-H,'width':W,'height':H}
    pg.screenshot(path='l1l2-fab-corner-b.png', clip=clip)
    print("OK", clip)
    b.close()
