import os, re, json
import core
from core import esc, figure, splice, element
import data as D

OUT = os.path.join(core.W, "out")
PAGES = [  # file, key, nav label, page title, nav icon, group
  ("index.html", "overview", "Overview", "Overview", "ic-dashboard", None),
  ("accounts.html", "accounts", "Accounts and transactions", "Accounts and transactions", "ic-account", "Money"),
  ("liquidity.html", "liquidity", "Liquidity and funding", "Liquidity and funding", "ic-liquidity", "Money"),
  ("payments.html", "payments", "Payments and approvals", "Payments and approvals", "ic-payments", "Money"),
  ("fx.html", "fx", "FX and markets", "FX and markets", "ic-fx", "Markets and risk"),
  ("risk.html", "risk", "Risk and limits", "Risk and limits", "ic-risk", "Markets and risk"),
  ("trade.html", "trade", "Trade finance", "Trade finance", "ic-trade", "Markets and risk"),
  ("reports.html", "reports", "Reports", "Reports", "ic-report", "Insight and service"),
  ("messages.html", "messages", "Messages and requests", "HSBC messages and service requests", "ic-message", "Insight and service"),
  ("settings.html", "settings", "Settings", "Settings", "ic-settings", None),
]
ICON = lambda i: '<svg viewBox="0 0 18 18" aria-hidden="true"><use href="#%s"/></svg>' % i

def nav_links(cur, rail_ids=True, prefix="nw"):
    groups, order = {}, []
    for f, k, lab, t, ic, g in PAGES:
        if k == "settings": continue
        if g not in groups: groups[g] = []; order.append(g)
        groups[g].append((f, k, lab, ic))
    out = []
    for gi, g in enumerate(order):
        items = "".join('<li><a class="sn-link" href="%s" data-nav="%s"%s><span class="si" aria-hidden="true">%s</span><span class="sn-label t-cm-label">%s</span></a></li>'
                        % (f, k, ' aria-current="page"' if k == cur else "", ICON(ic), esc(lab)) for f, k, lab, ic in groups[g])
        if g is None:
            out.append('<div class="sn-group"><ul>%s</ul></div>' % items)
        else:
            gid = "%s-g%d" % (prefix, gi)
            out.append('<div class="sn-group"><span class="sn-group-label t-cm-caption" id="%s">%s</span><ul aria-labelledby="%s">%s</ul></div>' % (gid, esc(g), gid, items))
    foot = '<div class="sn-foot"><ul><li><a class="sn-link" href="settings.html" data-nav="settings"%s><span class="si" aria-hidden="true">%s</span><span class="sn-label t-cm-label">Settings</span></a></li></ul></div>' % (' aria-current="page"' if cur == "settings" else "", ICON("ic-settings"))
    return "\n".join(out), foot

def shell(cur, title, main):
    links, foot = nav_links(cur)
    slinks, sfoot = nav_links(cur, prefix="ns")
    crumbs = ('<li><a class="crumb t-ed-body-small" href="index.html" data-nav="overview">Home</a></li><li><span class="sep t-ed-body-small" aria-hidden="true">/</span><span class="t-ed-body-small em" aria-current="page">%s</span></li>' % esc(title)
              if cur != "overview" else '<li><span class="t-ed-body-small em" aria-current="page">Home</span></li>')
    return f'''<div class="cn-app-shell-side-nav">
      <div class="sh" data-nav="auto" id="shell">
        <a class="sh-skip t-cm-button" href="#main">Skip to main content</a>
        <header class="sh-appbar">
          <button class="sh-menu" type="button" aria-expanded="false" aria-controls="sheet-shell" aria-label="Open main menu" data-menu="shell">
            {ICON("ic-menu")}
          </button>
          <span class="sh-logo"><img class="sh-mark" data-mode="light" src="../pack/knowledge/assets/logos/masterbrand-light-colour.svg" alt="HSBC" width="315" height="85"><img class="sh-mark" data-mode="dark" src="../pack/knowledge/assets/logos/masterbrand-dark-colour.svg" alt="HSBC" width="315" height="85"></span>
          <div class="sh-actions">
            <button type="button" aria-label="HSBC messages and service requests" data-href="messages.html">{ICON("ic-message")}</button>
            <button type="button" aria-label="Your profile and settings" data-href="settings.html">{ICON("ic-profile")}</button>
          </div>
        </header>
        <div class="sh-body">
          <nav class="sn" aria-label="Main" id="nav-main">
            <div class="sn-head">
              <span class="sn-brand t-cm-label">Meridian Global Holdings</span>
              <button class="sn-toggle" type="button" aria-expanded="true" aria-controls="nav-main-body" aria-label="Collapse navigation" data-navtoggle="shell">
                <svg viewBox="0 0 18 18" aria-hidden="true"><use href="#ic-chevron-left"/></svg>
              </button>
            </div>
            <div class="sn-body" id="nav-main-body">
{links}
            </div>
            {foot}
          </nav>
          <div class="sh-content">
            <nav class="sh-crumbs" aria-label="Breadcrumb"><ol>{crumbs}</ol></nav>
            <main class="sh-main" id="main">
{main}
            </main>
            <footer class="sh-foot" role="contentinfo" aria-label="Legal footer">
              <div class="sh-legal">
                <ul>
                  <li><a class="lnk t-ed-body-small" href="#" data-action="not-in-prototype">Terms and conditions</a></li>
                  <li><a class="lnk t-ed-body-small" href="#" data-action="not-in-prototype">Privacy notice</a></li>
                  <li><a class="lnk t-ed-body-small" href="#" data-action="not-in-prototype">Accessibility statement</a></li>
                </ul>
                <p class="copy t-cm-legal">Prototype with illustrative data. No live banking connection. © HSBC Group 2026.</p>
              </div>
            </footer>
          </div>
        </div>
        <div class="sh-scrim" data-scrim="shell"></div>
        <div class="sh-sheet" id="sheet-shell" tabindex="-1" role="dialog" aria-modal="true" aria-label="Main menu">
          <nav class="sn" aria-label="Main, in menu">
            <div class="sn-head">
              <span class="sn-brand t-cm-label">Meridian Global Holdings</span>
              <button class="sn-toggle" type="button" aria-label="Close main menu" data-close="shell">
                <svg viewBox="0 0 18 18" aria-hidden="true"><use href="#ic-chevron-left"/></svg>
              </button>
            </div>
            <div class="sn-body">
{slinks}
            </div>
            {sfoot}
          </nav>
        </div>
      </div>
    </div>'''

# ------------------------------------------------------------------ small component copies
_DD = core.snip("Dropdown")
CHECK = re.search(r'<li class="opt" role="option" aria-selected="true" tabindex="-1">United Kingdom (<svg.*?</svg>)</li>', _DD, re.S).group(1)
def dropdown(did, label, opts, attrs=""):
    lis = "".join('<li class="opt" role="option" aria-selected="%s" tabindex="-1" data-value="%s">%s %s</li>' % ("true" if i == 0 else "false", esc(v), esc(t), CHECK) for i, (v, t) in enumerate(opts))
    return f'''<div class="cn-dropdown"><div class="dd boxed" id="{did}" {attrs}>
        <label id="{did}-l" for="{did}-t">{esc(label)}</label>
        <button class="trigger" id="{did}-t" type="button" role="combobox" aria-haspopup="listbox" aria-expanded="false" aria-controls="{did}-m" aria-labelledby="{did}-l {did}-t">
          <span class="ddval">{esc(opts[0][1])}</span>
          <span class="chev" aria-hidden="true">▾</span>
        </button>
        <ul class="menu" id="{did}-m" role="listbox" aria-labelledby="{did}-l" tabindex="-1">{lis}</ul>
      </div></div>'''

def seg(sid, label, opts, size="md", attrs=""):
    bs = "".join('<button type="button" aria-pressed="%s" data-value="%s">%s</button>' % ("true" if i == 0 else "false", esc(v), esc(t)) for i, (v, t) in enumerate(opts))
    return f'<div class="cn-segmented-control"><div class="seg {size}" role="group" aria-label="{esc(label)}" id="{sid}" {attrs}><span class="ind" aria-hidden="true"></span>{bs}</div></div>'

def btn(label, kind="tertiary", attrs=""):
    return '<button class="btn %s" type="button" %s>%s</button>' % (kind, attrs, esc(label))

def page_header(title, eyebrow, actions=""):
    return f'''<div class="cn-page-header-lockup"><div class="ph-outer"><div class="ph">
          <div class="ph-row">
            <div class="ph-titleblock">
              <span class="eyebrow t-cm-caption">{esc(eyebrow)}</span>
              <h1 class="ph-title t-cm-heading">{esc(title)}</h1>
            </div>
            <div class="ph-actions">{actions}</div>
          </div>
        </div></div></div>'''

ENT_OPTS = [("all", "All entities")] + [(e["id"], e["name"]) for e in D.entities]
REG_OPTS = [("all", "All regions")] + [(r["id"], r["name"]) for r in D.REGIONS]
RANGE_OPTS = [("30", "30 days"), ("14", "14 days"), ("7", "7 days")]
THEME_OPTS = [("light", "Light"), ("dark", "Dark")]
def filter_row():
    return f'''<div class="cn-layout-utilities"><div class="l-row" data-gap="m" data-align="end" role="group" aria-label="Shared filters">
        {dropdown("f-entity", "Entity", ENT_OPTS, 'data-filter="entity"')}
        {dropdown("f-region", "Region", REG_OPTS, 'data-filter="region"')}
        {seg("f-range", "Date range", RANGE_OPTS, "md", 'data-filter="range"')}
        {seg("f-theme", "Colour mode", THEME_OPTS, "md", 'data-pref="theme"')}
        <p class="t-cm-caption" id="asof">GBP at illustrative FX rates, as at {esc(D.DATA["asOfLabel"])}. Not live.</p>
      </div></div>'''

# ------------------------------------------------------------------ bento grammar (canon classes, template-dashboard-bento $bentoGrammar)
def group(role, label, tiles, gid=""):
    return f'''<section class="c-bento__tile c-bento tpl-group tpl-group-{role}" data-bento-role="dashboard" data-c="6" data-r="1" aria-label="{esc(label)}"{' id="%s"' % gid if gid else ''}>
              <div class="c-bento__grid">
{tiles}
              </div>
            </section>'''
def panel(inner, c=6, pid="", extra=""):
    return f'''<div class="c-bento__tile stat-card" data-c="{c}" data-r="1"{' id="%s"' % pid if pid else ''} {extra}>
{inner}
                </div>'''
def phead(title, link=None, hid=""):
    ln = ('<div class="cn-section-heading-lockup"><a class="arrow" href="%s"><span class="lbl t-cm-button">%s</span><span class="tip" aria-hidden="true"><svg><use href="#sh-arrow-tip"/></svg></span></a></div>' % link) if link else ""
    return '<div class="tpl-panel-head"><h3 class="t-cm-section-label"%s>%s</h3>%s</div>' % (' id="%s"' % hid if hid else "", esc(title), ln)
def wall(label, groups):
    return f'''<section class="ceo-ground" aria-label="{esc(label)}"><div class="cn-template-dashboard-bento"><div class="tpl-page"><div class="tpl-bento-stack">
          <div class="c-bento tpl-wall" data-bento-role="dashboard" aria-label="{esc(label)}">
            <div class="c-bento__grid">
{"".join(groups)}
            </div>
          </div>
        </div></div></div></section>'''

def kpi(key, label, href, per="vs start of period"):
    return f'''<div class="c-bento__tile" data-c="1" data-r="1"><div class="cn-kpi-tile"><div class="kpi-tile as-link" role="group" aria-label="{esc(label)}" data-kpi="{key}">
      <p class="kpi-lbl t-cm-caption"><a class="kpi-link" href="{href}">{esc(label)}</a></p>
      <span class="kpi-val t-cm-figure-4"><span class="unit">£</span><span data-f="value">–</span></span>
      <span class="kpi-delta flat" data-carries="symbol label"><span class="glyph" aria-hidden="true"><svg><use href="#kpi-flat"/></svg></span><span class="t-cm-figure-6" data-f="delta">–</span><span class="kpi-per t-cm-legal" data-f="per">{esc(per)}</span></span>
      <div class="kpi-spark">
        <svg class="spark-inline" data-trend="flat" viewBox="0 0 200 48" preserveAspectRatio="none" aria-hidden="true" data-bespoke="chart canvas — dataviz geometry, not an icon (validate-dataviz territory)">
          <line class="dv-base" x1="3" y1="45" x2="197" y2="45"/>
          <polygon class="dv-area" points="3.0,45 197.0,45"/>
          <polyline class="dv-series" points="3.0,45 197.0,45"/>
        </svg>
      </div>
      <span class="kpi-chev" aria-hidden="true"><svg><use href="#kpi-chev"/></svg></span>
    </div></div></div>'''

def grid_panel(title_hint, actions=""):
    head = '<div class="tpl-panel-head"><h3 class="t-cm-section-label" id="gridHead">%s</h3><div class="cn-layout-utilities"><div class="cn-button"><div class="l-row" data-gap="s">%s</div></div></div></div>' % (esc(title_hint), actions)
    inner = head + '\n<div class="cn-data-grid">\n' + splice("Data-grid", ".dg", "Data-grid#grid") + "\n" + splice("Data-grid", "#dgHint", "Data-grid#hint") + "\n" + splice("Data-grid", "#dgStatus", "Data-grid#status") + "\n</div>"
    return panel(inner, 6, "records")

def list_panel(lid, title, c=3, search_label="Search", tools=""):
    return panel(f'''{phead(title, hid=lid + "-h")}
      <div class="cn-layout-utilities"><div class="l-stack" data-gap="m">
        <div class="l-row" data-gap="m" data-align="end">
          <div class="cn-search-field"><div class="search boxed">
            <span class="mag" aria-hidden="true"><svg viewBox="0 0 18 18" aria-hidden="true"><use href="#ic-search"/></svg></span>
            <input type="search" id="{lid}-q" aria-label="{esc(search_label)}" placeholder="{esc(search_label)}" value="">
          </div></div>
          {tools}
        </div>
        <p class="t-cm-caption" id="{lid}-count" aria-live="polite"></p>
        <div class="cn-list-items"><ul class="list" id="{lid}" aria-labelledby="{lid}-h"></ul></div>
        <div class="cn-pagination"><nav class="pg" aria-label="{esc(title)} pages" id="{lid}-pg"><ul></ul></nav></div>
      </div></div>''', c, lid + "-panel")

def drill_panel_links(pid):
    return '<div class="cn-tags"><div class="row" id="%s" aria-label="Drill through to positions by region"></div></div>' % pid

# ------------------------------------------------------------------ pages
def page_overview():
    g1 = group("lead", "Financial resilience — can we fund our plans?", "\n".join([
        kpi("cash", "Cash", "accounts.html"), kpi("liquidity", "Available liquidity", "liquidity.html"),
        kpi("headroom", "Funding headroom", "liquidity.html"), kpi("outflows", "Committed outflows, next 30 days", "liquidity.html", "vs 30-day average")]), "q1")
    g2 = group("evidence", "Financial resilience — cash, liquidity and facilities", "\n".join([
        panel(figure("multiline", "ov-liq", "Cash, available liquidity and funding headroom", "Cash, available liquidity and funding headroom by day, GBP millions", ["Day", "Cash (£m)", "Available liquidity (£m)", "Funding headroom (£m)"], ["Cash", "Available liquidity", "Funding headroom"])),
        panel(figure("bullet", "ov-fac", "Committed facilities: how much is drawn", "Committed facility utilisation against the 75% policy ceiling, per cent", ["Facility", "Drawn (%)", "Policy ceiling (%)"]))]))
    g3 = group("evidence", "Risk outlook — where are we exposed?", "\n".join([
        panel(figure("stacked-column", "ov-exp", "Exposure by region and currency", "Exposure by region, split by currency, GBP millions", ["Region", "USD", "EUR", "GBP", "Asian currencies", "Other"], ["USD", "EUR", "GBP", "Asian currencies", "Other"]) +
              '\n<p class="t-cm-caption">Select a column or a region below to drill through to its positions and limits.</p>\n' + drill_panel_links("ov-drill")),
        panel(figure("donut", "ov-ccy", "Share of exposure by currency", "Share of total exposure by currency, GBP millions", ["Currency", "Exposure (£m)"], ["USD", "EUR", "GBP", "HKD", "Other"]))]), "q2")
    g4 = group("context", "Decisions — what needs my attention?", "\n".join([
        panel(phead("Pending approvals", ("payments.html", "Open the approval queue")) + '<div id="ov-approvals"></div>', 3, "ov-approvals-card"),
        panel(phead("Material risk exceptions", ("risk.html", "Open risk and limits")) + '<div id="ov-exceptions"></div>', 3, "ov-exceptions-card")]), "q3")
    return wall("Overview dashboard", [g1, g2, g3, g4])

def page_accounts():
    g1 = group("evidence", "Balances over the period", "\n".join([
        panel(figure("stacked-area", "ac-bal", "Balances by region", "Cash balances by day, stacked by region, GBP millions", ["Day"] + [r["name"] for r in D.REGIONS], [r["name"] for r in D.REGIONS])),
        panel(figure("bar", "ac-ent", "Balance by entity", "Closing cash balance by entity, GBP millions", ["Entity", "Balance (£m)"]))]))
    g2 = group("evidence", "Transactions", grid_panel("Transactions", btn("Open selected", "secondary", 'data-action="open-selected"') + btn("Export CSV", "tertiary", 'data-action="export-grid"')))
    return wall("Accounts and transactions", [g1, g2])

def page_liquidity():
    g1 = group("lead", "Liquidity position", "\n".join([
        kpi("liquidity", "Available liquidity", "#liq-flow"), kpi("headroom", "Funding headroom", "#liq-fac-panel"),
        kpi("undrawn", "Undrawn committed facilities", "#liq-fac-panel"), kpi("trapped", "Restricted cash", "risk.html")]))
    g2 = group("evidence", "Cash flow and facilities", "\n".join([
        panel(figure("combo", "liq-flow", "Daily net cash flow and available liquidity", "Daily net cash flow (columns, GBP millions) and available liquidity (line, GBP millions)", ["Day", "Net cash flow (£m)", "Available liquidity (£m)"], ["Net cash flow", "Available liquidity"])),
        panel(figure("bullet", "liq-fac", "Facility utilisation against policy ceiling", "Committed facility utilisation against the 75% policy ceiling, per cent", ["Facility", "Drawn (%)", "Policy ceiling (%)"]) + '\n<dl class="summary" id="liq-fac-list"></dl>', 6, "liq-fac-panel")]))
    g3 = group("evidence", "Cash-flow forecast", grid_panel("Cash-flow forecast, next 30 days", btn("Export CSV", "tertiary", 'data-action="export-grid"')))
    return wall("Liquidity and funding", [g1, g2, g3])

def page_payments():
    g1 = group("evidence", "Payment flows", "\n".join([
        panel(figure("column", "pay-daily", "Daily payment outflows", "Value of payments released per day, GBP millions", ["Day", "Outflows (£m)"])),
        panel(figure("pie", "pay-method", "Approval queue by payment method", "Value awaiting approval by payment method, GBP millions", ["Method", "Value (£m)"], ["SWIFT", "CHAPS", "SEPA credit transfer", "Fedwire", "Other"]))]))
    acts = btn("Review selected", "secondary", 'data-action="open-selected"') + btn("Approve selected", "primary", 'data-action="bulk-approve"') + btn("Export CSV", "tertiary", 'data-action="export-grid"')
    g2 = group("evidence", "Approval queue", grid_panel("Payments — select a row to review it", acts))
    return wall("Payments and approvals", [g1, g2])

def page_fx():
    g1 = group("evidence", "Rates", "\n".join([
        panel(figure("candlestick", "fx-ohlc", "GBP/USD daily range", "GBP/USD open, high, low and close by day, illustrative", ["Day", "Open", "High", "Low", "Close"])),
        panel(figure("multiline", "fx-idx", "Sterling against the group's currencies", "Sterling against six currencies, indexed to 100 at the start of the period", ["Day", "GBP/USD", "EUR/GBP", "GBP/HKD", "GBP/SGD", "GBP/CNY"], ["GBP/USD", "EUR/GBP", "GBP/HKD", "GBP/SGD", "GBP/CNY"]))]))
    g2 = group("evidence", "Exposure and hedging", "\n".join([
        panel(figure("butterfly-h", "fx-nat", "Receivables against payables, next 30 days", "Forecast receivables and payables by currency, next 30 days, GBP millions", ["Currency", "Receivables (£m)", "Payables (£m)"], ["Receivables", "Payables"])),
        panel(phead("Illustrative rates and hedge cover") + '<div class="cn-summary"><dl class="summary" id="fx-rates"></dl></div>')]))
    g3 = group("evidence", "Deals", grid_panel("FX deals", btn("Export CSV", "tertiary", 'data-action="export-grid"')))
    return wall("FX and markets", [g1, g2, g3])

def page_risk():
    g1 = group("evidence", "Exposure against limits", "\n".join([
        panel(figure("grouped-column", "rk-reg", "Exposure against limit by region", "Exposure and approved limit by region, GBP millions", ["Region", "Exposure (£m)", "Limit (£m)"], ["Exposure", "Limit"])),
        panel(figure("scatter", "rk-cp", "Bank counterparties: size against limit use", "Bank counterparty exposure (GBP millions, across) against limit utilisation (per cent, up)", ["Exposure (£m)", "Limit used (%)"]))]))
    tools = dropdown("rk-sev", "Severity", [("all", "All severities"), ("High", "High"), ("Medium", "Medium"), ("Low", "Low")], 'data-list-filter="severity"')
    g2 = group("evidence", "Exceptions and limits", "\n".join([
        list_panel("rk-exc", "Risk exceptions", 6, "Search exceptions", tools),
        panel(phead("Limit utilisation", ("#records", "See the positions")) + '<div class="cn-layout-utilities"><div class="l-stack" data-gap="m" id="rk-limits"></div></div>', 6)]))
    g3 = group("evidence", "Positions", grid_panel("Positions behind the exposure", btn("Export CSV", "tertiary", 'data-action="export-grid"')))
    return wall("Risk and limits", [g1, g2, g3])

def page_trade():
    g1 = group("evidence", "Instrument profile", "\n".join([
        panel(figure("histogram", "tr-exp", "Days to expiry", "Live instruments by days to expiry", ["Days to expiry", "Instruments"], ["Instruments"])),
        panel(figure("bar", "tr-type", "Value by instrument type", "Value of live instruments by type, GBP millions", ["Type", "Value (£m)"]))]))
    g2 = group("evidence", "Instruments", grid_panel("Trade finance instruments", btn("Open selected", "secondary", 'data-action="open-selected"') + btn("Export CSV", "tertiary", 'data-action="export-grid"')))
    return wall("Trade finance", [g1, g2])

def page_reports():
    g1 = group("evidence", "Service levels", "\n".join([
        panel(figure("boxplot", "rp-settle", "Payment settlement time by region", "Hours from release to settlement, by region, five-number summary", ["Region", "Minimum", "Q1", "Median", "Q3", "Maximum", "Outlier"])),
        panel(phead("Report runs per day") + figure("spark", "rp-runs", "Report runs per day", "Reports generated per day over the period", ["Day", "Runs"]) + '\n<div class="cn-summary"><dl class="summary" id="rp-runs-note"></dl></div>')]))
    tools = dropdown("rp-fam", "Family", [("all", "All families")] + [(f, f) for f in sorted({r["family"] for r in D.reports})], 'data-list-filter="family"')
    g2 = group("evidence", "Report catalogue", list_panel("rp-list", "Report catalogue", 6, "Search reports", tools))
    return wall("Reports", [g1, g2])

def sr_form():
    cats = [("", "Choose a category")] + [(c, c) for c in D.SRC]
    ents = [("", "Choose an entity")] + [(e["id"], e["name"]) for e in D.entities]
    ta = core.element("Textarea", "#live")
    ta = ta.replace('id="live"', 'id="sr-desc-group"').replace('for="t1"', 'for="sr-desc"').replace('id="t1"', 'id="sr-desc"').replace("t1-help", "sr-desc-help").replace("t1-count", "sr-desc-count").replace("t1-live", "sr-desc-live")
    ta = re.sub(r'(<label class="t-cm-label" for="sr-desc">)[^<]*', r'\1Describe what you need', ta)
    ta = re.sub(r'(<textarea[^>]*>)[^<]*(</textarea>)', r'\1\2', ta)
    ta = ta.replace('maxlength="300"', 'maxlength="600"').replace(">78/300<", ">0/600<")
    ta = re.sub(r'(<p class="tx-help[^>]*>)[^<]*', r'\1At least 20 characters. Do not include passwords or card numbers.', ta)
    return panel(phead("Raise a service request", hid="sr-form-h") + f'''
      <form id="sr-form" novalidate aria-labelledby="sr-form-h"><div class="cn-layout-utilities"><div class="l-stack" data-gap="m">
        <div class="l-row" data-gap="m" data-align="start">
          {dropdown("sr-cat", "Category", cats, 'data-field="category"')}
          {dropdown("sr-ent", "Entity", ents, 'data-field="entity"')}
          {seg("sr-pri", "Priority", [("Normal", "Normal"), ("High", "High")], "md", 'data-field="priority"')}
        </div>
        <div class="cn-input-fields"><div class="field" id="sr-subj-field">
          <div class="lbl"><label for="sr-subj">Subject</label></div>
          <div class="box"><input id="sr-subj" type="text" maxlength="80" aria-describedby="sr-subj-help"></div>
          <p class="help-text" id="sr-subj-help">A short summary, for example "Trace SWIFT payment to supplier".</p>
        </div></div>
        <div class="cn-textarea">{ta}</div>
        <div class="l-row" data-gap="m"><div class="cn-button">{btn("Submit request", "primary", 'data-action="sr-submit"')}</div><div class="cn-button">{btn("Clear", "secondary", 'data-action="sr-clear"')}</div></div>
        <p class="t-cm-caption" id="sr-errors" role="alert"></p>
      </div></div></form>''', 6, "sr-panel")

def page_messages():
    g1 = group("evidence", "Service activity", "\n".join([
        panel(figure("grouped-column", "ms-sr", "Service requests opened and resolved by week", "Service requests opened and resolved per week", ["Week", "Opened", "Resolved"], ["Opened", "Resolved"])),
        panel(figure("pie", "ms-cat", "Messages by category", "Messages received by category, count", ["Category", "Messages"], ["Relationship", "Service update", "Compliance request", "Market insight"]))]))
    tools_m = seg("ms-unread", "Show", [("all", "All"), ("unread", "Unread")], "md", 'data-list-filter="unread"')
    tools_s = dropdown("sr-status", "Status", [("all", "All statuses"), ("Submitted", "Submitted"), ("In progress", "In progress"), ("Awaiting your input", "Awaiting your input"), ("Resolved", "Resolved")], 'data-list-filter="status"')
    g2 = group("evidence", "Inbox and requests", "\n".join([list_panel("ms-list", "HSBC messages", 6, "Search messages", tools_m), list_panel("sr-list", "Service requests", 6, "Search requests", tools_s)]))
    g3 = group("evidence", "New request", sr_form())
    return wall("HSBC messages and service requests", [g1, g2, g3])

def page_settings():
    notif = core.element("Selection-controls", "#sc")
    fields = re.findall(r'<div class="field"><input type="checkbox" id="c1">.*?</div>', notif, re.S)[0]
    def cb(cid, text, checked):
        f = fields.replace('id="c1"', 'id="%s"' % cid).replace('for="c1"', 'for="%s"' % cid).replace(" Email notifications", " " + text)
        if checked: f = f.replace('type="checkbox" id="%s"' % cid, 'type="checkbox" id="%s" checked' % cid)
        return f.replace('<input ', '<input data-pref="notify" ')
    boxes = "\n".join([cb("n-approvals", "Email me when a payment needs my approval", True), cb("n-exceptions", "Email me when a high-severity risk exception is raised", True),
                       cb("n-messages", "Notify me about new HSBC messages", False), cb("n-digest", "Send a daily liquidity digest at 07:00 London", True)])
    prefs = ('<div class="cn-layout-utilities"><div class="l-stack" data-gap="l">'
      + figure("bullet", "st-auth", "Your approval authority this week", "Value you approved this week against your weekly authority, GBP millions", ["Authority", "Used (£m)", "Weekly limit (£m)"])
      + phead("Appearance") + seg("s-theme", "Colour mode", THEME_OPTS, "md", 'data-pref="theme"') + '<p class="t-cm-caption">Applies to every page and is remembered on this device.</p>'
      + phead("Defaults") + '<div class="l-row" data-gap="m" data-align="end">' + dropdown("s-entity", "Default entity", ENT_OPTS, 'data-pref="entity"') + seg("s-range", "Default date range", RANGE_OPTS, "md", 'data-pref="range"') + '</div>'
      + phead("Notifications") + '<div class="cn-selection-controls"><div class="sc">' + boxes + '</div></div>'
      + phead("Prototype data") + '<div class="l-row" data-gap="m"><div class="cn-button">' + btn("Reset prototype data", "secondary", 'data-action="reset-data"') + '</div></div><p class="t-cm-caption">Reset clears approvals, acknowledgements, requests, replies and saved filters made in this browser.</p>'
      + '</div></div>')
    g1 = group("evidence", "Authority and preferences", panel(prefs))
    return wall("Settings", [g1])

BUILDERS = {"overview": page_overview, "accounts": page_accounts, "liquidity": page_liquidity, "payments": page_payments, "fx": page_fx,
            "risk": page_risk, "trade": page_trade, "reports": page_reports, "messages": page_messages, "settings": page_settings}
ACTIONS = {"overview": btn("Export summary CSV", "tertiary", 'data-action="export-summary"'),
           "accounts": "", "payments": "", "reports": "", "settings": ""}
GRID_PAGES = {"accounts", "liquidity", "payments", "fx", "risk", "trade"}
DONUT_PAGES = {"overview", "payments", "messages"}

STYLE = """
  /* PLACEMENT ONLY (rule 3a). The one ground this page paints is the bento section's: the rails'
     bentoBg dial = grey -> --surface-subtle (_bento_edit_rails.json dials.bentoBg.tokens.grey).
     The page ground and the title area are left to the shell. 24px is a ruled spacing stop. */
  .ceo-ground{ background:var(--surface-subtle); padding-top:24px; }
"""
TOKEN_MANIFEST = {"component": "CEO international banking prototype (page)", "vars": {"--surface-subtle": "surface/subtle"},
                  "$note": "The page's own <style> binds one token: the bento section ground (rails dial bentoBg=grey)."}
BEHAVIOUR_MANIFEST = {"$what": "Per-control behaviour sources on this page (rule 2a / s258-D1).", "sources": [
  {"component": "component:data-grid", "script": "knowledge/snippets/Data-grid.reference.html#script", "carried": "verbatim (byte-identical); rows re-bound from DATA by out/app.js through the grid's own DATA array + render()"},
  {"component": "component:app-shell-side-nav", "script": "knowledge/snippets/App-shell-side-nav.reference.html (inline script)", "carried": "verbatim"},
  {"component": "component:dropdown", "script": "knowledge/snippets/Dropdown.reference.html (inline script)", "carried": "verbatim; filter/field wiring added in out/app.js by delegation"},
  {"component": "component:segmented-control", "script": "knowledge/snippets/Segmented-control.reference.html (inline script)", "carried": "verbatim; value wiring added in out/app.js"},
  {"component": "chart-*", "script": "knowledge/canon/dv-render.js + type partials + dv-behaviour.js + dv-legend.js", "carried": "loaded by <script src>; specs built from DATA in out/app.js"},
  {"component": "component:drawer / modals / toast", "script": "none declared in their metas", "carried": "open/close/focus-trap mechanics re-authored in out/app.js after Drawer/Modals/Toast snippet scripts (authored JS)"}]}

def build():
    os.makedirs(OUT, exist_ok=True)
    data_js = json.dumps(D.DATA, separators=(",", ":"), ensure_ascii=False)
    shell_js = core.exec_scripts("App-shell-side-nav")[0]
    dd_js = core.exec_scripts("Dropdown")[0]
    seg_js = core.exec_scripts("Segmented-control")[0]
    grid_js = core.exec_scripts("Data-grid")[0]
    modal = core.element("Modals", "#overlay")
    for a, b in (('id="overlay"', 'id="mOverlay"'), ('"dtitle"', '"mTitle"'), ('"dbody"', '"mBody"'), ('id="close"', 'id="mClose"'), ('id="confirm"', 'id="mConfirm"'), ('id="cancel"', 'id="mCancel"')):
        modal = modal.replace(a, b)
    sprites = "\n".join([core.icon_sprite(), core.sprite("Kpi-tile"), core.sprite("Data-grid"), core.sprite("Toast"), core.sprite("Alert"), core.sprite("Section-heading-lockup")])
    for f, key, lab, title, ic, g in PAGES:
        main = page_header(title, "Meridian Global Holdings · CEO view", ACTIONS.get(key, "")) + "\n" + filter_row() + "\n" + BUILDERS[key]()
        grid = key in GRID_PAGES
        scripts = ['<script>\n{ const DATA = %s;\n  window.CEO_DATA = DATA; }\n</script>' % data_js]
        scripts.append("<script>%s</script>" % shell_js)
        scripts.append("<script>%s</script>" % dd_js)
        scripts.append("<script>%s</script>" % seg_js)
        if grid: scripts.append("<script>%s</script>" % grid_js)
        scripts.append(core.canon_scripts())
        scripts.append('<script src="app.js"></script>')
        if key in DONUT_PAGES: scripts.append('<script src="../pack/knowledge/canon/dv-donut-sweep.js"></script>')
        page = f'''<!DOCTYPE html>
<html lang="en" class="canon" data-apollo-theme="common" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} — HSBC CEO view (prototype)</title>
<!-- Composed from Apollo Spider v1.0.14 (candidate-2) canon. Brief: briefs/2026-09-27-ceo-international-banking-grill.md -->
<link rel="stylesheet" href="../pack/knowledge/canon/canon.css">
<link rel="stylesheet" href="../pack/knowledge/canon/type.css">
<script>try{{var t=localStorage.getItem('ceo.theme');if(t==='dark'||t==='light')document.documentElement.setAttribute('data-theme',t);}}catch(e){{}}</script>
<script type="application/json" id="token-manifest">{json.dumps(TOKEN_MANIFEST)}</script>
<script type="application/json" id="provenance-receipt">{{"pack": "Apollo Spider v1.0.14 candidate-2", "regions": []}}</script>
<script type="application/json" id="behaviour-manifest">{json.dumps(BEHAVIOUR_MANIFEST)}</script>
<style>{STYLE}</style>
</head>
<body data-page="{key}">
{sprites}
{shell(key, title, main)}
<div class="cn-drawer">
{splice("Drawer", "#scrim", "Drawer#scrim")}
{splice("Drawer", "#sheet", "Drawer#sheet")}
</div>
<div class="cn-modals">
{modal}
</div>
<div class="cn-toast">
{splice("Toast", "#toastRegion", "Toast#region")}
</div>
{chr(10).join(scripts)}
</body>
</html>
'''
        open(os.path.join(OUT, f), "w", encoding="utf-8").write(page)
        print("wrote", f, len(page))

if __name__ == "__main__":
    build()
