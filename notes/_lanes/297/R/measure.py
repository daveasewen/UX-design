# #297 lane R - measure the plain deck: type roles, edges, line breaks, rail overlap, diagram grammar.
# Usage: python3 measure.py <deck.html> <out.json> [WxH,WxH,...] [--shots dir ids]
import os, sys, json, time
from playwright.sync_api import sync_playwright
deck = os.path.abspath(sys.argv[1]); out = os.path.abspath(sys.argv[2])
vps = [tuple(int(x) for x in v.split('x')) for v in (sys.argv[3] if len(sys.argv) > 3 else '1440x900').split(',')]
shots = None
if '--shots' in sys.argv:
    i = sys.argv.index('--shots'); shots = (sys.argv[i+1], sys.argv[i+2].split(','))
BLOCK = ("window.addEventListener('pointermove', function(e){ e.stopImmediatePropagation(); }, {capture:true});"
         "window.addEventListener('mousemove', function(e){ e.stopImmediatePropagation(); }, {capture:true});")
JS = r"""(sid) => {
 const s = document.getElementById(sid);
 const cs = (e, pse) => getComputedStyle(e, pse || null);
 const R = r => ({x:+r.x.toFixed(1), y:+r.y.toFixed(1), w:+r.width.toFixed(1), h:+r.height.toFixed(1)});
 function lines(e){ // group words by line top
   const out = []; const tw = document.createTreeWalker(e, NodeFilter.SHOW_TEXT); let n;
   const words = [];
   while ((n = tw.nextNode())) { const t = n.textContent; const re = /\S+/g; let m;
     while ((m = re.exec(t))) { const r = document.createRange(); r.setStart(n, m.index); r.setEnd(n, m.index + m[0].length);
       const rr = r.getClientRects()[0]; if (rr) words.push({w:m[0], top:Math.round(rr.top), l:rr.left, r:rr.right}); } }
   words.forEach(w => { let L = out.find(o => Math.abs(o.top - w.top) < 6); if (!L) { L = {top:w.top, words:[], l:w.l, r:w.r}; out.push(L); } L.words.push(w.w); L.l = Math.min(L.l, w.l); L.r = Math.max(L.r, w.r); });
   out.sort((a,b)=>a.top-b.top); return out.map(o => ({top:o.top, text:o.words.join(' '), l:+o.l.toFixed(1), r:+o.r.toFixed(1)}));
 }
 function sty(e){ const c = cs(e); return {fs:c.fontSize, fw:c.fontWeight, lh:c.lineHeight, ls:c.letterSpacing, tt:c.textTransform, col:c.color, ff:c.fontFamily.split(',')[0], fst:c.fontStyle}; }
 const roles = {label:'.label', h1:'h1', h2:'h2', lead:'.lead', body:'.body', foot:'.foot', pagenum:'.pagenum', h3:'h3', ix:'.ix',
   sh:'.sh', sb:'.sb', st:'.st', wbh:'.wb-h span', gl:'.gl', li:'li', done:'.done', tdesc:'.tile .d', src:'.src', badge:'.badge', idx:'.idx',
   hubh:'.hubh', strap:'.strap', ask:'.ask', draft:'.draft', close:'.close-line', sub:'.sub', chn:'.chapters .n', chb:'.chapters b', chem:'.chapters em', regen:'.rl', p:'.c5 p:last-child, .grid5 p:not(.ix)'};
 const res = {id:sid, cls:s.className, roles:{}};
 for (const [k, q] of Object.entries(roles)) {
   const els = [...s.querySelectorAll(q)].filter(e => e.getClientRects().length);
   if (!els.length) continue;
   res.roles[k] = els.slice(0, 14).map(e => Object.assign(sty(e), {rect:R(e.getBoundingClientRect()), lines: ['h1','h2','lead','ask','close','sub','h3','body','foot'].includes(k) ? lines(e) : undefined, txt: e.innerText.slice(0,80)}));
 }
 // rail
 const cur = document.querySelector('#chrail .cr-ch.is-cur .cr-t'), circ = document.querySelector('#chrail .cr-ch.is-cur .cr-c');
 const nav = document.getElementById('chrail');
 res.rail = {hidden: nav.classList.contains('is-hidden'), title: cur ? Object.assign(sty(cur), {rect:R(cur.getBoundingClientRect()), txt:cur.innerText}) : null, circle: circ ? R(circ.getBoundingClientRect()) : null};
 // overlaps with rail title (text line boxes)
 res.overlaps = [];
 if (cur && !res.rail.hidden) {
   const rr = cur.getBoundingClientRect(); const pad = 8;
   const tw = document.createTreeWalker(s, NodeFilter.SHOW_TEXT); let n;
   while ((n = tw.nextNode())) { if (!n.textContent.trim()) continue; const pe = n.parentElement; if (!pe.getClientRects().length) continue;
     const op = +cs(pe).opacity; const r = document.createRange(); r.selectNodeContents(n);
     for (const q of r.getClientRects()) { if (q.width < 1) continue;
       const gapX = Math.max(rr.left - q.right, q.left - rr.right), gapY = Math.max(rr.top - q.bottom, q.top - rr.bottom);
       if (gapX < pad && gapY < pad) res.overlaps.push({el: pe.tagName.toLowerCase() + (pe.className ? '.' + String(pe.className).split(' ')[0] : ''), txt: n.textContent.trim().slice(0,40), gapX:+gapX.toFixed(1), gapY:+gapY.toFixed(1), line:R(q)}); } }
 }
 // left edges and extents of content
 const inner = s.querySelector('.inner'); res.inner = inner ? R(inner.getBoundingClientRect()) : null;
 const lab = s.querySelector('.label'); res.labelRect = lab ? R(lab.getBoundingClientRect()) : null;
 res.pagenumRect = s.querySelector('.pagenum') ? R(s.querySelector('.pagenum').getBoundingClientRect()) : null;
 // diagram grammar
 const g = {};
 const pick = (q, props, pse) => { const e = s.querySelector(q); if (!e) return null; const c = cs(e, pse); const o = {}; props.forEach(p => o[p] = c.getPropertyValue(p)); if (!pse) o.rect = R(e.getBoundingClientRect()); return o; };
 const B = ['border-top-width','border-top-style','border-top-color','border-left-width','border-left-color','border-radius','background-color','padding-top','padding-left'];
 const T = ['font-size','font-weight','letter-spacing','text-transform','line-height','color','font-family'];
 if (sid === 's5x') { g.box = pick('.steps li', B); g.boxBlk = pick('.steps li.blk', B); g.boxRed = pick('.steps li.red', B);
   g.head = pick('.steps li .sh', T.concat(['background-color','padding-top','min-height'])); g.headBlk = pick('.steps li.blk .sh', ['background-color','color']); g.headRed = pick('.steps li.red .sh', ['background-color','color']);
   g.body = pick('.steps .sb', T); g.tag = pick('.steps .st', T.concat(['font-style'])); g.tagRed = pick('.steps .k4 .st', T);
   g.connLine = pick('.steps li+li', ['border-top-width','border-top-color','width','top','left'], '::before'); g.connHead = pick('.steps li+li', ['border-left-width','border-left-color','border-top-width','border-bottom-width'], '::after');
   g.regen = pick('.regen', ['border-left-width','border-left-style','border-left-color','height'].concat([])); g.regenTip = pick('.regen .tip', ['border-bottom-width','border-left-width']); g.regenLabel = pick('.regen .rl', T);
   g.steps = R(s.querySelector('.steps').getBoundingClientRect()); g.gap = cs(s.querySelector('.steps')).columnGap; g.xl = R(s.querySelector('.xl').getBoundingClientRect()); }
 if (sid === 's4p') { g.col = pick('.c5 > div', B); g.ix = pick('.c5 .ix', T); g.h3 = pick('.c5 h3', T); g.p = pick('.c5 div p:last-child', T); g.gap = cs(s.querySelector('.c5')).columnGap;
   g.cols = [...s.querySelectorAll('.c5 > div')].map(d => R(d.getBoundingClientRect())); g.h3lines = [...s.querySelectorAll('.c5 h3')].map(h => lines(h).length); }
 if (sid === 's6b') { g.chip = pick('.wb-h.sp span', T.concat(['background-color','padding-top','padding-left','min-width'])); g.chipCo = pick('.wb-h.co span', ['background-color']); g.chipQu = pick('.wb-h.qu span', ['background-color']);
   g.bus = pick('.wb-bus path', ['stroke','stroke-width','fill']); g.busRect = R(s.querySelector('.wb-bus').getBoundingClientRect());
   g.card = pick('.wb-g.sp', B); g.cardAll = pick('.wb-g.all', ['border-top-width','border-top-color']); g.cardQu = pick('.wb-g.qu', ['border-top-width','border-top-color']);
   g.gl = pick('.wb-g .gl', T); g.glAll = pick('.wb-g.all .gl', ['color']); g.li = pick('.wb-g li', T.concat(['border-top-width','border-top-color','padding-top'])); g.li2 = pick('.wb-g li+li', ['border-top-width','border-top-color']); g.done = pick('.done', T);
   g.chips = [...s.querySelectorAll('.wb-h span')].map(e => R(e.getBoundingClientRect())); g.cards = [...s.querySelectorAll('.wb-g')].map(e => R(e.getBoundingClientRect())); }
 if (sid === 's10') { g.cell = pick('.grid5 > div', B.concat(['border-right-width','border-right-color','border-bottom-color'])); g.grid = pick('.grid5', ['border-top-width','border-top-color','border-left-color']); g.pic = pick('.grid5 .pic', B.concat(['object-fit','mix-blend-mode']));
   g.ix = pick('.grid5 .ix', T); g.h3 = pick('.grid5 h3', T); g.p = pick('.grid5 p:not(.ix)', T); g.foot = pick('.foot', T);
   g.pics = [...s.querySelectorAll('.grid5 .pic')].map(e => ({rect:R(e.getBoundingClientRect()), src:(e.getAttribute('src')||'').slice(0,30), nat:[e.naturalWidth, e.naturalHeight]})); }
 if (sid === 's10map') { g.grid = pick('.dsm', ['background-color','row-gap','border-top-width','border-top-color']); g.tile = pick('.tile.p01', B.concat(['padding-bottom'])); g.soon = pick('.tile.p02', ['background-color']); g.soonInk = pick('.tile.p02 .ink-block', ['opacity']);
   g.idx = pick('.tile .idx', T); g.h3 = pick('.tile h3', T); g.d = pick('.tile .d', T); g.src = pick('.tile .src', T); g.badge = pick('.badge', T.concat(['border-top-width','border-top-color','padding-left']));
   g.tick = pick('.tile.p01 .tick', ['width','height','background-color']); g.tickSoon = pick('.tile.p02 .tick', ['background-color']); g.hubh = pick('.hubh', T); g.rule = pick('.accent-rule', ['width','height','background-color']); g.strap = pick('.strap', T);
   g.dsm = R(s.querySelector('.dsm').getBoundingClientRect()); g.tileRect = R(s.querySelector('.tile.p01').getBoundingClientRect()); }
 res.g = g;
 return res;
}"""
data = {}
t0 = time.time(); errs = []
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ['RENDER_SHELL'], args=['--no-sandbox'])
    for (W, H) in vps:
        pg = b.new_page(viewport={'width': W, 'height': H}, device_scale_factor=1)
        pg.add_init_script(BLOCK)
        pg.on('pageerror', lambda x: errs.append('pageerror: %s' % x))
        pg.goto('file://' + deck, wait_until='load'); time.sleep(3.0)
        order = pg.evaluate("() => [...document.querySelectorAll('section.slide')].map(s => s.id)")
        rows = []
        for i, sid in enumerate(order):
            pg.evaluate('n => window.deckGo(n)', i); time.sleep(1.5)
            rows.append(pg.evaluate(JS, sid))
            if shots and ('%dx%d' % (W, H)) in shots[0] and sid in shots[1]:
                os.makedirs(os.path.dirname(os.path.abspath(shots[0])) or '.', exist_ok=True)
                pg.screenshot(path='%s-%02d-%s.png' % (shots[0], i + 1, sid))
        data['%dx%d' % (W, H)] = rows
        if (W, H) == vps[0]:
            data['anatomy'] = pg.evaluate('() => window.anatomyState ? window.anatomyState() : null')
        pg.close()
    b.close()
data['errors'] = errs; data['secs'] = round(time.time() - t0, 1)
json.dump(data, open(out, 'w'), indent=1)
print('measured', list(data.keys()), 'errors', len(errs), 'secs', data['secs'])
