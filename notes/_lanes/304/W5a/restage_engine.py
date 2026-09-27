"""restage_engine.py <stage-dir> <tree> — W5a: put <tree>'s dv-behaviour.js into a staged cold run IN PLACE:
the pack copy, and every inlined `/* INJECTED from knowledge/canon/dv-behaviour.js` <script> body. Stage copies only."""
import os, re, sys, glob, shutil
d, T = sys.argv[1], sys.argv[2]
src = open(os.path.join(T, 'knowledge/canon/dv-behaviour.js'), encoding='utf-8').read()
shutil.copy(os.path.join(T, 'knowledge/canon/dv-behaviour.js'), os.path.join(d, 'pack/knowledge/canon/dv-behaviour.js'))
pat = re.compile(r'(<script>\n)(/\* INJECTED from knowledge/canon/dv-behaviour\.js .*?)(\n</script>)', re.S)
n = 0
for f in glob.glob(os.path.join(d, 'out/*.html')):
    s = open(f, encoding='utf-8').read()
    def rep(m):
        global n; n += 1
        hdr = m.group(2).split('*/', 1)[0] + '*/'
        return m.group(1) + hdr + '\n' + src + m.group(3)
    open(f, 'w', encoding='utf-8').write(pat.sub(rep, s))
print(d, 'inlined dv-behaviour blocks replaced:', n)
