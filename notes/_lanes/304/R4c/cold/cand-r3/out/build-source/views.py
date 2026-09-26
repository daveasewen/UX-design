# View layout — exec'd by build.py. Every group answers ONE question (rule 7b); its aria-label is that question.
Q1 = 'Financial resilience — can we fund our plans?'
Q2 = 'Risk outlook — where are we exposed?'
Q3 = 'Decisions — what needs my attention?'

TX_COLS = [('id', 'Reference', 'txt'), ('date', 'Date', 'txt'), ('entity', 'Entity', 'txt'), ('counterparty', 'Counterparty', 'txt'),
           ('type', 'Type', 'txt'), ('ccy', 'Currency', 'txt'), ('amount', 'Amount', 'num'), ('gbp', 'GBP equivalent', 'num')]
ACC_COLS = [('id', 'Account', 'txt'), ('name', 'Name', 'txt'), ('entity', 'Entity', 'txt'), ('region', 'Region', 'txt'),
            ('ccy', 'Currency', 'txt'), ('balance', 'Balance', 'num'), ('gbp', 'GBP equivalent', 'num')]
FAC_COLS = [('id', 'Facility', 'txt'), ('name', 'Name', 'txt'), ('entity', 'Borrower', 'txt'), ('type', 'Type', 'txt'),
            ('limit', 'Limit (£m)', 'num'), ('drawn', 'Drawn (£m)', 'num'), ('util', 'Utilisation', 'num'), ('maturity', 'Matures', 'txt')]
PAY_COLS = [('id', 'Payment', 'txt'), ('valueDate', 'Value date', 'txt'), ('entity', 'Entity', 'txt'), ('beneficiary', 'Beneficiary', 'txt'),
            ('ccy', 'Currency', 'txt'), ('amount', 'Amount', 'num'), ('gbp', 'GBP equivalent', 'num'), ('status', 'Status', 'txt')]
DEAL_COLS = [('id', 'Deal', 'txt'), ('trade', 'Traded', 'txt'), ('entity', 'Entity', 'txt'), ('product', 'Product', 'txt'),
             ('pair', 'Pair', 'txt'), ('notional', 'Notional (£m)', 'num'), ('rate', 'Rate', 'num'), ('maturity', 'Matures', 'txt'), ('mtm', 'Mark to market (£k)', 'num')]
POS_COLS = [('id', 'Position', 'txt'), ('entity', 'Entity', 'txt'), ('region', 'Region', 'txt'), ('counterparty', 'Counterparty', 'txt'),
            ('ccy', 'Currency', 'txt'), ('product', 'Product', 'txt'), ('gbp', 'Exposure (£m)', 'num')]
LIM_COLS = [('id', 'Limit', 'txt'), ('name', 'Limit on', 'txt'), ('kind', 'Kind', 'txt'), ('region', 'Region', 'txt'),
            ('limit', 'Limit (£m)', 'num'), ('used', 'Used (£m)', 'num'), ('util', 'Utilisation', 'num'), ('status', 'Status', 'txt')]
EXC_COLS = [('id', 'Exception', 'txt'), ('raised', 'Raised', 'txt'), ('entity', 'Entity', 'txt'), ('title', 'Exception', 'txt'),
            ('severity', 'Severity', 'txt'), ('status', 'Status', 'txt')]
TF_COLS = [('id', 'Instrument', 'txt'), ('type', 'Type', 'txt'), ('entity', 'Applicant', 'txt'), ('counterparty', 'Beneficiary', 'txt'),
           ('ccy', 'Currency', 'txt'), ('amount', 'Amount', 'num'), ('expiry', 'Expires', 'txt'), ('status', 'Status', 'txt')]
REP_COLS = [('id', 'Report', 'txt'), ('name', 'Name', 'txt'), ('category', 'Category', 'txt'), ('frequency', 'Frequency', 'txt'),
            ('lastRun', 'Last run', 'txt'), ('status', 'Status', 'txt'), ('act', 'Action', 'nosort')]
MSG_COLS = [('id', 'Message', 'txt'), ('date', 'Received', 'txt'), ('from', 'From', 'txt'), ('subject', 'Subject', 'txt'),
            ('entity', 'Entity', 'txt'), ('status', 'Status', 'txt')]
SR_COLS = [('id', 'Request', 'txt'), ('opened', 'Opened', 'txt'), ('entity', 'Entity', 'txt'), ('category', 'Category', 'txt'),
           ('subject', 'Subject', 'txt'), ('status', 'Status', 'txt')]

def lead(kpis):
    return group('lead', 6, Q1, [kpi(k, l) for k, l in kpis])

VIEWS = []

VIEWS.append(('overview', 'Overview',
  'Three questions for the group: can we fund our plans, where are we exposed, and what needs your decision. All values are GBP at the illustrative rates shown under FX and markets.',
  wall('overview', 'Group overview', [
    lead([('ov-cash', 'Cash'), ('ov-liq', 'Available liquidity'), ('ov-head', 'Funding headroom'), ('ov-runway', 'Liquidity runway')]),
    group('evidence', 4, Q2, [chart_tile('ov-exposure', 'stacked', 6)]),
    group('context', 2, Q3, [summary_tile('ov-approvals', 'Pending approvals', 6, 1, ('Open payments', '#/payments?status=Pending%20approval')),
                            summary_tile('ov-exceptions', 'Material risk exceptions', 6, 1, ('Open risk and limits', '#/risk?tab=exceptions'))]),
    group('evidence', 3, Q1, [chart_tile('ov-liqtrend', 'stackedarea', 6)]),
    group('evidence', 3, Q2, [chart_tile('ov-ccy', 'donut', 6)]),
  ])))

VIEWS.append(('accounts', 'Accounts and transactions',
  'Balances across every entity and account, and the transactions that moved them. Select a reference to see the full record.',
  wall('accounts', 'Accounts and transactions', [
    group('lead', 6, 'Where does our cash sit, and how is it moving?', [kpi('ac-bal', 'Total balances'), kpi('ac-in', 'Money in'), kpi('ac-out', 'Money out'), kpi('ac-count', 'Transactions')]),
    group('evidence', 3, 'How have balances moved by region?', [chart_tile('ac-trend', 'multiline', 6)]),
    group('evidence', 3, 'Which entities hold the cash?', [chart_tile('ac-entity', 'bar', 6)]),
    group('evidence', 3, 'How large are our transactions?', [chart_tile('ac-hist', 'histogram', 6)]),
    group('evidence', 3, 'Which currencies move the most?', [chart_tile('ac-ccyflow', 'grouped', 6)]),
    group('evidence', 6, 'The records', [records_tile(tabs('ac-tabs', [('tx', 'Transactions'), ('acc', 'Accounts')],
        {'tx': grid('tx', 'Transactions', TX_COLS), 'acc': grid('acc', 'Accounts', ACC_COLS)}))]),
  ])))

VIEWS.append(('liquidity', 'Liquidity and funding',
  'Cash plus undrawn committed facilities, set against the funding the plan needs over the next 90 days.',
  wall('liquidity', 'Liquidity and funding', [
    lead([('lq-liq', 'Available liquidity'), ('lq-undrawn', 'Undrawn committed facilities'), ('lq-head', 'Funding headroom'), ('lq-need', 'Liquidity cover of the 90-day plan')]),
    group('evidence', 3, 'How has liquidity moved by region?', [chart_tile('lq-trend', 'stackedarea', 6)]),
    group('evidence', 3, 'How much of each facility is drawn?', [chart_tile('lq-combo', 'combo', 6)]),
    group('evidence', 6, 'Which facilities are close to their internal limit?', [chart_tile('lq-bullet', 'bullet', 6)]),
    group('evidence', 6, 'The records', [records_tile(grid('fac', 'Funding facilities', FAC_COLS))]),
  ])))

VIEWS.append(('payments', 'Payments and approvals',
  'Payments waiting for you, and what has already been released or rejected. Approvals are simulated and recorded with an audit note.',
  wall('payments', 'Payments and approvals', [
    group('lead', 6, 'What is waiting for approval?', [kpi('py-pending', 'Awaiting approval'), kpi('py-value', 'Value awaiting approval'), kpi('py-released', 'Released'), kpi('py-rejected', 'Rejected')]),
    group('evidence', 3, 'Where is payment value by currency and status?', [chart_tile('py-status', 'grouped', 6)]),
    group('evidence', 3, 'Which regions pay out more than they receive?', [chart_tile('py-flows', 'butterflyh', 6)]),
    group('evidence', 6, 'The records', [records_tile(grid('pay', 'Payments', PAY_COLS))]),
  ])))

VIEWS.append(('fx', 'FX and markets',
  'Illustrative rates against sterling, hedges in place, and simulated quotes. Rates are placeholders for design only and are not market data.',
  wall('fx', 'FX and markets', [
    group('lead', 6, 'Where are rates, and how much is hedged?', [kpi('fx-usd', 'GBP/USD'), kpi('fx-eur', 'GBP/EUR'), kpi('fx-unhedged', 'Net unhedged exposure'), kpi('fx-ratio', 'Hedge ratio')]),
    group('evidence', 4, 'How did sterling trade against the dollar?', [chart_tile('fx-candle', 'candlestick', 6)]),
    group('context', 2, 'Which rates does this prototype use?', [summary_tile('fx-rates', 'Illustrative FX rates, 1 GBP buys', 6, 1)]),
    group('evidence', 3, 'How have rates moved, indexed to the start?', [chart_tile('fx-index', 'multiline', 6)]),
    group('evidence', 3, 'How widely do daily moves spread?', [chart_tile('fx-box', 'boxplot', 6)]),
    group('evidence', 6, 'The records', [records_tile(grid('deal', 'Hedges and deals', DEAL_COLS))]),
  ])))

VIEWS.append(('risk', 'Risk and limits',
  'Exposure by region, counterparty and currency, the limits that bound it, and the exceptions that need an acknowledgement.',
  wall('risk', 'Risk and limits', [
    group('lead', 6, Q2, [kpi('rk-exp', 'Total exposure'), kpi('rk-breach', 'Limits in breach'), kpi('rk-near', 'Limits above 90%'), kpi('rk-open', 'Open exceptions')]),
    group('evidence', 3, 'Which regions carry the exposure?', [chart_tile('rk-region', 'bar', 6)]),
    group('evidence', 3, 'Which counterparties are large and heavily used?', [chart_tile('rk-scatter', 'scatter', 6)]),
    group('evidence', 6, 'Which limits are closest to breach?', [chart_tile('rk-bullet', 'bullet', 6)]),
    group('evidence', 6, 'The records', [records_tile(tabs('rk-tabs', [('positions', 'Positions'), ('limits', 'Limits'), ('exceptions', 'Exceptions')],
        {'positions': grid('pos', 'Positions', POS_COLS), 'limits': grid('lim', 'Limits', LIM_COLS), 'exceptions': grid('exc', 'Exceptions', EXC_COLS)}))]),
  ])))

VIEWS.append(('trade', 'Trade finance',
  'Letters of credit, guarantees and collections issued for the group, with what expires soon.',
  wall('trade', 'Trade finance', [
    group('lead', 6, 'How much trade support is outstanding?', [kpi('tf-out', 'Outstanding instruments'), kpi('tf-lc', 'Letters of credit'), kpi('tf-exp', 'Expiring in 30 days'), kpi('tf-util', 'Trade line utilisation')]),
    group('evidence', 3, 'What is the instrument mix?', [chart_tile('tf-mix', 'pie', 6)]),
    group('evidence', 3, 'When do instruments expire?', [chart_tile('tf-expiry', 'column', 6)]),
    group('evidence', 6, 'The records', [records_tile(grid('tf', 'Trade instruments', TF_COLS))]),
  ])))

VIEWS.append(('reports', 'Reports',
  'Standard reports for the board and the treasury committee. Running a report is simulated and produces a CSV from the prototype data.',
  wall('reports', 'Reports', [
    group('lead', 6, 'Which way are the headline figures moving?', [kpi('rp-cash', 'Cash'), kpi('rp-liq', 'Available liquidity'), kpi('rp-exp', 'Total exposure'), kpi('rp-pay', 'Payments released')]),
    group('evidence', 6, 'How do receipts compare with payments, week by week?', [chart_tile('rp-weekly', 'butterflyv', 6)]),
    group('evidence', 6, 'The records', [records_tile(grid('rep', 'Report library', REP_COLS))]),
  ])))

VIEWS.append(('messages', 'HSBC messages and service requests',
  'Messages from your HSBC team and the service requests you have raised. Replies and new requests are simulated.',
  wall('messages', 'HSBC messages and service requests', [
    group('lead', 6, 'What needs a reply?', [kpi('ms-unread', 'Unread messages'), kpi('ms-open', 'Open requests'), kpi('ms-you', 'Awaiting your reply'), kpi('ms-days', 'Average resolution')]),
    group('evidence', 3, 'What are the open requests about?', [chart_tile('ms-cat', 'donut', 6)]),
    group('evidence', 3, 'Raise a service request', [records_tile('<div data-form="sr"></div>')]),
    group('evidence', 6, 'The records', [records_tile(tabs('ms-tabs', [('msg', 'Messages'), ('sr', 'Service requests')],
        {'msg': grid('msg', 'Messages', MSG_COLS), 'sr': grid('sr', 'Service requests', SR_COLS)}))]),
  ])))

VIEWS.append(('settings', 'Settings',
  'Preferences for this prototype. They are stored in this browser only.',
  wall('settings', 'Settings', [
    group('evidence', 6, 'Preferences', [records_tile('<div data-form="settings"></div>')]),
  ])))
