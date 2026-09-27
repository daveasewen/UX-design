/* CEO banking prototype — the page's own wiring (s258-D1: authored JavaScript, declared).
   Reads ONE dataset (CEO_DATA). Drives: shell nav + crumbs, shared filters (URL + localStorage),
   KPI tiles, dvRender charts + legends + drill-through, the Data-grid (through its own verbatim
   script's globals), the drawer, toasts, workflows and persistence. Illustrative data only. */
(function () {
  'use strict';
  var D = CEO_DATA, PAGE = document.body.getAttribute('data-page');
  var STORE = 'ceo-proto-v1', THEME = 'ceo-proto-theme';
  var MON = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  function $(s, r) { return (r || document).querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function fdate(iso) { var p = iso.split('-'); return +p[2] + ' ' + MON[+p[1] - 1] + ' ' + p[0]; }
  function sdate(iso) { var p = iso.split('-'); return +p[2] + ' ' + MON[+p[1] - 1]; }
  function grp(n, dp) { return Math.abs(n).toFixed(dp).replace(/\B(?=(\d{3})+(?!\d))/g, ','); }
  function big(n) { var a = Math.abs(n); return a >= 1e9 ? grp(n / 1e9, 2) + 'bn' : a >= 1e6 ? grp(n / 1e6, 1) + 'm' : a >= 1e3 ? grp(n / 1e3, 0) + 'k' : grp(n, 0); }
  function money(n) { return (n < 0 ? '−' : '') + '£' + big(n); }
  function local(n, ccy) { return ccy + ' ' + (n < 0 ? '−' : '') + grp(n, 2); }
  function m1(n) { return Math.round(n / 1e5) / 10; }            /* £ -> £m, one decimal */
  function sum(a, f) { var t = 0; a.forEach(function (x) { t += f ? f(x) : x; }); return t; }
  function initials(s) { return s.split(/\s+/).filter(Boolean).slice(0, 2).map(function (w) { return w[0]; }).join('').toUpperCase(); }
  function entName(id) { var e = D.entities.filter(function (x) { return x.id === id; })[0]; return e ? e.name : id; }

  /* ---------------- persistence ---------------- */
  function load() { try { return JSON.parse(localStorage.getItem(STORE)) || {}; } catch (e) { return {}; } }
  var S = load();
  ['decisions', 'acks', 'read', 'prefs', 'grid', 'amend'].forEach(function (k) { S[k] = S[k] || {}; });
  S.requests = S.requests || []; S.audit = S.audit || [];
  function save() { try { localStorage.setItem(STORE, JSON.stringify(S)); } catch (e) { /* private mode: state lives for the tab */ } }
  function audit(what, id, note) { S.audit.unshift({ at: new Date().toISOString(), by: D.user.name, what: what, id: id, note: note || '' }); S.audit = S.audit.slice(0, 200); save(); }

  /* ---------------- shared filters: URL first, then this browser, then settings defaults ---------------- */
  var Q = new URLSearchParams(location.search);
  var DEF = S.prefs.defaults || { entity: 'all', region: 'all', days: '30' };
  var F = {
    entity: Q.get('entity') || (S.filters && S.filters.entity) || DEF.entity,
    region: Q.get('region') || (S.filters && S.filters.region) || DEF.region,
    days: Q.get('days') || (S.filters && S.filters.days) || DEF.days
  };
  function writeState() {
    S.filters = { entity: F.entity, region: F.region, days: F.days }; save();
    var q = new URLSearchParams(location.search);
    ['entity', 'region', 'days'].forEach(function (k) { q.set(k, F[k]); });
    history.replaceState(null, '', location.pathname + '?' + q.toString() + location.hash);
    decorateLinks();
  }
  function qs(extra) {
    var q = new URLSearchParams({ entity: F.entity, region: F.region, days: F.days });
    if (extra) { Object.keys(extra).forEach(function (k) { q.set(k, extra[k]); }); }
    return '?' + q.toString();
  }
  function href(slug, extra) { return slug + '.html' + qs(extra); }
  function decorateLinks() {
    $$('a[data-slug]').forEach(function (a) { a.setAttribute('href', href(a.getAttribute('data-slug'), a.__extra)); });
  }
  var DAYS = function () { return D.days.slice(-(+F.days)); };
  function inScope(r) {
    if (F.entity !== 'all' && r.entity !== F.entity) { return false; }
    if (F.region !== 'all' && r.region !== F.region) { return false; }
    return true;
  }
  function inWindow(iso) { return iso >= DAYS()[0]; }
  function scopeEnts() { return D.entities.filter(function (e) { return inScope({ entity: e.id, region: e.region }); }); }
  function scopeLabel() {
    var a = F.entity === 'all' ? 'All entities' : entName(F.entity);
    var b = F.region === 'all' ? 'all regions' : F.region;
    return a + ', ' + b + ', last ' + F.days + ' days';
  }

  /* ---------------- derived series (GBP) ---------------- */
  function acctScope() { var ids = scopeEnts().map(function (e) { return e.id; }); return D.accounts.filter(function (a) { return ids.indexOf(a.entity) >= 0; }); }
  function cashSeries() {
    var off = D.days.length - (+F.days), acc = acctScope();
    return DAYS().map(function (d, i) { return sum(acc, function (a) { return a.series[off + i] / D.fx[a.ccy]; }); });
  }
  function facScope() { return D.facilities.filter(inScope); }
  function undrawnSeries() {
    var off = D.days.length - (+F.days), f = facScope().filter(function (x) { return x.committed; });
    return DAYS().map(function (d, i) { return sum(f, function (x) { return x.limitGbp - x.drawnSeries[off + i]; }); });
  }
  function groupCash0() { return sum(D.accounts, function (a) { return a.series[D.days.length - 1] / D.fx[a.ccy]; }); }
  function buffer() { var c = cashSeries(); return D.minBuffer * (c[c.length - 1] / groupCash0()); }
  function maturing() {
    var lim = new Date(D.asOf); lim.setDate(lim.getDate() + 60); var iso = lim.toISOString().slice(0, 10);
    return sum(facScope().filter(function (f) { return f.maturity <= iso; }), function (f) { return f.drawnGbp; });
  }
  function liqSeries() { var c = cashSeries(), u = undrawnSeries(); return c.map(function (v, i) { return v + u[i]; }); }
  function headSeries() { var l = liqSeries(), b = buffer(), m = maturing(); return l.map(function (v) { return v - b - m; }); }
  function txScope() { return D.transactions.filter(function (t) { return inScope(t) && inWindow(t.date); }); }
  function payStatus(p) { return (S.decisions[p.id] && S.decisions[p.id].status) || p.status; }
  function payScope() { return D.payments.filter(function (p) { return inScope(p) && inWindow(p.date); }); }
  function posScope() { return D.positions.filter(inScope); }
  function excStatus(x) { return S.acks[x.id] ? 'Acknowledged' : x.status; }
  function excScope() { return D.exceptions.filter(inScope); }
  function tradeScope() { return D.trade.filter(inScope); }
  function dealScope() { return D.deals.filter(function (x) { return inScope(x) && inWindow(x.date); }); }
  function allRequests() { return S.requests.concat(D.requests).map(function (r) { var o = Object.assign({}, r); if (S.decisions[r.id]) { o.status = S.decisions[r.id].status; } return o; }); }
  function reqScope() { return allRequests().filter(function (r) { return F.entity === 'all' || r.entity === F.entity; }); }

  /* ---------------- toast (Toast.reference.html spawn pattern) ---------------- */
  var region = $('#toastRegion');
  function toast(kind, msg) {
    var glyph = { ok: 'to-success', info: 'to-info', warn: 'to-warning' }[kind];
    var t = document.createElement('div'); t.className = 'toast ' + kind; t.setAttribute('role', 'status');
    t.setAttribute('data-carries', 'symbol label');
    t.innerHTML = '<span class="ic"><svg aria-hidden="true"><use href="#' + glyph + '"/><\/svg></span><p class="msg t-ed-body">' + esc(msg) +
      '</p><button class="x" type="button" aria-label="Dismiss message"><svg aria-hidden="true"><use href="#to-close"/><\/svg></button>';
    region.appendChild(t);
    var origin = document.activeElement, timer = setTimeout(leave, 6000);
    function leave() { if (matchMedia('(prefers-reduced-motion: reduce)').matches) { t.remove(); return; } t.classList.add('leaving'); t.addEventListener('transitionend', function () { t.remove(); }, { once: true }); setTimeout(function () { t.remove(); }, 800); }
    t.querySelector('.x').addEventListener('click', function () { clearTimeout(timer); leave(); if (origin && document.body.contains(origin)) { origin.focus(); } });
  }

  /* ---------------- templates ---------------- */
  function tpl(id) { return document.getElementById(id).content.firstElementChild.cloneNode(true); }
  var uid = 0; function nid(p) { uid += 1; return p + '-' + uid; }
  function button(kind, label, onClick) {
    var w = tpl(kind === 'primary' ? 'tpl-btn-primary' : 'tpl-btn-secondary'), b = w.querySelector('button');
    b.textContent = label; b.type = 'button'; if (onClick) { b.addEventListener('click', onClick); }
    return w;
  }
  function segmented(label, options, current, onPick) {
    var w = tpl('tpl-seg'), seg = w.querySelector('.seg'), bs = $$('button', seg);
    seg.setAttribute('aria-label', label);
    bs.forEach(function (b, i) { if (i >= options.length) { b.remove(); } });
    bs = $$('button', seg);
    options.forEach(function (o, i) { bs[i].textContent = o.label; bs[i].setAttribute('data-value', o.value); bs[i].setAttribute('aria-pressed', String(o.value === current)); });
    function moveInd() { var ind = seg.querySelector('.ind'), a = seg.querySelector('button[aria-pressed="true"]'); if (!ind || !a) { return; }
      var sr = seg.getBoundingClientRect(), br = a.getBoundingClientRect(); ind.style.left = (br.left - sr.left - seg.clientLeft) + 'px'; ind.style.width = br.width + 'px'; }
    bs.forEach(function (b) { b.addEventListener('click', function () { bs.forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); }); moveInd(); onPick(b.getAttribute('data-value')); }); });
    requestAnimationFrame(moveInd); addEventListener('resize', moveInd); w.__place = moveInd;
    return w;
  }
  function dropdown(label, options, current, onPick) {
    var w = tpl('tpl-dd'), dd = w.querySelector('.dd'), lab = dd.querySelector('label'), trig = dd.querySelector('.trigger'), menu = dd.querySelector('.menu');
    var id = nid('dd'); lab.id = id + '-l'; lab.setAttribute('for', id + '-t'); lab.textContent = label;
    trig.id = id + '-t'; trig.setAttribute('aria-controls', id + '-m'); trig.setAttribute('aria-labelledby', id + '-l ' + id + '-t');
    menu.id = id + '-m'; menu.setAttribute('aria-labelledby', id + '-l');
    var proto = menu.querySelector('li.opt'); menu.innerHTML = '';
    options.forEach(function (o) { var li = proto.cloneNode(true); li.firstChild.textContent = o.label + ' '; li.setAttribute('data-value', o.value); li.setAttribute('aria-selected', String(o.value === current)); menu.appendChild(li); });
    var cur = options.filter(function (o) { return o.value === current; })[0] || options[0];
    trig.querySelector('.ddval').textContent = cur.label;
    var opts = $$('[role=option]', menu);
    function open(o) { menu.setAttribute('data-open', String(o)); trig.setAttribute('aria-expanded', String(o));
      if (o) { (opts.filter(function (x) { return x.getAttribute('aria-selected') === 'true'; })[0] || opts[0]).focus(); } }
    function choose(o) { opts.forEach(function (x) { x.setAttribute('aria-selected', String(x === o)); }); trig.querySelector('.ddval').textContent = o.firstChild.textContent.trim(); open(false); trig.focus(); onPick(o.getAttribute('data-value')); }
    trig.addEventListener('click', function () { open(menu.getAttribute('data-open') !== 'true'); });
    trig.addEventListener('keydown', function (e) { if (['ArrowDown', 'Enter', ' '].indexOf(e.key) >= 0) { e.preventDefault(); open(true); } });
    opts.forEach(function (o) { o.addEventListener('click', function () { choose(o); });
      o.addEventListener('keydown', function (e) { var i = opts.indexOf(o);
        if (e.key === 'ArrowDown') { e.preventDefault(); opts[(i + 1) % opts.length].focus(); }
        else if (e.key === 'ArrowUp') { e.preventDefault(); opts[(i - 1 + opts.length) % opts.length].focus(); }
        else if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); choose(o); }
        else if (e.key === 'Escape') { open(false); trig.focus(); } }); });
    return w;
  }
  document.addEventListener('click', function (e) { if (!e.target.closest('.dd')) { $$('.dd').forEach(function (dd) { var m = dd.querySelector('.menu'); if (m) { m.setAttribute('data-open', 'false'); dd.querySelector('.trigger').setAttribute('aria-expanded', 'false'); } }); } });
  function heading(text, linkLabel, linkHref) {
    var w = tpl('tpl-heading'), h = w.querySelector('h2'), a = w.querySelector('a');
    h.textContent = text; h.id = nid('h');
    if (linkLabel) { a.querySelector('.lbl').textContent = linkLabel; a.setAttribute('data-slug', linkHref[0]); a.__extra = linkHref[1]; a.setAttribute('href', href(linkHref[0], linkHref[1])); }
    else { a.remove(); }
    return w;
  }
  /* rows: {title, status:{kind:'ok'|'warn'|'err', text}|null, tag, desc, amount, avatar, onOpen} */
  function list(rows, emptyText) {
    var w = tpl('tpl-list'), ul = w.querySelector('ul'); ul.id = nid('list');
    var proto = ul.querySelector('li'); ul.innerHTML = '';
    if (!rows.length) { var p = document.createElement('p'); p.className = 't-ed-body-small'; p.textContent = emptyText || 'Nothing to show for the current filters.'; w.appendChild(p); return w; }
    rows.forEach(function (r) {
      var li = proto.cloneNode(true), b = li.querySelector('button.row');
      b.querySelector('.avatar').textContent = r.avatar || initials(r.title); b.querySelector('.avatar').setAttribute('aria-label', r.avatarLabel || r.title);
      b.querySelector('.title').textContent = r.title;
      var st = b.querySelector('.status');
      if (r.status) { st.className = 'status ' + r.status.kind; st.lastChild.textContent = r.status.text; } else { st.remove(); }
      b.querySelector('.desc').textContent = r.desc; b.querySelector('.amount').textContent = r.amount || '';
      b.addEventListener('click', r.onOpen);
      ul.appendChild(li);
    });
    return w;
  }
  function summary(rows) {
    var w = tpl('tpl-summary'), dl = w.querySelector('dl'), proto = dl.querySelector('.summary__row'); dl.innerHTML = '';
    rows.forEach(function (r) { var row = proto.cloneNode(true); row.querySelector('dt').textContent = r[0]; row.querySelector('dd').textContent = r[1]; dl.appendChild(row); });
    return w;
  }

  /* ---------------- drawer (Drawer.reference.html open order: show · 2 frames · focus in · then inert) ---------------- */
  var scrim = $('#scrim'), sheet = $('#sheet'), app = $('#app'), noteWrap = $('[data-part="note"]'), partsHome = $('#parts');
  var noteGroup = noteWrap.querySelector('.tx-group'), noteTa = noteGroup.querySelector('textarea');
  var opener = null, current = null;
  function focusables() { return $$('button,[href],textarea,input,[tabindex]:not([tabindex="-1"])', sheet).filter(function (el) { return !el.disabled && el.offsetParent !== null; }); }
  function setNoteError(msg) {
    var old = noteGroup.querySelector('.tx-msg'); if (old) { old.remove(); }
    noteGroup.classList.toggle('is-error', !!msg);
    if (msg) { noteTa.setAttribute('aria-invalid', 'true'); var m = document.createElement('div'); m.className = 'tx-msg'; m.id = 't1-err';
      m.innerHTML = '<span class="ic" aria-hidden="true"><svg class="icn" viewBox="0 0 18 18"><use href="#ic-error"/><\/svg></span><p class="t-ed-body">' + esc(msg) + '</p>';
      noteGroup.appendChild(m); noteTa.setAttribute('aria-describedby', 't1-help t1-count t1-err'); }
    else { noteTa.removeAttribute('aria-invalid'); noteTa.setAttribute('aria-describedby', 't1-help t1-count'); }
  }
  function openDrawer(o) {
    current = o; opener = document.activeElement;
    $('#dtitle').textContent = o.title;
    var body = $('#dbody'); body.innerHTML = '';
    if (o.lead) { var p = document.createElement('p'); p.className = 't-ed-body'; p.textContent = o.lead; body.appendChild(p); }
    if (o.rows) { body.appendChild(summary(o.rows)); }
    if (o.extra) { body.appendChild(o.extra); }
    if (o.note) {
      noteGroup.querySelector('label').textContent = o.note.label; $('#t1-help').textContent = o.note.help || '';
      noteTa.value = ''; noteTa.dispatchEvent(new Event('input')); setNoteError(null); body.appendChild(noteWrap);   /* move the SCOPE, not just the group: .cn-textarea styles it */
    }
    var act = $('#act'), cancel = $('#cancel');
    act.hidden = !o.primary; if (o.primary) { act.textContent = o.primary.label; }
    cancel.textContent = o.secondary ? o.secondary.label : 'Close';
    scrim.classList.add('open'); sheet.classList.add('open');
    requestAnimationFrame(function () { requestAnimationFrame(function () {
      var f = focusables(); if (f.length) { f[0].focus(); }
      app.inert = true; app.setAttribute('aria-hidden', 'true');
    }); });
  }
  function closeDrawer() {
    if (!sheet.classList.contains('open')) { return; }
    scrim.classList.remove('open'); sheet.classList.remove('open');
    app.inert = false; app.removeAttribute('aria-hidden');
    if (noteWrap.parentNode !== partsHome && !noteWrap.__pinned) { partsHome.appendChild(noteWrap); }
    current = null; if (opener && document.body.contains(opener)) { opener.focus(); }
  }
  function runAction(a) {
    if (!a) { closeDrawer(); return; }
    var res = a.run(noteTa.value.trim());
    if (res === true) { closeDrawer(); } else if (typeof res === 'string') { setNoteError(res); noteTa.focus(); }
  }
  $('#close').addEventListener('click', closeDrawer);
  scrim.addEventListener('click', closeDrawer);
  $('#act').addEventListener('click', function () { runAction(current && current.primary); });
  $('#cancel').addEventListener('click', function () { runAction(current && current.secondary); });
  document.addEventListener('keydown', function (e) {
    if (!sheet.classList.contains('open')) { return; }
    if (e.key === 'Escape') { closeDrawer(); return; }
    if (e.key === 'Tab') { var f = focusables(), a = f[0], z = f[f.length - 1];
      if (e.shiftKey && document.activeElement === a) { e.preventDefault(); z.focus(); }
      else if (!e.shiftKey && document.activeElement === z) { e.preventDefault(); a.focus(); } }
  });

  /* ---------------- theme ---------------- */
  function theme() { return document.documentElement.getAttribute('data-theme'); }
  function setTheme(t) { document.documentElement.setAttribute('data-theme', t); try { localStorage.setItem(THEME, t); } catch (e) { }
    var q = new URLSearchParams(location.search); q.delete('theme'); history.replaceState(null, '', location.pathname + '?' + q.toString());
    $$('.seg[data-theme-switch] button').forEach(function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-value') === t)); });
    window.dispatchEvent(new Event('resize')); }
  function themeSwitch() { var w = segmented('Colour mode', [{ label: 'Light', value: 'light' }, { label: 'Dark', value: 'dark' }], theme(), function (v) { setTheme(v); toast('info', (v === 'dark' ? 'Dark' : 'Light') + ' mode on.'); });
    w.querySelector('.seg').setAttribute('data-theme-switch', ''); return w; }

  /* ---------------- shell: nav, crumbs, actions ---------------- */
  var NAV_GROUPS = [{ label: null, items: ['index'] }, { label: 'Cash and funding', items: ['accounts', 'liquidity', 'payments'] },
    { label: 'Markets and risk', items: ['fx', 'risk', 'trade'] }, { label: 'Insight and service', items: ['reports', 'messages'] }];
  var ICON = { index: 'ap-dashboard', accounts: 'ic-account', liquidity: 'ap-liquidity', payments: 'ic-transfer', fx: 'ap-fx', risk: 'ap-alert', trade: 'ap-trade', reports: 'ap-report', messages: 'ap-message', settings: 'ic-settings' };
  function label(slug) { return CEO_NAV.filter(function (n) { return n.slug === slug; })[0].label; }
  function buildNav() {
    var nav = $('#nav-wide'), body = nav.querySelector('.sn-body');
    nav.querySelector('.sn-brand').textContent = 'Meridian Holdings';
    var protoGroup = body.querySelector('.sn-group-label').closest('.sn-group').cloneNode(true);
    var protoLi = body.querySelector('a.sn-link').closest('li').cloneNode(true);
    protoLi.querySelector('a').removeAttribute('aria-current');
    body.innerHTML = '';
    NAV_GROUPS.forEach(function (g, gi) {
      var grpEl = protoGroup.cloneNode(true), ul = grpEl.querySelector('ul'), lab = grpEl.querySelector('.sn-group-label');
      if (g.label) { lab.textContent = g.label; lab.id = 'nw-g' + gi; ul.setAttribute('aria-labelledby', lab.id); } else { lab.remove(); ul.removeAttribute('aria-labelledby'); }
      ul.innerHTML = '';
      g.items.forEach(function (slug) { var li = protoLi.cloneNode(true), a = li.querySelector('a');
        a.setAttribute('data-slug', slug); a.querySelector('.sn-label').textContent = label(slug);
        a.querySelector('use').setAttribute('href', '#' + ICON[slug]);
        if (slug === PAGE) { a.setAttribute('aria-current', 'page'); } ul.appendChild(li); });
      body.appendChild(grpEl);
    });
    var foot = nav.querySelector('.sn-foot a.sn-link'); foot.setAttribute('data-slug', 'settings');
    if (PAGE === 'settings') { foot.setAttribute('aria-current', 'page'); }
    var tog = nav.querySelector('.sn-toggle');
    function rail(on) { nav.classList.toggle('is-rail', on); tog.setAttribute('aria-expanded', String(!on)); tog.setAttribute('aria-label', on ? 'Expand navigation' : 'Collapse navigation');
      nav.setAttribute('aria-label', on ? 'Main, collapsed' : 'Main'); tog.querySelector('use').setAttribute('href', on ? '#ic-chevron-right' : '#ic-chevron-left'); window.dispatchEvent(new Event('resize')); }
    rail(!!S.navRail);
    tog.addEventListener('click', function () { S.navRail = !nav.classList.contains('is-rail'); save(); rail(S.navRail); });
  }
  function buildCrumbs() {
    var ol = $('.sh-crumbs ol'), lis = $$('li', ol), first = lis[0].cloneNode(true), last = lis[lis.length - 1].cloneNode(true);
    ol.innerHTML = '';
    first.querySelector('a').textContent = 'Meridian Holdings'; first.querySelector('a').setAttribute('data-slug', 'index');
    ol.appendChild(first);
    if (PAGE !== 'index') { last.querySelector('[aria-current]').textContent = label(PAGE); ol.appendChild(last); }
    else { first.querySelector('a').setAttribute('aria-current', 'page'); }
  }
  function buildActions() {
    var bs = $$('.sh-actions button');
    bs[0].addEventListener('click', function () {
      var s = $('#dgSearch');
      if (s) { s.focus(); s.scrollIntoView({ block: 'center' }); toast('info', 'Search this page’s records, then press Enter to apply.'); }
      else { location.href = href('accounts', { focus: 'search' }); }
    });
    bs[1].addEventListener('click', function () {
      openDrawer({ title: D.user.name, lead: D.user.role + ', ' + entName(D.user.entity) + '. Simulated session — no real credentials or banking connection.',
        rows: [['Approval limit', money(D.user.limitGbp)], ['Entities in view', String(D.entities.length)], ['Decisions recorded here', String(Object.keys(S.decisions).length)],
          ['Acknowledgements recorded here', String(Object.keys(S.acks).length)], ['Last action', S.audit[0] ? S.audit[0].what + ' ' + S.audit[0].id : 'None yet']],
        secondary: { label: 'Close', run: function () { return true; } } });
    });
    var ta = $('#title-actions');
    ta.appendChild(themeSwitch());
    ta.appendChild(button('secondary', 'Export CSV', function () { exportPage(); }));
  }
  function csv(name, head, rows) {
    var lines = [head.join(',')].concat(rows.map(function (r) { return r.map(function (v) { v = String(v == null ? '' : v); return /[",\n]/.test(v) ? '"' + v.replace(/"/g, '""') + '"' : v; }).join(','); }));
    var blob = new Blob([lines.join('\n')], { type: 'text/csv' }), a = document.createElement('a');
    a.href = URL.createObjectURL(blob); a.download = name + '-' + D.asOf + '.csv'; document.body.appendChild(a); a.click();
    setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 500);
    toast('ok', 'Exported ' + rows.length + ' row' + (rows.length === 1 ? '' : 's') + ' to ' + a.download + ' (' + scopeLabel() + ').');
    audit('Exported', name, rows.length + ' rows');
  }

  /* ---------------- filters row ---------------- */
  function buildFilters() {
    var row = $('#filter-row');
    var ents = [{ label: 'All entities', value: 'all' }].concat(D.entities.map(function (e) { return { label: e.name, value: e.id }; }));
    var regs = [{ label: 'All regions', value: 'all' }].concat(D.regions.map(function (r) { return { label: r, value: r }; }));
    var days = [{ label: 'Last 7 days', value: '7' }, { label: 'Last 14 days', value: '14' }, { label: 'Last 30 days', value: '30' }];
    row.appendChild(dropdown('Entity', ents, F.entity, function (v) { F.entity = v; changed(); }));
    row.appendChild(dropdown('Region', regs, F.region, function (v) { F.region = v; changed(); }));
    row.appendChild(dropdown('Period', days, F.days, function (v) { F.days = v; changed(); }));
    $('#fx-note').textContent = D.fxNote + ' GBP 1 = ' + Object.keys(D.fx).filter(function (k) { return k !== 'GBP'; }).map(function (k) { return k + ' ' + D.fx[k]; }).join(' · ') + '. Reporting currency GBP. Data as of ' + fdate(D.asOf) + '.';
  }
  function changed() { writeState(); renderPage(); toast('info', 'Showing ' + scopeLabel() + '.'); }

  /* ---------------- KPI tile (Kpi-tile.reference.html .as-link) ---------------- */
  function kpi(key, o) {
    var t = $('[data-kpi="' + key + '"] .kpi-tile'); if (!t) { return; }
    t.setAttribute('aria-label', o.label + ', ' + o.text + ', ' + scopeLabel());
    var a = t.querySelector('.kpi-link'); a.textContent = o.label; a.setAttribute('data-slug', o.slug); a.__extra = o.extra; a.setAttribute('href', href(o.slug, o.extra));
    var v = t.querySelector('.kpi-val'); v.children[0].textContent = o.unit || ''; v.children[1].textContent = o.text;
    var s = o.series || [], first = s[0], last = s[s.length - 1];
    var ch = first ? (last - first) / (Math.abs(first) || 1) * 100 : (last ? 100 : 0);
    if (o.count && !o.delta) { var dd = last - first; o.delta = dd === 0 ? 'No change' : (dd > 0 ? '+' : '\u2212') + Math.abs(dd) + ' in ' + F.days + ' days'; }
    var dir = !s.length || Math.abs(ch) < 0.05 ? 'flat' : ch > 0 ? 'up' : 'down';
    var dl = t.querySelector('.kpi-delta'); dl.className = 'kpi-delta ' + dir;
    dl.querySelector('use').setAttribute('href', '#kpi-' + dir);
    dl.children[1].textContent = o.delta || (dir === 'flat' ? 'No change' : (ch > 0 ? '+' : '−') + Math.abs(ch).toFixed(1) + '% ' + dir);
    dl.querySelector('.kpi-per').textContent = o.per || ('vs ' + F.days + ' days ago');
    var svg = t.querySelector('svg.spark-inline');
    if (svg && s.length > 1) {
      var lo = Math.min.apply(null, s), hi = Math.max.apply(null, s), sp = hi - lo || 1;
      var pts = s.map(function (v2, i) { return (3 + i * 194 / (s.length - 1)).toFixed(1) + ',' + (45 - (v2 - lo) / sp * 42).toFixed(1); });
      svg.setAttribute('data-trend', dir);
      svg.querySelector('polyline').setAttribute('points', pts.join(' '));
      svg.querySelector('polygon').setAttribute('points', pts.join(' ') + ' 197.0,45 3.0,45');
    }
  }

  /* ---------------- charts (dvRender from CEO_DATA) ---------------- */
  var LET = 'ABCDEFGHIJ';
  function syncLegend(fig, names) {
    var ul = fig.querySelector('ul.dv-leg'); if (!ul) { return; }
    var rows = $$('li.dv-legrow', ul), proto = rows[0], reset = ul.querySelector('.dv-leg-reset-wrap');
    rows.forEach(function (r) { r.remove(); });
    names.forEach(function (n, i) {
      var li = proto.cloneNode(true), id = String(i + 1), sw = li.querySelector('.dv-leg-sw'), bt = li.querySelector('.dv-leg-item');
      li.setAttribute('data-series', id); sw.setAttribute('aria-checked', 'true'); sw.setAttribute('aria-label', 'Show or hide ' + n);
      sw.style.setProperty('--sc', 'var(--data-series-' + ((i % 5) + 1) + ')');
      var shapes = ['sw-circle', 'sw-square', 'sw-diamond']; shapes.forEach(function (c) { sw.classList.remove(c); });
      if (proto.querySelector('.sw-circle,.sw-square,.sw-diamond')) { sw.classList.add(shapes[i % 3]); }
      bt.setAttribute('data-series', id); bt.setAttribute('aria-pressed', 'false'); bt.setAttribute('aria-label', 'Isolate ' + n);
      var k = bt.querySelector('.dv-key'); if (k) { k.textContent = LET[i]; }
      bt.querySelector('.dv-leg-name').textContent = n;
      li.classList.remove('is-ghost', 'is-faded', 'is-peek');
      ul.insertBefore(li, reset);
    });
    delete ul.__dv; var rb = ul.querySelector('.dv-leg-reset'); if (rb) { rb.disabled = true; }
  }
  var CH = {};
  function chart(key, o) {
    var tile = $('[data-chart="' + key + '"]'); if (!tile) { return; }
    var fig = tile.querySelector('figure.dv'); CH[key] = { fig: fig, o: o };
    drawChart(key);
  }
  function drawChart(key) {
    var c = CH[key], fig = c.fig, o = c.o, spec = o.spec();
    var empty = !spec.categories.length;
    if (empty) { spec.categories = ['No data in scope']; spec.series = spec.series.map(function (s) { return { name: s.name, values: [0] }; }); }
    var view = fig.querySelector('[data-dv-view-btn][aria-pressed="true"]');
    if (view && o.view) { spec = o.view(view.getAttribute('data-dv-view-btn'), spec); }
    var title = empty ? 'No data for ' + scopeLabel() : (typeof o.title === 'function' ? o.title(spec) : o.title);
    var h = fig.querySelector('.dv-title'); if (h) { h.textContent = title; }
    fig.setAttribute('data-lockup-title', title);
    var cap = fig.querySelector('figcaption'); if (cap) { cap.textContent = spec.caption; }
    var tp = fig.querySelector('.dv-tablepanel'); if (tp) { tp.setAttribute('aria-label', spec.caption + ', data table'); }
    window.dvRender(fig, spec);
    var names = (spec.type === 'donut' || spec.type === 'pie') ? spec.categories : spec.series.map(function (s) { return s.name; });
    syncLegend(fig, names);
    fig.__drill = empty ? null : o.drill;
    if (o.drill) { $$('svg [data-tip]', fig).forEach(function (m) { m.setAttribute('aria-label', (m.getAttribute('aria-label') || '') + '. Press Enter to see the underlying records.'); }); }
  }
  function catOf(mark) { var t = mark.getAttribute('data-tip') || ''; return t.split('·').pop().split(':')[0].trim(); }
  document.addEventListener('click', function (e) {
    var m = e.target.closest && e.target.closest('figure.dv svg [data-tip]'); if (!m) { return; }
    var fig = m.closest('figure.dv'); if (fig.__drill) { fig.__drill(catOf(m)); }
  });
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Enter') { return; }
    var m = e.target.closest && e.target.closest('figure.dv svg [data-tip]'); if (!m) { return; }
    var fig = m.closest('figure.dv'); if (fig.__drill) { e.preventDefault(); fig.__drill(catOf(m)); }
  });
  /* view switches inside a figure (sort, value/percent): dv-behaviour flips aria-pressed; we re-render */
  document.addEventListener('click', function (e) {
    var b = e.target.closest && e.target.closest('figure.dv [data-dv-view-btn]'); if (!b) { return; }
    var fig = b.closest('figure.dv');
    Object.keys(CH).forEach(function (k) { if (CH[k].fig === fig) { setTimeout(function () { drawChart(k); }, 0); } });
  });
  function sortView(v, spec) {
    if (v === 'orig' || !spec.series.length) { return spec; }
    var ix = spec.categories.map(function (c, i) { return i; }), vals = spec.series[0].values;
    ix.sort(function (a, b) { return v === 'asc' ? vals[a] - vals[b] : vals[b] - vals[a]; });
    return Object.assign({}, spec, { categories: ix.map(function (i) { return spec.categories[i]; }), series: spec.series.map(function (s) { return { name: s.name, values: ix.map(function (i) { return s.values[i]; }) }; }) });
  }
  function shareView(v, spec) {
    if (v !== 'percent') { return spec; }
    var tot = sum(spec.series[0].values) || 1;
    return Object.assign({}, spec, { unit: '%', format: 'percent', series: [{ name: 'Share', values: spec.series[0].values.map(function (x) { return Math.round(x / tot * 1000) / 10; }) }] });
  }
  function top(pairs, n) { pairs.sort(function (a, b) { return b[1] - a[1]; }); if (pairs.length <= n) { return pairs; }
    var head = pairs.slice(0, n - 1), rest = sum(pairs.slice(n - 1), function (p) { return p[1]; }); return head.concat([['Other', rest]]); }
  function by(rows, keyF, valF) { var m = {}; rows.forEach(function (r) { var k = keyF(r); m[k] = (m[k] || 0) + (valF ? valF(r) : 1); }); return Object.keys(m).map(function (k) { return [k, m[k]]; }); }
  /* day/month labels (28/8): short enough that the first and last band labels clear the value axes (geometry G7) */
  var dayCats = function () { return DAYS().map(function (iso) { var p = iso.split('-'); return +p[2] + '/' + (+p[1]); }); };

  /* ---------------- data grid (Data-grid.reference.html, verbatim script, fed through its globals) ---------------- */
  var G = null;
  function gridSetup(o) {
    if (typeof DATA === 'undefined' || !document.getElementById('dg')) { return; }
    if (G) { G.rows = o.rows; G.open = o.open; return; }
    G = o;
    /* EXTENDED from outside the verbatim script (s258-D1): the snippet's renderPager lists EVERY page,
       which at 260 rows / 8 per page is 33 buttons and overflows the tile. Same button markup, windowed,
       with Pagination.reference.html's own aria-hidden ellipsis. */
    window.renderPager = function (pages) {
      var ul = document.getElementById('pgList'), cur = state.page, want = [1, pages, cur - 1, cur, cur + 1].filter(function (p) { return p >= 1 && p <= pages; });
      var nums = want.filter(function (p, i) { return want.indexOf(p) === i; }).sort(function (a, b) { return a - b; });
      var h = '<li><button class="pbtn" type="button" aria-label="Previous page" ' + (cur === 1 ? 'disabled' : '') + ' data-go="prev"><svg viewBox="0 0 18 18" aria-hidden="true"><use href="#dg-cleft"/><\/svg><\/button><\/li>';
      nums.forEach(function (p, i) {
        if (i && p - nums[i - 1] > 1) { h += '<li><span class="cn-pagination"><span class="ellipsis" aria-hidden="true">…<\/span><\/span><\/li>'; }
        var on = p === cur;
        h += '<li><button class="pbtn ' + (on ? 't-cm-button' : 't-cm-label') + '" type="button" data-go="' + p + '" ' + (on ? 'aria-current="page" aria-label="Page ' + p + ', current page"' : 'aria-label="Page ' + p + '"') + '>' + p + '<\/button><\/li>';
      });
      h += '<li><button class="pbtn" type="button" aria-label="Next page" ' + (cur === pages ? 'disabled' : '') + ' data-go="next"><svg viewBox="0 0 18 18" aria-hidden="true"><use href="#dg-cright"/><\/svg><\/button><\/li>';
      ul.innerHTML = h;
      ul.querySelectorAll('.pbtn').forEach(function (b) { b.addEventListener('click', function () {
        var g = b.dataset.go; state.page = g === 'prev' ? state.page - 1 : g === 'next' ? state.page + 1 : +g;
        render(); announce('Page ' + state.page + ' of ' + pages + '.'); var f = ul.querySelector('[data-go="' + g + '"]') || ul.querySelector('[aria-current]'); if (f && !f.disabled) { f.focus(); } }); });
    };
    $('#dgTitle').textContent = o.title;
    var s = $('#dgSearch'); s.setAttribute('aria-label', 'Filter ' + o.noun); s.setAttribute('placeholder', 'Filter ' + o.noun + ' — press enter to apply');
    Object.keys(o.cols).forEach(function (k) {
      COLS[k] = o.cols[k];
      var th = $('#tbl thead tr.cols th[data-key="' + k + '"]'); if (!th) { return; }
      th.querySelector('.lbl').textContent = o.cols[k];
      var f = th.querySelector('.colf'); if (f) { f.setAttribute('aria-label', 'Filter by ' + o.cols[k].toLowerCase()); }
      var cm = th.querySelector('.cml'); if (cm) { cm.textContent = o.cols[k] + ' contains'; }
      var cmg = th.querySelector('.colmenu'); if (cmg) { cmg.setAttribute('aria-label', 'Filter by ' + o.cols[k].toLowerCase()); }
      var rz = th.querySelector('.rsz'); if (rz) { rz.setAttribute('aria-label', 'Resize ' + o.cols[k].toLowerCase() + ' column'); }
    });
    var gl = $$('#tbl thead tr.grp .glabel'); gl[0].textContent = o.groups[0]; gl[1].textContent = o.groups[1];
    var saved = S.grid[PAGE];
    if (saved) {
      state.sortKey = saved.sortKey; state.sortDir = saved.sortDir || 'none'; state.pageSize = saved.pageSize || 8; state.page = saved.page || 1;
      state.filters = (saved.filters || []).slice();
      $$('#tbl thead tr.cols th[data-key]').forEach(function (th) { th.setAttribute('aria-sort', th.getAttribute('data-key') === state.sortKey ? state.sortDir : 'none'); });
      $('#pp').value = String(state.pageSize);
    }
    if (o.presetFilter) { state.filters = state.filters.filter(function (f) { return f.key !== o.presetFilter.key; }); state.filters.push(o.presetFilter); state.page = 1; }
    gridFeed();
    ['click', 'keydown', 'change', 'input'].forEach(function (ev) { $('#dg').addEventListener(ev, function () { setTimeout(persistGrid, 0); }); });
    $('#tbody').addEventListener('click', function (e) {
      var td = e.target.closest('td'); if (!td || td.classList.contains('sel') || td.classList.contains('edit') || td.classList.contains('dg-empty')) { return; }
      var tr = td.closest('tr[data-id]'); if (tr) { openRow(+tr.getAttribute('data-id')); }
    });
    $('#tbl').addEventListener('keydown', function (e) {
      if (e.key !== 'Enter') { return; }
      var td = e.target.closest && e.target.closest('tbody td'); if (!td || td.classList.contains('sel') || td.classList.contains('edit')) { return; }
      var tr = td.closest('tr[data-id]'); if (tr) { e.preventDefault(); openRow(+tr.getAttribute('data-id')); }
    });
    $('#dgHint').textContent = 'Arrow keys move between cells. Enter on a row opens its detail; Enter on a column header sorts. Double-click or F2 edits the reference.';
  }
  var ROWS = {};
  function gridFeed() {
    if (!G) { return; }
    var rows = G.rows(); ROWS = {};
    DATA.length = 0;
    rows.forEach(function (r, i) { var row = { id: i + 1, date: r.date, payee: r.payee, ref: r.ref, type: r.type, amount: r.amount }; ROWS[i + 1] = r; DATA.push(row); });
    state.sel.clear(); renderChips(); render(); persistGrid();
  }
  function persistGrid() { if (!G) { return; } S.grid[PAGE] = { sortKey: state.sortKey, sortDir: state.sortDir, pageSize: state.pageSize, page: state.page, filters: state.filters }; save(); }
  function openRow(id) { var r = ROWS[id]; if (r && G.open) { G.open(r.rec); } }

  /* ================================= PAGES ================================= */
  function pctS(a) { return a.toFixed(1) + '%'; }
  function cumCount(rows, key) { return DAYS().map(function (d) { return rows.filter(function (r) { return r[key] <= d; }).length; }); }
  var PAGES = {};

  PAGES.index = function () {
    var cs = cashSeries(), ls = liqSeries(), hs = headSeries(), tx = txScope();
    kpi('cash', { label: 'Cash', slug: 'accounts', unit: '£', text: big(cs[cs.length - 1]), series: cs });
    kpi('liquidity', { label: 'Available liquidity', slug: 'liquidity', unit: '£', text: big(ls[ls.length - 1]), series: ls });
    kpi('headroom', { label: 'Funding headroom', slug: 'liquidity', unit: hs[hs.length - 1] < 0 ? '−£' : '£', text: big(hs[hs.length - 1]), series: hs, per: 'after buffer and 60-day maturities' });
    var net = DAYS().map(function (d) { return sum(tx.filter(function (t) { return t.date === d; }), function (t) { return t.gbp; }); });
    var cum = []; net.reduce(function (a, v) { cum.push(a + v); return a + v; }, 0);
    var nf = cum[cum.length - 1] || 0;
    kpi('netflow', { label: 'Net cash flow', slug: 'accounts', unit: (nf < 0 ? '−' : '+') + '£', text: big(nf), series: cum, delta: (nf < 0 ? 'Net outflow' : 'Net inflow'), per: 'over ' + F.days + ' days' });
    var pos = posScope();
    chart('exposure-region', { title: function (s) { var e = s.series[0].values, l = s.series[1].values, i = e.indexOf(Math.max.apply(null, e)); return s.categories[i] + ' carries the most exposure, at ' + Math.round(e[i] / l[i] * 100) + '% of its limit'; },
      spec: function () { var regs = D.regions.filter(function (r) { return pos.some(function (p) { return p.region === r; }); });
        return { type: 'grouped-column', categories: regs, categoryLabel: 'Region', unit: '£m', caption: 'Exposure and limit by region, pounds millions (click a column for the positions)',
          series: [{ name: 'Exposure', values: regs.map(function (r) { return m1(sum(pos.filter(function (p) { return p.region === r; }), function (p) { return p.exposure; })); }) },
                   { name: 'Limit', values: regs.map(function (r) { return m1(sum(pos.filter(function (p) { return p.region === r; }), function (p) { return p.limit; })); }) }] }; },
      drill: function (cat) { location.href = href('risk', { region: cat }); } });
    chart('exposure-ccy', { title: function (s) { var t = sum(s.series[0].values) || 1; return s.categories[0] + ' is ' + Math.round(s.series[0].values[0] / t * 100) + '% of exposure by currency'; },
      spec: function () { var p = top(by(pos, function (x) { return x.ccy; }, function (x) { return m1(x.exposure); }), 5);
        return { type: 'donut', categories: p.map(function (x) { return x[0]; }), series: [{ name: 'Exposure', values: p.map(function (x) { return Math.round(x[1] * 10) / 10; }) }], unit: '£m', categoryLabel: 'Currency', caption: 'Exposure by currency, pounds millions (click a segment for the positions)' }; },
      view: shareView, drill: function (cat) { location.href = href('risk', cat === 'Other' ? {} : { ccy: cat }); } });
    var us0 = undrawnSeries();
    chart('liquidity-trend', { title: function () { return 'Available liquidity ' + (ls[ls.length - 1] >= ls[0] ? 'held up' : 'eased') + ' over ' + F.days + ' days, ending at ' + money(ls[ls.length - 1]) + ' (headroom ' + money(hs[hs.length - 1]) + ')'; },
      spec: function () { return { type: 'multiline', categories: dayCats(), categoryLabel: 'Day (day/month)', unit: '\u00a3m', caption: 'Available liquidity, cash and undrawn committed facilities by day, pounds millions',
        series: [{ name: 'Available liquidity', values: ls.map(m1) }, { name: 'Cash', values: cs.map(m1) }, { name: 'Undrawn committed facilities', values: us0.map(m1) }] }; } });
    var pend = D.payments.filter(function (p) { return inScope(p) && payStatus(p) === 'Pending approval'; }).sort(function (a, b) { return b.gbp - a.gbp; });
    var ap = $('[data-panel="approvals"]'); ap.innerHTML = '';
    ap.appendChild(heading('Pending approvals (' + pend.length + ', ' + money(sum(pend, function (p) { return p.gbp; })) + ')', 'View all', ['payments', {}]));
    ap.appendChild(list(pend.slice(0, 4).map(function (p) { return { title: p.beneficiary, avatar: p.ccy, avatarLabel: p.ccy, status: { kind: 'warn', text: 'Pending approval' }, desc: p.id + ' · ' + entName(p.entity) + ' · value ' + sdate(p.valueDate), amount: local(-p.amount, p.ccy),
      onOpen: function () { location.href = href('payments', { open: p.id }); } }; }), 'No payments are waiting for approval in this scope.'));
    var exc = excScope().filter(function (x) { return excStatus(x) === 'Open' && x.severity === 'Breach'; }).sort(function (a, b) { return b.util - a.util; });
    var ep = $('[data-panel="exceptions"]'); ep.innerHTML = '';
    ep.appendChild(heading('Material risk exceptions (' + exc.length + ' open breaches)', 'View all', ['risk', {}]));
    ep.appendChild(list(exc.slice(0, 4).map(function (x) { return { title: x.cpty, avatar: x.ccy, avatarLabel: x.ccy, status: { kind: 'err', text: 'Breach ' + pctS(x.util) }, desc: x.id + ' · ' + x.instrument + ' · ' + x.region, amount: money(x.exposure),
      onOpen: function () { location.href = href('risk', { open: x.id }); } }; }), 'No open limit breaches in this scope.'));
  };

  PAGES.accounts = function () {
    var cs = cashSeries(), tx = txScope(), acc = acctScope();
    var inS = DAYS().map(function (d) { return sum(tx.filter(function (t) { return t.date === d && t.gbp > 0; }), function (t) { return t.gbp; }); });
    var outS = DAYS().map(function (d) { return -sum(tx.filter(function (t) { return t.date === d && t.gbp < 0; }), function (t) { return t.gbp; }); });
    kpi('cash', { label: 'Cash across accounts', slug: 'accounts', unit: '£', text: big(cs[cs.length - 1]), series: cs });
    kpi('inflow', { label: 'Inflows', slug: 'accounts', unit: '+£', text: big(sum(inS)), series: inS, delta: tx.filter(function (t) { return t.gbp > 0; }).length + ' receipts', per: 'in ' + F.days + ' days' });
    kpi('outflow', { label: 'Outflows', slug: 'accounts', unit: '−£', text: big(sum(outS)), series: outS, delta: tx.filter(function (t) { return t.gbp < 0; }).length + ' payments', per: 'in ' + F.days + ' days' });
    kpi('accounts', { label: 'Transactions settled', slug: 'accounts', unit: '', text: String(tx.length), series: cumCount(tx, 'date'), count: true, per: 'across ' + acc.length + ' accounts' });
    var off = D.days.length - (+F.days), groups = [['GBP', ['GBP']], ['EUR', ['EUR']], ['USD', ['USD']], ['Asian currencies', ['SGD', 'HKD', 'INR', 'JPY']], ['AED', ['AED']]];
    chart('balances-ccy', { title: function (s) { var l = s.series.map(function (x) { return x.values[x.values.length - 1]; }), i = l.indexOf(Math.max.apply(null, l)); return s.series[i].name + ' holds the largest share of balances'; },
      spec: function () { var g = groups.filter(function (x) { return acc.some(function (a) { return x[1].indexOf(a.ccy) >= 0; }); });
        return { type: 'stacked-area', categories: dayCats(), categoryLabel: 'Day (day/month)', unit: '£m', caption: 'Balances by currency, pounds millions equivalent',
          series: g.map(function (x) { return { name: x[0], values: DAYS().map(function (d, i) { return m1(sum(acc.filter(function (a) { return x[1].indexOf(a.ccy) >= 0; }), function (a) { return a.series[off + i] / D.fx[a.ccy]; })); }) }; }) }; } });
    var BANDS = [[0, 5e4, 'Under £50k'], [5e4, 1e5, '£50–100k'], [1e5, 2.5e5, '£100–250k'], [2.5e5, 5e5, '£250–500k'], [5e5, 1e6, '£500k–1m'], [1e6, 2.5e6, '£1–2.5m'], [2.5e6, 5e6, '£2.5–5m'], [5e6, 1e12, '£5m and over']];
    chart('txn-size', { title: function (s) { var v = s.series[0].values, i = v.indexOf(Math.max.apply(null, v)); return 'Most transactions fall in the ' + s.categories[i] + ' band'; },
      spec: function () { return { type: 'histogram', categories: BANDS.map(function (b) { return b[2]; }), categoryLabel: 'Value band', caption: 'Transactions by value band, pounds equivalent',
        series: [{ name: 'transactions', values: BANDS.map(function (b) { return tx.filter(function (t) { var a = Math.abs(t.gbp); return a >= b[0] && a < b[1]; }).length; }) }] }; } });
    chart('balance-entity', { title: function (s) { return s.categories.length ? s.categories[0] + ' holds the most cash' : ''; },
      spec: function () { var p = scopeEnts().map(function (e) { return [e.name, m1(sum(acc.filter(function (a) { return a.entity === e.id; }), function (a) { return a.series[D.days.length - 1] / D.fx[a.ccy]; }))]; }).sort(function (a, b) { return b[1] - a[1]; });
        return { type: 'bar', categories: p.map(function (x) { return x[0]; }), series: [{ name: 'Balance', values: p.map(function (x) { return x[1]; }) }], unit: '£m', categoryLabel: 'Entity', caption: 'Closing balance by entity, pounds millions equivalent' }; } });
    gridSetup({ title: 'Transactions', noun: 'transactions', cols: { date: 'Date', payee: 'Counterparty', ref: 'Reference', type: 'Type', amount: 'Amount (GBP)' }, groups: ['Transaction detail', 'Value (GBP equivalent)'],
      rows: function () { return txScope().map(function (t) { return { date: t.date, payee: t.cpty, ref: t.ref, type: t.type, amount: t.gbp, rec: t }; }); },
      open: function (t) { var a = D.accounts.filter(function (x) { return x.id === t.account; })[0];
        openDrawer({ title: t.type + ' — ' + t.cpty, lead: local(t.amount, t.ccy) + ' (' + money(t.gbp) + ' at the illustrative rate GBP 1 = ' + t.ccy + ' ' + D.fx[t.ccy] + '), settled ' + fdate(t.date) + '.',
          rows: [['Transaction', t.id], ['Account', t.account + ' · ' + a.type + ' · ' + a.iban], ['Entity', entName(t.entity)], ['Region', t.region], ['Reference', t.ref], ['Status', 'Settled']],
          primary: { label: 'Export this record', run: function () { csv(t.id, ['id', 'date', 'account', 'entity', 'counterparty', 'type', 'reference', 'currency', 'amount', 'gbp'], [[t.id, t.date, t.account, t.entity, t.cpty, t.type, t.ref, t.ccy, t.amount, t.gbp]]); return true; } },
          secondary: { label: 'Close', run: function () { return true; } } }); } });
  };

  PAGES.liquidity = function () {
    var ls = liqSeries(), us = undrawnSeries(), hs = headSeries(), b = buffer(), fac = facScope();
    kpi('liquidity', { label: 'Available liquidity', slug: 'liquidity', unit: '£', text: big(ls[ls.length - 1]), series: ls });
    kpi('undrawn', { label: 'Undrawn committed facilities', slug: 'liquidity', unit: '£', text: big(us[us.length - 1]), series: us });
    kpi('headroom', { label: 'Funding headroom', slug: 'liquidity', unit: hs[hs.length - 1] < 0 ? '−£' : '£', text: big(hs[hs.length - 1]), series: hs, per: 'after ' + money(b) + ' buffer' });
    var cov = ls.map(function (v) { return v / b * 100; });
    kpi('buffer', { label: 'Buffer coverage', slug: 'liquidity', unit: '', text: Math.round(cov[cov.length - 1]) + '%', series: cov, per: 'liquidity ÷ minimum buffer' });
    var tx = txScope();
    chart('flows-combo', { title: function () { return 'Inflows against available liquidity, ' + scopeLabel(); },
      spec: function () { return { type: 'combo', categories: dayCats(), categoryLabel: 'Day (day/month)', caption: 'Daily inflows (columns, pounds millions) and available liquidity (line, pounds billions)',
        series: [{ name: 'Inflows (£m)', kind: 'column', unit: '£m', values: DAYS().map(function (d) { return m1(sum(tx.filter(function (t) { return t.date === d && t.gbp > 0; }), function (t) { return t.gbp; })); }) },
                 { name: 'Available liquidity (£bn)', kind: 'line', unit: '', values: ls.map(function (v) { return Math.round(v / 1e7) / 100; }) }] }; } });
    var LIMIT = { 'Committed RCF': 75, 'Term loan': 100, 'Commercial paper': 80, 'Overdraft': 60, 'Trade loan': 80 };
    chart('facility-bullet', { title: function (s) { var v = s.series[0].values, t = s.series[1].values, n = v.filter(function (x, i) { return x > t[i]; }).length; return n ? n + ' facilit' + (n === 1 ? 'y is' : 'ies are') + ' above policy utilisation' : 'Every facility is inside policy utilisation'; },
      spec: function () { var f = fac.slice(0, 6); return { type: 'bullet', categories: f.map(function (x) { return x.id.replace('FAC-', ''); }), categoryLabel: 'Facility', ranges: [50, 80, 100], caption: 'Facility utilisation against policy maximum, per cent',
        series: [{ name: 'Measure', values: f.map(function (x) { return Math.round(x.drawnGbp / x.limitGbp * 100); }) }, { name: 'Target', values: f.map(function (x) { return LIMIT[x.type]; }) }] }; } });
    chart('facility-mix', { title: function (s) { return s.categories[0] + ' provides most undrawn capacity'; },
      spec: function () { var p = top(by(fac, function (x) { return x.type; }, function (x) { return m1(x.limitGbp - x.drawnGbp); }), 5).filter(function (x) { return x[1] > 0; });
        return { type: 'donut', categories: p.map(function (x) { return x[0]; }), series: [{ name: 'Undrawn', values: p.map(function (x) { return Math.round(x[1] * 10) / 10; }) }], unit: '£m', categoryLabel: 'Facility type', caption: 'Undrawn capacity by facility type, pounds millions' }; }, view: shareView });
    gridSetup({ title: 'Facilities and maturities', noun: 'facilities', cols: { date: 'Maturity', payee: 'Lender', ref: 'Facility', type: 'Type', amount: 'Undrawn (GBP)' }, groups: ['Facility detail', 'Undrawn (GBP equivalent)'],
      rows: function () { return facScope().map(function (f) { return { date: f.maturity, payee: f.lender, ref: f.id, type: f.type, amount: f.limitGbp - f.drawnGbp, rec: f }; }); },
      open: function (f) { openDrawer({ title: f.name, lead: 'Drawn ' + money(f.drawnGbp) + ' of ' + money(f.limitGbp) + ' (' + Math.round(f.drawnGbp / f.limitGbp * 100) + '% utilised). Matures ' + fdate(f.maturity) + '.',
        rows: [['Facility', f.id], ['Lender', f.lender], ['Type', f.type + (f.committed ? ', committed' : ', uncommitted')], ['Currency limit', local(f.limit, f.ccy)], ['Drawn', local(f.drawn, f.ccy)], ['Entity', entName(f.entity)]],
        note: { label: 'Drawdown request note', help: 'Simulated: describe the amount and purpose. Nothing is sent to HSBC.' },
        primary: { label: 'Request drawdown', run: function (n) { if (!f.committed) { return 'This facility is uncommitted — speak to your relationship team instead.'; } if (n.length < 10) { return 'Add at least 10 characters describing amount and purpose.'; }
          var id = 'SR-' + (2000 + S.requests.length); S.requests.unshift({ id: id, date: D.asOf, type: 'Facility query', subject: 'Drawdown request: ' + f.name, status: 'Open', entity: f.entity, priority: 'High', note: n }); audit('Requested drawdown', f.id, n); save();
          toast('ok', 'Drawdown request ' + id + ' raised for ' + f.name + '. Track it under HSBC messages and service requests.'); return true; } },
        secondary: { label: 'Close', run: function () { return true; } } }); } });
  };

  function approvePayment(p, n, approve) {
    if (payStatus(p) !== 'Pending approval') { return 'This payment is no longer pending.'; }
    if (!approve && n.length < 10) { return 'A rejection needs an audit note of at least 10 characters.'; }
    if (approve && p.gbp > D.user.limitGbp) { return 'This payment (' + money(p.gbp) + ') exceeds your approval limit of ' + money(D.user.limitGbp) + '. Reject it with a note, or ask the board delegate.'; }
    if (approve && p.approvals === 2 && n.length < 10) { return 'Payments of £5m and over need an audit note (at least 10 characters) for the second approver.'; }
    var st = approve ? (p.approvals === 2 ? 'Approved (awaiting release)' : 'Approved') : 'Rejected';
    S.decisions[p.id] = { status: st, note: n, at: new Date().toISOString(), by: D.user.name }; audit(approve ? 'Approved' : 'Rejected', p.id, n); save();
    toast(approve ? 'ok' : 'warn', p.id + ' ' + st.toLowerCase() + ' — ' + local(p.amount, p.ccy) + ' to ' + p.beneficiary + '.');
    renderPage(); return true;
  }
  function openPayment(p) {
    var st = payStatus(p), d = S.decisions[p.id], pending = st === 'Pending approval';
    openDrawer({ title: 'Payment ' + p.id, lead: local(p.amount, p.ccy) + ' (' + money(p.gbp) + ') to ' + p.beneficiary + ', value date ' + fdate(p.valueDate) + '.',
      rows: [['Status', st], ['Debit entity', entName(p.entity)], ['Method', p.method], ['Purpose', p.purpose], ['Raised by', p.maker + ' on ' + fdate(p.date)], ['Approvals required', String(p.approvals)]].concat(d ? [['Your decision', d.status + ' — ' + (d.note || 'no note')]] : []),
      note: pending ? { label: 'Audit note', help: 'Required to reject, and for payments of £5m and over. Stored in this browser only.' } : null,
      primary: pending ? { label: 'Approve', run: function (n) { return approvePayment(p, n, true); } } : null,
      secondary: pending ? { label: 'Reject', run: function (n) { return approvePayment(p, n, false); } } : { label: 'Close', run: function () { return true; } } });
  }
  PAGES.payments = function () {
    var ps = payScope(), pend = ps.filter(function (p) { return payStatus(p) === 'Pending approval'; });
    var pv = DAYS().map(function (d) { return sum(pend.filter(function (p) { return p.date <= d; }), function (p) { return p.gbp; }); });
    kpi('pendingValue', { label: 'Awaiting approval', slug: 'payments', unit: '£', text: big(sum(pend, function (p) { return p.gbp; })), series: pv, per: 'raised in ' + F.days + ' days' });
    kpi('pendingCount', { label: 'Payments to approve', slug: 'payments', unit: '', text: String(pend.length), series: cumCount(pend, 'date'), count: true, per: pend.filter(function (p) { return p.gbp > D.user.limitGbp; }).length + ' above your limit' });
    var rel = ps.filter(function (p) { return payStatus(p) === 'Released'; });
    kpi('released', { label: 'Released', slug: 'payments', unit: '£', text: big(sum(rel, function (p) { return p.gbp; })), series: DAYS().map(function (d) { return sum(rel.filter(function (p) { return p.date <= d; }), function (p) { return p.gbp; }); }), delta: rel.length + ' payments' });
    var rej = ps.filter(function (p) { return payStatus(p) === 'Rejected'; });
    kpi('rejected', { label: 'Rejected', slug: 'payments', unit: '', text: String(rej.length), series: cumCount(rej, 'date'), count: true });
    chart('pending-ccy', { title: function (s) { return s.categories.length ? s.categories[s.series[0].values.indexOf(Math.max.apply(null, s.series[0].values))] + ' carries the largest pending value' : ''; },
      spec: function () { var p = by(pend, function (x) { return x.ccy; }, function (x) { return m1(x.gbp); }); return { type: 'column', categories: p.map(function (x) { return x[0]; }), series: [{ name: 'Pending', values: p.map(function (x) { return Math.round(x[1] * 10) / 10; }) }], unit: '£m', categoryLabel: 'Currency', caption: 'Value awaiting approval by payment currency, pounds millions (click a column to filter the list)' }; },
      view: sortView, drill: function (cat) { state.filters = state.filters.filter(function (f) { return f.key !== 'type'; }); state.filters.push({ key: null, term: 'Pending' }); renderChips(); render(); $('#dg').scrollIntoView({ block: 'start' }); toast('info', 'Showing pending payments; search ' + cat + ' beneficiaries in the list.'); } });
    chart('status-share', { title: function (s) { var t = sum(s.series[0].values) || 1; return Math.round(s.series[0].values[s.categories.indexOf('Released')] / t * 100 || 0) + '% of payments were released'; },
      spec: function () { var order = ['Released', 'Pending approval', 'Approved', 'Rejected', 'Approved (awaiting release)'], p = by(ps, payStatus).sort(function (a, b) { return order.indexOf(a[0]) - order.indexOf(b[0]); });
        return { type: 'pie', categories: p.map(function (x) { return x[0]; }), series: [{ name: 'Payments', values: p.map(function (x) { return x[1]; }) }], categoryLabel: 'Status', caption: 'Payments by status, count' }; },
      drill: function (cat) { state.filters = [{ key: 'type', term: cat }]; state.page = 1; renderChips(); render(); persistGrid(); $('#dg').scrollIntoView({ block: 'start' }); } });
    gridSetup({ title: 'Payments', noun: 'payments', cols: { date: 'Raised', payee: 'Beneficiary', ref: 'Payment', type: 'Status', amount: 'Amount (GBP)' }, groups: ['Payment detail', 'Value (GBP equivalent)'],
      rows: function () { return payScope().map(function (p) { return { date: p.date, payee: p.beneficiary, ref: p.id, type: payStatus(p), amount: -p.gbp, rec: p }; }); }, open: openPayment });
  };

  PAGES.fx = function () {
    var n = +F.days, usd = D.fxSeries['GBP/USD'].slice(-n), eur = D.fxSeries['GBP/EUR'].slice(-n), sgd = D.fxSeries['GBP/SGD'].slice(-n);
    kpi('gbpusd', { label: 'GBP/USD', slug: 'fx', unit: '', text: usd[usd.length - 1][3].toFixed(4), series: usd.map(function (r) { return r[3]; }), per: 'close, illustrative' });
    kpi('gbpeur', { label: 'GBP/EUR', slug: 'fx', unit: '', text: eur[eur.length - 1][3].toFixed(4), series: eur.map(function (r) { return r[3]; }), per: 'close, illustrative' });
    var ds = dealScope(), fwd = ds.filter(function (x) { return x.kind !== 'Spot' && x.status !== 'Settled'; });
    kpi('openFwd', { label: 'Open forwards and swaps', slug: 'fx', unit: '£', text: big(sum(fwd, function (x) { return x.gbp; })), series: DAYS().map(function (d) { return sum(fwd.filter(function (x) { return x.date <= d; }), function (x) { return x.gbp; }); }), delta: fwd.length + ' deals' });
    var fc = sum(acctScope().filter(function (a) { return a.ccy !== 'GBP'; }), function (a) { return a.series[D.days.length - 1] / D.fx[a.ccy]; });
    var hr = fc ? Math.min(100, sum(fwd, function (x) { return x.gbp; }) / fc * 100) : 0;
    var hs2 = DAYS().map(function (d) { return fc ? Math.min(100, sum(fwd.filter(function (x) { return x.date <= d; }), function (x) { return x.gbp; }) / fc * 100) : 0; });
    kpi('hedge', { label: 'Hedge ratio', slug: 'fx', unit: '', text: Math.round(hr) + '%', series: hs2, per: 'policy 50\u201375%, forwards \u00f7 foreign-currency cash' });
    chart('gbpusd-ohlc', { title: function () { var c = usd[usd.length - 1][3], o = usd[0][0]; return 'Sterling ' + (c >= o ? 'firmed' : 'eased') + ' against the dollar over ' + n + ' days, ' + o.toFixed(4) + ' to ' + c.toFixed(4); },
      spec: function () { return { type: 'candlestick', categories: dayCats(), categoryLabel: 'Day (day/month)', caption: 'GBP/USD daily open, high, low and close (illustrative)',
        series: ['Open', 'High', 'Low', 'Close'].map(function (nm, k) { return { name: nm, values: usd.map(function (r) { return r[k]; }) }; }) }; } });
    chart('fx-index', { title: function () { var c = eur[eur.length - 1][3], o = eur[0][3]; return 'Sterling ' + (c >= o ? 'rose' : 'fell') + ' ' + Math.abs((c / o - 1) * 100).toFixed(1) + '% against the euro, and ' + Math.abs((usd[usd.length - 1][3] / usd[0][3] - 1) * 100).toFixed(1) + '% against the dollar'; },
      spec: function () { function ix(a) { return a.map(function (r) { return Math.round(r[3] / a[0][3] * 10000) / 100; }); }
        return { type: 'multiline', categories: dayCats(), categoryLabel: 'Day (day/month)', caption: 'GBP/USD and GBP/EUR daily closes, units per pound (illustrative)', series: [{ name: 'GBP/USD', values: usd.map(function (r) { return r[3]; }) }, { name: 'GBP/EUR', values: eur.map(function (r) { return r[3]; }) }] }; } });
    chart('deals-kind', { title: function (s) { return 'Forwards carry the largest hedged notional'; },
      spec: function () { var k = ['Spot', 'Forward', 'Swap']; return { type: 'grouped-column', categories: k, categoryLabel: 'Deal type', unit: '£m', caption: 'Deal notional by type and direction, pounds millions',
        series: ['Buy', 'Sell'].map(function (sd) { return { name: sd, values: k.map(function (kk) { return m1(sum(ds.filter(function (x) { return x.kind === kk && x.side === sd; }), function (x) { return x.gbp; })); }) }; }) }; },
      drill: function (cat) { state.filters = [{ key: 'type', term: cat }]; state.page = 1; renderChips(); render(); persistGrid(); $('#dg').scrollIntoView({ block: 'start' }); } });
    gridSetup({ title: 'FX deals', noun: 'deals', cols: { date: 'Trade date', payee: 'Pair and side', ref: 'Deal', type: 'Type and status', amount: 'Notional (GBP)' }, groups: ['Deal detail', 'Notional (GBP equivalent)'],
      rows: function () { return dealScope().map(function (x) { return { date: x.date, payee: x.pair + ' ' + x.side.toLowerCase(), ref: x.id, type: x.kind + ' · ' + x.status, amount: x.gbp, rec: x }; }); },
      open: function (x) { openDrawer({ title: x.kind + ' ' + x.pair + ' — ' + x.id, lead: x.side + ' ' + x.base + ' ' + grp(x.notional, 0) + ' (' + money(x.gbp) + '), maturing ' + fdate(x.maturity) + '.',
        rows: [['Status', x.status], ['Entity', entName(x.entity)], ['Region', x.region], ['Trade date', fdate(x.date)], ['Maturity', fdate(x.maturity)]],
        primary: x.status === 'Open' ? { label: 'Mark as confirmed', run: function () { x.status = 'Confirmed'; audit('Confirmed deal', x.id); toast('ok', x.id + ' marked as confirmed (simulated).'); renderPage(); return true; } } : null,
        secondary: { label: 'Close', run: function () { return true; } } }); } });
  };

  function openPosition(p) {
    var ex = D.exceptions.filter(function (x) { return x.position === p.id; })[0], open = ex && excStatus(ex) === 'Open';
    openDrawer({ title: p.cpty + ' — ' + p.instrument, lead: 'Exposure ' + money(p.exposure) + ' against a limit of ' + money(p.limit) + ' (' + pctS(p.util) + ' used).',
      rows: [['Position', p.id], ['Entity', entName(p.entity)], ['Region', p.region], ['Currency', p.ccy], ['As of', fdate(p.date)]].concat(ex ? [['Exception', ex.id + ' · ' + ex.severity + ' · ' + excStatus(ex)]] : []).concat(ex && S.acks[ex.id] ? [['Acknowledged', S.acks[ex.id].by + ': ' + S.acks[ex.id].note]] : []),
      note: open ? { label: 'Acknowledgement and audit note', help: 'Say what you will do about it. Required, at least 15 characters.' } : null,
      primary: open ? { label: 'Acknowledge exception', run: function (n) { if (n.length < 15) { return 'An acknowledgement needs an audit note of at least 15 characters.'; }
        S.acks[ex.id] = { note: n, at: new Date().toISOString(), by: D.user.name }; audit('Acknowledged', ex.id, n); save(); toast('ok', ex.id + ' acknowledged with your note. It stays on the record as a ' + ex.severity.toLowerCase() + '.'); renderPage(); return true; } } : null,
      secondary: { label: 'Close', run: function () { return true; } } });
  }
  PAGES.risk = function () {
    var pos = posScope(), exc = excScope(), te = sum(pos, function (p) { return p.exposure; }), tl = sum(pos, function (p) { return p.limit; });
    var drift = DAYS().map(function (d, i, a) { return te * (0.94 + 0.06 * i / (a.length - 1 || 1)); });
    kpi('exposure', { label: 'Total exposure', slug: 'risk', unit: '£', text: big(te), series: drift, per: 'across ' + pos.length + ' positions' });
    kpi('utilisation', { label: 'Limit utilisation', slug: 'risk', unit: '', text: tl ? Math.round(te / tl * 100) + '%' : '0%', series: drift.map(function (v) { return tl ? v / tl * 100 : 0; }), per: 'of ' + money(tl) + ' limits' });
    var br = exc.filter(function (x) { return x.severity === 'Breach' && excStatus(x) === 'Open'; }), nl = exc.filter(function (x) { return x.severity !== 'Breach' && excStatus(x) === 'Open'; });
    kpi('breaches', { label: 'Open limit breaches', slug: 'risk', unit: '', text: String(br.length), series: cumCount(br, 'date'), count: true, per: exc.filter(function (x) { return S.acks[x.id]; }).length + ' acknowledged' });
    kpi('nearLimit', { label: 'Near limit (92\u2013100%)', slug: 'risk', unit: '', text: String(nl.length), series: cumCount(nl, 'date'), count: true, per: 'watch list' });
    chart('region-butterfly', { title: function (s) { return 'Exposure sits inside limits in ' + s.categories.filter(function (c, i) { return s.series[0].values[i] <= s.series[1].values[i]; }).length + ' of ' + s.categories.length + ' regions'; },
      spec: function () { var regs = D.regions.filter(function (r) { return pos.some(function (p) { return p.region === r; }); });
        return { type: 'butterfly-h', categories: regs, categoryLabel: 'Region', unit: '£m', caption: 'Exposure against limit by region, pounds millions (click a bar to filter by region)',
          series: [{ name: 'Exposure', values: regs.map(function (r) { return m1(sum(pos.filter(function (p) { return p.region === r; }), function (p) { return p.exposure; })); }) }, { name: 'Limit', values: regs.map(function (r) { return m1(sum(pos.filter(function (p) { return p.region === r; }), function (p) { return p.limit; })); }) }] }; },
      drill: function (cat) { F.region = cat; writeState(); location.reload(); } });
    chart('util-scatter', { title: function () { return pos.filter(function (p) { return p.util >= 92; }).length + ' of ' + pos.length + ' positions run at 92% of their limit or more'; },
      spec: function () { var p = pos.slice().sort(function (a, b) { return a.util - b.util; });
        return { type: 'scatter', categories: p.map(function (x) { return String(Math.round(x.util)); }), categoryLabel: 'Limit used (%)', caption: 'Exposure against limit utilisation per position, pounds millions and per cent', series: [{ name: 'Exposure (\u00a3m)', values: p.map(function (x) { return m1(x.exposure); }) }] }; } });
    chart('cpty-bar', { title: function (s) { return s.categories.length ? s.categories[0] + ' is the largest counterparty exposure' : ''; },
      spec: function () { var p = by(pos, function (x) { return x.cpty; }, function (x) { return m1(x.exposure); }).sort(function (a, b) { return b[1] - a[1]; });
        return { type: 'bar', categories: p.map(function (x) { return x[0]; }), series: [{ name: 'Exposure', values: p.map(function (x) { return Math.round(x[1] * 10) / 10; }) }], unit: '£m', categoryLabel: 'Counterparty', caption: 'Exposure by counterparty, pounds millions (click a bar to filter the positions)' }; },
      drill: function (cat) { state.filters = [{ key: 'payee', term: cat }]; state.page = 1; renderChips(); render(); persistGrid(); $('#dg').scrollIntoView({ block: 'start' }); } });
    var ccy = Q.get('ccy');
    gridSetup({ title: 'Positions and limits', noun: 'positions', cols: { date: 'As of', payee: 'Counterparty', ref: 'Position', type: 'Currency, instrument, use', amount: 'Exposure (GBP)' }, groups: ['Position detail', 'Exposure (GBP)'],
      presetFilter: ccy ? { key: 'type', term: ccy } : null,
      rows: function () { return posScope().map(function (p) { var ex = D.exceptions.filter(function (x) { return x.position === p.id; })[0];
        return { date: p.date, payee: p.cpty, ref: p.id, type: p.ccy + ' · ' + p.instrument + ' · ' + pctS(p.util) + (ex ? (excStatus(ex) === 'Open' ? ' · ' + ex.severity : ' · acknowledged') : ''), amount: p.exposure, rec: p }; }); },
      open: openPosition });
  };

  PAGES.trade = function () {
    var tf = tradeScope(), live = tf.filter(function (x) { return x.status !== 'Settled'; });
    var cum = function (rows) { return DAYS().map(function (d) { return sum(rows.filter(function (x) { return x.date <= d; }), function (x) { return x.gbp; }); }); };
    kpi('tfOutstanding', { label: 'Outstanding trade instruments', slug: 'trade', unit: '£', text: big(sum(live, function (x) { return x.gbp; })), series: cum(live), delta: live.length + ' live' });
    var lcs = live.filter(function (x) { return /LC/.test(x.type); });
    kpi('tfLc', { label: 'Letters of credit', slug: 'trade', unit: '£', text: big(sum(lcs, function (x) { return x.gbp; })), series: cum(lcs), delta: lcs.length + ' LCs' });
    var soon = new Date(D.asOf); soon.setDate(soon.getDate() + 30); var siso = soon.toISOString().slice(0, 10);
    var exp = live.filter(function (x) { return x.expiry <= siso; });
    var expS = DAYS().map(function (d) { var e2 = new Date(d); e2.setDate(e2.getDate() + 30); var i2 = e2.toISOString().slice(0, 10); return live.filter(function (x) { return x.expiry >= d && x.expiry <= i2; }).length; });
    kpi('tfExpiring', { label: 'Expiring within 30 days', slug: 'trade', unit: '', text: String(exp.length), series: expS, count: true, per: money(sum(exp, function (x) { return x.gbp; })) + ' to renew or let lapse' });
    var docs = live.filter(function (x) { return x.status === 'Documents presented'; });
    kpi('tfDocs', { label: 'Documents presented', slug: 'trade', unit: '', text: String(docs.length), series: cumCount(docs, 'date'), count: true, per: 'awaiting checking' });
    chart('import-export', { title: function (s) { var a = sum(s.series[0].values), b = sum(s.series[1].values); return (a >= b ? 'Import' : 'Export') + ' instruments carry more value across our regions'; },
      spec: function () { var regs = D.regions.filter(function (r) { return live.some(function (x) { return x.region === r; }); }), imp = /Import|collection|guarantee/i;
        return { type: 'butterfly-v', categories: regs, categoryLabel: 'Region', unit: '£m', caption: 'Import-side and export-side instruments by region, pounds millions',
          series: [{ name: 'Import side', values: regs.map(function (r) { return m1(sum(live.filter(function (x) { return x.region === r && imp.test(x.type); }), function (x) { return x.gbp; })); }) },
                   { name: 'Export side', values: regs.map(function (r) { return m1(sum(live.filter(function (x) { return x.region === r && !imp.test(x.type); }), function (x) { return x.gbp; })); }) }] }; } });
    chart('instrument-mix', { title: function (s) { return s.categories[0] + ' is the largest instrument by value'; },
      spec: function () { var p = top(by(live, function (x) { return x.type; }, function (x) { return m1(x.gbp); }), 5); return { type: 'donut', categories: p.map(function (x) { return x[0]; }), series: [{ name: 'Value', values: p.map(function (x) { return Math.round(x[1] * 10) / 10; }) }], unit: '£m', categoryLabel: 'Instrument', caption: 'Live instruments by type, pounds millions (click a segment to filter the list)' }; },
      view: shareView, drill: function (cat) { if (cat === 'Other') { return; } state.filters = [{ key: 'type', term: cat }]; state.page = 1; renderChips(); render(); persistGrid(); $('#dg').scrollIntoView({ block: 'start' }); } });
    gridSetup({ title: 'Trade instruments', noun: 'instruments', cols: { date: 'Issued', payee: 'Counterparty', ref: 'Instrument', type: 'Type and status', amount: 'Amount (GBP)' }, groups: ['Instrument detail', 'Value (GBP equivalent)'],
      rows: function () { return tradeScope().map(function (x) { return { date: x.date, payee: x.cpty, ref: x.id, type: x.type + ' · ' + (S.amend[x.id] ? 'Amendment requested' : x.status), amount: x.gbp, rec: x }; }); },
      open: function (x) { openDrawer({ title: x.type + ' ' + x.id, lead: local(x.amount, x.ccy) + ' (' + money(x.gbp) + ') with ' + x.cpty + ', expiring ' + fdate(x.expiry) + '.',
        rows: [['Status', S.amend[x.id] ? 'Amendment requested' : x.status], ['Entity', entName(x.entity)], ['Region', x.region], ['Issued', fdate(x.date)], ['Expiry', fdate(x.expiry)]],
        note: x.status !== 'Settled' ? { label: 'Amendment requested', help: 'Describe the change (for example a new expiry or amount). Required, at least 10 characters.' } : null,
        primary: x.status !== 'Settled' ? { label: 'Request amendment', run: function (n) { if (n.length < 10) { return 'Describe the amendment in at least 10 characters.'; }
          var id = 'SR-' + (2000 + S.requests.length); S.amend[x.id] = id; S.requests.unshift({ id: id, date: D.asOf, type: 'Trade instrument amendment', subject: 'Amend ' + x.id + ': ' + n.slice(0, 60), status: 'Open', entity: x.entity, priority: 'Normal', note: n });
          audit('Requested amendment', x.id, n); save(); toast('ok', 'Amendment request ' + id + ' raised for ' + x.id + '.'); renderPage(); return true; } } : null,
        secondary: { label: 'Close', run: function () { return true; } } }); } });
  };

  var REPORT_DATA = {
    Liquidity: function () { return [['date', 'cash_gbp', 'available_liquidity_gbp', 'headroom_gbp']].concat(DAYS().map(function (d, i) { return [d, Math.round(cashSeries()[i]), Math.round(liqSeries()[i]), Math.round(headSeries()[i])]; })); },
    Funding: function () { return [['facility', 'type', 'lender', 'limit_gbp', 'drawn_gbp', 'maturity']].concat(facScope().map(function (f) { return [f.id, f.type, f.lender, Math.round(f.limitGbp), Math.round(f.drawnGbp), f.maturity]; })); },
    Payments: function () { return [['id', 'date', 'entity', 'beneficiary', 'currency', 'amount', 'gbp', 'status']].concat(payScope().map(function (p) { return [p.id, p.date, p.entity, p.beneficiary, p.ccy, p.amount, p.gbp, payStatus(p)]; })); },
    Markets: function () { return [['id', 'date', 'pair', 'side', 'type', 'notional', 'gbp', 'status']].concat(dealScope().map(function (x) { return [x.id, x.date, x.pair, x.side, x.kind, x.notional, x.gbp, x.status]; })); },
    Risk: function () { return [['id', 'counterparty', 'region', 'currency', 'instrument', 'exposure_gbp', 'limit_gbp', 'utilisation_pct']].concat(posScope().map(function (p) { return [p.id, p.cpty, p.region, p.ccy, p.instrument, p.exposure, p.limit, p.util]; })); },
    Trade: function () { return [['id', 'type', 'counterparty', 'currency', 'amount', 'gbp', 'issued', 'expiry', 'status']].concat(tradeScope().map(function (x) { return [x.id, x.type, x.cpty, x.ccy, x.amount, x.gbp, x.date, x.expiry, x.status]; })); },
    Accounts: function () { return [['id', 'date', 'account', 'counterparty', 'type', 'currency', 'amount', 'gbp']].concat(txScope().map(function (t) { return [t.id, t.date, t.account, t.cpty, t.type, t.ccy, t.amount, t.gbp]; })); },
    Service: function () { return [['id', 'date', 'type', 'subject', 'status', 'entity']].concat(reqScope().map(function (r) { return [r.id, r.date, r.type, r.subject, r.status, r.entity]; })); }
  };
  function exportPage() {
    var map = { index: 'Liquidity', accounts: 'Accounts', liquidity: 'Funding', payments: 'Payments', fx: 'Markets', risk: 'Risk', trade: 'Trade', reports: 'Liquidity', messages: 'Service', settings: null };
    if (PAGE === 'settings') { csv('audit-trail', ['at', 'by', 'what', 'id', 'note'], S.audit.map(function (a) { return [a.at, a.by, a.what, a.id, a.note]; })); return; }
    var t = REPORT_DATA[map[PAGE]](); csv(PAGE, t[0], t.slice(1));
  }

  PAGES.reports = function () {
    var cs = cashSeries(), ls = liqSeries(), pos = posScope();
    kpi('cash', { label: 'Cash', slug: 'accounts', unit: '\u00a3', text: big(cs[cs.length - 1]), series: cs });
    kpi('liquidity', { label: 'Available liquidity', slug: 'liquidity', unit: '\u00a3', text: big(ls[ls.length - 1]), series: ls });
    var te = sum(pos, function (p) { return p.exposure; });
    kpi('exposure', { label: 'Total exposure', slug: 'risk', unit: '\u00a3', text: big(te), series: DAYS().map(function (d, i, a) { return te * (0.94 + 0.06 * i / (a.length - 1 || 1)); }), per: 'across ' + pos.length + ' positions' });
    [['sp1', 'Cash', cs], ['sp2', 'Available liquidity', ls], ['sp3', 'Funding headroom', headSeries()]].forEach(function (x) {
      chart(x[0], { title: x[1] + ' ' + money(x[2][x[2].length - 1]), spec: function () { return { type: 'spark', categories: dayCats(), categoryLabel: 'Day (day/month)', markers: x[0] === 'sp1', series: [{ name: x[1], values: x[2].map(m1) }], caption: x[1] + ' over ' + F.days + ' days, pounds millions' }; } });
    });
    kpi('reportsReady', { label: 'Reports ready', slug: 'reports', unit: '', text: String(D.reports.length), series: cumCount(D.reports, 'date'), count: true, per: 'generated to ' + fdate(D.asOf) });
    function five(a) { a = a.slice().sort(function (x, y) { return x - y; }); function q(p) { var i = (a.length - 1) * p, lo = Math.floor(i), hi = Math.ceil(i); return a[lo] + (a[hi] - a[lo]) * (i - lo); } return [a[0], q(0.25), q(0.5), q(0.75), a[a.length - 1]]; }
    chart('pay-boxplot', { title: 'Payment values vary most in Asia-Pacific and the Americas',
      spec: function () { var rows = payScope().concat(txScope().filter(function (t) { return t.gbp < 0; }).map(function (t) { return { region: t.region, gbp: -t.gbp }; }));
        var regs = D.regions.filter(function (r) { return rows.filter(function (x) { return x.region === r; }).length >= 3; });
        var f = regs.map(function (r) { return five(rows.filter(function (x) { return x.region === r; }).map(function (x) { return Math.round(x.gbp / 1e3); })); });
        return { type: 'boxplot', categories: regs, categoryLabel: 'Region', caption: 'Outgoing payment value by region, five-number summary, pounds thousands',
          series: ['Minimum', 'Q1', 'Median', 'Q3', 'Maximum'].map(function (n, k) { return { name: n, values: f.map(function (v) { return Math.round(v[k]); }) }; }) }; } });
    chart('reports-category', { title: function (s) { return 'Risk and liquidity reports make up most of the pack'; },
      spec: function () { var p = by(D.reports, function (r) { return r.category; }); return { type: 'column', categories: p.map(function (x) { return x[0]; }), series: [{ name: 'Reports', values: p.map(function (x) { return x[1]; }) }], categoryLabel: 'Category', caption: 'Scheduled reports by category, count' }; } });
    var pl = $('[data-panel="reportList"]'); pl.innerHTML = '';
    pl.appendChild(heading('Scheduled reports', null));
    pl.appendChild(list(D.reports.map(function (r) { return { title: r.name, avatar: r.category.slice(0, 2).toUpperCase(), avatarLabel: r.category, status: { kind: 'ok', text: 'Ready' }, desc: r.id + ' · ' + r.frequency + ' · generated ' + sdate(r.date) + ' · ' + r.format, amount: r.category,
      onOpen: function () { var rows = REPORT_DATA[r.category] ? REPORT_DATA[r.category]() : [['none']];
        openDrawer({ title: r.name, lead: 'A ' + r.frequency.toLowerCase() + ' ' + r.category.toLowerCase() + ' report for ' + scopeLabel() + '. ' + (rows.length - 1) + ' rows at the current filters.',
          rows: [['Report', r.id], ['Category', r.category], ['Frequency', r.frequency], ['Last generated', fdate(r.date)], ['Format', r.format]],
          primary: { label: 'Download CSV', run: function () { csv(r.id + '-' + r.name.toLowerCase().replace(/[^a-z]+/g, '-'), rows[0], rows.slice(1)); return true; } },
          secondary: { label: 'Close', run: function () { return true; } } }); } }; })));
  };

  /* ---- messages + service requests ---- */
  var formBuilt = false;
  function field(label, help, id) {
    var w = tpl('tpl-field'), f = w.querySelector('.field'), lab = f.querySelector('label'), inp = f.querySelector('input'), hp = f.querySelector('.help-text');
    lab.textContent = label; lab.setAttribute('for', id); inp.id = id; inp.setAttribute('placeholder', ''); hp.id = id + '-help'; hp.textContent = help; inp.setAttribute('aria-describedby', id + '-help');
    return w;
  }
  function fieldError(w, msg) {
    var f = w.querySelector('.field'), inp = f.querySelector('input'), old = f.querySelector('.err-msg'); if (old) { old.remove(); }
    f.classList.toggle('is-error', !!msg);
    if (msg) { inp.setAttribute('aria-invalid', 'true'); var m = document.createElement('div'); m.className = 'err-msg';
      m.innerHTML = '<span class="ic" aria-hidden="true"><svg class="icn" viewBox="0 0 18 18"><use href="#ic-error"/><\/svg></span><p id="' + inp.id + '-err">' + esc(msg) + '</p>';
      f.appendChild(m); inp.setAttribute('aria-describedby', inp.id + '-help ' + inp.id + '-err'); }
    else { inp.removeAttribute('aria-invalid'); inp.setAttribute('aria-describedby', inp.id + '-help'); }
  }
  function buildRequestForm(prefill) {
    var host = $('[data-panel="requestForm"]'); host.innerHTML = '';
    host.appendChild(heading('Raise a service request', null));
    var types = ['Payment investigation', 'User entitlement change', 'Account opening', 'Statement request', 'Facility query', 'Trade instrument amendment'].map(function (t) { return { label: t, value: t }; });
    var chosen = { type: prefill && prefill.type || '', entity: F.entity !== 'all' ? F.entity : D.user.entity };
    var stack = document.createElement('div'); stack.className = 'cn-layout-utilities';
    var inner = document.createElement('div'); inner.className = 'l-stack'; inner.setAttribute('data-gap', 'l'); stack.appendChild(inner);
    var ddType = dropdown('Request type', [{ label: 'Choose a type', value: '' }].concat(types), chosen.type, function (v) { chosen.type = v; });
    var ddEnt = dropdown('Entity', D.entities.map(function (e) { return { label: e.name, value: e.id }; }), chosen.entity, function (v) { chosen.entity = v; });
    var subj = field('Subject', 'A short summary HSBC will see first.', 'sr-subject');
    inner.appendChild(ddType); inner.appendChild(ddEnt); inner.appendChild(subj);
    noteWrap.__pinned = true; noteGroup.querySelector('label').textContent = 'Details'; $('#t1-help').textContent = 'What happened, and what you need. At least 20 characters.';
    noteTa.value = prefill && prefill.detail || ''; noteTa.dispatchEvent(new Event('input')); inner.appendChild(noteWrap);
    if (prefill && prefill.subject) { subj.querySelector('input').value = prefill.subject; }
    var submit = button('primary', 'Submit request', function () {
      var s = subj.querySelector('input').value.trim(), d = noteTa.value.trim(), ok = true;
      /* GAP: Dropdown ships no error state in this pack, so a missing type is flagged with aria-invalid
         on its trigger and named in the toast — no error markup is invented for it. */
      var trg = ddType.querySelector('.trigger');
      if (!chosen.type) { ok = false; trg.setAttribute('aria-invalid', 'true'); } else { trg.removeAttribute('aria-invalid'); }
      fieldError(subj, s.length < 5 ? 'Enter a subject of at least 5 characters.' : null); if (s.length < 5) { ok = false; }
      setNoteError(d.length < 20 ? 'Add at least 20 characters of detail.' : null); if (d.length < 20) { ok = false; }
      if (!ok) { toast('warn', (chosen.type ? '' : 'Choose a request type. ') + 'Check the highlighted fields.'); var first = host.querySelector('[aria-invalid="true"]'); if (first) { first.focus(); } return; }
      var id = 'SR-' + (2000 + S.requests.length);
      S.requests.unshift({ id: id, date: D.asOf, type: chosen.type, subject: s, status: 'Open', entity: chosen.entity, priority: 'Normal', note: d }); audit('Raised service request', id, s); save();
      toast('ok', 'Service request ' + id + ' raised (simulated). HSBC would normally reply within one working day.');
      subj.querySelector('input').value = ''; noteTa.value = ''; noteTa.dispatchEvent(new Event('input')); renderPage();
    });
    inner.appendChild(submit);
    host.appendChild(stack); formBuilt = true;
  }
  PAGES.messages = function () {
    var msgs = D.messages, reqs = reqScope();
    var unread = msgs.filter(function (m) { return !(S.read[m.id] || m.read); });
    kpi('unread', { label: 'Unread messages', slug: 'messages', unit: '', text: String(unread.length), series: cumCount(unread, 'date'), count: true, per: msgs.length + ' in inbox' });
    var open = reqs.filter(function (r) { return r.status === 'Open' || r.status === 'In progress'; });
    kpi('openReq', { label: 'Open service requests', slug: 'messages', unit: '', text: String(open.length), series: cumCount(open, 'date'), count: true, per: reqs.filter(function (r) { return r.priority === 'High' && r.status !== 'Closed'; }).length + ' high priority' });
    var aw = reqs.filter(function (r) { return r.status === 'Awaiting you'; }), cl = reqs.filter(function (r) { return r.status === 'Closed'; });
    kpi('awaitingYou', { label: 'Awaiting your reply', slug: 'messages', unit: '', text: String(aw.length), series: cumCount(aw, 'date'), count: true, per: 'reply to keep the service level' });
    kpi('closedReq', { label: 'Closed requests', slug: 'messages', unit: '', text: String(cl.length), series: cumCount(cl, 'date'), count: true, per: 'resolved' });
    chart('req-type', { title: function (s) { var v = s.series[0].values; return s.categories[v.indexOf(Math.max.apply(null, v))] + ' is our most common request'; },
      spec: function () { var p = by(reqs, function (r) { return r.type; }); return { type: 'column', categories: p.map(function (x) { return x[0]; }), series: [{ name: 'Requests', values: p.map(function (x) { return x[1]; }) }], categoryLabel: 'Type', caption: 'Service requests by type, count' }; } });
    chart('req-status', { title: function (s) { return s.series[0].values[s.categories.indexOf('Closed')] + ' of ' + sum(s.series[0].values) + ' requests are closed'; },
      spec: function () { var order = ['Open', 'In progress', 'Awaiting you', 'Closed'], p = by(reqs, function (r) { return r.status; }).sort(function (a, b) { return order.indexOf(a[0]) - order.indexOf(b[0]); });
        return { type: 'pie', categories: p.map(function (x) { return x[0]; }), series: [{ name: 'Requests', values: p.map(function (x) { return x[1]; }) }], categoryLabel: 'Status', caption: 'Service requests by status, count' }; } });
    var ib = $('[data-panel="inbox"]'); ib.innerHTML = '';
    ib.appendChild(heading('HSBC messages (' + unread.length + ' unread)', null));
    var showAll = !!S.prefs.inboxAll, shown = showAll ? msgs : msgs.slice(0, 6);
    ib.appendChild(list(shown.map(function (m) { var isRead = S.read[m.id] || m.read; return { title: m.subject, avatar: initials(m.from), avatarLabel: m.from, status: isRead ? null : { kind: 'warn', text: 'Unread' }, desc: m.from + ' · ' + sdate(m.date), amount: m.category,
      onOpen: function () { S.read[m.id] = true; save(); renderPage();
        openDrawer({ title: m.subject, lead: m.body, rows: [['From', m.from], ['Received', fdate(m.date)], ['Category', m.category], ['Reference', m.id]],
          primary: { label: 'Reply as a service request', run: function () { buildRequestForm({ subject: 'Re: ' + m.subject, detail: '', type: m.category === 'Trade' ? 'Trade instrument amendment' : m.category === 'Payments' ? 'Payment investigation' : '' }); setTimeout(function () { $('#sr-subject').focus(); }, 50); return true; } },
          secondary: { label: 'Close', run: function () { return true; } } }); } }; })));
    ib.appendChild(button('secondary', showAll ? 'Show the 6 latest' : 'Show all ' + msgs.length + ' messages', function () { S.prefs.inboxAll = !showAll; save(); renderPage(); }));
    if (!formBuilt) { buildRequestForm(); }
    var rl = $('[data-panel="requestList"]'); rl.innerHTML = '';
    rl.appendChild(heading('Your service requests (' + reqs.length + ')', null));
    var KIND = { 'Open': 'warn', 'In progress': 'warn', 'Awaiting you': 'err', 'Closed': 'ok' };
    rl.appendChild(list(reqs.map(function (r) { return { title: r.subject, avatar: r.id.slice(3), avatarLabel: r.id, status: { kind: KIND[r.status] || 'warn', text: r.status }, desc: r.id + ' · ' + r.type + ' · ' + entName(r.entity) + ' · ' + sdate(r.date), amount: r.priority,
      onOpen: function () { var closable = r.status !== 'Closed';
        openDrawer({ title: r.id + ' — ' + r.subject, lead: r.note || 'Raised ' + fdate(r.date) + ' for ' + entName(r.entity) + '.', rows: [['Type', r.type], ['Status', r.status], ['Priority', r.priority], ['Entity', entName(r.entity)]],
          primary: closable ? { label: 'Mark as resolved', run: function () { S.decisions[r.id] = { status: 'Closed', at: new Date().toISOString(), by: D.user.name }; audit('Closed request', r.id); save(); toast('ok', r.id + ' marked as resolved.'); renderPage(); return true; } } : null,
          secondary: { label: 'Close', run: function () { return true; } } }); } }; }), 'No service requests for this entity.'));
  };

  PAGES.settings = function () {
    var pr = $('[data-panel="prefs"]'); pr.innerHTML = '';
    pr.appendChild(heading('Appearance and default view', null));
    var st = document.createElement('div'); st.className = 'cn-layout-utilities'; var inner = document.createElement('div'); inner.className = 'l-stack'; inner.setAttribute('data-gap', 'l'); st.appendChild(inner);
    var p1 = document.createElement('p'); p1.className = 't-cm-label'; p1.textContent = 'Colour mode'; inner.appendChild(p1); inner.appendChild(themeSwitch());
    var dflt = S.prefs.defaults || { entity: 'all', region: 'all', days: '30' };
    inner.appendChild(dropdown('Default entity', [{ label: 'All entities', value: 'all' }].concat(D.entities.map(function (e) { return { label: e.name, value: e.id }; })), dflt.entity, function (v) { dflt.entity = v; S.prefs.defaults = dflt; save(); toast('ok', 'Default entity saved.'); }));
    inner.appendChild(dropdown('Default region', [{ label: 'All regions', value: 'all' }].concat(D.regions.map(function (r) { return { label: r, value: r }; })), dflt.region, function (v) { dflt.region = v; S.prefs.defaults = dflt; save(); toast('ok', 'Default region saved.'); }));
    inner.appendChild(dropdown('Default period', [{ label: 'Last 7 days', value: '7' }, { label: 'Last 14 days', value: '14' }, { label: 'Last 30 days', value: '30' }], dflt.days, function (v) { dflt.days = v; S.prefs.defaults = dflt; save(); toast('ok', 'Default period saved.'); }));
    inner.appendChild(button('secondary', 'Reset prototype data', function () {
      openDrawer({ title: 'Reset prototype data?', lead: 'This clears every decision, acknowledgement, service request, read marker, saved filter and grid setting stored in this browser. The illustrative data itself is unchanged.',
        rows: [['Decisions', String(Object.keys(S.decisions).length)], ['Acknowledgements', String(Object.keys(S.acks).length)], ['Requests raised here', String(S.requests.length)], ['Audit entries', String(S.audit.length)]],
        primary: { label: 'Reset', run: function () { try { localStorage.removeItem(STORE); } catch (e) { } S = load(); ['decisions', 'acks', 'read', 'prefs', 'grid', 'amend'].forEach(function (k) { S[k] = {}; }); S.requests = []; S.audit = []; toast('ok', 'Prototype data reset.'); renderPage(); return true; } },
        secondary: { label: 'Cancel', run: function () { return true; } } }); }));
    pr.appendChild(st);
    var nt = $('[data-panel="notify"]'); nt.innerHTML = '';
    nt.appendChild(heading('Notifications (simulated)', null));
    var st2 = document.createElement('div'); st2.className = 'cn-layout-utilities'; var in2 = document.createElement('div'); in2.className = 'l-stack'; in2.setAttribute('data-gap', 's'); st2.appendChild(in2);
    var N = S.prefs.notify || { approvals: true, breaches: true, weekly: false, expiry: false };
    [['approvals', 'A payment needs my approval'], ['breaches', 'A limit is breached'], ['daily', 'Daily cash position at 08:00'], ['weekly', 'Weekly liquidity summary'], ['expiry', 'A trade instrument expires within 30 days']].forEach(function (o) {
      var w = tpl('tpl-check'), inp = w.querySelector('input'), lab = w.querySelector('label'), id = 'nt-' + o[0];
      inp.id = id; lab.setAttribute('for', id); lab.lastChild.textContent = ' ' + o[1]; inp.checked = !!N[o[0]];
      inp.addEventListener('change', function () { N[o[0]] = inp.checked; S.prefs.notify = N; save(); toast('ok', (inp.checked ? 'On: ' : 'Off: ') + o[1].toLowerCase() + '.'); });
      in2.appendChild(w);
    });
    nt.appendChild(st2);
    chart('approval-limits', { title: function (s) { var v = s.series[0].values; return v[v.length - 1] ? v[v.length - 1] + ' pending payment' + (v[v.length - 1] === 1 ? ' is' : 's are') + ' above your ' + money(D.user.limitGbp) + ' limit' : 'Every pending payment is inside your approval limit'; },
      spec: function () { var pend = D.payments.filter(function (p) { return inScope(p) && payStatus(p) === 'Pending approval'; }), T = [[0, 1e6, 'Under £1m'], [1e6, 5e6, '£1–5m (one approver)'], [5e6, 25e6, '£5–25m (two approvers)'], [25e6, 1e15, 'Over £25m (above your limit)']];
        return { type: 'column', categories: T.map(function (t) { return t[2]; }), series: [{ name: 'Payments', values: T.map(function (t) { return pend.filter(function (p) { return p.gbp >= t[0] && p.gbp < t[1]; }).length; }) }], categoryLabel: 'Approval tier', caption: 'Pending payments by approval tier, count' }; } });
  };

  function renderPage() { PAGES[PAGE](); gridFeed(); decorateLinks(); }

  /* ---------------- boot ---------------- */
  buildNav(); buildCrumbs(); buildActions(); buildFilters();
  renderPage(); writeState();
  var openId = Q.get('open');
  if (openId && PAGE === 'payments') { var p = D.payments.filter(function (x) { return x.id === openId; })[0]; if (p) { openPayment(p); } }
  if (openId && PAGE === 'risk') { var ex = D.exceptions.filter(function (x) { return x.id === openId; })[0]; if (ex) { openPosition(D.positions.filter(function (x) { return x.id === ex.position; })[0]); } }
  if (Q.get('region') && PAGE === 'risk' && Q.get('region') !== 'all') { toast('info', 'Drilled through to ' + Q.get('region') + ' positions and limits.'); }
  if (Q.get('ccy') && PAGE === 'risk') { toast('info', 'Drilled through to ' + Q.get('ccy') + ' positions and limits.'); }
  if (Q.get('focus') === 'search' && $('#dgSearch')) { $('#dgSearch').focus(); }
  window.CEO = { F: F, S: S, renderPage: renderPage, openDrawer: openDrawer };
}());
