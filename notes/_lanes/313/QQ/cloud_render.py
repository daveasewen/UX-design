import sys, os, json, re
sys.path.insert(0,'knowledge/canon'); sys.path.insert(0,'knowledge')
import gen_theme_cascade as C
from playwright.sync_api import sync_playwright
OUT=sys.argv[1]
themes=C.load_themes()
def doc(name, slug):
    src=open(f'knowledge/snippets/{name}.reference.html').read()
    mm=re.search(r'<script[^>]*id="token-manifest"[^>]*>(.*?)</script>',src,re.S)
    varmap=json.loads(mm.group(1))['vars']
    css=C.snippet_theme_css(varmap, slug)
    return src.replace('</head>','<style id="apollo-theme-cascade">\n'+css+'\n</style>\n</head>',1)
res=[]
with sync_playwright() as p:
    b=p.chromium.launch()
    for name,slug in (('Date-picker','date-picker'),('Calendar','calendar')):
        html=doc(name,slug)
        path=os.path.join(OUT,f'{name}.html'); open(path,'w').write(html)
        for t in themes:
            for mode in ('light','dark'):
                pg=b.new_page(viewport={'width':900,'height':900})
                pg.goto('file://'+os.path.abspath(path)+'#')
                pg.evaluate(f"document.documentElement.setAttribute('data-apollo-theme','{t['attr']}');document.body.setAttribute('data-theme','{mode}')")
                info={}
                if name=='Date-picker':
                    pg.click('#dp-open'); pg.wait_for_timeout(250)
                    info=pg.evaluate("""()=>{const p=document.getElementById('dp-panel').getBoundingClientRect();
                      const g=document.getElementById('dp-grid').getBoundingClientRect();
                      const d=[...document.querySelectorAll('#dp-body .cal-day')];
                      const btn=d.filter(x=>x.tagName==='BUTTON'); const r=btn[0].getBoundingClientRect();
                      const nav=document.getElementById('dp-prev-y').getBoundingClientRect();
                      return {panel:[p.width,p.height], grid:[g.width,g.height], gridOverflow: g.right>p.right-16.5, cells:d.length, days:btn.length, empty:d.filter(x=>x.classList.contains('is-empty')).length,
                        cell:[Math.round(r.width*10)/10,r.height], nav:[nav.width,nav.height], focusIsDay: document.activeElement.classList.contains('cal-day'),
                        hscroll: document.documentElement.scrollWidth>innerWidth,
                        todaySel: (()=>{const t=document.querySelector('#dp-body .is-today'); return t?getComputedStyle(t).boxShadow:null})()}}""")
                    pg.screenshot(path=os.path.join(OUT,f'{name}-{t["attr"]}-{mode}.png'), full_page=True)
                    # select today to show today+chosen in the live panel
                    pg.keyboard.press('Enter'); pg.wait_for_timeout(150)
                    info['afterEnter']=pg.evaluate("[document.getElementById('f-date').value, document.activeElement.id, document.getElementById('dp-panel').classList.contains('is-open')]")
                    pg.click('#dp-open'); pg.wait_for_timeout(200)
                    info['todaySelectedShadow']=pg.evaluate("getComputedStyle(document.querySelector('#dp-body .is-today')).boxShadow")
                    pg.keyboard.press('ArrowRight'); pg.keyboard.press('PageDown'); pg.wait_for_timeout(100)
                    info['kbd']=pg.evaluate("[document.activeElement.className, document.getElementById('dp-title').textContent]")
                    pg.keyboard.press('Escape'); pg.wait_for_timeout(100)
                    info['esc']=pg.evaluate("[document.activeElement.id, document.getElementById('dp-panel').classList.contains('is-open')]")
                    pg.click('#dp-open'); pg.wait_for_timeout(200)
                    pg.locator('#dp-panel').screenshot(path=os.path.join(OUT,f'{name}-{t["attr"]}-{mode}-panel-today-chosen.png'))
                else:
                    pg.screenshot(path=os.path.join(OUT,f'{name}-{t["attr"]}-{mode}.png'), full_page=True)
                res.append((name,t['attr'],mode,info)); pg.close()
    # narrow
    pg=b.new_page(viewport={'width':390,'height':900}); pg.goto('file://'+os.path.abspath(os.path.join(OUT,'Date-picker.html')))
    pg.click('#dp-open'); pg.wait_for_timeout(200)
    res.append(('Date-picker','390','light',pg.evaluate("({hscroll: document.documentElement.scrollWidth>innerWidth, panel: document.getElementById('dp-panel').getBoundingClientRect().width, grid: document.getElementById('dp-grid').getBoundingClientRect().width})")))
    pg.screenshot(path=os.path.join(OUT,'Date-picker-390.png'), full_page=True)
    b.close()
for r in res: print(r)
