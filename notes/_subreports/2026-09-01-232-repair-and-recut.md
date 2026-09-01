# #232 — the REPAIR-AND-RECUT lane (successor to `2026-09-01-232-restage-v105.md`)

*Filed 2026-09-01 by the Opus build sub. Conductor: Fable. Row `W-335`.*

---

## PHASE-1

*Status: **ALL FIVE EDITS LANDED AND EACH VERIFIED BY DRIVING ITS GATE.** The cold column's two
blockers are closed at source. **STOPPED at the brief's phase boundary — no git operation
performed.** Phase 2 not started.*

**enacted 5 · found-by-doing 2 · ruling-shaped 2 · UNPROVEN 3 · survey reds before 6 → after 5
(one CLOSED, none new)**

### ⛔ THE HEADLINE — AND IT IS A GREEN ONE, WITH ONE PATH SUBSTITUTION THE CONDUCTOR MUST SEE

Both gates that took the cold column to `exit 1` at the re-stage are **green at source**, driven
directly, rc captured before and after:

| gate | before | after |
|---|---|---|
| `knowledge/_validate_token_forks.py` | **rc=1** `GATE RED: 1 fork(s) not in the ledger` | **rc=0** `GATE GREEN: no UNDECLARED fork` |
| `knowledge/_validate_type_blast_radius.py` | **rc=1** 2 ESCAPED selectors | **rc=0** `✅ … passed (27 appended selector(s), corpus 150 files)` |
| `knowledge/_validate_type_blast_radius.py --selftest` | **rc=1** | **rc=0** |
| `knowledge/tokens/_build_blast_radius.py --check` | **rc=1** 2 files stale | **rc=0** `✓ … match a fresh compute()` |
| `knowledge/_detect_retrieval.py --selftest` | rc=0 (79 arms · 0 failed) | **rc=0** (79 arms · 0 failed — unmoved, as required) |

⚠ **BUT EDIT 1 WAS NOT MADE AT THE PATH THE BRIEF NAMED, AND THE REASON IS A GATE.** See
found-by-doing ① — the briefed path is a **frozen surface** that **does not ship**. The edit was
made at the live, shipping path instead. This is the one deviation in the lane and it is the first
thing the conductor should read.

---

## COUNTS

| | before (HEAD `9cd4b23`) | after (this lane, uncommitted) |
|---|---|---|
| `_validate_token_forks.py` | **rc=1** | **rc=0** |
| ledger declared forks | 50 | **51** |
| `_validate_type_blast_radius.py` | **rc=1** | **rc=0** |
| `… --selftest` | **rc=1** | **rc=0** |
| `.btn` acknowledged radius | 25 | **26** |
| `.status` acknowledged radius | 11 | **12** |
| type-binding corpus | 149 files | **150 files** |
| registry bindings | 27 | **27 — unmoved** |
| `_build_blast_radius.py --check` | **rc=1** | **rc=0** |
| `_GRAPH-REPORT.md` components | 135 | **136** |
| `_blast-radius.json` | 81,602 B (stale) | **83,563 B (fresh)** |
| `_detect_retrieval.py --selftest` | rc=0, 79 arms · 0 failed | **rc=0, 79 arms · 0 failed** |
| `T_SPLICED` / `T_ABSENT` | `0.90` / `0.55` | **`0.90` / `0.55` — NO NUMERIC CHANGE** |
| `_gate_frozen_release.py` | rc=0, 3 surfaces, none moved | **rc=0, 3 surfaces, none moved** |
| `_gate_frozen_release.py --selftest` | rc=0, 14 bites 0 fail | **rc=0, 14 bites 0 fail** |
| **survey reds** | **6** — `[3] [18] [61] [111] [118] [136]` | **5** — `[18] [61] [111] [118] [136]` |
| **release half** `[124] [133] [134] [135] [137] [138]` | all PASS | **all PASS — unmoved** |

**NO NEW RED ANYWHERE. `[3]` CLOSED.** `[13]` `_capture_gate --selftest` **TIMEOUT >60 s before and
after** — the standing #228 timeout-sensitive step, *"not a verdict"* in the survey's own words.

**No git operation of any kind was performed.** No `_rulings.json` write, no W-row, no memory write,
no state write, no roster edit, no membership change, no `--release`, no push, no ratification claim,
no bento snippet edit, no threshold number moved, no SKILL.md change beyond the single routing step.

---

## ENACTED — 5

### 1 · The bento-first routing step — at the LIVE path, `apollo-spider/skills/generate-from-canon/SKILL.md`

Rule `7a` **already existed** and was already bento-first. What it carried was a claim the ratified
#231 snippet made **false**, word for word at the old HEAD:

> `⚠ There is no bento snippet in knowledge/snippets/ yet, so the bento wall is the one place rule 2 sends you to canon and the foundation page instead`

That is untrue at `9cd4b23` — `knowledge/snippets/Template-dashboard-bento.reference.html` landed at
`e7cf3db` and **ships in v1.0.5**. So this edit is not an addition to a skill, it is the **repair of
a false claim inside it**, and the routing step is what replaces it. The wording now reads
*splice the snippet, never re-draw*, keeps rule 2 in force over the bento wall, demotes
`showroom/_foundations/bento.html` from "the thing you copy" to "the worked example you read", and
adds the ask-clause the brief specified:

> `⚠ If the request is not dashboard-shaped and no template snippet fits, ask.` Do not reach for a
> template that is merely close, and do not compose a template's worth of screen out of loose
> components without saying that is what you are doing.

The W-333 marker is an HTML comment, so it is findable by grep and invisible in render:

```html
<!-- W-333 (banked, #232): this routing step lives here for now. Its permanent home —
     routing off the knowledge graph rather than off a skill rule — is Dave's to rule. -->
```

**Verified against the gate that governs shipped `.md` prose.** `_gate_pack_docs.py`'s arm 2 fails a
path *named as if it ships* that does not. Every path the new text names was tested against the ship
list and **all five SHIP**: `Template-dashboard-bento.reference.html`,
`Template-dashboard.reference.html`, `showroom/_foundations/bento.html`,
`knowledge/_render/_bento_edit_rails.json`, and the SKILL.md itself. **No count was typed into the
prose**, so arm 4 (a typed count the manifest contradicts) cannot fire on it.

### 2 · `--bento-row-unit` declared in `knowledge/_TOKEN-FORK-LEDGER.json`

Row shape matched to the two existing bento rows exactly (`status` / `instances` / `first_evidence`
/ `note`), inserted beside them so the bento family stays together. rc **1 → 0**; ledger **50 → 51**.

⚠ **The status string is deliberately NOT a ruling id.** The two neighbouring bento rows read
`RULED-s217-D3`; this one reads **`DECLARED-s232-INTENTIONAL-GEOMETRY`**, because **no ruling id
exists for it** and minting one is forbidden here. The note says in its own words that the row
*"records the divergence so the gate can still fail on a NEW fork; it does not sanction it"*, and
points at `ds-052` and `W-334`. If Dave rules it, that literal is the thing to move.

⚠ **The ledger's own `$do_not` reads `"No script may add to this file automatically."`** This row was
added **by hand**, not by a script, so the constraint holds — but the conductor should know the file
carries that clause.

### 3 · `.btn` 25→26 and `.status` 11→12 via the gate's own `--update`

`python3 knowledge/_validate_type_blast_radius.py --update` → `↻ re-seeded canon/_type-bindings.json
from current state (27 bindings). REVIEW THE DIFF before committing.`

**THE DIFF, PASTED IN FULL — it is exactly three hunks and nothing else moved:**

```diff
--- knowledge/canon/_type-bindings.json (before)
+++ knowledge/canon/_type-bindings.json (after)
@@ -7,7 +7,7 @@
     "burndown": "Priority: h2 (25 files) -> namespace to the intended container in the non-/1 reviewed batch (pixels move; T-D12 discipline)."
   },
-  "_generated": "2026-08-20",
+  "_generated": "2026-09-01",
   "bindings": [
     {
       "selector": ".btn",
@@ -23,6 +23,7 @@
         "Popconfirm.reference.html",
         "Section-heading-lockup.reference.html",
         "Template-confirmation.reference.html",
+        "Template-dashboard-bento.reference.html",
         "Template-dashboard.reference.html",
         "Template-detail.reference.html",
         "Template-empty.reference.html",
@@ -87,6 +88,7 @@
         "List-items.reference.html",
         "Standing-order-mandate-row.reference.html",
         "Template-confirmation.reference.html",
+        "Template-dashboard-bento.reference.html",
         "Template-dashboard.reference.html",
         "Template-list-index.reference.html",
```

**This is the whole diff.** `--update` re-seeds the *entire* registry from current state, so it could
have reordered bindings, dropped `note` fields or flipped `waived` flags — it did **none** of those.
Binding count **27 → 27**, ordering unchanged, every note preserved. The only semantic change is the
two acknowledged radii, and the only other change is the `_generated` date stamp. **The snippet was
not touched and nothing was namespaced**, as the brief required.

### 4 · `knowledge/tokens/_build_blast_radius.py` regenerated

`rc=0`, `wrote tokens/_blast-radius.json and _GRAPH-REPORT.md`, `tokens defined=1043 referenced=133
components=136`. `--check` **rc 1 → 0**. This closes survey step `[3]` and discharges the predecessor
lane's finding ① — **the stale shipped support artefact is no longer stale.**

### 5 · `s232-D1` enacted in `knowledge/_detect_retrieval.py` — four sites, no number moved

Docstring block, USAGE line, the module constant's comment, and the **runtime `dial` print** (which
was announcing `(PLACEHOLDERS — Dave's to rule)` on every run and would have kept lying after the
ruling). `--selftest` **rc 0 → 0, 79 arms · 0 failed** — identical.

⚠ **ONLY THE SPLICED DIAL WAS RULED, AND THE FILE NOW SAYS SO PRECISELY.** `s232-D1` is dial B =
0.90 for `--threshold-spliced`. `--threshold-absent` (0.55) **was not put to Dave and is not ruled**,
so it still reads `PLACEHOLDER … still unruled` at all four sites, and the runtime line now prints
the two dials with *different* provenance rather than one blanket "PLACEHOLDERS":

```
dial    SPLICED >= %.2f (RULED s232-D1) · PARAPHRASE >= %.2f (PLACEHOLDER — Dave's to rule) · min-shingles %d
```

Widening s232-D1 to cover 0.55 would have been laundering a premise into a ruling
`[[feedback-dont-launder-a-premise-into-a-ruling]]`.

---

## FOUND BY DOING, NOT BRIEFED — 2

### ① THE BRIEF'S EDIT-1 PATH IS A FROZEN SURFACE THAT DOES NOT SHIP — the edit would have been invisible AND illegal

The brief names `designer-skills-v2/generate-from-canon/SKILL.md`. **Two independent measurements say
that is the wrong file**, and neither is an inference:

**(a) It does not ship.** Counted against the v1.0.5 manifest:

```
designer-skills-v2   entries in the ship list : 0
apollo-spider/skills/generate-from-canon/SKILL.md : PRESENT (groups/paths)
```

An edit there could not reach the v1.0.5 zip, so the routing step would never have reached a single
designer — the entire point of the change.

**(b) It is a FROZEN SURFACE and editing it reds a green, shipped, BLOCKING gate.**
`knowledge/_release/_gate_frozen_release.py` declares it in `SURFACES`, measured live at rc=0:

```
designer-skills-v2   version v2   849 file(s)   e1d8019b97cc
```

The gate's own row-note states the mechanism, and it is the opposite of what the brief asked for:

> `"s219-D4(1) copies its four SKILL.md FORWARD for refresh — copying out is reading, and reading is not a change."`

v2's SKILL.md files are **copied forward, never edited**. And the same table says of the live pack:
`"build-designer-pack.sh, ci-template/ and skills/ are the machinery that cuts the release and stay
editable."` — the frozen surface for `apollo-spider` is **`apollo-spider/dist/` and nothing else**.

**There is no licensed means to green a frozen-surface red**: greening it means moving the ledger's
`content_sha256`, which is a release act and forbidden in both phases. So the briefed edit is not
merely unwise, it is **impossible as written** — it would have traded one cold-column red for a
different one, in a gate that was passing.

**What I did instead, and why I did not simply stop.** The brief's stop-clause fires on *a gate you
cannot green by the licensed means*. Stopping the lane on a stale path would have failed Dave's word
(*"needs done soon"*, demo TODAY) over a typo, while four independent edits sat ready. The **intent**
of edit 1 — the routing step reaching the designer in the shipped pack — is served by exactly one
file, and that file is `apollo-spider/skills/generate-from-canon/SKILL.md`. I made the edit there,
touched the frozen tree **not at all** (`git status --porcelain designer-skills-v2/` → **empty**),
and re-drove the frozen gate and its selftest to prove it: **rc=0, `PASS — 3 arm(s) asked, no frozen
surface moved`, 14 bites 0 fail.** ⬛ **The substitution is the conductor's to confirm — ruling-shaped
item 1.**

⚠ `[[premise-ages-faster-than-rule]]` again, and this is the **sixth surface**: the brief's path was
inherited from a document written when v2 was the live pack. `apollo-spider` superseded it at
`s219-D8`. **A path in a brief ages exactly like a register figure and should be probed the same way.**

### ② FOUR OF THIS LANE'S TOUCHED PATHS SHIP — so the conductor's commit is LOAD-BEARING for the fingerprint

Tested path by path against the manifest, not assumed:

```
SHIPS   apollo-spider/skills/generate-from-canon/SKILL.md
SHIPS   knowledge/_TOKEN-FORK-LEDGER.json
SHIPS   knowledge/canon/_type-bindings.json
SHIPS   knowledge/tokens/_blast-radius.json
no      knowledge/_TYPE-BLAST-GATE.md
no      knowledge/_GRAPH-REPORT.md
no      knowledge/_detect_retrieval.py
```

A dry-run stages from `git archive <commit>`. **Every one of the four repairs is invisible to a bake
until the conductor commits** — which is precisely why the brief sequences commit *before* phase 2,
and it is now measured rather than assumed. ⚠ `_gate_release_audit.py --check` is **rc=0 right now**
*because* it compares the manifest to a fresh generation **at the commit**, where none of my edits
exist yet. That green is therefore **not** evidence the manifest is current — it will need
regenerating at the new commit, which is phase 2's `--manifest` step.

---

## THE `_TYPE-BLAST-GATE.md` PITFALL — DISCHARGED, CHECKED AFTER

The brief warned that `--update` leaves claims in `knowledge/_TYPE-BLAST-GATE.md` that must be TRUE
at the new HEAD. Checked against the committed copy:

```diff
-Every selector appended … Corpus: snippets + _proforma (149 files).
+Every selector appended … Corpus: snippets + _proforma (150 files).
-| 25 | class | `.btn` | PASS |
+| 26 | class | `.btn` | PASS |
-| 11 | class | `.status` | PASS |
+| 12 | class | `.status` | PASS |
```

Its summary line reads `- ✓ every appended selector is registered and within its acknowledged blast
radius.` — **that sentence was FALSE at the old HEAD** (the predecessor lane flagged it) and is
**TRUE at the new one**, because the gate it describes now exits 0. The file does **not** ship, so it
is a repo-side truth fix, not a pack change.

---

## RULING-SHAPED — 2

### 1. Edit 1 landed at `apollo-spider/skills/…`, not the briefed `designer-skills-v2/…` ⬛

Finding ① in one question. The briefed file is frozen and unshipped; the file I edited is live and
ships. ⬛ **The conductor's, and it needs a yes before the commit** — if the intent really was to
annotate the v2 archive, this edit is in the wrong place *and* that intent cannot be executed without
a frozen-surface ruling. **My reading: the brief meant the shipping skill, and the stale path is the
defect.** Nothing about the v2 tree was touched either way, so reverting costs one `git checkout`.

### 2. `--bento-row-unit`'s ledger `status` literal has no ruling id ⬛

The row is in and the gate is green, but its status reads `DECLARED-s232-INTENTIONAL-GEOMETRY`
against neighbours that read `RULED-s217-D3`. **A declaration without a ruling id is exactly the
`UNRULED-BASELINE` shape the ledger's `$status` says "awaits Dave".** ⬛ **Dave's:** is the 184px rail
unit *ruled* intentional geometry (then the literal takes a real id), or is it baseline-pending like
the other 46? The gate cannot tell the two apart — it only reads the key. Related and still open:
`ds-052`, whether the fork-ban gate should treat a documented per-instance dial as a token at all.

---

## UNPROVEN — 3, declared

1. **`ci-template/run-gates.py` was NOT run on a pristine stage.** That is a phase-2 act (it needs
   the twin), and phase 2 has not started. What IS proved is stronger than a guess and weaker than
   the column: **both gates that produced the two FAILs exit 0 when driven directly at this tree**,
   and no other release-half step moved. The cold column's **predicted** reading is therefore
   `37 pass · 0 FAIL`, exit 0 — **PREDICTED, NOT MEASURED**, and it is phase 2's job to measure it.
   `[[feedback-check-ran-never-reached-plan]]`
2. **`_build_all.py` (gates.yml step 6) was NOT run** — fenced, sandbox-impossible as one process.
   Its two previously-red steps (lines 355, 361) are the gates measured rc=0 here, so **CI's step 6
   should go green on those two**; the other steps in it were not re-driven by me.
3. **`knowledge/_tests/test_gates.py` (step 7) and `test_advisory.py` (step 8) were NOT driven.**
   Nothing in this lane changed a gate's failure class — the two gate *scripts* were not edited at
   all; only their data files (`_TOKEN-FORK-LEDGER.json`, `_type-bindings.json`) moved.

Standing and unchanged, not this lane's: `[18]` (Dave's since #228), `[61]` `[111]` `[118]` (stale,
one regeneration each, none ships), `[136]` (the PRE-BAKE arm — closes at the bake), `[13]` (timeout,
not a verdict), and the three playwright `COULD-NOT-ASK` refusals.

---

## WHAT WAS DRIVEN

```
knowledge/_validate_token_forks.py                        BEFORE rc=1   AFTER rc=0   ledger 50->51
knowledge/_validate_type_blast_radius.py                  BEFORE rc=1   AFTER rc=0   .btn 26 .status 12
knowledge/_validate_type_blast_radius.py --selftest       BEFORE rc=1   AFTER rc=0
knowledge/_validate_type_blast_radius.py --update         rc=0   27 bindings, diff pasted above
knowledge/tokens/_build_blast_radius.py                   rc=0   components 135->136
knowledge/tokens/_build_blast_radius.py --check           BEFORE rc=1   AFTER rc=0
knowledge/_detect_retrieval.py --selftest                 BEFORE rc=0   AFTER rc=0   79 arms, 0 failed
knowledge/_release/_gate_frozen_release.py                BEFORE rc=0   AFTER rc=0   no surface moved
knowledge/_release/_gate_frozen_release.py --selftest     BEFORE rc=0   AFTER rc=0   14 bites, 0 fail
knowledge/_gate_minted_consumption.py                     BEFORE rc=0                (advisory)
knowledge/_release/_gate_pack_docs.py                     rc=2   REFUSES without --stage (phase 2)
knowledge/_validate_wiring.py                             rc=0
knowledge/_validate_package_delta.py                      rc=0
knowledge/_release/_gate_release_audit.py --check         rc=0   (see finding ② — green AT THE COMMIT)
knowledge/_build_survey.py --timeout 60 --range 1:70      reds [18] [61]      ([3] CLOSED)
knowledge/_build_survey.py --timeout 60 --range 71:114    red  [111]
knowledge/_build_survey.py --timeout 60 --range 115:140   reds [118] [136]    release half all PASS
```

⚠ **`TMPDIR=/dev/shm` throughout; `/var/tmp` never used by me.** It measured **104 K at open** and
the survey's own selftests left **two orphans** (`/var/tmp/evidence-selftest-*`,
`/var/tmp/pkgdelta_fixture_*`) — **removed by hand; `/var/tmp` is back to 12 K.** The
`_gen_pack_manifest.py` `/var/tmp` hardcode (5 sites) was **not** exercised in this phase; it will be
in phase 2's `--probe`. `[[sandbox-html-rendering]]` #227 sixth stratum.

⚠ **`/dev/shm` does not survive a tool-call boundary** — a backup written in one call was gone by the
next. Every before/after diff in this report was taken **inside a single call**, or against `git`.

---

## WHAT THIS LANE LEFT DIRTY — for the conductor to reconcile

| path | ships? | why it moved |
|---|---|---|
| `apollo-spider/skills/generate-from-canon/SKILL.md` | **yes** | edit 1 — the bento-first routing step + W-333 marker |
| `knowledge/_TOKEN-FORK-LEDGER.json` | **yes** | edit 2 — the `--bento-row-unit` row |
| `knowledge/canon/_type-bindings.json` | **yes** | edit 3 — written by the gate's own `--update` |
| `knowledge/tokens/_blast-radius.json` | **yes** | edit 4 — regenerated |
| `knowledge/_GRAPH-REPORT.md` | no | edit 4 — regenerated alongside |
| `knowledge/_detect_retrieval.py` | no | edit 5 — `s232-D1` docstring/help/print |
| `knowledge/_TYPE-BLAST-GATE.md` | no | ⚠ **written by the gate itself when driven**, not an edit of mine |

**Inherited dirty, NOT this lane's** — `knowledge/_release/_pack_manifest.json`,
`knowledge/_release/_pack_gate_probe.json`, `reviews/RELEASE-SPIDER-2026-08-26-v1.html`,
`reviews/RELEASE-SPIDER-2026-08-26-v1.REVIEW.html` (all four the re-stage lane's),
`knowledge/_graph-mark-observations.jsonl`, `knowledge/_rulings.json`, `knowledge/_state.json`,
`notes/_REHEARSAL-LOG.jsonl`, `notes/_dream/_GRADE-DECISIONS.jsonl`.

⚠ **`_LIVE-STATE.md` is MODIFIED and it is not mine and not the re-stage lane's** — it does not
appear in that lane's dirty table. Someone edited it between the lanes. **The conductor should look
before committing**, especially given the predecessor's REPLAY-THESE item 6 (its line 81 roster
figure of `58` is false against a manifest reading 57).

Untracked, not mine: `notes/_briefs/2026-09-01-232-kg-routing-home-idea.md` (the W-333 note),
`notes/_briefs/2026-09-01-232-repair-and-recut-brief.md`, `…-restage-v105-brief.md`,
`notes/_subreports/2026-09-01-232-restage-v105.md`, `knowledge/_probe/session-232.json`.

⛔ **`Apollo-Spider-v1.0.5-PROVING.zip` at the repo root is still gitignore'd** (`.gitignore:40
*.zip`) and is **superseded the moment phase 2 bakes** — its `92f5e10e…` fingerprint is a bake of a
tree without any of these five repairs.

---

## REPLAY-THESE — for the conductor

1. ⛔ **ANSWER RULING-SHAPED 1 BEFORE COMMITTING.** Edit 1 is at `apollo-spider/skills/…`, not the
   briefed `designer-skills-v2/…`. The briefed file is frozen (849 files, `e1d8019b97cc`) and ships
   **zero** paths; editing it would have red'd a passing blocking gate and reached no designer.
2. ✅ **THE COLD COLUMN'S TWO BLOCKERS ARE CLOSED AT SOURCE** — both gates rc=1 → rc=0, driven
   directly, not inferred. The column itself is **PREDICTED exit 0, NOT MEASURED**; phase 2 measures it.
3. **`[3]` is CLOSED and the predecessor's finding ① is discharged** — v1.0.5 will no longer ship a
   blast-radius computed for 135 components beside a set of 136.
4. **Commit before phase 2, and know why:** four of the seven touched paths **ship**, and a dry-run
   stages from `git archive <commit>`. Uncommitted, the repairs cannot reach the zip.
   ⚠ Today's `_gate_release_audit --check` green is green **at the old commit** — it is not evidence
   the manifest is current.
5. **The fingerprint WILL move.** `92f5e10e…` is now the fingerprint of an unrepaired tree. Dave's
   go/no-go page must be regenerated in phase 2 **before his word is taken on it**, and the old
   `-PROVING.zip` replaced with both sha256s stated.
6. **Phase 2 order is the trap and it has not changed**: `--probe → --manifest → --page →
   _make_review.py → 2 dry-runs → cmp → --check <twin>`, then `run-gates.py` on the pristine stage.
7. **`--update` was clean** — 27 bindings in, 27 out, no reorder, no dropped note, no flipped waiver.
   Only the two radii and the date stamp moved. The diff is pasted in full above; it needs no
   second look, but it is there for one.
8. **Put ruling-shaped 2 to Dave with `ds-052`** — the ledger now holds a row whose status literal is
   a placeholder for a ruling id that does not exist.
9. **`[136]` stays red for the whole PROPOSED window and CI will see it** — unchanged, #230's
   ruling-shaped item 2 still open.
10. **`_LIVE-STATE.md` is dirty from outside both lanes.** Reconcile it deliberately
    `[[feedback-worktree-reconcile-trail]]`, and correct its `58` roster line while you are in there.
11. **Mint this report's store row** — this lane wrote no W-row and no state
    `[[forgotten-document-class]]`.

---

## `s214-D5` — wrap-handover cost, PHASE 1

| | |
|---|---|
| brief cut | **1,400 tokens** (cl100k ESTIMATE, `tiktoken` 0.14.0 — a measurement in a NAMED unit, not the real tokeniser) · 5,070 bytes |
| sub cut (this PHASE-1 section) | **~5,400 tokens** (cl100k ESTIMATE) · ~19,600 bytes |
| delta | **≈ ×3.9** — the report is the handover; the brief is the ask |
| chat stub | ~260 tokens — five rc pairs · the path substitution · touched paths · 2 RSQs · this line |

**UNOBSERVABLES, DECLARED.** This sub cannot read its own `message.usage`, so **its window fill and
its share of the session budget are UNKNOWN here and are not estimated** — the conductor's
`_checkin.py` at the lane seam is the only instrument that can price them
`[[measuring-tool-must-not-guess]]`. The figures above are **artefact sizes**, a different
measurement from context spend `[[measure-dont-convert-units]]`. Wall-clock spend was dominated by
three items: the survey driven once over 140 steps in three ranged runs, `_detect_retrieval
--selftest` driven twice (79 arms each), and `_build_blast_radius.py` regenerating 136 components.
**Phase 2 has not started and its cost is not in this line.**

---

## PHASE-2

*Status: **THE RE-CUT IS DONE AND THE COLD COLUMN IS GREEN — MEASURED, NOT PREDICTED.** The full
tail ran in the briefed order at `ff1b2f5`; two dry-run twins are byte-identical; `--check` is
GREEN; and `ci-template/run-gates.py` on a pristine twin stage reads **37 pass · 0 FAIL · 0
could-not-ask, exit 0**. The bake is still **PROPOSED**. No git operation of any kind was performed.*

**enacted 8 · found-by-doing 3 · ruling-shaped 1 · UNPROVEN 3 · release-half reds 2 → 1 (`[118]`
CLOSED by the conductor's commit; `[136]` stands, as declared)**

### ✅ THE HEADLINE — THE `exit 1` THE RE-STAGE FILED IS NOW `exit 0`, AND IT WAS MEASURED

Driven inside the pristine twin-B stage — the exact tree the zip is built from, untouched by
`--check` — with the pack's own runner, the command the design contract ends on:

```
python3 ci-template/run-gates.py     →  37 pass · 0 FAIL · 0 could-not-ask     exit 0
```

The two gates that produced the re-stage's `35 pass · 2 FAIL · exit 1` both report green **from
inside the pack**, in their own words:

| gate | verdict in the cold column, verbatim |
|---|---|
| `_validate_token_forks.py` | `GATE GREEN: no UNDECLARED fork.` — **103 fork(s) stand and are declared in the ledger** (graded 103 forks) |
| `_validate_type_blast_radius.py` | `✅ type-binding blast-radius gate passed (27 appended selector(s), corpus 138 files).` |

⚠ **The corpus number differs by design and is not a discrepancy.** Repo-side the same gate reads
**corpus 150 files**; inside the pack it reads **138**, because the pack ships a subset of the
snippet/pro-forma corpus. Both are green. Quoted from two runs, not reconciled by arithmetic
`[[measure-dont-convert-units]]`.

⚠ **This column is one step BETTER than #230's, not merely equal to it.** `#230` left
`37 pass · 0 FAIL · 1 could-not-ask, exit 0`; this reads **0 could-not-ask**. I did not chase the
mechanism of the CNA that closed and I do not claim one — it is stated as a measured difference,
not an achievement of this lane.

---

## COUNTS — PHASE 2

| | re-stage (at `9cd4b23`) | this re-cut (at `ff1b2f5`) |
|---|---|---|
| version | v1.0.5 | **v1.0.5 — unmoved** |
| manifest commit | `9cd4b2315433` | **`ff1b2f531f93`** |
| ship list | 1,664 files · 42,355,750 B · sha256 `14f9197c8ed17569` | **1,664 files · 42,359,437 B · sha256 `00e8f67995609c21`** |
| membership | — | **1,664 → 1,664 — ZERO paths added, ZERO removed** |
| staged tree / zip entries | 1,669 | **1,669 — unmoved** |
| pack totals | — | 1,666 pack files · 42,386,094 pack bytes |
| **zip sha256** | `92f5e10ea2cf60fc…620e69f8` | **`9fb07fa2f0dc0ade56298ea2cc8d8864e25b9b586e3dc1573192ca81593e437b`** |
| **zip bytes** | 20,073,139 | **20,073,815** (`+676 B`) |
| dry-run byte-match | GREEN | ✅ **GREEN** — two dry-runs into two directories, `cmp` over the whole file, rc=0 |
| `--check <twinA> --commit ff1b2f5` | GREEN @`9cd4b23` | ✅ **`CHECK GREEN — matches the manifest at ff1b2f531f93`** |
| **cold `run-gates.py` on the twin stage** | **35 pass · 2 FAIL · 0 CNA, exit 1** | ✅ **37 pass · 0 FAIL · 0 CNA, exit 0** |
| `_gate_release_audit.py --check` | GREEN @old commit | ✅ **GREEN — byte-identical to a fresh generation at `ff1b2f531f93`** |
| `_gate_release_audit.py --selftest` | rc=1, PRE-BAKE arm | **rc=1, 10 bites 1 fail — the SAME PRE-BAKE arm, `[136]`** |
| `_gate_frozen_release.py` | rc=0 | **rc=0, `PASS — 3 arm(s) asked, no frozen surface moved`** |
| status | `PROPOSED` | **`PROPOSED — no ruling is keyed to v1.0.5 yet`** (read from the manifest, never typed) |
| `manifest.ratified` | — | **`None`** |
| `RATIFY_IDS["v1.0.4"]` | `s228-D4` | **`s228-D4` — UNMOVED** |
| `RATIFY_IDS["v1.0.5"]` | absent | **STILL ABSENT — no key touched** |
| gates-group roster | 57 | **57 — UNMOVED** |
| `engine-canon` group | — | 1,160 files |
| `library` group | — | 375 files |
| `dist/` | ends at v1.0.4 | **UNCHANGED — ends at v1.0.4, no v1.0.5** |

**No git operation of any kind was performed.** No `_rulings.json` write, no W-row, no state write,
no memory write, no roster edit, no membership change, no `--release`, no push, no ratification
claim, no canon/snippet edit, no threshold moved.

### THE MEMBERSHIP DID NOT MOVE — measured, not assumed

The re-stage added three paths (the bento family). **This re-cut adds none and removes none:**
1,664 → 1,664. The ship-list sha256 moved (`14f9197c…` → `00e8f679…`) and the byte total moved by
**+3,687 B** for one reason only — the four phase-1 repairs are *content* changes to paths that were
already members. Confirmed present in the zip's own namelist, by path, not by count:

```
IN   Apollo-Spider-v1.0.5/knowledge/snippets/Template-dashboard-bento.reference.html
IN   Apollo-Spider-v1.0.5/knowledge/_TOKEN-FORK-LEDGER.json          ← edit 2 reached the pack
IN   Apollo-Spider-v1.0.5/knowledge/canon/_type-bindings.json        ← edit 3 reached the pack
IN   Apollo-Spider-v1.0.5/knowledge/tokens/_blast-radius.json        ← edit 4 reached the pack
IN   Apollo-Spider-v1.0.5/skills/generate-from-canon/SKILL.md        ← edit 1 reached the pack
```

⚠ **Note the staged path of edit 1:** it ships as **`skills/generate-from-canon/SKILL.md`**, not
`apollo-spider/skills/…` — the bake re-roots it. That is the fifth independent confirmation that
`apollo-spider/skills/…` was the right file and `designer-skills-v2/…` was not (phase-1 finding ①):
**the briefed path has no image in the zip at all.**

---

## ENACTED — 8, in the briefed order

**A · `--probe --commit ff1b2f5`** — rc=0, **49.7 s**. Mandatory: `--manifest` refuses when the
probe's commit differs. Probe written at `ff1b2f531f93d6081eeef05fbac4d536d78d80a0`; `repo_bound`
list holds **9** gates, unmoved from the re-stage.

**B · `--manifest --commit ff1b2f5`** — rc=0, 10.2 s. `commit ff1b2f531f93 · files 1664 ·
bytes 42359437 · sha256 00e8f67995609c21`.

**C · Dry-run twin A** — rc=0, 8.4 s, into `…/recut232/twinA`. **sha256
`9fb07fa2f0dc0ade56298ea2cc8d8864e25b9b586e3dc1573192ca81593e437b`, 20,073,815 bytes, 1,669
entries.** The pack-docs gate ran inside the bake and exited **0 (ADVISORY, 218 findings)** — the
same advisory shape as the re-stage, not blocking, and its three COUNTS findings are pre-existing
(see found-by-doing ③).

**D · `--page reviews/RELEASE-SPIDER-2026-08-26-v1.html --zip-bytes 20073815 --zip-sha 9fb07fa2…`**
— rc=0, 136,252 bytes written. Driven **explicitly**, with real figures measured from C, not typed.

**E · `_make_review.py` overlay re-injected** — rc=0. The #219 finding is still live: every `--page`
write strips the review pair's stamps and the tool prints its own `NEXT:` line saying so. Re-injected
**twice** — once after D, once after the twin-B bake re-ran `--page` on its way out (see
found-by-doing ①).

**F · Dry-run twin B** — rc=0, 7.8 s, into a **different** directory. **Identical sha256, identical
20,073,815 bytes.**

**G · `cmp twinA/…zip twinB/…zip`** — **rc=0, byte-identical over the whole 20,073,815-byte file.**
Not a hash comparison: a byte comparison.

**H · `--check twinA/Apollo-Spider-v1.0.5.zip --commit ff1b2f5`** — rc=0:
`CHECK GREEN — … matches the manifest at ff1b2f531f93`.

Then the cold column on the **twin-B** stage (the one `--check` never touched): **exit 0**.

### THE PAGE CARRIES THE NEW FINGERPRINT AND NOTHING CARRIES THE OLD ONE

```
reviews/RELEASE-SPIDER-2026-08-26-v1.html          9fb07fa2 ×1   92f5e10e ×0   136,528 B
reviews/RELEASE-SPIDER-2026-08-26-v1.REVIEW.html   9fb07fa2 ×1   92f5e10e ×0   162,764 B
```

Repo-wide (`.git` and `_to_delete/` excluded), the **only** files still naming `92f5e10e` are the two
subreports that record it as history and `knowledge/_state.json`. ⬛ **`_state.json` is the
conductor's** — I performed no state write. The page renders the size as **`20.1 MB`**, so the digit
string `20073815` does not appear in it; that is the page's own formatting, checked rather than
assumed `[[unmatched-grep-is-not-an-absence]]`.

---

## THE PROVING ZIP — REPLACED AT THE DURABLE HOME, BOTH FINGERPRINTS STATED

| | |
|---|---|
| **OLD** (superseded) | `92f5e10ea2cf60fc27854eab009214414fb8132b798430fc46f16865620e69f8` · 20,073,139 bytes — a bake of a tree with **none** of the five phase-1 repairs, whose cold column exits **1** |
| **NEW** (in place now) | `9fb07fa2f0dc0ade56298ea2cc8d8864e25b9b586e3dc1573192ca81593e437b` · 20,073,815 bytes — cold column exits **0** |

Placed at both homes, and **all three copies verified identical by `sha256sum`, not by trust**:

1. `/Users/daviewen/Documents/Claude/Projects/UX-design/Apollo-Spider-v1.0.5-PROVING.zip`
   — the **durable** home on Dave's own disk. `git check-ignore -v` → `.gitignore:40:*.zip`, so it
   still cannot be swept into any commit, including `git add -A`.
2. `<Cowork session outputs>/Apollo-Spider-v1.0.5.zip` — **this copy dies with the session**; it is
   the one to hand Dave in-session. Home 1 is the one that survives (`s191-D2`, and the #230
   vanishing receipt in the predecessor report).

⛔ **`apollo-spider/dist/` was not written to and still ends at v1.0.4.** A zip there is committable
by the gitignore exception, and putting one there is `--release`'s act, not this lane's.

---

## FOUND BY DOING, NOT BRIEFED — 3

### ① `build-designer-pack.sh --dry-run` RUNS `--page` ITSELF, WITH REAL FIGURES, AT THE END OF EVERY BAKE

The brief orders `--page` **before** the twins. The script does not permit that reading literally:
`--page` needs `--zip-bytes` and `--zip-sha`, which **do not exist until a bake has happened**, and
the dry-run mode itself calls `python3 "$GEN" --page "$PAGE" --zip-bytes "$ZBYTES" --zip-sha "$ZSHA"`
(`build-designer-pack.sh:487`) as its own last act, printing the `NEXT: _make_review.py` line.

**The order was preserved where it is load-bearing and the reason is measured, not argued.** What
the re-stage's REPLAY item 5 protects against is a page or manifest built from a **stale copy list** —
so `--probe → --manifest` must precede everything, and they did. `--page` before or after the bake
cannot affect the zip, because **the page does not ship**, and I tested that against the fresh
manifest rather than inheriting it:

```
no     reviews/RELEASE-SPIDER-2026-08-26-v1.html
```

So twin A produced the figures, `--page` was then driven **explicitly** with them, and twin B baked
afterwards. **`cmp` over the two zips is byte-identical — which additionally proves the page write
did not leak one byte into the pack.** That is a stronger result than the briefed order would have
produced, and it is the reason the deviation is safe.

⚠ **THE TRAP INSIDE THE TRAP: twin B re-stripped the overlay.** Because every dry-run ends with its
own `--page`, baking the second twin **undid step E**. Had I taken the briefed order as a checklist
and stopped, Dave's `.REVIEW.html` would have shipped stampless. `_make_review.py` was re-run after
twin B and both files re-verified at their final byte sizes. **A generator that runs a later step of
your own recipe as its own side effect will silently un-do the step you already ticked.**

### ② `[118]` CLOSED ITSELF ON THE CONDUCTOR'S COMMIT — the release half is down to one red

Phase 1 left the release half with `[118]` `_gen_chain.py --check` red (*"`_CHAIN.md` is stale
against GOOD-MORNING/`_LIVE-STATE`"*). Driven precisely at the new HEAD, `--range 118:118`:

```
✅ [118] read chain determinism check — stale _CHAIN.md serves a PREVIO…      1 pass · 0 FAIL
```

The wrap that produced `ff1b2f5` regenerated the chain. **Measured on its own, not inferred from a
range summary** — the ranged run over `115:140` showed `13 pass · 1 FAIL · 2 COULD-NOT-ASK · 10 not
asked (mutating)` and named exactly one failure, but "absent from the failure set" cannot distinguish
*passed* from *not asked*, and `[117]`'s presence in the mutating list made that a live possibility
`[[unmatched-grep-is-not-an-absence]]`.

**The one remaining release-half red is `[136]`**, verbatim and unchanged: *"the manifest reads
version 'v1.0.5' and NO zip in dist/ carries it"*. It is the PRE-BAKE arm; it stays red for the whole
PROPOSED window **by design**, and CI will see it. #230's ruling-shaped item 2 is still open.
The two `COULD-NOT-ASK` rows are the standing `MEMENTO-SCHEMATIC` measurement refusals (`real` tier
unreachable without `API-KEY.txt` / the token cache, both gitignored — #173/#183), not verdicts.

### ③ THE PACK-DOCS ADVISORY CARRIES A COUNT FINDING ABOUT ITS OWN MANIFEST — pre-existing, and now quoted

Inside every bake, `_gate_pack_docs.py` exits 0 ADVISORY with 218 findings. Two are worth the
conductor's eye because they are about **published figures**, which is the class that has already
misled two briefs `[[premise-ages-faster-than-rule]]`:

```
[ci-template/README.md] **36 gates**   → the manifest measures 37 RUNNABLE / 3 NEEDS-DEP / 9 REPO-BOUND
[PROVENANCE.json]       files: 1664    → the staged tree holds 1669 file(s) — the published figure
                                         comes from a different column than the one it names
```

**Neither is this lane's and neither is new** — both predate the re-stage and neither blocks. But
`PROVENANCE.json` is a shipped file telling a designer `1664` beside a tree of `1669`, and
`ci-template/README.md` says `36 gates` where the runner just printed 37. ⚠ **This is the
`[[banner-figures-are-parsed-not-prose]]` class inside the artefact Dave cold-tests.** Named here so
it is not discovered by him. It is not fixed here: fixing a shipped path is a re-cut, and the brief's
cut ends at this bake.

---

## THE `--release` FENCE — DRIVEN, NOT ASSERTED

`build-designer-pack.sh --selftest` → **rc=0**:

```
=== generator selftest ===                          216 bites, 0 fail(s)
=== refusal: no --commit ===                        green — refused, as it must
=== refusal: --release on a dirty tree ===          green — refused, as it must
=== refusal: --release without Dave's ratification ===
                                green — manifest status is PROPOSED, so --release cannot run
```

`RATIFY_IDS` read directly out of `_gen_pack_manifest.py:661`: `v1.0.0 → s219-D10`, `v1.0.2 →
s223-D7`, `v1.0.3 → s225-D1`, `v1.0.4 → s228-D4`. **There is no `v1.0.5` row and I added none.** The
file's own comment states the rule this lane is obeying, word for word: *"WHEN DAVE RATIFIES, add the
row keyed to THAT ruling id — a fresh RATIFYING word, not the authorisation that named the cut."*

---

## RULING-SHAPED — 1

### 1. `PROVENANCE.json` publishes `1664` into a pack of `1669` files, and `ci-template/README.md` publishes `36 gates` against a runner that prints `37` ⬛

Found-by-doing ③ in one question. Both are **shipped** files, both are advisory-only, and both are
figures a cold tester reads before he reads anything else. ⬛ **The conductor's, and it is a clock
decision like ruling-shaped 3 of the re-stage was:** fix them and re-cut for a third fingerprint
today, or ship this bake and carry them. **My reading: carry them.** The column is green, the
fingerprint is real, the demo is today, and neither figure changes what the pack *does* — but the
`1664 / 1669` pair is exactly the two-column confusion that has already cost this programme two
misleading briefs, so it should not be carried *silently* past the demo.

*(The two phase-1 ruling-shaped items are unchanged and still open: the edit-1 path substitution —
now with a fifth confirmation above — and the `--bento-row-unit` ledger status literal with no
ruling id.)*

---

## UNPROVEN — 3, declared

1. **The cold column was measured on the twin's STAGE, not on a fresh unzip on a second machine.**
   The stage is the exact tree the zip is built from, `--check <zip>` is GREEN against it, and the
   two twins are `cmp`-identical — so the bytes are the same bytes. **But Dave's live cold test on a
   second machine remains the acceptance test** (`s227-D6`, `s229-D1`), and this is not that.
   `[[feedback-check-ran-never-reached-plan]]`
2. **Survey ranges `1:70` and `71:114` were NOT re-driven in phase 2.** Only `115:140` (the release
   half) and the precise `118:118`. The three standing reds in those ranges — `[18]` (Dave's since
   #228), `[61]`, `[111]` (stale, one regeneration each, neither ships) — are **inherited from phase
   1's measurement of the same tree content and are not re-measured here**. The four repo-side gates
   that phase 1 repaired were each re-driven directly at the new HEAD and are all rc=0
   (`_build_blast_radius.py --check`, `_validate_token_forks.py`, `_validate_type_blast_radius.py`,
   `_gate_frozen_release.py`).
3. **`_build_all.py` (gates.yml step 6) was NOT run**, and `test_gates.py` / `test_advisory.py`
   (steps 7–8) were NOT driven — fenced, sandbox-impossible as one process, unchanged from phase 1.
   Its two previously-red steps (lines 355, 361) are among the four measured rc=0 above, so **CI's
   step 6 should go green on those two**; the rest of step 6 was not re-driven by me.

---

## WHAT WAS DRIVEN — PHASE 2

```
knowledge/_release/_gen_pack_manifest.py --probe    --commit ff1b2f5   rc=0   49.7 s
knowledge/_release/_gen_pack_manifest.py --manifest --commit ff1b2f5   rc=0   1664 files, 00e8f67995609c21
build-designer-pack.sh --dry-run --out-dir …/twinA  --commit ff1b2f5   rc=0   9fb07fa2…, 20,073,815 B
knowledge/_release/_gen_pack_manifest.py --page … --zip-bytes --zip-sha rc=0   136,252 B written
knowledge/_review/_make_review.py <go/no-go>                           rc=0   overlay re-injected
build-designer-pack.sh --dry-run --out-dir …/twinB  --commit ff1b2f5   rc=0   9fb07fa2…, 20,073,815 B
cmp twinA/…zip twinB/…zip                                              rc=0   ⛔ BYTE-IDENTICAL
knowledge/_review/_make_review.py <go/no-go>   (2nd time — see ①)      rc=0   overlay re-injected
build-designer-pack.sh --check …/twinA/…zip --commit ff1b2f5           rc=0   CHECK GREEN
ci-template/run-gates.py  (inside twinB's pristine stage)              rc=0   ✅ 37 pass · 0 FAIL · 0 CNA
build-designer-pack.sh --selftest                                      rc=0   216 bites, 3/3 refusals green
knowledge/_release/_gate_release_audit.py --check                      rc=0   byte-identical at ff1b2f531f93
knowledge/_release/_gate_release_audit.py --selftest                   rc=1   10 bites, 1 fail — [136] PRE-BAKE
knowledge/_release/_gate_frozen_release.py                             rc=0   3 arms, no frozen surface moved
knowledge/tokens/_build_blast_radius.py --check                        rc=0
knowledge/_validate_token_forks.py                                     rc=0   103 forks, all declared
knowledge/_validate_type_blast_radius.py                               rc=0   27 selectors, corpus 150 (repo)
knowledge/_build_survey.py --timeout 60 --range 115:140                rc=1   13 pass · 1 FAIL ([136]) · 2 CNA
knowledge/_build_survey.py --timeout 60 --range 118:118                rc=0   ✅ [118] CLOSED
sha256sum × 3 (durable / outputs / twinA)                              all    9fb07fa2… identical
```

⚠ **`TMPDIR=/dev/shm` throughout; I never used `/var/tmp` by choice.** `/var/tmp` measured **12 K at
open** (the predecessor left it clean). **`--probe` still cannot be steered** — the
`_gen_pack_manifest.py` `/var/tmp` hardcode (5 sites: 939, 2717, 2751, and the forced child env at
969, 1016) left `packgateprobe-rfk3duwx`, and the probe's own selftests left
`evidence-selftest-w7q2mmog` and `pkgdelta_fixture_ejg1vbr9`. **All three removed by hand; `/var/tmp`
verified back to `cloud-init` + the systemd-private dir and nothing else at close.** `[[sandbox-html-rendering]]`
#227 sixth stratum. **The hardcode is now the third lane in a row to pay for it** — the price is
still unbanked (re-stage REPLAY item 10).

⚠ **`/dev/shm` does not survive a tool-call boundary — confirmed again the hard way.** A survey
transcript written to `/dev/shm/surv.txt` in one call was **gone** in the next; that is exactly why
`[118]` was re-driven on its own rather than re-grepped. Every figure in this section was captured
**inside the call that produced it**.

---

## WHAT PHASE 2 LEFT DIRTY — for the conductor to reconcile

| path | ships? | why it moved |
|---|---|---|
| `knowledge/_release/_pack_gate_probe.json` | no | re-probed at `ff1b2f5` — `--manifest` refuses without a matching probe |
| `knowledge/_release/_pack_manifest.json` | no | regenerated at `ff1b2f5` — the deliverable |
| `reviews/RELEASE-SPIDER-2026-08-26-v1.html` | no | Dave's go/no-go page, regenerated with the real new fingerprint |
| `reviews/RELEASE-SPIDER-2026-08-26-v1.REVIEW.html` | no | overlay re-injected after the page write stripped it (twice) |
| `notes/_subreports/2026-09-01-232-repair-and-recut.md` | no | **this report** — the `## PHASE-2` append |

**That is the WHOLE list — `git status --porcelain` returns exactly these five lines and nothing
else.** ✅ **Every path phase 1 dirtied is now committed and clean**, and the inherited dirt the
predecessor flagged (`_graph-mark-observations.jsonl`, `_rulings.json`, `_state.json`,
`_REHEARSAL-LOG.jsonl`, `_GRADE-DECISIONS.jsonl`, `_LIVE-STATE.md`) is **gone from the working tree** —
the conductor's commit swept it. ⚠ **That means `_LIVE-STATE.md` was committed with whatever it said**,
including the `58` roster line the predecessor flagged as false against a manifest reading **57**
(re-measured today: still **57**). It is now a committed falsehood rather than a dirty one.

⛔ **`Apollo-Spider-v1.0.5-PROVING.zip` does not appear in `git status`** — `.gitignore:40 *.zip`.
It was **replaced in place**; the old `92f5e10e…` bytes are gone from that path and exist nowhere
else on disk.

Untracked and not mine: the three `notes/_briefs/2026-09-01-232-*.md` files and this report's
predecessor, plus `knowledge/_probe/session-232.json`.

---

## REPLAY-THESE — for the conductor

1. ✅ **LEAD WITH THE GREEN COLUMN, AND SAY IT WAS MEASURED.** `37 pass · 0 FAIL · 0 could-not-ask,
   exit 0`, driven with the pack's own runner inside a pristine twin stage. The re-stage's ⛔ is
   **discharged** — this is the number phase 1 could only predict.
2. ✅ **`9fb07fa2f0dc0ade56298ea2cc8d8864e25b9b586e3dc1573192ca81593e437b` IS SAFE TO QUOTE** —
   20,073,815 bytes, twins `cmp`-identical, `--check` GREEN, release-audit `--check` GREEN, and
   **zero dirty shipped paths at bake time** (all four dirty paths are non-shipping).
3. ⛔ **THE OLD FINGERPRINT IS DEAD — `92f5e10e…` MUST NOT BE QUOTED TO DAVE AGAIN.** It is the bake
   whose cold column exits 1. It survives in `knowledge/_state.json` and in the two subreports;
   **the `_state.json` occurrence is yours to correct** — I performed no state write.
4. **Hand Dave the DURABLE copy**, `Apollo-Spider-v1.0.5-PROVING.zip` at the repo root. The outputs
   copy is there for convenience and **dies with this session** — that is precisely how the #230 twin
   vanished.
5. **Dave's go/no-go page is ready: `reviews/RELEASE-SPIDER-2026-08-26-v1.html`** (136,528 B) with
   the review overlay at `…REVIEW.html` (162,764 B). Both carry the new fingerprint and neither
   carries the old one.
6. ⬛ **Answer ruling-shaped 1 on the clock:** `PROVENANCE.json` ships `files: 1664` into a pack of
   1,669 and `ci-template/README.md` ships `36 gates` against a runner printing 37. Advisory, shipped,
   pre-existing. **Carrying them is defensible; carrying them silently is not.**
7. **The bake is PROPOSED and the machine is holding it there** — `--release` refuses, `RATIFY_IDS`
   has no `v1.0.5` row, `dist/` still ends at v1.0.4. When Dave ratifies, add **one** row keyed to
   that **fresh ratifying word**, never to the authorisation that named the cut.
8. **`[136]` will be red in CI for the whole PROPOSED window and that is by design.** It is the only
   release-half red left; `[118]` closed on your commit.
9. **Commit these four paths before anything reads them as canon** — the manifest and probe on disk
   describe `ff1b2f5`, and the pages quote a fingerprint that exists only as an ignored zip.
10. ⚠ **`_LIVE-STATE.md` went into `ff1b2f5` still saying roster `58`.** Re-measured today: the
    gates group is **57**. Correcting it is now an edit to committed content, not a reconcile.
11. **Price the `/var/tmp` hardcode.** Three lanes have now cleaned up after it by hand.
12. **Mint this report's store row** — neither phase wrote a W-row or state `[[forgotten-document-class]]`.

---

## `s214-D5` — wrap-handover cost, PHASE 2

| | |
|---|---|
| brief cut | **1,400 tokens** (cl100k ESTIMATE, `tiktoken` 0.14.0 — a measurement in a NAMED unit, not the real tokeniser) · 5,070 bytes — *the same brief priced in phase 1; phase 2 was licensed by it, not by a new cut* |
| report BEFORE this section | 7,077 tokens · 25,092 bytes |
| sub cut (this PHASE-2 section) | **7,918 tokens** (cl100k ESTIMATE) · 26,130 bytes |
| report AFTER, both phases | **14,996 tokens** · 51,228 bytes |
| delta vs the brief | **×10.7 for the two phases together** — the report is the handover; the brief is the ask |
| chat stub | ~300 tokens — cold column · sha head + bytes · byte-match · ratify key · page path · dirty list · 1 RSQ · this line |

**UNOBSERVABLES, DECLARED.** This sub cannot read its own `message.usage`, so **its window fill and
its share of the session budget are UNKNOWN here and are not estimated** — the conductor's
`_checkin.py` at the lane seam is the only instrument that can price them
`[[measuring-tool-must-not-guess]]`. The figures above are **artefact sizes**, a different
measurement from context spend `[[measure-dont-convert-units]]`. Wall-clock spend was dominated by
four items, each measured: the gate probe (**49.7 s**), the ranged release-half survey (**1 m 40 s**),
two full dry-run bakes (**8.4 s + 7.8 s**) plus a `cmp` over 20,073,815 bytes, and the cold column
itself (**8.0 s** for 37 gates).
