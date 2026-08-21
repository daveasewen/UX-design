# LANE R6 receipt — `gen_component_partials.declared_value()` comment defect (R1's priced sibling)

**Session** #211 findings-repair wave 3 · **lane** R6 (Opus) · **brief** `notes/_briefs/2026-08-21-211-findings-repair-wave1-v1.md`
**Repo HEAD at lane open AND at lane close** `652d432` · **NO COMMITS MADE** · **no `git checkout`** · **no `_build_all.py`**
**Files touched: ONE** — `knowledge/gen_component_partials.py` (+112 / −5), selftest arms in-file per this repo's convention.

> ⛔ **NOTHING IN THIS RECEIPT IS A RULING.** Every DO-NOT-RULE item this lane brushed is returned PRICED, below.

---

## HEADLINE

**The contract readers now read the document's LIVE bytes, not its prose.** Three readers in this file
fail-open on commented-out content; all three are fixed with the length-preserving comment mask lane R1
proved, and the fence — the markers that *are* HTML comments — is driven in both directions.

**Mutation-tested 7/7 with a green control** (`M0` green, `M1`–`M7` all bite, each on its own named arm).
**Before the fix, `declared_value()` returned `'2'` for a `--press-travel` that existed only inside an HTML
comment; after, it returns `None` and the contract fails loud. A real uncommented declaration still returns `'2'`.**

★ **THE SYNC STAYED A NO-OP.** Write mode ran; **159 hashed files, zero changed; `git status --short`
byte-identical before and after.** The gate was **not** green over live defects — blast radius measured at
**0 new failures** on all three readers before a line was edited. **No regen decision comes back to the conductor.**

---

## THE DEFECT, AT CAUSE

`declared_value()` asked the **raw** html:

```python
m = re.search(re.escape(var) + r'\s*:\s*([^;]+);', html)     # HEAD
```

so `<!-- the control used to carry --press-travel:2; here -->` **satisfied `requires.vars`**, and supplied a
`matchValues` comparand. This is R1's class exactly: raw-text reading satisfied by content inside HTML comments —
the shape that silently killed 120 declarations through `gen_token_ramp`, and that ds-018's C2 gate was green over.

**Two siblings in the SAME file carry the SAME exposure**, and fixing one face and not the others is
[[conflated-fix-guarantees-recurrence]]:

- `check_contracts()`'s `declarations` test — `if needle not in html` — a required declaration present **only in a
  comment** satisfied the contract.
- `manifest_vars()` — a whole `<script id="token-manifest">` inside a comment was read as the document's manifest.
  Measured: a commented-out manifest yielded **22 live bindings** to the `$manifestBinds` check.

**The fix**: `mask_comments()` (length- and newline-preserving; an unterminated `<!--` masks to EOF, as a browser
reads it), memoised through `live_text()`. `declared_value` and the `declarations` test read the masked copy.
`manifest_vars` is **LOCATED** in the masked copy but **PARSED from the original bytes at that span** — so the mask
can never corrupt the JSON it helped find. That makes length-preservation a **property with a real consumer**, not a
convenience, which is why mutant `M4` bites.

⛔ **THE MASK IS FENCED.** It is applied to the three CONTRACT readers only. `BEHAVIOUR_RE`, `AUTO_MARKUP_RE`,
`markup_source_block` and `non_consumer_marker_fails` read markers that **ARE HTML comments by design** — masking
there would blind the generator to its own injection sites. Measured cost of over-reach: **4 + 80 + 48 = 132 markers
lost.** Mutant `M6` drives the fence.

---

## SIBLING CENSUS — every raw-text reader in the file, NAMED, with its verdict

Population: **135 snippet files**. "inside an HTML comment" is asked of the token's start offset against the
comment spans of the same file.

| # | reader | line (HEAD) | what it reads | occurrences | inside a comment | verdict |
|---|---|---|---|---|---|---|
| 1 | `declared_value` | 199 | raw html for `--var: value;` | — | — | ★ **FIXED — masked** |
| 2 | `check_contracts` `declarations` | 229 | raw substring `needle not in html` | — | — | ★ **FIXED — masked** |
| 3 | `manifest_vars` / `MANIFEST_RE` | 204/206 | `<script id="token-manifest">` | 135 | **0** | ★ **FIXED — located masked, parsed raw** |
| 4 | `source_block` | 79 | `/* ===== PARTIAL … */` (CSS comment) | 24 | **0** | left raw — explicit human-placed markers, **0 live exposure measured** |
| 5 | `AUTO_RE` | 85 | `/* ===== AUTO-PARTIAL … */` (CSS comment) | 46 | **0** | left raw — same, **0 live exposure measured** |
| 6 | `FIGURE_RE` / `figure_attrs` | 104/106 | raw `<figure` | 43 | **1** | ⚠ **LATENT — reported priced below, NOT touched** |
| 7 | `BEHAVIOUR_RE` | 90 | `<!-- ===== AUTO-BEHAVIOUR … -->` | 48 | (is a comment) | ⛔ **MUST NOT MASK** — fence, `M6` |
| 8 | `AUTO_MARKUP_RE` | 121 | `<!-- ===== AUTO-MARKUP … -->` | 80 | (is a comment) | ⛔ **MUST NOT MASK** — fence, `M6` |
| 9 | `markup_source_block` | 117 | `<!-- ===== MARKUP … -->` | 4 | (is a comment) | ⛔ **MUST NOT MASK** — fence, `M6` |
| 10 | `non_consumer_marker_fails` | 174 | delegates to `BEHAVIOUR_RE` | — | — | ⛔ **MUST NOT MASK** — fence, `M6` |
| 11 | `rewrite_selectors` · `render_markup` | 182/125 | already-extracted fragments | — | — | not exposed — never sees a document |
| 12 | `load_registry` · `check_caches` · `_resolve_semantic` | 67/259/240 | JSON stores | — | — | not exposed — no HTML grammar |

⚠ **A CORRECTION TO MY OWN FIRST PROBE, DECLARED.** My initial census reported "4 MARKUP markers sit inside an
HTML comment" in `Chart-combo`. **That was the probe's artefact, not a finding** — a `<!-- ===== MARKUP … -->`
marker *is* an HTML comment, so masking necessarily blanks its own start offset. Rows 7–9 above therefore ask a
different question (*would a mask lose them?*), which is the question that matters for those readers.
[[unmatched-grep-is-not-an-absence]] cuts both ways: a **matched** grep is not a presence either.

---

## CLAIM TABLE (`s182-D1` — every mechanical claim carries a probeable token)

All commands run from the repo root, `/sessions/loving-dreamy-wright/mnt/UX-design`.

| # | claim | probeable token | verdict |
|---|---|---|---|
| 1 | **BEFORE the fix, a declaration living ONLY inside an HTML comment satisfied `declared_value`** | `python3 /var/tmp/r6fix/mut.py` → row `F1 planted-in-COMMENT  BEFORE  '2'  ACCEPTS  0` | ✅ DRIVEN |
| 2 | **AFTER the fix it is rejected, and the contract fails LOUD** | same run → `F1 planted-in-COMMENT  AFTER  None  REJECTS  1  Icon-button: required var --press-travel not declared` | ✅ DRIVEN |
| 3 | **A real uncommented declaration is still accepted (no over-reach)** | same run → `F2 real declaration (control)  BEFORE '2' ACCEPTS` / `AFTER '2' ACCEPTS` | ✅ DRIVEN |
| 4 | `manifest_vars` read a commented-out manifest as 22 live bindings; now reads 0; the real manifest still reads 22 | same run → `F3 manifest-only-in-COMMENT BEFORE vars=22 AFTER vars=0` · `F3 control BEFORE vars=22 AFTER vars=22` | ✅ DRIVEN |
| 5 | The `declarations` substring test was satisfied by commented text; now fails; the real declaration still passes | same run → `F4 declarations-in-COMMENT BEFORE fails=0 AFTER fails=1` · `F4 control BEFORE fails=0 AFTER fails=0` | ✅ DRIVEN |
| 6 | **BLAST RADIUS: masking adds ZERO failures on the live tree** (asked BEFORE any edit, by monkeypatching HEAD) | `python3 /var/tmp/r6_blast.py` → `BASELINE fails=0 oos=0` · `A declared_value MASKED fails=0` · `B whole-contract MASKED fails=0` · `C manifest_vars MASKED fails=0` | ✅ DRIVEN |
| 7 | **STEP [38] green** | `python3 knowledge/gen_component_partials.py --check` → `gen_component_partials --check OK — all AUTO-PARTIAL blocks in sync, contracts hold.` **rc=0** | ✅ DRIVEN |
| 8 | **STEP [39] green** | `python3 knowledge/gen_component_partials.py --selftest` → `gen_component_partials selftest OK` **rc=0** | ✅ DRIVEN |
| 9 | ★ **The step numbers are [38]/[39], read off `STEPS` itself — my own hand count said [27]/[28] and was WRONG** | `ast.literal_eval` of the `STEPS` assign in `knowledge/_build_all.py` → `len(STEPS) = 128` · `STEP [38] component-partials sync … ['--check']` · `STEP [39] component-partials selftest … ['--selftest']` | ✅ DRIVEN |
| 10 | ★ **THE SYNC IS A NO-OP — nothing rewritten** | `md5sum` of all 159 files under `knowledge/snippets` + `knowledge/_proforma`, before and after `python3 knowledge/gen_component_partials.py` (write mode) → `diff` empty; generator's own line: `0 consumer block(s) injected/refreshed (all in sync)` rc=0 | ✅ DRIVEN |
| 11 | ★ **`git status --short` is byte-identical across the write run** | `git status --short > before` … write run … `> after`; `diff before after` → empty | ✅ DRIVEN |
| 12 | Blast radius is contained to this one file — nothing imports these functions | `grep -rn "declared_value\|manifest_vars" --include=*.py knowledge/ \| grep -v gen_component_partials.py` → only unrelated **local names** (`gen_showroom.py:415` and `canon/gen_theme_cascade.py:464` take a *parameter* named `manifest_vars`; `_validate_kg.py:313` has a *local* named `live_text`). No importer of this module exists. | ✅ DRIVEN |
| 13 | The masked reads cost nothing measurable | `time python3 knowledge/gen_component_partials.py --check` → `real 0m0.136s` | ✅ DRIVEN |
| 14 | The file still compiles | `python3 -m py_compile knowledge/gen_component_partials.py` → rc=0, `COMPILE_OK`; `__pycache__/` is gitignored (`git check-ignore -v` → `.gitignore:8:__pycache__/`) | ✅ DRIVEN |
| 15 | No `/* PARTIAL */` or `/* AUTO-PARTIAL */` marker sits inside an HTML comment on the live tree (why rows 4–5 were left raw — MEASURED, not asserted) | the census script in § SIBLING CENSUS → `PARTIAL occurrences=24 INSIDE=0 []` · `AUTO-PARTIAL occurrences=46 INSIDE=0 []` | ✅ DRIVEN |
| 16 | Masking the HTML-comment markers would blind the generator to 132 injection sites | same census → `MARKUP 4→0` · `AUTO-MARKUP 80→0` · `AUTO-BEHAVIOUR 48→0` | ✅ DRIVEN |

### Mutation matrix — the CLAUSE, not the feature [[mutation-tests-the-clause-not-the-feature]]

Harness: `(NON-REPO: /var/tmp/r6fix/mutants.py)` — edits a **copy** of the fixed generator, reloads it with its
repo paths restored, runs `selftest()`. Verdict `BITES` = selftest rc 1. **Every mutant is reported with the arm
that caught it**, so a mutant "caught" by an unrelated arm cannot pass as a pass.

| mutant | rc | caught by | verdict |
|---|---|---|---|
| **M0 — none (green control)** | 0 | — | ✅ **GREEN** |
| M1 — `declared_value` reads RAW html (the defect restored) | 1 | `declared_value satisfied by a declaration inside an HTML comment (#211 class)` | ✅ BITES |
| M2 — `declarations` substring test reads RAW html | 1 | `required declaration satisfied by text inside an HTML comment (#211 class)` | ✅ BITES |
| M3 — `manifest_vars` reads RAW html | 1 | `manifest_vars read a #token-manifest sitting inside an HTML comment (#211 class)` | ✅ BITES |
| M4 — `mask_comments` stops PRESERVING LENGTH | 1 | `mask_comments stopped preserving length — manifest_vars' span misaligns` | ✅ BITES |
| M5 — an unterminated `<!--` no longer masks to EOF | 1 | `an unterminated <!-- did not mask to EOF (a browser reads it as a comment)` | ✅ BITES |
| M6 — **FENCE BREACH**: the mask reaches the HTML-comment injection markers | 1 | `non-consumer carrying AUTO-BEHAVIOUR markers not refused (inert payload undetected)` | ✅ BITES |
| M7 — the memo cache returns a STALE mask for a different document | 1 | `universal-only contract wrongly failing when the universal hook is present` | ✅ BITES |

**7/7 bite, control green. No mutant survives — R1's honest `M2 SURVIVES` has no analogue here**, because this
lane added no redundant backstop: every guard has a consumer.

### ⛔ THE HARNESS LIED ONCE, AND THE CORRECTION IS THE POINT

**My first mutation run reported M2 and M3 as `BITES` — with M1's failure arm.** Cause: every mutant was written
to the *same* path (`/var/tmp/r6fix/_mut.py`) under the *same* module name, so CPython served M1's cached `.pyc`
for M2 and M3. **The matrix was green for the wrong reason and would have been reported as proof.** Fixed with
`sys.dont_write_bytecode = True` plus a unique path and module name per mutant; the table above is the re-run.

This is the **blind-harness class** — [[mutation-tests-the-clause-not-the-feature]] again, at the harness layer
rather than the subject layer, and it was only visible because the matrix prints **which arm** caught each mutant.
★ **A mutation table that prints only rc cannot see this.** That is a cheap, general strengthening and it is
**REPORTED, NOT WIRED** (a repair does not extend other lanes' harnesses).

---

## WHAT WAS DRIVEN vs WHAT STAYS UNPROVEN

**DRIVEN** — the generator's own two build steps ([38] `--check`, [39] `--selftest`), write mode, the
before/after module pair loaded side by side, the live-tree blast radius, the 135-file census, the 159-file hash
diff, the `git status` diff, compile, timing.

**Fixtures**: built in `/var/tmp/r6fix/` from a **copy** of `knowledge/snippets/Icon-button.reference.html`.
**No tracked snippet was edited, and no fixture was homed in the repo** — `(NON-REPO: /var/tmp/r6fix/)`, `s191-D2`
marker carried in each harness header (`mut.py`, `mutants.py`, `/var/tmp/r6_blast.py`).

**UNPROVEN — each a priced TODO, none smoothed:**

1. **Nothing was rendered.** This lane changed a *contract reader*, not any artefact — the sync is a proven no-op
   (claims 10/11), so no pixel can have moved. But that is an inference from "no bytes changed", not a render.
   Price: **0** — there is nothing to look at.
2. **No `_build_all.py` run** (hard fence). Steps [38]/[39] were driven standalone, both rc=0. **The other 126
   steps are UNRUN by this lane.** In particular ds-018's **C2 gate (`_validate_property_resolves.py`) was RED
   on the tree at wave 1** (R1's finding, 12 failures) — this lane neither caused nor cleared that; **it was not
   re-run here**, because a sibling lane's repairs were landing in the same tree while I worked and any figure I
   took would have been unattributable. Price: ~2 min at the conductor's serial, when the tree is still.
3. **`declared_value` is still a REGEX over text, not a CSS parse.** It now reads the right *bytes*, but it still
   cannot tell a declaration inside `@media`/`@supports` from one at `:root`, and it takes the **first** match in
   document order regardless of cascade. That is the pre-existing contract and this lane did not widen it —
   named so nobody reads "comment-masked" as "parses CSS". [[no-gate-parses-the-artefact]] is **not** discharged
   here. Price: a `tinycss2` rewrite of the three readers, ~45–60 min + its own blast-radius run.
4. **`mask_comments` is duplicated, not shared** with `gen_token_ramp`'s. Deliberate: importing a sibling
   generator runs its help gate at import time. **The two can now drift** and no gate compares them. Price:
   ~20 min to home one copy in a shared helper and repoint both — but that touches `gen_token_ramp`, which is
   **R1's file, not mine**, so it is returned rather than done.
5. **The `FIGURE_RE` exposure is latent and unmeasured beyond its count** — see the finding below.

---

## ⚠ THE FINDING THE CONDUCTOR NEEDS — `FIGURE_RE`, LATENT NOT LIVE

**`Image-block.reference.html` carries a `<figure` inside its prose header comment** (offset 368, in the
"CANONICAL REFERENCE for Image block (Apollo MONO)" block). `FIGURE_RE` reads raw text, so a commented `<figure>`
would be walked for AUTO-MARKUP injection.

**It is NOT live today, and that was measured, not assumed:** the only group carrying `$markup` is `dataviz`, and
its members are the 14 `Chart-*` snippets. **`Image-block` is not a member** (`"Image-block" in $members → False`),
so `FIGURE_RE` never reads that file.

⛔ **NOT TOUCHED, AND DELIBERATELY SO — it is a DIFFERENT exposure class from this lane's.** Mine is *commented
content satisfying a contract*; `FIGURE_RE`'s is *injecting a live payload into dead markup* — R1's class, at an
injection site. Fixing it changes **what gets written**, and the brief's own instruction is to STOP before any
rewrite. **PRICED: ~20 min** — skip a `<figure>` whose start offset falls inside a comment (the mask's
length-preservation makes that a two-line filter, and it must **not** mask the figure's *contents*, or the
AUTO-MARKUP markers inside it vanish). **Needs a blast-radius run first**, and the decision that a commented-out
figure should never be injected into is the conductor's, not a repair's.

---

## PROBE DELTAS

**None asked, and that is deliberate rather than an omission.** P-7 and P-8 read *snippet artefacts*; this lane
changed a *generator's contract readers* and wrote **zero artefact bytes** (claims 10/11), so no probe count can
have moved by my hand. Running them would have measured **lane R5's** concurrent snippet edits and reported them
under my name. **The conductor should take P-7/P-8 at the serial, on a still tree** [[conclusions-are-debt-s129-d5]].

---

## ⛔ DO-NOT-RULE ITEMS THIS LANE BRUSHED — RETURNED PRICED, NOTHING SETTLED

| item | how this lane brushed it | returned as |
|---|---|---|
| **ANY threshold, constant or count in gates** (`s208-D1` rider) | none moved | **Nothing dialed.** No numeral in this file was changed. The selftest gained arms; **no existing arm was removed, relaxed, narrowed or renamed** (`_RUNBOOK-parallel-conductor.md:69`). The generator's own output strings are untouched. |
| **P-7 / P-8 promotion or park** (`W-85`) | not measured — see § PROBE DELTAS | **Untouched. Not proposed.** Still ADVISORY, still Dave's. |
| **the 34 proposed organisms + REVIEW-210 pages** (his eye queue) | `Icon-button` was **copied** to `/var/tmp` as a fixture | **Zero tracked bytes read for writing, zero written.** No design content judged or altered. The fixture is non-repo and is not a specimen. |
| **ds-005 class choice** | not reached by me — but lane **R5** is repairing its input leg in three files in this same tree | **Untouched by R6.** Named only for attribution of the dirty paths below. |
| **`gen_token_ramp.py`** (lane R1's file) | the duplicated `mask_comments` invites a shared helper | ⛔ **NOT TOUCHED — outside my fence.** Returned as UNPROVEN #4. |

---

## CONSEQUENCES / PITFALLS (mandatory, Dave #165)

**What could recur:**

1. **The class is fixed in this file's contract readers and NOWHERE ELSE.** ds-018's C2 gate
   (`_validate_property_resolves.py`) is **still HTML-comment-blind** — R1 priced that repair at ~30–40 min and it
   remains **unwired**. So a human editor can still hand-write this defect into a snippet and no gate will see it;
   only the two generators can no longer *create* it.
2. **A fence is as fragile as its test.** The mask must never reach `BEHAVIOUR_RE` / `AUTO_MARKUP_RE` /
   `markup_source_block`. The only thing standing between a future "let's mask everywhere for consistency" edit and
   132 lost injection sites is selftest arm **5f (vi)** and mutant **M6**. If someone deletes that arm as
   redundant, the fence goes silent. **It is named here so the arm reads as load-bearing.**
3. **The memo cache is keyed on the document string.** `M7` shows a stale-mask mutant is caught, but the cache
   grows unbounded within a run (~150 documents, bounded by the snippet population). Harmless at this size;
   it would not be in a per-file loop over a much larger corpus.
4. **A mutation harness that reuses a path reports the wrong mutant as caught.** It happened here and was only
   visible because the matrix prints the catching arm. Any lane copying my harness shape must keep
   `sys.dont_write_bytecode = True` and a unique module name per mutant.

**What this repair does NOT fix:**

- The C2 gate's HTML-comment blindness (R1's priced, unwired item).
- `FIGURE_RE`'s latent injection exposure (priced above).
- Anything about *cascade* correctness: `declared_value` still takes the first textual match and knows nothing of
  `@media`, specificity or scope. It reads the right bytes now; it still does not parse CSS.
- The 12 ABSENT P-8 findings in four templates — untouched, still outside every wave-1/3 fence I can see.

**Which class it belongs to:** [[no-gate-parses-the-artefact]] — the contract reader did not read in the
consumer's grammar — compounded with [[conflated-fix-guarantees-recurrence]], which is why all three faces in the
file were fixed together rather than only the one the brief named.

---

## `git status --short` — READ BACK VERBATIM AT LANE CLOSE

```
 M knowledge/gen_component_partials.py
 M knowledge/snippets/Combobox.reference.html
 M knowledge/snippets/Multi-select.reference.html
 M knowledge/snippets/Tags-input.reference.html
?? notes/_receipts/2026-08-21-211-wave3-laneR5-descender-clips.md
```

**Every path attributed:**

| path | whose |
|---|---|
| `knowledge/gen_component_partials.py` | **MINE** — the fix + selftest arm 5f (+112 / −5) |
| `knowledge/snippets/Combobox.reference.html` | **LANE R5's** — ds-005 input leg |
| `knowledge/snippets/Multi-select.reference.html` | **LANE R5's** — ds-005 input leg |
| `knowledge/snippets/Tags-input.reference.html` | **LANE R5's** — ds-005 input leg |
| `?? notes/_receipts/…-laneR5-descender-clips.md` | **LANE R5's** receipt |

★ **The three snippet paths are attributed by EVIDENCE, not by elimination.** They appeared between my baseline
(clean tree) and my blast-radius probe; the probe ran `run(write=False)` only. Each diff adds a
`.<x> .<y> input{text-box-edge:text text;}` rule whose own comment reads *"#211 lane R3 caught it live in this
file; lane R5 repairs it"*, and R5's receipt is on disk. **They are not mine.**

⚠ **The tree is shared and this listing is a MOMENT, not a state** [[conclusions-are-debt-s129-d5]] — re-read it
at the conductor's serial, do not carry mine forward.

**No gate I ran wrote a tracked file.** `--check`, `--selftest` and **write mode** were all run; only my own edit
appears. `knowledge/__pycache__/` was written by `py_compile` and is **gitignored** (`.gitignore:8`).

**Environment change, declared: NONE.** No `pip install`, no download, no browser. `tiktoken` was never needed —
no knowledge script refused.

**NO COMMITS. NO `git checkout`. NO `_build_all.py`.** HEAD `652d432` at open and at close.

---

## SUB SPEND

⛔ **NOT MEASURABLE FROM INSIDE THE LANE — declared UNKNOWN rather than estimated**
[[feedback-measuring-tool-must-not-guess]]. A sub cannot read its own `message.usage`; the conductor takes the
figure from the sub's usage record for the `subs N tokens (n=…)` line at wrap. Reported as a **shape**, labelled as
such: **2 file reads (both required by the brief), 1 target file read, ~12 bash calls, 3 edits, no renders, no
browser, no `_build_all` run.**
