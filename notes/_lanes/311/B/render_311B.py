"""#311 lane B — pictures and facts for s311-D1 (dark icons follow the ink) and s311-D2 (Supercharge's dark
page and section take warm/4 #25211C). BEFORE = canon.css at 84bd8c93 (the tree before this lane), written to
/dev/shm with copies of the pages whose links point at it; AFTER = the tree. Nothing is scratch-overridden.
Usage: python3 render_311B.py count|icons|scpage   (at the seat, after seat_env.sh)"""
import os, sys, json, io, subprocess
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont
R=os.getcwd(); OUT="notes/_lanes/311/B/img"; SH="/dev/shm/b311B"; os.makedirs(SH,exist_ok=True); os.makedirs(OUT,exist_ok=True)
BASE="84bd8c93"
open(f"{SH}/canon-before.css","w").write(subprocess.run(["git","show",f"{BASE}:knowledge/canon/canon.css"],capture_output=True,text=True,check=True).stdout)
def before_copy(src,name,rel):
    s=open(src).read()
    s=s.replace(f'{rel}knowledge/canon/canon.css',f'file://{SH}/canon-before.css').replace(f'{rel}knowledge/',f'file://{R}/knowledge/')
    open(f"{SH}/{name}","w").write(s); return f"file://{SH}/{name}"
DEMO="dashboards/international-banking-dashboard.canon.html"
U={"after":"file://"+R+"/"+DEMO,"before":before_copy(DEMO,"demo.html","../")}
SCP="notes/_lanes/311/B/sc-page.html"
US={"after":"file://"+R+"/"+SCP,"before":before_copy(SCP,"sc.html","../../../../")}
SET="""([th,mode])=>{const r=document.documentElement;
  if(th) r.setAttribute('data-apollo-theme',th); else r.removeAttribute('data-apollo-theme');
  r.setAttribute('data-theme',mode); document.querySelectorAll('[data-theme]').forEach(e=>e.setAttribute('data-theme',mode));}"""
LIB="""const hex=c=>{const m=c.match(/[\\d.]+/g);return '#'+m.slice(0,3).map(n=>(+n|0).toString(16).padStart(2,'0')).join('').toUpperCase()};
 const L=h=>{const r=[1,3,5].map(i=>parseInt(h.slice(i,i+2),16)/255).map(x=>x<=0.04045?x/12.92:((x+0.055)/1.055)**2.4);return .2126*r[0]+.7152*r[1]+.0722*r[2]};
 const cr=(a,b)=>{const x=L(a),y=L(b);return +((Math.max(x,y)+.05)/(Math.min(x,y)+.05)).toFixed(2)};
 const bgOf=e=>{while(e){const b=getComputedStyle(e).backgroundColor;if(!/^rgba\\(.*, 0\\)$/.test(b))return hex(b);e=e.parentElement}return '#FFFFFF'};"""
# An icon = an <svg> outside a chart canvas (.dv-svg), drawn (non-zero box). Painted white = a shape inside it
# resolves fill or stroke to rgb(255,255,255). Counted per icon element, with the nav search bar opened.
COUNT="()=>{"+LIB+"""const W='rgb(255, 255, 255)';
 const vis=e=>{const r=e.getBoundingClientRect();return r.width>0&&r.height>0};
 const icons=[...document.querySelectorAll('svg')].filter(s=>!s.closest('.dv-svg')&&!s.classList.contains('dashboard-live')&&vis(s));
 const white=icons.filter(s=>[...s.querySelectorAll('path,circle,rect,line,polyline,polygon,ellipse,use')].some(e=>{const cs=getComputedStyle(e);return cs.fill===W||cs.stroke===W}));
 const where=s=>{const h=s.parentElement;return h.tagName.toLowerCase()+'.'+String(h.className).split(' ')[0]+(h.closest('.cn-navigations')?' (header)':'')};
 const pair=(icoSel,txtSel)=>{const i=document.querySelector(icoSel),t=document.querySelector(txtSel);if(!i||!t)return null;
   const ic=hex(getComputedStyle(i).color), tc=hex(getComputedStyle(t,'::placeholder').color), g=bgOf(t); return {icon:ic,placeholder:tc,ground:g,icon_cr:cr(ic,g),text_cr:cr(tc,g)}};
 return {icons:icons.length,white:white.length,white_where:white.map(where),
   header_glass:pair('.nav-searchbar .mag','.nav-searchbar input'),toolbar_glass:pair('.ftb-search .mag','.ftb-search input'),
   text_default:getComputedStyle(document.documentElement).getPropertyValue('--text-default').trim(),
   icon_default:getComputedStyle(document.querySelector('.cn-navigations')).getPropertyValue('--icon-default').trim()}}"""
def launch(p): return p.chromium.launch(executable_path=os.environ["RENDER_SHELL"])
def font(n):
    for f in ("/System/Library/Fonts/Helvetica.ttc","DejaVuSans.ttf"):
        try: return ImageFont.truetype(f,n)
        except Exception: pass
    return ImageFont.load_default()
def label(img,text):
    W,H=img.size; c=Image.new("RGB",(W,H+44),(245,245,245)); c.paste(img,(0,44)); ImageDraw.Draw(c).text((12,10),text,fill=(20,20,20),font=font(22)); return c
def side(a,b,la,lb,gap=16):
    a=label(a,la); b=label(b,lb); s=Image.new("RGB",(a.width+gap+b.width,max(a.height,b.height)),(128,128,128)); s.paste(a,(0,0)); s.paste(b,(a.width+gap,0)); return s
def open_nav(pg):
    pg.evaluate("()=>{const b=document.getElementById('navSearch'); if(b) b.hidden=false}"); pg.wait_for_timeout(200)
THEMES=[("mono",""),("console","console"),("common","legacy"),("supercharge","supercharge")]
job=sys.argv[1]; facts={}; FF=f"{OUT}/facts-{job}.json"
with sync_playwright() as p:
    b=launch(p)
    if job=="count":
        pg=b.new_page(viewport={"width":1440,"height":900})
        for nm,th in THEMES:
            for rd in ("before","after"):
                pg.goto(U[rd]); pg.wait_for_timeout(400); pg.evaluate(SET,[th,"dark"]); open_nav(pg); pg.wait_for_timeout(500)
                k=f"{nm}-{rd}"; facts[k]=pg.evaluate(COUNT); print(k,facts[k])
    elif job=="icons":
        pg=b.new_page(viewport={"width":1440,"height":900})
        for rd in ("before","after"):
            pg.goto(U[rd]); pg.wait_for_timeout(400); pg.evaluate(SET,["console","dark"]); open_nav(pg); pg.wait_for_timeout(600)
            y=pg.evaluate("document.querySelector('.ftb-search').getBoundingClientRect().bottom")+24
            pg.screenshot(path=f"{OUT}/01-console-{rd}-top.png",clip={"x":0,"y":0,"width":1440,"height":y},full_page=True)
        pg=b.new_page(viewport={"width":1440,"height":900},device_scale_factor=2); crops={}
        for rd in ("before","after"):
            pg.goto(U[rd]); pg.wait_for_timeout(400); pg.evaluate(SET,["console","dark"]); open_nav(pg); pg.wait_for_timeout(600)
            parts=[]
            for sel in (".nav-searchbar .nav-search",".ftb-search .search"):
                e=pg.query_selector(sel); e.scroll_into_view_if_needed(); bb=e.bounding_box()
                c=Image.open(io.BytesIO(pg.screenshot(clip={"x":bb["x"],"y":bb["y"],"width":min(bb["width"],230),"height":bb["height"]})))
                parts.append(c.resize((c.width*2,c.height*2),Image.NEAREST))   # 2x DPR x 2 = 4x
            W=max(q.width for q in parts); s=Image.new("RGB",(W,sum(q.height for q in parts)+16),(128,128,128)); y=0
            for q in parts: s.paste(q,(0,y)); y+=q.height+16
            crops[rd]=s
        side(crops["before"],crops["after"],"Before: glass #FFFFFF","After: glass #E1E1E1, as the text").save(f"{OUT}/01-crop-console-4x.png")
    elif job=="scpage":
        pg=b.new_page(viewport={"width":1440,"height":900})
        MEAS="()=>{"+LIB+"""const rs=getComputedStyle(document.documentElement),v=n=>rs.getPropertyValue(n).trim().toUpperCase();
          const page=hex(getComputedStyle(document.body).backgroundColor), sec=hex(getComputedStyle(document.querySelector('.sc-section')).backgroundColor),
                tile=hex(getComputedStyle(document.querySelector('.dashboard-tile')).backgroundColor), ink=hex(getComputedStyle(document.querySelector('.metric-val')).color),
                nav=bgOf(document.querySelector('.cn-navigations .masthead'));
          return {page,section:sec,tile,nav,ink,tile_on_page:cr(tile,page),tile_on_section:cr(tile,sec),ink_on_tile:cr(ink,tile),ink_on_page:cr(ink,page),
            tokens:{'background/default':v('--background-default'),'surface/section':v('--surface-section'),'surface/raised':v('--surface-raised'),'surface/digital-black':v('--surface-digital-black'),'tertiary/background/pressed':v('--tertiary-background-pressed')}}}"""
        for rd in ("before","after"):
            pg.goto(US[rd]); pg.wait_for_timeout(400); pg.evaluate(SET,["supercharge","dark"]); pg.wait_for_timeout(600)
            facts[rd]=pg.evaluate(MEAS); print(rd,facts[rd])
            h=pg.evaluate("document.querySelector('.sc-stack').getBoundingClientRect().bottom")
            pg.screenshot(path=f"{OUT}/02-sc-{rd}.png",clip={"x":0,"y":0,"width":1440,"height":h},full_page=True)
    b.close()
if facts: json.dump(facts,open(FF,"w"),indent=1)
