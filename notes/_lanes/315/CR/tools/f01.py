import json
from playwright.sync_api import sync_playwright
JS='''()=>{const bg=e=>{while(e){const c=getComputedStyle(e).backgroundColor;if(c!=='rgba(0, 0, 0, 0)')return c;e=e.parentElement}return 'none'};
 const m=document.querySelector('.cn-metric'); const v=m&&m.querySelector('[class*=value],[class*=fig],strong,b')||m;
 const scopesWithTheme=[...document.querySelectorAll('[data-theme]')].map(e=>e.tagName.toLowerCase()+(e.className?'.'+String(e.className).split(' ')[0]:''));
 return {htmlTheme:document.documentElement.getAttribute('data-theme'), htmlApollo:document.documentElement.getAttribute('data-apollo-theme'), bodyTheme:document.body.getAttribute('data-theme'),
  dataThemeOn:scopesWithTheme, bodyHasCn:[...document.body.classList].filter(c=>c.startsWith('cn-')),
  pageBg:bg(document.body), metricBg:bg(m), metricInk:getComputedStyle(v).color}}'''
R={}
with sync_playwright() as p:
    b=p.chromium.launch()
    for i in (1,2,3):
        r={}
        for mode in ('light','dark'):
            c=b.new_context(viewport={'width':1440,'height':900},color_scheme=mode); pg=c.new_page(); pg.goto(f'http://127.0.0.1:870{i}/out/dashboard.html'); pg.wait_for_timeout(1000)
            r[mode]=pg.evaluate(JS)
            if i==1 and mode=='light':
                pg.locator('button',has_text='Dark mode').first.click(); pg.wait_for_timeout(400); r['light→click Dark mode']=pg.evaluate(JS)
            c.close()
        r['F01_reproduces']= not (r['light']['metricBg']!=r['dark']['metricBg'] and r['light']['pageBg']!=r['dark']['pageBg'])
        R[f'G{i}']=r
    b.close()
json.dump(R,open('f01.json','w'),indent=1); print(json.dumps(R,indent=1))
