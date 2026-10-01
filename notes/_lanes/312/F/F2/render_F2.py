"""#311 overnight wave 1, lane F2 (brief notes/_lanes/312/F/BRIEF.md item 4) - pictures for two calls:
(a) the list rule worked on its own (W-305e1) and (b) the page-header lock-up (W-305e3).
Read-only against canon: nothing under knowledge/ is written; composed pages live in /dev/shm and link the
repo's canon.css and type.css by absolute file:// path. Usage, at the seat after seat_env.sh:
  python3 notes/_lanes/312/F/F2/render_F2.py list|header|all"""
import os, sys, json, io, re, subprocess
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont
R=os.getcwd(); OUT="notes/_lanes/312/F/F2/img"; SH="/dev/shm/f311F2"; os.makedirs(SH,exist_ok=True); os.makedirs(OUT,exist_ok=True)
SHA=subprocess.run(["git","rev-parse","--short","HEAD"],capture_output=True,text=True).stdout.strip()
DEMO="dashboards/international-banking-dashboard.canon.html"
demo_src=open(DEMO).read()
def absolutise(s,rel="../"): return s.replace(f'{rel}knowledge/',f'file://{R}/knowledge/')
def write(name,s): open(f"{SH}/{name}","w").write(s); return f"file://{SH}/{name}"
SET="""([th,mode])=>{const r=document.documentElement;
  if(th) r.setAttribute('data-apollo-theme',th); else r.removeAttribute('data-apollo-theme');
  r.setAttribute('data-theme',mode); document.querySelectorAll('[data-theme]').forEach(e=>e.setAttribute('data-theme',mode));}"""
def launch(p): return p.chromium.launch(executable_path=os.environ["RENDER_SHELL"])
def font(n):
    for f in ("/System/Library/Fonts/Helvetica.ttc","DejaVuSans.ttf","/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        try: return ImageFont.truetype(f,n)
        except Exception: pass
    return ImageFont.load_default()
def label(img,text):
    W,H=img.size; c=Image.new("RGB",(W,H+40),(240,240,240)); c.paste(img,(0,40)); ImageDraw.Draw(c).text((12,9),text,fill=(20,20,20),font=font(20)); return c
def stack(imgs,labels,gap=14):
    ims=[label(i,l) for i,l in zip(imgs,labels)]; W=max(i.width for i in ims)
    s=Image.new("RGB",(W,sum(i.height for i in ims)+gap*(len(ims)-1)),(128,128,128)); y=0
    for i in ims: s.paste(i,(0,y)); y+=i.height+gap
    return s
def shot(pg,sel,path=None,pad=0):
    e=pg.query_selector(sel); e.scroll_into_view_if_needed(); pg.wait_for_timeout(150)
    if pad:
        bb=e.bounding_box(); sy=pg.evaluate("window.scrollY"); sx=pg.evaluate("window.scrollX")
        png=pg.screenshot(clip={"x":bb["x"]+sx-pad,"y":bb["y"]+sy-pad,"width":bb["width"]+2*pad,"height":bb["height"]+2*pad},full_page=True)
    else: png=e.screenshot()
    if path: open(path,"wb").write(png)
    return Image.open(io.BytesIO(png))
# ---------- the 12 payment records, lifted from the demo's own DATA (the same records in every shape) ----------
m=re.search(r"const DATA=(\[\[.*?\]\])\.map",demo_src,re.S); DATA=__import__("ast").literal_eval(m.group(1))
def money(cur,n): return f"{cur} {n:,.0f}"
def table_html(width):
    rows="".join(f'<tr><th scope="row" data-first data-label="Counterparty"><span class="v">{c}</span></th>'
                 f'<td data-label="Reference"><span class="v">{ref}</span></td><td data-label="Market"><span class="v">{mk}</span></td>'
                 f'<td data-label="Date"><span class="v">{d}</span></td><td data-label="Status"><span class="v">{st}</span></td>'
                 f'<td data-label="Amount" class="num"><span class="v">{"−" if dr=="debit" else "+"}{money(cur,amt)}</span></td></tr>'
                 for d,c,ref,mk,cur,dr,amt,st in DATA)
    return f"""<!doctype html><html lang="en" data-theme="light"><head><meta charset="utf-8">
<link rel="stylesheet" href="file://{R}/knowledge/canon/type.css"><link rel="stylesheet" href="file://{R}/knowledge/canon/canon.css">
<style>body{{margin:0;padding:24px;background:var(--background-default,#fff)}} .box{{width:{width}px}}</style></head>
<body><div class="box"><div class="cn-table"><table data-headers="both"><caption class="t-cm-section-label">International payment activity <span class="sub t-cm-caption">12 payments, amounts read down the column</span></caption>
<thead><tr><th scope="col">Counterparty</th><th scope="col">Reference</th><th scope="col">Market</th><th scope="col">Date</th><th scope="col">Status</th><th scope="col" class="num">Amount</th></tr></thead>
<tbody>{rows}</tbody></table></div></div></body></html>"""
# ---------- the three lock-up arrangements, composed from canon classes only (.cn-page-header-lockup) ----------
HDR_RE=re.compile(r'<section class="dashboard-page-header cn-page-header-lockup".*?</section>',re.S)
CHEV='<span class="sep" aria-hidden="true"><svg class="chev" viewBox="0 0 18 18"><path fill-rule="evenodd" clip-rule="evenodd" d="M4.15234 17L12.1503 9L4.15234 1H5.84834L13.8483 9L5.84834 17H4.15234Z" fill="currentColor"/></svg></span>'
HDR_B=f'''<section class="dashboard-page-header cn-page-header-lockup" id="overview" aria-labelledby="pageTitle"><div class="ph-outer"><div class="ph">
<nav class="ph-crumb" aria-label="Breadcrumb"><ol class="t-cm-caption"><li><a class="crumb" href="#">Treasury</a></li><li>{CHEV}<a class="crumb" href="#">Positions</a></li><li>{CHEV}<span class="t-cm-ctl-14" aria-current="page">Global treasury overview</span></li></ol></nav>
<div class="ph-row"><div class="ph-titleblock"><h1 class="ph-title t-cm-heading" id="pageTitle">Global treasury overview</h1><div class="ph-meta t-cm-legal">Consolidated position · 28 August 2026 · GBP equivalent</div></div>
<div class="ph-actions"><button class="btn tertiary" type="button" id="exportButton">Export CSV</button><button class="btn primary" type="button">New payment</button></div></div>
<div class="ph-tabs tabs-b"><div class="tablist" role="tablist" aria-label="Treasury views"><button class="tab t-cm-button" role="tab" aria-selected="true" tabindex="0">Overview</button><button class="tab t-cm-button" role="tab" aria-selected="false" tabindex="-1">Cash positions</button><button class="tab t-cm-button" role="tab" aria-selected="false" tabindex="-1">Payments</button><button class="tab t-cm-button" role="tab" aria-selected="false" tabindex="-1">FX exposure</button><button class="tab t-cm-button" role="tab" aria-selected="false" tabindex="-1">Reports</button><span class="indicator" aria-hidden="true" style="left:0;width:88px"></span></div></div>
</div></div></section>'''
HDR_C='''<section class="dashboard-page-header cn-page-header-lockup" id="overview" aria-labelledby="pageTitle"><div class="ph-outer"><div class="ph">
<div class="ph-row"><div class="ph-titleblock"><span class="eyebrow t-cm-caption">Corporate international banking</span><h1 class="ph-title t-cm-heading" id="pageTitle">Global treasury overview</h1></div></div>
<div class="ph-row" style="align-items:center"><div class="ph-titleblock"><div class="ph-meta t-cm-legal">Consolidated position · 28 August 2026 · GBP equivalent</div></div>
<div class="ph-actions"><button class="btn tertiary" type="button" id="exportButton">Export CSV</button><button class="btn primary" type="button">New payment</button></div></div>
</div></div></section>'''
def demo_with_header(name,hdr):
    s=absolutise(demo_src); s=HDR_RE.sub(lambda _: hdr, s, count=1); return write(name,s)
U_A=write("demo-a.html",absolutise(demo_src)); U_B=demo_with_header("demo-b.html",HDR_B); U_C=demo_with_header("demo-c.html",HDR_C)
GRID="file://"+R+"/knowledge/snippets/Data-grid.reference.html"
job=sys.argv[1] if len(sys.argv)>1 else "all"; facts={"sha":SHA,"records":len(DATA)}
with sync_playwright() as p:
    b=launch(p)
    if job in ("list","all"):
        pg=b.new_page(viewport={"width":1440,"height":1100})
        for mode in ("light","dark"):
            pg.goto(U_A); pg.wait_for_timeout(500); pg.evaluate(SET,["",mode]); pg.wait_for_timeout(300)
            bb=pg.query_selector("#transactions").bounding_box(); facts[f"tile_{mode}"]={k:round(v) for k,v in bb.items()}
            facts[f"rows_shown_{mode}"]=pg.evaluate("document.querySelectorAll('#transactionList li').length")
            a=shot(pg,"#transactions",f"{OUT}/01-list-as-built-{mode}.png")
            # the same list filtered to Europe, through the tile's own filter (chips appear)
            pg.click('[data-filter="market"] .trigger'); pg.wait_for_timeout(200); pg.click('#marketMenu [data-value="Europe"]'); pg.wait_for_timeout(400)
            facts[f"rows_europe_{mode}"]=pg.evaluate("document.querySelectorAll('#transactionList li').length")
            facts[f"count_text_{mode}"]=pg.evaluate("document.getElementById('transactionCount').textContent")
            f=shot(pg,"#transactions",f"{OUT}/01-list-filtered-europe-{mode}.png")
            # the same twelve records as a table on canon, at the tile's width
            pg.goto(write(f"table-{mode}.html",table_html(round(bb["width"])))); pg.wait_for_timeout(400); pg.evaluate(SET,["",mode]); pg.wait_for_timeout(200)
            t=shot(pg,".cn-table",f"{OUT}/01-table-{mode}.png",pad=8)
            # the canon data grid reference, its own records, cropped to the grid
            pg.goto(GRID); pg.wait_for_timeout(700); pg.evaluate(SET,["",mode]); pg.wait_for_timeout(400)
            g=shot(pg,"#dg",f"{OUT}/01-grid-{mode}.png",pad=8)
            stack([a,f,t,g],["List, as the demo stands: search, two filters, a direction switch, pages",
                              "The same list filtered to Europe: the rule he rejected would make this a data grid",
                              "The same twelve payments as a table: the amounts are read DOWN a column",
                              "The data grid (canon reference, its own records): select, column filters, edit in place"]).save(f"{OUT}/01-three-shapes-{mode}.png")
    if job in ("header","all"):
        pg=b.new_page(viewport={"width":1440,"height":900})
        for mode in ("light","dark"):
            ims=[]
            for nm,u in (("a",U_A),("b",U_B),("c",U_C)):
                pg.goto(u); pg.wait_for_timeout(500); pg.evaluate(SET,["",mode]); pg.wait_for_timeout(300)
                if nm=="b": pg.evaluate("()=>{const t=document.querySelector('.ph-tabs .tab[aria-selected=true]'),i=document.querySelector('.ph-tabs .indicator');if(t&&i){i.style.left=t.offsetLeft+'px';i.style.width=t.offsetWidth+'px'}}")
                bb=pg.query_selector(".dashboard-page-header").bounding_box(); facts[f"header_{nm}_{mode}"]={k:round(v) for k,v in bb.items()}
                ims.append(shot(pg,".dashboard-page-header",f"{OUT}/02-lockup-{nm}-{mode}.png"))
            stack(ims,["Option 1, as built: eyebrow, title, meta line; the action on the title row",
                       "Option 2, the drill-down: breadcrumb, title and actions, the tab strip on the lock-up's foot",
                       "Option 3, two rows: the title alone on its row; meta line and actions share the second"]).save(f"{OUT}/02-lockup-options-{mode}.png")
        # the recommended shape at phone width, light
        pg=b.new_page(viewport={"width":390,"height":844})
        for nm,u in (("a",U_A),("b",U_B)):
            pg.goto(u); pg.wait_for_timeout(500); pg.evaluate(SET,["","light"]); pg.wait_for_timeout(300)
            pg.evaluate("()=>{const t=document.querySelector('.ph-tabs .tab[aria-selected=true]'),i=document.querySelector('.ph-tabs .indicator');if(t&&i){i.style.left=t.offsetLeft+'px';i.style.width=t.offsetWidth+'px'}}")
            bb=pg.query_selector(".dashboard-page-header").bounding_box(); facts[f"header_{nm}_390"]={k:round(v) for k,v in bb.items()}
            shot(pg,".dashboard-page-header",f"{OUT}/02-lockup-{nm}-390.png")
    b.close()
json.dump(facts,open(f"{OUT}/facts-{job}.json","w"),indent=1); print(json.dumps(facts,indent=1))
