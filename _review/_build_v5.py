#!/usr/bin/env python3
"""Build state-contrast-mono-preview-v5.html from v3 (machinery reuse, same slices as _build_v4.py).
ONE coherent FLOATED treatment, no options. Writes only into _review/."""
import json, io, re, os
D = os.path.dirname(os.path.abspath(__file__))
src = io.open(os.path.join(D, 'state-contrast-ruled-preview-v3.html'), encoding='utf-8').read().split('\n')
head      = src[0:67]     # 1..67
tabs_star = src[139:199]  # 140..199 (tabs card, star card, blank)
tail      = src[215:]     # 216.. (wrap close, script...)

def lum(h):
    h = h.lstrip('#'); c = [int(h[i:i+2], 16)/255 for i in (0, 2, 4)]
    c = [v/12.92 if v <= 0.03928 else ((v+0.055)/1.055)**2.4 for v in c]
    return .2126*c[0] + .7152*c[1] + .0722*c[2]
def ratio(a, b):
    l1, l2 = lum(a), lum(b); hi, lo = max(l1, l2), min(l1, l2)
    return round((hi+.05)/(lo+.05), 2)
def mix(fg, bg, p):
    f = [int(fg.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)]
    b = [int(bg.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)]
    return '#' + ''.join('%02X' % round(f[i]*p + b[i]*(1-p)) for i in range(3))

INK, WHITE = '#1A1A1A', '#FFFFFF'
FILL = '#F6604C'
MARK_L, MARK_D = '#DA1A00', '#F6604C'
WASH = [('base', 0.0), ('hover', 0.08), ('pressed', 0.14)]

banner_rows = []
for st, p in WASH:
    surf = mix(WHITE, FILL, p) if p else FILL
    banner_rows.append({'state': st, 'wash': int(p*100), 'surf': surf,
                        'r': ratio(INK, surf), 'r_white': ratio(WHITE, surf)})
B_BASE, B_HOVER, B_PRESSED = (r['r'] for r in banner_rows)
S_HOVER, S_PRESSED = banner_rows[1]['surf'], banner_rows[2]['surf']

sel_rows = [
    {'mode': 'light', 'part': 'mark / tick (rung rag-error-ink)', 'fg': MARK_L, 'bg': WHITE, 'r': ratio(MARK_L, WHITE)},
    {'mode': 'light', 'part': 'box border (follows the mark)',    'fg': MARK_L, 'bg': WHITE, 'r': ratio(MARK_L, WHITE)},
    {'mode': 'light', 'part': 'label (ink &mdash; s130-D5, unchanged)', 'fg': INK, 'bg': WHITE, 'r': ratio(INK, WHITE)},
    {'mode': 'dark',  'part': 'mark / tick (rung dark leg)',      'fg': MARK_D, 'bg': INK,   'r': ratio(MARK_D, INK)},
    {'mode': 'dark',  'part': 'box border (follows the mark)',    'fg': MARK_D, 'bg': INK,   'r': ratio(MARK_D, INK)},
    {'mode': 'dark',  'part': 'label (ink &mdash; s130-D5, unchanged)', 'fg': WHITE, 'bg': INK, 'r': ratio(WHITE, INK)},
]

def badge(r, thr=4.5):
    return ('<span class="b pass">%s:1 PASS</span>' % r) if r >= thr else ('<span class="b fail">%s:1 FAIL</span>' % r)
def sw(h):
    return '<span class="sw" style="background:%s"></span><span class="mono">%s</span>' % (h, h)

# ---------------------------------------------------------------- banner card
btab = ['<table class="m"><tr><th>state</th><th>white wash</th><th>fill under the text</th>'
        '<th>text #1A1A1A (the treatment)</th><th>white text (today&rsquo;s banner ink, for reference)</th></tr>']
for r in banner_rows:
    btab.append('<tr class="vr"><td class="mono">%s</td><td class="mono">%d%%</td><td>%s</td><td>%s</td><td>%s</td></tr>'
                % (r['state'], r['wash'], sw(r['surf']), badge(r['r']), badge(r['r_white'])))
btab.append('</table>')
btab = ''.join(btab)

banner_card = """<div class="card" id="card-banner"><h2>1 &middot; Banner &mdash; ONE treatment: fill <span class="mono">#F6604C</span>, text <span class="mono">#1A1A1A</span>, WHITE wash 8%/14%</h2>
<div class="floatbar"><b>FLOATED &mdash; NOT RULED. MONO THEME ONLY.</b> This is <b>your own pick</b>, drawn as one
coherent treatment so you can see it whole before ruling. There are <b>no options on this page</b>: exactly one
banner and exactly one selection control are rendered. Nothing here is recorded as a decision.</div>
<div class="diag"><b>The standard being previewed, stated once:</b> <b>dark text <span class="mono">#1A1A1A</span> on
<span class="mono">#F6604C</span></b> is the mono-wide banner standard. The fill <b>stays</b>
<span class="mono">#F6604C</span> &mdash; it does <i>not</i> move to <span class="mono">#B92F1E</span>. Because the
text is dark, the ghost-action wash inverts: hover and pressed are <b>WHITE transparencies at 8% and 14%</b>, which
<i>lighten</i> the fill and therefore <b>raise</b> the black-text ratio in every interactive state instead of
lowering it.</div>
<pre class="rule">/* FLOATED &mdash; scoped preview override inside the iframe, NOT written to canon */
.banner.err { --fill:#F6604C; --ink:#1A1A1A }                       /* dark text on the kept fill */
.banner .actions .abtn.fx-h { background:color-mix(in srgb, #FFFFFF 8%,  transparent) }   /* WHITE wash */
.banner .actions .abtn.fx-p { background:color-mix(in srgb, #FFFFFF 14%, transparent) }</pre>
__BTAB__
<div class="flag"><b>Measured, in-page, WCAG 2.x from the hexes above.</b>
base <span class="mono">#F6604C</span> &rarr; <b>__B_BASE__:1</b> &middot;
hover <span class="mono">__S_HOVER__</span> (8% white) &rarr; <b>__B_HOVER__:1</b> &middot;
pressed <span class="mono">__S_PRESSED__</span> (14% white) &rarr; <b>__B_PRESSED__:1</b>.
All three clear 4.5, and the ratio <b>climbs</b> with state pressure &mdash; the state that is hardest to read is
the resting one, which is the opposite of the black-wash arithmetic v4 measured.</div>
<div class="specrow"><div class="rowlab">light theme &mdash; mono</div><div class="specs">
<div class="spec"><div class="hd">light &middot; CURRENT (canon as-is: white text, #F6604C)</div><iframe data-frame="0" width="505" height="500"></iframe></div>
<div class="spec"><div class="hd">light &middot; THE TREATMENT &mdash; base / hover / pressed forced</div><iframe data-frame="11" width="505" height="500"></iframe></div>
</div></div>
<div class="specrow"><div class="rowlab">dark theme &mdash; mono</div><div class="specs">
<div class="spec"><div class="hd">dark &middot; CURRENT (canon as-is)</div><iframe data-frame="4" width="505" height="500"></iframe></div>
<div class="spec"><div class="hd">dark &middot; THE TREATMENT &mdash; base / hover / pressed forced</div><iframe data-frame="12" width="505" height="500"></iframe></div>
</div></div>
<div class="flag"><b>RAG fills do not invert (s122-D1/D2/D3)</b>, so the light and dark banner pair are expected to
look identical &mdash; that sameness is the theme layer working, not a rendering fault.</div>
<div class="open"><b>Still open, and NOT picked here.</b> <b>(i)</b> A white wash is not what
<span class="mono">s130-D4</span> wrote &mdash; D4's wash derives from <span class="mono">--ink</span>. Keeping 8%/14%
but sourcing them from white is a <i>change of source</i>, not of number; that is yours to say.
<b>(ii)</b> This forks mono's banner from legacy / console / supercharge unless they follow.
<b>(iii)</b> The dismiss <span class="mono">.x</span> and the <span class="mono">.ic</span> mark ride
<span class="mono">--ink</span> and turn dark with the text; shown above, not separately ruled.</div>
</div>"""
banner_card = (banner_card.replace('__BTAB__', btab)
               .replace('__B_BASE__', str(B_BASE)).replace('__B_HOVER__', str(B_HOVER))
               .replace('__B_PRESSED__', str(B_PRESSED))
               .replace('__S_HOVER__', S_HOVER).replace('__S_PRESSED__', S_PRESSED))

# ------------------------------------------------------------- selection card
stab = ['<table class="m"><tr><th>mode</th><th>part</th><th>colour</th><th>ground</th>'
        '<th>as TEXT (4.5)</th><th>as a GRAPHIC (1.4.11, 3.0)</th></tr>']
for r in sel_rows:
    stab.append('<tr class="vr"><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>'
                % (r['mode'], r['part'], sw(r['fg']), sw(r['bg']), badge(r['r'], 4.5), badge(r['r'], 3.0)))
stab.append('</table>')
stab = ''.join(stab)

sel_card = """<div class="card" id="card-selection"><h2>2 &middot; Selection controls &mdash; ONE treatment: the mark carries the <span class="mono">s145-D1</span> rung, BOTH legs</h2>
<div class="floatbar"><b>FLOATED &mdash; NOT RULED. MONO THEME ONLY.</b> One control per theme, no alternatives:
checkmarks and marks take the <span class="mono">s145-D1</span> <span class="mono">rag/error-ink</span> rung
&mdash; <b>light <span class="mono">#DA1A00</span>, dark <span class="mono">#F6604C</span></b>. The rung stays
whole across modes; the dark leg is the rung's own dark value, not a substitute.</div>
<div class="flag"><b>This touches <span class="mono">s130-D5</span>, said plainly.</b> At #130 the signal moved
<i>off</i> the control's label and onto the box border plus the message. This puts colour back on the control
&mdash; on the <b>mark</b>, not the label. The label stays ink in both modes and nothing here re-opens it.</div>
<pre class="rule">/* FLOATED &mdash; scoped preview override inside the iframe, NOT written to canon */
/* light */  .field.is-error .box path { stroke:#DA1A00 }   .field.is-error .box { border-color:#DA1A00 }
/* dark  */  .field.is-error .box path { stroke:#F6604C }   .field.is-error .box { border-color:#F6604C }
/* both  */  .field.is-error label { color:var(--label) }   /* ink &mdash; s130-D5, unchanged */</pre>
__STAB__
<div class="flag"><b>Why the rung needs two legs at all.</b> <span class="mono">#DA1A00</span> on
<span class="mono">#1A1A1A</span> measures <b>__DREF__:1</b> &mdash; it clears the 3.0 graphic line but not 4.5,
which is exactly why <span class="mono">s145-D1</span> gives the rung a <i>different</i> dark value. A tick is a
graphical object under 1.4.11 (3.0), not text, so both columns are shown and neither is asserted as governing.</div>
<div class="specrow"><div class="rowlab">light theme &mdash; mono</div><div class="specs">
<div class="spec"><div class="hd">light &middot; CURRENT (canon as-is)</div><iframe data-frame="1" width="400" height="380"></iframe></div>
<div class="spec"><div class="hd">light &middot; THE TREATMENT &mdash; mark #DA1A00</div><iframe data-frame="13" width="400" height="380"></iframe></div>
</div></div>
<div class="specrow"><div class="rowlab">dark theme &mdash; mono</div><div class="specs">
<div class="spec"><div class="hd">dark &middot; CURRENT (canon as-is)</div><iframe data-frame="5" width="400" height="380"></iframe></div>
<div class="spec"><div class="hd">dark &middot; THE TREATMENT &mdash; mark #F6604C</div><iframe data-frame="14" width="400" height="380"></iframe></div>
</div></div>
<div class="open"><b>Still open, and NOT picked here.</b> <b>(i)</b> The specimens force the error checkbox
<i>checked</i> so a mark exists at all; canon ships the error field unchecked, where only the border shows.
<b>(ii)</b> The border is drawn following the mark in both modes above &mdash; that is the drawing, not a ruling
(v3 named it D5-a). <b>(iii)</b> Whether &ldquo;marks&rdquo; reaches the radio dot, the switch and the
indeterminate dash is not stated.</div>
</div>"""
sel_card = sel_card.replace('__STAB__', stab).replace('__DREF__', str(ratio(MARK_L, INK)))

# ----------------------------------------------------------------- export card
export_card = """<div class="card" id="card-export"><h2>One confirm &mdash; the page rules nothing by itself</h2>
<p class="diag">Everything above is <b>one treatment</b>, drawn from your own floated picks, for the <b>mono</b>
theme only. There is nothing to choose between. This block asks a single question: does the drawing match what you
meant, and is it now firm?</p>
<div>
<label class="lic"><input type="radio" name="confirm" value="RULE IT"> <b>RULE IT</b> &mdash; this is the mono standard: banner <span class="mono">#1A1A1A</span> on <span class="mono">#F6604C</span> with white 8%/14% wash; marks on the <span class="mono">s145-D1</span> rung, light <span class="mono">#DA1A00</span> / dark <span class="mono">#F6604C</span>.</label>
<label class="lic"><input type="radio" name="confirm" value="AMEND" checked> <b>amend</b> &mdash; something is off; it stays FLOATED. Say what in the box below. (default)</label>
</div>
<p class="diag" style="margin-top:14px"><b>Free text</b> &mdash; the amendment, or anything to carry forward,
including the open items named on the cards.</p>
<textarea id="free" placeholder="e.g. the box border should stay at --error; the wash source needs to be named explicitly against s130-D4; radios and switches follow the tick; ..."></textarea>
<p style="margin:14px 0 0"><button class="act" id="copy">Copy readback</button> <span id="copied" class="mono"></span></p>
<textarea id="ruling" readonly></textarea>
</div>
"""

# ------------------------------------------------------------- head rewrite
head_txt = '\n'.join(head)
head_txt = head_txt.replace(
    'RULED s130-D4 / s130-D5 &mdash; enactment preview v3 (session #149)',
    'FLOATED mono treatment &mdash; preview v5 (session #149)')
head_txt = head_txt.replace(
    ' #ruling{min-height:300px}',
    ' #ruling{min-height:300px}\n .floatbar{background:#F3EAFA;border:1px solid #A87FD4;border-radius:8px;padding:12px 14px;margin:0 0 14px;font-size:13.5px}\n .spec > .hd{background:#F2EFEA;color:#2E2A25}')
head_lines = head_txt.split('\n')
new_intro = """<h1>FLOATED mono treatment <span class="mono">v5</span> &mdash; one picture, no options</h1>
<div class="ruledbar" style="background:#F3EAFA;border-color:#A87FD4"><b>NOTHING ON THIS PAGE IS RULED. THIS IS A FLOATED TREATMENT, MONO THEME ONLY.</b><br>
This page draws <b>your own floated picks as one coherent whole</b>, so you can see them together before ruling.
Unlike <span class="mono">v4</span>, there are <b>no alternatives rendered</b> &mdash; exactly one banner and one
selection control.<br>
<b>Banner:</b> fill <span class="mono">#F6604C</span> (kept), text and label <span class="mono">#1A1A1A</span>,
hover / pressed = <b>WHITE</b> transparencies at <b>8% / 14%</b>.
<b>Marks:</b> the <span class="mono">s145-D1</span> rung, both legs &mdash; light <span class="mono">#DA1A00</span>,
dark <span class="mono">#F6604C</span>.<br>
The mono-wide standard being previewed, in one line: <b>dark text <span class="mono">#1A1A1A</span> on
<span class="mono">#F6604C</span></b>.<br>
The other three themes (legacy, console, supercharge) are <b>not</b> in scope and are not shown.</div>

<p class="sub">Session #149, lane red 63, iteration 5. Machinery reused verbatim from
<span class="mono">state-contrast-ruled-preview-v3.html</span> via
<span class="mono">_review/_build_v5.py</span>: specimens are the <b>real canon snippets</b>
(<span class="mono">knowledge/snippets/Banner.reference.html</span>,
<span class="mono">Selection-controls.reference.html</span>,
<span class="mono">Tabs.reference.html</span>) embedded and rendered live in iframes with their own canon CSS and
the HSBC type layer. The floated treatment is applied as a <b>scoped preview override injected into that iframe
only</b>; each card states its override verbatim. <b>No canon, token or gate file was edited to produce this page,
and nothing was committed.</b> All ratios are computed by the WCAG 2.x relative-luminance formula from the hexes
shown. Hover and pressed are forced visible by rewriting <span class="mono">:hover</span>/<span
class="mono">:active</span> to classes, with transitions killed first. <b>Cards 3 and 4 (tabs re-point, path.star)
are carried from v3 unchanged.</b></p>"""
cut = next(i for i, l in enumerate(head_lines) if l.startswith('</style></head><body>'))
head_txt = '\n'.join(head_lines[:cut + 1]) + '\n\n' + new_intro + '\n'

# ------------------------------------------------------------------ new frames
BCSS = ("/* FLOATED PREVIEW OVERRIDE — mono only. Not written to canon.css. */\n"
        ".banner.err{--fill:#F6604C !important; --ink:#1A1A1A !important}\n"
        ".banner .actions .abtn.fx-h{background:color-mix(in srgb, #FFFFFF 8%, transparent)!important}\n"
        ".banner .actions .abtn.fx-p{background:color-mix(in srgb, #FFFFFF 14%, transparent)!important}\n")
def scss(stroke):
    return ("/* FLOATED PREVIEW OVERRIDE — mono only. Not written to canon.css. */\n"
            ".field.is-error label{color:var(--label)!important}\n"
            ".field.is-error .box{border-color:%s !important; background:transparent !important}\n"
            ".field.is-error .box path{stroke:%s !important; stroke-dashoffset:0 !important}\n" % (stroke, stroke))

NEW = []
for theme in ('light', 'dark'):                       # frames 11, 12
    NEW.append({"card": "banner", "comp": "Banner", "theme": theme, "variant": "floated",
                "container": ".banner.err", "target": ".abtn",
                "states": ["base", "hover", "pressed"], "w": 505, "h": 500,
                "css": BCSS, "seed": "", "pair": ""})
for theme, stroke in (('light', MARK_L), ('dark', MARK_D)):   # frames 13, 14
    NEW.append({"card": "selection", "comp": "Selection", "theme": theme, "variant": "floated",
                "container": ".field.is-error", "target": "label",
                "states": ["base", "hover", "pressed"], "w": 400, "h": 380,
                "css": scss(stroke), "seed": "checkerr", "pair": ".err-msg"})

tail_txt = '\n'.join(tail)
m = re.search(r'^const FRAMES = (\[.*\]);$', tail_txt, re.M)
frames = json.loads(m.group(1))
assert len(frames) == 11, len(frames)
frames += NEW
tail_txt = tail_txt[:m.start()] + 'const FRAMES = ' + json.dumps(frames) + ';' + tail_txt[m.end():]

old_seed = "if(C.seed==='ovcount'){var tg2=cl.querySelector('.overflow__trigger');if(tg2){tg2.innerHTML='More <span class=\"ovcount\">2</span>'}}"
assert old_seed in tail_txt
tail_txt = tail_txt.replace(old_seed, old_seed +
    "\n  if(C.seed==='checkerr'){var ip=cl.querySelector('input[type=checkbox]');if(ip){ip.checked=true;ip.setAttribute('checked','')}}")

# replace ruling() body
r0 = tail_txt.index('function ruling(){')
r1 = tail_txt.index("document.addEventListener('change',ruling);")
new_ruling = """function ruling(){
  const g=n=>{const p=document.querySelector('input[name='+n+']:checked');return p?p.value:'(none selected)'};
  const L=['FLOATED READBACK \\u2014 session #149, from _review/state-contrast-mono-preview-v5.html',
   'SUBJECT: ONE coherent FLOATED treatment, drawn from Dave\\'s own picks. No options were offered.',
   'SCOPE: MONO THEME ONLY. legacy / console / supercharge are not in scope and were not shown.',
   'THE PAGE RULES NOTHING BY ITSELF.',
   '',
   'THE TREATMENT, as drawn:',
   '  BANNER   fill #F6604C (kept, NOT #B92F1E) | text + label #1A1A1A',
   '           hover / pressed = WHITE transparencies 8% / 14% (the wash LIGHTENS the fill)',
   '  MARKS    s145-D1 rag/error-ink rung, BOTH legs: light #DA1A00, dark #F6604C',
   '  STANDARD mono-wide: dark text #1A1A1A on #F6604C',
   '',
   'CONFIRM : '+g('confirm'),
   '',
   'MEASURED IN-PAGE (WCAG 2.x, from the hexes shown):'];
  MEASURED.bannerv5.forEach(r=>{L.push('  banner  '+r.state.padEnd(8)+' white wash '+String(r.wash).padStart(2)+
    '%  surface '+r.surf+'   #1A1A1A '+r.r+':1 '+(r.r>=4.5?'PASS':'FAIL')+'   (white text '+r.r_white+':1)')});
  MEASURED.selv5.forEach(r=>{L.push('  control '+r.mode.padEnd(5)+' '+r.part.replace(/&mdash;/g,'-').padEnd(34)+
    r.fg+' on '+r.bg+'   '+r.r+':1  text4.5 '+(r.r>=4.5?'PASS':'FAIL')+'  graphic3.0 '+(r.r>=3.0?'PASS':'FAIL'))});
  L.push('');
  L.push('WHAT THE MEASUREMENT SAYS (measurement, not a pick):');
  L.push('  the white wash RAISES black-text contrast with state pressure: base is the WORST case, not the best.');
  L.push('  all three banner states clear 4.5 with #1A1A1A.');
  L.push('  #DA1A00 on #1A1A1A is only __DREF__:1 - it clears 3.0 (graphic) but not 4.5, which is why the rung has a separate dark leg.');
  L.push('');
  L.push('OPEN ITEMS NAMED ON THE PAGE, NOTHING PICKED:');
  L.push('  a-i    the wash SOURCE changes from --ink to white; s130-D4 wrote an ink-derived wash. Same numbers, different source.');
  L.push('  a-ii   this forks mono\\'s banner from legacy / console / supercharge unless they follow.');
  L.push('  a-iii  the dismiss .x and the .ic mark ride --ink and turn dark with the text; shown, not ruled.');
  L.push('  b-i    the specimens force the error checkbox CHECKED so a mark exists; canon ships it unchecked.');
  L.push('  b-ii   the box BORDER is drawn following the mark; that is the drawing, not a ruling (v3 named it D5-a).');
  L.push('  b-iii  does "marks" reach the radio dot, the switch and the indeterminate dash?');
  L.push('  b-iv   this puts colour back ON the control, which is the surface s130-D5 moved the signal OFF.');
  L.push('  TABS   card 3 carries v3\\'s unruled .ovcount re-point unchanged.');
  L.push('');
  L.push('FREE TEXT:');
  L.push((document.getElementById('free').value||'(none)'));
  L.push('');
  L.push('No canon.css / token / gate file was edited to produce this page, and nothing was committed.');
  document.getElementById('ruling').value=L.join('\\n');
}
"""
new_ruling = new_ruling.replace('__DREF__', str(ratio(MARK_L, INK)))
tail_txt = tail_txt[:r0] + new_ruling + tail_txt[r1:]

m2 = re.search(r'^const MEASURED = (\{.*\});$', tail_txt, re.M)
meas = json.loads(m2.group(1))
meas['bannerv5'] = banner_rows
meas['selv5'] = sel_rows
tail_txt = tail_txt[:m2.start()] + 'const MEASURED = ' + json.dumps(meas) + ';' + tail_txt[m2.end():]

out = head_txt + '\n' + banner_card + '\n\n' + sel_card + '\n\n' + '\n'.join(tabs_star) + '\n' + export_card + '\n' + tail_txt
p = os.path.join(D, 'state-contrast-mono-preview-v5.html')
io.open(p, 'w', encoding='utf-8').write(out)
print('wrote', p, len(out))
print('banner', [(r['state'], r['surf'], r['r']) for r in banner_rows])
print('sel', [(r['mode'], r['fg'], r['bg'], r['r']) for r in sel_rows])
print('DA1A00 on ink', ratio(MARK_L, INK))
