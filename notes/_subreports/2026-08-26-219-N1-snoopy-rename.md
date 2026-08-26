# #219 lane N1 — THE RENAME: Apollo — Snoopy, carrying Memento — Gumdrop

**Lane:** N1 (release machinery) · **Model:** Opus · **Date:** 2026-08-26 · **Base:** `9ebd94c`
**Charter:** `s219-D7` (read verbatim), with `s219-D5` Q2/Q3 as tasks 3 and 4; `s219-D4`/`s219-D6`
read as history (D6 SUPERSEDED). Brief: `notes/_briefs/2026-08-25-219-crank-divvy.md` —
DO-NOT-RULE binds. Shape inherited from `notes/_subreports/2026-08-26-219-seam7-reconcile.md`.
**Parallel lane:** N2 owns `knowledge/_validate_*`, snippets, tokens — untouched here, with ONE
declared collision (§ ⑦).

COUNTS: findings **7** · ruling-shaped **4** · UNPROVEN **5** · stale references left in
hand-maintained files **0** (grep proof § ②) · selftest bites **118 + 14 + 10 + 8** ·
new bites added **49** (40 generator + 3 frozen-gate + 6 invocation) · mutations driven **5**,
each RED by a named bite · handoffs taken from another lane **1** (`W-189`, § ⑥b) ·
store rows minted **2** · store rows repointed after the rename **6**

⚠ **NOTHING COMMITTED, NOTHING PUSHED.** Two generated artefacts are STALE BY DESIGN and clear
on the conductor's regeneration — read § ⑧ REPLAY-THESE **before committing**.

---

## ① THE FOUR NAMING DECISIONS, DECLARED

`s219-D7` names the release and lists the rename wave; it does not spell the casing or say what
happens to the machinery's own filenames. Four decisions were taken, each stated here so the
conductor can strike any of them:

| # | decision | why |
|---|---|---|
| 1 | The directory is **`apollo-snoopy/`** | The repo's directory register is lowercase-hyphen without exception: `designer-skills-v1`, `designer-skills-v2`, `memento-package`. Title case would make this the only capitalised directory in the tree. |
| 2 | The zip is **`Apollo-Snoopy-v1.0.0.zip`** and the pack root inside it is `Apollo-Snoopy-v1.0.0/` | The brief names the zip. The pack root matches the zip stem, as `Apollo-designer-skills-v3.0.0/` did. The FILENAME register is title-case-hyphen; the PROSE register is `Apollo — Snoopy`. Both are held as constants (`PACK_SLUG`, `PACK_NAME`) with a bite asserting they agree. |
| 3 | The generator and its two artefacts take **GENERIC** names: `_gen_pack_manifest.py`, `_pack_manifest.json`, `_pack_gate_probe.json` | This is the one decision worth arguing. A Snoopy-specific name would be renamed again at Eagle, and at Columbia after that. **#219 has just paid that bill:** the v3-named generator and its two v3-named artefacts had to be chased across nine files the moment Dave named the release. The release IDENTITY belongs in the data (`pack`, `slug`, `version`, `carries`) and in the zip's name, where it is read by consumers; it does not belong in the path of the machinery that cuts *whichever* pack is current. `ADR-0017`/write-once reasoning: the live fact has one home, and pointers to it should not carry a copy of its value. |
| 4 | `build-designer-pack.sh` **keeps its name** | `s219-D7`'s wave names dir, zip, manifest, ledger, CI references, page and in-pack docs. The script is none of those, it is still literally the thing that builds the designer pack, and renaming it would churn six reference sites for no ruling. |

**The identity now lives in exactly four places, all generated:** the manifest's `pack`/`slug`/
`version`/`carries` fields, the pack `README.md`, `PROVENANCE.json`, and the page title. Every
one of them is emitted from `PACK_NAME` / `PACK_SLUG` / `VERSION` / `MEMENTO_CUT_*` in
`knowledge/_release/_gen_pack_manifest.py`. Nothing is typed twice.

### The Memento cut's identity

`Memento — Gumdrop v1.0.0` is stamped where the pack states its provenance and **nowhere inside
`memento-package/`**, exactly as briefed — that directory is the repo's own machinery and not
this release's to sign. Three stamps, all in files the stager GENERATES into the pack root:

```
_MANIFEST.json   "carries": {"name": "Memento — Gumdrop", "version": "v1.0.0", "what": …}
PROVENANCE.json  "carries": {"name": "Memento — Gumdrop", "version": "v1.0.0", "what": …}
README.md        title line: "# Apollo — Snoopy (v1.0.0), carrying Memento — Gumdrop"
                 provenance table row: | carries | `Memento — Gumdrop v1.0.0` |
                 the memento-package bullet now names it and says its version line is its own
```

The README also carries one plain sentence of the naming grammar, as briefed: *"Apollo releases
are named after the LUNAR MODULES, because they are the part that lands. Memento is named after
the COMMAND MODULES, because it is the part that navigates and remembers."*

---

## ② THE RENAME — 0 stale references, with the grep

Twelve paths moved by `git mv` (rename detection preserved, history intact):

```
designer-skills-v3/**                        -> apollo-snoopy/**                       (9 files)
knowledge/_release/_gen_v3_manifest.py       -> knowledge/_release/_gen_pack_manifest.py
knowledge/_release/_v3_manifest.json         -> knowledge/_release/_pack_manifest.json
knowledge/_release/_v3_gate_probe.json       -> knowledge/_release/_pack_gate_probe.json
reviews/RELEASE-V3-MANIFEST-2026-08-26-v1{,.REVIEW}.html
                                             -> reviews/RELEASE-SNOOPY-2026-08-26-v1{,.REVIEW}.html
```

Nine files carried references and every one was rewritten: `apollo-snoopy/build-designer-pack.sh`
(10 path refs + PACKNAME + VERSION + both heredocs), `_gen_pack_manifest.py` (27 + the group
rules + the flatten prefix), `_gate_release_audit.py` (the DIST path, the zip glob, the import,
the remedy strings), `_gate_ci_template.py` (TEMPLATE_DIR/REL + the manifest path),
`_gate_frozen_release.py` (the SURFACES row), `_frozen-releases.json` (the ledger row — see § ③),
`knowledge/_build_all.py` (4 paths + 3 step labels, **in both STEPS and ROUTE_ROWS**),
`.github/workflows/gates.yml` (2 paths + 3 step names + a fifth correction-log entry),
`.gitignore` (the dist exception + the zip glob).

**The proof, run over the whole tree:**

```
grep -rn "designer-skills-v3|_gen_v3_manifest|_v3_manifest|_v3_gate_probe|
          Apollo-designer-skills-v3|RELEASE-V3-MANIFEST"  (excluding .git, __pycache__)
```

leaves **zero** hits in any hand-maintained file. What remains, and why each is correct:

| where | count | why it stays |
|---|---|---|
| `knowledge/_rulings.json`, `knowledge/_state.json`, `notes/_subreports/*`, `_to_delete/_219-entry-inputs/*`, `_retired/**` | many | **HISTORY, frozen.** `s219-D6` and `s219-D7` quote the old name; rewriting a ruling's text to match a later rename is the thing `ADR-0017` and [[header-wins-over-audit]] forbid. |
| `_gate_frozen_release.py` ×4, `_frozen-releases.json` ×2 | 6 | The DECLARED rename — `renamed_from: "designer-skills-v3"` and the comment explaining it. These are the mechanism that makes the rename auditable; deleting them is the defect (§ ③). |
| `.github/workflows/gates.yml` ×1 | 1 | The fifth correction-log entry, which has to name what was renamed. |
| `knowledge/_release/_pack_manifest.json`, `reviews/RELEASE-SNOOPY-*.html` | 22 | **GENERATED, STALE BY DESIGN** — they are a function of a commit that does not exist yet. § ⑧. |

**A bite now guards it.** `naming/no-stale:*` greps the generator's own source for four dead
tokens on every selftest run. ⚠ The first cut of that bite went RED on itself four times — the
dead names were typed as literals into the file being grepped. They are assembled from fragments
now, and the identity comment that cited the old filenames as history was reworded. Recording it
because "weaken the assertion" was the obvious wrong fix and it was one keystroke away.

---

## ③ THE LEDGER — measured, not typed, and a hole this rename would have opened

The v3 row became the Snoopy row by **re-seeding at its own baseline commit**:

```
python3 knowledge/_release/_gate_frozen_release.py --seed --at 71bb2f77ff59…
```

`--seed` MEASURES every surface at the named rev, so this is not a hand-edit — and because the
ledger was originally seeded at that same commit, **v1's and v2's rows come out byte-identical**.
The diff is four lines, all in the third row: `id`, `note`, `surface`, `version`, plus the new
`renamed_from`. `content_sha256` and `baseline_commit` do not move: `apollo-snoopy/dist/` is empty
at `71bb2f7` exactly as `designer-skills-v3/dist/` was, and an empty surface hashes the same.

### ⛔ THE HOLE, FOUND BY DOING THE RENAME

The laundering arm — the reason the ledger is not a rubber stamp — matches rows **by id** against
the parent commit's ledger, and skips an id it cannot find. So a RENAME made the old id vanish
and the new id unmatched, and **a rename carrying a content move would have gone through the
gate in total silence**: the exact shape the arm exists to stop, wearing a different name. This
was not reasoned about in the abstract — it is what my own change was about to do.

Fixed at cause, not patched around:

- `SURFACES` takes an optional fifth field, `renamed_from`, and `--seed` writes it into the row.
- The laundering arm FOLLOWS a declared rename, so the recording is compared across the name
  change instead of skipped.
- **A new arm: a row present at the parent and gone now is RED**, with the remedy in the message
  ("if it was renamed, declare it"). A gate that has gone blind must say so
  [[instrument-without-a-consumer]].

Three bites added (11 → **14**), driven on the fixture repo as three children of the SAME parent
commit — the only shape in which "did the arm follow the rename?" is a real question:

| bite | what it drives |
|---|---|
| `rename/undeclared-vanish-bites` | rename with nothing declared ⇒ RED, naming the vanished id |
| `rename/declared-is-green` | rename + `renamed_from`, nothing moved ⇒ green |
| `rename/does-not-launder-a-move` | rename + `renamed_from` + a moved recording + no version bump ⇒ **RED**. `renamed_from` is a bridge, never an escape hatch. |

---

## ④ Q3 — THE GENERATOR WARNING: the design chosen, and why the two offered ones were not

**The conflict the brief names is real, and it is sharper than "an audit might compare them".**
`check_pack` verifies EVERY shipped file against the commit's own git blob — that is the whole
fidelity arm, 1,594 paths of it. So:

- a **bake-time guard injection** makes every injected file differ from its blob. The audit goes
  red, and the only way out is to teach the audit an exception — an audit with a carve-out in it
  is the thing this machinery was built to replace;
- a **stager-emitted wrapper + renamed original** breaks membership in both directions: the
  manifest names a path the pack no longer has, and the pack holds a path the manifest never
  named. Both arms fire, and again the fix would be an exception.

**Chosen instead: ONE copy of each generator, byte-identical everywhere, and the warning is
conditional on WHERE IT FINDS ITSELF RUNNING.**

`knowledge/_helpgate.py` gains a third leg beside `help_gate` and `write_gate`: `pack_gate`. It
walks up from `__file__` for the pack's own marker — a `_MANIFEST.json` carrying the pack
manifest's schema, sitting beside a `knowledge/` directory. The stager writes that file; this
repo has no `_MANIFEST.json` anywhere (verified by `find`). Each of the four canon generators
carries one line after its help gate.

Why `_helpgate.py` is the right home and not a new module: it already ships (the gates import it,
so it is in the measured helper closure), it is already imported by every entry point, and it is
already the file that means "the gates at the top of a script". A new module would have needed a
new group rule to ship at all.

**Both properties proved, not asserted:**

| property | proof |
|---|---|
| every audit green | `--check` on the baked zip: **CHECK GREEN — matches the manifest at 1747d52dc97e**. That check IS the byte-identity proof: it compares all 1,594 files to the commit's blobs, `_helpgate.py` and the four generators included. |
| the warning is real in a staged pack | driven in the real bake at `/var/tmp/n1/bake1/Apollo-Snoopy-v1.0.0/`: all four generators exit **2** with `✖ REFUSED (pack-gate)`, carrying Dave's framing verbatim — *"Changing a token and re-minting canon can produce canon that never passed a gate"* — and naming the flag. Nothing was minted. |
| `--i-understand` proceeds | same pack: `gen_canon_tokens.py --i-understand` ran to `TOTAL: 577 root vars, 195 dark overrides / Wrote …/knowledge/canon/canon.css`, rc **0**. The flag is CONSUMED out of `sys.argv` before the generator's own parse — a bite proves the generator sees `['--only','x']` and not the acknowledgement (#157: an unrecognised argument was once taken as a snippet filter). |
| repo behaviour unchanged | `pack_root()` returns `None` for all four generators in this repo (bitten), and all four `--check` runs are green with the *same* verdict text seam 7 quoted: `135 components in sync`, `230 override path(s), 387 component projection(s) in sync`, `AUTO-BENTO in sync`. `--help` still answers first (the help gate is upstream of the new line), and `_validate_help_gate.py` is green over **214 scripts**. |

**Five mutations, each RED by a NAMED bite, control green before and after:**

| mutation | bite that bit |
|---|---|
| M1 a canon generator unwired | `packguard/wired:gen_canon_bento.py` |
| M2 the guard never refuses | `packguard/refuses-in-a-pack` + `packguard/carries-daves-framing` + `packguard/minted-nothing` |
| M3 Q2's answer loses its ruling id | `questions/answered-cites-a-ruling:Q2` |
| M4 the dead name creeps back into the generator | `naming/no-stale:designer-skills-v3` |
| M5 the marker check drops the schema read | `packguard/wrong-schema-is-not-a-pack` |

⚠ The guard **fails OPEN**: an unreadable `_MANIFEST.json` is treated as "not a marker" and the
walk continues. A guard that raises breaks every generator it is meant to protect
[[a-crash-is-not-a-fail]]. The consequence is stated plainly: if a pack ever shipped without its
manifest, the warning would not fire — and that same missing file is a `--check` red, so the
condition is not silent.

---

## ⑤ Q2 — THE FONTS, and the licence position on the card

The 54 licensed desktop fonts were already claimed by the `library.fonts` group rule; nothing had
to be added to make them ship, and **the count is measured at three points, not typed**:

```
manifest group library.fonts   54 files
distinct ship paths under knowledge/assets/fonts/_desktop/   54
entries in the baked zip under .../knowledge/assets/fonts/_desktop/   54
```

What changed is the CARD. It used to read *"LICENCE QUESTION — see the open questions"* and point
at a question Dave has since answered. It now states the position: **settled at `s219-D5`, these
ship — "designers are in-licence", the same licence that lets the desktop set be tracked in this
private repo. The webfont packs stay out.** The `EXCLUDED` fence over the rest of
`knowledge/assets/fonts/` is unmoved.

### The five cards now carry their answers — and this is TRANSCRIPTION, not a ruling

`s219-D5` answers all five cards on that page, and the page was still asking all five. An
`answered` block was added per card: the ruling id, Dave's position in his own words, and — for
Q2 and Q3, **this lane's clauses only** — an `enacted` line saying what the pack now does. Q1, Q4
and Q5 carry his position and **no enactment claim**; their work belongs to other lanes.

The renderer paints an answered card with a RULED band and **no radio input**, and moves it out
of the "only you can settle" section — whose count is derived from the UNANSWERED set, so the
heading cannot lie in either direction. Measured on the rendered page: heading
**"Five things you settled"**, 5 ruled bands, **0 radio inputs**, headline metrics
`0 questions for you` / `5 you have settled`. (The two literal `checked` strings are prose in
Q1's body — "I checked, because the brief asked" — as seam 7 recorded.)

A bite pins the scope: `questions/Q2-and-Q3-are-this-lanes-clauses` asserts that Q2 and Q3 are
the *only* cards claiming an enactment. If a later lane enacts Q1/Q4/Q5 it must change that bite
deliberately, which is the point.

---

## ⑥ VERDICTS — every selftest the rename touches, re-driven in the final tree

| | verdict |
|---|---|
| `_gen_pack_manifest.py --selftest` | ✅ **118 bites, 0 fail** (was 78 pre-rename: +40) |
| `_gate_frozen_release.py --check` | ✅ **PASS — 3 arm(s) asked, no frozen surface moved** |
| `_gate_frozen_release.py --selftest` | ✅ **14 bites, 0 fail** (was 11: +3) |
| `_gate_ci_template.py --check` | ✅ **PASS — the template parses, ships what it calls, and hides nothing** |
| `_gate_ci_template.py --selftest` | ✅ **10 bites (mutants), 0 fail** |
| `_gate_release_audit.py --selftest` | ⚠ **8 bites, 1 fail — EXPECTED, § ⑧** |
| `_gate_release_audit.py --check` | ⚠ **RED — EXPECTED, § ⑧** |
| `_build_all.py --selftest` | ✅ **PASS — exact-ID failure routing over 140 steps** |
| `build-designer-pack.sh --selftest` | ✅ generator 118/0, and all three refusal arms green (no-commit, dirty-tree, un-ratified) |
| `_validate_help_gate.py` | ✅ **214 script(s) scanned; every entry point answers --help before it can write** |
| `.github/workflows/gates.yml` | ✅ parses as YAML — 3 jobs, `release` job intact at 12 steps |
| the four canon generators, in the repo | ✅ all `--check` green, verdict text identical to seam 7's |

### The bake, driven end to end at a SYNTHETIC commit

The manifest is a function of a NAMED COMMIT and the landing commit does not exist yet, so the
whole chain was driven against a synthetic commit built with `GIT_INDEX_FILE` —
`1747d52dc97ed67b82519f2d985a4ea353c6f990` = **HEAD + exactly this lane's files, and nothing
else** (N2's in-flight edits deliberately excluded, so the numbers below are attributable). The
real index and HEAD were untouched, verified after. It is a dangling object: never pushed, and
nothing on disk names it (§ ⑧).

| proof | result |
|---|---|
| gate probe re-run in full at the synthetic commit | 47 gates: **36 RUNNABLE · 3 NEEDS-DEP · 8 REPO-BOUND**, 43s. Byte-identical to the probe on disk except the commit line ⇒ **the rename changed no gate verdict**. The four reds are still the four the fifth card names. |
| `--manifest` | **1,594 files**, 33,891,913 bytes, sha256 `f5f2d6a0e866e468` — the same path count as before the rename, as a rename must give |
| ship list vs the old name | **0** paths containing the old prefix; `ci_template` and `skills` now under `apollo-snoopy/` |
| fonts in the manifest / in the zip | **54 / 54** |
| double dry-run bake, two out-dirs, through the REAL `build-designer-pack.sh` | **identical sha256 `93164a13510a08ae969b69892350bc8587f9965d4f356bd31459f1723df9de43`**, 13M |
| zip layout | 1,597 entries, **one root** `Apollo-Snoopy-v1.0.0/`, **0** stale path components; root holds `skills/` · `ci-template/` · `knowledge/` · `showroom/` · `memento-package/` · `_MANIFEST.json` · `PROVENANCE.json` · `README.md` |
| pack README / PROVENANCE / _MANIFEST | all three carry `Apollo — Snoopy v1.0.0` and `Memento — Gumdrop v1.0.0`; README carries the naming sentence, `s219-D7`, and the `--i-understand` paragraph |
| `--check` on the baked zip | ✅ **CHECK GREEN — matches the manifest at 1747d52dc97e** |
| tamper T1 (one byte in `knowledge/tokens/colour.json`) | ✅ **CHECK RED**, rc 1, names the file |
| tamper T2 (skills re-nested under `apollo-snoopy/`) | ✅ **CHECK RED** — 5 missing + 5 unnamed, both lists the skills. The checker checks the FLAT shape, not "either shape". |
| the page, rendered from that manifest | title `Apollo — Snoopy — the release manifest — PROPOSED`, h1 matching, the naming note present with both families, 0 stale refs, 0 radios, 5 ruled bands, `1,594 files in the pack` |

---

## ⑥b N2's HANDOFF, TAKEN — the per-gate invocation (`W-189`)

N2 filed `W-189` mid-lane: the pack calls `_validate_type_composites.py` bare, so a designer meets
the design system's whole standing composite debt on day one as if they had caused it; the gate
should be invoked `--check` (its own ratchet arm). Three touches, all in my files. **Taken, with
one change to what was specified.**

- **(c) the runner** — `gates_from_manifest()` now returns `(gate, path, argv)`, the glob fallback
  returns `(…, [])`, and `run_one()` passes the argv. The argv is read out of **the pack's own
  `_MANIFEST.json`** (`shlex.split(v["invocation"])`), never from a list copied into a third
  place. `--list` prints it beside the gate name.
- **(b) the carry-through** — no schema change was needed: the manifest already carries
  `invocation` per gate as a string, and the probe already writes it.
- **(a) NOT a hand-edit of the probe artefact.** N2 specified *"set `invocation: ["--check"]` … in
  `_pack_gate_probe.json`"* — that file is GENERATED, and hand-editing it is the defect the
  release audit exists to catch. The invocation is declared in the generator's SOURCE instead
  (`DECLARED_INVOCATIONS`), so `--probe` emits it and the artefact stays a pure generation.

⚠ **AND THE DECLARED CLAIM IS CHECKED BY THE PROBE, because driving it found the trap.** With the
entry in place, the probe at my synthetic commit produced:

```
_validate_type_composites.py | invocation='--check' | ran, verdict FAIL …
                               ! cannot read --check: [Errno 2]
```

That commit's copy of the gate has **no `--check` arm** — N2 is adding it — so the flag was read
as a FILENAME and a typed table had turned an honest red into an invented argument error. A
declared invocation is a claim, so the probe now disowns it when it does not work
(`flag_rejected()`: the flag NEXT TO an error phrase, never the flag alone) and falls back to the
measured bare run. Re-driven at the same commit: `invocation='' · verdict RUNNABLE`, the honest
bare verdict restored. Six bites cover it, including both directions of `flag_rejected`.

**Driven end to end on the runner side**, against a fake pack whose manifest declares an
invocation for a gate that exits 0 only when it receives it:

```
gates_from_manifest -> [('_validate_fake.py', …, ['--check'])]
run_one … argv  rc=0  "ARGV ['--check']"
run_one … bare  rc=1  "ARGV []"      <- the red the handoff removes
```

**What is NOT proved:** N2's 35-pass figure. It needs their `--check` arm in the commit, and my
synthetic commit deliberately excludes their files. At the landing commit the probe will emit
`--check`, keep it, and the gate's verdict should move — that is the conductor's stage-2 read.
I did **not** wire `--ratchet`, per N2's explicit warning that it rewrites the designer's
`_type_ratchet.json`.

**Also from that row: three store rows my rename orphaned.** `W-99zt`, `W-99zv` and `W-99zy`
pointed at `knowledge/_release/_v3_manifest.json`, `designer-skills-v3/skills/` and
`designer-skills-v3/ci-template/`, and `_state.check()` went RED (`3 UNRESOLVABLE`, blocking).
Repointed through `_state` — path strings in `home`/`links` only, no title, state, owner or
close condition touched — six rows moved (`W-99zt/zu/zv/zw/zy/zz`). `_state.py --check` now reads
**0 UNRESOLVABLE**; `_state.py --selftest` 57 bites green; `_gate_doc_rows.py` unrowed 0.

---

## ⑦ THE ONE CROSS-LANE COLLISION, DECLARED

`knowledge/canon/canon.css` is modified in the working tree **partly by my hand, and it is N2's
region.** Driving `python3 knowledge/canon/gen_canon_tokens.py --check` to prove repo behaviour
was unchanged, I discovered that **`gen_canon_tokens.py` has no `--check` arm at all** — it
ignores argv (its only argv test is `--selftest`) and regenerated `canon.css` from source. The
source it read was N2's in-flight edit (the `.search` → `.nav-search` namespacing for the
type-blast-radius red), so the regenerated file carries N2's change, materialised by my run.

**Not reverted** — reverting would throw away a regeneration N2 needs anyway, and the file is
generated, so its correct content is whatever the current source produces. The conductor should
attribute that line to N2 and expect N2's own regen to be a no-op over it. **Nothing else of
N2's was touched**, and the synthetic commit above deliberately excludes their files so none of
my numbers are contaminated by them.

---

## ⑧ ⛔ REPLAY-THESE (conductor) — READ BEFORE COMMITTING

- **`_gate_release_audit.py --check` is RED and `--selftest` is 8/1, BY DESIGN, and both are
  BLOCKING** (`_build_all` `[135]`/`[136]` and the CI `release` job). The manifest on disk is
  R1's generation at `801fe7c`, where the pack still lived under the old prefix; the generator
  now claims `apollo-snoopy/`. The gate names it exactly: *"8 path(s) the file ships that a fresh
  generation does not"* — the 5 skills + 3 ci-template files at the old prefix, and nothing else.
  **This is the same designed stage-1 red seam 7 landed with, for the same reason, and it clears
  the same way.** Do not push before it is cleared.

- **STAGE 2, after the landing commit `<sha>` exists:**

  ```
  python3 knowledge/_release/_gen_pack_manifest.py --probe    --commit <sha>   # ~45s
  python3 knowledge/_release/_gen_pack_manifest.py --manifest --commit <sha>
  python3 knowledge/_release/_gen_pack_manifest.py --page reviews/RELEASE-SNOOPY-2026-08-26-v1.html
  python3 knowledge/_make_review.py …    # the bake/page rewrite strips the review pair's stamps
  python3 knowledge/_release/_gate_release_audit.py --check      # must go GREEN
  python3 knowledge/_release/_gate_release_audit.py --selftest   # must go 8/0
  ```

  **Expected: 1,594 paths** (unchanged by a rename), fonts 54, skills 5, ci-template 3, all under
  `apollo-snoopy/`. If N2's four-reds fixes are in the same commit the PROBE verdicts will move
  (fewer reds) — that is correct and expected, and **the fifth card's four gate names should then
  be re-read**: `Q5_RED_GATES` is bitten for existence, not for still-being-red.

- **The two generated artefacts are STALE ON DISK and were deliberately NOT regenerated.**
  `knowledge/_release/_pack_manifest.json` and both `reviews/RELEASE-SNOOPY-*.html` are pure
  renames (`R`, no `M`) of R1's `801fe7c` generation. They still say the old name INSIDE. The
  alternative — leaving the synthetic commit's artefacts on disk — was rejected as worse than
  stale: the audit would have gone green locally against a dangling object and REFUSED (77) in
  CI, i.e. a gate passing on a commit that will never exist.

- **The ledger's third row is renamed and re-seeded**, and `renamed_from` is what lets the
  laundering arm see across the change. **Do not drop that field**, and do not re-seed the whole
  ledger at HEAD — that would move `baseline_commit` on v1 and v2 and light the laundering arm
  for both.

- **`knowledge/canon/canon.css` in the tree is N2's content, materialised by my run** (§ ⑦).

- **Store ids:** `W-191` and `W-192` (N2 took 188–190 concurrently). The `W-99z*` range is still
  exhausted and still sorts after every numeric row.

- **N2's `W-189` handoff is DONE except for its verdict** (§ ⑥b): the runner now replays a
  per-gate argv from the manifest, and the invocation is declared in the generator's source, not
  hand-edited into the probe artefact. Its 35-pass figure needs N2's `--check` arm in the commit
  — read it at stage 2.

---

## ⑨ THE TREE — this lane's lines, for the conductor's reconcile

```
 M .github/workflows/gates.yml            (3 step names, 2 paths, a FIFTH correction-log entry)
 M .gitignore                             (the dist exception + the zip glob)
 M _CHAIN.md                              (REGENERATED — stale because this lane minted 2 rows;
                                           GOOD-MORNING.md and _LIVE-STATE.md untouched, verified)
RM designer-skills-v3/build-designer-pack.sh -> apollo-snoopy/build-designer-pack.sh
R  designer-skills-v3/ci-template/{README.md,gates.yml}  -> apollo-snoopy/ci-template/…
RM designer-skills-v3/ci-template/run-gates.py           -> apollo-snoopy/ci-template/… (W-189)
R  designer-skills-v3/skills/*/SKILL.md (5)              -> apollo-snoopy/skills/…
 M knowledge/_build_all.py                (4 paths + 3 labels, in STEPS **and** ROUTE_ROWS)
 M knowledge/_helpgate.py                 (+96 — the third leg, pack_gate)
 M knowledge/_release/_frozen-releases.json          (the third row, RE-SEEDED not typed)
 M knowledge/_release/_gate_ci_template.py           (TEMPLATE_DIR/REL + the manifest path)
 M knowledge/_release/_gate_frozen_release.py        (+113 — rename bridge, vanished-row arm, 3 bites)
 M knowledge/_release/_gate_release_audit.py         (DIST, the zip glob, the import, the remedies)
RM knowledge/_release/_gen_v3_manifest.py -> knowledge/_release/_gen_pack_manifest.py  (+~470)
R  knowledge/_release/_v3_gate_probe.json -> knowledge/_release/_pack_gate_probe.json  (⚠ STALE)
R  knowledge/_release/_v3_manifest.json   -> knowledge/_release/_pack_manifest.json    (⚠ STALE)
 M knowledge/_state.json                  (2 rows minted, 6 repointed — all through _state)
 M knowledge/canon/gen_canon_{bento,components,tokens}.py, gen_theme_cascade.py  (+4 lines each)
R  reviews/RELEASE-V3-MANIFEST-2026-08-26-v1{,.REVIEW}.html
                                          -> reviews/RELEASE-SNOOPY-2026-08-26-v1{,.REVIEW}.html
                                          (⚠ STALE INSIDE — content is R1's 801fe7c generation)
?? notes/_subreports/2026-08-26-219-N1-snoopy-rename.md   (this report)
```

**NOT mine, in the same tree** (N2's lane, do not attribute to N1): `knowledge/_validate_evidence.py`
· `_validate_token_forks.py` · `_validate_type_composites.py` · `knowledge/snippets/Navigations.reference.html`
· `knowledge/_COMPOSE-AUDIT.md` · `knowledge/_TYPE-BLAST-GATE.md` · their report and its asset ·
`knowledge/_rulings.json` (the conductor's). And `knowledge/canon/canon.css` — N2's content, my
run (§ ⑦).

---

## FINDINGS

1. **A release name inside a machinery filename is a recurring bill, not a one-off.** Three files
   had to be renamed and nine had to be chased because the previous cut spelled "v3" in paths. The
   generic names stop the next lunar module costing the same. The general shape: a pointer should
   not carry a copy of the value it points at.
2. **The laundering arm was blind to a rename, and only doing the rename found it** (§ ③). A gate
   that matches by id has an unstated assumption — that ids are stable — and the first rename is
   where it is discovered. Fixed at cause with a declared-rename bridge plus a vanished-row arm.
3. **`gen_canon_tokens.py` accepts `--check` and silently does a full write** (§ ⑦). It is not
   wired into `_build_all` or CI, so nothing is currently red because of it — but
   `_build_survey.py` treats `--check` as NON-MUTATING and would RUN it if it were ever wired.
   That is a mutating step wearing a read-only flag, one wiring away from writing in a survey.
   **Priced: a `--check` arm on that generator, ~15 lines, the same shape its three siblings
   already have.** Not taken — it is a canon generator mid-wave and not this lane's file.
4. **A self-referential grep bite fails on its own text.** `naming/no-stale` went red four times
   on the literals in its own source. The fix is to assemble the forbidden token from fragments,
   never to weaken the assertion — worth remembering because "make the grep narrower" is the
   obvious and wrong move.
5. **The probe at the synthetic commit was byte-identical to the probe on disk except for the
   commit line.** That is a stronger statement than "the rename should not affect gates": no
   verdict, no `why` string, no selftest classification moved. It also means the conductor's
   stage-2 probe cost is real but its RESULT is predictable — any movement there is N2's fixes,
   not mine.
6. **The build script's dirty-tree refusal arm accepts ANY refusal.** With the manifest at a
   different commit from HEAD, `--release --commit HEAD` dies at the manifest-mismatch check
   BEFORE `require_clean` is reached — and the selftest prints "green — refused, as it must".
   The arm is true but not specific: it proves *a* refusal, not *that* refusal. Priced: match the
   refusal text, ~2 lines. Not taken this lane (it would have been a change to an arm I was
   simultaneously relying on).

---

## RULING-SHAPED QUESTIONS (not decided here)

1. **Do the answered cards belong on Dave's page at all, or should the page become a pure ship
   list once he has ruled?** I kept all five, with his answers, because an answer with the
   question deleted is not legible. But this is his decision surface and the shape of it is his.
2. **Q1, Q4 and Q5 are transcribed with no enactment claim.** Whoever owns those clauses should
   fill in the `enacted` line — and the scope bite (`questions/Q2-and-Q3-are-this-lanes-clauses`)
   must be updated deliberately when they do. Is that the conductor's, or the lane's?
3. **The generic-filename decision (§ ① #3) is mine and can be struck.** If the house prefers the
   release name in the machinery's paths, it is a `git mv` plus nine reference sites — the same
   bill, paid again at Eagle.
4. **`build-designer-pack.sh` kept its name** (§ ① #4). If the wave is meant to reach the script
   too, say so and it moves with its six references.

---

## UNPROVEN, declared

1. **No commit and no CI run exists.** Every verdict above was driven in this working tree. R2's
   standing UNPROVEN — neither workflow has ever run on GitHub Actions — is **unchanged**; I did
   not discharge it and cannot.
2. **The bake was proved at a SYNTHETIC commit, not at the landing commit.** The tree at that
   commit is HEAD + this lane's files, which is what the landing commit will contain only if the
   conductor commits exactly this lane and no other. If N2 lands in the same commit, the ship
   list is the same 1,594 paths (their files are all in `knowledge/` and already claimed) but the
   PROBE verdicts will differ — see § ⑧.
3. **The pack-side runner was not re-driven from inside this pack.** Seam 7 drove
   `ci-template/run-gates.py --list` from the flat pack and it found the root by walking up for
   `_MANIFEST.json`; the rename does not touch that mechanism and the layout is unchanged, but I
   asserted it from the shape rather than re-measuring it. Priced: one command inside
   `/var/tmp/n1/bake1/Apollo-Snoopy-v1.0.0/`.
4. **N2's 35-pass runner figure is not reproduced here** (§ ⑥b). The mechanism is driven; the
   verdict needs their `--check` arm, which is not in my synthetic commit.
5. **The warning's WORDING has not been past Dave.** It carries his framing verbatim inside a
   longer paragraph I wrote. If he wants the shorter version, it is one string in
   `knowledge/_helpgate.py` and a bite asserts only the framing sentence survives.

---

## Not touched

`designer-skills-v1/` · `designer-skills-v2/` (read only) · `memento-package/` (the Gumdrop
identity lives in the PACK's generated files, exactly as briefed) · `knowledge/_validate_*` ·
`knowledge/snippets/` · `knowledge/tokens/` (all N2's) · `GOOD-MORNING.md` · `_LIVE-STATE.md` ·
`knowledge/_rulings.json` · Dave-owned rows · any constant, band, advisory or threshold · the two
generated release artefacts' CONTENT. No commit, no push. Everything under `/var/tmp/n1/` is a
throwaway.

## Store rows

Two, minted through `_state.add()` (never by hand-editing `_state.json`): **`W-191`** for the
rename and the release machinery, **`W-192`** for this filed report (`s218-D7`, forgotten-document
class #185). ⚠ `W-188`/`W-189`/`W-190` were taken by N2 while this lane was open — ids were
re-derived from the store rather than reserved in advance. Six existing rows were also REPOINTED
(path strings only) because this rename orphaned their homes — § ⑥b.

---

## ⤷ CORRECTION APPENDED 2026-08-26 (#219 seam 8) — THE NAME FLIPPED TO **SPIDER** BEFORE ANY COMMIT

`s219-D8` supersedes `s219-D7` on the pack name, and it landed while this lane's work was still
uncommitted. **The pack is `Apollo — Spider v1.0.0`** (dir `apollo-spider/`, zip
`Apollo-Spider-v1.0.0.zip`, page `reviews/RELEASE-SPIDER-*.html`), still carrying
`Memento — Gumdrop v1.0.0`; the release grammar is now the STRICT MISSION PAIR — one mission's
LM and CM together, and Spider + Gumdrop are both Apollo 9. Because **no commit ever carried the
Snoopy name**, the tree records ONE rename, `designer-skills-v3` → `apollo-spider`, and the
ledger's `renamed_from` bridge names `designer-skills-v3` — the transient id was kept out of it.
Nothing in the body above is rewritten: it is this lane's filed record of the work as it was done,
and § ① decision #3 (generic machinery filenames) is exactly what made the second flip cheap.
Enacted and re-driven at `notes/_subreports/2026-08-26-219-seam8-reconcile.md`.
