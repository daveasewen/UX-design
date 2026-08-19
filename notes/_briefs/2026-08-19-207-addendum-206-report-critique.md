# ADDENDUM to the #206 record — Dave's critique, homed for the next run (#207, 2026-08-19)

> **Status: DAVE'S REVIEW NOTES, homed verbatim-in-substance. Nothing here is a ruling.**
> Delivered in chat at the #207 opener with the words *"consider this as an addendum to the
> preload and the next run"*. This file is that addendum's durable home (store row `W-51`;
> the forgotten-document class #185 is why it is a file and not a chat message).

## 1 — The promotion line was an ID-code decision surface (the #170 class)

"P-2, P-4, P-5" is not a surface Dave can rule on; ruling on it requires opening a manifest,
which is the burden the plain-prose rule exists to remove. **The plain-words expansion, which
every future presentation of this decision must use:**

- **P-2 = the duplicate-id / unresolved-IDREF scan** — caught the #204 duplicate-ids-across-theme-panes
  class; at #206 it found 46 findings (10 duplicate-id, 36 unresolved-IDREF) across 7 pre-#204 review files.
- **P-4 = the premise-vs-store scan (unrowed-document catch)** — caught briefs with no store row;
  at #206 it caught the #206 brief itself (repaired in-session, row `W-50`) and
  `notes/_briefs/2026-08-16-memento-closeout-plan.md` (still unrowed).
- **P-5 = the stale-figure grep** — caught `knowledge/README.md:13` typing "(38 metas)" against a
  live 92 (repaired at #207, see §3).

## 2 — "Promote or wait" may be pre-answered, and presenting it as free launders an open question

`s204-D1`'s promotion bar is *caught twice, two sessions, receipts named*. All three candidates
are **mixed basis**: **one live catch each** (#206) plus **mined history**. Whether a mined
historical occasion counts as a "catch" toward the twice-caught bar is a **vocabulary question
nobody has ruled** — presenting "promote or wait" as a free choice quietly launders it into a
settled premise ([[feedback-dont-launder-a-premise-into-a-ruling]]).

**The honest form, Dave's own words:** *"one live catch each; whether mined history counts toward
the twice-caught bar is itself yours — if it doesn't, the ruled answer is already 'wait'."*

Open question, with its store search per `s202-D3`:
`python3 knowledge/_memento_search.py "twice-caught mined historical live catch"` and
`grep -i "twice" knowledge/_rulings.json` — both run at #207: no ruling defines "catch".
**OPEN, DAVE'S.**

## 3 — Decision 1 was bundled; the README half cost Dave a decision it shouldn't have

The README count (38 → 92) was a factual re-measure with direct precedent — Dave said "do it" to
the identical ASSERT-009 class at #205. **DONE at #207 by the conductor, not put back to Dave:**
live count re-measured in-sandbox (92), `knowledge/README.md:13` corrected to point at
**ASSERT-009** (which already registers the count as a re-tested predicate, `glob_count n=92`),
and `README.md` added to ASSERT-009's `asserted_in` so the P-5 class re-tests it instead of
anyone repeating it.

**The one real decision remaining from #206's "Decision 1": repair-or-park on the 46
duplicate-id / unresolved-IDREF findings** (carried by `W-49`'s `closes_when`). **DAVE'S.**

## 4 — Candidature homing: the tool's restraint is correct, but stdout is not a home

The spec said promotion candidature gets recorded in `knowledge/_DS-IMPROVEMENTS.md`; `_promote.py`
correctly writes nothing (mtime-proven). But candidature living only in a chat message is the
forgotten-document class wearing a new hat. **Homed at #207:** a candidature entry now exists in
`knowledge/_DS-IMPROVEMENTS.md` (recording, not promoting — promotion stays Dave's under
derivation governance).

## What Dave said reads clean (recorded so the next run doesn't re-litigate it)

The red-then-targeted-fix CI arc, "reported not repaired", the restraint on the two non-promoted
probes (the meta-schema check and the dangling-var pixel probe), and the declared heuristic limits.
