#!/usr/bin/env python3
"""#283 wrap, step 1 — PREPEND the new `Last refreshed` segment to `_LIVE-STATE.md`'s header
zone, demoting #282's segment to `Previous:`. The date comes from `date`, never from belief
(T-D12). Span reconstruction asserted in this process before anything is written.

✅ NO DATE SPLIT — #283 opened, ran and wrapped inside 2026-09-18.
"""
import os, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
LS = os.path.join(ROOT, "_LIVE-STATE.md")

NEW = (
 "*Last refreshed: 2026-09-18 (Fri from `date` — **#283 wrap**. "
 "✅ **NO DATE SPLIT: the session, its two conductor commits, this ritual and its own commit are ALL 2026-09-18** "
 "— #283 opened and closed inside one day. The four standing WRAP DATE SPLIT notices belong to #241, #248, #261 and "
 "#272/#277, and ⬛ **#241's ruling-shaped question — what a midnight-spanning wrap should stamp — is still Dave's, "
 "now at AGE 42, asked fifteen times and unanswered.** "
 "⛔★★★ **READ `_HANDOFF-134-the-seam-check-is-born-and-the-disk-is-diagnosed.md` FIRST — IT IS NEWER THAN `_CHAIN.md` "
 "AND OUTRANKS IT**, and it does NOT replace `_HANDOFF-130`, `-131`, `-132` or `-133`, whose open items still stand. "
 "★★ **ONE RULING, `knowledge/_rulings.json` 619 → 620, VERIFIED BY TEXTUAL SPAN AT THIS SEAT RATHER THAN RESTATED — "
 "`git show --numstat 107aa44 -- knowledge/_rulings.json` reads `15  0`, ZERO deletions, and a `json.load` counts 620.** "
 "**`s283-D1`** (`107aa44`, the conductor's own) — **THE LANE-SEAM CHECK IS STANDING, EVERY SESSION**: before every lane "
 "is cut and after every lane lands, `python3 knowledge/_seam.py`, and **its FILL line QUOTED in chat verbatim** with the "
 "verdict against stop **180,000** / tolerated **220,000** / hard **256,000**; the same call reads DISK and cleans the "
 "session's OWN scratch, `/tmp/gitshim` on a keep-list. ⚠ **ADVISORY — blocking is his.** His three sentences that made "
 "it: *\"can we do this in every session\"* · *\"good, maybe we make this a regular check- more mechanical\"* · *\"go\"*. "
 "✅ **AND `notes/_RULINGS.html` WAS RE-RENDERED FRESH IN THE SAME COMMIT (`28 10`) — the #281/#282 stale-page pattern "
 "did NOT get a third instance, and `--check` reads FRESH at this seat.** "
 "★★★ **THE FINDING OF THE SESSION IS THAT THE INSTRUMENT FIRED AND WAS OBEYED.** `knowledge/_seam.py` was born this "
 "morning (selftest 6 arms green) and **fired at its FIRST REAL SEAM — 210,476 real at turn 43 — and the conductor "
 "OBEYED IT: the per-size logo-masters lane was NOT cut.** ⇒ **the masters are still #284's first move, and that is the "
 "ruling working rather than the session failing.** ⚠ **n=1: one obeyed advisory is a data point, not a trend**, and the "
 "three-breach arc (#277 crossed under pressure · #281 read the gauge and overruled it · #282 did not read it at all) is "
 "not withdrawn by it. "
 "⛔★★ **THE SESSION'S SECOND STORY IS THE DISK, AND IT IS FINDINGS — HIS TO RULE ON, INSCRIBED AS NOTHING ELSE.** "
 "**(a) The #227/#228 fix HELD** — `/var/tmp` is empty and the scratch-hygiene gate did its job; the disk record shows "
 "it clearing exactly twice (#233, and the night before #282), **both times by an external rebuild after hitting 100%, "
 "never by anything in the repo**. **(b) Today's real cause was OURS: the repo was 9.3 GB on a 9.8 GB disk** — "
 "`knowledge/assets/assets (5).zip` 2.5G duplicating `photography/` 2.5G (both gitignored) · `.git` 2.6G with **28,991 "
 "loose objects never packed against a 63 KB pack, plus 745 `tmp_obj_` stubs (120 MB) from the index-lock class** · "
 "`outputs/_render-env-229` 482M · `_to_delete/` 133M · three zips 60M. **(c) Dave fixed it on his own Mac, instructed "
 "step by step** (*\"you'll have to instruct me im not a terminal ace pilot\"* — two Finder moves and one line, "
 "`git gc --prune=now && find .git/objects -name 'tmp_obj_*' -delete`): measured after, **repo 4.3 GB · `.git` 576 MB · "
 "`count-objects` count 0 / size-pack 575,855 KB / garbage 0**, `git status` unchanged, photography originals kept. "
 "⛔ **(d) AND THE DISK DID NOT RELEASE: 9.1G used / 136 MB free after a full app restart** (VM `uptime` 1 min, the same "
 "127 dead session dirs). `/sessions` is a **persistent ext4 volume** and the 4.8 GB residue is **127 "
 "`drwxr-x--- nobody:nogroup` session homes, mtimes Sep 9–15, unreadable and unremovable from any session uid, no "
 "`sudo`** — every session AND every sub-lane gets one, ~38 MB each, and the rebuild appears to trigger at 100% rather "
 "than on a schedule. ⛔ **NOT fixable from inside; NOT fixable from his Mac.** His options, neither taken here: "
 "**thumbs-down feedback to Anthropic naming the dead-home leak**, or **wait for the next rebuild — which now buys ~5 GB "
 "of headroom instead of 500 MB, because the repo shrank**. **(e) The one lever inside was pulled** (`85aee08`): "
 "`_gate_scratch_hygiene.py` gained SCRATCH_ROOTS `~/tmp` and `~/.cache`, `WRAP_ONLY_ROOTS` `~/.local` under `--wrap`, "
 "and **`KEEP = /tmp/gitshim`**. ✅ **VERIFIED AT THIS SEAT AT 4c: `--clean --wrap` removed two entries and printed "
 "`/tmp/gitshim → KEPT (keep-list)` — which CLOSES the 4c/step-5 collision #282 measured.** "
 "⚙ **GAUGE, MEASURED AT THIS SEAT against the conductor's own transcript** — the session's top-level window, this wrap "
 "seat being a subagent log beneath it, which is what makes the subtraction legal: **FILL 226,084 real over 53 turns** "
 "against **221,028 real / 51 turns DECLARED** at the brief cut ⇒ **delta 5,056**. ⛔ **6,084 OUTSIDE the ≤220,000 "
 "tolerance and 46,084 past the ruled 180,000 stop line** — ✅★★ **BUT THE 256,000 HARD LINE WAS NOT BREACHED: the FIRST "
 "SESSION IN FOUR to stay under it.** The cause of the fill is NAMED by the conductor and not smoothed: the disk "
 "investigation, where **one `git count-objects -vH` printed 745 `tmp_obj_` garbage lines (~60K real) that should have "
 "been piped through `grep`**. **BOOT 80,871 real, n=1** against the `s129-D1` floor 70,794 — **+10,077, NOT a re-base**, "
 "`BOOT_FIRSTTURN_TK` untouched and n=1 published as n=1; it agrees with the brief's declaration to the token, and it is "
 "the **EIGHTH** post-diet reading over `BOOT_CEILING_TK` 70,000 — **cutting the boot is his word and raising the literal "
 "is forbidden** [[gate-must-quote-what-it-forbids]]. ⛔ **NO `subs` LINE IS WRITTEN: no lanes were cut, sub-tokens are "
 "0 and n=0** — and `s214-D5` forbids defaulting an absence into a number, which is as true of a zero as of an unknown. "
 "⛔ **NO PACE PANEL WAS ASKED FOR AND NONE IS INVENTED.** ⛔ **`/sessions` 98.6%, 139,712 KB free measured here.** "
 "⛔ **SIX BLOCKING GATE FAILS CARRIED IN THE `#243` FORM — the NINTH consecutive wrap on that path — every one another "
 "session's append-only testimony in `notes/_GAUGE-LOG.md`** (the boot-drift ceiling breach and five boot double-counts: "
 "#243, #264, #272, #273, #274). ⛔ **A WRAP MAY NOT REPAIR AN INHERITED GATE FAIL and this one did not try.** "
 "⚠ **A SEVENTH STOOD AT THE OPEN AND IS THIS SEAT'S OWN: the retrieval index was STALE against GM/LS, exactly the #32 "
 "defect — closed at 2g, which is where the ritual puts it.** "
 "⚠ **TWO INSTRUMENTATION APPENDS (`knowledge/_graph-mark-observations.jsonl`, `notes/_dream/_GRADE-DECISIONS.jsonl`) "
 "stood in the tree at the brief cut and more accrued during this ritual; they are committed with this wrap to clear the "
 "push gate, exactly as #282 did, and the POLICY on them is still Dave's (dream pass 6 P2, floated).** "
 "✅★★ **CLOUD MEMORY (step 3) WAS WRITTEN FROM THIS WRAP SUB'S OWN SEAT — n=5, the FIFTH consecutive wrap to measure the "
 "runbook's \"structural\" seat limit FALSE** (`wrap-283-the-seam-check-is-born-and-the-disk-is-diagnosed.md`, **5,118 B**; "
 "`index.md` now **16,099 B of the 49,152 B cap**), and ⛔ **the runbook line is STILL NOT EDITED — amending a ratified "
 "step is Dave's word.** Gauge, declared skips with their sizes, and not-done: the ⏱ LATEST DELTA below. "
 "**`_CARRIES.md` § `## residual → #284` is the carry set (`s225-D2`); the banner carries the pointer and the probeable "
 "count.** **This wrap's own filed report (`s218-D7`): `notes/_subreports/2026-09-18-283-W-wrap.md`.** "
 "**Narrative dossier (1b): `_DECISION-HISTORY/2026-09-18-283-the-seam-check-is-born-and-the-disk-is-diagnosed.md`.** "
 "**His words verbatim: `notes/_lanes/283/DAVE-RULINGS-2026-09-18.md`.**)*  "
 "Previous: "
)

OLD_HEAD = "*Last refreshed: 2026-09-18 (Fri from `date` — **#282 wrap**."
NEW_HEAD = "2026-09-18 (Fri from `date` — **#282 wrap**."

orig = open(LS, encoding="utf-8").read()
assert orig.count(OLD_HEAD) == 1, ("anchor must be unique", orig.count(OLD_HEAD))
new = orig.replace(OLD_HEAD, NEW + NEW_HEAD, 1)
assert new.count("*Last refreshed: 2026-09-18 (Fri from `date` — **#283 wrap**.") == 1
assert len(new) == len(orig) + len(NEW) + len(NEW_HEAD) - len(OLD_HEAD)
if "--write" not in sys.argv:
    print(f"DRY: new segment {len(NEW)} chars; file {len(orig)} → {len(new)}"); sys.exit(0)
open(LS, "w", encoding="utf-8").write(new)
print(f"WROTE: new `Last refreshed` segment, {len(NEW)} chars; file {len(orig)} → {len(new)}")
