/* CEO international banking prototype — the authored wiring (generate-from-canon rule 2a).
   Reads window.DATA (data.js). Charts are drawn by the pack's engine (dvRender), never by hand.
   State: shared filters, theme, per-grid sort/page, and every simulated workflow outcome persist
   in localStorage; filters and the open record are mirrored in the URL so a view is shareable. */
(function () {
  'use strict';
  var D = window.DATA, KEY = 'apollo-ceo-proto-v1', PAGE = document.body.getAttribute('data-page');
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* ------------------------------------------------------------------ STORE + URL (rule 15) */
  function readStore() { try { return JSON.parse(localStorage.getItem(KEY)) || {}; } catch (e) { return {}; } }
  var S = readStore();
  function init(k, v) { if (S[k] === undefined || S[k] === null) { S[k] = v; } }
  init('filters', { region: 'all', entity: 'all', days: 30 }); init('grids', {}); init('decisions', {}); init('acks', {});
  init('newRequests', []); init('replies', {}); init('read', {}); init('runs', {}); init('deals', []); init('drawdowns', []);
  init('prefs', { approvals: true, exceptions: true, messages: true, digest: false }); init('theme', 'light'); init('q', {}); init('view', {});
  function save() { try { localStorage.setItem(KEY, JSON.stringify(S)); } catch (e) { /* private mode: state lives for this page only */ } }
  var P = new URLSearchParams(location.search);
  var REG_OK = ['all'].concat(D.regions), ENT_OK = ['all'].concat(D.entities.map(function (e) { return e.id; }));
  if (P.has('region') && REG_OK.indexOf(P.get('region')) >= 0) { S.filters.region = P.get('region'); }
  if (P.has('entity') && ENT_OK.indexOf(P.get('entity')) >= 0) { S.filters.entity = P.get('entity'); }
  if (P.has('days') && ['7', '14', '30'].indexOf(P.get('days')) >= 0) { S.filters.days = +P.get('days'); }
  if (P.has('q')) { S.q[PAGE] = P.get('q'); }
  var EXTRA = {};                                           /* page-level URL filters: status, ccy, id */
  ['status', 'ccy', 'id'].forEach(function (k) { if (P.has(k)) { EXTRA[k] = P.get(k); } });
  save();
  function syncURL() {
    var q = new URLSearchParams(), f = S.filters;
    if (f.region !== 'all') { q.set('region', f.region); }
    if (f.entity !== 'all') { q.set('entity', f.entity); }
    if (+f.days !== 30) { q.set('days', f.days); }
    if (S.q[PAGE]) { q.set('q', S.q[PAGE]); }
    Object.keys(EXTRA).forEach(function (k) { if (EXTRA[k]) { q.set(k, EXTRA[k]); } });
    var s = q.toString();
    try { history.replaceState(null, '', location.pathname + (s ? '?' + s : '') + location.hash); } catch (e) { /* file: origins may refuse */ }
    /* carry the shared filters on every masthead link, so a copied link reproduces the view */
    var carry = new URLSearchParams();
    if (f.region !== 'all') { carry.set('region', f.region); }
    if (f.entity !== 'all') { carry.set('entity', f.entity); }
    if (+f.days !== 30) { carry.set('days', f.days); }
    $$('.sh-nav a').forEach(function (a) { var base = a.getAttribute('href').split('?')[0]; a.setAttribute('href', base + (carry.toString() ? '?' + carry : '')); });
  }

  /* ------------------------------------------------------------------ APPLY PERSISTED OUTCOMES */
  D.payments.forEach(function (p) { var d = S.decisions[p.id]; if (d) { p.status = d.status; p.audit = p.audit.concat(d.audit || []); } });
  D.exceptions.forEach(function (x) { var a = S.acks[x.id]; if (a) { x.status = 'Acknowledged'; x.audit = x.audit.concat(a); } });
  D.requests = S.newRequests.concat(D.requests);
  D.messages.forEach(function (m) { if (S.read[m.id]) { m.read = true; } m.thread = S.replies[m.id] || []; });
  D.deals = S.deals.concat(D.deals);
  D.reports.forEach(function (r) { var n = S.runs[r.id]; if (n) { r.runs += n.count; r.lastRun = n.last; } });

  /* ------------------------------------------------------------------ SCOPE + FORMAT */
  function inScope(eid) { var e = D.ent(eid), f = S.filters; return !!e && (f.entity === 'all' || f.entity === eid) && (f.region === 'all' || e.region === f.region); }
  function nDays() { return +S.filters.days || 30; }
  function w0() { return 30 - nDays(); }
  function inWin(date) { return date >= D.days[w0()] && date <= D.days[29]; }
  function win(a) { return a.slice(w0()); }
  var MON = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  function dt(s) { var d = new Date(s + 'T00:00:00Z'); return d.getUTCDate() + ' ' + MON[d.getUTCMonth()] + ' ' + d.getUTCFullYear(); }
  function dd(s) { var d = new Date(s + 'T00:00:00Z'); return d.getUTCDate() + ' ' + MON[d.getUTCMonth()]; }
  function dayLabels() { var ds = win(D.days); return ds.map(function (s) { return nDays() > 14 ? String(+s.slice(8)) : dd(s); }); }
  function periodText() { return dd(D.days[w0()]) + ' to ' + dt(D.days[29]); }
  var nf2 = new Intl.NumberFormat('en-GB', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  var nf0 = new Intl.NumberFormat('en-GB', { maximumFractionDigits: 0 });
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function mm(v) { return Math.round(v / 1e5) / 10; }                     /* GBP -> £m, 1 dp, for chart values */
  function short(v) {                                                      /* KPI figure without the symbol */
    var a = Math.abs(v);
    return a >= 1e9 ? (a / 1e9).toFixed(2) + 'bn' : a >= 1e6 ? (a / 1e6).toFixed(1) + 'm' : a >= 1e3 ? (a / 1e3).toFixed(0) + 'k' : a.toFixed(0);
  }
  function gbpS(v) { return (v < 0 ? '−' : '') + '£' + short(v); }
  function gbp(v) { return (v < 0 ? '−' : '') + '£' + nf2.format(Math.abs(v)); }
  function money(v, c) { return (v < 0 ? '−' : '') + c + ' ' + nf2.format(Math.abs(v)); }
  function sum(a, f) { var t = 0; for (var i = 0; i < a.length; i++) { t += f ? f(a[i]) : a[i]; } return t; }
  function pct(a, b) { return b ? (a - b) / Math.abs(b) * 100 : 0; }
  function entName(id) { var e = D.ent(id); return e ? e.name : id; }

  /* ------------------------------------------------------------------ THEME (data-theme on <html>) */
  function applyTheme(t) {
    S.theme = t === 'dark' ? 'dark' : 'light'; save();
    document.documentElement.setAttribute('data-theme', S.theme);
    $$('[data-theme-set]').forEach(function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-theme-set') === S.theme)); });
    $$('.seg').forEach(moveInd);
  }

  /* ------------------------------------------------------------------ SEGMENTED INDICATOR (Segmented-control grammar) */
  function moveInd(seg) {
    var ind = seg.querySelector('.ind'); if (!ind) { return; }
    var a = seg.querySelector('button[aria-pressed="true"]'); if (!a) { return; }
    var sr = seg.getBoundingClientRect(), br = a.getBoundingClientRect();
    if (!sr.width) { return; }
    ind.style.left = (br.left - sr.left - seg.clientLeft) + 'px'; ind.style.width = br.width + 'px';   /* Segmented-control's own rule: left, not transform */
  }

  /* ------------------------------------------------------------------ DROPDOWNS (Dropdown grammar: menu[data-open]) */
  function wireDD(dd, onChoose) {
    var trig = dd.querySelector('.trigger'), menu = dd.querySelector('.menu'), val = dd.querySelector('.ddval');
    function opts() { return $$('[role=option]', menu); }
    function open(o) {
      menu.setAttribute('data-open', String(o)); trig.setAttribute('aria-expanded', String(o));
      if (o) { var sel = opts().filter(function (x) { return x.getAttribute('aria-selected') === 'true'; })[0] || opts()[0]; if (sel) { sel.focus(); } }
    }
    function choose(o) {
      var v = o.getAttribute('data-value');
      if (onChoose(v, o) === false) { open(false); trig.focus(); return; }
      if (!dd.hasAttribute('data-no-latch')) { opts().forEach(function (x) { x.setAttribute('aria-selected', String(x === o)); }); val.textContent = o.textContent.trim(); }
      open(false); trig.focus();
    }
    trig.addEventListener('click', function () { open(menu.getAttribute('data-open') !== 'true'); });
    trig.addEventListener('keydown', function (e) { if (['ArrowDown', 'Enter', ' '].indexOf(e.key) >= 0) { e.preventDefault(); open(true); } });
    menu.addEventListener('click', function (e) { var o = e.target.closest('[role=option]'); if (o) { choose(o); } });
    menu.addEventListener('keydown', function (e) {
      var o = e.target.closest('[role=option]'); if (!o) { return; }
      var all = opts(), i = all.indexOf(o);
      if (e.key === 'ArrowDown') { e.preventDefault(); all[(i + 1) % all.length].focus(); }
      else if (e.key === 'ArrowUp') { e.preventDefault(); all[(i - 1 + all.length) % all.length].focus(); }
      else if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); choose(o); }
      else if (e.key === 'Escape') { e.preventDefault(); open(false); trig.focus(); }
    });
    dd.__set = function (v) {
      opts().forEach(function (x) { var on = x.getAttribute('data-value') === String(v); x.setAttribute('aria-selected', String(on)); if (on) { val.textContent = x.textContent.trim(); } });
    };
    return dd;
  }
  document.addEventListener('click', function (e) {
    $$('.dd').forEach(function (d) { if (!d.contains(e.target)) { var m = d.querySelector('.menu'), t = d.querySelector('.trigger'); if (m) { m.setAttribute('data-open', 'false'); } if (t) { t.setAttribute('aria-expanded', 'false'); } } });
  });

  /* ------------------------------------------------------------------ TOAST (Toast grammar) */
  var ICON = { ok: 'i-success', info: 'i-info', warn: 'i-warning' };
  function toast(kind, msg) {
    var r = $('#toastRegion'); if (!r) { return; }
    var t = document.createElement('div');
    t.className = 'toast ' + kind; t.setAttribute('role', 'status'); t.setAttribute('data-carries', 'symbol label');
    t.innerHTML = '<span class="ic"><svg aria-hidden="true"><use href="#' + ICON[kind] + '"/></svg></span><p class="msg t-ed-body">' + esc(msg) +
      '</p><button class="x" type="button" aria-label="Dismiss message"><svg aria-hidden="true"><use href="#i-close"/></svg></button>';
    r.appendChild(t);
    var gone = function () { t.classList.add('leaving'); setTimeout(function () { if (t.parentNode) { t.parentNode.removeChild(t); } }, 220); };
    var timer = setTimeout(gone, 6000);
    t.addEventListener('mouseenter', function () { clearTimeout(timer); });
    t.addEventListener('mouseleave', function () { timer = setTimeout(gone, 3000); });
    t.querySelector('.x').addEventListener('click', gone);
  }

  /* ------------------------------------------------------------------ INERT BACKGROUND (Drawer / Modals open order) */
  function bg() { var w = $('.cn-template-dashboard-bento'); return $$(':scope > header, :scope > main, :scope > footer', w); }
  function setInert(on) { bg().forEach(function (el) { el.inert = on; if (on) { el.setAttribute('aria-hidden', 'true'); } else { el.removeAttribute('aria-hidden'); } }); }
  function focusables(root) { return $$('button,a[href],input,select,textarea,[tabindex]:not([tabindex="-1"])', root).filter(function (el) { return !el.disabled && el.offsetParent !== null; }); }

  /* ------------------------------------------------------------------ DRAWER */
  var Dr = { opener: null, onClose: null, isOpen: false };
  function drawerOpen(title, bodyHTML, footHTML, after) {
    var sheet = $('#sheet'), scrim = $('#scrim');
    Dr.opener = Dr.isOpen ? Dr.opener : document.activeElement;
    $('#dtitle').textContent = title; $('#dbody').innerHTML = bodyHTML; $('#dfoot').innerHTML = footHTML || '';
    $('#dbody').scrollTop = 0;
    scrim.classList.add('open'); sheet.classList.add('open'); Dr.isOpen = true;
    if (after) { after(sheet); }
    requestAnimationFrame(function () { requestAnimationFrame(function () {           /* 1 show · 2 two frames · 3 focus in · 4 then inert */
      var f = focusables(sheet); if (f.length) { (f[1] || f[0]).focus(); }
      setInert(true);
    }); });
  }
  function drawerClose() {
    if (!Dr.isOpen) { return; }
    $('#scrim').classList.remove('open'); $('#sheet').classList.remove('open'); Dr.isOpen = false; setInert(false);
    if (EXTRA.id) { delete EXTRA.id; syncURL(); }
    if (Dr.opener && document.contains(Dr.opener)) { Dr.opener.focus(); }
    if (Dr.onClose) { var f = Dr.onClose; Dr.onClose = null; f(); }
  }

  /* ------------------------------------------------------------------ MODAL (Modals grammar) — returns a promise */
  var Md = { resolve: null, opener: null };
  function confirmModal(title, text, label) {
    return new Promise(function (res) {
      Md.resolve = res; Md.opener = document.activeElement;
      $('#mtitle').textContent = title; $('#mbody').textContent = text; $('#mconfirm').textContent = label || 'Confirm';
      $('#overlay').classList.add('open');
      requestAnimationFrame(function () { requestAnimationFrame(function () { $('#mconfirm').focus(); }); });
    });
  }
  function modalClose(v) {
    if (!Md.resolve) { return; }
    $('#overlay').classList.remove('open'); var r = Md.resolve; Md.resolve = null;
    if (Md.opener && document.contains(Md.opener)) { Md.opener.focus(); }
    r(v);
  }

  document.addEventListener('keydown', function (e) {
    if (Md.resolve) {
      if (e.key === 'Escape') { e.preventDefault(); modalClose(false); return; }
      if (e.key === 'Tab') { var mf = focusables($('#overlay')), ma = mf[0], mz = mf[mf.length - 1];
        if (e.shiftKey && document.activeElement === ma) { e.preventDefault(); mz.focus(); } else if (!e.shiftKey && document.activeElement === mz) { e.preventDefault(); ma.focus(); } }
      return;
    }
    if (Dr.isOpen) {
      if (e.key === 'Escape') { var openMenu = $('#sheet .menu[data-open="true"]'); if (!openMenu) { e.preventDefault(); drawerClose(); } return; }
      if (e.key === 'Tab') { var f = focusables($('#sheet')), a = f[0], z = f[f.length - 1];
        if (e.shiftKey && document.activeElement === a) { e.preventDefault(); z.focus(); } else if (!e.shiftKey && document.activeElement === z) { e.preventDefault(); a.focus(); } }
    }
  });

  /* ------------------------------------------------------------------ FORM PARTS (Input-fields / Textarea / Dropdown / Summary / Timeline grammar) */
  function fInput(id, label, help, value, type) {
    return '<div class="cn-input-fields"><div class="field" id="' + id + '-f"><div class="lbl"><label for="' + id + '">' + esc(label) + '</label></div>' +
      (help ? '<p class="help-text" id="' + id + '-h">' + esc(help) + '</p>' : '') +
      '<div class="box"><input id="' + id + '" type="' + (type || 'text') + '" value="' + esc(value || '') + '"' + (help ? ' aria-describedby="' + id + '-h"' : '') + '></div>' +
      '<div class="err-msg" id="' + id + '-e" hidden><span class="ic" aria-hidden="true"><svg class="icn" viewBox="0 0 18 18"><use href="#i-error"/></svg></span><p></p></div></div></div>';
  }
  function fText(id, label, help, max) {
    return '<div class="cn-textarea"><div class="tx-group" id="' + id + '-f"><div class="tx-lblrow"><label class="t-cm-label" for="' + id + '">' + esc(label) + '</label></div>' +
      '<div class="tx-box"><textarea id="' + id + '" class="t-ed-body" maxlength="' + (max || 300) + '" rows="4" aria-describedby="' + id + '-h ' + id + '-c"></textarea></div>' +
      '<div class="tx-foot"><p class="tx-help t-ed-body-small" id="' + id + '-h">' + esc(help) + '</p><span class="tx-count t-cm-legal" id="' + id + '-c">0/' + (max || 300) + '</span></div>' +
      '<div class="tx-msg" id="' + id + '-e" hidden><span class="ic" aria-hidden="true"><svg class="icn" viewBox="0 0 18 18"><use href="#i-error"/></svg></span><p class="t-ed-body"></p></div></div></div>';
  }
  var TICK = '<svg data-bespoke="neutral selection checkmark (library only has teal status ticks)" class="tick" viewBox="0 0 18 18" aria-hidden="true"><path d="M3.5 9.5 L7.5 13.5 L14.5 5"/></svg>';
  function fSelect(id, label, options, value) {
    var cur = options.filter(function (o) { return o[0] === value; })[0] || options[0];
    return '<div class="cn-dropdown"><div class="dd boxed" id="' + id + '" data-value="' + esc(cur[0]) + '"><label id="' + id + 'L" for="' + id + 'T">' + esc(label) + '</label>' +
      '<button class="trigger" id="' + id + 'T" type="button" role="combobox" aria-haspopup="listbox" aria-expanded="false" aria-controls="' + id + 'M" aria-labelledby="' + id + 'L ' + id + 'T"><span class="ddval">' + esc(cur[1]) + '</span><span class="chev" aria-hidden="true">▾</span></button>' +
      '<ul class="menu" id="' + id + 'M" role="listbox" aria-labelledby="' + id + 'L" tabindex="-1" data-open="false">' +
      options.map(function (o) { return '<li class="opt" role="option" aria-selected="' + (o[0] === cur[0]) + '" tabindex="-1" data-value="' + esc(o[0]) + '">' + esc(o[1]) + ' ' + TICK + '</li>'; }).join('') + '</ul></div></div>';
  }
  function fCheck(id, label) {
    return '<div class="cn-selection-controls"><div class="field"><input type="checkbox" id="' + id + '"><label for="' + id + '"><span class="box"><svg data-bespoke="checkbox tick, animated stroke-draw control glyph" viewBox="0 0 18 18"><path class="tick" d="M3.5 9.5 L7.5 13.5 L14.5 5"/></svg></span> ' + esc(label) + '</label></div></div>';
  }
  function summary(rows) {
    return '<div class="cn-summary"><dl class="summary">' + rows.map(function (r) { return '<div class="summary__row"><dt class="summary__k">' + esc(r[0]) + '</dt><dd class="summary__v">' + esc(r[1]) + '</dd></div>'; }).join('') + '</dl></div>';
  }
  function timeline(title, items) {
    var id = 'tl' + Math.floor(Math.random() * 1e6);
    return '<div class="cn-timeline"><section class="tl" aria-labelledby="' + id + '"><h2 id="' + id + '" class="sr-only">' + esc(title) + '</h2><div class="tl-group"><h3 class="t-cm-caption">' + esc(title) + '</h3><ol class="tl-list">' +
      items.slice().reverse().map(function (a) {
        return '<li class="' + (a.kind || 'inf') + '"><span class="tl-node" aria-hidden="true"></span><span class="tl-line"><span class="tl-title t-cm-ctl-14">' + esc(a.what) + '</span></span>' +
          '<span class="tl-meta"><time class="t-cm-legal">' + esc(a.at) + '</time><span class="t-cm-legal">' + esc(a.who) + '</span></span>' + (a.note ? '<p class="tl-desc t-ed-body-small">' + esc(a.note) + '</p>' : '') + '</li>';
      }).join('') + '</ol></div></section></div>';
  }
  function fieldError(id, msg) {
    var f = $('#' + id + '-f'), e = $('#' + id + '-e'), inp = $('#' + id); if (!f) { return; }
    f.classList.toggle('is-error', !!msg);
    if (e) { e.hidden = !msg; e.querySelector('p').textContent = msg || ''; }
    if (inp) { if (msg) { inp.setAttribute('aria-invalid', 'true'); inp.setAttribute('aria-describedby', id + '-e'); } else { inp.removeAttribute('aria-invalid'); } }
  }
  function wireCounter(id, max) {
    var t = $('#' + id), c = $('#' + id + '-c'); if (!t || !c) { return; }
    t.addEventListener('input', function () { c.textContent = t.value.length + '/' + max; if (t.value.trim()) { fieldError(id, ''); } });
  }
  function ddValue(id) { var d = $('#' + id); return d ? d.getAttribute('data-value') : null; }
  function wireFormDD(sheet) {
    $$('.dd', sheet).forEach(function (d) { if (d.id === 'tfPick' || d.id === 'ddFac') { return; } wireDD(d, function (v) { d.setAttribute('data-value', v); }); });
  }
  function nowStamp() { var d = new Date(); return d.getUTCFullYear() + '-' + String(d.getUTCMonth() + 1).padStart(2, '0') + '-' + String(d.getUTCDate()).padStart(2, '0') + ' ' + String(d.getHours()).padStart(2, '0') + ':' + String(d.getMinutes()).padStart(2, '0'); }
  function dbtn(label, act, kind) { return '<button class="dbtn ' + (kind || 'primary') + ' t-cm-button t-cm-slot" type="button" data-dact="' + act + '">' + esc(label) + '</button>'; }
  function chip(kind, label) { return '<span class="cn-status-indicator"><span class="chip ' + kind + '"><span class="dot" aria-hidden="true"></span>' + esc(label) + '</span></span>'; }
  function statusChip(label) {
    var k = /reject|breach|failed|discrep|high/i.test(label) ? 'err' : /awaiting|pending|open|warning|medium|expir|in progress/i.test(label) ? 'warn' : /released|approved|settled|acknowledged|closed|confirmed|issued|ok|low/i.test(label) ? 'ok' : 'inf';
    return chip(k, label);
  }

  /* ------------------------------------------------------------------ KPI TILE (Kpi-tile grammar, template splice) */
  function kpi(id, o) {
    var t = document.getElementById(id); if (!t) { return; }
    t.querySelector('.amt').innerHTML = '<span>' + esc(o.pre || '') + '</span><span>' + esc(o.val) + '</span>';
    var d = t.querySelector('.delta'), dir = o.dir || 'flat';
    d.className = 'delta' + (dir === 'up' ? ' up' : dir === 'down' ? ' down' : '');
    if (dir === 'flat') { d.removeAttribute('data-carries'); } else { d.setAttribute('data-carries', 'symbol label'); }   /* Stat-card: a flat delta carries no symbol */
    d.innerHTML = (dir === 'flat' ? '' : '<span class="arrow" aria-hidden="true"><svg><use href="#kpi-' + dir + '"/></svg></span>') +
      '<span class="t-cm-figure-6">' + esc(o.delta) + '</span><span class="per t-cm-legal">' + esc(o.per || '') + '</span>';
    var svg = t.querySelector('.spark-inline'), s = o.series;
    if (svg && s && s.length > 1) {
      var lo = Math.min.apply(null, s), hi = Math.max.apply(null, s), sp = hi - lo || 1, pts = [];
      for (var i = 0; i < s.length; i++) { pts.push((3 + i * 194 / (s.length - 1)).toFixed(1) + ',' + (45 - (s[i] - lo) / sp * 42).toFixed(1)); }
      var last = pts[pts.length - 1].split(',');
      svg.setAttribute('data-trend', s[s.length - 1] > s[0] ? 'up' : s[s.length - 1] < s[0] ? 'down' : 'flat');
      svg.innerHTML = '<line class="dv-base" x1="3" y1="45" x2="197" y2="45"/><polyline class="dv-series" points="' + pts.join(' ') + '"/><circle class="dv-end" cx="' + last[0] + '" cy="' + last[1] + '" r="3"/>';
    }
  }
  function deltaOf(a, b, per, unit) {
    var p = pct(a, b), r = Math.round(p * 10) / 10;
    if (Math.abs(r) < 0.05) { return { delta: 'No change', dir: 'flat', per: per }; }
    return { delta: (r > 0 ? '+' : '−') + Math.abs(r).toFixed(1) + (unit || '%') + (r > 0 ? ' up' : ' down'), dir: r > 0 ? 'up' : 'down', per: per };
  }
  function mix(a, b) { for (var k in b) { a[k] = b[k]; } return a; }

  /* ------------------------------------------------------------------ CHARTS — the engine draws, we hand it specs */
  var SHAPES = ['sw-circle', 'sw-square', 'sw-diamond'];
  function draw(id, spec, after) {
    var fig = document.getElementById(id); if (!fig || !window.dvRender) { return; }
    if (spec.type === 'donut' || spec.type === 'pie') { fig.setAttribute('data-total', String(Math.round(sum(spec.series[0].values) * 10) / 10)); }
    try { window.dvRender(fig, spec); } catch (e) { console.error(e); return; }
    var ul = fig.querySelector('ul.dv-leg');
    if (ul) {
      var ring = spec.type === 'donut' || spec.type === 'pie', names = ring ? spec.categories : spec.series.map(function (s) { return s.name; });
      var line = spec.type === 'multiline' || spec.type === 'line';
      var nu = ul.cloneNode(false);                                          /* a fresh host resets dv-legend's cached state */
      nu.innerHTML = names.map(function (n, i) {
        return '<li class="dv-legrow" data-series="' + (i + 1) + '"><span class="dv-leg-sw' + (line ? ' ' + SHAPES[i % 3] : '') + '" role="checkbox" aria-checked="true" tabindex="0" aria-label="Show or hide ' + esc(n) +
          '" style="--sc:var(--data-series-' + ((i % 5) + 1) + ')"></span><button type="button" class="dv-leg-item t-cm-chart-label" data-series="' + (i + 1) + '" aria-pressed="false" aria-label="Isolate ' + esc(n) +
          '"><span class="dv-key t-cm-chart-key">' + 'ABCDEFGH'.charAt(i) + '</span><span class="dv-leg-name">' + esc(n) + '</span></button></li>';
      }).join('') + '<li class="dv-leg-reset-wrap"><button type="button" class="dv-leg-reset t-cm-chart-label" data-for="' + ul.id + '" disabled>Reset</button></li>';
      ul.parentNode.replaceChild(nu, ul);
    }
    if (after) { after(fig); }
  }
  function top(pairs, n, other) {                                          /* keep n categories, fold the rest into "Other" */
    pairs.sort(function (a, b) { return b[1] - a[1]; });
    if (pairs.length <= n) { return pairs; }
    var keep = pairs.slice(0, n - 1), rest = sum(pairs.slice(n - 1), function (p) { return p[1]; });
    keep.push([other || 'Other', rest]); return keep;
  }

  /* ------------------------------------------------------------------ DATA-GRID (Data-grid grammar; lighter: native table, no roving cell focus) */
  var GRIDS = [];
  function Grid(cfg) {
    var root = document.getElementById(cfg.id); if (!root) { return null; }
    var st = S.grids[PAGE + '.' + cfg.id] = S.grids[PAGE + '.' + cfg.id] || { sort: cfg.sort || null, dir: cfg.dir || 'descending', page: 1, size: 10 };
    var body = document.getElementById(cfg.id + '-body'), pp = document.getElementById(cfg.id + '-pp');
    pp.value = String(st.size);
    var view = [];
    function text(r) { return cfg.cols.map(function (c) { return String(c.val ? c.val(r) : r[c.key]); }).join(' ').toLowerCase(); }
    function rows() {
      var q = (S.q[PAGE] || '').trim().toLowerCase(), a = cfg.rows();
      if (q) { a = a.filter(function (r) { return text(r).indexOf(q) >= 0; }); }
      if (st.sort) {
        var c = cfg.cols.filter(function (x) { return x.key === st.sort; })[0];
        if (c) {
          var f = c.sortv || c.val || function (r) { return r[c.key]; }, m = st.dir === 'ascending' ? 1 : -1;
          a = a.slice().sort(function (x, y) { var p = f(x), q2 = f(y); return (p > q2 ? 1 : p < q2 ? -1 : 0) * m; });
        }
      }
      return a;
    }
    function render() {
      view = rows();
      var total = cfg.rows().length, pages = Math.max(1, Math.ceil(view.length / st.size));
      if (st.page > pages) { st.page = pages; }
      var start = (st.page - 1) * st.size, pg = view.slice(start, start + st.size);
      $$('th[data-key]', root).forEach(function (th) { th.setAttribute('aria-sort', th.getAttribute('data-key') === st.sort ? st.dir : 'none'); });
      if (!pg.length) {
        body.innerHTML = '<tr><td colspan="' + cfg.cols.length + '" class="dg-empty"><span class="why t-cm-label">No ' + esc(cfg.noun) + ' match your filters</span>' +
          '<span class="try t-cm-caption">Try removing a filter, or clear them all</span><button class="clearbtn t-cm-button" type="button" data-action="clear-filters">Clear filters</button></td></tr>';
      } else {
        body.innerHTML = pg.map(function (r) {
          return '<tr data-id="' + esc(cfg.key(r)) + '">' + cfg.cols.map(function (c, i) {
            var v = c.cell ? c.cell(r) : '<span class="t-cm-label">' + esc(c.val ? c.val(r) : r[c.key]) + '</span>';
            if (i === 0 && cfg.open) { v = '<a class="tpl-link t-cm-label" href="?id=' + encodeURIComponent(cfg.key(r)) + '" data-open="' + esc(cfg.key(r)) + '" data-grid="' + cfg.id + '">' + esc(c.val ? c.val(r) : r[c.key]) + '</a>'; }
            return '<td' + (c.num ? ' class="num"' : '') + '>' + v + '</td>';
          }).join('') + '</tr>';
        }).join('');
      }
      var cnt = document.getElementById(cfg.id + '-count'); if (cnt) { cnt.textContent = view.length + ' of ' + total + ' ' + cfg.noun; }
      var rg = document.getElementById(cfg.id + '-range'); if (rg) { rg.textContent = view.length ? (start + 1) + '–' + Math.min(start + st.size, view.length) + ' of ' + view.length : '0 of 0'; }
      var ul = document.getElementById(cfg.id + '-pg'), h = '<li><button class="pbtn" type="button" aria-label="Previous page" ' + (st.page === 1 ? 'disabled' : '') + ' data-go="prev"><svg viewBox="0 0 18 18" aria-hidden="true"><use href="#i-cleft"/></svg></button></li>';
      var from = Math.max(1, Math.min(st.page - 2, pages - 4)), to = Math.min(pages, from + 4);
      for (var p = from; p <= to; p++) {
        var cur = p === st.page;
        h += '<li><button class="pbtn ' + (cur ? 't-cm-button' : 't-cm-label') + '" type="button" data-go="' + p + '" ' + (cur ? 'aria-current="page" aria-label="Page ' + p + ', current page"' : 'aria-label="Page ' + p + '"') + '>' + p + '</button></li>';
      }
      h += '<li><button class="pbtn" type="button" aria-label="Next page" ' + (st.page === pages ? 'disabled' : '') + ' data-go="next"><svg viewBox="0 0 18 18" aria-hidden="true"><use href="#i-cright"/></svg></button></li>';
      if (ul) { ul.innerHTML = h; }
      if (cfg.after) { cfg.after(view); }
    }
    $$('th[data-key] .sort', root).forEach(function (b) {
      b.addEventListener('click', function () {
        var k = b.closest('th').getAttribute('data-key');
        if (st.sort !== k) { st.sort = k; st.dir = 'ascending'; } else if (st.dir === 'ascending') { st.dir = 'descending'; } else { st.sort = null; st.dir = 'descending'; }
        st.page = 1; save(); render();
      });
    });
    pp.addEventListener('change', function () { st.size = +pp.value; st.page = 1; save(); render(); });
    root.addEventListener('click', function (e) {
      var b = e.target.closest('.pbtn');
      if (b && !b.disabled) { var g = b.getAttribute('data-go'); st.page = g === 'prev' ? st.page - 1 : g === 'next' ? st.page + 1 : +g; save(); render();
        var nb = root.querySelector('.pbtn[aria-current="page"]'); if (nb) { nb.focus(); } return; }
      var a = e.target.closest('a[data-open]');
      if (a && cfg.open) { e.preventDefault(); var r = cfg.rows().filter(function (x) { return cfg.key(x) === a.getAttribute('data-open'); })[0]; if (r) { EXTRA.id = cfg.key(r); syncURL(); cfg.open(r); } }
    });
    var g = { cfg: cfg, render: render, view: function () { return view.length ? view : rows(); }, find: function (id) { return cfg.rows().filter(function (x) { return cfg.key(x) === id; })[0]; } };
    GRIDS.push(g); render();
    return g;
  }

  /* ------------------------------------------------------------------ EXPORT (a real file, built from the filtered rows) */
  function download(name, text, type) {
    var blob = new Blob([text], { type: type }), a = document.createElement('a');
    a.href = URL.createObjectURL(blob); a.download = name; document.body.appendChild(a); a.click();
    setTimeout(function () { URL.revokeObjectURL(a.href); a.parentNode.removeChild(a); }, 0);
  }
  function toCSV(rows, cols) {
    var q = function (v) { v = String(v === null || v === undefined ? '' : v); return /[",\n]/.test(v) ? '"' + v.replace(/"/g, '""') + '"' : v; };
    return cols.map(function (c) { return q(c[1]); }).join(',') + '\n' + rows.map(function (r) { return cols.map(function (c) { return q(typeof c[0] === 'function' ? c[0](r) : r[c[0]]); }).join(','); }).join('\n');
  }
  function exportGrid(fmt, g) {
    g = g || GRIDS[GRIDS.length - 1]; if (!g) { toast('info', 'Nothing to export on this page.'); return; }
    var rows = g.view(), cols = g.cfg.cols.map(function (c) { return [c.raw || c.val || c.key, c.label]; });
    var stamp = D.asOf + '-' + PAGE;
    if (fmt === 'json') { download('northwind-' + stamp + '.json', JSON.stringify(rows.map(function (r) { var o = {}; cols.forEach(function (c) { o[c[1]] = typeof c[0] === 'function' ? c[0](r) : r[c[0]]; }); return o; }), null, 2), 'application/json'); }
    else { download('northwind-' + stamp + '.csv', toCSV(rows, cols), 'text/csv'); }
    toast('ok', 'Exported ' + rows.length + ' ' + g.cfg.noun + ' as ' + fmt.toUpperCase() + '.');
  }

  /* ------------------------------------------------------------------ SHARED DERIVATIONS */
  var CTRY = { E01: 'UK', E02: 'Germany', E03: 'France', E04: 'US', E05: 'Hong Kong', E06: 'Singapore', E07: 'China', E08: 'India', E09: 'UAE' };
  function accIn() { return D.accounts.filter(function (a) { return inScope(a.entity); }); }
  function accGbp(a, i) { return a.series[i === undefined ? 29 : i] * D.fx[a.ccy].gbp; }
  function cashSeries(list) { var s = []; for (var i = 0; i < 30; i++) { s.push(sum(list || accIn(), function (a) { return accGbp(a, i); })); } return s; }
  function facIn() { return D.facilities.filter(function (f) { return inScope(f.entity); }); }
  function undrawnSeries(committed) { var s = [], fs = facIn().filter(function (f) { return f.committed === committed; }); for (var i = 0; i < 30; i++) { s.push(sum(fs, function (f) { return f.limitGbp - f.drawnSeries[i]; })); } return s; }
  function txIn() { return D.transactions.filter(function (t) { return inScope(t.entity) && inWin(t.date); }); }
  function perDay(list, f) { var ds = win(D.days); return ds.map(function (d) { return sum(list.filter(function (t) { return t.date === d; }), f); }); }
  function posIn() { return D.positions.filter(function (p) { return inScope(p.entity) && (!EXTRA.ccy || PAGE !== 'risk' || p.group === EXTRA.ccy); }); }
  function payIn() { return D.payments.filter(function (p) { return inScope(p.entity) && (/Awaiting/.test(p.status) || p.due >= D.days[w0()]); }); }
  function exIn() { return D.exceptions.filter(function (x) { var f = S.filters; return (f.region === 'all' || x.region === f.region) && (f.entity === 'all' || D.ent(f.entity).region === x.region); }); }
  function limitUse(l, pos) {
    var ps = pos || D.positions.filter(function (p) { return inScope(p.entity); });
    if (l.kind === 'Country') { return sum(ps.filter(function (p) { return p.region === l.key; }), function (p) { return Math.abs(p.gbp); }); }
    if (l.kind === 'Currency') { return Math.abs(sum(ps.filter(function (p) { return p.group === l.key; }), function (p) { return p.gbp; })); }
    return sum(ps.filter(function (p) { return p.counterparty === l.key && p.gbp > 0; }), function (p) { return p.gbp; });
  }
  function limitRows() { return D.limits.map(function (l) { var u = limitUse(l); return mix({ used: u, util: u / l.limit * 100 }, l); }); }
  function trIn() { return D.trade.filter(function (t) { return inScope(t.entity); }); }
  function outstanding(t) { return t.status !== 'Settled' && t.status !== 'Expired' && t.expiry >= D.asOf; }
  function weekly(vals, labels) {                                         /* > 14 days: fold into weeks so labels stay legible */
    if (nDays() <= 14) { return { cats: labels, vals: vals }; }
    var ds = win(D.days), c = [], v = [];
    for (var i = 0; i < ds.length; i += 7) { c.push('w/c ' + dd(ds[i])); v.push(vals.slice(i, i + 7)); }
    return { cats: c, vals: v, fold: true };
  }
  function bucket(vals) {
    var ds = win(D.days);
    if (nDays() <= 14) { return { cats: ds.map(dd), vals: vals }; }
    var c = [], v = [];
    for (var i = 0; i < ds.length; i += 7) { c.push('w/c ' + dd(ds[i])); v.push(sum(vals.slice(i, i + 7))); }
    return { cats: c, vals: v };
  }
  function r1(v) { return Math.round(v * 10) / 10; }
  var PER = function () { return 'vs ' + dd(D.days[w0()]); };

  /* ================================================================== PAGES */
  var PAGES = {};

  /* ---------------------------------------------------------------- OVERVIEW */
  PAGES.index = {
    render: function () {
      var cash = cashSeries(), cu = undrawnSeries(true), liq = cash.map(function (v, i) { return v + cu[i]; });
      var i0 = w0();
      kpi('k-cash', mix({ pre: '£', val: short(cash[29]), series: win(cash) }, deltaOf(cash[29], cash[i0], PER())));
      kpi('k-liq', mix({ pre: '£', val: short(liq[29]), series: win(liq) }, deltaOf(liq[29], liq[i0], PER())));
      kpi('k-head', mix({ pre: '£', val: short(cu[29]), series: win(cu) }, deltaOf(cu[29], cu[i0], PER())));
      var tx = txIn(), net = sum(tx, function (t) { return t.gbp; }), daily = perDay(tx, function (t) { return t.gbp; }), run = 0;
      var cum = daily.map(function (v) { run += v; return run; });
      kpi('k-flow', { pre: net < 0 ? '−£' : '+£', val: short(net), dir: 'flat', delta: '£' + short(sum(tx.filter(function (t) { return t.gbp > 0; }), function (t) { return t.gbp; })) + ' in', per: '£' + short(-sum(tx.filter(function (t) { return t.gbp < 0; }), function (t) { return t.gbp; })) + ' out · ' + nDays() + ' days', series: cum });
      /* exposure — gross, by region x currency group */
      var pos = D.positions.filter(function (p) { return inScope(p.entity); });
      var regs = D.regions.filter(function (r) { return pos.some(function (p) { return p.region === r; }); });
      if (regs.length) {
        draw('ch-exposure', { type: 'stacked-column', categories: regs, categoryLabel: 'Region', unit: '£m',
          caption: 'Gross exposure by region and currency, GBP millions',
          series: D.ccyGroups.map(function (g) { return { name: g, values: regs.map(function (r) { return r1(mm(sum(pos.filter(function (p) { return p.region === r && p.group === g; }), function (p) { return Math.abs(p.gbp); }))); }) }; }) },
          function (fig) {
            $$('rect.dv-series', fig).forEach(function (rc) {
              var lab = rc.getAttribute('aria-label') || '', reg = regs.filter(function (r) { return lab.indexOf(r) >= 0; })[0], gi = +rc.getAttribute('data-series-group') - 1;
              if (reg) { rc.setAttribute('data-drill', 'risk.html?region=' + encodeURIComponent(reg) + (gi >= 0 ? '&ccy=' + encodeURIComponent(D.ccyGroups[gi]) : '') + '#positions'); rc.style.cursor = 'pointer';
                rc.setAttribute('aria-label', lab + '. Press Enter to open positions and limits.'); }
            });
            /* the engine's series key letter sits on top of its segment — it drills to the same place */
            $$('text.dv-barkey', fig).forEach(function (tx) {
              var t = tx.getBoundingClientRect(), cx = t.left + t.width / 2, cy = t.top + t.height / 2;
              var hit = $$('rect[data-drill][data-series-group="' + tx.getAttribute('data-series-group') + '"]', fig).filter(function (rc) { var r = rc.getBoundingClientRect(); return cx >= r.left && cx <= r.right && cy >= r.top && cy <= r.bottom; })[0];
              if (hit) { tx.setAttribute('data-drill', hit.getAttribute('data-drill')); tx.style.cursor = 'pointer'; }
            });
          });
        $('#drillRow').innerHTML = regs.map(function (r) { return '<a class="tpl-link t-cm-caption" href="risk.html?region=' + encodeURIComponent(r) + '#positions">' + esc(r) + ' · £' + short(sum(pos.filter(function (p) { return p.region === r; }), function (p) { return Math.abs(p.gbp); })) + '</a>'; }).join('');
      }
      /* decisions */
      var mine = D.payments.filter(function (p) { return inScope(p.entity) && p.status === 'Awaiting your approval'; }).sort(function (a, b) { return b.gbp - a.gbp; });
      var mat = mine.filter(function (p) { return p.material; }).length, all = D.payments.filter(function (p) { return inScope(p.entity) && /Awaiting/.test(p.status); }).length;
      $('#naCount').textContent = all + ' payments · ' + mine.length + ' need you' + (mat ? ' · ' + mat + ' material' : '');
      $('#naTotal').textContent = gbpS(sum(mine, function (p) { return p.gbp; }));
      $('#naList').innerHTML = mine.length ? mine.slice(0, 4).map(function (p) {
        return '<div class="l-row" data-gap="s" data-justify="between"><a class="tpl-link t-cm-label" href="payments.html?id=' + p.id + '#approvals">' + esc(p.beneficiary) + ' · ' + gbpS(p.gbp) + '</a>' +
          '<span class="status ' + (p.material ? 'err' : 'warn') + '" data-carries="label"><span class="dot" aria-hidden="true"></span><span class="t-cm-legal">' + (p.material ? 'Material · ' : '') + 'due ' + dd(p.due) + '</span></span></div>';
      }).join('') : '<p class="t-ed-body-small">Nothing is waiting for you in this scope.</p>';
      var ex = exIn().filter(function (x) { return x.status === 'Open' && x.material; });
      var hi = ex.filter(function (x) { return x.severity === 'High'; }).length;
      $('#exCount').textContent = ex.length + ' open · ' + hi + ' high';
      $('#exWorst').textContent = ex.length ? ex[0].severity : 'None';
      $('#exList').innerHTML = ex.length ? ex.slice(0, 4).map(function (x) {
        return '<div class="l-row" data-gap="s" data-justify="between"><a class="tpl-link t-cm-label" href="risk.html?id=' + x.id + '#exceptions">' + esc(x.title) + '</a>' +
          '<span class="status ' + (x.severity === 'High' ? 'err' : 'warn') + '" data-carries="label"><span class="dot" aria-hidden="true"></span><span class="t-cm-legal">' + esc(x.severity) + '</span></span></div>';
      }).join('') : '<p class="t-ed-body-small">No open material exceptions in this scope.</p>';
      $('#stripApprovals').textContent = 'Awaiting approval · ' + all + ' payments · ' + mine.length + ' need you';
      $('#stripRisk').textContent = 'Material exceptions · ' + ex.length + ' open';
      draw('ch-trend', { type: 'multiline', categories: dayLabels(), categoryLabel: 'Day (' + periodText() + ')', unit: '£m', caption: 'Daily group cash and available liquidity, GBP millions',
        series: [{ name: 'Cash', values: win(cash).map(function (v) { return r1(mm(v)); }) }, { name: 'Available liquidity', values: win(liq).map(function (v) { return r1(mm(v)); }) }] });
      var byG = D.ccyGroups.map(function (g) { return [g, r1(mm(sum(accIn().filter(function (a) { return D.ccyGroup[a.ccy] === g; }), function (a) { return accGbp(a); })))]; }).filter(function (p) { return p[1] > 0; });
      if (byG.length) { draw('ch-ccymix', { type: 'donut', categories: byG.map(function (p) { return p[0]; }), unit: '£m', categoryLabel: 'Currency', caption: 'Group cash by currency, GBP millions', series: [{ name: 'Cash', values: byG.map(function (p) { return p[1]; }) }] }); }
      return { count: D.entities.filter(function (e) { return inScope(e.id); }).length, total: D.entities.length };
    }
  };
  document.addEventListener('click', function (e) { var r = e.target.closest('[data-drill]'); if (r) { location.href = r.getAttribute('data-drill'); } });
  document.addEventListener('keydown', function (e) { if (e.key === 'Enter') { var r = e.target.closest && e.target.closest('[data-drill]'); if (r) { location.href = r.getAttribute('data-drill'); } } });

  /* ---------------------------------------------------------------- ACCOUNTS */
  var TXCOLS = [{ key: 'date', label: 'Date', val: function (r) { return dt(r.date); }, sortv: function (r) { return r.date; }, raw: 'date' }, { key: 'id', label: 'Transaction' },
    { key: 'entity', label: 'Entity', val: function (r) { return entName(r.entity); } }, { key: 'type', label: 'Type' }, { key: 'counterparty', label: 'Counterparty' },
    { key: 'amount', label: 'Amount', num: 1, val: function (r) { return money(r.amount, r.ccy); }, sortv: function (r) { return r.amount; }, raw: function (r) { return r.amount + ' ' + r.ccy; }, cell: function (r) { return '<span class="t-cm-figure-5">' + esc(money(r.amount, r.ccy)) + '</span>'; } },
    { key: 'gbp', label: 'GBP equivalent', num: 1, val: function (r) { return gbp(r.gbp); }, sortv: function (r) { return r.gbp; }, raw: 'gbp', cell: function (r) { return '<span class="t-cm-figure-5">' + esc(gbp(r.gbp)) + '</span>'; } },
    { key: 'status', label: 'Status', cell: function (r) { return statusChip(r.status); } }];
  function txDrawer(t) {
    var a = D.accounts.filter(function (x) { return x.id === t.account; })[0];
    drawerOpen('Transaction ' + t.id, summary([['Date', dt(t.date)], ['Type', t.type], ['Counterparty', t.counterparty], ['Amount', money(t.amount, t.ccy)], ['GBP equivalent', gbp(t.gbp) + ' at ' + D.fx[t.ccy].gbp + ' GBP per ' + t.ccy],
      ['Account', (a ? a.name + ' ' + a.number : t.account)], ['Entity', entName(t.entity)], ['Reference', t.ref], ['Status', t.status]]) +
      '<p class="t-ed-body-small">Something wrong with this transaction? Raising an investigation creates a service request with HSBC.</p>',
      dbtn('Raise an investigation', 'investigate') + dbtn('Download advice (CSV)', 'advice', 'secondary'),
      function (sheet) {
        sheet.querySelector('[data-dact="advice"]').onclick = function () { download(t.id + '-advice.csv', toCSV([t], [['id', 'Transaction'], ['date', 'Date'], ['type', 'Type'], ['counterparty', 'Counterparty'], ['amount', 'Amount'], ['ccy', 'Currency'], ['gbp', 'GBP'], ['ref', 'Reference'], ['status', 'Status']]), 'text/csv'); toast('ok', 'Advice for ' + t.id + ' downloaded.'); };
        sheet.querySelector('[data-dact="investigate"]').onclick = function () { var sr = newRequest('Payments investigation', t.entity, 'Standard', 'Investigate transaction ' + t.id + ' — ' + t.counterparty, 'Raised from the transactions view.'); drawerClose(); toast('ok', sr.id + ' raised — find it under Messages.'); };
      });
  }
  PAGES.accounts = {
    init: function () {
      this.gAcc = Grid({ id: 'gAcc', noun: 'accounts', key: function (r) { return r.id; }, rows: accIn, sort: 'gbp', dir: 'descending',
        cols: [{ key: 'id', label: 'Account' }, { key: 'entity', label: 'Entity', val: function (r) { return entName(r.entity); } }, { key: 'name', label: 'Type' }, { key: 'ccy', label: 'Currency' },
          { key: 'balance', label: 'Balance', num: 1, val: function (r) { return money(r.balance, r.ccy); }, sortv: function (r) { return r.balance; }, raw: 'balance', cell: function (r) { return '<span class="t-cm-figure-5">' + esc(money(r.balance, r.ccy)) + '</span>'; } },
          { key: 'gbp', label: 'GBP equivalent', num: 1, val: function (r) { return gbp(accGbp(r)); }, sortv: function (r) { return accGbp(r); }, raw: function (r) { return Math.round(accGbp(r) * 100) / 100; }, cell: function (r) { return '<span class="t-cm-figure-5">' + esc(gbp(accGbp(r))) + '</span>'; } }],
        open: function (a) {
          var tx = D.transactions.filter(function (t) { return t.account === a.id; }).slice(0, 6);
          drawerOpen(a.name + ' ' + a.number, summary([['Entity', entName(a.entity)], ['Currency', a.ccy + ' — ' + D.fx[a.ccy].name], ['Closing balance', money(a.balance, a.ccy)], ['GBP equivalent', gbp(accGbp(a))], ['30 days ago', money(a.series[0], a.ccy)]].concat(a.iban ? [['IBAN', a.iban]] : [])) +
            timeline('Latest transactions', tx.map(function (t) { return { at: dt(t.date), who: t.counterparty, what: t.type + ' · ' + money(t.amount, t.ccy), kind: t.amount < 0 ? 'warn' : 'ok' }; }).reverse()),
            dbtn('Download statement (CSV)', 'stmt') + dbtn('Close', 'close', 'secondary'),
            function (sheet) { sheet.querySelector('[data-dact="stmt"]').onclick = function () { download(a.id + '-statement.csv', toCSV(D.transactions.filter(function (t) { return t.account === a.id && inWin(t.date); }), [['date', 'Date'], ['id', 'Transaction'], ['type', 'Type'], ['counterparty', 'Counterparty'], ['amount', 'Amount'], ['ccy', 'Currency'], ['ref', 'Reference']]), 'text/csv'); toast('ok', 'Statement for ' + a.number + ' downloaded.'); }; });
        } });
      this.gTx = Grid({ id: 'gTx', noun: 'transactions', key: function (r) { return r.id; }, rows: txIn, sort: 'date', dir: 'descending', cols: TXCOLS, open: txDrawer });
    },
    render: function () {
      var cash = cashSeries(), tx = txIn(), inn = sum(tx.filter(function (t) { return t.gbp > 0; }), function (t) { return t.gbp; }), out = -sum(tx.filter(function (t) { return t.gbp < 0; }), function (t) { return t.gbp; });
      var pend = tx.filter(function (t) { return t.status === 'Pending'; });
      kpi('k-cash', mix({ pre: '£', val: short(cash[29]), series: win(cash) }, deltaOf(cash[29], cash[w0()], PER())));
      var dIn = perDay(tx, function (t) { return t.gbp > 0 ? t.gbp : 0; }), dOut = perDay(tx, function (t) { return t.gbp < 0 ? -t.gbp : 0; });
      kpi('k-in', { pre: '£', val: short(inn), dir: 'flat', delta: tx.filter(function (t) { return t.gbp > 0; }).length + ' receipts', per: nDays() + ' days', series: dIn });
      kpi('k-out', { pre: '£', val: short(out), dir: 'flat', delta: tx.filter(function (t) { return t.gbp < 0; }).length + ' payments', per: nDays() + ' days', series: dOut });
      kpi('k-pend', { pre: '£', val: short(sum(pend, function (t) { return Math.abs(t.gbp); })), dir: 'flat', delta: pend.length + ' pending', per: 'value dated today or tomorrow' });
      draw('ch-bal', { type: 'line', categories: dayLabels(), categoryLabel: 'Day (' + periodText() + ')', unit: '£m', caption: 'Daily closing cash balance, GBP millions', series: [{ name: 'Cash', values: win(cash).map(function (v) { return r1(mm(v)); }) }] });
      var ents = D.entities.filter(function (e) { return inScope(e.id); }).map(function (e) { return [e.short, r1(mm(sum(accIn().filter(function (a) { return a.entity === e.id; }), function (a) { return accGbp(a); })))]; }).sort(function (a, b) { return b[1] - a[1]; });
      if (ents.length) { draw('ch-byent', { type: 'bar', categories: ents.map(function (p) { return p[0]; }), categoryLabel: 'Entity', unit: '£m', caption: 'Closing cash by entity, GBP millions', series: [{ name: 'Cash', values: ents.map(function (p) { return p[1]; }) }] }); }
      var bi = bucket(dIn), bo = bucket(dOut);
      draw('ch-flows', { type: 'grouped-column', categories: bi.cats, categoryLabel: nDays() > 14 ? 'Week' : 'Day', unit: '£m', caption: 'Money in and money out, GBP millions',
        series: [{ name: 'Money in', values: bi.vals.map(function (v) { return r1(mm(v)); }) }, { name: 'Money out', values: bo.vals.map(function (v) { return r1(mm(v)); }) }] });
      var BANDS = [['Under £10k', 0, 1e4], ['£10k–50k', 1e4, 5e4], ['£50k–250k', 5e4, 2.5e5], ['£250k–1m', 2.5e5, 1e6], ['£1m–5m', 1e6, 5e6], ['£5m and over', 5e6, Infinity]];
      draw('ch-hist', { type: 'histogram', categories: BANDS.map(function (b) { return b[0]; }), categoryLabel: 'Value band', caption: 'Number of transactions by GBP value band',
        series: [{ name: 'Transactions', values: BANDS.map(function (b) { return tx.filter(function (t) { var a = Math.abs(t.gbp); return a >= b[1] && a < b[2]; }).length; }) }] });
      if (this.gAcc) { this.gAcc.render(); } if (this.gTx) { this.gTx.render(); }
      return { count: this.gTx ? this.gTx.view().length : 0, total: this.gTx ? txIn().length : 0 };
    },
    resolve: function (id) { var t = D.transactions.filter(function (x) { return x.id === id; })[0]; if (t) { txDrawer(t); return; } var a = this.gAcc && this.gAcc.find(id); if (a) { this.gAcc.cfg.open(a); } }
  };

  /* ---------------------------------------------------------------- SHARED WORKFLOW: service request */
  function newRequest(cat, entity, prio, summaryText, details) {
    var n = D.requests.length + S.newRequests.length;
    var sr = { id: 'SR-' + (70000 + n * 7 + S.newRequests.length), category: cat, entity: entity, status: 'Open', opened: D.asOf, priority: prio, summary: summaryText, details: details, mine: true, created: nowStamp() };
    S.newRequests.unshift(sr); D.requests.unshift(sr); save();
    return sr;
  }

  /* ---------------------------------------------------------------- LIQUIDITY */
  function facDrawer(f, preset) {
    var fs = facIn().filter(function (x) { return x.limitGbp - x.drawnGbp > 0; });
    if (!f && !fs.length) { toast('info', 'No facility with undrawn headroom in this scope.'); return; }
    f = f || fs[0];
    var mine = S.drawdowns.filter(function (r) { return r.facility === f.id; });
    var undrawn = f.limitGbp - f.drawnGbp;
    drawerOpen(f.name, summary([['Facility', f.id + ' · ' + f.type + (f.committed ? ' · committed' : ' · uncommitted')], ['Borrower', entName(f.entity)], ['Limit', money(f.limit, f.ccy) + ' (' + gbp(f.limitGbp) + ')'],
      ['Drawn', money(f.drawn, f.ccy) + ' (' + gbp(f.drawnGbp) + ')'], ['Undrawn', gbp(undrawn)], ['Pricing', f.margin], ['Final maturity', dt(f.maturity)]]) +
      (mine.length ? timeline('Your drawdown requests', mine.map(function (r) { return { at: r.at, who: 'You', what: 'Drawdown of ' + gbp(r.amount) + ' for ' + dt(r.value), note: r.purpose, kind: 'warn' }; })) : '') +
      (undrawn > 0 ? '<h4 class="t-cm-section-label">Request a drawdown (simulated)</h4><div class="stack-16">' +
        (preset ? fSelect('ddFac', 'Facility', fs.map(function (x) { return [x.id, x.id + ' · ' + x.name]; }), f.id) : '') +
        fInput('ddAmt', 'Amount in GBP', 'Up to ' + gbp(undrawn) + ' undrawn', '', 'text') + fInput('ddDate', 'Value date', 'On or after ' + dt(D.asOf), D.asOf, 'date') +
        fText('ddWhy', 'Purpose', 'Recorded with the request. At least 10 characters.', 200) + '</div>' : '<p class="t-ed-body">This facility is fully drawn.</p>'),
      (undrawn > 0 ? dbtn('Submit request', 'submit') : '') + dbtn('Close', 'close', 'secondary'),
      function (sheet) {
        wireCounter('ddWhy', 200);
        var fsel = $('#ddFac', sheet); if (fsel) { wireDD(fsel, function (v) { fsel.setAttribute('data-value', v); setTimeout(function () { facDrawer(D.facilities.filter(function (x) { return x.id === v; })[0], true); }, 0); }); }
        var sb = sheet.querySelector('[data-dact="submit"]'); if (!sb) { return; }
        sb.onclick = function () {
          var raw = $('#ddAmt').value.replace(/[£,\s]/g, ''), amt = +raw, ok = true;
          if (!raw || !isFinite(amt) || amt <= 0) { fieldError('ddAmt', 'Enter an amount in pounds, for example 25000000.'); ok = false; }
          else if (amt > undrawn) { fieldError('ddAmt', 'That is more than the ' + gbp(undrawn) + ' undrawn on this facility.'); ok = false; } else { fieldError('ddAmt', ''); }
          var vd = $('#ddDate').value; if (!vd || vd < D.asOf) { fieldError('ddDate', 'Choose a value date on or after ' + dt(D.asOf) + '.'); ok = false; } else { fieldError('ddDate', ''); }
          var why = $('#ddWhy').value.trim(); if (why.length < 10) { fieldError('ddWhy', 'Say what the funds are for, in at least 10 characters.'); ok = false; } else { fieldError('ddWhy', ''); }
          if (!ok) { var bad = sheet.querySelector('[aria-invalid="true"]'); if (bad) { bad.focus(); } return; }
          S.drawdowns.push({ facility: f.id, amount: amt, value: vd, purpose: why, at: nowStamp() }); save();
          drawerClose(); toast('ok', 'Drawdown request for ' + gbp(amt) + ' sent to HSBC (simulated).');
        };
      });
  }
  PAGES.liquidity = {
    init: function () {
      this.g = Grid({ id: 'gFac', noun: 'facilities', key: function (r) { return r.id; }, rows: facIn, sort: 'limitGbp', dir: 'descending',
        cols: [{ key: 'id', label: 'Facility' }, { key: 'name', label: 'Name' }, { key: 'entity', label: 'Entity', val: function (r) { return entName(r.entity); } }, { key: 'type', label: 'Type', val: function (r) { return r.type + (r.committed ? '' : ' (uncommitted)'); } },
          { key: 'limitGbp', label: 'Limit (GBP)', num: 1, val: function (r) { return gbp(r.limitGbp); }, sortv: function (r) { return r.limitGbp; }, raw: 'limitGbp', cell: function (r) { return '<span class="t-cm-figure-5">' + gbp(r.limitGbp) + '</span>'; } },
          { key: 'drawnGbp', label: 'Drawn (GBP)', num: 1, val: function (r) { return gbp(r.drawnGbp); }, sortv: function (r) { return r.drawnGbp; }, raw: 'drawnGbp', cell: function (r) { return '<span class="t-cm-figure-5">' + gbp(r.drawnGbp) + '</span>'; } },
          { key: 'util', label: 'Utilised', num: 1, val: function (r) { return Math.round(r.drawnGbp / r.limitGbp * 100) + '%'; }, sortv: function (r) { return r.drawnGbp / r.limitGbp; } },
          { key: 'maturity', label: 'Maturity', val: function (r) { return dt(r.maturity); }, sortv: function (r) { return r.maturity; }, raw: 'maturity' }],
        open: function (f) { facDrawer(f); } });
    },
    render: function () {
      var cash = cashSeries(), cu = undrawnSeries(true), uu = undrawnSeries(false), i0 = w0();
      var liq = cash.map(function (v, i) { return v + cu[i]; });
      kpi('k-cash', mix({ pre: '£', val: short(cash[29]), series: win(cash) }, deltaOf(cash[29], cash[i0], PER())));
      kpi('k-cu', mix({ pre: '£', val: short(cu[29]), series: win(cu) }, deltaOf(cu[29], cu[i0], PER())));
      kpi('k-uu', mix({ pre: '£', val: short(uu[29]), series: win(uu) }, deltaOf(uu[29], uu[i0], PER())));
      kpi('k-liq', mix({ pre: '£', val: short(liq[29]), series: win(liq) }, deltaOf(liq[29], liq[i0], PER())));
      var net = perDay(txIn(), function (t) { return t.gbp; }), run = 0, cum = net.map(function (v) { run += v; return run; });
      draw('ch-combo', { type: 'combo', categories: dayLabels(), categoryLabel: 'Day (' + periodText() + ')', caption: 'Daily net cash flow and cumulative net flow, GBP millions', sharedScale: true,
        series: [{ name: 'Net flow', kind: 'column', unit: '£m', values: net.map(function (v) { return r1(mm(v)); }) }, { name: 'Cumulative', kind: 'line', unit: '£m', values: cum.map(function (v) { return r1(mm(v)); }) }] });
      var fs = facIn().slice().sort(function (a, b) { return b.limitGbp - a.limitGbp; }).slice(0, 6);
      if (fs.length) {
        draw('ch-bullet', { type: 'bullet', categories: fs.map(function (f) { return f.id + ' ' + CTRY[f.entity]; }), categoryLabel: 'Facility', format: 'percent', ranges: [50, 75, 100], caption: 'Drawn as a share of limit, per facility, against the 75% policy marker',
          series: [{ name: 'Utilised', values: fs.map(function (f) { return Math.round(f.drawnGbp / f.limitGbp * 100); }) }, { name: 'Policy', values: fs.map(function () { return 75; }) }] });
      }
      var regs = D.regions.filter(function (r) { return accIn().some(function (a) { return D.ent(a.entity).region === r; }); });
      if (regs.length) {
        draw('ch-area', { type: 'stacked-area', categories: dayLabels(), categoryLabel: 'Day (' + periodText() + ')', unit: '£m', caption: 'Daily cash by region, GBP millions',
          series: regs.map(function (r) { var s = cashSeries(accIn().filter(function (a) { return D.ent(a.entity).region === r; })); return { name: r, values: win(s).map(function (v) { return r1(mm(v)); }) }; }) });
      }
      var yrs = ['2026', '2027', '2028', '2029', '2030', '2031'];
      draw('ch-mat', { type: 'column', categories: yrs, categoryLabel: 'Year', unit: '£m', caption: 'Facility limits by year of final maturity, GBP millions',
        series: [{ name: 'Maturing', values: yrs.map(function (y) { return r1(mm(sum(facIn().filter(function (f) { return f.maturity.slice(0, 4) === y; }), function (f) { return f.limitGbp; }))); }) }] });
      if (this.g) { this.g.render(); }
      return { count: this.g ? this.g.view().length : 0, total: facIn().length };
    },
    resolve: function (id) { var f = D.facilities.filter(function (x) { return x.id === id; })[0]; if (f) { facDrawer(f); } }
  };

  /* ---------------------------------------------------------------- PAYMENTS */
  function payDrawer(p) {
    var mineNow = p.status === 'Awaiting your approval';
    drawerOpen('Payment ' + p.id, (p.material && mineNow ? '<div class="cn-alert"><div class="alert warn" role="status" data-carries="symbol label"><span class="ic"><svg aria-hidden="true"><use href="#i-warning"/></svg></span><p class="main t-ed-body"><strong class="em">Material payment.</strong> £5m or more — approving asks you to confirm, and an audit note is required.</p></div></div>' : '') +
      summary([['Beneficiary', p.beneficiary], ['Amount', money(p.amount, p.ccy)], ['GBP equivalent', gbp(p.gbp)], ['Rail', p.rail], ['Due', dt(p.due)], ['Paying entity', entName(p.entity)], ['Requested by', p.requestedBy], ['Purpose', p.purpose], ['Status', p.status]]) +
      timeline('Audit trail', p.audit) +
      (mineNow ? fText('payNote', 'Audit note', p.material ? 'Required for a material payment, and for a rejection. At least 10 characters.' : 'Optional for approval, required for a rejection. At least 10 characters.', 300) : ''),
      mineNow ? dbtn('Approve', 'approve') + dbtn('Reject', 'reject', 'secondary') : dbtn('Close', 'close', 'secondary'),
      function (sheet) {
        if (!mineNow) { return; }
        wireCounter('payNote', 300);
        function act(ok) {
          var note = $('#payNote').value.trim();
          if ((!ok || p.material) && note.length < 10) { fieldError('payNote', ok ? 'A material payment needs an audit note of at least 10 characters.' : 'Enter a reason of at least 10 characters for the audit trail.'); $('#payNote').focus(); return; }
          fieldError('payNote', '');
          var go = ok && p.material ? confirmModal('Approve a material payment?', 'You are approving ' + money(p.amount, p.ccy) + ' (' + gbp(p.gbp) + ') to ' + p.beneficiary + '. It will be queued for release after your approval.', 'Approve payment') : Promise.resolve(true);
          go.then(function (yes) {
            if (!yes) { return; }
            var st = ok ? 'Approved' : 'Rejected', entry = { at: nowStamp(), who: 'You (CEO)', what: ok ? 'Approved' : 'Rejected', note: note, kind: ok ? 'ok' : 'err' };
            var d = S.decisions[p.id] || { audit: [] }; d.status = st; d.audit.push(entry); S.decisions[p.id] = d; save();
            p.status = st; p.audit.push(entry);
            drawerClose(); refresh(); toast(ok ? 'ok' : 'info', (ok ? 'Approved ' : 'Rejected ') + p.id + ' — ' + gbp(p.gbp) + ' to ' + p.beneficiary + '.');
          });
        }
        sheet.querySelector('[data-dact="approve"]').onclick = function () { act(true); };
        sheet.querySelector('[data-dact="reject"]').onclick = function () { act(false); };
      });
  }
  PAGES.payments = {
    init: function () {
      var self = this;
      if (EXTRA.status === 'mine') { S.view.payments = 'mine'; }
      var seg = $('#payView');
      function setView(v) { S.view.payments = v; EXTRA.status = v === 'mine' ? 'mine' : ''; save(); syncURL(); $$('button', seg).forEach(function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-view') === v)); }); moveInd(seg); refresh(); }
      seg.addEventListener('click', function (e) { var b = e.target.closest('button[data-view]'); if (b) { setView(b.getAttribute('data-view')); } });
      $$('button', seg).forEach(function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-view') === (S.view.payments || 'all'))); });
      this.g = Grid({ id: 'gPay', noun: 'payments', key: function (r) { return r.id; }, sort: 'due', dir: 'ascending',
        rows: function () { var a = payIn(); return (S.view.payments === 'mine') ? a.filter(function (p) { return p.status === 'Awaiting your approval'; }) : a; },
        cols: [{ key: 'id', label: 'Payment' }, { key: 'due', label: 'Due', val: function (r) { return dt(r.due); }, sortv: function (r) { return r.due; }, raw: 'due' }, { key: 'entity', label: 'Entity', val: function (r) { return entName(r.entity); } },
          { key: 'beneficiary', label: 'Beneficiary' }, { key: 'rail', label: 'Rail' },
          { key: 'amount', label: 'Amount', num: 1, val: function (r) { return money(r.amount, r.ccy); }, sortv: function (r) { return r.gbp; }, raw: function (r) { return r.amount + ' ' + r.ccy; }, cell: function (r) { return '<span class="t-cm-figure-5">' + esc(money(r.amount, r.ccy)) + '</span>'; } },
          { key: 'gbp', label: 'GBP equivalent', num: 1, val: function (r) { return gbp(r.gbp); }, sortv: function (r) { return r.gbp; }, raw: 'gbp', cell: function (r) { return '<span class="t-cm-figure-5">' + esc(gbp(r.gbp)) + '</span>'; } },
          { key: 'status', label: 'Status', val: function (r) { return r.status + (r.material ? ' · material' : ''); }, cell: function (r) { return statusChip(r.status + (r.material && /Awaiting/.test(r.status) ? ' · material' : '')); } }],
        open: payDrawer });
    },
    render: function () {
      var a = D.payments.filter(function (p) { return inScope(p.entity); });
      var mine = a.filter(function (p) { return p.status === 'Awaiting your approval'; }), sec = a.filter(function (p) { return p.status === 'Awaiting second approver'; });
      var rel = a.filter(function (p) { return p.status === 'Released' && inWin(p.due); }), rej = a.filter(function (p) { return p.status === 'Rejected'; });
      kpi('k-mine', { pre: '£', val: short(sum(mine, function (p) { return p.gbp; })), dir: 'flat', delta: mine.length + ' payments', per: mine.filter(function (p) { return p.material; }).length + ' material' });
      kpi('k-second', { pre: '£', val: short(sum(sec, function (p) { return p.gbp; })), dir: 'flat', delta: sec.length + ' payments', per: 'with a second approver' });
      kpi('k-rel', { pre: '£', val: short(sum(rel, function (p) { return p.gbp; })), dir: 'flat', delta: rel.length + ' payments', per: nDays() + ' days', series: perDay(rel.map(function (p) { return { date: p.due, gbp: p.gbp }; }), function (t) { return t.gbp; }) });
      kpi('k-rej', { pre: '£', val: short(sum(rej, function (p) { return p.gbp; })), dir: 'flat', delta: rej.length + ' payments', per: 'rejected, all time' });
      var ents = D.entities.filter(function (e) { return inScope(e.id); }), groups = [['Released', /Released/], ['Approved or scheduled', /Approved|Scheduled/], ['Awaiting approval', /Awaiting/], ['Rejected', /Rejected/]];
      var pi = payIn();
      draw('ch-paystack', { type: 'stacked-column', categories: ents.map(function (e) { return CTRY[e.id]; }), categoryLabel: 'Paying entity', unit: '£m', caption: 'Payment value by paying entity and status, GBP millions',
        series: groups.map(function (g) { return { name: g[0], values: ents.map(function (e) { return r1(mm(sum(pi.filter(function (p) { return p.entity === e.id && g[1].test(p.status); }), function (p) { return p.gbp; }))); }) }; }) });
      var rails = top(D.rails.map(function (r) { return [r, r1(mm(sum(rel.filter(function (p) { return p.rail === r; }), function (p) { return p.gbp; })))]; }).filter(function (x) { return x[1] > 0; }), 5);
      if (rails.length) { draw('ch-rails', { type: 'pie', categories: rails.map(function (x) { return x[0]; }), categoryLabel: 'Rail', unit: '£m', caption: 'Released payment value by rail, GBP millions', series: [{ name: 'Released', values: rails.map(function (x) { return x[1]; }) }] }); }
      var bs = {}; pi.forEach(function (p) { bs[p.beneficiary] = (bs[p.beneficiary] || 0) + p.gbp; });
      var bl = Object.keys(bs).map(function (k) { return [k, r1(mm(bs[k]))]; }).sort(function (x, y) { return y[1] - x[1]; }).slice(0, 8);
      if (bl.length) { draw('ch-benef', { type: 'bar', categories: bl.map(function (x) { return x[0]; }), categoryLabel: 'Beneficiary', unit: '£m', caption: 'Payment value by beneficiary, GBP millions, top eight', series: [{ name: 'Value', values: bl.map(function (x) { return x[1]; }) }] }); }
      if (this.g) { this.g.render(); }
      return { count: this.g ? this.g.view().length : 0, total: payIn().length };
    },
    resolve: function (id) { var p = D.payments.filter(function (x) { return x.id === id; })[0]; if (p) { payDrawer(p); } }
  };

  /* ---------------------------------------------------------------- FX */
  function quantile(a, q) { var s = a.slice().sort(function (x, y) { return x - y; }), p = (s.length - 1) * q, b = Math.floor(p); return s[b + 1] !== undefined ? s[b] + (p - b) * (s[b + 1] - s[b]) : s[b]; }
  function dealDrawer(d) {
    drawerOpen('FX deal ' + d.id, summary([['Pair', d.pair], ['Type', d.kind], ['Side', d.side + ' ' + d.pair.split('/')[1]], ['Notional', money(d.notional, d.pair.split('/')[1])], ['GBP equivalent', gbp(d.gbp)], ['Rate', String(d.rate) + ' per GBP'],
      ['Trade date', dt(d.trade)], ['Value date', dt(d.value)], ['Entity', entName(d.entity)], ['Status', d.status]]),
      dbtn('Request confirmation copy', 'conf') + dbtn('Close', 'close', 'secondary'),
      function (sheet) { sheet.querySelector('[data-dact="conf"]').onclick = function () { var sr = newRequest('Statement request', d.entity, 'Standard', 'Confirmation copy for ' + d.id, 'Requested from the FX deals view.'); drawerClose(); toast('ok', sr.id + ' raised for a confirmation copy.'); }; });
  }
  function quoteDrawer() {
    var ents = D.entities.filter(function (e) { return inScope(e.id); });
    drawerOpen('Request an indicative quote', '<p class="t-ed-body-small">Rates are illustrative placeholders, not a price. Booking creates a simulated deal awaiting confirmation.</p><div class="stack-16">' +
      fSelect('qPair', 'Currency pair', D.pairs.map(function (c) { return ['GBP/' + c, 'GBP/' + c + ' — ' + D.fx[c].name]; }), 'GBP/USD') +
      fSelect('qSide', 'You', [['Sell', 'Sell pounds, buy the currency'], ['Buy', 'Buy pounds, sell the currency']], 'Sell') +
      fSelect('qTenor', 'Value date', [['Spot', 'Spot (two business days)'], ['1M', 'One month forward'], ['3M', 'Three months forward']], 'Spot') +
      fSelect('qEnt', 'Booking entity', ents.map(function (e) { return [e.id, e.name]; }), ents[0] ? ents[0].id : 'E01') +
      fInput('qAmt', 'Amount in GBP', 'Between £10,000 and £50,000,000', '', 'text') + '</div><div id="qOut"></div>',
      dbtn('Get indicative rate', 'price') + dbtn('Close', 'close', 'secondary'),
      function (sheet) {
        wireFormDD(sheet);
        var quote = null;
        sheet.querySelector('[data-dact="price"]').onclick = function () {
          var amt = +$('#qAmt').value.replace(/[£,\s]/g, '');
          if (!isFinite(amt) || amt < 1e4 || amt > 5e7) { fieldError('qAmt', 'Enter an amount between £10,000 and £50,000,000.'); $('#qAmt').focus(); return; }
          fieldError('qAmt', '');
          var c = ddValue('qPair').split('/')[1], side = ddValue('qSide'), ten = ddValue('qTenor'), fwd = ten === '1M' ? 0.0011 : ten === '3M' ? 0.0032 : 0;
          var rate = Math.round(D.fx[c].quote * (1 + (side === 'Sell' ? -0.0015 : 0.0015) - fwd) * 10000) / 10000;
          quote = { c: c, side: side, ten: ten, amt: amt, rate: rate, ent: ddValue('qEnt') };
          $('#qOut').innerHTML = summary([['Indicative rate', rate + ' ' + c + ' per GBP'], ['You ' + (side === 'Sell' ? 'receive' : 'pay'), money(amt * rate, c)], ['Value', ten === 'Spot' ? 'Spot' : ten === '1M' ? 'One month' : 'Three months'], ['Valid for', '30 seconds (simulated)']]);
          $('#dfoot').innerHTML = dbtn('Book deal', 'book') + dbtn('Close', 'close', 'secondary');
          $('#dfoot [data-dact="book"]').onclick = function () {
            confirmModal('Book this FX deal?', 'You ' + quote.side.toLowerCase() + ' ' + gbp(quote.amt) + ' against ' + quote.c + ' at ' + quote.rate + '. The deal will await confirmation (simulated).', 'Book deal').then(function (yes) {
              if (!yes) { return; }
              var d = { id: 'FXD-' + (99000 + S.deals.length * 3 + 1), entity: quote.ent, pair: 'GBP/' + quote.c, kind: quote.ten === 'Spot' ? 'Spot' : 'Forward', side: quote.side === 'Sell' ? 'Buy' : 'Sell',
                notional: Math.round(quote.amt * quote.rate), gbp: quote.amt, rate: quote.rate, trade: D.asOf, value: D.asOf, status: 'Awaiting confirmation' };
              S.deals.unshift(d); D.deals.unshift(d); save(); drawerClose(); refresh(); toast('ok', 'Booked ' + d.id + ' — awaiting confirmation.');
            });
          };
        };
      });
  }
  PAGES.fx = {
    init: function () {
      this.gR = Grid({ id: 'gRates', noun: 'rates', key: function (r) { return r.pair; }, rows: function () { return D.pairs.map(function (c) { var s = win(D.fxSeries[c]); return { pair: 'GBP/' + c, name: D.fx[c].name, quote: D.fx[c].quote, gbp: D.fx[c].gbp, chg: pct(s[s.length - 1], s[0]) }; }); },
        cols: [{ key: 'pair', label: 'Pair' }, { key: 'name', label: 'Currency' }, { key: 'quote', label: 'Units per GBP', num: 1 }, { key: 'gbp', label: 'GBP per unit', num: 1 },
          { key: 'chg', label: 'Period change', num: 1, val: function (r) { return (r.chg >= 0 ? '+' : '−') + Math.abs(r.chg).toFixed(2) + '%'; }, sortv: function (r) { return r.chg; } }] });
      this.g = Grid({ id: 'gDeals', noun: 'deals', key: function (r) { return r.id; }, rows: function () { return D.deals.filter(function (d) { return inScope(d.entity); }); }, sort: 'trade', dir: 'descending',
        cols: [{ key: 'id', label: 'Deal' }, { key: 'trade', label: 'Trade date', val: function (r) { return dt(r.trade); }, sortv: function (r) { return r.trade; }, raw: 'trade' }, { key: 'entity', label: 'Entity', val: function (r) { return entName(r.entity); } },
          { key: 'pair', label: 'Pair' }, { key: 'kind', label: 'Type' }, { key: 'side', label: 'Side' },
          { key: 'notional', label: 'Notional', num: 1, val: function (r) { return money(r.notional, r.pair.split('/')[1]); }, sortv: function (r) { return r.gbp; }, raw: 'notional' },
          { key: 'gbp', label: 'GBP equivalent', num: 1, val: function (r) { return gbp(r.gbp); }, sortv: function (r) { return r.gbp; }, raw: 'gbp' },
          { key: 'status', label: 'Status', cell: function (r) { return statusChip(r.status); } }], open: dealDrawer });
    },
    render: function () {
      ['USD', 'EUR', 'HKD'].forEach(function (c) { var s = win(D.fxSeries[c]); kpi('k-' + c.toLowerCase(), mix({ pre: '', val: s[s.length - 1].toFixed(4), series: s }, deltaOf(s[s.length - 1], s[0], PER()))); });
      var pos = D.positions.filter(function (p) { return inScope(p.entity) && p.ccy !== 'GBP'; });
      kpi('k-net', { pre: '£', val: short(sum(pos, function (p) { return Math.abs(p.gbp) * (1 - p.hedged / 100); })), dir: 'flat', delta: Math.round(sum(pos, function (p) { return Math.abs(p.gbp) * p.hedged / 100; }) / (sum(pos, function (p) { return Math.abs(p.gbp); }) || 1) * 100) + '% hedged', per: 'non-sterling positions' });
      var o = D.ohlc.filter(function (x) { return inWin(x.d); });
      if (o.length) {
        draw('ch-candle', { type: 'candlestick', categories: o.map(function (x) { return nDays() > 14 ? String(+x.d.slice(8)) : dd(x.d); }), categoryLabel: 'Session (' + periodText() + ')', caption: 'GBP/USD by session, US dollars per pound',
          series: [{ name: 'Open', values: o.map(function (x) { return x.o; }) }, { name: 'High', values: o.map(function (x) { return x.h; }) }, { name: 'Low', values: o.map(function (x) { return x.l; }) }, { name: 'Close', values: o.map(function (x) { return x.c; }) }] });
      }
      var cs = D.pairs.map(function (c) { var ps = pos.filter(function (p) { return p.ccy === c; }), g = sum(ps, function (p) { return Math.abs(p.gbp); }); return { c: c, x: r1(mm(g)), y: g ? Math.round(sum(ps, function (p) { return Math.abs(p.gbp) * p.hedged; }) / g) : 0 }; }).filter(function (p) { return p.x > 0; });
      var seen = {}; cs.forEach(function (p) { while (seen[p.x]) { p.x = r1(p.x + 0.1); } seen[p.x] = 1; });
      if (cs.length) { draw('ch-hedge', { type: 'scatter', categories: cs.map(function (p) { return String(p.x); }), categoryLabel: 'Gross exposure (£m)', format: 'percent', caption: 'Hedge ratio against gross exposure by currency: ' + cs.map(function (p) { return p.c; }).join(', '), series: [{ name: 'Hedge ratio', values: cs.map(function (p) { return p.y; }) }] }); }
      var idx = ['USD', 'EUR', 'HKD', 'CNY', 'INR'];
      draw('ch-index', { type: 'multiline', categories: dayLabels(), categoryLabel: 'Day (' + periodText() + ')', caption: 'Units per pound rebased to 100 at the start of the period',
        series: idx.map(function (c) { var s = win(D.fxSeries[c]); return { name: 'GBP/' + c, values: s.map(function (v) { return Math.round(v / s[0] * 10000) / 100; }) }; }) });
      var mv = D.pairs.map(function (c) { var s = win(D.fxSeries[c]), m = []; for (var i = 1; i < s.length; i++) { m.push(Math.round((s[i] / s[i - 1] - 1) * 1e5) / 10); } return m.length ? m : [0]; });
      draw('ch-box', { type: 'boxplot', categories: D.pairs, categoryLabel: 'Currency', caption: 'Daily move in units per pound, basis points',
        series: [['Minimum', 0], ['Q1', 0.25], ['Median', 0.5], ['Q3', 0.75], ['Maximum', 1]].map(function (q) { return { name: q[0], values: mv.map(function (m) { return Math.round(quantile(m, q[1]) * 10) / 10; }) }; }) });
      if (this.gR) { this.gR.render(); } if (this.g) { this.g.render(); }
      return { count: this.g ? this.g.view().length : 0, total: D.deals.filter(function (d) { return inScope(d.entity); }).length };
    },
    resolve: function (id) { var d = D.deals.filter(function (x) { return x.id === id; })[0]; if (d) { dealDrawer(d); } }
  };

  /* ---------------------------------------------------------------- RISK */
  function excDrawer(x) {
    var l = x.limit ? limitRows().filter(function (r) { return r.id === x.limit; })[0] : null, open = x.status === 'Open';
    drawerOpen(x.id + ' · ' + x.severity, summary([['Exception', x.title], ['Region', x.region], ['Currency', x.ccy], ['Raised', dt(x.raised)], ['Owner', x.owner], ['Material', x.material ? 'Yes' : 'No'], ['Status', x.status]].concat(l ? [['Limit', l.name], ['Utilisation', gbp(l.used) + ' of ' + gbp(l.limit) + ' (' + Math.round(l.util) + '%)']] : [])) +
      '<p class="t-ed-body-small"><a class="tpl-link" href="risk.html?region=' + encodeURIComponent(x.region) + '&ccy=' + encodeURIComponent(x.ccy) + '#positions">View the underlying positions for ' + esc(x.region) + ' · ' + esc(x.ccy) + '</a></p>' +
      timeline('Audit trail', x.audit) + '<div class="stack-16">' +
      fText('ackNote', open ? 'Acknowledgement note' : 'Add an audit note', 'Written to the audit trail with your name and the time. At least 15 characters.', 400) +
      (open ? fCheck('ackChk', 'I have reviewed the underlying positions and limits') + '<p class="t-ed-body-small" id="ackChk-e" hidden>Confirm you have reviewed the positions and limits.</p>' : '') + '</div>',
      dbtn(open ? 'Acknowledge' : 'Add note', 'ack') + dbtn('Close', 'close', 'secondary'),
      function (sheet) {
        wireCounter('ackNote', 400);
        sheet.querySelector('[data-dact="ack"]').onclick = function () {
          var note = $('#ackNote').value.trim(), ok = true;
          if (note.length < 15) { fieldError('ackNote', 'Write an audit note of at least 15 characters.'); ok = false; } else { fieldError('ackNote', ''); }
          var chk = $('#ackChk'); if (chk && !chk.checked) { $('#ackChk-e').hidden = false; chk.setAttribute('aria-invalid', 'true'); chk.setAttribute('aria-describedby', 'ackChk-e'); ok = false; } else if (chk) { $('#ackChk-e').hidden = true; chk.removeAttribute('aria-invalid'); }
          if (!ok) { var bad = sheet.querySelector('[aria-invalid="true"]'); if (bad) { bad.focus(); } return; }
          var e = { at: nowStamp(), who: 'You (CEO)', what: open ? 'Acknowledged' : 'Audit note added', note: note, kind: 'ok' };
          S.acks[x.id] = (S.acks[x.id] || []).concat([e]); x.status = 'Acknowledged'; x.audit.push(e); save();
          drawerClose(); refresh(); toast('ok', (open ? 'Acknowledged ' : 'Note added to ') + x.id + '.');
        };
      });
  }
  PAGES.risk = {
    init: function () {
      this.gE = Grid({ id: 'gExc', noun: 'exceptions', key: function (r) { return r.id; }, rows: exIn, sort: 'raised', dir: 'descending',
        cols: [{ key: 'id', label: 'Exception' }, { key: 'raised', label: 'Raised', val: function (r) { return dt(r.raised); }, sortv: function (r) { return r.raised; }, raw: 'raised' }, { key: 'title', label: 'Exception' }, { key: 'region', label: 'Region' },
          { key: 'severity', label: 'Severity', sortv: function (r) { return { High: 3, Medium: 2, Low: 1 }[r.severity]; }, cell: function (r) { return statusChip(r.severity); } },
          { key: 'status', label: 'Status', val: function (r) { return r.status + (r.material ? ' · material' : ''); }, cell: function (r) { return statusChip(r.status + (r.material ? ' · material' : '')); } }], open: excDrawer });
      this.gP = Grid({ id: 'gPos', noun: 'positions', key: function (r) { return r.id; }, rows: posIn, sort: 'gbp', dir: 'descending',
        cols: [{ key: 'id', label: 'Position' }, { key: 'entity', label: 'Entity', val: function (r) { return entName(r.entity); } }, { key: 'region', label: 'Region' }, { key: 'ccy', label: 'Currency' }, { key: 'type', label: 'Type' }, { key: 'counterparty', label: 'Counterparty' },
          { key: 'gbp', label: 'GBP equivalent', num: 1, val: function (r) { return gbp(r.gbp); }, sortv: function (r) { return r.gbp; }, raw: 'gbp', cell: function (r) { return '<span class="t-cm-figure-5">' + esc(gbp(r.gbp)) + '</span>'; } },
          { key: 'hedged', label: 'Hedged', num: 1, val: function (r) { return r.hedged + '%'; }, sortv: function (r) { return r.hedged; } },
          { key: 'maturity', label: 'Maturity', val: function (r) { return dt(r.maturity); }, sortv: function (r) { return r.maturity; }, raw: 'maturity' }],
        open: function (p) { drawerOpen('Position ' + p.id, summary([['Entity', entName(p.entity)], ['Region', p.region], ['Type', p.type], ['Counterparty', p.counterparty], ['Notional', money(p.notional, p.ccy)], ['GBP equivalent', gbp(p.gbp)], ['Hedged', p.hedged + '%'], ['Maturity', dt(p.maturity)]]), dbtn('Close', 'close', 'secondary')); } });
    },
    render: function () {
      var pos = posIn(), all = D.positions.filter(function (p) { return inScope(p.entity); }), lr = limitRows();
      kpi('k-gross', { pre: '£', val: short(sum(pos, function (p) { return Math.abs(p.gbp); })), dir: 'flat', delta: pos.length + ' positions', per: EXTRA.ccy ? EXTRA.ccy + ' only' : 'all currencies' });
      var nop = sum(D.ccyGroups.filter(function (g) { return g !== 'GBP'; }), function (g) { return Math.abs(sum(all.filter(function (p) { return p.group === g; }), function (p) { return p.gbp; })); });
      kpi('k-nop', { pre: '£', val: short(nop), dir: 'flat', delta: 'across four currency groups', per: 'long plus short' });
      var warn = lr.filter(function (l) { return l.util >= 85; }), br = lr.filter(function (l) { return l.util >= 100; });
      kpi('k-lim', { pre: '', val: String(warn.length), dir: 'flat', delta: br.length + ' in breach', per: 'of ' + lr.length + ' limits' });
      var ex = exIn(), op = ex.filter(function (x) { return x.status === 'Open'; });
      kpi('k-exc', { pre: '', val: String(op.length), dir: 'flat', delta: op.filter(function (x) { return x.material; }).length + ' material', per: (ex.length - op.length) + ' acknowledged' });
      var regs = D.regions.filter(function (r) { return all.some(function (p) { return p.region === r; }); });
      draw('ch-reglim', { type: 'grouped-column', categories: regs, categoryLabel: 'Region', unit: '£m', caption: 'Gross exposure and limit by region, GBP millions',
        series: [{ name: 'Exposure', values: regs.map(function (r) { return r1(mm(sum(all.filter(function (p) { return p.region === r; }), function (p) { return Math.abs(p.gbp); }))); }) },
                 { name: 'Limit', values: regs.map(function (r) { return r1(mm(D.limits.filter(function (l) { return l.key === r; })[0].limit)); }) }] });
      draw('ch-fly', { type: 'butterfly-h', categories: D.ccyGroups, categoryLabel: 'Currency', unit: '£m', caption: 'Long and short positions by currency group, GBP millions',
        series: [{ name: 'Long', values: D.ccyGroups.map(function (g) { return r1(mm(sum(all.filter(function (p) { return p.group === g && p.gbp > 0; }), function (p) { return p.gbp; }))); }) },
                 { name: 'Short', values: D.ccyGroups.map(function (g) { return r1(mm(-sum(all.filter(function (p) { return p.group === g && p.gbp < 0; }), function (p) { return p.gbp; }))); }) }] });
      var lt = lr.slice().sort(function (a, b) { return b.util - a.util; }).slice(0, 7);
      draw('ch-limits', { type: 'bullet', categories: lt.map(function (l) { return l.name.split(' — ')[0]; }), categoryLabel: 'Limit', format: 'percent', ranges: [70, 85, 120], caption: 'Utilisation of each limit as a share of the limit, against an 85% warning marker',
        series: [{ name: 'Utilised', values: lt.map(function (l) { return Math.min(120, Math.round(l.util)); }) }, { name: 'Warning', values: lt.map(function () { return 85; }) }] });
      if (this.gE) { this.gE.render(); } if (this.gP) { this.gP.render(); }
      return { count: this.gP ? this.gP.view().length : 0, total: all.length };
    },
    resolve: function (id) { var x = D.exceptions.filter(function (e) { return e.id === id; })[0]; if (x) { excDrawer(x); return; } var p = this.gP && this.gP.find(id); if (p) { this.gP.cfg.open(p); } }
  };

  /* ---------------------------------------------------------------- TRADE */
  function tfDrawer(t) {
    var list = trIn().filter(outstanding);
    if (!t && !list.length) { toast('info', 'No outstanding instruments in this scope.'); return; }
    var pick = !t; t = t || list[0];
    var sr = D.requests.filter(function (r) { return r.summary.indexOf(t.id) >= 0; });
    drawerOpen(pick ? 'Request an amendment' : t.type + ' ' + t.id, (pick ? '<div class="stack-16">' + fSelect('tfPick', 'Instrument', list.map(function (x) { return [x.id, x.id + ' · ' + x.type + ' · ' + money(x.amount, x.ccy)]; }), t.id) + '</div>' : '') +
      summary([['Type', t.type], ['Applicant', entName(t.entity)], ['Counterparty', t.counterparty], ['Amount', money(t.amount, t.ccy)], ['GBP equivalent', gbp(t.gbp)], ['Issued', dt(t.issued)], ['Expiry', dt(t.expiry)], ['Port', t.port], ['Status', t.status]]) +
      (sr.length ? timeline('Service requests on this instrument', sr.map(function (r) { return { at: dt(r.opened), who: r.id, what: r.summary, kind: 'warn' }; })) : '') +
      (outstanding(t) ? '<h4 class="t-cm-section-label">Amend this instrument (simulated)</h4><div class="stack-16">' + fSelect('tfKind', 'Amendment', [['Extend expiry', 'Extend expiry'], ['Increase amount', 'Increase amount'], ['Change beneficiary details', 'Change beneficiary details'], ['Waive discrepancy', 'Waive discrepancy']], 'Extend expiry') +
        fText('tfWhy', 'Details for the trade desk', 'What should change, and why. At least 10 characters.', 300) + '</div>' : '<p class="t-ed-body">This instrument is ' + esc(t.status.toLowerCase()) + ' and cannot be amended.</p>'),
      (outstanding(t) ? dbtn('Send amendment request', 'send') : '') + dbtn('Close', 'close', 'secondary'),
      function (sheet) {
        wireFormDD(sheet); wireCounter('tfWhy', 300);
        var p = $('#tfPick', sheet); if (p) { wireDD(p, function (v) { setTimeout(function () { tfDrawerPick(v); }, 0); }); }
        var b = sheet.querySelector('[data-dact="send"]'); if (!b) { return; }
        b.onclick = function () {
          var why = $('#tfWhy').value.trim(); if (why.length < 10) { fieldError('tfWhy', 'Describe the amendment in at least 10 characters.'); $('#tfWhy').focus(); return; }
          var r = newRequest('Trade finance amendment', t.entity, 'High', ddValue('tfKind') + ' — ' + t.id, why); drawerClose(); refresh(); toast('ok', r.id + ' sent to the trade finance desk.');
        };
      });
  }
  function tfDrawerPick(id) { var t = D.trade.filter(function (x) { return x.id === id; })[0]; if (t) { tfDrawer(t); } }
  PAGES.trade = {
    init: function () {
      this.g = Grid({ id: 'gTf', noun: 'instruments', key: function (r) { return r.id; }, rows: trIn, sort: 'expiry', dir: 'ascending',
        cols: [{ key: 'id', label: 'Instrument' }, { key: 'type', label: 'Type' }, { key: 'entity', label: 'Entity', val: function (r) { return entName(r.entity); } }, { key: 'counterparty', label: 'Counterparty' },
          { key: 'amount', label: 'Amount', num: 1, val: function (r) { return money(r.amount, r.ccy); }, sortv: function (r) { return r.gbp; }, raw: function (r) { return r.amount + ' ' + r.ccy; }, cell: function (r) { return '<span class="t-cm-figure-5">' + esc(money(r.amount, r.ccy)) + '</span>'; } },
          { key: 'gbp', label: 'GBP equivalent', num: 1, val: function (r) { return gbp(r.gbp); }, sortv: function (r) { return r.gbp; }, raw: 'gbp', cell: function (r) { return '<span class="t-cm-figure-5">' + esc(gbp(r.gbp)) + '</span>'; } },
          { key: 'expiry', label: 'Expiry', val: function (r) { return dt(r.expiry); }, sortv: function (r) { return r.expiry; }, raw: 'expiry' },
          { key: 'status', label: 'Status', cell: function (r) { return statusChip(r.status); } }], open: tfDrawer });
    },
    render: function () {
      var a = trIn(), out = a.filter(outstanding), soon = out.filter(function (t) { return t.expiry <= '2026-10-25'; }), disc = a.filter(function (t) { return t.status === 'Discrepancies found'; });
      var lines = D.tradeLines.filter(function (l) { return inScope(l.entity); }), lim = sum(lines, function (l) { return l.limitGbp; }), used = sum(out, function (t) { return t.gbp; });
      kpi('k-out', { pre: '£', val: short(used), dir: 'flat', delta: out.length + ' instruments', per: 'outstanding' });
      kpi('k-exp', { pre: '£', val: short(sum(soon, function (t) { return t.gbp; })), dir: 'flat', delta: soon.length + ' instruments', per: 'expire by 25 Oct' });
      kpi('k-disc', { pre: '£', val: short(sum(disc, function (t) { return t.gbp; })), dir: 'flat', delta: disc.length + ' presentations', per: 'with discrepancies' });
      kpi('k-line', { pre: '£', val: short(lim - used), dir: 'flat', delta: Math.round(used / (lim || 1) * 100) + '% used', per: 'of ' + gbpS(lim) + ' lines' });
      var months = []; for (var i = 0; i < 12; i++) { var d = new Date(Date.UTC(2026, 8 + i, 1)); months.push(d.getUTCFullYear() + '-' + String(d.getUTCMonth() + 1).padStart(2, '0')); }
      draw('ch-expiry', { type: 'column', categories: months.map(function (m) { return MON[+m.slice(5) - 1] + (m.slice(5) === '01' || m === months[0] ? ' ' + m.slice(2, 4) : ''); }), categoryLabel: 'Month of expiry', unit: '£m', caption: 'Outstanding instrument value by month of expiry, GBP millions',
        series: [{ name: 'Expiring', values: months.map(function (m) { return r1(mm(sum(out.filter(function (t) { return t.expiry.slice(0, 7) === m; }), function (t) { return t.gbp; }))); }) }] });
      var types = ['Import letter of credit', 'Export letter of credit', 'Standby letter of credit', 'Bank guarantee', 'Documentary collection'].map(function (k) { return [k, r1(mm(sum(out.filter(function (t) { return t.type === k; }), function (t) { return t.gbp; })))]; }).filter(function (x) { return x[1] > 0; });
      if (types.length) { draw('ch-types', { type: 'donut', categories: types.map(function (x) { return x[0]; }), categoryLabel: 'Instrument', unit: '£m', caption: 'Outstanding value by instrument type, GBP millions', series: [{ name: 'Outstanding', values: types.map(function (x) { return x[1]; }) }] }); }
      if (lines.length) {
        draw('ch-lines', { type: 'bullet', categories: lines.map(function (l) { return CTRY[l.entity]; }), categoryLabel: 'Entity', format: 'percent', ranges: [50, 75, 100], caption: 'Outstanding instruments as a share of each entity trade line, against a 75% policy marker',
          series: [{ name: 'Utilised', values: lines.map(function (l) { return Math.min(100, Math.round(sum(out.filter(function (t) { return t.entity === l.entity; }), function (t) { return t.gbp; }) / l.limitGbp * 100)); }) }, { name: 'Policy', values: lines.map(function () { return 75; }) }] });
      }
      if (this.g) { this.g.render(); }
      return { count: this.g ? this.g.view().length : 0, total: a.length };
    },
    resolve: function (id) { tfDrawerPick(id); }
  };

  /* ---------------------------------------------------------------- REPORTS */
  function reportData(r) {
    var map = { Liquidity: [accIn(), [['id', 'Account'], ['entity', 'Entity'], ['name', 'Type'], ['ccy', 'Currency'], ['balance', 'Balance']]], Funding: [facIn(), [['id', 'Facility'], ['name', 'Name'], ['entity', 'Entity'], ['limitGbp', 'Limit GBP'], ['drawnGbp', 'Drawn GBP'], ['maturity', 'Maturity']]],
      Markets: [D.deals.filter(function (d) { return inScope(d.entity); }), [['id', 'Deal'], ['pair', 'Pair'], ['kind', 'Type'], ['notional', 'Notional'], ['gbp', 'GBP'], ['status', 'Status']]],
      Risk: [D.positions.filter(function (p) { return inScope(p.entity); }), [['id', 'Position'], ['entity', 'Entity'], ['region', 'Region'], ['ccy', 'Currency'], ['type', 'Type'], ['gbp', 'GBP'], ['hedged', 'Hedged %']]],
      Payments: [payIn(), [['id', 'Payment'], ['due', 'Due'], ['beneficiary', 'Beneficiary'], ['rail', 'Rail'], ['gbp', 'GBP'], ['status', 'Status']]],
      Trade: [trIn(), [['id', 'Instrument'], ['type', 'Type'], ['counterparty', 'Counterparty'], ['gbp', 'GBP'], ['expiry', 'Expiry'], ['status', 'Status']]],
      Accounts: [txIn(), [['date', 'Date'], ['id', 'Transaction'], ['type', 'Type'], ['counterparty', 'Counterparty'], ['amount', 'Amount'], ['ccy', 'Currency'], ['gbp', 'GBP']]],
      Service: [D.requests, [['id', 'Request'], ['opened', 'Opened'], ['category', 'Category'], ['status', 'Status'], ['summary', 'Summary']]] };
    if (r.category === 'Board') {
      var cash = cashSeries(), cu = undrawnSeries(true);
      return [[{ k: 'Cash (GBP)', v: Math.round(cash[29]) }, { k: 'Committed undrawn (GBP)', v: Math.round(cu[29]) }, { k: 'Available liquidity (GBP)', v: Math.round(cash[29] + cu[29]) },
        { k: 'Payments awaiting approval', v: D.payments.filter(function (p) { return p.status === 'Awaiting your approval'; }).length }, { k: 'Open material exceptions', v: D.exceptions.filter(function (x) { return x.status === 'Open' && x.material; }).length }], [['k', 'Measure'], ['v', 'Value']]];
    }
    return map[r.category] || map.Accounts;
  }
  function runReport(r, dl) {
    var n = S.runs[r.id] || { count: 0 }; n.count++; n.last = D.asOf; S.runs[r.id] = n; r.runs++; r.lastRun = D.asOf; save();
    if (dl) { var x = reportData(r); download(r.id + '-' + r.name.toLowerCase().replace(/[^a-z0-9]+/g, '-') + '.csv', toCSV(x[0], x[1]), 'text/csv'); }
    refresh(); toast('ok', r.name + ' run' + (dl ? ' and downloaded' : '') + ' (' + reportData(r)[0].length + ' rows).');
  }
  function repDrawer(r) {
    drawerOpen(r.name, summary([['Report', r.id], ['Category', r.category], ['Frequency', r.frequency], ['Owner', r.owner], ['Last run', dt(r.lastRun)], ['Runs to date', String(r.runs)], ['Rows at current filters', String(reportData(r)[0].length)]]) +
      '<p class="t-ed-body-small">Runs use the shared entity, region and date filters. Downloads are CSV built from the illustrative data.</p>',
      dbtn('Run and download CSV', 'rundl') + dbtn('Run now', 'run', 'secondary'),
      function (sheet) { sheet.querySelector('[data-dact="rundl"]').onclick = function () { drawerClose(); runReport(r, true); }; sheet.querySelector('[data-dact="run"]').onclick = function () { drawerClose(); runReport(r, false); }; });
  }
  PAGES.reports = {
    init: function () {
      this.g = Grid({ id: 'gRep', noun: 'reports', key: function (r) { return r.id; }, rows: function () { return D.reports; }, sort: 'name', dir: 'ascending',
        cols: [{ key: 'id', label: 'Report' }, { key: 'name', label: 'Name' }, { key: 'category', label: 'Category' }, { key: 'frequency', label: 'Frequency' }, { key: 'owner', label: 'Owner' },
          { key: 'lastRun', label: 'Last run', val: function (r) { return dt(r.lastRun); }, sortv: function (r) { return r.lastRun; }, raw: 'lastRun' }, { key: 'runs', label: 'Runs', num: 1 }], open: repDrawer });
    },
    render: function () {
      var tx = txIn(), regs = D.regions.filter(function (r) { return D.entities.some(function (e) { return e.region === r && inScope(e.id); }); });
      draw('ch-bfly', { type: 'butterfly-v', categories: regs, categoryLabel: 'Region', unit: '£m', caption: 'Money in and money out by region over the period, GBP millions',
        series: [{ name: 'Money in', values: regs.map(function (r) { return r1(mm(sum(tx.filter(function (t) { return D.ent(t.entity).region === r && t.gbp > 0; }), function (t) { return t.gbp; }))); }) },
                 { name: 'Money out', values: regs.map(function (r) { return r1(mm(-sum(tx.filter(function (t) { return D.ent(t.entity).region === r && t.gbp < 0; }), function (t) { return t.gbp; }))); }) }] });
      var cats = {}; D.reports.forEach(function (r) { cats[r.category] = (cats[r.category] || 0) + 1; });
      var cl = top(Object.keys(cats).map(function (k) { return [k, cats[k]]; }), 5);
      draw('ch-cats', { type: 'pie', categories: cl.map(function (x) { return x[0]; }), categoryLabel: 'Category', caption: 'Number of reports in the library by category', series: [{ name: 'Reports', values: cl.map(function (x) { return x[1]; }) }] });
      var cash = win(cashSeries());
      draw('ch-spark1', { type: 'spark', categories: dayLabels(), categoryLabel: 'Day', unit: '£m', caption: 'Daily group cash, GBP millions', series: [{ name: 'Cash', values: cash.map(function (v) { return r1(mm(v)); }) }] });
      draw('ch-spark2', { type: 'spark', categories: dayLabels(), categoryLabel: 'Day', caption: 'Number of transactions per day', series: [{ name: 'Transactions', values: perDay(tx, function () { return 1; }) }] });
      if (this.g) { this.g.render(); }
      return { count: this.g ? this.g.view().length : 0, total: D.reports.length };
    },
    resolve: function (id) { var r = D.reports.filter(function (x) { return x.id === id; })[0]; if (r) { repDrawer(r); } }
  };

  /* ---------------------------------------------------------------- MESSAGES AND SERVICE REQUESTS */
  function msgDrawer(m) {
    if (!m.read) { m.read = true; S.read[m.id] = true; save(); }
    drawerOpen(m.subject, summary([['From', m.from], ['Received', dt(m.date)], ['Reference', m.id]]) + '<p class="t-ed-body">' + esc(m.body) + '</p>' +
      (m.thread.length ? timeline('Your replies', m.thread) : '') + fText('reply', 'Reply to ' + m.from, 'Sent securely to HSBC (simulated). At least 2 characters.', 1000),
      dbtn('Send reply', 'send') + dbtn('Close', 'close', 'secondary'),
      function (sheet) {
        wireCounter('reply', 1000);
        sheet.querySelector('[data-dact="send"]').onclick = function () {
          var t = $('#reply').value.trim(); if (t.length < 2) { fieldError('reply', 'Write a reply before sending.'); $('#reply').focus(); return; }
          var e = { at: nowStamp(), who: 'You (CEO)', what: 'Reply sent', note: t, kind: 'ok' };
          S.replies[m.id] = (S.replies[m.id] || []).concat([e]); m.thread = S.replies[m.id]; save(); drawerClose(); refresh(); toast('ok', 'Reply sent to ' + m.from + '.');
        };
      });
    refresh();
  }
  function srDrawer(r) {
    var notes = S.replies[r.id] || [];
    drawerOpen(r.id + ' · ' + r.category, summary([['Summary', r.summary], ['Entity', entName(r.entity)], ['Opened', dt(r.opened)], ['Priority', r.priority], ['Status', r.status]].concat(r.details ? [['Details', r.details]] : [])) +
      timeline('Progress', [{ at: dt(r.opened), who: r.mine ? 'You' : 'HSBC Service Centre', what: 'Request opened', kind: 'inf' }].concat(notes)) +
      (r.status !== 'Closed' ? fText('srNote', 'Add a comment for HSBC', 'At least 2 characters.', 600) : ''),
      (r.status !== 'Closed' ? dbtn('Add comment', 'note') : '') + dbtn('Close', 'close', 'secondary'),
      function (sheet) {
        var b = sheet.querySelector('[data-dact="note"]'); if (!b) { return; } wireCounter('srNote', 600);
        b.onclick = function () { var t = $('#srNote').value.trim(); if (t.length < 2) { fieldError('srNote', 'Write a comment before sending.'); $('#srNote').focus(); return; }
          S.replies[r.id] = notes.concat([{ at: nowStamp(), who: 'You (CEO)', what: 'Comment added', note: t, kind: 'ok' }]); save(); drawerClose(); toast('ok', 'Comment added to ' + r.id + '.'); };
      });
  }
  function newSrDrawer() {
    var ents = D.entities.filter(function (e) { return inScope(e.id); });
    drawerOpen('New service request', '<div class="stack-16">' +
      fSelect('srCat', 'Category', ['Payments investigation', 'Account maintenance', 'Mandate change', 'Trade finance amendment', 'Statement request', 'Access and entitlements'].map(function (c) { return [c, c]; }), 'Payments investigation') +
      fSelect('srEnt', 'Entity', ents.map(function (e) { return [e.id, e.name]; }), ents[0] ? ents[0].id : 'E01') +
      fSelect('srPri', 'Priority', [['Standard', 'Standard — within two business days'], ['High', 'High — same business day']], 'Standard') +
      fInput('srSum', 'Summary', 'One line, at least 8 characters.', '', 'text') + fText('srDet', 'Details', 'What happened, what you need, any references. At least 20 characters.', 1000) + '</div>',
      dbtn('Submit request', 'submit') + dbtn('Cancel', 'close', 'secondary'),
      function (sheet) {
        wireFormDD(sheet); wireCounter('srDet', 1000);
        sheet.querySelector('[data-dact="submit"]').onclick = function () {
          var s = $('#srSum').value.trim(), d = $('#srDet').value.trim(), ok = true;
          if (s.length < 8) { fieldError('srSum', 'Give the request a summary of at least 8 characters.'); ok = false; } else { fieldError('srSum', ''); }
          if (d.length < 20) { fieldError('srDet', 'Add at least 20 characters of detail.'); ok = false; } else { fieldError('srDet', ''); }
          if (!ok) { var bad = sheet.querySelector('[aria-invalid="true"]'); if (bad) { bad.focus(); } return; }
          var r = newRequest(ddValue('srCat'), ddValue('srEnt'), ddValue('srPri'), s, d); drawerClose(); refresh(); toast('ok', r.id + ' submitted to HSBC (simulated).');
        };
      });
  }
  PAGES.messages = {
    init: function () {
      this.gM = Grid({ id: 'gMsg', noun: 'messages', key: function (r) { return r.id; }, rows: function () { return D.messages; }, sort: 'date', dir: 'descending',
        cols: [{ key: 'date', label: 'Date', val: function (r) { return dt(r.date); }, sortv: function (r) { return r.date; }, raw: 'date' }, { key: 'from', label: 'From' }, { key: 'subject', label: 'Subject' },
          { key: 'state', label: 'Status', val: function (r) { return r.thread.length ? 'Replied' : r.read ? 'Read' : 'Unread'; }, cell: function (r) { return chip(r.thread.length ? 'ok' : r.read ? 'neu' : 'inf', r.thread.length ? 'Replied' : r.read ? 'Read' : 'Unread'); } }],
        open: msgDrawer });
      this.gS = Grid({ id: 'gSr', noun: 'service requests', key: function (r) { return r.id; }, rows: function () { return D.requests.filter(function (r) { return inScope(r.entity) && (r.mine || inWin(r.opened)); }); }, sort: 'opened', dir: 'descending',
        cols: [{ key: 'id', label: 'Request' }, { key: 'opened', label: 'Opened', val: function (r) { return dt(r.opened); }, sortv: function (r) { return r.opened + (r.created || ''); }, raw: 'opened' }, { key: 'category', label: 'Category' },
          { key: 'entity', label: 'Entity', val: function (r) { return entName(r.entity); } }, { key: 'summary', label: 'Summary' }, { key: 'priority', label: 'Priority' }, { key: 'status', label: 'Status', cell: function (r) { return statusChip(r.status); } }],
        open: srDrawer });
    },
    render: function () {
      var rq = D.requests.filter(function (r) { return inScope(r.entity) && (r.mine || inWin(r.opened)); });
      var perD = win(D.days).map(function (d) { return rq.filter(function (r) { return r.opened === d; }).length; }), b = bucket(perD);
      draw('ch-srday', { type: 'column', categories: b.cats, categoryLabel: nDays() > 14 ? 'Week' : 'Day', caption: 'Service requests opened', series: [{ name: 'Opened', values: b.vals }] });
      var st = ['Open', 'In progress', 'Awaiting your response', 'Closed'].map(function (s) { return [s, rq.filter(function (r) { return r.status === s; }).length]; }).filter(function (x) { return x[1] > 0; });
      if (st.length) { draw('ch-srstat', { type: 'donut', categories: st.map(function (x) { return x[0]; }), categoryLabel: 'Status', caption: 'Service requests by status', series: [{ name: 'Requests', values: st.map(function (x) { return x[1]; }) }] }); }
      if (this.gM) { this.gM.render(); } if (this.gS) { this.gS.render(); }
      return { count: this.gS ? this.gS.view().length : 0, total: rq.length };
    },
    resolve: function (id) { var m = D.messages.filter(function (x) { return x.id === id; })[0]; if (m) { msgDrawer(m); return; } var r = D.requests.filter(function (x) { return x.id === id; })[0]; if (r) { srDrawer(r); } }
  };

  /* ---------------------------------------------------------------- SETTINGS */
  PAGES.settings = {
    init: function () {
      $$('[data-pref]').forEach(function (c) { c.checked = !!S.prefs[c.getAttribute('data-pref')]; c.addEventListener('change', function () { S.prefs[c.getAttribute('data-pref')] = c.checked; save(); refresh(); toast('info', (c.checked ? 'On: ' : 'Off: ') + c.parentNode.textContent.trim() + '.'); }); });
    },
    render: function () {
      var cnt = { approvals: D.payments.filter(function (p) { return inScope(p.entity) && (/Awaiting your/.test(p.status) || inWin(p.due)); }).length, exceptions: exIn().filter(function (x) { return x.material; }).length, messages: D.messages.length, digest: nDays() };
      var ks = [['approvals', 'Approvals'], ['exceptions', 'Exceptions'], ['messages', 'Messages'], ['digest', 'Daily digest']];
      draw('ch-alerts', { type: 'column', categories: ks.map(function (k) { return k[1]; }), categoryLabel: 'Alert type', caption: 'Alerts you would have received at your current settings', series: [{ name: 'Alerts', values: ks.map(function (k) { return S.prefs[k[0]] ? cnt[k[0]] : 0; }) }] });
      return { count: D.entities.filter(function (e) { return inScope(e.id); }).length, total: D.entities.length };
    }
  };

  /* ================================================================== FILTER BAR (Filter-toolbar-bar grammar) + REFRESH */
  var CUR = PAGES[PAGE] || { render: function () { return { count: 0, total: 0 }; } };
  function refresh() {
    var r = CUR.render() || { count: 0, total: 0 };
    var f = S.filters, chips = [];
    if (f.region !== 'all') { chips.push(['region', 'Region: ' + f.region]); }
    if (f.entity !== 'all') { chips.push(['entity', 'Entity: ' + entName(f.entity)]); }
    if (+f.days !== 30) { chips.push(['days', 'Last ' + f.days + ' days']); }
    if (S.q[PAGE]) { chips.push(['q', 'Search: ' + S.q[PAGE]]); }
    if (EXTRA.ccy && PAGE === 'risk') { chips.push(['ccy', 'Currency: ' + EXTRA.ccy]); }
    if (EXTRA.status === 'mine' && PAGE === 'payments') { chips.push(['status', 'Needs me']); }
    var outer = $('#ftb');
    if (outer) {
      outer.setAttribute('data-ftb-state', chips.length ? (r.count ? 'filtered' : 'empty') : 'no-filters');
      $('#ftbCount').textContent = r.count; $('#ftbTotal').textContent = r.total;
      $('#ftbChips .row').innerHTML = chips.map(function (c) { return '<span class="tag t-cm-caption"><span class="lbl">' + esc(c[1]) + '</span><button class="x" type="button" data-chip="' + c[0] + '" aria-label="Remove filter: ' + esc(c[1]) + '"><svg viewBox="0 0 18 18" aria-hidden="true"><use href="#i-close"/></svg></button></span>'; }).join('');
      ['fRegion', 'fEntity', 'fDays'].forEach(function (id) { var d = $('#' + id); if (d && d.__set) { d.__set(id === 'fRegion' ? f.region : id === 'fEntity' ? f.entity : String(f.days)); } });
    }
  }
  function changed() { GRIDS.forEach(function (g) { var st = S.grids[PAGE + '.' + g.cfg.id]; if (st) { st.page = 1; } }); save(); syncURL(); refresh(); }
  function clearChip(k) {
    if (k === 'region') { S.filters.region = 'all'; } else if (k === 'entity') { S.filters.entity = 'all'; } else if (k === 'days') { S.filters.days = 30; }
    else if (k === 'q') { S.q[PAGE] = ''; var q = $('#ftbQ'); if (q) { q.value = ''; } } else if (k === 'ccy') { delete EXTRA.ccy; }
    else if (k === 'status') { EXTRA.status = ''; S.view.payments = 'all'; $$('#payView button').forEach(function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-view') === 'all')); }); $$('.seg').forEach(moveInd); }
  }
  function wireFTB() {
    var r = $('#fRegion'), e = $('#fEntity'), d = $('#fDays'), x = $('#fExport'), q = $('#ftbQ');
    if (r) { wireDD(r, function (v) { S.filters.region = v; if (v !== 'all' && S.filters.entity !== 'all' && D.ent(S.filters.entity).region !== v) { S.filters.entity = 'all'; } changed(); }); }
    if (e) { wireDD(e, function (v) { S.filters.entity = v; if (v !== 'all') { S.filters.region = D.ent(v).region; } changed(); }); }
    if (d) { wireDD(d, function (v) { S.filters.days = +v; changed(); }); }
    if (x) { x.setAttribute('data-no-latch', ''); wireDD(x, function (v) { exportGrid(v); return false; }); }
    if (q) {
      q.value = S.q[PAGE] || ''; var t;
      q.addEventListener('input', function () { clearTimeout(t); t = setTimeout(function () { S.q[PAGE] = q.value.trim(); changed(); }, 180); });
      var c = q.parentNode.querySelector('.clear'); if (c) { c.addEventListener('click', function () { q.value = ''; S.q[PAGE] = ''; changed(); q.focus(); }); }
    }
    var ch = $('#ftbChips'); if (ch) { ch.addEventListener('click', function (ev) { var b = ev.target.closest('[data-chip]'); if (b) { clearChip(b.getAttribute('data-chip')); changed(); var n = $('#ftbChips [data-chip]') || $('#ftbQ') || $('#fRegionT'); if (n) { n.focus(); } } }); }
  }
  function clearAll() { S.filters = { region: 'all', entity: 'all', days: 30 }; S.q[PAGE] = ''; delete EXTRA.ccy; if (PAGE === 'payments') { clearChip('status'); } var q = $('#ftbQ'); if (q) { q.value = ''; } changed(); }

  /* ================================================================== GLOBAL ACTIONS (one delegated listener, rule 14) */
  var ACTIONS = {
    'focus-search': function () { var q = $('#ftbQ') || $('#fRegionT'); if (q) { q.focus(); } },
    'go-settings': function () { location.href = 'settings.html'; },
    'go-approvals': function () { location.href = 'payments.html?status=mine#approvals'; },
    'export-csv': function () { exportGrid('csv'); },
    'clear-filters': clearAll,
    'drawdown': function () { facDrawer(null, true); },
    'next-approval': function () { var p = D.payments.filter(function (x) { return inScope(x.entity) && x.status === 'Awaiting your approval'; }).sort(function (a, b) { return a.due < b.due ? -1 : 1; })[0]; if (p) { payDrawer(p); } else { toast('info', 'Nothing is waiting for your approval in this scope.'); } },
    'quote': quoteDrawer,
    'next-exception': function () { var x = exIn().filter(function (y) { return y.status === 'Open'; }).sort(function (a, b) { return a.severity === 'High' ? -1 : b.severity === 'High' ? 1 : 0; })[0]; if (x) { excDrawer(x); } else { toast('info', 'No open exceptions in this scope.'); } },
    'amend': function () { tfDrawer(null); },
    'run-board': function () { var r = D.reports.filter(function (x) { return x.category === 'Board'; })[0]; runReport(r, true); },
    'new-sr': newSrDrawer,
    'reset': function () { confirmModal('Reset the demo data?', 'This clears approvals, acknowledgements, replies, requests, deals, filters and theme stored in this browser.', 'Reset').then(function (y) { if (!y) { return; } try { localStorage.removeItem(KEY); } catch (e) { /* nothing stored */ } location.href = 'index.html'; }); }
  };
  document.addEventListener('click', function (e) {
    var a = e.target.closest('[data-action]');
    if (a && ACTIONS[a.getAttribute('data-action')]) { e.preventDefault(); ACTIONS[a.getAttribute('data-action')](); return; }
    if (e.target.closest('[data-ftb-clear]')) { clearAll(); return; }
    var cta = e.target.closest('.kpi-tile.has-cta');
    if (cta && !e.target.closest('a')) { location.href = cta.getAttribute('data-href'); return; }
    var da = e.target.closest('#sheet [data-dact="close"]'); if (da) { drawerClose(); return; }
    var tb = e.target.closest('[data-theme-set]'); if (tb) { applyTheme(tb.getAttribute('data-theme-set')); return; }
    var anc = e.target.closest('[data-dp08-anchor]');
    if (anc) { var tg = document.querySelector(anc.getAttribute('href')); if (tg) { e.preventDefault(); tg.scrollIntoView({ block: 'center' }); tg.focus({ preventScroll: true }); } }
  });
  $('#dclose').addEventListener('click', drawerClose); $('#scrim').addEventListener('click', drawerClose);
  $('#mconfirm').addEventListener('click', function () { modalClose(true); }); $('#mcancel').addEventListener('click', function () { modalClose(false); }); $('#mclose').addEventListener('click', function () { modalClose(false); });
  $('#overlay').addEventListener('click', function (e) { if (e.target === $('#overlay')) { modalClose(false); } });

  /* ================================================================== BOOT */
  applyTheme(S.theme);
  wireFTB();
  if (CUR.init) { CUR.init(); }
  syncURL(); refresh();
  requestAnimationFrame(function () { $$('.seg').forEach(moveInd); });
  window.addEventListener('resize', function () { $$('.seg').forEach(moveInd); });
  if (EXTRA.id && CUR.resolve) { var rid = EXTRA.id; setTimeout(function () { CUR.resolve(rid); EXTRA.id = rid; syncURL(); }, 60); }
  window.__proto = { S: S, refresh: refresh, GRIDS: GRIDS };               /* test hook for the driven proof, read-only use */
}());
