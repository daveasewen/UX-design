import sys, json, os
from playwright.sync_api import sync_playwright
JS = r"""
() => {
  const out=[];
  const tiles=[...document.querySelectorAll('.c-bento__tile, figure, article, section')];
  for (const t of tiles){
    const r=t.getBoundingClientRect(); if (r.height<400||r.width<200) continue;
    const isGroup=!!t.querySelector('.c-bento__grid');
    // ink: text rects + svg marks + img/canvas
    const bands=[];
    const tw=document.createTreeWalker(t,NodeFilter.SHOW_TEXT); let n;
    while((n=tw.nextNode())){ if(!n.nodeValue.trim()) continue; const rg=document.createRange(); rg.selectNodeContents(n); for(const q of rg.getClientRects()){ if(q.height>0) bands.push([q.top,q.bottom]); } }
    for (const d of t.querySelectorAll('svg path,svg circle,svg rect,svg line,svg polyline,svg text,img,canvas,button,input,select')){
      const c=getComputedStyle(d); if(c.display==='none'||c.visibility==='hidden') continue;
      if (d.namespaceURI==='http://www.w3.org/2000/svg'){ const fn=(c.fill==='none'||c.fill==='rgba(0, 0, 0, 0)'), sn=(c.stroke==='none'||c.stroke==='rgba(0, 0, 0, 0)'); if(fn&&sn&&d.tagName!=='text') continue; }
      const q=d.getBoundingClientRect(); if(q.height>0&&q.width>0) bands.push([q.top,q.bottom]);
    }
    bands.sort((a,b)=>a[0]-b[0]); const m=[]; for(const b of bands){const l=m[m.length-1]; if(l&&b[0]<=l[1]+0.5) l[1]=Math.max(l[1],b[1]); else m.push([b[0],b[1]]);}
    let gap=0, where='';
    if (m.length){ gap=m[0][0]-r.top; where='top';
      for(let i=0;i<m.length-1;i++){ const g=m[i+1][0]-m[i][1]; if(g>gap){gap=g; where='between '+Math.round(m[i][1]-r.top)+'..'+Math.round(m[i+1][0]-r.top);} }
      const g2=r.bottom-m[m.length-1][1]; if(g2>gap){gap=g2; where='bottom';} }
    const h=(t.querySelector('h1,h2,h3,h4,figcaption')||{}).textContent||''; 
    out.push({tag:t.tagName, cls:t.className.toString().slice(0,60), h:Math.round(r.height), w:Math.round(r.width), group:isGroup, gap:Math.round(gap), where, head:h.trim().slice(0,50)});
  }
  return out;
}
"""
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=os.environ['RENDER_SHELL'])
    for run in sys.argv[1:]:
        pg=b.new_page(viewport={'width':1440,'height':1000})
        pg.goto('file://'+os.path.abspath(f'{os.environ["HOME"]}/r4c/stage/cold-{run}/out/index.html')); pg.wait_for_timeout(1500)
        pg.add_style_tag(content='.sh{height:auto!important}')
        pg.wait_for_timeout(300)
        res=pg.evaluate(JS)
        print('==',run)
        for x in res:
            if x['gap']>=48 or x['h']>700: print(x)
        pg.close()
    b.close()
