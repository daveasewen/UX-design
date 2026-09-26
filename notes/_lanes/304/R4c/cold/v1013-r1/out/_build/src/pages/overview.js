/* Overview — the three questions: resilience (KPI row), risk outlook (exposure chart with
   drill-through to positions and limits), decisions (approvals and exceptions, each a link to a
   record you can act on). Everything is derived from DATA under the shared filters. */
(function () {
  'use strict';
  var A = APP, D = A.D, F = A.F, esc = A.esc, $ = A.$;
  var GROUPS = [{ k: 'GBP', l: 'Sterling' }, { k: 'EUR', l: 'Euro' }, { k: 'USD', l: 'US dollar' }, { k: 'ASIA', l: 'Asian currencies' }, { k: 'OTHER', l: 'Dirham and peso' }];
  function grp(c) { return c === 'GBP' || c === 'EUR' || c === 'USD' ? c : c === 'SGD' || c === 'HKD' || c === 'CNY' ? 'ASIA' : 'OTHER'; }
  var view = A.PS.expView || 'region';

  A.mountChart($('#host-exposure'), { id: 'ch-exposure', note: 'As at 25 Sep 2026; the date range does not apply', type: 'stacked-column', title: 'Where we are exposed — net position by region and currency',
    caption: 'Net exposure by region, split by currency group, £ millions', legend: GROUPS.map(function (g) { return g.l; }),
    controls: '<div class="seg sm" role="group" aria-label="Group the exposure by"><span class="ind" aria-hidden="true"></span><button type="button" class="t-cm-chart-label" data-exp-view="region" aria-pressed="' + (view === 'region') + '">By region</button><button type="button" class="t-cm-chart-label" data-exp-view="ccy" aria-pressed="' + (view === 'ccy') + '">By currency</button></div>',
    after: '<p class="t-cm-caption ceo-drill" id="drill"></p>' });
  A.mountChart($('#host-liquidity'), { id: 'ch-liquidity', type: 'multiline', title: 'Liquidity stayed well above the policy buffer',
    caption: 'Cash, available liquidity and funding headroom by day, £ millions', legend: ['Cash', 'Available liquidity', 'Funding headroom'] });
  A.mountChart($('#host-ccy'), { id: 'ch-ccy', note: 'As at 25 Sep 2026', type: 'donut', title: 'Cash by currency', caption: 'Cash by currency, £ millions equivalent', legend: ['Sterling', 'Euro', 'US dollar', 'Hong Kong dollar', 'Renminbi', 'Other'] });
  A.mountChart($('#host-facilities'), { id: 'ch-fac', note: 'As at 25 Sep 2026', type: 'bullet', title: 'Facility utilisation against the 75% policy ceiling', caption: 'Drawn as a share of limit, per cent, against a 75% ceiling', max: 100 });

  function exposure() {
    var byR = A.calc.exposureByRegionCcy(), regions = D.REGIONS.filter(function (r) { return byR[r.id]; });
    if (!regions.length) { A.emptyChart('ch-exposure'); $('#drill').innerHTML = ''; return; }
    var spec;
    if (view === 'region') {
      spec = { type: 'stacked-column', categories: regions.map(function (r) { return r.name; }), categoryLabel: 'Region', unit: '£m',
        caption: 'Net exposure by region, split by currency group, £ millions',
        series: GROUPS.map(function (g) { return { name: g.l, values: regions.map(function (r) { var t = 0; Object.keys(byR[r.id]).forEach(function (c) { if (grp(c) === g.k) { t += byR[r.id][c]; } }); return Math.max(0, Math.round(t / 1e5) / 10); }) }; }) };
    } else {
      var ccys = D.CCYS.filter(function (c) { return regions.some(function (r) { return byR[r.id][c]; }); });
      spec = { type: 'stacked-column', categories: ccys, categoryLabel: 'Currency', unit: '£m', caption: 'Net exposure by currency, split by region, £ millions',
        series: D.REGIONS.map(function (r) { return { name: r.name, values: ccys.map(function (c) { return Math.max(0, Math.round(((byR[r.id] || {})[c] || 0) / 1e5) / 10); }) }; }) };
    }
    /* the legend names the series of the view on screen */
    var names = spec.series.map(function (s) { return s.name; });
    A.$$('#ch-exposure .dv-legrow .dv-leg-name').forEach(function (n, i) { n.textContent = names[i] || ''; });
    A.$$('#ch-exposure .dv-legrow').forEach(function (r, i) { r.querySelector('.dv-leg-sw').setAttribute('aria-label', 'Show or hide ' + names[i]); r.querySelector('.dv-leg-item').setAttribute('aria-label', 'Isolate ' + names[i]); });
    A.drawChart('ch-exposure', spec);
    A.$$('#ch-exposure svg .dv-series').forEach(function (m) { m.setAttribute('data-drill', '1'); });
    $('#drill').innerHTML = 'Drill through to positions and limits: ' + regions.map(function (r) {
      return '<a class="tpl-link" data-app-href="risk.html?region=' + r.id + '#positions" href="risk.html">' + esc(r.name) + '</a>';
    }).join(' · ') + '. Select a column to open that region.';
    A.decorateLinks();
  }
  function drillFromMark(m) {
    var label = (m.getAttribute('data-tip') || m.getAttribute('aria-label') || '');
    var r = D.REGIONS.filter(function (x) { return label.indexOf(x.name) > -1; })[0];
    if (view === 'ccy' && !r) { var c = D.CCYS.filter(function (x) { return label.indexOf(x) > -1; })[0]; if (c) { location.href = 'risk.html?' + shared() + '&p.g-pos.q=' + c + '#positions'; } return; }
    if (r) { location.href = 'risk.html?region=' + r.id + (A.S.days !== 30 ? '&days=' + A.S.days : '') + '#positions'; }
  }
  function shared() { return (A.S.entity !== 'all' ? 'entity=' + A.S.entity + '&' : '') + (A.S.region !== 'all' ? 'region=' + A.S.region + '&' : '') + 'days=' + A.S.days; }
  A.onClick = function (e) {
    var b = e.target.closest('[data-exp-view]'); if (b) { view = b.getAttribute('data-exp-view'); A.PS.expView = view; A.persist(); exposure(); return; }
    var m = e.target.closest('#ch-exposure svg .dv-series'); if (m) { drillFromMark(m); return; }
    if (e.target.closest('[data-action="export-overview"]')) {
      var k = kpiList(), rows = [['Measure', 'Value (GBP m)', 'Scope']];
      k.forEach(function (x) { rows.push([x.label, F.m(x.series[x.series.length - 1]).replace(/,/g, ''), A.scopeLabel()]); });
      var byR = A.calc.exposureByRegionCcy();
      Object.keys(byR).forEach(function (r) { Object.keys(byR[r]).forEach(function (c) { rows.push(['Net exposure ' + A.regionName(r) + ' ' + c, F.m(byR[r][c]).replace(/,/g, ''), A.scopeLabel()]); }); });
      A.csv('group-overview.csv', rows);
    }
  };
  A.onKey = function (e) { var m = e.target.closest && e.target.closest('#ch-exposure svg .dv-series'); if (m && e.key === 'Enter') { drillFromMark(m); } };

  function kpiList() {
    var cash = A.calc.cashSeries(), liq = A.calc.liquiditySeries(), head = A.calc.headroomSeries(), und = A.calc.undrawnSeries();
    return [
      { id: 'cash', label: 'Cash', series: cash, note: 'Closing cash across HSBC accounts of the entities in scope, converted to GBP at the illustrative rates.' },
      { id: 'liq', label: 'Available liquidity', series: liq, note: 'Cash plus undrawn committed facilities.' },
      { id: 'head', label: 'Funding headroom', series: head, note: 'Available liquidity less the policy buffer (£400m, allocated by share of cash) and planned commitments.' },
      { id: 'undrawn', label: 'Undrawn committed facilities', series: und, note: 'Committed facility limits less drawn amounts.' }
    ];
  }
  function render() {
    var ents = A.scopedEntities();
    A.renderKpis($('#kpis'), kpiList());
    exposure();
    var ds = A.days(), cash = A.calc.cashSeries(), liq = A.calc.liquiditySeries(), head = A.calc.headroomSeries();
    if (!ents.length) { A.emptyChart('ch-liquidity'); } else {
      A.drawChart('ch-liquidity', { type: 'multiline', categories: ds.map(F.dshort), categoryLabel: 'Date', unit: '£m', caption: 'Cash, available liquidity and funding headroom by day, £ millions',
        series: [{ name: 'Cash', values: cash.map(function (v) { return Math.round(v / 1e5) / 10; }) }, { name: 'Available liquidity', values: liq.map(function (v) { return Math.round(v / 1e5) / 10; }) },
          { name: 'Funding headroom', values: head.map(function (v) { return Math.round(v / 1e5) / 10; }) }] });
    }
    /* cash by currency */
    var by = { GBP: 0, EUR: 0, USD: 0, HKD: 0, CNY: 0, Other: 0 };
    D.ACCOUNTS.forEach(function (ac) { if (A.inScope(ac.entity)) { var k = by[ac.ccy] != null ? ac.ccy : 'Other'; by[k] += D.toGBP(ac.balances[29], ac.ccy); } });
    var cats = ['Sterling', 'Euro', 'US dollar', 'Hong Kong dollar', 'Renminbi', 'Other'], vals = ['GBP', 'EUR', 'USD', 'HKD', 'CNY', 'Other'].map(function (k) { return Math.round(by[k] / 1e5) / 10; });
    if (!ents.length) { A.emptyChart('ch-ccy'); } else { A.drawChart('ch-ccy', { type: 'donut', categories: cats, series: [{ name: 'Cash', values: vals }], unit: '£m', categoryLabel: 'Currency', caption: 'Cash by currency, £ millions equivalent' }); }
    /* facility utilisation */
    var fac = D.FACILITIES.filter(function (f) { return A.inScope(f.entity); }).sort(function (a, b) { return b.drawn / b.limit - a.drawn / a.limit; }).slice(0, 6);
    if (!fac.length) { A.emptyChart('ch-fac'); } else {
      A.drawChart('ch-fac', { type: 'bullet', categories: fac.map(function (f) { return f.name.replace(/ (facility|programme|line)$/, ''); }), unit: '%', categoryLabel: 'Facility', caption: 'Drawn as a share of limit, per cent, against a 75% ceiling',
        series: [{ name: 'Drawn', values: fac.map(function (f) { return Math.round(f.drawn / f.limit * 1000) / 10; }) }, { name: 'Policy ceiling', values: fac.map(function () { return 75; }) }] });
    }
    /* decisions */
    var pays = A.calc.payments().filter(function (p) { return p.status === 'Awaiting your approval' && A.inScope(p.entity); }).sort(function (a, b) { return b.gbp - a.gbp; });
    var total = pays.reduce(function (a, p) { return a + p.gbp; }, 0);
    $('#na-approvals').innerHTML = '<dl class="summary tpl-na-head"><div class="summary__row"><dt class="summary__k t-cm-label">Awaiting your approval <span class="t-cm-legal">' + pays.length + ' payment' + (pays.length === 1 ? '' : 's') + ' · ' + pays.filter(function (p) { return p.approvals === 2; }).length + ' under dual control</span></dt><dd class="summary__v t-cm-figure-5">' + F.gbpM(total) + '</dd></div></dl>' +
      (pays.length ? '<div class="l-stack" data-gap="m">' + pays.slice(0, 4).map(function (p) {
        return '<div class="l-row" data-gap="s" data-justify="between"><a class="tpl-link t-cm-label" data-app-href="payments.html?p.open=' + p.id + '" href="payments.html">' + esc(p.beneficiary) + ' · ' + F.moneyM(p.amount, p.ccy) + '</a>' +
          '<span class="status ' + (p.flags.length ? 'warn' : 'inf') + '" data-carries="label"><span class="dot" aria-hidden="true"></span><span class="t-cm-legal">' + (p.flags.length ? esc(p.flags[0].replace(' dual-control threshold', '')) : 'Due ' + F.dshort(p.valueDate)) + '</span></span></div>';
      }).join('') + '</div>' : '<p class="t-ed-body-small">Nothing is waiting for you in this scope.</p>');
    var exc = A.calc.exceptions().filter(function (x) { return x.severity === 'Material' && x.status === 'Open' && A.inScope(x.entity); });
    $('#na-exceptions').innerHTML = '<dl class="summary tpl-na-head"><div class="summary__row"><dt class="summary__k t-cm-label">Material and unacknowledged <span class="t-cm-legal">' + exc.length + ' exception' + (exc.length === 1 ? '' : 's') + ' · ' + A.calc.exceptions().filter(function (x) { return x.status === 'Open' && A.inScope(x.entity); }).length + ' open in total</span></dt><dd class="summary__v t-cm-figure-5">' + exc.length + '</dd></div></dl>' +
      (exc.length ? '<div class="l-stack" data-gap="m">' + exc.map(function (x) {
        return '<div class="l-row" data-gap="s" data-justify="between"><a class="tpl-link t-cm-label" data-app-href="risk.html?p.open=' + x.id + '" href="risk.html">' + esc(x.title) + '</a><span class="status err" data-carries="label"><span class="dot" aria-hidden="true"></span><span class="t-cm-legal">' + esc(x.type.replace(/ near breach| breach/, '')) + '</span></span></div>';
      }).join('') + '</div>' : '<p class="t-ed-body-small">No material exceptions are open in this scope.</p>');
    /* status strip */
    $('#strip').innerHTML = '<div class="l-row" data-gap="m"><span class="status ok" data-carries="label"><span class="dot" aria-hidden="true"></span><span class="t-cm-legal">Figures as at ' + F.date(D.AS_OF) + ', ' + D.AS_OF_TIME + '</span></span>' +
      '<a class="status warn tpl-strip-link" href="#dp08-na" data-carries="label"><span class="dot" aria-hidden="true"></span><span class="t-cm-legal">Awaiting approval · ' + pays.length + ' payments · ' + F.gbpM(total) + '</span></a>' +
      '<span class="tpl-strip-plain t-cm-legal">Illustrative data and FX · no live banking connection</span></div>';
    A.decorateLinks();
  }
  A.boot(render);
}());
