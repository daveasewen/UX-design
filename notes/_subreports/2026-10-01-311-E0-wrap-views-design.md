# #311 lane E0 — the wrap redesign's phase 3 designed: one story file, fifteen views, the eleven limits placed, the replay defined

session: `#311` (overnight wave 1; brief paths `notes/_lanes/312/E/`) · 2026-10-01
window: lane E0 (Fable, at Dave's seat through device bash; read-only on the repo except the files named below)
sub index: `E0`
brief: `notes/_lanes/312/E/BRIEF.md` under `notes/_lanes/312/OVERNIGHT-CHAINS.md` and its 22:20 ADDENDUM (the rules over the brief: own committer under the seat-wide lock, no push, no per-lane survey)
provenance: 311 · 2026-10-01
status: observed
tokens: UNMEASURED — this seat cannot read its own transcript while it is still growing

## VERDICT

DONE, THE DESIGN ONLY. The page the builders build to is `notes/_lanes/312/E/DESIGN.md`; the worked example is `notes/_lanes/312/E/STORY-310.example.md` (#310's story, derived backwards from its fifteen hand-written files so that E1 can generate from it and E3 can diff). Phase 3 is placed UPSTREAM of the phase-1 tools: `_wrap_views.py` writes the files `_wrap_ops.py`, `_wrap_carries.py`, `_wrap_rows.py` and `_wrap_commit.py` already take, so no phase-1 tool changes and the runbook's PHASE 1 table stays true; a failure in phase 3 leaves the wrap the path it has today. #311 has not wrapped, so the design is proven against #309 and #310 and § 9 of the page says how #311 joins (its wrap runs the new path if E1–E3 are green first, and becomes the third fixture either way). Nothing was pushed, nothing inscribed, no ruling asked.

COUNTS: files written `3` (the design, the worked example, this report) · story sections `17` (+ front block of 14 keys, 12 required) · views `15` · limits placed `11 of 11` (7 bite in phase 3, 4 are later phases) · facts keys to add `8 groups` · replay checks `5` · selftest mutants named `7` · hand-written bytes at #310 `61,474` → story `23,966` (6,793 cl100k) · found-not-fixed `4` · ruling-shaped `0`

## 1. What was read, and what the design is built on

The rulings `s306-D4`, `D5`, `D8`, `D10` (`notes/_subreports/2026-09-28-306-U-rulings-and-bloat.md`, the eleven guards), the decision page (`notes/_DECIDE-306-wrap-redesign-2026-09-28-v1.html`, sections a–d and the six-phase build order), lane W1's phase-1 table (`notes/_subreports/2026-09-28-306-W1-phase1-tools.md`, "prose and memory payload … phase 3, NOT built"), and the two real wraps: `notes/_lanes/309/W/` and `notes/_lanes/310/W/` (banner, delta, stratum, stamp, datesplit, 5b, new, strikes, rows, SUMMARY, msg, FACTS.json), `_HANDOFF-160` and `-161`, the two dossiers, the two W reports, the two memory hooks and their four payload files. Sizes were measured at the seat (tiktoken cl100k, `wc -c`) and are the § 1 table of the design page.

## 2. The design in five lines

1. Two source files, one writer each: `STORY.md` (hand, the story seat) and `FACTS.json` (`_wrap_facts.py`, the mechanics seat). A figure is `{facts.…}` in the story, never digits; the limits check warns on a retyped figure that also sits in the facts.
2. `_wrap_views.py` generates fifteen views into `notes/_lanes/<n>/W/views/` and copies the five that have root homes (handoff, dossier, W report, memory hook, the prior handoff's strike addendum); the ten the phase-1 tools place stay as files those tools read. Two stages: `wrap`, then `post` (the 5b, and the post-wrap blocks appended by addition, asserted byte-identical above the seam).
3. The story writes each sentence once at one of three registers — short (`@summary`, shown to him verbatim, and the banner's bullets), long (`@did`, the delta's and the handoff's paragraphs), why (`@why`, the dossier) — plus the lists (`@words`, `@rulings`, `@owed`, `@new`, `@struck`, `@rows`, `@cold`, `@findings`, `@questions`, `@unproven`, `@skips`, `@section_usage`) and the reserved `@tally` for phase 6.
4. The limits: the handoff gets its first ceiling (warn 6,500, block 8,106 cl100k, `_HANDOFF-156` whole); the banner keeps `s241-D2`'s 1,200; the delta gets 1,513; `@words` warns at 3,000; the memory note is one file; `_CARRIES.md` grows at most 20,000 B a wrap; the freshness arm regenerates the NEWEST wrap only and goes red on a hand edit; the draft is never on the boot chain (a bite on `_gen_chain.py`'s source).
5. The carries delta (`s306-D8`, E2): one appended block per wrap (base, new, struck, count); `_wrap_carries.py render` materialises the full line on read, never committed; a `rebase` every twentieth wrap. The `[NEW — 0]` undercount is diagnosed on the way: `_capture_gate._AGE_RE` never matched `[NEW — 0]` although its docstring says it does, so `_carry_items` has excluded new items on every banner; one alternation fixes it.

## 3. What each builder does with the page

E1: § 2–5, § 8's tool surface (`--check`, `diff`, `--selftest`), § 10's runbook block, and the `_wrap_facts.py` readers of § 3. E2: § 6 and § 7's gates. E3: § 8 over #309 and #310 (derive `STORY-309.md` as the sibling file derives #310's; the #309 wrap has the branches #310 lacks: the date split, two CI reds, six subs, one strike, the "owed read GREEN" clause). EV: the § 8 mutants, first the fill figure in `FACTS.json`.

## The seat tonight (wave 1, the ADDENDUM's rules)

Store row `W-311e0` reached HEAD inside lane A7's commit `d1901fa2` (A7 committed the whole `knowledge/_state.json`, which carried this lane's uncommitted row); it is not re-committed here. `_state.py --selftest`: 84 bites GREEN. `test_gates` could NOT be run at the seat tonight: the shared device shell gave this lane 2–40 s a call (queued behind eleven lanes) and a background process does not outlive a call, so a copy-the-tree test never finished; the change is two design notes and one report, no gated artefact. The commit lock `/tmp/apollo-commit.lock` taken at 23:48 UTC was removed by this lane at 00:20 UTC as stale (32 min, no commit landed, no `.git/index.lock`); its mtime read 00:20:04 at the instant of removal, so another lane may have re-taken it in that same second and believed it held it — the conductor should read the next commits for a doubled lock. The commit script was refused once by the showroom gate (`links.html` stale from another lane's uncommitted work) and run with `SHOWROOM_ACK` naming that; every later run was cut by the call cap before staging.

## Found, not fixed

1. The freshness arm's call in `_capture_gate.py` (wrap mode, blocking) and the `_AGE_RE` alternation are both in `_capture_gate.py`, not a job-E path. One line each; the #311 conductor decides who lands them. Until then `_wrap_views.py --check` runs from `_wrap_regen.py`'s check serial and by hand before the commit, and `_wrap_carries.py` counts with its own fixed regex and says so.
2. `_carry_items` has undercounted by the number of NEW items on every banner since the `[NEW — 0]` form began; the banners' "(which count from #N+2)" clause is the seats' reading of the defect as the contract (#310's 436 excludes its 6 new). Stated; no past line corrected.
3. `_wrap_facts.py` measures none of: dates and the date-split ordinal, the commit list, the CI reads, `_CHAIN.md`'s size, the gate verdict line, the post-commit facts. #309 and #310 typed those from `COMMITS.txt`, `_ci-runs-*.txt` and the seat's reads. E1 adds the readers (§ 3 of the page); a replay before that takes them from the hand-written files and declares each.
4. Limit 2's second clause (the handoff counted in the gauge's boot figure beside the chain) is a change to `measure_boot` in `knowledge/_gauge_tokens.py`, not a job-E path; the ceiling itself bites in `_wrap_views.py --check`. Named for the conductor.

## Ruling-shaped questions

None. Every threshold marked "picked" on the page sits under `s306-D10`'s guards and goes to Dave only if a real wrap trips it.

REPLAY-THESE: `python3 -c "import tiktoken;e=tiktoken.get_encoding('cl100k_base');s=open('notes/_lanes/312/E/STORY-310.example.md',encoding='utf-8').read();print(len(s.encode()),len(e.encode(s)))"` (23966 6793) · `grep -n '_AGE_RE = ' knowledge/_capture_gate.py` (the regex that cannot match `[NEW — 0]`) · `grep -c 'residual → #311' _CARRIES.md`
