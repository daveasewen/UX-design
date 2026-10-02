import json
from playwright.sync_api import sync_playwright
R={}
with sync_playwright() as p:
    b=p.chromium.launch()
    for i in (1,2,3):
        pg=b.new_page(viewport={'width':1440,'height':900}); errs=[]
        pg.on('pageerror', lambda e: errs.append((str(e)[:150], (e.stack or '')[:400])))
        pg.goto(f'http://127.0.0.1:870{i}/out/dashboard.html'); pg.wait_for_timeout(1200)
        leg=pg.locator('[class*="cn-chart-"] button',has_text='A ').filter(visible=True).first
        chart=leg.locator('xpath=ancestor::*[contains(@class,"cn-chart-")][1]')
        st=lambda: chart.evaluate("c=>[...c.querySelectorAll('button')].filter(b=>/Reset|^A |^B /.test(b.innerText.trim())).map(b=>b.innerText.trim().slice(0,8)+' pressed='+b.getAttribute('aria-pressed')+' disabled='+b.disabled+' ariaDis='+b.getAttribute('aria-disabled')+' vis='+(b.getBoundingClientRect().width>0)+' pe='+getComputedStyle(b).pointerEvents+' op='+getComputedStyle(b).opacity)")
        before=st(); leg.click(); pg.wait_for_timeout(400); after=st()
        rs=chart.locator('button',has_text='Reset').first
        try: rs.click(timeout=3000); res='clicked'
        except Exception as e: res='EXC '+str(e).split('Call log')[1][:500] if 'Call log' in str(e) else str(e)[:300]
        pg.wait_for_timeout(300); after2=st()
        R[f'G{i}']=dict(before=before, after_isolate=after, reset=res, after_reset=after2)
        if i==2:
            pg.locator('header nav a',has_text='Liquidity').first.click(); pg.wait_for_timeout(500)
            pg.locator('header nav a',has_text='Payments').first.click(); pg.wait_for_timeout(500)
            R['G2']['nav_errors']=errs[:]
            pg.locator('header nav a',has_text='Overview').first.click(); pg.wait_for_timeout(500)
            row=pg.locator('[data-action=open-payment]').filter(visible=True).first
            row.click(); pg.wait_for_timeout(700)
            R['G2']['F02']=pg.evaluate("()=>{const a=document.activeElement;const d=a&&a.closest('.cn-drawer,[role=dialog]');return {focusInDrawer:!!d, text:d?d.innerText.slice(0,160):null, dialogs:[...document.querySelectorAll('.cn-drawer')].map(e=>e.className+' hidden='+e.hidden+' aria='+e.getAttribute('aria-hidden')+' w='+e.getBoundingClientRect().width)}}")
            # approve in drawer
            if pg.locator('#act').filter(visible=True).count():
                k0=pg.evaluate("()=>[...document.querySelectorAll('.cn-metric')].map(e=>e.innerText.replace(/\\s+/g,' ')).join('|')")
                lab=pg.locator('#act').inner_text(); pg.locator('#act').click(); pg.wait_for_timeout(600)
                k1=pg.evaluate("()=>[...document.querySelectorAll('.cn-metric')].map(e=>e.innerText.replace(/\\s+/g,' ')).join('|')")
                R['G2']['approve']=dict(label=lab, kpi_changed=k0!=k1)
            # view persistence: nav to Payments then reload
            pg.locator('#close').click(timeout=3000) if pg.locator('#close').filter(visible=True).count() else None
            pg.locator('header nav a',has_text='Payments').first.click(); pg.wait_for_timeout(500)
            u=pg.url; v=pg.evaluate("()=>[...document.querySelectorAll('[aria-current]')].map(e=>e.innerText.trim()).join('|')")
            pg.reload(); pg.wait_for_timeout(1200); v2=pg.evaluate("()=>[...document.querySelectorAll('[aria-current]')].map(e=>e.innerText.trim()).join('|')")
            R['G2']['view_persist']=dict(url=u, before=v, after=v2, url_after=pg.url)
            R['G2']['all_errors']=errs
        if i==3:
            pg.locator('header nav a',has_text='Payments').first.click(); pg.wait_for_timeout(500)
            pag=pg.evaluate("()=>[...document.querySelectorAll('button')].filter(b=>b.innerText.trim()==='2'&&b.getBoundingClientRect().width>0).map(b=>b.parentElement.className+' > '+b.parentElement.parentElement.className)")
            g0=pg.evaluate("()=>[...document.querySelectorAll('.cn-data-grid tbody tr')].slice(0,2).map(r=>r.innerText.slice(0,40)).join('|')")
            pg.locator('button',has_text='2').filter(visible=True).first.click() if False else pg.locator('xpath=//button[normalize-space()="2"]').filter(visible=True).first.click()
            pg.wait_for_timeout(500)
            g1=pg.evaluate("()=>[...document.querySelectorAll('.cn-data-grid tbody tr')].slice(0,2).map(r=>r.innerText.slice(0,40)).join('|')")
            R['G3']['page2']=dict(parents=pag, changed=g0!=g1, url=pg.url, first=g1[:80])
            # select row + approve selected
            cbinfo=pg.evaluate("()=>{const i=document.querySelector('.cn-data-grid tbody input[type=checkbox]');const r=i.getBoundingClientRect();const l=i.closest('label');return {w:r.width,h:r.height,label:!!l,lw:l?l.getBoundingClientRect().width:0}}")
            R['G3']['checkbox']=cbinfo
            pg.locator('.cn-data-grid tbody tr').first.locator('label').first.click(); pg.wait_for_timeout(300)
            sel=pg.evaluate("()=>document.querySelector('.cn-data-grid tbody input[type=checkbox]:checked')?1:0")
            st0=pg.evaluate("()=>[...document.querySelectorAll('.cn-data-grid tbody tr')].find(r=>r.querySelector('input:checked'))?.innerText.replace(/\\s+/g,' ').slice(0,120)")
            dis=pg.evaluate("()=>document.querySelector('#btnApprove').disabled")
            # try a pending row
            pend=pg.locator('.cn-data-grid tbody tr',has_text='Pending approval').first
            pend.locator('label').first.click(); pg.wait_for_timeout(300)
            sel2=pg.evaluate("()=>[...document.querySelectorAll('.cn-data-grid tbody input[type=checkbox]:checked')].length")
            dis2=pg.evaluate("()=>document.querySelector('#btnApprove').disabled")
            res='not tried'
            if not dis2:
                pg.locator('#btnApprove').click(); pg.wait_for_timeout(700)
                res=pg.evaluate("()=>[...document.querySelectorAll('.cn-data-grid tbody tr')].slice(0,10).map(r=>r.innerText.replace(/\\s+/g,' ').slice(0,90))")
            R['G3']['approve']=dict(selected_after_first=sel, first_row=st0, approve_disabled=dis, checked_after_pending=sel2, approve_disabled_after_pending=dis2, result=res)
            R['G3']['errors']=errs
    b.close()
print(json.dumps(R,indent=1))
json.dump(R,open('probe2.json','w'),indent=1)
