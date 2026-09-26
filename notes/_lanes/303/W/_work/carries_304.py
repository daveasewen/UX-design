# #303 wrap seat - write _CARRIES.md section "residual -> #304": new #303 items first, then the #303 set
# with EVERY age bracket +1 (the #297-#302 rule, re-verified below against #302's own bump), and the
# strikes BY ADDITION with receipts (s183-D1 / s188-D2). Modelled on #302's carries_303.py.
import re, sys
sys.path.insert(0, 'knowledge'); sys.path.insert(0, 'notes/_lanes/303/W/_work')
import _capture_gate as cg
from names_303 import *
AGE = cg._AGE_RE
P = '_CARRIES.md'
txt = open(P, encoding='utf-8').read()
L = txt.split('\n')
assert L[45] == '## residual → #303' and L[47].startswith('> **residual → #303:**'), (L[45], L[47][:40])
assert L[49] == '## residual → #302' and L[51].startswith('> **residual → #302:**')
assert '## residual → #304' not in txt
def bump_all(s):
    s = re.sub(r"\[NEW — 0(,[^\]]*)?\]", lambda m: '[\x00' + (m.group(1) or '') + ']', s)
    s = AGE.sub(lambda m: '[' + str(int(m.group(1)) + 1) + m.group(0)[1 + len(m.group(1)):], s)
    return s.replace('[\x00', '[1')
body = re.sub(r"^> \*\*residual → #303:\*\*", "", L[47]).strip()
b302 = re.sub(r"^> \*\*residual → #302:\*\*", "", L[51]).strip()
# #303's line = 6 new + ' · ' + bumped #302 body (with #302's one strike appended). Verify the +1 rule.
old303_tail = body.split(' ·  ', 1)[1]
bb = bump_all(b302).split('·'); oo = old303_tail.split('·')
diff = [i for i in range(min(len(bb), len(oo))) if bb[i].strip() != oo[i].strip()]
print('verify +1 on #302->#303: segs', len(bb), len(oo), 'differing', len(diff), '(expect 1 = the #302 strike on the ask)', diff[:8])
old = bump_all(body)
B = '`' + BRIEF + '`'
TAIL = " `_rulings.json` 638, nothing inscribed; his changes are his acts"
STRIKES = [
 ("⬛ **① THE DEMO PROMPT — HE ASKED TO SEE IT AT 12:42, AND FRIDAY IS TOMORROW**",
  "STRUCK AT THE #303 WRAP, BY ADDITION, WORDING ABOVE UNCHANGED — BY HIS ACT. RECEIPT: his 15:37 BST words of 2026-09-24, answering it at #303's opener: *\"I've tested this already, and it doesn't ask the questions, they are answered already, but if you recommend restructuring I'm happy with that, " + Q1537 + ".\"*; three observations at 15:46; closed at 15:51 *\"" + Q1551 + "\"* The restructured prompt is `" + PROMPT + "`, committed at `" + SHA1 + "` (" + B + "). Whether he tested it, and how it ran, is carried as a NEW #303 item." + TAIL),
 ("⬛ **② SLIDE 15'S LIGHT HEADWORDS — CHECK THEM ON HIS OWN SCREEN**",
  "STRUCK AT THE #303 WRAP, BY ADDITION, WORDING ABOVE UNCHANGED — SUPERSEDED BY HIS ACT. RECEIPT: at 18:00 to 18:35 BST on 2026-09-24 he rebuilt the benefits slide on new input into one 3x2 grid of six (*\"" + Q1814 + "\"*, 18:14), titled *\"Deliver more, faster, at much lower cost\"* (18:35); the three Light headwords are gone from the live deck (the earlier versions are parked in `<template id=\"parked-s11-two-slides\">` in `" + DECK_SRC + "`). His 18:39 ask to get the first two titles on one line was checked with the HSBC face forced (" + B + ")." + TAIL),
 ("⬛ **④ SLIDE 13 SAYS \"judgement layer\" WHILE ITS DRAWING IS SLIDE 12'S KNOWLEDGE AND GRAPH SPHERE — KEEP, OR \"knowledge layer\"?**",
  "STRUCK AT THE #303 WRAP, BY ADDITION, WORDING ABOVE UNCHANGED — BY HIS ACT. RECEIPT: his 15:57 BST words of 2026-09-24: *\"slide 13: " + Q1557 + " 'A smart design system' -- 'Anatomy of a smart design system'\"*. The title is gone, so the clash is gone (" + B + ")." + TAIL),
 ("⬛ **① THE DEMO BRIEF — \"TOMORROW\", HIS WORD**",
  "STRUCK AT THE #303 WRAP, BY ADDITION, WORDING ABOVE UNCHANGED — BY HIS ACT, THE SAME RECEIPT AS #303's ① ABOVE: his 15:37 BST words of 2026-09-24 and the restructured prompt `" + PROMPT + "` (" + B + ")." + TAIL),
 ("⬛ **① THE ASK ON SLIDE 15, THEN POLISH FOR FRIDAY — WHAT GOES ON THE ASK, AND WHICH POLISH COMES FIRST?**",
  "FURTHER STRUCK IN PART AT THE #303 WRAP, BY ADDITION, WORDING ABOVE UNCHANGED — WHETHER THE ASK'S WORDS GO IN AS GIVEN. RECEIPT: at 17:12 BST on 2026-09-24 he gave the slide his OWN copy, *\"Slide 15: " + Q1712 + " What we do next\"* with five steps; the draft ask is parked in a comment in `" + DECK_SRC + "`, not deleted, and the DRAFT stamp is off the live deck. His colleagues' ask is superseded by his act, not by a ruling (" + B + "). NOT STRUCK, STILL AS CARRIED: which polish comes first." + TAIL),
 ("⬛ **⑥ THE DEMO BRIEF'S CHANGES ARE HIS**",
  "STRUCK AT THE #303 WRAP, BY ADDITION, WORDING ABOVE UNCHANGED — HE GAVE THEM. RECEIPT: his 15:37 and 15:46 BST words of 2026-09-24 (Common, liberal with data visualisations, the bento section on the lightest grey, components at their own size, the lightest pattern per interaction), in `" + PROMPT + "` (" + B + ")." + TAIL),
]
segs = old.split('·')
for key, why in STRIKES:
    assert '·' not in why, why[:60]
    hits = [i for i, s in enumerate(segs) if s.strip().startswith(key) or s.strip().startswith('> **residual → #303:** ' + key)]
    assert len(hits) == 1, (key, hits)
    segs[hits[0]] = segs[hits[0]].rstrip() + ' ⛔ **' + why + '** '
old = '·'.join(segs)
NEW = [
 "⬛ **① THE APOLLO-MCP PROPOSAL PAGE — HE ASKED FOR IT, AND IT IS #304'S FIRST BEAT** [NEW — 0, DAVE'S] — his 13:29 BST words of Saturday 2026-09-26: *\"" + Q1329 + "\"*. Two lanes ran and filed: G1, the repo archaeology (`" + REPG1 + "`), and G2, the landscape, 40 dated sources (`" + REPG2 + "`). The page was NOT written, because the conductor's window was at 392,986. The conductor's recommended headline: do not invent a protocol; publish Apollo as a versioned A2UI catalogue served over MCP, with MCP Apps as the fallback shell; Apollo adds when-to-use, gates before anything renders, entitlements at the tool scope and the graph as the audit record; first vehicle the June note's contextual dashboard (`" + VISION + "`). ⚠ G1's caution: Jev is ruled dev-time only (#294). Swiss-design-system HTML, in the repo beside its sources",
 "⬛ **② HIS THREE DEMO OBSERVATIONS — ROLL THEM INTO THE GRAPH** [NEW — 0, DAVE'S] — his 15:46 BST words of 2026-09-24: the bento section (only the section, not the page or the title) on the lightest grey; buttons and table headings coming out smaller than they should; and a modal chosen where a split button or a drop-down would be better. *\"" + Q1546 + "\"*. In the prompt only as quality expectations, at his ask (" + B + ")",
 "⬛ **③ DID THE COMMON PROMPT RUN, AND HOW?** [NEW — 0, DAVE'S] — *\"" + Q1551 + "\"* (15:51 BST, 2026-09-24). The file is `" + PROMPT + "`. Put, not answered in the record",
 "⬛ **④ FRIDAY 2026-09-25 — WHAT CAME BACK?** [NEW — 0, DAVE'S] — the presentation happened after this session's Thursday work; nothing he said on Friday or Saturday mentions it. Ask; do not assume an outcome",
 "⬛ **⑤ WHICH SPIDER PACK IS ON HIS WORK MACHINE?** [NEW — 0, DAVE'S] — his 19:44 BST question *\"so we included the spider pack too?\"* was answered yes (v1.0.13, cut 2026-09-11, seven commits since have touched components or canon) and the conductor asked which pack his work machine has; unanswered. The bundles `" + ZIP + "` (22 MB) and `" + ZIP_SMALL + "` (1 MB) are gitignored and stay untracked on purpose",
 "⚠ **⑥ THE CONDUCTOR'S WINDOW RAN 102,607 PAST THE 300K HARD LINE** [NEW — 0] — a hand sum at the #303 wrap seat over `" + TRANSCRIPT + "`: boot 128,423, over 300,000 at 18:01:54 BST on Thursday (the 85th distinct message), 392,986 at 13:42:58 BST on Saturday, and 402,607 at the message that launched the wrap seat. Named, not graded; lane P's own window closed at 262,025",
]
for n in NEW:
    assert '·' not in n, n[:60]
line = '> **residual → #304:** ' + ' · '.join(NEW) + ' ·  ' + old.strip()
L[45:45] = ['## residual → #304', '', line, '']
open(P, 'w', encoding='utf-8').write('\n'.join(L))
chk = open(P, encoding='utf-8').read().split('\n')
l304 = next(l for l in chk if l.startswith('> **residual → #304:**'))
items = cg._carry_items(l304)
l303 = next(l for l in chk if l.startswith('> **residual → #303:**'))
print('items', len(items), 'prev', len(cg._carry_items(l303)), 'struck-this-wrap', l304.count('AT THE #303 WRAP, BY ADDITION'), 'new', len(NEW))
open('notes/_lanes/303/W/_work/carries_count.txt', 'w').write(str(len(items)) + '\n')
