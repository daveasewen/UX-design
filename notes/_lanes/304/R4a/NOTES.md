# R4a resumable notes (#304 Run 4 seat 4a)
- HEAD at start: 6af293df. Old skill blob: HEAD:apollo-spider/skills/generate-from-canon/SKILL.md (314 lines).
- Mechanism confirmed: skills group = paths under apollo-spider/skills/ (gen_pack_manifest _groups 'skills'); reader group arms when VERSION >= READER_SHIPS_FROM (v1.0.14). Builder reads a COMMIT via git archive -> candidate must be built in a scratch clone with the overlay committed there and VERSION set to v1.0.14 in the clone only.
- Reader has no overlay flag -> drafts do NOT ride in the candidate.
- Steps: [1] skill rewrite  [2] drafts  [3] build_candidate.sh  [4] checks  [5] report
- DONE [1] skill rewritten (350 lines); [2] drafts + check_drafts.py 7/7 arms PASS; [3] candidate built, reproducible
  (zip sha 2e827237…, manifest 81e640e5…, candidate commit d3578c68 over 6af293df); [4] verify_skill.py C1–C7 PASS.
- Findings to carry: stamp block rewrites 3 historical rulings in knowledge/_rulings.json (--check RED); knowledge/brain/
  not shipped; canon role-vars emit legacy only, so data-apollo-theme="common" gets mono's 40/4 dashboard gutters.
- Report: notes/_subreports/2026-09-26-304-R4a-skill-composes.md
