#!/usr/bin/env python3
"""Build the CEO prototype pages from the Apollo pack IN PLACE (../pack relative to out/).
Every page = the App-shell-side-nav frame + the Template-dashboard-bento header and bento wall,
component markup by the snippets' own classes, the ONE in-page DATA script, the app core, the
page script, and the chart engine's AUTO-BEHAVIOUR blocks SPLICED byte-identically out of the
chart snippets by the pack's own gen_provenance_receipt.py (--compose), then receipted (--mint)."""
import json, os, re, subprocess, sys, glob
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
PACK = os.path.abspath(os.path.join(OUT, '..', 'pack'))
SN = os.path.join(PACK, 'knowledge', 'snippets')
ICONS = os.path.join(PACK, 'knowledge', 'assets', 'icons')

def snip(name):
    for f in glob.glob(os.path.join(SN, '*.reference.html')):
        if os.path.basename(f).lower() == name.lower() + '.reference.html':
            return open(f, encoding='utf-8').read()
    raise SystemExit('no snippet ' + name)

# ---------- the sprite: symbols copied verbatim from the snippets that carry them, + library glyphs
def symbols(src, ids):
    out = {}
    for m in re.finditer(r'<symbol id="([^"]+)"[^>]*>.*?</symbol>', src, re.S):
        if m.group(1) in ids:
            out[m.group(1)] = m.group(0)
    missing = [i for i in ids if i not in out]
    if missing:
        raise SystemExit('missing symbols %s' % missing)
    return out
SYM = {}
for name, ids in [
    ('App-shell-side-nav', ['ic-menu', 'ic-search', 'ic-profile', 'ic-chevron-left', 'ic-chevron-right']),
    ('Template-dashboard-bento', ['ic-chevron', 'kpi-up', 'kpi-down', 'kpi-table']),
    ('Data-grid', ['dg-sort', 'dg-cup', 'dg-cdown', 'dg-cleft', 'dg-cright', 'dg-search', 'dg-close']),
    ('Filter-toolbar-bar', ['ic-filter', 'ic-calendar', 'ic-export', 'ic-close', 'ic-error']),
    ('Toast', ['to-success', 'to-info', 'to-warning', 'to-close']),
    ('Alert', ['al-error', 'al-warning', 'al-success', 'al-info']),
]:
    for k, v in symbols(snip(name), ids).items():
        SYM.setdefault(k, v)

def lib(name):
    hits = glob.glob(os.path.join(ICONS, '**', name + '.svg'), recursive=True)
    if not hits:
        raise SystemExit('no icon ' + name)
    s = open(hits[0], encoding='utf-8').read()
    paths = re.findall(r'<path[^>]*/>', s)
    vb = re.search(r'viewBox="([^"]+)"', s).group(1)
    return '<symbol id="i-%s" viewBox="%s">%s</symbol>' % (name, vb, ''.join(paths))
NAV = [  # file, key, label, icon, group
    ('index.html', 'overview', 'Overview', 'dashboard', None),
    ('accounts.html', 'accounts', 'Accounts', 'account', 'Money'),
    ('liquidity.html', 'liquidity', 'Liquidity and funding', 'cash', 'Money'),
    ('payments.html', 'payments', 'Payments and approvals', 'payments-and-transfers', 'Money'),
    ('fx.html', 'fx', 'FX and markets', 'global-money', 'Money'),
    ('risk.html', 'risk', 'Risk and limits', 'warning', 'Risk and trade'),
    ('trade.html', 'trade', 'Trade finance', 'trade-finance', 'Risk and trade'),
    ('reports.html', 'reports', 'Reports', 'document-report', 'Insight'),
    ('messages.html', 'messages', 'Messages and requests', 'contact-message', 'Insight'),
    ('settings.html', 'settings', 'Settings', 'settings', None),
]
LIBSYM = []
for _, _, _, ic, _ in NAV:
    LIBSYM.append(lib(ic))
    if glob.glob(os.path.join(ICONS, '**', ic + '-active.svg'), recursive=True):
        LIBSYM.append(lib(ic + '-active'))
SPRITE = ('<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false">\n' +
          '\n'.join(SYM.values()) + '\n' + '\n'.join(LIBSYM) + '\n</svg>')

# ---------- verbatim pieces lifted from snippets
CB = snip('Chart-bar')
CSVBTN = re.search(r'<button type="button" class="dv-vt dv-act dv-csv t-cm-chart-label">.*?</button>', CB, re.S).group(0)
SUMMARY = re.search(r'<summary class="dv-tbl-toggle[^>]*>.*?</summary>', CB, re.S).group(0)
SUMMARY = re.sub(r'aria-controls="[^"]+"', 'aria-controls="%ID%-tbl"', SUMMARY)
DRAWER_CLOSE = re.search(r'<button class="close" id="close" type="button" aria-label="Close drawer">.*?</button>', snip('Drawer'), re.S).group(0).replace(' id="close"', '')
MODAL_CLOSE = re.search(r'<button class="close" id="close" type="button" aria-label="Close dialog">.*?</button>', snip('Modals'), re.S).group(0).replace(' id="close"', '')

def navlinks(cur, sheet=False):
    out, group = [], '__'
    items = [n for n in NAV if n[1] != 'settings']
    for f, key, label, ic, g in items:
        if g != group:
            if group != '__':
                out.append('</ul></div>')
            gid = ('sg-' if sheet else 'ng-') + (g or 'top').lower().replace(' ', '-')
            out.append('<div class="sn-group">' + ('<span class="sn-group-label t-cm-caption" id="%s">%s</span><ul aria-labelledby="%s">' % (gid, g, gid) if g else '<ul>'))
            group = g
        active = key == cur
        icn = ic + ('-active' if active and ('id="i-%s-active"' % ic) in SPRITE else '')
        out.append('<li><a class="sn-link" data-app-href="%s" href="%s"%s><span class="si" aria-hidden="true"><svg viewBox="0 0 18 18" aria-hidden="true"><use href="#i-%s"/></svg></span><span class="sn-label t-cm-label">%s</span></a></li>'
                   % (f, f, ' aria-current="page"' if active else '', icn, label))
    out.append('</ul></div>')
    f, key, label, ic, g = NAV[-1]
    active = key == cur
    icn = ic + ('-active' if active and ('id="i-%s-active"' % ic) in SPRITE else '')
    foot = ('<div class="sn-foot"><ul><li><a class="sn-link" data-app-href="%s" href="%s"%s><span class="si" aria-hidden="true"><svg viewBox="0 0 18 18" aria-hidden="true"><use href="#i-%s"/></svg></span><span class="sn-label t-cm-label">%s</span></a></li></ul></div>'
            % (f, f, ' aria-current="page"' if active else '', icn, label))
    return '\n'.join(out), foot

def page_html(p):
    body_nav, foot = navlinks(p['key'])
    sheet_nav, sheet_foot = navlinks(p['key'], sheet=True)
    crumbs = '<li><a class="crumb" data-app-href="index.html" href="index.html">Group overview</a></li>' if p['key'] != 'overview' else ''
    crumbs += ('<li>%s<span class="t-cm-ctl-14" aria-current="page">%s</span></li>' %
               ('<span class="sep" aria-hidden="true"><svg class="chev" viewBox="0 0 18 18"><use href="#ic-chevron"/></svg></span>' if p['key'] != 'overview' else '', p['crumb']))
    filterbar = '' if p.get('nofilters') else FILTERBAR
    return TEMPLATE.format(**{
        'key': p['key'], 'title': p['title'], 'desc': p['desc'], 'sprite': SPRITE, 'nav': body_nav, 'navfoot': foot, 'sheetnav': sheet_nav, 'sheetfoot': sheet_foot,
        'crumbs': crumbs, 'h1': p['h1'], 'sub': p['sub'], 'actions': p.get('actions', ''), 'strip': p.get('strip', ''), 'filterbar': filterbar,
        'wall': p['wall'], 'walllabel': p['h1'], 'drawerclose': DRAWER_CLOSE, 'modalclose': MODAL_CLOSE,
    })

FILTERBAR = '''<div class="cn-filter-toolbar-bar"><div class="ftb-outer" id="ftb" data-ftb-state="no-filters" data-density="full">
<form class="ftb" role="search" aria-label="Filter every figure on this page" onsubmit="return false;">
<div class="ftb-primary">
<div class="ftb-ctl dd boxed" id="dd-entity"><label id="dd-entity-l" for="dd-entity-t" class="sr-only">Entity</label>
<button class="trigger t-cm-button" id="dd-entity-t" type="button" role="combobox" aria-haspopup="listbox" aria-expanded="false" aria-controls="dd-entity-m" aria-labelledby="dd-entity-l dd-entity-t"><span class="mag" aria-hidden="true"><svg viewBox="0 0 18 18" aria-hidden="true"><use href="#ic-filter"/></svg></span><span class="ddval">All entities</span><span class="chev" aria-hidden="true">▾</span></button>
<ul class="menu" id="dd-entity-m" role="listbox" aria-labelledby="dd-entity-l" tabindex="-1"></ul></div>
<div class="ftb-ctl dd boxed" id="dd-region"><label id="dd-region-l" for="dd-region-t" class="sr-only">Region</label>
<button class="trigger t-cm-button" id="dd-region-t" type="button" role="combobox" aria-haspopup="listbox" aria-expanded="false" aria-controls="dd-region-m" aria-labelledby="dd-region-l dd-region-t"><span class="mag" aria-hidden="true"><svg viewBox="0 0 18 18" aria-hidden="true"><use href="#ic-filter"/></svg></span><span class="ddval">All regions</span><span class="chev" aria-hidden="true">▾</span></button>
<ul class="menu" id="dd-region-m" role="listbox" aria-labelledby="dd-region-l" tabindex="-1"></ul></div>
<div class="ftb-ctl dd boxed" id="dd-days"><label id="dd-days-l" for="dd-days-t" class="sr-only">Date range</label>
<button class="trigger t-cm-button" id="dd-days-t" type="button" role="combobox" aria-haspopup="listbox" aria-expanded="false" aria-controls="dd-days-m" aria-labelledby="dd-days-l dd-days-t"><span class="mag" aria-hidden="true"><svg viewBox="0 0 18 18" aria-hidden="true"><use href="#ic-calendar"/></svg></span><span class="ddval">Last 30 days</span><span class="chev" aria-hidden="true">▾</span></button>
<ul class="menu" id="dd-days-m" role="listbox" aria-labelledby="dd-days-l" tabindex="-1"></ul></div>
</div>
<div class="ftb-context">
<p class="ftb-status t-cm-caption" role="status" aria-live="polite" aria-atomic="true"><span data-when="no-filters filtered empty error"><span class="num t-cm-figure-6" id="ftb-count">9</span> of <span class="num t-cm-figure-6" id="ftb-total">9</span> entities · GBP reporting · illustrative FX as at 25 Sep 2026</span></p>
<span class="ftb-hint t-cm-caption" data-when="no-filters">No filters applied</span>
<div class="ftb-chips filterbar" id="ftb-chips" tabindex="-1" data-when="filtered loading empty error" aria-label="Applied filters" role="group"><div class="row"></div></div>
<div class="ftb-clear" data-when="filtered loading empty error"><button type="button" class="lnk t-cm-caption" data-ftb-clear>Clear all</button></div>
</div>
</form></div></div>'''

TEMPLATE = '''<!DOCTYPE html>
<html lang="en" class="canon" data-apollo-theme="common" data-theme="light" data-page="{key}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · HSBC CEO view (prototype)</title>
<meta name="description" content="{desc}">
<!-- Apollo Spider v1.0.13, referenced in place. Theme: common (data-apollo-theme), light/dark (data-theme). -->
<link rel="stylesheet" href="../pack/knowledge/canon/type.css">
<link rel="stylesheet" href="../pack/knowledge/canon/canon.css">
<script>/* theme before first paint: the stored choice, read defensively */
try {{ var s = JSON.parse(localStorage.getItem('hsbc-ceo-proto.v1')) || {{}}; if (s.theme === 'dark' || s.theme === 'light') {{ document.documentElement.setAttribute('data-theme', s.theme); }} }} catch (e) {{}}</script>
<style>
/* HARNESS ONLY — page frame and the ruled page ground. No hex, no .c-* / .cn-* redefinition.
   Every value is a token or a rail stop. */
body {{ margin: 0; }}
.ceo-frame {{ height: 100vh; height: 100dvh; }}                         /* the shell frame fills the window */
.ceo-head {{ padding: var(--gap-fixed-subsection-xsmall) var(--gap-fixed-subsection-small) var(--gap-fixed-subsection-xsmall); }}
.ceo-ground {{ background: var(--surface-subtle); padding-top: var(--gap-fixed-subsection-xsmall); }}  /* page rail: grey = --surface-subtle (s219-D3(4)) */
/* DARK: the rail's grey (--surface-subtle) resolves to the SAME value as the tile surface in dark
   (measured: both rgb(31,31,31)), so the tiles would lose the definition the brief asks the grey for.
   The rail's own "page" member (--background-default) keeps it. Declared default; the dark ground is
   an open question on the rail itself. */
[data-theme="dark"] .ceo-ground {{ background: var(--background-default); }}
.ceo-page {{ flex: 1 0 auto; }}
.ceo-chart {{ min-width: 0; }}
.ceo-stack {{ display: flex; flex-direction: column; gap: var(--gap-fixed-content-medium); }}
.ceo-empty {{ padding: var(--padding-fixed-medium) 0; }}
.ceo-drill {{ margin-top: var(--padding-fixed-medium); }}   /* clears the legend rows' 24px hit areas (measured overlap) */
/* SCOPE COLLISION REPAIR (found by measurement in this build): the template's spliced chart CSS
   (`:where(.cn-template-dashboard-bento) figure.dv-fit-on .dv-svg{{width:100%}}` and the fixed
   580x260 rule) is not scoped to its own chart, so it reaches a donut/pie nested in the template
   and stretches the ring's fixed canvas. `auto` hands the size back to the svg's own width/height
   attributes, exactly as the Chart-donut snippet ships them. No value is introduced. */
.ceo-chart .dv-donut-row > svg.dv-svg {{ width: auto; height: auto; }}
/* THE COMMON DASHBOARD DIAL (knowledge/_render/_bento_edit_rails.json defaults.values.dashboard.legacy:
   mainSpacing 24, subSpacing 4). The template snippet ships mono's 40 on the wall at (0,6,0); its own
   header says "declare instance dials as `.c-bento.my-wall{{…}}`". This is that declaration, one class
   heavier so it wins on weight, set to the rail stop 24 through its token. */
.tpl-page.ceo-ground .c-bento.tpl-wall.ceo-wall[data-bento-role="dashboard"]:has(> .c-bento__grid > .c-bento) {{ --bento-gutter: var(--gap-fixed-subsection-xsmall); }}
</style>
</head>
<body>
{sprite}
<div class="cn-app-shell-side-nav">
<div class="sh ceo-frame" data-nav="auto" id="shell">
<a class="sh-skip t-cm-button" href="#main">Skip to main content</a>
<header class="sh-appbar">
<button class="sh-menu" type="button" aria-expanded="false" aria-controls="sheet" aria-label="Open main menu" data-menu="shell"><svg viewBox="0 0 18 18" aria-hidden="true"><use href="#ic-menu"/></svg></button>
<span class="sh-logo"><img class="sh-mark" data-mode="light" src="../pack/knowledge/assets/logos/masterbrand-light-colour.svg" alt="HSBC" width="315" height="85"><img class="sh-mark" data-mode="dark" src="../pack/knowledge/assets/logos/masterbrand-dark-colour.svg" alt="HSBC" width="315" height="85"></span>
<div class="sh-actions">
<div class="cn-segmented-control"><div class="seg s" role="group" aria-label="Colour mode"><span class="ind" aria-hidden="true"></span><button type="button" aria-pressed="true" data-theme-btn="light">Light</button><button type="button" aria-pressed="false" data-theme-btn="dark">Dark</button></div></div>
<button type="button" aria-label="Your profile: Chief executive, Harbourline Group" data-action="profile"><svg viewBox="0 0 18 18" aria-hidden="true"><use href="#ic-profile"/></svg></button>
</div>
</header>
<div class="sh-body">
<nav class="sn" aria-label="Main" id="nav-main">
<div class="sn-head"><span class="sn-brand t-cm-label">Harbourline Group</span>
<button class="sn-toggle" type="button" aria-expanded="true" aria-controls="nav-main-body" aria-label="Collapse navigation" data-navtoggle="shell"><svg viewBox="0 0 18 18" aria-hidden="true"><use href="#ic-chevron-left"/></svg></button></div>
<div class="sn-body" id="nav-main-body">
{nav}
</div>
{navfoot}
</nav>
<div class="sh-content">
<div class="cn-template-dashboard-bento ceo-page">
<header class="tpl-header l-stack ceo-head" data-gap="l">
<nav class="tpl-crumbs" aria-label="Breadcrumb"><ol class="t-cm-caption">{crumbs}</ol></nav>
<div class="l-row" data-align="end" data-gap="l">
<div class="tpl-display l-measure"><h1 class="t-ed-heading-2">{h1}</h1><p class="t-ed-body">{sub} <span data-scope-label></span>.</p></div>
<div class="tpl-actions l-row" data-gap="m">{actions}</div>
</div>
{strip}
{filterbar}
</header>
<main class="tpl-page ceo-ground" id="main" tabindex="-1">
<div class="tpl-bento-stack">
<div class="c-bento tpl-wall ceo-wall" data-bento-role="dashboard" aria-label="{walllabel}">
<div class="c-bento__grid">
{wall}
</div>
</div>
</div>
</main>
</div>
FOOTER_SPLICE
</div>
</div>
<div class="sh-scrim" id="shell-scrim" data-scrim="shell"></div>
<div class="sh-sheet" id="sheet" tabindex="-1" role="dialog" aria-modal="true" aria-label="Main menu">
<nav class="sn" aria-label="Main, in menu">
<div class="sn-head"><span class="sn-brand t-cm-label">Harbourline Group</span><button class="sn-toggle" type="button" aria-label="Close main menu" data-close="shell"><svg viewBox="0 0 18 18" aria-hidden="true"><use href="#ic-chevron-left"/></svg></button></div>
<div class="sn-body">
{sheetnav}
</div>
{sheetfoot}
</nav>
</div>
</div>
</div>
<div class="cn-drawer"><div class="scrim" id="scrim"></div>
<div class="sheet" id="drawer" role="dialog" aria-modal="true" aria-labelledby="drawer-t" aria-describedby="drawer-b">
<div class="sheet-head"><h3 class="t-ed-heading-4 em" id="drawer-t">Details</h3>
{drawerclose}</div>
<div class="sheet-body" id="drawer-b"></div>
<div class="sheet-foot" id="drawer-f"></div>
</div></div>
<div class="cn-modals"><div class="overlay" id="modal" hidden>
<div class="dialog" role="dialog" aria-modal="true" aria-labelledby="modal-t" aria-describedby="modal-b" tabindex="-1">
{modalclose}
<h2 id="modal-t">Confirm</h2>
<div id="modal-b" class="ceo-stack"></div>
<div class="actions" id="modal-a"></div>
</div></div></div>
<div class="cn-toast"><div class="toast-region" id="toasts" aria-live="polite"></div></div>
BEHAVIOUR_SPLICES
<script>
%%DATA%%
</script>
<script>
%%CORE%%
</script>
<script>
%%PAGE%%
</script>
</body>
</html>
'''

sys.path.insert(0, HERE)
from pages import PAGES   # noqa: E402

ENGINE = ['dv-behaviour', 'dv-legend', 'dv-render', 'dv-render-bar', 'dv-render-line', 'dv-render-stacked-area', 'dv-render-donut', 'dv-donut-sweep',
          'dv-render-combo', 'dv-render-bullet', 'dv-render-candlestick', 'dv-render-scatter', 'dv-render-boxplot', 'dv-render-histogram',
          'dv-render-butterfly', 'dv-render-sparkline']
# The chart engine is the pack's own canon/*.js, loaded IN PLACE by <script src>. It is NOT inlined as
# AUTO-BEHAVIOUR splices: measured at build time, the composed-screen gate's icon-source step reads the
# engine SOURCE as markup — the comment "everything inside the <svg> ..." in dv-render.js and the path
# template d="' + arc(...) + '" in dv-render-donut.js — and reports them as unknown icons. Inherited, not ours.
def engine_tags(needs):
    return '\n'.join('<script src="../pack/knowledge/canon/%s.js"></script>' % n for n in ENGINE if n in needs)

def splices(tmp):
    spec = {'title': 'splice source', 'pack': '1.0.13', 'theme': 'light', 'regions':
            [{'snippet': 'App-shell-side-nav', 'select': '.sh-foot', 'kind': 'markup'}]}
    sp = os.path.join(tmp, 'spec.json'); json.dump(spec, open(sp, 'w'))
    op = os.path.join(tmp, 'spliced.html')
    subprocess.run([sys.executable, os.path.join(PACK, 'knowledge', 'gen_provenance_receipt.py'), '--compose', sp, '-o', op], check=True, cwd=PACK, stdout=subprocess.DEVNULL)
    src = open(op, encoding='utf-8').read()
    regs = re.findall(r'(<!-- ===== APOLLO-SPLICE (\S+) START .*?<!-- ===== APOLLO-SPLICE \2 END ===== -->)', src, re.S)
    return [r[0] for r in regs if r[1].startswith('App-shell-side-nav')][0]

def main():
    tmp = os.path.join(HERE, '_tmp'); os.makedirs(tmp, exist_ok=True)
    data = open(os.path.join(HERE, 'src', 'data.js'), encoding='utf-8').read()
    core = open(os.path.join(HERE, 'src', 'core.js'), encoding='utf-8').read().replace("'%%CSVBTN%%'", json.dumps(CSVBTN)).replace("'%%SUMMARY%%'", json.dumps(SUMMARY))
    only = sys.argv[1:]
    for p in PAGES:
        if only and p['key'] not in only:
            continue
        if not os.path.exists(os.path.join(HERE, 'src', 'pages', p['key'] + '.js')):
            print('skip', p['key']); continue
        needs = {'dv-behaviour', 'dv-legend', 'dv-render'} | set(p['behaviours'])
        foot = splices(tmp)
        html = page_html(p).replace('FOOTER_SPLICE', foot).replace('BEHAVIOUR_SPLICES', engine_tags(needs))
        js = open(os.path.join(HERE, 'src', 'pages', p['key'] + '.js'), encoding='utf-8').read()
        html = html.replace('%%DATA%%', data).replace('%%CORE%%', core).replace('%%PAGE%%', js)
        manifest = {
            '$what': 'Behaviour manifest (ADS-generate-from-canon Output): what each control drives and where its state persists.',
            'borrowed': ['knowledge/canon/%s.js (loaded by <script src>, unmodified)' % n for n in ENGINE if n in needs],
            'authored': ['APP core (inline): shared filters, persistence, theme, Filter-toolbar-bar menus, Data-grid sort/search/page, Drawer, Modals, Toast, CSV export, dvRender calls',
                         'page script (inline): %s charts, KPIs, grids and workflows' % p['key'],
                         'Segmented-control indicator: the snippet moveInd() extended to every .seg on the page'],
            'controls': {
                'entity / region / date menus': 'every KPI, chart, grid and card on the page; URL query (entity, region, days) + localStorage; carried on every in-app link',
                'chip remove / Clear all': 'resets that filter / all filters; same persistence',
                'Light / Dark': 'data-theme on <html>; localStorage; applied before first paint',
                'navigation collapse': 'Sidebar rail; localStorage',
                'grid search, sort, page, rows per page': 'that grid; URL p.<grid>.* + localStorage',
                'row (click or Enter)': 'opens the record in the Drawer; URL p.open',
                'workflow actions (approve, reject, acknowledge, request, reply, run, reset)': 'validated in a Modal or Drawer form; recorded in localStorage (hsbc-ceo-proto.v1.work) with an audit entry',
                'export buttons': 'download a CSV of the rows in view',
                'chart legend, tooltip, table, copy CSV': 'dv-legend / dv-behaviour, unmodified'},
            'fallback': 'JavaScript off: the shell, header, filter bar and empty bento tiles render; no figures, charts or records (every number is drawn from DATA by script). Not a supported mode for this prototype.'}
        html = html.replace('</head>', '<script type="application/json" id="behaviour-manifest">\n' + json.dumps(manifest, indent=1, ensure_ascii=False) + '\n</script>\n</head>', 1)
        path = os.path.join(OUT, p['file'])
        open(path, 'w', encoding='utf-8').write(html)
        subprocess.run([sys.executable, os.path.join(PACK, 'knowledge', 'gen_provenance_receipt.py'), '--mint', path], check=True, cwd=PACK, stdout=subprocess.DEVNULL)
        print('built', p['file'], os.path.getsize(path))

if __name__ == '__main__':
    main()
