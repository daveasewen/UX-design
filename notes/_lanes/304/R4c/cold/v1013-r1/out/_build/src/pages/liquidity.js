/* Liquidity and funding — can we fund our plans? Liquidity against utilisation (combo), facility
   headroom (Limits-meter), utilisation against the policy ceiling (bullet), thirty-day shape
   (sparklines), the facilities grid, and a validated drawdown request. */
(function () {
  'use strict';
  var A = APP, D = A.D, F = A.F, H = A.H, esc = A.esc, $ = A.$;
  A.mountChart($('#host-combo'), { id: 'ch-combo', type: 'combo', title: 'Liquidity held up as facility use edged higher', caption: 'Available liquidity, £ millions (columns), and committed facility utilisation, per cent (line)', legend: ['Available liquidity', 'Utilisation'] });
  A.mountChart($('#host-bullet'), { id: 'ch-bullet', note: 'As at 25 Sep 2026', type: 'bullet', title: 'Drawn against limit, and the 75% ceiling', caption: 'Drawn as a share of limit by facility, per cent, against a 75% ceiling', max: 100 });
  $('#sparks').innerHTML = '<div class="ceo-stack"><p class="t-cm-caption">Cash</p><div id="sp1"></div><p class="t-cm-caption">Undrawn committed facilities</p><div id="sp2"></div><p class="t-cm-caption">Funding headroom</p><div id="sp3"></div></div>';
  A.mountChart($('#sp1'), { id: 'ch-sp1', type: 'spark', caption: 'Cash over the period' });
  A.mountChart($('#sp2'), { id: 'ch-sp2', type: 'spark', caption: 'Undrawn committed facilities over the period' });
  A.mountChart($('#sp3'), { id: 'ch-sp3', type: 'spark', caption: 'Funding headroom over the period' });
  function facs() { return D.FACILITIES.filter(function (f) { return A.inScope(f.entity); }).map(function (f) { return Object.assign({}, f, { drawnG: D.toGBP(f.drawn, f.ccy), limitG: D.toGBP(f.limit, f.ccy), util: f.drawn / f.limit * 100 }); }); }
  A.grid($('#host-gfac'), { id: 'g-fac', title: 'Facilities', placeholder: 'Search facility, type or entity', size: 10, sort: 'util', dir: 'descending',
    tools: '<button type="button" class="clearbtn t-cm-button" data-export="g-fac" data-file="facilities.csv">Export CSV</button>',
    rows: facs, text: function (r) { return [r.name, r.type, D.ENT[r.entity].name, r.ccy, r.margin].join(' '); }, rowLabel: function (r) { return 'Open facility ' + r.name; },
    cols: [{ k: 'name', label: 'Facility' }, { k: 'type', label: 'Type' }, { k: 'committed', label: 'Basis', fmt: function (r) { return r.committed ? 'Committed' : 'Uncommitted'; } },
      { k: 'entity', label: 'Borrower', fmt: function (r) { return D.ENT[r.entity].short; } }, { k: 'maturity', label: 'Maturity', fmt: function (r) { return F.date(r.maturity); } },
      { k: 'limitG', label: 'Limit', num: true, fmt: function (r) { return F.gbpM(r.limitG); } }, { k: 'drawnG', label: 'Drawn', num: true, fmt: function (r) { return F.gbpM(r.drawnG); } },
      { k: 'util', label: 'Utilisation', num: true, fmt: function (r) { return F.pct(r.util); } }],
    open: openFac });
  function openFac(id) {
    var f = facs().filter(function (x) { return x.id === id; })[0] || D.FACILITIES.filter(function (x) { return x.id === id; })[0]; if (!f) { return; }
    A.openDrawer({ id: id, title: f.name, body: H.summary([{ k: 'Borrower', v: D.ENT[f.entity].name }, { k: 'Type', v: f.type + (f.committed ? ', committed' : ', uncommitted') }, { k: 'Limit', v: F.moneyM(f.limit, f.ccy) },
      { k: 'Drawn', v: F.moneyM(f.drawn, f.ccy) }, { k: 'Undrawn', v: F.moneyM(f.limit - f.drawn, f.ccy) }, { k: 'Pricing', v: f.margin }, { k: 'Final maturity', v: F.date(f.maturity) }]) +
      H.limit({ id: f.id, label: 'Headroom on this facility', used: D.toGBP(f.drawn, f.ccy), limit: D.toGBP(f.limit, f.ccy) }),
      actions: [{ id: 'draw', label: 'Request a drawdown', kind: 'primary' }, { id: 'close', label: 'Close' }],
      onAction: function (a) { if (a === 'close') { A.closeDrawer(); } else { A.closeDrawer(); drawdown(f.id); } } });
  }
  function drawdown(fid) {
    var list = D.FACILITIES.filter(function (f) { return A.inScope(f.entity) && f.limit > f.drawn; });
    if (!list.length) { A.toast('No facility in this scope has undrawn headroom.', 'warn'); return; }
    var sel = fid || list[0].id;
    A.openForm({ title: 'Request a drawdown', body:
      '<p class="t-ed-body">A drawdown request goes to HSBC as a service request. Nothing moves until HSBC confirms it.</p>' +
      H.radios({ name: 'dd-fac', legend: 'Facility', value: sel, options: list.map(function (f) { return { v: f.id, label: f.name + ' — ' + F.moneyM(f.limit - f.drawn, f.ccy) + ' undrawn' }; }) }) +
      H.field({ id: 'dd-amt', label: 'Amount', prefix: 'Local currency', help: 'In the facility currency, up to the undrawn amount.', inputmode: 'decimal' }) +
      H.field({ id: 'dd-date', label: 'Value date', help: 'A business day on or after ' + F.date('2026-09-28') + ', written as YYYY-MM-DD.', value: '2026-09-30' }) +
      H.textarea({ id: 'dd-note', label: 'Purpose', help: 'Required. Say what the funds are for.', max: 300, rows: 3 }),
      actions: [{ id: 'send', label: 'Send request', kind: 'primary' }, { id: 'cancel', label: 'Cancel' }],
      onAction: function (a) {
        if (a === 'cancel') { return true; }
        var fsel = (document.querySelector('input[name="dd-fac"]:checked') || {}).value, f = D.FACILITIES.filter(function (x) { return x.id === fsel; })[0];
        var amt = parseFloat(String(A.val('dd-amt')).replace(/,/g, '')), date = A.val('dd-date'), note = A.val('dd-note'), ok = true;
        if (!f) { A.fail('dd-fac', 'Choose a facility.'); ok = false; }
        if (!(amt > 0)) { A.fail('dd-amt', 'Enter an amount greater than zero, in figures.'); ok = false; }
        else if (f && amt > f.limit - f.drawn) { A.fail('dd-amt', 'That is more than the ' + F.money(f.limit - f.drawn, f.ccy) + ' undrawn on this facility.'); ok = false; }
        var d = new Date(date + 'T12:00:00Z'), wd = d.getUTCDay();
        if (!/^\d{4}-\d{2}-\d{2}$/.test(date) || isNaN(d)) { A.fail('dd-date', 'Enter the date as YYYY-MM-DD.'); ok = false; }
        else if (date < '2026-09-28') { A.fail('dd-date', 'The earliest value date is 28 Sep 2026.'); ok = false; }
        else if (wd === 0 || wd === 6) { A.fail('dd-date', 'That is a weekend. Choose a business day.'); ok = false; }
        if (note.length < 10) { A.fail('dd-note', 'Give a purpose of at least 10 characters.'); ok = false; }
        if (!ok) { var first = document.querySelector('#drawer [aria-invalid="true"], #modal [aria-invalid="true"]'); if (first) { first.focus(); } return false; }
        var id = 'SR-' + String(30000 + A.W.sr.length + 1);
        A.W.sr.unshift({ id: id, type: 'Facility amendment', entity: f.entity, subject: 'Drawdown ' + F.money(amt, f.ccy) + ' on ' + f.name + ' for value ' + date, opened: D.AS_OF, updated: D.AS_OF, status: 'Submitted', sla: 2, priority: 'High',
          events: [{ date: D.AS_OF, title: 'Drawdown request submitted: ' + note, tone: 'inf' }] });
        A.W.audit.unshift({ at: new Date().toISOString(), what: 'Requested drawdown of ' + F.money(amt, f.ccy) + ' on ' + f.name }); A.saveWork();
        A.toast('Drawdown request ' + id + ' sent to HSBC. Track it in Messages and service requests.', 'ok');
        return true;
      } });
  }
  A.onClick = function (e) {
    if (e.target.closest('[data-action="drawdown"]')) { drawdown(); }
    if (e.target.closest('[data-action="export-fac"]')) { A.$('[data-export="g-fac"]').click(); }
  };
  function r1(v) { return Math.round(v / 1e5) / 10; }
  function render() {
    var liq = A.calc.liquiditySeries(), cash = A.calc.cashSeries(), und = A.calc.undrawnSeries(), head = A.calc.headroomSeries(), idx = A.dayIdx(), ds = A.days();
    A.renderKpis($('#kpis'), [{ id: 'liq', label: 'Available liquidity', series: liq, note: 'Cash plus undrawn committed facilities.' }, { id: 'cash', label: 'Cash', series: cash, note: 'Closing cash, GBP at illustrative rates.' },
      { id: 'undrawn', label: 'Undrawn committed facilities', series: und, note: 'Committed limits less drawn.' }, { id: 'head', label: 'Funding headroom', series: head, note: 'Available liquidity less the allocated £400m policy buffer and planned commitments.' }]);
    var cf = D.FACILITIES.filter(function (f) { return A.inScope(f.entity) && f.committed; });
    if (!cf.length && !A.scopedEntities().length) { ['ch-combo', 'ch-bullet', 'ch-sp1', 'ch-sp2', 'ch-sp3'].forEach(function (c) { A.emptyChart(c); }); }
    else {
      var util = idx.map(function (i) { var lim = cf.reduce(function (a, f) { return a + D.toGBP(f.limit, f.ccy); }, 0), dr = cf.reduce(function (a, f) { return a + D.toGBP(f.drawnSeries[i], f.ccy); }, 0); return lim ? Math.round(dr / lim * 1000) / 10 : 0; });
      A.drawChart('ch-combo', { type: 'combo', categories: ds.map(F.dshort), categoryLabel: 'Date', caption: 'Available liquidity, £ millions (columns), and committed facility utilisation, per cent (line)',
        series: [{ name: 'Available liquidity', kind: 'column', unit: '£m', values: liq.map(r1) }, { name: 'Utilisation', kind: 'line', unit: '%', values: util }], target: 75, targetLabel: 'Ceiling 75%' });
      var fl = facs().sort(function (a, b) { return b.util - a.util; });
      if (fl.length) {
        A.drawChart('ch-bullet', { type: 'bullet', categories: fl.map(function (f) { return f.name.replace(/ (facility|programme|line)$/, ''); }), unit: '%', categoryLabel: 'Facility', caption: 'Drawn as a share of limit by facility, per cent, against a 75% ceiling',
          series: [{ name: 'Drawn', values: fl.map(function (f) { return Math.round(f.util * 10) / 10; }) }, { name: 'Policy ceiling', values: fl.map(function () { return 75; }) }] });
      } else { A.emptyChart('ch-bullet'); }
      A.drawChart('ch-sp1', { type: 'spark', categories: ds.map(F.dshort), series: [{ name: 'Cash', values: cash.map(r1) }], unit: '£m', caption: 'Cash over the period' });
      A.drawChart('ch-sp2', { type: 'spark', categories: ds.map(F.dshort), series: [{ name: 'Undrawn', values: und.map(r1) }], unit: '£m', caption: 'Undrawn committed facilities over the period' });
      A.drawChart('ch-sp3', { type: 'spark', categories: ds.map(F.dshort), series: [{ name: 'Headroom', values: head.map(r1) }], unit: '£m', caption: 'Funding headroom over the period' });
    }
    var fl2 = facs().sort(function (a, b) { return b.util - a.util; }).slice(0, 2);
    $('#lim-list').innerHTML = fl2.length ? '<div class="ceo-stack">' + fl2.map(function (f) { return H.limit({ id: f.id, label: f.name, used: f.drawnG, limit: f.limitG }); }).join('') + '</div>' : '<p class="t-ed-body-small">No facilities in this scope.</p>';
    var cm = D.COMMITMENTS.filter(function (c) { return A.inScope(c.entity); });
    $('#commit-list').innerHTML = '<dl class="summary">' + cm.map(function (c) { return '<div class="summary__row"><dt class="summary__k t-cm-label">' + esc(c.name) + ' <span class="t-cm-legal">' + F.date(c.due) + '</span></dt><dd class="summary__v t-cm-figure-5">' + F.gbpM(D.toGBP(c.amount, c.ccy)) + '</dd></div>'; }).join('') +
      '<div class="summary__row summary__row--total"><dt class="summary__k t-cm-label">Policy buffer (allocated)</dt><dd class="summary__v t-cm-figure-5">' + F.gbpM(A.calc.buffer()) + '</dd></div></dl>';
    A.renderGrid('g-fac');
  }
  A.afterBoot = function () { if (A.PS.open) { openFac(A.PS.open); } };
  A.boot(render);
}());
