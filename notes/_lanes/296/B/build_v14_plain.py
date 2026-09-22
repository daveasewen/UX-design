#!/usr/bin/env python3
"""#296 lane B - v14 PLAIN: v13 re-told structure-first, no car-plant metaphor.
Run from a fresh cp of ref/v13.html. Asserts on every anchor; refuses a second pass."""
import io, re, sys
F = '/home/claude/296/B/_DEMO-SLIDES-apollo-2026-09-22-v14-plain.html'
s = io.open(F, encoding='utf-8').read()
assert 'v14-plain' not in s, 'already built'
N = 15

def one(old, new):
    global s
    assert s.count(old) == 1, ('anchor count', s.count(old), old[:80])
    s = s.replace(old, new)

# ---- 1 · slides 2..9 are re-told as one block (s6/s7/s8 canvases kept byte-for-byte)
a = s.index('<!-- ===== 2 · The strip')
b = s.index('<!-- ===== 10 - What she is made of')
NEW = '''<!-- ===== v14-plain (#296 lane B) · 2 · What you'll see — six beats, no metaphor ===== -->
<section class="slide" id="s2">
  <div class="invert"></div>
  <div class="lift"></div>
  <img id="kgPrint2" alt="">
  <div class="inner">
    <p class="label rv">How this goes</p>
    <h2 class="rv d1" style="font-size:clamp(28px,3vw,40px);margin-bottom:var(--s5);max-width:22em;text-wrap:balance">
      What you&rsquo;ll see in the next 15&ndash;20&nbsp;minutes.</h2>
    <ol class="chapters rv d2" style="grid-template-columns:repeat(6,1fr)">
      <li><span class="n">1</span><b>Observation<em>dev got fast</em></b></li>
      <li><span class="n">2</span><b>Problem<em>why design is slow</em></b></li>
      <li><span class="n">3</span><b>Analysis<em>breaking it down</em></b></li>
      <li><span class="n">4</span><b>Experiment<em>agentic loops</em></b></li>
      <li><span class="n">5</span><b>Results<em>what we saw</em></b></li>
      <li><span class="n">6</span><b>Response<em>the library &middot; the graph</em></b></li>
    </ol>
  </div>
  <div class="pagenum">02 / 15</div>
</section>

<!-- ===== 3 · Observation — v13 s3, label only re-named ===== -->
<section class="slide dark" id="s3">
  <div class="inner">
    <p class="label rv">Observation</p>
    <h2 class="rv d1"><b>Dev got fast.</b></h2>
    <p class="lead rv d2">Build fast, test with real, shippable code. Design became the bottleneck.</p>
    <p class="lead rv d3" style="margin-top:var(--s3)">So we asked: how do we speed up design?</p>
    <p class="foot rv d4">That question was the first experiment.</p>
  </div>
  <div class="pagenum">03 / 15</div>
</section>

<!-- ===== 4 · Problem — the SPEED flow from Dave's whiteboard, broken down ===== -->
<section class="slide" id="s4p">
  <div class="inner">
    <p class="label rv">Problem &middot; speed</p>
    <h2 class="rv d1">Why is design slow? <b>Two causes.</b></h2>
    <div class="grid4 pb rv d2">
      <div><p class="ix">01</p><h3>Governance process</h3><p>It is a queue. Every component waits its turn for review.</p></div>
      <div><p class="ix">02</p><h3>2 stage process (Figma + Code&nbsp;library)</h3><p>Every component is designed twice: once in Figma, once in code.</p></div>
    </div>
    <p class="foot rv d3">From the whiteboard: Current problems &rarr; Speed.</p>
  </div>
  <div class="pagenum">04 / 15</div>
</section>

<!-- ===== 5 · Analysis + experiment — v13 s5, de-metaphored ===== -->
<section class="slide grey" id="s5x">
  <div class="inner">
    <p class="label rv">Analysis &middot; the experiment</p>
    <h2 class="rv d1">Could AI design and build in one step? <b>We tested it with agentic&nbsp;loops.</b></h2>
    <p class="lead rv d2">One brief, two arms &mdash; one governed, one not. In each, the agent:</p>
    <ol class="loop rv d3">
      <li><span class="ix">01</span><b>builds,</b></li>
      <li><span class="ix">02</span><b>checks its own work against the standards,</b></li>
      <li><span class="ix">03</span><b>and goes again.</b><span class="back" aria-hidden="true">&#8634;</span></li>
    </ol>
    <p class="foot rv d4">June&ndash;July 2026: one brief, two arms &mdash; governed and ungoverned &mdash; both on Opus.</p>
  </div>
  <div class="pagenum">05 / 15</div>
</section>

<!-- ===== 6 · Results — what was observed at that point (v13 s5's finding, de-metaphored) ===== -->
<section class="slide dark" id="s5r">
  <div class="inner">
    <p class="label rv">Results &middot; what we saw</p>
    <h2 class="rv d1">Where the component library was empty, <b>the agents invented parts &mdash; and got them&nbsp;wrong.</b></h2>
    <p class="lead rv d2">Our designers were doing exactly the same thing.</p>
    <p class="lead rv d3" style="margin-top:var(--s3)">The problem was always there. Automating it made it obvious.</p>
  </div>
  <div class="pagenum">06 / 15</div>
</section>

<!-- ===== 7 · Response 1 — the component library (v13 s6; the catalogue canvas, verbatim) ===== -->
<section class="slide" id="s6">
  <div class="inner">
    <div class="type">
      <p class="label rv">Response 1 &middot; the component library</p>
      <h2 class="rv d1"><b>The first improvement:</b> the catalogue went from 36 to&nbsp;137.</h2>
      <p class="lead rv d2">125 components, 12 templates, 8 foundations &mdash; 101 new &mdash; each one in code, built to our design and accessibility standards.</p>
      <p class="switch rv d3">Switch to the library</p>
      <p class="foot rv d4">Source: showroom/index.json, read 2026-09-22. Growing.</p>
    </div>
    <div class="draw rv d2">
      <canvas id="ct"></canvas>
      <img id="ctPrint" alt="">
    </div>
  </div>
  <div class="pagenum">07 / 15</div>
</section>

<!-- ===== 8 · The other two — consistency and quality; the whiteboard rebuilt slide-native ===== -->
<section class="slide grey" id="s6b">
  <div class="inner">
    <p class="label rv">Consistency and quality</p>
    <h2 class="rv d1">It confirmed what we always knew &mdash; <b>and a chance to solve three things at&nbsp;once.</b></h2>
    <div class="wb rv d2" aria-label="Current problems: speed, consistency and quality, and what they share">
      <div class="wb-h sp"><span>Speed</span></div>
      <div class="wb-h co"><span>Consistency</span></div>
      <div class="wb-h qu"><span>Quality</span></div>
      <svg class="wb-bus" viewBox="0 0 700 40" preserveAspectRatio="none" aria-hidden="true">
        <path d="M100 0V40M350 0V40M600 0V40M100 16H600" vector-effect="non-scaling-stroke"/>
      </svg>
      <div class="wb-g sp"><p class="gl">Speed</p><ul><li>Governance process</li><li>2 stage process (Figma + Code library)</li></ul>
        <p class="done">Addressed first &middot; the library</p></div>
      <div class="wb-g all"><p class="gl">All &middot; shared by all three</p><ul><li>Small component library</li><li>Lack of design standards and accessibility knowledge</li><li>Low/variable skills</li></ul></div>
      <div class="wb-g qu"><p class="gl">Quality</p><ul><li>Lack of data and research</li><li>AI generation quality (slop)</li></ul></div>
    </div>
    <div class="wb-out rv d3">
      <p class="ai">Introduce AI to build solutions <span aria-hidden="true">&rarr;</span></p>
      <div class="ap"><p class="gl">Apollo</p><ul><li>Gates and evals</li><li>Full library in code</li><li>A graph that holds all the tokens, components, standards and compliance</li></ul></div>
      <div class="rg"><p class="gl">Another group</p><ul><li>Research graph?</li></ul></div>
    </div>
  </div>
  <div class="pagenum">08 / 15</div>
</section>

<!-- ===== 9 · Response 2 — the knowledge graph joins it all (v13 s7; the brain canvas, verbatim) ===== -->
<section class="slide" id="s7">
  <div class="inner">
    <div class="type">
      <p class="label rv">Response 2 &middot; the knowledge graph</p>
      <h2 class="rv d1">The knowledge graph <b>joins it all together.</b></h2>
      <p class="lead rv d2">Standards, accessibility, rulings, governance, usage and theory &mdash; in one graph, retrieved at build time.</p>
      <p class="body rv d3">Every build comes with a record of account.</p>
      <p class="switch rv d4">Switch to the knowledge-graph explorer</p>
      <p class="foot rv d5">4,820 nodes &middot; 8,648 edges &middot; explorer builder 1.27, 2026-09-19.</p>
    </div>
    <div class="draw rv d2">
      <canvas id="br"></canvas>
      <img id="brPrint" alt="">
    </div>
  </div>
  <div class="pagenum">09 / 15</div>
</section>

<!-- ===== 10 · Gates and evals — the same graph rechecks the work (v13 s8; the callipers canvas, verbatim) ===== -->
<section class="slide" id="s8">
  <div class="inner">
    <div class="type">
      <p class="label rv">Response 2 &middot; gates and evals</p>
      <h2 class="rv d1">The same graph <b>rechecks the work.</b></h2>
      <p class="lead rv d2">Gates and evals are the quality control: every build is checked against the standards it was built from.</p>
      <p class="body rv d3">Corrections are made at the check, not sent back to the start.</p>
    </div>
    <div class="draw rv d2">
      <canvas id="cp"></canvas>
      <img id="cpPrint" alt="">
    </div>
  </div>
  <div class="pagenum">10 / 15</div>
</section>

<!-- ===== 11 · The build — v13 s9, plant words out ===== -->
<section class="slide dark" id="s9">
  <div class="inner">
    <p class="label rv">The build</p>
    <h2 class="rv d1"><b>Live build.</b></h2>
    <p class="lead rv d2">One cold, repeatable testing prompt. The build, the checks and the finished product, live.</p>
    <p class="switch rv d3">Switch to the editor</p>
    <p class="foot rv d4">Live and unedited, with the recording as the fallback.</p>
  </div>
  <div class="pagenum">11 / 15</div>
</section>

<style data-lane="296-B">
/* v14-plain: problem cells, the loop strip, and the whiteboard rebuilt. Scoped; no globals. */
#s4p .pb{grid-template-columns:repeat(2,1fr);margin-top:var(--s5);border-top:3px solid var(--accent)}
#s4p .pb>div{padding:var(--s4) var(--s4) var(--s5)}
#s4p .pb h3{font-size:clamp(22px,2vw,28px);line-height:1.3}
#s4p .pb p:last-child{font-size:clamp(17px,1.4vw,20px);line-height:1.5;margin-top:var(--s2)}
#s5x h2{max-width:20em}
#s5x .loop{list-style:none;margin:var(--s4) 0 0;padding:0;display:grid;grid-template-columns:repeat(3,1fr);
  border-top:1px solid var(--g3)}
#s5x .loop li{padding:var(--s3) var(--s4) 0 0;position:relative}
#s5x .loop li+li{padding-left:var(--s4);border-left:1px solid var(--g3)}
#s5x .loop .ix{display:block;font-size:12px;letter-spacing:.14em;color:var(--accent);font-weight:500;line-height:1.5;margin-bottom:var(--s2)}
#s5x .loop b{display:block;font-size:clamp(20px,1.8vw,26px);font-weight:400;line-height:1.35}
#s5x .loop .back{position:absolute;right:0;top:var(--s3);font-size:34px;line-height:1.2;color:var(--accent)}
#s5r h2{max-width:19em}

/* 8 · the whiteboard. Speed carries the accent (the board's red); consistency the
   black; quality mid-grey. The names carry the meaning; hue only repeats it. */
#s6b h2{font-size:clamp(28px,3vw,40px);max-width:24em;margin-bottom:var(--s4)}
#s6b .wb{display:grid;grid-template-columns:2fr 3fr 2fr;column-gap:0}
#s6b .wb-h{display:flex;justify-content:center;padding:0 var(--s2)}
#s6b .wb-h span{display:block;min-width:60%;text-align:center;font-size:13px;font-weight:600;letter-spacing:.1em;
  text-transform:uppercase;line-height:1.5;padding:8px 14px;color:var(--white)}
#s6b .wb-h.sp span{background:var(--accent)}
#s6b .wb-h.co span{background:var(--g8)}
#s6b .wb-h.qu span{background:var(--g6)}
#s6b .wb-bus{grid-column:1/-1;display:block;width:100%;height:28px}
#s6b .wb-bus path{fill:none;stroke:var(--g5);stroke-width:1.25}
#s6b .wb-g{margin:0 var(--s1);background:var(--white);border-top:3px solid var(--g6);padding:var(--s2) var(--s3) var(--s3)}
#s6b .wb-g.sp{border-top-color:var(--accent);margin-left:0}
#s6b .wb-g.all{border-top-color:var(--g8)}
#s6b .wb-g.qu{margin-right:0}
#s6b .gl{font-size:11px;font-weight:500;letter-spacing:.14em;text-transform:uppercase;color:var(--g6);line-height:1.5;margin:0 0 var(--s1)}
#s6b .wb-g.sp .gl{color:var(--accent)}
#s6b ul{list-style:none;margin:0;padding:0}
#s6b .wb-g li{font-size:15px;line-height:1.45;padding:7px 0;border-top:1px solid var(--g2)}
#s6b .wb-g li:first-child{border-top:0}
#s6b .wb-g.all ul{display:grid;grid-template-columns:repeat(3,1fr);column-gap:var(--s3)}
#s6b .wb-g.all li{border-top:0}
#s6b .done{margin:var(--s1) 0 0;font-size:12px;font-weight:500;letter-spacing:.06em;line-height:1.5;color:var(--accent)}
#s6b .done::before{content:"\\2713\\00a0"}
#s6b .wb-out{display:grid;grid-template-columns:auto 1fr auto;gap:var(--s3);align-items:stretch;margin-top:var(--s3);
  padding-top:var(--s3);border-top:1px solid var(--g3)}
#s6b .ai{margin:0;align-self:center;font-size:17px;font-weight:600;line-height:1.4;max-width:11em}
#s6b .ai span{color:var(--accent)}
#s6b .ap{background:var(--g8);color:var(--white);padding:var(--s2) var(--s3)}
#s6b .ap .gl{color:var(--accent-dark)}
#s6b .ap ul{display:grid;grid-template-columns:1fr 1fr 2fr;column-gap:var(--s3)}
#s6b .ap li,#s6b .rg li{font-size:14px;line-height:1.45}
#s6b .rg{border:1px dashed var(--g5);padding:var(--s2) var(--s3);color:var(--g7)}
@media print{
  #s6b h2{font-size:28px} #s6b .wb-g li{font-size:13px;padding:4px 0} #s6b .ap li,#s6b .rg li{font-size:12px}
  #s4p .pb h3{font-size:22px} #s5x .loop b{font-size:20px}
}
</style>

'''
s = s[:a] + NEW + s[b:]

# ---- 2 · s10: plant words out
one('<p>The inventory: 137 components in code.</p>', '<p>The library: 137 components in code.</p>')
one('Three roles in the story &mdash; the inventory, the assembly engineer, the inspector &mdash; and this is what the engineer is made of.',
    'Parts, knowledge and the judgement to compose from them.')

# ---- 3 · counters
for old, new in [('01 / 12', '01 / 15'), ('10 / 12', '12 / 15'), ('10A / 12', '13 / 15'),
                 ('11 / 12', '14 / 15'), ('12 / 12', '15 / 15')]:
    one('<div class="pagenum">%s</div>' % old, '<div class="pagenum">%s</div>' % new)

io.open(F, 'w', encoding='utf-8').write(s)
pn = re.findall(r'<div class="pagenum">([^<]*)</div>', s)
print(len(pn), pn)
