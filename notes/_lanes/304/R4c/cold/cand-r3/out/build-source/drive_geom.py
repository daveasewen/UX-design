G = open(W + '/tools/geom.js').read()
R['geometry'] = {}
for v in ['overview', 'accounts', 'liquidity', 'payments', 'fx', 'risk', 'trade', 'reports', 'messages', 'settings']:
    pg.goto(URL + '#/' + v); pg.wait_for_timeout(1100)
    g = ev(pg, G); R['geometry'][v] = g
    check('%s: no ragged rows, no tile overflow' % v, not g['issues'], g['issues'][:4])
    check('%s: no horizontal page scroll' % v, not g['pageHScroll'] and not g['contentHScroll'])
    check('%s: filter toolbar is exactly as wide as the bento section it controls' % v, abs(g['ftbWidth'] - g['groundWidth']) < 1, [g['ftbWidth'], g['groundWidth']])
    print('   ', v, 'groundPad', g['groundPad'], 'wallGap', g['wallGap'], '|', '; '.join(sorted(set(g['notes'])))[:600])
# showroom comparison: the KPI tile at its own size
pg.goto('file://' + W + '/pack/showroom/kpi-tile.html'); pg.wait_for_timeout(1200)
show = ev(pg, "() => { const all = [...document.querySelectorAll('.kpi-tile'), ...[...document.querySelectorAll('iframe')].flatMap(f => { try { return [...f.contentDocument.querySelectorAll('.kpi-tile')]; } catch (e) { return []; } })]; const k = all.find(e => !e.classList.contains('compact') && !e.classList.contains('hero') && e.classList.contains('as-link')) || all.find(e => !e.classList.contains('compact') && !e.classList.contains('hero')); if (!k) return ['none', document.querySelectorAll('iframe').length]; const cs = getComputedStyle(k); return [k.getBoundingClientRect().height, cs.paddingTop, cs.rowGap || cs.gap, getComputedStyle(k.querySelector('.kpi-val')).fontSize]; }")
pg.goto(URL + '#/overview'); pg.wait_for_timeout(1100)
mine = ev(pg, "() => { const k = document.querySelector('.kpi-tile'); const cs = getComputedStyle(k); return [k.getBoundingClientRect().height, cs.paddingTop, cs.rowGap || cs.gap, getComputedStyle(k.querySelector('.kpi-val')).fontSize]; }")
R['kpiCompare'] = {'showroom': show, 'page': mine}
check('KPI tile keeps its showroom padding, gap and value size', show and mine[1:] == show[1:], [show, mine])
print('    KPI showroom', show, 'page', mine)
