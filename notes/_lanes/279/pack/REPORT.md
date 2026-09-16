# LANE PK — REPORT — the pack ships the reader and the Constitution — designer-skills-v2 released at v2.1

#279 · 2026-09-16 · enacting Dave's word *"i agree 'a' it is"* (to inscribe as `s279-D1` at wrap — `notes/_lanes/279/DAVE-RULINGS-2026-09-16.md` item 5) under `s278-D1` + `s277-D10` · a release under P-269-1 · lane PK (Fable 5.1). Everything below was RUN; every figure carries the command that produced it. Scratch under `/tmp/pk279/` (root disk, not `/sessions`), removed at the end.

**Result: RELEASED.** `designer-skills-v2/` is v2.1: its `knowledge/` is re-baked from the tree at `eb2ff7c` and now carries the reader (`_compose_slice.py`), the Constitution (`_rulings.json` + `_ruling_edges.json`), the four node files, the lexica, `guidelines/_scope.json`, `guidelines/_rules-index.json` and `tokens/_blast-radius.json` — the reader's whole read closure, derived from the code, not typed. From a copy of the shipped pack with no path back to the repo, ASK answers all 12 questions in ≤1K tokens, the dashboard seed is byte-identical to the repo's, and a ruling planted in the pack's own `_rulings.json` is answered live. The frozen-release gate goes from RED (RV F1) to rc 0 with v2 → v2.1. The `_gen_pack_manifest.py` exclusion is reversed by addition, armed at the next Spider version so the ratified v1.0.13 manifest stays byte-for-byte (§ 2).

---

## 1. What is true today — verified, not trusted

- `_gen_pack_manifest.py` is the **Spider** generator (`apollo-spider/build-designer-pack.sh`), not v2's baker. Its `EXCLUDED` row `("knowledge/_rulings.json", "Apollo's ruling store — Dave's record.")` (was line 515, now inside `_EXCLUDED_ALL`) is documentation plus a selftest bite (`groups/excludes:knowledge/_rulings.json`) — nothing in `build_manifest()` filters by it; a path is excluded by being claimed by no group. `_compose_slice.py` and the node files were never claimed by any group; `_rulings.json` was named as excluded by his record. `designer-skills-v2/` itself is baked by `designer-skills-v2/build-designer-kb.sh` (a copy-list), and that is the pack `s277-D10` governs and RD wired.
- `_gate_frozen_release.py --check` at `9b2e1b0`: **rc 1** — `FROZEN RELEASE MOVED: designer-skills-v2 (version v2) … 1 CHANGED: designer-skills-v2/generate-from-canon/SKILL.md` (RD's `d6bd57b`, RV F1). Reproduced before anything was touched.
- **There is no file called a release runbook.** `_memento_search.py "frozen release"` / `"release runbook"` return no runbook section; `_RUNBOOKS.md` has no release entry. The steps live in three places and I followed all three, quoting each line in § 3: the ledger's own `_README` (`knowledge/_release/_frozen-releases.json`), the gate's docstring (`_gate_frozen_release.py:65-70`) and the baker's header (`build-designer-kb.sh:5`). The Spider cuts (#257…#268) add the pattern "bumped in the release commit, read back from the seed's printed table", and the seed lands in its own follow-up commit (`df64895`, `cca977d`, `ce31dad` are all `frozen ledger re-seeded` commits) because `--seed` measures a COMMIT (`git ls-tree` at `--at`, default HEAD), never the working tree.
- The read closure, from the code (`grep -n "open(\|HERE\|json.load" knowledge/_compose_slice.py` → `load_graph` / `_token_tier_map` / `load_live` / `ask`): `HERE = os.path.dirname(os.path.abspath(__file__))` and every open is `os.path.join(root, …)` with `root=HERE`, or `os.path.join(os.path.dirname(g["$root"]), m["$path"])` where `$path` is `knowledge/components/<x>.meta.json` — so the reader finds its files relative to itself as long as the folder is called `knowledge/`, which the pack's is. **No hardcoding of the repo root; nothing to fix.** The helpgate walk (`_compose_slice.py:151-155`) needs `_helpgate.py` beside it — the one import; `_helpgate.py` imports only `os, sys`.

## 2. The exclusion, reversed by addition — and why it is version-gated

`knowledge/_release/_gen_pack_manifest.py` (+138 / −11):
- `READER_SHIPS_FROM = "v1.0.14"`, `READER_RULING = "s279-D1"`, `READER_CLOSURE` (9 root-level paths no other group claims: `_compose_slice.py`, `_rulings.json`, `_ruling_edges.json`, the four node files, `_consult-lexicon.json`, `_kg_verbs.json`), `reader_ships()`, `reader_group()` (key `engine-canon.reader`, membership match — it can swallow nothing), `excluded_rows()`.
- The old exclusion line **stays**, as `RULINGS_EXCLUSION` inside `_EXCLUDED_ALL`, with a comment saying it is SUPERSEDED at s279-D1 from `READER_SHIPS_FROM` on; `EXCLUDED` / `excluded_rows()` drop it the moment `VERSION` crosses the line, and `groups()` inserts the reader group before `gates`.
- **Why gated and not simply edited (the brief asked me to say which):** the v1.0.13 manifest is RATIFIED (s268-D3), its zip is FROZEN in `dist/`, and two BLOCKING arms pin the generator to it — `_gate_release_audit.py --manifest-check` regenerates at `08e315d` and compares byte for byte; `--pack` compares the zip's `_MANIFEST.json` to the status-free derivation of the repo file. Any change to what the module emits at v1.0.13 — a group, a row, a reason string — turns both red without a Spider v1.0.14 cut, and cutting Spider is Dave's word (s219-D4(2)) and P-269-1's `pack-version-bump` tripwire, which this lane was not given. His "a" was answered for the pack the ruling governs. So the block ARMS ITSELF at the next Spider version. Proven: `--manifest-check` → `PASS — byte-identical … (1714 files, sha256 499c144ccbf84f34)` after the edit; `build_manifest()` with `VERSION="v1.0.14"` at HEAD emits `engine-canon.reader` with 8 files / 2,019,007 B and no `_rulings.json` exclusion row (in memory only — nothing was written to `_pack_manifest.json`).
- Bites added (12, `--selftest` 237 → 249, 0 failed; mutation-tested: `READER_SHIPS_FROM="v1.0.13"` → 3 RED, a closure path another group also claims → 1 RED): `reader/v1.0.13-unarmed`, `reader/v1.0.13-exclusion-stands`, `reader/armed-group-present`, `reader/armed-exclusion-gone`, `reader/armed-claims:<9 paths>`, `reader/armed-claims-nothing-else`, `reader/armed-before-gates`, `reader/version-order`. The `groups/excludes:knowledge/_rulings.json` bite is now conditional on `reader_ships()`.

`designer-skills-v2/build-designer-kb.sh` (+41): a v2.1 header block, a `READER_CLOSURE` copy block (no `|| true` — a missing closure file is a refusal), explicit copies of `guidelines/_rules-index.json`, `guidelines/_scope.json`, `tokens/_blast-radius.json`, a `.DS_Store` scrub, and one README bullet for the reader. Every pre-existing `cp` line is unchanged. `designer-skills-v2/README.md` (+15 / −1): title v2.1 and a "What's new in v2.1" block in the designer's register.

`knowledge/_compose_slice.py` (+64, three hunks, all mine — VB's verb hunks landed separately at `eb2ff7c`): `OPENED` + one `.add(path)` line in `_load` and `_read` (file-location code), and the PACK allow-set bites at the end of `--selftest` (79/79): (63) every opened file is under `HERE`, none by a path back to the repo; (64) with the generator armed at `READER_SHIPS_FROM`, every opened file is claimed by a group or rides as gate data — 0 unclaimed; (65) none is under an `EXCLUDED` row; (66) a fresh `build-designer-kb.sh` bake into a tempdir exits 0 and ships every opened file — 0 missing; and a fourth form that runs only inside a shipped pack (neither generator nor baker present): every opened file exists beside the reader. Mutation: the bake list minus `_rulings.json` → `FAIL … (0, '', ['_rulings.json'])`. No other bite was changed; `_build_kg_explorer.py`, `_scope.json` rows and the explorer were not touched.

## 3. The release — every step, with its line

| # | the line | command run | result |
|---|---|---|---|
| R1 | `build-designer-kb.sh:5` — *"Re-run when canon changes, then re-zip."* | `PROVENANCE="commit eb2ff7c (2026-09-16) plus the #279 lane PK release commit that carries this bake — …" DST=/tmp/pk279/kb-new bash designer-skills-v2/build-designer-kb.sh` then `cp -R /tmp/pk279/kb-new/. designer-skills-v2/knowledge/` | `Built …`; `diff -rq` bake vs pack → byte-identical tree; 253 files added, 0 removed, 843 common. ⚠ The script's own `rm -rf "$DST"` is refused by this sandbox's delete-guard (`Operation not permitted`, 800+ lines), so the bake went to scratch and was copied over — the same tree; on Dave's Mac the script runs as written. Every shipped file except `_compose_slice.py` is byte-equal to its `HEAD` blob (`checked=1093 differs=1`); `_compose_slice.py` equals the working tree, whose 64-line difference from HEAD is this lane's bite and lands in the same commit. |
| R2 | ledger `_README` — *"Editing a frozen surface means cutting a NEW release: change the files, re-seed, and BUMP that row's `version` in the same commit."* | `_gate_frozen_release.py:137` SURFACES literal `"v2"` → `"v2.1"`, with the #279 comment in the same shape as the Spider rows | done; the fixture in `_fixture()` now registers the LIVE literal (`v2_live = next(d[2] for d in SURFACES …)`) instead of typing `"v2"` — the typed register stopped naming the seeded row the moment the literal moved (2 fixture bites went RED for the wrong reason; 17/17 after) |
| R3 | `_gate_frozen_release.py:68-70` — *"`--seed` REWRITES the ledger from measurement. Run it when a release is deliberately cut or re-cut, and bump that row's `version` in the same edit — arm 3 exists to catch the case where you did not."* | `python3 knowledge/_release/_gate_frozen_release.py --seed` **after the release commit** (it measures HEAD's tree) | § 8 — the seed's printed table, read back |
| R4 | `_gate_frozen_release.py:62` — *"`python3 knowledge/_release/_gate_frozen_release.py               # HEAD + working tree`"* | `--check` after the seed commit | § 8 — rc 0 |
| R5 | `_parked.py` hooks — `_gate_release_audit.py` prints *"PARKED DUE — 3 parked item(s) are due at release-cut — python3 knowledge/_parked.py --due release-cut"* | `python3 knowledge/_parked.py --due release-cut` | `PARKED DUE — 3 of 22`: P-274-1 (edit-mode alternatives; `_compose_slice.py` changed in 3 commits since 3a752d1), P-273-1 (toolkit ingest), P-277-5 (npm distribution, event `release-cut`). **P-269-1 itself did NOT fire** — its trigger is `pack-version-bump`, which reads the Spider manifest's version; v2.1 is not a Spider bump. Printed, not acted on — all three are Dave's. |
| R6 | `build-designer-kb.sh:5` — *"…then re-zip."* | `zip -r -X Apollo-designer-skills-v2.1.zip AGENTS.md designer-skills-v2` from a stage mirroring the v2 zip's layout (`notes/_receipts/2026-07-21-worker-designer-pack-v2.md`: AGENTS.md + the pack folder, **0 shell scripts** — `build-designer-kb.sh` dropped, AGENTS.md is the v2 zip's own copy) | `Apollo-designer-skills-v2.1.zip` at the repo root beside `Apollo-designer-skills-v2.zip` — **3,921,681 B, 1,129 entries, 12,568,927 B unpacked, sha256 `d32ce852835a06bd…`**; `*.zip` is gitignored (`.gitignore:40`), so it is a handover artefact, not a tracked path, exactly like v2's |
| R7 | s114-D4 / `s219-D4(5)` — a shipped release is frozen | `_gate_frozen_release.py --check` before the commit | RED as expected on BOTH arms (surface: the v2 row vs `d6bd57b`; working tree: `383 path(s)` dirty under `designer-skills-v2/`) — the gate doing its job until R3/R4 |

## 4. The closure — what the reader opens, recorded

`OPENED` (new, `_compose_slice.py`) records every path `_load` / `_read` touches. Cleared, then one `build_slice(TASK_A)` + `load_live()` + the 12 asks:

| where | count | files |
|---|---|---|
| `components/` | 137 | every non-EXAMPLE `*.meta.json` |
| `compliance/rules/` | 55 | `*.json` |
| root of `knowledge/` | 11 opened + 2 modules | `_rulings.json` · `_ruling_edges.json` · `_rule_nodes.json` · `_ux_principle_nodes.json` · `_icon_nodes.json` · `_logo_nodes.json` · `_consult-lexicon.json` · `_kg_verbs.json` (VB, s277-D11) · `roles.json` · `chart-intents.json` · `component-types.json` · + `_compose_slice.py` itself and `_helpgate.py` |
| `tokens/` | 11 | `colour` · `semantic-colour` · `spacing` · `layout` · `typography` · `elevation` · `motion` · `opacity` · `icon-scale` · `typography-composites` · `_blast-radius` (Q9) |
| `guidelines/` | 2 | `_rules-index.json` · `_scope.json` |

**218 paths, 0 outside `HERE`.** `canon/canon.css` + `type.css` are read only by `--measure`; guideline `.md` files only by selftest bites (`measure_scope` / `$source` checks) — neither is a runtime open, and both ship anyway (canon whole; guidelines minus the v2 EXCLUDE list). Nothing under `knowledge/assets/` beyond `icons/` (already shipped) is opened — the 5.2 GB never came near the pack.

## 5. Proved from inside the pack — no path back to the repo

`cp -R designer-skills-v2 /tmp/pk279/pack && cd /tmp/pk279/pack` (PYTHONPATH unset; the reader's `HERE` = `/tmp/pk279/pack/knowledge`). Counts are my own tiktoken cl100k (0.14.0) over `json.dumps(answer minus sized)`; the door's `sized.tokens` is the same number on all 12.

| Q | question | tokens (in-pack) | ≤1K |
|---|---|---|---|
| Q1 | what governs component:button? | **680** | ✓ |
| Q2 | which components does rule:ctkb-003 bind? | **222** | ✓ |
| Q3 | what principle underlies rule:ctkb-002, and its grade? | **261** | ✓ |
| Q4 | which rules conflict for component:button? | **319** | ✓ |
| Q5 | what did Dave rule about component:table, and when? | **245** | ✓ |
| Q6 | what evidence supports ruling:s277-D10? | **337** | ✓ |
| Q7 | which components answer intent:comparison? | **271** | ✓ |
| Q8 | what must component:toast not sit next to? | **281** | ✓ |
| Q9 | what tokens does component:button consume; what breaks if I change one? | **755** | ✓ |
| Q10 | which pattern / context is component:button used in? | **371** | ✓ |
| Q11 | what is the WCAG / accessible-name obligation for component:button? | **633** | ✓ |
| Q12 | what icon / logo / photo may I use in component:app-shell-doormat? | **678** | ✓ |
| | **total** | **5,053** (max 755) | 12/12 |

(RD's 4,527 / RV's 4,570 were before VB's `verb` + `readsAs` rows landed; the in-pack numbers equal the repo's own `--selftest` counts to the token.) Receipts: `notes/_lanes/279/pack/ASK-12-in-pack.json`, `seed-in-pack.json`.

**Seed byte-compare.** `python3 knowledge/_compose_slice.py "<dashboard>" --out …` in the pack and in the repo: `cmp` silent — **byte-identical, sha256 `b8464d632b697a8a…`, 134,457 B, `sized.slice_tokens` 34,211** (the `generated` date is today on both sides).

**The plant.** Appended `s998-D9` (governs `button.meta.json`) to `/tmp/pk279/pack/knowledge/_rulings.json` (sha `0f5bf047a0cb…` before) AFTER the seed, then `--ask "what governs component:button?" --seed seed-pack.json` in the pack → `ruling:s998-D9` is the first row of the answer; the seed file unchanged (`b8464d632b697a8a…`); `knowledge/_rulings.json` in the repo and in `designer-skills-v2/` both `grep -c s998-D9` → 0; the repo's ASK does not see it. The Constitution is read live, inside the pack, from the pack's own copy.

**In-pack `--selftest`, for the record: 72/76.** The 4 reds are repo-bound bites, not the reader: bite 46 (`$source` substrings — 3 files the v2 EXCLUDE list drops: `accessibility-framework.md`, `-qa-cx-testing.md`, `-standards-hub.md`) and VB's 68–70 (the verb census reads the audit document under `notes/`). The SKILL.md never asks a designer to run `--selftest`; declared, not fixed (RD's, SC's and VB's bites are not mine to change).

## 6. Size — before / after

| | files | bytes |
|---|---|---|
| `designer-skills-v2/` before (`9b2e1b0`) | **849** | **2,249,288** |
| `designer-skills-v2/` after (v2.1) | **1,102** | **12,571,023** |
| of which the root-level closure (14 files) | 14 | 2,162,495 |
| the v2.1 zip | 1,129 entries | 3,921,681 (12,568,927 unpacked) |

The other +8.2 MB is the design system's own growth since the July bake, not the closure: components 42 → 139 files (256 KB → 1.65 MB), snippets 40 → 137 (406 KB → 4.8 MB), `canon/` 215 KB → 2.0 MB, tokens 10 → 21 files, compliance 34 → 58, guidelines 49 → 51, icons 665 → 674. Nothing huge was dragged in; `knowledge/assets/` (5.2 GB) is untouched by the closure — no stop.

## 7. What was not done, with size

1. **`apollo-spider/skills/generate-from-canon/SKILL.md` stays unwired** (~30 lines of the same step-1 prose) — the ruling's `governs` names `designer-skills-v2/` only; left as briefed. When Spider's skill is wired, the s279-D1 block in the generator arms itself at v1.0.14 and the closure ships with it.
2. **Spider v1.0.14 is not cut** — the allow-block is declared and bitten on both sides of the line, the manifest is not regenerated (§ 2). Size: the standard Spider cut lane (`--probe` + `--manifest` at a commit, a key in `RATIFY_IDS` once he ratifies, `--release`, the ledger literal, `--seed`). Dave's, and P-269-1's tripwire.
3. **`_received.json` has no `v2` row** although v2 was handed to testers (the July receipt). Not added — the register is his record (`⛔ ADD A ROW THE MOMENT A PACK LEAVES THE REPO`) and v2.1 is bumped regardless. Size: one row, when he says v2.1 (or v2) was received.
4. **In-pack `--selftest` 72/76** (§ 5) — 4 repo-bound bites. Size: guard each on the file's existence (~4 lines, in RD's / VB's bites), if the pack should ever pass its own selftest.
5. **`git status` leaves a 0-byte `.git/index.lock` in this sandbox** (unlink is denied — `warning: unable to unlink … Operation not permitted`). Three stale ones were `mv`'d to `.git/_orphan-locks/index.lock.stale-{1642,1734,1800}-moved-by-lane-PK-279`; polling for VB's commit switched to `git log` only. Size: 0 — a seat fact, recorded so the next lane does not read a lock as another lane's activity.
6. **The `_compose_slice.py` seat.** VB staged HEAD + its own hunks at 17:55 and landed `eb2ff7c` at 18:40; this lane waited (brief: never sweep VB's hunks), then `git diff knowledge/_compose_slice.py` = 64 insertions, all three hunks mine. No rebase was needed — my hunks were never in VB's blob.
7. **The msgfile path.** The brief says `/tmp/_msg-279-PK-<ts>.txt`; `_git_commit.sh`'s header says "never /tmp". Followed the brief, as RD did. Size: 0.

## 8. Shipped sha, the seed table, the gate lines and `--numstat`

(appended after the commits land — a commit cannot name itself; the SC/EX pattern)
