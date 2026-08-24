#!/usr/bin/env python3
"""
Mint the Nio dashboard composed screen — knowledge/_fitness-test/nio-dash-console-v1.canon.html

WHY A GENERATOR (s200-D1, mint-time derivation): the canon chart components carry BAKED SVG
geometry (rect x/y/width/height, polyline points, donut arc `d`, data-fx/data-fw/data-fxs
reflow hooks). Hand-typing that geometry for new data is exactly the "hand-rolling invents
defects" failure. So the DATA lives here as plain lists, and the geometry is DERIVED with the
same arithmetic canon's own snippets encode:

    plot frame   viewBox 0 0 580 260 · data-pl=46 · data-pr=12 · data-h=260
    x            46 .. 568   (522 wide)
    y            230 (domain 0) .. 14 (domain max)   → 216px of range
    data-fx      (x - 46) / 522          data-fw  width / 522
    donut        cx150 cy130 ro100 ri60, θ from -90°, x=cx+r·cosθ, y=cy+r·sinθ

Nothing here authors a colour, a font-size or a font-weight. Every fill is var(--data-series-N)
or a canon semantic token; every text element carries a .t-cm-* / .t-ed-* composite.

Run:  python3 knowledge/_render/gen_nio_dash.py
Gate: python3 knowledge/_validate_screen.py --render
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)

import math, os

HERE = os.path.dirname(os.path.abspath(__file__))
KNOW = os.path.dirname(HERE)
OUT = os.path.join(KNOW, "_fitness-test", "nio-dash-console-v2.canon.html")

# ---------------------------------------------------------------- plot frame constants
X0, X1, Y0, YT = 46.0, 568.0, 230.0, 14.0
W = X1 - X0          # 522
H = Y0 - YT          # 216


def fx(x):
    return round((x - X0) / W, 4)


def ypos(v, vmax):
    return round(Y0 - H * (v / vmax), 1)


def axis(vmax, ticks):
    """Grid lines + value labels, bottom to top (canon order)."""
    out = []
    for i, t in enumerate(ticks):
        y = ypos(t, vmax)
        out.append(f'<line class="dv-grid" x1="46" y1="{y}" x2="568" y2="{y}" '
                   f'stroke="var(--data-grid)" data-fx="0" data-fx2="1"/>')
        out.append(f'<text class="dv-axis t-cm-chart-value" fill="var(--data-axis)" x="38" '
                   f'y="{round(y + 3, 1)}" text-anchor="end" data-fx="0" data-dx="-8">{t}</text>')
    out.append('<line class="dv-axis" x1="46" y1="230" x2="568" y2="230" '
               'stroke="var(--baseline)" data-fx="0" data-fx2="1"/>')
    return "\n        ".join(out)


def cat_labels(names):
    """Slot-centred category labels for a column chart."""
    slot = W / len(names)
    out = []
    for i, n in enumerate(names):
        cx = X0 + i * slot + slot / 2
        out.append(f'<text class="dv-label t-cm-chart-label" fill="var(--data-axis)" '
                   f'x="{round(cx,1)}" y="246" text-anchor="middle" data-fx="{fx(cx)}">{n}</text>')
    return "\n        ".join(out)


def point_labels(names):
    """Point-aligned labels for a line chart."""
    n = len(names)
    out = []
    for i, nm in enumerate(names):
        x = X0 + i * W / (n - 1)
        out.append(f'<text class="dv-label t-cm-chart-label" fill="var(--data-axis)" '
                   f'x="{round(x,1)}" y="246" text-anchor="middle" data-fx="{fx(x)}">{nm}</text>')
    return "\n        ".join(out)


KEYS = "ABCDEFGH"


def grouped_columns(groups, series, data, vmax, bw, step, unit=""):
    """groups: month names · series: [(letter, name)] · data[g][s] = value."""
    slot = W / len(groups)
    gw = step * len(series) - (step - bw)
    off = (slot - gw) / 2
    bars, keys, delay = [], [], 0
    for gi, g in enumerate(groups):
        for si, (ltr, sname) in enumerate(series):
            v = data[gi][si]
            x = X0 + gi * slot + off + si * step
            y = ypos(v, vmax)
            h = round(Y0 - y, 1)
            lab = f"{ltr}, {sname}, {g}: {v}{unit}"
            tip = f"{ltr} &middot; {sname} &middot; {g}: {v}{unit}"
            bars.append(
                f'<rect class="dv-series" data-series-group="{si+1}" data-grow="up" '
                f'style="animation-delay:{delay}ms" fill="var(--data-series-{si+1})" '
                f'x="{round(x,1)}" y="{y}" width="{bw}" height="{h}" data-fx="{fx(x)}" '
                f'data-fw="{round(bw/W,4)}" tabindex="0" role="img" aria-label="{lab}" '
                f'data-tip="{tip}"></rect>')
            keys.append(
                f'<text class="dv-barkey t-cm-chart-key" data-series-group="{si+1}" '
                f'fill="var(--ink)" x="{round(x+bw/2,1)}" y="{round(y-4,1)}" '
                f'text-anchor="middle" data-fx="{fx(x+bw/2)}">{ltr}</text>')
            delay += 45
    return "\n        ".join(bars + keys)


def line_series(values, vmax, si):
    n = len(values)
    pts, fxs, ys = [], [], []
    for i, v in enumerate(values):
        x = X0 + i * W / (n - 1)
        y = ypos(v, vmax)
        pts.append(f"{round(x,1)},{y}")
        fxs.append(str(fx(x)))
        ys.append(str(y))
    return (f'<polyline class="dv-series" data-series-group="{si}" pathLength="2400" fill="none" '
            f'stroke="var(--data-series-{si})" stroke-width="2.5" stroke-linejoin="round" '
            f'stroke-linecap="round" vector-effect="non-scaling-stroke" points="{" ".join(pts)}" '
            f'data-fxs="{" ".join(fxs)}" data-ys="{" ".join(ys)}"/>')


def markers(values, vmax, si, ltr, sname, months, unit=""):
    """Circle (1) · square (2) · diamond (3) · square (4) — canon's shape rotation."""
    n = len(values)
    out = []
    for i, v in enumerate(values):
        x = X0 + i * W / (n - 1)
        y = ypos(v, vmax)
        lab = f"{ltr}, {sname}, {months[i]}: {v}{unit}"
        tip = f"{ltr} &middot; {sname} &middot; {months[i]}: {v}{unit}"
        shape = {1: f'<circle class="dv-mk" style="--sc:var(--data-series-1)" cx="{round(x,1)}" cy="{y}" r="5.5"/>',
                 2: f'<rect class="dv-mk" style="--sc:var(--data-series-2)" x="{round(x-5.5,1)}" y="{round(y-5.5,1)}" width="11" height="11"/>',
                 3: f'<polygon class="dv-mk" style="--sc:var(--data-series-3)" points="{round(x,1)},{round(y-6.5,1)} {round(x+6.5,1)},{y} {round(x,1)},{round(y+6.5,1)} {round(x-6.5,1)},{y}"/>',
                 4: f'<rect class="dv-mk" style="--sc:var(--data-series-4)" x="{round(x-5.5,1)}" y="{round(y-5.5,1)}" width="11" height="11"/>'}[si]
        out.append(f'<g class="dv-marker" data-series-group="{si}" tabindex="0" role="img" '
                   f'aria-label="{lab}" data-tip="{tip}" data-fx="{fx(x)}" data-x0="{round(x,1)}" '
                   f'style="animation-delay:{i*110}ms">{shape}</g>')
    return "\n        ".join(out)


# ---------------------------------------------------------------- donut
CX, CY, RO, RI = 150.0, 130.0, 100.0, 60.0


def _pt(r, deg):
    a = math.radians(deg)
    return round(CX + r * math.cos(a), 2), round(CY + r * math.sin(a), 2)


def donut(rows, total, cur="&pound;"):
    segs, leaders, letters, legs = [], [], [], []
    a = -90.0
    for i, (ltr, name, val) in enumerate(rows):
        sweep = 360.0 * val / total
        a2 = a + sweep
        large = 1 if sweep > 180 else 0
        x1, y1 = _pt(RO, a)
        x2, y2 = _pt(RO, a2)
        x3, y3 = _pt(RI, a2)
        x4, y4 = _pt(RI, a)
        d = (f"M{x1:.2f} {y1:.2f} A{RO:.0f} {RO:.0f} 0 {large} 1 {x2:.2f} {y2:.2f} "
             f"L{x3:.2f} {y3:.2f} A{RI:.0f} {RI:.0f} 0 {large} 0 {x4:.2f} {y4:.2f} Z")
        pct = round(100.0 * val / total)
        segs.append(
            f'<path class="dv-series dv-donut-seg dv-marker" data-series-group="{i+1}" tabindex="0" '
            f'role="img" aria-label="{ltr}, {name}: {val} pounds, {pct} per cent" '
            f'data-tip="{ltr} &middot; {name}: {cur}{val:,}" data-tip-value="{ltr} &middot; {name}: {cur}{val:,}" '
            f'data-tip-percent="{ltr} &middot; {name}: {pct}%" data-cx="150" data-cy="130" data-ro="100" '
            f'data-ri="60" data-a1="{a:.3f}" data-a2="{a2:.3f}" fill="var(--data-series-{i+1})" '
            f'stroke="var(--page)" stroke-width="2" d="{d}"/>')
        mid = (a + a2) / 2
        lx1, ly1 = _pt(102, mid)
        lx2, ly2 = _pt(113, mid)
        tx, _ = _pt(122, mid)
        leaders.append(f'<polyline class="dv-leader dv-anno show" data-seq="{i}" '
                       f'data-series-group="{i+1}" points="{lx1},{ly1} {lx2},{ly2}"/>')
        letters.append(f'<text class="dv-key-el dv-anno show t-cm-chart-key" data-seq="{i}" '
                       f'data-series-group="{i+1}" fill="var(--ink)" x="{tx}" y="{round(ly2+4,1)}" '
                       f'text-anchor="middle">{ltr}</text>')
        legs.append(
            f'<li class="dv-legrow" data-series="{i+1}"><span class="dv-leg-sw" role="checkbox" '
            f'aria-checked="true" tabindex="0" aria-label="Show or hide {name}" '
            f'style="--sc:var(--data-series-{i+1})"></span><button type="button" '
            f'class="dv-leg-item t-cm-chart-label" data-series="{i+1}" aria-pressed="false" '
            f'aria-label="Isolate {name}"><span class="dv-key t-cm-chart-key">{ltr}</span>'
            f'<span class="dv-leg-name">{name}</span></button></li>')
        a = a2
    return ("\n        ".join(segs + leaders + letters),
            "\n        ".join(legs))


def spark(values, trend):
    """Twelve-point inline sparkline in the KPI tile slot (viewBox 0 0 200 48)."""
    lo, hi = min(values), max(values)
    rng = (hi - lo) or 1
    n = len(values)
    pts = []
    for i, v in enumerate(values):
        x = 3 + i * (197 - 3) / (n - 1)
        y = 45 - 42 * (v - lo) / rng
        pts.append(f"{round(x,1)},{round(y,1)}")
    ex, ey = pts[-1].split(",")
    return (f'<svg class="spark-inline" data-trend="{trend}" viewBox="0 0 200 48" '
            f'preserveAspectRatio="none" aria-hidden="true" data-bespoke="chart canvas — dataviz '
            f'geometry, not an icon (validate-dataviz territory)">\n'
            f'          <line class="dv-base" x1="3" y1="45" x2="197" y2="45"/>\n'
            f'          <polyline class="dv-series" points="{" ".join(pts)}"/>\n'
            f'          <circle class="dv-end" cx="{ex}" cy="{ey}" r="3"/>\n        </svg>')


def leg(rows, shapes=False, ident="", label="Series"):
    sw = {1: "sw-circle", 2: "sw-square", 3: "sw-diamond", 4: "sw-square"}
    out = []
    for i, (ltr, name) in enumerate(rows):
        cls = " " + sw[i + 1] if shapes else ""
        out.append(
            f'<li class="dv-legrow" data-series="{i+1}"><span class="dv-leg-sw{cls}" role="checkbox" '
            f'aria-checked="true" tabindex="0" aria-label="Show or hide {name}" '
            f'style="--sc:var(--data-series-{i+1})"></span><button type="button" '
            f'class="dv-leg-item t-cm-chart-label" data-series="{i+1}" aria-pressed="false" '
            f'aria-label="Isolate {name}"><span class="dv-key t-cm-chart-key">{ltr}</span>'
            f'<span class="dv-leg-name">{name}</span></button></li>')
    out.append(f'<li class="dv-leg-reset-wrap"><button type="button" class="dv-leg-reset '
               f't-cm-chart-label" data-for="{ident}" disabled>Reset</button></li>')
    return ("\n        ".join(out))


# ================================================================= THE DATA
# Figures are read from Nio-Dash.png. Where the reference prints a number, the number is
# verbatim. Where it only DRAWS a bar or a line (the four chart panels), the series are read
# off the drawn heights against the printed 0–100 axis — declared, not invented.

MONTHS12 = ["May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "Jan", "Feb", "Mar", "Apr"]

# Balances overview — grouped column, money in vs money out
BAL_SERIES = [("A", "Money in"), ("B", "Money out")]
BAL = [[45, 30], [62, 100], [18, 22], [55, 60], [85, 40], [42, 30],
       [58, 46], [50, 60], [95, 72], [40, 65], [30, 22], [20, 25]]

# Spending breakdown — the printed legend, verbatim
SPEND = [("A", "Payroll", 8500), ("B", "Rent", 2400), ("C", "Software", 1050),
         ("D", "Travel", 890), ("E", "Utilities", 314), ("F", "Other", 580)]
SPEND_TOTAL = sum(r[2] for r in SPEND)          # 13,734 — see the divergence note in the page

# Spending overview — single-series line
SPEND_LINE = [30, 100, 42, 8, 30, 28, 55, 62, 58, 65, 68, 88]

# Your spending — four-series line
YS_SERIES = [("A", "Payroll"), ("B", "Suppliers"), ("C", "Overheads"), ("D", "Travel")]
YS_LINES = {
    1: [30, 34, 40, 22, 62, 30, 42, 50, 40, 52, 60, 92],
    2: [22, 28, 45, 55, 44, 70, 38, 30, 34, 44, 62, 88],
    3: [10, 16, 30, 44, 30, 34, 44, 32, 38, 50, 74, 86],
    4: [12, 90, 46, 40, 58, 38, 30, 40, 36, 42, 52, 80],
}

# Your spending — grouped column, six months, three series
YS_MONTHS = ["May", "Jun", "Jul", "Aug", "Sep", "Oct"]
YS_BARS = [[30, 55, 44], [50, 68, 82], [18, 24, 14], [40, 52, 46], [92, 70, 60], [22, 46, 38]]

# KPI sparklines (12 points each), read off the reference tiles
SPK = {
    "combined": [96, 92, 88, 84, 86, 80, 74, 76, 70, 66, 62, 55],
    "spending": [40, 46, 52, 50, 58, 62, 60, 66, 72, 78, 82, 92],
    "credit":   [92, 88, 86, 80, 82, 74, 70, 72, 64, 58, 54, 48],
    "cashin":   [30, 38, 44, 42, 50, 54, 52, 60, 68, 62, 72, 86],
}

# ================================================================= ICONS (verbatim library paths)
P = {
    "menu":      'M0 15.6H18V14.4H0V15.6ZM0 2.40002V3.60002H18V2.40002H0ZM0 9.60002H18V8.40002H0V9.60002Z',
    "close":     'M16.5 2.35668L15.6433 1.5L9 8.14332L2.35668 1.5L1.5 2.35668L8.14332 9L1.5 15.6433L2.35668 16.5L9 9.85668L15.6433 16.5L16.5 15.6433L9.85668 9L16.5 2.35668Z',
    "search":    'M2.19675 12.803C3.66075 14.268 5.58075 15 7.49975 15C9.23175 15 10.9598 14.398 12.3577 13.206L17.1257 17.973L17.9748 17.125L13.2067 12.357C15.7197 9.41 15.5898 4.981 12.8048 2.196C11.3388 0.732 9.41875 0 7.49975 0C5.58075 0 3.66075 0.732 2.19675 2.197C-0.73225 5.126 -0.73225 9.874 2.19675 12.803ZM1.19975 7.5C1.19975 5.817 1.85575 4.235 3.04475 3.045C4.23375 1.855 5.81675 1.2 7.49975 1.2C9.18275 1.2 10.7648 1.855 11.9548 3.045C14.4108 5.501 14.4108 9.498 11.9548 11.955C10.7648 13.145 9.18275 13.8 7.49975 13.8C5.81675 13.8 4.23475 13.145 3.04475 11.955C1.85475 10.765 1.19975 9.183 1.19975 7.5Z',
    "profile":   'M16.191 12.775C15.993 12.286 15.713 11.831 15.345 11.453C14.47 10.552 13.375 9.87 12.083 9.451L9.01 12.524L5.932 9.445C4.633 9.864 3.533 10.548 2.654 11.453C2.286 11.832 2.006 12.286 1.808 12.775L0 17.25H18L16.191 12.775ZM2.921 13.225C3.07 12.857 3.27 12.542 3.515 12.29C4.11 11.677 4.82 11.191 5.63 10.84L9.012 14.221L12.386 10.847C13.19 11.197 13.894 11.681 14.485 12.29C14.73 12.542 14.93 12.857 15.079 13.226L16.221 16.051H1.779L2.921 13.225ZM9.01 9.25C11.459 9.25 12.5 6.952 12.5 4.891C12.5 2.751 11.479 0.75 9.01 0.75C6.541 0.75 5.5 2.732 5.5 4.891C5.5 7.011 6.52 9.25 9.01 9.25ZM9.01 1.95C11.077 1.95 11.3 4.007 11.3 4.891C11.3 6.064 10.818 8.05 9.01 8.05C6.811 8.05 6.7 5.419 6.7 4.891C6.7 4.007 6.925 1.95 9.01 1.95Z',
    "add":       'M18 8.4H9.6V0H8.4V8.4H0V9.6H8.4V18H9.6V9.6H18V8.4Z',
    "more":      'M1.5 7.5C0.672 7.5 0 8.172 0 9C0 9.828 0.672 10.5 1.5 10.5C2.328 10.5 3 9.829 3 9C3 8.171 2.328 7.5 1.5 7.5ZM16.5 7.5C15.672 7.5 15 8.172 15 9C15 9.828 15.672 10.5 16.5 10.5C17.328 10.5 18 9.829 18 9C18 8.171 17.328 7.5 16.5 7.5ZM9 7.5C8.172 7.5 7.5 8.172 7.5 9C7.5 9.828 8.172 10.5 9 10.5C9.828 10.5 10.5 9.828 10.5 9C10.5 8.172 9.828 7.5 9 7.5Z',
    "share":     'M12.9989 5.99986V7.21686H15.7819V15.7829H2.22091V7.21686H4.99891V5.99986H1.00391V16.9999H16.9989V5.99986H12.9989ZM8.39891 11.9999H9.59891V2.44786L11.9989 4.84786V3.15186L8.99891 0.151855L5.99891 3.15186V4.84786L8.39891 2.44786V11.9999Z',
    "sort":      'M1.5 7.5L9 0L16.5 7.5H1.5Z',
    "sort2":     'M16.5 10.5L9 18L1.5 10.5H16.5Z',
    "settings":  'M16.376 6.992C16.208 6.374 15.96 5.774 15.634 5.206L16.319 3.592L14.408 1.68L12.794 2.365C12.225 2.04 11.626 1.791 11.007 1.623L10.352 0H7.648L6.992 1.624C6.374 1.791 5.774 2.04 5.206 2.365L3.592 1.68L1.68 3.592L2.365 5.206C2.04 5.774 1.791 6.374 1.624 6.992L0 7.648V10.351L1.624 11.007C1.791 11.626 2.04 12.225 2.366 12.794L1.68 14.408L3.592 16.32L5.206 15.635C5.775 15.961 6.374 16.209 6.993 16.377L7.648 18H10.351L11.007 16.377C11.625 16.209 12.225 15.961 12.794 15.635L14.408 16.32L16.32 14.408L15.635 12.794C15.961 12.225 16.209 11.626 16.377 11.007L18 10.352V7.648L16.376 6.992ZM15.374 10.118L15.218 10.694C15.077 11.214 14.867 11.72 14.593 12.198L14.298 12.715L14.53 13.263L14.899 14.132L14.132 14.899L12.716 14.297L12.199 14.593C11.721 14.866 11.215 15.077 10.694 15.218L10.119 15.374L9.542 16.8H8.458L7.882 15.375L7.306 15.219C6.785 15.078 6.28 14.867 5.802 14.594L5.285 14.298L4.736 14.53L3.868 14.899L3.101 14.132L3.703 12.716L3.407 12.199C3.134 11.721 2.923 11.215 2.782 10.694L2.626 10.119L1.2 9.542V8.458L2.625 7.882L2.781 7.307C2.922 6.786 3.133 6.28 3.406 5.802L3.702 5.285L3.47 4.737L3.101 3.868L3.868 3.101L5.285 3.703L5.802 3.407C6.28 3.134 6.786 2.924 7.307 2.782L7.882 2.626L8.458 1.2H9.543L10.119 2.625L10.694 2.781C11.215 2.922 11.721 3.133 12.199 3.406L12.716 3.702L14.133 3.1L14.9 3.867L14.297 5.285L14.593 5.802C14.866 6.279 15.076 6.785 15.218 7.306L15.374 7.881L15.927 8.104L16.8 8.458V9.542L15.374 10.118ZM9 4.8C7.878 4.8 6.823 5.237 6.03 6.03C5.237 6.823 4.8 7.878 4.8 9C4.8 10.122 5.237 11.177 6.03 11.97C6.823 12.763 7.878 13.2 9 13.2C10.122 13.2 11.176 12.763 11.97 11.97C12.764 11.177 13.2 10.122 13.2 9C13.2 7.878 12.763 6.823 11.97 6.03C11.177 5.237 10.122 4.8 9 4.8ZM11.121 11.121C10.536 11.707 9.768 12 9 12C8.232 12 7.464 11.707 6.878 11.121C5.707 9.95 5.707 8.05 6.878 6.879C7.464 6.293 8.232 6 9 6C9.768 6 10.536 6.293 11.121 6.879C12.293 8.05 12.293 9.95 11.121 11.121Z',
    "edit":      'M17.368 1.584L16.416 0.632C15.994 0.211 15.441 0 14.889 0C14.337 0 13.784 0.211 13.362 0.632L2.954 11.041L0 18L6.959 15.046L17.368 4.638C18.211 3.795 18.211 2.427 17.368 1.584ZM6.276 14.032L2.265 15.734L3.967 11.723L12.421 3.269L14.729 5.577L6.276 14.032ZM16.519 3.789L15.578 4.73L13.27 2.422L14.211 1.481C14.392 1.3 14.633 1.2 14.889 1.2C15.145 1.2 15.386 1.3 15.567 1.481L16.519 2.433C16.893 2.807 16.893 3.415 16.519 3.789Z',
    "viewall":   'M1 17H8V1H1V17ZM2.2 2.2H6.8V15.8H2.2V2.2ZM10 1V5H17V1H10ZM15.8 3.8H11.2V2.2H15.8V3.8ZM10 17H17V13H10V17ZM11.2 14.2H15.8V15.8H11.2V14.2ZM10 11H17V7H10V11ZM11.2 8.2H15.8V9.8H11.2V8.2Z',
    "grid":      'M1 8H8V1H1V8ZM1 17H8V10H1V17ZM10 1V8H17V1H10ZM10 17H17V10H10V17Z',
    "kpiup":     'M16 12L2 12L9 5L16 12Z',
    "kpidown":   'M2 6H16L9 13L2 6Z',
    "ptcheck":   'M5.91547 15.9421L0.105469 10.1341L1.37747 8.86011L5.91547 13.3971L16.6215 2.69312L17.8935 3.96712L5.91547 15.9421Z',
    "aschev":    'M17 4.15198L9 12.15L1 4.15198V5.84798L9 13.848L17 5.84798V4.15198Z',
    "chevleft":  'M13.8483 17L5.85034 9L13.8483 1H12.1523L4.15234 9L12.1523 17H13.8483Z',
    "snhome":    'M9 0L1 8V18H8V11.2H10V18H17V8L9 0ZM15.8 16.8H11.2V10H6.8V16.8H2.2V8.497L9 1.697L15.8 8.497V16.8Z',
    "snacct":    'M16.5 5H1.5C0.675 5 0 5.675 0 6.5V16.5C0 17.325 0.675 18 1.5 18H16.5C17.325 18 18 17.325 18 16.5V6.5C18 5.675 17.325 5 16.5 5ZM16.8 16.5C16.8 16.663 16.663 16.8 16.5 16.8H1.5C1.337 16.8 1.2 16.663 1.2 16.5V6.5C1.2 6.337 1.337 6.2 1.5 6.2H16.5C16.663 6.2 16.8 6.337 16.8 6.5V16.5ZM3 12H5V10H3V12ZM14.8 2.6H3.2C2.537 2.6 2 3.137 2 3.8H16C16 3.137 15.463 2.6 14.8 2.6ZM12.8 0H5.2C4.537 0 4 0.537 4 1.2H14C14 0.537 13.463 0 12.8 0Z',
    "sncard":    'M16.5 6H1.5C0.675 6 0 6.675 0 7.5V16.5C0 17.325 0.675 18 1.5 18H16.5C17.325 18 18 17.325 18 16.5V7.5C18 6.675 17.325 6 16.5 6ZM16.8 16.5C16.8 16.663 16.663 16.8 16.5 16.8H1.5C1.337 16.8 1.2 16.663 1.2 16.5V10.2H16.8V16.5ZM16.8 9H1.2V7.5C1.2 7.337 1.337 7.2 1.5 7.2H16.5C16.663 7.2 16.8 7.337 16.8 7.5V9ZM15 12H12V13.2H15V12ZM13.05 1.221C13.085 1.207 13.122 1.2 13.159 1.2C13.262 1.2 13.389 1.258 13.441 1.387L14.82 4.8H16.114L14.553 0.938C14.318 0.355 13.753 0 13.159 0C12.973 0 12.784 0.035 12.601 0.109L0.988 4.8H4.192L13.05 1.221Z',
    "sntransfer": 'M15.003 7.18915H11.997V5.98497H15.003V7.18915ZM6.05701 8.62698L5.09401 9.58853H8.748V10.7837H5.06701L6.05701 11.7632H4.36501L2.79002 10.1996L4.36501 8.62698H6.05701ZM7.551 12.2216L9.126 13.7942L7.551 15.3309H5.85901L6.84901 14.3783H3.17702V13.1561H6.82201L5.85901 12.1946L7.551 12.2216ZM6.00301 7.18915C4.05227 7.18188 2.2899 8.35058 1.54002 10.1487C0.790141 11.9469 1.20094 14.0191 2.58033 15.3964C3.95972 16.7738 6.03509 17.1839 7.83595 16.4352C9.63682 15.6864 10.8073 13.9267 10.8 11.9789C10.7901 9.3377 8.64821 7.199 6.00301 7.18915ZM6.00301 5.99395C8.43708 5.99033 10.6332 7.45254 11.5655 9.6976C12.4978 11.9427 11.9823 14.5275 10.2599 16.2448C8.53746 17.9621 5.94795 18.4728 3.70091 17.5386C1.45386 16.6043 -0.00725782 14.4093 2.71165e-05 11.9789C2.34e-05 8.66709 2.6862 5.98094 6.00301 5.97598V5.99395ZM18 1.49175V10.4782C17.9986 10.6786 17.9589 10.8768 17.883 11.0623C17.6403 11.6097 17.0966 11.9623 16.497 11.9609H13.212C13.2075 11.5663 13.1714 11.1726 13.104 10.7837H16.497C16.664 10.779 16.7983 10.6449 16.803 10.4782V4.18768H4.20301V5.02342C3.78991 5.13033 3.3865 5.27161 2.99702 5.44578V1.49175C3.00197 0.666427 3.67343 -1.47967e-05 4.50001 2.46473e-10H16.497C17.3236 -1.47967e-05 17.995 0.666427 18 1.49175ZM16.497 1.1952H4.50001C4.42125 1.1952 4.3457 1.22644 4.29 1.28205C4.23431 1.33767 4.20301 1.4131 4.20301 1.49175V2.99248H16.803V1.49175C16.7981 1.32652 16.6625 1.19512 16.497 1.1952Z',
    "snchart":   'M11 0V7H18C18 3.134 14.866 0 11 0ZM12.2 1.325C14.437 1.797 16.203 3.563 16.675 5.8H12.2V1.325ZM9 2H8C3.582 2 0 5.582 0 10C0 14.418 3.582 18 8 18C12.418 18 16 14.418 16 10V9H9V2ZM1.2 10C1.2 6.318 4.143 3.317 7.8 3.21V9.551L2.885 14.466C1.839 13.27 1.2 11.71 1.2 10ZM8 16.8C6.392 16.8 4.914 16.236 3.749 15.299L8 11.049L12.251 15.299C11.086 16.236 9.608 16.8 8 16.8ZM14.79 10.2C14.742 11.831 14.12 13.317 13.115 14.466L8.849 10.2H14.79Z',
    "pdf":       'M3.69006 9.378H3.37306V10.176H3.64006C4.18706 10.176 4.26106 9.967 4.26106 9.763C4.26106 9.489 4.09506 9.378 3.69006 9.378ZM12.9891 0H2.78906V5.8H3.98906V1.2H11.7891V5H15.5891V16.8H3.98906V15.2H2.78906V18H16.7891V3.8L12.9891 0ZM12.9891 3.8V1.697L15.0921 3.8H12.9891ZM12.7891 13.99V7.01C12.7891 7.004 12.7851 7 12.7791 7H0.799062C0.793062 7 0.789062 7.004 0.789062 7.01V13.99C0.789062 13.995 0.793062 14 0.799062 14H12.7791C12.7851 14 12.7891 13.995 12.7891 13.99ZM4.54906 10.77L4.54806 10.771C4.37706 10.84 4.14306 10.877 3.89006 10.877H3.37306V12.15H2.46106V8.676H3.77606C4.09806 8.676 4.43606 8.692 4.72006 8.883C5.02206 9.088 5.18106 9.404 5.18106 9.795C5.18206 10.239 4.94506 10.604 4.54906 10.77ZM6.60206 12.151H5.47406V8.676H6.71206C7.98706 8.676 8.63406 9.255 8.63406 10.398C8.63306 11.952 7.54806 12.151 6.60206 12.151ZM11.3691 9.383H9.90606V10.058H11.2831V10.76H9.90606V12.152H9.00706V8.676H11.3691V9.383ZM6.64806 9.378H6.38506V11.449H6.62006C7.37906 11.449 7.70306 11.137 7.70306 10.406C7.70306 9.675 7.39806 9.378 6.64806 9.378Z',
    "download":  'M15.8 12V15.8H2.2V12H1V17H17V12H15.8ZM14 8.848V7.151L9.6 11.551V1H8.4V11.551L4 7.151V8.848L9 13.849L14 8.848Z',
    "tip":       'M5 17L5 1L13 9L5 17Z',
    "ftup":      'M16 12L2 12L9 5L16 12Z',
    "fglsec":    'M15.5 5.734H14V4C14 1.8 12.2 0 10 0H8C5.8 0 4 1.8 4 4V5.734H2.5C1.675 5.734 1 6.409 1 7.234V16.5C1 17.325 1.675 18 2.5 18H15.5C16.325 18 17 17.325 17 16.5V7.234C17 6.409 16.325 5.734 15.5 5.734ZM5.2 4C5.2 2.456 6.456 1.2 8 1.2H10C11.544 1.2 12.8 2.456 12.8 4V5.734H11.6V4C11.6 3.118 10.882 2.4 10 2.4H8C7.118 2.4 6.4 3.118 6.4 4V5.734H5.2V4ZM10.4 4V5.734H7.6V4C7.6 3.783 7.783 3.6 8 3.6H10C10.217 3.6 10.4 3.783 10.4 4ZM15.8 16.5C15.8 16.663 15.663 16.8 15.5 16.8H2.5C2.337 16.8 2.2 16.663 2.2 16.5V7.234C2.2 7.071 2.337 6.934 2.5 6.934H15.5C15.663 6.934 15.8 7.071 15.8 7.234V16.5ZM8.4 14H9.6V10H8.4V14Z',
    "fglmob":    'M4.78906 0H12.7891C13.8891 0 14.7891 0.9 14.7891 2V16C14.7891 17.1 13.8891 18 12.7891 18H4.78906C3.68906 18 2.78906 17.1 2.78906 16V2C2.78906 0.9 3.68906 0 4.78906 0ZM12.7891 1.2H4.78906C4.38906 1.2 3.98906 1.6 3.98906 2V13H13.5891V2C13.5891 1.6 13.1891 1.2 12.7891 1.2ZM12.7891 16.8H4.78906C4.38906 16.8 3.98906 16.4 3.98906 16V14.2H13.5891V16C13.5891 16.4 13.1891 16.8 12.7891 16.8Z',
    "success":   'M7.21594 13.553L3.58594 9.92401L4.85894 8.65001L7.21594 11.008L13.1409 5.08301L14.4139 6.35601L7.21594 13.553Z',
    "copy":      'M0 18H10.8V7.2H0V18ZM1.2 8.4H9.6V16.8H1.2V8.4ZM8.4 3.6H7.2V6H8.4V3.6ZM8.4 1.2H9.6V0H7.2V2.4H8.4V1.2ZM15.6 0V1.2H16.8V2.4H18V0H15.6ZM12 10.8H14.4V9.6H12V10.8ZM16.8 9.6H15.6V10.8H18V8.4H16.8V9.6ZM16.8 7.2H18V3.6H16.8V7.2ZM10.8 1.2H14.4V0H10.8V1.2Z',
    "tick":      'M7.21594 13.553L3.58594 9.92401L4.85894 8.65001L7.21594 11.008L13.1409 5.08301L14.4139 6.35601L7.21594 13.553Z',
    "arrowdn":   'M2 6H16L9 13L2 6Z',
}


def sym(i, vb="0 0 18 18"):
    return f'<symbol id="{i}" viewBox="{vb}"><path fill-rule="evenodd" clip-rule="evenodd" d="{P[i]}" fill="currentColor"/></symbol>'


def use(i):
    return f'<svg viewBox="0 0 18 18" aria-hidden="true"><use href="#{i}"/></svg>'


# chart tool cluster, copied verbatim from the canon chart snippets
def dv_tools(tid, caption, head, rows, seg=None):
    segments = ""
    if seg:
        segments = ('<div class="seg sm" role="group" aria-label="Range">'
                    '<span class="ind" aria-hidden="true"></span>' +
                    "".join(f'<button type="button" class="t-cm-chart-label" aria-pressed="'
                            f'{"true" if i == 0 else "false"}">{s}</button>' for i, s in enumerate(seg)) +
                    '</div>')
    body = "".join(f'<tr><th scope="row">{a}</th><td>{b}</td></tr>' for a, b in rows)
    return f'''<div class="dv-controls" role="group" aria-label="Chart tools">
        {segments}
        <button type="button" class="dv-vt dv-act dv-csv t-cm-chart-label"><svg class="dv-ico dv-ico-copy" viewBox="0 0 18 18" aria-hidden="true" focusable="false"><path d="{P["copy"]}" fill="currentColor"/></svg><svg class="dv-ico dv-ico-tick" viewBox="0 0 18 18" aria-hidden="true" focusable="false"><path d="{P["tick"]}" fill="currentColor"/></svg><span>Copy data (CSV)</span></button>
        <details class="dv-tbl">
          <summary class="dv-tbl-toggle dv-vt dv-dd t-cm-chart-label" aria-controls="{tid}"><span>View as table</span><svg class="dv-ico dv-ico-arrow" viewBox="0 0 18 18" aria-hidden="true" focusable="false"><path d="{P["arrowdn"]}" fill="currentColor"/></svg></summary>
          <div class="dv-tablepanel" id="{tid}" role="region" aria-label="{caption}, data table" tabindex="-1">
          <table class="dv-table t-cm-legal"><caption>{caption}</caption>
          <thead><tr><th scope="col">{head[0]}</th><th scope="col">{head[1]}</th></tr></thead>
          <tbody>{body}</tbody></table>
          </div>
        </details>
      </div>'''


# ================================================================= BUILD
def build():
    # ---- charts -------------------------------------------------------
    bal_rows = [(m, " / ".join(str(v) for v in BAL[i])) for i, m in enumerate(MONTHS12)]
    bal_chart = f'''<figure class="dv dv-animate" data-dv-type="grouped-column" data-domain-min="0" data-surface="page" role="group" aria-labelledby="bal-h">
      <figcaption id="bal-h" class="sr-only">Money in and money out by month, thousands of euro</figcaption>
      <div class="dv-head">
        <h3 class="dv-title t-cm-section-label">Balances overview</h3>
        {dv_tools("bal-tbl", "Money in and money out by month, thousands of euro", ("Month", "In / out"), bal_rows, seg=["1Y", "6M", "3M", "1M"])}
      </div>
      <div class="dv-stage"><div class="dv-chart-area">
      <svg class="dv-svg dv-fit" data-pl="46" data-pr="12" data-h="260" data-bespoke="chart canvas — dataviz geometry, not an icon (validate-dataviz territory)" viewBox="0 0 580 260" role="group" aria-label="Money in and money out by month, thousands of euro, twelve months to April.">
        {axis(100, [0, 20, 40, 60, 80, 100])}
        {grouped_columns(MONTHS12, BAL_SERIES, BAL, 100, 14, 16)}
        {cat_labels(MONTHS12)}
      </svg>
      </div></div>
      <ul class="dv-leg center t-cm-chart-label" id="bal-legend" role="group" aria-label="Series — uncheck a swatch to dim it, click a name to isolate — then check swatches to add — Reset to show all">
        {leg(BAL_SERIES, ident="bal-legend")}
      </ul>
      <p class="dv-sr" id="bal-live" role="status" aria-live="polite"></p>
    </figure>'''

    segs, legs = donut(SPEND, SPEND_TOTAL)
    # ⑤ the LIST-style legend rows: identical dv-legend class contract, one extra value cell
    #    placed INSIDE .dv-leg-item AFTER .dv-leg-name (nameOf() reads .dv-leg-name, untouched).
    legs_list = "\n        ".join(
        f'<li class="dv-legrow" data-series="{i+1}"><span class="dv-leg-sw" role="checkbox" '
        f'aria-checked="true" tabindex="0" aria-label="Show or hide {n}" '
        f'style="--sc:var(--data-series-{i+1})"></span><button type="button" '
        f'class="dv-leg-item t-cm-chart-label" data-series="{i+1}" aria-pressed="false" '
        f'aria-label="Isolate {n}"><span class="dv-key t-cm-chart-key">{l}</span>'
        f'<span class="dv-leg-name">{n}</span>'
        f'<span class="nio-leg-val t-cm-chart-label">{v:,}</span></button></li>'
        for i, (l, n, v) in enumerate(SPEND))
    donut_rows = [(f"{l}. {n}", f"{v:,}") for l, n, v in SPEND]
    donut_chart = f'''<figure class="dv" data-dv-type="donut" data-total="{SPEND_TOTAL}" data-surface="page" data-labelling="spider" role="group" aria-labelledby="sp-h">
      <figcaption id="sp-h" class="sr-only">Spending breakdown this month, pounds</figcaption>
      <div class="dv-head">
        <h3 class="dv-title t-cm-section-label">Spending breakdown</h3>
        {dv_tools("sp-tbl", "Spending breakdown this month, pounds", ("Category", "Amount (&pound;)"), donut_rows)}
      </div>
      <div class="dv-stage"><div class="dv-donut-row">
        <svg class="dv-svg" data-bespoke="chart canvas — dataviz geometry, not an icon (validate-dataviz territory)" viewBox="0 0 300 260" width="300" height="260" role="group" aria-label="Spending by category. Total {SPEND_TOTAL:,} pounds.">
        {segs}
        <g data-dv-view="value"><text class="dv-val t-cm-figure-3" fill="var(--ink)" x="150" y="138" text-anchor="middle">&pound;{SPEND_TOTAL:,}</text></g>
        </svg>
        <ul class="dv-leg vert t-cm-chart-label" id="sp-legend" data-leg-variant="capsule" role="group" aria-label="Categories — uncheck a swatch to dim it, click a name to isolate — then check swatches to add — Reset to show all">
        {legs}
        <li class="dv-leg-reset-wrap"><button type="button" class="dv-leg-reset t-cm-chart-label" data-for="sp-legend" disabled>Reset</button></li>
        </ul>
        <p class="dv-sr" id="sp-live" role="status" aria-live="polite"></p>
        <ul class="dv-leg vert nio-leg-list nio-leg-off t-cm-chart-label" id="sp-legend-list" data-leg-variant="list" hidden role="group" aria-label="Categories with values — uncheck a swatch to dim it, click a row to isolate — then check swatches to add — Reset to show all">
        {legs_list}
        <li class="nio-leg-total t-cm-chart-label"><span class="nio-leg-total-k">Total</span><span class="nio-leg-val">{SPEND_TOTAL:,}</span></li>
        <li class="dv-leg-reset-wrap"><button type="button" class="dv-leg-reset t-cm-chart-label" data-for="sp-legend-list" disabled>Reset</button></li>
        </ul>
        <p class="dv-sr" id="sp-live-list" role="status" aria-live="polite"></p>
      </div></div>
    </figure>'''

    spend_summary = ('<dl class="summary">' + "".join(
        f'<div class="summary__row"><dt class="summary__k">{l}. {n}</dt>'
        f'<dd class="summary__v">{v:,}</dd></div>' for l, n, v in SPEND) +
        f'<div class="summary__row summary__row--total"><dt class="summary__k">Total</dt>'
        f'<dd class="summary__v">{SPEND_TOTAL:,}</dd></div></dl>')

    sl_rows = [(m, str(SPEND_LINE[i])) for i, m in enumerate(MONTHS12)]
    spend_line = f'''<figure class="dv dv-animate" data-dv-type="line" data-surface="page" role="group" aria-labelledby="sl-h">
      <figcaption id="sl-h" class="sr-only">Spending by month, thousands of pounds</figcaption>
      <div class="dv-head">
        <h3 class="dv-title t-cm-section-label">Spending Overview</h3>
        {dv_tools("sl-tbl", "Spending by month, thousands of pounds", ("Month", "Spend"), sl_rows, seg=["1Y", "6M", "3M", "1M"])}
      </div>
      <div class="dv-stage"><div class="dv-chart-area">
      <svg class="dv-svg dv-fit" data-pl="46" data-pr="12" data-h="260" data-bespoke="chart canvas — dataviz geometry, not an icon (validate-dataviz territory)" viewBox="0 0 580 260" role="group" aria-label="Spending by month, May to April.">
        {axis(100, [0, 20, 40, 60, 80, 100])}
        {line_series(SPEND_LINE, 100, 1)}
        {markers(SPEND_LINE, 100, 1, "A", "Spend", MONTHS12)}
        {point_labels(MONTHS12)}
      </svg>
      </div></div>
    </figure>'''

    ys_rows = [(m, " / ".join(str(YS_LINES[s][i]) for s in (1, 2, 3, 4)))
               for i, m in enumerate(MONTHS12)]
    ys_lines = "\n        ".join(line_series(YS_LINES[s], 100, s) for s in (1, 2, 3, 4))
    ys_marks = "\n        ".join(
        markers(YS_LINES[s], 100, s, YS_SERIES[s - 1][0], YS_SERIES[s - 1][1], MONTHS12)
        for s in (1, 2, 3, 4))
    ys_line = f'''<figure class="dv dv-animate" data-dv-type="multiline" data-surface="page" role="group" aria-labelledby="ysl-h">
      <figcaption id="ysl-h" class="sr-only">Spending by category by month, thousands of pounds</figcaption>
      <div class="dv-head">
        <h3 class="dv-title t-cm-section-label">Spending Overview</h3>
        {dv_tools("ysl-tbl", "Spending by category by month, thousands of pounds", ("Month", "Payroll / Suppliers / Overheads / Travel"), ys_rows, seg=["1Y", "6M", "3M", "1M"])}
      </div>
      <div class="dv-stage"><div class="dv-chart-area">
      <svg class="dv-svg dv-fit" data-pl="46" data-pr="12" data-h="260" data-bespoke="chart canvas — dataviz geometry, not an icon (validate-dataviz territory)" viewBox="0 0 580 260" role="group" aria-label="Spending by category over twelve months: Payroll, Suppliers, Overheads and Travel.">
        {axis(100, [0, 20, 40, 60, 80, 100])}
        {ys_lines}
        {ys_marks}
        {point_labels(MONTHS12)}
      </svg>
      </div></div>
      <ul class="dv-leg center t-cm-chart-label" id="ysl-legend" role="group" aria-label="Series — uncheck a swatch to dim it, click a name to isolate — then check swatches to add — Reset to show all">
        {leg(YS_SERIES, shapes=True, ident="ysl-legend")}
      </ul>
    </figure>'''

    ysb_series = [("A", "Payroll"), ("B", "Suppliers"), ("C", "Overheads")]
    ysb_rows = [(m, " / ".join(str(v) for v in YS_BARS[i])) for i, m in enumerate(YS_MONTHS)]
    ys_bars = f'''<figure class="dv dv-animate" data-dv-type="grouped-column" data-domain-min="0" data-surface="page" role="group" aria-labelledby="ysb-h">
      <figcaption id="ysb-h" class="sr-only">Spending by category by month, thousands of pounds</figcaption>
      <div class="dv-head">
        <h3 class="dv-title t-cm-section-label">Spending Overview</h3>
        {dv_tools("ysb-tbl", "Spending by category, six months", ("Month", "Payroll / Suppliers / Overheads"), ysb_rows, seg=["1Y", "6M", "3M", "1M"])}
      </div>
      <div class="dv-stage"><div class="dv-chart-area">
      <svg class="dv-svg dv-fit" data-pl="46" data-pr="12" data-h="260" data-bespoke="chart canvas — dataviz geometry, not an icon (validate-dataviz territory)" viewBox="0 0 580 260" role="group" aria-label="Spending by category over six months: Payroll, Suppliers and Overheads.">
        {axis(100, [0, 20, 40, 60, 80, 100])}
        {grouped_columns(YS_MONTHS, ysb_series, YS_BARS, 100, 20, 24)}
        {cat_labels(YS_MONTHS)}
      </svg>
      </div></div>
      <ul class="dv-leg center t-cm-chart-label" id="ysb-legend" role="group" aria-label="Series — uncheck a swatch to dim it, click a name to isolate — then check swatches to add — Reset to show all">
        {leg(ysb_series, ident="ysb-legend")}
      </ul>
    </figure>'''

    # ---- KPI tiles ----------------------------------------------------
    def kpi(label, cur, val, delta_cls, delta, per, sk, trend, status):
        arrow = ""
        if delta_cls:
            gl = "kpiup" if delta_cls == "up" else "kpidown"
            arrow = f'<span class="arrow" aria-hidden="true">{use(gl)}</span>'
        return f'''<div class="kpi-tile" role="group" aria-label="{label}">
        <p class="lbl16 t-cm-caption"><span class="stat {status}" data-carries="label"><span class="dot" aria-hidden="true"></span><span class="t-cm-caption">{label}</span></span></p>
        <span class="amt t-cm-figure-4"><span>{val}</span><span class="nio-cur t-cm-figure-6">{cur}</span></span>
        <span class="delta {delta_cls}" data-carries="symbol label">{arrow}<span class="t-cm-figure-6">{delta}</span><span class="per t-cm-legal">{per}</span></span>
        <div class="kpi-spark">{spark(SPK[sk], trend)}</div>
      </div>'''

    kpis = "\n      ".join([
        kpi("Combined cash balance - FX adjusted", "EUR", "32,875.00", "down",
            "&minus;1,900.78 down", "vs last month", "combined", "down", "err"),
        kpi("Spending this month", "EUR", "4,236.42", "up",
            "&minus;1,900.78 up", "vs last month", "spending", "up", "ok"),
        kpi("Total credit available", "EUR", "82,200.00", "down",
            "Limit: 100,000.00", "82% drawn", "credit", "down", "err"),
        kpi("Total cash in", "EUR", "2,278.70", "up",
            "7,345.70 up", "vs last month", "cashin", "up", "ok"),
    ])

    # ---- accounts -----------------------------------------------------
    ACCTS = [("Current Account", "42,710.18", "Current"),
             ("Business Reserve Savings", "60,000.00", "Savings"),
             ("Tax Savings", "22,825.38", "Savings"),
             ("Business Credit Card", "6,225.10", "Cards"),
             ("Business Credit Card", "6,225.10", "Cards"),
             ("UK Current Account", "42,710.18", "Current"),
             ("Instant access savings", "22,825.38", "Savings"),
             ("Instant access savings", "22,825.38", "Savings")]
    acct_rows = "\n          ".join(
        f'''<li><button class="row" type="button">
            <span class="body">
              <span class="line"><span class="title">{n}</span><span class="amount">{b} GBP</span></span>
              <span class="line"><span class="desc">GB | 001-011113-004</span><span class="tag">{t}</span></span>
            </span>
          </button></li>''' for n, b, t in ACCTS)

    # ---- predictive signals -------------------------------------------
    SIGNALS = [("USD", "Credit facility headroom", "48.5M", "3 of 5 tranches undrawn", 99, "ok"),
               ("USD", "30 day liquidity gap", "- 4.2M", "USD drawdown vs EUR surplus", 87, "warn"),
               ("EUR", "FX exposure (EUR)", "+12.4M", "Unhedged, maturing 45d", 91, "err"),
               ("USD", "30 day liquidity gap", "- 4.2M", "USD drawdown vs EUR surplus", 87, "warn")]
    signals = "\n      ".join(
        f'''<div class="stat-card nio-signal" role="group" aria-label="{title}">
        <div class="nio-signal-head">
          <span class="t-cm-caption em">{ccy}</span>
          <span class="t-cm-caption">{title}</span>
        </div>
        <span class="amt t-cm-figure-4">{val}</span>
        <p class="t-cm-legal nio-signal-note">{note}</p>
        <div class="meter">
          <div class="meter-track" role="progressbar" aria-labelledby="sig{i}-l" aria-valuenow="{conf}" aria-valuemin="0" aria-valuemax="100" aria-valuetext="Confidence {conf} percent">
            <div class="meter-fill" style="width:{conf}%"></div>
          </div>
        </div>
        <div class="nio-signal-foot">
          <span class="stat {tone}" data-carries="label"><span class="dot" aria-hidden="true"></span><span class="t-cm-legal" id="sig{i}-l">Confidence {conf}%</span></span>
          <a class="arrow" href="#"><span class="lbl t-cm-button">Inspect XAI</span><span class="tip" aria-hidden="true">{use("tip")}</span></a>
        </div>
      </div>''' for i, (ccy, title, val, note, conf, tone) in enumerate(SIGNALS))

    # ---- learn more ---------------------------------------------------
    FEATS = [("fglsec", "Manage your mandates online",
              "React to changes in your business and get greater control over your signatories by viewing, updating, and setting up bank mandates online."),
             ("snacct", "Make account changes seamlessly",
              "Maintaining up-to-date and accurate account information has never been easier. Change your business name, address and more with a few clicks."),
             ("fglmob", "A Digital Security Device in your pocket",
              "Securely log on to HSBCnet with mobile authentication. Generate codes in the banking app for seamless account access, anywhere, anytime, no extra device needed."),
             ("snchart", "Trade transactions on-the-go",
              "Trade Transaction Tracker gives you a global view of your documentary credits, collections, trade loans and guarantees across the world, all in a single app.")]
    feats = "\n          ".join(
        f'''<article class="card feat">
            <span class="ic" aria-hidden="true"><svg width="24" height="24" viewBox="0 0 18 18"><use href="#{g}"/></svg></span>
            <h3 class="t-cm-button">{t}</h3>
            <p class="t-ed-body-small">{d}</p>
            <p class="nio-feat-cta"><button class="btn primary" type="button">Find out more</button></p>
          </article>''' for g, t, d in FEATS)

    symbols = "".join(sym(k) for k in [
        "menu", "close", "search", "profile", "add", "more", "share", "settings", "edit",
        "viewall", "grid", "kpiup", "kpidown", "ptcheck", "aschev", "chevleft", "snhome",
        "snacct", "sncard", "sntransfer", "snchart", "pdf", "download", "tip", "ftup",
        "fglsec", "fglmob", "success"])
    symbols += (f'<symbol id="sort" viewBox="0 0 18 18"><path d="{P["sort"]}" fill="currentColor"/>'
                f'<path d="{P["sort2"]}" fill="currentColor"/></symbol>')

    html = f'''<!DOCTYPE html>
<html lang="en" data-apollo-theme="console" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Nio business-banking overview v2 — Apollo Console, review variants</title>
<link rel="stylesheet" href="../canon/type.css">
<link rel="stylesheet" href="../canon/canon.css">
<!--
  COMPOSED SCREEN — a recreation of Nio-Dash.png (HSBC "Nio" business-banking overview) under the
  APOLLO CONSOLE theme, assembled EXCLUSIVELY from components already in the library. Nothing here
  is a new component. Dave's constraint, verbatim: "recreate this using console components, don't
  invent anything apart from the header and footer."

  ⬛ NOT GATED-AS-CANON, NOTHING RULED, AWAITING DAVE'S EYE. Fitness-test surface.

  HOW IT IS BUILT
    · Root carries data-apollo-theme="console" + data-theme="light|dark" — Console resolution only.
      Radius therefore arrives per-theme (surface 20px / control 8px) from canon's own cascade.
    · Page scaffold = .cn-template-dashboard (.tpl-page/.tpl-section/.tpl-panel/.l-* utilities).
      Each component sits inside its own .cn-<component> scope, with the SNIPPET'S OWN MARKUP.
    · ZERO authored colour. The reference's HSBC reds and greens are NOT copied: financial
      direction and RAG arrive from canon's semantic tokens under Console resolution
      (--data-series-N, .status ok/warn/err, .delta up/down). Two-red law s151-D1 untouched.
    · ZERO font-size and ZERO font-weight declared on this page. Every text element carries a
      .t-cm-* / .t-ed-* composite. The style block below is LAYOUT HARNESS ONLY (.nio-*):
      no hex colour, no canon-class redefinition, no component CSS.
      (v2: this line no longer spells out the canon class prefixes with literal asterisks, and no
      longer names the style tag. Both were load-bearing defects — see the style block's own note
      and ds-041: the asterisk-slash closed the CSS comment and ate a rule, and the tag name in
      prose moved the compose gate's style-block scan window into this comment.)
    · Chart geometry is MINTED, not hand-typed — knowledge/_render/gen_nio_dash.py (s200-D1
      mint-time derivation). Re-run the generator to change the data; never edit the SVG here.

  CONTENT PROVENANCE
    · Every printed figure, label, account row, invoice line and predictive signal is verbatim
      from the reference.
    · ⚠ The reference's own spending arithmetic does not close: its six category rows sum to
      13,734 but it prints "£12,684" in the donut centre and in the Total row. This screen keeps
      the six rows verbatim and shows the ARITHMETIC SUM (13,734), because the donut arcs are
      derived from the rows. Declared, not silently reconciled.
    · The four chart panels print no numbers, only shapes. Their series are read off the drawn
      heights against the reference's own 0–100 axis — declared as a reading, not a measurement.

  MAPPING TABLE: nio-dash-console-v1.mapping.md, beside this file (v1's; v2 changes are the
  six items below and nothing else about the composition moved).

  ======================================================================================
  V2 — SIX CHANGES ON TOP OF v1. v1 IS PRESERVED UNTOUCHED BESIDE THIS FILE.
  Generator: knowledge/_render/gen_nio_dash_v2.py. NOTHING RULED. Awaiting Dave's eye.
  ======================================================================================

  ① LIGHT GREY PAGE BACKGROUND — and the reason v1 did not have one.
     v1 declared `body{{ background: var(--surface-hover) }}` and IT NEVER APPLIED — but NOT for
     the reason it looks like. THE RULE WAS NEVER PARSED. v1's harness header comment wrote its
     exclusion list with literal asterisks ("no .c-<star>/.cn-<star>"), and <star>-then-slash is a
     CSS COMMENT TERMINATOR: the comment closed early, the parser hit garbage and DISCARDED THE
     NEXT RULE, which was `body{{ }}`. Measured: v1's page style block parses to 44 rules with no
     body rule in it, and v1 still shows the browser's default 8px body margin — the other
     declaration in that same dead rule. Specificity was never involved, and a specificity fix
     would have been a false fix on a true symptom. The comment is repaired in v2's style block,
     where the mechanism is written out. v2 then FEEDS canon's own painting rule by re-pointing
     canon's own `--page` variable on <body>. Every .cn-* scope re-declares --page from
     --background-default, so component internals (including the donut's inter-segment
     stroke="var(--page)") are unaffected; only the .canon reset reads the new value.
     ⚠ THE GREY IS PER-MODE, AND THAT IS A TOKEN DEFECT, NOT A PREFERENCE. Under Console
     there is NO single surface token that is grey-and-distinct-from-card in BOTH modes:
        light: --surface-subtle   vs card --surface-raised   -> DISTINCT (grey on white) ✓
               --background-default vs card --surface-raised   -> IDENTICAL (both white)  ✗
        dark:  --surface-subtle   vs card --surface-raised   -> IDENTICAL (same grey)   ✗
               --background-default vs card --surface-raised   -> DISTINCT (darker)      ✓
     (The measured values are tabulated in nio-dash-console-v2.mapping.md. They are deliberately
      NOT written here: v1's own comment above carries a literal style tag, which makes the
      compose gate's style-block scan start there and swallow this comment — logged as a gate
      defect in _DS-IMPROVEMENTS.md.)
     So v2 selects --surface-subtle in light and --background-default in dark. ZERO values are
     minted; both are existing tokens read verbatim. This is the SAME defect v1's sibling
     exploration surfaced (surface/raised == background in light) seen from the other mode.
     LOGGED as a DS defect — the library has no "page behind raised surfaces" token that holds
     its meaning across light and dark.

  ② 1600px CONTENT COLUMN. .l-container's own `--l-max` (1120px) is RE-POINTED to 1600px on the
     page shell rather than overridden — the component keeps owning its own centring maths. The
     masthead and footer inners are given the same measure by a harness class so chrome stays
     full-bleed while its content lines up with the column.

  ③ THE CONSOLE-STYLING MISS ON INPUTS — ROOT CAUSE, MEASURED, NOT INFERRED.
     Dave read the search field as "not Console". It is not a cascade-order, specificity or
     scope problem: the field IS inside .cn-search-field, and --border-radius-control resolves
     to 8px ON THAT VERY ELEMENT. THE COMPONENT'S CSS SIMPLY NEVER CONSUMES IT.
        .cn-search-field .search.boxed  ->  border-radius 0px    (--border-radius-control = 8px)
        .cn-input-fields  boxed field   ->  border-radius 8px
        .cn-dropdown .trigger           ->  border-radius 8px
        .cn-account-selector .as-trigger->  border-radius 8px
        .cn-amount-input .ai-box        ->  border-radius 8px
        .btn.primary                    ->  border-radius 8px
     Search-field is the ONLY boxed control on this screen that draws a 1px box and declares no
     radius, so under Console (8px) it is the one square control in a family of rounded ones —
     which is exactly what "generic, not Console" looks like. THE CLASS: a sweep of all 135
     .cn-* scopes in canon.css finds 16 that declare no border-radius at all, and SEVEN of those
     nevertheless draw a full 1px box: .cn-search-field, .cn-headers (.frame), .cn-quick-actions
     (.qa), .cn-reorder (ul.reorder), .cn-view-options (.seg), .cn-splitter (.demo-box),
     .cn-pagination (.pg a). Every one of them is invisible under mono (radius 0) and wrong
     under the other three themes. That is why it survived review.
     WHERE THE REAL FIX LIVES: knowledge/snippets/Search-field.reference.html — canon.css is
     GENERATED from the snippets by canon/gen_canon_components.py, so a canon.css edit would be
     erased on the next regeneration. It is NOT applied here for two reasons, both stated:
     (a) it is a gated-snippet change, un-ruled, and would ripple through the whole library;
     (b) canon.css is shared, so changing it would retroactively restyle v1 — the artefact Dave
     asked to keep as the comparison. LOGGED to _DS-IMPROVEMENTS.md instead.
     WHAT v2 DOES: one page-level rule, applied to the CLASS of boxed search fields on this
     screen (both instances and any added later), consuming the token the component forgot —
     `.nio-shell .search.boxed{{ border-radius: var(--border-radius-control) }}`. It names no
     .cn-* selector, so the compose gate's redefinition check stays satisfied.
     ⚙ WHAT A COMPILED PER-THEME STYLESHEET WOULD HAVE PREVENTED (evidence for the ADR-0011 /
     s200-D1 proposal, which this page does NOT build): a compiler minting a Console sheet from
     the override store would emit a CONCRETE `border-radius: 8px` for every rule that draws a
     box, and the absence of a radius declaration on a boxed control becomes a MISSING OUTPUT —
     a thing the compiler can be asked about ("which boxed controls got no radius under
     console?") and can refuse to emit. Today the miss is a NON-EVENT: the token resolves
     correctly, nothing dangles, no gate has anything to look at, and the only detector is a
     human noticing one square corner among six rounded ones. The defect is not a wrong value;
     it is an UNCONSUMED value, and only a compiler that enumerates consumers can see it.

  ④ LIGHT / DARK SWITCH. data-theme on <html>, the bento showcase mechanism, driven from a
     .cn-segmented-control. Buttons, so keyboard operation is native; the sliding indicator is
     re-placed through canon's OWN dv-behaviour placeSegs() (a resize event), not re-implemented.

  ⑤ DONUT LEGEND — CAPSULE vs LIST, live toggle, NEITHER RECOMMENDED.
     v1 needed TWO blocks side by side to reproduce the reference: .dv-leg (the interactive
     filter, names only) plus a .cn-summary dl (the figures). v2 adds a LIST variant that merges
     them: one list, swatch + letter + label + value per row, plus the Total row.
     ⚙ IT NEEDED NO BEHAVIOUR-LAYER EXTENSION, AND THAT IS THE FINDING. dv-legend.js binds
     nothing to a layout: every listener is delegated at document level and resolves by CLASS
     CONTRACT (.dv-leg host, .dv-legrow[data-series], .dv-leg-sw, .dv-leg-item, .dv-leg-reset,
     .dv-leg-name), with state parked on the host as host.__dv. A list-shaped legend that honours
     that contract inherits hover-fade, ghost-toggle, isolate-latch (DV-D19), the "at least one
     must stay" guard, Reset and the live region for free. The value cell is added INSIDE
     .dv-leg-item, after .dv-leg-name, so nameOf() reads exactly what it read before.
     ⇒ COMPONENT-VARIANT CANDIDATE, not a new component: dv-legend gains a VALUE COLUMN and a
     list presentation. Gap-logged. This is the DS question v1's mapping row 19 already asked.
     ⚠ TWO HONEST LIMITS, both declared and neither hidden:
       · dv-legend keeps ONE state record per host. The two legends therefore hold SEPARATE
         states, so the variant switch RESETS the outgoing legend (its own Reset button is
         clicked) before swapping — selection does not carry across the switch.
       · dv-legend's hover path resolves a figure's legend with figure.querySelector('.dv-leg'),
         i.e. the FIRST one. The inactive legend therefore has its `dv-leg` class removed while
         hidden, so exactly one legend is ever discoverable. Without that, hovering an arc would
         drive the wrong record.

  ⑥ CHROMELESS ACCOUNT-LIST VARIANT, live toggle against v1's card form.
     .cn-list-items draws its chrome in exactly three places: ul.list carries
     `background:var(--surface)` + `border:1px solid var(--divider)` (the card), li+li carries
     `border-top:1px solid var(--divider)` (the separator), and .tag carries
     `border:1px solid var(--tag-border)` (the outline box). Chromeless = the first two
     declarations off, the SEPARATOR KEPT. Because the tag outline is genuinely ambiguous as
     "chrome", BOTH readings are offered: Chromeless (tags kept) and Chromeless, plain tags.
     Row behaviour, hover, press, focus ring and markup are untouched in every variant.
     ⇒ COMPONENT-VARIANT CANDIDATE for .cn-list-items: a `flush` form. Gap-logged.

  ⚙ EVERYTHING ELSE IS v1 VERBATIM. Still zero authored colour, zero font-size, zero
    font-weight, no canon-class redefinition, canon radius throughout, two-red law untouched.
-->
<style>
  /* ============ LAYOUT HARNESS ONLY. No colour values, no type, no canon-class redefinition.
     ⛔ v2 FIX — THIS COMMENT USED TO EAT THE NEXT RULE. v1 wrote the exclusion list with literal
     asterisks as "no .c-STAR/.cn-STAR"; that STAR-then-slash sequence is a CSS COMMENT TERMINATOR,
     so the comment closed early, the parser hit garbage and DISCARDED THE VERY NEXT RULE — which
     was body{{ }}. MEASURED on v1: its page style block parses to 44 rules with NO body rule at all,
     so BOTH of v1's body declarations were dead. Its page grey never applied (that, not
     specificity, is why v1's background stayed white) and v1 still carries the browser default 8px
     body margin. Same species as ds-039's SECOND form, which canon/gen_canon_components.py already
     guards against at the EMITTER for canon.css — but a composed screen writes its own style block
     and no gate parses it. Logged to _DS-IMPROVEMENTS.md. ============ */
  /* ① PAGE GREY — canon's OWN --page variable re-pointed, never an out-specified background.
     canon.css paints the page with `.canon`+background:var(--page), so feeding --page is the
     component-respecting move: every .cn- scope re-declares --page from --background-default, so
     nothing inside a component (the donut's inter-arc stroke included) is disturbed.
     Per-mode because no Console surface token is grey-and-distinct-from-card in BOTH modes —
     see the header note and the mapping table. Both values are EXISTING tokens; none is minted.
     ⚠ v1's grey was not lost to specificity. It was lost to the comment defect fixed above. */
  body{{ margin:0; --page:var(--surface-subtle); color:var(--text); }}
  [data-theme="dark"] body{{ --page:var(--background-default); }}

  /* ② 1600px MEASURE. .l-container owns its own --l-max (1120px default) — re-pointed, not
     overridden. Chrome stays full-bleed; its inner content takes the same measure. */
  .nio-shell{{ min-height:100vh; display:flex; flex-direction:column; --nio-max:1600px; }}
  .nio-shell > main{{ flex:1; --l-max:var(--nio-max); }}
  .nio-shell .sh-masthead,
  .nio-shell .ft-inner{{ width:100%; max-width:var(--nio-max); margin-inline:auto; }}

  /* ③ THE SEARCH-FIELD RADIUS MISS — the component draws a 1px box and never consumes
     --border-radius-control, so it renders square in every theme (invisible under mono, wrong
     under the other three). Applied to the CLASS of boxed search fields on this page, feeding
     the token the component forgot. Real home: knowledge/snippets/Search-field.reference.html
     (canon.css is generated from it) — logged to _DS-IMPROVEMENTS.md, not patched here, because
     canon.css is shared with v1. NOT a .cn-* redefinition: the selector names no canon scope. */
  .nio-shell .search.boxed{{ border-radius:var(--border-radius-control); }}

  /* ④⑤⑥ REVIEW BAR — page chrome for Dave's live comparison. Not part of any component; delete
     the bar and its controller and the page renders at its authored defaults. */
  .nio-review{{ position:sticky; top:0; z-index:20; display:flex; flex-wrap:wrap; align-items:center;
                gap:24px; padding:10px 32px; border-bottom:1px solid var(--divider);
                background:var(--surface-raised); }}
  .nio-review-in{{ display:flex; flex-wrap:wrap; align-items:center; gap:24px;
                   width:100%; max-width:var(--nio-max); margin-inline:auto; }}
  .nio-rv-grp{{ display:flex; align-items:center; gap:10px; }}

  /* ⑤ LIST-STYLE LEGEND — presentation only. Every dv-legend class contract is honoured, so the
     behaviour layer is untouched: swatch = check, label = isolate, Reset, hover fade, live
     region. The value cell sits INSIDE .dv-leg-item, after .dv-leg-name, so nameOf() is unmoved. */
  /* In LIST mode the separate figures column is withdrawn, so the donut panel collapses to a
     single column and .dv-donut-row's own flex lays donut | list SIDE BY SIDE — which is the
     placement asked for. No component rule is touched; only the harness grid changes. */
  .nio-donut-split[data-nio-leg="list"]{{ grid-template-columns:minmax(0,1fr); }}
  /* ⚠ `width:100%` here made the list take the WHOLE flex line and wrap under the donut —
     .dv-donut-row is `display:flex; flex-wrap:wrap`, so a 100%-wide item can never sit beside
     anything. It is a flex ITEM: give it a basis and let it share the line. */
  .nio-leg-list{{ align-self:center; flex:1 1 300px; min-width:0; }}

  /* ⚠ CANON SCOPE BLEED, FOUND WHILE PLACING THE LIST LEGEND — measured, and it affects v1 too.
     The PAGE-SHELL scope declares `:where(.cn-template-dashboard) .dv-svg{{width:580px;height:260px}}`
     (canon.css line ~16124). It is component-specific chart geometry living in a TEMPLATE scope,
     and it comes LATER in the file than `:where(.cn-chart-donut) .dv-svg`, which sets no width at
     all — so on any dashboard-templated page the DONUT is forced to 580px wide even though its own
     markup says width="300". In v1 that makes the donut overflow its 426px column and become
     horizontally SCROLLABLE (.dv-stage carries overflow-x:auto, which hides the symptom).
     v2 restores the size the svg's own width/height attributes already declare. No value is
     invented — 300 and 260 are read off the markup. Logged to _DS-IMPROVEMENTS.md. */
  .nio-donut-split .dv-svg{{ width:300px; height:260px; }}
  .nio-leg-list .dv-legrow{{ width:100%; }}
  .nio-leg-list .dv-leg-item{{ flex:1; min-width:0; display:flex; align-items:center; gap:10px; }}
  .nio-leg-list .dv-leg-name{{ flex:1; min-width:0; }}
  .nio-leg-val{{ flex:none; margin-left:auto; font-variant-numeric:tabular-nums; }}
  .nio-leg-total{{ display:flex; align-items:center; gap:10px; padding-top:8px; margin-top:4px;
                   border-top:1px solid var(--divider); }}
  .nio-leg-total .nio-leg-total-k{{ flex:1; }}
  .nio-leg-total .nio-leg-val{{ margin-left:auto; }}
  .nio-leg-off{{ display:none; }}

  /* ⑥ CHROMELESS LIST — the three chrome declarations .cn-list-items owns, switched off by
     data attribute. The SEPARATOR (li + li border-top) is deliberately kept: that is the whole
     brief. --surface-transparent is an existing canon token, not an authored value. */
  .nio-acct-list[data-nio-list="flush"] ul.list,
  .nio-acct-list[data-nio-list="flush-plain"] ul.list{{ background:var(--surface-transparent); border:0; }}
  .nio-acct-list[data-nio-list="flush-plain"] .row .tag{{ border:0; padding:0; height:auto; }}

  /* --- masthead (App-shell-top-nav's own .sh chrome, laid out for this screen).
     ⚠ THREE LAYOUT-ONLY OVERRIDES, declared: the shell's .sh frame is a SPECIMEN frame —
     min-height:560px + a 1px border + a 20px radius exist so the component reads as a card in
     the showroom. On a real page the masthead is full-bleed chrome. Nothing else about the
     component is touched: no colour, no type, no spacing inside the bar. --- */
  .nio-shell .sh{{ min-height:0; border:0; border-radius:0; border-bottom:1px solid var(--divider); }}
  .nio-brandrule{{ border-left:1px solid var(--divider); padding-left:12px; margin-left:12px; }}
  .nio-assist{{ flex:1; min-width:0; max-width:520px; margin-left:auto; display:flex; align-items:center; gap:8px; }}
  .nio-assist .search{{ flex:1; min-width:0; }}

  /* --- panels --- */
  .nio-panel-title{{ margin:0; }}
  .nio-flush{{ padding:0; }}
  .nio-flush > .nio-panel-title{{ padding:24px 24px 20px; }}
  .nio-divider{{ border-top:1px solid var(--divider); }}
  .nio-kpis{{ display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); }}
  .nio-kpis > .kpi-tile{{ border:0; border-left:1px solid var(--divider); border-radius:0; }}
  .nio-kpis > .kpi-tile:first-child{{ border-left:0; }}
  .nio-cur{{ margin-left:3px; }}
  .nio-acct-head .amount__cur{{ margin-left:3px; }}
  .nio-kpis .stat{{ margin:0; min-width:0; }}
  .nio-kpis .stat > span:last-child{{ min-width:0; overflow-wrap:anywhere; }}

  /* --- accounts --- */
  .nio-acct-head{{ display:flex; align-items:center; justify-content:space-between; gap:12px; padding:0 24px 12px; }}
  .nio-acct-list{{ border-top:1px solid var(--divider); padding:0 12px; }}
  .nio-acct-foot{{ padding:12px 24px 24px; }}
  .nio-two{{ display:grid; grid-template-columns:minmax(0,4fr) minmax(0,6fr); gap:24px; align-items:start; }}
  .nio-donut-split{{ display:grid; grid-template-columns:minmax(0,1fr) minmax(0,1fr); gap:24px; align-items:center; }}

  /* --- payments --- */
  .nio-pay{{ display:grid; grid-template-columns:220px minmax(0,1fr); gap:32px; align-items:start; }}
  .nio-pay-cols{{ display:grid; grid-template-columns:minmax(0,1fr) minmax(0,1fr); gap:32px; align-items:start; }}
  .nio-stack{{ display:flex; flex-direction:column; gap:16px; }}
  .nio-stack-s{{ display:flex; flex-direction:column; gap:8px; }}
  .nio-payee{{ border:1px solid var(--border); border-radius:var(--border-radius-container); padding:16px; }}
  .nio-payee-top{{ display:flex; align-items:flex-start; justify-content:space-between; gap:12px; }}
  .nio-invoice{{ display:flex; align-items:center; gap:12px; border:1px solid var(--border);
                border-radius:var(--border-radius-control); padding:12px 16px; }}
  .nio-invoice .nio-grow{{ flex:1; min-width:0; }}
  .nio-actions{{ display:flex; align-items:center; justify-content:space-between; gap:12px; margin-top:24px; }}
  .nio-actions-r{{ display:flex; gap:12px; }}

  /* --- predictive signals --- */
  .nio-signals{{ display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); }}
  .nio-signal{{ border:0; border-left:1px solid var(--divider); border-radius:0;
               display:flex; flex-direction:column; gap:10px; padding:20px; }}
  .nio-signals > .nio-signal:first-child{{ border-left:0; }}
  .nio-signal-head{{ display:flex; align-items:baseline; justify-content:space-between; gap:12px; }}
  .nio-signal-note{{ margin:0; }}
  .nio-signal .stat{{ margin:0; }}
  .nio-signal-foot{{ display:flex; align-items:center; justify-content:space-between; gap:12px; margin-top:auto; }}

  /* --- feedback + doormat --- */
  .nio-feedback{{ display:flex; flex-direction:column; align-items:center; gap:20px; padding:32px 24px; }}
  .nio-chips{{ display:flex; gap:16px; flex-wrap:wrap; justify-content:center; }}
  .nio-feat-cta{{ margin:16px 0 0; }}
  .nio-legal{{ margin:16px 0 0; max-width:70ch; }}

  /* --- narrow --- */
  @media (max-width:1100px){{
    .nio-review{{ padding:10px 16px; }}
  }}
  @media (max-width:900px){{
    .nio-two, .nio-pay, .nio-pay-cols, .nio-donut-split{{ grid-template-columns:minmax(0,1fr); }}
    .nio-kpis, .nio-signals{{ grid-template-columns:repeat(2,minmax(0,1fr)); }}
    .nio-kpis > .kpi-tile:nth-child(odd),
    .nio-signals > .nio-signal:nth-child(odd){{ border-left:0; }}
  }}
  @media (max-width:560px){{
    .nio-kpis, .nio-signals{{ grid-template-columns:minmax(0,1fr); }}
    .nio-kpis > .kpi-tile, .nio-signals > .nio-signal{{ border-left:0; border-top:1px solid var(--divider); }}
  }}
</style>
</head>
<body class="canon">
<svg width="0" height="0" style="position:absolute" aria-hidden="true">{symbols}</svg>

<div class="cn-template-dashboard nio-shell">

<!-- ============ REVIEW BAR (v2) — page chrome, NOT a component. Every control is a canon
     Segmented-control: real <button>s, so Tab + Enter/Space work natively. ============ -->
<div class="nio-review" role="region" aria-label="Review controls">
  <div class="nio-review-in">
    <div class="nio-rv-grp">
      <span class="t-cm-legal" id="rvModeL">Mode</span>
      <div class="cn-segmented-control">
        <div class="seg sm" id="rvMode" role="group" aria-labelledby="rvModeL">
          <span class="ind" aria-hidden="true"></span>
          <button type="button" class="t-cm-button" data-v="light" aria-pressed="true">Light</button>
          <button type="button" class="t-cm-button" data-v="dark" aria-pressed="false">Dark</button>
        </div>
      </div>
    </div>
    <div class="nio-rv-grp">
      <span class="t-cm-legal" id="rvLegL">Donut legend</span>
      <div class="cn-segmented-control">
        <div class="seg sm" id="rvLeg" role="group" aria-labelledby="rvLegL">
          <span class="ind" aria-hidden="true"></span>
          <button type="button" class="t-cm-button" data-v="capsule" aria-pressed="true">Capsule + values</button>
          <button type="button" class="t-cm-button" data-v="list" aria-pressed="false">One list</button>
        </div>
      </div>
    </div>
    <div class="nio-rv-grp">
      <span class="t-cm-legal" id="rvListL">Account list</span>
      <div class="cn-segmented-control">
        <div class="seg sm" id="rvList" role="group" aria-labelledby="rvListL">
          <span class="ind" aria-hidden="true"></span>
          <button type="button" class="t-cm-button" data-v="card" aria-pressed="true">Card</button>
          <button type="button" class="t-cm-button" data-v="flush" aria-pressed="false">Chromeless</button>
          <button type="button" class="t-cm-button" data-v="flush-plain" aria-pressed="false">Chromeless, plain tags</button>
        </div>
      </div>
    </div>
    <p class="t-cm-legal" style="margin:0; max-width:56ch">Neither legend and neither list form is a
      recommendation — both are here to be compared. Nothing on this page is ruled.</p>
  </div>
</div>

<!-- ============ MASTHEAD — App-shell-top-nav (inline form) + Search-field + Icon-button ====== -->
<div class="cn-app-shell-top-nav">
  <div class="sh" data-form="inline">
    <a class="sh-skip t-cm-button" href="#nio-main">Skip to main content</a>
    <header class="sh-masthead">
      <span class="sh-logo t-ed-heading-4" aria-label="HSBC">HSBC</span>
      <span class="t-cm-caption nio-brandrule">NIO</span>
      <nav class="sh-nav" aria-label="Primary">
        <a class="t-cm-button" href="#" aria-current="page">Overview</a>
        <a class="t-cm-button" href="#">Spending</a>
        <a class="t-cm-button" href="#">Payments</a>
        <a class="t-cm-button" href="#">Authorisations</a>
      </nav>
      <div class="nio-assist">
        <div class="cn-icon-button"><button class="iconbtn tertiary" type="button" aria-label="Add a shortcut">{use("add")}</button></div>
        <div class="cn-search-field">
          <div class="search boxed">
            <span class="mag" aria-hidden="true">{use("search")}</span>
            <input type="search" aria-label="Nio assist: ask a question or search for something" placeholder="Nio assist: ask a question or search for something" value="">
          </div>
        </div>
      </div>
      <div class="sh-actions">
        <button type="button" aria-label="Notifications">{use("more")}</button>
        <button type="button" aria-label="Your profile">{use("profile")}</button>
      </div>
    </header>
  </div>
</div>

<main class="tpl-page l-container" id="nio-main">
  <div class="l-stack" data-gap="xxl">

    <!-- ============ BALANCES ============ -->
    <section class="tpl-section" aria-labelledby="bal-sec">
      <div class="stat-card tpl-panel nio-flush">
        <h2 id="bal-sec" class="nio-panel-title t-ed-heading-3">Balances</h2>
        <div class="cn-kpi-tile cn-status-indicator nio-divider">
          <div class="nio-kpis">
      {kpis}
          </div>
        </div>
        <div class="cn-chart-bar cn-segmented-control nio-divider" style="padding:24px">
      {bal_chart}
        </div>
      </div>
    </section>

    <!-- ============ ACCOUNTS  |  SPENDING ============ -->
    <section class="tpl-section" aria-label="Accounts and spending">
      <div class="nio-two">

        <div class="stat-card tpl-panel nio-flush">
          <h2 class="nio-panel-title t-ed-heading-3" id="acct-h">Accounts</h2>
          <div class="nio-acct-head">
            <div class="cn-amount-display nio-stack-s">
              <p class="t-cm-caption" id="bal-total-l" style="margin:0">Balance total</p>
              <span class="amount amount--display t-cm-figure-4" aria-labelledby="bal-total-l"><span class="amount__val">112,514.11</span><span class="amount__cur">GBP</span></span>
            </div>
          </div>
          <div class="nio-acct-head">
            <div class="cn-segmented-control">
              <div class="seg sm" role="group" aria-label="Filter accounts">
                <span class="ind" aria-hidden="true"></span>
                <button type="button" aria-pressed="true">All</button>
                <button type="button" aria-pressed="false">Current</button>
                <button type="button" aria-pressed="false">Cards</button>
              </div>
            </div>
            <div class="cn-view-options">
              <div class="seg" role="group" aria-label="List tools">
                <span class="ind" aria-hidden="true"></span>
                <button type="button" aria-pressed="false" aria-label="Filter accounts">{use("settings")}</button>
                <button type="button" aria-pressed="false" aria-label="Sort accounts">{use("sort")}</button>
              </div>
            </div>
          </div>
          <div class="cn-list-items nio-acct-list" id="acctList" data-nio-list="card">
            <ul class="list" aria-labelledby="acct-h">
          {acct_rows}
            </ul>
          </div>
          <div class="cn-search-field nio-acct-foot">
            <div class="search boxed">
              <span class="mag" aria-hidden="true">{use("search")}</span>
              <input type="search" aria-label="Search accounts" placeholder="Search" value="">
            </div>
          </div>
        </div>

        <div class="nio-stack">
          <div class="stat-card tpl-panel">
            <h2 class="nio-panel-title t-ed-heading-3">Spending</h2>
            <div class="cn-chart-donut cn-summary nio-donut-split" style="margin-top:20px">
        {donut_chart}
              <div id="spSummary">{spend_summary}</div>
            </div>
          </div>
          <div class="stat-card tpl-panel cn-chart-line cn-segmented-control">
      {spend_line}
          </div>
        </div>

      </div>
    </section>

    <!-- ============ PAYMENTS ============ -->
    <section class="tpl-section" aria-labelledby="pay-h">
      <div class="stat-card tpl-panel nio-flush">
        <h2 id="pay-h" class="nio-panel-title t-ed-heading-3">Payments</h2>
        <div class="nio-divider" style="padding:24px">
          <div class="nio-pay">

            <div class="cn-sidebar-nav">
              <nav class="sn" aria-label="Payment types">
                <div class="sn-body">
                  <div class="sn-group">
                    <ul>
                      <li><a class="sn-link" href="#"><span class="si" aria-hidden="true">{use("sntransfer")}</span><span class="sn-label t-cm-label">Transfers</span></a></li>
                      <li><a class="sn-link" href="#" aria-current="page"><span class="si" aria-hidden="true">{use("pdf")}</span><span class="sn-label t-cm-label">Bills</span></a></li>
                      <li><a class="sn-link" href="#"><span class="si" aria-hidden="true">{use("snacct")}</span><span class="sn-label t-cm-label">Standing Orders</span></a></li>
                      <li><a class="sn-link" href="#"><span class="si" aria-hidden="true">{use("sncard")}</span><span class="sn-label t-cm-label">Direct Debits</span></a></li>
                      <li><a class="sn-link" href="#"><span class="si" aria-hidden="true">{use("snhome")}</span><span class="sn-label t-cm-label">Payments</span></a></li>
                      <li><a class="sn-link" href="#"><span class="si" aria-hidden="true">{use("snchart")}</span><span class="sn-label t-cm-label">Term Deposit</span></a></li>
                    </ul>
                  </div>
                </div>
              </nav>
            </div>

            <div class="nio-stack">
              <h3 class="t-ed-heading-4" style="margin:0">Make a payment</h3>

              <div class="cn-progress-tracker">
                <div class="pt" style="--demo-width:100%">
                  <ol class="steps" aria-label="Make a payment progress">
                    <li class="done"><span class="dot" aria-hidden="true">{use("ptcheck")}</span><span class="step-label">Payee</span></li>
                    <li class="current" aria-current="step"><span class="dot" aria-hidden="true">2</span><span class="step-label">Details</span></li>
                    <li><span class="dot" aria-hidden="true">3</span><span class="step-label">Review</span></li>
                  </ol>
                </div>
              </div>

              <div class="cn-document-row cn-status-indicator nio-invoice">
                <span class="dr-glyph" aria-hidden="true">{use("pdf")}</span>
                <span class="nio-grow t-cm-label">British_Gas_Invoice_April_2024.pdf</span>
                <span class="status ok" data-carries="label"><span class="dot" aria-hidden="true"></span><span class="t-cm-legal">Validated</span></span>
              </div>

              <div class="nio-pay-cols">

                <div class="nio-stack-s">
                  <p class="t-cm-label" style="margin:0">Paying to</p>
                  <div class="cn-tags cn-summary nio-payee">
                    <div class="nio-payee-top">
                      <div>
                        <p class="t-ed-heading-4" style="margin:0">British Gas Business</p>
                        <p class="t-ed-body-small" style="margin:4px 0 0">1st Floor, Millstream, Maidenhead Road, Windsor, SL4 5GD</p>
                      </div>
                      <span class="tag"><span class="lbl">Utility</span></span>
                    </div>
                    <dl class="summary" style="margin-top:12px">
                      <div class="summary__row"><dt class="summary__k">INV-2026-04-15678</dt><dd class="summary__v">Issued: 20 April 2026</dd></div>
                      <div class="summary__row"><dt class="summary__k">&nbsp;</dt><dd class="summary__v">Due: 29 April 2026</dd></div>
                    </dl>
                  </div>
                  <div class="cn-summary">
                    <dl class="summary">
                      <div class="summary__row"><dt class="summary__k">Account number</dt><dd class="summary__v">12343181</dd></div>
                      <div class="summary__row"><dt class="summary__k">Sort code</dt><dd class="summary__v">38-15-81</dd></div>
                      <div class="summary__row"><dt class="summary__k">Reference</dt><dd class="summary__v">GAS-APR-2026</dd></div>
                    </dl>
                  </div>
                  <div class="cn-accordion cn-summary">
                    <div class="acc">
                      <div class="item">
                        <button class="head" type="button" aria-expanded="true" aria-controls="gasPanel"><span class="t-cm-label">Gas Supply &ndash; total &nbsp; &pound;1,247.85 GBP</span><span class="chev" aria-hidden="true">{use("aschev")}</span></button>
                        <div class="panel" id="gasPanel" style="max-height:220px"><div class="inner">
                          <dl class="summary">
                            <div class="summary__row"><dt class="summary__k">Gas Supply (March 2026)</dt><dd class="summary__v">&pound;1,058.25</dd></div>
                            <div class="summary__row"><dt class="summary__k">Standing Charge</dt><dd class="summary__v">&pound;13.95</dd></div>
                            <div class="summary__row"><dt class="summary__k">Network Charges</dt><dd class="summary__v">&pound;125.00</dd></div>
                            <div class="summary__row"><dt class="summary__k">VAT (5%)</dt><dd class="summary__v">&pound;50.65</dd></div>
                          </dl>
                        </div></div>
                      </div>
                    </div>
                  </div>
                </div>

                <div class="nio-stack">
                  <div class="cn-account-selector">
                    <div class="as">
                      <span class="as-label t-cm-caption" id="payFromL">Paying from</span>
                      <button class="as-trigger" id="payFrom" role="combobox" aria-haspopup="listbox" aria-expanded="false" aria-controls="payFromMenu" aria-labelledby="payFromL payFrom">
                        <span class="who"><span class="t-cm-label em">Operations</span><span class="mask16 t-cm-legal" aria-label="Current account ending 4417">Current &nbsp;&middot;&middot;&middot;&middot; 4417</span></span>
                        <span class="bal t-cm-figure-5"><span>&pound;</span><span>32,450 GBP</span></span>
                        <span class="chev" aria-hidden="true">{use("aschev")}</span>
                      </button>
                      <ul class="as-menu" id="payFromMenu" role="listbox" aria-labelledby="payFromL" tabindex="-1">
                        <li class="as-opt" role="option" aria-selected="true" data-name="Operations" data-mask="&middot;&middot;&middot;&middot;4417" data-bal="32,450">
                          <span class="who"><span class="t-cm-label em">Operations</span><span class="mask16 t-cm-legal">Current &middot;&middot;&middot;&middot; 4417</span></span>
                          <span class="bal t-cm-figure-6"><span>&pound;</span><span>32,450</span></span></li>
                        <li class="as-opt" role="option" aria-selected="false" data-name="Tax Savings" data-mask="&middot;&middot;&middot;&middot;0041" data-bal="22,825.38">
                          <span class="who"><span class="t-cm-label">Tax Savings</span><span class="mask16 t-cm-legal">Savings &middot;&middot;&middot;&middot; 0041</span></span>
                          <span class="bal t-cm-figure-6"><span>&pound;</span><span>22,825.38</span></span></li>
                      </ul>
                    </div>
                  </div>

                  <div class="cn-amount-input cn-icon-button">
                    <div class="ai-group">
                      <div class="ai-lblrow"><label class="t-cm-label" for="payAmt">Amount</label></div>
                      <div class="ai-box">
                        <input id="payAmt" class="t-cm-figure-5" type="text" inputmode="decimal" value="&pound;1,247.85 GBP" readonly>
                        <button class="iconbtn tertiary" type="button" aria-label="Edit amount">{use("edit")}</button>
                      </div>
                    </div>
                  </div>

                  <div class="cn-dropdown">
                    <div class="dd boxed">
                      <label id="payTypeL" for="payType">Payment type</label>
                      <button class="trigger" id="payType" role="combobox" aria-haspopup="listbox" aria-expanded="false" aria-controls="payTypeMenu" aria-labelledby="payTypeL payType">
                        <span class="ddval">Instant payment &mdash; under 2 minutes via Faster Payments</span>
                        <span class="chev" aria-hidden="true">&#9662;</span>
                      </button>
                      <ul class="menu" id="payTypeMenu" role="listbox" aria-labelledby="payTypeL" tabindex="-1">
                        <li class="opt" role="option" aria-selected="true" tabindex="-1">Instant payment &mdash; under 2 minutes via Faster Payments</li>
                        <li class="opt" role="option" aria-selected="false" tabindex="-1">Standard payment &mdash; next working day</li>
                      </ul>
                    </div>
                  </div>

                  <div class="cn-button nio-actions">
                    <button class="btn tertiary" type="button">Back</button>
                    <span class="nio-actions-r">
                      <button class="btn secondary" type="button">Cancel</button>
                      <button class="btn primary" type="button">Continue</button>
                    </span>
                  </div>
                </div>

              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ============ PREDICTIVE SIGNALS ============ -->
    <section class="tpl-section" aria-labelledby="sig-h">
      <div class="stat-card tpl-panel nio-flush">
        <h2 id="sig-h" class="nio-panel-title t-ed-heading-3">Predictive signals</h2>
        <div class="cn-meter cn-status-indicator cn-links nio-divider">
          <div class="nio-signals">
      {signals}
          </div>
        </div>
      </div>
    </section>

    <!-- ============ YOUR SPENDING ============ -->
    <section class="tpl-section" aria-labelledby="ys-h">
      <div class="stat-card tpl-panel nio-flush">
        <h2 id="ys-h" class="nio-panel-title t-ed-heading-3">Your spending</h2>
        <div class="cn-chart-line cn-segmented-control nio-divider" style="padding:24px">
      {ys_line}
        </div>
        <div class="cn-chart-bar cn-segmented-control nio-divider" style="padding:24px">
      {ys_bars}
        </div>
      </div>
    </section>

    <!-- ============ FEEDBACK ============ -->
    <section class="tpl-section" aria-labelledby="fb-h">
      <div class="stat-card tpl-panel cn-cta-lockup cn-button nio-flush">
        <div class="ctal centered nio-feedback">
          <div class="ctal-titleblock">
            <p class="ctal-support t-ed-body">Your feedback is important to us</p>
            <h2 class="ctal-heading t-ed-heading-3" id="fb-h">Tell us what you think about Nio</h2>
          </div>
          <div class="nio-chips">
            <button class="btn tertiary" type="button">I like something {use("success")}</button>
            <button class="btn tertiary" type="button">I don't like something {use("close")}</button>
            <button class="btn tertiary" type="button">I have a suggestion {use("add")}</button>
          </div>
        </div>
      </div>
    </section>

    <!-- ============ LEARN MORE ============ -->
    <section class="tpl-section" aria-labelledby="lm-h">
      <h2 id="lm-h" class="tpl-section-head t-ed-heading-3">Learn more about Neo</h2>
      <div class="cn-feature-grid-lockup cn-button">
        <div class="fgl-outer">
          <div class="fgl-grid up-4">
          {feats}
          </div>
        </div>
      </div>
    </section>

  </div>
</main>

<!-- ============ FOOTER — Footer (compact / legal band form) ============ -->
<div class="cn-footer">
  <footer class="ft slim" role="contentinfo" aria-label="Legal footer">
    <div class="ft-inner">
      <div class="ft-legal">
        <ul>
          <li><a class="lnk t-cm-legal" href="#">HSBC UK Customer Legal Information</a></li>
          <li><a class="lnk t-cm-legal" href="#">Security</a></li>
          <li><a class="lnk t-cm-legal" href="#">Careers at HSBC</a></li>
          <li><a class="lnk t-cm-legal" href="#">Terms &amp; Conditions of use</a></li>
          <li><a class="lnk t-cm-legal" href="#">Privacy and data protection statement</a></li>
        </ul>
        <p class="copy t-cm-legal">&copy; HSBC Bank plc 2026</p>
      </div>
      <p class="t-cm-legal nio-legal">All rights reserved. No endorsement or approval of any third parties or their advice, opinions, information, products or services is expressed or implied by any information on this Site or by any hyperlinks to or from any third party websites or pages. Your use of this website is subject to the terms and conditions governing it. Please read those terms and conditions before using the website.</p>
    </div>
  </footer>
</div>

</div>

<!-- ============ V2 REVIEW CONTROLLER — page chrome only. It drives the three review
     switches and NOTHING inside any component. Delete it and the page renders at its
     authored defaults: Console light, capsule legend, card list. ============ -->
<script>
(function () {{
  "use strict";
  var root = document.documentElement;

  /* canon's own dv-behaviour re-places every .seg indicator on resize (placeSegs). Reuse it
     rather than re-implementing the atom's maths. */
  function replaceIndicators() {{ window.dispatchEvent(new Event("resize")); }}

  function seg(id, onPick) {{
    var box = document.getElementById(id);
    if (!box) {{ return; }}
    box.addEventListener("click", function (e) {{
      var b = e.target.closest("button[data-v]");
      if (!b || !box.contains(b) || b.getAttribute("aria-pressed") === "true") {{ return; }}
      Array.prototype.forEach.call(box.querySelectorAll("button[data-v]"), function (o) {{
        o.setAttribute("aria-pressed", String(o === b));
      }});
      replaceIndicators();
      onPick(b.getAttribute("data-v"));
    }});
  }}

  /* ④ light / dark — data-theme on <html>, the bento mechanism. */
  seg("rvMode", function (v) {{ root.setAttribute("data-theme", v); }});

  /* ⑤ capsule <-> list legend.
     dv-legend holds ONE state record per host and resolves a figure's legend with
     figure.querySelector('.dv-leg') — the FIRST match. So: reset the OUTGOING legend while it is
     still discoverable, then remove its `dv-leg` class and hide it, so exactly one legend is ever
     findable. Declared on the face of the page: selection does not carry across the switch. */
  var legs = [document.getElementById("sp-legend"), document.getElementById("sp-legend-list")];
  var summary = document.getElementById("spSummary");
  seg("rvLeg", function (v) {{
    legs.forEach(function (el) {{
      if (!el) {{ return; }}
      if (el.getAttribute("data-leg-variant") !== v) {{
        var r = el.querySelector(".dv-leg-reset");
        if (r && !r.disabled) {{ r.click(); }}
      }}
    }});
    legs.forEach(function (el) {{
      if (!el) {{ return; }}
      var on = el.getAttribute("data-leg-variant") === v;
      el.classList.toggle("dv-leg", on);
      el.classList.toggle("nio-leg-off", !on);
      if (on) {{ el.removeAttribute("hidden"); }} else {{ el.setAttribute("hidden", ""); }}
    }});
    /* the separate figures column is v1's answer; the list variant carries the values itself,
       and the panel collapses to one column so the list sits BESIDE the donut rather than under it */
    if (summary) {{ summary.hidden = (v === "list"); }}
    var split = document.querySelector(".nio-donut-split");
    if (split) {{ split.setAttribute("data-nio-leg", v); }}
  }});

  /* ⑥ account list chrome. */
  var acct = document.getElementById("acctList");
  seg("rvList", function (v) {{ if (acct) {{ acct.setAttribute("data-nio-list", v); }} }});
}}());
</script>
<script src="../canon/dv-behaviour.js"></script>
<script src="../canon/dv-legend.js"></script>
<script src="../canon/dv-donut-sweep.js"></script>
</body>
</html>
'''
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"wrote {OUT} ({len(html):,} bytes)")


if __name__ == "__main__":
    build()
