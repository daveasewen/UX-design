# #303 wrap seat - the ONE _gm_move.py transaction for 2c / 2d / 2f and the new banner, delta, stamp,
# header date-split line and stratum. Unique, session-owned ops file, asserted to exist. Modelled on #302's build_ops_302W.py.
import json, os, sys
sys.path.insert(0, 'notes/_lanes/303/W/_work')
from names_303 import *
gm = open('GOOD-MORNING.md', encoding='utf-8').read().split('\n')
ls = open('_LIVE-STATE.md', encoding='utf-8').read().split('\n')
ops = []
t_old = [l for l in gm if l.startswith('> **TITLE THE NEXT CHAT →**')]
assert len(t_old) == 1
ops.append({"op": "replace", "file": "GOOD-MORNING.md", "find": t_old, "replace": ["> **TITLE THE NEXT CHAT →** `" + NEXT_TITLE + "`"]})
SPLIT7 = '> ⚠ **WRAP DATE SPLIT, SEVENTH OCCURRENCE ON THIS RUN'
assert sum(1 for l in gm if l.startswith(SPLIT7)) == 1
ops.append({"op": "insert", "file": "GOOD-MORNING.md", "at": SPLIT7, "where": "after", "lines": [
 "> ⚠ **WRAP DATE SPLIT, EIGHTH OCCURRENCE ON THIS RUN — SESSION OPENED THURSDAY 2026-09-24, RESUMED FRIDAY 2026-09-25 AND SATURDAY 2026-09-26; RITUAL + WRAP COMMIT 2026-09-26.** #303 opened at 13:48 BST on 09-24 and both of its commits carry that date (`" + SHA1 + "` · `" + SHA2 + "`); one question on Friday, the Apollo-MCP ask and lanes G1/G2 on Saturday, and this ritual are 09-26. ⛔ **Nothing re-dated** — `s294-D11`'s shape: the session date on keys, the dossier, lane P's report and the stratum (`2026-09-24-303-*`), the ritual date on this one line so the gate's `is not today` check grades a true statement; G1, G2 and the wrap report carry 2026-09-26, the day they were written."]})
PROBE = "PYTHONPATH=knowledge python3 -c \"import _capture_gate as c;print(len(c._carry_items([l for l in open('_CARRIES.md') if '#304:**' in l][0])))\""
NC = int(open('notes/_lanes/303/W/_work/carries_count.txt').read().split()[0])
PREV = 703
B = [
 "> ## ★ LATEST — 2026-09-26 (Sat **#303**, DATE SPLIT from Thu 09-24, Opus 5.5 conductor in the CLOUD, **3 Opus subs**, DELEGATED wrap on Opus 5.5 — ★★ **" + HEADLINE + "**)",
 ">",
 "> - ★★★ ① **APOLLO-MCP WAS ASKED FOR; THE PAGE IS #304'S FIRST BEAT.** Sat 13:29 *\"Can I have this as a page, do you think we could create our own MCP-UI -- Apollo-MCP maybe\"*. G1 (`" + REPG1 + "`) and G2 (`" + REPG2 + "`) filed; **the page was not written** (window 392,986). Headline: an A2UI catalogue over MCP, MCP Apps as fallback, no new protocol. **`_rulings.json` STAYS 638.**",
 "> - ★★ ② **THE DECK WAS FINISHED FOR FRIDAY — 16 SLIDES, HIS ACTS, `" + SHA1 + "` + `" + SHA2 + "`:** the demo prompt restructured on his words, Common, *\"" + Q1551 + "\"*; 13's title ditched; 14 a 3x2 grid; 15 his own copy, the ask parked; 16 the press loop (`" + REPP + "`); explorer v1.27. Friday's outcome is not in the record.",
 "> - ⚠ ③ **FILL 402,607 at the wrap (hand sum), over the 300K hard line since Thu 18:01.** The font stack still does not name `HSBC_MtUnivers_Latin`. The wrap gate is RED on the boot ceiling: DECLARED not-a-wrap path again. **`" + HO + "` OUTRANKS `_CHAIN.md`.**",
 "> **residual → #304:** ⬛ **THE APOLLO-MCP PROPOSAL PAGE** [1, DAVE'S] — write it first. `s225-D2`. **" + format(NC, ',') + " items, 6 new, 6 STRUCK (5 by his acts, 1 further in part)**, `_CARRIES.md` § `residual → #304` `carries:residual-304`. PROBE `" + PROBE + "` = " + str(NC) + ". The 6 new are counted by it: " + str(PREV) + "→" + str(NC) + ".",
 "",
]
ops.append({"op": "insert", "file": "GOOD-MORNING.md", "at": "> ## ★ LATEST — 2026-09-24 (Thu **#302**", "where": "before", "lines": B})
old302 = [l for l in gm if l.startswith('> ## ★ LATEST — 2026-09-24 (Thu **#302**')]
assert len(old302) == 1
ops.append({"op": "replace", "file": "GOOD-MORNING.md", "find": old302, "replace": [old302[0].replace('> ## ★ LATEST —', '> ## ★ PRIOR —', 1)]})
ops.append({"op": "insert", "file": "_GM-ARCHIVE.md", "at": "## Batch 2026-09-24 #302", "where": "before", "lines": [
 "## Batch 2026-09-24 #303", "",
 "*Rolled at the #303 wrap (2c, ritual 2026-09-26). The #301 ★ PRIOR banner, moved VERBATIM by `_gm_move.py` — a move, never a rewrite. Its durable content already lives in `_DECISION-HISTORY/`, `notes/_subreports/`, the ledgers and git, and every ⬛/⚠ item on it is carried in `_CARRIES.md` (§ `residual → #302` onward, now § `residual → #304`) at its true age; this archive is a convenience copy, never a tattoo.*", ""]})
ops.append({"op": "move", "src": "GOOD-MORNING.md", "start": "> ## ★ PRIOR — 2026-09-23 (Wed **#301**", "end": "## ⬛ DO THIS FIRST",
            "dst": "_GM-ARCHIVE.md", "at": "## Batch 2026-09-24 #303", "where": "after"})
ops.append({"op": "roll_2f", "session": 302, "pm_start": "#### 2026-09-24 #302", "pm_end": "> **COMMIT STATE #302:**",
            "cs_start": "> **COMMIT STATE #302:**", "cs_end": "#### 2026-08-05 #96"})
S = open('notes/_lanes/303/W/_work/stratum_303.txt', encoding='utf-8').read().rstrip('\n').split('\n')
ops.append({"op": "insert", "file": "GOOD-MORNING.md", "at": "#### 2026-08-05 #96", "where": "before", "lines": S + [""]})
ops.append({"op": "insert", "file": "_LIVE-STATE.md", "at": "*Last refreshed: 2026-09-24 (Thu from `date` — **#302 wrap**", "where": "after", "lines": [
 "*Last refreshed: 2026-09-26 (Sat from `date` — **#303 wrap**. ⛔★★ **DATE SPLIT, THE EIGHTH ON THIS RUN AND `s294-D11`'s SHAPE: #303 opened Thursday 2026-09-24 at 13:48 BST and both of its commits carry that date (`" + SHA1 + "` · `" + SHA2 + "`); one question on Friday 2026-09-25, the Apollo-MCP ask, lanes G1 and G2, and this ritual are Saturday 2026-09-26** — `date` at this seat read `Sat Sep 26 12:50:50 UTC 2026` (13:50 BST). ⛔★★★ **READ `" + HO + "` FIRST — IT IS NEWER THAN `_CHAIN.md` AND OUTRANKS IT.** ★★ **THE SESSION IS ONE SENTENCE: THE DECK WAS FINISHED FOR FRIDAY ON HIS WORDS — THE PROMPT, THE COPY, THE PRESS LOOP — AND ON SATURDAY HE ASKED FOR AN APOLLO-MCP PROPOSAL, WHOSE PAGE IS #304'S FIRST BEAT.** Nothing inscribed. The full record is in the ⏱ LATEST DELTA below, its sole home under `s241-D2`.)*"]})
D = open('notes/_lanes/303/W/_work/delta_303.txt', encoding='utf-8').read().rstrip('\n').split('\n')
ops.append({"op": "insert", "file": "_LIVE-STATE.md", "at": "## ⏱ LATEST DELTA — 2026-09-24 (Thu from `date`) (**#302**", "where": "before", "lines": D + [""]})
d302 = [l for l in ls if l.startswith('## ⏱ LATEST DELTA — 2026-09-24 (Thu from `date`) (**#302**')]
assert len(d302) == 1
ops.append({"op": "replace", "file": "_LIVE-STATE.md", "find": d302, "replace": [d302[0].replace('## ⏱ LATEST DELTA', '## ⏱ PRIOR DELTA', 1)]})
ops.append({"op": "insert", "file": "_LIVE-STATE-ARCHIVE.md", "at": "## Rolled 2026-09-24 #302", "where": "before", "lines": [
 "## Rolled 2026-09-24 #303 (2d, at the #303 wrap, ritual 2026-09-26) — via the mover", "",
 "*The #300 ⏱ delta block, moved VERBATIM by `_gm_move.py`. ⚠ No `Previous:` chain segment moved with it: none is left in `_LIVE-STATE.md`'s stamp lines; the #293–#302 stamps stand as separate lines and were not rolled — declared in the #303 stratum.*", ""]})
ops.append({"op": "move", "src": "_LIVE-STATE.md", "start": "## ⏱ PRIOR DELTA — 2026-09-23 (Wed from `date`) (**#300**", "end": "## 🕓 OPEN — Latin Univers",
            "dst": "_LIVE-STATE-ARCHIVE.md", "at": "## Rolled 2026-09-24 #302", "where": "before"})
out = 'notes/_lanes/303/W/_ops-303W-main.json'
json.dump(ops, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
assert os.path.exists(out) and os.path.getsize(out) > 10000, os.path.getsize(out)
print('ops', len(ops), 'bytes', os.path.getsize(out))
