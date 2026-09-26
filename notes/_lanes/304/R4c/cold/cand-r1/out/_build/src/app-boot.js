/* CEO APP — BOOT: the shell, navigation, page header, the shared filter bar's contract, routing,
   theme and persistence. */
(function () {
  'use strict';
  var D = window.CEO_DATA, APP = window.CEO_APP, S = APP.state, V = APP.views;
  var NAV = APP.NAV = [['overview', 'Overview', 'ap-dashboard'], ['accounts', 'Accounts and transactions', 'ap-account'], ['liquidity', 'Liquidity and funding', 'ap-liquidity'],
    ['payments', 'Payments and approvals', 'ap-payments'], ['fx', 'FX and markets', 'ap-fx'], ['risk', 'Risk and limits', 'ap-risk'], ['trade', 'Trade finance', 'ap-trade'],
    ['reports', 'Reports', 'ap-reports'], ['messages', 'HSBC messages and service requests', 'ap-messages'], ['settings', 'Settings', 'ap-settings']];
  var GROUPS = [[null, ['overview']], ['Money', ['accounts', 'liquidity', 'payments', 'fx']], ['Risk and trade', ['risk', 'trade']], ['Insight and service', ['reports', 'messages']]];
  APP.navLabel = function (v) { for (var i = 0; i < NAV.length; i++) { if (NAV[i][0] === v) { return NAV[i][1]; } } return v; };
  APP.renderErrors = [];
  var shell, ph, restoring = false, bar = document.getElementById('ftbA'), FTB = window.CEO_FTB;
  var LOGO = '../pack/knowledge/assets/logos/';

  /* ------------------------------------------------------------------ shell */
  function buildNavList(nav, flat) {
    var body = nav.querySelector('.sn-body'), groups = [].slice.call(body.querySelectorAll('.sn-group'));
    var liProto = body.querySelector('a.sn-link[aria-current]') ? body.querySelector('a.sn-link[aria-current]').closest('li').cloneNode(true) : body.querySelector('a.sn-link').closest('li').cloneNode(true);
    liProto.querySelector('a').removeAttribute('aria-current');
    var labelled = groups.filter(function (g) { return g.querySelector('.sn-group-label'); })[0], plain = groups[0];
    groups.forEach(function (g) { g.remove(); });
    function link(v) { var li = liProto.cloneNode(true), a = li.querySelector('a'), n = NAV.filter(function (x) { return x[0] === v; })[0];
      a.setAttribute('href', '?view=' + v); a.setAttribute('data-view', v); a.querySelector('use').setAttribute('href', '#' + n[2]); a.querySelector('.sn-label').textContent = n[1]; return li; }
    if (flat) { var g = plain.cloneNode(true), ul = g.querySelector('ul'); ul.textContent = ''; NAV.forEach(function (n) { ul.appendChild(link(n[0])); }); body.appendChild(g); return; }
    GROUPS.forEach(function (gr, i) {
      var g = (gr[0] ? labelled : plain).cloneNode(true), ul = g.querySelector('ul'); ul.textContent = '';
      if (gr[0]) { var lab = g.querySelector('.sn-group-label'); lab.textContent = gr[0]; lab.id = 'ceo-nav-g' + i; ul.setAttribute('aria-labelledby', lab.id); }
      gr[1].forEach(function (v) { ul.appendChild(link(v)); }); body.appendChild(g); });
    var foot = nav.querySelector('.sn-foot ul'); if (foot) { var fl = foot.querySelector('li'); foot.textContent = ''; var s = link('settings'); foot.appendChild(s); void fl; }
  }
  function mountShell() {
    var sh = APP.tpl('shell');
    shell = sh;
    [].slice.call(sh.querySelectorAll('img.sh-mark')).forEach(function (img) { img.setAttribute('src', LOGO + img.getAttribute('src').split('/').pop()); });
    [].slice.call(sh.querySelectorAll('.sn-brand')).forEach(function (b) { b.textContent = 'Aldergrove Group'; });
    buildNavList(sh.querySelector('.sh-body > .sn'), false);
    buildNavList(sh.querySelector('.sh-sheet .sn'), true);
    var main = sh.querySelector('.sh-main'); main.textContent = '';
    /* page header — Page-header-lockup */
    var phEl = APP.tpl('phead'); ph = { el: phEl, eyebrow: phEl.querySelector('.eyebrow'), title: phEl.querySelector('.ph-title'), acts: phEl.querySelector('.ph-actions') };
    ph.title.id = 'ceo-title'; ph.title.setAttribute('tabindex', '-1');
    ph.btnT = ph.acts.querySelector('.btn.tertiary'); ph.btnP = ph.acts.querySelector('.btn.primary');
    ph.btnT.addEventListener('click', function () { APP.exportView('csv'); });
    ph.btnP.addEventListener('click', function () { if (ph.primary) { ph.primary(); } });
    main.appendChild(APP.scope('cn-page-header-lockup', phEl));
    main.appendChild(document.getElementById('ceo-ftb-scope'));
    var views = document.getElementById('ceo-views'); while (views.firstChild) { main.appendChild(views.firstChild); }
    sh.querySelector('#t-ac-r-grid').appendChild(document.getElementById('ceo-dg-scope'));
    /* app bar: theme switch beside the pack's search and profile buttons */
    var acts = sh.querySelector('.sh-actions');
    APP.themeSeg = APP.seg('Colour theme', [['light', 'Light'], ['dark', 'Dark']], S.theme, function (v) { APP.setTheme(v); });
    acts.insertBefore(APP.themeSeg, acts.firstChild);
    acts.querySelector('[aria-label="Search"]').addEventListener('click', function () { var q = document.getElementById('ftbQ'); q.focus(); q.select(); });
    acts.querySelector('[aria-label="Your profile"]').addEventListener('click', function () {
      APP.drawer.open({ title: 'Your profile', body: [APP.summary([['Name', 'Chief Executive Officer (illustrative)'], ['Organisation', 'Aldergrove Group'], ['Entities', String(D.entities.length) + ' across ' + D.regions.length + ' regions'],
        ['Approval authority', 'Payments of ' + APP.gbpc(D.policy.approvalThresholdGbp) + ' or more'], ['Acknowledges', 'Material risk exceptions'], ['Session', 'Simulated — no sign-in, no credentials']])],
        actions: [{ label: 'Open settings', onClick: function () { APP.drawer.close(true); APP.go('settings'); } }] }); });
    /* nav: collapse to the rail, and the phone-width sheet */
    /* The shell's own script (App-shell-side-nav.reference.html) binds by id at parse time, before this
       template clone exists, so its two mechanics are re-stated here as the snippet states them:
       the toggle flips data-nav on the shell AND Sidebar-nav's .is-rail on the column; the sheet opens
       show → two frames → focus in → only then inert, and closes returning focus to the menu button. */
    var tog = sh.querySelector('.sn-toggle[data-navtoggle]'), col = sh.querySelector('.sh-body > .sn');
    tog.addEventListener('click', function () { var rail = !col.classList.contains('is-rail');
      col.classList.toggle('is-rail', rail); sh.setAttribute('data-nav', rail ? 'rail' : 'expanded');
      tog.setAttribute('aria-expanded', String(!rail)); tog.setAttribute('aria-label', rail ? 'Expand navigation' : 'Collapse navigation');
      col.setAttribute('aria-label', rail ? 'Main, collapsed' : 'Main');
      tog.querySelector('use').setAttribute('href', rail ? '#ic-chevron-right' : '#ic-chevron-left'); });
    var menu = sh.querySelector('.sh-menu'), sheet = sh.querySelector('.sh-sheet'), scrim = sh.querySelector('.sh-scrim');
    var inertTargets = [].slice.call(sh.children).filter(function (c) { return c !== sheet && c !== scrim; });
    function sheetOpen(o) {
      if (o) { menu.setAttribute('aria-expanded', 'true');
        requestAnimationFrame(function () { requestAnimationFrame(function () { scrim.classList.add('open'); sheet.classList.add('open');
          requestAnimationFrame(function () { requestAnimationFrame(function () { var f = sheet.querySelector('a,button'); if (f) { f.focus(); } if (document.activeElement !== f) { sheet.focus(); }
            inertTargets.forEach(function (t) { t.inert = true; t.setAttribute('aria-hidden', 'true'); }); }); }); }); });
      } else { menu.setAttribute('aria-expanded', 'false'); scrim.classList.remove('open'); sheet.classList.remove('open');
        inertTargets.forEach(function (t) { t.inert = false; t.removeAttribute('aria-hidden'); }); menu.focus(); }
    }
    APP.sheetOpen = sheetOpen;
    menu.addEventListener('click', function () { sheetOpen(true); });
    scrim.addEventListener('click', function () { sheetOpen(false); });
    var cl = sheet.querySelector('[data-close]'); if (cl) { cl.addEventListener('click', function () { sheetOpen(false); }); }
    sheet.addEventListener('keydown', function (e) { if (e.key === 'Escape') { sheetOpen(false); } });
    sh.addEventListener('click', function (e) { var a = e.target.closest('a.sn-link[data-view]'); if (!a) { return; } e.preventDefault();
      if (sheet.classList.contains('open')) { sheetOpen(false); }
      APP.go(a.getAttribute('data-view'), null, true); });
    var crumbs = sh.querySelector('.sh-crumbs ol');
    ph.crumbs = crumbs; ph.crumbHome = crumbs.querySelector('li').cloneNode(true); ph.crumbCur = crumbs.lastElementChild.cloneNode(true);
    ph.crumbHome.querySelector('a').setAttribute('href', '?view=overview'); ph.crumbHome.querySelector('a').setAttribute('data-go', 'overview');
    sh.querySelector('.sh-legal .copy').textContent = '© HSBC Group 2026. Illustrative prototype — no live banking connection.';
    document.getElementById('ceo-root').appendChild(APP.scope('cn-app-shell-side-nav', sh));
    document.getElementById('ceo-root').addEventListener('click', function (e) { var a = e.target.closest('a[data-go]'); if (!a) { return; } e.preventDefault(); APP.go(a.getAttribute('data-go'), null, true); });
  }

  /* ------------------------------------------------------------------ the shared filter bar (its own contract: apollo:filter-change) */
  APP.setResult = function (count, total, noun) {
    var c = document.getElementById('ceo-consumer');
    c.setAttribute('data-apollo-result-count', String(count)); c.setAttribute('data-apollo-result-total', String(total));
    c.setAttribute('data-apollo-result-state', 'ok');
    var span = bar.querySelector('#ftbStatusA [data-when="no-filters filtered empty error"]');
    if (span) { var nums = span.querySelectorAll('.num'); nums[0].textContent = String(count); nums[1].textContent = String(total); span.lastChild.textContent = ' ' + noun + ' in view'; }
  };
  function labelFor(facet, value) { var o = bar.querySelector('#ftbAdd .opt[data-facet="' + facet + '"][data-value="' + value + '"]'); return o && typeof ddLabel === 'function' ? ddLabel(o) : value; }
  APP.setFilter = function (facet, value, keepOthers) {
    FTB.state.filters = FTB.state.filters.filter(function (f) { return keepOthers || f.facet !== facet; });
    if (!FTB.state.filters.some(function (f) { return f.facet === facet && f.value === value; })) { FTB.state.filters.push({ key: facet + ':' + value, facet: facet, value: value, label: labelFor(facet, value) }); }
    FTB.apply();
  };
  APP.setQuery = function (q) { var inp = document.getElementById('ftbQ'); inp.value = q; FTB.state.query = q; FTB.apply(); };
  APP.clearFilters = function () { var b = bar.querySelector('[data-ftb-clear]'); if (b) { b.click(); } };
  function setRangeUI(days) { var dd = bar.querySelector('#ftbRange'); [].slice.call(dd.querySelectorAll('.opt')).forEach(function (o) { var on = o.getAttribute('data-days') === String(days); o.setAttribute('aria-selected', String(on)); if (on) { dd.querySelector('.ddval').textContent = o.firstChild.textContent.trim(); } }); }
  function setSegUI(id, attr, v) { var seg = bar.querySelector('#' + id); [].slice.call(seg.querySelectorAll('button')).forEach(function (b) { b.setAttribute('aria-pressed', String(b.getAttribute(attr) === v)); }); if (typeof moveInd === 'function') { moveInd(seg); } }
  APP.setRecView = function (v) { FTB.state.view = v; setSegUI('ftbView', 'data-view', v); FTB.apply(); };
  bar.addEventListener('apollo:filter-change', function (e) {
    var d = e.detail;
    var before = JSON.stringify([S.q, S.filters, S.days]);
    S.q = d.query || ''; S.filters = (d.filters || []).map(function (f) { return { facet: f.facet, value: f.value }; });
    S.days = d.range && d.range.days ? d.range.days : S.days; S.recView = d.view === 'cards' ? 'cards' : 'table'; S.density = d.density === 'compact' ? 'compact' : 'full';
    if (JSON.stringify([S.q, S.filters, S.days]) !== before) { S.page = {}; }
    var dgd = document.querySelector('.dgden button[data-density="' + (S.density === 'compact' ? 'compact' : 'comfortable') + '"]');
    if (dgd && dgd.getAttribute('aria-pressed') !== 'true') { dgd.click(); }
    APP.save();
    if (!restoring) { APP.refresh(); }
  });
  bar.addEventListener('apollo:filter-export', function (e) { APP.exportView(e.detail.format); });
  function restoreBar() {
    restoring = true;
    var q = document.getElementById('ftbQ'); q.value = S.q; FTB.state.query = S.q;
    FTB.state.filters = S.filters.filter(function (f) { return bar.querySelector('#ftbAdd .opt[data-facet="' + f.facet + '"][data-value="' + f.value + '"]'); })
      .map(function (f) { return { key: f.facet + ':' + f.value, facet: f.facet, value: f.value, label: labelFor(f.facet, f.value) }; });
    var lab = { 7: 'Last 7 days', 30: 'Last 30 days', 90: 'Last 90 days' }[S.days] || 'Last 30 days';
    FTB.state.range = { preset: S.days + 'd', days: S.days, label: lab }; setRangeUI(S.days);
    FTB.state.view = S.recView; setSegUI('ftbView', 'data-view', S.recView);
    FTB.state.density = S.density; setSegUI('ftbDensity', 'data-density', S.density);
    FTB.apply();
    restoring = false;
  }

  /* ------------------------------------------------------------------ routing */
  var PRIMARY = {
    overview: ['Review approvals', function () { S.sort.payments = 'stOrder:asc'; APP.go('payments'); }],
    accounts: ['Download statements (CSV)', function () { APP.exportView('csv', 'accounts'); }],
    liquidity: ['Request a facility change', function () { APP.newRequest('Facility amendment'); }],
    payments: ['Review next approval', function () { var p = D.payments.filter(function (x) { return APP.passE(x) && APP.pay(x) === 'Awaiting your approval'; }).sort(function (a, b) { return b.gbp - a.gbp; })[0];
      if (p) { APP.openPayment(p); } else { APP.toast('info', 'Nothing is waiting for your approval in view.'); } }],
    fx: ['Request an FX quote', function () { APP.newRequest('FX quote request', null, 'Please quote a forward for '); }],
    risk: ['Acknowledge next exception', function () { var x = D.exceptions.filter(function (e) { return APP.pass(e) && APP.exc(e) === 'Open'; }).sort(function (a, b) { return (a.severity === 'Material' ? 0 : 1) - (b.severity === 'Material' ? 0 : 1); })[0];
      if (x) { APP.openException(x); } else { APP.toast('info', 'No open exceptions in view.'); } }],
    trade: ['Request an amendment', function () { APP.newRequest('Facility amendment', null, 'Please amend '); }],
    reports: ['Generate the board pack', function () { APP.generateReport(D.reports.filter(function (r) { return r.name === 'Board treasury pack'; })[0], 'csv'); }],
    messages: ['New service request', function () { APP.newRequest(); }],
    settings: ['Reset the prototype', function () { var b = document.querySelector('#t-st-f-data .btn'); if (b) { b.click(); } }]
  };
  function showView(v, focusTitle) {
    if (!NAV.some(function (n) { return n[0] === v; })) { v = 'overview'; }
    S.view = v;
    [].slice.call(document.querySelectorAll('.ceo-view')).forEach(function (s) { s.hidden = s.getAttribute('data-view') !== v; });
    [].slice.call(shell.querySelectorAll('a.sn-link[data-view]')).forEach(function (a) { if (a.getAttribute('data-view') === v) { a.setAttribute('aria-current', 'page'); } else { a.removeAttribute('aria-current'); } });
    ph.crumbs.textContent = ''; if (v !== 'overview') { ph.crumbs.appendChild(ph.crumbHome.cloneNode(true)); }
    var cur = ph.crumbCur.cloneNode(true); cur.querySelector('[aria-current]').textContent = APP.navLabel(v); ph.crumbs.appendChild(cur);
    if (v === 'overview') { var sep = cur.querySelector('.sep'); if (sep) { sep.remove(); } }
    ph.eyebrow.textContent = 'Aldergrove Group · CEO · illustrative data as at ' + D.asAtLabel;
    ph.title.textContent = APP.navLabel(v);
    ph.btnP.textContent = PRIMARY[v][0]; ph.primary = PRIMARY[v][1];
    ph.btnT.textContent = v === 'settings' ? 'Export settings' : 'Export';
    document.title = APP.navLabel(v) + ' — CEO international banking — Aldergrove Group';
    APP.save();
    APP.refresh();
    if (focusTitle) { ph.title.focus(); }
  }
  APP.go = function (v, filters, focusTitle) {
    var changed = v !== S.view;
    if (changed) { try { history.pushState(null, '', '?view=' + v); } catch (e) { /* ignore */ } }
    if (filters) { S.view = v; filters.forEach(function (f) { APP.setFilter(f.facet, f.value); }); }
    showView(v, focusTitle);
  };
  window.addEventListener('popstate', function () { APP.readURL(); showView(S.view); });
  APP.refresh = function () {
    var v = S.view;
    try { V[v](); } catch (err) { APP.renderErrors.push(v + ': ' + err.message); var al = document.getElementById('alerts-' + v);
      if (al) { al.textContent = ''; APP.alert(al, 'err', 'Part of this page could not be drawn.', err.message); } }
    APP.writeURL();
    requestAnimationFrame(function () { window.dispatchEvent(new Event('resize')); });
  };

  /* ------------------------------------------------------------------ theme */
  APP.setTheme = function (t) {
    S.theme = t === 'dark' ? 'dark' : 'light'; document.documentElement.setAttribute('data-theme', S.theme); APP.save();
    if (APP.themeSeg) { APP.segSet(APP.themeSeg, S.theme); }
    var st = document.getElementById('t-st-f-display'); if (st && st.__theme) { APP.segSet(st.__theme, S.theme); }
    APP.toast('info', (S.theme === 'dark' ? 'Dark' : 'Light') + ' theme on.');
  };

  /* ------------------------------------------------------------------ exports for the current view */
  APP.exportView = function (fmt, forced) {
    var v = forced || S.view, x = null;
    var P = { id: function (r) { return r.id; } };
    if (v === 'accounts') { x = { title: 'Accounts', cols: [{ label: 'Account', text: function (a) { return a.name; } }, { label: 'Currency', text: function (a) { return a.ccy; } }, { label: 'Balance', text: function (a) { return a.balance; } }, { label: 'GBP equivalent', text: function (a) { return a.gbp; } }], rows: D.accounts.filter(APP.pass) };
      if (!forced) { x = { title: 'Transactions', cols: APP.TXCOLS, rows: D.transactions.filter(function (t) { return APP.pass(t) && APP.inRange(t.date) && APP.matchQ(t, ['counterparty', 'ref', 'type', 'account', 'ccy']); }) }; } }
    var rec = function (id) { var host = null;
      [].slice.call(document.querySelectorAll('.ceo-view:not([hidden]) .stat-card')).forEach(function (h) { if (h.__rec && h.__rec.cfg.id === id) { host = h; } }); return host ? host.__rec : null; };
    var pick = { overview: 'payments', liquidity: 'facilities', payments: 'payments', fx: 'deals', risk: 'positions', trade: 'trade', reports: 'catalogue', messages: 'inbox' }[v];
    if (!x && v === 'overview') { var pend = D.payments.filter(function (p) { return APP.passE(p) && APP.pay(p) === 'Awaiting your approval'; });
      x = { title: 'Pending approvals', cols: [{ label: 'Payment', text: P.id }, { label: 'Beneficiary', text: function (p) { return p.beneficiary; } }, { label: 'Amount', text: function (p) { return p.amount; } }, { label: 'Currency', text: function (p) { return p.ccy; } }, { label: 'GBP equivalent', text: function (p) { return p.gbp; } }], rows: pend }; }
    if (!x && pick) { var r = rec(pick); if (r) { x = { title: r.cfg.title, rows: r.rows, cols: r.cfg.cols.map(function (c) { return { label: c.label, text: function (row) { var val = c.v(row); return val && val.nodeType ? val.textContent : val; } }; }) }; } }
    if (!x) { APP.toast('info', 'There is nothing to export on ' + APP.navLabel(v) + '.'); return; }
    APP.toast('ok', APP.exportRows(fmt || 'csv', x.title, x.cols, x.rows));
  };

  /* ------------------------------------------------------------------ boot — after DOMContentLoaded, so the dv engine blocks at the foot of the body have run */
  function boot() {
  var hadView = new URLSearchParams(location.search).has('view');
  APP.readURL();
  if (!hadView) { S.view = S.prefs.defaultView || 'overview'; }
  document.documentElement.setAttribute('data-theme', S.theme);
  mountShell();
  restoreBar();
  showView(S.view);
  var dgTbl = document.getElementById('tbl');
  if (dgTbl) {
    dgTbl.addEventListener('click', function (e) { var td = e.target.closest('tbody td'); if (!td || td.classList.contains('sel') || td.classList.contains('edit') || td.closest('.dg-empty')) { return; }
      var tr = td.closest('tr[data-id]'); if (tr) { APP.openTransaction(+tr.getAttribute('data-id')); } });
    dgTbl.addEventListener('keydown', function (e) { if (e.key !== 'Enter') { return; } var td = e.target.closest('tbody td'); if (!td || td.classList.contains('sel') || td.classList.contains('edit')) { return; }
      var tr = td.closest('tr[data-id]'); if (tr) { APP.openTransaction(+tr.getAttribute('data-id')); } });
  }
  if (typeof placeAll === 'function') { requestAnimationFrame(placeAll); }
  }
  if (document.readyState === 'loading') { document.addEventListener('DOMContentLoaded', boot); } else { boot(); }
}());
