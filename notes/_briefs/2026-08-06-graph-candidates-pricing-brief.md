# Graph-engineering candidates — pricing + ordering brief (#115, 2026-08-06)

Source: `_RESEARCH-graph-engineering-2026-08-05-v3.html` § "Six candidates, cheapest first".
Status at survey: NONE enacted (verified in-repo #115, not from roll pointers).

## Finding that re-prices the lane (measured this session)

The doc priced candidates 1+2 "Small — a lookup and a merge, not a new data structure."
**Premise half-false:** `_decision-graph.json` node IDs (100: `ADR-*`, `R-D*`, `TYPE:*`, …)
have **0/575 overlap** with `_memento-index.json` record IDs (`gm:*`, ledger ids). Edges
cannot be joined by ID. Records DO mention node IDs in body text (33 records hit on a
5-node sample), so a **mention-map** (node-id → record-ids, built by scanning record
blobs) is the missing join — an extra build artefact with its own freshness obligation
(`index_freshness_check` is content-compared and BLOCKING). Re-price: 1+2 = **Medium**.

## Blast-radius survey (what a ranking change can touch)

- `_search_core.py` `search()` is the ONE spine; consumers: `_memento_search.py`
  (Memento door) + `_consult.py` (DS door). Both have known-answer selftests that
  assert *presence within caps* — a demotion (candidate 2) can push a known-answer
  record below its bucket cap and fail those tests, or worse, silently change what a
  cold session retrieves.
- `_capture_gate.py` imports only `RECEIPT_LINE_RE` / `validate_receipt_payload` —
  ranking changes do NOT touch the gate. Confirmed by grep, quoted lines 2925–2954.
- `search()` already has a `decorate(entry)` hook — the ADVISORY seam: attachments
  can ride it with **zero ordering change**.
- `_build_all.py` step runs `_search_core.py --selftest`; its selftest asserts
  behaviours that must keep biting (miss, caps, honest denominators).

## Order (the ruling being asked for) — each step inert until the next is opened

0. **Mention-map builder** — new small artefact `_build_graph_mention_map.py` →
   `_graph-mention-map.json`; wired into `_build_all.py` + freshness check.
   No consumer yet (instrument-without-a-consumer declared, discharged by step 1).
   ~8–12K sub-build (planning estimate).
1. **Candidate 1, ADVISORY/display-only** — via the `decorate` hook: attach
   `supersedes/refines/bounds` neighbours to results as extra lines. **No score
   change, no re-ordering** ⇒ known-answer selftests pass unchanged by construction;
   still DRIVE it on real queries before trusting (green tests can't see scope).
   ~15–20K sub-build + drive. Check-in inside the lane (>15K rule).
2. **Candidate 3** — three-questions claim gate as a runbook line. Trivial, ~2K,
   zero blast radius; can land any time, kept out of step 1's commit
   (conflated-fix rule).
3. **Candidate 2, MARK first** — superseded results get a visible ⛔ mark, still
   ranked as before. Observe across a session.
4. **Candidate 2, DEMOTE** — the ONLY step that changes ordering. Separate commit;
   detection and demotion mutation-tested as SEPARATE clauses (#114-D2 pattern);
   known-answer selftests re-driven; any known-answer displaced = stop + re-price.
   ~10–15K.
5. **Candidates 4 / 5 / 6** — separate later lanes, NOT opened by this brief:
   4 temporal ADR-0007 (specified, unbuilt); 5 blast-radius gate (must ship
   ADVISORY per gate rules); 6 compile views 2–6 (Large).

## Budget vs quota (which binds)

Builds delegatable to Sonnet subs ⇒ cheap in FILL, 5–10× markup in QUOTA.
Conductor fill for steps 0–4 ≈ briefs + report ingestion + drives, est 25–35K.
Name Dave's live quota reading at the opener before picking posture.

DO-NOT-RULE for any sub: no cap raised to clear its own gate; no promotion of
candidate 2 to demote without the step-3 observation window; edge set stays
closed (#75).
