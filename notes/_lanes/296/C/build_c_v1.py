# #296 lane C - chapter rail (orientation pattern) into the v14-plain deck.
# Inserts ONE <style data-lane="296-C">, ONE <nav id="chrail">, ONE <script data-lane="296-C">.
# Idempotent: rebuilds from notes/_lanes/296/C/v14-plain-before-c.html every run.
import os
R = os.path.abspath('.') + '/'
SRC = R + 'notes/_lanes/296/C/v14-plain-before-c.html'
DST = R + 'notes/_DEMO-SLIDES-apollo-2026-09-22-v14-plain.html'
h = open(SRC, encoding='utf-8').read()

STYLE = r'''<style data-lane="296-C">
/* #296 lane C - THE CHAPTER RAIL (orientation pattern).
   Dave: "a vertical timeline style progress indicator with circles indicating
   the chapters and smaller filled dots indicating any sub-pages ... persistent
   and not scroll with the slides ... the position indicator should grow to be
   a larger circle with the chapter number inside and the chapter title to the
   right ... I want to see them [the other titles] very tiny in the first version."
   Fixed, outside .deck, so it never moves with the slides. Every row has a fixed
   height and the nav a fixed width, so its box is identical on every slide. */
#chrail{--rk:var(--black);--rk2:var(--g6);--rdot:var(--g5);--rground:var(--white);--racc:var(--accent);
  position:fixed;left:16px;top:50%;transform:translateY(-50%);z-index:120;width:200px;margin:0;padding:0;
  font-family:var(--font);pointer-events:none;opacity:1;transition:opacity .2s var(--ease);}
#chrail.is-grey{--rground:var(--g1);}
#chrail.is-dark{--rk:var(--white);--rk2:var(--g5);--rdot:var(--g6);--rground:var(--black);--racc:var(--accent-dark);}
#chrail.is-hidden{opacity:0;}
#chrail.is-hidden .cr-row{pointer-events:none;}
#chrail ol{list-style:none;margin:0;padding:0;position:relative;}
/* the thin vertical line, through the centre of the 28px marker column */
#chrail ol::before{content:"";position:absolute;left:13.5px;top:15px;bottom:8px;width:1px;background:var(--rk2);opacity:.55;transition:background .2s;}
#chrail li{margin:0;padding:0;}
#chrail .cr-row{display:flex;align-items:center;gap:10px;height:30px;padding:0;margin:0;border:0;background:none;
  cursor:pointer;pointer-events:auto;font:inherit;color:var(--rk);text-align:left;}
#chrail .cr-sub .cr-row{height:16px;}
#chrail .cr-mk{flex:0 0 28px;height:28px;display:flex;align-items:center;justify-content:center;}
#chrail .cr-sub .cr-mk{height:16px;}
/* chapter: hollow circle */
#chrail .cr-c{width:10px;height:10px;border-radius:50%;border:1px solid var(--rk);background:var(--rground);
  display:flex;align-items:center;justify-content:center;font-size:0;font-weight:500;color:var(--rk);line-height:1;
  transition:width .2s var(--ease),height .2s var(--ease),font-size .2s var(--ease),border-color .2s,background .2s,color .2s;}
/* sub-page: smaller filled dot */
#chrail .cr-d{width:5px;height:5px;border-radius:50%;background:var(--rdot);
  transition:width .2s var(--ease),height .2s var(--ease),background .2s;}
/* titles: very tiny for the others (flag: tinyTitles) */
#chrail .cr-t{font-size:7px;font-weight:500;letter-spacing:.12em;text-transform:uppercase;color:var(--rk2);
  line-height:1.4;white-space:nowrap;display:flex;align-items:center;gap:6px;
  transition:font-size .2s var(--ease),color .2s;}
#chrail.no-tiny .cr-ch:not(.is-cur) .cr-t{display:none;}
#chrail .cr-t::before{content:"";width:0;height:1px;background:var(--racc);transition:width .2s var(--ease);}
/* THE CURRENT CHAPTER: larger circle, number inside, title to the right, red rule */
#chrail .cr-ch.is-cur .cr-c{width:28px;height:28px;font-size:12px;border-color:var(--rk);}
#chrail .cr-ch.is-cur > .cr-row .cr-t{font-size:12px;letter-spacing:.14em;color:var(--racc);}
#chrail .cr-ch.is-cur > .cr-row .cr-t::before{width:16px;}
/* the current sub-page's own dot */
#chrail .cr-sub.is-cur .cr-d{width:9px;height:9px;background:var(--racc);}
#chrail .cr-row:focus-visible{outline:1px solid var(--racc);outline-offset:2px;}
@media (prefers-reduced-motion:reduce){ #chrail, #chrail *{transition:none !important;} }
@media print{ #chrail{display:none !important;} }
</style>
<nav id="chrail" class="is-hidden" aria-label="Chapters"></nav>
'''

SCRIPT = r'''<script data-lane="296-C">
/* #296 lane C - the chapter rail. RAIL is the only thing to edit:
   a chapter is {n, title, id, subs:[ids]}; ids are the slides' own ids.
   The rail follows DOM order; the current slide is found by POSITION
   (the deck's own rule: which slide the scroll top sits on). */
var RAIL = {
  hideOn:     ['s1'],      // rail hidden on these slides (cover); shown everywhere else
  tinyTitles: true,        // first version: every chapter title shown, very tiny
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
  var ol = document.createElement('ol'), byId = {};
  function row(li, id, label, inner){
    var b = document.createElement('button');
    b.type = 'button'; b.className = 'cr-row'; b.setAttribute('aria-label', label);
    b.innerHTML = inner;
    b.addEventListener('click', function(){
      var s = document.getElementById(id); if (s) s.scrollIntoView({behavior:'smooth'});
    });
    li.appendChild(b); ol.appendChild(li);
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
  var last = null;
  function current(){
    var top = deck.scrollTop + deck.clientHeight / 2, cur = slides[0];
    for (var i = 0; i < slides.length; i++){ if (slides[i].offsetTop <= top) cur = slides[i]; }
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
