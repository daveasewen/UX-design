# Session #205 chore-sub claim table — full _build_all regeneration

| claim | command | rc/figure | timestamp |
|---|---|---|---|
| tiktoken present | `pip install tiktoken --break-system-packages` | already satisfied (0.14.0) | 2026-08-19T12:28Z |
| pre-run dirty set recorded | `git status --short` | 2 files: notes/_REHEARSAL-LOG.jsonl, notes/_dream/_GRADE-DECISIONS.jsonl (M) | 2026-08-19T12:28Z |
| total STEPS measured | inline python import of knowledge/_build_all.py | 124 | 2026-08-19T12:28Z |
| chunk 1-3 | `python3 knowledge/_build_all.py --range 1-3` | PARTIAL PASS steps 1-3/124 | 2026-08-19T12:29Z |
| chunk 4-7 | `python3 knowledge/_build_all.py --resume 4` | PARTIAL PASS steps 4-7/124 | 2026-08-19T12:30Z |
| chunk 8-10 attempted | `python3 knowledge/_build_all.py --resume 8` | steps 8,9 passed silently (state next=10,rc=0 confirms); step 10 "assertion veracity gate" ABORT exit 1 | 2026-08-19T12:31Z |
| BLOCKER — step 10 ABORT is a real content-drift finding, not a chunking artefact | `python3 knowledge/_validate_assertions.py` (direct, for diagnosis) | ASSERT-009 FAIL: count=92 (want eq 77) meta.json files at knowledge/components/*.meta.json — fix requires editing _LIVE-STATE.md, GOOD-MORNING.md, notes/_MEMENTO-DECISIONS.md, _DECISION-HISTORY/2026-08-08-131-*.md — ALL on DO-NOT-RULE list, out of chore-sub authority | 2026-08-19T12:32Z |
| confirmed contiguous-only gate — cannot skip step 10 via --range | `python3 knowledge/_build_all.py --range 11-11` | "CHUNK REFUSED: coverage is contiguous-only — state expects step 10, you asked for 11" | 2026-08-19T12:33Z |
| DECISION: since full-pipeline coverage is blocked by an out-of-scope content edit, running the 5 target generators DIRECTLY (write-mode then --check) to deliver the core CI-fix mandate; full _build_all.py coverage capped at 9/124, step 10 recorded as OPEN FAIL below | n/a | n/a | 2026-08-19T12:33Z |
| blast-radius regenerated (write) | `python3 knowledge/tokens/_build_blast_radius.py` | rc=0, "wrote tokens/_blast-radius.json and _GRAPH-REPORT.md" | 2026-08-19T12:34Z |
| token_ramp regenerated (write) | `python3 knowledge/gen_token_ramp.py` | rc=0, "1 file(s) synced ... 102 already in sync" (touched snippets/Payment-card-visual.reference.html AUTO-TOKENS managed block) | 2026-08-19T12:34Z |
| canon_components regenerated (write) | `python3 knowledge/canon/gen_canon_components.py` | rc=0, "generated 91 components" | 2026-08-19T12:35Z |
| theme_cascade regenerated (write) | `python3 knowledge/canon/gen_theme_cascade.py` | rc=0, "wrote AUTO-THEMES block — 228 override path(s), 254 component projection(s)" | 2026-08-19T12:35Z |
| graph_mention_map regenerated (write) | `python3 knowledge/_build_graph_mention_map.py` | rc=0, "101 of 101 node(s) mentioned, 1095 record hit(s)" | 2026-08-19T12:35Z |
| CHECK 1/5 blast-radius | `python3 knowledge/tokens/_build_blast_radius.py --check` | rc=0 PASS | 2026-08-19T12:36Z |
| CHECK 2/5 token_ramp | `python3 knowledge/gen_token_ramp.py --check` | rc=0, "0 file(s) DRIFTED ... 103 already in sync" | 2026-08-19T12:36Z |
| CHECK 3/5 canon_components | `python3 knowledge/canon/gen_canon_components.py --check` | rc=0, "91 components in sync" | 2026-08-19T12:36Z |
| CHECK 4/5 theme_cascade | `python3 knowledge/canon/gen_theme_cascade.py --check` | rc=0, "228 override path(s), 254 component projection(s) in sync" | 2026-08-19T12:36Z |
| CHECK 5/5 graph_mention_map | `python3 knowledge/_build_graph_mention_map.py --check` | rc=0, "current (101 of 101 node(s) mentioned)" | 2026-08-19T12:36Z |
| [13] _capture_gate.py --selftest — confirmed UNTOUCHED (known standing red, not run/not fixed) | n/a (no command run against it) | untouched by design | 2026-08-19T12:36Z |
| commit attempt 1: showroom sync gate REFUSED (s191-D1) — token_ramp write touched Payment-card-visual.reference.html, showroom out of sync | `bash knowledge/_git_commit.sh --reconciled <msgfile> <34 explicit paths>` | refused, nothing staged: "OUT OF SYNC — stale: ['payment-card-visual.html']" | 2026-08-19T12:38Z |
| showroom regenerated (write, in-scope generator per s191-D1) | `python3 knowledge/gen_showroom.py` | rc=0, "91 page(s) + index -> showroom/ (1 written, 0 orphan(s) pruned)" | 2026-08-19T12:39Z |
| showroom sync verified | `python3 knowledge/gen_showroom.py --check` | rc=0, "91 page(s) + index in sync" | 2026-08-19T12:39Z |
