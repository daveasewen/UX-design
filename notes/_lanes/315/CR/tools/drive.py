import json, sys, hashlib
from playwright.sync_api import sync_playwright
i=int(sys.argv[1]); G=f'G{i}'; BASE=f'http://127.0.0.1:870{i}/out/dashboard.html'
SIG='''()=>{
 const vis=e=>{if(!e)return false;const r=e.getBoundingClientRect();const s=getComputedStyle(e);return r.width>0&&r.height>0&&s.visibility!=='hidden'&&s.display!=='none'};
 const h=s=>{let x=0;for(let k=0;k<s.length;k++){x=(x*31+s.charCodeAt(k))|0}return x};
 const q=(s)=>[...document.querySelectorAll(s)];
 const charts=q('[class*="cn-chart-"] svg').filter(vis).map(e=>e.innerHTML).join('|');
 const drawer=q('.cn-drawer, [role=dialog]').some(e=>vis(e)&&e.getBoundingClientRect().right>0&&e.getBoundingClientRect().left<innerWidth&&!e.closest('[hidden]')&&e.getAttribute('aria-hidden')!=='true'&&(e.matches('[open],.is-open,[data-open=true]')||e.querySelector('[open]')||getComputedStyle(e).transform==='none'));
 return {url:location.search+location.hash,
  count:(q('.ftb-status').map(e=>e.innerText).join('|')+' '+q('.dg-count').map(e=>e.innerText).join('|')).trim(),
  kpi:q('.cn-metric').filter(vis).map(e=>e.innerText.replace(/\\s+/g,' ')).join('|').slice(0,400),
  chartH:h(charts), nCharts:q('[class*="cn-chart-"]').filter(vis).length,
  list:q('[data-action=open-payment]').filter(vis).slice(0,4).map(e=>e.innerText.replace(/\\s+/g,' ').slice(0,40)).join('|'),
  nList:q('[data-action=open-payment]').filter(vis).length,
  grid:q('.cn-data-grid tbody tr, .cn-table tbody tr').filter(vis).slice(0,3).map(e=>e.innerText.replace(/\\s+/g,' ').slice(0,50)).join('|'),
  view:q('h2,h3').filter(vis).map(e=>e.innerText.trim()).slice(0,8).join('|'),
  chips:q('.cn-filter-toolbar-bar .tag, .cn-filter-toolbar-bar [class*=chip]').filter(vis).map(e=>e.innerText.trim()).join('|'),
  theme:document.documentElement.getAttribute('data-theme')+'/'+document.documentElement.getAttribute('data-mode'),
  active:(document.activeElement&&(document.activeElement.id||document.activeElement.className||'').toString().slice(0,40)),
  dialogs:q('[role=dialog],.cn-drawer').filter(e=>vis(e)).map(e=>{const r=e.getBoundingClientRect();return Math.round(r.left)+':'+Math.round(r.width)+':'+(e.getAttribute('aria-hidden')||'')+':'+(e.hidden)}).join(','),
  pressed:q('[aria-pressed=true],[aria-selected=true],[aria-current]').filter(vis).map(e=>e.innerText.trim().slice(0,15)).join('|').slice(0,200),
  expanded:q('[aria-expanded=true]').filter(vis).map(e=>e.id||e.innerText.trim().slice(0,15)).join('|'),
  detailsOpen:q('details[open]').filter(vis).length,
  density:document.querySelector('[data-density]')?document.querySelector('[data-density]').getAttribute('data-density'):null,
 }}'''
steps=[]; errs=[]; cons=[]; downloads=[]
def diff(a,b): return [k for k in a if a[k]!=b[k] and k not in('active',)]
def step(pg,name,fn,expect=None,wait=500):
    e0=len(errs); before=pg.evaluate(SIG); ok=True; note=''
    try: r=fn(); note=str(r) if r else ''
    except Exception as ex: ok=False; note='EXC '+str(ex).split('\n')[0][:160]
    pg.wait_for_timeout(wait); after=pg.evaluate(SIG); ch=diff(before,after)
    hit=[k for k in (expect or []) if k in ch]
    verdict='works' if ok and ch and (not expect or hit) else ('dead' if ok else 'error')
    rec=dict(step=name,verdict=verdict,changed=ch,expected=expect,hit=hit,note=note,newErrors=errs[e0:],after={k:after[k] for k in ch})
    steps.append(rec); print(f'{verdict:6} {name} :: {ch} {note[:80]} {errs[e0:][:1]}')
    return after
def opt(pg, menu, text): pg.locator(f'#{menu} [role=option]', has_text=text).first.click()
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(viewport={'width':1440,'height':900}, accept_downloads=True); pg=ctx.new_page()
    pg.on('pageerror', lambda e: errs.append(str(e)[:200])); pg.on('console', lambda m: cons.append(m.text[:200]) if m.type=='error' else None)
    pg.on('download', lambda d: downloads.append(d.suggested_filename))
    pg.goto(BASE); pg.wait_for_timeout(1200)
    init=pg.evaluate(SIG)
    # F02 premise: are list rows rendered after load?
    src=pg.evaluate("async()=>{const t=await (await fetch(location.pathname)).text();const d=new DOMParser().parseFromString(t,'text/html');return {srcRows:d.querySelectorAll('[data-action=open-payment]').length, srcMetricVals:d.querySelectorAll('.cn-metric').length}}")
    live=pg.evaluate("()=>document.querySelectorAll('[data-action=open-payment]').length")
    navs=pg.evaluate("()=>[...document.querySelectorAll('header nav a, .cn-app-shell-top-nav nav a')].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&r.top<70}).map(e=>e.innerText.trim()).filter(Boolean)")
    print('navs',navs,'src rows',src,'live rows',live)
    for n in navs[1:]+navs[:1]:
        step(pg,f'nav: {n}', lambda n=n: pg.locator('header nav a, .cn-app-shell-top-nav nav a').filter(has_text=n).filter(visible=True).first.click(), ['view','url'])
    # toolbar on overview
    q=init['list'].split('|')[0].split(' ')[1] if init['list'] else 'EUR'
    step(pg,f'search click+type "{q}"', lambda: (pg.click('#ftbQ'), pg.keyboard.type(q)), ['count','list','kpi','chartH','grid'], wait=800)
    step(pg,'search clear (click, select-all, delete)', lambda: (pg.click('#ftbQ',click_count=3), pg.keyboard.press('Delete')), ['count','list','kpi','chartH','grid'], wait=800)
    opts=pg.evaluate("()=>[...document.querySelectorAll('#ftbAddM [role=option]')].map(e=>e.innerText.trim())")
    ccy=[o for o in opts if o in('EUR','GBP','HKD')][0]
    step(pg,'add filter: open menu', lambda: pg.click('#ftbAddT'), ['expanded'])
    step(pg,f'add filter: {ccy}', lambda: opt(pg,'ftbAddM',ccy), ['chips','count','kpi','chartH','list','grid'], wait=800)
    pg.mouse.click(1430,890); pg.wait_for_timeout(200)
    ropts=pg.evaluate("()=>[...document.querySelectorAll('#ftbRangeM [role=option]')].map(e=>e.innerText.trim())")
    cur=pg.locator('#ftbRangeT').inner_text().replace('▾','').strip(); r2=[o for o in ropts if o!=cur][-1]
    step(pg,'range: open', lambda: pg.click('#ftbRangeT'), ['expanded'])
    step(pg,f'range: {r2}', lambda: opt(pg,'ftbRangeM',r2), ['kpi','chartH','count','list','grid'], wait=800)
    # legend isolate + reset, view-as-table
    leg=pg.locator('.dv-leg').filter(visible=True).first
    if leg.count():
        step(pg,'legend isolate A', lambda: leg.locator('.dv-leg-item').first.click(), ['chartH','pressed'])
        step(pg,'legend reset', lambda: leg.locator('.dv-leg-reset').click(timeout=4000), ['chartH','pressed'])
    step(pg,'view as table', lambda: pg.locator('[class*="cn-chart-"] summary').first.click(), ['detailsOpen'])
    step(pg,'view as table close', lambda: pg.locator('[class*="cn-chart-"] summary').first.click(), ['detailsOpen'])
    # F02: a row rendered by script opens the drawer
    rec=step(pg,'F02 open a script-rendered payment row', lambda: pg.locator('[data-action=open-payment]').filter(visible=True).first.click(), ['dialogs'], wait=700)
    drawer_text=pg.evaluate("()=>{const a=document.activeElement;const d=a&&a.closest('.cn-drawer,[role=dialog]');return d?d.innerText.slice(0,200):null}")
    focus_in=pg.evaluate("()=>!!(document.activeElement&&document.activeElement.closest('.cn-drawer,[role=dialog]'))")
    print('drawer text:', (drawer_text or '')[:120].replace('\n',' '), 'focus inside', focus_in)
    step(pg,'drawer close (button)', lambda: pg.locator('#close').click(), ['dialogs'])
    # segmented buttons in toolbar
    segs=pg.evaluate("()=>[...document.querySelectorAll('.cn-filter-toolbar-bar button')].filter(e=>e.getBoundingClientRect().width>0&&!e.id&&!e.getAttribute('aria-haspopup')&&e.getAttribute('aria-pressed')==='false').map(e=>e.innerText.trim())")
    for s in segs:
        step(pg,f'toolbar segment: {s}', lambda s=s: pg.locator('.cn-filter-toolbar-bar button',has_text=s).first.click(), ['list','grid','pressed','density','url'])
    # export
    if pg.locator('#ftbExportT').count():
        step(pg,'export: open', lambda: pg.click('#ftbExportT'), ['expanded'])
        with pg.expect_download(timeout=5000) as dl:
            pg.locator('#ftbExportM [role=option]').first.click()
        downloads.append(dl.value.suggested_filename); print('download', dl.value.suggested_filename)
    elif pg.locator('button',has_text='Export CSV').count():
        with pg.expect_download(timeout=5000) as dl:
            pg.locator('button',has_text='Export CSV').first.click()
        downloads.append(dl.value.suggested_filename); print('download', dl.value.suggested_filename)
    # theme toggle (if any)
    if pg.locator('button',has_text='Dark mode').count():
        step(pg,'theme toggle: Dark mode', lambda: pg.locator('button',has_text='Dark mode').first.click(), ['theme'])
    # go to payments view, pagination, grid
    pn=[n for n in navs if 'ayment' in n][0]
    step(pg,f'nav: {pn} (for paging)', lambda: pg.locator('header nav a, .cn-app-shell-top-nav nav a').filter(has_text=pn).filter(visible=True).first.click(), ['view','url'])
    pager=pg.locator('xpath=//*[self::a or self::button][normalize-space()="2"]').filter(visible=True)
    if pager.count(): step(pg,'page 2', lambda: pager.first.click(), ['list','grid','url','pressed'])
    else: steps.append(dict(step='page 2',verdict='missing')); print('missing page 2')
    if pg.locator('.cn-data-grid th button').filter(visible=True).count():
        step(pg,'grid sort Amount', lambda: pg.locator('.cn-data-grid th button',has_text='Amount').first.click(), ['grid','url'])
        step(pg,'grid sort Amount again', lambda: pg.locator('.cn-data-grid th button',has_text='Amount').first.click(), ['grid','url'])
        step(pg,'grid rows per page 25', lambda: pg.select_option('#pp','25'), ['grid','count','url'])
        step(pg,'grid select a pending row (label click)', lambda: pg.locator('.cn-data-grid tbody tr',has_text='Pending approval').first.locator('label').first.click(), ['grid','pressed','count','kpi'])
    before_reload=pg.evaluate(SIG); url=pg.url
    pg.reload(); pg.wait_for_timeout(1500); after_reload=pg.evaluate(SIG)
    keys=['url','count','kpi','chartH','list','grid','view','chips','theme','pressed']
    persist={k:(before_reload[k]==after_reload[k]) for k in keys}
    print('persist', persist)
    # cold load of the URL in a fresh context
    c2=b.new_context(viewport={'width':1440,'height':900}); p2=c2.new_page(); p2.goto(url); p2.wait_for_timeout(1500); cold=p2.evaluate(SIG); c2.close()
    persist_cold={k:(before_reload[k]==cold[k]) for k in keys}
    print('persist cold', persist_cold)
    # 820 menu sheet
    c3=b.new_context(viewport={'width':820,'height':1180}); p3=c3.new_page(); e3=[]; p3.on('pageerror',lambda e:e3.append(str(e)[:200])); p3.goto(BASE); p3.wait_for_timeout(1200)
    burger=p3.locator('header button[aria-label*="menu" i], header button[aria-controls*=sheet i], header .nv-burger, header button').filter(visible=True).first
    blabel=burger.get_attribute('aria-label'); burger.click(); p3.wait_for_timeout(500)
    sheet_links=p3.evaluate("()=>[...document.querySelectorAll('a')].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&r.left>=0&&r.left<300&&r.top<400&&e.closest('[role=dialog],.nv-sheet,[class*=sheet],[class*=drawer],aside,nav')}).map(e=>e.innerText.trim()).filter(Boolean)")
    ok820=False
    if len(sheet_links)>1:
        lab=sheet_links[-1]; p3.locator('a',has_text=lab).filter(visible=True).last.click(); p3.wait_for_timeout(600)
        ok820=lab in p3.evaluate("()=>location.search+location.hash+document.title+[...document.querySelectorAll('[aria-current]')].map(e=>e.innerText).join('|')")
    print('820 burger', blabel, 'sheet', sheet_links, 'nav via sheet ok', ok820, 'errs', e3)
    c3.close(); b.close()
out=dict(arm=G, url=BASE, initial=init, F02_premise=dict(source=src, live_rows=live), steps=steps, drawer_text=drawer_text, drawer_focus_inside=focus_in,
  downloads=downloads, persistence=dict(reload=persist, cold_url=url, cold=persist_cold), m820=dict(burger=blabel, sheet_links=sheet_links, nav_ok=ok820, errors=e3),
  pageerrors=errs, console_errors=cons)
json.dump(out, open(f'/home/claude/cr/m/{G}/drive.json','w'), indent=1)
print('TOTAL steps',len(steps),'works',sum(s['verdict']=='works' for s in steps),'dead',[s['step'] for s in steps if s['verdict']!='works'],'pageerrors',len(errs),'console',len(cons))
