# #300 wrap seat - the ONE _gm_move.py transaction for 2c / 2d / 2f and the new banner, delta,
# stamp and stratum. Unique, session-owned ops file, asserted to exist. Modelled on #299's.
import json, os, sys
sys.path.insert(0, 'notes/_lanes/300/W/_work')
from names_300 import *
gm = open('GOOD-MORNING.md', encoding='utf-8').read().split('\n')
ls = open('_LIVE-STATE.md', encoding='utf-8').read().split('\n')
ops = []
t_old = [l for l in gm if l.startswith('> **TITLE THE NEXT CHAT →**')]
assert len(t_old) == 1
ops.append({"op": "replace", "file": "GOOD-MORNING.md", "find": t_old, "replace": ["> **TITLE THE NEXT CHAT →** `" + NEXT_TITLE + "`"]})
PROBE = "PYTHONPATH=knowledge python3 -c \"import _capture_gate as c;print(len(c._carry_items([l for l in open('_CARRIES.md') if '#301:**' in l][0])))\""
B = [
 "> ## ★ LATEST — 2026-09-23 (Wed **#300**, Opus 5.5 conductor in the CLOUD, **8 Opus subs**, DELEGATED wrap on Opus 5.5 — ★★ **" + HEADLINE + "**)",
 ">",
 "> - ★★★ ① **THE BOOT WAS MEASURED.** Cloud boot **126,185** = tools ~65K · Anthropic's prompt ~31.5K · the memory list ~19K; our own opener **81,049**, a 19,371 memory re-send inside it. Lanes **A B C D**, adversary **X**, plan **P** (`" + PLAN + "`). **NOTHING INSCRIBED — `_rulings.json` STAYS 638.**",
 "> - ★★ ② **THE READING STAYS** — X's cold-seat quiz: card alone 4/18, FALSE · card + chain 12/18 · handoff + chain 18/18. A BM25 look-up finds 11/18 against today's 2/18: it complements the reading, never replaces it. ⛔ **HE PASTED THE NEW START — his act, not a ruling:** no memory at the opener or while a chat is live. **ONE HEADLINE STRUCK.**",
 "> - ⚙ ③ **FILL A HAND SUM, 278,666 AT THE WRAP; THE ASK ON 15 WENT UNANSWERED.** The wrap gate is RED on the boot ceiling (only the Mac seat clears it), so the DECLARED not-a-wrap path again. **`" + HO + "` OUTRANKS `_CHAIN.md`.**",
 "> **residual → #301:** ⬛ **THE ASK ON SLIDE 15, THEN POLISH FOR FRIDAY** [1, DAVE'S] — ask at the opener. `s225-D2`. **692 items, 5 new, 1 HEADLINE STRUCK**, `_CARRIES.md` § `residual → #301` `carries:residual-301`. PROBE `" + PROBE + "` = 692. ⚠ **5 new INVISIBLE to it**; 687→692.",
 "",
]
ops.append({"op": "insert", "file": "GOOD-MORNING.md", "at": "> ## ★ LATEST — 2026-09-23 (Wed **#299**", "where": "before", "lines": B})
old299 = [l for l in gm if l.startswith('> ## ★ LATEST — 2026-09-23 (Wed **#299**')]
assert len(old299) == 1
ops.append({"op": "replace", "file": "GOOD-MORNING.md", "find": old299, "replace": [old299[0].replace('> ## ★ LATEST —', '> ## ★ PRIOR —', 1)]})
ops.append({"op": "insert", "file": "_GM-ARCHIVE.md", "at": "## Batch 2026-09-23 #299", "where": "before", "lines": [
 "## Batch 2026-09-23 #300", "",
 "*Rolled at the #300 wrap (2c). The #298 ★ PRIOR banner, moved VERBATIM by `_gm_move.py` — a move, never a rewrite. Its durable content already lives in `_DECISION-HISTORY/`, `notes/_subreports/`, the ledgers and git, and every ⬛/⚠ item on it is carried in `_CARRIES.md` (§ `residual → #299` onward, now § `residual → #301`) at its true age; this archive is a convenience copy, never a tattoo.*", ""]})
ops.append({"op": "move", "src": "GOOD-MORNING.md", "start": "> ## ★ PRIOR — 2026-09-23 (Wed **#298**", "end": "## ⬛ DO THIS FIRST",
            "dst": "_GM-ARCHIVE.md", "at": "## Batch 2026-09-23 #300", "where": "after"})
ops.append({"op": "roll_2f", "session": 299, "pm_start": "#### 2026-09-23 #299", "pm_end": "> **COMMIT STATE #299:**",
            "cs_start": "> **COMMIT STATE #299:**", "cs_end": "#### 2026-08-05 #96"})
S = open('notes/_lanes/300/W/_work/stratum_300.txt', encoding='utf-8').read().rstrip('\n').split('\n')
ops.append({"op": "insert", "file": "GOOD-MORNING.md", "at": "#### 2026-08-05 #96", "where": "before", "lines": S + [""]})
ops.append({"op": "insert", "file": "_LIVE-STATE.md", "at": "*Last refreshed: 2026-09-23 (Wed from `date` — **#299 wrap**", "where": "after", "lines": [
 "*Last refreshed: 2026-09-23 (Wed from `date` — **#300 wrap**. ✅ **ONE DAY, NO DATE SPLIT: the session, all eight delegated Opus subs and this ritual are all Wednesday 2026-09-23** — `date` at this seat read `Wed Sep 23 16:58:14 UTC 2026` (17:58 BST). ⛔★★★ **READ `" + HO + "` FIRST — IT IS NEWER THAN `_CHAIN.md` AND OUTRANKS IT.** ★★ **THE SESSION IS ONE SENTENCE: THE BOOT WAS MEASURED FOUR WAYS AND ATTACKED BY AN ADVERSARY, THE READING AT THE START STAYS, AND BEFORE \"WRAP\" HE PASTED THE PLAN'S NEW START-OF-CHAT INSTRUCTIONS — HIS ACT, NOT A RULING. NOTHING INSCRIBED.** ⬛ The ask on 15 is still a draft and Friday is 2026-09-25. The full record is in the ⏱ LATEST DELTA below, its sole home under `s241-D2`.)*"]})
D = open('notes/_lanes/300/W/_work/delta_300.txt', encoding='utf-8').read().rstrip('\n').split('\n')
ops.append({"op": "insert", "file": "_LIVE-STATE.md", "at": "## ⏱ LATEST DELTA — 2026-09-23 (Wed from `date`) (**#299**", "where": "before", "lines": D + [""]})
d299 = [l for l in ls if l.startswith('## ⏱ LATEST DELTA — 2026-09-23 (Wed from `date`) (**#299**')]
assert len(d299) == 1
ops.append({"op": "replace", "file": "_LIVE-STATE.md", "find": d299, "replace": [d299[0].replace('## ⏱ LATEST DELTA', '## ⏱ PRIOR DELTA', 1)]})
ops.append({"op": "insert", "file": "_LIVE-STATE-ARCHIVE.md", "at": "## Rolled 2026-09-23 #299", "where": "before", "lines": [
 "## Rolled 2026-09-23 #300 (2d, at the #300 wrap) — via the mover", "",
 "*The #297 ⏱ delta block, moved VERBATIM by `_gm_move.py`. ⚠ No `Previous:` chain segment moved with it: none is left in `_LIVE-STATE.md`'s stamp lines; the #293–#299 stamps stand as separate lines and were not rolled — declared in the #300 stratum.*", ""]})
ops.append({"op": "move", "src": "_LIVE-STATE.md", "start": "## ⏱ PRIOR DELTA — 2026-09-23 (Wed from `date`) (**#297**", "end": "## 🕓 OPEN — Latin Univers",
            "dst": "_LIVE-STATE-ARCHIVE.md", "at": "## Rolled 2026-09-23 #299", "where": "before"})
out = 'notes/_lanes/300/W/_ops-300W-main.json'
json.dump(ops, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
assert os.path.exists(out) and os.path.getsize(out) > 10000, os.path.getsize(out)
print('ops', len(ops), 'bytes', os.path.getsize(out))
