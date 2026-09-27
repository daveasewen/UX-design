"""R4s2 copy of W4a/restage.py: the six EARLIER cold runs restaged against candidate-2's engine + canon (pack tree).
Only DST and the run filter changed."""
"""restage.py <variant> <tree> — stage the six cold runs against <tree>'s engine + canon.css/type.css.
Inlined engine blocks (<script>/* INJECTED from knowledge/canon/X.js ...*/ ... </script>) are replaced
by <tree>'s X.js; src-loaded ones resolve to a canon dir whose dv-*.js / canon.css / type.css are <tree>'s."""
import os, re, sys, shutil, glob
V, T = sys.argv[1], sys.argv[2]
SRC = os.path.expanduser('~/r4c/stage'); DST = os.path.expanduser('~/r4s2/st/' + V)
if os.path.exists(DST): shutil.rmtree(DST)
canon = os.path.join(T, 'knowledge/canon')
pat = re.compile(r'<script>\n/\* INJECTED from knowledge/canon/([\w-]+)\.js .*?\n</script>', re.S)
for run in sorted([g for g in glob.glob(SRC + '/cold-*') if '-cand2-' not in g]):
    r = os.path.basename(run); d = os.path.join(DST, r); os.makedirs(d)
    shutil.copytree(run + '/out', d + '/out')
    pk = run + '/pack'; os.makedirs(d + '/pack/knowledge/canon')
    for e in os.listdir(pk):
        if e != 'knowledge': os.symlink(os.path.join(pk, e), d + '/pack/' + e)
    for e in os.listdir(pk + '/knowledge'):
        if e != 'canon': os.symlink(os.path.join(pk, 'knowledge', e), d + '/pack/knowledge/' + e)
    for e in os.listdir(pk + '/knowledge/canon'):
        src = os.path.join(canon, e) if (e.endswith('.js') and e.startswith('dv-')) or e in ('canon.css', 'type.css') else os.path.join(pk, 'knowledge/canon', e)
        if not os.path.exists(src): src = os.path.join(pk, 'knowledge/canon', e)
        shutil.copy(src, d + '/pack/knowledge/canon/' + e)
    n = 0
    for f in glob.glob(d + '/out/*.html'):
        s = open(f).read()
        def rep(m):
            global n; n += 1
            body = open(os.path.join(canon, m.group(1) + '.js')).read()
            return '<script>\n/* INJECTED from knowledge/canon/%s.js (restaged by R4s2 from %s) */\n%s\n</script>' % (m.group(1), V, body)
        s2 = pat.sub(rep, s)
        open(f, 'w').write(s2)
    print(r, 'inlined blocks replaced:', n)
