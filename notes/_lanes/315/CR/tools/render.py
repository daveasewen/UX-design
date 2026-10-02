import json, sys, os
from playwright.sync_api import sync_playwright
out = '/home/claude/cr/m'
res = {}
with sync_playwright() as p:
    b = p.chromium.launch()
    for i in (1,2,3):
        g=f'G{i}'; url=f'http://127.0.0.1:870{i}/out/dashboard.html'; res[g]={}
        os.makedirs(f'{out}/{g}', exist_ok=True)
        for w,h in ((1440,900),(820,1180)):
            for mode in ('light','dark'):
                ctx = b.new_context(viewport={'width':w,'height':h}, color_scheme=mode)
                pg = ctx.new_page(); errs=[]; cons=[]
                pg.on('pageerror', lambda e: errs.append(str(e)[:300]))
                pg.on('console', lambda m: cons.append(m.text[:300]) if m.type=='error' else None)
                pg.goto(url, wait_until='load'); pg.wait_for_timeout(1500)
                geo = pg.evaluate('''()=>{const de=document.documentElement,bd=document.body;
                  const cs=getComputedStyle(bd);
                  const firstCn=[...document.querySelectorAll('[class*="cn-"]')].slice(1).find(e=>getComputedStyle(e).backgroundColor!=='rgba(0, 0, 0, 0)');
                  return {scrollW:de.scrollWidth, innerW:innerWidth, docH:de.scrollHeight,
                   htmlTheme:de.getAttribute('data-theme'), bodyTheme:bd.getAttribute('data-theme'),
                   htmlAttrs:[...de.attributes].map(a=>a.name+'='+a.value).join(' ').slice(0,300),
                   bodyClass:bd.className.slice(0,200), bodyBg:cs.backgroundColor, bodyColor:cs.color,
                   cnSample: firstCn? (firstCn.className.slice(0,80)+' bg '+getComputedStyle(firstCn).backgroundColor):null,
                   svgCount:document.querySelectorAll('svg').length,
                   cnScopes:[...new Set([...document.querySelectorAll('[class]')].flatMap(e=>[...e.classList]).filter(c=>/^cn-/.test(c)))].length}}''')
                pg.screenshot(path=f'{out}/{g}/{w}-{mode}.png', full_page=True)
                pg.screenshot(path=f'{out}/{g}/{w}-{mode}-fold.png', full_page=False)
                res[g][f'{w}-{mode}'] = dict(geo, pageerrors=errs, consoleErrors=cons)
                ctx.close()
    b.close()
json.dump(res, open(f'{out}/render.json','w'), indent=1)
for g in res:
    for k,v in res[g].items(): print(g,k,{x:v[x] for x in ('scrollW','innerW','docH','htmlTheme','bodyTheme','bodyBg','cnSample','cnScopes')}, 'errs',len(v['pageerrors']),'cons',len(v['consoleErrors']))
