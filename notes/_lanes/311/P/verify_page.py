import os, sys, json
from playwright.sync_api import sync_playwright
ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','..','..'))
page_path='file://'+os.path.join(ROOT,'notes/_PLAN-311-thursday-burn-2026-10-01-v1.html')
out={}
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=os.environ.get('RENDER_SHELL') or None)
    for w in (1440,390):
        pg=b.new_page(viewport={'width':w,'height':900})
        pg.goto(page_path); pg.wait_for_timeout(300)
        sw=pg.evaluate('document.documentElement.scrollWidth'); cw=pg.evaluate('document.documentElement.clientWidth')
        # answer every call
        pg.evaluate('''()=>{document.querySelectorAll('.call').forEach((el,i)=>{const c=el.querySelector('.chip'); if(c) c.click(); const t=el.querySelector('textarea'); if(t){t.value='note '+i; t.dispatchEvent(new Event('input',{bubbles:true}));}})}''')
        txt=pg.evaluate('window.__reviewText()')
        n=pg.evaluate("document.getElementById('count').textContent")
        calls=pg.evaluate("document.querySelectorAll('.call').length")
        qs=pg.evaluate("[...document.querySelectorAll('.call')].map(e=>e.dataset.q)")
        missing=[q for q in qs if q not in txt and q!='Note on the page']
        pg.screenshot(path=os.path.join(os.path.dirname(__file__),f'shot-{w}.png'), full_page=(w==390))
        out[w]={'scrollWidth':sw,'clientWidth':cw,'side_scroll':sw>cw,'count':n,'calls':calls,'missing_in_text':missing,'text_lines':txt.count('\n')}
        pg.evaluate("localStorage.clear()")
    b.close()
print(json.dumps(out,indent=1))
