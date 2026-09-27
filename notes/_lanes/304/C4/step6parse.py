# #304 C4: name every red/advisory/could-not-ask in the gates job's step 6 by [N].
import re, sys
L = open(sys.argv[1], encoding='utf-8', errors='replace').read().split('\n')
cur = None; red = []; adv = []; cna = []
for ln in L:
    s = ln[29:] if len(ln) > 29 and ln[:4] == '2026' else ln
    m = re.match(r'=== \[(\d+)/148\]', s.strip())
    if m: cur = int(m.group(1)); continue
    if cur is None: continue
    t = s.strip()
    if re.match(r'❌ .*failed \(exit', t) and cur not in red: red.append(cur)
    if t.startswith('⚠ advisory step') and cur not in adv: adv.append(cur)
    if t.startswith('⊘ step') and 'COULD-NOT-ASK' in t and cur not in cna: cna.append(cur)
    if t.startswith('❌ build gate failed'): break
print('gate red', red); print('advisory', adv); print('could-not-ask', cna)
