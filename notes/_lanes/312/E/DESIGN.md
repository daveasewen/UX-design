# Lane E0 — the design phase 3 is built to: one story, written once, every view generated

session: `#311` (overnight wave 1, brief paths `notes/_lanes/312/E/`) · 2026-10-01
lane: E0 (Fable, design only; nothing here is code)
brief: `notes/_lanes/312/E/BRIEF.md` under `notes/_lanes/312/OVERNIGHT-CHAINS.md` and its ADDENDUM
ruled by: `s306-D4` (story plus measured figures, all views generated), `s306-D5` (the generated wrap report is the filed report), `s306-D8` (carries as changes), `s306-D10` (lane U's eleven limits), `s306-D9` (later: the seam writes the draft)
fixtures: the #309 and #310 wraps as they were hand-written (`notes/_lanes/309/W/`, `notes/_lanes/310/W/`, `_HANDOFF-160`, `_HANDOFF-161`, the two dossiers, the two W reports, the two memory hooks). #311 has not wrapped; § 9 says how it joins.
worked example: `notes/_lanes/312/E/STORY-310.example.md` — #310's story, derived backwards from its hand-written views, so E1 can generate from it and E3 can diff.

E1 builds § 2–5 and § 8; E2 builds § 6 and § 7; E3 runs § 8; EV attacks § 5 and § 8. Where this page and a builder's judgement differ on a detail, the builder writes the difference in its report under `## Found, not fixed`; nothing here is Dave's ruling except the rulings named above.

---

## 0. The shape in one paragraph

The wrap seat writes ONE file by hand, `notes/_lanes/<n>/W/STORY.md`, and measures ONE file by tool, `notes/_lanes/<n>/W/FACTS.json` (`_wrap_facts.py`, built at #306). A new tool, `knowledge/_wrap_views.py`, reads both and writes every other file the wrap produces, into `notes/_lanes/<n>/W/views/`, and from there into their homes. The phase-1 tools do not change: `_wrap_ops.py` still takes `banner.md`, `stratum.md`, `delta.md`, `stamp.md`, `datesplit.md`, `5b.md`; `_wrap_carries.py` still takes `new.txt` and strike files; `_wrap_rows.py` still takes `rows.json`; `_wrap_commit.py msg` still takes a message file. Phase 3 sits UPSTREAM of phase 1: it writes those inputs instead of a person writing them. So the runbook's PHASE 1 table stays true, and the wrap seat's first command becomes `_wrap_views.py`. A figure lives in `FACTS.json` and nowhere else; a sentence lives in `STORY.md` and nowhere else; the story names a figure as `{facts.fill.now:,}` and never types it. The gate's new arm regenerates the newest wrap's views in memory and compares them with disk, so a hand edit to a generated file goes red, and each view is measured against its limit before anything moves.

Why this and not "the handoff is the story" (his option b, not taken): today the handoff, the dossier and the W report share no sentence over 60 characters (lane R, #306), and 24 of 27 facts were hand-written in five or more places. The story is smaller than the handoff (it holds each sentence once, at one register) and the handoff becomes the largest VIEW, under a ceiling for the first time.

---

## 1. What each hand-written file of the #310 wrap was, and what it becomes

Measured on the #310 wrap's own files (cl100k by tiktoken at the seat, 2026-10-01; bytes by `wc -c`).

| hand-written today | B | cl100k | becomes | written by |
|---|---|---|---|---|
| `banner.md` | 2,271 | 741 | view `banner` | generated from `@summary`, `@owed[0]`, facts |
| `delta.md` | 3,170 | 1,068 | view `delta` | generated from `@did`, facts |
| `stratum.md` | 5,685 | 1,820 | view `stratum` | generated from facts, `@skips`, `@section_usage` |
| `stamp.md` | 675 | 222 | view `stamp` | generated from front block, facts |
| `datesplit.md` (#309 only) | 617 | 228 | view `datesplit` | generated from facts `dates` |
| `5b.md` | 473 | 167 | view `5b` | generated from facts `post` |
| `_HANDOFF-161-…md` | 14,863 | 4,622 | view `handoff` | generated from every section |
| `_DECISION-HISTORY/2026-09-30-310-…md` | 5,770 | 1,385 | view `dossier` | generated from `@why`, `@resolved` |
| `notes/_subreports/2026-09-30-310-W-wrap.md` | 6,997 | 2,236 | view `report` | generated from facts, `@findings`, `@questions`, `@unproven` |
| `WRAP-MEMORY-HOOK.md` + `memory_{front,body,file,indexline}` (5 files, the body three times) | 4,106 + 7,167 | 1,169 + ~2,000 | view `memory` (one hook file that CONTAINS the payloads once; the placer cuts from it) | generated from front block, `@summary`, `@owed`, facts |
| `new.txt` + `strike-1..4.txt` | 2,807 + 1,737 | 846 + 559 | view `carries` (`new.txt`, `strike-<k>.txt`, and from E2 on the `_CARRIES.md` delta block) | generated from `@new`, `@struck` |
| `rows.json` | 2,635 | 857 | view `rows` | generated: the four mint ops from the front block; close/note ops from `@rows` |
| `_msg-W1.txt` | 1,378 | 473 | view `msg` | generated from front block, facts, `@summary` |
| `SUMMARY.md` | 1,740 | 435 | view `summary` | `@summary` verbatim |
| the STRUCK addendum appended to `_HANDOFF-160` | — | — | view `prior-strikes` (appended by addition to the previous handoff) | generated from `@struck` |

Fifteen hand-written files (61,474 bytes at #310 by `wc -c`, the memory body written three times among them) become one story of 23,966 bytes / 6,793 cl100k (the worked example, measured at the seat) plus one measured JSON. Nothing is typed twice.

---

## 2. `STORY.md` — the one file the story seat writes

Plain Markdown. A front block of `key: value` scalars between `---` lines (no YAML library: split on the first `:`; a value is a string; `null` is null), then sections opened by `## @name`. Unknown sections are refused by name (a typo does not silently vanish). Sections may be empty; the empty ones are listed in § 2.3. The parser is `_wrap_views.py`'s; the grammar is this page.

Figures: any `{facts.<dotted.path>}` inside any value or section is resolved against `FACTS.json` with Python format specs allowed (`{facts.fill.now:,}` → `372,194`; `{facts.rulings.total}` → `849`). A path that does not resolve is an error, never blank. Derived values (§ 4) are addressed as `{d.<name>}`. A figure typed as digits inside a story sentence is allowed (the story seat may quote a lane's figure that no tool measured) but the limits check WARNS on any run of 5+ digits with a thousands separator that also appears in `FACTS.json`, naming the placeholder it should have been. That is the "never retype" rule as a measurement.

### 2.1 The front block

```
---
session: 310
headline: the dark tiles were built, and the soft white waits to be seen
one_sentence: THE ARROW AND THE DARK GROUND WERE RULED, THE BLACK TILES WERE BUILT, AND THE SOFT WHITE AND THE TAB STRIP WAIT TO BE BUILT AND SEEN
opened_word: Good Morning!
wrap_word: wrap
wrap_word_context: answering the conductor's *"Yours: wrap now?"* after it reported the fill past the hard line
conductor: Opus 5.5, a CLOUD session linked to Dave's computer
wrap_seat: delegated, Opus 5.5
lanes: A dark tiles (Opus 5.5) · B white ink and tab strip (Opus 5.5)
first_beat: READ THE `CI owed:` LINE AT THE FOOT, THEN BUILD `s310-D7` AND `s310-D8` AND SHOW HIM
next_title: Apollo - #311: the soft white and the tab strip, built and shown
words_files: notes/_lanes/310/DAVE-WORDS-2026-09-30-1403.md · notes/_lanes/310/DAVE-RULINGS-2026-09-30-1443-the-dark-ground.md · notes/_lanes/310/DAVE-WORDS-2026-09-30-1624.md · notes/_lanes/310/DAVE-RULINGS-2026-09-30-1735-white-ink-and-tab-strip.md
lane_reports: notes/_subreports/2026-09-30-310-A-dark-tiles.md · notes/_subreports/2026-09-30-310-B-white-ink-and-tab-strip.md
prior_handoff_struck: 1, 2, 3, 7
---
```

Every key is required except `wrap_word_context` and `prior_handoff_struck`. `headline` is lower case; the generator derives the CAPS form and the slug (§ 4). Times and dates are NOT in the front block: they are facts (`facts.dates`, § 3). Lists use ` · ` as today's files do.

### 2.2 The sections, in the order the story seat writes them

Each item line starts `- `. A leading mark (`★★★`, `★★`, `★`, `⚠`, `⛔`, `✅`, `⬛`) is the item's rank and is carried into every view that ranks. `[DAVE'S]` after a title means the item is his. The em dash ` — ` separates a title from its body wherever a title exists (the `s128-D2` shape the carry gate keys on).

| section | what one item is | feeds |
|---|---|---|
| `## @words` | `- HH:MM — his line verbatim *(context)*`, or `- HH:MM — export `path`: what each call chose, quoted`. Chat lines only; exports are cited by path and quoted call by call, never copied whole (limit 4). One item per message. | handoff HIS WORDS; the delta's quotations; memory body's quotations; the dossier's quotations |
| `## @rulings` | `- `sNNN-Dk` — his phrase, verbatim, in quotes — what it means in one clause — RULED|ENACTED|RULED NOT ENACTED`. The id and count come from facts; the gloss is the story. Order = the file's. | banner ①; summary Decisions; memory What landed; handoff's rulings line |
| `## @summary` | three sub-lists `### decisions`, `### outputs`, `### problems`, each 1–4 short lines in Dave's register (no ids, no shas, plain words; `s305-D63`). Written ONCE here and shown to him verbatim. | `SUMMARY.md` verbatim; banner ②③ (outputs, problems); memory What landed; the commit message's bullets |
| `## @did` | topic blocks: `### TITLE IN CAPS` then one paragraph, shas in backticks, his words in *"…"*. 3–6 blocks. | delta paragraphs (`> ★★ **TITLE.** para`); handoff WHAT THE SESSION DID (`- **Title.** para`) |
| `## @problems` | `- ⚠ sentence` — the session's reds and breaches in prose (the figures are facts) | delta's ⚠ paragraph; handoff cold-seat list (new lines); summary is NOT fed from here (it has its own) |
| `## @owed` | ordered `- MARK owner: **question?** — body`; owner ∈ `mine`, `dave`, `future`, `found`, `standing`. Item 1 is the first beat. | handoff OWED; memory OPEN (items 1–4); banner residual first item; `@new` items are usually the same questions — see the rule below |
| `## @new` | `- MARK **TITLE IN CAPS** [DAVE'S] — body` — the items entering `_CARRIES.md`. The generator inserts `[NEW — 0]` / `[NEW — 0, DAVE'S]`; the story never types an age. | `new.txt`; the `_CARRIES.md` delta (E2) |
| `## @struck` | `- **TITLE AS IT STANDS IN _CARRIES.md** — VERDICT — receipt sentence` with VERDICT ∈ ANSWERED, BUILT, DECIDED, DROPPED, SUPERSEDED. | `strike-<k>.txt` (the `s183-D1` form); the prior handoff's STRUCK addendum; banner's "k STRUCK (…)"; the `_CARRIES.md` delta |
| `## @rows` | `- close W-309g2 — receipt sentence` · `- note W-309g4 — paragraph` · `- reopen W-… — why`. The four mints (h, dh, w, wk) are derived; never written here. | `rows.json` |
| `## @cold` | `- ⛔★★ **LESSON IN CAPS.** sentence` — the lines this session adds to the cold-seat list. The standing lines are a template constant (§ 5, handoff), not story. | handoff cold-seat list |
| `## @why` | `### k. title` + paragraphs; the last block is `### Resolved, and still open`. The dossier body, verbatim. | `dossier`; nothing else |
| `## @findings` | `- **Finding.** sentence` — what the WRAP found (the W report's § 3) | report |
| `## @questions` | ruling-shaped questions for Dave from the wrap seat, or `None.` | report; handoff OWED (owner `dave`) only if ALSO listed in `@owed` — the story seat lists it there; this section is the report's heading |
| `## @unproven` | `- **Claim.** why it is unproven, and its price` or `None.` | report |
| `## @skips` | one paragraph: declared skips and not-done at this wrap (2e, `Previous:` trim, step 3 seat limit, other-seat dirty paths) | stratum's DECLARED SKIPS line |
| `## @section_usage` | one line, the seat's self-report (`GM HDR:R LATEST:C …`) | stratum |
| `## @tally` | RESERVED for phase 6 (`s306-D9`): one block, replaced in place, never appended (limit 3). Empty until then; the parser accepts it and the limits check fails on a second `## @tally`. | nothing yet |

The rule that keeps `@owed` and `@new` from being typed twice: an `@owed` item whose owner is `mine`, `dave` or `future` and whose mark is `⬛` IS a new carried item unless it ends with `(carried)` — meaning it already stands in `_CARRIES.md` under an older age. The generator derives `@new` from `@owed` when `## @new` is absent, and REFUSES when both are present and disagree on a title. The worked example writes `@new` explicitly, because #310's bodies differ between the handoff and the carries; E1 may keep the explicit form and add the derivation later. Either way there is one writer.

### 2.3 What is required, what may be empty

Required and non-empty: front block, `@words`, `@rulings` (or the line `None this session.`), `@summary` (all three), `@did`, `@owed`, `@why`. May be `None.`: `@problems`, `@new`, `@struck`, `@rows`, `@cold`, `@findings`, `@questions`, `@unproven`. Always present, one paragraph: `@skips`, `@section_usage`. Reserved: `@tally`.

---

## 3. `FACTS.json` — what phase 3 needs that `_wrap_facts.py` does not measure yet

Today's keys (measured at #309/#310): `measured_at, tree, tool, rulings{total,newest,last_in_file,by_status,base}, store, carries{section,items,probe_form,segments,struck_this_line}, sizes{bytes,section_sizes_line}, git{head,origin_master,ahead_of_origin,since{sha,commits,range}}, fill{unit,transcript,until,turns,boot,now,now_at,peak,crossings,boot_ceiling}, subs{n,total,largest,smallest,excluded}`. The views need these additions, all measured, all by `_wrap_facts.py` (E1 owns it; each is a small reader with a bite):

| key | measured how | used by |
|---|---|---|
| `dates.opened_at` (ISO), `dates.opened_local` (`Wed 2026-09-30 14:02 BST`), `dates.wrap_at`, `dates.wrap_local`, `dates.ritual_date` (from `date` at the seat, never the session's belief) | first record and the `--until` record of the transcript; `date` | banner header, delta header, stamp, handoff's days line, dossier intro, memory front |
| `dates.split` (`null` or `{opened_day, resumed_day, resumed_at, ordinal}`) — `ordinal` = 1 + the count of `WRAP DATE SPLIT` lines in `GOOD-MORNING.md` + `notes/_GM-ARCHIVE.md` | grep; the resumed time is the first user record after a gap of > 4 h, declared as the rule | `datesplit` view, and the `DATE SPLIT` clause in banner/stamp/handoff/dossier |
| `git.commits[]` = `{sha8, at, subject}` for `since.range` | `git log --format` | the COMMITS table in the handoff, the stratum's COMMIT STATE, the report |
| `git.pushed_through` (sha8 of `origin/master` at measure time) | already `origin_master` | the "pushed through X, Y rides the wrap push" clause |
| `handoff.prev_no`, `handoff.no`, `handoff.prev_name` | the newest `_HANDOFF-*.md` by number, +1 | every view that names the handoff |
| `ci.owed` = `{sha8, run_id, verdict}` (the opener's owed read), `ci.reds[]` = `{sha8, step, fixed_by}` | `_ci_readback.py`'s saved summaries in `notes/_lanes/<n>/`, read by path; the reds the story seat names are typed in `@problems` — the sha is checked against `git.commits` | delta ⚠ paragraph, summary Problems, banner ③, handoff |
| `chain.tk` (cl100k of `_CHAIN.md`), `chain.warn`, `chain.block` | tiktoken; `_capture_gate.CHAIN_BUDGET_TK` | the 5b line, the report |
| `gate.open` = `"247 in scope · 0 fail · 33 warn"` | the seat passes `--gate-log <path>` and the tool parses the last verdict line | report's WRAP COUNTS |
| `post` (added AFTER the commit by `_wrap_facts.py --post --facts FACTS.json …`, by addition into the same file): `wrap_sha`, `seat_sha`, `gate_wrap`, `push_range`, `pushed_at`, `minutes_to_push`, `ci.run_id`, `ci.verdict`, `ci.jobs`, `prepush{pass,fail,advisory,could_not_ask,tests}`, `chain_tk_after_regen`, `chain_tk_after_5b`, `titles.brief`, `titles.derived` | git, the saved `_ci-runs-<sha8>.txt`, the prepush logs, `_gen_titles.py` | the `5b` view, the handoff's POST-WRAP ADDENDUM, the report's POST-COMMIT, the memory hook's CI line |

`FACTS.json` keeps one writer. The `post` block is the only write after the first; it is an addition (the pre-commit keys are byte-identical before and after, and the tool checks that before saving).

---

## 4. Derived values (`{d.…}`), computed by the generator, never typed

`d.session` (#310) · `d.headline_caps` (upper of `headline`) · `d.slug` (kebab of `headline`, the `_HANDOFF-<no>-<slug>.md` and dossier names) · `d.handoff_name`, `d.dossier_path` (`_DECISION-HISTORY/<session date>-<n>-<slug>.md`, the SESSION date under a date split, `s294-D11`), `d.report_path` (`notes/_subreports/<ritual date>-<n>-W-wrap.md`), `d.memory_name` (`wrap-<n>-<slug>`) · `d.days` ("one day, no date split" or "DATE SPLIT from Tue 09-29", from `facts.dates.split`) · `d.rulings_delta` (`841 → 849`), `d.rulings_ids` (`s310-D1`..`D8`), `d.rulings_n_words` ("EIGHT RULINGS") · `d.rulings_summary` ("8 rulings, 841 → 849", Dave's register) · `d.hard_line`, `d.stop_line`, `d.limit_line` (the three window lines from `_capture_gate`), `d.hard_crossed_local`, `d.stop_crossed_local`, `d.limit_crossed_local` (local times from `facts.fill.crossings`, whose keys carry a space and a number and so are not dotted-addressable; the generator maps them) · `d.fill_line` (the crossings sentence in the form the stratum and handoff use, from `facts.fill.crossings`, with "OVER the ceiling by 179" / "under … by 1,308") · `d.subs_line` · `d.carries_line` ("436 items by `_carry_items`, 6 new (which count from #312), 4 STRUCK (…)") — the "(which count from #N+2)" clause is DROPPED once E2's `_AGE_RE` fix lands (§ 6), because new items then count at once · `d.probe_line` (the PROBE one-liner with `#N+1`) · `d.commits_line` ("17 commits `7bc6b0c5..69173275`; 16 pushed through `44696966`, `69173275` rides the wrap push") · `d.struck_titles` (from `@struck`) · `d.first_beat` (`@owed[0]`'s question) · `d.new_count`, `d.struck_count`.

---

## 5. The views — one template each, copied from the #310 files, not redrawn

Templates are Python f-strings/`str.format` blocks inside `_wrap_views.py` (one dict `VIEWS`, one function per view; no template library). Every fixed line in a view is a CONSTANT in the tool; every variable line names its story section or fact. The shape of each is the #310 file, byte for byte where nothing varies. Where #309 and #310 differ, the difference is a fact (`dates.split`, `ci.reds`, `subs.n`) and the template branches on it. Listed with its home, its limit and its size at #310.

| view | written to | then to (home) | limit (cl100k unless said) | #310 |
|---|---|---|---|---|
| `banner` | `views/banner.md` | `_wrap_ops.py --banner` → GM ★ LATEST | ≤ 10 lines, ≤ 1,200 (`s241-D2`, existing gate) · the generator prints each bullet's size and REFUSES over 1,200, naming the longest bullet | 741 |
| `delta` | `views/delta.md` | `_wrap_ops.py --delta` → LS ⏱ LATEST | ≤ 1,513 (limit 3/6; #305's delta) · refuse over | 1,068 |
| `stratum` | `views/stratum.md` | `_wrap_ops.py --stratum` | none new (2f rolls it next wrap) | 1,820 |
| `stamp` | `views/stamp.md` | `_wrap_ops.py --stamp` | one line | 222 |
| `datesplit` | `views/datesplit.md` (only when `facts.dates.split`) | `_wrap_ops.py --date-split` | one line | 228 (#309) |
| `5b` | `views/5b.md` (stage `post`) | `_wrap_ops.py --fill-token PLACEHOLDER-<n>W` | one line | 167 |
| `handoff` | `views/handoff.md` | `_HANDOFF-<no>-<slug>.md` at the root | WARN over 6,500, BLOCK over 8,106 (limit 2: `_HANDOFF-156` whole, the largest of the ten before #306) — measured WITH the 5b addendum | 4,622 |
| `prior-strikes` | `views/prior-strikes.md` | appended by addition to `_HANDOFF-<no-1>-*.md` under `## ⬛ STRUCK AT THE #<n> WRAP — BY ADDITION` | none | — |
| `dossier` | `views/dossier.md` | `_DECISION-HISTORY/<date>-<n>-<slug>.md` | WARN over 2,500 (#310 is 1,385; the number is picked) | 1,385 |
| `report` | `views/report.md` | `notes/_subreports/<date>-<n>-W-wrap.md` | must carry `COUNTS:`, `## Found, not fixed`, `## Ruling-shaped questions`, `REPLAY-THESE:` (`s218-D7`; the generated report IS the filed report, `s306-D5`) | 2,236 |
| `memory` | `views/WRAP-MEMORY-HOOK.md` | `notes/_lanes/<n>/WRAP-MEMORY-HOOK.md` — ONE file holding the placer's instructions, the index line, the front block and the body, each ONCE, under marked headings the placer cuts at | one memory file per wrap (limit 11); description ≤ 800 B (picked: the harness listing truncates near 150 characters, so the first clause must carry the session) | 1,169 |
| `carries` | `views/new.txt`, `views/strike-<k>.txt` | `_wrap_carries.py roll --new`, `strike --note-file` (today); E2's delta block (§ 6) | `_CARRIES.md` growth ≤ 20,000 B a wrap (limit 10) | 846 + 559 |
| `rows` | `views/rows.json` | `_wrap_rows.py --spec` | schema = today's `rows.json` | 857 |
| `msg` | `views/msg.txt` | `_wrap_commit.py msg` | line 1 ≤ 170, no `#N date —` prefix (existing) | 473 |
| `summary` | `views/SUMMARY.md` | chat, at the push (`s306-D7`) | `s305-D63`'s three headings | 435 |

Two stages: `_wrap_views.py --session N --stage wrap` writes everything but `5b`; `--stage post` (after `FACTS.json` has `post`) writes `5b`, and REGENERATES `handoff`, `report` and `memory` with their post-wrap blocks appended — the tool asserts the pre-commit part of each is byte-identical to the stage-wrap output before it writes (the "by addition, nothing above is rewritten" rule as a check). Dry run by default: prints each view's size against its limit and the diff against disk; `--write` writes the `views/` files AND copies each to its home (`--home` may be withheld for the ones a phase-1 tool places: banner, delta, stratum, stamp, datesplit, 5b, new.txt, strike-*, rows.json, msg — those are read from `views/` by the runbook's PHASE 1 commands).

The handoff's cold-seat list: eleven STANDING lines are a constant in the tool (never memory read/write at the opener; never `git status`; an inscription runs the titles and the rulings page; the conductor's own push runs the pre-push check; read the fill between lanes; commit msgfile line 1 without the prefix; the state-contrast sweep's 2 min a slice; `device_bash` 120 s default; the window lines; Project memory placed only after he says he is done; other-seat paths dirty by declaration). The session's OWN lines come from `@cold`. The tool prints the count so the list is seen to grow only from `@cold`.

The handoff's READ FIRST list is a constant with three variables: `handoff.prev_no`, `prior_handoff_struck`, `words_files`, `lane_reports`.

### 5.1 The freshness arm (limit 7), and where it runs

`_wrap_views.py --check --session N` regenerates every view for the NEWEST wrap only (the newest `_HANDOFF-*.md` names N) and compares with disk: the `views/` files, and the homes for `handoff`, `dossier`, `report`, `memory`. Red on any difference, naming the file and the first differing line. It also runs every limit in § 5 and § 2 (the retype warn, the `@tally` count, `@words` over 3,000 cl100k warns — limit 4). It runs in `_wrap_regen.py`'s `--check` serial (E1 adds the step; `_wrap_*.py` is this job's path) and is the wrap gate's arm once the conductor allows the one call in `_capture_gate.py` (NOT this job's path; named under Found-not-fixed for the #311 conductor). Until then the seat runs it by hand before the commit, and the runbook says so.

Limit 1 (the draft is never on the boot chain) is a bite in the selftest: `_gen_chain.py`'s source is read and must contain no `notes/_lanes` path; `STORY.md` is never written under a `_HANDOFF-` name. Limit 6 (the chain takes only banner and delta) is true by construction: `_gen_chain.py` is unchanged and `_wrap_views.py` writes nothing else that `_gen_chain.py` reads.

---

## 6. The carries delta (`s306-D8`, E2)

Today each wrap writes a whole `## residual → #N+1` line (368,624–803,996 chars) with every age +1. From E2 on, a wrap APPENDS to `_CARRIES.md` one small block, generated from `@new` and `@struck`:

```
## residual → #312 (delta from #311)

> **base:** `residual → #311` (the last FULL line; every item on it is one wrap older here)
> **new → #312:** ⬛ **① TITLE** [NEW — 0] — body · ⬛ **② TITLE** [NEW — 0, DAVE'S] — body
> **struck → #312:** **TITLE AS IT STANDS** — VERDICT — receipt · **TITLE** — VERDICT — receipt
> **count → #312:** 439 (PROBE `python3 knowledge/_wrap_carries.py count --section 312`)
```

`_wrap_carries.py render --section N` materialises the full line: take the newest FULL line at or before N (the base), apply every delta block after it in order (ages +1 per wrap, strikes as `~~…~~` in place with their receipts, new items first), and print it, or write it to a gitignored `knowledge/_tmp/carries-<N>.md` — never committed per wrap (limit 10). `count` and the gate's `_carry_items` read the rendered line. Every twentieth wrap (picked, not ruled) the seat may `_wrap_carries.py rebase --section N --write` to commit a new FULL line so the render never replays more than twenty deltas. The reconstruction proof (`s183-D1`) holds: rendering the deltas and diffing against the last hand-written full line at #311 must give #311's line byte for byte, which is E3's replay for this piece.

The `[NEW — 0]` count defect, fixed on the way: `_capture_gate._AGE_RE` is `\[(\d+)(?:\s*[,—-][^\]]*)?\]`; its docstring says `[NEW — 0]` "is stripped to 0", but the bracket starts with `NEW`, so it never matches and NEW items are NOT counted — hence every banner's "(which count from #N+2)". The fix is one alternation, `\[(?:NEW\s*[—-]\s*)?(\d+)(?:\s*[,—-][^\]]*)?\]`, in `_capture_gate.py` — not this job's path, so E2 makes `_wrap_carries.py` carry its own `AGE_RE` with the fix (and `bump_ages` keeps working: `NEW_RE` runs first), reports the one-line `_capture_gate.py` change under Found-not-fixed, and the count line says which regex it counted with until the gate's is fixed. The instruction-right-cause-wrong lesson applies: the docstring's cause is wrong and the count has been low by the new items for as long as the form has existed.

---

## 7. The limits, as one table (from `s306-D10`, lane U's eleven; the numbers marked "picked" are not his)

| # | limit | where it bites | number |
|---|---|---|---|
| 1 | the story draft is never on the boot chain | selftest bite on `_gen_chain.py` source; the name rule | — |
| 2 | ceiling on the generated handoff | `--check`, blocking | warn 6,500 (picked) · block 8,106 cl100k |
| 3 | the tally is one block, replaced | parser refuses a second `## @tally` | 1,513 cl100k when phase 6 lands |
| 4 | his words verbatim with times; exports by path | `@words` grammar; warn over 3,000 cl100k | 3,000 |
| 5 | the seam prints one line | phase 6 | — |
| 6 | the chain takes only banner and delta | by construction; banner ≤ 1,200, delta ≤ 1,513 | existing + 1,513 |
| 7 | freshness checks the newest wrap only | `--check` reads the newest handoff's N | — |
| 8 | the opener's CI read prints the summary | phase 2, done | — |
| 9 | one shared brief, one line per seat | phase 4 | — |
| 10 | the full carried list is generated on read; `_CARRIES.md` ≤ 20,000 B a wrap | `_wrap_carries.py render`; `--check` measures the delta block | 20,000 B |
| 11 | one memory file per wrap | the `memory` view is one file | — |

---

## 8. The replay (E3), and what "green" means

For #309 and #310: derive `STORY-<n>.md` backwards from the hand-written views (the #310 one is on this page's sibling file; E3 derives #309's the same way — it has the date split, two CI reds, six subs, one strike and the "owed read GREEN" clause, so it exercises every branch #310 does not). Run `_wrap_views.py --session <n> --story … --facts notes/_lanes/<n>/W/FACTS.json --out /dev/shm/replay<n>/` (dry, no homes). Diff each generated view against the hand-written file with `_wrap_views.py diff --generated A --hand B`, which reports, per view:

1. FIGURES — every number of 3+ digits, every sha8, every `sNNN-Dk`, every `W-…` id and every path in each file, as sets: missing from the generated view, extra in it. Green = no figure in the hand-written view is missing from the generated one, and no extra figure is unsourced (not in `FACTS.json` or the story).
2. HIS WORDS — every *"…"* quotation in the hand-written view appears verbatim in the generated one.
3. HEADINGS — the `## `/`### ` sequence is identical (the handoff, report, dossier, memory hook); for the banner, the bullet count and rank marks; for the delta, the paragraph count.
4. SIZE — the generated view's cl100k against the limit, and against the hand-written file (a generated view may not be larger than 110% of the hand-written one; picked).
5. BYTES — a plain diff, filed but not graded (prose will differ in wording; that is expected and is the point of the story: E3 explains the residue in its report).

The replay is GREEN for a session when 1–4 pass on every view. Diffs and verdicts are filed at `notes/_lanes/312/E/replay/<n>/` and summarised in E3's report. The frozen fixtures then go to `knowledge/_tests/wrap_views/<n>/{STORY.md, FACTS.json, expected/}` and `_wrap_views.py --selftest` regenerates and compares byte-exact, with these mutants each turning it red: a fill figure changed in `FACTS.json` (every view that shows it changes, or the check is red — EV's attack); a `@words` line changed; a `@tally` doubled; a handoff pushed over 8,106 by padding `@did`; a hand edit to a generated file; a `{facts.no.such.key}`; a typed `372,194` in a story sentence (warn).

## 9. How #311 joins, and which path the #311 wrap takes

#311 has not wrapped, so there is no third hand-written fixture. Two cases, both written into the runbook block (§ 10):

- If E1–E3 are green on #309 and #310 BEFORE the #311 wrap seat is launched, the #311 wrap runs the NEW path: the story seat writes `STORY.md`, runs `_wrap_views.py --check` (limits and schema) and `--write`, and the rest of the ritual is the PHASE 1 table unchanged, its inputs now generated. Its `STORY.md`, `FACTS.json` and views become the third fixture (`knowledge/_tests/wrap_views/311/`) in the same commit as the wrap's seat files, which closes the brief's "three fixtures" clause. `W-305wr` gains a note; it stays open until a wrap has run and the counts (hand-written characters before and after; homes per fact) are measured, as the decision page's proof for phase 3 says.
- If not, the #311 wrap runs the PHASE 1 path as #309 and #310 did, and its hand-written views are the third replay fixture, derived exactly as #309's. E3 (or a wave-2 lane) replays it; the first wrap on the new path is #312's.

Either way the phase-1 tools are the ones that move files, so a failure in phase 3 never leaves a wrap without a path: the seat writes the fifteen files by hand, as today.

## 10. The runbook, by addition only (E1 writes; text to paste after the `s306-D7` block)

`### ★ PHASE 3 — ONE STORY, EVERY VIEW GENERATED (s306-D4, s306-D5, s306-D8, s306-D10; #311/#312, 2026-10-01; added by addition — the PHASE 1 table above is unchanged and its inputs are now generated)`. Content: the two-file rule (one writer each); the story's sections in one table (a copy of § 2.2's first two columns); the command order — `_wrap_facts.py` → write `STORY.md` → `_wrap_views.py --check` → `--write` → the PHASE 1 table from `_wrap_ops.py` on, reading `views/` → commit → push → `_ci_readback.py` → `_wrap_facts.py --post` → `_wrap_views.py --stage post --write` → the 5b commit; which path the seat takes (§ 9) and why (the replay verdict, by session, filed at `notes/_lanes/312/E/replay/`); and the limits table (§ 7). Nothing in steps 1–5b is rewritten.

## 11. Phases 4–6, if they fall out cheaply (named, not started)

- Phase 4 (three seats, `s306-D6`): the story seat writes `STORY.md`; the mechanics seat runs `_wrap_facts.py`, the open gate, `_wrap_carries.py` and `_wrap_rows.py` — but the carries and rows now come from the STORY, so the mechanics seat's independent work shrinks to facts, gate and the archive moves' projection; the commit seat runs `_wrap_views.py --write`, `_wrap_ops.py`, `_gm_move.py`, regen, commit, push. The join is `views/`. The split is a brief template, not code.
- Phase 5 is § 6 (E2 builds it in this job).
- Phase 6 (`s306-D9`): the seam appends to `@words` and replaces `@tally`. The grammar already holds both; the tool needs `_wrap_views.py append-words --at HH:MM --text …` and `set-tally`, each a bite. Not started until a real wrap has run on phase 3.

## Found, not fixed (for the #311 conductor)

1. The freshness arm's one call in `_capture_gate.py` (wrap mode, blocking) and the `_AGE_RE` alternation are both in `_capture_gate.py`, which no lane in job E owns. Both are one-line changes; the conductor decides who lands them.
2. `_carry_items` has undercounted by the number of NEW items on every banner since the `[NEW — 0]` form began; the "(which count from #N+2)" clause in the banners is the seats' reading of the defect as the contract. Stated, not corrected in any past line.
3. `_wrap_facts.py` does not measure dates, commits, CI, chain size or the post-commit facts (§ 3); the #309 and #310 handoffs typed them from `COMMITS.txt`, `_ci-runs-*.txt` and the seat's own reads. E1 adds the readers; until then a replay must take those from the hand-written files, which E3 declares per figure.
4. Limit 2's second clause — "count the handoff in the gauge's boot figure beside the chain" — is a change to `measure_boot` in `knowledge/_gauge_tokens.py`, not a job-E path. The handoff ceiling on this page (§ 5, § 7) bites in `_wrap_views.py --check`; the gauge's boot figure keeps not counting the handoff until the conductor names a lane for that one reader.

## Ruling-shaped questions

None. Every number marked "picked" is a threshold under `s306-D10`'s guards, put to Dave only if a real wrap trips one.
