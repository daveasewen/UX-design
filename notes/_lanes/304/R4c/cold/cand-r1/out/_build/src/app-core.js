/* CEO APP — CORE. Authored wiring (ADS-generate-from-canon rule 2a, s258-D1): state, persistence,
   formatting, and the builders that CLONE each component from its spliced <template> (the
   verbatim snippet bytes) and fill it from CEO_DATA. No component markup is typed here except the
   minimal structural wrappers named in the run report. */
(function () {
  'use strict';
  var D = window.CEO_DATA, APP = window.CEO_APP = {};
  var LS = 'ceo-proto-v1';
  var MON = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

  /* ------------------------------------------------------------------ state + persistence */
  var DEFAULT = { view: 'overview', q: '', filters: [], days: 30, theme: 'light', recView: 'table', density: 'full',
    sort: {}, page: {}, tabs: {}, wf: { pay: {}, exc: {}, msg: {}, srNew: [], srUpd: {}, rep: [] },
    prefs: { notify: { approvals: true, breaches: true, messages: true, digest: false }, defaultView: 'overview' } };
  function clone(o) { return JSON.parse(JSON.stringify(o)); }
  function merge(a, b) { Object.keys(b || {}).forEach(function (k) {
    if (b[k] && typeof b[k] === 'object' && !Array.isArray(b[k]) && a[k] && typeof a[k] === 'object') { merge(a[k], b[k]); } else { a[k] = b[k]; } }); return a; }
  function load() { try { var s = JSON.parse(localStorage.getItem(LS) || 'null'); return merge(clone(DEFAULT), s || {}); } catch (e) { return clone(DEFAULT); } }
  APP.state = load();
  APP.DEFAULT = DEFAULT;
  APP.save = function () {
    try { localStorage.setItem(LS, JSON.stringify(APP.state)); } catch (e) { /* private window: state lives for this visit only */ }
    APP.writeURL();
  };
  APP.writeURL = function () {
    var s = APP.state, p = new URLSearchParams();
    p.set('view', s.view);
    if (s.q) { p.set('q', s.q); }
    if (s.filters.length) { p.set('f', s.filters.map(function (f) { return f.facet + ':' + f.value; }).join(',')); }
    if (s.days !== 30) { p.set('days', String(s.days)); }
    if (s.theme !== 'light') { p.set('theme', s.theme); }
    try { history.replaceState(null, '', location.pathname + '?' + p.toString() + location.hash); } catch (e) { /* file: URLs in some browsers */ }
  };
  APP.readURL = function () {
    var p = new URLSearchParams(location.search), s = APP.state;
    if (p.get('view')) { s.view = p.get('view'); }
    if (p.has('q')) { s.q = p.get('q'); }
    if (p.get('f')) { s.filters = p.get('f').split(',').map(function (x) { var i = x.indexOf(':'); return { facet: x.slice(0, i), value: x.slice(i + 1) }; })
      .filter(function (f) { return f.facet && f.value; }); }
    if (p.get('days')) { var d = +p.get('days'); if ([7, 30, 90].indexOf(d) >= 0) { s.days = d; } }
    if (p.get('theme') === 'dark' || p.get('theme') === 'light') { s.theme = p.get('theme'); }
  };

  /* ------------------------------------------------------------------ formatting */
  var SYM = { GBP: '£', USD: '$', EUR: '€' };
  function num(n, dp) { return Number(n).toLocaleString('en-GB', { minimumFractionDigits: dp || 0, maximumFractionDigits: dp || 0 }); }
  APP.num = num;
  APP.gbpc = function (n) { var a = Math.abs(n), s = n < 0 ? '−' : '';
    if (a >= 1e9) { return s + '£' + (a / 1e9).toFixed(2) + 'bn'; } if (a >= 1e6) { return s + '£' + (a / 1e6).toFixed(1) + 'm'; }
    if (a >= 1e3) { return s + '£' + (a / 1e3).toFixed(1) + 'k'; } return s + '£' + a.toFixed(0); };
  APP.money = function (ccy, n) { var s = n < 0 ? '−' : ''; return s + (SYM[ccy] || ccy + ' ') + num(Math.abs(n), 2); };
  APP.mc = function (ccy, n) { var a = Math.abs(n), s = n < 0 ? '−' : '', p = SYM[ccy] || ccy + ' ';
    return s + p + (a >= 1e9 ? (a / 1e9).toFixed(2) + 'bn' : a >= 1e6 ? (a / 1e6).toFixed(1) + 'm' : a >= 1e3 ? (a / 1e3).toFixed(1) + 'k' : a.toFixed(0)); };
  APP.m = function (n) { return Math.round(n / 1e5) / 10; };           /* £ → £m, one decimal, for chart specs */
  APP.date = function (iso) { if (!iso) { return '—'; } var p = iso.split('-'); return +p[2] + ' ' + MON[+p[1] - 1] + ' ' + p[0]; };
  APP.dshort = function (iso) { var p = iso.split('-'); return +p[2] + ' ' + MON[+p[1] - 1]; };
  APP.now = function () { var d = new Date(); return d.toISOString().slice(0, 16).replace('T', ' '); };
  APP.ent = function (id) { for (var i = 0; i < D.entities.length; i++) { if (D.entities[i].id === id) { return D.entities[i]; } } return { short: id, name: id }; };
  APP.regionName = function (id) { for (var i = 0; i < D.regions.length; i++) { if (D.regions[i].id === id) { return D.regions[i].name; } } return id || '—'; };
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  APP.esc = esc;

  /* ------------------------------------------------------------------ the shared filters */
  APP.facets = function () { var f = { entity: [], region: [], currency: [] };
    APP.state.filters.forEach(function (x) { if (f[x.facet]) { f[x.facet].push(x.value); } }); return f; };
  APP.pass = function (r) { var f = APP.facets();
    if (f.entity.length && r.entity && f.entity.indexOf(r.entity) < 0) { return false; }
    if (f.region.length && r.region && f.region.indexOf(r.region) < 0) { return false; }
    if (f.currency.length && r.ccy && f.currency.indexOf(r.ccy) < 0) { return false; }
    return true; };
  APP.startDate = function () { return D.dates[D.dates.length - APP.state.days]; };
  APP.inRange = function (iso) { return !iso || iso >= APP.startDate(); };
  APP.matchQ = function (r, fields) { var q = (APP.state.q || '').trim().toLowerCase(); if (!q) { return true; }
    return fields.some(function (k) { return r[k] != null && String(r[k]).toLowerCase().indexOf(q) >= 0; }); };
  /* entities in view: the entity + region facets, and the currency facet read against each entity's base currency */
  APP.entitiesInView = function () { return D.entities.filter(function (e) { return APP.pass({ entity: e.id, region: e.region, ccy: e.ccy }); }); };
  APP.series = function (key, entities) { var es = entities || APP.entitiesInView(), n = APP.state.days, out = [];
    for (var i = D.dates.length - n; i < D.dates.length; i++) { var s = 0; es.forEach(function (e) { s += D.daily[e.id][key][i]; }); out.push(s); }
    return out; };
  APP.rangeDates = function () { return D.dates.slice(D.dates.length - APP.state.days); };
  APP.rangeLabel = function () { return 'last ' + APP.state.days + ' days to ' + APP.date(D.asAt); };

  /* ------------------------------------------------------------------ templates */
  var uid = 0;
  APP.tpl = function (key) { var t = document.getElementById('T-' + key); if (!t) { throw new Error('no template ' + key); }
    var el = t.content.firstElementChild; return el.cloneNode(true); };
  /* Every cloned id is prefixed and every in-component reference follows it, so repeated clones never collide. */
  APP.reid = function (root) {
    var pre = 'u' + (++uid) + '-', map = {}, all = [root].concat([].slice.call(root.querySelectorAll('[id]')));
    all.forEach(function (el) { if (el.id) { map[el.id] = pre + el.id; el.id = pre + el.id; } });
    ['aria-labelledby', 'aria-controls', 'aria-describedby', 'data-for', 'for', 'data-lockup-table'].forEach(function (a) {
      [root].concat([].slice.call(root.querySelectorAll('[' + a + ']'))).forEach(function (el) {
        var v = el.getAttribute(a); if (!v) { return; }
        el.setAttribute(a, v.split(/\s+/).map(function (t) { return map[t] || t; }).join(' '));
      });
    });
    return pre;
  };
  APP.scope = function (cls, child, tag) { var w = document.createElement(tag || 'div'); w.className = cls; if (child) { w.appendChild(child); } return w; };
  APP.el = function (tag, cls, text) { var e = document.createElement(tag); if (cls) { e.className = cls; } if (text != null) { e.textContent = text; } return e; };

  /* ------------------------------------------------------------------ status indicator */
  /* Status-indicator: the TINT CHIP everywhere, the FILLED CELL inside a table (the snippet's own dense-table
     form). Neutral has no chip or fill (the snippet names that token gap) — it takes the inline dot form with
     the reference's own margin:0, exactly as the specimen does. */
  var STAT_KIND = { ok: 'ok', warn: 'warn', err: 'err', inf: 'inf' };
  APP.statForm = 'chip';
  APP.stat = function (kind, label) {
    var k = STAT_KIND[kind], el;
    if (APP.statForm === 'cell' && k) { el = APP.tpl('statcell').querySelector('.cell').cloneNode(true); el.className = 'cell ' + k; el.textContent = label; }
    else if (k) { el = APP.tpl('statchips').querySelector('.chip').cloneNode(true); el.className = 'chip ' + k; el.lastChild.textContent = label; }
    else { el = APP.tpl('statchips').querySelector('.stat.neu').cloneNode(true); el.lastElementChild.textContent = label; }
    return APP.scope('cn-status-indicator', el, 'span');
  };
  APP.statusKind = function (status) {
    return ({ 'Awaiting your approval': 'warn', 'Awaiting second approver': 'inf', 'Approved': 'ok', 'Released': 'ok', 'Scheduled': 'inf',
      'Rejected': 'err', 'Open': 'warn', 'Acknowledged': 'ok', 'Closed': 'neu', 'Within': 'ok', 'Approaching': 'warn', 'Breach': 'err',
      'Issued': 'ok', 'Documents presented': 'inf', 'Amendment requested': 'warn', 'Discrepant documents': 'err', 'Paid': 'neu',
      'Confirmed': 'ok', 'Settled': 'neu', 'Awaiting confirmation': 'warn', 'Submitted': 'inf', 'In progress': 'inf',
      'Awaiting your information': 'warn', 'Resolved': 'ok', 'Ready': 'ok', 'Unread': 'warn', 'Read': 'neu', 'Active': 'ok' })[status] || 'neu';
  };

  /* ------------------------------------------------------------------ toast */
  var toastRegion = null;
  APP.toast = function (kind, msg) {
    if (!toastRegion) { toastRegion = APP.tpl('toastregion'); document.body.appendChild(APP.scope('cn-toast', toastRegion)); }
    var t = APP.tpl('toast'); t.className = 'toast ' + (kind || 'ok');
    var use = t.querySelector('.ic use'); if (use) { use.setAttribute('href', { ok: '#to-success', info: '#to-info', warn: '#to-warning' }[kind] || '#to-success'); }
    t.querySelector('.msg').textContent = msg;
    toastRegion.appendChild(t);
    var remain = 6000, started = Date.now(), paused = false, timer = setTimeout(leave, remain);
    function leave() { if (t.parentNode) { t.remove(); } }
    function pause() { if (paused) { return; } paused = true; clearTimeout(timer); remain -= Date.now() - started; }
    function resume() { if (!paused) { return; } paused = false; started = Date.now(); timer = setTimeout(leave, Math.max(remain, 1000)); }
    t.addEventListener('mouseenter', pause); t.addEventListener('mouseleave', resume);
    t.addEventListener('focusin', pause); t.addEventListener('focusout', resume);
    var x = t.querySelector('.x'); if (x) { x.addEventListener('click', function () { clearTimeout(timer); leave(); }); }
  };

  /* ------------------------------------------------------------------ summary + timeline */
  APP.summary = function (pairs) {
    var dl = APP.tpl('summary'), row = dl.querySelector('.summary__row'); dl.textContent = '';
    pairs.forEach(function (p) { var r = row.cloneNode(true); r.querySelector('.summary__k').textContent = p[0];
      var v = r.querySelector('.summary__v'); v.textContent = ''; if (p[1] && p[1].nodeType) { v.appendChild(p[1]); } else { v.textContent = p[1] == null ? '—' : p[1]; }
      dl.appendChild(r); });
    return APP.scope('cn-summary', dl);
  };
  APP.timeline = function (title, entries) {
    var tl = APP.tpl('timeline'); APP.reid(tl);
    var h = tl.querySelector('h2'); if (h) { h.textContent = title; }
    var grp = tl.querySelector('.tl-group'), li = grp.querySelector('.tl-list li');
    [].slice.call(tl.querySelectorAll('.tl-group')).forEach(function (g) { g.remove(); });
    var byDay = {};
    entries.slice().sort(function (a, b) { return a.when < b.when ? 1 : -1; }).forEach(function (e) { var d = e.when.slice(0, 10); (byDay[d] = byDay[d] || []).push(e); });
    Object.keys(byDay).sort().reverse().forEach(function (d) {
      var g = grp.cloneNode(true), ol = g.querySelector('.tl-list'); g.querySelector('h3').textContent = APP.date(d); ol.textContent = '';
      byDay[d].forEach(function (e) { var it = li.cloneNode(true); it.className = e.tone || 'ok';
        it.querySelector('.tl-title').textContent = e.text;
        var amt = it.querySelector('.tl-amount'); if (amt) { amt.textContent = e.amount || ''; }
        var tm = it.querySelector('time'); if (tm) { tm.setAttribute('datetime', e.when.replace(' ', 'T')); tm.textContent = e.when.length > 10 ? e.when.slice(11, 16) : ''; }
        var st = it.querySelector('.status'); if (st) { st.className = 'status ' + (e.tone || 'ok') + ' t-cm-legal'; st.lastChild.textContent = e.who || 'System'; }
        var ds = it.querySelector('.tl-desc'); if (ds) { if (e.note) { ds.textContent = e.note; } else { ds.remove(); } }
        ol.appendChild(it); });
      tl.appendChild(g);
    });
    return APP.scope('cn-timeline', tl);
  };

  /* ------------------------------------------------------------------ empty state */
  APP.empty = function (title, text, action) {
    var e = APP.tpl('empty'); APP.reid(e);
    e.querySelector('h3').textContent = title; e.querySelector('p').textContent = text;
    var b = e.querySelector('.ebtn');
    if (action) { b.textContent = action.label; b.addEventListener('click', action.onClick); } else { if (b) { b.remove(); } var gap = e.querySelector('.gap'); if (gap) { gap.remove(); } }
    return APP.scope('cn-empty-state', e);
  };

  /* ------------------------------------------------------------------ buttons (the page-header / modal / drawer own theirs) */
  APP.button = function (label, kind, onClick) {
    var row = APP.tpl('btnrow'), b = row.querySelector('.btn.' + (kind || 'secondary')) || row.querySelector('.btn');
    b = b.cloneNode(true); b.textContent = label; b.type = 'button'; b.className = 'btn ' + (kind || 'secondary');
    if (onClick) { b.addEventListener('click', onClick); }
    return APP.scope('cn-button', b, 'span');
  };

  /* ------------------------------------------------------------------ segmented control */
  APP.seg = function (label, options, value, onChange) {
    var seg = APP.tpl('seg'), ind = seg.querySelector('.ind'), proto = seg.querySelector('button');
    seg.setAttribute('aria-label', label); [].slice.call(seg.querySelectorAll('button')).forEach(function (b) { b.remove(); });
    options.forEach(function (o) { var b = proto.cloneNode(true); b.textContent = o[1]; b.setAttribute('data-value', o[0]);
      b.setAttribute('aria-pressed', String(o[0] === value)); seg.appendChild(b); });
    seg.addEventListener('click', function (e) { var b = e.target.closest('button'); if (!b) { return; }
      [].slice.call(seg.querySelectorAll('button')).forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); });
      if (typeof moveInd === 'function') { moveInd(seg); }
      onChange(b.getAttribute('data-value')); });
    var w = APP.scope('cn-segmented-control', seg);
    requestAnimationFrame(function () { if (typeof moveInd === 'function') { moveInd(seg); } });
    void ind; return w;
  };
  APP.segSet = function (wrap, value) { var seg = wrap.querySelector('.seg');
    [].slice.call(seg.querySelectorAll('button')).forEach(function (x) { x.setAttribute('aria-pressed', String(x.getAttribute('data-value') === value)); });
    if (typeof moveInd === 'function') { moveInd(seg); } };

  /* ------------------------------------------------------------------ dropdown (boxed) — wired by the pack's wireDD */
  APP.dropdown = function (label, options, value, onChoose) {
    var dd = APP.tpl('dd'); APP.reid(dd);
    var lab = dd.querySelector('label'), menu = dd.querySelector('.menu'), opt = menu.querySelector('.opt'), val = dd.querySelector('.ddval');
    lab.textContent = label; menu.textContent = '';
    options.forEach(function (o) { var li = opt.cloneNode(true); li.firstChild.textContent = o[1] + ' '; li.setAttribute('data-value', o[0]);
      li.setAttribute('aria-selected', String(o[0] === value)); menu.appendChild(li); if (o[0] === value) { val.textContent = o[1]; } });
    if (typeof wireDD === 'function') { wireDD(dd, function (o) { onChoose(o.getAttribute('data-value')); return true; }); }
    return APP.scope('cn-dropdown', dd);
  };

  /* ------------------------------------------------------------------ KPI tile */
  APP.kpi = function (slot, o) {
    var t = APP.tpl('kpi');
    t.classList.add('c-bento__tile'); t.setAttribute('data-c', slot.getAttribute('data-c') || '1'); t.id = slot.id;
    var a = t.querySelector('.kpi-link'); a.textContent = o.label; a.setAttribute('href', '?view=' + o.go); a.setAttribute('data-go', o.go);
    var v = t.querySelector('.kpi-val'), spans = v.querySelectorAll('span');
    spans[0].textContent = o.unit || ''; spans[1].textContent = o.value;
    var dl = t.querySelector('.kpi-delta'), dir = o.delta > 0.05 ? 'up' : o.delta < -0.05 ? 'down' : 'flat';
    dl.className = 'kpi-delta ' + dir;
    dl.querySelector('use').setAttribute('href', '#kpi-' + dir);
    dl.querySelector('.t-cm-figure-6').textContent = dir === 'flat' ? 'No change' : (o.delta > 0 ? '+' : '−') + (Math.abs(o.delta) >= 1000 ? '999+' : Math.abs(o.delta).toFixed(1)) + '% ' + dir;
    dl.querySelector('.kpi-per').textContent = o.per;
    var svg = t.querySelector('svg.spark-inline'), s = o.series, lo = Math.min.apply(null, s), hi = Math.max.apply(null, s), span = hi - lo || 1;
    var pts = s.map(function (x, i) { return (3 + i * 194 / (s.length - 1)).toFixed(1) + ',' + (45 - (x - lo) / span * 42).toFixed(1); });
    svg.setAttribute('data-trend', dir);
    svg.querySelector('polyline').setAttribute('points', pts.join(' '));
    svg.querySelector('polygon').setAttribute('points', pts.join(' ') + ' 197.0,45 3.0,45');
    t.setAttribute('aria-label', o.label + ', ' + (o.unit || '') + o.value + ', ' + dl.querySelector('.t-cm-figure-6').textContent + ' ' + o.per);
    slot.parentNode.replaceChild(t, slot);
    return t;
  };

  /* ------------------------------------------------------------------ charts — dvRender owns the arithmetic */
  var CH = { column: ['ch-column', 'cn-chart-bar'], bar: ['ch-hbar', 'cn-chart-bar'], 'grouped-column': ['ch-grouped', 'cn-chart-bar'],
    'stacked-column': ['ch-stacked', 'cn-chart-bar'], line: ['ch-line', 'cn-chart-line'], multiline: ['ch-multiline', 'cn-chart-line'],
    'stacked-area': ['ch-area', 'cn-chart-stacked-area'], donut: ['ch-donut', 'cn-chart-donut'], pie: ['ch-pie', 'cn-chart-pie'],
    combo: ['ch-combo', 'cn-chart-combo'], candlestick: ['ch-candle', 'cn-chart-candlestick'], bullet: ['ch-bullet', 'cn-chart-bullet'],
    'butterfly-h': ['ch-butterfly', 'cn-chart-butterfly-h'], scatter: ['ch-scatter', 'cn-chart-scatter'], histogram: ['ch-hist', 'cn-chart-histogram'],
    boxplot: ['ch-box', 'cn-chart-boxplot'], spark: ['ch-spark', 'cn-chart-sparkline'] };
  APP.chartErrors = [];
  function legendFor(fig, spec, names) {
    var old = fig.querySelector('ul.dv-leg'); if (!old) { return; }
    var live = fig.querySelector('p.dv-sr');
    if (!names || names.length < 2) { old.remove(); if (live) { live.remove(); } return; }
    var fresh = old.cloneNode(true), rows = [].slice.call(fresh.querySelectorAll('.dv-legrow'));
    var anchor = rows[rows.length - 1].nextSibling;
    rows.forEach(function (r) { r.remove(); });
    names.forEach(function (n, i) {
      /* row i keeps the specimen's own swatch for position i (butterfly keys series 1 and 3, lines cycle shapes) */
      var src = rows[i] || rows[rows.length - 1], r = src.cloneNode(true), sw = r.querySelector('.dv-leg-sw'), b = r.querySelector('.dv-leg-item');
      r.setAttribute('data-series', String(i + 1));
      if (!rows[i]) { sw.setAttribute('style', '--sc:var(--data-series-' + ((i % 5) + 1) + ')'); }
      sw.setAttribute('aria-label', 'Show or hide ' + n); sw.setAttribute('aria-checked', 'true');
      b.setAttribute('data-series', String(i + 1)); b.setAttribute('aria-label', 'Isolate ' + n); b.setAttribute('aria-pressed', 'false');
      var key = b.querySelector('.dv-key'); if (key) { key.textContent = String.fromCharCode(65 + i); }
      b.querySelector('.dv-leg-name').textContent = n;
      fresh.insertBefore(r, anchor);
    });
    var rb = fresh.querySelector('.dv-leg-reset'); if (rb) { rb.disabled = true; }
    old.parentNode.replaceChild(fresh, old);
    if (live) { live.textContent = ''; }
  }
  /* o: { title, spec, legend: [names] | undefined, drill: fn(catIndex), sortable, domainMax } */
  APP.chart = function (tile, o) {
    var type = o.spec.type, def = CH[type];
    var fig = tile.querySelector('figure.dv');
    if (!fig || fig.getAttribute('data-ceo-type') !== type) {
      tile.textContent = ''; tile.className = tile.className.replace(/\bcn-chart-[a-z-]+/g, '').trim();
      tile.classList.add(def[1]);
      fig = APP.tpl(def[0]); APP.reid(fig); fig.setAttribute('data-ceo-type', type);
      fig.setAttribute('data-dv-type', type);
      /* the specimen's own data-driven view toggles (monthly/YTD, target/ghost overlays) belong to its data, not ours */
      if (!o.sortable) { [].slice.call(fig.querySelectorAll('.dv-controls .seg')).forEach(function (s) { if (s.querySelector('[data-dv-view-btn="discrete"],[data-dv-view-btn="orig"]')) { s.remove(); } }); }
      [].slice.call(fig.querySelectorAll('.dv-controls .dv-toggle-seg')).forEach(function (s) {
        var b = s.querySelector('[data-dv-toggle]'); if (!(o.spec.target != null && b && b.getAttribute('data-dv-toggle') === 'target')) { s.remove(); } });
      fig.removeAttribute('data-total');
      /* dv-behaviour lands .dv-fit-on on the figures present at ITS init; a figure born later opts in the same way */
      fig.classList.add('dv-fit-on');
      tile.appendChild(fig);
      if (o.drill) {
        tile.addEventListener('click', function (e) {
          var m = e.target.closest('.dv-series');
          if (!m && e.target.closest('svg.dv-svg')) {   /* a letter key or label drawn over a mark: hit-test the marks under the pointer */
            [].slice.call(fig.querySelectorAll('.dv-series')).some(function (x) { var b = x.getBoundingClientRect();
              if (e.clientX >= b.left && e.clientX <= b.right && e.clientY >= b.top && e.clientY <= b.bottom) { m = x; return true; } return false; }); }
          if (m && fig.contains(m)) { drill(m); } });
        tile.addEventListener('keydown', function (e) { if (e.key !== 'Enter') { return; } var m = e.target.closest('.dv-series'); if (m) { e.preventDefault(); drill(m); } });
      }
    }
    function drill(mark) {
      var lab = mark.getAttribute('aria-label') || mark.getAttribute('data-tip') || '', cats = fig.__dvSpec ? fig.__dvSpec.categories : [];
      for (var i = 0; i < cats.length; i++) { if (lab.indexOf(cats[i]) === 0 || lab.indexOf(', ' + cats[i]) > 0 || lab.indexOf(cats[i] + ',') >= 0) { return fig.__ceoDrill(i); } }
    }
    fig.__ceoDrill = o.drill || null;
    if (o.domainMax != null) { fig.setAttribute('data-domain-max', String(o.domainMax)); }
    var h = fig.querySelector('.dv-title');
    if (h) { h.textContent = o.title; fig.setAttribute('data-lockup-title', o.title); }
    else { /* the sparkline is an atom with no title slot (s182-D2): the tile names it, above the figure */
      var th = tile.querySelector('h3.t-cm-section-label'); if (!th) { th = APP.el('h3', 't-cm-section-label'); tile.insertBefore(th, fig); } th.textContent = o.title; }
    var cap = fig.querySelector('figcaption'); cap.textContent = o.spec.caption || o.title;
    legendFor(fig, o.spec, o.legend);
    try { window.dvRender(fig, o.spec); fig.removeAttribute('data-ceo-error'); }
    catch (err) { APP.chartErrors.push(type + ': ' + err.message); fig.setAttribute('data-ceo-error', err.message); }
    return fig;
  };

  /* ------------------------------------------------------------------ drawer (one surface at a time) */
  var drawer = null;
  function focusables(el) { return [].slice.call(el.querySelectorAll('button,[href],input,textarea,select,[tabindex]:not([tabindex="-1"])')).filter(function (x) { return !x.disabled && x.offsetParent !== null; }); }
  APP.drawer = {
    open: function (o) {
      APP.modal.close(true);
      if (!drawer) {
        var scrim = APP.tpl('scrim'), sheet = APP.tpl('sheet'); scrim.id = 'ceo-scrim'; sheet.id = 'ceo-sheet';
        var w = APP.scope('cn-drawer'); w.appendChild(scrim); w.appendChild(sheet); document.body.appendChild(w);
        sheet.querySelector('h3').id = 'ceo-sheet-title'; sheet.setAttribute('aria-labelledby', 'ceo-sheet-title');
        sheet.querySelector('.sheet-body').id = 'ceo-sheet-body'; sheet.setAttribute('aria-describedby', 'ceo-sheet-body');
        sheet.querySelector('.close').removeAttribute('id');
        drawer = { scrim: scrim, sheet: sheet, proto: sheet.querySelector('.dbtn.primary').cloneNode(true), proto2: sheet.querySelector('.dbtn.secondary').cloneNode(true) };
        sheet.querySelector('.close').addEventListener('click', function () { APP.drawer.close(); });
        scrim.addEventListener('click', function () {
          /* Drawer anti-pattern: a scrim click must not throw away typed input. Keep the sheet and say so. */
          if (drawer.dirty && drawer.dirty()) { APP.toast('info', 'You have unsent text — use Cancel or Close to discard it.'); var t = document.getElementById('t1'); if (t) { t.focus(); } return; }
          APP.drawer.close(); });
        document.addEventListener('keydown', function (e) {
          if (!sheet.classList.contains('open')) { return; }
          if (e.key === 'Escape') { APP.drawer.close(); return; }
          if (e.key === 'Tab') { var f = focusables(sheet), a = f[0], z = f[f.length - 1];
            if (e.shiftKey && document.activeElement === a) { e.preventDefault(); z.focus(); } else if (!e.shiftKey && document.activeElement === z) { e.preventDefault(); a.focus(); } }
        });
      }
      if (!drawer.sheet.contains(document.activeElement) && !(document.getElementById('ceo-overlay') && document.getElementById('ceo-overlay').contains(document.activeElement))) { drawer.opener = document.activeElement; }
      drawer.dirty = o.dirty || null; drawer.onClose = o.onClose || null;
      drawer.sheet.querySelector('h3').textContent = o.title;
      var body = drawer.sheet.querySelector('.sheet-body'); body.textContent = '';
      (o.body || []).forEach(function (n) { if (n) { body.appendChild(n); } });
      var foot = drawer.sheet.querySelector('.sheet-foot'); foot.textContent = '';
      (o.actions || []).forEach(function (a, i) { var b = (i === 0 && a.kind !== 'secondary' ? drawer.proto : drawer.proto2).cloneNode(true);
        b.removeAttribute('id'); b.textContent = a.label; if (a.disabled) { b.disabled = true; b.title = a.disabled; }
        b.addEventListener('click', a.onClick); foot.appendChild(b); });
      if (!o.actions || !o.actions.length) { var c = drawer.proto2.cloneNode(true); c.removeAttribute('id'); c.textContent = 'Close'; c.addEventListener('click', function () { APP.drawer.close(); }); foot.appendChild(c); }
      drawer.scrim.classList.add('open'); drawer.sheet.classList.add('open');
      requestAnimationFrame(function () { requestAnimationFrame(function () { var f = focusables(drawer.sheet); if (f.length) { (o.focus ? drawer.sheet.querySelector(o.focus) || f[0] : f[0]).focus(); }
        var root = document.getElementById('ceo-root'); root.inert = true; root.setAttribute('aria-hidden', 'true'); }); });
    },
    close: function (silent) {
      if (!drawer || !drawer.sheet.classList.contains('open')) { return; }
      drawer.scrim.classList.remove('open'); drawer.sheet.classList.remove('open');
      var root = document.getElementById('ceo-root'); root.inert = false; root.removeAttribute('aria-hidden');
      APP.park();
      if (drawer.onClose) { drawer.onClose(); }
      if (!silent && drawer.opener && document.body.contains(drawer.opener)) { drawer.opener.focus(); }
    },
    isOpen: function () { return !!(drawer && drawer.sheet.classList.contains('open')); },
    opener: function () { return drawer ? drawer.opener : null; }
  };

  /* ------------------------------------------------------------------ modal (a blocking decision) */
  var modal = null;
  APP.modal = {
    open: function (o) {
      var from = APP.drawer.isOpen() ? APP.drawer.opener() : document.activeElement;
      APP.drawer.close(true);
      if (!modal) {
        var ov = APP.tpl('modal'); ov.id = 'ceo-overlay'; document.body.appendChild(APP.scope('cn-modals', ov));
        var dlg = ov.querySelector('.dialog'); dlg.querySelector('h2').id = 'ceo-dlg-title'; dlg.querySelector('p').id = 'ceo-dlg-body';
        dlg.setAttribute('aria-labelledby', 'ceo-dlg-title'); dlg.setAttribute('aria-describedby', 'ceo-dlg-body');
        ['close', 'confirm', 'cancel'].forEach(function (k) { var b = dlg.querySelector('#' + k); if (b) { b.removeAttribute('id'); b.setAttribute('data-role', k); } });
        var slot = document.createElement('div'); slot.className = 'ceo-stack'; slot.id = 'ceo-dlg-slot'; dlg.insertBefore(slot, dlg.querySelector('.actions'));
        modal = { ov: ov, dlg: dlg, slot: slot };
        dlg.querySelector('[data-role="close"]').addEventListener('click', function () { APP.modal.close(); });
        dlg.querySelector('[data-role="cancel"]').addEventListener('click', function () { APP.modal.close(); });
        dlg.querySelector('[data-role="confirm"]').addEventListener('click', function () { if (modal.onConfirm && modal.onConfirm() === false) { return; } APP.modal.close(); });
        ov.addEventListener('click', function (e) { if (e.target === ov) { APP.modal.close(); } });
        document.addEventListener('keydown', function (e) {
          if (!ov.classList.contains('open')) { return; }
          if (e.key === 'Escape') { APP.modal.close(); return; }
          if (e.key === 'Tab') { var f = focusables(dlg), a = f[0], z = f[f.length - 1];
            if (e.shiftKey && document.activeElement === a) { e.preventDefault(); z.focus(); } else if (!e.shiftKey && document.activeElement === z) { e.preventDefault(); a.focus(); } }
        });
      }
      modal.opener = o.opener || from; modal.onConfirm = o.onConfirm;
      modal.dlg.querySelector('h2').textContent = o.title; modal.dlg.querySelector('p').textContent = o.text;
      modal.slot.textContent = ''; (o.body || []).forEach(function (n) { if (n) { modal.slot.appendChild(n); } });
      var c = modal.dlg.querySelector('[data-role="confirm"]'); c.textContent = o.confirmLabel || 'Confirm';
      modal.dlg.querySelector('[data-role="cancel"]').textContent = o.cancelLabel || 'Cancel';
      var root = document.getElementById('ceo-root'); root.inert = true; root.setAttribute('aria-hidden', 'true');
      requestAnimationFrame(function () { requestAnimationFrame(function () { modal.ov.classList.add('open');
        setTimeout(function () { var f = o.focus ? modal.dlg.querySelector(o.focus) : null; (f || focusables(modal.dlg)[0]).focus(); }, 60); }); });
    },
    close: function (silent) {
      if (!modal || !modal.ov.classList.contains('open')) { return; }
      modal.ov.classList.remove('open');
      var root = document.getElementById('ceo-root'); root.inert = false; root.removeAttribute('aria-hidden');
      APP.park();
      if (!silent && modal.opener && document.body.contains(modal.opener)) { modal.opener.focus(); }
    }
  };

  /* ------------------------------------------------------------------ the one live textarea (#t1) — its own script counts it */
  APP.note = function (label, help, value) {
    var scope = document.getElementById('ceo-tx-scope'), g = scope.querySelector('.tx-group'), ta = g.querySelector('textarea');
    g.querySelector('label').textContent = label; ta.value = value || ''; ta.removeAttribute('aria-invalid');
    g.classList.remove('is-error'); var h = g.querySelector('.tx-help'); h.textContent = help;
    ta.dispatchEvent(new Event('input')); return scope;
  };
  APP.noteValue = function () { return document.getElementById('t1').value.trim(); };
  APP.noteError = function (msg) { var scope = document.getElementById('ceo-tx-scope'), g = scope.querySelector('.tx-group'), ta = g.querySelector('textarea');
    g.classList.add('is-error'); ta.setAttribute('aria-invalid', 'true'); g.querySelector('.tx-help').textContent = msg; ta.focus(); };
  APP.park = function () { var p = document.getElementById('ceo-parking'), s = document.getElementById('ceo-tx-scope'); if (s && s.parentNode !== p) { p.appendChild(s); } };

  /* ------------------------------------------------------------------ exports */
  APP.download = function (name, mime, text) {
    var blob = new Blob([text], { type: mime }), a = document.createElement('a');
    a.href = URL.createObjectURL(blob); a.download = name; document.body.appendChild(a); a.click();
    setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 500);
  };
  APP.exportRows = function (fmt, title, cols, rows) {
    var safe = title.toLowerCase().replace(/[^a-z0-9]+/g, '-');
    if (fmt === 'pdf') { window.print(); return 'Print dialog opened — choose "Save as PDF".'; }
    if (fmt === 'xlsx') {
      var h = '<table><thead><tr>' + cols.map(function (c) { return '<th>' + esc(c.label) + '</th>'; }).join('') + '</tr></thead><tbody>' +
        rows.map(function (r) { return '<tr>' + cols.map(function (c) { return '<td>' + esc(c.text(r)) + '</td>'; }).join('') + '</tr>'; }).join('') + '</tbody></table>';
      APP.download(safe + '.xls', 'application/vnd.ms-excel', '<html><head><meta charset="utf-8"></head><body>' + h + '</body></html>');
      return rows.length + ' rows exported as an Excel-readable table (.xls).';
    }
    var csv = [cols.map(function (c) { return '"' + c.label.replace(/"/g, '""') + '"'; }).join(',')].concat(rows.map(function (r) {
      return cols.map(function (c) { return '"' + String(c.text(r)).replace(/"/g, '""') + '"'; }).join(','); })).join('\n');
    APP.download(safe + '.csv', 'text/csv', csv);
    return rows.length + ' rows exported as CSV.';
  };
}());
