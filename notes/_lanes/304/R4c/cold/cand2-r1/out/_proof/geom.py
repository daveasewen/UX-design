import os, json, sys
from playwright.sync_api import sync_playwright
W = os.path.expanduser("~/cold/cand2-r1"); OUT = W + "/out"
pages = sys.argv[1:] or ["index", "accounts", "liquidity", "payments", "fx", "risk", "trade", "reports", "messages", "settings"]
JS = r"""() => {
  const R = e => e.getBoundingClientRect();
  const out = {page: document.body.dataset.page, rows: [], deadSpace: [], gutters: [], hscroll: [], small: [], misc: {}};
  // tiles sharing a row share top and bottom edges (every bento grid, both levels)
  document.querySelectorAll('.c-bento__grid').forEach((g, gi) => {
    const tiles = [...g.children].filter(t => t.classList.contains('c-bento__tile'));
    const byTop = {};
    tiles.forEach(t => { const r = R(t); const k = Math.round(r.top); (byTop[k] = byTop[k] || []).push(r); });
    Object.values(byTop).forEach(rs => { if (rs.length > 1) { const b = rs.map(r => r.bottom); out.rows.push({grid: gi, n: rs.length, bottomSpread: +(Math.max(...b) - Math.min(...b)).toFixed(1)}); } });
    // gutters: horizontal gap between neighbours in a row, vertical gap between rows
    Object.values(byTop).forEach(rs => { rs.sort((a, b) => a.left - b.left); for (let i = 1; i < rs.length; i++) out.gutters.push({grid: gi, dir: 'x', gap: +(rs[i].left - rs[i-1].right).toFixed(1)}); });
    const tops = Object.keys(byTop).map(Number).sort((a, b) => a - b);
    for (let i = 1; i < tops.length; i++) { const prevBottom = Math.max(...byTop[tops[i-1]].map(r => r.bottom)); out.gutters.push({grid: gi, dir: 'y', gap: +(tops[i] - prevBottom).toFixed(1)}); }
  });
  // dead space: panel bottom padding edge vs its last content bottom
  document.querySelectorAll('.stat-card.c-bento__tile, .c-bento__tile > .cn-kpi-tile').forEach(p => {
    const pr = R(p), cs = getComputedStyle(p); let maxB = pr.top;
    [...p.children].forEach(e => { const r = R(e); if (r.height > 0 && r.width > 0 && getComputedStyle(e).position !== 'fixed') maxB = Math.max(maxB, r.bottom); });
    const dead = pr.bottom - parseFloat(cs.paddingBottom) - maxB;
    out.deadSpace.push({id: p.id || (p.querySelector('figure') || {}).id || (p.querySelector('[data-kpi]') || {dataset:{}}).dataset.kpi || p.className.slice(0, 30), dead: +dead.toFixed(1), h: +pr.height.toFixed(1)});
  });
  // horizontal overflow
  [document.documentElement, document.querySelector('.sh-content'), document.querySelector('.sh-main')].forEach(e => { if (e && e.scrollWidth > e.clientWidth + 1) out.hscroll.push((e.className || e.tagName) + ' ' + e.scrollWidth + '>' + e.clientWidth); });
  document.querySelectorAll('.stat-card, .kpi-tile').forEach(e => { if (e.scrollWidth > e.clientWidth + 1) out.hscroll.push('panel ' + (e.id || e.className.slice(0, 40)) + ' ' + e.scrollWidth + '>' + e.clientWidth); });
  // small targets (visible interactive < 24px either side)
  document.querySelectorAll('button, a[href], input, [role=option], [tabindex="0"]').forEach(e => { const r = R(e); if (r.width > 0 && r.height > 0 && (r.width < 24 || r.height < 24) && e.offsetParent !== null && !e.closest('.sn') ) out.small.push((e.tagName + '.' + (e.className.baseVal !== undefined ? e.className.baseVal : e.className)).slice(0, 40) + ' ' + Math.round(r.width) + 'x' + Math.round(r.height) + ' ' + (e.textContent || e.getAttribute('aria-label') || '').trim().slice(0, 30)); });
  // filter row: controls share a bottom edge
  const fr = document.querySelector('[aria-label="Shared filters"]');
  if (fr) { const cs = [...fr.querySelectorAll('.trigger, .seg')].map(e => R(e)); out.misc.filterBottoms = cs.map(r => +r.bottom.toFixed(1)); out.misc.filterHeights = cs.map(r => +r.height.toFixed(1)); out.misc.filterGap = getComputedStyle(fr).columnGap; }
  const sh = document.querySelector('.sh'); out.misc.shell = sh ? [Math.round(R(sh).width), Math.round(R(sh).height)] : null;
  const ground = document.querySelector('.ceo-ground'); if (ground) { const g = R(ground), w = R(ground.querySelector('.tpl-wall')); out.misc.ground = {bg: getComputedStyle(ground).backgroundColor, insetTop: +(w.top - g.top).toFixed(1), insetLeft: +(w.left - g.left).toFixed(1), insetRight: +(g.right - w.right).toFixed(1), insetBottom: +(g.bottom - w.bottom).toFixed(1)}; const ph = document.querySelector('.cn-page-header-lockup'); out.misc.titleBg = getComputedStyle(document.querySelector('.sh-main')).backgroundColor; }
  const panel = document.querySelector('.stat-card.c-bento__tile'); if (panel) { const cs = getComputedStyle(panel); out.misc.panel = {bg: cs.backgroundColor, pad: cs.padding, border: cs.borderTopWidth}; }
  return out;
}"""
res = {}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ["RENDER_SHELL"])
    for vw in [int(os.environ.get("VW", "1440"))]:
        ctx = b.new_context(viewport={"width": vw, "height": 900})
        for name in pages:
            pg = ctx.new_page(); pg.goto("file://%s/%s.html" % (OUT, name)); pg.wait_for_timeout(600)
            r = pg.evaluate(JS)
            res[name] = r; pg.close()
    b.close()
for k, r in res.items():
    rows = [x for x in r["rows"] if x["bottomSpread"] > 0.5]
    gx = sorted({(x["grid"], x["dir"], x["gap"]) for x in r["gutters"]})
    dead = [x for x in r["deadSpace"] if x["dead"] > 8]
    print("==", k, "shell", r["misc"].get("shell"), "ground", r["misc"].get("ground"), "panel", r["misc"].get("panel"))
    print("   ragged rows:", rows)
    print("   gutters:", gx)
    print("   dead>8px:", dead)
    print("   hscroll:", r["hscroll"])
    print("   small:", r["small"][:12], len(r["small"]))
    print("   filters:", r["misc"].get("filterBottoms"), r["misc"].get("filterHeights"), r["misc"].get("filterGap"))
