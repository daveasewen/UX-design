"""Build helpers: every component's markup is COPIED from knowledge/snippets/ (by machine, from the
reference bytes), never typed from memory. Regions used verbatim are wrapped in APOLLO-SPLICE markers
so gen_provenance_receipt.py can mint a receipt for them; regions that had to be filled with page
content are copied-then-filled and carry no splice marker (they are not byte-identical, and saying
so is the honest form)."""
import os, re, json, html, sys
W = os.path.expanduser("~/cold/cand2-r1")
PACK = os.path.join(W, "pack")
SNIP = os.path.join(PACK, "knowledge", "snippets")
ICONS = os.path.join(PACK, "knowledge", "assets", "icons")
sys.path.insert(0, os.path.join(PACK, "knowledge"))
import gen_provenance_receipt as GPR
import _validate_receipt as VR

def snip(name):
    return open(os.path.join(SNIP, name + ".reference.html"), encoding="utf-8").read()

def element(name, select):
    return GPR.extract_element(snip(name), select)[0]

def splice(name, select, region):
    text = element(name, select)
    src = "knowledge/snippets/%s.reference.html" % name
    return "%s\n%s\n%s" % (VR.splice_marker_start(region, src, "markup"), text, VR.splice_marker_end(region))

def body(name):
    h = snip(name)
    return re.search(r"<body[^>]*>(.*)</body>", h, re.S).group(1)

def outside_fences(b):
    return re.sub(r"<!-- ===== APOLLO-DEMO (.*?) START.*?<!-- ===== APOLLO-DEMO \1 END ===== -->", "", b, flags=re.S)

def exec_scripts(name):
    """The component's own executable inline scripts, byte-exact, outside every APOLLO-DEMO fence."""
    b = outside_fences(body(name))
    return [m.group(2) for m in re.finditer(r"<script([^>]*)>(.*?)</script>", b, re.S)
            if "application/json" not in m.group(1) and "src=" not in m.group(1)]

def sprite(name):
    """A snippet's own icon sprite, copied verbatim (library-matched <symbol>s)."""
    b = body(name)
    return re.search(r"<svg width=\"0\" height=\"0\"[^>]*>.*?</svg>", b, re.S).group(0)

def lib_symbol(sid, rel):
    s = open(os.path.join(ICONS, rel), encoding="utf-8").read()
    inner = re.search(r"<svg[^>]*>(.*)</svg>", s, re.S).group(1).strip()
    assert "clip-path" not in inner and "<defs" not in inner, rel
    return '<symbol id="%s" viewBox="0 0 18 18">%s</symbol>' % (sid, inner)

SHELL_SYMS = re.findall(r'<symbol id="(ic-[^"]+)".*?</symbol>', sprite("App-shell-side-nav"), re.S)
def shell_symbol(sid):
    return re.search(r'<symbol id="%s".*?</symbol>' % re.escape(sid), sprite("App-shell-side-nav"), re.S).group(0)

MY_ICONS = {  # nav + chrome glyphs, each byte-copied from assets/icons
    "ic-dashboard": "media/dashboard.svg", "ic-liquidity": "products-and-services/liquidity-management.svg",
    "ic-payments": "products-and-services/payments-and-transfers.svg", "ic-fx": "products-and-services/fx.svg",
    "ic-risk": "status-icons/warning.svg", "ic-trade": "products-and-services/trade-finance.svg",
    "ic-report": "media/document-report.svg", "ic-message": "media/contact-message.svg",
    "ic-close": "global-controls/close.svg",
    "ic-error": "status-icons/error.svg",
}
def icon_sprite():
    syms = [shell_symbol(s) for s in ("ic-home", "ic-account", "ic-settings", "ic-chevron-left", "ic-chevron-right",
                                       "ic-chevron-down", "ic-menu", "ic-search", "ic-profile")]
    syms += [lib_symbol(k, v) for k, v in MY_ICONS.items()]
    return '<svg width="0" height="0" style="position:absolute" aria-hidden="true">\n' + "\n".join(syms) + "\n</svg>"

esc = lambda s: html.escape(str(s), quote=True)

# ------------------------------------------------------------------ charts (copied from each chart snippet)
FIGS = {  # kind -> (snippet, figure index, id prefix in that figure, scope class)
    "column": ("Chart-bar", 0, "cb1", "cn-chart-bar"), "bar": ("Chart-bar", 1, "cb2", "cn-chart-bar"),
    "grouped-column": ("Chart-bar", 3, "cb4", "cn-chart-bar"), "stacked-column": ("Chart-bar", 4, "cb5", "cn-chart-bar"),
    "line": ("Chart-line", 0, "cl1", "cn-chart-line"), "multiline": ("Chart-line", 1, "cl2", "cn-chart-line"),
    "donut": ("Chart-donut", 0, "cd1", "cn-chart-donut"), "pie": ("Chart-pie", 0, "cp1", "cn-chart-pie"),
    "stacked-area": ("Chart-stacked-area", 0, "csa1", "cn-chart-stacked-area"), "combo": ("Chart-combo", 0, "cc1", "cn-chart-combo"),
    "bullet": ("Chart-bullet", 0, "cbl1", "cn-chart-bullet"), "candlestick": ("Chart-candlestick", 0, "ccs1", "cn-chart-candlestick"),
    "scatter": ("Chart-scatter", 0, "cs1", "cn-chart-scatter"), "histogram": ("Chart-histogram", 0, "ch1", "cn-chart-histogram"),
    "boxplot": ("Chart-boxplot", 0, "cbp1", "cn-chart-boxplot"), "butterfly-h": ("Chart-butterfly-h", 0, "cbh1", "cn-chart-butterfly-h"),
    "spark": ("Chart-sparkline", 0, "cs1", "cn-chart-sparkline"),
}
def _figures(name):
    h = re.sub(r"<!-- ===== AUTO-BEHAVIOUR (\S+) START.*?AUTO-BEHAVIOUR \1 END ===== -->", "", snip(name), flags=re.S)
    b = outside_fences(h[h.find("<body"):])
    out, pos = [], 0
    while True:
        i = b.find("<figure", pos)
        if i < 0: return out
        depth = 0
        for m in re.finditer(r"<(/?)figure\b", b[i:]):
            depth += -1 if m.group(1) else 1
            if depth == 0:
                j = b.find(">", i + m.end()) + 1; break
        out.append(b[i:j]); pos = j

LETTERS = "ABCDEFGHIJ"
SHAPES = ["sw-circle", "sw-square", "sw-diamond"]
def figure(kind, fid, title, caption, cols, series=None, keep_seg=False):
    name, idx, pfx, scope = FIGS[kind]
    f = _figures(name)[idx]
    f = re.sub(r"<!--.*?-->", "", f, flags=re.S)
    f = re.sub(r'(["\s#])%s(?=["-])' % pfx, lambda m: m.group(1) + fid, f)
    if not re.match(r'<figure[^>]*\sid="%s"' % fid, f):
        f = f.replace("<figure", '<figure id="%s"' % fid, 1)
    f = re.sub(r'data-lockup-title="[^"]*"', 'data-lockup-title="%s"' % esc(title), f)
    f = re.sub(r'(<h3 class="dv-title[^"]*">).*?(</h3>)', lambda m: m.group(1) + esc(title) + m.group(2), f, flags=re.S)
    f = re.sub(r'(<figcaption[^>]*>).*?(</figcaption>)', lambda m: m.group(1) + esc(caption) + m.group(2), f, flags=re.S)
    f = re.sub(r'(<caption>).*?(</caption>)', lambda m: m.group(1) + esc(caption) + m.group(2), f, flags=re.S)
    f = re.sub(r'(class="dv-tablepanel[^"]*"[^>]*aria-label=")[^"]*(")', lambda m: m.group(1) + esc(caption) + ", data table" + m.group(2), f)
    f = re.sub(r'(<svg class="dv-svg[^>]*aria-label=")[^"]*(")', lambda m: m.group(1) + esc(caption) + "." + m.group(2), f, flags=re.S)
    f = re.sub(r'<thead>.*?</thead>', '<thead><tr>' + "".join('<th scope="col">%s</th>' % esc(c) for c in cols) + '</tr></thead>', f, flags=re.S)
    f = re.sub(r'(<tbody[^>]*>).*?(</tbody>)', r'\1\2', f, flags=re.S)
    f = re.sub(r'<tbody[^>]*class="dv-off"[^>]*></tbody>\s*', '', f)
    f = re.sub(r'<tbody data-dv-view="orig">', '<tbody>', f)
    if not keep_seg:
        f = re.sub(r'<div class="seg sm"[^>]*>.*?</div>\s*', '', f, flags=re.S)
    if kind != "combo":
        f = re.sub(r'<div class="dv-toggle-seg">.*?</div>\s*', '', f, flags=re.S)
    f = re.sub(r'\sdata-total="[^"]*"', '', f)
    f = re.sub(r'\sdata-domain-max="[^"]*"', '', f)
    if series is not None:
        if kind == "butterfly-h":
            names = iter(series)
            f = re.sub(r'(<span class="dv-leg-name">)[^<]*(</span>)', lambda m: m.group(1) + esc(next(names)) + m.group(2), f)
        elif kind == "histogram":
            f = re.sub(r'(<ul class="dv-leg-static[^>]*>\s*<li><span class="sw"></span><span>)[^<]*', lambda m: m.group(1) + esc(series[0]), f)
        else:
            m = re.search(r'(<ul class="dv-leg[^"]*"[^>]*>)(.*?)(</ul>)', f, re.S)
            if m:
                rows = re.findall(r'<li class="dv-legrow".*?</li>', m.group(2), re.S)
                tpl = rows[0]; oldname = re.search(r'dv-leg-name">([^<]*)<', tpl).group(1)
                lines = kind in ("line", "multiline")
                out = []
                for i, nm in enumerate(series):
                    r = tpl.replace('data-series="1"', 'data-series="%d"' % (i + 1))
                    r = r.replace("--data-series-1)", "--data-series-%d)" % (i % 5 + 1))
                    r = r.replace(">A</span>", ">%s</span>" % LETTERS[i])
                    r = r.replace(oldname, esc(nm))
                    if lines: r = re.sub(r"sw-(circle|square|diamond)", SHAPES[i % 3], r)
                    out.append(r)
                reset = re.search(r'<li class="dv-leg-reset-wrap">.*?</li>', m.group(2), re.S)
                f = f[:m.start(2)] + "\n      " + "\n      ".join(out) + ("\n      " + reset.group(0) if reset else "") + "\n    " + f[m.end(2):]
    return '<div class="%s">%s</div>' % (scope, f)

def canon_scripts():
    base = "../pack/knowledge/canon/"
    order = ["dv-behaviour", "dv-legend", "dv-render", "dv-render-bar", "dv-render-line", "dv-render-combo", "dv-render-donut",
             "dv-render-stacked-area", "dv-render-bullet", "dv-render-candlestick", "dv-render-scatter", "dv-render-histogram",
             "dv-render-boxplot", "dv-render-butterfly", "dv-render-sparkline"]
    return "\n".join('<script src="%s%s.js"></script>' % (base, n) for n in order)
