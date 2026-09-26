/* Payments and approvals — the approval queue with validated approve / reject, dual control above
   £10m (your approval moves it to the second approver), sanctions holds you cannot override, and a
   persistent audit trail. */
(function () {
  'use strict';
  var A = APP, D = A.D, F = A.F, H = A.H, esc = A.esc, $ = A.$;
  var view = A.PS.view || 'all';
  A.mountChart($('#host-byccy'), { id: 'ch-byccy', note: 'Pending now; the date range does not apply', type: 'bar', title: 'Pending value by currency', caption: 'Value of payments not yet released, by currency, £ millions equivalent' });
  A.mountChart($('#host-scatter'), { id: 'ch-scatter', note: 'Pending now; the date range does not apply', type: 'scatter', title: 'Large payments cluster in the next week', caption: 'Pending payments: days to value date against value, £ millions' });
  A.mountChart($('#host-flow'), { id: 'ch-flow', type: 'line', title: 'Value released per day', caption: 'Payments released by value date, £ millions' });
  var TONE = { 'Awaiting your approval': 'warn', 'Awaiting second approver': 'inf', 'Approved': 'ok', 'Released': 'ok', 'Rejected': 'err', 'Held for screening': 'err' };
  function pays() { return A.calc.payments().filter(function (p) { return A.inScope(p.entity); }); }
  A.grid($('#host-gpay'), { id: 'g-pay', title: 'Payments', placeholder: 'Search beneficiary, payment id, type or entity', size: 10, sort: 'valueDate', dir: 'ascending',
    tools: '<div class="cn-segmented-control"><div class="seg s" role="group" aria-label="Show payments"><span class="ind" aria-hidden="true"></span><button type="button" data-pay-view="mine" aria-pressed="' + (view === 'mine') + '">Waiting for me</button><button type="button" data-pay-view="all" aria-pressed="' + (view === 'all') + '">All payments</button></div></div>' +
      '<button type="button" class="clearbtn t-cm-button" data-export="g-pay" data-file="payments.csv">Export CSV</button>',
    rows: function () { return pays().filter(function (p) { return view === 'all' || p.status === 'Awaiting your approval'; }); },
    text: function (r) { return [r.id, r.beneficiary, r.type, D.ENT[r.entity].name, r.ccy, r.status, r.initiator].join(' '); },
    rowLabel: function (r) { return 'Open payment ' + r.id + ' to ' + r.beneficiary + ', ' + F.money(r.amount, r.ccy) + ', ' + r.status; },
    empty: 'Nothing is waiting for your approval in this scope',
    cols: [{ k: 'id', label: 'Payment' }, { k: 'beneficiary', label: 'Beneficiary' }, { k: 'type', label: 'Type' }, { k: 'entity', label: 'Entity', fmt: function (r) { return D.ENT[r.entity].short; } },
      { k: 'valueDate', label: 'Value date', fmt: function (r) { return F.date(r.valueDate); }, csv: function (r) { return r.valueDate; } },
      { k: 'status', label: 'Status', html: function (r) { return H.stat(TONE[r.status], r.status); }, csv: function (r) { return r.status; } },
      { k: 'amount', label: 'Amount', num: true, fmt: function (r) { return F.money(r.amount, r.ccy); } }, { k: 'gbp', label: 'In GBP', num: true, fmt: function (r) { return F.gbpM(r.gbp); }, csv: function (r) { return r.gbp; } }],
    open: openPay });
  function history(p) {
    var ev = [{ date: p.created, title: 'Created by ' + p.initiator, tone: 'inf' }];
    if (p.status === 'Released' || p.status === 'Approved') { ev.push({ date: p.created, title: 'Approved' + (p.approvals === 2 ? ' by two approvers' : ''), tone: 'ok' }); }
    if (p.status === 'Released') { ev.push({ date: p.valueDate, title: 'Released to HSBC for payment', tone: 'ok' }); }
    if (p.status === 'Held for screening') { ev.push({ date: p.created, title: 'Held by HSBC sanctions screening', tone: 'err' }); }
    A.W.audit.filter(function (a) { return a.ref === p.id; }).reverse().forEach(function (a) { ev.push({ date: a.at, when: new Date(a.at).toLocaleString('en-GB'), title: a.what, desc: a.note, tone: /Reject/.test(a.what) ? 'err' : 'ok' }); });
    return H.timeline(ev.reverse());
  }
  function openPay(id) {
    var p = A.calc.payments().filter(function (x) { return x.id === id; })[0]; if (!p) { return; }
    var mine = p.status === 'Awaiting your approval';
    A.openDrawer({ id: id, title: p.id + ' · ' + p.beneficiary, body:
      (p.flags.length ? H.alert(p.status === 'Held for screening' ? 'err' : 'warn', p.flags.length + ' check' + (p.flags.length > 1 ? 's' : '') + ' before you approve.', p.flags.join(' · ') + '.') : '') +
      H.summary([{ k: 'Amount', v: F.money(p.amount, p.ccy) }, { k: 'GBP equivalent', v: F.money(p.gbp, 'GBP') + ' (illustrative rate)' }, { k: 'Beneficiary', v: p.beneficiary }, { k: 'Type', v: p.type },
        { k: 'From', v: D.ENT[p.entity].name }, { k: 'Value date', v: F.date(p.valueDate) }, { k: 'Approvals required', v: p.approvals === 2 ? 'Two (dual control)' : 'One' },
        { k: 'Status', html: H.stat(TONE[p.status], p.status) }]) + history(p),
      actions: mine ? [{ id: 'approve', label: 'Approve', kind: 'primary' }, { id: 'reject', label: 'Reject' }] : [{ id: 'close', label: 'Close', kind: 'primary' }],
      onAction: function (a) { if (a === 'close') { A.closeDrawer(); return; } A.closeDrawer(); decide(p, a); } });
  }
  function decide(p, act) {
    if (act === 'approve') {
      A.openModal({ title: 'Approve ' + F.money(p.amount, p.ccy) + ' to ' + p.beneficiary, body:
        H.summary([{ k: 'Payment', v: p.id }, { k: 'Value date', v: F.date(p.valueDate) }, { k: 'After your approval', v: p.approvals === 2 ? 'Goes to a second approver (dual control above £10m)' : 'Released to HSBC on the value date' }]) +
        H.check({ id: 'ap-ok', label: 'I have checked the beneficiary, amount and purpose against the supporting documents' }) +
        (p.approvals === 2 ? H.field({ id: 'ap-ref', label: 'Type the last four digits of the payment id to confirm', help: 'Dual-control payments need this extra confirmation.', inputmode: 'numeric' }) : '') +
        H.textarea({ id: 'ap-note', label: 'Note for the audit trail', optional: true, max: 300, rows: 2, help: 'Kept with the payment record.' }),
        actions: [{ id: 'go', label: 'Approve payment', kind: 'primary' }, { id: 'cancel', label: 'Cancel' }],
        onAction: function (a) {
          if (a === 'cancel') { return true; }
          var ok = true;
          if (!A.val('ap-ok')) { A.fail('ap-ok', 'Confirm you have checked the payment.'); ok = false; }
          if (p.approvals === 2 && A.val('ap-ref') !== p.id.slice(-4)) { A.fail('ap-ref', 'That does not match. Enter the last four digits of ' + p.id + '.'); ok = false; }
          if (!ok) { var f = document.querySelector('#modal [aria-invalid="true"]'); if (f) { f.focus(); } return false; }
          var st = p.approvals === 2 ? 'Awaiting second approver' : 'Approved';
          A.W.pay[p.id] = { status: st, at: new Date().toISOString(), note: A.val('ap-note') };
          A.W.audit.unshift({ at: new Date().toISOString(), ref: p.id, what: 'Approved by you — ' + st.toLowerCase(), note: A.val('ap-note') }); A.saveWork();
          A.toast(p.id + ' approved. ' + (p.approvals === 2 ? 'It now needs a second approver.' : 'It will be released on ' + F.date(p.valueDate) + '.'), 'ok');
          render(); return true;
        } });
    } else {
      A.openModal({ title: 'Reject ' + p.id, body: '<p class="t-ed-body">The initiator (' + esc(p.initiator) + ') sees your reason. Rejected payments cannot be reopened; a new one must be raised.</p>' +
        H.textarea({ id: 'rj-why', label: 'Reason for rejecting', max: 300, rows: 3, help: 'Required, at least 15 characters.' }),
        actions: [{ id: 'go', label: 'Reject payment', kind: 'primary' }, { id: 'cancel', label: 'Cancel' }],
        onAction: function (a) {
          if (a === 'cancel') { return true; }
          var why = A.val('rj-why'); if (why.length < 15) { A.fail('rj-why', 'Give a reason of at least 15 characters.'); document.getElementById('rj-why').focus(); return false; }
          A.W.pay[p.id] = { status: 'Rejected', at: new Date().toISOString(), reason: why };
          A.W.audit.unshift({ at: new Date().toISOString(), ref: p.id, what: 'Rejected by you', note: why }); A.saveWork();
          A.toast(p.id + ' rejected. ' + p.initiator.split(' (')[0] + ' has been told why.', 'info');
          render(); return true;
        } });
    }
  }
  A.onClick = function (e) {
    var v = e.target.closest('[data-pay-view]'); if (v) { view = v.getAttribute('data-pay-view'); A.PS.view = view; A.GRIDS['g-pay'].state.page = 1; A.renderGrid('g-pay'); A.segAll(); return; }
    if (e.target.closest('[data-action="export-pay"]')) { A.$('[data-export="g-pay"]').click(); }
  };
  function render() {
    var ps = pays(), idx = A.dayIdx(), ds = A.days();
    function cumBy(st) { return idx.map(function (i) { return ps.filter(function (p) { return (Array.isArray(st) ? st.indexOf(p.status) > -1 : p.status === st) && (p.status === 'Released' ? p.valueDate : p.created) <= D.DAYS[i]; }).reduce(function (a, p) { return a + p.gbp; }, 0); }); }
    A.renderKpis($('#kpis'), [{ id: 'mine', label: 'Awaiting your approval', series: cumBy('Awaiting your approval'), note: 'Value awaiting your approval, by the date each was created.' },
      { id: 'second', label: 'Awaiting second approver', series: cumBy('Awaiting second approver'), note: 'Dual-control payments with one approval.' },
      { id: 'released', label: 'Released', series: cumBy('Released'), note: 'Released to HSBC, cumulative by value date.' },
      { id: 'held', label: 'Held or rejected', series: cumBy(['Held for screening', 'Rejected']), note: 'Held by screening or rejected.' }]);
    var pend = ps.filter(function (p) { return /Awaiting|Held|Approved/.test(p.status); });
    var by = {}; pend.forEach(function (p) { by[p.ccy] = (by[p.ccy] || 0) + p.gbp; });
    var cc = Object.keys(by).sort(function (a, b) { return by[b] - by[a]; });
    if (cc.length) { A.drawChart('ch-byccy', { type: 'bar', categories: cc, series: [{ name: 'Pending value', values: cc.map(function (c) { return Math.round(by[c] / 1e5) / 10; }) }], unit: '£m', categoryLabel: 'Currency', caption: 'Value of payments not yet released, by currency, £ millions equivalent' }); } else { A.emptyChart('ch-byccy', 'No pending payments in this scope.'); }
    var pts = ps.filter(function (p) { return /Awaiting|Held/.test(p.status); }).sort(function (x, y) { return x.valueDate < y.valueDate ? -1 : 1; });
    if (pts.length > 1) {
      var dd = function (p) { return Math.round((new Date(p.valueDate) - new Date(D.AS_OF)) / 864e5); };
      A.drawChart('ch-scatter', { type: 'scatter', categories: pts.map(function (p) { return String(dd(p)); }), categoryLabel: 'Days to value date', unit: '£m',
        caption: 'Pending payments: days to value date against value, £ millions', series: [{ name: 'Payment value', values: pts.map(function (p) { return Math.round(p.gbp / 1e5) / 10; }) }] });
    } else { A.emptyChart('ch-scatter', 'Fewer than two pending payments in this scope.'); }
    var rel = idx.map(function (i) { return Math.round(ps.filter(function (p) { return p.status === 'Released' && p.valueDate === D.DAYS[i]; }).reduce(function (a, p) { return a + p.gbp; }, 0) / 1e5) / 10; });
    A.drawChart('ch-flow', { type: 'line', categories: ds.map(F.dshort), categoryLabel: 'Value date', series: [{ name: 'Released', values: rel }], unit: '£m', caption: 'Payments released by value date, £ millions' });
    var mine = ps.filter(function (p) { return p.status === 'Awaiting your approval'; }).sort(function (a, b) { return a.created < b.created ? -1 : 1; });
    $('#pay-mine').innerHTML = mine.length ? '<div class="l-stack" data-gap="m">' + mine.slice(0, 5).map(function (p) {
      return '<div class="l-row" data-gap="s" data-justify="between"><a class="tpl-link t-cm-label" href="#' + p.id + '" data-open-pay="' + p.id + '">' + esc(p.beneficiary) + '</a><span class="t-cm-figure-6">' + F.moneyM(p.amount, p.ccy) + '</span></div>';
    }).join('') + '</div>' : '<p class="t-ed-body-small">Nothing is waiting for you in this scope.</p>';
    $('#pay-rule').innerHTML = '<p class="t-ed-body-small">Payments above £10m need two approvers. Your approval of one of those moves it to a second approver; it is not released until both have approved. Payments held by HSBC sanctions screening cannot be approved here.</p>' +
      '<dl class="summary"><div class="summary__row"><dt class="summary__k t-cm-label">Dual-control payments pending</dt><dd class="summary__v t-cm-figure-5">' + ps.filter(function (p) { return p.approvals === 2 && /Awaiting/.test(p.status); }).length + '</dd></div>' +
      '<div class="summary__row"><dt class="summary__k t-cm-label">Your decisions in this browser</dt><dd class="summary__v t-cm-figure-5">' + Object.keys(A.W.pay).length + '</dd></div></dl>';
    A.renderGrid('g-pay');
  }
  document.addEventListener('click', function (e) { var a = e.target.closest('[data-open-pay]'); if (a) { e.preventDefault(); openPay(a.getAttribute('data-open-pay')); } });
  A.afterBoot = function () { if (A.PS.open) { openPay(A.PS.open); } };
  A.boot(render);
}());
