/* Accounts and transactions — balances by region over time, where cash sits, flow sizes, and two
   records grids (transactions, accounts) with detail drawers. */
(function () {
  'use strict';
  var A = APP, D = A.D, F = A.F, H = A.H, esc = A.esc, $ = A.$;
  A.mountChart($('#host-bal'), { id: 'ch-bal', type: 'stacked-area', title: 'Cash by region, day by day', caption: 'Closing cash by region, £ millions', legend: D.REGIONS.map(function (r) { return r.name; }) });
  A.mountChart($('#host-entity'), { id: 'ch-entity', note: 'As at 25 Sep 2026', type: 'bar', title: 'Where the cash sits today', caption: 'Closing cash by entity, £ millions' });
  A.mountChart($('#host-hist'), { id: 'ch-hist', type: 'histogram', title: 'Most flows are under £2m', caption: 'Transactions in the period by value band, £ equivalent, count',
    after: '<ul class="dv-leg-static t-cm-chart-label" aria-hidden="true"><li><span class="sw"></span><span>Transactions</span></li></ul>' });
  function acct(id) { return D.ACCOUNTS.filter(function (a) { return a.id === id; })[0]; }
  function txRows() { return D.TRANSACTIONS.filter(function (t) { return A.inScope(t.entity) && A.inWindow(t.date); }); }
  A.grid($('#host-gtx'), { id: 'g-tx', title: 'Transactions', placeholder: 'Search counterparty, reference, category or entity', size: 25, sort: 'date', dir: 'descending',
    tools: '<button type="button" class="clearbtn t-cm-button" data-export="g-tx" data-file="transactions.csv">Export CSV</button>',
    rows: txRows, text: function (r) { return [r.counterparty, r.ref, r.category, D.ENT[r.entity].name, r.ccy, r.id, r.status].join(' '); },
    rowLabel: function (r) { return 'Open transaction ' + r.ref + ', ' + r.counterparty + ', ' + F.money(r.amount, r.ccy); },
    cols: [
      { k: 'date', label: 'Date', fmt: function (r) { return F.date(r.date); }, csv: function (r) { return r.date; } },
      { k: 'counterparty', label: 'Counterparty' },
      { k: 'category', label: 'Category' },
      { k: 'entity', label: 'Entity', fmt: function (r) { return D.ENT[r.entity].short; }, val: function (r) { return D.ENT[r.entity].short; } },
      { k: 'status', label: 'Status', html: function (r) { return H.stat(r.status === 'Settled' ? 'ok' : 'warn', r.status); } },
      { k: 'amount', label: 'Amount', num: true, fmt: function (r) { return F.money(r.amount, r.ccy); }, csv: function (r) { return r.amount + ' ' + r.ccy; } },
      { k: 'gbp', label: 'In GBP', num: true, fmt: function (r) { return F.money(r.gbp, 'GBP'); }, csv: function (r) { return r.gbp; } }
    ],
    open: openTx });
  A.grid($('#host-gacc'), { id: 'g-acc', title: 'Accounts', placeholder: 'Search account, entity or currency', size: 10, sort: 'gbp', dir: 'descending',
    rows: function () { return D.ACCOUNTS.filter(function (a) { return A.inScope(a.entity); }).map(function (a) { return Object.assign({}, a, { bal: a.balances[29], gbp: D.toGBP(a.balances[29], a.ccy), chg: (a.balances[29] - a.balances[30 - A.S.days]) / a.balances[30 - A.S.days] * 100 }); }); },
    text: function (r) { return [r.name, D.ENT[r.entity].name, r.ccy, r.type, r.number].join(' '); },
    rowLabel: function (r) { return 'Open account ' + r.name; },
    cols: [
      { k: 'name', label: 'Account' }, { k: 'number', label: 'Number', sort: false }, { k: 'entity', label: 'Entity', fmt: function (r) { return D.ENT[r.entity].short; } },
      { k: 'ccy', label: 'Currency' },
      { k: 'bal', label: 'Balance', num: true, fmt: function (r) { return F.money(r.bal, r.ccy); } },
      { k: 'gbp', label: 'In GBP', num: true, fmt: function (r) { return F.money(r.gbp, 'GBP'); } },
      { k: 'chg', label: 'Change', num: true, html: function (r) { return '<span class="t-cm-figure-5">' + F.signedPct(r.chg) + '</span>'; }, csv: function (r) { return r.chg.toFixed(1); } }
    ],
    open: openAcct });
  function openTx(id) {
    var t = D.TRANSACTIONS.filter(function (x) { return x.id === id; })[0]; if (!t) { return; }
    var ac = acct(t.account);
    A.openDrawer({ id: id, title: t.category + ' · ' + t.ref, body: H.summary([
      { k: 'Counterparty', v: t.counterparty }, { k: 'Amount', v: F.money(t.amount, t.ccy) }, { k: 'GBP equivalent', v: F.money(t.gbp, 'GBP') + ' at ' + D.FX[t.ccy] + ' ' + t.ccy + '/GBP (illustrative)' },
      { k: 'Date', v: F.date(t.date) }, { k: 'Status', html: H.stat(t.status === 'Settled' ? 'ok' : 'warn', t.status) }, { k: 'Account', v: ac.name + ' ' + ac.number },
      { k: 'Entity', v: D.ENT[t.entity].name }, { k: 'Transaction id', v: t.id }]) +
      (t.status === 'Pending' ? H.alert('info', 'Pending.', 'This item has not settled yet. If it looks wrong you can ask HSBC to investigate it.') : ''),
      actions: [{ id: 'invest', label: 'Ask HSBC to investigate', kind: 'primary' }, { id: 'close', label: 'Close' }],
      onAction: function (a) {
        if (a === 'close') { A.closeDrawer(); return; }
        A.W.sr.unshift({ id: 'SR-' + String(30000 + A.W.sr.length + 1), type: 'Payment investigation', entity: t.entity, subject: 'Investigate ' + t.ref + ' — ' + t.counterparty, opened: D.AS_OF, updated: D.AS_OF,
          status: 'Submitted', sla: 3, priority: 'Normal', events: [{ date: D.AS_OF, title: 'Request submitted from Accounts', tone: 'inf' }] });
        A.W.audit.unshift({ at: new Date().toISOString(), what: 'Raised a payment investigation for ' + t.ref }); A.saveWork();
        A.closeDrawer(); A.toast('Investigation request sent for ' + t.ref + '. Track it in Messages and service requests.', 'ok');
      } });
  }
  function openAcct(id) {
    var a = acct(id); if (!a) { return; }
    var ds = A.days(), idx = A.dayIdx();
    A.openDrawer({ id: id, title: a.name, body: H.summary([{ k: 'Account', v: a.number + ' · ' + a.bank }, { k: 'Entity', v: D.ENT[a.entity].name }, { k: 'Currency', v: a.ccy },
      { k: 'Closing balance', v: F.money(a.balances[29], a.ccy) }, { k: 'GBP equivalent', v: F.money(D.toGBP(a.balances[29], a.ccy), 'GBP') }, { k: 'Overdraft limit', v: a.overdraft ? F.money(a.overdraft, a.ccy) : 'None' }]) +
      '<div id="acc-spark"></div>' +
      H.timeline(D.TRANSACTIONS.filter(function (t) { return t.account === a.id && A.inWindow(t.date); }).slice(0, 6).map(function (t) { return { date: t.date, title: t.counterparty + ' · ' + t.category, amount: F.money(t.amount, t.ccy), tone: t.status === 'Settled' ? 'ok' : 'warn' }; })),
      actions: [{ id: 'stmt', label: 'Export statement (CSV)', kind: 'primary' }, { id: 'close', label: 'Close' }],
      onAction: function (x) {
        if (x === 'close') { A.closeDrawer(); return; }
        A.csv(a.id + '-statement.csv', [['Date', 'Counterparty', 'Category', 'Reference', 'Amount', 'Currency', 'Status']].concat(D.TRANSACTIONS.filter(function (t) { return t.account === a.id && A.inWindow(t.date); }).map(function (t) { return [t.date, t.counterparty, t.category, t.ref, t.amount, t.ccy, t.status]; })));
      } });
    A.mountChart($('#acc-spark'), { id: 'ch-acc-spark', type: 'spark', caption: a.name + ' closing balance over the period' });
    A.drawChart('ch-acc-spark', { type: 'spark', categories: ds.map(F.dshort), series: [{ name: 'Balance', values: idx.map(function (i) { return Math.round(a.balances[i]); }) }], unit: a.ccy, caption: a.name + ' closing balance over the period' });
  }
  A.onClick = function (e) {
    if (e.target.closest('[data-action="export-tx"]')) { A.$('[data-export="g-tx"]').click(); }
  };
  function render() {
    var idx = A.dayIdx(), ds = A.days(), tx = txRows();
    var inflow = idx.map(function (i) { return tx.filter(function (t) { return t.date === D.DAYS[i] && t.gbp > 0; }).reduce(function (a, t) { return a + t.gbp; }, 0); });
    var outflow = idx.map(function (i) { return -tx.filter(function (t) { return t.date === D.DAYS[i] && t.gbp < 0; }).reduce(function (a, t) { return a + t.gbp; }, 0); });
    var cum = function (arr) { var s = 0; return arr.map(function (v) { s += v; return s; }); };
    A.renderKpis($('#kpis'), [
      { id: 'cash', label: 'Cash', series: A.calc.cashSeries(), note: 'Closing cash across accounts in scope, GBP at illustrative rates.' },
      { id: 'in', label: 'Money in', series: cum(inflow), note: 'Cumulative receipts in the period.' },
      { id: 'out', label: 'Money out', series: cum(outflow), note: 'Cumulative payments in the period.' },
      { id: 'net', label: 'Net flow', series: cum(inflow.map(function (v, i) { return v - outflow[i]; })), note: 'Cumulative receipts less payments.' }]);
    var regs = D.REGIONS.filter(function (r) { return A.scopedEntities().some(function (e) { return e.region === r.id; }); });
    if (!regs.length) { ['ch-bal', 'ch-entity', 'ch-hist'].forEach(function (c) { A.emptyChart(c); }); }
    else {
      A.drawChart('ch-bal', { type: 'stacked-area', categories: ds.map(F.dshort), categoryLabel: 'Date', unit: '£m', caption: 'Closing cash by region, £ millions',
        series: D.REGIONS.map(function (r) { return { name: r.name, values: idx.map(function (i) { return Math.round(D.ACCOUNTS.reduce(function (a, ac) { return A.inScope(ac.entity) && D.ENT[ac.entity].region === r.id ? a + D.toGBP(ac.balances[i], ac.ccy) : a; }, 0) / 1e5) / 10; }) }; }) });
      var ents = A.scopedEntities().map(function (e) { return { n: e.short, v: D.ACCOUNTS.reduce(function (a, ac) { return ac.entity === e.id ? a + D.toGBP(ac.balances[29], ac.ccy) : a; }, 0) }; }).sort(function (a, b) { return b.v - a.v; });
      A.drawChart('ch-entity', { type: 'bar', categories: ents.map(function (e) { return e.n; }), series: [{ name: 'Cash', values: ents.map(function (e) { return Math.round(e.v / 1e5) / 10; }) }], unit: '£m', categoryLabel: 'Entity', caption: 'Closing cash by entity, £ millions' });
      var bands = [0, 0.25e6, 0.5e6, 1e6, 2e6, 4e6, 8e6, 16e6], labels = ['<£0.25m', '£0.25–0.5m', '£0.5–1m', '£1–2m', '£2–4m', '£4–8m', '£8–16m', '£16m+'], counts = bands.map(function () { return 0; });
      tx.forEach(function (t) { var v = Math.abs(t.gbp), k = 0; for (var i = 0; i < bands.length; i++) { if (v >= bands[i]) { k = i; } } counts[k]++; });
      if (tx.length) { A.drawChart('ch-hist', { type: 'histogram', categories: labels, series: [{ name: 'Transactions', values: counts }], categoryLabel: 'Value band', caption: 'Transactions in the period by value band, £ equivalent, count' }); } else { A.emptyChart('ch-hist'); }
    }
    var top = D.ACCOUNTS.filter(function (a) { return A.inScope(a.entity); }).sort(function (a, b) { return D.toGBP(b.balances[29], b.ccy) - D.toGBP(a.balances[29], a.ccy); }).slice(0, 5);
    $('#acc-top').innerHTML = top.length ? '<dl class="summary">' + top.map(function (a) { return '<div class="summary__row"><dt class="summary__k t-cm-label">' + esc(a.name) + '</dt><dd class="summary__v t-cm-figure-5">' + F.moneyM(a.balances[29], a.ccy) + '</dd></div>'; }).join('') + '</dl>' : '<p class="t-ed-body-small">No accounts in this scope.</p>';
    var pend = tx.filter(function (t) { return t.status === 'Pending'; });
    $('#acc-pending').innerHTML = '<dl class="summary tpl-na-head"><div class="summary__row"><dt class="summary__k t-cm-label">Not yet settled <span class="t-cm-legal">' + pend.length + ' items</span></dt><dd class="summary__v t-cm-figure-5">' + F.gbpM(pend.reduce(function (a, t) { return a + Math.abs(t.gbp); }, 0)) + '</dd></div></dl>' +
      '<div class="l-stack" data-gap="m">' + pend.slice(0, 4).map(function (t) { return '<div class="l-row" data-gap="s" data-justify="between"><span class="t-cm-label">' + esc(t.counterparty) + '</span><span class="t-cm-figure-6">' + F.moneyM(t.amount, t.ccy) + '</span></div>'; }).join('') + '</div>';
    A.renderGrid('g-tx'); A.renderGrid('g-acc');
  }
  A.afterBoot = function () { var o = A.PS.open; if (o) { if (/^TX/.test(o)) { openTx(o); } else if (/^AC/.test(o)) { openAcct(o); } } };
  A.boot(render);
}());
