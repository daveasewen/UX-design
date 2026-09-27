"""W4b: axis-label spacing per svg row — why G7 misses the 30-date collisions."""
import sys, os
sys.path.insert(0, 'knowledge')
import _validate_geometry as G
JS = r"""() => { const out=[];
 for (const s of document.querySelectorAll('svg')) {
   const rows=new Map();
   for (const t of s.querySelectorAll('text')) { const r=t.getBoundingClientRect(); if(!r.width) continue; const k=Math.round(r.top); if(!rows.has(k)) rows.set(k,[]); rows.get(k).push([r.left,r.right,t.textContent]); }
   for (const [k,v] of rows) { if (v.length<6) continue; v.sort((a,b)=>a[0]-b[0]); let mn=1e9, ex='';
     for (let i=0;i<v.length-1;i++){ const g=v[i+1][0]-v[i][1]; if(g<mn){mn=g; ex=v[i][2]+'|'+v[i+1][2];} }
     out.push({svg:(s.getAttribute('class')||'').slice(0,30), n:v.length, mingap:Math.round(mn*10)/10, ex}); }
 }
 return out; }"""
with G.Harness() as h:
    for page in sys.argv[1:]:
        pg = h.b.new_page(viewport={'width':1440,'height':900}); pg.goto('file://'+os.path.abspath(page)); pg.wait_for_timeout(1500)
        print('==', page[-40:]); [print(x) for x in pg.evaluate(JS)]; pg.close()
