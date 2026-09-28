# #305 wrap seat - the ONE _gm_move.py transaction for 2c / 2d / 2f and the new banner, delta, stamp,
# header date-split line and stratum. Unique, session-owned ops file, asserted to exist. Modelled on #304's build_ops_304W.py.
import json, os, sys
sys.path.insert(0, 'notes/_lanes/305/W/_work')
from names_305 import *
gm = open('GOOD-MORNING.md', encoding='utf-8').read().split('\n')
ls = open('_LIVE-STATE.md', encoding='utf-8').read().split('\n')
ops = []
t_old = [l for l in gm if l.startswith('> **TITLE THE NEXT CHAT →**')]
assert len(t_old) == 1
ops.append({"op": "replace", "file": "GOOD-MORNING.md", "find": t_old, "replace": ["> **TITLE THE NEXT CHAT →** `" + NEXT_TITLE + "`"]})
SPLIT9 = '> ⚠ **WRAP DATE SPLIT, NINTH OCCURRENCE ON THIS RUN'
assert sum(1 for l in gm if l.startswith(SPLIT9)) == 1
ops.append({"op": "insert", "file": "GOOD-MORNING.md", "at": SPLIT9, "where": "after", "lines": [
 "> ⚠ **WRAP DATE SPLIT, TENTH OCCURRENCE ON THIS RUN — SESSION OPENED SUNDAY 2026-09-27; LOOSE ENDS, RITUAL + WRAP COMMIT MONDAY 2026-09-28.** #305 opened at 13:25 BST on 09-27; its commits carry both dates (`27efb7b6` to `01fb005a` on 09-27, `f6aeb264` and `cd16f7ec` on 09-28). ⛔ **Nothing re-dated** — `s294-D11`'s shape: the session date on keys, the dossier and the stratum (`2026-09-27-305-*`), the ritual date on this one line so the gate's `is not today` check grades a true statement; reports keep the day their lanes wrote them; `s305-D58`..`D61` carry 2026-09-28, the day he ruled them."]})
PROBE = "PYTHONPATH=knowledge python3 -c \"import _capture_gate as c;print(len(c._carry_items([l for l in open('_CARRIES.md') if '#306:**' in l][0])))\""
NC = int(open('notes/_lanes/305/W/_work/carries_count.txt').read().split()[0])
PREV = 391
B = [
 "> ## ★ LATEST — 2026-09-28 (Mon **#305**, DATE SPLIT from Sun 09-27, Opus 5.5 conductor in the CLOUD, **21 subs**, DELEGATED wrap on Opus 5.5 — ★★ **" + HEADLINE + "**)",
 ">",
 "> - ★★★ ① **HE TOOK THE SITTING — 53 CALLS AND FRIDAY — AND THE LOOSE ENDS ON MONDAY; `_rulings.json` 638 → 699.** `s305-D1`: a yes is inscribe AND build (*\"set in ink\"*). 40 of the 61 built and stamped with receipts; the rest wait on October (Launchpad) or on his eye. Friday: *\"" + QFRI + "\"*",
 "> - ★★ ② **v1.0.14 CUT (`0ef30746` · `02d679b3` · `d3b809a7`) AND CI ALL GREEN, TWICE (`36349147952`, `36393419907`), 154 OF 154 ASKED.** Fourteen commits pushed `" + RANGE + "` to a PUBLIC repo on his 19:45 yes. The token is behind a credential helper; boot ceiling 130,000; window lines 256K / 300K.",
 "> - ⚠ ③ **REVIEW PAGES: PICTURES INLINE, OPENED IN THE PAGE — never `target=_blank` to a file (his 07:11 and 07:15 words).** FILL 450,794 at the wrap (hand sum), over 300K since Sun 18:31. **`" + HO + "` OUTRANKS `_CHAIN.md`.**",
 "> **residual → #306:** ⬛ **THE 102 PARKED QUESTIONS, HIS KEEP-OPEN TICKS** [1, DAVE'S] — put it first. `s225-D2`. **" + format(NC, ",") + " items, 15 new, 12 STRUCK (by his acts and rulings, with receipts)**, `_CARRIES.md` § `residual → #306` `carries:residual-306`. PROBE `" + PROBE + "` = " + str(NC) + ". #304's 10 new are counted by it now: " + str(PREV) + "→" + str(NC) + ".",
 "",
]
ops.append({"op": "insert", "file": "GOOD-MORNING.md", "at": "> ## ★ LATEST — 2026-09-27 (Sun **#304**", "where": "before", "lines": B})
old304 = [l for l in gm if l.startswith('> ## ★ LATEST — 2026-09-27 (Sun **#304**')]
assert len(old304) == 1
ops.append({"op": "replace", "file": "GOOD-MORNING.md", "find": old304, "replace": [old304[0].replace('> ## ★ LATEST —', '> ## ★ PRIOR —', 1)]})
ops.append({"op": "insert", "file": "_GM-ARCHIVE.md", "at": "## Batch 2026-09-26 #304", "where": "before", "lines": [
 "## Batch 2026-09-27 #305", "",
 "*Rolled at the #305 wrap (2c, ritual 2026-09-28). The #303 ★ PRIOR banner, moved VERBATIM by `_gm_move.py` — a move, never a rewrite. Its durable content already lives in `_DECISION-HISTORY/`, `notes/_subreports/`, the ledgers and git, and every ⬛/⚠ item on it is carried in `_CARRIES.md` (§ `residual → #304` onward, now § `residual → #306`) at its true age; this archive is a convenience copy, never a tattoo.*", ""]})
ops.append({"op": "move", "src": "GOOD-MORNING.md", "start": "> ## ★ PRIOR — 2026-09-26 (Sat **#303**", "end": "## ⬛ DO THIS FIRST",
            "dst": "_GM-ARCHIVE.md", "at": "## Batch 2026-09-27 #305", "where": "after"})
ops.append({"op": "roll_2f", "session": 304, "pm_start": "#### 2026-09-26 #304", "pm_end": "> **COMMIT STATE #304:**",
            "cs_start": "> **COMMIT STATE #304:**", "cs_end": "#### 2026-08-05 #96"})
S = open('notes/_lanes/305/W/_work/stratum_305.txt', encoding='utf-8').read().rstrip('\n').split('\n')
ops.append({"op": "insert", "file": "GOOD-MORNING.md", "at": "#### 2026-08-05 #96", "where": "before", "lines": S + [""]})
ops.append({"op": "insert", "file": "_LIVE-STATE.md", "at": "*Last refreshed: 2026-09-27 (Sun from `date` — **#304 wrap**", "where": "after", "lines": [
 "*Last refreshed: 2026-09-28 (Mon from `date` — **#305 wrap**. ⛔★★ **DATE SPLIT, THE TENTH ON THIS RUN AND `s294-D11`'s SHAPE: #305 opened Sunday 2026-09-27 at 13:25 BST; the sitting and the cut were Sunday, the loose ends and this ritual Monday 2026-09-28** — `date` at this seat read `Mon Sep 28 09:10:17 UTC 2026` (10:10 BST). ⛔★★★ **READ `" + HO + "` FIRST — IT IS NEWER THAN `_CHAIN.md` AND OUTRANKS IT.** ★★ **THE SESSION IS ONE SENTENCE: HE TOOK THE SITTING AND THE LOOSE ENDS, EVERY YES WAS INSCRIBED AND BUILT, v1.0.14 WAS CUT, AND CI WENT GREEN ON ALL THREE JOBS.** Rulings 638 → 699. The full record is in the ⏱ LATEST DELTA below, its sole home under `s241-D2`.)*"]})
D = open('notes/_lanes/305/W/_work/delta_305.txt', encoding='utf-8').read().rstrip('\n').split('\n')
ops.append({"op": "insert", "file": "_LIVE-STATE.md", "at": "## ⏱ LATEST DELTA — 2026-09-27 (Sun from `date`) (**#304**", "where": "before", "lines": D + [""]})
d304 = [l for l in ls if l.startswith('## ⏱ LATEST DELTA — 2026-09-27 (Sun from `date`) (**#304**')]
assert len(d304) == 1
ops.append({"op": "replace", "file": "_LIVE-STATE.md", "find": d304, "replace": [d304[0].replace('## ⏱ LATEST DELTA', '## ⏱ PRIOR DELTA', 1)]})
ops.append({"op": "insert", "file": "_LIVE-STATE-ARCHIVE.md", "at": "## Rolled 2026-09-26 #304", "where": "before", "lines": [
 "## Rolled 2026-09-27 #305 (2d, at the #305 wrap, ritual 2026-09-28) — via the mover", "",
 "*The #302 ⏱ delta block, moved VERBATIM by `_gm_move.py`. ⚠ No `Previous:` chain segment moved with it: none is left in `_LIVE-STATE.md`'s stamp lines; the #293–#304 stamps and dream pass 14's stand as separate lines and were not rolled — declared in the #305 stratum.*", ""]})
ops.append({"op": "move", "src": "_LIVE-STATE.md", "start": "## ⏱ PRIOR DELTA — 2026-09-24 (Thu from `date`) (**#302**", "end": "## 🕓 OPEN — Latin Univers",
            "dst": "_LIVE-STATE-ARCHIVE.md", "at": "## Rolled 2026-09-26 #304", "where": "before"})
out = 'notes/_lanes/305/W/_ops-305W-main.json'
json.dump(ops, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
assert os.path.exists(out) and os.path.getsize(out) > 10000, os.path.getsize(out)
print('ops', len(ops), 'bytes', os.path.getsize(out))
