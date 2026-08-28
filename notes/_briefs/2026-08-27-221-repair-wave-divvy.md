# #221 REPAIR-WAVE DIVVY — 2026-08-27 (Thu)

**Conductor:** Fable seat, #221. **Workers:** 4 Opus lanes (A–D), then 1 Opus adversarial verifier.
**Mission:** enact the repairs the #220 six-lane audit priced and expressly did not make ("next-session lanes by the wave's own fence"). Today is the next session.
**WHICH BUDGET BINDS (name it first):** QUOTA is use-it-or-lose-it before today's reset — effectively free. The conductor's window FILL is the binding budget. Therefore: subs do the work, chat gets stubs, files get the truth.

## Findings sources — cite BY PATH, verify the premise in the tree FIRST
The audit ran yesterday; a premise ages faster than a rule. Before fixing anything, REPLAY the finding you are about to fix (run the probe the report names) and record whether it still reproduces at today's HEAD.

- Lane A source: `notes/_subreports/2026-08-27-220-audit-L1.md`
- Lane B sources: `notes/_subreports/2026-08-27-220-audit-L2.md` + the mechanical (non-fork-value) findings of `-audit-L3.md`
- Lane C source: `notes/_subreports/2026-08-27-220-audit-L4.md`
- Lane D sources: the priced-never-built carries named in its section (each names its origin receipt)
- All lanes: `notes/_subreports/2026-08-27-220-replay-discharge.md` — any of its 12 RED items that fall inside your region are yours to repair; name each one you take or decline.

## GLOBAL FENCE — DO-NOT-RULE (binding on every lane)
1. `knowledge/_rulings.json` is READ-ONLY. No sub writes it, ever (`_inscribe_ruling.py` is conductor+Dave machinery).
2. NO promotions and NO tier changes: every advisory gate stays advisory; every new instrument is born ADVISORY and says so in its own header. Promotion is Dave's word.
3. NO row of `knowledge/_state.json` is closed, reworded, or minted by a sub. Report what a row needs; the conductor mints.
4. NO ruled VALUE changes: token values, per-theme mints, defaults, thresholds, bands, stop lines, walls, lanes. If a fix seems to require one, STOP that item and file it as a RULING-SHAPED QUESTION.
5. Mono's gallery default is Dave's one word. Do not touch anything that expresses a mono gallery default.
6. NO `git commit`, NO `git checkout`, NO push, NO release/bake, NO `_to_delete/` moves. Working-tree edits only; the conductor commits per lane.
7. DO NOT run `_build_all.py` (any partial run strands the tree mid-build). Run targeted scripts only.
8. DO NOT regenerate `knowledge/_proforma/DataViz-interactive.html` (W-176: artefact is AHEAD of its generator; a blind regenerate deletes ~7KB and flips the dark ground to #000000).
9. Regeneration discipline: if you regenerate ANY member of an ordered serial set, run the WHOLE serial for that wave — ramp first, index last (#210 paid ~6 CI reds for skipping this).
10. Stay inside your lane's REGION (named below). If a real fix wants a file outside your region, file it as a handoff in your report instead of editing.

## GLOBAL PITFALLS — consequences replayed (Dave #165)
- **Sandbox call-boundary kill ~178s:** nothing survives a tool-call boundary; drive steps individually, never one mega-command. `tiktoken` is already installed this session.
- **ENOSPC:** use `/var/tmp` for scratch if `/tmp` fills.
- **`_capture_gate.py --selftest` WRITES `knowledge/_CAPTURE-GATE.md`** (the #158 write-by-default door, unfixed until Lane D lands). If you run it, restore with `git show HEAD:knowledge/_CAPTURE-GATE.md > knowledge/_CAPTURE-GATE.md` (this mount refuses `git checkout`).
- **#173 class:** a gate that cannot pass (or cannot fail) in one environment is a defect. Every bite you add must be drivable to BOTH verdicts locally, and must not depend on macOS-only or CI-only facts unless it declares the environment split explicitly.
- **A crash is not a fail:** parse helpers fail LOUD and NAMED; declare residuals.
- **Unmatched grep ≠ absence; matched ≠ presence** — name the probe, quote the line.
- **Green tests can't see scope:** after building any new instrument, DRIVE it on real data and report what it caught. An instrument without a consumer is not a deliverable — wire it (advisory) or name where it will be run.
- **A mutation test proves the CLAUSE, not the FEATURE:** plant the defect, watch the gate fire, remove it, watch it clear — both directions, per claim.
- Paths: file tools use `/Users/daviewen/Documents/Claude/Projects/UX-design/...`; bash uses `/sessions/eloquent-zealous-bohr/mnt/UX-design/...`.

## REPORT CONTRACT (every lane, and the verifier)
File a full report at `notes/_subreports/2026-08-27-221-<lane>.md`. Chat return = a STUB: lane name, report path, COUNTS line, one sentence.
The report MUST carry, in this order: **COUNTS:** (items taken · fixed-at-cause · bites added · mutations driven both-ways · declined-with-reason · UNPROVEN) · **FINDINGS** · **RULING-SHAPED QUESTIONS** (anything that needs Dave) · **REPLAY-THESE** (exact commands a verifier reruns) · **UNPROVEN** (honest, priced) · **FILES TOUCHED** (every path, for the conductor's reconcile) · **USAGE:** your own total token usage if you can read it, else `UNMEASURED — declared`.
Fixes are REAL fixes at cause, never patches; where the defect is a class, the fix includes the (advisory) gate or bite that would have caught it.

---

## LANE A — CI + the false-green class
**Region owned:** `.github/workflows/**` · `knowledge/_validate_wiring.py` · the specific `knowledge/_gate_*.py` / `knowledge/_validate_*.py` files L1 proved blind + their bite/selftest files · any committed gate artefacts L1 found stale + (new file) an advisory stale-artefact comparer.
**Tasks (from L1, replay each premise first):**
1. The CI `gates` job has been RED AT ITS FIRST STEP since `aa26947`. Find the cause in the workflow, fix at cause. CI itself is unreachable from this seat (`gh` absent, API 404s): prove the fix with the local bare-clone proxy the L1 report used, and say plainly that the green is a local proxy — the CI read-back stays Dave's.
2. The eight false greens: fix at cause the two BLOCKING gates blind to CSS logical properties and the one blind to `style=""`; for each of the four planted-defect-proved blindnesses, land a bite pair (planted defect fires / clean tree clears).
3. `_validate_wiring.py` is green only because its glob cannot see the `_gate_*.py` namespace — widen at cause + bite.
4. Five committed gate artefacts stale at HEAD with nothing comparing them: build the advisory comparer, drive it, report what it catches today.
5. "The fleet's static leg has no HTML or CSS parser anywhere" is the #122 class (first gate = PARSE in the consumer's grammar). Do NOT boil the ocean: build ONE seed advisory parse-gate over the narrowest population where a parser would have caught a proved false green, drive it, and price the rest.
**Lane pitfalls:** do not "fix" CI by weakening a step; the L6 trims touch CI too — they are NOT yours unless they fall inside a fix you are already making at cause. Do not re-derive CI state from scratch — L1's measurement is the premise, replay it via the proxy.

## LANE B — generators
**Region owned:** `knowledge/gen_dashboard.py` (+ its artefact) · `knowledge/gen_library_214.py` · the `SPACING_STOPS` homes · the 5 sibling generators with drifted fallback cause-sites (L3 names them) + their selftests · the fork-ledger rows + probe README L3 names.
**Tasks:**
1. `gen_dashboard.py --check` can return 0 or 77 and never 1 — give the BLOCKING check a reachable FAIL path (drive it to both verdicts), then regenerate its stale dashboard (store now ~299 items) via the proper serial.
2. `gen_library_214.py` is byte-identical on macOS and silently degrades on Linux (case-sensitivity), taking 7 components: fix at cause (normalise the references — do NOT blind-rename files on this case-insensitive mount), and add a bite that FAILS on a casing mismatch on both platforms.
3. `SPACING_STOPS` lives in two homes and one carries a comment claiming it is the only home: consolidate to ONE home + addresses (ADR-0017 WRITE-ONCE), fix the lying comment, add the bite.
4. L3's 16 drifted fallback cause-sites across 5 sibling generators: repair at cause (fallbacks must re-derive, not restate), bite the class.
5. Fork-ledger rot (5 rows) + the probe README asserting 64 findings that are gone: make the artefacts tell today's truth; where a figure should be generated rather than typed, generate it.
6. `_validate_token_forks.py` answers two questions and only the permissive one is wired (0 wired / 1 under `--strict` on 98 forks): produce a TRIAGE TABLE of the 98 forks (real defect / intended override / stale) in your report. CHANGE NOTHING about the gate's wiring or the fork values — both are ruling-shaped, file them as such.
**Lane pitfalls:** regen serial is ORDERED — ramp first, index last, whole serial per wave. Dangling dataviz var = SILENT BLACK. Fence 8 (never regenerate `DataViz-interactive.html`). No token VALUE moves — a fallback repair re-derives the same value; if it wouldn't, stop and file.

## LANE C — the designer pack's first hour
**Region owned:** `memento-package/**` · `knowledge/_release/**` (scripts + docs only — NO bake) · `.github/copilot-instructions.md` + `.github/prompts/**` · pack-side docs the L4 report names.
**Tasks:**
1. `tiktoken` is documented *Optional* while the wrap step hard-REFUSES without it. The refusal is CORRECT (a measuring tool must not guess) — fix the DOCS to say REQUIRED and make the pack's cold-start path install/verify it before a designer reaches the refusal.
2. The retrieval signpost names a script the pack does not carry: ship the script or fix the signpost — whichever the packed corpus says is the real intent; say which you chose and why.
3. The runner's phantom zero-population logic: fix at cause.
4. no-playwright FAIL-vs-CNA: absence of the renderer must read COULD-NOT-ASK, never FAIL.
5. The 9 doc-vs-behaviour drifts (3 claims failed when driven): align doc to behaviour or behaviour to doc — the ruled side wins; if neither side is ruled, pick behaviour and file the choice as ruling-shaped.
6. Build the priced doc-resolver bake gate (~2.5K, L4) — advisory at birth, driven both ways.
**Lane pitfalls:** everything lands repo-side for the NEXT release — v1.0.1 is frozen history and no bake runs today. The release-audit `--pack` arm now speaks for ONE version (`b6f5ad0`) — do not "fix" it back. The pack-import gate stays fenced out of the gates roster (`RELEASE_SIDE_GATES`) so the ruled 55 does not move.

## LANE D — priced-never-built machinery debts
**Region owned:** `knowledge/_capture_gate.py` (EXCLUSIVE — no other lane touches it) · new instrument files you create · `knowledge/_state.py` READ-ONLY.
**Tasks (each carries its origin in the chain carries; replay the premise first):**
1. Boot-drift parser: *"a delta beside `boot` is not a reading"* — `_parse_boot_samples` refused a prose phrase carrying a delta (#215 case). Fix the parser at cause + bite with the original offending sentence.
2. The #158 write-by-default door: `_capture_gate.py --selftest` writes tracked `knowledge/_CAPTURE-GATE.md`. Fix the class: selftests write to scratch, never the tracked file. Bite it.
3. The regen-serial class fix (third conductor instance): an advisory check that a regen wave touched the whole ordered serial (ramp→index), not a subset.
4. The register-vs-store join check: `_GOVERNING-RECORDS.md` rows vs `_state.json` G-rows drift (three rows proved it) — advisory join checker, driven on today's real data.
5. The `mask_comments` dedup: duplicated across two generators with no comparing gate — build the advisory comparer (do NOT refactor the generators themselves; that is Lane B territory and a ruled-refactor question).
6. The capture-gate INSTRUMENT-STRAY re-scope: it refuses the exact artefact class `s217-D1` ruled legal (untracked web derivatives) — re-scope at cause so ruled-legal populations pass while the #138 class still fires. Bite both directions.
**Lane pitfalls:** `_capture_gate.py` is load-bearing wrap machinery — after EVERY edit, run its selftest (then restore the tracked file per the global pitfall until your fix 2 lands, after which prove the door is closed). Keep each fix a separate, revertable edit; the conductor commits this lane last.

---

## VERIFIER (after lanes land, separate Opus sub)
Read the four lane reports. Replay every REPLAY-THESE item. Drive every new bite BOTH directions. Grade each lane's claims green/red/could-not-run. REPAIR NOTHING; rule nothing. File `notes/_subreports/2026-08-27-221-verify.md` per the report contract.
