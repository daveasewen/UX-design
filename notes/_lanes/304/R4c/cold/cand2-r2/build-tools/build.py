"""Build the CEO prototype pages from the Apollo pack's own snippets (copy, never re-draw).
usage: python3 build.py <W>   (W holds pack/ and out/; tools/ holds app.js and data.json)"""
import json, os, re, sys, html as H

W = os.path.abspath(sys.argv[1]); PACK = os.path.join(W, 'pack'); K = os.path.join(PACK, 'knowledge')
OUT = os.path.join(W, 'out'); TOOLS = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, K)
import gen_provenance_receipt as G   # noqa: E402  (the pack's own extractor)
import _validate_receipt as VR       # noqa: E402  (the pack's own marker grammar)

DATA = json.load(open(os.path.join(TOOLS, 'data.json')))
APP = open(os.path.join(TOOLS, 'app.js'), encoding='utf-8').read()
REL = '../pack/knowledge/'
TAG_RE = re.compile(r"<(/?)([a-zA-Z][\w:-]*)([^>]*?)(/?)>", re.S)
_cache = {}


def snip(name):
    if name not in _cache:
        _cache[name] = open(os.path.join(K, 'snippets', name + '.reference.html'), encoding='utf-8').read()
    return _cache[name]


def live_body(name):
    b = re.search(r'<body[^>]*>(.*)</body>', snip(name), re.S).group(1)
    return re.sub(r'<!-- ===== APOLLO-DEMO (.*?) START.*?<!-- ===== APOLLO-DEMO \1 END ===== -->', '', b, flags=re.S)


def el(name, select):
    if select.count('.') > 1:          # compound class: exact class attribute, balanced from its tag
        b = live_body(name)
        i = b.find('class="%s"' % ' '.join(select.strip('.').split('.')))
        if i < 0:
            raise SystemExit('no %s in %s' % (select, name))
        st = b.rfind('<', 0, i)
        return balanced(b, st, re.match(r'<(\w+)', b[st:]).group(1))
    return G.extract_element(snip(name), select)[0]


def balanced(b, start, tag):
    mk = re.sub(r'<!--.*?-->', lambda m: ' ' * len(m.group(0)), b, flags=re.S)
    depth = 0
    for n in TAG_RE.finditer(mk, start):
        if n.group(2).lower() != tag:
            continue
        depth += -1 if n.group(1) else 1
        if depth == 0:
            return b[start:n.end()]
    raise SystemExit('unbalanced %s' % tag)


def figure(name, dvtype, idx=0):
    b = live_body(name); b = b[:b.find('<script')] if '<script' in b else b
    hits = [m.start() for m in re.finditer(r'<figure\s[^>]*data-dv-type="%s"' % re.escape(dvtype), b)]
    return balanced(b, hits[idx], 'figure')


def sprite(name):
    m = re.search(r'<svg[^>]*style="position:absolute"[^>]*>.*?</svg>', live_body(name), re.S)
    return m.group(0) if m else ''


def behaviour(bname):
    for f in sorted(os.listdir(os.path.join(K, 'snippets'))):
        h = snip(f[:-len('.reference.html')])
        if re.search(r'AUTO-BEHAVIOUR\s+%s\s+START' % re.escape(bname), h):
            return G.extract_behaviour(h, bname)[0], f[:-len('.reference.html')]
    raise SystemExit('no behaviour ' + bname)


def inline_script(name, idx=0):
    b = live_body(name)
    b = re.sub(r'<!-- ===== AUTO-BEHAVIOUR (\S+) START.*?AUTO-BEHAVIOUR \1 END ===== -->', '', b, flags=re.S)
    return re.findall(r'<script>(.*?)</script>', b, re.S)[idx]


class Page:
    def __init__(self):
        self.n = {}
        self.regions = []

    def splice(self, snippet, text, kind='markup', label=None):
        k = (label or snippet)
        self.n[k] = self.n.get(k, 0) + 1
        rid = '%s#%d' % (k, self.n[k])
        src = 'knowledge/snippets/%s.reference.html' % snippet
        return VR.splice_marker_start(rid, src, kind) + text + VR.splice_marker_end(rid)


def esc(s):
    return H.escape(str(s), quote=True)


# ------------------------------------------------------------------ navigation
NAV = [('index', 'Overview', 'ic-home', None),
       ('accounts', 'Accounts and transactions', 'ic-account', 'Cash and liquidity'),
       ('liquidity', 'Liquidity and funding', 'ic-liquidity', 'Cash and liquidity'),
       ('payments', 'Payments and approvals', 'ic-transfer', 'Cash and liquidity'),
       ('fx', 'FX and markets', 'ic-fx', 'Markets and risk'),
       ('risk', 'Risk and limits', 'ic-alert', 'Markets and risk'),
       ('trade', 'Trade finance', 'ic-trade', 'Markets and risk'),
       ('reports', 'Reports', 'ic-report', 'Insight and service'),
       ('messages', 'HSBC messages and service requests', 'ic-message', 'Insight and service'),
       ('settings', 'Settings', 'ic-settings', 'FOOT')]
EXTRA_ICONS = {'ic-liquidity': 'products-and-services/liquidity-management.svg', 'ic-fx': 'products-and-services/fx.svg',
               'ic-alert': 'informative/alert.svg', 'ic-trade': 'products-and-services/trade-finance.svg',
               'ic-report': 'media/document-report.svg', 'ic-message': 'media/contact-message.svg'}


def href(p):
    return p + '.html'


def nav_link(p, label, ic, current):
    cur = ' aria-current="page"' if current else ''
    return ('<li><a class="sn-link" href="%s" data-nav-link="%s"%s><span class="si" aria-hidden="true"><svg viewBox="0 0 18 18" aria-hidden="true">'
            '<use href="#%s"/></svg></span><span class="sn-label t-cm-label">%s</span></a></li>') % (href(p), href(p), cur, ic, esc(label))


def nav_body(page, gid):
    groups, order = {}, []
    for p, label, ic, grp in NAV:
        if grp == 'FOOT':
            continue
        g = grp or ''
        if g not in groups:
            groups[g] = []; order.append(g)
        groups[g].append(nav_link(p, label, ic, p == page))
    out = []
    for i, g in enumerate(order):
        if not g:
            out.append('              <div class="sn-group">\n                <ul>\n                  %s\n                </ul>\n              </div>' % '\n                  '.join(groups[g]))
        else:
            out.append(('              <div class="sn-group">\n                <span class="sn-group-label t-cm-caption" id="%s-g%d">%s</span>\n'
                        '                <ul aria-labelledby="%s-g%d">\n                  %s\n                </ul>\n              </div>') % (gid, i, esc(g), gid, i, '\n                  '.join(groups[g])))
    foot = nav_link('settings', 'Settings', 'ic-settings', page == 'settings')
    return '\n'.join(out), foot


def shell_parts(pg, page, title):
    sh = el('App-shell-side-nav', '#shell-wide')
    appbar = balanced(sh, sh.find('<header class="sh-appbar">'), 'header')
    appbar = appbar.replace('aria-controls="sheet-wide"', 'aria-controls="sheet-wide"')
    nav = balanced(sh, sh.find('<nav class="sn" aria-label="Main" id="nav-wide">'), 'nav')
    body, foot = nav_body(page, 'nw')
    nav = re.sub(r'(<div class="sn-body" id="nav-wide-body">).*?(\n            </div>\n            <div class="sn-foot">)', lambda m: m.group(1) + '\n' + body + m.group(2), nav, flags=re.S)
    nav = re.sub(r'(<div class="sn-foot">\s*<ul>\s*).*?(\s*</ul>)', lambda m: m.group(1) + foot + m.group(2), nav, flags=re.S)
    nav = nav.replace('<span class="sn-brand t-cm-label">Business banking</span>', '<span class="sn-brand t-cm-label">Group treasury</span>')
    crumbs = balanced(sh, sh.find('<nav class="sh-crumbs"'), 'nav')
    if page == 'index':
        crumbs = re.sub(r'<ol>.*?</ol>', '<ol>\n                <li><span class="t-ed-body-small em" aria-current="page">Overview</span></li>\n              </ol>', crumbs, flags=re.S)
    else:
        crumbs = re.sub(r'<ol>.*?</ol>', ('<ol>\n                <li><a class="crumb t-ed-body-small" href="index.html" data-nav-link="index.html">Overview</a></li>\n'
                                          '                <li><span class="sep t-ed-body-small" aria-hidden="true">/</span><span class="t-ed-body-small em" aria-current="page">%s</span></li>\n              </ol>') % esc(title), crumbs, flags=re.S)
    footer = balanced(sh, sh.find('<footer class="sh-foot"'), 'footer')
    sheet = balanced(sh, sh.find('<div class="sh-sheet"'), 'div')
    sbody, sfoot = nav_body(page, 'ns')
    sheet = re.sub(r'(<div class="sn-body">).*?(\n            </div>\n            <div class="sn-foot">)', lambda m: m.group(1) + '\n' + sbody + m.group(2), sheet, flags=re.S)
    sheet = re.sub(r'(<div class="sn-foot">\s*<ul>\s*).*?(\s*</ul>)', lambda m: m.group(1) + sfoot + m.group(2), sheet, flags=re.S)
    sheet = sheet.replace('<span class="sn-brand t-cm-label">Business banking</span>', '<span class="sn-brand t-cm-label">Group treasury</span>')
    skip = balanced(sh, sh.find('<a class="sh-skip'), 'a')
    appbar = appbar.replace('src="../assets/logos/', 'src="../pack/knowledge/assets/logos/')
    S = lambda t: pg.splice('App-shell-side-nav', t)
    return S(skip), S(appbar), S(nav), S(crumbs), S(footer), S(sheet)


def icon_symbols():
    out = []
    for sid, path in EXTRA_ICONS.items():
        svg = open(os.path.join(K, 'assets', 'icons', path), encoding='utf-8').read()
        p = re.search(r'<path[^>]*/>', svg).group(0)
        out.append('<symbol id="%s" viewBox="0 0 18 18">%s</symbol>' % (sid, p))
    return '<svg width="0" height="0" style="position:absolute" aria-hidden="true">\n    %s\n  </svg>' % '\n    '.join(out)


# ------------------------------------------------------------------ components
def seg(pg, attr, label, items, pressed, size='s'):
    s = el('Segmented-control', '.seg.s')
    btns = ''.join('\n    <button type="button" data-value="%s" aria-pressed="%s">%s</button>' % (v, 'true' if v == pressed else 'false', esc(t)) for v, t in items)
    s = re.sub(r'(<span class="ind" aria-hidden="true"></span>).*?(\n\s*</div>)$', lambda m: m.group(1) + btns + m.group(2), s, flags=re.S)
    s = s.replace('aria-label="Period"', 'aria-label="%s" %s' % (esc(label), attr), 1)
    return '<div class="cn-segmented-control">' + pg.splice('Segmented-control', s) + '</div>'


def dropdown(pg, key, label, options):
    d = el('Dropdown', '.dd.boxed')
    uid = 'dd-' + key
    tick = re.search(r'<svg data-bespoke="neutral selection checkmark[^>]*>.*?</svg>', d, re.S).group(0)
    opts = ''.join('\n          <li class="opt" role="option" data-value="%s" aria-selected="false" tabindex="-1">%s %s</li>' % (esc(v), esc(t), tick) for v, t in options)
    d = re.sub(r'(<ul class="menu"[^>]*>).*?(\n\s*</ul>)', lambda m: m.group(1) + opts + m.group(2), d, flags=re.S)
    d = d.replace('ddLabel2', uid + '-l').replace('ddTrigger2', uid + '-t').replace('ddMenu2', uid + '-m')
    d = d.replace('Country of residence', esc(label)).replace('<span class="ddval">United Kingdom</span>', '<span class="ddval">%s</span>' % esc(options[0][1]))
    d = d.replace('<div class="dd boxed">', '<div class="dd boxed" data-filter="%s">' % key, 1)
    return '<div class="cn-dropdown">' + pg.splice('Dropdown', d) + '</div>'


def button(pg, text, variant, attrs):
    b = '<button class="btn %s" type="button" %s>%s</button>' % (variant, attrs, esc(text))
    return '<div class="cn-button">' + pg.splice('Button', b) + '</div>'


def kpi_tile(pg, tid):
    k = el('Kpi-tile', '.kpi-tile')
    k = k.replace('<div class="kpi-tile" role="group"', '<div class="kpi-tile" id="%s" role="group"' % tid, 1)
    return pg.splice('Kpi-tile', k)


CHART = {  # our type -> (snippet, figure dv-type, scope, figure index)
    'column': ('Chart-bar', 'column', 'cn-chart-bar', 1), 'bar': ('Chart-bar', 'bar', 'cn-chart-bar', 0),
    'grouped-column': ('Chart-bar', 'grouped-column', 'cn-chart-bar', 0), 'stacked-column': ('Chart-bar', 'stacked-column', 'cn-chart-bar', 0),
    'line': ('Chart-line', 'line', 'cn-chart-line', 0), 'multiline': ('Chart-line', 'multiline', 'cn-chart-line', 0),
    'stacked-area': ('Chart-stacked-area', 'stacked-area', 'cn-chart-stacked-area', 0), 'donut': ('Chart-donut', 'donut', 'cn-chart-donut', 0),
    'pie': ('Chart-pie', 'pie', 'cn-chart-pie', 0), 'combo': ('Chart-combo', 'combo', 'cn-chart-combo', 0),
    'scatter': ('Chart-scatter', 'scatter', 'cn-chart-scatter', 0), 'histogram': ('Chart-histogram', 'histogram', 'cn-chart-histogram', 0),
    'boxplot': ('Chart-boxplot', 'boxplot', 'cn-chart-boxplot', 0), 'bullet': ('Chart-bullet', 'bullet', 'cn-chart-bullet', 0),
    'butterfly-h': ('Chart-butterfly-h', 'butterfly-h', 'cn-chart-butterfly-h', 0), 'butterfly-v': ('Chart-butterfly-v', 'butterfly-v', 'cn-chart-butterfly-v', 0),
    'candlestick': ('Chart-candlestick', 'candlestick', 'cn-chart-candlestick', 0), 'spark': ('Chart-sparkline', 'spark', 'cn-chart-sparkline', 0),
}
PARTIALS = {'Chart-bar': ['dv-behaviour', 'dv-render', 'dv-render-bar'], 'Chart-line': ['dv-behaviour', 'dv-legend', 'dv-render', 'dv-render-line'],
            'Chart-stacked-area': ['dv-behaviour', 'dv-legend', 'dv-render', 'dv-render-stacked-area'],
            'Chart-donut': ['dv-behaviour', 'dv-legend', 'dv-donut-sweep', 'dv-render', 'dv-render-donut'],
            'Chart-pie': ['dv-behaviour', 'dv-legend', 'dv-render', 'dv-render-donut'],
            'Chart-combo': ['dv-behaviour', 'dv-legend', 'dv-render', 'dv-render-bar', 'dv-render-line', 'dv-render-combo'],
            'Chart-scatter': ['dv-behaviour', 'dv-render', 'dv-render-scatter'], 'Chart-histogram': ['dv-behaviour', 'dv-render', 'dv-render-histogram'],
            'Chart-boxplot': ['dv-behaviour', 'dv-render', 'dv-render-boxplot'], 'Chart-bullet': ['dv-behaviour', 'dv-render', 'dv-render-bullet'],
            'Chart-butterfly-h': ['dv-behaviour', 'dv-render', 'dv-render-butterfly', 'dv-legend'],
            'Chart-butterfly-v': ['dv-behaviour', 'dv-render', 'dv-render-butterfly', 'dv-legend'],
            'Chart-candlestick': ['dv-behaviour', 'dv-render', 'dv-render-candlestick'], 'Chart-sparkline': ['dv-behaviour', 'dv-render', 'dv-render-sparkline']}
ORDER = ['dv-behaviour', 'dv-legend', 'dv-donut-sweep', 'dv-render', 'dv-render-bar', 'dv-render-line', 'dv-render-combo', 'dv-render-donut',
         'dv-render-stacked-area', 'dv-render-scatter', 'dv-render-histogram', 'dv-render-boxplot', 'dv-render-bullet', 'dv-render-butterfly',
         'dv-render-candlestick', 'dv-render-sparkline']


def chart(pg, cid, ctype, title, caption, legend=False):
    snippet, dvt, scope, ix = CHART[ctype]
    f = figure(snippet, dvt, ix)
    pg.partials.update(PARTIALS[snippet])
    if legend:
        pg.partials.add('dv-legend')
    ids = re.findall(r'\sid="([^"]+)"', f)
    for k, old in enumerate(ids):
        # keep each id's role suffix (-h, -tbl, -legend, -live): dv-legend finds its live region by
        # rewriting '-legend' to '-live' in the host id, so the suffix is part of the contract
        if k == 0 and f.find('id="%s"' % old) < f.find('>'):
            new = cid
        elif '-' in old:
            new = cid + old[old.index('-'):]
        else:
            new = '%s-x%d' % (cid, k)
        f = re.sub(r'(?<=["\s])%s(?=["\s])' % re.escape(old), new, f)
    if not re.match(r'<figure[^>]*\sid=', f):
        f = f.replace('<figure ', '<figure id="%s" ' % cid, 1)
    f = re.sub(r'data-lockup-title="[^"]*"', 'data-lockup-title="%s"' % esc(title), f, 1)
    f = re.sub(r'(<h3 class="dv-title t-cm-section-label">)[^<]*(</h3>)', lambda m: m.group(1) + esc(title) + m.group(2), f, 1)
    f = re.sub(r'(<figcaption[^>]*>)[^<]*(</figcaption>)', lambda m: m.group(1) + esc(caption) + m.group(2), f, 1)
    f = re.sub(r'(<caption>)[^<]*(</caption>)', lambda m: m.group(1) + esc(caption) + m.group(2), f)
    f = re.sub(r'(<div class="dv-tablepanel"[^>]*aria-label=")[^"]*(")', lambda m: m.group(1) + esc(caption) + ', data table' + m.group(2), f)
    f = re.sub(r'<tbody>.*?</tbody>', '<tbody></tbody>', f, flags=re.S)
    f = re.sub(r'(<svg class="dv-svg[^>]*aria-label=")[^"]*(")', lambda m: m.group(1) + esc(caption) + m.group(2), f, 1)
    f = re.sub(r'<svg class="dv-svg([^"]*)"([^>]*)>.*?</svg>', lambda m: '<svg class="dv-svg%s"%s></svg>' % (m.group(1), m.group(2)), f, count=1, flags=re.S)
    # controls the engine cannot drive for our data are left out: overlay toggles; view switches except the donut/pie value|percent
    f = re.sub(r'<div class="dv-toggle-seg">.*?</div>', '', f, flags=re.S)
    if ctype not in ('donut', 'pie'):
        f = re.sub(r'<div class="seg sm"[^>]*>.*?</div>', '', f, flags=re.S)
    # any baked annotation or empty-state siblings of the plot are left to the engine
    f = re.sub(r'<p class="dv-sr"[^>]*>.*?</p>', lambda m: m.group(0), f, flags=re.S)
    if not legend:
        f = re.sub(r'\s*<ul class="dv-leg[^"]*"[^>]*>.*?</ul>', '', f, flags=re.S)
    return '<div class="%s">' % scope + pg.splice(snippet, f) + '</div>'


def section_head(pg, hid, text, badge_id=None, link=None):
    h = '<div class="l-row" data-justify="between" data-align="baseline">\n        <div class="l-row" data-gap="s" data-align="baseline">\n          <h2 id="%s" class="t-ed-heading-4">%s</h2>' % (hid, esc(text))
    if badge_id:
        h += '\n          <span class="badge standalone" id="%s" aria-label="">0</span>' % badge_id
    h += '\n        </div>'
    if link:
        a = el('Section-heading-lockup', '.arrow')
        a = a.replace('href="#"', 'href="%s" data-nav-link="%s"' % (link[0], link[0])).replace('>View all<', '>%s<' % esc(link[1]))
        h += '\n        ' + a
    h += '\n      </div>'
    return '<div class="cn-section-heading-lockup">' + pg.splice('Section-heading-lockup', h) + '</div>'


def list_items(pg, lid):
    return '<div class="cn-list-items">' + pg.splice('List-items', '<ul class="list" id="%s"></ul>' % lid) + '</div>'


def search_field(pg, sid, label):
    s = el('Search-field', '.search.boxed')
    s = s.replace('aria-label="Search transactions" placeholder="Search transactions" value="Statements"', 'id="%s" aria-label="%s" placeholder="%s" value=""' % (sid, esc(label), esc(label)))
    return '<div class="cn-search-field">' + pg.splice('Search-field', s) + '</div>'


def pagination(pg, pid):
    p = el('Pagination', '.pg')
    p = re.sub(r'<ul>.*?</ul>', '<ul></ul>', p, flags=re.S).replace('aria-label="Pagination"', 'id="%s" aria-label="Pages"' % pid)
    return '<div class="cn-pagination">' + pg.splice('Pagination', p) + '</div>'


def data_grid(pg, title, labels, noun, colfilters):
    g = el('Data-grid', '.dg')
    g = g.replace('<span class="t-cm-section-label" id="dgTitle">Transactions</span>', '<span class="t-cm-section-label" id="dgTitle">%s</span>' % esc(title))
    g = g.replace('aria-label="Filter transactions"', 'aria-label="Filter %s"' % esc(noun)).replace('placeholder="Filter transactions — press enter to apply"', 'placeholder="Filter %s — press enter to apply"' % esc(noun))
    for key, lab in zip(['Date', 'Payee', 'Reference', 'Type', 'Amount'], labels[:5]):
        g = g.replace('<span class="lbl">%s</span>' % key, '<span class="lbl">%s</span>' % esc(lab))
    g = g.replace('<span class="glabel t-cm-caption">Transaction detail</span>', '<span class="glabel t-cm-caption">%s</span>' % esc(labels[5]))
    if not colfilters:
        g = re.sub(r'\s*<button class="colf".*?</button>', '', g, flags=re.S)
        g = re.sub(r'\s*<div class="colmenu".*?</div>', '', g, flags=re.S)
    hint = el('Data-grid', '#dgHint'); status = el('Data-grid', '#dgStatus')
    return '<div class="cn-data-grid">' + pg.splice('Data-grid', g + '\n  ' + hint + '\n  ' + status) + '</div>'


def grid_script():
    s = inline_script('Data-grid')
    a = s.index('const DATA = [') + len('const DATA = ')
    b = s.index('];', a) + 1
    return s[:a] + 'window.CEO_ROWS' + s[b:]


def overlays(pg):
    scrim = el('Drawer', '#scrim'); sheet = el('Drawer', '#sheet')
    sheet = re.sub(r'(<div class="sheet-body" id="dbody">).*?(</div>)', lambda m: m.group(1) + m.group(2), sheet, flags=re.S)
    sheet = re.sub(r'<div class="sheet-foot">.*?</div>', '<div class="sheet-foot" id="dfoot"></div>', sheet, flags=re.S)
    drawer = '<div class="cn-drawer">' + pg.splice('Drawer', scrim + '\n  ' + sheet) + '</div>'
    ta = el('Textarea', '#live')
    ta = ta.replace('id="live"', 'id="t1-group"').replace('Notes for the finance team', 'Audit note')
    ta = re.sub(r'(<textarea[^>]*>)[^<]*(</textarea>)', lambda m: m.group(1) + m.group(2), ta).replace('78/300', '0/300')
    ta = ta.replace('<p class="tx-help t-ed-body-small" id="t1-help">Visible to approvers only.</p>', '<p class="tx-help t-ed-body-small" id="t1-help">Saved to the audit trail.</p>')
    err = el('Input-fields', '.err-msg') if False else None
    modal = el('Modals', '#overlay')
    modal = modal.replace('aria-labelledby="dtitle" aria-describedby="dbody"', 'aria-labelledby="mtitle" aria-describedby="mbody"')
    modal = modal.replace('id="close"', 'id="mclose"').replace('<h2 id="dtitle">Confirm payment</h2>', '<h2 id="mtitle">Confirm</h2>')
    modal = re.sub(r'<p id="dbody">.*?</p>', '<p id="mbody"></p>', modal, flags=re.S)
    note = ('<div class="cn-textarea">' + ta + '\n        <div class="cn-input-fields"><div class="field is-error"><div class="err-msg" id="t1-err" hidden><span class="ic" aria-hidden="true">'
            '<svg class="icn" viewBox="0 0 18 18"><use href="#ic-error"/></svg></span><p>Add an audit note.</p></div></div></div></div>')
    modal = modal.replace('<div class="actions">', note + '\n      <div class="actions">', 1)
    modal = modal.replace('id="confirm"', 'id="mconfirm"').replace('>Confirm payment<', '>Confirm<').replace('id="cancel"', 'id="mcancel"')
    modals = '<div class="cn-modals">' + pg.splice('Modals', modal) + '</div>'
    toast = '<div class="cn-toast">' + pg.splice('Toast', el('Toast', '.toast-region')) + '</div>'
    return drawer + '\n' + modals + '\n' + toast


def alert_info(pg, text):
    a = re.search(r'<div class="alert info" role="status" data-carries="symbol label">.*?</div>', live_body('Alert'), re.S).group(0)
    a = re.sub(r'<p class="main t-ed-body">.*?</p>', '<p class="main t-ed-body">%s</p>' % text, a, flags=re.S)
    a = re.sub(r'<button class="x".*?</button>', '', a, flags=re.S)
    return '<div class="cn-alert">' + pg.splice('Alert', a) + '</div>'


def tabs(pg, items):
    t = el('Tabs', '.tabs')
    btns = ''.join('\n      <button class="tab" role="tab" id="rk-tab-%s" data-tab="%s" aria-selected="%s" aria-controls="rk-panel" tabindex="%s">%s</button>' % (v, v, 'true' if i == 0 else 'false', 0 if i == 0 else -1, esc(l)) for i, (v, l) in enumerate(items))
    t = re.sub(r'(<div class="tablist"[^>]*>).*?(\n\s*<div class="overflow" hidden>)', lambda m: m.group(1) + btns + m.group(2), t, flags=re.S)
    t = t.replace('aria-label="Account views"', 'aria-label="Risk views"')
    t = re.sub(r'\s*<div class="tabpanel.*?</div>', '', t, flags=re.S)
    t = re.sub(r'\s*<div class="panel.*?</div>', '', t, flags=re.S)
    return '<div class="cn-tabs">' + pg.splice('Tabs', t) + '</div>'


def switch(pg, sid, key, label):
    s = '<div class="field"><input type="checkbox" role="switch" id="%s" data-notify="%s"><label for="%s"><span class="switch"><span class="thumb"></span></span> %s</label></div>' % (sid, key, sid, esc(label))
    return pg.splice('Selection-controls', s)


# ------------------------------------------------------------------ page composition
def tile(c, inner, extra=''):
    return '<div class="c-bento__tile stat-card" data-c="%s"%s>%s</div>' % (c, extra, inner)


def group(role, label, tiles, extra_cls=''):
    return ('<section class="c-bento__tile c-bento tpl-group tpl-group-%s%s" data-bento-role="dashboard" data-c="6" aria-label="%s">\n'
            '              <div class="c-bento__grid">\n                %s\n              </div>\n            </section>') % (role, extra_cls, esc(label), '\n                '.join(tiles))


def wall(label, groups):
    return ('<section class="ceo-wall" aria-label="%s"><div class="cn-template-dashboard-bento"><div class="tpl-page">\n'
            '        <div class="c-bento tpl-wall" data-bento-role="dashboard" aria-label="%s">\n          <div class="c-bento__grid">\n            %s\n          </div>\n        </div>\n      </div></div></section>') % (esc(label), esc(label), '\n            '.join(groups))


def stack(*parts):
    return '<div class="ceo-stack">' + ''.join(parts) + '</div>'


def grid_tile(pg, title, labels, noun, colf, extra_bar=''):
    return tile(6, stack(extra_bar, data_grid(pg, title, labels, noun, colf)) if extra_bar else data_grid(pg, title, labels, noun, colf))


def build_page(page, title, intro):
    pg = Page(); pg.partials = set()
    skip, appbar, navc, crumbs, footer, sheet = shell_parts(pg, page, title)
    ent_opts = [('all', 'All entities')] + [(e['id'], e['name']) for e in DATA['entities']]
    reg_opts = [('all', 'All regions')] + [(r['id'], r['name']) for r in DATA['regions']]
    filters = ('<div class="ceo-filters" role="group" aria-label="Shared filters">' + dropdown(pg, 'entity', 'Entity', ent_opts) + dropdown(pg, 'region', 'Region', reg_opts) +
               seg(pg, 'data-period-seg', 'Period', [('7', '7 days'), ('14', '14 days'), ('30', '30 days')], '30') +
               button(pg, 'Reset filters', 'tertiary', 'data-action="reset-filters"') + '</div>')
    theme = ('<div class="ceo-actions">' + button(pg, 'Export CSV', 'secondary', 'data-action="export"') +
             seg(pg, 'data-theme-seg', 'Theme', [('light', 'Light'), ('dark', 'Dark')], 'light') + '</div>')
    body = CONTENT[page](pg)
    main = ('<main class="sh-main" id="main-wide">\n              <div class="sh-title">\n                <h1 class="t-ed-heading-2">%s</h1>\n                %s\n              </div>\n'
            '              <p class="t-ed-body-small" id="scope-note">All entities · last 30 days</p>\n              %s\n              %s\n            </main>') % (esc(title), theme, filters, body)
    shell = ('<div class="cn-app-shell-side-nav" id="app-shell">\n      <div class="sh" data-nav="auto" id="shell-wide">\n        %s\n        %s\n        <div class="sh-body">\n          %s\n'
             '          <div class="sh-content">\n            %s\n            %s\n            %s\n          </div>\n        </div>\n        <div class="sh-scrim" data-scrim="shell-wide"></div>\n        %s\n      </div>\n    </div>') % (
        skip, appbar, navc, crumbs, main, footer, sheet)
    sprites = '\n  '.join([sprite('App-shell-side-nav'), icon_symbols(), sprite('Data-grid'), sprite('Kpi-tile'), sprite('Toast'), sprite('Input-fields'), sprite('Section-heading-lockup')])
    scripts = []
    for bname in [b for b in ORDER if b in pg.partials]:
        blk, src = behaviour(bname)
        scripts.append(pg.splice(src, blk, kind='behaviour', label='behaviour-' + bname))
    app = APP.replace('/*__DATA__*/null', json.dumps(DATA, separators=(',', ':')))
    scripts.append('<script>\n' + app + '\n</script>')
    if pg.has_grid:
        scripts.append('<script>' + grid_script() + '</script>')
    scripts.append('<script>' + inline_script('Textarea') + '</script>')
    scripts.append('<script>' + inline_script('App-shell-side-nav') + '</script>')
    scripts.append('<script>\n  /* after the component scripts: restore the grid\'s saved sort/page and wire row detail */\n  if (window.__ceoAfterGrid) window.__ceoAfterGrid();\n</script>')
    beh_manifest = {'component': 'page:' + page, '$note': 'Behaviour addresses this page starts from (s258-D1: carried verbatim or extended, and said which).',
                    'addresses': [
                        {'component': 'data-grid', 'script': 'knowledge/snippets/Data-grid.reference.html#script', 'how': 'extended: the DATA literal is replaced by window.CEO_ROWS (the page model), every other byte verbatim'} if pg.has_grid else None,
                        {'component': 'textarea', 'script': 'knowledge/snippets/Textarea.reference.html#script', 'how': 'verbatim'},
                        {'component': 'app-shell-side-nav', 'script': 'snippet inline script (nav toggle, off-canvas sheet)', 'how': 'verbatim'},
                        {'component': 'charts', 'script': 'knowledge/canon/dv-render.js', 'partial': sorted(pg.partials), 'how': 'verbatim AUTO-BEHAVIOUR blocks'} if pg.partials else None,
                        {'component': 'drawer · modals · toast · dropdown · tabs · segmented-control · list-items · pagination · search-field', 'script': None,
                         'how': 'authored in the page script, following each snippet\'s own mechanics (meta behaviour is null for these)'}]}
    beh_manifest['addresses'] = [a for a in beh_manifest['addresses'] if a]
    tok_manifest = {'$note': 'Tokens the page\'s own placement style reads (placement only — no component is restyled).',
                    '--surface-subtle': 'surface/subtle (bentoBg = grey, the lightest grey section ground)', '--gap-fixed-content-xsmall': 'gap/fixed/content/xsmall (4px — the wall rim equals the inner bento gutter)',
                    '--padding-fixed-medium': 'padding/fixed/medium'}
    doc = '''<!DOCTYPE html>
<html lang="en" class="canon" data-apollo-theme="common" data-theme="light">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>%(title)s — CEO view · HSBC corporate banking (prototype)</title>
  <link rel="stylesheet" href="%(rel)scanon/canon.css">
  <link rel="stylesheet" href="%(rel)scanon/type.css">
  <script>
    /* theme before first paint: URL wins, then the saved choice (per viewer, localStorage) */
    (function () { var t = 'light'; try { var s = JSON.parse(localStorage.getItem('ceo-hsbc-prototype-v1') || '{}'); if (s.theme) t = s.theme; } catch (e) {}
      var q = new URLSearchParams(location.search).get('theme'); if (q === 'dark' || q === 'light') t = q;
      document.documentElement.setAttribute('data-theme', t); }());
  </script>
  <script type="application/json" id="token-manifest">
%(tok)s
  </script>
  <script type="application/json" id="behaviour-manifest">
%(beh)s
  </script>
  <style>
    /* PLACEMENT ONLY (rule 3a): where parts sit and the section ground. No component is sized or restyled. */
    .ceo-filters{display:flex; flex-wrap:wrap; align-items:flex-end; gap:var(--padding-fixed-medium);}
    .ceo-wall{background:var(--surface-subtle); padding:var(--gap-fixed-content-xsmall);}
    .ceo-stack{display:flex; flex-direction:column; gap:var(--padding-fixed-medium);}
    .ceo-actions{display:flex; flex-wrap:wrap; align-items:center; gap:var(--padding-fixed-medium);}
    .ceo-bar{display:flex; flex-wrap:wrap; align-items:center; justify-content:space-between; gap:var(--padding-fixed-medium);}
  </style>
</head>
<body data-page="%(page)s">
  %(sprites)s
  %(shell)s
  %(overlays)s
  %(scripts)s
</body>
</html>
''' % {'title': esc(title), 'rel': REL, 'tok': json.dumps(tok_manifest, indent=1), 'beh': json.dumps(beh_manifest, indent=1), 'page': page, 'sprites': sprites,
       'shell': shell, 'overlays': overlays(pg), 'scripts': '\n  '.join(scripts)}
    open(os.path.join(OUT, href(page)), 'w', encoding='utf-8').write(doc)
    return pg


# ------------------------------------------------------------------ the ten screens
def c_index(pg):
    pg.has_grid = False
    lead = group('lead', 'Financial resilience — can we fund our plans?', ['<div class="c-bento__tile" data-c="1">' + '<div class="cn-kpi-tile">' + kpi_tile(pg, k) + '</div></div>' for k in ('kpi-cash', 'kpi-liq', 'kpi-head', 'kpi-flow')])
    ev = group('evidence', 'Risk outlook — where are we exposed?', [
        tile(3, chart(pg, 'ov-region', 'stacked-column', 'Exposure by region — select a column for its positions', 'Exposure by region and currency, £ millions', legend=True)),
        tile(3, chart(pg, 'ov-ccy', 'bar', 'Exposure by currency — select a bar for its positions', 'Exposure by currency, £ millions')),
        tile(3, chart(pg, 'ov-limits', 'bullet', 'Limit utilisation by region', 'Limit utilisation by region, per cent of limit')),
        tile(3, chart(pg, 'ov-trend', 'stacked-area', 'Exposure trend by region', 'Exposure by region over the period, £ millions', legend=True))])
    ctx = group('context', 'Decisions — what needs my attention?', [
        tile(3, stack(section_head(pg, 'dec-pay-h', 'Pending approvals', 'dec-pay-count', ('payments.html', 'All payments')), list_items(pg, 'dec-pay'))),
        tile(3, stack(section_head(pg, 'dec-exc-h', 'Material risk exceptions', 'dec-exc-count', ('risk.html', 'All exceptions')), list_items(pg, 'dec-exc')))])
    return wall('Overview dashboard', [lead, ev, ctx])


def c_accounts(pg):
    pg.has_grid = True
    ev = group('evidence', 'Where the cash sits', [
        tile(6, chart(pg, 'ac-bal', 'multiline', 'Cash balance by region', 'Cash balance by region, £ millions', legend=True)),
        tile(6, chart(pg, 'ac-type', 'grouped-column', 'Money in and out by type', 'Money in and out by transaction type, £ millions', legend=True)),
        tile(6, chart(pg, 'ac-ccy', 'pie', 'Closing cash by currency', 'Closing cash by currency, £ millions', legend=True))])
    rec = group('evidence', 'Transactions', [grid_tile(pg, 'Transactions', ['Date', 'Counterparty', 'Reference', 'Type', 'Amount', 'Transaction detail'], 'transactions', True,
                                                    button(pg, 'Open selected row', 'tertiary', 'data-action="open-selected"'))])
    return wall('Accounts and transactions', [ev, rec])


def c_liquidity(pg):
    pg.has_grid = True
    ev = group('evidence', 'Liquidity position', [
        tile(6, chart(pg, 'lq-combo', 'combo', 'Daily net cash flow and liquidity cover', 'Daily net cash flow and liquidity cover', legend=True)),
        tile(6, chart(pg, 'lq-mix', 'donut', 'Sources of available liquidity', 'Sources of available liquidity today, £ millions', legend=True)),
        tile(6, chart(pg, 'lq-fac', 'bullet', 'Facility utilisation', 'Facility utilisation, per cent drawn'))])
    rec = group('evidence', 'Facilities', [grid_tile(pg, 'Facilities by maturity', ['Maturity', 'Entity', 'Facility · lender', 'Type', 'Undrawn', 'Facility detail'], 'facilities', False,
                                                    button(pg, 'Open selected row', 'tertiary', 'data-action="open-selected"'))])
    return wall('Liquidity and funding', [ev, rec])


def c_payments(pg):
    pg.has_grid = True
    ev = group('evidence', 'Payment flows', [
        tile(3, chart(pg, 'py-daily', 'column', 'Payment value created per day', 'Payment value created per day, £ millions')),
        tile(3, chart(pg, 'py-hist', 'histogram', 'Payment size distribution', 'Number of payments by size band')),
        tile(6, chart(pg, 'py-status', 'donut', 'Payments by status', 'Payments by status, count', legend=True)),
        tile(6, chart(pg, 'py-region', 'grouped-column', 'Pending versus released by region', 'Pending versus released value by region, £ millions', legend=True))])
    bar = '<div class="ceo-bar"><p class="t-ed-body-small" id="py-pending">0 awaiting your approval</p>' + button(pg, 'Review selected payment', 'primary', 'data-action="open-selected"') + '</div>'
    rec = group('evidence', 'Payments', [grid_tile(pg, 'Payments', ['Created', 'Beneficiary', 'Payment · purpose', 'Status', 'Amount', 'Payment detail'], 'payments', True, bar)])
    return wall('Payments and approvals', [ev, rec])


def c_fx(pg):
    pg.has_grid = True
    rates = ('<div class="ceo-stack"><h2 class="t-ed-heading-4" id="fx-rates-h">Illustrative rates used in this prototype</h2><div class="cn-summary">' +
             pg.splice('Summary', '<dl class="summary" id="fx-rates" aria-labelledby="fx-rates-h"></dl>') + '</div>' +
             alert_info(pg, '<strong class="em">Not live rates.</strong> GBP per one unit of currency, fixed for this prototype. Every GBP figure uses them.') + '</div>')
    ev = group('evidence', 'Markets', [
        tile(6, chart(pg, 'fx-candle', 'candlestick', 'GBP/USD daily range', 'GBP/USD daily open, high, low and close (illustrative)')),
        tile(6, chart(pg, 'fx-index', 'multiline', 'Cumulative currency bought', 'Cumulative currency bought over the period, £ millions', legend=True)),
        tile(6, chart(pg, 'fx-fly', 'butterfly-h', 'Currency bought versus sold', 'Currency bought versus sold against sterling, £ millions', legend=True)),
        tile(6, rates)])
    rec = group('evidence', 'FX deals', [grid_tile(pg, 'FX deal blotter', ['Trade date', 'Deal', 'Deal id · bank', 'Type · status', 'GBP equivalent', 'Deal detail'], 'deals', False,
                                                  button(pg, 'Open selected deal', 'tertiary', 'data-action="open-selected"'))])
    return wall('FX and markets', [ev, rec])


def c_risk(pg):
    pg.has_grid = True
    ev = group('evidence', 'Exposure against limits', [
        tile(3, chart(pg, 'rk-limits', 'grouped-column', 'Exposure against limit by region', 'Exposure against limit by region, £ millions', legend=True)),
        tile(3, chart(pg, 'rk-box', 'boxplot', 'Spread of daily exposure', 'Spread of daily exposure over the period by region, £ millions')),
        tile(6, chart(pg, 'rk-scatter', 'scatter', 'Counterparty concentration', 'Counterparty concentration, £ millions'))])
    bar = '<div class="ceo-bar">' + tabs(pg, [('exceptions', 'Risk exceptions'), ('positions', 'Positions and limits')]) + button(pg, 'Open selected row', 'tertiary', 'data-action="open-selected"') + '</div>'
    rec = group('evidence', 'Exceptions and positions', ['<div class="c-bento__tile stat-card" data-c="6" id="rk-panel" role="tabpanel" aria-labelledby="rk-tab-exceptions">' +
                                                        stack(bar, data_grid(pg, 'Risk exceptions', ['Raised', 'Counterparty', 'Exception', 'Severity · status', 'Over limit', 'Exception detail'], 'records', False)) + '</div>'])
    return wall('Risk and limits', [ev, rec])


def c_trade(pg):
    pg.has_grid = True
    ev = group('evidence', 'Trade book', [
        tile(6, chart(pg, 'tf-fly', 'butterfly-v', 'Import versus export by region', 'Import versus export instruments by region, £ millions', legend=True)),
        tile(6, chart(pg, 'tf-stack', 'stacked-column', 'Instrument value by status', 'Instrument value by status and type, £ millions', legend=True))])
    rec = group('evidence', 'Instruments', [grid_tile(pg, 'Letters of credit, guarantees and collections', ['Expiry', 'Counterparty', 'Instrument', 'Status', 'Amount', 'Instrument detail'], 'instruments', False,
                                                     button(pg, 'Open selected row', 'tertiary', 'data-action="open-selected"'))])
    return wall('Trade finance', [ev, rec])


def list_block(pg, lid, head, sorts, search_label, head_extra=''):
    sort = seg(pg, 'data-list-sort="%s"' % lid, 'Sort', sorts, sorts[0][0])
    return stack('<div class="ceo-bar">' + section_head(pg, lid + '-h', head) + head_extra + '</div>',
                 '<div class="ceo-bar">' + search_field(pg, lid + '-q', search_label) + sort + '</div>',
                 '<p class="t-cm-caption" id="%s-count" aria-live="polite"></p>' % lid, list_items(pg, lid), pagination(pg, lid + '-pg'))


def c_reports(pg):
    pg.has_grid = False
    ev = group('evidence', 'Reporting activity', [
        tile(6, chart(pg, 'rp-runs', 'column', 'Reports generated per day', 'Reports generated per day')),
        tile(6, chart(pg, 'rp-cat', 'pie', 'Catalogue by category', 'Report catalogue by category, count', legend=True))])
    rec = group('evidence', 'Report catalogue', [tile(6, list_block(pg, 'rp-list', 'Report catalogue', [('name', 'Name'), ('recent', 'Last run'), ('category', 'Category')], 'Search reports'))])
    return wall('Reports', [ev, rec])


def c_messages(pg):
    pg.has_grid = False
    ev = group('evidence', 'Service with HSBC', [
        tile(6, chart(pg, 'ms-resp', 'line', 'HSBC response time', 'Average HSBC response time to your requests, hours')),
        tile(6, chart(pg, 'ms-cat', 'stacked-column', 'Requests by category', 'Service requests by category and state, count', legend=True))])
    rec = group('context', 'Messages and requests', [
        tile(3, list_block(pg, 'ms-list', 'Messages from HSBC', [('recent', 'Newest'), ('unread', 'Unread first')], 'Search messages', '<p class="t-cm-caption" id="ms-unread"></p>')),
        tile(3, list_block(pg, 'sr-list', 'Service requests', [('recent', 'Newest'), ('status', 'Status'), ('priority', 'Priority')], 'Search requests',
                           button(pg, 'New service request', 'primary', 'data-action="new-request"')))])
    return wall('HSBC messages and service requests', [ev, rec])


def c_settings(pg):
    pg.has_grid = False
    sw = '<div class="cn-selection-controls">' + ''.join([switch(pg, 'nt-app', 'approvals', 'Email me when a payment needs my approval'),
                                                          switch(pg, 'nt-exc', 'exceptions', 'Email me when a material risk exception opens'),
                                                          switch(pg, 'nt-msg', 'messages', 'Email me when HSBC sends a message')]) + '</div>'
    prefs = stack(section_head(pg, 'st-n-h', 'Notifications'), '<p class="t-ed-body-small">Alerts go to the email address HSBC holds for you. In this prototype nothing is sent; the choices are remembered on this device.</p>', sw)
    appearance = stack(section_head(pg, 'st-a-h', 'Appearance and data'), '<p class="t-ed-body-small">The theme switch beside the page title and the shared filters above are remembered on this device and carried in every link.</p>',
                       alert_info(pg, '<strong class="em">Prototype.</strong> Illustrative data for Northwind Group. No live banking connection, no credentials, and no payment is ever sent.'),
                       button(pg, 'Reset the prototype', 'tertiary', 'data-action="reset-prototype"'))
    signins = stack(section_head(pg, 'st-s-h', 'Your sign-ins'), chart(pg, 'st-logins', 'spark', 'Sign-ins per day', 'Your sign-ins per day over the period'),
                    '<p class="t-ed-body-small">Every sign-in to this prototype is simulated; the series is illustrative.</p>')
    ev = group('evidence', 'Limits and notifications', [
        tile(3, chart(pg, 'st-limits', 'bullet', 'Approval limit used by approver', 'Approval limit used this month by approver, per cent of limit')),
        tile(3, prefs)])
    ctx = group('context', 'Activity and data', [tile(3, signins), tile(3, appearance)])
    return wall('Settings', [ev, ctx])


CONTENT = {'index': c_index, 'accounts': c_accounts, 'liquidity': c_liquidity, 'payments': c_payments, 'fx': c_fx, 'risk': c_risk,
           'trade': c_trade, 'reports': c_reports, 'messages': c_messages, 'settings': c_settings}
TITLES = {p: l for p, l, _, _ in NAV}
TITLES['index'] = 'Overview'

if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for p, _l, _i, _g in NAV:
        pg = build_page(p, TITLES[p], '')
        print('built', href(p), 'regions', sum(pg.n.values()), 'partials', len(pg.partials))
