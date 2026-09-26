"""Driven proof B — DOM geometry and computed spacing, read from the page (not from a screenshot)."""
import os, json, sys
from playwright.sync_api import sync_playwright
W = os.path.expanduser('~/cold/cand-r2'); URL = 'file://' + W + '/out/index.html'; SN = 'file://' + W + '/pack/knowledge/snippets/'
R = []; CON = []
def ok(name, cond, detail=''): R.append({'check': name, 'pass': bool(cond), 'detail': detail})
GEO = """() => { const R = e => { const b = e.getBoundingClientRect(); return {l: b.left, t: b.top, w: b.width, h: b.height, r: b.right, b: b.bottom}; };
  const v = document.querySelector('.app-view:not([hidden])'), out = {groups: [], rows: [], deadspace: [], overflow: []};
  v.querySelectorAll('.tpl-group').forEach(g => {
    const grid = g.querySelector(':scope > .c-bento__grid'), tiles = [...grid.children].map(R);
    const rows = {}; tiles.forEach(t => { const k = Math.round(t.t); (rows[k] = rows[k] || []).push(t); });
    Object.values(rows).forEach(row => { out.rows.push({group: g.getAttribute('aria-label').slice(0, 24), n: row.length, bottoms: row.map(t => Math.round(t.b)), hgap: row.slice(1).map((t, i) => Math.round((t.l - row[i].r) * 10) / 10)}); });
    out.groups.push({label: g.getAttribute('aria-label').slice(0, 24), gap: getComputedStyle(grid).gap, tiles: tiles.length});
  });
  out.wallGaps = []; v.querySelectorAll('.tpl-wall').forEach(w => { const gs = [...w.querySelectorAll(':scope > .c-bento__grid > .tpl-group')].map(R); gs.slice(1).forEach((g, i) => out.wallGaps.push(Math.round(g.t - gs[i].b))); });
  const walls = [...v.querySelectorAll('.tpl-wall')].map(R); out.sectionGaps = walls.slice(1).map((w, i) => Math.round(w.t - walls[i].b));
  v.querySelectorAll('.tpl-group .stat-card').forEach(t => { const tb = R(t), cs = getComputedStyle(t), inner = t.firstElementChild, last = inner.lastElementChild || inner;
    const contentBottom = Math.max(...[...inner.querySelectorAll(':scope > *')].map(c => R(c).b));
    out.deadspace.push({k: (t.querySelector('[data-chart]') || {}).dataset ? (t.querySelector('[data-chart]') || t).getAttribute('data-chart') || t.getAttribute('data-panel') || 'panel' : '', pad: cs.paddingTop + ' ' + cs.paddingLeft, dead: Math.round(tb.b - parseFloat(cs.paddingBottom) - contentBottom)}); });
  const main = document.querySelector('.sh-main'), mb = R(main);
  main.querySelectorAll('*').forEach(e => { if (e.closest('[hidden]') || e.closest('.sh-sheet') || e.closest('details:not([open]) > :not(summary)')) return; const b = R(e); if (b.w && b.r > mb.r + 0.5) out.overflow.push((e.className || e.tagName).toString().slice(0, 40) + ' r=' + Math.round(b.r)); });
  const content = document.querySelector('.sh-content'); out.hscroll = content.scrollWidth - content.clientWidth;
  const ph = R(document.querySelector('.ph')), ftb = R(document.querySelector('.ftb-outer')), stack = R(document.querySelector('.sh-main .l-stack'));
  out.bars = {ph: [Math.round(ph.l), Math.round(ph.w)], ftb: [Math.round(ftb.l), Math.round(ftb.w)], stack: [Math.round(stack.l), Math.round(stack.w)], stackGap: getComputedStyle(document.querySelector('.sh-main .l-stack')).rowGap, viewGap: getComputedStyle(v).rowGap};
  const gr = v.querySelector('.app-ground'); if (gr) { const gb = R(gr), first = R(v.querySelector('.tpl-group')); out.ground = {padTop: getComputedStyle(gr).paddingTop, firstGroupInset: Math.round(first.t - gb.t), side: Math.round(first.l - gb.l), bg: getComputedStyle(gr).backgroundColor}; }
  return out; }"""
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ['RENDER_SHELL'])
    pg = b.new_page(viewport={'width': 1920, 'height': 1080})
    pg.on('console', lambda m: CON.append([m.type, m.text[:200]]) if m.type in ('error',) else None)
    pg.on('pageerror', lambda e: CON.append(['pageerror', str(e)[:300]]))
    pg.goto(URL + '#/overview'); pg.evaluate("() => { try { localStorage.clear(); } catch(e){} }"); pg.goto(URL + '#/overview'); pg.wait_for_timeout(1500)
    views = sys.argv[1:] or ['overview', 'accounts', 'liquidity', 'payments', 'fx', 'risk', 'trade', 'reports', 'messages', 'settings']
    for mode in ['light', 'dark']:
        pg.evaluate("m => document.documentElement.setAttribute('data-theme', m)", mode)
        for v in views:
            pg.evaluate("v => { location.hash = '#/' + v; }", v); pg.wait_for_timeout(700)
            g = pg.evaluate(GEO)
            if mode == 'light':
                ok('%s: tiles sharing a row share their bottom edge' % v, all(len(set(r['bottoms'])) == 1 for r in g['rows']), g['rows'])
                ok('%s: gutters between tiles equal the group gap (4px)' % v, all(all(abs(x - 4) < 0.6 for x in r['hgap']) for r in g['rows']) and all(x['gap'] == '4px' for x in g['groups']), [r['hgap'] for r in g['rows']])
                ok('%s: gaps between groups inside a wall are equal' % v, len(set(g['wallGaps'])) <= 1, {'wall': g['wallGaps'], 'between sections (heading + gaps)': g['sectionGaps']})
                ok('%s: no dead space below tile content (<=24px)' % v, all(d['dead'] <= 24 for d in g['deadspace']), g['deadspace'])
                ok('%s: no horizontal overflow' % v, g['hscroll'] == 0 and not g['overflow'], (g['hscroll'], g['overflow'][:5]))
                ok('%s: filter bar as wide as the header and the content column' % v, g['bars']['ph'] == g['bars']['ftb'] == g['bars']['stack'], g['bars'])
                if g.get('ground'): ok('%s: bento ground is the lightest grey, inset on the 24 stop' % v, g['ground']['bg'] == 'rgb(240, 240, 240)' and g['ground']['padTop'] == '24px', g['ground'])
                R[-1]['geo'] = g
            else:
                ok('%s (dark): no horizontal overflow' % v, g['hscroll'] == 0 and not g['overflow'], (g['hscroll'], g['overflow'][:5]))
    pg.evaluate("() => document.documentElement.setAttribute('data-theme', 'light')")
    # component sizes against their reference snippet (the showroom page embeds the same file)
    pg.evaluate("() => { location.hash = '#/overview'; }"); pg.wait_for_timeout(600)
    mine = pg.evaluate("""() => { const h = s => { const e = document.querySelector(s); if (!e) return null; const b = e.getBoundingClientRect(); const c = getComputedStyle(e); return {h: Math.round(b.height*10)/10, w: Math.round(b.width), pad: c.padding, font: c.fontSize}; };
        return {kpiVal: h('[data-kpi] .kpi-val'), kpiLbl: h('[data-kpi] .kpi-lbl'), kpiSpark: h('[data-kpi] .kpi-spark svg'), kpiDelta: h('[data-kpi] .kpi-delta'),
          seg: h('.ph-actions .seg'), segBtn: h('.ph-actions .seg button'), btn: h('.ph-actions .btn'), trig: h('#flt-entity-t'), summaryRow: h('[data-panel] .summary__row')}; }""")
    pg.evaluate("() => { location.hash = '#/accounts'; }"); pg.wait_for_timeout(600)
    mine.update(pg.evaluate("""() => { const h = s => { const e = document.querySelector(s); const b = e.getBoundingClientRect(); const c = getComputedStyle(e); return {h: Math.round(b.height*10)/10, pad: c.padding}; };
        return {dgRow: h('[data-grid="txns"] tbody tr'), dgTd: h('[data-grid="txns"] tbody td'), dgTh: h('[data-grid="txns"] thead th'), dgSearch: h('[data-grid="txns"] .dgsearch'), pbtn: h('[data-grid="txns"] .pbtn')}; }"""))
    ref = {}
    for snip, js in [('Kpi-tile', """() => { const h = s => { const e = document.querySelector(s); const b = e.getBoundingClientRect(); const c = getComputedStyle(e); return {h: Math.round(b.height*10)/10, w: Math.round(b.width), pad: c.padding, font: c.fontSize}; }; return {kpiVal: h('.kpi-tile.as-link .kpi-val'), kpiLbl: h('.kpi-tile.as-link .kpi-lbl'), kpiSpark: h('.kpi-tile.as-link .kpi-spark svg'), kpiDelta: h('.kpi-tile.as-link .kpi-delta')}; }"""),
                     ('Segmented-control', """() => { const e = document.querySelector('.seg.md'), b = e.getBoundingClientRect(), bb = e.querySelector('button').getBoundingClientRect(); return {seg: {h: Math.round(b.height*10)/10}, segBtn: {h: Math.round(bb.height*10)/10}}; }"""),
                     ('Button', """() => { const b = document.querySelector('.btn.tertiary').getBoundingClientRect(); return {btn: {h: Math.round(b.height*10)/10}}; }"""),
                     ('Filter-toolbar-bar', """() => { const b = document.querySelector('.ftb-ctl.dd.boxed .trigger').getBoundingClientRect(); return {trig: {h: Math.round(b.height*10)/10}}; }"""),
                     ('Data-grid', """() => { const q = s => document.querySelector(s); const h = s => { const e = q(s); const b = e.getBoundingClientRect(); return {h: Math.round(b.height*10)/10, pad: getComputedStyle(e).padding}; }; return {dgRow: h('#tbody tr'), dgTd: h('#tbody td'), dgTh: h('thead tr.cols th'), dgSearch: h('.dgsearch'), pbtn: h('.pbtn')}; }""")]:
        pg2 = b.new_page(viewport={'width': 1440, 'height': 900}); pg2.goto(SN + snip + '.reference.html'); pg2.wait_for_timeout(900)
        try: ref.update(pg2.evaluate(js))
        except Exception as e: ref[snip] = 'not measured: ' + str(e)[:80]
        pg2.close()
    for k in ['kpiVal', 'kpiLbl', 'kpiSpark', 'kpiDelta', 'seg', 'segBtn', 'btn', 'trig', 'dgRow', 'dgTh', 'dgSearch', 'pbtn']:
        a, r = mine.get(k), ref.get(k)
        ok('size matches reference: ' + k, a and r and isinstance(r, dict) and abs(a['h'] - r['h']) <= 1, {'page': a, 'reference': r})
    ok('zero console errors across views and both modes', not CON, CON)
    b.close()
json.dump({'results': R, 'console': CON}, open(W + '/proof/drive-b.json', 'w'), indent=1)
print('%d/%d pass' % (sum(r['pass'] for r in R), len(R)))
for r in R:
    if not r['pass']: print('FAIL', r['check'], json.dumps(r['detail'])[:600])
