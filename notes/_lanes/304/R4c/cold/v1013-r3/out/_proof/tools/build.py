import sys, json
sys.path.insert(0, __import__('os').path.dirname(__file__))
from lib import *

NAV = [('index.html','Overview'),('accounts.html','Accounts'),('liquidity.html','Liquidity'),('payments.html','Payments'),('fx.html','FX'),
       ('risk.html','Risk'),('trade.html','Trade'),('reports.html','Reports'),('messages.html','Messages'),('settings.html','Settings')]
FOOT = region_bytes('App-shell-side-nav', '.sh-foot')   # the bento template's own footer region mints a behaviour address its meta denies (FAIL:BEHAVIOUR-ADDRESS-DISAGREES) — same markup, taken from the shell that carries no script
SCRIM = region_bytes('Drawer', '.scrim')
TOASTR = region_bytes('Toast', '.toast-region')
SPRITE = sprite()

HARNESS = '''<style>
/* HARNESS ONLY (generate-from-canon step 3): page-level placement for composed canon parts.
   No hex, no .c-/.cn- redefinition; every length is a spacing token from canon.css. */
body{margin:0;}
.tpl-page{--layout-bento-columns:6;}
.lead-grid{grid-template-columns:repeat(4,minmax(0,1fr));}                   /* restates canon's own lead-row pin (template rule 10a) so the composition gate, which reads only this page's CSS, sees four columns */                                          /* the canon base column count, declared so the composition gate can read it */
.page-pad{padding-inline:var(--gap-fixed-subsection-small);}                 /* 32 = the template's own wall and masthead inset */
.page-section{padding-block:var(--gap-fixed-subsection-medium) var(--gap-fixed-subsection-xsmall);}
.page-section{--dg-vh:none;}                                                  /* Data-grid's own height dial: show the page of rows, no scroll-in-scroll */
.page-section + .page-section{padding-top:var(--padding-fixed-medium);}
.wall-ground{background:var(--wall-ground); padding-block:var(--gap-fixed-subsection-xsmall);}   /* bentoBg grey: the template's own ground var (light resolves to the lightest grey; dark keeps definition against the tiles) */
.cn-filter-toolbar-bar.page-pad{padding-block:var(--padding-fixed-medium);}
.tpl-header.page-pad{padding-top:var(--gap-fixed-subsection-xsmall);}
.chart-note{margin:var(--padding-fixed-medium) 0 0;}
.drill-row{display:flex; flex-wrap:wrap; gap:var(--gap-fixed-content-xsmall) var(--padding-fixed-medium); margin-top:var(--padding-fixed-medium);}
.layer-top{position:relative; z-index:7;}                                      /* a confirm raised from inside the drawer must sit above its scrim (z 5) and sheet (z 6) */
.stack-16{display:flex; flex-direction:column; gap:var(--padding-fixed-medium);}
.set-grid{display:grid; grid-template-columns:repeat(auto-fit,minmax(320px,1fr)); gap:var(--gap-fixed-subsection-xsmall);}
</style>'''

def page(fn, title, h1, lede, body, strip='', actions='', noun='records', search=True, ftb_on=True, export=True):
    nav = ''.join('<a class="t-cm-button" href="%s"%s>%s</a>' % (h, ' aria-current="page"' if h == fn else '', l) for h, l in NAV)
    crumbs = '<li><a class="crumb" href="index.html">Home</a></li>'
    if fn != 'index.html':
        crumbs += '<li><span class="sep" aria-hidden="true"><svg class="chev" viewBox="0 0 18 18"><use href="#ic-chevron"/></svg></span><a class="crumb" href="index.html">CEO overview</a></li>'
    crumbs += '<li><span class="sep" aria-hidden="true"><svg class="chev" viewBox="0 0 18 18"><use href="#ic-chevron"/></svg></span><span class="t-cm-ctl-14" aria-current="page">%s</span></li>' % E(h1)
    theme = ('<div class="cn-segmented-control"><div class="seg s" role="group" aria-label="Theme" id="themeSeg"><span class="ind" aria-hidden="true"></span>'
             '<button type="button" aria-pressed="true" data-theme-set="light">Light</button><button type="button" aria-pressed="false" data-theme-set="dark">Dark</button></div></div>')
    manifest = {"page": fn, "borrowed": {"dv-behaviour": "knowledge/canon/dv-behaviour.js", "dv-legend": "knowledge/canon/dv-legend.js",
                "dv-render": "knowledge/canon/dv-render.js + type partials", "dropdown": "knowledge/snippets/Filter-toolbar-bar.reference.html#script (wireDD pattern, re-authored)",
                "drawer": "knowledge/snippets/Drawer.reference.html#script (open order carried)", "segmented": "knowledge/snippets/Filter-toolbar-bar.reference.html#script (moveInd, re-authored)"},
                "authored": {"app.js": "DATA-driven wiring: filters, grids, drawers, workflows, persistence; chart specs handed to dvRender", "data.js": "the in-page DATA model (rule 13)"}}
    scripts = ''.join('<script src="../pack/knowledge/canon/%s.js"></script>\n' % s for s in
                      ['dv-behaviour', 'dv-legend', 'dv-donut-sweep', 'dv-render', 'dv-render-bar', 'dv-render-line', 'dv-render-stacked-area', 'dv-render-donut',
                       'dv-render-combo', 'dv-render-bullet', 'dv-render-butterfly', 'dv-render-boxplot', 'dv-render-candlestick', 'dv-render-histogram',
                       'dv-render-scatter', 'dv-render-sparkline'])
    doc = '''<!DOCTYPE html>
<html lang="en" class="canon" data-apollo-theme="common" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(title)s — HSBC for CEOs (prototype)</title>
<script>try{var s=JSON.parse(localStorage.getItem('apollo-ceo-proto-v1')||'{}');if(s.theme==='dark'||s.theme==='light'){document.documentElement.setAttribute('data-theme',s.theme);}}catch(e){}</script>
<link rel="stylesheet" href="../pack/knowledge/canon/type.css">
<link rel="stylesheet" href="../pack/knowledge/canon/canon.css">
%(harness)s
<script type="application/json" id="behaviour-manifest">%(manifest)s</script>
</head>
<body data-page="%(pagekey)s">
%(sprite)s
<div class="cn-template-dashboard-bento">
  <header class="sh-masthead">
    <span class="sh-logo"><img class="sh-mark" data-mode="light" src="../pack/knowledge/assets/logos/masterbrand-light-colour.svg" alt="HSBC" width="315" height="85"><img class="sh-mark" data-mode="dark" src="../pack/knowledge/assets/logos/masterbrand-dark-colour.svg" alt="HSBC" width="315" height="85"></span>
    <nav class="sh-nav" aria-label="Primary">%(nav)s</nav>
    <div class="sh-actions">
      <button type="button" aria-label="Search this page" data-action="focus-search"><svg viewBox="0 0 18 18" aria-hidden="true"><use href="#i-search"/></svg></button>
      <button type="button" aria-label="Your profile and settings" data-action="go-settings"><svg viewBox="0 0 18 18" aria-hidden="true"><use href="#i-profile"/></svg></button>
    </div>
  </header>
  <header class="tpl-header l-stack page-pad" data-gap="l">
    <nav class="tpl-crumbs" aria-label="Breadcrumb"><ol class="t-cm-caption">%(crumbs)s</ol></nav>
    <div class="l-row" data-align="end" data-gap="l">
      <div class="tpl-display l-measure"><h1 class="t-ed-heading-2">%(h1)s</h1><p class="t-ed-body">%(lede)s</p></div>
      <div class="tpl-actions l-row" data-gap="m">%(actions)s%(theme)s</div>
    </div>
    <div class="l-row tpl-strip" data-justify="between" data-gap="m" role="region" aria-label="Status"><div class="l-row" data-gap="m" id="strip">%(strip)s</div></div>
  </header>
  <main class="tpl-page" id="tplMain">
%(ftb)s
%(body)s
  </main>
  %(foot)s
  <div class="cn-drawer">%(scrim)s
    <div class="sheet" id="sheet" role="dialog" aria-modal="true" aria-labelledby="dtitle">
      <div class="sheet-head"><h3 class="t-ed-heading-4 em" id="dtitle">Details</h3>
        <button class="close" id="dclose" type="button" aria-label="Close drawer"><svg viewBox="0 0 18 18" aria-hidden="true"><use href="#i-close"/></svg></button></div>
      <div class="sheet-body" id="dbody"></div>
      <div class="sheet-foot" id="dfoot"></div>
    </div>
  </div>
  <div class="layer-top"><div class="cn-modals"><div class="overlay" id="overlay">
    <div class="dialog" role="dialog" aria-modal="true" aria-labelledby="mtitle" aria-describedby="mbody">
      <button class="close" id="mclose" type="button" aria-label="Close dialog"><svg viewBox="0 0 18 18" aria-hidden="true"><use href="#i-close"/></svg></button>
      <h2 id="mtitle">Confirm</h2>
      <p id="mbody"></p>
      <div class="actions"><button class="btn primary" id="mconfirm" type="button">Confirm</button><button class="btn secondary" id="mcancel" type="button">Cancel</button></div>
    </div>
  </div></div></div>
  <div class="cn-toast">%(toast)s</div>
</div>
%(scripts)s<script src="data.js"></script>
<script src="app.js"></script>
</body>
</html>
''' % dict(title=E(h1), harness=HARNESS, manifest=json.dumps(manifest), pagekey=fn.replace('.html', ''), sprite=SPRITE, nav=nav, crumbs=crumbs,
           h1=E(h1), lede=lede, actions=actions, theme=theme, strip=strip, ftb=ftb(noun, search, export) if ftb_on else '', body=body,
           foot=splice('App-shell-side-nav#1', 'App-shell-side-nav', '.sh-foot', FOOT),
           scrim=splice('Drawer#2', 'Drawer', '.scrim', SCRIM), toast=splice('Toast#3', 'Toast', '.toast-region', TOASTR), scripts=scripts)
    open(W + '/out/' + fn, 'w').write(doc)
    print('wrote', fn, len(doc))

def btn(label, action, kind='primary', extra=''):
    return '<button type="button" class="btn %s" data-action="%s"%s>%s</button>' % (kind, action, extra, E(label))

def headcard(title, link=None):
    return '<div class="tpl-panel-head"><h3 class="t-cm-section-label">%s</h3>%s</div>' % (E(title), ('<a class="tpl-link t-cm-caption" href="%s">%s</a>' % link) if link else '')

import pages
pages.build(page, btn, headcard)
