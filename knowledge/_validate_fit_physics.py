#!/usr/bin/env python3
"""_validate_fit_physics.py — the two-axis FIT physics gate (s248-D2/D3, s249-D4; #249 FIT lane).

The 19 checks of outputs/w2-debt/dp18/_render.py, run against every `svg.dv-fit` of Chart-line,
Chart-bar and Template-dashboard-bento, each figure placed in a FIXED 438px-tall .c-bento__tile
(the composed page's evidence tile, #248) at 1440 and 1100. The invariant under test is DV-D02:
the chart fills its tile's width AND height with y/height RE-DERIVED from data — the viewBox is
re-pinned 1:1 to the box in both axes, so text and strokes never scale, every mark rides its
line, every bar keeps its bake fraction, ticks keep their fixed offset, and a live resize returns.

Harness pages are BUILT here (outputs/fit-physics/<Target>.html): the snippet verbatim, plus one
script placed right before its AUTO-BEHAVIOUR block that wraps each figure.dv in the tile before
the engine's init pass runs — so the engine under test is the snippet's own injected partial,
not a copy. Playwright, goto('file://…') only.

Exit 0 iff every check passes on every target.

  python3 knowledge/_validate_fit_physics.py                # the gate
  python3 knowledge/_validate_fit_physics.py --mutate no-fity    # MUTATION: fitY removed → expect fails
  python3 knowledge/_validate_fit_physics.py --mutate scale      # MUTATION: viewBox scaled, not re-pinned → expect fails
  python3 knowledge/_validate_fit_physics.py --json out.json     # write the probe

A mutation rewrites the ENGINE TEXT INSIDE THE HARNESS COPY only (the source is never touched);
the expected result of a mutation is a non-zero exit — a gate that still passes with fitY gone
does not test the clause (memory: mutation-tests-the-clause-not-the-feature).
"""
import sys, os, re, json, argparse
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SNIP = os.path.join(HERE, 'snippets')
OUT = os.path.join(ROOT, 'outputs', 'fit-physics')
TILE_H = 438
TARGETS = ['Chart-line', 'Chart-bar', 'Template-dashboard-bento']
WIDTHS = (1440, 1100)

WRAP_JS = """<script>
/* fit-physics harness — wrap every figure.dv in a fixed %dpx .c-bento__tile BEFORE the engine's init pass */
(function(){
  var figs=document.querySelectorAll('figure.dv'), i;
  for(i=0;i<figs.length;i++){
    var f=figs[i]; if(f.closest('.c-bento__tile')){ f.closest('.c-bento__tile').setAttribute('style','height:%dpx;box-sizing:border-box;padding:24px;border:1px solid #ccc;display:flex;flex-direction:column;overflow:hidden'); continue; }
    var t=document.createElement('div'); t.className='c-bento__tile'; t.setAttribute('style','height:%dpx;box-sizing:border-box;padding:24px;border:1px solid #ccc;display:flex;flex-direction:column;overflow:hidden;margin:16px 0');
    f.parentNode.insertBefore(t,f); t.appendChild(f);
  }
  window.__errs=[]; window.addEventListener('error',function(e){window.__errs.push(String(e.message))});
}());
</script>
""" % (TILE_H, TILE_H, TILE_H)

MUTATIONS = {
    'no-fity': ("var Y = fitY(svg, H);", "var Y = null;"),
    'scale': ("var Y = fitY(svg, H);",
              "var Y = null; svg.setAttribute('viewBox', '0 0 ' + W + ' ' + parseFloat(svg.getAttribute('data-h') || '260')); svg.style.height = H + 'px';"),
}

def build_harness(target, mutate):
    src = open(os.path.join(SNIP, target + '.reference.html'), encoding='utf-8').read()
    marker = '<!-- ===== AUTO-BEHAVIOUR dv-behaviour START'
    if marker not in src:
        raise SystemExit('%s: no AUTO-BEHAVIOUR dv-behaviour block — not a dataviz member' % target)
    html = src.replace(marker, WRAP_JS + marker, 1)
    if mutate:
        old, new = MUTATIONS[mutate]
        if html.count(old) != 1:
            raise SystemExit('mutation %s: anchor found %d times' % (mutate, html.count(old)))
        html = html.replace(old, new)
    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, target + ('-' + mutate if mutate else '') + '.html')
    open(p, 'w', encoding='utf-8').write(html)
    return p, src

# per-svg probe: geometry AFTER the engine, plus the BAKE (parsed from the raw HTML string, pre-JS)
PROBE = r"""(raw)=>{
const doc=new DOMParser().parseFromString(raw,'text/html');
const bakeSvgs=[...doc.querySelectorAll('svg.dv-fit')];
const num=v=>parseFloat(v);
const shape=(el)=>{const t=el.tagName.toLowerCase();
  if(t==='circle')return {t,cy:num(el.getAttribute('cy')),size:num(el.getAttribute('r'))};
  if(t==='rect')return {t,cy:num(el.getAttribute('y'))+num(el.getAttribute('height'))/2,size:num(el.getAttribute('height')),w:num(el.getAttribute('width'))};
  const ys=el.getAttribute('points').trim().split(/\s+/).map(s=>num(s.split(',')[1]));return {t,cy:ys.reduce((a,b)=>a+b,0)/ys.length,size:+(Math.max(...ys)-Math.min(...ys)).toFixed(2)}};
const read=(svg)=>{
  const vb=svg.getAttribute('viewBox').split(' ').map(Number);
  const PT=num(svg.dataset.pt||14), PB=num(svg.dataset.pb||30), H0=num(svg.dataset.h||260);
  const hgrid=[...svg.querySelectorAll('line.dv-grid')].filter(l=>l.getAttribute('y1')===l.getAttribute('y2')).map(l=>num(l.getAttribute('y1')));
  const axisY=[...svg.querySelectorAll('line.dv-axis')].map(l=>Math.max(num(l.getAttribute('y1')),num(l.getAttribute('y2'))));
  const ticks=[...svg.querySelectorAll('text.dv-axis')].map(t=>({y:num(t.getAttribute('y')),dy:t.getAttribute('data-dy'),fs:getComputedStyle(t).fontSize}));
  const labels=[...svg.querySelectorAll('text.dv-label')].map(t=>({y:num(t.getAttribute('y')),fs:getComputedStyle(t).fontSize}));
  const pls=[...svg.querySelectorAll('polyline.dv-series,polyline[data-ys]')].map(p=>{const ys=p.getAttribute('points').trim().split(/\s+/).map(s=>num(s.split(',')[1]));return {ys,sw:getComputedStyle(p).strokeWidth,g:p.dataset.seriesGroup||'1'}});
  const bars=[...svg.querySelectorAll('rect.dv-series:not(.dv-mk)')].map(r=>({y:num(r.getAttribute('y')),h:num(r.getAttribute('height'))}));
  const marks=[...svg.querySelectorAll('g.dv-marker')].map(g=>({g:g.dataset.seriesGroup||'1',...shape(g.querySelector('.dv-mk'))}));
  const grid1=svg.querySelector('line.dv-grid'), ser1=svg.querySelector('.dv-series');
  return {vbW:vb[2],vbH:vb[3],PT,PB,H0,hgrid,gridN:svg.querySelectorAll('line.dv-grid').length,axisY,ticks,labels,pls,bars,marks,
    gridStroke:grid1?getComputedStyle(grid1).strokeWidth:null, seriesStroke:ser1?getComputedStyle(ser1).strokeWidth:null};
};
const out=[...document.querySelectorAll('svg.dv-fit')].map((svg,i)=>{
  const fig=svg.closest('figure.dv'), tile=fig.closest('.c-bento__tile'); const cs=getComputedStyle(tile);
  const edge=tile.getBoundingClientRect().bottom-parseFloat(cs.paddingBottom)-parseFloat(cs.borderBottomWidth);
  const b=svg.getBoundingClientRect(); const bake=read(bakeSvgs[i]);
  const after=read(svg);
  return {i,label:svg.getAttribute('aria-label').slice(0,40),svg:{w:+b.width.toFixed(1),h:+b.height.toFixed(1)},tile:{h:+tile.getBoundingClientRect().height.toFixed(1)},
    slack:+(edge-fig.getBoundingClientRect().bottom).toFixed(1),after,bake};
});
return {svgs:out,errs:window.__errs||[]};
}"""

def near(a, b, tol=0.15): return abs(a - b) <= tol

def checks_for(A, B, live):
    """A = probe at 1440, B = at 1100 (one svg each); live = [(w, vbW, vbH, slack)]. Returns {name: bool}."""
    a, b, k = A['after'], B['after'], A['bake']
    baseA = a['vbH'] - a['PB']; base0 = k['H0'] - k['PB']
    plotA = a['vbH'] - a['PT'] - a['PB']; plot0 = k['H0'] - k['PT'] - k['PB']
    # 14: marks on their line (line charts) / bars keep their bake fractions (bar charts)
    on_data = True
    if a['marks']:
        idx = {}
        for m in a['marks']:            # a mark rides its line: its centre == some series polyline's y at its point index
            j = idx.get(m['g'], 0); idx[m['g']] = j + 1
            cands = [p['ys'][j % len(p['ys'])] for p in a['pls'] if p['g'] == m['g'] and p['ys']]
            if not cands or not any(near(m['cy'], y) for y in cands): on_data = False
    for r0, r1 in zip(k['bars'], a['bars']):
        if not (near((r1['y'] - a['PT']) / plotA, (r0['y'] - k['PT']) / plot0, 0.004) and
                near((r1['y'] + r1['h'] - a['PT']) / plotA, (r0['y'] + r0['h'] - k['PT']) / plot0, 0.004)): on_data = False
    # 16: ticks with data-dy sit their offset under their gridline (index-paired with the horizontal gridlines)
    tick_ok = True                  # a tick with a dy sits exactly dy under its NEAREST gridline (or the baseline)
    anchors = a['hgrid'] + [baseA]
    for t in a['ticks']:
        if t['dy'] is None: continue
        y = t['y'] - float(t['dy']); nearest = min(anchors, key=lambda g: abs(g - y))
        if not near(y, nearest): tick_ok = False
    # 17: every text BELOW the baseline in the bake keeps its offset from the baseline (labels at baseline+16)
    below_ok = True
    for t0, t1 in zip(k['labels'] + k['ticks'], a['labels'] + a['ticks']):
        if t0['y'] > base0 + 0.5 and not near(t1['y'] - baseA, t0['y'] - base0): below_ok = False
    ys_all = [y for p in a['pls'] for y in p['ys']] + [r['y'] for r in a['bars']] + [r['y'] + r['h'] for r in a['bars']]
    grid_max = max(a['hgrid']) if a['hgrid'] else (max(a['axisY']) if a['axisY'] else baseA)
    return {
        '01 bake: tile had >20px slack under the figure at data-h (the defect exists)': A['slack'] + (a['vbH'] - k['H0']) > 20,
        '02 1440: slack under the figure < 1px': abs(A['slack']) < 1,
        '03 1440: svg box == viewBox in BOTH axes (1:1 pin)': near(A['svg']['h'], a['vbH'], 1) and near(A['svg']['w'], a['vbW'], 1),
        '04 1100: svg box h == viewBox h': near(B['svg']['h'], b['vbH'], 1),
        '05 1100: slack under the figure < 1px': abs(B['slack']) < 1,
        '06 tick font-size equal 1440 vs 1100 (one value)': len({t['fs'] for t in a['ticks']} | {t['fs'] for t in b['ticks']}) <= 1,
        '07 label font-size equal 1440 vs 1100 (one value)': len({t['fs'] for t in a['labels']} | {t['fs'] for t in b['labels']}) <= 1,
        '08 grid stroke equal across widths': a['gridStroke'] == b['gridStroke'],
        '09 series stroke equal across widths': a['seriesStroke'] == b['seriesStroke'],
        '10 gridline count unchanged vs bake': a['gridN'] == k['gridN'],
        '11 1440: lowest gridline/axis == baseline (vbH - PB)': near(grid_max, baseA, 0.6),
        '12 1440: no gridline outside the box': grid_max <= a['vbH'],
        '13 1440: every series y within [PT, vbH - PB]': all(a['PT'] - 0.6 <= y <= baseA + 0.6 for y in ys_all),
        '14 1440: every mark rides its line / every bar keeps its bake fraction': on_data,
        '15 mark glyph sizes unchanged vs bake': [m['size'] for m in a['marks']] == [m['size'] for m in k['marks']],
        '16 1440: data-dy ticks sit their offset under their gridline': tick_ok,
        '17 below-baseline text keeps its bake offset (labels at baseline+16)': below_ok,
        '18 live resize 1440->1100->1440 returns (viewBox equal, 1100 differs)': live[0][1:3] == live[2][1:3] and live[1][1:3] != live[0][1:3],
        '19 0 page errors': not A['errs'] and not B['errs'],
    }

def run(targets, mutate, json_out):
    from playwright.sync_api import sync_playwright
    report = {}; total_fail = 0
    with sync_playwright() as p:
        br = p.chromium.launch(args=['--no-sandbox'])
        for t in targets:
            path, raw = build_harness(t, mutate)
            per_w = {}
            for w in WIDTHS:
                pg = br.new_page(viewport={'width': w, 'height': 900}); errs = []
                pg.on('pageerror', lambda e: errs.append(str(e)))
                pg.goto('file://' + path); pg.wait_for_timeout(900)
                m = pg.evaluate(PROBE, raw)
                for s in m['svgs']: s['errs'] = m['errs'] + errs
                per_w[w] = m['svgs']; pg.close()
            pg = br.new_page(viewport={'width': 1440, 'height': 900}); pg.goto('file://' + path); pg.wait_for_timeout(700)
            live = []
            for w in (1440, 1100, 1440):
                pg.set_viewport_size({'width': w, 'height': 900}); pg.wait_for_timeout(450)
                m = pg.evaluate(PROBE, raw); live.append([(w, s['after']['vbW'], s['after']['vbH'], s['slack']) for s in m['svgs']])
            pg.close()
            tres = {}
            for i, A in enumerate(per_w[1440]):
                B = per_w[1100][i]
                c = checks_for(A, B, [live[j][i] for j in range(3)])
                tres['svg%d %s' % (i, A['label'])] = {'checks': c, 'svg1440': A['svg'], 'vb1440': (A['after']['vbW'], A['after']['vbH']), 'slack1440': A['slack'],
                                                     'svg1100': B['svg'], 'vb1100': (B['after']['vbW'], B['after']['vbH']), 'slack1100': B['slack'], 'tile': A['tile']}
            # aggregate: a check passes for the target iff it passes on every svg
            names = list(next(iter(tres.values()))['checks'].keys())
            agg = {n: all(v['checks'][n] for v in tres.values()) for n in names}
            nfail = sum(1 for v in agg.values() if not v); total_fail += nfail
            print('%s%s — %d svg(s) in a %dpx tile — %d/19 PASS' % (t, ' [MUTATION %s]' % mutate if mutate else '', len(tres), TILE_H, 19 - nfail))
            for n, v in agg.items():
                print('  %s %s' % ('PASS' if v else 'FAIL', n))
            for k, v in tres.items():
                print('  · %s: 1440 svg %s vb %s slack %s | 1100 svg %s vb %s slack %s' % (k, v['svg1440'], v['vb1440'], v['slack1440'], v['svg1100'], v['vb1100'], v['slack1100']))
            report[t] = {'agg': agg, 'svgs': tres, 'live': live, 'harness': path}
        br.close()
    if json_out: json.dump(report, open(json_out, 'w'), indent=1)
    print('fit-physics: %d check(s) failed across %d target(s)%s' % (total_fail, len(targets), ' [MUTATION %s — fails EXPECTED]' % mutate if mutate else ''))
    return 0 if total_fail == 0 else 1

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--mutate', choices=sorted(MUTATIONS)); ap.add_argument('--json'); ap.add_argument('--targets', nargs='*')
    a = ap.parse_args()
    sys.exit(run(a.targets or TARGETS, a.mutate, a.json))
