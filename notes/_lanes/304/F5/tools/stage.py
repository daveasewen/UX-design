"""stage.py <side> <tree> — F5: stage candidate 2's three cold runs against <tree>'s canon.css/type.css + dv-*.js
(pack copies AND inlined engine blocks), as R4s2's restage_c2.py / W5a's restage_engine.py did. Stage copies only."""
import os, re, sys, shutil, glob
V, T = sys.argv[1], sys.argv[2]
SRC = os.path.expanduser('~/r4c/stage'); DST = os.path.expanduser('~/f5st/' + V)
if os.path.exists(DST): shutil.rmtree(DST)
canon = os.path.join(T, 'knowledge/canon')
pat = re.compile(r'<script>\n/\* INJECTED from knowledge/canon/([\w-]+)\.js .*?\n</script>', re.S)
for r in (1, 2, 3):
    run = SRC + '/cold-cand2-r%d' % r; d = os.path.join(DST, 'c2r%d' % r); os.makedirs(d)
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
            return '<script>\n/* INJECTED from knowledge/canon/%s.js (restaged by F5 from %s) */\n%s\n</script>' % (m.group(1), V, body)
        open(f, 'w').write(pat.sub(rep, s))
    print(V, 'c2r%d' % r, 'inlined blocks replaced:', n)
