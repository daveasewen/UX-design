# ADR-0017 — WRITE-ONCE: live facts get ONE home and addresses; history gets copies, dated and frozen

**Date:** 2026-08-17 · **Status:** accepted (Dave, in-chat, 2026-08-17 #192: *"promote WRITE-ONCE to an ADR, but lets get this fixed very soon, it's foundational"* — promoting the candidate-ADR he parked earlier the same morning) · **Origin:** the #192 reconnaissance lane's parked record, committed at `b9c72c6` (`knowledge/_DS-IMPROVEMENTS.md` § ds-0NN #192 GENERALISATION — that entry is now a dated PERIOD RECORD of the drafting; THIS file is the live home) · **Extends:** ADR-0007 (decision graph), ADR-0016 (enactment proof — liveness is the enforcement half; write-once is the storage half) · **Relates:** ADR-0013 ruling 3 (accrete from observed duplication, never speculation)

## The principle

A **live fact** — a number, a rule, a path, a status that can still change — lives in exactly
**one home**. Everything else that needs it carries an **address** into that home, never a copy.
**History** is the opposite: a dated period record is a **frozen copy** and rewriting it
falsifies the record.

## Why it is foundational (Dave's word)

The project's two worst recurring failure shapes are both violations of this principle:

1. **Re-discovering what exists** — a fact with no findable single home gets re-derived,
   re-built, or presented as open while ruled (#80 re-derived a ruled measurement; #188
   presented a 4-session-old ruling as open; DV-J1 was queued while already closed).
2. **Building what nothing reads** — an instrument that is not the addressed home of anything
   participates in nothing ([[instrument-without-a-consumer]]; the sparkline proof, the survey
   bucket, the surface recorder — and the blind-harness class, which recurred at #191 and is
   now gated by `knowledge/_gate_harness_stubs.py`, W-33).

Copies of live facts stale silently (#185 B3 WRONG-TEXT figures; #167 home-pointer rot;
#41 five sessions overpaying for a chain instruction buried in the file it governed).
The system's best fixes are already applications of the principle: `_gen_chain.py` (chain
GENERATED from one source), `_gen_lanes.py` (gate IMPORTS the one implementation),
canon.css regenerated from snippets, s177-D1 (no evidence pointers into rolling files),
s188-D1 (the grader reads the hook FILE), and the token spine + alias hop itself.
The full receipt list, by instance, is in the period record at `b9c72c6`.

## Rules

1. **One home per live fact.** Before writing a fact down, name its home. If a home exists,
   address it; if not, create the home and address it from day one.
2. **An address must have a resolver.** An address nothing resolves is the #145 binds gap —
   *worse than a copy*, because it looks checked and is not. Entity and first resolver land
   TOGETHER, or the address is prose with extra syntax.
3. **History is exempt and protected.** Dated period records (ledger entries, ds-entries,
   decision-history dossiers, ratified records) are frozen copies BY DESIGN; rewriting them is
   the falsification this ADR forbids in the other direction ([[feedback-header-wins-over-audit]],
   the #184 ruling on `_DS-IMPROVEMENTS.md:249`).
4. **Maps are generated and gated, never hand-kept.** A hand-maintained inventory is itself a
   copy of live facts and rots accordingly (`_lanes.json`, stale since Jul 28, is the standing
   exhibit). If a map is wanted, it is emitted from the homes and a gate compares.
5. **Consumer-first.** A new instrument lands with the consumer that reads it, and a new
   document lands with its store row (`_state.add()`, the doc-row gate, #188) — presence in
   the addressed graph at creation, not later.

## Enforcement posture ("very soon" — Dave)

Adoption is ADR-0013-style: **accrete from observed duplication**. Each next instance is
converted as it is touched, not in a big-bang sweep. The named candidate next instances
(meta `$status`/`$note` prose → address into `_rulings.json`; MEMORY.md hooks restating file
content → hook-as-address) are queued in the period record. New work is held to Rules 1–5
from this date; a violation found in review is cited against this ADR by number.

## Consequences and pitfalls (replayed, Dave #165)

- **(a)** Rule 2 cuts both ways: converting prose to addresses WITHOUT building the resolver
  makes things worse, not better. When in doubt, keep the copy until the resolver is priced.
- **(b)** Rule 4 does not license deleting `_lanes.json`-class documents — it licenses
  generating them; their content may still be Dave's.
- **(c)** The ADR itself is now the ONE home of the principle. The `_DS-IMPROVEMENTS.md`
  ds-0NN GENERALISATION block is a period record of the drafting and must not be edited to
  "sync" with this file.
