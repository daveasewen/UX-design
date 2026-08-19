# Claim table — #204 BUILD-PM wave (P2 gaps + CI repair)

*⚠ **WRITTEN BY A FINISHER, NOT BY THE BUILD-PM.** The BUILD-PM was killed by a connection loss at
the last step of its brief — writing this table. This document was reconstructed from the four
on-disk receipts plus first-hand re-runs. **That is one lossy hop**, and it is the first thing in
the pitfalls section. Written 2026-08-19 under the `s203-D2` PM-topology trial.*

*⛔ Fences honoured by this finisher, all of them: no commit, no push, no `git checkout/restore/stash`,
no write to `knowledge/_rulings.json` (`git status --porcelain knowledge/_rulings.json` → empty),
`_build_all.py` NEVER run, `GOOD-MORNING.md` / `_CHAIN.md` / `_LIVE-STATE.md` / the frozen
`reviews/ITINERARY-2026-07-14-*` files untouched. Nothing here is a ruling.*

## Tag vocabulary

| Tag | Meaning |
|---|---|
| **PROVEN** | The finisher ran the command in this session and read the exit code |
| **MEASURED** | The finisher read the artefact / store / filesystem first-hand this session |
| **CLAIMED** | Only a lane receipt asserts it; the finisher did **not** re-run it |
| **UNPROVEN** | Named, not established — a declared stop or an open item |

---

## A · The five gates — RE-RUN FIRST-HAND, exit codes read from `$?`

⚠ **A methodology note that is itself a finding.** The first attempt redirected gate output to
`/var/tmp/<gate>.out`. Those paths already held **stale files owned by a foreign session**, so the
redirect failed `Permission denied`, the gate **never ran**, `rc=1` came from bash's redirect
error, and `tail` then printed a **previous session's output** (`76 snippet(s)`, DRIFT failures on
`--pri-hover`). Two of five gates read as RED off numbers that were months old. Re-run into a fresh
`mktemp -d`. **This is the `a-crash-is-not-a-fail` / `ritual-output-is-not-evidence` class in a new
place: a shell redirect can fail and still hand you plausible output.** Every rc below is from the
clean re-run.

| id | claim | evidence pointer | tag |
|---|---|---|---|
| G-1 | `_validate_snippets.py` is green over the wave | `python3 knowledge/_validate_snippets.py` → **rc=0** · `snippet gate: 91 snippet(s), 0 failure(s)` | **PROVEN** |
| G-2 | `_validate_a11y.py` is green | `python3 knowledge/_validate_a11y.py` → **rc=0** · `a11y gate: 91 snippet(s), 0 failure(s), 186 warning(s), 218 note(s) · 566 controls + 203 marks measured · 107 mark(s) below 24` | **PROVEN** |
| G-3 | `_validate_radius.py` is green with the six registered | `python3 knowledge/_validate_radius.py` → **rc=0** · `_validate_radius: 0 strict fail(s), 0 advisory file(s) pending migration -> _RADIUS-GATE.md` | **PROVEN** |
| G-4 | `_validate_coverage.py` is green and meta/snippet counts match | `python3 knowledge/_validate_coverage.py` → **rc=0** · `coverage gate: 91 meta(s) / 91 snippet(s), 0 failure(s)` | **PROVEN** |
| G-5 | `_validate_icons.py` is green — no invented glyph shipped | `python3 knowledge/_validate_icons.py` → **rc=0** · `0 UNKNOWN, 69 bespoke, across 91 snippet(s); 746 library glyphs` | **PROVEN** |
| G-6 | Lane P's residual "`_validate_icons.py` not run, so the byte-copied `contactless.svg` is unproven" is now CLOSED | G-5 above, rc=0, **0 UNKNOWN** across all 91 snippets including `Payment-card-visual.reference.html` | **PROVEN** |
| G-7 | `_gate_doc_rows.py` passes | `python3 knowledge/_gate_doc_rows.py` → **rc=0** · `doc-row gate: population 13 (added >= 2026-08-15, PICKED) · unrowed 0` — ⚠ but see D-3: it passes **vacuously** for this wave | **PROVEN** |
| G-8 | `_validate_state_contrast.py` — the residual all three lanes declared | **NOT RUN by the finisher either.** A filtered run overwrites the tracked `_STATE-CONTRAST-AUDIT.md`; the finisher holds no more licence than the lanes did. **Still owed to the conductor or CI.** | **UNPROVEN** |
| G-9 | `_validate_type_composites.py` repo-wide is red at 1,097 and the wave added zero | Three lane receipts each report `rc=1 · TYPE GATE FAIL — 1097 violation(s) across 90/106 file(s)`. **Not re-run by the finisher.** ⚠ 1,097 is the ratchet figure `MEMORY.md` carries; a re-run is the cheap check | **CLAIMED** |

---

## B · Lane 1 — CI repair. The four CI-failing commands, RE-RUN FIRST-HAND

| id | claim | evidence pointer | tag |
|---|---|---|---|
| L1-1 | `[3]` blast radius REPAIRED | `python3 knowledge/tokens/_build_blast_radius.py --check` → **rc=0** · `✓ _build_blast_radius --check PASS — tokens/_blast-radius.json and _GRAPH-REPORT.md match a fresh compute() (content, not mtime)` | **PROVEN — FIXED** |
| L1-2 | `[110]` graph mention map REPAIRED | `python3 knowledge/_build_graph_mention_map.py --check` → **rc=0** · `graph mention map --check: current (101 of 101 node(s) mentioned)` | **PROVEN — FIXED** |
| L1-3 | `[114]` `_gen_chain.py --selftest` STILL RED, and for the reason lane 1 named | `python3 knowledge/_gen_chain.py --selftest` → **rc=1** · failing bite verbatim: `✗ is materially smaller than GOOD-MORNING.md (34,250 vs 81,637 tape, <40%)` · `✗ _gen_chain selftest: 1 bite(s) failed` | **PROVEN — STILL RED** |
| L1-4 | The `[114]` figures are the LIVE tree's `34,250 vs 81,637`, **not** the brief's `21,237 vs 51,204` (which are the capture-gate fixture tree's) | The verbatim gate line in L1-3. ⛔ **Do not quote the brief's numbers** | **PROVEN** |
| L1-5 | `[114]` is **not** clearable by regeneration; the levers are a constant (Dave's), the wrapper (trades against sibling bites) or `GOOD-MORNING.md` (fenced) | Lane-1 receipt's arithmetic: mandatory verbatim content alone = 31,668 tape = 38.79% of GM, headroom 1.21pp, wrapper costs 3.16pp. **Finisher did not re-derive the tape breakdown** — only the gate verdict (L1-3) | **CLAIMED** (verdict PROVEN, arithmetic CLAIMED) |
| L1-6 | `[13]` `_capture_gate.py --selftest` STILL RED, with **two** causes not one | `python3 knowledge/_capture_gate.py --selftest` → **rc=1** · `capture gate [wrap]: 5 in scope · 4 fail · 2 warn`; three ❌ verdicts verbatim: `_governs.py selftest is RED — 1 failure(s)` · `_governs: an unrelated path matched a ruling — the matcher is too loose to carry information` · `#70/#71 non-catch: _gen_chain.py --selftest is NOT green` | **PROVEN — STILL RED** |
| L1-7 | The `_governs` defect is ONE token in ONE ruling: `s202-D3`'s `governs` list contains the bare directory name `knowledge`, which matches every path including the negative control | Lane-1 receipt's isolation: `203 rulings · 77 bare-token governs entries · governs entries that are BARE DIRECTORY NAMES: [('s202-D3','knowledge')]`. **Finisher re-ran the gate (L1-6) but did NOT re-run the census** | **CLAIMED** |
| L1-8 | `[13]`/`[114]` are inherited from #202/#203, not caused by this wave | `git status --porcelain` → `knowledge/_rulings.json`, `GOOD-MORNING.md`, `_CHAIN.md`, `_LIVE-STATE.md` all **absent from the modified list** | **PROVEN** |
| L1-9 | Both stops were DECLARED, not worked around — no constant moved, no ruling edited, no negative control laundered | `git status` shows `knowledge/_gen_chain.py`, `_capture_gate.py`, `_governs.py`, `_rulings.json` all unmodified | **PROVEN** |
| L1-10 | ⛔ **THE LANE-1 RECEIPT IS WRONG ON ONE POINT.** It states `gen_canon_components.py` and `gen_theme_cascade.py` "**do not exist**" (`rc=2, No such file or directory`) | `find . -name "gen_canon_components.py" -o -name "gen_theme_cascade.py"` → **`./knowledge/canon/gen_canon_components.py`** and **`./knowledge/canon/gen_theme_cascade.py`**. They exist — at `knowledge/canon/`, not `knowledge/`. Likewise `canon.css` is at **`knowledge/canon/canon.css`**. **`unmatched-grep-is-not-an-absence` / `refusal-names-the-first-obstacle`: the receipt named a wrong path as an absence.** ⚠ The *consequence* the receipt drew is still correct (C-6 below) | **PROVEN — receipt claim FALSE** |
| L1-11 | ⛔ CI itself has seen **none** of this | No CI run was triggered; the wave is uncommitted (`git log --oneline -1` → `3a88777`, the same head CI failed on) | **PROVEN** |

---

## C · The components — six built, one refused

Existence matrix probed first-hand with `[ -f ]` per artefact, per slug.

| id | claim | evidence pointer | tag |
|---|---|---|---|
| C-1 | **All six components have all four artefacts.** For each of `popconfirm · footer · layout-utilities · document-row · payment-card-visual · runway-bar`: `knowledge/snippets/<Slug>.reference.html` · `knowledge/components/<slug>.meta.json` · `reviews/REVIEW-204-<slug>-four-themes-v1.html` · `showroom/<slug>.html` | `[ -f ]` on all 24 paths → **ok ×24, MISSING ×0**. Corroborated by `git status --porcelain`: 6 untracked snippets, 6 untracked metas, 6 untracked review pages, 6 untracked showroom pages | **MEASURED** |
| C-2 | All six ship **PROPOSED** | `grep -ic PROPOSED <snippet>` → popconfirm 5 · footer 4 · layout-utilities 5 · document-row 9 · payment-card-visual 6 · runway-bar 6. **Zero snippets ship unmarked** | **MEASURED** |
| C-3 | All six are registered in the **radius ratchet** | `git diff knowledge/_validate_radius.py` → six names added to `MIGRATED_SNIPPETS` under a comment recording 0 advisory hardcodes before registration. `grep -c` per slug → 1 each. ⚠ **This is a GATE ratchet, not promotion** | **MEASURED** |
| C-4 | ⛔ None of the six is registered in `gen_showroom.CATEGORIES` — deliberate, promotion is Dave's | `grep -c "\"<slug>\"" knowledge/gen_showroom.py` → **0 for all six**. They fall to the generator's "More" fallback bucket | **MEASURED** |
| C-5 | ⛔ None of the six is in `knowledge/component-types.json` — so none takes an `AUTO-BEHAVIOUR` or press-physics partial | `grep -c` per slug → **0 for all six** | **MEASURED** |
| C-6 | ⛔ None of the six exists in `canon.css`; the review pages carry **hand-mirrored** `.cn-` scopes, not generator output | `grep -c "cn-<slug>" knowledge/canon/canon.css` → **0 for all six** (control: `cn-list-items` → **54**). ⚠ **The conductor owns this reconciliation**, and per L1-10 the generators DO exist to do it | **MEASURED** |
| C-7 | Every render/theme/contrast/hit-area figure in the three lane receipts | Driven in a browser by each worker; **the finisher re-drove nothing**. `_validate_snippets.py` resolves the **mono base only** — the Legacy / Console / Supercharge legs are gate-invisible by construction | **CLAIMED** |
| C-8 | Metas validate against `meta.schema.json` (lane M's three) | Lane M receipt: `popconfirm SCHEMA PASS · footer SCHEMA PASS · layout-utilities SCHEMA PASS`. **Not re-run.** ⚠ Lanes N and P do **not** report a schema run at all | **CLAIMED** (lanes N/P: **UNPROVEN**) |

---

## D · Row 91 — THE OPEN QUESTION, ANSWERED

**Verdict: row 91 was DELIBERATELY REFUSED at step 0 with a documented finding. It was NOT
"never reached before the kill." Nothing is owed. No transaction row was built and none should be.**

| id | claim | evidence pointer | tag |
|---|---|---|---|
| D-1 | Row 91 was refused, not missed | Lane N receipt, headline: *"Row 91 'Transaction / ledger row' **IS A DUPLICATE**… I built no transaction row"*; premise-table row 3 verdict: *"⛔ **FALSE — and false in the OPPOSITE DIRECTION** … **STOPPED on this component, per the brief**"*; residuals: *"Row 91 produced no artefact at all, **by design**"* | **MEASURED** (the refusal is on disk, in three independent places in the receipt) |
| D-2 | The reason: the transaction row is a **Dave-promoted, gated, 9.0/9 component** shipping as a *variant* of `list-items`, not a gap | `list-items.meta.json` `build.$status` = *"PROMOTED 2026-06-22 (Dave) — TRANSACTION row brought to the Tabs-bar standard"*; `build.scope` = *"Transaction row only"*; `List-items.reference.html` `<title>` = *"List items — Transaction row (reference implementation, gated)"*. **Quoted by lane N; the finisher did not re-open the two files** | **CLAIMED** ⚠ *this is the single most load-bearing unverified claim in the table — see P-2* |
| D-3 | No transaction-row artefact exists anywhere | `ls knowledge/snippets/ knowledge/components/ reviews/ showroom/ \| grep -i transaction` → **empty** | **MEASURED** |
| D-4 | The refusal is recorded where Dave will see it | `knowledge/_REVIEW-SIGNOFF.md` line 299 states verbatim *"six built, **one refused**"* and carries the `list-items` quotation | **MEASURED** |
| D-5 | ★ The class finding underneath it: **a slug-shaped probe cannot see a component that ships as a VARIANT of another**, so any derived-status instrument that probes by slug manufactures this false gap for every variant-shipped row | Lane N finding 2. Consistent with D-3 (all five artefact probes were correctly negative). **The generalisation is not independently tested** | **CLAIMED** |
| D-6 | ★ The genuinely open item row 91 leaves: the gated transaction row renders `−1,234.00 HKD` — currency code **after** the value **with a space** — which is `amount-display.meta.json` antiPattern #1 (`copy-025`) verbatim, and it does not compose the Amount-display atom | Lane N finding 3. **Not re-verified by the finisher.** A small repair on a gated file — **Dave's or the conductor's, not a worker's** | **CLAIMED** |
| D-7 | Whether the itinerary row should be re-marked **Duplicate** | ⛔ **NOT RULED, and not rulable here.** Store search that failed to settle it (`s202-D3`): direct grep of all 203 `_rulings.json` entries for `transaction\|ledger\|statement row\|document row\|line[- ]item\|debit\|credit` → **16 hits, all 16 using "ledger" in the record-keeping sense, zero about a component**. The frozen itinerary files were not touched | **UNPROVEN — Dave's** |

---

## E · The 7-vs-8 P2 count — the brief's own flagged discrepancy, MEASURED

| id | claim | evidence pointer | tag |
|---|---|---|---|
| E-1 | The JSON yields **7** P2 true gaps, not the #203 banner's 8 | `reviews/ITINERARY-STATUS-2026-08-19-v1.json`: `$true_gaps` = 23 row numbers; joined to `rows` on `n` → priorities `Counter({'P3': 15, 'P2': 7, 'P1': 1})`. The seven, verbatim: **75 Popconfirm · 81 Footer · 82 Grid / stack utilities · 91 Transaction / ledger row · 92 Statement / document row · 93 Payment-card visual · 94 Coverage / runway bar** — exactly the brief's list, all `layer: 1 Base` | **PROVEN (re-derived from the JSON this session)** |
| E-2 | The itinerary's `itinerary_status` column is wrong for rows 91 and 92 — both read `Partial` | Same query: rows 91 and 92 both `Partial`; the other five `Gap`. Row 91's store holds a **promoted 9.0/9 build** (D-2), so `Partial` understates it; row 92 is a true gap, so `Partial` understates it the other way. ★ `premise-ages-faster-than-rule` earned its keep — **a derived Status column was wrong for 2 of 7 rows** | **PROVEN + CLAIMED** (counts PROVEN, the row-91 adjudication CLAIMED per D-2) |
| E-3 | The 8th P2 in the #203 banner | **Never located.** Not re-derivable from the JSON. Build proceeded off the JSON, as the brief instructed | **UNPROVEN — declared, not resolved** |

---

## F · Every modified TRACKED file, attributed

`git status --porcelain` run this session. 14 modified tracked files, 30 untracked. **Zero deletions,
zero renames.** ⚠ Some audit outputs below were **rewritten again by the finisher's own gate re-runs**
in section A — that is declared, not hidden.

| id | path | attribution | tag |
|---|---|---|---|
| F-1 | `knowledge/tokens/_blast-radius.json` | Lane 1 — regenerated (85→91 components). Verified fresh by L1-1 | **PROVEN** |
| F-2 | `knowledge/_GRAPH-REPORT.md` | Lane 1 — regenerated with F-1. Verified fresh by L1-1 | **PROVEN** |
| F-3 | `knowledge/_graph-mention-map.json` | Lane 1 — regenerated. Verified fresh by L1-2 | **PROVEN** |
| F-4 | `knowledge/_validate_radius.py` | **BUILD-PM** — six slugs added to `MIGRATED_SNIPPETS` + provenance comment. Diff read first-hand (C-3). ⚠ The only **hand-edited source file** in the wave | **MEASURED** |
| F-5 | `knowledge/_REVIEW-SIGNOFF.md` | **BUILD-PM** — **+1 line, 0 removed** (`git diff` confirms pure append; `add, never trim` honoured) | **PROVEN** |
| F-6 | `showroom/index.html` | Lane 1 — showroom regeneration (index + 6 new pages) | **CLAIMED** (the file is modified: **MEASURED**; that `gen_showroom.py` produced it: CLAIMED) |
| F-7 | `knowledge/_A11Y-GATE.md` · `_SNIPPET-AUDIT.md` · `_RADIUS-GATE.md` · `_ICON-SOURCE-AUDIT.md` · `_COVERAGE-GATE.md` | Gate side-effect outputs — rewritten by running the gates. ⚠ **Rewritten AGAIN by the finisher in section A**; their current content is the finisher's run, not the BUILD-PM's | **PROVEN** |
| F-8 | `knowledge/_graph-mark-observations.jsonl` | Gate side-effect append (+41 lines) | **MEASURED** |
| F-9 | `notes/_REHEARSAL-LOG.jsonl` | **⚠ UNATTRIBUTED BY ANY RECEIPT.** +7 lines, all `{"date":"2026-08-19","fails":0,"heals_at_wrap":0,"kind":"wrap-open","structural":0,"warns":15}`. Shape says `_capture_gate.py` rehearsal appends (the lanes' and BUILD-PM's `_checkin.py` runs, plus **one from the finisher's L1-6**). **No lane receipt lists it as a touched path** | **MEASURED (content) / UNPROVEN (attribution)** |
| F-10 | `notes/_dream/_GRADE-DECISIONS.jsonl` | **⚠ UNATTRIBUTED BY ANY RECEIPT.** +5 lines, all `{"kind":"alert",...,"at":"2026-08-19T09:03:__"}`. Shape says dream-grade alert appends from `_checkin.py`. **No lane receipt lists it** | **MEASURED (content) / UNPROVEN (attribution)** |
| F-11 | ⛔ Nothing fenced was touched | `git status --porcelain` shows **no** entry for `knowledge/_rulings.json`, `GOOD-MORNING.md`, `_CHAIN.md`, `_LIVE-STATE.md`, `reviews/ITINERARY-2026-07-14-*`, `component-types.json`, `knowledge/canon/canon.css`, `gen_showroom.py`, `_state.json`, `_a11y_target.py`, `meta.schema.json`, `_DS-IMPROVEMENTS.md` | **PROVEN** |
| F-12 | 30 untracked files: 6 snippets + 6 metas + 6 review pages + 6 showroom pages + 1 brief + 5 receipts (4 lane + this table) | `git status --porcelain` | **MEASURED** |

---

## G · Registration — signoff rows and store rows (the forgotten-document class)

| id | claim | evidence pointer | tag |
|---|---|---|---|
| G-a | `_REVIEW-SIGNOFF.md` **already carries the six spreads** — one combined row naming all six by filename, `⬛ AWAITING DAVE`, with the row-91 refusal, the runway-bar fixture provenance, the Legacy two-red seam and the missing destructive seat all called out | Line 299 of `knowledge/_REVIEW-SIGNOFF.md`, read first-hand. **This matches the existing pattern** — #203's nine spreads are likewise one row. **Nothing added by the finisher; nothing was missing** | **MEASURED — no action needed** |
| G-b | `knowledge/_state.json` has **no** row for any of the six components, the six review pages, or the five receipts | `grep -ic` over the store for each slug and for `REVIEW-204` → **0 for all**. ⚠ **This matches the existing pattern**: the store is a **work-item register** (63 items, `W-nn`/`G-nn` IDs with `home`/`closes_when`/`condition`), not a document catalogue, and **#203's nine components have no rows either**. **The finisher added none** — minting a `W-nn` with a `closes_when` condition is authoring an open work item, which is the conductor's seat, not mechanical registration | **MEASURED — deliberately not written** |
| G-c | ⛔ **BUT: `_gate_doc_rows.py` WILL FAIL THE MOMENT THIS WAVE IS COMMITTED.** Its population is briefs only (`notes/_briefs/*`, `_BRIEF-*`) **and git-tracked**. `notes/_briefs/2026-08-19-204-buildpm-brief.md` is currently **untracked**, so today's `rc=0 · unrowed 0` is **vacuous for this wave** | Simulated first-hand: `python3 -c "import _gate_doc_rows as g; g.unrowed(store, pop + [('2026-08-19','notes/_briefs/2026-08-19-204-buildpm-brief.md')])"` → **`[('2026-08-19', 'notes/_briefs/2026-08-19-204-buildpm-brief.md')]`**. The only rowed #204 brief is `W-42`, which homes `_BRIEF-204-pm-topology-trial-…md` — **a different file**. **THE FIX IS ONE `_state.add()` CALL BY THE CONDUCTOR BEFORE COMMITTING** | **PROVEN** |
| G-d | ★ The gate's glob is narrower than the class it is named for | `_gate_doc_rows.PATTERNS = ["notes/_briefs", "_BRIEF-"]`, read first-hand. Snippets, metas, review pages and receipts are **all outside its population by construction** (`gate-glob-scope-rule`: a rule is only as wide as its gate's glob). **Not a defect — a scope, stated so it is not mistaken for coverage** | **MEASURED** |

---

## H · Declared stops and residuals carried out of the wave

| id | item | tag |
|---|---|---|
| H-1 | `[114]` chain-vs-GM compression bite — needs a constant (Dave's), the wrapper, or GM's wrap discipline | **UNPROVEN — stop declared, decision named** |
| H-2 | `[13]` `_governs` matcher red — one bare `knowledge` token in `s202-D3`'s `governs`. All three fixes are out of fence (write `_rulings.json` / narrow a RULED item's reach / launder the negative control). ★ Gate-class finding: **`_inscribe_ruling.py` is the only writer of `_rulings.json` and does not run the reader's selftest** — an `instrument-without-a-consumer` inversion, red across two sessions | **UNPROVEN — stop declared, decision named** |
| H-3 | `_validate_state_contrast.py` never run by anyone in this wave (would overwrite a tracked audit) | **UNPROVEN — owed** |
| H-4 | `_build_memento_index.py` not run — the retrieval index is STALE, so `_memento_search.py` served a **previous session's record** to all three workers. Every ruling claim in the wave therefore rests on a **direct grep of `_rulings.json`** (`retrieval-default-hides-the-ruling`: store > chain) | **CLAIMED — declared by lane 1** |
| H-5 | `canon.css` regeneration not run; six components absent from canon; review pages are hand-mirrors. Per L1-10 **the generators exist at `knowledge/canon/`** — the reconciliation is available, not blocked | **MEASURED — owed to the conductor** |
| H-6 | `_build_integrity.py`, `gen_component_partials.py`, `gen_token_ramp.py`, `_validate_dtcg.py`, `_validate_kg.py`, `_validate_hit_area.py`, `_validate_dataviz.py` — none run | **UNPROVEN — declared** |
| H-7 | ⛔ Dave's decision list is **large and unresolved**: lane M 20 items, lane N 10, lane P 14. Two are red-law adjacent and neither was taken: the **Legacy `#DA1A00` vs `#DB0011` 1.03:1 collision** and **whether a destructive button seat should exist** (the store has none) | **UNPROVEN — Dave's** |
| H-8 | ★ Three lanes independently hit the **same** defect class in their own page-builders: a self-referential custom property `--x: var(--x)`, which CSS resolves to the initial value **silently and often plausibly**. n=3 in one wave. Same species as #184's dangling dataviz var | **CLAIMED — but n=3 makes it the wave's strongest gate candidate** |

---

## ⛔ CONSEQUENCES / PITFALLS — Dave #165

### 0 · The connection loss is the first pitfall, and it is structural

**This table was written by a finisher, not by the agent that did the work.** The BUILD-PM died before
writing it, so everything here is either (a) re-run by the finisher — tagged PROVEN/MEASURED — or
(b) **read off receipts the BUILD-PM's workers wrote about themselves** — tagged CLAIMED. **One lossy
hop.** The specific losses:

- **The BUILD-PM's own session knowledge is gone.** Any premise it verified, any stop it took, any
  decision it made that never reached a receipt **does not exist anywhere**. This table cannot know
  what it does not know. The four receipts are complete-looking, which is exactly the risk.
- **The BUILD-PM's token spend and worker count (`n=`) are unrecoverable** — the brief asked for both
  in its final message, and the final message never arrived. Not estimated here
  (`planning-estimate-is-not-a-measurement`).
- **`_validate_radius.py` (F-4) is the only hand-edited source file in the wave and no receipt of the
  editing agent survives** — only the comment it left in the file and lane 1's touched-paths table.
- **Two tracked files (F-9, F-10) are modified and NO receipt names them.** They are almost certainly
  instrument appends. "Almost certainly" is not attribution.

### 1 · What was NOT run

`_build_all.py` (⛔ hazard, correctly never approached) · `_validate_state_contrast.py` (would
overwrite a tracked audit) · `_build_memento_index.py` · `_build_integrity.py` ·
`gen_canon_components.py` / `gen_theme_cascade.py` (they **exist** — L1-10) · `gen_component_partials.py` ·
`gen_token_ramp.py` · `_validate_dtcg.py` · `_validate_kg.py` · `_validate_hit_area.py` ·
`_validate_dataviz.py` · `_validate_type_composites.py` (by the finisher) · **the CI job itself**.
⛔ **Nothing in this wave has been seen by CI**, and two of the four CI failures are still red.

### 2 · What a green cannot see

- **`_validate_snippets.py` resolves the MONO BASE ONLY.** Every Legacy / Console / Supercharge figure
  in every receipt was read off a DOM by the worker that built the thing. **rc=0 is not a four-theme
  verdict.**
- **No gate parses a review page.** The six `REVIEW-204-*.html` files are outside `snippets/`, so the
  snippet and a11y gates never look at them — and **that is exactly where all three lanes found their
  worst defects.** `no-gate-parses-the-artefact` (#122), alive.
- **No gate reads 44px for hit-area geometry.** Every hit-area number is a hand-driven *moment*
  (`conclusions-are-debt`). One padding edit erases it with every gate green.
- **No gate sees disabled-element contrast** (1.4.3 exempts it) — lane N proved a glyph at 1.00:1, and
  the gated parent ships 1.42:1.
- **No gate compares adjacent MEANINGS.** The Legacy two-red collision is between two values that each
  pass independently and that no manifest declares as a pair.
- **No gate detects `--x: var(--x)`.** Three lanes, three page-builders, three occurrences (H-8).
- **A green gate cannot tell you whether a component should exist.** Row 94 is fully green and
  originates in a **test fixture** — declining it is a legitimate answer.
- **`_gate_doc_rows.py` rc=0 is vacuous for this wave** (G-c) and will flip to rc=1 on commit.
- **A shell redirect can fail and still hand you plausible output** (section A) — two gates read RED
  off a foreign session's stale file before the re-run.

### 3 · What the adversarial verifier should attack FIRST, in order

1. **D-2 — the row-91 duplicate adjudication.** It is the one refusal in the wave, it is tagged
   **CLAIMED**, and **everything downstream of it ("don't build it") is wrong if it is wrong.** Open
   `knowledge/components/list-items.meta.json` `build.$status` / `build.scope` and
   `knowledge/snippets/List-items.reference.html`'s `<title>` **yourself**. It is cheap and it is
   load-bearing.
2. **F-9 / F-10 — the two unattributed tracked files.** Two files are staged for a commit that no
   receipt explains. Attribute them or revert them **before** the commit, not after.
3. **G-c — run `_gate_doc_rows.py` again AFTER `git add`, before committing.** It is proven to flip
   red. One `_state.add()` for the buildpm brief is the fix.
4. **H-8 — the `--x: var(--x)` class against `gen_canon_components.py`'s REAL output**, not against a
   throwaway mirror. Three lanes hit it independently. If the generator has the same shape, the bug is
   in canon, not in scaffolding. **Mutation-test it: change one theme's radius and confirm it appears.**
5. **C-6 / H-5 — regenerate `canon.css` and re-render.** All six review pages are hand-mirrors today.
   A mirror that is faithful at 09:00 is a fork by definition; lane N and lane P each found their
   mirror carrying a *neighbour's absence* rather than their own manifest.
6. **G-9 — re-run `_validate_type_composites.py` repo-wide.** Three receipts assert 1,097 unchanged;
   **the finisher did not confirm it**, and the ratchet is shrink-only, so a silent increase is exactly
   the failure it exists to catch.
7. **C-8 — schema-validate the metas from lanes N and P.** Lane M ran `jsonschema` and reported three
   PASSes. **Lanes N and P report no schema run at all.** Three metas are unvalidated.
8. **H-7's two red items** — the Legacy `1.03:1` collision and the missing destructive seat. Lane M is
   right that this and #203's arrow-seat finding are the same species and should move together, and
   **Dave is astigmatic with red as a problem hue**, which is why it is surfaced rather than absorbed.

### 4 · The failure mode I would bet on

**Not the snippets — the six review pages.** They are ungated, hand-built, hand-mirrored from a
generator that was never run, and they already produced silent defects in **all three lanes** that
eight green gates could not see. And Dave rules by eye off exactly those files.

**Second bet: the commit itself.** Two unexplained tracked files (F-9/F-10), a doc-row gate proven to
flip red on commit (G-c), and two CI steps still red (L1-3, L1-6). **A wave that gates green locally
can still land red**, and this one is currently on course to.

---

# ADDENDUM — FIX PASS, 2026-08-19 (#204 FIX sub)

*Appended, never rewritten: everything above is the finisher's claim table as written, and the
adversarial verifier's `notes/_receipts/2026-08-19-204-verifier-challenge-table.md` is unedited.
This section records only what the FIX sub CHANGED and the command that proves it. **Nothing here
is a ruling.** Three defects were repaired — C-8 (schema), NEW-1 (duplicate ids), G-c (doc row).
The two still-red CI items (`[13] _capture_gate --selftest`, `[114] _gen_chain --selftest`) were
NOT touched — declared, out of this sub's fence.*

## FIX 1 — three metas now conform to `knowledge/components/meta.schema.json` (verifier C-8)

| file | defect (verbatim from the verifier) | repair |
|---|---|---|
| `knowledge/components/document-row.meta.json` | `['stateModel'] enum: 'interactive' is not one of ['simple','full']` | `stateModel` set to **`"full"`** (the schema's documented default for a component with more than default+hover+focus). The authored word is preserved in a new `$stateModelNote` explaining the repair. |
| ″ | `['edges'] additionalProperties: 'siblingOf','contains' were unexpected` | re-keyed to the schema's own edge types: `contains` → **`hasPart`**, `siblingOf` → **`family`**. Same refs, same `$note` prose, each `$note` extended to record the original key. No edge was dropped. |
| ″ | `[] additionalProperties: 'howThisDiffersFromFileUpload','howThisDiffersFromListItems','openQuestionsForDave' do not match '^\$'` | renamed to **`$howThisDiffersFromFileUpload` / `$howThisDiffersFromListItems` / `$openQuestionsForDave`** — the annotation form the schema already permits everywhere, and the form the two passing lane-P metas use (`$differsFrom`, `$decisionsForDave`). **Bodies byte-identical.** |
| `knowledge/components/payment-card-visual.meta.json` | `['provenance','source'] enum: <300-char prose> is not one of ['figma','code','both','gap-report','proforma-promotion']` | prose moved **verbatim** into `provenance.$sourceNarrative` (`$`-keys are legal under `provenance` by the schema's own `patternProperties`); `source` set to **`"gap-report"`** — the enum value the paragraph itself describes (itinerary/gap-report origin, empty `figma_node`). |
| `knowledge/components/runway-bar.meta.json` | same enum, value begins `'⚠⚠ THIS ROW ORIGINATES IN A TEST FIXTURE…'` | identical repair. **The test-fixture warning is preserved word for word** in `provenance.$sourceNarrative`, headline first. |

⛔ **What this repair does NOT do.** It does **not** amend `meta.schema.json` and it does **not**
settle the verifier's OPEN-TO-DAVE question ("repair in place, or widen the schema with a typed
`provenance.note`?"). That question stays open and is Dave's, on the store's own precedent
(`s140-D1`, `s165-D5` — every schema amendment was ruled by Dave). This sub took the only route that
needed **no** schema decision: `$`-prefixed annotation keys, which the schema already allows.
The narrative is intact, so widening later is a lossless move.

**Verification — the full population, with the control:**

```
python3 -c "jsonschema.Draft7Validator(meta.schema.json) over glob(knowledge/components/*.meta.json)"
BEFORE : total metas=92 PASS=88 FAIL=4  (EXAMPLE-button, document-row, payment-card-visual, runway-bar)
AFTER  : total metas=92 PASS=91 FAIL=1  (EXAMPLE-button only — 'tokenValidation' is a required property)
rc=0 · zero regressions: no meta that passed before fails now
```
`EXAMPLE-button.meta.json` is the **pre-existing template** the verifier already identified as
out of scope; it is untouched. Corroborating gate: `python3 knowledge/_validate_coverage.py` →
**rc=0** · `coverage gate: 91 meta(s) / 91 snippet(s), 0 failure(s)` — all three files still parse.

## FIX 2 — duplicate `id`s removed from three review pages (verifier NEW-1)

Every `id` inside a theme pane is now suffixed `--<theme>-<mode>` (`--mono-light` … `--supercharge-dark`),
which is **the pattern lane M's clean pages already use** (`pc1--mono-light` in
`reviews/REVIEW-204-popconfirm-four-themes-v1.html`). Panes were delimited by their own
`<div class="pane" data-theme="…">` markers, 8 per page, and **every reference was rewritten inside
its own pane only**: `aria-labelledby` / `aria-describedby` / `aria-controls` / `for` / `headers`
(IDREFS split on whitespace, token by token) and `href` / `xlink:href="#…"` fragment refs.

⚠ **The one judgment made, stated plainly:** a fragment reference was rewritten **only when its
target id is defined in the same pane**. That deliberately leaves `document-row`'s demo hrefs
(`#doc-jun`, `#doc-may`, `#doc-tax`, `#doc-long`, `#dl-jun`, `#dl-may`) untouched — they are
placeholder links to ids that **exist nowhere in the document**, a pre-existing specimen habit, not
a duplicate-id defect. It is recorded here rather than silently "fixed", because inventing targets
for them would be a design decision. Same for `footer`'s `#top`. **Residual, declared, not repaired.**

**Verification — all six pages, ids counted and every ARIA reference resolved:**

```
python3 -c "Counter(id=) + resolve every aria-labelledby/describedby/controls/for/headers token"
OK   REVIEW-204-document-row-four-themes-v1.html       ids= 32 unique= 32 DUP=0 unresolved_aria=0
OK   REVIEW-204-footer-four-themes-v1.html             ids= 40 unique= 40 DUP=0 unresolved_aria=0
OK   REVIEW-204-layout-utilities-four-themes-v1.html   ids=  0 unique=  0 DUP=0 unresolved_aria=0
OK   REVIEW-204-payment-card-visual-four-themes-v1.htm ids= 56 unique= 56 DUP=0 unresolved_aria=0
OK   REVIEW-204-popconfirm-four-themes-v1.html         ids= 96 unique= 96 DUP=0 unresolved_aria=0
OK   REVIEW-204-runway-bar-four-themes-v1.html         ids= 40 unique= 40 DUP=0 unresolved_aria=0
rc=0
```
The three lane-M pages are **re-checked and unchanged** (96/40/0, the verifier's own figures) — the
control that proves this pass did not regress them. Spot-check of the defect the verifier named:
`REVIEW-204-runway-bar-…:104` now reads `aria-labelledby="rwy1-label--mono-light"` against
`id="rwy1-label--mono-light"` at `:106`, and the legacy/light pane carries `--legacy-light`.
**Seven of eight progressbars no longer take their accessible name from the mono/light pane.**

⚠ **Not re-verified:** no browser was driven. The panes render from the same markup, and only
`id`/IDREF/fragment text changed (no class, no token, no CSS selector — `#`-selectors were grepped
for and the only hits are prose in the header comments), so a visual change is not expected.
**Expected is not measured.** Dave's eye is still the test.

## FIX 3 — the doc-row gate no longer flips red on commit (verifier G-c)

`notes/_briefs/2026-08-19-204-buildpm-brief.md` had no store row. Added **`W-43`** through the
store's own writer — `_state.add()` then `_state.save()`, exactly the repair
`knowledge/_gate_doc_rows.py` prescribes in its own docstring ("the fix is one `_state.add()` row").
`home` = the brief's repo-relative path; `closes_when` references the #204 wrap landing and its CI
read-back, the same both-limbs condition `W-42` carries for this trial. **Mechanical registration of
an existing document — the row ratifies nothing in the brief.**

**Verification:**

```
_state.check()                                  → ok=True, fails=[]
git diff --numstat knowledge/_state.json        → 13  0     (pure append; no row reordered, none trimmed)
python3 knowledge/_gate_doc_rows.py             → rc=0  doc-row gate: population 13 · unrowed 0
POST-ADD SIMULATION (the verifier's own probe, re-run):
  g.unrowed(store, population() + [('2026-08-19','notes/_briefs/2026-08-19-204-buildpm-brief.md')])
                                                → []        (was [('2026-08-19', …buildpm-brief.md)])
  mutation-arm — same simulation with the W-43 home string deleted from the store text
                                                → [('2026-08-19', …buildpm-brief.md)]
                                                   (the green CAN still fail — it is not always-true)
python3 knowledge/_gate_doc_rows.py --selftest  → rc=0  fail-arm 12 unrowed · pass-arm clean · mutation-arm flagged
```

## Declared side effects and residuals

- **Tree delta from this pass:** `knowledge/_state.json` becomes the **15th** modified file (it was
  14; the verifier's sweep confirmed it was untouched then). One untracked file was added by the
  verifier, not by me (its own challenge table), taking untracked 30 → 31. **No other path changed
  state; nothing was deleted or renamed.**
- `knowledge/_COVERAGE-GATE.md` was rewritten by the corroborating coverage run — the same tracked
  audit output F-7 already declares.
- ⛔ **Untouched, as instructed:** `[13] _capture_gate.py --selftest` and `[114] _gen_chain.py
  --selftest` remain **RED**. No commit, no push, no write to `knowledge/_rulings.json`,
  `_build_all.py` never run, and `GOOD-MORNING.md` / `_CHAIN.md` / `_LIVE-STATE.md` /
  `reviews/ITINERARY-2026-07-14-*` untouched.
- **Still open to Dave (unchanged by this pass):** whether `meta.schema.json` gains a typed
  `provenance.note`; the dangling demo hrefs in `document-row` and `footer`; and every
  `⬛ PROPOSED` decision in the six components — **none of which this pass ruled on.**
