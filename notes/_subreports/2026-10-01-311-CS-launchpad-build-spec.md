# `#311`-`CS` — Launchpad, day one: the build spec the three build lanes build to

session: `#311` · 2026-09-30 (overnight wave 1; the brief says #312, read #311 per `notes/_lanes/312/OVERNIGHT-CHAINS.md`)
window: overnight wave 1, lane CS (Fable, cloud, working at the seat through device_bash)
sub index: `CS`
brief: `notes/_lanes/312/C/BRIEF.md` (lane CS's line only) under `notes/_lanes/312/OVERNIGHT-CHAINS.md` and its 22:20 addendum
tokens: `UNMEASURED — message.usage is not readable from this seat`

## VERDICT

DONE. One page, `notes/_lanes/312/C/SPEC-launchpad-day-one.md` (30,203 bytes), fixes what the brief asked for: the catalogue's shape for the dashboard set, the tool surface (seven tools, four mock roles, scopes, the £500,000 limit), the record per screen, the folder layout under `apollo-launchpad/`, and the tests each of steps one, three and four must pass (T1.1–T1.7, T3.1–T3.6, T4.1–T4.6), plus the worked example as the one shared fixture. Every shape is lifted from the proposal v2, the R5 probe and the #305 rulings; the eleven places where a build lane needed a name or number neither source gives are marked **[spec]** on the page. Nothing was built, nothing inscribed, no meta, schema or canon file touched. One finding matters to C1 and C4 tonight: the probe's derived dashboard set is stale by one ruling — `stat-card` and `kpi-tile` became aliases of `metric` at #309 (`s308-D42`, commit 879f9aae) — so the published set is 17, not 18, and the chooser must resolve aliases.

COUNTS: findings `4` · ruling-shaped `0` · UNPROVEN `2`

## What was done

- Read, in order: `notes/_lanes/312/OVERNIGHT-CHAINS.md` with its addendum; `notes/_lanes/312/C/BRIEF.md`; `notes/_PROPOSAL-apollo-mcp-2026-09-26-v2.html` (text extracted; § The proof of concept, § Four mock roles, § Worked example, § The build path, § What exists today, § Risks); `notes/_subreports/2026-09-26-304-R5-mcp-probe.md`; `notes/_lanes/304/R5/SPEC-when-evaluator.md` and the R5 catalogue's entry shape; `notes/_DECIDE-304-schema-2026-09-26-v1.html` (the illustrated field names for `s305-D17`/`D18`); the rulings `s294-D10`, `s305-D15`–`D23`, `D40`, `D45`–`D54`, `D58` from `knowledge/_rulings.json`; the metas of the 19 derived parts and `metric.meta.json`; `knowledge/_validate_screen.py`'s gate list and the signatures of `_validate_composition.check(html)`, `_validate_compose.check_screen(path)`, `_validate_a11y.check(fp)`; `knowledge/shapes.json` (23 shapes), `knowledge/when-fields.json` (44 fields), `knowledge/roles.json`'s header.
- Wrote `notes/_lanes/312/C/SPEC-launchpad-day-one.md`, thirteen sections: what binds and what tonight is; folder layout; vocabulary; the dashboard part set; the catalogue's shape; the tool surface; the gate and the chooser; the record; the worked example as fixture; the renderer stretch; tests; dependencies and seats; what the page did not decide.
- Filed this report with a born-closed store row (`s305-D40` form).

## Findings

1. **The derived dashboard set moved since the probe.** `knowledge/components/stat-card.meta.json` and `kpi-tile.meta.json` now read `aliasOf: component:metric` ("ENACTED #309 lane C per s308-D42 and s309-D2"; `git log` on kpi-tile: 879f9aae). The probe's 18 included both as parts. The spec publishes `metric` once with `aliases: ["stat-card","kpi-tile"]`, drops `view-options` (deprecated, when-rule NEVER, per the probe), and adds `template-dashboard-bento` as the wall (`s305-D18`): 17 published. C1 derives the count by script; the page says the table is not the source.
2. **Six of the probe's seven "decisions for Dave" are now ruled**, so the spec cites them rather than re-asking: `s305-D15` (states), `s305-D17` (own words), `s305-D18` (the wall), `s305-D19`+`D58` (setting or slot), `s305-D21`/`D22`/`D23` (chart-line clauses, variant B, data-grid `needs`), `s305-D54` (motion per part), `s305-D20` (beta parts in, marked proposals). Probe: `## Decisions for Dave` 1–7; rulings: `knowledge/_rulings.json`.
3. **`knowledge/roles.json` and the PoC's "roles" are two vocabularies.** roles.json is the `provides` tier (12 slugs, `s252-D1`); the proposal's four are banking roles. The spec names them "provides role" and "mock role" and forbids a bare `role` (§ 3), the vocabulary-collision class of #202.
4. **Two static gates still take a path, not a string.** `_validate_compose.check_screen(path)` (line 118) and `_validate_receipt` (step 0 of `_validate_screen.py`); `_validate_composition.check(html)` and the a11y check already take strings. The spec has C3 write those two to `/dev/shm` and declare it, and lists the `check_text()` splits under canon as later work (§ 13 item 4) — canon is not job C's.

## Found, not fixed

- The R5 catalogue's `catalogId` is on `apollo.invalid`; the real domain is nobody's yet. The spec keeps the reserved domain at `v0.1.0` and lists the domain as a later question.
- The proposal's "the graph keeps a record" has no home in the KG build; the spec makes the file the record tonight and lists the node kind as later.
- `layout-utilities` sits in the derived set by the template's `$composes` but is not the container after `s305-D18`; left in, flagged (§ 13 item 5).
- `/tmp/apollo-commit.lock` was held by another lane at 21:18 UTC when this lane first looked (stat 21:18:19); not stale.
- **This lane's own slip, disclosed.** The store row `W-311s1` was written to `knowledge/_state.json` at about 21:37 UTC **outside** the seat-wide commit lock, against addendum rule 2. Lane A7 held the lock at the time and its `_git_commit.sh --reconciled` staged the whole store, so the row rode into A7's commit `d1901fa2` (`git show d1901fa2:knowledge/_state.json | grep -c W-311s1` → 1) before this report existed in the tree. No harm found (A7's gates passed and the commit landed), but the #311 conductor should know that commit carries one row that is not A7's. This lane's own commit therefore names only its two files.
- `knowledge/_tests/test_gates.py` could not be run in this lane's first pass: every `device_bash` call was being cut at about 15–25 s regardless of `timeout_ms` (a bare `sleep 35` was killed at 23.6 s), and the first pass ended before its commit, leaving the page and this report uncommitted in the working tree. A second pass of the same lane (22:20 UTC) found full call windows again, ran the suite at the seat (`TMPDIR=/dev/shm`, 22:22:14 → 22:24:36 UTC, log `/dev/shm/cs-test-gates.log`): **36 test(s), 0 failure(s)**, state-contrast and `--render` skipped by design. This lane's change is two Markdown files under `notes/`; the one gate that reads them, `knowledge/_gate_doc_rows.py`, runs inside `_git_commit.sh`.

## RULING-SHAPED QUESTIONS

**None.** The brief says Dave has no moment tonight, and nothing on the page needs his word before the build lanes run. The five later questions are listed on the page (§ 13) for the next sitting page, priced by what the lanes measure.

## UNPROVEN / CLAIMED (ADR-0016)

- **UNPROVEN:** that C0's committed field names match the decision page's illustrations (`label`, `title`, `items`, `rows`, `trail`, `tiles`). The spec tells C1 to read them from C0's sha, not from the page — price to prove: one `git show` of C0's commit when it lands.
- **UNPROVEN:** the expected L2 count of 17 of 17 for the published set after `s305-D15`/`D16`; the probe measured 13 of 18 before those landed. C1's T1.3 measures it.
- **CLAIMED:** the probe's figures quoted on the page (137/137, 61 ms, 0.27 ms, 1.6 s, 19 of 20) are read from the R5 report and `s305-D21`, not re-run tonight.

## Evidence

No evidence files: every claim above quotes its probe inline; the deliverable is `notes/_lanes/312/C/SPEC-launchpad-day-one.md`.

REPLAY-THESE: `notes/_lanes/312/C/SPEC-launchpad-day-one.md` § 4 and § 11 (~2,500 tk) — the part-set change and the tests are what C1, C3 and C4 must read in full.
