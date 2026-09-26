# R5 — Apollo-MCP probe · resumable notes (lead seat, #304, 2026-09-26)

HEAD at start: 571d458c (read-only). No Agent tool at this seat: lead ran 5a/5b/5c itself.
Env: seat python3 3.10.12 has jsonschema 3.2.0 (draft-7 only). A2UI is draft 2020-12, so a venv
at $HOME/.r5venv (jsonschema 4.23.0) is used for A2UI checks ONLY. Recreate:
  python3 -m venv $HOME/.r5venv && $HOME/.r5venv/bin/pip install jsonschema==4.23.0
A2UI v0.9.1 spec fetched at the seat into a2ui-v0.9.1/ (FETCHED.txt has URLs, UTC time, sha256;
same hashes as the cloud fetch 2026-09-26T15:23Z).

Plan: 5a gen_catalogue.py -> catalogue-dashboard.json, catalogue-all.json, catalogue-report.json
      5a validate_a2ui.py (venv) -> a2ui-validation.json
      5b gate_mem.py -> gate-mem-results.json (differential vs disk a11y.check, planted defects, timing, audit-hook no-write proof)
      5c SPEC-when-evaluator.md (5a's spec), when_eval.py -> when-eval-results.json (test table, reader comparison)
Dashboard parts = union of $composes on template-dashboard + template-dashboard-bento, + worked-example
parts (chart-line, list-items), + the #261 dashboard metas (filter-toolbar-bar, legend).
Status log:
- 2026-09-26T15:35:21Z 5a gen_catalogue + validate_a2ui done (137/137, 18/18 A2UI-valid; 4 of 13 schema errors published via stateModel). 5b gate_mem done (T1 137/137 identical; P0-P13 ok; K1-K3 known misses; warm ~60ms, 0 writes). Next: 5c.
- 2026-09-26T15:52:07Z final run_all.sh done; RUN-LOG.txt has receipts. Next: report.
- 2026-09-26T15:54:55Z report filed.
