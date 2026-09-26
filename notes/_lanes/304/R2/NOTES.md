# #304 Run 2 — working notes (resumable)

Lead: R2 seat (Opus 5.5), 2026-09-26 evening. Baseline HEAD 571d458c; stores clean at HEAD
(git diff --stat empty for _state.json/_rulings.json/_state.py at start).
Baseline sha256: _state.json 819af21f… · _rulings.json 96ee3fce… · _state.py 13fac7d6…
Round-trip: _state.load()+save() is byte-identical on the live store (1,029,244 B) — save() is safe.

Plan: A = back-stamp audit (_inscribe_ruling.py --set-status only); B = receipted closes (via _state API);
C = advisory regrowth arm in _state.check() + mutation test. Every write logged in WRITES.log.

## Progress (all DONE 2026-09-26 evening)
- 2a audit: audit.py → audit_proposals.json (450 = 424 bare + 26 not-enacted-text); decide.py → decisions.json
  (ENACTED 184 · UNCERTAIN 109 · NOT-FOUND 157). stamp.py --write stamped 184 via _inscribe_ruling.set_status;
  verify_stamps.py (second pass) 0 errors. Pre-stamp copy /tmp/r2/rulings-pre-stamp.json (sha 8c482d45…, includes Run 1's s282 amends).
- 2b closes: close_receipts.py/cite_lines.py → close_plan.py → close_plan.json (CLOSE 53 · LEAVE-OPEN 40);
  close.py --write via _state API; verify_closes.py (second pass) 0 errors. Pre-close copy /tmp/r2/state-pre-close.json (= HEAD).
- 2c arm: knowledge/_state.py REGROWTH arm + selftest bites (66 → 72); mutation_test.py → mutation_test.json VERDICT BITES.
- Regenerable inputs live in /tmp/r2 (VM): gitlog.raw/commits.json (parse_git.py), treelines.txt (git grep, see audit.py header).
- NOT done by design: no commit, no push, no regen (chain/rulings page/schematic go stale — commit seat regenerates).
