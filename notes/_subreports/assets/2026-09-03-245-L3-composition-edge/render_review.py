"""Render-verify the L3 review page: 4 themes x light/dark x 1440/390 -> scrollWidth == clientWidth, console errors, PNGs (4)."""
import asyncio, json, os
from playwright.async_api import async_playwright
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.abspath(os.path.join(HERE,'..','..','..'))
PAGE=os.path.join(ROOT,'_REVIEW-L3-composition-edge-2026-09-03-v1.html')
async def main():
    res=[]; errs=[]
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path=os.environ.get('RENDER_SHELL') or None)
        for w in (1440,390):
            pg=await b.new_page(viewport={'width':w,'height':1000})
            pg.on('console', lambda m: errs.append(m.text) if m.type=='error' else None)
            pg.on('pageerror', lambda x: errs.append(str(x)))
            await pg.goto('file://'+PAGE); await pg.wait_for_timeout(200)
            for t in ('mono','legacy','console','supercharge'):
                for m in ('light','dark'):
                    await pg.evaluate("([t,m])=>{document.documentElement.setAttribute('data-apollo-theme',t);document.documentElement.setAttribute('data-theme',m);}",[t,m])
                    await pg.wait_for_timeout(60)
                    r=await pg.evaluate("()=>({sw:document.documentElement.scrollWidth,cw:document.documentElement.clientWidth,bg:getComputedStyle(document.body).backgroundColor,ink:getComputedStyle(document.body).color,accent:getComputedStyle(document.querySelector('.label')).color})")
                    r.update(theme=t,mode=m,w=w); res.append(r)
                    if (t,m) in (('mono','light'),('mono','dark'),('supercharge','light'),('console','dark')) and w==1440:
                        await pg.screenshot(path=os.path.join(HERE,'review-%s-%s-%d.png'%(t,m,w)),full_page=False)
                    if (t,m)==('mono','light') and w==390:
                        await pg.screenshot(path=os.path.join(HERE,'review-mono-light-390.png'),full_page=False)
            await pg.close()
        await b.close()
    bad=[r for r in res if r['sw']!=r['cw']]
    out={'page':os.path.relpath(PAGE,ROOT),'states':len(res),'overflow':bad,'console_errors':errs,'states_detail':res}
    open(os.path.join(HERE,'render-review.json'),'w').write(json.dumps(out,indent=1)+'\n')
    print('states %d · overflow %d · console_errors %s'%(len(res),len(bad),errs))
    for r in res:
        if r['w']==1440: print(' %-12s %-5s bg=%s ink=%s accent=%s'%(r['theme'],r['mode'],r['bg'],r['ink'],r['accent']))
asyncio.run(main())
