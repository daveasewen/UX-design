# Lane A7 (#311 overnight wave 1, Sonnet chore lane) - the hit-area advisory wired into CI, and the status stamps

COUNTS: hit-area advisory regenerated on 137 snippets (3,357 targets measured, 1,045 findings, 1,084 exempt, 0 fonts unasserted) · CI render job now names `_validate_hit_area.py` (selftest + sweep, advisory, report uploaded) · 10 rulings stamped enacted, each checked against the tree first · s308-D42 already enacted (879f9aae), left alone · verdict: DONE, nothing held back.

## What was built

1. The advisory, regenerated. `_validate_hit_area.py --all` at the seat (two halves of the snippet list, because one sweep takes about 163 s and a call may not outlast 178 s). Output merged through the script's own `render_report`: `knowledge/_HIT-AREA-ADVISORY.md`. First line now says it was regenerated #311 A7; the old "NOT wired into _build_all.py" wording was stale since #209 and is corrected in the generator and the report. The script's `--selftest` passed first (6 of 6 known cases). Two full runs gave 1,047 and 1,045 findings (a sub-0.2 percent wobble between runs; the report carries 1,045).
2. CI wiring. `.github/workflows/gates.yml`, `render` job: two new steps after the probe registry. The sweep step runs `--selftest` then `--all --out knowledge/_HIT-AREA-ADVISORY.md`, `continue-on-error: true` (ADVISORY, its own tier), and an `always()` upload of both logs and the report. A dated SEVENTH ENTRY comment says why. The `gates` job still runs the build step and still gets the declared 77 there; that is unchanged. YAML parses (jobs: gates, render, release). `_validate_wiring.py` still passes.
3. The docstring's TIER paragraph in `_validate_hit_area.py` said "deliberately not wired"; it now says what is true.

## Stamps (each found in the tree before it was stamped)

- s308-D16 (one edge register) and D17 (ends checked): `a7742aee`. `knowledge/_edge_register.json` exists (now 64 rows), `_validate_edges.py --coverage` OK with 0 refusals, `--check` 11,695 edges, 0 fail.
- s308-D18 (one direction stored) and D19 (each type's shape said, self-lines moved): `6bb91a0b`. hasPart is `RETIRED_EDGE_TYPES` in gen_kg_edges.py and `stored:false` in the register; every row has `opposite` and `shape`; `--check` reports shape none; 7 metas carry `count` and 9 carry `covers`; selftest 34 arms green.
- s308-D39, D40, D41, D43, D44: `94ba3c73` (batches a to d `d84169d3`..`4abdb8eb` carry the kind lines). `$containers` block present with the five kinds, terms and four limits; 137 of 139 metas declare a `kind`, the other two (limits-meter, progress-bar) are alias seats, which the rule excepts; `--check` EDGE ACCEPTS passes, selftest arms 26 to 34 green; the role reads `chart` in roles.json with `$renamedFrom: chart-panel`; `$containers.rulings` carries D44 (housing for holder, cell the grid position only).
- s310-D2: `7bc6b0c5`. The dashboard's Net FX exposure tile carries `.up-is-bad` and its down arrow.
- s308-D42 was already `enacted` with `879f9aae`; not touched.
Each stamp went through `_inscribe_ruling.py --set-status ... --write`, inside the seat-wide lock; every one printed "reconstruction proof PASSED". Then `gen_kg_titles.py --write` (851 rulings titled, 0 untitled) and `_render_rulings.py`.

## Gates run

`_validate_hit_area.py --selftest` (pass), `_validate_edges.py --coverage / --check / --selftest` (pass), `_validate_wiring.py` (pass), YAML parse of gates.yml. `test_gates` is run before the commit, in the lock; its verdict is in the commit step below.

## Found, not fixed

- Two metas without a `kind` (limits-meter, progress-bar) are alias seats and correctly excepted; nothing to do.
- The D42 row was already stamped; the brief's range "D39..D44" includes it only as already done.
- The advisory's 1,045 findings stand: 819 control and 226 mark. Remedy and promotion to BLOCKING are Dave's (the script header and the gates.yml comment say so). The worst are text links and buttons measured at 10 to 16 px tall (Template-detail `a.crumb`, List-items `input#dense`, Cards `a.arrow`, Modals `button#open`).
- The CI `render` job has never run this step; the first GitHub run is the proof. Declared, not claimed.

## Ruling-shaped questions

- Should the hit-area sweep become BLOCKING once the 819 control findings are triaged, or stay advisory? Dave's call; nothing is proposed here.
