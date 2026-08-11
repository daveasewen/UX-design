#!/usr/bin/env python3
"""Build state-contrast-mono-preview-v4.html from v3 (machinery reuse). Writes only into _review/."""
import json, io, re, os
D = os.path.dirname(os.path.abspath(__file__))
src = io.open(os.path.join(D, 'state-contrast-ruled-preview-v3.html'), encoding='utf-8').read().split('\n')
# 1-indexed line slices from v3
head    = src[0:67]      # 1..67
tabs_star = src[139:199] # 140..199 (tabs card, star card, blank)
tail    = src[215:]      # 216.. (wrap close, script...)

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
FA, FB = '#F6604C', '#B92F1E'
WASH = [('base', 0.0), ('hover', 0.08), ('pressed', 0.14)]

banner_rows = []
for opt, fill in (('A', FA), ('B', FB)):
    for st, p in WASH:
        surf = mix(INK, fill, p) if p else fill
        banner_rows.append({'opt': opt, 'fill': fill, 'state': st, 'wash': int(p*100),
                            'surf': surf, 'ink': INK, 'r': ratio(INK, surf),
                            'r_white': ratio(WHITE, surf)})
sel_rows = [
    {'mode': 'light', 'opt': 'floated', 'part': 'mark (tick + box border)', 'fg': '#DA1A00', 'bg': '#FFFFFF', 'r': ratio('#DA1A00', '#FFFFFF')},
    {'mode': 'light', 'opt': 'floated', 'part': 'label (ink, s130-D5)',     'fg': INK,       'bg': '#FFFFFF', 'r': ratio(INK, '#FFFFFF')},
    {'mode': 'light', 'opt': 'current', 'part': 'mark (rag/error #F6604C)', 'fg': FA,        'bg': '#FFFFFF', 'r': ratio(FA, '#FFFFFF')},
    {'mode': 'dark',  'opt': 'b1',      'part': 'mark = ink #FFFFFF',       'fg': '#FFFFFF', 'bg': INK,       'r': ratio('#FFFFFF', INK)},
    {'mode': 'dark',  'opt': 'b2',      'part': 'mark = rung dark #F6604C', 'fg': FA,        'bg': INK,       'r': ratio(FA, INK)},
    {'mode': 'dark',  'opt': '(ref)',   'part': 'light rung #DA1A00 in dark', 'fg': '#DA1A00', 'bg': INK,     'r': ratio('#DA1A00', INK)},
]
# last wash % that still clears 4.5 with black ink on option A
last_ok = max(p for p in range(0, 26) if ratio(INK, mix(INK, FA, p/100)) >= 4.5)

def badge(r, thr=4.5):
    return ('<span class="b pass">%s:1 PASS</span>' % r) if r >= thr else ('<span class="b fail">%s:1 FAIL</span>' % r)
def sw(h):
    return '<span class="sw" style="background:%s"></span><span class="mono">%s</span>' % (h, h)

# ---------------------------------------------------------------- banner card
btab = ['<table class="m"><tr><th>option</th><th>state</th><th>black wash</th><th>fill under the text</th>'
        '<th>text #1A1A1A (FLOATED)</th><th>white text (today\'s banner ink)</th></tr>']
for r in banner_rows:
    cls = 'vr' if r['opt'] == 'A' else 'vc'
    btab.append('<tr class="%s"><td><b>%s</b> &mdash; fill %s</td><td class="mono">%s</td><td class="mono">%d%%</td>'
                '<td>%s</td><td>%s</td><td>%s</td></tr>'
                % (cls, r['opt'], r['fill'], r['state'], r['wash'], sw(r['surf']), badge(r['r']), badge(r['r_white'])))
btab.append('</table>')
btab = ''.join(btab)

banner_card = """<div class="card" id="card-banner"><h2>1 &middot; Banner &mdash; FLOATED mono reversal: banner text <span class="mono">#1A1A1A</span> <span class="mono">(MONO ONLY &mdash; NOT RULED)</span></h2>
<div class="floatbar"><b>FLOATED, NOT RULED &mdash; MONO THEME ONLY.</b> Dave floated (firmness not given) that the
<b>mono</b> banner text joins the mono ink camp (<span class="mono">s122-D2</span> marks,
<span class="mono">s134-D4</span> glyphs) at <span class="mono">#1A1A1A</span>. Everything on this card is a
<b>preview of a floated idea</b>. Nothing here is picked, and the other three themes are untouched.</div>
<div class="diag">Black banner text changes the arithmetic in two places at once. <b>(1) The fill.</b> Today's
mono error fill is <span class="mono">#F6604C</span>; <span class="mono">s130-D4</span> moves it to
<span class="mono">#B92F1E</span> &mdash; but D4 chose that darker red <i>to carry WHITE text</i>. With black text
the direction of travel reverses. <b>(2) The wash.</b> <span class="mono">s130-D4</span>'s ghost actions derive
their wash from <span class="mono">--ink</span>, so with black ink the 8%%/14%% wash now <b>darkens</b> the fill
instead of lightening it &mdash; and black text on a darkening fill loses contrast with every state.</div>
<div class="open"><b>OPEN CLARIFIER (a) &mdash; both options rendered, NOTHING PICKED.</b>
<b>Option A</b>: the fill <i>stays</i> <span class="mono">#F6604C</span>.
<b>Option B</b>: the fill still moves to <span class="mono">#B92F1E</span> per <span class="mono">s130-D4</span>.
The table below computes black text on both, in every washed state.</div>
<pre class="rule">/* FLOATED &mdash; scoped preview override inside the iframe, NOT written to canon */
/* option A */  .banner.err { --fill:#F6604C; --ink:#1A1A1A }
/* option B */  .banner.err { --fill:#B92F1E; --ink:#1A1A1A }
/* both, per s130-D4's 8%%/14%% remap &mdash; the wash is INK-derived, so it is now BLACK */
.banner .actions .abtn.fx-h { background:color-mix(in srgb, var(--ink) 8%%,  transparent) }
.banner .actions .abtn.fx-p { background:color-mix(in srgb, var(--ink) 14%%, transparent) }</pre>
__BTAB__
<div class="flag"><b>What the numbers say, stated as measurement not as a choice.</b>
<b>Option A</b> (<span class="mono">#F6604C</span> kept): black text is <b>%(a_base)s:1</b> at rest and
<b>%(a_hover)s:1</b> at hover &mdash; both clear 4.5 &mdash; but the 14%% pressed wash darkens the fill to
<span class="mono">%(a_psurf)s</span> and black text there measures <b>%(a_pressed)s:1</b>, which is
<b>below 4.5</b>. The last black-wash percentage that still clears 4.5 on this fill is <b>%(last_ok)d%%</b>.
<b>Option B</b> (<span class="mono">#B92F1E</span>): black text measures <b>%(b_base)s:1</b> at rest, before any
wash, falling to <b>%(b_pressed)s:1</b> pressed. <b>That measurement kills option B under the floated black-text
premise</b> &mdash; not an opinion: #B92F1E was chosen at #130 precisely because it is dark enough for WHITE text
(%(b_white)s:1), and the same darkness is what black text cannot survive. If the banner text is to be black, the
fill cannot also be #B92F1E. Both remain rendered above and below so you can see them.</div>
<div class="specrow"><div class="rowlab">light theme &mdash; mono</div><div class="specs">
<div class="spec"><div class="hd">light &middot; CURRENT (canon as-is: white text, #F6604C)</div><iframe data-frame="0" width="505" height="500"></iframe></div>
<div class="spec"><div class="hd">light &middot; FLOATED opt A &mdash; black text, fill #F6604C</div><iframe data-frame="11" width="505" height="500"></iframe></div>
<div class="spec"><div class="hd">light &middot; FLOATED opt B &mdash; black text, fill #B92F1E</div><iframe data-frame="12" width="505" height="500"></iframe></div>
</div></div>
<div class="specrow"><div class="rowlab">dark theme &mdash; mono</div><div class="specs">
<div class="spec"><div class="hd">dark &middot; CURRENT (canon as-is)</div><iframe data-frame="4" width="505" height="500"></iframe></div>
<div class="spec"><div class="hd">dark &middot; FLOATED opt A &mdash; black text, fill #F6604C</div><iframe data-frame="13" width="505" height="500"></iframe></div>
<div class="spec"><div class="hd">dark &middot; FLOATED opt B &mdash; black text, fill #B92F1E</div><iframe data-frame="14" width="505" height="500"></iframe></div>
</div></div>
<div class="flag"><b>RAG fills do not invert (s122-D1/D2/D3)</b>, so the light and dark banner pairs are expected
to be identical &mdash; that sameness is the theme layer working, not a rendering fault.</div>
<div class="open"><b>Also open, nothing picked.</b> <b>(i)</b> If the wash must shrink to keep pressed above 4.5,
that <i>re-opens</i> the 8%%/14%% numbers <span class="mono">s130-D4</span> already ruled &mdash; a floated mono
reversal cannot silently amend a ruled percentage; that is yours to say. <b>(ii)</b> A white-text banner and a
black-text banner want <i>different</i> fills, so this floated reversal makes mono's banner fill fork from the
other three themes unless they follow. <b>(iii)</b> The banner dismiss <span class="mono">.x</span> and the
<span class="mono">.ic</span> mark both ride <span class="mono">--ink</span> and would turn black with the text;
shown above, not separately ruled.</div>
</div>""" % {
    'a_base': banner_rows[0]['r'], 'a_hover': banner_rows[1]['r'], 'a_pressed': banner_rows[2]['r'],
    'a_psurf': banner_rows[2]['surf'], 'b_base': banner_rows[3]['r'], 'b_pressed': banner_rows[5]['r'],
    'b_white': banner_rows[3]['r_white'], 'last_ok': last_ok,
}
banner_card = banner_card.replace('__BTAB__', btab)

# ------------------------------------------------------------- selection card
stab = ['<table class="m"><tr><th>mode</th><th>option</th><th>part</th><th>colour</th><th>ground</th>'
        '<th>as TEXT (4.5)</th><th>as a GRAPHIC (1.4.11, 3.0)</th></tr>']
for r in sel_rows:
    cls = 'vr' if r['opt'] in ('floated', 'b1', 'b2') else 'vc'
    stab.append('<tr class="%s"><td>%s</td><td class="mono">%s</td><td>%s</td><td>%s</td><td>%s</td>'
                '<td>%s</td><td>%s</td></tr>'
                % (cls, r['mode'], r['opt'], r['part'], sw(r['fg']), sw(r['bg']),
                   badge(r['r'], 4.5), badge(r['r'], 3.0)))
stab.append('</table>')
stab = ''.join(stab)

sel_card = """<div class="card" id="card-selection"><h2>2 &middot; Selection-controls &mdash; FLOATED: the checkmark carries the rung red <span class="mono">(MONO ONLY &mdash; NOT RULED)</span></h2>
<div class="floatbar"><b>FLOATED, NOT RULED &mdash; MONO THEME ONLY.</b> Dave floated that checkmarks / marks take
the <span class="mono">s145-D1</span> rung <span class="mono">rag/error-ink</span> &mdash; light
<span class="mono">#DA1A00</span>. Firmness has not been given.</div>
<div class="flag"><b>This touches <span class="mono">s130-D5</span>, and it is worth saying plainly.</b>
At #130 the signal was moved <i>off</i> the control's label and onto the box border plus the message. This floated
item <b>puts colour back onto the control</b> &mdash; on the mark rather than the label, so it is not a straight
reversal, but it is the same surface. The label stays ink either way; nothing here re-opens the label.</div>
<pre class="rule">/* FLOATED &mdash; scoped preview override inside the iframe, NOT written to canon */
/* light */        .field.is-error .box path { stroke:#DA1A00 }   .field.is-error .box { border-color:#DA1A00 }
/* dark, opt b1 */ .field.is-error .box path { stroke:#FFFFFF }   /* "red text only with dark ink" */
/* dark, opt b2 */ .field.is-error .box path { stroke:#F6604C }   /* the rung's own dark value */
/* both */         .field.is-error label { color:var(--label) }   /* ink &mdash; s130-D5, unchanged */</pre>
__STAB__
<div class="open"><b>OPEN CLARIFIER (b) &mdash; both dark options rendered, NOTHING PICKED.</b>
<b>b1</b> &mdash; the dark mark is <b>ink/white</b> (<span class="mono">%(b1)s:1</span>), reading
&ldquo;red text only with dark ink&rdquo; as covering marks too, which leaves the dark control with <i>no</i> red
at all. <b>b2</b> &mdash; the dark mark takes the rung's own dark value <span class="mono">#F6604C</span>
(<span class="mono">%(b2)s:1</span>), which keeps the rung whole across modes. Both clear both thresholds; this is
a meaning question, not a contrast question, and it is yours.</div>
<div class="flag"><b>Why the light rung cannot simply be carried into dark.</b>
<span class="mono">#DA1A00</span> on <span class="mono">#1A1A1A</span> is <b>%(dref)s:1</b> &mdash; it clears the
3.0 graphic line but not 4.5, which is exactly why <span class="mono">s145-D1</span> gives the rung a
<i>different</i> dark value. A checkbox tick is a graphical object under 1.4.11 (3.0), not text, so both columns
are shown and neither is asserted as the governing one.</div>
<div class="specrow"><div class="rowlab">light theme &mdash; mono</div><div class="specs">
<div class="spec"><div class="hd">light &middot; CURRENT (canon as-is)</div><iframe data-frame="1" width="400" height="380"></iframe></div>
<div class="spec"><div class="hd">light &middot; FLOATED &mdash; mark #DA1A00</div><iframe data-frame="15" width="400" height="380"></iframe></div>
</div></div>
<div class="specrow"><div class="rowlab">dark theme &mdash; mono</div><div class="specs">
<div class="spec"><div class="hd">dark &middot; CURRENT (canon as-is)</div><iframe data-frame="5" width="400" height="380"></iframe></div>
<div class="spec"><div class="hd">dark &middot; FLOATED b1 &mdash; mark = ink #FFFFFF</div><iframe data-frame="16" width="400" height="380"></iframe></div>
<div class="spec"><div class="hd">dark &middot; FLOATED b2 &mdash; mark = #F6604C</div><iframe data-frame="17" width="400" height="380"></iframe></div>
</div></div>
<div class="open"><b>Also open, nothing picked.</b> <b>(i)</b> The error checkbox is forced <i>checked</i> in the
specimens so the mark is visible at all &mdash; in canon the error field ships unchecked, so an unchecked error
control shows only the border and this floated item does nothing for it. <b>(ii)</b> Whether the box
<i>border</i> follows the mark to the rung, or stays at <span class="mono">--error #F6604C</span>, is the same
unruled item v3 named as D5-a. <b>(iii)</b> &ldquo;Checkmarks / marks&rdquo; is shown here on the checkbox tick;
whether it reaches the radio dot, the switch, and the indeterminate dash is not stated.</div>
</div>""" % {'b1': sel_rows[3]['r'], 'b2': sel_rows[4]['r'], 'dref': sel_rows[5]['r']}
sel_card = sel_card.replace('__STAB__', stab)

# ----------------------------------------------------------------- export card
export_card = """<div class="card" id="card-export"><h2>FLOATED readback &mdash; nothing is ruled by this page</h2>
<p class="diag">This block records <b>what was floated and what you say about it</b>. It is a readback, not a
licence. Leave the firmness line at &ldquo;keep floating&rdquo; and nothing has been decided.</p>
<p class="rowlab">clarifier (a) &mdash; the mono banner FILL under black text</p>
<div>
<label class="lic"><input type="radio" name="fill" value="A"> <b>A</b> &mdash; fill stays <span class="mono">#F6604C</span> (black text %(a_base)s:1 base, %(a_hover)s:1 hover, %(a_pressed)s:1 pressed &mdash; pressed is below 4.5)</label>
<label class="lic"><input type="radio" name="fill" value="B"> <b>B</b> &mdash; fill still moves to <span class="mono">#B92F1E</span> per s130-D4 (black text %(b_base)s:1 &mdash; measured FAIL at every state)</label>
<label class="lic"><input type="radio" name="fill" value="OPEN"> <b>neither yet</b> &mdash; the fill question stays open</label>
</div>
<p class="rowlab" style="margin-top:14px">clarifier (b) &mdash; the DARK-mode checkmark</p>
<div>
<label class="lic"><input type="radio" name="mark" value="b1"> <b>b1</b> &mdash; ink / white <span class="mono">#FFFFFF</span> (%(b1)s:1) &mdash; no red on the dark control</label>
<label class="lic"><input type="radio" name="mark" value="b2"> <b>b2</b> &mdash; the rung's dark <span class="mono">#F6604C</span> (%(b2)s:1) &mdash; the rung stays whole</label>
<label class="lic"><input type="radio" name="mark" value="OPEN"> <b>neither yet</b> &mdash; the dark-mark question stays open</label>
</div>
<p class="rowlab" style="margin-top:14px">firmness</p>
<div>
<label class="lic"><input type="radio" name="firm" value="FLOATING" checked> <b>keep floating</b> &mdash; this is still an idea; do not record it as a ruling (default)</label>
<label class="lic"><input type="radio" name="firm" value="RULED"> <b>ruled</b> &mdash; record the picks above as a decision for the <b>mono</b> theme</label>
</div>
<p class="diag" style="margin-top:14px"><b>Free text</b> &mdash; anything to carry forward, including answers to the
open items named on the cards.</p>
<textarea id="free" placeholder="e.g. shrink the pressed wash to 12%% rather than move the fill; b2 for dark; radios and switches follow the tick; ..."></textarea>
<p style="margin:14px 0 0"><button class="act" id="copy">Copy readback</button> <span id="copied" class="mono"></span></p>
<textarea id="ruling" readonly></textarea>
</div>
""" % {'a_base': banner_rows[0]['r'], 'a_hover': banner_rows[1]['r'], 'a_pressed': banner_rows[2]['r'],
       'b_base': banner_rows[3]['r'], 'b1': sel_rows[3]['r'], 'b2': sel_rows[4]['r']}

# ------------------------------------------------------------- head rewrite
head_txt = '\n'.join(head)
head_txt = head_txt.replace(
    'RULED s130-D4 / s130-D5 &mdash; enactment preview v3 (session #149)',
    'FLOATED mono reversal &mdash; preview v4 (session #149)')
head_txt = head_txt.replace(
    ' #ruling{min-height:300px}',
    ' #ruling{min-height:300px}\n .floatbar{background:#F3EAFA;border:1px solid #A87FD4;border-radius:8px;padding:12px 14px;margin:0 0 14px;font-size:13.5px}\n .spec > .hd{background:#F2EFEA;color:#2E2A25}')
# replace the h1 + ruledbar + sub block (v3 lines 46..66 -> indices 45..65)
head_lines = head_txt.split('\n')
new_intro = """<h1>FLOATED mono reversal <span class="mono">v4</span></h1>
<div class="ruledbar" style="background:#F3EAFA;border-color:#A87FD4"><b>NOTHING ON THIS PAGE IS RULED. THIS IS A FLOATED IDEA, MONO THEME ONLY.</b><br>
Dave <b>floated</b> &mdash; firmness <b>not</b> given &mdash; that (1) <b>mono banner text</b> becomes
<span class="mono">#1A1A1A</span>, joining the mono ink camp (<span class="mono">s122-D2</span> marks,
<span class="mono">s134-D4</span> glyphs); and (2) <b>checkmarks / marks</b> take the
<span class="mono">s145-D1</span> rung <span class="mono">rag/error-ink</span>, light
<span class="mono">#DA1A00</span>.<br>
<b>Two clarifiers are open and BOTH options of each are rendered live below. Nothing is picked here.</b>
<b>(a)</b> does the mono banner <b>fill</b> stay <span class="mono">#F6604C</span> or still move to
<span class="mono">#B92F1E</span> per <span class="mono">s130-D4</span>?
<b>(b)</b> in <b>dark</b>, is the checkmark <b>ink/white</b> or the rung's dark
<span class="mono">#F6604C</span>?<br>
The other three themes (legacy, console, supercharge) are <b>not</b> in scope and are not shown.</div>

<p class="sub">Session #149, lane red 63, iteration 4. Machinery reused verbatim from
<span class="mono">state-contrast-ruled-preview-v3.html</span>: specimens are the <b>real canon snippets</b>
(<span class="mono">knowledge/snippets/Banner.reference.html</span>,
<span class="mono">Selection-controls.reference.html</span>,
<span class="mono">Tabs.reference.html</span>) embedded and rendered live in iframes with their own canon CSS and
the HSBC type layer. Floated treatments are applied as a <b>scoped preview override injected into that iframe
only</b>; every card states its override verbatim. <b>No canon, token or gate file was edited to produce this
page, and nothing was committed.</b> All ratios are computed by the WCAG 2.x relative-luminance formula from the
hexes shown. Hover and pressed are forced visible by rewriting <span class="mono">:hover</span>/<span
class="mono">:active</span> to classes, with transitions killed first. <b>Cards 3 and 4 (tabs re-point,
path.star) are carried from v3 unchanged.</b></p>"""
cut = next(i for i, l in enumerate(head_lines) if l.startswith('</style></head><body>'))
head_txt = '\n'.join(head_lines[:cut + 1]) + '\n\n' + new_intro + '\n'

# ------------------------------------------------------------------ new frames
def bcss(fill):
    return ("/* FLOATED PREVIEW OVERRIDE — mono only. Not written to canon.css. */\n"
            ".banner.err{--fill:%s !important; --ink:#1A1A1A !important}\n"
            ".banner .actions .abtn.fx-h{background:color-mix(in srgb, var(--ink) 8%%, transparent)!important}\n"
            ".banner .actions .abtn.fx-p{background:color-mix(in srgb, var(--ink) 14%%, transparent)!important}\n" % fill)
def scss(stroke):
    return ("/* FLOATED PREVIEW OVERRIDE — mono only. Not written to canon.css. */\n"
            ".field.is-error label{color:var(--label)!important}\n"
            ".field.is-error .box{border-color:%s !important; background:transparent !important}\n"
            ".field.is-error .box path{stroke:%s !important; stroke-dashoffset:0 !important}\n" % (stroke, stroke))

NEW = []
for theme in ('light', 'dark'):
    for fill in (FA, FB):
        NEW.append({"card": "banner", "comp": "Banner", "theme": theme, "variant": "floated",
                    "container": ".banner.err", "target": ".abtn",
                    "states": ["base", "hover", "pressed"], "w": 505, "h": 500,
                    "css": bcss(fill), "seed": "", "pair": ""})
# order must be 11 light-A, 12 light-B, 13 dark-A, 14 dark-B  -> already that order
for stroke in ('#DA1A00',):
    NEW.append({"card": "selection", "comp": "Selection", "theme": "light", "variant": "floated",
                "container": ".field.is-error", "target": "label",
                "states": ["base", "hover", "pressed"], "w": 400, "h": 380,
                "css": scss(stroke), "seed": "checkerr", "pair": ".err-msg"})
for stroke in ('#FFFFFF', '#F6604C'):
    NEW.append({"card": "selection", "comp": "Selection", "theme": "dark", "variant": "floated",
                "container": ".field.is-error", "target": "label",
                "states": ["base", "hover", "pressed"], "w": 400, "h": 380,
                "css": scss(stroke), "seed": "checkerr", "pair": ".err-msg"})

tail_txt = '\n'.join(tail)
m = re.search(r'^const FRAMES = (\[.*\]);$', tail_txt, re.M)
frames = json.loads(m.group(1))
assert len(frames) == 11, len(frames)
frames += NEW
tail_txt = tail_txt[:m.start()] + 'const FRAMES = ' + json.dumps(frames) + ';' + tail_txt[m.end():]

# seed hook for the forced-checked error control
old_seed = "if(C.seed==='ovcount'){var tg2=cl.querySelector('.overflow__trigger');if(tg2){tg2.innerHTML='More <span class=\"ovcount\">2</span>'}}"
assert old_seed in tail_txt
tail_txt = tail_txt.replace(old_seed, old_seed +
    "\n  if(C.seed==='checkerr'){var ip=cl.querySelector('input[type=checkbox]');if(ip){ip.checked=true;ip.setAttribute('checked','')}}")

# replace ruling() body
r0 = tail_txt.index('function ruling(){')
r1 = tail_txt.index("document.addEventListener('change',ruling);")
new_ruling = """function ruling(){
  const g=n=>{const p=document.querySelector('input[name='+n+']:checked');return p?p.value:'(none selected)'};
  const L=['FLOATED READBACK — session #149, from _review/state-contrast-mono-preview-v4.html',
   'SUBJECT: a FLOATED mono reversal. NOTHING ON THE PAGE IS RULED, and this block rules nothing by itself.',
   'SCOPE: MONO THEME ONLY. legacy / console / supercharge are not in scope and were not shown.',
   '',
   'THE FLOATED ITEMS, as put:',
   '  1  mono banner text -> #1A1A1A (joins the mono ink camp: s122-D2 marks, s134-D4 glyphs)',
   '  2  checkmarks / marks -> s145-D1 rung rag/error-ink, light #DA1A00',
   '',
   'CLARIFIER (a) mono banner FILL under black text : '+g('fill'),
   'CLARIFIER (b) DARK-mode checkmark               : '+g('mark'),
   'FIRMNESS                                        : '+g('firm'),
   '',
   'MEASURED IN-PAGE (WCAG 2.x, from the hexes shown):'];
  MEASURED.bannerv4.forEach(r=>{L.push('  banner opt '+r.opt+'  fill '+r.fill+'  '+r.state.padEnd(8)+
    ' black wash '+String(r.wash).padStart(2)+'%  surface '+r.surf+'   #1A1A1A '+r.r+':1 '+(r.r>=4.5?'PASS':'FAIL')+
    '   (white text '+r.r_white+':1)')});
  MEASURED.selv4.forEach(r=>{L.push('  control '+r.mode.padEnd(5)+' '+r.opt.padEnd(8)+' '+r.part.padEnd(26)+
    r.fg+' on '+r.bg+'   '+r.r+':1  text4.5 '+(r.r>=4.5?'PASS':'FAIL')+'  graphic3.0 '+(r.r>=3.0?'PASS':'FAIL'))});
  L.push('');
  L.push('WHAT THE MEASUREMENT SETTLES BY ITSELF (measurement, not a pick):');
  L.push('  option B (#B92F1E) cannot carry #1A1A1A text — 2.89:1 at rest, before any wash.');
  L.push('  option A (#F6604C) carries it at rest and hover, but s130-D4\\'s 14% BLACK pressed wash lands at 4.40:1.');
  L.push('  the last black wash % that still clears 4.5 on #F6604C is """ + str(last_ok) + """%.');
  L.push('');
  L.push('OPEN ITEMS NAMED ON THE PAGE, NOTHING PICKED:');
  L.push('  a-i    keeping pressed above 4.5 would amend s130-D4\\'s ruled 8%/14% — a floated item cannot do that silently.');
  L.push('  a-ii   black-text mono forks the banner fill away from the other three themes unless they follow.');
  L.push('  a-iii  the dismiss .x and the .ic mark ride --ink and turn black with the text; shown, not ruled.');
  L.push('  b-i    the specimens force the error checkbox CHECKED so a mark exists; canon ships it unchecked.');
  L.push('  b-ii   does the box BORDER follow the mark to the rung, or stay at --error #F6604C? (v3 named this D5-a)');
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
tail_txt = tail_txt[:r0] + new_ruling + tail_txt[r1:]
# append the v4 measurement data onto MEASURED
m2 = re.search(r'^const MEASURED = (\{.*\});$', tail_txt, re.M)
meas = json.loads(m2.group(1))
meas['bannerv4'] = banner_rows
meas['selv4'] = sel_rows
tail_txt = tail_txt[:m2.start()] + 'const MEASURED = ' + json.dumps(meas) + ';' + tail_txt[m2.end():]

out = head_txt + '\n' + banner_card + '\n\n' + sel_card + '\n\n' + '\n'.join(tabs_star) + '\n' + export_card + '\n' + tail_txt
p = os.path.join(D, 'state-contrast-mono-preview-v4.html')
io.open(p, 'w', encoding='utf-8').write(out)
print('wrote', p, len(out))
