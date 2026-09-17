#!/usr/bin/env python3
"""#281 wrap — build `_CARRIES.md` § `## residual → #282` from § `## residual → #281`.

ONE programmatic pass, the #261…#280 shape:
  (a) every age bracket bumped by one — `[NEW — 0…]` → `[1…]`, `[N…]` → `[N+1…]`;
  (b) ★ ONE surgical edit carrying its `s183-D1`/`s188-D2` receipt: #280's ① (the orphan census
      export "HAS NOT ARRIVED") — it ARRIVED at 11:02Z and was enacted across five lanes. Struck,
      never re-typed; what survives the strike is carried as a NEW item rather than left inside it;
  (c) the session's SEVEN new items written in front, newest first.
⛔ Nothing is dropped, re-worded, re-ordered or truncated. `s225-D2` clause (i).
⚠ NOT re-minted: the eye-check of the six cells (already item ② of this set, ageing to [1]), the
  logo review (item ④ at [3] → [4]), `s277-D12` (→ [2]), the `#243` not-a-wrap form, the four
  `_HANDOFF-130` items. The age bracket is what carries a repeat, never a second copy.
"""
import os, re, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
CARRIES = os.path.join(ROOT, "_CARRIES.md")
sys.path.insert(0, os.path.join(ROOT, "knowledge"))
import _capture_gate as cg  # the ONE definition of "a carry"

text = open(CARRIES, encoding="utf-8").read()
src = [l for l in text.split("\n") if l.startswith("> **residual → #281:**")]
assert len(src) == 1, len(src)
src = src[0]
before = len(cg._carry_items(src))

# ---- (a) ages -----------------------------------------------------------------------------
n_new = len(re.findall(r"\[NEW — 0(?=[,\]])", src))
aged = re.sub(r"\[(\d+)(?=[,\]])", lambda m: "[%d" % (int(m.group(1)) + 1), src)
aged = re.sub(r"\[NEW — 0(?=[,\]])", "[1", aged)
assert "[NEW — 0" not in aged

# ---- (b) the ONE surgical edit -------------------------------------------------------------
OLD1 = "⬛ **① THE ORPHAN CENSUS EXPORT IS HIS, TEN RADIOS, AND IT HAS NOT ARRIVED — #281'S FIRST MOVE** [1, DAVE'S]"
NEW1 = ("~~⬛ **① THE ORPHAN CENSUS EXPORT IS HIS, TEN RADIOS, AND IT HAS NOT ARRIVED — #281'S FIRST MOVE** [1, DAVE'S]~~ "
        "⛔ **STRUCK AT THE #281 WRAP — THE EXPORT ARRIVED AND WAS ENACTED; THE STRIKE CARRIES ITS RECEIPT "
        "(`s183-D1` strike, `s188-D2` receipt).** The claim below — that the census export had NOT arrived — was "
        "TRUE when written at the #280 wrap and is FALSE now. **It arrived at 11:02Z as ELEVEN radios, not ten, "
        "every one of them on the recommendation** — `notes/_lanes/281/orphan-plan/DAVE-EXPORT-2026-09-17.json` — "
        "and the census became the ORPHAN PLAN (`notes/_lanes/281/orphan-plan/`, conductor `2904db0`). "
        "**FIVE LANES ENACTED IT AND SIX RULINGS CAME OUT OF IT** (`s281-D1`…`s281-D6`, `knowledge/_rulings.json` "
        "607 → 613): the dark-dot count went **157 → 108 → 8** across explorer 1.21 → 1.25 (CM `06e28bb` · PH "
        "`b95042c` · RO `ea2c87e` · FO `fd85bbe` · TV `d23aed9` · RL `7f714f0`). His five decision questions "
        "followed at 11:58Z — all (a) — and his own words closed them: *\"Okay these all look good to me, thanks "
        "for the explanation\"*. Correction inscribed at: `knowledge/_rulings.json` §§ `s281-D1`…`s281-D6` · "
        "`notes/_lanes/281/DAVE-RULINGS-2026-09-17.md` · `_HANDOFF-132-the-orphan-plan-and-the-brain-learns-why.md`. "
        "⚠ **WHAT SURVIVES THE STRIKE IS CARRIED AS NEW ITEMS RATHER THAN LEFT INSIDE A STRUCK ONE: the 15 rule "
        "notes (item ① below) and the six lanes' own open questions (items ②–⑦ below).**")
assert aged.count(OLD1) == 1, ("strike anchor 1", aged.count(OLD1))
aged = aged.replace(OLD1, NEW1, 1)

# ---- (c) the session's SEVEN new items -----------------------------------------------------
NEWITEMS = [
 "⬛ **① THE 15 RULE NOTES ARE HIS, AND THEY ARE #282'S FIRST MOVE** [NEW — 0, DAVE'S] — put to Dave at "
 "the wrap call and NOT answered. `s281-D6` rules that **a note about the rule is not a rule edit**, so lane "
 "RL filed his rule-refinement notes rather than enacting them: **`notes/_lanes/281/rests-on-land/"
 "RULE-NOTES-2026-09-17.md`, 15 rows**, each carrying his note VERBATIM, the rule's stored text, and one "
 "sentence on what would change if it were inscribed. **13 rows argue with the rule itself** (rows 1–13) and "
 "**2 ride on a \"both 1 and 2\" answer whose link half is already landed as edges** (`col26-016`, `neuro-026`, "
 "rows 14–15, the difference named in the file). A sixteenth, `type26-003`, is filed at the foot as a "
 "borderline and is NOT landed. ⛔ **Nothing in that file has been inscribed and no guideline file has been "
 "changed** — every row is a question for him, one at a time, and enacting any of them is a guideline edit "
 "plus a regen of `_rules-index.json`. Receipt: `notes/_subreports/2026-09-17-281-RL-rests-on-land.md` · "
 "`7f714f0` · `notes/_lanes/281/rests-on/DAVE-EXPORT-2026-09-17.json` (14:49:41Z, 59 cards).",

 "⬛ **② WHERE IS AN OBLIGATION ON A UX PRINCIPLE DRAWN? — LANE CM'S QUESTION, AND LANE PH MADE IT CHEAPER** "
 "[NEW — 0, DAVE'S] — put to Dave at the wrap call. The **14 `obeys` → `ux:` lines are HELD, not dropped**, "
 "and explorer 1.21 says so on the page. `s277-D8` fixed Design governance at **three** provenances (WCAG "
 "`sc:`, HSBC `rule:`, the rulings a design cites) and a `ux:` target is none of the three, so drawing them "
 "is a ruling and not a lane's call. CM's options, his: **(a)** a FOURTH provenance sub-chip inside the "
 "obligation box — one chip, but it reopens a count he settled at three; **(b)** draw them in **Explanation**, "
 "where the `ux:` node already lives; **(c)** leave them held and permanently declared. ⚠ **`s281-D1` MOVED "
 "THE GROUND UNDER THIS QUESTION AND THE PRICE CHANGED:** 32 family nodes and 85 new dots put the Explanation "
 "view within reach and `EON` now reads an edge's own `fam`, so **(b) is cheaper than when CM priced it — the "
 "14 lines could carry a family without a new chip.** CM recommended (a), PH recommends the conductor "
 "re-put the question with the new price. Receipts: `notes/_subreports/2026-09-17-281-CM-chip-map.md` "
 "§ RULING-SHAPED 1 · `notes/_subreports/2026-09-17-281-PH-principles-home.md` § RULING-SHAPED 3.",

 "⬛ **③ FORCE BY GRADE, AND THE GHOST LAYER'S COLOUR — TWO LANES MET THE SAME TWO QUESTIONS AND NEITHER "
 "RULED** [NEW — 0, DAVE'S] — put to Dave at the wrap call. **(a) DOES FORCE FOLLOW GRADE?** `s281-D4` "
 "DELIBERATELY DOES NOT RULE IT — whether a high-graded principle binds a design that has not cited it. TV "
 "left it until `restsOn` had an export; that export has now arrived and landed (65 edges, `7f714f0`), so "
 "**the precondition TV named is met and the question is live**. Its shape if ruled: a second, DERIVED "
 "sub-chip beside the authored one, dashed, because it would be inferred and not authored. **(b) DOES THE "
 "GHOST LAYER FOLLOW THE DRAWN FAMILY OR THE STORED ONE?** 1.24 answers *the drawn family* by implication "
 "(75 px) and 1.25 met the bigger version of the same question (**42,192 px** of default canvas in off-chip "
 "`restsOn` ghosts). **Both lanes recommend AS SHIPPED**, and both say the same thing: **one line "
 "(`EDRAWF` → `EFAM`, or `if(ROC(e))continue`) freezes the default canvas byte-for-byte if he wants it**, "
 "and a general ruling on the ghost layer would settle it for every family still to land. Receipts: "
 "`notes/_subreports/2026-09-17-281-TV-theory-view.md` §§ RULING-SHAPED 1–2 · "
 "`notes/_subreports/2026-09-17-281-RL-rests-on-land.md` §§ RULING-SHAPED 1–2.",

 "⬛ **④ THE TWO UNTIED GOVERNANCE ARTEFACTS, AND WHETHER A REPO TOOL DESERVES A FAMILY OF ITS OWN** "
 "[NEW — 0, DAVE'S] — put to Dave at the wrap call; row **`W-281fo`**, open, closes on his word. `s281-D2` "
 "gave the guideline family its double-named files and lane FO tied **14** (not the brief's 3) and re-homed "
 "**5**, taking census set 06 from **24 → 0**. Two things it deliberately did NOT do: **(a)** "
 "`knowledge/_rules-index.json` and the bare directory `knowledge/guidelines/` are named by RULINGS ONLY and "
 "stay untied — reading *every* path under `knowledge/guidelines/` as the guideline family's is a SECOND "
 "ruling, and it needs an answer for the dark dot it would create, since their only line is a `governs`; "
 "**(b)** **9 of the 14 tied files are validators and builders** sitting in the Constitution because a ruling "
 "names them — true but thin, since the rule index names them as enforcement too. **There is no \"tools\" "
 "family and no chip for one**; the tie is recorded on each node, which FO calls the honest holding position. "
 "⚠ A THIRD kind arriving is a question by construction — the kind map is two rules long and the builder "
 "PRINTS an unmatched kind rather than deciding. Receipt: "
 "`notes/_subreports/2026-09-17-281-FO-file-owner.md` § RULING-SHAPED 1–3 · `fd85bbe`.",

 "⬛ **⑤ THREE ASKs AND ONE BORDERLINE OUT OF THE 59-CARD EXPORT** [NEW — 0, DAVE'S] — put to Dave at the "
 "wrap call; every one of them is HIS own note asking for a conversation, landed as an edge and flagged "
 "rather than quietly resolved. **`col26-012`** — *\"I'm actually not sure about this.\"* His link "
 "(`pr-nng-consistency`) IS landed and the doubt is carried on the edge. **`aid-009`** — *\"maybe we need to "
 "discuss.\"* His link (`pr-fitts`, grade A) IS landed; the note underneath it is that the rule is **\"too "
 "boolean\"**, which is a RULE conversation and not a link one. **`type26-002`** — *\"I think 1 is also "
 "applicable.\"* Landed **BOTH ways** under `s281-D6` (`restsOn` is many-to-many; his \"both\" lands both), "
 "with a null AND option 1, and the ASK is whether that is what he meant. ⛔ **AND ONE BORDERLINE IS NOT "
 "LANDED: `type26-003`** — its note reads *\"linked to 2 as you stated\"*, which RL read as agreement and not "
 "a second link, and declined to infer. Receipt: `notes/_subreports/2026-09-17-281-RL-rests-on-land.md` "
 "§ the three ASKs + the borderline · `notes/_lanes/281/rests-on-land/RULE-NOTES-2026-09-17.md`.",

 "⬛ **⑥ `gen_kg_rules.py` WOULD DELETE ALL 73 HAND-AUTHORED `restsOn` LINES, AND `inFamily` IS READ BY NO "
 "VERB** [NEW — 0, DAVE'S] — named, not fixed, by the lanes that found each. **(a) THE FOOTGUN IS LIVE.** "
 "`knowledge/_rule_nodes.json` says *\"regenerate with `gen_kg_rules.py --land`; never hand-edit\"*, and the "
 "`restsOn` block is hand-authored **by ruling** (`s281-D3`, `s281-D6`). The file's `$description` now says "
 "so and names the idempotent re-lander, but **the generator itself was not on RL's file list and is "
 "unguarded** — one preserve-block in that generator is the honest fix. **(b) TWO EDGE TYPES HAVE NO "
 "READING.** `inFamily` (145 edges, `s281-D1`) is read by no verb at all, and `evidencedBy`'s existing verb "
 "now lies to half its edges after gaining a second family. PH's options: **(a)** `inFamily` joins ***is-a*** "
 "and `evidencedBy` gains a `$splits` branch by family — the `obeys` split is the precedent and the machinery "
 "exists, ~20 lines; **(b)** an `unread` note on each, a declared gap rather than a reading; **(c)** leave "
 "both silent. PH recommends (a): **a reading map that misreads is worse than one with a declared hole.** "
 "`knowledge/_kg_verbs.json` is `s277-D11`'s and was in neither ruling's `governs`, which is why no lane "
 "touched it. Receipts: `notes/_subreports/2026-09-17-281-RL-rests-on-land.md` § RULING-SHAPED 3 · "
 "`notes/_subreports/2026-09-17-281-PH-principles-home.md` § RULING-SHAPED 1.",

 "⬛ **⑦ THE SANDBOX REFUSES `unlink` UNDER THE MOUNT, AND A GATE-FAILED COMMIT RUN CAN LEAVE "
 "`.git/index.lock` BEHIND — A RUNBOOK LINE IS OWED AND IT IS HIS** [NEW — 0, DAVE'S] — put to Dave at the "
 "wrap call. Lane CM MEASURED it at its own seat: **`rm`, `mv` and `os.remove` all return `Operation not "
 "permitted`** under the FUSE mount by default, so a seat that cannot delete cannot clear a lock it did not "
 "make. ⛔ **The consequence is the one worth a line: a commit run that a gate REFUSES can leave "
 "`.git/index.lock` in place, and the next seat meets a repository that looks corrupted when it is merely "
 "locked.** ⚠ This is a SEAT-LIMIT observation and a repair recipe, not a defect in any script — which is "
 "exactly why it is a runbook line rather than a quiet fix, and **amending `_RUNBOOK-git-commit.md` or "
 "`_RUNBOOK-capture-ritual.md` is Dave's word** [[premise-ages-faster-than-rule]]. Receipt: "
 "`notes/_subreports/2026-09-17-281-CM-chip-map.md` § UNPROVEN / CLAIMED, the DECLARED obstacle line · "
 "`06e28bb`.",
]

body = aged[len("> **residual → #281:** "):]
newline = "> **residual → #282:** " + " · ".join(NEWITEMS) + " · " + body
after = len(cg._carry_items(newline))
print("carries: before %d (of which %d were [NEW — 0]) → after %d ; new items %d"
      % (before, n_new, after, len(NEWITEMS)))

SECTION = "## residual → #282"
assert SECTION not in text, "section already exists"
anchor = "## residual → #281"
i = text.index(anchor)
text = text[:i] + SECTION + "\n\n" + newline + "\n\n" + text[i:]
open(CARRIES, "w", encoding="utf-8").write(text)
print("WROTE", CARRIES)
