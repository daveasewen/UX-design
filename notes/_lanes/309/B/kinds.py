"""#309 lane B — splice `"kind"` into every non-alias component meta (s308-D39/D40/D44), right after
its top-level "category" line, by text (the file's own formatting kept). Idempotent: a meta already
carrying a top-level kind is left alone. The map is the lane's assignment against the ruled
definitions; the judgement calls are recorded in knowledge/_edge_register.json $containers."""
import json, glob, os, re, sys
K = 'knowledge/components'
LAYOUT = {'layout-utilities', 'form-layout', 'splitter', 'stats-band-lockup', 'feature-grid-lockup',
          'footer', 'footer-doormat-lockup', 'hero', 'hero-variants'}
HOUSING = {'carousel', 'drawer', 'modals', 'modal-lightbox', 'popover', 'accordion', 'tabs'}
RECORD = {'cards', 'account-card', 'transaction-row', 'document-row', 'standing-order-mandate-row'}
PART = {'card-header-lockup'}
def kind(stem):
    if stem.startswith('template-') or stem.startswith('app-shell-') or stem in LAYOUT: return 'layout'
    if stem in HOUSING: return 'housing'
    if stem in RECORD: return 'record'
    if stem in PART: return 'part'
    return 'block'
if __name__ == '__main__':
    out = {}
    for f in sorted(glob.glob(os.path.join(K, '*.meta.json'))):
        stem = os.path.basename(f)[:-len('.meta.json')]
        m = json.load(open(f, encoding='utf-8'))
        if 'aliasOf' in m: out[stem] = 'alias of ' + m['aliasOf']['component']; continue
        k = kind(stem); out[stem] = k
        if 'kind' in m: continue
        if '--write' in sys.argv:
            s = open(f, encoding='utf-8').read()
            s2, n = re.subn(r'(?m)^(  "category": [^\n]*,\n)', lambda mo: mo.group(1) + f'  "kind": "{k}",\n', s, count=1)
            assert n == 1, f
            json.loads(s2)
            open(f, 'w', encoding='utf-8').write(s2)
    from collections import Counter
    print(Counter(v if not v.startswith('alias') else 'alias' for v in out.values()))
    for k in ('layout', 'housing', 'record', 'part'):
        print(k, sorted(s for s, v in out.items() if v == k))
