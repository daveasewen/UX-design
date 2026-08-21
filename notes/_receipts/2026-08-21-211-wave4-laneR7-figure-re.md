# LANE R7 receipt — `FIGURE_RE` and the injection-site span selectors (R6's priced latent item)

**Session** #211 findings-repair wave 4 · **lane** R7 (Opus) · **brief** `notes/_briefs/2026-08-21-211-findings-repair-wave1-v1.md`
**Repo HEAD at lane open AND at lane close** `95973cd` · **NO COMMITS MADE** · **no `git checkout`** · **no `_build_all.py`**
**Files touched: ONE** — `knowledge/gen_component_partials.py` (+145 / −14), selftest arm in-file per this repo's convention.

> ⛔ **NOTHING IN THIS RECEIPT IS A RULING.** Every DO-NOT-RULE item this lane brushed is returned PRICED, below.

---

## HEADLINE

**The injection-site selectors now select out of the document's LIVE bytes.** R6 fixed the three
CONTRACT readers; the readers that pick a **source or target SPAN** out of the file were left raw, and
one of them was live-adjacent. All three are now fixed with one discipline — **LOCATE LIVE, SLICE RAW** —
and R6's fence (the markers that *are* HTML comments) is untouched and still driven in both directions.

★ **THE EXPOSURE WAS WORSE THAN "a commented figure gets injected into", and this was MEASURED, not
assumed.** `FIGURE_RE` is `<figure\b.*?</figure>` under `re.S` — **non-greedy across newlines**. The
`<figure>` inside `Image-block.reference.html`'s prose header (offset 368) has **no `</figure>` in that
comment**, so the raw match ran **from the comment to the first REAL `</figure>`**: one span
`(368, 7777)` **swallowing the whole prose block AND the file's first real figure**. Live selection
gives `(6915, 7777)` — the real figure. A commented `<figure>` did not add a bogus injection site;
it **ate a real one**.

★ **DRIVEN ON THE REAL GENERATOR, NOT ON A PROPERTY.** Fixture: a copy of the whole snippet tree with
that exact prose shape planted above `Chart-line`'s first real figure. **BEFORE the fix the generator
injected 2 blocks instead of 4, dropped the first chart's title entirely, and raised 2 extra loud
contract failures. AFTER, 4/4 injected, both titles rendered, failures back to the control's.** The
real-figure control is **byte-identical BEFORE and AFTER**.

★ **THE SYNC STAYED A NO-OP.** Write mode ran twice on the real tree; **147 hashed files, zero
changed; `git status --short` byte-identical across the write run, both times.** Blast radius asked
BEFORE any edit landed in the numbers: **0 new failures, 0 new out-of-sync**. **No regen decision comes
back to the conductor.**

**Mutant matrix 5/5 bite with a green control — after TWO SURVIVORS were found, named and closed.**

---

## THE DEFECT, AT CAUSE

`run()` walked figures with `FIGURE_RE.sub(process_fig, html)` over **raw** text. R6's mask existed but
stopped at the contract readers. Three selectors still read raw:

| selector | what it picks | raw exposure |
|---|---|---|
| `FIGURE_RE` (in `run`) | the per-occurrence AUTO-MARKUP injection site | **1 live occurrence, span-swallowing (above)** |
| `source_block` | the atom's PARTIAL CSS — the payload injected into every consumer | 0 today (latent) |
| `AUTO_RE` (in `run`) | the consumer's injection TARGET span | 0 today (latent) |

**The fix is one discipline, applied three times: LOCATE the span in the comment-masked copy, SLICE the
bytes from the ORIGINAL.** That is exactly what R6's `manifest_vars` already does, and it is why
`mask_comments`' length-preservation is a **property with real consumers** rather than a convenience.

New machinery, all in this one file:

- `live_match(rx, html)` — `rx` searched against the live copy; **group spans transfer index-for-index**, so the caller compares and rewrites the original bytes.
- `live_figure_spans(html)` — spans of every LIVE `<figure>…</figure>`.
- `rewrite_live_figures(html, fn)` — rebuilds the document with `fn` applied to each live figure, **splicing the original bytes either side**. ⛔ `fn` receives the figure's **original** bytes, never the mask.

⛔ **THE R6 FENCE IS UNTOUCHED AND NOT WIDENED.** `BEHAVIOUR_RE`, `AUTO_MARKUP_RE`,
`markup_source_block` and `non_consumer_marker_fails` read markers that **ARE HTML comments by design**
and still read RAW text. Masking a figure's *contents* rather than its *selection* would blank **all 80
AUTO-MARKUP markers** and the generator would silently inject nothing — that is mutant **M2**, and it is
why `rewrite_live_figures` hands the callback raw bytes.

---

## INJECTION-SITE CENSUS — every span selector in the file, NAMED, with its verdict

Population **147** documents (`knowledge/snippets/*.reference.html` = 135, plus `knowledge/_proforma/*.html` = 12).
"inside an HTML comment" is asked of the token's start offset against `live_text()` of the same file.

| # | selector | what it selects | occurrences | inside a comment | verdict |
|---|---|---|---|---|---|
| 1 | `FIGURE_RE` via `run()` | injection site (per `<figure>`) | 58 | **1** | ★ **FIXED — `live_figure_spans` + `rewrite_live_figures`** |
| 2 | `source_block` | the atom's PARTIAL CSS payload | 3 START markers (24 PARTIAL markers total) | **0** | ★ **FIXED — located live, sliced raw** |
| 3 | `AUTO_RE` via `run()` | the consumer's injection TARGET | 23 START markers (46 AUTO-PARTIAL markers total) | **0** | ★ **FIXED — `live_match`, span-spliced** |
| 4 | `MANIFEST_RE` / `manifest_vars` | the document's manifest | 145 | **0** | already fixed by R6 — unchanged |
| 5 | `figure_attrs` | `data-lockup-*` off a figure's opening tag | — | n/a | **left raw, DELIBERATE** — it is handed an already-LIVE-selected figure and reads its offset-0 opening tag; it selects nothing itself |
| 6 | `render_markup` · `rewrite_selectors` · `markup_provenance` | already-extracted fragments | — | — | not exposed — never sees a document |
| 7 | `BEHAVIOUR_RE` | AUTO-BEHAVIOUR marker pair | 48 markers | (is a comment) | ⛔ **MUST NOT MASK** — R6 fence, mutant M2 |
| 8 | `AUTO_MARKUP_RE` | AUTO-MARKUP marker pair | 80 markers | (is a comment) | ⛔ **MUST NOT MASK** — R6 fence, mutant M2 |
| 9 | `markup_source_block` | MARKUP source fragment | 4 markers | (is a comment) | ⛔ **MUST NOT MASK** — R6 fence |
| 10 | `non_consumer_marker_fails` | delegates to `BEHAVIOUR_RE` | — | — | ⛔ **MUST NOT MASK** — R6 fence |

⚠ **A RECONCILIATION WITH R6's OWN CENSUS, DECLARED.** R6 reported rows 2/3 as "24" and "46"
occurrences; I report "3" and "23" START markers. **Both are right and neither is the other's
correction** — R6 counted every marker (START **and** END, so 24 = 12 pairs, 46 = 23 pairs); I counted
only the START marker each selector actually anchors on. Verified with a third instrument:
`grep -ro "===== PARTIAL " → 24` and `grep -ro "===== AUTO-PARTIAL " → 46`. **The inside-a-comment
answer is 0 under both countings**, which is the number the verdict rests on. [[measure-dont-convert-units]]:
name the unit — "markers" and "anchor sites" are different units.

---

## CLAIM TABLE (`s182-D1` — every mechanical claim carries a probeable token)

All commands run from the repo root, `/sessions/loving-dreamy-wright/mnt/UX-design`.

| # | claim | probeable token | verdict |
|---|---|---|---|
| 1 | **`Image-block.reference.html` carries a `<figure` inside its prose header comment, at offset 368** | `python3 /var/tmp/r7/census.py` → `HIT ('knowledge/snippets/Image-block.reference.html', 368, '<figure>/<figcaption> semantics: an image area,…')` | ✅ DRIVEN |
| 2 | ★ **Read RAW, that match SWALLOWS the file's first real figure** — one span from the comment to the first real `</figure>` | same run → `DELTA knowledge/snippets/Image-block.reference.html raw=6 live=6 first raw [(368, 7777), …] first live [(6915, 7777), …]` | ✅ DRIVEN |
| 3 | It is the ONLY such occurrence in the tree | same run → `population: 147` · `FIGURE_RE raw occurrences=58 INSIDE-COMMENT=1` | ✅ DRIVEN |
| 4 | **It is LATENT, not live — `Image-block` is not a member of the only `$markup` group** | `python3 -c` over `component-types.json` → `group with $markup: dataviz \| members: ['Chart-bar',…,'Chart-stacked-area']` · `Image-block a member of any $markup group: False` | ✅ DRIVEN (R6's finding, re-measured) |
| 5 | ★ **MUTATION F1 — BEFORE the fix, the generator selects the COMMENTED span and under-injects** | `python3 /var/tmp/r7/mut.py` → `BEFORE selector=FIGURE_RE.finditer (raw) first span=(24336, 40794) starts '<figure>/<figcaption>⏎ semantics…'` · `injected=2 Chart-line-related fails=4` · `titles rendered into Chart-line: ['Savings drove growth across every product']` | ✅ DRIVEN |
| 6 | ★ **AFTER the fix it selects the REAL figure and injects all four** | same run → `AFTER selector=live_figure_spans first span=(24424, 40794) starts '<figure class="dv dv-animate" data-dv-type="li'` · `injected=4 … fails=2` · `titles … ['Balance climbed steadily through the year', 'Savings drove growth across every product']` | ✅ DRIVEN |
| 7 | **The defect's LOUD face: two extra contract failures that vanish after the fix** | `python3` fails-diff over the same fixture → `dataviz/markup/dv-lockup-title: Chart-line: figure missing data-lockup-title (required to render dv-lockup-title)` + the `dv-lockup-table` twin · `counts BEFORE=4 AFTER=2` · `output bytes identical BEFORE vs AFTER: False` (`len BEFORE=97788 AFTER=98835`) | ✅ DRIVEN |
| 8 | ★ **REAL-FIGURE CONTROL UNCHANGED (no over-reach)** | same run, arm `F2` → BEFORE and AFTER both `first span=(24274, 40644)` · `injected=4` · `fails=2` · identical titles | ✅ DRIVEN |
| 9 | **BLAST RADIUS on the live tree: ZERO new failures, asked BEFORE/AFTER side by side** | `python3 /var/tmp/r7/blast.py` → `BEFORE(HEAD) fails=0 out_of_sync=0 injected=0` · `AFTER (fix) fails=0 out_of_sync=0 injected=0` · `fails identical: True \| out_of_sync identical: True` | ✅ DRIVEN |
| 10 | ★ **THE SYNC IS A NO-OP — nothing rewritten** | `md5sum` of all **147** files under `knowledge/snippets` + `knowledge/_proforma`, before and after `python3 knowledge/gen_component_partials.py` (write mode) → `diff` empty, `HASHES IDENTICAL across the write run (147 files, 0 changed)`; generator's own line `0 consumer block(s) injected/refreshed (all in sync)` rc=0 | ✅ DRIVEN (twice — mid-lane and on the final file) |
| 11 | ★ **`git status --short` byte-identical across the write run** | `git status --short > before` … write run … `> after`; `diff` → empty, `GIT STATUS BYTE-IDENTICAL across the write run` | ✅ DRIVEN |
| 12 | **STEP [38] green** | `python3 knowledge/gen_component_partials.py --check` → `gen_component_partials --check OK — all AUTO-PARTIAL blocks in sync, contracts hold.` **rc=0** | ✅ DRIVEN |
| 13 | **STEP [39] green** | `python3 knowledge/gen_component_partials.py --selftest` → `gen_component_partials selftest OK` **rc=0** | ✅ DRIVEN |
| 14 | ⚠ **The step numbers [38]/[39] are 1-BASED RUNNER labels, not list indices** — read off `STEPS` and off the printer | `ast.literal_eval` of the `STEPS` assign → `len(STEPS) = 128`, `STEP [37] (…'--check')`, `STEP [38] (…'--selftest')` **0-based**; `knowledge/_build_all.py:1182` `for i, step in enumerate(STEPS[start - 1:end], start)` + `:1186` `print(f"\n=== [{i}/{len(STEPS)}] …")` ⇒ the runner prints **[38]/[39]**. R6's and the brief's numbers are the RUNNER's and are correct. | ✅ DRIVEN |
| 15 | No document in the tree carries a literal `<!--` inside a `<style>` block (why masking the CSS selectors is safe — MEASURED, not assumed) | `python3 /var/tmp/r7/census2.py` → `style blocks containing a literal '<!--' (CDO risk for masking CSS readers): 0 []` | ✅ DRIVEN |
| 16 | Nothing outside this file imports the changed functions | `grep -rn "live_figure_spans\|rewrite_live_figures\|source_block\|live_match\|FIGURE_RE" --include=*.py knowledge/ \| grep -v gen_component_partials.py` → only `_validate_kg`-class **local name collisions**: `knowledge/_validate_evidence.py:106,172` defines its OWN unrelated `FIGURE_RE` (a numbers-in-prose regex). **No importer of this module exists.** | ✅ DRIVEN |
| 17 | The masked selection costs nothing measurable | `time python3 knowledge/gen_component_partials.py --check` → `real 0m0.138s` (R6 measured `0m0.136s`) | ✅ DRIVEN |
| 18 | The file still compiles | `python3 -m py_compile knowledge/gen_component_partials.py` → rc=0, `COMPILE_OK`; `__pycache__/` gitignored (`.gitignore:8`) | ✅ DRIVEN |
| 19 | Diff size, read off git not off memory | `git diff --stat -- knowledge/gen_component_partials.py` → `1 file changed, 145 insertions(+), 14 deletions(-)` | ✅ DRIVEN |

### Mutation matrix — the CLAUSE **and the CALL SITE** [[mutation-tests-the-clause-not-the-feature]]

Harness `(NON-REPO: /var/tmp/r7/mutants.py)` — each mutant edits a **copy** of the fixed generator,
written to **its own path under its own module name with `sys.dont_write_bytecode = True`** (R6's
stale-`.pyc` trap, its receipt § THE HARNESS LIED ONCE). Every mutant reports **which arm caught it**.

| mutant | rc | caught by | verdict |
|---|---|---|---|
| **M0 — none (green control)** | 0 | — | ✅ **GREEN** |
| M1 — `live_figure_spans` reads RAW text (the defect restored) | 1 | `live_figure_spans selected a <figure> named inside an HTML comment (#211 lane R7)` + `rewrite_live_figures handed the callback the wrong figure bytes` | ✅ BITES |
| M2 — **FENCE BREACH**: the figure is sliced from the MASK, not the original bytes | 1 | `rewrite_live_figures is not byte-identity under an identity callback` + `…wrong figure bytes` + `the figure reached the injection callback as MASKED bytes` | ✅ BITES |
| M3 — `source_block` locates in RAW text again | 1 | `source_block read a PARTIAL block sitting inside an HTML comment as the atom's source of truth` | ✅ BITES |
| M4 — `source_block` returns the MASKED bytes instead of the original CSS | 1 | `source_block returned MASKED bytes instead of the original CSS` | ✅ BITES |
| M5 — `live_match` matches against RAW text | 1 | `an AUTO-PARTIAL marker pair inside an HTML comment was selected as an injection target` | ✅ BITES |

### ⛔ TWO MUTANTS SURVIVED THE FIRST MATRIX, AND THE CORRECTION IS THE POINT

**First run: M2 and M4 came back `GREEN`.** Both survivals were real holes in my own arms, and both are
the same shape — **the arm tested the clause I wrote, not the thing the generator runs**:

1. **M2 survived because the splice was an INLINE LOOP inside `run()`.** My arm checked
   `AUTO_MARKUP_RE.search(doc_fig[a:b])` — a re-implementation of the splice — so mutating the real
   splice changed nothing the selftest could see. **Fix: the loop was lifted into a named
   `rewrite_live_figures(html, fn)` that `run()` calls, and the arm now drives THAT function with a
   probe callback** which records the bytes it was handed. This is `[[mutation-tests-the-clause-not-the-feature]]`
   at the *harness/seam* layer: a test that re-implements its subject cannot fail with it.
2. **M4 survived because my control document had nothing to distinguish.** The `source_block` control
   CSS contained no HTML comment, so masked bytes and raw bytes were **identical** — the arm could not
   tell `html[m.start(1):m.end(1)]` from `m.group(1)`. **Fix: a second control whose PARTIAL payload
   contains an HTML comment**, so a masked return injects blanks where the source held bytes.
   ⚠ That document shape has **0 live occurrences today** (claim 15) — it is a **latent** shape, the
   same class I was sent to close, and it is labelled as such in the arm's own comment.

★ **A mutant matrix is only as honest as the run you report.** The first table would have read
`5/5 BITES` had I written the arms slightly differently and not run the mutants; it read `3/5` and the
two survivors bought a real structural improvement.

---

## WHAT WAS DRIVEN vs WHAT STAYS UNPROVEN

**DRIVEN** — the generator's two build steps ([38] `--check`, [39] `--selftest`), write mode on the
real tree (twice), the BEFORE/AFTER module pair loaded side by side on the live tree, the end-to-end
fixture injection with a control, the 147-document census, the 147-file hash diff, the `git status`
diff, the mutant matrix, compile, timing, the step-number re-derivation.

**Fixtures**: built in `/var/tmp/r7/` from **copies** of `knowledge/snippets/` (the whole tree, copied
per arm). **No tracked snippet was edited and no fixture is homed in the repo** —
`(NON-REPO: /var/tmp/r7/)`, `s191-D2` marker carried in every harness header (`census.py`, `census2.py`,
`blast.py`, `mut.py`, `mutants.py`).

**UNPROVEN — each a priced TODO, none smoothed:**

1. **Nothing was rendered.** This lane changed span *selection*, and the sync is a proven byte-level
   no-op (claims 10/11), so no pixel can have moved. That is an inference from "no bytes changed", not
   a render. Price: **0** — there is nothing to look at.
2. **No `_build_all.py` run** (hard fence). Steps [38]/[39] were driven standalone, both rc=0. **The
   other 126 steps are UNRUN by this lane.** Price: the conductor's serial.
3. **P-7 / P-8 not re-run.** Same reasoning R6 gave and it still holds: this lane wrote **zero artefact
   bytes**, so no probe count can have moved by my hand, and a figure taken on a tree where sibling
   lanes are landing would be unattributable. Price: ~1 min at the serial, on a still tree
   [[conclusions-are-debt-s129-d5]].
4. **`FIGURE_RE` is still a REGEX, not an HTML parse.** It now selects out of the right bytes, but
   `<figure\b.*?</figure>` still cannot see **nested** figures, a `</figure>` inside a string or
   attribute, or an unclosed figure. [[no-gate-parses-the-artefact]] is **NOT discharged** — named so
   nobody reads "comment-masked" as "parses HTML". Price: an `html.parser`/`lxml` rewrite of the walk,
   ~45–60 min + its own blast-radius run.
5. **`mask_comments` is still duplicated** with `gen_token_ramp`'s (R6's UNPROVEN #4, unchanged and
   **not mine to fix** — `gen_token_ramp` is lane R1's file). The two can drift; no gate compares them.
   Price: ~20 min, and it crosses a fence.
6. **The C2 gate (`_validate_property_resolves.py`) is still HTML-comment-blind** — R1's priced,
   unwired item. A human can still hand-write this class into a snippet.
7. **`figure_attrs` reads raw and is argued safe, not proven exhaustively.** The argument is that it
   only ever sees an already-live-selected figure and reads its offset-0 opening tag. If a future
   caller hands it something else, the argument lapses. No gate enforces that precondition.
   Price: ~5 min for an assert, **not added** — a repair does not add fences nobody asked for.

---

## PROBE DELTAS

**None asked, deliberately** — see UNPROVEN #3. **Zero artefact bytes written** (claims 10/11), so no
P-7/P-8 count can have moved by my hand. The conductor should take both at the serial on a still tree.

---

## ⛔ DO-NOT-RULE ITEMS THIS LANE BRUSHED — RETURNED PRICED, NOTHING SETTLED

| item | how this lane brushed it | returned as |
|---|---|---|
| **ANY threshold, constant or count in gates** (`s208-D1` rider) | none moved | **Nothing dialed.** No numeral in this file changed. The selftest **gained** arm 5g; **no existing arm was removed, relaxed, narrowed or renamed** (`_RUNBOOK-parallel-conductor.md:69`). Every generator output string is untouched. |
| **P-7 / P-8 promotion or park** (`W-85`) | not measured | **Untouched. Not proposed.** Still ADVISORY, still Dave's. |
| **the 34 proposed organisms + REVIEW-210 pages** (his eye queue) | `Image-block` was **read** (the finding's subject); the snippet tree was **copied** to `/var/tmp` as a fixture | **Zero tracked bytes written. No design content judged or altered.** `Image-block` is Dave's `W-71` item and I neither edited it nor proposed an edit — the comment stays exactly as authored. |
| **whether a commented-out figure should ever be an injection site** | this is the fix's premise | ⚠ **NOT a design ruling and I claim no licence for one.** The generator now treats prose as prose. If Dave ever wants the opposite, the answer is a real marker, not a raw-text match. |
| **`knowledge/assets/photography/`** (2.5GB untracked, conductor is fencing it) | **never read, never staged, never touched.** My hashes cover `knowledge/snippets` + `knowledge/_proforma` only | **Untouched.** The ` M .gitignore` in the status listing is the **conductor's**, not mine. |
| **`gen_token_ramp.py`** (lane R1's file) | the duplicated `mask_comments` still invites a shared helper | ⛔ **NOT TOUCHED — outside my fence.** UNPROVEN #5. |

---

## CONSEQUENCES / PITFALLS (mandatory, Dave #165)

**What could recur:**

1. **The fence is now protected by ONE named function.** `rewrite_live_figures` exists in that shape so
   mutant M2 has something to bite. If a future edit inlines it back into `run()` "for clarity", **the
   fence goes silent again exactly as it was silent in my first matrix**. It is named here so the
   function reads as load-bearing, not as indirection.
2. **A test that re-implements its subject cannot fail with it.** That is the general lesson from M2's
   survival, and it is **REPORTED, NOT WIRED** — extending other lanes' harnesses is not a repair's job.
3. **Masking a CSS-marker selector is only safe while no `<style>` block contains `<!--`.** Measured 0
   today (claim 15). If one ever appears, `source_block` / `AUTO_RE` would fail to locate their markers
   — **loudly** (`… carries no AUTO-PARTIAL markers`), never silently — but the message would name the
   wrong cause. Priced: ~10 min to add a `<!--`-in-`<style>` detector to the loud message. **Not wired.**
4. **The AUTO-PARTIAL leg now rewrites by SPAN, not by `rx.sub`.** Behaviour is identical while there
   is exactly one marker pair per file (the shape today); if a file ever carried two pairs for the same
   partial, span-splice and `sub(count=1)` both take the first — same semantics, but nothing gates it.
5. **`_validate_evidence.py` has its own unrelated `FIGURE_RE`.** A grep for the name spans two
   meanings — the `W-59` local-name-collision class, **reported not repaired** (different file).

**What this repair does NOT fix:**

- The C2 gate's HTML-comment blindness (R1's priced, unwired item).
- Anything about *parsing*: `FIGURE_RE` still cannot see nested or unclosed figures (UNPROVEN #4).
- `mask_comments` duplication across two generators (UNPROVEN #5).
- The 12 ABSENT P-8 findings in four templates — untouched, outside every fence I can see.

**Which class it belongs to:** [[no-gate-parses-the-artefact]] — the selector did not read in the
consumer's grammar — compounded with [[conflated-fix-guarantees-recurrence]], which is why all three
raw span selectors were fixed together rather than only the one the brief named, and with
[[mutation-tests-the-clause-not-the-feature]], which is what the two surviving mutants were.

---

## `git status --short` — READ BACK VERBATIM AT LANE CLOSE

Taken AFTER this receipt was written, so the listing includes itself — a status read taken before the
receipt exists is a listing of a moment that no longer applies by the time anyone reads it:

```
 M .gitignore
 M knowledge/gen_component_partials.py
?? notes/_receipts/2026-08-21-211-wave4-laneR7-figure-re.md
```

**Every path attributed:**

| path | whose |
|---|---|
| `.gitignore` | **THE CONDUCTOR'S** — the `knowledge/assets/photography/` fence named in my brief. Not mine, not read, not staged. |
| `knowledge/gen_component_partials.py` | **MINE** — the fix + selftest arm 5g (+145 / −14) |
| `?? notes/_receipts/…-wave4-laneR7-figure-re.md` | **MINE** — this receipt |

★ **The `.gitignore` path is attributed by EVIDENCE, not elimination**: it was already ` M` in my
**opening** `git status --short` at HEAD `95973cd`, **before I made any edit**, and my brief names the
conductor as the one fencing that directory.

⚠ **The tree is shared and this listing is a MOMENT, not a state** [[conclusions-are-debt-s129-d5]] —
re-read it at the conductor's serial.

**No gate I ran wrote a tracked file.** `--check`, `--selftest` and **write mode** were all run; only my
own edit appears. `knowledge/__pycache__/` is gitignored (`.gitignore:8`).

**Environment change, declared: NONE.** No `pip install`, no download, no browser, no new dependency.

**NO COMMITS. NO `git checkout`. NO `_build_all.py`.** HEAD `95973cd` at open and at close.

---

## SUB SPEND

⛔ **NOT MEASURABLE FROM INSIDE THE LANE — declared UNKNOWN rather than estimated**
[[feedback-measuring-tool-must-not-guess]]. A sub cannot read its own `message.usage`; the conductor
takes the figure from the sub's usage record for the `subs N tokens (n=…)` line at wrap. Reported as a
**shape**, labelled as such: **2 briefing-file reads (both required by the brief), 1 target file read,
~12 bash calls, 8 edits, 1 receipt write, no renders, no browser, no `_build_all` run.**
