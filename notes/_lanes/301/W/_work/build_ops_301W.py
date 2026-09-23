# #301 wrap seat - the ONE _gm_move.py transaction for 2c / 2d / 2f and the new banner, delta,
# stamp and stratum. Unique, session-owned ops file, asserted to exist. Modelled on #300's.
import json, os, sys
sys.path.insert(0, 'notes/_lanes/301/W/_work')
from names_301 import *
gm = open('GOOD-MORNING.md', encoding='utf-8').read().split('\n')
ls = open('_LIVE-STATE.md', encoding='utf-8').read().split('\n')
ops = []
t_old = [l for l in gm if l.startswith('> **TITLE THE NEXT CHAT →**')]
assert len(t_old) == 1
ops.append({"op": "replace", "file": "GOOD-MORNING.md", "find": t_old, "replace": ["> **TITLE THE NEXT CHAT →** `" + NEXT_TITLE + "`"]})
PROBE = "PYTHONPATH=knowledge python3 -c \"import _capture_gate as c;print(len(c._carry_items([l for l in open('_CARRIES.md') if '#302:**' in l][0])))\""
B = [
 "> ## ★ LATEST — 2026-09-23 (Wed **#301**, Opus 5.5 conductor in the CLOUD, **1 Opus sub**, DELEGATED wrap on Opus 5.5 — ★★ **" + HEADLINE + "**)",
 ">",
 "> - ★★★ ① **THE WINDOW LINES MOVED ON HIS WORD — HIS ACTS, NOT INSCRIBED.** *\"Lets try 300k and cross our fingers\"* (19:45) · *\"1. is right, might be a good experiment.\"* (19:47) · *\"200k isnt enough make it 256\"* (20:21): lane G set hard **300,000** and working **256,000**, PICKED Dave #301 (`" + REPG + "`); amber and `BOOT_CEILING_TK` 72,768 unchanged. **`_rulings.json` STAYS 638.** Stop 180,000 and tolerance 220,000 now sit under the working line — put to him, unanswered.",
 "> - ★★ ② **HIS 19:26 ANSWERS CLOSED FOUR POLISH ITEMS** — the ask on 02's index, the 07/08 headlines, the −27 angles, and Judgment → **Judgement** on 12 (source edited, deck rebuilt, not rendered). The demo brief is *\"tomorrow\"*; the 26 suggestions surfaced, none picked. **FOUR STRUCK, TWO HEADLINES STRUCK.**",
 "> - ⚙ ③ **THE NEW OPENER, MEASURED (hand sum):** boot 126,767 · 163,380 at the first reply · **187,604 after his first message, NO memory re-send** (#300: 211,454) — but the conductor's own reasoning stays in the window. **244,884 at the wrap.** The wrap gate is RED on the boot ceiling, so the DECLARED not-a-wrap path again. **`" + HO + "` OUTRANKS `_CHAIN.md`.**",
 "> **residual → #302:** ⬛ **THE ASK ON SLIDE 15 AND THE DEMO BRIEF** [2, DAVE'S] — ask at the opener. `s225-D2`. **697 items, 6 new, 4 STRUCK AND 2 HEADLINES STRUCK**, `_CARRIES.md` § `residual → #302` `carries:residual-302`. PROBE `" + PROBE + "` = 697. ⚠ **6 new INVISIBLE to it**; 692→697.",
 "",
]
ops.append({"op": "insert", "file": "GOOD-MORNING.md", "at": "> ## ★ LATEST — 2026-09-23 (Wed **#300**", "where": "before", "lines": B})
old300 = [l for l in gm if l.startswith('> ## ★ LATEST — 2026-09-23 (Wed **#300**')]
assert len(old300) == 1
ops.append({"op": "replace", "file": "GOOD-MORNING.md", "find": old300, "replace": [old300[0].replace('> ## ★ LATEST —', '> ## ★ PRIOR —', 1)]})
ops.append({"op": "insert", "file": "_GM-ARCHIVE.md", "at": "## Batch 2026-09-23 #300", "where": "before", "lines": [
 "## Batch 2026-09-23 #301", "",
 "*Rolled at the #301 wrap (2c). The #299 ★ PRIOR banner, moved VERBATIM by `_gm_move.py` — a move, never a rewrite. Its durable content already lives in `_DECISION-HISTORY/`, `notes/_subreports/`, the ledgers and git, and every ⬛/⚠ item on it is carried in `_CARRIES.md` (§ `residual → #300` onward, now § `residual → #302`) at its true age; this archive is a convenience copy, never a tattoo.*", ""]})
ops.append({"op": "move", "src": "GOOD-MORNING.md", "start": "> ## ★ PRIOR — 2026-09-23 (Wed **#299**", "end": "## ⬛ DO THIS FIRST",
            "dst": "_GM-ARCHIVE.md", "at": "## Batch 2026-09-23 #301", "where": "after"})
ops.append({"op": "roll_2f", "session": 300, "pm_start": "#### 2026-09-23 #300", "pm_end": "> **COMMIT STATE #300:**",
            "cs_start": "> **COMMIT STATE #300:**", "cs_end": "#### 2026-08-05 #96"})
S = open('notes/_lanes/301/W/_work/stratum_301.txt', encoding='utf-8').read().rstrip('\n').split('\n')
ops.append({"op": "insert", "file": "GOOD-MORNING.md", "at": "#### 2026-08-05 #96", "where": "before", "lines": S + [""]})
ops.append({"op": "insert", "file": "_LIVE-STATE.md", "at": "*Last refreshed: 2026-09-23 (Wed from `date` — **#300 wrap**", "where": "after", "lines": [
 "*Last refreshed: 2026-09-23 (Wed from `date` — **#301 wrap**. ✅ **ONE DAY, NO DATE SPLIT: the session, lane G and this ritual are all Wednesday 2026-09-23** — `date` at this seat read `Wed Sep 23 19:59:36 UTC 2026` (20:59 BST). ⛔★★★ **READ `" + HO + "` FIRST — IT IS NEWER THAN `_CHAIN.md` AND OUTRANKS IT.** ★★ **THE SESSION IS ONE SENTENCE: THE FIRST CHAT UNDER HIS PASTED INSTRUCTIONS MEASURED NO MEMORY RE-SEND, HIS 19:26 ANSWERS CLOSED FOUR POLISH ITEMS, AND ON HIS WORD THE WINDOW'S LINES MOVED TO 256K WORKING AND 300K HARD — HIS ACTS, NOT INSCRIBED.** ⬛ The ask on 15 is still a draft and Friday is 2026-09-25; the demo brief is \"tomorrow\". The full record is in the ⏱ LATEST DELTA below, its sole home under `s241-D2`.)*"]})
D = open('notes/_lanes/301/W/_work/delta_301.txt', encoding='utf-8').read().rstrip('\n').split('\n')
ops.append({"op": "insert", "file": "_LIVE-STATE.md", "at": "## ⏱ LATEST DELTA — 2026-09-23 (Wed from `date`) (**#300**", "where": "before", "lines": D + [""]})
d300 = [l for l in ls if l.startswith('## ⏱ LATEST DELTA — 2026-09-23 (Wed from `date`) (**#300**')]
assert len(d300) == 1
ops.append({"op": "replace", "file": "_LIVE-STATE.md", "find": d300, "replace": [d300[0].replace('## ⏱ LATEST DELTA', '## ⏱ PRIOR DELTA', 1)]})
ops.append({"op": "insert", "file": "_LIVE-STATE-ARCHIVE.md", "at": "## Rolled 2026-09-23 #300", "where": "before", "lines": [
 "## Rolled 2026-09-23 #301 (2d, at the #301 wrap) — via the mover", "",
 "*The #298 ⏱ delta block, moved VERBATIM by `_gm_move.py`. ⚠ No `Previous:` chain segment moved with it: none is left in `_LIVE-STATE.md`'s stamp lines; the #293–#300 stamps stand as separate lines and were not rolled — declared in the #301 stratum.*", ""]})
ops.append({"op": "move", "src": "_LIVE-STATE.md", "start": "## ⏱ PRIOR DELTA — 2026-09-23 (Wed from `date`) (**#298**", "end": "## 🕓 OPEN — Latin Univers",
            "dst": "_LIVE-STATE-ARCHIVE.md", "at": "## Rolled 2026-09-23 #300", "where": "before"})
out = 'notes/_lanes/301/W/_ops-301W-main.json'
json.dump(ops, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
assert os.path.exists(out) and os.path.getsize(out) > 10000, os.path.getsize(out)
print('ops', len(ops), 'bytes', os.path.getsize(out))
