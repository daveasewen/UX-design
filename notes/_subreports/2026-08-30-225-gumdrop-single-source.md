# `#225`-`gumdrop-single-source` — `s225-D3`: the carried cut's version is stamped, not typed

session: `#225` · 2026-08-30
window: Opus enactment sub, `s225-D3`
sub index: `gumdrop-single-source`
brief: in-chat (no brief file) — conductor's `s225-D3` enactment brief, fences quoted below
tokens: `UNMEASURED — no `message.usage` reader is reachable from a sub's own tool surface`

## VERDICT

**DONE, and proven end-to-end at the manifest's commit.** Every `Memento — Gumdrop v*` literal in
the pack now derives from `carries.version`: the bake sweeps the whole stage for the literal and
stamps it from the committed manifest, so the three hand-typed instances (`_state.json` `built_by`
and the two runbook headers) are retired as a SOURCE even though they still read correctly in the
repo. The manifest's superseded sentence is corrected at its source in `_gen_pack_manifest.py`
citing `s225-D3`, and a second hand-typed twin of that same sentence — which the brief did not
know about, in the bake script's `PROVENANCE.json` heredoc — is now read from the manifest too.
Two `--dry-run` bakes produced the **identical** zip sha `17a4b661…`, so determinism holds. Arm 5
prints **`Memento — Gumdrop v1.0.3 (×5) — internally consistent`** on the staged pack.

The one design decision the brief left open, and the reason it mattered: the brief's "preferred
shape" (stage-time stamping) collides with `check_pack`'s byte-fidelity arm, which compares every
shipped path to the commit's blob. I resolved it by keeping the REAL current value in the repo
sources rather than a placeholder, which makes the stamp **idempotent and byte-neutral whenever
the repo is in sync** — measured: 0 files rewritten in the post-commit simulation. Drift is not
silent either: every rewrite prints a named DRIFT line, and `--check` was driven to confirm it
names exactly those paths and no others.

COUNTS: findings `10` · ruling-shaped `4` · UNPROVEN `2`

## What was done

Four files, all inside the fence.

- **`apollo-spider/gumdrop/runbooks/_RUNBOOK-context-gauge.md:3`** and
  **`_RUNBOOK-capture-ritual.md:3`** — literal moved `v1.0.0 → v1.0.3`, plus a two-line HTML
  comment marker under each ("STAMPED at bake from the pack manifest's `carries.version`
  (`s225-D3`). Do not hand-edit"). The marker carries **no path and no version**, so it cannot rot
  and cannot trip arm 1 or arm 2 of the doc gate; the full address lives in the bake script.
- **`apollo-spider/gumdrop/_state.json:17`** — `built_by` moved `v1.0.0 → v1.0.3`. JSON has no
  comment register, so it carries no marker; that boundary is stated in the bake script's block
  and here, not left silent.
- **`apollo-spider/build-designer-pack.sh`** — three changes:
  (a) a new `s225-D3` stamp block immediately after `MEM_VERSION` is read (i.e. after `--stage`,
  before `PROVENANCE.json`/`README.md` are written and before the advisory doc gate reads the
  stage), with a comment block justifying the shape from the `#220` precedent quoted below;
  (b) `PROVENANCE.json`'s `carries.what` stops being a hand-typed twin of the generator's
  sentence and is read from the manifest, JSON-escaped via `json.dumps` so a sentence containing
  a quote or backslash cannot break the file;
  (c) the README's own superseded sentence ("Its version line is its own — this pack's version
  does not move it, and a later Apollo release may carry the same Gumdrop or a newer cut")
  replaced with the `s225-D3` truth, interpolating `$MEM_NAME $MEM_VERSION`.
- **`knowledge/_release/_gen_pack_manifest.py`** — `carries.what`'s closing sentence rewritten
  (the superseded sentence, at its source), with an `s225-D3` comment above it recording what it
  used to say, what #224 measured, and Dave's words. The comment block immediately above `carries`
  also had to change: it asserted the version was stamped "NOWHERE inside `memento-package/`",
  which the stamp makes false — that claim was true of v1.0.0 and became the #224 defect the
  moment a literal was typed in there anyway.

No commits, no `git add`, no push. No writes to `_rulings.json`, `_state.json` (the repo's),
`_CHAIN.md`, `GOOD-MORNING.md`, `_LIVE-STATE.md`, `dist/`, the frozen ledger, `RATIFY_IDS`, the
committed `_pack_manifest.json`, or any gate. Arm 5 of `_gate_pack_docs.py` is untouched — its own
`--selftest` still reports *"5 arms, each driven to BOTH verdicts"*.

## Findings

1. **The brief's preferred shape collides with `check_pack`, and this is the finding the whole
   design turns on.** `_gen_pack_manifest.py:check_pack` byte-verifies EVERY manifest path against
   the commit's blob (`want_sha = blob_shas(sha, …)`; `"%d file(s) differ from the commit's
   blobs"`). Only `README.md`, `PROVENANCE.json` and `_MANIFEST.json` are exempt, and only because
   they are not manifest paths at all. All three Gumdrop literals ARE manifest paths
   (`apollo-spider/gumdrop/_state.json`, `…/runbooks/_RUNBOOK-*.md`, confirmed present in
   `_pack_manifest.json`'s `gumdrop` group, 15 paths). A stage-time rewrite of them therefore
   makes `--check` red. **Driven, not reasoned:**
   `bash apollo-spider/build-designer-pack.sh --check <dry-run zip> --commit 1e028a1…` →
   `CHECK RED — 1 problem(s): 3 file(s) differ from the commit's blobs, first:
   ['memento-package/_state.json', 'memento-package/runbooks/_RUNBOOK-capture-ritual.md',
   'memento-package/runbooks/_RUNBOOK-context-gauge.md']`
   — exactly the three the DRIFT lines named, and **no others**.
2. **Which is why the in-repo sources keep the REAL value, not a placeholder.** The brief offered
   both. A placeholder makes the repo copy permanently un-blob-equal to what ships, so `--check`
   would be red on those paths FOREVER by construction. Keeping the real value makes the stamp a
   no-op whenever the repo is in sync, so the strongest audit property in the release shape
   survives intact. **Measured:** the real stamp block, extracted verbatim from the script and
   driven over a stage carrying the working-tree files, printed
   `4 staged file(s) carry the literal, 0 rewritten`
   (4 not 3 because the generated `README.md` was already present in that copied stage).
3. **The justifying precedent, quoted from the build script itself** (`#220`, the block directly
   above where the stamp now sits): *"It is now READ from the manifest the generator wrote
   (ADR-0017, one home). A missing key dies loud under `set -e` rather than defaulting to a
   version nobody chose."* The stamp is the same move for the three files the `#220` fix could not
   reach, because those come out of the commit via `git archive` rather than being written by the
   script. The script header's own rule — *"same commit + same manifest ⇒ byte-identical zip"* —
   is preserved: the replacement value comes from the COMMITTED manifest, never from today.
4. **Determinism proven the way the header demands.** Two independent `--dry-run` bakes at
   `1e028a1…`, into separate out-dirs, both produced
   `sha256: 17a4b6616bdc7b006b5877358ae602a9ffa6a5f55d704c9ab804096b34b9961a`
   and the same packed-manifest sha `ea115bca…`. Assets: `dryrun-a.log`, `dryrun-b.log`.
5. **Arm 5 GREEN, in both states.** On the dry-run stage (sources still at v1.0.0, stamped up) and
   again on the post-commit-simulated stage (sources already at v1.0.3, stamp a no-op), the
   standalone run of `python3 knowledge/_release/_gate_pack_docs.py --stage <stage>` prints:
   `carried cut, as the shipped documents name it: Memento — Gumdrop v1.0.3 (×5) — internally consistent.`
   ×5 = the two runbook headers plus three occurrences in the generated README (heading table row,
   the `memento-package/` bullet, and the new `s225-D3` sentence). The HTML markers add no sixth
   literal, by design — they name no version.
6. **The stamped `_state.json` is valid JSON, checked twice.** The stamp only substitutes the
   version substring INSIDE the existing string (never a re-serialisation, so no formatting
   churn), and it re-parses every `.json` it touched under `set -e` so a broken stamp dies at the
   bake rather than in a designer's hands. Read back from the stage:
   `JSON OK -> Memento — Gumdrop v1.0.3 (empty starter store)`.
7. **A SECOND hand-typed twin of the superseded sentence existed, and the brief did not name it.**
   `carries.what` was typed in full in the bake script's `PROVENANCE.json` heredoc
   (`build-designer-pack.sh:208`) as well as authored in `_gen_pack_manifest.py:1759`. Correcting
   only the generator would have shipped a `PROVENANCE.json` contradicting the `_MANIFEST.json`
   beside it — the exact `#224` defect one register up. Now read from the manifest.
8. **A FOURTH stale literal survives, outside the pack and outside my fence:**
   `.github/workflows/gates.yml:187` — `"clean cut of Memento it carries is **Memento — Gumdrop
   v1.0.0**"`. Probed: it is repo CI, **not** a manifest path (the manifest's only `gates.yml` is
   `apollo-spider/ci-template/gates.yml`), so it does not ship and arm 5 cannot see it. Left as
   found.
9. **A `--dry-run` DIRTIES THE REPO, and it dirtied Dave's go/no-go page with a sha that is not
   the released pack's.** The script's closing block folds the measured zip size and sha back into
   `reviews/RELEASE-SPIDER-2026-08-26-v1.html`. Both my dry-runs stamped `17a4b661…` over the page
   — the frozen v1.0.3 release's sha is `fadd3eac…`. It also printed *"this write stripped the
   review pair's stamps"*. I restored the file with `git checkout --` after each run; `git status`
   shows `reviews/` clean. Nothing else in `reviews/` was touched. (Two rows that appeared in
   `notes/_REHEARSAL-LOG.jsonl` were NOT mine: its md5 was unchanged across the second bake —
   `3826801c1efc77d4fec6de2f04b8076e` before and after — so they are the conductor's concurrent
   writes and were left alone.)
10. **`--dry-run --commit HEAD` cannot run today.** The manifest is pinned at `1e028a1…` and HEAD
    is `3c1582c…`, so the script refuses (*"the manifest was generated at 1e028a1…, you asked to
    bake 3c1582c…"*). Every verification above ran at the manifest's commit, which is the honest
    reading anyway. Two environment notes for whoever repeats this: the sandbox's `/` is **100%
    full**, so `/var/tmp` staging dies with `No space left on device` and the stage must go under
    `_to_delete/` on the mount; and a full `--dry-run` takes ~60s, comfortably inside the wall, but
    must be launched with the `&` inside a subshell or the `cd` is backgrounded with it.

## RULING-SHAPED QUESTIONS

1. **Should `--check` learn about stamped paths?** As built, `--check` is red on exactly the paths
   the stamp moved, and green once the repo copies are synced (finding 2). Option (a) leave it
   strict — drift stays loud and the repo is the thing that gets fixed; option (b) exempt the
   stamped paths in `check_pack` the way `README.md`/`PROVENANCE.json`/`_MANIFEST.json` are
   exempt, which makes the repo copies irrelevant and lets a placeholder be used later.
   **Recommend (a)**, and it is what I built: (b) would retire the strongest audit property the
   release has — *"Every file above came out of that commit via `git archive`"*, a sentence the
   shipped README itself makes — for three files whose only job is to agree with a figure the
   manifest already publishes. `check_pack` was outside my fence in any case; (b) is an edit
   somebody would have to make deliberately.
2. **`.github/workflows/gates.yml:187` still says `Memento — Gumdrop v1.0.0`** (finding 8).
   Option (a) correct it to v1.0.3 as part of this ruling's sweep; option (b) leave it — it is a
   comment in repo CI, ships nowhere, and no gate reads it. **Recommend (a)**, cheap (~1 line),
   because it is the same class Dave just ruled on and a stale literal in CI is where the next
   person looks up "what version is Gumdrop".
3. **Should a `--dry-run` be allowed to write `reviews/RELEASE-SPIDER-*.html` at all?**
   (finding 9). Option (a) leave it — the page's zip figures are only honest from a bake that
   actually ran; option (b) fence the page write to `--release` only; option (c) keep it but make
   `--dry-run` write to a `-dryrun` copy. **Recommend (b)**: after a release is cut, a dry-run
   silently replaces the released sha on Dave's decision page with a throwaway one, which is a
   page that lies about a frozen artefact. Out of my fence; costed at ~5 lines.
4. **The HTML comment markers ship inside two designer-facing runbooks.** Option (a) keep them —
   they are invisible in any renderer and they are what stops the next editor hand-typing a
   version; option (b) drop them and let the bake script be the only address. **Recommend (a)**,
   as built, but it is a taste call about what a designer sees in raw source and it is Dave's eye.

## UNPROVEN / CLAIMED (ADR-0016)

- **UNPROVEN: the full bake path over a commit that CARRIES these edits.** The bake reads a named
  commit via `git archive`, never the tree, and I am fenced from committing. What was proven
  instead, component by component: the real stamp block (extracted verbatim from the script, kept
  at `assets/…/stamp-block-as-extracted.py`) driven over a hand-assembled stage carrying the
  working-tree copies of all three files → `0 rewritten`, and arm 5 green on that stage. Price to
  close: one commit plus one `--manifest` + `--dry-run` pair at the new sha (~2 min of machine
  time, and it is the conductor's call because it moves the committed manifest).
- **UNPROVEN: the regenerated manifest.** I did NOT regenerate `_pack_manifest.json` (brief's
  fence — it is the conductor's, and the committed one is the ratified v1.0.3 cut's). The
  generator offers no `--check`/`--dry` mode for the manifest, only `--manifest` which writes.
  Expected diff, stated so it can be checked rather than trusted: **exactly one key moves,
  `carries.what`**, from *"… Its version line is its own; the pack's version does not move it."*
  to *"… Its version moves WITH the pack (s225-D3): every Gumdrop version line in the cut is
  stamped from this one, so the pack cannot disagree with itself about what it carries."*
  `carries.name` and `carries.version` are untouched (`MEMENTO_CUT_NAME`/`MEMENTO_CUT_VERSION`
  were already v1.0.3). Everything else in my generator diff is comments.
- **CLAIMED (regression-free):** `python3 knowledge/_release/_gen_pack_manifest.py --selftest` →
  `selftest: 216 bites, 0 fail(s)`; `bash apollo-spider/build-designer-pack.sh --selftest` → both
  refusal arms green, ratification arm SKIPPED (already ratified);
  `python3 knowledge/_release/_gate_pack_docs.py --selftest` → `5 arms, each driven to BOTH
  verdicts`. These were re-read from the runs, not from a banner — but they are the instruments'
  OWN reading of themselves, which is not the same as a fresh eye over the diff.

## Evidence

`notes/_subreports/assets/2026-08-30-225-gumdrop-single-source/` —
`dryrun-a.log` / `dryrun-b.log`: the two full dry-run bakes at `1e028a1…` proving the identical
zip sha and carrying the stamp + DRIFT lines and arm 5's verdict (the 198 pre-existing PATH
findings are elided in these copies, marked in place). `check-red-unsynced.txt`: `--check` naming
exactly the three drifted paths. `postcommit-simulation.txt`: the same stamp code over a stage
carrying the working-tree files — `0 rewritten`, arm 5 green.
`stamp-block-as-extracted.py`: the stamp block as `awk` pulled it out of the shipped script, so
the simulation above is provably the real code and not a paraphrase of it.

REPLAY-THESE: `apollo-spider/build-designer-pack.sh` lines ~186–232 — the stamp block, its
justification comment and the `PROVENANCE.json` change (~1.6K tk) · ruling-shaped question 1 (the
`check_pack` trade-off), and questions 2 and 3, both of which are edits outside this sub's fence
(~0.6K tk)
