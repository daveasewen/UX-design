/* ============================================================================================
   CEO international banking prototype — the page's ONE data model and its wiring.
   Authored JavaScript (generate-from-canon rule 2a, s258-D1). Charts are drawn by the pack's
   engine: window.dvRender(figure, spec) — the spec is built here from DATA, never geometry.
   Every number on the page is derived from DATA at render time (rule 13); nothing is typed twice.
   Simulated only: no network, no credentials, no live banking connection.
   ============================================================================================ */
(function () {
'use strict';

/* ---------------------------------------------------------------- deterministic generator */
var seed = 20260925;
function rnd() { seed |= 0; seed = seed + 0x6D2B79F5 | 0; var t = Math.imul(seed ^ seed >>> 15, 1 | seed);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }
function pick(a) { return a[Math.floor(rnd() * a.length)]; }
function between(a, b) { return a + rnd() * (b - a); }
function r2(v) { return Math.round(v * 100) / 100; }
function pad(n, w) { n = String(n); while (n.length < w) { n = '0' + n; } return n; }

/* ---------------------------------------------------------------- dates */
var AS_AT = new Date(Date.UTC(2026, 8, 25));           /* 25 Sep 2026 — the reporting date */
var DAY = 86400000;
function dayISO(offset) { return new Date(AS_AT.getTime() - offset * DAY).toISOString().slice(0, 10); }
function daysBefore(iso) { return Math.round((AS_AT.getTime() - Date.parse(iso + 'T00:00:00Z')) / DAY); }
var MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
function fmtDate(iso) { var d = new Date(iso + 'T00:00:00Z'); return d.getUTCDate() + ' ' + MONTHS[d.getUTCMonth()] + ' ' + d.getUTCFullYear(); }
function shortDate(iso) { var d = new Date(iso + 'T00:00:00Z'); return d.getUTCDate() + ' ' + MONTHS[d.getUTCMonth()]; }
var SERIES_DAYS = [];                                    /* 30 daily points, oldest first */
for (var sd = 29; sd >= 0; sd--) { SERIES_DAYS.push(dayISO(sd)); }

/* ---------------------------------------------------------------- the data model */
var DATA = {
  asAt: dayISO(0),
  /* ILLUSTRATIVE FX — units of each currency bought by 1 GBP. Placeholders for design, not market data. */
  fx: { GBP: 1, USD: 1.3420, EUR: 1.1650, SGD: 1.7280, HKD: 10.4500, AED: 4.9290, CNY: 9.5700 },
  regions: ['United Kingdom', 'Europe', 'Americas', 'Asia-Pacific', 'Middle East'],
  entities: [
    { id: 'NWG-UK', name: 'Northwind Group plc', region: 'United Kingdom', ccy: 'GBP' },
    { id: 'NWG-DE', name: 'Northwind Deutschland GmbH', region: 'Europe', ccy: 'EUR' },
    { id: 'NWG-FR', name: 'Northwind France SAS', region: 'Europe', ccy: 'EUR' },
    { id: 'NWG-US', name: 'Northwind Americas Inc.', region: 'Americas', ccy: 'USD' },
    { id: 'NWG-SG', name: 'Northwind Asia Pte. Ltd.', region: 'Asia-Pacific', ccy: 'SGD' },
    { id: 'NWG-HK', name: 'Northwind Hong Kong Ltd', region: 'Asia-Pacific', ccy: 'HKD' },
    { id: 'NWG-AE', name: 'Northwind Middle East FZE', region: 'Middle East', ccy: 'AED' }
  ],
  accounts: [], transactions: [], facilities: [], plannedNeed: [], payments: [], deals: [], fxSeries: {},
  positions: [], limits: [], exceptions: [], trade: [], reports: [], messages: [], requests: [], mmf: []
};
var ENT = {}; DATA.entities.forEach(function (e) { ENT[e.id] = e; });
function toGBP(amount, ccy) { return amount / DATA.fx[ccy]; }

var COUNTERPARTIES = ['Atlas Components Ltd', 'Borealis Shipping AS', 'Castellan Steel SA', 'Delphine Logistics BV', 'Everly Packaging Inc.',
  'Fairhaven Energy plc', 'Granite Freight LLC', 'Harbourline Ports Pte', 'Ionic Semiconductors KK', 'Juniper Chemicals GmbH',
  'Kestrel Aerospace Ltd', 'Lumen Retail SAS', 'Meridian Foods Inc.', 'Northgate Utilities', 'Orchard Pharma AG',
  'Pioneer Textiles Ltd', 'Quayside Engineering', 'Riverton Paper Co.', 'Saffron Trading FZE', 'Tidewater Metals Inc.'];

/* accounts — 3 or 4 per entity, a 30-day balance walk each (local currency) */
var ACC_KINDS = ['Operating account', 'Collections account', 'Payroll account', 'Deposit account', 'USD currency account'];
DATA.entities.forEach(function (e, ei) {
  var n = ei === 0 ? 4 : 3 + (ei % 2);
  for (var k = 0; k < n; k++) {
    var kind = ACC_KINDS[k], ccy = kind === 'USD currency account' ? 'USD' : e.ccy;
    var baseGBP = (ei === 0 ? 180 : 60) * between(0.35, 1.4) * (k === 3 ? 1.6 : 1);   /* £m */
    var bal = baseGBP * DATA.fx[ccy] * 1e6, walk = [];
    for (var d = 0; d < 30; d++) { bal = Math.max(bal * (1 + between(-0.035, 0.04)), 2e6); walk.push(Math.round(bal)); }
    DATA.accounts.push({ id: e.id.slice(4) + '-' + pad(4100 + ei * 10 + k, 4), name: kind, entity: e.id, region: e.region,
      ccy: ccy, series: walk, balance: walk[29], iban: 'GB' + pad(Math.floor(rnd() * 99), 2) + ' HBUK •••• ' + pad(Math.floor(rnd() * 9999), 4) });
  }
});

/* transactions — 320 over the 30 days */
var TX_TYPES = [['Customer receipt', 1], ['Supplier payment', -1], ['Payroll', -1], ['Tax payment', -1], ['Intercompany transfer', 0],
  ['FX settlement', 0], ['Card settlement', -1], ['Interest', 1], ['Dividend received', 1], ['Loan repayment', -1]];
for (var ti = 0; ti < 320; ti++) {
  var acc = pick(DATA.accounts), tt = pick(TX_TYPES), sign = tt[1] === 0 ? (rnd() < 0.5 ? -1 : 1) : tt[1];
  var mag = Math.exp(between(Math.log(20000), Math.log(18e6)));
  var amt = Math.round(sign * mag * DATA.fx[acc.ccy] / 100) * 100;
  DATA.transactions.push({ id: 'TX-' + pad(880000 + ti * 7, 6), date: dayISO(Math.floor(rnd() * 30)), account: acc.id, entity: acc.entity,
    region: acc.region, counterparty: tt[0] === 'Intercompany transfer' ? pick(DATA.entities).name : pick(COUNTERPARTIES),
    type: tt[0], ccy: acc.ccy, amount: amt, gbp: toGBP(amt, acc.ccy), status: rnd() < 0.93 ? 'Settled' : 'Pending' });
}

/* money-market funds (GBP m) — a 30-day level */
(function () { var v = 420; for (var d = 0; d < 30; d++) { v = v * (1 + between(-0.02, 0.022)); DATA.mmf.push(v); } }());

/* funding facilities (GBP m) */
[['RCF-01', 'Syndicated revolving credit facility', 'NWG-UK', 'Revolving credit', 1500, 420, '2029-06-30', 85],
 ['TL-02', 'Term loan A', 'NWG-UK', 'Term loan', 600, 600, '2028-03-31', 100],
 ['CP-03', 'Euro commercial paper programme', 'NWG-UK', 'Commercial paper', 1000, 310, '2027-01-15', 90],
 ['RCF-04', 'US revolving credit facility', 'NWG-US', 'Revolving credit', 450, 265, '2028-09-30', 85],
 ['TF-05', 'Trade finance line — Asia', 'NWG-SG', 'Trade line', 300, 214, '2027-06-30', 80],
 ['TF-06', 'Trade finance line — Europe', 'NWG-DE', 'Trade line', 220, 96, '2027-03-31', 80],
 ['OD-07', 'Overdraft — Hong Kong', 'NWG-HK', 'Overdraft', 60, 41, '2027-09-30', 75],
 ['OD-08', 'Overdraft — Middle East', 'NWG-AE', 'Overdraft', 45, 12, '2027-09-30', 75],
 ['BL-09', 'Bilateral facility — France', 'NWG-FR', 'Revolving credit', 180, 150, '2027-12-31', 85]
].forEach(function (f) {
  DATA.facilities.push({ id: f[0], name: f[1], entity: f[2], region: ENT[f[2]].region, type: f[3], limit: f[4], drawn: f[5],
    maturity: f[6], internalLimit: f[7], committed: f[3] !== 'Overdraft', history: [] });
});
/* planned funding need over the next 90 days by entity (GBP m): capex, maturities, dividends */
DATA.entities.forEach(function (e, i) { DATA.plannedNeed.push({ entity: e.id, region: e.region, amount: [1450, 260, 140, 520, 210, 95, 70][i] }); });

/* payments — 140, a spread of statuses; the approvals the CEO acts on are "Pending approval" */
var PAY_TYPES = ['Supplier payment', 'Intercompany funding', 'Tax payment', 'Dividend', 'Capital expenditure', 'Debt service'];
var PAY_STATUS = ['Pending approval', 'Released', 'Released', 'Released', 'Scheduled', 'Rejected', 'Released', 'Pending approval'];
for (var pi = 0; pi < 140; pi++) {
  var pe = pick(DATA.entities), pccy = rnd() < 0.7 ? pe.ccy : pick(['USD', 'EUR', 'GBP', 'CNY']);
  var pgbp = Math.exp(between(Math.log(0.15), Math.log(24)));          /* £m */
  var created = Math.floor(rnd() * 30), pst = pick(PAY_STATUS);
  if (pi < 16) { pst = 'Pending approval'; created = Math.floor(rnd() * 5); }
  if (pst === 'Pending approval' && created > 5) { pst = 'Released'; }
  var pamt = Math.round(pgbp * 1e6 * DATA.fx[pccy] / 100) * 100;
  DATA.payments.push({ id: 'PAY-' + pad(24100 + pi, 5), created: dayISO(created), valueDate: dayISO(Math.max(created - 2, -6)),
    entity: pe.id, region: pe.region, beneficiary: pick(COUNTERPARTIES), type: pick(PAY_TYPES), ccy: pccy, amount: pamt,
    gbp: toGBP(pamt, pccy), status: pst, direction: 'out', approvals: pst === 'Pending approval' ? '1 of 2' : '2 of 2',
    requestedBy: pick(['A. Okafor (Group treasury)', 'M. Lindqvist (Treasury operations)', 'S. Chen (Regional finance)', 'R. Patel (Accounts payable)']),
    audit: [{ at: dayISO(created), who: 'Maker', note: 'Payment created and submitted for approval' }] });
}

/* FX — 30 sessions per pair against GBP, ending on the illustrative rate. GBP/USD also carries OHLC. */
['USD', 'EUR', 'SGD', 'HKD', 'AED'].forEach(function (c) {
  var end = DATA.fx[c], v = end * between(0.975, 1.02), closes = [], ohlc = [];
  for (var d = 0; d < 30; d++) {
    var open = v, target = end + (v - end) * (1 - (d + 1) / 30);
    var close = target * (1 + between(-0.0045, 0.0045)); if (d === 29) { close = end; }
    var hi = Math.max(open, close) * (1 + between(0.0005, 0.004)), lo = Math.min(open, close) * (1 - between(0.0005, 0.004));
    ohlc.push([open, hi, lo, close]); closes.push(close); v = close;
  }
  DATA.fxSeries[c] = { closes: closes, ohlc: ohlc };
});

/* hedges and deals — 48 */
var PAIRS = ['GBP/USD', 'GBP/EUR', 'GBP/SGD', 'GBP/HKD', 'GBP/AED', 'EUR/USD'];
for (var di = 0; di < 48; di++) {
  var de = pick(DATA.entities), pair = pick(PAIRS), q = pair.split('/')[1];
  var base = q === 'USD' && pair.indexOf('EUR') === 0 ? 1.152 : DATA.fx[q];
  DATA.deals.push({ id: 'FXD-' + pad(51200 + di * 3, 5), trade: dayISO(Math.floor(rnd() * 200)), entity: de.id, region: de.region,
    product: pick(['Forward', 'Forward', 'Swap', 'Spot', 'Window forward']), pair: pair, notional: r2(between(2, 65)),
    rate: Math.round(base * between(0.985, 1.015) * 10000) / 10000, maturity: dayISO(-Math.floor(between(5, 360))),
    mtm: Math.round(between(-900, 1100)), status: rnd() < 0.85 ? 'Open' : 'Settled', ccy: q });
}

/* exposure positions — 72, by entity, counterparty, currency and product (GBP m) */
var PRODUCTS = ['Deposits placed', 'Derivative MTM', 'Trade receivables', 'Guarantees issued', 'Settlement exposure'];
var RATINGS = ['AA', 'AA-', 'A+', 'A', 'A-', 'BBB+', 'BBB', 'BB+'];
var CP_RATING = {}; COUNTERPARTIES.forEach(function (c) { CP_RATING[c] = pick(RATINGS); });
for (var xi = 0; xi < 72; xi++) {
  var xe = pick(DATA.entities), xc = rnd() < 0.55 ? xe.ccy : pick(['USD', 'EUR', 'CNY', 'GBP']), cp = pick(COUNTERPARTIES);
  DATA.positions.push({ id: 'POS-' + pad(3100 + xi, 4), entity: xe.id, region: xe.region, counterparty: cp, rating: CP_RATING[cp],
    ccy: xc, product: pick(PRODUCTS), gbp: r2(Math.exp(between(Math.log(4), Math.log(160)))) });
}

/* limits — counterparty limits for every counterparty with positions, plus country limits */
COUNTERPARTIES.forEach(function (cp, i) {
  var used = DATA.positions.filter(function (p) { return p.counterparty === cp; }).reduce(function (s, p) { return s + p.gbp; }, 0);
  if (!used) { return; }
  var first = DATA.positions.filter(function (p) { return p.counterparty === cp; })[0];
  var headroomFactor = [0.92, 1.35, 1.8, 0.98, 1.2, 2.4, 1.05, 1.6, 0.88, 1.45][i % 10];
  DATA.limits.push({ id: 'LIM-C' + pad(i + 1, 2), name: cp, kind: 'Counterparty', rating: CP_RATING[cp], region: first.region,
    entity: first.entity, limit: Math.round(used * headroomFactor), used: r2(used) });
});
DATA.regions.forEach(function (rg, i) {
  var used = DATA.positions.filter(function (p) { return p.region === rg; }).reduce(function (s, p) { return s + p.gbp; }, 0);
  DATA.limits.push({ id: 'LIM-R' + pad(i + 1, 2), name: rg, kind: 'Country and region', rating: '', region: rg, entity: null,
    limit: Math.round(used * [1.25, 1.1, 0.97, 1.4, 1.9][i]), used: r2(used) });
});
DATA.limits.forEach(function (l) { l.util = Math.round(l.used / l.limit * 1000) / 10;
  l.status = l.util >= 100 ? 'Breach' : l.util >= 90 ? 'Near limit' : 'Within limit'; });

/* exceptions — every limit at or over 90%, plus operational exceptions */
DATA.limits.filter(function (l) { return l.util >= 90; }).forEach(function (l, i) {
  var material = l.util >= 100 || (l.util >= 90 && ['BBB+', 'BBB', 'BB+'].indexOf(l.rating) >= 0);
  DATA.exceptions.push({ id: 'EXC-' + pad(701 + i, 3), raised: dayISO(Math.floor(rnd() * 12)), entity: l.entity || 'NWG-UK',
    region: l.region, limitId: l.id, title: (l.util >= 100 ? 'Limit breach — ' : 'Limit above 90% — ') + l.name,
    severity: material ? 'Material' : 'Moderate', status: 'Open', detail: l.kind + ' limit ' + l.id + ' is at ' + l.util + '% of £' + l.limit + 'm.', audit: [] });
});
[['Late trade confirmation — Castellan Steel SA', 'NWG-FR', 'Moderate'], ['Covenant headroom below 15% — Bilateral facility France', 'NWG-FR', 'Material'],
 ['Unmatched settlement — GBP/HKD swap', 'NWG-HK', 'Moderate'], ['Sanctions screening hit pending review — Saffron Trading FZE', 'NWG-AE', 'Material']
].forEach(function (x, i) {
  DATA.exceptions.push({ id: 'EXC-' + pad(760 + i, 3), raised: dayISO(Math.floor(rnd() * 20)), entity: x[1], region: ENT[x[1]].region,
    limitId: null, title: x[0], severity: x[2], status: 'Open', detail: 'Raised by the monitoring rule set. Needs an acknowledgement with an audit note.', audit: [] });
});

/* trade finance — 56 instruments */
var TF_TYPES = ['Import letter of credit', 'Export letter of credit', 'Standby letter of credit', 'Bank guarantee', 'Documentary collection'];
for (var fi2 = 0; fi2 < 56; fi2++) {
  var fe = pick(DATA.entities), fccy = rnd() < 0.6 ? 'USD' : pick([fe.ccy, 'EUR', 'CNY']);
  var fgbp = Math.exp(between(Math.log(0.2), Math.log(28)));
  var famt = Math.round(fgbp * 1e6 * DATA.fx[fccy] / 1000) * 1000;
  DATA.trade.push({ id: 'TF-' + pad(93000 + fi2 * 11, 5), type: pick(TF_TYPES), entity: fe.id, region: fe.region,
    counterparty: pick(COUNTERPARTIES), ccy: fccy, amount: famt, gbp: toGBP(famt, fccy), issued: dayISO(Math.floor(between(0, 150))),
    expiry: dayISO(-Math.floor(between(-4, 120))), status: pick(['Issued', 'Issued', 'Issued', 'Documents presented', 'Amendment requested']), audit: [] });
}
DATA.trade.forEach(function (t) { if (daysBefore(t.expiry) > 0) { t.status = 'Expired'; } });

/* reports */
[['RPT-01', 'Group liquidity position', 'Liquidity', 'Daily'], ['RPT-02', 'Cash by entity and currency', 'Cash', 'Daily'],
 ['RPT-03', 'Funding headroom and facility usage', 'Liquidity', 'Weekly'], ['RPT-04', 'Payments released', 'Payments', 'Daily'],
 ['RPT-05', 'Approvals audit trail', 'Payments', 'Weekly'], ['RPT-06', 'FX exposure and hedge ratio', 'Markets', 'Weekly'],
 ['RPT-07', 'Hedge book maturity ladder', 'Markets', 'Monthly'], ['RPT-08', 'Counterparty exposure', 'Risk', 'Daily'],
 ['RPT-09', 'Limit utilisation and breaches', 'Risk', 'Daily'], ['RPT-10', 'Risk exceptions and acknowledgements', 'Risk', 'Weekly'],
 ['RPT-11', 'Trade instruments outstanding', 'Trade', 'Weekly'], ['RPT-12', 'Instruments expiring in 90 days', 'Trade', 'Monthly'],
 ['RPT-13', 'Board treasury pack', 'Board', 'Monthly'], ['RPT-14', 'Service requests and resolution times', 'Service', 'Monthly'],
 ['RPT-15', 'Bank fees by entity', 'Cash', 'Monthly'], ['RPT-16', 'Intercompany positions', 'Cash', 'Weekly']
].forEach(function (r, i) {
  DATA.reports.push({ id: r[0], name: r[1], category: r[2], frequency: r[3], lastRun: dayISO(i % 9), status: 'Ready', entity: null, region: null });
});

/* messages and service requests */
var FROMS = ['Relationship manager — J. Morgan-Hale', 'HSBC Global Liquidity and Cash Management', 'HSBC Markets desk', 'HSBC Trade services', 'HSBCnet service team'];
var SUBJ = ['Quarterly relationship review — agenda', 'Change to cut-off times for EUR payments', 'Your forward book — upcoming maturities',
  'Letter of credit presentation received', 'Planned maintenance window on Sunday', 'Credit facility renewal — term sheet', 'New user access request approved',
  'Sanctions review — additional information needed', 'Rate indication for GBP/USD 6-month forward', 'Cash pooling structure proposal'];
for (var mi = 0; mi < 26; mi++) {
  var me = pick(DATA.entities);
  DATA.messages.push({ id: 'MSG-' + pad(4400 + mi, 4), date: dayISO(Math.floor(rnd() * 30)), from: pick(FROMS), subject: pick(SUBJ),
    entity: me.id, region: me.region, status: mi < 7 ? 'Unread' : (mi < 11 ? 'Awaiting your reply' : 'Read'),
    body: 'Dear Northwind treasury team, please find the details on this topic below. This message is simulated for the prototype and contains no real client information.',
    thread: [] });
}
var SR_CATS = ['Payment investigation', 'Mandate and signatory change', 'Trade instrument amendment', 'User access', 'Account opening or closure'];
for (var si = 0; si < 18; si++) {
  var se = pick(DATA.entities), sst = pick(['Open', 'In progress', 'Awaiting you', 'Resolved', 'Resolved']);
  DATA.requests.push({ id: 'SR-' + pad(60210 + si * 4, 5), opened: dayISO(Math.floor(rnd() * 30)), entity: se.id, region: se.region,
    category: pick(SR_CATS), subject: pick(['Beneficiary did not receive funds', 'Add authorised signatory', 'Extend expiry by 60 days',
      'Reset user token', 'Close dormant collections account', 'Increase daily payment limit']), status: sst,
    resolvedDays: sst === 'Resolved' ? Math.round(between(1, 9)) : null, detail: 'Simulated request raised in the prototype.' });
}

/* exposure over the 30 days, as a factor per region ending at today's positions (1.0) */
DATA.expWalk = {};
DATA.regions.forEach(function (rg) { var f = 1, w = [1]; for (var d = 0; d < 29; d++) { f = f * (1 + between(-0.025, 0.022)); w.unshift(f); } DATA.expWalk[rg] = w; });

/* ---------------------------------------------------------------- persisted workflow state
   Simulated workflow outcomes live in localStorage ("ceo.work") and are re-applied over DATA on
   load, so an approval, an acknowledgement or a new request survives a reload. */
function load(k, d) { try { var v = JSON.parse(localStorage.getItem(k)); return v == null ? d : v; } catch (e) { return d; } }
function save(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { /* private mode — state is session-only */ } }
var WORK = load('ceo.work', {});
['payments', 'exceptions', 'trade', 'messages', 'reports'].forEach(function (k) { WORK[k] = WORK[k] || {}; });
['newRequests', 'newDeals', 'drawdowns'].forEach(function (k) { WORK[k] = WORK[k] || []; });
function persistWork() { save('ceo.work', WORK); }
function applyWork() {
  DATA.payments.forEach(function (p) { var w = WORK.payments[p.id]; if (w) { p.status = w.status; p.approvals = w.approvals || p.approvals; p.audit = p.audit.slice(0, 1).concat(w.audit || []); } });
  DATA.exceptions.forEach(function (x) { var w = WORK.exceptions[x.id]; if (w) { x.status = w.status; x.audit = w.audit || []; } });
  DATA.trade.forEach(function (t) { var w = WORK.trade[t.id]; if (w) { t.status = w.status; t.audit = w.audit || []; } });
  DATA.messages.forEach(function (m) { var w = WORK.messages[m.id]; if (w) { m.status = w.status; m.thread = w.thread || []; } });
  DATA.reports.forEach(function (r) { var w = WORK.reports[r.id]; if (w) { r.lastRun = w.lastRun; r.status = w.status; } });
  WORK.newRequests.forEach(function (r) { if (!DATA.requests.some(function (x) { return x.id === r.id; })) { DATA.requests.unshift(r); } });
  WORK.newDeals.forEach(function (d) { if (!DATA.deals.some(function (x) { return x.id === d.id; })) { DATA.deals.unshift(d); } });
  WORK.drawdowns.forEach(function (d) { var f = DATA.facilities.filter(function (x) { return x.id === d.facility; })[0];
    if (f && !f.history.some(function (h) { return h.id === d.id; })) { f.drawn = r2(f.drawn + d.amount); f.history.push(d); } });
}
applyWork();

/* ---------------------------------------------------------------- view state (URL + localStorage) */
var UI = load('ceo.ui', { sort: {}, pp: {}, tab: {} });
UI.sort = UI.sort || {}; UI.pp = UI.pp || {}; UI.tab = UI.tab || {};
var saved = load('ceo.filters', {});
var STATE = { view: 'overview', record: null, entity: saved.entity || 'all', region: saved.region || 'all', days: saved.days || 30,
  q: '', status: null, page: {} };
var VIEWS = ['overview', 'accounts', 'liquidity', 'payments', 'fx', 'risk', 'trade', 'reports', 'messages', 'settings'];
var TITLES = {};
function persistUI() { save('ceo.ui', UI); save('ceo.filters', { entity: STATE.entity, region: STATE.region, days: STATE.days }); }

/* ---------------------------------------------------------------- formatting */
function grp3(n, dp) { var s = Math.abs(n).toFixed(dp || 0).split('.'); s[0] = s[0].replace(/\B(?=(\d{3})+(?!\d))/g, ','); return (n < 0 ? '−' : '') + s.join('.'); }
function gbpM(m, dp) { return (m < 0 ? '−£' : '£') + grp3(Math.abs(m), dp == null ? 1 : dp) + 'm'; }
function money(amount, ccy) { return ccy + ' ' + grp3(amount, 0); }
function pct(v, dp) { return (Math.round(v * Math.pow(10, dp || 1)) / Math.pow(10, dp || 1)).toFixed(dp == null ? 1 : dp) + '%'; }
function esc(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return c === '&' ? '&amp;' : c === '<' ? '&lt;' : c === '>' ? '&gt;' : '&quot;'; }); }
function sum(a, f) { return a.reduce(function (s, x) { return s + (f ? f(x) : x); }, 0); }
function entName(id) { return ENT[id] ? ENT[id].name : '—'; }

/* ---------------------------------------------------------------- scope: the shared filters */
function inScope(r, dateKey) {
  if (STATE.entity !== 'all' && r.entity && r.entity !== STATE.entity) { return false; }
  if (STATE.region !== 'all' && r.region && r.region !== STATE.region) { return false; }
  if (dateKey && r[dateKey]) { var d = daysBefore(r[dateKey]); if (d >= STATE.days) { return false; } }
  return true;
}
function matchesQ(r, fields) {
  if (!STATE.q) { return true; }
  var q = STATE.q.toLowerCase();
  return fields.some(function (f) { var v = f === 'entity' ? entName(r.entity) : r[f]; return v != null && String(v).toLowerCase().indexOf(q) >= 0; });
}
function scopedEntities() { return DATA.entities.filter(function (e) { return inScope(e); }); }
function periodIdx() { return SERIES_DAYS.slice(30 - STATE.days); }          /* the days in view */
function sliceSeries(a) { return a.slice(30 - STATE.days); }

/* per-day cash (GBP m) for a set of accounts */
function cashSeries(accounts) {
  var out = []; for (var d = 0; d < 30; d++) { out.push(sum(accounts, function (a) { return toGBP(a.series[d], a.ccy) / 1e6; })); }
  return out;
}
function scopedAccounts() { return DATA.accounts.filter(function (a) { return inScope(a); }); }
function scopedFacilities() { return DATA.facilities.filter(function (f) { return inScope(f); }); }
function undrawnCommitted(fs) { return sum(fs.filter(function (f) { return f.committed; }), function (f) { return f.limit - f.drawn; }); }
function mmfShare() { var ents = scopedEntities(); return ents.some(function (e) { return e.id === 'NWG-UK'; }) ? 1 : 0; }  /* MMF sits with the parent */
function liquiditySeries() {
  var cash = cashSeries(scopedAccounts()), und = undrawnCommitted(scopedFacilities()), m = mmfShare();
  return { cash: cash, undrawn: cash.map(function () { return und; }), mmf: DATA.mmf.map(function (v) { return v * m; }),
    total: cash.map(function (c, i) { return c + und + DATA.mmf[i] * m; }) };
}
function plannedNeed() { return sum(DATA.plannedNeed.filter(function (p) { return inScope(p); }), function (p) { return p.amount; }); }

/* ================================================================ CHARTS — clone the verbatim
   snippet figure out of its <template>, make its ids unique, set the words, rebuild the legend
   rows for this data, then hand the spec to the library's engine. */
var ID_ATTRS = ['aria-labelledby', 'aria-controls', 'aria-describedby', 'for', 'data-for', 'data-lockup-table', 'href'];
function uniquify(root, prefix) {
  var map = {};
  [root].concat([].slice.call(root.querySelectorAll('[id]'))).forEach(function (el) {
    if (el.id) { map[el.id] = prefix + '-' + el.id; el.id = map[el.id]; }
  });
  [root].concat([].slice.call(root.querySelectorAll('*'))).forEach(function (el) {
    ID_ATTRS.forEach(function (a) {
      var v = el.getAttribute(a); if (!v) { return; }
      if (a === 'href') { if (v.charAt(0) === '#' && map[v.slice(1)]) { el.setAttribute(a, '#' + map[v.slice(1)]); } return; }
      el.setAttribute(a, v.split(/\s+/).map(function (t) { return map[t] || t; }).join(' '));
    });
  });
}
function rebuildLegend(fig, names) {
  var leg = fig.querySelector('.dv-leg'); if (!leg) { return; }
  var rows = [].slice.call(leg.querySelectorAll('.dv-legrow')); if (!rows.length) { return; }
  var fresh = leg.cloneNode(false), tail = [].slice.call(leg.children).filter(function (c) { return !c.classList.contains('dv-legrow'); });
  names.forEach(function (nm, i) {
    var r = rows[i % rows.length].cloneNode(true), k = String(i + 1);
    r.setAttribute('data-series', k);
    var sw = r.querySelector('.dv-leg-sw');
    if (sw) { sw.setAttribute('style', '--sc:var(--data-series-' + k + ')'); sw.setAttribute('aria-checked', 'true');
      if (sw.hasAttribute('aria-label')) { sw.setAttribute('aria-label', 'Show or hide ' + nm); } }
    var b = r.querySelector('.dv-leg-item');
    if (b) { b.setAttribute('data-series', k); b.setAttribute('aria-pressed', 'false');
      var n = b.querySelector('.dv-leg-name'); if (n) { n.textContent = nm; } else { b.textContent = nm; }
      if (b.hasAttribute('aria-label')) { b.setAttribute('aria-label', 'Isolate ' + nm); } }
    fresh.appendChild(r);
  });
  tail.forEach(function (c) { var cc = c.cloneNode(true); var rb = cc.querySelector('.dv-leg-reset') || (cc.classList.contains('dv-leg-reset') ? cc : null);
    if (rb) { rb.disabled = true; } fresh.appendChild(cc); });
  leg.parentNode.replaceChild(fresh, leg);
}
function chart(id, spec, o, slotEl) {
  var slot = slotEl || document.querySelector('[data-chart="' + id + '"]'); if (!slot || !window.dvRender) { return null; }
  var fig = slot.querySelector('figure.dv'), fresh = false;
  if (!fig) {
    var tpl = document.getElementById('tpl-' + slot.getAttribute('data-tpl'));
    fig = tpl.content.querySelector('figure').cloneNode(true);
    uniquify(fig, id); slot.appendChild(fig); fresh = true;
    /* dv-behaviour's JS-on opt-in, which its parse-time init could not see for a figure cloned later.
       NOT for the radial and standalone-spark canvases: inside the dashboard scope the template's
       bar-family fit rules would stretch them past their own size (reported as a gap). */
    if (['donut', 'pie', 'spark'].indexOf(spec.type) < 0) { fig.classList.add('dv-fit-on'); }            /* dv-behaviour's JS-on opt-in, which its parse-time init could not see for a figure cloned later */
  }
  var t = fig.querySelector('.dv-title'); if (t) { t.textContent = o.title; }
  if (fig.hasAttribute('data-lockup-title')) { fig.setAttribute('data-lockup-title', o.title); }
  var fc = fig.querySelector('figcaption'); if (fc) { fc.textContent = o.caption || o.title; }
  var tp = fig.querySelector('.dv-tablepanel'); if (tp) { tp.setAttribute('aria-label', (o.caption || o.title) + ', data table'); }
  var ls = fig.querySelector('.dv-leg-static span:last-child'); if (ls && spec.series[0]) { ls.textContent = spec.series[0].name; }
  if (spec.type === 'donut' || spec.type === 'pie') {
    fig.setAttribute('data-total', String(Math.round(sum(spec.series[0].values))));
    var nm = spec.categories.join('|'); if (fresh || fig.__names !== nm) { rebuildLegend(fig, spec.categories); fig.__names = nm; }
  } else if (spec.series.length > 1) {
    var sn = spec.series.map(function (s) { return s.name; }).join('|');
    if (fresh || fig.__names !== sn) { rebuildLegend(fig, spec.series.map(function (s) { return s.name; })); fig.__names = sn; }
  }
  fig.__base = spec; fig.__opts = o;
  var srt = fig.querySelector('button[data-dv-view-btn][aria-pressed="true"]');
  var s2 = srt && /^(asc|desc)$/.test(srt.getAttribute('data-dv-view-btn')) ? sortedSpec(spec, srt.getAttribute('data-dv-view-btn')) : spec;
  try { window.dvRender(fig, s2); } catch (e) { console.error('dvRender', id, e); }
  if (o.drill) { fig.setAttribute('data-drill', o.drill); }
  return fig;
}
function sortedSpec(spec, order) {
  var ix = spec.categories.map(function (c, i) { return i; }), v = spec.series[0].values;
  ix.sort(function (a, b) { return order === 'asc' ? v[a] - v[b] : v[b] - v[a]; });
  var out = {}; for (var k in spec) { out[k] = spec[k]; }
  out.categories = ix.map(function (i) { return spec.categories[i]; });
  out.series = spec.series.map(function (s) { var c = {}; for (var k2 in s) { c[k2] = s[k2]; } c.values = ix.map(function (i) { return s.values[i]; }); return c; });
  return out;
}
/* the column snippet's Original / Ascending / Descending seg re-renders from the stored spec
   (Chart-bar's own engine-call idiom, generalised to every mounted column figure) */
document.addEventListener('click', function (e) {
  var b = e.target.closest && e.target.closest('button[data-dv-view-btn]'); if (!b) { return; }
  var fig = b.closest('figure.dv'); var ord = b.getAttribute('data-dv-view-btn');
  if (!fig || !fig.__base || !/^(orig|asc|desc)$/.test(ord)) { return; }
  setTimeout(function () { window.dvRender(fig, ord === 'orig' ? fig.__base : sortedSpec(fig.__base, ord)); }, 0);
});

/* ================================================================ KPI tiles (Kpi-tile markup, as-link variant) */
function sparkPoints(vals) {
  var lo = Math.min.apply(null, vals), hi = Math.max.apply(null, vals), sp = hi - lo || 1, n = vals.length;
  return vals.map(function (v, i) { return (3 + i * 194 / Math.max(n - 1, 1)).toFixed(1) + ',' + (45 - (v - lo) / sp * 42).toFixed(1); });
}
function kpi(id, o) {
  var tile = document.querySelector('[data-kpi="' + id + '"]'); if (!tile) { return; }
  var link = tile.querySelector('.kpi-link'); link.setAttribute('href', o.href || '#/overview');
  if (o.label) { link.textContent = o.label; tile.setAttribute('aria-label', o.label); }
  var v = tile.querySelectorAll('.kpi-val > span'); v[0].textContent = o.unit || ''; v[1].textContent = o.value;
  var d = tile.querySelector('.kpi-delta'), dir = o.dir || (o.delta > 0.05 ? 'up' : o.delta < -0.05 ? 'down' : 'flat');
  d.className = 'kpi-delta ' + dir;
  d.querySelector('use').setAttribute('href', '#kpi-' + dir);
  d.querySelector('.t-cm-figure-6').textContent = o.deltaText;
  d.querySelector('.kpi-per').textContent = o.per || '';
  var svg = tile.querySelector('.spark-inline');
  if (o.series && o.series.length > 1) {
    var pts = sparkPoints(o.series);
    svg.querySelector('polyline').setAttribute('points', pts.join(' '));
    svg.querySelector('polygon').setAttribute('points', pts.join(' ') + ' 197.0,45 3.0,45');
    svg.setAttribute('data-trend', dir);
  }
}
function deltaPct(now, then) { return then ? (now - then) / Math.abs(then) * 100 : 0; }
function deltaText(p, suffix) { var r = Math.round(p * 10) / 10; if (Math.abs(r) < 0.05) { return 'No change'; }
  if (suffix === '') { return (r > 0 ? '+' : '−') + Math.abs(Math.round(r)) + (r > 0 ? ' up' : ' down'); }
  return (r > 0 ? '+' : '−') + Math.abs(r).toFixed(1) + (suffix || '%') + (r > 0 ? ' up' : ' down'); }

/* ================================================================ status chips (template scope `.status`) */
var STATUS_CLASS = { 'Pending approval': 'warn', 'Released': 'ok', 'Approved': 'ok', 'Scheduled': 'inf', 'Rejected': 'err',
  'Breach': 'err', 'Near limit': 'warn', 'Within limit': 'ok', 'Open': 'warn', 'Acknowledged': 'inf', 'Resolved': 'ok', 'Closed': 'ok',
  'Material': 'err', 'Moderate': 'warn', 'Issued': 'ok', 'Documents presented': 'inf', 'Amendment requested': 'warn', 'Expired': 'err',
  'Unread': 'inf', 'Read': 'ok', 'Awaiting your reply': 'warn', 'Awaiting you': 'warn', 'In progress': 'inf', 'Ready': 'ok',
  'Running': 'inf', 'Settled': 'ok', 'Pending': 'warn', 'Drawn': 'ok' };
function statusClass(t) { return STATUS_CLASS[t] || (/^Value date/.test(t) ? 'warn' : 'inf'); }
function chip(text) {
  return '<span class="status ' + statusClass(text) + '" data-carries="label"><span class="dot" aria-hidden="true"></span><span class="t-cm-legal">' + esc(text) + '</span></span>';
}

/* ================================================================ summary cards (Summary + the template's card idiom) */
function summary(id, head, rows) {
  var tile = document.querySelector('[data-summary="' + id + '"]'); if (!tile) { return; }
  tile.querySelector('dl.summary').innerHTML = head ? '<div class="summary__row"><dt class="summary__k t-cm-label">' + esc(head.k) +
    (head.sub ? ' <span class="t-cm-legal">' + esc(head.sub) + '</span>' : '') + '</dt><dd class="summary__v t-cm-figure-5">' + esc(head.v) + '</dd></div>' : '';
  tile.querySelector('.l-stack').innerHTML = rows.length ? rows.map(function (r) {
    return '<div class="l-row" data-gap="s" data-justify="between">' + (r.href ? '<a class="tpl-link t-cm-label" href="' + r.href + '">' + esc(r.label) + '</a>'
      : '<span class="t-cm-label">' + esc(r.label) + '</span>') + (r.status ? chip(r.status) : '<span class="t-cm-figure-6">' + esc(r.value || '') + '</span>') + '</div>';
  }).join('') : '<span class="t-cm-label">Nothing needs your attention in this scope.</span>';
}

/* ================================================================ record grids (Data-grid markup; authored wiring)
   Each grid: rows() -> scoped + searched rows; cells per column; sort, page size and page persist. */
var GRIDS = {};
function grid(gid, def) { GRIDS[gid] = def; }
function cellHTML(def, col, r) {
  var v = r[col];
  if (def.cell && def.cell[col]) { return def.cell[col](r); }
  if (col === 'id') { return '<a class="tpl-link t-cm-label" href="#/' + def.view + '/' + esc(r.id) + '">' + esc(r.id) + '</a>'; }
  if (col === 'status' || col === 'severity') { return chip(v); }
  if (col === 'entity') { return '<span class="t-cm-label">' + esc(entName(v)) + '</span>'; }
  return '<span class="t-cm-label">' + esc(v) + '</span>';
}
function sortVal(def, col, r) { if (def.sortKey && def.sortKey[col]) { return def.sortKey[col](r); } var v = r[col]; return col === 'entity' ? entName(v) : v; }
function gridRows(gid) {
  var def = GRIDS[gid], rows = def.rows(), s = UI.sort[gid] || def.defaultSort;
  if (s) { rows = rows.slice().sort(function (a, b) { var x = sortVal(def, s.key, a), y = sortVal(def, s.key, b);
    var c = typeof x === 'number' && typeof y === 'number' ? x - y : String(x).localeCompare(String(y)); return s.dir === 'desc' ? -c : c; }); }
  return rows;
}
function renderGrid(gid) {
  var def = GRIDS[gid], root = document.getElementById('dg-' + gid); if (!def || !root) { return; }
  var rows = gridRows(gid), pp = UI.pp[gid] || 10, pages = Math.max(1, Math.ceil(rows.length / pp));
  var page = Math.min(STATE.page[gid] || 1, pages); STATE.page[gid] = page;
  var cols = [].slice.call(root.querySelectorAll('thead th')).map(function (th) { return th.getAttribute('data-key'); });
  var s = UI.sort[gid] || def.defaultSort || {};
  root.querySelectorAll('thead th[aria-sort]').forEach(function (th) {
    th.setAttribute('aria-sort', th.getAttribute('data-key') === s.key ? (s.dir === 'desc' ? 'descending' : 'ascending') : 'none'); });
  var slice = rows.slice((page - 1) * pp, page * pp), tb = root.querySelector('tbody');
  tb.innerHTML = slice.length ? slice.map(function (r) {
    return '<tr data-id="' + esc(r.id) + '">' + cols.map(function (c) {
      var th = root.querySelector('thead th[data-key="' + c + '"]');
      return '<td' + (th && th.classList.contains('num') ? ' class="num"' : '') + '>' + cellHTML(def, c, r) + '</td>'; }).join('') + '</tr>';
  }).join('') : '<tr><td colspan="' + cols.length + '" class="dg-empty"><span class="why t-cm-label">No ' + def.noun + ' match these filters</span>' +
    '<span class="try t-cm-caption">Try removing a filter, or clear them all</span><button class="clearbtn t-cm-button" type="button" data-ftb-clear>Clear filters</button></td></tr>';
  document.getElementById(gid + '-count').textContent = rows.length + ' ' + (rows.length === 1 ? def.one : def.noun);
  document.getElementById(gid + '-range').textContent = rows.length ? ((page - 1) * pp + 1) + '–' + Math.min(page * pp, rows.length) + ' of ' + rows.length : '0 of 0';
  var sel = document.getElementById(gid + '-pp'); sel.value = String(pp);
  var ul = root.querySelector('[data-pager]'), h = '', lo = Math.max(1, Math.min(page - 3, pages - 6)), hi = Math.min(pages, lo + 6);
  h += '<li><button class="pbtn" type="button" aria-label="Previous page" ' + (page === 1 ? 'disabled' : '') + ' data-go="prev" data-grid-go="' + gid + '"><svg viewBox="0 0 18 18" aria-hidden="true"><use href="#dg-cleft"/></svg></button></li>';
  for (var p = lo; p <= hi; p++) { var cur = p === page;
    h += '<li><button class="pbtn ' + (cur ? 't-cm-button' : 't-cm-label') + '" type="button" data-go="' + p + '" data-grid-go="' + gid + '" ' +
      (cur ? 'aria-current="page" aria-label="Page ' + p + ', current page"' : 'aria-label="Page ' + p + '"') + '>' + p + '</button></li>'; }
  h += '<li><button class="pbtn" type="button" aria-label="Next page" ' + (page === pages ? 'disabled' : '') + ' data-go="next" data-grid-go="' + gid + '"><svg viewBox="0 0 18 18" aria-hidden="true"><use href="#dg-cright"/></svg></button></li>';
  ul.innerHTML = h;
  return rows;
}
document.addEventListener('click', function (e) {
  var sb = e.target.closest && e.target.closest('.dg th button.sort');
  if (sb) { var gid = sb.closest('.dg').getAttribute('data-grid'), key = sb.getAttribute('data-sort'), cur = UI.sort[gid] || GRIDS[gid].defaultSort || {};
    UI.sort[gid] = { key: key, dir: cur.key === key && cur.dir === 'asc' ? 'desc' : 'asc' }; STATE.page[gid] = 1; persistUI(); renderGrid(gid);
    var again = document.querySelector('#dg-' + gid + ' th[data-key="' + key + '"] button.sort'); if (again) { again.focus(); } return; }
  var pg = e.target.closest && e.target.closest('button[data-grid-go]');
  if (pg && !pg.disabled) { var g = pg.getAttribute('data-grid-go'), go = pg.getAttribute('data-go');
    STATE.page[g] = go === 'prev' ? STATE.page[g] - 1 : go === 'next' ? STATE.page[g] + 1 : +go; renderGrid(g);
    var cp = document.querySelector('#dg-' + g + ' .pbtn[aria-current="page"]'); if (cp) { cp.focus(); } }
});
document.addEventListener('change', function (e) {
  var s = e.target.closest && e.target.closest('select[data-pp]'); if (!s) { return; }
  var gid = s.getAttribute('data-pp'); UI.pp[gid] = +s.value; STATE.page[gid] = 1; persistUI(); renderGrid(gid);
});
function csvOf(gid) {
  var def = GRIDS[gid], rows = gridRows(gid), cols = def.csv || Object.keys(rows[0] || {}).filter(function (k) { return typeof rows[0][k] !== 'object'; });
  return [cols.join(',')].concat(rows.map(function (r) { return cols.map(function (c) { var v = c === 'entity' ? entName(r[c]) : r[c];
    v = v == null ? '' : String(v); return /[",\n]/.test(v) ? '"' + v.replace(/"/g, '""') + '"' : v; }).join(','); })).join('\n');
}
function download(name, text) {
  var a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([text], { type: 'text/csv' })); a.download = name;
  document.body.appendChild(a); a.click(); setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 500);
}

/* ================================================================ tabs (Tabs snippet behaviour, per instance) */
function placeTabIndicator(tabs) {
  var s = tabs.querySelector('[role="tab"][aria-selected="true"]'), ind = tabs.querySelector('.indicator');
  if (!s || !ind || !s.offsetWidth) { return; } ind.style.opacity = '1'; ind.style.left = s.offsetLeft + 'px'; ind.style.width = s.offsetWidth + 'px';
}
function selectTab(tabs, key, focus) {
  var tid = tabs.getAttribute('data-tabs');
  tabs.querySelectorAll('[role="tab"]').forEach(function (t) { var on = t.getAttribute('data-tab') === key;
    t.setAttribute('aria-selected', String(on)); t.tabIndex = on ? 0 : -1; if (on && focus) { t.focus(); }
    document.getElementById(t.getAttribute('aria-controls')).hidden = !on; });
  UI.tab[tid] = key; persistUI(); placeTabIndicator(tabs); updateCount();
}
document.addEventListener('click', function (e) { var t = e.target.closest && e.target.closest('.tabs [role="tab"]');
  if (t) { selectTab(t.closest('.tabs'), t.getAttribute('data-tab')); syncHash(); } });
document.addEventListener('keydown', function (e) {
  var t = e.target.closest && e.target.closest('.tabs [role="tab"]'); if (!t) { return; }
  var all = [].slice.call(t.closest('.tablist').querySelectorAll('[role="tab"]')), i = all.indexOf(t), n = null;
  if (e.key === 'ArrowRight') { n = all[(i + 1) % all.length]; } else if (e.key === 'ArrowLeft') { n = all[(i - 1 + all.length) % all.length]; }
  else if (e.key === 'Home') { n = all[0]; } else if (e.key === 'End') { n = all[all.length - 1]; }
  if (n) { e.preventDefault(); selectTab(t.closest('.tabs'), n.getAttribute('data-tab'), true); syncHash(); }
});

/* ================================================================ segmented indicator (Segmented-control JS, as the toolbar snippet carries it) */
function moveInd(seg) { var ind = seg.querySelector('.ind'); if (!ind) { return; }
  var a = seg.querySelector('button[aria-pressed="true"]'); if (!a || !a.offsetWidth) { return; }
  var sr = seg.getBoundingClientRect(), br = a.getBoundingClientRect();
  ind.style.left = (br.left - sr.left - seg.clientLeft) + 'px'; ind.style.width = br.width + 'px'; }
function placeAll() { document.querySelectorAll('.seg').forEach(moveInd); document.querySelectorAll('.tabs').forEach(placeTabIndicator); }
document.addEventListener('click', function (e) { var b = e.target.closest && e.target.closest('.seg button'); if (!b) { return; }
  var seg = b.closest('.seg'); if (seg.closest('figure.dv')) { return; }                /* chart segs belong to dv-behaviour */
  seg.querySelectorAll('button').forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); }); moveInd(seg); });
var _raf = 0; addEventListener('resize', function () { if (_raf) { cancelAnimationFrame(_raf); } _raf = requestAnimationFrame(function () { _raf = 0; placeAll(); }); });

/* ================================================================ dropdowns (Dropdown JS as carried by Filter-toolbar-bar, with the documented choose hook) */
function wireDD(dd, onChoose) {
  var trig = dd.querySelector('.trigger'), menu = dd.querySelector('.menu'), val = dd.querySelector('.ddval');
  function opts() { return [].slice.call(menu.querySelectorAll('[role=option]')); }
  function open(o) { menu.setAttribute('data-open', String(o)); trig.setAttribute('aria-expanded', String(o));
    if (o) { var os = opts(), sel = os.filter(function (x) { return x.getAttribute('aria-selected') === 'true'; })[0] || os[0]; if (sel) { sel.focus(); } } }
  function choose(o) {
    if (onChoose && onChoose(o, val) === false) { open(false); trig.focus(); return; }
    opts().forEach(function (x) { x.setAttribute('aria-selected', String(x === o)); }); val.textContent = o.textContent.trim(); open(false); trig.focus(); }
  trig.addEventListener('click', function () { open(menu.getAttribute('data-open') !== 'true'); });
  trig.addEventListener('keydown', function (e) { if (['ArrowDown', 'Enter', ' '].indexOf(e.key) >= 0) { e.preventDefault(); open(true); } });
  menu.addEventListener('click', function (e) { var o = e.target.closest('[role=option]'); if (o) { choose(o); } });
  menu.addEventListener('keydown', function (e) { var os = opts(), o = e.target.closest('[role=option]'), i = os.indexOf(o); if (!o) { return; }
    if (e.key === 'ArrowDown') { e.preventDefault(); os[(i + 1) % os.length].focus(); }
    else if (e.key === 'ArrowUp') { e.preventDefault(); os[(i - 1 + os.length) % os.length].focus(); }
    else if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); choose(o); }
    else if (e.key === 'Escape') { open(false); trig.focus(); } });
  dd.__set = function (value) { opts().forEach(function (x) { var on = x.getAttribute('data-value') === String(value);
    x.setAttribute('aria-selected', String(on)); if (on) { val.textContent = x.textContent.trim(); } }); };
}
document.addEventListener('click', function (e) { if (!e.target.closest('.dd')) {
  document.querySelectorAll('.dd').forEach(function (dd) { var m = dd.querySelector('.menu'), t = dd.querySelector('.trigger');
    if (m && t) { m.setAttribute('data-open', 'false'); t.setAttribute('aria-expanded', 'false'); } }); } });
var TICK = '<svg data-bespoke="neutral selection checkmark (library only has teal status ticks)" class="tick" viewBox="0 0 18 18" aria-hidden="true"><path d="M3.5 9.5 L7.5 13.5 L14.5 5"/></svg>';

/* ================================================================ drawer (Drawer snippet mechanics: show · two frames · focus in · THEN inert) */
var shellRoot = document.querySelector('.ceo-shell');
var DRAWER = { el: document.getElementById('drawer'), scrim: document.getElementById('drawer-scrim'), opener: null, onClose: null };
function drawerFocusables() { return [].slice.call(DRAWER.el.querySelectorAll('button,a[href],input,textarea,select,[tabindex]:not([tabindex="-1"])')).filter(function (x) { return !x.disabled && x.offsetParent !== null; }); }
function openDrawer(title, bodyHTML, actions, onClose) {
  var ae = document.activeElement;
  DRAWER.opener = DRAWER.opener || (ae && ae !== document.body && !ae.closest('#overlay, #drawer') ? ae : null); DRAWER.onClose = onClose || null;
  document.getElementById('drawer-title').textContent = title;
  document.getElementById('drawer-body').innerHTML = bodyHTML;
  document.getElementById('drawer-foot').innerHTML = (actions || []).map(function (a, i) {
    return '<button class="dbtn ' + (a.kind || (i === 0 ? 'primary' : 'secondary')) + ' t-cm-button t-cm-slot" type="button" data-drawer-act="' + i + '">' + esc(a.label) + '</button>'; }).join('');
  DRAWER.actions = actions || [];
  var wasOpen = DRAWER.el.classList.contains('open');
  DRAWER.scrim.classList.add('open'); DRAWER.el.classList.add('open');
  /* the snippet's order — show · wait until the sheet's transitioned visibility has landed · focus in ·
     only then inert — with the wait polled per frame instead of a fixed two frames (driven: after a
     hashchange two frames were not enough and focus fell to <body>) */
  whenVisible(DRAWER.el, function () {
    if (!wasOpen) { var f = drawerFocusables(); if (f.length) { f[0].focus(); } }
    shellRoot.inert = true; shellRoot.setAttribute('aria-hidden', 'true'); });
}
function whenVisible(el, fn, n) {
  n = n || 0;
  requestAnimationFrame(function () { if (getComputedStyle(el).visibility === 'visible' || n > 30) { fn(); } else { whenVisible(el, fn, n + 1); } });
}
function isShown(el) { return !!el && el !== document.body && document.body.contains(el) && el.getClientRects().length > 0 && getComputedStyle(el).visibility !== 'hidden' && !el.closest('[inert]'); }
function closeDrawer(silent, keepOpener) {
  if (!DRAWER.el.classList.contains('open')) { if (!keepOpener) { DRAWER.opener = null; } return; }
  DRAWER.scrim.classList.remove('open'); DRAWER.el.classList.remove('open');
  shellRoot.inert = false; shellRoot.removeAttribute('aria-hidden');
  var rec = STATE.record ? '#/' + STATE.view + '/' + encodeURIComponent(STATE.record) : null;
  var cb = DRAWER.onClose; DRAWER.onClose = null; if (cb && !silent) { cb(); }
  var o = DRAWER.opener; if (!keepOpener) { DRAWER.opener = null; }
  /* the opener may have been re-rendered while the drawer was open (a decision re-draws the grid):
     fall back to the same record's link as it now exists, then to the main region */
  if (!isShown(o) && rec) { o = document.querySelector('.ceo-view:not([hidden]) a[href="' + rec + '"]'); }
  var target = isShown(o) ? o : document.getElementById('main-app');
  /* driven: a focus() in the same task as `inert = false` is dropped (the page is still inert to it),
     so the return lands on the next frame */
  requestAnimationFrame(function () { if (!MODAL.ov.classList.contains('open') && !DRAWER.el.classList.contains('open')) { target.focus(); } });
}
document.getElementById('drawer-close').addEventListener('click', function () { closeDrawer(); });
DRAWER.scrim.addEventListener('click', function () { closeDrawer(); });
DRAWER.el.addEventListener('click', function (e) { var b = e.target.closest('[data-drawer-act]'); if (!b) { return; }
  var a = DRAWER.actions[+b.getAttribute('data-drawer-act')]; if (a && a.run) { a.run(b); } else { closeDrawer(); } });

/* ================================================================ modal dialog (the spliced Modals overlay; content set per use) */
var MODAL = { ov: document.getElementById('overlay'), opener: null, onConfirm: null };
var mTitle = document.getElementById('dtitle'), mBody = document.getElementById('dbody'), mConfirm = document.getElementById('confirm'),
    mCancel = document.getElementById('cancel'), mClose = document.getElementById('close');
var mForm = document.createElement('div'); mForm.className = 'ceo-modal-form'; mForm.id = 'modal-form';
mBody.parentNode.insertBefore(mForm, mBody.nextSibling);
function modalFocusables() { return [].slice.call(MODAL.ov.querySelectorAll('button,a[href],input,textarea,[tabindex]:not([tabindex="-1"])')).filter(function (x) { return !x.disabled && x.offsetParent !== null; }); }
function openModal(o) {
  /* one modal surface at a time (drawer meta mustNotNeighbour): the drawer steps aside while the
     dialog is up and comes back, re-read, when the dialog closes */
  MODAL.reopen = null;
  if (DRAWER.el.classList.contains('open')) { var v = STATE.view, id = STATE.record; MODAL.reopen = function () { if (id) { openRecord(v, id); } }; closeDrawer(true, true); }
  MODAL.opener = document.activeElement; MODAL.onConfirm = o.onConfirm;
  mTitle.textContent = o.title; mBody.textContent = o.text || ''; mForm.innerHTML = o.form || ''; mForm.hidden = !o.form;
  mConfirm.textContent = o.confirm || 'Confirm'; mCancel.textContent = o.cancel || 'Cancel';
  MODAL.ov.classList.add('open');
  whenVisible(MODAL.ov, function () {
    var first = mForm.querySelector('input,textarea,button.trigger') || mConfirm; first.focus();
    shellRoot.inert = true; DRAWER.el.inert = true; });
  if (o.after) { o.after(mForm); }
}
function closeModal(confirmed) {
  MODAL.ov.classList.remove('open'); DRAWER.el.inert = false;
  var drawerOpen = DRAWER.el.classList.contains('open');
  if (!drawerOpen) { shellRoot.inert = false; }
  var o = MODAL.opener; MODAL.opener = null;
  if (drawerOpen) { var f = drawerFocusables(); if (f.length) { f[0].focus(); } }
  else if (o) { requestAnimationFrame(function () { if (isShown(o)) { o.focus(); } }); }
  if (!confirmed && MODAL.reopen && !drawerOpen) { MODAL.reopen(); }
  MODAL.reopen = null;
}
mConfirm.addEventListener('click', function () { if (!MODAL.onConfirm || MODAL.onConfirm(mForm) !== false) { closeModal(true); } });
mCancel.addEventListener('click', function () { closeModal(false); }); mClose.addEventListener('click', function () { closeModal(false); });
document.addEventListener('keydown', function (e) {
  if (MODAL.ov.classList.contains('open')) {
    if (e.key === 'Escape') { e.preventDefault(); closeModal(false); return; }
    if (e.key === 'Tab') { var f = modalFocusables(), a = f[0], z = f[f.length - 1];
      if (e.shiftKey && document.activeElement === a) { e.preventDefault(); z.focus(); } else if (!e.shiftKey && document.activeElement === z) { e.preventDefault(); a.focus(); } }
    return;
  }
  if (DRAWER.el.classList.contains('open')) {
    if (e.key === 'Escape') { closeDrawer(); return; }
    if (e.key === 'Tab') { var g = drawerFocusables(), b = g[0], y = g[g.length - 1];
      if (e.shiftKey && document.activeElement === b) { e.preventDefault(); y.focus(); } else if (!e.shiftKey && document.activeElement === y) { e.preventDefault(); b.focus(); } }
  }
});
/* form fields — Input-fields boxed field and Textarea markup, validated on confirm */
var FID = 0;
function textField(name, label, help, o) {
  o = o || {}; var id = 'f-' + name + '-' + (++FID);
  return '<div class="cn-input-fields"><div class="field" data-field="' + name + '"><div class="lbl"><label for="' + id + '">' + esc(label) + '</label></div>' +
    (help ? '<p class="help-text" id="' + id + '-help">' + esc(help) + '</p>' : '') +
    '<div class="box">' + (o.prefix ? '<span class="prefix" aria-hidden="true">' + esc(o.prefix) + '</span>' : '') +
    '<input id="' + id + '" name="' + name + '" type="text"' + (o.inputmode ? ' inputmode="' + o.inputmode + '"' : '') + ' value="' + esc(o.value || '') + '"' +
    (help ? ' aria-describedby="' + id + '-help"' : '') + '></div></div></div>';
}
function areaField(name, label, help, o) {
  o = o || {}; var id = 'f-' + name + '-' + (++FID), max = o.max || 500;
  return '<div class="cn-textarea"><div class="tx-group" data-field="' + name + '"><div class="tx-lblrow"><label class="t-cm-label" for="' + id + '">' + esc(label) + '</label></div>' +
    '<div class="tx-box"><textarea id="' + id + '" name="' + name + '" class="t-ed-body" maxlength="' + max + '" rows="4" aria-describedby="' + id + '-help ' + id + '-count">' + esc(o.value || '') + '</textarea></div>' +
    '<div class="tx-foot"><p class="tx-help t-ed-body-small" id="' + id + '-help">' + esc(help || '') + '</p><span class="tx-count t-cm-legal" id="' + id + '-count">0/' + max + '</span></div></div></div>';
}
function selectField(name, label, options, value) {
  var id = 'f-' + name + '-' + (++FID);
  return '<div class="cn-dropdown"><div class="dd boxed" data-field="' + name + '" data-value="' + esc(value || '') + '"><label id="' + id + 'L" for="' + id + 'T">' + esc(label) + '</label>' +
    '<button class="trigger" id="' + id + 'T" type="button" role="combobox" aria-haspopup="listbox" aria-expanded="false" aria-controls="' + id + 'M" aria-labelledby="' + id + 'L ' + id + 'T">' +
    '<span class="ddval">' + esc((options.filter(function (o) { return o[0] === value; })[0] || [0, 'Choose one'])[1]) + '</span><span class="chev" aria-hidden="true">▾</span></button>' +
    '<ul class="menu" id="' + id + 'M" role="listbox" aria-labelledby="' + id + 'L" tabindex="-1">' + options.map(function (o) {
      return '<li class="opt" role="option" aria-selected="' + (o[0] === value) + '" tabindex="-1" data-value="' + esc(o[0]) + '">' + esc(o[1]) + ' ' + TICK + '</li>'; }).join('') + '</ul></div></div>';
}
function wireForm(root) {
  root.querySelectorAll('.dd[data-field]').forEach(function (dd) { if (dd.__wired) { return; } dd.__wired = true;
    wireDD(dd, function (o) { dd.setAttribute('data-value', o.getAttribute('data-value')); clearError(dd); }); });
  root.querySelectorAll('.tx-group textarea').forEach(function (t) { var c = document.getElementById(t.id + '-count');
    var up = function () { c.textContent = t.value.length + '/' + t.maxLength; }; up(); t.addEventListener('input', function () { up(); clearError(t.closest('.tx-group')); }); });
  root.querySelectorAll('.field input').forEach(function (i) { i.addEventListener('input', function () { clearError(i.closest('.field')); }); });
}
function fieldVal(root, name) { var f = root.querySelector('[data-field="' + name + '"]'); if (!f) { return ''; }
  if (f.classList.contains('dd')) { return f.getAttribute('data-value') || ''; } var i = f.querySelector('input,textarea'); return i ? i.value.trim() : ''; }
function setError(root, name, msg) {
  var f = root.querySelector('[data-field="' + name + '"]'); if (!f) { return; } clearError(f);
  f.classList.add('is-error'); var ctl = f.querySelector('input,textarea,.trigger'); var eid = (ctl.id || name) + '-err';
  if (ctl) { ctl.setAttribute('aria-invalid', 'true'); ctl.setAttribute('aria-describedby', ((ctl.getAttribute('aria-describedby') || '') + ' ' + eid).trim()); }
  f.insertAdjacentHTML('beforeend', '<div class="err-msg" data-err><span class="ic" aria-hidden="true"><svg class="icn" viewBox="0 0 18 18"><use href="#ic-error"/></svg></span><p id="' + eid + '">' + esc(msg) + '</p></div>');
}
function clearError(f) { if (!f) { return; } f.classList.remove('is-error'); var e = f.querySelector('[data-err]'); if (e) { e.remove(); }
  var ctl = f.querySelector('[aria-invalid]'); if (ctl) { ctl.removeAttribute('aria-invalid'); } }
function focusFirstError(root) { var f = root.querySelector('.is-error input, .is-error textarea, .is-error .trigger'); if (f) { f.focus(); } }

/* ================================================================ toast (Toast snippet spawn, verbatim logic) */
var toastRegion = document.getElementById('toastRegion');
var RM = matchMedia('(prefers-reduced-motion: reduce)').matches;
function toast(status, msg) {
  var glyph = { ok: 'to-success', info: 'to-info', warn: 'to-warning' }[status], origin = document.activeElement;
  var t = document.createElement('div'); t.className = 'toast ' + status; t.setAttribute('role', 'status');
  if (glyph) { t.setAttribute('data-carries', 'symbol label'); }
  t.innerHTML = (glyph ? '<span class="ic"><svg aria-hidden="true"><use href="#' + glyph + '"/></svg></span>' : '') + '<p class="msg t-ed-body">' + esc(msg) + '</p>' +
    '<button class="x" type="button" aria-label="Dismiss message"><svg aria-hidden="true"><use href="#to-close"/></svg></button>';
  toastRegion.appendChild(t);
  var remain = 6000, started = Date.now(), timer = setTimeout(leave, remain), paused = false;
  function leave() { if (RM) { t.remove(); return; } t.classList.add('leaving'); t.addEventListener('transitionend', function () { t.remove(); }, { once: true }); setTimeout(function () { t.remove(); }, 400); }
  function pause() { if (paused) { return; } paused = true; clearTimeout(timer); remain -= Date.now() - started; }
  function resume() { if (!paused) { return; } paused = false; started = Date.now(); timer = setTimeout(leave, Math.max(remain, 1000)); }
  t.addEventListener('mouseenter', pause); t.addEventListener('mouseleave', resume); t.addEventListener('focusin', pause); t.addEventListener('focusout', resume);
  var self = t.querySelector('.x');
  self.addEventListener('click', function () { clearTimeout(timer); leave();
    var nxt = [].slice.call(toastRegion.querySelectorAll('.toast:not(.leaving) .x')).filter(function (b) { return b !== self; })[0];
    var home = nxt || origin; if (home && document.body.contains(home)) { home.focus(); } });
}

/* ================================================================ the shared filter toolbar (Filter-toolbar-bar markup, authored wiring) */
var FTB = document.getElementById('ftb'), ftbQ = document.getElementById('ftbQ');
var ddEntity = document.getElementById('ftbEntity'), ddRegion = document.getElementById('ftbRegion'), ddDays = document.getElementById('ftbDays');
ddEntity.querySelector('.menu').innerHTML = [['all', 'All entities']].concat(DATA.entities.map(function (e) { return [e.id, e.name]; })).map(function (o) {
  return '<li class="opt t-cm-label" role="option" aria-selected="false" tabindex="-1" data-value="' + o[0] + '">' + esc(o[1]) + ' ' + TICK + '</li>'; }).join('');
ddRegion.querySelector('.menu').innerHTML = [['all', 'All regions']].concat(DATA.regions.map(function (r) { return [r, r]; })).map(function (o) {
  return '<li class="opt t-cm-label" role="option" aria-selected="false" tabindex="-1" data-value="' + o[0] + '">' + esc(o[1]) + ' ' + TICK + '</li>'; }).join('');
wireDD(ddEntity, function (o) { STATE.entity = o.getAttribute('data-value');
  if (STATE.entity !== 'all' && STATE.region !== 'all' && ENT[STATE.entity].region !== STATE.region) { STATE.region = 'all'; }
  setTimeout(refilter, 0); });
wireDD(ddRegion, function (o) { STATE.region = o.getAttribute('data-value');
  if (STATE.entity !== 'all' && STATE.region !== 'all' && ENT[STATE.entity].region !== STATE.region) { STATE.entity = 'all'; }
  setTimeout(refilter, 0); });
wireDD(ddDays, function (o) { STATE.days = +o.getAttribute('data-value'); setTimeout(refilter, 0); });
wireDD(document.getElementById('ftbExport'), function (o) {
  var fmt = o.getAttribute('data-value'), gid = primaryGrid();
  if (fmt === 'csv') {
    if (!gid) { toast('info', 'This view has no records to export.'); return false; }
    download('northwind-' + STATE.view + '-' + gid + '-' + DATA.asAt + '.csv', csvOf(gid));
    toast('ok', 'Exported ' + gridRows(gid).length + ' ' + GRIDS[gid].noun + ' as CSV.');
  } else { window.print(); }
  return false;                                  /* an action menu does not latch a value */
});
var qTimer = 0;
ftbQ.addEventListener('input', function () { clearTimeout(qTimer); qTimer = setTimeout(function () { STATE.q = ftbQ.value.trim(); refilter(); }, 200); });
FTB.querySelector('.search .clear').addEventListener('click', function () { ftbQ.value = ''; STATE.q = ''; refilter(); ftbQ.focus(); });
document.getElementById('ftbTheme').addEventListener('click', function (e) { var b = e.target.closest('button[data-theme-set]'); if (b) { setTheme(b.getAttribute('data-theme-set')); } });
document.addEventListener('click', function (e) {
  if (e.target.closest && e.target.closest('[data-ftb-clear]')) { STATE.entity = 'all'; STATE.region = 'all'; STATE.days = 30; STATE.q = ''; STATE.status = null;
    ftbQ.value = ''; refilter(); ftbQ.focus(); return; }
  var x = e.target.closest && e.target.closest('#ftbChips button[data-chip]');
  if (x) { var k = x.getAttribute('data-chip');
    if (k === 'entity') { STATE.entity = 'all'; } else if (k === 'region') { STATE.region = 'all'; } else if (k === 'days') { STATE.days = 30; }
    else if (k === 'q') { STATE.q = ''; ftbQ.value = ''; } else if (k === 'status') { STATE.status = null; }
    refilter(); var nx = document.querySelector('#ftbChips button[data-chip]'); (nx || ftbQ).focus(); }
});
function chipHTML(key, label) {
  return '<span class="tag t-cm-caption"><span class="lbl">' + esc(label) + '</span><button class="x" type="button" data-chip="' + key + '" aria-label="Remove filter: ' + esc(label) + '">' +
    '<svg viewBox="0 0 18 18" aria-hidden="true"><use href="#ic-close"/></svg></button></span>';
}
function syncToolbar() {
  ddEntity.__set(STATE.entity); ddRegion.__set(STATE.region); ddDays.__set(STATE.days);
  if (ftbQ.value.trim() !== STATE.q) { ftbQ.value = STATE.q; }
  var chips = [];
  if (STATE.entity !== 'all') { chips.push(chipHTML('entity', 'Entity: ' + entName(STATE.entity))); }
  if (STATE.region !== 'all') { chips.push(chipHTML('region', 'Region: ' + STATE.region)); }
  if (STATE.days !== 30) { chips.push(chipHTML('days', 'Date: last ' + STATE.days + ' days')); }
  if (STATE.status) { chips.push(chipHTML('status', 'Status: ' + STATE.status)); }
  if (STATE.q) { chips.push(chipHTML('q', 'Search: ' + STATE.q)); }
  document.querySelector('#ftbChips .row').innerHTML = chips.join('');
  FTB.setAttribute('data-ftb-state', chips.length ? 'filtered' : 'no-filters');
  updateCount();
}
function primaryGrid() {
  var sec = document.querySelector('.ceo-view[data-view="' + STATE.view + '"]'); if (!sec) { return null; }
  var vis = [].slice.call(sec.querySelectorAll('.dg[data-grid]')).filter(function (g) { return !g.closest('[role="tabpanel"][hidden]'); })[0];
  return vis ? vis.getAttribute('data-grid') : null;
}
function updateCount() {
  var gid = primaryGrid(), n = 0, t = 0, noun = 'records';
  if (gid && GRIDS[gid]) { n = GRIDS[gid].rows().length; t = GRIDS[gid].all().length; noun = GRIDS[gid].noun; }
  document.getElementById('ftbCount').textContent = n; document.getElementById('ftbTotal').textContent = t; document.getElementById('ftbNoun').textContent = noun;
  if (gid && n === 0 && FTB.getAttribute('data-ftb-state') !== 'no-filters') { FTB.setAttribute('data-ftb-state', 'empty'); }
}
function refilter() { Object.keys(STATE.page).forEach(function (k) { STATE.page[k] = 1; }); renderView(); syncToolbar(); syncHash(); }

/* ================================================================ theme (both modes; the attribute lives on <html>) */
function setTheme(t) {
  document.documentElement.setAttribute('data-theme', t); save('ceo.theme', t); try { localStorage.setItem('ceo.theme', t); } catch (e) {}
  document.querySelectorAll('[data-theme-set]').forEach(function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-theme-set') === t)); });
  requestAnimationFrame(placeAll);
}

/* ================================================================ router — #/<view>[/<record>]?entity=&region=&days=&q=&status=&tab= */
function parseHash() {
  var h = location.hash.replace(/^#\/?/, ''), qi = h.indexOf('?'), path = qi >= 0 ? h.slice(0, qi) : h, qs = qi >= 0 ? h.slice(qi + 1) : '';
  var parts = path.split('/').map(function (x) { return decodeURIComponent(x); }), p = {};
  qs.split('&').forEach(function (kv) { if (!kv) { return; } var i = kv.indexOf('='); p[decodeURIComponent(kv.slice(0, i))] = decodeURIComponent(kv.slice(i + 1).replace(/\+/g, ' ')); });
  return { view: parts[0] || 'overview', record: parts[1] || null, p: p };
}
function hashFor(view, record) {
  var q = [];
  if (STATE.entity !== 'all') { q.push('entity=' + encodeURIComponent(STATE.entity)); }
  if (STATE.region !== 'all') { q.push('region=' + encodeURIComponent(STATE.region)); }
  if (STATE.days !== 30) { q.push('days=' + STATE.days); }
  if (STATE.q) { q.push('q=' + encodeURIComponent(STATE.q)); }
  if (STATE.status) { q.push('status=' + encodeURIComponent(STATE.status)); }
  var sec = document.querySelector('.ceo-view[data-view="' + view + '"] .tabs');
  if (sec) { var t = UI.tab[sec.getAttribute('data-tabs')]; if (t) { q.push('tab=' + t); } }
  return '#/' + view + (record ? '/' + encodeURIComponent(record) : '') + (q.length ? '?' + q.join('&') : '');
}
function syncHash() { var h = hashFor(STATE.view, STATE.record); if (location.hash !== h) { history.replaceState(null, '', h); } persistUI(); }
function onRoute() {
  var r = parseHash(), p = r.p;
  if (VIEWS.indexOf(r.view) < 0) { r.view = 'overview'; r.record = null; }
  if (p.entity && (p.entity === 'all' || ENT[p.entity])) { STATE.entity = p.entity; }
  if (p.region && (p.region === 'all' || DATA.regions.indexOf(p.region) >= 0)) { STATE.region = p.region; }
  if (p.days && [7, 14, 30].indexOf(+p.days) >= 0) { STATE.days = +p.days; }
  if ('q' in p) { STATE.q = p.q; }
  STATE.status = p.status || null;
  var changed = STATE.view !== r.view; STATE.view = r.view; STATE.record = r.record;
  showView(r.view, p.tab);
  renderView(); syncToolbar();
  if (r.record) { openRecord(r.view, r.record); } else { closeDrawer(true); }
  syncHash();
  if (changed && !r.record) { document.getElementById('main-app').focus({ preventScroll: true }); document.getElementById('sh-content').scrollTop = 0; }
}
function showView(v, tab) {
  document.querySelectorAll('.ceo-view').forEach(function (s) { s.hidden = s.getAttribute('data-view') !== v; });
  var sec = document.querySelector('.ceo-view[data-view="' + v + '"]');
  document.getElementById('page-h1').textContent = TITLES[v].title; document.getElementById('page-h1').id = 'page-h1';
  sec.setAttribute('aria-labelledby', 'page-h1');
  document.getElementById('page-lede').textContent = TITLES[v].lede;
  document.getElementById('crumb-here').textContent = TITLES[v].title;
  document.title = TITLES[v].title + ' — Northwind Group — CEO banking (prototype)';
  document.querySelectorAll('.sn-link[data-nav]').forEach(function (a) { if (a.getAttribute('data-nav') === v) { a.setAttribute('aria-current', 'page'); } else { a.removeAttribute('aria-current'); } });
  sec.querySelectorAll('.tabs').forEach(function (t) { var tid = t.getAttribute('data-tabs'), key = tab && t.querySelector('[data-tab="' + tab + '"]') ? tab : UI.tab[tid];
    if (key && t.querySelector('[data-tab="' + key + '"]')) { selectTab(t, key); } });
  requestAnimationFrame(placeAll);
}
function renderView() { var f = RENDER[STATE.view]; if (f) { f(); } }
function go(hash) { location.hash = hash; }
window.addEventListener('hashchange', onRoute);
document.addEventListener('click', function (e) {
  var a = e.target.closest && e.target.closest('[data-act]'); if (!a) { return; }
  if (a.getAttribute('data-act') === 'focus-search') { ftbQ.focus(); }
  if (a.getAttribute('data-act') === 'go-settings') { go('#/settings'); }
});
var RENDER = {}, RECORD = {};
function openRecord(view, id) { var f = RECORD[view]; if (f) { if (!f(id)) { toast('warn', 'Record ' + id + ' is not in this prototype.'); STATE.record = null; syncHash(); } } }
function recordClosed() { STATE.record = null; syncHash(); }
function dl(pairs) { return '<div class="cn-summary"><dl class="summary">' + pairs.map(function (p) {
  return '<div class="summary__row"><dt class="summary__k">' + esc(p[0]) + '</dt><dd class="summary__v">' + (p[2] ? p[1] : esc(p[1])) + '</dd></div>'; }).join('') + '</dl></div>'; }
function auditHTML(list) { if (!list || !list.length) { return '<p class="t-ed-body-small">No audit entries yet.</p>'; }
  return '<div class="cn-summary"><dl class="summary">' + list.map(function (a) { return '<div class="summary__row"><dt class="summary__k">' + esc(fmtDate(a.at)) + ' · ' + esc(a.who) +
    '</dt><dd class="summary__v">' + esc(a.note) + '</dd></div>'; }).join('') + '</dl></div>'; }
function para(t) { return '<p class="t-ed-body">' + esc(t) + '</p>'; }
function head4(t) { return '<p class="t-cm-label">' + esc(t) + '</p>'; }
/* the drawer sits outside the dashboard scope, so its status carrier is Status-indicator's own `.stat` */
function stat(text) { return '<span class="cn-status-indicator"><span class="stat ' + ({ ok: 'ok', warn: 'warn', err: 'err', inf: 'inf' }[STATUS_CLASS[text]] || 'inf') +
  '" data-carries="label"><span class="dot" aria-hidden="true"></span><span>' + esc(text) + '</span></span></span>'; }
function per() { return 'vs ' + shortDate(SERIES_DAYS[30 - STATE.days]); }
function r1(v) { return Math.round(v * 10) / 10; }
function days() { return periodIdx().map(shortDate); }
var CCY5 = ['USD', 'EUR', 'GBP', 'CNY'];
function ccyBucket(c) { return CCY5.indexOf(c) >= 0 ? c : 'Other'; }

/* ================================================================ OVERVIEW — three questions */
RENDER.overview = function () {
  var cash = sliceSeries(cashSeries(scopedAccounts())), L = liquiditySeries(), liq = sliceSeries(L.total), need = plannedNeed();
  var outTx = DATA.transactions.filter(function (t) { return inScope(t, 'date') && t.gbp < 0; });
  var dailyOut = Math.max(sum(outTx, function (t) { return -t.gbp / 1e6; }) / STATE.days, 0.1);
  kpi('ov-cash', { unit: '£', value: grp3(cash[cash.length - 1], 1) + 'm', delta: deltaPct(cash[cash.length - 1], cash[0]),
    deltaText: deltaText(deltaPct(cash[cash.length - 1], cash[0])), per: per(), series: cash, href: '#/accounts' });
  kpi('ov-liq', { unit: '£', value: grp3(liq[liq.length - 1], 1) + 'm', delta: deltaPct(liq[liq.length - 1], liq[0]),
    deltaText: deltaText(deltaPct(liq[liq.length - 1], liq[0])), per: per(), series: liq, href: '#/liquidity' });
  var head = liq.map(function (v) { return v - need; });
  kpi('ov-head', { unit: head[head.length - 1] < 0 ? '−£' : '£', value: grp3(Math.abs(head[head.length - 1]), 1) + 'm', delta: deltaPct(head[head.length - 1], head[0]),
    deltaText: deltaText(deltaPct(head[head.length - 1], head[0])), per: per(), series: head, href: '#/liquidity' });
  var run = liq.map(function (v) { return v / dailyOut; });
  kpi('ov-runway', { unit: '', value: grp3(run[run.length - 1], 0) + ' days', delta: deltaPct(run[run.length - 1], run[0]),
    deltaText: deltaText(deltaPct(run[run.length - 1], run[0])), per: '£' + grp3(dailyOut, 1) + 'm out a day', series: run, href: '#/liquidity' });

  var pos = DATA.positions.filter(function (p) { return inScope(p); }), regs = DATA.regions.filter(function (r) { return STATE.region === 'all' || r === STATE.region; });
  regs = regs.filter(function (r) { return pos.some(function (p) { return p.region === r; }); });
  var buckets = CCY5.concat(['Other']);
  if (regs.length) {
    chart('ov-exposure', { type: 'stacked-column', categories: regs, categoryLabel: 'Region', unit: '£m',
      series: buckets.map(function (b) { return { name: b, values: regs.map(function (r) { return r1(sum(pos.filter(function (p) { return p.region === r && ccyBucket(p.ccy) === b; }), function (p) { return p.gbp; })); }) }; }),
      caption: 'Exposure by region, split by currency, GBP millions' },
      { title: 'Exposure by region and currency — select a region to see its positions', drill: 'region' });
  }
  var pend = DATA.payments.filter(function (p) { return inScope(p) && p.status === 'Pending approval'; }).sort(function (a, b) { return b.gbp - a.gbp; });
  summary('ov-approvals', { k: 'Awaiting your approval', sub: pend.length + ' payments · ' + pend.filter(function (p) { return p.gbp >= 5e6; }).length + ' of £5m or more',
    v: gbpM(sum(pend, function (p) { return p.gbp / 1e6; })) }, pend.slice(0, 3).map(function (p) {
    return { label: p.id + ' · ' + gbpM(p.gbp / 1e6) + ' to ' + p.beneficiary, href: '#/payments/' + p.id, status: 'Value date ' + shortDate(p.valueDate) }; }));
  var exc = DATA.exceptions.filter(function (x) { return inScope(x) && x.status === 'Open' && x.severity === 'Material'; });
  summary('ov-exceptions', { k: 'Open material exceptions', sub: DATA.exceptions.filter(function (x) { return inScope(x) && x.status === 'Open'; }).length + ' open in total', v: String(exc.length) },
    exc.slice(0, 3).map(function (x) { return { label: x.title, href: '#/risk/' + x.id, status: x.severity }; }));

  chart('ov-liqtrend', { type: 'stacked-area', categories: days(), categoryLabel: 'Day', unit: '£m',
    series: [{ name: 'Cash', values: sliceSeries(L.cash).map(r1) }, { name: 'Undrawn committed facilities', values: sliceSeries(L.undrawn).map(r1) },
             { name: 'Money market funds', values: sliceSeries(L.mmf).map(r1) }],
    caption: 'Available liquidity by source, daily, GBP millions' }, { title: 'Available liquidity by source, last ' + STATE.days + ' days' });
  var byC = buckets.map(function (b) { return r1(sum(pos.filter(function (p) { return ccyBucket(p.ccy) === b; }), function (p) { return p.gbp; })); });
  chart('ov-ccy', { type: 'donut', categories: buckets.filter(function (b, i) { return byC[i] > 0; }), categoryLabel: 'Currency', unit: '£m',
    series: [{ name: 'Exposure', values: byC.filter(function (v) { return v > 0; }) }], caption: 'Exposure by currency, GBP millions' },
    { title: 'Share of exposure by currency' });
};
/* drill-through: a stacked column's region opens Risk and limits on that region's positions */
function drillFrom(el) {
  var fig = el.closest('figure.dv[data-drill]'); if (!fig) { return false; }
  var lab = el.getAttribute('data-tip') || el.getAttribute('aria-label') || '';
  var reg = DATA.regions.filter(function (r) { return lab.indexOf(r) === 0 || lab.indexOf(r + ' ') >= 0 || lab.indexOf(r + ',') >= 0 || lab.indexOf(r + ':') >= 0; })[0];
  if (!reg) { return false; }
  STATE.region = reg; if (STATE.entity !== 'all' && ENT[STATE.entity].region !== reg) { STATE.entity = 'all'; }
  UI.tab['rk-tabs'] = 'positions'; persistUI(); go(hashFor('risk'));
  return true;
}
document.addEventListener('click', function (e) { var m = e.target.closest && e.target.closest('figure.dv[data-drill] .dv-series'); if (m) { drillFrom(m); } });
document.addEventListener('keydown', function (e) { if (e.key !== 'Enter') { return; } var m = e.target.closest && e.target.closest('figure.dv[data-drill] .dv-series'); if (m) { drillFrom(m); } });

/* ================================================================ ACCOUNTS AND TRANSACTIONS */
grid('tx', { view: 'accounts', noun: 'transactions', one: 'transaction', defaultSort: { key: 'date', dir: 'desc' },
  all: function () { return DATA.transactions; },
  rows: function () { return DATA.transactions.filter(function (t) { return inScope(t, 'date') && matchesQ(t, ['id', 'counterparty', 'type', 'entity', 'ccy', 'account']); }); },
  cell: { date: function (r) { return '<span class="t-cm-label">' + fmtDate(r.date) + '</span>'; },
          amount: function (r) { return '<span class="t-cm-figure-5">' + grp3(r.amount, 0) + '</span>'; },
          gbp: function (r) { return '<span class="t-cm-figure-5">' + gbpM(r.gbp / 1e6, 2) + '</span>'; } },
  csv: ['id', 'date', 'entity', 'account', 'counterparty', 'type', 'ccy', 'amount', 'gbp', 'status'] });
grid('acc', { view: 'accounts', noun: 'accounts', one: 'account', defaultSort: { key: 'gbp', dir: 'desc' },
  all: function () { return DATA.accounts; },
  rows: function () { return DATA.accounts.map(function (a) { a.gbp = toGBP(a.balance, a.ccy); return a; }).filter(function (a) { return inScope(a) && matchesQ(a, ['id', 'name', 'entity', 'ccy', 'region']); }); },
  cell: { balance: function (r) { return '<span class="t-cm-figure-5">' + grp3(r.balance, 0) + '</span>'; },
          gbp: function (r) { return '<span class="t-cm-figure-5">' + gbpM(r.gbp / 1e6, 1) + '</span>'; } },
  csv: ['id', 'name', 'entity', 'region', 'ccy', 'balance', 'gbp'] });
RENDER.accounts = function () {
  var acc = scopedAccounts(), cash = sliceSeries(cashSeries(acc)), tx = DATA.transactions.filter(function (t) { return inScope(t, 'date'); });
  var pd = periodIdx(), inD = pd.map(function (d) { return sum(tx.filter(function (t) { return t.date === d && t.gbp > 0; }), function (t) { return t.gbp / 1e6; }); });
  var outD = pd.map(function (d) { return sum(tx.filter(function (t) { return t.date === d && t.gbp < 0; }), function (t) { return -t.gbp / 1e6; }); });
  var cnt = pd.map(function (d) { return tx.filter(function (t) { return t.date === d; }).length; });
  var half = Math.floor(pd.length / 2);
  function halves(a) { return deltaPct(sum(a.slice(half)), sum(a.slice(0, half))); }
  kpi('ac-bal', { unit: '£', value: grp3(cash[cash.length - 1], 1) + 'm', delta: deltaPct(cash[cash.length - 1], cash[0]), deltaText: deltaText(deltaPct(cash[cash.length - 1], cash[0])), per: per(), series: cash, href: '#/accounts?tab=acc' });
  kpi('ac-in', { unit: '£', value: grp3(sum(inD), 1) + 'm', delta: halves(inD), deltaText: deltaText(halves(inD)), per: 'second half vs first', series: inD, href: '#/accounts?tab=tx' });
  kpi('ac-out', { unit: '£', value: grp3(sum(outD), 1) + 'm', delta: halves(outD), deltaText: deltaText(halves(outD)), per: 'second half vs first', series: outD, href: '#/accounts?tab=tx' });
  kpi('ac-count', { unit: '', value: grp3(sum(cnt), 0), delta: halves(cnt), deltaText: deltaText(halves(cnt)), per: 'second half vs first', series: cnt, href: '#/accounts?tab=tx' });
  var regs = DATA.regions.filter(function (r) { return acc.some(function (a) { return a.region === r; }); });
  if (regs.length) {
    chart('ac-trend', { type: 'multiline', categories: days(), categoryLabel: 'Day', unit: '£m', caption: 'Closing cash by region, daily, GBP millions',
      series: regs.map(function (r) { return { name: r, values: sliceSeries(cashSeries(acc.filter(function (a) { return a.region === r; }))).map(r1) }; }) },
      { title: 'Closing cash by region, last ' + STATE.days + ' days' });
  }
  var ents = scopedEntities().filter(function (e) { return acc.some(function (a) { return a.entity === e.id; }); });
  if (ents.length) {
    chart('ac-entity', { type: 'bar', categories: ents.map(function (e) { return e.name.replace(/^Northwind /, ''); }), categoryLabel: 'Entity', unit: '£m',
      series: [{ name: 'Cash', values: ents.map(function (e) { return r1(sum(acc.filter(function (a) { return a.entity === e.id; }), function (a) { return toGBP(a.balance, a.ccy) / 1e6; })); }) }],
      caption: 'Cash by entity today, GBP millions' }, { title: 'Cash by entity today' });
  }
  var BINS = [[0, 0.1, 'Under £0.1m'], [0.1, 0.5, '£0.1m–0.5m'], [0.5, 1, '£0.5m–1m'], [1, 2.5, '£1m–2.5m'], [2.5, 5, '£2.5m–5m'], [5, 10, '£5m–10m'], [10, 1e9, '£10m and over']];
  chart('ac-hist', { type: 'histogram', categories: BINS.map(function (b) { return b[2]; }), categoryLabel: 'Transaction size',
    series: [{ name: 'Transactions', values: BINS.map(function (b) { return tx.filter(function (t) { var m = Math.abs(t.gbp) / 1e6; return m >= b[0] && m < b[1]; }).length; }) }],
    caption: 'Transactions by size band, GBP equivalent' }, { title: 'How large transactions are, last ' + STATE.days + ' days' });
  var ccys = ['GBP', 'EUR', 'USD', 'SGD', 'HKD', 'AED'].filter(function (c) { return tx.some(function (t) { return t.ccy === c; }); });
  if (ccys.length) {
    chart('ac-ccyflow', { type: 'grouped-column', categories: ccys, categoryLabel: 'Currency', unit: '£m', caption: 'Money in and money out by currency, GBP millions',
      series: [{ name: 'Money in', values: ccys.map(function (c) { return r1(sum(tx.filter(function (t) { return t.ccy === c && t.gbp > 0; }), function (t) { return t.gbp / 1e6; })); }) },
               { name: 'Money out', values: ccys.map(function (c) { return r1(sum(tx.filter(function (t) { return t.ccy === c && t.gbp < 0; }), function (t) { return -t.gbp / 1e6; })); }) }] },
      { title: 'Money in and out by currency' });
  }
  renderGrid('tx'); renderGrid('acc');
};
RECORD.accounts = function (id) {
  var t = DATA.transactions.filter(function (x) { return x.id === id; })[0], a = DATA.accounts.filter(function (x) { return x.id === id; })[0];
  if (t) {
    openDrawer('Transaction ' + t.id, dl([['Date', fmtDate(t.date)], ['Entity', entName(t.entity)], ['Account', t.account], ['Counterparty', t.counterparty],
      ['Type', t.type], ['Amount', money(t.amount, t.ccy)], ['GBP equivalent', gbpM(t.gbp / 1e6, 2) + ' at ' + DATA.fx[t.ccy] + ' ' + t.ccy + ' per GBP (illustrative)'],
      ['Status', stat(t.status), true]]) + para('Figures are simulated for the prototype.'),
      [{ label: 'Download as CSV', run: function () { download(t.id + '.csv', 'field,value\n' + Object.keys(t).map(function (k) { return k + ',' + t[k]; }).join('\n')); toast('ok', 'Downloaded ' + t.id + ' as CSV.'); } },
       { label: 'Raise an investigation', kind: 'secondary', run: function () { closeDrawer(true); raiseRequest('Payment investigation', t.entity, 'Query on ' + t.id + ' — ' + t.counterparty); } }], recordClosed);
    return true;
  }
  if (a) {
    var s = a.series;
    openDrawer(a.name + ' ' + a.id, dl([['Entity', entName(a.entity)], ['Region', a.region], ['Currency', a.ccy], ['Account', a.iban],
      ['Balance today', money(a.balance, a.ccy)], ['GBP equivalent', gbpM(toGBP(a.balance, a.ccy) / 1e6, 2)], ['30 days ago', money(s[0], a.ccy)],
      ['Change', pct(deltaPct(s[29], s[0]))]]) + para('Opening and closing balances are simulated.'),
      [{ label: 'Show transactions', run: function () { closeDrawer(true); STATE.q = a.id; ftbQ.value = a.id; UI.tab['ac-tabs'] = 'tx'; go(hashFor('accounts')); } },
       { label: 'Close', kind: 'secondary' }], recordClosed);
    return true;
  }
  return false;
};

/* ================================================================ LIQUIDITY AND FUNDING */
grid('fac', { view: 'liquidity', noun: 'facilities', one: 'facility', defaultSort: { key: 'util', dir: 'desc' },
  all: function () { return DATA.facilities; },
  rows: function () { return DATA.facilities.map(function (f) { f.util = Math.round(f.drawn / f.limit * 1000) / 10; return f; })
    .filter(function (f) { return inScope(f) && matchesQ(f, ['id', 'name', 'entity', 'type']); }); },
  cell: { util: function (r) { return '<span class="t-cm-figure-5">' + pct(r.util) + '</span>'; }, maturity: function (r) { return '<span class="t-cm-label">' + fmtDate(r.maturity) + '</span>'; },
          limit: function (r) { return '<span class="t-cm-figure-5">' + grp3(r.limit, 0) + '</span>'; }, drawn: function (r) { return '<span class="t-cm-figure-5">' + grp3(r.drawn, 1) + '</span>'; } },
  csv: ['id', 'name', 'entity', 'type', 'limit', 'drawn', 'util', 'maturity', 'internalLimit'] });
RENDER.liquidity = function () {
  var L = liquiditySeries(), liq = sliceSeries(L.total), fs = scopedFacilities(), und = undrawnCommitted(fs), need = plannedNeed();
  kpi('lq-liq', { unit: '£', value: grp3(liq[liq.length - 1], 1) + 'm', delta: deltaPct(liq[liq.length - 1], liq[0]), deltaText: deltaText(deltaPct(liq[liq.length - 1], liq[0])), per: per(), series: liq, href: '#/liquidity' });
  var undS = sliceSeries(L.undrawn);
  kpi('lq-undrawn', { unit: '£', value: grp3(und, 1) + 'm', delta: 0, deltaText: pct(und / Math.max(sum(fs.filter(function (f) { return f.committed; }), function (f) { return f.limit; }), 1) * 100) + ' of limits',
    per: 'undrawn', dir: 'flat', series: undS.map(function (v, i) { return v + i * 0; }), href: '#/liquidity' });
  var hd = liq.map(function (v) { return v - need; });
  kpi('lq-head', { unit: hd[hd.length - 1] < 0 ? '−£' : '£', value: grp3(Math.abs(hd[hd.length - 1]), 1) + 'm', delta: deltaPct(hd[hd.length - 1], hd[0]), deltaText: deltaText(deltaPct(hd[hd.length - 1], hd[0])), per: per(), series: hd, href: '#/liquidity' });
  var cover = liq.map(function (v) { return need ? v / need : 0; });
  kpi('lq-need', { unit: '', value: (Math.round(cover[cover.length - 1] * 10) / 10).toFixed(1) + '×', delta: deltaPct(cover[cover.length - 1], cover[0]),
    deltaText: deltaText(deltaPct(cover[cover.length - 1], cover[0])), per: 'of £' + grp3(need, 0) + 'm planned', series: cover, href: '#/liquidity' });
  var regs = DATA.regions.filter(function (r) { return STATE.region === 'all' || r === STATE.region; }).filter(function (r) { return scopedAccounts().some(function (a) { return a.region === r; }); });
  if (regs.length) {
    chart('lq-trend', { type: 'stacked-area', categories: days(), categoryLabel: 'Day', unit: '£m', caption: 'Cash plus undrawn committed facilities by region, daily, GBP millions',
      series: regs.map(function (r) { var ac = scopedAccounts().filter(function (a) { return a.region === r; }), u = undrawnCommitted(fs.filter(function (f) { return f.region === r; }));
        return { name: r, values: sliceSeries(cashSeries(ac)).map(function (v) { return r1(v + u); }) }; }) },
      { title: 'Available liquidity by region, last ' + STATE.days + ' days' });
  }
  var fz = fs.slice().sort(function (a, b) { return b.limit - a.limit; });
  if (fz.length) {
    chart('lq-combo', { type: 'combo', categories: fz.map(function (f) { return f.id; }), categoryLabel: 'Facility', target: 80, targetLabel: 'Internal limit 80%',
      series: [{ name: 'Drawn', kind: 'column', unit: '£m', values: fz.map(function (f) { return r1(f.drawn); }) },
               { name: 'Utilisation', kind: 'line', unit: '%', values: fz.map(function (f) { return r1(f.drawn / f.limit * 100); }) }],
      caption: 'Drawn amount (GBP millions, left) and utilisation (per cent, right) by facility' }, { title: 'Drawn and utilisation by facility' });
    var top = fs.slice().sort(function (a, b) { return b.drawn / b.limit - a.drawn / a.limit; }).slice(0, 6);
    chart('lq-bullet', { type: 'bullet', categories: top.map(function (f) { return f.id + ' ' + f.type; }), categoryLabel: 'Facility', unit: '%', ranges: [60, 85, 120],
      series: [{ name: 'Utilisation', values: top.map(function (f) { return r1(f.drawn / f.limit * 100); }) }, { name: 'Internal limit', values: top.map(function (f) { return f.internalLimit; }) }],
      caption: 'Facility utilisation against internal limit, per cent' }, { title: 'Utilisation against internal limit, highest six' });
  }
  renderGrid('fac');
};
RECORD.liquidity = function (id) {
  var f = DATA.facilities.filter(function (x) { return x.id === id; })[0]; if (!f) { return false; }
  var room = r1(f.limit * f.internalLimit / 100 - f.drawn);
  openDrawer(f.name, dl([['Facility', f.id], ['Borrower', entName(f.entity)], ['Type', f.type], ['Limit', gbpM(f.limit, 0)], ['Drawn', gbpM(f.drawn)],
    ['Utilisation', pct(f.drawn / f.limit * 100)], ['Internal limit', f.internalLimit + '% of limit'], ['Room to internal limit', gbpM(Math.max(room, 0))], ['Matures', fmtDate(f.maturity)]]) +
    head4('Drawdowns requested in this prototype') + auditHTML(f.history.map(function (h) { return { at: h.at, who: 'You', note: gbpM(h.amount) + ' for ' + h.purpose }; })),
    [{ label: 'Request a drawdown', run: function () { drawdown(f); } }, { label: 'Close', kind: 'secondary' }], recordClosed);
  return true;
};
function drawdown(f) {
  var room = r1(f.limit * f.internalLimit / 100 - f.drawn);
  openModal({ title: 'Request a drawdown — ' + f.id, text: 'Simulated request. Room to the internal limit is ' + gbpM(Math.max(room, 0)) + '.', confirm: 'Submit request',
    form: textField('amount', 'Amount in GBP millions', 'Up to ' + grp3(Math.max(room, 0), 1) + ' without breaching the internal limit.', { prefix: 'GBP m', inputmode: 'decimal' }) +
      selectField('date', 'Value date', [1, 2, 3, 4, 5].map(function (d) { var iso = dayISO(-d); return [iso, fmtDate(iso)]; }), '') +
      areaField('purpose', 'Purpose', 'At least 10 characters. Visible to approvers.', { max: 300 }),
    after: wireForm,
    onConfirm: function (form) {
      var amt = parseFloat(fieldVal(form, 'amount').replace(/,/g, '')), ok = true;
      if (!(amt > 0)) { setError(form, 'amount', 'Enter an amount greater than zero, in GBP millions.'); ok = false; }
      else if (amt > room) { setError(form, 'amount', 'This would take ' + f.id + ' over its internal limit. The most you can draw is ' + grp3(Math.max(room, 0), 1) + 'm.'); ok = false; }
      if (!fieldVal(form, 'date')) { setError(form, 'date', 'Choose a value date.'); ok = false; }
      if (fieldVal(form, 'purpose').length < 10) { setError(form, 'purpose', 'Describe the purpose in at least 10 characters.'); ok = false; }
      if (!ok) { focusFirstError(form); return false; }
      var d = { id: 'DD-' + Date.now().toString(36).toUpperCase(), facility: f.id, amount: r2(amt), at: dayISO(0), valueDate: fieldVal(form, 'date'), purpose: fieldVal(form, 'purpose') };
      WORK.drawdowns.push(d); persistWork(); f.drawn = r2(f.drawn + d.amount); f.history.push(d);
      toast('ok', 'Drawdown of ' + gbpM(amt) + ' on ' + f.id + ' requested for ' + fmtDate(d.valueDate) + '.');
      renderView(); RECORD.liquidity(f.id); return true;
    } });
}

/* ================================================================ PAYMENTS AND APPROVALS */
grid('pay', { view: 'payments', noun: 'payments', one: 'payment', defaultSort: { key: 'valueDate', dir: 'asc' },
  all: function () { return DATA.payments; },
  rows: function () { return DATA.payments.filter(function (p) { return inScope(p, 'created') && (!STATE.status || p.status === STATE.status) &&
    matchesQ(p, ['id', 'beneficiary', 'entity', 'ccy', 'type', 'status']); }); },
  cell: { valueDate: function (r) { return '<span class="t-cm-label">' + fmtDate(r.valueDate) + '</span>'; }, amount: function (r) { return '<span class="t-cm-figure-5">' + grp3(r.amount, 0) + '</span>'; },
          gbp: function (r) { return '<span class="t-cm-figure-5">' + gbpM(r.gbp / 1e6, 2) + '</span>'; } },
  sortKey: { status: function (r) { return r.status === 'Pending approval' ? '0' : r.status; } },
  csv: ['id', 'created', 'valueDate', 'entity', 'beneficiary', 'type', 'ccy', 'amount', 'gbp', 'status', 'approvals'] });
RENDER.payments = function () {
  var ps = DATA.payments.filter(function (p) { return inScope(p); }), inP = ps.filter(function (p) { return inScope(p, 'created'); }), pd = periodIdx();
  var pend = ps.filter(function (p) { return p.status === 'Pending approval'; });
  var pendS = pd.map(function (d) { return pend.filter(function (p) { return p.created <= d; }).length; });
  var valS = pd.map(function (d) { return sum(pend.filter(function (p) { return p.created <= d; }), function (p) { return p.gbp / 1e6; }); });
  var rel = inP.filter(function (p) { return p.status === 'Released'; }), relS = pd.map(function (d) { return sum(rel.filter(function (p) { return p.created === d; }), function (p) { return p.gbp / 1e6; }); });
  var rej = inP.filter(function (p) { return p.status === 'Rejected'; }), rejS = pd.map(function (d) { return rej.filter(function (p) { return p.created <= d; }).length; });
  kpi('py-pending', { unit: '', value: String(pend.length), delta: 0, dir: 'flat', deltaText: pend.filter(function (p) { return p.gbp >= 5e6; }).length + ' of £5m+', per: 'need a note', series: pendS, href: '#/payments?status=Pending%20approval' });
  kpi('py-value', { unit: '£', value: grp3(sum(pend, function (p) { return p.gbp / 1e6; }), 1) + 'm', delta: 0, dir: 'flat', deltaText: 'largest ' + gbpM(Math.max.apply(null, pend.map(function (p) { return p.gbp / 1e6; }).concat([0]))), per: '', series: valS, href: '#/payments?status=Pending%20approval' });
  kpi('py-released', { unit: '£', value: grp3(sum(rel, function (p) { return p.gbp / 1e6; }), 1) + 'm', delta: deltaPct(sum(relS.slice(Math.floor(pd.length / 2))), sum(relS.slice(0, Math.floor(pd.length / 2)))),
    deltaText: deltaText(deltaPct(sum(relS.slice(Math.floor(pd.length / 2))), sum(relS.slice(0, Math.floor(pd.length / 2))))), per: 'second half vs first', series: relS, href: '#/payments?status=Released' });
  kpi('py-rejected', { unit: '', value: String(rej.length), delta: 0, dir: 'flat', deltaText: rel.length + rej.length ? pct(rej.length / (rel.length + rej.length) * 100) + ' of decisions' : 'No decisions', per: '', series: rejS, href: '#/payments?status=Rejected' });
  var ccys = CCY5.concat(['Other']).filter(function (c) { return inP.some(function (p) { return ccyBucket(p.ccy) === c; }); });
  var STS = ['Pending approval', 'Scheduled', 'Released', 'Rejected'];
  if (ccys.length) {
    chart('py-status', { type: 'grouped-column', categories: ccys, categoryLabel: 'Currency', unit: '£m', caption: 'Payment value by currency and status, GBP millions',
      series: STS.map(function (st) { return { name: st, values: ccys.map(function (c) { return r1(sum(inP.filter(function (p) { return ccyBucket(p.ccy) === c && p.status === st; }), function (p) { return p.gbp / 1e6; })); }) }; }) },
      { title: 'Payment value by currency and status' });
  }
  var tx = DATA.transactions.filter(function (t) { return inScope(t, 'date'); }), regs = DATA.regions.filter(function (r) { return tx.some(function (t) { return t.region === r; }); });
  if (regs.length) {
    chart('py-flows', { type: 'butterfly-h', categories: regs, categoryLabel: 'Region', unit: '£m', caption: 'Money in against money out by region, GBP millions',
      series: [{ name: 'Money in', values: regs.map(function (r) { return r1(sum(tx.filter(function (t) { return t.region === r && t.gbp > 0; }), function (t) { return t.gbp / 1e6; })); }) },
               { name: 'Money out', values: regs.map(function (r) { return r1(sum(tx.filter(function (t) { return t.region === r && t.gbp < 0; }), function (t) { return -t.gbp / 1e6; })); }) }] },
      { title: 'Money in against money out by region' });
  }
  renderGrid('pay');
};
RECORD.payments = function (id) {
  var p = DATA.payments.filter(function (x) { return x.id === id; })[0]; if (!p) { return false; }
  var acts = p.status === 'Pending approval' ? [{ label: 'Approve', run: function () { decide(p, 'approve'); } }, { label: 'Reject', kind: 'secondary', run: function () { decide(p, 'reject'); } }]
    : [{ label: 'Close', kind: 'secondary' }];
  openDrawer('Payment ' + p.id, dl([['Status', stat(p.status), true], ['Beneficiary', p.beneficiary], ['Amount', money(p.amount, p.ccy)], ['GBP equivalent', gbpM(p.gbp / 1e6, 2)],
    ['Value date', fmtDate(p.valueDate)], ['Debit entity', entName(p.entity)], ['Type', p.type], ['Requested by', p.requestedBy], ['Approvals', p.approvals]]) +
    (p.status === 'Pending approval' && p.gbp >= 5e6 ? para('This payment is £5m or more, so an approval note is required.') : '') + head4('Audit trail') + auditHTML(p.audit), acts, recordClosed);
  return true;
};
function decide(p, what) {
  var big = p.gbp >= 5e6, approve = what === 'approve';
  openModal({ title: (approve ? 'Approve ' : 'Reject ') + p.id, text: (approve ? 'You are approving ' : 'You are rejecting ') + money(p.amount, p.ccy) + ' to ' + p.beneficiary + '. This is a simulation; nothing is sent.',
    confirm: approve ? 'Approve payment' : 'Reject payment',
    form: approve && !big ? '' : areaField('note', approve ? 'Approval note' : 'Reason for rejection', 'At least 10 characters. Recorded in the audit trail.', { max: 300 }),
    after: wireForm,
    onConfirm: function (form) {
      var note = fieldVal(form, 'note');
      if ((!approve || big) && note.length < 10) { setError(form, 'note', approve ? 'Payments of £5m or more need an approval note of at least 10 characters.' : 'Give a reason of at least 10 characters.'); focusFirstError(form); return false; }
      p.status = approve ? 'Released' : 'Rejected'; p.approvals = approve ? '2 of 2' : p.approvals;
      var entry = { at: dayISO(0), who: 'You (CEO)', note: (approve ? 'Approved and released' : 'Rejected') + (note ? ' — ' + note : '') };
      var w = WORK.payments[p.id] || { audit: [] }; w.status = p.status; w.approvals = p.approvals; w.audit = (w.audit || []).concat([entry]); WORK.payments[p.id] = w; persistWork();
      p.audit.push(entry);
      toast(approve ? 'ok' : 'info', p.id + (approve ? ' approved and released.' : ' rejected.'));
      renderView(); RECORD.payments(p.id); return true;
    } });
}

/* ================================================================ FX AND MARKETS */
grid('deal', { view: 'fx', noun: 'deals', one: 'deal', defaultSort: { key: 'trade', dir: 'desc' },
  all: function () { return DATA.deals; },
  rows: function () { return DATA.deals.filter(function (d) { return inScope(d) && matchesQ(d, ['id', 'pair', 'product', 'entity', 'status']); }); },
  cell: { trade: function (r) { return '<span class="t-cm-label">' + fmtDate(r.trade) + '</span>'; }, maturity: function (r) { return '<span class="t-cm-label">' + fmtDate(r.maturity) + '</span>'; },
          notional: function (r) { return '<span class="t-cm-figure-5">' + grp3(r.notional, 1) + '</span>'; }, rate: function (r) { return '<span class="t-cm-figure-5">' + r.rate.toFixed(4) + '</span>'; },
          mtm: function (r) { return '<span class="t-cm-figure-5">' + grp3(r.mtm, 0) + '</span>'; } },
  csv: ['id', 'trade', 'entity', 'product', 'pair', 'notional', 'rate', 'maturity', 'mtm', 'status'] });
function fxExposure() { return sum(DATA.positions.filter(function (p) { return inScope(p) && p.ccy !== 'GBP'; }), function (p) { return p.gbp; }); }
RENDER.fx = function () {
  var n = STATE.days, us = DATA.fxSeries.USD.closes.slice(30 - n), eu = DATA.fxSeries.EUR.closes.slice(30 - n);
  kpi('fx-usd', { unit: '', value: DATA.fx.USD.toFixed(4), delta: deltaPct(us[us.length - 1], us[0]), deltaText: deltaText(deltaPct(us[us.length - 1], us[0])), per: per(), series: us, href: '#/fx' });
  kpi('fx-eur', { unit: '', value: DATA.fx.EUR.toFixed(4), delta: deltaPct(eu[eu.length - 1], eu[0]), deltaText: deltaText(deltaPct(eu[eu.length - 1], eu[0])), per: per(), series: eu, href: '#/fx' });
  var exp = fxExposure(), open = DATA.deals.filter(function (d) { return inScope(d) && d.status === 'Open'; });
  var hedS = periodIdx().map(function (d) { return sum(open.filter(function (x) { return x.trade <= d; }), function (x) { return x.notional; }); });
  var unS = hedS.map(function (h) { return Math.max(exp - h, 0); }), ratS = hedS.map(function (h) { return exp ? Math.min(h / exp * 100, 100) : 0; });
  kpi('fx-unhedged', { unit: '£', value: grp3(unS[unS.length - 1], 1) + 'm', delta: deltaPct(unS[unS.length - 1], unS[0]), deltaText: deltaText(deltaPct(unS[unS.length - 1], unS[0])), per: per(), series: unS, href: '#/fx' });
  kpi('fx-ratio', { unit: '', value: pct(ratS[ratS.length - 1]), delta: ratS[ratS.length - 1] - ratS[0], deltaText: deltaText(ratS[ratS.length - 1] - ratS[0], ' pts'), per: 'of £' + grp3(exp, 0) + 'm', series: ratS, href: '#/fx' });
  var o = DATA.fxSeries.USD.ohlc.slice(30 - n);
  chart('fx-candle', { type: 'candlestick', categories: days(), categoryLabel: 'Session', caption: 'GBP/USD open, high, low and close by session (illustrative)',
    series: ['Open', 'High', 'Low', 'Close'].map(function (nm, k) { return { name: nm, values: o.map(function (c) { return Math.round(c[k] * 10000) / 10000; }) }; }) },
    { title: 'GBP/USD, last ' + n + ' sessions (illustrative)' });
  summary('fx-rates', { k: 'Rates as at ' + fmtDate(DATA.asAt), sub: 'placeholders, not market data', v: 'GBP base' },
    ['USD', 'EUR', 'SGD', 'HKD', 'AED', 'CNY'].map(function (c) { return { label: '1 GBP buys ' + c, value: DATA.fx[c].toFixed(4) + ' ' + c }; }));
  var cs = ['USD', 'EUR', 'SGD', 'HKD', 'AED'];
  chart('fx-index', { type: 'multiline', categories: days(), categoryLabel: 'Session', caption: 'Sterling against five currencies, indexed to 100 at the start of the period',
    series: cs.map(function (c) { var s = DATA.fxSeries[c].closes.slice(30 - n); return { name: 'GBP/' + c, values: s.map(function (v) { return Math.round(v / s[0] * 10000) / 100; }) }; }) },
    { title: 'Sterling indexed to 100, last ' + n + ' sessions' });
  function q(a, p) { var s = a.slice().sort(function (x, y) { return x - y; }), i = (s.length - 1) * p, lo = Math.floor(i); return s[lo] + (s[Math.ceil(i)] - s[lo]) * (i - lo); }
  var moves = cs.map(function (c) { var s = DATA.fxSeries[c].closes.slice(30 - n); var m = []; for (var i = 1; i < s.length; i++) { m.push(Math.abs(s[i] / s[i - 1] - 1) * 10000); } return m.length ? m : [0]; });
  chart('fx-box', { type: 'boxplot', categories: cs.map(function (c) { return 'GBP/' + c; }), categoryLabel: 'Pair', unit: 'bp', caption: 'Size of daily moves by pair, basis points',
    series: ['Minimum', 'Lower quartile', 'Median', 'Upper quartile', 'Maximum'].map(function (nm, k) { return { name: nm, values: moves.map(function (m) { return Math.round(q(m, k / 4) * 10) / 10; }) }; }) },
    { title: 'How large daily moves are, by pair' });
  renderGrid('deal');
};
RECORD.fx = function (id) {
  var d = DATA.deals.filter(function (x) { return x.id === id; })[0]; if (!d) { return false; }
  openDrawer('Deal ' + d.id, dl([['Status', stat(d.status === 'Open' ? 'Open' : 'Settled'), true], ['Product', d.product], ['Pair', d.pair], ['Notional', gbpM(d.notional)], ['Rate', d.rate.toFixed(4)],
    ['Traded', fmtDate(d.trade)], ['Matures', fmtDate(d.maturity)], ['Entity', entName(d.entity)], ['Mark to market', '£' + grp3(d.mtm, 0) + 'k (illustrative)']]),
    [{ label: 'Request a quote like this', run: function () { closeDrawer(true); quote(d.pair); } }, { label: 'Close', kind: 'secondary' }], recordClosed);
  return true;
};
function quote(pair) {
  openModal({ title: 'Request an indicative quote', text: 'Simulated. The rate comes from the illustrative rates, not from a market feed, and no deal is sent to HSBC.', confirm: 'Book simulated deal',
    form: selectField('pair', 'Currency pair', PAIRS.map(function (p) { return [p, p]; }), pair || 'GBP/USD') +
      selectField('side', 'You', [['Buy', 'Buy the foreign currency'], ['Sell', 'Sell the foreign currency']], 'Buy') +
      selectField('tenor', 'Tenor', [['Spot', 'Spot'], ['1M', 'One month'], ['3M', 'Three months'], ['6M', 'Six months']], '3M') +
      textField('notional', 'Notional in GBP millions', 'Between 0.1 and 100.', { prefix: 'GBP m', inputmode: 'decimal' }) +
      selectField('entity', 'Booking entity', DATA.entities.map(function (e) { return [e.id, e.name]; }), STATE.entity !== 'all' ? STATE.entity : 'NWG-UK'),
    after: wireForm,
    onConfirm: function (form) {
      var n = parseFloat(fieldVal(form, 'notional')), ok = true;
      if (!(n >= 0.1 && n <= 100)) { setError(form, 'notional', 'Enter a notional between 0.1 and 100 GBP millions.'); ok = false; }
      if (!ok) { focusFirstError(form); return false; }
      var pr = fieldVal(form, 'pair'), qc = pr.split('/')[1], base = pr.indexOf('EUR') === 0 ? DATA.fx.USD / DATA.fx.EUR : DATA.fx[qc];
      var tenor = fieldVal(form, 'tenor'), pts = { Spot: 0, '1M': 0.0012, '3M': 0.0034, '6M': 0.0065 }[tenor], rate = Math.round(base * (1 - pts) * 10000) / 10000;
      var e = fieldVal(form, 'entity'), deal = { id: 'FXD-' + pad(60000 + WORK.newDeals.length + 1, 5), trade: dayISO(0), entity: e, region: ENT[e].region,
        product: tenor === 'Spot' ? 'Spot' : 'Forward', pair: pr, notional: r2(n), rate: rate, maturity: dayISO(-({ Spot: 2, '1M': 30, '3M': 91, '6M': 182 }[tenor])), mtm: 0, status: 'Open', ccy: qc };
      WORK.newDeals.push(deal); persistWork(); DATA.deals.unshift(deal);
      toast('ok', 'Simulated ' + fieldVal(form, 'side').toLowerCase() + ' of ' + gbpM(n) + ' ' + pr + ' at ' + rate.toFixed(4) + ' booked as ' + deal.id + '.');
      renderView(); return true;
    } });
}

/* ================================================================ RISK AND LIMITS */
grid('pos', { view: 'risk', noun: 'positions', one: 'position', defaultSort: { key: 'gbp', dir: 'desc' },
  all: function () { return DATA.positions; },
  rows: function () { return DATA.positions.filter(function (p) { return inScope(p) && matchesQ(p, ['id', 'counterparty', 'entity', 'ccy', 'product', 'region']); }); },
  cell: { gbp: function (r) { return '<span class="t-cm-figure-5">' + grp3(r.gbp, 1) + '</span>'; } },
  csv: ['id', 'entity', 'region', 'counterparty', 'rating', 'ccy', 'product', 'gbp'] });
grid('lim', { view: 'risk', noun: 'limits', one: 'limit', defaultSort: { key: 'util', dir: 'desc' },
  all: function () { return DATA.limits; },
  rows: function () { return DATA.limits.filter(function (l) { return inScope(l) && matchesQ(l, ['id', 'name', 'kind', 'region', 'status']); }); },
  cell: { util: function (r) { return '<span class="t-cm-figure-5">' + pct(r.util) + '</span>'; }, limit: function (r) { return '<span class="t-cm-figure-5">' + grp3(r.limit, 0) + '</span>'; },
          used: function (r) { return '<span class="t-cm-figure-5">' + grp3(r.used, 1) + '</span>'; } },
  csv: ['id', 'name', 'kind', 'rating', 'region', 'limit', 'used', 'util', 'status'] });
grid('exc', { view: 'risk', noun: 'exceptions', one: 'exception', defaultSort: { key: 'status', dir: 'desc' },
  all: function () { return DATA.exceptions; },
  rows: function () { return DATA.exceptions.filter(function (x) { return inScope(x, 'raised') && matchesQ(x, ['id', 'title', 'entity', 'severity', 'status']); }); },
  cell: { raised: function (r) { return '<span class="t-cm-label">' + fmtDate(r.raised) + '</span>'; } },
  sortKey: { status: function (r) { return (r.status === 'Open' ? 'z' : 'a') + (r.severity === 'Material' ? 'z' : 'a'); } },
  csv: ['id', 'raised', 'entity', 'title', 'severity', 'status'] });
function limitsAt(d) { return DATA.limits.filter(function (l) { return inScope(l); }).map(function (l) { return l.used * DATA.expWalk[l.region][d] / l.limit * 100; }); }
RENDER.risk = function () {
  var pos = DATA.positions.filter(function (p) { return inScope(p); }), idx = [];
  for (var d = 30 - STATE.days; d < 30; d++) { idx.push(d); }
  var expS = idx.map(function (d) { return sum(pos, function (p) { return p.gbp * DATA.expWalk[p.region][d]; }); });
  var brS = idx.map(function (d) { return limitsAt(d).filter(function (u) { return u >= 100; }).length; });
  var nrS = idx.map(function (d) { return limitsAt(d).filter(function (u) { return u >= 90 && u < 100; }).length; });
  var openX = DATA.exceptions.filter(function (x) { return inScope(x) && x.status === 'Open'; });
  var opS = idx.map(function (d) { var iso = SERIES_DAYS[d]; return DATA.exceptions.filter(function (x) { return inScope(x) && x.raised <= iso && (x.status === 'Open' || (x.audit.length && x.audit[x.audit.length - 1].at > iso)); }).length; });
  kpi('rk-exp', { unit: '£', value: grp3(expS[expS.length - 1], 1) + 'm', delta: deltaPct(expS[expS.length - 1], expS[0]), deltaText: deltaText(deltaPct(expS[expS.length - 1], expS[0])), per: per(), series: expS, href: '#/risk?tab=positions' });
  kpi('rk-breach', { unit: '', value: String(brS[brS.length - 1]), delta: brS[brS.length - 1] - brS[0], deltaText: deltaText(brS[brS.length - 1] - brS[0], ''), per: per(), series: brS, href: '#/risk?tab=limits' });
  kpi('rk-near', { unit: '', value: String(nrS[nrS.length - 1]), delta: nrS[nrS.length - 1] - nrS[0], deltaText: deltaText(nrS[nrS.length - 1] - nrS[0], ''), per: per(), series: nrS, href: '#/risk?tab=limits' });
  kpi('rk-open', { unit: '', value: String(openX.length), delta: 0, dir: 'flat', deltaText: openX.filter(function (x) { return x.severity === 'Material'; }).length + ' material', per: '', series: opS, href: '#/risk?tab=exceptions' });
  var regs = DATA.regions.filter(function (r) { return pos.some(function (p) { return p.region === r; }); });
  if (regs.length) {
    chart('rk-region', { type: 'bar', categories: regs, categoryLabel: 'Region', unit: '£m', caption: 'Exposure by region, GBP millions',
      series: [{ name: 'Exposure', values: regs.map(function (r) { return r1(sum(pos.filter(function (p) { return p.region === r; }), function (p) { return p.gbp; })); }) }] },
      { title: 'Exposure by region — select a region to filter', drill: 'region' });
  }
  var lims = DATA.limits.filter(function (l) { return inScope(l) && l.kind === 'Counterparty'; }).sort(function (a, b) { return a.used - b.used; });
  var seen = {};
  if (lims.length) {
    chart('rk-scatter', { type: 'scatter', categoryLabel: 'Exposure (£m)', caption: 'Counterparty exposure (GBP millions) against limit utilisation (per cent)',
      categories: lims.map(function (l) { var x = r1(l.used); while (seen[x]) { x = r1(x + 0.1); } seen[x] = 1; return String(x); }),
      series: [{ name: 'Utilisation (%)', values: lims.map(function (l) { return l.util; }) }] },
      { title: 'Counterparties: exposure against limit utilisation' });
  }
  var top = DATA.limits.filter(function (l) { return inScope(l); }).sort(function (a, b) { return b.util - a.util; }).slice(0, 6);
  if (top.length) {
    chart('rk-bullet', { type: 'bullet', categories: top.map(function (l) { return l.name; }), categoryLabel: 'Limit', unit: '%', ranges: [75, 90, 130],
      series: [{ name: 'Utilisation', values: top.map(function (l) { return Math.min(l.util, 130); }) }, { name: 'Limit', values: top.map(function () { return 100; }) }],
      caption: 'Limit utilisation against the limit, per cent' }, { title: 'The six limits closest to breach' });
  }
  renderGrid('pos'); renderGrid('lim'); renderGrid('exc');
};
RECORD.risk = function (id) {
  var x = DATA.exceptions.filter(function (e) { return e.id === id; })[0], l = DATA.limits.filter(function (e) { return e.id === id; })[0], p = DATA.positions.filter(function (e) { return e.id === id; })[0];
  if (x) {
    openDrawer(x.title, dl([['Exception', x.id], ['Status', stat(x.status), true], ['Severity', stat(x.severity), true], ['Raised', fmtDate(x.raised)], ['Entity', entName(x.entity)], ['Region', x.region]]) +
      para(x.detail) + head4('Acknowledgements and audit notes') + auditHTML(x.audit),
      x.status === 'Open' ? [{ label: 'Acknowledge with a note', run: function () { acknowledge(x); } }, { label: x.limitId ? 'Show the limit' : 'Close', kind: 'secondary', run: function () { if (x.limitId) { go(hashFor('risk', x.limitId)); } else { closeDrawer(); } } }]
        : [{ label: 'Add an audit note', run: function () { acknowledge(x); } }, { label: 'Close', kind: 'secondary' }], recordClosed);
    return true;
  }
  if (l) {
    openDrawer('Limit ' + l.id, dl([['Limit on', l.name], ['Kind', l.kind], ['Rating', l.rating || '—'], ['Region', l.region], ['Limit', gbpM(l.limit, 0)], ['Used', gbpM(l.used)],
      ['Utilisation', pct(l.util)], ['Status', stat(l.status), true]]), [{ label: 'Show positions', run: function () { closeDrawer(true); STATE.q = l.kind === 'Counterparty' ? l.name : ''; ftbQ.value = STATE.q;
        if (l.kind !== 'Counterparty') { STATE.region = l.region; } UI.tab['rk-tabs'] = 'positions'; go(hashFor('risk')); } }, { label: 'Close', kind: 'secondary' }], recordClosed);
    return true;
  }
  if (p) {
    openDrawer('Position ' + p.id, dl([['Counterparty', p.counterparty], ['Rating', p.rating], ['Entity', entName(p.entity)], ['Region', p.region], ['Currency', p.ccy], ['Product', p.product], ['Exposure', gbpM(p.gbp)]]),
      [{ label: 'Close', kind: 'secondary' }], recordClosed);
    return true;
  }
  return false;
};
function acknowledge(x) {
  openModal({ title: 'Acknowledge ' + x.id, text: x.title + '. Your note is recorded against the exception with your name and today\'s date.', confirm: 'Acknowledge',
    form: areaField('note', 'Audit note', 'At least 15 characters: what you have decided and who follows up.', { max: 500 }) +
      selectField('owner', 'Follow-up owner', [['Group treasurer', 'Group treasurer'], ['Chief risk officer', 'Chief risk officer'], ['Regional CFO', 'Regional CFO'], ['HSBC relationship manager', 'HSBC relationship manager']], ''),
    after: wireForm,
    onConfirm: function (form) {
      var note = fieldVal(form, 'note'), owner = fieldVal(form, 'owner'), ok = true;
      if (note.length < 15) { setError(form, 'note', 'Write an audit note of at least 15 characters.'); ok = false; }
      if (!owner) { setError(form, 'owner', 'Choose who follows this up.'); ok = false; }
      if (!ok) { focusFirstError(form); return false; }
      x.status = 'Acknowledged'; x.audit.push({ at: dayISO(0), who: 'You (CEO) → ' + owner, note: note });
      WORK.exceptions[x.id] = { status: x.status, audit: x.audit }; persistWork();
      toast('ok', x.id + ' acknowledged. Follow-up owner: ' + owner + '.');
      renderView(); RECORD.risk(x.id); return true;
    } });
}

/* ================================================================ TRADE FINANCE */
grid('tf', { view: 'trade', noun: 'instruments', one: 'instrument', defaultSort: { key: 'expiry', dir: 'asc' },
  all: function () { return DATA.trade; },
  rows: function () { return DATA.trade.filter(function (t) { return inScope(t) && matchesQ(t, ['id', 'type', 'entity', 'counterparty', 'ccy', 'status']); }); },
  cell: { amount: function (r) { return '<span class="t-cm-figure-5">' + grp3(r.amount, 0) + '</span>'; }, expiry: function (r) { return '<span class="t-cm-label">' + fmtDate(r.expiry) + '</span>'; } },
  csv: ['id', 'type', 'entity', 'counterparty', 'ccy', 'amount', 'gbp', 'issued', 'expiry', 'status'] });
RENDER.trade = function () {
  var ts = DATA.trade.filter(function (t) { return inScope(t); }), live = ts.filter(function (t) { return t.status !== 'Expired'; }), pd = periodIdx();
  var liveOn = function (d) { return live.filter(function (t) { return t.issued <= d; }); };
  var outS = pd.map(function (d) { return sum(liveOn(d), function (t) { return t.gbp / 1e6; }); });
  var lcS = pd.map(function (d) { return sum(liveOn(d).filter(function (t) { return /letter of credit/.test(t.type); }), function (t) { return t.gbp / 1e6; }); });
  var soon = live.filter(function (t) { var d = -daysBefore(t.expiry); return d >= 0 && d <= 30; });
  var soonS = pd.map(function (d) { return live.filter(function (t) { var k = (Date.parse(t.expiry) - Date.parse(d)) / DAY; return t.issued <= d && k >= 0 && k <= 30; }).length; });
  var lines = scopedFacilities().filter(function (f) { return f.type === 'Trade line'; }), lim = sum(lines, function (f) { return f.limit; });
  var utS = outS.map(function (v) { return lim ? v / lim * 100 : 0; });
  kpi('tf-out', { unit: '£', value: grp3(outS[outS.length - 1], 1) + 'm', delta: deltaPct(outS[outS.length - 1], outS[0]), deltaText: deltaText(deltaPct(outS[outS.length - 1], outS[0])), per: live.length + ' instruments', series: outS, href: '#/trade' });
  kpi('tf-lc', { unit: '£', value: grp3(lcS[lcS.length - 1], 1) + 'm', delta: deltaPct(lcS[lcS.length - 1], lcS[0]), deltaText: deltaText(deltaPct(lcS[lcS.length - 1], lcS[0])), per: per(), series: lcS, href: '#/trade' });
  kpi('tf-exp', { unit: '', value: String(soon.length), delta: soonS[soonS.length - 1] - soonS[0], deltaText: deltaText(soonS[soonS.length - 1] - soonS[0], ''), per: gbpM(sum(soon, function (t) { return t.gbp / 1e6; })) + ' in value', series: soonS, href: '#/trade' });
  kpi('tf-util', { unit: '', value: lim ? pct(utS[utS.length - 1]) : '—', delta: utS[utS.length - 1] - utS[0], deltaText: lim ? deltaText(utS[utS.length - 1] - utS[0], ' pts') : 'No trade line in scope', per: lim ? 'of £' + grp3(lim, 0) + 'm lines' : '', series: utS, href: '#/liquidity' });
  var types = TF_TYPES.filter(function (t) { return live.some(function (x) { return x.type === t; }); });
  if (types.length) {
    chart('tf-mix', { type: 'pie', categories: types, categoryLabel: 'Instrument', unit: '£m', caption: 'Outstanding trade instruments by type, GBP millions',
      series: [{ name: 'Outstanding', values: types.map(function (t) { return r1(sum(live.filter(function (x) { return x.type === t; }), function (x) { return x.gbp / 1e6; })); }) }] },
      { title: 'Instrument mix by value' });
  }
  var weeks = [0, 1, 2, 3, 4, 5, 6, 7], wl = weeks.map(function (w) { return 'From ' + shortDate(dayISO(-w * 7 - 1)); });
  chart('tf-expiry', { type: 'column', categories: wl, categoryLabel: 'Week', unit: '£m', caption: 'Value of instruments expiring each week for the next eight weeks, GBP millions',
    series: [{ name: 'Expiring', values: weeks.map(function (w) { return r1(sum(live.filter(function (t) { var k = -daysBefore(t.expiry); return k > w * 7 && k <= w * 7 + 7; }), function (t) { return t.gbp / 1e6; })); }) }] },
    { title: 'Value expiring each week, next eight weeks' });
  renderGrid('tf');
};
RECORD.trade = function (id) {
  var t = DATA.trade.filter(function (x) { return x.id === id; })[0]; if (!t) { return false; }
  openDrawer(t.type + ' ' + t.id, dl([['Status', stat(t.status), true], ['Applicant', entName(t.entity)], ['Beneficiary', t.counterparty], ['Amount', money(t.amount, t.ccy)],
    ['GBP equivalent', gbpM(t.gbp / 1e6, 2)], ['Issued', fmtDate(t.issued)], ['Expires', fmtDate(t.expiry)]]) + head4('Amendments and notes') + auditHTML(t.audit),
    t.status === 'Expired' ? [{ label: 'Close', kind: 'secondary' }] : [{ label: 'Request an amendment', run: function () { amend(t); } }, { label: 'Close', kind: 'secondary' }], recordClosed);
  return true;
};
function amend(t) {
  openModal({ title: 'Request an amendment to ' + t.id, text: 'This raises a simulated service request with HSBC Trade services.', confirm: 'Send request',
    form: selectField('kind', 'Amendment', [['Extend expiry', 'Extend the expiry date'], ['Increase amount', 'Increase the amount'], ['Change documents', 'Change the required documents']], '') +
      areaField('detail', 'Details', 'At least 20 characters.', { max: 500 }),
    after: wireForm,
    onConfirm: function (form) {
      var k = fieldVal(form, 'kind'), d = fieldVal(form, 'detail'), ok = true;
      if (!k) { setError(form, 'kind', 'Choose the amendment you need.'); ok = false; }
      if (d.length < 20) { setError(form, 'detail', 'Give at least 20 characters of detail.'); ok = false; }
      if (!ok) { focusFirstError(form); return false; }
      var sr = newRequest('Trade instrument amendment', t.entity, k + ' — ' + t.id, d);
      t.status = 'Amendment requested'; t.audit.push({ at: dayISO(0), who: 'You (CEO)', note: k + ' requested as ' + sr.id + ': ' + d });
      WORK.trade[t.id] = { status: t.status, audit: t.audit }; persistWork();
      toast('ok', 'Amendment request ' + sr.id + ' sent for ' + t.id + '.'); renderView(); RECORD.trade(t.id); return true;
    } });
}

/* ================================================================ REPORTS */
grid('rep', { view: 'reports', noun: 'reports', one: 'report', defaultSort: { key: 'id', dir: 'asc' },
  all: function () { return DATA.reports; },
  rows: function () { return DATA.reports.filter(function (r) { return matchesQ(r, ['id', 'name', 'category', 'frequency']); }); },
  cell: { lastRun: function (r) { return '<span class="t-cm-label">' + fmtDate(r.lastRun) + '</span>'; },
          act: function (r) { return '<div class="cn-button"><button class="btn tertiary" type="button" data-run="' + r.id + '"' + (r.status === 'Running' ? ' disabled' : '') + '>Run ' + '<span class="visually-hidden">' + esc(r.name) + '</span></button></div>'; } },
  csv: ['id', 'name', 'category', 'frequency', 'lastRun', 'status'] });
var REPORT_SRC = { Liquidity: 'fac', Cash: 'acc', Payments: 'pay', Markets: 'deal', Risk: 'lim', Trade: 'tf', Board: 'acc', Service: 'sr' };
function runReport(r) {
  r.status = 'Running'; renderGrid('rep'); toast('info', 'Running ' + r.name + '…');
  setTimeout(function () {
    r.status = 'Ready'; r.lastRun = dayISO(0); WORK.reports[r.id] = { status: 'Ready', lastRun: r.lastRun }; persistWork();
    var g = REPORT_SRC[r.category]; download(r.id + '-' + r.name.toLowerCase().replace(/[^a-z0-9]+/g, '-') + '-' + DATA.asAt + '.csv', csvOf(g));
    toast('ok', r.name + ' is ready and has downloaded as CSV (' + gridRows(g).length + ' rows, current filters).'); renderGrid('rep');
    var b = document.querySelector('[data-run="' + r.id + '"]'); if (b) { b.focus(); }
  }, 900);
}
document.addEventListener('click', function (e) { var b = e.target.closest && e.target.closest('[data-run]'); if (!b || b.disabled) { return; }
  var r = DATA.reports.filter(function (x) { return x.id === b.getAttribute('data-run'); })[0]; if (r) { runReport(r); } });
function reportMetric(r) {
  var pos = DATA.positions.filter(function (p) { return inScope(p); }), exp = [];
  for (var d = 30 - STATE.days; d < 30; d++) { exp.push(sum(pos, function (p) { return p.gbp * DATA.expWalk[p.region][d]; })); }
  var rel = DATA.payments.filter(function (p) { return inScope(p) && p.status === 'Released'; });
  return { Liquidity: ['Available liquidity (£m)', sliceSeries(liquiditySeries().total)], Cash: ['Cash (£m)', sliceSeries(cashSeries(scopedAccounts()))], Board: ['Cash (£m)', sliceSeries(cashSeries(scopedAccounts()))],
    Payments: ['Payments released (£m)', periodIdx().map(function (d) { return sum(rel.filter(function (p) { return p.created === d; }), function (p) { return p.gbp / 1e6; }); })],
    Markets: ['GBP/USD', DATA.fxSeries.USD.closes.slice(30 - STATE.days)], Risk: ['Total exposure (£m)', exp], Trade: ['Total exposure (£m)', exp],
    Service: ['Available liquidity (£m)', sliceSeries(liquiditySeries().total)] }[r.category];
}
RENDER.reports = function () {
  var cash = sliceSeries(cashSeries(scopedAccounts())), liq = sliceSeries(liquiditySeries().total), pos = DATA.positions.filter(function (p) { return inScope(p); });
  var exp = []; for (var d = 30 - STATE.days; d < 30; d++) { exp.push(sum(pos, function (p) { return p.gbp * DATA.expWalk[p.region][d]; })); }
  var rel = DATA.payments.filter(function (p) { return inScope(p) && p.status === 'Released'; }), relS = periodIdx().map(function (d) { return sum(rel.filter(function (p) { return p.created === d; }), function (p) { return p.gbp / 1e6; }); });
  [['rp-cash', cash, '#/accounts'], ['rp-liq', liq, '#/liquidity'], ['rp-exp', exp, '#/risk'], ['rp-pay', relS, '#/payments?status=Released']].forEach(function (k) {
    var v = k[1], last = k[0] === 'rp-pay' ? sum(v) : v[v.length - 1], dp = k[0] === 'rp-pay' ? deltaPct(sum(v.slice(Math.floor(v.length / 2))), sum(v.slice(0, Math.floor(v.length / 2)))) : deltaPct(v[v.length - 1], v[0]);
    kpi(k[0], { unit: '£', value: grp3(last, 1) + 'm', delta: dp, deltaText: deltaText(dp), per: k[0] === 'rp-pay' ? 'second half vs first' : per(), series: v, href: k[2] });
  });
  var tx = DATA.transactions.filter(function (t) { return inScope(t, 'date'); }), wk = [], pd = periodIdx();
  for (var i = 0; i < pd.length; i += 7) { wk.push(pd.slice(i, i + 7)); }
  chart('rp-weekly', { type: 'butterfly-v', categories: wk.map(function (w) { return 'From ' + shortDate(w[0]); }), categoryLabel: 'Week', unit: '£m', caption: 'Receipts against payments by week, GBP millions',
    series: [{ name: 'Receipts', values: wk.map(function (w) { return r1(sum(tx.filter(function (t) { return w.indexOf(t.date) >= 0 && t.gbp > 0; }), function (t) { return t.gbp / 1e6; })); }) },
             { name: 'Payments', values: wk.map(function (w) { return r1(sum(tx.filter(function (t) { return w.indexOf(t.date) >= 0 && t.gbp < 0; }), function (t) { return -t.gbp / 1e6; })); }) }] },
    { title: 'Receipts against payments, week by week' });
  renderGrid('rep');
};
RECORD.reports = function (id) {
  var r = DATA.reports.filter(function (x) { return x.id === id; })[0]; if (!r) { return false; }
  openDrawer(r.name, dl([['Report', r.id], ['Category', r.category], ['Frequency', r.frequency], ['Last run', fmtDate(r.lastRun)], ['Status', stat(r.status), true]]) +
    head4('Headline trend, last ' + STATE.days + ' days') + '<div class="cn-chart-sparkline" id="rep-spark"></div>' +
    para('Running this report produces a CSV from the prototype data with the current entity, region and date filters applied.'),
    [{ label: 'Run and download', run: function () { closeDrawer(); runReport(r); } }, { label: 'Close', kind: 'secondary' }], recordClosed);
  var m = reportMetric(r), slot = document.getElementById('rep-spark'); slot.setAttribute('data-tpl', 'spark');
  chart('rep-spark-' + r.id, { type: 'spark', categories: days(), categoryLabel: 'Day', markers: true, series: [{ name: m[0], values: m[1].map(function (v) { return Math.round(v * 10000) / 10000; }) }],
    caption: m[0] + ', daily, last ' + STATE.days + ' days' }, { title: m[0] }, slot);
  return true;
};

/* ================================================================ HSBC MESSAGES AND SERVICE REQUESTS */
grid('msg', { view: 'messages', noun: 'messages', one: 'message', defaultSort: { key: 'date', dir: 'desc' },
  all: function () { return DATA.messages; },
  rows: function () { return DATA.messages.filter(function (m) { return inScope(m, 'date') && matchesQ(m, ['id', 'from', 'subject', 'entity', 'status']); }); },
  cell: { date: function (r) { return '<span class="t-cm-label">' + fmtDate(r.date) + '</span>'; } },
  csv: ['id', 'date', 'from', 'subject', 'entity', 'status'] });
grid('sr', { view: 'messages', noun: 'service requests', one: 'service request', defaultSort: { key: 'opened', dir: 'desc' },
  all: function () { return DATA.requests; },
  rows: function () { return DATA.requests.filter(function (r) { return inScope(r, 'opened') && matchesQ(r, ['id', 'category', 'subject', 'entity', 'status']); }); },
  cell: { opened: function (r) { return '<span class="t-cm-label">' + fmtDate(r.opened) + '</span>'; } },
  csv: ['id', 'opened', 'entity', 'category', 'subject', 'status'] });
function newRequest(cat, entity, subject, detail) {
  var sr = { id: 'SR-' + pad(70000 + WORK.newRequests.length + 1, 5), opened: dayISO(0), entity: entity, region: ENT[entity].region, category: cat, subject: subject, status: 'Open', resolvedDays: null, detail: detail };
  WORK.newRequests.push(sr); persistWork(); DATA.requests.unshift(sr); return sr;
}
function raiseRequest(cat, entity, subject) { UI.tab['ms-tabs'] = 'sr'; persistUI(); go('#/messages'); setTimeout(function () { fillSR(cat, entity, subject); }, 50); }
var SR_FORM = document.querySelector('[data-form="sr"]');
function srFormHTML() {
  return '<div class="tpl-panel-head"><h3 class="t-cm-section-label">Raise a service request</h3></div><form class="l-stack" data-gap="l" novalidate id="sr-form">' +
    selectField('category', 'Category', SR_CATS.map(function (c) { return [c, c]; }), '') +
    selectField('entity', 'Entity', DATA.entities.map(function (e) { return [e.id, e.name]; }), STATE.entity !== 'all' ? STATE.entity : '') +
    textField('subject', 'Subject', 'At least 5 characters.', {}) + areaField('detail', 'What do you need?', 'At least 20 characters. Do not include passwords or card numbers.', { max: 600 }) +
    '<div class="l-row" data-gap="m"><div class="cn-button"><button class="btn primary" type="submit">Send request</button></div>' +
    '<div class="cn-button"><button class="btn secondary" type="reset">Clear</button></div></div></form>';
}
function mountSR() {
  SR_FORM.innerHTML = srFormHTML(); var f = document.getElementById('sr-form'); wireForm(f);
  f.addEventListener('reset', function () { setTimeout(mountSR, 0); });
  f.addEventListener('submit', function (e) {
    e.preventDefault(); var ok = true;
    f.querySelectorAll('.is-error').forEach(clearError);
    if (!fieldVal(f, 'category')) { setError(f, 'category', 'Choose a category.'); ok = false; }
    if (!fieldVal(f, 'entity')) { setError(f, 'entity', 'Choose the entity this is for.'); ok = false; }
    if (fieldVal(f, 'subject').length < 5) { setError(f, 'subject', 'Write a subject of at least 5 characters.'); ok = false; }
    var d = fieldVal(f, 'detail');
    if (d.length < 20) { setError(f, 'detail', 'Describe what you need in at least 20 characters.'); ok = false; }
    else if (/\d{12,19}/.test(d.replace(/[\s-]/g, ''))) { setError(f, 'detail', 'This looks like a card or account number. Remove it; HSBC will never ask for it here.'); ok = false; }
    if (!ok) { focusFirstError(f); return; }
    var sr = newRequest(fieldVal(f, 'category'), fieldVal(f, 'entity'), fieldVal(f, 'subject'), d);
    toast('ok', 'Service request ' + sr.id + ' sent to HSBC (simulated).');
    UI.tab['ms-tabs'] = 'sr'; persistUI(); mountSR(); renderView(); selectTab(document.querySelector('[data-tabs="ms-tabs"]'), 'sr');
    var link = document.querySelector('#dg-sr a[href="#/messages/' + sr.id + '"]'); if (link) { link.focus(); }
  });
}
function fillSR(cat, entity, subject) {
  var f = document.getElementById('sr-form'); if (!f) { return; }
  var c = f.querySelector('[data-field="category"]'); c.setAttribute('data-value', cat); c.__set(cat);
  var e = f.querySelector('[data-field="entity"]'); e.setAttribute('data-value', entity); e.__set(entity);
  var s = f.querySelector('[data-field="subject"] input'); s.value = subject; f.querySelector('[data-field="detail"] textarea').focus();
}
RENDER.messages = function () {
  var ms = DATA.messages.filter(function (m) { return inScope(m); }), rs = DATA.requests.filter(function (r) { return inScope(r); }), pd = periodIdx();
  var openR = rs.filter(function (r) { return r.status !== 'Resolved'; }), res = rs.filter(function (r) { return r.resolvedDays; });
  kpi('ms-unread', { unit: '', value: String(ms.filter(function (m) { return m.status === 'Unread'; }).length), delta: 0, dir: 'flat', deltaText: ms.length + ' in total', per: '',
    series: pd.map(function (d) { return ms.filter(function (m) { return m.date <= d && m.status === 'Unread'; }).length; }), href: '#/messages?tab=msg' });
  kpi('ms-open', { unit: '', value: String(openR.length), delta: 0, dir: 'flat', deltaText: rs.length + ' raised', per: '',
    series: pd.map(function (d) { return openR.filter(function (r) { return r.opened <= d; }).length; }), href: '#/messages?tab=sr' });
  var you = ms.filter(function (m) { return m.status === 'Awaiting your reply'; }).length + rs.filter(function (r) { return r.status === 'Awaiting you'; }).length;
  kpi('ms-you', { unit: '', value: String(you), delta: 0, dir: 'flat', deltaText: 'messages and requests', per: '',
    series: pd.map(function (d) { return ms.filter(function (m) { return m.date <= d && m.status === 'Awaiting your reply'; }).length + rs.filter(function (r) { return r.opened <= d && r.status === 'Awaiting you'; }).length; }), href: '#/messages' });
  var avg = res.length ? sum(res, function (r) { return r.resolvedDays; }) / res.length : 0;
  kpi('ms-days', { unit: '', value: res.length ? (Math.round(avg * 10) / 10) + ' days' : '—', delta: 0, dir: 'flat', deltaText: res.length + ' resolved', per: '',
    series: pd.map(function (d) { var rr = res.filter(function (r) { return r.opened <= d; }); return rr.length ? sum(rr, function (r) { return r.resolvedDays; }) / rr.length : 0; }), href: '#/messages?tab=sr' });
  var cats = SR_CATS.filter(function (c) { return openR.some(function (r) { return r.category === c; }); });
  if (cats.length) {
    chart('ms-cat', { type: 'donut', categories: cats, categoryLabel: 'Category', series: [{ name: 'Open requests', values: cats.map(function (c) { return openR.filter(function (r) { return r.category === c; }).length; }) }],
      caption: 'Open service requests by category, count' }, { title: 'Open requests by category' });
  }
  if (!document.getElementById('sr-form')) { mountSR(); }
  renderGrid('msg'); renderGrid('sr');
};
RECORD.messages = function (id) {
  var m = DATA.messages.filter(function (x) { return x.id === id; })[0], r = DATA.requests.filter(function (x) { return x.id === id; })[0];
  if (m) {
    if (m.status === 'Unread') { m.status = 'Read'; WORK.messages[m.id] = { status: 'Read', thread: m.thread }; persistWork(); renderView(); }
    openDrawer(m.subject, dl([['From', m.from], ['Received', fmtDate(m.date)], ['Entity', entName(m.entity)], ['Status', stat(m.status), true]]) + para(m.body) +
      head4('Your replies') + auditHTML(m.thread) + '<div id="reply-box">' + areaField('reply', 'Reply', 'At least 5 characters. Simulated; nothing is sent.', { max: 1000 }) + '</div>',
      [{ label: 'Send reply', run: function () {
          var box = document.getElementById('reply-box'), t = fieldVal(box, 'reply');
          if (t.length < 5) { setError(box, 'reply', 'Write a reply of at least 5 characters.'); focusFirstError(box); return; }
          m.thread.push({ at: dayISO(0), who: 'You (CEO)', note: t }); m.status = 'Read';
          WORK.messages[m.id] = { status: m.status, thread: m.thread }; persistWork(); toast('ok', 'Reply sent to ' + m.from.split(' — ')[0] + ' (simulated).');
          renderView(); RECORD.messages(m.id); } },
       { label: 'Close', kind: 'secondary' }], recordClosed);
    wireForm(document.getElementById('reply-box'));
    return true;
  }
  if (r) {
    openDrawer(r.subject, dl([['Request', r.id], ['Status', stat(r.status), true], ['Category', r.category], ['Entity', entName(r.entity)], ['Opened', fmtDate(r.opened)],
      ['Resolution', r.resolvedDays ? r.resolvedDays + ' days' : 'Not resolved yet']]) + para(r.detail), [{ label: 'Close', kind: 'secondary' }], recordClosed);
    return true;
  }
  return false;
};

/* ================================================================ SETTINGS */
var PREFS = load('ceo.prefs', { notifyApprovals: true, notifyExceptions: true, notifyMessages: false });
RENDER.settings = function () {
  var box = document.querySelector('[data-form="settings"]'); if (box.__done) { syncSettings(); return; } box.__done = true;
  function sw(key, label) { return '<div class="field"><input type="checkbox" role="switch" id="pref-' + key + '" data-pref="' + key + '"' + (PREFS[key] ? ' checked' : '') + '><label for="pref-' + key + '"><span class="switch"><span class="thumb"></span></span> ' + esc(label) + '</label></div>'; }
  box.innerHTML = '<div class="tpl-panel-head"><h3 class="t-cm-section-label">Preferences</h3></div><div class="l-stack" data-gap="l">' +
    '<div class="l-stack" data-gap="s"><span class="t-cm-label" id="set-theme-l">Theme</span><div class="cn-segmented-control"><div class="seg md" role="group" aria-labelledby="set-theme-l"><span class="ind" aria-hidden="true"></span>' +
    '<button type="button" aria-pressed="true" data-theme-set="light">Light</button><button type="button" aria-pressed="false" data-theme-set="dark">Dark</button></div></div></div>' +
    selectField('defEntity', 'Entity filter when the prototype opens', [['all', 'All entities']].concat(DATA.entities.map(function (e) { return [e.id, e.name]; })), STATE.entity) +
    '<div class="l-stack" data-gap="s"><span class="t-cm-label">Notify me about</span><div class="cn-selection-controls">' +
    sw('notifyApprovals', 'Payments waiting for my approval') + sw('notifyExceptions', 'Material risk exceptions') + sw('notifyMessages', 'New messages from HSBC') + '</div></div>' +
    '<div class="l-row" data-gap="m"><div class="cn-button"><button class="btn secondary" type="button" data-reset>Reset prototype data</button></div></div></div>';
  wireForm(box);
  box.querySelector('[data-field="defEntity"]').addEventListener('click', function (e) { var o = e.target.closest('[role=option]'); if (!o) { return; }
    STATE.entity = o.getAttribute('data-value'); if (STATE.entity !== 'all') { STATE.region = 'all'; } refilter(); toast('ok', 'Entity filter set to ' + (STATE.entity === 'all' ? 'all entities' : entName(STATE.entity)) + '.'); });
  box.addEventListener('change', function (e) { var c = e.target.closest('[data-pref]'); if (!c) { return; } PREFS[c.getAttribute('data-pref')] = c.checked; save('ceo.prefs', PREFS);
    toast('ok', 'Preference saved in this browser.'); });
  box.addEventListener('click', function (e) {
    var t = e.target.closest('[data-theme-set]'); if (t) { setTheme(t.getAttribute('data-theme-set')); }
    if (e.target.closest('[data-reset]')) { openModal({ title: 'Reset prototype data?', text: 'Approvals, acknowledgements, requests, replies, deals, drawdowns and preferences made in this browser will be cleared. The page then reloads.',
      confirm: 'Reset and reload', onConfirm: function () { ['ceo.work', 'ceo.ui', 'ceo.filters', 'ceo.prefs', 'ceo.theme'].forEach(function (k) { try { localStorage.removeItem(k); } catch (x) {} });
        location.hash = '#/overview'; location.reload(); return true; } }); }
  });
  syncSettings();
};
function syncSettings() { var t = document.documentElement.getAttribute('data-theme');
  document.querySelectorAll('[data-theme-set]').forEach(function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-theme-set') === t)); });
  var d = document.querySelector('[data-form="settings"] [data-field="defEntity"]'); if (d && d.__set) { d.__set(STATE.entity); } requestAnimationFrame(placeAll); }

/* ================================================================ boot */
VIEWS.forEach(function (v) { var s = document.querySelector('.ceo-view[data-view="' + v + '"]'); TITLES[v] = { title: s.getAttribute('data-title'), lede: s.getAttribute('data-lede') }; });
/* The chart engine blocks are inlined AFTER this script (so the icon-source gate's <svg>…</svg> scan
   cannot pair a prose "<svg" inside the engine with a later "</svg>"); boot waits for them. */
function boot() {
  setTheme(document.documentElement.getAttribute('data-theme') || 'light');
  if (!location.hash) { history.replaceState(null, '', '#/overview'); }
  onRoute();
}
if (document.readyState === 'loading') { document.addEventListener('DOMContentLoaded', boot); } else { boot(); }
window.CEO = { DATA: DATA, STATE: STATE, GRIDS: GRIDS, gridRows: gridRows };
}());
