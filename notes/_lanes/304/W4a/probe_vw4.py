import os, sys, json
from playwright.sync_api import sync_playwright
VAR = sys.argv[4] if len(sys.argv)>4 else "after"
RUN = sys.argv[1]; PAGE = sys.argv[2]; N = int(sys.argv[3]) if len(sys.argv)>3 else 8
INIT = r"""
(()=>{ let real; Object.defineProperty(window,'dvRender',{configurable:true,get(){return real;},set(fn){
  if(typeof fn!=='function'){real=fn;return;}
  const w=function(fig,spec){ const s=fig.querySelector('svg.dv-fit')||fig.querySelector('svg.dv-svg');
    if(/donut|pie/.test(spec.type)){ const cs=getComputedStyle(s);
     (window.__log=window.__log||[]).push({t:Math.round(performance.now()),type:spec.type,rw:s.getBoundingClientRect().width,cw:cs.width,fiton:fig.classList.contains('dv-fit-on'),rs:document.readyState,
       sheets:[...document.styleSheets].map(x=>{try{return x.cssRules.length}catch(e){return 'x'}}), fonts:document.fonts.status, anims:document.getAnimations().filter(a=>a.effect&&a.effect.target===s).map(a=>[a.constructor.name,a.transitionProperty||a.animationName,a.playState,a.currentTime, JSON.stringify(a.effect.getKeyframes()).slice(0,300)]), tr:getComputedStyle(s).transition});}
    return fn.apply(this,arguments);};
  Object.keys(fn).forEach(k=>w[k]=fn[k]); real=w; }}); })();
"""
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ["RENDER_SHELL"])
    for i in range(N):
        c = b.new_context(viewport={'width':1440,'height':900}); pg = c.new_page(); pg.add_init_script(INIT)
        pg.emulate_media(reduced_motion='reduce')
        pg.goto('file://'+os.path.expanduser('~/w4a/st/%s/cold-%s/out/index.html' % (VAR, RUN))); pg.wait_for_timeout(900)
        pg.locator('a[href="%s"]' % PAGE).first.click(); pg.wait_for_load_state('load'); pg.wait_for_timeout(1500)
        ring = pg.evaluate('''()=>[...document.querySelectorAll('figure.dv')].filter(f=>/donut|pie/.test(f.getAttribute('data-dv-type'))).map(f=>{const s=f.querySelector('svg.dv-svg');return [s.getAttribute('viewBox'), s.getBoundingClientRect().width|0, s.getBoundingClientRect().height|0]})''')
        print('ring', ring)
        print(i, json.dumps(pg.evaluate("window.__log||[]")))
        c.close()
    b.close()
