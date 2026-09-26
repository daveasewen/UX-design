#!/usr/bin/env python3
"""Assemble out/index.html from exact snippet cuts (templates) + authored CSS/JS. Run from anywhere."""
import os, re, sys, json
W = os.path.expanduser('~/cold/cand-r2'); PACK = W + '/pack'; K = PACK + '/knowledge'
sys.path.insert(0, K)
import gen_provenance_receipt as g
import _validate_receipt as VR
SRC = W + '/src'

def snip(name):
    return open(os.path.join(K, 'snippets', name + '.reference.html'), encoding='utf-8').read()

def cut_where(html, pred, nth=0):
    """exact bytes of the nth element in <body> whose opening tag satisfies pred(tag, attrs)."""
    bm = g.BODY_RE.search(html); body = bm.group(1)
    masked = g.COMMENT_RE.sub(lambda m: ' ' * len(m.group(0)), body)
    k = -1
    for m in g.TAG_RE.finditer(masked):
        closing, tag, attrs, sc = m.group(1), m.group(2).lower(), m.group(3), m.group(4)
        if closing or not pred(tag, attrs):
            continue
        k += 1
        if k < nth:
            continue
        if sc or tag in g.VOID:
            return body[m.start():m.end()]
        depth = 1
        for n in g.TAG_RE.finditer(masked, m.end()):
            if n.group(2).lower() != tag: continue
            if n.group(1):
                depth -= 1
                if depth == 0: return body[m.start():n.end()]
            elif not (n.group(4) or n.group(2).lower() in g.VOID): depth += 1
    raise SystemExit('cut failed')

def has(attr_sub):
    return lambda tag, attrs: attr_sub in attrs

REGIONS = []   # (template_id, snippet, bytes, receipted)
def part(tid, name, text, receipted=True):
    if 'APOLLO-DEMO' in text: raise SystemExit('demo chrome in cut %s' % tid)
    REGIONS.append((tid, name, text, receipted))

def sel(name, s): return g.extract_element(snip(name), s)[0]

# ---------------- the cuts ----------------
part('t-shell', 'App-shell-side-nav', sel('App-shell-side-nav', '#shell-wide'))
part('t-kpi', 'Kpi-tile', sel('Kpi-tile', '.as-link'))
FIGS = [('t-col','Chart-bar','cb1-h'),('t-hbar','Chart-bar','cb2-h'),('t-grouped','Chart-bar','cb4-h'),
        ('t-line','Chart-line','cl1-h'),('t-multi','Chart-line','cl2-h'),('t-donut','Chart-donut','cd1-h'),
        ('t-pie','Chart-pie','cp1-h'),('t-area','Chart-stacked-area','csa1-h'),('t-combo','Chart-combo','cc1-h'),
        ('t-scatter','Chart-scatter','cs1-h'),('t-bullet','Chart-bullet','cbl1-h'),('t-candle','Chart-candlestick','ccs1-h'),
        ('t-hist','Chart-histogram','ch1-h'),('t-box','Chart-boxplot','cbp1-h'),('t-fly','Chart-butterfly-h','cbh1-h'),
        ('t-spark','Chart-sparkline','cs1-h')]
for tid, name, lab in FIGS:
    part(tid, name, cut_where(snip(name), lambda t, a, lab=lab: t == 'figure' and 'aria-labelledby="%s"' % lab in a))
part('t-summary', 'Summary', sel('Summary', '.summary'))
part('t-scrim', 'Drawer', sel('Drawer', '#scrim'))
part('t-sheet', 'Drawer', sel('Drawer', '#sheet'))
part('t-modal', 'Modals', sel('Modals', '#overlay'))
part('t-toast', 'Toast', sel('Toast', '.toast'))
part('t-toastregion', 'Toast', sel('Toast', '#toastRegion'))
part('t-btn', 'Button', sel('Button', '.btn'))
part('t-btn3', 'Button', cut_where(snip('Button'), lambda t, a: t == 'button' and 'class="btn tertiary"' in a))
part('t-ph', 'Page-header-lockup', sel('Page-header-lockup', '.ph'))
part('t-sechead', 'Section-heading-lockup', cut_where(snip('Section-heading-lockup'), lambda t, a: t == 'div' and 'class="l-row"' in a and 'data-justify="between"' in a))
part('t-seg', 'Segmented-control', sel('Segmented-control', '.seg'))
part('t-chip', 'Status-indicator', sel('Status-indicator', '.chip'))
part('t-filterbar', 'Tags', sel('Tags', '#filterbar'))
part('t-lim', 'Limits-meter', sel('Limits-meter', '.lim'))
part('t-tl', 'Timeline', sel('Timeline', '.tl'))
part('t-list', 'List-items', sel('List-items', '.list'))
part('t-alert', 'Alert', sel('Alert', '.alert'))
part('t-alertwarn', 'Alert', cut_where(snip('Alert'), lambda t, a: t == 'div' and 'class="alert warn"' in a))
part('t-alertok', 'Alert', cut_where(snip('Alert'), lambda t, a: t == 'div' and 'class="alert ok"' in a))
part('t-field', 'Input-fields', sel('Input-fields', '.field'))
part('t-dd', 'Dropdown', sel('Dropdown', '.dd'))

def cut_at(html, needle):
    i = html.index(needle); j = html.index('<body'); 
    # predicate: the element starting exactly at i
    bm = g.BODY_RE.search(html); off = bm.start(1)
    return cut_where(html, lambda t, a, _c=[0]: False) if False else _cut_from(html, i)

def _cut_from(html, i):
    masked = g.COMMENT_RE.sub(lambda m: ' ' * len(m.group(0)), html)
    m = g.TAG_RE.match(masked, i); tag = m.group(2).lower(); depth = 1
    for n in g.TAG_RE.finditer(masked, m.end()):
        if n.group(2).lower() != tag: continue
        if n.group(1):
            depth -= 1
            if depth == 0: return html[i:n.end()]
        elif not (n.group(4) or tag in g.VOID): depth += 1

part('t-switch', 'Selection-controls', cut_at(snip('Selection-controls'), '<div class="field"><input type="checkbox" role="switch" id="s1">'))
# ---- copied whole but NOT receipted: their metas declare a #script address whose demo script targets demo ids ----
part('t-grid', 'Data-grid', sel('Data-grid', '#dg'), receipted=False)
part('t-ftb', 'Filter-toolbar-bar', sel('Filter-toolbar-bar', '#ftbA'), receipted=False)
part('t-tx', 'Textarea', sel('Textarea', '#live'), receipted=False)

# ---------------- sprite: union of the snippets' own <symbol> sheets + library glyphs ----------------
SPRITE_FROM = ['App-shell-side-nav','Kpi-tile','Data-grid','Input-fields','Textarea','Filter-toolbar-bar','Tags','Alert','Page-header-lockup','Section-heading-lockup','Empty-state','Card-header-lockup','Stat-card']
syms = {}; order = []; conflicts = []
for n in SPRITE_FROM:
    h = snip(n)
    for m in re.finditer(r'<symbol id="([^"]+)"[^>]*>.*?</symbol>', h, re.S):
        sid, txt = m.group(1), m.group(0)
        if sid in syms:
            if re.sub(r'\s+','',syms[sid]) != re.sub(r'\s+','',txt): conflicts.append((sid, n))
            continue
        syms[sid] = txt; order.append(sid)
LIB = {'ic-nav-liquidity':'products-and-services/liquidity-management.svg','ic-nav-fx':'products-and-services/fx.svg',
       'ic-nav-risk':'global-controls/security-secure.svg','ic-nav-trade':'products-and-services/trade-finance.svg',
       'ic-nav-reports':'informative/document-report.svg' ,'ic-nav-messages':'informative/contact-message.svg',
       'ic-nav-payments':'products-and-services/payments-and-transfers.svg','ic-nav-accounts':'products-and-services/account.svg',
       'ic-nav-home':'global-controls/home.svg','ic-nav-settings':'global-controls/settings.svg','ic-lib-download':'global-controls/download.svg'}
import glob
for sid, rel in LIB.items():
    f = glob.glob(K + '/assets/icons/**/' + os.path.basename(rel), recursive=True)
    f = [x for x in f if x.endswith(rel)] or f
    svg = open(f[0]).read()
    inner = re.search(r'<svg[^>]*>(.*)</svg>', svg, re.S).group(1).strip()
    inner = re.sub(r'fill="#[0-9A-Fa-f]{3,6}"', 'fill="currentColor"', inner)
    syms[sid] = '<symbol id="%s" viewBox="0 0 18 18">%s</symbol>' % (sid, inner); order.append(sid)
sprite = '<svg width="0" height="0" style="position:absolute" aria-hidden="true">\n' + '\n'.join(syms[s] for s in order) + '\n</svg>'

# ---------------- token manifest: union of the cut snippets' manifests ----------------
vars_union = {}
for n in sorted(set(r[1] for r in REGIONS)):
    vars_union.update(g.manifest_vars(snip(n)))

# ---------------- behaviour blocks (the chart engine), spliced whole ----------------
BEH = [('dv-render','Chart-bar'),('dv-render-bar','Chart-bar'),('dv-render-line','Chart-line'),('dv-render-donut','Chart-donut'),
       ('dv-render-stacked-area','Chart-stacked-area'),('dv-render-combo','Chart-combo'),('dv-render-scatter','Chart-scatter'),
       ('dv-render-bullet','Chart-bullet'),('dv-render-candlestick','Chart-candlestick'),('dv-render-histogram','Chart-histogram'),
       ('dv-render-boxplot','Chart-boxplot'),('dv-render-butterfly','Chart-butterfly-h'),('dv-render-sparkline','Chart-sparkline'),
       ('dv-behaviour','Chart-bar'),('dv-legend','Chart-bar'),('dv-donut-sweep','Chart-donut')]

def splice(region, name, kind, text):
    src = 'knowledge/snippets/%s.reference.html' % name
    return '%s\n%s\n%s' % (VR.splice_marker_start(region, src, kind), text, VR.splice_marker_end(region))

tpl = []
for tid, name, text, rec in REGIONS:
    body = splice('%s@%s' % (name, tid), name, 'markup', text) if rec else \
        '<!-- COPIED (not receipted) from knowledge/snippets/%s.reference.html: its meta declares a #script address; the demo script is not carried (see RUN-REPORT) -->\n%s' % (name, text)
    tpl.append('<template id="%s">\n%s\n</template>' % (tid, body))
beh = [splice('%s@%s' % (name, b), name, 'behaviour', g.extract_behaviour(snip(name), b)[0]) for b, name in BEH]

css = open(SRC + '/app.css').read()
data_js = open(SRC + '/data.js').read(); build_js = open(SRC + '/views.js').read(); wire_js = open(SRC + '/wire.js').read()
page = f"""<!DOCTYPE html>
<html lang="en" class="canon" data-apollo-theme="common" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Group CEO view — international banking prototype</title>
<link rel="stylesheet" href="../pack/knowledge/canon/canon.css">
<link rel="stylesheet" href="../pack/knowledge/canon/type.css">
<script type="application/json" id="token-manifest">{json.dumps({"vars": vars_union}, indent=1)}</script>
<script type="application/json" id="behaviour-manifest">{json.dumps(json.load(open(SRC + '/behaviour-manifest.json')), indent=1)}</script>
<style>
{css}
</style>
<script>
/* theme first, before paint: URL ?theme= wins, then the saved choice */
(function(){{try{{var q=new URLSearchParams(location.search).get('theme');var t=q||localStorage.getItem('ceo.theme');if(t==='dark'||t==='light'){{document.documentElement.setAttribute('data-theme',t);}}}}catch(e){{}}}}());
</script>
</head>
<body>
{sprite}
<div id="app"></div>
<noscript><p class="t-ed-body">This prototype builds its screens from the design system's templates with JavaScript. Turn JavaScript on to use it.</p></noscript>
{chr(10).join(tpl)}
<script>
{data_js}
</script>
<script>
{build_js}
</script>
{chr(10).join(beh)}
<script>
{wire_js}
</script>
</body>
</html>
"""
os.makedirs(W + '/out', exist_ok=True)
open(W + '/out/index.html', 'w', encoding='utf-8').write(page)
print('wrote', len(page), 'bytes;', len(REGIONS), 'parts;', len(beh), 'behaviour blocks; sprite', len(order), 'symbols; conflicts', conflicts)
