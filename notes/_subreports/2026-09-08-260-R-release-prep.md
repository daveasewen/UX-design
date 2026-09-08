# `#260`-`R` — release prep: v1.0.8 proved to the edge of Dave's word

session: `#260` · 2026-09-08
sub index: `R`
lane: release prep (DID NOT RELEASE — `--release` is Dave's word, s219-D4(2))

provenance: 260 · 2026-09-08
status: observed

## VERDICT

**v1.0.8 is PROPOSED at `ffb2240` and proved: the manifest is byte-identical to a fresh
generation at its own commit, the zip bakes twice to the same sha256
`091c8ae5862cbfa37bcda6d92d0b392b2b850336ba7ad4d41c8655806bc2ee33`, `--check` is GREEN against
the commit, and the generator's 216 bites pass.** Seven of the nine release gates are green; the
two reds are `audit --selftest` and `audit --pack`, and both are the **known pre-bake pair** —
they say "the manifest names a release nobody baked", which is the true state of a proposed cut
and is exactly the 7/9-before / 9/9-after shape #245 L5 recorded. They clear when `--release`
puts the v1.0.8 zip in `dist/`.

⬛ **ONE FINDING IS RULING-SHAPED AND IS NOT TAKEN HERE:** `knowledge/_validate_dataviz.py`
**leaves the ship set at v1.0.8** — it shipped in v1.0.7 and does not ship in v1.0.8, because
#260's own receipt gate (`223310b`, s260-D3) made it depend on a file the pack does not carry.

COUNTS: findings 4 · ruling-shaped 2 · declared skips 2

---

## Step 1 — the nine release gates

The list is the one #245 L5 ran and #257 re-ran (`notes/_subreports/2026-09-03-245-L5-cut.md`
§ Step 6). `_build_all.py` was READ (`--help`) and NOT run: its own contract says the full form
takes no argv, and both #245 and #257 recorded it as sandbox-impossible (`_build_all.py` is
sandbox-impossible — #257 wrap, UNPROVEN list). It is not the release-gate runner; the nine
below are.

Pass 1 (at `223310b`, before any of this lane's work):

| # | gate | rc | line |
|---|---|---|---|
| 1 | `_gate_frozen_release.py --check` | 0 | `PASS — 3 arm(s) asked, no frozen surface moved.` |
| 2 | `_gate_frozen_release.py --selftest` | 0 | `selftest: 14 bites, 0 fail(s)` |
| 3 | `_gate_release_audit.py --check` | 0 | `PASS — the manifest … byte-identical to a fresh generation at b9c4c802439c (1673 files, sha256 f98b7a6601991d48)` |
| 4 | `_gate_release_audit.py --selftest` | 0 | `selftest: 10 bites, 0 fail(s)` |
| 5 | `_gate_release_audit.py --pack` | 0 | `PASS — apollo-spider/dist/Apollo-Spider-v1.0.7.zip matches the manifest at b9c4c802439c` |
| 6 | `_gate_ci_template.py --check` | 0 | `PASS — the template parses, ships what it calls, and hides nothing.` |
| 7 | `_gate_ci_template.py --selftest` | 0 | `selftest: 10 bites, 0 fail(s)` |
| 8 | `build-designer-pack.sh --selftest` | 0 | `selftest: 216 bites, 0 fail(s)` + two `green — refused, as it must` |
| 9 | `cold-start/gen_projections.py --check` | 0 | `gen_projections --check OK — 3 projection(s) and 3 PLACED host file(s) in sync…` |

**9/9 green.** ⚠ Gate 9 does not live at `knowledge/gen_projections.py` (where #245's shorthand
implies); its only home is `apollo-spider/cold-start/gen_projections.py`.

Pass 2 (at `8357651`, after the bump — the pre-bake state):

| # | gate | rc | line |
|---|---|---|---|
| 1 | frozen `--check` | 0 | `PASS — 3 arm(s) asked, no frozen surface moved.` (apollo-spider row still `v1.0.7` — correct; the literal moves at `--seed`, after the bake) |
| 2 | frozen `--selftest` | 0 | `selftest: 14 bites, 0 fail(s)` |
| 3 | audit `--check` | 0 | `PASS — the manifest … byte-identical to a fresh generation at ffb2240ea178 (1678 files, sha256 c5610a43abd82877)` |
| 4 | audit `--selftest` | **1** | `RED [pack/frozen-history-is-skipped-not-failed] with the current zip green, an older frozen zip must not turn the arm red (the pre-#220 category error); got rc=1` |
| 5 | audit `--pack` | **1** | `❌ the manifest reads version 'v1.0.8' and NO zip in dist/ carries it … the manifest names a release nobody baked.` |
| 6 | ci `--check` | 0 | `PASS — the template parses, ships what it calls, and hides nothing.` |
| 7 | ci `--selftest` | 0 | `selftest: 10 bites, 0 fail(s)` |
| 8 | `build-designer-pack.sh --selftest` | 0 | `selftest: 216 bites, 0 fail(s)` |
| 9 | `gen_projections --check` | 0 | `gen_projections --check OK — 3 projection(s) and 3 PLACED host file(s) in sync…` |

**7/9 — and the two reds are the SAME PAIR #245 L5 recorded before its bake ("7/9 green before
the bake, 9/9 green after").** [4] is [5]'s arm: the selftest asserts the `--pack` behaviour, so
one red causes the other. Neither is a defect in the cut; both are the honest statement that a
PROPOSED version has no baked zip yet. ⛔ They are NOT to be "made green" by baking — the bake is
`--release` and that is Dave's word.

### Declared skips, with their reasons

- **`knowledge/_validate_screen.py` — NOT RUN, and this is a finding, not a bypass.** #258's wrap
  (RULING-SHAPED 1) records that it *"writes its ledger into `knowledge/_screen-gate/` keyed on
  BASENAME and clobbered tracked files four times today"*. Measured here: the file is unchanged
  since `44c8061` (#256) — i.e. **the clobber is unrepaired** — `GATE_DIR` is still
  `knowledge/_screen-gate` and the home is still `os.path.basename(path)` (L128/L131/L190), and
  `git ls-files knowledge/_screen-gate/` returns **10 tracked ledgers**
  (`dashboard.md`, `payments-journey.canon.md`, `sme-payments*.canon.md`,
  `nio-dash-console-v[12].canon.md`, `canon-gallery.canon.md`,
  `international-banking-dashboard.regen-v[12]*.md`). Running it on any screen whose basename
  collides with one of those ten **overwrites a tracked row**. ⬛ Its write policy is Dave's
  (#258 RSQ 1: hash/run-id key, refuse-to-overwrite, or move the directory out of the tree);
  this lane names it and stops the step [[gate-cannot-pass-in-one-environment]].
- **`knowledge/_tests/test_gates.py` — SKIPPED: it copytrees ~5 GB and cannot run in this
  sandbox** (the ENOSPC precedent #245 L5 names in its UNPROVEN list). Unchanged as a carry.

## Step 2 — the showroom

    python3 knowledge/gen_showroom.py --check
    gen_showroom --check: OUT OF SYNC — stale: ['action-bar.html', 'alert.html', …] orphaned: [] index: ok

⚠ `--check` prints only `stale[:6]` (gen_showroom.py L589), which is why the count reads as six.
The true count is the generator's own write tally:

    python3 knowledge/gen_showroom.py
    gen_showroom: 136 page(s) -> showroom/ (66 written, 0 orphan(s) pruned; index owned by knowledge/_render/gen_library_214.py)

**Stale before: 66** (the 60 pre-existing + the 6 chart pages, as #259's wrap predicted at ≈66).

    python3 knowledge/gen_showroom.py --check
    gen_showroom --check OK — 136 page(s) + index in sync (index owned by knowledge/_render/gen_library_214.py).

**Stale after: 0.** Commit **`ff46588`** — `#260 R: showroom regenerated (66 pages)`.

## Step 3 — the version bump and the manifest

⛔ The version is **not** typed in the build script (#228). `VERSION` and `MEMENTO_CUT_VERSION`
live in the generator, and the #245/#257 shape carries **four further literals** that
`--check` reads back off the staged tree. All six were moved v1.0.7 → v1.0.8:

| file | literal |
|---|---|
| `knowledge/_release/_gen_pack_manifest.py:113` | `VERSION = "v1.0.8"` |
| `knowledge/_release/_gen_pack_manifest.py:119` | `MEMENTO_CUT_VERSION = "v1.0.8"` (s225-D3 — ONE version story) |
| `apollo-spider/FIRST-SESSION.md:51` | `Apollo-Spider-v1.0.8` |
| `apollo-spider/gumdrop/_state.json:17` | `"built_by": "Memento — Gumdrop v1.0.8 (empty starter store)"` |
| `apollo-spider/gumdrop/runbooks/_RUNBOOK-context-gauge.md:3` | `Memento — Gumdrop v1.0.8` |
| `apollo-spider/gumdrop/runbooks/_RUNBOOK-capture-ritual.md:3` | `Memento — Gumdrop v1.0.8` |

⛔ **`RATIFY_IDS` was NOT touched.** No row is keyed to `v1.0.8`, so `ratification_status()`
derives **PROPOSED** and `--release` refuses. That is the machine waiting for Dave's word
(s223-D3 / s237-D9 — derived, never typed), and inventing the row here is exactly the laundering
#257 refused.
⛔ **`_gate_frozen_release.py:130`'s apollo-spider literal is still `v1.0.7`** and must stay so
until the bake exists; it moves at `--seed`, after `--release`, not before.

Commit **`ffb2240`** — `#260 R: v1.0.8 version story — VERSION + MEMENTO_CUT_VERSION + the four
carried literals` (5 files, +6/−6). Generator `--selftest` after the bump: **216 bites, 0 fails**
(the `naming/memento-cut-is-named` bite asserts the two literals agree — it would have caught a
half-bump).

    bash apollo-spider/build-designer-pack.sh --manifest --commit ffb2240 --full-stage /var/tmp/full8
    probing the gates at ffb2240ea178 (measured, not read by eye)…
    manifest -> knowledge/_release/_pack_manifest.json
      commit ffb2240ea178  files 1678  bytes 43682135  sha256 c5610a43abd82877

⚠ **`--full-stage` is not optional in substance, and the first run here proved it.** Run without
it, the differential arm at `_gen_pack_manifest.py:1029` (`if full_stage:`) never fires, and the
manifest came out at **1679 files / sha256 `17814be1cf62dc54`** with `_validate_dataviz.py`
graded `RUNNABLE — a verdict is a run`. With a `git archive` full stage of the same commit the
same probe grades it `REPO-BOUND — full-tree PASS`, and the manifest is **1678 files / sha256
`c5610a43abd82877`**. Two different ship sets from the same commit, decided by a flag. The
full-stage form is the sanctioned one (v1.0.7's own probe carries differentials), and it is the
one committed. ⬛ **That the flag is optional at all is ruling-shaped** — named, not ruled.

Probe at `ffb2240` (with full stage): **40 RUNNABLE · 11 REPO-BOUND · 3 NEEDS-DEP** (v1.0.7 was
41 / 9 / 4). Commit **`7d45a12`** — `#260 R: v1.0.8 manifest at ffb2240 (PROPOSED, 1678 files)`.

## Step 4 — the bake, proved

    bash apollo-spider/build-designer-pack.sh --dry-run --out-dir /var/tmp/bake1 --commit ffb2240
    sha256: 091c8ae5862cbfa37bcda6d92d0b392b2b850336ba7ad4d41c8655806bc2ee33   size: 20M

    bash apollo-spider/build-designer-pack.sh --dry-run --out-dir /var/tmp/bake2 --commit ffb2240
    sha256: 091c8ae5862cbfa37bcda6d92d0b392b2b850336ba7ad4d41c8655806bc2ee33   size: 20M

    cmp /var/tmp/bake1/… /var/tmp/bake2/…      → BYTE-IDENTICAL (rc 0, no output)

    bash apollo-spider/build-designer-pack.sh --check /var/tmp/bake1/Apollo-Spider-v1.0.8.zip --commit ffb2240
    CHECK GREEN — /var/tmp/bake1/Apollo-Spider-v1.0.8.zip matches the manifest at ffb2240ea178

    bash apollo-spider/build-designer-pack.sh --selftest
    selftest: 216 bites, 0 fail(s)
    === refusal: --release on a dirty tree ===            green — refused, as it must
    === refusal: --release without Dave's ratification === green — refused, as it must

The dry-run rewrites Dave's go/no-go page with the proof rows; the overlay was re-injected
(`_make_review.py`) and the pair committed as **`8357651`** — the page now carries the twice-baked
fingerprint and the delta-check line.

## Step 5 — is the engine actually in the ship set?

Verified **INSIDE the zip**, not inferred from the tree (#257's lesson) —
`unzip -l /var/tmp/bake1/Apollo-Spider-v1.0.8.zip`:

- `Apollo-Spider-v1.0.8/knowledge/canon/dv-render.js` (18,022 B) **IN**
- `dv-render-bar.js` 9,262 · `dv-render-line.js` 9,187 · `dv-render-stacked-area.js` 10,285 ·
  `dv-render-donut.js` 8,641 · `dv-render-sparkline.js` 9,852 · `dv-render-combo.js` 11,625 →
  **all six type partials IN**
- the six snippets that draw from data — `Chart-bar` · `Chart-line` · `Chart-stacked-area` ·
  `Chart-donut` · `Chart-sparkline` · `Chart-combo` `.reference.html` — **IN**
- the six `knowledge/components/chart-*.meta.json` behaviour contracts and the six
  `showroom/chart-*.html` pages — **IN**

All seven engine files are NEW at v1.0.8 (they are the only additions to the ship set over
v1.0.7).

### `_receipts.json` and the driver — OUT, and here is the rule that puts them out

| path | in/out | the manifest rule |
|---|---|---|
| `knowledge/_tests/chart-engine/_receipts.json` | **OUT** | no group's `match` claims `knowledge/_tests/`; it is unclaimed, not excluded by a named reason |
| `knowledge/_drive_chart_engine.py` | **OUT** | the `gates` group matches `knowledge/_validate_*.py` or `knowledge/_gate_*.py` (`_gen_pack_manifest.py:425`); `_drive_*` matches neither |
| `knowledge/_validate_dataviz.py` | **OUT at v1.0.8, IN at v1.0.7** | probe verdict `REPO-BOUND` ⇒ dropped from the gates group |

⬛ **RULING-SHAPED 1 — the receipt gate took the dataviz gate out of the pack.** Measured, not
argued. Staged the v1.0.8 manifest and ran the gate inside the stage:

    (in /tmp/stg8) python3 knowledge/_validate_dataviz.py
      [FAIL] snippets/Chart-donut.reference.html  (2 charts, 1 blocking, 0 advisory)
         ✗ dv-004: donut is ENGINE-DRAWN (no marks in the markup) and there is no driven receipt
           at knowledge/_tests/chart-engine/_receipts.json. Record one:
           python3 knowledge/_drive_chart_engine.py
      ❌ DataViz gate FAILED
    (in the repo) python3 knowledge/_validate_dataviz.py
      ✅ DataViz gate passed (15 chart surface file(s)).

Green in the repo, red in the pack ⇒ the differential arm classifies it REPO-BOUND ⇒ it stops
shipping. The remedy the gate itself names (`_drive_chart_engine.py`) is also not in the pack, so
a designer could not clear it even if they wanted to. **The options are Dave's, not this lane's:**
(a) ship the receipt + the driver (needs Chromium at the designer's end); (b) let the gate take
the static path when no receipt exists and say so out loud; (c) accept that dv-004 is a
repo-side check and the pack ships one gate fewer. **⛔ No option was taken and nothing was
changed to make this green** — the cut is reported as it measures.

⬛ **RULING-SHAPED 2 — `--full-stage` decides the ship set and is an optional flag** (Step 3).

### Also moved, and named rather than fixed

`_validate_fit_physics.py` flipped `NEEDS-DEP(playwright)` at v1.0.7 → `REPO-BOUND (crashed)`
here, on the same box class. Its verdict is environment-shaped, and it is the second gate that
leaves the pack (65 → 63 gates). Not investigated further at this seat — declared.

## What Dave has to do

**THE SENTENCE HE SAYS — one word is enough, but this is the unambiguous form:**

> **"Ratify v1.0.8."**

That is a RATIFYING word under s223-D3 (not an authorisation naming a cut, which is what
"cut 1.0.8" would be). ⬛ Inscribing it as a ruling id, keying `RATIFY_IDS["v1.0.8"]` to that id,
and moving the frozen literal are the conductor's steps after he says it — **this lane wrote
none of them.**

**THE COMMAND THE CONDUCTOR RUNS AFTER HE SAYS IT** (after the ruling is inscribed and
`RATIFY_IDS["v1.0.8"] = "<that id>"` is keyed, on a clean tree):

    bash apollo-spider/build-designer-pack.sh --release --commit ffb2240

It refuses on a dirty tree and refuses without the ratification, so both conditions are checked
by the script rather than by memory. Expect `apollo-spider/dist/Apollo-Spider-v1.0.8.zip` at
sha256 `091c8ae5862cbfa37bcda6d92d0b392b2b850336ba7ad4d41c8655806bc2ee33` — **byte-identical to
the dry-run above, and that equality is the point of the dry run**. Then, in order:
`_gate_frozen_release.py`'s apollo-spider literal `v1.0.7` → `v1.0.8` · the cut commit ·
`_gen_pack_manifest.py --seed --at HEAD` · the ledger commit · release gates pass 3 (expect 9/9).

## Commits this lane made

| sha | subject |
|---|---|
| `ff46588` | `#260 R: showroom regenerated (66 pages)` |
| `ffb2240` | `#260 R: v1.0.8 version story — VERSION + MEMENTO_CUT_VERSION + the four carried literals` |
| `7d45a12` | `#260 R: v1.0.8 manifest at ffb2240 (PROPOSED, 1678 files)` |
| `8357651` | `#260 R: the v1.0.8 go/no-go page carries the twice-baked zip proof (091c8ae5862cbfa3)` |

NOT PUSHED — Dave pushes via GitHub Desktop. `DOC_ROW_ACK` was declared on every commit for
lanes A's and V's filed reports; their `_state` rows belong to those lanes / the wrap, not here.

## UNPROVEN from this seat

- CI green on GitHub (nothing pushed; `_build_all.py` sandbox-impossible — the #257 carry stands).
- The screen gate's verdict on any #260 surface — see the declared skip.
- Whether the v1.0.8 zip opens correctly for a cold designer: `--check` proves it against the
  manifest, which is not the same as unzipping it and driving the gates from inside.

REPLAY-THESE: the two ruling-shaped blocks in Step 5 (~500 tk) · the pass-2 gate table (~250 tk —
why 7/9 is the right number before a bake) · Step 3's `--full-stage` paragraph (~250 tk).
