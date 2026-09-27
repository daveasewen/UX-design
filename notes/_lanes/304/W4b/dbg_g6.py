"""W4b: reproduce W3b's G6 miss — dump the gate's own model for big tiles."""
import sys, os, json
sys.path.insert(0, 'knowledge')
import _validate_geometry as G
page = sys.argv[1]
with G.Harness() as h:
    m = h.model(page, 1440)
print('docH', m['docH'], 'tiles', len(m['tiles']))
for t in m['tiles']:
    r = t['rect']
    if r['h'] > 400:
        print(t['id'], t['sel'], t['name'][:30], 'h=%d w=%d' % (r['h'], r['w']), 'group', t['group'], 'ink', [[round(a), round(b)] for a, b in (t.get('ink') or [])][:30], 'pads', t['pads'])
