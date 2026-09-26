#!/usr/bin/env python3
"""Assemble out/index.html from src/page.html + verbatim snippet regions.
Placeholders in page.html:
  <!--@SPRITES-->               sprite <svg> blocks from the used snippets (symbols de-duplicated)
  <!--@TEMPLATES-->             every TEMPLATE region, each in <template id="T-key"> with APOLLO-SPLICE markers
  <!--@LIVE key-->              a LIVE region spliced in place
  <!--@BEHAVIOURS-->            AUTO-BEHAVIOUR blocks (dv engine), spliced verbatim (kind=behaviour)
  <!--@SCRIPT name-->           a snippet's inline script (verbatim or declared extension)
  <!--@FILE path-->             inline a file from src/ as-is
"""
import os, re, sys, json
W = os.path.expanduser('~/cold/cand-r1')
PK = os.path.join(W, 'pack', 'knowledge')
sys.path.insert(0, PK)
import gen_provenance_receipt as G
import _validate_receipt as V
SN = os.path.join(PK, 'snippets')

def src(name): return open(os.path.join(SN, name + '.reference.html'), encoding='utf-8').read()

def nth_element(html, tag, n, attr_re=None):
    bm = G.BODY_RE.search(html); body = bm.group(1)
    masked = G.COMMENT_RE.sub(lambda m: ' ' * len(m.group(0)), body)
    # also mask APOLLO-DEMO fenced spans so nothing inside a fence can be matched
    k = 0
    for m in G.TAG_RE.finditer(masked):
        closing, t, attrs, selfclose = m.group(1), m.group(2).lower(), m.group(3), m.group(4)
        if closing or t != tag: continue
        if attr_re and not re.search(attr_re, attrs): continue
        k += 1
        if k != n: continue
        depth = 1
        for q in G.TAG_RE.finditer(masked, m.end()):
            if q.group(2).lower() != tag: continue
            if q.group(1):
                depth -= 1
                if depth == 0: return body[m.start():q.end()]
            elif not (q.group(4) or t in G.VOID): depth += 1
    raise SystemExit('REFUSED: no %s #%d' % (tag, n))

def region(snippet, sel):
    h = src(snippet)
    if isinstance(sel, tuple):
        text = nth_element(h, *sel)
    else:
        text, _ = G.extract_element(h, sel)
    if 'APOLLO-DEMO' in text: raise SystemExit('REFUSED: %s %s carries an APOLLO-DEMO fence' % (snippet, sel))
    return text

# key, snippet, selector, select-hint
TEMPLATES = [
 ('shell','App-shell-side-nav','#shell-wide'),
 ('phead','Page-header-lockup','.ph'),
 ('kpi','Kpi-tile','.as-link'),
 ('ch-column','Chart-bar',('figure',1)),
 ('ch-hbar','Chart-bar',('figure',2)),
 ('ch-grouped','Chart-bar',('figure',4)),
 ('ch-stacked','Chart-bar',('figure',5)),
 ('ch-line','Chart-line',('figure',1)),
 ('ch-multiline','Chart-line',('figure',2)),
 ('ch-area','Chart-stacked-area',('figure',1)),
 ('ch-donut','Chart-donut','#cd1'),
 ('ch-pie','Chart-pie','#cp1'),
 ('ch-combo','Chart-combo',('figure',1)),
 ('ch-candle','Chart-candlestick','#ccs1'),
 ('ch-bullet','Chart-bullet','#cbl1'),
 ('ch-butterfly','Chart-butterfly-h','#cbh1'),
 ('ch-scatter','Chart-scatter','#cs2-fig'),
 ('ch-hist','Chart-histogram','#ch1-fig'),
 ('ch-box','Chart-boxplot','#cbp1'),
 ('ch-spark','Chart-sparkline',('figure',1)),
 ('card','Cards','.card'),
 ('list','List-items','#liveList'),
 ('table','Table','.scroll'),
 ('pager','Pagination','.pg'),
 ('scrim','Drawer','#scrim'),
 ('sheet','Drawer','#sheet'),
 ('modal','Modals','#overlay'),
 ('toast','Toast','.toast'),
 ('toastregion','Toast','#toastRegion'),
 ('statchips','Status-indicator','.chips'),
 ('statcell','Status-indicator','.statustable'),
 ('limits','Limits-meter','.lim'),
 ('summary','Summary','.summary'),
 ('timeline','Timeline','.tl'),
 ('empty','Empty-state','.empty'),
 ('seg','Segmented-control','.seg'),
 ('dd','Dropdown','.boxed'),
 ('field','Input-fields',('div',2,r'class="field"')),
 ('sc','Selection-controls','#sc'),
 ('alert','Alert','#awrap'),
 ('badge','Badge','.standalone'),
 ('btnrow','Button','.row'),
 ('shead','Section-heading-lockup',('div',2,r'class="l-row"')),
]
LIVE = {
 'ftb': ('Filter-toolbar-bar','#ftbA'),
 'dg': ('Data-grid','#dg'),
 'dghint': ('Data-grid','#dgHint'),
 'dgstatus': ('Data-grid','#dgStatus'),
 'tx': ('Textarea','#live'),
}
BEHAVIOURS = [('Chart-bar','dv-behaviour'),('Chart-line','dv-legend'),('Chart-donut','dv-donut-sweep'),('Chart-bar','dv-render'),
 ('Chart-bar','dv-render-bar'),('Chart-line','dv-render-line'),('Chart-stacked-area','dv-render-stacked-area'),
 ('Chart-donut','dv-render-donut'),('Chart-combo','dv-render-combo'),('Chart-candlestick','dv-render-candlestick'),
 ('Chart-bullet','dv-render-bullet'),('Chart-butterfly-h','dv-render-butterfly'),('Chart-scatter','dv-render-scatter'),
 ('Chart-histogram','dv-render-histogram'),('Chart-boxplot','dv-render-boxplot'),('Chart-sparkline','dv-render-sparkline')]
SPRITE_FROM = ['App-shell-side-nav','Kpi-tile','Filter-toolbar-bar','Data-grid','Drawer','Toast','Alert','Cards','Pagination','Empty-state','Links','Page-header-lockup','Selection-controls','Section-heading-lockup','Tags','Textarea','Input-fields','Search-field']

def rel(sn): return 'knowledge/snippets/%s.reference.html' % sn
def splice(rid, sn, kind, text):
    return '%s\n%s\n%s' % (V.splice_marker_start(rid, rel(sn), kind), text, V.splice_marker_end(rid))

def sprites(extra_symbols):
    seen, out = set(), []
    for sn in SPRITE_FROM:
        h = src(sn); b = h[h.find('<body'):]
        for m in re.finditer(r'<svg[^>]*(?:width="0"|display:none|position:absolute)[^>]*>(.*?)</svg>', b, re.S):
            for s in re.finditer(r'<symbol id="([^"]+)".*?</symbol>', m.group(1), re.S):
                if s.group(1) in seen: continue
                seen.add(s.group(1)); out.append(s.group(0))
    for sid, sym in extra_symbols:
        if sid not in seen: seen.add(sid); out.append(sym)
    return '<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false">\n' + '\n'.join(out) + '\n</svg>', seen

ICONS_DIR = os.path.join(PK, 'assets', 'icons')
def lib_symbol(sid, relpath):
    t = open(os.path.join(ICONS_DIR, relpath), encoding='utf-8').read()
    paths = re.findall(r'<path\b[^>]*/>', t)
    return (sid, '<symbol id="%s" viewBox="0 0 18 18">%s</symbol>' % (sid, ''.join(paths)))

EXTRA = [lib_symbol(*x) for x in [
 ('ap-dashboard','media/dashboard.svg'),('ap-dashboard-a','media/dashboard-active.svg'),
 ('ap-account','products-and-services/account.svg'),('ap-account-a','products-and-services/account-active.svg'),
 ('ap-liquidity','products-and-services/liquidity-management.svg'),('ap-liquidity-a','products-and-services/liquidity-management-active.svg'),
 ('ap-payments','products-and-services/payments-and-transfers.svg'),('ap-payments-a','products-and-services/payments-and-transfers-active.svg'),
 ('ap-fx','products-and-services/fx.svg'),('ap-fx-a','products-and-services/fx-active.svg'),
 ('ap-risk','informative/alert.svg'),('ap-risk-a','informative/alert-active.svg'),
 ('ap-trade','products-and-services/trade-finance.svg'),('ap-trade-a','products-and-services/trade-finance-active.svg'),
 ('ap-reports','media/document-report.svg'),('ap-reports-a','media/document-report-active.svg'),
 ('ap-messages','media/contact-message.svg'),('ap-messages-a','media/contact-message-active.svg'),
 ('ap-settings','global-controls/settings.svg'),('ap-settings-a','global-controls/settings-active.svg'),
 ('ap-download','global-controls/download.svg'),('ap-export','global-controls/export.svg'),
 ('ap-print','global-controls/print.svg'),('ap-close','global-controls/close.svg'),
 ('ap-chevron-right','arrows-and-chevrons/chevron-right.svg'),('ap-add','global-controls/add.svg'),
 ('ap-send','global-controls/send.svg'),('ap-refresh','global-controls/refresh.svg'),
 ('ap-compose','global-controls/compose.svg'),('ap-search','global-controls/search.svg'),
]]

def script_of(sn, idx=0):
    k, parts, err = V.resolve_address('knowledge/snippets/%s.reference.html#script' % sn)
    if err: raise SystemExit(err)
    return parts[idx][1]


# ---------------------------------------------------------------- static view skeletons
# view id, nav label, blocks: (heading, [groups: (role, kpis3?, [(tile id, span, kind)])])
VIEWS = [
 ('overview', 'Overview', [
   ('Financial resilience — can we fund our plans?', [('lead', True, [('ov-k-cash',1,'kpi'),('ov-k-liq',1,'kpi'),('ov-k-head',1,'kpi'),('ov-k-cover',1,'kpi')]),
                                                      ('evidence', False, [('ov-c-trend',6,'chart')])]),
   ('Risk outlook — where are we exposed?', [('evidence', False, [('ov-c-exposure',3,'chart'),('ov-c-ccy',3,'chart')])]),
   ('Decisions — what needs my attention?', [('context', False, [('ov-d-approvals',3,'card'),('ov-d-exceptions',3,'card')])])]),
 ('accounts', 'Accounts and transactions', [
   ('Where the cash sits', [('evidence', False, [('ac-c-entity',3,'chart'),('ac-c-ccy',3,'chart')])]),
   ('How cash moved', [('evidence', False, [('ac-c-flows',3,'chart'),('ac-c-daily',3,'chart')])]),
   ('Accounts', [('context', False, [('ac-r-accounts',6,'records')])]),
   ('Transactions', [('context', False, [('ac-r-grid',6,'grid')])])]),
 ('liquidity', 'Liquidity and funding', [
   ('Liquidity position', [('lead', True, [('lq-k-avail',1,'kpi'),('lq-k-undrawn',1,'kpi'),('lq-k-head',1,'kpi'),('lq-k-due',1,'kpi')]),
                           ('evidence', False, [('lq-c-composition',6,'chart')])]),
   ('Funding', [('evidence', False, [('lq-c-util',3,'chart'),('lq-c-ladder',3,'chart')])]),
   ('Facilities', [('context', False, [('lq-r-facilities',6,'records')])])]),
 ('payments', 'Payments and approvals', [
   ('Payments at a glance', [('lead', True, [('py-k-await',1,'kpi'),('py-k-second',1,'kpi'),('py-k-released',1,'kpi'),('py-k-rejected',1,'kpi')])]),
   ('Flow and mix', [('evidence', False, [('py-c-combo',6,'chart'),('py-c-hist',3,'chart'),('py-c-status',3,'chart')])]),
   ('Payments', [('context', False, [('py-r-payments',6,'records')])])]),
 ('fx', 'FX and markets', [
   ('Rates, last 30 sessions', [('lead', True, [('fx-s-usd',1,'spark'),('fx-s-eur',1,'spark'),('fx-s-cny',1,'spark'),('fx-s-jpy',1,'spark')])]),
   ('Markets and hedging', [('evidence', False, [('fx-c-candle',6,'chart'),('fx-c-hedge',3,'chart'),('fx-c-exposure',3,'chart')])]),
   ('Illustrative rates', [('context', False, [('fx-r-rates',6,'records')])]),
   ('FX deals', [('context', False, [('fx-r-deals',6,'records')])])]),
 ('risk', 'Risk and limits', [
   ('Exposure', [('evidence', False, [('rk-c-region',6,'chart'),('rk-c-scatter',3,'chart'),('rk-c-limits',3,'chart')])]),
   ('Limits closest to their cap', [('context', False, [('rk-m-1',3,'meter'),('rk-m-2',3,'meter'),('rk-m-3',3,'meter'),('rk-m-4',3,'meter')])]),
   ('Positions', [('context', False, [('rk-r-positions',6,'records')])]),
   ('Limits', [('context', False, [('rk-r-limits',6,'records')])]),
   ('Risk exceptions', [('context', False, [('rk-r-exceptions',6,'records')])])]),
 ('trade', 'Trade finance', [
   ('Portfolio', [('evidence', False, [('tf-c-mix',3,'chart'),('tf-c-expiry',3,'chart'),('tf-c-region',3,'chart'),('tf-c-tenor',3,'chart')])]),
   ('Instruments', [('context', False, [('tf-r-trade',6,'records')])])]),
 ('reports', 'Reports', [
   ('Reporting activity', [('evidence', False, [('rp-c-runs',3,'chart'),('rp-c-cash',3,'chart')])]),
   ('Report catalogue', [('context', False, [('rp-r-catalogue',6,'records')])]),
   ('Generated reports', [('context', False, [('rp-r-history',6,'records')])])]),
 ('messages', 'HSBC messages and service requests', [
   ('Service at a glance', [('evidence', False, [('ms-c-status',3,'chart'),('ms-c-weekly',3,'chart')])]),
   ('HSBC messages', [('context', False, [('ms-r-inbox',6,'records')])]),
   ('Service requests', [('context', False, [('ms-r-requests',6,'records')])])]),
 ('settings', 'Settings', [
   ('Preferences', [('context', False, [('st-f-display',6,'form'),('st-f-notify',6,'form')])]),
   ('Alerts delivered', [('evidence', False, [('st-c-alerts',6,'chart')])]),
   ('Prototype data', [('context', False, [('st-f-data',6,'form')])])]),
]

def views_html():
    out = []
    for vid, label, blocks in VIEWS:
        out.append('<section class="ceo-view ceo-stack" id="view-%s" data-view="%s" aria-label="%s" hidden>' % (vid, vid, label))
        out.append('<div class="ceo-alerts ceo-stack" id="alerts-%s"></div>' % vid)
        out.append('<div class="cn-template-dashboard-bento ceo-ground"><div class="tpl-page ceo-stack">')
        for bi, (heading, groups) in enumerate(blocks):
            hid = 'h-%s-%d' % (vid, bi)
            out.append('<h2 class="t-cm-section-label" id="%s">%s</h2>' % (hid, heading))
            out.append('<div class="c-bento tpl-wall" data-bento-role="dashboard" aria-labelledby="%s"><div class="c-bento__grid">' % hid)
            for gi, (role, kpis, tiles) in enumerate(groups):
                extra = ' cn-kpi-tile' if kpis and tiles[0][2] == 'kpi' else ''
                out.append('<section class="c-bento__tile c-bento tpl-group tpl-group-%s%s" data-bento-role="dashboard" data-c="6" aria-label="%s"><div class="c-bento__grid">' % (role, extra, heading))
                for tid, span, kind in tiles:
                    cls = 'c-bento__tile' if kind in ('kpi',) else 'c-bento__tile stat-card'
                    out.append('<div class="%s" data-c="%d" id="t-%s" data-kind="%s"></div>' % (cls, span, tid, kind))
                out.append('</div></section>')
            out.append('</div></div>')
        out.append('</div></div></section>')
    return '\n'.join(out)

def build():
    page = open(os.path.join(W, 'src', 'page.html'), encoding='utf-8').read()
    sp, _ = sprites(EXTRA)
    page = page.replace('<!--@SPRITES-->', sp)
    page = page.replace('<!--@VIEWS-->', views_html())
    tpls = []
    for key, sn, sel in TEMPLATES:
        tpls.append('<template id="T-%s">\n%s\n</template>' % (key, splice('%s#%s' % (sn, key), sn, 'markup', region(sn, sel))))
    page = page.replace('<!--@TEMPLATES-->', '\n'.join(tpls))
    for key, (sn, sel) in LIVE.items():
        page = page.replace('<!--@LIVE %s-->' % key, splice('%s#%s' % (sn, key), sn, 'markup', region(sn, sel)))
    beh = []
    for sn, name in BEHAVIOURS:
        text, _ = G.extract_behaviour(src(sn), name)
        beh.append(splice('%s#%s' % (sn, name), sn, 'behaviour', text))
    page = page.replace('<!--@BEHAVIOURS-->', '\n'.join(beh))
    # scripts
    dg0 = script_of('Data-grid', 0)
    m = re.search(r'const DATA = \[.*?\n    \];', dg0, re.S)
    if not m: raise SystemExit('dg DATA literal not found')
    dg0x = dg0[:m.start()] + 'const DATA = window.CEO_GRID_ROWS;   /* EXTENDED (s258-D1): rows come from the page dataset CEO_DATA, not the specimen literal */' + dg0[m.end():]
    page = page.replace('<!--@SCRIPT dg0-->', '<script>' + dg0x + '</script>')
    page = page.replace('<!--@SCRIPT dg1-->', '<script>' + script_of('Data-grid', 1) + '</script>')
    ftb = script_of('Filter-toolbar-bar', 0)
    anchor = '      const DATA=['
    i = ftb.find(anchor)
    if i < 0: raise SystemExit('ftb consumer anchor not found')
    ftbx = ftb[:i] + '      /* EXTENDED (s258-D1): the specimen consumer below is dead code on this page — the page app listens for apollo:filter-change and answers the bar itself. */\n      window.CEO_FTB = { apply: apply, state: state }; return;\n' + ftb[i:]
    page = page.replace('<!--@SCRIPT ftb-->', '<script>' + ftbx + '</script>')
    page = page.replace('<!--@SCRIPT tx-->', '<script>' + script_of('Textarea', 0) + '</script>')
    def inc(mm):
        return open(os.path.join(W, 'src', mm.group(1)), encoding='utf-8').read()
    page = re.sub(r'<!--@FILE (\S+)-->', inc, page)
    out = os.path.join(W, 'out', 'index.html')
    open(out, 'w', encoding='utf-8').write(page)
    print('wrote', out, len(page.encode('utf-8')), 'bytes;', len(TEMPLATES), 'templates;', len(LIVE), 'live;', len(BEHAVIOURS), 'behaviours')

if __name__ == '__main__':
    build()
