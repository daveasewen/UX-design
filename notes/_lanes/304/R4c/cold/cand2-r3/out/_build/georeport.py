import json, sys
vw, theme = sys.argv[1], sys.argv[2]
for l in sys.stdin:
    d = json.loads(l); r = d['res']
    rag, part, dead, gaps = [], [], [], set()
    for g in r['groups']:
        gaps.add(g['gap'])
        rows = {}
        for t in g['tiles']: rows.setdefault(t['rect'][1], []).append(t)
        tops = sorted(rows)
        for top in tops:
            ts = rows[top]
            if len({t['rect'][1] + t['rect'][3] for t in ts}) > 1: rag.append((g['cls'][10:], top))
            ts2 = sorted(ts, key=lambda t: t['rect'][0])
            for a, b in zip(ts2, ts2[1:]): gaps.add('h%d' % (b['rect'][0] - a['rect'][0] - a['rect'][2]))
            if sum(t['rect'][2] for t in ts) + 4 * (len(ts) - 1) < r['wall'][0][2] - 2: part.append((g['cls'][10:], [t['k'] for t in ts]))
        for a, b in zip(tops, tops[1:]):
            h = rows[a][0]; gaps.add('v%d' % (b - a - h['rect'][3]))
        dead += [(t['k'], t['dead'] - 24) for t in g['tiles'] if t['dead'] - 24 > 8]
    gs = r['groups']; wallv = sorted(set(gs[i + 1]['rect'][1] - gs[i]['rect'][1] - gs[i]['rect'][3] for i in range(len(gs) - 1)))
    print('%s %s %-9s errs=%d pageScroll=%s ground=%s groundPad=%s wallGap(v)=%s tileGaps=%s ragged=%s partialRows=%s deadBeyondPadding=%s tileOverflow=%s'
          % (vw, theme, d['page'], len(d['errors']), r['viewport'][2] == int(vw), r['ground'][1], r['ground'][2], wallv, sorted(gaps), rag or 'none', part or 'none', dead or 'none',
             [t['k'] for g in gs for t in g['tiles'] if t['over']] or 'none'))
