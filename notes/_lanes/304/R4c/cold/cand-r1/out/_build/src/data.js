/* CEO_DATA — THE ONE IN-PAGE DATASET (ADS-generate-from-canon rule 13). Every KPI, chart, record
   list, filter option and drawer reads from it; nothing is typed twice into the HTML.
   ⚠ It is named CEO_DATA, not DATA, because the Data-grid's own carried script owns the global
   `const DATA` binding, and a second top-level `const DATA` is a redeclaration SyntaxError.
   ILLUSTRATIVE ONLY: placeholder entities, counterparties, amounts and FX rates. Seeded, so every
   load produces the same figures. Reporting currency GBP; every GBP figure is derived from the
   local amount × the explicit illustrative rate in CEO_DATA.fx. */
(function () {
  'use strict';
  var seed = 20260926;
  function rnd() { seed |= 0; seed = seed + 0x6D2B79F5 | 0; var t = Math.imul(seed ^ seed >>> 15, 1 | seed);
    t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }
  function pick(a) { return a[Math.floor(rnd() * a.length)]; }
  function between(a, b) { return a + rnd() * (b - a); }
  function r2(n) { return Math.round(n * 100) / 100; }
  var AS_AT = new Date(Date.UTC(2026, 8, 26));
  function iso(d) { return d.toISOString().slice(0, 10); }
  function daysAgo(n) { var d = new Date(AS_AT.getTime()); d.setUTCDate(d.getUTCDate() - n); return iso(d); }
  function daysAhead(n) { return daysAgo(-n); }

  var regions = [
    { id: 'EMEA', name: 'Europe' }, { id: 'AMER', name: 'Americas' },
    { id: 'APAC', name: 'Asia Pacific' }, { id: 'MENA', name: 'Middle East' }];
  var entities = [
    { id: 'ALD-UK', name: 'Aldergrove Holdings plc', short: 'Holdings (UK)', country: 'United Kingdom', region: 'EMEA', ccy: 'GBP' },
    { id: 'ALD-DE', name: 'Aldergrove Europe GmbH', short: 'Europe (DE)', country: 'Germany', region: 'EMEA', ccy: 'EUR' },
    { id: 'ALD-US', name: 'Aldergrove Americas Inc', short: 'Americas (US)', country: 'United States', region: 'AMER', ccy: 'USD' },
    { id: 'ALD-SG', name: 'Aldergrove Asia Pacific Pte Ltd', short: 'Asia Pacific (SG)', country: 'Singapore', region: 'APAC', ccy: 'SGD' },
    { id: 'ALD-HK', name: 'Aldergrove Hong Kong Ltd', short: 'Hong Kong (HK)', country: 'Hong Kong SAR', region: 'APAC', ccy: 'HKD' },
    { id: 'ALD-AE', name: 'Aldergrove Gulf FZE', short: 'Gulf (AE)', country: 'United Arab Emirates', region: 'MENA', ccy: 'AED' }];
  /* Illustrative FX — GBP per one unit of currency, as at 26 Sep 2026 10:00 London. NOT market data. */
  var fx = { GBP: 1, USD: 0.7862, EUR: 0.8431, SGD: 0.5874, HKD: 0.1009, AED: 0.2141, CNY: 0.1103, JPY: 0.00531 };
  var currencies = ['GBP', 'USD', 'EUR', 'SGD', 'HKD', 'AED', 'CNY', 'JPY'];
  function gbp(ccy, amt) { return r2(amt * fx[ccy]); }
  function ent(id) { for (var i = 0; i < entities.length; i++) { if (entities[i].id === id) { return entities[i]; } } return null; }

  /* ---- accounts ---- */
  var accTypes = ['Operating account', 'Collections account', 'Payroll account', 'Liquidity deposit'];
  var accounts = [], ai = 0;
  entities.forEach(function (e, ei) {
    var scale = [140e6, 60e6, 110e6, 55e6, 70e6, 40e6][ei] / fx[e.ccy];
    accTypes.forEach(function (t, ti) {
      if (t === 'Liquidity deposit' && ei > 2) { return; }
      ai++;
      var bal = r2(scale * [0.46, 0.27, 0.09, 0.62][ti] * between(0.8, 1.2));
      accounts.push({ id: 'ACC-' + (1000 + ai), entity: e.id, region: e.region, ccy: e.ccy, type: t,
        name: e.short + ' · ' + t, number: '•••• ' + (4100 + ai * 37 % 900),
        balance: bal, gbp: gbp(e.ccy, bal), bank: 'HSBC ' + e.country, status: 'Active' });
    });
    if (ei === 0 || ei === 2) {
      ai++; var b2 = r2(scale * 0.08);
      var c2 = ei === 0 ? 'USD' : 'EUR';
      accounts.push({ id: 'ACC-' + (1000 + ai), entity: e.id, region: e.region, ccy: c2, type: 'Foreign currency account',
        name: e.short + ' · ' + c2 + ' account', number: '•••• ' + (4100 + ai * 37 % 900),
        balance: r2(b2 * fx[e.ccy] / fx[c2]), gbp: gbp(e.ccy, b2), bank: 'HSBC ' + e.country, status: 'Active' });
    }
  });

  /* ---- 90 days of daily cash per entity (GBP equivalent), inflows and outflows ---- */
  var DAYS = 90, dates = [];
  for (var d = DAYS - 1; d >= 0; d--) { dates.push(daysAgo(d)); }
  var daily = {};
  entities.forEach(function (e) {
    var base = accounts.filter(function (a) { return a.entity === e.id; }).reduce(function (s, a) { return s + a.gbp; }, 0);
    var cash = [], inn = [], out = [], v = base * between(0.86, 0.94);
    for (var i = 0; i < DAYS; i++) {
      var wk = new Date(dates[i] + 'T00:00:00Z').getUTCDay();
      var weekend = wk === 0 || wk === 6;
      var infl = weekend ? 0 : base * between(0.012, 0.03);
      var outf = weekend ? 0 : base * between(0.011, 0.029);
      if (i % 30 === 24) { outf += base * 0.06; }          /* month-end payroll and tax */
      v = v + infl - outf; if (i === DAYS - 1) { v = base; }
      cash.push(Math.round(v)); inn.push(Math.round(infl)); out.push(Math.round(outf));
    }
    daily[e.id] = { cash: cash, inflow: inn, outflow: out };
  });

  /* ---- committed facilities ---- */
  var facilities = [
    { id: 'FAC-01', entity: 'ALD-UK', type: 'Revolving credit facility', ccy: 'GBP', limit: 750e6, drawn: 180e6, maturity: '2029-06-30', committed: true },
    { id: 'FAC-02', entity: 'ALD-US', type: 'Term loan', ccy: 'USD', limit: 400e6, drawn: 400e6, maturity: '2027-03-31', committed: true },
    { id: 'FAC-03', entity: 'ALD-DE', type: 'Overdraft', ccy: 'EUR', limit: 50e6, drawn: 12e6, maturity: '2027-09-30', committed: false },
    { id: 'FAC-04', entity: 'ALD-SG', type: 'Trade line', ccy: 'SGD', limit: 120e6, drawn: 38e6, maturity: '2027-01-31', committed: true },
    { id: 'FAC-05', entity: 'ALD-HK', type: 'Overdraft', ccy: 'HKD', limit: 200e6, drawn: 0, maturity: '2027-06-30', committed: false },
    { id: 'FAC-06', entity: 'ALD-AE', type: 'Working capital facility', ccy: 'AED', limit: 150e6, drawn: 42e6, maturity: '2026-12-15', committed: true },
    { id: 'FAC-07', entity: 'ALD-UK', type: 'Commercial paper programme', ccy: 'GBP', limit: 300e6, drawn: 95e6, maturity: '2026-11-20', committed: false }];
  facilities.forEach(function (f) { var e = ent(f.entity); f.region = e.region; f.limitGbp = gbp(f.ccy, f.limit); f.drawnGbp = gbp(f.ccy, f.drawn);
    f.undrawnGbp = r2(f.limitGbp - f.drawnGbp); f.name = f.type + ' · ' + e.short; });
  var policy = { minimumLiquidityGbp: 400e6, approvalThresholdGbp: 5e6 };
  var maturities = [ { bucket: '0–3 months', gbp: 128e6 }, { bucket: '3–6 months', gbp: 214e6 }, { bucket: '6–12 months', gbp: 96e6 },
    { bucket: '1–2 years', gbp: 355e6 }, { bucket: '2–5 years', gbp: 520e6 }, { bucket: 'Over 5 years', gbp: 180e6 } ];

  /* ---- counterparties (placeholders — no real institution) ---- */
  var cps = ['Kestrel Bank AG', 'Banco Meridiano', 'Harbourline Trading', 'Solace Components', 'Northgate Logistics', 'Pemberton Steel',
    'Lumen Packaging', 'Cobalt Freight', 'Orrery Pharmaceuticals', 'Tamarind Foods', 'Sable Energy', 'Vireo Systems', 'Quayside Retail',
    'Atlas Tooling', 'Bluewater Shipping', 'Mistral Chemicals', 'Juniper Textiles', 'Crescent Minerals'];
  var ratings = ['AA', 'AA-', 'A+', 'A', 'A-', 'BBB+', 'BBB', 'BBB-', 'BB+'];

  /* ---- positions (risk) ---- */
  var instruments = ['Cash and deposits', 'Trade receivables', 'Trade payables', 'FX forwards', 'Intercompany loans', 'Trade finance'];
  var positions = [];
  var expCcyByRegion = { EMEA: ['GBP', 'EUR', 'USD'], AMER: ['USD', 'EUR'], APAC: ['SGD', 'HKD', 'CNY', 'JPY', 'USD'], MENA: ['AED', 'USD'] };
  for (var p = 1; p <= 72; p++) {
    var e = entities[(p * 5) % entities.length], c = pick(expCcyByRegion[e.region]);
    var amt = r2(between(4e6, 68e6) / fx[c]);
    var cp = pick(cps);
    positions.push({ id: 'POS-' + (3000 + p), entity: e.id, region: e.region, ccy: c, instrument: pick(instruments),
      counterparty: cp, rating: ratings[cps.indexOf(cp) % ratings.length], amount: amt, gbp: gbp(c, amt),
      maturity: daysAhead(Math.floor(between(5, 420))), limitId: null });
  }
  /* ---- limits ---- */
  var limits = [];
  regions.forEach(function (r, i) {
    var used = positions.filter(function (x) { return x.region === r.id; }).reduce(function (s, x) { return s + x.gbp; }, 0);
    var cap = Math.round(Math.max(used, 5e7) / [0.63, 0.54, 0.88, 1.06][i] / 1e6) * 1e6;
    limits.push({ id: 'LIM-R' + (i + 1), kind: 'Country and region', name: r.name + ' aggregate exposure', region: r.id, ccy: 'GBP', limitGbp: cap, usedGbp: r2(used) });
  });
  ['USD', 'EUR', 'SGD', 'HKD', 'AED', 'CNY', 'JPY'].forEach(function (c, i) {
    var used = positions.filter(function (x) { return x.ccy === c; }).reduce(function (s, x) { return s + x.gbp; }, 0);
    var cap = Math.round(Math.max(used * 0.55, 5e6) / [0.42, 0.71, 0.58, 0.64, 0.91, 0.77, 0.49][i] / 1e6) * 1e6;
    limits.push({ id: 'LIM-C' + (i + 1), kind: 'Currency net open position', name: c + ' net open position', ccy: c, region: null, limitGbp: cap, usedGbp: r2(used * 0.55) });
  });
  cps.slice(0, 8).forEach(function (cp, i) {
    var used = positions.filter(function (x) { return x.counterparty === cp; }).reduce(function (s, x) { return s + x.gbp; }, 0);
    var cap = Math.round(Math.max(used, 2e7) / [0.81, 0.66, 1.04, 0.72, 0.35, 0.87, 0.58, 0.69][i] / 1e6) * 1e6;
    limits.push({ id: 'LIM-P' + (i + 1), kind: 'Counterparty', name: cp, ccy: 'GBP', region: null, limitGbp: cap, usedGbp: r2(used) });
  });
  limits.forEach(function (l) { l.pct = Math.round(l.usedGbp / l.limitGbp * 1000) / 10;
    l.status = l.pct > 100 ? 'Breach' : l.pct >= 85 ? 'Approaching' : 'Within'; });
  positions.forEach(function (x) {
    var l = limits.filter(function (m) { return m.kind === 'Counterparty' && m.name === x.counterparty; })[0] ||
            limits.filter(function (m) { return m.region === x.region; })[0];
    x.limitId = l ? l.id : null; });

  /* ---- risk exceptions ---- */
  var exceptions = [];
  limits.filter(function (l) { return l.status !== 'Within'; }).forEach(function (l, i) {
    exceptions.push({ id: 'EXC-' + (501 + i), title: l.name + ' ' + (l.status === 'Breach' ? 'above limit' : 'within 15% of limit'),
      severity: l.status === 'Breach' ? 'Material' : 'Moderate', limitId: l.id, region: l.region, ccy: l.ccy,
      entity: l.region ? (entities.filter(function (e) { return e.region === l.region; })[0] || {}).id : 'ALD-UK',
      detected: daysAgo(1 + i * 2), owner: pick(['Group Treasurer', 'Head of Risk', 'Regional CFO, APAC', 'Regional CFO, Americas']),
      status: 'Open', gbp: r2(l.usedGbp - l.limitGbp * 0.85), audit: [] });
  });
  [['Sanctions screening hit held for review', 'Material', 'ALD-AE', 'AED'], ['Unreconciled intercompany balance over 5 days', 'Moderate', 'ALD-DE', 'EUR'],
   ['Hedge ratio below policy for CNY exposures', 'Material', 'ALD-HK', 'CNY'], ['Signatory mandate expires within 30 days', 'Moderate', 'ALD-US', 'USD']].forEach(function (x, i) {
    var e = ent(x[2]);
    exceptions.push({ id: 'EXC-' + (540 + i), title: x[0], severity: x[1], limitId: null, region: e.region, ccy: x[3], entity: e.id,
      detected: daysAgo(2 + i * 3), owner: pick(['Group Treasurer', 'Head of Compliance', 'Regional CFO, Europe']), status: 'Open', gbp: r2(between(2e6, 30e6)), audit: [] });
  });

  /* ---- payments ---- */
  var payTypes = ['Supplier', 'Intercompany', 'Payroll', 'Tax', 'Treasury deal', 'Dividend'];
  var channels = { GBP: 'CHAPS', EUR: 'SEPA', USD: 'Fedwire', SGD: 'MEPS+', HKD: 'CHATS', AED: 'UAEFTS', CNY: 'CIPS', JPY: 'SWIFT' };
  var initiators = ['M. Okafor (Treasury)', 'L. Brennan (AP)', 'S. Iyer (Treasury)', 'D. Keller (Finance)', 'A. Haddad (Gulf finance)', 'J. Tan (APAC finance)'];
  var payments = [];
  for (var k = 1; k <= 96; k++) {
    var pe = entities[k % entities.length], pc = rnd() < 0.7 ? pe.ccy : pick(currencies);
    var big = rnd() < 0.18, pa = r2((big ? between(5.2e6, 42e6) : between(0.04e6, 4.6e6)) / fx[pc]);
    var st = big ? (k % 5 === 0 ? 'Released' : 'Awaiting your approval') : pick(['Released', 'Released', 'Released', 'Approved', 'Scheduled', 'Awaiting second approver', 'Rejected']);
    var created = Math.floor(between(0, 29));
    payments.push({ id: 'PAY-' + (26000 + k * 7), entity: pe.id, region: pe.region, ccy: pc, amount: pa, gbp: gbp(pc, pa),
      beneficiary: pick(cps), type: big ? pick(['Intercompany', 'Treasury deal', 'Dividend', 'Tax']) : pick(payTypes), channel: channels[pc],
      created: daysAgo(created), valueDate: daysAgo(Math.max(-5, created - Math.floor(between(0, 4)))), status: st,
      initiator: pick(initiators), reference: 'INV-' + (70000 + Math.floor(rnd() * 9000)), audit: [] });
  }

  /* ---- transactions (ledger) — the Data-grid's rows derive from these ---- */
  var txTypes = ['Receipt', 'Supplier payment', 'Intercompany', 'Payroll', 'Tax', 'FX settlement', 'Interest', 'Fee'];
  var transactions = [];
  for (var t = 1; t <= 240; t++) {
    var te = entities[(t * 7) % entities.length], acc = pick(accounts.filter(function (a) { return a.entity === te.id; }));
    var tt = pick(txTypes), sign = (tt === 'Receipt' || tt === 'Interest' || (tt === 'Intercompany' && rnd() < 0.5)) ? 1 : -1;
    var ta = r2(between(8e3, 3.8e6) / fx[acc.ccy]) * sign;
    transactions.push({ id: t, date: daysAgo(Math.floor(between(0, 89))), entity: te.id, region: te.region, account: acc.id, ccy: acc.ccy,
      amount: ta, gbp: gbp(acc.ccy, ta), counterparty: pick(cps), type: tt, ref: pick(['INV-', 'PO-', 'IC-', 'TAX-', 'FX-']) + (10000 + Math.floor(rnd() * 89999)) });
  }
  transactions.sort(function (a, b) { return a.date < b.date ? 1 : -1; });

  /* ---- FX: 30 GBP/USD sessions (USD per GBP), forwards, hedge ratios ---- */
  var fxSeries = {};
  ['USD', 'EUR', 'SGD', 'HKD', 'AED', 'CNY', 'JPY'].forEach(function (c) {
    var arr = [], v = fx[c] * between(0.97, 1.03);
    for (var i = 0; i < 30; i++) { v = v * (1 + between(-0.004, 0.004)); arr.push(v); }
    arr[29] = fx[c]; fxSeries[c] = arr.map(function (x) { return +x.toFixed(c === 'JPY' ? 6 : 4); });
  });
  /* 30 illustrative OHLC sessions per pair, units of currency per GBP, closing on the series above */
  var candles = {};
  Object.keys(fxSeries).forEach(function (c) { var dp = c === 'JPY' ? 2 : 4, prev = 1 / fxSeries[c][0];
    candles[c] = fxSeries[c].map(function (v, i) { var cl = 1 / v, o = prev, sp = Math.abs(cl - o) + cl * between(0.0008, 0.004);
      prev = cl; return { date: dates[DAYS - 30 + i], open: +o.toFixed(dp), close: +cl.toFixed(dp), high: +(Math.max(o, cl) + sp * between(0.1, 0.6)).toFixed(dp), low: +(Math.min(o, cl) - sp * between(0.1, 0.6)).toFixed(dp) }; }); });
  var fxDeals = [];
  for (var f2 = 1; f2 <= 34; f2++) {
    var fe = entities[f2 % entities.length], fc = pick(['USD', 'EUR', 'SGD', 'HKD', 'AED', 'CNY', 'JPY'].filter(function (c) { return c !== fe.ccy; }));
    var notional = r2(between(2e6, 60e6) / fx[fc]);
    fxDeals.push({ id: 'FXD-' + (8800 + f2), entity: fe.id, region: fe.region, ccy: fc, pair: 'GBP/' + fc, side: rnd() < 0.5 ? 'Buy ' + fc : 'Sell ' + fc,
      product: pick(['Forward', 'Forward', 'Swap', 'Spot']), amount: notional, gbp: gbp(fc, notional), rate: +(1 / fx[fc] * between(0.985, 1.015)).toFixed(4),
      trade: daysAgo(Math.floor(between(1, 60))), value: daysAhead(Math.floor(between(2, 180))), status: pick(['Confirmed', 'Confirmed', 'Settled', 'Awaiting confirmation']) });
  }
  var hedge = [ { ccy: 'USD', actual: 78, target: 75 }, { ccy: 'EUR', actual: 71, target: 75 }, { ccy: 'SGD', actual: 62, target: 60 },
    { ccy: 'HKD', actual: 55, target: 60 }, { ccy: 'CNY', actual: 41, target: 60 }, { ccy: 'AED', actual: 66, target: 50 } ];

  /* ---- trade finance ---- */
  var tfTypes = ['Import letter of credit', 'Export letter of credit', 'Bank guarantee', 'Standby letter of credit', 'Documentary collection', 'Supply chain finance'];
  var trade = [];
  for (var q = 1; q <= 48; q++) {
    var qe = entities[(q * 3) % entities.length], qc = rnd() < 0.55 ? 'USD' : qe.ccy, qa = r2(between(0.3e6, 24e6) / fx[qc]);
    var issued = Math.floor(between(3, 200)), tenor = Math.floor(between(30, 360));
    trade.push({ id: 'TF-' + (41000 + q * 13), type: pick(tfTypes), entity: qe.id, region: qe.region, ccy: qc, amount: qa, gbp: gbp(qc, qa),
      counterparty: pick(cps), issued: daysAgo(issued), expiry: daysAhead(tenor - issued > 5 ? tenor - issued : 12), tenor: tenor,
      status: pick(['Issued', 'Issued', 'Documents presented', 'Amendment requested', 'Discrepant documents', 'Paid']) });
  }

  /* ---- reports ---- */
  var reportCatalogue = [
    ['Group cash position', 'Liquidity', 'Daily'], ['Liquidity and funding headroom', 'Liquidity', 'Weekly'],
    ['Payments released and pending', 'Payments', 'Daily'], ['FX exposure and hedging', 'Markets', 'Weekly'],
    ['Limit utilisation', 'Risk', 'Daily'], ['Risk exceptions register', 'Risk', 'Weekly'],
    ['Trade finance portfolio', 'Trade', 'Monthly'], ['Bank fee analysis', 'Cost', 'Monthly'],
    ['Intercompany positions', 'Liquidity', 'Weekly'], ['Board treasury pack', 'Governance', 'Monthly'],
    ['Counterparty exposure', 'Risk', 'Weekly'], ['Debt maturity profile', 'Liquidity', 'Monthly']];
  var reports = reportCatalogue.map(function (r, i) {
    return { id: 'RPT-' + (100 + i), name: r[0], category: r[1], frequency: r[2], lastRun: daysAgo(i % 7), format: pick(['PDF', 'CSV', 'Excel']),
      runs: Array.apply(null, Array(12)).map(function () { return Math.floor(between(2, 26)); }) };
  });

  /* ---- messages and service requests ---- */
  var senders = ['Your relationship manager', 'HSBC Global Liquidity desk', 'HSBC Trade services', 'HSBC Client service', 'HSBC Markets', 'HSBC Compliance'];
  var subjects = ['Quarter-end liquidity window', 'Facility amendment draft ready for review', 'Documents received under your import LC',
    'Rate indication for your USD forward', 'KYC periodic review due', 'Planned maintenance this Sunday', 'New cut-off times for CNY payments',
    'Your RCF utilisation notice', 'Discrepancy notice — export collection', 'Invitation: treasury outlook briefing', 'Card programme renewal',
    'Sweep structure proposal for APAC', 'Confirmation of dividend payment', 'Sanctions screening query', 'Monthly fee statement available',
    'Interest rate reset notice', 'Guarantee expiry reminder', 'Account opening complete'];
  var messages = subjects.map(function (s, i) {
    var e = entities[i % entities.length];
    return { id: 'MSG-' + (900 + i), subject: s, from: senders[i % senders.length], entity: e.id, region: e.region, ccy: e.ccy,
      date: daysAgo(Math.floor(i * 1.6)), read: i > 5, category: pick(['Action required', 'Information', 'Information', 'Service']),
      body: 'Dear Aldergrove team, ' + s.toLowerCase() + ' for ' + e.name + '. Please review the details in the attached summary and reply here if anything needs to change. This is an illustrative message.',
      thread: [] };
  });
  var srTypes = ['Facility amendment', 'Signatory mandate change', 'New account opening', 'Payment investigation', 'KYC document refresh', 'Card programme change'];
  var srStatus = ['Submitted', 'In progress', 'In progress', 'Awaiting your information', 'Resolved', 'Resolved'];
  var serviceRequests = [];
  for (var r = 1; r <= 16; r++) {
    var re = entities[(r * 5) % entities.length], opened = Math.floor(between(1, 80)), stS = pick(srStatus);
    serviceRequests.push({ id: 'SR-' + (61200 + r * 11), type: pick(srTypes), entity: re.id, region: re.region, ccy: re.ccy, priority: pick(['Standard', 'Standard', 'High', 'Urgent']),
      opened: daysAgo(opened), status: stS, resolutionDays: stS === 'Resolved' ? Math.floor(between(1, 14)) : null,
      summary: 'Illustrative request raised by the CEO office for ' + re.short + '.', updates: [ { date: daysAgo(opened), text: 'Request received by HSBC client service.', tone: 'ok' } ] });
  }
  var alertsSent = Array.apply(null, Array(30)).map(function () { return Math.floor(between(4, 22)); });

  window.CEO_DATA = {
    asAt: iso(AS_AT), asAtLabel: '26 September 2026, 10:00 London', reporting: 'GBP', fx: fx, fxNote: 'Illustrative rates, GBP per one unit, 26 Sep 2026 10:00 London — not market data',
    regions: regions, entities: entities, currencies: currencies, accounts: accounts, dates: dates, daily: daily,
    facilities: facilities, policy: policy, maturities: maturities, positions: positions, limits: limits, exceptions: exceptions,
    payments: payments, transactions: transactions, candles: candles, fxSeries: fxSeries, fxDeals: fxDeals, hedge: hedge,
    trade: trade, reports: reports, messages: messages, serviceRequests: serviceRequests, alertsSent: alertsSent, counterparties: cps
  };
  /* The Data-grid's rows: a LIVE array the grid's own script reads as its DATA (see the grid's one-line extension). */
  window.CEO_GRID_ROWS = [];
}());
