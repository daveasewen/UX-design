import json
from playwright.sync_api import sync_playwright
PAGE='/sessions/bold-focused-hopper/mnt/UX-design/knowledge/snippets/Template-dashboard-bento.reference.html'
ST=r"""()=>{const na=document.getElementById('dp08-na');const b=na.getBoundingClientRect();return{
 y:Math.round(scrollY),active:document.activeElement?(document.activeElement.id||document.activeElement.className||document.activeElement.tagName):null,
 hash:location.hash,tabindex:na.getAttribute('tabindex'),arrived:na.classList.contains('is-dp08-arrived'),
 naTop:Math.round(b.top),mainVisible:!!document.querySelector('#tplMain'),panels:document.querySelectorAll('[role="tabpanel"]').length};}"""
with sync_playwright() as p:
    b=p.chromium.launch(args=['--no-sandbox'])
    for mode in ('normal','reduce'):
        ctx=b.new_context(viewport={'width':1440,'height':900},reduced_motion=('reduce' if mode=='reduce' else 'no-preference'))
        pg=ctx.new_page(); seen=[]; pg.on("pageerror",lambda e:seen.append(str(e)))
        pg.goto(f"file://{PAGE}"); pg.wait_for_timeout(400)
        print('==',mode,'BEFORE',pg.evaluate(ST))
        pg.evaluate("()=>document.querySelector('[data-dp08-anchor]').click()")
        for t in (150,600,1400,2400):
            pg.wait_for_timeout(t- (0 if t==150 else 0))
            print('   t~',t,pg.evaluate(ST))
            pg.wait_for_timeout(0)
        print('   errors',seen)
        ctx.close()
    # KEYBOARD path: focus the chip via keyboard and press Enter
    ctx=b.new_context(viewport={'width':1440,'height':900}); pg=ctx.new_page()
    seen=[]; pg.on("pageerror",lambda e:seen.append(str(e)))
    pg.goto(f"file://{PAGE}"); pg.wait_for_timeout(400)
    n=0
    while n<40:
        pg.keyboard.press('Tab'); n+=1
        cur=pg.evaluate("()=>document.activeElement&&document.activeElement.hasAttribute&&document.activeElement.hasAttribute('data-dp08-anchor')")
        if cur: break
    print('== KEYBOARD tabs to reach chip:',n,'reached',cur)
    if cur:
        ring=pg.evaluate("()=>{const e=document.activeElement;const s=getComputedStyle(e);return{outline:s.outlineWidth+' '+s.outlineStyle+' '+s.outlineColor,boxShadow:s.boxShadow};}")
        print('   focus ring on chip',ring)
        pg.keyboard.press('Enter'); pg.wait_for_timeout(400)
        print('   AFTER Enter',pg.evaluate(ST))
    print('   errors',seen)
    # NO-JS control: does the plain anchor still work with JS disabled?
    ctx2=b.new_context(viewport={'width':1440,'height':900},java_script_enabled=False)
    pg2=ctx2.new_page(); pg2.goto(f"file://{PAGE}"); pg2.wait_for_timeout(300)
    pg2.click('[data-dp08-anchor]'); pg2.wait_for_timeout(400)
    print('== NOJS scrollY after click:', pg2.evaluate("()=>0") if False else pg2.evaluate("window.scrollY") if False else 'n/a')
    b.close()
