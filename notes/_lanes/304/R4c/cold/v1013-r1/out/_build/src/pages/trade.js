/* Trade finance — instruments outstanding, imports against exports by region, mix and maturity,
   and the decisions HSBC trade services need: accept or refuse a discrepancy, or ask for an
   amendment. */
(function () {
  'use strict';
  var A = APP, D = A.D, F = A.F, H = A.H, esc = A.esc, $ = A.$;
  var TYPES = ['Import letter of credit', 'Export letter of credit', 'Standby letter of credit', 'Bank guarantee', 'Documentary collection'];
  A.mountChart($('#host-bfv'), { id: 'ch-bfv', note: 'Live instruments as at 25 Sep 2026', type: 'butterfly-v', title: 'Imports outweigh exports everywhere but Asia-Pacific', caption: 'Import and export instruments outstanding by region, £ millions', legend: ['Import', 'Export'] });
  A.mountChart($('#host-pie'), { id: 'ch-pie', note: 'Live instruments as at 25 Sep 2026', type: 'pie', title: 'Instrument mix by value', caption: 'Outstanding instruments by type, £ millions', legend: TYPES.map(function (t) { return t.replace(' letter of credit', ' LC'); }) });
  A.mountChart($('#host-expiry'), { id: 'ch-expiry', note: 'Live instruments as at 25 Sep 2026', type: 'column', title: 'What expires, month by month', caption: 'Value of live instruments by expiry month, £ millions' });
  var TONE = { 'Issued': 'ok', 'Documents presented': 'inf', 'Discrepancy raised': 'err', 'Amendment requested': 'warn', 'Settled': 'ok', 'Expiring soon': 'warn' };
  function status(t) { var w = A.W.pay[t.id]; return w ? w.status : t.status; }
  function items() { return D.TRADE.filter(function (t) { return A.inScope(t.entity); }).map(function (t) { return Object.assign({}, t, { status: status(t) }); }); }
  function live() { return items().filter(function (t) { return t.status !== 'Settled'; }); }
  A.grid($('#host-gtf'), { id: 'g-tf', title: 'Instruments', placeholder: 'Search reference, counterparty, type or entity', size: 10, sort: 'expiry', dir: 'ascending',
    tools: '<button type="button" class="clearbtn t-cm-button" data-export="g-tf" data-file="trade-instruments.csv">Export CSV</button>',
    rows: items, text: function (r) { return [r.id, r.type, r.counterparty, D.ENT[r.entity].name, r.ccy, r.status].join(' '); }, rowLabel: function (r) { return 'Open ' + r.type + ' ' + r.id + ', ' + r.status; },
    cols: [{ k: 'id', label: 'Reference' }, { k: 'type', label: 'Type' }, { k: 'counterparty', label: 'Counterparty' }, { k: 'entity', label: 'Entity', fmt: function (r) { return D.ENT[r.entity].short; } },
      { k: 'expiry', label: 'Expiry', fmt: function (r) { return F.date(r.expiry); }, csv: function (r) { return r.expiry; } }, { k: 'status', label: 'Status', html: function (r) { return H.stat(TONE[r.status] || 'inf', r.status); }, csv: function (r) { return r.status; } },
      { k: 'amount', label: 'Amount', num: true, fmt: function (r) { return F.moneyM(r.amount, r.ccy); } }, { k: 'gbp', label: 'In GBP', num: true, fmt: function (r) { return F.gbpM(r.gbp); }, csv: function (r) { return r.gbp; } }],
    open: openTf });
  function openTf(id) {
    var t = items().filter(function (x) { return x.id === id; })[0] || D.TRADE.filter(function (x) { return x.id === id; })[0]; if (!t) { return; }
    var ev = t.events.slice(); A.W.audit.filter(function (a) { return a.ref === t.id; }).reverse().forEach(function (a) { ev.push({ date: a.at, when: new Date(a.at).toLocaleString('en-GB'), title: a.what, desc: a.note, tone: 'ok' }); });
    var acts = t.status === 'Discrepancy raised' ? [{ id: 'accept', label: 'Accept discrepancy', kind: 'primary' }, { id: 'refuse', label: 'Refuse documents' }] :
      t.status === 'Settled' ? [{ id: 'close', label: 'Close', kind: 'primary' }] : [{ id: 'amend', label: 'Request an amendment', kind: 'primary' }, { id: 'close', label: 'Close' }];
    A.openDrawer({ id: id, title: t.type + ' ' + t.id, body: (t.status === 'Discrepancy raised' ? H.alert('err', 'Decision needed.', 'HSBC will not pay under this instrument until you accept or refuse the discrepancy.') : '') +
      H.summary([{ k: 'Counterparty', v: t.counterparty }, { k: 'Amount', v: F.money(t.amount, t.ccy) }, { k: 'GBP equivalent', v: F.gbpM(t.gbp) }, { k: 'Issued', v: F.date(t.issued) }, { k: 'Expiry', v: F.date(t.expiry) }, { k: 'Entity', v: D.ENT[t.entity].name }, { k: 'Status', html: H.stat(TONE[t.status] || 'inf', t.status) }]) +
      H.timeline(ev.reverse()), actions: acts,
      onAction: function (a) { if (a === 'close') { A.closeDrawer(); return; } A.closeDrawer(); decide(t, a); } });
  }
  function decide(t, a) {
    var title = { accept: 'Accept the discrepancy on ' + t.id, refuse: 'Refuse the documents on ' + t.id, amend: 'Request an amendment to ' + t.id }[a];
    A.openModal({ title: title, body: (a === 'amend' ? H.radios({ name: 'am-what', legend: 'What should change', value: 'expiry', options: [{ v: 'expiry', label: 'Extend the expiry date' }, { v: 'amount', label: 'Change the amount' }, { v: 'terms', label: 'Change documents or terms' }] }) : '') +
      H.textarea({ id: 'tf-note', label: a === 'amend' ? 'Details for HSBC trade services' : 'Instruction and reason', max: 400, rows: 3, help: 'Required, at least 15 characters.' }),
      actions: [{ id: 'go', label: a === 'accept' ? 'Accept and pay' : a === 'refuse' ? 'Refuse documents' : 'Send request', kind: 'primary' }, { id: 'cancel', label: 'Cancel' }],
      onAction: function (x) {
        if (x === 'cancel') { return true; }
        var n = A.val('tf-note'); if (n.length < 15) { A.fail('tf-note', 'Write at least 15 characters.'); document.getElementById('tf-note').focus(); return false; }
        var st = a === 'accept' ? 'Documents presented' : a === 'refuse' ? 'Amendment requested' : 'Amendment requested';
        A.W.pay[t.id] = { status: st, at: new Date().toISOString(), note: n };
        A.W.audit.unshift({ at: new Date().toISOString(), ref: t.id, what: { accept: 'Discrepancy accepted by you', refuse: 'Documents refused by you', amend: 'Amendment requested by you' }[a], note: n });
        A.W.sr.unshift({ id: 'SR-' + String(30000 + A.W.sr.length + 1), type: 'Trade instruction', entity: t.entity, subject: title, opened: D.AS_OF, updated: D.AS_OF, status: 'Submitted', sla: 2, priority: 'High', events: [{ date: D.AS_OF, title: 'Instruction sent: ' + n, tone: 'inf' }] });
        A.saveWork(); A.toast('Instruction on ' + t.id + ' sent to HSBC trade services.', 'ok'); render(); return true;
      } });
  }
  A.onClick = function (e) {
    if (e.target.closest('[data-action="export-tf"]')) { A.$('[data-export="g-tf"]').click(); }
    var o = e.target.closest('[data-open-tf]'); if (o) { e.preventDefault(); openTf(o.getAttribute('data-open-tf')); }
  };
  function render() {
    var its = items(), lv = live(), idx = A.dayIdx();
    function cum(fn) { return idx.map(function (i) { return lv.filter(fn).filter(function (t) { return t.issued <= D.DAYS[i]; }).reduce(function (a, t) { return a + t.gbp; }, 0); }); }
    A.renderKpis($('#kpis'), [{ id: 'out', label: 'Outstanding', series: cum(function () { return true; }), note: 'Live instruments by issue date, £ equivalent.' },
      { id: 'imp', label: 'Import instruments', series: cum(function (t) { return t.flow === 'Import'; }), note: 'Import letters of credit and collections.' },
      { id: 'exp', label: 'Export instruments', series: cum(function (t) { return t.flow === 'Export'; }), note: 'Export letters of credit.' },
      { id: 'gua', label: 'Guarantees and standbys', series: cum(function (t) { return t.flow === 'Guarantee'; }), note: 'Bank guarantees and standby letters of credit.' }]);
    var regs = D.REGIONS.filter(function (r) { return A.scopedEntities().some(function (e) { return e.region === r.id; }); });
    if (!regs.length || !lv.length) { ['ch-bfv', 'ch-pie', 'ch-expiry'].forEach(function (c) { A.emptyChart(c); }); }
    else {
      A.drawChart('ch-bfv', { type: 'butterfly-v', categories: regs.map(function (r) { return r.name; }), categoryLabel: 'Region', unit: '£m', caption: 'Import and export instruments outstanding by region, £ millions',
        series: ['Import', 'Export'].map(function (f) { return { name: f, values: regs.map(function (r) { return Math.round(lv.filter(function (t) { return t.flow === f && D.ENT[t.entity].region === r.id; }).reduce(function (a, t) { return a + t.gbp; }, 0) / 1e5) / 10; }) }; }) });
      A.drawChart('ch-pie', { type: 'pie', categories: TYPES.map(function (t) { return t.replace(' letter of credit', ' LC'); }), categoryLabel: 'Instrument', unit: '£m', caption: 'Outstanding instruments by type, £ millions',
        series: [{ name: 'Value', values: TYPES.map(function (ty) { return Math.round(lv.filter(function (t) { return t.type === ty; }).reduce(function (a, t) { return a + t.gbp; }, 0) / 1e5) / 10; }) }] });
      var months = ['2026-10', '2026-11', '2026-12', '2027-01', '2027-02', '2027-03', '2027-04'], ml = ['Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr+'];
      A.drawChart('ch-expiry', { type: 'column', categories: ml, categoryLabel: 'Expiry month', unit: '£m', caption: 'Value of live instruments by expiry month, £ millions',
        series: [{ name: 'Expiring', values: months.map(function (m, k) { return Math.round(lv.filter(function (t) { return k === months.length - 1 ? t.expiry.slice(0, 7) >= m : t.expiry.slice(0, 7) === m || (k === 0 && t.expiry.slice(0, 7) < m); }).reduce(function (a, t) { return a + t.gbp; }, 0) / 1e5) / 10; }) }] });
    }
    var act = its.filter(function (t) { return t.status === 'Discrepancy raised' || t.status === 'Amendment requested'; });
    $('#tf-action').innerHTML = act.length ? '<div class="l-stack" data-gap="m">' + act.slice(0, 5).map(function (t) { return '<div class="l-row" data-gap="s" data-justify="between"><a class="tpl-link t-cm-label" href="#' + t.id + '" data-open-tf="' + t.id + '">' + esc(t.id + ' · ' + t.counterparty) + '</a>' + '<span class="status ' + (TONE[t.status] === 'err' ? 'err' : 'warn') + '" data-carries="label"><span class="dot" aria-hidden="true"></span><span class="t-cm-legal">' + esc(t.status) + '</span></span></div>'; }).join('') + '</div>' : '<p class="t-ed-body-small">No decisions waiting in this scope.</p>';
    var soon = lv.filter(function (t) { return t.expiry <= '2026-10-25'; });
    $('#tf-expiring').innerHTML = '<dl class="summary">' + (soon.length ? soon.slice(0, 5).map(function (t) { return '<div class="summary__row"><dt class="summary__k t-cm-label">' + esc(t.id) + ' <span class="t-cm-legal">' + F.date(t.expiry) + '</span></dt><dd class="summary__v t-cm-figure-5">' + F.gbpM(t.gbp) + '</dd></div>'; }).join('') : '<div class="summary__row"><dt class="summary__k t-cm-label">Nothing expires in 30 days</dt><dd class="summary__v t-cm-figure-5">0</dd></div>') + '</dl>';
    A.renderGrid('g-tf');
  }
  A.afterBoot = function () { if (A.PS.open) { openTf(A.PS.open); } };
  A.boot(render);
}());
