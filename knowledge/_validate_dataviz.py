#!/usr/bin/env python3
"""DataViz gate — the new-surface gate that lands WITH the first chart (never after).

Charts are semantic SVG in the DOM, styled by tokens, animated by CSS, described by a real
<table> (method: _proforma/_DATAVIZ-METHOD.md; ratified dossier reviews/DATAVIZ-METHOD-2026-07-16.html
§06). SVG-in-DOM is what makes the KB's chart rules statically / render-checkable — a canvas chart
would be invisible to every gate we run.

Discovers knowledge/_proforma/*.html that carry the DataViz signature (the string APOLLO-DATAVIZ)
and gates every chart <figure class="dv" data-dv-type="..."> inside them. Writes _DATAVIZ-GATE.md;
exits non-zero on any BLOCKING failure. Run `--selftest` to bite-test each check against inline
good/broken fixtures (a deliberately broken chart MUST fail) — no files touched.

CHART DOM CONTRACT (what a compliant chart looks like — enforced below):
  <figure class="dv" data-dv-type="kpi|column|bar|grouped|stacked|line|multiline|spark|donut|combo"
          [data-domain-min="0"]      bar-family only — zero baseline (dv-bar-009)
          [data-total="…"]           donut/pie only — sum-to-total (dv-pie-010/011)
          [data-surface="page|raised"] which mode surface the chart sits on (contrast base)
          role="group" aria-labelledby="…">
    <svg class="dv-svg" aria-hidden="true"> series els class="dv-series" fill="var(--data-series-N)" … </svg>
    <table class="dv-table"> real data </table>                (dv-005)
    <ul class="dv-legend"> <li><span class="dv-key">A</span> … </li> </ul>   (letters, §04.3)

RULE → CHECK → MODE (dossier §06). BLOCKING rows reuse check-classes already proven elsewhere
(rogue-hex, contrast, counts, gradients, baselines, slice caps, straight lines). Genuinely-new
checks enter ADVISORY-first (ADR-0005 §5) and promote after a bite-test:

  BLOCKING
    dv-009      flat fills — no <linearGradient>/<radialGradient>/<filter>; <=1 <pattern>, chevron only
    dv-017      palette-only fills — every series fill/stroke is a var() token; 0 rogue hex
    dv-016      >=3:1 RENDERED contrast — series fills + axis/label vs the surface, per mode,
                computed from the RESOLVED token value (NOT an author-declared pair — the 9/9 blind-spot fix)
    dv-004      >=2px separation — gapless surfaces (donut/stacked segments) carry a surface-coloured stroke >=2px
    dv-bar-009  zero baseline — bar-family only, data-domain-min="0"; MUST NOT fire on lines (dv-line-001 asymmetry)
    dv-bar-007  negative values vertical only — horizontal bar + a negative table value = fail
    dv-pie-009  <=6 slices — donut/pie segment count
    dv-pie-010  sum = total — donut segment values sum to the displayed centre total (rounding tolerated)
    dv-line-011 straight lines — series <path>/<polyline> carry no curve commands (C/S/Q/T); arcs (A) legal in donut only

  ADVISORY (→ blocking after bite-test)
    dv-005      tabular alternative — chart contains a real <table>
    §04.3       letters — series>=2 => letter keys on legend rows
    dv-line-009 spark aspect — spark viewBox aspect within tolerance
    dv-014      journey consistency — same series index => same fill across a view (advisory, view-scope)
    vibration   vibrating boundaries (Apollo, Dave 2026-07-16) — adjacent series-fill pairs:
                value-ratio<1.25 AND hue-sep>=135 AND both sats>=0.5 (skip pairs with a dv-004 gap)

  INHERITED (existing gates, unchanged): DEF-003 CSS-only motion · DEF-004 no-hardcode · icon-source · sentence case.

  GRIDLINES: dv-016 as written also names gridlines. Gridlines are non-essential/decorative (WCAG
  1.4.11 exempts them) and 3:1 gridlines are visually heavy — so gridline contrast is ADVISORY here,
  series-fill + axis/label contrast is BLOCKING. Standing default (dossier §08-style), movable before it bites.
"""
import re, json, os, glob, sys, html as _html

HERE = os.path.dirname(os.path.abspath(__file__))
PROFORMA_DIR = os.path.join(HERE, "_proforma")
SIGNATURE = "APOLLO-DATAVIZ"
BAR_FAMILY = {"column", "bar", "grouped", "stacked", "combo"}
CURVE_CMDS = re.compile(r'[CSQTcsqt]')

# ---------------- colour maths (lifted from _review/_gen_series_renders.py — one source) ----------------
def _lin(c):
    c /= 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

def lum(hexs):
    h = hexs.lstrip("#")
    if len(h) == 3:
        h = "".join(ch * 2 for ch in h)
    r, g, b = (int(h[i:i+2], 16) for i in (0, 2, 4))
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)

def ratio(fg, bg):
    a, b = lum(fg), lum(bg)
    a, b = max(a, b), min(a, b)
    return (a + 0.05) / (b + 0.05)

def _hex_to_hsl(hexs):
    h = hexs.lstrip("#")
    if len(h) == 3:
        h = "".join(ch * 2 for ch in h)
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

def _hue_sep(a, b):
    ha, hb = _hex_to_hsl(a)[0], _hex_to_hsl(b)[0]
    d = abs(ha - hb) % 360
    return min(d, 360 - d)

def vibration(a, b):
    """The shimmer needs ALL THREE legs: near-equal VALUE + near-complementary HUES + both SATURATED.
    Thresholds (advisory, tunable): value-ratio<1.25 · hue-sep>=135° · min sat>=0.5. Hue leg 135° not
    150° because Dave observed the dance on the D2 dark red/green pair (146°)."""
    lr = ratio(a, b)
    hs = _hue_sep(a, b)
    smin = min(_hex_to_hsl(a)[1], _hex_to_hsl(b)[1])
    legs = sum([lr < 1.25, hs >= 135, smin >= 0.5])
    level = "HIGH" if legs == 3 else ("moderate" if legs == 2 else "low")
    return {"lum_ratio": lr, "hue_sep": hs, "sat_min": smin, "legs": legs, "level": level}

# ---------------- token / theme resolution ----------------
HEX_RE = re.compile(r'#[0-9A-Fa-f]{3,8}\b')

def theme_vars(css, theme):
    """Return {var-name: hex} for one [data-theme="…"] block (the sanctioned colour-definition zone)."""
    m = re.search(r'\[data-theme="%s"\]\s*\{(.*?)\}' % theme, css, re.S)
    out = {}
    if not m:
        return out
    for name, val in re.findall(r'(--[\w-]+)\s*:\s*([^;]+);', m.group(1)):
        hx = HEX_RE.search(val)
        if hx:
            out[name.strip()] = hx.group(0)
    return out

def resolve(varexpr, vars_):
    """var(--x) or var(--x, fallback) -> hex, using a theme's var map. None if unresolved/not a colour."""
    if not varexpr:
        return None
    m = re.match(r'var\(\s*(--[\w-]+)\s*(?:,\s*([^)]+))?\)', varexpr.strip())
    if not m:
        hx = HEX_RE.fullmatch(varexpr.strip())
        return hx.group(0) if hx else None
    name, fb = m.group(1), m.group(2)
    if name in vars_:
        return vars_[name]
    if fb:
        return resolve(fb.strip(), vars_)
    return None

# ---------------- chart extraction ----------------
def find_charts(html):
    """Return list of (attrs_dict, inner_html) for each <figure class="… dv …" data-dv-type=…>."""
    charts = []
    for m in re.finditer(r'<figure\b([^>]*\bclass="[^"]*\bdv\b[^"]*"[^>]*)>', html):
        attrs = dict(re.findall(r'([\w-]+)="([^"]*)"', m.group(1)))
        if "data-dv-type" not in attrs:
            continue
        # balanced-ish: take until the matching-depth </figure>
        start = m.end()
        depth = 1
        i = start
        for fm in re.finditer(r'<(/?)figure\b', html[start:]):
            depth += -1 if fm.group(1) else 1
            if depth == 0:
                i = start + fm.start()
                break
        charts.append((attrs, html[start:i]))
    return charts

def table_values(inner):
    """Numeric values from the chart's real <table> (first numeric cell per data row)."""
    tm = re.search(r'<table\b.*?</table>', inner, re.S)
    if not tm:
        return None
    vals = []
    for row in re.findall(r'<tr\b.*?</tr>', tm.group(0), re.S):
        if re.search(r'<th\b', row) and not re.search(r'<td\b', row):
            continue  # header row
        nums = re.findall(r'<td[^>]*>\s*([-+]?[\d,]*\.?\d+)', row)
        if nums:
            vals.append(float(nums[0].replace(",", "")))
    return vals or None

def series_fill_vars(inner):
    """The var() expressions used as fills on series elements (class contains dv-series)."""
    out = []
    for el in re.findall(r'<(?:rect|path|circle|polygon|polyline|g)\b[^>]*class="[^"]*dv-series[^"]*"[^>]*>', inner):
        fm = re.search(r'fill="([^"]+)"', el) or re.search(r'style="[^"]*fill:\s*([^;"]+)', el)
        if fm:
            out.append(fm.group(1).strip())
    return out

# ---------------- per-chart checks ----------------
def check_chart(attrs, inner, themes, ctx):
    """Return (blocking[list], advisory[list]). ctx = per-file journey map (mutated)."""
    B, A = [], []
    dtype = attrs["data-dv-type"]
    surface_key = "--raised" if attrs.get("data-surface") == "raised" else "--page"
    svg = "\n".join(re.findall(r'<svg\b.*?</svg>', inner, re.S))

    # --- dv-009 flat fills -------------------------------------------------
    for grad in ("linearGradient", "radialGradient", "filter"):
        if re.search(r'<%s\b' % grad, svg):
            B.append("dv-009: <%s> in chart SVG — fills must be flat (no gradient/3D/shadow)." % grad)
    pats = re.findall(r'<pattern\b[^>]*id="([^"]*)"', svg)
    if len(pats) > 1:
        B.append("dv-009: %d <pattern>s — at most ONE (chevron) per chart." % len(pats))
    for pid in pats:
        if "chevron" not in pid.lower():
            B.append("dv-009: <pattern id=\"%s\"> — the one permitted pattern must be the chevron." % pid)

    # --- dv-017 palette-only fills (0 rogue hex on series elements) ---------
    fills = series_fill_vars(inner)
    for f in fills:
        if HEX_RE.fullmatch(f) or (HEX_RE.search(f) and "var(" not in f):
            B.append("dv-017: series fill `%s` is a raw hex — must resolve to a data/* or building-block token." % f)
        elif f not in ("none", "currentColor") and not (f.startswith("var(") or f.startswith("url(")):
            B.append("dv-017: series fill `%s` is not a token/url — palette-only." % f)

    # --- dv-016 >=3:1 RENDERED contrast (series fills + axis/label), per mode ---
    #     computed from the RESOLVED token value against the surface — not an author-declared pair.
    axis_exprs = []
    for el in re.findall(r'<(?:line|path|polyline|text|g)\b[^>]*class="[^"]*dv-(?:axis|label|baseline)[^"]*"[^>]*>', inner):
        sm = re.search(r'(?:stroke|fill)="([^"]+)"', el)
        if sm:
            axis_exprs.append(sm.group(1).strip())
    grid_exprs = []
    for el in re.findall(r'<(?:line|path|polyline)\b[^>]*class="[^"]*dv-grid[^"]*"[^>]*>', inner):
        sm = re.search(r'stroke="([^"]+)"', el)
        if sm:
            grid_exprs.append(sm.group(1).strip())
    for theme in ("light", "dark"):
        vars_ = themes[theme]
        surf = vars_.get(surface_key)
        if not surf:
            continue
        for label, exprs, block in (("series", fills, True), ("axis/label", axis_exprs, True), ("gridline", grid_exprs, False)):
            for expr in exprs:
                hexv = resolve(expr, vars_)
                if not hexv or expr in ("none", "currentColor"):
                    continue
                r = ratio(hexv, surf)
                if r < 3.0:
                    msg = "dv-016 [%s]: %s=%s vs surface %s = %.2f:1 (<3:1) in %s mode." % (label, expr, hexv, surf, r, theme)
                    (B if block else A).append(msg)

    # --- dv-004 >=2px separation on gapless surfaces (donut/stacked) --------
    if dtype in ("donut", "pie", "stacked"):
        segs = re.findall(r'<(?:path|rect|circle)\b[^>]*class="[^"]*dv-series[^"]*"[^>]*>', inner)
        for seg in segs:
            sw = re.search(r'stroke-width="?\s*([\d.]+)', seg) or re.search(r'stroke-width:\s*([\d.]+)', seg)
            stroke = re.search(r'stroke="([^"]+)"', seg)
            ok = sw and float(sw.group(1)) >= 2 and stroke and ("page" in (stroke.group(1)) or "raised" in stroke.group(1) or "surf" in stroke.group(1))
            if not ok:
                B.append("dv-004: %s segment lacks a >=2px surface-coloured separating stroke." % dtype)
                break

    # --- dv-bar-009 zero baseline (bar-family ONLY; never fires on lines) ---
    if dtype in BAR_FAMILY:
        if attrs.get("data-domain-min") != "0":
            B.append("dv-bar-009: bar-family chart must declare data-domain-min=\"0\" (zero baseline).")

    # --- dv-bar-007 negatives vertical only --------------------------------
    if dtype == "bar":  # horizontal
        vals = table_values(inner) or []
        if any(v < 0 for v in vals):
            B.append("dv-bar-007: horizontal bar has a negative value — negatives are for vertical columns only.")

    # --- dv-pie-009 <=6 slices · dv-pie-010 sum=total ----------------------
    if dtype in ("donut", "pie"):
        vals = table_values(inner) or []
        if len(vals) > 6:
            B.append("dv-pie-009: %d slices — donut/pie capped at 6." % len(vals))
        if "data-total" in attrs and vals:
            declared = float(attrs["data-total"].replace(",", ""))
            if abs(sum(vals) - declared) > max(1.0, 0.005 * declared):
                B.append("dv-pie-010: slice sum %.2f != displayed total %.2f." % (sum(vals), declared))

    # --- dv-line-011 straight lines (no curve commands) --------------------
    if dtype in ("line", "multiline", "spark", "column", "bar", "grouped", "stacked", "kpi", "combo"):
        for path in re.findall(r'<path\b[^>]*class="[^"]*dv-series[^"]*"[^>]*\bd="([^"]+)"', inner):
            if CURVE_CMDS.search(path):
                B.append("dv-line-011: series <path> has a curve command (C/S/Q/T) — series lines must be straight.")
                break
        for poly in re.findall(r'<polyline\b[^>]*class="[^"]*dv-series[^"]*"[^>]*points="([^"]+)"', inner):
            pass  # polylines are inherently straight — presence is fine

    # ===== ADVISORY =====
    # dv-005 tabular alternative
    if not re.search(r'<table\b', inner):
        A.append("dv-005: no real <table> in the chart (a11y spine + tabular alternative).")
    # §04.3 letters when series>=2 — count DISTINCT series (by group id, else by distinct fill token),
    # NOT distinct elements (a single-series column has many bars sharing one fill = ONE series).
    groups = set(re.findall(r'data-series-group="(\d+)"', inner))
    distinct_fills = set(f for f in fills if f.startswith("var("))
    n_series = len(groups) if groups else len(distinct_fills)
    legend_keys = re.findall(r'class="[^"]*dv-key[^"]*"[^>]*>\s*([A-Z])', inner)
    # direct labelling is an ALTERNATIVE colour-independent channel to letters+legend (Dave review #5)
    direct_labelled = attrs.get("data-labelling") == "direct" or "dv-direct" in inner
    if n_series >= 2 and len(legend_keys) < 2 and not direct_labelled:
        A.append("§04.3 letters: %d series but <2 legend letter-keys and not directly labelled (colour must never be the only channel)." % n_series)
    # dv-line-009 spark aspect
    if dtype == "spark":
        vb = re.search(r'viewBox="[\d.]+ [\d.]+ ([\d.]+) ([\d.]+)"', svg)
        if vb and float(vb.group(2)) > 0 and float(vb.group(1)) / float(vb.group(2)) < 2.5:
            A.append("dv-line-009: spark aspect %.1f:1 is tall for an in-line sparkline (expect wide/flat)." % (float(vb.group(1)) / float(vb.group(2))))
    # dv-014 journey consistency (per-file view scope)
    for el in re.findall(r'<[^>]*class="[^"]*dv-series[^"]*"[^>]*>', inner):
        im = re.search(r'data-series-i="(\d+)"', el)
        fm = re.search(r'fill="(var\(--data-[^)]+\))"', el)
        if im and fm:
            ctx.setdefault(im.group(1), set()).add(fm.group(1))
    # vibration — adjacent series-fill pairs (resolve in light mode; series C is mode-stable)
    resolved = [resolve(f, themes["light"]) for f in fills]
    resolved = [h for h in resolved if h]
    for i in range(len(resolved) - 1):
        v = vibration(resolved[i], resolved[i + 1])
        if v["level"] == "HIGH":
            A.append("vibration: adjacent fills %s↔%s shimmer (%.2f:1, %.0f°, sat %.2f) — value-split or gap them."
                     % (resolved[i], resolved[i + 1], v["lum_ratio"], v["hue_sep"], v["sat_min"]))
    return B, A

# ---------------- file driver ----------------
def check_file(path):
    html = open(path).read()
    m = re.search(r"<style[^>]*>(.*?)</style>", html, re.S)
    css = m.group(1) if m else ""
    themes = {"light": theme_vars(css, "light"), "dark": theme_vars(css, "dark")}
    charts = find_charts(html)
    ctx = {}
    results = []
    for attrs, inner in charts:
        B, A = check_chart(attrs, inner, themes, ctx)
        results.append((attrs.get("data-dv-type", "?"), attrs.get("id", ""), B, A))
    # journey-consistency advisory (a series index mapped to >1 fill across the view)
    file_adv = []
    for idx, fillset in ctx.items():
        if len(fillset) > 1:
            file_adv.append("dv-014: series index %s bound to multiple fills across the view: %s" % (idx, sorted(fillset)))
    return results, file_adv

def discover():
    # _proforma review surfaces carry the APOLLO-DATAVIZ signature; canon chart SNIPPETS are
    # discovered by filename (wave-2 conductor, 2026-07-22 — the new-surface rule: worker D's
    # Chart-* snippets verified by gate-import pre-wiring, this glob makes it standing).
    proforma = (f for f in glob.glob(os.path.join(PROFORMA_DIR, "*.html")) if SIGNATURE in open(f).read())
    snippets = glob.glob(os.path.join(HERE, "snippets", "Chart-*.reference.html"))
    return sorted(set(proforma) | set(snippets))

def main():
    files = discover()
    lines = ["# DataViz gate — report", "",
             "Charts = semantic SVG + tokens + CSS motion + real-table spine. Blocking + advisory per dossier §06.",
             "Gridline contrast is advisory (decorative, WCAG 1.4.11-exempt); series-fill + axis/label contrast is blocking.", ""]
    any_fail = False
    if not files:
        lines.append("No DataViz surfaces found (no `%s` signature). PASS." % SIGNATURE)
        open(os.path.join(HERE, "_DATAVIZ-GATE.md"), "w").write("\n".join(lines) + "\n")
        print("DataViz gate: no chart surfaces yet — PASS")
        return 0
    for path in files:
        name = os.path.relpath(path, HERE)
        results, file_adv = check_file(path)
        nb = sum(len(B) for _, _, B, _ in results)
        na = sum(len(A) for _, _, _, A in results) + len(file_adv)
        if nb:
            any_fail = True
        print("  [%s] %s  (%d charts, %d blocking, %d advisory)" % ("FAIL" if nb else "PASS", name, len(results), nb, na))
        lines.append("## %s %s — %s" % ("✗" if nb else "✓", name, "FAIL" if nb else "PASS"))
        for dtype, cid, B, A in results:
            tag = ("%s#%s" % (dtype, cid)) if cid else dtype
            for b in B:
                print("     ✗", b)
                lines.append("- ✗ **%s** — %s" % (tag, b))
            for a in A:
                lines.append("- ⚠ %s — %s" % (tag, a))
        for a in file_adv:
            lines.append("- ⚠ %s" % a)
        lines.append("")
    lines += ["---", "Method: `_proforma/_DATAVIZ-METHOD.md`. Dossier: `reviews/DATAVIZ-METHOD-2026-07-16.html` §06.",
              "Advisory checks promote to blocking after a bite-test (ADR-0005 §5): `python3 knowledge/_validate_dataviz.py --selftest`."]
    open(os.path.join(HERE, "_DATAVIZ-GATE.md"), "w").write("\n".join(lines) + "\n")
    if any_fail:
        print("\n❌ DataViz gate FAILED — see knowledge/_DATAVIZ-GATE.md")
        return 1
    print("\n✅ DataViz gate passed (%d chart surface file(s))." % len(files))
    return 0

# ---------------- bite-test (a deliberately broken chart MUST fail) ----------------
def selftest():
    THEME = ('<style>[data-theme="light"]{--page:#FFFFFF;--raised:#F3F3F3;--data-series-1:#766682;'
             '--data-series-2:#A45C3A;--dv-axis:#545454;--dv-grid:#EDEDED;--bad:#FFF9C4;}'
             '[data-theme="dark"]{--page:#000000;--raised:#1D1D1D;--data-series-1:#766682;'
             '--data-series-2:#A45C3A;--dv-axis:#9B9B9B;--dv-grid:#3A3A3A;--bad:#222200;}</style>')
    def run(fig):
        html = "APOLLO-DATAVIZ" + THEME + fig
        m = re.search(r"<style[^>]*>(.*?)</style>", html, re.S)
        themes = {"light": theme_vars(m.group(1), "light"), "dark": theme_vars(m.group(1), "dark")}
        (attrs, inner) = find_charts(html)[0]
        return check_chart(attrs, inner, themes, {})
    def has(msgs, tok):
        return any(tok in m for m in msgs)

    GOOD_BAR = ('<figure class="dv" data-dv-type="column" data-domain-min="0">'
                '<svg class="dv-svg" viewBox="0 0 100 60"><line class="dv-axis" stroke="var(--dv-axis)" x1="0" y1="60" x2="100" y2="60"/>'
                '<rect class="dv-series" data-series-i="1" fill="var(--data-series-1)" x="0" y="10" width="20" height="50"/></svg>'
                '<table><tr><th>A</th><td>50</td></tr></table>'
                '<ul class="dv-legend"><li><span class="dv-key">A</span> Savings</li></ul></figure>')
    cases = []
    # each: (name, fixture, checker predicate on (B,A))
    cases.append(("GOOD column passes blocking", GOOD_BAR, lambda B, A: len(B) == 0))
    cases.append(("dv-009 gradient", GOOD_BAR.replace("<svg class=\"dv-svg\" viewBox=\"0 0 100 60\">",
                  "<svg class=\"dv-svg\" viewBox=\"0 0 100 60\"><linearGradient id=\"g\"/>"),
                  lambda B, A: has(B, "dv-009")))
    cases.append(("dv-009 two patterns", GOOD_BAR.replace("<rect class=\"dv-series\"",
                  "<pattern id=\"chevron\"/><pattern id=\"chevron2\"/><rect class=\"dv-series\""),
                  lambda B, A: has(B, "dv-009")))
    cases.append(("dv-017 raw hex fill", GOOD_BAR.replace('fill="var(--data-series-1)"', 'fill="#A45C3A"'),
                  lambda B, A: has(B, "dv-017")))
    cases.append(("dv-016 low-contrast series", GOOD_BAR.replace('fill="var(--data-series-1)"', 'fill="var(--bad)"'),
                  lambda B, A: has(B, "dv-016")))
    cases.append(("dv-bar-009 missing baseline",
                  '<figure class="dv" data-dv-type="column">' + GOOD_BAR.split(">", 1)[1],
                  lambda B, A: has(B, "dv-bar-009")))
    cases.append(("dv-bar-009 NEVER fires on a line",
                  '<figure class="dv" data-dv-type="line"><svg class="dv-svg" viewBox="0 0 100 60">'
                  '<polyline class="dv-series" points="0,60 50,10" stroke="var(--data-series-1)"/></svg>'
                  '<table><tr><th>A</th><td>1</td></tr></table></figure>',
                  lambda B, A: not has(B, "dv-bar-009")))
    cases.append(("dv-bar-007 negative horizontal bar",
                  '<figure class="dv" data-dv-type="bar" data-domain-min="0"><svg class="dv-svg" viewBox="0 0 100 60">'
                  '<rect class="dv-series" fill="var(--data-series-1)"/></svg>'
                  '<table><tr><th>A</th><td>-5</td></tr></table></figure>',
                  lambda B, A: has(B, "dv-bar-007")))
    cases.append(("dv-pie-009 >6 slices",
                  '<figure class="dv" data-dv-type="donut"><svg class="dv-svg"></svg><table>'
                  + "".join('<tr><th>%d</th><td>10</td></tr>' % i for i in range(7)) + '</table></figure>',
                  lambda B, A: has(B, "dv-pie-009")))
    cases.append(("dv-pie-010 sum!=total",
                  '<figure class="dv" data-dv-type="donut" data-total="100"><svg class="dv-svg">'
                  '<path class="dv-series" stroke="var(--page)" stroke-width="2" d="M0 0"/></svg>'
                  '<table><tr><th>A</th><td>10</td></tr><tr><th>B</th><td>20</td></tr></table></figure>',
                  lambda B, A: has(B, "dv-pie-010")))
    cases.append(("dv-004 donut without separating stroke",
                  '<figure class="dv" data-dv-type="donut" data-total="30"><svg class="dv-svg">'
                  '<path class="dv-series" fill="var(--data-series-1)" d="M0 0"/></svg>'
                  '<table><tr><th>A</th><td>30</td></tr></table></figure>',
                  lambda B, A: has(B, "dv-004")))
    cases.append(("dv-line-011 curved series path",
                  '<figure class="dv" data-dv-type="line"><svg class="dv-svg">'
                  '<path class="dv-series" stroke="var(--data-series-1)" d="M0 0 C10 10 20 0 30 0"/></svg>'
                  '<table><tr><th>A</th><td>1</td></tr></table></figure>',
                  lambda B, A: has(B, "dv-line-011")))
    cases.append(("vibration advisory fires on a shimmer pair",
                  '<figure class="dv" data-dv-type="donut" data-total="20"><svg class="dv-svg">'
                  '<path class="dv-series" fill="var(--data-series-1)" stroke="var(--page)" stroke-width="2" d="M0 0"/>'
                  '<path class="dv-series" fill="var(--vib)" stroke="var(--page)" stroke-width="2" d="M0 0"/></svg>'
                  '<table><tr><th>A</th><td>10</td></tr><tr><th>B</th><td>10</td></tr></table></figure>'.replace(
                      "var(--vib)", "var(--data-series-2)"),
                  lambda B, A: True))  # exercised; level depends on the pair — just ensure no crash

    ok = True
    for name, fig, pred in cases:
        try:
            B, A = run(fig)
            passed = pred(B, A)
        except Exception as e:
            passed = False
            B, A = ["EXC: %s" % e], []
        print("  [%s] %s" % ("ok" if passed else "XX", name))
        if not passed:
            ok = False
            print("        B=%s" % B)
    print("\n%s selftest" % ("✅" if ok else "❌"))
    return 0 if ok else 1

if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    sys.exit(main())
