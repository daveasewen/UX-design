from playwright.sync_api import sync_playwright
U="file:///sessions/serene-hopeful-pasteur/mnt/UX-design/reviews/SEGMENTED-RULING-2026-08-30-v1.html"
with sync_playwright() as p:
    b=p.chromium.launch()
    pg=b.new_page(viewport={'width':1300,'height':1000},device_scale_factor=2)
    pg.goto(U); pg.wait_for_timeout(900)
    pg.eval_on_selector('section.theme[data-apollo-theme="console"][data-theme="light"]','e=>e.scrollIntoView({block:"start"})')
    pg.wait_for_timeout(400)
    r=pg.evaluate("""()=>{const s=document.querySelector('section.theme[data-apollo-theme="console"][data-theme="light"]');
      const ps=[...s.querySelectorAll('.pair')].slice(0,2).map(e=>e.getBoundingClientRect());
      const x=Math.min(...ps.map(p=>p.left)), y=Math.min(...ps.map(p=>p.top));
      const r2=Math.max(...ps.map(p=>p.right)), b2=Math.max(...ps.map(p=>p.bottom));
      return {x:x-8,y:y-8,width:(r2-x)+16,height:(b2-y)+16};}""")
    print(r)
    pg.screenshot(path='l4-console-xs-s.png', clip=r)
    print("OK")
    b.close()
