import os, sys, json
from playwright.sync_api import sync_playwright
JS = r"""
() => {
 const T = s => !s || s==='transparent' || /rgba\(\s*0,\s*0,\s*0,\s*0\s*\)/.test(s);
 const out=[];
 const all=[...document.querySelectorAll('body *')];
 for (const el of all){
  const cs=getComputedStyle(el);
  if(!(cs.display.includes('grid')||cs.display.includes('flex'))) continue;
  const kids=[...el.children].filter(k=>{const c=getComputedStyle(k); if(c.display==='none'||c.position==='absolute'||c.position==='fixed')return false; const r=k.getBoundingClientRect(); return r.width>0&&r.height>0;});
  if(kids.length<2) continue;
  const r=el.getBoundingClientRect();
  if(r.width<300) continue;
  let d=0,p=el; while(p.parentElement){d++;p=p.parentElement;}
  out.push({depth:d, tag:el.tagName, cls:(el.className&&el.className.baseVal!==undefined?el.className.baseVal:el.className).slice(0,60), disp:cs.display, dir:cs.flexDirection, cg:cs.columnGap, rg:cs.rowGap,
   rect:[r.left,r.top,r.width,r.height].map(Math.round),
   kids:kids.map(k=>{const q=k.getBoundingClientRect(); const c=getComputedStyle(k); return {cls:(typeof k.className==='string'?k.className:'').slice(0,40), r:[q.left,q.top,q.right,q.bottom].map(v=>Math.round(v*10)/10), bg:T(c.backgroundColor)?'':c.backgroundColor, bw:c.borderTopWidth}})});
 }
 return {docW:document.documentElement.scrollWidth, docH:document.documentElement.scrollHeight, conts:out};
}
"""
shell=os.environ["RENDER_SHELL"]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=shell,headless=True,args=["--no-sandbox"])
    for f in sys.argv[1:]:
        for w in (1440,):
            pg=b.new_page(viewport={"width":w,"height":1000})
            pg.goto("file://"+os.path.abspath(f)); pg.wait_for_timeout(600)
            d=pg.evaluate(JS)
            print("=====",f,w,"doc",d["docW"],d["docH"])
            for c in d["conts"]:
                if c["rect"][3]<40: continue
                print(" "*(c["depth"]-2), c["tag"], c["cls"][:50], c["disp"], c["dir"] if 'flex' in c['disp'] else '', "gap",c["cg"],c["rg"], c["rect"])
                for k in c["kids"][:12]:
                    print(" "*(c["depth"]), "  -", k["cls"][:34], k["r"], "bg" if k["bg"] else "", k["bw"] if k['bw']!='0px' else '')
            pg.close()
    b.close()
