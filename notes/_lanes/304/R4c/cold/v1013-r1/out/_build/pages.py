"""Page definitions: the bento wall for each page. Spans use ONLY 6 and 3 (and the template's
4+2 evidence/context pair), every row holds an even number of 3s — the Template-dashboard-bento
law that keeps every band square without a squaring pass. Content is rendered by the page script
from DATA into the hosts named here."""

def kpis(ids_labels):
    tiles = ''.join(
        '<div class="c-bento__tile kpi-tile has-cta" role="group" aria-label="%s" data-c="1" data-r="1" data-kpi="%s"><p class="lbl16 t-cm-caption">%s</p><span class="amt t-cm-figure-3"><span>—</span></span></div>' % (l, i, l)
        for i, l in ids_labels)
    return ('<section class="c-bento__tile c-bento tpl-group tpl-group-lead" data-bento-role="dashboard" data-c="6" data-r="1" aria-label="%s">'
            '<div class="c-bento__grid" id="kpis">%s</div></section>') % ('Headline figures', tiles)

def group(role, c, label, tiles):
    return ('<section class="c-bento__tile c-bento tpl-group tpl-group-%s" data-bento-role="dashboard" data-c="%d" data-r="1" aria-label="%s"><div class="c-bento__grid">%s</div></section>'
            % (role, c, label, ''.join(tiles)))

def chart(host, c=6):
    return '<div class="c-bento__tile stat-card" data-c="%d" data-r="1" id="%s"></div>' % (c, host)

def panel(title, host, c=3, link=None, extra=''):
    head = '<div class="tpl-panel-head"><h3 class="t-cm-section-label">%s</h3>%s</div>' % (
        title, '<a class="tpl-link t-cm-caption" data-app-href="%s" href="%s">%s</a>' % (link[0], link[0], link[1]) if link else '')
    return '<div class="c-bento__tile stat-card" data-c="%d" data-r="1"%s>%s<div id="%s"></div></div>' % (c, extra, head, host)

def btn(label, action, kind='tertiary'):
    return '<button type="button" class="btn %s" data-action="%s">%s</button>' % (kind, action, label)

ALL = {'dv-render-bar', 'dv-render-line', 'dv-render-stacked-area', 'dv-render-donut', 'dv-donut-sweep', 'dv-render-combo', 'dv-render-bullet',
       'dv-render-candlestick', 'dv-render-scatter', 'dv-render-boxplot', 'dv-render-histogram', 'dv-render-butterfly', 'dv-render-sparkline'}

PAGES = [
  dict(file='index.html', key='overview', title='Group overview', crumb='Group overview', h1='Good evening — here is the group today',
       desc='CEO overview: financial resilience, risk outlook and decisions waiting, across every Harbourline entity.',
       sub='Financial resilience, risk outlook and the decisions waiting for you:',
       actions=btn('Export overview (CSV)', 'export-overview') + '<a class="btn primary" data-app-href="payments.html?p.view=mine" href="payments.html?p.view=mine">Review approvals</a>',
       strip='<div class="l-row tpl-strip" data-justify="between" data-gap="m" role="region" aria-label="Status" id="strip"></div>',
       behaviours=['dv-render-bar', 'dv-render-line', 'dv-render-donut', 'dv-donut-sweep', 'dv-render-bullet'],
       wall=kpis([('cash', 'Cash'), ('liq', 'Available liquidity'), ('head', 'Funding headroom'), ('undrawn', 'Undrawn committed facilities')]) +
            group('evidence', 4, 'Risk outlook — where are we exposed?', [chart('host-exposure'), chart('host-liquidity')]) +
            group('context', 2, 'Decisions — what needs my attention?', [panel('Pending approvals', 'na-approvals', 3, ('payments.html?p.view=mine', 'View all'), ' id="dp08-na"'), panel('Material risk exceptions', 'na-exceptions', 3, ('risk.html', 'View all'))]) +
            group('evidence', 6, 'Resilience detail', [chart('host-ccy', 3), chart('host-facilities', 3)])),

  dict(file='accounts.html', key='accounts', title='Accounts and transactions', crumb='Accounts and transactions', h1='Accounts and transactions',
       desc='Balances across 29 HSBC accounts and every transaction in the period, searchable, sortable and paged.',
       sub='Balances and flows across the group’s HSBC accounts:',
       actions=btn('Export transactions (CSV)', 'export-tx'),
       behaviours=['dv-render-bar', 'dv-render-stacked-area', 'dv-render-histogram'],
       wall=kpis([('cash', 'Cash'), ('in', 'Money in'), ('out', 'Money out'), ('net', 'Net flow')]) +
            group('evidence', 4, 'Cash over time', [chart('host-bal')]) +
            group('context', 2, 'Largest balances', [panel('Largest balances', 'acc-top', 3), panel('Pending transactions', 'acc-pending', 3)]) +
            group('evidence', 6, 'Where cash sits and how big the flows are', [chart('host-entity', 3), chart('host-hist', 3)]) +
            group('evidence', 6, 'Transactions', [chart('host-gtx')]) +
            group('evidence', 6, 'Accounts', [chart('host-gacc')])),

  dict(file='liquidity.html', key='liquidity', title='Liquidity and funding', crumb='Liquidity and funding', h1='Liquidity and funding',
       desc='Available liquidity, committed facilities, utilisation and funding headroom after the policy buffer and planned commitments.',
       sub='Can we fund our plans? Cash plus undrawn committed facilities, less the £400m policy buffer and planned commitments:',
       actions=btn('Export facilities (CSV)', 'export-fac') + btn('Request a drawdown', 'drawdown', 'primary'),
       behaviours=['dv-render-bar', 'dv-render-line', 'dv-render-combo', 'dv-render-bullet', 'dv-render-sparkline'],
       wall=kpis([('liq', 'Available liquidity'), ('cash', 'Cash'), ('undrawn', 'Undrawn committed facilities'), ('head', 'Funding headroom')]) +
            group('evidence', 4, 'Liquidity against utilisation', [chart('host-combo')]) +
            group('context', 2, 'Facility headroom', [panel('Most-drawn facilities', 'lim-list', 3), panel('Planned commitments', 'commit-list', 3)]) +
            group('evidence', 6, 'Facility utilisation and trends', [chart('host-bullet', 3), panel('Thirty-day shape', 'sparks', 3)]) +
            group('evidence', 6, 'Facilities', [chart('host-gfac')])),

  dict(file='payments.html', key='payments', title='Payments and approvals', crumb='Payments and approvals', h1='Payments and approvals',
       desc='Payments awaiting your approval, with dual control above £10m, validated approval and rejection, and a full audit trail.',
       sub='Payments that need your approval, and everything already through:',
       actions=btn('Export payments (CSV)', 'export-pay'),
       behaviours=['dv-render-bar', 'dv-render-line', 'dv-render-scatter'],
       wall=kpis([('mine', 'Awaiting your approval'), ('second', 'Awaiting second approver'), ('released', 'Released'), ('held', 'Held or rejected')]) +
            group('evidence', 4, 'Pending value by currency', [chart('host-byccy')]) +
            group('context', 2, 'Needs you', [panel('Oldest waiting for you', 'pay-mine', 3), panel('Dual-control rule', 'pay-rule', 3)]) +
            group('evidence', 6, 'Size, timing and flow', [chart('host-scatter', 3), chart('host-flow', 3)]) +
            group('evidence', 6, 'Payments', [chart('host-gpay')])),

  dict(file='fx.html', key='fx', title='FX and markets', crumb='FX and markets', h1='FX and markets',
       desc='Illustrative GBP rates, 30-day price action, net currency exposure, hedges and quote requests.',
       sub='Currency exposure and hedging, with illustrative rates to GBP:',
       actions=btn('Export hedges (CSV)', 'export-hedge') + btn('Request a hedge quote', 'quote', 'primary'),
       behaviours=['dv-render-bar', 'dv-render-line', 'dv-render-candlestick', 'dv-render-butterfly'],
       wall=kpis([('net', 'Net open exposure'), ('hedge', 'Hedged notional'), ('mtm', 'Forward revaluation'), ('rec', 'Foreign-currency receivables')]) +
            group('evidence', 4, 'Price action', [chart('host-candle')]) +
            group('context', 2, 'Rates', [panel('Illustrative rates to GBP', 'rates', 3), panel('About these rates', 'rate-note', 3)]) +
            group('evidence', 6, 'Exposure and relative moves', [chart('host-bfly', 3), chart('host-index', 3)]) +
            group('evidence', 6, 'Hedges', [chart('host-ghedge')])),

  dict(file='risk.html', key='risk', title='Risk and limits', crumb='Risk and limits', h1='Risk and limits',
       desc='Regional, currency and counterparty exposure against limits, the underlying positions, and exceptions to acknowledge with an audit note.',
       sub='Where are we exposed, and what has broken or is close to breaking:',
       actions=btn('Export positions (CSV)', 'export-pos') + btn('Export exceptions (CSV)', 'export-exc'),
       behaviours=['dv-render-bar', 'dv-render-scatter', 'dv-render-boxplot'],
       wall=kpis([('net', 'Net exposure'), ('gross', 'Gross exposure'), ('cp', 'Bank counterparty exposure'), ('unhedged', 'Unhedged foreign exposure')]) +
            group('evidence', 4, 'Exposure against limit', [chart('host-regions')]) +
            group('context', 2, 'Regional limits', [panel('Closest to their regional limit', 'reg-limits', 3), panel('Open exceptions', 'exc-summary', 3)]) +
            group('evidence', 6, 'Counterparties', [chart('host-cp', 3), chart('host-box', 3)]) +
            group('evidence', 6, 'Exceptions', [chart('host-gexc')]) +
            group('evidence', 6, 'Underlying positions', [chart('host-gpos')])),

  dict(file='trade.html', key='trade', title='Trade finance', crumb='Trade finance', h1='Trade finance',
       desc='Letters of credit, guarantees and collections: what is outstanding, what expires, and discrepancies to decide.',
       sub='Letters of credit, guarantees and collections outstanding with HSBC:',
       actions=btn('Export instruments (CSV)', 'export-tf'),
       behaviours=['dv-render-bar', 'dv-render-butterfly', 'dv-render-donut'],
       wall=kpis([('out', 'Outstanding'), ('imp', 'Import instruments'), ('exp', 'Export instruments'), ('gua', 'Guarantees and standbys')]) +
            group('evidence', 4, 'Imports against exports', [chart('host-bfv')]) +
            group('context', 2, 'Needs a decision', [panel('Discrepancies and amendments', 'tf-action', 3), panel('Expiring in 30 days', 'tf-expiring', 3)]) +
            group('evidence', 6, 'Mix and maturity', [chart('host-pie', 3), chart('host-expiry', 3)]) +
            group('evidence', 6, 'Instruments', [chart('host-gtf')])),

  dict(file='reports.html', key='reports', title='Reports', crumb='Reports', h1='Reports',
       desc='Scheduled and on-demand treasury reports, run history, and CSV exports built from the data on screen.',
       sub='Run a report now or see what has run:',
       actions=btn('Export run history (CSV)', 'export-runs'),
       behaviours=['dv-render-bar', 'dv-render-donut'],
       wall=kpis([('runs', 'Report runs'), ('sched', 'Scheduled runs'), ('manual', 'Run by your team'), ('exports', 'Your exports')]) +
            group('evidence', 4, 'Runs over time', [chart('host-runs')]) +
            group('context', 2, 'Recent activity', [panel('Your recent exports', 'rep-audit', 3), panel('Board pack', 'rep-board', 3)]) +
            group('evidence', 6, 'Mix and run time', [chart('host-cat', 3), chart('host-time', 3)]) +
            group('evidence', 6, 'Reports', [chart('host-grep')])),

  dict(file='messages.html', key='messages', title='HSBC messages and service requests', crumb='Messages and service requests', h1='HSBC messages and service requests',
       desc='Secure messages from HSBC and service requests with their progress against service levels.',
       sub='Secure messages from HSBC, and requests you have raised:',
       actions=btn('Export requests (CSV)', 'export-sr') + btn('New service request', 'new-sr', 'primary'),
       behaviours=['dv-render-bar', 'dv-render-bullet'],
       wall=kpis([('unread', 'Unread messages'), ('action', 'Messages needing action'), ('open', 'Open service requests'), ('input', 'Waiting for your input')]) +
            group('evidence', 4, 'Requests over time', [chart('host-srs')]) +
            group('context', 2, 'Your relationship team', [panel('Waiting for you', 'sr-waiting', 3), panel('Contacts', 'contacts', 3)]) +
            group('evidence', 6, 'Service levels and topics', [chart('host-sla', 3), chart('host-topics', 3)]) +
            group('evidence', 6, 'Messages', [chart('host-gmsg')]) +
            group('evidence', 6, 'Service requests', [chart('host-gsr')])),

  dict(file='settings.html', key='settings', title='Settings', crumb='Settings', h1='Settings', nofilters=True,
       desc='Colour mode, default view, notification preferences and the prototype’s stored data.',
       sub='How this view behaves for you. Changes save as you make them — shown for',
       behaviours=['dv-render-bar'],
       wall=group('evidence', 6, 'Preferences', [panel('Appearance', 'set-appearance', 3), panel('Default view', 'set-default', 3)]) +
            group('evidence', 6, 'Notifications and data', [panel('Notifications', 'set-notify', 3), panel('Prototype data', 'set-data', 3)]) +
            group('evidence', 6, 'Your activity', [chart('host-activity')])),
]
