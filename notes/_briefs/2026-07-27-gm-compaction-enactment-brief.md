# ENACTMENT BRIEF — GM growth contracts (GM-D1…D9)

provenance: local_1ffa04b1-ec26-4dd2-ab19-8c1d8e94167d · 2026-07-27
status: ruled — `notes/_MEMENTO-DECISIONS.md` § GM growth-contracts ruling

**For the enacting window. Opus conducts; Sonnet optional for the mechanical move lanes.
Price: ~30–40% of one window. READ, don't reconstruct:**

1. **The ruling** — `notes/_MEMENTO-DECISIONS.md` § *GM growth-contracts ruling — 2026-07-27*
   (nine rows, each with its WHY). That section is the authority; this brief only sequences it.
2. **The full option text + evidence** — `notes/_briefs/2026-07-27-gm-compaction-architecture-proposal-v1.md`
   §3 (decisions) + §1 (measured diagnosis). Do not re-derive the diagnosis; numbers were
   measured 2026-07-27 and re-measuring is only needed where an edit depends on a current count.

## Order of work (runbook-first — the rule must exist before any move cites it)

1. **Amend `knowledge/_RUNBOOK-capture-ritual.md`:** add step **2e** (DO-FIRST contract + roll,
   D1/D2/D3) and step **2f** (stratum stack, D5) · amend step 2's required structure per **D4**
   (§B deleted; banner spec absorbs evidence-per-claim, provenance-shaped lines, model/effort,
   gauge stamp) · archive batch key → `<date> <session#>` (D5).
2. **Amend `_RUNBOOK-context-gauge.md`** per **D9**: floor measured per session, bands on remaining
   budget; band numbers put to Dave in that pass if he wants them re-dialled, else carried over.
3. **Wire `_capture_gate.py`** per **D8**: per-section line counts + GM/LIVE-STATE size stamps
   (D7), warn at cap / BLOCK at cap+50%, failure text = runbook step name only.
   **Ships with bites: an over-budget fixture must go RED, plus a bite-the-bite.**
4. **One supervised compaction pass** under the new rules, one commit:
   - §B strata → `_GM-ARCHIVE.md` (D4) · dead DO-FIRST strata (#10/#11 layers + retired notices
     per D2 tests) → archive (D1) · stack post-mortems → NEW `notes/_GAUGE-LOG.md`, commit-states →
     archive, LATEST kept in GM (D5) · §C pruning pass to pointer+state+owner, cap 150 (D6) ·
     read-chain contract line replaces GM :288's open chain; GM :5 band table → pointer (D7/D9).
   - **The D3 grandfather audit rides along:** existing untagged notices retire ONLY via the D2
     tests, checked one by one, receipts in the batch headers.

## Non-negotiables (verbatim from the ruling — violating any of these voids the pass)

- **§A is UNTOUCHED.** No cap, no roll, no rewrite, not even a guard banner. Verify by hash:
  the §A byte range must be identical before/after every edit session (07-18 incident, runbook :126–131).
- **Every roll passes the 2c EXIT CHECK** (runbook :107–112): ⚠/⬛/AWAITING/OPEN-CALL/DEFERRED-TO-DAVE
  items must already live in a standing section before their block moves. Dated homes do NOT count.
- **Rolls are verbatim MOVES, never rewrites.** Archive = convenience copy, never a tattoo:
  durable rules/thresholds must be inscribed in their proper homes BEFORE the move (2c precondition).
- **Splitting never buys headroom** (ADR-0015 phrase, ruled into D8): content may not migrate to a
  new un-governed file.
- **Nothing beyond the nine rulings.** `_LIVE-STATE` 2d-tightening is explicitly OUT OF SCOPE
  (D7 note) — if the D7 budget can't be met without it, STOP and put that fork to Dave.

## STOP conditions

Any EXIT-CHECK item with no standing home (copy it up first, then continue) · any edit that would
touch §A · gate bites failing to go red · projected band breaching the reserve. On STOP: inscribe
state, fork to Dave.

## Receipts owed at close

Per-batch EXIT-CHECK receipts in `_GM-ARCHIVE.md` headers (batch key `<date> <session#>`) ·
`_capture_gate.py` selftest green incl. new bites · STAND-002 green · before/after line+token table
for GM (§4 of the proposal predicts ~910 → ~450–500; publish actuals against it) · one paste-ready commit.
