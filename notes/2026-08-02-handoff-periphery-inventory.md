# Handoff periphery — measured producers/consumers inventory (phase 2 evidence base)

provenance: local_d88890e5-8ac4-4fa4-8447-31fedf412293 · 2026-08-02
status: observed

*Dave's ask, #77 mid-flight, verbatim: "after I want to test/analyse all the peripheral
mechanisms too, the graphs, eval, hooks, the state manager, all the supporting mechanisms too,
anything that touches it." This is the MEASURED inventory (Explore sub, 15 named probes,
conductor-replayed highlights) that phase 2's test plan builds on. Companion:
`notes/2026-08-02-handoff-testing-regime-plan.md` § Phase 2.*

## The table (mechanism · reads · writes · selftest? · wired where · can fail?)

| mechanism | reads | writes | selftest? | wired | can fail? |
|---|---|---|---|---|---|
| `_capture_gate.py` | GM, LS, chain, gauge-log, both archives, index (in-process) | `_CAPTURE-GATE.md` (build mode only) | yes | build ×2 + CI; `--wrap` only via `_git_commit.sh` | yes |
| `_git_commit.sh` | GM (T3 parse), msgfile, git; transitively `--check`+`--wrap` | msgfile line 1, the commit, lock moves, `git add -A` | **no** | **nothing runs it** | yes |
| `_gen_chain.py` | GM, LS | `_CHAIN.md` | yes | build ×3; `--check` also at commit | yes |
| `_build_memento_index.py` | GM, LS, gauge-log, archives, notes | `_memento-index.json` | yes | build ×3 + in-process gate | yes |
| `_memento_search.py` | index | — | yes | build (`--selftest`) | yes |
| `_gm_move.py` | **any path named in ops JSON** | same, atomic | yes | build (`--selftest` only) — **real mover has no build/CI caller** | yes |
| `_gm_usage.py` | GM, LS, gauge-log | — | yes | build (`--selftest`); live probes inside the gate | yes |
| `_roll_state.py` (new #77) | GM, LS, gauge-log, archives | — (one line) | yes | **wired into build by this session** (was: `--wrap` path only) | yes |
| `_gauge_tokens.py` | chain, token-cache | token-cache | **no** | imported by gate (budgets) | yes |
| `_context_gauge.py` / `_checkin.py` | transcript only — no surface | — | **no** | **nowhere** | yes |
| `_validate_standing_instructions.py` | GM + SPINE | — | **no** | build plain step | yes |
| `_validate_assertions.py` | `_assertions.json` + targets | `_ASSERTIONS.md` | yes — **selftest NOT wired** | build plain step | yes |
| `_build_live_state.py` | LS, `_decision-graph.json` | **LS IN PLACE** (lifecycle splice) + `_LIVE-STATE-CHECK.md` | **no** | build, advisory label → **never gates** | swallowed |
| `_gen_lanes.py` | `_lanes.json`, LS | LS in place (AUTO-LANES) | yes | build ×3 + gate import (BLOCKING) | yes |
| `_build_decision_graph.py` | seed + repo | `_DECISION-GRAPH.md`, `_decision-graph.json` → feeds the LS splice | yes — **selftest NOT wired** | build, advisory → never gates | reports only |
| `_build_consult_index.py` | LS `## OPEN` | `_consult-index.json` | no | build plain step — ⛔ **label misroute, see finding 3** | yes, misreported |
| `gen_runbook_index.py` | runbooks | `_RUNBOOKS.md` (SPINE half) | **no** | build plain step | yes |
| `_measure_tokenizer.py` | chain, GM | — | no | **nowhere** | reports only |
| `tokens/_build_blast_radius.py` | tokens | `_GRAPH-REPORT.md` + json | no | build step 2 — **no reader of the report exists** | yes |
| `_tests/test_gates.py`/`test_advisory.py` | fixtures — **zero handoff cases** | tmp | n/a | CI steps 3–4 | yes |
| `.git/hooks/` | — | — | — | **only `*.sample` — no hook installed** (this clone) | — |
| `memento-package/**/machinery/` ×2 copies | same literals | — | inherited | **nothing runs them** — silent drift vs `knowledge/` | — |
| `outputs/_wrap60_*.py`, `_ops-56.json` | GM/LS/archives via mover | via mover | no | dead one-offs, hardcode a dead sandbox | — |

## Mechanisms that cannot currently fail where it matters

`_git_commit.sh` (no selftest, no runner — and since #74-D1/#77 it is the seam everything
else is delivered through) · `_build_live_state.py` (WRITES the spine, advisory, unproven) ·
`_gauge_tokens.py` (the budget constants every wrap is graded against are unbitten) ·
`_validate_assertions.py --selftest` + `_build_decision_graph.py --selftest` (exist, not in
STEPS) · `_gm_move.py`'s production path (selftest wired, real moves never re-checked) ·
`test_gates.py` "every gate must BITE" carries zero handoff-surface cases.

## Three live findings (beyond the list)

1. ⛔ **`_build_all.py` routes step failures by SUBSTRING LABEL MATCH** — `_build_consult_index`'s
   label contains "surface", so its failure reports as *"dark-surface gate failed — see
   `_DARK-SURFACE-AUDIT.md`"*. Wrong cause, wrong remedy, on a step that reads `_LIVE-STATE.md`.
   The scope-blindness class (`[[scope-blindness-gate-vocabulary]]`): fix = exact step IDs +
   fail loud on unknown label, never enumerate.
2. ⚠ **The spine has an ungated writer:** `_build_live_state.py` splices generated content into
   `_LIVE-STATE.md` with no selftest and an advisory label — a producer that cannot fail,
   writing the handoff's own surface. (Whether it SHOULD gate is Dave's — derivation governance.)
3. ⚠ **Duplicate machinery copies** under `memento-package/` (×2) drift silently against
   `knowledge/` — nothing runs or compares them. Ties to the package boundary ruling (#66).

## Declared blind spots (the sub's, kept verbatim in spirit)

`_gm_move.py` write targets are data not code (ops lists, unenumerable statically) · shell
interpolation + `git add -A` in `_git_commit.sh` make its write set dynamic · constructed
paths and aliased imports escape literal greps · `_to_delete/ _retired/ archive/` excluded ·
prose mechanisms (runbooks, GM itself, `dreamer.md`) produce these surfaces via a human
following steps and have no exit code — outside any table by construction · can-fail cells
read from source, not observed by running · hook absence is proven for THIS CLONE only
(Desktop-side hooks on Dave's machine would be invisible here).
