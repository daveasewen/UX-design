from lib import *

def build(page, btn, headcard):
    # ---------------------------------------------------------------- OVERVIEW
    decisions = [
        card(3, headcard('Pending approvals', ('payments.html?status=mine', 'View all')) +
             '<dl class="summary tpl-na-head"><div class="summary__row"><dt class="summary__k t-cm-label">Awaiting your approval <span class="t-cm-legal" id="naCount">—</span></dt><dd class="summary__v t-cm-figure-5" id="naTotal">—</dd></div></dl>'
             '<div class="l-stack" data-gap="m" id="naList"></div>', id='dp08-na', extra=' data-dp08-target tabindex="-1"'),
        card(3, headcard('Material risk exceptions', ('risk.html#exceptions', 'View all')) +
             '<dl class="summary tpl-na-head"><div class="summary__row"><dt class="summary__k t-cm-label">Open and material <span class="t-cm-legal" id="exCount">—</span></dt><dd class="summary__v t-cm-figure-5" id="exWorst">—</dd></div></dl>'
             '<div class="l-stack" data-gap="m" id="exList"></div>', id='risk-na', extra=' tabindex="-1"'),
    ]
    body = wall('Group overview', [
        group('lead', 6, 'Financial resilience — can we fund our plans?', [
            kpi('k-cash', 'Cash', ('Open accounts and balances', 'accounts.html')),
            kpi('k-liq', 'Available liquidity', ('Open liquidity and funding', 'liquidity.html')),
            kpi('k-head', 'Funding headroom', ('Open facilities', 'liquidity.html#facilities')),
            kpi('k-flow', 'Net cash flow', ('Open transactions', 'accounts.html#transactions'))]),
        group('evidence', 4, 'Risk outlook — where are we exposed?', [card(6, chart('ch-exposure', 'stacked-column', 'Where we are exposed, by region and currency',
            'Net exposure by region, split by currency, GBP millions at illustrative rates', legend=True,
            note='Select a bar segment, or a region below, to drill through to its positions and limits.') + '<div class="drill-row" id="drillRow"></div>')]),
        group('context', 2, 'Decisions — what needs my attention?', decisions),
        group('evidence', 4, 'Liquidity trend', [card(6, chart('ch-trend', 'multiline', 'Cash and available liquidity', 'Daily group cash and available liquidity, GBP millions', legend=True))]),
        group('context', 2, 'Currency mix', [card(6, chart('ch-ccymix', 'donut', 'Cash by currency', 'Group cash by currency, GBP millions'))]),
    ])
    strip = ('<span class="status ok" data-carries="label"><span class="dot" aria-hidden="true"></span><span class="t-cm-legal">Balances updated 25 Sep 2026, 07:45 UK</span></span>'
             '<a class="status warn tpl-strip-link" href="#dp08-na" data-dp08-anchor data-carries="label"><span class="dot" aria-hidden="true"></span><span class="t-cm-legal" id="stripApprovals">Awaiting approval</span></a>'
             '<a class="status err tpl-strip-link" href="#risk-na" data-dp08-anchor data-carries="label"><span class="dot" aria-hidden="true"></span><span class="t-cm-legal" id="stripRisk">Risk exceptions</span></a>'
             '<span class="tpl-strip-plain t-cm-legal">GBP reporting · illustrative FX: USD 1.3400 · EUR 1.1601 · HKD 10.4525 per GBP</span>')
    page('index.html', 'Overview', 'Group overview', 'Northwind Group — nine entities, five regions. Can we fund our plans, where are we exposed, and what needs your decision today.',
         body, strip=strip, actions=btn('Review approvals', 'go-approvals'), noun='entities', search=False)

    # ---------------------------------------------------------------- ACCOUNTS
    body = wall('Accounts', [
        group('lead', 6, 'Balances', [kpi('k-cash', 'Cash'), kpi('k-in', 'Money in'), kpi('k-out', 'Money out'), kpi('k-pend', 'Pending transactions')]),
        group('evidence', 4, 'Balance trend', [card(6, chart('ch-bal', 'line', 'Group cash balance', 'Daily closing cash balance across selected accounts, GBP millions'))]),
        group('context', 2, 'Balance by entity', [card(6, chart('ch-byent', 'bar', 'Cash by entity', 'Closing cash balance by entity, GBP millions'))]),
        group('evidence', 6, 'Transaction activity', [card(3, chart('ch-flows', 'grouped-column', 'Money in and out, by day', 'Daily money in and money out, GBP millions', legend=True)),
                                                      card(3, chart('ch-hist', 'histogram', 'Transaction size distribution', 'Number of transactions by GBP value band'))]),
    ])
    body += section('Accounts', grid('gAcc', 'Accounts', [('id','Account',0,110),('entity','Entity',0,230),('name','Type',0,180),('ccy','Currency',0,100),('balance','Balance',1,170),('gbp','GBP equivalent',1,170)], None))
    body += section_id('transactions', 'Transactions', grid('gTx', 'Transactions', [('date','Date',0,120),('id','Transaction',0,120),('entity','Entity',0,200),('type','Type',0,170),('counterparty','Counterparty',0,200),('amount','Amount',1,170),('gbp','GBP equivalent',1,150),('status','Status',0,130)], None))
    page('accounts.html', 'Accounts', 'Accounts and transactions', 'Every account across the group, with 30 days of activity you can search, sort, page and export.', body,
         actions=btn('Export transactions', 'export-csv', 'tertiary'), noun='transactions')

    # ---------------------------------------------------------------- LIQUIDITY
    body = wall('Liquidity and funding', [
        group('lead', 6, 'Liquidity position', [kpi('k-cash', 'Cash'), kpi('k-cu', 'Committed undrawn'), kpi('k-uu', 'Uncommitted undrawn'), kpi('k-liq', 'Available liquidity')]),
        group('evidence', 4, 'Cash flow', [card(6, chart('ch-combo', 'combo', 'Net cash flow and cumulative position', 'Daily net cash flow (columns, GBP millions) and cumulative net flow (line, GBP millions)', legend=True))]),
        group('context', 2, 'Facility utilisation', [card(6, chart('ch-bullet', 'bullet', 'Facility utilisation against policy', 'Drawn as a share of limit, per facility, against the 75% policy marker'))]),
        group('evidence', 4, 'Cash by region', [card(6, chart('ch-area', 'stacked-area', 'Cash by region', 'Daily cash by region, GBP millions, stacked', legend=True))]),
        group('context', 2, 'Maturities', [card(6, chart('ch-mat', 'column', 'Debt maturity profile', 'Facility limits by year of maturity, GBP millions'))]),
    ])
    body += section_id('facilities', 'Facilities', grid('gFac', 'Facilities', [('id','Facility',0,90),('name','Name',0,260),('entity','Entity',0,200),('type','Type',0,150),('limitGbp','Limit (GBP)',1,150),('drawnGbp','Drawn (GBP)',1,150),('util','Utilised',1,110),('maturity','Maturity',0,120)], None))
    page('liquidity.html', 'Liquidity', 'Liquidity and funding', 'Cash, committed and uncommitted headroom, and when the debt falls due. Drawdown requests are simulated.', body,
         actions=btn('Request a drawdown', 'drawdown'), noun='facilities')

    # ---------------------------------------------------------------- PAYMENTS
    body = wall('Payments and approvals', [
        group('lead', 6, 'Approvals', [kpi('k-mine', 'Awaiting your approval'), kpi('k-second', 'Awaiting second approver'), kpi('k-rel', 'Released'), kpi('k-rej', 'Rejected')]),
        group('evidence', 4, 'Payment flow', [card(6, chart('ch-paystack', 'stacked-column', 'Payment value by day and outcome', 'Payment value by due date and status, GBP millions', legend=True))]),
        group('context', 2, 'Payment rails', [card(6, chart('ch-rails', 'pie', 'Released value by payment rail', 'Released payment value by rail, GBP millions'))]),
        group('evidence', 6, 'Beneficiaries', [card(6, chart('ch-benef', 'bar', 'Largest beneficiaries', 'Total payment value by beneficiary, GBP millions, top eight'))]),
    ])
    body += section_id('approvals', 'Payments', grid('gPay', 'Payments', [('id','Payment',0,120),('due','Due',0,110),('entity','Entity',0,190),('beneficiary','Beneficiary',0,190),('rail','Rail',0,150),('amount','Amount',1,170),('gbp','GBP equivalent',1,150),('status','Status',0,210)], None),
        '<div class="cn-segmented-control"><div class="seg s" role="group" aria-label="Show payments" id="payView"><span class="ind" aria-hidden="true"></span><button type="button" aria-pressed="false" data-view="mine">Needs me</button><button type="button" aria-pressed="true" data-view="all">All</button></div></div>')
    page('payments.html', 'Payments', 'Payments and approvals', 'Approve or reject with an audit note. Payments of £5m or more are material and ask you to confirm. Nothing is sent to a bank.', body,
         actions=btn('Approve next', 'next-approval'), noun='payments')

    # ---------------------------------------------------------------- FX
    body = wall('FX and markets', [
        group('lead', 6, 'Rates and exposure', [kpi('k-usd', 'GBP/USD'), kpi('k-eur', 'GBP/EUR'), kpi('k-hkd', 'GBP/HKD'), kpi('k-net', 'Unhedged FX exposure')]),
        group('evidence', 4, 'Sterling against the dollar', [card(6, chart('ch-candle', 'candlestick', 'GBP/USD daily sessions', 'GBP/USD open, high, low and close by session, US dollars per pound'))]),
        group('context', 2, 'Hedging', [card(6, chart('ch-hedge', 'scatter', 'Hedge ratio against exposure', 'Hedge ratio (%) against gross exposure (GBP millions), by currency'))]),
        group('evidence', 6, 'Rate movement', [card(3, chart('ch-index', 'multiline', 'Sterling against each currency', 'Units per pound, rebased to 100 at the start of the period', legend=True)),
                                               card(3, chart('ch-box', 'boxplot', 'Spread of daily moves', 'Distribution of daily moves in units per pound, basis points, by currency'))]),
    ])
    body += section('Illustrative rates', grid('gRates', 'Rates', [('pair','Pair',0,120),('name','Currency',0,200),('quote','Units per GBP',1,150),('gbp','GBP per unit',1,150),('chg','Period change',1,150)], None))
    body += section('FX deals', grid('gDeals', 'FX deals', [('id','Deal',0,120),('trade','Trade date',0,120),('entity','Entity',0,190),('pair','Pair',0,110),('kind','Type',0,170),('side','Side',0,80),('notional','Notional',1,170),('gbp','GBP equivalent',1,150),('status','Status',0,190)], None))
    page('fx.html', 'FX', 'FX and markets', 'Illustrative rates and a simulated quote. Rates are fixed placeholders as at 25 September 2026, not market data.', body,
         actions=btn('Request a quote', 'quote'), noun='deals')

    # ---------------------------------------------------------------- RISK
    body = wall('Risk and limits', [
        group('lead', 6, 'Risk position', [kpi('k-gross', 'Gross exposure'), kpi('k-nop', 'Net open FX position'), kpi('k-lim', 'Limits at warning or breach'), kpi('k-exc', 'Open exceptions')]),
        group('evidence', 4, 'Exposure against limits', [card(6, chart('ch-reglim', 'grouped-column', 'Exposure against limit, by region', 'Gross exposure and limit by region, GBP millions', legend=True))]),
        group('context', 2, 'Long and short', [card(6, chart('ch-fly', 'butterfly-h', 'Long and short, by currency', 'Long and short positions by currency group, GBP millions', legend=True))]),
        group('evidence', 6, 'Limit utilisation', [card(6, chart('ch-limits', 'bullet', 'Limit utilisation', 'Utilisation of each limit as a share of the limit, against an 85% warning marker'))]),
    ])
    body += section_id('exceptions', 'Risk exceptions', grid('gExc', 'Risk exceptions', [('id','Exception',0,120),('raised','Raised',0,110),('title','Exception',0,380),('region','Region',0,150),('severity','Severity',0,110),('status','Status',0,170)], None))
    body += section_id('positions', 'Positions', grid('gPos', 'Positions', [('id','Position',0,110),('entity','Entity',0,190),('region','Region',0,140),('ccy','Currency',0,90),('type','Type',0,160),('counterparty','Counterparty',0,190),('gbp','GBP equivalent',1,150),('hedged','Hedged',1,90),('maturity','Maturity',0,110)], None))
    page('risk.html', 'Risk', 'Risk and limits', 'Where the group is exposed, against which limits, and the exceptions that need an acknowledgement with an audit note.', body,
         actions=btn('Acknowledge next exception', 'next-exception'), noun='positions')

    # ---------------------------------------------------------------- TRADE
    body = wall('Trade finance', [
        group('lead', 6, 'Trade position', [kpi('k-out', 'Outstanding instruments'), kpi('k-exp', 'Expiring in 30 days'), kpi('k-disc', 'Discrepancies to resolve'), kpi('k-line', 'Trade line headroom')]),
        group('evidence', 4, 'Expiry profile', [card(6, chart('ch-expiry', 'column', 'Instruments by month of expiry', 'Outstanding instrument value by month of expiry, GBP millions'))]),
        group('context', 2, 'Instrument mix', [card(6, chart('ch-types', 'donut', 'Outstanding by instrument type', 'Outstanding instrument value by type, GBP millions'))]),
        group('evidence', 6, 'Line utilisation', [card(6, chart('ch-lines', 'bullet', 'Trade line utilisation by entity', 'Outstanding trade instruments as a share of each entity line, against a 75% policy marker'))]),
    ])
    body += section('Instruments', grid('gTf', 'Trade instruments', [('id','Instrument',0,110),('type','Type',0,210),('entity','Entity',0,190),('counterparty','Counterparty',0,180),('amount','Amount',1,160),('gbp','GBP equivalent',1,150),('expiry','Expiry',0,110),('status','Status',0,200)], None))
    page('trade.html', 'Trade', 'Trade finance', 'Letters of credit, guarantees and collections. Amendments raise a simulated service request.', body,
         actions=btn('Request an amendment', 'amend'), noun='instruments')

    # ---------------------------------------------------------------- REPORTS
    body = wall('Reports', [
        group('evidence', 4, 'Flows by region', [card(6, chart('ch-bfly', 'butterfly-v', 'Money in against money out, by region', 'Money in and money out by region over the period, GBP millions', legend=True))]),
        group('context', 2, 'Library', [card(6, chart('ch-cats', 'pie', 'Report library by category', 'Number of reports in the library by category'))]),
        group('evidence', 6, 'Trends', [card(3, chart('ch-spark1', 'spark', 'Group cash, daily', 'Daily group cash, GBP millions')),
                                        card(3, chart('ch-spark2', 'spark', 'Transactions per day', 'Number of transactions per day'))]),
    ])
    body += section('Report library', grid('gRep', 'Reports', [('id','Report',0,110),('name','Name',0,320),('category','Category',0,140),('frequency','Frequency',0,130),('owner','Owner',0,170),('lastRun','Last run',0,130),('runs','Runs',1,90)], None))
    page('reports.html', 'Reports', 'Reports', 'Run and export the group reports. Each export is a CSV of the illustrative data behind it.', body,
         actions=btn('Run board treasury pack', 'run-board'), noun='reports')

    # ---------------------------------------------------------------- MESSAGES
    body = wall('Messages and service requests', [
        group('evidence', 4, 'Request volume', [card(6, chart('ch-srday', 'column', 'Service requests opened, by day', 'Number of service requests opened per day'))]),
        group('context', 2, 'Request status', [card(6, chart('ch-srstat', 'donut', 'Service requests by status', 'Number of service requests by status'))]),
    ])
    body += section_id('inbox', 'Messages from HSBC', grid('gMsg', 'Messages', [('date','Date',0,120),('from','From',0,200),('subject','Subject',0,420),('state','Status',0,130)], None))
    body += section_id('requests', 'Service requests', grid('gSr', 'Service requests', [('id','Request',0,120),('opened','Opened',0,120),('category','Category',0,210),('entity','Entity',0,190),('summary','Summary',0,320),('priority','Priority',0,110),('status','Status',0,200)], None))
    page('messages.html', 'Messages', 'HSBC messages and service requests', 'Read and reply to your bank, and raise service requests. Replies and requests are simulated and stay in this browser.', body,
         actions=btn('New service request', 'new-sr'), noun='requests')

    # ---------------------------------------------------------------- SETTINGS
    notif = ''.join('<div class="field"><input type="checkbox" id="n-%s" data-pref="%s"><label for="n-%s"><span class="box"><svg data-bespoke="checkbox tick, animated stroke-draw control glyph" viewBox="0 0 18 18"><path class="tick" d="M3.5 9.5 L7.5 13.5 L14.5 5"/></svg></span> %s</label></div>' % (k, k, k, l)
                    for k, l in [('approvals', 'Payments awaiting my approval'), ('exceptions', 'Material risk exceptions'), ('messages', 'New messages from HSBC'), ('digest', 'Daily digest at 07:30 UK')])
    body = wall('Settings', [group('evidence', 6, 'Alerts', [card(6, chart('ch-alerts', 'column', 'Alerts you would have received, last 30 days', 'Number of alerts by type over the last 30 days, at your current settings'))])])
    body += ('<section class="page-pad page-section" aria-label="Preferences"><div class="set-grid">'
             '<div class="stack-16"><h2 class="t-ed-heading-4">Appearance</h2><p class="t-ed-body-small">Theme applies to every page and is remembered in this browser.</p>'
             '<div class="cn-segmented-control"><div class="seg md" role="group" aria-label="Theme" id="themeSeg2"><span class="ind" aria-hidden="true"></span><button type="button" aria-pressed="true" data-theme-set="light">Light</button><button type="button" aria-pressed="false" data-theme-set="dark">Dark</button></div></div></div>'
             '<div class="stack-16"><h2 class="t-ed-heading-4">Notifications</h2><div class="cn-selection-controls"><div class="stack-16">%s</div></div></div>'
             '<div class="stack-16"><h2 class="t-ed-heading-4">Demo data</h2><p class="t-ed-body-small">Approvals, acknowledgements, replies, requests and filters are stored in this browser only. Reset returns the prototype to its first state.</p>'
             '<div class="cn-button"><button type="button" class="btn secondary" data-action="reset">Reset demo data</button></div></div>'
             '</div></section>') % notif
    page('settings.html', 'Settings', 'Settings', 'Theme, notifications and the shared filters every page starts from.', body,
         actions='', noun='entities', search=False, export=False)
