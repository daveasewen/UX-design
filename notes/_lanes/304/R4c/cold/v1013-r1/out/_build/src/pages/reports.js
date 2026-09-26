/* Reports — run history over time, mix by category, run time, and a validated "run now" that
   builds a real CSV from DATA under the current filters. */
(function () {
  'use strict';
  var A = APP, D = A.D, F = A.F, H = A.H, esc = A.esc, $ = A.$;
  var CATS = ['Liquidity', 'Funding', 'Risk', 'Payments', 'Trade', 'Board', 'Governance'];
  var RCAT = function (id) { return D.REPORTS.filter(function (r) { return r.id === id; })[0].category; };
  var LEG = ['Liquidity and funding', 'Risk', 'Payments and trade', 'Board and governance'];
  function bucket(c) { return c === 'Liquidity' || c === 'Funding' ? 0 : c === 'Risk' ? 1 : c === 'Payments' || c === 'Trade' ? 2 : 3; }
  A.mountChart($('#host-runs'), { id: 'ch-runs', note: 'Group-wide: entity and region do not apply', type: 'stacked-column', title: 'Reports run each day', caption: 'Report runs per day by category group, count', legend: LEG });
  A.mountChart($('#host-cat'), { id: 'ch-cat', note: 'Group-wide', type: 'donut', title: 'Risk reports are the most run', caption: 'Report runs in the period by category group, count', legend: LEG });
  A.mountChart($('#host-time'), { id: 'ch-time', note: 'Group-wide', type: 'bar', title: 'Average run time', caption: 'Average run time by category, seconds' });
  function runs() { return D.REPORT_RUNS.filter(function (r) { return A.inWindow(r.date); }).concat(A.W.runs.filter(function (r) { return A.inWindow(r.date); })); }
  A.grid($('#host-grep'), { id: 'g-rep', title: 'Reports', placeholder: 'Search reports', size: 25, sort: 'name', dir: 'ascending',
    rows: function () { var rs = runs(); return D.REPORTS.map(function (r) { var mine = rs.filter(function (x) { return x.report === r.id; }); return Object.assign({}, r, { runs: mine.length, last: mine.map(function (x) { return x.date; }).sort().pop() || '' }); }); },
    text: function (r) { return [r.name, r.category, r.frequency].join(' '); }, rowLabel: function (r) { return 'Run ' + r.name; },
    cols: [{ k: 'name', label: 'Report' }, { k: 'category', label: 'Category' }, { k: 'frequency', label: 'Frequency' }, { k: 'last', label: 'Last run', fmt: function (r) { return r.last ? F.date(r.last) : 'Not in period'; } },
      { k: 'runs', label: 'Runs in period', num: true, fmt: function (r) { return String(r.runs); } }, { k: 'format', label: 'Format', sort: false }],
    open: function (id) { runNow(id); } });
  function build(id) {   /* the report's rows, from DATA, under the current filters */
    var sc = A.scopeLabel();
    switch (id) {
      case 'RPT-01': return [['Entity', 'Account', 'Currency', 'Closing balance', 'GBP equivalent']].concat(D.ACCOUNTS.filter(function (a) { return A.inScope(a.entity); }).map(function (a) { return [D.ENT[a.entity].name, a.name, a.ccy, a.balances[29], Math.round(D.toGBP(a.balances[29], a.ccy))]; }));
      case 'RPT-03': return [['Facility', 'Currency', 'Limit', 'Drawn', 'Utilisation %', 'Maturity']].concat(D.FACILITIES.filter(function (f) { return A.inScope(f.entity); }).map(function (f) { return [f.name, f.ccy, f.limit, f.drawn, (f.drawn / f.limit * 100).toFixed(1), f.maturity]; }));
      case 'RPT-04': return [['Counterparty', 'Rating', 'Limit (GBP)', 'Exposure (GBP)']].concat(D.COUNTERPARTIES.map(function (c) { return [c.name, c.rating, c.limit, c.exposure]; }));
      case 'RPT-05': return [['Entity', 'Currency', 'Position', 'Local', 'GBP']].concat(D.POSITIONS.filter(function (p) { return A.inScope(p.entity) && p.ccy !== 'GBP'; }).map(function (p) { return [D.ENT[p.entity].name, p.ccy, p.type, p.local, p.gbp]; }));
      case 'RPT-06': return [['Payment', 'Beneficiary', 'Currency', 'Amount', 'Status', 'Value date']].concat(A.calc.payments().filter(function (p) { return A.inScope(p.entity); }).map(function (p) { return [p.id, p.beneficiary, p.ccy, p.amount, p.status, p.valueDate]; }));
      case 'RPT-07': return [['Reference', 'Type', 'Counterparty', 'Currency', 'Amount', 'Expiry', 'Status']].concat(D.TRADE.filter(function (t) { return A.inScope(t.entity); }).map(function (t) { return [t.id, t.type, t.counterparty, t.ccy, t.amount, t.expiry, t.status]; }));
      case 'RPT-12': return [['When', 'What', 'Reference', 'Note']].concat(A.W.audit.map(function (a) { return [a.at, a.what, a.ref || '', a.note || '']; }));
      default: return [['Date', 'Cash (GBP)', 'Available liquidity (GBP)', 'Funding headroom (GBP)', 'Scope']].concat(A.days().map(function (d, i) { return [d, Math.round(A.calc.cashSeries()[i]), Math.round(A.calc.liquiditySeries()[i]), Math.round(A.calc.headroomSeries()[i]), sc]; }));
    }
  }
  function runNow(id) {
    var r = D.REPORTS.filter(function (x) { return x.id === id; })[0]; if (!r) { return; }
    A.openModal({ title: 'Run ' + r.name, body: '<p class="t-ed-body">Builds the report now from the figures on screen, for ' + esc(A.scopeLabel()) + '.</p>' +
      H.radios({ name: 'rp-when', legend: 'Deliver', value: 'now', options: [{ v: 'now', label: 'Download now as CSV' }, { v: 'inbox', label: 'Download now and keep a copy in Reports' }] }) +
      H.check({ id: 'rp-ok', label: 'I understand this prototype uses illustrative data only' }),
      actions: [{ id: 'go', label: 'Run report', kind: 'primary' }, { id: 'cancel', label: 'Cancel' }],
      onAction: function (a) {
        if (a === 'cancel') { return true; }
        if (!A.val('rp-ok')) { A.fail('rp-ok', 'Confirm you understand the data is illustrative.'); document.getElementById('rp-ok').focus(); return false; }
        A.W.runs.push({ report: r.id, date: D.AS_OF, seconds: 3.2, by: 'You' }); A.saveWork();
        A.csv(r.name.toLowerCase().replace(/\W+/g, '-') + '.csv', build(r.id)); render(); return true;
      } });
  }
  A.onClick = function (e) {
    if (e.target.closest('[data-action="export-runs"]')) { A.csv('report-runs.csv', [['Date', 'Report', 'Category', 'Seconds', 'Run by']].concat(runs().map(function (x) { return [x.date, D.REPORTS.filter(function (r) { return r.id === x.report; })[0].name, RCAT(x.report), x.seconds, x.by]; }))); }
    var b = e.target.closest('[data-run]'); if (b) { runNow(b.getAttribute('data-run')); }
  };
  function render() {
    var rs = runs(), idx = A.dayIdx(), ds = A.days();
    var perDay = function (fn) { return idx.map(function (i) { return rs.filter(function (r) { return r.date === D.DAYS[i] && fn(r); }).length; }); };
    var cum = function (a) { var s = 0; return a.map(function (v) { s += v; return s; }); };
    var myExports = A.W.audit.filter(function (a) { return /^Exported/.test(a.what); });
    A.renderKpis($('#kpis'), [{ id: 'runs', label: 'Report runs', count: true, series: cum(perDay(function () { return true; })), note: 'Cumulative report runs in the period.' },
      { id: 'sched', label: 'Scheduled runs', count: true, series: cum(perDay(function (r) { return r.by === 'Scheduled'; })), note: 'Runs by the scheduler.' },
      { id: 'manual', label: 'Run by your team', count: true, series: cum(perDay(function (r) { return r.by !== 'Scheduled'; })), note: 'Runs started by a person.' },
      { id: 'exports', label: 'Your exports', count: true, series: idx.map(function (i, k) { return k === idx.length - 1 ? myExports.length : 0; }), note: 'CSV exports you have made in this browser.' }]);
    A.drawChart('ch-runs', { type: 'stacked-column', categories: ds.map(F.dshort), categoryLabel: 'Date', caption: 'Report runs per day by category group, count',
      series: LEG.map(function (l, k) { return { name: l, values: perDay(function (r) { return bucket(RCAT(r.report)) === k; }) }; }) });
    A.drawChart('ch-cat', { type: 'donut', categories: LEG, categoryLabel: 'Category group', caption: 'Report runs in the period by category group, count', series: [{ name: 'Runs', values: LEG.map(function (l, k) { return rs.filter(function (r) { return bucket(RCAT(r.report)) === k; }).length; }) }] });
    var cats = CATS.filter(function (c) { return rs.some(function (r) { return RCAT(r.report) === c; }); });
    A.drawChart('ch-time', { type: 'bar', categories: cats, categoryLabel: 'Category', unit: 's', caption: 'Average run time by category, seconds',
      series: [{ name: 'Average seconds', values: cats.map(function (c) { var m = rs.filter(function (r) { return RCAT(r.report) === c; }); return Math.round(m.reduce(function (a, r) { return a + r.seconds; }, 0) / m.length * 10) / 10; }) }] });
    $('#rep-audit').innerHTML = myExports.length ? H.timeline(myExports.slice(0, 5).map(function (a) { return { date: a.at, when: new Date(a.at).toLocaleString('en-GB'), title: a.what, tone: 'ok' }; })) : '<p class="t-ed-body-small">You have not exported anything in this browser yet. Every export button on every page records here.</p>';
    $('#rep-board').innerHTML = '<p class="t-ed-body-small">The board treasury pack combines liquidity, funding, risk and exceptions for the period.</p><div class="l-row" data-gap="m"><button type="button" class="btn secondary" data-run="RPT-08">Run the board pack</button><button type="button" class="btn tertiary" data-run="RPT-12">Run the audit trail</button></div>';
    A.renderGrid('g-rep');
  }
  A.boot(render);
}());
