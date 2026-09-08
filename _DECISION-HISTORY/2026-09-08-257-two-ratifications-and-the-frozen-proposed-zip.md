# #257 — two ratifications in one day, and the gate that refused the first one's re-bake

provenance: 257 · 2026-09-08
status: observed

*Spine: `_LIVE-STATE.md` ⏱ LATEST DELTA #257 · banner: `GOOD-MORNING.md` ★ LATEST #257 ·
ledger: `knowledge/_rulings.json` § `s257-D1`, § `s257-D2`, § `s257-D3` (entries 396/397/398) ·
filed report: `notes/_subreports/2026-09-08-257-wrap.md`. This file holds the WHY and HOW; the
WHAT is in those. Both-way links, per `_DECISION-HISTORY/README.md`.*

---

## The session opened to do one thing and did none of it

#257's stated job was **dashboards one-shotable** — the cold run of the frozen prompt against a
dashboard. It was never run. Two ratifications and a frozen-ledger finding took the whole window,
and the conductor's FILL reached **216,975 real**, 66,046 past the 150,929 advisory and past the
200,000 wall. That is the first thing a cold reader should know, because everything below is what
the window was spent on instead, and none of it was planned.

## Finding 1 — the ratification that was one word, and the lock that was zero bytes

Dave's opener answer was **"ratiify."** (sic). Under `s223-D3`/`s228-D1` that is a *ratifying*
word, not the authorisation that names a cut, so it was inscribed as `s257-D1` and
`RATIFY_IDS['v1.0.6']` was keyed **directly** rather than at the next cut — the usual route —
because `dist/` did not match the manifest and the pack had to be re-baked from the ratified
surface. The manifest regenerated RATIFIED at `1f4c35587f30` (1,673 files, 43,160,016 B).

The commit then failed on a **0-byte `.git/index.lock`**. Zero bytes is the diagnostic: a live
writer holds a lock with content in it, so an empty one is a dead session's residue. Runbook step
0 covers exactly this; `mcp__cowork__allow_cowork_file_delete` was granted and `rm` cleared it.
Commit `367be6d`. `--release` then baked `dist/Apollo-Spider-v1.0.6.zip` at sha256 `4781994f…`,
**byte-identical to #256's dry-run**, and `_gate_release_audit.py --pack` went **RED → PASS**
(`2b781c9`). That equality is the point of a dry run and it was reported rather than assumed.

## Finding 2 — the frozen gate went red, and it was right about a defect seeded at #245

Immediately after the bake, `knowledge/_release/_gate_frozen_release.py` refused:
**`RE-RECORDED WITHOUT A VERSION BUMP`** — recorded `398c695a`, measured `85f4f4db`.

The instinct in this situation is to treat a gate that reddens on a correct-looking action as
lagging its subject. It was not. The root cause is twelve sessions old: **#245 seeded a
*PROPOSED* zip into the frozen ledger.** Once a proposed artefact is recorded as frozen, re-baking
at the same version replaces a proposed hash with a ratified one under a single ledger key — which
is precisely the laundering the frozen ledger exists to prevent. ★ **The gate was reading its own
rule correctly against a subject that had been admitted wrongly.**

⛔ Two remedies were available and only one of them is honest. Re-seeding the ledger at v1.0.6
would have made the red go away by rewriting the record the gate protects. **A version bump does
not** — it leaves the #245 row untouched and gives the ratified artefact its own key. The bump was
recommended to Dave in one line.

⬛ **Ruling-shaped and still his:** should `--seed` REFUSE a PROPOSED surface outright, or should
the birth clause admit a PROPOSED → RATIFIED transition at one version? The bump made the question
non-blocking, which is exactly the condition under which a design question stops being asked. It
is priced and carried on `→ #258`, not taken.

## Finding 3 — the demo audience was wrong in the record, and it had a home

Mid-session Dave asked: *"where do you get the idea that this has anything to do with Sutherland?
The demo is to David Rice at HSBC"*.

The wrong belief was not a slip in chat. It had an inscribed home:
`_DECISION-HISTORY/2026-09-05-246-the-library-dictates.md` **L31** wrote "the Sutherland demo" as
an **inference** — Sutherland is HSBC's React library, i.e. a *subject* of the demo and never its
audience — and nothing between #246 and #257 tested it. ★ **The general form: an inference written
into a dated home reads, one session later, exactly like an observation.**

✅ The correction was made **BY ADDITION**: L31 stands, with a ⚠ CORRECTED block above it. A dated
dossier lands whole and is never silently edited (`_DECISION-HISTORY/README.md`), and a struck-out
wrong claim beside its correction is more useful to a cold reader than a tidy file.

Research (HSBC media release 23 Mar 2026 · Banking Dive · Disruption Banking · HSBC USA 2020)
established **David Rice as HSBC's first Chief AI Officer from 1 April 2026**, previously COO of
Commercial & Institutional Banking, ~20 years in the bank. ★ **He is an operator, not a platform
owner** — CTO Shamtani owns the model platform — which changes what a demo to him should lead
with. Prep note: `notes/_DEMO-PREP-david-rice-hsbc.html` (swiss, ~6 KB), commit `992699b`.
⬛ Three questions in it are his: who else is in the room, what the ask is, and HSBC's
external-LLM constraint.

## Finding 4 — v1.0.7, and a premise that was checked instead of assumed

`s257-D2` — *"Cut 1.0.7 can you prepend ADS- to the skill names so they are easy to spot in a
list"* — is an authorisation, not a ruling on the release. It was read as `name:` in SKILL.md on
six pack skills plus 25 in-skill cross-references. ★ **Directories were left alone, and that was a
CHECKED premise: no gate binds a skill's `name:` to its directory.** Had that not been checked, a
directory rename would have been either an unnecessary risk or a missing half.

The version story took the **#245 shape** — `VERSION` + `MEMENTO_CUT_VERSION` to v1.0.7 with the
four carried literals (`FIRST-SESSION.md`, the gumdrop `_state.json` `built_by`, two gumdrop
runbook headers). Generator selftest 216/216. Cut commit `b9c4c80`. Probe 41 RUNNABLE / 9
REPO-BOUND / 4 NEEDS-DEP; manifest 1,673 files, 43,162,006 B; dry-run zip `13a593de1b11…` (20 MB),
`--check` GREEN, `--manifest-check` PASS. ★ **`ADS-grill-me` was verified INSIDE the zip rather
than inferred from the tree** — the rename's whole purpose is what a reader sees in a list, and
the shipped artefact is the only place that can be observed. `540c7ec`, PROPOSED.

On *"ratify"* (`s257-D3`): RATIFY_IDS keyed, the frozen-ledger literal moved v1.0.6 → v1.0.7,
manifest RATIFIED (`dbf4d0a`), `--release` → `dist/Apollo-Spider-v1.0.7.zip` at `13a593de…`,
byte-identical to the dry-run (`a4bf8c2`), `--seed` → apollo-spider row v1.0.7, 7 files,
`9431a8f6a707` (`82b310c`). Frozen PASS on all three arms · `--pack` PASS at `b9c4c802439c` ·
`--drift` clean. **Pushed `71ab931..82b310c`, verified.**

## Finding 5 — the boot ceiling fell, one session after the cut that moved it

Boot at #257's first turn read **68,837 real** — 1,163 under the 70,000 shrink-only ceiling and
1,404 below #256's 70,241. ★ **This is #256's `MEMORY.md` stub cut measured at last.** #256 said
in its own wrap that the cut could not move a figure taken at the first turn of the session that
made it, and that #257's opener would be the reading. It was, and it landed where predicted.

⛔ **The arm still refuses, and it is right to.** Its clause is *every* post-breach reading under
the ceiling; #255's 70,127 and #256's 70,241 both stand over it. The literal was **not moved** —
shrink-only under `s240-D2`/`s241-D1`, and raising it is never a price a wrap pays to unblock
itself. The `--wrap` commit form is refused for the **eleventh** wrap running and the commit is
made in the #243 form. ⬛ What to do with the arm now is Dave's, and it is a smaller question than
it was yesterday, because the remedy the arm itself names has now been shown to work.

## Finding 6 — a seam-less run is how a seat reaches 216,975

`knowledge/_checkin.py` ran at the opener and at the end, and **not once at the seams between the
three cuts**. ★ **Release work is many small measured steps, each individually cheap, so the seat
feels busy rather than full** — the same mechanism #255 named for lane replays, in a different
shape. The FILL was therefore *discovered* at the brief cut rather than watched, at 66,046 past
the advisory. The harness reported far more room; ⛔ the ruled unit wins, and it is stated rather
than argued.

## Resolved state, and what is still open

**Resolved:** v1.0.6 and v1.0.7 are both RATIFIED and shipped; `dist/` holds seven zips; the
apollo-spider frozen row reads v1.0.7; every release gate is green; the tree is pushed. The demo
audience is corrected in the record. The boot index cut is measured.

**Open, and Dave's:** the cold run of the frozen prompt (the day's stated job) · his rulings page ·
whether the skill *directories* take the `ADS-` prefix too · the frozen-ledger birth-clause
question above · the boot-ceiling arm now that a cut has been proven to work · the three demo-prep
questions · and the standing set carried at `_CARRIES.md` § `residual → #258`.
