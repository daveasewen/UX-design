import os, re, html
W = os.path.expanduser('~/cold/v1013-r3')
PACK = W + '/pack'
ICONS = PACK + '/knowledge/assets/icons'
SN = PACK + '/knowledge/snippets'
E = html.escape

def lib_symbol(sid, rel):
    s = open(ICONS + '/' + rel + '.svg').read()
    inner = s[s.index('>') + 1: s.rindex('</svg>')].strip()
    vb = re.search(r'viewBox="([^"]+)"', s).group(1)
    return '<symbol id="%s" viewBox="%s">%s</symbol>' % (sid, vb, inner)

LIB = [('i-home','global-controls/home'),('i-search','global-controls/search'),('i-settings','global-controls/settings'),
       ('i-close','global-controls/close'),('i-sort','global-controls/sort'),('i-filter','global-controls/filter'),
       ('i-download','global-controls/download'),('i-export','global-controls/export'),('i-clear','global-controls/clear'),
       ('i-cleft','arrows-and-chevrons/chevron-left'),('i-cright','arrows-and-chevrons/chevron-right'),
       ('i-cup','arrows-and-chevrons/chevron-up'),('i-cdown','arrows-and-chevrons/chevron-down'),
       ('i-account','products-and-services/account'),('i-liquidity','products-and-services/liquidity-management'),
       ('i-payments','products-and-services/payments-and-transfers'),('i-fx','products-and-services/fx'),
       ('i-trade','products-and-services/trade-finance'),('i-report','media/document-report'),
       ('i-message','media/contact-message'),('i-calendar','media/calendar'),('i-profile','informative/avatar'),
       ('i-risk','global-controls/security-secure'),('i-success','status-icons/success'),('i-info','status-icons/information'),
       ('i-warning','status-icons/warning'),('i-error','status-icons/error')]

def template_symbols():
    s = open(SN + '/Template-dashboard-bento.reference.html').read()
    keep = ['kpi-up', 'kpi-down', 'kpi-table', 'ic-chevron']
    out = []
    for k in keep:
        m = re.search(r'\s*<symbol id="%s".*?</symbol>' % k, s, re.S)
        out.append(m.group(0).strip())
    return out

def sprite():
    syms = template_symbols() + [lib_symbol(a, b) for a, b in LIB]
    return '<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false">\n    ' + '\n    '.join(syms) + '\n</svg>'

def region_bytes(snippet, select):
    """Byte-identical cut via the pack's own extractor (the same one --compose uses)."""
    import subprocess, json, tempfile
    spec = {"title": "x", "pack": "1.0.13", "theme": "light", "regions": [{"snippet": snippet, "select": select, "kind": "markup"}]}
    d = tempfile.mkdtemp()
    open(d + '/s.json', 'w').write(json.dumps(spec))
    subprocess.run(['python3', 'knowledge/gen_provenance_receipt.py', '--compose', d + '/s.json', '-o', d + '/o.html'], cwd=PACK, check=True, capture_output=True)
    o = open(d + '/o.html').read()
    m = re.search(r'(<!-- ===== APOLLO-SPLICE \S+ START.*?===== -->)(.*?)(<!-- ===== APOLLO-SPLICE \S+ END ===== -->)', o, re.S)
    return m.group(2)

def splice(name, snippet, select, body):
    return ('<!-- ===== APOLLO-SPLICE %s START (source=knowledge/snippets/%s.reference.html kind=markup) ===== -->' % (name, snippet)
            + body + '<!-- ===== APOLLO-SPLICE %s END ===== -->' % name)

TICK = '<svg data-bespoke="neutral selection checkmark (library only has teal status ticks)" class="tick" viewBox="0 0 18 18" aria-hidden="true"><path d="M3.5 9.5 L7.5 13.5 L14.5 5"/></svg>'

def dd(id, label, icon, value, options, extra_cls=''):
    """Filter-toolbar-bar dropdown control (Dropdown grammar: .dd.boxed > label + .trigger + ul.menu[data-open])."""
    opts = ''.join('<li class="opt t-cm-label" role="option" aria-selected="%s" tabindex="-1" data-value="%s">%s %s</li>'
                   % ('true' if v == value else 'false', E(v), E(t), TICK) for v, t in options)
    ic = '<span class="mag" aria-hidden="true"><svg viewBox="0 0 18 18" aria-hidden="true"><use href="#%s"/></svg></span>' % icon if icon else ''
    cur = [t for v, t in options if v == value]
    return ('<div class="ftb-ctl dd boxed %s" id="%s" data-dd>'
            '<label id="%sL" for="%sT" style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0,0,0,0);">%s</label>'
            '<button class="trigger t-cm-button" id="%sT" type="button" role="combobox" aria-haspopup="listbox" aria-expanded="false" aria-controls="%sM" aria-labelledby="%sL %sT">'
            '%s<span class="ddval">%s</span><span class="chev" aria-hidden="true">▾</span></button>'
            '<ul class="menu" id="%sM" role="listbox" aria-labelledby="%sL" tabindex="-1" data-open="false">%s</ul></div>'
            % (extra_cls, id, id, id, E(label), id, id, id, id, ic, E(cur[0] if cur else label), id, id, opts))

REGION_OPTS = [('all', 'All regions')] + [(r, r) for r in ['United Kingdom', 'Europe', 'Americas', 'Asia Pacific', 'Middle East']]
ENTITY_OPTS = [('all', 'All entities')] + [(i, n) for i, n in [('E01','Northwind Holdings plc'),('E02','Northwind Europe GmbH'),('E03','Northwind France SAS'),('E04','Northwind Americas Inc'),('E05','Northwind Asia Ltd'),('E06','Northwind Singapore Pte Ltd'),('E07','Northwind Trading (Shanghai) Co'),('E08','Northwind India Pvt Ltd'),('E09','Northwind Gulf FZE')]]
DAY_OPTS = [('7', 'Last 7 days'), ('14', 'Last 14 days'), ('30', 'Last 30 days')]

def ftb(noun, search=True, export=True):
    s = ''
    if search:
        s += ('<div class="ftb-search"><div class="search boxed"><span class="mag" aria-hidden="true"><svg viewBox="0 0 18 18" aria-hidden="true"><use href="#i-search"/></svg></span>'
              '<input type="search" id="ftbQ" aria-label="Search %s" placeholder="Search %s" value="">'
              '<button class="clear" type="button" aria-label="Clear search"><svg viewBox="0 0 18 18" aria-hidden="true"><use href="#i-clear"/></svg></button></div></div>') % (noun, noun)
    s += dd('fRegion', 'Region', 'i-filter', 'all', REGION_OPTS)
    s += dd('fEntity', 'Entity', 'i-filter', 'all', ENTITY_OPTS)
    s += dd('fDays', 'Date range', 'i-calendar', '30', DAY_OPTS)
    act = ''
    if export:
        act = '<div class="ftb-actions">' + dd('fExport', 'Export results', 'i-export', '', [('csv', 'CSV'), ('json', 'JSON')]).replace('<span class="ddval"></span>', '<span class="ddval">Export</span>').replace('<span class="ddval">Export results</span>', '<span class="ddval">Export</span>') + '</div>'
    return ('<div class="cn-filter-toolbar-bar page-pad"><div class="ftb-outer" data-ftb-state="no-filters" data-density="full" data-stuck="false" id="ftb">'
            '<form class="ftb" role="search" aria-label="Filter %s" onsubmit="return false;"><div class="ftb-primary">%s%s</div>'
            '<div class="ftb-context"><p class="ftb-status t-cm-caption" id="ftbStatus" role="status" aria-live="polite" aria-atomic="true">'
            '<span data-when="no-filters filtered empty error"><span class="num t-cm-figure-6" id="ftbCount">0</span> of <span class="num t-cm-figure-6" id="ftbTotal">0</span> %s</span></p>'
            '<span class="ftb-hint t-cm-caption" data-when="no-filters">No filters applied · GBP reporting at illustrative rates</span>'
            '<div class="ftb-chips filterbar" id="ftbChips" tabindex="-1" data-when="filtered loading empty error" aria-label="Applied filters" role="group"><div class="row"></div></div>'
            '<div class="ftb-clear" data-when="filtered loading empty error"><button type="button" class="lnk t-cm-caption" data-ftb-clear>Clear all</button></div>'
            '</div></form></div></div>') % (noun, s, act, noun)

SCOPE = {'column':'bar','bar':'bar','grouped-column':'bar','stacked-column':'bar','line':'line','multiline':'line','stacked-area':'stacked-area',
         'donut':'donut','pie':'pie','combo':'combo','bullet':'bullet','butterfly-h':'butterfly-h','butterfly-v':'butterfly-v','boxplot':'boxplot',
         'candlestick':'candlestick','histogram':'histogram','scatter':'scatter','spark':'sparkline'}
CSV_BTN = open(SN + '/Chart-bar.reference.html').read()
CSV_BTN = re.search(r'<button type="button" class="dv-vt dv-act dv-csv.*?</button>', CSV_BTN, re.S).group(0)
SVG_B = 'data-bespoke="chart canvas — dataviz geometry, not an icon (validate-dataviz territory)"'

def chart(id, typ, title, caption, legend=False, note=''):
    sc = SCOPE[typ]
    if typ in ('donut', 'pie'):
        seg = ('<div class="seg sm" role="group" aria-label="Segment values — pounds or share"><span class="ind" aria-hidden="true"></span>'
               '<button type="button" data-dv-view-btn="value" aria-pressed="true">Value</button><button type="button" data-dv-view-btn="percent" aria-pressed="false">Percent</button></div>')
        svg = '<svg class="dv-svg" %s viewBox="0 0 300 260" width="300" height="260" role="group" aria-label="%s"></svg>' % (SVG_B, E(caption))
        stage = '<div class="dv-stage"><div class="dv-donut-row">%s<ul class="dv-leg vert t-cm-chart-label" id="%s-legend" role="group" aria-label="Categories — uncheck a swatch to dim it, click a name to isolate — then check swatches to add — Reset to show all"></ul><p class="dv-sr" id="%s-live" role="status" aria-live="polite"></p></div></div>' % (svg, id, id)
        fig_extra = ' data-total="0"' + (' data-labelling="spider"' if typ == 'donut' else '')
        anim = 'dv'
    else:
        seg = ''
        if typ == 'bullet':
            attrs = 'data-pl="120" data-pl-fit="text.dv-label" data-pr="12" data-h="200" data-pt="4" data-pb="16" data-h-min="200" viewBox="0 0 580 200"'
        elif typ == 'bar':
            attrs = 'data-pl="46" data-pl-fit="text.dv-label" data-pr="12" data-h="260" data-pt="14" data-pb="30" data-h-min="200" viewBox="0 0 580 260"'
        elif typ == 'butterfly-h':
            attrs = 'data-pl="60" data-pr="60" data-h="260" viewBox="0 0 580 260"'
        elif typ == 'scatter':
            attrs = 'data-pl="46" data-pr="12" data-h="260" data-pt="14" data-pb="40" data-h-min="200" viewBox="0 0 580 260"'   # pb 40: the x-axis title sits at VH-2, ticks at y0+16
        elif typ == 'combo':
            attrs = 'data-pl="46" data-pr="44" data-h="260" data-pt="14" data-pb="30" data-h-min="200" viewBox="0 0 580 260"'
        elif typ == 'spark':
            attrs = 'data-trend="flat" data-pl="4" data-pr="4" data-pt="4" data-pb="4" data-h="90" data-h-min="90" viewBox="0 0 580 90" preserveAspectRatio="none"'
        else:
            attrs = 'data-pl="46" data-pr="12" data-h="260" data-pt="14" data-pb="30" data-h-min="200" viewBox="0 0 580 260"'
        cls = 'dv-svg spark-standalone' if typ == 'spark' else 'dv-svg dv-fit'
        svg = '<svg class="%s" %s %s role="group" aria-label="%s"></svg>' % (cls, attrs, SVG_B, E(caption))
        leg = ('<ul class="dv-leg center t-cm-chart-label" id="%s-legend" role="group" aria-label="Series — uncheck a swatch to dim it, click a name to isolate — then check swatches to add — Reset to show all"></ul><p class="dv-sr" id="%s-live" role="status" aria-live="polite"></p>' % (id, id)) if legend else ''
        stage = '<div class="dv-stage"><div class="dv-chart-area">%s</div></div>%s' % (svg, leg)
        fig_extra = ' data-domain-min="0"' if typ in ('column','bar','grouped-column','stacked-column','histogram','butterfly-h','butterfly-v','combo') else ''
        anim = 'dv dv-animate'
    tbl = ('<details class="dv-tbl"><summary class="dv-tbl-toggle dv-vt dv-dd t-cm-chart-label" aria-controls="%s-tbl"><span>View as table</span><svg class="dv-ico dv-ico-arrow" viewBox="0 0 18 18" aria-hidden="true" focusable="false"><path d="M2 6H16L9 13L2 6Z" fill="currentColor"/></svg></summary>'
           '<div class="dv-tablepanel" id="%s-tbl" role="region" aria-label="%s, data table" tabindex="-1"><table class="dv-table t-cm-legal"><caption>%s</caption></table></div></details>') % (id, id, E(caption), E(caption))
    return ('<div class="cn-chart-%s"><figure class="%s" id="%s" data-dv-type="%s"%s data-surface="page" role="group" aria-labelledby="%s-h" data-lockup-title="%s" data-lockup-table="%s-tbl">'
            '<figcaption id="%s-h" class="sr-only">%s</figcaption><div class="dv-head"><h3 class="dv-title t-cm-section-label">%s</h3>'
            '<div class="dv-controls" role="group" aria-label="Chart tools">%s%s%s</div></div>%s%s</figure></div>'
            % (sc, anim, id, typ, fig_extra, id, E(title), id, id, E(caption), E(title), seg, CSV_BTN, tbl, stage,
               ('<p class="t-cm-caption chart-note">%s</p>' % note) if note else ''))

def card(c, inner, id=None, extra=''):
    return '<div class="c-bento__tile stat-card"%s data-c="%s" data-r="1"%s>%s</div>' % ((' id="%s"' % id) if id else '', c, extra, inner)

def group(role, c, label, tiles):
    return ('<section class="c-bento__tile c-bento tpl-group tpl-group-%s" data-bento-role="dashboard" data-c="%s" data-r="1" aria-label="%s"><div class="c-bento__grid%s">%s</div></section>'
            % (role, c, E(label), ' lead-grid' if role == 'lead' else '', ''.join(tiles)))

def wall(label, groups):
    return ('<div class="tpl-bento-stack wall-ground"><div class="c-bento tpl-wall" data-bento-role="dashboard" aria-label="%s"><div class="c-bento__grid">%s</div></div></div>'
            % (E(label), ''.join(groups)))

def kpi(id, label, cta=None):
    ctab = ('<button type="button" class="kpi-cta" aria-label="%s" data-href="%s"><svg viewBox="0 0 18 18" aria-hidden="true"><use href="#kpi-table"/></svg></button>' % (E(cta[0]), cta[1])) if cta else ''
    return ('<div class="c-bento__tile kpi-tile%s" role="group" aria-label="%s" data-c="1" data-r="1" id="%s"%s>'
            '<p class="lbl16 t-cm-caption">%s</p><span class="amt t-cm-figure-3"><span></span><span>—</span></span>'
            '<span class="delta" data-carries="symbol label"><span class="arrow" aria-hidden="true"><svg><use href="#kpi-up"/></svg></span><span class="t-cm-figure-6"></span><span class="per t-cm-legal"></span></span>'
            '<div class="kpi-spark"><svg class="spark-inline" data-trend="flat" viewBox="0 0 200 48" preserveAspectRatio="none" aria-hidden="true" data-bespoke="chart canvas — dataviz geometry, not an icon (validate-dataviz territory)"></svg></div>%s</div>'
            % (' has-cta' if cta else '', E(label), id, (' data-href="%s"' % cta[1]) if cta else '', E(label), ctab))

def grid(id, title, cols, search_ph=None):
    """Data-grid grammar: .dg > .dg-head + .dg-toolbar(.dgsearch) + .dg-scroll(table) + .dg-foot(range, rows per page, .dgpg)."""
    colg = ''.join('<col style="width:%dpx">' % c[3] for c in cols)
    ths = ''
    for key, label, num, w in cols:
        ths += ('<th scope="col" aria-sort="none" data-key="%s"%s><div class="th-in"><button class="sort full t-cm-button" type="button"><span class="lbl">%s</span>'
                '<span class="ic ic-none" aria-hidden="true"><svg viewBox="0 0 18 18"><use href="#i-sort"/></svg></span>'
                '<span class="ic ic-asc" aria-hidden="true"><svg viewBox="0 0 18 18"><use href="#i-cup"/></svg></span>'
                '<span class="ic ic-desc" aria-hidden="true"><svg viewBox="0 0 18 18"><use href="#i-cdown"/></svg></span></button></div></th>'
                % (key, ' class="num"' if num else '', E(label)))
    srch = ''
    if search_ph:
        srch = ('<div class="dg-toolbar"><div class="dgsearch"><span class="mag" aria-hidden="true"><svg viewBox="0 0 18 18" aria-hidden="true"><use href="#i-search"/></svg></span>'
                '<input type="search" id="%s-q" class="t-cm-input" aria-label="%s" placeholder="%s">'
                '<button class="dgs-clear" type="button" aria-label="Clear filter text"><svg viewBox="0 0 18 18" aria-hidden="true"><use href="#i-close"/></svg></button></div></div>') % (id, E(search_ph), E(search_ph))
    return ('<div class="cn-data-grid"><div class="dg" id="%s" data-density="comfortable" data-grid>'
            '<div class="dg-head"><span class="t-cm-section-label" id="%s-title">%s</span><span class="dg-count t-cm-caption" id="%s-count" aria-live="polite"></span></div>%s'
            '<div class="dg-scroll"><table id="%s-tbl" aria-labelledby="%s-title"><colgroup>%s</colgroup><thead><tr class="cols">%s</tr></thead><tbody id="%s-body"></tbody></table></div>'
            '<div class="dg-foot"><span class="dg-range t-cm-caption" id="%s-range"></span><div class="dg-pp"><label class="t-cm-caption" for="%s-pp">Rows per page</label>'
            '<select id="%s-pp" class="t-cm-caption"><option value="10" selected>10</option><option value="25">25</option><option value="50">50</option></select></div>'
            '<nav class="dgpg" aria-label="%s pages"><ul id="%s-pg"></ul></nav></div></div></div>'
            % (id, id, E(title), id, srch, id, id, colg, ths, id, id, id, id, E(title), id))

def section(title, inner, action=''):
    return section_id(None, title, inner, action)

def section_id(id_, title, inner, action=''):
    return ('<section class="page-pad page-section"' + (' id="%s"' % id_ if id_ else '') + ' aria-label="%s"><div class="tpl-panel-head"><h2 class="t-ed-heading-4">%s</h2>%s</div>%s</section>'
            % (E(title), E(title), action, inner))
