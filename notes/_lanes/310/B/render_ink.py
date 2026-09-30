"""#310 lane B — the white ink on black tiles: five options, alive on the banking demo (Console dark).
Each option is applied to the LIVE tree by page-level CSS custom properties only (no canon edit):
  ink  -> --text-default and --text-secondary on every dark element (the token a ruling would move)
  tile -> --surface-raised/--tertiary-background-default/--surface on the tiles
  grey -> data-dark-tiles="grey" (the registered s310-D3 option)
Writes img/02-<opt>-top.png, img/02-<opt>-crop.png and img/ink-facts.json.
"""
import os, json, io
from playwright.sync_api import sync_playwright
from PIL import Image
R=os.getcwd(); OUT="notes/_lanes/310/B/img"; U="file://"+R+"/dashboards/international-banking-dashboard.canon.html"
SET="""([th,mode,opt])=>{const r=document.documentElement;
  if(th) r.setAttribute('data-apollo-theme',th); else r.removeAttribute('data-apollo-theme');
  r.setAttribute('data-theme',mode);
  document.querySelectorAll('[data-theme]').forEach(e=>{e.setAttribute('data-theme',mode);
    if(opt) e.setAttribute('data-dark-tiles',opt); else e.removeAttribute('data-dark-tiles');});}"""
OPTS=[("1-as-built","",None,None),("2a-n13","",'#F0F0F0',None),("2b-n12","",'#E1E1E1',None),("3-grey-tiles","grey",None,None),("4-n3-tile","",None,'#0F0F0F')]
def css(ink,tile):
    s=""
    if ink: s+=f"[data-theme=dark],[data-theme=dark] *{{--text-default:{ink}!important;--text-secondary:{ink}!important}}"
    if tile: s+=f".dashboard-tile{{--surface-raised:{tile}!important;--tertiary-background-default:{tile}!important;--surface:{tile}!important;background-color:{tile}!important}}"
    return s
FACTS="""()=>{const hex=c=>{const m=c.match(/[\\d.]+/g);return '#'+m.slice(0,3).map(n=>(+n|0).toString(16).padStart(2,'0')).join('').toUpperCase()};
 const L=h=>{const r=[1,3,5].map(i=>parseInt(h.slice(i,i+2),16)/255).map(x=>x<=0.04045?x/12.92:((x+0.055)/1.055)**2.4);return .2126*r[0]+.7152*r[1]+.0722*r[2]};
 const cr=(a,b)=>{const x=L(a),y=L(b);return +((Math.max(x,y)+.05)/(Math.min(x,y)+.05)).toFixed(2)};
 const t=document.querySelector('.dashboard-tile'); const tile=hex(getComputedStyle(t).backgroundColor);
 const ground=hex(getComputedStyle(document.querySelector('.c-bento.dashboard-bento')).backgroundColor);
 const page=hex(getComputedStyle(document.body).backgroundColor);
 const q=s=>{const e=document.querySelector(s);return e?hex(getComputedStyle(e).color):null};
 const cs=getComputedStyle(t); const v=n=>cs.getPropertyValue(n).trim();
 const eff=(s)=>{const e=document.querySelector(s);let a=1,x=e;while(x&&x!==document.body){a*=+getComputedStyle(x).opacity;x=x.parentElement}
   const c=getComputedStyle(e).color.match(/[\d.]+/g).map(Number), tb=[1,3,5].map(i=>parseInt(tile.slice(i,i+2),16));
   return {alpha:+a.toFixed(2), hex:'#'+[0,1,2].map(i=>Math.round(a*c[i]+(1-a)*tb[i]).toString(16).padStart(2,'0')).join('').toUpperCase()}};
 const sE=eff('.metric-per'), tE=eff('.dv-title');
 const body=q('.metric-val'), sec=q('.metric-per'), lbl=q('.metric-lbl');
 const white=[...document.querySelectorAll('.dashboard-tile *')].filter(e=>[...e.childNodes].some(n=>n.nodeType==3&&n.textContent.trim())&&getComputedStyle(e).color=='rgb(255, 255, 255)').length;
 const succ=v('--rag-success-ink'), err=v('--rag-error-ink'), sg=v('--rag-success'), eg=v('--rag-error');
 return {page,ground,tile,tile_on_ground:cr(tile,ground),body,body_cr:cr(body,tile),secondary:sec,secondary_cr:cr(sec,tile),label:lbl,
   rag_success_ink:succ,succ_cr:cr(succ,tile),rag_error_ink:err,err_cr:cr(err,tile),rag_success_glyph:sg,sg_cr:cr(sg,tile),rag_error_glyph:eg,eg_cr:cr(eg,tile),
   ground_text_cr:cr(body,ground),secondary_alpha:sE.alpha,secondary_eff:sE.hex,secondary_eff_cr:cr(sE.hex,tile),title_eff:tE.hex,title_eff_cr:cr(tE.hex,tile),pure_white_text_left_in_tiles:white}}"""
facts={}
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=os.environ["RENDER_SHELL"])
    for dsf in (1,2):
        pg=b.new_page(viewport={"width":1440,"height":900},device_scale_factor=dsf)
        for name,opt,ink,tile in OPTS:
            pg.goto(U); pg.wait_for_timeout(500)
            pg.evaluate(SET,["console","dark",opt]); 
            s=css(ink,tile)
            if s: pg.add_style_tag(content=s)
            pg.wait_for_timeout(900)
            if dsf==1:
                facts[name]=pg.evaluate(FACTS)
                top=pg.query_selector(".dashboard-bento-stack").bounding_box()
                pg.screenshot(path=f"{OUT}/02-{name}-top.png",clip={"x":0,"y":top["y"]-10,"width":1440,"height":560})
                print(name,facts[name])
            else:
                mt=pg.query_selector(".dashboard-stat-tile"); mt.scroll_into_view_if_needed()
                a=Image.open(io.BytesIO(mt.screenshot())).crop((0,0,2*260,2*110))
                row=pg.query_selector(".cn-list-items button.row"); row.scroll_into_view_if_needed()
                z=Image.open(io.BytesIO(row.screenshot())); z=z.crop((0,0,min(z.width,2*360),z.height))
                # dsf 2 x nearest 2 = 4x CSS size: the pixels a retina screen draws, enlarged
                a=a.resize((a.width*2,a.height*2),Image.NEAREST); z=z.resize((z.width*2,z.height*2),Image.NEAREST)
                W=max(a.width,z.width); H=a.height+16+z.height
                s2=Image.new("RGB",(W,H),(128,128,128)); s2.paste(a,(0,0)); s2.paste(z,(0,a.height+16)); s2.save(f"{OUT}/02-{name}-crop.png")
        pg.close()
    b.close()
json.dump(facts,open(f"{OUT}/ink-facts.json","w"),indent=1)
