#!/usr/bin/env python3
"""gen_rag_matting.py — the matting ladder, shown on the artefacts.

Dave, 2026-07-18: *"maybe we matt them a little, the red is good but the others are looking like a
Benetton advert, correct hue."* Plus, per hue: amber *"too saturated, and maybe too light… a little
more 'grown up' but it still pops"*; green *"adjust saturation down a bit"*; blue *"I love this hue,
we might have to adjust the sat and brightness"*.

METHOD — why OKLCh and not HSL/HSV
  "Saturation" in HSL is not perceptual: equal HSL saturation across hues does NOT look equally
  vivid, so matting in HSL bends the hue and changes the apparent lightness. OKLCh separates
  Lightness / Chroma / Hue perceptually, so chroma can be pulled down with the HUE HELD EXACTLY —
  which is what Dave asked for ("correct hue").

  MEASURED FIRST, and it corrected the brief: green is ALREADY less chromatic than red (0.72x) and
  blue is EQUAL to red (1.00x). So the Benetton read is not simply "too saturated" — blue and amber
  also sit LIGHTER and more primary. Hence L is tuned alongside C, not held.

CONTRAST MARGIN IS BUILT IN, deliberately
  R-D1 flagged that green (+0.11), blue (+0.10) cleared 4.5 by less than a rounding step. Every
  candidate here targets 5.0 for white text and 7.0 for dark ink on amber, so matting BUYS the
  margin instead of spending it. Two problems, one move.

Usage:  python3 reviews/gen_rag_matting.py
Then:   python3 knowledge/_review/_make_review.py reviews/RAG-MATTING-2026-07-18.html
"""
import os, math

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "reviews", "RAG-MATTING-2026-07-18.html")
INK = "#1A1A1A"


def s2l(c): return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
def l2s(c):
    c = max(0.0, min(1.0, c))
    return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055
def hex2lin(h):
    h = h.lstrip("#"); return [s2l(int(h[i:i + 2], 16) / 255) for i in (0, 2, 4)]
def lin2hex(r, g, b): return "#%02X%02X%02X" % tuple(round(l2s(x) * 255) for x in (r, g, b))

M1 = [[0.4122214708, 0.5363325363, 0.0514459929], [0.2119034982, 0.6806995451, 0.1073969566],
      [0.0883024619, 0.2817188376, 0.6299787005]]
M2 = [[0.2104542553, 0.7936177850, -0.0040720468], [1.9779984951, -2.4285922050, 0.4505937099],
      [0.0259040371, 0.7827717662, -0.8086757660]]


def oklch(h):
    r, g, b = hex2lin(h)
    l, m, s = [sum(M1[i][j] * [r, g, b][j] for j in range(3)) for i in range(3)]
    l, m, s = [x ** (1 / 3) if x > 0 else -((-x) ** (1 / 3)) for x in (l, m, s)]
    L, a, b2 = [sum(M2[i][j] * [l, m, s][j] for j in range(3)) for i in range(3)]
    return L, math.hypot(a, b2), math.degrees(math.atan2(b2, a)) % 360


def from_lch(L, C, H):
    a, b = C * math.cos(math.radians(H)), C * math.sin(math.radians(H))
    l_, m_, s_ = L + .3963377774 * a + .2158037573 * b, L - .1055613458 * a - .0638541728 * b, \
                 L - .0894841775 * a - 1.2914855480 * b
    l, m, s = l_ ** 3, m_ ** 3, s_ ** 3
    Mi = [[4.0767416621, -3.3077115913, 0.2309699292], [-1.2684380046, 2.6097574011, -0.3413193965],
          [-0.0041960863, -0.7034186147, 1.7076147010]]
    return lin2hex(*[sum(Mi[i][j] * [l, m, s][j] for j in range(3)) for i in range(3)])


def lum(h):
    r, g, b = hex2lin(h); return .2126 * r + .7152 * g + .0722 * b
def cr(a, b):
    l1, l2 = sorted([lum(a), lum(b)], reverse=True); return (l1 + .05) / (l2 + .05)


def tune(base, mode, target, pct):
    L, C, H = oklch(base)
    rng = range(60, -260, -1) if mode == "white" else range(-260, 60)
    for step in rng:
        cand = from_lch(L + step * .001, C * pct, H)
        v = cr("#FFFFFF", cand) if mode == "white" else cr(INK, cand)
        if v >= target:
            return cand, v
    return base, cr("#FFFFFF" if mode == "white" else INK, base)


ARROW = ('<svg viewBox="0 0 16 16" width="16" height="16" aria-hidden="true"><path d="M3 8h9'
         'M8.5 4.5L12 8l-3.5 3.5" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>')
TICK = ('<svg viewBox="0 0 16 16" width="16" height="16" aria-hidden="true"><path d="M3 8.5l3.5 3'
        'L13 5" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>')
STEPS = [(1.00, "as now"), (0.85, "matted 15%"), (0.72, "matted 28%"), (0.60, "matted 40%")]
HUES = [("amber", "#FFBB33", "ink", 7.0), ("green", "#16864E", "white", 5.0),
        ("blue", "#2573DC", "white", 5.0)]


def carriers(bg, ink, glyph=None):
    """bg = the FILL. glyph = the colour for arrows/text on the PAGE.

    They are the same for red/green/blue — those hues sit at mid luminance and work in both
    roles. For AMBER they must diverge: the fill is light (dark ink on it), but a glyph on a
    white page has to be dark to clear 4.5:1. Passing glyph=bg for amber is exactly the bug
    Dave caught — it rendered an illegible amber arrow and contradicted the ground/glyph split.
    """
    g = glyph or bg
    return (f'<span class="tag" style="background:{bg};color:{ink}">Pending</span>'
            f'<span class="badge" style="background:{bg};color:{ink}">{TICK}<span>Complete</span></span>'
            f'<span class="gl" style="color:{g}">{ARROW}</span>'
            f'<span class="gl" style="color:{g}"><b>Status</b></span>')


def glyph_for(base, pct):
    """Darkest-permissible glyph on a white page at this chroma — 4.5:1, hue held."""
    L, C, H = oklch(base)
    for step in range(60, -400, -1):
        cand = from_lch(L + step * .001, C * pct, H)
        if cr("#FFFFFF", cand) >= 4.5:
            return cand
    return base


def block(name, base, mode, target):
    L0, C0, H0 = oklch(base)
    rows = ""
    for pct, label in STEPS:
        cand, v = tune(base, mode, target, pct)
        ink = INK if mode == "ink" else "#FFFFFF"
        L, C, H = oklch(cand)
        # amber alone needs a separate glyph value; the others double as their own
        gl = glyph_for(base, pct) if mode == "ink" else cand
        glnote = (f'<br><span class="met">glyph <code>{gl}</code></span>'
                  if gl != cand else '')
        rows += (f'<tr><td><b>{label}</b><br><span class="met">C {C:.3f}</span></td>'
                 f'<td><code>{cand}</code><br><span class="met">L {L:.3f} · H {H:.1f}°</span>{glnote}</td>'
                 f'<td class="car">{carriers(cand, ink, gl)}</td>'
                 f'<td class="c"><span class="r ok">{v:.2f}</span><br><span class="met">'
                 f'{"dark ink" if mode == "ink" else "white text"}</span>'
                 f'<br><span class="r ok">{cr("#FFFFFF", gl):.2f}</span>'
                 f'<span class="met"> glyph/page</span></td>'
                 f'<td class="ask"></td></tr>')
    return (f'<h2>{name.title()} <span class="met">— hue held at {H0:.1f}°</span></h2>'
            f'<p class="sub">Current <code>{base}</code> — L {L0:.3f}, C {C0:.3f}. '
            f'Chroma falls down the table; hue does not move.</p>'
            f'<table><thead><tr><th>Step</th><th>Value</th><th>Tag · badge · arrow · text</th>'
            f'<th>Contrast</th><th class="ask">Your pick</th></tr></thead><tbody>{rows}</tbody></table>')


HTML = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>RAG — the matting ladder</title>
<style>
:root{{--ink:#1c1c1c;--mut:#6b6b6b;--line:#e4e4e4;--red:#db0011;--ok:#0b7a34}}
*{{box-sizing:border-box}}
body{{font-family:"HSBC_MtUnivers_Latin","Univers Next for HSBC","Helvetica Neue",Arial,sans-serif;
 color:var(--ink);margin:0;padding:40px;max-width:1120px;line-height:1.5;background:#fafafa}}
h1{{font-size:30px;font-weight:300;margin:0 0 4px}}
h2{{font-size:19px;font-weight:500;margin:38px 0 4px;padding-top:14px;border-top:2px solid var(--ink)}}
.sub{{color:var(--mut);font-size:13px;margin:0 0 14px}}
.lead{{font-size:15px;background:#fff;border:1px solid var(--line);border-left:3px solid var(--red);
 padding:16px 20px;margin:18px 0}}
.card{{background:#fff;border:1px solid var(--line);padding:16px 20px;margin:12px 0;font-size:14px}}
table{{width:100%;border-collapse:collapse;background:#fff;margin:10px 0;font-size:13px}}
th,td{{text-align:left;padding:12px 10px;border-bottom:1px solid var(--line);vertical-align:middle}}
th{{font-weight:500;font-size:11px;letter-spacing:.04em;color:var(--mut);background:#f4f4f4}}
td.c{{text-align:center}} td.car{{white-space:nowrap}}
.met{{color:var(--mut);font-size:11px}}
code{{font-family:ui-monospace,Menlo,monospace;font-size:11px;background:#f2f2f2;padding:1px 4px}}
.r{{font-weight:500;font-size:13px}} .ok{{color:var(--ok)}}
.tag{{display:inline-flex;align-items:center;font-size:12px;padding:3px 9px;line-height:1;margin-right:10px}}
.badge{{display:inline-flex;align-items:center;gap:6px;font-size:12px;padding:4px 9px;line-height:1;margin-right:12px}}
.gl{{display:inline-flex;align-items:center;font-size:13px;margin-right:12px;vertical-align:middle}}
.ask{{width:130px;background:#fffdf5}}
.anchor{{background:#fff;border:1px solid var(--line);padding:14px 20px;margin:12px 0}}
.foot{{color:var(--mut);font-size:12px;margin-top:40px;border-top:1px solid var(--line);padding-top:12px}}
</style></head><body>
<h1>The matting ladder</h1>
<p class="sub">Apollo SDS &middot; 2026-07-18 &middot; hue held exactly, chroma pulled down, shown on the four carriers. Nothing promoted.</p>

<div class="lead"><b>Measuring first corrected the brief.</b> In OKLCh — where chroma is
perceptual, unlike HSL saturation — <b>green is already LESS chromatic than red (0.72&times;) and
blue is exactly EQUAL to it (1.00&times;)</b>. So "too saturated" isn't quite the whole story: blue
and amber also sit <b>lighter</b> and more primary than red, and lightness is doing much of the
Benetton work. Each ladder therefore moves L as well as C — while holding hue to the decimal, which
is what you asked for.</div>

<div class="anchor"><b>Red — the anchor, unchanged.</b> <code>#B92F1E</code> · L 0.520 · C 0.177 ·
H 30.7° · white text 6.02<br><span style="margin-top:8px;display:inline-block">{carriers('#B92F1E', '#FFFFFF')}</span></div>

<div class="card"><b>The matting also buys back the margin.</b> R-D1 flagged that green and blue
cleared 4.5:1 by about a tenth — less than a rounding step, so any later nudge would silently drop
them below AA. Every candidate below targets <b>5.0</b> for white text (and <b>7.0</b> for dark ink
on amber), so making them more grown-up and making them safe is <b>one move, not two</b>.</div>

{''.join(block(*h) for h in HUES)}

<h2>The amber glyph — a constraint, not a tuning problem</h2>
<div class="card"><b>You spotted that the amber glyph was broken, and the first version of this
sheet was genuinely wrong</b> — it painted the arrow and text in the FILL colour, which for amber
is light and illegible on a white page. Fixed above: amber now carries its own glyph value.<br><br>
<b>But the fix exposes the real issue.</b> To clear 4.5:1 on a white page an amber glyph has to sit
at about <b>L 0.57</b>. At that lightness the hue reads as <b>dark gold / ochre</b> — it cannot
look like the light amber of the fill, at any chroma. That is not a tuning failure, it is the hue:
amber's identity IS lightness, so an amber that is dark enough to be a glyph has stopped looking
like amber. Red, green and blue have no such problem because they live at mid luminance already.
<br><br><b>Three honest ways out:</b><br>
&mdash; <b>Accept the divergence.</b> Amber ground light, amber glyph ochre. Linked by role, not by
appearance. Costs: the pair looks like two colours, and someone will "fix" it later.<br>
&mdash; <b>Amber has no bare glyph.</b> Amber only ever appears as a FILL — tag, badge, chip. A
standalone amber arrow or amber sentence is simply not permitted; warning status is always carried
by a filled carrier. <b>My recommendation</b> — it matches how warning states are normally built,
and it removes the case rather than compromising it.<br>
&mdash; <b>Outline instead.</b> Light amber fill with a darker amber border, so the EDGE carries the
3:1 and the glyph question never arises. Adds a border to a square mono component — a look decision.
</div>

<h2>Questions</h2>
<table><thead><tr><th>question</th><th class="ask">your call</th></tr></thead><tbody>
<tr><td><b>Q0.</b> The amber glyph: accept the divergence · no bare amber glyph (recommended) · outline the fill?</td><td class="ask"></td></tr>
<tr><td><b>Q1.</b> One matting level across all three for consistency, or per-hue?</td><td class="ask"></td></tr>
<tr><td><b>Q2.</b> Amber's ladder is notably darker than the current <code>#FFBB33</code> (L 0.83 &rarr; ~0.72) — that is the "too light" fix. Far enough, or too far toward the brown you rejected?</td><td class="ask"></td></tr>
<tr><td><b>Q3.</b> Red stays as-is — or does it get matted a touch too, once the others move?</td><td class="ask"></td></tr>
</tbody></table>

<p class="foot">Apollo SDS &middot; RAG-MATTING-2026-07-18 &middot; generated by <code>reviews/gen_rag_matting.py</code>.
OKLCh conversion in-file; contrast per WCAG 2.x relative luminance. Ink = <code>{INK}</code> (R-D1).</p>
</body></html>"""

open(OUT, "w").write(HTML)
print(f"wrote {os.path.relpath(OUT, ROOT)}")
