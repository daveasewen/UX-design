# Brief — #232 repair lane (Opus, continuation of the re-stage sub): green the cold column, route bento-first, re-cut

provenance: 232 · 2026-09-01 · conductor Fable · row W-335 (minted AT CREATION)
Dave's word, #232, verbatim: "I just want a solid output. lets get on it. needs done soon
so I'll go with your recommendations." The demo is TODAY (W-308). Licensed by that word:
the four recommendations as put to him in chat — repair the two gate reds at source, ship
the routing step, roster 57 stands (`s232-D2`), dial B (`s232-D1`).

## The job — PHASE 1 (edits, NO git), then STOP for the conductor's commit, then PHASE 2 (re-cut)

### Phase 1 — five edits, each verified by driving its gate

1. **Routing step in `designer-skills-v2/generate-from-canon/SKILL.md`** — a dashboard
   brief goes BENTO-FIRST: splice `knowledge/snippets/Template-dashboard-bento.reference.html`,
   never re-draw; if the brief is not dashboard-shaped and no template fits, ask. Keep it
   short and imperative, in the skill's existing voice. ⚠ This is the TACTICAL half of
   W-333 (Dave's KG-routing idea, banked) — add a one-line comment marker citing W-333 so
   the step is findable when the permanent home is ruled.
2. **Declare the fork**: add the `--bento-row-unit` row to `knowledge/_TOKEN-FORK-LEDGER.json`
   (intentional rail geometry, 184px under `.cn-template-dashboard-bento .c-bento.tpl-group-rail`
   vs 320px default). Match the ledger's existing row shape exactly. Verify:
   `_validate_token_forks.py` rc=0.
3. **Widen the type-blast acknowledgment** for `.btn` (25→26) and `.status` (11→12) via the
   gate's own `--update`, and PASTE THE DIFF of the acknowledgment change in the report.
   Verify: `_validate_type_blast_radius.py` rc=0 and `--selftest` green.
4. **Regenerate the stale support pair**: `python3 knowledge/tokens/_build_blast_radius.py`
   (135→136 components). Verify: `--check` rc=0.
5. **Enact `s232-D1`**: in `knowledge/_detect_retrieval.py`, the 0.90 spliced default is no
   longer a placeholder — update the docstring/help "PLACEHOLDER — Dave's dial" language to
   cite `s232-D1` (ruled 2026-09-01, B = 0.90). No numeric change (0.90 is already the
   default). Verify: `--selftest` still green.

Then run `ci-template/run-gates.py` semantics locally: drive the two repaired gates plus
the release-half survey steps you ran at the re-stage; confirm no NEW red. **STOP. Report
phase 1. The conductor commits (you perform NO git operation), then tells you to start
phase 2.**

### Phase 2 — the re-cut tail, in order, at the NEW commit

`--probe → --manifest → --page (reviews/RELEASE-SPIDER-2026-08-26-v1.html, real zip
figures) → _make_review.py overlay re-inject → two dry-run twins into two directories →
cmp → --check <twin>`. Then `ci-template/run-gates.py` on the pristine twin stage — the
target is **exit 0**. Replace `Apollo-Spider-v1.0.5-PROVING.zip` at the repo root with the
new bake (same durable-home rule as the re-stage; the old zip is superseded, say so with
both sha256s in the report). Fresh fingerprint stamped everywhere the old one was.

## Hard rules

- Everything from the re-stage brief stands: bake PROPOSED not ratified, `RATIFY_IDS`
  untouched, no membership change beyond what already landed, no `--release`, no push.
- The bento snippet body (`Template-dashboard-bento.reference.html`) is NOT edited — Dave
  parked further bento work (W-334). The fork is declared, not unified, for that reason.
- The `.btn`/`.status` remedy is `--update` (widen acknowledgment), NOT namespacing — the
  snippet stays untouched; this was put to Dave and adopted.
- If any edit reds a gate you cannot green by the licensed means: STOP and report.

## DO-NOT-RULE

No `_rulings.json`, no W-rows, no memory writes, no git operations in either phase, no
threshold change beyond the s232-D1 docstring, no bento-RSQ answers, no roster edits, no
ratification claim, no SKILL.md changes beyond the single routing step.

## Pitfalls — replayed

- All the re-stage brief's pitfalls stand (tiktoken first · call boundaries · ~178s wall ·
  mount-side + `TMPDIR` · never pipe hashes through tail/head · counts copied not
  estimated). You hit the `/var/tmp` hardcode last time — clean up any probe orphan again.
- The re-cut order is the trap: page before manifest, or twins before the probe, and the
  stale-copy defect returns wearing the version's clothes.
- `--update` on the blast gate writes `knowledge/_TYPE-BLAST-GATE.md` — that file's claims
  must end up TRUE at the new HEAD; check its text after.

## Report

APPEND a `## PHASE-1` and later `## PHASE-2` section to
`notes/_subreports/2026-09-01-232-restage-v105.md`'s successor:
`notes/_subreports/2026-09-01-232-repair-and-recut.md` — COUNTS (gate rc before/after per
edit · cold column pass/fail/exit · new zip sha256 + bytes · both fingerprints old/new),
the pasted `--update` diff, RECEIPTS, REPLAY-THESE, RULING-SHAPED QUESTIONS, `s214-D5`
cost line. Chat STUB per phase: verdicts + sha head + page path only.
