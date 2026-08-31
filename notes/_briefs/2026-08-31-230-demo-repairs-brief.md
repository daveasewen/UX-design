# Brief — #230 repair lane (Opus): the rehearsal's demo-killers, fixed at source tonight

provenance: 230 · 2026-08-31 · conductor Fable · row W-322
Contract: fix the four findings below from `notes/_subreports/2026-08-31-230-rehearsal.md`
(read it FIRST — F-numbers refer to it). Then the conductor commits and re-cuts.

**Dave's ruling tonight, verbatim, BANKED for cold-seat inscription (#231, s214-D1):**
> "use this as teh default logo 'masterbrand-light-colour'"
Context: the rehearsal found a cold builder copies the literal HSBC text wordmark silently
while twelve masterbrand SVGs ship unbound; his target wears the hexagon. His ruling: the
masthead binds `masterbrand-light-colour` by default; the builder asks only when the brief
names a different brand.

## The four fixes (real fixes, never patches — s229-D3 / s228-D7)

1. **F1 — the contract must reach a cold seat.** Place the generated projections into the
   three auto-load hosts (`gen_projections.py` / `verify_placement.py` machinery — make
   placement real in the SHIPPED files, `.github/copilot-instructions.md` included, via the
   generator, never hand-paste). The class fix: placement is generated + checked, so a
   future contract edit cannot silently strand the hosts again. If `verify_placement`'s
   designer-facing exit-0 should stay, its BUILD-time consumer must red on cold hosts.
2. **Bento-ask arm — build Dave's OR.** Per his goal (demo-day brief § ★ THE GOAL): a
   dashboard ask either goes bento-first or ASKS "dashboard bento — is that right?". Wire
   the ask into the auto-loaded surface + `generate-from-canon/SKILL.md` in the contract's
   own vocabulary; skip-friendly like grill-me. It must be REACHABLE cold (the rehearsal's
   column A) — prove by re-driving that column's beat.
3. **Logo — enact Dave's default.** Bind `masterbrand-light-colour` as the masthead default
   in the snippet/meta/skill chain (source snippets, full ordered serial after). If dark
   chrome mechanically requires the dark sibling, wire the theme pair and DECLARE it in the
   report; if that pairing needs a design word, enact light-colour only and raise the dark
   half as a RULING-SHAPED question. The ask-only-if-another-brand behaviour goes with fix 2's
   surface.
4. **F6 — run-gates must pass on a clean pack.** `ci-template/run-gates.py` red on a pristine
   install (23 orphan gates from repo wiring a pack does not have) would print FAIL on stage.
   Gate the condition: the runner must know pack context (e.g. `_MANIFEST.json` presence)
   and scope the wiring check accordingly — a shipped baseline or a scoped skip, stated
   loudly, never a silent pass. Mutation-prove: plant a REAL defect in a scratch pack and
   show the runner still reds on it.

## DO-NOT-RULE

No git (conductor commits) · no `_rulings.json` (Dave's words are BANKED here, inscription
is #231's cold seat) · no W-rows/state · no memory · no roster edits · no `--release`/dist ·
no `_build_all.py`. Regen serial + the per-surface gates you touch, only.

## Report

`notes/_subreports/2026-08-31-230-demo-repairs.md` — COUNTS:, REPLAY-THESE:, RULING-SHAPED
QUESTIONS. Chat STUB: per-fix one-liner + the re-driven cold-column beat count.

## Pitfalls — replayed

- The placement fix is the third "instrument without a consumer" tonight — the checker
  existed and exited 0. Wire the consumer or the class recurs.
- ~178s call wall; TMPDIR=/dev/shm; fonts session-path-bound (three-way probe) if you render.
- The shipped copilot file and SKILL.md are RELEASE surfaces — every edit lands via
  generator/source so the next cut carries it; nothing hand-edited in a generated file.
