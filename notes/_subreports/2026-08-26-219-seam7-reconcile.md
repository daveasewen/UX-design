# #219 seam 7 — the release reconcile: three lanes landed, three cross-lane fixes made, stage 1 of 2

**Lane:** seam 7 (reconcile), #219 designer-pack-v3 build · **Model:** Opus · **Date:** 2026-08-26
**Charter:** `s219-D4` (read verbatim from `knowledge/_rulings.json`, which is itself the object
being verified this seam — see § RECONCILE ③)
**Reconciles:** base `71bb2f7` + conductor telemetry + lanes R1, R2, R3 (R1 first; R2 and R3
concurrently)
**Read first, as briefed:** `s219-D4` · `notes/_subreports/2026-08-26-219-R1-v3-manifest.md` ·
`…-R2-release-ci.md` · `…-R3-skills.md`
**Stage:** ⚠ **STAGE 1 OF 2. NOTHING COMMITTED, NOTHING PUSHED.** Stage 2 (bake the manifest and
the page at the landing commit) waits on the conductor sending that commit hash.

COUNTS: status lines reconciled **36** · unclaimed **0** · paths inherited **27** · paths added by
this seam **9** · authorised fixes declared **3** (+1 consequential, declared) · verdicts driven
**21** · new selftest bites added **24** · mutations driven **4** · store rows minted **1**

---

## ① THE RECONCILE — 36 lines, 0 unclaimed

Every line of `git status --porcelain -uall`, attributed. Nothing is attributed by guess: each
lane's own filed report names its files, and the two store-shaped files were verified structurally
before being included (§ ③).

### Inherited — 27 lines

| # | path | owner | evidence |
|---|---|---|---|
| 1 | `.github/workflows/gates.yml` | **R2** | R2 "What landed": EDITED, correction-log entry + `release` job |
| 2 | `.gitignore` | **R1** | R1 "What landed": EDITED, one stanza, the `dist/` zip exception |
| 3 | `knowledge/_build_all.py` | **R2** | R2: 8 STEPS + 8 ROUTE_ROWS |
| 4 | `knowledge/_rulings.json` | **conductor** | the `s219-D4` inscription — verified, § ③ |
| 5 | `knowledge/_state.json` | **R1·R2·R3** | 7 rows, 2+3+2, matching the three reports — verified, § ③ |
| 6 | `notes/_receipts/2026-08-25-219-role-defaults-exports.md` | **conductor** | telemetry: Dave's parked capsule-chord correction, `s219-D4(6)` names this file |
| 7 | `designer-skills-v3/build-designer-pack.sh` | **R1** | R1: NEW, the build |
| 8–10 | `designer-skills-v3/ci-template/{README.md,gates.yml,run-gates.py}` | **R2** | R2: the pack-side template, three files |
| 11–15 | `designer-skills-v3/skills/{check-against-design-system,check-with-gates,draft-a-new-pattern,generate-from-canon,usability-review}/SKILL.md` | **R3** | R3: five `SKILL.md`, four refreshed + one new |
| 16–19 | `knowledge/_release/{_frozen-releases.json,_gate_ci_template.py,_gate_frozen_release.py,_gate_release_audit.py}` | **R2** | R2: the freeze gate, its seeded ledger, the two audits, the template gate |
| 20–22 | `knowledge/_release/{_gen_v3_manifest.py,_v3_gate_probe.json,_v3_manifest.json}` | **R1** | R1: the generator + its two generated artefacts (R2 edited the generator, declared in R2's own table) |
| 23–25 | `notes/_subreports/2026-08-26-219-{R1-v3-manifest,R2-release-ci,R3-skills}.md` | **R1·R2·R3** | the three filed reports, `s218-D7` |
| 26–27 | `reviews/RELEASE-V3-MANIFEST-2026-08-26-v1{,.REVIEW}.html` | **R1** | R1: Dave's go/no-go page + its review pair |

### Added by this seam — 9 lines

| # | path | why |
|---|---|---|
| 28–34 | `knowledge/_render/verify_{behaviour_218w3_media,behaviour_218w3_nav,behaviour_218w3_overlay,phantom_surfaces_218,wave3_alpha_218,wave3_beta_218,wave3_gamma_218}.py` | fix (c) — the help-gate red, fixed at cause |
| 35 | `_CHAIN.md` | REGENERATED, not edited — it was STALE because the lanes' seven store rows moved it |
| 36 | `notes/_subreports/2026-08-26-219-seam7-reconcile.md` | this report (`s218-D7`) |

**UNCLAIMED: none.** Every one of the 36 lines resolves to a lane, to conductor telemetry, or to
this seam. No path required investigation beyond reading the reports.

### ⚠ One attribution worth stating plainly

`knowledge/_release/_gen_v3_manifest.py` is **R1's file with R2's edits and now seam 7's**. Three
authors, one untracked path, one line of `git status`. It is attributed to R1 above because R1
created it, but the conductor should not read that line as "R1's work" when reviewing the diff —
there is no diff to read, it is untracked and lands whole.

---

## ② THE THREE AUTHORISED FIXES — each is another lane's file, each declared

Every fix below is **mechanical**: it enacts something a filed report explicitly asked for. None
decides anything taste-level. Where a lane asked for a decision, the decision was turned into a
question on Dave's surface (fix b) rather than taken.

### FIX (a) — the skills group points at v3, not v2 · R1's file · **requested by R3 Q1**

R3's Q1: *"Until this changes the pack ships v2's four skills and none of mine."* Four lines were
named. ⚠ R2's finding 7 warned the cited **line numbers had already rotted** — R2's three
generator additions shifted them. So all four targets were **re-derived by name**, not by number,
and the numbers R3 gave were not used:

| R3's cited line | actually found at | what changed |
|---|---|---|
| `:284` the `match` lambda | `:288` | `designer-skills-v2/` + `/SKILL.md` → `designer-skills-v3/skills/` + `/SKILL.md` |
| `:1251` the selftest bite | `:1305` | the pinned probe path repointed, and `check-with-gates` added beside it |
| `:719-724` the `placeholders` block | `:741` | removed — the slot is filled |
| `:194` / `:899-903` the prose | `:194` / `:920` | the EXCLUDED reason and the page's skills lead rewritten |

**The name: `check-with-gates` wins**, per the brief — R3's shipped name beats R1's
`run-apollo-gates` placeholder. Recorded as a fact, not re-litigated: R3's reasoning (the pairing
with `check-against-design-system` is the pedagogy) is in its report and the conductor's brief
settled it.

**Proved in both directions, which the original bite could not do.** The old bite only asserted
that *some* group claims a v2 SKILL.md — it would have stayed green if the match had widened to
claim **both** v2 and v3. A second bite now asserts v2's `SKILL.md` is claimed by **nobody**
(v2 is a frozen release, `s114-D4`). Mutation M4 below drives it.

### FIX (b) — the FIFTH CARD on Dave's go/no-go page · R1's file · **requested by R2 Q1, seconded by R3 Q6**

Two lanes reached the same finding from opposite ends and both asked for a card. R2: *"he is
currently being shown '39 gates that run away from this repo' with no mention that four of them
arrive red."* R3: *"a designer who unzips, runs the runner as both R2's README and my skill tell
them to, and is met with 665 violations they did not cause will conclude the gates are noise — on
day one, permanently."*

`Q5` added to `OPEN_QUESTIONS`. The four gates are stated **by name with a one-line cause each**:

| gate | the cause, one line |
|---|---|
| `_validate_evidence.py` | exits 2 — bad arguments, not a verdict; it needs a rows file and the pack's runner gives it none |
| `_validate_token_forks.py` | three token forks are not in the ledger |
| `_validate_type_blast_radius.py` | one selector, `.search input`, escaped its declared radius |
| `_validate_type_composites.py` | 664 composite violations in the pack, 1,091 in this repo — the standing type-composite debt |

⚠ **The 664/665 discrepancy, resolved rather than averaged.** R2 measured **664** in the pack; R3
measured **665**. They are not in conflict: R3's walk-8 stage carried R3's own planted tranche file
(`knowledge/_proforma/status-tile.html`), which R3's own report records as tripping `TYPE-001`.
664 is the clean pack figure and is what the card states. [[measure-dont-convert-units]] — the
figure carries its population, not just its number.

The three dispositions are presented **as Dave's choice**: fix-before-bake · ship with the
baseline switched on (R2 built `--baseline` and deliberately left it unwired) · ship red and
documented. **The card decides nothing** — and that is enforced, not merely intended: the page
renderer paints a `recommended` flag on any option whose text carries the word, and a bite asserts
no Q5 option carries it. Mutation M2 drives that bite red.

**A typed count found one inch from where Dave rules.** The section heading was the literal word
*"Four things only you can settle"* while the list beside it was data. A fifth card would have left
the heading lying on his own decision surface — [[banner-figures-are-parsed-not-prose]] at the
worst possible location. Now derived from `len(open_questions)`; the rendered page reads **"Five
things only you can settle"** and the headline metric reads **5**.

### FIX (b′) — CONSEQUENTIAL, not requested, declared

Removing the `placeholders` producer left its **consumer** behind — a renderer looping
`entries[0].get("placeholders", [])`. That is not harmless, and it was not reasoned about, it was
**measured**: rendering the new generator against the *stale* manifest still on disk painted
**"Empty slot, named: PLACEHOLDER — R3 writes it"** onto Dave's page, for a skill that exists.
A consumer that outlives its producer keeps telling the old story to whoever feeds it old data.
Removed. Re-driven against the same stale manifest: `Empty slot, named` **absent**, `PLACEHOLDER`
**absent**, `run-apollo-gates` **absent**.

### FIX (c) — the help-gate red, fixed at cause · #218's files · **named by R2 as pre-existing**

R2 flagged it and correctly disclaimed it: `_validate_help_gate.py` → exit 1, **7 findings**, all
seven `knowledge/_render/verify_*_218*.py`, all tracked at HEAD since `941c92d` (2026-08-25). It
is `ABORT`-routed in `_build_all`, so a full build stops there **before** any release step is
reached — it would have blocked the landing commit's own build.

Fixed at cause, in those seven scripts, using **the pattern the sibling verify scripts already
use** (copied from `verify_segmented_219.py`, not invented): the six-line preamble placed
immediately after the module docstring, before any executable statement.

Applied by AST, not by regex — the insertion point is `body[0].end_lineno` where `body[0]` is
asserted to be the docstring, and the result is re-parsed before being written. **`git diff
--numstat` = 7 added / 0 deleted on each of the seven** — insertion-only, nothing re-ordered.

⚠ **One false positive, caught by the guard and worth recording.** The first pass refused
`verify_wave3_alpha_218.py` on a `'_helpgate' in src` check. The mentions were real but were the
script's **own body** copying sibling modules into a stage, not a preamble. The guard was narrowed
to the actual marker `_help_gate(__doc__`. [[unmatched-grep-is-not-an-absence]] in its mirror
form: a *matched* grep is not a presence either — the four files edited before the refusal were
correct, and the guard stopping the run is the guard working.

**Driven, not just gated.** The AST gate going green proves the clause, not the feature
[[mutation-tests-the-clause-not-the-feature]]. So all seven were **run with `--help`**:

```
verify_behaviour_218w3_media       rc=0  lines=28   verify_wave3_alpha_218   rc=0  lines=56
verify_behaviour_218w3_nav         rc=0  lines=31   verify_wave3_beta_218    rc=0  lines=58
verify_behaviour_218w3_overlay     rc=0  lines=45   verify_wave3_gamma_218   rc=0  lines=60
verify_phantom_surfaces_218        rc=0  lines=53
```

Each printed its own docstring and exited 0. **Tree assert after:** `git status -uall` showed only
the seven files themselves — no script wrote anything on the help path, which is the whole point of
the #158 class.

---

## ③ THE TWO STORE-SHAPED FILES — verified BEFORE inclusion

Both were checked structurally rather than by reading the diff, because a diff of a large JSON file
is not evidence of insertion-only.

**`knowledge/_rulings.json` — the conductor's `s219-D4`.** `+17 / -0`. Parsed both sides:

```
old 253 rulings · new 254 · added ['s219-D4'] · removed []
old entries byte-identical as a prefix of new: True
_README unchanged: True
```

⇒ **one appended object, insertion-only, no prior ruling touched.** Included.

**`knowledge/_state.json` — seven lane rows.** As inherited: `+126 / -0`, 252 → 259 items,
**0 removed**, every prior row byte-identical. The seven:

| id | owner | lane |
|---|---|---|
| `W-99zt` · `W-99zu` | dave | **R1** — the release machinery + manifest, and R1's filed report |
| `W-99zv` · `W-99zw` | claude · dave | **R3** — the five skills, and R3's filed report |
| `W-99zx` · `W-99zy` · `W-99zz` | claude · claude · dave | **R2** — repo-side CI, pack-side template, and R2's filed report |

⇒ `W-99zv/zw/zx/zy/zz` **intact**, R1's `W-99zt/zu` **intact**, nothing rewritten. Included.

**Final state after this seam's own row.** `+147 / −0`, 252 → **260** items:

```
removed : []          added : ['W-187','W-99zt','W-99zu','W-99zv','W-99zw','W-99zx','W-99zy','W-99zz']
CHANGED : NONE — every prior row byte-identical
old order preserved exactly within the new file : True        meta unchanged : True
```

⚠ **A naive prefix check calls this red, and it is not.** `W-187` lands at index **215 of 260**,
not at the end, because `_state.save()` sorts through the store's own `_sort_key`. "Old items are a
byte-identical *prefix*" is the wrong assertion for a store that sorts; the right one is
"no row removed, no row changed, relative order preserved" — which is what is quoted above, and
which the line-level `−0` corroborates independently.

**Store gates, driven after everything (including this report's own row):**

```
python3 knowledge/_state.py --selftest      → 57 bites, all GREEN
python3 knowledge/_gate_doc_rows.py         → population 86, unrowed 0 — PASS
```

⚠ **`W-99zz` exhausts the `W-99z*` scratch range** (`zo`…`zz` are all taken). This seam's own row
is therefore `W-187`, continuing the numeric sequence the previous reconcile seam used (`W-186`).
The conductor may want to decide whether the twelve `W-99z*` rows get renumbered at the wrap — they
are ordered *after* every numeric row by any lexical sort, which is not where #219's work belongs.

---

## ④ VERDICTS — 21 driven

### The generator, after the edits

| | before | after |
|---|---|---|
| `_gen_v3_manifest.py --selftest` | 45 bites, 0 fail | **69 bites, 0 fail** |

**+24 bites**, all added by this seam: 2 for the skills repoint (the v3 claim + the v2 non-claim),
22 for the open-question surface (per-question body and option-count bites across all five, plus
Q5's presence, its four gate names, the existence of each of those four gates in the repo, its
three dispositions, and its decides-nothing property).

**Four mutations driven, each RED by name, control GREEN before and after:**

| mutation | bite that bit |
|---|---|
| M1 — a gate named on the card is renamed | `questions/Q5-gate-exists:_validate_type_RENAMED.py` — *"the card names a gate that is no longer in the repo — re-derive it"* |
| M2 — an option is marked `(recommended)` | `questions/Q5-decides-nothing` — *"the red-gate card must not pre-select a disposition"* |
| M3 — the fifth card is dropped | `questions/Q5-present` — *"R2's Q1 card — four gates arrive red at bake"* |
| M4 — the skills match repointed back to v2 | `groups/excludes:designer-skills-v2/generate-from-canon/SKILL.md` — *"an EXCLUDED path was claimed by ['skills']"* |

⚠ **A harness artefact, corrected rather than reported as a bug.** The first mutation run read the
mutations as `green(BAD)` — the harness called `selftest()` and read the process exit code, but
`main` uses `sys.exit(0 if selftest() else 1)`, i.e. the verdict is the **return value**. The RED
bite lines were printing correctly all along. Re-driven reading the return value: all four RED,
control GREEN twice. There is no exit-code defect in the generator. Recording it because
"the gate doesn't fail" was the wrong conclusion I was one step from filing.

**The card renders.** Not regenerated into `reviews/` (see § ⑤) — rendered to `/var/tmp` against a
spliced manifest, which is also what surfaced fix (b′):

```
heading "Five things only you can settle" · headline metric 5 · 13 radios · 0 checked attributes
Q5 names all four gates · 3 dispositions · 0 'recommended' flags on Q5
```

The two literal `checked` strings in the page are **prose** (R1's Q1 body: *"I checked, because the
brief asked"*) — `0` radio inputs carry the attribute, so R1's *"nothing pre-selected"* property
survives the addition.

### R2's selftests, re-driven

| | verdict |
|---|---|
| `_gate_frozen_release.py --selftest` | **11 bites, 0 fail** ✅ |
| `_gate_ci_template.py --selftest` | **10 bites (mutants), 0 fail** ✅ |
| `_build_all.py --selftest` | **PASS — exact-ID routing over 140 steps** ✅ |
| `_gate_release_audit.py --selftest` | **8 bites, 1 fail** ⚠ — EXPECTED, see below |

### ⛔ THE ONE RED, EXPECTED AND PRICED — it clears in stage 2

`_gate_release_audit.py --selftest` bite `manifest/matches-a-fresh-generation` is RED, and
`--check` is RED, **because fix (a) and fix (b) changed the generator while the manifest on disk is
still R1's pre-edit generation.** The brief forbade regenerating in stage 1 (the manifest bakes
from a commit, and the landing commit does not exist yet), so this red is the *designed* state at
the end of stage 1.

It is the right red, and it names itself precisely:

```
❌ THE SHIP LIST ON DISK IS NOT WHAT THE GENERATOR PRODUCES at 71bb2f77ff59.
   on disk: 1590 files, sha256 ad0d985534457a1b
   fresh:   1586 files, sha256 36c327106c3d2d97
   4 path(s) the file ships that a fresh generation does not, first:
   ['designer-skills-v2/check-against-design-system/SKILL.md', …/draft-a-new-pattern/…,
    …/generate-from-canon/…, …/usability-review/…]
```

Exactly the four v2 skills the repoint dropped, and nothing else. **R2's instrument works** — this
is the gate biting on real drift on its first real occasion, which R2's UNPROVEN list could not
claim.

⚠ **CONDUCTOR — READ THIS BEFORE COMMITTING.** `release-audit --check` is wired **BLOCKING** in
both CI and `_build_all` `[135]`, and `--selftest` is `ABORT`-routed at `[136]`. **The landing
commit will be red on those two steps until stage 2 regenerates the manifest.** That is the
designed sequence, not an accident, but it must not be discovered by CI.

**Arithmetic for stage 2, so the result can be checked rather than accepted:** 1590 − 4 (v2 skills
dropped) + 5 (R3's skills, tracked from the landing commit) + 3 (R2's ci-template, likewise) =
**1,594 paths expected**. R2 predicted 1,593 for the ci-template addition alone; the extra one is
the fifth skill.

### The four CI-drift checks + the library index

| step | verdict |
|---|---|
| `[40]` `gen_token_ramp.py --check` | ✅ `0 file(s) DRIFTED, 147 already in sync` |
| `[45]` `canon/gen_canon_components.py --check` | ✅ `135 components in sync` |
| `[50]` `canon/gen_theme_cascade.py --check` | ✅ `230 override path(s), 387 component projection(s) in sync` |
| `[107]` `_build_memento_index.py --check` | ✅ `current (1791 records)` |
| `gen_library_214.py --check` | ✅ `143 component(s), index + index.json + stub in sync` |

All five hold — none of the three lanes' work disturbed the #219 wave-1 regen serial.

### The help gate and the chain

| | verdict |
|---|---|
| `_validate_help_gate.py` | ✅ **`214 script(s) scanned; every entry point answers --help before it can write`** (was: 7 failures) |
| `_gen_chain.py --check` | was ✗ STALE → **regenerated** → ✅ `FRESH — byte-matches the live chain` |

The chain regen wrote **only `_CHAIN.md`** (verified against `git status`): `GOOD-MORNING.md` and
`_LIVE-STATE.md` are untouched, as the brief requires. `_CHAIN.md` is `+10 / −6` — it is a
generated file and the delta is the seven new store rows presenting in the index.

---

## ⑤ STAGE 2 — NOT DONE, BY INSTRUCTION

Not run this seam, and deliberately: **the manifest and the page bake from a COMMIT, and the
landing commit does not exist yet.** The generator edits are the whole of stage 1.

On receipt of the landing commit hash, stage 2 is:

1. `_gen_v3_manifest.py --probe --commit <sha>` then `--manifest --commit <sha>` then `--page`
2. `--check` green
3. verify the page carries: the **ci-template** line in the gates group · the **corrected skills
   group** (five v3 skills, `check-with-gates` among them, zero `designer-skills-v2/` paths) · the
   **fifth card** with its four named gates and three dispositions
4. re-drive `_gate_release_audit.py --check` and `--selftest` — both must go **green**
5. after any `--dry-run` bake, re-run `_make_review.py` (R2's finding 6 — the bake rewrites the
   page and strips the review pair's stamps)
6. report the new tree lines for the conductor's second commit

---

## FINDINGS

1. **A rotted line-number citation cost nothing this time only because R2 flagged it.** R3's store
   row and Q1 both cite `_gen_v3_manifest.py` line numbers; R2's edits moved all four before this
   seam opened. Re-deriving by name is the fix, and it worked — but the general lesson is that a
   **cross-lane instruction addressed to a line number is a stale premise by construction** when
   lanes run concurrently. Cross-lane fix requests should cite the code by its text.
2. **Two lanes independently asked for the same card.** R2 Q1 and R3 Q6 are the same finding from
   opposite ends (R2 from building the runner, R3 from driving it). When two lanes converge on a
   question unprompted, that is signal about its weight, and it is the argument for the card being
   on Dave's surface rather than in two filed reports.
3. **A consumer outliving its producer is not inert.** Fix (b′) — the placeholder renderer still
   painted "PLACEHOLDER — R3 writes it" onto the page when fed the stale manifest. Found by
   *rendering* rather than by reading the code, which is the only reason it was found at all.
4. **A typed count sat one inch from Dave's radio buttons.** "Four things only you can settle" was
   prose beside data. Any change to the question list would have made his own decision surface
   lie about how many decisions it was asking for.
5. **The help-gate red would have blocked the landing commit's build**, not merely annoyed it —
   it is `ABORT`-routed and sits at a step number *below* every release step R2 added.

---

## UNPROVEN, declared

1. **Nothing is committed and no CI run exists.** Every verdict above was driven in this working
   tree. R2's UNPROVEN 1 and 2 (neither workflow has ever run on GitHub Actions) are **unchanged**
   by this seam — I did not discharge them and cannot.
2. **The manifest and the page are STALE on disk right now**, by instruction. Everything stated
   about the fifth card's rendering was measured on a `/var/tmp` render against a spliced manifest,
   not on the artefact in `reviews/`. The artefacts are correct only after stage 2.
3. **The seven help-gate fixes were driven on `--help` only.** Each script's *actual* verification
   run (the browser work) was not re-driven — the preamble is a no-op on any argv that is not
   `-h`/`--help`/`--usage`, and it sits before the scripts' own imports, but "the verifier still
   verifies" is asserted from the gate's shape, not measured. Priced: cheap, needs the render
   staging; the seven are #218 artefacts and were not otherwise touched this seam.
4. **`W-187` vs the `W-99z*` range is my reading, not a ruling.** I continued the numeric sequence
   because the previous reconcile seam did. If the conductor intends a different scheme for #219,
   this row is a one-line change.

---

## REPLAY-THESE (conductor)

- ⛔ **`release-audit --check` and `--selftest` are RED at the landing commit and stay red until
  stage 2 regenerates the manifest.** Both are BLOCKING/ABORT in CI and `_build_all` `[135]`/`[136]`.
  Land the commit knowing this, and do not push before stage 2 — or expect a red Actions run.
- **Expected ship-list size after stage 2: 1,594 paths** (1590 − 4 v2 skills + 5 v3 skills + 3
  ci-template). If `--manifest` produces a different number, something else moved.
- **`check-with-gates` is now the settled name** and is encoded in the generator, R3's five skill
  files and R2's template README. It is no longer a question.
- **R3's Q2 is still open and is the loudest unanswered one**: the skills land at
  `Apollo-designer-skills-v3.0.0/designer-skills-v3/skills/…` inside the zip. R3's own consequence
  note: *"most will not find the skills at all. That is a silent failure of the whole release."*
  It is a one-line path rewrite in the stager and it was **not** made this seam — no lane owns it
  and the brief did not authorise it.
- **The `W-99z*` id range is exhausted.** Twelve #219 rows sort after every numeric row.
- **Dave's open questions are now five, not four**, and the fifth is the only one whose answer
  changes what an outside designer sees first.

## Store rows

One row minted through `_state.add()` (never by hand-editing `_state.json`): `W-187`, for this
filed report (`s218-D7`, forgotten-document class #185). The doc-row gate was re-driven after
minting: `unrowed 0`.

## Not touched

`designer-skills-v1/` · `designer-skills-v2/` (read only — its four `SKILL.md` were repointed
*away from*, never edited) · `GOOD-MORNING.md` · `_LIVE-STATE.md` · `knowledge/_rulings.json`
(verified and included, never written) · Dave-owned rows · any constant, band, advisory or
threshold · `knowledge/_release/_v3_manifest.json` and `_v3_gate_probe.json` and the two
`reviews/RELEASE-V3-MANIFEST-*.html` (NOT regenerated, NOT hand-edited — stage 2's job) ·
R2's and R3's own files. No commit, no push.
