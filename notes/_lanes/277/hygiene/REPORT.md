# LANE CH — HYGIENE — #277 · 2026-09-15 · model: opus

CV's `notes/_lanes/277/verify/VERIFY.md` items **9, 10, 11, 13, 14, 15** are this lane's. Items 1–8 and
12 are lane CP's; **nothing under `notes/_lanes/277/page/` was opened.**

```
item                                                     outcome
1  correct CO's §5 / §4 / §11 figures, by addition        DONE — CORRECTIONS.md C-1, C-2, C-3
2  correct CJ's blast radius, by addition                 DONE — CORRECTIONS.md C-4 (CV is right)
3  park the dv-019 index defect with a tripwire           DONE — P-277-1, tripwire proven firable
4  park the chart-meta capitalisation split               DONE — P-277-2, tripwire proven firable
5  stop _dry_run.py writing into the lane it audits       DONE — read-only by default; verdict identical
6  sweep the two stray files at repo root                 DONE — both deleted, both confirmed orphan first
7  report .git/_orphan-locks/                             DONE — 11 locks + tmp_obj/, nothing deleted
```

---

## 1 & 2 — the four corrected figures

In `CORRECTIONS.md`, beside the reports, not inside them. **Nothing in `notes/_lanes/277/charts/` or
`notes/_lanes/277/judgement/` was edited** except the one file item 5 names, and that is said plainly
below. Every figure was re-driven here rather than copied from `VERIFY.md` — this lane is correcting a
correction, and a wrong one is worse than none.

| # | where | as written | measured here | verdict |
|---|---|---|---|---|
| C-1 | `REPORT.md` §5 | "**11** of the 57 would be false" | **8** (57 cells, 49 binding, off CO's own `FAMILY` matrix) | CV right; 11 is CJ's number |
| C-2 | `REPORT.md` §4 | "12 of **139** metas" | **12 of 137** (138 files − 1 EXAMPLE; 139 is the gate's, +proforma +EXAMPLE) | CV right |
| C-3 | `REPORT.md` §11 | `b4d42eb` / `460 REPORT.md` | **`8c80aa2` / `482`** — `b4d42eb` is a real but pre-amend object | CV right |
| C-4 | `RECOMMEND.md` | "**29–50** files per component" | **114–159 tracked per component, 279 in the union**; knowledge/ only 27–42, union 78 | **CV right**, CJ is the knowledge/-only figure unqualified |

**One honest divergence from CV, declared:** my repo-wide counts are 1 higher (159/279 against CV's
158/278). CV measured before its own commit; `VERIFY.md` now names the seven stems, so it counts itself.
`git grep -l … | grep -c notes/_lanes/277/verify` = **1** — the entire difference. The `knowledge/`-only
union is **78 in both lanes**. Neither figure is wrong; they are two moments.

---

## 3 & 4 — the two parked rows

Appended to `knowledge/_parked.json` **by textual span**. The receipt is the diff, not the message:

```
$ git diff --numstat knowledge/_parked.json
34   0   knowledge/_parked.json          <- 34 added, 0 removed. A pure addition.
```

**0 deletions is the point.** A re-dump of this file would show hundreds of lines changed on both sides
and `--selftest` would still pass — the `#179` class, which no green gate catches.

### P-277-1 — the `dv-019` index defect

**Verified on disk before parking, all three files:**
- `knowledge/guidelines/_rules-index.json` — the `dv-019` row's `rule` field opens with **dv-017's**
  sentence (*"Only palette colours in charts … the unified supporting palette."*) and literally contains
  the other rule's tag, **`{#dv-017}`**, before the scoped-override prose.
- `knowledge/_rule_nodes.json` — `rule:dv-019`'s `text` carries the same wrong sentence. **In the graph.**
- `knowledge/_consult-index.json` — the `dv-019` entry too. **On the consult surface.**
- The true `dv-019` is `data-visualisation.md` clause (c) of that override block — *"NEW APOLLO-ADDED RULE
  — avoid vibrating boundaries … value-ratio <1.25 AND hue-sep ≥135° AND both HSL sats ≥0.5"*, tagged
  `{#dv-019}`. CO's diagnosis (the indexer takes the whole bullet from `-` to the closing `{#…}`) is
  consistent with what is on disk.

⚠ **A path correction the brief inherited from CV.** The generator is
**`knowledge/guidelines/gen_rules_index.py`** — under `guidelines/`. `knowledge/gen_rules_index.py`
**does not exist**; briefing a lane against that path would send it looking for a missing file. The row
says so in its own text. (`knowledge/gen_kg_rules.py` also writes this file, at line 392 — a second lane
brief should know there are two writers.)

Trigger: `file-changed` on `knowledge/guidelines/_rules-index.json`, `at_commit f6320b5` (the last commit
to touch it, 2026-08-21). Currently **WAITING** — correct: it becomes due the moment anyone regenerates
or splices the index, which is exactly when regenerate-vs-splice becomes Dave's live question and when a
naive regeneration would either re-emit the defect or fix it and leave the two derived surfaces stale.

### P-277-2 — the chart-meta capitalisation split

7 up / 7 down, both cases created by `df44e51` in one wave (re-confirmed by `--numstat`), the stem is the
node id, blast radius as C-4 measures it, two-step `git mv` required. Owner: **Dave** (whether to rename
at all); a lane once he rules. **Explicitly not this wave's work** — all three lanes refused it inside the
charts lane and all three were right.

Trigger: `event` `kg-edge-gen`. It has a consumer — `knowledge/gen_kg_edges.py:613` calls
`_parked.notice("kg-edge-gen")` — so it fires at every edge generation, which is the moment the node ids
are minted from the stems.

### Proof the tripwires can fire — the P-276-1 test, run not read

P-276-1 shipped last session with a tripwire that could **never** fire, and it was caught by *running the
door*. So both new rows were driven, and mutated:

```
P-277-1 as parked                                  -> (False, 'knowledge/guidelines/_rules-index.json unchanged since f6320b5')
P-277-1 MUTANT (at_commit -> 0678f7f, one touching-commit back)
                                                   -> (True,  '… changed in 1 commit(s) since 0678f7f')

P-277-2 as parked, plain --check                   -> (False, 'waits for the kg-edge-gen event')
P-277-2 at its own moment (--due kg-edge-gen)      -> (True,  'the kg-edge-gen event is now')
P-277-2 MUTANT (event renamed to never-happens)    -> (False, 'waits for never-happens')
```

Each row goes **red on the mutant and green at its moment**. A trigger that cannot go both ways proves
nothing; these go both ways.

```
$ python3 knowledge/_parked.py --selftest
[OK] a malformed item REFUSES at load
[OK] the real register loads and every item has a legal trigger
[OK] door has no write path
parked selftest: OK

$ python3 knowledge/_parked.py --check          (headline, then this lane's two rows)
PARKED DUE — 3 of 19 parked item(s) due
  … P-277-1 — THE dv-019 ROW IN _rules-index.json CARRIES dv-017'S SENTENCE. …
       knowledge/guidelines/_rules-index.json unchanged since f6320b5 · owner a lane, once briefed
       (the generator fix + the two derived surfaces); Dave (regenerate the whole index, or splice the
       one row) · parked 2026-09-15 #277
  … P-277-2 — THE CHART METAS ARE SPLIT ON CASE — 7 UP, 7 DOWN, FROM ONE WAVE. …
       waits for the kg-edge-gen event · owner Dave (whether to rename at all, and when); a lane of its
       own once he rules · parked 2026-09-15 #277

$ python3 knowledge/_parked.py --due kg-edge-gen
PARKED DUE — 1 of 19 parked item(s) due at kg-edge-gen
  ⏰ P-277-2 — … the kg-edge-gen event is now …
```

The register is **21 rows, 19 live** (P-274-2 and P-274-3 are `enacted`; rows are never deleted).

---

## 5 — `_dry_run.py` no longer writes into the lane it audits

**This is the one file under `notes/_lanes/277/charts/` that this lane edited, and it is said plainly
here because editing another lane's committed tree needs saying out loud.** It is CV's item 14 and the
brief names it explicitly. Nothing else in CO's lane was touched; `dry-run.json` and `dry-run.txt` are
byte-identical to CO's committed versions (md5 `b618226d…` / `e998c416…`, re-checked after every run
below).

**The defect, reproduced first** — as shipped, a second seat checking CO's receipt destroys it:

```
$ python3 notes/_lanes/277/charts/_dry_run.py
$ git status --porcelain notes/_lanes/277/charts/
 M notes/_lanes/277/charts/dry-run.json
 M notes/_lanes/277/charts/dry-run.txt
```

**The change.** Read-only by default; the write is opt-in:

```
_dry_run.py              # READ-ONLY: prints the audit, writes nothing
_dry_run.py --out DIR    # write dry-run.json / dry-run.txt into DIR (outside the audited tree)
_dry_run.py --write      # write back into the lane — the original behaviour, now explicit
```

Three edits, all local: the docstring, an `OUT_DIR` resolved from `sys.argv` where `OUT` used to be a
constant, and the final write block guarded by `if OUT_DIR is None`. **The four audit sections, the
figures, the negative controls, the simulated-tree run and the exit code are untouched.**

**Proved by running it before and after and diffing the verdict:**

```
BEFORE (as shipped)   VERDICT: OK   exit 0   + rewrote CO's two receipt files
AFTER  (default)      VERDICT: OK   exit 0   "read-only … nothing written"

$ diff <before> <after>          (the write line excluded, since that is the change)
25c25
<   changed paths: 6  ·  outside notes/_lanes/277/: 4
---
>   changed paths: 7  ·  outside notes/_lanes/277/: 4
```

**One line differs, and it is the audit working, not the audit changing.** §4 counts live `git status`
paths; my own in-flight edit of `_dry_run.py` is the seventh. Every other line — all three schema
validations, all four negative controls, the resolution block, the 81 / 29 / 110 dry-run figures, the
simulated `_validate_kg.py` exit, the ownership rows and `VERDICT: OK` — is byte-identical.

Both other arms driven: `--out /tmp/dr` wrote the pair there and left the lane clean; `--write` wrote
into the lane (original behaviour intact) and was restored with
`git restore --source=HEAD --worktree`; `--out` with no directory refuses (`--out needs a directory`).

⚠ **Found, not fixed:** the help gate at the top of `_dry_run.py` never engages. It walks *up* from the
lane looking for `_helpgate.py`, which lives in `knowledge/` — not an ancestor of
`notes/_lanes/277/charts/` — so `--help` runs the full audit instead of printing the docstring. Harmless
here and pre-existing; it means every lane script written under `notes/_lanes/` carries a help gate that
does nothing. Not this lane's to fix.

---

## 6 — the two strays, swept

Confirmed orphan **before** deleting, on all three tests the brief names:

```
size / md5        artefact  0 B   d41d8cd98f00b204e9800998ecf8427e   (the empty-file hash)
                  rule?    49 B   4919f39261aedefd24f9e5129c87681d
content of rule?  "--- does any edge type point component- or role-"
tracked?          git ls-files --error-unmatch artefact  -> "did not match any file(s) known to git"
                  git ls-files --error-unmatch 'rule?'   -> "did not match any file(s) known to git"
referenced?       git grep on the exact content string   -> 0 hits
                  git grep for either as a PATH          -> 0 hits
```

Both match CV's A-3 exactly (same sizes, same md5s), so nothing changed them between 21:33 and now. The
word "artefact" appears in tracked files — `"type": "artefact"` in `_rule_nodes.json`, a column header in
`apollo-spider/…/_encoder_home.py` — but **as a word in data, never as a path to this file**. The shell
redirect that made them is visible in the content: a here-doc question truncated at a `?` glob.

**Both deleted.** `git status --porcelain` now shows neither. The only untracked paths left are lane CJ's
`BRIEF.md` and lane CP's in-flight `notes/_lanes/277/page/`.

---

## 7 — `.git/_orphan-locks/` — reported, nothing deleted

**11 zero-byte lock files and one directory.** Every one is 0 B, so none holds content that could be lost.

```
HEAD.lock.1789500346                             19:47
HEAD.lock.20260915T213906.laneCJ-post            21:38
HEAD.lock.20260915T213917.laneCJ-amend           21:39
index.lock.1789500328                            19:49
index.lock.20260915T213854.laneCJ                21:26
index.lock.20260915T213916.laneCJ-status         21:39
index.lock.20260915T213922.laneCJ-final          21:39
index.lock.214425                                21:39
index.lock.laneIX-214459                         21:44
index.lock.stale-1836-moved-by-lane-TO-276       18:36
index.lock.stale-194705                          19:46
tmp_obj/                        directory, 72 entries, mtime 21:39
```

**What it says.** Five of the eleven are lane CJ's, from a seven-minute window (21:26–21:39) around its
commit-and-amend; one is lane IX's; one is lane TO's, from **#276** — this folder is accumulating across
sessions, not just today. The naming has drifted three ways (raw epoch `1789500346`, bare clock `214425`,
and the readable `20260915T213917.laneCJ-amend`), so only some rows say who moved them.

⚠ **`tmp_obj/` is the one worth a second look, and it is not a lock.** 72 entries, mtime 21:39 — the same
minute as lane CJ's last lock. Git's own `.git/objects/tmp_obj_*` files are *unreferenced loose objects*
left when an object write is interrupted; a directory of 72 of them moved in here alongside the locks
suggests a `git gc`/write interruption, not a stale lock. It is untouched, as instructed.

**Nothing deleted. Nothing opened.** This is a report, and the folder's growth across two sessions is
ruling-shaped — whether `.git/_orphan-locks/` is a permanent midden or something a wrap should empty is
not a lane's call.

---

## Ownership and gates

```
$ git status --porcelain            (before this lane's commit)
 M knowledge/_parked.json                    <- this lane, +34 / -0, textual span
 M notes/_REHEARSAL-LOG.jsonl                <- harness, not mine (also CV's A-2)
 M notes/_dream/_GRADE-DECISIONS.jsonl       <- harness, not mine
 M notes/_lanes/277/charts/_dry_run.py       <- this lane, item 5, declared above
?? notes/_lanes/277/judgement/BRIEF.md       <- lane CJ's
?? notes/_lanes/277/page/                    <- lane CP's, in flight — NOT OPENED
?? notes/_lanes/277/hygiene/                 <- THIS LANE
```

`artefact` and `rule?` are gone from this listing — that is item 6's receipt.

No `git stash`. `gen_kg_edges.py` and `_build_all.py` were never run. No `.git/index.lock` was
encountered and nothing in `.git/_orphan-locks/` was touched. Lane CP was running in parallel throughout;
this lane committed once, serially, and wrote nothing under `notes/_lanes/277/page/`.

## The commit

One commit. **`git show --numstat` from the shipped sha is the receipt, never the message** — and per C-3,
this lane quotes **no sha of its own**, because this block is spliced in before the commit exists and any
sha written here would be the exact defect C-3 corrects.
