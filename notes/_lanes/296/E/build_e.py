# #296 lane E - the shells graph on s7, the brain to a new s7b (rest angle corrected).
# Rebuilds the lane-C SOURCE from notes/_lanes/296/E/v14-plain-before-e.html every run
# (idempotent), then the caller runs notes/_lanes/296/C/build_c.py to make the deck.
import os, re
R = os.path.abspath('.') + '/'
E = R + 'notes/_lanes/296/E/'
SRC = E + 'v14-plain-before-e.html'
DST = R + 'notes/_lanes/296/C/v14-plain-before-c.html'
h = open(SRC, encoding='utf-8').read()
def rep(old, new, n=1):
    global h
    assert h.count(old) == n, (h.count(old), old[:90])
    h = h.replace(old, new)

# 1 - CSS: #s7b gets every rule #s7 has; the shells print sits beside the brain's
rep('#s4,#s5,#s6,#s7,#s8{', '#s4,#s5,#s6,#s7,#s7b,#s8{')
for x in [' .inner', ' .type', ' h2', ' .lead', ' .body', ' .foot', ' .draw', ' canvas']:
    c = h.count('#s7' + x + ',')
    assert c >= 1, x
    h = h.replace('#s7' + x + ',', '#s7' + x + ',#s7b' + x + ',')
rep('#s7 #brPrint,', '#s7 #shlPrint,#s7b #brPrint,', 2)

# 2 - s7: the shells canvas in the brain's slot
rep('''      <canvas id="br"></canvas>
      <img id="brPrint" alt="">''', '''      <canvas id="shl"></canvas>
      <img id="shlPrint" alt="">''')
rep('<!-- ===== 9 · Response 2 — the knowledge graph joins it all (v13 s7; the brain canvas, verbatim) ===== -->',
    '<!-- ===== 9 · Response 2 — the knowledge graph joins it all (v13 s7; #296 E: the shells graph replaces the brain) ===== -->')

# 3 - s7b: the designer's brain, after gates and evals, before the breakdown
S7B = '''<!-- ===== 10b · The designer's brain (#296 lane E; the brain canvas moved here from s7, rest angle -50 / 20 / 33).
     Headline and lead are DRAFT FOR DAVE'S WORDS. ===== -->
<section class="slide" id="s7b">
  <div class="inner">
    <div class="type">
      <p class="label rv">The designer&rsquo;s brain</p>
      <h2 class="rv d1">Fourth: <b>a designer&rsquo;s judgement, built into the system.</b></h2>
      <p class="lead rv d2">The parts and the knowledge are not enough on their own &mdash; the brain is the judgement to compose from them, the way an experienced designer would.</p>
    </div>
    <div class="draw rv d2">
      <canvas id="br"></canvas>
      <img id="brPrint" alt="">
    </div>
  </div>
  <div class="pagenum">00 / 16</div>
</section>

'''
rep('<section class="slide grey" id="s6b">', S7B + '<section class="slide grey" id="s6b">')

# 4 - the brain IIFE: the drawing file's pass-nine rest (notes/_lanes/289/illustration/brain.html)
rep('  var HALF = (2*WMAX+GMAX)*1.15, AOV = 12;',
    '  /* #296 E: AOV 12 -> 33, from 289/illustration/brain.html PASS EIGHT (#292 B2). */\n'
    '  var HALF = (2*WMAX+GMAX)*1.15, AOV = 33;')
rep('  var YAW0 = 10*Math.PI/180, PIT0 = 8*Math.PI/180;',
    '  /* #296 E: the deck copy was three passes behind the drawing file. Pass nine\n'
    '     (#292 B3, 289/illustration/brain.html L474), ruled by Dave: YAW0 -50 / PIT0 20. */\n'
    '  var YAW0 = -50*Math.PI/180, PIT0 = 20*Math.PI/180;')
rep("    var s7el = document.getElementById('s7'); if (s7el) io7.observe(s7el);",
    "    var s7el = document.getElementById('s7b'); if (s7el) io7.observe(s7el);")
rep("  window.addEventListener('focus', function(){ var e=document.getElementById('s7'), r=e&&e.getBoundingClientRect(); if (r && r.bottom>0 && r.top<innerHeight) start(); });\n\n  /* v9 deck port: print — the resting frame, baked to the <img>. */",
    "  window.addEventListener('focus', function(){ var e=document.getElementById('s7b'), r=e&&e.getBoundingClientRect(); if (r && r.bottom>0 && r.top<innerHeight) start(); });\n\n  /* v9 deck port: print — the resting frame, baked to the <img>. */")

# 5 - the shells IIFE, straight after the brain's
anchor = "  window.brReady = true;\n})();\n"
rep(anchor, anchor + '\n' + open(E + 'shells-iife.js', encoding='utf-8').read())

# 6 - pagenums, by DOM order
pn = re.compile(r'<div class="pagenum">\d+ / \d+</div>')
tot = len(pn.findall(h)); assert tot == 16, tot
k = [0]
def num(m):
    k[0] += 1; return '<div class="pagenum">%02d / %d</div>' % (k[0], tot)
h = pn.sub(num, h)
open(DST, 'w', encoding='utf-8').write(h)
print('wrote', DST, len(h.encode()), 'pagenums', tot)
