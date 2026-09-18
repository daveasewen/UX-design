#!/usr/bin/env python3
"""#283 wrap — build `_CARRIES.md` § `## residual → #284` from § `## residual → #283`.

ONE programmatic pass, the #261…#282 shape:
  (a) every age bracket bumped by one — `[NEW — 0…]` → `[1…]`, `[N…]` → `[N+1…]`;
  (b) ZERO strikes. No #283 ruling retracted or corrected the CLAIM of any carried item.
      `s283-D1` is the session's only ruling and it MINTS an instrument; it closes nothing
      that was carried. A strike that is wrong is worse than an item that is merely stale
      (`s271-D4`), so none is written.
  (c) THREE new items in front, newest first.
⛔ Nothing is dropped, re-worded, re-ordered or truncated. `s225-D2` clause (i).
⚠ NOT re-minted, because the age bracket is what carries a repeat and never a second copy:
  the per-size logo masters (#283's ① → [1] — they did NOT run today, and the reason is the
  ruling working, which is said in the NEW item ② rather than by editing theirs), the
  hard-wall question (#283's ⑤ → [1]), the git-lock runbook line (#283's ⑦ → [1]), the four
  generators (#283's ⑥ and ③ → [1]), `col26-012` (#283's ④ → [1]), the boot ceiling
  ([6]/[8]/[13]), `s277-D12`, the `#243` not-a-wrap form, `jade-lifestyle`, the VM disk
  item at [55] — which the NEW item ① answers in part WITHOUT touching its wording.
"""
import os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
CARRIES = os.path.join(ROOT, "_CARRIES.md")
sys.path.insert(0, os.path.join(ROOT, "knowledge"))
import _capture_gate as cg  # the ONE definition of "a carry"

text = open(CARRIES, encoding="utf-8").read()
src = [l for l in text.split("\n") if l.startswith("> **residual → #283:**")]
assert len(src) == 1, len(src)
src = src[0]
before = len(cg._carry_items(src))

# ---- (a) ages -----------------------------------------------------------------------------
n_new = len(re.findall(r"\[NEW — 0(?=[,\]])", src))
aged = re.sub(r"\[(\d+)(?=[,\]])", lambda m: "[%d" % (int(m.group(1)) + 1), src)
aged = re.sub(r"\[NEW — 0(?=[,\]])", "[1", aged)
assert "[NEW — 0" not in aged

# ---- (b) NO strikes -------------------------------------------------------------------------
# declared, not silent: zero `~~` were added by this pass.
assert aged.count("~~") == src.count("~~")

# ---- (c) the session's THREE new items ------------------------------------------------------
NEWITEMS = [
 "⬛ **① THE DISK: THE HALF THAT WAS OURS IS FIXED, AND THE HALF THAT IS NOT IS NOT FIXABLE FROM ANY "
 "SEAT WE CAN REACH** [NEW — 0, DAVE'S] — put to Dave at the wrap call; FINDINGS, his to rule on. "
 "**(a) THE #227/#228 FIX HELD.** `/var/tmp` is empty and the scratch-hygiene gate did its job; the "
 "disk record (`_HANDOFF-119` 96.5% · `-129` 97% · `-131` 99% · `notes/_lanes/279/DAVE-RULINGS-2026-09-16.md` "
 "*\"can we fix this now?\"*) shows it clearing exactly twice, at #233 and the night before #282, **both "
 "times by an external rebuild after hitting 100%, never by anything in the repo**. **(b) TODAY'S REAL "
 "CAUSE WAS OURS: the repo was 9.3 GB on a 9.8 GB disk** — `knowledge/assets/assets (5).zip` 2.5G "
 "(a duplicate of `photography/` 2.5G, both gitignored) · `.git` 2.6G, **28,991 loose objects never "
 "packed against a 63 KB pack, plus 745 `tmp_obj_` stubs (120 MB) from the index-lock class** · "
 "`outputs/_render-env-229` 482M · `_to_delete/` 133M · three zips 60M. **(c) DAVE FIXED IT ON THE MAC, "
 "INSTRUCTED STEP BY STEP** (*\"you'll have to instruct me im not a terminal ace pilot\"* — two Finder "
 "moves and one line, `git gc --prune=now && find .git/objects -name 'tmp_obj_*' -delete`): repo **4.3 GB**, "
 "`.git` **576 MB**, `count-objects` count 0 / size-pack 575,855 KB / garbage 0, `git status` unchanged, "
 "photography originals kept. ⛔ **(d) AND THE DISK DID NOT RELEASE: 9.1G used / 136 MB free after a full "
 "app restart** (VM `uptime` 1 min, the same 127 dead session dirs). `/sessions` is a persistent ext4 "
 "volume and the 4.8 GB residue is **127 `drwxr-x--- nobody:nogroup` session homes, mtimes Sep 9–15, "
 "unreadable and unremovable from any session uid, no `sudo`** — every session AND every sub-lane gets "
 "one, ~38 MB of pip installs and tokenizer cache each, and the rebuild appears to trigger at 100% rather "
 "than on a schedule. ⛔ **NOT fixable from inside and NOT fixable from his Mac.** His options, neither "
 "taken here: **thumbs-down feedback to Anthropic naming the dead-home leak**, or **wait for the next "
 "rebuild — which now buys ~5 GB of headroom instead of 500 MB, because the repo shrank**. **(e) THE ONE "
 "LEVER INSIDE WAS PULLED** (`85aee08`): `_gate_scratch_hygiene.py` now cleans our own session home "
 "(`~/tmp`, `~/.cache`, and `~/.local` under `--wrap`). ⬛ **AND ONE FURTHER QUESTION IS HIS: whether the "
 "seam check's \"no render lane over 90%\" should be promoted from ADVISORY to BLOCKING.** Receipts: the "
 "#283 wrap brief § THE DISK 1–5 · `notes/_lanes/283/DAVE-RULINGS-2026-09-18.md` § Later, on the disk · "
 "`knowledge/_seam.py` · `85aee08`.",

 "⬛ **② A SESSION STOPPED AT ITS OWN SEAM CHECK FOR THE FIRST TIME — A DATA POINT ON THE HARD-WALL "
 "QUESTION, NOT AN ANSWER TO IT** [NEW — 0] — the hard-wall carry ages beside this one at `[1]` and its "
 "wording is untouched, because **this is evidence and that is the question**. `s283-D1` was ruled this "
 "morning on his *\"can we do this in every session\"*; `knowledge/_seam.py` was built the same hour "
 "(`107aa44`, selftest 6 arms green) and **FIRED AT ITS FIRST REAL SEAM — 210,476 real at turn 43 — and "
 "the conductor OBEYED IT: the per-size logo-masters lane was NOT cut.** ★ **That is why the masters are "
 "still open, and it is the point of the ruling rather than a failure of the session.** ⛔ **The session "
 "still closed OUTSIDE the ≤220,000 tolerance** (see the ⏱ LATEST DELTA for the measured figure) — the "
 "check is ADVISORY by `s283-D1`'s own words and blocking is HIS — **but the 256,000 hard line was NOT "
 "breached, the first session in four to stay under it.** ⚠ **n=1. One obeyed advisory is a data point, "
 "not a trend**, and the three-breach arc (#277 crossed under pressure · #281 read and overruled · #282 "
 "did not read at all) is not withdrawn by it. Receipts: `knowledge/_rulings.json` § `s283-D1` (`107aa44`, "
 "span `15  0`) · `knowledge/_seam.py` · `knowledge/_RUNBOOK-context-gauge.md` § the seam line.",

 "⬛ **③ THE 4c/STEP-5 COLLISION IS CLOSED — AND THE CARRY THAT WAS SAID TO HOLD IT WAS NEVER MINTED** "
 "[NEW — 0] — two facts, and the second is the one worth writing. **(a) CLOSED.** #282 measured step 4c "
 "(`_gate_scratch_hygiene.py --clean`) deleting `/tmp/gitshim`, the shim step 5 depends on under this "
 "mount. `85aee08` puts `/tmp/gitshim` on the gate's **KEEP list by name** and updates the runbook's 4c "
 "line in the same commit; **verified at this seat at 4c — the shim survived `--clean --wrap`**. ⛔ **(b) "
 "AND THE RECORD SAID IT WAS CARRIED WHEN IT WAS NOT.** `notes/_subreports/2026-09-18-282-W-wrap.md` "
 "finding 6 states the collision *\"is now in `_CARRIES.md`, the handoff and the store line\"*; a probe of "
 "§ `residual → #283` at this seat finds **no item mentioning `gitshim` or step 4c at all** — the git-lock "
 "runbook line carried at `[1]` is its SIBLING and says nothing about 4c. **The collision survived one "
 "wrap on a claim rather than on a carry**, and it is only closed today because the conductor fixed it "
 "from a different direction. ★ **The class is the one `s188-D2` exists for read backwards: a wrap may "
 "state that it homed an item, and nothing checks that it did** [[instrument-without-a-consumer]] — the "
 "2c EXIT CHECK tests PRESENCE for items it can SEE, and an item that was never written is invisible to "
 "it. ⚠ **The git-lock runbook line itself is UNTOUCHED and still his** (ageing at `[1]`); today's data "
 "point on it is that **the shim dies with every VM rebuild — it was gone at this session's open after "
 "Dave restarted the app — while the commit script survives without it and leaves an unlinkable "
 "`index.lock` warning each time** (`107aa44`, `85aee08`, and this wrap's own commit). Receipts: "
 "`notes/_subreports/2026-09-18-282-W-wrap.md` finding 6 · `85aee08` · "
 "`knowledge/_RUNBOOK-capture-ritual.md` step 4c.",
]

body = aged[len("> **residual → #283:** "):]
newline = "> **residual → #284:** " + " · ".join(NEWITEMS) + " · " + body
after = len(cg._carry_items(newline))
print("carries: before %d (of which %d were [NEW — 0]) → after %d ; new items %d ; strikes 0"
      % (before, n_new, after, len(NEWITEMS)))

SECTION = "## residual → #284"
assert SECTION not in text, "section already exists"
anchor = "## residual → #283"
i = text.index(anchor)
if "--write" not in sys.argv:
    print("DRY — nothing written"); sys.exit(0)
text = text[:i] + SECTION + "\n\n" + newline + "\n\n" + text[i:]
open(CARRIES, "w", encoding="utf-8").write(text)
print("WROTE", CARRIES)
