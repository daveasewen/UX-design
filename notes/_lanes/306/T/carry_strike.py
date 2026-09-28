#!/usr/bin/env python3
"""#306 T — strike item ① of `_CARRIES.md` § residual → #306 in the s183-D1 strike form (s188-D2 receipt), BY ADDITION:
`~~` goes round the item's bold title and a ⛔ STRUCK note follows it; the original item follows unedited. PROVEN: removing
the three inserted spans gives back the original bytes.   python3 carry_strike.py --dry-run | --write"""
import sys
WRITE = '--write' in sys.argv
P = '_CARRIES.md'
orig = open(P, encoding='utf-8').read()
sec = orig.index('## residual → #306'); end = orig.index('## residual → #305')
TITLE = '**① THE 102 PARKED QUESTIONS, HIS KEEP-OPEN TICKS**'
a = orig.index(TITLE, sec); assert a < end and orig.count(TITLE, sec, end) == 1
assert orig[a - 2:a] == '⬛ ', repr(orig[a - 4:a])
NOTE = (' ⛔ **STRUCK #306 2026-09-28 BY LANE T (`s183-D1` strike form, `s188-D2` receipt) — HIS TICKS CAME BACK AND ARE ENACTED.** '
        'He answered on the #306 check page `notes/_CHECK-306-parked-superseded-2026-09-28-v1.html` (lane S read the 102 '
        'against the rulings, `notes/_subreports/2026-09-28-306-S-parked-check.md`); his export is '
        '`notes/_lanes/306/DAVE-RULINGS-2026-09-28-parked-check.md`, 15:20 BST. His two calls, verbatim: '
        '"Close the 24 already-answered questions?" → "yes" and "Does the call-33 yes settle the two old release rows '
        '(W-222, W-272)?" → "yes"; and "Keep open" ticked on the other 78. Enacted in `knowledge/_state.json` by addition: '
        '24 closed as answered (`s306-D1`, W-222 and W-272 also `s306-D2`), 78 reopened (`s306-D3`), rows `W-305n5` and '
        '`W-305b4` closed with their receipts, `W-305hr` stays open on its kind-6 half. Receipts: '
        '`notes/_subreports/2026-09-28-306-T-parked-enact.md`. The original item follows unedited.')
new = orig[:a] + '~~' + TITLE + '~~' + NOTE + orig[a + len(TITLE):]
# reconstruction proof
back = new[:a] + new[a + 2:a + 2 + len(TITLE)] + new[a + 2 + len(TITLE) + 2 + len(NOTE):]
assert back == orig, 'reconstruction failed'
assert ' · ' not in NOTE
print(('WRITE' if WRITE else 'DRY-RUN'), 'inserted', len(new) - len(orig), 'chars at', a, '; reconstruction proof PASSED')
if WRITE:
    open(P, 'w', encoding='utf-8').write(new); print('written')
