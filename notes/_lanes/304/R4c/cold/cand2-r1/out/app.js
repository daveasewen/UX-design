/* CEO international-banking prototype — page runtime (authored JS, s258-D1).
   Reads ONE dataset (window.CEO_DATA, declared once per page as `const DATA`), derives every KPI,
   chart spec, grid row and list from it, and keeps filter / navigation / workflow state in the URL
   and localStorage. Component markup is the pack's (knowledge/snippets); chart geometry is the
   pack's engine (window.dvRender). Nothing here draws a chart or invents a component. */
(function () {
  'use strict';
  var D = window.CEO_DATA;
  var PAGE = document.body.getAttribute('data-page');
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var ENT = {}; D.entities.forEach(function (e) { ENT[e.id] = e; });
  var REG = {}; D.regions.forEach(function (r) { REG[r.id] = r; });
  var ASOF = D.asOf;

  /* ------------------------------------------------------------------ storage (never load-bearing) */
  var store = {
    get: function (k, d) { try { var v = localStorage.getItem('ceo.' + k); return v == null ? d : JSON.parse(v); } catch (e) { return d; } },
    set: function (k, v) { try { localStorage.setItem('ceo.' + k, JSON.stringify(v)); } catch (e) { /* private mode */ } },
    del: function (k) { try { localStorage.removeItem('ceo.' + k); } catch (e) { } }
  };

  /* ------------------------------------------------------------------ workflow overlay (persists) */
  var WF = store.get('wf', null) || { pay: {}, exc: {}, sr: [], msg: {}, srUpd: {} };
  function saveWF() { store.set('wf', WF); }
  function applyWF() {
    D.payments.forEach(function (p) { var w = WF.pay[p.id]; if (w) { p.status = w.status; p.note = w.note; p.decidedAt = w.at; } });
    D.exceptions.forEach(function (x) {
      var w = WF.exc[x.id]; if (!w) { return; }
      x.status = 'Acknowledged';
      x.audit = x.audit.slice(0, 1).concat(w.audit);
    });
    var have = {}; D.requests.forEach(function (r) { have[r.id] = 1; });
    WF.sr.forEach(function (r) { if (!have[r.id]) { D.requests.unshift(r); have[r.id] = 1; } });
    D.requests.forEach(function (r) { var u = WF.srUpd[r.id]; if (u) { r.status = u.status; r.thread = u.thread; } });
    D.messages.forEach(function (m) { var w = WF.msg[m.id]; if (w) { m.unread = !w.read ? m.unread : false; m.thread = w.thread || []; } });
  }
  applyWF();

  /* ------------------------------------------------------------------ formatting */
  function grp(n, dp) { return Number(n).toFixed(dp).replace(/\B(?=(\d{3})+(?!\d))/g, ','); }
  function money(v) { return (v < 0 ? '−' : '') + '£' + grp(Math.abs(v), 2); }
  function mShort(v) {
    var a = Math.abs(v), s = a >= 1e9 ? grp(a / 1e9, 2) + 'bn' : grp(a / 1e6, 1) + 'm';
    return (v < 0 ? '−' : '') + '£' + s;
  }
  function inCcy(v, ccy) { return (v < 0 ? '−' : '') + grp(Math.abs(v), 2) + ' ' + ccy; }
  var MON = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  function dLabel(iso) { var p = iso.split('-'); return +p[2] + ' ' + MON[+p[1] - 1]; }
  function dLong(iso) { var p = iso.slice(0, 10).split('-'); return +p[2] + ' ' + MON[+p[1] - 1] + ' ' + p[0]; }
  function nowStamp() { var d = new Date(); return d.toISOString().slice(0, 16); }
  function r1(v) { return Math.round(v * 10) / 10; }
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function sum(a, f) { var t = 0; a.forEach(function (x) { t += f ? f(x) : x; }); return t; }
  function rate(ccy) { return D.fx[ccy]; }
  function fxLine(ccy) { return ccy === 'GBP' ? 'GBP reporting currency' : '1 ' + ccy + ' = £' + rate(ccy).toFixed(ccy === 'JPY' ? 6 : 4) + ' (illustrative)'; }

  /* ------------------------------------------------------------------ shared filters: URL > storage > defaults */
  var DEF = store.get('defaults', { entity: 'all', range: '30' });
  var F = store.get('filters', null) || { entity: DEF.entity || 'all', region: 'all', range: DEF.range || '30' };
  (function () {
    var q = new URLSearchParams(location.search);
    ['entity', 'region', 'range'].forEach(function (k) { if (q.get(k)) { F[k] = q.get(k); } });
    if (!ENT[F.entity]) { F.entity = 'all'; }
    if (!REG[F.region]) { F.region = 'all'; }
    if (['7', '14', '30'].indexOf(String(F.range)) < 0) { F.range = '30'; }
  }());
  function entOk(eid) { return (F.entity === 'all' || F.entity === eid) && (F.region === 'all' || (ENT[eid] && ENT[eid].region === F.region)); }
  function days() { return D.days.slice(30 - (+F.range)); }
  function i0() { return 30 - (+F.range); }
  function inRange(iso) { return iso.slice(0, 10) >= D.days[i0()] && iso.slice(0, 10) <= ASOF; }
  function qs(extra) {
    var q = new URLSearchParams();
    if (F.entity !== 'all') { q.set('entity', F.entity); }
    if (F.region !== 'all') { q.set('region', F.region); }
    if (F.range !== '30') { q.set('range', F.range); }
    if (extra) { Object.keys(extra).forEach(function (k) { q.set(k, extra[k]); }); }
    var s = q.toString(); return s ? '?' + s : '';
  }
  function decorateLinks() {
    $$('a[href]').forEach(function (a) {
      var h = a.getAttribute('href');
      var m = /^([a-z]+\.html)(\?[^#]*)?(#.*)?$/.exec(h); if (!m) { return; }
      var q = new URLSearchParams(m[2] || ''), keep = {};
      q.forEach(function (v, k) { if (['entity', 'region', 'range'].indexOf(k) < 0) { keep[k] = v; } });
      if (!a.hasAttribute('data-region-link')) {
        a.setAttribute('href', m[1] + qs(keep) + (m[3] || ''));
      }
    });
  }
  function writeFilters() {
    store.set('filters', F);
    var q = new URLSearchParams(location.search); ['entity', 'region', 'range'].forEach(function (k) { q.delete(k); });
    var extra = {}; q.forEach(function (v, k) { extra[k] = v; });
    try { history.replaceState(null, '', location.pathname + qs(extra) + location.hash); } catch (e) { }
    decorateLinks();
  }

  /* ------------------------------------------------------------------ dropdown + segmented values (component scripts run first) */
  function ddSet(dd, value) {
    if (!dd) { return; }
    var opts = $$('[role=option]', dd), hit = null;
    opts.forEach(function (o) { var on = o.getAttribute('data-value') === String(value); o.setAttribute('aria-selected', String(on)); if (on) { hit = o; } });
    if (hit) { $('.ddval', dd).textContent = hit.firstChild.textContent.trim(); }
  }
  function ddGet(dd) { var o = $('[role=option][aria-selected="true"]', dd); return o ? o.getAttribute('data-value') : null; }
  function segSet(seg, value) {
    if (!seg) { return; }
    $$('button', seg).forEach(function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-value') === String(value))); });
    requestAnimationFrame(function () { window.dispatchEvent(new Event('resize')); });
  }
  function segGet(seg) { var b = $('button[aria-pressed="true"]', seg); return b ? b.getAttribute('data-value') : null; }
  function syncControls() {
    ddSet($('#f-entity'), F.entity); ddSet($('#f-region'), F.region); segSet($('#f-range'), F.range);
    var th = document.documentElement.getAttribute('data-theme');
    $$('[data-pref="theme"]').forEach(function (s) { segSet(s, th); });
  }
  function onChoice(el, value) {
    var dd = el.closest('.dd'), sg = el.closest('.seg');
    var host = dd || sg; if (!host) { return; }
    var filt = host.getAttribute('data-filter'), pref = host.getAttribute('data-pref'), lf = host.getAttribute('data-list-filter');
    if (filt) {
      F[filt] = value;
      if (filt === 'entity' && value !== 'all') { F.region = 'all'; }
      if (filt === 'region' && F.entity !== 'all' && ENT[F.entity].region !== value && value !== 'all') { F.entity = 'all'; }
      syncControls(); writeFilters(); refresh();
      announce('Filters: ' + (F.entity === 'all' ? 'all entities' : ENT[F.entity].name) + ', ' + (F.region === 'all' ? 'all regions' : REG[F.region].name) + ', last ' + F.range + ' days.');
      return;
    }
    if (pref === 'theme') { setTheme(value); return; }
    if (pref === 'entity' || pref === 'range') { DEF[pref] = value; store.set('defaults', DEF); toast('ok', 'Default ' + (pref === 'entity' ? 'entity' : 'date range') + ' saved.'); return; }
    if (lf) { LISTS.forEach(function (L) { if (L.filterHost === host.id) { L.page = 1; L.render(); } }); return; }
  }
  document.addEventListener('click', function (e) {
    var o = e.target.closest('.dd [role=option]');
    if (o) { onChoice(o, o.getAttribute('data-value')); return; }
    var b = e.target.closest('.seg button[data-value]');
    if (b && !b.closest('figure')) { onChoice(b, b.getAttribute('data-value')); }
  });
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Enter' && e.key !== ' ') { return; }
    var o = e.target.closest && e.target.closest('.dd [role=option]');
    if (o) { onChoice(o, o.getAttribute('data-value')); }
  });

  /* ------------------------------------------------------------------ theme */
  function setTheme(t) {
    document.documentElement.setAttribute('data-theme', t);
    try { localStorage.setItem('ceo.theme', t); } catch (e) { }
    $$('[data-pref="theme"]').forEach(function (s) { segSet(s, t); });
    announce((t === 'dark' ? 'Dark' : 'Light') + ' mode.');
  }

  /* ------------------------------------------------------------------ live region + toast (Toast snippet's spawn, re-authored) */
  var live = document.createElement('div'); live.className = 'visually-hidden'; live.setAttribute('role', 'status');
  live.setAttribute('aria-live', 'polite'); live.id = 'ceo-live';
  $('.cn-toast').appendChild(live);
  function announce(msg) { live.textContent = ''; requestAnimationFrame(function () { live.textContent = msg; }); }
  var RM = matchMedia('(prefers-reduced-motion: reduce)').matches;
  function toast(status, msg) {
    var region = $('#toastRegion'); if (!region) { return; }
    var glyph = { ok: 'to-success', info: 'to-info', warn: 'to-warning' }[status];
    var origin = document.activeElement;
    var t = document.createElement('div'); t.className = 'toast ' + status; t.setAttribute('role', 'status');
    if (glyph) { t.setAttribute('data-carries', 'symbol label'); }
    t.innerHTML = (glyph ? '<span class="ic"><svg aria-hidden="true"><use href="#' + glyph + '"/></svg></span>' : '') +
      '<p class="msg t-ed-body">' + esc(msg) + '</p><button class="x" type="button" aria-label="Dismiss message"><svg aria-hidden="true"><use href="#to-close"/></svg></button>';
    region.appendChild(t);
    var remain = 6000, started = Date.now(), timer = setTimeout(leave, remain), paused = false;
    function leave() { if (RM) { t.remove(); return; } t.classList.add('leaving'); t.addEventListener('transitionend', function () { t.remove(); }, { once: true }); setTimeout(function () { t.remove(); }, 800); }
    function pause() { if (paused) { return; } paused = true; clearTimeout(timer); remain -= Date.now() - started; }
    function resume() { if (!paused) { return; } paused = false; started = Date.now(); timer = setTimeout(leave, Math.max(remain, 1000)); }
    t.addEventListener('mouseenter', pause); t.addEventListener('mouseleave', resume);
    t.addEventListener('focusin', pause); t.addEventListener('focusout', resume);
    var self = t.querySelector('.x');
    self.addEventListener('click', function () {
      clearTimeout(timer); leave();
      var nxt = $$('.toast:not(.leaving) .x', region).filter(function (b) { return b !== self; })[0];
      var home = nxt || origin; if (home && document.body.contains(home)) { home.focus(); }
    });
  }

  /* ------------------------------------------------------------------ drawer (Drawer snippet mechanics, re-authored for many records) */
  var DR = { sheet: $('#sheet'), scrim: $('#scrim'), title: $('#dtitle'), body: $('#dbody'), act: $('#act'), cancel: $('#cancel'), close: $('#close'), opener: null, onAct: null, onCancel: null };
  var BG = function () { return [$('.cn-app-shell-side-nav')]; };
  function drFocusable() { return $$('button,[href],input,textarea,select,[tabindex]:not([tabindex="-1"])', DR.sheet).filter(function (el) { return !el.disabled && el.offsetParent !== null; }); }
  function drawer(opts) {
    DR.opener = document.activeElement;
    DR.title.textContent = opts.title;
    DR.body.innerHTML = opts.body;
    DR.onAct = opts.act ? opts.act.fn : null; DR.onCancel = opts.cancel ? opts.cancel.fn : null;
    DR.act.hidden = !opts.act; if (opts.act) { DR.act.textContent = opts.act.label; }
    DR.cancel.textContent = opts.cancel ? opts.cancel.label : 'Close';
    DR.scrim.classList.add('open'); DR.sheet.classList.add('open');
    requestAnimationFrame(function () { requestAnimationFrame(function () {
      var f = drFocusable(); if (f.length) { (opts.focus ? $(opts.focus, DR.sheet) || f[0] : f[0]).focus(); }
      BG().forEach(function (b) { b.inert = true; b.setAttribute('aria-hidden', 'true'); });
    }); });
    if (opts.after) { opts.after(DR.body); }
  }
  function drawerClose() {
    if (!DR.sheet.classList.contains('open')) { return; }
    DR.scrim.classList.remove('open'); DR.sheet.classList.remove('open');
    BG().forEach(function (b) { b.inert = false; b.removeAttribute('aria-hidden'); });
    var u = new URL(location.href); if (u.searchParams.has('open')) { u.searchParams.delete('open'); try { history.replaceState(null, '', u.pathname + u.search + u.hash); } catch (e) { } }
    if (DR.opener && document.body.contains(DR.opener)) { DR.opener.focus(); }
  }
  if (DR.sheet) {
    DR.close.addEventListener('click', drawerClose);
    DR.scrim.addEventListener('click', drawerClose);
    DR.cancel.addEventListener('click', function () { if (DR.onCancel) { DR.onCancel(); } else { drawerClose(); } });
    DR.act.addEventListener('click', function () { if (DR.onAct) { DR.onAct(); } });
    document.addEventListener('keydown', function (e) {
      if (!DR.sheet.classList.contains('open')) { return; }
      if (e.key === 'Escape') { drawerClose(); return; }
      if (e.key === 'Tab') {
        var f = drFocusable(), a = f[0], z = f[f.length - 1];
        if (e.shiftKey && document.activeElement === a) { e.preventDefault(); z.focus(); }
        else if (!e.shiftKey && document.activeElement === z) { e.preventDefault(); a.focus(); }
      }
    });
  }

  /* ------------------------------------------------------------------ modal (Modals snippet mechanics; never opened over the drawer) */
  var MD = { ov: $('#mOverlay'), title: $('#mTitle'), body: $('#mBody'), ok: $('#mConfirm'), no: $('#mCancel'), x: $('#mClose'), cb: null, opener: null };
  function mFocusable() { return $$('button,[href],[tabindex]:not([tabindex="-1"])', MD.ov).filter(function (el) { return !el.disabled; }); }
  function modal(title, bodyHTML, okLabel, cb) {
    MD.opener = document.activeElement; MD.cb = cb;
    MD.title.textContent = title; MD.body.innerHTML = bodyHTML; MD.ok.textContent = okLabel; MD.no.textContent = 'Cancel';
    BG().forEach(function (b) { b.inert = true; b.setAttribute('aria-hidden', 'true'); });
    requestAnimationFrame(function () { requestAnimationFrame(function () { MD.ov.classList.add('open'); }); });
    setTimeout(function () { MD.ok.focus(); }, 60);
  }
  function modalClose(ok) {
    MD.ov.classList.remove('open'); BG().forEach(function (b) { b.inert = false; b.removeAttribute('aria-hidden'); });
    if (MD.opener && document.body.contains(MD.opener)) { MD.opener.focus(); }
    var cb = MD.cb; MD.cb = null; if (ok && cb) { cb(); }
  }
  if (MD.ov) {
    MD.ok.addEventListener('click', function () { modalClose(true); });
    MD.no.addEventListener('click', function () { modalClose(false); });
    MD.x.addEventListener('click', function () { modalClose(false); });
    MD.ov.addEventListener('click', function (e) { if (e.target === MD.ov) { modalClose(false); } });
    document.addEventListener('keydown', function (e) {
      if (!MD.ov.classList.contains('open')) { return; }
      if (e.key === 'Escape') { modalClose(false); return; }
      if (e.key === 'Tab') { var f = mFocusable(), a = f[0], z = f[f.length - 1];
        if (e.shiftKey && document.activeElement === a) { e.preventDefault(); z.focus(); }
        else if (!e.shiftKey && document.activeElement === z) { e.preventDefault(); a.focus(); } }
    });
  }

  /* ------------------------------------------------------------------ markup copied from snippets (runtime templates) */
  function summary(rows, total) {
    return '<div class="cn-summary"><dl class="summary">' + rows.map(function (r, i) {
      return '<div class="summary__row' + (total && i === rows.length - 1 ? ' summary__row--total' : '') + '"><dt class="summary__k">' + esc(r[0]) + '</dt><dd class="summary__v">' + (r[2] ? r[1] : esc(r[1])) + '</dd></div>';
    }).join('') + '</dl></div>';
  }
  var TONE = { 'Awaiting your approval': 'warn', 'Awaiting second approver': 'inf', 'Approved': 'ok', 'Released': 'ok', 'Rejected': 'err',
    'Open': 'warn', 'Acknowledged': 'ok', 'High': 'err', 'Medium': 'warn', 'Low': 'inf', 'Submitted': 'inf', 'In progress': 'inf',
    'Awaiting your input': 'warn', 'Resolved': 'ok', 'Settled': 'ok', 'Pending': 'warn', 'Issued': 'ok', 'Expired': 'err',
    'Amendment pending': 'warn', 'Documents presented': 'inf', 'Discrepancies noted': 'err', 'Awaiting acceptance': 'warn' };
  function chip(label, tone) {
    return '<span class="chip ' + (tone || TONE[label] || 'inf') + '"><span class="dot" aria-hidden="true"></span>' + esc(label) + '</span>';
  }
  function chips(labels) { return '<div class="cn-status-indicator"><div class="chips">' + labels.map(function (l) { return chip(l[0], l[1]); }).join('') + '</div></div>'; }
  function statusDot(label, tone) { return '<span class="status ' + (tone || TONE[label] || 'inf') + '" data-carries="label"><span class="dot" aria-hidden="true"></span>' + esc(label) + '</span>'; }
  function alertBox(kind, title, text) {
    var ic = { err: 'al-error', warn: 'al-warning', ok: 'al-success', info: 'al-info' }[kind];
    return '<div class="cn-alert"><div class="alert ' + kind + '" role="' + (kind === 'err' ? 'alert' : 'status') + '" data-carries="symbol label"><span class="ic"><svg aria-hidden="true"><use href="#' + ic + '"/></svg></span><p class="main t-ed-body"><strong class="em">' + esc(title) + '</strong> ' + esc(text) + '</p></div></div>';
  }
  function textarea(id, label, help, max, min) {
    return '<div class="cn-textarea"><div class="tx-group" id="' + id + '-group"><div class="tx-lblrow"><label class="t-cm-label" for="' + id + '">' + esc(label) + '</label></div>' +
      '<div class="tx-box"><textarea id="' + id + '" class="t-ed-body" maxlength="' + max + '" rows="3" aria-describedby="' + id + '-help ' + id + '-count" data-min="' + (min || 0) + '"></textarea></div>' +
      '<div class="tx-foot"><p class="tx-help t-ed-body-small" id="' + id + '-help">' + esc(help) + '</p><span class="tx-count t-cm-legal" id="' + id + '-count">0/' + max + '</span></div></div></div>';
  }
  function checkbox(id, label) {
    return '<div class="cn-selection-controls"><div class="sc"><div class="field"><input type="checkbox" id="' + id + '"><label for="' + id + '"><span class="box"><svg data-bespoke="checkbox tick, animated stroke-draw control glyph" viewBox="0 0 18 18"><path class="tick" d="M3.5 9.5 L7.5 13.5 L14.5 5"/></svg></span> ' + esc(label) + '</label></div></div></div>';
  }
  function timeline(title, items) {
    return '<div class="cn-timeline"><section class="tl" aria-label="' + esc(title) + '"><div class="tl-group"><h4 class="t-cm-caption">' + esc(title) + '</h4><ol class="tl-list">' +
      items.map(function (it) {
        return '<li class="' + (it.tone || 'inf') + '"><span class="tl-node" aria-hidden="true"></span><span class="tl-line"><span class="tl-title t-cm-ctl-14">' + esc(it.title) + '</span></span>' +
          '<span class="tl-meta"><time class="t-cm-legal" datetime="' + esc(it.at) + '">' + esc(dLong(it.at) + (it.at.length > 10 ? ', ' + it.at.slice(11, 16) : '')) + '</time>' + (it.who ? '<span class="t-cm-legal">' + esc(it.who) + '</span>' : '') + '</span>' +
          (it.desc ? '<p class="tl-desc t-ed-body-small">' + esc(it.desc) + '</p>' : '') + '</li>';
      }).join('') + '</ol></div></section></div>';
  }
  function stack(parts) { return '<div class="cn-layout-utilities"><div class="l-stack" data-gap="m">' + parts.join('') + '</div></div>'; }
  function wireCounter(id) {
    var t = document.getElementById(id); if (!t) { return; }
    var c = document.getElementById(id + '-count'), max = +t.getAttribute('maxlength');
    t.addEventListener('input', function () { c.textContent = t.value.length + '/' + max; });
  }
  function fieldError(id, msg) {
    var g = document.getElementById(id + '-group') || document.getElementById(id + '-field');
    var t = document.getElementById(id);
    var old = g && g.querySelector('.err-msg'); if (old) { old.remove(); }
    if (g) { g.classList.toggle('is-error', !!msg); }
    if (t) { if (msg) { t.setAttribute('aria-invalid', 'true'); } else { t.removeAttribute('aria-invalid'); } }
    if (msg && g) {
      var p = document.createElement('div'); p.className = 'err-msg';
      p.innerHTML = '<span class="ic" aria-hidden="true"><svg class="icn" viewBox="0 0 18 18"><use href="#ic-error"/></svg></span><p id="' + id + '-err">' + esc(msg) + '</p>';
      g.appendChild(p);
      t.setAttribute('aria-describedby', (t.getAttribute('aria-describedby') || '').replace(' ' + id + '-err', '') + ' ' + id + '-err');
    }
    return !msg;
  }

  /* ------------------------------------------------------------------ CSV export (browser-only file) */
  function csv(rows, cols) {
    var q = function (v) { v = v == null ? '' : String(v); return /[",\n]/.test(v) ? '"' + v.replace(/"/g, '""') + '"' : v; };
    return [cols.map(function (c) { return q(c[0]); }).join(',')].concat(rows.map(function (r) { return cols.map(function (c) { return q(typeof c[1] === 'function' ? c[1](r) : r[c[1]]); }).join(','); })).join('\n');
  }
  function download(name, text) {
    var blob = new Blob([text], { type: 'text/csv;charset=utf-8' });
    var a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = name;
    document.body.appendChild(a); a.click(); setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 500);
    window.CEO_LAST_EXPORT = { name: name, bytes: text.length, lines: text.split('\n').length };
    toast('ok', 'Exported ' + name + ' (' + (text.split('\n').length - 1) + ' rows).');
  }
  function stampName(base) { return base + '-' + ASOF + (F.entity !== 'all' ? '-' + F.entity : '') + (F.region !== 'all' ? '-' + F.region : '') + '.csv'; }

  /* ------------------------------------------------------------------ derived measures */
  function series() {
    var n = 30, cash = [], restricted = [], undrawn = [], liquidity = [], headroom = [];
    var accs = D.accounts.filter(function (a) { return entOk(a.entity); });
    var facs = D.facilities.filter(function (f) { return entOk(f.entity); });
    var buffer = sum(Object.keys(D.buffers).filter(entOk), function (k) { return D.buffers[k]; });
    var out = committedOut();
    for (var i = 0; i < n; i++) {
      var c = sum(accs, function (a) { return a.balGbp[i]; }), r = sum(accs.filter(function (a) { return a.restricted; }), function (a) { return a.balGbp[i]; });
      var u = sum(facs, function (f) { return f.undrawnSeries[i]; });
      cash.push(c); restricted.push(r); undrawn.push(u); liquidity.push(c - r + u); headroom.push(c - r + u - out - buffer);
    }
    return { cash: cash, restricted: restricted, undrawn: undrawn, liquidity: liquidity, headroom: headroom, buffer: buffer, out: out };
  }
  function committedOut() {
    var f = D.forecast.filter(function (x) { return entOk(x.entity) && x.gbp < 0 && x.certainty === 'Committed'; });
    var p = D.payments.filter(function (x) { return entOk(x.entity) && /^Awaiting|^Approved/.test(x.status); });
    return -sum(f, function (x) { return x.gbp; }) + sum(p, function (x) { return x.gbp; });
  }
  function outflowLadder() {
    var byDay = {}; D.forecast.forEach(function (x) { if (entOk(x.entity) && x.gbp < 0 && x.certainty === 'Committed') { byDay[x.date] = (byDay[x.date] || 0) - x.gbp; } });
    var t = sum(D.payments.filter(function (x) { return entOk(x.entity) && /^Awaiting|^Approved/.test(x.status); }), function (x) { return x.gbp; });
    var out = [], d = new Date(ASOF + 'T00:00:00Z');
    for (var i = 1; i <= 30; i++) { d.setUTCDate(d.getUTCDate() + 1); t += byDay[d.toISOString().slice(0, 10)] || 0; out.push(t); }
    return out;
  }
  function trailingOutflows() { return -sum(D.transactions.filter(function (t) { return entOk(t.entity) && t.gbp < 0; }), function (t) { return t.gbp; }); }
  function bucketCcy(c) { return ['USD', 'EUR', 'GBP'].indexOf(c) >= 0 ? c : (['HKD', 'SGD', 'CNY', 'JPY', 'INR'].indexOf(c) >= 0 ? 'Asian currencies' : 'Other'); }

  /* ------------------------------------------------------------------ KPI tiles (Kpi-tile markup; inline spark geometry = the snippet's 200×48 grammar) */
  function setKpi(key, vals, opts) {
    var tile = $('.kpi-tile[data-kpi="' + key + '"]'); if (!tile) { return; }
    opts = opts || {};
    var v = vals.slice(i0()), last = opts.value != null ? opts.value : v[v.length - 1], first = opts.base != null ? opts.base : v[0];
    var pct = first ? (last - first) / Math.abs(first) * 100 : 0;
    var dir = Math.abs(pct) < 0.05 ? 'flat' : (pct > 0 ? 'up' : 'down');
    var val = mShort(last);
    tile.querySelector('[data-f="value"]').textContent = val.replace(/^−?£/, function (m) { return m.charAt(0) === '−' ? '−' : ''; });
    tile.querySelector('.unit').textContent = '£';
    var dl = tile.querySelector('.kpi-delta'); dl.className = 'kpi-delta ' + dir;
    dl.querySelector('use').setAttribute('href', '#kpi-' + dir);
    tile.querySelector('[data-f="delta"]').textContent = dir === 'flat' ? 'No change' : (pct > 0 ? '+' : '−') + Math.abs(pct).toFixed(1) + '% ' + dir;
    tile.querySelector('[data-f="per"]').textContent = opts.per || ('vs ' + dLabel(D.days[i0()]));
    tile.setAttribute('aria-label', tile.querySelector('.kpi-link').textContent + ': ' + val + ', ' + tile.querySelector('[data-f="delta"]').textContent + ' ' + tile.querySelector('[data-f="per"]').textContent);
    var sv = opts.spark || v, mn = Math.min.apply(null, sv), mx = Math.max.apply(null, sv), span = mx - mn || 1;
    var pts = sv.map(function (x, i) { return (3 + i * 194 / Math.max(1, sv.length - 1)).toFixed(1) + ',' + (45 - (x - mn) / span * 42).toFixed(1); });
    var svg = tile.querySelector('.spark-inline');
    svg.setAttribute('data-trend', sv[sv.length - 1] > sv[0] ? 'up' : sv[sv.length - 1] < sv[0] ? 'down' : 'flat');
    svg.querySelector('.dv-series').setAttribute('points', pts.join(' '));
    svg.querySelector('.dv-area').setAttribute('points', pts.join(' ') + ' 197.0,45 3.0,45');
  }

  /* ------------------------------------------------------------------ charts: spec from DATA -> the pack's engine */
  function chart(id, spec) {
    var fig = document.getElementById(id); if (!fig || !window.dvRender) { return; }
    if (!spec.categories.length) {
      spec.categories = ['Nothing matches the filters'];
      spec.series = spec.series.map(function (s) { var o = {}; for (var k in s) { o[k] = s[k]; } o.values = [0]; return o; });
    }
    try { window.dvRender(fig, spec); } catch (e) { console.error(e); }
  }
  function m(v) { return r1(v / 1e6); }

  /* ------------------------------------------------------------------ the data grid: bind this page's rows to the pack's grid */
  var GRID = null;
  try { GRID = (0, eval)('typeof DATA !== "undefined" && typeof state !== "undefined" ? { rows: DATA, state: state, render: render } : null'); } catch (e) { GRID = null; }
  var GRID_OPEN = null, GRID_SRC = [];
  function gridSetup(cfg) {
    if (!GRID) { return; }
    var tbl = $('#tbl');
    $('#dgTitle').textContent = cfg.title;
    Object.keys(cfg.cols).forEach(function (k) {
      var th = $('th[data-key="' + k + '"]', tbl); if (!th) { return; }
      th.querySelector('.lbl').textContent = cfg.cols[k];
      var sb = th.querySelector('.colf'); if (sb) { sb.setAttribute('aria-label', 'Filter by ' + cfg.cols[k].toLowerCase()); }
      var ml = th.querySelector('.cml'); if (ml) { ml.textContent = cfg.cols[k] + ' contains'; }
      var cm = th.querySelector('.colmenu'); if (cm) { cm.setAttribute('aria-label', 'Filter by ' + cfg.cols[k].toLowerCase()); }
      var rz = th.querySelector('.rsz'); if (rz) { rz.setAttribute('aria-label', 'Resize ' + cfg.cols[k].toLowerCase() + ' column'); }
    });
    var gl = $$('thead tr.grp .glabel', tbl); if (gl[0]) { gl[0].textContent = cfg.group; } if (gl[1]) { gl[1].textContent = 'Value (GBP)'; }
    var s = $('#dgSearch'); s.setAttribute('aria-label', 'Filter ' + cfg.noun); s.setAttribute('placeholder', 'Filter ' + cfg.noun + ' — press enter to apply');
    GRID_OPEN = cfg.open;
    var saved = store.get('grid.' + PAGE, null);
    GRID.state.pageSize = cfg.pageSize || 12; $('#pp').value = String(GRID.state.pageSize);
    if (saved) {
      GRID.state.pageSize = saved.pageSize || 8; GRID.state.page = saved.page || 1;
      $('#pp').value = String(GRID.state.pageSize);
      if (saved.sortKey) {
        GRID.state.sortKey = saved.sortKey; GRID.state.sortDir = saved.sortDir;
        var th = $('thead tr.cols th[data-key="' + saved.sortKey + '"]', tbl); if (th) { th.setAttribute('aria-sort', saved.sortDir); }
      }
    }
    function persist() { setTimeout(function () { store.set('grid.' + PAGE, { pageSize: GRID.state.pageSize, page: GRID.state.page, sortKey: GRID.state.sortKey, sortDir: GRID.state.sortDir }); }, 0); }
    $('#dg').addEventListener('click', persist); $('#dg').addEventListener('change', persist); $('#dg').addEventListener('keydown', persist);
    // open a record: click a body cell (not the checkbox or the editable reference), or Enter on one
    $('#tbody').addEventListener('click', function (e) {
      if (e.target.closest('td.sel, td.edit, input, button')) { return; }
      var tr = e.target.closest('tr[data-id]'); if (tr && GRID_OPEN) { GRID_OPEN(+tr.getAttribute('data-id')); }
    });
    tbl.addEventListener('keydown', function (e) {
      if (e.key !== 'Enter') { return; }
      var td = e.target.closest('tbody td'); if (!td || td.classList.contains('edit') || td.classList.contains('sel')) { return; }
      var tr = td.closest('tr[data-id]'); if (tr && GRID_OPEN) { e.preventDefault(); GRID_OPEN(+tr.getAttribute('data-id')); }
    });
  }
  function gridRows(rows, src) {
    if (!GRID) { return; }
    GRID_SRC = src || rows;
    GRID.rows.length = 0; Array.prototype.push.apply(GRID.rows, rows);
    var ids = {}; rows.forEach(function (r) { ids[r.id] = 1; });
    GRID.state.sel.forEach(function (id) { if (!ids[id]) { GRID.state.sel.delete(id); } });
    GRID.render();
    var h = $('#gridHead'); if (h) { h.setAttribute('data-count', rows.length); }
  }
  function gridSelected() { return GRID ? Array.from(GRID.state.sel) : []; }

  /* ------------------------------------------------------------------ list-items + pagination + search */
  var LISTS = [];
  function list(cfg) {
    var L = { id: cfg.id, page: 1, size: cfg.size || 5, filterHost: cfg.filterHost, cfg: cfg };
    var ul = document.getElementById(cfg.id), q = document.getElementById(cfg.id + '-q'), pg = document.getElementById(cfg.id + '-pg'), cnt = document.getElementById(cfg.id + '-count');
    L.render = function () {
      var term = (q.value || '').trim().toLowerCase();
      var host = cfg.filterHost ? document.getElementById(cfg.filterHost) : null;
      var fv = host ? (host.classList.contains('seg') ? segGet(host) : ddGet(host)) : 'all';
      var rows = cfg.rows().filter(function (r) { return (fv === 'all' || cfg.match(r, fv)) && (!term || cfg.text(r).toLowerCase().indexOf(term) >= 0); });
      var pages = Math.max(1, Math.ceil(rows.length / L.size)); L.page = Math.min(L.page, pages);
      var slice = rows.slice((L.page - 1) * L.size, L.page * L.size);
      cnt.textContent = rows.length + ' ' + (rows.length === 1 ? cfg.noun1 : cfg.noun) + (term ? ' matching "' + q.value.trim() + '"' : '');
      ul.innerHTML = slice.length ? slice.map(function (r) {
        var x = cfg.row(r);
        return '<li><button class="row" type="button" data-id="' + esc(r.id) + '"><span class="avatar" role="img" aria-label="' + esc(x.who) + '">' + esc(x.ini) + '</span><span class="body">' +
          '<span class="line"><span class="title">' + esc(x.title) + '</span>' + statusDot(x.status, x.tone) + '</span>' +
          '<span class="line"><span class="desc">' + esc(x.desc) + '</span><span class="amount">' + esc(x.right || '') + '</span></span></span></button></li>';
      }).join('') : '<li><div class="cn-empty-state"><section class="empty" aria-label="Nothing to show"><h3 class="t-ed-heading-4 em">Nothing matches</h3><p class="t-ed-body-small">Try a different search, or widen the filters above.</p></section></div></li>';
      var h = '<li><button class="ctrl" type="button" aria-label="Previous page" data-go="prev"' + (L.page === 1 ? ' disabled' : '') + '><svg viewBox="0 0 18 18" aria-hidden="true"><use href="#ic-chevron-left"/></svg></button></li>';
      for (var p = 1; p <= pages; p++) { h += '<li><a href="#" data-go="' + p + '"' + (p === L.page ? ' aria-current="page" aria-label="Page ' + p + ', current page"' : ' aria-label="Page ' + p + '"') + '>' + p + '</a></li>'; }
      h += '<li><button class="ctrl" type="button" aria-label="Next page" data-go="next"' + (L.page === pages ? ' disabled' : '') + '><svg viewBox="0 0 18 18" aria-hidden="true"><use href="#ic-chevron-right"/></svg></button></li>';
      pg.querySelector('ul').innerHTML = h;
      store.set('list.' + cfg.id, { page: L.page, q: q.value });
    };
    var saved = store.get('list.' + cfg.id, null); if (saved) { L.page = saved.page || 1; q.value = saved.q || ''; }
    q.addEventListener('input', function () { L.page = 1; L.render(); });
    pg.addEventListener('click', function (e) {
      var t = e.target.closest('[data-go]'); if (!t) { return; } e.preventDefault();
      var g = t.getAttribute('data-go'); L.page = g === 'prev' ? L.page - 1 : g === 'next' ? L.page + 1 : +g; L.render();
      var cur = pg.querySelector('[aria-current="page"]'); if (cur) { cur.focus(); }
      announce('Page ' + L.page + '.');
    });
    ul.addEventListener('click', function (e) { var b = e.target.closest('button.row'); if (b) { cfg.open(b.getAttribute('data-id')); } });
    LISTS.push(L); return L;
  }
  function refreshLists() { LISTS.forEach(function (L) { L.render(); }); }

  /* ================================================================== records + workflows */
  function ent(eid) { return ENT[eid] ? ENT[eid].name : eid; }
  function shortEnt(eid) { return ENT[eid] ? ENT[eid].name.replace('Meridian ', '').replace(/ (plc|GmbH|Inc\.|Ltda|Ltd|Pte Ltd|Co|FZE)$/, '') : eid; }

  // ---- payments
  function payById(id) { return D.payments.filter(function (p) { return p.id === +id; })[0]; }
  function decide(p, status, note) {
    var at = nowStamp();
    WF.pay[p.id] = { status: status, note: note || '', at: at }; saveWF();
    p.status = status; p.note = note; p.decidedAt = at;
  }
  function openPayment(id) {
    var p = payById(id); if (!p) { return; }
    var flags = p.flags.map(function (f) { return [f, f === 'Screening match to review' ? 'err' : 'warn']; });
    var actionable = p.status === 'Awaiting your approval';
    var needNote = p.gbp >= D.noteThreshold, screen = p.flags.indexOf('Screening match to review') >= 0;
    var parts = [
      chips([[p.status]].concat(flags)),
      summary([['Beneficiary', p.beneficiary], ['From', ent(p.entity)], ['Method', p.method], ['Amount', inCcy(p.amount, p.ccy)],
        ['GBP equivalent', money(p.gbp) + ' <span class="t-cm-legal">' + esc(fxLine(p.ccy)) + '</span>', 1], ['Value date', dLong(p.valueDate)],
        ['Purpose', p.purpose], ['Initiated by', p.initiator], ['Reference', p.ref]].concat(p.note ? [['Audit note', p.note]] : []).concat(p.decidedAt ? [['Decided', dLong(p.decidedAt) + ' ' + p.decidedAt.slice(11, 16)]] : []))
    ];
    if (actionable) {
      parts.push(textarea('pay-note', needNote ? 'Audit note (required above £10m and for a rejection)' : 'Audit note (required for a rejection)', 'At least 12 characters. Stored with the decision.', 400, 12));
      if (screen) { parts.push(checkbox('pay-screen', 'I have reviewed the screening assessment and agree it is a false positive')); }
      parts.push('<div id="pay-msg"></div>');
    } else {
      parts.push(alertBox('info', 'No action needed from you.', p.status === 'Awaiting second approver' ? 'This payment is below your approval threshold and is waiting for a second approver in treasury.' : 'This payment has already been decided.'));
    }
    var step = 0;
    drawer({ title: 'Payment ' + p.ref, body: stack(parts), focus: actionable ? '#pay-note' : null,
      act: actionable ? { label: 'Approve', fn: function () { approveStep(); } } : null,
      cancel: actionable ? { label: 'Reject', fn: function () { rejectStep(); } } : { label: 'Close' },
      after: function () { wireCounter('pay-note'); } });
    function noteOk(req) {
      var t = $('#pay-note'), v = t ? t.value.trim() : '';
      if (req && v.length < 12) { fieldError('pay-note', 'Enter an audit note of at least 12 characters.'); t.focus(); return null; }
      fieldError('pay-note', ''); return v;
    }
    function approveStep() {
      var note = noteOk(needNote); if (note === null) { return; }
      if (screen && !$('#pay-screen').checked) { $('#pay-msg').innerHTML = alertBox('err', 'Confirm the screening review.', 'Tick the box to confirm you have reviewed the screening assessment.'); $('#pay-screen').focus(); return; }
      if (step === 0) {
        step = 1; $('#pay-msg').innerHTML = alertBox('warn', 'Check before you confirm.', 'You are approving ' + money(p.gbp) + ' (' + inCcy(p.amount, p.ccy) + ') to ' + p.beneficiary + ' for value ' + dLong(p.valueDate) + '.');
        DR.act.textContent = 'Confirm approval'; DR.cancel.textContent = 'Back'; DR.onCancel = function () { step = 0; DR.act.textContent = 'Approve'; DR.cancel.textContent = 'Reject'; DR.onCancel = rejectStep; $('#pay-msg').innerHTML = ''; };
        DR.act.focus(); return;
      }
      decide(p, 'Approved', note); drawerClose(); toast('ok', 'Approved ' + p.ref + ' — ' + money(p.gbp) + ' to ' + p.beneficiary + '.'); refresh();
    }
    function rejectStep() {
      var note = noteOk(true); if (note === null) { return; }
      decide(p, 'Rejected', note); drawerClose(); toast('warn', 'Rejected ' + p.ref + '. The initiator has been told, with your note.'); refresh();
    }
  }
  function bulkApprove() {
    var sel = gridSelected().map(payById).filter(Boolean);
    if (!sel.length) { toast('info', 'Select one or more payments in the grid first.'); return; }
    var ok = sel.filter(function (p) { return p.status === 'Awaiting your approval' && p.gbp < D.noteThreshold && p.flags.indexOf('Screening match to review') < 0; });
    var skip = sel.filter(function (p) { return ok.indexOf(p) < 0; });
    var body = '<p>' + (ok.length ? 'Approve ' + ok.length + ' payment' + (ok.length > 1 ? 's' : '') + ' totalling ' + money(sum(ok, function (p) { return p.gbp; })) + '?' : 'None of the selected payments can be approved in bulk.') + '</p>' +
      (skip.length ? '<p>' + skip.length + ' need individual review (above £10m, a screening match, or not awaiting you): ' + esc(skip.map(function (p) { return p.ref; }).join(', ')) + '.</p>' : '');
    if (!ok.length) { toast('warn', 'None of the selected payments can be approved in bulk: ' + skip.map(function (p) { return p.ref; }).join(', ') + '.'); return; }
    modal('Approve selected payments', body, 'Approve ' + ok.length, function () {
      ok.forEach(function (p) { decide(p, 'Approved', 'Bulk approval'); }); GRID.state.sel.clear();
      toast('ok', 'Approved ' + ok.length + ' payment' + (ok.length > 1 ? 's' : '') + '.'); refresh();
    });
  }

  // ---- risk exceptions
  function excById(id) { return D.exceptions.filter(function (x) { return x.id === id; })[0]; }
  function openException(id) {
    var x = excById(id); if (!x) { return; }
    var lim = x.limit ? D.limits.filter(function (l) { return l.id === x.limit; })[0] : null;
    var parts = [chips([[x.severity], [x.status]]), '<p class="t-ed-body">' + esc(x.detail) + '</p>',
      summary([['Entity', ent(x.entity)], ['Region', REG[x.region].name], ['Owner', x.owner], ['Raised', dLong(x.raised) + ', ' + x.raised.slice(11, 16)]].concat(lim ? [['Limit', lim.name + ' — ' + mShort(lim.used) + ' of ' + mShort(lim.limit) + ' (' + Math.round(lim.used / lim.limit * 100) + '%)']] : [])),
      timeline('Audit trail', x.audit.map(function (a) { return { at: a.at, title: a.what, who: a.who, desc: a.note, tone: a.what === 'Exception raised' ? 'warn' : 'ok' }; }))];
    var open = x.status === 'Open';
    if (open) { parts.push(textarea('exc-note', 'Audit note', 'At least 20 characters: what you have decided and who acts next.', 500, 20), checkbox('exc-confirm', 'I have reviewed this exception and accept the remediation owner'), '<div id="exc-msg"></div>'); }
    drawer({ title: x.title, body: stack(parts), focus: open ? '#exc-note' : null,
      act: open ? { label: 'Acknowledge', fn: ack } : null, cancel: { label: 'Close' }, after: function () { wireCounter('exc-note'); } });
    function ack() {
      var t = $('#exc-note'), v = t.value.trim();
      var good = fieldError('exc-note', v.length < 20 ? 'Enter an audit note of at least 20 characters.' : '');
      if (!good) { t.focus(); return; }
      if (!$('#exc-confirm').checked) { $('#exc-msg').innerHTML = alertBox('err', 'Confirm your review.', 'Tick the box to confirm you have reviewed the exception.'); $('#exc-confirm').focus(); return; }
      var entry = { at: nowStamp(), who: 'You (CEO)', what: 'Acknowledged', note: v };
      WF.exc[x.id] = { audit: (WF.exc[x.id] ? WF.exc[x.id].audit : []).concat([entry]) }; saveWF();
      x.status = 'Acknowledged'; x.audit.push(entry);
      drawerClose(); toast('ok', 'Acknowledged: ' + x.title + '. Your note is in the audit trail.'); refresh();
    }
  }

  // ---- generic record drawers
  function openTxn(id) {
    var t = D.transactions.filter(function (x) { return x.id === id; })[0]; if (!t) { return; }
    drawer({ title: t.type + ' ' + t.ref, body: stack([chips([[t.status]]), summary([['Date', dLong(t.date)], ['Entity', ent(t.entity)], ['Counterparty', t.counterparty], ['Type', t.type], ['Amount', inCcy(t.amount, t.ccy)], ['GBP equivalent', money(t.gbp) + ' <span class="t-cm-legal">' + esc(fxLine(t.ccy)) + '</span>', 1], ['Reference', t.ref]])]),
      act: { label: 'Export this record', fn: function () { download('transaction-' + t.ref + '.csv', csv([t], [['Date', 'date'], ['Entity', function (r) { return ent(r.entity); }], ['Counterparty', 'counterparty'], ['Type', 'type'], ['Reference', 'ref'], ['Currency', 'ccy'], ['Amount', 'amount'], ['GBP equivalent', 'gbp'], ['Status', 'status']])); } }, cancel: { label: 'Close' } });
  }
  function openForecast(id) {
    var t = D.forecast.filter(function (x) { return x.id === id; })[0]; if (!t) { return; }
    drawer({ title: t.category + ' ' + t.ref, body: stack([chips([[t.certainty, t.certainty === 'Committed' ? 'ok' : 'inf']]), summary([['Expected', dLong(t.date)], ['Entity', ent(t.entity)], ['Counterparty', t.counterparty], ['Category', t.category], ['Amount', inCcy(t.amount, t.ccy)], ['GBP equivalent', money(t.gbp)]])]), cancel: { label: 'Close' } });
  }
  function openDeal(id) {
    var t = D.deals.filter(function (x) { return x.id === id; })[0]; if (!t) { return; }
    drawer({ title: t.kind + ' ' + t.pair + ' ' + t.ref, body: stack([summary([['Trade date', dLong(t.trade)], ['Value date', dLong(t.value)], ['Entity', ent(t.entity)], ['Side', t.side + ' ' + t.ccy], ['Notional', inCcy(t.notional, t.ccy)], ['Deal rate', t.pair + ' ' + t.rate], ['GBP equivalent', money(t.gbp)], ['Counterparty', t.counterparty]]),
      alertBox('info', 'Illustrative.', 'Deal data is placeholder; no dealing connection exists in this prototype.')]), cancel: { label: 'Close' } });
  }
  function openPosition(id) {
    var t = D.positions.filter(function (x) { return x.id === id; })[0]; if (!t) { return; }
    var lim = D.limits.filter(function (l) { return l.name === t.counterparty; })[0];
    drawer({ title: t.kind + ' ' + t.ref, body: stack([summary([['Counterparty', t.counterparty], ['Entity', ent(t.entity)], ['Region', REG[t.region].name], ['Instrument', t.kind], ['Amount', inCcy(t.amount, t.ccy)], ['GBP equivalent', money(t.gbp)], ['Maturity', dLong(t.maturity)]].concat(lim ? [['Counterparty limit', mShort(lim.used) + ' used of ' + mShort(lim.limit) + ' (' + Math.round(lim.used / lim.limit * 100) + '%)']] : []))]), cancel: { label: 'Close' } });
  }
  function openInstrument(id) {
    var t = D.instruments.filter(function (x) { return x.id === id; })[0]; if (!t) { return; }
    var live = t.status !== 'Expired';
    drawer({ title: t.kind + ' ' + t.ref, body: stack([chips([[t.status]]), summary([['Counterparty', t.counterparty], ['Entity', ent(t.entity)], ['Amount', inCcy(t.amount, t.ccy)], ['GBP equivalent', money(t.gbp)], ['Issued', dLong(t.issued)], ['Expiry', dLong(t.expiry)]])].concat(live ? [textarea('tr-note', 'Amendment request', 'What should change, for example a new expiry date. At least 20 characters.', 400, 20)] : [])),
      act: live ? { label: 'Request amendment', fn: function () {
        var v = $('#tr-note').value.trim(); if (!fieldError('tr-note', v.length < 20 ? 'Describe the amendment in at least 20 characters.' : '')) { $('#tr-note').focus(); return; }
        var sr = newSR('Trade documents', t.entity, 'Amend ' + t.ref, v, 'Normal'); drawerClose(); toast('ok', 'Amendment request ' + sr.id + ' raised with HSBC Trade Services.');
      } } : null, cancel: { label: 'Close' }, after: function () { wireCounter('tr-note'); } });
  }
  function newSR(cat, entity, subj, desc, pri) {
    var n = D.requests.length + WF.sr.length + 1;
    var sr = { id: 'SR-' + (41000 + n * 7), category: cat, entity: entity, subject: subj, opened: ASOF, status: 'Submitted', priority: pri, resolvedHours: null, desc: desc, thread: [{ at: nowStamp(), who: 'You', what: 'Request submitted', note: desc }] };
    WF.sr.unshift(sr); saveWF(); D.requests.unshift(sr); return sr;
  }
  function openReport(id) {
    var r = D.reports.filter(function (x) { return x.id === id; })[0]; if (!r) { return; }
    var rows = reportRows(r);
    drawer({ title: r.name, body: stack([summary([['Family', r.family], ['Frequency', r.frequency], ['Last generated', dLong(r.last)], ['Rows in current scope', String(rows.rows.length)], ['Scope', (F.entity === 'all' ? 'All entities' : ent(F.entity)) + ' · ' + (F.region === 'all' ? 'all regions' : REG[F.region].name) + ' · last ' + F.range + ' days']]),
      alertBox('info', 'Generated in your browser.', 'The CSV is built from the prototype data with your current filters. Nothing is sent anywhere.')]),
      act: { label: 'Download CSV', fn: function () { download(stampName(r.id.toLowerCase() + '-' + r.name.toLowerCase().replace(/[^a-z0-9]+/g, '-')), csv(rows.rows, rows.cols)); } }, cancel: { label: 'Close' } });
  }
  function reportRows(r) {
    var S = r.source;
    if (S === 'accounts') { return { rows: D.accounts.filter(function (a) { return entOk(a.entity); }), cols: [['Account', 'number'], ['Entity', function (a) { return ent(a.entity); }], ['Currency', 'ccy'], ['Type', 'type'], ['Balance', 'bal'], ['GBP equivalent', function (a) { return a.balGbp[29]; }], ['Restricted', function (a) { return a.restricted ? 'Yes' : 'No'; }]] }; }
    if (S === 'forecast') { return { rows: D.forecast.filter(function (x) { return entOk(x.entity); }), cols: [['Date', 'date'], ['Entity', function (x) { return ent(x.entity); }], ['Category', 'category'], ['Counterparty', 'counterparty'], ['Certainty', 'certainty'], ['Currency', 'ccy'], ['Amount', 'amount'], ['GBP', 'gbp']] }; }
    if (S === 'facilities') { return { rows: D.facilities.filter(function (x) { return entOk(x.entity); }), cols: [['Facility', 'name'], ['Entity', function (x) { return ent(x.entity); }], ['Currency', 'ccy'], ['Limit', 'limit'], ['Drawn', 'drawn'], ['Limit GBP', 'limitGbp'], ['Drawn GBP', 'drawnGbp'], ['Maturity', 'maturity']] }; }
    if (S === 'transactions') { return { rows: D.transactions.filter(function (x) { return entOk(x.entity) && inRange(x.date); }), cols: [['Date', 'date'], ['Entity', function (x) { return ent(x.entity); }], ['Counterparty', 'counterparty'], ['Type', 'type'], ['Reference', 'ref'], ['Currency', 'ccy'], ['Amount', 'amount'], ['GBP', 'gbp'], ['Status', 'status']] }; }
    if (S === 'payments') { return { rows: D.payments.filter(function (x) { return entOk(x.entity); }), cols: [['Reference', 'ref'], ['Entity', function (x) { return ent(x.entity); }], ['Beneficiary', 'beneficiary'], ['Method', 'method'], ['Currency', 'ccy'], ['Amount', 'amount'], ['GBP', 'gbp'], ['Value date', 'valueDate'], ['Status', 'status'], ['Audit note', 'note'], ['Decided', 'decidedAt']] }; }
    if (S === 'deals') { return { rows: D.deals.filter(function (x) { return entOk(x.entity) && inRange(x.trade); }), cols: [['Reference', 'ref'], ['Trade date', 'trade'], ['Value date', 'value'], ['Type', 'kind'], ['Side', 'side'], ['Pair', 'pair'], ['Notional', 'notional'], ['Rate', 'rate'], ['GBP', 'gbp']] }; }
    if (S === 'limits') { return { rows: D.limits.filter(function (l) { return F.region === 'all' || l.region === F.region; }), cols: [['Limit', 'name'], ['Kind', 'kind'], ['Region', function (l) { return REG[l.region].name; }], ['Rating', 'rating'], ['Limit GBP', 'limit'], ['Used GBP', 'used'], ['Utilisation %', function (l) { return Math.round(l.used / l.limit * 100); }]] }; }
    if (S === 'exceptions') { var rows = []; D.exceptions.filter(function (x) { return entOk(x.entity); }).forEach(function (x) { x.audit.forEach(function (a) { rows.push({ id: x.id, title: x.title, severity: x.severity, status: x.status, at: a.at, who: a.who, what: a.what, note: a.note || '' }); }); });
      return { rows: rows, cols: [['Exception', 'id'], ['Title', 'title'], ['Severity', 'severity'], ['Status', 'status'], ['When', 'at'], ['Who', 'who'], ['Event', 'what'], ['Note', 'note']] }; }
    if (S === 'positions') { return { rows: D.positions.filter(function (x) { return entOk(x.entity); }), cols: [['Reference', 'ref'], ['Entity', function (x) { return ent(x.entity); }], ['Counterparty', 'counterparty'], ['Instrument', 'kind'], ['Currency', 'ccy'], ['Amount', 'amount'], ['GBP', 'gbp'], ['Maturity', 'maturity']] }; }
    if (S === 'instruments') { return { rows: D.instruments.filter(function (x) { return entOk(x.entity); }).sort(function (a, b) { return a.expiry < b.expiry ? -1 : 1; }), cols: [['Reference', 'ref'], ['Type', 'kind'], ['Entity', function (x) { return ent(x.entity); }], ['Counterparty', 'counterparty'], ['Currency', 'ccy'], ['Amount', 'amount'], ['GBP', 'gbp'], ['Expiry', 'expiry'], ['Status', 'status']] }; }
    return { rows: D.requests.filter(function (x) { return entOk(x.entity); }), cols: [['Request', 'id'], ['Category', 'category'], ['Entity', function (x) { return ent(x.entity); }], ['Subject', 'subject'], ['Opened', 'opened'], ['Status', 'status'], ['Priority', 'priority']] };
  }
  function openMessage(id) {
    var mm = D.messages.filter(function (x) { return x.id === id; })[0]; if (!mm) { return; }
    mm.unread = false; WF.msg[mm.id] = { read: true, thread: mm.thread }; saveWF();
    drawer({ title: mm.subject, body: stack([chips([[mm.category, 'inf']]), summary([['From', mm.from], ['Received', dLong(mm.date)]]), '<p class="t-ed-body">' + esc(mm.body) + '</p>',
      mm.thread.length ? timeline('Your replies', mm.thread.map(function (t) { return { at: t.at, title: 'Reply sent', who: 'You', desc: t.note, tone: 'ok' }; })) : '',
      textarea('msg-reply', 'Reply', 'Replies go to ' + mm.from + '. At least 5 characters.', 1000, 5)]), focus: '#msg-reply',
      act: { label: 'Send reply', fn: function () {
        var v = $('#msg-reply').value.trim(); if (!fieldError('msg-reply', v.length < 5 ? 'Write a reply of at least 5 characters.' : '')) { $('#msg-reply').focus(); return; }
        mm.thread.push({ at: nowStamp(), note: v }); WF.msg[mm.id] = { read: true, thread: mm.thread }; saveWF(); drawerClose(); toast('ok', 'Reply sent to ' + mm.from + '.'); refresh();
      } }, cancel: { label: 'Close' }, after: function () { wireCounter('msg-reply'); } });
    refresh();
  }
  function openSR(id) {
    var r = D.requests.filter(function (x) { return x.id === id; })[0]; if (!r) { return; }
    var needs = r.status === 'Awaiting your input';
    drawer({ title: r.id + ' — ' + r.subject, body: stack([chips([[r.status], [r.priority === 'High' ? 'High priority' : 'Normal priority', r.priority === 'High' ? 'warn' : 'inf']]),
      summary([['Category', r.category], ['Entity', ent(r.entity)], ['Opened', dLong(r.opened)]].concat(r.resolvedHours ? [['Resolved in', r1(r.resolvedHours) + ' hours']] : [])),
      r.desc ? '<p class="t-ed-body">' + esc(r.desc) + '</p>' : '',
      (r.thread || []).length ? timeline('Updates', r.thread.map(function (t) { return { at: t.at, title: t.what, who: t.who, desc: t.note, tone: 'inf' }; })) : '',
      needs ? textarea('sr-reply', 'Information for HSBC', 'HSBC is waiting for this to continue. At least 10 characters.', 800, 10) : alertBox('info', r.status === 'Resolved' ? 'Resolved.' : 'With HSBC.', r.status === 'Resolved' ? 'No further action is needed.' : 'HSBC is working on this request. You will get a message when it changes.')]),
      focus: needs ? '#sr-reply' : null,
      act: needs ? { label: 'Send information', fn: function () {
        var v = $('#sr-reply').value.trim(); if (!fieldError('sr-reply', v.length < 10 ? 'Enter at least 10 characters.' : '')) { $('#sr-reply').focus(); return; }
        r.status = 'In progress'; r.thread = (r.thread || []).concat([{ at: nowStamp(), who: 'You', what: 'Information sent', note: v }]);
        WF.srUpd[r.id] = { status: r.status, thread: r.thread }; saveWF(); drawerClose(); toast('ok', 'Sent to HSBC. ' + r.id + ' is back in progress.'); refresh();
      } } : null, cancel: { label: 'Close' }, after: function () { wireCounter('sr-reply'); } });
  }

  /* ================================================================== per-page renderers */
  var R = {};
  R.overview = function () {
    var S = series();
    setKpi('cash', S.cash); setKpi('liquidity', S.liquidity); setKpi('headroom', S.headroom);
    var ladder = outflowLadder(), trail = trailingOutflows();
    setKpi('outflows', ladder, { value: S.out, base: trail, spark: ladder, per: 'vs last 30 days actual' });
    var ds = days();
    chart('ov-liq', { type: 'multiline', categories: ds.map(dLabel), categoryLabel: 'Day', unit: '£m',
      caption: 'Cash, available liquidity and funding headroom by day, GBP millions',
      series: [{ name: 'Cash', values: S.cash.slice(i0()).map(m) }, { name: 'Available liquidity', values: S.liquidity.slice(i0()).map(m) }, { name: 'Funding headroom', values: S.headroom.slice(i0()).map(m) }] });
    var facs = D.facilities.filter(function (f) { return entOk(f.entity); }).sort(function (a, b) { return b.limitGbp - a.limitGbp; }).slice(0, 4);
    chart('ov-fac', { type: 'bullet', categories: facs.map(function (f) { return f.name.replace(' facility', '').replace(' line', ''); }), categoryLabel: 'Facility', format: 'percent',
      caption: 'Committed facility utilisation against the 75% policy ceiling, per cent', ranges: [60, 85, 100],
      series: [{ name: 'Drawn', values: facs.map(function (f) { return Math.round(f.drawnGbp / f.limitGbp * 100); }) }, { name: 'Policy ceiling', values: facs.map(function () { return 75; }) }] });
    // exposure: region x currency
    var regs = D.regions.filter(function (r) { return F.region === 'all' || r.id === F.region; });
    var buckets = ['USD', 'EUR', 'GBP', 'Asian currencies', 'Other'];
    var pos = D.positions.filter(function (p) { return entOk(p.entity); });
    chart('ov-exp', { type: 'stacked-column', categories: regs.map(function (r) { return r.name; }), categoryLabel: 'Region', unit: '£m',
      caption: 'Exposure by region, split by currency, GBP millions',
      series: buckets.map(function (b) { return { name: b, values: regs.map(function (r) { return m(sum(pos.filter(function (p) { return p.region === r.id && bucketCcy(p.ccy) === b; }), function (p) { return p.gbp; })); }) }; }) });
    $('#ov-drill').innerHTML = regs.map(function (r) {
      var t = sum(pos.filter(function (p) { return p.region === r.id; }), function (p) { return p.gbp; });
      return '<a class="tag link" data-region-link href="risk.html' + qs({ region: r.id }).replace(/entity=[^&]*&?/, '') + '#records"><span class="lbl">' + esc(r.name) + ' · ' + mShort(t) + '</span></a>';
    }).join('');
    var cc = ['USD', 'EUR', 'GBP', 'HKD'];
    chart('ov-ccy', { type: 'donut', categories: ['USD', 'EUR', 'GBP', 'HKD', 'Other'], categoryLabel: 'Currency', unit: '£m', caption: 'Share of total exposure by currency, GBP millions',
      series: [{ name: 'Exposure', values: cc.map(function (c) { return m(sum(pos.filter(function (p) { return p.ccy === c; }), function (p) { return p.gbp; })); }).concat([m(sum(pos.filter(function (p) { return cc.indexOf(p.ccy) < 0; }), function (p) { return p.gbp; }))]) }] });
    // decisions
    var aw = D.payments.filter(function (p) { return entOk(p.entity) && p.status === 'Awaiting your approval'; }).sort(function (a, b) { return b.gbp - a.gbp; });
    $('#ov-approvals').innerHTML = decisionCard(aw.length + ' payment' + (aw.length === 1 ? '' : 's') + ' awaiting you', 'Oldest value date ' + (aw.length ? dLong(aw.map(function (p) { return p.valueDate; }).sort()[0]) : '—'), money(sum(aw, function (p) { return p.gbp; })),
      aw.slice(0, 3).map(function (p) { return { href: 'payments.html' + qs({ open: p.id }), who: shortEnt(p.entity), ini: ENT[p.entity].ccy.slice(0, 2), label: p.beneficiary, desc: p.ref + ' · ' + shortEnt(p.entity) + ' · value ' + dLabel(p.valueDate), right: mShort(p.gbp), status: p.flags.length ? p.flags[0] : 'Awaiting you', tone: p.flags.indexOf('Screening match to review') >= 0 ? 'err' : 'warn' }; }), 'No payments are waiting for you.');
    var sev = { High: 0, Medium: 1, Low: 2 };
    var ex = D.exceptions.filter(function (x) { return entOk(x.entity) && x.status === 'Open'; }).sort(function (a, b) { return sev[a.severity] - sev[b.severity]; });
    $('#ov-exceptions').innerHTML = decisionCard(ex.length + ' open exception' + (ex.length === 1 ? '' : 's'), ex.filter(function (x) { return x.severity === 'High'; }).length + ' high severity', String(ex.length),
      ex.slice(0, 3).map(function (x) { return { href: 'risk.html' + qs({ open: x.id }), who: x.severity + ' severity', ini: x.severity.charAt(0), label: x.title, desc: shortEnt(x.entity) + ' · raised ' + dLabel(x.raised), right: x.owner, status: x.severity, tone: TONE[x.severity] }; }), 'No open risk exceptions in this scope.');
  };
  function decisionCard(k, sub, v, items, empty) {
    return '<div class="cn-summary"><dl class="summary tpl-na-head"><div class="summary__row"><dt class="summary__k t-cm-label">' + esc(k) + ' <span class="t-cm-legal">' + esc(sub) + '</span></dt><dd class="summary__v t-cm-figure-5">' + esc(v) + '</dd></div></dl></div>' +
      (items.length ? '<div class="cn-list-items"><ul class="list">' + items.map(function (it) {
        return '<li><a class="row" href="' + it.href + '"><span class="avatar" role="img" aria-label="' + esc(it.who) + '">' + esc(it.ini) + '</span><span class="body"><span class="line"><span class="title">' + esc(it.label) + '</span>' + statusDot(it.status, it.tone) + '</span><span class="line"><span class="desc">' + esc(it.desc) + '</span><span class="amount">' + esc(it.right || '') + '</span></span></span></a></li>';
      }).join('') + '</ul></div>' : '<div class="cn-empty-state"><section class="empty" aria-label="Nothing to do"><h3 class="t-ed-heading-4 em">You\u2019re all caught up</h3><p class="t-ed-body-small">' + esc(empty) + '</p></section></div>');
  }
  R.accounts = function () {
    var ds = days(), accs = D.accounts.filter(function (a) { return entOk(a.entity); });
    chart('ac-bal', { type: 'stacked-area', categories: ds.map(dLabel), categoryLabel: 'Day', unit: '£m', caption: 'Cash balances by day, stacked by region, GBP millions',
      series: D.regions.map(function (r) { return { name: r.name, values: ds.map(function (d, j) { var i = i0() + j; return m(sum(accs.filter(function (a) { return ENT[a.entity].region === r.id; }), function (a) { return a.balGbp[i]; })); }) }; }) });
    var es = D.entities.filter(function (e) { return entOk(e.id); });
    chart('ac-ent', { type: 'bar', categories: es.map(function (e) { return shortEnt(e.id); }), categoryLabel: 'Entity', unit: '£m', caption: 'Closing cash balance by entity, GBP millions',
      series: [{ name: 'Balance', values: es.map(function (e) { return m(sum(accs.filter(function (a) { return a.entity === e.id; }), function (a) { return a.balGbp[29]; })); }) }] });
    var tx = D.transactions.filter(function (t) { return entOk(t.entity) && inRange(t.date); });
    gridRows(tx.map(function (t) { return { id: t.id, date: t.date, payee: t.counterparty, ref: t.ref, type: t.type + ' · ' + shortEnt(t.entity), amount: t.gbp }; }), tx);
  };
  R.liquidity = function () {
    var S = series(), ds = days();
    setKpi('liquidity', S.liquidity); setKpi('headroom', S.headroom); setKpi('undrawn', S.undrawn); setKpi('trapped', S.restricted);
    var net = ds.map(function (d) { return sum(D.transactions.filter(function (t) { return t.date === d && entOk(t.entity); }), function (t) { return t.gbp; }); });
    chart('liq-flow', { type: 'combo', categories: ds.map(dLabel), categoryLabel: 'Day', caption: 'Daily net cash flow (columns, GBP millions) and available liquidity (line, GBP millions)',
      series: [{ name: 'Net cash flow (£m)', kind: 'column', unit: '£m', values: net.map(m) }, { name: 'Available liquidity (£m)', kind: 'line', unit: '£m', values: S.liquidity.slice(i0()).map(m) }] });
    var facs = D.facilities.filter(function (f) { return entOk(f.entity); });
    chart('liq-fac', { type: 'bullet', categories: facs.map(function (f) { return f.name.replace(' facility', '').replace(' line', ''); }), categoryLabel: 'Facility', format: 'percent', ranges: [60, 85, 100],
      caption: 'Committed facility utilisation against the 75% policy ceiling, per cent',
      series: [{ name: 'Drawn', values: facs.map(function (f) { return Math.round(f.drawnGbp / f.limitGbp * 100); }) }, { name: 'Policy ceiling', values: facs.map(function () { return 75; }) }] });
    $('#liq-fac-list').outerHTML = '<dl class="summary" id="liq-fac-list">' + facs.map(function (f) {
      return '<div class="summary__row"><dt class="summary__k t-cm-label">' + esc(f.name) + ' <span class="t-cm-legal">' + esc(shortEnt(f.entity) + ' · matures ' + dLong(f.maturity)) + '</span></dt><dd class="summary__v t-cm-figure-6">' + esc(mShort(f.limitGbp - f.drawnGbp)) + ' undrawn</dd></div>';
    }).join('') + '<div class="summary__row summary__row--total"><dt class="summary__k">Policy liquidity buffer</dt><dd class="summary__v">' + esc(mShort(S.buffer)) + '</dd></div></dl>';
    var horizon = new Date(ASOF + 'T00:00:00Z'); horizon.setUTCDate(horizon.getUTCDate() + (+F.range)); var hz = horizon.toISOString().slice(0, 10);
    var fc = D.forecast.filter(function (x) { return entOk(x.entity) && x.date <= hz; });
    gridRows(fc.map(function (x) { return { id: x.id, date: x.date, payee: x.counterparty, ref: x.ref + ' · ' + x.certainty, type: x.category, amount: x.gbp }; }), fc);
  };
  R.payments = function () {
    var ds = days();
    chart('pay-daily', { type: 'column', categories: ds.map(dLabel), categoryLabel: 'Day', unit: '£m', caption: 'Value of payments released per day, GBP millions',
      series: [{ name: 'Outflows', values: ds.map(function (d) { return m(-sum(D.transactions.filter(function (t) { return t.date === d && t.gbp < 0 && entOk(t.entity); }), function (t) { return t.gbp; })); }) }] });
    var q = D.payments.filter(function (p) { return entOk(p.entity) && /^Awaiting/.test(p.status); });
    var meth = ['SWIFT', 'CHAPS', 'SEPA credit transfer', 'Fedwire'];
    chart('pay-method', { type: 'pie', categories: meth.concat(['Other']), categoryLabel: 'Method', unit: '£m', caption: 'Value awaiting approval by payment method, GBP millions',
      series: [{ name: 'Value', values: meth.map(function (mm) { return m(sum(q.filter(function (p) { return p.method === mm; }), function (p) { return p.gbp; })); }).concat([m(sum(q.filter(function (p) { return meth.indexOf(p.method) < 0; }), function (p) { return p.gbp; }))]) }] });
    var ps = D.payments.filter(function (p) { return entOk(p.entity); });
    gridRows(ps.map(function (p) { return { id: p.id, date: p.valueDate, payee: p.beneficiary, ref: p.ref, type: p.status, amount: -p.gbp }; }), ps);
  };
  R.fx = function () {
    var ds = days(), a = i0();
    chart('fx-ohlc', { type: 'candlestick', categories: ds.map(dLabel), categoryLabel: 'Day', caption: 'GBP/USD open, high, low and close by day, illustrative',
      series: [{ name: 'Open', values: D.ohlc.open.slice(a) }, { name: 'High', values: D.ohlc.high.slice(a) }, { name: 'Low', values: D.ohlc.low.slice(a) }, { name: 'Close', values: D.ohlc.close.slice(a) }] });
    var pairs = ['GBP/USD', 'EUR/GBP', 'GBP/HKD', 'GBP/SGD', 'GBP/CNY'];
    chart('fx-idx', { type: 'multiline', categories: ds.map(dLabel), categoryLabel: 'Day', caption: 'Sterling against five currencies, indexed to 100 at the start of the period',
      series: pairs.map(function (p) { var s = D.fxSeries[p].slice(a), b = s[0]; return { name: p, values: s.map(function (v) { return Math.round(v / b * 1000) / 10; }) }; }) });
    var ccys = ['USD', 'EUR', 'HKD', 'CNY', 'SGD', 'AED'];
    var fc = D.forecast.filter(function (x) { return entOk(x.entity); });
    chart('fx-nat', { type: 'butterfly-h', categories: ccys, categoryLabel: 'Currency', unit: '£m', caption: 'Forecast receivables and payables by currency, next 30 days, GBP millions',
      series: [{ name: 'Receivables', values: ccys.map(function (c) { return m(sum(fc.filter(function (x) { return x.ccy === c && x.gbp > 0; }), function (x) { return x.gbp; })); }) },
               { name: 'Payables', values: ccys.map(function (c) { return m(-sum(fc.filter(function (x) { return x.ccy === c && x.gbp < 0; }), function (x) { return x.gbp; })); }) }] });
    $('#fx-rates').innerHTML = ['USD', 'EUR', 'HKD', 'SGD', 'CNY', 'AED'].map(function (c) {
      var h = D.hedgeRatio[c]; var floor = 70;
      return '<div class="summary__row"><dt class="summary__k t-cm-label">GBP/' + c + ' ' + (1 / D.fx[c]).toFixed(4) + ' <span class="t-cm-legal">1 ' + c + ' = £' + D.fx[c].toFixed(4) + '</span></dt><dd class="summary__v">' + statusDot(h + '% hedged', h < floor ? 'warn' : 'ok') + '</dd></div>';
    }).join('') + '<div class="summary__row"><dt class="summary__k t-cm-legal">' + esc(D.fxNote) + ' Hedge policy floor 70%.</dt><dd class="summary__v"></dd></div>';
    var dl = D.deals.filter(function (x) { return entOk(x.entity) && inRange(x.trade); });
    gridRows(dl.map(function (x) { return { id: x.id, date: x.trade, payee: x.kind + ' · ' + x.side + ' ' + x.pair, ref: x.ref, type: 'Value ' + dLabel(x.value), amount: x.gbp }; }), dl);
  };
  R.risk = function () {
    var regs = D.regions.filter(function (r) { return F.region === 'all' || r.id === F.region; });
    var pos = D.positions.filter(function (p) { return entOk(p.entity); });
    chart('rk-reg', { type: 'grouped-column', categories: regs.map(function (r) { return r.name; }), categoryLabel: 'Region', unit: '£m', caption: 'Exposure and approved limit by region, GBP millions',
      series: [{ name: 'Exposure', values: regs.map(function (r) { return m(sum(pos.filter(function (p) { return p.region === r.id; }), function (p) { return p.gbp; })); }) },
               { name: 'Limit', values: regs.map(function (r) { var l = D.limits.filter(function (x) { return x.id === 'L-CTRY-' + r.id; })[0]; return m(l.limit); }) }] });
    var banks = D.limits.filter(function (l) { return l.kind === 'Counterparty' && (F.region === 'all' || l.region === F.region); }).sort(function (a, b) { return a.used - b.used; });
    chart('rk-cp', { type: 'scatter', categories: banks.map(function (l) { return String(m(l.used)); }), categoryLabel: 'Exposure (£m)', caption: 'Bank counterparty exposure (GBP millions, across) against limit utilisation (per cent, up)',
      series: [{ name: 'Limit used (%)', values: banks.map(function (l) { return Math.round(l.used / l.limit * 100); }) }] });
    var lims = D.limits.filter(function (l) { return F.region === 'all' || l.region === F.region; }).sort(function (a, b) { return b.used / b.limit - a.used / a.limit; }).slice(0, 6);
    $('#rk-limits').innerHTML = '<div class="cn-limits-meter"><div class="lim-stack" role="group" aria-labelledby="rk-lim-h"><p class="lim-label t-cm-label" id="rk-lim-h">Highest utilisation</p><p class="lim-caption t-cm-caption">Counterparty and region limits, as at ' + esc(dLong(ASOF)) + '. A full bar means the limit is blocked.</p>' +
      lims.map(function (l, i) { var u = l.used / l.limit * 100;
        return '<div class="lim-row"><div class="lim-row-head"><span class="lim-row-name t-cm-legal" id="rk-lim-' + i + '">' + esc(l.name) + (u >= 100 ? ' — breached' : u >= 90 ? ' — approaching' : '') + '</span><span class="lim-row-fig t-cm-figure-6">' + esc(mShort(l.used) + ' of ' + mShort(l.limit) + ' · ' + Math.round(u) + '%') + '</span></div>' +
          '<div class="pb-track" role="progressbar" aria-labelledby="rk-lim-' + i + '" aria-valuenow="' + Math.round(l.used) + '" aria-valuemin="0" aria-valuemax="' + Math.round(l.limit) + '" aria-valuetext="' + esc(Math.round(u) + ' per cent of the ' + l.name + ' limit used') + '"><div class="pb-fill" style="width:' + Math.min(100, u).toFixed(2) + '%"></div></div></div>';
      }).join('') + '</div></div>';
    gridRows(pos.map(function (p) { return { id: p.id, date: p.maturity, payee: p.counterparty, ref: p.ref, type: p.kind + ' · ' + p.ccy, amount: p.gbp }; }), pos);
  };
  R.trade = function () {
    var live = D.instruments.filter(function (x) { return entOk(x.entity) && x.status !== 'Expired'; });
    var bins = [[0, 30], [31, 60], [61, 90], [91, 120], [121, 150], [151, 180], [181, 210], [211, 240], [241, 270], [271, 300]];
    var dte = function (x) { return Math.round((new Date(x.expiry) - new Date(ASOF)) / 864e5); };
    chart('tr-exp', { type: 'histogram', categories: bins.map(function (b) { return b[0] + '–' + b[1]; }), categoryLabel: 'Days to expiry', caption: 'Live instruments by days to expiry',
      series: [{ name: 'Instruments', values: bins.map(function (b) { return live.filter(function (x) { var d = dte(x); return d >= b[0] && d <= b[1]; }).length; }) }] });
    var types = ['Import letter of credit', 'Export letter of credit', 'Standby letter of credit', 'Bank guarantee', 'Documentary collection'];
    chart('tr-type', { type: 'bar', categories: types, categoryLabel: 'Type', unit: '£m', caption: 'Value of live instruments by type, GBP millions',
      series: [{ name: 'Value', values: types.map(function (t) { return m(sum(live.filter(function (x) { return x.kind === t; }), function (x) { return x.gbp; })); }) }] });
    var all = D.instruments.filter(function (x) { return entOk(x.entity); });
    gridRows(all.map(function (x) { return { id: x.id, date: x.expiry, payee: x.counterparty, ref: x.ref, type: x.kind + ' · ' + x.status, amount: x.gbp }; }), all);
  };
  function five(a) {
    a = a.slice().sort(function (x, y) { return x - y; }); if (!a.length) { return null; }
    var q = function (p) { var i = (a.length - 1) * p, lo = Math.floor(i), hi = Math.ceil(i); return a[lo] + (a[hi] - a[lo]) * (i - lo); };
    var q1 = q(0.25), q3 = q(0.75), iqr = q3 - q1, lo = q1 - 1.5 * iqr, hi = q3 + 1.5 * iqr;
    var inr = a.filter(function (v) { return v >= lo && v <= hi; }), out = a.filter(function (v) { return v < lo || v > hi; });
    return [inr[0], q1, q(0.5), q3, inr[inr.length - 1], out.length ? out[out.length - 1] : q(0.5)].map(r1);
  }
  R.reports = function () {
    var regs = D.regions.filter(function (r) { return F.region === 'all' || r.id === F.region; });
    var st = regs.map(function (r) { return five(D.payments.filter(function (p) { return ENT[p.entity].region === r.id && (F.entity === 'all' || p.entity === F.entity); }).map(function (p) { return p.settleHours; })); });
    var ok = regs.filter(function (r, i) { return st[i]; }); st = st.filter(Boolean);
    var names = ['Minimum', 'Q1', 'Median', 'Q3', 'Maximum', 'Outlier'];
    chart('rp-settle', { type: 'boxplot', categories: ok.map(function (r) { return r.name; }), categoryLabel: 'Region', unit: 'hours', caption: 'Hours from release to settlement, by region, five-number summary',
      series: names.map(function (n, k) { return { name: n, values: st.map(function (s) { return s[k]; }) }; }) });
    var runs = D.reportRuns.slice(i0());
    chart('rp-runs', { type: 'spark', categories: days().map(dLabel), categoryLabel: 'Day', caption: 'Reports generated per day over the period', series: [{ name: 'Runs', values: runs }] });
    var busiest = runs.indexOf(Math.max.apply(null, runs));
    $('#rp-runs-note').innerHTML = [['Reports generated', String(sum(runs))], ['Average per day', r1(sum(runs) / runs.length).toString()], ['Busiest day', dLabel(days()[busiest]) + ' · ' + runs[busiest] + ' runs']].map(function (r) {
      return '<div class="summary__row"><dt class="summary__k">' + esc(r[0]) + '</dt><dd class="summary__v">' + esc(r[1]) + '</dd></div>'; }).join('');
  };
  R.messages = function () {
    var weeks = [], d = new Date(ASOF + 'T00:00:00Z'); d.setUTCDate(d.getUTCDate() - 34);
    for (var w = 0; w < 5; w++) { var s = d.toISOString().slice(0, 10); d.setUTCDate(d.getUTCDate() + 7); weeks.push([s, d.toISOString().slice(0, 10)]); }
    var reqs = D.requests.filter(function (r) { return entOk(r.entity); });
    var resolvedOn = function (r) { if (!r.resolvedHours) { return null; } var x = new Date(r.opened + 'T09:00:00Z'); x.setTime(x.getTime() + r.resolvedHours * 36e5); return x.toISOString().slice(0, 10); };
    chart('ms-sr', { type: 'grouped-column', categories: weeks.map(function (w) { return 'w/c ' + dLabel(w[0]); }), categoryLabel: 'Week', caption: 'Service requests opened and resolved per week',
      series: [{ name: 'Opened', values: weeks.map(function (w) { return reqs.filter(function (r) { return r.opened >= w[0] && r.opened < w[1]; }).length; }) },
               { name: 'Resolved', values: weeks.map(function (w) { return reqs.filter(function (r) { var x = resolvedOn(r); return x && x >= w[0] && x < w[1]; }).length; }) }] });
    var cats = ['Relationship', 'Service update', 'Compliance request', 'Market insight'];
    chart('ms-cat', { type: 'pie', categories: cats, categoryLabel: 'Category', caption: 'Messages received by category, count',
      series: [{ name: 'Messages', values: cats.map(function (c) { return D.messages.filter(function (mm) { return mm.category === c; }).length; }) }] });
  };
  R.settings = function () {
    var wk = new Date(ASOF + 'T00:00:00Z'); wk.setUTCDate(wk.getUTCDate() - 6); var from = wk.toISOString().slice(0, 10);
    var used = sum(D.payments.filter(function (p) { return p.status === 'Approved' && p.decidedAt && p.decidedAt.slice(0, 10) >= from; }), function (p) { return p.gbp; })
      + sum(D.payments.filter(function (p) { return p.status === 'Approved' && !p.decidedAt; }), function (p) { return p.gbp; });
    chart('st-auth', { type: 'bullet', categories: ['This week'], categoryLabel: 'Authority', unit: '£m', ranges: [150, 225, 300],
      caption: 'Value you approved this week against your weekly authority, GBP millions',
      series: [{ name: 'Used', values: [m(used)] }, { name: 'Weekly limit', values: [250] }] });
  };

  /* ================================================================== page setup */
  var GRIDCFG = {
    accounts: { title: 'Transactions', noun: 'transactions', pageSize: 24, group: 'Transaction detail', cols: { date: 'Date', payee: 'Counterparty', ref: 'Reference', type: 'Type · entity', amount: 'Amount' }, open: openTxn },
    liquidity: { title: 'Forecast items', noun: 'forecast items', group: 'Forecast item', cols: { date: 'Expected', payee: 'Counterparty', ref: 'Reference', type: 'Category', amount: 'Amount' }, open: openForecast },
    payments: { title: 'Payments', noun: 'payments', group: 'Payment detail', cols: { date: 'Value date', payee: 'Beneficiary', ref: 'Reference', type: 'Status', amount: 'Amount' }, open: openPayment },
    fx: { title: 'FX deals', noun: 'deals', group: 'Deal detail', cols: { date: 'Trade date', payee: 'Deal', ref: 'Reference', type: 'Settlement', amount: 'Amount' }, open: openDeal },
    risk: { title: 'Positions', noun: 'positions', group: 'Position detail', cols: { date: 'Maturity', payee: 'Counterparty', ref: 'Reference', type: 'Instrument', amount: 'Amount' }, open: openPosition },
    trade: { title: 'Instruments', noun: 'instruments', group: 'Instrument detail', cols: { date: 'Expiry', payee: 'Counterparty', ref: 'Reference', type: 'Type · status', amount: 'Amount' }, open: openInstrument }
  };
  if (GRIDCFG[PAGE]) { gridSetup(GRIDCFG[PAGE]); }

  if (PAGE === 'risk') {
    list({ id: 'rk-exc', noun: 'exceptions', noun1: 'exception', size: 4, filterHost: 'rk-sev', rows: function () { var s = { High: 0, Medium: 1, Low: 2 }; return D.exceptions.filter(function (x) { return entOk(x.entity); }).sort(function (a, b) { return (a.status === 'Open' ? 0 : 1) - (b.status === 'Open' ? 0 : 1) || s[a.severity] - s[b.severity]; }); },
      match: function (x, v) { return x.severity === v; }, text: function (x) { return x.title + ' ' + x.detail + ' ' + x.owner; },
      row: function (x) { return { who: x.severity + ' severity', ini: x.severity.charAt(0), title: x.title, status: x.status, desc: shortEnt(x.entity) + ' · raised ' + dLabel(x.raised), right: x.severity }; }, open: openException });
  }
  if (PAGE === 'reports') {
    list({ id: 'rp-list', noun: 'reports', noun1: 'report', size: 6, filterHost: 'rp-fam', rows: function () { return D.reports; }, match: function (r, v) { return r.family === v; }, text: function (r) { return r.name + ' ' + r.family; },
      row: function (r) { return { who: r.family, ini: r.family.slice(0, 2), title: r.name, status: r.frequency, tone: 'inf', desc: r.family + ' · last generated ' + dLong(r.last), right: reportRows(r).rows.length + ' rows' }; }, open: openReport });
  }
  if (PAGE === 'messages') {
    list({ id: 'ms-list', noun: 'messages', noun1: 'message', size: 5, filterHost: 'ms-unread', rows: function () { return D.messages; }, match: function (mm) { return mm.unread; }, text: function (mm) { return mm.subject + ' ' + mm.from + ' ' + mm.body; },
      row: function (mm) { return { who: mm.from, ini: mm.from.split(' ').map(function (w) { return w.charAt(0); }).join('').slice(0, 2), title: mm.subject, status: mm.unread ? 'Unread' : (mm.thread.length ? 'Replied' : 'Read'), tone: mm.unread ? 'warn' : 'ok', desc: mm.from + ' · ' + dLabel(mm.date), right: mm.category }; }, open: openMessage });
    list({ id: 'sr-list', noun: 'requests', noun1: 'request', size: 5, filterHost: 'sr-status', rows: function () { return D.requests.filter(function (r) { return entOk(r.entity); }); }, match: function (r, v) { return r.status === v; }, text: function (r) { return r.id + ' ' + r.subject + ' ' + r.category; },
      row: function (r) { return { who: r.category, ini: r.category.split(' ').map(function (w) { return w.charAt(0); }).join('').slice(0, 2).toUpperCase(), title: r.subject, status: r.status, desc: r.id + ' · ' + r.category + ' · opened ' + dLabel(r.opened), right: shortEnt(r.entity) }; }, open: openSR });
    wireCounter('sr-desc');
  }

  function refresh() {
    if (R[PAGE]) { R[PAGE](); }
    refreshLists();
    var unread = D.messages.filter(function (mm) { return mm.unread; }).length;
    var mb = $('.sh-actions button[data-href="messages.html"]'); if (mb) { mb.setAttribute('aria-label', 'HSBC messages and service requests, ' + unread + ' unread'); }
  }

  /* ------------------------------------------------------------------ actions (delegated) */
  document.addEventListener('click', function (e) {
    var a = e.target.closest('[data-action]');
    var nav = e.target.closest('.sh-actions button[data-href]');
    if (nav) { location.href = nav.getAttribute('data-href') + qs(); return; }
    if (!a) { return; }
    var act = a.getAttribute('data-action');
    if (act === 'not-in-prototype') { e.preventDefault(); toast('info', 'Legal pages are not part of this prototype.'); return; }
    if (act === 'export-grid') {
      var cfg = GRIDCFG[PAGE]; var rows = GRID ? GRID.rows.slice() : [];
      download(stampName(PAGE + '-' + cfg.noun.replace(/ /g, '-')), csv(rows, [[cfg.cols.date, 'date'], [cfg.cols.payee, 'payee'], [cfg.cols.ref, 'ref'], [cfg.cols.type, 'type'], ['Amount (GBP)', 'amount']]));
      return;
    }
    if (act === 'open-selected') { var s = gridSelected(); if (!s.length) { toast('info', 'Select a row first — use the checkbox at the start of the row.'); return; } GRID_OPEN(s[0]); return; }
    if (act === 'bulk-approve') { bulkApprove(); return; }
    if (act === 'export-summary') {
      var S = series(), rows2 = D.days.slice(i0()).map(function (d, j) { var i = i0() + j; return { day: d, cash: Math.round(S.cash[i]), liquidity: Math.round(S.liquidity[i]), headroom: Math.round(S.headroom[i]) }; });
      download(stampName('ceo-overview'), csv(rows2, [['Day', 'day'], ['Cash GBP', 'cash'], ['Available liquidity GBP', 'liquidity'], ['Funding headroom GBP', 'headroom']])); return;
    }
    if (act === 'reset-data') {
      modal('Reset prototype data', '<p>This clears approvals, acknowledgements, service requests, replies and saved filters made in this browser. The page reloads.</p>', 'Reset data', function () {
        ['wf', 'filters', 'defaults', 'notify', 'grid.accounts', 'grid.liquidity', 'grid.payments', 'grid.fx', 'grid.risk', 'grid.trade', 'list.rk-exc', 'list.rp-list', 'list.ms-list', 'list.sr-list', 'nav'].forEach(store.del);
        location.href = location.pathname;
      }); return;
    }
    if (act === 'sr-submit') { e.preventDefault(); submitSR(); return; }
    if (act === 'sr-clear') { e.preventDefault(); clearSR(); return; }
  });
  function submitSR() {
    var cat = ddGet($('#sr-cat')), en = ddGet($('#sr-ent')), pri = segGet($('#sr-pri')) || 'Normal';
    var subj = $('#sr-subj').value.trim(), desc = $('#sr-desc').value.trim(), errs = [];
    var ddErr = function (id, bad, msg) { var dd = $('#' + id); dd.classList.toggle('is-error', bad); $('.trigger', dd).setAttribute('aria-invalid', String(bad)); if (bad) { errs.push(msg); } };
    ddErr('sr-cat', !cat, 'Choose a category.'); ddErr('sr-ent', !en, 'Choose an entity.');
    if (!fieldError('sr-subj', subj.length < 5 ? 'Enter a subject of at least 5 characters.' : '')) { errs.push('Enter a subject of at least 5 characters.'); }
    if (!fieldError('sr-desc', desc.length < 20 ? 'Describe what you need in at least 20 characters.' : '')) { errs.push('Describe what you need in at least 20 characters.'); }
    if (/\b\d{13,19}\b/.test(desc) || /password/i.test(desc)) { fieldError('sr-desc', 'Remove card numbers or passwords before you submit.'); errs.push('Remove card numbers or passwords.'); }
    $('#sr-errors').textContent = errs.length ? 'There ' + (errs.length === 1 ? 'is 1 problem' : 'are ' + errs.length + ' problems') + ': ' + errs.join(' ') : '';
    if (errs.length) { var first = $('#sr-form [aria-invalid="true"]'); if (first) { first.focus(); } return; }
    var sr = newSR(cat, en, subj, desc, pri); clearSR(); toast('ok', 'Request ' + sr.id + ' submitted to HSBC.'); refresh();
  }
  function clearSR() {
    ddSet($('#sr-cat'), ''); ddSet($('#sr-ent'), ''); segSet($('#sr-pri'), 'Normal');
    $('#sr-subj').value = ''; $('#sr-desc').value = ''; $('#sr-desc-count').textContent = '0/600';
    ['sr-subj', 'sr-desc'].forEach(function (i) { fieldError(i, ''); });
    ['sr-cat', 'sr-ent'].forEach(function (i) { $('#' + i).classList.remove('is-error'); $('#' + i + ' .trigger').removeAttribute('aria-invalid'); });
    $('#sr-errors').textContent = '';
  }

  /* ------------------------------------------------------------------ exposure drill: a column is a link to its region's positions */
  function drill(el) {
    var lab = el.getAttribute('aria-label') || '';
    var r = D.regions.filter(function (x) { return lab.indexOf(x.name) >= 0; })[0]; if (!r) { return; }
    location.href = 'risk.html' + qs({ region: r.id }).replace(/entity=[^&]*&?/, '') + '#records';
  }
  document.addEventListener('click', function (e) {
    if (!e.target.closest || !e.target.closest('#ov-exp svg')) { return; }
    var mk = e.target.closest('.dv-series') || document.elementsFromPoint(e.clientX, e.clientY).filter(function (el) { return el.classList && el.classList.contains('dv-series'); })[0];
    if (mk) { drill(mk); }
  });
  document.addEventListener('keydown', function (e) { if (e.key !== 'Enter') { return; } var mk = e.target.closest && e.target.closest('#ov-exp .dv-series'); if (mk) { drill(mk); } });

  /* ------------------------------------------------------------------ settings prefs */
  if (PAGE === 'settings') {
    ddSet($('#s-entity'), DEF.entity || 'all'); segSet($('#s-range'), DEF.range || '30');
    var NT = store.get('notify', null);
    $$('input[data-pref="notify"]').forEach(function (c) {
      if (NT && c.id in NT) { c.checked = NT[c.id]; }
      c.addEventListener('change', function () { var o = store.get('notify', {}) || {}; o[c.id] = c.checked; store.set('notify', o); toast('ok', 'Notification preference saved.'); });
    });
  }

  /* ------------------------------------------------------------------ nav collapse persists (the shell's own toggle does the work) */
  (function () {
    var sh = $('#shell'), tg = $('[data-navtoggle="shell"]');
    if (!sh || !tg) { return; }
    if (store.get('nav', null) === 'rail' && sh.getAttribute('data-nav') !== 'rail') { tg.click(); }
    new MutationObserver(function () { var v = sh.getAttribute('data-nav'); if (v === 'rail' || v === 'expanded') { store.set('nav', v); } }).observe(sh, { attributes: true, attributeFilter: ['data-nav'] });
  }());

  /* ------------------------------------------------------------------ boot */
  syncControls(); decorateLinks(); refresh();
  var openId = new URLSearchParams(location.search).get('open');
  if (openId) {
    var opener = { payments: function () { openPayment(+openId); }, risk: function () { openException(openId); } }[PAGE];
    if (opener) { setTimeout(opener, 50); }
  }
  window.CEO_APP = { F: F, refresh: refresh, gridRows: function () { return GRID ? GRID.rows.length : null; }, WF: WF };
}());
