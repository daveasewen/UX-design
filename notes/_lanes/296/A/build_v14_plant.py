# 296 lane A: v13 -> v14-plant. Idempotent from a fresh cp of ref/v13.html; asserts on every anchor.
import io, re, sys
SRC = '/home/claude/296/ref/v13.html'
OUT = '/home/claude/296/A/_DEMO-SLIDES-apollo-2026-09-22-v14-plant.html'
s = io.open(SRC, encoding='utf-8').read()

def rep(old, new, count=1):
    global s
    n = s.count(old)
    assert n == count, (n, old[:90])
    s = s.replace(old, new)

# --- title + head note
rep('<title>Apollo — demo cards — v11</title>', '<title>Apollo — demo cards — v14 plant</title>')
rep('<!DOCTYPE html>', '<!-- v14-plant · #296 lane A · 2026-09-22 · copied from v13, re-ordered to Dave\'s run order of 2026-09-22:\n     cover · agenda · observation · systemised design · experiment · insight (new) · breakdown (new) ·\n     first improvement · shared brain · QC · live build · anatomy · map · ask · close. 15 cards. -->\n<!DOCTYPE html>')

# --- s2 agenda
rep('''    <p class="label rv">How this goes</p>
    <h2 class="rv d1" style="font-size:clamp(28px,3vw,40px);margin-bottom:var(--s5);max-width:22em;text-wrap:balance">
      A custom shop that builds at the speed of a car&nbsp;plant.</h2>
    <ol class="chapters rv d2">
      <li><span class="n">1</span><b>Why now</b></li>
      <li><span class="n">2</span><b>The line</b></li>
      <li><span class="n">3</span><b>The robots</b></li>
      <li><span class="n">4</span><b>What we built<em>the inventory &middot; the assembly engineer &middot; the inspector</em></b></li>
      <li><span class="n">5</span><b>The build and the ask</b></li>
    </ol>''', '''    <p class="label rv">How this goes</p>
    <h2 class="rv d1" style="font-size:clamp(28px,3vw,40px);margin-bottom:var(--s5);max-width:22em;text-wrap:balance">
      What you&rsquo;ll see in the next 15&ndash;20&nbsp;minutes.</h2>
    <ol class="chapters rv d2">
      <li><span class="n">1</span><b>Why now</b></li>
      <li><span class="n">2</span><b>Systemised design</b></li>
      <li><span class="n">3</span><b>The experiment</b></li>
      <li><span class="n">4</span><b>The insight</b></li>
      <li><span class="n">5</span><b>The breakdown<em>speed &middot; consistency &middot; quality</em></b></li>
      <li><span class="n">6</span><b>What we built<em>the parts &middot; the shared brain &middot; QC</em></b></li>
      <li><span class="n">7</span><b>The build and the ask</b></li>
    </ol>''')
rep('#s2 .chapters{grid-template-columns:repeat(5,1fr);gap:var(--s3) var(--s4);}',
    '#s2 .chapters{grid-template-columns:repeat(4,1fr);gap:var(--s3) var(--s4);}   /* v14: seven chapters, 4 + 3 */')

# --- s3 eyebrow
rep('''    <p class="label rv">Why now</p>
    <h2 class="rv d1"><b>Dev got fast.</b></h2>''', '''    <p class="label rv">The observation</p>
    <h2 class="rv d1"><b>Dev got fast.</b></h2>''')

# --- s4: the metaphor as an intro only; observations move to the insight card
rep('''      <p class="label rv">The line</p>
      <h2 class="rv d1">An assembly line is only as fast as its parts bin, the skill of the assembly engineer, and the rigour of&nbsp;QC.</h2>
      <p class="lead rv d2">Ours: a parts bin that is too small, engineers with dramatically different skill levels, and QC that is rigorous but slow.</p>
      <p class="body rv d3">No one has the full picture. Missing parts are machined all the time, by engineers without the skills to do so. The builds are unreliable and they go back down the line to be repaired.</p>''',
'''      <p class="label rv">Systemised design</p>
      <h2 class="rv d1">An assembly line is only as fast as its parts bin, the skill of the assembly engineer, and the rigour of&nbsp;QC.</h2>
      <p class="lead rv d2">A design system is a line like this. The parts bin is our components, the assembly engineers are our designers, and QC checks every build before it ships.</p>''')

# --- NEW insight + breakdown cards, inserted between s5 and s6
NEW = '''<!-- ===== 6 · NEW v14 · The insight — the observations lifted off old s4 ===== -->
<section class="slide grey" id="s5insight">
  <div class="inner">
    <p class="label rv">The insight</p>
    <h2 class="rv d1">The robots didn&rsquo;t create the problems.<br><b>They made them obvious.</b></h2>
    <div class="grid4 ins">
      <div class="rv d2"><p class="ix">01 &middot; The parts bin</p><h3>Too small.</h3><p>Missing parts are machined all the time, by engineers without the skills to do&nbsp;so.</p></div>
      <div class="rv d2"><p class="ix">02 &middot; The engineers</p><h3>Dramatically different skill&nbsp;levels.</h3><p>No one has the full&nbsp;picture.</p></div>
      <div class="rv d3"><p class="ix">03 &middot; QC</p><h3>Rigorous but slow.</h3><p>Unreliable builds go back down the line to be&nbsp;repaired.</p></div>
    </div>
    <p class="foot rv d4">The same failures, human or robot.</p>
  </div>
  <div class="pagenum">06 / 15</div>
</section>

<!-- ===== 7 · NEW v14 · The breakdown — Dave's whiteboard, rebuilt slide-native ===== -->
<section class="slide" id="s5break">
  <div class="inner">
    <p class="label rv">The breakdown</p>
    <h2 class="rv d1">This confirmed what we always knew.<br><b>Now there is a chance to solve three things at&nbsp;once.</b></h2>
    <div class="bd rv d2" aria-label="Current problems: speed, consistency and quality, their causes, and what Apollo introduces">
      <div class="bd-row bd-heads">
        <div class="bd-h sp"><span>01</span>Speed</div>
        <div class="bd-h co"><span>02</span>Consistency</div>
        <div class="bd-h qu"><span>03</span>Quality</div>
      </div>
      <div class="bd-row bd-causes">
        <div class="bd-g sp"><p class="bd-gl">Speed</p><ul><li>Governance process</li><li>2 stage process (Figma + Code library)</li></ul></div>
        <div class="bd-g co"><p class="bd-gl">All three</p><ul><li>Small component library</li><li>Lack of design standards and accessibility knowledge</li><li>Low/variable skills</li></ul></div>
        <div class="bd-g qu"><p class="bd-gl">Quality</p><ul><li>Lack of data and research</li><li>AI generation quality (Slop)</li></ul></div>
      </div>
      <div class="bd-join" aria-hidden="true"></div>
      <div class="bd-ai"><span>Introduce AI to build solutions</span></div>
      <div class="bd-stem" aria-hidden="true"></div>
      <div class="bd-row bd-out">
        <div class="bd-apollo"><p class="bd-name">Apollo</p><ul><li>Gates and evals</li><li>Full library in code</li><li>A graph that holds all the tokens, components, standards and compliance</li></ul></div>
        <div class="bd-link" aria-hidden="true"></div>
        <div class="bd-research"><p class="bd-gl">Another group&rsquo;s work</p><ul><li>Research graph?</li></ul></div>
      </div>
    </div>
  </div>
  <div class="pagenum">07 / 15</div>
</section>

<style data-lane="296A">
/* v14 · the insight card: the .grid4 idiom of s10, three-up, no pictures */
#s5insight .grid4.ins{grid-template-columns:repeat(3,1fr);margin-top:var(--s5)}
#s5insight .grid4.ins h3{font-size:24px;line-height:1.3}
#s5insight .grid4.ins p:not(.ix){font-size:16px;line-height:1.6}
#s5insight h2{font-size:clamp(30px,3.6vw,48px)}
/* v14 · the breakdown: Dave's whiteboard in the deck's own palette. The three
   problems are told apart by label and rule weight, not by hue: speed takes the
   accent (the deck's one colour), consistency black, quality mid-grey dashed. */
#s5break h2{font-size:clamp(24px,2.5vw,34px);line-height:1.15;margin-bottom:var(--s4)}
#s5break .bd{--sp:var(--accent);--co:var(--black);--qu:var(--g6);font-size:14px;line-height:1.45}
#s5break .bd-row{display:grid;grid-template-columns:1fr 1.35fr 1fr;gap:var(--s3)}
#s5break .bd-h{border-top:3px solid;padding-top:10px;font-weight:600;font-size:18px;line-height:1.35}
#s5break .bd-h span{display:block;font-size:12px;font-weight:500;letter-spacing:.14em;line-height:1.5;margin-bottom:2px}
#s5break .bd-h.sp{border-color:var(--sp)} #s5break .bd-h.sp span{color:var(--sp)}
#s5break .bd-h.co{border-color:var(--co)} #s5break .bd-h.co span{color:var(--co)}
#s5break .bd-h.qu{border-top-style:dashed;border-color:var(--qu)} #s5break .bd-h.qu span{color:var(--g7)}
#s5break .bd-causes{margin-top:var(--s2)}
#s5break .bd-g{border:1px solid var(--g3);padding:12px 14px 14px;background:var(--white)}
#s5break .bd-g.sp{border-left:3px solid var(--sp)}
#s5break .bd-g.co{background:var(--g1);border:1px dashed var(--g5)}
#s5break .bd-g.qu{border-left:3px dashed var(--qu)}
#s5break .bd-gl{margin:0 0 6px;font-size:11px;font-weight:500;letter-spacing:.14em;text-transform:uppercase;color:var(--g6);line-height:1.5}
#s5break .bd-g.sp .bd-gl{color:var(--sp)}
#s5break ul{list-style:none;margin:0;padding:0}
#s5break li{padding:5px 0;border-top:1px solid var(--g2);color:var(--g8)}
#s5break li:first-child{border-top:0;padding-top:0}
#s5break .bd-g.co li{border-top-color:var(--g3)}
/* the three groups converge: a rule under all three, a stem down to the AI step */
#s5break .bd-join{height:18px;margin:0 14.3%;border:1px solid var(--g5);border-top:0}
#s5break .bd-ai{display:flex;justify-content:center;position:relative}
#s5break .bd-ai::before{content:"";position:absolute;left:50%;top:-18px;height:18px;border-left:1px solid var(--g5)}
#s5break .bd-ai span{display:inline-block;margin-top:0;padding:9px 22px;border:1px solid var(--black);border-radius:999px;
  font-weight:600;font-size:15px;line-height:1.4;background:var(--white)}
#s5break .bd-stem{width:0;height:18px;margin:0 auto;border-left:1px solid var(--g5)}
#s5break .bd-out{grid-template-columns:3.35fr 36px 1fr;gap:0;align-items:stretch}
#s5break .bd-apollo{background:var(--black);color:var(--white);padding:12px 16px 14px;display:grid;
  grid-template-columns:auto 1fr 1fr 1.6fr;gap:var(--s3);align-items:start}
#s5break .bd-apollo .bd-name{margin:0;font-size:24px;font-weight:600;line-height:1.2;color:var(--accent-dark)}
#s5break .bd-apollo ul{display:contents}
#s5break .bd-apollo li{border-top:0;border-left:1px solid var(--g7);padding:0 0 0 12px;color:var(--white)}
#s5break .bd-link{align-self:center;border-top:1px dashed var(--g5);height:0}
#s5break .bd-research{border:1px dashed var(--g5);padding:12px 14px 14px}
#s5break .bd-research li{font-weight:600}
@media print{ #s5break h2{font-size:26px} #s5insight h2{font-size:38px} #s5break .bd{font-size:12.5px} }
</style>

<!-- ===== 6 · The inventory'''
rep('<!-- ===== 6 · The inventory', NEW)

# --- old s6 -> 08: the first improvement
rep('''      <p class="label rv">The inventory · what she builds with</p>
      <h2 class="rv d1"><b>36 &rarr; 137.</b> Now there is no need to machine parts.</h2>
      <p class="lead rv d2">First we focused on the inventory: 125 components, 12 templates, 8 foundations &mdash; 101 new &mdash; each one in code, built to our design and accessibility standards.</p>
      <p class="switch rv d3">Switch to the library</p>
      <p class="foot rv d4">Source: showroom/index.json, read 2026-09-19. Growing.</p>''',
'''      <p class="label rv">The parts bin</p>
      <h2 class="rv d1">The first improvement: <b>the catalogue went from 36&nbsp;to&nbsp;137.</b></h2>
      <p class="lead rv d2">125 components, 12 templates, 8 foundations &mdash; 101 new &mdash; each one in code, built to our design and accessibility standards. Now there is no need to machine parts.</p>
      <p class="switch rv d3">Switch to the library</p>
      <p class="foot rv d4">Source: showroom/index.json, read 2026-09-22. Growing.</p>''')

# --- old s7 -> 09: the shared brain first, then the custom shop
rep('''      <p class="label rv">The assembly engineer · what she knows</p>
      <h2 class="rv d1">A custom shop that builds <b>at the speed of a car plant.</b></h2>
      <p class="lead rv d2">Each product is custom designed and built &mdash; so we needed the knowledge of a designer and an assembly engineer embedded in the system too.</p>''',
'''      <p class="label rv">The shared brain · what she knows</p>
      <h2 class="rv d1">The robots needed<br><b>a shared brain.</b></h2>
      <p class="lead rv d2">A custom shop that builds at the speed of a car plant &mdash; so the knowledge of a designer and an assembly engineer is embedded in the system too.</p>''')

# --- old s8 -> 10: the same brain rechecks the work
rep('''      <p class="lead rv d2">Quality is built into the parts and the assembly is powered by a vast knowledge base &mdash; and the inspector still checks every build.</p>''',
'''      <p class="lead rv d2">Quality is built into the parts, and the same brain that guides the build rechecks the work &mdash; every build, before it ships.</p>''')

# --- pagenums: position -> NN / 15
order = ['s1','s2','s3','s4','s5','s5insight','s5break','s6','s7','s8','s9','s10','s10map','s11','s12']
secs = re.findall(r'<section class="slide[^"]*" id="([^"]+)"', s)
assert secs == order, secs
for i, sid in enumerate(order, 1):
    a = s.index('id="%s"' % sid)
    b = s.index('<div class="pagenum">', a)
    e = s.index('</div>', b)
    s = s[:b] + '<div class="pagenum">%02d / 15' % i + s[e:]
assert len(re.findall(r'class="pagenum">\d\d / 15<', s)) == 15
io.open(OUT, 'w', encoding='utf-8').write(s)
print('ok', len(s.encode('utf-8')))
