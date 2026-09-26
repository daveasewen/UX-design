/* ================= WIRE — state, filters, charts (dvRender from DATA), grids, workflows, persistence.
   Authored for this page (s258-D1). Wiring is delegated from the document (rule 14). ================= */
(function () {
  'use strict';
  var STORE_KEY = 'ceo.proto.v1';
  function load() { try { return JSON.parse(localStorage.getItem(STORE_KEY) || '{}'); } catch (e) { return {}; } }
  function save() { try { localStorage.setItem(STORE_KEY, JSON.stringify(SAVED)); } catch (e) { /* storage unavailable: state lives for this visit only */ } }
  var SAVED = load();
  SAVED.grids = SAVED.grids || {}; SAVED.work = SAVED.work || {}; SAVED.settings = SAVED.settings || {};

  /* ---------- re-apply saved workflow outcomes onto DATA (decisions, acknowledgements, requests, deals) ---------- */
  function byId(list, id) { for (var i = 0; i < list.length; i++) { if (list[i].id === id) { return list[i]; } } return null; }
  var W = SAVED.work;
  (W.payments || []).forEach(function (p) { var x = byId(DATA.PAYMENTS, p.id); if (x) { x.status = p.status; x.approvals = p.approvals; x.audit = p.audit; } });
  (W.exceptions || []).forEach(function (p) { var x = byId(DATA.EXCEPTIONS, p.id); if (x) { x.status = p.status; x.audit = p.audit; } });
  (W.requests || []).forEach(function (r) { var x = byId(DATA.REQUESTS, r.id); if (x) { x.status = r.status; x.history = r.history; } else { DATA.REQUESTS.unshift(r); } });
  (W.deals || []).forEach(function (d) { if (!byId(DATA.DEALS, d.id)) { DATA.DEALS.unshift(d); } });
  (W.drawdowns || []).forEach(function (d) { var f = byId(DATA.FACILITIES, d.facility); if (f && !f.requests.some(function (r) { return r.id === d.id; })) { f.requests.push(d); } });
  (W.reads || []).forEach(function (id) { var m = byId(DATA.MESSAGES, id); if (m) { m.unread = false; } });
  (W.unreads || []).forEach(function (id) { var m = byId(DATA.MESSAGES, id); if (m) { m.unread = true; } });
  (W.replies || []).forEach(function (r) { var m = byId(DATA.MESSAGES, r.id); if (m) { m.replies = r.replies; } });
  (W.runs || []).forEach(function (r) { var x = byId(DATA.REPORTS, r.id); if (x) { x.lastRun = r.lastRun; } });
  function remember(kind, obj, key) {
    W[kind] = (W[kind] || []).filter(function (x) { return (key ? x[key] : x.id) !== (key ? obj[key] : obj.id); });
    W[kind].push(obj); save();
  }

  /* ---------- STATE: view + filters in the URL (shareable), everything else in storage ---------- */
  var S = { view: 'overview', record: null, entity: 'all', region: 'all', days: 30, pair: 'GBP/USD' };
  function readUrl() {
    var h = (location.hash || '').replace(/^#\/?/, '').split('/');
    S.view = VIEWS.some(function (v) { return v.id === h[0]; }) ? h[0] : (SAVED.settings.start || 'overview');
    S.record = h[1] ? decodeURIComponent(h[1]) : null;
    var q = new URLSearchParams(location.search);
    S.entity = q.get('entity') || SAVED.entity || 'all';
    S.region = q.get('region') || SAVED.region || 'all';
    S.days = +(q.get('days') || SAVED.days || 30);
    S.pair = q.get('pair') || SAVED.pair || 'GBP/USD';
    if ([7, 14, 30].indexOf(S.days) < 0) { S.days = 30; }
  }
  function writeUrl(push) {
    var q = new URLSearchParams(location.search);
    [['entity', 'all'], ['region', 'all'], ['days', 30], ['pair', 'GBP/USD']].forEach(function (p) { if (String(S[p[0]]) === String(p[1])) { q.delete(p[0]); } else { q.set(p[0], S[p[0]]); } });
    q.set('theme', document.documentElement.getAttribute('data-theme'));
    var url = location.pathname + '?' + q.toString() + '#/' + S.view + (S.record ? '/' + encodeURIComponent(S.record) : '');
    history[push ? 'pushState' : 'replaceState'](null, '', url);
    SAVED.entity = S.entity; SAVED.region = S.region; SAVED.days = S.days; SAVED.pair = S.pair; save();
  }

  /* ---------- scope ---------- */
  function scopeEnts() { return DATA.ENTITIES.filter(function (e) { return (S.entity === 'all' || e.id === S.entity) && (S.region === 'all' || e.region === S.region); }); }
  function inScope(id) { return scopeEnts().some(function (e) { return e.id === id; }); }
  function entOf(id) { return byId(DATA.ENTITIES, id); }
  function periodDays() { return DATA.DAYS.slice(30 - S.days); }
  function m(v) { return Math.round(v / 1e5) / 10; }   /* pounds -> £m, 1dp */
  function sum(a) { return a.reduce(function (s, v) { return s + v; }, 0); }

  function cashSeries() {
    var acc = DATA.ACCOUNTS.filter(function (a) { return inScope(a.entity); });
    return DATA.DAYS.map(function (d, i) { return sum(acc.map(function (a) { return a.series[i]; })); }).slice(30 - S.days);
  }
  function undrawnCommitted() { return sum(DATA.FACILITIES.filter(function (f) { return f.kind === 'Committed' && inScope(f.entity); }).map(function (f) { return f.limitGbp - f.drawnGbp; })); }
  function scheduledOut() { return sum(DATA.PAYMENTS.filter(function (p) { return inScope(p.entity) && (p.status === 'Awaiting approval' || p.status === 'Approved'); }).map(function (p) { return p.gbp; })); }

  /* ---------- helpers for markup cloned from templates ---------- */
  function chip(kind, label) {
    var c = document.getElementById('t-chip').content.firstElementChild.cloneNode(true);
    c.className = 'chip ' + kind; c.lastChild.textContent = label; return '<span class="cn-status-indicator">' + c.outerHTML + '</span>';
  }
  var STATUS_KIND = { 'Awaiting approval': 'warn', 'Approved': 'inf', 'Released': 'ok', 'Rejected': 'err', 'Settled': 'ok', 'Pending': 'warn',
    'Open': 'err', 'Acknowledged': 'ok', 'High': 'err', 'Medium': 'warn', 'Low': 'inf', 'Issued': 'ok', 'Awaiting documents': 'warn',
    'Documents discrepant': 'err', 'Amendment requested': 'inf', 'Paid': 'ok', 'In progress': 'inf', 'Awaiting your input': 'warn', 'Completed': 'ok', 'Submitted': 'inf', 'Requested': 'inf' };
  function status(label) { return chip(STATUS_KIND[label] || 'inf', label); }
  function recLink(view, id, label) { return '<a class="lnk t-cm-label" href="#/' + view + '/' + encodeURIComponent(id) + '" data-record="' + esc(id) + '">' + esc(label || id) + '</a>'; }
  function signed(v, fmt) { return '<span class="t-cm-figure-5">' + (fmt || gbp)(v) + '</span>'; }

  /* ================= CHARTS ================= */
  function legend(fig, names) {
    var ul = fig.querySelector('.dv-leg'); if (!ul) { return; }
    var rows = ul.querySelectorAll('.dv-legrow'), tpl = rows[0];
    rows.forEach(function (r, i) { if (i) { r.remove(); } });
    var reset = ul.querySelector('.dv-leg-reset-wrap');
    names.forEach(function (n, i) {
      var r = i ? tpl.cloneNode(true) : tpl;
      r.setAttribute('data-series', String(i + 1));
      var sw = r.querySelector('.dv-leg-sw'); sw.setAttribute('aria-label', 'Show or hide ' + n); sw.style.setProperty('--sc', 'var(--data-series-' + (i % 5 + 1) + ')');
      var b = r.querySelector('.dv-leg-item'); b.setAttribute('data-series', String(i + 1)); b.setAttribute('aria-label', 'Isolate ' + n);
      var k = r.querySelector('.dv-key'); if (k) { k.textContent = String.fromCharCode(65 + i); }
      var nm = r.querySelector('.dv-leg-name'); if (nm) { nm.textContent = n; }
      ul.insertBefore(r, reset);
    });
  }
  function draw(key, spec, names) {
    var fig = FIGURES[key]; if (!fig) { return; }
    if (names) { legend(fig, names); }
    try { window.dvRender(fig, spec); fig.removeAttribute('data-empty'); }
    catch (e) { fig.setAttribute('data-empty', 'true'); console.warn('chart not drawn:', key, e.message); }
  }
  var CAT_REGION = DATA.REGIONS.map(function (r) { return r.name; });
  function exposureBy(field, keys) {
    var pos = DATA.POSITIONS.filter(function (p) { return inScope(p.entity); });
    return keys.map(function (k) { return m(sum(pos.filter(function (p) { return p[field] === k; }).map(function (p) { return p.exposure; }))); });
  }
  function ccyShares() {
    var pos = DATA.POSITIONS.filter(function (p) { return inScope(p.entity); }), t = {};
    pos.forEach(function (p) { t[p.ccy] = (t[p.ccy] || 0) + p.exposure; });
    var ks = Object.keys(t).sort(function (a, b) { return t[b] - t[a]; });
    var top = ks.slice(0, 4), rest = sum(ks.slice(4).map(function (k) { return t[k]; }));
    var cats = top.slice(), vals = top.map(function (k) { return m(t[k]); });
    if (rest > 0) { cats.push('Other'); vals.push(m(rest)); }
    return { cats: cats, vals: vals };
  }
  function labelsFor(days) { return days.map(dShort); }
  function sortSpec(spec, order) {
    if (!order || order === 'orig') { return spec; }
    var ix = spec.categories.map(function (c, i) { return i; }), v = spec.series[0].values;
    ix.sort(function (a, b) { return order === 'asc' ? v[a] - v[b] : v[b] - v[a]; });
    var o = {}; for (var k in spec) { o[k] = spec[k]; }
    o.categories = ix.map(function (i) { return spec.categories[i]; });
    o.series = spec.series.map(function (s) { return { name: s.name, values: ix.map(function (i) { return s.values[i]; }) }; });
    return o;
  }
  function activeView(fig, attr) { var b = fig.querySelector('button[' + attr + '][aria-pressed="true"]'); return b ? b.getAttribute(attr) : null; }
  function fiveNum(vals) {
    var a = vals.slice().sort(function (x, y) { return x - y; }); if (!a.length) { return [0, 0, 0, 0, 0]; }
    function q(p) { var i = (a.length - 1) * p, lo = Math.floor(i), hi = Math.ceil(i); return a[lo] + (a[hi] - a[lo]) * (i - lo); }
    return [a[0], q(0.25), q(0.5), q(0.75), a[a.length - 1]].map(function (v) { return Math.round(v * 100) / 100; });
  }
  function boxSpec(cats, groups, caption) {
    var f = groups.map(fiveNum);
    return { type: 'boxplot', categories: cats, categoryLabel: 'Group', caption: caption,
      series: ['Minimum', 'Q1', 'Median', 'Q3', 'Maximum'].map(function (n, i) { return { name: n, values: f.map(function (x) { return x[i]; }) }; }) };
  }

  var CHARTS = {
    'ov-cash-region': function () {
      var days = periodDays();
      var regs = DATA.REGIONS.filter(function (r) { return scopeEnts().some(function (e) { return e.region === r.id; }); });
      var names = regs.map(function (r) { return r.name; });
      var series = regs.map(function (r) {
        var acc = DATA.ACCOUNTS.filter(function (a) { var e = entOf(a.entity); return e.region === r.id && inScope(a.entity); });
        return { name: r.name, values: DATA.DAYS.map(function (d, i) { return m(sum(acc.map(function (a) { return a.series[i]; }))); }).slice(30 - S.days) };
      });
      draw('ov-cash-region', { type: 'stacked-area', categories: labelsFor(days), series: series, categoryLabel: 'Day', unit: '£m', caption: 'Cash balance by region by day, pounds millions' }, names);
    },
    'ov-facilities': function () {
      var fs = DATA.FACILITIES.filter(function (f) { return inScope(f.entity); }); if (!fs.length) { fs = DATA.FACILITIES; }
      draw('ov-facilities', { type: 'combo', categories: fs.map(function (f) { return f.name.replace('Revolving credit facility', 'RCF').replace('US commercial paper backstop', 'CP backstop'); }), categoryLabel: 'Facility',
        caption: 'Drawn amount and utilisation by facility', target: 75, targetLabel: 'Policy 75%',
        series: [{ name: 'Drawn (£m)', kind: 'column', unit: '£m', values: fs.map(function (f) { return m(f.drawnGbp); }) },
                 { name: 'Utilisation (%)', kind: 'line', unit: '', format: 'percent', values: fs.map(function (f) { return Math.round(f.drawnGbp / f.limitGbp * 1000) / 10; }) }] },
        ['Drawn — left axis, £ millions', 'Utilisation — right axis, %']);
    },
    'ov-exposure-region': function () { draw('ov-exposure-region', { type: 'bar', categories: CAT_REGION, series: [{ name: 'Exposure', values: exposureBy('region', DATA.REGIONS.map(function (r) { return r.id; })) }], unit: '£m', categoryLabel: 'Region', caption: 'Counterparty exposure by region, pounds millions' }); },
    'ov-exposure-ccy': function () { var c = ccyShares(); draw('ov-exposure-ccy', { type: 'donut', categories: c.cats, series: [{ name: 'Exposure', values: c.vals }], unit: '£m', categoryLabel: 'Currency', caption: 'Counterparty exposure by currency, pounds millions' }, c.cats); },
    'ov-exposure-kind': function () {
      var kinds = ['Deposit', 'Nostro balance', 'FX forward', 'Money market', 'Trade exposure'], v = exposureBy('kind', kinds);
      var cats = kinds.filter(function (k, i) { return v[i] > 0; }); v = v.filter(function (x) { return x > 0; });
      draw('ov-exposure-kind', { type: 'pie', categories: cats, series: [{ name: 'Exposure', values: v }], unit: '£m', categoryLabel: 'Product', caption: 'Counterparty exposure by product type, pounds millions' }, cats);
    },
    'pm-ccy': function () {
      var ps = DATA.PAYMENTS.filter(function (p) { return inScope(p.entity) && p.status === 'Awaiting approval'; }), t = {};
      ps.forEach(function (p) { t[p.ccy] = (t[p.ccy] || 0) + p.gbp; });
      var ks = Object.keys(t).sort(function (a, b) { return t[b] - t[a]; }), top = ks.slice(0, 3), rest = sum(ks.slice(4).map(function (k) { return t[k]; }));
      var cats = top.slice(), vals = top.map(function (k) { return m(t[k]); }); if (rest > 0) { cats.push('Other'); vals.push(m(rest)); }
      draw('pm-ccy', { type: 'donut', categories: cats, series: [{ name: 'Awaiting approval', values: vals }], unit: '£m', categoryLabel: 'Currency', caption: 'Value awaiting approval by payment currency, pounds millions' }, cats);
    },
    'ac-balance-entity': function () {
      var ents = scopeEnts(), fig = FIGURES['ac-balance-entity'];
      var spec = { type: 'column', categories: ents.map(function (e) { return e.short; }), series: [{ name: 'Cash', values: ents.map(function (e) { return m(sum(DATA.ACCOUNTS.filter(function (a) { return a.entity === e.id; }).map(function (a) { return a.gbp; }))); }) }], unit: '£m', categoryLabel: 'Entity', caption: 'Cash balance by entity today, pounds millions' };
      draw('ac-balance-entity', sortSpec(spec, activeView(fig, 'data-dv-view-btn')));
    },
    'ac-flows': function () {
      var ents = scopeEnts(), days = periodDays(), tx = DATA.TXNS.filter(function (t) { return days.indexOf(t.date) >= 0; });
      var inn = ents.map(function (e) { return m(sum(tx.filter(function (t) { return t.entity === e.id && t.gbp > 0; }).map(function (t) { return t.gbp; }))); });
      var out = ents.map(function (e) { return m(-sum(tx.filter(function (t) { return t.entity === e.id && t.gbp < 0; }).map(function (t) { return t.gbp; }))); });
      draw('ac-flows', { type: 'butterfly-h', categories: ents.map(function (e) { return e.short; }), series: [{ name: 'Money in', values: inn }, { name: 'Money out', values: out }], unit: '£m', categoryLabel: 'Entity', caption: 'Receipts and payments by entity in the period, pounds millions' }, ['Money in', 'Money out']);
    },
    'ac-netflow': function () {
      var fig = FIGURES['ac-netflow'], days = periodDays();
      var net = days.map(function (d) { return m(sum(DATA.TXNS.filter(function (t) { return t.date === d && inScope(t.entity); }).map(function (t) { return t.gbp; }))); });
      var cum = activeView(fig, 'data-dv-view-btn') === 'cumulative';
      if (cum) { var t = 0; net = net.map(function (v) { t += v; return Math.round(t * 10) / 10; }); }
      draw('ac-netflow', { type: 'line', categories: labelsFor(days), categoryLabel: 'Day', unit: '£m', series: [{ name: cum ? 'Cumulative net flow' : 'Net flow', values: net }], caption: cum ? 'Cumulative net cash flow, pounds millions' : 'Net cash flow by day, pounds millions' });
    },
    'lq-trend': function () {
      var days = periodDays(), cash = cashSeries(), und = undrawnCommitted(), out = scheduledOut();
      draw('lq-trend', { type: 'multiline', categories: labelsFor(days), categoryLabel: 'Day', unit: '£m', caption: 'Cash, available liquidity and funding headroom by day, pounds millions',
        series: [{ name: 'Cash', values: cash.map(m) }, { name: 'Available liquidity', values: cash.map(function (c) { return m(c + und); }) }, { name: 'Funding headroom', values: cash.map(function (c) { return m(c + und - out); }) }] },
        ['Cash', 'Available liquidity', 'Funding headroom']);
    },
    'lq-bullet': function () {
      var fs = DATA.FACILITIES.filter(function (f) { return inScope(f.entity); }); if (!fs.length) { fs = DATA.FACILITIES; }
      draw('lq-bullet', { type: 'bullet', categories: fs.map(function (f) { return f.name; }), categoryLabel: 'Facility', ranges: [50, 75, 100], unit: '%', caption: 'Utilisation by facility against target, per cent',
        series: [{ name: 'Utilisation', values: fs.map(function (f) { return Math.round(f.drawnGbp / f.limitGbp * 100); }) }, { name: 'Policy', values: fs.map(function () { return 75; }) }] });
    },
    'lq-limits': function () {
      var fs = DATA.FACILITIES.filter(function (f) { return inScope(f.entity); }); if (!fs.length) { fs = DATA.FACILITIES; }
      draw('lq-limits', { type: 'grouped-column', categories: fs.map(function (f) { return f.id; }), categoryLabel: 'Facility', unit: '£m', caption: 'Limit and drawn amount by facility, pounds millions',
        series: [{ name: 'Limit', values: fs.map(function (f) { return m(f.limitGbp); }) }, { name: 'Drawn', values: fs.map(function (f) { return m(f.drawnGbp); }) }] }, ['Limit', 'Drawn']);
    },
    'pm-status': function () {
      var ps = DATA.PAYMENTS.filter(function (p) { return inScope(p.entity); }), sts = ['Awaiting approval', 'Approved', 'Released', 'Rejected'];
      var vals = sts.map(function (s) { return m(sum(ps.filter(function (p) { return p.status === s; }).map(function (p) { return p.gbp; }))); });
      var cats = sts.filter(function (s, i) { return vals[i] > 0; }); vals = vals.filter(function (v) { return v > 0; });
      draw('pm-status', { type: 'pie', categories: cats, series: [{ name: 'Value', values: vals }], unit: '£m', categoryLabel: 'Status', caption: 'Payment value by status, pounds millions' }, cats);
    },
    'pm-valuedate': function () {
      var ps = DATA.PAYMENTS.filter(function (p) { return inScope(p.entity) && p.status === 'Awaiting approval'; });
      var ds = ['2026-09-28', '2026-09-29', '2026-09-30', '2026-10-01', '2026-10-02'], fig = FIGURES['pm-valuedate'];
      var spec = { type: 'column', categories: ds.map(dShort), series: [{ name: 'Awaiting approval', values: ds.map(function (d) { return m(sum(ps.filter(function (p) { return p.valueDate === d; }).map(function (p) { return p.gbp; }))); }) }], unit: '£m', categoryLabel: 'Value date', caption: 'Value awaiting approval by value date, pounds millions' };
      draw('pm-valuedate', sortSpec(spec, activeView(fig, 'data-dv-view-btn')));
    },
    'fx-candle': function () {
      var c = DATA.CANDLES[S.pair], n = S.days, days = periodDays(), fig = FIGURES['fx-candle'];
      var t = S.pair + ' daily range'; fig.setAttribute('data-lockup-title', t); fig.querySelector('.dv-title').textContent = t;
      draw('fx-candle', { type: 'candlestick', categories: labelsFor(days), categoryLabel: 'Day', caption: S.pair + ' open, high, low and close by day, illustrative',
        series: [{ name: 'Open', values: c.open.slice(30 - n) }, { name: 'High', values: c.high.slice(30 - n) }, { name: 'Low', values: c.low.slice(30 - n) }, { name: 'Close', values: c.close.slice(30 - n) }] });
    },
    'fx-index': function () {
      var days = periodDays(), prs = ['GBP/USD', 'GBP/EUR', 'GBP/HKD'];
      draw('fx-index', { type: 'multiline', categories: labelsFor(days), categoryLabel: 'Day', caption: 'Sterling rate indexed to 100 at the start of the period',
        series: prs.map(function (p) { var cl = DATA.CANDLES[p].close.slice(30 - S.days); return { name: p, values: cl.map(function (v) { return Math.round(v / cl[0] * 10000) / 100; }) }; }) }, prs);
    },
    'rk-region': function () { draw('rk-region', { type: 'bar', categories: CAT_REGION, series: [{ name: 'Exposure', values: exposureBy('region', DATA.REGIONS.map(function (r) { return r.id; })) }], unit: '£m', categoryLabel: 'Region', caption: 'Counterparty exposure by region, pounds millions' }); },
    'rk-scatter': function () {
      var pos = DATA.POSITIONS.filter(function (p) { return inScope(p.entity); }).slice().sort(function (a, b) { return a.exposure - b.exposure; });
      var seen = {}, cats = [], vals = [];
      pos.forEach(function (p) { var k = String(m(p.exposure)); if (seen[k]) { return; } seen[k] = 1; cats.push(k); vals.push(p.util); });
      draw('rk-scatter', { type: 'scatter', categories: cats, series: [{ name: 'Limit used (%)', values: vals }], categoryLabel: 'Exposure (£m)', caption: 'Position exposure in pounds millions against limit utilisation per cent' });
    },
    'tf-expiry': function () {
      var tr = DATA.TRADE.filter(function (t) { return inScope(t.entity) && t.status !== 'Paid'; });
      var bands = [[0, 30], [31, 60], [61, 90], [91, 120], [121, 150], [151, 180]];
      draw('tf-expiry', { type: 'histogram', categories: bands.map(function (b) { return b[0] + '–' + b[1] + ' days'; }), categoryLabel: 'Days to expiry', caption: 'Number of live instruments by days to expiry',
        series: [{ name: 'instruments', values: bands.map(function (b) { return tr.filter(function (t) { return t.daysToExpiry >= b[0] && t.daysToExpiry <= b[1]; }).length; }) }] });
    },
    'tf-box': function () {
      var kinds = ['Import letter of credit', 'Export letter of credit', 'Standby letter of credit', 'Bank guarantee', 'Documentary collection'];
      var tr = DATA.TRADE.filter(function (t) { return inScope(t.entity); });
      var groups = kinds.map(function (k) { return tr.filter(function (t) { return t.kind === k; }).map(function (t) { return m(t.gbp); }); });
      var keep = kinds.map(function (k, i) { return groups[i].length ? i : -1; }).filter(function (i) { return i >= 0; });
      draw('tf-box', boxSpec(keep.map(function (i) { return kinds[i].replace(' letter of credit', ' LC'); }), keep.map(function (i) { return groups[i]; }), 'Instrument value by type, five-number summary, pounds millions'));
    },
    'rp-outflows': function () {
      var days = periodDays();
      var regs = DATA.REGIONS.filter(function (r) { return scopeEnts().some(function (e) { return e.region === r.id; }); });
      var groups = regs.map(function (r) { return days.map(function (d) { return m(-sum(DATA.TXNS.filter(function (t) { return t.date === d && t.gbp < 0 && entOf(t.entity).region === r.id && inScope(t.entity); }).map(function (t) { return t.gbp; }))); }); });
      draw('rp-outflows', boxSpec(regs.map(function (r) { return r.name.replace('Middle East and Africa', 'MEA'); }), groups, 'Daily payments out by region in the period, five-number summary, pounds millions'));
    },
    'rp-spark': function () { var days = periodDays(); draw('rp-spark', { type: 'spark', categories: labelsFor(days), categoryLabel: 'Day', markers: true, series: [{ name: 'Group cash (£m)', values: cashSeries().map(m) }], caption: 'Group cash by day, pounds millions' }); },
    'ms-requests': function () {
      var sts = ['Awaiting your input', 'In progress', 'Submitted', 'Completed'];
      var rq = DATA.REQUESTS.filter(function (r) { return inScope(r.entity); });
      draw('ms-requests', { type: 'bar', categories: sts, series: [{ name: 'Requests', values: sts.map(function (s) { return rq.filter(function (r) { return r.status === s; }).length; }) }], categoryLabel: 'Status', caption: 'Number of service requests by status' });
    },
    'st-signins': function () { var days = periodDays(); draw('st-signins', { type: 'spark', categories: labelsFor(days), categoryLabel: 'Day', series: [{ name: 'Sign-ins', values: DATA.SIGNINS.slice(30 - S.days) }], caption: 'Sign-ins to this prototype by day' }); }
  };
  function renderCharts(view) {
    var sec = document.querySelector('.app-view[data-view="' + view + '"]');
    Object.keys(CHARTS).forEach(function (k) { if (FIGURES[k] && sec.contains(FIGURES[k])) { CHARTS[k](); } });
  }

  /* ================= KPIs (Kpi-tile, whole-tile link) and decision panels ================= */
  function spark(svg, vals) {
    var lo = Math.min.apply(null, vals), hi = Math.max.apply(null, vals), n = vals.length;
    var pts = vals.map(function (v, i) { var x = 3 + 194 * i / (n - 1), y = hi === lo ? 24 : 45 - 42 * (v - lo) / (hi - lo); return x.toFixed(1) + ',' + y.toFixed(1); });
    svg.querySelector('polyline').setAttribute('points', pts.join(' '));
    svg.querySelector('polygon').setAttribute('points', pts.join(' ') + ' 197.0,45 3.0,45');
  }
  function setKpi(key, value, series, href, per) {
    var t = document.querySelector('[data-kpi="' + key + '"]'); if (!t) { return; }
    var first = series[0], last = series[series.length - 1], ch = first ? (last - first) / Math.abs(first) * 100 : 0;
    var dir = Math.abs(ch) < 0.05 ? 'flat' : ch > 0 ? 'up' : 'down';
    var vals = t.querySelectorAll('.kpi-val > span');
    if (key === 'coverage') { vals[0].textContent = ''; vals[1].textContent = value.toFixed(2) + '×'; }
    else { vals[0].textContent = '£'; vals[1].textContent = (value / 1e6).toLocaleString('en-GB', { minimumFractionDigits: 1, maximumFractionDigits: 1 }) + 'm'; }
    var d = t.querySelector('.kpi-delta'); d.className = 'kpi-delta ' + dir;
    d.querySelector('use').setAttribute('href', '#kpi-' + dir);
    d.querySelector('.t-cm-figure-6').textContent = dir === 'flat' ? 'No change' : (ch > 0 ? '+' : MINUS) + Math.abs(ch).toFixed(1) + '% ' + dir;
    d.querySelector('.kpi-per').textContent = per;
    var sv = t.querySelector('.spark-inline'); sv.setAttribute('data-trend', dir); spark(sv, series);
    t.querySelector('.kpi-link').setAttribute('href', href);
  }
  function renderKpis() {
    var cash = cashSeries(), und = undrawnCommitted(), out = scheduledOut(), per = 'vs ' + dShort(periodDays()[0]);
    var liq = cash.map(function (c) { return c + und; }), head = liq.map(function (l) { return l - out; }), cov = liq.map(function (l) { return out ? l / out : 0; });
    setKpi('cash', cash[cash.length - 1], cash, '#/accounts', per);
    setKpi('liquidity', liq[liq.length - 1], liq, '#/liquidity', per);
    setKpi('headroom', head[head.length - 1], head, '#/liquidity', per);
    setKpi('coverage', cov[cov.length - 1], cov, '#/payments', per);
  }
  function summaryRows(dl, rows) {
    var tpl = document.getElementById('t-summary').content.querySelector('.summary__row');
    dl.innerHTML = '';
    rows.forEach(function (r) { var row = tpl.cloneNode(true); row.querySelector('dt').innerHTML = r[0]; row.querySelector('dd').innerHTML = r[1]; dl.appendChild(row); });
  }
  function renderPanels() {
    var ap = DATA.PAYMENTS.filter(function (p) { return inScope(p.entity) && p.status === 'Awaiting approval'; }).sort(function (a, b) { return b.gbp - a.gbp; });
    var ex = DATA.EXCEPTIONS.filter(function (x) { return inScope(x.entity) && x.status === 'Open'; }).sort(function (a, b) { return (a.severity === 'High' ? 0 : a.severity === 'Medium' ? 1 : 2) - (b.severity === 'High' ? 0 : b.severity === 'Medium' ? 1 : 2) || b.amount - a.amount; });
    var pa = document.querySelector('[data-panel="approvals"]'), pe = document.querySelector('[data-panel="exceptions"]');
    pa.querySelector('h2').textContent = 'Pending approvals: ' + ap.length + ' worth ' + gbpShort(sum(ap.map(function (p) { return p.gbp; })));
    pe.querySelector('h2').textContent = 'Material risk exceptions: ' + ex.length + ' open';
    summaryRows(pa.querySelector('.summary'), ap.slice(0, 4).map(function (p) { return [recLink('payments', p.id, p.beneficiary) + ' <span class="t-cm-legal">' + esc(p.id + ' · value ' + dShort(p.valueDate)) + '</span>', '<span class="t-cm-figure-6">' + gbp(p.gbp) + '</span>']; })
      .concat(ap.length ? [] : [['Nothing is waiting for you', '']]));
    summaryRows(pe.querySelector('.summary'), ex.slice(0, 4).map(function (x) { return [recLink('risk', x.id, x.title) + ' <span class="t-cm-legal">' + esc(x.id) + '</span>', '<span class="t-cm-figure-6">' + gbpShort(x.amount) + '</span> ' + status(x.severity)]; })
      .concat(ex.length ? [] : [['No open exceptions in this scope', '']]));
  }
  function renderLimits() {
    var box = UI.limits; box.innerHTML = '';
    var ls = DATA.LIMITS.filter(function (l) { return S.region === 'all' || l.region === S.region; });
    if (!ls.length) { box.innerHTML = '<p class="t-ed-body-small">No limits are set for this region.</p>'; return; }
    ls.forEach(function (l) {
      var lim = T('t-lim'), pct = l.used / l.limit * 100, left = l.limit - l.used, over = left < 0;
      var lab = lim.querySelector('.lim-label'); lab.textContent = l.name;
      var chipEl = lim.querySelector('.chip'); chipEl.className = 'chip ' + (over ? 'err' : pct > 85 ? 'warn' : 'ok'); chipEl.querySelector('.t-cm-legal').textContent = over ? 'Over limit' : pct > 85 ? 'Approaching limit' : 'Within limit';
      var amt = lim.querySelectorAll('.amount > span'); amt[0].textContent = over ? MINUS + '£' : '£'; amt[1].textContent = num(Math.abs(left) / 1e6, 1) + 'm';
      lim.querySelector('.lim-verdict').textContent = over ? 'Over the limit by this much' : 'Left before the limit';
      var tr = lim.querySelector('.pb-track'); tr.setAttribute('aria-valuenow', String(Math.round(l.used))); tr.setAttribute('aria-valuemax', String(l.limit));
      tr.setAttribute('aria-valuetext', num(l.used / 1e6, 1) + ' million pounds used of a ' + num(l.limit / 1e6, 0) + ' million pound limit');
      lim.querySelector('.pb-fill').style.width = Math.min(100, pct).toFixed(2) + '%';
      var keys = lim.querySelectorAll('.lim-key');
      keys[0].lastChild.textContent = gbpShort(l.used); keys[0].childNodes[1].textContent = 'Used ';
      keys[1].lastChild.textContent = gbpShort(Math.max(0, left)); keys[1].childNodes[1].textContent = 'Left ';
      box.appendChild(lim);
    });
  }

  /* ================= GRIDS (Data-grid markup, rows rendered from DATA) ================= */
  function gstate(key) { var g = SAVED.grids[key] = SAVED.grids[key] || {}; g.page = g.page || 1; g.pp = g.pp || 8; g.q = g.q || ''; g.density = g.density || 'comfortable'; return g; }
  var ROWS = {
    accounts: function () { return DATA.ACCOUNTS.filter(function (a) { return inScope(a.entity); }).map(function (a) { return { _id: a.id, name: a.name, entity: entOf(a.entity).short, ccy: a.ccy, local: a.local, gbp: a.gbp, _cells: { name: recLink('accounts', a.id, a.name), local: signed(a.local, function (v) { return ccyAmt(v, a.ccy); }) } }; }); },
    txns: function () { var days = periodDays(); return DATA.TXNS.filter(function (t) { return inScope(t.entity) && days.indexOf(t.date) >= 0; }).map(function (t) { return { _id: t.id, date: t.date, counterparty: t.counterparty, type: t.type, entity: entOf(t.entity).short, status: t.status, gbp: t.gbp, ref: t.ref, _cells: { date: recLink('accounts', t.id, dLong(t.date)), status: status(t.status) } }; }); },
    facilities: function () { return DATA.FACILITIES.filter(function (f) { return inScope(f.entity); }).map(function (f) { return { _id: f.id, name: f.name, entity: entOf(f.entity).short, kind: f.kind, maturity: f.maturity, limitGbp: f.limitGbp, undrawn: f.limitGbp - f.drawnGbp, _cells: { name: recLink('liquidity', f.id, f.name), maturity: esc(dLong(f.maturity)) } }; }); },
    payments: function () { return DATA.PAYMENTS.filter(function (p) { return inScope(p.entity); }).map(function (p) { return { _id: p.id, id: p.id, beneficiary: p.beneficiary, entity: entOf(p.entity).short, valueDate: p.valueDate, status: p.status, gbp: p.gbp, rail: p.rail, _cells: { id: recLink('payments', p.id), valueDate: esc(dLong(p.valueDate)), status: status(p.status) } }; }); },
    rates: function () { return DATA.PAIRS.map(function (p) { var c = DATA.CANDLES[p].close, a = c[30 - S.days], b = c[29]; return { _id: p, pair: p, rate: DATA.RATE[p], chg: Math.round((b - a) / a * 10000) / 100, _cells: { pair: '<a class="lnk t-cm-label" href="#/fx" data-pair="' + p + '">' + p + '</a>', rate: '<span class="t-cm-figure-5">' + DATA.RATE[p].toFixed(4) + '</span>', chg: '<span class="t-cm-figure-5">' + (b >= a ? '+' : MINUS) + Math.abs((b - a) / a * 100).toFixed(2) + '%</span>' } }; }); },
    deals: function () { return DATA.DEALS.filter(function (d) { return inScope(d.entity); }).map(function (d) { return { _id: d.id, id: d.id, pair: d.pair, side: d.side, kind: d.kind, maturity: d.maturity, notional: d.notional, mtm: d.mtm, entity: entOf(d.entity).short, _cells: { id: recLink('fx', d.id), maturity: esc(dLong(d.maturity)) } }; }); },
    exceptions: function () { return DATA.EXCEPTIONS.filter(function (x) { return inScope(x.entity); }).map(function (x) { return { _id: x.id, id: x.id, title: x.title, entity: entOf(x.entity).short, severity: x.severity, status: x.status, amount: x.amount, _cells: { id: recLink('risk', x.id), severity: status(x.severity), status: status(x.status) } }; }); },
    positions: function () { return DATA.POSITIONS.filter(function (p) { return inScope(p.entity); }).map(function (p) { return { _id: p.id, id: p.id, counterparty: p.counterparty, entity: entOf(p.entity).short, ccy: p.ccy, kind: p.kind, exposure: p.exposure, util: p.util, region: regName(p.region), _cells: { id: recLink('risk', p.id), util: '<span class="t-cm-figure-5">' + p.util.toFixed(1) + '%</span>' } }; }); },
    trade: function () { return DATA.TRADE.filter(function (t) { return inScope(t.entity); }).map(function (t) { return { _id: t.id, id: t.id, kind: t.kind, counterparty: t.counterparty, expiry: t.expiry, status: t.status, gbp: t.gbp, _cells: { id: recLink('trade', t.id), expiry: esc(dLong(t.expiry)), status: status(t.status) } }; }); },
    reports: function () { return DATA.REPORTS.map(function (r) { return { _id: r.id, name: r.name, area: r.area, freq: r.freq, lastRun: r.lastRun, rows: reportRows(r).length, _cells: { name: recLink('reports', r.id, r.name), lastRun: esc(dLong(r.lastRun)), rows: '<span class="t-cm-figure-5">' + reportRows(r).length + '</span>' } }; }); },
    requests: function () { return DATA.REQUESTS.filter(function (r) { return inScope(r.entity); }).map(function (r) { return { _id: r.id, id: r.id, subject: r.subject, category: r.category, opened: r.opened, priority: r.priority, status: r.status, _cells: { id: recLink('messages', r.id), opened: esc(dLong(r.opened)), status: status(r.status) } }; }); }
  };
  function cell(row, c) {
    if (row._cells && row._cells[c.key] != null) { return row._cells[c.key]; }
    var v = row[c.key];
    if (c.num) { return '<span class="t-cm-figure-5">' + (typeof v === 'number' ? gbp(v) : esc(v)) + '</span>'; }
    return '<span class="t-cm-label">' + esc(v) + '</span>';
  }
  function gridRows(key) {
    var g = gstate(key), cfg = GRIDS[key], rows = ROWS[key]();
    if (g.q) { var q = g.q.toLowerCase(); rows = rows.filter(function (r) { return Object.keys(r).some(function (k) { return k.charAt(0) !== '_' && String(r[k]).toLowerCase().indexOf(q) >= 0; }); }); }
    if (g.sort) {
      var k = g.sort, dir = g.dir === 'descending' ? -1 : 1;
      rows.sort(function (a, b) { var x = a[k], y = b[k]; return (typeof x === 'number' ? x - y : String(x).localeCompare(String(y))) * dir; });
    }
    return rows;
  }
  function renderGrid(key) {
    var cfg = GRIDS[key]; if (!cfg) { return; }
    var g = gstate(key), dg = cfg.el, rows = gridRows(key), n = rows.length;
    var pages = Math.max(1, Math.ceil(n / g.pp)); if (g.page > pages) { g.page = pages; }
    var start = (g.page - 1) * g.pp, page = rows.slice(start, start + g.pp);
    dg.setAttribute('data-density', g.density);
    dg.querySelectorAll('.dgden button').forEach(function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-density') === g.density)); });
    var s = dg.querySelector('[data-grid-search]'); if (document.activeElement !== s) { s.value = g.q; }
    dg.querySelectorAll('th[data-key]').forEach(function (th) { if (th.hasAttribute('aria-sort')) { th.setAttribute('aria-sort', th.getAttribute('data-key') === g.sort ? g.dir : 'none'); } });
    var nsel = Object.keys(cfg.sel).length;
    dg.querySelector('.dg-count').textContent = n + (n === 1 ? ' result' : ' results') + (nsel ? ' · ' + nsel + ' selected — Export CSV takes the selection' : '');
    var sa = dg.querySelector('[data-grid-selall]'), onPage = page.filter(function (r) { return cfg.sel[r._id]; }).length;
    sa.checked = page.length > 0 && onPage === page.length; sa.indeterminate = onPage > 0 && onPage < page.length;
    var tb = dg.querySelector('tbody');
    if (!n) {
      tb.innerHTML = '<tr><td colspan="' + (cfg.cols.length + 1) + '" class="dg-empty"><span class="why t-cm-label">No ' + esc(cfg.title.toLowerCase()) + ' match</span><span class="try t-cm-caption">Try a different search, or widen the entity, region or period filters.</span><button class="clearbtn t-cm-button" type="button" data-grid-clear="' + key + '">Clear the search</button></td></tr>';
    } else {
      tb.innerHTML = page.map(function (r) {
        var on = !!cfg.sel[r._id], cb = cfg.selCell.cloneNode(true), inp = cb.querySelector('input'), id = 'sel-' + key + '-' + String(r._id).replace(/[^A-Za-z0-9]/g, '');
        inp.id = id; inp.removeAttribute('tabindex'); inp.setAttribute('aria-label', 'Select ' + r._id); inp.setAttribute('data-grid-select', key); inp.setAttribute('value', r._id); if (on) { inp.setAttribute('checked', ''); }
        cb.querySelector('label').setAttribute('for', id);
        return '<tr data-id="' + esc(r._id) + '" aria-selected="' + on + '"><td class="sel">' + cb.outerHTML + '</td>' + cfg.cols.map(function (c) { return '<td' + (c.num ? ' class="num"' : '') + '>' + cell(r, c) + '</td>'; }).join('') + '</tr>';
      }).join('');
    }
    dg.querySelector('.dg-range').textContent = n ? (start + 1) + '–' + Math.min(n, start + g.pp) + ' of ' + n : '0 of 0';
    dg.querySelector('[data-grid-pp]').value = String(g.pp);
    var ul = dg.querySelector('[data-grid-pager]'), h = '<li><button class="pbtn" type="button" aria-label="Previous page" data-grid-go="prev" data-grid="' + key + '"' + (g.page === 1 ? ' disabled' : '') + '><svg viewBox="0 0 18 18" aria-hidden="true"><use href="#dg-cleft"/><\/svg></button></li>';
    var show = []; for (var q = 1; q <= pages; q++) { if (pages <= 7 || q === 1 || q === pages || Math.abs(q - g.page) <= 1 || (g.page <= 3 && q <= 4) || (g.page >= pages - 2 && q >= pages - 3)) { show.push(q); } }
    var prevShown = 0;
    for (var si = 0; si < show.length; si++) { var p = show[si]; if (p - prevShown > 1) { h += '<li><span class="cn-pagination"><span class="ellipsis" aria-hidden="true">\u2026</span></span></li>'; } prevShown = p; var cur = p === g.page; h += '<li><button class="pbtn ' + (cur ? 't-cm-button' : 't-cm-label') + '" type="button" data-grid-go="' + p + '" data-grid="' + key + '" ' + (cur ? 'aria-current="page" aria-label="Page ' + p + ', current page"' : 'aria-label="Page ' + p + '"') + '>' + p + '</button></li>'; }
    h += '<li><button class="pbtn" type="button" aria-label="Next page" data-grid-go="next" data-grid="' + key + '"' + (g.page === pages ? ' disabled' : '') + '><svg viewBox="0 0 18 18" aria-hidden="true"><use href="#dg-cright"/><\/svg></button></li>';
    ul.innerHTML = h;
  }
  var VIEW_GRIDS = { accounts: ['accounts', 'txns'], liquidity: ['facilities'], payments: ['payments'], fx: ['rates', 'deals'], risk: ['exceptions', 'positions'], trade: ['trade'], reports: ['reports'], messages: ['requests'], overview: [], settings: [] };

  /* ================= CSV export ================= */
  function csv(rows, cols) {
    var q = function (v) { v = v == null ? '' : String(v); return /[",\n]/.test(v) ? '"' + v.replace(/"/g, '""') + '"' : v; };
    return [cols.map(function (c) { return q(c.label); }).join(',')].concat(rows.map(function (r) { return cols.map(function (c) { return q(r[c.key]); }).join(','); })).join('\n');
  }
  function download(name, text) {
    var a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([text], { type: 'text/csv' })); a.download = name;
    document.body.appendChild(a); a.click(); setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 0);
    toast('Downloaded ' + name + '.');
  }
  function reportRows(r) {
    var days = periodDays();
    switch (r.source) {
      case 'accounts': return DATA.ACCOUNTS.filter(function (a) { return inScope(a.entity); });
      case 'txns': return DATA.TXNS.filter(function (t) { return inScope(t.entity) && days.indexOf(t.date) >= 0; });
      case 'facilities': return DATA.FACILITIES.filter(function (f) { return inScope(f.entity); });
      case 'payments': return DATA.PAYMENTS.filter(function (p) { return inScope(p.entity) && p.status === 'Awaiting approval'; });
      case 'deals': return DATA.DEALS.filter(function (d) { return inScope(d.entity); });
      case 'positions': return DATA.POSITIONS.filter(function (p) { return inScope(p.entity); });
      case 'exceptions': return DATA.EXCEPTIONS.filter(function (x) { return inScope(x.entity); });
      default: return DATA.TRADE.filter(function (t) { return inScope(t.entity); });
    }
  }
  function reportCsv(r) {
    var rows = reportRows(r); if (!rows.length) { return 'No rows in the current scope'; }
    var keys = Object.keys(rows[0]).filter(function (k) { return typeof rows[0][k] !== 'object'; });
    return csv(rows.map(function (x) { var o = {}; keys.forEach(function (k) { o[k] = x[k]; }); o.entity = x.entity ? entName(x.entity) : ''; return o; }), keys.map(function (k) { return { key: k, label: k }; }));
  }
  function exportView() {
    var gs = VIEW_GRIDS[S.view] || [];
    if (!gs.length) {
      var rows = DATA.PAYMENTS.filter(function (p) { return inScope(p.entity) && p.status === 'Awaiting approval'; }).map(function (p) { return { kind: 'Pending approval', id: p.id, what: p.beneficiary, entity: entName(p.entity), gbp: p.gbp }; })
        .concat(DATA.EXCEPTIONS.filter(function (x) { return inScope(x.entity) && x.status === 'Open'; }).map(function (x) { return { kind: 'Risk exception', id: x.id, what: x.title, entity: entName(x.entity), gbp: x.amount }; }));
      download('decisions-' + DATA.ASAT + '.csv', csv(rows, [{ key: 'kind', label: 'Item' }, { key: 'id', label: 'Reference' }, { key: 'what', label: 'Detail' }, { key: 'entity', label: 'Entity' }, { key: 'gbp', label: 'GBP' }]));
      return;
    }
    var k = gs.filter(function (g) { return Object.keys(GRIDS[g].sel).length; })[0] || gs[gs.length > 1 && S.view === 'accounts' ? 1 : 0];
    var rows = gridRows(k), sel = GRIDS[k].sel;
    if (Object.keys(sel).length) { rows = rows.filter(function (r) { return sel[r._id]; }); }
    download(k + (Object.keys(sel).length ? '-selected' : '') + '-' + DATA.ASAT + '.csv', csv(rows, GRIDS[k].cols));
  }

  /* ================= TOAST · MODAL · DRAWER ================= */
  function toast(msg) {
    var t = T('t-toast'); t.querySelector('.msg').textContent = msg;
    UI.toasts.appendChild(t);
    var timer = setTimeout(function () { t.remove(); }, 5000);
    t.querySelector('.x').addEventListener('click', function () { clearTimeout(timer); t.remove(); });
  }
  var lastFocus = null, lastRecord = null;
  function setInert(on) { [document.getElementById('app')].forEach(function (n) { n.inert = on; if (on) { n.setAttribute('aria-hidden', 'true'); } else { n.removeAttribute('aria-hidden'); } }); }
  function confirmBox(title, body, label) {
    return new Promise(function (resolve) {
      var ov = UI.modal, dlg = ov.querySelector('.dialog');
      dlg.querySelector('h2').textContent = title; dlg.querySelector('p').textContent = body;
      var bs = dlg.querySelectorAll('.actions .btn'); bs[0].textContent = label; bs[1].textContent = 'Cancel';
      var prev = document.activeElement;
      UI.sheet.inert = true;
      ov.classList.add('open');
      setTimeout(function () { bs[0].focus(); }, 30);
      function done(v) { ov.classList.remove('open'); UI.sheet.inert = false; bs[0].onclick = bs[1].onclick = dlg.querySelector('.close').onclick = null; document.removeEventListener('keydown', esc1, true); if (prev) { prev.focus(); } resolve(v); }
      function esc1(e) { if (e.key === 'Escape') { e.stopPropagation(); done(false); } }
      bs[0].onclick = function () { done(true); }; bs[1].onclick = function () { done(false); }; dlg.querySelector('.close').onclick = function () { done(false); };
      document.addEventListener('keydown', esc1, true);
    });
  }
  /* Drawer's graph edge: it must not sit with an open modal — so a decision taken INSIDE the drawer is
     confirmed inside it: an Alert states the consequence and the foot swaps to Confirm / Back. */
  function confirmStep(title, body, label) {
    return new Promise(function (resolve) {
      var sh = UI.sheet, bodyEl = sh.querySelector('.sheet-body'), foot = sh.querySelector('.sheet-foot');
      var saved = [].slice.call(foot.children);
      var al = alertBox('warn', title, body); al.setAttribute('data-confirm-step', ''); var alw = wrap('cn-alert', al); bodyEl.insertBefore(alw, bodyEl.firstChild);
      var p = (saved.filter(function (b) { return b.classList.contains('primary'); })[0] || saved[0]).cloneNode(false), s2 = saved[saved.length - 1].cloneNode(false);
      p.textContent = label; s2.textContent = 'Back';
      foot.innerHTML = ''; foot.appendChild(p); foot.appendChild(s2); p.focus();
      function done(v) { alw.remove(); foot.innerHTML = ''; saved.forEach(function (b) { foot.appendChild(b); }); resolve(v); }
      p.addEventListener('click', function () { done(true); }); s2.addEventListener('click', function () { done(false); });
    });
  }
  function openDrawer(title, build, actions) {
    var sh = UI.sheet, body = sh.querySelector('.sheet-body'), foot = sh.querySelector('.sheet-foot');
    sh.querySelector('.sheet-head h3').textContent = title;
    body.innerHTML = ''; build(body);
    var tplP = foot.querySelector('.dbtn.primary') || document.getElementById('t-sheet').content.querySelector('.dbtn.primary');
    var tplS = foot.querySelector('.dbtn.secondary') || document.getElementById('t-sheet').content.querySelector('.dbtn.secondary');
    var p = tplP.cloneNode(true), s = tplS.cloneNode(true); p.removeAttribute('id'); s.removeAttribute('id');
    foot.innerHTML = '';
    (actions || []).forEach(function (a) { var b = (a.primary ? p : s).cloneNode(true); b.textContent = a.label; b.addEventListener('click', a.run); foot.appendChild(b); });
    var c = s.cloneNode(true); c.textContent = 'Close'; c.addEventListener('click', closeDrawer); foot.appendChild(c);
    if (!sh.classList.contains('open')) { lastFocus = document.activeElement; lastRecord = S.record; }
    UI.scrim.classList.add('open'); sh.classList.add('open');
    requestAnimationFrame(function () { requestAnimationFrame(function () { var f = sh.querySelector('.sheet-head .close'); f.focus(); setInert(true); }); });
  }
  function closeDrawer(fromRoute) {
    if (!UI.sheet.classList.contains('open')) { return; }
    UI.scrim.classList.remove('open'); UI.sheet.classList.remove('open'); setInert(false);
    if (lastFocus && !document.contains(lastFocus) && lastRecord) { lastFocus = document.querySelector('.app-view:not([hidden]) a[data-record="' + lastRecord + '"]'); }
    if (lastFocus && document.contains(lastFocus)) { lastFocus.focus(); }
    if (fromRoute !== true && S.record) { S.record = null; writeUrl(false); }
  }

  /* ---------- form parts, cloned from Input-fields, Textarea, Dropdown, Segmented-control ---------- */
  function field(label, id, value, opts) {
    opts = opts || {};
    var f = T('t-field'), inp = f.querySelector('input'); f._scope = 'cn-input-fields';
    ['.help-btn', '.tail-btn', '.count'].forEach(function (s) { var n = f.querySelector(s); if (n) { n.remove(); } });
    var pre = f.querySelector('.prefix'); if (opts.prefix) { pre.textContent = opts.prefix; } else { pre.remove(); }
    var lab = f.querySelector('label'); lab.textContent = label; lab.setAttribute('for', id);
    inp.id = id; inp.value = value || ''; inp.removeAttribute('maxlength'); inp.setAttribute('placeholder', opts.placeholder || '');
    inp.setAttribute('inputmode', opts.inputmode || 'text');
    var help = f.querySelector('.help-text'); if (opts.help) { help.textContent = opts.help; help.id = id + '-help'; inp.setAttribute('aria-describedby', help.id); } else { help.remove(); inp.removeAttribute('aria-describedby'); }
    return f;
  }
  function textarea(label, id, help, max) {
    var g = T('t-tx'), ta = g.querySelector('textarea'); g._scope = 'cn-textarea';
    var lab = g.querySelector('label'); lab.textContent = label; lab.setAttribute('for', id);
    ta.id = id; ta.value = ''; ta.setAttribute('maxlength', String(max || 300));
    var h = g.querySelector('.tx-help'); h.textContent = help; h.id = id + '-help';
    var c = g.querySelector('.tx-count'); c.id = id + '-count'; c.textContent = '0/' + (max || 300);
    ta.setAttribute('aria-describedby', h.id + ' ' + c.id);
    var live = g.querySelector('.sr-live'); if (live) { live.id = id + '-live'; }
    ta.addEventListener('input', function () { c.textContent = ta.value.length + '/' + (max || 300); });
    return g;
  }
  function dropdown(label, opts, current) {
    var dd = T('t-dd'); dd._scope = 'cn-dropdown'; dd.querySelector('label').textContent = label;
    var menu = dd.querySelector('.menu'), tpl = menu.querySelector('.opt').cloneNode(true); menu.innerHTML = '';
    opts.forEach(function (o) { var li = tpl.cloneNode(true); li.firstChild.textContent = o[1] + ' '; li.setAttribute('data-value', o[0]); li.setAttribute('aria-selected', String(o[0] === current)); menu.appendChild(li); });
    dd.querySelector('.ddval').textContent = (opts.filter(function (o) { return o[0] === current; })[0] || opts[0])[1];
    dd.setAttribute('data-value', current);
    return dd;
  }
  function segmented(label, opts, current) {
    var seg = T('t-seg'); seg._scope = 'cn-segmented-control'; seg.setAttribute('aria-label', label);
    var bs = seg.querySelectorAll('button'); for (var i = opts.length; i < bs.length; i++) { bs[i].remove(); }
    opts.forEach(function (o, i) { bs[i].textContent = o[1]; bs[i].setAttribute('data-value', o[0]); bs[i].setAttribute('aria-pressed', String(o[0] === current)); });
    seg.setAttribute('data-value', current);
    return seg;
  }
  function setError(wrapper, msg) {
    var isTx = wrapper.classList.contains('tx-group'), ctl = wrapper.querySelector('input,textarea,button.trigger');
    var old = wrapper.querySelector('.err-msg,.tx-msg'); if (old) { old.remove(); }
    wrapper.classList.toggle('is-error', !!msg);
    if (!msg) { if (ctl) { ctl.removeAttribute('aria-invalid'); } return true; }
    var id = (ctl && ctl.id ? ctl.id : 'f' + (++UID)) + '-err';
    var m = H('<div class="' + (isTx ? 'tx-msg' : 'err-msg') + '"><span class="ic" aria-hidden="true"><svg class="icn" viewBox="0 0 18 18"><use href="#ic-error"/><\/svg></span><p id="' + id + '"' + (isTx ? ' class="t-ed-body"' : '') + '>' + esc(msg) + '</p></div>');
    wrapper.appendChild(m);
    if (ctl) { ctl.setAttribute('aria-invalid', 'true'); ctl.setAttribute('aria-describedby', ((ctl.getAttribute('aria-describedby') || '').replace(id, '') + ' ' + id).trim()); }
    return false;
  }
  function alertBox(kind, title, text) { var a = T(kind === 'ok' ? 't-alertok' : kind === 'warn' ? 't-alertwarn' : 't-alert'); a._scope = 'cn-alert'; var p = a.querySelector('.main'); p.innerHTML = '<strong class="em">' + esc(title) + '</strong> ' + esc(text); var x = a.querySelector('.x'); if (x) { x.addEventListener('click', function () { a.remove(); }); } return a; }
  function timeline(title, items) {
    var tl = T('t-tl'); tl._scope = 'cn-timeline'; var grp = tl.querySelector('.tl-group'), li = grp.querySelector('li').cloneNode(true);
    tl.querySelectorAll('.tl-group').forEach(function (g, i) { if (i) { g.remove(); } });
    tl.querySelector('h2').textContent = title; grp.querySelector('h3').textContent = title;
    var ol = grp.querySelector('ol'); ol.innerHTML = '';
    items.slice().reverse().forEach(function (it) {
      var n = li.cloneNode(true); n.className = it.state || 'inf';
      n.querySelector('.tl-title').textContent = it.what;
      var am = n.querySelector('.tl-amount'); if (it.amount) { am.textContent = it.amount; } else { am.remove(); }
      var tm = n.querySelector('time'); tm.textContent = it.at; tm.setAttribute('datetime', it.at.replace(' ', 'T'));
      var st = n.querySelector('.status'); st.className = 'status ' + (it.state || 'inf') + ' t-cm-legal'; st.lastChild.textContent = it.label || '';
      if (!it.label) { st.remove(); }
      var d = n.querySelector('.tl-desc'); if (it.note) { if (!d) { d = H('<p class="tl-desc t-ed-body-small"></p>'); n.appendChild(d); } d.textContent = it.note; } else if (d) { d.remove(); }
      ol.appendChild(n);
    });
    return tl;
  }
  function add(parent, el) { parent.appendChild(el._scope ? wrap(el._scope, el) : el); return el; }
  function kv(rows) { var dl = T('t-summary'); dl._scope = 'cn-summary'; summaryRows(dl, rows.map(function (r) { return [esc(r[0]), r[2] ? r[1] : esc(r[1])]; })); return dl; }
  function now() { var d = new Date(); return DATA.ASAT + ' ' + String(d.getHours()).padStart(2, '0') + ':' + String(d.getMinutes()).padStart(2, '0'); }

  /* ================= RECORDS: detail drawers and their workflows ================= */
  function openRecord(view, id) {
    var p;
    if (view === 'payments' && (p = byId(DATA.PAYMENTS, id))) { return paymentDrawer(p); }
    if (view === 'risk' && (p = byId(DATA.EXCEPTIONS, id))) { return exceptionDrawer(p); }
    if (view === 'risk' && (p = byId(DATA.POSITIONS, id))) {
      return openDrawer('Position ' + p.id, function (b) { add(b, kv([['Counterparty', p.counterparty], ['Entity', entName(p.entity)], ['Region', regName(p.region)], ['Currency', p.ccy], ['Type', p.kind], ['Exposure', gbp(p.exposure)], ['Limit', gbp(p.limit)], ['Limit used', p.util.toFixed(1) + '%']])); if (p.util > 100) { add(b, alertBox('err', 'Over limit.', 'This position is above its limit. Any exception raised against it is listed under Limit exceptions.')); } });
    }
    if (view === 'accounts' && (p = byId(DATA.ACCOUNTS, id))) {
      return openDrawer(p.name, function (b) { add(b, kv([['Entity', entName(p.entity)], ['Account', p.iban], ['Currency', p.ccy], ['Balance', ccyAmt(p.local, p.ccy)], ['Balance in GBP', gbp(p.gbp)], ['Illustrative rate', p.ccy === 'GBP' ? '1.0000' : '1 ' + p.ccy + ' = £' + DATA.FX[p.ccy].toFixed(4)]])); },
        [{ label: 'Show its transactions', primary: true, run: function () { gstate('txns').q = p.entity ? entOf(p.entity).short : ''; gstate('txns').page = 1; save(); closeDrawer(); renderGrid('txns'); GRIDS.txns.el.scrollIntoView({ block: 'start' }); } }]);
    }
    if (view === 'accounts' && (p = byId(DATA.TXNS, id))) {
      return openDrawer('Transaction ' + p.id, function (b) { add(b, kv([['Date', dLong(p.date)], ['Counterparty', p.counterparty], ['Type', p.type], ['Entity', entName(p.entity)], ['Account', byId(DATA.ACCOUNTS, p.account).name], ['Amount', ccyAmt(p.amount, p.ccy)], ['Amount in GBP', gbp(p.gbp)], ['Reference', p.ref], ['Status', status(p.status), true]])); },
        [{ label: 'Download as CSV', primary: true, run: function () { download(p.id + '.csv', csv([p], ['id', 'date', 'counterparty', 'type', 'ccy', 'amount', 'gbp', 'ref', 'status'].map(function (k) { return { key: k, label: k }; }))); } }]);
    }
    if (view === 'liquidity' && (p = byId(DATA.FACILITIES, id))) { return facilityDrawer(p); }
    if (view === 'fx' && (p = byId(DATA.DEALS, id))) {
      return openDrawer('FX deal ' + p.id, function (b) { add(b, kv([['Entity', entName(p.entity)], ['Pair', p.pair], ['Side', p.side + ' sterling'], ['Type', p.kind], ['Notional', gbp(p.notional)], ['Deal rate', p.rate.toFixed(4)], ['Illustrative rate now', DATA.RATE[p.pair].toFixed(4)], ['Valuation', gbp(p.mtm)], ['Maturity', dLong(p.maturity)]])); });
    }
    if (view === 'trade' && (p = byId(DATA.TRADE, id))) { return tradeDrawer(p); }
    if (view === 'reports' && (p = byId(DATA.REPORTS, id))) { return reportDrawer(p); }
    if (view === 'messages' && (p = byId(DATA.REQUESTS, id))) { return requestDrawer(p); }
    if (view === 'messages' && (p = byId(DATA.MESSAGES, id))) { return messageDrawer(p); }
    return false;
  }
  function paymentDrawer(p) {
    var pending = p.status === 'Awaiting approval', reason;
    openDrawer('Payment ' + p.id, function (b) {
      if (p.flag !== 'None' && pending) { add(b, alertBox('warn', p.flag + '.', 'Check the beneficiary and amount before you approve.')); }
      add(b, kv([['Beneficiary', p.beneficiary], ['From', entName(p.entity)], ['Amount', ccyAmt(p.amount, p.ccy)], ['In GBP', gbp(p.gbp)], ['Rail', p.rail], ['Value date', dLong(p.valueDate)], ['Initiated by', p.initiator + ' on ' + dLong(p.created)], ['Approvals', p.approvals + ' of ' + p.required], ['Status', status(p.status), true]]));
      if (pending) { reason = textarea('Note for the audit trail', 'pm-note', 'Required if you reject. Visible to approvers and auditors.', 300); add(b, reason); }
      add(b, timeline('Audit trail', [{ at: dLong(p.created), what: 'Created by ' + p.initiator, state: 'inf', label: 'Created' }].concat(p.approvals && p.status !== 'Rejected' ? [{ at: dLong(p.created), what: 'First approval recorded', state: 'ok', label: 'Approved' }] : []).concat(p.audit)));
    }, pending ? [
      { label: 'Approve', primary: true, run: function () {
        confirmStep('Approve ' + p.id + '?', 'You are approving ' + gbp(p.gbp) + ' to ' + p.beneficiary + ' for value ' + dLong(p.valueDate) + '. This is a simulation; no payment will be sent.', 'Approve payment').then(function (ok) {
          if (!ok) { return; }
          p.approvals = Math.min(p.required, p.approvals + 1); p.status = p.approvals >= p.required ? 'Approved' : 'Awaiting approval';
          var note = reason.querySelector('textarea').value.trim();
          p.audit = p.audit.concat([{ at: now(), what: 'Approved by Group CEO' + (p.status === 'Approved' ? ' — ready to release' : ' — one more approval needed'), state: 'ok', label: 'Approved', note: note }]);
          remember('payments', { id: p.id, status: p.status, approvals: p.approvals, audit: p.audit });
          toast(p.id + (p.status === 'Approved' ? ' approved and ready to release.' : ' approved; it needs one more approver.'));
          refresh(); paymentDrawer(p);
        });
      } },
      { label: 'Reject', run: function () {
        var note = reason.querySelector('textarea').value.trim();
        if (!setError(reason, note.length < 10 ? 'Enter a reason of at least 10 characters to reject this payment.' : '')) { reason.querySelector('textarea').focus(); return; }
        confirmStep('Reject ' + p.id + '?', 'The payment will be returned to ' + p.initiator + ' with your note. This is a simulation.', 'Reject payment').then(function (ok) {
          if (!ok) { return; }
          p.status = 'Rejected'; p.audit = p.audit.concat([{ at: now(), what: 'Rejected by Group CEO', state: 'err', label: 'Rejected', note: note }]);
          remember('payments', { id: p.id, status: p.status, approvals: p.approvals, audit: p.audit });
          toast(p.id + ' rejected and returned to ' + p.initiator + '.'); refresh(); paymentDrawer(p);
        });
      } }] : []);
  }
  function exceptionDrawer(x) {
    var open = x.status === 'Open', note;
    var pos = byId(DATA.POSITIONS, x.position);
    openDrawer(x.title, function (b) {
      add(b, kv([['Reference', x.id], ['Entity', entName(x.entity)], ['Region', regName(x.region)], ['Currency', x.ccy], ['Severity', status(x.severity), true], ['Excess', gbp(x.amount)], ['Raised', dLong(x.raised)], ['Position', recLink('risk', x.position), true], ['Limit used', pos ? pos.util.toFixed(1) + '%' : '—'], ['Status', status(x.status), true]]));
      if (open) { note = textarea('Acknowledgement note', 'ex-note', 'Say what you have agreed and who owns the fix. At least 20 characters.', 400); add(b, note); }
      add(b, timeline('Audit trail', [{ at: dLong(x.raised), what: 'Exception raised by limit monitoring', state: 'err', label: 'Raised' }].concat(x.audit.map(function (a) { return { at: a.at, what: 'Acknowledged by ' + a.by, state: 'ok', label: 'Acknowledged', note: a.note }; }))));
    }, open ? [{ label: 'Acknowledge', primary: true, run: function () {
      var v = note.querySelector('textarea').value.trim();
      if (!setError(note, v.length < 20 ? 'Write an audit note of at least 20 characters before you acknowledge.' : '')) { note.querySelector('textarea').focus(); return; }
      x.status = 'Acknowledged'; x.audit = x.audit.concat([{ at: now(), by: 'Group CEO', note: v }]);
      remember('exceptions', { id: x.id, status: x.status, audit: x.audit });
      toast(x.id + ' acknowledged with your note.'); refresh(); exceptionDrawer(x);
    } }] : []);
  }
  function facilityDrawer(f) {
    var amt, date;
    var undrawn = f.limitGbp - f.drawnGbp;
    openDrawer(f.name, function (b) {
      add(b, kv([['Borrower', entName(f.entity)], ['Type', f.kind], ['Currency', f.ccy], ['Limit', ccyAmt(f.limit, f.ccy)], ['Drawn', ccyAmt(f.drawn, f.ccy)], ['Undrawn in GBP', gbp(undrawn)], ['Utilisation', (f.drawnGbp / f.limitGbp * 100).toFixed(1) + '%'], ['Maturity', dLong(f.maturity)]]));
      if (undrawn > 0) {
        amt = field('Drawdown amount', 'fc-amt', '', { prefix: f.ccy, inputmode: 'decimal', help: 'Up to ' + ccyAmt(f.limit - f.drawn, f.ccy) + ' is undrawn.' }); add(b, amt);
        date = field('Value date', 'fc-date', '2026-09-30', { help: 'Format YYYY-MM-DD, a business day after ' + dLong(DATA.ASAT) + '.' }); add(b, date);
      } else { add(b, alertBox('warn', 'Fully drawn.', 'There is nothing left to draw on this facility.')); }
      if (f.requests.length) { add(b, timeline('Drawdown requests', f.requests.map(function (r) { return { at: r.at, what: 'Drawdown of ' + ccyAmt(r.amount, f.ccy) + ' for value ' + dLong(r.value), state: 'inf', label: 'Requested' }; }))); }
    }, undrawn > 0 ? [{ label: 'Request drawdown', primary: true, run: function () {
      var a = parseFloat(amt.querySelector('input').value.replace(/[, ]/g, '')), d = date.querySelector('input').value.trim();
      var ok1 = setError(amt, !(a > 0) ? 'Enter an amount greater than zero.' : a > f.limit - f.drawn ? 'That is more than the undrawn ' + ccyAmt(f.limit - f.drawn, f.ccy) + '.' : '');
      var dd = new Date(d + 'T00:00:00Z'), wd = dd.getUTCDay();
      var ok2 = setError(date, !/^\d{4}-\d{2}-\d{2}$/.test(d) || isNaN(dd) ? 'Enter the date as YYYY-MM-DD.' : d <= DATA.ASAT ? 'Choose a date after ' + dLong(DATA.ASAT) + '.' : (wd === 0 || wd === 6) ? 'Choose a business day, not a weekend.' : '');
      if (!ok1 || !ok2) { (ok1 ? date : amt).querySelector('input').focus(); return; }
      var r = { id: 'DD-' + Date.now(), facility: f.id, amount: a, value: d, at: now() };
      f.requests.push(r); remember('drawdowns', r);
      toast('Drawdown request for ' + ccyAmt(a, f.ccy) + ' sent to HSBC (simulated).'); facilityDrawer(f);
    } }] : []);
  }
  function tradeDrawer(t) {
    openDrawer(t.kind + ' ' + t.id, function (b) {
      if (t.status === 'Documents discrepant') { add(b, alertBox('err', 'Documents discrepant.', 'HSBC needs your instruction to accept or refuse the documents.')); }
      add(b, kv([['Entity', entName(t.entity)], ['Counterparty', t.counterparty], ['Amount', ccyAmt(t.amount, t.ccy)], ['In GBP', gbp(t.gbp)], ['Expiry', dLong(t.expiry) + ' (' + t.daysToExpiry + ' days)'], ['Status', status(t.status), true]]));
    }, t.status === 'Paid' ? [] : [{ label: 'Request an amendment', primary: true, run: function () { closeDrawer(); newRequest({ category: 'Trade', entity: t.entity, subject: 'Amend ' + t.kind.toLowerCase() + ' ' + t.id }); } }]);
  }
  function reportDrawer(r) {
    openDrawer(r.name, function (b) { add(b, kv([['Area', r.area], ['Frequency', r.freq], ['Last run', dLong(r.lastRun)], ['Rows in current scope', String(reportRows(r).length)], ['Format', 'CSV']])); },
      [{ label: 'Run now', primary: true, run: function () { r.lastRun = now(); remember('runs', { id: r.id, lastRun: r.lastRun }); toast(r.name + ' ran with ' + reportRows(r).length + ' rows.'); refresh(); reportDrawer(r); } },
       { label: 'Download CSV', run: function () { download(r.id + '-' + r.name.toLowerCase().replace(/[^a-z]+/g, '-') + '.csv', reportCsv(r)); } }]);
  }
  function requestDrawer(r) {
    openDrawer(r.id + ' — ' + r.subject, function (b) {
      add(b, kv([['Category', r.category], ['Entity', entName(r.entity)], ['Priority', r.priority], ['Opened', dLong(r.opened)], ['Status', status(r.status), true]]));
      add(b, timeline('Progress', r.history.map(function (h) { return { at: h.at, what: h.what, state: h.state, label: '' }; })));
    });
  }
  function messageDrawer(msg) {
    var reply;
    if (msg.unread) { msg.unread = false; W.unreads = (W.unreads || []).filter(function (i) { return i !== msg.id; }); W.reads = (W.reads || []).filter(function (i) { return i !== msg.id; }).concat([msg.id]); save(); renderInbox(); }
    openDrawer(msg.subject, function (b) {
      add(b, kv([['From', msg.from + ', HSBC'], ['Received', dLong(msg.date)]]));
      add(b, H('<p class="t-ed-body"></p>')).textContent = msg.body;
      if (msg.replies && msg.replies.length) { add(b, timeline('Your replies', msg.replies.map(function (r) { return { at: r.at, what: 'You replied', state: 'ok', label: 'Sent', note: r.text }; }))); }
      reply = textarea('Reply to ' + msg.from.toLowerCase(), 'ms-reply', 'Replies go to your HSBC team in this simulation only.', 500); add(b, reply);
    }, [{ label: 'Send reply', primary: true, run: function () {
      var v = reply.querySelector('textarea').value.trim();
      if (!setError(reply, v.length < 2 ? 'Write a reply before you send it.' : '')) { reply.querySelector('textarea').focus(); return; }
      msg.replies = (msg.replies || []).concat([{ at: now(), text: v }]); remember('replies', { id: msg.id, replies: msg.replies });
      toast('Reply sent to ' + msg.from.toLowerCase() + ' (simulated).'); messageDrawer(msg);
    } }, { label: 'Mark as unread', run: function () { msg.unread = true; W.reads = (W.reads || []).filter(function (i) { return i !== msg.id; }); W.unreads = (W.unreads || []).filter(function (i) { return i !== msg.id; }).concat([msg.id]); save(); renderInbox(); closeDrawer(); toast('Marked as unread.'); } }]);
  }
  function newRequest(pre) {
    pre = pre || {};
    var cat, ent, subj, desc, pri;
    openDrawer('New service request', function (b) {
      cat = dropdown('Category', [['Account services', 'Account services'], ['Payments', 'Payments'], ['Liquidity', 'Liquidity'], ['Trade', 'Trade'], ['User access', 'User access']], pre.category || 'Account services');
      ent = dropdown('Entity', DATA.ENTITIES.map(function (e) { return [e.id, e.name]; }), pre.entity || (S.entity !== 'all' ? S.entity : 'E01'));
      subj = field('Subject', 'sr-subj', pre.subject || '', { help: 'At least 8 characters.' });
      desc = textarea('What do you need?', 'sr-desc', 'At least 20 characters. Do not include passwords or card numbers.', 600);
      var lab = H('<p class="t-cm-label">Priority</p>');
      pri = segmented('Priority', [['Low', 'Low'], ['Normal', 'Normal'], ['High', 'High']], 'Normal');
      [cat, ent, subj, desc, lab, pri].forEach(function (n) { add(b, n); });
    }, [{ label: 'Submit request', primary: true, run: function () {
      var s = subj.querySelector('input').value.trim(), d = desc.querySelector('textarea').value.trim();
      var ok1 = setError(subj, s.length < 8 ? 'Enter a subject of at least 8 characters.' : '');
      var ok2 = setError(desc, d.length < 20 ? 'Describe what you need in at least 20 characters.' : /\b\d{12,19}\b/.test(d) ? 'Remove what looks like a card or account number.' : '');
      if (!ok1 || !ok2) { (ok1 ? desc.querySelector('textarea') : subj.querySelector('input')).focus(); return; }
      var id = 'SR-' + (3312 + DATA.REQUESTS.filter(function (r) { return r.id >= 'SR-3312'; }).length);
      var r = { id: id, category: cat.getAttribute('data-value'), subject: s, entity: ent.getAttribute('data-value'), priority: pri.getAttribute('data-value'), status: 'Submitted', opened: DATA.ASAT, detail: d,
        history: [{ at: now(), what: 'Request submitted', state: 'inf' }] };
      DATA.REQUESTS.unshift(r); remember('requests', r);
      toast(id + ' submitted to HSBC (simulated).'); closeDrawer();
      if (S.view !== 'messages') { go('messages', null); } else { refresh(); }
    } }]);
  }
  function renderInbox() {
    var ul = UI.inbox; ul.innerHTML = '';
    DATA.MESSAGES.forEach(function (msg) {
      var li = UI.inboxLi.cloneNode(true), row = li.querySelector('.row');
      row.setAttribute('data-message', msg.id);
      var av = li.querySelector('.avatar'); av.textContent = 'HS'; av.setAttribute('aria-label', 'HSBC');
      li.querySelector('.title').textContent = msg.subject;
      var st = li.querySelector('.status'); st.className = 'status ' + (msg.unread ? 'warn' : 'ok'); st.lastChild.textContent = msg.unread ? 'Unread' : 'Read';
      li.querySelector('.desc').textContent = dShort(msg.date) + ' · ' + msg.from;
      var am = li.querySelector('.amount'); if (am) { am.remove(); }
      ul.appendChild(li);
    });
  }
  function bookDeal() {
    var pr, side, amt;
    openDrawer('Book an FX deal', function (b) {
      add(b, alertBox('warn', 'Illustrative only.', 'Rates are placeholders as at ' + dLong(DATA.ASAT) + '. Nothing is sent to a market.'));
      pr = dropdown('Currency pair', DATA.PAIRS.map(function (p) { return [p, p + ' at ' + DATA.RATE[p].toFixed(4)]; }), S.pair);
      side = segmented('Side', [['Buy', 'Buy sterling'], ['Sell', 'Sell sterling']], 'Buy');
      amt = field('Amount in GBP', 'fx-amt', '', { prefix: 'GBP', inputmode: 'decimal', help: 'Between £100,000 and £25,000,000.' });
      [pr, side, amt].forEach(function (n) { add(b, n); });
    }, [{ label: 'Book deal', primary: true, run: function () {
      var a = parseFloat(amt.querySelector('input').value.replace(/[, ]/g, ''));
      if (!setError(amt, !(a >= 1e5 && a <= 2.5e7) ? 'Enter an amount between £100,000 and £25,000,000.' : '')) { amt.querySelector('input').focus(); return; }
      var p = pr.getAttribute('data-value'), sd = side.getAttribute('data-value');
      confirmStep('Book ' + sd.toLowerCase() + ' ' + gbp(a) + ' against ' + p.slice(4) + '?', 'At the illustrative rate of ' + DATA.RATE[p].toFixed(4) + ' that is ' + ccyAmt(a * DATA.RATE[p], p.slice(4)) + '. Simulation only.', 'Book deal').then(function (ok) {
        if (!ok) { return; }
        var d = { id: 'FXD-' + (8000 + DATA.DEALS.length), entity: S.entity !== 'all' ? S.entity : 'E01', pair: p, side: sd, kind: 'Spot', notional: a, rate: DATA.RATE[p], maturity: '2026-09-29', mtm: 0 };
        DATA.DEALS.unshift(d); remember('deals', d); toast(d.id + ' booked (simulated).'); closeDrawer(); refresh();
      });
    } }]);
  }

  /* ================= FILTER BAR, THEME, NAV, ROUTER ================= */
  function setDd(dd, value) {
    var menu = dd.querySelector('.menu'); var label = null;
    menu.querySelectorAll('.opt').forEach(function (o) { var on = o.getAttribute('data-value') === String(value); o.setAttribute('aria-selected', String(on)); if (on) { label = o.firstChild.textContent.trim(); } });
    if (label) { dd.querySelector('.ddval').textContent = label; }
    dd.setAttribute('data-value', value);
  }
  function syncFilterBar() {
    setDd(document.getElementById('flt-entity'), S.entity); setDd(document.getElementById('flt-region'), S.region); setDd(document.getElementById('flt-days'), String(S.days));
    var chips = [], tpl = document.getElementById('t-filterbar').content.querySelector('.tag');
    UI.ftbChips.innerHTML = '';
    [['entity', S.entity !== 'all' ? entName(S.entity) : null], ['region', S.region !== 'all' ? regName(S.region) : null], ['days', S.days !== 30 ? 'Last ' + S.days + ' days' : null]].forEach(function (c) {
      if (!c[1]) { return; }
      var t = tpl.cloneNode(true); t.querySelector('.lbl').textContent = c[1]; t.querySelector('.lbl').removeAttribute('title');
      var x = t.querySelector('.x'); x.setAttribute('aria-label', 'Remove filter: ' + c[1]); x.setAttribute('data-unfilter', c[0]); x.setAttribute('type', 'button');
      UI.ftbChips.appendChild(t); chips.push(c);
    });
    UI.ftb.setAttribute('data-ftb-state', chips.length ? 'filtered' : 'no-filters');
    UI.ftbCount.textContent = String(scopeEnts().length);
  }
  function moveSeg(seg) {
    var ind = seg.querySelector('.ind'), a = seg.querySelector('button[aria-pressed="true"]'); if (!ind || !a) { return; }
    var sr = seg.getBoundingClientRect(), br = a.getBoundingClientRect(); if (!sr.width) { return; }
    ind.style.left = (br.left - sr.left - seg.clientLeft) + 'px'; ind.style.width = br.width + 'px';
  }
  function placeSegs() { document.querySelectorAll('.seg').forEach(moveSeg); }
  function setTheme(t, persist) {
    document.documentElement.setAttribute('data-theme', t);
    [UI.themeSeg, UI.themeSeg2].forEach(function (seg) { seg.querySelectorAll('button').forEach(function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-theme-set') === t)); }); });
    if (persist) { try { localStorage.setItem('ceo.theme', t); } catch (e) { /* no storage */ } writeUrl(false); }
    placeSegs(); window.dispatchEvent(new Event('resize'));
  }
  function refresh() {
    syncFilterBar();
    if (S.view === 'overview') { renderKpis(); renderPanels(); }
    if (S.view === 'risk') { renderLimits(); }
    if (S.view === 'messages') { renderInbox(); }
    (VIEW_GRIDS[S.view] || []).forEach(renderGrid);
    renderCharts(S.view);
    requestAnimationFrame(function () { window.dispatchEvent(new Event('resize')); placeSegs(); });
  }
  var shownView = null, shownKey = null;
  function show() {
    var key = S.view + '|' + S.entity + '|' + S.region + '|' + S.days;
    if (key === shownKey) { if (S.record) { openRecord(S.view, S.record); } else { closeDrawer(true); } return; }
    shownKey = key; shownView = S.view;
    document.querySelectorAll('.app-view').forEach(function (v) { v.hidden = v.getAttribute('data-view') !== S.view; });
    var meta = VIEW_INTRO[S.view];
    UI.ph.querySelector('.eyebrow').textContent = 'Northwind Group · ' + (S.entity === 'all' ? 'all entities' : entName(S.entity)) + ' · as at ' + dLong(DATA.ASAT);
    UI.ph.querySelector('.ph-title').textContent = meta[0];
    document.title = meta[0] + ' — Group CEO view';
    document.querySelectorAll('.sn-link[data-nav]').forEach(function (a) { if (a.getAttribute('data-nav') === S.view) { a.setAttribute('aria-current', 'page'); } else { a.removeAttribute('aria-current'); } });
    var li = UI.crumbs.querySelectorAll('li');
    li[1].querySelector('a').textContent = 'Group'; li[1].querySelector('a').setAttribute('href', '#/overview');
    li[0].querySelector('a').textContent = 'Home'; li[0].querySelector('a').setAttribute('href', '#/overview');
    li[2].querySelector('[aria-current]').textContent = meta[0];
    refresh();
    if (S.record) { if (openRecord(S.view, S.record) === false) { S.record = null; writeUrl(false); } } else { closeDrawer(true); }
  }
  function go(view, record) { S.view = view; S.record = record || null; writeUrl(true); show(); var m = document.getElementById('main'); if (m && !record) { m.closest('.sh-content').scrollTop = 0; } }
  function setFilter(k, v) { S[k] = k === 'days' ? +v : v;
    if (!scopeEnts().length) { var other = k === 'entity' ? 'region' : 'entity'; S[other] = 'all'; toast('That entity sits outside the chosen region, so the ' + other + ' filter was cleared.'); } SAVED.grids = Object.keys(SAVED.grids).reduce(function (o, g) { o[g] = SAVED.grids[g]; o[g].page = 1; return o; }, {}); writeUrl(false); show(); }

  /* ---------- dropdown behaviour (the Dropdown contract: aria-expanded on the trigger, data-open on the menu) ---------- */
  function closeMenus(except) { document.querySelectorAll('.menu[data-open="true"]').forEach(function (mn) { if (mn !== except) { mn.removeAttribute('data-open'); var t = document.querySelector('[aria-controls="' + mn.id + '"]'); if (t) { t.setAttribute('aria-expanded', 'false'); } } }); }
  function pickOption(opt) {
    var menu = opt.closest('.menu'), dd = menu.closest('.dd'), trig = dd.querySelector('.trigger'), v = opt.getAttribute('data-value');
    closeMenus(); trig.focus();
    if (trig.hasAttribute('data-filter')) { setFilter(trig.getAttribute('data-filter'), v); return; }
    setDd(dd, v);
    if (trig.getAttribute('data-setting') === 'start') { SAVED.settings.start = v; save(); toast('The prototype will open on ' + VIEWS.filter(function (x) { return x.id === v; })[0].label + '.'); }
  }

  /* ---------- delegated events ---------- */
  document.addEventListener('click', function (e) {
    var t = e.target, el;
    if ((el = t.closest('.trigger[aria-haspopup="listbox"]'))) {
      var menu = document.getElementById(el.getAttribute('aria-controls')), open = menu.getAttribute('data-open') === 'true';
      closeMenus(menu); if (open) { menu.removeAttribute('data-open'); el.setAttribute('aria-expanded', 'false'); } else { menu.setAttribute('data-open', 'true'); el.setAttribute('aria-expanded', 'true'); var s = menu.querySelector('[aria-selected="true"]') || menu.querySelector('.opt'); if (s) { s.focus(); } }
      return;
    }
    if ((el = t.closest('.menu .opt'))) { pickOption(el); return; }
    if (!t.closest('.menu')) { closeMenus(); }
    if ((el = t.closest('[data-unfilter]'))) { setFilter(el.getAttribute('data-unfilter'), el.getAttribute('data-unfilter') === 'days' ? 30 : 'all'); return; }
    if (t.closest('[data-ftb-clear]')) { S.entity = 'all'; S.region = 'all'; setFilter('days', 30); return; }
    if ((el = t.closest('[data-theme-set]'))) { setTheme(el.getAttribute('data-theme-set'), true); toast((el.getAttribute('data-theme-set') === 'dark' ? 'Dark' : 'Light') + ' theme on.'); return; }
    if ((el = t.closest('.seg button[data-value]'))) { var sg = el.closest('.seg'); sg.querySelectorAll('button').forEach(function (b) { b.setAttribute('aria-pressed', String(b === el)); }); sg.setAttribute('data-value', el.getAttribute('data-value')); moveSeg(sg); return; }
    if ((el = t.closest('[data-action]'))) {
      var a = el.getAttribute('data-action');
      if (a === 'export-view') { exportView(); }
      if (a === 'new-request') { newRequest(); }
      if (a === 'book-deal') { bookDeal(); }
      if (a === 'go-settings') { go('settings'); }
      if (a === 'global-search') { go('accounts'); setTimeout(function () { GRIDS.txns.el.querySelector('[data-grid-search]').focus(); }, 60); }
      if (a === 'reset-state') { confirmBox('Reset saved state?', 'This clears your saved filters, grid settings, decisions, acknowledgements, requests and deals in this browser, then reloads.', 'Reset and reload').then(function (ok) { if (ok) { try { localStorage.removeItem(STORE_KEY); localStorage.removeItem('ceo.theme'); } catch (x) { /* none */ } location.href = location.pathname; } }); }
      return;
    }
    if ((el = t.closest('a[data-pair]'))) { e.preventDefault(); S.pair = el.getAttribute('data-pair'); writeUrl(false); CHARTS['fx-candle'](); FIGURES['fx-candle'].scrollIntoView({ block: 'center' }); toast('Chart shows ' + S.pair + '.'); return; }
    if ((el = t.closest('[data-message]'))) { S.record = el.getAttribute('data-message'); writeUrl(true); messageDrawer(byId(DATA.MESSAGES, S.record)); return; }
    if ((el = t.closest('[data-grid-sort]'))) { var k = el.getAttribute('data-grid-sort'), th = el.closest('th'), g = gstate(k), col = th.getAttribute('data-key'); g.dir = g.sort === col && g.dir === 'ascending' ? 'descending' : 'ascending'; g.sort = col; g.page = 1; save(); renderGrid(k); return; }
    if ((el = t.closest('[data-grid-go]'))) { var gk = el.getAttribute('data-grid'), gs = gstate(gk), go2 = el.getAttribute('data-grid-go'); gs.page = go2 === 'prev' ? gs.page - 1 : go2 === 'next' ? gs.page + 1 : +go2; save(); renderGrid(gk); var cur = GRIDS[gk].el.querySelector('[aria-current="page"]'); if (cur) { cur.focus(); } return; }
    if ((el = t.closest('[data-grid-density]'))) { var dk = el.getAttribute('data-grid-density'); gstate(dk).density = el.getAttribute('data-density'); save(); renderGrid(dk); return; }
    if ((el = t.closest('[data-grid-clear]'))) { var ck = el.getAttribute('data-grid-clear'); gstate(ck).q = ''; gstate(ck).page = 1; save(); renderGrid(ck); GRIDS[ck].el.querySelector('[data-grid-search]').focus(); return; }
    /* chart drill-through: a region bar or a currency slice opens the positions behind it */
    if ((el = t.closest('figure[data-chart] [data-tip]'))) {
      var fig = el.closest('figure'), key = fig.getAttribute('data-chart'), tip = el.getAttribute('data-tip') || '';
      if (key === 'ov-exposure-region' || key === 'rk-region') {
        var reg = DATA.REGIONS.filter(function (r) { return tip.indexOf(r.name) === 0; })[0];
        if (reg) { S.region = S.region === reg.id && key === 'rk-region' ? 'all' : reg.id; if (key === 'ov-exposure-region') { S.view = 'risk'; S.record = null; writeUrl(true); } else { writeUrl(false); } show(); toast(S.region === 'all' ? 'Showing every region.' : 'Showing positions and limits in ' + reg.name + '.'); setTimeout(function () { GRIDS.positions.el.scrollIntoView({ block: 'start' }); }, 80); }
      }
      if (key === 'ov-exposure-ccy') {
        var cc = tip.split(/[\s:·]/)[0];
        if (/^[A-Z]{3}$/.test(cc)) { gstate('positions').q = cc; gstate('positions').page = 1; save(); go('risk'); toast('Showing ' + cc + ' positions.'); setTimeout(function () { GRIDS.positions.el.scrollIntoView({ block: 'start' }); }, 80); }
      }
      return;
    }
    /* chart view switches that change the data: re-render from DATA (dv-behaviour has already flipped aria-pressed) */
    if ((el = t.closest('figure[data-chart] button[data-dv-view-btn]'))) { var fk = el.closest('figure').getAttribute('data-chart'); if (CHARTS[fk] && /ac-balance-entity|ac-netflow|pm-valuedate/.test(fk)) { setTimeout(function () { CHARTS[fk](); }, 0); } return; }
    if ((el = t.closest('a[data-record]'))) { /* hashchange opens it */ return; }
  });
  document.addEventListener('keydown', function (e) {
    var t = e.target;
    if (e.key === 'Escape') { if (document.querySelector('.menu[data-open="true"]')) { var mo = document.querySelector('.menu[data-open="true"]'); closeMenus(); var tr = document.querySelector('[aria-controls="' + mo.id + '"]'); if (tr) { tr.focus(); } return; } if (UI.sheet.classList.contains('open') && !UI.modal.classList.contains('open')) { closeDrawer(); return; } }
    if (t.closest && t.closest('.menu .opt')) {
      var opts = [].slice.call(t.closest('.menu').querySelectorAll('.opt')), i = opts.indexOf(t);
      if (e.key === 'ArrowDown') { e.preventDefault(); (opts[i + 1] || opts[0]).focus(); }
      if (e.key === 'ArrowUp') { e.preventDefault(); (opts[i - 1] || opts[opts.length - 1]).focus(); }
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); pickOption(t); }
      return;
    }
    if ((e.key === 'Enter' || e.key === ' ') && t.matches && t.matches('figure[data-chart] [data-tip][tabindex]')) { e.preventDefault(); t.dispatchEvent(new MouseEvent('click', { bubbles: true })); }
    if (e.key === 'Tab' && UI.sheet.classList.contains('open') && !UI.modal.classList.contains('open')) {
      var f = [].slice.call(UI.sheet.querySelectorAll('button:not([disabled]),input,textarea,a[href],[tabindex="0"]')).filter(function (n) { return n.offsetParent !== null; });
      if (f.length) { if (e.shiftKey && document.activeElement === f[0]) { e.preventDefault(); f[f.length - 1].focus(); } else if (!e.shiftKey && document.activeElement === f[f.length - 1]) { e.preventDefault(); f[0].focus(); } }
    }
  });
  document.addEventListener('input', function (e) {
    var s = e.target.closest('[data-grid-search]'); if (!s) { return; }
    var k = s.getAttribute('data-grid-search'); gstate(k).q = s.value.trim(); gstate(k).page = 1; save(); renderGrid(k);
  });
  document.addEventListener('change', function (e) {
    var sel = e.target.closest('[data-grid-select]');
    if (sel) { var sk = sel.getAttribute('data-grid-select'); if (sel.checked) { GRIDS[sk].sel[sel.value] = 1; } else { delete GRIDS[sk].sel[sel.value]; } renderGrid(sk); var again = document.getElementById(sel.id); if (again) { again.focus(); } return; }
    var sa = e.target.closest('[data-grid-selall]');
    if (sa) { var ak = sa.getAttribute('data-grid-selall'); GRIDS[ak].el.querySelectorAll('[data-grid-select]').forEach(function (i) { if (sa.checked) { GRIDS[ak].sel[i.value] = 1; } else { delete GRIDS[ak].sel[i.value]; } }); renderGrid(ak); document.getElementById(sa.id).focus(); return; }
    var p = e.target.closest('[data-grid-pp]'); if (p) { var k = p.getAttribute('data-grid-pp'); gstate(k).pp = +p.value; gstate(k).page = 1; save(); renderGrid(k); return; }
    var sw = e.target.closest('input[role="switch"][data-setting]'); if (sw) { SAVED.settings[sw.getAttribute('data-setting')] = sw.checked; save(); toast(sw.checked ? 'Notification on.' : 'Notification off.'); }
  });
  UI.scrim.addEventListener('click', function () { closeDrawer(); });
  UI.sheet.querySelector('.sheet-head .close').addEventListener('click', function () { closeDrawer(); });
  window.addEventListener('popstate', function () { readUrl(); show(); });
  window.addEventListener('hashchange', function () { readUrl(); show(); });

  /* ---------- shell: nav rail toggle and the off-canvas menu (App-shell-side-nav's contract) ---------- */
  (function () {
    var shell = UI.shell, col = shell.querySelector('.sh-body > .sn'), btn = shell.querySelector('[data-navtoggle]');
    function rail(on) { col.classList.toggle('is-rail', on); shell.setAttribute('data-nav', on ? 'rail' : 'expanded'); btn.setAttribute('aria-expanded', String(!on)); btn.setAttribute('aria-label', on ? 'Expand navigation' : 'Collapse navigation'); col.setAttribute('aria-label', on ? 'Main, collapsed' : 'Main'); var u = btn.querySelector('use'); if (u) { u.setAttribute('href', on ? '#ic-chevron-right' : '#ic-chevron-left'); } }
    if (SAVED.rail) { rail(true); }
    btn.addEventListener('click', function () { var on = !col.classList.contains('is-rail'); rail(on); SAVED.rail = on; save(); setTimeout(function () { window.dispatchEvent(new Event('resize')); }, 250); });
    var mbtn = shell.querySelector('[data-menu]'), sheet = shell.querySelector('.sh-sheet'), scrim = shell.querySelector('[data-scrim]'), close = shell.querySelector('[data-close]');
    function open() { mbtn.setAttribute('aria-expanded', 'true'); scrim.classList.add('open'); sheet.classList.add('open'); requestAnimationFrame(function () { requestAnimationFrame(function () { var f = sheet.querySelector('a,button'); if (f) { f.focus(); } }); }); }
    function shut() { mbtn.setAttribute('aria-expanded', 'false'); scrim.classList.remove('open'); sheet.classList.remove('open'); mbtn.focus(); }
    mbtn.addEventListener('click', open); close.addEventListener('click', shut); scrim.addEventListener('click', shut);
    sheet.addEventListener('click', function (e) { if (e.target.closest('a[data-nav]')) { shut(); } });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && sheet.classList.contains('open')) { shut(); } });
  }());

  /* ---------- start ---------- */
  (function () {
    var fxv = document.querySelector('.app-view[data-view="fx"]'), recs = fxv.querySelectorAll('.app-records')[1];
    var b = T('t-btn'); b.textContent = 'Book an FX deal'; b.setAttribute('type', 'button'); b.setAttribute('data-action', 'book-deal');
    var row = document.createElement('div'); row.className = 'l-row'; row.setAttribute('data-justify', 'end'); row.appendChild(wrap('cn-button', b)); recs.insertBefore(row, recs.firstChild);
    ['ac-netflow'].forEach(function (k) { var bs = FIGURES[k].querySelectorAll('button[data-dv-view-btn]'); if (bs[0]) { bs[0].textContent = 'Daily'; } if (bs[1]) { bs[1].textContent = 'Cumulative'; } });
    document.querySelectorAll('input[role="switch"][data-setting]').forEach(function (sw) { var v = SAVED.settings[sw.getAttribute('data-setting')]; sw.checked = v == null ? sw.getAttribute('data-setting') !== 'notifyMessages' : v; });
    if (SAVED.settings.start) { setDd(UI.startDd, SAVED.settings.start); }
  }());
  readUrl();
  setTheme(document.documentElement.getAttribute('data-theme') || 'light', false);
  writeUrl(false);
  show();
  if (document.fonts && document.fonts.ready) { document.fonts.ready.then(function () { placeSegs(); window.dispatchEvent(new Event('resize')); }); }
}());
