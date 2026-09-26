/* Settings — colour mode, the default view new sessions start in, notification preferences, and
   the prototype's stored data (export the audit trail, reset the simulated workflow). */
(function () {
  'use strict';
  var A = APP, D = A.D, F = A.F, H = A.H, esc = A.esc, $ = A.$;
  var PREF = A.PS.prefs ? JSON.parse(A.PS.prefs) : { email: true, sms: false, digest: true, approvals: true };
  A.mountChart($('#host-activity'), { id: 'ch-activity', note: 'Your actions in this browser', type: 'column', title: 'What you have done in this prototype, by day', caption: 'Your actions recorded on the audit trail per day, count' });
  function render() {
    $('#set-appearance').innerHTML = '<div class="ceo-stack"><p class="t-ed-body-small">Common theme, in light or dark. The switch in the top bar does the same thing.</p>' +
      '<div class="cn-segmented-control"><div class="seg m" role="group" aria-label="Colour mode"><span class="ind" aria-hidden="true"></span><button type="button" data-theme-btn="light" aria-pressed="' + (A.S.theme === 'light') + '">Light</button><button type="button" data-theme-btn="dark" aria-pressed="' + (A.S.theme === 'dark') + '">Dark</button></div></div>' +
      H.check({ id: 'st-rail', label: 'Keep the navigation collapsed to icons', role: 'switch', checked: A.S.nav === 'rail' }) + '</div>';
    $('#set-default').innerHTML = '<div class="ceo-stack">' + H.radios({ name: 'st-region', legend: 'Region shown when you arrive', value: A.S.region, options: [{ v: 'all', label: 'All regions' }].concat(D.REGIONS.map(function (r) { return { v: r.id, label: r.name }; })) }) +
      H.radios({ name: 'st-days', legend: 'Date range', value: String(A.S.days), options: [{ v: '7', label: 'Last 7 days' }, { v: '14', label: 'Last 14 days' }, { v: '30', label: 'Last 30 days' }] }) + '</div>';
    $('#set-notify').innerHTML = '<div class="ceo-stack"><p class="t-ed-body-small">Simulated: no message leaves this prototype.</p>' +
      H.check({ id: 'nt-approvals', label: 'Tell me when a payment needs my approval', role: 'switch', checked: PREF.approvals }) +
      H.check({ id: 'nt-email', label: 'Material risk exceptions by email', role: 'switch', checked: PREF.email }) +
      H.check({ id: 'nt-sms', label: 'Material risk exceptions by text message', role: 'switch', checked: PREF.sms }) +
      H.check({ id: 'nt-digest', label: 'A daily digest at 07:00', role: 'switch', checked: PREF.digest }) + '</div>';
    $('#set-data').innerHTML = '<div class="ceo-stack"><p class="t-ed-body-small">Your approvals, acknowledgements, requests and exports are kept in this browser only.</p>' +
      '<dl class="summary"><div class="summary__row"><dt class="summary__k t-cm-label">Audit entries</dt><dd class="summary__v t-cm-figure-5">' + A.W.audit.length + '</dd></div><div class="summary__row"><dt class="summary__k t-cm-label">Requests you raised</dt><dd class="summary__v t-cm-figure-5">' + A.W.sr.length + '</dd></div></dl>' +
      '<div class="l-row" data-gap="m"><button type="button" class="btn secondary" data-action="export-audit">Export audit trail (CSV)</button><button type="button" class="btn tertiary" data-action="reset">Reset prototype data</button></div></div>';
    var idx = A.dayIdx(), ds = A.days();
    var per = idx.map(function (i) { return A.W.audit.filter(function (a) { return a.at.slice(0, 10) === D.DAYS[i]; }).length; });
    /* audit timestamps are real clock time; anything after the data's as-at date counts on the last day */
    per[per.length - 1] += A.W.audit.filter(function (a) { return a.at.slice(0, 10) > D.AS_OF; }).length;
    A.drawChart('ch-activity', { type: 'column', categories: ds.map(F.dshort), categoryLabel: 'Date', caption: 'Your actions recorded on the audit trail per day, count', series: [{ name: 'Actions', values: per }] });
    A.segAll();
  }
  A.onChange = function (e) {
    var t = e.target;
    if (t.id === 'st-rail') { var sn = $('#nav-main'); if (sn.classList.contains('is-rail') !== t.checked) { $('[data-navtoggle]').click(); } A.toast(t.checked ? 'Navigation collapsed.' : 'Navigation expanded.', 'info'); }
    if (t.name === 'st-region') { A.S.region = t.value; A.S.entity = 'all'; A.persist(); A.toast('New visits open on ' + (t.value === 'all' ? 'all regions' : A.regionName(t.value)) + '.', 'ok'); }
    if (t.name === 'st-days') { A.S.days = +t.value; A.persist(); A.toast('New visits show the last ' + t.value + ' days.', 'ok'); render(); }
    if (/^nt-/.test(t.id)) { PREF[t.id.slice(3)] = t.checked; A.PS.prefs = JSON.stringify(PREF); A.persist(); A.toast('Notification preference saved.', 'ok'); }
  };
  A.onClick = function (e) {
    if (e.target.closest('[data-action="export-audit"]')) { A.csv('audit-trail.csv', [['When', 'What', 'Reference', 'Note']].concat(A.W.audit.map(function (a) { return [a.at, a.what, a.ref || '', a.note || '']; }))); render(); }
    if (e.target.closest('[data-action="reset"]')) {
      A.openModal({ title: 'Reset prototype data?', body: '<p class="t-ed-body">This clears every approval, acknowledgement, request, reply and export recorded in this browser. Filters and colour mode are kept.</p>' + H.check({ id: 'rs-ok', label: 'I understand this cannot be undone' }),
        actions: [{ id: 'go', label: 'Reset data', kind: 'primary' }, { id: 'cancel', label: 'Cancel' }],
        onAction: function (a) {
          if (a === 'cancel') { return true; }
          if (!A.val('rs-ok')) { A.fail('rs-ok', 'Confirm you understand.'); document.getElementById('rs-ok').focus(); return false; }
          ['pay', 'exc', 'msg'].forEach(function (k) { A.W[k] = {}; }); ['sr', 'audit', 'runs'].forEach(function (k) { A.W[k] = []; }); A.saveWork(); render(); A.toast('Prototype data reset.', 'ok'); return true;
        } });
    }
    if (e.target.closest('[data-theme-btn]')) { setTimeout(render, 0); }
  };
  A.boot(render);
}());
