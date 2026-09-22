# Lane 296-B2: s4p -> five causes; s5x -> the experiment loop from the archive spec v0.2.
# Idempotent: always rebuilds from the saved before-copy. Touches only s4p/s5x markup and their scoped rules.
import re
SRC = 'notes/_lanes/296/B2/v14-plain-before-b2.html'
DST = 'notes/_DEMO-SLIDES-apollo-2026-09-22-v14-plain.html'
s = open(SRC, encoding='utf-8').read()

def swap(old, new):
    global s
    assert s.count(old) == 1, (s.count(old), old[:80])
    s = s.replace(old, new)

# ---------- s4p markup ----------
a = s.index('<section class="slide" id="s4p">'); b = s.index('</section>', a) + len('</section>')
swap(s[a:b], '''<section class="slide" id="s4p">
  <div class="inner">
    <p class="label rv">Problem &middot; speed</p>
    <h2 class="rv d1">Why is design slow? <b>Five causes.</b></h2>
    <div class="c5 rv d2">
      <p class="grp sp">Speed</p>
      <p class="grp all">All &middot; shared with consistency and quality</p>
      <div><p class="ix">01</p><h3>Governance process</h3><p>It is a queue. Every component waits its turn for review.</p></div>
      <div><p class="ix">02</p><h3>2 stage process (Figma + Code&nbsp;library)</h3><p>Every component is designed twice: once in Figma, once in code.</p></div>
      <div><p class="ix">03</p><h3>Small component library</h3><p>Too few parts, so designers draw the rest from scratch.</p></div>
      <div><p class="ix">04</p><h3>Lack of design standards and accessibility knowledge</h3><p>With no written rules, each decision is made again, and accessibility is fixed late.</p></div>
      <div><p class="ix">05</p><h3>Low/variable skills</h3><p>How good and how fast the work is depends on who picks it up.</p></div>
    </div>
    <p class="foot rv d3">From the whiteboard: Current problems &rarr; Speed, which runs into its own group and into All.</p>
  </div>
  <div class="pagenum">04 / 15</div>
</section>''')

# ---------- s5x markup ----------
a = s.index('<section class="slide grey" id="s5x">'); b = s.index('</section>', a) + len('</section>')
swap(s[a:b], '''<section class="slide grey" id="s5x">
  <div class="inner">
    <p class="label rv">Analysis &middot; the experiment</p>
    <h2 class="rv d1">Built only from the 36 components. <b>Then the work, and the output, checked.</b></h2>
    <p class="lead rv d2">The agent never invents a part. Anything missing is raised as a gap &mdash; never improvised.</p>
    <div class="xl rv d3">
      <ol class="steps">
        <li class="k1"><p class="sh">1 &middot; Intake</p><p class="sb">The brief, its jobs and assumptions.</p></li>
        <li class="k2 blk"><p class="sh">2 &middot; Criteria contract</p><p class="sb">Success and failure written as executable checks.</p><p class="st">&rarr; the gates</p></li>
        <li class="k3"><p class="sh">3 &middot; Generate &times;&nbsp;N</p><p class="sb">N variants, built from the 36 components only.</p><p class="st">from canon only</p></li>
        <li class="k4 blk"><p class="sh">4 &middot; Objective gates</p><p class="sb">Contrast &middot; a11y &middot; tokens &middot; states. Kill the broken.</p><p class="st">checks the work</p></li>
        <li class="k5 red"><p class="sh">5 &middot; Taste + test</p><p class="sb">Human + users pick the winner.</p><p class="st">checks the output</p></li>
        <li class="k6"><p class="sh">6 &middot; Prototype</p><p class="sb">Tuned, with a handoff spec.</p></li>
      </ol>
      <div class="regen" aria-label="A step that fails a gate goes back to generate"><span class="tip" aria-hidden="true"></span><span class="rl">fail a gate &rarr; regenerate</span></div>
    </div>
    <p class="foot rv d4">June&ndash;July 2026: one brief, two arms &mdash; governed and ungoverned &mdash; both on Opus.</p>
  </div>
  <div class="pagenum">05 / 15</div>
</section>''')

# ---------- scoped rules inside the 296-B style block ----------
st = s.index('<style data-lane="296-B">'); en = s.index('</style>', st)
blk = s[st:en]
old_rules = re.search(r'#s4p \.pb\{.*?#s5x \.loop \.back\{[^\n]*\n', blk, re.S).group(0)
new_rules = '''/* 296-B2: five causes, grouped 2 + 3 as the whiteboard's Speed arrow splits (Speed | All). */
#s4p h2{margin-bottom:var(--s4)}
#s4p .c5{display:grid;grid-template-columns:repeat(5,1fr);column-gap:var(--s3)}
#s4p .grp{margin:0;font-size:12px;font-weight:500;letter-spacing:.14em;text-transform:uppercase;line-height:1.5;
  padding-bottom:var(--s1);border-bottom:3px solid var(--accent);color:var(--accent)}
#s4p .grp.sp{grid-column:1/3}
#s4p .grp.all{grid-column:3/6;border-bottom-color:var(--g8);color:var(--g8)}
#s4p .c5>div{padding:var(--s3) 0 var(--s2)}
#s4p .c5 .ix{font-size:12px;letter-spacing:.14em;color:var(--accent);font-weight:500;margin:0 0 var(--s2);line-height:1.5}
#s4p .c5 h3{font-size:clamp(18px,1.55vw,22px);font-weight:600;line-height:1.3;margin:0 0 var(--s2)}
#s4p .c5 div p:last-child{font-size:clamp(15px,1.15vw,17px);line-height:1.5;color:var(--g7);margin:0}
#s4p .foot{margin-top:var(--s4)}
/* 296-B2: the experiment loop, rebuilt from archive/apollo-pipeline-spec_v0.2 (diagram 0). */
#s5x h2{max-width:21em;font-size:clamp(32px,3.7vw,54px)}
#s5x .lead{font-size:clamp(17px,1.5vw,21px);max-width:40em;margin-top:var(--s2)}
#s5x .xl{--gap:26px;position:relative;margin-top:var(--s4);padding-bottom:76px}
#s5x .steps{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(6,1fr);column-gap:var(--gap)}
#s5x .steps li{position:relative;background:var(--white);border:1.5px solid var(--g3);display:flex;flex-direction:column}
#s5x .steps li+li::before{content:"";position:absolute;left:calc(-1 * var(--gap) - 1.5px);top:28px;width:calc(var(--gap) - 7px);
  height:0;border-top:1.5px solid var(--g7)}
#s5x .steps li+li::after{content:"";position:absolute;left:-8px;top:24px;border:5px solid transparent;border-left:7px solid var(--g7);border-right:0}
#s5x .sh{margin:0;padding:10px 12px;font-size:11.5px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;line-height:1.4;
  background:var(--g2);color:var(--black);min-height:calc(2.8em + 20px);box-sizing:border-box}
#s5x .blk{border-color:var(--black)} #s5x .blk .sh{background:var(--black);color:var(--white)}
#s5x .red{border-color:var(--accent)} #s5x .red .sh{background:var(--accent);color:var(--white)}
#s5x .k5::before{border-top-color:var(--accent)!important} #s5x .k5::after{border-left-color:var(--accent)!important}
#s5x .sb{margin:0;padding:12px 12px 6px;font-size:clamp(14px,1.1vw,16px);line-height:1.45;color:var(--g8);flex:1}
#s5x .st{margin:0;padding:0 12px 12px;font-size:12px;font-style:italic;line-height:1.5;color:var(--g6)}
#s5x .k4 .st,#s5x .k5 .st{color:var(--accent);font-style:normal;font-weight:500;letter-spacing:.04em}
/* regenerate: from under step 4 back up into step 3 (centre to centre of columns 3 and 4) */
#s5x .regen{position:absolute;bottom:30px;height:36px;border:2px dashed var(--accent);border-top:0;
  left:calc((100% - 5 * var(--gap)) / 6 * 2.5 + var(--gap) * 2);right:calc((100% - 5 * var(--gap)) / 6 * 2.5 + var(--gap) * 2)}
#s5x .regen .tip{position:absolute;left:-7px;top:-12px;border:6px solid transparent;border-bottom:10px solid var(--accent);border-top:0}
#s5x .regen .rl{position:absolute;left:50%;top:calc(100% + 6px);transform:translateX(-50%);white-space:nowrap;
  padding:0;font-size:13px;font-weight:500;letter-spacing:.04em;line-height:1.5;color:var(--accent)}
'''
blk2 = blk.replace(old_rules, new_rules)
blk2 = blk2.replace('#s4p .pb h3{font-size:22px} #s5x .loop b{font-size:20px}',
                    '#s4p .c5 h3{font-size:18px} #s4p .c5 div p:last-child{font-size:14px} #s5x h2{font-size:40px} #s5x .sb{font-size:13px}')
assert blk2 != blk
s = s[:st] + blk2 + s[en:]
open(DST, 'w', encoding='utf-8').write(s)
print('ok', len(s.encode()))
