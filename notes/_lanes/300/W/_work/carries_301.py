# #300 wrap seat - write _CARRIES.md section "residual -> #301": new #300 items first, then the
# #300 set with EVERY age bracket +1 (the rule the #297-#299 wraps used, re-verified below),
# ONE partial strike (a headline of one item) appended BY ADDITION with receipts (s183-D1 / s188-D2).
import re, sys
sys.path.insert(0, 'knowledge'); sys.path.insert(0, 'notes/_lanes/300/W/_work')
import _capture_gate as cg
from names_300 import *
AGE = cg._AGE_RE
P = '_CARRIES.md'
txt = open(P, encoding='utf-8').read()
L = txt.split('\n')
assert L[45] == '## residual → #300' and L[47].startswith('> **residual → #300:**'), (L[45], L[47][:40])
assert L[49] == '## residual → #299' and L[51].startswith('> **residual → #299:**')
assert '## residual → #301' not in txt
def bump_all(s):
    s = re.sub(r"\[NEW — 0(,[^\]]*)?\]", lambda m: '[\x00' + (m.group(1) or '') + ']', s)
    s = AGE.sub(lambda m: '[' + str(int(m.group(1)) + 1) + m.group(0)[1 + len(m.group(1)):], s)
    return s.replace('[\x00', '[1')
body = re.sub(r"^> \*\*residual → #300:\*\*", "", L[47]).strip()
b299 = re.sub(r"^> \*\*residual → #299:\*\*", "", L[51]).strip()
old300 = body.split(' ·  ', 1)[1] if ' ·  ' in body else None
assert old300 is not None
bb = bump_all(b299).split('·'); oo = old300.split('·')
diff = [i for i in range(min(len(bb), len(oo))) if bb[i].strip() != oo[i].strip()]
print('verify +1: segs', len(bb), len(oo), 'differing', len(diff), '(expect 2 = #299 strikes)', diff[:5])
old = bump_all(body)
B = '`' + BRIEF + '`'
KEY = "⬛ **⑤ AFTER FRIDAY — HIS \"careful plan\" FOR THE OPENER, THE CHAIN MADE MORE EFFICIENT, AND HIS 256K QUESTION** [1, DAVE'S]"
WHY = ("STRUCK IN PART AT THE #300 WRAP, BY ADDITION, WORDING ABOVE UNCHANGED — THE FIRST HEADLINE ONLY, HIS \"careful plan\" FOR WHERE THE MEMORY HOOK IS PLACED AND WHAT IT COSTS AT THE OPENER. "
       "RECEIPT: on his 15:58 BST words of 2026-09-23 (*\"… come up with a careful plan for this … hatch a plan, then lets do some quick wins before Friday\"*, verbatim in " + B + ") "
       "the opener was measured at 81,049 real (lane C, `" + REPC + "`), graded by lane X (`" + REPX + "`) and planned on lane P's page (`" + PLAN + "`); "
       "before \"wrap\" he pasted the page's instructions himself, and they place the note only after he says he is done (`" + LIVE_TXT + "`, md5 `" + LIVE_MD5 + "`). "
       "His act, not a ruling; `_rulings.json` 638. The same headline is struck on `" + HO_PREV + "`. What the new opener costs is carried as ① above. "
       "NOT STRUCK, STILL OPEN: the chain made more efficient, and whether the working line moves toward 256K")
assert '·' not in WHY
segs = old.split('·')
hit = 0
for i, s in enumerate(segs):
    if s.strip().startswith(KEY):
        segs[i] = s.rstrip() + ' ⛔ **' + WHY + '.** '
        hit += 1
assert hit == 1, hit
old = '·'.join(segs)
NEW = [
 "⬛ **① WHAT DOES THE NEW OPENER COST? #301 IS THE FIRST CHAT UNDER HIS PASTED INSTRUCTIONS** [NEW — 0, DAVE'S] — before \"wrap\" at #300 he pasted the plan page's start-of-chat text (his act, not a ruling; `" + LIVE_TXT + "`, md5 `" + LIVE_MD5 + "`, the diff in `" + LIVE + "`): one shell call, the handoff and `_CHAIN.md` still read, no Project-memory read or write at the opener or while the chat is live. Hand-sum #301's fill in the cloud shell at the first reply and after his first message, against the page's projection (~161K after his first message; lane C's table ~156,300 at the first reply) and #300's 187,863 and 211,454 (" + B + "). The ~126K boot will not move",
 "⬛ **② THE PAGE'S TWO OTHER BEFORE-FRIDAY MOVES — HELPERS DO THE LONG THINKING, AND TYPE, DON'T STOP — ARE THEY HIS?** [NEW — 0, DAVE'S] — `" + PLAN + "`, moves 3 and 4. He did move 1 (the paste), which carries move 2 in its step 4. Move 3: subs do the long thinking and writing and the conductor reads their reports from disk (up to ~37K lighter on a heavy day, lane P, `" + REPP + "`). Move 4: his 16:56 BST stop discarded the running turn and threw away the first X and P (~17.1M input processed), while his 16:08 and 16:16 notes, typed mid-run, got through without a stop (lane X, `" + REPX + "` §3.1). Put to him in the conductor's last reply (17:46 BST); not answered",
 "⬛ **③ AFTER FRIDAY — THE PAGE'S SIX STEPS AND SEVEN QUESTIONS, EACH WITH THE ADVERSARY'S VERDICT BESIDE IT: WHICH, AND IN WHAT ORDER?** [NEW — 0, DAVE'S] — the page's order: copy the memory store into the repo, index the handoff and chain with a BM25 ranking, build the card and run the quiz on three fresh chats, prepare and trial the Mac seat, his rulings, then (with his word) cut the store. The seven questions: handoff and chain, or card and chain after three quiz passes; the memory note after \"done\", or no Apollo memory; cut the store or leave it; trial the Mac seat; keep the declared wrap path until the seat is decided; restore or retire the silent check-in's five checks; Jev at the start as an add-only extra, or dev-only. X's verdict beside each is tabled in `" + HO + "` item 11. None is needed before Friday",
 "⬛ **④ HIS PASTE MADE TWO RUNBOOK LINES STALE — AMEND BY ADDITION?** [NEW — 0, DAVE'S] — `knowledge/_RUNBOOK-capture-ritual.md` step 3's #278 paragraph still has the NEXT opener place the memory hook, and `knowledge/_RUNBOOK-render-verify.md` still says \"after the `_checkin.py` step\"; his pasted instructions now place the note after he says he is done and drop the check-in from the opener (lane C's minimal change set, item 2, `" + REPC + "`). Not amended at the #300 wrap, because his paste is an act, not a ruling",
 "⚠ **⑤ THE GIT REMOTE'S URL CARRIES A GITHUB TOKEN IN `.git/config` — MOVE IT TO A CREDENTIAL HELPER?** [NEW — 0, DAVE'S] — lane X, claim B8 (`" + REPX + "`): a 93-character `github_pat_` token in the `origin` URL, masked in the report; no leak found in five flagged repo files or in any #300 transcript, and the #300 wrap seat's scan of every #300 file found none. A note, not a lever (lane P)",
]
for n in NEW:
    assert '·' not in n, n[:60]
line = '> **residual → #301:** ' + ' · '.join(NEW) + ' ·  ' + old.strip()
L[45:45] = ['## residual → #301', '', line, '']
open(P, 'w', encoding='utf-8').write('\n'.join(L))
chk = open(P, encoding='utf-8').read().split('\n')
l301 = next(l for l in chk if l.startswith('> **residual → #301:**'))
items = cg._carry_items(l301)
l300 = next(l for l in chk if l.startswith('> **residual → #300:**'))
print('items', len(items), 'prev', len(cg._carry_items(l300)), 'struck-this-wrap', l301.count('STRUCK IN PART AT THE #300 WRAP'), 'new', len(NEW))
