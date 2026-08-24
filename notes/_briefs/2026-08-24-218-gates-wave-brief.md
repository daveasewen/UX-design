# #218 build brief — the gates wave (priced machinery, batch of six)

Opened under Dave's #218 crank. Every item below is PRICED IN THE RECORD and has bitten at
least once. Fix the CLASS, never patch ("always real fixes never patches, they just get lost").

1. **INSTRUMENT-STRAY re-scope** (`_capture_gate.py`): its premise predates `s217-D1` — it fires
   on committed-surface derivatives in `knowledge/assets/photography-web/` because it keys on
   UNTRACKED. Re-scope so ruled committed surfaces (the s217-D1 derivative dir) are recognised;
   the check must still catch a genuine instrument-stray (keep a red arm proving it).
2. **Capture-gate write-door class (#158)**: `--selftest` (and audit any other read-shaped
   flags) writes `knowledge/_CAPTURE-GATE.md`. Read-shaped invocations must not write; move the
   write behind the explicit write path only. Grep for the class, not the instance.
3. **Boot-drift parser**: `_parse_boot_samples` reads any number beside 'boot' as a reading —
   "declared boot 2,345 over the band" parsed as a 2,345 boot. A delta beside boot is not a
   reading; make the parser distinguish, with tests from the #215 line verbatim.
4. **Register-vs-store join gate**: `knowledge/_GOVERNING-RECORDS.md` rows vs `_state.json` —
   three rows proved the drift (#212). Build the comparing check into the wrap gate set,
   ADVISORY at birth (promotion is Dave's).
5. **`mask_comments` dedup**: duplicated across two generators with no comparing gate (W-92
   residual). Either a shared helper consumed by both, or a byte-comparing gate — prefer the
   helper (one implementation), keep both call sites' tests green.
6. **Section-usage vocabulary finding (#218 wrap)**: `WEATHER` unregistered + 7 LS sections
   without testimony — #217's line passed, #218's failed, so the vocabulary tightened between
   wraps. Find what changed, make the rule explicit and self-testing; do not loosen it blind.

**Fence:** no rulings, no threshold/constant/band changes, no promotion of any advisory to
blocking (Dave's), no lane/GM/LS/memory edits, no commit/push. Every new/changed gate DRIVEN
red on a planted defect before it counts ([[instrument-without-a-consumer]] — never inscribe a
fence you did not try to cross). Selftests for everything touched. Return: per-item verdict,
red-arm receipts, residuals priced.
