#!/usr/bin/env python3
"""#284 wrap — build `_CARRIES.md` § `## residual → #285` from § `## residual → #284`.

ONE programmatic pass, the #261…#283 shape:
  (a) every age bracket bumped by one — `[NEW — 0…]` → `[1…]`, `[N…]` → `[N+1…]`;
  (b) ONE STRIKE, and it carries its receipt (`s183-D1` strike form, `s188-D2` receipt):
      #284's item ① claimed the disk was "NOT FIXABLE FROM ANY SEAT WE CAN REACH". #284
      FIXED IT FROM HIS MAC. The headline is struck in place, the retraction names the
      session and where the correction is inscribed, and THE BODY IS NOT RE-TYPED.
  (c) FOUR new items in front, newest first.
⛔ Nothing is dropped, re-worded, re-ordered or truncated. `s225-D2` clause (i).
⚠ NOT re-minted, because the age bracket carries a repeat and never a second copy: the
  per-size logo masters (#284's ② → [1] — they RAN today and were ACCEPTED BY EYE, which is
  said in NEW item ③ rather than by editing theirs, because acceptance is not the close
  condition `W-284lm` states), the hard-wall question, the git-lock runbook line, the four
  generators, `col26-012`, the boot ceiling, `s277-D12`, the `#243` not-a-wrap form,
  `jade-lifestyle`, the third dial, the theory door.
"""
import os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
CARRIES = os.path.join(ROOT, "_CARRIES.md")
sys.path.insert(0, os.path.join(ROOT, "knowledge"))
import _capture_gate as cg  # the ONE definition of "a carry"

text = open(CARRIES, encoding="utf-8").read()
src = [l for l in text.split("\n") if l.startswith("> **residual → #284:**")]
assert len(src) == 1, len(src)
src = src[0]
before = len(cg._carry_items(src))

# ---- (a) ages -----------------------------------------------------------------------------
n_new = len(re.findall(r"\[NEW — 0(?=[,\]])", src))
aged = re.sub(r"\[(\d+)(?=[,\]])", lambda m: "[%d" % (int(m.group(1)) + 1), src)
aged = re.sub(r"\[NEW — 0(?=[,\]])", "[1", aged)
assert "[NEW — 0" not in aged

# ---- (b) ONE strike, with its receipt ------------------------------------------------------
OLD_HEAD = ("⬛ **① THE DISK: THE HALF THAT WAS OURS IS FIXED, AND THE HALF THAT IS NOT IS NOT "
            "FIXABLE FROM ANY SEAT WE CAN REACH** [1, DAVE'S]")
NEW_HEAD = ("⬛ ~~**① THE DISK: THE HALF THAT WAS OURS IS FIXED, AND THE HALF THAT IS NOT IS NOT "
            "FIXABLE FROM ANY SEAT WE CAN REACH**~~ ⛔ **STRUCK AT THE #284 WRAP — THE SECOND HALF "
            "IS RETRACTED, AND THE RETRACTION NAMES ITS RECEIPT (`s183-D1` strike form, `s188-D2` "
            "receipt): IT WAS FIXABLE FROM HIS MAC.** The Cowork VM disk is a bundle on Dave's Mac "
            "under `~/Library/Application Support/Claude/`; he quit the app and trashed "
            "`claudevm.bundle`, keeping the `warm` folder, and `/sessions` went **98.7% (127,716 KB "
            "free) → 0.1% (9,665,792 KB free)** with `uptime` 1 min and the 127 dead homes gone. "
            "Correction inscribed at `notes/_lanes/284/DISK-LEVER-2026-09-18.md`, commit `ade8a403`; "
            "his word was *\"we've done all this i guess\"* and ⛔ **it is a FINDING plus an ACT, "
            "not a ruling.** ⚠ The source was a web how-to Dave pasted (reddit r/ClaudeAI 1rlc71n; "
            "anthropics/claude-code issue 37581) and **neither the bundle's filename nor its size "
            "was verified from inside the sandbox** — it cannot read that folder. ⚠ And the file "
            "itself predicted *\"the session performing the wipe ends\"*; **it did not — #284 "
            "survived the rebuild and continued in the same chat**, measured at this seat. The "
            "original item follows unedited. [1, DAVE'S]")
assert aged.count(OLD_HEAD) == 1, "the #284 ① headline did not match exactly once"
aged = aged.replace(OLD_HEAD, NEW_HEAD)

# ---- (c) the session's FOUR new items ------------------------------------------------------
NEWITEMS = [
 "⬛ **① THE DELEGATION LAPSE — HIS WORDS, RULING-SHAPED, RESTATING #57 / `s204-D1`** [NEW — 0, "
 "DAVE'S] — put to Dave at the wrap call; ⛔ **NOT INSCRIBED, and inscribing it is his.** His "
 "sentence verbatim: *\"I thought we had a subs strategy, basically everything is Delegated even if "
 "its a fable sub and the lane is always an orchestrator and judgment layer so we can get more work "
 "done in a session, this seems to have been lost\"*. **The measurement behind it, named by the "
 "conductor about himself:** #284 did lane work IN SEAT four times — the disk lever and its spec "
 "(~15K) · SIX runs of the commit script (~30K) · two screenshots read in-seat · the context-window "
 "research in-seat — and **only the drawing was a lane.** **The conductor's proposed mechanical fix, "
 "PROPOSED AND NOT BUILT:** `_seam.py` gains a conductor IN-SEAT TOOL-OUTPUT arm measuring tokens "
 "since the last seam and warning above a threshold; the opener STATES ITS ROUTING before the first "
 "beat; the COMMIT IS A LANE BY DEFAULT. ⚠ **A proposal is not a ruling and this one is a "
 "conductor's, not Dave's.** Receipts: `notes/_lanes/284/DAVE-RULINGS-2026-09-18.md` § On delegation "
 "· `knowledge/_rulings.json` § `s204-D1` · `_HANDOFF-135`.",

 "⬛ **② THE CONTEXT-WINDOW FINDING, AND DAVE'S CORRECTION OF WHAT IT MEANS** [NEW — 0, DAVE'S] — "
 "put to Dave at the wrap call; the correction is already his and is quoted, not paraphrased. "
 "**THE FINDING:** Anthropic's help centre, *\"How large is the context window on paid Claude "
 "plans?\"* (updated ~2 weeks before 2026-09-18) — *\"When using Claude Cowork with a Pro, Max, "
 "Team, or Enterprise plan, Claude Fable 5.1, Fable 5, Opus 5, Sonnet 5, Opus 4.8, and Opus 4.7 "
 "support a 1M token context window\"*; auto-compaction summarises earlier messages near the limit "
 "and *\"does not count towards your usage limit\"*; *\"Manage tools and connectors: These features "
 "are token-intensive\"*. ⛔ **THE CONDUCTOR READ IT AS A LICENCE TO RE-BASE THE STOP LINE AND DAVE "
 "CORRECTED HIM IN THE SAME TURN:** *\"but we gauged this against the messy middle problem not the "
 "1M context window, that was actually relevant then as it is now\"* ⇒ **the 180,000 line is a "
 "QUALITY line, not a wall line, and it STANDS.** ⚠ **WHAT THE FINDING DOES CHANGE, AND IT IS A "
 "WORDING FIX HE HAS NOT ORDERED:** the 256,000 figure in `_gauge_tokens.py` is called *hard* and "
 "is **not a wall for this model in Cowork**, so #277's, #281's and #282's *\"hard-line breaches\"* "
 "were QUALITY breaches and not crash risks. ⛔ **NOT DONE, and editing `_gauge_tokens.py` "
 "constants is fenced from a wrap.** Receipts: `notes/_lanes/284/DAVE-RULINGS-2026-09-18.md` "
 "§ FINDING · `knowledge/_gauge_tokens.py` · `_HANDOFF-135`.",

 "⬛ **③ THE 40 MASTERS ARE DRAWN AND ACCEPTED BY EYE; THE REGISTRATION IS OWED** [NEW — 0, DAVE'S] "
 "— put to Dave at the wrap call for the second half only. ✅ **DRAWN:** lane LM built "
 "`knowledge/assets/logos/_gen_masters.py` (`--check` rc 0) and `knowledge/assets/logos/masters/` — "
 "**40 SVGs, 8 lockups × 5 raw heights 24/28/32/36/40**, raw px width AND height, **no viewBox**, "
 "hexagon exact on the h/4 grid, wordmark stems snapped; masterbrand widths **89/104/119/133/148** "
 "(rounded — the floor alternative is named in the lane's own report). ✅ **ACCEPTED BY HIS OWN "
 "WORD: *\"the sheet is good BTW\"*** off `notes/_lanes/284/logo-masters/MASTERS-2026-09-18.html`, "
 "⇒ **`s282-D3` IS THEREBY ENACTED.** ⚠ **The one flaw the lane named itself and he accepted over: "
 "the B's horizontals sit a pixel off the H's crossbar at 24 and 40.** ⛔ **AND THE MASTERS ARE NOT "
 "REGISTERED IN `_logo_nodes.json`** — the lane was fenced from `gen_kg_icons.py`, which is one of "
 "the four generators that undo hand-authored state, **so HOW to run it is his word and the "
 "registration is the open half of row `W-284lm`.** Receipts: `notes/_subreports/2026-09-18-284-LM-"
 "logo-masters.md` · `notes/_lanes/284/logo-masters/BRIEF.md` · `ade8a403` · row `W-284lm` in "
 "`knowledge/_state.json`.",

 "⬛ **④ THE COMMIT TOOK SIX RUNS, AND TWO OF THEM WERE A STRANDED `index.lock` BECAUSE RUNBOOK "
 "STEP 0 WAS SKIPPED** [NEW — 0] — a finding about the ritual's own cost, not a ruling. The one "
 "#284 commit `ade8a403` took **SIX runs of `knowledge/_git_commit.sh`**: a showroom refusal "
 "(ack'd), a doc-row refusal (the `W-284lm` row added), a chain-stale refusal (`_CHAIN.md` "
 "regenerated and staged), then **a stranded `.git/index.lock` TWICE** because the git-commit "
 "runbook's step 0 — the `allow_cowork_file_delete` grant — **had not been taken**; once granted, "
 "`rm -f .git/index.lock` worked and the commit landed. ⚠ **FOUR of the six were the script working "
 "and are not a defect**; the two lock runs are, and their cause is a skipped step. ★ **The cost is "
 "the finding: ~30K of the conductor's own window went on commit-script output**, which is why "
 "`--quiet` on `_git_commit.sh` and running the commit AS A LANE are #285's third move. ⚠ **The "
 "shim `/tmp/gitshim` is GONE (it dies with every rebuild) and was not needed.** Receipts: "
 "`knowledge/_RUNBOOK-git-commit.md` step 0 · `ade8a403` · `_HANDOFF-135` § #285 FIRST MOVES.",
]

body = aged[len("> **residual → #284:** "):]
newline = "> **residual → #285:** " + " · ".join(NEWITEMS) + " · " + body
after = len(cg._carry_items(newline))
print("carries: before %d (of which %d were [NEW — 0]) → after %d ; new items %d ; strikes 1"
      % (before, n_new, after, len(NEWITEMS)))

SECTION = "## residual → #285"
assert SECTION not in text, "section already exists"
anchor = "## residual → #284"
i = text.index(anchor)
if "--write" not in sys.argv:
    print("DRY — nothing written"); sys.exit(0)
text = text[:i] + SECTION + "\n\n" + newline + "\n\n" + text[i:]
open(CARRIES, "w", encoding="utf-8").write(text)
print("WROTE", CARRIES)
