from playwright.sync_api import sync_playwright
U="file:///sessions/serene-hopeful-pasteur/mnt/UX-design/reviews/FAB-READINGS-2026-08-30-v1.html"
with sync_playwright() as p:
    b=p.chromium.launch()
    pg=b.new_page(viewport={'width':1400,'height':1400},device_scale_factor=3)
    pg.goto(U); pg.wait_for_timeout(2500)
    pg.click('#hintToggle'); pg.wait_for_timeout(300)
    pg.eval_on_selector('#wrapB','e=>e.scrollIntoView({block:"center"})'); pg.wait_for_timeout(500)
    box = pg.evaluate("()=>{const r=document.getElementById('wrapB').getBoundingClientRect();return {x:r.x,y:r.y,w:r.width,h:r.height};}")
    print("box",box)
    pg.mouse.move(box['x']+box['w']-30, box['y']+box['h']-30); pg.wait_for_timeout(1500)
    print(pg.evaluate("""()=>{const w=document.getElementById('wrapB');
      const btn=w.querySelector('.af-btn'), hint=w.querySelector('.af-hint');
      const cb=btn?getComputedStyle(btn):null, ch=hint?getComputedStyle(hint):null;
      return {btn_op:cb&&cb.opacity, btn_vis:cb&&cb.visibility, btn_rect:btn&&btn.getBoundingClientRect().toJSON(),
              hint_op:ch&&ch.opacity, hint_rect:hint&&hint.getBoundingClientRect().toJSON()};}"""))
    clip={'x':box['x']+box['w']-190,'y':box['y']+box['h']-170,'width':206,'height':184}
    pg.screenshot(path='l1l2-fab-corner-b.png', clip=clip)
    print("OK", clip)
    b.close()
