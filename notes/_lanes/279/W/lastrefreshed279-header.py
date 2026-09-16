#!/usr/bin/env python3
"""#279 wrap, step 1: stamp `Last refreshed` from `date` and demote #278's segment to
`Previous:`. ONE textual span inserted, ONE eleven-character prefix rewritten, both asserted
by reconstruction in this process before the write. The date comes from `date`, never belief."""
import subprocess, sys
LS = "_LIVE-STATE.md"
orig = open(LS, encoding="utf-8").read()
TODAY = subprocess.check_output(["date", "+%Y-%m-%d (%a"], text=True).strip()
assert TODAY.startswith("2026-09-16 (Wed"), TODAY

OLD_HEAD = "*Last refreshed: 2026-09-16 (Wed from `date` — **#278 wrap**."
NEW_HEAD = "Previous: 2026-09-16 (Wed from `date` — **#278 wrap**."
assert orig.count(OLD_HEAD) == 1, orig.count(OLD_HEAD)

SEG = (
 "*Last refreshed: 2026-09-16 (Wed from `date` — **#279 wrap**. ✅ **NO DATE SPLIT: the session, "
 "its ritual and all seventeen of its commits are 2026-09-16** — #279 opened and closed inside one "
 "day. The four standing WRAP DATE SPLIT notices belong to #241, #248, #261 and #272/#277, and "
 "⬛ **#241's ruling-shaped question — what a midnight-spanning wrap should stamp — is still "
 "Dave's, now at AGE 38, asked eleven times and unanswered.** ⛔★★★ **READ "
 "`_HANDOFF-130-the-wave-lands-and-the-graph-question.md` FIRST — IT IS NEWER THAN `_CHAIN.md` AND "
 "OUTRANKS IT**, and it does NOT replace `_HANDOFF-129`, whose cloud-store findings and STRUCTURAL "
 "REDS are live; #129's \"#279 FIRST MOVES\" list is SPENT — every move on it ran. ★★ **ONE "
 "RULING, `knowledge/_rulings.json` 604 → 605, BY TEXTUAL SPAN — `git diff --numstat` reads "
 "`18  0`, ZERO deletions, span 1,682 bytes at offset 828,664, `_inscribe_ruling.py` reconstruction "
 "proof PASSED, verified here.** **`s279-D1`**: on his *\"i agree 'a' it is\"*, asked for in plain "
 "prose first, **the designer pack ships the reader (`_compose_slice.py`) and the Constitution "
 "(`_rulings.json`), so ASK reads the Constitution LIVE in-pack** — reversing the deliberate "
 "exclusion in `knowledge/_gen_pack_manifest.py`, a release under `P-269-1`, and changing neither "
 "storage nor the `s278-D1` seed contract. ★★★ **THE `s277` WAVE IS IN THE TREE — "
 "`s277-D4..D11` and `D13` ENACTED across ten lane commits, and ⛔ `s277-D12` (tokens at "
 "group+tier) WAS NEVER STARTED**: icons `f641242` (688 nodes / 1,299 edges / 32 declared nulls) + "
 "`84658db` · reader `d6bd57b` (`_compose_slice.py` wired as step 1, seed 31,372 vs 1,005,758 = "
 "**32.06×**) · scope `9e7a158` + `e3facb4` (34 rows; rules reaching a component 107 → 408 "
 "of 470; BLOCKING 9 → 52 of 59) · explorer `2c6b640` + `9b2e1b0` (v1.16, four labelled boxes, "
 "`assets` shipping chip OFF) · verbs `eb2ff7c` (12 verbs over 36 of 58 edge types, 75% of edges "
 "walked) · pack `df33a24` + `3710d6b` (designer-skills-v2 **v2.1**, 1,102 files, read closure 218 "
 "paths with 0 outside the pack). ⛔★★★ **AND DAVE'S OWN EYE REFUSED THE RESULT**: "
 "*\"this does not look like 3 layers, just relabelling and grouping them isn't what I expected tbh.\"* "
 "The lanes enacted `s277-D8` to its LETTER — storage untouched, chips and labels changed — and "
 "what he wants is a **LAYOUT**. **RULING-SHAPED, NOT INSCRIBED: #280's FIRST move is a layout lane "
 "with ONE concrete option on a page.** ⬛ **HIS 15-BASE EXPORT ARRIVED 15:55Z AND IS UNREAD BY THE "
 "RECORD** — `notes/_lanes/279/active-review/DAVE-EXPORT-active-2026-09-16.json`, 15/15 twins, 12 "
 "mislabels, flag-vs-note disagreeing on `electricity` and four rows note-only; **inscribe lane at "
 "#280, NOTE beats FLAG, ask on the four.** ⚙ **GAUGE: FILL 213,222 real / 43 turns MEASURED "
 "first-hand at this wrap seat against the conductor's own transcript** (first user record his own "
 "opener, so the subtraction is legal) against **207,989 real / 41 turns DECLARED** at the check-in "
 "⇒ **delta 5,233**; ⛔ **the 200,000 working line is BREACHED, the second breach in three "
 "sessions, DECLARED not excused** — his *\"use fable judgment liberally and subs\"* is on the "
 "record as its cause and his *\"keep an eye on the context window\"* closed the day. **BOOT 72,447 "
 "real, n=1** against the `s129-D1` floor 70,794 — **+1,653, NOT a re-base**, `BOOT_FIRSTTURN_TK` "
 "untouched. ⛔ **`/sessions` 98.2%, 169,500 KB free, measured here** — nothing in the repo "
 "fixes it and he was told so at the opener. **No `subs` line is written**: fourteen delegated seats, "
 "the conductor's figure an ESTIMATE, and `s214-D5` forbids defaulting an absence into a number. "
 "⛔ **`_validate_roles_resolve.py` READS FAIL(6) and `_validate_lane_ownership.py --selftest` "
 "READS 2/3, both measured here and both INHERITED.** ✅ **ONE INHERITED STORE RED REPAIRED HERE: "
 "`knowledge/_state.json`'s `W-278wr` row was missing its required `links` field** — four #279 "
 "lanes reported it and none could fix it from a lane seat; added by textual span, insertions only. "
 "⛔ **MEMORY (step 3) IS UNREACHABLE FROM THIS SEAT — A STRUCTURAL SEAT LIMIT, NOT A SKIP** "
 "— hook body and index line at `notes/_lanes/279/WRAP-MEMORY-HOOK.md` for the conductor to place "
 "at the #280 opener. Gauge, declared skips (each with its size) and not-done: the ⏱ LATEST DELTA "
 "below. **`_CARRIES.md` § `## residual → #280` is the carry set (`s225-D2`); the banner carries "
 "the pointer and the probeable count.** **This wrap's own filed report (`s218-D7`): "
 "`notes/_subreports/2026-09-16-279-W-wrap.md`.** **Narrative dossier (1b): "
 "`_DECISION-HISTORY/2026-09-16-279-the-wave-lands-and-the-graph-question.md`.**)*  ")

i = orig.find(OLD_HEAD)
new = orig[:i] + SEG + NEW_HEAD + orig[i+len(OLD_HEAD):]
# reconstruction: removing the inserted span and restoring the demoted prefix gives the original
chk = new[:i] + OLD_HEAD + new[i+len(SEG)+len(NEW_HEAD):]
assert chk == orig, "REFUSED — reconstruction failed"
if "--write" not in sys.argv:
    print(f"DRY: insert {len(SEG)} chars at {i}; prefix demoted; reconstruction PASSED"); sys.exit(0)
open(LS, "w", encoding="utf-8").write(new)
print(f"WROTE: Last refreshed stamped #279 from `date` ({TODAY}); "
      f"#278 demoted to Previous:; span {len(SEG)} chars; reconstruction PASSED before the write")
