# #296 lane C - chapter rail (orientation pattern) into the v14-plain deck.
# Inserts ONE <style data-lane="296-C">, ONE <nav id="chrail">, ONE <script data-lane="296-C">.
# Idempotent: rebuilds from notes/_lanes/296/C/v14-plain-before-c.html every run.
import os
R = os.path.abspath('.') + '/'
SRC = R + 'notes/_lanes/296/C/v14-plain-before-c.html'
DST = R + 'notes/_DEMO-SLIDES-apollo-2026-09-22-v14-plain.html'
h = open(SRC, encoding='utf-8').read()

STYLE = r'''<style data-lane="296-C">
/* #296 lane C - THE CHAPTER RAIL (orientation pattern), v2.
   v1 Dave: "a vertical timeline style progress indicator with circles indicating
   the chapters and smaller filled dots indicating any sub-pages ... persistent ...
   the position indicator should grow to be a larger circle with the chapter number
   inside and the chapter title to the right ... I want to see them very tiny".
   v2 Dave: "have the line go all the way down the screen, and the items up to the
   top ... the circles with the number have a line running through it, can we remove
   ... the current slide number in the same position by bunching the others up ...
   the circle and title bigger".
   So: the nav is fixed and full height; the line runs top 0 to bottom 0; every
   circle is filled with the slide's ground so the line never shows through; the
   current chapter sits at a fixed anchor y and the rest bunch above and below it. */
#chrail{--rk:var(--black);--rk2:var(--g6);--rdot:var(--g5);--rground:var(--white);--racc:var(--accent);
  position:fixed;left:16px;top:0;bottom:0;z-index:120;width:280px;margin:0;padding:0;
  font-family:var(--font);pointer-events:none;opacity:1;transition:opacity .2s var(--ease);}
#chrail.is-grey{--rground:var(--g1);}
#chrail.is-dark{--rk:var(--white);--rk2:var(--g5);--rdot:var(--g6);--rground:var(--black);--racc:var(--accent-dark);}
#chrail.is-hidden{opacity:0;}
#chrail.is-hidden .cr-row{pointer-events:none;}
#chrail ol{list-style:none;margin:0;padding:0;position:absolute;inset:0;}
/* the line: full viewport height, through the centre of the 44px marker column */
#chrail ol::before{content:"";position:absolute;left:21.5px;top:0;bottom:0;width:1px;background:var(--rk2);opacity:.55;transition:background .2s;}
#chrail li{position:absolute;left:0;top:0;height:0;margin:0;padding:0;
  transition:top .25s var(--ease);}
#chrail .cr-row{position:absolute;left:0;top:0;transform:translateY(-50%);display:flex;align-items:center;gap:12px;
  height:44px;padding:0;margin:0;border:0;background:none;cursor:pointer;pointer-events:auto;font:inherit;color:var(--rk);text-align:left;}
#chrail .cr-sub .cr-row{height:14px;}
#chrail .cr-mk{flex:0 0 44px;height:44px;display:flex;align-items:center;justify-content:center;}
#chrail .cr-sub .cr-mk{height:14px;}
/* chapter: hollow circle, filled with the ground so the line stops at its edge */
#chrail .cr-c{position:relative;z-index:1;width:12px;height:12px;border-radius:50%;border:1px solid var(--rk);background:var(--rground);
  display:flex;align-items:center;justify-content:center;font-size:0;font-weight:300;color:var(--rk);line-height:1;
  transition:width .25s var(--ease),height .25s var(--ease),font-size .25s var(--ease),border-color .2s,background .2s,color .2s;}
/* sub-page: smaller filled dot */
#chrail .cr-d{position:relative;z-index:1;width:6px;height:6px;border-radius:50%;background:var(--rdot);
  transition:width .2s var(--ease),height .2s var(--ease),background .2s;}
/* titles: very tiny for the others (flag: tinyTitles) */
#chrail .cr-t{font-size:7px;font-weight:500;letter-spacing:.12em;text-transform:uppercase;color:var(--rk2);
  line-height:1.4;white-space:nowrap;display:flex;align-items:center;gap:8px;
  transition:font-size .25s var(--ease),color .2s;}
#chrail.no-tiny .cr-ch:not(.is-cur) .cr-t{display:none;}
#chrail .cr-t::before{content:"";width:0;height:1px;background:var(--racc);transition:width .25s var(--ease);}
/* THE CURRENT CHAPTER: 44px circle, number in the display face; v4: title = the slides' own eyebrow (.label) */
#chrail .cr-ch.is-cur .cr-c{width:44px;height:44px;font-size:22px;font-weight:300;letter-spacing:-.01em;border-color:var(--rk);}
#chrail .cr-ch.is-cur > .cr-row .cr-t{font-size:12px;font-weight:500;letter-spacing:.14em;line-height:1.4;color:var(--racc);}
#chrail .cr-ch.is-cur > .cr-row .cr-t::before{width:24px;}
/* the current sub-page's own dot */
#chrail .cr-sub.is-cur .cr-d{width:10px;height:10px;background:var(--racc);}
#chrail .cr-row:focus-visible{outline:1px solid var(--racc);outline-offset:2px;}
@media (prefers-reduced-motion:reduce){ #chrail, #chrail *{transition:none !important;} }
@media print{ #chrail{display:none !important;} }
</style>
<nav id="chrail" class="is-hidden" aria-label="Chapters"></nav>
'''

SCRIPT = r'''<script data-lane="296-C">
/* #296 lane C - the chapter rail, v2. RAIL is the only thing to edit:
   a chapter is {n, title, id, subs:[ids]}; ids are the slides' own ids.
   The rail follows DOM order; the current slide is found by POSITION
   (which slide the middle of the screen sits on). The current chapter's
   circle sits at anchor x viewport height on every slide; v3: everything
   before it stacks upward and everything after stacks downward at one
   fixed spacing (RAIL.step), so the rail is laid out the same way always.
   On the agenda (nothing current) the items spread evenly top to bottom. */
var RAIL = {
  hideOn:      ['s1','s2'], // rail hidden on these slides (cover, agenda); shown everywhere else
  tinyTitles:  false,      // v3: only the current chapter shows its title (true brings the tiny titles back)
  anchor:      0.38,       // current chapter's centre, as a fraction of viewport height
  topInset:    40,         // px, first item's centre from the top edge
  bottomInset: 40,         // px, last item's centre from the bottom edge
  clear:       40,         // px, gap kept between the grown circle's centre and its neighbours
  step:        34,         // px, v4: item-to-item spacing, above and below, on every slide. If the
                           //  full stack would not fit the viewport at this step, the largest step that
                           //  fits is used instead (at 900px high that is 26.2px; 34px from ~1105px high)
  chapters: [
    {n:1, title:'Observation', id:'s3',  subs:[]},
    {n:2, title:'Problem',     id:'s4p', subs:[]},
    {n:3, title:'Experiment',  id:'s5x', subs:[]},
    {n:4, title:'Results',     id:'s5r', subs:[]},
    {n:5, title:'Response',    id:'s6',  subs:['s6b','s7','s8']},
    {n:6, title:'The build',   id:'s9',  subs:['s10','s10map']},
    {n:7, title:'The ask',     id:'s11', subs:['s12']}
  ]
};
(function(){
  var deck = document.getElementById('deck'), nav = document.getElementById('chrail');
  if (!deck || !nav) return;
  var slides = Array.prototype.slice.call(document.querySelectorAll('.slide'));
  if (!RAIL.tinyTitles) nav.classList.add('no-tiny');
  var ol = document.createElement('ol'), byId = {}, items = [];
  function row(li, id, label, inner){
    var b = document.createElement('button');
    b.type = 'button'; b.className = 'cr-row'; b.setAttribute('aria-label', label);
    b.innerHTML = inner;
    b.addEventListener('click', function(){
      var s = document.getElementById(id); if (s) s.scrollIntoView({behavior:'smooth'});
    });
    li.appendChild(b); ol.appendChild(li); items.push(li);
  }
  RAIL.chapters.forEach(function(c){
    var li = document.createElement('li'); li.className = 'cr-ch';
    row(li, c.id, c.n + ' ' + c.title,
        '<span class="cr-mk"><span class="cr-c">' + c.n + '</span></span><span class="cr-t">' + c.title + '</span>');
    byId[c.id] = {ch:li};
    (c.subs || []).forEach(function(sid){
      var sl = document.createElement('li'); sl.className = 'cr-sub';
      row(sl, sid, c.title + ' - ' + sid, '<span class="cr-mk"><span class="cr-d"></span></span>');
      byId[sid] = {ch:li, sub:sl};
    });
  });
  nav.appendChild(ol);
  /* spread n items evenly from a to b (a and b included); one item sits at a */
  function spread(n, a, b){
    var out = [], i; if (n === 1) return [a];
    for (i = 0; i < n; i++) out.push(a + (b - a) * i / (n - 1));
    return out;
  }
  function layout(curLi){
    var H = window.innerHeight, top = RAIL.topInset, bot = H - RAIL.bottomInset, ys = [], k = items.indexOf(curLi);
    if (k < 0){ ys = spread(items.length, top, bot); }
    else {
      var A = Math.round(H * RAIL.anchor), up = [], dn = [], i, n = items.length;
      /* one step for every slide at this viewport: RAIL.step, or the largest that fits the
         worst cases (last chapter current -> most items above; first chapter current -> most below) */
      var chs = items.filter(function(li){ return li.classList.contains('cr-ch'); });
      var kHi = items.indexOf(chs[chs.length - 1]), kLo = items.indexOf(chs[0]);
      var st = Math.min(RAIL.step, (A - RAIL.clear - top) / Math.max(1, kHi - 1), (bot - A - RAIL.clear) / Math.max(1, n - kLo - 2));
      /* v3: fixed spacing - stack upward and downward from the anchor at RAIL.step */
      for (i = 0; i < k; i++) up.push(A - RAIL.clear - i * st);
      for (i = 0; i < items.length - k - 1; i++) dn.push(A + RAIL.clear + i * st);
      ys = up.slice(0, k).reverse().concat([A], dn.slice(0, items.length - k - 1));
    }
    items.forEach(function(li, i){ li.style.top = (Math.round(ys[i] * 10) / 10) + 'px'; });
  }
  var last = null;
  function current(){
    var mid = deck.scrollTop + deck.clientHeight / 2, cur = slides[0];
    for (var i = 0; i < slides.length; i++){ if (slides[i].offsetTop <= mid) cur = slides[i]; }
    return cur;
  }
  function update(){
    var s = current(); if (s === last) return; last = s;
    nav.classList.toggle('is-hidden', RAIL.hideOn.indexOf(s.id) > -1);
    nav.classList.toggle('is-dark', s.classList.contains('dark'));
    nav.classList.toggle('is-grey', s.classList.contains('grey'));
    Array.prototype.forEach.call(nav.querySelectorAll('.is-cur'), function(n){ n.classList.remove('is-cur'); });
    Array.prototype.forEach.call(nav.querySelectorAll('[aria-current]'), function(n){ n.removeAttribute('aria-current'); });
    var m = byId[s.id];
    if (m){
      m.ch.classList.add('is-cur');
      if (m.sub){ m.sub.classList.add('is-cur'); m.sub.firstChild.setAttribute('aria-current', 'step'); }
      else m.ch.firstChild.setAttribute('aria-current', 'step');
    }
    layout(m ? m.ch : null);
  }
  var raf = 0;
  deck.addEventListener('scroll', function(){ if (!raf) raf = requestAnimationFrame(function(){ raf = 0; update(); }); });
  window.addEventListener('resize', function(){ last = null; update(); });
  update();
  window.chRail = {data: RAIL, update: function(){ last = null; update(); }};
})();
</script>
'''
anchor = '<p class="keyhint" id="keyhint">'
assert h.count(anchor) == 1 and h.count('</body>') == 1 and 'data-lane="296-C"' not in h
i = h.index(anchor); j = h.index('\n', i) + 1
h = h[:j] + STYLE + h[j:]
h = h.replace('</body>', SCRIPT + '</body>')
open(DST, 'w', encoding='utf-8').write(h)
print('wrote', DST, len(h.encode()))
