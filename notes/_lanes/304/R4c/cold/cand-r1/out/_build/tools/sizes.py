"""Rule 3a/8 check: each part's rendered size on this page vs the same part on its own reference page."""
import os, json
from playwright.sync_api import sync_playwright
W=os.path.expanduser('~/cold/cand-r1'); URL='file://'+W+'/out/index.html'; SN='file://'+W+'/pack/knowledge/snippets/'
PARTS=[ # name, snippet, selector in snippet, page view, selector on page, props
 ('KPI tile', 'Kpi-tile', '.kpi-tile.as-link', 'overview', '#view-overview .kpi-tile', ['padding','fontSize@.kpi-val','h@.kpi-spark']),
 ('Segmented control (md)', 'Segmented-control', '.seg.md', 'overview', '.sh-actions .seg', ['h','padding']),
 ('Dropdown trigger (boxed)', 'Dropdown', '.dd.boxed .trigger', 'payments', '#t-py-r-payments .dd .trigger', ['h','padding']),
 ('Pagination page link', 'Pagination', '.pg a', 'payments', '#t-py-r-payments .pg a', ['h','w']),
 ('Pagination control', 'Pagination', '.pg .ctrl', 'payments', '#t-py-r-payments .pg .ctrl', ['h','w']),
 ('Table body row', 'Table', 'tbody tr', 'payments', '#t-py-r-payments tbody tr', ['h']),
 ('Table cell padding', 'Table', 'tbody td', 'payments', '#t-py-r-payments tbody td', ['padding']),
 ('Status indicator — filled cell', 'Status-indicator', '.statustable .cell', 'payments', '#t-py-r-payments .cell', ['h','padding','fontSize']),
 ('Status indicator — tint chip', 'Status-indicator', '.chips .chip', 'overview', '#t-ov-d-approvals .chip', ['h','padding','fontSize']),
 ('Sidebar link', 'App-shell-side-nav', '.sn-link', 'overview', '.sh-body > .sn .sn-link', ['h']),
 ('App bar', 'App-shell-side-nav', '.sh-appbar', 'overview', '.sh-appbar', ['h']),
 ('Card (action)', 'Cards', '.card.action', 'overview', '#t-ov-d-approvals .card', ['padding']),
 ('Card action button', 'Cards', '.card.action .qbtn', 'overview', '#t-ov-d-approvals .qbtn', ['h']),
 ('Limits meter track', 'Limits-meter', '.pb-track', 'risk', '#t-rk-m-1 .pb-track', ['h']),
 ('Page-header title', 'Page-header-lockup', '.ph-title', 'overview', '.ph-title', ['fontSize','lineHeight']),
 ('Page-header button', 'Page-header-lockup', '.ph-actions .btn.primary', 'overview', '.ph-actions .btn.primary', ['h','padding']),
 ('Chart title', 'Chart-line', '.dv-title', 'overview', '#t-ov-c-trend .dv-title', ['fontSize','lineHeight']),
 ('Filter bar search', 'Filter-toolbar-bar', '#ftbQ', 'overview', '#ftbQ', ['h']),
 ('Data-grid header cell', 'Data-grid', '#tbl thead tr.cols th', 'accounts', '#tbl thead tr.cols th', ['h']),
]
JS=r"""([sel, props])=>{const e=document.querySelector(sel); if(!e) return null; const cs=getComputedStyle(e), b=e.getBoundingClientRect(); const o={};
 props.forEach(p=>{ if(p==='h') o.h=Math.round(b.height*10)/10; else if(p==='w') o.w=Math.round(b.width*10)/10;
   else if(p.includes('@')){ const [k,s]=p.split('@'); const c=e.querySelector(s); if(!c){o[p]=null;return;} o[p]= k==='h'? Math.round(c.getBoundingClientRect().height*10)/10 : getComputedStyle(c)[k]; }
   else o[p]=cs[p]; }); return o; }"""
out=[]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=os.environ['RENDER_SHELL'])
    pg=b.new_page(viewport={'width':1440,'height':900}); ref=b.new_page(viewport={'width':1440,'height':900})
    for name, sn, ssel, view, psel, props in PARTS:
        ref.goto(SN+sn+'.reference.html'); ref.wait_for_timeout(400)
        pg.goto(URL+'?view='+view); pg.wait_for_timeout(700)
        a=ref.evaluate(JS,[ssel,props]); c=pg.evaluate(JS,[psel,props])
        same = a==c
        out.append({'part':name,'reference':a,'page':c,'match':same})
    b.close()
print(json.dumps(out,indent=1))
