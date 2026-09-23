# #301 wrap seat - write _CARRIES.md section "residual -> #302": new #301 items first, then the
# #301 set with EVERY age bracket +1 (the #297-#300 rule, re-verified below against #300's own bump),
# FOUR whole strikes and TWO headline strikes appended BY ADDITION with receipts (s183-D1 / s188-D2).
import re, sys
sys.path.insert(0, 'knowledge'); sys.path.insert(0, 'notes/_lanes/301/W/_work')
import _capture_gate as cg
from names_301 import *
AGE = cg._AGE_RE
P = '_CARRIES.md'
txt = open(P, encoding='utf-8').read()
L = txt.split('\n')
assert L[45] == '## residual → #301' and L[47].startswith('> **residual → #301:**'), (L[45], L[47][:40])
assert L[49] == '## residual → #300' and L[51].startswith('> **residual → #300:**')
assert '## residual → #302' not in txt
def bump_all(s):
    s = re.sub(r"\[NEW — 0(,[^\]]*)?\]", lambda m: '[\x00' + (m.group(1) or '') + ']', s)
    s = AGE.sub(lambda m: '[' + str(int(m.group(1)) + 1) + m.group(0)[1 + len(m.group(1)):], s)
    return s.replace('[\x00', '[1')
body = re.sub(r"^> \*\*residual → #301:\*\*", "", L[47]).strip()
b300 = re.sub(r"^> \*\*residual → #300:\*\*", "", L[51]).strip()
old301 = body.split(' ·  ', 1)[1]
bb = bump_all(b300).split('·'); oo = old301.split('·')
diff = [i for i in range(min(len(bb), len(oo))) if bb[i].strip() != oo[i].strip()]
print('verify +1 on #300->#301: segs', len(bb), len(oo), 'differing', len(diff), '(expect 1 = #300 headline strike)', diff[:5])
old = bump_all(body)
B = '`' + BRIEF + '`'; G = '`' + REPG + '`'
TAIL = " The strike is recorded by addition on `" + HO_PREV + "` too; `_rulings.json` 638, nothing inscribed"
STRIKES = [
 ("⬛ **① WHAT DOES THE NEW OPENER COST? #301 IS THE FIRST CHAT UNDER HIS PASTED INSTRUCTIONS**",
  "STRUCK AT THE #301 WRAP, BY ADDITION, WORDING ABOVE UNCHANGED — MEASURED. RECEIPT: the #301 wrap seat's hand sum over the conductor's cloud transcript (`" + TRANSCRIPT + "`, input + cache creation + cache read per distinct message id), reproducing the conductor's own figures in " + B + " fact 1: boot 126,767, 163,380 going into the first reply (the page projected ~156,300), 187,604 after his first message (the page projected ~161K; #300 211,454) and NO memory re-send. The miss against the page is the conductor's own first-reply output (24,060) carried forward whole, a NEW finding carried as ⑤ above" + TAIL),
 ("⬛ **② 07 AND 08 STILL REST AT −35 WHILE THE BRAIN (10) AND THE CALLIPERS (09) REST AT −27 — SHOULD 07 AND 08 MATCH?**",
  "STRUCK AT THE #301 WRAP, BY ADDITION, WORDING ABOVE UNCHANGED. RECEIPT: his 19:26 BST words of 2026-09-23, item 3, answering whether 07, 08 and 13's graph rest at −27 like 09 and 10: *\"don't worry about this\"* (verbatim in " + B + "). Nothing was changed in the deck. The chain's delta said −35 where the handoff said −27; now moot" + TAIL),
 ("⬛ **③ \"THE ASK\" IS A CHAPTER ON THE RAIL BUT NOT IN THE ORDER OF PLAY ON 02 — DOES HIS #296 WORD STILL STAND?**",
  "STRUCK AT THE #301 WRAP, BY ADDITION, WORDING ABOVE UNCHANGED. RECEIPT: his 19:26 BST words of 2026-09-23, item 1: *\"no chapter mention on the index, thats fine\"* (verbatim in " + B + "). 02 stays as it is" + TAIL),
 ("⬛ **④ THE 26 REVIEW SUGGESTIONS HE NEVER ANSWERED — WHICH, IF ANY, BEFORE FRIDAY?**",
  "STRUCK IN PART AT THE #301 WRAP, BY ADDITION, WORDING ABOVE UNCHANGED — THE \"Judgment or judgement\" QUESTION ONLY. RECEIPT: his 19:26 BST words, item 4: *\"can you surface that doc again for me, 'judgement' is correct\"* (verbatim in " + B + "); slide 12's plate title changed Judgment → Judgement in the SOURCE `" + DECK_SRC + "` and the deck `" + DECK + "` rebuilt by `build_c.py` (one character, proven by diff, NOT rendered), committed with the #301 wrap. NOT STRUCK, STILL OPEN: which of the 26 — the review was surfaced again (`" + REVIEW + "`) and he picked none" + TAIL),
 ("⬛ **⑤ AFTER FRIDAY — HIS \"careful plan\" FOR THE OPENER, THE CHAIN MADE MORE EFFICIENT, AND HIS 256K QUESTION**",
  "STRUCK IN PART AT THE #301 WRAP, BY ADDITION, WORDING ABOVE UNCHANGED — HIS 256K QUESTION. RECEIPT: his 20:21 BST words of 2026-09-23, *\"" + Q2021 + "\"*, and at 19:45 *\"Lets try 300k and cross our fingers\"* (verbatim in " + B + "); lane G set `knowledge/_gauge_tokens.py` `BUDGET_WORKING` 256,000 and `BUDGET_HARD` 300,000, PICKED Dave #301 (" + G + "). His acts, enacted in code, NOT inscribed. NOT STRUCK, STILL OPEN: the chain made more efficient" + TAIL),
 ("⬛ **④ THE LAPTOP-SIZE HEADLINES WRAP ON 07 (THREE LINES) AND 08 (FOUR)**",
  "STRUCK AT THE #301 WRAP, BY ADDITION, WORDING ABOVE UNCHANGED. RECEIPT: his 19:26 BST words of 2026-09-23, item 2, answering the 07 and 08 laptop headlines: *\"this  is fine for Friday\"* (verbatim in " + B + "). Nothing was changed in the deck" + TAIL),
]
segs = old.split('·')
for key, why in STRIKES:
    assert '·' not in why, why[:60]
    hits = [i for i, s in enumerate(segs) if s.strip().startswith(key)]
    assert len(hits) == 1, (key, hits)
    segs[hits[0]] = segs[hits[0]].rstrip() + ' ⛔ **' + why + '.** '
old = '·'.join(segs)
NEW = [
 "⬛ **① THE DEMO BRIEF — \"TOMORROW\", HIS WORD** [NEW — 0, DAVE'S] — his 19:26 BST words of 2026-09-23, item 5, answering when the demo brief comes: *\"Yes lets not worry about that until tomorrow\"* (verbatim in " + B + "). Deferred by him, NOT struck. The cold source is `" + GRILL + "`; he said at #296 *\"but we'll make changes to it\"*. Friday is 2026-09-25, so tomorrow is Thursday 2026-09-24",
 "⬛ **② THE STOP LINE (180,000) AND THE TOLERANCE LINE (220,000) NOW SIT UNDER THE 256K WORKING LINE — MOVE THEM TO 236K AND 276K, THE SAME OFFSETS?** [NEW — 0, DAVE'S] — put to him in the conductor's 20:21 reply; \"wrap\" came before an answer. The order was stop < working < tolerance < hard and is now stop < tolerance < working < hard, so the seam's \"OUTSIDE TOLERANCE, no more lanes\" fires 36,000 before the working line (lane G, " + G + " § Follow-up). No code asserts an order between them",
 "⬛ **③ HIS THREE WINDOW WORDS ARE ENACTED IN CODE BUT NOT INSCRIBED — INSCRIBE THEM?** [NEW — 0, DAVE'S] — *\"" + Q1945 + "\"* (19:45), then *\"" + Q1947 + "\"* (19:47, choosing the window's hard line over the boot ceiling), then *\"" + Q2021 + "\"* (20:21). Lane G enacted them as PICKED Dave #301 (" + G + "); he never said \"inscribe\", so `_rulings.json` stays 638 and the #301 wrap records them as his acts (the #296 to #300 precedent). The boot ceiling `BOOT_CEILING_TK` 72,768 did not move and the declared not-a-wrap path stays until the Mac seat",
 "⚠ **④ `knowledge/_standing.md:19` IS RATIFIED AS WRITTEN (`s287-D1`) AND LANE G REWORDED IT ON HIS NUMBERS — IS THE WORDING HIS?** [NEW — 0, DAVE'S] — the line now reads working 256,000 and hard 300,000 with his three quotes; the standing block measures 291 of its 300-token ceiling by the seam's own count, 9 under (" + G + "). Lane G's first report said the file was not to be touched; its follow-up touched line 19 on his 20:21 numbers",
 "⚠ **⑤ THE CONDUCTOR'S OWN REASONING STAYS IN THE WINDOW** [NEW — 0] — measured at #301 (" + B + " fact 1): the first reply's 24,060 output, ~22K of it reasoning, carried forward whole, and the conductor's output was 45,995 over its first nine calls. That, not a memory re-send, is why 187,604 after his first message missed the page's ~161K. The conductor adopted a practice after it: keep its own reasoning short and send edits, renders and checks to helpers, which is the plan page's move 3 (`" + PLAN + "`), carried above as his to confirm",
 "⚠ **⑥ THE JUDGEMENT FIX IS PROVEN BY DIFF, NOT RENDERED** [NEW — 0] — the rebuilt deck (530,658 B) equals the old deck with that one swap reversed (a one-character delta); judgment 0 and judgement 4 in both the source and the deck (" + B + " fact 3). A render at Dave's seat before Friday would show slide 12's plate by eye",
]
for n in NEW:
    assert '·' not in n, n[:60]
line = '> **residual → #302:** ' + ' · '.join(NEW) + ' ·  ' + old.strip()
L[45:45] = ['## residual → #302', '', line, '']
open(P, 'w', encoding='utf-8').write('\n'.join(L))
chk = open(P, encoding='utf-8').read().split('\n')
l302 = next(l for l in chk if l.startswith('> **residual → #302:**'))
items = cg._carry_items(l302)
l301 = next(l for l in chk if l.startswith('> **residual → #301:**'))
print('items', len(items), 'prev', len(cg._carry_items(l301)), 'struck-this-wrap', l302.count('AT THE #301 WRAP, BY ADDITION'), 'new', len(NEW))
