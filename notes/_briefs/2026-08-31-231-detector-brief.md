# #231 LANE BRIEF — retrieval-vs-interpretation detector (repo-side)

provenance: #231 conductor (Fable) · 2026-08-31 · Dave approved build-today, repo-side.
Row: W-325 (minted at creation). Report: `notes/_subreports/2026-08-31-231-detector.md` (file FULL report there; chat gets a stub — s218-D7, include a REPLAY-THESE section).

## THE GOAL — Dave's finding, verbatim (from `notes/_receipts/2026-08-31-230-postwrap-dave-v102-test.md` — READ IT FIRST)

> "it seems to interpreted rather than get the component, it was really close but I could
> tell it was built locally rather than retrieved... bit odd"

No shipped gate can see this: a close paraphrase passes compose/icon-source/a11y and drifts
silently. Build the instrument that reds on it.

## Deliverable

`knowledge/_detect_provenance.py` (adjust name to repo convention if a stronger precedent exists — say why in the report):
1. Fingerprints DERIVED FROM `knowledge/snippets/` AT RUN TIME (generator, never a baked list — a baked list rots the day a snippet lands; mint-time derivation s200-D1 idiom).
2. Structure-only signature (tag sequence + class chains). NEVER content: Dave's data/copy/labels/aria text must not move the reading.
3. Grades a built HTML file per component family: SPLICED (structural match) · PARAPHRASE (close but drifted) · ABSENT. Output names the snippet, the score, the evidence lines.
4. Refusals LOUD and NAMED, rc nonzero ([[a-crash-is-not-a-fail]]). UNKNOWN never defaulted.
5. Selftest MUTATION-TESTED both directions — and DRIVE THE THING on real files, not only fixtures ([[mutation-tests-the-clause-not-the-feature]], [[green-tests-cannot-see-scope]]).

## Real data — probe before you plant

Search the tree for Dave's v1.0.2 test output (try `_incoming*`, `uploads`, recent mtimes). His interpreted charts are the ground truth. If absent: build planted paraphrases (3 grades of drift) and DECLARE the approximation prominently — the real-sample proof is then a PRICED TODO, not a silent gap.

## The threshold is RULING-SHAPED — render readings, never pick

Where SPLICED ends and PARAPHRASE begins is Dave's dial. Render 2–3 candidate thresholds SIDE BY SIDE against the same samples into `reviews/DETECTOR-READINGS-2026-08-31-v1.html` (live specimens, light+dark, [[feedback-mock-the-readings-before-building]], version -vN never overwrite). Rendering: read `_RUNBOOK-render-verify.md` FIRST — everything MOUNT-SIDE, `TMPDIR=/dev/shm`, no `set_content()`, canvas probe not fonts.check(). Sandbox: NOTHING survives a tool-call boundary; wall ~178s — drive steps individually; `pip install tiktoken --break-system-packages` first if any gauge/chain machinery is touched.

## DO-NOT-RULE (violating any line is the #110 defect)

- The threshold value — Dave's, off the readings page.
- Whether/when this ships in the pack — Dave's; roster is HELD at 58 (s228-D5); touch NO release machinery, no version bump, no dist/, no manifest.
- NO writes to `knowledge/_rulings.json` (only `_inscribe_ruling.py` may, and not from a sub) or `knowledge/_state.json`. NO commits, NO push (conductor commits). NO edits to `knowledge/snippets/` or any generated canon.
- Do not invent close conditions, do not close/re-scope any W-row.
- Grep `knowledge/_rulings.json` (298 entries) for prior rulings on provenance/fingerprint/detection BEFORE calling anything open or new.

## Pitfalls replayed (consequences, per Dave #165)

False reds on legitimate variation kill trust in the instrument on day one — structure-only, proven by a mutation that changes ONLY content and must stay green. A detector too loose is a green that cannot fail. An unmatched grep is not an absence — name every probe. If a gate/regen goes red on a pre-existing condition, DECLARE it, don't fix out-of-scope.
