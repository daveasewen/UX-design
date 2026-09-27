import os, sys, json
from playwright.sync_api import sync_playwright
RUN = sys.argv[1]; PAGE = sys.argv[2]; N = int(sys.argv[3]) if len(sys.argv)>3 else 8
INIT = r"""
(()=>{ let real; Object.defineProperty(window,'dvRender',{configurable:true,get(){return real;},set(fn){
  if(typeof fn!=='function'){real=fn;return;}
  const w=function(fig,spec){ const s=fig.querySelector('svg.dv-fit')||fig.querySelector('svg.dv-svg');
    if(/donut|pie/.test(spec.type)){ const cs=getComputedStyle(s);
     (window.__log=window.__log||[]).push({t:Math.round(performance.now()),type:spec.type,rw:s.getBoundingClientRect().width,cw:cs.width,fiton:fig.classList.contains('dv-fit-on'),rs:document.readyState,
       sheets:[...document.styleSheets].map(x=>{try{return x.cssRules.length}catch(e){return 'x'}}), fonts:document.fonts.status});}
    return fn.apply(this,arguments);};
  Object.keys(fn).forEach(k=>w[k]=fn[k]); real=w; }}); })();
"""
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ["RENDER_SHELL"])
    for i in range(N):
        c = b.new_context(viewport={'width':1440,'height':900}); pg = c.new_page(); pg.add_init_script(INIT)
        pg.goto('file://'+os.path.expanduser('~/r4c/stage/cold-%s/out/%s' % (RUN, PAGE))); pg.wait_for_timeout(1500)
        print(i, json.dumps(pg.evaluate("window.__log||[]")))
        c.close()
    b.close()
