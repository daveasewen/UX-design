/* ===== APP CORE — authored JavaScript (s258-D1: the author writes the wiring the snippets cannot
   know about). Wires, by DELEGATION at the document (rule 14), every control the pages render from
   DATA: the shared entity / region / date filters, persistence (URL query + localStorage, rule 15),
   the theme switch, dropdown menus, the drawer, the modal, toasts, the records grid, CSV export and
   the chart calls into the pack's own engine (window.dvRender — canon/dv-render.js, spliced).
   Markup it writes is the markup of the named snippets, by class: Data-grid, Filter-toolbar-bar,
   Drawer, Modals, Toast, Status-indicator, Summary, Input-fields, Textarea, Selection-controls,
   Segmented-control, Kpi-tile (Template-dashboard-bento form), Timeline, Limits-meter, Alert. ===== */
var APP = (function () {
  'use strict';
  var D = DATA;
  var PAGE = document.documentElement.getAttribute('data-page');
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return [].slice.call((r || document).querySelectorAll(s)); };
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  var MON = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  var SYM = { GBP: '£', EUR: '€', USD: '$', SGD: 'S$', HKD: 'HK$', AED: 'AED ', MXN: 'MX$', CNY: 'CN¥' };

  /* ---------- formatting */
  var F = {
    date: function (iso) { if (!iso) { return '—'; } var p = iso.split('-'); return (+p[2]) + ' ' + MON[+p[1] - 1] + ' ' + p[0]; },
    dshort: function (iso) { var p = iso.split('-'); return (+p[2]) + ' ' + MON[+p[1] - 1]; },
    num: function (v, d) { return Number(v).toLocaleString('en-GB', { minimumFractionDigits: d || 0, maximumFractionDigits: d || 0 }); },
    gbpM: function (v) { return (v < 0 ? '−' : '') + '£' + F.num(Math.abs(v) / 1e6, 1) + 'm'; },
    m: function (v) { return F.num(v / 1e6, 1); },
    money: function (v, ccy) { return (v < 0 ? '−' : '') + (SYM[ccy] || ccy + ' ') + F.num(Math.abs(v), 2); },
    moneyM: function (v, ccy) { return (v < 0 ? '−' : '') + (SYM[ccy] || ccy + ' ') + F.num(Math.abs(v) / 1e6, 2) + 'm'; },
    pct: function (v, d) { return F.num(v, d == null ? 1 : d) + '%'; },
    signedPct: function (v) { return (v > 0 ? '+' : v < 0 ? '−' : '') + F.num(Math.abs(v), 1) + '%'; }
  };

  /* ---------- persistence: URL query (shareable) + localStorage (survives reload and page change) */
  var KEY = 'hsbc-ceo-proto.v1', WKEY = 'hsbc-ceo-proto.v1.work';
  function load(k) { try { return JSON.parse(localStorage.getItem(k)) || {}; } catch (e) { return {}; } }
  function save(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { /* private mode: state lives in the URL only */ } }
  var stored = load(KEY);
  var q = new URLSearchParams(location.search);
  var S = {
    entity: q.get('entity') || stored.entity || 'all',
    region: q.get('region') || stored.region || 'all',
    days: +(q.get('days') || stored.days || 30),
    theme: stored.theme || 'light',
    nav: stored.nav || 'auto'
  };
  if ([7, 14, 30].indexOf(S.days) < 0) { S.days = 30; }
  if (S.entity !== 'all' && !D.ENT[S.entity]) { S.entity = 'all'; }
  if (S.region !== 'all' && !D.REGIONS.some(function (r) { return r.id === S.region; })) { S.region = 'all'; }
  if (S.entity !== 'all' && S.region !== 'all' && D.ENT[S.entity].region !== S.region) { S.entity = 'all'; }   /* a drill-through region wins */
  var PS = (stored.pages && stored.pages[PAGE]) || {};          /* page-specific state */
  q.forEach(function (v, k) { if (k.indexOf('p.') === 0) { PS[k.slice(2)] = v; } });
  var W = load(WKEY);                                           /* workflow record: approvals, acknowledgements, requests */
  ['pay', 'exc', 'msg'].forEach(function (k) { W[k] = W[k] || {}; });
  ['sr', 'audit', 'runs'].forEach(function (k) { W[k] = W[k] || []; });

  function persist() {
    var all = load(KEY); all.entity = S.entity; all.region = S.region; all.days = S.days; all.theme = S.theme; all.nav = S.nav;
    all.pages = all.pages || {}; all.pages[PAGE] = PS; save(KEY, all);
    var u = new URLSearchParams();
    if (S.entity !== 'all') { u.set('entity', S.entity); }
    if (S.region !== 'all') { u.set('region', S.region); }
    if (S.days !== 30) { u.set('days', S.days); }
    Object.keys(PS).forEach(function (k) { if (PS[k] !== '' && PS[k] != null) { u.set('p.' + k, PS[k]); } });
    var s = u.toString();
    history.replaceState(null, '', location.pathname + (s ? '?' + s : '') + location.hash);
    decorateLinks();
  }
  function saveWork() { save(WKEY, W); }
  function shared() {
    var u = new URLSearchParams();
    if (S.entity !== 'all') { u.set('entity', S.entity); }
    if (S.region !== 'all') { u.set('region', S.region); }
    if (S.days !== 30) { u.set('days', S.days); }
    return u.toString();
  }
  /* every in-app link carries the shared filters, so the filter state follows the reader across pages */
  function decorateLinks() {
    var s = shared();
    $$('a[data-app-href]').forEach(function (a) {
      var h = a.getAttribute('data-app-href'), parts = h.split('#'), base = parts[0], hash = parts[1] ? '#' + parts[1] : '';
      var extra = new URLSearchParams(base.indexOf('?') > -1 ? base.slice(base.indexOf('?') + 1) : ''), u = new URLSearchParams(s);
      extra.forEach(function (v, k) { u.set(k, v); });   /* a drill-through parameter overrides the carried filter */
      var path = base.split('?')[0], qs = u.toString();
      a.setAttribute('href', path + (qs ? '?' + qs : '') + hash);
    });
  }

  /* ---------- scope: entity / region / date filters */
  function inScope(entityId) {
    var e = D.ENT[entityId]; if (!e) { return false; }
    if (S.entity !== 'all' && S.entity !== entityId) { return false; }
    if (S.region !== 'all' && S.region !== e.region) { return false; }
    return true;
  }
  function scopedEntities() { return D.ENTITIES.filter(function (e) { return inScope(e.id); }); }
  function dayIdx() { var out = []; for (var i = 30 - S.days; i < 30; i++) { out.push(i); } return out; }
  function days() { return dayIdx().map(function (i) { return D.DAYS[i]; }); }
  function inWindow(iso) { return iso >= D.DAYS[30 - S.days] && iso <= D.AS_OF; }
  function scopeLabel() {
    var e = S.entity !== 'all' ? D.ENT[S.entity].name : null, r = S.region !== 'all' ? regionName(S.region) : null;
    return (e || (r ? r + ' entities' : 'All entities')) + ' · last ' + S.days + ' days to ' + F.date(D.AS_OF);
  }
  function regionName(id) { var r = D.REGIONS.filter(function (x) { return x.id === id; })[0]; return r ? r.name : id; }

  /* ---------- derived treasury figures, always from the rows (rule 13: never a hard-coded total) */
  var calc = {
    cashSeries: function () {   /* daily cash, £, over the window, for entities in scope */
      return dayIdx().map(function (i) { return D.ACCOUNTS.reduce(function (a, ac) { return inScope(ac.entity) ? a + D.toGBP(ac.balances[i], ac.ccy) : a; }, 0); });
    },
    undrawnSeries: function () {
      return dayIdx().map(function (i) { return D.FACILITIES.reduce(function (a, f) { return inScope(f.entity) && f.committed ? a + D.toGBP(f.limit - f.drawnSeries[i], f.ccy) : a; }, 0); });
    },
    commitments: function () { return D.COMMITMENTS.reduce(function (a, c) { return inScope(c.entity) ? a + D.toGBP(c.amount, c.ccy) : a; }, 0); },
    buffer: function () {  /* policy buffer allocated by share of group cash */
      var all = D.ACCOUNTS.reduce(function (a, ac) { return a + D.toGBP(ac.balances[29], ac.ccy); }, 0);
      var mine = D.ACCOUNTS.reduce(function (a, ac) { return inScope(ac.entity) ? a + D.toGBP(ac.balances[29], ac.ccy) : a; }, 0);
      return D.POLICY_BUFFER_GBP * (all ? mine / all : 0);
    },
    liquiditySeries: function () { var c = calc.cashSeries(), u = calc.undrawnSeries(); return c.map(function (v, i) { return v + u[i]; }); },
    headroomSeries: function () { var l = calc.liquiditySeries(), b = calc.buffer(), cm = calc.commitments(); return l.map(function (v) { return v - b - cm; }); },
    exposureByRegionCcy: function () {  /* net exposure, £, positions of in-scope entities */
      var out = {};
      D.POSITIONS.forEach(function (p) { if (!inScope(p.entity)) { return; } var r = D.ENT[p.entity].region; out[r] = out[r] || {}; out[r][p.ccy] = (out[r][p.ccy] || 0) + p.gbp; });
      return out;
    },
    payments: function () { return D.PAYMENTS.map(function (p) { var w = W.pay[p.id]; return w ? Object.assign({}, p, { status: w.status, decidedAt: w.at, note: w.note, reason: w.reason }) : p; }); },
    exceptions: function () { return D.EXCEPTIONS.map(function (x) { var w = W.exc[x.id]; return Object.assign({}, x, { status: w && w.length ? 'Acknowledged' : 'Open', notes: w || [] }); }); },
    requests: function () { return W.sr.concat(D.REQUESTS); }
  };

  /* ---------- toasts (Toast snippet markup; polite live region) */
  function toast(msg, kind) {
    var host = $('#toasts'); if (!host) { return; }
    var k = kind || 'ok', ic = { ok: 'to-success', info: 'to-info', warn: 'to-warning' }[k];
    var t = document.createElement('div');
    t.className = 'toast ' + k; t.setAttribute('role', 'status'); t.setAttribute('data-carries', 'symbol label');
    t.innerHTML = '<span class="ic"><svg aria-hidden="true"><use href="#' + ic + '"/></svg></span><p class="msg t-ed-body">' + esc(msg) + '</p>' +
      '<button class="x" type="button" aria-label="Dismiss message" data-action="toast-close"><svg aria-hidden="true"><use href="#to-close"/></svg></button>';
    host.appendChild(t);
    var timer = setTimeout(function () { close(); }, 6000);
    t.addEventListener('mouseenter', function () { clearTimeout(timer); });
    t.addEventListener('mouseleave', function () { timer = setTimeout(close, 3000); });
    function close() { t.classList.add('leaving'); setTimeout(function () { t.remove(); }, 220); }
    t.__close = close;
  }

  /* ---------- modal (Modals snippet: .overlay > .dialog; inert page, focus trap, Esc, return focus) */
  var lastFocus = null;
  function openModal(o) {
    var ov = $('#modal'), dlg = $('.dialog', ov);
    $('#modal-t').textContent = o.title;
    $('#modal-b').innerHTML = o.body;
    $('#modal-a').innerHTML = (o.actions || []).map(function (a) {
      return '<button class="btn ' + (a.kind || 'secondary') + '" type="button" data-modal-act="' + a.id + '">' + esc(a.label) + '</button>';
    }).join('');
    ov.__on = o.onAction || function () {};
    lastFocus = document.activeElement;
    ov.classList.add('open'); ov.removeAttribute('hidden');
    $('#shell').inert = true;
    var f = $('input, textarea, select, button[data-modal-act]', dlg);
    /* the overlay's visibility transitions in; focus lands once it is visible */
    setTimeout(function () { (f || dlg).focus(); }, 40);
  }
  var lastRecord = null;
  /* focus goes back to what opened the layer; when that was re-rendered (a decision re-draws the
     grid) or never existed (a record opened from the URL), to the record's row, else to <main> */
  function refocus(el) {
    if (el && el !== document.body && document.contains(el) && el.focus) { el.focus(); return; }
    var row = lastRecord && document.querySelector('tr[data-id="' + lastRecord + '"]');
    (row || document.getElementById('main')).focus();
  }
  function closeModal() {
    var ov = $('#modal'); ov.classList.remove('open'); ov.setAttribute('hidden', '');
    $('#shell').inert = false; setTimeout(function () { refocus(lastFocus); }, 0);
  }
  /* ---------- drawer (Drawer snippet: .scrim + .sheet) */
  var drawerFocus = null;
  function openDrawer(o) {
    $('#drawer-t').textContent = o.title;
    $('#drawer-b').innerHTML = o.body;
    $('#drawer-f').innerHTML = (o.actions || []).map(function (a) {
      return '<button class="dbtn ' + (a.kind || 'secondary') + ' t-cm-button t-cm-slot" type="button" data-drawer-act="' + a.id + '">' + esc(a.label) + '</button>';
    }).join('');
    $('#drawer').__on = o.onAction || function () {};
    drawerFocus = document.activeElement;
    $('#scrim').classList.add('open'); $('#drawer').classList.add('open');
    $('#shell').inert = true;
    setTimeout(function () { $('#drawer .close').focus(); }, 40);   /* after the sheet's visibility transition */
    if (o.id) { PS.open = o.id; lastRecord = o.id; persist(); }
  }
  function closeDrawer() {
    $('#scrim').classList.remove('open'); $('#drawer').classList.remove('open');
    $('#shell').inert = false; refocus(drawerFocus);
    if (PS.open) { delete PS.open; persist(); }
  }
  /* a longer form (many options) goes in the Drawer's scrolling side sheet, not the Modal — the
     modal's dialog does not scroll, so it is kept for short confirmations */
  function openForm(o) {
    openDrawer({ title: o.title, body: o.body, actions: o.actions, onAction: function (a) {
      if (a === 'cancel') { closeDrawer(); return; }
      if (o.onAction(a) !== false) { closeDrawer(); }
    } });
  }
  function trap(e, root) {
    if (e.key !== 'Tab') { return; }
    var f = $$('a[href], button:not([disabled]), input:not([disabled]), textarea, select, [tabindex="0"]', root).filter(function (x) { return x.offsetParent !== null; });
    if (!f.length) { return; }
    var first = f[0], last = f[f.length - 1];
    if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
    else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
  }

  /* ---------- markup helpers (snippet classes) */
  var H = {
    stat: function (tone, label) { return '<span class="cn-status-indicator"><span class="stat ' + tone + '" data-carries="label"><span class="dot" aria-hidden="true"></span><span class="t-cm-legal">' + esc(label) + '</span></span></span>'; },
    summary: function (rows) {
      return '<div class="cn-summary"><dl class="summary">' + rows.map(function (r) {
        return '<div class="summary__row' + (r.total ? ' summary__row--total' : '') + '"><dt class="summary__k">' + esc(r.k) + '</dt><dd class="summary__v">' + (r.html || esc(r.v)) + '</dd></div>';
      }).join('') + '</dl></div>';
    },
    field: function (o) {   /* Input-fields boxed field */
      return '<div class="cn-input-fields"><div class="field' + (o.error ? ' is-error' : '') + '" data-field="' + o.id + '"><div class="lbl"><label for="' + o.id + '">' + esc(o.label) + '</label></div>' +
        (o.help ? '<p class="help-text" id="' + o.id + '-help">' + esc(o.help) + '</p>' : '') +
        '<div class="box">' + (o.prefix ? '<span class="prefix" aria-hidden="true">' + esc(o.prefix) + '</span>' : '') +
        '<input id="' + o.id + '" type="text" ' + (o.inputmode ? 'inputmode="' + o.inputmode + '" ' : '') + 'value="' + esc(o.value || '') + '"' + (o.help ? ' aria-describedby="' + o.id + '-help"' : '') + '></div>' +
        '<div class="err-msg" hidden><span class="ic" aria-hidden="true"><svg class="icn" viewBox="0 0 18 18"><use href="#ic-error"/></svg></span><p id="' + o.id + '-err"></p></div></div></div>';
    },
    textarea: function (o) {
      return '<div class="cn-textarea"><div class="tx-group" data-field="' + o.id + '"><div class="tx-lblrow"><label class="t-cm-label" for="' + o.id + '">' + esc(o.label) + '</label>' + (o.optional ? '<span class="tx-opt t-cm-caption">(optional)</span>' : '') + '</div>' +
        '<div class="tx-box"><textarea id="' + o.id + '" class="t-ed-body" maxlength="' + (o.max || 500) + '" rows="' + (o.rows || 4) + '" aria-describedby="' + o.id + '-help ' + o.id + '-count"></textarea></div>' +
        '<div class="tx-foot"><p class="tx-help t-ed-body-small" id="' + o.id + '-help">' + esc(o.help || '') + '</p><span class="tx-count t-cm-legal" id="' + o.id + '-count">0/' + (o.max || 500) + '</span></div>' +
        '<p class="err-msg t-ed-body-small" id="' + o.id + '-err" hidden></p></div></div>';
    },
    check: function (o) {
      return '<div class="cn-selection-controls"><div class="sc"><div class="field" data-field="' + o.id + '"><input type="checkbox" id="' + o.id + '"' + (o.checked ? ' checked' : '') + (o.role ? ' role="' + o.role + '"' : '') + '><label for="' + o.id + '">' +
        (o.role === 'switch' ? '<span class="switch"><span class="thumb"></span></span> ' : '<span class="box"><svg data-bespoke="checkbox tick, animated stroke-draw control glyph" viewBox="0 0 18 18"><path class="tick" d="M3.5 9.5 L7.5 13.5 L14.5 5"/></svg></span> ') +
        esc(o.label) + '</label></div><p class="err-msg" id="' + o.id + '-err" hidden></p></div></div>';
    },
    radios: function (o) {
      return '<div class="cn-selection-controls"><div class="sc"><fieldset data-field="' + o.name + '"><legend>' + esc(o.legend) + '</legend>' + o.options.map(function (op, i) {
        var id = o.name + '-' + i;
        return '<div class="field"><input type="radio" name="' + o.name + '" id="' + id + '" value="' + esc(op.v) + '"' + (op.v === o.value ? ' checked' : '') + '><label for="' + id + '"><span class="radio"><span class="dot"></span></span> ' + esc(op.label) + '</label></div>';
      }).join('') + '<p class="err-msg" id="' + o.name + '-err" hidden></p></fieldset></div></div>';
    },
    alert: function (tone, title, text) {
      var ic = { err: 'al-error', warn: 'al-warning', ok: 'al-success', info: 'al-info' }[tone];
      return '<div class="cn-alert"><div class="alert ' + tone + '" role="' + (tone === 'err' ? 'alert' : 'status') + '" data-carries="symbol label"><span class="ic"><svg aria-hidden="true"><use href="#' + ic + '"/></svg></span><p class="main t-ed-body"><strong class="em">' + esc(title) + '</strong> ' + esc(text) + '</p></div></div>';
    },
    timeline: function (items) {
      return '<div class="cn-timeline"><section class="tl" aria-label="History"><div class="tl-group"><ol class="tl-list">' + items.map(function (it) {
        return '<li class="' + (it.tone || 'inf') + '"><span class="tl-node" aria-hidden="true"></span><span class="tl-line"><span class="tl-title t-cm-ctl-14">' + esc(it.title) + '</span>' +
          (it.amount ? '<span class="tl-amount t-cm-figure-6">' + esc(it.amount) + '</span>' : '') + '</span><span class="tl-meta"><time class="t-cm-legal" datetime="' + esc(it.date) + '">' + esc(it.when || F.date(it.date.slice(0, 10))) + '</time></span>' +
          (it.desc ? '<p class="tl-desc t-ed-body-small">' + esc(it.desc) + '</p>' : '') + '</li>';
      }).join('') + '</ol></div></section></div>';
    },
    limit: function (o) {   /* Limits-meter: ink on track, the word changes, not the hue */
      var pct = Math.max(0, Math.min(100, o.used / o.limit * 100)), tone = pct >= 100 ? 'err' : pct >= 85 ? 'warn' : 'ok', id = 'lim-' + o.id;
      return '<div class="cn-limits-meter"><div class="lim" role="group" aria-labelledby="' + id + '"><div class="lim-head"><span class="lim-label t-cm-label" id="' + id + '">' + esc(o.label) + '</span>' +
        '<span class="chip ' + tone + '"><span class="dot" aria-hidden="true"></span><span class="t-cm-legal">' + esc(o.chip || (F.pct(o.used / o.limit * 100, 0) + ' used')) + '</span></span></div>' +
        '<span class="amount amount--display t-cm-figure-4"><span>£</span><span>' + F.m(Math.max(0, o.limit - o.used)) + 'm</span></span><span class="lim-verdict t-cm-caption">' + esc(o.verdict || 'Headroom') + '</span>' +
        '<div class="pb-track" role="progressbar" aria-labelledby="' + id + '" aria-valuenow="' + Math.round(o.used) + '" aria-valuemin="0" aria-valuemax="' + Math.round(o.limit) + '" aria-valuetext="' + esc(F.gbpM(o.used) + ' used of a ' + F.gbpM(o.limit) + ' limit') + '"><div class="pb-fill" style="width:' + pct.toFixed(2) + '%"></div></div>' +
        '<div class="lim-legend"><span class="lim-key t-cm-legal"><span class="sw sw--used" aria-hidden="true"></span>Used <span class="v t-cm-figure-6">' + F.gbpM(o.used) + '</span></span><span class="lim-key t-cm-legal"><span class="sw sw--left" aria-hidden="true"></span>Limit <span class="v t-cm-figure-6">' + F.gbpM(o.limit) + '</span></span></div></div></div>';
    }
  };

  /* ---------- KPI tile (Template-dashboard-bento's kpi-tile, compact); the spark is data-driven polyline */
  function spark(vals) {
    var lo = Math.min.apply(null, vals), hi = Math.max.apply(null, vals), span = hi - lo || 1, n = vals.length;
    var pts = vals.map(function (v, i) { return [(3 + 194 * i / (n - 1)).toFixed(1), (45 - 42 * (v - lo) / span).toFixed(1)]; });
    return { pts: pts.map(function (p) { return p.join(','); }).join(' '), end: pts[pts.length - 1] };
  }
  function kpi(o) {
    var first = o.series[0], last = o.series[o.series.length - 1], ch = first ? (last - first) / Math.abs(first) * 100 : 0;
    var dir = Math.abs(ch) < 0.05 ? 'flat' : ch > 0 ? 'up' : 'down', sp = spark(o.series);
    return '<div class="c-bento__tile kpi-tile has-cta" role="group" aria-label="' + esc(o.label) + '" data-c="1" data-r="1" data-kpi="' + o.id + '">' +
      '<p class="lbl16 t-cm-caption">' + esc(o.label) + '</p>' +
      (o.count ? '<span class="amt t-cm-figure-3"><span>' + F.num(last) + '</span></span>' : '<span class="amt t-cm-figure-3"><span>' + (last < 0 ? '−£' : '£') + '</span><span>' + F.m(Math.abs(last)) + 'm</span></span>') +
      '<span class="delta ' + dir + '" data-carries="symbol label"><span class="arrow" aria-hidden="true"><svg><use href="#kpi-' + (dir === 'flat' ? 'up' : dir) + '"/></svg></span><span class="t-cm-figure-6">' + F.signedPct(ch) + ' ' + (dir === 'flat' ? 'flat' : dir) + '</span><span class="per t-cm-legal">vs ' + F.dshort(days()[0]) + '</span></span>' +
      '<div class="kpi-spark"><svg class="spark-inline" data-trend="' + dir + '" viewBox="0 0 200 48" preserveAspectRatio="none" aria-hidden="true" data-bespoke="chart canvas — dataviz geometry, not an icon (validate-dataviz territory)">' +
      '<line class="dv-base" x1="3" y1="45" x2="197" y2="45"/><polyline class="dv-series" points="' + sp.pts + '"/><circle class="dv-end" cx="' + sp.end[0] + '" cy="' + sp.end[1] + '" r="3"/></svg></div>' +
      '<button type="button" class="kpi-cta" aria-label="' + esc(o.label) + ', daily figures" data-action="kpi-table" data-kpi="' + o.id + '"><svg viewBox="0 0 18 18" aria-hidden="true"><use href="#kpi-table"/></svg></button></div>';
  }
  var KPI = {};
  function renderKpis(host, list) {
    list.forEach(function (k) { KPI[k.id] = k; });
    host.innerHTML = list.map(kpi).join('');
  }
  function kpiTable(id) {
    var k = KPI[id]; if (!k) { return; }
    var ds = days();
    openDrawer({ title: k.label + ' — daily, ' + scopeLabel(), body:
      '<p class="t-ed-body-small">' + esc(k.note || '') + '</p><div class="cn-table"><div class="scroll" role="region" aria-label="' + esc(k.label) + ' by day" tabindex="0"><table><caption>' + esc(k.label) + ' by day' + (k.count ? '' : ', £ millions') + '</caption><thead><tr><th scope="col">Date</th><th scope="col" class="num">£m</th></tr></thead><tbody>' +
      k.series.map(function (v, i) { return '<tr><th scope="row" data-first><span class="v">' + F.date(ds[i]) + '</span></th><td class="num"><span class="v">' + (k.count ? F.num(v) : F.m(v)) + '</span></td></tr>'; }).reverse().join('') + '</tbody></table></div></div>',
      actions: [{ id: 'csv', label: 'Export CSV', kind: 'primary' }, { id: 'close', label: 'Close' }],
      onAction: function (a) { if (a === 'csv') { csv(k.label.toLowerCase().replace(/\W+/g, '-') + '.csv', [['Date', k.label + ' (GBP m)']].concat(k.series.map(function (v, i) { return [ds[i], F.m(v).replace(/,/g, '')]; }))); } else { closeDrawer(); } } });
  }

  /* ---------- CSV export (a real file, built from the rows the reader is looking at) */
  function csv(name, rows) {
    var body = rows.map(function (r) { return r.map(function (c) { c = String(c == null ? '' : c); return /[",\n]/.test(c) ? '"' + c.replace(/"/g, '""') + '"' : c; }).join(','); }).join('\n');
    var url = URL.createObjectURL(new Blob([body], { type: 'text/csv' })), a = document.createElement('a');
    a.href = url; a.download = name; document.body.appendChild(a); a.click(); a.remove();
    setTimeout(function () { URL.revokeObjectURL(url); }, 1000);
    W.audit.unshift({ at: new Date().toISOString(), what: 'Exported ' + name + ' (' + (rows.length - 1) + ' rows)' }); saveWork();
    toast('Exported ' + (rows.length - 1) + ' rows to ' + name, 'ok');
  }

  /* ---------- charts: figure skeletons in the chart snippets' own grammar, drawn by dvRender */
  var CSVBTN = '%%CSVBTN%%', SUMM = '%%SUMMARY%%';
  /* the chart snippets' scope classes, written out whole so every class name on the page is a literal */
  var SCOPE = { column: 'cn-chart-bar', bar: 'cn-chart-bar', 'grouped-column': 'cn-chart-bar', 'stacked-column': 'cn-chart-bar', line: 'cn-chart-line', multiline: 'cn-chart-line',
    'stacked-area': 'cn-chart-stacked-area', donut: 'cn-chart-donut', pie: 'cn-chart-pie', combo: 'cn-chart-combo', bullet: 'cn-chart-bullet', candlestick: 'cn-chart-candlestick',
    scatter: 'cn-chart-scatter', boxplot: 'cn-chart-boxplot', histogram: 'cn-chart-histogram', 'butterfly-h': 'cn-chart-butterfly-h', 'butterfly-v': 'cn-chart-butterfly-v', spark: 'cn-chart-sparkline' };
  var LETTERS = 'ABCDEFGHIJ';
  function legend(id, names, pal) {
    return '<ul class="dv-leg ' + (pal === 'vert' ? 'vert' : 'center') + ' t-cm-chart-label" id="' + id + '-legend" role="group" aria-label="Series — uncheck a swatch to dim it, click a name to isolate — then check swatches to add — Reset to show all">' +
      names.map(function (n, i) {
        var sc = 'var(--data-series-' + ((i % 5) + 1) + ')';
        return '<li class="dv-legrow" data-series="' + (i + 1) + '"><span class="dv-leg-sw" role="checkbox" aria-checked="true" tabindex="0" aria-label="Show or hide ' + esc(n) + '" style="--sc:' + sc + '"></span><button type="button" class="dv-leg-item t-cm-chart-label" data-series="' + (i + 1) + '" aria-pressed="false" aria-label="Isolate ' + esc(n) + '"><span class="dv-key t-cm-chart-key">' + LETTERS[i] + '</span><span class="dv-leg-name">' + esc(n) + '</span></button></li>';
      }).join('') + '<li class="dv-leg-reset-wrap"><button type="button" class="dv-leg-reset t-cm-chart-label" data-for="' + id + '-legend" disabled>Reset</button></li></ul><p class="dv-sr" id="' + id + '-live" role="status" aria-live="polite"></p>';
  }
  function figure(c) {
    var t = c.type, id = c.id, radial = t === 'donut' || t === 'pie', dvt = t === 'spark' ? 'spark' : t;
    var svg;
    if (radial) { svg = '<svg class="dv-svg" data-bespoke="chart canvas — dataviz geometry, not an icon (validate-dataviz territory)" viewBox="0 0 300 260" width="300" height="260" role="group" aria-label="' + esc(c.caption) + '"></svg>'; }
    else if (t === 'bullet') { svg = '<svg class="dv-svg dv-fit" data-pl="120" data-pl-fit="text.dv-label" data-pr="12" data-h="' + (c.h || 200) + '" data-pt="4" data-pb="16" data-h-min="' + (c.h || 200) + '" data-bespoke="chart canvas — dataviz geometry, not an icon (validate-dataviz territory)" viewBox="0 0 580 ' + (c.h || 200) + '" role="group" aria-label="' + esc(c.caption) + '"></svg>'; }
    else if (t === 'spark') { svg = '<svg class="dv-svg spark-standalone" data-trend="flat" data-pl="4" data-pr="4" data-pt="4" data-pb="4" data-h="90" data-h-min="90" data-bespoke="chart canvas — dataviz geometry, not an icon (validate-dataviz territory)" viewBox="0 0 580 90" preserveAspectRatio="none" role="group" aria-label="' + esc(c.caption) + '"></svg>'; }
    else {
      var pl = t === 'bar' ? 46 : /butterfly-h/.test(t) ? 60 : 46, pr = t === 'combo' ? 44 : /butterfly-h/.test(t) ? 60 : 12;
      svg = '<svg class="dv-svg dv-fit" data-pl="' + pl + '"' + (t === 'bar' ? ' data-pl-fit="text.dv-label"' : '') + ' data-pr="' + pr + '" data-h="' + (c.h || 260) + '" data-pt="14" data-pb="30" data-h-min="200" data-bespoke="chart canvas — dataviz geometry, not an icon (validate-dataviz territory)" viewBox="0 0 580 ' + (c.h || 260) + '" role="group" aria-label="' + esc(c.caption) + '"></svg>';
    }
    var head = t === 'spark' ? '' :
      '<div class="dv-head"><h3 class="dv-title t-cm-section-label">' + esc(c.title) + '</h3>' + (c.note ? '<span class="t-cm-caption">' + esc(c.note) + '</span>' : '') + '<div class="dv-controls" role="group" aria-label="Chart tools">' + (c.controls || '') + CSVBTN +
      '<details class="dv-tbl">' + SUMM.replace('%ID%', id) + '<div class="dv-tablepanel" id="' + id + '-tbl" role="region" aria-label="' + esc(c.caption) + ', data table" tabindex="-1"><table class="dv-table t-cm-legal"><caption>' + esc(c.caption) + '</caption></table></div></details></div></div>';
    var leg = c.legend ? legend(id, c.legend, radial ? 'vert' : 'center') : '';
    var stage = radial ? '<div class="dv-stage"><div class="dv-donut-row">' + svg + leg + '</div></div>' :
      t === 'spark' ? '<div class="dv-stage">' + svg + '</div><div class="dv-tablepanel sr-only" role="region" aria-label="' + esc(c.caption) + ', data table"><table class="dv-table t-cm-legal"><caption>' + esc(c.caption) + '</caption></table></div>' :
      '<div class="dv-stage"><div class="dv-chart-area">' + svg + '</div></div>' + leg;
    var extra = '';
    if (t === 'donut' || t === 'pie') { extra = ' data-total="0" data-labelling="spider"'; }
    if (c.max != null) { extra += ' data-domain-max="' + c.max + '"'; }
    var dmin = /candlestick|scatter|line|multiline|spark|combo/.test(t) ? '' : ' data-domain-min="0"';
    return '<div class="' + SCOPE[t] + ' ceo-chart"><figure class="dv dv-fit-on' + (t === 'donut' ? '' : ' dv-animate') + '" id="' + id + '" data-dv-type="' + dvt + '"' + dmin + extra + ' data-surface="page" role="group" aria-labelledby="' + id + '-h"' +
      (t === 'spark' ? '' : ' data-lockup-title="' + esc(c.title) + '" data-lockup-table="' + id + '-tbl"') + '><figcaption id="' + id + '-h" class="sr-only">' + esc(c.caption) + '</figcaption>' + head + stage + (c.after || '') + '</figure></div>';
  }
  var CHARTS = {};
  function mountChart(host, c) { host.innerHTML = figure(c); CHARTS[c.id] = c; }
  function drawChart(id, spec) {
    var fig = document.getElementById(id); if (!fig || !window.dvRender) { return; }
    try {
      if (spec.type === 'donut' || spec.type === 'pie') { fig.setAttribute('data-total', String(Math.round(spec.series[0].values.reduce(function (a, b) { return a + b; }, 0) * 10) / 10)); }
      window.dvRender(fig, spec);
      if (fig.__dvLegendReset) { fig.__dvLegendReset(); }
      var lg = fig.querySelector('.dv-leg'); if (lg && lg.__dv) { delete lg.__dv; }
      var empty = fig.querySelector('.ceo-empty'); if (empty) { empty.remove(); }
    } catch (err) { console.warn(err); }
  }
  function emptyChart(id, text) {
    var fig = document.getElementById(id); if (!fig) { return; }
    var svg = fig.querySelector('svg.dv-svg'); if (svg) { svg.innerHTML = ''; }
    var t = fig.querySelector('table.dv-table'); if (t) { t.innerHTML = '<caption>No data in scope</caption>'; }
    if (!fig.querySelector('.ceo-empty')) {
      fig.insertAdjacentHTML('beforeend', '<div class="ceo-empty"><div class="cn-empty-state"><div class="empty"><h3 class="t-cm-caption">No data to display</h3><p class="t-cm-legal">' + esc(text || 'Nothing in the current entity, region and date filters.') + '</p></div></div></div>');
    }
  }

  /* ---------- records grid (Data-grid markup; sort, search, page, open-a-record) */
  var GRIDS = {};
  function grid(host, g) {
    GRIDS[g.id] = g;
    g.state = { q: PS[g.id + '.q'] || '', sort: PS[g.id + '.sort'] || g.sort || '', dir: PS[g.id + '.dir'] || g.dir || 'descending', page: +(PS[g.id + '.page'] || 1), size: +(PS[g.id + '.size'] || g.size || 10) };
    var cols = g.cols.map(function (c) {
      var sortable = c.sort !== false;
      return '<th scope="col" ' + (sortable ? 'aria-sort="none" ' : 'data-disabled="true" ') + 'data-key="' + c.k + '"' + (c.num ? ' class="num"' : '') + '><div class="th-in">' +
        (sortable ? '<button class="sort full t-cm-button" type="button" data-grid="' + g.id + '" data-sort="' + c.k + '"><span class="lbl">' + esc(c.label) + '</span>' +
          '<span class="ic ic-none" aria-hidden="true"><svg viewBox="0 0 18 18"><use href="#dg-sort"/></svg></span><span class="ic ic-asc" aria-hidden="true"><svg viewBox="0 0 18 18"><use href="#dg-cup"/></svg></span><span class="ic ic-desc" aria-hidden="true"><svg viewBox="0 0 18 18"><use href="#dg-cdown"/></svg></span></button>'
          : '<span class="sort full t-cm-button"><span class="lbl">' + esc(c.label) + '</span></span>') + '</div></th>';
    }).join('');
    host.innerHTML = '<div class="cn-data-grid"><div class="dg" id="' + g.id + '" data-density="comfortable" data-groups="off">' +
      '<div class="dg-head"><span class="t-cm-section-label" id="' + g.id + '-title">' + esc(g.title) + '</span><span class="dg-count t-cm-caption" id="' + g.id + '-count" aria-live="polite"></span></div>' +
      '<div class="dg-toolbar"><div class="dgsearch"><span class="mag" aria-hidden="true"><svg viewBox="0 0 18 18" aria-hidden="true"><use href="#dg-search"/></svg></span>' +
      '<input type="search" class="t-cm-input" data-grid-search="' + g.id + '" aria-label="' + esc(g.searchLabel || 'Search ' + g.title.toLowerCase()) + '" placeholder="' + esc(g.placeholder || 'Search') + '" value="' + esc(g.state.q) + '">' +
      '<button class="dgs-clear" type="button" aria-label="Clear search" data-grid-clear="' + g.id + '"><svg viewBox="0 0 18 18" aria-hidden="true"><use href="#dg-close"/></svg></button></div>' + (g.tools || '') + '</div>' +
      '<div class="dg-scroll"><table id="' + g.id + '-tbl" aria-labelledby="' + g.id + '-title"><colgroup>' +
      g.cols.map(function (c) { return '<col data-col="' + c.k + '" style="width:' + (c.w || (c.num ? 168 : c.k === 'status' || c.k === 'severity' || c.k === 'category' ? 184 : /date|raised|opened|expiry|maturity|valueDate/.test(c.k) ? 152 : 168)) + 'px">'; }).join('') + '</colgroup><thead><tr class="cols">' + cols + '</tr></thead><tbody id="' + g.id + '-body"></tbody></table></div>' +
      '<div class="dg-foot"><span class="dg-range t-cm-caption" id="' + g.id + '-range"></span><div class="dg-pp"><label class="t-cm-caption" for="' + g.id + '-pp">Rows per page</label>' +
      '<select id="' + g.id + '-pp" class="t-cm-caption" data-grid-size="' + g.id + '">' + [10, 25, 50].map(function (n) { return '<option value="' + n + '"' + (n === g.state.size ? ' selected' : '') + '>' + n + '</option>'; }).join('') + '</select></div>' +
      '<nav class="dgpg" aria-label="' + esc(g.title) + ' pages"><ul id="' + g.id + '-pg"></ul></nav></div></div></div>';
    renderGrid(g.id);
  }
  function gridRows(g) {
    var rows = g.rows(), qv = g.state.q.trim().toLowerCase();
    if (qv) { rows = rows.filter(function (r) { return g.text(r).toLowerCase().indexOf(qv) > -1; }); }
    if (g.state.sort) {
      var col = g.cols.filter(function (c) { return c.k === g.state.sort; })[0], d = g.state.dir === 'ascending' ? 1 : -1;
      var val = col && col.val ? col.val : function (r) { return r[g.state.sort]; };
      rows = rows.slice().sort(function (a, b) { var x = val(a), y = val(b); return (typeof x === 'number' ? x - y : String(x).localeCompare(String(y))) * d; });
    }
    return rows;
  }
  function renderGrid(id) {
    var g = GRIDS[id], rows = gridRows(g), total = rows.length, pages = Math.max(1, Math.ceil(total / g.state.size));
    g.state.page = Math.min(Math.max(1, g.state.page), pages);
    var start = (g.state.page - 1) * g.state.size, pr = rows.slice(start, start + g.state.size);
    g.visible = rows;
    $$('#' + id + ' th[data-key]').forEach(function (th) { if (th.hasAttribute('aria-sort')) { th.setAttribute('aria-sort', th.getAttribute('data-key') === g.state.sort ? g.state.dir : 'none'); } });
    $('#' + id + '-count').textContent = total + ' result' + (total === 1 ? '' : 's');
    $('#' + id + '-range').textContent = total ? (start + 1) + '–' + Math.min(start + g.state.size, total) + ' of ' + total : '0 of 0';
    var body = $('#' + id + '-body');
    if (!pr.length) {
      body.innerHTML = '<tr><td colspan="' + g.cols.length + '" class="dg-empty"><span class="why t-cm-label">' + esc(g.empty || 'No records match these filters') + '</span><span class="try t-cm-caption">Widen the date range, change entity or region, or clear the search.</span>' +
        '<button class="clearbtn t-cm-button" type="button" data-grid-clear="' + id + '">Clear search</button></td></tr>';
    } else {
      body.innerHTML = pr.map(function (r) {
        return '<tr data-grid-row="' + id + '" data-id="' + esc(r.id) + '" tabindex="0" aria-label="' + esc(g.rowLabel ? g.rowLabel(r) : 'Open ' + r.id) + '">' + g.cols.map(function (c) {
          return '<td' + (c.num ? ' class="num"' : '') + '>' + (c.html ? c.html(r) : '<span class="' + (c.num ? 't-cm-figure-5' : 't-cm-label') + '">' + esc(c.fmt ? c.fmt(r) : r[c.k]) + '</span>') + '</td>';
        }).join('') + '</tr>';
      }).join('');
    }
    var h = '<li><button class="pbtn" type="button" aria-label="Previous page" ' + (g.state.page === 1 ? 'disabled' : '') + ' data-grid-go="prev" data-grid="' + id + '"><svg viewBox="0 0 18 18" aria-hidden="true"><use href="#dg-cleft"/></svg></button></li>';
    for (var p = 1; p <= pages; p++) {
      var cur = p === g.state.page;
      h += '<li><button class="pbtn ' + (cur ? 't-cm-button' : 't-cm-label') + '" type="button" data-grid-go="' + p + '" data-grid="' + id + '" ' + (cur ? 'aria-current="page" aria-label="Page ' + p + ', current page"' : 'aria-label="Page ' + p + '"') + '>' + p + '</button></li>';
    }
    h += '<li><button class="pbtn" type="button" aria-label="Next page" ' + (g.state.page === pages ? 'disabled' : '') + ' data-grid-go="next" data-grid="' + id + '"><svg viewBox="0 0 18 18" aria-hidden="true"><use href="#dg-cright"/></svg></button></li>';
    $('#' + id + '-pg').innerHTML = h;
    PS[id + '.q'] = g.state.q; PS[id + '.sort'] = g.state.sort; PS[id + '.dir'] = g.state.dir; PS[id + '.page'] = g.state.page; PS[id + '.size'] = g.state.size;
    persist();
  }
  function exportGrid(id, name) {
    var g = GRIDS[id];
    csv(name, [g.cols.map(function (c) { return c.label; })].concat(g.visible.map(function (r) { return g.cols.map(function (c) { return c.csv ? c.csv(r) : c.fmt ? c.fmt(r) : r[c.k]; }); })));
  }

  /* ---------- filter toolbar (Filter-toolbar-bar: dd boxed menus, chips, clear all, status line) */
  function ddOptions(which) {
    if (which === 'entity') {
      return [{ v: 'all', l: 'All entities' }].concat(D.ENTITIES.filter(function (e) { return S.region === 'all' || e.region === S.region; }).map(function (e) { return { v: e.id, l: e.name }; }));
    }
    if (which === 'region') { return [{ v: 'all', l: 'All regions' }].concat(D.REGIONS.map(function (r) { return { v: r.id, l: r.name }; })); }
    return [{ v: '7', l: 'Last 7 days' }, { v: '14', l: 'Last 14 days' }, { v: '30', l: 'Last 30 days' }];
  }
  function ddValue(which) { return which === 'entity' ? S.entity : which === 'region' ? S.region : String(S.days); }
  function renderMenu(which) {
    var m = $('#dd-' + which + '-m'); if (!m) { return; }
    var cur = ddValue(which), opts = ddOptions(which);
    m.innerHTML = opts.map(function (o) {
      return '<li class="opt t-cm-label" role="option" aria-selected="' + (o.v === cur) + '" tabindex="-1" data-dd="' + which + '" data-value="' + esc(o.v) + '">' + esc(o.l) + ' <svg data-bespoke="neutral selection checkmark (library only has teal status ticks)" class="tick" viewBox="0 0 18 18" aria-hidden="true"><path d="M3.5 9.5 L7.5 13.5 L14.5 5"/></svg></li>';
    }).join('');
    var sel = opts.filter(function (o) { return o.v === cur; })[0];
    $('#dd-' + which + ' .ddval').textContent = sel ? sel.l : opts[0].l;
  }
  function renderFilterContext() {
    ['entity', 'region', 'days'].forEach(renderMenu);
    var chips = [];
    if (S.region !== 'all') { chips.push({ k: 'region', l: 'Region: ' + regionName(S.region) }); }
    if (S.entity !== 'all') { chips.push({ k: 'entity', l: 'Entity: ' + D.ENT[S.entity].short }); }
    if (S.days !== 30) { chips.push({ k: 'days', l: 'Dates: last ' + S.days + ' days' }); }
    $$('[data-scope-label]').forEach(function (el) { el.textContent = scopeLabel(); });
    var outer = $('#ftb'); if (!outer) { return; }
    outer.setAttribute('data-ftb-state', chips.length ? 'filtered' : 'no-filters');
    $('#ftb-chips .row').innerHTML = chips.map(function (c) {
      return '<span class="tag t-cm-caption"><span class="lbl">' + esc(c.l) + '</span><button class="x" type="button" aria-label="Remove filter: ' + esc(c.l) + '" data-chip="' + c.k + '"><svg viewBox="0 0 18 18" aria-hidden="true"><use href="#ic-close"/></svg></button></span>';
    }).join('');
    var n = scopedEntities().length;
    $('#ftb-count').textContent = n; $('#ftb-total').textContent = D.ENTITIES.length;
    $$('[data-scope-label]').forEach(function (el) { el.textContent = scopeLabel(); });
  }
  function setFilter(k, v) {
    if (k === 'entity') { S.entity = v; if (v !== 'all' && S.region !== 'all' && D.ENT[v].region !== S.region) { S.region = 'all'; } }
    if (k === 'region') { S.region = v; if (S.entity !== 'all' && v !== 'all' && D.ENT[S.entity].region !== v) { S.entity = 'all'; } }
    if (k === 'days') { S.days = +v; }
    Object.keys(GRIDS).forEach(function (id) { GRIDS[id].state.page = 1; });
    persist(); renderFilterContext(); rerender();
  }
  function closeMenus(except) {
    $$('.ftb .menu[data-open="true"], .ceo-menu[data-open="true"]').forEach(function (m) { if (m !== except) { m.setAttribute('data-open', 'false'); var t = document.querySelector('[aria-controls="' + m.id + '"]'); if (t) { t.setAttribute('aria-expanded', 'false'); } } });
  }

  /* ---------- theme (data-theme on <html>; data-apollo-theme stays "common") */
  function applyTheme(t) {
    S.theme = t; document.documentElement.setAttribute('data-theme', t);
    $$('[data-theme-btn]').forEach(function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-theme-btn') === t)); });
    segAll(); persist();
    setTimeout(function () { window.dispatchEvent(new Event('resize')); }, 30);
  }
  /* Segmented-control's sliding indicator (the snippet's own moveInd, extended to run on any seg) */
  function moveInd(seg) {
    var ind = seg.querySelector('.ind'); if (!ind) { return; }
    var a = seg.querySelector('button[aria-pressed="true"]'); if (!a) { return; }
    var sr = seg.getBoundingClientRect(), br = a.getBoundingClientRect();
    ind.style.left = (br.left - sr.left - seg.clientLeft) + 'px'; ind.style.width = br.width + 'px';
  }
  function segAll() { $$('.seg').forEach(moveInd); }

  /* ---------- the one delegated listener set (rule 14: controls rendered from DATA do not exist
     when a per-element listener would run) */
  var rerender = function () {};
  document.addEventListener('click', function (e) {
    var t = e.target;
    var trig = t.closest('.ftb .trigger, [data-menu-trigger]');
    if (trig) {
      var m = document.getElementById(trig.getAttribute('aria-controls')), open = m.getAttribute('data-open') === 'true';
      closeMenus(m); m.setAttribute('data-open', String(!open)); trig.setAttribute('aria-expanded', String(!open));
      if (!open) { var s = m.querySelector('[aria-selected="true"]') || m.querySelector('.opt'); if (s) { s.focus(); } }
      return;
    }
    var opt = t.closest('.opt[data-dd]');
    if (opt) { var w = opt.getAttribute('data-dd'); closeMenus(); setFilter(w, opt.getAttribute('data-value')); var tr = $('#dd-' + w + ' .trigger'); if (tr) { tr.focus(); } toast('Showing ' + scopeLabel(), 'info'); return; }
    if (!t.closest('.menu, .ceo-menu')) { closeMenus(); }
    var chip = t.closest('[data-chip]'); if (chip) { setFilter(chip.getAttribute('data-chip'), chip.getAttribute('data-chip') === 'days' ? '30' : 'all'); var c1 = $('#dd-entity .trigger'); if (c1) { c1.focus(); } return; }
    if (t.closest('[data-ftb-clear]')) { S.entity = 'all'; S.region = 'all'; S.days = 30; persist(); renderFilterContext(); rerender(); toast('Filters cleared', 'info'); return; }
    var th = t.closest('[data-theme-btn]'); if (th) { applyTheme(th.getAttribute('data-theme-btn')); return; }
    var sb = t.closest('button[data-sort]');
    if (sb) { var g = GRIDS[sb.getAttribute('data-grid')], k = sb.getAttribute('data-sort'); g.state.dir = g.state.sort === k && g.state.dir === 'ascending' ? 'descending' : 'ascending'; g.state.sort = k; renderGrid(g.id); var again = $('#' + g.id + ' button[data-sort="' + k + '"]'); if (again) { again.focus(); } return; }
    var go = t.closest('[data-grid-go]');
    if (go) { var gg = GRIDS[go.getAttribute('data-grid')], v = go.getAttribute('data-grid-go'); gg.state.page = v === 'prev' ? gg.state.page - 1 : v === 'next' ? gg.state.page + 1 : +v; renderGrid(gg.id); var cp = $('#' + gg.id + '-pg [aria-current="page"]'); if (cp) { cp.focus(); } return; }
    var gc = t.closest('[data-grid-clear]');
    if (gc) { var g2 = GRIDS[gc.getAttribute('data-grid-clear')]; g2.state.q = ''; var inp = $('[data-grid-search="' + g2.id + '"]'); if (inp) { inp.value = ''; inp.focus(); } renderGrid(g2.id); return; }
    var row = t.closest('tr[data-grid-row]');
    if (row && !t.closest('button, a, input')) { var g3 = GRIDS[row.getAttribute('data-grid-row')]; if (g3.open) { g3.open(row.getAttribute('data-id')); } return; }
    var ma = t.closest('[data-modal-act]'); if (ma) { var r = $('#modal').__on(ma.getAttribute('data-modal-act')); if (r !== false) { closeModal(); } return; }
    if (t.closest('#modal .close')) { closeModal(); return; }
    if (t.closest('#modal') && t.id === 'modal') { closeModal(); return; }
    var da = t.closest('[data-drawer-act]'); if (da) { $('#drawer').__on(da.getAttribute('data-drawer-act')); return; }
    if (t.closest('#drawer .close') || t.id === 'scrim') { closeDrawer(); return; }
    var tc = t.closest('[data-action="toast-close"]'); if (tc) { var to = tc.closest('.toast'); if (to && to.__close) { to.__close(); } return; }
    var kt = t.closest('[data-action="kpi-table"]'); if (kt) { kpiTable(kt.getAttribute('data-kpi')); return; }
    var nt = t.closest('[data-navtoggle]');
    if (nt) { var sn = $('#nav-main'), rail = !sn.classList.contains('is-rail'); sn.classList.toggle('is-rail', rail); nt.setAttribute('aria-expanded', String(!rail)); nt.setAttribute('aria-label', rail ? 'Expand navigation' : 'Collapse navigation'); S.nav = rail ? 'rail' : 'auto'; persist(); setTimeout(function () { window.dispatchEvent(new Event('resize')); segAll(); }, 250); return; }
    if (t.closest('[data-menu="shell"]')) { $('#sheet').classList.add('open'); $('#shell-scrim').classList.add('open'); var b = $('[data-menu="shell"]'); b.setAttribute('aria-expanded', 'true'); $('#sheet').focus(); return; }
    if (t.closest('[data-close="shell"]') || t.id === 'shell-scrim') { $('#sheet').classList.remove('open'); $('#shell-scrim').classList.remove('open'); var b2 = $('[data-menu="shell"]'); b2.setAttribute('aria-expanded', 'false'); b2.focus(); return; }
    var ex = t.closest('[data-export]'); if (ex) { exportGrid(ex.getAttribute('data-export'), ex.getAttribute('data-file')); return; }
    var sg = t.closest('.seg button'); if (sg && !sg.hasAttribute('data-theme-btn')) { var seg = sg.closest('.seg'); $$('button', seg).forEach(function (x) { x.setAttribute('aria-pressed', String(x === sg)); }); moveInd(seg); }
    if (APP.onClick) { APP.onClick(e); }
  });
  document.addEventListener('keydown', function (e) {
    var t = e.target;
    if (e.key === 'Escape') {
      if ($('#modal.open')) { closeModal(); return; }
      if ($('#drawer.open')) { closeDrawer(); return; }
      var om = $('.menu[data-open="true"], .ceo-menu[data-open="true"]'); if (om) { closeMenus(); var tg = document.querySelector('[aria-controls="' + om.id + '"]'); if (tg) { tg.focus(); } return; }
      if ($('#sheet.open')) { $('#sheet').classList.remove('open'); $('#shell-scrim').classList.remove('open'); return; }
    }
    if ($('#modal.open')) { trap(e, $('#modal .dialog')); }
    else if ($('#drawer.open')) { trap(e, $('#drawer')); }
    if (t.matches && t.matches('.opt')) {
      var list = $$('.opt', t.closest('.menu, .ceo-menu')), i = list.indexOf(t);
      if (e.key === 'ArrowDown') { e.preventDefault(); (list[i + 1] || list[0]).focus(); }
      if (e.key === 'ArrowUp') { e.preventDefault(); (list[i - 1] || list[list.length - 1]).focus(); }
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); t.click(); }
    }
    if (t.matches && t.matches('tr[data-grid-row]') && (e.key === 'Enter' || e.key === ' ')) { e.preventDefault(); var g = GRIDS[t.getAttribute('data-grid-row')]; if (g.open) { g.open(t.getAttribute('data-id')); } }
    if (APP.onKey) { APP.onKey(e); }
  });
  var searchT = null;
  document.addEventListener('input', function (e) {
    var t = e.target;
    if (t.matches('[data-grid-search]')) { clearTimeout(searchT); searchT = setTimeout(function () { var g = GRIDS[t.getAttribute('data-grid-search')]; g.state.q = t.value; g.state.page = 1; renderGrid(g.id); }, 160); }
    if (t.matches('textarea[maxlength]')) { var c = document.getElementById(t.id + '-count'); if (c) { c.textContent = t.value.length + '/' + t.getAttribute('maxlength'); } }
    var f = t.closest('[data-field]'); if (f) { f.classList.remove('is-error'); var em = f.querySelector('.err-msg'); if (em) { em.hidden = true; } t.removeAttribute('aria-invalid'); }
  });
  document.addEventListener('change', function (e) {
    var t = e.target;
    if (t.matches('[data-grid-size]')) { var g = GRIDS[t.getAttribute('data-grid-size')]; g.state.size = +t.value; g.state.page = 1; renderGrid(g.id); }
    var f = t.closest('[data-field]'); if (f) { f.classList.remove('is-error'); var em = f.querySelector('.err-msg'); if (em) { em.hidden = true; } }
    if (APP.onChange) { APP.onChange(e); }
  });
  window.addEventListener('resize', function () { segAll(); });

  /* ---------- validation helpers (Input-fields / Textarea / Selection-controls error states) */
  function fail(id, msg) {
    var el = document.getElementById(id), f = el ? el.closest('[data-field]') : document.querySelector('[data-field="' + id + '"]');
    if (!f) { return; }
    f.classList.add('is-error'); if (el) { el.setAttribute('aria-invalid', 'true'); }
    var em = f.querySelector('.err-msg') || f.parentNode.querySelector('.err-msg'); if (em) { em.hidden = false; var p = em.querySelector('p') || em; p.textContent = msg; if (el) { el.setAttribute('aria-describedby', ((el.getAttribute('aria-describedby') || '') + ' ' + p.id).trim()); } }
  }
  function val(id) { var el = document.getElementById(id); return el ? (el.type === 'checkbox' ? el.checked : el.value.trim()) : ''; }

  /* ---------- boot */
  function boot(pageRender) {
    rerender = pageRender || function () {};
    document.documentElement.setAttribute('data-theme', S.theme);
    $$('[data-theme-btn]').forEach(function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-theme-btn') === S.theme)); });
    if (S.nav === 'rail') { var sn = $('#nav-main'); sn.classList.add('is-rail'); var nt = $('[data-navtoggle]'); nt.setAttribute('aria-expanded', 'false'); nt.setAttribute('aria-label', 'Expand navigation'); }
    var np = $('#nav-pay-count'); if (np) { var c = calc.payments().filter(function (p) { return p.status === 'Awaiting your approval'; }).length; np.textContent = c; np.setAttribute('aria-label', c + ' payments awaiting your approval'); np.hidden = !c; }
    renderFilterContext(); decorateLinks(); rerender(); segAll();
    requestAnimationFrame(function () { segAll(); window.dispatchEvent(new Event('resize')); });
    if (APP.afterBoot) { APP.afterBoot(); }
    persist();
  }

  return { D: D, S: S, PS: PS, W: W, F: F, H: H, esc: esc, $: $, $$: $$, calc: calc, inScope: inScope, scopedEntities: scopedEntities, days: days, dayIdx: dayIdx,
    inWindow: inWindow, scopeLabel: scopeLabel, regionName: regionName, toast: toast, openModal: openModal, closeModal: closeModal, openDrawer: openDrawer,
    closeDrawer: closeDrawer, openForm: openForm, renderKpis: renderKpis, mountChart: mountChart, drawChart: drawChart, emptyChart: emptyChart, grid: grid, renderGrid: renderGrid,
    GRIDS: GRIDS, csv: csv, saveWork: saveWork, persist: persist, fail: fail, val: val, boot: boot, segAll: segAll, decorateLinks: decorateLinks, PAGE: PAGE };
}());
