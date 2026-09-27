import os,sys
from playwright.sync_api import sync_playwright
H=os.environ['HOME']
JS="()=>[...document.querySelectorAll('svg.dv-svg')].map(s=>(s.getAttribute('viewBox')||'').split(' ')[2])"
N=int(sys.argv[1]); pages=sys.argv[2:]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=os.environ.get("RENDER_SHELL"))
    for pgn in pages:
      for S in ('before','after'):
        bad=0
        for i in range(N):
            pg=b.new_page(viewport={"width":1440,"height":900},reduced_motion='reduce'); pg.goto("file://%s/v5st/%s/out/%s"%(H,S,pgn)); pg.wait_for_timeout(1300)
            r=pg.evaluate(JS); pg.close()
            if any(x in ('580','618') for x in r): bad+=1
        print(pgn,S,'unfit loads',bad,'of',N)
    b.close()
