/* CEO APP — RECORD LISTS, TABS, METERS, CARDS and the ten VIEWS. Every figure is derived from
   CEO_DATA under the shared filters (entity · region · currency · date range · search). */
(function () {
  'use strict';
  var D = window.CEO_DATA, APP = window.CEO_APP, S = APP.state;
  var $ = function (id) { return document.getElementById(id); };
  var PAGE = 8;

  /* ------------------------------------------------------------------ workflow overlays on the seeded records */
  APP.pay = function (p) { var w = S.wf.pay[p.id]; return w ? w.status : p.status; };
  APP.payAudit = function (p) { var base = [{ when: p.created + ' 09:00', text: 'Payment created by ' + p.initiator, who: 'Created', tone: 'inf' }];
    if (p.status === 'Released') { base.push({ when: p.valueDate + ' 11:30', text: 'Released to ' + p.channel, who: 'Released', tone: 'ok' }); }
    return base.concat((S.wf.pay[p.id] || {}).audit || []); };
  APP.exc = function (x) { var w = S.wf.exc[x.id]; return w ? w.status : x.status; };
  APP.excAudit = function (x) { return [{ when: x.detected + ' 07:15', text: 'Detected by the overnight limit run', who: 'Detected', tone: 'warn' }].concat((S.wf.exc[x.id] || {}).audit || []); };
  APP.msgRead = function (m) { var w = S.wf.msg[m.id]; return w && w.read != null ? w.read : m.read; };
  APP.srs = function () { return D.serviceRequests.concat(S.wf.srNew || []).map(function (r) { var u = S.wf.srUpd[r.id]; if (!u) { return r; }
    var c = JSON.parse(JSON.stringify(r)); c.status = u.status || c.status; c.updates = c.updates.concat(u.updates || []); return c; }); };
  function audit(bucket, id, status, text, note, tone) {
    var w = S.wf[bucket][id] = S.wf[bucket][id] || { audit: [] };
    w.status = status; w.audit.push({ when: APP.now(), text: text, who: 'You (CEO)', note: note || '', tone: tone || 'ok' }); APP.save();
  }

  /* ------------------------------------------------------------------ record lists (Table · List-items · Pagination · Dropdown) */
  APP.records = function (host, cfg) {
    var r = host.__rec;
    if (!r) {
      host.textContent = '';
      r = host.__rec = { cfg: cfg };
      var head = APP.el('div', 'ceo-split');
      r.h = APP.el('h3', 't-cm-section-label', cfg.title); head.appendChild(r.h);
      var tools = APP.el('div', 'ceo-tools'); r.count = APP.el('span', 't-cm-caption'); r.count.setAttribute('aria-live', 'polite'); tools.appendChild(r.count);
      if (cfg.sorts) {
        var cur = S.sort[cfg.id] || cfg.sorts[0][0];
        tools.appendChild(APP.dropdown('Sort by', cfg.sorts, cur, function (v) { S.sort[cfg.id] = v; S.page[cfg.id] = 1; APP.save(); APP.records(host, r.cfg); }));
      }
      head.appendChild(tools);
      r.body = APP.el('div'); r.pager = APP.el('div', 'cn-pagination');
      var st = APP.el('div', 'ceo-stack'); st.appendChild(head); st.appendChild(r.body); st.appendChild(r.pager); host.appendChild(st);
      r.pager.addEventListener('click', function (e) {
        var a = e.target.closest('a[data-page], button.ctrl'); if (!a || a.disabled) { return; } e.preventDefault();
        var p = S.page[cfg.id] || 1; p = a.hasAttribute('data-page') ? +a.getAttribute('data-page') : (/Previous/.test(a.getAttribute('aria-label')) ? p - 1 : p + 1);
        S.page[cfg.id] = p; APP.save(); APP.records(host, r.cfg);
        var f = r.pager.querySelector('[aria-current="page"]'); if (f) { f.focus(); }
      });
      r.body.addEventListener('click', function (e) {
        var o = e.target.closest('[data-open]'); if (!o) { return; } e.preventDefault();
        var row = r.rows.filter(function (x) { return String(x[r.cfg.key || 'id']) === o.getAttribute('data-open'); })[0];
        if (row) { r.cfg.open(row, o); }
      });
    }
    r.cfg = cfg;
    var rows = cfg.rows().slice();
    var sk = (S.sort[cfg.id] || (cfg.sorts ? cfg.sorts[0][0] : '')).split(':');
    if (sk[0]) { var k = sk[0], dir = sk[1] === 'desc' ? -1 : 1;
      rows.sort(function (a, b) { var x = a[k], y = b[k]; if (typeof x === 'number' && typeof y === 'number') { return (x - y) * dir; } return String(x).localeCompare(String(y)) * dir; }); }
    r.rows = rows;
    var pages = Math.max(1, Math.ceil(rows.length / PAGE)), page = Math.min(Math.max(1, S.page[cfg.id] || 1), pages);
    S.page[cfg.id] = page;
    var slice = rows.slice((page - 1) * PAGE, page * PAGE);
    r.count.textContent = rows.length ? ((page - 1) * PAGE + 1) + '–' + ((page - 1) * PAGE + slice.length) + ' of ' + rows.length + ' ' + cfg.noun : 'No ' + cfg.noun;
    r.body.textContent = '';
    if (!rows.length) {
      r.body.appendChild(APP.empty('No ' + cfg.noun + ' match', 'Nothing matches the filters and search in view. Remove a filter or widen the date range.',
        (S.filters.length || S.q) ? { label: 'Clear all filters', onClick: APP.clearFilters } : null));
    } else if (S.recView === 'cards' && cfg.card) {
      var ul = APP.tpl('list'); APP.reid(ul); ul.removeAttribute('id');
      var proto = ul.querySelector('li'); ul.textContent = '';
      slice.forEach(function (row) { var c = cfg.card(row), li = proto.cloneNode(true), b = li.querySelector('button.row');
        b.setAttribute('data-open', String(row[cfg.key || 'id'])); b.setAttribute('aria-label', c.title + ', ' + (c.status ? c.status[1] + ', ' : '') + c.desc + ', ' + c.amount);
        var av = b.querySelector('.avatar'); av.textContent = c.initials; av.setAttribute('aria-label', c.avatar || c.title);
        b.querySelector('.title').textContent = c.title;
        var s = b.querySelector('.status'); if (c.status && c.status[0] !== 'neu') { s.className = 'status ' + c.status[0]; s.lastChild.textContent = c.status[1]; } else { s.remove(); }   /* the row status has no neutral form: a neutral state shows none */
        b.querySelector('.desc').textContent = c.desc; b.querySelector('.amount').textContent = c.amount; ul.appendChild(li); });
      r.body.appendChild(APP.scope('cn-list-items', ul));
    } else {
      var sc = APP.tpl('table'); APP.reid(sc); sc.setAttribute('aria-label', cfg.title + ', scrollable');
      var t = sc.querySelector('table'); t.removeAttribute('id');
      var capEl = t.querySelector('caption'), sub = capEl.querySelector('.sub'); capEl.firstChild.textContent = cfg.title; sub.textContent = cfg.sub ? cfg.sub() : '';
      var htr = t.querySelector('thead tr'); htr.textContent = '';
      cfg.cols.forEach(function (c) { var th = APP.el('th', c.num ? 'num' : '', c.label); th.setAttribute('scope', 'col'); htr.appendChild(th); });
      var tb = t.querySelector('tbody'); tb.textContent = '';
      slice.forEach(function (row) { var tr = document.createElement('tr');
        cfg.cols.forEach(function (c, i) {
          var cell = document.createElement(i === 0 ? 'th' : 'td'); if (i === 0) { cell.setAttribute('scope', 'row'); cell.setAttribute('data-first', ''); }
          cell.setAttribute('data-label', c.label); if (c.num) { cell.className = 'num'; }
          APP.statForm = 'cell'; var v = APP.el('span', 'v'), val = c.v(row); APP.statForm = 'chip';
          if (i === 0) { var a = APP.el('a', 'lnk', val); a.href = '#'; a.setAttribute('data-open', String(row[cfg.key || 'id'])); v.appendChild(APP.scope('cn-links', a, 'span')); }
          else if (val && val.nodeType) { v.appendChild(val); } else { v.textContent = val == null ? '—' : val; }
          cell.appendChild(v); tr.appendChild(cell); });
        tb.appendChild(tr); });
      r.body.appendChild(APP.scope('cn-table', sc));
    }
    /* pagination — rebuilt from the component's own items */
    r.pager.textContent = '';
    if (pages > 1) {
      var nav = APP.tpl('pager'); nav.setAttribute('aria-label', cfg.title + ', pages');
      var ulp = nav.querySelector('ul'), lis = [].slice.call(ulp.children);
      var prev = lis[0].cloneNode(true), next = lis[lis.length - 1].cloneNode(true), link = lis[1].cloneNode(true), ell = ulp.querySelector('.ellipsis').parentNode.cloneNode(true);
      ulp.textContent = '';
      prev.querySelector('button').disabled = page === 1; prev.querySelector('button').type = 'button'; ulp.appendChild(prev);
      var shown = [];
      for (var p = 1; p <= pages; p++) { if (p === 1 || p === pages || Math.abs(p - page) <= 1) { shown.push(p); } }
      shown.forEach(function (p, i) { if (i && p - shown[i - 1] > 1) { ulp.appendChild(ell.cloneNode(true)); }
        var li = link.cloneNode(true), a = li.querySelector('a'); a.textContent = String(p); a.setAttribute('data-page', String(p)); a.href = '#';
        if (p === page) { a.setAttribute('aria-current', 'page'); a.setAttribute('aria-label', 'Page ' + p + ', current page'); } else { a.removeAttribute('aria-current'); a.setAttribute('aria-label', 'Page ' + p); }
        ulp.appendChild(li); });
      next.querySelector('button').disabled = page === pages; next.querySelector('button').type = 'button'; ulp.appendChild(next);
      r.pager.appendChild(nav);
    }
    if (cfg.primary) { APP.setResult(rows.length, cfg.total ? cfg.total() : rows.length, cfg.noun); }
    return r;
  };

  /* ------------------------------------------------------------------ tabs */
  APP.tabs = function (host, tabs, key) {
    var t = host.__tabs;
    if (!t) {
      var el = APP.tpl('tabs'); APP.reid(el);
      var list = el.querySelector('.tablist'), proto = list.querySelector('.tab'), pproto = el.querySelector('.panel'), ind = list.querySelector('.indicator');
      list.setAttribute('aria-label', tabs.label);
      [].slice.call(list.querySelectorAll('.tab')).forEach(function (b) { b.remove(); }); [].slice.call(el.querySelectorAll('.panel')).forEach(function (p) { p.remove(); });
      var ov = list.querySelector('.overflow');
      t = host.__tabs = { el: el, list: list, ind: ind, btns: [], panels: [] };
      tabs.items.forEach(function (it, i) {
        var b = proto.cloneNode(true), p = pproto.cloneNode(false);
        b.id = 'tab-' + key + '-' + i; p.id = 'panel-' + key + '-' + i; b.setAttribute('aria-controls', p.id); p.setAttribute('aria-labelledby', b.id);
        b.removeAttribute('disabled'); b.textContent = it.label; list.insertBefore(b, ov);
        el.appendChild(p); t.btns.push(b); t.panels.push(p);
      });
      function select(i, focus) { S.tabs[key] = i; APP.save();
        t.btns.forEach(function (b, j) { b.setAttribute('aria-selected', String(i === j)); b.tabIndex = i === j ? 0 : -1; t.panels[j].hidden = i !== j; });
        if (focus) { t.btns[i].focus(); } place(); tabs.onSelect(i); }
      function place() { var b = t.btns[S.tabs[key] || 0]; if (!b || !b.offsetWidth) { return; } ind.style.opacity = '1'; ind.style.left = b.offsetLeft + 'px'; ind.style.width = b.offsetWidth + 'px'; }
      t.place = place; t.select = select;
      list.addEventListener('click', function (e) { var b = e.target.closest('.tab'); if (b) { select(t.btns.indexOf(b)); } });
      list.addEventListener('keydown', function (e) { var i = t.btns.indexOf(document.activeElement); if (i < 0) { return; }
        var n = e.key === 'ArrowRight' ? (i + 1) % t.btns.length : e.key === 'ArrowLeft' ? (i - 1 + t.btns.length) % t.btns.length : e.key === 'Home' ? 0 : e.key === 'End' ? t.btns.length - 1 : null;
        if (n !== null) { e.preventDefault(); select(n, true); } });
      host.textContent = ''; host.appendChild(APP.scope('cn-tabs', el));
      t.btns.forEach(function (b, j) { b.setAttribute('aria-selected', String((S.tabs[key] || 0) === j)); b.tabIndex = (S.tabs[key] || 0) === j ? 0 : -1; t.panels[j].hidden = (S.tabs[key] || 0) !== j; });
    }
    tabs.items.forEach(function (it, i) { t.btns[i].textContent = it.label; });
    requestAnimationFrame(t.place);
    return t;
  };

  /* ------------------------------------------------------------------ limits meter */
  APP.meter = function (host, l) {
    host.textContent = '';
    var m = APP.tpl('limits'); APP.reid(m);
    var over = l.usedGbp > l.limitGbp, left = l.limitGbp - l.usedGbp, kind = l.status === 'Breach' ? 'err' : l.status === 'Approaching' ? 'warn' : 'ok';
    m.querySelector('.lim-label').textContent = l.name;
    var chip = m.querySelector('.chip'); chip.className = 'chip ' + kind; chip.lastElementChild.textContent = l.status + ' · ' + l.pct + '% used';
    var amt = m.querySelector('.amount').children; amt[0].textContent = '£'; amt[1].textContent = APP.num(Math.abs(left) / 1e6, 1) + 'm';
    m.querySelector('.lim-verdict').textContent = over ? 'Over the limit' : 'Left under the limit';
    var tr = m.querySelector('.pb-track'); tr.setAttribute('aria-valuenow', String(Math.round(Math.min(l.usedGbp, l.limitGbp))));
    tr.setAttribute('aria-valuemax', String(Math.round(l.limitGbp)));
    tr.setAttribute('aria-valuetext', APP.gbpc(l.usedGbp) + ' used of a ' + APP.gbpc(l.limitGbp) + ' limit, ' + (over ? APP.gbpc(-left) + ' over' : APP.gbpc(left) + ' left'));
    m.querySelector('.pb-fill').style.width = Math.min(100, l.usedGbp / l.limitGbp * 100).toFixed(2) + '%';
    var keys = m.querySelectorAll('.lim-key');
    keys[0].firstChild.nextSibling.textContent = 'Used '; keys[0].querySelector('.v').textContent = APP.gbpc(l.usedGbp);
    keys[1].firstChild.nextSibling.textContent = 'Limit '; keys[1].querySelector('.v').textContent = APP.gbpc(l.limitGbp);
    host.appendChild(APP.scope('cn-limits-meter', m));
    return m;
  };

  /* ------------------------------------------------------------------ decision card (Cards · action) */
  APP.card = function (host, o) {
    host.textContent = '';
    var c = APP.tpl('card'), svg = c.querySelector('.ic svg');
    svg.removeAttribute('data-icon'); svg.innerHTML = '<use href="#' + o.icon + '"/>';
    c.querySelector('h3').textContent = o.title; var p = c.querySelector('.body p'); p.textContent = o.text;
    if (o.items && o.items.length) {
      var ul = APP.el('ul'); ul.className = 'ceo-stack';
      o.items.forEach(function (it) { var li = APP.el('li'), a = APP.el('a', 'lnk', it.label); a.href = '#'; a.addEventListener('click', function (e) { e.preventDefault(); it.onClick(a); });
        li.appendChild(APP.scope('cn-links', a, 'span')); li.appendChild(document.createTextNode(' ')); li.appendChild(APP.stat(it.kind, it.status)); ul.appendChild(li); });
      p.parentNode.appendChild(ul);
    }
    var acts = c.querySelector('.actions'), proto = acts.querySelector('.qbtn'); acts.textContent = '';
    o.actions.forEach(function (a) { var b = proto.cloneNode(true); b.textContent = a.label; b.addEventListener('click', a.onClick); acts.appendChild(b); });
    host.appendChild(APP.scope('cn-cards', c));
  };

  /* ------------------------------------------------------------------ alert */
  APP.alert = function (host, kind, title, text, link) {
    var wrap = APP.tpl('alert'), a = wrap.querySelector('.alert.' + kind) || wrap.querySelector('.alert');
    a = a.cloneNode(true); var main = a.querySelector('.main'); main.textContent = '';
    var s = APP.el('strong', 'em', title + ' '); main.appendChild(s); main.appendChild(document.createTextNode(text + ' '));
    if (link) { var l = APP.el('a', '', link.label); l.href = '#'; l.addEventListener('click', function (e) { e.preventDefault(); link.onClick(); }); main.appendChild(l); }
    var x = a.querySelector('.x'); if (x) { x.addEventListener('click', function () { a.remove(); }); }
    host.appendChild(APP.scope('cn-alert', a));
  };

  /* ------------------------------------------------------------------ helpers for charts */
  function top(map, n) { var ks = Object.keys(map).sort(function (a, b) { return map[b] - map[a]; });
    if (ks.length <= n + 1) { return ks.map(function (k) { return [k, map[k]]; }); }
    var head = ks.slice(0, n).map(function (k) { return [k, map[k]]; }), rest = ks.slice(n).reduce(function (s, k) { return s + map[k]; }, 0);
    return head.concat([['Other', rest]]); }
  APP.top = top;
  function by(rows, key, val) { var m = {}; rows.forEach(function (r) { m[r[key]] = (m[r[key]] || 0) + val(r); }); return m; }
  APP.by = by;
  function dateCats() { return APP.rangeDates().map(APP.dshort); }
  function tile(id) { return $('t-' + id); }
  APP.tile = tile;
  function share(ents) { var all = 0, some = 0; D.entities.forEach(function (e) { var c = D.daily[e.id].cash[89]; all += c; if (ents.indexOf(e) >= 0) { some += c; } }); return all ? some / all : 0; }
  function passE(r) { return APP.pass(r) && APP.entitiesInView().some(function (e) { return e.id === r.entity; }); }
  APP.passE = passE;
  function sub() { return 'GBP equivalents at illustrative rates · ' + D.asAtLabel; }

  /* ------------------------------------------------------------------ shared record openers */
  function kv(pairs) { return APP.summary(pairs); }
  function para(t) { return APP.el('p', 't-ed-body', t); }
  APP.openPayment = function (p) {
    var st = APP.pay(p), mine = st === 'Awaiting your approval';
    APP.drawer.open({ title: 'Payment ' + p.id, body: [
      kv([['Status', APP.stat(APP.statusKind(st), st)], ['Beneficiary', p.beneficiary], ['Type', p.type], ['Entity', APP.ent(p.entity).name],
          ['Amount', APP.money(p.ccy, p.amount)], ['GBP equivalent', APP.money('GBP', p.gbp) + ' at ' + D.fx[p.ccy] + ' GBP per ' + p.ccy],
          ['Channel', p.channel], ['Created', APP.date(p.created)], ['Value date', APP.date(p.valueDate)], ['Initiated by', p.initiator], ['Reference', p.reference]]),
      APP.timeline('Audit trail', APP.payAudit(p))],
      actions: [
        { label: 'Approve', onClick: function () { APP.approve(p, true); }, disabled: mine ? null : (st === 'Awaiting second approver' ? 'Needs the finance second approver first' : 'Nothing to approve') },
        { label: 'Reject', kind: 'secondary', onClick: function () { APP.approve(p, false); }, disabled: mine ? null : 'Nothing to reject' },
        { label: 'Close', kind: 'secondary', onClick: function () { APP.drawer.close(); } }] });
  };
  APP.approve = function (p, yes) {
    var big = p.gbp >= 10e6, need = !yes || big;
    APP.modal.open({ title: (yes ? 'Approve ' : 'Reject ') + p.id + '?',
      text: (yes ? 'Approve ' : 'Reject ') + APP.money(p.ccy, p.amount) + ' (' + APP.gbpc(p.gbp) + ') to ' + p.beneficiary + ' from ' + APP.ent(p.entity).short + '. ' +
        (yes ? 'It is released on its value date. This is a simulation — nothing leaves any account.' : 'The initiator is told why.'),
      body: [APP.note(yes ? 'Audit note' + (big ? '' : ' (optional)') : 'Reason for rejecting', need ? 'At least 10 characters — it is kept in the audit trail.' : 'Kept in the audit trail.')],
      confirmLabel: yes ? 'Approve payment' : 'Reject payment', focus: need ? '#t1' : null,
      onConfirm: function () { var n = APP.noteValue();
        if (need && n.length < 10) { APP.noteError(yes ? 'Payments of £10m or more need an audit note of at least 10 characters.' : 'Give a reason of at least 10 characters so the initiator can act on it.'); return false; }
        audit('pay', p.id, yes ? 'Approved' : 'Rejected', yes ? 'Approved by you' : 'Rejected by you', n, yes ? 'ok' : 'err');
        APP.toast(yes ? 'ok' : 'info', (yes ? 'Approved ' : 'Rejected ') + p.id + ' — ' + APP.gbpc(p.gbp) + ' to ' + p.beneficiary + '.');
        APP.refresh(); } });
  };
  APP.openException = function (x) {
    var st = APP.exc(x), lim = D.limits.filter(function (l) { return l.id === x.limitId; })[0];
    var body = [kv([['Status', APP.stat(APP.statusKind(st), st)], ['Severity', APP.stat(x.severity === 'Material' ? 'err' : 'warn', x.severity)], ['Entity', APP.ent(x.entity).name],
      ['Region', APP.regionName(x.region)], ['Currency', x.ccy], ['Amount at risk', APP.gbpc(x.gbp)], ['Detected', APP.date(x.detected)], ['Owner', x.owner]])];
    if (lim) { var h = APP.el('div'); APP.meter(h, lim); body.push(h); }
    body.push(APP.timeline('Audit trail', APP.excAudit(x)));
    APP.drawer.open({ title: x.id + ' · ' + x.title, body: body, actions: [
      { label: 'Acknowledge', onClick: function () { APP.acknowledge(x); }, disabled: st === 'Open' ? null : 'Already acknowledged' },
      { label: 'View positions', kind: 'secondary', onClick: function () { APP.drawer.close(true); APP.go('risk', x.region ? [{ facet: 'region', value: x.region }] : null); } }] });
  };
  APP.acknowledge = function (x) {
    var min = x.severity === 'Material' ? 15 : 10;
    APP.modal.open({ title: 'Acknowledge ' + x.id + '?', text: x.title + '. Acknowledging records that you have seen it and what happens next; it does not close the exception.',
      body: [APP.note('Audit note', 'At least ' + min + ' characters: the action you expect and by when.')], confirmLabel: 'Acknowledge', focus: '#t1',
      onConfirm: function () { var n = APP.noteValue();
        if (n.length < min) { APP.noteError('A ' + x.severity.toLowerCase() + ' exception needs an audit note of at least ' + min + ' characters.'); return false; }
        audit('exc', x.id, 'Acknowledged', 'Acknowledged by you', n, 'ok');
        APP.toast('ok', x.id + ' acknowledged. The note is in its audit trail.'); APP.refresh(); } });
  };

  /* ------------------------------------------------------------------ VIEWS */
  var V = APP.views = {};
  function kpiSeries(ents) {
    var cash = APP.series('cash', ents), und = D.facilities.filter(function (f) { return f.committed && ents.some(function (e) { return e.id === f.entity; }); }).reduce(function (s, f) { return s + f.undrawnGbp; }, 0);
    var sh = share(ents), buffer = D.policy.minimumLiquidityGbp * sh, mat = D.maturities[0].gbp * sh;
    var avail = cash.map(function (c) { return c + und; }), head = avail.map(function (a) { return a - buffer - mat; });
    return { cash: cash, avail: avail, head: head, und: und, buffer: buffer, mat: mat };
  }
  function coverSeries(ents, cash) { var o = APP.series('outflow', ents), avg = o.reduce(function (s, v) { return s + v; }, 0) / Math.max(1, o.filter(function (v) { return v > 0; }).length);
    return cash.map(function (c) { return avg ? c / avg : 0; }); }
  function weekPct(s) { var n = s.length, now = s[n - 1], then = s[Math.max(0, n - 8)]; return then ? (now - then) / then * 100 : (now ? 100 : 0); }
  function pct(s) { return s[0] ? (s[s.length - 1] - s[0]) / Math.abs(s[0]) * 100 : 0; }
  function kpiVal(n) { return APP.gbpc(n).replace('£', ''); }

  V.overview = function () {
    var ents = APP.entitiesInView(), k = kpiSeries(ents), per = 'vs ' + S.days + ' days ago';
    [['ov-k-cash', 'Cash', k.cash, 'accounts'], ['ov-k-liq', 'Available liquidity', k.avail, 'liquidity'], ['ov-k-head', 'Funding headroom', k.head, 'liquidity']].forEach(function (x) {
      APP.kpi(tile(x[0]), { label: x[1], unit: '£', value: kpiVal(x[2][x[2].length - 1]), delta: pct(x[2]), series: x[2], per: per, go: x[3] }); });
    var cov = coverSeries(ents, k.cash);
    APP.kpi(tile('ov-k-cover'), { label: 'Days of cash cover', unit: '', value: Math.round(cov[cov.length - 1]) + ' days', delta: pct(cov), series: cov, per: per, go: 'liquidity' });
    APP.chart(tile('ov-c-trend'), { title: 'Cash, available liquidity and funding headroom, ' + APP.rangeLabel(),
      legend: ['Cash', 'Available liquidity', 'Funding headroom'],
      spec: { type: 'multiline', categories: dateCats(), categoryLabel: 'Day', unit: '£m',
        series: [{ name: 'Cash', values: k.cash.map(APP.m) }, { name: 'Available liquidity', values: k.avail.map(APP.m) }, { name: 'Funding headroom', values: k.head.map(APP.m) }],
        caption: 'Cash, available liquidity (cash plus undrawn committed facilities) and funding headroom (less the minimum liquidity buffer and debt due within three months), £m' } });
    var pos = D.positions.filter(function (p) { return APP.pass(p) && APP.matchQ(p, ['counterparty', 'id', 'instrument']); });
    var regs = D.regions.filter(function (r) { return pos.some(function (p) { return p.region === r.id; }); });
    var ccys = top(by(pos, 'ccy', function (p) { return p.gbp; }), 4).map(function (x) { return x[0]; });
    if (regs.length && ccys.length) {
      APP.chart(tile('ov-c-exposure'), { title: 'Exposure by region and currency — select a column to open its positions', legend: ccys,
        drill: function (i) { APP.go('risk', [{ facet: 'region', value: regs[i].id }]); },
        spec: { type: 'stacked-column', categories: regs.map(function (r) { return r.name; }), categoryLabel: 'Region', unit: '£m',
          series: ccys.map(function (c) { return { name: c, values: regs.map(function (r) { return APP.m(pos.filter(function (p) { return p.region === r.id && (c === 'Other' ? ccys.indexOf(p.ccy) < 0 : p.ccy === c); }).reduce(function (s, p) { return s + p.gbp; }, 0)); }) }; }),
          caption: 'Gross exposure by region, split by currency, £m GBP equivalent' } });
      var cs = top(by(pos, 'ccy', function (p) { return p.gbp; }), 4);
      APP.chart(tile('ov-c-ccy'), { title: 'Share of exposure by currency — select a slice to drill in', legend: cs.map(function (x) { return x[0]; }),
        drill: function (i) { if (cs[i][0] !== 'Other') { APP.go('risk', [{ facet: 'currency', value: cs[i][0] }]); } },
        spec: { type: 'donut', categories: cs.map(function (x) { return x[0]; }), categoryLabel: 'Currency', unit: '£m',
          series: [{ name: 'Exposure', values: cs.map(function (x) { return APP.m(x[1]); }) }], caption: 'Gross exposure by currency, £m GBP equivalent' } });
    } else { tile('ov-c-exposure').textContent = ''; tile('ov-c-exposure').appendChild(APP.empty('No exposure in view', 'No positions match the filters in view.', { label: 'Clear all filters', onClick: APP.clearFilters }));
      tile('ov-c-ccy').textContent = ''; }
    var pend = D.payments.filter(function (p) { return passE(p) && APP.pay(p) === 'Awaiting your approval'; }).sort(function (a, b) { return b.gbp - a.gbp; });
    var pv = pend.reduce(function (s, p) { return s + p.gbp; }, 0);
    APP.card(tile('ov-d-approvals'), { icon: 'ap-payments', title: 'Pending approvals',
      text: pend.length ? pend.length + ' payments worth ' + APP.gbpc(pv) + ' need your approval. Largest first:' : 'Nothing is waiting for your approval in view.',
      items: pend.slice(0, 3).map(function (p) { return { label: p.id + ' · ' + APP.gbpc(p.gbp) + ' to ' + p.beneficiary, kind: 'warn', status: 'Awaiting you', onClick: function () { APP.openPayment(p); } }; }),
      actions: [{ label: pend.length ? 'Open ' + pend[0].id : 'Open payments', onClick: function () { if (pend.length) { APP.openPayment(pend[0]); } else { APP.go('payments'); } } },
                { label: 'All payments', onClick: function () { APP.go('payments'); } }] });
    var ex = D.exceptions.filter(function (x) { return APP.pass(x) && APP.exc(x) === 'Open' && x.severity === 'Material'; });
    APP.card(tile('ov-d-exceptions'), { icon: 'ap-risk', title: 'Material risk exceptions',
      text: ex.length ? ex.length + ' material exceptions are open and need your acknowledgement:' : 'No material exceptions are open in view.',
      items: ex.slice(0, 3).map(function (x) { return { label: x.id + ' · ' + x.title, kind: 'err', status: 'Material', onClick: function () { APP.openException(x); } }; }),
      actions: [{ label: ex.length ? 'Open ' + ex[0].id : 'Open risk', onClick: function () { if (ex.length) { APP.openException(ex[0]); } else { APP.go('risk'); } } },
                { label: 'All exceptions', onClick: function () { APP.go('risk'); } }] });
    APP.setResult(pend.length + ex.length, D.payments.filter(function (p) { return APP.pay(p) === 'Awaiting your approval'; }).length + D.exceptions.filter(function (x) { return x.severity === 'Material' && APP.exc(x) === 'Open'; }).length, 'decisions');
  };

  V.accounts = function () {
    var accs = D.accounts.filter(function (a) { return APP.pass(a) && APP.matchQ(a, ['name', 'id', 'number', 'type', 'ccy']); });
    var be = by(accs, 'entity', function (a) { return a.gbp; }), ents = D.entities.filter(function (e) { return be[e.id] != null; });
    if (ents.length) {
      APP.chart(tile('ac-c-entity'), { title: 'Balances by entity', spec: { type: 'bar', categories: ents.map(function (e) { return e.short; }), categoryLabel: 'Entity', unit: '£m',
        series: [{ name: 'Balance', values: ents.map(function (e) { return APP.m(be[e.id]); }) }], caption: 'Account balances by entity, £m GBP equivalent, ' + D.asAtLabel } });
      var bc = top(by(accs, 'ccy', function (a) { return a.gbp; }), 4);
      APP.chart(tile('ac-c-ccy'), { title: 'Balances by account currency', legend: bc.map(function (x) { return x[0]; }),
        spec: { type: 'pie', categories: bc.map(function (x) { return x[0]; }), categoryLabel: 'Currency', unit: '£m', series: [{ name: 'Balance', values: bc.map(function (x) { return APP.m(x[1]); }) }], caption: 'Account balances by currency, £m GBP equivalent' } });
    }
    var ev = APP.entitiesInView(), infl = ev.map(function (e) { return APP.series('inflow', [e]).reduce(function (s, v) { return s + v; }, 0); }), outf = ev.map(function (e) { return APP.series('outflow', [e]).reduce(function (s, v) { return s + v; }, 0); });
    if (ev.length) {
      APP.chart(tile('ac-c-flows'), { title: 'Inflows against outflows by entity, ' + APP.rangeLabel(), legend: ['Inflows', 'Outflows'],
        spec: { type: 'butterfly-h', categories: ev.map(function (e) { return e.short; }), categoryLabel: 'Entity', unit: '£m',
          series: [{ name: 'Inflows', values: infl.map(APP.m) }, { name: 'Outflows', values: outf.map(APP.m) }], caption: 'Total inflows and outflows by entity, £m GBP equivalent' } });
      var regs = D.regions.filter(function (r) { return ev.some(function (e) { return e.region === r.id; }); });
      APP.chart(tile('ac-c-daily'), { title: 'Daily closing cash by region, ' + APP.rangeLabel(), legend: regs.length > 1 ? regs.map(function (r) { return r.name; }) : null,
        spec: { type: regs.length > 1 ? 'multiline' : 'line', categories: dateCats(), categoryLabel: 'Day', unit: '£m',
          series: regs.map(function (r) { return { name: r.name, values: APP.series('cash', ev.filter(function (e) { return e.region === r.id; })).map(APP.m) }; }), caption: 'Daily closing cash by region, £m GBP equivalent' } });
    }
    APP.records(tile('ac-r-accounts'), { id: 'accounts', title: 'Accounts', noun: 'accounts', sub: sub, primary: false,
      rows: function () { return accs; }, sorts: [['gbp:desc', 'Largest balance first'], ['name:asc', 'Account name'], ['ccy:asc', 'Currency']],
      cols: [{ label: 'Account', v: function (a) { return a.name; } }, { label: 'Number', v: function (a) { return a.number; } }, { label: 'Currency', v: function (a) { return a.ccy; } },
        { label: 'Balance', num: true, v: function (a) { return APP.money(a.ccy, a.balance); } }, { label: 'GBP equivalent', num: true, v: function (a) { return APP.money('GBP', a.gbp); } },
        { label: 'Status', v: function (a) { return APP.stat('ok', a.status); } }],
      card: function (a) { return { title: a.name, initials: a.ccy, desc: a.number + ' · ' + a.bank, amount: APP.money(a.ccy, a.balance), status: ['ok', a.status] }; },
      open: function (a) { var tx = D.transactions.filter(function (t) { return t.account === a.id; });
        APP.drawer.open({ title: a.name, body: [kv([['Account', a.number], ['Entity', APP.ent(a.entity).name], ['Bank', a.bank], ['Type', a.type], ['Balance', APP.money(a.ccy, a.balance)],
          ['GBP equivalent', APP.money('GBP', a.gbp)], ['Rate used', D.fx[a.ccy] + ' GBP per ' + a.ccy + ' (illustrative)'], ['Transactions, 90 days', String(tx.length)]])],
          actions: [{ label: 'Download statement (CSV)', onClick: function () { APP.toast('ok', APP.exportRows('csv', a.name + ' statement', TXCOLS, tx)); } },
            { label: 'Show its transactions', kind: 'secondary', onClick: function () { APP.drawer.close(true); APP.setQuery(a.id); } }] }); } });
    var tx = D.transactions.filter(function (t) { return APP.pass(t) && APP.inRange(t.date) && APP.matchQ(t, ['counterparty', 'ref', 'type', 'account', 'ccy']); });
    var rows = window.CEO_GRID_ROWS; rows.length = 0;
    tx.forEach(function (t) { rows.push({ id: t.id, date: t.date, payee: t.counterparty, ref: t.ref, type: t.type + ' · ' + t.ccy, amount: t.gbp }); });
    if (typeof state !== 'undefined' && typeof render === 'function') { state.page = 1; render(); }
    APP.setResult(tx.length, D.transactions.length, 'transactions');
  };
  var TXCOLS = [{ label: 'Date', text: function (t) { return t.date; } }, { label: 'Counterparty', text: function (t) { return t.counterparty; } }, { label: 'Reference', text: function (t) { return t.ref; } },
    { label: 'Type', text: function (t) { return t.type; } }, { label: 'Currency', text: function (t) { return t.ccy; } }, { label: 'Amount', text: function (t) { return t.amount; } }, { label: 'GBP equivalent', text: function (t) { return t.gbp; } }];
  APP.TXCOLS = TXCOLS;
  APP.openTransaction = function (id) { var t = D.transactions.filter(function (x) { return x.id === id; })[0]; if (!t) { return; }
    APP.drawer.open({ title: 'Transaction ' + t.ref, body: [kv([['Date', APP.date(t.date)], ['Counterparty', t.counterparty], ['Type', t.type], ['Entity', APP.ent(t.entity).name], ['Account', t.account],
      ['Amount', APP.money(t.ccy, t.amount)], ['GBP equivalent', APP.money('GBP', t.gbp)], ['Rate used', D.fx[t.ccy] + ' GBP per ' + t.ccy + ' (illustrative)']])],
      actions: [{ label: 'Raise an investigation', onClick: function () { APP.drawer.close(true); APP.newRequest('Payment investigation', t.entity, 'Please investigate ' + t.type.toLowerCase() + ' ' + t.ref + ' of ' + APP.money(t.ccy, t.amount) + ' on ' + APP.date(t.date) + '.'); } }] }); };

  V.liquidity = function () {
    var ents = APP.entitiesInView(), k = kpiSeries(ents), per = 'vs ' + S.days + ' days ago';
    var cover = coverSeries(ents, k.cash);
    var unc = D.facilities.filter(function (f) { return !f.committed && ents.some(function (e) { return e.id === f.entity; }); }).reduce(function (s, f) { return s + f.undrawnGbp; }, 0);
    APP.kpi(tile('lq-k-avail'), { label: 'Available liquidity', unit: '£', value: kpiVal(k.avail[k.avail.length - 1]), delta: pct(k.avail), series: k.avail, per: per, go: 'liquidity' });
    APP.kpi(tile('lq-k-undrawn'), { label: 'Undrawn committed', unit: '£', value: kpiVal(k.und), delta: 0, series: k.avail.map(function () { return k.und; }), per: 'unchanged in period', go: 'liquidity' });
    APP.kpi(tile('lq-k-head'), { label: 'Funding headroom', unit: '£', value: kpiVal(k.head[k.head.length - 1]), delta: pct(k.head), series: k.head, per: per, go: 'liquidity' });
    var due = D.facilities.filter(function (f) { return ents.some(function (e) { return e.id === f.entity; }) && f.maturity <= '2027-03-31'; }).reduce(function (s, f) { return s + f.drawnGbp; }, 0);
    APP.kpi(tile('lq-k-due'), { label: 'Debt due by Mar 2027', unit: '£', value: kpiVal(due), delta: 0, series: k.head.map(function () { return due; }), per: 'unchanged in period', go: 'liquidity' });
    void cover;
    APP.chart(tile('lq-c-composition'), { title: 'What makes up available liquidity, ' + APP.rangeLabel(), legend: ['Cash', 'Undrawn committed', 'Undrawn uncommitted'],
      spec: { type: 'stacked-area', categories: dateCats(), categoryLabel: 'Day', unit: '£m',
        series: [{ name: 'Cash', values: k.cash.map(APP.m) }, { name: 'Undrawn committed', values: k.cash.map(function () { return APP.m(k.und); }) }, { name: 'Undrawn uncommitted', values: k.cash.map(function () { return APP.m(unc); }) }],
        caption: 'Available liquidity by source, £m GBP equivalent' } });
    var fac = D.facilities.filter(function (f) { return ents.some(function (e) { return e.id === f.entity; }) && APP.matchQ(f, ['name', 'type', 'id', 'ccy']); });
    if (fac.length) {
      APP.chart(tile('lq-c-util'), { title: 'Facility utilisation against the 80% policy line', domainMax: 100,
        spec: { type: 'bullet', categories: fac.map(function (f) { return f.id; }), categoryLabel: 'Facility', ranges: [60, 80, 100], unit: '%',
          series: [{ name: 'Drawn', values: fac.map(function (f) { return Math.round(f.drawnGbp / f.limitGbp * 100); }) }, { name: 'Policy line', values: fac.map(function () { return 80; }) }],
          caption: 'Drawn as a percentage of each facility limit, against the 80% policy line' } });
    }
    var sh = share(ents);
    APP.chart(tile('lq-c-ladder'), { title: 'Debt maturity profile' + (sh < 0.999 ? ', pro-rated to the entities in view' : ''),
      spec: { type: 'column', categories: D.maturities.map(function (m) { return m.bucket; }), categoryLabel: 'Maturity', unit: '£m',
        series: [{ name: 'Maturing', values: D.maturities.map(function (m) { return APP.m(m.gbp * sh); }) }], caption: 'Debt maturing by bucket, £m' } });
    APP.records(tile('lq-r-facilities'), { id: 'facilities', title: 'Facilities', noun: 'facilities', sub: sub, primary: true, total: function () { return D.facilities.length; },
      rows: function () { return fac.map(function (f) { f.util = Math.round(f.drawnGbp / f.limitGbp * 100); return f; }); },
      sorts: [['util:desc', 'Most drawn first'], ['maturity:asc', 'Soonest maturity'], ['limitGbp:desc', 'Largest limit']],
      cols: [{ label: 'Facility', v: function (f) { return f.name; } }, { label: 'Limit', num: true, v: function (f) { return APP.mc(f.ccy, f.limit); } },
        { label: 'Drawn', num: true, v: function (f) { return APP.mc(f.ccy, f.drawn); } }, { label: 'Undrawn (GBP)', num: true, v: function (f) { return APP.gbpc(f.undrawnGbp); } },
        { label: 'Utilisation', num: true, v: function (f) { return f.util + '%'; } }, { label: 'Matures', v: function (f) { return APP.dshort(f.maturity) + ' ' + f.maturity.slice(2, 4); } }],
      card: function (f) { return { title: f.name, initials: f.ccy, desc: 'Matures ' + APP.date(f.maturity) + ' · ' + f.util + '% drawn', amount: APP.gbpc(f.undrawnGbp) + ' undrawn', status: [f.util >= 80 ? 'warn' : 'ok', f.util >= 80 ? 'Above policy line' : 'Within policy'] }; },
      open: function (f) { var h = APP.el('div'); APP.meter(h, { name: f.name, status: f.util > 100 ? 'Breach' : f.util >= 80 ? 'Approaching' : 'Within', pct: f.util, usedGbp: f.drawnGbp, limitGbp: f.limitGbp });
        APP.drawer.open({ title: f.name, body: [kv([['Entity', APP.ent(f.entity).name], ['Type', f.type], ['Committed', f.committed ? 'Yes' : 'No'], ['Limit', APP.money(f.ccy, f.limit)], ['Drawn', APP.money(f.ccy, f.drawn)],
          ['Undrawn, GBP equivalent', APP.money('GBP', f.undrawnGbp)], ['Matures', APP.date(f.maturity)]]), h],
          actions: [{ label: 'Request a change', onClick: function () { APP.drawer.close(true); APP.newRequest('Facility amendment', f.entity, 'Please propose terms to amend ' + f.name + ' (' + f.id + ').'); } }] }); } });
  };

  V.payments = function () {
    var pays = D.payments.filter(function (p) { return passE(p) && APP.inRange(p.created) && APP.matchQ(p, ['id', 'beneficiary', 'type', 'reference', 'initiator', 'ccy']); });
    var await_ = pays.filter(function (p) { return APP.pay(p) === 'Awaiting your approval'; });
    var cats = APP.rangeDates(), dcat = dateCats();
    function daily(pred, val) { return cats.map(function (d) { return pays.filter(function (p) { return p.created === d && pred(p); }).reduce(function (s, p) { return s + val(p); }, 0); }); }
    var rel = daily(function (p) { return APP.pay(p) === 'Released'; }, function (p) { return p.gbp; });
    var cum = 0, pendS = cats.map(function (d) { cum += pays.filter(function (p) { return p.created === d && APP.pay(p) === 'Awaiting your approval'; }).reduce(function (s, p) { return s + p.gbp; }, 0); return cum; });
    var rej = daily(function (p) { return APP.pay(p) === 'Rejected'; }, function () { return 1; }), rc = 0, rejCum = rej.map(function (v) { rc += v; return rc; });
    var relC = 0, relCum = rel.map(function (v) { relC += v; return relC; });
    APP.kpi(tile('py-k-await'), { label: 'Awaiting you', unit: '£', value: kpiVal(await_.reduce(function (s, p) { return s + p.gbp; }, 0)), delta: weekPct(pendS), series: pendS, per: 'vs a week ago', go: 'payments' });
    var sec = pays.filter(function (p) { return APP.pay(p) === 'Awaiting second approver'; }), secS = cats.map(function (d) { return sec.filter(function (p) { return p.created <= d; }).length; });
    APP.kpi(tile('py-k-second'), { label: 'With second approver', unit: '', value: String(sec.length), delta: weekPct(secS), series: secS.length > 1 ? secS : [0, 0], per: 'vs a week ago', go: 'payments' });
    APP.kpi(tile('py-k-released'), { label: 'Released', unit: '£', value: kpiVal(relC), delta: weekPct(relCum), series: relCum, per: 'running total vs a week ago', go: 'payments' });
    APP.kpi(tile('py-k-rejected'), { label: 'Rejected', unit: '', value: String(rc), delta: weekPct(rejCum), series: rejCum.length > 1 ? rejCum : [0, 0], per: 'running total vs a week ago', go: 'payments' });
    APP.chart(tile('py-c-combo'), { title: 'Value released and payments created per day, ' + APP.rangeLabel(), legend: ['Released (£m)', 'Payments created'],
      spec: { type: 'combo', categories: dcat, categoryLabel: 'Day',
        series: [{ name: 'Released (£m)', kind: 'column', unit: '£m', values: rel.map(APP.m) }, { name: 'Payments created', kind: 'line', unit: '', values: daily(function () { return true; }, function () { return 1; }) }],
        caption: 'Value released per day (£m, columns) and number of payments created per day (line)' } });
    var bins = [[0, 0.5e6, 'Under £0.5m'], [0.5e6, 1e6, '£0.5–1m'], [1e6, 2e6, '£1–2m'], [2e6, 5e6, '£2–5m'], [5e6, 10e6, '£5–10m'], [10e6, 20e6, '£10–20m'], [20e6, 1e12, '£20m and over']];
    APP.chart(tile('py-c-hist'), { title: 'How payment values are distributed',
      spec: { type: 'histogram', categories: bins.map(function (b) { return b[2]; }), categoryLabel: 'Value band', series: [{ name: 'payments', values: bins.map(function (b) { return pays.filter(function (p) { return p.gbp >= b[0] && p.gbp < b[1]; }).length; }) }],
        caption: 'Number of payments by GBP-equivalent value band' } });
    var groups = [['Awaiting your approval', ['Awaiting your approval']], ['Awaiting second approver', ['Awaiting second approver']], ['Approved or scheduled', ['Approved', 'Scheduled']], ['Released', ['Released']], ['Rejected', ['Rejected']]];
    var gv = groups.map(function (g) { return pays.filter(function (p) { return g[1].indexOf(APP.pay(p)) >= 0; }).length; });
    var gk = groups.filter(function (g, i) { return gv[i] > 0; }), gvals = gv.filter(function (v) { return v > 0; });
    if (gk.length) { APP.chart(tile('py-c-status'), { title: 'Payments by status', legend: gk.map(function (g) { return g[0]; }),
      spec: { type: 'donut', categories: gk.map(function (g) { return g[0]; }), categoryLabel: 'Status', series: [{ name: 'Payments', values: gvals }], caption: 'Number of payments by status' } }); }
    APP.records(tile('py-r-payments'), { id: 'payments', title: 'Payments', noun: 'payments', sub: sub, primary: true, total: function () { return D.payments.length; },
      rows: function () { return pays.map(function (p) { p.st = APP.pay(p); p.stOrder = p.st === 'Awaiting your approval' ? 0 : p.st === 'Awaiting second approver' ? 1 : 2; return p; }); },
      sorts: [['stOrder:asc', 'Needs you first'], ['gbp:desc', 'Largest first'], ['valueDate:asc', 'Soonest value date'], ['created:desc', 'Newest first']],
      cols: [{ label: 'Payment', v: function (p) { return p.id; } }, { label: 'Beneficiary', v: function (p) { return p.beneficiary; } },
        { label: 'Amount', num: true, v: function (p) { return APP.money(p.ccy, p.amount); } }, { label: 'GBP equivalent', num: true, v: function (p) { return APP.gbpc(p.gbp); } },
        { label: 'Value date', v: function (p) { return APP.dshort(p.valueDate); } }, { label: 'Status', v: function (p) { return APP.stat(APP.statusKind(p.st), p.st); } }],
      card: function (p) { return { title: p.beneficiary, initials: p.ccy, avatar: p.ccy, desc: p.id + ' · ' + APP.dshort(p.valueDate) + ' · ' + p.type, amount: APP.money(p.ccy, p.amount), status: [APP.statusKind(p.st), p.st] }; },
      open: APP.openPayment });
  };

  V.fx = function () {
    var f = APP.facets(), nS = Math.min(30, S.days), sess = D.dates.slice(D.dates.length - 30).slice(30 - nS).map(APP.dshort);
    var pick = ['USD', 'EUR', 'CNY', 'JPY'], chosen = f.currency.filter(function (c) { return c !== 'GBP'; });
    var four = chosen.concat(pick.filter(function (c) { return chosen.indexOf(c) < 0; })).slice(0, 4);
    ['fx-s-usd', 'fx-s-eur', 'fx-s-cny', 'fx-s-jpy'].forEach(function (id, i) { var c = four[i], s = D.fxSeries[c].slice(30 - nS).map(function (v) { return +(1 / v).toFixed(c === 'JPY' ? 2 : 4); });
      APP.chart(tile(id), { title: 'GBP/' + c + ' ' + s[s.length - 1] + ' (' + (pct(s) >= 0 ? '+' : '−') + Math.abs(pct(s)).toFixed(2) + '%)',
        spec: { type: 'spark', categories: sess, categoryLabel: 'Day', series: [{ name: c + ' per GBP', values: s }], caption: c + ' per pound, last ' + nS + ' sessions, illustrative' } }); });
    var cc0 = four[0], cd = D.candles[cc0].slice(30 - nS);
    APP.chart(tile('fx-c-candle'), { title: 'GBP/' + cc0 + ', last ' + nS + ' sessions (illustrative)' + (chosen.length ? '' : ' — add a currency filter to switch pair'),
      spec: { type: 'candlestick', categories: cd.map(function (c) { return APP.dshort(c.date); }), categoryLabel: 'Session',
        series: [{ name: 'Open', values: cd.map(function (c) { return c.open; }) }, { name: 'High', values: cd.map(function (c) { return c.high; }) },
                 { name: 'Low', values: cd.map(function (c) { return c.low; }) }, { name: 'Close', values: cd.map(function (c) { return c.close; }) }],
        caption: 'GBP/' + cc0 + ' open, high, low and close, ' + cc0 + ' per pound, ' + nS + ' sessions, illustrative' } });
    var hed = D.hedge.filter(function (h) { return !f.currency.length || f.currency.indexOf(h.ccy) >= 0; });
    if (hed.length) { APP.chart(tile('fx-c-hedge'), { title: 'Hedge ratio against policy target', domainMax: 100,
      spec: { type: 'bullet', categories: hed.map(function (h) { return h.ccy; }), categoryLabel: 'Currency', ranges: [40, 60, 100], unit: '%',
        series: [{ name: 'Hedged', values: hed.map(function (h) { return h.actual; }) }, { name: 'Target', values: hed.map(function (h) { return h.target; }) }], caption: 'Share of forecast exposure hedged, against the policy target, per cent' } }); }
    var pos = D.positions.filter(APP.pass), deals = D.fxDeals.filter(function (d) { return APP.pass(d) && d.product !== 'Spot' && d.status !== 'Settled'; });
    var cc = ['USD', 'EUR', 'SGD', 'HKD', 'AED', 'CNY', 'JPY'].filter(function (c) { return pos.some(function (p) { return p.ccy === c; }); });
    if (cc.length) { APP.chart(tile('fx-c-exposure'), { title: 'Foreign-currency exposure and hedges in place', legend: ['Gross exposure', 'Hedged by open forwards and swaps'],
      spec: { type: 'grouped-column', categories: cc, categoryLabel: 'Currency', unit: '£m',
        series: [{ name: 'Gross exposure', values: cc.map(function (c) { return APP.m(pos.filter(function (p) { return p.ccy === c; }).reduce(function (s, p) { return s + p.gbp; }, 0)); }) },
                 { name: 'Hedged by open forwards and swaps', values: cc.map(function (c) { return APP.m(deals.filter(function (d) { return d.ccy === c; }).reduce(function (s, d) { return s + d.gbp; }, 0)); }) }],
        caption: 'Gross exposure and open hedges by currency, £m GBP equivalent' } }); }
    var rates = D.currencies.filter(function (c) { return c !== 'GBP' && (!f.currency.length || f.currency.indexOf(c) >= 0); }).map(function (c) {
      var s = D.fxSeries[c]; return { id: c, ccy: c, gbpPer: D.fx[c], perGbp: +(1 / D.fx[c]).toFixed(c === 'JPY' ? 2 : 4), chg: +((s[29] - s[0]) / s[0] * 100).toFixed(2) }; })
      .filter(function (r) { return APP.matchQ(r, ['ccy']); });
    APP.records(tile('fx-r-rates'), { id: 'rates', title: 'Illustrative FX rates used for GBP reporting', noun: 'rates', sub: function () { return D.fxNote; },
      rows: function () { return rates; }, sorts: [['ccy:asc', 'Currency'], ['chg:desc', 'Biggest 30-day rise']],
      cols: [{ label: 'Currency', v: function (r) { return r.ccy; } }, { label: 'GBP per unit', num: true, v: function (r) { return String(r.gbpPer); } }, { label: 'Units per GBP', num: true, v: function (r) { return String(r.perGbp); } },
        { label: '30-day change', num: true, v: function (r) { return (r.chg >= 0 ? '+' : '−') + Math.abs(r.chg).toFixed(2) + '%'; } }],
      card: function (r) { return { title: 'GBP/' + r.ccy, initials: r.ccy, desc: r.gbpPer + ' GBP per ' + r.ccy, amount: r.perGbp + ' ' + r.ccy + ' per GBP', status: null }; },
      open: function (r) { APP.drawer.open({ title: 'GBP/' + r.ccy + ' (illustrative)', body: [kv([['GBP per ' + r.ccy, String(r.gbpPer)], [r.ccy + ' per GBP', String(r.perGbp)], ['30-day change', r.chg + '%'], ['Source', D.fxNote]]),
        para('Every GBP equivalent in this prototype is the local amount multiplied by this rate. These are not market rates and must not be used to deal.')],
        actions: [{ label: 'Copy rate', onClick: function () { try { navigator.clipboard.writeText(r.ccy + ' ' + r.gbpPer); APP.toast('ok', 'Rate copied.'); } catch (e) { APP.toast('warn', 'Copying needs clipboard permission.'); } } }] }); } });
    var dl = D.fxDeals.filter(function (d) { return APP.pass(d) && APP.inRange(d.trade) && APP.matchQ(d, ['id', 'pair', 'side', 'product', 'status']); });
    APP.records(tile('fx-r-deals'), { id: 'deals', title: 'FX deals', noun: 'deals', sub: sub, primary: true, total: function () { return D.fxDeals.length; }, rows: function () { return dl; },
      sorts: [['value:asc', 'Soonest value date'], ['gbp:desc', 'Largest first'], ['trade:desc', 'Newest trade']],
      cols: [{ label: 'Deal', v: function (d) { return d.id; } }, { label: 'Pair', v: function (d) { return d.pair; } }, { label: 'Side', v: function (d) { return d.side; } }, { label: 'Product', v: function (d) { return d.product; } },
        { label: 'Notional', num: true, v: function (d) { return APP.money(d.ccy, d.amount); } }, { label: 'GBP equivalent', num: true, v: function (d) { return APP.gbpc(d.gbp); } },
        { label: 'Value date', v: function (d) { return APP.date(d.value); } }, { label: 'Status', v: function (d) { return APP.stat(APP.statusKind(d.status), d.status); } }],
      card: function (d) { return { title: d.pair + ' ' + d.product.toLowerCase(), initials: d.ccy, desc: d.id + ' · value ' + APP.dshort(d.value), amount: APP.money(d.ccy, d.amount), status: [APP.statusKind(d.status), d.status] }; },
      open: function (d) { APP.drawer.open({ title: 'FX deal ' + d.id, body: [kv([['Entity', APP.ent(d.entity).name], ['Pair', d.pair], ['Side', d.side], ['Product', d.product], ['Notional', APP.money(d.ccy, d.amount)],
        ['GBP equivalent', APP.money('GBP', d.gbp)], ['Deal rate', String(d.rate)], ['Traded', APP.date(d.trade)], ['Value date', APP.date(d.value)], ['Status', APP.stat(APP.statusKind(d.status), d.status)]])],
        actions: [{ label: 'Ask HSBC Markets about this deal', onClick: function () { APP.drawer.close(true); APP.newRequest('Payment investigation', d.entity, 'Query on FX deal ' + d.id + ' (' + d.pair + ', value ' + APP.date(d.value) + ').'); } }] }); } });
  };

  V.risk = function () {
    var al = $('alerts-risk'); al.textContent = '';
    var lim = D.limits.filter(function (l) { return (!l.region || APP.pass({ region: l.region })) && (l.kind !== 'Currency net open position' || APP.pass({ ccy: l.ccy })); });
    var br = lim.filter(function (l) { return l.status === 'Breach'; });
    if (br.length) { APP.alert(al, 'err', br.length + (br.length === 1 ? ' limit is' : ' limits are') + ' above their cap.', br.map(function (l) { return l.name + ' (' + l.pct + '%)'; }).join(', ') + '.',
      { label: 'Review risk exceptions', onClick: function () { var t = tile('rk-r-exceptions'); t.scrollIntoView({ block: 'start' }); var a = t.querySelector('a.lnk'); if (a) { a.focus(); } } }); }
    var pos = D.positions.filter(function (p) { return APP.pass(p) && APP.matchQ(p, ['id', 'counterparty', 'instrument', 'ccy']); });
    var regs = D.regions.filter(function (r) { return pos.some(function (p) { return p.region === r.id; }); });
    var ccys = top(by(pos, 'ccy', function (p) { return p.gbp; }), 4).map(function (x) { return x[0]; });
    if (regs.length) { APP.chart(tile('rk-c-region'), { title: 'Exposure by region and currency — select a column to narrow the positions below', legend: ccys,
      drill: function (i) { APP.setFilter('region', regs[i].id); },
      spec: { type: 'grouped-column', categories: regs.map(function (r) { return r.name; }), categoryLabel: 'Region', unit: '£m',
        series: ccys.map(function (c) { return { name: c, values: regs.map(function (r) { return APP.m(pos.filter(function (p) { return p.region === r.id && (c === 'Other' ? ccys.indexOf(p.ccy) < 0 : p.ccy === c); }).reduce(function (s, p) { return s + p.gbp; }, 0)); }) }; }),
        caption: 'Gross exposure by region and currency, £m GBP equivalent' } }); }
    var cpl = lim.filter(function (l) { return l.kind === 'Counterparty' && l.usedGbp > 0; }).sort(function (a, b) { return a.usedGbp - b.usedGbp; });
    if (cpl.length) { APP.chart(tile('rk-c-scatter'), { title: 'Counterparties: exposure against limit utilisation',
      spec: { type: 'scatter', categories: cpl.map(function (l) { return String(APP.m(l.usedGbp)); }), categoryLabel: 'Exposure (£m)',
        series: [{ name: 'Utilisation (%)', values: cpl.map(function (l) { return l.pct; }) }], caption: 'Each point is a counterparty: exposure in £m against the share of its limit used, per cent' } }); }
    var worst = lim.slice().sort(function (a, b) { return b.pct - a.pct; });
    APP.chart(tile('rk-c-limits'), { title: 'The six most used limits against the 85% warning line', domainMax: 125,
      spec: { type: 'bullet', categories: worst.slice(0, 6).map(function (l) { return l.id; }), categoryLabel: 'Limit', ranges: [60, 85, 100], unit: '%',
        series: [{ name: 'Used', values: worst.slice(0, 6).map(function (l) { return Math.min(125, l.pct); }) }, { name: 'Warning line', values: worst.slice(0, 6).map(function () { return 85; }) }],
        caption: 'Limit utilisation, per cent, against the 85% warning line; the limits are named in the Limits list below' } });
    ['rk-m-1', 'rk-m-2', 'rk-m-3', 'rk-m-4'].forEach(function (id, i) { var t = tile(id); if (worst[i]) { APP.meter(t, worst[i]); } else { t.textContent = ''; } });
    APP.records(tile('rk-r-positions'), { id: 'positions', title: 'Positions', noun: 'positions', sub: sub, primary: true, total: function () { return D.positions.length; }, rows: function () { return pos; },
      sorts: [['gbp:desc', 'Largest first'], ['maturity:asc', 'Soonest maturity'], ['counterparty:asc', 'Counterparty']],
      cols: [{ label: 'Position', v: function (p) { return p.id; } }, { label: 'Counterparty', v: function (p) { return p.counterparty; } },
        { label: 'Instrument', v: function (p) { return p.instrument; } }, { label: 'Currency', v: function (p) { return p.ccy; } },
        { label: 'GBP equivalent', num: true, v: function (p) { return APP.gbpc(p.gbp); } }, { label: 'Matures', v: function (p) { return APP.dshort(p.maturity) + ' ' + p.maturity.slice(2, 4); } }, { label: 'Limit', v: function (p) { return p.limitId || '—'; } }],
      card: function (p) { return { title: p.counterparty, initials: p.ccy, desc: p.id + ' · ' + p.instrument, amount: APP.money(p.ccy, p.amount), status: null }; },
      open: function (p) { var l = D.limits.filter(function (m) { return m.id === p.limitId; })[0], h = APP.el('div'); if (l) { APP.meter(h, l); }
        APP.drawer.open({ title: 'Position ' + p.id, body: [kv([['Counterparty', p.counterparty + ' (' + p.rating + ')'], ['Entity', APP.ent(p.entity).name], ['Region', APP.regionName(p.region)], ['Instrument', p.instrument],
          ['Amount', APP.money(p.ccy, p.amount)], ['GBP equivalent', APP.money('GBP', p.gbp)], ['Matures', APP.date(p.maturity)], ['Governing limit', l ? l.name : '—']]), h] }); } });
    APP.records(tile('rk-r-limits'), { id: 'limits', title: 'Limits', noun: 'limits', sub: sub, rows: function () { return lim.filter(function (l) { return APP.matchQ(l, ['name', 'kind', 'id']); }); },
      sorts: [['pct:desc', 'Most used first'], ['name:asc', 'Name'], ['kind:asc', 'Kind']],
      cols: [{ label: 'Limit', v: function (l) { return l.name; } }, { label: 'Kind', v: function (l) { return l.kind; } }, { label: 'Limit (GBP)', num: true, v: function (l) { return APP.gbpc(l.limitGbp); } },
        { label: 'Used (GBP)', num: true, v: function (l) { return APP.gbpc(l.usedGbp); } }, { label: 'Used', num: true, v: function (l) { return l.pct + '%'; } }, { label: 'Status', v: function (l) { return APP.stat(APP.statusKind(l.status), l.status); } }],
      card: function (l) { return { title: l.name, initials: l.id.slice(4), desc: l.kind, amount: l.pct + '% used', status: [APP.statusKind(l.status), l.status] }; },
      open: function (l) { var h = APP.el('div'); APP.meter(h, l); var n = D.positions.filter(function (p) { return p.limitId === l.id; }).length;
        APP.drawer.open({ title: l.name, body: [h, kv([['Limit id', l.id], ['Kind', l.kind], ['Positions against it', String(n)]])],
          actions: [{ label: 'Show its positions', onClick: function () { APP.drawer.close(true); if (l.region) { APP.setFilter('region', l.region); } else if (l.kind === 'Counterparty') { APP.setQuery(l.name); } else { APP.setFilter('currency', l.ccy); } } }] }); } });
    var exc = D.exceptions.filter(function (x) { return APP.pass(x) && APP.matchQ(x, ['id', 'title', 'owner', 'severity']); });
    APP.records(tile('rk-r-exceptions'), { id: 'exceptions', title: 'Risk exceptions', noun: 'exceptions', sub: sub,
      rows: function () { return exc.map(function (x) { x.st = APP.exc(x); x.order = (x.st === 'Open' ? 0 : 2) + (x.severity === 'Material' ? 0 : 1); return x; }); },
      sorts: [['order:asc', 'Open and material first'], ['detected:desc', 'Newest first'], ['gbp:desc', 'Largest amount at risk']],
      cols: [{ label: 'Exception', v: function (x) { return x.id; } }, { label: 'What happened', v: function (x) { return x.title; } }, { label: 'Severity', v: function (x) { return APP.stat(x.severity === 'Material' ? 'err' : 'warn', x.severity); } },
        { label: 'Detected', v: function (x) { return APP.date(x.detected); } }, { label: 'Owner', v: function (x) { return x.owner; } }, { label: 'Status', v: function (x) { return APP.stat(APP.statusKind(x.st), x.st); } }],
      card: function (x) { return { title: x.title, initials: x.ccy, desc: x.id + ' · ' + x.severity + ' · ' + x.owner, amount: APP.gbpc(x.gbp) + ' at risk', status: [APP.statusKind(x.st), x.st] }; },
      open: APP.openException });
  };

  V.trade = function () {
    var tr = D.trade.filter(function (t) { return APP.pass(t) && APP.matchQ(t, ['id', 'type', 'counterparty', 'status']); });
    var mix = top(by(tr, 'type', function (t) { return t.gbp; }), 4);
    if (tr.length) {
      APP.chart(tile('tf-c-mix'), { title: 'Portfolio by instrument', legend: mix.map(function (x) { return x[0]; }),
        spec: { type: 'pie', categories: mix.map(function (x) { return x[0]; }), categoryLabel: 'Instrument', unit: '£m', series: [{ name: 'Outstanding', values: mix.map(function (x) { return APP.m(x[1]); }) }], caption: 'Outstanding trade instruments by type, £m GBP equivalent' } });
      var months = [], d0 = new Date(D.asAt + 'T00:00:00Z');
      for (var i = 0; i < 6; i++) { var d = new Date(Date.UTC(d0.getUTCFullYear(), d0.getUTCMonth() + i, 1)); months.push(d.toISOString().slice(0, 7)); }
      APP.chart(tile('tf-c-expiry'), { title: 'What expires in the next six months',
        spec: { type: 'column', categories: months.map(function (m) { return APP.dshort(m + '-01').split(' ')[1] + ' ' + m.slice(2, 4); }), categoryLabel: 'Month', unit: '£m',
          series: [{ name: 'Expiring', values: months.map(function (m) { return APP.m(tr.filter(function (t) { return t.expiry.slice(0, 7) === m; }).reduce(function (s, t) { return s + t.gbp; }, 0)); }) }], caption: 'Value of instruments expiring each month, £m' } });
      var rg = D.regions.filter(function (r) { return tr.some(function (t) { return t.region === r.id; }); });
      APP.chart(tile('tf-c-region'), { title: 'Portfolio by region',
        spec: { type: 'bar', categories: rg.map(function (r) { return r.name; }), categoryLabel: 'Region', unit: '£m', series: [{ name: 'Outstanding', values: rg.map(function (r) { return APP.m(tr.filter(function (t) { return t.region === r.id; }).reduce(function (s, t) { return s + t.gbp; }, 0)); }) }], caption: 'Outstanding by region, £m' } });
      var types = D.trade.map(function (t) { return t.type; }).filter(function (t, i, a) { return a.indexOf(t) === i && tr.some(function (x) { return x.type === t; }); });
      function q(a, p) { var s = a.slice().sort(function (x, y) { return x - y; }), i = (s.length - 1) * p, lo = Math.floor(i), hi = Math.ceil(i); return Math.round(s[lo] + (s[hi] - s[lo]) * (i - lo)); }
      var tn = types.map(function (t) { return tr.filter(function (x) { return x.type === t; }).map(function (x) { return x.tenor; }); });
      APP.chart(tile('tf-c-tenor'), { title: 'Tenor spread by instrument, days', domainMax: 400,
        spec: { type: 'boxplot', categories: types.map(function (t) { return t.replace(' letter of credit', ' LC'); }), categoryLabel: 'Instrument',
          series: [['Minimum', 0], ['Q1', 0.25], ['Median', 0.5], ['Q3', 0.75], ['Maximum', 1]].map(function (x) { return { name: x[0], values: tn.map(function (a) { return q(a, x[1]); }) }; }),
          caption: 'Tenor in days by instrument type: minimum, quartiles and maximum' } });
    }
    APP.records(tile('tf-r-trade'), { id: 'trade', title: 'Trade instruments', noun: 'instruments', sub: sub, primary: true, total: function () { return D.trade.length; }, rows: function () { return tr; },
      sorts: [['expiry:asc', 'Soonest expiry'], ['gbp:desc', 'Largest first'], ['type:asc', 'Instrument type']],
      cols: [{ label: 'Reference', v: function (t) { return t.id; } }, { label: 'Instrument', v: function (t) { return t.type; } }, { label: 'Counterparty', v: function (t) { return t.counterparty; } },
        { label: 'GBP equivalent', num: true, v: function (t) { return APP.gbpc(t.gbp); } },
        { label: 'Expires', v: function (t) { return APP.dshort(t.expiry) + ' ' + t.expiry.slice(2, 4); } }, { label: 'Status', v: function (t) { return APP.stat(APP.statusKind(t.status), t.status); } }],
      card: function (t) { return { title: t.type, initials: t.ccy, desc: t.id + ' · ' + t.counterparty + ' · expires ' + APP.dshort(t.expiry), amount: APP.money(t.ccy, t.amount), status: [APP.statusKind(t.status), t.status] }; },
      open: function (t) { APP.drawer.open({ title: t.type + ' ' + t.id, body: [kv([['Status', APP.stat(APP.statusKind(t.status), t.status)], ['Applicant', APP.ent(t.entity).name], ['Counterparty', t.counterparty],
        ['Amount', APP.money(t.ccy, t.amount)], ['GBP equivalent', APP.money('GBP', t.gbp)], ['Issued', APP.date(t.issued)], ['Expires', APP.date(t.expiry)], ['Tenor', t.tenor + ' days']])],
        actions: [{ label: 'Request an amendment', onClick: function () { APP.drawer.close(true); APP.newRequest('Facility amendment', t.entity, 'Please amend ' + t.type.toLowerCase() + ' ' + t.id + ' (' + APP.money(t.ccy, t.amount) + ').'); } },
          { label: 'Download advice (CSV)', kind: 'secondary', onClick: function () { APP.toast('ok', APP.exportRows('csv', t.id + ' advice', [{ label: 'Field', text: function (r) { return r[0]; } }, { label: 'Value', text: function (r) { return r[1]; } }],
            [['Reference', t.id], ['Instrument', t.type], ['Counterparty', t.counterparty], ['Amount', t.amount + ' ' + t.ccy], ['Expires', t.expiry], ['Status', t.status]])); } }] }); } });
  };

  var REPORT_DATA = {
    Liquidity: function () { return { cols: [{ label: 'Account', text: function (a) { return a.name; } }, { label: 'Currency', text: function (a) { return a.ccy; } }, { label: 'Balance', text: function (a) { return a.balance; } }, { label: 'GBP equivalent', text: function (a) { return a.gbp; } }], rows: D.accounts.filter(APP.pass) }; },
    Payments: function () { return { cols: [{ label: 'Payment', text: function (p) { return p.id; } }, { label: 'Beneficiary', text: function (p) { return p.beneficiary; } }, { label: 'Amount', text: function (p) { return p.amount + ' ' + p.ccy; } }, { label: 'Status', text: function (p) { return APP.pay(p); } }], rows: D.payments.filter(APP.pass) }; },
    Risk: function () { return { cols: [{ label: 'Limit', text: function (l) { return l.name; } }, { label: 'Limit GBP', text: function (l) { return l.limitGbp; } }, { label: 'Used GBP', text: function (l) { return l.usedGbp; } }, { label: 'Status', text: function (l) { return l.status; } }], rows: D.limits }; },
    Markets: function () { return { cols: [{ label: 'Deal', text: function (d) { return d.id; } }, { label: 'Pair', text: function (d) { return d.pair; } }, { label: 'Notional', text: function (d) { return d.amount; } }, { label: 'Value date', text: function (d) { return d.value; } }], rows: D.fxDeals.filter(APP.pass) }; },
    Trade: function () { return { cols: [{ label: 'Reference', text: function (t) { return t.id; } }, { label: 'Instrument', text: function (t) { return t.type; } }, { label: 'Amount', text: function (t) { return t.amount + ' ' + t.ccy; } }, { label: 'Expires', text: function (t) { return t.expiry; } }], rows: D.trade.filter(APP.pass) }; }
  };
  function reportData(r) { return (REPORT_DATA[r.category] || REPORT_DATA.Liquidity)(); }
  V.reports = function () {
    var monthsL = [], d0 = new Date(D.asAt + 'T00:00:00Z');
    for (var i = 11; i >= 0; i--) { var d = new Date(Date.UTC(d0.getUTCFullYear(), d0.getUTCMonth() - i, 1)); monthsL.push(d.toISOString().slice(0, 7)); }
    var cats = ['Liquidity', 'Risk', 'Payments', 'Markets'];
    APP.chart(tile('rp-c-runs'), { title: 'Report runs per month, by category', legend: cats.concat(['Other']),
      spec: { type: 'stacked-column', categories: monthsL.map(function (m) { return APP.dshort(m + '-01').split(' ')[1] + ' ' + m.slice(2, 4); }), categoryLabel: 'Month',
        series: cats.concat(['Other']).map(function (c) { return { name: c, values: monthsL.map(function (m, i) { return D.reports.filter(function (r) { return c === 'Other' ? cats.indexOf(r.category) < 0 : r.category === c; }).reduce(function (s, r) { return s + r.runs[i]; }, 0); }) }; }),
        caption: 'Number of report runs per month by report category, last 12 months' } });
    var cash = APP.series('cash');
    APP.chart(tile('rp-c-cash'), { title: 'Group cash position report — preview, ' + APP.rangeLabel(),
      spec: { type: 'line', categories: dateCats(), categoryLabel: 'Day', unit: '£m', series: [{ name: 'Group cash', values: cash.map(APP.m) }], caption: 'Group closing cash for the entities in view, £m GBP equivalent' } });
    APP.records(tile('rp-r-catalogue'), { id: 'catalogue', title: 'Report catalogue', noun: 'reports', primary: true, total: function () { return D.reports.length; },
      sub: function () { return 'Reports reflect the filters in view when generated'; },
      rows: function () { return D.reports.filter(function (r) { return APP.matchQ(r, ['name', 'category', 'frequency']); }); },
      sorts: [['name:asc', 'Name'], ['category:asc', 'Category'], ['lastRun:desc', 'Most recently run']],
      cols: [{ label: 'Report', v: function (r) { return r.name; } }, { label: 'Category', v: function (r) { return r.category; } }, { label: 'Frequency', v: function (r) { return r.frequency; } },
        { label: 'Last run', v: function (r) { return APP.date(r.lastRun); } }, { label: 'Default format', v: function (r) { return r.format; } }],
      card: function (r) { return { title: r.name, initials: r.category.slice(0, 2), desc: r.frequency + ' · last run ' + APP.dshort(r.lastRun), amount: r.format, status: null }; },
      open: function (r) { var fmt = { v: r.format === 'Excel' ? 'xlsx' : r.format.toLowerCase() };
        APP.drawer.open({ title: r.name, body: [kv([['Category', r.category], ['Frequency', r.frequency], ['Last run', APP.date(r.lastRun)], ['Scope', APP.state.filters.length ? APP.state.filters.map(function (f) { return f.value; }).join(', ') : 'Whole group']]),
          APP.dropdown('Format', [['csv', 'CSV'], ['xlsx', 'Excel'], ['pdf', 'PDF']], fmt.v, function (v) { fmt.v = v; })],
          actions: [{ label: 'Generate now', onClick: function () { APP.generateReport(r, fmt.v); } }] }); } });
    var hist = (S.wf.rep || []).slice().reverse();
    APP.records(tile('rp-r-history'), { id: 'history', title: 'Generated reports', noun: 'generated reports', rows: function () { return hist.filter(function (h) { return APP.matchQ(h, ['name', 'id', 'format']); }); },
      sorts: [['when:desc', 'Newest first'], ['name:asc', 'Report']],
      cols: [{ label: 'Run', v: function (h) { return h.id; } }, { label: 'Report', v: function (h) { return h.name; } }, { label: 'Generated', v: function (h) { return h.when; } },
        { label: 'Format', v: function (h) { return h.format.toUpperCase(); } }, { label: 'Rows', num: true, v: function (h) { return String(h.rows); } }, { label: 'Status', v: function () { return APP.stat('ok', 'Ready'); } }],
      card: function (h) { return { title: h.name, initials: h.format.slice(0, 2).toUpperCase(), desc: h.id + ' · ' + h.when, amount: h.rows + ' rows', status: ['ok', 'Ready'] }; },
      open: function (h) { var r = D.reports.filter(function (x) { return x.id === h.report; })[0];
        APP.drawer.open({ title: h.name + ' · ' + h.id, body: [kv([['Generated', h.when], ['Format', h.format.toUpperCase()], ['Rows', String(h.rows)], ['Scope', h.scope]])],
          actions: [{ label: 'Download', onClick: function () { var dd = reportData(r); APP.toast('ok', APP.exportRows(h.format, h.name, dd.cols, dd.rows)); } }] }); } });
  };
  APP.generateReport = function (r, fmt) {
    var dd = reportData(r), id = 'RUN-' + (1000 + (S.wf.rep || []).length + 1);
    S.wf.rep.push({ id: id, report: r.id, name: r.name, when: APP.now(), format: fmt, rows: dd.rows.length, scope: S.filters.length ? S.filters.map(function (f) { return f.value; }).join(', ') : 'Whole group' });
    APP.save(); APP.drawer.close(true); APP.toast('ok', r.name + ' generated as ' + id + ' — download it from Generated reports.'); APP.refresh();
  };

  V.messages = function () {
    var srs = APP.srs().filter(function (r) { return APP.pass(r) && APP.inRange(r.opened) && APP.matchQ(r, ['id', 'type', 'status', 'priority', 'summary']); });
    var stc = by(srs, 'status', function () { return 1; }), sk = Object.keys(stc).slice(0, 5);
    if (sk.length) { APP.chart(tile('ms-c-status'), { title: 'Service requests by status', legend: sk,
      spec: { type: 'donut', categories: sk, categoryLabel: 'Status', series: [{ name: 'Requests', values: sk.map(function (k) { return stc[k]; }) }], caption: 'Number of service requests by status' } }); }
    else { tile('ms-c-status').textContent = ''; tile('ms-c-status').appendChild(APP.empty('No service requests in view', 'Widen the date range or clear the filters.', null)); }
    var weeks = [], w0 = new Date(D.asAt + 'T00:00:00Z');
    for (var i = 11; i >= 0; i--) { var a = new Date(w0.getTime() - (i + 1) * 7 * 864e5), b = new Date(w0.getTime() - i * 7 * 864e5); weeks.push([a.toISOString().slice(0, 10), b.toISOString().slice(0, 10)]); }
    var allMsgs = D.messages.filter(APP.pass), allSr = APP.srs().filter(APP.pass);
    APP.chart(tile('ms-c-weekly'), { title: 'Messages received and requests opened per week', legend: ['Messages', 'Service requests'],
      spec: { type: 'grouped-column', categories: weeks.map(function (w) { return APP.dshort(w[1]); }), categoryLabel: 'Week ending',
        series: [{ name: 'Messages', values: weeks.map(function (w) { return allMsgs.filter(function (m) { return m.date > w[0] && m.date <= w[1]; }).length; }) },
                 { name: 'Service requests', values: weeks.map(function (w) { return allSr.filter(function (r) { return r.opened > w[0] && r.opened <= w[1]; }).length; }) }],
        caption: 'Messages received and service requests opened per week, last 12 weeks' } });
    var msgs = D.messages.filter(function (m) { return APP.pass(m) && APP.inRange(m.date) && APP.matchQ(m, ['subject', 'from', 'category', 'body']); });
    var unread = msgs.filter(function (m) { return !APP.msgRead(m); }).length;
    APP.records(tile('ms-r-inbox'), { id: 'inbox', title: 'HSBC messages (' + unread + ' unread)', noun: 'messages', primary: true, total: function () { return D.messages.length; },
      rows: function () { return msgs.map(function (m) { m.rd = APP.msgRead(m) ? 'Read' : 'Unread'; return m; }); }, sorts: [['date:desc', 'Newest first'], ['rd:desc', 'Unread first'], ['from:asc', 'Sender']],
      cols: [{ label: 'Subject', v: function (m) { return m.subject; } }, { label: 'From', v: function (m) { return m.from; } },
        { label: 'Received', v: function (m) { return APP.dshort(m.date); } }, { label: 'Category', v: function (m) { return m.category; } }, { label: 'Status', v: function (m) { return APP.stat(m.rd === 'Unread' ? 'warn' : 'neu', m.rd); } }],
      card: function (m) { return { title: m.subject, initials: 'HS', avatar: m.from, desc: m.from + ' · ' + APP.dshort(m.date), amount: m.category, status: [m.rd === 'Unread' ? 'warn' : 'ok', m.rd] }; },
      open: APP.openMessage });
    APP.records(tile('ms-r-requests'), { id: 'requests', title: 'Service requests', noun: 'service requests', total: function () { return APP.srs().length; }, rows: function () { return srs; },
      sorts: [['opened:desc', 'Newest first'], ['status:asc', 'Status'], ['priority:asc', 'Priority']],
      cols: [{ label: 'Request', v: function (r) { return r.id; } }, { label: 'Type', v: function (r) { return r.type; } }, { label: 'Entity', v: function (r) { return APP.ent(r.entity).short; } },
        { label: 'Priority', v: function (r) { return r.priority; } }, { label: 'Opened', v: function (r) { return APP.date(r.opened); } }, { label: 'Status', v: function (r) { return APP.stat(APP.statusKind(r.status), r.status); } }],
      card: function (r) { return { title: r.type, initials: 'SR', desc: r.id + ' · ' + APP.ent(r.entity).short + ' · ' + r.priority, amount: 'Opened ' + APP.dshort(r.opened), status: [APP.statusKind(r.status), r.status] }; },
      open: APP.openRequest });
  };
  APP.openMessage = function (m) {
    var w = S.wf.msg[m.id] = S.wf.msg[m.id] || {}; var wasUnread = !APP.msgRead(m); w.read = true; w.thread = w.thread || []; APP.save();
    var entries = [{ when: m.date + ' 08:30', text: 'Message from ' + m.from, who: 'HSBC', tone: 'inf', note: m.body }].concat(w.thread);
    APP.drawer.open({ title: m.subject, body: [kv([['From', m.from], ['Received', APP.date(m.date)], ['Entity', APP.ent(m.entity).name], ['Category', m.category]]), para(m.body),
      APP.timeline('Conversation', entries), APP.note('Reply', 'At least 5 characters. Replies are simulated — HSBC does not receive them.')],
      dirty: function () { return APP.noteValue().length > 0; }, focus: '#t1',
      actions: [{ label: 'Send reply', onClick: function () { var n = APP.noteValue(); if (n.length < 5) { APP.noteError('Write at least 5 characters before sending.'); return; }
        w.thread.push({ when: APP.now(), text: 'Your reply', who: 'You (CEO)', tone: 'ok', note: n });
        w.thread.push({ when: APP.now(), text: 'Automatic acknowledgement', who: 'HSBC', tone: 'inf', note: 'Thank you — your relationship team will respond within one business day. (Simulated.)' });
        APP.save(); APP.drawer.close(true); APP.toast('ok', 'Reply sent on "' + m.subject + '" (simulated).'); APP.refresh(); } },
        { label: 'Close', kind: 'secondary', onClick: function () { APP.drawer.close(); } }], onClose: wasUnread ? function () { APP.refresh(); } : null });
  };
  APP.openRequest = function (r) {
    var waiting = r.status === 'Awaiting your information';
    APP.drawer.open({ title: r.id + ' · ' + r.type, body: [kv([['Status', APP.stat(APP.statusKind(r.status), r.status)], ['Entity', APP.ent(r.entity).name], ['Priority', r.priority], ['Opened', APP.date(r.opened)],
      ['Resolved in', r.resolutionDays ? r.resolutionDays + ' days' : '—']]), APP.el('p', 't-ed-body', r.summary), APP.timeline('Updates', r.updates.map(function (u) { return { when: u.date.length > 10 ? u.date : u.date + ' 09:00', text: u.text, who: u.who || 'HSBC', tone: u.tone || 'inf', note: u.note }; })),
      r.status !== 'Resolved' ? APP.note(waiting ? 'Information requested by HSBC' : 'Add an update', waiting ? 'At least 10 characters. Sending moves the request back to HSBC.' : 'At least 10 characters.') : null],
      focus: r.status !== 'Resolved' ? '#t1' : null,
      actions: r.status === 'Resolved' ? [] : [{ label: waiting ? 'Send information' : 'Add update', onClick: function () { var n = APP.noteValue();
        if (n.length < 10) { APP.noteError('Write at least 10 characters.'); return; }
        var u = S.wf.srUpd[r.id] = S.wf.srUpd[r.id] || { updates: [] }; if (waiting) { u.status = 'In progress'; }
        u.updates.push({ date: APP.now(), text: waiting ? 'Information sent by you' : 'Update from you', who: 'You (CEO)', tone: 'ok', note: n }); APP.save();
        APP.drawer.close(true); APP.toast('ok', r.id + ' updated.'); APP.refresh(); } }, { label: 'Close', kind: 'secondary', onClick: function () { APP.drawer.close(); } }] });
  };
  var SR_TYPES = ['Facility amendment', 'FX quote request', 'Signatory mandate change', 'New account opening', 'Payment investigation', 'KYC document refresh', 'Card programme change'];
  APP.newRequest = function (type, entity, text) {
    var form = { type: type || SR_TYPES[0], entity: entity || D.entities[0].id, priority: 'Standard' };
    var box = APP.el('div', 'ceo-stack');
    box.appendChild(APP.dropdown('Request type', SR_TYPES.map(function (t) { return [t, t]; }), form.type, function (v) { form.type = v; }));
    box.appendChild(APP.dropdown('Entity', D.entities.map(function (e) { return [e.id, e.name]; }), form.entity, function (v) { form.entity = v; }));
    var pl = APP.el('span', 't-cm-label', 'Priority'); box.appendChild(pl);
    box.appendChild(APP.seg('Priority', [['Standard', 'Standard'], ['High', 'High'], ['Urgent', 'Urgent']], 'Standard', function (v) { form.priority = v; }));
    box.appendChild(APP.note('What do you need?', 'At least 20 characters. HSBC client service sees exactly this text.', text || ''));
    APP.drawer.open({ title: 'New service request', body: [box], dirty: function () { return APP.noteValue().length > 0 && APP.noteValue() !== (text || ''); }, focus: '#t1',
      actions: [{ label: 'Submit request', onClick: function () { var n = APP.noteValue();
        if (n.length < 20) { APP.noteError('Describe the request in at least 20 characters so HSBC can act on it.'); return; }
        var e = APP.ent(form.entity), id = 'SR-' + (70000 + (S.wf.srNew || []).length + 1);
        S.wf.srNew.push({ id: id, type: form.type, entity: e.id, region: e.region, ccy: e.ccy, priority: form.priority, opened: D.asAt, status: 'Submitted', resolutionDays: null, summary: n,
          updates: [{ date: APP.now(), text: 'Submitted by you', who: 'You (CEO)', tone: 'ok' }, { date: APP.now(), text: 'Received by HSBC client service (simulated)', who: 'HSBC', tone: 'inf' }] });
        S.sort.requests = 'opened:desc'; APP.save(); APP.drawer.close(true); APP.toast('ok', id + ' submitted — ' + form.type.toLowerCase() + ', ' + form.priority.toLowerCase() + ' priority.');
        if (S.view !== 'messages') { APP.go('messages'); } else { APP.refresh(); } var rq = tile('ms-r-requests'); if (rq) { rq.scrollIntoView({ block: 'start' }); } } },
        { label: 'Cancel', kind: 'secondary', onClick: function () { APP.drawer.close(); } }] });
  };

  V.settings = function () {
    var d = tile('st-f-display');
    if (!d.__built) { d.__built = true; d.textContent = '';
      var st = APP.el('div', 'ceo-stack'); st.appendChild(APP.el('h3', 't-cm-section-label', 'Display'));
      st.appendChild(APP.el('span', 't-cm-label', 'Theme'));
      d.__theme = APP.seg('Theme', [['light', 'Light'], ['dark', 'Dark']], S.theme, function (v) { APP.setTheme(v); }); st.appendChild(d.__theme);
      st.appendChild(APP.el('span', 't-cm-label', 'Show records as'));
      d.__rv = APP.seg('Show records as', [['table', 'Table'], ['cards', 'Cards']], S.recView, function (v) { APP.setRecView(v); }); st.appendChild(d.__rv);
      st.appendChild(APP.dropdown('Open the prototype on', APP.NAV.map(function (n) { return [n[0], n[1]]; }), S.prefs.defaultView, function (v) { S.prefs.defaultView = v; APP.save(); APP.toast('ok', 'The prototype will open on ' + APP.navLabel(v) + ' when no view is in the address.'); }));
      d.appendChild(st);
      var nt = tile('st-f-notify'); nt.textContent = '';
      var ns = APP.el('div', 'ceo-stack'); ns.appendChild(APP.el('h3', 't-cm-section-label', 'Notify me about'));
      var sc = APP.tpl('sc'), sw = sc.querySelector('input[role="switch"]').closest('.field');
      [['approvals', 'Payments waiting for my approval'], ['breaches', 'Limit breaches and material exceptions'], ['messages', 'New HSBC messages'], ['digest', 'A weekly digest by email']].forEach(function (x) {
        var f = sw.cloneNode(true), inp = f.querySelector('input'), lab = f.querySelector('label');
        inp.id = 'ceo-sw-' + x[0]; lab.setAttribute('for', inp.id); lab.lastChild.textContent = ' ' + x[1]; inp.checked = !!S.prefs.notify[x[0]];
        inp.addEventListener('change', function () { S.prefs.notify[x[0]] = inp.checked; APP.save(); APP.toast('ok', x[1] + (inp.checked ? ' — on.' : ' — off.')); });
        ns.appendChild(APP.scope('cn-selection-controls', f)); });
      ns.appendChild(APP.el('p', 't-ed-body-small', 'Notification preferences are stored in this browser only. Nothing is sent.'));
      nt.appendChild(ns);
      var dt = tile('st-f-data'); dt.textContent = '';
      var ds = APP.el('div', 'ceo-stack'); ds.appendChild(APP.el('h3', 't-cm-section-label', 'Prototype data'));
      ds.appendChild(APP.el('p', 't-ed-body', 'All entities, balances, counterparties and rates are illustrative placeholders. Reporting currency is GBP; every GBP figure is the local amount multiplied by the illustrative rate on the FX and markets page. There is no connection to any bank, and no credential is asked for or stored.'));
      ds.appendChild(APP.el('p', 't-ed-body-small', D.fxNote + '.'));
      ds.appendChild(APP.button('Reset the prototype', 'secondary', function () { APP.modal.open({ title: 'Reset the prototype?', text: 'This clears every approval, acknowledgement, reply, request, generated report and preference stored in this browser, then reloads.', confirmLabel: 'Reset and reload',
        onConfirm: function () { try { localStorage.removeItem('ceo-proto-v1'); } catch (e) { /* nothing stored */ } location.href = location.pathname; } }); }));
      dt.appendChild(ds);
    } else { APP.segSet(d.__theme, S.theme); APP.segSet(d.__rv, S.recView); }
    var a = D.alertsSent.slice(30 - Math.min(30, S.days));
    APP.chart(tile('st-c-alerts'), { title: 'Alerts delivered per day, ' + (S.days > 30 ? 'last 30 days (the alert log keeps 30)' : APP.rangeLabel()),
      spec: { type: 'line', categories: D.dates.slice(90 - a.length).map(APP.dshort), categoryLabel: 'Day', series: [{ name: 'Alerts', values: a }], caption: 'Number of alerts delivered per day' } });
    APP.setResult(0, 0, 'settings');
  };
}());
