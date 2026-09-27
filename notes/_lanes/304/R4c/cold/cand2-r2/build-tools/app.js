(function () {
  'use strict';
  /* ONE in-page data model (rule 13). Every KPI, chart, grid, list and filter option below reads
     from DATA; nothing is typed twice. Illustrative data only — no live banking connection. */
  const DATA = /*__DATA__*/null;
  const PAGE = document.body.getAttribute('data-page');
  const LS = 'ceo-hsbc-prototype-v1';
  const ENT = {}; DATA.entities.forEach(e => { ENT[e.id] = e; });
  const REG = {}; DATA.regions.forEach(r => { REG[r.id] = r; });
  const FX = DATA.fx, DAYS = DATA.days, N = DAYS.length;
  const MON = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

  /* ---------- persisted state: localStorage (per viewer) + URL (shareable) ---------- */
  function load() { try { return JSON.parse(localStorage.getItem(LS)) || {}; } catch (e) { return {}; } }
  const S = Object.assign({ theme: 'light', entity: 'all', region: 'all', period: 30, pay: {}, exc: {}, req: [],
    reqUpd: {}, msg: {}, tf: {}, fxNew: [], grid: {}, notify: { approvals: true, exceptions: true, messages: false },
    reports: {}, tab: {} }, load());
  function save() { try { localStorage.setItem(LS, JSON.stringify(S)); } catch (e) { /* storage blocked: state lives for this view only */ } }
  const Q = new URLSearchParams(location.search);
  if (Q.has('entity')) S.entity = Q.get('entity');
  if (Q.has('region')) S.region = Q.get('region');
  if (Q.has('period')) S.period = +Q.get('period') || 30;
  if (Q.has('theme')) S.theme = Q.get('theme') === 'dark' ? 'dark' : 'light';
  if (S.entity !== 'all' && !ENT[S.entity]) S.entity = 'all';
  if (S.region !== 'all' && !REG[S.region]) S.region = 'all';
  if ([7, 14, 30].indexOf(S.period) < 0) S.period = 30;
  if (PAGE === 'risk' && Q.has('tab')) S.tab.risk = Q.get('tab') === 'positions' ? 'positions' : 'exceptions';

  function syncUrl() {
    const p = new URLSearchParams(location.search);
    ['entity', 'region'].forEach(k => { if (S[k] === 'all') p.delete(k); else p.set(k, S[k]); });
    if (S.period === 30) p.delete('period'); else p.set('period', S.period);
    p.delete('theme');
    const qs = p.toString();
    history.replaceState(null, '', location.pathname + (qs ? '?' + qs : '') + location.hash);
    carryParams();
  }
  /* every internal link carries the shared filters, so the next page opens where this one was left */
  function carryParams() {
    document.querySelectorAll('a[data-nav-link]').forEach(a => {
      const base = a.getAttribute('data-nav-link');
      const p = new URLSearchParams();
      if (S.entity !== 'all') p.set('entity', S.entity);
      if (S.region !== 'all') p.set('region', S.region);
      if (S.period !== 30) p.set('period', S.period);
      const extra = a.getAttribute('data-nav-extra');
      if (extra) new URLSearchParams(extra).forEach((v, k) => p.set(k, v));
      const qs = p.toString();
      a.setAttribute('href', base + (qs ? '?' + qs : ''));
    });
  }

  /* ---------- formatting (display only; tables keep raw numbers) ---------- */
  const nf0 = new Intl.NumberFormat('en-GB', { maximumFractionDigits: 0 });
  const nf1 = new Intl.NumberFormat('en-GB', { minimumFractionDigits: 1, maximumFractionDigits: 1 });
  const nf2 = new Intl.NumberFormat('en-GB', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  function gbpM(v) { const s = v < 0 ? '−' : ''; return s + '£' + (Math.abs(v) / 1e6).toFixed(1) + 'm'; }
  function gbpFull(v) { const s = v < 0 ? '−' : ''; return s + '£' + nf2.format(Math.abs(v)); }
  function ccyFull(ccy, v) { const s = v < 0 ? '−' : ''; return s + nf2.format(Math.abs(v)) + ' ' + ccy; }
  function fmtDate(iso) { const d = iso.slice(0, 10).split('-'); return (+d[2]) + ' ' + MON[+d[1] - 1] + ' ' + d[0]; }
  function short(iso) { const d = iso.split('-'); return (+d[2]) + ' ' + MON[+d[1] - 1]; }
  function esc(s) { return String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c])); }
  function m1(v) { return Math.round(v / 1e5) / 10; }   /* GBP -> £ millions, one decimal */

  /* ---------- scope: the shared entity / region / period filters ---------- */
  function regOf(r) { return r.region || (r.entity && ENT[r.entity] ? ENT[r.entity].region : null); }
  function inScope(r) {
    if (S.entity !== 'all' && r.entity && r.entity !== S.entity) return false;
    if (S.region !== 'all' && regOf(r) !== S.region) return false;
    return true;
  }
  function firstDay() { return DAYS[N - S.period]; }
  function inPeriod(iso) { return iso >= firstDay(); }
  /* line-family charts keep ≤12 points (per-point markers above 12 are clutter — geometry gate G11):
     every nth day, always ending on the as-of date */
  function sampleIdx(idx) { const step = Math.ceil(idx.length / 10); return { step: step, idx: idx.filter((_, k) => (idx.length - 1 - k) % step === 0) }; }
  function everyNote(step) { return step > 1 ? ', every ' + step + ' days' : ''; }
  function periodIdx() { const o = []; for (let i = N - S.period; i < N; i++) o.push(i); return o; }
  function entitiesInScope() { return DATA.entities.filter(e => inScope({ entity: e.id, region: e.region })); }
  function scopeLabel() {
    const a = S.entity !== 'all' ? ENT[S.entity].name : S.region !== 'all' ? REG[S.region].name : 'All entities';
    return a + ' · last ' + S.period + ' days';
  }

  /* ---------- workflow overlays: decisions made in this prototype, persisted ---------- */
  DATA.payments.forEach(p => { const o = S.pay[p.id]; if (o) { p.status = o.status; p.audit = p.audit.concat(o.audit || []); } });
  DATA.exceptions.forEach(x => { const o = S.exc[x.id]; if (o) { x.status = o.status; x.audit = x.audit.concat(o.audit || []); } });
  DATA.trade.forEach(t => { const o = S.tf[t.id]; if (o) { t.status = o.status; } });
  DATA.messages.forEach(m => { if (S.msg[m.id]) m.read = true; });
  S.req.forEach(r => { if (!DATA.requests.some(x => x.id === r.id)) DATA.requests.unshift(JSON.parse(JSON.stringify(r))); });
  DATA.requests.forEach(r => { const u = S.reqUpd[r.id]; if (u) { if (u.status) r.status = u.status; r.audit = r.audit.concat(u.audit || []); } });
  S.fxNew.forEach(d => { if (!DATA.fxDeals.some(x => x.id === d.id)) DATA.fxDeals.unshift(d); });
  function nowStamp() { const d = new Date(); return DATA.meta.asOf + 'T' + String(d.getHours()).padStart(2, '0') + ':' + String(d.getMinutes()).padStart(2, '0'); }

  /* ---------- derived measures ---------- */
  function cashSeries() {
    const out = new Array(N).fill(0);
    DATA.accounts.forEach(a => { if (!inScope(a)) return; a.balances.forEach((b, i) => { out[i] += b * FX[a.ccy]; }); });
    return out;
  }
  function headroomSeries() {
    const out = new Array(N).fill(0);
    DATA.facilities.forEach(f => { if (!f.committed || !inScope(f)) return; f.drawn.forEach((d, i) => { out[i] += f.limit - d; }); });
    return out;
  }
  function netFlowSeries() {
    const out = new Array(N).fill(0);
    DATA.transactions.forEach(t => { if (inScope(t)) out[DAYS.indexOf(t.date)] += t.gbp; });
    return out;
  }
  function positionsInScope() { return DATA.positions.filter(inScope); }
  function exposureBy(key) {
    const m = {}; positionsInScope().forEach(p => { m[p[key]] = (m[p[key]] || 0) + p.gbp; }); return m;
  }

  /* ---------- theme ---------- */
  function applyTheme() {
    document.documentElement.setAttribute('data-theme', S.theme);
    document.querySelectorAll('[data-theme-seg] button').forEach(b => b.setAttribute('aria-pressed', String(b.getAttribute('data-value') === S.theme)));
  }

  /* ---------- toast (Toast snippet mechanics: 6s, pause on hover/focus, focus hand-off) ---------- */
  const RM = matchMedia('(prefers-reduced-motion: reduce)').matches;
  function toast(msg, kind) {
    const region = document.getElementById('toastRegion'); if (!region) return;
    const glyph = kind === 'ok' ? 'to-success' : kind === 'warn' ? 'to-warning' : 'to-info';
    const origin = document.activeElement;
    const t = document.createElement('div'); t.className = 'toast ' + (kind || 'info'); t.setAttribute('role', 'status');
    t.setAttribute('data-carries', 'symbol label');
    t.innerHTML = '<span class="ic"><svg aria-hidden="true"><use href="#' + glyph + '"/></svg></span><p class="msg t-ed-body">' + esc(msg) +
      '</p><button class="x" type="button" aria-label="Dismiss message"><svg aria-hidden="true"><use href="#to-close"/></svg></button>';
    region.appendChild(t);
    let remain = 6000, started = Date.now(), timer = setTimeout(leave, remain), paused = false;
    function leave() { if (RM) { t.remove(); return; } t.classList.add('leaving'); t.addEventListener('transitionend', () => t.remove(), { once: true }); setTimeout(() => t.remove(), 600); }
    function pause() { if (paused) return; paused = true; clearTimeout(timer); remain -= Date.now() - started; }
    function resume() { if (!paused) return; paused = false; started = Date.now(); timer = setTimeout(leave, Math.max(remain, 1000)); }
    t.addEventListener('mouseenter', pause); t.addEventListener('mouseleave', resume);
    t.addEventListener('focusin', pause); t.addEventListener('focusout', resume);
    const self = t.querySelector('.x');
    self.addEventListener('click', () => {
      clearTimeout(timer); leave();
      const nxt = [...region.querySelectorAll('.toast:not(.leaving) .x')].filter(b => b !== self)[0];
      const home = nxt || origin; if (home && document.body.contains(home)) home.focus();
    });
  }

  /* ---------- drawer (Drawer snippet mechanics: show, two frames, focus in, THEN inert) ---------- */
  const shellHost = document.getElementById('app-shell');
  let drawerReturn = null, returnSel = null;   /* returnSel re-finds the row when a re-render replaced it */
  function openDrawer(title, bodyHtml, actions) {
    const sheet = document.getElementById('sheet'), scrim = document.getElementById('scrim');
    drawerReturn = document.activeElement;
    document.getElementById('dtitle').textContent = title;
    document.getElementById('dbody').innerHTML = bodyHtml;
    const foot = document.getElementById('dfoot');
    foot.innerHTML = (actions || []).map((a, i) => '<button class="dbtn ' + (i === 0 ? 'primary' : 'secondary') +
      ' t-cm-button t-cm-slot" type="button" data-drawer-act="' + i + '">' + esc(a.label) + '</button>').join('') +
      '<button class="dbtn secondary t-cm-button t-cm-slot" type="button" data-drawer-close>Close</button>';
    foot.__acts = actions || [];
    scrim.classList.add('open'); sheet.classList.add('open');
    requestAnimationFrame(() => requestAnimationFrame(() => {
      const f = drawerFocusable(); if (f.length) f[0].focus();
      shellHost.inert = true; shellHost.setAttribute('aria-hidden', 'true');
    }));
  }
  function drawerFocusable() { return [...document.getElementById('sheet').querySelectorAll('button,[href],input,textarea,select,[tabindex]:not([tabindex="-1"])')].filter(el => !el.disabled); }
  function closeDrawer(keepFocus) {
    const sheet = document.getElementById('sheet'); if (!sheet.classList.contains('open')) return;
    document.getElementById('scrim').classList.remove('open'); sheet.classList.remove('open');
    shellHost.inert = false; shellHost.removeAttribute('aria-hidden');
    if (!keepFocus) refocus(drawerReturn);
  }
  function refocus(el) {
    if (el && el !== document.body && document.body.contains(el)) { el.focus(); return; }
    const alt = returnSel && document.querySelector(returnSel); if (alt) alt.focus();
  }

  /* ---------- modal with the audit note (Modals + Textarea); validation before commit ---------- */
  let modalCfg = null, modalReturn = null;
  function openModal(cfg) {
    modalCfg = cfg; modalReturn = document.activeElement;
    /* one modal surface at a time (drawer meta mustNotNeighbour: "a second drawer or open modal"):
       a decision taken from the drawer closes the drawer, and focus later returns to the record's row */
    if (document.getElementById('sheet').classList.contains('open')) { modalReturn = drawerReturn; closeDrawer(true); }
    document.getElementById('mtitle').textContent = cfg.title;
    document.getElementById('mbody').textContent = cfg.body;
    document.getElementById('mconfirm').textContent = cfg.confirm;
    const ta = document.getElementById('t1'); ta.value = '';
    ta.dispatchEvent(new Event('input'));
    document.getElementById('t1-help').textContent = cfg.noteMin ? 'Required — at least ' + cfg.noteMin + ' characters. Saved to the audit trail.' : 'Optional. Saved to the audit trail.';
    setNoteError('');
    const ov = document.getElementById('overlay'); ov.classList.add('open');
    requestAnimationFrame(() => requestAnimationFrame(() => { ta.focus(); shellHost.inert = true; shellHost.setAttribute('aria-hidden', 'true'); }));
  }
  function setNoteError(msg) {
    const g = document.getElementById('t1-group'), e = document.getElementById('t1-err'), ta = document.getElementById('t1');
    g.classList.toggle('is-error', !!msg); e.hidden = !msg; e.querySelector('p').textContent = msg;
    if (msg) ta.setAttribute('aria-invalid', 'true'); else ta.removeAttribute('aria-invalid');
  }
  function closeModal() {
    const ov = document.getElementById('overlay'); if (!ov.classList.contains('open')) return;
    ov.classList.remove('open');
    shellHost.inert = false; shellHost.removeAttribute('aria-hidden');
    refocus(modalReturn);
    modalCfg = null;
  }
  function confirmModal() {
    if (!modalCfg) return;
    const note = document.getElementById('t1').value.trim();
    if (modalCfg.noteMin && note.length < modalCfg.noteMin) { setNoteError('Add an audit note of at least ' + modalCfg.noteMin + ' characters.'); document.getElementById('t1').focus(); return; }
    const err = modalCfg.validate ? modalCfg.validate(note) : '';
    if (err) { setNoteError(err); return; }
    const done = modalCfg.onConfirm; closeModal(); done(note);
  }

  /* ---------- CSV export ---------- */
  function downloadCsv(name, header, rows) {
    const q = v => '"' + String(v).replace(/"/g, '""') + '"';
    const csv = [header.map(q).join(',')].concat(rows.map(r => r.map(q).join(','))).join('\r\n');
    const url = URL.createObjectURL(new Blob([csv], { type: 'text/csv' }));
    const a = document.createElement('a'); a.href = url; a.download = name; document.body.appendChild(a); a.click();
    setTimeout(() => { URL.revokeObjectURL(url); a.remove(); }, 0);
    toast('Exported ' + rows.length + ' rows to ' + name + '.', 'ok');
  }

  /* ---------- charts: every figure is drawn by dvRender from DATA, re-drawn on every filter change ---------- */
  const LETTERS = 'ABCDEFGHIJKL';
  const SHAPES = ['sw-circle', 'sw-square', 'sw-diamond', 'sw-circle', 'sw-square'];
  function legendRows(host, names, shaped) {
    if (!host) return;
    const id = host.id;
    const fresh = host.cloneNode(false);            /* a new host resets dv-legend's per-host record */
    fresh.innerHTML = names.map((n, i) => '<li class="dv-legrow" data-series="' + (i + 1) + '"><span class="dv-leg-sw' +
      (shaped ? ' ' + SHAPES[i % SHAPES.length] : '') + '" role="checkbox" aria-checked="true" tabindex="0" aria-label="Show or hide ' + esc(n) +
      '" style="--sc:var(--data-series-' + ((i % 5) + 1) + ')"></span><button type="button" class="dv-leg-item t-cm-chart-label" data-series="' + (i + 1) +
      '" aria-pressed="false" aria-label="Isolate ' + esc(n) + '"><span class="dv-key t-cm-chart-key">' + LETTERS[i] +
      '</span><span class="dv-leg-name">' + esc(n) + '</span></button></li>').join('') +
      '<li class="dv-leg-reset-wrap"><button type="button" class="dv-leg-reset t-cm-chart-label" data-for="' + id + '" disabled>Reset</button></li>';
    host.replaceWith(fresh);
  }
  /* dv-pie-009: a ring carries at most six slices — the smallest fold into "Other" */
  function capSlices(pairs) {
    if (pairs.length <= 6) return pairs;
    const head = pairs.slice(0, 5), rest = pairs.slice(5);
    return head.concat([['Other', rest.reduce((s, x) => s + x[1], 0)]]);
  }
  function draw(id, spec, legend) {
    const fig = document.getElementById(id); if (!fig || !window.dvRender) return;
    try {
      const empty = !spec.series.length || !spec.categories.length || spec.series.every(s => s.values.every(v => v === 0));
      fig.toggleAttribute('data-empty', empty);
      if (empty) { spec = Object.assign({}, spec, { categories: ['No data'], series: [{ name: spec.series[0] ? spec.series[0].name : 'Value', values: [0] }] }); }
      if (legend) legendRows(fig.querySelector('ul.dv-leg'), legend, spec.type === 'line' || spec.type === 'multiline' || spec.type === 'scatter');
      window.dvRender(fig, spec);
    } catch (e) { console.error(e); }
  }

  /* KPI tile sparkline — the Kpi-tile's own passive inline scale (viewBox 200×48, aria-hidden),
     its points computed from DATA rather than typed. */
  function sparkPoints(vals) {
    const lo = Math.min.apply(null, vals), hi = Math.max.apply(null, vals), span = hi - lo || 1;
    return vals.map((v, i) => (3 + i * 194 / (vals.length - 1)).toFixed(1) + ',' + (45 - (v - lo) / span * 42).toFixed(1));
  }
  function kpi(id, label, vals, opts) {
    const el = document.getElementById(id); if (!el) return;
    const last = vals[vals.length - 1], first = vals[0];
    const pct = first ? (last - first) / Math.abs(first) * 100 : 0;
    const dir = Math.abs(pct) < 0.05 ? 'flat' : pct > 0 ? 'up' : 'down';
    el.querySelector('.kpi-lbl').textContent = label;
    el.setAttribute('aria-label', label + ', ' + scopeLabel());
    el.querySelector('.kpi-val').innerHTML = (opts && opts.plain) ? '<span>' + esc(opts.plain(last)) + '</span>' :
      '<span class="unit">' + (last < 0 ? '−£' : '£') + '</span><span>' + nf1.format(Math.abs(last) / 1e6) + 'm</span>';
    const d = el.querySelector('.kpi-delta'); d.className = 'kpi-delta ' + dir;
    d.innerHTML = '<span class="glyph" aria-hidden="true"><svg><use href="#kpi-' + dir + '"/></svg></span><span class="t-cm-figure-6">' +
      (dir === 'flat' ? 'No change' : (pct > 0 ? '+' : '−') + Math.abs(pct).toFixed(1) + '% ' + dir) + '</span><span class="kpi-per t-cm-legal">vs ' + short(DAYS[N - vals.length]) + '</span>';
    const svg = el.querySelector('svg.spark-inline'); if (!svg) return;
    svg.setAttribute('data-trend', dir);
    const pts = sparkPoints(vals);
    svg.querySelector('polyline').setAttribute('points', pts.join(' '));
    svg.querySelector('polygon').setAttribute('points', pts.join(' ') + ' 197.0,45 3.0,45');
  }

  /* ---------- list engine (List-items rows + Search-field + Pagination), for records without an amount ---------- */
  const LISTS = {};
  function listEngine(cfg) {
    const st = { q: '', sort: cfg.sorts[0].key, page: 1, size: cfg.size || 8 };
    const saved = S.grid[PAGE + ':' + cfg.id]; if (saved) Object.assign(st, saved, { q: saved.q || '' });
    LISTS[cfg.id] = { cfg, st };
    const host = document.getElementById(cfg.id);
    const search = document.getElementById(cfg.id + '-q'), pg = document.getElementById(cfg.id + '-pg');
    const count = document.getElementById(cfg.id + '-count');
    if (search) search.value = st.q;
    function persist() { S.grid[PAGE + ':' + cfg.id] = { q: st.q, sort: st.sort, page: st.page }; save(); }
    function render() {
      let rows = cfg.rows().filter(r => !st.q || cfg.text(r).toLowerCase().indexOf(st.q.toLowerCase()) >= 0);
      const s = cfg.sorts.find(x => x.key === st.sort) || cfg.sorts[0];
      rows = rows.slice().sort(s.fn);
      const pages = Math.max(1, Math.ceil(rows.length / st.size)); st.page = Math.min(st.page, pages);
      const slice = rows.slice((st.page - 1) * st.size, st.page * st.size);
      host.innerHTML = slice.length ? slice.map(cfg.row).join('') :
        '<li><div class="row"><span class="body"><span class="line"><span class="title">Nothing matches</span></span><span class="line"><span class="desc">Clear the search or widen the filters.</span></span></span></div></li>';
      if (count) count.textContent = rows.length + ' of ' + cfg.rows().length + ' shown';
      if (pg) {
        let h = '<li><button class="ctrl" type="button" aria-label="Previous page" data-pg="prev"' + (st.page === 1 ? ' disabled' : '') + '><svg viewBox="0 0 18 18" aria-hidden="true"><use href="#dg-cleft"/></svg></button></li>';
        for (let p = 1; p <= pages; p++) h += '<li><a href="#" data-pg="' + p + '"' + (p === st.page ? ' aria-current="page" aria-label="Page ' + p + ', current page"' : ' aria-label="Page ' + p + '"') + '>' + p + '</a></li>';
        h += '<li><button class="ctrl" type="button" aria-label="Next page" data-pg="next"' + (st.page === pages ? ' disabled' : '') + '><svg viewBox="0 0 18 18" aria-hidden="true"><use href="#dg-cright"/></svg></button></li>';
        pg.querySelector('ul').innerHTML = h;
      }
      document.querySelectorAll('[data-list-sort="' + cfg.id + '"] button').forEach(b => b.setAttribute('aria-pressed', String(b.getAttribute('data-value') === st.sort)));
      persist();
    }
    if (search) {
      search.addEventListener('input', () => { st.q = search.value; st.page = 1; render(); });
      const clr = search.parentNode.querySelector('.clear');
      if (clr) clr.addEventListener('click', () => { search.value = ''; st.q = ''; st.page = 1; render(); search.focus(); });
    }
    if (pg) pg.addEventListener('click', e => {
      const b = e.target.closest('[data-pg]'); if (!b) return; e.preventDefault();
      const v = b.getAttribute('data-pg'); st.page = v === 'prev' ? st.page - 1 : v === 'next' ? st.page + 1 : +v; render();
      const cur = pg.querySelector('[aria-current="page"]'); if (cur) cur.focus();
    });
    document.querySelectorAll('[data-list-sort="' + cfg.id + '"] button').forEach(b => b.addEventListener('click', () => { st.sort = b.getAttribute('data-value'); st.page = 1; render(); }));
    host.addEventListener('click', e => { const b = e.target.closest('[data-open]'); if (!b) return; returnSel = '#' + cfg.id + ' [data-open="' + b.getAttribute('data-open') + '"]'; cfg.open(b.getAttribute('data-open')); });
    LISTS[cfg.id].render = render;
    render();
  }
  function statusClass(s) {
    return /Pending|Awaiting|Open|Amendment|Draft|Documents|In progress|Moderate/.test(s) ? 'warn' :
      /Rejected|Breach|Material|Failed/.test(s) ? 'err' : /Approved|Released|Settled|Resolved|Acknowledged|Confirmed|Issued|Received/.test(s) ? 'ok' : 'inf';
  }
  function listRow(id, title, status, desc, amount, avatar) {
    return '<li><button class="row" type="button" data-open="' + esc(id) + '"><span class="avatar" role="img" aria-label="' + esc(title) + '">' + esc(avatar) +
      '</span><span class="body"><span class="line"><span class="title">' + esc(title) + '</span><span class="status ' + statusClass(status) +
      '" data-carries="label"><span class="dot" aria-hidden="true"></span>' + esc(status) + '</span></span><span class="line"><span class="desc">' +
      esc(desc) + '</span><span class="amount">' + esc(amount) + '</span></span></span></button></li>';
  }
  function initials(s) { return s.replace(/[^A-Za-z ]/g, '').split(' ').filter(Boolean).slice(0, 2).map(w => w[0]).join('').toUpperCase(); }

  /* ---------- detail content: Summary key/value + Timeline audit trail ---------- */
  function summary(rows) {
    return '<div class="cn-summary"><dl class="summary">' + rows.map(r => '<div class="summary__row"><dt class="summary__k">' + esc(r[0]) +
      '</dt><dd class="summary__v">' + esc(r[1]) + '</dd></div>').join('') + '</dl></div>';
  }
  function timeline(audit) {
    if (!audit || !audit.length) return '';
    return '<div class="cn-timeline"><section class="tl" aria-labelledby="tl-h"><h2 id="tl-h" class="t-cm-section-label">Audit trail</h2><div class="tl-group"><ol class="tl-list">' +
      audit.slice().reverse().map(a => '<li class="' + (/Reject|raised automatically/.test(a.note) ? 'warn' : 'ok') + '"><span class="tl-node" aria-hidden="true"></span><span class="tl-line"><span class="tl-title t-cm-ctl-14">' +
        esc(a.by) + '</span></span><span class="tl-meta"><time class="t-cm-legal" datetime="' + esc(a.at) + '">' + esc(fmtDate(a.at) + ' ' + a.at.slice(11, 16)) +
        '</time></span><p class="tl-desc t-ed-body-small">' + esc(a.note) + '</p></li>').join('') + '</ol></div></section></div>';
  }

  /* ---------- the data grid: rows handed to the Data-grid component's own script ---------- */
  window.CEO_ROWS = [];
  let GRID = null;   /* {rows(): [...records], map(rec, i) -> row, open(rec)} */
  function gridRows() {
    if (!GRID) return [];
    return GRID.rows().map((r, i) => Object.assign({ id: i + 1, __rec: r }, GRID.map(r)));
  }
  function refreshGrid() {
    if (!GRID) return;
    const rows = gridRows();
    window.CEO_ROWS.length = 0; rows.forEach(r => window.CEO_ROWS.push(r));
    if (typeof window.__ceoGridRender === 'function') window.__ceoGridRender();
  }
  function gridRecord(tr) { const id = +tr.getAttribute('data-id'); const r = window.CEO_ROWS.find(x => x.id === id); return r ? r.__rec : null; }

  /* ================================================================ PAGES ================ */
  const P = {};

  P.index = function () {
    const idx = periodIdx();
    const cash = cashSeries(), head = headroomSeries();
    const liq = cash.map((c, i) => c + head[i]);
    const flow = netFlowSeries(); let run = 0; const cum = idx.map(i => (run += flow[i]));
    kpi('kpi-cash', 'Cash', idx.map(i => cash[i]));
    kpi('kpi-liq', 'Available liquidity', idx.map(i => liq[i]));
    kpi('kpi-head', 'Funding headroom', idx.map(i => head[i]));
    kpi('kpi-flow', 'Net cash flow, period to date', cum);
    const regs = DATA.regions.filter(r => S.region === 'all' || r.id === S.region);
    const byRC = {}, ccyTot = {};
    positionsInScope().forEach(p => { byRC[p.region + p.ccy] = (byRC[p.region + p.ccy] || 0) + p.gbp; ccyTot[p.ccy] = (ccyTot[p.ccy] || 0) + p.gbp; });
    const ccys = Object.keys(ccyTot).sort((a, b) => ccyTot[b] - ccyTot[a]);
    const top = ccys.slice(0, 4), rest = ccys.slice(4);
    const series = top.map(c => ({ name: c, values: regs.map(r => m1(byRC[r.id + c] || 0)) }));
    if (rest.length) series.push({ name: 'Other', values: regs.map(r => m1(rest.reduce((s, c) => s + (byRC[r.id + c] || 0), 0))) });
    draw('ov-region', { type: 'stacked-column', categories: regs.map(r => r.name), series: series, unit: '£m', categoryLabel: 'Region',
      caption: 'Exposure by region and currency, £ millions, ' + scopeLabel() }, series.map(s => s.name));
    draw('ov-ccy', { type: 'bar', categories: ccys, series: [{ name: 'Exposure', values: ccys.map(c => m1(ccyTot[c])) }], unit: '£m', categoryLabel: 'Currency',
      caption: 'Exposure by currency, £ millions' });
    const byR = exposureBy('region');
    draw('ov-limits', { type: 'bullet', categories: regs.map(r => r.name), series: [
      { name: 'Utilisation', values: regs.map(r => Math.round((byR[r.id] || 0) / DATA.regionLimits[r.id] * 1000) / 10) },
      { name: 'Policy ceiling', values: regs.map(() => 80) }], ranges: [60, 80, 100], format: 'percent', categoryLabel: 'Region',
      caption: 'Limit utilisation by region, per cent of limit, against the 80% policy ceiling' });
    /* ≤12 points per series (the geometry gate's G11 marker rule): sample every nth day, ending today */
    const sm = sampleIdx(idx), step = sm.step, sidx = sm.idx;
    draw('ov-trend', { type: 'stacked-area', categories: sidx.map(i => short(DAYS[i])), series: regs.map(r => {
      const tot = DATA.positions.filter(p => p.region === r.id).reduce((s, p) => s + p.gbp, 0) || 1;
      const f = (byR[r.id] || 0) / tot;
      return { name: r.name, values: sidx.map(i => m1(DATA.exposureHist[r.id][i] * f)) };
    }), unit: '£m', categoryLabel: 'Day', caption: 'Exposure by region over the period, £ millions' + (step > 1 ? ', every ' + step + ' days' : '') }, regs.map(r => r.name));
    /* decisions */
    const pend = DATA.payments.filter(p => p.status === 'Pending approval' && inScope(p)).sort((a, b) => b.gbp - a.gbp);
    const exc = DATA.exceptions.filter(x => x.status === 'Open' && x.severity === 'Material' && inScope(x)).sort((a, b) => b.over - a.over);
    setText('dec-pay-count', String(pend.length)); setAttr('dec-pay-count', 'aria-label', pend.length + ' payments awaiting approval');
    setText('dec-exc-count', String(exc.length)); setAttr('dec-exc-count', 'aria-label', exc.length + ' material exceptions open');
    fillList('dec-pay', pend.slice(0, 5).map(p => listRowLink('payments.html', p.id, p.beneficiary, p.status, ENT[p.entity].name + ' · ' + short(p.date), gbpM(p.gbp), initials(p.beneficiary))),
      'No payments are waiting for you in this scope.');
    fillList('dec-exc', exc.slice(0, 5).map(x => listRowLink('risk.html', x.id, x.type + ' — ' + x.counterparty, x.severity, REG[x.region].name + ' · ' + x.ccy + ' · ' + short(x.date), gbpM(x.over) + ' over', initials(x.counterparty))),
      'No material exceptions are open in this scope.');
  };
  function setText(id, t) { const e = document.getElementById(id); if (e) e.textContent = t; }
  function setAttr(id, a, v) { const e = document.getElementById(id); if (e) e.setAttribute(a, v); }
  function fillList(id, rows, emptyMsg) {
    const ul = document.getElementById(id); if (!ul) return;
    ul.innerHTML = rows.length ? rows.join('') : '<li><div class="row"><span class="body"><span class="line"><span class="title">Nothing to decide</span></span><span class="line"><span class="desc">' + esc(emptyMsg) + '</span></span></span></div></li>';
  }
  function listRowLink(page, id, title, status, desc, amount, av) {
    return listRow(id, title, status, desc, amount, av).replace('<button class="row" type="button" data-open="' + esc(id) + '">', '<button class="row" type="button" data-goto="' + page + '?open=' + encodeURIComponent(id) + '">');
  }

  P.accounts = function () {
    const idx = periodIdx();
    const regs = DATA.regions.filter(r => S.region === 'all' || r.id === S.region);
    const accs = DATA.accounts.filter(inScope);
    const sb = sampleIdx(idx);
    draw('ac-bal', { type: 'multiline', categories: sb.idx.map(i => short(DAYS[i])), categoryLabel: 'Day', unit: '£m',
      caption: 'Cash balance by region, £ millions' + everyNote(sb.step), series: regs.map(r => ({ name: r.name, values: sb.idx.map(i => m1(accs.filter(a => ENT[a.entity].region === r.id).reduce((s, a) => s + a.balances[i] * FX[a.ccy], 0))) })) }, regs.map(r => r.name));
    const byC = {}; accs.forEach(a => { byC[a.ccy] = (byC[a.ccy] || 0) + a.balances[N - 1] * FX[a.ccy]; });
    const cs = capSlices(Object.keys(byC).sort((a, b) => byC[b] - byC[a]).map(c => [c, byC[c]]));
    draw('ac-ccy', { type: 'pie', categories: cs.map(c => c[0]), series: [{ name: 'Balance', values: cs.map(c => m1(c[1])) }], unit: '£m', categoryLabel: 'Currency',
      caption: 'Closing cash by currency, £ millions' }, cs.map(c => c[0]));
    const tx = DATA.transactions.filter(t => inScope(t) && inPeriod(t.date));
    const types = [...new Set(DATA.transactions.map(t => t.type))];
    draw('ac-type', { type: 'grouped-column', categories: types, categoryLabel: 'Type', unit: '£m', caption: 'Money in and out by transaction type, £ millions',
      series: [{ name: 'In', values: types.map(t => m1(tx.filter(x => x.type === t && x.gbp > 0).reduce((s, x) => s + x.gbp, 0))) },
               { name: 'Out', values: types.map(t => m1(-tx.filter(x => x.type === t && x.gbp < 0).reduce((s, x) => s + x.gbp, 0))) }] }, ['In', 'Out']);
  };
  P.accounts.grid = {
    rows: () => DATA.transactions.filter(t => inScope(t) && inPeriod(t.date)).sort((a, b) => b.date.localeCompare(a.date)),
    map: t => ({ date: t.date, payee: t.counterparty, ref: t.ref, type: t.type, amount: t.gbp }),
    open: t => openDrawer('Transaction ' + t.ref, summary([['Date', fmtDate(t.date)], ['Entity', ENT[t.entity].name], ['Account', t.account + ' · ' + t.ccy], ['Counterparty', t.counterparty],
      ['Type', t.type], ['Amount', ccyFull(t.ccy, t.amount)], ['GBP equivalent', gbpFull(t.gbp)], ['Illustrative rate', '1 ' + t.ccy + ' = £' + FX[t.ccy]]]),
      [{ label: 'Raise a query', run: () => raiseRequest('Payments investigation', 'Query on transaction ' + t.ref, t.entity) },
       { label: 'Export this row', run: () => downloadCsv(t.ref + '.csv', ['Date', 'Entity', 'Counterparty', 'Reference', 'Type', 'Currency', 'Amount', 'GBP'], [[t.date, ENT[t.entity].name, t.counterparty, t.ref, t.type, t.ccy, t.amount, t.gbp]]) }]),
    csv: () => [['Date', 'Entity', 'Counterparty', 'Reference', 'Type', 'Currency', 'Amount', 'GBP'], P.accounts.grid.rows().map(t => [t.date, ENT[t.entity].name, t.counterparty, t.ref, t.type, t.ccy, t.amount, t.gbp])]
  };

  P.liquidity = function () {
    const idx = periodIdx();
    const cash = cashSeries(), head = headroomSeries(), flow = netFlowSeries();
    const sq = sampleIdx(idx);
    /* each bar is the net flow of the days since the previous point, so no day is dropped by the sampling */
    const netFor = k => { const hi = sq.idx[k], lo = k ? sq.idx[k - 1] + 1 : idx[0]; let t = 0; for (let i = lo; i <= hi; i++) t += flow[i]; return m1(t); };
    draw('lq-combo', { type: 'combo', categories: sq.idx.map(i => short(DAYS[i])), categoryLabel: 'Day', caption: 'Net cash flow (£ millions) and liquidity cover against the policy minimum (%)' + everyNote(sq.step),
      series: [{ name: 'Net cash flow (£m)', kind: 'column', unit: '£m', values: sq.idx.map((_, k) => netFor(k)) },
               { name: 'Liquidity cover (%)', kind: 'line', unit: '', format: 'percent', values: sq.idx.map(i => Math.round((cash[i] + head[i]) / DATA.meta.policyMinLiquidity * 1000) / 10) }] }, ['Net cash flow (£m)', 'Liquidity cover (%)']);
    const last = N - 1;
    const facs = DATA.facilities.filter(inScope);
    const comp = [['Cash at bank', cash[last]], ['Committed undrawn facilities', facs.filter(f => f.committed).reduce((s, f) => s + f.limit - f.drawn[last], 0)],
      ['Uncommitted undrawn lines', facs.filter(f => !f.committed).reduce((s, f) => s + f.limit - f.drawn[last], 0)]];
    draw('lq-mix', { type: 'donut', categories: comp.map(c => c[0]), series: [{ name: 'Liquidity', values: comp.map(c => m1(c[1])) }], unit: '£m', categoryLabel: 'Source',
      caption: 'Sources of available liquidity today, £ millions' }, comp.map(c => c[0]));
    draw('lq-fac', { type: 'bullet', categories: facs.map(f => f.id + ' ' + f.type.split(' ')[0]), categoryLabel: 'Facility', format: 'percent', ranges: [50, 85, 100],
      caption: 'Facility utilisation, per cent drawn, against the 85% drawdown trigger',
      series: [{ name: 'Drawn', values: facs.map(f => Math.round(f.drawn[last] / f.limit * 1000) / 10) }, { name: 'Trigger', values: facs.map(() => 85) }] });
  };
  P.liquidity.grid = {
    rows: () => DATA.facilities.filter(inScope).sort((a, b) => a.maturity.localeCompare(b.maturity)),
    map: f => ({ date: f.maturity, payee: ENT[f.entity].name, ref: f.id + ' · ' + f.lender, type: f.type, amount: f.limit - f.drawn[N - 1] }),
    open: f => openDrawer(f.type + ' ' + f.id, summary([['Entity', ENT[f.entity].name], ['Lender', f.lender], ['Committed', f.committed ? 'Yes' : 'No'], ['Limit', gbpFull(f.limit)],
      ['Drawn today', gbpFull(f.drawn[N - 1])], ['Undrawn', gbpFull(f.limit - f.drawn[N - 1])], ['Margin', f.margin + '% over reference rate'], ['Maturity', fmtDate(f.maturity)]]),
      [{ label: 'Request a drawdown', run: () => raiseRequest('Account maintenance', 'Drawdown request on ' + f.id + ' (' + f.type + ')', f.entity) }]),
    csv: () => [['Facility', 'Entity', 'Type', 'Lender', 'Limit', 'Drawn', 'Undrawn', 'Maturity'], P.liquidity.grid.rows().map(f => [f.id, ENT[f.entity].name, f.type, f.lender, f.limit, f.drawn[N - 1], f.limit - f.drawn[N - 1], f.maturity])]
  };

  const CEO_LIMIT = 50e6;
  function decidePayment(p, decision, note) {
    const by = 'Chief Executive Officer (you)';
    const status = decision === 'approve' ? 'Approved' : 'Rejected';
    const entry = { at: nowStamp(), by: by, note: (decision === 'approve' ? 'Approved. ' : 'Rejected. ') + (note || 'No note added.') };
    p.status = status; p.audit.push(entry);
    const o = S.pay[p.id] || { audit: [] }; o.status = status; o.audit.push(entry); S.pay[p.id] = o; save();
    toast('Payment ' + p.id + ' ' + status.toLowerCase() + '. The audit trail has been updated.', decision === 'approve' ? 'ok' : 'warn');
    rerender();
  }
  function approvalModal(p, decision) {
    openModal({ title: (decision === 'approve' ? 'Approve ' : 'Reject ') + p.id,
      body: (decision === 'approve' ? 'Approve ' : 'Reject ') + gbpFull(p.gbp) + ' (' + ccyFull(p.ccy, p.amount) + ') to ' + p.beneficiary + ' from ' + ENT[p.entity].name + '. This is a simulated approval — no payment is sent.',
      confirm: decision === 'approve' ? 'Approve payment' : 'Reject payment', noteMin: decision === 'reject' ? 15 : 0,
      validate: () => p.status !== 'Pending approval' ? 'This payment is no longer pending.' : (decision === 'approve' && p.gbp > CEO_LIMIT ? 'This payment is above your £50m approval limit. Reject it or ask the board delegate.' : ''),
      onConfirm: note => { decidePayment(p, decision, note); closeDrawer(); } });
  }
  P.payments = function () {
    const idx = periodIdx();
    const pays = DATA.payments.filter(p => inScope(p) && inPeriod(p.date));
    draw('py-daily', { type: 'column', categories: idx.map(i => short(DAYS[i])), categoryLabel: 'Day', unit: '£m', caption: 'Payment value created per day, £ millions',
      series: [{ name: 'Value', values: idx.map(i => m1(pays.filter(p => p.date === DAYS[i]).reduce((s, p) => s + p.gbp, 0))) }] });
    const bands = [[0, 1e6, '<£1m'], [1e6, 2e6, '£1–2m'], [2e6, 4e6, '£2–4m'], [4e6, 6e6, '£4–6m'], [6e6, 1e12, '>£6m']];
    draw('py-hist', { type: 'histogram', categories: bands.map(b => b[2]), categoryLabel: 'Size band', caption: 'Number of payments by size band',
      series: [{ name: 'payments', values: bands.map(b => pays.filter(p => p.gbp >= b[0] && p.gbp < b[1]).length) }] });
    const regs = DATA.regions.filter(r => S.region === 'all' || r.id === S.region);
    draw('py-region', { type: 'grouped-column', categories: regs.map(r => r.name), categoryLabel: 'Region', unit: '£m', caption: 'Pending versus released value by region, £ millions',
      series: [{ name: 'Pending approval', values: regs.map(r => m1(pays.filter(p => p.region === r.id && p.status === 'Pending approval').reduce((s, p) => s + p.gbp, 0))) },
               { name: 'Released', values: regs.map(r => m1(pays.filter(p => p.region === r.id && p.status === 'Released').reduce((s, p) => s + p.gbp, 0))) }] }, ['Pending approval', 'Released']);
    const sts = ['Pending approval', 'Approved', 'Released', 'Scheduled', 'Rejected'];
    draw('py-status', { type: 'donut', categories: sts, series: [{ name: 'Payments', values: sts.map(s => pays.filter(p => p.status === s).length) }], categoryLabel: 'Status',
      caption: 'Payments by status, count' }, sts);
    const pend = pays.filter(p => p.status === 'Pending approval').length;
    setText('py-pending', pend + ' awaiting your approval');
  };
  P.payments.grid = {
    rows: () => DATA.payments.filter(p => inScope(p) && inPeriod(p.date)).sort((a, b) => (a.status === 'Pending approval' ? 0 : 1) - (b.status === 'Pending approval' ? 0 : 1) || b.date.localeCompare(a.date)),
    map: p => ({ date: p.date, payee: p.beneficiary, ref: p.id + ' · ' + p.purpose, type: p.status, amount: p.gbp }),
    open: p => openDrawer('Payment ' + p.id, summary([['Status', p.status], ['Beneficiary', p.beneficiary], ['Debit entity', ENT[p.entity].name], ['Amount', ccyFull(p.ccy, p.amount)],
      ['GBP equivalent', gbpFull(p.gbp)], ['Method', p.method], ['Value date', fmtDate(p.valueDate)], ['Purpose', p.purpose], ['Maker', p.maker]]) + timeline(p.audit),
      p.status === 'Pending approval' ? [{ label: 'Approve', run: () => approvalModal(p, 'approve') }, { label: 'Reject', run: () => approvalModal(p, 'reject') }] :
        [{ label: 'Download advice', run: () => downloadCsv(p.id + '-advice.csv', ['Payment', 'Beneficiary', 'Currency', 'Amount', 'Status', 'Value date'], [[p.id, p.beneficiary, p.ccy, p.amount, p.status, p.valueDate]]) }]),
    csv: () => [['Payment', 'Date', 'Entity', 'Beneficiary', 'Currency', 'Amount', 'GBP', 'Status'], P.payments.grid.rows().map(p => [p.id, p.date, ENT[p.entity].name, p.beneficiary, p.ccy, p.amount, p.gbp, p.status])]
  };

  P.fx = function () {
    const idx = periodIdx();
    const o = DATA.gbpusdOhlc;
    draw('fx-candle', { type: 'candlestick', categories: idx.map(i => short(DAYS[i])), categoryLabel: 'Day', caption: 'GBP/USD daily open, high, low and close (illustrative)',
      series: ['open', 'high', 'low', 'close'].map(k => ({ name: k[0].toUpperCase() + k.slice(1), values: idx.map(i => o[k][i]) })) });
    const deals = DATA.fxDeals.filter(d => inScope(d) && inPeriod(d.date));
    const cs = ['USD', 'EUR', 'HKD', 'CNY'], sf = sampleIdx(idx);
    draw('fx-index', { type: 'multiline', categories: sf.idx.map(i => short(DAYS[i])), categoryLabel: 'Day', unit: '£m',
      caption: 'Cumulative currency bought over the period, £ millions' + everyNote(sf.step),
      series: cs.map(c => ({ name: c, values: sf.idx.map(i => m1(deals.filter(d => d.ccy === c && d.side === 'Buy' && d.date <= DAYS[i]).reduce((s, d) => s + d.gbp, 0))) })) }, cs);
    const all = ['USD', 'EUR', 'HKD', 'SGD', 'CNY', 'AED'];
    draw('fx-fly', { type: 'butterfly-h', categories: all, categoryLabel: 'Currency', caption: 'Currency bought versus sold against sterling, £ millions',
      series: [{ name: 'Bought', values: all.map(c => m1(deals.filter(d => d.ccy === c && d.side === 'Buy').reduce((s, d) => s + d.gbp, 0))) },
               { name: 'Sold', values: all.map(c => m1(deals.filter(d => d.ccy === c && d.side === 'Sell').reduce((s, d) => s + d.gbp, 0))) }] }, ['Bought', 'Sold']);
    const rt = document.getElementById('fx-rates');
    if (rt) rt.innerHTML = Object.keys(FX).filter(c => c !== 'GBP').map(c => '<div class="summary__row"><dt class="summary__k">1 ' + c + '</dt><dd class="summary__v">£' + FX[c] + '</dd></div>').join('');
  };
  P.fx.grid = {
    rows: () => DATA.fxDeals.filter(d => inScope(d) && inPeriod(d.date)).sort((a, b) => b.date.localeCompare(a.date)),
    map: d => ({ date: d.date, payee: d.side + ' ' + d.ccy + ' · ' + ENT[d.entity].name, ref: d.id + ' · ' + d.bank, type: d.type + ' · ' + d.status, amount: d.gbp }),
    open: d => openDrawer('FX deal ' + d.id, summary([['Pair', d.pair], ['Side', d.side + ' ' + d.ccy], ['Notional', ccyFull(d.ccy, d.amount)], ['GBP equivalent', gbpFull(d.gbp)], ['Rate', d.rate + ' ' + d.ccy + ' per GBP'],
      ['Type', d.type], ['Value date', fmtDate(d.valueDate)], ['Bank', d.bank], ['Status', d.status]]),
      [{ label: 'Request confirmation', run: () => raiseRequest('Trade documents', 'Confirmation for FX deal ' + d.id, d.entity) }]),
    csv: () => [['Deal', 'Date', 'Entity', 'Pair', 'Side', 'Notional', 'GBP', 'Rate', 'Type', 'Status'], P.fx.grid.rows().map(d => [d.id, d.date, ENT[d.entity].name, d.pair, d.side, d.amount, d.gbp, d.rate, d.type, d.status])]
  };

  function riskTab() { return S.tab.risk || 'exceptions'; }
  P.risk = function () {
    const regs = DATA.regions.filter(r => S.region === 'all' || r.id === S.region);
    const byR = exposureBy('region');
    draw('rk-limits', { type: 'grouped-column', categories: regs.map(r => r.name), categoryLabel: 'Region', unit: '£m', caption: 'Exposure against limit by region, £ millions',
      series: [{ name: 'Exposure', values: regs.map(r => m1(byR[r.id] || 0)) }, { name: 'Limit', values: regs.map(r => m1(DATA.regionLimits[r.id])) }] }, ['Exposure', 'Limit']);
    const idx = periodIdx();
    draw('rk-box', { type: 'boxplot', categories: regs.map(r => r.name), categoryLabel: 'Region', caption: 'Spread of daily exposure over the period by region, £ millions',
      series: (function () {
        const q = regs.map(r => { const v = idx.map(i => m1(DATA.exposureHist[r.id][i])).sort((a, b) => a - b); const at = f => v[Math.min(v.length - 1, Math.round(f * (v.length - 1)))]; return [v[0], at(.25), at(.5), at(.75), v[v.length - 1]]; });
        return ['Minimum', 'Q1', 'Median', 'Q3', 'Maximum'].map((n, k) => ({ name: n, values: q.map(x => x[k]) }));
      }()) });
    const cps = {}; positionsInScope().forEach(p => { cps[p.counterparty] = cps[p.counterparty] || { n: 0, v: 0 }; cps[p.counterparty].n++; cps[p.counterparty].v += p.gbp; });
    const keys = Object.keys(cps).sort((a, b) => cps[a].n - cps[b].n || cps[a].v - cps[b].v).slice(-12);
    draw('rk-scatter', { type: 'scatter', categories: keys.map(k => String(cps[k].n)), categoryLabel: 'Open positions with the counterparty', caption: 'Counterparty concentration: number of positions against total exposure, £ millions',
      series: [{ name: 'Exposure (£m)', values: keys.map(k => m1(cps[k].v)) }] });
  };
  P.risk.gridFor = function (tab) {
    return tab === 'positions' ? {
      rows: () => positionsInScope().filter(p => !Q.get('ccy') || p.ccy === Q.get('ccy')).sort((a, b) => b.gbp - a.gbp),
      map: p => ({ date: p.maturity, payee: p.counterparty, ref: p.id + ' · ' + ENT[p.entity].name, type: p.type + ' · ' + REG[p.region].name + ' · ' + p.ccy, amount: p.gbp }),
      open: p => { const used = (exposureBy('region')[p.region] || 0); openDrawer('Position ' + p.id, summary([['Counterparty', p.counterparty], ['Entity', ENT[p.entity].name], ['Region', REG[p.region].name], ['Type', p.type],
        ['Notional', ccyFull(p.ccy, p.notional)], ['GBP equivalent', gbpFull(p.gbp)], ['Maturity', fmtDate(p.maturity)], ['Region limit', gbpFull(DATA.regionLimits[p.region])],
        ['Region utilisation', (used / DATA.regionLimits[p.region] * 100).toFixed(1) + '%'], ['Currency limit', gbpFull(DATA.ccyLimits[p.ccy] || 0)]]), []); },
      csv: () => [['Position', 'Entity', 'Region', 'Currency', 'Type', 'Counterparty', 'Notional', 'GBP', 'Maturity'], P.risk.gridFor('positions').rows().map(p => [p.id, ENT[p.entity].name, REG[p.region].name, p.ccy, p.type, p.counterparty, p.notional, p.gbp, p.maturity])]
    } : {
      rows: () => DATA.exceptions.filter(inScope).sort((a, b) => (a.status === 'Open' ? 0 : 1) - (b.status === 'Open' ? 0 : 1) || b.over - a.over),
      map: x => ({ date: x.date, payee: x.counterparty, ref: x.id + ' · ' + x.type, type: x.severity + ' · ' + x.status, amount: x.over }),
      open: x => openDrawer(x.type + ' ' + x.id, summary([['Status', x.status], ['Severity', x.severity], ['Counterparty', x.counterparty], ['Entity', ENT[x.entity].name], ['Region', REG[x.region].name],
        ['Currency', x.ccy], ['Over limit by', gbpFull(x.over)], ['Position', x.position], ['Owner', x.owner]]) + timeline(x.audit),
        x.status === 'Open' ? [{ label: 'Acknowledge', run: () => openModal({ title: 'Acknowledge ' + x.id, body: 'Record that you have seen this ' + x.type.toLowerCase() + ' and what happens next. The note goes to ' + x.owner + ' and the audit trail.',
          confirm: 'Acknowledge exception', noteMin: 20, validate: () => x.status !== 'Open' ? 'This exception is already acknowledged.' : '',
          onConfirm: note => { const e = { at: nowStamp(), by: 'Chief Executive Officer (you)', note: 'Acknowledged. ' + note }; x.status = 'Acknowledged'; x.audit.push(e);
            const o = S.exc[x.id] || { audit: [] }; o.status = 'Acknowledged'; o.audit.push(e); S.exc[x.id] = o; save(); closeDrawer();
            toast('Exception ' + x.id + ' acknowledged with your note.', 'ok'); rerender(); } }) }] :
          [{ label: 'View position', run: () => { location.href = 'risk.html?tab=positions&open=' + encodeURIComponent(x.position); } }]),
      csv: () => [['Exception', 'Date', 'Type', 'Severity', 'Status', 'Entity', 'Region', 'Currency', 'Counterparty', 'Over limit GBP'], P.risk.gridFor('exceptions').rows().map(x => [x.id, x.date, x.type, x.severity, x.status, ENT[x.entity].name, REG[x.region].name, x.ccy, x.counterparty, x.over])]
    };
  };

  P.trade = function () {
    const regs = DATA.regions.filter(r => S.region === 'all' || r.id === S.region);
    const tf = DATA.trade.filter(inScope);
    draw('tf-fly', { type: 'butterfly-v', categories: regs.map(r => r.name), categoryLabel: 'Region', caption: 'Import versus export instruments by region, £ millions',
      series: [{ name: 'Import', values: regs.map(r => m1(tf.filter(t => t.region === r.id && t.direction === 'Import').reduce((s, t) => s + t.gbp, 0))) },
               { name: 'Export', values: regs.map(r => m1(tf.filter(t => t.region === r.id && t.direction === 'Export').reduce((s, t) => s + t.gbp, 0))) }] }, ['Import', 'Export']);
    const types = ['Import letter of credit', 'Export letter of credit', 'Bank guarantee', 'Standby letter of credit', 'Documentary collection'];
    const sts = ['Issued', 'Documents presented', 'Amendment requested', 'Settled', 'Draft'];
    draw('tf-stack', { type: 'stacked-column', categories: sts, categoryLabel: 'Status', unit: '£m', caption: 'Instrument value by status and type, £ millions',
      series: types.map(ty => ({ name: ty, values: sts.map(s => m1(tf.filter(t => t.status === s && t.type === ty).reduce((a, t) => a + t.gbp, 0))) })) }, types);
  };
  P.trade.grid = {
    rows: () => DATA.trade.filter(inScope).sort((a, b) => a.expiry.localeCompare(b.expiry)),
    map: t => ({ date: t.expiry, payee: t.party, ref: t.id + ' · ' + t.type, type: t.status, amount: t.gbp }),
    open: t => openDrawer(t.type + ' ' + t.id, summary([['Status', t.status], ['Counterparty', t.party], ['Entity', ENT[t.entity].name], ['Direction', t.direction],
      ['Amount', ccyFull(t.ccy, t.amount)], ['GBP equivalent', gbpFull(t.gbp)], ['Issued', fmtDate(t.date)], ['Expiry', fmtDate(t.expiry)]]),
      t.status === 'Settled' ? [] : [{ label: 'Request an amendment', run: () => openModal({ title: 'Request an amendment to ' + t.id, body: 'Describe the change (for example a new expiry date or amount). HSBC Trade Services receives it as a service request.',
        confirm: 'Send amendment request', noteMin: 20, onConfirm: note => { t.status = 'Amendment requested'; S.tf[t.id] = { status: t.status }; save(); closeDrawer(); raiseRequest('Trade documents', 'Amendment to ' + t.id + ': ' + note.slice(0, 60), t.entity, true); rerender(); } }) }]),
    csv: () => [['Instrument', 'Type', 'Status', 'Entity', 'Counterparty', 'Currency', 'Amount', 'GBP', 'Expiry'], P.trade.grid.rows().map(t => [t.id, t.type, t.status, ENT[t.entity].name, t.party, t.ccy, t.amount, t.gbp, t.expiry])]
  };

  P.reports = function () {
    const idx = periodIdx();
    draw('rp-runs', { type: 'column', categories: idx.map(i => short(DAYS[i])), categoryLabel: 'Day', caption: 'Reports generated per day',
      series: [{ name: 'Reports', values: idx.map(i => DATA.reportRuns[i] + Object.keys(S.reports).filter(k => S.reports[k].ranOn === DAYS[i]).length) }] });
    const cats = capSlices([...new Set(DATA.reports.map(r => r.category))].map(c => [c, DATA.reports.filter(r => r.category === c).length]).sort((a, b) => b[1] - a[1]));
    draw('rp-cat', { type: 'pie', categories: cats.map(c => c[0]), series: [{ name: 'Reports', values: cats.map(c => c[1]) }], categoryLabel: 'Category',
      caption: 'Report catalogue by category, count' }, cats.map(c => c[0]));
  };
  function runReport(r) {
    const rows = r.category === 'Payments' ? DATA.payments.filter(inScope).map(p => [p.id, p.date, p.beneficiary, p.status, p.gbp]) :
      r.category === 'Risk' ? DATA.exceptions.filter(inScope).map(x => [x.id, x.date, x.type, x.status, x.over]) :
      r.category === 'Trade' ? DATA.trade.filter(inScope).map(t => [t.id, t.date, t.type, t.status, t.gbp]) :
      DATA.accounts.filter(inScope).map(a => [a.id, DATA.meta.asOf, ENT[a.entity].name, a.type, Math.round(a.balances[N - 1] * FX[a.ccy] * 100) / 100]);
    S.reports[r.id] = { ranOn: DATA.meta.asOf }; save();
    downloadCsv(r.id + '-' + r.name.toLowerCase().replace(/[^a-z0-9]+/g, '-') + '.csv', ['Id', 'Date', 'Name', 'Status or type', 'GBP'], rows);
    rerender();
  }
  const REPORT_LIST = {
    id: 'rp-list', size: 8,
    rows: () => DATA.reports,
    text: r => r.name + ' ' + r.category + ' ' + r.frequency + ' ' + r.id,
    sorts: [{ key: 'name', fn: (a, b) => a.name.localeCompare(b.name) }, { key: 'recent', fn: (a, b) => lastRun(b).localeCompare(lastRun(a)) }, { key: 'category', fn: (a, b) => a.category.localeCompare(b.category) || a.name.localeCompare(b.name) }],
    row: r => listRow(r.id, r.name, (S.reports[r.id] && S.reports[r.id].sched === false) || (!S.reports[r.id] || S.reports[r.id].sched === undefined) && !r.scheduled ? 'On demand' : 'Scheduled',
      r.category + ' · ' + r.frequency + ' · last run ' + short(lastRun(r)), r.format, initials(r.category)),
    open: id => { const r = DATA.reports.find(x => x.id === id); const sched = S.reports[id] && S.reports[id].sched !== undefined ? S.reports[id].sched : r.scheduled;
      openDrawer(r.name, summary([['Report', r.id], ['Category', r.category], ['Frequency', r.frequency], ['Format', r.format], ['Owner', r.owner], ['Last run', fmtDate(lastRun(r))], ['Delivery', sched ? 'Scheduled to your inbox' : 'On demand'], ['Scope', scopeLabel()]]),
        [{ label: 'Run and export now', run: () => runReport(r) }, { label: sched ? 'Stop the schedule' : 'Schedule it', run: () => { S.reports[id] = Object.assign(S.reports[id] || {}, { sched: !sched }); save(); closeDrawer(); toast(r.name + (sched ? ' is now on demand.' : ' is scheduled ' + r.frequency.toLowerCase() + '.'), 'ok'); rerender(); } }]); }
  };
  function lastRun(r) { return S.reports[r.id] && S.reports[r.id].ranOn ? S.reports[r.id].ranOn : r.date; }

  function raiseRequest(category, subject, entity, quiet) {
    const id = 'SR-' + (88000 + DATA.requests.length + 1 + Math.floor(Math.random() * 900));
    const r = { id: id, date: DATA.meta.asOf, category: category, entity: entity || 'E01', subject: subject, priority: 'Normal', status: 'Open', hours: 0,
      audit: [{ at: nowStamp(), by: 'Chief Executive Officer (you)', note: 'Request raised: ' + subject }] };
    DATA.requests.unshift(r); S.req.push(r); save();
    closeDrawer();
    toast('Service request ' + id + ' raised with HSBC. Track it under HSBC messages and service requests.', 'ok');
    if (!quiet) rerender();
    return r;
  }
  P.messages = function () {
    const idx = periodIdx();
    const sr = sampleIdx(idx);
    draw('ms-resp', { type: 'line', categories: sr.idx.map(i => short(DAYS[i])), categoryLabel: 'Day', caption: 'Average HSBC response time to your requests, hours' + everyNote(sr.step),
      series: [{ name: 'Hours', values: sr.idx.map(i => DATA.respHours[i]) }] });
    const req = DATA.requests.filter(r => inScope(r) && inPeriod(r.date));
    const cats = [...new Set(DATA.requests.map(r => r.category))];
    draw('ms-cat', { type: 'stacked-column', categories: cats, categoryLabel: 'Category', caption: 'Service requests by category and state, count',
      series: [{ name: 'Open', values: cats.map(c => req.filter(r => r.category === c && r.status !== 'Resolved').length) }, { name: 'Resolved', values: cats.map(c => req.filter(r => r.category === c && r.status === 'Resolved').length) }] }, ['Open', 'Resolved']);
    const unread = DATA.messages.filter(m => !m.read).length;
    setText('ms-unread', unread + ' unread');
  };
  const MSG_LIST = {
    id: 'ms-list', size: 6,
    rows: () => DATA.messages,
    text: m => m.subject + ' ' + m.from + ' ' + m.category,
    sorts: [{ key: 'recent', fn: (a, b) => b.date.localeCompare(a.date) }, { key: 'unread', fn: (a, b) => (a.read - b.read) || b.date.localeCompare(a.date) }],
    row: m => listRow(m.id, m.subject, m.read ? 'Read' : 'Unread', m.from + ' · ' + short(m.date), m.category, initials(m.from)),
    open: id => { const m = DATA.messages.find(x => x.id === id); m.read = true; S.msg[id] = true; save(); if (LISTS['ms-list']) LISTS['ms-list'].render(); P.messages();
      openDrawer(m.subject, summary([['From', m.from], ['Received', fmtDate(m.date)], ['Category', m.category]]) + '<p class="t-ed-body">' + esc(m.body) + '</p>',
        [{ label: 'Reply', run: () => openModal({ title: 'Reply to ' + m.from.split(',')[0], body: 'Your reply is sent through secure messaging (simulated).', confirm: 'Send reply', noteMin: 10,
          onConfirm: () => { closeDrawer(); toast('Reply sent to ' + m.from.split(',')[0] + '.', 'ok'); } }) }]); }
  };
  const REQ_LIST = {
    id: 'sr-list', size: 6,
    rows: () => DATA.requests.filter(inScope),
    text: r => r.subject + ' ' + r.category + ' ' + r.id + ' ' + r.status,
    sorts: [{ key: 'recent', fn: (a, b) => b.date.localeCompare(a.date) || b.id.localeCompare(a.id) }, { key: 'status', fn: (a, b) => a.status.localeCompare(b.status) }, { key: 'priority', fn: (a, b) => ['High', 'Normal', 'Low'].indexOf(a.priority) - ['High', 'Normal', 'Low'].indexOf(b.priority) }],
    row: r => listRow(r.id, r.subject, r.status, r.id + ' · ' + r.category + ' · ' + ENT[r.entity].name.replace('Northwind ', ''), r.priority + ' priority', initials(r.category)),
    open: id => { const r = DATA.requests.find(x => x.id === id);
      const upd = (status, note) => { const e = { at: nowStamp(), by: 'Chief Executive Officer (you)', note: note }; r.audit.push(e); if (status) r.status = status;
        const u = S.reqUpd[r.id] || { audit: [] }; u.audit.push(e); if (status) u.status = status; S.reqUpd[r.id] = u; save(); closeDrawer(); rerender(); };
      openDrawer('Service request ' + r.id, summary([['Subject', r.subject], ['Category', r.category], ['Entity', ENT[r.entity].name], ['Priority', r.priority], ['Status', r.status], ['Opened', fmtDate(r.date)]]) + timeline(r.audit),
        r.status === 'Resolved' ? [] : [{ label: 'Add an update', run: () => openModal({ title: 'Update ' + r.id, body: 'Add information for HSBC Client Service.', confirm: 'Send update', noteMin: 10,
          onConfirm: note => { upd(r.status === 'Awaiting you' ? 'In progress' : null, note); toast('Update added to ' + r.id + '.', 'ok'); } }) },
          { label: 'Close request', run: () => openModal({ title: 'Close ' + r.id, body: 'Tell HSBC why the request can close.', confirm: 'Close request', noteMin: 10,
            onConfirm: note => { upd('Resolved', 'Closed by client. ' + note); toast(r.id + ' closed.', 'ok'); } }) }]); }
  };

  /* new service request — a validated form in the drawer (Input-fields + native select) */
  function newRequestForm() {
    const opts = (arr, sel) => arr.map(v => '<option' + (v === sel ? ' selected' : '') + '>' + esc(v) + '</option>').join('');
    const ents = DATA.entities.map(e => '<option value="' + e.id + '"' + ((S.entity === e.id) ? ' selected' : '') + '>' + esc(e.name) + '</option>').join('');
    openDrawer('New service request', '<form id="sr-form" class="ceo-stack" novalidate>' +
      field('sr-cat', 'Category', '<select id="sr-cat" class="t-cm-input">' + opts(['Payments investigation', 'Account maintenance', 'Mandate change', 'Statement request', 'Trade documents', 'Digital access'], '') + '</select>') +
      field('sr-ent', 'Entity', '<select id="sr-ent" class="t-cm-input">' + ents + '</select>') +
      field('sr-sub', 'Subject', '<input id="sr-sub" type="text" autocomplete="off" aria-describedby="sr-sub-err">', 'At least 8 characters.') +
      field('sr-pri', 'Priority', '<select id="sr-pri" class="t-cm-input">' + opts(['High', 'Normal', 'Low'], 'Normal') + '</select>') +
      '</form>', [{ label: 'Send request', keep: true, run: () => {
        const sub = document.getElementById('sr-sub');
        const ok = sub.value.trim().length >= 8;
        const f = sub.closest('.field'); f.classList.toggle('is-error', !ok);
        document.getElementById('sr-sub-err').hidden = ok;
        if (!ok) { sub.setAttribute('aria-invalid', 'true'); sub.focus(); return; }
        sub.removeAttribute('aria-invalid');
        const r = raiseRequest(document.getElementById('sr-cat').value, sub.value.trim(), document.getElementById('sr-ent').value);
        r.priority = document.getElementById('sr-pri').value; save(); rerender();
      } }]);
  }
  function field(id, label, control, help) {
    return '<div class="cn-input-fields"><div class="field"><div class="lbl"><label for="' + id + '">' + label + '</label></div>' + (help ? '<p class="help-text">' + help + '</p>' : '') +
      '<div class="box">' + control + '</div>' + (id === 'sr-sub' ? '<div class="err-msg" id="sr-sub-err" hidden><span class="ic" aria-hidden="true"><svg class="icn" viewBox="0 0 18 18"><use href="#ic-error"/></svg></span><p>Enter a subject of at least 8 characters.</p></div>' : '') + '</div></div>';
  }

  P.settings = function () {
    const ap = DATA.approvers;
    draw('st-limits', { type: 'bullet', categories: ap.map(a => a.name.replace('Regional CFO, ', 'CFO ')), categoryLabel: 'Approver', format: 'percent', ranges: [50, 80, 100],
      caption: 'Approval limit used this month by approver, per cent of limit', series: [{ name: 'Used', values: ap.map(a => Math.round(a.used / a.limit * 1000) / 10) }, { name: 'Review point', values: ap.map(() => 80) }] });
    const idx = periodIdx();
    draw('st-logins', { type: 'spark', categories: idx.map(i => short(DAYS[i])), caption: 'Your sign-ins per day over the period', series: [{ name: 'Sign-ins', values: idx.map(i => DATA.logins[i]) }] });
    document.querySelectorAll('[data-notify]').forEach(i => { i.checked = !!S.notify[i.getAttribute('data-notify')]; });
  };

  /* ---------- wiring common to every page ---------- */
  function syncFilters() {
    document.querySelectorAll('[data-filter]').forEach(dd => {
      const k = dd.getAttribute('data-filter'), v = S[k];
      const opts = [...dd.querySelectorAll('[role=option]')];
      opts.forEach(o => o.setAttribute('aria-selected', String(o.getAttribute('data-value') === v)));
      const sel = opts.find(o => o.getAttribute('data-value') === v) || opts[0];
      dd.querySelector('.ddval').textContent = sel.firstChild.textContent.trim();
    });
    document.querySelectorAll('[data-period-seg] button').forEach(b => b.setAttribute('aria-pressed', String(+b.getAttribute('data-value') === S.period)));
    setText('scope-note', scopeLabel());
  }
  function rerender() {
    syncFilters();
    if (P[PAGE]) P[PAGE]();
    refreshGrid();
    Object.keys(LISTS).forEach(k => LISTS[k].render());
  }
  function setFilter(k, v) { S[k] = v; if (k === 'entity' && v !== 'all') S.region = 'all'; save(); syncUrl(); rerender(); }

  /* Dropdown mechanics (the Dropdown snippet's own wire(), one per .dd) + a change hook */
  function wireDropdown(dd) {
    const trig = dd.querySelector('.trigger'), menu = dd.querySelector('.menu'), opts = [...menu.querySelectorAll('[role=option]')];
    function open(o) { menu.setAttribute('data-open', String(o)); trig.setAttribute('aria-expanded', String(o));
      if (o) { const sel = opts.find(x => x.getAttribute('aria-selected') === 'true') || opts[0]; sel.focus(); } }
    function choose(o) { open(false); trig.focus(); setFilter(dd.getAttribute('data-filter'), o.getAttribute('data-value')); }
    trig.addEventListener('click', () => open(menu.getAttribute('data-open') !== 'true'));
    trig.addEventListener('keydown', e => { if (['ArrowDown', 'Enter', ' '].includes(e.key)) { e.preventDefault(); open(true); } });
    opts.forEach(o => { o.addEventListener('click', () => choose(o));
      o.addEventListener('keydown', e => { const i = opts.indexOf(o);
        if (e.key === 'ArrowDown') { e.preventDefault(); opts[(i + 1) % opts.length].focus(); }
        else if (e.key === 'ArrowUp') { e.preventDefault(); opts[(i - 1 + opts.length) % opts.length].focus(); }
        else if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); choose(o); }
        else if (e.key === 'Escape') { open(false); trig.focus(); } }); });
  }

  function init() {
    applyTheme(); carryParams(); syncFilters();
    document.querySelectorAll('.dd[data-filter]').forEach(wireDropdown);
    document.addEventListener('click', e => { if (!e.target.closest('.dd')) document.querySelectorAll('.dd[data-filter]').forEach(dd => {
      dd.querySelector('.menu').setAttribute('data-open', 'false'); dd.querySelector('.trigger').setAttribute('aria-expanded', 'false'); }); });
    document.querySelectorAll('[data-theme-seg] button').forEach(b => b.addEventListener('click', () => { S.theme = b.getAttribute('data-value'); save(); applyTheme(); toast((S.theme === 'dark' ? 'Dark' : 'Light') + ' theme on. It stays on across pages.', 'info'); }));
    document.querySelectorAll('[data-period-seg] button').forEach(b => b.addEventListener('click', () => setFilter('period', +b.getAttribute('data-value'))));
    document.querySelectorAll('[data-action="reset-filters"]').forEach(b => b.addEventListener('click', () => { S.entity = 'all'; S.region = 'all'; S.period = 30; save(); syncUrl(); rerender(); toast('Filters reset to all entities, last 30 days.', 'info'); }));
    document.querySelectorAll('[data-action="export"]').forEach(b => b.addEventListener('click', () => {
      const g = GRID && GRID.csv ? GRID.csv() : PAGE === 'reports' ? [['Report', 'Name', 'Category', 'Frequency', 'Format', 'Last run'], DATA.reports.map(r => [r.id, r.name, r.category, r.frequency, r.format, lastRun(r)])] :
        PAGE === 'messages' ? [['Request', 'Date', 'Category', 'Subject', 'Status', 'Priority'], DATA.requests.filter(inScope).map(r => [r.id, r.date, r.category, r.subject, r.status, r.priority])] :
        overviewCsv();
      downloadCsv(PAGE + '-' + DATA.meta.asOf + '.csv', g[0], g[1]);
    }));
    /* drawer + modal + overlay keyboard (Drawer / Modals snippet mechanics) */
    document.getElementById('close').addEventListener('click', closeDrawer);
    document.getElementById('scrim').addEventListener('click', closeDrawer);
    document.getElementById('dfoot').addEventListener('click', e => {
      if (e.target.closest('[data-drawer-close]')) { closeDrawer(); return; }
      const b = e.target.closest('[data-drawer-act]'); if (!b) return;
      const a = e.currentTarget.__acts[+b.getAttribute('data-drawer-act')]; if (a) a.run();
    });
    document.getElementById('mclose').addEventListener('click', closeModal);
    document.getElementById('mcancel').addEventListener('click', closeModal);
    document.getElementById('mconfirm').addEventListener('click', confirmModal);
    document.addEventListener('keydown', e => {
      const ov = document.getElementById('overlay'), sheet = document.getElementById('sheet');
      const box = ov.classList.contains('open') ? ov.querySelector('.dialog') : sheet.classList.contains('open') ? sheet : null;
      if (!box) return;
      if (e.key === 'Escape') { e.preventDefault(); if (box === sheet) closeDrawer(); else closeModal(); return; }
      if (e.key === 'Tab') { const f = [...box.querySelectorAll('button,[href],input,textarea,select')].filter(el => !el.disabled && el.offsetParent !== null);
        if (!f.length) return; const a = f[0], z = f[f.length - 1];
        if (e.shiftKey && document.activeElement === a) { e.preventDefault(); z.focus(); } else if (!e.shiftKey && document.activeElement === z) { e.preventDefault(); a.focus(); } }
    });
    /* decision cards: rows go to the record */
    document.addEventListener('click', e => { const b = e.target.closest('button[data-goto]'); if (!b) return; location.href = withParams(b.getAttribute('data-goto')); });
    /* appbar: search opens a cross-record finder in the drawer; profile opens settings */
    const sb = document.querySelector('.sh-appbar [aria-label="Search"]');
    if (sb) sb.addEventListener('click', openFinder);
    const pb = document.querySelector('.sh-appbar [aria-label="Your profile"]');
    if (pb) pb.addEventListener('click', () => { location.href = withParams('settings.html'); });
    /* the exposure charts drill through to positions and limits */
    [['ov-region', 'region'], ['ov-ccy', 'ccy']].forEach(pair => {
      const fig = document.getElementById(pair[0]); if (!fig) return;
      const go = t => { const m = t.closest('rect.dv-series'); if (!m) return; const lab = m.getAttribute('aria-label') || '';
        let dest = null;
        if (pair[1] === 'region') { const r = DATA.regions.find(x => lab.indexOf(x.name) >= 0); if (r) dest = 'risk.html?tab=positions&region=' + r.id; }
        else { const c = Object.keys(FX).find(x => new RegExp('(^|\\W)' + x + '(\\W|$)').test(lab)); if (c) dest = 'risk.html?tab=positions&ccy=' + c; }
        if (dest) location.href = withParams(dest); };
      fig.addEventListener('click', e => go(e.target));
      fig.addEventListener('keydown', e => { if (e.key === 'Enter') go(e.target); });
    });
    if (PAGE === 'messages') { listEngine(MSG_LIST); listEngine(REQ_LIST);
      const nb = document.querySelector('[data-action="new-request"]'); if (nb) nb.addEventListener('click', newRequestForm); }
    if (PAGE === 'reports') listEngine(REPORT_LIST);
    if (PAGE === 'settings') {
      document.querySelectorAll('[data-notify]').forEach(i => i.addEventListener('change', () => { S.notify[i.getAttribute('data-notify')] = i.checked; save();
        toast((i.checked ? 'On: ' : 'Off: ') + i.closest('.field').querySelector('label').textContent.trim() + '.', 'info'); }));
      const rb = document.querySelector('[data-action="reset-prototype"]');
      if (rb) rb.addEventListener('click', () => openModal({ title: 'Reset the prototype', body: 'Clears every simulated approval, acknowledgement, request, saved filter and theme on this device.', confirm: 'Reset everything', noteMin: 0,
        onConfirm: () => { try { localStorage.removeItem(LS); } catch (e) { /* nothing stored */ } location.href = 'settings.html'; } }));
    }
    /* tabs on the risk page switch the one grid between exceptions and positions */
    document.querySelectorAll('.tablist [role=tab]').forEach(t => t.addEventListener('click', () => selectTab(t)));
    document.querySelectorAll('.tablist').forEach(tl => tl.addEventListener('keydown', e => {
      const tabs = [...tl.querySelectorAll('[role=tab]')], i = tabs.indexOf(document.activeElement); if (i < 0) return;
      if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') { e.preventDefault(); const n = tabs[(i + (e.key === 'ArrowRight' ? 1 : tabs.length - 1)) % tabs.length]; n.focus(); selectTab(n); }
    }));
    if (P[PAGE]) P[PAGE]();
  }
  function overviewCsv() {
    const c = cashSeries(), h = headroomSeries(), rows = [];
    periodIdx().forEach(i => rows.push([DAYS[i], Math.round(c[i]), Math.round(h[i]), Math.round(c[i] + h[i])]));
    return [['Date', 'Cash GBP', 'Funding headroom GBP', 'Available liquidity GBP'], rows];
  }
  function withParams(href) {
    const u = new URL(href, location.href);
    if (S.entity !== 'all' && !u.searchParams.has('entity')) u.searchParams.set('entity', S.entity);
    if (S.region !== 'all' && !u.searchParams.has('region')) u.searchParams.set('region', S.region);
    if (S.period !== 30) u.searchParams.set('period', S.period);
    return u.pathname.split('/').pop() + u.search;
  }
  function selectTab(t) {
    const tl = t.closest('.tablist');
    tl.querySelectorAll('[role=tab]').forEach(x => { const on = x === t; x.setAttribute('aria-selected', String(on)); x.tabIndex = on ? 0 : -1; });
    const ind = tl.querySelector('.indicator'); if (ind) { ind.style.left = t.offsetLeft + 'px'; ind.style.width = t.offsetWidth + 'px'; ind.style.opacity = '1'; }
    const v = t.getAttribute('data-tab');
    if (PAGE === 'risk') { S.tab.risk = v; save(); GRID = P.risk.gridFor(v); relabelGrid(v); if (typeof state !== 'undefined') { state.page = 1; } refreshGrid(); }
  }
  function relabelGrid(tab) {
    const L = tab === 'positions' ? ['Maturity', 'Counterparty', 'Position · entity', 'Type · region · currency', 'Exposure (GBP)', 'Positions and limits'] :
      ['Raised', 'Counterparty', 'Exception', 'Severity · status', 'Over limit (GBP)', 'Risk exceptions'];
    const k = ['date', 'payee', 'ref', 'type', 'amount'];
    k.forEach((key, i) => { const l = document.querySelector('#tbl th[data-key="' + key + '"] .lbl'); if (l) l.textContent = L[i]; });
    setText('dgTitle', L[5]);
    const panel = document.getElementById('rk-panel'); if (panel) panel.setAttribute('aria-labelledby', 'rk-tab-' + tab);
  }

  function openFinder() {
    openDrawer('Find a record', '<div class="cn-search-field"><div class="search boxed"><span class="mag" aria-hidden="true"><svg viewBox="0 0 18 18" aria-hidden="true"><use href="#dg-search"/></svg></span>' +
      '<input type="search" id="finder-q" aria-label="Search payments, exceptions, instruments and requests" placeholder="Search by id, name or counterparty"></div></div>' +
      '<p class="t-cm-caption" id="finder-count" aria-live="polite">Type at least two characters.</p><div class="cn-list-items"><ul class="list" id="finder-list"></ul></div>', []);
    const q = document.getElementById('finder-q'), ul = document.getElementById('finder-list');
    q.addEventListener('input', () => {
      const t = q.value.trim().toLowerCase(); if (t.length < 2) { ul.innerHTML = ''; setText('finder-count', 'Type at least two characters.'); return; }
      const hits = [].concat(
        DATA.payments.filter(p => (p.id + p.beneficiary).toLowerCase().includes(t)).map(p => listRowLink('payments.html', p.id, p.id + ' · ' + p.beneficiary, p.status, 'Payment · ' + short(p.date), gbpM(p.gbp), 'PY')),
        DATA.exceptions.filter(x => (x.id + x.counterparty + x.type).toLowerCase().includes(t)).map(x => listRowLink('risk.html', x.id, x.id + ' · ' + x.type, x.status, x.counterparty, gbpM(x.over), 'RK')),
        DATA.trade.filter(x => (x.id + x.party).toLowerCase().includes(t)).map(x => listRowLink('trade.html', x.id, x.id + ' · ' + x.party, x.status, x.type, gbpM(x.gbp), 'TF')),
        DATA.requests.filter(x => (x.id + x.subject).toLowerCase().includes(t)).map(x => listRowLink('messages.html', x.id, x.id + ' · ' + x.subject, x.status, x.category, x.priority, 'SR'))).slice(0, 12);
      ul.innerHTML = hits.join(''); setText('finder-count', hits.length ? hits.length + ' matches (first 12)' : 'No records match.');
    });
  }

  /* hooks the Data-grid script and the post-load step call back into */
  window.__ceoInitGrid = function () {
    if (PAGE === 'risk') { GRID = P.risk.gridFor(riskTab()); } else if (P[PAGE] && P[PAGE].grid) { GRID = P[PAGE].grid; }
    if (!GRID) return;
    const rows = gridRows(); window.CEO_ROWS.length = 0; rows.forEach(r => window.CEO_ROWS.push(r));
  };
  window.__ceoAfterGrid = function () {
    if (!GRID || typeof state === 'undefined') return;
    const key = PAGE + ':grid' + (PAGE === 'risk' ? ':' + riskTab() : '');
    const g = S.grid[key];
    if (g) { state.sortKey = g.sortKey || null; state.sortDir = g.sortDir || 'none'; state.pageSize = g.pageSize || 8; state.page = g.page || 1;
      const pp = document.getElementById('pp'); if (pp) pp.value = String(state.pageSize);
      document.querySelectorAll('#tbl thead tr.cols th[data-key]').forEach(th => th.setAttribute('aria-sort', th.getAttribute('data-key') === state.sortKey ? state.sortDir : 'none')); }
    else if (PAGE === 'accounts') { state.pageSize = 24; const pp = document.getElementById('pp'); if (pp) pp.value = '24'; }  /* 220 rows: the pager lists every page, so 24 a page keeps it inside the tile */
    if (Q.get('ccy') && PAGE === 'risk') { state.filters = [{ key: null, term: Q.get('ccy') }]; renderChips(); }
    window.__ceoGridRender = function () { render(); };
    render();
    const persist = () => setTimeout(() => { S.grid[PAGE + ':grid' + (PAGE === 'risk' ? ':' + riskTab() : '')] = { sortKey: state.sortKey, sortDir: state.sortDir, pageSize: state.pageSize, page: state.page }; save(); }, 0);
    const dg = document.getElementById('dg');
    dg.addEventListener('click', persist); dg.addEventListener('change', persist); dg.addEventListener('keydown', persist);
    /* row -> detail view: click a cell, or press Enter on a non-editable body cell */
    const openRow = td => { const tr = td.closest('tr[data-id]'); if (!tr) return; const rec = gridRecord(tr);
      returnSel = '#tbody tr[data-id="' + tr.getAttribute('data-id') + '"] td:nth-child(' + (td.cellIndex + 1) + ')'; if (rec) GRID.open(rec); };
    dg.addEventListener('click', e => { const td = e.target.closest('tbody td'); if (td && !td.classList.contains('sel') && !td.classList.contains('edit') && !td.classList.contains('dg-empty')) openRow(td); });
    dg.addEventListener('keydown', e => { if (e.key !== 'Enter') return; const td = e.target.closest('tbody td'); if (td && !td.classList.contains('sel') && !td.classList.contains('edit')) openRow(td); });
    const open = Q.get('open');
    if (open) {
      const ix = window.CEO_ROWS.findIndex(r => r.__rec.id === open || r.__rec.ref === open);
      if (ix >= 0) { const rec = window.CEO_ROWS[ix].__rec; state.page = Math.floor(ix / state.pageSize) + 1; render(); GRID.open(rec); }
    }
    const sel = document.querySelector('[data-action="open-selected"]');
    if (sel) sel.addEventListener('click', () => { const id = [...state.sel][0]; const r = window.CEO_ROWS.find(x => x.id === id);
      if (r) GRID.open(r.__rec); else toast('Select a row with its checkbox first.', 'info'); });
  };
  window.__ceoInitGrid();
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
  window.addEventListener('load', () => {
    if (PAGE === 'risk') { const t = document.querySelector('.tablist [data-tab="' + riskTab() + '"]'); if (t) { selectTab(t); } }
    if (Q.get('open') && !GRID) { const l = LISTS['sr-list'] || LISTS['ms-list'] || LISTS['rp-list']; if (l && l.cfg.rows().some(r => r.id === Q.get('open'))) l.cfg.open(Q.get('open')); }
  });
}());
