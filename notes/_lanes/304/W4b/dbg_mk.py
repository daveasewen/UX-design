"""W4b: marker and letter counts per chart (to set G11's arms against real pages)."""
import sys, os
sys.path.insert(0, 'knowledge')
import _validate_geometry as G
JS = r"""() => { const out=[];
 for (const s of document.querySelectorAll('svg')) { const sb=s.getBoundingClientRect(); if(sb.width<160) continue;
   const mk={}, let_={}; let lines=0, maxv=0;
   for (const d of s.querySelectorAll('circle,ellipse,rect,polygon')) { const c=getComputedStyle(d); if(d.classList.contains('dv-hit')) continue;
     const fn=c.fill==='none'||/rgba\(.*,\s*0\)/.test(c.fill); const sn=c.stroke==='none'||/rgba\(.*,\s*0\)/.test(c.stroke); if(fn&&sn) continue;
     const r=d.getBoundingClientRect(); if(r.width<3||r.width>16||r.height<3||r.height>16) continue; if(d.tagName==='rect'&&!d.classList.contains('dv-mk')) continue;
     const g=(d.closest('[data-series-group]')||{getAttribute:()=>null}).getAttribute('data-series-group')||c.fill; mk[g]=(mk[g]||0)+1; }
   for (const t of s.querySelectorAll('text')) { const x=t.textContent.trim(); if(/^[A-Z]$/.test(x)) let_[x]=(let_[x]||0)+1; }
   for (const p of s.querySelectorAll('polyline,path')) { const n=p.tagName==='polyline'?(p.getAttribute('points')||'').trim().split(/\s+/).length:((p.getAttribute('d')||'').match(/[LlMmCcHhVv]/g)||[]).length; if(n>maxv) maxv=n; }
   out.push({cls:(s.getAttribute('class')||'').slice(0,20), chart:(s.closest('[class*=cn-chart]')||{className:''}).className.toString().slice(0,30), w:sb.width|0,h:sb.height|0, mk, let_, maxv}); }
 return out; }"""
with G.Harness() as h:
    for page in sys.argv[1:]:
        pg = h.b.new_page(viewport={'width':1440,'height':900}); pg.emulate_media(reduced_motion='reduce'); pg.goto('file://'+os.path.abspath(page)); pg.wait_for_timeout(1500)
        print('==', page[-40:]); [print(x) for x in pg.evaluate(JS)]; pg.close()
