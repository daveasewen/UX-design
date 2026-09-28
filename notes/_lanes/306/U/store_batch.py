#!/usr/bin/env python3
"""#306 U — store writes for Dave's wrap-redesign answers (export 16:01 BST), through _state.load -> mutate ->
_state.check -> _state.save, BY ADDITION (#306 T's method): W-305wr gains a dated body paragraph (it stays open);
W-306r (lane R's report) and W-306u (lane U's report) are born closed under s305-D40.
  python3 notes/_lanes/306/U/store_batch.py --dry-run | --write"""
import json, sys
sys.path.insert(0, 'knowledge')
import _state
WRITE = '--write' in sys.argv
EX = 'notes/_lanes/306/DAVE-RULINGS-2026-09-28-wrap-redesign.md'
PAGE = 'notes/_DECIDE-306-wrap-redesign-2026-09-28-v1.html'
RREP = 'notes/_subreports/2026-09-28-306-R-wrap-redesign.md'
UREP = 'notes/_subreports/2026-09-28-306-U-rulings-and-bloat.md'
HEAD = '#306 U (2026-09-28)'
doc = _state.load(); by = {i['id']: i for i in doc['items']}
before = _state.counts(doc); ops = []
wr = by['W-305wr']
if '#306 U' not in (wr.get('body') or ''):
    wr['body'] = (wr.get('body') or '').rstrip() + '\n\n' + (
        f'✎ {HEAD} — BY ADDITION: the design was RULED at 16:01 BST on Mon 2026-09-28. Dave answered all six calls '
        f'on the decision page `{PAGE}` on the recommendations (export `{EX}`), inscribed as `s306-D4`..`s306-D9`, '
        f'status `ruled`. The build is the page\'s six phases, each proven on one real wrap: 1 the mechanics become '
        f'permanent tools; 2 his summary at the push, no second CI wait (`s306-D7`); 3 one story, every view generated '
        f'(`s306-D4`, `s306-D5`); 4 three seats (`s306-D6`); 5 carried items written as changes (`s306-D8`); 6 wrap as '
        f'you go (`s306-D9`). His bloat question is answered on measurement in `{UREP}` (guards proposed, not ruled). '
        f'This row stays OPEN: `closes_when` is unchanged, and it closes only when a wrap has run on the redesign. '
        f'Design: `{RREP}`.')
    ops.append(('W-305wr', 'body+'))
NEW = [
 dict(id='W-306r', title="#306 R - the wrap redesign measured (#303-#305) and put to Dave on one decision page: six calls",
      project='apollo', state='done', opened=306, owner='claude', condition='stated', home=RREP,
      links=[PAGE, EX, 'notes/_lanes/306/R/', 'notes/_lanes/293/IDEA-wrap-is-slow-five-levers.md', 'W-305wr'],
      closes_when='the report is committed and its decision page is put to Dave',
      closed_by=f'born closed (s305-D40): {RREP} filed at #306 — the file is the record. Its page {PAGE} was put to him and he answered all six calls at 16:01 BST ({EX}); inscribed as s306-D4..D9 by lane U ({UREP}).',
      body="s218-D7 filed report. The last three wraps measured from their own logs and git (half of every wrap is waiting on CI twice; each key fact hand-written in about seven places) and the redesign designed: one story plus measured figures, every view generated, three seats, six phases each proven on a real wrap."),
 dict(id='W-306u', title="#306 U - his six wrap-redesign answers inscribed s306-D4..D9, and his bloat question measured per phase",
      project='apollo', state='done', opened=306, owner='claude', condition='stated', home=UREP,
      links=['knowledge/_rulings.json', 'knowledge/_state.json', EX, PAGE, 'notes/_lanes/306/U/', 'W-305wr', 'W-306r'],
      closes_when='the report is committed',
      closed_by=f'born closed (s305-D40): {UREP} filed at #306 — the file is the record.',
      body=("s218-D7 filed report. Six rulings inscribed as `ruled` (705 -> 711). The bloat check measured today's boot "
            "terms (handoff 8,106 cl100k, ungated; chain 7,906 cl100k) and found the old boot bloat was the append-only "
            "delta and stratum stacks read whole until the #33 chain cut; eleven guards proposed, not ruled.")),
]
for n in NEW:
    if n['id'] in by: ops.append((n['id'], 'SKIP-exists')); continue
    doc['items'].append(n); by[n['id']] = n; ops.append((n['id'], 'added'))
ok, fails, notes = _state.check(doc)
after = _state.counts(doc)
print(('WRITE' if WRITE else 'DRY-RUN'), ops, 'check ok', ok, 'fails', len(fails))
for f in fails[:10]: print('  FAIL', f[:300])
for n in notes:
    if 'DOC BIRTH' in n or 'REGROWTH' in n.upper(): print('  NOTE', n[:240])
print(' before', before['live'], before['by_state']); print(' after ', after['live'], after['by_state'])
json.dump({'ops': ops, 'before': before, 'after': after, 'check_ok': ok, 'fails': fails},
          open(f'notes/_lanes/306/U/store_batch.{"write" if WRITE else "dry"}.json', 'w'), indent=1, ensure_ascii=False)
if WRITE and ok:
    _state.save(doc); print(' saved')
