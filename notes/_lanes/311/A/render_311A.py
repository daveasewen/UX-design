"""#311 lane A — pictures for the soft white (s310-D7), the tab strip (s310-D8) and Supercharge's dark page.
BEFORE = canon.css at the commit before the build (6faaca8d~1), written to /dev/shm with a copy of the page
whose links point at it; AFTER = the tree. Supercharge page variants are SCRATCH overrides on the page only.
Usage: python3 render_311A.py ink|crop|tabs|scpage   (run at the seat after seat_env.sh)"""
import os, sys, json, io, subprocess
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont
R=os.getcwd(); OUT="notes/_lanes/311/A/img"; SH="/dev/shm/b311"; os.makedirs(SH,exist_ok=True)
BASE="6faaca8d~1"
open(f"{SH}/canon-before.css","w").write(subprocess.run(["git","show",f"{BASE}:knowledge/canon/canon.css"],capture_output=True,text=True,check=True).stdout)
def before_copy(src,name,rel):
    s=open(src).read()
    s=s.replace(f'{rel}knowledge/canon/canon.css',f'file://{SH}/canon-before.css').replace(f'{rel}knowledge/',f'file://{R}/knowledge/')
    open(f"{SH}/{name}","w").write(s); return f"file://{SH}/{name}"
DEMO="dashboards/international-banking-dashboard.canon.html"
U={"after":"file://"+R+"/"+DEMO,"before":before_copy(DEMO,"demo.html","../")}
CTX="notes/_lanes/311/A/tabs-context.html"
UC={"after":"file://"+R+"/"+CTX,"before":before_copy(CTX,"ctx.html","../../../../")}
SET="""([th,mode])=>{const r=document.documentElement;
  if(th) r.setAttribute('data-apollo-theme',th); else r.removeAttribute('data-apollo-theme');
  r.setAttribute('data-theme',mode); document.querySelectorAll('[data-theme]').forEach(e=>e.setAttribute('data-theme',mode));}"""
LIB="""const hex=c=>{const m=c.match(/[\\d.]+/g);return '#'+m.slice(0,3).map(n=>(+n|0).toString(16).padStart(2,'0')).join('').toUpperCase()};
 const L=h=>{const r=[1,3,5].map(i=>parseInt(h.slice(i,i+2),16)/255).map(x=>x<=0.04045?x/12.92:((x+0.055)/1.055)**2.4);return .2126*r[0]+.7152*r[1]+.0722*r[2]};
 const cr=(a,b)=>{const x=L(a),y=L(b);return +((Math.max(x,y)+.05)/(Math.min(x,y)+.05)).toFixed(2)};
 const bgOf=e=>{while(e){const b=getComputedStyle(e).backgroundColor;if(!/^rgba\\(.*, 0\\)$/.test(b))return hex(b);e=e.parentElement}return '#FFFFFF'};
 const eff=(e,ground)=>{let a=1,x=e;while(x&&x!==document.body){a*=+getComputedStyle(x).opacity;x=x.parentElement}
   const c=getComputedStyle(e).color.match(/[\\d.]+/g).map(Number), tb=[1,3,5].map(i=>parseInt(ground.slice(i,i+2),16));
   return {alpha:+a.toFixed(2), hex:'#'+[0,1,2].map(i=>Math.round(a*c[i]+(1-a)*tb[i]).toString(16).padStart(2,'0')).join('').toUpperCase()}};"""
FACTS="()=>{"+LIB+"""
 const t=document.querySelector('.dashboard-tile'); const tile=hex(getComputedStyle(t).backgroundColor);
 const ground=hex(getComputedStyle(document.querySelector('.c-bento.dashboard-bento')).backgroundColor);
 const ph=document.querySelector('.ph-title'); const phg=bgOf(ph);
 const rs=getComputedStyle(document.documentElement), v=n=>rs.getPropertyValue(n).trim().toUpperCase();
 const tv=n=>getComputedStyle(t).getPropertyValue(n).trim().toUpperCase();
 const q=s=>{const e=document.querySelector(s);return e?hex(getComputedStyle(e).color):null};
 const body=q('.metric-val'); const se=eff(document.querySelector('.metric-per'),tile); const ti=eff(document.querySelector('.dv-title'),tile);
 const chev=[...document.querySelectorAll('.chev')].map(e=>hex(getComputedStyle(e).color));
 const whites=[...document.querySelectorAll('body *')].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&[...e.childNodes].some(n=>n.nodeType==3&&n.textContent.trim())&&getComputedStyle(e).color=='rgb(255, 255, 255)'}).length;
 const inks={'text/default':v('--text-default'),'text/secondary':v('--text-secondary'),'rag/success-ink':v('--rag-success-ink'),'rag/error-ink':v('--rag-error-ink'),
   'rag/success (glyph)':v('--rag-success'),'rag/warning (glyph)':v('--rag-warning'),'rag/error (glyph)':v('--rag-error'),'rag/information (glyph)':v('--rag-information')};
 const grounds={tile:tile,ground:ground,page:v('--background-default')};
 const pairs={}; for(const [k,c] of Object.entries(inks)){ if(!/^#[0-9A-F]{6}$/.test(c)) continue; pairs[k]={ink:c}; for(const [g,gc] of Object.entries(grounds)) pairs[k][g]=cr(c,gc);}
 return {page:v('--background-default'),ground,tile,header_ground:phg,header_text:q('.ph-title'),header_cr:cr(q('.ph-title'),phg),body,body_cr:cr(body,tile),
   secondary60:se.hex,secondary60_cr:cr(se.hex,tile),title_eff:ti.hex,title_eff_cr:cr(ti.hex,tile),chevrons:chev,pure_white_text_nodes:whites,pairs}}"""
def launch(p): return p.chromium.launch(executable_path=os.environ["RENDER_SHELL"])
def label(img,text):
    W,H=img.size; c=Image.new("RGB",(W,H+44),(245,245,245)); c.paste(img,(0,44)); d=ImageDraw.Draw(c)
    try: f=ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc",22)
    except Exception:
        try: f=ImageFont.truetype("DejaVuSans.ttf",22)
        except Exception: f=ImageFont.load_default()
    d.text((12,10),text,fill=(20,20,20),font=f); return c
def side(a,b,la,lb,gap=16):
    a=label(a,la); b=label(b,lb); W=a.width+gap+b.width; H=max(a.height,b.height)
    s=Image.new("RGB",(W,H),(128,128,128)); s.paste(a,(0,0)); s.paste(b,(a.width+gap,0)); return s
THEMES=[("mono",""),("console","console"),("common","legacy")]
job=sys.argv[1]; facts={}
FF=f"{OUT}/facts-{job}.json"
with sync_playwright() as p:
    b=launch(p)
    if job=="ink":
        pg=b.new_page(viewport={"width":1440,"height":900})
        for nm,th in THEMES+[("supercharge","supercharge")]:
            for rd in ("before","after"):
                pg.goto(U[rd]); pg.wait_for_timeout(400); pg.evaluate(SET,[th,"dark"]); pg.wait_for_timeout(700)
                k=f"{nm}-{rd}"; facts[k]=pg.evaluate(FACTS)
                top=pg.query_selector(".dashboard-bento-stack").bounding_box()
                if nm!="supercharge" or rd=="after":
                    pg.screenshot(path=f"{OUT}/01-{k}-top.png",clip={"x":0,"y":0,"width":1440,"height":top["y"]+470})
                print(k,{x:facts[k][x] for x in ("page","ground","tile","body","body_cr","secondary60_cr","header_cr","chevrons","pure_white_text_nodes")})
    elif job=="crop":
        pg=b.new_page(viewport={"width":1440,"height":900},device_scale_factor=2)
        shots={}
        for rd in ("before","after"):
            pg.goto(U[rd]); pg.wait_for_timeout(400); pg.evaluate(SET,["console","dark"]); pg.wait_for_timeout(700)
            mt=pg.query_selector(".dashboard-stat-tile"); mt.scroll_into_view_if_needed()
            a=Image.open(io.BytesIO(mt.screenshot())).crop((0,0,2*260,2*110))
            row=pg.query_selector(".cn-list-items button.row"); row.scroll_into_view_if_needed()
            z=Image.open(io.BytesIO(row.screenshot())); z=z.crop((0,0,min(z.width,2*360),z.height))
            a=a.resize((a.width*2,a.height*2),Image.NEAREST); z=z.resize((z.width*2,z.height*2),Image.NEAREST)
            W=max(a.width,z.width); s2=Image.new("RGB",(W,a.height+16+z.height),(128,128,128)); s2.paste(a,(0,0)); s2.paste(z,(0,a.height+16))
            tr=pg.query_selector_all(".ftb-filter .trigger")[:2]
            bx=[t.bounding_box() for t in tr]; x0=min(q["x"] for q in bx)-8; y0=min(q["y"] for q in bx)-8
            x1=max(q["x"]+q["width"] for q in bx)+8; y1=max(q["y"]+q["height"] for q in bx)+8
            tr[0].scroll_into_view_if_needed(); bx=[t.bounding_box() for t in tr]
            x0=min(q["x"] for q in bx)-8; y0=min(q["y"] for q in bx)-8; x1=max(q["x"]+q["width"] for q in bx)+8; y1=max(q["y"]+q["height"] for q in bx)+8
            c=Image.open(io.BytesIO(pg.screenshot(clip={"x":x0,"y":y0,"width":x1-x0,"height":y1-y0})))
            c=c.resize((c.width*2,c.height*2),Image.NEAREST)
            shots[rd]=(s2,c)
        side(shots["before"][0],shots["after"][0],"Before: #FFFFFF","After: #E1E1E1").save(f"{OUT}/01-crop-console.png")
        side(shots["before"][1],shots["after"][1],"Before: white chevrons","After: they follow the text").save(f"{OUT}/01-chevrons-console.png")
    elif job=="tabs":
        pg=b.new_page(viewport={"width":1440,"height":900})
        MEAS="()=>{"+LIB+"""return [...document.querySelectorAll('.ctx')].map(c=>{const l=c.querySelector('.tablist');const strip=getComputedStyle(l).backgroundColor;
          const g=bgOf(l.parentElement); const lab=c.querySelector('.tab[aria-selected=false]'); const e=eff(lab,g); const ind=c.querySelector('.indicator');
          return {ctx:c.querySelector('.cap').textContent.slice(0,3),strip:strip,ground:g,label:e.hex,label_alpha:e.alpha,label_cr:cr(e.hex,g),
            selected_cr:cr(hex(getComputedStyle(c.querySelector('.tab[aria-selected=true]')).color),g),bar:hex(getComputedStyle(ind).backgroundColor),bar_cr:cr(hex(getComputedStyle(ind).backgroundColor),g)}})}"""
        for th,mode in (("console","light"),("console","dark"),("supercharge","dark")):
            for rd in ("before","after"):
                pg.goto(UC[rd]); pg.wait_for_timeout(400); pg.evaluate(SET,[th,mode]); pg.wait_for_timeout(700); pg.evaluate("place()")
                k=f"{th}-{mode}-{rd}"; facts[k]=pg.evaluate(MEAS); print(k,[(f['ctx'],f['strip'],f['ground'],f['label_cr'],f['bar_cr']) for f in facts[k]])
                h=pg.evaluate("document.querySelector('.grid').getBoundingClientRect().height")
                pg.screenshot(path=f"{OUT}/02-ctx-{k}.png",clip={"x":0,"y":0,"width":1440,"height":h})
    elif job=="scpage":
        pg=b.new_page(viewport={"width":1440,"height":900})
        V=[("asis",None),("fix-13110E","#13110E"),("warm4-25211C","#25211C")]
        MEAS="()=>{"+LIB+"""const rs=getComputedStyle(document.documentElement),v=n=>rs.getPropertyValue(n).trim().toUpperCase();
          const out={page:hex(getComputedStyle(document.body).backgroundColor),bg_default:v('--background-default'),section:v('--surface-section'),subtle:v('--surface-subtle'),tile:v('--surface-raised'),ink:v('--text-default')};
          out.tile_on_page=cr(out.tile,out.bg_default); out.tile_on_section=cr(out.tile,out.section); out.tile_on_subtle=cr(out.tile,out.subtle); out.ink_on_page=cr(out.ink,out.bg_default); return out}"""
        for vn,val in V:
            css=("" if not val else f"html[data-apollo-theme=supercharge],html[data-apollo-theme=supercharge] *{{--background-default:{val}!important;--page:{val}!important;--nav-page:{val}!important;--surface-section:{val}!important}}html[data-apollo-theme=supercharge] body,html[data-apollo-theme=supercharge] .grid{{background:{val}!important}}")
            for src,uu in (("demo",U["after"]),("ctx",UC["after"])):  # the demo's page is its bento ground: measured, not pictured
                if src=="demo" and "--pictures-demo" not in sys.argv: pass
                pg.goto(uu); pg.wait_for_timeout(400); pg.evaluate(SET,["supercharge","dark"])
                if css: pg.add_style_tag(content=css)
                pg.wait_for_timeout(700)
                if src=="ctx": pg.evaluate("place()")
                k=f"{vn}-{src}"; facts[k]=pg.evaluate(MEAS)
                if src=="demo":
                    facts[k]["header_ground"]=pg.evaluate("()=>{"+LIB+"return bgOf(document.querySelector('.ph-title'))}")
                    if "--pictures-demo" in sys.argv:
                        top=pg.query_selector(".dashboard-bento-stack").bounding_box()
                        pg.screenshot(path=f"{OUT}/03-sc-{vn}-demo.png",clip={"x":0,"y":0,"width":1440,"height":top["y"]+300})
                else:
                    h=pg.evaluate("document.querySelector('.grid').getBoundingClientRect().height")
                    pg.screenshot(path=f"{OUT}/03-sc-{vn}-ctx.png",clip={"x":0,"y":0,"width":1440,"height":h})
                print(k,facts[k])
    b.close()
if facts: json.dump(facts,open(FF,"w"),indent=1)
