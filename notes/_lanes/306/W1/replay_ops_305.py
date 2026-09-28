# #306 W1 - replay #305's main move file with _wrap_ops.build on the tree BEFORE the #305 wrap commit
# (cd16f7ec = 81bce363^), inputs read out of #305's own _ops-305W-main.json (never retyped). Both op lists
# are applied by the REAL mover to two projections; the five files are compared byte for byte. Then the
# two placeholders are filled on a projection and compared with #305's -gen.json and -sizes.json values.
# Read-only on the repo: git show into /dev/shm; nothing under the working tree is written but this lane's logs.
import json, os, subprocess, sys, tempfile, shutil
sys.path.insert(0, 'knowledge')
import _wrap_ops as wo
W = 'notes/_lanes/305/W/'
OLD = json.load(open(W + '_ops-305W-main.json', encoding='utf-8'))
BASE = '81bce363^'
def tree():
    td = tempfile.mkdtemp(prefix='w1replay-', dir='/dev/shm')
    for f in wo.FILES:
        os.makedirs(os.path.dirname(os.path.join(td, f)) or td, exist_ok=True)
        open(os.path.join(td, f), 'wb').write(subprocess.run(['git', '--no-optional-locks', 'show', f'{BASE}:{f}'], capture_output=True, check=True).stdout)
    return td
ins = [o for o in OLD if o['op'] == 'insert']
def pick(file, at_prefix):
    return next(o for o in ins if o['file'] == file and o['at'].startswith(at_prefix))
title = [o for o in OLD if o['op'] == 'replace' and o['find'][0].startswith('> **TITLE')][0]['replace'][0].split('`')[1]
split = pick('GOOD-MORNING.md', '> ⚠ **WRAP DATE SPLIT')['lines']
banner = pick('GOOD-MORNING.md', '> ## ★ LATEST')['lines']
batch = pick('_GM-ARCHIVE.md', '## Batch')['lines']
stratum = pick('GOOD-MORNING.md', '#### ')['lines']
stamp = pick('_LIVE-STATE.md', '*Last refreshed')['lines']
delta = pick('_LIVE-STATE.md', '## ⏱ LATEST DELTA')['lines']
rolled = pick('_LIVE-STATE-ARCHIVE.md', '## Rolled')['lines']
t1, t2 = tree(), tree()
try:
    new = wo.build(t1, 305, '2026-09-28', '2026-09-27', banner, stratum, delta, stamp, title=title, date_split=split,
                   batch_note=batch[2:-1], rolled_note=rolled[2:-1])
    print('ops: #305 hand-built', len(OLD), '· _wrap_ops.build', len(new))
    print('op kinds equal, in order:', [o['op'] for o in OLD] == [o['op'] for o in new])
    for td, ops, name in ((t1, new, 'new'), (t2, OLD, 'old')):
        p = os.path.join(td, '_ops.json'); json.dump(ops, open(p, 'w', encoding='utf-8'), ensure_ascii=False)
        rc, out = wo._mover(td, p, False)
        print(f'mover on the {name} ops: rc {rc} ·', (out.strip().splitlines() or ['?'])[-1][:160])
    same = {f: open(os.path.join(t1, f), 'rb').read() == open(os.path.join(t2, f), 'rb').read() for f in wo.FILES}
    print('five files byte-identical after both moves:', same)
    # placeholders: the #305 PENDING sizes line -> {{SECTION_SIZES}}; the gen line after the residual line -> {{ROLL_STATE}}
    st2 = ['{{SECTION_SIZES}}' if l.startswith('> **section-sizes #305 (real):**') else l for l in stratum]
    b2 = []
    for l in banner:
        b2.append(l)
        if l.startswith('> **residual → #306:**'): b2.append('{{ROLL_STATE}}')
    t3 = tree()
    try:
        ops3 = wo.build(t3, 305, '2026-09-28', '2026-09-27', b2, st2, delta, stamp, title=title, date_split=split,
                        batch_note=batch[2:-1], rolled_note=rolled[2:-1])
        filled, rec = wo.project_and_fill(t3, ops3, 305, '2026-09-28')
    finally:
        shutil.rmtree(t3, ignore_errors=True)
    fj = json.dumps(filled, ensure_ascii=False)
    gen = json.load(open(W + '_ops-305W-gen.json', encoding='utf-8'))[0]['lines'][0]
    sizes = json.load(open(W + '_ops-305W-sizes.json', encoding='utf-8'))[0]['replace'][0]
    got_roll = next(l for o in filled if o['op'] == 'insert' for l in o.get('lines', []) if l.startswith('> **residual (GENERATED'))
    got_sizes = next(l for o in filled if o['op'] == 'insert' for l in o.get('lines', []) if l.startswith('> **section-sizes'))
    print('ROLL_STATE line == #305 -gen.json:', got_roll == gen); print('   ', got_roll[:160])
    print('SECTION_SIZES line == #305 -sizes.json:', got_sizes == sizes)
    print('   mine :', got_sizes); print('   #305 :', sizes)
    a = dict(x.split(':') for x in got_sizes.split(':** ')[1].replace(' · ', ' ').split() if ':' in x and x.split(':')[1].isdigit())
    b = dict(x.split(':') for x in sizes.split(':** ')[1].replace(' · ', ' ').split() if ':' in x and x.split(':')[1].isdigit())
    print('   sections that differ:', {k: (b.get(k), a.get(k)) for k in a if a.get(k) != b.get(k)})
finally:
    shutil.rmtree(t1, ignore_errors=True); shutil.rmtree(t2, ignore_errors=True)
