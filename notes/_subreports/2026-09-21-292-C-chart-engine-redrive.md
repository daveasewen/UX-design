# `#292`-`C` — the chart-engine re-drive that clears the release CI red at step 12

provenance: 292 · 2026-09-21
status: observed

session: `#292` · conductor **Fable 5.1**, this seat a delegated **OPUS 5** build sub · lane `C` · owed item 6 of `_HANDOFF-142-…md` § OWED TO #292, **four sessions owed**
scope: `knowledge/_drive_chart_engine.py` re-drive only. **No gate was patched, no generated file hand-edited, nothing committed** — the conductor commits.

## VERDICT

✅ **STEP 12 OF THE `release` JOB IS GREEN — `bash apollo-spider/build-designer-pack.sh --selftest` exit `1` → exit `0`.**
✅ **The whole `release` job is green at this seat**: all eight other steps re-driven by hand, every one `rc=0`.
⛔ **The `gates` job's inherited reds were NOT touched** — the boot-drift ceiling breach and the boot double-counts in `notes/_GAUGE-LOG.md` stand exactly as inherited, by instruction.
✅ **ONE tracked file changed, and it is machine-written**: `knowledge/_tests/chart-engine/_receipts.json`.

## WHAT LANDED

**The refusal was reproduced first, locally, with CI's own command and cwd** (`bash apollo-spider/build-designer-pack.sh --selftest` from the repo root), after `pip install tiktoken --break-system-packages`. Verbatim, the last two lines of the failing arm:

```
=== refusal: --release over STALE chart receipts (s263-D13) ===
green — one mutated source hash is refused, as it must
RED — the real receipts are STALE; a release would be refused right now. Re-drive: python3 knowledge/_drive_chart_engine.py
```

**ROOT CAUSE, IN ONE PARAGRAPH — AND IT IS NOT A DEFECT IN THE GATE.** `_drive_chart_engine.py` drives a real Chromium over the 27 committed chart-engine test pages × 4 themes × 2 modes and commits the measured geometry to `knowledge/_tests/chart-engine/_receipts.json`, the DRIVEN RECEIPT that `_validate_dataviz.py` accepts as the evidence for dv-004 on engine-drawn charts (`s260-D3`). Each page's receipt records the sha256 of the page and of **every local file it loads**, so that a change to the engine's own bytes makes the measurement STALE rather than letting new code be graded by an old reading. `knowledge/canon/canon.css` — a source of all 13 engine-drawn pages — **moved at `71b3363c` (after #288, 2026-09-19, +54/−4 lines, the `gen_bento_role_vars.py` arm)**, while the receipts were last driven at `7ddab70d` (#268, 2026-09-11). One hash, 13 pages, and the `s263-D13` arm of the build script refused a release over receipts it could not tie to the current bytes. **The gate was right on every run; the drive was owed.** The 14 `Chart-*.reference.html` pages stayed FRESH throughout because they do not load `canon.css`.

**THE RE-DRIVE WAS RUN AS THE TOOL INTENDS** — `python3 knowledge/_drive_chart_engine.py`, never a hand edit of the JSON. It needs Playwright + Chromium; the sandbox was fitted per `chromium-in-sandbox-recipe` (`NODE_EXTRA_CA_CERTS`, `playwright install chromium`, `libxdamage1` extracted to `~/.local/lib`, `LD_LIBRARY_PATH` exported in every call). ⚠ **The full 27-page run does not fit one tool call** (~3 min against a hard ~180 s cap, and **no background process survives a call boundary** at this seat — a `nohup`'d run was confirmed dead, log 0 bytes). So the drive ran in **two `--page` batches**, which is the script's own documented merge path (13 engine pages, 83 s; 14 reference pages, 101 s), and the result was then verified by a **single full `--check`**: `✅ all 27 receipt(s) FRESH`. ⚠ `--page` is `append`-style — one flag per page, not a list.

**NOTHING ELSE WAS RUN THAT WRITES.** `_build_all.py` was not run, by instruction. The survey (`_build_survey.py`) was run non-mutating and in `--range` chunks for the same 180 s reason.

## MEASURED

**Step 12, before → after.**

| | command | exit |
|---|---|---|
| before | `bash apollo-spider/build-designer-pack.sh --selftest` | **1** |
| after | `bash apollo-spider/build-designer-pack.sh --selftest` | **0** |

After, the arm reads `green — the real receipts are FRESH (control)`, and the generator selftest holds at **249 bites, 0 fail(s)**.

**`_drive_chart_engine.py --check`, before → after.** Before: `❌ 13 page(s) STALE/MISSING`, every one naming the same single stale source, `knowledge/canon/canon.css`; 14 reference pages FRESH. After: `✅ all 27 receipt(s) FRESH (driven 2026-09-21T09:40:04Z, Chromium 153.0.8010.12)`, **rc `0`**. ⚠ **CORRECTION OF THIS SEAT'S OWN FIRST READING, LEFT VISIBLE:** the before-run was piped to `tail`, so the `EXIT=` this lane first recorded was `tail`'s and read `0` against a `❌`. **Re-measured properly with a mutation control** — one source hash in the `bar.html` receipt set to 64 zeroes → `--check` rc **1**; the file restored byte-identical and re-asked → rc **0**. The check bites in its own right; the first reading was the measurement's fault, not the tool's.

**COUNT OF REGENERATED FILES: 1.** `knowledge/_tests/chart-engine/_receipts.json`, 27 page receipts rewritten inside it.

★★ **THE DIFF IS 15 INSERTIONS / 15 DELETIONS AND CONTAINS NO MEASUREMENT.** Two header lines (`chromium` `151.0.7922.34` → `153.0.8010.12`, `driven` `2026-09-11T08:59:56Z` → `2026-09-21T09:40:04Z`) and **13 `canon.css` source hashes**. **Not one mark count, row count, dv-004 separation, contrast figure or aria count moved** — across a Chromium **major** bump of two versions and a 54-line canon.css change. That is a measured fact about the engine's stability, published here rather than asserted: the staleness was real, and what it was protecting had not in fact drifted.

**Release job, every step driven by hand at this seat (the eight besides step 12):**

```
rc=0  _gate_frozen_release.py --check       PASS — 3 arm(s) asked, no frozen surface moved.
rc=0  _gate_frozen_release.py --selftest    17 bites, 0 fail(s)
rc=0  _gate_release_audit.py --check        PARKED DUE — 5 parked item(s) due at release-cut
rc=0  _gate_release_audit.py --selftest     10 bites, 0 fail(s)
rc=0  _gate_release_audit.py --pack         SKIPPED — Apollo-Spider-v1.0.9.zip is FROZEN HISTORY
rc=0  _gate_ci_template.py --check          PASS — parses, ships what it calls, hides nothing.
rc=0  _gate_ci_template.py --selftest       10 bites, 0 fail(s)
rc=0  apollo-spider/cold-start/gen_projections.py --check   3 projections in sync
```

**`gates` job — NO NEW FAIL INTRODUCED, and the inherited ones left alone.**

```
rc=0  knowledge/_tests/test_gates.py                 27 gate bites
rc=0  knowledge/_tests/test_advisory.py              19 cases, all bite, none block
rc=0  bash knowledge/_git_commit.sh --selftest       14 bites: 6 fire, 7 silent, 1 hatch
rc=0  knowledge/_gate_artefact_fresh.py --check      (advisory)
rc=0  knowledge/_gate_inline_style_parse.py --check  (advisory)
rc=1  knowledge/_validate_evidence.py notes/_claims  6 lint · 0 unparsed · 4 rc/observation mismatch
       ⇒ INHERITED and UNCHANGED — the frozen #204/#206/#207 residual, `continue-on-error: true` in CI.
rc=0  knowledge/_gen_chain.py --check                _CHAIN.md FRESH, 11,500 tiktoken cl100k_base
rc=0  knowledge/_validate_dataviz.py                 ✅ 15 chart surface file(s) — the receipt's own consumer, green on the NEW receipt
```

**Survey (step 5), non-mutating, `--range` chunks, `--timeout 20`.** Failure set: `[9]` blast-radius sync · `[11]` assertion-veracity selftest · `[38]` component-partials contracts · `[61]` dashboard sync · `[123]` schematic determinism · `[134]` governs matcher. ⚠ **Five steps read TIMEOUT at 20 s** (`[4]`, `[13]`, `[121]`, `[124]`, `[128]`) — **that is this seat's tighter budget, not CI's; CI runs `--timeout 60`.** `[74]` state-contrast is the usual COULD-NOT-ASK (77). ⛔ **Step 6 (`_build_all.py`) was NOT run** — forbidden by the brief, so no verdict on it is claimed here, honestly or otherwise. **None of the six survey reds reads `_receipts.json`**; the only consumers of that file in the repo are `_validate_dataviz.py`, `test_gates.py`, `_probe_fail_open.py`, `_gen_pack_manifest.py`, `_drive_chart_engine.py` and `build-designer-pack.sh`, and every one of them was driven green above.

## PATHS CHANGED, BY CATEGORY

**Regenerated by the drive (1):**
- `knowledge/_tests/chart-engine/_receipts.json`

**Hand-edited (1) — this report only:**
- `notes/_subreports/2026-09-21-292-C-chart-engine-redrive.md`

**Machine appends, PRE-EXISTING at this lane's open and NOT this lane's work (3):**
- `knowledge/_graph-mark-observations.jsonl` · `notes/_REHEARSAL-LOG.jsonl` · `notes/_dream/_GRADE-DECISIONS.jsonl`

**Untracked, pre-existing (1):** `notes/_lanes/292/`

⛔ **`GOOD-MORNING.md`, `_CHAIN.md`, `_LIVE-STATE.md`, `_state.json` and `_rulings.json` were NOT touched** — confirmed by `git status --short`, which names none of them.

## RULING-SHAPED QUESTIONS

⛔ **Only Dave decides these. Nothing below was decided at this seat.**

1. ⬛ **The receipt has a freshness check and no runner, so a canon edit stays invisible until someone tries to cut a release.** `_drive_chart_engine.py --check` is not in `_build_all.STEPS` and not a CI step; `canon.css` moved on 2026-09-19 and the first thing that said so was the release job, four sessions later. **Should `--check` be wired as a step — and if so, blocking or advisory?** It is a browser-free hash compare, so it has no legitimate refusal.
2. ⬛ **The re-drive silently changed the browser the receipts were measured with — Chromium 151 → 153, a major bump — and nothing in the repo grades that.** The receipt records the version; no gate reads it. **Should a re-drive on a different Chromium major be allowed to land without a declaration, given the receipt is evidence for a BLOCKING dv-004 verdict?** The measurement-identical diff here is evidence, not an answer.
3. ⬛ **The release job is now green end to end at this seat, and `_gate_release_audit.py --check` reports `PARKED DUE — 5 parked item(s) are due at release-cut`.** Whether to cut is `s219-D4(2)` and untouched here.

COUNTS: findings `4` · ruling-shaped `3` · UNPROVEN `1` · files regenerated `1` · files hand-edited `1`

REPLAY-THESE:
```
pip install tiktoken --break-system-packages
export NODE_EXTRA_CA_CERTS=/etc/ssl/certs/ca-certificates.crt
python3 -m playwright install chromium
apt-get download libxdamage1 && dpkg-deb -x libxdamage1_*.deb ~/.local/xd
cp ~/.local/xd/usr/lib/*/libXdamage.so.1* ~/.local/lib/
export LD_LIBRARY_PATH=$HOME/.local/lib APOLLO_PW_LD_LIBRARY_PATH=$HOME/.local/lib

python3 knowledge/_drive_chart_engine.py --check                  # 27 FRESH
bash apollo-spider/build-designer-pack.sh --selftest              # exit 0  ← step 12
python3 knowledge/_validate_dataviz.py                            # the receipt's consumer
python3 knowledge/_gen_chain.py --check                           # FRESH
python3 knowledge/_tests/test_gates.py && python3 knowledge/_tests/test_advisory.py
git status --short                                                # one regenerated file
```
⚠ **UNPROVEN AND DECLARED:** this lane never reached the GitHub API — nothing was read from the run on `753d48a1` / `de0aec41`. **Every verdict above is a local re-drive of CI's own commands, at this seat, on this tree.** The claim that step 12 goes green *in CI* is an inference from a byte-identical local run, not a read of a job log.
