import asyncio, json
from playwright.async_api import async_playwright
R='/sessions/adoring-relaxed-allen/mnt/UX-design/'
OUT='/sessions/adoring-relaxed-allen/mnt/outputs/'
PAGES=[('strand','notes/_STRAND-MAP-2026-09-19.html','#s2'),('review','notes/_lanes/288/T/template-quality-review.html','#pack')]
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        for name,path,anchor in PAGES:
            pg=await b.new_page(viewport={'width':1280,'height':900})
            errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
            await pg.goto('file://'+R+path); await pg.wait_for_timeout(300)
            n=await pg.evaluate("document.querySelectorAll('.dd-box').length")
            labels=await pg.evaluate("[...document.querySelectorAll('.dd-box')].map(b=>b.dataset.id+' | '+b.querySelector('.dd-label').textContent+' | '+b.parentElement.className)")
            # interact: click chip, type, check localStorage + markdown
            box=pg.locator('.dd-box').nth(1)
            await box.locator('.dd-chip', has_text='Inscribe').click()
            await box.locator('textarea[data-f=decision]').fill('yes, do it — but keep the 4 + 2 wall')
            await box.locator('textarea[data-f=comment]').fill('a comment\nsecond line')
            cnt=await pg.evaluate("document.getElementById('dd-count').textContent")
            ls=await pg.evaluate("localStorage.getItem('dave-decisions:'+(location.pathname.includes('STRAND')?'strand-map':'template-quality-review'))")
            await pg.reload(); await pg.wait_for_timeout(300)
            persisted=await pg.evaluate("[...document.querySelectorAll('.dd-box')][1].querySelector('textarea[data-f=decision]').value")
            async with pg.expect_download() as dl:
                await pg.click('#dd-dl')
            d=await dl.value; md=open(await d.path()).read()
            await pg.locator(anchor).scroll_into_view_if_needed(); await pg.wait_for_timeout(200)
            await pg.screenshot(path=OUT+f'verify-{name}.png')
            await pg.evaluate("document.querySelector('.dd-box').scrollIntoView()"); await pg.wait_for_timeout(200)
            await pg.screenshot(path=OUT+f'verify-{name}-box.png')
            print('==',name,'boxes',n,'errors',errs,'count',cnt,'persisted',repr(persisted),'download',d.suggested_filename)
            print('\n'.join(labels)); print('--- md head ---'); print(md[:700])
        await b.close()
asyncio.run(main())
