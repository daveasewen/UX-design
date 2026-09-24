# #302 wrap seat - the ONE _gm_move.py transaction for 2c / 2d / 2f and the new banner, delta,
# stamp and stratum. Unique, session-owned ops file, asserted to exist. Modelled on #301's build_ops_301W.py.
import json, os, sys
sys.path.insert(0, 'notes/_lanes/302/W/_work')
from names_302 import *
gm = open('GOOD-MORNING.md', encoding='utf-8').read().split('\n')
ls = open('_LIVE-STATE.md', encoding='utf-8').read().split('\n')
ops = []
t_old = [l for l in gm if l.startswith('> **TITLE THE NEXT CHAT →**')]
assert len(t_old) == 1
ops.append({"op": "replace", "file": "GOOD-MORNING.md", "find": t_old, "replace": ["> **TITLE THE NEXT CHAT →** `" + NEXT_TITLE + "`"]})
PROBE = "PYTHONPATH=knowledge python3 -c \"import _capture_gate as c;print(len(c._carry_items([l for l in open('_CARRIES.md') if '#303:**' in l][0])))\""
NC = int(open('notes/_lanes/302/W/_work/carries_count.txt').read().split()[0])
PREV = 697
B = [
 "> ## ★ LATEST — 2026-09-24 (Thu **#302**, Opus 5.5 conductor in the CLOUD, **1 Opus sub**, DELEGATED wrap on Opus 5.5 — ★★ **" + HEADLINE + "**)",
 ">",
 "> - ★★★ ① **THE ASK WENT TO HIS COLLEAGUES; THE DEMO PROMPT IS NEXT.** *\"" + Q0743 + "\"* · *\"" + Q0743b + "\"* (07:43). At 12:42 *\"" + Q1242 + "\"* — no room at 285,325, so it is #303's first beat. **Friday is 2026-09-25 — tomorrow.** The ask (now 16) stays DRAFT. **`_rulings.json` STAYS 638.**",
 "> - ★★ ② **THE DECK IS 17 SLIDES — HIS ACTS, `7f10b5b8`:** 11–13 copy on his words; **Scrutiny** 03 before Judgement 04 on 12; the callipers turned over and floating (*\"this is perfect.\"*); **new 15, \"Benefits beyond speed, quality and consistency\"** — Customisation · Convergence · Cost-effectiveness, Light, **$3.2m bold red** (`" + REPA + "`, `" + REPB + "`).",
 "> - ⚠ ③ **THE SEAT RENDERS ON A FALLBACK FACE** — \"Univers Next\" does not resolve there; `HSBC_MtUnivers_Latin` does, and the font stack never names it. His to add. **FILL 285,325 at 12:42 (hand sum), over the 256K working line, under 300K.** The wrap gate is RED on the boot ceiling: DECLARED not-a-wrap path again. **`" + HO + "` OUTRANKS `_CHAIN.md`.**",
 "> **residual → #303:** ⬛ **THE DEMO PROMPT, THE DAY BEFORE FRIDAY** [1, DAVE'S] — put it at the opener. `s225-D2`. **" + format(NC, ',') + " items, 6 new, 1 STRUCK IN PART (the ask, to his colleagues)**, `_CARRIES.md` § `residual → #303` `carries:residual-303`. PROBE `" + PROBE + "` = " + str(NC) + ". The 6 new are counted by it: " + str(PREV) + "→" + str(NC) + ".",
 "",
]
ops.append({"op": "insert", "file": "GOOD-MORNING.md", "at": "> ## ★ LATEST — 2026-09-23 (Wed **#301**", "where": "before", "lines": B})
old301 = [l for l in gm if l.startswith('> ## ★ LATEST — 2026-09-23 (Wed **#301**')]
assert len(old301) == 1
ops.append({"op": "replace", "file": "GOOD-MORNING.md", "find": old301, "replace": [old301[0].replace('> ## ★ LATEST —', '> ## ★ PRIOR —', 1)]})
ops.append({"op": "insert", "file": "_GM-ARCHIVE.md", "at": "## Batch 2026-09-23 #301", "where": "before", "lines": [
 "## Batch 2026-09-24 #302", "",
 "*Rolled at the #302 wrap (2c). The #300 ★ PRIOR banner, moved VERBATIM by `_gm_move.py` — a move, never a rewrite. Its durable content already lives in `_DECISION-HISTORY/`, `notes/_subreports/`, the ledgers and git, and every ⬛/⚠ item on it is carried in `_CARRIES.md` (§ `residual → #301` onward, now § `residual → #303`) at its true age; this archive is a convenience copy, never a tattoo.*", ""]})
ops.append({"op": "move", "src": "GOOD-MORNING.md", "start": "> ## ★ PRIOR — 2026-09-23 (Wed **#300**", "end": "## ⬛ DO THIS FIRST",
            "dst": "_GM-ARCHIVE.md", "at": "## Batch 2026-09-24 #302", "where": "after"})
ops.append({"op": "roll_2f", "session": 301, "pm_start": "#### 2026-09-23 #301", "pm_end": "> **COMMIT STATE #301:**",
            "cs_start": "> **COMMIT STATE #301:**", "cs_end": "#### 2026-08-05 #96"})
S = open('notes/_lanes/302/W/_work/stratum_302.txt', encoding='utf-8').read().rstrip('\n').split('\n')
ops.append({"op": "insert", "file": "GOOD-MORNING.md", "at": "#### 2026-08-05 #96", "where": "before", "lines": S + [""]})
ops.append({"op": "insert", "file": "_LIVE-STATE.md", "at": "*Last refreshed: 2026-09-23 (Wed from `date` — **#301 wrap**", "where": "after", "lines": [
 "*Last refreshed: 2026-09-24 (Thu from `date` — **#302 wrap**. ✅ **ONE DAY, NO DATE SPLIT: the session, lane A, the conductor's commit `7f10b5b8` and this ritual are all Thursday 2026-09-24** — `date` at this seat read `Thu Sep 24 11:43:51 UTC 2026` (12:43 BST). ⛔★★★ **READ `" + HO + "` FIRST — IT IS NEWER THAN `_CHAIN.md` AND OUTRANKS IT.** ★★ **THE SESSION IS ONE SENTENCE: THE ASK WENT TO HIS COLLEAGUES, THE DECK GREW TO 17 SLIDES ON HIS WORDS — A SCRUTINY PLATE, THE CALLIPERS TURNED OVER AND A NEW BENEFITS SLIDE — AND THE DEMO PROMPT WAITS FOR #303, THE DAY BEFORE FRIDAY.** Nothing inscribed. The full record is in the ⏱ LATEST DELTA below, its sole home under `s241-D2`.)*"]})
D = open('notes/_lanes/302/W/_work/delta_302.txt', encoding='utf-8').read().rstrip('\n').split('\n')
ops.append({"op": "insert", "file": "_LIVE-STATE.md", "at": "## ⏱ LATEST DELTA — 2026-09-23 (Wed from `date`) (**#301**", "where": "before", "lines": D + [""]})
d301 = [l for l in ls if l.startswith('## ⏱ LATEST DELTA — 2026-09-23 (Wed from `date`) (**#301**')]
assert len(d301) == 1
ops.append({"op": "replace", "file": "_LIVE-STATE.md", "find": d301, "replace": [d301[0].replace('## ⏱ LATEST DELTA', '## ⏱ PRIOR DELTA', 1)]})
ops.append({"op": "insert", "file": "_LIVE-STATE-ARCHIVE.md", "at": "## Rolled 2026-09-23 #301", "where": "before", "lines": [
 "## Rolled 2026-09-24 #302 (2d, at the #302 wrap) — via the mover", "",
 "*The #299 ⏱ delta block, moved VERBATIM by `_gm_move.py`. ⚠ No `Previous:` chain segment moved with it: none is left in `_LIVE-STATE.md`'s stamp lines; the #293–#301 stamps stand as separate lines and were not rolled — declared in the #302 stratum.*", ""]})
ops.append({"op": "move", "src": "_LIVE-STATE.md", "start": "## ⏱ PRIOR DELTA — 2026-09-23 (Wed from `date`) (**#299**", "end": "## 🕓 OPEN — Latin Univers",
            "dst": "_LIVE-STATE-ARCHIVE.md", "at": "## Rolled 2026-09-23 #301", "where": "before"})
out = 'notes/_lanes/302/W/_ops-302W-main.json'
json.dump(ops, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
assert os.path.exists(out) and os.path.getsize(out) > 10000, os.path.getsize(out)
print('ops', len(ops), 'bytes', os.path.getsize(out))
