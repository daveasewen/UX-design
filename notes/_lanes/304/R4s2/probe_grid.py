"""probe_grid.py — are the data-grid G7 collisions real ink? For one page: locate #dgHint and the grid,
report each grid scroll box (overflow, client/scroll height), where the colliding row text sits relative to
it, and what elementFromPoint returns at the overlap. Also screenshots the grid region."""
import sys, json, os
from playwright.sync_api import sync_playwright
page_path, out_png = sys.argv[1], sys.argv[2]
JS = r"""() => {
 const hint = document.getElementById('dgHint'); if(!hint) return {nohint:true};
 const grid = hint.closest('[class*=cn-data-grid]') || hint.parentElement;
 const hr = hint.getBoundingClientRect();
 const boxes = [];
 for (let e = hint; e; e = e.parentElement) { const cs = getComputedStyle(e);
   if (/(auto|scroll|hidden|clip)/.test(cs.overflowY)) boxes.push({el: e.tagName+'.'+[...e.classList].slice(0,3).join('.'), ov: cs.overflowY, ch: e.clientHeight, sh: e.scrollHeight, top: e.getBoundingClientRect().top}); }
 // rows
 const rows = [...grid.querySelectorAll('tbody tr, [role=row]')];
 const scroller = rows.length ? (()=>{ for (let e=rows[0].parentElement; e; e=e.parentElement){const cs=getComputedStyle(e); if(/(auto|scroll)/.test(cs.overflowY)||/(auto|scroll)/.test(cs.overflow)) return e;} return null;})() : null;
 const sr = scroller ? scroller.getBoundingClientRect() : null;
 const lastRow = rows.length ? rows[rows.length-1].getBoundingClientRect() : null;
 const hit = document.elementFromPoint(hr.left+20, hr.top+hr.height/2);
 return {hint:{top:hr.top,bottom:hr.bottom,left:hr.left,w:hr.width}, hintAncestorsOverflow: boxes.slice(0,6), nrows: rows.length,
   rowScroller: scroller ? {el: scroller.tagName+'.'+[...scroller.classList].join('.'), top: sr.top, bottom: sr.bottom, ch: scroller.clientHeight, sh: scroller.scrollHeight, ov: getComputedStyle(scroller).overflowY} : null,
   lastRow: lastRow ? {top:lastRow.top,bottom:lastRow.bottom} : null,
   hitAtHint: hit ? hit.tagName+'#'+hit.id+'.'+[...hit.classList].join('.') : null,
   gridBox: (()=>{const r=grid.getBoundingClientRect(); return {top:r.top,bottom:r.bottom}})()};
}"""
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ.get("RENDER_SHELL"))
    pg = b.new_page(viewport={"width":1440,"height":900}); pg.goto("file://"+os.path.abspath(page_path)); pg.wait_for_timeout(1200)
    r = pg.evaluate(JS); print(json.dumps(r, indent=1))
    h = pg.query_selector('#dgHint')
    if h:
        g = pg.evaluate_handle("() => document.getElementById('dgHint').closest('[class*=cn-data-grid]') || document.getElementById('dgHint').parentElement")
        g.as_element().scroll_into_view_if_needed(); pg.wait_for_timeout(300)
        g.as_element().screenshot(path=out_png)
    b.close()
