"""#311 overnight wave 1, lane F1 — the top-nav shell as an IA question (W-305e2).
Wireframe options drawn IN SCRATCH over a copy of the banking demo
(dashboards/international-banking-dashboard.canon.html) with canon.css taken from the
committed sha (git show <SHA>:knowledge/canon/canon.css) so the working tree's dirty canon
is never read. Nothing in the tree is edited: the demo's own masthead is hidden and a
wireframe masthead is injected in its place; the page header and bento below stay real.
Usage (at the seat, after seat_env.sh):  python3 notes/_lanes/312/F/render_F1.py <sha>
Writes notes/_lanes/312/F/img/F1-*.png and img/F1-facts.json."""
import os, sys, json, subprocess
from playwright.sync_api import sync_playwright
R=os.getcwd(); OUT="notes/_lanes/312/F/img"; SH="/dev/shm/f1_311"; os.makedirs(SH,exist_ok=True); os.makedirs(OUT,exist_ok=True)
SHA=sys.argv[1] if len(sys.argv)>1 else "HEAD"
sha_full=subprocess.run(["git","rev-parse",SHA],capture_output=True,text=True,check=True).stdout.strip()
open(f"{SH}/canon.css","w").write(subprocess.run(["git","show",f"{SHA}:knowledge/canon/canon.css"],capture_output=True,text=True,check=True).stdout)
open(f"{SH}/type.css","w").write(subprocess.run(["git","show",f"{SHA}:knowledge/canon/type.css"],capture_output=True,text=True,check=True).stdout)
DEMO="dashboards/international-banking-dashboard.canon.html"
s=subprocess.run(["git","show",f"{SHA}:{DEMO}"],capture_output=True,text=True,check=True).stdout
s=s.replace('../knowledge/canon/canon.css',f'file://{SH}/canon.css').replace('../knowledge/canon/type.css',f'file://{SH}/type.css').replace('../knowledge/',f'file://{R}/knowledge/')
open(f"{SH}/demo.html","w").write(s); URL=f"file://{SH}/demo.html"

# ---- the IA used for every option: a corporate international banking portal, nine primaries, three levels ----
IA=[
 ("Overview",[]),
 ("Accounts",[("Positions",["Balances","Intraday","Account groups"]),("Records",["Statements","Advices"])]),
 ("Payments",[("Move money",["Make a payment","Bulk files","Standing orders","Payment templates"]),
              ("Manage",["Beneficiaries","Approvals","Limits"]),
              ("Track",["Payment status","Returns & recalls","Cut-off times"])]),
 ("Receivables",[("Collect",["Direct debits","Virtual accounts"]),("Match",["Reconciliation","Collections"])]),
 ("Liquidity",[("Position",["Cash position","Forecast"]),("Structure",["Pooling & sweeps","Investments"])]),
 ("Trade",[("Finance",["Letters of credit","Guarantees","Trade loans","Supply chain finance"]),("Documents",["Documentary collections","Document upload"])]),
 ("FX",[("",["Spot & forward","Rates","Orders"])]),
 ("Reports",[("",["Scheduled reports","Report builder","Audit log"])]),
 ("Admin",[("People",["Users & roles","Approval matrix"]),("Setup",["Entities","Security"])]),
]
IA_JSON=json.dumps(IA)

CSS="""
.wf-hide{display:none!important}
.wf{--wf-ink:#1F1F1F;--wf-mute:#6B6B6B;--wf-line:#9A9A9A;--wf-fill:#F2F2F2;--wf-fill2:#E4E4E4;--wf-mark:#1F1F1F;
  font:14px/1.3 Helvetica,Arial,sans-serif;color:var(--wf-ink);position:relative;z-index:1000}
.wf *{box-sizing:border-box}
.wf-band{display:flex;align-items:center;gap:24px;padding:0 32px;background:var(--wf-fill);border-bottom:1px dashed var(--wf-line)}
.wf-band.h64{min-height:64px}.wf-band.h56{min-height:56px;background:#FAFAFA}.wf-band.h48{min-height:48px;background:#FAFAFA}
.wf-logo{width:42px;height:36px;border:1px solid var(--wf-line);background:repeating-linear-gradient(135deg,#fff 0 4px,var(--wf-fill2) 4px 8px);flex:none;display:flex;align-items:center;justify-content:center;font-size:10px;color:var(--wf-mute)}
.wf-nav{display:flex;gap:4px;margin-right:auto;min-width:0;height:100%}
.wf-item{display:inline-flex;align-items:center;gap:6px;height:64px;padding:0 12px;position:relative;white-space:nowrap;color:var(--wf-ink)}
.h56 .wf-item{height:56px}.h48 .wf-item{height:48px;font-size:13px}
.wf-item.cur{font-weight:700;box-shadow:inset 0 -3px 0 var(--wf-mark)}
.wf-item.open{background:#fff;box-shadow:inset 0 -3px 0 var(--wf-mark)}
.wf-chev{width:8px;height:8px;border-right:1.5px solid var(--wf-mute);border-bottom:1.5px solid var(--wf-mute);transform:translateY(-2px) rotate(45deg)}
.wf-item.open .wf-chev{transform:translateY(2px) rotate(-135deg)}
.wf-acts{display:flex;gap:4px;flex:none}
.wf-btn{width:44px;height:44px;border:1px dashed var(--wf-line);display:flex;align-items:center;justify-content:center;font-size:10px;color:var(--wf-mute);background:#fff}
.wf-menu{position:relative}
.wf-mega{position:absolute;left:0;right:0;top:100%;background:#fff;border-bottom:1px solid var(--wf-line);box-shadow:0 12px 24px rgba(0,0,0,.14);padding:24px 32px 28px;z-index:1060}
.wf-mega .cols{display:grid;grid-template-columns:repeat(12,1fr);gap:24px}
.wf-mega .col{grid-column:span 3}
.wf-mega h4{margin:0 0 8px;font:700 11px/1.2 Helvetica,Arial,sans-serif;letter-spacing:.08em;text-transform:uppercase;color:var(--wf-mute);padding-bottom:8px;border-bottom:1px solid var(--wf-fill2)}
.wf-mega a,.wf-fly a,.wf-sheet a{display:flex;align-items:center;min-height:36px;padding:0 8px;margin:0 -8px;color:var(--wf-ink);text-decoration:none}
.wf-mega a.cur,.wf-fly a.cur,.wf-sheet a.cur{font-weight:700;box-shadow:inset 3px 0 0 var(--wf-mark);padding-left:12px}
.wf-mega .feat{grid-column:span 3;border-left:1px solid var(--wf-fill2);padding-left:24px}
.wf-mega .feat .box{height:96px;background:repeating-linear-gradient(135deg,#fff 0 4px,var(--wf-fill2) 4px 8px);border:1px solid var(--wf-line);margin-bottom:10px}
.wf-mega .foot{margin-top:20px;padding-top:12px;border-top:1px solid var(--wf-fill2);display:flex;gap:24px;color:var(--wf-mute);font-size:13px}
.wf-fly{position:absolute;top:100%;min-width:240px;background:#fff;border:1px solid var(--wf-line);box-shadow:0 8px 16px rgba(0,0,0,.14);padding:8px 16px;z-index:1060}
.wf-scrim{position:absolute;left:0;right:0;top:100%;height:900px;background:rgba(0,0,0,.28);z-index:1055;pointer-events:none}
.wf-tag{background:#1F1F1F;color:#fff;font:700 11px/1 Helvetica,Arial,sans-serif;letter-spacing:.08em;padding:11px 16px}
.wf-notes{background:#FFF3B0;color:#1F1F1F;font:12px/1.4 Helvetica,Arial,sans-serif;padding:7px 16px;border-bottom:1px solid #C9A800;display:flex;gap:28px}
.wf-notes span{flex:1}
.wf-tabs{display:flex;gap:0;padding:0 24px;background:transparent;border-bottom:1px solid var(--wf-line);margin:0 0 8px;font:14px/1.3 Helvetica,Arial,sans-serif}
.wf-tabs span{padding:12px 16px;color:var(--wf-mute)}.wf-tabs span.cur{color:var(--wf-ink);font-weight:700;box-shadow:inset 0 -3px 0 var(--wf-mark)}
.wf-crumb{padding:12px 32px 0;color:var(--wf-mute);font-size:13px}.wf-crumb b{color:var(--wf-ink);font-weight:400}
/* side-nav foil */
.wf-side{display:grid;grid-template-columns:248px 1fr;font:14px/1.3 Helvetica,Arial,sans-serif}
.wf-sidecol{background:var(--wf-fill);border-right:1px dashed var(--wf-line);padding:12px 0;min-height:560px}
.wf-sidecol h5{margin:12px 16px 4px;font:700 11px/1.2 Helvetica,Arial,sans-serif;letter-spacing:.08em;text-transform:uppercase;color:var(--wf-mute)}
.wf-sidecol a{display:flex;align-items:center;min-height:40px;padding:0 16px;color:var(--wf-ink);text-decoration:none;font-size:14px}
.wf-sidecol a.cur{font-weight:700;box-shadow:inset 3px 0 0 var(--wf-mark)}
.wf-sidecol a.sub{padding-left:32px;color:var(--wf-mute);min-height:34px}
/* phone sheet */
.wf-sheet{position:absolute;left:0;top:100%;width:296px;background:#fff;border-right:1px solid var(--wf-line);box-shadow:8px 0 24px rgba(0,0,0,.18);z-index:1060;padding:8px 16px 24px;min-height:760px}
.wf-sheet .grp{border-bottom:1px solid var(--wf-fill2)}
.wf-sheet .grp>a{min-height:48px;font-weight:400;justify-content:space-between}
.wf-sheet .grp.open>a{font-weight:700}
.wf-sheet .grp h4{margin:8px 0 2px 8px;font:700 11px/1.2 Helvetica,Arial,sans-serif;letter-spacing:.08em;text-transform:uppercase;color:var(--wf-mute)}
.wf-sheet .grp .kids{padding:0 0 8px 8px}.wf-sheet .grp .kids a{min-height:40px;color:var(--wf-mute)}
.wf-burger{width:44px;height:44px;border:1px dashed var(--wf-line);display:flex;align-items:center;justify-content:center;font-size:10px;color:var(--wf-mute);background:#fff}
"""

BUILD=r"""([opt,IA,css])=>{
  const $=(t,c,h)=>{const e=document.createElement(t);if(c)e.className=c;if(h!=null)e.innerHTML=h;return e};
  const st=$('style','',css); document.head.appendChild(st);
  const old=document.querySelector('.cn-navigations'); old.classList.add('wf-hide');
  const wf=$('div','wf'); old.parentNode.insertBefore(wf,old);
  const strip=$('div','wf-tag',''); wf.appendChild(strip); const notesEl=$('div','wf-notes',''); wf.appendChild(notesEl);
  const tag=(t)=>{strip.innerHTML=t};
  const note=(t)=>{notesEl.appendChild($('span','',t))};
  const chev='<span class="wf-chev"></span>';
  const primaries=(cls,cur,openName,withChev)=>{const n=$('nav','wf-nav');
    IA.forEach(([p,kids])=>{const a=$('a','wf-item'+(p===cur?' cur':'')+(p===openName?' open':''),p+(withChev&&kids.length?chev:'')); n.appendChild(a)}); return n};
  const acts=()=>$('div','wf-acts','<span class="wf-btn">search</span><span class="wf-btn">alerts</span><span class="wf-btn">account</span>');
  const mega=(pname,curLeaf)=>{const [,groups]=IA.find(x=>x[0]===pname); const m=$('div','wf-mega'); const cols=$('div','cols');
    groups.forEach(([h,links])=>{const c=$('div','col'); if(h)c.appendChild($('h4','',h)); links.forEach(l=>c.appendChild($('a',l===curLeaf?'cur':'',l))); cols.appendChild(c)});
    const f=$('div','feat','<div class="box"></div><div style="font-size:13px;color:#6B6B6B">Optional: a featured task or a notice for this area (cut-off today 16:30, 2 approvals waiting)</div>'); cols.appendChild(f);
    m.appendChild(cols); m.appendChild($('div','foot','<span>All of '+pname+' &rarr;</span><span>Level 2 = the column heading &middot; Level 3 = the link &middot; up to 4 columns &middot; a column never exceeds 6 links (s272-D70)</span>')); return m};
  const fly=(pname,leftPx)=>{const [,groups]=IA.find(x=>x[0]===pname); const f=$('div','wf-fly'); f.style.left=leftPx+'px'; groups[0][1].forEach(l=>f.appendChild($('a','',l))); return f};
  const crumb=(parts)=>$('div','wf-crumb',parts.map((p,i)=>i<parts.length-1?p+' &nbsp;/&nbsp; ':'<b>'+p+'</b>').join(''));
  const tabs=(names,cur)=>{const t=$('div','wf-tabs'); names.forEach(n=>t.appendChild($('span',n===cur?'cur':'',n))); return t};
  const ph=document.querySelector('.dashboard-page-header');

  if(opt==='1'){ // flat row, level 2 as tabs in the page, no level 3
    const b=$('div','wf-band h64'); b.appendChild($('div','wf-logo','logo')); b.appendChild(primaries('', 'Payments', null, false)); b.appendChild(acts()); wf.appendChild(b);
    ph.querySelector('.ph-outer').appendChild(tabs(['Make a payment','Bulk files','Standing orders','Templates','Beneficiaries','Approvals','Limits','Payment status','Returns & recalls','Cut-off times'],'Approvals'));
    tag('OPTION 1 &middot; FLAT ROW, LEVEL 2 AS PAGE TABS &middot; WIREFRAME');
    note('9 destinations in one 64px row. Fits at 1440; the wireframe row needs 812px and overflows the space beside brand and actions at 1024 (measured; the canon nav sets wider type, so the real number sits higher).');
    note('Level 2 becomes a tab strip on every page of the area: 10 peers here, and it wraps or scrolls. Level 3 has nowhere to live.');
  }
  if(opt==='2a'){ // top nav + mega menu, open on Payments
    const b=$('div','wf-band h64'); b.appendChild($('div','wf-logo','logo')); b.appendChild(primaries('', 'Payments','Payments', true)); b.appendChild(acts()); wf.appendChild(b);
    wf.appendChild(mega('Payments','Approvals')); wf.appendChild($('div','wf-scrim'));
    tag('OPTION 2 &middot; TOP NAV + MEGA MENU (open on Payments) &middot; WIREFRAME');
    note('Row unchanged: the nine primaries. A chevron marks the ones that open.');
  }
  if(opt==='2b'){ // same shell, FX open as a plain flyout
    const b=$('div','wf-band h64'); b.appendChild($('div','wf-logo','logo')); b.appendChild(primaries('', 'Payments','FX', true)); b.appendChild(acts()); wf.appendChild(b);
    const fxEl=[...wf.querySelectorAll('.wf-item')].find(e=>e.textContent.trim()==='FX'); const r=fxEl.getBoundingClientRect(); const wr=wf.getBoundingClientRect();
    wf.appendChild(fly('FX',r.left-wr.left));
    tag('OPTION 2 &middot; THE SAME SHELL, FX OPEN &middot; 3 LINKS = A FLYOUT, NOT A MEGA MENU');
    note('Under the ceiling ratified at s272-D70 (6 links, one column) the destination opens a plain flyout. Over it, or grouped under headings, the mega menu.',r.left-wr.left+260,80,330);
  }
  if(opt==='3'){ // stacked: masthead + primaries band + section tier
    const b=$('div','wf-band h64'); b.appendChild($('div','wf-logo','logo')); const sp=$('div','',' '); sp.style.flex='1'; b.appendChild(sp); b.appendChild(acts()); wf.appendChild(b);
    const b2=$('div','wf-band h56'); b2.appendChild(primaries('', 'Payments',null,false)); wf.appendChild(b2);
    const b3=$('div','wf-band h48'); const n=$('nav','wf-nav'); ['Make a payment','Bulk files','Standing orders','Payment templates','Beneficiaries','Approvals','Limits','Payment status','Returns & recalls','Cut-off times'].forEach(l=>n.appendChild($('a','wf-item'+(l==='Approvals'?' cur':''),l))); b3.appendChild(n); wf.appendChild(b3);
    tag('OPTION 3 &middot; STACKED: PRIMARIES BAND + SECTION TIER &middot; WIREFRAME');
    note('168px of chrome before the page title (64 + 56 + 48). On a laptop that is the fold.');
    note('Level 2 always visible, scrolls sideways when long. Level 3 still needs tabs in the page.');
  }
  if(opt==='4'){ // the side-nav foil: what the current rule does at > 7
    const b=$('div','wf-band h64'); b.appendChild($('div','wf-logo','logo')); const sp=$('div','',' '); sp.style.flex='1'; b.appendChild(sp); b.appendChild(acts()); wf.appendChild(b);
    const root=document.querySelector('.dashboard-root')||document.body;
    const grid=$('div','wf-side wf'); const col=$('div','wf-sidecol');
    IA.forEach(([p,kids])=>{col.appendChild($('a',p==='Payments'?'cur':'',p)); if(p==='Payments'){kids.forEach(([h,links])=>{col.appendChild($('h5','',h)); links.forEach(l=>col.appendChild($('a','sub'+(l==='Approvals'?' cur':''),l)))})}});
    grid.appendChild(col); const main=$('div',''); 
    let n=wf.nextSibling; const moved=[]; while(n){const nx=n.nextSibling; if(n.nodeType===1&&!n.classList.contains('wf-hide')&&!n.classList.contains('dashboard-live')){moved.push(n)} n=nx}
    moved.forEach(e=>main.appendChild(e)); grid.appendChild(main); wf.parentNode.insertBefore(grid,wf.nextSibling);
    tag('FOIL &middot; WHAT THE RULE AS IT STANDS DOES AT 9 DESTINATIONS: THE SIDE NAV');
    note('The current when-rule (destinations &lt;= 7 AND nav.levels &lt;= 2) hands this page to the side-nav shell. 248px leaves the bento 1128px; all three levels sit in one column.');
  }
  if(opt==='phone'){ // recommendation collapsed: burger, sheet with accordion
    const b=$('div','wf-band h64'); b.style.padding='0 16px'; b.style.gap='8px'; b.appendChild($('span','wf-burger','menu')); b.appendChild($('div','wf-logo','logo')); b.appendChild($('div','','&nbsp;')); const a=$('div','wf-acts','<span class="wf-btn">search</span><span class="wf-btn">acct</span>'); a.style.marginLeft='auto'; b.appendChild(a); wf.appendChild(b);
    const sh=$('div','wf-sheet');
    IA.forEach(([p,kids])=>{const g=$('div','grp'+(p==='Payments'?' open':'')); g.appendChild($('a','',p+(kids.length?chev:''))); if(p==='Payments'){const k=$('div','kids'); kids.forEach(([h,links])=>{if(h)k.appendChild($('h4','',h)); links.forEach(l=>k.appendChild($('a',l==='Approvals'?'cur':'',l)))}); g.appendChild(k)} sh.appendChild(g)});
    wf.appendChild(sh); wf.appendChild($('div','wf-scrim'));
    tag('OPTION 2 BELOW 600px &middot; THE MEGA MENU BECOMES AN ACCORDION IN THE SHEET');
    note('Same map as the row: the sheet holds the nine primaries; one with children opens in place and keeps its group headings. One map of the building, two shapes.');
  }
  const chrome=[...wf.querySelectorAll('.wf-band')].reduce((a,e)=>a+e.getBoundingClientRect().height,0); const scr=wf.querySelector('.wf-scrim'); const sr=scr?scr.getBoundingClientRect():null; return {chrome, items: wf.querySelectorAll('.wf-item').length, strip: strip.getBoundingClientRect().height+notesEl.getBoundingClientRect().height, scrim: sr?[sr.top,sr.height]:null};
}"""

def launch(p): return p.chromium.launch(executable_path=os.environ["RENDER_SHELL"])
facts={"sha":sha_full,"demo":DEMO,"canon":"git show %s:knowledge/canon/canon.css"%SHA,"shots":{}}
with sync_playwright() as p:
    b=launch(p)
    pg=b.new_page(viewport={"width":1440,"height":900},device_scale_factor=1)
    for opt,h in (("1",620),("2a",700),("2b",620),("3",680),("4",680)):
        pg.goto(URL); pg.wait_for_timeout(500)
        f=pg.evaluate(BUILD,[opt,IA,CSS]); pg.wait_for_timeout(300)
        pg.screenshot(path=f"{OUT}/F1-opt{opt}.png",clip={"x":0,"y":0,"width":1440,"height":h})
        facts["shots"][f"opt{opt}"]={"chrome_px":f["chrome"],"row_items":f["items"],"viewport":1440}
        print(opt,f)
    # row-fit probe for option 1/2: at which width does the nine-item row overflow the space beside brand+actions?
    pg.goto(URL); pg.wait_for_timeout(400); pg.evaluate(BUILD,["2a",IA,CSS]); pg.wait_for_timeout(200)
    fit={}
    for w in (1440,1280,1180,1120,1024):
        pg.set_viewport_size({"width":w,"height":900}); pg.wait_for_timeout(150)
        fit[w]=pg.evaluate("()=>{const n=document.querySelector('.wf-nav');return {need:n.scrollWidth,have:n.clientWidth}}")
    facts["row_fit"]=fit; print("row fit",fit)
    pg.close()
    pg=b.new_page(viewport={"width":390,"height":900},device_scale_factor=2)
    pg.goto(URL); pg.wait_for_timeout(500); f=pg.evaluate(BUILD,["phone",IA,CSS]); pg.wait_for_timeout(300)
    pg.screenshot(path=f"{OUT}/F1-phone.png",clip={"x":0,"y":0,"width":390,"height":900})
    facts["shots"]["phone"]={"chrome_px":f["chrome"],"viewport":390}
    MAP="""<!doctype html><html><head><meta charset="utf-8"><style>
body{margin:0;background:#fff;font:14px/1.35 Helvetica,Arial,sans-serif;color:#1F1F1F}
.m{width:1440px;padding:24px 32px 28px;box-sizing:border-box}
h1{font:700 11px/1 Helvetica,Arial,sans-serif;letter-spacing:.08em;text-transform:uppercase;margin:0 0 20px;background:#1F1F1F;color:#fff;display:inline-block;padding:11px 16px}
.row{display:grid;grid-template-columns:52px 1fr 1fr;gap:0 24px;align-items:stretch;margin-bottom:12px}
.n{background:#1F1F1F;color:#fff;font-weight:700;display:flex;align-items:center;justify-content:center;font-size:18px}
.q{border:1px solid #9A9A9A;padding:14px 16px;background:#F2F2F2}
.q b{display:block;margin-bottom:4px}
.a{display:grid;gap:8px}
.a div{border:1px dashed #9A9A9A;padding:10px 14px;background:#fff}
.a div b{font-weight:700}
.a div.def{border:2px solid #1F1F1F;background:#FFF3B0}
.foot{margin-top:18px;color:#6B6B6B;font-size:13px;border-top:1px solid #E4E4E4;padding-top:10px}
</style></head><body><div class="m"><h1>What hands over to what &middot; the order the frame is chosen in &middot; recommendation, not a ruling</h1>
<div class="row"><div class="n">1</div><div class="q"><b>Is there anywhere else to go?</b>No primary navigation, one exit, one job: signing in, a passcode, a wizard.</div><div class="a"><div><b>No &rarr; the focused shell.</b> Defined by what it removes. Unchanged.</div></div></div>
<div class="row"><div class="n">2</div><div class="q"><b>What shape is the job?</b>A list the person works through one record at a time; or two things side by side with neither subordinate.</div><div class="a"><div><b>List and detail &rarr; the multi-column shell.</b> Unchanged.</div><div><b>Two peers at once &rarr; the split shell.</b> Unchanged.</div></div></div>
<div class="row"><div class="n">3</div><div class="q"><b>Is it a site, not an app?</b>Marketing or servicing pages with more destinations than a masthead should carry.</div><div class="a"><div><b>Site &rarr; the doormat shell.</b> Four in the masthead, the rest in the mega-footer. Unchanged.</div></div></div>
<div class="row"><div class="n">4</div><div class="q"><b>Otherwise: the top nav. Whatever the count, whatever the depth.</b>The primaries sit in one 64px row. The count of destinations and levels no longer chooses the frame; it chooses what a destination opens.</div><div class="a"><div class="def"><b>Up to 6 links, no groups &rarr; a flyout</b> (one column; the ceiling ratified at s272-D70).</div><div class="def"><b>Over 6, or grouped under headings &rarr; the mega menu</b> (up to 4 columns of 12; level 2 = the heading, level 3 = the link; a column never exceeds 6).</div><div class="def"><b>The current page&rsquo;s peer views &rarr; tabs in the page-header lock-up.</b> Never a third band of chrome.</div><div><b>Below 600px &rarr; the sheet,</b> the same map as an accordion.</div></div></div>
<div class="row"><div class="n">5</div><div class="q"><b>The one case the side nav keeps.</b>The second level must stay on screen while the person works: a back-office workbench where they hop between siblings many times a minute. A job test, never a count.</div><div class="a"><div><b>Workbench &rarr; the side-nav shell;</b> content cannot spare 248px &rarr; the nav rail.</div></div></div>
<div class="foot">The rule as it stands (destinations &le; 7 AND nav.levels &le; 2, side nav above that) is replaced at step 4: the count stops choosing the frame. Dave, 2026-09-28: &ldquo;the preference in general is a top nav, if there are multiple levels we use a mega menu.&rdquo;</div>
</div></body></html>"""
    open(f"{SH}/map.html","w").write(MAP)
    pg=b.new_page(viewport={"width":1440,"height":1200}); pg.goto(f"file://{SH}/map.html"); pg.wait_for_timeout(300)
    hh=pg.evaluate("()=>document.querySelector('.m').getBoundingClientRect().height")
    pg.screenshot(path=f"{OUT}/F1-handover-map.png",clip={"x":0,"y":0,"width":1440,"height":hh})
    facts["shots"]["map"]={"height":hh}
    b.close()
json.dump(facts,open(f"{OUT}/F1-facts.json","w"),indent=1)
print(json.dumps(facts,indent=1))
