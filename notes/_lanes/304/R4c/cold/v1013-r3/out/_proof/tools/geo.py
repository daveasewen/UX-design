import os, sys, json
from playwright.sync_api import sync_playwright
W = os.path.expanduser('~/cold/v1013-r3/out')
name = sys.argv[1]; vw = int(sys.argv[2]) if len(sys.argv) > 2 else 1440; theme = sys.argv[3] if len(sys.argv) > 3 else 'light'
JS = r'''() => {
 const vw = document.documentElement.clientWidth, out = {vw, over: []};
 for (const el of document.querySelectorAll('body *')) { const r = el.getBoundingClientRect(); if (r.width && r.right > vw + 0.5 && getComputedStyle(el).position !== 'fixed') { let p = el.parentElement, clipped = false; while (p) { const o = getComputedStyle(p).overflowX; if (o === 'auto' || o === 'hidden' || o === 'scroll') { const pr = p.getBoundingClientRect(); if (pr.right <= vw + 0.5) { clipped = true; break; } } p = p.parentElement; } if (!clipped) out.over.push(el.tagName + '.' + (el.className.baseVal !== undefined ? el.className.baseVal : el.className).toString().slice(0, 40) + ' r=' + Math.round(r.right)); } }
 out.over = out.over.slice(0, 12);
 const q = (s) => document.querySelector(s), box = (s) => { const e = q(s); if (!e) return null; const r = e.getBoundingClientRect(), c = getComputedStyle(e); return {x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height), pad: c.padding, bg: c.backgroundColor}; };
 out.masthead = box('.sh-masthead'); out.nav = box('.sh-nav'); out.header = box('.tpl-header'); out.ftb = box('.cn-filter-toolbar-bar'); out.wall = box('.wall-ground'); out.wallInner = box('.tpl-wall');
 out.firstTile = box('.kpi-tile') || box('.stat-card'); out.section = box('.page-section'); out.grid = box('.dg'); out.foot = box('.sh-foot');
 const tiles = [...document.querySelectorAll('.c-bento__tile.kpi-tile, .c-bento__tile.stat-card')].map(t => { const r = t.getBoundingClientRect(); return [Math.round(r.x), Math.round(r.y), Math.round(r.width), Math.round(r.height), getComputedStyle(t).backgroundColor]; });
 out.tiles = tiles; out.bodyBg = getComputedStyle(document.body).backgroundColor; out.docH = document.documentElement.scrollHeight;
 return out; }'''
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ['RENDER_SHELL'])
    ctx = b.new_context(viewport={'width': vw, 'height': 900})
    ctx.add_init_script("localStorage.setItem('apollo-ceo-proto-v1', JSON.stringify({theme:'%s'}))" % theme)
    pg = ctx.new_page(); pg.goto('file://' + W + '/' + name + '.html'); pg.wait_for_timeout(600)
    print(json.dumps(pg.evaluate(JS), indent=0)[:3500])
    b.close()
