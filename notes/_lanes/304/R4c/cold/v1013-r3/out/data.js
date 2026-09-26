/* CEO international banking prototype — THE DATA MODEL (generate-from-canon rule 13).
   One deterministic, seeded dataset. Every KPI, chart, grid, filter option and drawer reads it.
   All entities, counterparties, amounts and rates are ILLUSTRATIVE PLACEHOLDERS — no live data. */
(function () {
  'use strict';
  function rng(seed) { return function () { seed |= 0; seed = seed + 0x6D2B79F5 | 0; var t = Math.imul(seed ^ seed >>> 15, 1 | seed); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
  var R = rng(20260925);
  function pick(a) { return a[Math.floor(R() * a.length)]; }
  function between(a, b) { return a + (b - a) * R(); }
  function round(v, d) { var p = Math.pow(10, d || 0); return Math.round(v * p) / p; }
  function pad(n) { return (n < 10 ? '0' : '') + n; }

  var AS_OF = '2026-09-25';
  var DAY = 864e5, END = Date.UTC(2026, 8, 25);
  function iso(t) { var d = new Date(t); return d.getUTCFullYear() + '-' + pad(d.getUTCMonth() + 1) + '-' + pad(d.getUTCDate()); }
  var DAYS = [];                                   /* the 30-day window, oldest first */
  for (var i = 29; i >= 0; i--) { DAYS.push(iso(END - i * DAY)); }

  /* ILLUSTRATIVE FX — GBP value of ONE unit of each currency, and the market quote (units per GBP). */
  var FX = {
    GBP: { gbp: 1, quote: 1, name: 'Pound sterling' },
    USD: { gbp: 0.7463, quote: 1.3400, name: 'US dollar' },
    EUR: { gbp: 0.8620, quote: 1.1601, name: 'Euro' },
    HKD: { gbp: 0.09567, quote: 10.4525, name: 'Hong Kong dollar' },
    SGD: { gbp: 0.5790, quote: 1.7271, name: 'Singapore dollar' },
    CNY: { gbp: 0.10482, quote: 9.5400, name: 'Chinese renminbi' },
    AED: { gbp: 0.2032, quote: 4.9212, name: 'UAE dirham' },
    INR: { gbp: 0.008937, quote: 111.90, name: 'Indian rupee' }
  };
  var CCY_GROUP = { GBP: 'GBP', EUR: 'EUR', USD: 'USD', HKD: 'Asian currencies', SGD: 'Asian currencies', CNY: 'Asian currencies', INR: 'Asian currencies', AED: 'AED' };
  var CCY_GROUPS = ['GBP', 'EUR', 'USD', 'Asian currencies', 'AED'];
  var REGIONS = ['United Kingdom', 'Europe', 'Americas', 'Asia Pacific', 'Middle East'];

  var ENTITIES = [
    { id: 'E01', name: 'Northwind Holdings plc', short: 'Holdings plc', region: 'United Kingdom', country: 'United Kingdom', ccy: 'GBP' },
    { id: 'E02', name: 'Northwind Europe GmbH', short: 'Europe GmbH', region: 'Europe', country: 'Germany', ccy: 'EUR' },
    { id: 'E03', name: 'Northwind France SAS', short: 'France SAS', region: 'Europe', country: 'France', ccy: 'EUR' },
    { id: 'E04', name: 'Northwind Americas Inc', short: 'Americas Inc', region: 'Americas', country: 'United States', ccy: 'USD' },
    { id: 'E05', name: 'Northwind Asia Ltd', short: 'Asia Ltd', region: 'Asia Pacific', country: 'Hong Kong SAR', ccy: 'HKD' },
    { id: 'E06', name: 'Northwind Singapore Pte Ltd', short: 'Singapore Pte', region: 'Asia Pacific', country: 'Singapore', ccy: 'SGD' },
    { id: 'E07', name: 'Northwind Trading (Shanghai) Co', short: 'Shanghai Co', region: 'Asia Pacific', country: 'China', ccy: 'CNY' },
    { id: 'E08', name: 'Northwind India Pvt Ltd', short: 'India Pvt', region: 'Asia Pacific', country: 'India', ccy: 'INR' },
    { id: 'E09', name: 'Northwind Gulf FZE', short: 'Gulf FZE', region: 'Middle East', country: 'United Arab Emirates', ccy: 'AED' }
  ];
  function ent(id) { for (var i = 0; i < ENTITIES.length; i++) { if (ENTITIES[i].id === id) { return ENTITIES[i]; } } return null; }

  /* ---------- ACCOUNTS — balances in account currency; GBP equivalent via FX. */
  var ACC_TYPES = ['Operating account', 'Collections account', 'Liquidity account', 'Payroll account', 'Deposit account'];
  var SIZE = { E01: 180e6, E02: 64e6, E03: 38e6, E04: 92e6, E05: 410e6, E06: 58e6, E07: 260e6, E08: 1.9e9, E09: 120e6 };
  var ACCOUNTS = [], an = 0;
  ENTITIES.forEach(function (e) {
    var n = e.id === 'E01' ? 4 : e.id === 'E04' || e.id === 'E05' ? 3 : 2;
    for (var k = 0; k < n; k++) {
      an++;
      var ccy = k === 2 && e.ccy !== 'USD' ? 'USD' : k === 3 ? 'EUR' : e.ccy;
      var bal = round(SIZE[e.id] * between(0.25, 0.8) / (ccy === e.ccy ? 1 : FX[ccy].gbp / FX[e.ccy].gbp), 2);
      ACCOUNTS.push({ id: 'A' + pad(an), entity: e.id, name: ACC_TYPES[k % ACC_TYPES.length], ccy: ccy,
        number: '•••• ' + (4000 + Math.floor(R() * 5999)), balance: bal, iban: ccy === 'EUR' ? 'DE89 •••• ' + (1000 + an) : null });
    }
  });

  /* ---------- TRANSACTIONS over the 30-day window. */
  var CPTY = ['Halden Logistics', 'Oakridge Components', 'Brightwater Utilities', 'Castell Freight', 'Marlow Packaging', 'Veldt Mining Supply', 'Seren Software', 'Kintyre Chemicals', 'Arbor Retail Group', 'Lumen Energy', 'Pacifica Shipping', 'Orion Semiconductors', 'Tay Estates', 'Galen Insurance Brokers', 'Northwind Holdings plc', 'Northwind Americas Inc', 'Northwind Europe GmbH'];
  var TX_TYPES = [
    ['Customer receipt', 1, 0.34], ['Supplier payment', -1, 0.28], ['Payroll', -1, 0.08], ['Intercompany transfer', 0, 0.1],
    ['FX settlement', 0, 0.08], ['Tax payment', -1, 0.04], ['Interest', 1, 0.04], ['Bank fees', -1, 0.04]];
  function txType() { var r = R(), c = 0; for (var i = 0; i < TX_TYPES.length; i++) { c += TX_TYPES[i][2]; if (r <= c) { return TX_TYPES[i]; } } return TX_TYPES[0]; }
  var TRANSACTIONS = [];
  for (var t = 0; t < 320; t++) {
    var a = pick(ACCOUNTS), tt = txType(), day = Math.floor(R() * 30), size = SIZE[a.entity] / FX[a.ccy].gbp * FX[ent(a.entity).ccy].gbp;
    var mag = tt[0] === 'Bank fees' ? between(200, 9000) : tt[0] === 'Interest' ? between(5e3, 90e3) : size * between(0.002, 0.045);
    var sign = tt[1] === 0 ? (R() < 0.5 ? -1 : 1) : tt[1];
    var amt = round(sign * mag, 2);
    TRANSACTIONS.push({ id: 'TX' + (100000 + t * 7 + Math.floor(R() * 7)), date: DAYS[day], account: a.id, entity: a.entity, ccy: a.ccy,
      type: tt[0], counterparty: tt[0] === 'Bank fees' || tt[0] === 'Interest' ? 'HSBC' : pick(CPTY),
      amount: amt, gbp: round(amt * FX[a.ccy].gbp, 2),
      status: day >= 28 && R() < 0.4 ? 'Pending' : 'Settled',
      ref: (tt[0] === 'Payroll' ? 'PAY-' : tt[0] === 'Customer receipt' ? 'INV-' : 'REF-') + (20000 + Math.floor(R() * 79999)) });
  }
  TRANSACTIONS.sort(function (x, y) { return x.date < y.date ? 1 : x.date > y.date ? -1 : 0; });

  /* Daily closing balances per account, backed out from today's balance and the transactions. */
  ACCOUNTS.forEach(function (acc) {
    var s = new Array(30), b = acc.balance;
    for (var d = 29; d >= 0; d--) {
      s[d] = round(b, 2);
      TRANSACTIONS.forEach(function (x) { if (x.account === acc.id && x.date === DAYS[d]) { b -= x.amount; } });
      b += acc.balance * between(-0.004, 0.004);                   /* unexplained float — sweeps, value dating */
    }
    acc.series = s;
  });

  /* ---------- FUNDING FACILITIES (committed / uncommitted), GBP-equivalent limits. */
  var FACILITIES = [
    { id: 'F01', entity: 'E01', name: 'Syndicated revolving credit facility', type: 'Revolving credit', ccy: 'GBP', limit: 750e6, drawn: 120e6, committed: true, maturity: '2029-06-30', margin: 'SONIA + 1.10%' },
    { id: 'F02', entity: 'E01', name: 'Term loan A', type: 'Term loan', ccy: 'GBP', limit: 300e6, drawn: 300e6, committed: true, maturity: '2027-03-31', margin: 'SONIA + 1.35%' },
    { id: 'F03', entity: 'E04', name: 'US dollar revolver', type: 'Revolving credit', ccy: 'USD', limit: 250e6, drawn: 60e6, committed: true, maturity: '2028-09-30', margin: 'SOFR + 1.20%' },
    { id: 'F04', entity: 'E02', name: 'Euro bilateral facility', type: 'Revolving credit', ccy: 'EUR', limit: 150e6, drawn: 45e6, committed: true, maturity: '2027-12-15', margin: 'EURIBOR + 0.95%' },
    { id: 'F05', entity: 'E05', name: 'Hong Kong trade and working capital line', type: 'Working capital', ccy: 'HKD', limit: 900e6, drawn: 310e6, committed: false, maturity: '2026-12-31', margin: 'HIBOR + 1.05%' },
    { id: 'F06', entity: 'E06', name: 'Singapore overdraft', type: 'Overdraft', ccy: 'SGD', limit: 40e6, drawn: 6e6, committed: false, maturity: '2027-03-31', margin: 'SORA + 1.40%' },
    { id: 'F07', entity: 'E07', name: 'Onshore renminbi loan', type: 'Term loan', ccy: 'CNY', limit: 500e6, drawn: 420e6, committed: true, maturity: '2026-11-28', margin: 'LPR + 0.60%' },
    { id: 'F08', entity: 'E08', name: 'Rupee working capital facility', type: 'Working capital', ccy: 'INR', limit: 4.5e9, drawn: 3.1e9, committed: true, maturity: '2027-05-31', margin: 'MCLR + 0.75%' },
    { id: 'F09', entity: 'E09', name: 'Dirham revolving facility', type: 'Revolving credit', ccy: 'AED', limit: 300e6, drawn: 90e6, committed: true, maturity: '2028-03-31', margin: 'EIBOR + 1.15%' },
    { id: 'F10', entity: 'E03', name: 'French overdraft', type: 'Overdraft', ccy: 'EUR', limit: 20e6, drawn: 0, committed: false, maturity: '2027-06-30', margin: 'EURIBOR + 1.50%' },
    { id: 'F11', entity: 'E01', name: 'Sterling commercial paper backstop', type: 'Revolving credit', ccy: 'GBP', limit: 200e6, drawn: 0, committed: true, maturity: '2030-01-31', margin: 'SONIA + 0.85%' },
    { id: 'F12', entity: 'E04', name: 'US private placement notes', type: 'Bond', ccy: 'USD', limit: 400e6, drawn: 400e6, committed: true, maturity: '2031-05-15', margin: 'Fixed 4.85%' }
  ];
  FACILITIES.forEach(function (f) {
    f.limitGbp = round(f.limit * FX[f.ccy].gbp, 0); f.drawnGbp = round(f.drawn * FX[f.ccy].gbp, 0);
    /* 30-day drawn history: two drawdown events and a repayment, deterministic. */
    var s = [], d0 = f.drawnGbp * between(0.82, 1.05);
    for (var d = 0; d < 30; d++) { s.push(round(d < 12 ? d0 : d < 21 ? (d0 + f.drawnGbp) / 2 : f.drawnGbp, 0)); }
    f.drawnSeries = s;
  });

  /* ---------- PAYMENTS AND APPROVALS. */
  var RAILS = ['CHAPS', 'SWIFT', 'SEPA credit transfer', 'Faster Payments', 'Intragroup sweep', 'Bulk supplier file'];
  var REQUESTERS = ['A. Okafor (Group Treasury)', 'M. Lindqvist (Treasury Ops)', 'S. Iyer (AP, India)', 'J. Chen (Finance, Shanghai)', 'R. Haddad (Finance, Gulf)', 'L. Moreau (Finance, France)', 'D. Park (Treasury, Americas)'];
  var PAY_STATUS = ['Awaiting your approval', 'Awaiting second approver', 'Approved', 'Released', 'Rejected', 'Scheduled'];
  var PAYMENTS = [];
  for (var p = 0; p < 72; p++) {
    var pe = ENTITIES[p % ENTITIES.length], pccy = R() < 0.7 ? pe.ccy : pick(['USD', 'EUR', 'GBP']);
    var big = R() < 0.22, pg = big ? between(5.2e6, 38e6) : between(35e3, 4.6e6);
    var st = p < 11 ? 'Awaiting your approval' : p < 18 ? 'Awaiting second approver' : pick(['Released', 'Released', 'Released', 'Approved', 'Scheduled', 'Rejected']);
    var dd = st === 'Released' || st === 'Rejected' ? DAYS[Math.floor(R() * 29)] : iso(END + Math.floor(R() * 7) * DAY);
    PAYMENTS.push({ id: 'PAY-' + (58200 + p * 13), entity: pe.id, beneficiary: pick(CPTY.slice(0, 14)), rail: pccy === 'EUR' && R() < 0.7 ? 'SEPA credit transfer' : pick(RAILS),
      ccy: pccy, amount: round(pg / FX[pccy].gbp, 2), gbp: round(pg, 2), due: dd, status: st, requestedBy: pick(REQUESTERS),
      purpose: pick(['Supplier settlement — Q3 components', 'Quarterly VAT', 'Dividend to parent', 'Capital expenditure — plant upgrade', 'Freight and logistics', 'Intercompany loan repayment', 'Payroll funding', 'Licence fees']),
      material: pg >= 5e6, audit: [{ at: dd + ' 08:' + pad(10 + p % 49), who: 'System', what: 'Payment created by ' + 'workflow' }] });
  }

  /* ---------- RISK — positions, limits, exceptions. */
  var POS_TYPES = ['Cash deposit', 'FX forward', 'Trade receivable', 'Trade payable', 'Intercompany loan', 'Money market fund'];
  var BANKS = ['Counterparty bank A', 'Counterparty bank B', 'Counterparty bank C', 'Counterparty bank D', 'HSBC'];
  var POSITIONS = [];
  for (var q = 0; q < 64; q++) {
    var qe = ENTITIES[q % ENTITIES.length], qccy = R() < 0.55 ? qe.ccy : pick(['USD', 'EUR', 'GBP', 'CNY', 'HKD']);
    var qt = pick(POS_TYPES), sgn = qt === 'Trade payable' || (qt === 'FX forward' && R() < 0.5) ? -1 : 1;
    var qg = sgn * between(2e6, 64e6);
    POSITIONS.push({ id: 'POS-' + (7100 + q), entity: qe.id, region: qe.region, ccy: qccy, group: CCY_GROUP[qccy], type: qt,
      counterparty: qt === 'Trade receivable' || qt === 'Trade payable' ? pick(CPTY.slice(0, 14)) : pick(BANKS),
      notional: round(qg / FX[qccy].gbp, 0), gbp: round(qg, 0), maturity: iso(END + Math.floor(between(5, 400)) * DAY),
      hedged: qt === 'FX forward' ? 100 : Math.round(between(0, 90)) });
  }
  var LIMITS = [
    { id: 'L01', name: 'United Kingdom — gross exposure', kind: 'Country', key: 'United Kingdom', limit: 520e6 },
    { id: 'L02', name: 'Europe — gross exposure', kind: 'Country', key: 'Europe', limit: 330e6 },
    { id: 'L03', name: 'Americas — gross exposure', kind: 'Country', key: 'Americas', limit: 300e6 },
    { id: 'L04', name: 'Asia Pacific — gross exposure', kind: 'Country', key: 'Asia Pacific', limit: 420e6 },
    { id: 'L05', name: 'Middle East — gross exposure', kind: 'Country', key: 'Middle East', limit: 140e6 },
    { id: 'L06', name: 'US dollar — net open position', kind: 'Currency', key: 'USD', limit: 120e6 },
    { id: 'L07', name: 'Euro — net open position', kind: 'Currency', key: 'EUR', limit: 90e6 },
    { id: 'L08', name: 'Asian currencies — net open position', kind: 'Currency', key: 'Asian currencies', limit: 150e6 },
    { id: 'L09', name: 'UAE dirham — net open position', kind: 'Currency', key: 'AED', limit: 45e6 },
    { id: 'L10', name: 'Counterparty bank A — deposits', kind: 'Counterparty', key: 'Counterparty bank A', limit: 150e6 },
    { id: 'L11', name: 'Counterparty bank B — deposits', kind: 'Counterparty', key: 'Counterparty bank B', limit: 150e6 },
    { id: 'L12', name: 'Counterparty bank C — deposits', kind: 'Counterparty', key: 'Counterparty bank C', limit: 120e6 },
    { id: 'L13', name: 'Counterparty bank D — deposits', kind: 'Counterparty', key: 'Counterparty bank D', limit: 100e6 }
  ];
  var EXCEPTIONS = [
    { id: 'EXC-3101', title: 'Asian currencies net open position above 90% of limit', limit: 'L08', severity: 'High', material: true, raised: DAYS[27], region: 'Asia Pacific', ccy: 'Asian currencies', owner: 'Group Treasury risk' },
    { id: 'EXC-3102', title: 'Counterparty bank A deposits exceed policy concentration', limit: 'L10', severity: 'High', material: true, raised: DAYS[26], region: 'United Kingdom', ccy: 'GBP', owner: 'Group Treasury risk' },
    { id: 'EXC-3103', title: 'Onshore renminbi loan matures in under 90 days without refinancing', limit: null, severity: 'High', material: true, raised: DAYS[24], region: 'Asia Pacific', ccy: 'Asian currencies', owner: 'Treasury, Shanghai' },
    { id: 'EXC-3104', title: 'Middle East gross exposure trending towards limit', limit: 'L05', severity: 'Medium', material: false, raised: DAYS[22], region: 'Middle East', ccy: 'AED', owner: 'Finance, Gulf' },
    { id: 'EXC-3105', title: 'Euro hedge ratio below 60% policy floor', limit: 'L07', severity: 'Medium', material: true, raised: DAYS[20], region: 'Europe', ccy: 'EUR', owner: 'Group Treasury risk' },
    { id: 'EXC-3106', title: 'Settlement limit spike on SWIFT batch, India', limit: null, severity: 'Medium', material: false, raised: DAYS[18], region: 'Asia Pacific', ccy: 'Asian currencies', owner: 'Treasury Ops' },
    { id: 'EXC-3107', title: 'US dollar net open position above 85% of limit', limit: 'L06', severity: 'Medium', material: true, raised: DAYS[16], region: 'Americas', ccy: 'USD', owner: 'Treasury, Americas' },
    { id: 'EXC-3108', title: 'Know-your-customer document expiring — Gulf FZE signatories', limit: null, severity: 'Low', material: false, raised: DAYS[12], region: 'Middle East', ccy: 'AED', owner: 'Company secretariat' },
    { id: 'EXC-3109', title: 'Trade guarantee claim window opens within 14 days', limit: null, severity: 'Low', material: false, raised: DAYS[9], region: 'Europe', ccy: 'EUR', owner: 'Trade finance desk' },
    { id: 'EXC-3110', title: 'Counterparty bank C rating outlook changed to negative', limit: 'L12', severity: 'Medium', material: true, raised: DAYS[6], region: 'Asia Pacific', ccy: 'USD', owner: 'Group Treasury risk' }
  ];
  EXCEPTIONS.forEach(function (x) { x.status = 'Open'; x.audit = [{ at: x.raised + ' 07:30', who: 'Risk engine', what: 'Exception raised' }]; });

  /* ---------- TRADE FINANCE. */
  var TF_TYPES = ['Import letter of credit', 'Export letter of credit', 'Standby letter of credit', 'Bank guarantee', 'Documentary collection'];
  var TF_STATUS = ['Issued', 'Issued', 'Amended', 'Documents presented', 'Discrepancies found', 'Settled', 'Expired'];
  var TRADE = [];
  for (var r = 0; r < 44; r++) {
    var re_ = ENTITIES[(r * 5) % ENTITIES.length], rccy = R() < 0.6 ? 'USD' : pick(['EUR', 'GBP', re_.ccy]);
    var rg = between(0.4e6, 22e6);
    TRADE.push({ id: 'TF-' + (40200 + r * 11), type: pick(TF_TYPES), entity: re_.id, counterparty: pick(CPTY.slice(0, 14)), ccy: rccy,
      amount: round(rg / FX[rccy].gbp, 0), gbp: round(rg, 0), issued: DAYS[Math.floor(R() * 30)], expiry: iso(END + Math.floor(between(-20, 330)) * DAY),
      status: pick(TF_STATUS), port: pick(['Felixstowe', 'Rotterdam', 'Shanghai', 'Jebel Ali', 'Singapore', 'Long Beach', 'Nhava Sheva', 'Hamburg']) });
  }
  var TRADE_LINES = ENTITIES.map(function (e, i) { return { entity: e.id, limitGbp: [180e6, 60e6, 30e6, 90e6, 120e6, 40e6, 110e6, 50e6, 45e6][i] }; });

  /* ---------- FX AND MARKETS — 30-day daily quotes (units per GBP), a seeded walk ending at today's quote. */
  var PAIRS = ['USD', 'EUR', 'HKD', 'SGD', 'CNY', 'AED', 'INR'];
  var FXSERIES = {};
  PAIRS.forEach(function (c, k) {
    var s = new Array(30), v = FX[c].quote, vol = c === 'AED' || c === 'HKD' ? 0.0022 : 0.0045;
    for (var d = 29; d >= 0; d--) { s[d] = round(v, 4); v = v / (1 + (R() - 0.5) * 2 * vol + (k % 2 ? 0.0003 : -0.0002)); }
    FXSERIES[c] = s;
  });
  var OHLC = [];                                   /* GBP/USD sessions: weekdays of the window */
  DAYS.forEach(function (d, i) {
    var wd = new Date(d + 'T00:00:00Z').getUTCDay(); if (wd === 0 || wd === 6) { return; }
    var c = FXSERIES.USD[i], o = i ? FXSERIES.USD[i - 1] : c * 0.998;
    OHLC.push({ d: d, o: o, c: c, h: round(Math.max(o, c) * (1 + R() * 0.0035), 4), l: round(Math.min(o, c) * (1 - R() * 0.0035), 4) });
  });
  var DEALS = [];
  for (var u = 0; u < 46; u++) {
    var uc = pick(PAIRS), kind = pick(['Spot', 'Forward', 'Forward', 'Swap', 'Non-deliverable forward']), ue = pick(ENTITIES);
    var ug = between(0.5e6, 30e6);
    DEALS.push({ id: 'FXD-' + (91000 + u * 17), entity: ue.id, pair: 'GBP/' + uc, kind: kind, side: R() < 0.5 ? 'Buy' : 'Sell',
      notional: round(ug / FX[uc].gbp, 0), gbp: round(ug, 0), rate: round(FX[uc].quote * between(0.992, 1.008), 4),
      trade: DAYS[Math.floor(R() * 30)], value: iso(END + Math.floor(between(-25, 180)) * DAY), status: pick(['Confirmed', 'Confirmed', 'Settled', 'Awaiting confirmation']) });
  }

  /* ---------- REPORTS, MESSAGES, SERVICE REQUESTS. */
  var REPORTS = [
    ['Group cash position', 'Liquidity', 'Daily'], ['Thirteen-week cash forecast', 'Liquidity', 'Weekly'], ['Facility utilisation and covenants', 'Funding', 'Monthly'],
    ['Debt maturity profile', 'Funding', 'Monthly'], ['FX exposure and hedge effectiveness', 'Markets', 'Weekly'], ['Counterparty concentration', 'Risk', 'Weekly'],
    ['Limit utilisation and exceptions', 'Risk', 'Daily'], ['Payments released', 'Payments', 'Daily'], ['Approvals audit trail', 'Payments', 'Monthly'],
    ['Trade instruments outstanding', 'Trade', 'Weekly'], ['Letters of credit expiring', 'Trade', 'Weekly'], ['Bank fees analysis', 'Accounts', 'Monthly'],
    ['Intercompany positions', 'Accounts', 'Monthly'], ['Board treasury pack', 'Board', 'Quarterly'], ['Regional liquidity heatmap', 'Liquidity', 'Weekly'],
    ['Service request summary', 'Service', 'Monthly'], ['Interest income and expense', 'Accounts', 'Monthly'], ['Sanctions screening outcomes', 'Risk', 'Monthly']
  ].map(function (x, i) { return { id: 'RPT-' + (500 + i), name: x[0], category: x[1], frequency: x[2], lastRun: DAYS[29 - (i % 9)], owner: pick(['Group Treasury', 'Finance', 'Risk', 'Company secretariat']), runs: 3 + (i * 7) % 11 }; });

  var MESSAGES = [
    ['Relationship manager', 'Refinancing options for the renminbi loan', 'Following our call, attached are three refinancing structures for the onshore loan maturing in November, with indicative pricing.'],
    ['HSBC Service Centre', 'Mandate update completed — Europe GmbH', 'The signatory mandate change for Northwind Europe GmbH has been applied. New signatories can approve from tomorrow.'],
    ['Trade finance desk', 'Discrepancy notice — TF-40365', 'Documents presented under the import letter of credit show a discrepancy in the bill of lading date. Please advise whether to waive.'],
    ['Markets desk', 'Weekly FX outlook', 'Sterling is range-bound against the US dollar ahead of central bank meetings. Our view on hedging windows for Q4 is attached.'],
    ['Relationship manager', 'Annual facility review — agenda', 'Proposed agenda for the annual review of the syndicated revolving credit facility, including covenant headroom.'],
    ['HSBC Service Centre', 'Scheduled maintenance this weekend', 'Some payment services will be unavailable between 01:00 and 04:00 UK time on Sunday. Scheduled payments are unaffected.'],
    ['Liquidity solutions', 'Notional pooling proposal for Asia Pacific', 'A proposal to extend the notional pool to Singapore and Hong Kong entities, with an estimate of interest benefit.'],
    ['Compliance', 'Know-your-customer refresh — Gulf FZE', 'Please provide updated identification documents for two signatories of Northwind Gulf FZE by 15 October.'],
    ['Trade finance desk', 'Guarantee expiry reminder', 'Bank guarantee TF-40508 expires in 21 days. Let us know whether an extension is required.'],
    ['Relationship manager', 'Invitation — trade and supply chain forum', 'You are invited to the trade and supply chain forum in London on 14 October.'],
    ['HSBC Service Centre', 'Statement format change', 'From 1 November, camt.053 statements will include structured remittance data by default.'],
    ['Markets desk', 'Forward points update — Indian rupee', 'Forward points for rupee non-deliverable forwards widened this week. Revised indicative levels attached.']
  ].map(function (x, i) { return { id: 'MSG-' + (8800 + i), from: x[0], subject: x[1], body: x[2], date: DAYS[29 - i * 2 < 0 ? 0 : 29 - i * 2], read: i > 4, thread: [] }; });
  var SR_CAT = ['Payments investigation', 'Account maintenance', 'Mandate change', 'Trade finance amendment', 'Statement request', 'Access and entitlements'];
  var SR_STATUS = ['Open', 'In progress', 'Awaiting your response', 'Closed', 'Closed', 'In progress'];
  var REQUESTS = [];
  for (var w = 0; w < 26; w++) {
    REQUESTS.push({ id: 'SR-' + (61000 + w * 29), category: pick(SR_CAT), entity: pick(ENTITIES).id, status: pick(SR_STATUS),
      opened: DAYS[Math.floor(R() * 30)], priority: pick(['Standard', 'Standard', 'High']),
      summary: pick(['Trace inbound SWIFT payment not received', 'Close dormant collections account', 'Add two authorised signatories', 'Extend letter of credit expiry by 30 days', 'Re-issue September statements in MT940', 'Grant approval rights to new treasury analyst', 'Recall duplicated supplier payment', 'Update registered address']) });
  }

  window.DATA = { asOf: AS_OF, days: DAYS, fx: FX, ccyGroup: CCY_GROUP, ccyGroups: CCY_GROUPS, regions: REGIONS, entities: ENTITIES, ent: ent,
    accounts: ACCOUNTS, transactions: TRANSACTIONS, facilities: FACILITIES, payments: PAYMENTS, positions: POSITIONS, limits: LIMITS,
    exceptions: EXCEPTIONS, trade: TRADE, tradeLines: TRADE_LINES, pairs: PAIRS, fxSeries: FXSERIES, ohlc: OHLC, deals: DEALS,
    reports: REPORTS, messages: MESSAGES, requests: REQUESTS, rails: RAILS };
}());
