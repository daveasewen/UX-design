# #297 lane B - the rail vs content: bounding-box collisions per slide, plus optional renders.
# Usage: python3 rail_check.py <deck.html> <out.json> WxH [--shots DIR] [--dsf N]
# Rail elements: the line (ol::before, derived from the ol box), every visible circle (.cr-c), dot (.cr-d)
# and title (.cr-t, its own box, which carries the drawn dash when present). Content elements: every text
# line box in the slide, every img/canvas/svg/video box, every element that paints a border or a background
# (or carries ::before/::after content), at effective opacity > .05, inside the viewport, smaller than 90%
# of the viewport. A collision = the two boxes overlap by > 0 px in both axes. Clearance = the smallest gap.
import os, sys, json, time
from playwright.sync_api import sync_playwright
deck = os.path.abspath(sys.argv[1]); out = os.path.abspath(sys.argv[2])
W, H = (int(x) for x in sys.argv[3].split('x'))
shots = sys.argv[sys.argv.index('--shots') + 1] if '--shots' in sys.argv else None
dsf = float(sys.argv[sys.argv.index('--dsf') + 1]) if '--dsf' in sys.argv else 1
BLOCK = ("window.addEventListener('pointermove', function(e){ e.stopImmediatePropagation(); }, {capture:true});"
         "window.addEventListener('mousemove', function(e){ e.stopImmediatePropagation(); }, {capture:true});")
JS = r"""(sid) => {
 const s = document.getElementById(sid), VW = innerWidth, VH = innerHeight;
 const R = r => ({x:+r.left.toFixed(1), y:+r.top.toFixed(1), r:+r.right.toFixed(1), b:+r.bottom.toFixed(1)});
 const nav = document.getElementById('chrail');
 const rail = []; const hidden = !nav || nav.classList.contains('is-hidden');
 if (nav && !hidden) {
   const ol = nav.querySelector('ol'); const o = ol.getBoundingClientRect();
   const bl = parseFloat(getComputedStyle(ol, '::before').left) || 21.5;
   rail.push({k:'line', x:o.left + bl, y:0, r:o.left + bl + 1, b:VH});
   nav.querySelectorAll('.cr-c, .cr-d, .cr-t').forEach(e => { if (!e.getClientRects().length) return;
     const q = e.getBoundingClientRect(); if (q.width < .5 || q.height < .5 || q.bottom < 0 || q.top > VH) return;
     rail.push(Object.assign({k: e.className + (e.className === 'cr-t' ? ':' + e.textContent : '')}, R(q))); });
 }
 const eop = e => { let o = 1; for (let n = e; n && n !== document.body; n = n.parentElement) o *= +getComputedStyle(n).opacity; return o; };
 const content = [];
 const add = (kind, e, q, txt) => { if (q.width < .5 || q.height < .5) return; if (q.right <= 0 || q.left >= VW || q.bottom <= 0 || q.top >= VH) return;
   if (q.width * q.height > .9 * VW * VH) return;
   content.push({k: kind, el: e.tagName.toLowerCase() + (e.id ? '#' + e.id : '') + (typeof e.className === 'string' && e.className ? '.' + e.className.trim().split(/\s+/).join('.') : ''), t: (txt || '').slice(0, 40), ...R(q)}); };
 const vis = e => { const c = getComputedStyle(e); return c.visibility !== 'hidden' && c.display !== 'none' && eop(e) > .05; };
 // text line boxes
 const tw = document.createTreeWalker(s, NodeFilter.SHOW_TEXT); let n;
 while ((n = tw.nextNode())) { if (!n.textContent.trim()) continue; const pe = n.parentElement; if (!pe || !pe.getClientRects().length || !vis(pe)) continue;
   const r = document.createRange(); r.selectNodeContents(n); for (const q of r.getClientRects()) add('text', pe, q, n.textContent.trim()); }
 // painted boxes
 s.querySelectorAll('*').forEach(e => { if (!e.getClientRects().length || !vis(e)) return; const c = getComputedStyle(e); const tag = e.tagName;
   let paint = /^(IMG|CANVAS|SVG|VIDEO|PICTURE)$/i.test(tag) || tag === 'svg';
   if (!paint) for (const sd of ['top','right','bottom','left']) { if (parseFloat(c['border-' + sd + '-width']) > 0 && c['border-' + sd + '-style'] !== 'none' && !/rgba\(0, 0, 0, 0\)|transparent/.test(c['border-' + sd + '-color'])) paint = true; }
   if (!paint && !/rgba\(0, 0, 0, 0\)|transparent/.test(c.backgroundColor)) paint = true;
   if (!paint && c.backgroundImage !== 'none') paint = true;
   if (!paint) for (const p of ['::before','::after']) { const pc = getComputedStyle(e, p); if (pc.content && pc.content !== 'none' && pc.content !== 'normal' && pc.display !== 'none') paint = true; }
   if (paint && e.closest('svg') && tag !== 'svg') return;
   if (paint) add('box', e, e.getBoundingClientRect(), (e.innerText || '').trim()); });
 const hits = []; let clear = 1e9, near = null;
 for (const a of rail) for (const c of content) {
   const ox = Math.min(a.r, c.r) - Math.max(a.x, c.x), oy = Math.min(a.b, c.b) - Math.max(a.y, c.y);
   if (ox > 0 && oy > 0) hits.push({rail: a.k, el: c.el, t: c.t, k: c.k, ox:+ox.toFixed(1), oy:+oy.toFixed(1)});
   else { const gx = Math.max(a.x - c.r, c.x - a.r), gy = Math.max(a.y - c.b, c.y - a.b); const g = Math.max(gx, gy); if (g < clear) { clear = g; near = {rail:a.k, el:c.el, t:c.t, gap:+g.toFixed(1)}; } }
 }
 const railRight = rail.filter(a => a.k !== 'line').reduce((m, a) => Math.max(m, a.r), 0);
 const contentLeft = content.reduce((m, c) => Math.min(m, c.x), 1e9);
 return {id: sid, railHidden: hidden, rail, nRail: rail.length, nContent: content.length, hits, near, railRight:+railRight.toFixed(1), contentLeft:+contentLeft.toFixed(1)};
}"""
res = {'viewport': [W, H], 'deck': deck, 'slides': []}; errs = []
t0 = time.time()
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ['RENDER_SHELL'], args=['--no-sandbox'])
    pg = b.new_page(viewport={'width': W, 'height': H}, device_scale_factor=dsf)
    pg.add_init_script(BLOCK)
    pg.on('pageerror', lambda x: errs.append('pageerror: %s' % x))
    pg.goto('file://' + deck, wait_until='load'); time.sleep(3.0)
    order = pg.evaluate("() => [...document.querySelectorAll('section.slide')].map(s => s.id)")
    if shots: os.makedirs(shots, exist_ok=True)
    for i, sid in enumerate(order):
        pg.evaluate('n => window.deckGo(n)', i); time.sleep(1.8)
        pg.evaluate('() => { window.brSet && window.brSet(0,0); window.shlSet && window.shlSet(0,0); if (window.calSetTime){ window.calSetTime(0); window.calStill(); } if (window.kgPause){ window.kgPause(true); window.kgStill(); } }'); time.sleep(0.3)
        r = pg.evaluate(JS, sid); r['n'] = i + 1; res['slides'].append(r)
        if shots: pg.screenshot(path=os.path.join(shots, '%02d-%s.png' % (i + 1, sid)))
    b.close()
res['errors'] = errs; res['secs'] = round(time.time() - t0, 1)
json.dump(res, open(out, 'w'), indent=1)
tot = 0
for r in res['slides']:
    k = len(r['hits']); tot += 1 if k else 0
    print('%02d %-7s %s hits=%d railR=%s contentL=%s near=%s %s' % (r['n'], r['id'], 'HIDDEN' if r['railHidden'] else 'rail  ', k, r['railRight'], r['contentLeft'], r['near'] and r['near']['gap'], (r['hits'][:2] if k else '')))
print('%dx%d slides with a collision: %d of %d (rail visible on %d); errors %d; secs %s' % (W, H, tot, len(res['slides']), sum(1 for r in res['slides'] if not r['railHidden']), len(errs), res['secs']))
