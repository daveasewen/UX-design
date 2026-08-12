# #164 — the gate that could not run, and the five sessions that walked through it

```
provenance: 164 · 2026-08-12
status: observed
```

*Narrative dossier (ritual step 1b). Spine entry: `_LIVE-STATE.md` ⏱ LATEST delta #164 · banner:
`GOOD-MORNING.md` ★ LATEST #164. Commits: `434c455` · `3ef22c7` · `7543b48` (all pushed) + this wrap.
Model: `claude-fable-5` conductor + two OPUS build subs + this OPUS wrap sub. Dave live.*

## Why this session looks like a detour and is not one

#164 opened as a side-lane about **borrowed instruments** — a product brief, not a build — and ended
holding the most consequential *finding* of the last five sessions: **`_build_all.py` has been dying
before step 1 since #158, so step 13's provenance gate has not run, so five sessions' rulings were
inscribed ungated.** Nothing about that was planned. It surfaced because a brief-writing lane needed
a green build to say "nothing enacted" honestly, and the build would not go.

## Finding 1 — the brief that was allowed to be a brief

`_BRIEF-borrowed-instruments-2026-08-12-v1.md`, then `-v2.md`, committed at `434c455`. Status is
**RULED-TO-EXPLORE**: Dave's word parked enactment for the Friday sessions. The version discipline
held (`-vN`, never overwrite), and the v2 exists because v1's framing was superseded in-session
rather than edited over.

⛔ **The commit itself reproduced the #133 msgfile-prefix class, instance 9.** The first attempt
(`ac5ecac`) carried a **DOUBLED `after #N <date> —` prefix**, because the msgfile already contained
what SESSION_N mode generates. Repaired by amend from a **fresh `printf` msgfile** before pushing.
The lesson has not changed and the class has not been gated: the script prefixes; the msgfile must
not. What #164 adds to the record is only the count.

## Finding 2 — the showroom was six pages out of sync and nobody knew

`gen_showroom.py --check` was RED on 6 pages: the #158 banner/badge-ink enactment had changed the
snippets and the generated pages were never regenerated. Regenerated in `3ef22c7`; `--check` now
**rc=0, 75 pages + index in sync** (re-driven by this wrap sub, not relayed). This is the ordinary
form of the generated-never-inherited law failing quietly: the generator is the truth, but nothing
was *running* the generator.

## Finding 3 — the build died before step 1, and the cause was two missing table rows

`_build_all.py`'s `ROUTE_ROWS` is a table of `(step label, kind, remedy)`. The two **help-gate steps
added at #158** were registered as steps but given **no route rows** — so the very first lookup
failed and the build aborted before step 1 ran. Two rows (both `ABORT`, like every other
gate+selftest pair) fixed it, and the build then reached **step 13** for the first time since #158.

★ The shape worth keeping: **a new step silently bypassed the table that governs steps.** The
omission was invisible because its symptom (build dies at the top) reads as an environment problem,
not as a missing row.

## Finding 4 — step 13 was red, and it had been unable to be red for five sessions

With the build reaching step 13, `_governs.py --selftest` came back **RED**, in two layers:

- **(a) an environment layer** — `tiktoken` absent env-side (the sandbox disk is ~full; the working
  recipe is a session-suffixed `--target /var/tmp/...`);
- **(b) 15 REAL failures** — rulings **`s157-D1` … `s163-D1`** in `knowledge/_rulings.json` missing
  `governs` / `evidence` / `status`, or carrying **prose evidence without the legal pointer form**
  (`chat #<n>` / `commit <sha>`). Re-driven by this wrap sub: **15 FAIL lines**, unchanged.

⛔ **This is the instrument-without-a-consumer class, in its purest form: the gate did not fail,
because the gate could not run.** Five sessions inscribed rulings behind a green-looking wall.

★ **A sixteenth failure was a FALSE positive, and fixing it at source is the part that generalises.**
`PATHISH_RE` extracted `knowledge/snippets/Tooltip.reference.html` as `…/Tooltip.reference` — its
final-segment class excluded `.`, so **double-extension filenames**, which are the norm in
`snippets/`, were truncated and then reported as pointing at a non-existent file. The **extractor was
wrong, not the pointer**; fixed in `3ef22c7` with fixture-driven checks, 16 → 15. Fixing the pointer
would have been the conflated repair: a true rot-detector taught to accept a mangled path.

⛔ **The 15 are NOT this session's to fix, and were not touched.** Authoring `governs`/`evidence`/
`status` values for someone else's rulings is inventing provenance — the exact failure the gate
exists to catch. They are Dave-side, targeted at the **Friday 2026-08-14 housekeeping session**.

## Finding 5 — the 42-verdict controller, and the honest thing about its name

`reviews/pri-hover-verdicts-42-v1.html` was built by an OPUS sub and render-verified: **42 cards, 0
console errors, live hover, localStorage persistence, well-formed JSON export**, and the conductor
separately verified **zero pre-selected inputs in the markup** — a controller that pre-picks is a
controller that rules.

⚠ **Scope note, recorded rather than smoothed:** the 42 are the **whole token-fork ledger from #139**
(`knowledge/_TOKEN-FORK-LEDGER.json`), of which `--pri-hover` is **one card**. The filename came from
the original brief and **undersells what the artefact is**. ⛔ Not renamed here — the naming question
is Dave's, and it is carried as an open question, because a wrap that renames a review artefact has
quietly re-scoped the review.

## Finding 6 — the dashboard, ruled

Dave, verbatim: *"this is a priority after the side quest, it will really help me."* Recorded in
`_BRIEF-progress-dashboard-2026-08-13-v1.md` (`7543b48`): **Mono components + the
`swiss-design-system` skill aesthetic**, generated from the stores (never hand-edited), build session
**2026-08-13** after his sidequest, and a **candidate agenda screen for Friday's housekeeping**.

## Where it leaves us

**Resolved:** the build routes past step 13 · the showroom is in sync · the `PATHISH_RE` truncation
is fixed at source · three briefs are inscribed and pushed.
**Open:** the **15 provenance fails** (Dave-side, Friday) · **T2** — `selftest_growth` *crashes*
rather than failing named when `tiktoken` is absent (`_capture_gate.py:5307`), a crash-vs-named-FAIL
ruling that is not this wrap's · **T3** — the sandbox disk, an environment chore · the **controller's
name/scope question** · and **Dave's sidequest**, which is the next fresh lane and whose subject he
has not yet stated.

⛔ **This dossier rules nothing.** Every open item above is carried, not decided.
