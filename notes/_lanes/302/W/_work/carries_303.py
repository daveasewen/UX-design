# #302 wrap seat - write _CARRIES.md section "residual -> #303": new #302 items first, then the
# #302 set with EVERY age bracket +1 (the #297-#301 rule, re-verified below against #301's own bump),
# ONE item struck IN PART by addition with its receipt (s183-D1 / s188-D2). Modelled on #301's carries_302.py.
import re, sys
sys.path.insert(0, 'knowledge'); sys.path.insert(0, 'notes/_lanes/302/W/_work')
import _capture_gate as cg
from names_302 import *
AGE = cg._AGE_RE
P = '_CARRIES.md'
txt = open(P, encoding='utf-8').read()
L = txt.split('\n')
assert L[45] == '## residual → #302' and L[47].startswith('> **residual → #302:**'), (L[45], L[47][:40])
assert L[49] == '## residual → #301' and L[51].startswith('> **residual → #301:**')
assert '## residual → #303' not in txt
def bump_all(s):
    s = re.sub(r"\[NEW — 0(,[^\]]*)?\]", lambda m: '[\x00' + (m.group(1) or '') + ']', s)
    s = AGE.sub(lambda m: '[' + str(int(m.group(1)) + 1) + m.group(0)[1 + len(m.group(1)):], s)
    return s.replace('[\x00', '[1')
body = re.sub(r"^> \*\*residual → #302:\*\*", "", L[47]).strip()
b301 = re.sub(r"^> \*\*residual → #301:\*\*", "", L[51]).strip()
old302 = body.split(' ·  ', 1)[1]
bb = bump_all(b301).split('·'); oo = old302.split('·')
diff = [i for i in range(min(len(bb), len(oo))) if bb[i].strip() != oo[i].strip()]
print('verify +1 on #301->#302: segs', len(bb), len(oo), 'differing', len(diff), '(expect 6 = #301 strikes on 4 items + 2 headlines)', diff[:8])
old = bump_all(body)
B = '`' + BRIEF + '`'
TAIL = " The strike is recorded by addition on `" + HO_PREV + "` too; `_rulings.json` 638, nothing inscribed"
STRIKES = [
 ("⬛ **① THE ASK ON SLIDE 15, THEN POLISH FOR FRIDAY — WHAT GOES ON THE ASK, AND WHICH POLISH COMES FIRST?**",
  "STRUCK IN PART AT THE #302 WRAP, BY ADDITION, WORDING ABOVE UNCHANGED — WHAT GOES ON THE ASK, AS HIS ITEM. RECEIPT: his 07:43 BST words of 2026-09-24, answering the opener's first question (the ask): *\"" + Q0743 + "\"* (verbatim in " + B + "). The ask is now slide 16 of 17 (a benefits slide went in before it) and is still stamped DRAFT until his colleagues' words come. NOT STRUCK, STILL OPEN: which polish comes first, and whether the slide's words, when they come, go in as given" + TAIL),
]
segs = old.split('·')
for key, why in STRIKES:
    assert '·' not in why, why[:60]
    hits = [i for i, s in enumerate(segs) if s.strip().startswith(key)]
    assert len(hits) == 1, (key, hits)
    segs[hits[0]] = segs[hits[0]].rstrip() + ' ⛔ **' + why + '.** '
old = '·'.join(segs)
NEW = [
 "⬛ **① THE DEMO PROMPT — HE ASKED TO SEE IT AT 12:42, AND FRIDAY IS TOMORROW** [NEW — 0, DAVE'S] — his 07:43 BST words of 2026-09-24, answering the opener's second question (the demo brief): *\"" + Q0743b + "\"*; the changes came (slides 11 to 13, the Scrutiny plate, the callipers, a new slide 15), and at 12:42 he wrote *\"" + Q1242 + "\"*. There was no room (285,325, over the 256K working line), so the conductor recommended a fresh chat. The cold source is `" + GRILL + "`; he said at #296 *\"but we'll make changes to it\"*. Friday is 2026-09-25",
 "⬛ **② SLIDE 15'S LIGHT HEADWORDS — CHECK THEM ON HIS OWN SCREEN** [NEW — 0, DAVE'S] — Customisation, Convergence and Cost-effectiveness at weight 300, clamp(26px,2.5vw,40px), print 34px, with $3.2m bold red, on his 11:52 BST words *\"make the font light rather than thin and make $3.2m bold and red\"* and 12:32 *\"" + Q1232 + "\"*. The seat cannot show Univers Next (③), so only his screen shows the Light weight as he will present it (" + B + ")",
 "⬛ **③ THE SEAT RENDERS ON A FALLBACK FACE — ADD `HSBC_MtUnivers_Latin` TO THE DECK'S FONT STACK?** [NEW — 0, DAVE'S] — NEW FINDING at #302: the render seat does not resolve \"Univers Next\", so every weight falls back to a Helvetica-style face (`" + WT + "`). The HSBC face is at the seat as `HSBC_MtUnivers_Latin` (Thin, Light, Medium, Bold), but the deck's --font stack never names it. So every by-eye type judgement from seat renders, this session and earlier, was on the fallback face. Offered to him; unanswered",
 "⬛ **④ SLIDE 13 SAYS \"judgement layer\" WHILE ITS DRAWING IS SLIDE 12'S KNOWLEDGE AND GRAPH SPHERE — KEEP, OR \"knowledge layer\"?** [NEW — 0, DAVE'S] — his 07:52 BST words: *\"'The twelve types of entities in the graph.' change to 'The twelve types of entity in the judgment layer.\"*, enacted as \"judgement\" on his #301 word (*\"'judgement' is correct\"*). The conductor flagged the clash with slide 12's plates; unanswered (" + B + ")",
 "⬛ **⑤ THE CALLIPERS OVERRUN THE FRAME BY ABOUT 50PX AT THE EXTREME ORBIT CORNER — LEAVE, OR REFRAME?** [NEW — 0, DAVE'S] — the rest view is in frame and he said *\"this is perfect.\"* (11:28 BST); at the extreme orbit corner the tray overruns the frame by about 50px. Put to him; unanswered. The rod-end tilt is one command away: `" + SWAP + "` B (lane A, `" + REPA + "`)",
 "⚠ **⑥ LANE A'S OWN WINDOW CLOSED AT 303,392, OVER THE 300K HARD LINE** [NEW — 0] — a hand sum at the #302 wrap seat over `" + LANE_A_T + "` (110 distinct messages, resumed three times, 07:00 to 10:47 UTC). A sub's window, not the conductor's; the lines his #301 words moved are written for the conductor. Named, not graded. His 19:45 words at #301 were *\"let just use subs to stretch the window as much as possible\"*",
]
for n in NEW:
    assert '·' not in n, n[:60]
line = '> **residual → #303:** ' + ' · '.join(NEW) + ' ·  ' + old.strip()
L[45:45] = ['## residual → #303', '', line, '']
open(P, 'w', encoding='utf-8').write('\n'.join(L))
chk = open(P, encoding='utf-8').read().split('\n')
l303 = next(l for l in chk if l.startswith('> **residual → #303:**'))
items = cg._carry_items(l303)
l302 = next(l for l in chk if l.startswith('> **residual → #302:**'))
print('items', len(items), 'prev', len(cg._carry_items(l302)), 'struck-this-wrap', l303.count('AT THE #302 WRAP, BY ADDITION'), 'new', len(NEW))
open('notes/_lanes/302/W/_work/carries_count.txt', 'w').write(str(len(items)) + '\n')
