# The handoff testing regime — how #77 moved (the why and how)

provenance: local_d88890e5-8ac4-4fa4-8447-31fedf412293 · 2026-08-02
status: observed

*Companions: the ruled plan `notes/2026-08-02-handoff-testing-regime-plan.md` · ledger
`notes/_MEMENTO-DECISIONS.md` § ★ #77 · inventory `notes/2026-08-02-handoff-periphery-inventory.md`.
This records the ARC; the WHAT lives in those.*

## The ask, and why it wasn't answered with code first

Dave's #76 ask was a sentence: *"a rigorous testing regime… it keep breaking."* The temptation
was to build the memory's proposed `_roll_state.py` immediately — the shape was already
sketched. The session instead spent its first hour verifying the PREMISE against the call
graph, because the memory's own text warned "verified not assumed," and because the last seven
breakages were all fixes built on unverified premises. The verification changed the design
twice before a line was written: it confirmed the banner-before-gate mechanism structurally
(`gauge_log_continuity` BLOCKS and thereby *changes what the session did* after the banner
said what it did), and it found that the plan's central dichotomy — "wire the check at the
commit seam vs the wrap gate" — was FALSE, because #74-D1 had already unified them (the commit
script runs `--wrap`). The check needed a home, not wiring. A ruling was corrected by addition
at read-back, before enactment, instead of being discovered broken three sessions later.

## The read-back that separated a nod from a ruling

Dave's "cool, remember to test the crap out of it" read as approval; recording R1–R4 as ruled
on that sentence would have been laundering a nod. The read-back question cost one exchange
and got an explicit option-select ("All four ruled — build"). The distinction matters here
more than anywhere: this whole programme exists because testimony drifted from fact.

## The finding of the session: the gate's first live mutation was itself

The sub built T2 with two arms — the generated form plus authored roll-claim forms, my spec.
The first live `--wrap` run false-fired twice on RATIFIED #76 text: the heading's narration
word "RESIDUAL", and the banner *quoting* #75's false claim in italics with attribution.
USE vs MENTION, exactly as `[[gate-must-quote-what-it-forbids]]` predicts: unreachable by
syntax. The repair was also already canon — `[[ban-scoped-to-a-name]]`'s "home the measurement
in a standing form": the residual claim now has exactly ONE legal home (the generated line),
presence + uniqueness + correctness of that line are gated, and prose is never scanned. The
false-fire state is pinned as the mention-immunity fixture, so the regression corpus's first
entry is the regime's own first defect. A correct state (the ratified #76 banner) was briefly
unreachable-green; that class — a new gate refusing a correct state — is ds-022's lesson and
was caught the same hour because the live run WAS the mutation test.

## Dead ends and confessions, kept because they're the useful part

The `$?`-after-pipe misread: while attributing the step-11 red I echoed an exit code that
belonged to `tail`, not the selftest — the exact trap `[[check-after-its-own-remedy]]`
documents, committed by the session enacting that memory's sibling. The survey's direct exit
was the truth. Also: a `git stash` control run failed silently on a stale `.git/index.lock`;
the control was rebuilt on `git archive HEAD` instead, which reads the object DB and cannot
touch the index — a cleaner control than the one that failed. The lock was left for
`_git_commit.sh`'s dance, per the standing rule.

## The periphery inventory (Dave widened scope mid-flight)

Fifteen named probes produced the phase-2 evidence base and three live findings nobody asked
for: the `_build_all` label-substring misroute (a consult-index failure reports as
dark-surface), the spine's ungated writer (`_build_live_state.py`), and the fact that
`_git_commit.sh` — the seam the whole regime is delivered through — has no test and nothing
that runs it. The step-11 inherited red (`_gm_usage` real-repo arms, red AT HEAD, attributed
clean via the archive control) was declared and priced as P0, not chased at wrap depth.

## Resolved state, and what's open

Shipped and T0-proven: `_roll_state.py` · `roll_claim_check` (BLOCKING, one legal home) ·
T3 generated commit headline · the regression corpus with the growth contract R4 · the
measurer's selftest wired into STEPS. Open at #78: P0 step-11 diagnosis · phase-2 rulings
P1–P7 · the DV-D19 specimen rebuild (owed since #76, displaced by the periphery ask) · the
third consecutive zero consult-receipt, now a pattern. Declared unproven at authoring: T3's
first real headline fires on this wrap's own commit.
