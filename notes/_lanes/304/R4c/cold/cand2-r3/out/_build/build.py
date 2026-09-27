"""Builds the CEO prototype pages in ../out from the pack IN PLACE.
Every component region is a byte-identical cut from knowledge/snippets/*.reference.html, wrapped in
APOLLO-SPLICE markers (the pack's own grammar, _validate_receipt.splice_marker_start/end), then the
receipt is minted with the pack's generator. Wrappers (scope classes, bento grammar, tiles) and the
page's JavaScript are authored here and declared as such in RUN-REPORT.md."""
import os, re, sys, json, html as H
W = os.path.expanduser('~/cold/cand2-r3'); PACK = os.path.join(W, 'pack'); OUT = os.path.join(W, 'out')
sys.path.insert(0, os.path.join(PACK, 'knowledge'))
import _validate_receipt as VR
SN = os.path.join(PACK, 'knowledge', 'snippets')
TAG_RE = re.compile(r"<(/?)([a-zA-Z][\w:-]*)([^>]*?)(/?)>", re.S)
VOID = {"area","base","br","col","embed","hr","img","input","link","meta","param","source","track","wbr"}
_cache = {}
def src(name):
    if name not in _cache: _cache[name] = open(os.path.join(SN, name + '.reference.html'), encoding='utf-8').read()
    return _cache[name]

def cut(name, needle, nth=0):
    """The element whose opening tag STARTS with `needle` (nth live occurrence, comments masked),
    returned as exact source bytes via a balanced tag scan."""
    h = src(name)
    masked = re.sub(r"<!--.*?-->", lambda m: " " * len(m.group(0)), h, flags=re.S)
    bstart = masked.find('<body')
    idx, k, pos = -1, -1, bstart
    while True:
        pos = masked.find(needle, pos + 1)
        if pos < 0: break
        k += 1
        if k == nth: idx = pos; break
    if idx < 0: raise SystemExit('REFUSED: %s has no live %r (#%d)' % (name, needle, nth))
    m = TAG_RE.match(masked, idx); tag = m.group(2).lower()
    if m.group(4) or tag in VOID: return h[idx:m.end()]
    depth = 1
    for n in TAG_RE.finditer(masked, m.end()):
        if n.group(2).lower() != tag: continue
        if n.group(1):
            depth -= 1
            if depth == 0:
                out = h[idx:n.end()]
                assert out in h
                return out
        elif not (n.group(4) or tag in VOID): depth += 1
    raise SystemExit('REFUSED: unbalanced %s in %s' % (needle, name))

def behaviour(name, beh):
    h = src(name)
    s = re.search(r'<!--\s*=====\s*AUTO-BEHAVIOUR\s+%s\s+START[^>]*=====\s*-->' % re.escape(beh), h)
    e = re.search(r'<!--\s*=====\s*AUTO-BEHAVIOUR\s+%s\s+END\s*=====\s*-->' % re.escape(beh), h)
    return h[s.start():e.end()]

def script_of(name, needle):
    """A snippet's own inline <script> (the meta's #script address) whose body contains `needle`."""
    h = src(name)
    for m in re.finditer(r'<script>(.*?)</script>', h, re.S):
        if needle in m.group(1): return h[m.start():m.end()]
    raise SystemExit('no script %s in %s' % (needle, name))

class Page:
    def __init__(self): self.n = {}; self.used = []
    def splice(self, name, text, kind='markup'):
        self.n[name] = self.n.get(name, 0) + 1
        rid = '%s#%d' % (name, self.n[name])
        rel = os.path.relpath(os.path.join(SN, name + '.reference.html'), PACK)
        if name not in self.used: self.used.append(name)
        return '%s\n%s\n%s' % (VR.splice_marker_start(rid, rel, kind), text, VR.splice_marker_end(rid))
    def s(self, name, needle, nth=0): return self.splice(name, cut(name, needle, nth))

CHART_SRC = {  # figure needle per registered figure, and its canon scope
 'cl2': ('Chart-line', '<figure class="dv dv-animate" data-dv-type="multiline"', 'cn-chart-line', ['dv-render-line']),
 'cb1': ('Chart-bar', '<figure class="dv dv-animate" data-dv-type="column" data-domain-min="0" data-surface="page" role="group" aria-labelledby="cb1-h"', 'cn-chart-bar', ['dv-render-bar']),
 'cb2': ('Chart-bar', '<figure class="dv dv-animate" data-dv-type="bar"', 'cn-chart-bar', ['dv-render-bar']),
 'cb3': ('Chart-bar', '<figure class="dv dv-animate" data-dv-type="column" data-domain-min="0" data-surface="page" data-labelling="direct"', 'cn-chart-bar', ['dv-render-bar']),
 'cb4': ('Chart-bar', '<figure class="dv dv-animate" data-dv-type="grouped-column"', 'cn-chart-bar', ['dv-render-bar']),
 'cd1': ('Chart-donut', '<figure class="dv" id="cd1"', 'cn-chart-donut', ['dv-render-donut', 'dv-donut-sweep']),
 'cd2': ('Chart-donut', '<figure class="dv" data-dv-type="donut" data-total="2320" data-surface="page" data-labelling="direct"', 'cn-chart-donut', ['dv-render-donut', 'dv-donut-sweep']),
 'cp1': ('Chart-pie', '<figure class="dv" id="cp1"', 'cn-chart-pie', ['dv-render-donut']),
 'csa1': ('Chart-stacked-area', '<figure class="dv dv-animate" data-dv-type="stacked-area"', 'cn-chart-stacked-area', ['dv-render-stacked-area']),
 'cc1': ('Chart-combo', '<figure class="dv dv-animate" data-dv-type="combo"', 'cn-chart-combo', ['dv-render-bar', 'dv-render-line', 'dv-render-combo']),
 'cbl1': ('Chart-bullet', '<figure id="cbl1"', 'cn-chart-bullet', ['dv-render-bullet']),
 'ccs1': ('Chart-candlestick', '<figure id="ccs1"', 'cn-chart-candlestick', ['dv-render-candlestick']),
 'cbh1': ('Chart-butterfly-h', '<figure class="dv dv-animate" data-dv-type="butterfly-h"', 'cn-chart-butterfly-h', ['dv-render-butterfly']),
 'cbv1': ('Chart-butterfly-v', '<figure class="dv dv-animate" data-dv-type="butterfly-v"', 'cn-chart-butterfly-v', ['dv-render-butterfly']),
 'cs1': ('Chart-scatter', '<figure class="dv dv-animate" data-dv-type="scatter" data-surface="page" role="group" id="cs1-fig"', 'cn-chart-scatter', ['dv-render-scatter']),
 'ch1': ('Chart-histogram', '<figure class="dv dv-animate" data-dv-type="histogram"', 'cn-chart-histogram', ['dv-render-histogram']),
 'cbp1': ('Chart-boxplot', '<figure class="dv dv-animate" id="cbp1"', 'cn-chart-boxplot', ['dv-render-boxplot']),
 'sp1': ('Chart-sparkline', '<figure class="dv dv-animate" data-dv-type="spark" data-surface="page" role="group" aria-labelledby="cs1-h"', 'cn-chart-sparkline', ['dv-render-sparkline']),
 'sp2': ('Chart-sparkline', '<figure class="dv dv-animate" data-dv-type="spark" data-surface="page" role="group" aria-labelledby="cs2-h"', 'cn-chart-sparkline', ['dv-render-sparkline']),
 'sp3': ('Chart-sparkline', '<figure class="dv dv-animate" data-dv-type="spark" data-surface="page" role="group" aria-labelledby="cs3-h"', 'cn-chart-sparkline', ['dv-render-sparkline']),
}
PARTIAL_SRC = {'dv-behaviour': 'Chart-line', 'dv-legend': 'Chart-line', 'dv-render': 'Chart-line', 'dv-render-line': 'Chart-line',
               'dv-render-bar': 'Chart-bar', 'dv-render-donut': 'Chart-donut', 'dv-donut-sweep': 'Chart-donut',
               'dv-render-stacked-area': 'Chart-stacked-area', 'dv-render-combo': 'Chart-combo', 'dv-render-bullet': 'Chart-bullet',
               'dv-render-candlestick': 'Chart-candlestick', 'dv-render-butterfly': 'Chart-butterfly-h', 'dv-render-scatter': 'Chart-scatter',
               'dv-render-histogram': 'Chart-histogram', 'dv-render-boxplot': 'Chart-boxplot', 'dv-render-sparkline': 'Chart-sparkline'}
ORDER = ['dv-behaviour', 'dv-legend', 'dv-render', 'dv-render-bar', 'dv-render-line', 'dv-render-combo', 'dv-render-donut', 'dv-render-stacked-area',
         'dv-render-bullet', 'dv-render-candlestick', 'dv-render-butterfly', 'dv-render-scatter', 'dv-render-histogram', 'dv-render-boxplot',
         'dv-render-sparkline', 'dv-donut-sweep']

NAV = [('index', 'Overview'), ('accounts', 'Accounts and transactions'), ('liquidity', 'Liquidity and funding'), ('payments', 'Payments and approvals'),
       ('fx', 'FX and markets'), ('risk', 'Risk and limits'), ('trade', 'Trade finance'), ('reports', 'Reports'),
       ('messages', 'HSBC messages and service requests'), ('settings', 'Settings')]
# Page composition: groups answer ONE question each (rule 7b); tiles name the chosen part.
PAGES = {
 'index': dict(title='Overview', sub='Group position for Meridian Holdings — cash, exposure and decisions awaiting you.', groups=[
    ('lead', 'Financial resilience — can we fund our plans?', [('kpi', 'cash'), ('kpi', 'liquidity'), ('kpi', 'headroom'), ('kpi', 'netflow')]),
    ('evidence', 'Risk outlook — where are we exposed?', [('chart', 'cb4', 'exposure-region', 3), ('chart', 'cd1', 'exposure-ccy', 3), ('chart', 'cl2', 'liquidity-trend', 6)]),
    ('context', 'Decisions — what needs my attention?', [('panel', 'approvals', 3), ('panel', 'exceptions', 3)])]),
 'accounts': dict(title='Accounts and transactions', sub='Balances across the group and every settled transaction in the period.', grid=True, groups=[
    ('lead', 'How much cash do we hold, and how is it moving?', [('kpi', 'cash'), ('kpi', 'inflow'), ('kpi', 'outflow'), ('kpi', 'accounts')]),
    ('evidence', 'Where is the cash, and what size are our flows?', [('chart', 'csa1', 'balances-ccy', 3), ('chart', 'ch1', 'txn-size', 3), ('chart', 'cb2', 'balance-entity', 6)]),
    ('evidence', 'Which transactions made up the period?', [('grid', 6)])]),
 'liquidity': dict(title='Liquidity and funding', sub='Available liquidity, facility headroom and what matures next.', grid=True, groups=[
    ('lead', 'Can we fund our plans?', [('kpi', 'liquidity'), ('kpi', 'undrawn'), ('kpi', 'headroom'), ('kpi', 'buffer')]),
    ('evidence', 'How is liquidity moving and how hard are the facilities working?', [('chart', 'cc1', 'flows-combo', 6), ('chart', 'cbl1', 'facility-bullet', 3), ('chart', 'cd2', 'facility-mix', 3)]),
    ('evidence', 'Which facilities fund us, and when do they mature?', [('grid', 6)])]),
 'payments': dict(title='Payments and approvals', sub='Payments raised across the group, and those waiting for your approval.', grid=True, drawer=True, groups=[
    ('lead', 'What is waiting for approval?', [('kpi', 'pendingValue'), ('kpi', 'pendingCount'), ('kpi', 'released'), ('kpi', 'rejected')]),
    ('evidence', 'Where is the pending value, and how do payments resolve?', [('chart', 'cb1', 'pending-ccy', 3), ('chart', 'cp1', 'status-share', 3)]),
    ('evidence', 'Which payments need action?', [('grid', 6)])]),
 'fx': dict(title='FX and markets', sub='Sterling against our operating currencies, and the deals that hedge them.', grid=True, groups=[
    ('lead', 'Where is sterling trading?', [('kpi', 'gbpusd'), ('kpi', 'gbpeur'), ('kpi', 'openFwd'), ('kpi', 'hedge')]),
    ('evidence', 'How has sterling moved?', [('chart', 'ccs1', 'gbpusd-ohlc', 6), ('chart', 'cl2', 'fx-index', 3), ('chart', 'cb4', 'deals-kind', 3)]),
    ('evidence', 'Which deals are open?', [('grid', 6)])]),
 'risk': dict(title='Risk and limits', sub='Exposure against limits by region, currency and counterparty.', grid=True, drawer=True, groups=[
    ('lead', 'How exposed are we?', [('kpi', 'exposure'), ('kpi', 'utilisation'), ('kpi', 'breaches'), ('kpi', 'nearLimit')]),
    ('evidence', 'Where are we exposed?', [('chart', 'cbh1', 'region-butterfly', 3), ('chart', 'cs1', 'util-scatter', 3), ('chart', 'cb2', 'cpty-bar', 6)]),
    ('evidence', 'Which positions and exceptions need attention?', [('grid', 6)])]),
 'trade': dict(title='Trade finance', sub='Letters of credit, guarantees and collections outstanding.', grid=True, groups=[
    ('lead', 'What trade exposure is outstanding?', [('kpi', 'tfOutstanding'), ('kpi', 'tfLc'), ('kpi', 'tfExpiring'), ('kpi', 'tfDocs')]),
    ('evidence', 'Where does our trade business sit?', [('chart', 'cbv1', 'import-export', 3), ('chart', 'cd1', 'instrument-mix', 3)]),
    ('evidence', 'Which instruments are live?', [('grid', 6)])]),
 'reports': dict(title='Reports', sub='Scheduled reports, their spread, and exports of the data behind them.', drawer=True, groups=[
    ('lead', 'What do the report headlines say?', [('kpi', 'cash'), ('kpi', 'liquidity'), ('kpi', 'exposure'), ('kpi', 'reportsReady')]),
    ('evidence', 'How are the key series moving, what do we report on, and how widely do payments vary?', [('sparks', ['sp1', 'sp2', 'sp3'], 'key-series', 3), ('chart', 'cb3', 'reports-category', 3), ('chart', 'cbp1', 'pay-boxplot', 6)]),
    ('evidence', 'Which reports can I run?', [('panel', 'reportList', 6)])]),
 'messages': dict(title='HSBC messages and service requests', sub='Correspondence from your HSBC teams, and requests you have raised.', drawer=True, form=True, groups=[
    ('lead', 'What needs a reply?', [('kpi', 'unread'), ('kpi', 'openReq'), ('kpi', 'awaitingYou'), ('kpi', 'closedReq')]),
    ('evidence', 'What are we asking HSBC for?', [('chart', 'cb3', 'req-type', 3), ('chart', 'cp1', 'req-status', 3)]),
    ('context', 'What has HSBC sent, and what do I need to ask?', [('panel', 'inbox', 3), ('panel', 'requestForm', 3)]),
    ('evidence', 'Where do my requests stand?', [('panel', 'requestList', 6)])]),
 'settings': dict(title='Settings', sub='How this prototype looks and behaves for you. Stored in this browser only.', form=True, groups=[
    ('context', 'How should this prototype behave for me?', [('panel', 'prefs', 3), ('panel', 'notify', 3)]),
    ('evidence', 'How do pending payments sit against my approval limit?', [('chart', 'cb3', 'approval-limits', 6)])]),
}

def build(slug):
    spec = PAGES[slug]; P = Page()
    need_charts = [t[1] for g in spec['groups'] for t in g[2] if t[0] == 'chart'] + [f for g in spec['groups'] for t in g[2] if t[0] == 'sparks' for f in t[1]]
    has_kpi = any(t[0] == 'kpi' for g in spec['groups'] for t in g[2])
    grid = spec.get('grid'); form = spec.get('form')
    # ---------------- tiles ----------------
    def tile(t):
        kind = t[0]
        if kind == 'kpi':
            return '<div class="c-bento__tile ceo-fill" data-kpi="%s"><div class="cn-kpi-tile ceo-fill">%s</div></div>' % (t[1], P.s('Kpi-tile', '<div class="kpi-tile as-link"'))
        if kind == 'sparks':
            figs = ''.join('<div class="%s" data-chart="%s">%s</div>' % (CHART_SRC[f][2], f, P.s(CHART_SRC[f][0], CHART_SRC[f][1])) for f in t[1])
            return ('<div class="c-bento__tile stat-card" data-c="%d" data-panel="%s"><div class="cn-layout-utilities"><div class="l-stack" data-gap="m">%s</div></div></div>'
                    % (t[3], t[2], figs))
        if kind == 'spark':
            name, needle, scope, _ = CHART_SRC[t[1]]
            return '<div class="c-bento__tile stat-card" data-chart="%s" data-fig="%s"><div class="%s">%s</div></div>' % (t[1], t[1], scope, P.s(name, needle))
        if kind == 'chart':
            fig, key, span = t[1], t[2], t[3]
            name, needle, scope, _ = CHART_SRC[fig]
            return '<div class="c-bento__tile stat-card" data-c="%d" data-chart="%s" data-fig="%s"><div class="%s">%s</div></div>' % (span, key, fig, scope, P.s(name, needle))
        if kind == 'grid':
            return ('<div class="c-bento__tile stat-card" data-c="%d" data-grid-tile><div class="cn-data-grid">%s\n%s\n%s</div></div>'
                    % (t[1], P.s('Data-grid', '<p class="hint" id="dgHint">'),
                       P.s('Data-grid', '<div class="dg" id="dg"'), P.s('Data-grid', '<div class="visually-hidden" role="status" id="dgStatus"')))
        if kind == 'panel':
            return '<div class="c-bento__tile stat-card" data-c="%d" data-panel="%s"></div>' % (t[2], t[1])
    groups = []
    for role, label, tiles in spec['groups']:
        groups.append('<section class="c-bento__tile c-bento tpl-group tpl-group-%s" data-bento-role="dashboard" data-c="6" aria-label="%s">\n<div class="c-bento__grid">\n%s\n</div>\n</section>'
                      % (role, H.escape(label), '\n'.join(tile(t) for t in tiles)))
    wall = ('<div class="cn-template-dashboard-bento"><div class="tpl-page">\n<div class="c-bento tpl-wall" data-bento-role="dashboard" aria-label="%s">\n<div class="c-bento__grid">\n%s\n</div>\n</div>\n</div></div>'
            % (H.escape(spec['title'] + ' — panels'), '\n'.join(groups)))
    # ---------------- sprites ----------------
    sprites = [P.s('App-shell-side-nav', '<svg width="0" height="0"')]
    if has_kpi: sprites.append('<div class="cn-kpi-tile" hidden>%s</div>' % P.s('Kpi-tile', '<svg width="0" height="0"'))
    if grid: sprites.append('<div class="cn-data-grid" hidden>%s</div>' % P.s('Data-grid', '<svg width="0" height="0"'))
    sprites.append('<div class="cn-toast" hidden>%s</div>' % P.s('Toast', '<svg width="0" height="0"'))
    sprites.append('<div class="cn-section-heading-lockup" hidden>%s</div>' % P.s('Section-heading-lockup', '<svg width="0" height="0"'))
    sprites.append(ICON_SPRITE)
    # ---------------- frame ----------------
    logo = ('<span class="sh-logo"><img class="sh-mark" data-mode="light" src="../pack/knowledge/assets/logos/masterbrand-light-colour.svg" alt="HSBC" width="315" height="85">'
            '<img class="sh-mark" data-mode="dark" src="../pack/knowledge/assets/logos/masterbrand-dark-colour.svg" alt="HSBC" width="315" height="85"></span>')
    title_row = ('<div class="sh-title"><div class="cn-layout-utilities"><div class="l-stack" data-gap="s"><h1 class="t-ed-heading-2" id="page-title">%s</h1>'
                 '<p class="t-ed-body-small" id="page-sub">%s</p></div></div>'
                 '<div class="cn-layout-utilities"><div class="l-row" data-gap="l" id="title-actions"></div></div></div>'
                 % (H.escape(spec['title']), H.escape(spec['sub'])))
    filters = ('<div class="cn-layout-utilities"><div class="l-row" data-gap="l" id="filter-row" role="group" aria-label="Shared filters"></div></div>'
               '<p class="t-cm-legal" id="fx-note"></p>')
    # Frame: the shell's own parts, each in its canon scope; the page's placement wrappers (ceo-*) sit
    # OUTSIDE every .cn-* scope so placement never touches a component (rule 3a). The grey section is the
    # rails' bentoBg dial, inset by the theme's own main bento spacing token.
    frame = ('<div class="ceo-frame" id="app">\n<div class="cn-app-shell-side-nav">\n%s\n<header class="sh-appbar">\n%s\n%s\n</header>\n</div>\n'
             '<div class="ceo-body">\n<div class="cn-app-shell-side-nav ceo-navcol">\n%s\n</div>\n<div class="ceo-content">\n'
             '<main class="ceo-main" id="main-wide" tabindex="-1">\n<div class="cn-app-shell-side-nav">\n%s\n<div class="sh-main">\n%s\n%s\n</div>\n</div>\n'
             '<section class="ceo-ground" data-bento-bg="grey" aria-label="%s">\n%s\n</section>\n</main>\n<div class="cn-app-shell-side-nav">\n%s\n</div>\n</div>\n</div>\n</div>'
             % (P.s('App-shell-side-nav', '<a class="sh-skip t-cm-button"'), logo, P.s('App-shell-side-nav', '<div class="sh-actions">'),
                P.s('App-shell-side-nav', '<nav class="sn" aria-label="Main" id="nav-wide">'), P.s('App-shell-side-nav', '<nav class="sh-crumbs"'),
                title_row, filters, H.escape(spec['title'] + ' panels'), wall, P.s('App-shell-side-nav', '<footer class="sh-foot"')))
    overlays = ['<div class="cn-drawer">%s\n%s</div>' % (P.s('Drawer', '<div class="scrim" id="scrim"'), P.s('Drawer', '<div class="sheet" id="sheet"')),
                '<div class="cn-toast">%s</div>' % P.s('Toast', '<div class="toast-region" id="toastRegion"')]
    # parts: live instances moved by the page script, and templates cloned by it
    parts = ['<div hidden id="parts">',
             '<div class="cn-textarea" data-part="note">%s\n%s</div>' % (P.s('Textarea', '<svg width="0" height="0"'), P.s('Textarea', '<div class="tx-group" id="live"')),
             '</div>']
    tpls = ['<template id="tpl-dd"><div class="cn-dropdown">%s</div></template>' % P.s('Dropdown', '<div class="dd boxed">'),
            '<template id="tpl-seg"><div class="cn-segmented-control">%s</div></template>' % P.s('Segmented-control', '<div class="seg md"'),
            '<template id="tpl-btn-primary"><div class="cn-button">%s</div></template>' % P.s('Button', '<button class="btn primary">'),
            '<template id="tpl-btn-secondary"><div class="cn-button">%s</div></template>' % P.s('Button', '<button class="btn secondary">'),
            '<template id="tpl-summary"><div class="cn-summary">%s</div></template>' % P.s('Summary', '<dl class="summary">'),
            '<template id="tpl-list"><div class="cn-list-items">%s</div></template>' % P.s('List-items', '<ul class="list" id="liveList">'),
            '<template id="tpl-heading"><div class="cn-section-heading-lockup">%s</div></template>' % SECTION_HEADING(P)]
    if form:
        tpls.append('<template id="tpl-field"><div class="cn-input-fields">%s</div></template>' % P.s('Input-fields', '<div class="field">', 1))
        tpls.append('<template id="tpl-check"><div class="cn-selection-controls">%s</div></template>' % CHECKBOX(P))
    if form:
        sprites.append('<div class="cn-input-fields" hidden>%s</div>' % P.s('Input-fields', '<svg width="0" height="0"'))
    # ---------------- behaviours ----------------
    partials = set()
    for f in need_charts: partials.update(['dv-behaviour', 'dv-legend', 'dv-render'] + CHART_SRC[f][3])
    behs = [P.splice(PARTIAL_SRC[b], behaviour(PARTIAL_SRC[b], b), 'behaviour') for b in ORDER if b in partials]
    scripts = []
    if grid: scripts.append(P.splice('Data-grid', script_of('Data-grid', "const dg = document.getElementById('dg');")))
    scripts.append(P.splice('Textarea', script_of('Textarea', "const ta = document.getElementById('t1')")))
    data = open(os.path.join(W, 'tools', 'data.js'), encoding='utf-8').read()
    app = open(os.path.join(W, 'tools', 'app.js'), encoding='utf-8').read()
    token_vars = {}
    for nm in P.used:
        m = re.search(r'<script[^>]*id="token-manifest"[^>]*>(.*?)</script>', src(nm), re.S)
        if m:
            try: token_vars.update(json.loads(m.group(1)).get('vars', {}))
            except Exception: pass
    beh_manifest = {"$what": "behaviour addresses carried by this page (s258-D1: started from, extended where named)",
                    "dataviz": sorted(partials), "Data-grid": "knowledge/snippets/Data-grid.reference.html#script (verbatim; driven from outside through its own globals)" if grid else None,
                    "Textarea": "knowledge/snippets/Textarea.reference.html#script (verbatim)", "authored": "page script #ceo-app (shell, filters, charts, grid feed, drawer, workflows, persistence)"}
    nav_json = json.dumps([{"slug": s, "label": l} for s, l in NAV])
    page = '''<!DOCTYPE html>
<html lang="en" class="canon" data-apollo-theme="common" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(title)s — Meridian CEO banking prototype</title>
<script>try{var t=localStorage.getItem('ceo-proto-theme');var q=new URLSearchParams(location.search).get('theme');t=q||t;if(t==='dark'||t==='light'){document.documentElement.setAttribute('data-theme',t);}}catch(e){}</script>
<link rel="stylesheet" href="../pack/knowledge/canon/canon.css">
<link rel="stylesheet" href="../pack/knowledge/canon/type.css">
<script type="application/json" id="token-manifest">%(tokens)s</script>
<script type="application/json" id="behaviour-manifest">%(behman)s</script>
<style>
/* PLACEMENT ONLY (skill rule 3a): every rule below targets the page's own ceo-* wrappers, which sit
   OUTSIDE every .cn-* scope. No hex, no raw px. The ground is the rails' bentoBg dial (grey ->
   --surface-subtle, _bento_edit_rails.json dials.bentoBg.tokens.grey) inset by the selected theme's
   own main bento spacing (--bento-dashboard-main, s219-D1(5): common 24). */
body{margin:0;}
.ceo-frame{display:flex; flex-direction:column; min-height:100vh;}
.ceo-body{display:flex; flex:1 1 auto; align-items:stretch;}
.ceo-navcol{position:sticky; top:0; align-self:flex-start;}
.ceo-content{flex:1 1 auto; min-width:0; display:flex; flex-direction:column;}
.ceo-main{flex:1 1 auto; display:flex; flex-direction:column;}
.ceo-main:focus{outline:none;}
.ceo-fill{display:grid;}
.ceo-ground[data-bento-bg="grey"]{background:var(--surface-subtle); padding:var(--bento-dashboard-main) var(--bento-dashboard-main) 0;}
</style>
</head>
<body data-page="%(slug)s">
%(sprites)s
%(frame)s
%(overlays)s
%(parts)s
%(tpls)s
%(scripts)s
%(behs)s
<script id="ceo-data">
%(data)s
</script>
<script id="ceo-nav">const CEO_NAV = %(nav)s;</script>
<script id="ceo-app">
%(app)s
</script>
</body>
</html>
''' % dict(title=H.escape(spec['title']), tokens=json.dumps({"vars": token_vars}, indent=1), behman=json.dumps(beh_manifest, indent=1), slug=slug,
           sprites='\n'.join(sprites), frame=frame, overlays='\n'.join(overlays), parts='\n'.join(parts), tpls='\n'.join(tpls),
           behs='\n'.join(behs), scripts='\n'.join(scripts), data=data, nav=nav_json, app=app)
    out = os.path.join(OUT, slug + '.html')
    open(out, 'w', encoding='utf-8').write(page)
    return out

def SECTION_HEADING(P):
    return P.s('Section-heading-lockup', SEC_NEEDLE)
def CHECKBOX(P):
    return P.s('Selection-controls', CHK_NEEDLE)
SEC_NEEDLE = None; CHK_NEEDLE = None

# ---- icon sprite: library glyphs, paths copied byte-for-byte from knowledge/assets/icons ----
def icon_symbol(sid, fname):
    import glob
    p = glob.glob(os.path.join(PACK, 'knowledge', 'assets', 'icons', '**', fname + '.svg'), recursive=True)[0]
    s = open(p, encoding='utf-8').read()
    vb = re.search(r'viewBox="([^"]+)"', s).group(1)
    inner = s[s.index('>', s.index('<svg')) + 1: s.rindex('</svg>')].strip()
    return '<symbol id="%s" viewBox="%s">%s</symbol>' % (sid, vb, inner)
ICONS = [('ap-dashboard', 'dashboard'), ('ap-liquidity', 'liquidity-management'), ('ap-fx', 'fx'), ('ap-alert', 'alert'),
         ('ap-trade', 'trade-finance'), ('ap-report', 'document-report'), ('ap-message', 'contact-message'), ('ap-download', 'download')]
ICON_SPRITE = ''

if __name__ == '__main__':
    SEC_NEEDLE = sys.argv[1] if len(sys.argv) > 1 else None
    cfg = json.load(open(os.path.join(W, 'tools', 'needles.json')))
    SEC_NEEDLE, CHK_NEEDLE = cfg['section'], cfg['check']
    ICON_SPRITE = '<svg width="0" height="0" style="position:absolute" aria-hidden="true" data-source="knowledge/assets/icons (library glyphs, verbatim paths)">%s</svg>' % ''.join(icon_symbol(a, b) for a, b in ICONS)
    for slug in (sys.argv[2:] or PAGES):
        print(build(slug))
