import os,sys
from playwright.sync_api import sync_playwright
H=os.environ['HOME']
JS="()=>[...document.querySelectorAll('svg.dv-svg')].map(s=>{const r=s.getBoundingClientRect();const t=s.querySelector('text.dv-label,text.dv-axis');const tr=t?t.getBoundingClientRect():{height:0};return [s.getAttribute('viewBox'),Math.round(r.width),Math.round(tr.height*10)/10]})"
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=os.environ.get("RENDER_SHELL"))
    for S in sys.argv[1:]:
        for i in range(4):
            for rm in ('reduce','no-preference'):
                pg=b.new_page(viewport={"width":1440,"height":900},reduced_motion=rm); pg.goto("file://%s/v5st/%s/out/payments.html"%(H,S)); pg.wait_for_timeout(1300)
                r=pg.evaluate(JS); pg.close()
                print(S,'run',i,rm,'svgs',len(r),'label-h',[x[2] for x in r],'vb-w',[x[0].split()[2] if x[0] else None for x in r],'w',[x[1] for x in r])
    b.close()
