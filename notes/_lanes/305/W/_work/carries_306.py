# #305 wrap seat - write _CARRIES.md section "residual -> #306": new #305 items first, then the #305 set
# with EVERY age bracket +1 (the #297-#304 rule), and the strikes BY ADDITION with receipts
# (s183-D1 / s188-D2). Modelled on #304's carries_305.py. The #305 line is the one H1 dieted under
# s305-D36 (715 -> 391); nothing here re-words it.
import re, sys
sys.path.insert(0, 'knowledge'); sys.path.insert(0, 'notes/_lanes/305/W/_work')
import _capture_gate as cg
from names_305 import *
AGE = cg._AGE_RE
P = '_CARRIES.md'
txt = open(P, encoding='utf-8').read()
L = txt.split('\n')
i305 = L.index('## residual → #305')
assert L[i305 + 3].startswith('> **residual → #305:**'), L[i305 + 3][:60]
assert L[i305 + 2].startswith('<!-- CARRY DIET `s305-D36`')
assert '## residual → #306' not in txt
def bump_all(s):
    s = re.sub(r"\[NEW — 0(,[^\]]*)?\]", lambda m: '[\x00' + (m.group(1) or '') + ']', s)
    s = AGE.sub(lambda m: '[' + str(int(m.group(1)) + 1) + m.group(0)[1 + len(m.group(1)):], s)
    return s.replace('[\x00', '[1')
body = re.sub(r"^> \*\*residual → #305:\*\*", "", L[i305 + 3]).strip()
old = bump_all(body)
TAIL = " `_rulings.json` 699 at the #305 wrap"
B = '`' + BRIEF + '`'
STRIKES = [
 ("⬛ **① THE TUESDAY SITTING, 53 CALLS — CALL 1 FIRST",
  "STRUCK AT THE #305 WRAP, BY ADDITION, WORDING ABOVE UNCHANGED — BY HIS ACT. RECEIPT: he took the sitting on Sunday 2026-09-27, 13:59 to 14:53 BST, through the artifact, and returned `" + EXPORT1 + "` (53 calls and Friday); lane A inscribed `s305-D1` to `s305-D57` (`" + R['A'] + "`, committed at `27efb7b6`); call 1 was cut as v1.0.14 at `0ef30746`, `02d679b3` and `d3b809a7` (`" + R['K'] + "`), pushed and read back green in CI run `36349147952`." + TAIL),
 ("⬛ **② THREE BEHAVIOURS SHIPPED ON A VERIFIER'S READING",
  "STRUCK AT THE #305 WRAP, BY ADDITION, WORDING ABOVE UNCHANGED — RULED. RECEIPT: sitting call 6 kept the tick thinning and the right-hand twin (`s305-D7`, ratifying `3100da99` and `52049781`; his comment on complex charts is the new thread `W-305n1`) and call 13 kept the console padding (`s305-D14`, ratifying `4be130e5`), both inscribed at `27efb7b6`." + TAIL),
 ("⬛ **③ TWO THINGS HELD BACK FOR HIS EYE",
  "STRUCK AT THE #305 WRAP, BY ADDITION, WORDING ABOVE UNCHANGED — RULED. RECEIPT: call 5 took the clip-visible Kpi-tile form (`s305-D6`, built by B1 `" + R['B1'] + "` and stamped enacted at `568e2534`); call 41c kept today's trim through the cut and re-reviews the root version after it (`s305-D43`)." + TAIL),
 ("⬛ **④ THE APOLLO-MCP PAGE'S SEVEN DECISIONS",
  "STRUCK AT THE #305 WRAP, BY ADDITION, WORDING ABOVE UNCHANGED — RULED. RECEIPT: sitting calls 42 to 51 ruled them as `s305-D45` to `s305-D54`: route B, the PoC's scope, Jev as a ranker behind a switch, the name Launchpad (Apollo as eyebrow), the October start once calls 14 to 19 are in the tree, the delivery order; and his Friday words make the PoC a surprise (`" + FRIDAY + "`, row `W-305n6`)." + TAIL),
 ("⬛ **⑤ JEV AS AN EDGE SUGGESTER",
  "STRUCK AT THE #305 WRAP, BY ADDITION, WORDING ABOVE UNCHANGED — RULED AND BUILT. RECEIPT: call 52 said cut the hand-run sweep (`s305-D55`), W2 built it under `notes/` and ran it, 330 links asked and 13 look wrong, stamped enacted at `e4ff4284` (`" + R['W2'] + "`); call 53 is `s305-D56`." + TAIL),
 ("⚠ **⑥ THE REVIEW SURFACE IS NOW ONE ARTIFACT",
  "STRUCK AT THE #305 WRAP, BY ADDITION, WORDING ABOVE UNCHANGED — THE HUB'S LINKS OPEN. RECEIPT: he opened the sitting through the hub and returned his export at 14:53 BST (`" + EXPORT1 + "`), and his 20:04 BST screenshot shows the hub's list of pages 1 to 11 (" + B + "). A NEW lesson on the pages' pictures is carried as a #305 item." + TAIL),
 ("⬛ **③ DID THE COMMON PROMPT RUN, AND HOW?**",
  "STRUCK AT THE #305 WRAP, BY ADDITION, WORDING ABOVE UNCHANGED — ANSWERED IN HIS WORDS. RECEIPT: *\"" + QPROMPT + "\"* (his sitting export, Sunday 14:53 BST, recorded in `" + FRIDAY + "`)." + TAIL),
 ("⬛ **④ FRIDAY 2026-09-25 — WHAT CAME BACK?**",
  "STRUCK AT THE #305 WRAP, BY ADDITION, WORDING ABOVE UNCHANGED — ANSWERED IN HIS WORDS. RECEIPT: *\"" + QFRI + "\"* and *\"" + QSURPRISE + "\"* (`" + FRIDAY + "`); the surprise is store row `W-305n6`." + TAIL),
 ("⬛ **⑤ WHICH SPIDER PACK IS ON HIS WORK MACHINE?**",
  "STRUCK AT THE #305 WRAP, BY ADDITION, WORDING ABOVE UNCHANGED — ANSWERED IN HIS WORDS. RECEIPT: *\"" + Q13 + "\"* (Sunday) and, asked what 13 meant, *\"" + Q13B + "\"* (Monday 08:05 BST, `" + EXPORT2 + "`), both in `" + FRIDAY + "`: v1.0.13." + TAIL),
 ("⬛ **③ HIS THREE WINDOW WORDS ARE ENACTED IN CODE BUT NOT INSCRIBED",
  "STRUCK AT THE #305 WRAP, BY ADDITION, WORDING ABOVE UNCHANGED — INSCRIBED. RECEIPT: sitting call 28 is `s305-D28` (working 256,000, hard 300,000, stop 236,000, tolerance 276,000), enacted by H2 in `_gauge_tokens.py` (`" + R['H2'] + "`)." + TAIL),
 ("⚠ **⑤ THE GIT REMOTE'S URL CARRIES A GITHUB TOKEN",
  "STRUCK AT THE #305 WRAP, BY ADDITION, WORDING ABOVE UNCHANGED — DONE. RECEIPT: sitting call 30 is `s305-D30`; C1 moved the token into `.git/apollo-credentials` behind a get-only credential helper and set a clean `origin` URL (`" + R['C1'] + "`), and H2 taught `_git_commit.sh --push` the helper (`" + R['H2'] + "`). The token's expiry is unchanged." + TAIL),
 ("⬛ **⑥ THE SPIDER `v1.0.14` CUT IS ARMED",
  "STRUCK AT THE #305 WRAP, BY ADDITION, WORDING ABOVE UNCHANGED — FIRED ON HIS WORD. RECEIPT: sitting call 1 is `s305-D2`; K cut v1.0.14 as X `0ef30746`, Y1 `02d679b3` (the zip under `apollo-spider/dist/`) and Y2 `d3b809a7` (frozen at `444c58d22a68`), `" + R['K'] + "`; CI's release job green from run `36347602064` on." + TAIL),
]
segs = old.split('·')
for key, why in STRIKES:
    assert '·' not in why, why[:60]
    hits = [i for i, s in enumerate(segs) if s.strip().startswith(key)]
    assert len(hits) == 1, (key[:60], hits)
    segs[hits[0]] = segs[hits[0]].rstrip() + ' ⛔ **' + why + '** '
old = '·'.join(segs)
NEW = [
 "⬛ **① THE 102 PARKED QUESTIONS, HIS KEEP-OPEN TICKS** [NEW — 0, DAVE'S] — sitting call 32 (`s305-D32`) parked the 102 with tripwires AND asked for a page to scan; B4 built it (`" + SCAN + "`, `" + R['B4'] + "`), grouped by theme, oldest first, one \"Keep open\" tick per row, published in the artifact. His ticks have not come back. Put to him at the #305 wrap: which of the 102 does he want kept open (rows `W-305n5`, `W-305b4`)",
 "⬛ **② TWO OLD RULINGS STAMPED \"NOT BUILT\" WHOSE RECORDS LOOK BUILT — RE-SORT `s212-D1` AND `s256-D1`?** [NEW — 0, DAVE'S] — A2 stamped six rulings `ruled — NOT BUILT` on the kind-5 \"settled\" verdict (`" + R['A2'] + "`); two of them carry their own build evidence: `s212-D1` says its pairing is implemented at canon.css :351 and :648, DISCHARGED, and `s256-D1` names commits `1f4c355` and `3c8832a`. Put to him at the #305 wrap",
 "⬛ **③ THE RING — \"SET TO FILL\", AGAINST THE DONUT META'S \"DOES NOT STRETCH\"** [NEW — 0, DAVE'S] — `s305-D59` (his loose-ends words: *\"The chart pattern should be set to fill but its container should constrain it by being smaller of having more than one element in it\"*) amends `s305-D9`, keeps the half-width column, and leaves open how fill squares with ds-030 and with his call-8 \"not responsive, but not fixed\"; the ring is still drawn at its own diameter (B6 `" + R['B6'] + "`). On row `W-305n2`. Put to him at the #305 wrap",
 "⬛ **④ FIVE NEW THREADS FROM THE LOOSE ENDS, `W-305e1` TO `W-305e5`** [NEW — 0, DAVE'S] — the list's when-rule, worked on its own; the top-nav rule as an IA question (top nav, mega menu, what hands over to what); the page-title lock-up; a header part for bento groups; whether two closely linked subjects (exposure and resilience) may be one bento group. His \"Change\" answers, `" + EXPORT2 + "`. Each wants a page or a tripwire",
 "⬛ **⑤ TWO NEW TOKEN NAMES — `surface/section` AND `notification/contextual/border/alpha` — ACCEPT OR RENAME?** [NEW — 0, DAVE'S] — minted by B1 for calls 9 and 26 (`" + R['B1'] + "`); names are his under `s145-D1`. Row `W-305b1`",
 "⬛ **⑥ THE RAILS HALF OF CALL 9 IS HELD** [NEW — 0, DAVE'S] — `s305-D10` stays `ruled`: the rails generator's `theme_tokens()` picks the wrong supercharge block (drift since #288), and no rails word binds `surface/section` (W2 `" + R['W2'] + "`). Two questions for him: the ramp word and its scope. Row `W-305w2`",
 "⬛ **⑦ THE LOGOS FOUNDATION PAGE IN THE v1.0.14 PACK SHOWS FOUR BROKEN IMAGES** [NEW — 0] — `showroom/_foundations/logos.html` still points at the #282 masterbrand identifier files; v1.0.13 did not break (V2 `" + R['V2'] + "`). Rides the next cut. Row `W-305v2`",
 "⬛ **⑧ THE LAUNCHPAD PoC — OCTOBER, AFTER CALLS 14 TO 19 BUILD, AND A SURPRISE** [NEW — 0, DAVE'S] — `s305-D45` to `s305-D54`; route B; name Launchpad under an Apollo eyebrow; his Friday words *\"" + QSURPRISE + "\"* (`W-305n6`); the four setting-or-slot names (`s305-D58`) build with the other 23 then (B6 held them: no form to copy). V2 found the v1.0.14 pack ships the whole ruling store, Launchpad rulings included; his 18:16 BST answer, *\"" + Q1816 + "\"* — the `s279-D1` / `W-305n6` collision stays unruled on `W-305v2`",
 "⚠ **⑨ REVIEW PAGES: PICTURES INLINED AS DATA URIs AND OPENED IN THE PAGE, NEVER A `target=_blank` LINK TO A FILE** [NEW — 0] — his words Monday, *\"" + Q0711 + "\"* (07:11 BST) and *\"" + Q0715 + "\"* (07:15), screenshot lines *\"" + QSHOT.replace(" · ", "\" / \"") + "\"*: a link out of the artifact opens an outside browser, where claude.ai refuses. Fixed on the loose-ends and call-27 pages (artifact version 7); the #304 pages in the artifact were not checked",
 "⚠ **⑩ THE PUSH TOKEN LIVES IN `.git/apollo-credentials` BEHIND A GET-ONLY HELPER** [NEW — 0] — `s305-D30`, C1 (`" + R['C1'] + "`): the `origin` URL is clean, `_git_commit.sh --push` accepts the helper (H2), and CI read-back scripts must read the token through `notes/_lanes/305/C1/_ghtok.py` (the #304 scripts parse the URL and now run unauthenticated). The token is still plain text on disk; its expiry is 6 November",
 "⚠ **⑪ THE REPO `daveasewen/UX-design` IS PUBLIC** [NEW — 0] — read through the API on Sunday about 17:30 BST; every push publishes, the v1.0.14 zip and the Launchpad rulings included. He approved this session's pushes at 19:45 BST, *\"" + Q1945 + "\"*",
 "⚠ **⑫ `_build_all.py` HAS 154 STEPS** [NEW — 0] — C1 wired B2's two KG-sources rows at `27efb7b6`, so every step from the old 90 up moved +2 (on top of #304's +4 from 86 up); older notes quoting those steps read low (`" + R['C1'] + "`)",
 "⚠ **⑬ THE REGROWTH CHECK ARMS ITSELF WHEN THE 75 PINNED ROWS REACH 0 LIVE** [NEW — 0] — `s305-D40`, H2 (`" + R['H2'] + "`): 57 of 75 live at the #305 wrap; once armed it is blocking for every row it names, including `W-304a1` to `W-304a4` (and `W-303h`, closed at this wrap), so the batch that closes the last of the 75 must close or restate those too",
 "⚠ **⑭ THE CONDUCTOR'S WINDOW RAN 150,794 PAST THE 300K HARD LINE** [NEW — 0] — a hand sum at the #305 wrap seat over `" + TRANSCRIPT + "`: boot 131,040, over 160,000 at 13:26 BST Sunday, 200,000 at 14:54, 256,000 at 16:26, 300,000 at 18:31 Sunday, and 450,794 at the message that launched the wrap seat (Monday 10:09 BST). The work was delegated to 21 seats; named, not graded",
 "⬛ **⑮ THE RAISED BOOT CEILING IS ALREADY BREACHED — 130,000 AGAINST #304's 131,130** [NEW — 0, DAVE'S] — `s305-D29` moved `BOOT_CEILING_TK` from 72,768 to 130,000 (H2 `" + R['H2'] + "`), and the wrap gate at the #305 wrap's open read no boot-ceiling fail; once step 2f rolled #304's stratum into `notes/_GAUGE-LOG.md` the arm read *\"1 post-diet reading(s) EXCEED it — #304 131,130\"* (`notes/_lanes/305/W/_gate-prewrap.log`), and #305's own boot, 131,040, joins at the next roll. So the #305 wrap commit took the declared not-a-wrap path again. The gate forbids raising the literal as a wrap's remedy; cut the boot, move the ceiling again, or keep the declared path — his word. Put to him at the #305 wrap",
]
for n in NEW:
    assert '·' not in n, n[:60]
line = '> **residual → #306:** ' + ' · '.join(NEW) + ' ·  ' + old.strip()
L[i305:i305] = ['## residual → #306', '', line, '']
open(P, 'w', encoding='utf-8').write('\n'.join(L))
chk = open(P, encoding='utf-8').read().split('\n')
l306 = next(l for l in chk if l.startswith('> **residual → #306:**'))
items = cg._carry_items(l306)
l305 = next(l for l in chk if l.startswith('> **residual → #305:**'))
print('items', len(items), 'prev', len(cg._carry_items(l305)), 'struck-this-wrap', l306.count('AT THE #305 WRAP, BY ADDITION'), 'new', len(NEW))
open('notes/_lanes/305/W/_work/carries_count.txt', 'w').write(str(len(items)) + '\n')
