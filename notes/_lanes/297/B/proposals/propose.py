# #297 lane B - five diagram PROPOSALS, shown next to the slide as it is now. Nothing here reaches the deck.
# Writes notes/_lanes/297/B/proposals/deck-proposed.html = the rebuilt deck + ONE <style> + ONE <script>
# (data-lane="297-B-proposal"), renders "now" (the deck itself) and "proposed" (the copy) for 04 06 11 12 13
# at 1440x900, then composes one PNG per slide: Now | Proposed + the change list.
# Usage (repo root, render env sourced): python3 notes/_lanes/297/B/proposals/propose.py [shoot|compose|all]
import os, sys, time, json, html
R = os.path.abspath('.') + '/'
DECK = R + 'notes/_DEMO-SLIDES-apollo-2026-09-22-v14-plain.html'
PD = R + 'notes/_lanes/297/B/proposals/'
COPY = PD + 'deck-proposed.html'
SHOTS = PD + '_shots/'
OUT = R + 'notes/_lanes/297/B/'
W, H = 1440, 900
TARGETS = [('04', 's5x', 'The loop'), ('06', 's4p', 'Five causes'), ('11', 's6b', 'Three problems'),
           ('12', 's10', 'Three elements'), ('13', 's10map', 'The map')]

CSS = r"""<style data-lane="297-B-proposal">
/* #297 lane B - PROPOSAL ONLY, never in the deck. One grammar for 04 06 11 12 13, borrowed from the drawings
   on 07-10 (R1's grammar, notes/_subreports/2026-09-22-297-R1-art-director-diagrams.md):
   line 1px - things and flow in ink #111, dividers and frames round pictures in #D7D8D6 · dash 5/4 = goes back / not yet ·
   one arrowhead, solid 6x8, flow only · containers white and square, no filled bands, no white type on colour ·
   labels 12/500/caps/.14em, numbers grey, titles 18/600 or 16/600, body 16 #333 · red = the one thing to look at, a line, never a fill. */
:root{--pp-ink:#111;}
/* ---- 04 the loop ---- */
#s5x .steps li{border:1px solid var(--pp-ink)!important;}
#s5x .steps li.k4,#s5x .steps li.k5{border-color:var(--accent)!important;}
#s5x .sh,#s5x .blk .sh,#s5x .red .sh{background:none!important;color:var(--pp-ink)!important;font-size:12px!important;font-weight:500!important;
  letter-spacing:.14em!important;line-height:1.4!important;padding:12px 12px 10px!important;border-bottom:1px solid var(--g3);min-height:calc(2.8em + 22px)!important;}
#s5x .sh .pn{color:var(--g6);margin-right:.7em;}
#s5x .steps li+li::before{border-top:1px solid var(--pp-ink)!important;top:28px!important;left:calc(-1 * var(--gap) - 1px)!important;width:calc(var(--gap) - 6px)!important;}
#s5x .steps li+li::after{border:0!important;border-left:6px solid var(--pp-ink)!important;border-top:4px solid transparent!important;border-bottom:4px solid transparent!important;top:24.5px!important;left:-7px!important;}
#s5x .sb{font-size:16px!important;color:#333!important;}
#s5x .st{font-style:normal!important;font-weight:500!important;letter-spacing:.04em!important;color:var(--g6)!important;}
#s5x .k4 .st,#s5x .k5 .st{color:var(--accent)!important;}
#s5x .regen{border:0!important;}
#s5x .regen .tip{display:none!important;}
#s5x .regen .rl{font-size:12px!important;}
/* ---- 06 five causes ---- */
#s4p .c5 > div{border-top:1px solid var(--pp-ink);padding-top:16px!important;}
#s4p .c5 > div.pp-one{border-top:2px solid var(--accent);padding-top:15px!important;}
#s4p .c5 .ix{color:var(--g6)!important;}
#s4p .c5 h3{font-size:18px!important;line-height:1.3!important;}
#s4p .c5 div p:last-child{font-size:16px!important;line-height:1.5!important;color:#333!important;}
/* ---- 11 three problems ---- */
#s6b .wb-h span{background:none!important;color:var(--pp-ink)!important;font-size:12px!important;font-weight:500!important;letter-spacing:.14em!important;
  padding:0 0 8px!important;min-width:0!important;}
#s6b .wb-h.sp span{color:var(--accent)!important;}
#s6b .wb-bus path{stroke:var(--pp-ink)!important;stroke-width:1!important;}
#s6b .wb-g{border:1px solid var(--pp-ink)!important;}
#s6b .wb-g.sp{border-color:var(--accent)!important;}
#s6b .wb-g.sp .gl,#s6b .wb-g.qu .gl{display:none!important;}
#s6b .wb-g.all .gl{color:var(--g6)!important;font-size:12px!important;}
#s6b .wb-g li{font-size:16px!important;border-top-color:var(--g3)!important;}
#s6b .done{margin:6px 0 0!important;}
/* ---- 12 three elements ---- */
#s10 .grid5 .ix{color:var(--g6)!important;}
#s10 .grid4{border-top-color:var(--g3)!important;border-left-color:var(--g3)!important;}
#s10 .grid4>div{border-right-color:var(--g3)!important;border-bottom-color:var(--g3)!important;}
#s10 .grid5 p:not(.ix){font-size:16px!important;line-height:1.45!important;color:#333!important;}
/* ---- 13 the map ---- */
#s10map .dsm{border-color:var(--pp-ink)!important;}
#s10map .tile .src{display:none!important;}
#s10map .tile .idx{font-size:12px!important;font-weight:500!important;color:var(--g6)!important;margin-bottom:6px!important;}
#s10map .tile h3{font-size:16px!important;font-weight:600!important;line-height:1.3!important;}
#s10map .tile .d{font-size:13px!important;line-height:1.4!important;color:#333!important;margin-top:6px!important;}
#s10map .tile[data-state="soon"]{background-color:#fff!important;
  background-image:repeating-linear-gradient(90deg,var(--g5) 0 5px,transparent 5px 9px),repeating-linear-gradient(90deg,var(--g5) 0 5px,transparent 5px 9px),
    repeating-linear-gradient(180deg,var(--g5) 0 5px,transparent 5px 9px),repeating-linear-gradient(180deg,var(--g5) 0 5px,transparent 5px 9px)!important;
  background-size:calc(100% - 10px) 1px,calc(100% - 10px) 1px,1px calc(100% - 10px),1px calc(100% - 10px)!important;
  background-position:5px 5px,5px calc(100% - 5px),5px 5px,calc(100% - 5px) 5px!important;background-repeat:no-repeat!important;}
#s10map .tile[data-state="soon"] .ink-block{opacity:1!important;}
#s10map .badge{font-family:var(--font)!important;font-size:12px!important;font-weight:500!important;letter-spacing:.14em!important;border:0!important;
  padding:0!important;color:var(--g6)!important;background:none!important;}
</style>
"""

JS = r"""<script data-lane="297-B-proposal">
/* #297 lane B - PROPOSAL ONLY. DOM half of the five proposals. */
(function(){
  var NS = 'http://www.w3.org/2000/svg';
  var ACC = (getComputedStyle(document.documentElement).getPropertyValue('--accent') || '#DA1A00').trim();
  function q(s){ return document.querySelector(s); } function qa(s){ return [].slice.call(document.querySelectorAll(s)); }
  /* 04: "1 · Intake" -> grey "01" + "Intake"; the loop back as one red dashed hairline with one small head */
  qa('#s5x .sh').forEach(function(e){ var m = e.textContent.match(/^(\d)\s*·\s*([\s\S]*)$/); if (!m) return;
    e.textContent = ''; var n = document.createElement('span'); n.className = 'pn'; n.textContent = '0' + m[1]; e.appendChild(n); e.appendChild(document.createTextNode(m[2])); });
  function regen(){ var r = q('#s5x .regen'), st = q('#s5x .steps'); if (!r || !st) return;
    var old = r.querySelector('svg.pp'); if (old) old.parentNode.removeChild(old);
    var rb = r.getBoundingClientRect(), gap = Math.max(0, rb.top - st.getBoundingClientRect().bottom), w = rb.width, h = rb.height + gap;
    var s = document.createElementNS(NS, 'svg'); s.setAttribute('class', 'pp'); s.setAttribute('width', w); s.setAttribute('height', h);
    s.setAttribute('viewBox', '0 0 ' + w + ' ' + h); s.style.cssText = 'position:absolute;left:0;top:' + (-gap) + 'px;overflow:visible';
    var p = document.createElementNS(NS, 'path'); p.setAttribute('d', 'M' + (w - .5) + ' 0V' + (h - .5) + 'H.5V8');
    p.setAttribute('fill', 'none'); p.setAttribute('stroke', ACC); p.setAttribute('stroke-width', '1'); p.setAttribute('stroke-dasharray', '5 4'); s.appendChild(p);
    var t = document.createElementNS(NS, 'path'); t.setAttribute('d', 'M.5 0L4.5 8H-3.5Z'); t.setAttribute('fill', ACC); s.appendChild(t);
    r.appendChild(s); }
  /* 06: one title block height, so the five descriptions start on one line; the cause tackled first carries the red line */
  function eq(){ var hs = qa('#s4p .c5 h3'); hs.forEach(function(h){ h.style.minHeight = ''; });
    var mx = Math.max.apply(null, hs.map(function(h){ return h.getBoundingClientRect().height; })); hs.forEach(function(h){ h.style.minHeight = mx + 'px'; }); }
  qa('#s4p .c5 > div').forEach(function(d){ if (/Small component library/.test(d.textContent)) d.classList.add('pp-one'); });
  /* 11: the shared column's label, and the tick under the library it names */
  var all = q('#s6b .wb-g.all .gl'); if (all) all.textContent = 'Shared by all three';
  var done = q('#s6b .done'), lib = qa('#s6b .wb-g.all li').filter(function(l){ return /Small component library/.test(l.textContent); })[0];
  if (done && lib){ done.textContent = 'Addressed first'; lib.appendChild(done); }
  /* 13: sentence case */
  qa('#s10map .tile h3').forEach(function(h){ var t = h.textContent, w = t.split(' ');
    h.textContent = w.map(function(x, i){ return (i === 0 || /^(UX|CX|&)$/.test(x)) ? x : x.toLowerCase(); }).join(' '); });
  /* 12: the plates show the drawings of 07 (catalogue), 08 (graph) and 10 (brain), cropped to their ink and drawn at ONE scale */
  function crop(src){ return new Promise(function(res){ var im = new Image(); im.onload = function(){
      var c = document.createElement('canvas'); c.width = im.naturalWidth; c.height = im.naturalHeight; var x = c.getContext('2d'); x.drawImage(im, 0, 0);
      var d = x.getImageData(0, 0, c.width, c.height).data, x0 = c.width, y0 = c.height, x1 = 0, y1 = 0, X, Y, i;
      for (Y = 0; Y < c.height; Y++) for (X = 0; X < c.width; X++){ i = (Y * c.width + X) * 4;
        if (d[i] < 236 || d[i+1] < 236 || d[i+2] < 236){ if (X < x0) x0 = X; if (X > x1) x1 = X; if (Y < y0) y0 = Y; if (Y > y1) y1 = Y; } }
      res({im: im, x0: x0, y0: y0, w: x1 - x0 + 1, h: y1 - y0 + 1}); }; im.src = src; }); }
  var tries = 0;
  function plates(){ var M = [['an1', 'ctPrint'], ['an2', 'shlPrint'], ['an3', 'brPrint']];
    var src = M.map(function(p){ var e = document.getElementById(p[1]); return e && e.src && e.src.slice(0, 10) === 'data:image' ? e.src : null; });
    if (src.some(function(s){ return !s; })){ if (++tries < 40) setTimeout(plates, 400); return; }
    Promise.all(src.map(crop)).then(function(cs){
      var pics = M.map(function(p){ return document.getElementById(p[0]); });
      var pw = pics[0].clientWidth - 12, ph = pics[0].clientHeight - 12, k = Math.max(1, window.devicePixelRatio || 1);
      var sc = Math.min.apply(null, cs.map(function(c){ return Math.min(pw / c.w, ph / c.h); })) * .92;
      cs.forEach(function(c, j){ var cv = document.createElement('canvas'); cv.width = Math.round(pw * k); cv.height = Math.round(ph * k);
        var x = cv.getContext('2d'); x.fillStyle = '#fff'; x.fillRect(0, 0, cv.width, cv.height); x.imageSmoothingQuality = 'high';
        var dw = c.w * sc * k, dh = c.h * sc * k; x.drawImage(c.im, c.x0, c.y0, c.w, c.h, (cv.width - dw) / 2, (cv.height - dh) / 2, dw, dh);
        /* at ~0.4 scale a 1px line resamples to pale grey; a gamma on the plate brings the hairlines back to ink */
        var g = x.getImageData(0, 0, cv.width, cv.height), gd = g.data, gi; for (gi = 0; gi < gd.length; gi += 4){ gd[gi] = 255 * Math.pow(gd[gi] / 255, 2.4); gd[gi+1] = 255 * Math.pow(gd[gi+1] / 255, 2.4); gd[gi+2] = 255 * Math.pow(gd[gi+2] / 255, 2.4); } x.putImageData(g, 0, 0);
        pics[j].src = cv.toDataURL('image/png'); pics[j].style.objectFit = 'contain'; });
      pics[0].alt = 'Line drawing of the catalogue'; pics[1].alt = 'Line drawing of the knowledge graph'; pics[2].alt = 'Line drawing of a brain';
      window.ppPlates = {scale: +sc.toFixed(4), crops: cs.map(function(c){ return [c.w, c.h]; }), plate: [pw, ph]}; }); }
  function lay(){ regen(); eq(); }
  window.addEventListener('load', function(){ setTimeout(lay, 300); setTimeout(plates, 1600); });
  window.addEventListener('resize', lay);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(lay);
  window.ppLayout = lay;
})();
</script>
"""

CHANGES = {
 '04': ['The filled black, grey and red header bands go. Each step is a white box drawn in the drawings’ thin black line, its name a small label over a hairline.',
        'Step numbers read 01 to 06, in grey.',
        'Red marks one idea, the checking: steps 04 and 05 are outlined in red, like the red page in the catalogue drawing, and the way back from a failed gate is a thin red dashed line.',
        'The arrows are one thin black line with one small solid head. The italic notes stand upright.'],
 '06': ['A thin black line over each of the five columns, like the edges in the drawings. Still no boxes.',
        'Numbers in grey. Titles one size smaller (22 to 18) and given one height, so all five descriptions start on the same line.',
        'A red line, the one heavier line, marks the cause tackled first, the small component library: the thread into the catalogue on 07.',
        'Descriptions at the deck’s body size, 16, in dark grey.'],
 '11': ['The filled red, black and grey chips become plain labels: Speed in red, Consistency and Quality in black.',
        'The connecting line is one thin black line.',
        'Each card is outlined in the thin black line, the Speed card in red. The repeated SPEED and QUALITY labels inside the cards go.',
        '“All · shared by all three” reads “Shared by all three”. The tick moves under “Small component library” and reads “Addressed first”.'],
 '12': ['The plates show the three drawings the audience has just seen, the catalogue (07), the graph (08) and the brain (10), all at one scale. Today two of them, a gearbox and books, appear nowhere else in the deck.',
        'Numbers in grey, not red.',
        'The cell lines that are invisible today (light grey on light grey) are drawn in the drawings’ light grey.',
        'Descriptions at the deck’s body size, 16.'],
 '13': ['The twelve file paths go: tiny grey code type that no one can read from the room.',
        'Numbers, titles and descriptions come up to the deck’s sizes: grey 12 numbers, bold 16 titles in sentence case, 13 descriptions.',
        '“In progress” tiles become white with a grey dashed line inside, the drawings’ “not yet” line, instead of faded type on grey.',
        'The outer frame is drawn in the thin black line and the grid inside stays light grey. The red rule under Apollo stays the only red.'],
}

def write_copy():
    h = open(DECK, encoding='utf-8').read()
    assert h.count('</body>') == 1 and '297-B-proposal' not in h
    h = h.replace('</body>', CSS + JS + '</body>')
    open(COPY, 'w', encoding='utf-8').write(h); print('wrote', COPY, len(h.encode()))

def shoot():
    from playwright.sync_api import sync_playwright
    os.makedirs(SHOTS, exist_ok=True)
    BLOCK = ("window.addEventListener('pointermove', function(e){ e.stopImmediatePropagation(); }, {capture:true});"
             "window.addEventListener('mousemove', function(e){ e.stopImmediatePropagation(); }, {capture:true});")
    facts = {}; errs = []
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=os.environ['RENDER_SHELL'], args=['--no-sandbox'])
        for tag, f in (('now', DECK), ('proposed', COPY)):
            pg = b.new_page(viewport={'width': W, 'height': H}, device_scale_factor=1)
            pg.add_init_script(BLOCK); pg.on('pageerror', lambda x: errs.append('%s' % x))
            pg.goto('file://' + f, wait_until='load'); time.sleep(4.5)
            order = pg.evaluate("() => [...document.querySelectorAll('section.slide')].map(s => s.id)")
            for n, sid, name in TARGETS:
                i = order.index(sid)
                pg.evaluate('n => window.deckGo(n)', i); time.sleep(1.8)
                pg.evaluate('() => { window.brSet && window.brSet(0,0); window.shlSet && window.shlSet(0,0); if (window.calSetTime){ window.calSetTime(0); window.calStill(); } if (window.kgPause){ window.kgPause(true); window.kgStill(); } window.ppLayout && window.ppLayout(); }'); time.sleep(0.4)
                pg.screenshot(path='%s%s-%s.png' % (SHOTS, n, tag))
            facts[tag] = pg.evaluate('() => window.ppPlates || null')
            pg.close()
        b.close()
    facts['errors'] = errs; json.dump(facts, open(SHOTS + '_facts.json', 'w'), indent=1); print('shot', json.dumps(facts))

PAGE = """<!doctype html><html><head><meta charset="utf-8"><style>
body{margin:0;background:#fff;font-family:"Helvetica Neue",Helvetica,Arial,sans-serif;color:#111;-webkit-font-smoothing:antialiased;}
.wrap{width:2960px;padding:40px;}
.hd{display:flex;align-items:baseline;gap:28px;margin:0 0 26px;}
.hd .n{font-size:44px;font-weight:300;} .hd .t{font-size:34px;font-weight:600;} .hd .s{margin-left:auto;font-size:22px;font-weight:500;letter-spacing:.14em;text-transform:uppercase;color:#767676;}
.pair{display:grid;grid-template-columns:1440px 1440px;column-gap:40px;}
.lab{font-size:22px;font-weight:500;letter-spacing:.14em;text-transform:uppercase;margin:0 0 12px;display:flex;align-items:center;gap:14px;}
.lab::before{content:"";width:32px;height:1px;background:currentColor;}
.now .lab{color:#767676;} .pro .lab{color:#DA1A00;}
img{display:block;width:1440px;height:900px;outline:1px solid #D7D8D6;}
.cap{margin:34px 0 0;padding:26px 0 0;border-top:1px solid #111;display:grid;grid-template-columns:repeat(%(k)d,1fr);column-gap:40px;}
.cap div{font-size:25px;line-height:1.42;color:#333;} .cap b{display:block;font-size:22px;font-weight:500;letter-spacing:.14em;color:#767676;margin:0 0 8px;}
</style></head><body><div class="wrap">
<div class="hd"><span class="n">%(n)s</span><span class="t">%(name)s</span><span class="s">A proposal · not in the deck</span></div>
<div class="pair"><div class="now"><p class="lab">Now</p><img src="../_shots/%(n)s-now.png"></div>
<div class="pro"><p class="lab">Proposed</p><img src="../_shots/%(n)s-proposed.png"></div></div>
<div class="cap">%(cap)s</div></div></body></html>"""

def compose():
    from playwright.sync_api import sync_playwright
    cdir = PD + '_compose/'; os.makedirs(cdir, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=os.environ['RENDER_SHELL'], args=['--no-sandbox'])
        pg = b.new_page(viewport={'width': 3040, 'height': 1200}, device_scale_factor=1)
        for n, sid, name in TARGETS:
            cap = ''.join('<div><b>%02d</b>%s</div>' % (i + 1, html.escape(c)) for i, c in enumerate(CHANGES[n]))
            f = cdir + n + '.html'
            open(f, 'w', encoding='utf-8').write(PAGE % {'n': n, 'name': html.escape(name), 'cap': cap, 'k': len(CHANGES[n])})
            pg.goto('file://' + f, wait_until='load'); time.sleep(0.6)
            pg.screenshot(path=OUT + 'diagram-%s.png' % n, full_page=True)
            print('composed', OUT + 'diagram-%s.png' % n)
        b.close()
    json.dump({n: CHANGES[n] for n, _, _ in TARGETS}, open(PD + 'changes.json', 'w'), indent=1)

if __name__ == '__main__':
    what = sys.argv[1] if len(sys.argv) > 1 else 'all'
    if what in ('all', 'shoot'): write_copy(); shoot()
    if what in ('all', 'compose'): compose()
