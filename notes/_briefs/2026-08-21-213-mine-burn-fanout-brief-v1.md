# PM brief — #213 mine-side burn-down fan-out (hand-minted, conductor's seat)

> ⛔ **DATED PERIOD RECORD, NOT A LIVE HOME.** Minted 2026-08-21 by the #213 Fable conductor.
> The store stays the one live home (`knowledge/_state.json`, `knowledge/_rulings.json`).
> **Nothing a sub writes is a ruling.** Only `knowledge/_inscribe_ruling.py` writes rulings, only on Dave's word.
> Hand-minted (not gen_brief.py): these rows sit outside a lane record; every premise below is therefore
> a CLAIM the sub must re-probe before building on it — probe commands are given per lane.

| governance | value |
|---|---|
| session | #213, Fable conductor + Opus subs (quota-parity routing, Dave's word this morning) |
| rows served | `W-99` (s212-D1) · `W-99a` (s212-D2) · `W-59` (Dave's #209 fork sanction) · survey of §C·1 residual |
| serial set | registry · MIGRATED_SNIPPETS · CATEGORIES · spine · git — **CONDUCTOR'S ONLY**, one commit |

---

## FENCES — every lane, no exceptions

1. ⛔ **NO git commands of any kind.** No commit, no checkout, no stash, no add. The conductor owns git. (`specimen-starts-from-reference` runbook step 0: sub git-checkout ban.)
2. ⛔ **DO NOT edit shared state**: `GOOD-MORNING.md` · `_LIVE-STATE.md` · `MEMORY.md` · `_CHAIN.md` · `knowledge/_state.json` · `knowledge/_rulings.json` · any `_lanes.json`/registry/spine file. Your outputs are NEW dated files + the in-place code edits your lane explicitly names.
3. ⛔ **DO-NOT-RULE.** Dave owns 28 open rows and every open question named in any receipt. If your work surfaces a choice, write it PROPOSED-not-ruled in your receipt. Named live hazards you will meet:
   - the **B-D4 #808080 vs #9D9D9D value-drift question** — returns to Dave separately (s212-D1's own words);
   - the **dark twin of #9D9D9D** — UNRULED; propose explicitly, never assume;
   - **P8** (routing conflict), the **#211 seven-receipt sitting**, **W-95** strike-list — all Dave's, untouchable;
   - fintech/semantic bindings, promotions of probes, anything in `_DS-IMPROVEMENTS.md` candidature.
4. **Version, don't overwrite** — `-vN` filenames; sandbox cannot rm (use mv).
5. **Every "landed" claim names its evidence** (gate run · file path · render) — evidence-pointer rule. A claim without a probeable token is not a claim.
6. **Bounded verification (s172-D3):** targeted proof, depth cap 1, no new instruments beyond the lane's need; prove ONE seam can fail, not breadth.
7. **Mutation-proof the clause you changed by DRIVING THE THING** — a green assert on your own fixture proves nothing (#104, ×2 at #209).
8. **A crash is not a fail** — helpers fail LOUD and NAMED; declare residuals.
9. **The user is not watching**: proceed on reversible actions that follow from this brief; an end-of-turn promise is not a completion — do the work or flag the blocker.
10. **Unmatched grep ≠ absence** — name the probe; matched ≠ presence — quote the line.

## PITFALLS / CONSEQUENCES (mandatory replay, Dave #165)
- #202: five builds argued about a component that didn't exist — **re-probe every premise in this brief before building.**
- #184: a dangling `var()` renders SILENT BLACK and 13 gates are blind to it — after any token edit, drive a render.
- #210: regen serial set is ORDERED — you don't run it (conductor's), but name in your receipt which serial steps your work obligates.
- #171: self-comparing asserts pass on their own mutants — bites must be able to FAIL.
- Generators: ds-018 history says hand-patching canon.css instead of the generator guarantees recurrence — **fix the CLASS in the generator.**

---

## LANE E1 (Opus) — `W-99`: ds-018 disabled-state ENACTMENT (s212-D1)

**Ruled (quote, work to these words):** recessive disabled grey = **#9D9D9D** (mono-9/neutral-9). Constraints carried verbatim from Dave's notes: *"--text-disabled fixed in the SAME pass as --border-disabled; the disabled block is regenerated per chart family so the fix lands in the GENERATOR, never a canon.css hand-patch; every proof ships a bite proving it can FAIL and absence-claims carry a detectable-when-present arm; settle transitions before reading computed styles and compare colours AS COLOURS."*
**Light+dark:** the dark twin is UNRULED — pick one explicitly, mark it PROPOSED in your receipt and in a `$note` at the value site, and show light+dark paired explicitly, never assumed.
**Probe first:** read s212-D1 in `knowledge/_rulings.json`; locate the ds-018 record in `knowledge/_DS-IMPROVEMENTS.md`; find the generator(s) that emit the disabled block (grep for `--text-disabled` / `--border-disabled` / `disabled` across `knowledge/` generators — quote the emitting lines in your receipt before editing).
**Deliver:** generator edits + regenerated outputs left UNCOMMITTED · a driven render proof per theme (FOUR themes — mono, legacy, console, supercharge — test PER THEME, light+dark) · receipt `notes/_receipts/2026-08-21-213-laneE1-w99-ds018-enactment.md` with premise table, bites (shown failing on a mutant), residuals, and the B-D4 drift question restated for Dave.

## LANE E2 (Opus) — `W-99a`: G17 RAG manifestation A+B+C into canon (s212-D2)

**Ruled (quote):** *"The RAG status canon pick … is A+B+C — all three manifestations are canon."* Governs `knowledge/_GOVERNING-RECORDS.md`.
**Probe first:** read s212-D2; read the G17 row in `knowledge/_GOVERNING-RECORDS.md`; open `reviews/RAG-STATUS-MANIFESTATION-2026-07-19-v1.REVIEW.html` to identify exactly what A, B and C are (quote the artefact, never re-derive from memory); survey (grep) where RAG status manifests in canon/generators today.
**Deliver:** the wiring that makes A+B+C canon (generator/canon edits as the artefact defines them, uncommitted) · driven render proof per theme · receipt `notes/_receipts/2026-08-21-213-laneE2-w99a-rag-canon.md` — premise table, evidence pointers, any open choice PROPOSED-not-ruled. ⚠ `_GOVERNING-RECORDS.md` row-state updates are the CONDUCTOR'S — name the exact row edit you propose, don't make it.

## LANE E3 (Opus) — `W-59`: rename the 5 ledgered local-var collisions

**Premise:** 5 local-var collisions are LEDGERED somewhere in-repo (receipts or `_DS-IMPROVEMENTS.md`); the class fix is component-local names; Dave sanctioned the fork at #209.
**Probe first:** FIND the ledger (grep `collision` across `notes/_receipts/` and `knowledge/`); quote the 5 entries verbatim in your receipt. If the ledger cannot be found, STOP and return the named probes you ran — do not reconstruct the list from inference.
**Deliver:** the 5 renames applied component-locally (uncommitted) · proof each rename resolved the collision AND a driven render showing no dangling var (SILENT BLACK class, #184) · receipt `notes/_receipts/2026-08-21-213-laneE3-w59-var-renames.md`.

## LANE S (Opus, READ-ONLY) — §C·1 residual survey

**The job:** waves 3–6 ran at #209/#210. What of §C·1 strands (a)–(d) — chart expansion · wave 3 · templates/shells · enact window — is genuinely still open? Survey `_LIVE-STATE.md` lane-2 rows, the #209/#210 fanout briefs + lane receipts, `knowledge/_lanes.json`, and the store. **BUILD NOTHING. RULE NOTHING.**
**Deliver:** `notes/_briefs/2026-08-21-213-c1-residual-survey-v1.md` — per strand: LANDED (evidence pointer) / OPEN (what remains, sized S/M/L in job-window tokens) / BLOCKED-ON-DAVE (which row) — plus a proposed divvy plan (lanes · models · shared files each assigned to ONE lane) for the conductor to fire next.

## RETURN CONTRACT — every lane
Receipt file at the named path; premise table (probe · result · timestamp); claims each carrying a probeable token; residuals declared; open choices PROPOSED-not-ruled with the question stated in Dave's terms. The conductor replays every receipt to Dave and owns the serial set + commit.
