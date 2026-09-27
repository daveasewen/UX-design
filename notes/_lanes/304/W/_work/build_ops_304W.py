# #304 wrap seat - the ONE _gm_move.py transaction for 2c / 2d / 2f and the new banner, delta, stamp,
# header date-split line and stratum. Unique, session-owned ops file, asserted to exist. Modelled on #303's build_ops_303W.py.
import json, os, sys
sys.path.insert(0, 'notes/_lanes/304/W/_work')
from names_304 import *
gm = open('GOOD-MORNING.md', encoding='utf-8').read().split('\n')
ls = open('_LIVE-STATE.md', encoding='utf-8').read().split('\n')
ops = []
t_old = [l for l in gm if l.startswith('> **TITLE THE NEXT CHAT →**')]
assert len(t_old) == 1
ops.append({"op": "replace", "file": "GOOD-MORNING.md", "find": t_old, "replace": ["> **TITLE THE NEXT CHAT →** `" + NEXT_TITLE + "`"]})
SPLIT8 = '> ⚠ **WRAP DATE SPLIT, EIGHTH OCCURRENCE ON THIS RUN'
assert sum(1 for l in gm if l.startswith(SPLIT8)) == 1
ops.append({"op": "insert", "file": "GOOD-MORNING.md", "at": SPLIT8, "where": "after", "lines": [
 "> ⚠ **WRAP DATE SPLIT, NINTH OCCURRENCE ON THIS RUN — SESSION OPENED SATURDAY 2026-09-26 AND RAN THROUGH THE NIGHT ON DELEGATED SEATS; RITUAL + WRAP COMMIT SUNDAY 2026-09-27.** #304 opened at 14:40 BST on 09-26; its commits carry both dates (`6af293df` to `aaf3bb7e` on 09-26, `86249459` to `8a5fa863` on 09-27). ⛔ **Nothing re-dated** — `s294-D11`'s shape: the session date on keys, the dossier and the stratum (`2026-09-26-304-*`), the ritual date on this one line so the gate's `is not today` check grades a true statement; reports keep the day their lanes wrote them."]})
PROBE = "PYTHONPATH=knowledge python3 -c \"import _capture_gate as c;print(len(c._carry_items([l for l in open('_CARRIES.md') if '#305:**' in l][0])))\""
NC = int(open('notes/_lanes/304/W/_work/carries_count.txt').read().split()[0])
PREV = 709
B = [
 "> ## ★ LATEST — 2026-09-27 (Sun **#304**, DATE SPLIT from Sat 09-26, Opus 5.5 conductor in the CLOUD, **49 subs**, DELEGATED wrap on Opus 5.5 — ★★ **" + HEADLINE + "**)",
 ">",
 "> - ★★★ ① **THE TUESDAY SITTING IS #305'S FIRST BEAT — 53 CALLS, `" + SITTING + "`**, opened through the artifact. Call 1: cut v1.0.14 from candidate 2. Three behaviours shipped without a ruling (tick thinning, right gutter, console card padding 20 → 8) and two are held back (the Kpi-tile descender, the root trim) — his. **`_rulings.json` STAYS 638.**",
 "> - ★★ ② **SEVEN COMMITS, SIX CI READS, ALL PUSHED, `571d458c..8a5fa863`:** the Apollo-MCP page v1 and v2 (the PoC first; Jev not ruled out for GenUI), CI asks every step again, 184 statuses stamped with receipts, `s245-D10` and `s277-D12` built, the v1.0.14 candidate and nine cold runs scored. The scheduled dream pass (`" + DREAM_SHA + "`) ran `git status` on the mount and its row took CI step 117 red once.",
 "> - ⚠ ③ **HIS LINKS DID NOT WORK: `computer://` cannot be previewed in the app, so review pages go as ONE artifact, republished to the same URL; answers come back by \"Copy as text\". The hub's links lack the `notes/` prefix — UNPROVEN that they open.** FILL 453,905 at the wrap (hand sum), over 300K since Sat 22:08. **`" + HO + "` OUTRANKS `_CHAIN.md`.**",
 "> **residual → #305:** ⬛ **THE TUESDAY SITTING, 53 CALLS** [1, DAVE'S] — put it first. `s225-D2`. **" + format(NC, ',') + " items, 10 new, 4 STRUCK (1 by the act, 3 by receipt)**, `_CARRIES.md` § `residual → #305` `carries:residual-305`. PROBE `" + PROBE + "` = " + str(NC) + ". #304's 6 new are counted by it now: " + str(PREV) + "→" + str(NC) + ".",
 "",
]
ops.append({"op": "insert", "file": "GOOD-MORNING.md", "at": "> ## ★ LATEST — 2026-09-26 (Sat **#303**", "where": "before", "lines": B})
old303 = [l for l in gm if l.startswith('> ## ★ LATEST — 2026-09-26 (Sat **#303**')]
assert len(old303) == 1
ops.append({"op": "replace", "file": "GOOD-MORNING.md", "find": old303, "replace": [old303[0].replace('> ## ★ LATEST —', '> ## ★ PRIOR —', 1)]})
ops.append({"op": "insert", "file": "_GM-ARCHIVE.md", "at": "## Batch 2026-09-24 #303", "where": "before", "lines": [
 "## Batch 2026-09-26 #304", "",
 "*Rolled at the #304 wrap (2c, ritual 2026-09-27). The #302 ★ PRIOR banner, moved VERBATIM by `_gm_move.py` — a move, never a rewrite. Its durable content already lives in `_DECISION-HISTORY/`, `notes/_subreports/`, the ledgers and git, and every ⬛/⚠ item on it is carried in `_CARRIES.md` (§ `residual → #303` onward, now § `residual → #305`) at its true age; this archive is a convenience copy, never a tattoo.*", ""]})
ops.append({"op": "move", "src": "GOOD-MORNING.md", "start": "> ## ★ PRIOR — 2026-09-24 (Thu **#302**", "end": "## ⬛ DO THIS FIRST",
            "dst": "_GM-ARCHIVE.md", "at": "## Batch 2026-09-26 #304", "where": "after"})
ops.append({"op": "roll_2f", "session": 303, "pm_start": "#### 2026-09-24 #303", "pm_end": "> **COMMIT STATE #303:**",
            "cs_start": "> **COMMIT STATE #303:**", "cs_end": "#### 2026-08-05 #96"})
S = open('notes/_lanes/304/W/_work/stratum_304.txt', encoding='utf-8').read().rstrip('\n').split('\n')
ops.append({"op": "insert", "file": "GOOD-MORNING.md", "at": "#### 2026-08-05 #96", "where": "before", "lines": S + [""]})
ops.append({"op": "insert", "file": "_LIVE-STATE.md", "at": "*Last refreshed: 2026-09-26 (Sat from `date` — **#303 wrap**", "where": "after", "lines": [
 "*Last refreshed: 2026-09-27 (Sun from `date` — **#304 wrap**. ⛔★★ **DATE SPLIT, THE NINTH ON THIS RUN AND `s294-D11`'s SHAPE: #304 opened Saturday 2026-09-26 at 14:40 BST and ran through the night on delegated seats; its commits carry both dates, and this ritual is Sunday 2026-09-27** — `date` at this seat read `Sun Sep 27 11:21:13 UTC 2026` (12:21 BST). ⛔★★★ **READ `" + HO + "` FIRST — IT IS NEWER THAN `_CHAIN.md` AND OUTRANKS IT.** ★★ **THE SESSION IS ONE SENTENCE: THE WEEKEND RUNS HE ASKED FOR LANDED IN SEVEN PUSHED COMMITS, THE TUESDAY SITTING PAGE CARRIES WHAT IS HIS, AND BECAUSE HIS LINKS DID NOT OPEN THE REVIEW MOVED TO ONE ARTIFACT.** Nothing inscribed. The full record is in the ⏱ LATEST DELTA below, its sole home under `s241-D2`.)*"]})
D = open('notes/_lanes/304/W/_work/delta_304.txt', encoding='utf-8').read().rstrip('\n').split('\n')
ops.append({"op": "insert", "file": "_LIVE-STATE.md", "at": "## ⏱ LATEST DELTA — 2026-09-26 (Sat from `date`) (**#303**", "where": "before", "lines": D + [""]})
d303 = [l for l in ls if l.startswith('## ⏱ LATEST DELTA — 2026-09-26 (Sat from `date`) (**#303**')]
assert len(d303) == 1
ops.append({"op": "replace", "file": "_LIVE-STATE.md", "find": d303, "replace": [d303[0].replace('## ⏱ LATEST DELTA', '## ⏱ PRIOR DELTA', 1)]})
ops.append({"op": "insert", "file": "_LIVE-STATE-ARCHIVE.md", "at": "## Rolled 2026-09-24 #303", "where": "before", "lines": [
 "## Rolled 2026-09-26 #304 (2d, at the #304 wrap, ritual 2026-09-27) — via the mover", "",
 "*The #301 ⏱ delta block, moved VERBATIM by `_gm_move.py`. ⚠ No `Previous:` chain segment moved with it: none is left in `_LIVE-STATE.md`'s stamp lines; the #293–#303 stamps and dream pass 14's stand as separate lines and were not rolled — declared in the #304 stratum.*", ""]})
ops.append({"op": "move", "src": "_LIVE-STATE.md", "start": "## ⏱ PRIOR DELTA — 2026-09-23 (Wed from `date`) (**#301**", "end": "## 🕓 OPEN — Latin Univers",
            "dst": "_LIVE-STATE-ARCHIVE.md", "at": "## Rolled 2026-09-24 #303", "where": "before"})
out = 'notes/_lanes/304/W/_ops-304W-main.json'
json.dump(ops, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
assert os.path.exists(out) and os.path.getsize(out) > 10000, os.path.getsize(out)
print('ops', len(ops), 'bytes', os.path.getsize(out))
