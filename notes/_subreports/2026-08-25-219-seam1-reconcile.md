# `#219`-seam1 — the reconcile: every path accounted, the serial re-driven, four reds green, 11 thumbnails PROVEN churn and restored

session: `#219` · 2026-08-25
window: `#219` crank, wave 1 — **seam-1 reconcile** (after lanes 1, 2, 3 filed)
sub index: `seam1`
brief: `notes/_briefs/2026-08-25-219-crank-divvy.md`
tokens: UNMEASURED — a sub cannot read its own `message.usage`; the conductor's gauge is the authority.

## VERDICT

**CLEAN TO COMMIT, with two declared reds that are PRE-EXISTING AT HEAD and neither lane's.**
29 working-tree lines (28 at reconcile open, plus this report), every one attributed. The 11 changed thumbnails were **proven** pixel-identical
re-encodes (Pillow `ImageChops.difference` → `getbbox() is None` on all 11) and **restored from HEAD**
— the tree is 11 lines lighter than lane 1 left it. The ordered serial was re-driven whole,
ramp first / index last, and came back **idempotent**: every step reported *no change / 0 written / in
sync*, so lane 1's and lane 2's `canon.css` edits are mutually consistent and the co-ownership did not
strand anything. All four previously-red checks are **green locally**, verbatim below.

The two declared reds — `_validate_type_blast_radius.py` and the `_capture_gate.py --selftest` triple —
were **both measured against HEAD's own bytes** and reproduce there. Neither is a lane's doing, and
lane 2's `[40]` fix could not have cleared the blast-radius red (proof below: the escaping selector
matched at HEAD too). Their remedies are ruling-shaped and were not taken.

COUNTS: findings 6 · ruling-shaped 2 · UNPROVEN 2

---

## ① PATH-BY-PATH MANIFEST — 29 lines, 0 unaccounted

Ownership taken from each lane's own paths list. `restored` = reverted to HEAD by this reconcile.

### Modified — lane 1 (segmented adoption)

| path | lane | disposition |
|---|---|---|
| `knowledge/snippets/Segmented-control.reference.html` | 1 | include — the CAUSE edit (radius locals + `xs/s/m/l` grammar) |
| `knowledge/tokens/layout.json` | 1 | include — `s202-D1` base SIZE mint restored (finding 1 of lane 1) |
| `knowledge/gen_snippet_tokens.py` | 1 | include — router taught `size/` + `padding/` |
| `knowledge/_validate_snippets.py` | 1 | include — same router, second copy |
| `knowledge/_TYPE-BLAST-GATE.md` | 1 | include — **gate's own generated report**, now records the red honestly |
| `knowledge/_type_ratchet.json` | 1 | include — auto-ratchet `1093 → 1091`, shrink-only, legal |
| `showroom/index.html` | 1 | include — generated (library index payload) |
| `showroom/segmented-control.html` | 1 | include — generated; `10 → 30 token(s)`, console `0 → 16 var(s) re-bound` |

### Modified — lane 2 (CI drift)

| path | lane | disposition |
|---|---|---|
| `knowledge/canon/gen_canon_components.py` | 2 | include — `strip_css_noise()`, the `ds-039` third-species fix |
| `knowledge/_capture_gate.py` | 2 | include — `BOOT_DELTA_TAIL_RE` comparatives + 9 selftest arms |
| `knowledge/_gen_chain.py` | 2 | include — measured-tier label + one-measurer bite |
| `knowledge/snippets/Navigations.reference.html` | 2 | include — generated `AUTO-TOKENS` block, 28 lines, alpha ramp only |
| `showroom/navigations.html` | 2 | include — generated downstream of the line above (base64 payload re-embed) |

### Modified — co-owned lanes 1 + 2

| path | lane | disposition |
|---|---|---|
| `knowledge/canon/canon.css` | 1 + 2 | include — `AUTO-GENERATED TOKENS` + `AUTO-COMPONENTS` + `AUTO-THEMES`; **re-driven at the seam, idempotent** |
| `knowledge/_memento-index.json` | 2 (+ seam) | include — regenerated last, twice (once for the serial, once after the runbook edit) |

### Modified — this reconcile (seam)

| path | lane | disposition |
|---|---|---|
| `knowledge/_state.json` | seam | include — six existence rows `W-165 … W-170` (§④) |
| `knowledge/_RUNBOOK-render-verify.md` | seam | include — FIFTH STRATUM, addition-only (§⑤) |
| `knowledge/_RUNBOOKS.md` | seam | include — generated index, one date line, consequence of the runbook edit |

### Restored — 11 thumbnails, PROVEN encode churn

`showroom/_thumbs/` — `chart-butterfly-v` · `chart-combo` · `chart-donut` · `chart-line` ·
`chart-scatter` · `chart-sparkline` · `foundation-logos` · `loading-indicator` · `secure-entry` ·
`skeleton-loader` · `video-player` (`.png`).

**lane 1 → restored.** All eleven restored via `git show HEAD:<path> > <path>` (never `git checkout` —
this mount refuses it and it once ate a mint). Post-restore `git status` shows **0** `_thumbs` lines,
and both `gen_library_214.py --check` and `gen_showroom.py --check` stayed green over the restore, so
nothing downstream depended on the new bytes.

### UNCLAIMED — 2 lines, investigated, evidence given

| path | evidence | disposition |
|---|---|---|
| `notes/_REHEARSAL-LOG.jsonl` | +2 lines, both `{"date":"2026-08-25", "fails":0, ...}` — one `wrap-open`, one `rehearse`. Written by `knowledge/_checkin.py` (and `_capture_gate.py`), never by a lane. Lane 1 finding 9 records it as **already present at lane open**; lane 2 lists it under "NOT this lane"; lane 3 claims nothing. | **conductor's own check-in telemetry** — include, but it is the conductor's line to own, not a lane's |
| `notes/_dream/_GRADE-DECISIONS.jsonl` | +1 line, `{"kind":"alert", ..., "at":"2026-08-25T10:29:20"}`. Written by `knowledge/_checkin.py` / `_gardener.py`. Same three-lane position as the row above. | **conductor's own check-in telemetry** — include, same caveat |

**UNCLAIMED count: 2.** Both are append-only ritual telemetry with a named writer; neither is a lane
artefact and neither was discarded. ⚠ Stated rather than assumed: I did not *watch* the conductor's
`_checkin.py` runs produce them — the attribution is from the writer grep plus lane 1's open-state
record, not from a witnessed write.

### Untracked — 9 lines, all claimed

| path | lane | disposition |
|---|---|---|
| `notes/_briefs/2026-08-25-219-crank-divvy.md` | conductor | include — rowed `W-165` |
| `notes/_subreports/2026-08-25-219-lane1-segmented-adoption.md` | 1 | include — rowed `W-166` |
| `notes/_subreports/2026-08-25-219-lane2-ci-drift.md` | 2 | include — rowed `W-167` |
| `notes/_subreports/2026-08-25-219-lane3-review-regen.md` | 3 | include — rowed `W-168` |
| `notes/_subreports/2026-08-25-219-seam1-reconcile.md` | seam | include — **this report**, rowed `W-171` |
| `notes/_subreports/assets/2026-08-25-219-lane1-segmented-adoption/` | 1 | include — 7 evidence files |
| `notes/_subreports/assets/2026-08-25-219-lane3-review-regen/` | 3 | include — 2 evidence files (`name-check.txt`, the crop PNG) |
| `knowledge/_render/verify_segmented_219.py` | 1 | include — rowed `W-169` |
| `reviews/SEGMENTED-ADOPTION-2026-08-25-v1.html` | 1 | include — rowed `W-170` |

### LANE 3'S ZERO-CHANGE CLAIM — VERIFIED

`git status --porcelain` carries **no line** under `reviews/` other than lane 1's new
`SEGMENTED-ADOPTION-2026-08-25-v1.html`, and **no line** under `knowledge/_render/` other than lane 1's
new `verify_segmented_219.py`. The three bento pages (`BENTO-CANON-2026-08-23-v2.html`, `-v3.html`,
`GALLERY-COMPARE-2026-08-23-v1.html`) and the three `gen_bento_*_217.py` generators are **untouched**,
and no `-vN+1` duplicate was emitted. Lane 3's only tree footprint is its report plus its `assets/`
directory. **Claim holds exactly as filed.**

---

## ② THE ORDERED SERIAL, RE-DRIVEN AT THE SEAM — steps in order, each its own call

`canon.css` is co-owned by lanes 1 and 2 this wave, so the whole serial was re-run rather than
spot-checked. Never `_build_all.py` (a partial run strands the tree). `tiktoken` was already resident
in this sandbox (`import tiktoken` → ok) so the cold-start `pip install --break-system-packages` was a
no-op, not a skip. Order taken from `knowledge/_build_all.py::STEPS` and
`knowledge/_RUNBOOK-compose-from-canon.md` — **ramp first, index last**.

| # | step | verdict (verbatim) | rc |
|---|---|---|---|
| 0 | `canon/gen_canon_tokens.py` | `TOTAL: 577 root vars, 195 dark overrides` / `Wrote …/canon/canon.css` | 0 |
| 1 | `gen_token_ramp.py` **(RAMP FIRST)** | `gen_token_ramp: 0 file(s) synced (0 with block, 0 block-removed), 147 already in sync.` | 0 |
| 2 | `canon/gen_canon_components.py` | `gen_canon_components: no change (135 components in sync).` | 0 |
| 3 | `gen_snippet_tokens.py` | `4804 manifest bindings across 135 snippets + 9 tranches; 0 value(s) projected; 0 canon.css literal(s) projected.` | 0 |
| 4 | `canon/gen_theme_cascade.py` | `gen_theme_cascade: no change (in sync).` | 0 |
| 5 | `gen_showroom.py` | `135 page(s) -> showroom/ (0 written, 0 orphan(s) pruned; index owned by knowledge/_render/gen_library_214.py)` | 0 |
| 6 | `_render/gen_library_214.py --check` | `gen_library_214 --check OK — 142 component(s), index + index.json + stub in sync.` | 0 |
| 7 | `_build_memento_index.py` **(INDEX LAST)** | `1791 records → knowledge/_memento-index.json` | 0 |

Then, after the runbook edit of §⑤ (which is corpus the memento index reads):

| # | step | verdict | rc |
|---|---|---|---|
| 8 | `gen_runbook_index.py` | `runbook index: 17 runbooks -> _RUNBOOKS.md` | 0 |
| 9 | `_build_memento_index.py` **(INDEX LAST, again)** | `1791 records → knowledge/_memento-index.json` | 0 |

**`_render/gen_thumbs.py` was DELIBERATELY NOT RE-RUN, and this is a decision, not an omission.**
Every upstream step above reported *no change / 0 written*, so nothing a thumbnail depends on moved;
the generator has no `--check` arm and re-shoots all 142 unconditionally, so running it would have
manufactured the very encode churn this reconcile just proved and removed — 142 churned files instead
of 11. `gen_library_214.py --check` (which bites on a missing thumbnail) and `gen_showroom.py --check`
were both driven green **after** the 11 restores, which is the reading that matters.

⚠ **The serial came back IDEMPOTENT** — every write step said *no change* on a tree two lanes had
edited. That is the co-ownership verdict: lane 1's snippet edit and lane 2's `ds-039` generator fix
compose, and neither had left `canon.css` mid-flight.

---

## ③ THE FOUR CHECKS — verbatim, all green

```
[40]   gen_token_ramp: 0 file(s) DRIFTED (0 with block, 0 block-removed), 147 already in sync.        rc=0
[45]   gen_canon_components --check OK — 135 components in sync.                                      rc=0
[50]   gen_theme_cascade --check OK — 230 override path(s), 387 component projection(s) in sync.      rc=0
[107]  memento index --check: current (1791 records)                                                  rc=0
```

⚠ `[50]` reads **387** component projections where lane 2's report quotes 386 — the difference is
lane 1's segmented manifest bindings landing after lane 2 filed. Not a discrepancy; a sequence.

### Render-verify, lane 1's clean arm — RE-DRIVEN GREEN AFTER THE SEAM SERIAL

`knowledge/_render/verify_segmented_219.py` (no `--mutation`), driven per
`knowledge/_RUNBOOK-render-verify.md` with a **fresh** `#138` symlink font farm
(`/var/tmp/fonts-s219seam1` + `.conf`, 10 faces), `PLAYWRIGHT_BROWSERS_PATH=/var/tmp/pw-browsers-215`,
`LD_LIBRARY_PATH=/var/tmp/chromelibs-s213e2/root/usr/lib/aarch64-linux-gnu`, `TMPDIR=/var/tmp`:

```
128 measurement(s) across 32 theme x mode x scale cells

PASS — every track and thumb radius equals its theme's minted token; console rounds, the three
square themes stay square, hit zone = max(44, height).                                            rc=0
```

Console reads `xs 6/0 · s 8/2 · m 10/4 · l 12/6` (track/thumb); mono, legacy and supercharge read
`0/0` in all eight cells each; heights `24/36/44/48`; hit floor `44/44/44/48`. **Tree assertion after
the render (`#138`):** `ls -a knowledge/assets/fonts/_desktop/TTF/ | grep -c '^\.uuid'` → **0**.

### `_validate_type_blast_radius.py` — ⛔ STILL RED, and lane 2's `[40]` fix could NOT have cleared it

```
❌ type-binding blast-radius gate FAILED — see knowledge/_TYPE-BLAST-GATE.md
     - ESCAPED: `.search input` now matches ['Navigations.reference.html'] — outside its
       acknowledged radius. Namespace it, or `--update` and review the diff.                      rc=1
```

**Attribution PROVEN, not inferred.** The gate's matcher is `matches(selector, html, classes)` —
"every simple part must be present": the file needs a `class="… search …"` **and** an `<input`. Both
were driven against HEAD's own bytes and against the worktree's:

```
HEAD      matches('.search input') = True | 'search' in classes: True
WORKTREE  matches('.search input') = True | 'search' in classes: True
```

The lane-2 diff to `Navigations.reference.html` is **28 insertions, 0 deletions, all of them the
`AUTO-TOKENS` alpha ramp** — no markup, no `class=`, no `<input`. So the selector escaped **at HEAD**
and the committed `_TYPE-BLAST-GATE.md` (`.search input` · 4 files · PASS) was a **stale generated
artefact** from a run predating the markup that broke it. Running the gate today is what made the red
visible; it did not create it. Lane 1 called this "pre-existing, NOT mine" and was right, for a
slightly different reason than the one it gave.

⛔ **Not fixed here.** Both remedies the gate names are recorded conscious acts — `--update` rewrites
an *acknowledged blast radius*, and namespacing `.search input` is a `T-D9`/`T-D12` typography edit.
Ruling-shaped, see §⑥ Q1.

### `_capture_gate.py --selftest` — 3 failures, ALL THREE PRE-EXISTING AT HEAD

Worktree run: `capture gate [wrap]: 5 in scope · 4 fail · 2 warn`, with

```
❌ selftest: M10: a fat §A/§C warned the CHAIN — the re-point did not take. …
❌ selftest: M10: an ordinary chain warned — the budget fires on everything
❌ selftest: #70/#71 non-catch: _gen_chain.py --selftest is NOT green — …                          rc=1
```

Lane 2 reported *"exactly one failure"*. It is **three**. Rather than adjudicate by reading, I drove
it: `knowledge/_capture_gate.py` and `knowledge/_gen_chain.py` were swapped to their **HEAD bytes**
(backed up first, `trap`-restored, `cmp`-verified byte-identical on the way back — both files are
confirmed `M` with lane 2's 46 / 35 insertions still in place). The HEAD-version run produces
**the same three failures, by the same names**. ⇒ **Lane 2's B and C edits introduced no capture-gate
red.** The two `M10` chain-budget bites are a standing red the lane's regression run did not surface,
not a regression it caused.

---

## ④ STORE ROWS — six minted through `_state.py::add()`, `#185` forgotten-document class

Minted with the store's own machinery (`add()` refuses without a close condition; `save()` sorts), in
the exact grammar of the `#218` crank-seam rows `W-159` / `W-160` / `W-163` / `W-164`. Next fresh id
was `W-165` per `s215-D1`.

| id | home | owner | closes_when (abridged) |
|---|---|---|---|
| `W-165` | `notes/_briefs/2026-08-25-219-crank-divvy.md` | claude | retired with the `#219` record once the lanes land committed and the lane-4 hold is released or dropped |
| `W-166` | `notes/_subreports/2026-08-25-219-lane1-segmented-adoption.md` | dave | Dave rules lane 1's five ruling-shaped questions |
| `W-167` | `notes/_subreports/2026-08-25-219-lane2-ci-drift.md` | dave | Dave rules lane 2's three ruling-shaped questions |
| `W-168` | `notes/_subreports/2026-08-25-219-lane3-review-regen.md` | dave | how `_LIVE-STATE.md` residual ③ is discharged |
| `W-169` | `knowledge/_render/verify_segmented_219.py` | claude | absorbed into a standing render gate, or retired when the adoption is signed |
| `W-170` | `reviews/SEGMENTED-ADOPTION-2026-08-25-v1.html` | dave | Dave has looked at the page and ruled the legacy→minted radius mapping |
| `W-171` | `notes/_subreports/2026-08-25-219-seam1-reconcile.md` | claude | retired with the `#219` record once seam-1 commits and Q1 is ruled or committed-with-declared-red |

`W-171` is **this report**, rowed at creation like its three siblings — the `#185` class does not
exempt the document that names it. Seven rows, not six.

Every row's `body` is the precedent sentence verbatim: *"Existence row minted at the `#219` crank
seam-1 reconcile. Rules nothing, closes nothing."* No row closes anything, reopens anything, or
restates a lane's prose as a decision.

**Gate + selftest, after:**

```
_state selftest: 57 bites, all GREEN                                                              rc=0
_state.check()  → ok True, fails []
doc-row gate: population 69 (added >= 2026-08-15, PICKED) · of which staged-in-THIS-commit 0
  (#207 postscript: the single-commit blindspot) · unrowed 0
✅ PASS — every in-scope document has a store row.                                                 rc=0
```

Store counts after: `total 226 · live 147 · open 147 · done 60 · parked 19 · unconditioned 14`.

⚠ **ONE PICK DECLARED, so the conductor can overrule it cheaply.** All six rows carry
`project: "apollo"`, following the `#218` crank-seam precedent where every seam existence row used
`apollo`. Lane 2's subject matter is arguably `memento` (capture gate, chain, memento index) — the
enum has exactly two values and widening it is Dave's. **One-line flip if the conductor disagrees**;
it is a grouping label and nothing downstream is asserted on it here.

---

## ⑤ RUNBOOK ADDITION — `_RUNBOOK-render-verify.md`, FIFTH STRATUM, addition-only

Lane 3's finding 6 folded in as a new stratum, placed **above** the `#215` FOURTH STRATUM (the file
runs newest-first) and **nothing trimmed** — the fourth stratum's *"a FOREIGN session's artefact;
re-extract, don't rely"* stands untouched, and the new stratum names itself as what "don't rely" looks
like when it comes true.

**Re-verified first-hand before writing it — not relayed from lane 3's prose:**

```
ls -la /var/tmp/chromelibs/                     → total 24, . and .. only — HOLLOW
ls /var/tmp/chromelibs-s213e2/root/usr/lib/aarch64-linux-gnu/
                                                → libXdamage.so.1, libXdamage.so.1.1.0
LD_LIBRARY_PATH=…-s213e2/… ldd headless_shell | grep -c "not found"   → 0
```

The stratum carries the two-command move (`ls -A` the dir, then `ldd | grep "not found"` — never a
launch attempt) as a copy-pasteable block, and names the class:
`[[stale-mount-corroborates-a-stale-premise]]` for the hollow dir, `[[refusal-names-the-first-obstacle]]`
for why `libXdamage.so.1: cannot open shared object file` reads as a broken recipe instead of an empty
directory. `gen_runbook_index.py` and `_build_memento_index.py` re-run after, both green.

---

## Findings

**1 · The 11 thumbnails are PROVEN churn — lane 1's UNPROVEN is discharged.** All 11 are
byte-different (deltas `-56` to `+307`) and **pixel-identical**: `ImageChops.difference(HEAD, worktree)`
`.getbbox()` returns `None` on every one, at identical dimensions. Restored from HEAD. Cost to prove
was one sandbox call, exactly as lane 1 priced it.

**2 · The seam serial is IDEMPOTENT over both lanes' edits.** Nine steps, every write step *no change*.
This is the strongest available statement that the `canon.css` co-ownership landed clean.

**3 · `_validate_type_blast_radius.py`'s red is older than this session and its own report file lied
about it.** The committed `_TYPE-BLAST-GATE.md` said `PASS`; the gate says `FAIL·escaped` the moment
it runs. A generated gate report that is only refreshed when someone runs the gate will keep asserting
the last green it saw — `[[ritual-output-is-not-evidence]]`, and `[[conclusions-are-debt-s129-d5]]`:
"passed" is a property of a moment.

**4 · Lane 2's "exactly one failure" on `_capture_gate.py --selftest` is three, and all three are
HEAD's.** Corrected by driving HEAD's bytes, not by re-reading. The correction does not move any
verdict — lane 2 introduced nothing — but a regression baseline quoted one-third accurate is how a
future lane concludes it broke something it did not.

**5 · `gen_thumbs.py` has no `--check` arm, and that is why it manufactures churn at every seam.**
Every other generator in the serial can be asked *"would you change anything?"* for free.
`gen_thumbs.py` can only be asked by doing it, and doing it rewrites 142 PNGs whose bytes differ and
whose pixels do not. The shape of a fix is a content-hash `--check` (compare decoded pixels, not
bytes); **not built** — a new arm on a build-serial generator is outside a reconcile's licence.

**6 · Two paths in the tree belong to no lane, and both have a named writer.**
`notes/_REHEARSAL-LOG.jsonl` and `notes/_dream/_GRADE-DECISIONS.jsonl` are appended by
`knowledge/_checkin.py`. They are the conductor's own mandatory check-ins, not lane output. Listed
UNCLAIMED rather than folded silently into a lane, per the brief.

---

## RULING-SHAPED QUESTIONS

> ⛔ Neither was decided. Nothing in the tree pre-empts either.

**Q1 — `.search input` escaped its acknowledged blast radius, and the two remedies are different
decisions.** **(a)** `_validate_type_blast_radius.py --update` — records `Navigations.reference.html`
into the acknowledged set, i.e. **accepts** a fifth global binding site. Cheap, and the gate's own text
calls a new global binding *"a conscious, recorded act"*, so accepting it is a ruling, not a repair.
**(b)** Namespace the selector in `canon/type.css` + `canon/_type-bindings.json` — the debt-burndown
path the gate's footer already prescribes (`priority h2`, 25 files). Blast radius named by the gate as
seven files for the sibling `.seg.sm button` entry, so this is not a one-line edit. **(c)** Leave it
red and commit the honest report. ⚠ Whichever is picked, the gate is routed `GATE` in `_build_all.py`
(`:769`) — it will keep failing the build until (a) or (b).

**Q2 — the two `M10` chain-budget bites have been red at HEAD and nobody has been charged for
them.** They sit *inside* `_capture_gate.py --selftest`, which is the wrap ritual's own net, and they
assert that the `#33` §A/§C re-point took. Right now the selftest cannot certify that, and the wrap
runs anyway. Options, none built: **(a)** treat as a `#219` finding and price a lane; **(b)** declare
them known-red with an expiry (`[[conclusions-are-debt-s129-d5]]` triage); **(c)** leave. Naming it
because a selftest with standing reds is one step from a selftest nobody reads.

---

## UNPROVEN / CLAIMED (ADR-0016)

- **UNPROVEN: `_build_all.py` end to end.** Unchanged from both lanes' declarations — a full
  single-process run is sandbox-impossible. Bounded verification per `s172-D3`: the nine serial steps,
  the four target checks, `gen_showroom --check`, `gen_library_214 --check`, `_state --selftest`,
  `_gate_doc_rows`, the segmented render-verify clean arm, `_validate_type_blast_radius` and
  `_capture_gate --selftest` (both directions) — all quoted above. Steps this reconcile does not
  touch were not re-run.
- **UNPROVEN: the segmented `--mutation` arm was NOT re-driven at the seam.** Lane 1 drove it green
  (red on exactly `console/*/s`, contamination guard clean) before the seam serial; the serial then
  reported *no change* to `canon.css`, so the artefact the arm bit is the artefact on disk now. Carried
  forward, not re-measured. **Price to prove: one call**, `BM_MUTANT_DIR=/var/tmp/mut-s219seam1 …
  --mutation`.
- **CLAIMED (declared, not independently derived): the attribution of the two UNCLAIMED `.jsonl`
  appends to the conductor's `_checkin.py` runs.** Grounded in a writer grep plus lane 1's
  open-state record; no write was witnessed.
- **NON-REPO, declared per `s191-D2`:** the pixel-diff probe, the blast-radius matcher probe and the
  HEAD-bytes swap harness all ran as heredocs from `/var/tmp/s219seam1/`. None is a repo instrument
  and none needs to be — each is a one-shot attribution question, and its answer is quoted above
  rather than left in a file that would rot. The HEAD backups (`/var/tmp/s219seam1/bak/`) are
  scratch and `cmp`-verified spent.

## What the conductor still owns

1. **The commit itself** — nothing here was committed or pushed, and no `git checkout` was used.
2. **Q1**, or a deliberate decision to commit with `_validate_type_blast_radius.py` red.
3. **Lane 3's residual-③ discharge line** in `_LIVE-STATE.md` — a Dave-owned row; untouched here, as
   the DO-NOT-RULE binds.
4. **The `project: "apollo"` label on the six new rows** — flip `W-167` to `memento` if that reads
   better; one line, no consequence downstream.

REPLAY-THESE: §③ the four verdict lines + the blast-radius HEAD/WORKTREE matcher readings (~350 tk) ·
§① the UNCLAIMED pair with its writer evidence (~150 tk) · Q1 (~250 tk)
