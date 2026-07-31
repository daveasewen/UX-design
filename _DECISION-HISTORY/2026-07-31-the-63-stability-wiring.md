provenance: local_aa3d71d3-9961-4f44-9fc7-1d56283a5f90 · 2026-07-31
status: observed

# #63 — Stability wiring: CI learns to ask, the ladder gets its words, and a stale instruction dies

*Both-way links: ledger `notes/_MEMENTO-DECISIONS.md` § ★ #63 · spine `_LIVE-STATE.md` ⏱ LATEST
delta #63 · commits `816f726` → `e920080` → `618a3ea` → `90510dc` → `034c299` (+ wrap).*

## The arc

**1. The seam was found by reading, killed by asking.** Dave's redirect gave #63 "CI asks the
survey". The probe (research-first, his instruction at the opener) found the mechanism already
located to the line — #60-D4: `_build_all.py` writes the chain (:184-186) and the index
(:160-161) then checks its own output, and CI ran only `_build_all.py`. The design collapsed to
ONE inserted workflow step: run `_build_survey.py` against the COMMITTED tree before the build.
The probe also invalidated a premise nobody had flagged: `gates.yml`'s "zero pip installs,
stdlib-only" (07-02) pre-dates the real-token ruling — step [70] on a clean tree REFUSED under
the estimate fallback in this very session's fresh sandbox. tiktoken is now installed in CI, and
the refusal was recorded as the correct behaviour it is.

**2. Mutations before wiring, and the harness bit its own handler.** Controls green → stale
chain → [70] red (quoted) → restore → green; whitespace-injected index → [66] red → restore.
Mid-test, `git checkout` failed (the sandbox unlink guard), the `&&` chain broke, and a green
that looked like Mutation B was actually a control on the unmutated index — caught by reading
the output rather than the exit codes. Attribute the diff; a green needs a named cause too.

**3. A parallel window was live.** #62 was still closing while #63 worked: its 5b-4 commit
briefly swept this session's draft (repaired by #62 with explicit paths), its stand-down
receipt (`notes/_receipts/2026-07-31-62-tree-receipt.md`) landed between this session's
reconcile and its stage — so `e920080` carries a fifth file the reconcile never named. The
receipt turned out to be FOR this session, so the sweep was benign, but the lesson is #62's
own warning arriving one commit late: `git add -A` cannot scope, so a reconcile is stale the
moment another writer exists.

**4. The paste-ready summary died of its premise.** Dave: "I don't know where this instruction
has come from... you commit, I push." Traced: born 2026-06-24 when the sandbox could not commit
at all — Claude handed Dave a paste-ready block to run himself. `_git_commit.sh` (07-26) ended
the premise; the instruction survived in three live runbooks + memory. All four corrected by
addition (RETIRED notes, archives left as record). Premise-ages-faster-than-rule, textbook.

**5. The bite matrices ran on the six-beat ladder, and the replays earned their keep.** Dave's
chunking caution shaped the method: one gate per pass. Mover — Sonnet sub, whose replay
confirmed real findings (dead code at `_gm_move.py:196-197`; `STRATA_KEY_RE` blindness) and
caught its report disagreeing with its file and a "verbatim" block that was prose. Chain +
index — in-window, since the day's live mutations already proved their bites; a sub would have
re-proven the proven. Capture gate — phase 1 only (enumerate + map, zero mutations, hard rule):
96 claims, 66 selftest-proven, 30 UNCOVERED. The replay of THAT one convicted the conductor's
own instrument twice (a loose grep, then an anchored grep that missed bolded cells) before
finding the sub exactly right — replay cuts both ways, which is why it is a rule and not a vibe.

**6. The ladder got Dave's words.** RETRIEVE · RESEARCH · ANALYSE · PLAN · PROBE · TEST —
#63-D1, wording his, examples kept (conductor's call, explicitly offered): each beat names its
machinery, and a beat with no machinery yet is a gap worth seeing. He had invoked the ladder
twice at the opener before wording it — a ruling that records practice already in force.

**7. The one-pager.** Public register throughout (no gate/token mechanics), three functions per
his #62 correction: the record (layered, never flattened) · the pricing (declare cost first,
delegate-and-verify) · the orientation (what do I have to do today). Framed on the film's real
insight: the enemy is the confident false inscription, not forgetting. Approved in draft same
session; his voice pass owed.

## Dead ends and corrections

- Worktree isolation for subs is unavailable here (agent home ≠ git root) — fell back to a
  hard untouchable-files rule in the brief; both subs held it (verbatim `git status` proof).
- The first mutation-test bash chain silently skipped Mutation B (see 2) — re-run properly.
- Two stale `index.lock`s appeared mid-session (parallel-window era); both moved to
  `_to_delete/_stale_locks/`, never rm'd.

## Resolved state · still open

Resolved: CI asks before it builds (bite proven both directions) · #63-D1 inscribed ·
paste-ready retired · 4/5 matrices drafted · one-pager v1 approved in draft.
Open (queued #64, priced small-to-medium): `_gm_usage.py` matrix · capture phase 2 (30 rows;
headline: ds-022's #58 cross-check untested) · mover count reconciliation (4 unverdicted rows) ·
CI's first real verdict on the wired workflow (lands on Dave's push) · Apollo, six sessions
unmoved — #64 opens there.
