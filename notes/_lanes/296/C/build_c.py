# #296 lane C - chapter rail (orientation pattern) into the v14-plain deck.
# Inserts ONE <style data-lane="296-C">, ONE <nav id="chrail">, ONE <script data-lane="296-C">.
# Idempotent: rebuilds from notes/_lanes/296/C/v14-plain-before-c.html every run.
import os
R = os.path.abspath('.') + '/'
SRC = R + 'notes/_lanes/296/C/v14-plain-before-c.html'
DST = R + 'notes/_DEMO-SLIDES-apollo-2026-09-22-v14-plain.html'

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
/* v5 (Dave: "anything other than the current chapter to be faded ... a much lighter grey on the white
   backgrounds and a darker on the dark"): --rfade = everything not current (line, circles, dots);
   --rmid = the current chapter's own sub-dots. Deck tokens only: g3/g5 on light, g8/g6 on dark. */
#chrail{--rk:var(--black);--rk2:var(--g6);--rdot:var(--g5);--rground:var(--white);--racc:var(--accent);--rfade:var(--g3);--rmid:var(--g5);
  position:fixed;left:16px;top:0;bottom:0;z-index:120;width:280px;margin:0;padding:0;
  font-family:var(--font);pointer-events:none;opacity:1;transition:opacity .2s var(--ease);}
#chrail.is-grey{--rground:var(--g1);}
#chrail.is-dark{--rk:var(--white);--rk2:var(--g5);--rdot:var(--g6);--rground:var(--black);--racc:var(--accent-dark);--rfade:var(--g8);--rmid:var(--g6);}
#chrail.is-hidden{opacity:0;}
#chrail.is-hidden .cr-row{pointer-events:none;}
#chrail ol{list-style:none;margin:0;padding:0;position:absolute;inset:0;}
/* the line: full viewport height, through the centre of the 44px marker column */
#chrail ol::before{content:"";position:absolute;left:21.5px;top:0;bottom:0;width:1px;background:var(--rfade);transition:background .2s;}
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
/* v7 (#297 lane B): no dash before the title - Dave 2026-09-23: "lets remove the m-dash from the titles
   to get a little more space and give it a rail". The eyebrow's own dash on the slides (.label::before) is untouched. */
/* THE CURRENT CHAPTER: 44px circle, number in the display face; v4: title = the slides' own eyebrow (.label) */
#chrail .cr-ch.is-cur .cr-c{width:44px;height:44px;font-size:22px;font-weight:300;letter-spacing:-.01em;border-color:var(--rk);}
#chrail .cr-ch.is-cur > .cr-row .cr-t{font-size:12px;font-weight:500;letter-spacing:.14em;line-height:1.4;color:var(--racc);}
/* the current sub-page's own dot */
#chrail .cr-sub.is-cur .cr-d{width:10px;height:10px;background:var(--racc);}
#chrail .cr-row:focus-visible{outline:1px solid var(--racc);outline-offset:2px;}
/* v5 fade: not-current circles and dots go to --rfade; the current chapter's own dots to --rmid */
#chrail .cr-ch:not(.is-cur) .cr-c{border-color:var(--rfade);color:var(--rfade);}
#chrail .cr-ch:not(.is-cur) .cr-t{color:var(--rfade);}
#chrail .cr-sub .cr-d{background:var(--rfade);}
#chrail .cr-sub.is-grp .cr-d{background:var(--rmid);}
#chrail .cr-sub.is-cur .cr-d{background:var(--racc);}
/* v7 (#297 lane B) - THE RAIL'S OWN COLUMN. The rail title starts at 72px (16 inset + 44 marker + 12 gap);
   the longest, "EVALUATION", ends at ~163px; + a 32px (--s4) gutter, rounded up: --rail-w 200px. No slide's
   content enters it. Left padding is at least --rail-w; right padding matches it while the content can still
   centre (so at 1920 nothing moves) and gives way, never below the deck's own minimum, when it cannot (so at
   1440 the 1120 column steps right of the rail instead of shrinking). The drawing cards run a 1360 grid; the
   map keeps its own 72px minimum. #s1 keeps padding:0 (the rail is hidden there). */
:root{--rail-w:200px;}
.slide{padding-left:max(var(--s6),6vw,var(--rail-w));
  padding-right:max(var(--s6),6vw,min(var(--rail-w),100% - var(--rail-w) - var(--max)));}
#s4,#s5,#s6,#s7,#s7b,#s8{padding-right:max(var(--s6),6vw,min(var(--rail-w),100% - var(--rail-w) - 1360px));}
#s10map{padding-left:max(72px,var(--rail-w));padding-right:max(72px,min(var(--rail-w),100% - var(--rail-w) - var(--max)));}
/* the map fills the slide's height; below 1520 wide, where it has to step right of the rail, its bottom-right
   corner would meet the page number (1px at 1440), so there it stops above the page number's band. */
@media (max-width:1519px){ #s10map{padding-bottom:72px;} }
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
__CHAPTERS__};
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
    var li = document.createElement('li'); li.className = 'cr-ch'; li.setAttribute('data-ch', c.id);
    row(li, c.id, c.n + ' ' + c.title,
        '<span class="cr-mk"><span class="cr-c">' + c.n + '</span></span><span class="cr-t">' + c.title + '</span>');
    byId[c.id] = {ch:li};
    (c.subs || []).forEach(function(sid){
      var sl = document.createElement('li'); sl.className = 'cr-sub'; sl.setAttribute('data-ch', c.id);
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
    items.forEach(function(li, i){ /* positions only - the hide is opacity + pointer-events */ li.style.top = (Math.round(ys[i] * 10) / 10) + 'px'; });
  }
  var last = null;
  function current(){
    var mid = deck.scrollTop + deck.clientHeight / 2, cur = slides[0];
    for (var i = 0; i < slides.length; i++){ if (slides[i].offsetTop <= mid) cur = slides[i]; }
    return cur;
  }
  function update(){
    var s = current(); if (s === last) return; last = s;
    /* v6: on a hidden or unmapped slide the rail keeps the FIRST chapter's exact state -
       layout, grown circle, theme - so entering chapter 1 is a pure fade, no movement */
    var hidden = RAIL.hideOn.indexOf(s.id) > -1 || !byId[s.id];
    var eff = hidden ? (document.getElementById(RAIL.chapters[0].id) || s) : s;
    nav.classList.toggle('is-hidden', hidden);
    nav.classList.toggle('is-dark', eff.classList.contains('dark'));
    nav.classList.toggle('is-grey', eff.classList.contains('grey'));
    Array.prototype.forEach.call(nav.querySelectorAll('.is-cur,.is-grp'), function(n){ n.classList.remove('is-cur'); n.classList.remove('is-grp'); });
    Array.prototype.forEach.call(nav.querySelectorAll('[aria-current]'), function(n){ n.removeAttribute('aria-current'); });
    var m = byId[eff.id];
    if (m){
      m.ch.classList.add('is-cur');
      Array.prototype.forEach.call(nav.querySelectorAll('.cr-sub[data-ch="' + m.ch.getAttribute('data-ch') + '"]'),
        function(n){ n.classList.add('is-grp'); });
      if (m.sub) m.sub.classList.add('is-cur');
      if (!hidden) (m.sub || m.ch).firstChild.setAttribute('aria-current', 'step');
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
def build(src, dst, chapters, must=('you can bank on',)):
    h = open(src, encoding='utf-8').read()
    anchor = '<p class="keyhint" id="keyhint">'
    assert h.count(anchor) == 1 and h.count('</body>') == 1 and 'data-lane="296-C"' not in h
    i = h.index(anchor); j = h.index('\n', i) + 1
    h = h[:j] + STYLE + h[j:]
    h = h.replace('</body>', SCRIPT.replace('__CHAPTERS__', chapters) + '</body>')
    for m in must: assert m in h, 'missing: ' + m
    open(dst, 'w', encoding='utf-8').write(h)
    print('wrote', dst, len(h.encode()))

# v8 (#297 lane D): Dave 2026-09-23 08:50, "I want a new chapter called evolution after evaluation, that stars with
# slide 07". Evolution runs 07-13 (s6 ... s10map); Evaluation keeps 06 (s4p) alone. Six chapters, the same 14 items.
# v9 (#299 lane C): Dave 2026-09-23 13:34, the order of play's "The result" -> "Result"; the rail follows it (his
# standing rule: the order of play matches the tracker). Only chapter 5's title changes.
# v10 (#302 lane B): Dave 2026-09-24 11:28, "I want to add another slide probably between 11 and 12, but you might have
# other ideas: Benefits beyond speed, quality and consistency". Placed after the demo (s9) as Result's one sub,
# s11pre; the chapters and the order of play are unchanged. 17 slides.
PLAIN_CHAPTERS = '''  chapters: [
    {n:1, title:'Problem',     id:'s3',  subs:[]},
    {n:2, title:'Research',    id:'s5x', subs:['s5r']},
    {n:3, title:'Evaluation',  id:'s4p', subs:[]},
    {n:4, title:'Evolution',   id:'s6',  subs:['s7','s8','s7b','s6b','s10','s10map']},
    {n:5, title:'Result',      id:'s9',  subs:['s11pre']},
    {n:6, title:'The ask',     id:'s11', subs:['s12']}
  ]
'''

if __name__ == '__main__':
    build(SRC, DST, PLAIN_CHAPTERS)
