from playwright.sync_api import sync_playwright
PAGE='/sessions/bold-focused-hopper/mnt/UX-design/knowledge/snippets/Template-dashboard-bento.reference.html'
with sync_playwright() as p:
    b=p.chromium.launch(args=['--no-sandbox']); pg=b.new_page(viewport={'width':1440,'height':900})
    seen=[]; pg.on("pageerror",lambda e:seen.append(str(e)))
    pg.goto(f"file://{PAGE}"); pg.wait_for_timeout(400)
    pg.evaluate("()=>document.querySelector('[data-dp08-anchor]').click()"); pg.wait_for_timeout(600)
    print('ADV-A after click:',pg.evaluate("()=>({y:Math.round(scrollY),active:document.activeElement.id||document.activeElement.tagName,hash:location.hash,naById:!!document.getElementById('dp08-na'),arrivedAnywhere:document.querySelectorAll('.is-dp08-arrived').length})"))
    print('pageerrors',seen); b.close()
