#!/usr/bin/env python3
"""Assemble out/index.html for the CEO banking prototype (cold run cand-r3).
Verbatim regions (chart figure templates, modal overlay, toast region, AUTO-BEHAVIOUR blocks)
are spliced byte-for-byte from pack/knowledge/snippets and wrapped in APOLLO-SPLICE markers so
gen_provenance_receipt.py --mint can receipt them. Everything else is authored from the snippets'
markup grammar and is NOT receipted (declared in the run report)."""
import os, re, sys, json, html
W = os.path.expanduser('~/cold/cand-r3'); P = W + '/pack'; K = P + '/knowledge'; S = K + '/snippets'
T = W + '/tools'
sys.path.insert(0, K)
import _validate_receipt as VR

def rd(p): return open(p, encoding='utf-8').read()
SNIP = {}
def snip(name):
    if name not in SNIP: SNIP[name] = rd('%s/%s.reference.html' % (S, name))
    return SNIP[name]
def src(name): return 'knowledge/snippets/%s.reference.html' % name

COMMENT_RE = re.compile(r'<!--.*?-->', re.S)
def masked(s): return COMMENT_RE.sub(lambda m: ' ' * len(m.group(0)), s)

def nth_figure(name, dvtype, n=1):
    s = snip(name); m = masked(s); k = 0
    for mm in re.finditer(r'<figure\b[^>]*>', m):
        if ('data-dv-type="%s"' % dvtype) in mm.group(0):
            k += 1
            if k == n:
                end = m.find('</figure>', mm.end())
                return s[mm.start():end + len('</figure>')]
    raise SystemExit('no figure %s %s #%d' % (name, dvtype, n))

def element(name, select):
    import gen_provenance_receipt as G
    text, _ = G.extract_element(snip(name), select)
    return text

def splice(rid, name, kind, text):
    return VR.splice_marker_start(rid, src(name), kind) + text + VR.splice_marker_end(rid)

def behaviour_names(name):
    return re.findall(r'<!--\s*=====\s*AUTO-BEHAVIOUR\s+(\S+)\s+START', snip(name))

def behaviour_block(name, bname):
    s = snip(name)
    a = re.search(r'<!--\s*=====\s*AUTO-BEHAVIOUR\s+%s\s+START[^>]*=====\s*-->' % re.escape(bname), s)
    b = re.search(r'<!--\s*=====\s*AUTO-BEHAVIOUR\s+%s\s+END\s*=====\s*-->' % re.escape(bname), s)
    return s[a.start():b.end()]

def symbol(name, sid):
    m = re.search(r'<symbol id="%s"[^>]*>.*?</symbol>' % re.escape(sid), snip(name), re.S)
    if not m: raise SystemExit('no symbol %s in %s' % (sid, name))
    return m.group(0)

def lib_symbol(sid, rel):
    s = rd(K + '/assets/icons/' + rel)
    inner = s[s.find('>', s.find('<svg')) + 1: s.rfind('</svg>')].strip()
    return '<symbol id="%s" viewBox="0 0 18 18">%s</symbol>' % (sid, inner)

# ---------------------------------------------------------------- chart templates (verbatim)
TPL = {
  'column':      ('Chart-bar', 'column', 1, 'cn-chart-bar'),
  'bar':         ('Chart-bar', 'bar', 1, 'cn-chart-bar'),
  'grouped':     ('Chart-bar', 'grouped-column', 1, 'cn-chart-bar'),
  'stacked':     ('Chart-bar', 'stacked-column', 1, 'cn-chart-bar'),
  'multiline':   ('Chart-line', 'multiline', 1, 'cn-chart-line'),
  'stackedarea': ('Chart-stacked-area', 'stacked-area', 1, 'cn-chart-stacked-area'),
  'combo':       ('Chart-combo', 'combo', 1, 'cn-chart-combo'),
  'donut':       ('Chart-donut', 'donut', 1, 'cn-chart-donut'),
  'pie':         ('Chart-pie', 'pie', 1, 'cn-chart-pie'),
  'histogram':   ('Chart-histogram', 'histogram', 1, 'cn-chart-histogram'),
  'scatter':     ('Chart-scatter', 'scatter', 1, 'cn-chart-scatter'),
  'spark':       ('Chart-sparkline', 'spark', 1, 'cn-chart-sparkline'),
  'boxplot':     ('Chart-boxplot', 'boxplot', 1, 'cn-chart-boxplot'),
  'bullet':      ('Chart-bullet', 'bullet', 1, 'cn-chart-bullet'),
  'butterflyh':  ('Chart-butterfly-h', 'butterfly-h', 1, 'cn-chart-butterfly-h'),
  'butterflyv':  ('Chart-butterfly-v', 'butterfly-v', 1, 'cn-chart-butterfly-v'),
  'candlestick': ('Chart-candlestick', 'candlestick', 1, 'cn-chart-candlestick'),
}
SCOPE = {k: v[3] for k, v in TPL.items()}

def templates():
    out = []
    for key, (name, t, n, scope) in TPL.items():
        fig = nth_figure(name, t, n)
        out.append('<template id="tpl-%s">%s</template>' % (key, splice('%s-figure-%s' % (name, key), name, 'markup', fig)))
    return '\n'.join(out)

def behaviours():
    order = ['Chart-bar', 'Chart-line', 'Chart-stacked-area', 'Chart-combo', 'Chart-donut', 'Chart-pie',
             'Chart-histogram', 'Chart-scatter', 'Chart-sparkline', 'Chart-boxplot', 'Chart-bullet',
             'Chart-butterfly-h', 'Chart-butterfly-v', 'Chart-candlestick']
    seen = {}
    for name in order:
        for b in behaviour_names(name):
            if b not in seen: seen[b] = name
    early = ['dv-render'] + sorted(b for b in seen if b.startswith('dv-render-')) + ['dv-behaviour']
    late = [b for b in seen if b not in early]           # dv-legend, dv-donut-sweep: parse-time init, after the app
    def blk(b): return splice('behaviour-%s' % b, seen[b], 'behaviour', behaviour_block(seen[b], b))
    return '\n'.join(blk(b) for b in early if b in seen), '\n'.join(blk(b) for b in late), seen

# ---------------------------------------------------------------- sprite
def sprite():
    syms = []
    for sid in ['kpi-up', 'kpi-down', 'kpi-flat', 'kpi-chev']: syms.append(symbol('Kpi-tile', sid))
    for sid in ['dg-sort', 'dg-cup', 'dg-cdown', 'dg-cleft', 'dg-cright']: syms.append(symbol('Data-grid', sid))
    for sid in ['ic-home', 'ic-account', 'ic-transfer', 'ic-settings', 'ic-chevron-left', 'ic-chevron-right',
                'ic-chevron-down', 'ic-menu', 'ic-profile']: syms.append(symbol('App-shell-side-nav', sid))
    for sid in ['ic-search', 'ic-clear', 'ic-close', 'ic-calendar', 'ic-export', 'ic-alert', 'ic-error', 'ic-filter']:
        syms.append(symbol('Filter-toolbar-bar', sid))
    for sid in ['to-success', 'to-info', 'to-warning', 'to-close']: syms.append(symbol('Toast', sid))
    for sid in ['al-error', 'al-warning', 'al-success', 'al-info']: syms.append(symbol('Alert', sid))
    lib = [('lib-cash', 'products-and-services/cash.svg'), ('lib-fx', 'products-and-services/fx.svg'),
           ('lib-alert', 'informative/alert.svg'), ('lib-agreement', 'informative/agreement.svg'),
           ('lib-report', 'media/document-report.svg'), ('lib-message', 'media/contact-message.svg'),
           ('lib-download', 'global-controls/download.svg')]
    for sid, rel in lib: syms.append(lib_symbol(sid, rel))
    return ('<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false">\n  '
            + '\n  '.join(syms) + '\n</svg>')

# ---------------------------------------------------------------- shell (authored from App-shell-side-nav)
NAV = [
  (None, [('overview', 'Overview', 'ic-home')]),
  ('Money', [('accounts', 'Accounts and transactions', 'ic-account'),
             ('liquidity', 'Liquidity and funding', 'lib-cash'),
             ('payments', 'Payments and approvals', 'ic-transfer'),
             ('fx', 'FX and markets', 'lib-fx')]),
  ('Risk', [('risk', 'Risk and limits', 'lib-alert'),
            ('trade', 'Trade finance', 'lib-agreement')]),
  ('Service', [('reports', 'Reports', 'lib-report'),
               ('messages', 'HSBC messages and service requests', 'lib-message')]),
]
def nav_link(v, label, ic, ident=True):
    return ('<li><a class="sn-link" href="#/%s" data-nav="%s"><span class="si" aria-hidden="true"><svg viewBox="0 0 18 18" aria-hidden="true">'
            '<use href="#%s"/></svg></span><span class="sn-label t-cm-label">%s</span></a></li>') % (v, v, ic, label)

def nav_body(prefix):
    parts = []
    for i, (g, items) in enumerate(NAV):
        if g:
            gid = '%s-g%d' % (prefix, i)
            parts.append('<div class="sn-group"><span class="sn-group-label t-cm-caption" id="%s">%s</span><ul aria-labelledby="%s">%s</ul></div>'
                         % (gid, g, gid, ''.join(nav_link(*it) for it in items)))
        else:
            parts.append('<div class="sn-group"><ul>%s</ul></div>' % ''.join(nav_link(*it) for it in items))
    return '\n'.join(parts)

FOOT_NAV = nav_link('settings', 'Settings', 'ic-settings')
TICK = '<svg data-bespoke="neutral selection checkmark (library only has teal status ticks)" class="tick" viewBox="0 0 18 18" aria-hidden="true"><path d="M3.5 9.5 L7.5 13.5 L14.5 5"/></svg>'

# ---------------------------------------------------------------- page parts (authored from snippets)
def dd(did, label, icon, options, value_label):
    opts = ''.join('<li class="opt t-cm-label" role="option" aria-selected="false" tabindex="-1" data-value="%s">%s %s</li>'
                   % (html.escape(v), html.escape(t), TICK) for v, t in options)
    mag = '<span class="mag" aria-hidden="true"><svg viewBox="0 0 18 18" aria-hidden="true"><use href="#%s"/></svg></span>' % icon if icon else ''
    return ('<div class="ftb-ctl dd boxed" id="%s">'
            '<label id="%sL" for="%sT" style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0,0,0,0);">%s</label>'
            '<button class="trigger t-cm-button" id="%sT" type="button" role="combobox" aria-haspopup="listbox" aria-expanded="false" aria-controls="%sM" aria-labelledby="%sL %sT">'
            '%s<span class="ddval">%s</span><span class="chev" aria-hidden="true">▾</span></button>'
            '<ul class="menu" id="%sM" role="listbox" aria-labelledby="%sL" tabindex="-1">%s</ul></div>'
            ) % (did, did, did, label, did, did, did, did, mag, value_label, did, did, opts)

def filter_bar():
    return ('<div class="cn-filter-toolbar-bar ceo-ftb">'
            '<div class="ftb-outer" data-ftb-state="no-filters" data-density="full" data-stuck="false" id="ftb">'
            '<form class="ftb" role="search" aria-label="Filter this view" onsubmit="return false;">'
            '<div class="ftb-primary">'
            '<div class="ftb-search"><div class="search boxed">'
            '<span class="mag" aria-hidden="true"><svg viewBox="0 0 18 18" aria-hidden="true"><use href="#ic-search"/></svg></span>'
            '<input type="search" id="ftbQ" aria-label="Search records in this view" placeholder="Search name, reference or counterparty" value="">'
            '<button class="clear" type="button" aria-label="Clear search"><svg viewBox="0 0 18 18" aria-hidden="true"><use href="#ic-clear"/></svg></button>'
            '</div></div>'
            + dd('ftbEntity', 'Entity', 'ic-filter', [], 'All entities')
            + dd('ftbRegion', 'Region', 'ic-filter', [], 'All regions')
            + dd('ftbDays', 'Date range', 'ic-calendar', [('7', 'Last 7 days'), ('14', 'Last 14 days'), ('30', 'Last 30 days')], 'Last 30 days')
            + '<div class="ftb-actions">'
            '<div class="ftb-ctl"><div class="seg l" role="group" aria-label="Theme" id="ftbTheme"><span class="ind" aria-hidden="true"></span>'
            '<button type="button" aria-pressed="true" data-theme-set="light">Light</button>'
            '<button type="button" aria-pressed="false" data-theme-set="dark">Dark</button></div></div>'
            + dd('ftbExport', 'Export results', 'ic-export', [('csv', 'CSV'), ('print', 'Print or save as PDF')], 'Export')
            + '</div></div>'
            '<div class="ftb-context">'
            '<p class="ftb-status t-cm-caption" id="ftbStatus" role="status" aria-live="polite" aria-atomic="true">'
            '<span data-when="no-filters filtered empty error"><span class="num t-cm-figure-6" id="ftbCount">0</span> of <span class="num t-cm-figure-6" id="ftbTotal">0</span> <span id="ftbNoun">records</span></span></p>'
            '<span class="ftb-hint t-cm-caption" data-when="no-filters">No filters applied</span>'
            '<div class="ftb-chips filterbar" id="ftbChips" tabindex="-1" data-when="filtered loading empty error" aria-label="Applied filters" role="group"><div class="row"></div></div>'
            '<div class="ftb-clear" data-when="filtered loading empty error"><button type="button" class="lnk t-cm-caption" data-ftb-clear>Clear all</button></div>'
            '</div></form></div></div>')

def kpi(kid, label):
    return ('<div class="c-bento__tile kpi-tile as-link" role="group" aria-label="%s" data-c="1" data-r="1" data-kpi="%s">'
            '<p class="kpi-lbl t-cm-caption"><a class="kpi-link" href="#">%s</a></p>'
            '<span class="kpi-val t-cm-figure-4"><span class="unit"></span><span></span></span>'
            '<span class="kpi-delta flat" data-carries="symbol label"><span class="glyph" aria-hidden="true"><svg><use href="#kpi-flat"/></svg></span>'
            '<span class="t-cm-figure-6"></span><span class="kpi-per t-cm-legal"></span></span>'
            '<div class="kpi-spark"><svg class="spark-inline" data-trend="flat" viewBox="0 0 200 48" preserveAspectRatio="none" aria-hidden="true" '
            'data-bespoke="chart canvas — dataviz geometry, not an icon (validate-dataviz territory)">'
            '<line class="dv-base" x1="3" y1="45" x2="197" y2="45"/><polygon class="dv-area" points=""/><polyline class="dv-series" points=""/></svg></div>'
            '<span class="kpi-chev" aria-hidden="true"><svg><use href="#kpi-chev"/></svg></span></div>') % (label, kid, label)

def chart_tile(cid, tpl, c, r=1):
    return ('<div class="c-bento__tile stat-card" data-c="%d" data-r="%d"><div class="%s" data-chart="%s" data-tpl="%s"></div></div>'
            % (c, r, SCOPE[tpl], cid, tpl))

def spark_tile(cid, title, c=1):
    return ('<div class="c-bento__tile stat-card" data-c="%d" data-r="1"><div class="tpl-panel-head"><h3 class="t-cm-section-label">%s</h3>'
            '<span class="t-cm-figure-6" data-spark-val="%s"></span></div><div class="cn-chart-sparkline" data-chart="%s" data-tpl="spark"></div></div>') % (c, title, cid, cid)

def summary_tile(sid, title, c=6, r=1, link=None):
    lk = '<a class="tpl-link t-cm-caption" href="%s" data-sum-link="%s">%s</a>' % (link[1], sid, link[0]) if link else ''
    return ('<div class="c-bento__tile stat-card" data-c="%d" data-r="%d" data-summary="%s">'
            '<div class="tpl-panel-head"><h3 class="t-cm-section-label">%s</h3>%s</div>'
            '<dl class="summary tpl-na-head"></dl><div class="l-stack" data-gap="m"></div></div>') % (c, r, sid, title, lk)

def grid(gid, title, cols, tabs=None):
    th = []
    for key, label, kind in cols:
        num = ' class="num"' if kind == 'num' else ''
        if kind == 'nosort':
            th.append('<th scope="col" data-key="%s"><div class="th-in"><span class="t-cm-button">%s</span></div></th>' % (key, label))
            continue
        th.append(('<th scope="col"%s aria-sort="none" data-key="%s"><div class="th-in">'
                   '<button class="sort full t-cm-button" type="button" data-sort="%s"><span class="lbl">%s</span>'
                   '<span class="ic ic-none" aria-hidden="true"><svg viewBox="0 0 18 18"><use href="#dg-sort"/></svg></span>'
                   '<span class="ic ic-asc" aria-hidden="true"><svg viewBox="0 0 18 18"><use href="#dg-cup"/></svg></span>'
                   '<span class="ic ic-desc" aria-hidden="true"><svg viewBox="0 0 18 18"><use href="#dg-cdown"/></svg></span></button>'
                   '</div></th>') % (num, key, key, label))
    return ('<div class="cn-data-grid"><div class="dg" id="dg-%s" data-grid="%s" data-density="comfortable" data-groups="off">'
            '<div class="dg-head"><span class="t-cm-section-label" id="%s-title">%s</span>'
            '<span class="dg-count t-cm-caption" id="%s-count" aria-live="polite"></span></div>'
            '<div class="dg-scroll"><table id="%s-tbl" aria-labelledby="%s-title"><thead><tr class="cols">%s</tr></thead><tbody></tbody></table></div>'
            '<div class="dg-foot"><span class="dg-range t-cm-caption" id="%s-range"></span>'
            '<div class="dg-pp"><label class="t-cm-caption" for="%s-pp">Rows per page</label>'
            '<select id="%s-pp" class="t-cm-caption" data-pp="%s"><option value="10">10</option><option value="25">25</option><option value="50">50</option></select></div>'
            '<nav class="dgpg" aria-label="%s pages"><ul data-pager="%s"></ul></nav></div></div></div>'
            ) % (gid, gid, gid, title, gid, gid, gid, ''.join(th), gid, gid, gid, gid, title, gid)

def tabs(tid, items, panels):
    btns = ''.join('<button class="tab" role="tab" id="%s-t-%s" aria-selected="%s" aria-controls="%s-p-%s" tabindex="%s" data-tab="%s">%s</button>'
                   % (tid, k, 'true' if i == 0 else 'false', tid, k, '0' if i == 0 else '-1', k, lab) for i, (k, lab) in enumerate(items))
    pnl = ''.join('<div class="panel" role="tabpanel" id="%s-p-%s" aria-labelledby="%s-t-%s" tabindex="0"%s>%s</div>'
                  % (tid, k, tid, k, '' if i == 0 else ' hidden', panels[k]) for i, (k, lab) in enumerate(items))
    return ('<div class="cn-tabs"><div class="tabs" data-tabs="%s"><div class="tablist" role="tablist" aria-label="Record views">%s'
            '<span class="indicator" aria-hidden="true"></span></div>%s</div></div>') % (tid, btns, pnl)

def records_tile(inner, c=6):
    return '<div class="c-bento__tile stat-card" data-c="%d" data-r="1">%s</div>' % (c, inner)

def group(role, c, label, tiles):
    return ('<section class="c-bento__tile c-bento tpl-group tpl-group-%s%s" data-bento-role="dashboard" data-c="%d" data-r="1" aria-label="%s">'
            '<div class="c-bento__grid">%s</div></section>') % (role, ' cn-kpi-tile' if role == 'lead' else '', c, label, ''.join(tiles))

def wall(view, label, groups):
    return ('<div class="cn-template-dashboard-bento"><div class="tpl-page"><div class="ceo-ground">'
            '<div class="c-bento tpl-wall" data-bento-role="dashboard" aria-label="%s"><div class="c-bento__grid">%s</div></div>'
            '</div></div></div>') % (label, ''.join(groups))

exec(open(T + '/views.py', encoding='utf-8').read())   # defines VIEWS = [(key, title, lede, wall_html)]

def views_html():
    out = []
    for key, title, lede, body in VIEWS:
        out.append('<section class="ceo-view" data-view="%s" data-title="%s" data-lede="%s" aria-labelledby="page-h1" hidden>%s</section>'
                   % (key, html.escape(title), html.escape(lede), body))
    return '\n'.join(out)

def page():
    early, late, seen = behaviours()
    modal = element('Modals', '.overlay')
    toast_region = element('Toast', '.toast-region')
    shell_script = re.findall(r'<script>(.*?)</script>', snip('App-shell-side-nav'), re.S)[-1]
    css = rd(T + '/app.css'); js = rd(T + '/app.js')
    return '''<!DOCTYPE html>
<html lang="en-GB" class="canon" data-apollo-theme="common" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CEO international banking — Northwind Group (prototype)</title>
<link rel="stylesheet" href="../pack/knowledge/canon/canon.css">
<link rel="stylesheet" href="../pack/knowledge/canon/type.css">
<script>try{var t=localStorage.getItem('ceo.theme');if(t==='dark'||t==='light'){document.documentElement.setAttribute('data-theme',t);}}catch(e){}</script>
<style>
%(css)s
</style>
</head>
<body>
%(sprite)s
<div class="cn-app-shell-side-nav ceo-shell">
<div class="sh" data-nav="auto" id="shell-app">
  <a class="sh-skip t-cm-button" href="#main-app">Skip to main content</a>
  <header class="sh-appbar">
    <button class="sh-menu" type="button" aria-expanded="false" aria-controls="sheet-app" aria-label="Open main menu" data-menu="shell-app">
      <svg viewBox="0 0 18 18" aria-hidden="true"><use href="#ic-menu"/></svg>
    </button>
    <span class="sh-logo"><img class="sh-mark" data-mode="light" src="../pack/knowledge/assets/logos/masterbrand-light-colour.svg" alt="HSBC" width="315" height="85"><img class="sh-mark" data-mode="dark" src="../pack/knowledge/assets/logos/masterbrand-dark-colour.svg" alt="HSBC" width="315" height="85"></span>
    <div class="sh-actions">
      <button type="button" aria-label="Search this view" data-act="focus-search"><svg viewBox="0 0 18 18" aria-hidden="true"><use href="#ic-search"/></svg></button>
      <button type="button" aria-label="Your profile and settings" data-act="go-settings"><svg viewBox="0 0 18 18" aria-hidden="true"><use href="#ic-profile"/></svg></button>
    </div>
  </header>
  <div class="sh-body">
    <nav class="sn" aria-label="Main" id="nav-app">
      <div class="sn-head">
        <span class="sn-brand t-cm-label">Corporate banking</span>
        <button class="sn-toggle" type="button" aria-expanded="true" aria-controls="nav-app-body" aria-label="Collapse navigation" data-navtoggle="shell-app">
          <svg viewBox="0 0 18 18" aria-hidden="true"><use href="#ic-chevron-left"/></svg>
        </button>
      </div>
      <div class="sn-body" id="nav-app-body">
%(nav)s
      </div>
      <div class="sn-foot"><ul>%(foot)s</ul></div>
    </nav>
    <div class="sh-content" id="sh-content">
      <nav class="sh-crumbs" aria-label="Breadcrumb">
        <ol>
          <li><a class="crumb t-ed-body-small" href="#/overview">Northwind Group</a></li>
          <li><span class="sep t-ed-body-small" aria-hidden="true">/</span><span class="t-ed-body-small em" aria-current="page" id="crumb-here">Overview</span></li>
        </ol>
      </nav>
      <main class="sh-main" id="main-app" tabindex="-1">
        <div class="sh-title">
          <h1 class="t-ed-heading-2" id="page-h1">Overview</h1>
        </div>
        <p class="t-ed-body ceo-lede" id="page-lede"></p>
%(ftb)s
%(views)s
      </main>
      <footer class="sh-foot" role="contentinfo" aria-label="Legal footer">
        <div class="sh-legal">
          <ul>
            <li><a class="lnk t-ed-body-small" href="#/settings">Prototype settings</a></li>
            <li><a class="lnk t-ed-body-small" href="#/fx">Illustrative FX rates</a></li>
            <li><a class="lnk t-ed-body-small" href="#/messages">Contact HSBC</a></li>
          </ul>
          <p class="copy t-cm-legal">Prototype with simulated data. No live banking connection. © HSBC Group 2026.</p>
        </div>
      </footer>
    </div>
  </div>
  <div class="sh-scrim" data-scrim="shell-app"></div>
  <div class="sh-sheet" id="sheet-app" tabindex="-1" role="dialog" aria-modal="true" aria-label="Main menu">
    <nav class="sn" aria-label="Main, in menu">
      <div class="sn-head">
        <span class="sn-brand t-cm-label">Corporate banking</span>
        <button class="sn-toggle" type="button" aria-label="Close main menu" data-close="shell-app">
          <svg viewBox="0 0 18 18" aria-hidden="true"><use href="#ic-chevron-left"/></svg>
        </button>
      </div>
      <div class="sn-body">
%(navsheet)s
      </div>
      <div class="sn-foot"><ul>%(foot)s</ul></div>
    </nav>
  </div>
</div>
</div>
<div class="cn-drawer ceo-drawer">
  <div class="scrim" id="drawer-scrim"></div>
  <div class="sheet" id="drawer" role="dialog" aria-modal="true" aria-labelledby="drawer-title" aria-describedby="drawer-body">
    <div class="sheet-head"><h3 class="t-ed-heading-4 em" id="drawer-title">Record</h3>
      <button class="close" id="drawer-close" type="button" aria-label="Close drawer"><svg viewBox="0 0 18 18" aria-hidden="true"><use href="#ic-close"/></svg></button></div>
    <div class="sheet-body" id="drawer-body"></div>
    <div class="sheet-foot" id="drawer-foot"></div>
  </div>
</div>
<div class="cn-modals ceo-modal">
%(modal)s
</div>
<div class="cn-toast ceo-toast">
%(toast)s
</div>
%(templates)s
<script>
%(js)s
</script>
<script>
%(shellscript)s
</script>
%(early)s
%(late)s
</body>
</html>
''' % dict(css=css, sprite=sprite(), nav=nav_body('nw'), navsheet=nav_body('ns'), foot=FOOT_NAV, ftb=filter_bar(),
           views=views_html(), modal=splice('Modals-overlay', 'Modals', 'markup', modal),
           toast=splice('Toast-region', 'Toast', 'markup', toast_region), templates=templates(),
           early=early, late=late, js=js, shellscript=shell_script)

if __name__ == '__main__':
    out = W + '/out/index.html'
    open(out, 'w', encoding='utf-8').write(page())
    print('wrote', out, os.path.getsize(out), 'bytes')
