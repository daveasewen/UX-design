/* ================= BUILD — every part is CLONED from a <template> that holds the snippet's own markup,
   byte-for-byte (receipted regions are marked APOLLO-SPLICE). This script only arranges clones and
   fills them from DATA; it never draws a component. ================= */
var UID = 0;
var REFS = ['for', 'aria-labelledby', 'aria-describedby', 'aria-controls', 'data-for', 'data-lockup-table', 'list'];
function T(id) {
  var t = document.getElementById(id);
  var node = t.content.firstElementChild.cloneNode(true);
  var sfx = '-' + (++UID), map = {};
  [node].concat([].slice.call(node.querySelectorAll('[id]'))).forEach(function (el) {
    if (!el.id) { return; } map[el.id] = el.id + sfx; el.id = el.id + sfx;
  });
  [node].concat([].slice.call(node.querySelectorAll('*'))).forEach(function (el) {
    REFS.forEach(function (a) {
      var v = el.getAttribute(a); if (!v) { return; }
      el.setAttribute(a, v.split(/\s+/).map(function (x) { return map[x] || x; }).join(' '));
    });
    var h = el.getAttribute('href');
    if (h && h.charAt(0) === '#' && map[h.slice(1)]) { el.setAttribute('href', '#' + map[h.slice(1)]); }
    if (el.tagName === 'IMG') { el.setAttribute('src', el.getAttribute('src').replace('../assets/', '../pack/knowledge/assets/')); }
  });
  return node;
}
function H(html) { var d = document.createElement('div'); d.innerHTML = html.trim(); return d.firstElementChild; }
function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
function txt(el, sel, v) { var n = sel ? el.querySelector(sel) : el; if (n) { n.textContent = v; } return n; }
function wrap(cls, child) { var d = document.createElement('div'); d.className = cls; if (child) { d.appendChild(child); } return d; }

/* ---------- money and dates ---------- */
var MINUS = '−';
function gbpShort(v) { var a = Math.abs(v), s = a >= 1e9 ? (a / 1e9).toFixed(2) + 'bn' : a >= 1e6 ? (a / 1e6).toFixed(1) + 'm' : a >= 1e3 ? (a / 1e3).toFixed(0) + 'k' : a.toFixed(0); return (v < 0 ? MINUS : '') + '£' + s; }
function num(v, dp) { return Math.abs(v).toLocaleString('en-GB', { minimumFractionDigits: dp == null ? 2 : dp, maximumFractionDigits: dp == null ? 2 : dp }); }
function gbp(v) { return (v < 0 ? MINUS : '') + '£' + num(v); }
function ccyAmt(v, c) { return (v < 0 ? MINUS : '') + c + ' ' + num(v); }
var MON = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
function dShort(iso) { var p = iso.split('-'); return +p[2] + ' ' + MON[+p[1] - 1]; }
function dLong(iso) { var p = iso.slice(0, 10).split('-'); return +p[2] + ' ' + MON[+p[1] - 1] + ' ' + p[0] + (iso.length > 10 ? ' ' + iso.slice(11) : ''); }
function entName(id) { for (var i = 0; i < DATA.ENTITIES.length; i++) { if (DATA.ENTITIES[i].id === id) { return DATA.ENTITIES[i].name; } } return id; }
function regName(id) { for (var i = 0; i < DATA.REGIONS.length; i++) { if (DATA.REGIONS[i].id === id) { return DATA.REGIONS[i].name; } } return id; }

/* ---------- the destinations ---------- */
var VIEWS = [
  { id: 'overview', label: 'Overview', icon: 'ic-nav-home', group: '' },
  { id: 'accounts', label: 'Accounts and transactions', icon: 'ic-nav-accounts', group: 'Money' },
  { id: 'liquidity', label: 'Liquidity and funding', icon: 'ic-nav-liquidity', group: 'Money' },
  { id: 'payments', label: 'Payments and approvals', icon: 'ic-nav-payments', group: 'Money' },
  { id: 'fx', label: 'FX and markets', icon: 'ic-nav-fx', group: 'Markets and risk' },
  { id: 'risk', label: 'Risk and limits', icon: 'ic-nav-risk', group: 'Markets and risk' },
  { id: 'trade', label: 'Trade finance', icon: 'ic-nav-trade', group: 'Markets and risk' },
  { id: 'reports', label: 'Reports', icon: 'ic-nav-reports', group: 'Service' },
  { id: 'messages', label: 'HSBC messages and service requests', icon: 'ic-nav-messages', group: 'Service' },
  { id: 'settings', label: 'Settings', icon: 'ic-nav-settings', group: 'foot' }];
var VIEW_INTRO = {
  overview: ['Group overview', 'Can we fund our plans, where are we exposed, and what needs a decision today.'],
  accounts: ['Accounts and transactions', 'Balances by entity and every movement in the period.'],
  liquidity: ['Liquidity and funding', 'Available liquidity, facility usage and drawdown requests.'],
  payments: ['Payments and approvals', 'Payments waiting for a decision, with approval and audit history.'],
  fx: ['FX and markets', 'Illustrative rates, recent moves and the group’s FX deals.'],
  risk: ['Risk and limits', 'Exposure by region and currency, limits and exceptions to acknowledge.'],
  trade: ['Trade finance', 'Letters of credit, guarantees and collections by expiry and status.'],
  reports: ['Reports', 'Run and export the standard group reports.'],
  messages: ['HSBC messages and service requests', 'Messages from your HSBC teams and the requests you have raised.'],
  settings: ['Settings', 'Appearance, notifications and saved state for this prototype.']
};

/* ---------- the shell (App-shell-side-nav, whole) ---------- */
var UI = {};
function navItem(tplLi, v) {
  var li = tplLi.cloneNode(true), a = li.querySelector('a');
  a.setAttribute('href', '#/' + v.id); a.setAttribute('data-nav', v.id); a.removeAttribute('aria-current');
  txt(li, '.sn-label', v.label);
  var use = li.querySelector('use'); if (use) { use.setAttribute('href', '#' + v.icon); }
  return li;
}
function buildNav(nav, grouped) {
  var body = nav.querySelector('.sn-body'), foot = nav.querySelector('.sn-foot ul');
  var tplLi = nav.querySelector('.sn-link .si').closest('li').cloneNode(true);
  var tplGroup = nav.querySelector('.sn-group-label') ? nav.querySelector('.sn-group-label').closest('.sn-group').cloneNode(true) : null;
  var plainGroup = body.querySelector('.sn-group').cloneNode(true);
  body.innerHTML = ''; foot.innerHTML = '';
  var groups = {};
  VIEWS.forEach(function (v) {
    if (v.group === 'foot') { foot.appendChild(navItem(tplLi, v)); return; }
    var key = grouped ? v.group : '';
    if (!groups[key]) {
      var g = (key && tplGroup ? tplGroup : plainGroup).cloneNode(true);
      var ul = g.querySelector('ul'); ul.innerHTML = '';
      var lab = g.querySelector('.sn-group-label');
      if (lab) { lab.textContent = key; lab.id = 'navg-' + (++UID); ul.setAttribute('aria-labelledby', lab.id); }
      groups[key] = ul; body.appendChild(g);
    }
    groups[key].appendChild(navItem(tplLi, v));
  });
}
function buildShell() {
  var shell = T('t-shell');
  shell.id = 'shell';
  var app = document.getElementById('app');
  var scope = wrap('cn-app-shell-side-nav'); scope.appendChild(shell); app.appendChild(scope);
  shell.querySelectorAll('[data-menu],[data-navtoggle],[data-scrim],[data-close]').forEach(function (el) {
    ['data-menu', 'data-navtoggle', 'data-scrim', 'data-close'].forEach(function (a) { if (el.hasAttribute(a)) { el.setAttribute(a, 'shell'); } });
  });
  shell.querySelectorAll('.sn-brand').forEach(function (b) { b.textContent = 'Global banking'; });
  var navs = shell.querySelectorAll('nav.sn');
  buildNav(navs[0], true); buildNav(navs[1], false);
  var acts = shell.querySelectorAll('.sh-actions button');
  acts[0].setAttribute('data-action', 'global-search'); acts[0].setAttribute('aria-label', 'Search transactions');
  acts[1].setAttribute('data-action', 'go-settings'); acts[1].setAttribute('aria-label', 'Profile and settings');
  var main = shell.querySelector('.sh-main'); main.innerHTML = ''; main.id = 'main';
  shell.querySelector('.sh-skip').setAttribute('href', '#main');
  UI.shell = shell; UI.main = main; UI.crumbs = shell.querySelector('.sh-crumbs ol');
  shell.querySelector('.sh-legal .copy').textContent = '© HSBC Group 2026. Prototype with placeholder data — no live banking connection.';
}

/* ---------- page header (Page-header-lockup) + theme switch (Segmented-control) ---------- */
function buildHeader() {
  var ph = T('t-ph');
  var scope = wrap('cn-page-header-lockup'); scope.appendChild(ph);
  var acts = ph.querySelector('.ph-actions'); acts.innerHTML = '';
  var seg = T('t-seg'); seg.setAttribute('aria-label', 'Theme');
  var bs = seg.querySelectorAll('button'); bs[2].remove();
  bs[0].textContent = 'Light'; bs[0].setAttribute('data-theme-set', 'light');
  bs[1].textContent = 'Dark'; bs[1].setAttribute('data-theme-set', 'dark');
  acts.appendChild(wrap('cn-segmented-control', seg));
  var exp = T('t-btn3'); exp.textContent = 'Export CSV'; exp.setAttribute('type', 'button'); exp.setAttribute('data-action', 'export-view'); acts.appendChild(wrap('cn-button', exp));
  UI.ph = ph; UI.themeSeg = seg;
  return scope;
}

/* ---------- the shared filter bar (Filter-toolbar-bar: three boxed dropdowns + chips + clear all) ---------- */
function ddOptions(ul, opts, current) {
  var tplOpt = ul.querySelector('.opt').cloneNode(true);
  ul.innerHTML = '';
  opts.forEach(function (o) {
    var li = tplOpt.cloneNode(true);
    ['data-days'].forEach(function (a) { li.removeAttribute(a); });
    li.setAttribute('data-value', o[0]); li.setAttribute('aria-selected', String(o[0] === current));
    li.firstChild.textContent = o[1] + ' ';
    ul.appendChild(li);
  });
}
function buildFilterBar() {
  var outer = T('t-ftb'), prim = outer.querySelector('.ftb-primary');
  var scope = wrap('cn-filter-toolbar-bar'); scope.appendChild(outer);
  outer.removeAttribute('data-apollo-filter-bar'); outer.removeAttribute('data-apollo-filter-target');
  outer.setAttribute('data-ftb-state', 'no-filters');
  outer.querySelector('form').setAttribute('aria-label', 'Filter every view');
  var range = prim.querySelector('.ftb-ctl.dd.boxed[id^="ftbRange"]');
  prim.querySelector('.ftb-search').remove(); prim.querySelector('[id^="ftbAdd"]').remove();
  var acts = prim.querySelector('.ftb-actions'); acts.remove();
  var make = function (key, label, opts) {
    var c = range.cloneNode(true), sfx = '-' + key;
    c.querySelectorAll('[id]').forEach(function (el) { el.id = el.id + sfx; });
    c.id = 'flt-' + key;
    var lab = c.querySelector('label'), trig = c.querySelector('.trigger'), menu = c.querySelector('.menu');
    lab.id = 'flt-' + key + '-l'; lab.setAttribute('for', 'flt-' + key + '-t'); lab.textContent = label;
    trig.id = 'flt-' + key + '-t'; trig.setAttribute('aria-controls', 'flt-' + key + '-m'); trig.setAttribute('aria-labelledby', lab.id + ' ' + trig.id);
    menu.id = 'flt-' + key + '-m'; menu.setAttribute('aria-labelledby', lab.id);
    trig.setAttribute('data-filter', key);
    ddOptions(menu, opts, opts[0][0]);
    txt(trig, '.ddval', opts[0][1]);
    return c;
  };
  var ents = [['all', 'All entities']].concat(DATA.ENTITIES.map(function (e) { return [e.id, e.name]; }));
  var regs = [['all', 'All regions']].concat(DATA.REGIONS.map(function (r) { return [r.id, r.name]; }));
  var days = [['30', 'Last 30 days'], ['14', 'Last 14 days'], ['7', 'Last 7 days']];
  prim.appendChild(make('entity', 'Entity', ents));
  prim.appendChild(make('region', 'Region', regs));
  prim.appendChild(make('days', 'Period', days));
  range.remove();
  var status = outer.querySelector('.ftb-status');
  status.innerHTML = '<span data-when="no-filters filtered empty error"><span class="num t-cm-figure-6" data-count>8</span> of <span class="num t-cm-figure-6">8</span> entities in view · GBP reporting · rates as at ' + dLong(DATA.ASAT) + '</span>';
  UI.ftb = outer; UI.ftbChips = outer.querySelector('.ftb-chips .row'); UI.ftbCount = status.querySelector('[data-count]');
  return scope;
}

/* ---------- bento (canon grammar) ---------- */
function bento(label, groups, sections) {
  /* sections: [[heading, [groups…]], …] — one wall per question, each under its own section heading */
  sections = sections || [[label, groups]];
  var ground = document.createElement('div'); ground.className = 'app-ground';
  var scope = document.createElement('div'); scope.className = 'cn-template-dashboard-bento';
  scope.innerHTML = '<div class="tpl-page"><div class="tpl-bento-stack"><div class="app-secs"></div></div></div>';
  var stack = scope.querySelector('.app-secs');
  sections.forEach(function (s) {
    var sec = document.createElement('div'); sec.className = 'app-sec';
    var h = wrap('cn-section-heading-lockup'); h.appendChild(sectionHead(s[0], '', '')); sec.appendChild(h);
    var wall = document.createElement('div'); wall.className = 'c-bento tpl-wall'; wall.setAttribute('data-bento-role', 'dashboard'); wall.setAttribute('aria-label', s[0]);
    var grid = document.createElement('div'); grid.className = 'c-bento__grid'; wall.appendChild(grid);
    s[1].forEach(function (g) { grid.appendChild(g); });
    sec.appendChild(wall); stack.appendChild(sec);
  });
  ground.appendChild(scope);
  return ground;
}
function group(role, label, span, scopes, tiles) {
  var s = document.createElement('section');
  s.className = 'c-bento__tile c-bento tpl-group tpl-group-' + role + (scopes ? ' ' + scopes : '');
  s.setAttribute('data-bento-role', 'dashboard'); s.setAttribute('data-c', String(span)); s.setAttribute('data-r', '1'); s.setAttribute('aria-label', label);
  var g = document.createElement('div'); g.className = 'c-bento__grid'; s.appendChild(g);
  tiles.forEach(function (t) { g.appendChild(t); });
  return s;
}
/* a chart module: Stat-card surface holding one chart figure, cloned whole from its snippet */
var FIGURES = {};
function chart(tpl, key, scopeCls, title, caption, span) {
  var fig = T(tpl);
  fig.setAttribute('data-chart', key);
  fig.setAttribute('data-lockup-title', title);
  txt(fig, '.dv-title', title); txt(fig, 'figcaption', caption);
  var cap = fig.querySelector('table.dv-table caption'); if (cap) { cap.textContent = caption; }
  var panel = fig.querySelector('.dv-tablepanel'); if (panel) { panel.setAttribute('aria-label', caption + ', data table'); }
  var tile = document.createElement('div');
  tile.className = 'c-bento__tile stat-card'; tile.setAttribute('data-c', String(span || 3)); tile.setAttribute('data-r', '1');
  tile.appendChild(wrap(scopeCls + ' app-fill', fig));
  FIGURES[key] = fig;
  return tile;
}
function kpi(key, label) {
  var t = T('t-kpi');
  t.classList.add('c-bento__tile'); t.setAttribute('data-c', '1'); t.setAttribute('data-r', '1');
  t.setAttribute('data-kpi', key); t.setAttribute('aria-label', label);
  txt(t, '.kpi-link', label);
  return t;
}
function sectionHead(title, linkText, href) {
  var r = T('t-sechead');
  var h = r.querySelector('h2'); h.textContent = title; h.id = 'sec-' + (++UID);
  var a = r.querySelector('a.arrow');
  if (linkText) { txt(a, '.lbl', linkText); a.setAttribute('href', href); } else { a.remove(); }
  return r;
}
function panelTile(key, title, linkText, href) {   /* a Stat-card surface with a section heading and a Summary list */
  var tile = document.createElement('div');
  tile.className = 'c-bento__tile stat-card'; tile.setAttribute('data-c', '3'); tile.setAttribute('data-r', '1');
  tile.setAttribute('data-panel', key);
  var inner = wrap('app-fill'); tile.appendChild(inner);
  var head = sectionHead(title, linkText, href);
  inner.appendChild(wrap('cn-section-heading-lockup', head));
  var sum = T('t-summary'); sum.innerHTML = ''; sum.setAttribute('aria-labelledby', head.querySelector('h2').id);
  inner.appendChild(wrap('cn-summary', sum));
  return tile;
}

/* ---------- a records section: heading + Data-grid (copied whole, then fitted to its columns) ---------- */
var GRIDS = {};
function gridSection(key, title, cols, opts) {
  opts = opts || {};
  var dg = T('t-grid');
  var scope = wrap('cn-data-grid');
  scope.appendChild(dg);
  dg.setAttribute('data-grid', key); dg.setAttribute('data-groups', 'off');
  txt(dg, '.dg-head .t-cm-section-label', title);
  var search = dg.querySelector('.dgsearch input');
  search.setAttribute('aria-label', 'Search ' + title.toLowerCase()); search.setAttribute('placeholder', opts.placeholder || 'Search ' + title.toLowerCase());
  search.setAttribute('data-grid-search', key);
  dg.querySelectorAll('.dgden button').forEach(function (b) { b.setAttribute('data-grid-density', key); });
  dg.querySelector('.dgs-clear').setAttribute('data-grid-clear', key);
  var table = dg.querySelector('table');
  table.removeAttribute('role'); table.removeAttribute('aria-rowcount'); table.removeAttribute('aria-describedby');
  var cg = table.querySelector('colgroup'); if (cg) { cg.remove(); }
  table.querySelector('tr.grp').remove();
  var headRow = table.querySelector('tr.cols');
  var thSel = headRow.querySelector('th.sel').cloneNode(true);
  var thTpl = headRow.querySelector('th[data-key="date"]').cloneNode(true);
  var thNum = headRow.querySelector('th[data-key="amount"]').cloneNode(true);
  headRow.innerHTML = '';
  var sa = thSel.querySelector('input'); sa.id = 'sa-' + key; sa.removeAttribute('tabindex'); sa.setAttribute('data-grid-selall', key); sa.setAttribute('aria-label', 'Select all rows on this page');
  thSel.querySelector('label').setAttribute('for', sa.id); headRow.appendChild(thSel);
  cols.forEach(function (c) {
    var th = (c.num ? thNum : thTpl).cloneNode(true);
    th.setAttribute('data-key', c.key); th.removeAttribute('aria-rowindex');
    ['.colf', '.colmenu', '.rsz'].forEach(function (s) { var n = th.querySelector(s); if (n) { n.remove(); } });
    var b = th.querySelector('button.sort'); b.removeAttribute('tabindex'); b.setAttribute('data-grid-sort', key);
    txt(b, '.lbl', c.label);
    if (c.nosort) { th.removeAttribute('aria-sort'); b.setAttribute('disabled', ''); b.querySelectorAll('.ic').forEach(function (i) { i.remove(); }); }
    headRow.appendChild(th);
  });
  headRow.removeAttribute('aria-rowindex');
  var tb = table.querySelector('tbody'); tb.id = 'tb-' + key; tb.setAttribute('data-grid-body', key);
  var pp = dg.querySelector('.dg-pp select'); pp.setAttribute('data-grid-pp', key);
  pp.innerHTML = '<option value="8">8</option><option value="12">12</option><option value="24">24</option>';
  dg.querySelector('.dgpg ul').setAttribute('data-grid-pager', key);
  var hint = scope.parentNode ? null : null;
  var section = document.createElement('section');
  section.className = 'app-records'; section.setAttribute('aria-label', title);
  section.appendChild(scope);
  GRIDS[key] = { el: dg, cols: cols, opts: opts, title: title, selCell: thSel.querySelector('.cbx').cloneNode(true), sel: {} };
  return section;
}

/* ---------- views ---------- */
function viewShell(id) {
  var s = document.createElement('section'); s.className = 'app-view l-stack'; s.setAttribute('data-gap', 'l');
  s.setAttribute('data-view', id); s.setAttribute('aria-label', VIEW_INTRO[id][0]); s.hidden = true;
  return s;
}
function buildOverview() {
  var v = viewShell('overview');
  var lead = group('lead', 'Financial resilience — can we fund our plans?', 6, 'cn-kpi-tile', [
    kpi('cash', 'Cash'), kpi('liquidity', 'Available liquidity'), kpi('headroom', 'Funding headroom'), kpi('coverage', 'Liquidity coverage')]);
  var ev1 = group('evidence', 'Liquidity and funding, this period', 6, '', [
    chart('t-area', 'ov-cash-region', 'cn-chart-stacked-area', 'Cash by region', 'Cash balance by region by day, pounds millions', 3),
    chart('t-combo', 'ov-facilities', 'cn-chart-combo', 'Facilities: drawn and utilisation', 'Drawn amount and utilisation by facility', 3)]);
  var ev2 = group('evidence', 'Risk outlook — where are we exposed?', 6, '', [
    chart('t-hbar', 'ov-exposure-region', 'cn-chart-bar', 'Exposure by region — select a bar to see its positions and limits', 'Counterparty exposure by region, pounds millions', 6),
    chart('t-donut', 'ov-exposure-ccy', 'cn-chart-donut', 'Exposure by currency', 'Counterparty exposure by currency, pounds millions', 3),
    chart('t-pie', 'ov-exposure-kind', 'cn-chart-pie', 'Exposure by product', 'Counterparty exposure by product type, pounds millions', 3)]);
  var ctx = group('context', 'Decisions — what needs my attention?', 6, '', [
    panelTile('approvals', 'Pending approvals', 'All payments', '#/payments'),
    panelTile('exceptions', 'Material risk exceptions', 'All exceptions', '#/risk')]);
  v.appendChild(bento('Group overview', null, [['Financial resilience — can we fund our plans?', [lead, ev1]], ['Risk outlook — where are we exposed?', [ev2]], ['Decisions — what needs my attention?', [ctx]]]));
  return v;
}
function chartBento(label, tiles, role) { return bento(label, [group(role || 'evidence', label, 6, '', tiles)]); }
function buildAccounts() {
  var v = viewShell('accounts');
  v.appendChild(chartBento('Balances and flows', [
    chart('t-col', 'ac-balance-entity', 'cn-chart-bar', 'Cash by entity', 'Cash balance by entity today, pounds millions', 3),
    chart('t-fly', 'ac-flows', 'cn-chart-butterfly-h', 'Money in and out by entity', 'Receipts and payments by entity in the period, pounds millions', 3),
    chart('t-line', 'ac-netflow', 'cn-chart-line', 'Net cash flow', 'Net cash flow by day, pounds millions', 6)]));
  v.appendChild(gridSection('accounts', 'Accounts', [
    { key: 'name', label: 'Account' }, { key: 'entity', label: 'Entity' }, { key: 'ccy', label: 'Currency' },
    { key: 'local', label: 'Balance (local)', num: true }, { key: 'gbp', label: 'Balance (GBP)', num: true }], { placeholder: 'Search accounts' }));
  v.appendChild(gridSection('txns', 'Transactions', [
    { key: 'date', label: 'Date' }, { key: 'counterparty', label: 'Counterparty' }, { key: 'type', label: 'Type' },
    { key: 'entity', label: 'Entity' }, { key: 'status', label: 'Status' }, { key: 'gbp', label: 'Amount (GBP)', num: true }], { placeholder: 'Search counterparty, type or reference' }));
  return v;
}
function buildLiquidity() {
  var v = viewShell('liquidity');
  v.appendChild(chartBento('Liquidity and facilities', [
    chart('t-multi', 'lq-trend', 'cn-chart-line', 'Liquidity over the period', 'Cash, available liquidity and funding headroom by day, pounds millions', 6),
    chart('t-bullet', 'lq-bullet', 'cn-chart-bullet', 'Facility utilisation against the 75% policy line', 'Utilisation by facility against target, per cent', 3),
    chart('t-grouped', 'lq-limits', 'cn-chart-bar', 'Facility limit and drawn amount', 'Limit and drawn amount by facility, pounds millions', 3)]));
  v.appendChild(gridSection('facilities', 'Facilities', [
    { key: 'name', label: 'Facility' }, { key: 'entity', label: 'Borrower' }, { key: 'kind', label: 'Type' }, { key: 'maturity', label: 'Maturity' },
    { key: 'limitGbp', label: 'Limit (GBP)', num: true }, { key: 'undrawn', label: 'Undrawn (GBP)', num: true }], { placeholder: 'Search facilities' }));
  return v;
}
function buildPayments() {
  var v = viewShell('payments');
  v.appendChild(chartBento('Payments in the queue', [
    chart('t-pie', 'pm-status', 'cn-chart-pie', 'Payment value by status', 'Payment value by status, pounds millions', 3),
    chart('t-donut', 'pm-ccy', 'cn-chart-donut', 'Awaiting approval by currency', 'Value awaiting approval by payment currency, pounds millions', 3),
    chart('t-col', 'pm-valuedate', 'cn-chart-bar', 'Awaiting approval by value date', 'Value awaiting approval by value date, pounds millions', 6)]));
  v.appendChild(gridSection('payments', 'Payments', [
    { key: 'id', label: 'Payment' }, { key: 'beneficiary', label: 'Beneficiary' }, { key: 'entity', label: 'Entity' }, { key: 'valueDate', label: 'Value date' },
    { key: 'status', label: 'Status' }, { key: 'gbp', label: 'Amount (GBP)', num: true }], { placeholder: 'Search payment, beneficiary or rail' }));
  return v;
}
function buildFx() {
  var v = viewShell('fx');
  var tiles = [
    chart('t-candle', 'fx-candle', 'cn-chart-candlestick', 'GBP/USD daily range', 'GBP/USD open, high, low and close by day, illustrative', 6),
    chart('t-multi', 'fx-index', 'cn-chart-line', 'Sterling against three currencies', 'Sterling rate indexed to 100 at the start of the period', 6)];
  v.appendChild(chartBento('Rates', tiles));
  v.appendChild(gridSection('rates', 'Illustrative rates', [
    { key: 'pair', label: 'Pair' }, { key: 'rate', label: 'Rate', num: true }, { key: 'chg', label: 'Change in period', num: true }], { placeholder: 'Search pairs' }));
  v.appendChild(gridSection('deals', 'FX deals', [
    { key: 'id', label: 'Deal' }, { key: 'pair', label: 'Pair' }, { key: 'side', label: 'Side' }, { key: 'kind', label: 'Type' },
    { key: 'maturity', label: 'Maturity' }, { key: 'notional', label: 'Notional (GBP)', num: true }, { key: 'mtm', label: 'Valuation (GBP)', num: true }], { placeholder: 'Search deal, pair or entity' }));
  return v;
}
function buildRisk() {
  var v = viewShell('risk');
  var limTile = document.createElement('div');
  limTile.className = 'c-bento__tile stat-card'; limTile.setAttribute('data-c', '6'); limTile.setAttribute('data-r', '1');
  var limInner = wrap('app-fill'); limTile.appendChild(limInner);
  limInner.appendChild(wrap('cn-section-heading-lockup', sectionHead('Limits in view', '', '')));
  var limList = document.createElement('div'); limList.className = 'l-grid'; limList.setAttribute('data-gap', 'l'); limInner.appendChild(wrap('cn-limits-meter', limList));
  UI.limits = limList;
  v.appendChild(chartBento('Exposure', [
    chart('t-hbar', 'rk-region', 'cn-chart-bar', 'Exposure by region — select a bar to filter positions', 'Counterparty exposure by region, pounds millions', 3),
    chart('t-scatter', 'rk-scatter', 'cn-chart-scatter', 'Exposure against limit utilisation', 'Position exposure in pounds millions against limit utilisation per cent', 3),
    limTile]));
  v.appendChild(gridSection('exceptions', 'Limit exceptions', [
    { key: 'id', label: 'Exception' }, { key: 'title', label: 'Exception type' }, { key: 'entity', label: 'Entity' }, { key: 'severity', label: 'Severity' },
    { key: 'status', label: 'Status' }, { key: 'amount', label: 'Excess (GBP)', num: true }], { placeholder: 'Search exceptions' }));
  v.appendChild(gridSection('positions', 'Positions and limits', [
    { key: 'id', label: 'Position' }, { key: 'counterparty', label: 'Counterparty' }, { key: 'entity', label: 'Entity' }, { key: 'ccy', label: 'Currency' },
    { key: 'kind', label: 'Type' }, { key: 'exposure', label: 'Exposure (GBP)', num: true }, { key: 'util', label: 'Limit used', num: true }], { placeholder: 'Search positions' }));
  return v;
}
function buildTrade() {
  var v = viewShell('trade');
  v.appendChild(chartBento('Trade book', [
    chart('t-hist', 'tf-expiry', 'cn-chart-histogram', 'Instruments by days to expiry', 'Number of instruments by days to expiry', 3),
    chart('t-box', 'tf-box', 'cn-chart-boxplot', 'Instrument size by type', 'Instrument value by type, five-number summary, pounds millions', 3)]));
  v.appendChild(gridSection('trade', 'Trade instruments', [
    { key: 'id', label: 'Reference' }, { key: 'kind', label: 'Instrument' }, { key: 'counterparty', label: 'Counterparty' }, { key: 'expiry', label: 'Expiry' },
    { key: 'status', label: 'Status' }, { key: 'gbp', label: 'Value (GBP)', num: true }], { placeholder: 'Search reference, instrument or counterparty' }));
  return v;
}
function buildReports() {
  var v = viewShell('reports');
  v.appendChild(bento('Report signals', null, [['Report signals', [
    group('evidence', 'Daily outflows by region', 6, '', [chart('t-box', 'rp-outflows', 'cn-chart-boxplot', 'Daily outflows by region', 'Daily payments out by region in the period, five-number summary, pounds millions', 6)]),
    group('context', 'Group cash at a glance', 6, '', [chart('t-spark', 'rp-spark', 'cn-chart-sparkline', 'Group cash, this period', 'Group cash by day, pounds millions', 6)])]]]));
  v.appendChild(gridSection('reports', 'Report catalogue', [
    { key: 'name', label: 'Report' }, { key: 'area', label: 'Area' }, { key: 'freq', label: 'Frequency' }, { key: 'lastRun', label: 'Last run' },
    { key: 'rows', label: 'Rows in scope', num: true }], { placeholder: 'Search reports' }));
  return v;
}
function buildMessages() {
  var v = viewShell('messages');
  v.appendChild(chartBento('Service at a glance', [
    chart('t-hbar', 'ms-requests', 'cn-chart-bar', 'Service requests by status', 'Number of service requests by status', 6),
    (function () {
      var tile = document.createElement('div');
      tile.className = 'c-bento__tile stat-card'; tile.setAttribute('data-c', '6'); tile.setAttribute('data-r', '1');
      var inner = wrap('app-fill'); tile.appendChild(inner);
      inner.appendChild(wrap('cn-section-heading-lockup', sectionHead('Messages from HSBC', '', '')));
      var list = T('t-list'); list.innerHTML = ''; list.setAttribute('data-inbox', ''); UI.inbox = list; UI.inboxLi = document.getElementById('t-list').content.querySelector('li').cloneNode(true);
      inner.appendChild(wrap('cn-list-items', list));
      return tile;
    }())]));
  var reqs = gridSection('requests', 'Service requests', [
    { key: 'id', label: 'Request' }, { key: 'subject', label: 'Subject' }, { key: 'category', label: 'Category' }, { key: 'opened', label: 'Opened' },
    { key: 'priority', label: 'Priority' }, { key: 'status', label: 'Status' }], { placeholder: 'Search requests' });
  var newBtn = T('t-btn'); newBtn.textContent = 'New service request'; newBtn.setAttribute('type', 'button'); newBtn.setAttribute('data-action', 'new-request');
  var bar = document.createElement('div'); bar.className = 'l-row'; bar.setAttribute('data-justify', 'end'); bar.appendChild(wrap('cn-button', newBtn));
  reqs.insertBefore(bar, reqs.firstChild);
  v.appendChild(reqs);
  return v;
}
function buildSettings() {
  var v = viewShell('settings');
  v.appendChild(chartBento('Security', [chart('t-spark', 'st-signins', 'cn-chart-sparkline', 'Your sign-ins, this period', 'Sign-ins to this prototype by day', 6)], 'context'));
  var sec = document.createElement('section'); sec.className = 'app-settings l-stack'; sec.setAttribute('data-gap', 'l'); sec.setAttribute('aria-label', 'Preferences');
  var put = function (el, scope) { sec.appendChild(wrap(scope, el)); return el; };
  put(sectionHead('Appearance', '', ''), 'cn-section-heading-lockup');
  var seg = T('t-seg'); seg.setAttribute('aria-label', 'Theme, in settings'); var bs = seg.querySelectorAll('button'); bs[2].remove();
  bs[0].textContent = 'Light'; bs[0].setAttribute('data-theme-set', 'light'); bs[1].textContent = 'Dark'; bs[1].setAttribute('data-theme-set', 'dark');
  put(seg, 'cn-segmented-control'); UI.themeSeg2 = seg;
  put(sectionHead('Start page', '', ''), 'cn-section-heading-lockup');
  var dd = T('t-dd'); txt(dd, 'label', 'Open the prototype on');
  var menu = dd.querySelector('.menu'), tplOpt = menu.querySelector('.opt').cloneNode(true); menu.innerHTML = '';
  VIEWS.forEach(function (vw) { var li = tplOpt.cloneNode(true); li.firstChild.textContent = vw.label + ' '; li.setAttribute('data-value', vw.id); li.setAttribute('aria-selected', String(vw.id === 'overview')); menu.appendChild(li); });
  txt(dd, '.ddval', 'Overview'); dd.querySelector('.trigger').setAttribute('data-setting', 'start');
  put(dd, 'cn-dropdown'); UI.startDd = dd;
  put(sectionHead('Notifications', '', ''), 'cn-section-heading-lockup');
  [['notifyApprovals', 'Tell me when a payment needs my approval'], ['notifyExceptions', 'Tell me about new material risk exceptions'], ['notifyMessages', 'Tell me when HSBC sends a message']].forEach(function (n) {
    var f = T('t-switch'); var inp = f.querySelector('input'), lab = f.querySelector('label');
    inp.id = 'sw-' + n[0]; lab.setAttribute('for', inp.id); lab.lastChild.textContent = ' ' + n[1]; inp.setAttribute('data-setting', n[0]);
    put(f, 'cn-selection-controls');
  });
  put(sectionHead('Saved state', '', ''), 'cn-section-heading-lockup');
  var reset = T('t-btn3'); reset.textContent = 'Reset saved filters, decisions and requests'; reset.setAttribute('type', 'button'); reset.setAttribute('data-action', 'reset-state');
  var row = document.createElement('div'); row.className = 'l-row'; row.appendChild(wrap('cn-button', reset)); sec.appendChild(row);
  v.appendChild(sec);
  return v;
}

/* ---------- overlays: one Drawer, one Modal, one Toast region — each cloned whole ---------- */
function buildOverlays() {
  var d = wrap('cn-drawer');
  var scrim = T('t-scrim'), sheet = T('t-sheet');
  d.appendChild(scrim); d.appendChild(sheet); document.body.appendChild(d);
  UI.scrim = scrim; UI.sheet = sheet;
  var m = wrap('cn-modals'); var ov = T('t-modal'); m.appendChild(ov); document.body.appendChild(m); UI.modal = ov;
  var t = wrap('cn-toast'); var reg = T('t-toastregion'); t.appendChild(reg); document.body.appendChild(t); UI.toasts = reg;
}

function buildApp() {
  buildShell();
  var stack = document.createElement('div'); stack.className = 'cn-layout-utilities';
  var inner = document.createElement('div'); inner.className = 'l-stack'; inner.setAttribute('data-gap', 'l');
  stack.appendChild(inner);
  inner.appendChild(buildHeader());
  inner.appendChild(buildFilterBar());
  var views = [buildOverview(), buildAccounts(), buildLiquidity(), buildPayments(), buildFx(), buildRisk(), buildTrade(), buildReports(), buildMessages(), buildSettings()];
  views.forEach(function (vw) { inner.appendChild(vw); });
  UI.main.appendChild(stack);
  buildOverlays();
  document.querySelectorAll('figure.dv').forEach(function (f) { f.classList.add('dv-fit-on'); });
}
buildApp();
