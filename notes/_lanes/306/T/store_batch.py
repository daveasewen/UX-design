#!/usr/bin/env python3
"""#306 T — Dave's answers on the check page (export notes/_lanes/306/DAVE-RULINGS-2026-09-28-parked-check.md,
15:20 BST) applied to knowledge/_state.json through the store's own API (_state.load -> mutate -> _state.check ->
_state.save), BY ADDITION, mirroring #305 H1's store_batch.py: closes carry `closed_by` and a dated body paragraph,
reopens append a dated body paragraph; no existing text is rewritten; no closes_when is touched.
  python3 notes/_lanes/306/T/store_batch.py --dry-run | --write      (idempotent: rows no longer parked are skipped)"""
import json, re, sys, collections
sys.path.insert(0, 'knowledge')
import _state
WRITE = '--write' in sys.argv
LANE = 'notes/_lanes/306/T'
EX = 'notes/_lanes/306/DAVE-RULINGS-2026-09-28-parked-check.md'
PAGE = 'notes/_CHECK-306-parked-superseded-2026-09-28-v1.html'
SREP = 'notes/_subreports/2026-09-28-306-S-parked-check.md'
SJS = 'notes/_lanes/306/S/parked-102-check.json'
TREP = 'notes/_subreports/2026-09-28-306-T-parked-enact.md'
txt = open(EX, encoding='utf-8').read()
A = json.loads(re.search(r'```json\n(.*?)\n```', txt, re.S).group(1))['answers']
# his two calls, read from the export's markdown (never retyped)
CALLS = dict(re.findall(r'^- (.+?) → \*\*(.+?)\*\*$', txt, re.M))
Q1 = 'Close the 24 already-answered questions?'
Q2 = 'Does the call-33 yes settle the two old release rows (W-222, W-272)?'
assert CALLS.get(Q1) == 'yes' == A['dec']['close24'] and CALLS.get(Q2) == 'yes' == A['dec']['call33'], CALLS
KEEP = A['keep']
C = {r['id']: r for r in json.load(open(SJS, encoding='utf-8'))}
SUP = [i for i, r in C.items() if r['verdict'] == 'SUPERSEDED']
OTHER = [i for i, r in C.items() if r['verdict'] != 'SUPERSEDED']
assert len(C) == 102 and len(SUP) == 24 and len(OTHER) == 78, (len(C), len(SUP), len(OTHER))
assert set(OTHER) == set(KEEP) and not set(SUP) & set(KEEP), 'his Keep-open ticks are not exactly the 78 non-superseded rows'
doc = _state.load(); by = {i['id']: i for i in doc['items']}
before = _state.counts(doc)
arm_before = _state.regrowth_arming(doc['items'])
HEAD = '#306 T (2026-09-28)'
D1 = f'`s306-D1` (Dave, check page export 15:20 BST, verbatim: \'{Q1}\' → "{CALLS[Q1]}")'
D2 = f'`s306-D2` (Dave, check page export 15:20 BST, verbatim: \'{Q2}\' → "{CALLS[Q2]}")'
D3 = '`s306-D3` (Dave ticked "Keep open" on the check page; export 15:20 BST, section "Keep open (78 of 102)")'
SRC = f'the check page `{PAGE}`, his export `{EX}`, lane S\'s check `{SREP}` (rows `{SJS}`)'
ops = []
def para(it, p):
    it['body'] = ((it.get('body') or '').rstrip() + '\n\n' + p).lstrip()
for i in SUP:
    it, r = by[i], C[i]
    if it['state'] != 'parked':
        ops.append((i, 'SKIP-not-parked', it['state'])); continue
    extra = ''
    if i in ('W-222', 'W-272'):
        extra = (f' ALSO under {D2}: his call-33 yes (`s305-D33`) now closes this row too; it had been kept parked '
                 f'only so it stayed on his scan page (see the #305 paragraph above).')
    rec = (f'Answered by: {", ".join("`" + b + "`" for b in r["by"])}. The record, as lane S quoted it: {r["quote"]} '
           f'Lane S\'s reading: "{r["note"]}"')
    p = (f'✅ CLOSED AS ANSWERED {HEAD} under {D1}.{extra} {rec} Source: {SRC}. The #305 park paragraph above and '
         f'`closes_when` are unchanged; every file this row points at stays.')
    it['state'] = 'done'
    it['closed_by'] = (f'{HEAD} — CLOSED BY ADDITION under {D1}{" and " + D2 if extra else ""}. Answered by '
                       f'{", ".join(r["by"])}; receipt in the body\'s #306 paragraph and in {SREP}. '
                       f'The row\'s own close condition is closed as answered on his word, not re-measured here.')
    para(it, p); ops.append((i, 'done', r['by']))
for i in OTHER:
    it, r = by[i], C[i]
    if it['state'] != 'parked':
        ops.append((i, 'SKIP-not-parked', it['state'])); continue
    left = f' What lane S found still open: "{r["left"]}"' if r.get('left') else ''
    d37 = ''
    if 's305-D37' in (it.get('body') or ''):
        d37 = (' ⚠ This row was ALSO parked under `s305-D37` (tripwire: reopen when the catalogue lists the '
               'component); his Keep-open tick is the later word and reopens it. `s305-D37` is not edited.')
    p = (f'▶ REOPENED {HEAD} under {D3}: Dave ticked "Keep open" on this row (tick saved {KEEP[i]} BST); he '
         f'reopened it at 15:20 BST on 2026-09-28 from the check page. Lane S\'s verdict: {r["verdict"]}'
         f'{" (by " + ", ".join(r["by"]) + ")" if r["by"] else ""}.{left}{d37} Source: {SRC}. State parked → open. '
         f'The #305 park paragraph and its tripwire above are history, not deleted; `closes_when` is unchanged.')
    it['state'] = 'open'; para(it, p); ops.append((i, 'open', r['verdict']))
# ---- W-305hr: first half of its close answered; the kind-6 half is not, so it stays open
hr = by['W-305hr']
if '#306' not in (hr.get('body') or ''):
    para(hr, f'✎ {HEAD} — BY ADDITION: Dave has now said which way W-222 and W-272 go — {D2}, and both are closed '
             f'as answered under `s306-D1`. The other half of `closes_when` — the 28 kind-6 rulings re-sorted or left '
             f'— has NO answer from him yet, so this row stays open. Source: {SRC}.')
    ops.append(('W-305hr', 'body+', 'W-222/W-272 answered; stays open'))
# ---- W-305n5 and W-305b4 — each closes_when checked honestly (receipts in T's report)
n5 = by['W-305n5']
if n5['state'] == 'open':
    n5['state'] = 'done'
    n5['closed_by'] = (f'{HEAD} — CLOSED BY ADDITION. closes_when, limb by limb: (1) "a scan page listing all 102 '
                       f'questions parked under s305-D32, each with its tripwire, is filed and put to Dave" — '
                       f'notes/_SCAN-305-parked-questions-2026-09-27-v1.html (lane B4, committed 27efb7b6, in the '
                       f'artifact "Apollo 304 review" v7 per _HANDOFF-156), then the #306 check page {PAGE} over the same '
                       f'102, answered by him; (2) "every one he names in one line is reopened" — he named 78 by '
                       f'"Keep open" ticks, and all 78 are reopened under `s306-D3`; the other 24 are closed as answered '
                       f'under `s306-D1`. His export: {EX} (15:20 BST). Report: {TREP}.')
    ops.append(('W-305n5', 'done', 'met'))
b4 = by['W-305b4']
if b4['state'] == 'open':
    b4['state'] = 'done'
    b4['closed_by'] = (f'{HEAD} — CLOSED BY ADDITION. closes_when, limb by limb: (1) "both pages are committed" — '
                       f'notes/_SCAN-305-parked-questions-2026-09-27-v1.html at 27efb7b6 and '
                       f'notes/_REVIEW-305-call-27-visuals-2026-09-27-v1.html at f6aeb264 (git log, #306 T); (2) '
                       f'"and published to the review artifact" — _HANDOFF-156 WHAT LANDED: the artifact "Apollo 304 '
                       f'review" is at version 7 "with the call-27 visuals, the 102 scan and the loose-ends page added"; '
                       f'(3) "and Dave has scanned the 102" — his check-page export of 2026-09-28 15:20 BST ({EX}) '
                       f'answers all 102: 78 "Keep open" ticks (14:26 to 15:20 BST) and "yes" to closing the other 24. '
                       f'⚠ DECLARED: he answered on the #306 check page over the same 102 ids, not by ticks on B4\'s '
                       f'scan page itself. Report: {TREP}.')
    ops.append(('W-305b4', 'done', 'met, declared'))
# ---- the #306 document rows, BORN CLOSED under s305-D40 (DOC_BIRTH_FROM_SESSION = 306)
NEW = [
 dict(id='W-306s', title="#306 S - the 102 parked questions checked for supersession: 24 superseded, 34 partly, 10 unsure, 34 live",
      project='apollo', state='done', opened=306, owner='claude', condition='stated', home=SREP,
      links=[SJS, 'notes/_lanes/306/S/parked-102-pack.json', PAGE, EX, 'W-305n5'],
      closes_when='the report is committed and its check is put to Dave',
      closed_by=f'born closed (s305-D40): {SREP} filed at #306 — the file is the record. Its check was put to him on {PAGE} and he answered it at 15:20 BST ({EX}); enacted by lane T ({TREP}).',
      body=("s218-D7 filed report. Asked by Dave, Mon 12:59 BST, verbatim: \"can you check these I think some of them have been superseded\". "
            "Four readers checked the 102 rows parked under s305-D32 against knowledge/_rulings.json (702). The check page "
            f"`{PAGE}` carries it; its answers are `s306-D1`..`s306-D3`.")),
 dict(id='W-306t', title="#306 T - his check-page answers enacted: 24 closed as answered, 78 reopened, s306-D1..D3 inscribed",
      project='apollo', state='done', opened=306, owner='claude', condition='stated', home=TREP,
      links=['knowledge/_state.json', 'knowledge/_rulings.json', '_CARRIES.md', 'notes/_lanes/306/T/', 'W-306s'],
      closes_when='the report is committed',
      closed_by=f'born closed (s305-D40): {TREP} filed at #306 — the file is the record.',
      body="s218-D7 filed report. The store, rulings and carry writes for Dave's three answers on the #306 check page, each by addition with its receipt."),
]
for n in NEW:
    if n['id'] in by: ops.append((n['id'], 'SKIP-exists', '')); continue
    doc['items'].append(n); by[n['id']] = n; ops.append((n['id'], 'added', n['title'][:80]))
ok, fails, notes = _state.check(doc)
after = _state.counts(doc)
arm_after = _state.regrowth_arming(doc['items'])
kinds = collections.Counter(k for _, k, _ in ops)
print(('WRITE' if WRITE else 'DRY-RUN'), dict(kinds), 'check ok', ok, 'fails', len(fails))
for f in fails[:10]: print('  FAIL', f[:300])
for n in notes:
    if 'Regrowth' in n or 'REGROWTH' in n or 'DOC BIRTH' in n: print('  NOTE', n[:260])
print(' before live', before['live'], before['by_state'], before['by_owner'])
print(' after  live', after['live'], after['by_state'], after['by_owner'])
print(' pinned-75 still live: before', len(arm_before[1]), 'after', len(arm_after[1]), 'armed', arm_after[0])
json.dump({'ops': ops, 'before': before, 'after': after, 'check_ok': ok, 'fails': fails,
           'pinned_live_before': arm_before[1], 'pinned_live_after': arm_after[1]},
          open(f'{LANE}/store_batch.{"write" if WRITE else "dry"}.json', 'w'), indent=1, ensure_ascii=False)
if WRITE and ok:
    _state.save(doc); print(' saved')
