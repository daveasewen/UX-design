/* HSBC messages and service requests — read and reply to secure messages, raise a validated
   service request, answer HSBC when a request is waiting for you, and see service levels. */
(function () {
  'use strict';
  var A = APP, D = A.D, F = A.F, H = A.H, esc = A.esc, $ = A.$;
  var ST = { 'Submitted': 'inf', 'In progress': 'inf', 'Awaiting your input': 'warn', 'Completed': 'ok' };
  var CATTONE = { 'Action required': 'warn', 'Market insight': 'inf', 'Service update': 'inf', 'Statement ready': 'ok' };
  A.mountChart($('#host-srs'), { id: 'ch-srs', type: 'stacked-column', title: 'Requests opened each day', caption: 'Service requests opened per day by current status, count', legend: ['Open', 'Waiting for you', 'Completed'] });
  A.mountChart($('#host-sla'), { id: 'ch-sla', note: 'Open now; the date range does not apply', type: 'bullet', title: 'Days open against the service level', caption: 'Open requests: days open against the service level in days' });
  A.mountChart($('#host-topics'), { id: 'ch-topics', note: 'Group-wide messages: entity and region do not apply', type: 'bar', title: 'What HSBC wrote about', caption: 'Messages in the period by category, count' });
  function msgs() { return D.MESSAGES.filter(function (m) { return A.inWindow(m.date); }).map(function (m) { return Object.assign({}, m, { read: !!(A.W.msg[m.id] && A.W.msg[m.id].read), replies: (A.W.msg[m.id] && A.W.msg[m.id].replies) || [] }); }); }
  function reqs() { return A.calc.requests().filter(function (r) { return A.inScope(r.entity); }).map(function (r) { var w = A.W.msg[r.id]; return w && w.status ? Object.assign({}, r, { status: w.status, events: r.events.concat(w.events || []) }) : r; }); }
  A.grid($('#host-gmsg'), { id: 'g-msg', title: 'Messages from HSBC', placeholder: 'Search messages', size: 10, sort: 'date', dir: 'descending',
    rows: msgs, text: function (r) { return [r.subject, r.from, r.category, r.body].join(' '); }, rowLabel: function (r) { return (r.read ? '' : 'Unread. ') + 'Open message: ' + r.subject; },
    cols: [{ k: 'date', label: 'Received', fmt: function (r) { return F.date(r.date); }, csv: function (r) { return r.date; } }, { k: 'from', label: 'From' },
      { k: 'subject', label: 'Subject', html: function (r) { return '<span class="' + (r.read ? 't-cm-label' : 't-cm-button') + '">' + esc(r.subject) + '</span>'; } },
      { k: 'category', label: 'Category', html: function (r) { return H.stat(CATTONE[r.category], r.category); } }, { k: 'read', label: 'Read', fmt: function (r) { return r.read ? 'Read' : 'Unread'; }, val: function (r) { return r.read ? 1 : 0; } }],
    open: openMsg });
  A.grid($('#host-gsr'), { id: 'g-sr', title: 'Service requests', placeholder: 'Search requests', size: 10, sort: 'opened', dir: 'descending',
    tools: '<button type="button" class="clearbtn t-cm-button" data-export="g-sr" data-file="service-requests.csv">Export CSV</button>',
    rows: reqs, text: function (r) { return [r.id, r.type, r.subject, D.ENT[r.entity] ? D.ENT[r.entity].name : '', r.status].join(' '); }, rowLabel: function (r) { return 'Open request ' + r.id + ', ' + r.subject + ', ' + r.status; },
    cols: [{ k: 'id', label: 'Request' }, { k: 'subject', label: 'Subject' }, { k: 'opened', label: 'Opened', fmt: function (r) { return F.date(r.opened); }, csv: function (r) { return r.opened; } },
      { k: 'priority', label: 'Priority' }, { k: 'status', label: 'Status', html: function (r) { return H.stat(ST[r.status] || 'inf', r.status); }, csv: function (r) { return r.status; } }],
    open: openSr });
  function openMsg(id) {
    var m = msgs().filter(function (x) { return x.id === id; })[0] || D.MESSAGES.filter(function (x) { return x.id === id; })[0]; if (!m) { return; }
    A.W.msg[m.id] = Object.assign(A.W.msg[m.id] || {}, { read: true }); A.saveWork();
    A.openDrawer({ id: id, title: m.subject, body: H.summary([{ k: 'From', v: m.from + ', HSBC' }, { k: 'Received', v: F.date(m.date) }, { k: 'Category', html: H.stat(CATTONE[m.category], m.category) }]) +
      '<p class="t-ed-body">' + esc(m.body) + '</p>' + ((A.W.msg[m.id].replies || []).length ? H.timeline(A.W.msg[m.id].replies.map(function (r) { return { date: r.at, when: new Date(r.at).toLocaleString('en-GB'), title: 'You replied', desc: r.text, tone: 'ok' }; })) : ''),
      actions: [{ id: 'reply', label: 'Reply', kind: 'primary' }, { id: 'unread', label: 'Mark as unread' }],
      onAction: function (a) {
        if (a === 'unread') { A.W.msg[m.id].read = false; A.saveWork(); A.closeDrawer(); render(); A.toast('Marked as unread.', 'info'); return; }
        A.closeDrawer(); reply(m);
      } });
    render();
  }
  function reply(m) {
    A.openModal({ title: 'Reply: ' + m.subject, body: H.textarea({ id: 'rp-text', label: 'Your reply', max: 1000, rows: 5, help: 'Sent through HSBC secure messaging. At least 5 characters.' }),
      actions: [{ id: 'send', label: 'Send reply', kind: 'primary' }, { id: 'cancel', label: 'Cancel' }],
      onAction: function (a) {
        if (a === 'cancel') { return true; }
        var t = A.val('rp-text'); if (t.length < 5) { A.fail('rp-text', 'Write a reply of at least 5 characters.'); document.getElementById('rp-text').focus(); return false; }
        var w = A.W.msg[m.id] = A.W.msg[m.id] || {}; w.read = true; w.replies = (w.replies || []).concat([{ at: new Date().toISOString(), text: t }]);
        A.W.audit.unshift({ at: new Date().toISOString(), ref: m.id, what: 'Replied to ' + m.subject }); A.saveWork(); A.toast('Reply sent to ' + m.from + '.', 'ok'); render(); return true;
      } });
  }
  function openSr(id) {
    var r = reqs().filter(function (x) { return x.id === id; })[0]; if (!r) { return; }
    var waiting = r.status === 'Awaiting your input';
    A.openDrawer({ id: id, title: r.id + ' · ' + r.type, body: (waiting ? H.alert('warn', 'HSBC needs something from you.', 'Reply below to move this request on.') : '') +
      H.summary([{ k: 'Subject', v: r.subject }, { k: 'Entity', v: D.ENT[r.entity] ? D.ENT[r.entity].name : r.entity }, { k: 'Opened', v: F.date(r.opened) }, { k: 'Service level', v: r.sla + ' business day' + (r.sla === 1 ? '' : 's') }, { k: 'Priority', v: r.priority }, { k: 'Status', html: H.stat(ST[r.status] || 'inf', r.status) }]) +
      H.timeline(r.events.slice().reverse().map(function (e) { return Object.assign({}, e, { when: e.date.length > 10 ? new Date(e.date).toLocaleString('en-GB') : null }); })),
      actions: waiting ? [{ id: 'respond', label: 'Respond to HSBC', kind: 'primary' }, { id: 'close', label: 'Close' }] : [{ id: 'close', label: 'Close', kind: 'primary' }],
      onAction: function (a) {
        if (a === 'close') { A.closeDrawer(); return; }
        A.closeDrawer();
        A.openModal({ title: 'Respond on ' + r.id, body: H.textarea({ id: 'sr-resp', label: 'Your response', max: 800, rows: 4, help: 'Required, at least 10 characters.' }),
          actions: [{ id: 'send', label: 'Send response', kind: 'primary' }, { id: 'cancel', label: 'Cancel' }],
          onAction: function (x) {
            if (x === 'cancel') { return true; }
            var t = A.val('sr-resp'); if (t.length < 10) { A.fail('sr-resp', 'Write at least 10 characters.'); document.getElementById('sr-resp').focus(); return false; }
            A.W.msg[r.id] = { status: 'In progress', events: [{ date: new Date().toISOString(), title: 'You responded: ' + t, tone: 'ok' }] };
            A.W.audit.unshift({ at: new Date().toISOString(), ref: r.id, what: 'Responded on ' + r.id }); A.saveWork(); A.toast('Response sent. ' + r.id + ' is back with HSBC.', 'ok'); render(); return true;
          } });
      } });
  }
  function newSr() {
    var ents = A.scopedEntities().length ? A.scopedEntities() : D.ENTITIES;
    A.openForm({ title: 'New service request', body:
      H.radios({ name: 'ns-type', legend: 'Request type', value: '', options: ['Mandate change', 'User access', 'Payment investigation', 'Statement copy', 'Facility amendment', 'KYC document'].map(function (t) { return { v: t, label: t }; }) }) +
      H.radios({ name: 'ns-ent', legend: 'Entity', value: ents[0].id, options: ents.map(function (e) { return { v: e.id, label: e.name }; }) }) +
      H.field({ id: 'ns-subj', label: 'Subject', help: 'A short summary HSBC will see first.' }) +
      H.textarea({ id: 'ns-body', label: 'Details', max: 1000, rows: 4, help: 'Required, at least 20 characters. Do not include passwords or security codes.' }) +
      H.check({ id: 'ns-urgent', label: 'This is urgent (same-day handling)' }),
      actions: [{ id: 'send', label: 'Submit request', kind: 'primary' }, { id: 'cancel', label: 'Cancel' }],
      onAction: function (a) {
        if (a === 'cancel') { return true; }
        var ty = (document.querySelector('input[name="ns-type"]:checked') || {}).value, en = (document.querySelector('input[name="ns-ent"]:checked') || {}).value, sj = A.val('ns-subj'), bd = A.val('ns-body'), ok = true;
        if (!ty) { A.fail('ns-type', 'Choose a request type.'); ok = false; }
        if (sj.length < 5) { A.fail('ns-subj', 'Give a subject of at least 5 characters.'); ok = false; }
        if (bd.length < 20) { A.fail('ns-body', 'Give at least 20 characters of detail.'); ok = false; }
        if (/\b(password|passcode|pin)\b/i.test(bd)) { A.fail('ns-body', 'Remove anything that looks like a password, passcode or PIN.'); ok = false; }
        if (!ok) { var f = document.querySelector('#drawer [aria-invalid="true"], #modal [aria-invalid="true"]'); if (f) { f.focus(); } return false; }
        var id = 'SR-' + String(30000 + A.W.sr.length + 1);
        A.W.sr.unshift({ id: id, type: ty, entity: en, subject: sj, opened: D.AS_OF, updated: D.AS_OF, status: 'Submitted', sla: { 'Mandate change': 5, 'User access': 2, 'Payment investigation': 3, 'Statement copy': 1, 'Facility amendment': 10, 'KYC document': 5 }[ty], priority: A.val('ns-urgent') ? 'High' : 'Normal', events: [{ date: new Date().toISOString(), title: 'Request submitted: ' + bd, tone: 'inf' }] });
        A.W.audit.unshift({ at: new Date().toISOString(), ref: id, what: 'Raised ' + id + ' — ' + ty }); A.saveWork();
        A.toast('Request ' + id + ' submitted to HSBC.', 'ok'); render(); return true;
      } });
  }
  A.onClick = function (e) {
    if (e.target.closest('[data-action="new-sr"]')) { newSr(); }
    if (e.target.closest('[data-action="export-sr"]')) { A.$('[data-export="g-sr"]').click(); }
    var o = e.target.closest('[data-open-sr]'); if (o) { e.preventDefault(); openSr(o.getAttribute('data-open-sr')); }
  };
  function render() {
    var ms = msgs(), rs = reqs(), idx = A.dayIdx(), ds = A.days();
    var cum = function (fn, list) { return idx.map(function (i) { return list.filter(function (x) { return (x.date || x.opened) <= D.DAYS[i] && fn(x); }).length; }); };
    A.renderKpis($('#kpis'), [{ id: 'unread', label: 'Unread messages', count: true, series: cum(function (m) { return !m.read; }, ms), note: 'Unread messages received in the period.' },
      { id: 'action', label: 'Messages needing action', count: true, series: cum(function (m) { return m.category === 'Action required'; }, ms), note: 'Messages HSBC marked as needing action.' },
      { id: 'open', label: 'Open service requests', count: true, series: cum(function (r) { return r.status !== 'Completed'; }, rs), note: 'Requests not yet completed.' },
      { id: 'input', label: 'Waiting for your input', count: true, series: cum(function (r) { return r.status === 'Awaiting your input'; }, rs), note: 'Requests where HSBC is waiting for you.' }]);
    var inWin = rs.filter(function (r) { return A.inWindow(r.opened); });
    if (inWin.length) { A.drawChart('ch-srs', { type: 'stacked-column', categories: ds.map(F.dshort), categoryLabel: 'Date', caption: 'Service requests opened per day by current status, count',
      series: [['Open', function (r) { return r.status === 'Submitted' || r.status === 'In progress'; }], ['Waiting for you', function (r) { return r.status === 'Awaiting your input'; }], ['Completed', function (r) { return r.status === 'Completed'; }]].map(function (s) { return { name: s[0], values: idx.map(function (i) { return inWin.filter(function (r) { return r.opened === D.DAYS[i] && s[1](r); }).length; }) }; }) }); } else { A.emptyChart('ch-srs'); }
    var open = rs.filter(function (r) { return r.status !== 'Completed'; }).slice(0, 8);
    if (open.length) { A.drawChart('ch-sla', { type: 'bullet', categories: open.map(function (r) { return r.id; }), categoryLabel: 'Request', unit: 'd', caption: 'Open requests: days open against the service level in days',
      series: [{ name: 'Days open', values: open.map(function (r) { return Math.max(0, Math.round((new Date(D.AS_OF) - new Date(r.opened)) / 864e5)); }) }, { name: 'Service level', values: open.map(function (r) { return r.sla; }) }] }); } else { A.emptyChart('ch-sla', 'No open requests in this scope.'); }
    var cats = ['Action required', 'Market insight', 'Service update', 'Statement ready'];
    if (ms.length) { A.drawChart('ch-topics', { type: 'bar', categories: cats, categoryLabel: 'Category', caption: 'Messages in the period by category, count', series: [{ name: 'Messages', values: cats.map(function (c) { return ms.filter(function (m) { return m.category === c; }).length; }) }] }); } else { A.emptyChart('ch-topics'); }
    var wt = rs.filter(function (r) { return r.status === 'Awaiting your input'; });
    $('#sr-waiting').innerHTML = wt.length ? '<div class="l-stack" data-gap="m">' + wt.slice(0, 5).map(function (r) { return '<div class="l-row" data-gap="s" data-justify="between"><a class="tpl-link t-cm-label" href="#' + r.id + '" data-open-sr="' + r.id + '">' + esc(r.id + ' · ' + r.subject) + '</a><span class="status warn" data-carries="label"><span class="dot" aria-hidden="true"></span><span class="t-cm-legal">Since ' + F.dshort(r.updated) + '</span></span></div>'; }).join('') + '</div>' : '<p class="t-ed-body-small">Nothing is waiting for you.</p>';
    $('#contacts').innerHTML = '<dl class="summary"><div class="summary__row"><dt class="summary__k t-cm-label">Relationship director</dt><dd class="summary__v t-cm-label">Global Banking, London</dd></div><div class="summary__row"><dt class="summary__k t-cm-label">Treasury service desk</dt><dd class="summary__v t-cm-label">Secure message, 24 hours</dd></div><div class="summary__row"><dt class="summary__k t-cm-label">Trade services</dt><dd class="summary__v t-cm-label">Hong Kong and London</dd></div></dl>';
    A.renderGrid('g-msg'); A.renderGrid('g-sr');
  }
  A.afterBoot = function () { var o = A.PS.open; if (o) { if (/^MSG/.test(o)) { openMsg(o); } else { openSr(o); } } };
  A.boot(render);
}());
