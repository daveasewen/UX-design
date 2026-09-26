/* FX and markets — illustrative rates only. Candlestick per pair (switchable), receivables against
   payables per currency (butterfly), relative moves indexed to 100, hedges grid, and a validated
   hedge-quote request. No live market data. */
(function () {
  'use strict';
  var A = APP, D = A.D, F = A.F, H = A.H, esc = A.esc, $ = A.$;
  var PAIRS = ['USD', 'EUR', 'HKD', 'SGD'], pair = PAIRS.indexOf(A.PS.pair) > -1 ? A.PS.pair : 'USD';
  A.mountChart($('#host-candle'), { id: 'ch-candle', note: 'Market rates: entity and region do not apply', type: 'candlestick', title: 'Sterling against the ' + pair + ', thirty days', caption: 'GBP/' + pair + ' open, high, low and close by session, illustrative',
    controls: '<div class="seg sm" role="group" aria-label="Currency pair"><span class="ind" aria-hidden="true"></span>' + PAIRS.map(function (c) { return '<button type="button" class="t-cm-chart-label" data-pair="' + c + '" aria-pressed="' + (c === pair) + '">GBP/' + c + '</button>'; }).join('') + '</div>' });
  A.mountChart($('#host-bfly'), { id: 'ch-bfly', note: 'As at 25 Sep 2026', type: 'butterfly-h', title: 'Receivables against payables by currency', caption: 'Foreign-currency receivables and payables, £ millions equivalent', legend: ['Receivables', 'Payables'] });
  A.mountChart($('#host-index'), { id: 'ch-index', note: 'Market rates: entity and region do not apply', type: 'multiline', title: 'Sterling firmed against the dollar and the peso', caption: 'Units of currency per pound, indexed to 100 at the start of the period', legend: ['US dollar', 'Euro', 'Mexican peso', 'Renminbi'] });
  function hedges() { return D.HEDGES.filter(function (h) { return A.inScope(h.entity); }); }
  A.grid($('#host-ghedge'), { id: 'g-hedge', title: 'Forward contracts', placeholder: 'Search currency, entity, direction or bank', size: 10, sort: 'maturity', dir: 'ascending',
    tools: '<button type="button" class="clearbtn t-cm-button" data-export="g-hedge" data-file="hedges.csv">Export CSV</button>',
    rows: hedges, text: function (r) { return [r.id, r.ccy, r.direction, D.ENT[r.entity].name, r.counterparty].join(' '); }, rowLabel: function (r) { return 'Open forward ' + r.id; },
    cols: [{ k: 'id', label: 'Contract' }, { k: 'direction', label: 'Direction' }, { k: 'entity', label: 'Entity', fmt: function (r) { return D.ENT[r.entity].short; } },
      { k: 'maturity', label: 'Maturity', fmt: function (r) { return F.date(r.maturity); }, csv: function (r) { return r.maturity; } }, { k: 'rate', label: 'Contract rate', num: true, fmt: function (r) { return r.rate.toFixed(4); } },
      { k: 'notional', label: 'Notional', num: true, fmt: function (r) { return F.moneyM(r.notional, r.ccy); } }, { k: 'mtm', label: 'Revaluation', num: true, html: function (r) { return '<span class="t-cm-figure-5">' + F.gbpM(r.mtm) + '</span>'; }, csv: function (r) { return r.mtm; } }],
    open: function (id) {
      var h = D.HEDGES.filter(function (x) { return x.id === id; })[0]; if (!h) { return; }
      A.openDrawer({ id: id, title: 'Forward ' + h.id, body: H.summary([{ k: 'Direction', v: h.direction }, { k: 'Notional', v: F.money(h.notional, h.ccy) }, { k: 'GBP equivalent', v: F.money(h.gbp, 'GBP') }, { k: 'Contract rate', v: h.rate.toFixed(4) + ' ' + h.ccy + ' per GBP' },
        { k: 'Illustrative rate today', v: D.FX[h.ccy].toFixed(4) }, { k: 'Revaluation', v: F.gbpM(h.mtm) }, { k: 'Maturity', v: F.date(h.maturity) }, { k: 'Bank', v: h.counterparty }, { k: 'Entity', v: D.ENT[h.entity].name }]),
        actions: [{ id: 'roll', label: 'Request a roll quote', kind: 'primary' }, { id: 'close', label: 'Close' }],
        onAction: function (a) { A.closeDrawer(); if (a === 'roll') { quote(h.ccy, h.direction.indexOf('Sell') === 0 ? 'sell' : 'buy', h.notional); } } });
    } });
  function quote(ccy, dir, amt) {
    A.openForm({ title: 'Request an indicative hedge quote', body: '<p class="t-ed-body">HSBC markets will reply with an indicative quote in Messages. Nothing is traded until you accept a firm price with the dealing desk.</p>' +
      H.radios({ name: 'q-dir', legend: 'Direction', value: dir || 'sell', options: [{ v: 'sell', label: 'Sell foreign currency, buy sterling' }, { v: 'buy', label: 'Buy foreign currency, sell sterling' }] }) +
      H.field({ id: 'q-ccy', label: 'Currency', help: 'Three-letter code: USD, EUR, SGD, HKD, AED, MXN or CNY.', value: ccy || '' }) +
      H.field({ id: 'q-amt', label: 'Notional in that currency', inputmode: 'decimal', value: amt ? String(amt) : '' }) +
      H.radios({ name: 'q-ten', legend: 'Tenor', value: '3M', options: [{ v: '1M', label: 'One month' }, { v: '3M', label: 'Three months' }, { v: '6M', label: 'Six months' }, { v: '12M', label: 'Twelve months' }] }),
      actions: [{ id: 'go', label: 'Request quote', kind: 'primary' }, { id: 'cancel', label: 'Cancel' }],
      onAction: function (a) {
        if (a === 'cancel') { return true; }
        var c = A.val('q-ccy').toUpperCase(), n = parseFloat(A.val('q-amt').replace(/,/g, '')), ok = true;
        if (!D.FX[c] || c === 'GBP') { A.fail('q-ccy', 'Enter one of USD, EUR, SGD, HKD, AED, MXN or CNY.'); ok = false; }
        if (!(n > 0)) { A.fail('q-amt', 'Enter a notional greater than zero.'); ok = false; }
        else if (D.FX[c] && n / D.FX[c] > 250e6) { A.fail('q-amt', 'Above £250m equivalent the dealing desk must quote by phone.'); ok = false; }
        if (!ok) { var f = document.querySelector('#drawer [aria-invalid="true"], #modal [aria-invalid="true"]'); if (f) { f.focus(); } return false; }
        var d = (document.querySelector('input[name="q-dir"]:checked') || {}).value, t = (document.querySelector('input[name="q-ten"]:checked') || {}).value;
        var id = 'SR-' + String(30000 + A.W.sr.length + 1);
        A.W.sr.unshift({ id: id, type: 'Hedge quote', entity: A.S.entity !== 'all' ? A.S.entity : 'HLH', subject: (d === 'sell' ? 'Sell ' : 'Buy ') + F.money(n, c) + ' ' + t + ' forward', opened: D.AS_OF, updated: D.AS_OF, status: 'Submitted', sla: 1, priority: 'High', events: [{ date: D.AS_OF, title: 'Indicative quote requested', tone: 'inf' }] });
        A.W.audit.unshift({ at: new Date().toISOString(), what: 'Requested a ' + t + ' ' + c + ' forward quote' }); A.saveWork();
        A.toast('Quote request ' + id + ' sent. HSBC markets will reply in Messages.', 'ok'); return true;
      } });
  }
  A.onClick = function (e) {
    var pb = e.target.closest('[data-pair]');
    if (pb) { pair = pb.getAttribute('data-pair'); A.PS.pair = pair; A.persist(); var fig = $('#ch-candle'); fig.querySelector('.dv-title').textContent = 'Sterling against the ' + pair + ', thirty days'; fig.setAttribute('data-lockup-title', 'Sterling against the ' + pair + ', thirty days'); candle(); return; }
    if (e.target.closest('[data-action="quote"]')) { quote(); }
    if (e.target.closest('[data-action="export-hedge"]')) { A.$('[data-export="g-hedge"]').click(); }
  };
  function candle() {
    var rows = D.FX_SERIES[pair].filter(function (r) { return A.inWindow(r.date); });
    A.drawChart('ch-candle', { type: 'candlestick', categories: rows.map(function (r) { return F.dshort(r.date); }), categoryLabel: 'Session', caption: 'GBP/' + pair + ' open, high, low and close by session, illustrative',
      series: ['open', 'high', 'low', 'close'].map(function (k) { return { name: k[0].toUpperCase() + k.slice(1), values: rows.map(function (r) { return r[k]; }) }; }) });
  }
  function exposure(c) { /* receivables and payables for currency c, £ */
    var rec = 0, pay = 0;
    D.POSITIONS.forEach(function (p) { if (p.ccy === c && A.inScope(p.entity) && D.ENT[p.entity].ccy !== c) { if (p.type === 'Receivables') { rec += p.gbp; } if (p.type === 'Payables') { pay -= p.gbp; } } });
    D.POSITIONS.forEach(function (p) { if (p.ccy === c && A.inScope(p.entity) && D.ENT[p.entity].ccy === c && c !== 'GBP') { if (p.type === 'Receivables') { rec += p.gbp; } if (p.type === 'Payables') { pay -= p.gbp; } } });
    return { rec: rec, pay: pay };
  }
  function render() {
    var idx = A.dayIdx(), ccys = D.CCYS.filter(function (c) { return c !== 'GBP'; });
    var nonGbp = D.POSITIONS.filter(function (p) { return p.ccy !== 'GBP' && A.inScope(p.entity); });
    var hs = hedges();
    /* exposure revalued at each day's close (the FX series), so the KPIs move with the rates */
    function reval(filterFn, sign) {
      return idx.map(function (i) { var d = D.DAYS[i]; return nonGbp.filter(filterFn).reduce(function (a, p) { var ser = D.FX_SERIES[p.ccy], row = ser.filter(function (r) { return r.date <= d; }).pop() || ser[0]; return a + (sign ? Math.abs(p.local / row.close) : p.local / row.close); }, 0); });
    }
    A.renderKpis($('#kpis'), [
      { id: 'net', label: 'Net open exposure', series: reval(function () { return true; }).map(Math.abs), note: 'Net of all foreign-currency positions, revalued daily at illustrative rates.' },
      { id: 'hedge', label: 'Hedged notional', series: idx.map(function () { return hs.reduce(function (a, h) { return a + h.gbp; }, 0); }), note: 'Outstanding forwards, GBP equivalent at contract.' },
      { id: 'mtm', label: 'Forward revaluation', series: idx.map(function (i, k) { return hs.reduce(function (a, h) { return a + h.mtm; }, 0) * (0.6 + 0.4 * k / Math.max(1, idx.length - 1)); }), note: 'Illustrative revaluation of forwards against today’s rates.' },
      { id: 'rec', label: 'Foreign-currency receivables', series: reval(function (p) { return p.type === 'Receivables'; }, true), note: 'Receivables not in sterling, revalued daily.' }]);
    if (!A.scopedEntities().length) { ['ch-candle', 'ch-bfly', 'ch-index'].forEach(function (c) { A.emptyChart(c); }); }
    else {
      candle();
      var ex = ccys.map(function (c) { var e = exposure(c); return { c: c, rec: Math.round(e.rec / 1e5) / 10, pay: Math.round(e.pay / 1e5) / 10 }; }).filter(function (x) { return x.rec > 0 || x.pay > 0; });
      if (ex.length) { A.drawChart('ch-bfly', { type: 'butterfly-h', categories: ex.map(function (x) { return x.c; }), categoryLabel: 'Currency', unit: '£m', caption: 'Foreign-currency receivables and payables, £ millions equivalent',
        series: [{ name: 'Receivables', values: ex.map(function (x) { return Math.max(0, x.rec); }) }, { name: 'Payables', values: ex.map(function (x) { return Math.max(0, x.pay); }) }] }); } else { A.emptyChart('ch-bfly'); }
      var sess = D.SESSIONS.filter(A.inWindow);
      A.drawChart('ch-index', { type: 'multiline', categories: sess.map(F.dshort), categoryLabel: 'Session', caption: 'Units of currency per pound, indexed to 100 at the start of the period',
        series: ['USD', 'EUR', 'MXN', 'CNY'].map(function (c, k) { var rows = D.FX_SERIES[c].filter(function (r) { return A.inWindow(r.date); }), b = rows[0].close; return { name: ['US dollar', 'Euro', 'Mexican peso', 'Renminbi'][k], values: rows.map(function (r) { return Math.round(r.close / b * 10000) / 100; }) }; }) });
    }
    $('#rates').innerHTML = '<dl class="summary">' + ccys.map(function (c) { var s = D.FX_SERIES[c].filter(function (r) { return A.inWindow(r.date); }), ch = (s[s.length - 1].close - s[0].close) / s[0].close * 100;
      return '<div class="summary__row"><dt class="summary__k t-cm-label">GBP/' + c + ' <span class="t-cm-legal">' + F.signedPct(ch) + ' in period</span></dt><dd class="summary__v t-cm-figure-5">' + D.FX[c].toFixed(4) + '</dd></div>'; }).join('') + '</dl>';
    $('#rate-note').innerHTML = H.alert('info', 'Illustrative rates.', 'Fixed at ' + F.date(D.AS_OF) + ' ' + D.AS_OF_TIME + ' for this prototype. They are not market data and cannot be dealt on.') +
      '<p class="t-ed-body-small">Every sterling figure in this view converts at these rates. Hedge quotes come back from HSBC markets as messages.</p>';
    A.renderGrid('g-hedge');
  }
  A.afterBoot = function () { if (A.PS.open) { A.GRIDS['g-hedge'].open(A.PS.open); } };
  A.boot(render);
}());
