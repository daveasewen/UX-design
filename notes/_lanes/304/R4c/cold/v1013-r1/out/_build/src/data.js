/* ===== DATA — the ONE in-page dataset (ADS-generate-from-canon rule 13). Authored, illustrative.
   Every KPI, chart, grid, filter option and drawer on every page reads from this object; nothing is
   typed twice into the HTML. Deterministic: a seeded PRNG, so every page and every reload sees the
   same numbers. No live banking connection; all entities, counterparties and figures are invented.
   FX: GBP reporting. Rates are ILLUSTRATIVE, fixed, quoted as units of currency per 1 GBP, as at the
   AS_OF close. They are not market data. ===== */
const DATA = (function () {
  'use strict';
  function rng(seed) { return function () { seed |= 0; seed = seed + 0x6D2B79F5 | 0; var t = Math.imul(seed ^ seed >>> 15, 1 | seed); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
  var R = rng(20260925);
  function pick(a) { return a[Math.floor(R() * a.length)]; }
  function between(a, b) { return a + R() * (b - a); }
  function round(v, d) { var k = Math.pow(10, d || 0); return Math.round(v * k) / k; }
  function iso(d) { return d.toISOString().slice(0, 10); }

  var AS_OF = '2026-09-25';
  var AS_OF_TIME = '17:00 BST';
  var DAYS = [];
  (function () { var end = new Date(AS_OF + 'T12:00:00Z'); for (var i = 29; i >= 0; i--) { var d = new Date(end); d.setUTCDate(end.getUTCDate() - i); DAYS.push(iso(d)); } }());
  var SESSIONS = DAYS.filter(function (d) { var w = new Date(d + 'T12:00:00Z').getUTCDay(); return w !== 0 && w !== 6; });

  var FX = { GBP: 1, EUR: 1.1712, USD: 1.2745, SGD: 1.7130, HKD: 9.9310, AED: 4.6810, MXN: 23.4100, CNY: 9.1840 };
  var CCYS = Object.keys(FX);

  var REGIONS = [
    { id: 'uk', name: 'United Kingdom' }, { id: 'eu', name: 'Europe' }, { id: 'am', name: 'Americas' },
    { id: 'ap', name: 'Asia-Pacific' }, { id: 'me', name: 'Middle East' }
  ];
  var ENTITIES = [
    { id: 'HLH', name: 'Harbourline Holdings UK Ltd', short: 'Holdings UK', region: 'uk', ccy: 'GBP', country: 'United Kingdom' },
    { id: 'HLE', name: 'Harbourline Europe BV', short: 'Europe BV', region: 'eu', ccy: 'EUR', country: 'Netherlands' },
    { id: 'HLG', name: 'Harbourline Logistics GmbH', short: 'Logistics GmbH', region: 'eu', ccy: 'EUR', country: 'Germany' },
    { id: 'HLU', name: 'Harbourline Trading Inc', short: 'Trading Inc', region: 'am', ccy: 'USD', country: 'United States' },
    { id: 'HLM', name: 'Harbourline Mexico SA de CV', short: 'Mexico SA', region: 'am', ccy: 'MXN', country: 'Mexico' },
    { id: 'HLS', name: 'Harbourline Asia Pte Ltd', short: 'Asia Pte', region: 'ap', ccy: 'SGD', country: 'Singapore' },
    { id: 'HLK', name: 'Harbourline Hong Kong Ltd', short: 'Hong Kong Ltd', region: 'ap', ccy: 'HKD', country: 'Hong Kong SAR' },
    { id: 'HLC', name: 'Harbourline (Shanghai) Co Ltd', short: 'Shanghai Co', region: 'ap', ccy: 'CNY', country: 'China' },
    { id: 'HLA', name: 'Harbourline Middle East FZE', short: 'Middle East FZE', region: 'me', ccy: 'AED', country: 'United Arab Emirates' }
  ];
  var ENT = {}; ENTITIES.forEach(function (e) { ENT[e.id] = e; });
  function toGBP(v, ccy) { return v / FX[ccy]; }

  /* ---------- accounts, with a 30-day closing-balance series in local currency */
  var ACCT_TYPES = ['Operating', 'Collections', 'Payroll', 'Deposit'];
  var SIZE = { HLH: 260e6, HLE: 140e6, HLG: 70e6, HLU: 210e6, HLM: 900e6, HLS: 120e6, HLK: 520e6, HLC: 310e6, HLA: 160e6 };
  var ACCOUNTS = [], n = 0;
  ENTITIES.forEach(function (e) {
    var types = e.id === 'HLH' || e.id === 'HLU' ? ACCT_TYPES : ACCT_TYPES.slice(0, 3);
    types.forEach(function (t, i) {
      var ccy = e.ccy; if (t === 'Collections' && (e.region === 'ap' || e.region === 'me')) { ccy = 'USD'; }
      var base = SIZE[e.id] * [0.46, 0.28, 0.08, 0.36][i] * (ccy === e.ccy ? 1 : FX.USD / FX[e.ccy]);
      var bal = [], v = base * between(0.9, 1.05), drift = between(-0.004, 0.009);
      for (var d = 0; d < 30; d++) { v = Math.max(base * 0.35, v * (1 + drift + between(-0.03, 0.03))); if (t === 'Payroll' && d % 14 === 9) { v *= 0.55; } bal.push(round(v, 2)); }
      n++;
      ACCOUNTS.push({ id: 'AC' + String(n).padStart(3, '0'), entity: e.id, type: t, ccy: ccy, name: e.short + ' ' + t.toLowerCase(),
        number: '•••• ' + String(1000 + Math.floor(R() * 8999)), bank: 'HSBC ' + e.country, balances: bal,
        overdraft: t === 'Operating' ? round(base * 0.1, -3) : 0 });
    });
  });

  /* ---------- committed and uncommitted facilities (drawn series moves a little) */
  var FACILITIES = [
    { id: 'FAC-01', entity: 'HLH', name: 'Syndicated revolving credit facility', type: 'Revolving credit', ccy: 'GBP', limit: 500e6, drawn: 120e6, committed: true, maturity: '2029-06-30', margin: 'SONIA + 1.35%' },
    { id: 'FAC-02', entity: 'HLH', name: 'Commercial paper programme', type: 'Commercial paper', ccy: 'GBP', limit: 300e6, drawn: 90e6, committed: false, maturity: '2027-03-31', margin: 'Issued at discount' },
    { id: 'FAC-03', entity: 'HLU', name: 'US dollar term loan', type: 'Term loan', ccy: 'USD', limit: 300e6, drawn: 300e6, committed: true, maturity: '2028-09-15', margin: 'SOFR + 1.60%' },
    { id: 'FAC-04', entity: 'HLE', name: 'Euro revolving facility', type: 'Revolving credit', ccy: 'EUR', limit: 150e6, drawn: 40e6, committed: true, maturity: '2028-12-31', margin: 'EURIBOR + 1.25%' },
    { id: 'FAC-05', entity: 'HLS', name: 'Asia working capital line', type: 'Working capital', ccy: 'SGD', limit: 200e6, drawn: 85e6, committed: true, maturity: '2027-11-30', margin: 'SORA + 1.40%' },
    { id: 'FAC-06', entity: 'HLK', name: 'Hong Kong trade line', type: 'Trade line', ccy: 'HKD', limit: 800e6, drawn: 310e6, committed: false, maturity: '2027-04-30', margin: 'HIBOR + 1.10%' },
    { id: 'FAC-07', entity: 'HLA', name: 'Dirham overdraft', type: 'Overdraft', ccy: 'AED', limit: 150e6, drawn: 12e6, committed: false, maturity: '2027-01-31', margin: 'EIBOR + 1.75%' },
    { id: 'FAC-08', entity: 'HLM', name: 'Peso working capital line', type: 'Working capital', ccy: 'MXN', limit: 1200e6, drawn: 640e6, committed: true, maturity: '2027-08-31', margin: 'TIIE + 1.90%' },
    { id: 'FAC-09', entity: 'HLG', name: 'Euro asset finance', type: 'Term loan', ccy: 'EUR', limit: 60e6, drawn: 48e6, committed: true, maturity: '2030-05-31', margin: 'EURIBOR + 1.55%' }
  ];
  FACILITIES.forEach(function (f) {
    var s = [], v = f.drawn * between(0.85, 1.0);
    for (var d = 0; d < 30; d++) { v = Math.min(f.limit, Math.max(0, v + f.limit * between(-0.012, 0.014))); s.push(round(d === 29 ? f.drawn : v, 0)); }
    f.drawnSeries = s;
  });
  var POLICY_BUFFER_GBP = 400e6;
  var COMMITMENTS = [
    { id: 'CM-1', entity: 'HLH', name: 'Interim dividend', ccy: 'GBP', amount: 180e6, due: '2026-10-23' },
    { id: 'CM-2', entity: 'HLG', name: 'Warehouse automation capex', ccy: 'EUR', amount: 64e6, due: '2026-11-14' },
    { id: 'CM-3', entity: 'HLU', name: 'Bond coupon', ccy: 'USD', amount: 21e6, due: '2026-10-15' },
    { id: 'CM-4', entity: 'HLS', name: 'Acquisition deposit', ccy: 'SGD', amount: 95e6, due: '2026-12-01' },
    { id: 'CM-5', entity: 'HLM', name: 'Fleet renewal', ccy: 'MXN', amount: 410e6, due: '2026-11-28' }
  ];

  /* ---------- transactions — 30 days, enough rows to sort, filter and page */
  var CPTY = {
    uk: ['Kestrel Freight Ltd', 'Albion Packaging plc', 'Thameside Estates', 'HMRC', 'Northgate Utilities', 'Brightwater Foods'],
    eu: ['Rhein Logistik AG', 'Lumière Distribution SA', 'Delta Haven BV', 'Iberia Cargo SL', 'Nordlicht Energie'],
    am: ['Great Lakes Supply Co', 'Pacific Rim Traders', 'Lone Star Components', 'Sierra Madre Transportes', 'Hudson Ridge Retail'],
    ap: ['Jade Harbour Shipping', 'Straits Electronics Pte', 'Pearl River Textiles', 'Kowloon Terminals', 'Lion City Foods'],
    me: ['Gulf Horizon Trading', 'Dubai Creek Logistics', 'Arabian Sands Construction', 'Emirates Cold Chain']
  };
  var CATS = [
    { k: 'Customer receipt', dir: 1, w: 34 }, { k: 'Supplier payment', dir: -1, w: 30 }, { k: 'Payroll', dir: -1, w: 7 },
    { k: 'Tax', dir: -1, w: 4 }, { k: 'Intercompany', dir: 0, w: 10 }, { k: 'FX settlement', dir: 0, w: 8 },
    { k: 'Loan interest', dir: -1, w: 3 }, { k: 'Trade settlement', dir: -1, w: 4 }
  ];
  function wcat() { var t = R() * 100, a = 0; for (var i = 0; i < CATS.length; i++) { a += CATS[i].w; if (t < a) { return CATS[i]; } } return CATS[0]; }
  var TRANSACTIONS = [];
  for (var i = 0; i < 360; i++) {
    var ac = pick(ACCOUNTS), e = ENT[ac.entity], c = wcat(), dir = c.dir || (R() < 0.5 ? 1 : -1);
    var scale = SIZE[e.id] / 400 * (ac.ccy === e.ccy ? 1 : FX.USD / FX[e.ccy]);
    var amt = round(dir * scale * Math.exp(between(-2.2, 1.4)), 2);
    var day = DAYS[Math.floor(R() * 30)];
    var cp = c.k === 'Tax' ? (e.region === 'uk' ? 'HMRC' : 'Tax authority ' + e.country) : c.k === 'Payroll' ? 'Payroll bureau' :
      c.k === 'Intercompany' ? pick(ENTITIES.filter(function (x) { return x.id !== e.id; })).name : c.k === 'Loan interest' ? 'HSBC facility agent' : pick(CPTY[e.region]);
    TRANSACTIONS.push({ id: 'TX' + String(80000 + i * 7), date: day, entity: e.id, account: ac.id, counterparty: cp, category: c.k,
      ccy: ac.ccy, amount: amt, gbp: round(toGBP(amt, ac.ccy), 2), status: day >= DAYS[27] && R() < 0.35 ? 'Pending' : 'Settled',
      ref: (c.k === 'Customer receipt' ? 'INV-' : c.k === 'Supplier payment' ? 'PO-' : 'REF-') + String(Math.floor(between(10000, 99999))) });
  }
  TRANSACTIONS.sort(function (a, b) { return a.date < b.date ? 1 : -1; });

  /* ---------- payments awaiting / through approval */
  var PAY_TYPES = ['Supplier payment', 'Intercompany funding', 'Treasury deal settlement', 'Dividend', 'Tax payment', 'Capital expenditure'];
  var BENE = ['Rhein Logistik AG', 'Jade Harbour Shipping', 'Great Lakes Supply Co', 'Albion Packaging plc', 'Gulf Horizon Trading',
    'Straits Electronics Pte', 'Lumière Distribution SA', 'Sierra Madre Transportes', 'Kowloon Terminals', 'Nordlicht Energie', 'Harbourline Asia Pte Ltd', 'Harbourline Trading Inc'];
  var INITIATORS = ['A. Mensah (Group treasury)', 'L. Fischer (Europe finance)', 'R. Tan (Asia treasury)', 'J. Ortega (Americas finance)', 'S. Haddad (ME finance)'];
  var STATUS_PLAN = [].concat(Array(12).fill('Awaiting your approval'), Array(6).fill('Awaiting second approver'), Array(9).fill('Approved'),
    Array(14).fill('Released'), Array(3).fill('Rejected'), Array(4).fill('Held for screening'));
  var PAYMENTS = STATUS_PLAN.map(function (st, i) {
    var e = pick(ENTITIES), ccy = R() < 0.7 ? e.ccy : pick(['USD', 'EUR', 'GBP']);
    var gbp = Math.exp(between(Math.log(0.4e6), Math.log(38e6)));
    if (i === 0) { gbp = 42.5e6; } if (i === 3) { gbp = 18.2e6; }
    var amt = round(gbp * FX[ccy], 2), off = Math.floor(between(-6, 12));
    var vd = new Date(AS_OF + 'T12:00:00Z'); vd.setUTCDate(vd.getUTCDate() + (/Released|Rejected/.test(st) ? -Math.abs(off) - 1 : Math.abs(off) + 1));
    var created = new Date(AS_OF + 'T12:00:00Z'); created.setUTCDate(created.getUTCDate() - Math.floor(between(0, 9)));
    var type = i === 0 ? 'Dividend' : pick(PAY_TYPES), bene = type === 'Dividend' ? 'Registrar — shareholder account' : pick(BENE);
    var flags = [];
    if (gbp > 10e6) { flags.push('Above £10m dual-control threshold'); }
    if (R() < 0.18) { flags.push('New beneficiary'); }
    if (st === 'Held for screening') { flags.push('Sanctions screening hold'); }
    return { id: 'PAY-26-' + String(4100 + i * 3), entity: e.id, beneficiary: bene, type: type, ccy: ccy, amount: amt, gbp: round(toGBP(amt, ccy), 2),
      valueDate: iso(vd), created: iso(created), initiator: pick(INITIATORS), approvals: gbp > 10e6 ? 2 : 1, status: st, flags: flags,
      purpose: type + ' — ' + bene };
  });

  /* ---------- risk: positions by entity × currency, limits and exceptions */
  var POS_TYPES = ['Cash', 'Receivables', 'Payables', 'Hedges', 'Borrowings'];
  var POSITIONS = [];
  ENTITIES.forEach(function (e) {
    var ccys = [e.ccy].concat(e.ccy === 'USD' ? ['MXN'] : ['USD']).concat(e.region === 'eu' ? ['GBP'] : e.region === 'ap' ? ['CNY'] : []);
    ccys.forEach(function (ccy, ci) {
      POS_TYPES.forEach(function (pt) {
        var mag = SIZE[e.id] / FX[e.ccy] * [0.9, 0.55, 0.25][ci] * { Cash: 0.5, Receivables: 0.6, Payables: -0.45, Hedges: -0.25, Borrowings: -0.3 }[pt] * between(0.6, 1.3);
        if (pt === 'Hedges' && ccy === e.ccy) { return; }
        POSITIONS.push({ id: 'POS-' + e.id + '-' + ccy + '-' + pt.slice(0, 3).toUpperCase(), entity: e.id, ccy: ccy, type: pt, gbp: round(mag, 0),
          local: round(mag * FX[ccy], 0), tenor: pick(['Spot', '1M', '3M', '6M', '12M']) });
      });
    });
  });
  var REGION_LIMITS = { uk: 900e6, eu: 520e6, am: 640e6, ap: 700e6, me: 200e6 };
  var CCY_LIMITS = { GBP: 1200e6, EUR: 420e6, USD: 520e6, SGD: 140e6, HKD: 180e6, AED: 120e6, MXN: 90e6, CNY: 110e6 };
  var COUNTERPARTIES = [
    { id: 'CP-01', name: 'Northbridge Bank', rating: 'AA-', limit: 250e6, exposure: 171e6, region: 'uk' },
    { id: 'CP-02', name: 'Crestmark Capital', rating: 'A+', limit: 180e6, exposure: 166e6, region: 'eu' },
    { id: 'CP-03', name: 'Meridian Trust', rating: 'A', limit: 120e6, exposure: 64e6, region: 'am' },
    { id: 'CP-04', name: 'Aldgate Securities', rating: 'A-', limit: 90e6, exposure: 94e6, region: 'uk' },
    { id: 'CP-05', name: 'Pacific Crown Bank', rating: 'A+', limit: 160e6, exposure: 118e6, region: 'ap' },
    { id: 'CP-06', name: 'Gulfstar Bank', rating: 'A', limit: 80e6, exposure: 57e6, region: 'me' },
    { id: 'CP-07', name: 'Lumen Bank AG', rating: 'AA', limit: 200e6, exposure: 88e6, region: 'eu' },
    { id: 'CP-08', name: 'Riverside Savings', rating: 'BBB+', limit: 40e6, exposure: 37e6, region: 'am' },
    { id: 'CP-09', name: 'Harbour Pacific Bank', rating: 'A-', limit: 70e6, exposure: 29e6, region: 'ap' },
    { id: 'CP-10', name: 'Sterling Crescent Bank', rating: 'AA-', limit: 150e6, exposure: 112e6, region: 'uk' }
  ];
  COUNTERPARTIES.forEach(function (c) { var s = [], v = c.exposure * between(0.8, 1.0); for (var d = 0; d < 30; d++) { v = Math.max(0, v * (1 + between(-0.04, 0.045))); s.push(round(d === 29 ? c.exposure : v, 0)); } c.series = s; });
  var EXCEPTIONS = [
    { id: 'EXC-2609-01', type: 'Counterparty limit breach', severity: 'Material', entity: 'HLH', title: 'Aldgate Securities exposure above limit', value: 94e6, limit: 90e6, raised: '2026-09-24', owner: 'Group treasury', detail: 'Money-market deposits placed on 23 Sep took exposure to 104% of the approved limit. Treasury proposes to roll £10m to Northbridge Bank at maturity on 30 Sep.' },
    { id: 'EXC-2609-02', type: 'Currency limit near breach', severity: 'Material', entity: 'HLU', title: 'Net Mexican peso position at 96% of limit', value: 86.4e6, limit: 90e6, raised: '2026-09-23', owner: 'Americas finance', detail: 'Receivables growth in Mexico has outpaced forward hedging. Hedge ratio is 52% against a 70% policy floor.' },
    { id: 'EXC-2609-03', type: 'Unhedged exposure above policy', severity: 'High', entity: 'HLS', title: 'Singapore dollar acquisition deposit unhedged', value: 55.5e6, limit: 40e6, raised: '2026-09-22', owner: 'Asia treasury', detail: 'The SGD 95m acquisition deposit due 1 Dec is not yet covered by a forward. Policy requires cover once a commitment is signed.' },
    { id: 'EXC-2609-04', type: 'Counterparty limit near breach', severity: 'High', entity: 'HLE', title: 'Crestmark Capital at 92% of limit', value: 166e6, limit: 180e6, raised: '2026-09-21', owner: 'Europe finance', detail: 'Euro cash sweeping concentrates balances with one counterparty. A second sweep bank is being onboarded.' },
    { id: 'EXC-2609-05', type: 'Covenant headroom', severity: 'Material', entity: 'HLM', title: 'Mexico leverage covenant headroom below 10%', value: 2.71, limit: 3.0, raised: '2026-09-19', owner: 'Americas finance', detail: 'Net debt to EBITDA of 2.71x against a 3.00x covenant on the peso working capital line. Fleet renewal would reduce headroom further.' },
    { id: 'EXC-2609-06', type: 'Sanctions screening hold', severity: 'High', entity: 'HLA', title: 'Payment held — beneficiary name match', value: 3.2e6, limit: 0, raised: '2026-09-24', owner: 'Compliance', detail: 'A supplier payment to Gulf Horizon Trading is held pending a false-positive review of a partial name match.' },
    { id: 'EXC-2609-07', type: 'Regional limit near breach', severity: 'Medium', entity: 'HLK', title: 'Asia-Pacific exposure at 88% of regional limit', value: 616e6, limit: 700e6, raised: '2026-09-18', owner: 'Asia treasury', detail: 'Seasonal inventory build in Hong Kong and Shanghai. Expected to unwind by mid-November.' },
    { id: 'EXC-2609-08', type: 'KYC document overdue', severity: 'Medium', entity: 'HLC', title: 'Shanghai entity KYC refresh overdue', value: 0, limit: 0, raised: '2026-09-15', owner: 'Legal entity management', detail: 'Updated beneficial ownership declaration requested by HSBC on 1 Sep is outstanding.' },
    { id: 'EXC-2609-09', type: 'Counterparty rating change', severity: 'Medium', entity: 'HLU', title: 'Riverside Savings downgraded to BBB+', value: 37e6, limit: 40e6, raised: '2026-09-17', owner: 'Group treasury', detail: 'Policy limits BBB-rated counterparties to £25m. Current exposure of £37m requires reduction or a policy waiver.' },
    { id: 'EXC-2609-10', type: 'Facility utilisation', severity: 'Medium', entity: 'HLG', title: 'Euro asset finance 80% drawn', value: 48e6, limit: 60e6, raised: '2026-09-12', owner: 'Europe finance', detail: 'Headroom on the asset finance line is €12m ahead of the warehouse automation programme.' },
    { id: 'EXC-2609-11', type: 'Intraday overdraft', severity: 'Medium', entity: 'HLA', title: 'Dirham account overdrawn intraday on three days', value: 4.1e6, limit: 0, raised: '2026-09-10', owner: 'ME finance', detail: 'Payroll funding arrived after the payroll run on 5, 8 and 9 Sep.' },
    { id: 'EXC-2609-12', type: 'Unhedged exposure above policy', severity: 'Material', entity: 'HLC', title: 'Renminbi receivables hedge ratio at 38%', value: 71e6, limit: 50e6, raised: '2026-09-20', owner: 'Asia treasury', detail: 'Onshore hedging capacity is constrained; an offshore non-deliverable forward proposal is with the treasury committee.' }
  ];

  /* ---------- FX: 30-day OHLC per pair, closing on the illustrative fixing */
  var FX_SERIES = {};
  CCYS.filter(function (c) { return c !== 'GBP'; }).forEach(function (c) {
    var close = FX[c], v = close * between(0.97, 1.03), rows = [];
    SESSIONS.forEach(function (d, k) {
      var o = v, last = k === SESSIONS.length - 1, cl = last ? close : o * (1 + between(-0.006, 0.006));
      var hi = Math.max(o, cl) * (1 + between(0.0005, 0.004)), lo = Math.min(o, cl) * (1 - between(0.0005, 0.004));
      rows.push({ date: d, open: round(o, 4), high: round(hi, 4), low: round(lo, 4), close: round(cl, 4) }); v = cl;
    });
    FX_SERIES[c] = rows;
  });
  var HEDGES = [];
  for (var h = 0; h < 28; h++) {
    var he = pick(ENTITIES.filter(function (x) { return x.ccy !== 'GBP'; })), hc = pick([he.ccy, 'USD', 'EUR']);
    if (hc === 'GBP') { hc = 'USD'; }
    var hm = new Date(AS_OF + 'T12:00:00Z'); hm.setUTCDate(hm.getUTCDate() + Math.floor(between(5, 330)));
    var notional = round(Math.exp(between(Math.log(2e6), Math.log(60e6))) * FX[hc], -3);
    HEDGES.push({ id: 'FWD-' + String(7700 + h * 11), entity: he.id, ccy: hc, direction: R() < 0.6 ? 'Sell ' + hc + ' / buy GBP' : 'Buy ' + hc + ' / sell GBP',
      notional: notional, gbp: round(toGBP(notional, hc), 0), rate: round(FX[hc] * between(0.985, 1.015), 4), maturity: iso(hm),
      mtm: round(toGBP(notional, hc) * between(-0.03, 0.03), 0), counterparty: pick(['HSBC Bank plc', 'HSBC Bank USA', 'HSBC Singapore', 'HSBC Hong Kong']) });
  }

  /* ---------- trade finance instruments */
  var TF_TYPES = ['Import letter of credit', 'Export letter of credit', 'Standby letter of credit', 'Bank guarantee', 'Documentary collection'];
  var TF_STATUS = ['Issued', 'Issued', 'Documents presented', 'Discrepancy raised', 'Amendment requested', 'Settled', 'Expiring soon'];
  var TRADE = [];
  for (var t = 0; t < 40; t++) {
    var te = pick(ENTITIES), tt = pick(TF_TYPES), tc = pick([te.ccy, 'USD', 'USD', 'EUR']);
    var issued = new Date(AS_OF + 'T12:00:00Z'); issued.setUTCDate(issued.getUTCDate() - Math.floor(between(3, 150)));
    var expiry = new Date(issued); expiry.setUTCDate(expiry.getUTCDate() + Math.floor(between(60, 300)));
    var tamt = round(Math.exp(between(Math.log(0.3e6), Math.log(22e6))) * FX[tc], -2), ts = pick(TF_STATUS);
    var prefix = { 'Import letter of credit': 'ILC', 'Export letter of credit': 'ELC', 'Standby letter of credit': 'SBLC', 'Bank guarantee': 'BG', 'Documentary collection': 'DC' }[tt];
    var region = te.region, cp = pick(CPTY[pick(['uk', 'eu', 'am', 'ap', 'me'])]);
    var ev = [{ date: iso(issued), title: 'Application approved and ' + (tt === 'Documentary collection' ? 'collection lodged' : 'instrument issued'), tone: 'ok' }];
    var mid = new Date(issued); mid.setUTCDate(mid.getUTCDate() + 20);
    if (ts !== 'Issued' && ts !== 'Expiring soon') { ev.push({ date: iso(mid), title: 'Shipping documents received by HSBC', tone: 'inf' }); }
    if (ts === 'Discrepancy raised') { ev.push({ date: iso(mid), title: 'Discrepancy: late shipment date on bill of lading', tone: 'warn' }); }
    if (ts === 'Amendment requested') { ev.push({ date: iso(mid), title: 'Beneficiary requested an expiry extension', tone: 'warn' }); }
    if (ts === 'Settled') { ev.push({ date: iso(mid), title: 'Payment settled to beneficiary', tone: 'ok' }); }
    TRADE.push({ id: prefix + '-' + String(55000 + t * 13), type: tt, entity: te.id, counterparty: cp, ccy: tc, amount: tamt, gbp: round(toGBP(tamt, tc), 0),
      issued: iso(issued), expiry: iso(expiry), status: ts, events: ev, flow: /Export/.test(tt) ? 'Export' : /Import|Documentary/.test(tt) ? 'Import' : 'Guarantee' });
  }

  /* ---------- reports */
  var REPORTS = [
    { id: 'RPT-01', name: 'Group liquidity position', category: 'Liquidity', frequency: 'Daily', format: 'CSV' },
    { id: 'RPT-02', name: 'Thirteen-week cash forecast', category: 'Liquidity', frequency: 'Weekly', format: 'CSV' },
    { id: 'RPT-03', name: 'Facility utilisation and covenants', category: 'Funding', frequency: 'Monthly', format: 'CSV' },
    { id: 'RPT-04', name: 'Counterparty exposure', category: 'Risk', frequency: 'Daily', format: 'CSV' },
    { id: 'RPT-05', name: 'Net FX open positions', category: 'Risk', frequency: 'Daily', format: 'CSV' },
    { id: 'RPT-06', name: 'Payments approved and released', category: 'Payments', frequency: 'Daily', format: 'CSV' },
    { id: 'RPT-07', name: 'Trade finance instruments outstanding', category: 'Trade', frequency: 'Weekly', format: 'CSV' },
    { id: 'RPT-08', name: 'Board treasury pack', category: 'Board', frequency: 'Monthly', format: 'CSV' },
    { id: 'RPT-09', name: 'Bank account signatories', category: 'Governance', frequency: 'Quarterly', format: 'CSV' },
    { id: 'RPT-10', name: 'Hedge effectiveness', category: 'Risk', frequency: 'Monthly', format: 'CSV' },
    { id: 'RPT-11', name: 'Intercompany balances', category: 'Liquidity', frequency: 'Weekly', format: 'CSV' },
    { id: 'RPT-12', name: 'Exceptions and acknowledgements audit', category: 'Governance', frequency: 'On demand', format: 'CSV' }
  ];
  var REPORT_RUNS = [];
  DAYS.forEach(function (d) { REPORTS.forEach(function (r) {
    var p = { Daily: 0.95, Weekly: 0.16, Monthly: 0.04, Quarterly: 0.01, 'On demand': 0.1 }[r.frequency];
    if (R() < p) { REPORT_RUNS.push({ report: r.id, date: d, seconds: round(between(4, 70) * (r.category === 'Board' ? 3 : 1), 1), by: R() < 0.8 ? 'Scheduled' : 'Group treasury' }); }
  }); });

  /* ---------- HSBC messages and service requests */
  var MESSAGES = [
    { id: 'MSG-301', from: 'Your relationship director', subject: 'Revolving facility extension — indicative terms', category: 'Action required', date: '2026-09-25', body: 'Following the treasury committee, we have attached indicative terms for a one-year extension option on the £500m revolving credit facility. Please confirm whether you would like us to proceed to credit approval.' },
    { id: 'MSG-302', from: 'HSBC Global Research', subject: 'Sterling outlook into the November budget', category: 'Market insight', date: '2026-09-25', body: 'Our FX strategists expect sterling to trade in a narrow range against the dollar ahead of the Autumn Budget. This note sets out the scenarios we are watching.' },
    { id: 'MSG-303', from: 'Liquidity management service', subject: 'Euro sweep structure — second counterparty onboarding', category: 'Service update', date: '2026-09-24', body: 'The onboarding of the second euro sweep bank is complete on our side. Your Europe finance team needs to sign the updated mandate.' },
    { id: 'MSG-304', from: 'Trade services, Hong Kong', subject: 'Discrepancy notice on an import letter of credit', category: 'Action required', date: '2026-09-24', body: 'Documents presented under your import letter of credit show a shipment date after the latest date allowed. Please tell us whether to accept the discrepancy.' },
    { id: 'MSG-305', from: 'Payments operations', subject: 'Cut-off times for the UK bank holiday', category: 'Service update', date: '2026-09-23', body: 'Revised cut-off times apply to sterling payments ahead of the bank holiday. Payments submitted after 15:00 will be processed on the next business day.' },
    { id: 'MSG-306', from: 'Know your customer team', subject: 'Beneficial ownership declaration for Shanghai entity', category: 'Action required', date: '2026-09-22', body: 'We still need the updated beneficial ownership declaration for Harbourline (Shanghai) Co Ltd. Accounts may be restricted if it is not received by 15 October.' },
    { id: 'MSG-307', from: 'HSBC Global Research', subject: 'Asia supply chains: third-quarter review', category: 'Market insight', date: '2026-09-21', body: 'A review of freight rates, port throughput and working capital trends across Asia-Pacific supply chains.' },
    { id: 'MSG-308', from: 'Statements service', subject: 'August statements are ready', category: 'Statement ready', date: '2026-09-19', body: 'Statements for all 29 accounts for August are ready to download from Reports.' },
    { id: 'MSG-309', from: 'Your relationship director', subject: 'Mexican peso hedging capacity', category: 'Market insight', date: '2026-09-18', body: 'We can extend forward capacity on the peso to twelve months. Happy to walk the Americas finance team through pricing.' },
    { id: 'MSG-310', from: 'Cyber security', subject: 'Reminder: HSBC will never ask for your security codes', category: 'Service update', date: '2026-09-16', body: 'We have seen an increase in impersonation attempts targeting treasury teams. HSBC will never ask you to share a security code or approve a payment you did not start.' },
    { id: 'MSG-311', from: 'Trade services, London', subject: 'Standby letter of credit renewal', category: 'Action required', date: '2026-09-15', body: 'A standby letter of credit supporting your UK property lease expires in 60 days. Please confirm renewal instructions.' },
    { id: 'MSG-312', from: 'Liquidity management service', subject: 'Interest rate change on deposit accounts', category: 'Service update', date: '2026-09-12', body: 'Following the policy rate decision, rates on your call deposit accounts change from 1 October.' },
    { id: 'MSG-313', from: 'Statements service', subject: 'Facility interest advice — September', category: 'Statement ready', date: '2026-09-10', body: 'Interest advices for your facilities are available for September.' },
    { id: 'MSG-314', from: 'HSBC Global Research', subject: 'Middle East growth and dirham liquidity', category: 'Market insight', date: '2026-09-08', body: 'A look at regional liquidity conditions and what they mean for corporate deposits and funding.' },
    { id: 'MSG-315', from: 'Payments operations', subject: 'Confirmation of payee now live for euro payments', category: 'Service update', date: '2026-09-05', body: 'Name checks now run on euro payments to beneficiaries in the eurozone. Mismatches will be shown before you approve.' },
    { id: 'MSG-316', from: 'Your relationship director', subject: 'Agenda for the quarterly review', category: 'Action required', date: '2026-09-02', body: 'Please share any topics you would like to add to the agenda for the quarterly relationship review on 14 October.' }
  ];
  var SR_TYPES = ['Mandate change', 'User access', 'Payment investigation', 'Statement copy', 'Facility amendment', 'KYC document'];
  var SR_STATUS = ['Submitted', 'In progress', 'Awaiting your input', 'Completed'];
  var REQUESTS = [];
  for (var s = 0; s < 16; s++) {
    var se = pick(ENTITIES), opened = new Date(AS_OF + 'T12:00:00Z'); opened.setUTCDate(opened.getUTCDate() - Math.floor(between(0, 29)));
    var st2 = s < 3 ? 'Awaiting your input' : pick(SR_STATUS), ty = pick(SR_TYPES);
    var upd = new Date(opened); upd.setUTCDate(upd.getUTCDate() + Math.floor(between(0, 4)));
    if (upd > new Date(AS_OF + 'T12:00:00Z')) { upd = new Date(AS_OF + 'T12:00:00Z'); }
    REQUESTS.push({ id: 'SR-' + String(20450 + s * 17), type: ty, entity: se.id, subject: ty + ' — ' + se.short, opened: iso(opened), updated: iso(upd),
      status: st2, sla: { 'Mandate change': 5, 'User access': 2, 'Payment investigation': 3, 'Statement copy': 1, 'Facility amendment': 10, 'KYC document': 5 }[ty], priority: pick(['Normal', 'Normal', 'High']),
      events: [{ date: iso(opened), title: 'Request submitted', tone: 'inf' }].concat(st2 !== 'Submitted' ? [{ date: iso(upd), title: st2 === 'Completed' ? 'Request completed by HSBC' : st2 === 'Awaiting your input' ? 'HSBC asked for more information' : 'Assigned to a service specialist', tone: st2 === 'Completed' ? 'ok' : st2 === 'Awaiting your input' ? 'warn' : 'inf' }] : []) });
  }

  return {
    AS_OF: AS_OF, AS_OF_TIME: AS_OF_TIME, DAYS: DAYS, SESSIONS: SESSIONS, FX: FX, CCYS: CCYS, REGIONS: REGIONS, ENTITIES: ENTITIES, ENT: ENT,
    ACCOUNTS: ACCOUNTS, FACILITIES: FACILITIES, POLICY_BUFFER_GBP: POLICY_BUFFER_GBP, COMMITMENTS: COMMITMENTS, TRANSACTIONS: TRANSACTIONS,
    PAYMENTS: PAYMENTS, POSITIONS: POSITIONS, REGION_LIMITS: REGION_LIMITS, CCY_LIMITS: CCY_LIMITS, COUNTERPARTIES: COUNTERPARTIES,
    EXCEPTIONS: EXCEPTIONS, FX_SERIES: FX_SERIES, HEDGES: HEDGES, TRADE: TRADE, REPORTS: REPORTS, REPORT_RUNS: REPORT_RUNS,
    MESSAGES: MESSAGES, REQUESTS: REQUESTS, toGBP: toGBP
  };
}());
