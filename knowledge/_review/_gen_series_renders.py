#!/usr/bin/env python3
"""Generate the V7 series-assignment DECISION SHEET (real renders, light+dark).

Reads tokens/_proposals/supporting-palette.proposals.json, renders three candidate
series assignments (A hue-spread mid-step / B strong-step / C mode-stable) as real
inline-SVG charts (grouped bar, multi-series line, donut, stacked column) on the
REAL surface tokens (background/default: #FFFFFF light, #000000 dark), plus the
gain/loss delta options. Contrast ratios are RECOMPUTED here and cross-checked
against the proposals file's receipts — any mismatch prints a warning.

Usage: python3 knowledge/_review/_gen_series_renders.py   (from repo root)
Output: reviews/DATAVIZ-SERIES-RENDERS-2026-07-16.html  (clean; run _make_review.py after)
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
import json, math, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PAL = json.load(open(os.path.join(ROOT, "knowledge/tokens/_proposals/supporting-palette.proposals.json")))
OUT = os.path.join(ROOT, "reviews/DATAVIZ-SERIES-RENDERS-2026-07-16.html")

# ---------- contrast ----------
def _lin(c):
    c /= 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

def lum(hexs):
    h = hexs.lstrip("#")
    r, g, b = (int(h[i:i+2], 16) for i in (0, 2, 4))
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)

def ratio(fg, bg):
    a, b = lum(fg), lum(bg)
    a, b = max(a, b), min(a, b)
    return (a + 0.05) / (b + 0.05)

WHITE, BLACK = "#FFFFFF", "#000000"

def swatch(family, step):
    node = PAL[family][str(step)]
    hexv = node["$value"]
    st = node["$contrast"]
    cw, cb = ratio(hexv, WHITE), ratio(hexv, BLACK)
    for name, sv, comp in (("onWhite", st["onWhite"], cw), ("onBlack", st["onBlack"], cb)):
        if abs(sv - comp) > 0.15:
            print(f"  ! receipt mismatch {family}/{step} {name}: stated {sv} vs computed {comp:.2f}")
    return {"family": family, "step": step, "hex": hexv, "onWhite": cw, "onBlack": cb,
            "okLight": st["indicatorOK"]["light"], "okDark": st["indicatorOK"]["dark"]}

# ---------- candidates ----------
SERIES_NAMES = ["Current account", "Savings", "Credit card", "Loan", "Investments"]
LETTERS = ["A", "B", "C", "D", "E"]

CANDS = {
  "C": {
    "title": "Candidate C — mode-stable · CHOSEN DEFAULT",
    "status": ("chosen", "DEFAULT — picked in your 2026-07-16 markup"),
    "why": ("One assignment from the dual-legal mid-steps (indicatorOK true in BOTH modes) — the same data "
            "keeps the same colour when the user switches theme, the strongest reading of the KB's "
            "categorisation-consistency rule (dv-014). Your pick resolves the dv-014 scope question toward "
            "cross-mode stability; the muted mid-tone character is accepted as the default register, with "
            "the high-contrast switch (below) covering the legibility ceiling."),
    "light": [("midnight-blue", 5), ("burnt-orange", 4), ("forest-green", 5), ("olive-green", 4), ("rose-pink", 4)],
    "dark":  [("midnight-blue", 5), ("burnt-orange", 4), ("forest-green", 5), ("olive-green", 4), ("rose-pink", 4)],
  },
  "A": {
    "title": "Candidate A — hue-spread, mid-step · HIGH-CONTRAST ALTERNATE",
    "status": ("alt", "ALTERNATE — serves the per-chart high-contrast switch (your markup)"),
    "why": ("Palette-half per mode (col26-017 as written): light mode draws the five DARK families at "
            "step 3, dark mode the five LIGHT families at step 2 — the strongest fill-vs-surface separation "
            "of the three. Proposed mechanic: every chart carries a contrast switch "
            "(data-contrast=\"default|high\"); default binds the C set, high rebinds the SAME "
            "data/series-N tokens to this set. Pure token swap — no chart forks; gate checks both bindings."),
    "light": [("midnight-blue", 3), ("burnt-orange", 3), ("forest-green", 3), ("dusk-purple", 3), ("olive-green", 3)],
    "dark":  [("sky-blue", 2), ("apricot-orange", 2), ("mint-green", 2), ("rose-pink", 2), ("sun-yellow", 2)],
  },
  "B": {
    "title": "Candidate B — strong-step · NOT SELECTED (kept for the record)",
    "status": ("dead", "NOT SELECTED — retained as the receipt of the option considered"),
    "why": ("Same families and order as A but at step 1 — deepest in light, palest in dark. Weakest "
            "series-vs-series separation (hue the only channel). Not picked; may inform the future "
            "designer-selectable ranges exploration."),
    "light": [("midnight-blue", 1), ("burnt-orange", 1), ("forest-green", 1), ("dusk-purple", 1), ("olive-green", 1)],
    "dark":  [("sky-blue", 1), ("apricot-orange", 1), ("mint-green", 1), ("rose-pink", 1), ("sun-yellow", 1)],
  },
}

MODES = {
  "light": {"bg": WHITE, "ink": "#1A1A1A", "grey": "#767676", "grid": "#767676", "name": "Light — background/default #FFFFFF"},
  "dark":  {"bg": BLACK, "ink": "#F5F5F5", "grey": "#808080", "grid": "#808080", "name": "Dark — background/default #000000"},
}

def letter_ink(fill):
    return WHITE if ratio(WHITE, fill) >= ratio("#1A1A1A", fill) else "#1A1A1A"

# ---------- SVG builders (all rules on display: zero baseline, straight lines,
# 2px gaps, flat fills, letters on elements, colour+letter+name legends) ----------

def legend(colors, mode, n=5, y=0):
    m = MODES[mode]
    items = []
    x = 0
    for i in range(n):
        items.append(f'<rect x="{x}" y="{y}" width="10" height="10" fill="{colors[i]["hex"]}"/>'
                     f'<text x="{x+14}" y="{y+9}" font-size="9" fill="{m["ink"]}">{LETTERS[i]} · {SERIES_NAMES[i]}</text>')
        x += 14 + 8 + len(SERIES_NAMES[i]) * 4.6 + 14
    return "".join(items)

def grouped_bar(colors, mode):
    m = MODES[mode]
    vals = [[62, 68, 74], [45, 49, 44], [30, 26, 34], [22, 25, 19], [12, 15, 17]]
    W, H, base, top = 470, 210, 168, 22
    scale = (base - top) / 80.0
    out = [f'<svg viewBox="0 0 {W} {H+34}" role="img" aria-label="Grouped bar chart, five series" xmlns="http://www.w3.org/2000/svg">']
    out.append(f'<text x="0" y="12" font-size="11" font-weight="600" fill="{m["ink"]}">Balances rose through Q2 (£k)</text>')
    for gv in (0, 20, 40, 60, 80):
        y = base - gv * scale
        out.append(f'<line x1="34" y1="{y:.1f}" x2="{W}" y2="{y:.1f}" stroke="{m["grid"]}" stroke-width="{1 if gv else 1.5}" opacity="{0.55 if gv else 1}"/>')
        out.append(f'<text x="28" y="{y+3:.1f}" font-size="8.5" fill="{m["grey"]}" text-anchor="end">{gv}</text>')
    groups = ["Apr", "May", "Jun"]
    gw = (W - 44) / 3.0
    bw, gap = 18, 4  # 4px gap ≥ the 2px minimum (dv-004)
    for g in range(3):
        gx = 44 + g * gw + (gw - (bw * 5 + gap * 4)) / 2
        for s in range(5):
            v = vals[s][g]
            h = v * scale
            x = gx + s * (bw + gap)
            y = base - h
            fill = colors[s]["hex"]
            out.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bw}" height="{h:.1f}" fill="{fill}"/>')
            li = letter_ink(fill)
            out.append(f'<text x="{x+bw/2:.1f}" y="{y+11:.1f}" font-size="8.5" font-weight="600" fill="{li}" text-anchor="middle">{LETTERS[s]}</text>')
        out.append(f'<text x="{gx + (bw*5+gap*4)/2:.1f}" y="{base+14}" font-size="9.5" fill="{m["ink"]}" text-anchor="middle">{groups[g]}</text>')
    out.append(f'<g transform="translate(34,{base+24})">{legend(colors, mode)}</g>')
    out.append("</svg>")
    return "".join(out)

def line_chart(colors, mode):
    m = MODES[mode]
    series = [[30, 38, 36, 48, 55, 62], [52, 47, 50, 42, 40, 38], [18, 22, 26, 24, 30, 34]]
    W, H, base, top = 470, 190, 150, 22
    scale = (base - top) / 70.0
    xs = [44 + i * ((W - 64) / 5.0) for i in range(6)]
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    out = [f'<svg viewBox="0 0 {W} {H+30}" role="img" aria-label="Line chart, three series" xmlns="http://www.w3.org/2000/svg">']
    out.append(f'<text x="0" y="12" font-size="11" font-weight="600" fill="{m["ink"]}">Current account grew; savings dipped (£k)</text>')
    for gv in (0, 35, 70):
        y = base - gv * scale
        out.append(f'<line x1="34" y1="{y:.1f}" x2="{W-10}" y2="{y:.1f}" stroke="{m["grid"]}" stroke-width="{1 if gv else 1.5}" opacity="{0.55 if gv else 1}"/>')
        out.append(f'<text x="28" y="{y+3:.1f}" font-size="8.5" fill="{m["grey"]}" text-anchor="end">{gv}</text>')
    for i, x in enumerate(xs):
        out.append(f'<text x="{x:.1f}" y="{base+13}" font-size="8.5" fill="{m["grey"]}" text-anchor="middle">{months[i]}</text>')
    for s in range(3):
        fill = colors[s]["hex"]
        pts = " ".join(f"{xs[i]:.1f},{base - series[s][i]*scale:.1f}" for i in range(6))
        out.append(f'<polyline points="{pts}" fill="none" stroke="{fill}" stroke-width="2.5"/>')  # straight lines only (dv-line-011)
        for i in range(6):  # different-shaped markers per set (dv-line-002)
            x, y = xs[i], base - series[s][i] * scale
            if s == 0:
                out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.4" fill="{fill}"/>')
            elif s == 1:
                out.append(f'<rect x="{x-3:.1f}" y="{y-3:.1f}" width="6" height="6" fill="{fill}"/>')
            else:
                out.append(f'<path d="M{x:.1f} {y-4:.1f} L{x+4:.1f} {y+3.5:.1f} L{x-4:.1f} {y+3.5:.1f} Z" fill="{fill}"/>')
        ex, ey = xs[-1], base - series[s][-1] * scale
        out.append(f'<text x="{ex+7:.1f}" y="{ey+3:.1f}" font-size="9" font-weight="600" fill="{fill}">{LETTERS[s]}</text>')
    out.append(f'<g transform="translate(34,{base+22})">{legend(colors, mode, n=3)}</g>')
    out.append("</svg>")
    return "".join(out)

def donut(colors, mode):
    m = MODES[mode]
    vals = [34, 26, 18, 14, 8]  # desc, from 12 o'clock (dv-pie-001); 5 ≤ 6-slice cap (dv-pie-009)
    labels = ["Groceries", "Travel", "Bills", "Eating out", "Other"]
    cx, cy, r = 120, 108, 78
    out = [f'<svg viewBox="0 0 470 216" role="img" aria-label="Donut chart, five segments" xmlns="http://www.w3.org/2000/svg">']
    out.append(f'<text x="0" y="12" font-size="11" font-weight="600" fill="{m["ink"]}">Groceries led June spending</text>')
    a0 = -90.0
    total = sum(vals)
    for i, v in enumerate(vals):
        a1 = a0 + v / total * 360.0
        large = 1 if (a1 - a0) > 180 else 0
        x0, y0 = cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0))
        x1, y1 = cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1))
        out.append(f'<path d="M{cx} {cy} L{x0:.1f} {y0:.1f} A{r} {r} 0 {large} 1 {x1:.1f} {y1:.1f} Z" '
                   f'fill="{colors[i]["hex"]}" stroke="{m["bg"]}" stroke-width="2.5"/>')  # ≥2px separation (dv-004)
        mid = math.radians((a0 + a1) / 2)
        lx, ly = cx + (r + 16) * math.cos(mid), cy + (r + 16) * math.sin(mid)
        anch = "start" if math.cos(mid) >= 0 else "end"
        out.append(f'<text x="{lx:.1f}" y="{ly+3:.1f}" font-size="9" fill="{m["ink"]}" text-anchor="{anch}">'
                   f'{LETTERS[i]} · {v}%</text>')  # direct labelling adjacent (dv-pie-002/004)
        a0 = a1
    out.append(f'<circle cx="{cx}" cy="{cy}" r="46" fill="{m["bg"]}"/>')
    out.append(f'<text x="{cx}" y="{cy-2}" font-size="15" font-weight="700" fill="{m["ink"]}" text-anchor="middle">£2,410</text>')
    out.append(f'<text x="{cx}" y="{cy+14}" font-size="9" fill="{m["grey"]}" text-anchor="middle">Total spend · June</text>')  # value + descriptor (dv-pie-003)
    ly = 40
    for i in range(5):
        out.append(f'<rect x="268" y="{ly-9}" width="10" height="10" fill="{colors[i]["hex"]}"/>')
        out.append(f'<text x="286" y="{ly}" font-size="9.5" fill="{m["ink"]}">{LETTERS[i]} · {labels[i]} — {vals[i]}%</text>')
        ly += 20
    out.append(f'<text x="268" y="{ly+2}" font-size="8.5" fill="{m["grey"]}">Values rounded; sum = 100% (dv-pie-010/011)</text>')
    out.append("</svg>")
    return "".join(out)

def stacked(colors, mode):
    m = MODES[mode]
    cols = [[22, 18, 14, 10, 8], [26, 17, 16, 12, 7], [24, 21, 13, 14, 9], [28, 19, 17, 11, 10]]
    months = ["Mar", "Apr", "May", "Jun"]
    W, base, top = 470, 168, 24
    scale = (base - top) / 90.0
    out = [f'<svg viewBox="0 0 {W} 212" role="img" aria-label="Stacked column chart, five segments" xmlns="http://www.w3.org/2000/svg">']
    out.append(f'<text x="0" y="12" font-size="11" font-weight="600" fill="{m["ink"]}">Spending mix, stable across spring (£00)</text>')
    out.append(f'<line x1="34" y1="{base}" x2="{W-10}" y2="{base}" stroke="{m["grid"]}" stroke-width="1.5"/>')  # zero baseline (dv-bar-009)
    cw = 46
    for c in range(4):
        x = 60 + c * 100
        y = base
        for s in range(5):
            h = cols[c][s] * scale
            y -= h
            fill = colors[s]["hex"]
            out.append(f'<rect x="{x}" y="{y:.1f}" width="{cw}" height="{max(h-2.5,1):.1f}" fill="{fill}"/>')  # 2.5px gap (dv-004)
            if h > 13:
                li = letter_ink(fill)
                out.append(f'<text x="{x+cw/2}" y="{y+h/2+3:.1f}" font-size="8.5" font-weight="600" fill="{li}" text-anchor="middle">{LETTERS[s]}</text>')
        out.append(f'<text x="{x+cw/2}" y="{base-sum(cols[c])*scale-6:.1f}" font-size="9" fill="{m["ink"]}" text-anchor="middle">{sum(cols[c])}</text>')
        out.append(f'<text x="{x+cw/2}" y="{base+14}" font-size="9.5" fill="{m["ink"]}" text-anchor="middle">{months[c]}</text>')
    out.append(f'<g transform="translate(34,{base+26})">{legend(colors, mode)}</g>')
    out.append("</svg>")
    return "".join(out)

# ---------- delta (gain/loss/neutral/warning) — DERIVED sets, per Dave's markup ----------
# "Steal the most red and most green hue from the palette and adjust" + blue neutral + amber.
# Anchors: burnt-orange/1 #7D1F0F (reddest hue in the palette), forest-green/1 #1A4225,
# midnight-blue/1 #1B345D, sun-yellow/3 #D8AE74. Derivation: keep the anchor's hue lineage,
# blend toward the semantic target hue, set saturation, then solve LIGHTNESS so the value hits
# the target contrast vs the real surface token (binary search).

def _hex_to_hsl(hexs):
    h = hexs.lstrip("#")
    r, g, b = (int(h[i:i+2], 16) / 255.0 for i in (0, 2, 4))
    mx, mn = max(r, g, b), min(r, g, b)
    l = (mx + mn) / 2
    if mx == mn:
        return 0.0, 0.0, l
    d = mx - mn
    s = d / (2 - mx - mn) if l > 0.5 else d / (mx + mn)
    if mx == r:
        hdeg = ((g - b) / d + (6 if g < b else 0)) * 60
    elif mx == g:
        hdeg = ((b - r) / d + 2) * 60
    else:
        hdeg = ((r - g) / d + 4) * 60
    return hdeg % 360, s, l

def _hsl_to_hex(hdeg, s, l):
    c = (1 - abs(2 * l - 1)) * s
    x = c * (1 - abs((hdeg / 60) % 2 - 1))
    m = l - c / 2
    r, g, b = {0: (c, x, 0), 1: (x, c, 0), 2: (0, c, x), 3: (0, x, c), 4: (x, 0, c), 5: (c, 0, x)}[int(hdeg // 60) % 6]
    return "#%02X%02X%02X" % tuple(round((v + m) * 255) for v in (r, g, b))

def _blend_hue(a, b, t):
    d = ((b - a + 180) % 360) - 180
    return (a + d * t) % 360

def derive(anchor_hex, target_hue, hue_pull, sat, bg, target_ratio):
    """Adjusted colour: anchor hue pulled toward target, given saturation, lightness solved for contrast."""
    h0, _, _ = _hex_to_hsl(anchor_hex)
    hue = _blend_hue(h0, target_hue, hue_pull)
    lo, hi = (0.02, 0.62) if bg == WHITE else (0.30, 0.95)  # dark-on-light vs light-on-dark
    best = None
    for _ in range(28):
        mid = (lo + hi) / 2
        cand = _hsl_to_hex(hue, sat, mid)
        r = ratio(cand, bg)
        if r >= target_ratio:
            best = cand
            if bg == WHITE: lo = mid   # lighten toward the threshold
            else: hi = mid             # darken toward the threshold
        else:
            if bg == WHITE: hi = mid
            else: lo = mid
    return best or _hsl_to_hex(hue, sat, (0.32 if bg == WHITE else 0.72))

ANCHORS = {"loss": "#7D1F0F", "gain": "#1A4225", "neutral": "#1B345D", "warning": "#D8AE74"}
TARGET_HUES = {"loss": 6, "gain": 152, "neutral": 214, "warning": 38}

# ---------- vibrating-boundary risk (Dave 2026-07-16, from the Tuts+ "Vibrating boundaries" article) ----------
# The shimmer needs ALL THREE legs: near-equal VALUE + near-complementary HUES + both SATURATED.
# It is an accessibility hazard (astigmatism, sensory processing; and equal-value pairs vanish for CVD).
# Thresholds are advisory-first and tunable at the gate: value-ratio <1.25 · hue-sep ≥135° · min sat ≥0.5.
# (Hue leg set at 135° not 150°: Dave OBSERVED the dance on the D2 dark red/green pair, which sits at 146°.)

def _hs(hexs):
    h, s, _ = _hex_to_hsl(hexs)
    return h, s

def _hue_sep(a, b):
    ha, hb = _hs(a)[0], _hs(b)[0]
    d = abs(ha - hb) % 360
    return min(d, 360 - d)

def vibration(a, b):
    lr = ratio(a, b)
    hs = _hue_sep(a, b)
    smin = min(_hs(a)[1], _hs(b)[1])
    legs = sum([lr < 1.25, hs >= 135, smin >= 0.5])
    level = "HIGH" if legs == 3 else ("moderate" if legs == 2 else "low")
    return {"lum_ratio": lr, "hue_sep": hs, "sat_min": smin, "level": level}

def vibration_receipt_html(colors, label="adjacent series pairs"):
    """colors = list of hex; checks each adjacent pair, reports the worst + per-pair detail."""
    pairs = [(i, vibration(colors[i], colors[i + 1])) for i in range(len(colors) - 1)]
    worst = max(pairs, key=lambda p: {"low": 0, "moderate": 1, "HIGH": 2}[p[1]["level"]])[1]["level"]
    cls = {"low": "ok", "moderate": "", "HIGH": "no"}[worst]
    detail = " · ".join(f'{i+1}↔{i+2}: {v["lum_ratio"]:.2f}:1, {v["hue_sep"]:.0f}°, sat {v["sat_min"]:.2f} → {v["level"]}'
                        for i, v in pairs)
    return (f'<p class="striplabel">Vibration receipts ({label}): worst = '
            f'<span class="{cls}"><b>{worst}</b></span> — {detail}. '
            f'<small>Legs: value-ratio &lt;1.25 + hue-sep ≥135° + sat ≥0.5 — all three = shimmer risk.</small></p>')

def vibration_worst(colors):
    levels = [vibration(colors[i], colors[i + 1])["level"] for i in range(len(colors) - 1)]
    return max(levels, key=lambda l: {"low": 0, "moderate": 1, "HIGH": 2}[l])

# Delta options: (slug, name, status, note, hue_pull, sat, ratios per role as (light, dark) targets,
# per-role DARK saturation overrides). Amber runs at graphic-grade 3:1 on WHITE (col26-018; true amber
# can't reach 4.5 there without going tobacco) but is solved LUMINOUS on black.
# REV 3 (Dave's markup 2026-07-16): D2 PICKED — but the dark red/green pair "danced" (vibrating-boundary
# triple: equal value + 146° hue sep + sat .72). Fix: value-SPLIT the dark pair (gain brighter 6.2:1,
# loss 4.4:1) + desaturate dark red to .60 — the pair keeps convention but stops shimmering.
# D1 kept as an option (Dave). D3 retired to the record — its value-split mechanism is absorbed into D2-dark.
DELTA_OPTS = [
  ("d2", "D2 — convention-forward · PICKED (both pairs value-split)", "chosen",
   "Hue pulled hard to the finance convention (red down / green up); text-grade 4.5:1 (amber 3:1 light). "
   "Your note — dark red/green 'dance a little' — was the vibrating-boundary triple; and the receipts caught "
   "the SAME triple in light mode. Fix applied to both: value-split the pair (light: loss deepened to 6.0:1; "
   "dark: gain brightened to 6.2:1, loss 4.4:1) and calm dark red's saturation. Receipts below show both "
   "pairs out of the HIGH zone.",
   0.85, 0.72, {"loss": (6.0, 4.4), "gain": (4.6, 6.2), "neutral": (4.6, 4.6), "warning": (3.05, 6.5)},
   {"loss": 0.60}),
  ("d1", "D1 — adjusted, quiet · KEPT AS AN OPTION (same split applied)", "alt",
   "Closest to the palette's muted character; hue pulled halfway to convention. Kept per your markup — but the "
   "vibration receipts flagged its equal-value pair too (HSL saturation .55 still clears the .5 leg), so it "
   "carries the same value-split as D2 for consistency.",
   0.5, 0.55, {"loss": (6.0, 4.4), "gain": (4.6, 6.2), "neutral": (4.6, 4.6), "warning": (3.05, 6.5)},
   {}),
  ("d3", "D3 — CVD-split · RETIRED TO THE RECORD", "dead",
   "The deliberate red/green lightness split. Not picked as a set — but its mechanism IS the fix now living "
   "inside D2's dark mode, so it survives as method rather than as tokens.",
   0.85, 0.72, {"loss": (6.4, 7.5), "gain": (4.6, 4.6), "neutral": (4.6, 4.6), "warning": (3.05, 6.5)},
   {}),
]

def derive_set(hue_pull, sat, ratios, dark_sat=None):
    dark_sat = dark_sat or {}
    out = {}
    for role in ("gain", "loss", "neutral", "warning"):
        rl, rd = ratios[role]
        out[role] = {
            "light": derive(ANCHORS[role], TARGET_HUES[role], hue_pull, sat, WHITE, rl),
            "dark":  derive(ANCHORS[role], TARGET_HUES[role], hue_pull, dark_sat.get(role, sat), BLACK, rd),
        }
    return out

def delta_chips(mode, dset):
    m = MODES[mode]
    def chip(x, col, arrow, txt, note):
        return (f'<g transform="translate({x},0)">'
                f'<text x="0" y="16" font-size="14" font-weight="700" fill="{col}">{arrow} {txt}</text>'
                f'<text x="0" y="31" font-size="8" fill="{m["grey"]}">{note} · {ratio(col, m["bg"]):.2f}:1</text>'
                f'<text x="0" y="43" font-size="8" fill="{m["grey"]}"><tspan font-family="monospace">{col}</tspan></text></g>')
    g, l = dset["gain"][mode], dset["loss"][mode]
    n, w = dset["neutral"][mode], dset["warning"][mode]
    rg = ratio(g, l)
    bars = "".join(
        f'<rect x="{330+i*26}" y="{56-v if v>0 else 56}" width="20" height="{abs(v)}" fill="{g if v>0 else l}"/>'
        for i, v in enumerate((22, 34, -16, 28, -24)))
    return (f'<svg viewBox="0 0 470 92" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Delta indicator set">'
            + chip(0, g, "▲", "+2.4%", "gain") + chip(84, l, "▼", "−1.2%", "loss")
            + chip(168, n, "→", "0.0%", "neutral") + chip(248, w, "◆", "92%", "warning · 3:1 graphic")
            + bars
            + f'<line x1="330" y1="56" x2="458" y2="56" stroke="{m["grid"]}" stroke-width="1.2"/>'
            + f'<text x="330" y="88" font-size="8" fill="{m["grey"]}">diverging bars · gain↔loss {rg:.2f}:1 apart</text>'
            + f'<text x="0" y="66" font-size="8.5" fill="{m["ink"]}">sign + arrow always accompany colour (dv-011)</text>'
            + f'<text x="0" y="80" font-size="8" fill="{m["grey"]}">values at small sizes take text tokens; the arrow carries the hue</text></svg>')

# ---------- receipts table ----------
def receipts(colors, mode):
    m = MODES[mode]
    ok_key = "okLight" if mode == "light" else "okDark"
    r_key = "onWhite" if mode == "light" else "onBlack"
    rows = []
    for i, c in enumerate(colors):
        ok = c[ok_key]
        badge = ('<span class="ok">indicatorOK ✓</span>' if ok else '<span class="no">indicatorOK ✗</span>')
        li = letter_ink(c["hex"])
        lr = ratio(li, c["hex"])
        rows.append(f'<tr><td><span class="chip" style="background:{c["hex"]}"></span>series-{i+1} · {LETTERS[i]}</td>'
                    f'<td><code>{c["family"]}/{c["step"]}</code></td><td><code>{c["hex"]}</code></td>'
                    f'<td>{c[r_key]:.2f}:1</td><td>{badge}</td><td>{lr:.2f}:1</td></tr>')
    return (f'<table><thead><tr><th>Series</th><th>Token</th><th>Hex</th><th>vs {m["bg"]}</th>'
            f'<th>Receipt</th><th>letter-on-fill</th></tr></thead><tbody>{"".join(rows)}</tbody></table>')

# ---------- page ----------
def panel(mode, colors):
    m = MODES[mode]
    cls = "panel light" if mode == "light" else "panel dark"
    return (f'<div class="{cls}"><p class="pmode">{m["name"]}</p>'
            + grouped_bar(colors, mode) + line_chart(colors, mode) + donut(colors, mode) + stacked(colors, mode)
            + "</div>")

def candidate_section(idx, key):
    c = CANDS[key]
    lights = [swatch(f, s) for f, s in c["light"]]
    darks = [swatch(f, s) for f, s in c["dark"]]
    kind, label = c["status"]
    band = f'<p class="status {kind}">{label}</p>'
    extra = ""
    if key == "C":
        extra = ('<div class="tension"><span class="lbl">Rule notes recorded with this pick</span>'
                 '(1) dv-014 scope: your C pick reads categorisation-consistency ACROSS the theme switch, '
                 'not just within a mode — recorded as the working interpretation. '
                 '(2) col26-017 (dark-on-light / light-on-dark halves): C\'s dual-legal mid-steps sit outside its '
                 'letter; recorded as a conscious divergence, receipted by the per-swatch indicatorOK ✓✓ below. '
                 'Both provisional until you confirm the wording.</div>')
    if key == "B":
        return (f'<h2 id="cand-{key.lower()}"><span class="n">0{idx}</span>{c["title"]}</h2>{band}'
                f'<p class="sub">{c["why"]}</p>'
                f'<h3>Receipts (kept for the record)</h3>{receipts([swatch(f, s) for f, s in c["light"]], "light")}')
    return (f'<h2 id="cand-{key.lower()}"><span class="n">0{idx}</span>{c["title"]}</h2>{band}'
            f'<p class="sub">{c["why"]}</p>{extra}'
            f'<h3>Light-mode receipts</h3>{receipts(lights, "light")}'
            f'{vibration_receipt_html([s["hex"] for s in lights], "light, adjacent series")}'
            f'<h3>Dark-mode receipts</h3>{receipts(darks, "dark")}'
            f'{vibration_receipt_html([s["hex"] for s in darks], "dark, adjacent series")}'
            f'<div class="pair">{panel("light", lights)}{panel("dark", darks)}</div>')

def delta_section():
    blocks = []
    for slug, name, status, note, hue_pull, sat, ratios, dark_sat in DELTA_OPTS:
        dset = derive_set(hue_pull, sat, ratios, dark_sat)
        rows = []
        for role in ("gain", "loss", "neutral", "warning"):
            lh, dh = dset[role]["light"], dset[role]["dark"]
            rows.append(f'<tr><td>{role}</td>'
                        f'<td><span class="chip" style="background:{lh}"></span><code>{lh}</code> · {ratio(lh, WHITE):.2f}:1</td>'
                        f'<td><span class="chip" style="background:{dh}"></span><code>{dh}</code> · {ratio(dh, BLACK):.2f}:1</td>'
                        f'<td><code>{ANCHORS[role]}</code></td></tr>')
        table = ('<table><thead><tr><th>Role</th><th>Light (vs #FFFFFF)</th><th>Dark (vs #000000)</th>'
                 '<th>Palette anchor</th></tr></thead><tbody>' + "".join(rows) + '</tbody></table>')
        vib = (vibration_receipt_html([dset["gain"]["light"], dset["loss"]["light"]], "gain↔loss, light")
               + vibration_receipt_html([dset["gain"]["dark"], dset["loss"]["dark"]], "gain↔loss, dark"))
        band = f'<p class="status {status}">{ {"chosen": "CONFIRMED 2026-07-16 — promoted to semantic-colour.json data/delta-*", "alt": "KEPT AS AN OPTION — your markup", "dead": "RETIRED TO THE RECORD"}[status] }</p>'
        blocks.append(f'<h3>{name}</h3>{band}<p>{note}</p>{table}{vib}'
                      f'<div class="pair"><div class="panel light"><p class="pmode">Light</p>{delta_chips("light", dset)}</div>'
                      f'<div class="panel dark"><p class="pmode">Dark</p>{delta_chips("dark", dset)}</div></div>')
    return f'''
<h2 id="delta"><span class="n">05</span>Delta colours — D2 picked, pairs value-split (rev 3)</h2>
<p class="sub">Derived from palette anchors (most-red burnt-orange, most-green forest-green, blue neutral,
amber), per your earlier markup — the one place invented values are allowed ("only safe in the RAG"): these are
RAG-class semantics, never series fills. <b>Rev 3:</b> you picked <b>D2</b> but saw the dark red/green
"dance a little" — that is the vibrating-boundary effect from the article (the pair sat at equal value, 146°
hue separation, saturation .72: all three legs). Fixed by value-splitting the dark pair and calming dark red;
receipts under each option now show the vibration legs explicitly. D1 kept as an option per your markup;
D3 retired (its mechanism became the D2 fix). Red/green/blue run text-grade 4.5:1; amber 3:1 in light
(col26-018; luminous on black).</p>
<div class="tension"><span class="lbl">Same override, new scope</span>
These are NEW semantic tokens (proposal: <code>data/delta-gain · delta-loss · delta-neutral · delta-warning</code>),
not the RAG set and not HSBC Red — but a true red inside a chart still needs the conscious, scoped exception to
col26-012 / the red-once-per-screen rule recorded (deltas = data semantics, not actions). Scope stands:
<b>delta indicators only — never series fills.</b></div>
{''.join(blocks)}
<h3>Retired from this sheet</h3>
<p><small>Rev 1 offered rag/success+rag/error reuse (Option 1) and raw supporting-palette pairs (Option 2);
both retired by your markup — kept in git history as the receipt.</small></p>'''

# ---------- suggestion ranges (Dave: create ranges, categorise by intent; REV 3: palette-native only) ----------
def _strip(hexes, mode):
    bg = MODES[mode]["bg"]
    cells = []
    for hx in hexes:
        ink = letter_ink(hx)
        cells.append(f'<div style="background:{hx}"><span style="color:{ink}">{hx[1:]}<br>{ratio(hx, bg):.1f}:1</span></div>')
    return f'<div class="strip">{"".join(cells)}</div>'

def collect_ranges():
    """Suggestion ranges as data — feeds BOTH the HTML section and the tokens emit.
    REV 3 (Dave's markup): NO invented colours for series/ranges — 'only safe in the RAG' (deltas).
    Every swatch below is an EXISTING palette primitive, selected by a harmony/contrast rule.
    'Wider range' (Dave, ×3): each range now spans the family step-ramps 1→5, so adjacent picks are
    value-stepped — which simultaneously delivers the wider spread AND defeats vibrating boundaries."""
    specs = [
      ("analogous-midnight", "harmony", "Analogous — midnight",
       "the cool neighbours (blue · violet · teal-green) fanned across steps 1→5; calmest multi-series read, now full-width",
       [("midnight-blue", 1), ("dusk-purple", 2), ("forest-green", 3), ("midnight-blue", 4), ("dusk-purple", 5)],
       [("sky-blue", 1), ("mint-green", 2), ("sky-blue", 3), ("mint-green", 4), ("sky-blue", 5)]),
      ("split-complementary-ember", "harmony", "Split-complementary — ember",
       "burnt-orange against its cool flankers, stepped 1→5; warm/cool tension without a hard clash, wider spread",
       [("burnt-orange", 1), ("forest-green", 2), ("midnight-blue", 3), ("burnt-orange", 4), ("dusk-purple", 5)],
       [("apricot-orange", 1), ("mint-green", 2), ("sky-blue", 3), ("apricot-orange", 4), ("rose-pink", 5)]),
      ("triadic-forest", "harmony", "Triadic — forest",
       "green · violet · orange triangle walked down the steps 1→5; the most colourful harmony that still isn't a rainbow, widened",
       [("forest-green", 1), ("dusk-purple", 2), ("burnt-orange", 3), ("forest-green", 4), ("dusk-purple", 5)],
       [("mint-green", 1), ("rose-pink", 2), ("sun-yellow", 3), ("apricot-orange", 4), ("mint-green", 5)]),
      ("sequential-midnight", "contrast", "Sequential ramp — midnight/sky",
       "one family's OWN step ramp (midnight-blue 1→5 light · sky-blue 1→5 dark) — the palette already ships the value ramp; for ordered/quantitative series",
       [("midnight-blue", 1), ("midnight-blue", 2), ("midnight-blue", 3), ("midnight-blue", 4), ("midnight-blue", 5)],
       [("sky-blue", 1), ("sky-blue", 2), ("sky-blue", 3), ("sky-blue", 4), ("sky-blue", 5)]),
    ]
    out = []
    for slug, intent, name, desc, lsteps, dsteps in specs:
        light = [PAL[f][str(s)]["$value"] for f, s in lsteps]
        dark = [PAL[f][str(s)]["$value"] for f, s in dsteps]
        # legality guard: every pick must be indicatorOK in its mode
        for (f, s), hx in zip(lsteps, light):
            assert PAL[f][str(s)]["$contrast"]["indicatorOK"]["light"], f"{f}/{s} not light-legal"
        for (f, s), hx in zip(dsteps, dark):
            assert PAL[f][str(s)]["$contrast"]["indicatorOK"]["dark"], f"{f}/{s} not dark-legal"
        out.append({"slug": slug, "intent": intent, "name": name, "desc": desc,
                    "light": light, "dark": dark,
                    "light_tokens": [f"color/supporting/{f}/{s}" for f, s in lsteps],
                    "dark_tokens": [f"color/supporting/{f}/{s}" for f, s in dsteps]})
    return out

def ranges_section():
    ranges = collect_ranges()
    harmony = [r for r in ranges if r["intent"] == "harmony"]
    contrast = [r for r in ranges if r["intent"] == "contrast"]
    out = [f'''
<h2 id="ranges"><span class="n">06</span>Suggestion ranges — palette-native, widened (rev 3)</h2>
<p class="sub">Your rulings folded in: <b>(1) no invented colours</b> — "we can't invent anything; only safe in
the RAG": every swatch below is now an EXISTING supporting-palette primitive, selected by the harmony/contrast
rule rather than derived (the §05 deltas remain the sole derived-colour zone, as RAG-class semantics);
<b>(2) wider ranges</b> — each range now walks the family step-ramps 1→5, so it spans the palette's full value
range; that same stepping is what defeats vibrating boundaries (see the receipts under every strip);
<b>(3) the CVD diverging range is RETIRED</b> — right idea, too hard to implement; the guideline rules we
already carry (letters, marker shapes, direct labels, ≥2px gaps, zero-baseline position) are the mitigation.
Status: <b>SUGGESTIONS — ungoverned until promoted.</b> KB hooks: complementary pairs (col26-019), the step
structure of the palette itself, and the legacy <code>color/data-vis/*</code> ranges.</p>
<h3>Intent: harmony-led</h3>''']
    def block(r):
        return (f'<p style="margin-top:16px"><b>{r["name"]}</b> <code>range/{r["slug"]}</code></p>'
                f'<p class="striplabel">{r["desc"]}</p>'
                f'{_strip(r["light"], "light")}<p class="striplabel">light · vs #FFFFFF</p>'
                f'{vibration_receipt_html(r["light"], "light, adjacent picks")}'
                f'<div style="background:#000;padding:8px;border-radius:4px">{_strip(r["dark"], "dark")}</div>'
                f'<p class="striplabel">dark · vs #000000</p>'
                f'{vibration_receipt_html(r["dark"], "dark, adjacent picks")}')
    out.extend(block(r) for r in harmony)
    out.append('<h3>Intent: contrast-led</h3>')
    out.extend(block(r) for r in contrast)
    out.append('''<p style="margin-top:16px"><b>CVD-safe diverging — blue↔amber · RETIRED</b></p>
<p class="striplabel">Your markup: "I like this idea but it's too hard to implement; the other rules in the
dataviz guidelines are there to mitigate this issue." Retired from the catalog — the mitigation lives in the
rules the kit already enforces (letters on elements, marker shapes, direct labels, ≥2px separation, position
against a zero baseline). Kept here as the record.</p>''')
    out.append('''<div class="tension"><span class="lbl">Where ranges live — your edit-mode note, enacted</span>
Ranges are TOKENS, not chart code: every range is a named value-set for the same stable slots
(<code>data/series-1…5</code>), emitted by this generator into
<code>tokens/_proposals/dataviz-ranges.proposals.json</code> — the holding pen, same pattern as V7.
<code>range/default</code> = your C pick · <code>range/high-contrast</code> = A · the suggestions above ride
along tagged by intent, status <code>proposed</code>, every value a palette primitive with its token path. A chart selects a range the way it selects a theme
(<code>data-range="…"</code> — the contrast switch is just the first two values of this axis), which is exactly
the hook the future edit-mode harness needs: range-picking becomes an edit-mode dial over token modes, the gate
re-checks receipts per range, and promotion into <code>semantic-colour.json</code> stays your call.</div>
<p><small>Category ideas beyond these two, for the future catalog: perceptually-uniform spacing
(OKLCH steps), semantic ranges (sequential / diverging / categorical as intents of their own), register-tied
ranges (sober→expressive). Each range carries the same receipts and an intent tag; designers choose a range,
the gate checks the receipts.</small></p>''')
    return "".join(out)

HEAD = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Apollo · DataViz — V7 series assignment (decision sheet)</title>
<style>
  :root{--ink:#1a1a1a;--ink2:#5c5c5c;--ink3:#8a8a8a;--line:#e4e4e4;--line2:#d0d0d0;--page:#fff;--surf:#f6f6f6;
    --acc:#a8000b;--ok:#00847f;--info:#305a85;
    --font:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
    --mono:"SF Mono",ui-monospace,Menlo,Consolas,monospace;}
  *{box-sizing:border-box;}
  body{margin:0;background:var(--surf);color:var(--ink);font:400 16px/1.6 var(--font);-webkit-font-smoothing:antialiased;}
  .wrap{max-width:1060px;margin:0 auto;background:var(--page);padding:56px clamp(20px,5vw,64px);}
  header.head{border-bottom:2px solid var(--ink);padding-bottom:24px;margin-bottom:8px;}
  .eyebrow{font:600 12px/1 var(--font);letter-spacing:.12em;text-transform:uppercase;color:var(--ink2);margin:0 0 12px;}
  h1{font:700 34px/1.15 var(--font);margin:0 0 10px;letter-spacing:-.01em;}
  .lede{font-size:17px;color:var(--ink2);margin:0;max-width:70ch;}
  .meta{font:400 13px/1.5 var(--font);color:var(--ink3);margin-top:16px;}
  h2{font:700 24px/1.2 var(--font);margin:52px 0 4px;padding-top:20px;border-top:1px solid var(--line);}
  h2 .n{color:var(--ink3);font-weight:400;margin-right:.5ch;}
  h3{font:700 16px/1.3 var(--font);margin:24px 0 6px;}
  p{margin:8px 0;} .sub{color:var(--ink2);margin:2px 0 14px;max-width:78ch;}
  code{font:500 12.5px/1.4 var(--mono);background:var(--surf);border:1px solid var(--line);border-radius:3px;padding:1px 5px;}
  table{border-collapse:collapse;width:100%;margin:10px 0 18px;font-size:12.5px;}
  th,td{border:1px solid var(--line);padding:6px 9px;text-align:left;vertical-align:middle;}
  th{background:var(--surf);font-weight:600;}
  .chip{display:inline-block;width:14px;height:14px;border-radius:2px;vertical-align:-2px;margin-right:8px;border:1px solid var(--line2);}
  .ok{color:var(--ok);font-weight:600;} .no{color:var(--acc);font-weight:600;}
  .pair{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin:16px 0 8px;}
  .panel{border:1px solid var(--line2);border-radius:6px;padding:18px;}
  .panel.light{background:#fff;} .panel.dark{background:#000;}
  .panel svg{display:block;width:100%;height:auto;margin:14px 0;}
  .pmode{font:600 11px/1 var(--font);letter-spacing:.1em;text-transform:uppercase;margin:0 0 4px;}
  .panel.light .pmode{color:#5c5c5c;} .panel.dark .pmode{color:#9a9a9a;}
  .ask{border:1px solid var(--info);border-left:4px solid var(--info);background:#f3f7fb;padding:16px 20px;margin:20px 0;border-radius:0 6px 6px 0;}
  .ask .lbl{font:700 11px/1 var(--font);letter-spacing:.1em;text-transform:uppercase;color:var(--info);display:block;margin-bottom:6px;}
  .status{font:700 12px/1.3 var(--font);letter-spacing:.06em;text-transform:uppercase;margin:6px 0 2px;padding:6px 10px;border-radius:3px;display:inline-block;}
  .status.chosen{background:#e5f2f2;color:#00504c;border:1px solid #00847f;}
  .status.alt{background:#ebeff4;color:#1d3d5c;border:1px solid #305a85;}
  .status.dead{background:#f1f1f1;color:#6d6d6d;border:1px solid #d0d0d0;}
  .strip{display:flex;gap:4px;margin:6px 0 2px;} .strip div{flex:1;height:44px;border-radius:3px;position:relative;}
  .strip div span{position:absolute;left:4px;bottom:3px;font:600 8.5px/1 var(--mono);}
  .striplabel{font-size:12px;color:var(--ink3);margin:0 0 10px;}
  .tension{border:1px solid var(--acc);border-left:4px solid var(--acc);background:#fffafa;padding:14px 18px;margin:14px 0;font-size:14.5px;border-radius:0 6px 6px 0;}
  .tension .lbl{font:700 11px/1 var(--font);letter-spacing:.1em;text-transform:uppercase;color:var(--acc);display:block;margin-bottom:6px;}
  ul{margin:8px 0;padding-left:22px;} li{margin:4px 0;}
  @media(max-width:880px){.pair{grid-template-columns:1fr;}}
</style>
</head>
<body>
<div class="wrap">
<header class="head">
  <p class="eyebrow">Apollo · DataViz · V7 — series assignment</p>
  <h1>Series colours — the decision sheet</h1>
  <p class="lede">V7 has waited since 2026-07-02 for "proper renders" — here they are. Three candidate
  assignments of the supporting palette to <code>data/series-1…5</code>, rendered as real charts on the real
  surface tokens (<code>background/default</code>: #FFFFFF light · #000000 dark), with contrast receipts
  recomputed from the hex values (not trusted from the proposals file). Pick one (or mark up a mix) — on
  sign-off the assignment enters <code>semantic-colour.json</code> and the gates bind to it.</p>
  <p class="meta">Generated by <code>knowledge/_review/_gen_series_renders.py</code> from
  <code>tokens/_proposals/supporting-palette.proposals.json</code>. <b>REV 3, 2026-07-16 — second markup batch +
  the vibrating-boundaries article enacted:</b> D2 picked with the dark-pair fix, D1 kept, D3 retired; ranges
  rebuilt palette-native and widened across step-ramps; CVD-diverging retired; vibration receipts everywhere.
  Status: <b>CONFIRMED + ENACTED 2026-07-16 — data/series-* · data/series-high-contrast/* · data/delta-* live in
  semantic-colour.json; override dv-019 recorded; suggestion ranges stay proposed in the holding pen</b>.
  Revs 1–2 in git history.</p>
</header>

<div class="ask"><span class="lbl">Outcome — CONFIRMED by Dave 2026-07-16 ("happy with my initial selection with your adjustments") and ENACTED: series + high-contrast + delta tokens now LIVE in semantic-colour.json; override recorded in the guideline (dv-019)</span>
<b>RULED (recorded, confirm the readback):</b> <b>C = the DEFAULT</b> series assignment · <b>A = the
high-contrast ALTERNATE</b> (per-chart <code>data-contrast</code>/<code>data-range</code> token rebind) ·
B kept for the record · <b>D2 = the delta pick</b>, with its dark red/green pair FIXED for the "dance" you saw
(value-split + calmer red — the vibrating-boundary effect from the article you sent) · <b>D1 kept as an
option</b> · D3 retired (its mechanism became the D2 fix) · <b>ranges are palette-native only</b> ("we can't
invent anything — only safe in the RAG"): all suggestion ranges rebuilt from existing palette steps, WIDENED
across the 1→5 step-ramps as asked · CVD-diverging range retired (existing guideline rules are the mitigation).
<br><b>NEW RULE (from your article):</b> avoid vibrating boundaries — adjacent saturated near-complementary
equal-value pairs. Now a constraint-map entry, vibration receipts on every candidate/delta/range below, and an
advisory gate check for <code>_validate_dataviz.py</code>.
<br><b>Remaining asks:</b> 1 · confirm this readback. 2 · promote-or-park the §06 ranges. 3 · confirm the
vibration thresholds (1.25 · 135° · 0.5) as the gate's advisory starting point.</div>

<h2 id="constraints"><span class="n">01</span>The constraint map</h2>
<ul>
  <li><b>col26-017</b> — dark colours on light backgrounds, light on dark. The 10 families split cleanly:
  midnight-blue · forest-green · olive-green · burnt-orange · dusk-purple are the LIGHT-mode half;
  rose-pink · sky-blue · mint-green · sun-yellow · apricot-orange the DARK-mode half. (olive-green is the
  one family dual-legal at every step.)</li>
  <li><b>col26-011 / dv-016</b> — every chart colour ≥3:1 vs its background; the per-step
  <code>indicatorOK</code> receipts encode exactly this and are shown per swatch below.</li>
  <li><b>dv-018 / dv-014</b> — different colour per series; same data = same colour across the journey
  (scope resolved by your C pick: consistency holds ACROSS the theme switch — see 02).</li>
  <li><b>Palette guidance</b> — "don't create rainbow-like colour treatments": five anchored hues per mode,
  cycled in a fixed order, rather than ten hues at once.</li>
  <li><b>Dave's legend ruling</b> — every legend below is colour + LETTER + name; letters repeat on the
  elements themselves (the colour-independent channel).</li>
  <li><b>Vibrating boundaries (NEW — Dave 2026-07-16, from the Tuts+ article)</b> — adjacent SATURATED,
  near-COMPLEMENTARY colours at near-EQUAL VALUE shimmer at the boundary: an accessibility hazard (astigmatism,
  sensory processing; equal-value pairs also vanish for CVD). All three legs together = risk; any leg broken =
  calm. Every candidate, delta pair and range below now carries vibration receipts (value-ratio ≥1.25 · hue-sep
  &lt;135° · saturation &lt;0.5 — one leg broken is enough). Structural defence in charts: the dv-004 ≥2px
  surface-coloured gap is precisely the neutral boundary that kills the effect; the receipts protect legends,
  adjacent text and gapless edges. Goes to the gate as an advisory check in <code>_validate_dataviz.py</code>.</li>
</ul>
'''

FOOT = '''
<h2 id="next"><span class="n">07</span>On confirmation
</h2>
<ul>
  <li><b>C (default)</b> lands as <code>data/series-1…5</code> in <code>semantic-colour.json</code> — same value
  both modes; <b>A</b> lands as the <code>high-contrast</code> binding of the same tokens, switched per chart via
  <code>data-contrast</code>. The proposals file's semantic side retires to receipts.</li>
  <li><b>D2 (picked, dark pair fixed)</b> lands as <code>data/delta-gain · delta-loss · delta-neutral ·
  delta-warning</code> (per mode) with D1 held as <code>kept-option</code>, plus the scoped col26-012 /
  red-once-per-screen override wording recorded in <code>_LIVE-STATE</code> +
  <code>guidelines/data-visualisation.md</code>.</li>
  <li><b>Vibration rule</b> enters <code>_validate_dataviz.py</code> as an advisory adjacent-pair check
  (thresholds 1.25 · 135° · 0.5, tunable), alongside the blocking set.</li>
  <li>The chart gate binds palette-only fills (dv-017) to the assigned tokens across BOTH contrast bindings;
  indicator-contrast extends to <code>data/series-*</code> and <code>data/delta-*</code>.</li>
  <li>§06 ranges stay exploration unless you promote one; the range-catalog direction (intent-categorised,
  designer-selectable) is logged as the future workstream.</li>
  <li>Round-one kit (KPI card · line/spark · bar/column/stacked · donut) builds against C-default + A-high-contrast —
  spec in the method dossier (<code>reviews/DATAVIZ-METHOD-2026-07-16.html</code>).</li>
</ul>
<p class="meta" style="margin-top:32px;border-top:1px solid var(--line);padding-top:16px;">Apollo · DataViz V7
decision sheet · 2026-07-16 · charts obey the rules they model: zero baselines (bars), straight lines, ≤6
slices largest-first from 12 o'clock, ≥2px separation, flat fills, letters on elements, colour+letter+name
legends. To mark up: <code>python3 knowledge/_review/_make_review.py reviews/DATAVIZ-SERIES-RENDERS-2026-07-16.html</code>.</p>
</div>
</body>
</html>'''

TOKENS_OUT = os.path.join(ROOT, "knowledge/tokens/_proposals/dataviz-ranges.proposals.json")

def emit_tokens():
    """Ranges as tokens (Dave 2026-07-16: range selection = a future edit-mode dial, so ranges live in
    the token layer as a dataviz range mode). Holding pen, same pattern as supporting-palette V7."""
    def series_entry(cands_key, mode):
        return {f"series-{i+1}": {"$value": PAL[f][str(s)]["$value"],
                                  "$token": f"color/supporting/{f}/{s}"}
                for i, (f, s) in enumerate(CANDS[cands_key][mode])}
    doc = {
      "$README": ("GENERATED by knowledge/_review/_gen_series_renders.py — do not hand-edit. HOLDING PEN for the "
                  "dataviz RANGE mode (Dave 2026-07-16): a range = a named value-set for the stable slots "
                  "data/series-1..5 (+ data/delta-*), selected per chart via data-range — the future edit-mode "
                  "harness dial. Statuses: 'picked-pending-confirm' = Dave's 2026-07-16 markup (C default / A "
                  "high-contrast / delta d2 with the dark-pair vibration fix); 'kept-option' = d1 (Dave: keep as an "
                  "option); 'retired-record' = d3; 'proposed' = suggestions, ungoverned until Dave promotes "
                  "(derivation governance). RULES CARRIED: ranges are PALETTE-NATIVE only (Dave: 'we can't invent "
                  "anything — only safe in the RAG'; every range value carries its $token path); deltas are the sole "
                  "derived-colour zone (RAG-class). $vibration = worst adjacent-pair vibrating-boundary level "
                  "(legs: value-ratio <1.25 + hue-sep >=135deg + sat >=0.5; from the Tuts+ article, Dave 2026-07-16). "
                  "On confirmation the picked ranges enter semantic-colour.json; proposed ranges stay here until "
                  "individually promoted."),
      "$provenance": {"generator": "knowledge/_review/_gen_series_renders.py",
                      "renders": "reviews/DATAVIZ-SERIES-RENDERS-2026-07-16.html (REV 2)",
                      "date": "2026-07-16"},
      "range": {
        "default": {"$intent": "harmony", "$status": "confirmed-2026-07-16",
                    "$note": "Candidate C — mode-stable; same values both modes (dv-014 across the theme switch). PROMOTED to semantic-colour.json data/series-*",
                    "light": series_entry("C", "light"), "dark": series_entry("C", "dark")},
        "high-contrast": {"$intent": "contrast", "$status": "confirmed-2026-07-16",
                          "$note": "Candidate A — palette-half per mode; bound via data-contrast/high or data-range. PROMOTED to semantic-colour.json data/series-high-contrast/*",
                          "light": series_entry("A", "light"), "dark": series_entry("A", "dark")},
      },
      "delta": {},
    }
    for r in collect_ranges():
        doc["range"][r["slug"]] = {
          "$intent": r["intent"], "$status": "proposed", "$note": r["desc"],
          "$vibration": {"light": vibration_worst(r["light"]), "dark": vibration_worst(r["dark"])},
          "light": {f"series-{i+1}": {"$value": v, "$token": t} for i, (v, t) in enumerate(zip(r["light"], r["light_tokens"]))},
          "dark":  {f"series-{i+1}": {"$value": v, "$token": t} for i, (v, t) in enumerate(zip(r["dark"], r["dark_tokens"]))},
        }
    STATUS_MAP = {"chosen": "confirmed-2026-07-16", "alt": "kept-option", "dead": "retired-record"}
    for (slug, name, status, note, hue_pull, sat, ratios, dark_sat) in DELTA_OPTS:
        dset = derive_set(hue_pull, sat, ratios, dark_sat)
        doc["delta"][slug] = {"$status": STATUS_MAP[status], "$note": note,
                              "$vibration": {"gain-loss-light": vibration(dset["gain"]["light"], dset["loss"]["light"])["level"],
                                             "gain-loss-dark": vibration(dset["gain"]["dark"], dset["loss"]["dark"])["level"]},
                              **{role: {"light": {"$value": dset[role]["light"]},
                                        "dark": {"$value": dset[role]["dark"]}}
                                 for role in ("gain", "loss", "neutral", "warning")}}
    # vibration receipts on the picked series ranges too
    for key, cands_key in (("default", "C"), ("high-contrast", "A")):
        doc["range"][key]["$vibration"] = {
          "light": vibration_worst([PAL[f][str(s)]["$value"] for f, s in CANDS[cands_key]["light"]]),
          "dark": vibration_worst([PAL[f][str(s)]["$value"] for f, s in CANDS[cands_key]["dark"]]),
        }
    with open(TOKENS_OUT, "w") as f:
        json.dump(doc, f, indent=1)
        f.write("\n")
    print(f"  ✓ wrote {os.path.relpath(TOKENS_OUT, ROOT)}")

def main():
    body = [HEAD]
    for idx, key in enumerate(("C", "A", "B"), start=2):
        body.append(candidate_section(idx, key))
    body.append(delta_section())
    body.append(ranges_section())
    body.append(FOOT)
    html = "".join(body)
    with open(OUT, "w") as f:
        f.write(html)
    print(f"  ✓ wrote {os.path.relpath(OUT, ROOT)} ({len(html)//1024} KB)")
    emit_tokens()

if __name__ == "__main__":
    sys.exit(main())
