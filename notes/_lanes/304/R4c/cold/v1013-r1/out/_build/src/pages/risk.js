/* Risk and limits — exposure against limit by region (the overview drills through to here), bank
   counterparties, exceptions you acknowledge with an audit note, and the underlying positions. */
(function () {
  'use strict';
  var A = APP, D = A.D, F = A.F, H = A.H, esc = A.esc, $ = A.$;
  A.mountChart($('#host-regions'), { id: 'ch-regions', note: 'As at 25 Sep 2026', type: 'grouped-column', title: 'Net exposure against the regional limit', caption: 'Net exposure and limit by region, £ millions', legend: ['Net exposure', 'Limit'] });
  A.mountChart($('#host-cp'), { id: 'ch-cp', note: 'Bank counterparties: filtered by region only', type: 'scatter', title: 'Two banks sit above 90% of their limit', caption: 'Bank counterparties: limit used, per cent, against exposure, £ millions' });
  A.mountChart($('#host-box'), { id: 'ch-box', note: 'Bank counterparties: filtered by region and dates', type: 'boxplot', title: 'Daily counterparty exposure moved most in the UK', caption: 'Spread of daily bank counterparty exposure by region over the period, £ millions' });
  var SEV = { Material: 'err', High: 'warn', Medium: 'inf' };
  function rate(ccy, i) { var d = D.DAYS[i], ser = D.FX_SERIES[ccy]; if (!ser) { return 1; } var r = ser.filter(function (x) { return x.date <= d; }).pop() || ser[0]; return r.close; }
  function pos() { return D.POSITIONS.filter(function (p) { return A.inScope(p.entity); }); }
  function cps() { return D.COUNTERPARTIES.filter(function (c) { return A.S.region === 'all' || c.region === A.S.region; }); }
  A.grid($('#host-gexc'), { id: 'g-exc', title: 'Exceptions', placeholder: 'Search exceptions', size: 10, sort: 'raised', dir: 'descending',
    tools: '<button type="button" class="clearbtn t-cm-button" data-export="g-exc" data-file="exceptions.csv">Export CSV</button>',
    rows: function () { return A.calc.exceptions().filter(function (x) { return A.inScope(x.entity); }); },
    text: function (r) { return [r.id, r.title, r.type, r.severity, D.ENT[r.entity].name, r.owner, r.status].join(' '); }, rowLabel: function (r) { return 'Open exception ' + r.title + ', ' + r.severity + ', ' + r.status; },
    cols: [{ k: 'raised', label: 'Raised', fmt: function (r) { return F.date(r.raised); }, csv: function (r) { return r.raised; } }, { k: 'title', label: 'Exception' },
      { k: 'severity', label: 'Severity', html: function (r) { return H.stat(SEV[r.severity], r.severity); }, csv: function (r) { return r.severity; }, val: function (r) { return { Material: 0, High: 1, Medium: 2 }[r.severity]; } },
      { k: 'entity', label: 'Entity', fmt: function (r) { return D.ENT[r.entity].short; } }, { k: 'owner', label: 'Owner' },
      { k: 'status', label: 'Status', html: function (r) { return H.stat(r.status === 'Open' ? 'warn' : 'ok', r.status); }, csv: function (r) { return r.status + (r.notes.length ? ' — ' + r.notes[0].note : ''); } }],
    open: openExc });
  A.grid($('#host-gpos'), { id: 'g-pos', title: 'Underlying positions', placeholder: 'Search entity, currency or position type', size: 25, sort: 'abs', dir: 'descending',
    tools: '<button type="button" class="clearbtn t-cm-button" data-export="g-pos" data-file="positions.csv">Export CSV</button>',
    rows: function () { return pos().map(function (p) { return Object.assign({}, p, { abs: Math.abs(p.gbp), region: D.ENT[p.entity].region }); }); },
    text: function (r) { return [D.ENT[r.entity].name, r.ccy, r.type, A.regionName(r.region), r.tenor].join(' '); }, rowLabel: function (r) { return r.type + ' in ' + r.ccy + ' for ' + D.ENT[r.entity].short; },
    cols: [{ k: 'entity', label: 'Entity', fmt: function (r) { return D.ENT[r.entity].short; } }, { k: 'region', label: 'Region', fmt: function (r) { return A.regionName(r.region); } }, { k: 'ccy', label: 'Currency' },
      { k: 'type', label: 'Position' }, { k: 'tenor', label: 'Tenor' }, { k: 'local', label: 'Local amount', num: true, fmt: function (r) { return F.moneyM(r.local, r.ccy); } },
      { k: 'abs', label: 'In GBP', num: true, fmt: function (r) { return F.gbpM(r.gbp); }, csv: function (r) { return r.gbp; } }],
    open: function (id) {
      var p = D.POSITIONS.filter(function (x) { return x.id === id; })[0]; if (!p) { return; }
      var lim = D.CCY_LIMITS[p.ccy], net = pos().filter(function (x) { return x.ccy === p.ccy; }).reduce(function (a, x) { return a + x.gbp; }, 0);
      A.openDrawer({ id: id, title: p.type + ' · ' + p.ccy + ' · ' + D.ENT[p.entity].short, body: H.summary([{ k: 'Entity', v: D.ENT[p.entity].name }, { k: 'Region', v: A.regionName(D.ENT[p.entity].region) }, { k: 'Local amount', v: F.money(p.local, p.ccy) },
        { k: 'GBP equivalent', v: F.gbpM(p.gbp) }, { k: 'Tenor', v: p.tenor }]) + H.limit({ id: 'ccy-' + p.ccy, label: 'Net ' + p.ccy + ' position against its limit (in scope)', used: Math.abs(net), limit: lim }),
        actions: [{ id: 'close', label: 'Close', kind: 'primary' }], onAction: function () { A.closeDrawer(); } });
    } });
  function openExc(id) {
    var x = A.calc.exceptions().filter(function (e) { return e.id === id; })[0]; if (!x) { return; }
    var tl = [{ date: x.raised, title: 'Raised: ' + x.type, desc: 'Owner: ' + x.owner, tone: SEV[x.severity] === 'inf' ? 'inf' : 'warn' }].concat(x.notes.slice().reverse().map(function (n) { return { date: n.at, when: new Date(n.at).toLocaleString('en-GB'), title: 'Acknowledged by ' + n.by, desc: n.note, tone: 'ok' }; }));
    A.openDrawer({ id: id, title: x.title, body: H.alert(x.severity === 'Material' ? 'err' : 'warn', x.severity + ' exception.', x.detail) +
      H.summary([{ k: 'Type', v: x.type }, { k: 'Entity', v: D.ENT[x.entity].name }, { k: 'Measured', v: x.value > 100 ? F.gbpM(x.value) : x.value ? x.value + 'x' : '—' }, { k: 'Limit', v: x.limit > 100 ? F.gbpM(x.limit) : x.limit ? x.limit + 'x' : '—' },
        { k: 'Owner', v: x.owner }, { k: 'Status', html: H.stat(x.status === 'Open' ? 'warn' : 'ok', x.status) }]) + H.timeline(tl.reverse()),
      actions: [{ id: 'ack', label: x.status === 'Open' ? 'Acknowledge with a note' : 'Add an audit note', kind: 'primary' }, { id: 'close', label: 'Close' }],
      onAction: function (a) { if (a === 'close') { A.closeDrawer(); return; } A.closeDrawer(); ack(x); } });
  }
  function ack(x) {
    A.openModal({ title: (x.status === 'Open' ? 'Acknowledge: ' : 'Add a note: ') + x.title, body: '<p class="t-ed-body">Acknowledging records that you have seen this exception and what should happen next. It does not close it; the owner (' + esc(x.owner) + ') resolves it.</p>' +
      H.textarea({ id: 'ak-note', label: 'Audit note', max: 400, rows: 4, help: 'Required, at least 20 characters. Kept permanently with the exception.' }) +
      H.check({ id: 'ak-own', label: 'I have agreed the next step with the owner' }),
      actions: [{ id: 'go', label: x.status === 'Open' ? 'Acknowledge' : 'Add note', kind: 'primary' }, { id: 'cancel', label: 'Cancel' }],
      onAction: function (a) {
        if (a === 'cancel') { return true; }
        var n = A.val('ak-note'), ok = true;
        if (n.length < 20) { A.fail('ak-note', 'Write at least 20 characters so the note stands on its own later.'); ok = false; }
        if (!A.val('ak-own')) { A.fail('ak-own', 'Confirm you have agreed the next step with the owner.'); ok = false; }
        if (!ok) { var f = document.querySelector('#modal [aria-invalid="true"]'); if (f) { f.focus(); } return false; }
        A.W.exc[x.id] = (A.W.exc[x.id] || []).concat([{ at: new Date().toISOString(), by: 'You (chief executive)', note: n }]);
        A.W.audit.unshift({ at: new Date().toISOString(), ref: x.id, what: 'Acknowledged ' + x.id, note: n }); A.saveWork();
        A.toast('Acknowledged ' + x.id + '. The note is on the audit trail.', 'ok'); render(); return true;
      } });
  }
  A.onClick = function (e) {
    if (e.target.closest('[data-action="export-pos"]')) { A.$('[data-export="g-pos"]').click(); }
    if (e.target.closest('[data-action="export-exc"]')) { A.$('[data-export="g-exc"]').click(); }
    var o = e.target.closest('[data-open-exc]'); if (o) { e.preventDefault(); openExc(o.getAttribute('data-open-exc')); }
  };
  function render() {
    var ps = pos(), idx = A.dayIdx();
    function series(fn) { return idx.map(function (i) { return ps.filter(fn).reduce(function (a, p) { return a + (p.ccy === 'GBP' ? p.gbp : p.local / rate(p.ccy, i)); }, 0); }); }
    var cpS = idx.map(function (i) { return cps().reduce(function (a, c) { return a + c.series[i]; }, 0); });
    A.renderKpis($('#kpis'), [{ id: 'net', label: 'Net exposure', series: series(function () { return true; }), note: 'Sum of positions in scope, revalued daily at illustrative rates.' },
      { id: 'gross', label: 'Gross exposure', series: idx.map(function (i) { return ps.reduce(function (a, p) { return a + Math.abs(p.ccy === 'GBP' ? p.gbp : p.local / rate(p.ccy, i)); }, 0); }), note: 'Sum of absolute positions.' },
      { id: 'cp', label: 'Bank counterparty exposure', series: cpS, note: 'Deposits and derivative exposure to banks in the selected region.' },
      { id: 'unhedged', label: 'Unhedged foreign exposure', series: series(function (p) { return p.ccy !== 'GBP' && (p.type === 'Receivables' || p.type === 'Cash'); }).map(function (v) { return Math.max(0, v - D.HEDGES.filter(function (h) { return A.inScope(h.entity); }).reduce(function (a, h) { return a + h.gbp; }, 0) * 0.5); }), note: 'Foreign cash and receivables less half of forward cover (illustrative method).' }]);
    var byR = A.calc.exposureByRegionCcy(), regs = D.REGIONS.filter(function (r) { return byR[r.id]; });
    var net = function (r) { return Object.keys(byR[r.id]).reduce(function (a, c) { return a + byR[r.id][c]; }, 0); };
    if (regs.length) {
      A.drawChart('ch-regions', { type: 'grouped-column', categories: regs.map(function (r) { return r.name; }), categoryLabel: 'Region', unit: '£m', caption: 'Net exposure and limit by region, £ millions',
        series: [{ name: 'Net exposure', values: regs.map(function (r) { return Math.max(0, Math.round(net(r) / 1e5) / 10); }) }, { name: 'Limit', values: regs.map(function (r) { return D.REGION_LIMITS[r.id] / 1e6; }) }] });
      $('#reg-limits').innerHTML = '<div class="ceo-stack">' + regs.slice().sort(function (a, b) { return net(b) / D.REGION_LIMITS[b.id] - net(a) / D.REGION_LIMITS[a.id]; }).slice(0, 3).map(function (r) { return H.limit({ id: 'reg-' + r.id, label: r.name, used: Math.max(0, net(r)), limit: D.REGION_LIMITS[r.id] }); }).join('') + '</div>';
    } else { A.emptyChart('ch-regions'); $('#reg-limits').innerHTML = '<p class="t-ed-body-small">No positions in this scope.</p>'; }
    var c = cps();
    if (c.length > 1) { A.drawChart('ch-cp', { type: 'scatter', categories: c.map(function (x) { return String(Math.round(x.exposure / x.limit * 1000) / 10); }), categoryLabel: 'Limit used (%)', unit: '£m', caption: 'Bank counterparties: limit used, per cent, against exposure, £ millions',
      series: [{ name: 'Exposure', values: c.map(function (x) { return Math.round(x.exposure / 1e5) / 10; }) }] }); } else { A.emptyChart('ch-cp', 'Fewer than two bank counterparties in this region.'); }
    var bx = D.REGIONS.filter(function (r) { return D.COUNTERPARTIES.some(function (x) { return x.region === r.id; }) && (A.S.region === 'all' || A.S.region === r.id); }).map(function (r) {
      var daily = idx.map(function (i) { return D.COUNTERPARTIES.filter(function (x) { return x.region === r.id; }).reduce(function (a, x) { return a + x.series[i]; }, 0) / 1e6; }).sort(function (a, b) { return a - b; });
      var q = function (f) { var k = (daily.length - 1) * f, lo = Math.floor(k), hi = Math.ceil(k); return Math.round((daily[lo] + (daily[hi] - daily[lo]) * (k - lo)) * 10) / 10; };
      return { n: r.name, v: [q(0), q(0.25), q(0.5), q(0.75), q(1)] };
    });
    if (bx.length) { A.drawChart('ch-box', { type: 'boxplot', categories: bx.map(function (b) { return b.n; }), categoryLabel: 'Region', unit: '£m', caption: 'Spread of daily bank counterparty exposure by region over the period, £ millions',
      series: ['Minimum', 'Lower quartile', 'Median', 'Upper quartile', 'Maximum'].map(function (nm, k) { return { name: nm, values: bx.map(function (b) { return b.v[k]; }) }; }) }); } else { A.emptyChart('ch-box'); }
    var ex = A.calc.exceptions().filter(function (x) { return A.inScope(x.entity) && x.status === 'Open'; });
    $('#exc-summary').innerHTML = '<dl class="summary tpl-na-head"><div class="summary__row"><dt class="summary__k t-cm-label">Open and unacknowledged <span class="t-cm-legal">' + ex.filter(function (x) { return x.severity === 'Material'; }).length + ' material</span></dt><dd class="summary__v t-cm-figure-5">' + ex.length + '</dd></div></dl>' +
      '<div class="l-stack" data-gap="m">' + ex.slice(0, 4).map(function (x) { return '<div class="l-row" data-gap="s" data-justify="between"><a class="tpl-link t-cm-label" href="#' + x.id + '" data-open-exc="' + x.id + '">' + esc(x.title) + '</a>' + '<span class="status ' + SEV[x.severity] + '" data-carries="label"><span class="dot" aria-hidden="true"></span><span class="t-cm-legal">' + x.severity + '</span></span></div>'; }).join('') + '</div>';
    A.renderGrid('g-exc'); A.renderGrid('g-pos');
  }
  A.afterBoot = function () {
    if (A.PS.open) { if (/^EXC/.test(A.PS.open)) { openExc(A.PS.open); } else { A.GRIDS['g-pos'].open(A.PS.open); } return; }
    if (location.hash === '#positions') {
      var t = $('#host-gpos'); t.scrollIntoView(); var s = $('[data-grid-search="g-pos"]'); if (s) { s.focus({ preventScroll: true }); }
      A.toast('Showing the positions and limits behind ' + (A.S.region !== 'all' ? A.regionName(A.S.region) : 'the selected exposure') + '.', 'info');
    }
  };
  A.boot(render);
}());
