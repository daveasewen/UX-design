# R4c — eval harness + baseline cold runs · resumable notes (#304, Sat 2026-09-26)

State at hand-back:
- Harness BUILT: `harness/score.py` (+ browser.py, probe.js, selftest.py, build_fixtures.py, profiles/). Selftest PASS (8/8).
- Cold-run briefs WRITTEN: `cold/brief-v1013.md`, `cold/brief-candidate.md` (candidate pack path = `{{CANDIDATE_PACK_ZIP}}`).
- Cold runs NOT RUN: this seat has no Agent tool. The conductor dispatches v1013-r1..r3 (then cand-r1..r3).
- Extra baseline points SCORED: runs/x-292D-oneshot, tr-288P, tr-267, tr-258v1..v5 → runs/compare-extra-baselines.html.
- Static-only calibration runs (trace detector): tr-292D, tr-246A, tr-fitphys, tr-w2A (no scorecard; static.json only).
- runs/_to_delete/: stale stub-gate outputs, QA pngs, a __pycache__ — the mount refuses rm; delete by hand.

Next, when a cold run lands at cold/<RUN>/out/index.html (one seat call each, seat env sourced; repeat until CARD prints):
  python3 notes/_lanes/304/R4c/harness/score.py all --run-id cold-<RUN> --kind "cold run" --label "<RUN>" \
    --pack apollo-spider/dist/Apollo-Spider-v1.0.13.zip \
    --copy-out notes/_lanes/304/R4c/cold/<RUN>/out --page notes/_lanes/304/R4c/cold/<RUN>/out/index.html
Then: score.py compare --runs cold-v1013-r1,cold-v1013-r2,cold-v1013-r3 --out notes/_lanes/304/R4c/runs/compare-v1013.html
