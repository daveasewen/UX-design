from playwright.sync_api import sync_playwright
U="file:///sessions/serene-hopeful-pasteur/mnt/UX-design/reviews/CONFIRM-PASS-2026-08-31-v1.html"
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1000,'height':900})
    errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)[:200]))
    pg.goto(U); pg.wait_for_timeout(900)
    print("pageerrors:",errs)
    print("broken imgs:", pg.evaluate("()=>[...document.images].filter(i=>!i.complete||i.naturalWidth===0).map(i=>i.src)"))
    print("imgs:", pg.evaluate("()=>document.images.length"), "alt missing:", pg.evaluate("()=>[...document.images].filter(i=>!i.alt).length"))
    print("rows:", pg.eval_on_selector_all('section.row','e=>e.length'), "controlled:", pg.eval_on_selector_all('section.row[data-verbs]','e=>e.length'))
    b.close()
