#!/usr/bin/env python3
"""Hand-rolled geometry helper for the Apollo round-one chart kit (method decision 6: hand-rolled
maths first, d3-scale only when time-axes demand it). Emits the static, gate-visible SVG charts into
knowledge/_proforma/ as interactive MONO pro-forma files:

  DataViz-BarColumn-interactive.html   column · horizontal bar · grouped · stacked (+chevron)
  DataViz-Line-interactive.html        line · multi-series · sparkline
  DataViz-Donut-interactive.html       donut + centre total

The maths (nice ticks, linear scale, stack layout, arc geometry) lives here so it is inspectable; the
COORDINATES are baked into the DOM so every gate (knowledge/_validate_dataviz.py) can see the series
elements statically — a canvas/JS-injected chart would be invisible to the gate. Runtime JS in the
files is behaviour-only (theme/contrast/series toggle, tooltip) per rule 14; motion is CSS (DEF-003).

Run:  python3 knowledge/_review/_gen_dataviz_charts.py
Then: python3 knowledge/_build_all.py   (the DataViz gate + the four pro-forma gates check the output)
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
import os, math

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, "..", "_proforma"))
LETTERS = ["A", "B", "C", "D", "E"]

# ---------------- hand-rolled scale maths ----------------
def nice_max(v, ticks=4):
    """Smallest 'nice' number >= v (1/2/2.5/5 * 10^k), so the axis top is legible."""
    if v <= 0:
        return 1
    raw = v / ticks
    mag = 10 ** math.floor(math.log10(raw))
    for m in (1, 2, 2.5, 5, 10):
        if raw <= m * mag:
            step = m * mag
            break
    top = math.ceil(v / step) * step
    return top, step

def ticks(top, step):
    n = int(round(top / step))
    return [round(step * i, 4) for i in range(n + 1)]

def fmt(v):
    v = round(v, 2)
    return str(int(v)) if v == int(v) else ("%.1f" % v)

def line_node_delays(n, dur, x1=0.33, x2=0.30):
    """Delay (ms) for each line node so it appears when the LINE'S drawing head reaches it — i.e. the
    node cadence follows the line's easing (cubic-bezier x1,x2 with y1=0,y2=1), not a linear gap.
    The line's progress is Y(u)=3u^2-2u^3; node i wants Y=i/(n-1); its time is X(u)*dur."""
    if n <= 1:
        return [0.0]
    out = []
    for i in range(n):
        f = i / (n - 1)
        lo, hi = 0.0, 1.0
        for _ in range(40):                      # bisect u where Y(u)=f (Y monotonic)
            u = (lo + hi) / 2
            if 3 * u * u - 2 * u ** 3 < f: lo = u
            else: hi = u
        u = (lo + hi) / 2
        x = 3 * (1 - u) ** 2 * u * x1 + 3 * (1 - u) * u * u * x2 + u ** 3
        out.append(x * dur)
    return out

# ---------------- shared head / chrome ----------------
TOKENS = """  :root{
    --card-grow:1.006; --bw-sm:1px; --bw-md:2px; --bw-lg:4px; --radius:0; --radius-round:50%; --radius-pill:999px;
    --space-2:2px; --space-3:3px; --space-4:4px; --space-6:6px; --space-8:8px; --space-10:10px; --space-12:12px;
    --space-14:14px; --space-16:16px; --space-18:18px; --space-20:20px; --space-24:24px; --space-28:28px;
    --space-32:32px; --space-40:40px; --space-80:80px;
    --font:"Univers Next for HSBC","Helvetica Neue",Arial,Helvetica,sans-serif;
    /* type = KB typography.json (font-5/6/7 + weights). Display sizes (font-1..4) pending the two new Figma display
       types; --fs-display is a 4px-grid placeholder that will map cleanly when they land (Dave 2026-07-16). */
    --fw-regular:400; --fw-medium:500; --fw-bold:700;
    --fs-5:16px; --fs-6:14px; --fs-7:12px; --fs-display:40px;
    --ease:160ms cubic-bezier(.4,0,.2,1); --grow:760ms cubic-bezier(.22,.61,.36,1);
    /* the SAME 760ms as --grow, exposed alone: the DV-D16 stacked float needs a per-animation
       timing function, so it cannot use the duration+easing shorthand. Change both together. */
    --grow-dur:760ms;
    /* ★ s218-D5 (1) — THE STACKED TRIO'S CURVES ARE THE HOUSE FAMILY, NOT THE CSS KEYWORDS.
       --grow-ease-out IS --grow's curve; --grow-ease-in is its exact reversal (1-x2, 1-y2,
       1-x1, 1-y1), so the bottom segment reads the same gesture backwards. Intermediates stay
       `linear` — DV-D16's positional rule is unchanged, only the two curves joined the family.
       Same two tokens, same values, as the ENACTED Chart-bar.reference.html. */
    --grow-ease-out:cubic-bezier(.22,.61,.36,1);
    --grow-ease-in:cubic-bezier(.64,0,.78,.39);
    --draw:1000ms cubic-bezier(.22,.61,.36,1); --draw-slow:2400ms cubic-bezier(.33,0,.3,1);
  }
  [data-theme="light"]{
    --page:#FFFFFF; --raised:#F3F3F3; --ink:#333333; --ink2:#545454; --disi:#B7B7B7; --line:#D7D8D6; --line2:#EDEDED;
    --pri:#1A1A1A; --focus:#1A1A1A;
    --data-series-1:#766682; --data-series-2:#A45C3A; --data-series-3:#577C78; --data-series-4:#7F7B45; --data-series-5:#A37E94;
    --data-series-hc-1:#484D6F; --data-series-hc-2:#97482C; --data-series-hc-3:#385F4F; --data-series-hc-4:#6E465D; --data-series-hc-5:#7C6F34;
    --data-delta-gain:#16864E; --data-delta-loss:#B92F1E; --data-delta-neutral:#2573DC;
    --dv-axis:#545454; --dv-label:#545454; --dv-baseline:#333333; --dv-grid:#EDEDED;
    --dv-marker-fill:#FFFFFF; --shadow:#00000026;
    --drawer-bg:#FFFFFF; --drawer-ink:#1A1A1A; --drawer-ink2:#545454; --drawer-line:#D7D8D6;
  }
  [data-theme="dark"]{
    --page:#000000; --raised:#1D1D1D; --ink:#FFFFFF; --ink2:#9B9B9B; --disi:#767676; --line:#707070; --line2:#3A3A3A;
    --pri:#F2F2F2; --focus:#FFFFFF;
    --data-series-1:#766682; --data-series-2:#A45C3A; --data-series-3:#577C78; --data-series-4:#7F7B45; --data-series-5:#A37E94;
    --data-series-hc-1:#93B6CC; --data-series-hc-2:#E5A78F; --data-series-hc-3:#90BA9B; --data-series-hc-4:#D197A6; --data-series-hc-5:#E5C283;
    --data-delta-gain:#1AA05C; --data-delta-loss:#CC4333; --data-delta-neutral:#2674DC;
    --dv-axis:#9B9B9B; --dv-label:#9B9B9B; --dv-baseline:#FFFFFF; --dv-grid:#3A3A3A;
    --dv-marker-fill:#FFFFFF; --shadow:#000000D9;
    --drawer-bg:#FFFFFF; --drawer-ink:#1A1A1A; --drawer-ink2:#545454; --drawer-line:#D7D8D6;
  }
  [data-contrast="high"]{
    --data-series-1:var(--data-series-hc-1); --data-series-2:var(--data-series-hc-2); --data-series-3:var(--data-series-hc-3);
    --data-series-4:var(--data-series-hc-4); --data-series-5:var(--data-series-hc-5);
  }"""

BASE_CSS = """  *{box-sizing:border-box;}
  body{margin:0; font-family:var(--font); background:var(--page); color:var(--ink); -webkit-font-smoothing:antialiased;
    transition:background var(--ease), color var(--ease); line-height:1.5;}
  .wrap{max-width:920px; margin:0 auto; padding:0 var(--space-28) var(--space-80);}
  .top{position:sticky; top:0; z-index:20; background:var(--page); border-bottom:var(--bw-sm) solid var(--line2);
    display:flex; align-items:center; justify-content:space-between; padding:var(--space-14) var(--space-28);
    margin:0 calc(-1 * var(--space-28)) var(--space-8); gap:var(--space-12); flex-wrap:wrap;}
  .top .t{font:500 15px/1 var(--font);} .top .t small{color:var(--ink2); font-weight:400; margin-left:var(--space-8);}
  .ctrls{display:flex; align-items:center; gap:var(--space-12);}
  .tgl{font:500 13px/1 var(--font); padding:var(--space-8) var(--space-14); border:var(--bw-sm) solid var(--line);
    background:transparent; color:var(--ink); cursor:pointer; border-radius:var(--radius);}
  .tgl[aria-pressed="true"]{background:var(--pri); color:var(--page); border-color:var(--pri);}
  .tgl:focus-visible{outline:var(--bw-md) solid var(--focus); outline-offset:2px;}
  section{padding:var(--space-32) 0; border-top:var(--bw-sm) solid var(--line2);}
  section:first-of-type{border-top:0;}
  .h{display:flex; align-items:baseline; gap:var(--space-12); margin-bottom:var(--space-6); flex-wrap:wrap;}
  .h h2{font:500 19px/1.2 var(--font); margin:0;} .h .tag{font:500 11px/1 var(--font); color:var(--ink2);}
  .sub{color:var(--ink2); font:400 13px/1.5 var(--font); margin:0 0 var(--space-20); max-width:66ch;}
  .sr-only{position:absolute; width:1px; height:1px; padding:0; margin:calc(-1 * var(--space-2)); overflow:hidden; clip:rect(0,0,0,0); white-space:nowrap; border:0;}
  figure.dv{margin:0; max-width:100%;}
  .dv-svg{display:block; width:100%; height:auto; overflow:visible;}
  .dv-axis{stroke:var(--dv-axis); stroke-width:1; vector-effect:non-scaling-stroke;}
  .dv-grid{stroke:var(--dv-grid); stroke-width:1; vector-effect:non-scaling-stroke;}
  text.dv-label,text.dv-axis{fill:var(--dv-label); font:400 11px/1 var(--font); stroke:none;}
  text.dv-val{fill:var(--ink); font:600 11px/1 var(--font); stroke:none; font-variant-numeric:tabular-nums;}
  text.dv-key-el{font:700 11px/1 var(--font); stroke:none;}
  .dv-legend{list-style:none; display:flex; flex-wrap:wrap; gap:var(--space-16); margin:var(--space-14) 0 0; padding:0;}
  .dv-legend li{display:flex; align-items:center; gap:var(--space-8); font:400 12px/1 var(--font); color:var(--ink);}
  .dv-legend .sw{width:var(--space-12); height:var(--space-12); flex:none;}
  .dv-legend .dv-key{font-weight:700; color:var(--ink2); min-width:var(--space-12); font-variant-numeric:tabular-nums;}
  .dv-legend button{background:transparent; border:0; padding:0; margin:0; font:inherit; color:inherit; cursor:pointer; display:flex; align-items:center; gap:var(--space-8);}
  .dv-legend button[aria-pressed="false"]{opacity:.4;}
  .dv-legend button:focus-visible{outline:var(--bw-md) solid var(--focus); outline-offset:2px;}
  .tbl-toggle{margin-top:var(--space-12); font:500 12px/1 var(--font); color:var(--ink); background:transparent;
    border:var(--bw-sm) solid var(--line); padding:var(--space-6) var(--space-12); cursor:pointer; border-radius:var(--radius);}
  .tbl-toggle:focus-visible{outline:var(--bw-md) solid var(--focus); outline-offset:2px;}
  table.dv-table{border-collapse:collapse; margin-top:var(--space-14); font:400 12px/1.4 var(--font); color:var(--ink);}
  table.dv-table caption{text-align:left; color:var(--ink2); font-size:11px; margin-bottom:var(--space-6);}
  table.dv-table th,table.dv-table td{border:var(--bw-sm) solid var(--line2); padding:var(--space-4) var(--space-10); text-align:right;}
  table.dv-table th[scope=row]{text-align:left; font-weight:500;}
  table.dv-table thead th{color:var(--ink2); font-weight:600;}
  table.dv-table[hidden]{display:none;}
  .note{font:400 12px/1.5 var(--font); color:var(--ink2); margin-top:var(--space-16); max-width:72ch;}
  .note code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace; font-size:11px; background:var(--line2); padding:0 var(--space-4);}
"""

KPI_CSS = """
  .kpi-grid{display:flex; gap:var(--space-16); flex-wrap:wrap; align-items:stretch;}
  .kpi{display:flex; flex-direction:column; gap:var(--space-8); min-width:210px; flex:1 1 210px; max-width:280px;
    margin:0; padding:var(--space-18) var(--space-20); background:var(--raised); border:var(--bw-sm) solid var(--line2);
    border-radius:var(--radius); transition:transform var(--ease), border-color var(--ease);}
  .kpi:hover{transform:scale(var(--card-grow)); border-color:var(--line);}
  .kpi .kpi-label{font:500 12px/1.3 var(--font); color:var(--ink2);}
  /* headline: display size (4px-grid placeholder --fs-display) + one weight thinner (regular, KB font-weight) */
  .kpi .kpi-value{font-family:var(--font); font-size:var(--fs-display); line-height:1.05; font-weight:var(--fw-regular);
    color:var(--ink); font-variant-numeric:tabular-nums; letter-spacing:-.015em;}
  .kpi .kpi-value .unit{font-size:var(--fs-5); color:var(--ink2); font-weight:var(--fw-regular); margin-right:var(--space-2);}
  .kpi .kpi-foot{display:flex; align-items:center; gap:var(--space-8); flex-wrap:wrap; min-height:var(--space-20);}
  .delta{display:inline-flex; align-items:center; gap:var(--space-4); font:600 13px/1 var(--font); font-variant-numeric:tabular-nums;}
  .delta svg{width:10px; height:10px;} .delta .arrow{fill:currentColor;}
  .delta.gain{color:var(--data-delta-gain);} .delta.loss{color:var(--data-delta-loss);} .delta.flat{color:var(--data-delta-neutral);}
  .kpi-since{font:400 12px/1 var(--font); color:var(--ink2);}
  .spark-inline{display:block; width:100%; height:44px; margin-top:var(--space-4);}
  .spark-inline .dv-series{fill:none; stroke:var(--data-series-1); stroke-width:2; stroke-linecap:round; stroke-linejoin:round; vector-effect:non-scaling-stroke;}
  .spark-inline .dv-end{fill:var(--data-series-1);}
  .spark-inline .dv-base{stroke:var(--dv-grid); stroke-width:1; vector-effect:non-scaling-stroke;}
  @media (prefers-reduced-motion:no-preference){
    .spark-inline .dv-series{stroke-dasharray:600; stroke-dashoffset:600; animation:draw var(--draw) forwards;}
    .spark-inline .dv-end{opacity:0; animation:pop var(--ease) var(--draw) forwards;}
  }
  @keyframes draw{to{stroke-dashoffset:0;}} @keyframes pop{to{opacity:1;}}
"""

ANIM_CSS = """
  /* ---- entry animations (CSS-only, DEF-003) + hover interactions. Scoped to .dv-animate so a Replay re-triggers. ---- */
  rect.dv-series,path.dv-series{transition:filter var(--ease), opacity var(--ease);}
  rect.dv-series:hover,path.dv-series:hover{filter:brightness(1.12); cursor:pointer;}
  [data-theme="dark"] rect.dv-series:hover,[data-theme="dark"] path.dv-series:hover{filter:brightness(1.22);}
  .dv-legend button:hover{text-decoration:underline; text-underline-offset:3px;}
  @media (prefers-reduced-motion:no-preference){
    .dv-animate .dv-series[data-grow="up"]{transform-box:fill-box; transform-origin:bottom; animation:dvGrowY var(--grow) both;}
    .dv-animate .dv-series[data-grow="right"]{transform-box:fill-box; transform-origin:left; animation:dvGrowX var(--grow) both;}
    /* line builds slower + sequentially (per-series inline delay); markers land after each line finishes */
    .dv-animate .dv-svg polyline.dv-series{stroke-dasharray:2400; stroke-dashoffset:2400; animation:dvDraw var(--draw-slow) forwards;}
    .dv-animate .dv-svg g.dv-marker{opacity:0; animation:dvFade var(--ease) both;}
    /* donut segments RADIALLY SWEEP, sequentially — driven by JS (Dave review #7), so no CSS transform here */
    /* grouped letters RISE with the bar (per-element --rise + delay) — Dave review #3 */
    .dv-animate text.dv-key-el[data-rise]{animation:dvRise var(--grow) both;}
    .dv-animate text.dv-key-el:not([data-rise]):not(.dv-anno),.dv-animate text.dv-val{opacity:0; animation:dvFade var(--ease) both; animation-delay:calc(var(--grow) * 0.7);}
  }
  /* donut labels/legs fade in AS their segment grows (JS toggles .show) — sequenced with the sweep (#2) */
  .dv-anno{opacity:0; transition:opacity 240ms ease;}
  .dv-anno.show{opacity:1;}
  @keyframes dvGrowY{from{transform:scaleY(0);} to{transform:scaleY(1);}}
  @keyframes dvGrowX{from{transform:scaleX(0);} to{transform:scaleX(1);}}
  @keyframes dvRise{from{transform:translateY(var(--rise,12px)); opacity:0;} to{transform:translateY(0); opacity:1;}}
  @keyframes dvDraw{to{stroke-dashoffset:0;}}
  @keyframes dvFade{from{opacity:0;} to{opacity:1;}}
  /* ---- donut layouts (#4 legend-right vertical · #5 direct labelling) ---- */
  .dv-donut-row{display:flex; gap:var(--space-28); align-items:center; flex-wrap:wrap;}
  .dv-legend.vert{flex-direction:column; gap:var(--space-10); margin-top:0;}
  .dv-leader{stroke:var(--line); stroke-width:1; fill:none; vector-effect:non-scaling-stroke;}
  text.dv-direct{fill:var(--ink); font:500 11px/1 var(--font); stroke:none;}
  text.dv-direct .amt{font-weight:600;}
  .variant-tabs{display:flex; gap:var(--space-8); margin-bottom:var(--space-16);}
  .variant-tabs button{font:500 12px/1 var(--font); padding:var(--space-6) var(--space-12); border:var(--bw-sm) solid var(--line);
    background:transparent; color:var(--ink); cursor:pointer; border-radius:var(--radius);}
  .variant-tabs button[aria-selected="true"]{background:var(--pri); color:var(--page); border-color:var(--pri);}
  .variant-tabs button:focus-visible{outline:var(--bw-md) solid var(--focus); outline-offset:2px;}
  .variant[hidden]{display:none;}
  /* fit charts: fixed height so runtime fit() maps the viewBox 1:1 (text never scales); width compresses */
  .dv-svg.dv-fit{height:260px;}
  /* legend centring (#4) */
  .dv-legend.center{justify-content:center;}
  /* chart toolbar ABOVE the chart (#2) — holds the table control; extensible for more */
  .dv-toolbar{display:flex; gap:var(--space-8); justify-content:flex-end; align-items:center; margin-bottom:var(--space-10); flex-wrap:wrap;}
  /* markers (#4/#5) — CSS-driven from --sc (series colour). WHITE: white fill + colour border at line width;
     BACKGROUND: colour fill + page-colour border. Border width = line width (2.5) either way. */
  .dv-mk{vector-effect:non-scaling-stroke; stroke-width:2.5; fill:var(--dv-marker-fill); stroke:var(--sc);}
  .dv-mk-cross{vector-effect:non-scaling-stroke; stroke-width:2.5; stroke:var(--sc); fill:none;}
  .marker-scope[data-marker="white"] .dv-mk{fill:var(--dv-marker-fill); stroke:var(--sc);}
  .marker-scope[data-marker="bg"] .dv-mk{fill:var(--sc); stroke:var(--page);}
  /* table DRAWER = a frosted OVERLAY on the right of the chart (#1/#3) — the chart KEEPS its width;
     the panel is sized to the table + padding, white background + backdrop blur. */
  .dv-stage{position:relative; width:100%;}
  .dv-chart-area{width:100%; min-width:0;}
  .dv-drawer{position:absolute; top:0; right:0; height:100%; display:flex; align-items:flex-start;
    justify-content:flex-end; pointer-events:none; opacity:0; transform:translateX(8px);
    transition:opacity var(--ease), transform var(--ease);}
  .dv-drawer.open{opacity:1; transform:none; pointer-events:auto;}
  /* #2: no scroll — the panel sizes to the table and EXTENDS beyond the chart bounds if taller.
     #3: solid white, no frost/blur. */
  .dv-drawer-inner{width:max-content; max-width:min(100%,440px);
    padding:var(--space-12) var(--space-16); background:var(--drawer-bg);
    border:var(--bw-sm) solid var(--drawer-line); box-shadow:0 4px 20px var(--shadow); color:var(--drawer-ink);}
  .dv-drawer-inner .dv-table{margin:0; color:var(--drawer-ink);}
  .dv-drawer-inner .dv-table caption,.dv-drawer-inner .dv-table thead th{color:var(--drawer-ink2);}
  .dv-drawer-inner .dv-table th[scope=row]{color:var(--drawer-ink);}
  .dv-drawer-inner .dv-table th,.dv-drawer-inner .dv-table td{border-color:var(--drawer-line);}
  table.dv-table{margin-top:0;}
  /* responsive preview frame + width slider (start 1024) */
  .dv-frame{width:var(--fw,100%); max-width:100%; margin:0 auto;}
  .wctl{display:flex; align-items:center; gap:var(--space-8); font:400 12px/1 var(--font); color:var(--ink2);}
  .wctl input[type=range]{accent-color:var(--ink); width:130px;}
  .wctl b{color:var(--ink); font-weight:500; min-width:46px; text-align:right; font-variant-numeric:tabular-nums;}
  /* real tooltip (#9) — figure + relevant info on hover/focus, not just a hover state */
  .dv-tip{position:fixed; z-index:80; pointer-events:none; opacity:0; transform:translateY(2px);
    transition:opacity var(--ease), transform var(--ease); background:var(--pri); color:var(--page);
    font:500 12px/1.35 var(--font); padding:var(--space-6) var(--space-10); border-radius:var(--radius);
    max-width:240px; box-shadow:0 2px 10px var(--shadow);}
  .dv-tip.on{opacity:1; transform:translateY(0);}
"""

# ---------------- DV-D16 wording ② — the stacked float (CSS only, DEF-003) ----------------
# ⚠⚠ WORDING ① IS REVERSED AND MUST NOT COME BACK. Until #219 this generator emitted the
# SERIAL shape Dave ruled and then rejected the same session — per-rect `animation-delay:
# seq*420ms` + `animation-duration:400ms` + the literal `ease-in`/`linear`/`ease-out` keywords,
# i.e. "segment 2 starts when segment 1 lands". Dave's second wording, IN FORCE:
#   "they all grow at the same time, so they are floating and growing, rather than growing and
#    'handing off' to the next."
# Every segment animates SIMULTANEOUSLY on ONE shared timeline; because a stack's upper segments
# sit on the segment below, growing them all at once makes the upper ones FLOAT upward while
# growing — that float IS the effect, and the stack must never gap open mid-flight.
#
# ⚠ WHY NOT THE OBVIOUS `translateY(--below × (1 − own progress))`: the segments below grow on
# DIFFERENT curves, so a translate driven by a segment's OWN curve tracks a height nothing has.
# DRIVEN at #218, not reasoned (knowledge/_render/verify_dv_d16_render.py): that shape opens the
# ruled dv-004 boundaries to 8.6–30.5px mid-flight. The float therefore rides the CUMULATIVE
# ANIMATED height below: N registered progress numbers animate ONCE on the chart, and every rect
# composes translateY(Σ belowⱼ × (1 − fⱼ)) · scaleY(f_own) out of them.
#
# EMISSION CONTRACT (generation time, from the EMITTED geometry — never the data values): each
# rect carries `--b1…--b(i−1)` = the `height` attributes of the segments BELOW it in its own
# column, plus `--self` = its own progress var. This page separates segments with a 2px
# page-coloured STROKE on contiguous rects (the other half of dv-004's ≥2px rule; the snippet
# uses geometric gaps instead) — either way the boundary is preserved exactly at every frame,
# because the algebra is exact.
#
# The curve rule is POSITIONAL and is DV-D16's: first var(--grow-ease-in), last
# var(--grow-ease-out), everything between `linear` (s218-D5 (1) moved the two curved positions
# off the bare CSS keywords onto the house family; the POSITIONAL rule is untouched).
# DV-D16c caps a stack at 6 segments, so 2 ≤ STACK_DEPTH ≤ 6.
STACK_DEPTH = 4          # the one stacked figure on this page carries 4 series; guarded in build_stacked()

def stack_css(n):
    """The whole float mechanism for a stack n deep. Nothing here is dead: n is the page's own
    stack depth, and build_stacked() refuses to emit a stack of any other depth."""
    props = "".join('  @property --dvf%d{syntax:"<number>"; inherits:true; initial-value:1;}\n' % i
                    for i in range(1, n + 1))
    frames = "".join('  @keyframes dvStackF%d{from{--dvf%d:0;} to{--dvf%d:1;}}\n' % (i, i, i)
                     for i in range(1, n + 1))
    def curve(i):
        return "var(--grow-ease-in)" if i == 1 else ("var(--grow-ease-out)" if i == n else "linear")
    anim = (",\n" + " " * 16).join("dvStackF%d var(--grow-dur) %s both" % (i, curve(i))
                                   for i in range(1, n + 1))
    terms = " + ".join("var(--b%d,0px) * (1 - var(--dvf%d))" % (i, i) for i in range(1, n))
    return f"""
  /* ---- DV-D16 wording ② · the stacked float. See the block above _gen_dataviz_charts.head(). ---- */
{props}{frames}  @media (prefers-reduced-motion:no-preference){{
    .dv-animate figure[data-dv-type="stacked"] svg.dv-svg{{
      animation:{anim};}}
    .dv-animate figure[data-dv-type="stacked"] rect.dv-series[data-grow="up"]{{
      animation:none; transform-box:fill-box; transform-origin:bottom;
      transform:translateY(calc({terms}))
                scaleY(var(--self,1));}}
    /* ★ s218-D5 (2) — THE ON-SEGMENT LETTER KEYS WAIT FOR THE GROWTH TO LAND. A stacked key is
       drawn ON its segment, and mid-flight that segment is BOTH scaling and floating, so a key
       faded in on the generic --ease sat adrift of the fill it labels. The delay is exactly one
       growth. This is a LONGHAND after the generic `animation:` shorthand in ANIM_CSS (which
       resets animation-delay to 0s), so it must stay AFTER it in source order AND out-specify
       it — hence the same :not() pair. The grouped letters of the grouped column ride the bar
       on --rise and are never adrift; they keep the undelayed fade. */
    .dv-animate figure[data-dv-type="stacked"] text.dv-key-el:not([data-rise]):not(.dv-anno){{
      animation-delay:var(--grow-dur);}}
  }}
"""

def head(title, extra_css=""):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<!-- APOLLO-DATAVIZ · MONOCHROME pro-forma base. Charts = semantic SVG + tokens + CSS motion + real <table> spine.
     Series colour = DATA SEMANTICS bound to data/* tokens (semantic-colour.json V7). No hardcoded colour outside
     the theme blocks. Flat fills only (dv-009). Gated by knowledge/_validate_dataviz.py. Behaviours are LIVE. -->
<style>
:is(button,a,label,span,small,strong,em,b,i,th,td,dt,dd,li,figcaption,legend,caption,summary,output,time):not(:has(svg)){{text-box-trim:trim-both;text-box-edge:cap alphabetic;}}
{TOKENS}
{BASE_CSS}{extra_css}
</style>
</head>
<body data-theme="light">
<script type="application/json" id="icon-manifest">{{"icons":{{}}}}</script>
<noscript><style>.dv-donut-seg{{visibility:visible !important}} .dv-anno{{opacity:1 !important}}</style></noscript>
<div class="top">
  <div class="t">Apollo DataViz <small>{title.split('· ',1)[-1]}</small></div>
  <div class="ctrls">
    <label class="wctl">Width <input type="range" id="widthSlider" min="360" max="1024" value="1024" aria-label="Preview width"><b id="widthVal">1024</b></label>
    <button class="tgl" id="replayBtn">Replay animation</button>
    <button class="tgl" id="contrastToggle" aria-pressed="false">High contrast</button>
    <button class="tgl" id="themeToggle" aria-pressed="false">Dark</button>
  </div>
</div>
<div class="wrap dv-animate">
<div class="dv-frame" id="dvFrame" style="--fw:1024px">
"""

FOOT = """</div></div>
<div class="dv-tip" id="dvTip" role="status" aria-live="polite"></div>
<script>
  var body = document.body;
  document.getElementById('themeToggle').onclick = function(){
    var d = body.getAttribute('data-theme') === 'dark';
    body.setAttribute('data-theme', d ? 'light' : 'dark');
    this.setAttribute('aria-pressed', String(!d)); this.textContent = d ? 'Dark' : 'Light';
  };
  document.getElementById('contrastToggle').onclick = function(){
    var hi = body.getAttribute('data-contrast') === 'high';
    if (hi) body.removeAttribute('data-contrast'); else body.setAttribute('data-contrast','high');
    this.setAttribute('aria-pressed', String(!hi));
  };
  // behaviour-only: replay entry animations (remove class, force reflow, re-add)
  var rb = document.getElementById('replayBtn');
  if (rb) rb.onclick = function(){
    document.querySelectorAll('.dv-animate').forEach(function(w){
      w.classList.remove('dv-animate'); void w.offsetWidth; w.classList.add('dv-animate');
    });
    sweepVisibleDonuts();
  };
  // behaviour-only: responsive width-compression. Keeps a fixed height + non-scaling text; only the
  // HORIZONTAL positions relayout to the container width (the method's 'geometry' node at runtime).
  // Pure enhancement wrapped in try/catch — if it fails, the baked SVG still renders (proportional).
  var DV_PL = 46, DV_PR = 12, DV_H = 260;
  function fitCharts(){
    document.querySelectorAll('svg.dv-fit').forEach(function(svg){
      try{
        var W = Math.round(svg.getBoundingClientRect().width);
        if(!W){ return; }
        var plotW = W - DV_PL - DV_PR; if(plotW < 90){ plotW = 90; }
        svg.setAttribute('viewBox', '0 0 ' + W + ' ' + DV_H);
        var X = function(f){ return DV_PL + parseFloat(f) * plotW; };
        svg.querySelectorAll('[data-fx]').forEach(function(el){
          var x = X(el.getAttribute('data-fx')), tag = el.tagName.toLowerCase();
          if(tag === 'rect'){
            el.setAttribute('x', x.toFixed(1));
            var fw = el.getAttribute('data-fw'); if(fw !== null){ el.setAttribute('width', (parseFloat(fw) * plotW).toFixed(1)); }
          } else if(tag === 'text'){
            var dx = parseFloat(el.getAttribute('data-dx') || '0'); el.setAttribute('x', (x + dx).toFixed(1));
          } else if(tag === 'line'){
            el.setAttribute('x1', x.toFixed(1));
            var fx2 = el.getAttribute('data-fx2'); if(fx2 !== null){ el.setAttribute('x2', X(fx2).toFixed(1)); }
          } else if(tag === 'g'){
            var x0 = parseFloat(el.getAttribute('data-x0') || '0'); el.setAttribute('transform', 'translate(' + (x - x0).toFixed(1) + ',0)');
          }
        });
        svg.querySelectorAll('polyline[data-fxs]').forEach(function(pl){
          var fxs = pl.getAttribute('data-fxs').trim().split(/\\s+/), ys = pl.getAttribute('data-ys').trim().split(/\\s+/);
          pl.setAttribute('points', fxs.map(function(f, i){ return X(f).toFixed(1) + ',' + ys[i]; }).join(' '));
        });
      }catch(e){ /* leave the baked SVG intact */ }
    });
  }
  var dvRAF; window.addEventListener('resize', function(){ cancelAnimationFrame(dvRAF); dvRAF = requestAnimationFrame(fitCharts); });
  fitCharts();
  // behaviour-only: donut variant tabs (letters / spider / direct)
  document.querySelectorAll('.variant-tabs[data-variant-group]').forEach(function(tabs){
    tabs.querySelectorAll('button').forEach(function(btn){
      btn.onclick = function(){
        tabs.querySelectorAll('button').forEach(function(b){ b.setAttribute('aria-selected', String(b === btn)); });
        var group = tabs.getAttribute('data-variant-group');
        document.querySelectorAll('[data-variant-of="'+group+'"]').forEach(function(v){
          if (v.getAttribute('data-variant') === btn.getAttribute('data-variant')){
            v.removeAttribute('hidden');
            v.querySelectorAll('figure[data-dv-type="donut"]').forEach(sweepDonut);
          } else { v.setAttribute('hidden',''); }
        });
      };
    });
  });
  // behaviour-only: marker-fill toggle (white vs background)
  document.querySelectorAll('.variant-tabs[data-marker-group]').forEach(function(tabs){
    tabs.querySelectorAll('button').forEach(function(btn){
      btn.onclick = function(){
        tabs.querySelectorAll('button').forEach(function(b){ b.setAttribute('aria-selected', String(b === btn)); });
        var group = tabs.getAttribute('data-marker-group');
        document.querySelectorAll('.marker-scope[data-marker-of="'+group+'"]').forEach(function(s){
          s.setAttribute('data-marker', btn.getAttribute('data-marker'));
        });
      };
    });
  });
  // behaviour-only: real tooltip — figure + info on hover/focus of any [data-tip] series element
  var dvTip = document.getElementById('dvTip');
  function tipShow(e){
    var el = e.target.closest('[data-tip]'); if(!el){ return; }
    dvTip.textContent = el.getAttribute('data-tip'); dvTip.classList.add('on');
    var pt = e.touches ? e.touches[0] : e;
    var x = pt.clientX + 14, y = pt.clientY + 14;
    var r = dvTip.getBoundingClientRect();
    if(x + r.width > window.innerWidth - 8){ x = pt.clientX - r.width - 14; }
    if(y + r.height > window.innerHeight - 8){ y = pt.clientY - r.height - 14; }
    dvTip.style.left = x + 'px'; dvTip.style.top = y + 'px';
  }
  function tipHide(){ dvTip.classList.remove('on'); }
  document.addEventListener('pointermove', function(e){ if(e.target.closest('[data-tip]')){ tipShow(e); } else { tipHide(); } });
  document.addEventListener('focusin', function(e){
    var el = e.target.closest('[data-tip]'); if(!el){ return; }
    var b = el.getBoundingClientRect();
    dvTip.textContent = el.getAttribute('data-tip'); dvTip.classList.add('on');
    dvTip.style.left = (b.left + b.width/2) + 'px'; dvTip.style.top = (b.top - 8) + 'px';
  });
  document.addEventListener('focusout', tipHide);
  // behaviour-only: table DRAWER — a frosted overlay on the right of the chart; chart keeps its width (#1/#3)
  document.querySelectorAll('.tbl-toggle').forEach(function(b){
    b.onclick = function(){
      var d = document.getElementById(b.getAttribute('aria-controls'));
      var open = d.classList.toggle('open');
      d.setAttribute('aria-hidden', String(!open));
      b.setAttribute('aria-expanded', String(open));
      b.textContent = open ? 'Hide table' : 'View as table';
    };
  });
  // behaviour-only: responsive preview WIDTH slider (starts at 1024) — sets the frame width + refits
  var wS = document.getElementById('widthSlider'), wV = document.getElementById('widthVal'), frame = document.getElementById('dvFrame');
  if (wS && frame){ wS.addEventListener('input', function(){
    frame.style.setProperty('--fw', wS.value + 'px'); wV.textContent = wS.value; fitCharts();
  }); }
  // behaviour-only: donut RADIAL SWEEP — segments grow their arc 0->extent, sequentially (#7). JS-driven;
  // no-JS / reduced-motion leaves the baked full donut. Re-runs on Replay and on variant switch.
  function arcPath(cx, cy, R, r, a1, a2){
    function P(rad, deg){ var a = deg * Math.PI / 180; return [cx + rad*Math.cos(a), cy + rad*Math.sin(a)]; }
    var p1 = P(R,a1), p2 = P(R,a2), p3 = P(r,a2), p4 = P(r,a1), lg = (a2 - a1) > 180 ? 1 : 0;
    return 'M'+p1[0].toFixed(2)+' '+p1[1].toFixed(2)+' A'+R+' '+R+' 0 '+lg+' 1 '+p2[0].toFixed(2)+' '+p2[1].toFixed(2)+
           ' L'+p3[0].toFixed(2)+' '+p3[1].toFixed(2)+' A'+r+' '+r+' 0 '+lg+' 0 '+p4[0].toFixed(2)+' '+p4[1].toFixed(2)+' Z';
  }
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function sweepDonut(fig){
    var segs = [].slice.call(fig.querySelectorAll('.dv-donut-seg'));
    var annos = [].slice.call(fig.querySelectorAll('.dv-anno'));
    if (reduce) { segs.forEach(function(s){ s.style.visibility = ''; }); annos.forEach(function(a){ a.classList.add('show'); }); return; }
    segs.forEach(function(s){ s.style.visibility = 'hidden'; });
    annos.forEach(function(a){ a.classList.remove('show'); });
    var last = segs.length - 1, k = 0;
    function showAnno(idx){
      var m = fig.querySelectorAll('.dv-anno[data-seq="' + idx + '"]');
      for (var i = 0; i < m.length; i++) { m[i].classList.add('show'); }  // label/leg fades in as its segment grows (#2)
    }
    function grow(){
      if (k >= segs.length) { return; }
      var kk = k, s = segs[kk], cx = +s.getAttribute('data-cx'), cy = +s.getAttribute('data-cy'),
          R = +s.getAttribute('data-ro'), r = +s.getAttribute('data-ri'),
          a1 = +s.getAttribute('data-a1'), a2 = +s.getAttribute('data-a2');
      // collapse the arc to zero AND reveal in the SAME synchronous tick, so the full arc never paints (batch5 #1)
      s.setAttribute('d', arcPath(cx, cy, R, r, a1, a1));
      s.style.visibility = '';
      showAnno(kk);
      var dur = 220 + (a2 - a1) / 360 * 620, t0 = null;
      function frameStep(ts){
        if (t0 === null) { t0 = ts; }
        var p = Math.min(1, (ts - t0) / dur), e;
        // ease ONLY the first + last segments; middle linear. batch7 #1: ease-IN first, ease-OUT last
        if (kk === 0) { e = p * p * p; }
        else if (kk === last) { e = 1 - Math.pow(1 - p, 3); }
        else { e = p; }
        s.setAttribute('d', arcPath(cx, cy, R, r, a1, a1 + (a2 - a1) * e));
        if (p < 1) { requestAnimationFrame(frameStep); } else { k++; grow(); }
      }
      requestAnimationFrame(frameStep);
    }
    grow();
  }
  function sweepVisibleDonuts(){
    document.querySelectorAll('figure[data-dv-type="donut"]').forEach(function(fig){
      if (fig.closest('.variant[hidden]')) { return; }
      sweepDonut(fig);
    });
  }
  sweepVisibleDonuts();
  // behaviour-only: series show/hide (multi-series charts)
  document.querySelectorAll('.dv-legend button[data-series-toggle]').forEach(function(b){
    b.onclick = function(){
      var on = b.getAttribute('aria-pressed') === 'true';
      b.setAttribute('aria-pressed', String(!on));
      document.querySelectorAll('[data-series-group="'+b.getAttribute('data-series-toggle')+'"]').forEach(function(el){
        el.style.opacity = on ? '0' : ''; el.style.pointerEvents = on ? 'none' : '';
      });
    };
  });
</script>
</body>
</html>
"""

def legend(names, n, toggle=False, center=False):
    li = []
    for i in range(n):
        key = LETTERS[i]
        sw = f'<span class="sw" style="background:var(--data-series-{i+1})"></span>'
        inner = f'{sw}<span class="dv-key">{key}</span> {names[i]}'
        if toggle:
            li.append(f'<li><button data-series-toggle="{i+1}" aria-pressed="true">{inner}</button></li>')
        else:
            li.append(f'<li>{sw}<span class="dv-key">{key}</span> {names[i]}</li>')
    cls = "dv-legend center" if center else "dv-legend"
    return f'<ul class="{cls}">' + "".join(li) + "</ul>"

def tbl_el(tid, caption, cols, rows):
    head_html = "".join(f'<th scope="col">{c}</th>' for c in cols)
    body = ""
    for r in rows:
        cells = f'<th scope="row">{r[0]}</th>' + "".join(f"<td>{c}</td>" for c in r[1:])
        body += f"<tr>{cells}</tr>"
    return (f'<table class="dv-table" id="{tid}"><caption>{caption}</caption>'
            f'<thead><tr>{head_html}</tr></thead><tbody>{body}</tbody></table>')

def assemble(cid, fig_attrs, caption, chart_html, cols, rows, extra_toolbar=""):
    """One figure = toolbar (View-as-table) + a STAGE of [chart-area | right-hand table DRAWER].
    Opening the drawer compresses the chart to fit (Dave review #1/#8) — the drawer slides from the
    right of the CHART, not the page edge; the chart relayouts via fitCharts()."""
    drawer = cid + "-drawer"
    tbar = (f'<div class="dv-toolbar">{extra_toolbar}'
            f'<button class="tbl-toggle" aria-controls="{drawer}" aria-expanded="false">View as table</button></div>')
    tbl = tbl_el(cid + "-t", caption, cols, rows)
    stage = (f'<div class="dv-stage">'
             f'<div class="dv-chart-area">{chart_html}</div>'
             f'<aside class="dv-drawer" id="{drawer}" aria-hidden="true"><div class="dv-drawer-inner">{tbl}</div></aside>'
             f'</div>')
    return (f'<figure class="dv" {fig_attrs} role="group" aria-labelledby="{cid}-h">'
            f'<figcaption id="{cid}-h" class="sr-only">{caption}</figcaption>{tbar}{stage}</figure>')

# ---------------- plot frame ----------------
W, H = 580, 260
PL, PR, PT, PB = 46, 12, 14, 30
plotW, plotH = W - PL - PR, H - PT - PB
BASE_Y = PT + plotH

def fx(x):
    """Fraction of the plot width (0..1) — the anchor the runtime fit() re-expands to container width."""
    return (x - PL) / plotW

def y_axis(top, step, horizontal=False):
    """Gridlines + numeric axis labels for a 0..top linear scale."""
    els = []
    for t in ticks(top, step):
        if horizontal:
            x = PL + t / top * plotW; f = t / top
            els.append(f'<line class="dv-grid" data-fx="{f:.4f}" data-fx2="{f:.4f}" x1="{x:.1f}" y1="{PT}" x2="{x:.1f}" y2="{BASE_Y}"/>')
            els.append(f'<text class="dv-axis" data-fx="{f:.4f}" x="{x:.1f}" y="{BASE_Y+16}" text-anchor="middle">{fmt(t)}</text>')
        else:
            y = BASE_Y - t / top * plotH
            els.append(f'<line class="dv-grid" data-fx="0" data-fx2="1" x1="{PL}" y1="{y:.1f}" x2="{PL+plotW}" y2="{y:.1f}"/>')
            els.append(f'<text class="dv-axis" x="{PL-8}" y="{y+3:.1f}" text-anchor="end">{fmt(t)}</text>')
    return "".join(els)

def svg_open(label, fit=True):
    cls = "dv-svg dv-fit" if fit else "dv-svg"
    # Always meet (no distortion). Runtime fit() sets viewBox width = container px so the mapping is
    # exactly 1:1 (text + strokes at true size); pre-JS fallback scales down proportionally, harmless.
    return (f'<svg class="{cls}" viewBox="0 0 {W} {H}" role="img" aria-label="{label}" '
            f'preserveAspectRatio="xMidYMid meet">')

# ---------------- column (single series, vertical) ----------------
def build_column(cid, title, caption, cats, vals, si=1):
    top, step = nice_max(max(vals))
    band = plotW / len(cats)
    bw = band * 0.56
    bars, xlabels = [], []
    for i, (c, v) in enumerate(zip(cats, vals)):
        h = v / top * plotH
        x = PL + band * i + (band - bw) / 2
        y = BASE_Y - h
        bars.append(f'<rect class="dv-series" data-grow="up" style="animation-delay:{i*45}ms" '
                    f'data-fx="{fx(x):.4f}" data-fw="{bw/plotW:.4f}" data-tip="{c}: £{fmt(v)}" '
                    f'fill="var(--data-series-{si})" x="{x:.1f}" y="{y:.1f}" '
                    f'width="{bw:.1f}" height="{h:.1f}"><title>{c}: {fmt(v)}</title></rect>')
        xlabels.append(f'<text class="dv-label" data-fx="{fx(x+bw/2):.4f}" x="{x+bw/2:.1f}" y="{BASE_Y+16}" text-anchor="middle">{c}</text>')
    svg = (svg_open(f"{title}. {', '.join(f'{c} {fmt(v)}' for c,v in zip(cats,vals))}.")
           + y_axis(top, step)
           + f'<line class="dv-axis" data-fx="0" data-fx2="1" x1="{PL}" y1="{BASE_Y}" x2="{PL+plotW}" y2="{BASE_Y}"/>'
           + "".join(bars) + "".join(xlabels) + "</svg>")
    return assemble(cid, 'data-dv-type="column" data-domain-min="0" data-surface="page"', caption,
                    svg, ["Category", "Amount (£)"], list(zip(cats, [fmt(v) for v in vals])))

# ---------------- horizontal bar (single series) ----------------
def build_bar(cid, title, caption, cats, vals, si=3):
    top, step = nice_max(max(vals))
    band = plotH / len(cats)
    bh = band * 0.56
    bars, ylabels = [], []
    for i, (c, v) in enumerate(zip(cats, vals)):
        w = v / top * plotW
        y = PT + band * i + (band - bh) / 2
        # #6: horizontal bar uses the SAME fit scaling as the others — horizontal only (bar length = value fraction of plotW)
        bars.append(f'<rect class="dv-series" data-grow="right" style="animation-delay:{i*45}ms" '
                    f'data-fx="0" data-fw="{v/top:.4f}" data-tip="{c}: £{fmt(v)}" '
                    f'fill="var(--data-series-{si})" x="{PL}" y="{y:.1f}" '
                    f'width="{w:.1f}" height="{bh:.1f}"><title>{c}: {fmt(v)}</title></rect>')
        ylabels.append(f'<text class="dv-label" x="{PL-8}" y="{y+bh/2+3:.1f}" text-anchor="end">{c}</text>')
    svg = (svg_open(f"{title}. {', '.join(f'{c} {fmt(v)}' for c,v in zip(cats,vals))}.", fit=True)
           + y_axis(top, step, horizontal=True)
           + f'<line class="dv-axis" data-fx="0" data-fx2="0" x1="{PL}" y1="{PT}" x2="{PL}" y2="{BASE_Y}"/>'
           + "".join(bars) + "".join(ylabels) + "</svg>")
    return assemble(cid, 'data-dv-type="bar" data-domain-min="0" data-surface="page"', caption,
                    svg, ["Category", "Amount (£)"], list(zip(cats, [fmt(v) for v in vals])))

# ---------------- grouped (2+ series, vertical) ----------------
def build_grouped(cid, title, caption, cats, series):
    names = [s[0] for s in series]
    allv = [v for _, vs in series for v in vs]
    top, step = nice_max(max(allv))
    band = plotW / len(cats)
    n = len(series)
    gw = band * 0.7
    bw = gw / n
    bars, xlabels, keys = [], [], []
    for i, c in enumerate(cats):
        gx = PL + band * i + (band - gw) / 2
        for j, (name, vs) in enumerate(series):
            v = vs[i]
            h = v / top * plotH
            x = gx + bw * j
            y = BASE_Y - h
            bars.append(f'<rect class="dv-series" data-grow="up" data-series-group="{j+1}" style="animation-delay:{i*45}ms" '
                        f'data-fx="{fx(x):.4f}" data-fw="{(bw-2)/plotW:.4f}" '
                        f'data-tip="{LETTERS[j]} · {name} · {c}: £{fmt(v)}" '
                        f'fill="var(--data-series-{j+1})" '
                        f'x="{x:.1f}" y="{y:.1f}" width="{bw-2:.1f}" height="{h:.1f}"><title>{name} · {c}: {fmt(v)}</title></rect>')
            # letter rises WITH the bar (Dave review #3): starts at the baseline, travels up to the bar top, synced with the grow
            keys.append(f'<text class="dv-key-el" data-rise data-series-group="{j+1}" data-fx="{fx(x+(bw-2)/2):.4f}" '
                        f'style="--rise:{h+4:.0f}px; animation-delay:{i*45}ms" '
                        f'fill="var(--data-series-{j+1})" '
                        f'x="{x+(bw-2)/2:.1f}" y="{y-4:.1f}" text-anchor="middle">{LETTERS[j]}</text>')
        xlabels.append(f'<text class="dv-label" data-fx="{fx(gx+gw/2):.4f}" x="{gx+gw/2:.1f}" y="{BASE_Y+16}" text-anchor="middle">{c}</text>')
    svg = (svg_open(f"{title}, grouped columns.") + y_axis(top, step)
           + f'<line class="dv-axis" data-fx="0" data-fx2="1" x1="{PL}" y1="{BASE_Y}" x2="{PL+plotW}" y2="{BASE_Y}"/>'
           + "".join(bars) + "".join(keys) + "".join(xlabels) + "</svg>")
    rows = [[c] + [fmt(series[j][1][i]) for j in range(n)] for i, c in enumerate(cats)]
    chart = svg + legend(names, n, toggle=True, center=True)
    return assemble(cid, 'data-dv-type="grouped" data-domain-min="0" data-surface="page"', caption,
                    chart, ["Category"] + names, rows)

# ---------------- stacked (segments, +chevron on one series, +2px separation) ----------------
def build_stacked(cid, title, caption, cats, series, chevron_idx=None):
    names = [s[0] for s in series]
    totals = [sum(series[j][1][i] for j in range(len(series))) for i in range(len(cats))]
    top, step = nice_max(max(totals))
    band = plotW / len(cats)
    bw = band * 0.56
    n = len(series)
    # chevron texture reserved for gauge-type charts (Dave review 2026-07-16) — OFF for stacked; capability kept.
    defs = ""
    if chevron_idx is not None:
        defs = (f'<defs><pattern id="chevron-{chevron_idx+1}" width="8" height="8" patternUnits="userSpaceOnUse" '
                f'patternTransform="rotate(45)"><rect width="8" height="8" fill="var(--data-series-{chevron_idx+1})"/>'
                f'<rect width="4" height="8" fill="var(--page)" opacity="0.35"/></pattern></defs>')
    # ⛔ DV-D16c caps a stack at 6, and stack_css() is built for exactly STACK_DEPTH progress vars.
    #    A silent mismatch would emit --self:var(--dvfN) for an N that is never registered or
    #    animated, and the segment would sit at its initial value 1 — a chart that simply never
    #    animates, green in every static check. Fail LOUD and NAMED instead.
    if n != STACK_DEPTH:
        raise SystemExit("DV-D16: build_stacked(%r) has %d series but stack_css() is built for "
                         "STACK_DEPTH=%d — update STACK_DEPTH (DV-D16c caps stacks at 6) so the "
                         "@property registrations, the keyframes, the shared-timeline curve list "
                         "and the translate terms all follow the depth." % (cid, n, STACK_DEPTH))
    segs, xlabels, keys = [], [], []
    for i, c in enumerate(cats):
        x = PL + band * i + (band - bw) / 2
        acc = 0.0
        # DV-D16 ② EMISSION CONTRACT: the heights of the segments BELOW this one, in this column,
        # to the same 1dp the `height` attribute is emitted at, so a probe can re-derive every
        # --b from the artefact's own geometry rather than from the data.
        below = []
        for j, (name, vs) in enumerate(series):
            v = vs[i]
            h = v / top * plotH
            y = BASE_Y - (acc + v) / top * plotH
            fill = f'url(#chevron-{chevron_idx+1})' if (chevron_idx is not None and j == chevron_idx) else f'var(--data-series-{j+1})'
            # DV-D16 wording ② (in force): NO per-segment delay, NO per-segment duration, NO
            # per-segment timing function — one shared timeline lives on the <svg>, and each rect
            # only declares WHICH progress number is its own and WHAT is stacked beneath it.
            bvars = "".join(f'--b{k+1}:{hb:.1f}px; ' for k, hb in enumerate(below))
            segs.append(f'<rect class="dv-series" data-grow="up" data-series-group="{j+1}" '
                        f'style="{bvars}--self:var(--dvf{j+1})" '
                        f'data-fx="{fx(x):.4f}" data-fw="{bw/plotW:.4f}" '
                        f'data-tip="{LETTERS[j]} · {name} · {c}: £{fmt(v)}" '
                        f'fill="{fill}" '
                        f'stroke="var(--page)" stroke-width="2" x="{x:.1f}" y="{y:.1f}" '
                        f'width="{bw:.1f}" height="{h:.1f}"><title>{name} · {c}: {fmt(v)}</title></rect>')
            if h > 14:
                keys.append(f'<text class="dv-key-el" data-series-group="{j+1}" data-fx="{fx(x+bw/2):.4f}" fill="var(--page)" '
                            f'x="{x+bw/2:.1f}" y="{y+h/2+4:.1f}" text-anchor="middle">{LETTERS[j]}</text>')
            below.append(h)
            acc += v
        xlabels.append(f'<text class="dv-label" data-fx="{fx(x+bw/2):.4f}" x="{x+bw/2:.1f}" y="{BASE_Y+16}" text-anchor="middle">{c}</text>')
    svg = (svg_open(f"{title}, stacked columns.") + defs + y_axis(top, step)
           + f'<line class="dv-axis" data-fx="0" data-fx2="1" x1="{PL}" y1="{BASE_Y}" x2="{PL+plotW}" y2="{BASE_Y}"/>'
           + "".join(segs) + "".join(keys) + "".join(xlabels) + "</svg>")
    rows = [[c] + [fmt(series[j][1][i]) for j in range(n)] for i, c in enumerate(cats)]
    chart = svg + legend(names, n, toggle=True, center=True)
    return assemble(cid, 'data-dv-type="stacked" data-domain-min="0" data-surface="page"', caption,
                    chart, ["Period"] + names, rows)

# ---------------- line / multi-series ----------------
MARKERS = ["circle", "square", "diamond", "triangle", "cross"]
def marker(shape, cx, cy, scvar):
    """Fill + border are CSS-driven by the marker-scope (Dave review #4/#5): each marker carries its
    series colour as --sc. White option = white fill + series-colour border at LINE width; Background
    option = series-colour fill + page-colour border. Sizes are bigger so the border reads."""
    r = 4.2
    a = f'class="dv-mk" style="--sc:{scvar}"'
    if shape == "circle":
        return f'<circle {a} cx="{cx:.1f}" cy="{cy:.1f}" r="{r}"/>'
    if shape == "square":
        return f'<rect {a} x="{cx-r:.1f}" y="{cy-r:.1f}" width="{2*r}" height="{2*r}"/>'
    if shape == "diamond":
        return f'<polygon {a} points="{cx:.1f},{cy-r-.7:.1f} {cx+r+.7:.1f},{cy:.1f} {cx:.1f},{cy+r+.7:.1f} {cx-r-.7:.1f},{cy:.1f}"/>'
    if shape == "triangle":
        return f'<polygon {a} points="{cx:.1f},{cy-r-.7:.1f} {cx+r+.7:.1f},{cy+r:.1f} {cx-r-.7:.1f},{cy+r:.1f}"/>'
    return f'<path class="dv-mk-cross" style="--sc:{scvar}" d="M{cx-r:.1f} {cy-r:.1f} L{cx+r:.1f} {cy+r:.1f} M{cx+r:.1f} {cy-r:.1f} L{cx-r:.1f} {cy+r:.1f}"/>'

def build_spark(cid, title, caption, xs, name, vals):
    """Wide, flat, axis-free single-series sparkline (dv-line-009 aspect)."""
    SW, SH, sp = 580, 90, 4
    lo, hi = min(vals), max(vals)
    pts = []
    for i, v in enumerate(vals):
        x = sp + i / (len(vals) - 1) * (SW - 2 * sp)
        y = (SH - sp) - (v - lo) / (hi - lo) * (SH - 2 * sp)
        pts.append((x, y))
    pstr = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    lx, ly = pts[-1]
    svg = (f'<svg class="dv-svg" viewBox="0 0 {SW} {SH}" role="img" aria-label="{title}." '
           f'preserveAspectRatio="none" style="max-width:340px;height:64px">'
           f'<line class="dv-grid" x1="{sp}" y1="{SH-sp}" x2="{SW-sp}" y2="{SH-sp}"/>'
           f'<polyline class="dv-series" pathLength="2400" fill="none" stroke="var(--data-series-1)" stroke-width="2.5" '
           f'stroke-linejoin="round" stroke-linecap="round" vector-effect="non-scaling-stroke" points="{pstr}"/>'
           f'<circle class="dv-series" cx="{lx:.1f}" cy="{ly:.1f}" r="3.5" fill="var(--data-series-1)"/></svg>')
    return assemble(cid, 'data-dv-type="spark" data-surface="page"', caption,
                    svg, ["Point", name], list(zip(xs, [fmt(v) for v in vals])))

def build_line(cid, title, caption, xs, series, dtype="line"):
    if dtype == "spark":
        return build_spark(cid, title, caption, xs, series[0][0], series[0][1])
    names = [s[0] for s in series]
    allv = [v for _, vs in series for v in vs]
    top, step = nice_max(max(allv))
    band = plotW / (len(xs) - 1)
    n = len(series)
    parts, keys = [], []
    for j, (name, vs) in enumerate(series):
        pts = []
        for i, v in enumerate(vs):
            x = PL + band * i
            y = BASE_Y - v / top * plotH
            pts.append((x, y))
        pstr = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        fxs = " ".join(f"{fx(x):.4f}" for x, _ in pts)
        ys = " ".join(f"{y:.1f}" for _, y in pts)
        # batch8 #1: node cadence FOLLOWS the line's easing (not linear) — each node lands as the drawing
        # head passes it, so they keep pace with the line (fast through the middle, no slow linear trickle).
        node_delay = line_node_delays(len(vs), 2400)
        # pathLength="2400" NORMALISES the path so the dash-draw spans the WHOLE animation (not ~20% —
        # the real geometry is far shorter than the dasharray) and is immune to responsive rescaling.
        # This is what makes the line-draw share the SAME easing timeline as the nodes (batch9 #1).
        parts.append(f'<polyline class="dv-series" data-series-group="{j+1}" data-fxs="{fxs}" data-ys="{ys}" '
                     f'pathLength="2400" fill="none" '
                     f'stroke="var(--data-series-{j+1})" stroke-width="2.5" stroke-linejoin="round" '
                     f'stroke-linecap="round" vector-effect="non-scaling-stroke" points="{pstr}"><title>{name}</title></polyline>')
        for i, (x, y) in enumerate(pts):
            parts.append(f'<g class="dv-marker" data-series-group="{j+1}" data-fx="{fx(x):.4f}" data-x0="{x:.1f}" '
                         f'data-tip="{LETTERS[j]} · {name} · {xs[i]}: {fmt(vs[i])}" '
                         f'style="animation-delay:{node_delay[i]:.0f}ms">'
                         f'{marker(MARKERS[j], x, y, f"var(--data-series-{j+1})")}</g>')
        lx, ly = pts[-1]
        keys.append(f'<text class="dv-key-el" data-series-group="{j+1}" data-fx="{fx(lx):.4f}" data-dx="7" '
                    f'fill="var(--data-series-{j+1})" '
                    f'x="{lx+7:.1f}" y="{ly+3:.1f}">{LETTERS[j]}</text>')
    xlabels = "".join(f'<text class="dv-label" data-fx="{fx(PL+band*i):.4f}" x="{PL+band*i:.1f}" y="{BASE_Y+16}" text-anchor="middle">{x}</text>'
                      for i, x in enumerate(xs))
    svg = (svg_open(f"{title}.") + y_axis(top, step)
           + f'<line class="dv-axis" data-fx="0" data-fx2="1" x1="{PL}" y1="{BASE_Y}" x2="{PL+plotW}" y2="{BASE_Y}"/>'
           + "".join(parts) + ("".join(keys) if n >= 2 else "") + xlabels + "</svg>")
    rows = [[x] + [fmt(series[j][1][i]) for j in range(n)] for i, x in enumerate(xs)]
    leg = legend(names, n, toggle=True, center=True) if n >= 2 else ""
    return assemble(cid, f'data-dv-type="{dtype}" data-surface="page"', caption,
                    svg + leg, ["Point"] + names, rows)

# ---------------- donut + centre total (mode: legend-right | direct labels) ----------------
def _arc(cx, cy, R, r, a1, a2):
    def pt(rad, deg):
        a = math.radians(deg)
        return cx + rad * math.cos(a), cy + rad * math.sin(a)
    x1, y1 = pt(R, a1); x2, y2 = pt(R, a2)
    xr1, yr1 = pt(r, a2); xr2, yr2 = pt(r, a1)
    large = 1 if (a2 - a1) > 180 else 0
    return (f"M{x1:.2f} {y1:.2f} A{R} {R} 0 {large} 1 {x2:.2f} {y2:.2f} "
            f"L{xr1:.2f} {yr1:.2f} A{r} {r} 0 {large} 0 {xr2:.2f} {yr2:.2f} Z")

def _donut_centre(cx, cy, total, total_label):
    return (f'<text class="dv-val" x="{cx}" y="{cy-2}" text-anchor="middle" style="font-size:22px">{fmt(total)}</text>'
            f'<text class="dv-label" x="{cx}" y="{cy+16}" text-anchor="middle">{total_label}</text>')

def build_donut(cid, title, caption, cats, vals, total_label="Total", mode="letters"):
    """mode: 'letters' = legend + letter ON each segment · 'spider' = legend + letter on a spider leg ·
    'direct' = full labels in place, no legend. Segments GROW sequentially from the centre (Dave review #8)."""
    total = sum(vals)
    names = list(cats)
    fig_attrs = f'data-dv-type="donut" data-total="{fmt(total)}" data-surface="page" data-labelling="{mode}"'

    def seg(idx, c, v, cx, cy, R, r, a1, a2):
        # arc params travel on the element so the JS sweep (Dave review #7) can grow a1->a2 sequentially.
        # Baked hidden so the full arc never flashes before the grow (#2); noscript/reduced-motion reveals it.
        return (f'<path class="dv-series dv-donut-seg" data-seq="{idx}" style="visibility:hidden" '
                f'data-cx="{cx}" data-cy="{cy}" data-ro="{R}" data-ri="{r}" data-a1="{a1:.2f}" data-a2="{a2:.2f}" '
                f'data-tip="{LETTERS[idx]} · {c}: £{fmt(v)} ({v/total*100:.0f}%)" '
                f'fill="var(--data-series-{idx+1})" stroke="var(--page)" stroke-width="2" '
                f'd="{_arc(cx,cy,R,r,a1,a2)}"><title>{c}: {fmt(v)} ({v/total*100:.0f}%)</title></path>')

    if mode == "direct":  # full labels + leader lines, no legend
        cx, cy, R, r = 200, 128, 100, 60
        segs, extras, i0 = [], [], -90.0
        for idx, (c, v) in enumerate(zip(cats, vals)):
            sweep = v / total * 360; a2 = i0 + sweep; amid = i0 + sweep / 2
            segs.append(seg(idx, c, v, cx, cy, R, r, i0, a2))
            ar = math.radians(amid)
            px, py = cx + R * math.cos(ar), cy + R * math.sin(ar)
            ex, ey = cx + (R + 14) * math.cos(ar), cy + (R + 14) * math.sin(ar)
            right = math.cos(ar) >= 0
            lx = (cx + R + 60) if right else (cx - R - 60); anchor = "start" if right else "end"; tx = lx + (4 if right else -4)
            extras.append(f'<polyline class="dv-leader dv-anno" data-seq="{idx}" points="{px:.1f},{py:.1f} {ex:.1f},{ey:.1f} {lx:.1f},{ey:.1f}"/>')
            extras.append(f'<text class="dv-direct dv-anno" data-seq="{idx}" x="{tx:.1f}" y="{ey-2:.1f}" text-anchor="{anchor}">{LETTERS[idx]} · {c}'
                          f'<tspan class="amt" x="{tx:.1f}" dy="13">£{fmt(v)} · {v/total*100:.0f}%</tspan></text>')
            i0 = a2
        svg = (f'<svg class="dv-svg" viewBox="0 0 400 260" role="img" aria-label="{title}. Total {fmt(total)}." '
               f'preserveAspectRatio="xMidYMid meet" style="max-width:440px">'
               + "".join(extras) + "".join(segs) + _donut_centre(cx, cy, total, total_label) + "</svg>")
        body = svg
    else:  # 'letters' or 'spider' — legend on the right PLUS on-chart alphabetic labels
        vbW = 300 if mode == "spider" else 260
        cx, cy, R, r = (150, 130, 100, 60) if mode == "spider" else (130, 130, 108, 66)
        segs, marks, i0 = [], [], -90.0
        for idx, (c, v) in enumerate(zip(cats, vals)):
            sweep = v / total * 360; a2 = i0 + sweep; amid = i0 + sweep / 2
            segs.append(seg(idx, c, v, cx, cy, R, r, i0, a2))
            ar = math.radians(amid)
            if mode == "spider":
                px, py = cx + (R + 2) * math.cos(ar), cy + (R + 2) * math.sin(ar)
                ex, ey = cx + (R + 13) * math.cos(ar), cy + (R + 13) * math.sin(ar)
                lxp = cx + (R + 22) * math.cos(ar)
                marks.append(f'<polyline class="dv-leader dv-anno" data-seq="{idx}" points="{px:.1f},{py:.1f} {ex:.1f},{ey:.1f}"/>')
                marks.append(f'<text class="dv-key-el dv-anno" data-seq="{idx}" fill="var(--ink)" x="{lxp:.1f}" y="{ey+4:.1f}" '
                             f'text-anchor="middle">{LETTERS[idx]}</text>')
            else:  # letters on the segment body
                rm = (R + r) / 2
                mx, my = cx + rm * math.cos(ar), cy + rm * math.sin(ar)
                marks.append(f'<text class="dv-key-el dv-anno" data-seq="{idx}" fill="#FFFFFF" x="{mx:.1f}" y="{my+4:.1f}" '
                             f'text-anchor="middle">{LETTERS[idx]}</text>')
            i0 = a2
        svg = (f'<svg class="dv-svg" viewBox="0 0 {vbW} 260" role="img" aria-label="{title}. Total {fmt(total)}." '
               f'preserveAspectRatio="xMidYMid meet" style="max-width:{vbW}px">'
               + "".join(segs) + "".join(marks) + _donut_centre(cx, cy, total, total_label) + "</svg>")
        body = f'<div class="dv-donut-row">{svg}{legend(names, len(cats)).replace("dv-legend", "dv-legend vert")}</div>'
    return assemble(cid, fig_attrs, caption, body, ["Segment", "Amount", "Share"],
                    [[c, fmt(v), f"{v/total*100:.0f}%"] for c, v in zip(cats, vals)])

# ---------------- KPI stat card ----------------
ARROWS = {"gain": '<polygon points="5,1 9,8 1,8"/>', "loss": '<polygon points="5,9 9,2 1,2"/>',
          "flat": '<rect x="1" y="4" width="8" height="2"/>'}
def build_kpi(cid, label, value, unit="", delta=None, since="", spark=None, srcaption=None, rows=None):
    val_html = (f'<span class="unit">{unit}</span>' if unit else "") + value
    foot = ""
    if delta:
        kind, txt = delta
        foot = (f'<div class="kpi-foot"><span class="delta {kind}">'
                f'<svg class="arrow" viewBox="0 0 10 10" aria-hidden="true">{ARROWS[kind]}</svg>{txt}</span>'
                f'<span class="kpi-since">{since}</span></div>')
    spk = ""
    if spark:
        xs, vals = spark
        SW, SH, sp = 200, 48, 3
        lo, hi = min(vals), max(vals)
        pts = " ".join(f"{sp+i/(len(vals)-1)*(SW-2*sp):.1f},{(SH-sp)-(v-lo)/(hi-lo)*(SH-2*sp):.1f}" for i, v in enumerate(vals))
        lx = SW - sp; ly = (SH - sp) - (vals[-1] - lo) / (hi - lo) * (SH - 2 * sp)
        spk = (f'<svg class="spark-inline" viewBox="0 0 {SW} {SH}" preserveAspectRatio="none" aria-hidden="true">'
               f'<line class="dv-base" x1="{sp}" y1="{SH-sp}" x2="{SW-sp}" y2="{SH-sp}"/>'
               f'<polyline class="dv-series" points="{pts}"/><circle class="dv-end" cx="{lx}" cy="{ly:.1f}" r="3"/></svg>')
    if rows:
        tb = "".join(f'<tr><th scope="row">{r[0]}</th><td>{r[1]}</td></tr>' for r in rows)
        tbl = f'<table class="sr-only"><caption>{srcaption}</caption>{tb}</table>'
    else:
        tbl = f'<table class="sr-only"><caption>{srcaption}</caption><tr><th scope="row">{label}</th><td>{value}</td></tr></table>'
    return (f'<figure class="dv kpi" data-dv-type="kpi" data-surface="raised" role="group" aria-labelledby="{cid}-l">'
            f'<span class="kpi-label" id="{cid}-l">{label}</span><span class="kpi-value">{val_html}</span>'
            f'{foot}{spk}{tbl}</figure>')

def section(title, tag, sub, *figs, grid=False):
    body = ("".join(figs))
    if grid:
        body = f'<div class="kpi-grid">{body}</div>'
    return (f'<section><div class="h"><h2>{title}</h2><span class="tag">{tag}</span></div>'
            f'<p class="sub">{sub}</p>' + body + "</section>")

# ---------------- writers ----------------
def write(name, html):
    path = os.path.join(OUT, name)
    open(path, "w").write(html)
    print("wrote", os.path.relpath(path, os.path.join(HERE, "..", "..")))

def main():
    cats6 = ["Groceries", "Transport", "Housing", "Leisure", "Utilities", "Savings"]
    spend = [420, 180, 950, 260, 210, 300]
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    savings12 = [82, 80, 85, 83, 88, 90, 87, 92, 95, 93, 98, 104]

    h = head("Apollo DataViz · Round-one kit", extra_css=KPI_CSS + ANIM_CSS + stack_css(STACK_DEPTH))
    h += ('<section style="border-top:0"><div class="h"><h2>Round-one chart kit</h2>'
          '<span class="tag">4 types · gate-first</span></div>'
          '<p class="sub">The whole round-one kit on one page: KPI stat card, bar &amp; column, line, and donut. '
          'Semantic SVG + <code>data/*</code> tokens + CSS motion + a real <code>&lt;table&gt;</code> spine, all '
          'gated by <code>_validate_dataviz.py</code> (9 blocking + 5 advisory, both themes). Toggle '
          '<strong>Dark</strong> and <strong>High contrast</strong> top-right — the same charts rebind, no forks.</p></section>')

    # ---- 1 · KPI stat card ----
    h += section("KPI stat card", "kpi · metric · +delta · +spark",
                 "One number with optional delta and sparkline. Gain/loss uses the convention consciously (dv-019): sign <strong>and</strong> arrow <strong>and</strong> colour — three channels, so colour is never load-bearing alone. Deltas are data semantics, exempt from red-once-per-screen.",
                 build_kpi("k1", "Total balance", "18,240", unit="£", srcaption="Total balance"),
                 build_kpi("k2", "Monthly income", "3,120", unit="£", delta=("gain", "+6.4%"), since="vs last month",
                           srcaption="Monthly income, up 6.4% versus last month",
                           rows=[("This month", "£3,120"), ("Last month", "£2,933"), ("Change", "+6.4%")]),
                 build_kpi("k3", "Card spend", "1,486", unit="£", delta=("loss", "+12.1%"), since="vs last month",
                           srcaption="Card spend, up 12.1% versus last month",
                           rows=[("This month", "£1,486"), ("Last month", "£1,326"), ("Change", "+12.1%")]),
                 build_kpi("k4", "Direct debits", "14", delta=("flat", "0"), since="no change",
                           srcaption="Direct debits, no change", rows=[("Active", "14"), ("Change", "0")]),
                 build_kpi("k5", "Savings balance", "104,000", unit="£", delta=("gain", "+26.8%"), since="12 months",
                           spark=(months, savings12), srcaption="Savings balance by month, pounds thousands",
                           rows=list(zip(months, [str(v) for v in savings12]))),
                 grid=True)

    # ---- 2 · Bar / column ----
    h += section("Column", "column · single series",
                 "Vertical bars on a zero baseline (dv-bar-009). One series, one colour — the x-axis labels carry the categories, so colour is not doing redundant work. Grid + numeric y-axis from hand-rolled nice-ticks.",
                 build_column("col1", "Spend by category", "Spend by category this month, pounds", cats6, spend))
    h += section("Horizontal bar", "bar · single series",
                 "Long category labels read better horizontally. Negative values are not allowed on horizontal bars (dv-bar-007) — the gate blocks them; use a vertical column when a series can go negative.",
                 build_bar("bar1", "Spend by category", "Spend by category this month, pounds, horizontal", cats6, spend))
    h += section("Grouped column", "grouped · 2 series",
                 "Two series side by side for direct comparison. Each series carries a letter (A, B) on the bars and in the legend, so the comparison survives without colour (§04.3). Legend items toggle series visibility.",
                 build_grouped("grp1", "This year versus last", "This year versus last year by category, pounds",
                               ["Housing", "Leisure", "Transport", "Utilities", "Savings"],
                               [("This year", [950, 260, 180, 210, 300]), ("Last year", [910, 300, 165, 205, 220])]))
    h += section("Stacked column", "stacked · 4 series",
                 "Composition over time. Segments are separated by a 2px surface-coloured stroke (dv-004) so touching fills never shimmer at the boundary. Fills are solid — the chevron texture is reserved for gauge-type charts (your call), not stacked series.",
                 build_stacked("stk1", "Spend mix by quarter", "Spend mix by quarter, pounds",
                               ["Q1", "Q2", "Q3", "Q4"],
                               [("Housing", [950, 950, 960, 970]), ("Essentials", [610, 640, 600, 660]),
                                ("Leisure", [260, 300, 340, 290]), ("Savings", [300, 260, 320, 380])]))

    # ---- 3 · Line ----
    marker_ctl = ('<div class="variant-tabs" data-marker-group="line" role="tablist">'
                  '<button data-marker="white" aria-selected="true">Marker: white fill</button>'
                  '<button data-marker="bg" aria-selected="false">Marker: background fill</button></div>'
                  '<p class="sub" style="margin-top:var(--space-8)">Markers carry the series colour as a border. '
                  'Compare a solid <strong>white</strong> fill vs a <strong>background</strong> fill (adapts to the theme — '
                  'shows most clearly in dark mode). All lines build together, each symbol landing as the line reaches it.</p>')
    line_secs = (section("Line", "line · single series",
                 "A single series over time. Straight segments between points (dv-line-011) — no curve smoothing, which would misrepresent the values between readings. Markers sit on each reading.",
                 build_line("ln1", "Balance over the year", "Account balance by month, pounds thousands",
                            months, [("Balance", savings12)]))
                 + section("Multi-series line", "line · 3 series",
                 "Up to five series, each with its own colour, letter (A–C) and marker shape (dv-line-002) — three redundant channels so the lines are told apart without relying on colour. Legend toggles a series in and out.",
                 build_line("ln2", "Balances by product", "Balances by product by month, pounds thousands",
                            months,
                            [("Current", [12, 11, 13, 12, 14, 13, 15, 14, 16, 15, 17, 18]),
                             ("Savings", savings12),
                             ("Investments", [40, 42, 41, 45, 44, 48, 47, 52, 55, 53, 58, 62])],
                            dtype="multiline")))
    h += (f'<section><div class="h"><h2>Line</h2><span class="tag">line · marker styles</span></div>'
          f'{marker_ctl}</section>'
          f'<div class="marker-scope" data-marker-of="line" data-marker="white">{line_secs}</div>')
    h += section("Sparkline", "spark · inline trend",
                 "A wide, flat, axis-free single-series line for inline context (dv-line-009 aspect). It reads as shape, and the figures live in the table.",
                 build_line("ln3", "12-month trend", "Twelve-month trend, indexed",
                            months, [("Trend", savings12)], dtype="spark"))

    # ---- 4 · Donut (two labelling versions: legend-right vs direct — Dave review #4/#5) ----
    dcats, dvals = ["Housing", "Groceries", "Savings", "Leisure", "Other"], [950, 420, 300, 260, 390]
    dcap = "Spend by category this month, pounds"
    d_letters = build_donut("dn1", "Spend by category", dcap, dcats, dvals, total_label="Total spend", mode="letters")
    d_spider = build_donut("dn2", "Spend by category", dcap, dcats, dvals, total_label="Total spend", mode="spider")
    d_direct = build_donut("dn3", "Spend by category", dcap, dcats, dvals, total_label="Total spend", mode="direct")
    tabs = ('<div class="variant-tabs" data-variant-group="donut" role="tablist">'
            '<button data-variant="letters" aria-selected="true">Legend + letters on segments</button>'
            '<button data-variant="spider" aria-selected="false">Legend + spider letters</button>'
            '<button data-variant="direct" aria-selected="false">Direct labels</button></div>')
    variants = (f'<div class="variant" data-variant-of="donut" data-variant="letters">{d_letters}</div>'
                f'<div class="variant" data-variant-of="donut" data-variant="spider" hidden>{d_spider}</div>'
                f'<div class="variant" data-variant-of="donut" data-variant="direct" hidden>{d_direct}</div>')
    h += section("Donut with centre total", "donut · composition · label variants",
                 "Composition, capped at six slices (dv-pie-009), summing to the stated total (dv-pie-010), separated by a 2px surface stroke (dv-004). A legend still needs the alphabetic label ON the chart — three variants to compare (switch below): <strong>letters on segments</strong>, <strong>spider-leg letters</strong> (letter on a short leader outside the ring), and <strong>direct labels</strong> (full name + value in place, no legend). Segments grow sequentially from the centre.",
                 tabs + variants)

    h += ('<section><p class="note">Every fill resolves to a <code>data/series-*</code> token (V7, '
          '<code>semantic-colour.json</code>). Gridline contrast is advisory (decorative); series-fill + '
          'axis/label contrast is blocking at &ge;3:1, computed from the resolved hex in both modes. '
          'Gated by <code>_validate_dataviz.py</code> (step 22 of <code>_build_all.py</code>).</p></section>')
    write("DataViz-interactive.html", h + FOOT)

if __name__ == "__main__":
    main()

