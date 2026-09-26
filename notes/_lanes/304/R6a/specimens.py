"""R6a specimens: real renders of the repo's reference snippets, cropped to the part the decision
page needs. Nothing is redrawn: each PNG is a screenshot of knowledge/snippets/<Name>.reference.html
as it stands. Two shots carry a stated override (demo chrome hidden; the bento 'his sentence' leg
moves the grey from the page to the bento section) and say so on the page. Run from repo root at
Dave's seat after ensure_env + seat_env."""
import os, sys, json
from playwright.sync_api import sync_playwright
ROOT = os.getcwd(); SN = os.path.join(ROOT, 'knowledge/snippets')
OUT = os.path.join(ROOT, 'notes/_lanes/304/R6a/specimens')

FIND = r"""([start, mode, pad]) => {
  const all = [...document.querySelectorAll('body *')].filter(e => {
    const t = (e.textContent||'').replace(/\s+/g,' ').trim();
    if (!t.startsWith(start)) return false;
    return ![...e.children].some(c => (c.textContent||'').replace(/\s+/g,' ').trim().startsWith(start));
  });
  if (!all.length) return null;
  let el = all[0];
  let r = el.getBoundingClientRect();
  let x1=r.left,y1=r.top,x2=r.right,y2=r.bottom;
  if (mode !== 'self') {
    let n = el.nextElementSibling;
    while (n && !n.getBoundingClientRect().height) n = n.nextElementSibling;
    if (n) { const q = n.getBoundingClientRect(); if (mode==='next'){x1=q.left;y1=q.top;x2=q.right;y2=q.bottom;} else {x1=Math.min(x1,q.left);y1=Math.min(y1,q.top);x2=Math.max(x2,q.right);y2=Math.max(y2,q.bottom);} }
  }
  if (mode === 'parent') { const q = el.parentElement.getBoundingClientRect(); x1=q.left;y1=q.top;x2=q.right;y2=q.bottom; }
  return {x:Math.max(0,x1-pad)+scrollX, y:Math.max(0,y1-pad)+scrollY, width:(x2-x1)+2*pad, height:(y2-y1)+2*pad};
}"""
SEL = r"""([sel, pad, idx]) => { const e = document.querySelectorAll(sel)[idx||0]; if(!e) return null; const r = e.getBoundingClientRect();
  return {x:Math.max(0,r.left-pad)+scrollX, y:Math.max(0,r.top-pad)+scrollY, width:r.width+2*pad, height:r.height+2*pad}; }"""

# name, snippet, viewport w, h, how, args, extra css, wait ms, action
SPECS = [
 ('kpi-states',   'Kpi-tile', 1000, 900, 'find', ['States — loading', 'both', 8], '', 600, None),
 ('kpi-default',  'Kpi-tile', 1280, 900, 'sel',  ['.kpi-tile', 6, 0], '', 600, None),
 ('button-row',   'Button',   1280, 900, 'clip', [28, 56, 628, 108], '', 400, None),
 ('button-bar',   'Button',   1280, 900, 'clip', [28, 537, 612, 116], '', 400, None),
 ('appshell',     'App-shell-top-nav', 1280, 900, 'find', ['Form: inline', 'next', 4], '', 500, None),
 ('legend',       'Legend',   1280, 900, 'sel', ['figure', 6, 0], '', 600, None),
 ('layout',       'Layout-utilities', 1280, 900, 'find', ['Twelve columns', 'both', 8], '', 400, None),
 ('footer',       'Footer',   1280, 900, 'find', ['Default — one row', 'both', 8], '', 400, None),
 ('chart-line',   'Chart-line', 1000, 700, 'clip', [30, 87, 610, 348], '', 3500, 'nofit'),
 ('candlestick',  'Chart-candlestick', 1000, 700, 'sel', ['figure', 6, 0], '', 2500, None),
 ('split-open',   'Split-button', 900, 700, 'clip', [30, 228, 209, 212], '', 500, None),
 ('split-closed', 'Split-button', 900, 700, 'clip', [0, 55, 640, 135], '', 500, None),
 ('dropdown',     'Dropdown', 900, 700, 'clip', [20, 30, 380, 120], '', 400, None),
 ('modal-open',   'Modals',   1000, 640, 'clip', [230, 190, 540, 260], '', 600, 'modal'),
 ('bento-ruled',  'Template-dashboard-bento', 1280, 760, 'view', [], '.demo-bar{display:none!important}', 1500, None),
 ('bento-his',    'Template-dashboard-bento', 1280, 760, 'view', [],
    '.demo-bar{display:none!important} body.tpl-bento-body{background:var(--page)!important} .tpl-header{background:var(--page)!important} main.tpl-page{background:var(--wall-ground)!important}', 1500, None),
 ('bento-ruled-top', 'Template-dashboard-bento', 1280, 760, 'clip', [0, 0, 1280, 470], '.demo-bar{display:none!important}', 1500, None),
 ('bento-his-top', 'Template-dashboard-bento', 1280, 760, 'clip', [0, 0, 1280, 470],
    '.demo-bar{display:none!important} body.tpl-bento-body{background:var(--page)!important} .tpl-header{background:var(--page)!important} main.tpl-page{background:var(--wall-ground)!important}', 1500, None),
]
only = set(sys.argv[1:])
rep = {}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ['RENDER_SHELL'])
    for name, sn, w, h, how, args, css, wait, act in SPECS:
        if only and name not in only: continue
        ctx = b.new_context(viewport={'width': w, 'height': h}, device_scale_factor=2)
        pg = ctx.new_page(); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.goto('file://' + os.path.join(SN, sn + '.reference.html'))
        if css: pg.add_style_tag(content=css)
        pg.wait_for_timeout(wait)
        if act == 'modal':
            pg.get_by_role('button', name='Make payment').first.click(); pg.wait_for_timeout(700)
        if act == 'nofit':
            pg.evaluate("document.querySelectorAll('figure.dv-fit-on').forEach(f=>f.classList.remove('dv-fit-on'))"); pg.wait_for_timeout(600)
        path = os.path.join(OUT, name + '.png')
        if how == 'view':
            pg.screenshot(path=path); clip = {'x':0,'y':0,'width':w,'height':h}
        else:
            if how == 'find': clip = pg.evaluate(FIND, args)
            elif how == 'sel': clip = pg.evaluate(SEL, args)
            else: clip = dict(zip(['x','y','width','height'], args))
            if not clip: rep[name] = 'NOT FOUND'; ctx.close(); continue
            clip['width'] = min(clip['width'], w - clip['x'])
            pg.screenshot(path=path, clip=clip, full_page=True)
        rep[name] = {k: round(v) for k, v in clip.items()}; rep[name]['errors'] = errs
        ctx.close()
    b.close()
print(json.dumps(rep))
