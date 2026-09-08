# `#260`-`R2` — the driven-receipt evidence ships: the dataviz gate is back in the cut

session: `#260` · 2026-09-08
sub index: `R2`
lane: release prep, continued (DID NOT RELEASE — `--release` is Dave's word, s219-D4(2))
continues: `notes/_subreports/2026-09-08-260-R-release-prep.md` (lane R, RULING-SHAPED 1)

provenance: 260 · 2026-09-08
status: observed

## VERDICT

**Both gates that fell out of the v1.0.8 ship set are back, and neither was weakened to get
there.** `_validate_dataviz.py` is `RUNNABLE — ran clean, verdict PASS` inside the staged pack;
`_validate_fit_physics.py` is `NEEDS-DEP playwright install chromium`, which is what it was at
v1.0.7. The gates group goes **63 files / 43 gate `.py` → 73 files / 45 gate `.py`**; nothing was
removed. The manifest regenerates to **1688 files / sha256 `5a27b0df8df38c46`** at `193c567`, the
zip bakes twice to **`9b90edcbfb5976e6b8036f21dc368f5820ad1c48a65ff4c9d9288d5f52ca7b51`**,
`--check` is GREEN against the commit, and the dataviz gate was **RUN inside the unzipped pack and
MUTATION-PROVEN there** — take the receipt away and it goes red, touch a test page and it says
STALE. Release gates: **7/9, the same two known pre-bake reds** lane R recorded.

COUNTS: findings 2 · ruling-shaped 1 (carried from lane R, not new) · declared skips 2 (unchanged)

---

## Step 1 — what was dropped, and the two different causes

Lane R named the fact; this lane measured the cause of each.

### (a) `_validate_dataviz.py` — the receipt was in NO group's `match`

`_gen_pack_manifest.py:groups()` has no group whose `match` claims `knowledge/_tests/`. So
`knowledge/_tests/chart-engine/_receipts.json` — the committed evidence s260-D3 made dv-004 read —
was **unclaimed, not excluded by a named reason**. Inside the staged pack the gate therefore hit
its own no-receipt arm:

    ✗ dv-004: donut is ENGINE-DRAWN (no marks in the markup) and there is no driven receipt at
      knowledge/_tests/chart-engine/_receipts.json. Record one: python3 knowledge/_drive_chart_engine.py

Green in the full tree, red in the pack ⇒ the differential arm (`_gen_pack_manifest.py:1029`)
classifies **REPO-BOUND** ⇒ the gates group drops it. **#260's own receipt route took the gate out
of #260's own pack** — the exact shape #223 already paid for [[gate-cannot-pass-in-one-environment]].

    _validate_dataviz.py | REPO-BOUND | runs, but its subject is not in the pack — it is GREEN
    against the full repo and RED here | full-tree PASS

### (b) `_validate_fit_physics.py` — it CRASHED where its three siblings REFUSE

Not a packaging fact at all. Driven in the probe stage:

    playwright._impl._errors.Error: BrowserType.launch: Executable doesn't exist at
      …/chromium_headless_shell-1234/chrome-linux/headless_shell
    ╔══════ Looks like Playwright was just installed or updated. … ╝

`classify()` reads `Traceback (most recent call last)` and answers `REPO-BOUND — crashed`. The gate
was written at #249 with a bare `p.chromium.launch(args=['--no-sandbox'])`. **#223 already fixed
exactly this for `_validate_state_contrast.py`, `_validate_hit_area.py` and
`_validate_descender_computed.py`** — its own docstring records the consequence in advance: *"on a
box with no browser binaries this gate flipped NEEDS-DEP → REPO-BOUND and silently left the ship
list"*. The younger gate never got the treatment. At v1.0.7 the probe box had no `playwright`
module at all, so `MODNOTFOUND` caught it first and it read NEEDS-DEP; here the module is installed
and only the binaries are absent, so the traceback escaped. **Environment-shaped in appearance,
error-handling-shaped in fact.**

## Step 2 — the fix, inside existing policy

⛔ **No gate was weakened. No "skip if no receipt" path was added — s260-D3 says the route is never
skipped, and the mutation drive in Step 5 proves it still is not.**

### `GATE_DATA_CANDIDATES` — the sanctioned home, used the way #256 used it

The constant's own comment already states the rule: *"Data files the gates read that are NOT part
of any other group but must ride with the gates for them to have anything to check."* #256 added
`roles.json` / `shapes.json` / `when-fields.json` there for the identical reason
(Dave: *"ship — completeness over convenience"*). Eight paths added, each for a stated reason:

| path | why it must ride |
|---|---|
| `knowledge/_tests/chart-engine/_receipts.json` | the evidence itself — 116 KB, committed |
| `knowledge/_tests/chart-engine/{bar,combo,donut,line,sparkline,stacked-area}.html` | **the freshness hash covers them.** Each page's receipt records a `sources` sha256 map and `driven_dv004()` re-hashes every row ON DISK before grading; the FIRST row in every map is the test page itself. Ship the receipt without the pages and the gate reads `(file is missing)` and is BLOCKING-red in the pack for a reason no designer can fix |
| `knowledge/_drive_chart_engine.py` | the remedy dv-004 names **in its own failure text**, by the rule `DOOR_COMPANIONS` already states in prose ("a packed door travels with its builder"). Not routed through that closure because it fills a companion BESIDE a door that landed elsewhere; here door and driver both land in `knowledge/`, so the seed would be a no-op copy |

**⚠ NO PATH RESOLUTION NEEDED FIXING, and this was checked rather than assumed.** The remaining
`sources` rows are `knowledge/canon/*` (`canon.css`, `type.css`, `dv-behaviour.js`,
`dv-legend.js`, `dv-donut-sweep.js`, `dv-render.js`, `dv-render-<type>.js`) and are already owned
by `engine-canon.canon`. `driven_dv004()` resolves every row against `root = os.path.dirname(HERE)`
— the repo root in the tree, the **pack root** inside the pack — so the SAME receipt is fresh in
both, with the bytes byte-identical either side. Step 5 drives that claim rather than asserting it.

### `_validate_fit_physics.py` — the #223 treatment, fourth copy

Added `FitPhysicsUnreachable` + `_launch_chromium(p)`, mirroring `_validate_state_contrast.py`'s
shape, and an `except` in `__main__` that answers `_could_not_ask.EXIT`:

    $ python3 knowledge/_validate_fit_physics.py
    COULD-NOT-ASK: _validate_fit_physics.py — playwright is installed but its BROWSER BINARIES are
    not — the chromium executable it drives was never downloaded (Error: BrowserType.launch:
    Executable doesn't exist at …/headless_shell) — this gate measures rendered geometry and cannot
    be proven without a browser; install one with `playwright install chromium`
    rc=77

⚠ Keyed on the LAUNCH ACTUALLY FAILING, never on a path-glob guess about where binaries ought to
live [[feedback-measuring-tool-must-not-guess]] — `except Exception` is scoped to the single
`launch()` call. The import arm refuses the same way. **The 19 checks are untouched**: with a
browser present, `_launch_chromium` is `launch()` and nothing more. Reproducible on any machine by
taking the browser away, which is how it was proven here.

Commit **`193c567`** — `#260 R2: the driven-receipt evidence ships, and fit-physics refuses instead
of crashing` (2 files, +92/−3). Generator `--selftest` after the edit: **216 bites, 0 fail(s)**.

## Step 3 — the manifest, regenerated

    bash apollo-spider/build-designer-pack.sh --manifest --commit 193c567 --full-stage /var/tmp/full9
    probing the gates at 193c56772bfe (measured, not read by eye)…
    manifest -> knowledge/_release/_pack_manifest.json
      commit 193c56772bfe  files 1688  bytes 43882477  sha256 5a27b0df8df38c46

⚠ `--full-stage` again, and for lane R's reason: without it the differential arm never fires and
the ship set is decided by a flag. **That the flag is optional at all is still ruling-shaped and is
still not taken here** (lane R, RULING-SHAPED 2 — carried, not re-argued).

| probe | 41 RUNNABLE · 4 NEEDS-DEP · 9 REPO-BOUND |
|---|---|
| v1.0.7 | 41 / 4 / 9 |
| v1.0.8 at `7d45a12` | 40 / 3 / 11 |
| **v1.0.8 at `193c567`** | **41 / 4 / 9 — back to v1.0.7's shape** |

    _validate_dataviz.py     RUNNABLE  | ran clean, verdict PASS | selftest green
    _validate_fit_physics.py NEEDS-DEP | playwright install chromium

**Gates group, before → after: 63 files / 43 gate `.py` → 73 files / 45 gate `.py`.** The ten added
paths, diffed out of the two manifests rather than counted by eye:

    _validate_dataviz.py · _validate_fit_physics.py · _drive_chart_engine.py ·
    _tests/chart-engine/_receipts.json · bar.html · combo.html · donut.html · line.html ·
    sparkline.html · stacked-area.html
    REMOVED: []

Manifest files 1678 → 1688; bytes 43,682,135 → 43,882,477 (+200,342 B ≈ 196 KB).

Commit **`1459e55`** — `#260 R2: v1.0.8 manifest at 193c567 — the dataviz gate is back in the ship
set (45 gates)` (manifest + probe + the go/no-go page and its re-injected review overlay).

## Step 4 — the bake, proved twice

    bash apollo-spider/build-designer-pack.sh --dry-run --out-dir /var/tmp/bake1r2 --commit 193c567
    sha256: 9b90edcbfb5976e6b8036f21dc368f5820ad1c48a65ff4c9d9288d5f52ca7b51   size: 20M

    bash apollo-spider/build-designer-pack.sh --dry-run --out-dir /var/tmp/bake2r2 --commit 193c567
    sha256: 9b90edcbfb5976e6b8036f21dc368f5820ad1c48a65ff4c9d9288d5f52ca7b51   size: 20M

    cmp /var/tmp/bake1r2/… /var/tmp/bake2r2/…            → rc 0, no output — BYTE-IDENTICAL

    bash apollo-spider/build-designer-pack.sh --check /var/tmp/bake1r2/Apollo-Spider-v1.0.8.zip \
         --commit 193c567
    CHECK GREEN — /var/tmp/bake1r2/Apollo-Spider-v1.0.8.zip matches the manifest at 193c56772bfe

    bash apollo-spider/build-designer-pack.sh --selftest
    selftest: 216 bites, 0 fail(s)
    === refusal: --release on a dirty tree ===            green — refused, as it must
    === refusal: --release without Dave's ratification === green — manifest status is PROPOSED,
                                                           so --release cannot run

⛔ `RATIFY_IDS` untouched, no ruling id invented, the frozen gate's apollo-spider literal still
`v1.0.7`. The cut stays **PROPOSED**. The sentence Dave says and the command the conductor runs
afterwards are unchanged from lane R's report, except that the commit is now `193c567` and the
expected zip fingerprint is `9b90edcb…`.

## Step 5 — the gate RUN INSIDE THE UNZIPPED PACK, and mutation-proven there

⚠ Lane R's UNPROVEN list carried *"whether the v1.0.8 zip opens correctly for a cold designer:
`--check` proves it against the manifest, which is not the same as unzipping it and driving the
gates from inside"*. **That carry is now discharged for this gate.**

    unzip -q /var/tmp/bake1r2/Apollo-Spider-v1.0.8.zip -d /var/tmp/unz9
    cd /var/tmp/unz9/Apollo-Spider-v1.0.8
    ls knowledge/_tests/chart-engine/
      _receipts.json  bar.html  combo.html  donut.html  line.html  sparkline.html  stacked-area.html

    PYTHONPATH=$PWD/knowledge python3 knowledge/_validate_dataviz.py
      [PASS] snippets/Chart-donut.reference.html  (2 charts, 0 blocking, 1 advisory)
      …
      ✅ DataViz gate passed (14 chart surface file(s))
    rc=0

The graded snippet set inside the pack `diff`s empty against the repo's — same surfaces, not a
smaller question.

**⛔ A GREEN IS NOT A PROOF UNTIL IT CAN FAIL [[mutation-tests-the-clause-not-the-feature]].** Two
mutations driven on the unzipped stage:

| mutation | rc | the gate's own words |
|---|---|---|
| `mv knowledge/_tests/chart-engine/_receipts.json` away | **1** | `✗ dv-004: donut is ENGINE-DRAWN (no marks in the markup) and there is no driven receipt at knowledge/_tests/chart-engine/_receipts.json. Record one: python3 knowledge/_drive_chart_engine.py` |
| append one byte to `knowledge/_tests/chart-engine/donut.html` | **1** | `✗ dv-004: the driven receipt for donut.html is STALE — knowledge/_tests/chart-engine/donut.html has changed since it was driven. Re-drive: python3 knowledge/_drive_chart_engine.py` |

That is the whole claim, driven: **the pack's green comes from the receipt, the freshness hash
resolves the test page correctly at the PACK root, and there is no skip path.** And the remedy both
messages name is now in the pack — `knowledge/_drive_chart_engine.py`, 20,112 B, `--help` rc 0.

## Step 6 — the nine release gates, pass 3

⚠ Gates 1–7 do not live at `knowledge/_gate_*.py` (where the shorthand implies). Their only home is
**`knowledge/_release/`** — measured here after a `find`, the same shorthand trap lane R hit on
gate 9.

| # | gate | rc | line |
|---|---|---|---|
| 1 | `_release/_gate_frozen_release.py --check` | 0 | `PASS — 3 arm(s) asked, no frozen surface moved.` (apollo-spider row still `v1.0.7` — correct pre-bake) |
| 2 | `_release/_gate_frozen_release.py --selftest` | 0 | `selftest: 14 bites, 0 fail(s)` |
| 3 | `_release/_gate_release_audit.py --check` | 0 | `PASS — the manifest … byte-identical to a fresh generation at 193c56772bfe (1688 files, sha256 5a27b0df8df38c46)` |
| 4 | `_release/_gate_release_audit.py --selftest` | **1** | `RED [pack/frozen-history-is-skipped-not-failed] … got rc=1` |
| 5 | `_release/_gate_release_audit.py --pack` | **1** | `❌ the manifest reads version 'v1.0.8' and NO zip in dist/ carries it … the manifest names a release nobody baked.` |
| 6 | `_release/_gate_ci_template.py --check` | 0 | `PASS — the template parses, ships what it calls, and hides nothing.` |
| 7 | `_release/_gate_ci_template.py --selftest` | 0 | `selftest: 10 bites, 0 fail(s)` |
| 8 | `build-designer-pack.sh --selftest` | 0 | `selftest: 216 bites, 0 fail(s)` |
| 9 | `cold-start/gen_projections.py --check` | 0 | `gen_projections --check OK — 3 projection(s) and 3 PLACED host file(s) in sync…` |

**7/9 — [4] and [5] are the KNOWN PRE-BAKE PAIR, expected and unchanged.** [4] is [5]'s arm. They
say "the manifest names a release nobody baked", which is the true state of a PROPOSED cut, and
⛔ they are not to be made green by baking — the bake is `--release` and that is Dave's word.

### Declared skips, unchanged from lane R

- `knowledge/_validate_screen.py` — NOT RUN: its ledger writer still clobbers tracked files
  (#258 RSQ 1, unrepaired). Its write policy is ⬛ Dave's.
- `knowledge/_tests/test_gates.py` — SKIPPED: copytrees ~5 GB, ENOSPC in this sandbox.

## Commits this lane made

| sha | subject |
|---|---|
| `193c567` | `#260 R2: the driven-receipt evidence ships, and fit-physics refuses instead of crashing` |
| `1459e55` | `#260 R2: v1.0.8 manifest at 193c567 — the dataviz gate is back in the ship set (45 gates)` |
| `9f5fafa` | `#260 R2: the R2 report — both dropped gates back, mutation-proven inside the unzipped pack` |

NOT PUSHED — Dave pushes via GitHub Desktop. `DOC_ROW_ACK` declared on every commit: the unrowed
subreports are lanes A's and R's own filed reports and their `_state` rows belong to those lanes or
the wrap, not here.

## Ruling-shaped, still open

⬛ **`--full-stage` decides the ship set and is an OPTIONAL flag** (lane R, RULING-SHAPED 2).
Carried unchanged. Run `--manifest` without it and the differential arm at
`_gen_pack_manifest.py:1029` never fires, so a gate that is red-in-pack / green-in-tree ships
anyway and the pack's own gate list becomes a function of how the conductor typed the command.
This lane's fix makes the dataviz gate honest under BOTH forms, which narrows the blast radius but
does not close the hole. **Not taken here.**

⚠ NOT ruling-shaped, and stated so it is not mistaken for one: `knowledge/_tests/` remains
unclaimed by any group's `match`, and the eight paths ride via `GATE_DATA_CANDIDATES` — the
mechanism that exists for precisely this. If a later lane wants the directory claimed by a group of
its own, that is a refactor, not a decision.

## UNPROVEN from this seat

- `_validate_fit_physics.py`'s 19 checks under a REAL browser — no chromium binary on this box.
  The refusal path is driven; the measurement path is unchanged code and was not re-run.
- CI green on GitHub (nothing pushed; `_build_all.py` sandbox-impossible — the #257 carry stands).
- The other 44 shipped gates were not individually driven inside the unzipped pack; the probe
  drives each one in a staged copy, which is the manifest's own measurement, and the dataviz gate
  was additionally driven in the real unzipped artefact.
