#!/usr/bin/env python3
"""gen_amber_matrix.py — the amber background matrix: darkness × saturation.

Dave, 2026-07-18: *"we need to solve amber, we matt yellow with a little darkness and reducing
saturation."* Two variables, so a ladder cannot show it — this is a grid. Rows drop lightness,
columns drop chroma, hue held at 79.5° throughout.

WHY A MATRIX AND NOT A LADDER
  RAG-MATTING gave amber a single ladder that varied chroma only, and targeted 7.0:1 with dark ink.
  That target forced every candidate to L≈0.72 — all four DARKER than the current #FFBB33 (L 0.834)
  and back toward the brown Dave had already rejected. Dave's verdict: *"this for glyphs, but not
  for backgrounds."* The ladder was answering the wrong question.

CONTRAST IS NOT THE CONSTRAINT HERE — say so plainly
  Every cell in this window lands between 7.70 and 10.38 against the digital black. All AAA. So
  nothing in this grid is gated by accessibility, and the choice is PURELY aesthetic. Stating that
  matters: it stops a taste decision being dressed up as a compliance one.

GAMUT IS CHECKED, NOT ASSUMED
  OKLCh will happily describe colours sRGB cannot show; converting then silently clamps, and the
  swatch you see is not the colour you asked for. Cells that clip are marked — L 0.750 at full
  chroma is already outside. An unmarked clip is a lie in a specimen.

AMBER'S CARVE-OUT (R-D2) — carried, not re-argued
  Amber is the light hue: dark ink on its fill, and a DARKER separate value as its glyph. One
  exception, two consequences. The glyph column is shown alongside each row so the pair is judged
  together, never in isolation.

Usage:  python3 reviews/gen_amber_matrix.py
Then:   python3 knowledge/_review/_make_review.py reviews/AMBER-MATRIX-2026-07-18.html
"""
import os, math

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "reviews", "AMBER-MATRIX-2026-07-18.html")
INK = "#1A1A1A"
BASE = "#FFBB33"


def s2l(c): return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
def l2s(c):
    c = max(0.0, min(1.0, c))
    return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055
def hex2lin(h):
    h = h.lstrip("#"); return [s2l(int(h[i:i + 2], 16) / 255) for i in (0, 2, 4)]
def lin2hex(r, g, b): return "#%02X%02X%02X" % tuple(round(l2s(x) * 255) for x in (r, g, b))

M1 = [[.4122214708, .5363325363, .0514459929], [.2119034982, .6806995451, .1073969566],
      [.0883024619, .2817188376, .6299787005]]
M2 = [[.2104542553, .7936177850, -.0040720468], [1.9779984951, -2.4285922050, .4505937099],
      [.0259040371, .7827717662, -.8086757660]]
Mi = [[4.0767416621, -3.3077115913, .2309699292], [-1.2684380046, 2.6097574011, -.3413193965],
      [-.0041960863, -.7034186147, 1.7076147010]]


def oklch(h):
    r, g, b = hex2lin(h)
    l, m, s = [sum(M1[i][j] * [r, g, b][j] for j in range(3)) for i in range(3)]
    l, m, s = [x ** (1 / 3) if x > 0 else -((-x) ** (1 / 3)) for x in (l, m, s)]
    L, a, b2 = [sum(M2[i][j] * [l, m, s][j] for j in range(3)) for i in range(3)]
    return L, math.hypot(a, b2), math.degrees(math.atan2(b2, a)) % 360


def _lin(L, C, H):
    a, b = C * math.cos(math.radians(H)), C * math.sin(math.radians(H))
    l_, m_, s_ = L + .3963377774 * a + .2158037573 * b, L - .1055613458 * a - .0638541728 * b, \
                 L - .0894841775 * a - 1.2914855480 * b
    l, m, s = l_ ** 3, m_ ** 3, s_ ** 3
    return [sum(Mi[i][j] * [l, m, s][j] for j in range(3)) for i in range(3)]


def from_lch(L, C, H): return lin2hex(*_lin(L, C, H))
def clips(L, C, H):
    v = _lin(L, C, H); return min(v) < -0.001 or max(v) > 1.001
def lum(h):
    r, g, b = hex2lin(h); return .2126 * r + .7152 * g + .0722 * b
def cr(a, b):
    l1, l2 = sorted([lum(a), lum(b)], reverse=True); return (l1 + .05) / (l2 + .05)


def glyph_at(pct, H, C0):
    """The paired glyph — darkest-permissible on a white page, 4.5:1, same hue + chroma step."""
    for step in range(900, 300, -1):
        cand = from_lch(step * .001, C0 * pct, H)
        if cr("#FFFFFF", cand) >= 4.5:
            return cand
    return "#8E7245"


TICK = ('<svg viewBox="0 0 16 16" width="14" height="14" aria-hidden="true"><path d="M3 8.5l3.5 3'
        'L13 5" fill="none" stroke="currentColor" stroke-width="1.6"/></svg>')
ARROW = ('<svg viewBox="0 0 16 16" width="14" height="14" aria-hidden="true"><path d="M3 8h9'
         'M8.5 4.5L12 8l-3.5 3.5" fill="none" stroke="currentColor" stroke-width="1.6"/></svg>')

L0, C0, H0 = oklch(BASE)
LS = [(0.834, "as now"), (0.810, "−3%"), (0.790, "−5%"), (0.770, "−8%"), (0.750, "−10%")]
CS = [(1.00, "full"), (0.85, "−15%"), (0.72, "−28%"), (0.60, "−40%")]

head = "".join(f'<th>{lab}<br><span class="met">C {C0*p:.3f}</span></th>' for p, lab in CS)
rows = ""
for L, llab in LS:
    cells = ""
    for pct, clab in CS:
        hx = from_lch(L, C0 * pct, H0)
        bad = clips(L, C0 * pct, H0)
        v = cr(INK, hx)
        cells += (f'<td class="cell">'
                  f'<span class="tag" style="background:{hx};color:{INK}">{TICK}<span>Pending</span></span>'
                  f'<br><code>{hx}</code>{" <b class=clip>clipped</b>" if bad else ""}'
                  f'<br><span class="r ok">{v:.2f}</span><span class="met"> ink · 4.5</span>'
                  f'<br><span class="r {"ok" if cr("#FFFFFF", hx) >= 3 else "no"}">'
                  f'{cr("#FFFFFF", hx):.2f}</span><span class="met"> edge · 3.0</span></td>')
    rows += (f'<tr><th class="rh">{llab}<br><span class="met">L {L:.3f}</span></th>{cells}'
             f'<td class="ask"></td></tr>')

# DECORATIVE glyph — the light amber itself, beside a neutral label.
# Dave's ruling: "contrast with a white background is a luxury, the label carries the meaning."
# That is house canon already (1.4.1), stated in Account-card, Status-indicator, Confirmation,
# Countdown-timer and Links. If the icon is aria-hidden and the LABEL carries the state, the icon
# is decorative, 1.4.11 does not apply, and it may stay light — matching the fill.
decrow = "".join(
    f'<td class="cell"><span class="gl" style="color:{from_lch(0.790, C0*p, H0)}">{ARROW}</span>'
    f'<span class="gl" style="color:{INK}"><b>Pending</b></span>'
    f'<br><code>{from_lch(0.790, C0*p, H0)}</code><br>'
    f'<span class="met">{cr("#FFFFFF", from_lch(0.790, C0*p, H0)):.2f} — decorative, 1.4.1</span></td>'
    for p, _ in CS)
# TEXT-SAFE glyph — only needed where amber is the TEXT itself (1.4.3 applies, 4.5:1, no waiver).
def glyph_t(pct, target):
    for step in range(900, 300, -1):
        c = from_lch(step * .001, C0 * pct, H0)
        if cr("#FFFFFF", c) >= target:
            return c
    return "#8E7245"

# LONE glyph — no label, so the colour carries meaning: 1.4.11 non-text, 3:1. NOT 4.5 (that is the
# TEXT threshold, 1.4.3). Building this row at 4.5 was the error Dave caught — one rung too dark,
# which is what produced the ochre he would have rejected.
lonerow = "".join(
    f'<td class="cell"><span class="gl" style="color:{glyph_t(p, 3.0)}">{ARROW}</span>'
    f'<br><code>{glyph_t(p, 3.0)}</code><br>'
    f'<span class="r ok">{cr("#FFFFFF", glyph_t(p, 3.0)):.2f}</span>'
    f'<span class="met"> on page · 3.0 min</span></td>' for p, _ in CS)
textrow = "".join(
    f'<td class="cell"><span class="gl" style="color:{glyph_t(p, 4.5)}"><b>Pending</b></span>'
    f'<br><code>{glyph_t(p, 4.5)}</code><br>'
    f'<span class="r ok">{cr("#FFFFFF", glyph_t(p, 4.5)):.2f}</span>'
    f'<span class="met"> on page · 4.5 min</span></td>' for p, _ in CS)

t1 = from_lch(0.790, C0 * 0.85, H0)
t2 = glyph_t(0.85, 3.0)
t3 = glyph_t(0.85, 4.5)
r1a, r1b = cr(INK, t1), cr("#FFFFFF", t1)
r2, r3 = cr("#FFFFFF", t2), cr("#FFFFFF", t3)
L2 = oklch(t2)[0]

HTML = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>Amber — the matrix</title>
<style>
:root{{--ink:#1c1c1c;--mut:#6b6b6b;--line:#e4e4e4;--red:#db0011;--ok:#0b7a34}}
*{{box-sizing:border-box}}
body{{font-family:"HSBC_MtUnivers_Latin","Univers Next for HSBC","Helvetica Neue",Arial,sans-serif;
 color:var(--ink);margin:0;padding:40px;max-width:1080px;line-height:1.5;background:#fafafa}}
h1{{font-size:30px;font-weight:300;margin:0 0 4px}}
h2{{font-size:18px;font-weight:500;margin:34px 0 6px;padding-top:14px;border-top:2px solid var(--ink)}}
.sub{{color:var(--mut);font-size:13px;margin:0 0 18px}}
.lead{{font-size:15px;background:#fff;border:1px solid var(--line);border-left:3px solid var(--red);
 padding:16px 20px;margin:18px 0}}
.card{{background:#fff;border:1px solid var(--line);padding:15px 20px;margin:12px 0;font-size:14px}}
table{{width:100%;border-collapse:collapse;background:#fff;margin:12px 0;font-size:12px}}
th,td{{padding:12px 8px;border-bottom:1px solid var(--line);text-align:center;vertical-align:middle}}
th{{font-weight:500;font-size:11px;color:var(--mut);background:#f4f4f4}}
th.rh{{text-align:left;background:#fafafa;width:92px}}
.met{{color:var(--mut);font-size:10px}}
code{{font-family:ui-monospace,Menlo,monospace;font-size:10px;background:#f2f2f2;padding:1px 3px}}
.tag{{display:inline-flex;align-items:center;gap:5px;font-size:12px;padding:5px 10px;line-height:1}}
.gl{{display:inline-flex;align-items:center;gap:5px;font-size:12px}}
.clip{{color:var(--red);font-size:10px}}
.ask{{width:120px;background:#fffdf5}}
.foot{{color:var(--mut);font-size:12px;margin-top:38px;border-top:1px solid var(--line);padding-top:12px}}
</style></head><body>
<h1>Amber — darkness &times; saturation</h1>
<p class="sub">Apollo SDS &middot; 2026-07-18 &middot; hue held at {H0:.1f}° in every cell. Nothing promoted.</p>

<div class="lead"><b>Contrast is not the constraint here, and that is worth saying plainly.</b>
Every cell lands between <b>7.70 and 10.38</b> against the digital black — all AAA. Nothing in this
grid is gated by accessibility. <b>The choice is purely aesthetic, which makes it entirely yours</b>
— I have no basis to prefer one cell over another and will not pretend otherwise.</div>

<div class="card"><b>Why a matrix and not another ladder.</b> The last amber ladder varied chroma
only and chased a 7.0:1 target, which dragged every candidate to L&asymp;0.72 — darker than the
current <code>{BASE}</code> and back toward the brown you rejected. Darkness and saturation are two
independent moves; a single ladder cannot show their combination. Rows drop lightness, columns drop
chroma.</div>

<h2>The grid <span class="met">— rows darker &darr;, columns less saturated &rarr;</span></h2>
<table><thead><tr><th class="rh">lightness</th>{head}<th class="ask">Your pick</th></tr></thead>
<tbody>{rows}</tbody></table>
<p class="sub"><b>clipped</b> = outside sRGB; the conversion clamped it, so the swatch is not the
colour requested. Marked rather than hidden — an unmarked clip is a lie in a specimen.</p>

<h2>The glyph &mdash; and your ruling dissolves most of the problem</h2>
<div class="card"><b>&ldquo;Contrast with a white background is a luxury &mdash; the label carries
the meaning.&rdquo;</b> That is not a new position, it is <b>already this system's canon</b>, stated
in at least five snippets. Account-card: <i>&ldquo;Status dot is &lt; 3:1 standalone (1.4.11) so
meaning is carried by the label text (1.4.1).&rdquo;</i> Same in Status-indicator, Confirmation,
Countdown-timer and Links. <b>I built a dark amber glyph to satisfy a rule this system had already
and deliberately waived.</b><br><br>
<b>What follows:</b> where the icon is <code>aria-hidden</code> and the LABEL carries the state, the
icon is decorative &mdash; 1.4.11 does not apply, and the glyph <b>can stay light and match the
fill</b>. The ochre disappears.<br><br>
<b>The one case that survives:</b> amber as <b>TEXT</b>. Text IS the label, so 1.4.3 applies at
4.5:1 with no waiver. But that is answered by a rule rather than a token &mdash;
<b>&ldquo;amber is never a text colour&rdquo;</b> is simpler than maintaining a second amber, and it
costs nothing: the label sits in <code>{INK}</code> and the amber does the signalling.</div>

<h2>The three tiers &mdash; by how much work the colour is doing</h2>
<p class="sub">Every ratio is against a white page. <b>The threshold changes with the JOB</b>, not
with the colour &mdash; which is the whole point.</p>
<table><thead><tr><th class="rh">tier</th><th>what it is</th><th>rule</th><th>target</th><th>value</th><th>measured</th><th class="ask">Your call</th></tr></thead><tbody>
<tr><th class="rh">1</th><td style="text-align:left">fill, and glyph <b>WITH</b> a label</td>
 <td>1.4.1 &mdash; label carries meaning</td><td><b>none</b><br><span class="met">waived</span></td>
 <td><span class="tag" style="background:{t1};color:{INK}">{TICK}<span>Pending</span></span><br><code>{t1}</code></td>
 <td><span class="r ok">{r1a:.2f}</span> <span class="met">ink on fill (&ge;4.5)</span><br>
     <span class="r ok">{r1b:.2f}</span> <span class="met">fill vs page &mdash; no target</span></td><td class="ask"></td></tr>
<tr><th class="rh">2</th><td style="text-align:left">glyph <b>ALONE</b>, no label</td>
 <td>1.4.11 &mdash; non-text</td><td><b>3.0</b></td>
 <td><span class="gl" style="color:{t2}">{ARROW}</span> <code>{t2}</code></td>
 <td><span class="r ok">{r2:.2f}</span> <span class="met">on page (&ge;3.0)</span></td><td class="ask"></td></tr>
<tr><th class="rh">3</th><td style="text-align:left">amber as <b>TEXT</b></td>
 <td>1.4.3 &mdash; text</td><td><b>4.5</b></td>
 <td><span class="gl" style="color:{t3}"><b>Pending</b></span> <code>{t3}</code></td>
 <td><span class="r ok">{r3:.2f}</span> <span class="met">on page (&ge;4.5)</span></td><td class="ask"></td></tr>
</tbody></table>

<div class="card"><b>Belt and braces &mdash; Dave's framing, and it is the mechanism.</b> Red, green
and blue clear 4.5:1 on a white page unaided, so they carry the label <i>and</i> the contrast.
<b>Amber only ever has the belt.</b> Remove the label and the belt is gone &mdash; which is exactly
when tier 2 is required, and why it exists at all.<br><br>
<b>Correction on the record:</b> I first built the lone-glyph value at <b>4.5:1</b>
(<code>{t3}</code>, L&nbsp;0.573) &mdash; that is the <b>TEXT</b> threshold. A lone icon needs
<b>3:1</b>, giving <code>{t2}</code> at L&nbsp;{L2:.3f}: one rung lighter, and still amber rather
than the ochre. Wrong rung, not wrong idea.</div>

<h2>A &middot; Tier 1 &mdash; decorative glyph <span class="met">(the rule: accompanied by a label)</span></h2>
<p class="sub">Light amber icon, <code>{INK}</code> label. Row L 0.790 &mdash; the icon matches the fill.</p>
<table><thead><tr><th class="rh">glyph</th>{head}<th class="ask">Your pick</th></tr></thead>
<tbody><tr><th class="rh">decorative<br><span class="met">no target</span></th>{decrow}<td class="ask"></td></tr></tbody></table>

<h2>B &middot; Tier 2 &mdash; lone glyph <span class="met">(1.4.11 &middot; 3:1)</span></h2>
<table><thead><tr><th class="rh">glyph</th>{head}<th class="ask">Your pick</th></tr></thead>
<tbody><tr><th class="rh">alone<br><span class="met">3.0 min</span></th>{lonerow}<td class="ask"></td></tr></tbody></table>

<h2>C &middot; Tier 3 &mdash; amber as text <span class="met">(1.4.3 &middot; 4.5:1)</span></h2>
<p class="sub">Shown for completeness. If Q4 rules amber is never a text colour, this tier is deleted.</p>
<table><thead><tr><th class="rh">glyph</th>{head}<th class="ask">Your pick</th></tr></thead>
<tbody><tr><th class="rh">text<br><span class="met">4.5 min</span></th>{textrow}<td class="ask"></td></tr></tbody></table>

<h2>Your marks</h2>
<table><thead><tr><th style="text-align:left">question</th><th class="ask">your call</th></tr></thead><tbody>
<tr><td style="text-align:left"><b>Q1.</b> Which cell for the amber <b>background</b>? (row + column, e.g. &ldquo;&minus;5% / &minus;28%&rdquo;)</td><td class="ask"></td></tr>
<tr><td style="text-align:left"><b>Q2.</b> Which column for the amber <b>glyph</b>? It need not match the background's column.</td><td class="ask"></td></tr>
<tr><td style="text-align:left"><b>Q3.</b> Still recognisably <i>amber</i> at the bottom of the grid, or does it turn before then?</td><td class="ask"></td></tr>
<tr><td style="text-align:left"><b>Q4.</b> <b>Is amber ever a text colour?</b> If no, section B is deleted and amber collapses to ONE value — the carve-out shrinks from "dark ink + separate glyph" to just "dark ink on its fill".</td><td class="ask"></td></tr>
</tbody></table>

<p class="foot">Apollo SDS &middot; AMBER-MATRIX-2026-07-18 &middot; generated by <code>reviews/gen_amber_matrix.py</code>.
OKLCh in-file with sRGB gamut check; contrast per WCAG 2.x. Ink = <code>{INK}</code> (R-D1).</p>
</body></html>"""

open(OUT, "w").write(HTML)
print(f"wrote {os.path.relpath(OUT, ROOT)} — {len(LS)}×{len(CS)} grid + paired glyphs")
