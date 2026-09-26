/* ================= DATA — the one dataset every KPI, chart, grid, filter and drawer reads (rule 13).
   Placeholder entities and figures, generated deterministically (seeded) so every reload is identical.
   Reporting currency GBP. FX rates are ILLUSTRATIVE, stated on the page, never live. ================= */
const DATA = (function () {
  var seed = 20260925;
  function rnd() { seed = (seed * 1664525 + 1013904223) % 4294967296; return seed / 4294967296; }
  function pick(a) { return a[Math.floor(rnd() * a.length)]; }
  function between(lo, hi) { return lo + (hi - lo) * rnd(); }
  function r2(v) { return Math.round(v * 100) / 100; }

  var ASAT = '2026-09-25';
  var DAYS = [];
  (function () { var d = new Date(Date.UTC(2026, 7, 27)); for (var i = 0; i < 30; i++) { DAYS.push(d.toISOString().slice(0, 10)); d.setUTCDate(d.getUTCDate() + 1); } }());

  /* GBP per one unit of the currency — illustrative, as at the close of 25 September 2026 */
  var FX = { GBP: 1, USD: 0.7462, EUR: 0.8431, HKD: 0.0958, SGD: 0.5791, CNY: 0.1047, AED: 0.2032 };

  var REGIONS = [
    { id: 'uk', name: 'United Kingdom' }, { id: 'eu', name: 'Europe' }, { id: 'am', name: 'Americas' },
    { id: 'ap', name: 'Asia-Pacific' }, { id: 'me', name: 'Middle East and Africa' }];

  var ENTITIES = [
    { id: 'E01', name: 'Northwind Group plc', short: 'Group plc', region: 'uk', ccy: 'GBP', country: 'United Kingdom' },
    { id: 'E02', name: 'Northwind Europe BV', short: 'Europe BV', region: 'eu', ccy: 'EUR', country: 'Netherlands' },
    { id: 'E03', name: 'Northwind Deutschland GmbH', short: 'Deutschland GmbH', region: 'eu', ccy: 'EUR', country: 'Germany' },
    { id: 'E04', name: 'Northwind Americas Inc', short: 'Americas Inc', region: 'am', ccy: 'USD', country: 'United States' },
    { id: 'E05', name: 'Northwind Asia Ltd', short: 'Asia Ltd', region: 'ap', ccy: 'HKD', country: 'Hong Kong SAR' },
    { id: 'E06', name: 'Northwind Singapore Pte', short: 'Singapore Pte', region: 'ap', ccy: 'SGD', country: 'Singapore' },
    { id: 'E07', name: 'Northwind Trading (Shanghai)', short: 'Shanghai', region: 'ap', ccy: 'CNY', country: 'China' },
    { id: 'E08', name: 'Northwind Gulf FZE', short: 'Gulf FZE', region: 'me', ccy: 'AED', country: 'United Arab Emirates' }];

  var ACCOUNTS = [], kinds = ['Operating', 'Collections', 'Payroll'];
  ENTITIES.forEach(function (e, ei) {
    kinds.forEach(function (k, ki) {
      var base = [42, 18, 9][ki] * (ei === 0 ? 2.2 : ei === 3 ? 1.6 : 0.6 + rnd());
      var ccy = (ki === 1 && e.region === 'ap') ? 'USD' : e.ccy;
      ACCOUNTS.push({ id: 'A' + (ei + 1) + (ki + 1), entity: e.id, name: e.short + ' ' + k.toLowerCase(), kind: k, ccy: ccy,
        iban: '•••• ' + String(1000 + Math.floor(rnd() * 8999)), gbp0: base * 1e6 });
    });
  });
  ACCOUNTS.forEach(function (a) {
    var v = a.gbp0, path = [];
    for (var i = 0; i < 30; i++) { v = Math.max(a.gbp0 * 0.55, v * (1 + between(-0.035, 0.04))); path.push(Math.round(v)); }
    a.series = path; a.gbp = path[29]; a.local = r2(a.gbp / FX[a.ccy]);
  });

  var FACILITIES = [
    { id: 'F1', name: 'Revolving credit facility', entity: 'E01', ccy: 'GBP', limit: 400e6, drawn: 120e6, maturity: '2029-06-30', kind: 'Committed' },
    { id: 'F2', name: 'Term loan A', entity: 'E01', ccy: 'GBP', limit: 250e6, drawn: 250e6, maturity: '2028-03-31', kind: 'Committed' },
    { id: 'F3', name: 'US commercial paper backstop', entity: 'E04', ccy: 'USD', limit: 300e6, drawn: 85e6, maturity: '2027-11-15', kind: 'Committed' },
    { id: 'F4', name: 'Euro working capital line', entity: 'E02', ccy: 'EUR', limit: 150e6, drawn: 64e6, maturity: '2027-05-31', kind: 'Committed' },
    { id: 'F5', name: 'Asia trade line', entity: 'E05', ccy: 'USD', limit: 120e6, drawn: 71e6, maturity: '2027-02-28', kind: 'Uncommitted' },
    { id: 'F6', name: 'Gulf overdraft', entity: 'E08', ccy: 'AED', limit: 180e6, drawn: 22e6, maturity: '2026-12-31', kind: 'Uncommitted' }];
  FACILITIES.forEach(function (f) { f.limitGbp = f.limit * FX[f.ccy]; f.drawnGbp = f.drawn * FX[f.ccy]; f.requests = []; });

  var PAYEES = ['Kestrel Logistics', 'Aurora Components', 'Meridian Freight', 'Halden Steel', 'Cobalt Packaging', 'Vireo Energy',
    'Tamsin Foods', 'Orchard Chemicals', 'Pellham Ports', 'Saffron Textiles', 'Lumen Semiconductors', 'Brightwater Utilities',
    'Harbourline Shipping', 'Quarry Point Minerals', 'Nimbus Cloud Services', 'Redfern Insurance', 'Sable Consulting', 'Tidewater Leasing'];
  var BANKS = ['Harbour Bank', 'Continental Credit', 'Pacific Commerce Bank', 'Gulf Trust', 'Alpine Savings', 'Crescent Bank'];

  var TXNS = [], types = ['Receipt', 'Supplier payment', 'Payroll', 'FX settlement', 'Intercompany sweep', 'Bank fee', 'Interest'];
  DAYS.forEach(function (day, di) {
    for (var i = 0; i < 10; i++) {
      var acc = pick(ACCOUNTS), t = pick(types), sign = (t === 'Receipt' || t === 'Interest') ? 1 : (t === 'Intercompany sweep' ? (rnd() < 0.5 ? 1 : -1) : -1);
      var mag = t === 'Bank fee' ? between(40, 900) : t === 'Interest' ? between(2e3, 4e4) : t === 'Payroll' ? between(4e5, 3.2e6) : between(2e4, 2.4e6);
      var local = r2(sign * mag / FX[acc.ccy]);
      TXNS.push({ id: 'T' + (1001 + di * 10 + i), date: day, entity: acc.entity, account: acc.id,
        counterparty: t === 'Bank fee' || t === 'Interest' ? 'HSBC' : t === 'Intercompany sweep' ? pick(ENTITIES).short : pick(PAYEES),
        type: t, ccy: acc.ccy, amount: local, gbp: r2(local * FX[acc.ccy]), status: di > 27 && rnd() < 0.4 ? 'Pending' : 'Settled',
        ref: (t === 'Receipt' ? 'INV-' : t === 'Payroll' ? 'PAY-' : 'REF-') + (240000 + Math.floor(rnd() * 90000)) });
    }
  });

  var PAYMENTS = [], initiators = ['A. Mensah', 'L. Okafor', 'P. Whitlock', 'S. Iyer', 'M. Duarte'];
  for (var p = 0; p < 44; p++) {
    var e = pick(ENTITIES), ccy = rnd() < 0.3 ? 'USD' : e.ccy, gbp = r2(between(0.08, 9.5) * 1e6 * (rnd() < 0.15 ? 3 : 1));
    var st = p < 26 ? 'Awaiting approval' : pick(['Approved', 'Released', 'Rejected', 'Released']);
    PAYMENTS.push({ id: 'PMT-' + (58100 + p * 7), entity: e.id, beneficiary: pick(PAYEES), ccy: ccy, amount: r2(gbp / FX[ccy]), gbp: gbp,
      rail: ccy === 'EUR' ? 'SEPA credit' : ccy === 'USD' ? pick(['Fedwire', 'SWIFT']) : ccy === 'GBP' ? 'CHAPS' : pick(['SWIFT', 'RTGS']),
      valueDate: ['2026-09-28', '2026-09-29', '2026-09-30', '2026-10-01', '2026-10-02'][Math.floor(rnd() * 5)], created: DAYS[20 + Math.floor(rnd() * 10)],
      initiator: pick(initiators), status: st, approvals: st === 'Awaiting approval' ? (rnd() < 0.5 ? 1 : 0) : 2, required: 2,
      flag: gbp > 5e6 ? 'Above dual-control threshold' : (rnd() < 0.18 ? 'New beneficiary' : 'None'), audit: [] });
  }

  var PAIRS = ['GBP/USD', 'GBP/EUR', 'GBP/HKD', 'GBP/SGD', 'GBP/CNY', 'GBP/AED'];
  var RATE = {}; PAIRS.forEach(function (pr) { RATE[pr] = Math.round(1 / FX[pr.slice(4)] * 10000) / 10000; });
  function ohlc(last, vol) {
    var out = { open: [], high: [], low: [], close: [] }, c = last, closes = [];
    for (var i = 0; i < 30; i++) { c = c * (1 + between(-vol, vol)); closes.push(c); }
    var k = last / closes[29];
    closes = closes.map(function (v) { return v * k; });
    for (var j = 0; j < 30; j++) { var o = j ? closes[j - 1] : closes[0] * (1 - between(-vol, vol)); var cl = closes[j];
      out.open.push(+o.toFixed(4)); out.close.push(+cl.toFixed(4));
      out.high.push(+(Math.max(o, cl) * (1 + between(0.0005, vol))).toFixed(4)); out.low.push(+(Math.min(o, cl) * (1 - between(0.0005, vol))).toFixed(4)); }
    return out;
  }
  var CANDLES = {}; PAIRS.forEach(function (pr) { CANDLES[pr] = ohlc(RATE[pr], 0.004); });
  var DEALS = [];
  for (var d = 0; d < 34; d++) {
    var pr = pick(PAIRS), side = rnd() < 0.5 ? 'Buy' : 'Sell', notionalGbp = r2(between(0.5, 18) * 1e6), e2 = pick(ENTITIES);
    var dealRate = +(RATE[pr] * (1 + between(-0.012, 0.012))).toFixed(4);
    DEALS.push({ id: 'FXD-' + (7300 + d * 3), entity: e2.id, pair: pr, side: side, kind: rnd() < 0.6 ? 'Forward' : 'Spot', notional: notionalGbp,
      rate: dealRate, maturity: ['2026-10-15', '2026-11-27', '2026-12-18', '2027-01-29', '2027-03-31'][Math.floor(rnd() * 5)],
      mtm: r2(notionalGbp * (dealRate - RATE[pr]) / RATE[pr] * (side === 'Buy' ? -1 : 1)) });
  }

  var POSITIONS = [], ccys = ['GBP', 'USD', 'EUR', 'HKD', 'SGD', 'CNY', 'AED'];
  for (var q = 0; q < 60; q++) {
    var e3 = pick(ENTITIES), c3 = rnd() < 0.55 ? e3.ccy : pick(ccys), bank = pick(BANKS), lim = pick([50, 75, 100, 150, 200]) * 1e6;
    var div = (q % 4 === 0 ? 1 : 3), expo = r2(lim * between(0.22, 1.08) / div);
    POSITIONS.push({ id: 'POS-' + (400 + q), entity: e3.id, region: e3.region, ccy: c3, counterparty: bank,
      kind: pick(['Deposit', 'Nostro balance', 'FX forward', 'Money market', 'Trade exposure']), exposure: expo, limit: r2(lim / div) });
  }
  POSITIONS.forEach(function (x) { x.util = Math.round(x.exposure / x.limit * 1000) / 10; });
  var LIMITS = [
    { id: 'L1', name: 'Counterparty limit — Harbour Bank', kind: 'Counterparty', region: 'uk', limit: 300e6 },
    { id: 'L2', name: 'Country limit — China', kind: 'Country', region: 'ap', limit: 120e6 },
    { id: 'L3', name: 'Net open position — USD', kind: 'Currency', region: 'am', limit: 90e6 },
    { id: 'L4', name: 'Counterparty limit — Gulf Trust', kind: 'Counterparty', region: 'me', limit: 80e6 },
    { id: 'L5', name: 'Net open position — EUR', kind: 'Currency', region: 'eu', limit: 70e6 },
    { id: 'L6', name: 'Country limit — Hong Kong SAR', kind: 'Country', region: 'ap', limit: 150e6 }];
  LIMITS.forEach(function (l, i) { l.used = r2(l.limit * [0.64, 1.07, 0.93, 0.71, 1.02, 0.58][i]); });
  var EXCEPTIONS = [];
  var exText = ['Counterparty limit exceeded', 'Country limit exceeded', 'Net open position above limit', 'Concentration above 25% of cash', 'Unhedged exposure above policy', 'Covenant headroom below 15%'];
  for (var x2 = 0; x2 < 14; x2++) {
    var pos = POSITIONS[x2 * 4 % POSITIONS.length], sev = x2 < 5 ? 'High' : x2 < 10 ? 'Medium' : 'Low';
    EXCEPTIONS.push({ id: 'EXC-' + (2100 + x2), title: exText[x2 % exText.length], entity: pos.entity, region: pos.region, ccy: pos.ccy,
      position: pos.id, severity: sev, amount: r2(pos.exposure * between(0.04, 0.2)), raised: DAYS[15 + (x2 * 3) % 15],
      status: x2 % 5 === 4 ? 'Acknowledged' : 'Open',
      audit: x2 % 5 === 4 ? [{ at: '2026-09-22 10:14', by: 'Group CEO', note: 'Reviewed with the group treasurer; temporary excess agreed until month end.' }] : [] });
  }

  var TRADE = [], tkinds = ['Import letter of credit', 'Export letter of credit', 'Standby letter of credit', 'Bank guarantee', 'Documentary collection'];
  for (var t2 = 0; t2 < 38; t2++) {
    var e4 = pick(ENTITIES), c4 = rnd() < 0.5 ? 'USD' : e4.ccy, gbp4 = r2(between(0.15, 12) * 1e6), days = Math.floor(between(3, 175));
    var exp = new Date(Date.UTC(2026, 8, 25 + days)).toISOString().slice(0, 10);
    TRADE.push({ id: 'TF-' + (91000 + t2 * 11), entity: e4.id, kind: tkinds[t2 % tkinds.length], counterparty: pick(PAYEES), ccy: c4,
      amount: r2(gbp4 / FX[c4]), gbp: gbp4, expiry: exp, daysToExpiry: days,
      status: pick(['Issued', 'Issued', 'Awaiting documents', 'Documents discrepant', 'Amendment requested', 'Paid']) });
  }

  var REPORTS = [
    { id: 'R1', name: 'Group cash position', area: 'Liquidity', freq: 'Daily', source: 'accounts' },
    { id: 'R2', name: 'Thirty-day transaction ledger', area: 'Accounts', freq: 'Daily', source: 'txns' },
    { id: 'R3', name: 'Facility utilisation', area: 'Funding', freq: 'Weekly', source: 'facilities' },
    { id: 'R4', name: 'Payments awaiting approval', area: 'Payments', freq: 'Intraday', source: 'payments' },
    { id: 'R5', name: 'FX deal blotter', area: 'Markets', freq: 'Daily', source: 'deals' },
    { id: 'R6', name: 'Counterparty and country exposure', area: 'Risk', freq: 'Daily', source: 'positions' },
    { id: 'R7', name: 'Limit exceptions and acknowledgements', area: 'Risk', freq: 'Daily', source: 'exceptions' },
    { id: 'R8', name: 'Trade instruments by expiry', area: 'Trade', freq: 'Weekly', source: 'trade' }];
  REPORTS.forEach(function (r, i) { r.lastRun = DAYS[29 - (i % 3)] + ' 07:' + (10 + i * 4); r.format = 'CSV'; });

  var MESSAGES = [
    { id: 'M1', from: 'Relationship director', subject: 'Q4 funding review — proposed agenda', date: '2026-09-25', unread: true, body: 'Ahead of the Q4 funding review we propose covering the revolving facility extension, the Asia trade line renewal and your USD commercial paper backstop. Please confirm attendees.' },
    { id: 'M2', from: 'Liquidity and cash management', subject: 'Notional pooling go-live for Europe BV', date: '2026-09-24', unread: true, body: 'The notional pool for Northwind Europe BV and Deutschland GmbH is scheduled to go live on 1 October. No action is needed unless you want to change the header account.' },
    { id: 'M3', from: 'Trade and receivables finance', subject: 'Discrepancy notice on TF-91055', date: '2026-09-23', unread: true, body: 'Documents presented under the import letter of credit show a discrepancy in the bill of lading date. Please advise whether to accept or refuse.' },
    { id: 'M4', from: 'Markets desk', subject: 'Weekly FX outlook', date: '2026-09-22', unread: false, body: 'Sterling traded in a narrow range against the dollar this week. Rates shown in this prototype are illustrative only.' },
    { id: 'M5', from: 'Client service', subject: 'Your request SR-3304 is complete', date: '2026-09-19', unread: false, body: 'The additional user for Northwind Singapore Pte has been set up with approver rights.' },
    { id: 'M6', from: 'Relationship director', subject: 'Covenant certificate due 30 September', date: '2026-09-18', unread: false, body: 'A reminder that the half-year covenant compliance certificate for the term loan is due at month end.' },
    { id: 'M7', from: 'Global payments', subject: 'Planned maintenance, Sunday 04:00–06:00 UK time', date: '2026-09-16', unread: false, body: 'Payment release will pause during the window. Approvals can still be recorded.' }];
  var REQUESTS = [
    { id: 'SR-3311', category: 'Account services', subject: 'Open a USD collections account for Gulf FZE', entity: 'E08', priority: 'Normal', status: 'In progress', opened: '2026-09-21',
      history: [{ at: '2026-09-21 09:12', what: 'Request submitted', state: 'inf' }, { at: '2026-09-22 14:40', what: 'Documents received by HSBC', state: 'ok' }, { at: '2026-09-24 11:05', what: 'Account opening in progress', state: 'warn' }] },
    { id: 'SR-3309', category: 'Payments', subject: 'Raise the CHAPS daily limit to £75m', entity: 'E01', priority: 'High', status: 'Awaiting your input', opened: '2026-09-19',
      history: [{ at: '2026-09-19 16:02', what: 'Request submitted', state: 'inf' }, { at: '2026-09-23 10:31', what: 'HSBC needs a board resolution', state: 'warn' }] },
    { id: 'SR-3304', category: 'User access', subject: 'Add an approver for Singapore Pte', entity: 'E06', priority: 'Normal', status: 'Completed', opened: '2026-09-15',
      history: [{ at: '2026-09-15 08:47', what: 'Request submitted', state: 'inf' }, { at: '2026-09-19 12:00', what: 'User set up with approver rights', state: 'ok' }] },
    { id: 'SR-3298', category: 'Trade', subject: 'Amend expiry of standby letter of credit TF-91022', entity: 'E04', priority: 'Normal', status: 'In progress', opened: '2026-09-12',
      history: [{ at: '2026-09-12 13:20', what: 'Request submitted', state: 'inf' }, { at: '2026-09-17 09:45', what: 'Beneficiary consent requested', state: 'warn' }] },
    { id: 'SR-3290', category: 'Liquidity', subject: 'Add Shanghai to the Asia cash sweep', entity: 'E07', priority: 'Low', status: 'Completed', opened: '2026-09-03',
      history: [{ at: '2026-09-03 10:00', what: 'Request submitted', state: 'inf' }, { at: '2026-09-10 15:30', what: 'Sweep live', state: 'ok' }] }];

  var SIGNINS = DAYS.map(function (dd) { var wd = new Date(dd + 'T00:00:00Z').getUTCDay(); return (wd === 0 || wd === 6) ? Math.floor(between(0, 2)) : Math.floor(between(2, 7)); });

  return { ASAT: ASAT, DAYS: DAYS, FX: FX, REGIONS: REGIONS, ENTITIES: ENTITIES, ACCOUNTS: ACCOUNTS, FACILITIES: FACILITIES,
    TXNS: TXNS, PAYMENTS: PAYMENTS, PAIRS: PAIRS, RATE: RATE, CANDLES: CANDLES, DEALS: DEALS, POSITIONS: POSITIONS,
    LIMITS: LIMITS, EXCEPTIONS: EXCEPTIONS, TRADE: TRADE, REPORTS: REPORTS, MESSAGES: MESSAGES, REQUESTS: REQUESTS, SIGNINS: SIGNINS };
}());
