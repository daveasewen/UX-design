provenance: #63 sub draft, phase 1 (enumerate+map, no mutations) · status: DRAFT — not ratified

# Bite matrix — `knowledge/_capture_gate.py` (4,099 lines) — PHASE 1: ENUMERATE + MAP ONLY

Method followed: whole file read top-to-bottom in ~300-line chunks BEFORE any selftest run;
claims enumerated from the read; `--selftest` then run ONCE and mapped; a second read-only
pass (via sub-agent grep, no file writes) verified specific call-sites and fixture coverage
claims that could not be settled by inspection alone (whether `title=False` is ever actually
invoked, whether the compactable BLOCK branch is reachable, etc.). No mutation commands were
run anywhere in this pass. `pip install tiktoken --break-system-packages` was run first per
brief (already satisfied on this machine — real tiktoken cl100k_base instrument in use, not
the byte-estimate fallback).

Columns per row: **CLAIM** (numbered, exact lines, entry point) · **BITES** · **MUTATION-RED**
(`NOT-ASKED-THIS-PASS` throughout, per hard rule) · **CANNOT-SEE**.

Entry-point vocabulary used below: **build** = default invocation (`python3 _capture_gate.py`,
no flags) · **wrap** = `--wrap` (non-lane) · **wrap+lane** = `--wrap --lane` (many checks
SKIPPED, noted explicitly) · **selftest** = `--selftest` · **imported** = called only from
another module, not from this file's own `run()`.

---

## G0 — provenance/status field checks (`check_file`, lines 702–753)
Runs at: **build AND wrap** (unconditional — `run()` calls `check_file` for every file in
`in_scope(repo)` at lines 2520–2524, before the mode branch).

**1. Missing `status:` line → FAIL** (lines 723–724).
BITES: PROVEN-BY-SELFTEST ("`2026-07-26-missing-status.md`" fixture, `FIXTURES` dict l.2561).
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE: only checks the first `HEADER_LINES`(40) lines; a `status:` line at line 41+ reads
as absent. Checks presence of the token, not whether the surrounding record is real.

**2. Unknown status value → FAIL** (lines 728–729).
BITES: PROVEN-BY-SELFTEST ("`2026-07-26-unknown-status.md`", `status: vibes`).
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE: vocabulary is a fixed 5-value set (`VOCAB`); a plausible-but-wrong value outside
that set is the only thing this catches — it cannot judge whether a VALID value is honestly
applied (e.g. `status: observed` on something that was actually inferred).

**3. `status: ruled` with no ledger pointer after the value → FAIL** (lines 730–733).
BITES: PROVEN-BY-SELFTEST ("`2026-07-26-ruled-no-pointer.md`").
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE: only checks that *some* trailing text exists after `status: ruled`; does not check
that the trailing text is actually a ledger pointer, only that claim #4 (below) tries a
path-like regex on it IF one is found.

**4. `status: ruled` pointer matches no file on disk → WARN** (lines 735–737).
BITES: UNCOVERED. `FIXTURES` (lines 2558–2567) has exactly one `ruled` fixture with a *valid*
pointer (`_DECISION-HISTORY/README.md`, which the selftest harness creates at lines 4050–4052)
and one with *no* pointer at all (claim #3). No fixture supplies a `ruled` status with a
pointer-shaped string that does NOT resolve to a file — this WARN branch is never exercised.
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE: `PATHISH_RE` only fires on tokens ending `.md`; a pointer to a non-`.md` target
(e.g. a line number, an ADR id with no filename) is invisible to this check entirely — it
neither fails nor warns, it simply never tries to resolve it.

**5. Missing `provenance:` line → WARN** (lines 739–740).
BITES: UNCOVERED. All five `FIXTURES` entries include a `provenance:` line (even the
"missing-status" and "bad-date" ones) — no fixture omits `provenance:` entirely.
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE: soft by design (docstring calls session-id "soft"); this WARN cannot see whether an
*absent* session-id inside a present `provenance:` line still counts as compliant.

**6. `provenance:` with no parseable `YYYY-MM-DD` date → FAIL** (lines 750–752).
BITES: PROVEN-BY-SELFTEST ("`2026-07-26-bad-date.md`", `provenance: sess-x · yesterday-ish`).
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE: `ISO_DATE_RE` matches ANY three-group `\d{4}-\d{2}-\d{2}` in the line, including a
date that is not the file's actual capture date (e.g. a stray reference date to something
else) — it validates form, not that the date is the true provenance moment.

---

## G1 — pre-flight stamp: dispatch + percentage FORM + ds-023 band (`check_preflight`, 927–1051)
Runs at: **wrap only** (called from `wrap_checks` non-lane branch, line 2440); **SKIPPED
entirely** under `--wrap --lane` (note at lines 2426–2427 — "the stamp lives in
GOOD-MORNING.md, which lane sessions do not write").

**7. No `pre-flight:` stamp line found at all → FAIL** (lines 941–945).
BITES: PROVEN-BY-SELFTEST (`PREFLIGHT_FIXTURES[0]`, name "missing", l.2573).
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE: matches on `PREFLIGHT_RE` form only (any line starting with the word
"pre-flight"/"preflight" plus punctuation) — cannot tell a genuinely absent estimate from one
written in a wholly unrecognised shape (e.g. no colon, or a synonym like "context estimate:").

**8. Dispatch: `ABS_TOTAL_RE` match routes to `check_preflight_tokens` (line 950–951)** — not
itself a FAIL/WARN, a control-flow branch.
BITES: PROVEN-BY-SELFTEST (every `PREFLIGHT_TOKEN_FIXTURES` case reaches `check_preflight_tokens`
only via this dispatch, per `selftest_preflight_tokens` calling `check_preflight(text, ...)`,
line 2673).
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE (structural, matches the brief's flagged item): **this IS the mechanism by which the
percentage-form ds-023 band logic (claims 13–19 below, lines 990–1043) goes dormant.** Once a
stamp is written in the `= N of N` absolute form, line 950 returns immediately from
`check_preflight_tokens` and the percentage-band code at 990–1043 never executes for that
session. The percentage path is still fully live and green for any OLDER stamp shape, but a
session that has adopted #56's form structurally cannot exercise (or be protected/warned by)
the `BAND_FLOOR`/`HARD_STOP`/`MARKED_MAX` percentage logic any longer — it is superseded by
`check_preflight_tokens`'s own absolute-budget logic (claims 20–33), not merged with it.

**9. Missing 1+ of fill/job/wrap terms (percentage form) → FAIL** (lines 958–962).
BITES: PROVEN-BY-SELFTEST (`PREFLIGHT_FIXTURES[1]`, "two-term (wrap omitted)").
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE: `TERM_RE` matches the FIRST occurrence of `fill`/`job`/`wrap` near a number anywhere
on the line — cannot tell a genuine estimate from the word appearing in unrelated prose before
the real term (the #58 mention-vs-use class, fixed for the ABSOLUTE path via `_n()`'s digit
guard but this OLDER percentage-path `TERM_RE` has no equivalent guard — see also CANNOT-SEE #9b
below).

*(Additional note on claim #9's own code, not a separate testable claim — no independent
BITES status, folded into claim #9's row above.)* `TERM_RE = r"\b%s\b\D{0,4}(\d+)"` — unlike `ABS_TERM_RE`
(line 793, hardened post-#58 to require the digit group start with a digit), the percentage-path
regex still uses a plain `(\d+)` group. CANNOT-SEE: a bare non-digit run between the term word
and up to 4 non-digit chars could still, in principle, mis-parse in the same class of way #58
found on the absolute path — this legacy path was never re-hardened after that fix because it
is being phased out (per claim #8's dormancy finding), but it remains the LIVE fallback for any
stamp not yet in the new form.

**10. No total stated (percentage, `= N%`) → FAIL** (lines 966–967).
BITES: UNCOVERED. No entry in `PREFLIGHT_FIXTURES` (2572–2607) omits the `= N%` clause; all
have some `= NN% BAND`.
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE: n/a — untested, not a design gap.

**11. No band named (percentage) → FAIL** (lines 968–970).
BITES: UNCOVERED. Same reason — every fixture that reaches this far already carries a band word.
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE: n/a — untested.

**12. Arithmetic does not close (percentage) → FAIL** (lines 972–977).
BITES: PROVEN-BY-SELFTEST (`PREFLIGHT_FIXTURES[2]`, "arithmetic does not close").
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE: 1-point rounding slack (line 974, `abs(total - summed) > 1`) is hard-coded; cannot
tell genuine rounding from a stamp that is off by exactly 1 point for a different reason.

**13. Band mis-read vs `band_for()` table (percentage) → FAIL** (lines 978–982).
BITES: PROVEN-BY-SELFTEST (`PREFLIGHT_FIXTURES[3]` "band mis-read (70 called AMBER)" and `[4]`
"band mis-read at the boundary (60 is RED)").
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE: reads `band_for()` at call time, so it cannot detect drift if `BANDS` itself is
edited to something Dave never ruled — it only checks internal consistency between the stamp
and whatever `BANDS` currently says.

**14. ds-023: total < `BAND_FLOOR`(45) → NOTE, allowed but flagged as possible under-pricing**
(lines 990–999; `BAND_FLOOR` defined line 135).
BITES: PROVEN-BY-SELFTEST (`PREFLIGHT_FIXTURES` "below the band (44)" ×2, plus the dedicated
under-pricing bite at lines 2769–2779 checking the NOTE text itself, not just presence).
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE: cannot distinguish genuine thrift from chronic under-pricing habit — it is a NOTE
every time, with no memory of how many prior wraps also landed under 45.

**15. ds-023: 45 ≤ total ≤ 60 → NOTE, "IN the preferred band"** (lines 1000–1006).
BITES: PROVEN-BY-SELFTEST ("57 IN the band, UNMARKED — passes" + inline `in_band_marked` test,
lines 2751–2761, which ALSO proves a marker on an in-band stamp does NOT produce a receipt —
the #36 anti-habit defect specifically).
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE: n/a for this branch — well covered both ways (fires / stays silent).

**16. ds-023: 61 ≤ total ≤ 63 (`MARKED_MAX`), marked → WARN** (lines 1007–1015).
BITES: PROVEN-BY-SELFTEST ("62 over the line but MARKED — allowed, warns" + boundary loop
lines 2820–2833, cases `(61,True,False)` and `(63,True,False)`).
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE: `RESERVE_SPEND_RE` only checks the MARKER string is present anywhere on the line —
cannot verify the marked overrun was genuinely forked to Dave (vs. copy-pasted out of habit;
the docstring itself names this residual risk at line 1012–1013).

**17. ds-023: 61–63 unmarked → FAIL** (lines 1016–1024).
BITES: PROVEN-BY-SELFTEST ("62 over the line, UNMARKED — must FAIL" + boundary loop
`(61,False,True)`, `(63,False,True)`).
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE: n/a.

**18. ds-023: total > 63 (beyond `MARKED_MAX`), marked → WARN with "UNRULED" hatch note**
(lines 1025–1038).
BITES: **UNCOVERED.** No fixture in `PREFLIGHT_FIXTURES` supplies a >63% stamp WITH the
`RESERVE SPEND — forked to Dave` marker; the only >63 fixture ("70 beyond the marked tolerance,
UNMARKED — must FAIL") and the boundary loop's `(64, False, True)` entry are both unmarked. The
"marked-and-beyond-63 passes as WARN, not FAIL" branch has never been exercised.
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE: n/a — untested, not a design gap (the branch's logic mirrors claim #16's, so a
regression here would likely also show in #16, but that is an inference, not a bite).

**19. ds-023: total > 63, unmarked → FAIL with "UNRULED" hatch note** (lines 1039–1043).
BITES: PROVEN-BY-SELFTEST ("70 beyond the marked tolerance, UNMARKED — must FAIL" + the inline
UNRULED-text assertion at lines 2814–2819 + boundary loop `(64,False,True)`).
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE: the ">63 is UNRULED" gap is DECLARED, not closed — by design (see file header
comment ~l.128-131); this is intentional, not a defect.

**20. Wrap term below `WRAP_FLOOR`(5) → WARN** (lines 1045–1047).
BITES: UNCOVERED. Every `PREFLIGHT_FIXTURES` entry uses `wrap 5%` or higher; none go below 5.
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE: n/a — untested.

**21. No ring-fenced reserve mentioned → WARN** (lines 1048–1050).
BITES: UNCOVERED (as an isolated bite). Every fixture includes a `reserve NN%` clause; the one
fixture testing the ADJACENT rule (reserve must not be summed into total, lines 2715–2720) still
includes a reserve mention — no fixture omits `reserve` entirely, so this WARN's OWN trigger
condition (`not RESERVE_RE.search(line)`) is never hit.
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE: n/a — untested.

---

## G2 — pre-flight stamp: #56 ABSOLUTE/REAL-TOKENS form (`check_preflight_tokens`, 813–924)
Runs at: **wrap only**, reached exclusively via claim #8's dispatch; also directly callable
(and is, in `selftest_preflight_tokens`, bypassing the dispatch by calling `check_preflight`
which re-dispatches — so in practice it is never called with a non-matching line in this repo).

**22. Missing 1+ of boot/job/wrap AND not declared `unobservable(...)` → FAIL** (lines 835–842).
BITES: PROVEN-BY-SELFTEST ("D10 (c): the SAME term silently absent FAILS", l.2634–2635) —
paired with claim #23's positive control (declared-unobservable passes).
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE: `UNOBSERVABLE_RE` only requires the word "unobservable" followed by a parenthetical
of ≥3 chars anywhere tied loosely (`\D{0,60}`) to the term name — the REASON inside the
parens is never validated for honesty, only for existing.

**23. A term declared `unobservable (<reason>)` → passes (not a fail)** (lines 830–834, 835).
BITES: PROVEN-BY-SELFTEST ("D10 (c): a DECLARED-unobservable term passes", l.2631–2633).
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE: same as #22 — the reason string is unvalidated prose.

**24. No `= N of N` total clause → FAIL, early return** (lines 844–848).
BITES: **UNCOVERED.** Structurally very hard to reach via the normal call path: `check_preflight`
only calls `check_preflight_tokens` when `ABS_TOTAL_RE.search(line)` already matched (line 950),
and `check_preflight_tokens` re-runs the identical regex at line 844 — so by the time this
function is entered through `check_preflight`, the match is guaranteed and this FAIL is
DEAD CODE on that path. It is reachable only by calling `check_preflight_tokens(line, ...)`
directly with a line that was never validated by the caller, which no code in this file
(selftest or otherwise) does.
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE (structural): this is a defensive branch guarding against a caller contract that the
one real caller in this file already enforces — its own docstring doesn't note the redundancy.

**25. `budget != gauge.BUDGET_WORKING` → FAIL** (lines 850–854).
BITES: PROVEN-BY-SELFTEST ("a stamp priced against a budget nobody ruled FAILS", stamp `of
500,000`).
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE: reads `gauge.BUDGET_WORKING` live from the imported `_gauge_tokens` module — cannot
detect if THAT module's constant itself was silently re-dialled (a companion pin exists at
lines 2681–2686 checking `_gauge_tokens`'s three constants, which IS asserted in selftest).

**26. Arithmetic doesn't close (`boot+job+wrap != total`, tolerance `max(1000, summed//100)`)
→ FAIL** (lines 856–861).
BITES: PROVEN-BY-SELFTEST ("arithmetic that does not close FAILS").
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE: tolerance is itself a % of the summed value or a flat 1000, whichever is larger —
a stamp whose error is deliberately kept just under that tolerance would still pass; the check
cannot see intentional rounding abuse, only gross mismatch.

**27. No band word stated → FAIL** (lines 863–866).
BITES: UNCOVERED. Every `PREFLIGHT_TOKEN_FIXTURES` entry carries a band word.
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE: n/a — untested.

**28. Band mis-read vs `gauge.band_for(total)` → FAIL** (lines 867–872).
BITES: PROVEN-BY-SELFTEST ("band mis-read against the ruled thresholds FAILS",
`_ABS_OK.replace("GREEN","AMBER")`).
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE: same class as #13 — checks internal consistency against `gauge.band_for`, not
against an independently-verified truth.

**29. `total > gauge.BUDGET_HARD`(256,000) → FAIL always, marked or not** (lines 874–886).
BITES: PROVEN-BY-SELFTEST ("past the HARD line — FAILS EVEN WHEN MARKED").
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE: n/a — the asymmetry (marker cannot buy past HARD) is itself asserted and proven.

**30. `total > BUDGET_WORKING`, marked → WARN** (lines 887–893).
BITES: PROVEN-BY-SELFTEST ("over the working budget, MARKED — allowed, warns").
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE: same marker-honesty gap as claim #16.

**31. `total > BUDGET_WORKING`, unmarked → FAIL** (lines 894–901).
BITES: PROVEN-BY-SELFTEST ("over the working budget, UNMARKED — FAILS").
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE: n/a.

**32. `total < gauge.BUDGET_AMBER` → NOTE, "comfortable / check for under-pricing"**
(lines 902–907).
BITES: PROVEN-BY-SELFTEST (control fixture `_ABS_OK`, total 91,897 < 160,000 AMBER, is the
"control — priced, in budget..." case, l.2618).
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE: same under-pricing-cannot-be-distinguished-from-thrift gap as claim #14.

**33. Otherwise (`BUDGET_AMBER ≤ total ≤ BUDGET_WORKING`) → NOTE, "inside working budget"**
(lines 908–913).
BITES: PROVEN-BY-SELFTEST ("AMBER stated correctly passes", total 176,897).
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE: n/a.

**34. Position/U-shape recall note — published on EVERY path unconditionally** (lines 915–923).
BITES: PROVEN-BY-SELFTEST (explicit assertion at lines 2690–2695: "the position note did not
publish... recall is weakest in the MIDDLE").
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE: this is advisory prose only; nothing enforces that a session actually acts on it.

---

## G3 — `check_budgets` — structural section checks (1470–1508, 1519–1546)
Runs at: **wrap only** (line 2444); **SKIPPED under `--wrap --lane`** (lines 2428–2432).

**35. `GOOD-MORNING.md` file missing → FAIL, early return** (lines 1474–1475).
BITES: **UNCOVERED.** Every `check_budgets(td)` call site in the selftest suite (lines 2990,
3037, 3052, 3062, and the growth/M8/M10 fixtures) writes a `GOOD-MORNING.md` first. No fixture
calls `check_budgets` against a repo where the file is absent.
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE: n/a — untested, trivial guard.

**36. Required section marker(s) not found (`SECTION_REQUIRED`) → FAIL, early return**
(lines 1481–1484).
BITES: PROVEN-BY-SELFTEST (`BUDGET_FIXTURES` "required marker missing", `drop=("§C",)`).
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE: only checks the FOUR named markers (`DO-FIRST`,`§A`,`§B`,`§C`) exist somewhere in
the file by regex match on the line's start — cannot see if a marker is duplicated, or if the
markers are present but in an order the rest of the file's slicing logic cannot handle (see
claim #47 below, the §A/DO-FIRST order guard).

**37. `SECTION_RETIRED` (§B) present → FAIL** (lines 1485–1487).
BITES: PROVEN-BY-SELFTEST ("§B present (D4 deleted it)", `with_b=True`).
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE: matches only the literal `§B` heading regex — a retired section's content pasted
back in WITHOUT its own heading marker would not be caught by this specific check.

**38. 2f strata: `live_blocks > STRATA_MAX_BLOCKS`(1) → FAIL** (lines 1505–1508).
BITES: PROVEN-BY-SELFTEST ("strata stack 2 blocks deep (D5: LATEST only)" + "strata: 3 exempt
+ 2 live blocks — must FAIL"), and MUTATION-TESTED independently in `selftest_strata_exempt`
(lines 3012–3066: removes `#42` from `STRATA_EXEMPT`, asserts the SAME 4-block fixture flips
from green to red, then restores and asserts green again — genuine mutation coverage, not just
a pass/fail pin).
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE: counts BLOCKS, not their CONTENT — a block that is present but empty, or one whose
`#### <date> #<N>` key is malformed in a way `_key_session` still parses a number from, still
counts toward the cap.

**39. 2f strata: "fail loud on a fourth newly-unrollable block" cross-check against
`notes/_GAUGE-LOG.md` keys → FAIL** (lines 1509–1530, `_gauge_log_session_keys` at 1450–1467).
BITES: **UNCOVERED — confirmed by direct search.** Every `check_budgets(td)` fixture call in the
selftest suite writes ONLY `GOOD-MORNING.md` into its temp dir; none also create a matching
`notes/_GAUGE-LOG.md` with a pre-existing key that collides with a live (non-exempt) strata
block. Since `_gauge_log_session_keys` returns `None` when the file is absent (line 1462–1463)
and `check_budgets` then SKIPS the cross-check silently (line 1520: `if gauge_log_keys is not
None:`), this entire branch has never fired in any selftest run to date. This is the single
largest coverage gap found in this pass — the exact mechanism Dave ruled at #58 ("fail loud and
come back to me" on a fourth unrollable block) has no test proving it actually fires.
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE: even if tested, this check can only see a NAME collision (a session number appearing
both as a live strata key and as an already-keyed `_GAUGE-LOG.md` entry) — it cannot see whether
`roll_2f`'s duplicate-key guard (in the separate `_gm_move.py`, not this file) would actually
refuse it; it infers that refusal from the shared key format rather than invoking the mover.

**40. Section line cap: block threshold exceeded (DO-FIRST ≥180, §C ≥225) → FAIL**
(lines 1543–1544).
BITES: PROVEN-BY-SELFTEST ("DO-FIRST over block (266 ln...)" + "§C over block (260)").
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE: n/a for the block path.

**41. Section line cap: WARN threshold exceeded but under block (DO-FIRST 120–179, §C 150–224)
→ WARN** (lines 1545–1546).
BITES: **UNCOVERED — confirmed by direct search.** `BUDGET_FIXTURES` contains only block-level
values (266, 260) and a green control (default 10 lines); no fixture lands in the WARN band for
either section. The WARN branch of the two-tier cap (the half that fires BEFORE the hard block)
has never been exercised.
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE: n/a — untested.

---

## G4 — `check_budgets` — TITLE THE NEXT CHAT stamp, #60-D8 (1548–1567)
Runs at: **wrap only**, same call as above.

**42. No `TITLE THE NEXT CHAT` line found in header → FAIL** (lines 1550–1555).
BITES: **UNCOVERED — and the file's OWN comment is misleading about this.** `_gm_fixture`
defines a `title=True` default parameter (line 2844) and a large comment block (lines
2861–2870) explicitly states *"`title=False` is how the ABSENT-title path is bitten
deliberately"* — but a full-file search confirms `title=False` is never actually passed at any
`_gm_fixture(...)` call site in the whole suite (every call omits the `title` kwarg and gets the
default `True`). **This is a claim of coverage in the comment that the code does not deliver —
worth flagging on its own, independent of the underlying FAIL branch being untested.**
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE: n/a for the check itself — the finding here is about the test suite's own
documentation accuracy, not the gate's blind spot.

**43. `TITLE THE NEXT CHAT` line measures over `TITLE_CAP_TAPE`(120 tape) → FAIL**
(lines 1558–1564).
BITES: **UNCOVERED.** No fixture constructs an oversized title line; every fixture's title
(line 2873) is the short fixed string `"Apollo - #N fixture (read _CHAIN.md ONLY)"`, well under
120 tape.
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE: measured in `tape` via `measure_tokens`, so on a degraded (ESTIMATE) measurement
run the cap is checked against an estimate rather than a real token count, with no separate
flag raised for that degradation on this specific check (see G20 below).

---

## G5 — `check_budgets` — size stamp / ds-021 units / open 15 / open 25 (1569–1670)
Runs at: **wrap only**.

**44. No `size:` stamp found in header → FAIL** (lines 1599–1601).
BITES: PROVEN-BY-SELFTEST ("no size stamp", `stamp="(no stamp here)"`).
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE: n/a.

**45. `size:` stamp still spells the unit `tk` (legacy) → WARN** (lines 1605–1610).
BITES: PROVEN-BY-SELFTEST (`selftest_units`, bite 2, lines 3480–3494: a `tk`-spelled stamp
must warn AND must still parse).
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE: `LEGACY_UNIT_RE` only recognises the exact `\d[\d.]*\s*K\s*tk\b` shape — a
differently-misspelled legacy unit would not be caught by this specific warn (though it might
trip claim #46's "no GM figure" FAIL instead, depending on shape).

**46. `size:` stamp carries no parseable GM figure (`SIZE_TK_RE` no match) → FAIL**
(lines 1611–1613).
BITES: PROVEN-BY-SELFTEST ("size stamp with no K (25618 must not read as 25.6M)").
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE: deliberately requires the `K` suffix (comment at 428–429) — a raw `25618 tk` figure
is caught here specifically because it lacks `K`, but per the file's own admission this is a
narrow, declared scope, not a general "no number" detector.

**47. `size:` stamp's claimed GM figure drifts from measured tk by more than `SIZE_TOLERANCE`
(10%) → FAIL** (lines 1615–1618).
BITES: PROVEN-BY-SELFTEST ("size stamp STALE (claims 0.10K)").
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE: 10% tolerance is a flat constant; a stamp that is stale by exactly 9% would pass
clean.

**48. open 15: `CHAIN_STAMP_RE` finds ANY hand-written chain figure in the `size:` stamp →
FAIL, unconditionally on PRESENCE (not drift)** (lines 1620–1647).
BITES: PROVEN-BY-SELFTEST — this is one of the most heavily bitten checks in the file:
positive control (an ordinary stamp must NOT trip it, `selftest_growth` ~3686–3689), three
REAL historical hand-copy forms taken from `git log` (`"chain **4.4K tape**"`, `"chain 3.56K
tape"`, `"chain 34.7K tk"`, lines 3692–3703), and a dedicated SCOPE control proving the ban
does NOT escape into body prose (the GM:488 stratum record, lines 3704–3717).
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE (matches the brief's flagged item, quoted from the file's own header comment at
lines 458–468): **`CHAIN_STAMP_RE` requires the `K` suffix** (`([\d.]+)\s*K\s*(tape|tk)`) — a
hand-written chain figure with no `K` (e.g. a bare `4917 tape`) would not match this regex and
would pass silently. The file's own comment names this as inherited from "open 23" scope, not
a new hole. Scoped DELIBERATELY to the `size:` stamp only (line 458–461) — a chain figure
appearing in dated stratum prose elsewhere (a true historical record) correctly passes, by
design, because the regex is applied only to `stamp.group(1)`, not the whole file.

**49. open 25: `BARE_TOKEN_RE` finds a figure in the stamp with no accepted unit word beside
it → WARN** (lines 1649–1670).
BITES: PROVEN-BY-SELFTEST — six-part bite in `selftest_bare_token` (3081–3196): positive
control (ordinary stamp stays quiet), the two REAL forms live in GM's stamp at build time
(`§A **4.2K (EXEMPT)**`, `corpus **58.7K**`), a scope control (bare figure in banner PROSE must
NOT warn), a use/mention self-bite control (the gate's own warn TEXT, fed back through the
regex, is asserted to still contain a matchable figure — proving safety comes from SCOPE not
message-laundering), full unit-word coverage (every entry in `BARE_TOKEN_UNITS` suppresses),
and the `K`-required narrowing pinned as a declared scope limit (a bare `4,917` with no `K`
does NOT warn, asserted deliberately).
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE: same `K`-required narrowing as claim #48 (open 23's declared, inherited scope) — a
bare count with no `K` and no unit word (e.g. `4,917`) is invisible to this check by design.

---

## G6 — `check_budgets` — compactable region / M8 banner budget (1672–1732)
Runs at: **wrap only**.

**50. Compactable region ≥ BLOCK (bill) → FAIL** (lines 1702–1704).
BITES: **UNCOVERED — structurally dead code under the current constant.**
`SIZE_BUDGET_TK = {"compactable": 8000, "compactable_block": None}` (line 358) — `block_tk` is
always `None` (block WITHDRAWN #39), so execution always takes the `if block_tk is None:`
ADVISORY branch (1683–1697); the `else:` branch containing this FAIL (1698–1704) cannot execute
under the current constant, and `selftest_budgets` (line 3004) actively PINS the constant that
keeps it unreachable — no monkeypatch anywhere temporarily re-arms it to prove the FAIL logic
itself is sound.
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE (structural): if this branch is ever re-armed by changing `compactable_block` from
`None` to a number (Dave's call, per the header comment), it will go live UNTESTED — nothing in
the current suite proves the fail message or its arithmetic (`compact_bill >= block_bill`) is
correct, only that the ADVISORY branch works.

**51. Compactable region > WARN (bill), block withdrawn → WARN (advisory only)**
(lines 1693–1697).
BITES: PROVEN-BY-SELFTEST ("compactable over size WARN, block withdrawn #39 — advisory, must
NOT fail", `sec_c=5, fat_c=80`).
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE: n/a for this branch.

**52. M8: §A precedes DO-FIRST → banner region cannot be isolated → FAIL**
(lines 1713–1717).
BITES: **UNCOVERED — confirmed by direct search.** `_gm_fixture` always emits `DO-FIRST` before
`§A` in fixed order and has no parameter to reorder them; `DO-FIRST` is itself in
`SECTION_REQUIRED` (line 176), so a fixture that dropped it would trip the earlier "marker not
found" FAIL (claim #36) rather than reaching this one. No fixture anywhere constructs a
reordered file.
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE: n/a — untested; also worth noting the check's own docstring (lines 1710-1712)
frames this as fail-loud-on-reorder rather than a routine drift condition, so its low priority
for a fixture may be a deliberate choice rather than an oversight — still UNCOVERED as stated.

**53. M8: banner region (file top → DO-FIRST) ≥ block (bill) → FAIL** (lines 1727–1729).
BITES: PROVEN-BY-SELFTEST (`selftest_growth`, "M8: a 30-fat-line banner did not BLOCK",
line 3607–3609, with the 240-tk/line FAT constant MEASURED, not guessed — line 3601–3603 notes
an earlier guess put the fixture in the wrong band).
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE: the cap itself is DERIVED (`banner_budget_tk`, lines 584–605) from an archived
banner sample; if `_GM-ARCHIVE.md` is absent/undersized the FALLBACK constant is used instead
(claim #55 below) — this FAIL branch does not distinguish which provenance produced the
threshold it just tripped, though the accompanying NOTE (line 1724–1726) does publish it.

**54. M8: banner region > warn (bill) → WARN** (lines 1730–1732).
BITES: PROVEN-BY-SELFTEST ("M8: a 17-fat-line banner did not WARN", plus a positive control
that an ordinary banner must NOT warn, line 3610–3612).
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE: same as #53.

**55. M8 cap provenance: FALLBACK vs DERIVED declaration (`banner_budget_tk`, 584–605)** —
not itself a FAIL/WARN, but a declared-state the caps above depend on.
BITES: PROVEN-BY-SELFTEST — MUTATION-TESTED both ways (`selftest_growth`, lines 3614–3632): the
fixture repo has no archive so the FALLBACK path must fire and say so explicitly (line 3618),
then an archive of `BANNER_ARCHIVE_MIN_N + 2` banners is written and the SAME call must switch
to DERIVED (line 3626–3629), and block ≥ warn is asserted (line 3630–3631).
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE: `_banner_unit_samples` (565–581) trusts the archive's own banner-split regex to
correctly delimit each historical banner; a malformed archive that still parses as SOME split
(just the wrong one) would silently corrupt the derived median/p75 without being flagged as
wrong — only total absence or under-`BANNER_ARCHIVE_MIN_N` count is caught.

---

## G7 — `check_budgets` — M10 read-chain / corpus budget (1734–1770)
Runs at: **wrap only**.

**56. M10: `chain_file` unmeasured (refusal propagated from `chain_file_tk`) → WARN**
(lines 1745–1748).
BITES: PROVEN-BY-SELFTEST (`selftest_growth`, "THE REFUSAL PATH", lines 3748–3753: no ★ LATEST
banner ⇒ UNMEASURED and said so, never 0/green).
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE: this WARN reports the refusal but does not distinguish WHICH of `chain_file_tk`'s
three internal refusal reasons (import failure / `build()` raising / not-generatable, lines
1309–1317) produced it beyond echoing the detail string — a caller reading only the WARN prefix
would not know without reading the full text.

**57. M10: `chain_file` (bill) > warn (`CHAIN_BUDGET_TK[0]`) → WARN, ADVISORY only**
(lines 1749–1756).
BITES: PROVEN-BY-SELFTEST — heavily bitten in `selftest_growth` (3637–3746): the POSITIVE bite
(measurement actually happens and reports a number, not just "did it warn"), the UNIT bite
(the published figure is the FILE, which must EXCEED the slice, not merely equal it — proving
the wrapper is actually counted), the tag-uniqueness control (chain vs corpus messages don't
collide on substring match), the re-point control (a fat §A/§C must NOT warn the chain post-#33
cut), the positive-region control (a fat BANNER, which IS in the chain, DOES warn it), a tier
control (chain finding must never reach FAILS — advisory by ruling), and a remedy-text control
(must not prescribe rolling deltas, the withdrawn #33 advice).
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE: numbers are AGENT-DERIVED and ADVISORY pending Dave (stated repeatedly in-file);
cannot see whether the 4,917/6,417 tape thresholds are still appropriate once the 417-tape
wrapper pin (`_gen_chain`'s BANNER+FOOTER) itself changes — the pin is a SNAPSHOT (line 656),
not a live re-measurement, so a real wrapper-size drift would silently make the published
threshold stale until someone re-measures it by hand.

**58a. M10 corpus (GM+LS whole) — the corpus figure is published in a NOTE on every run,
warned or not** (lines 1763–1770, the always-runs publish half).
BITES: PROVEN-BY-SELFTEST (`selftest_growth`, "the corpus figure is not published" control,
lines 3758–3761 — proves the NOTE always appears).
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE: n/a for this half.

**58b. M10 corpus (GM+LS whole) > `CORPUS_BUDGET_TK`(36,000) → WARN, never blocks**
(lines 1763–1767, the over-budget branch specifically).
BITES: UNCOVERED. No fixture drives the corpus figure OVER 36,000 tape — only that the NOTE is
always published (claim #58a) is asserted anywhere in the suite; the WARN branch's own trigger
condition is never hit.
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE: the corpus warn never blocks, by design (post-#33 it is retrieval surface, not
cold-start cost) — untested here, not a design gap.

---

## G8 — `check_budgets` — M7 §A growth trigger (1772–1793)
Runs at: **wrap only**.

**59. M7: §A grew vs. stamped baseline (beyond `STAMP_PRECISION_TK`) AND no banner names a §A
change → WARN** (lines 1784–1789).
BITES: PROVEN-BY-SELFTEST (`selftest_growth`, "growth: stamp claims less than §A measures... did
not warn", line 3772–3774) — AND the suppressor is independently proven (a banner line naming
§A silences the warn, line 3776–3780) — AND the "§A finding must never reach FAILS" tier
constraint is separately asserted (line 3767–3770) — AND the "§A baseline UNSET" declared-gap
path (no stamped figure at all) is proven too (line 3781–3785).
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE: the suppressor (`banner_names_a`, line 1784) only checks that the literal string
`§A` appears in a non-stamp line above DO-FIRST — ANY mention of `§A`, not necessarily one that
actually explains growth, silences the warn. A banner line saying "§A untouched this session"
would still suppress it (the check cannot distinguish a real change-note from an incidental
mention).

**60. M7: §A (bill) past `SECTION_A_WARN_TK`(4,500) backstop → WARN** (lines 1790–1793).
BITES: PROVEN-BY-SELFTEST (`selftest_growth`, "§A past the backstop did not warn", `fat_a=30`
≈6K tk, plus the tier constraint that it must never reach FAILS, line 3767–3770).
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE: n/a — well covered.

---

## G9 — `stop_line_consistency` (1823–1849), ds-023 presence assertion
Runs at: **wrap only** (line 2474), BLOCKING at birth (not advisory-first, per its own
docstring — a deliberate exception to this file's usual convention).

**61. ds-023 stop-line phrase missing from one or more of `STOP_LINE_HOMES` → FAIL**
(lines 1837–1845).
BITES: PROVEN-BY-SELFTEST, and genuinely MUTATION-TESTED (`selftest_gauge_continuity`,
lines 3241–3271): both homes stated → green + homes-count NOTE; the ruling edited OUT of one
home → must go red and NAME that file; and a USE/MENTION control — prose that QUOTES the WRONG
form in order to correct it (`"THIS LINE USED TO SAY..."`) — must still pass, because this is a
presence-shaped check (asserting the correct phrase exists), not a ban-shaped one.
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE: checks for the literal phrases `"60 − the priced wrap"` / `"60 is where the wrap
has FINISHED"` as exact substrings (line 1812-1820) — a paraphrase that preserves the RULING
but not the exact wording would FAIL this check even though it is not actually wrong; the
presence-not-ban design trades this false-positive risk for immunity to the USE/MENTION
problem it was built to dodge.

---

## G10 — `gauge_log_continuity` (1852–1933), ds-022 (a)
Runs at: **wrap only** (line 2470), BLOCKING.

**62. Cannot read this session's number from GM (banner unreadable, stratum fallback also
fails) → WARN "UNARMED"** (lines 1879–1884).
BITES: PROVEN-BY-SELFTEST (`selftest_gauge_continuity`, last block, lines 3340–3350: no session
number anywhere → must announce UNARMED, never pass quietly).
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE: n/a.

**63. Banner session # disagrees with §C stratum # (the #37 "self-hiding clock" defect) →
FAIL** (lines 1892–1902).
BITES: PROVEN-BY-SELFTEST — the exact historical numbers (banner #36 vs stratum #35) are
reproduced (lines 3287–3297), AND the positive/negative controls around it: banner is proven to
be the SOURCE over decoy prose mentioning "★ LATEST" (lines 3273–3285, the literal #37 bug
shape), and the fallback-when-no-banner path is separately proven still to work (lines
3299–3306) so the whole suite doesn't quietly stop testing the pre-#37 behaviour.
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE: only detects a NUMBER mismatch between two structurally-different sources; cannot
detect the case where BOTH happen to already agree by coincidence despite step 2f genuinely
having been skipped for an unrelated reason.

**64. Previous session (`cur-1`) marked ABSENT → WARN (not pass, not fail)**
(lines 1917–1922).
BITES: PROVEN-BY-SELFTEST (lines 3330–3339 — both halves: ABSENT must not FAIL, and must not
pass SILENTLY, i.e. the WARN text itself is asserted to contain "ABSENT").
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE: n/a.

**65. Previous session left NO block and NO hole/absent line → FAIL** (lines 1923–1932).
BITES: PROVEN-BY-SELFTEST (line 3308–3313, the #26/#28/#29 historical defect reproduced) — and
the DECLARED-HOLE escape hatch is separately proven both to pass AND to publish its acceptance
NON-silently (lines 3315–3325).
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE: cannot verify the HOLE/ABSENT declaration's stated REASON is true — by design (its
own docstring, lines 1863–1864: "Do not teach it to grade prose").

---

## G11 — `unkeyed_testimony` (1989–2068), ds-022 (d), gated shut by Dave #54
Runs at: **wrap only** (line 2477), tier-routed by `UNKEYED_BLOCKING`(True, line 1968) —
**BLOCKING by that flag's current value.**

**66. Testimony present in `_GAUGE-LOG.md` with no key / HOLE / ABSENT line → FAIL "PRESENT
BUT UNKEYED"** (lines 2035–2047).
BITES: PROVEN-BY-SELFTEST — the exact historical case (#40's testimony with its key removed,
lines 3388–3401) AND the positive control (keyed testimony must stay green + NOTE, lines
3376–3386) AND the anti-forgery control (the FAIL message must NOT invite a `HOLE #40` line,
because HOLE would be a false positive claim — lines 3397–3401) AND the escape-hatch control
(a DECLARED HOLE alongside the testimony must still pass, lines 3403–3411).
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE: cannot verify the testimony's CONTENT is honestly about the keyed session — only
that a key/declaration exists for every session number the file names (its own docstring says
so explicitly, lines 2000–2003).

**67. Unclassified bold-lead marker naming an unaccounted session (label not in
`TESTIMONY_LABELS`) → FAIL "UNCLASSIFIED MARKER"** (lines 2049–2059).
BITES: PROVEN-BY-SELFTEST — the substring-vs-structure discrimination control (prose ABOUT
session #41 must NOT be classified as #41 testifying, lines 3413–3423), the anti-blindness
control (a brand-new label `FROBNICATE` must still fail rather than pass silently, lines
3429–3438), and the cost control (the same marker type but about an ALREADY-ACCOUNTED session
must stay silent, lines 3440–3450, so the check is not noisy on a clean file).
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE: `TESTIMONY_LABELS` is a closed enumerated tuple (line 1979); a label added to the
vocabulary later requires a matching code edit — the check's own safety net (any unrecognised
label still fails loud) is what makes the enumeration safe, per its own comment (1974–1978),
but this means a GENUINELY new, valid label type will ALSO fail loud until someone updates the
tuple — a false positive by design, traded for never silently missing an unknown state.

**Note on `UNKEYED_BLOCKING` itself:** unlike its three sibling tier flags
(`SECTION_USAGE_BLOCKING`, `USAGE_HISTORY_BLOCKING`, `CONSULT_RECEIPT_BLOCKING`, each of which
has an explicit pinned-value assertion in a `selftest_*` function — lines 3923–3924, 3880,
3956–3957 respectively), **`UNKEYED_BLOCKING`'s current value (`True`) has NO corresponding
selftest pin anywhere in the file.** A silent flip of this flag to `False` would not be caught
by any assertion in the suite, unlike its three siblings. This is UNCOVERED as its own finding,
separate from claims #66/#67 (which test the underlying logic, not the tier flag's value).

---

## G12 — `retirement_receipts` (2080–2137), M9, BLOCKING (Dave #22)
Runs at: **wrap only** (line 2448 — note the function's own local variable is named `warns` but
the caller escalates its first return value straight into `fails`, line 2449 — BLOCKING despite
the internal naming).

**68. DO-FIRST line(s) vanished since HEAD with no matching text anywhere in
`_GM-ARCHIVE.md` → escalated to FAIL by the caller** (lines 2128–2132).
BITES: PROVEN-BY-SELFTEST (`selftest_growth`, its own git-repo fixture, lines 3801–3834): a
line removed with no archive text must warn; archiving it must silence the warn (proving it
isn't noise); and a pure REWRAP (re-flowing the same content across line boundaries) must
produce NO removals at all, proving the `_norm()` normalisation is doing its job rather than
being line-shaped.
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE: explicitly a PROXY, by its own docstring (2080–2092) — cannot see whether a move
was verbatim, or whether a retirement was actually DUE; it only sees that removed text is
findable somewhere in the archive file, character-sequence-wise, after normalisation.

---

## G13 — `section_usage_probe` (2140–2173), #23/#24
Runs at: **wrap only** (line 2451), tier-routed by `SECTION_USAGE_BLOCKING`(True) →
**currently escalated to FAIL.**

**69. `_gm_usage.validate_stratum` returns issues (missing/malformed usage or sizes line) →
tier-routed FAIL** (line 2166, routed at 2451–2452).
BITES: PROVEN-BY-SELFTEST (`selftest_usage`, lines 3905–3928: good stratum stays quiet;
missing line fires; malformed line fires AND says "MALFORMED"; plus the tier-pin assertion that
`SECTION_USAGE_BLOCKING` is still `True`).
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE: FORM-checked only, explicitly by design (its own docstring, "honesty stays the
session's") — cannot verify the U/R/C testimony is truthful, only that it is well-formed.

---

## G14 — `index_freshness_check` (2176–2231), #32
Runs at: **wrap only** (line 2460), always BLOCKING (not tier-routed).

**70. `_build_memento_index` unimportable → FAIL** (lines 2200–2202).
BITES: UNCOVERED directly (no selftest breaks the import itself), but the function's other
four paths are all bitten (see below) — this specific import-guard branch is UNCOVERED.

MUTATION-RED: NOT-ASKED-THIS-PASS.
**71. `build_records()` raises an exception → FAIL** (lines 2205–2208).
BITES: UNCOVERED directly — `selftest_index_freshness` monkeypatches `build_records` to return
`([], [errors])` (a controlled refusal, claim #73) but never makes it raise an exception outright.

MUTATION-RED: NOT-ASKED-THIS-PASS.
**72. Corpus REFUSES to index (errors list non-empty) → FAIL, names offending source**
(lines 2210–2214).
BITES: PROVEN-BY-SELFTEST ("corpus REFUSAL fails and names the offending source (the #30
case)", line 4032–4033).

MUTATION-RED: NOT-ASKED-THIS-PASS.
**73. Index file `bmi.OUT_PATH` absent on disk → FAIL** (lines 2216–2218).
BITES: PROVEN-BY-SELFTEST ("ABSENT index fails", line 4025–4027).

MUTATION-RED: NOT-ASKED-THIS-PASS.
**74. Rendered records don't byte-match what's on disk → FAIL "STALE"** (lines 2222–2227).
BITES: PROVEN-BY-SELFTEST ("STALE index fails — the #32 defect itself", line 4020–4024) —
paired with the load-bearing POSITIVE control (a genuinely fresh index passes AND says "FRESH"
in its notes, line 4018–4019, so a revert that deletes the whole comparison couldn't pass
silently).
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE (for the whole function): deliberately NOT an mtime check (docstring, lines
2193–2195) — content-only, by design, to avoid the DV-D17 revert-reads-green shape. Cannot see
whether the freshly-rebuilt index MATCHES the intended retrieval semantics, only that it
byte-matches its own deterministic renderer's output.

---

## G15 — `usage_history_probe` (2244–2292), #35
Runs at: **wrap only** (line 2454), tier-routed by `USAGE_HISTORY_BLOCKING`(False) →
**currently WARN only.**

**75. `_gm_usage` unimportable → tier-routed issue (currently WARN)** (lines 2265–2267).
BITES: UNCOVERED. No selftest breaks this specific import.

MUTATION-RED: NOT-ASKED-THIS-PASS.
**76. `history_report` returns refusals → tier-routed issue (currently WARN)**
(lines 2270–2271).
BITES: UNCOVERED. No selftest drives `history_report` to a refusal state.

MUTATION-RED: NOT-ASKED-THIS-PASS.
**77. Deferral candidates found (never-cited + long-unread sections) → NOTE only, published,
never enforced** (lines 2280–2286) — not itself a refusal/fail.
BITES: UNCOVERED as a positive case — no selftest constructs a fixture with a genuine
never-cited streak to prove this NOTE fires with real candidate names; `selftest_usage`
(3905–3928) tests the SIBLING function `section_usage_probe`, not this one, and there is no
`selftest_history` equivalent for `usage_history_probe`'s own body logic — only the TIER PIN
(`USAGE_HISTORY_BLOCKING == False`, asserted at line 3880 inside `selftest_units`) is checked.
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE: explicitly publishes only, never prescribes remedy (its own docstring) — OFFLOAD
/TRIM/KEEP is Dave's, never this gate's.

---

## G16 — `consult_receipt_probe` (2295–2338), #25, the KG forcing function
Runs at: **wrap only** (line 2457), tier-routed by `CONSULT_RECEIPT_BLOCKING`(False) →
**currently WARN only.**

**78. `_search_core` unimportable → tier-routed issue (currently WARN)** (lines 2316–2318).
BITES: UNCOVERED. No selftest breaks this import.

MUTATION-RED: NOT-ASKED-THIS-PASS.
**79. Stratum carries NO `consult-receipts` line → tier-routed issue (currently WARN)**
(lines 2325–2328).
BITES: PROVEN-BY-SELFTEST (`selftest_receipts`, "missing stratum line did not raise — probe
dead" check, lines 3975–3977) — plus the positive control (a well-formed honest-negative
`none — <why>` must raise NOTHING, lines 3978–3982) and the tier pin
(`CONSULT_RECEIPT_BLOCKING == False`, lines 3956–3957).

MUTATION-RED: NOT-ASKED-THIS-PASS.
**80. Malformed receipt payload (e.g. empty ids after `→`) → tier-routed issue (currently
WARN)** (lines 2329–2331).
BITES: PROVEN-BY-SELFTEST (`selftest_receipts`, "malformed payload (empty ids) passed — bite
dead" check, lines 3983–3987) — plus a direct unit-level control on `_search_core
.validate_receipt_payload` itself (known-good payload must not be refused; bare `none` alone,
with no reason, must be refused — lines 3965–3969).
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE (both #79/#80): FORM-checked only, explicitly (docstring, "whether the queries were
run stays the session's honesty").

---

## G17 — `lane_routing_check` (2341–2366), O1′ #24
Runs at: **wrap only** (line 2463), always BLOCKING.

**81. `_gen_lanes` unimportable → FAIL** (lines 2354–2356).
BITES: UNCOVERED directly (`selftest_lanes`, lines 3931–3950, imports `_gen_lanes` successfully
and tests its OWN `check_routing_line` function's behaviour, not the import-failure branch of
`lane_routing_check` itself).

MUTATION-RED: NOT-ASKED-THIS-PASS.
**82. Lane records invalid (`_gen_lanes.load_lanes()` returns errors) → FAIL**
(lines 2358–2359).
BITES: UNCOVERED directly at the `lane_routing_check` level (the selftest instead constructs a
fixture lane list and calls `check_routing_line` directly, bypassing `load_lanes()` entirely).

MUTATION-RED: NOT-ASKED-THIS-PASS.
**83. GM eager ROUTING line disagrees with `knowledge/_lanes.json` records → FAIL**
(lines 2360–2362, delegated to `_gen_lanes.check_routing_line`).
BITES: PROVEN-BY-SELFTEST (`selftest_lanes`: good fixture stays quiet; missing routing line
fires; state drift — ACTIVE vs BLOCKED — fires) — but note this proves `_gen_lanes
.check_routing_line`'s OWN logic, called directly; the selftest's own docstring (lines
3932–3934) is candid that it "proves the gate's import path" only, and that "the deep refusal
bites live in `_gen_lanes.py --selftest` (its own build step)" — a SEPARATE file/build step not
audited in this pass.
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE: relies entirely on `_gen_lanes.py` as the one true implementation (deliberately, to
avoid the mover≠gate drift class) — a defect in `_gen_lanes.py`'s own logic would not be caught
by anything in `_capture_gate.py`'s own suite; that module's own `--selftest` is out of this
scan's scope (per the brief: this pass covers `_capture_gate.py` only).

---

## G18 — `dofirst_index_present_check` (2369–2414), #61
Runs at: **wrap only** (line 2466), always BLOCKING.

**84. Presence index could not be built at all (delegated refusal from `dofirst_index`) →
FAIL** (lines 2396–2398).
BITES: UNCOVERED directly at this function's level. `dofirst_index`'s OWN four internal refusal
paths (see G20, claims #90–93) are not separately driven through THIS wrapper function in any
selftest — the selftest suite tests `dofirst_index` refusals via `chain_parts`'s embedding
behaviour (claim shows up as a loud in-chain line, not a FAIL here) rather than via this
specific consumer function.

MUTATION-RED: NOT-ASKED-THIS-PASS.
**85. One or more open DO-FIRST items in GM are not individually named (by their number
token) in the on-disk `_CHAIN.md` → FAIL, names the missing item numbers** (lines 2404–2410).
BITES: UNCOVERED. No selftest fixture constructs a `GOOD-MORNING.md` + stale/incomplete
`_CHAIN.md` pair to drive this specific mismatch — this function is not called at all from any
`selftest_*` function; it is reachable only via the live `run()`/`wrap_checks` path against the
REAL repo's files (line 2466), which this Phase-1 pass explicitly did not exercise since doing
so would require running `--wrap` against the live repo, outside the selftest sandbox.
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE: per its own docstring (2383–2387), asserts PRESENCE only, not staleness — a chain
regenerated and verified in the same breath (the `_build_all.py:184-186` pattern named in the
docstring) proves only the generator is deterministic, not that the chain is actually current.

---

## G19 — `wrap_checks` direct checks: dates + git (2493–2513)
Runs at: **wrap only**, both lane and non-lane (the `targets` list just has fewer entries under
`--lane`, line 2421–2422).

**86. `_LIVE-STATE.md` or `GOOD-MORNING.md` missing → FAIL** (lines 2495–2497).
BITES: PROVEN-BY-SELFTEST indirectly — the S-D2 lane-flag bite test (lines 4068–4079) writes
BOTH files (with a stale date) rather than omitting either, so it proves the DATE check (claim
#87) but not the FILE-MISSING branch specifically. UNCOVERED for the missing-file branch itself.

MUTATION-RED: NOT-ASKED-THIS-PASS.
**87. Neither file's header carries today's ISO date within the first 40 lines → FAIL**
(lines 2500–2502).
BITES: PROVEN-BY-SELFTEST (lines 4068–4079: a plain wrap on a stale-dated GM must FAIL with
"GOOD-MORNING" in the message; the SAME repo run with `--lane` must NOT fail on this, since the
lane branch only checks `_LIVE-STATE.md`, per the `targets = targets[:1]` truncation at line
2422) — this ALSO proves claim #88 below (the lane skip itself).

MUTATION-RED: NOT-ASKED-THIS-PASS.
**88. `--lane` skips the GOOD-MORNING header check specifically (but not `_LIVE-STATE`'s)**
(control-flow, lines 2421–2435) — a scope-of-application claim, not a FAIL/WARN itself.
BITES: PROVEN-BY-SELFTEST (same fixture as #87, plus an explicit assertion that the skip is
NOTED, not silent — line 4080–4081: "`--lane` skip is silent — must be noted in output").

MUTATION-RED: NOT-ASKED-THIS-PASS.
**89. `git status --porcelain` reports uncommitted paths → WARN, count only**
(lines 2503–2508).
BITES: **UNCOVERED.** No selftest fixture drives an uncommitted-paths state and asserts the
WARN text; the M9 fixture (G12 above) DOES create and commit a git repo but never leaves
uncommitted changes at the point `wrap_checks` itself would be invoked against it — this
specific WARN's own trigger is never exercised end-to-end in the suite (only `git status`
itself, called elsewhere for other purposes, e.g. this very Phase-1 pass's own verification
runs, is exercised outside the gate).
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE: counts LINES of `git status --porcelain` output as a proxy for "uncommitted paths"
— cannot distinguish a single huge rename/move (many porcelain lines) from many small unrelated
edits; also silently WARNS (never fails) regardless of count, by design (advisory nudge only).

---

## G20 — measurement engine: refusals and degraded-state functions (1291–1408)
These are the low-level instruments `check_budgets` and others build on. None of these is
itself invoked as a top-level "check" with its own FAIL/WARN message class distinct from the
callers already enumerated above (G5–G8, G18) — they are the REFUSAL MECHANISM those callers
depend on. Listed separately per the brief's explicit instruction to include
`measure_tokens`/`measurement_degraded`.

**90. `measure_tokens()`: tiktoken import fails AND one-shot heal fails → falls back to
`bytes/BYTES_PER_TOKEN` ESTIMATE, always labelled `"...ESTIMATE (tiktoken absent)"`**
(lines 1350, 1363–1368).
BITES: PROVEN-BY-SELFTEST (`selftest_growth`, M6 bite, lines 3535–3554: forces `sys.modules
["tiktoken"] = None`, asserts the method string says ESTIMATE and names the absence, asserts a
positive token count is still returned, then restores and asserts the OBSERVED path resumes).
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE: this file's own callers (`check_budgets` etc.) read `measure_tokens(...)[0]` almost
everywhere and only occasionally surface `[1]` (the method) in a NOTE (e.g. line 1594, 1557) —
most callers never check whether they are silently operating on degraded (ESTIMATE) figures;
only the ONE explicit `measurement_degraded()` reader (which nothing in THIS file's live path
calls — see claim #92) is positioned to catch that centrally.

**91. `measure_tokens()`: `tiktoken.get_encoding("cl100k_base").encode()` itself raises (e.g.
cold-cache network fetch failure) even though import succeeded → also falls back to labelled
ESTIMATE, guarded separately from the import (#59)** (lines 1370–1374).
BITES: PROVEN-BY-SELFTEST (`selftest_growth`, lines 3576–3597: monkeypatches
`tiktoken.get_encoding` to raise, asserts fallback to ESTIMATE with a positive count, restores,
asserts return to OBSERVED).
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE: same as #90.

**92. `measurement_degraded()`: reports `True` iff the current process is running on the
ESTIMATE fallback (probes a 1-char string through the SAME code path)** (lines 1377–1395).
BITES: PROVEN-BY-SELFTEST (`selftest_growth`, lines 3556–3574: forces the degraded state, must
read True; restores, must read False) — but per this pass's own read of the file (confirmed by
a dedicated grep sub-agent), **this function is called ONLY from `selftest_growth`, nowhere in
the live `check_file`/`check_budgets`/`wrap_checks`/`run()` path.** Its docstring (1384–1394)
says it exists so `_gen_chain.py`'s `build()` can ask the question before measuring — i.e. it
is a UTILITY EXPORTED FOR AN EXTERNAL CONSUMER (`_gen_chain.py`, a different file, out of this
pass's scope), not something `_capture_gate.py` reads about itself.
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE (structural, worth flagging): `_capture_gate.py`'s OWN checks (the size/chain/banner
budgets in `check_budgets`) never call `measurement_degraded()` to gate their own verdicts — so
if tiktoken silently degrades mid-wrap, every cap in `check_budgets` keeps comparing ESTIMATE
figures against tape/bill thresholds derived from REAL tiktoken measurements, with no FAIL/WARN
raised for the degradation itself inside this file. The ONE declared instance of an outside
consumer (`_gen_chain.py`) reading this signal was not verified in this pass (out of scope).

**93a. `section_a_digest()`: produces the PINNED shape (§A → line before §C, `\n`.join, plus a
trailing newline) and a shape variant produces a DIFFERENT hash** (lines 1404–1408, the
positive/discriminating-shape half).
BITES: PROVEN-BY-SELFTEST (`selftest_growth`, lines 3787–3799: asserts the digest matches a
pinned, independently-recomputed hash AND that a shape variant — no trailing newline —
produces a DIFFERENT hash, so the bite can actually distinguish shapes, not merely reproduce
whatever the function happens to return).
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE (structural, confirmed by grep): **this function is called ONLY from
`selftest_growth`'s own pinned-digest bite — nothing in the live `check_file`/`check_budgets`
/`wrap_checks`/`run()` path calls it.** Its docstring says "M5's mover [`_gm_move.py`] MUST call
this function" — i.e. it is exported for an EXTERNAL consumer, not used by this file's own
checks. This pass did not verify `_gm_move.py` actually calls it correctly (out of scope, a
different file) — so the claim "the mover uses the same digest shape as the gate" rests on
`_gm_move.py`'s own code matching this function's pinned shape, unverified here.

**93b. `section_a_digest()`: raises (`KeyError`/`IndexError` via `spans["§A"]`/`spans["§C"]`) if
either marker is absent from `spans`** (lines 1404–1408, the exception-on-missing-marker half).
BITES: UNCOVERED. No selftest calls `section_a_digest` against a `spans` dict lacking `§A` or
`§C` to confirm it raises rather than silently misbehaving (e.g. slicing with a negative or
`None` index and returning a hash over the wrong — or empty — text).
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE: same external-consumer-only caveat as #93a — even if this raised correctly, nothing
in this file's own runtime path would ever trigger it, since `section_a_digest` is never called
outside `selftest_growth` and (per its docstring) `_gm_move.py`.

**94. `chain_parts()` / `dofirst_index()` internal refusals — the FIVE not already counted
elsewhere** (feeds `check_budgets` M10 section and `dofirst_index_present_check`; the SIXTH
reason in this family, "no `★ LATEST` banner found", is a DIFFERENT claim — it is already
claim #56 above, PROVEN-BY-SELFTEST there via `selftest_growth`'s `latest=False` fixture, and
is deliberately NOT re-listed here to avoid double-counting one proven reason inside an
otherwise-uncovered group):
  - no `_gm_usage` importable (lines 1112–1113, 1176–1177)
  - no `⬛ DO THIS FIRST` section found in GM (lines 1117–1120)
  - `⬛ DO THIS FIRST` found but zero items match `DOFIRST_ITEM_RE` (lines 1143–1147)
  - assembled index exceeds `DOFIRST_INDEX_TK_MAX`(420 tape) (lines 1155–1160)
  - `_LIVE-STATE.md` has no `⏱` delta section (lines 1234–1236, chain unmeasured)
BITES: UNCOVERED. `_gm_fixture` always emits a well-formed DO-FIRST section with matching
items, so the zero-items/no-section/over-ceiling paths of `dofirst_index` have no dedicated
fixture anywhere in the selftest suite. The "no `_LIVE-STATE.md`" case is exercised only
incidentally as a NON-refusal (the fixture repo simply has no such file and takes the "delta is
None" graceful-degradation path, lines 1229–1231) — that is a different code path from the
"has a file but no `⏱` delta section" refusal listed above, so it does not count as coverage of
this claim.
MUTATION-RED: NOT-ASKED-THIS-PASS.
CANNOT-SEE: `dofirst_index`'s zero-items refusal explicitly warns it "must never be mistaken for
an empty queue" (lines 1146–1147) — i.e. the function itself cannot tell a genuinely-empty
DO-FIRST from a parser that has gone blind on a reshaped item line; both produce the identical
refusal text.

---

## Summary table — quick counts (see final message for the MEASURED totals via grep)

| Group | Claims | PROVEN-BY-SELFTEST | UNCOVERED |
|---|---|---|---|
| G0 check_file | 1–6 | 4 | 2 |
| G1 preflight FORM (%) | 7–21 | 9 | 6 |
| G2 preflight ABS (#56) | 22–34 | 10 | 3 |
| G3 budgets structural | 35–41 | 3 | 4 |
| G4 TITLE stamp | 42–43 | 0 | 2 |
| G5 size/units/open15/25 | 44–49 | 6 | 0 |
| G6 compactable/M8 | 50–55 | 4 | 2 |
| G7 M10 chain/corpus | 56–58b | 3 (56, 57, 58a) | 1 (58b) |
| G8 M7 §A | 59–60 | 2 | 0 |
| G9 stop-line | 61 | 1 | 0 |
| G10 gauge continuity | 62–65 | 4 | 0 |
| G11 unkeyed | 66–67 (+flag note) | 2 | 1 (flag pin) |
| G12 retirement receipts | 68 | 1 | 0 |
| G13 usage probe | 69 | 1 | 0 |
| G14 index freshness | 70–74 | 3 | 2 |
| G15 usage history | 75–77 | 0 | 3 |
| G16 consult receipts | 78–80 | 2 | 1 |
| G17 lane routing | 81–83 | 1 (indirect) | 2 |
| G18 dofirst present | 84–85 | 0 | 2 |
| G19 wrap dates/git | 86–89 | 2 | 2 |
| G20 measurement engine | 90–94 | 3 (90, 91, 92 fires) | 2 (93's exception path, 94) |

(Exact totals are MEASURED in the final report message via `grep -c`, not recalled from this
table — this table is a navigation aid only.)

---

## § Replay #63 (conductor, in-window — per #57: replay what a sub reports)

- **Counts VERIFIED as reported: 96 rows · 66 PROVEN-BY-SELFTEST · 30 UNCOVERED** — and the
  replay convicted its own instrument twice before agreeing: a loose grep counted prose
  mentions (68/35), an anchored grep missed 10 bolded `**UNCOVERED.**` cells (66/20). The
  sub's figures balanced all along. ⚠ Cosmetic-but-real: the verdict vocabulary is written
  in two typographic forms, which breaks one-pass greppability — normalise at ratification.
- **VERIFIED in-window:** `UNKEYED_BLOCKING` (:1968, `True`, used :2478) has exactly two
  occurrences file-wide — no selftest pin; a silent flip is invisible. · The `_gm_fixture`
  comment at :2869 claims `title=False` bites the absent-title path; :2844's signature
  default is the ONLY other `title=` in the file — no call site passes it. A comment
  claiming a bite, with no bite: the documenting-a-defect-≠-immunity class, in the gate
  that inscribed that very lesson at :2861. · Selftest summary re-run in-window, matches
  the sub's quote verbatim.
- **Phase 2 queue = the 30 UNCOVERED rows**, headline items per the sub: #39 (ds-022's
  fail-loud-on-4th-unrollable cross-check — a #58 ruling untested), #42 (no-TITLE FAIL,
  the falsely-claimed bite), #84/#85 (dofirst-index checks never called by any selftest),
  #89 (git-uncommitted WARN). Status remains **DRAFT — not ratified**.

---

## § Ratification #64 (Fable conductor, 2026-07-31)

**RATIFIED.** Phase 1's enumeration (96 claims · 66 selftest-proven · 30 UNCOVERED) is
discharged as a map: phase 2 (`_bite-matrix-capture-gate-PHASE2-DRAFT.md`, ratified #64)
mutation-tested all 30 UNCOVERED rows against the enumeration as numbered here, and none of
its runs contradicted a phase-1 claim. The two flag-notes (UNKEYED_BLOCKING pin, the
`_gm_fixture` title=False call-site gap) remain open items, phase-2-verified as documentation
defects not mechanism defects.
