# #120 — The build was fine; the verdicts about it weren't

provenance: trusting-upbeat-mendel #120 · 2026-08-07
status: observed

## The arc

**1 · The fixture drift, diagnosed before it was fixed.** `_test_git_commit.py` had been RED since
#116 on a mechanical cause: the commit-seam harness's fixture environment never picked up
`SESSION_N`, and `_session.py` itself had grown a stub dependency the fixture didn't provide. The
repair was small — stub `_session.py` in the fixture, set `SESSION_N=77` in the fixture env — but
the session did not stop at "green again." It asked the harder question: a fixture that drifted
once can drift again, and the clauses it exists to protect (the post-#116 session-witness checks)
had no arm of their own asserting they still fire. Two new arms were added —
`wrap_undeclared_session_blocks_120` and `wrap_session_witness_refusal_blocks_120` — each written to
go RED if the clause it pins were deleted, not merely if the fixture broke. 20 arms, all green.
This is the difference between "the test passes" and "the test can fail" — a mutation-shaped
discipline applied to the harness's own regression coverage, not just to the code it tests.

**2 · The build's sole remaining red turned out to be content debt, not defect.** The full
`_build_all.py` had not been run end-to-end in weeks (per #119's finding that it had been aborting
since #116). This session ran it directly, for real, and it went 1→73 of 95 steps before stopping —
at the property-resolves C2 selftest, on 114 failures across 87 files, all undeclared
`--alpha-*` / `--mark` / `--phys-size` values. The gate's own text forbids inventing these numbers;
they are DO-FIRST item 1 in `GOOD-MORNING.md`, standing and Dave's, unchanged since before #118.
This is not a new problem this session found — it is the same DAVE-OWED debt the queue has been
carrying, now visible as the literal last thing standing between the repo and a fully green build.
Naming it correctly (his content debt, not an agent defect) matters because the alternative reading
— "the build is still broken" — would have sent the next session hunting for a bug that isn't there.

**3 · Steps 74–95 had never run either, and were clean once driven.** Nothing downstream of step 74
had executed in the same period. Run directly by the build sub, three purely mechanical fixes cleared
it to PASS 0 errors: a stale `AUTO-THEMES` block needing `gen_theme_cascade.py` regen, a pre-existing
memento known-answer FAIL (declared and deliberately left unfixed since #115) closed by re-pinning the
slug at `_memento_search.py:142` to the rebuilt index's actual answer, and three chart meta files
(`Chart-histogram`, `butterfly-v`, `butterfly-h`) carrying a stale `worker-composition` provenance enum
where the build now wants `code` — the worker context itself was kept in each `$note` rather than
deleted, and is flagged for Dave's eye as a judgment call, not silently resolved.

**4 · The finding that reframes #118's verdict: `_validate_screen.py` was never rotted.** #118 had
called it ROTTED off a crash (`ValueError: too many values to unpack`) and exempted it from the
wiring gate rather than repairing it — a reasonable call at the time, made without driving the file
past the crash. This session did: the crash was one line, a drifted `a11y.check()` call signature
(unpacking 3 values against the s114-D5 6-tuple contract it was written against). The fix was a
one-line unpack at line 63. It was mutation-tested the same way the #109 dossier tested its own
finding — an unguarded transition was injected on purpose, and the fixed checker named it correctly
as a 2.3.3 failure rather than crashing again. UN-EXEMPTED and WIRED into the wiring gate: 30
validators on disk, 29 wired, 1 exempt, 0 failures. `_validate_state_contrast.py` stays the one
exemption, but with a sharper reason than "environmental" as a shrug: playwright's module installs
fine, but its chromium download is blocked by the sandbox's TLS chain
(`UNABLE_TO_GET_ISSUER_CERT_LOCALLY`, tried against all 3 CDNs) — a fact worth re-checking if the
sandbox's cert posture ever changes, not a fact worth re-diagnosing from scratch next time.

★ **The general lesson, stated plainly because it is the throughline of the whole session:** a
verdict of "ROTTED" or "impossible to run" is a claim about what was tried, not about the artefact.
`_validate_screen.py` needed one line. The full 95-step build runs in the sandbox in under a minute
once actually attempted. Both verdicts had stood for sessions because nobody drove past the first
error. [[a-crash-is-not-a-fail]] and [[green-tests-cannot-see-scope]] both point at the same
discipline: run the thing, don't infer its state from a summary of a summary.

**5 · Titling was mechanised, closing #119's own post-wrap residual.** `_gen_titles.py` now derives
both the RENAME and the NEXT-SESSION-TITLE lines directly from the ★ LATEST banner headline and its
top residual item, writing a receipt (`_gen_titles_receipt.json`) and raising a named
`TitleDeriveError` rather than guessing when either input is missing. Own 4-bite selftest; wired into
`_capture_gate.py --wrap` as `title_generation_check` (receipt present, both lines present,
`banner_session` matches the session actually wrapping — 4 refusal arms bite-tested). Chat delivery
of the two title lines becomes a paste of the receipt's own text, never a re-derivation from prose
recall — the exact mechanism #78's `{17}`-literal class and #33's chain-diet lesson both argued for:
an instruction that lives only in prose is not a checked instruction.

## What's still open

Dave's ds-018 token values are now the **sole** blocker between the repo and a fully green 95-step
build — nothing else stands in front of it. The three provenance-enum edits (§3) are a judgment call
flagged for his eye, not a silent resolution. P1 confirm-to-open, G4 ratify, and the recorder-constants
refresh remain exactly as #119 left them, unanswered. Full residual list: `GOOD-MORNING.md` ★ LATEST
#120 banner, `→ #121`.

Both-way links: `GOOD-MORNING.md` ★ LATEST — 2026-08-07 #120 · `_LIVE-STATE.md` ⏱ LATEST DELTA #120.
