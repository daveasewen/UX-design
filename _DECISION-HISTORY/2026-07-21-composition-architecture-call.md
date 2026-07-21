# 2026-07-21 (late night #3) — The composition architecture call: ADR-0013 ruled in one pass

*Session "Apollo rulings + architecture" (Fable solo, fresh window ~22:40 BST). Opened per the
Phase-1 handoff to run Dave's ruling batch + the composition/atom-retrieval strategy call; Dave
ordered the strategy call first ("2 then 1"). Spine entries: `_LIVE-STATE.md` latest delta ·
`docs/decisions/ADR-0013-component-type-tier-composition.md`. Both-way links live in each.*

## The arc

**1. CONSULT ran thin — and Dave's mid-flight question found a real hole.** The pre-design CONSULT
on "composition mechanism / organisms / partials" surfaced only type-tier rulings. Dave asked "does
that mean CONSULT isn't being updated?" — the check that followed found the index fresh (rebuilt
every build) but the corpus MISSING `_BUTTON-DECISIONS.md` entirely: B-D1…B-D5 unfindable by any
query. Logged **ds-009** with a selftest fix (assert every `_proforma/_*-DECISIONS.md` on disk is
indexed) so the NEXT new ledger can't repeat it silently. Secondary, already a `_FUTURE-STATE`
path: keyword retrieval can't bridge vocabularies ("organisms" never reaches "override sets").

**2. The survey made the finding quantitative.** Worker A's Phase-1 claim ("organisms re-implement
atom rules") checked out worse than the handoff line: 13/40 snippets carry a local button recipe;
7 carry Button's scale-press by copy; 4 press with `translateY` — drifted physics;
Selection-controls carries BOTH in one file. Copies drift — that is the whole case, observed.

**3. The unlock: this is a symmetry, not an invention.** T-D9/T-D12 already solved rule-sharing for
TYPE — composites in `type.css`, bound by selector lists in `_type-bindings.json`, guarded by the
blast-radius gate. BOX/interaction had no equivalent. The composition mechanism is the box-side
twin of the type system, and Dave's queued component-type flex tier is where its VALUES live — one
architecture question, exactly as the handoff suspected ("retrieval must reach INSIDE organisms").

**4. Partials-vs-classes was decided on source-of-truth, not convenience.** Runtime class-sharing
(the "industry best practice" shape) is TRUE single-source but inverts the KB's dependency
architecture — snippets (the gated source) would consume `canon.css` (a generated artefact).
Generated partials keep the projector contract (source self-contained; generator projects; gate
verifies sync) and extend it from values to rules. Dave's stated principle — "correctness, solid
build, flexibility and best practice rather than expedience" — was applied and the answer held:
partials ARE the correct architecture inside the KB; class-composition lives at the ADR-0008
adapter boundary; the component machine stays the horizon with partials as its parts bin.

**5. The gauge earned its keep, then broke.** Dave asked for a context check. Half 2 (out-of-band
subagent measurement) failed twice: it measured LAST NIGHT's conductor session (picked by recency
from the session list — the live session wasn't identifiable), and `read_transcript` renders tool
calls as stubs with results stripped (13KB for a session whose receipts alone are bigger), then the
subagent RATIONALISED the bad number ("the reading is valid… conveyed efficiently") — the
confident-false-inscription class, caught because the tally said ~52% while the instrument said
19%. In-head tally (Half 1) governs until Half 2 is rebuilt; warning inscribed in
`_RUNBOOK-context-gauge.md`. Wrap fired at mid-Amber by agreement, per "author the handoff while
quality is intact".

**6. Ruled in one confirming line.** All four recommendations went firm under the correctness
principle; Dave: "very happy we can wrap up now". ADR-0013 inscribed same hour.

## Resolved state

ADR-0013 Accepted · ds-009 logged · gauge runbook warning added · `_FUTURE-STATE` tiered-flex
entry graduated → ADR-0013 · ruling batch (§C·1) NOT run this session — moved to the next window
by the gauge call. Open: everything in ADR-0013's Consequences (the clean-room build), the batch,
and the enact-queue.
