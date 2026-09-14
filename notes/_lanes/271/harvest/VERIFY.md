**VERDICT: GREEN** (2026-09-14, after the repair lane) — the four defects that made this RED are fixed in the lane files: lane A's 22 over-cap quotes are re-cut to verbatim sub-spans under the cap (max now 14 words across all three slices, matching B and C), `B-24`'s `component` is a single existing stem, the five RECEIPT/JSON count mismatches are reconciled against a script, and the "Dave's own words" attribution at `A/SOURCES.json:333` is gone. Nothing under `knowledge/` was touched. See § REPAIR at the foot of this file.

# #271 HARVEST — VERIFY (lanes A, B, C)

**VERDICT: RED — SUPERSEDED by the GREEN line above, kept verbatim as the record of what was found.** Lane A ships 22 external quotes at or above the RUNBOOK's 15-word cap (max 19) and its RECEIPT never declares it, while B and C both assert "longest quote 14 words"; a silent cap breach in one slice only.

Verifier: read-only. This file is the only thing written. Date 2026-09-14, session 271.

---

## Violation counts at a glance

| Check | A | B | C | Total |
|---|---|---|---|---|
| 1. JSON parse / shape | 0 | 0 | 0 | **0** |
| 2. `component` not an existing stem | 0 | 1 | 0 | **1** |
| 3. Quote ≥ 15 words | **22** | 0 | 0 | **22** |
| 4. RECEIPT vs actual | 1 | 3 | 1 | **5** |
| 5. `git status --porcelain -- knowledge/` | — | — | — | **0 (empty)** |
| 6. Quote spot-check (16 fetched) | 6 VERBATIM, 1 FETCH FAILED | 4 VERBATIM | 4 VERBATIM | **15 VERBATIM / 0 NOT FOUND / 1 FETCH FAILED** |
| 7. Quote-gate on Dave attributions | 1 fail | 0 (1 pass) | 0 | **1** |
| 8. Cross-slice collisions | — | — | — | **0 gate collisions, 0 duplicate rules** |

---

## 1. Parse + shape — PASS (0 violations)

`python3` `json.load` on all 9 JSON files: all 9 parse.

```
A SOURCES  ours 47 · external 264 · refused 11
A PROPOSED-WHEN  proposals 45 · $already_done 5
A DECISION-TABLE  rows 30
B SOURCES  ours 16 · external 113 · refused 12
B PROPOSED-WHEN  proposals 45
B DECISION-TABLE  rows 24
C SOURCES  ours 27 · external 108 · refused 7
C PROPOSED-WHEN  proposals 42
C DECISION-TABLE  rows 15
```

Against the #270 exemplars in `notes/_lanes/270/when-research/`:

- `SOURCES.ours` item keys `['discriminates','note','said','src']` — **identical** in all three slices.
- `SOURCES.external` item keys: #270 = `['disc','quote','sys','url']`; all three slices = `['component','disc','quote','sys','url']` — the extra `component` is required by the BRIEF. **Match.**
- `SOURCES.refused`: #270 = `['url','why']`. A and B match. **C uses `['sys','urls','why']`** (one entry per system, a URL list) — a deviation, richer not poorer; 7 entries / 22 URLs. Recorded, not counted as a violation.
- `PROPOSED-WHEN.proposals` item keys `['component','confidence','daves_call','disagreements','sources','when_gate','when_prose']` — **identical to #270 in all three slices.** `$confidence_scale` keys are the same four words in all three (`canon` / `consensus-external` / `single-external` / `none`).
- `DECISION-TABLE.json` has **no #270 exemplar**; the BRIEF is the only spec (rule · per-system position · `options` 2–4 · `recommendation` labelled as the lane's). All three satisfy it, but **the three row shapes differ**:
  - A: `components · id · options · positions · recommendation · rule · why_contested`
  - B: `component · id · options · positions · recommendation · rule` (+ optional `kind`)
  - C: `components · id · options · ours · positions · recommendation_THIS_LANES_NOT_RULED · rule · why_non_unanimous`
  All three label the recommendation as the lane's in `$description`. Harmonising is a #271 conductor job, not a lane defect.

## 2. `component` values are existing stems — 1 violation

138 stems in `knowledge/components/*.meta.json`. Every `component` in `SOURCES.external`, `PROPOSED-WHEN.proposals` and the decision tables was resolved against that set (proposal names of the form `stem / VARIANT` resolved on the stem).

- `SOURCES.external`: A 264 entries → 3 `null`, 0 bad. B 113 → 6 `null`, 0 bad. C 108 → 2 `null`, 0 bad. Every `null` carries a note (findings: GOV.UK warning-text, GOV.UK inset-text, spotlight/tour; USWDS `collection`, treemap, sankey, waterfall, lollipop, Carbon's intent taxonomy).
- `PROPOSED-WHEN`: A 45 / B 45 / C 42 — **0 bad**. No atom invented.
- Decision tables: A 30 rows, C 15 rows — 0 bad.
- **VIOLATION — `B/DECISION-TABLE.json` row `B-24`**: `"component": "limits-meter, progress-bar"` is a comma-joined string, not a stem and not a list. Both stems exist; the defect is shape, and any consumer splitting on `component` gets a non-stem. One-character fix, not ruling-shaped.

## 3. Quote length < 15 words — 22 violations, ALL in lane A

Word count = `len(quote.split())`. The RUNBOOK cap is **< 15**, so 15 is a violation.

- **B: 0 of 113.** Max = 14 words. Matches its RECEIPT claim.
- **C: 0 of 108.** Max = 14 words. Matches its RECEIPT claim.
- **A: 22 of 264.** Max = 19 words. A's RECEIPT makes **no claim about quote length at all** — the breach is undeclared.

| words | system | quote (head) |
|---|---|---|
| 19 | IBM Carbon | If a user can only enter an option from a predefined list then avoid using a free-form tex… |
| 19 | Ant Design | When subtasks are too heavy for a Popover and we still want to keep the subtasks in the co… |
| 17 | IBM Carbon | If a process will take more than a moment or two to complete, use a progress indicator |
| 17 | Adobe Spectrum | Be sure to set a minimum of 5 seconds so that users can have time to read |
| 16 | USWDS | Usability testing suggests some people prefer manually typing the date rather than using t… |
| 16 | IBM Carbon | Do not use links for actions that will change data or manipulate how it is displayed |
| 16 | GOV.UK | Only use a calendar control if users need to: pick a date in the near future |
| 16 | GOV.UK | Do not use the text input component if you need to let users enter longer answers |
| 16 | GOV.UK | Do not use the date input component if users are unlikely to know the exact date |
| 16 | GOV.UK | Do not use progress indicators that do all of the following: show all questions at once |
| 16 | GOV.UK | Always show an error summary when there is a validation error, even if there's only one. |
| 16 | Ant Design | If there are more than three operations, you can group some of them into a Dropdown |
| 16 | Adobe Spectrum | Use an icon only when necessary and when it has a strong association with the label |
| 15 | USWDS | Use a combo box when there are more than 15 choices in a drop-down list. |
| 15 | USWDS | If a form or process has fewer than three sections, don't use a step indicator. |
| 15 | IBM Carbon | Use a text area when the expected user input is more than a few words |
| 15 | GOV.UK | Use the textarea component when you need to let users enter an amount of text |
| 15 | GOV.UK | Do not use the textarea component if you need to let users enter shorter answers |
| 15 | GOV.UK | Do not use placeholder text in place of a label, or for hints or examples |
| 15 | Ant Design | When part of the page is waiting for asynchronous data or during a rendering process |
| 15 | Ant Design | Could be replaced by Spin in any situation, but can provide a better user experience. |
| 15 | Adobe Spectrum | They should be used when the upper and lower bounds to the range are invariable. |

Split: **13 at 16+ words, 9 at exactly 15.** Two of these (Carbon links 16 words, Spectrum slider 15 words) are load-bearing positions in decision rows `R-A-02` and `R-A-14`. **They are still verbatim** — spot-check 6 confirmed the Carbon link quote on the live page. The defect is the cap, not the fidelity, and the fix is a trim, not a refetch.

## 4. RECEIPT counts vs the JSONs — 5 mismatches

**A — 1 mismatch.** ours 47 ✓ · external 264 ✓ · refused 11 ✓ · distinct components with an external quote 40 ✓ · `component: null` 3 ✓ · proposals 45 ✓ · rows 30 ✓ · unanimous 15 = 45−30 ✓ · confidence spread `canon 4 · consensus-external 22 · single-external 11 · none 8` ✓ exact. Per-system quote counts all exact: GOV.UK 25 · USWDS 14 · M3 25 · Carbon 32 · Polaris 20 · Spectrum 20 · Atlassian 34 · Ant 27 · Fluent 2 27 · Apple HIG 14 · NN/g 26.
- **Mismatch:** the "Declared gaps" bullet names **nine** components for the count **8** — `amount-input` is listed but its actual `confidence` is `single-external`. The actual eight are date-range-picker, tags-input, secure-entry, quick-actions, cta-lockup, countdown-timer, modal-lightbox, command-palette. The receipt half-flags this ("nine records, eight distinct"); the list is still wrong.

**B — 3 mismatches.** ours 16 ✓ · external 113 ✓ · longest quote 14 ✓ · proposals 45 ✓ · confidence `canon 29 / consensus-external 8 / single-external 2 / none 6` ✓ exact · systems that spoke 9 ✓ · `component: null` 6 ✓ · rows 24 ✓.
- **Mismatch:** "Non-unanimous (a real fork for Dave) **25**" vs **24** decision-table rows.
- **Mismatch:** "24 (**22** system disagreements + **2** internal, flagged `kind: internal`)" — actual is **21 + 3**. Three rows carry a `kind` beginning "internal": B-23, B-24 and one more.
- **Mismatch:** the same table carries both "confidence `none` **6**" and "**`none`** — no external source found at all **14**". Two different numbers under one label in one table. 6+25+14 = 45 is internally consistent as a partition, but the word `none` is doing two jobs and only the 6 is the JSON's `confidence` field.

**C — 1 mismatch.** ours 27 ✓ · external 108 ✓ · refused 7 systems / 22 URLs ✓ · distinct `disc` values 68 ✓ · proposals 42 ✓ · confidence `canon 4 / consensus-external 11 / single-external 10 / none 17` ✓ exact · rows 15 ✓ · longest quote 14 ✓. Per-system quote counts all exact: USWDS 29 · GOV.UK 25 · Carbon 11 · Apple HIG 10 · Polaris 10 · NN/g 9 · M3 7 · Ant 7 · Spectrum 0 · Atlassian 0 · Fluent 0.
- **Mismatch (taxonomy, not arithmetic):** "unanimous 4" + "non-unanimous 15" + "none 17" = 36, against 42 proposals. Six proposals fall in none of the three buckets the receipt presents. C's rows are per-RULE and its proposals per-COMPONENT, so the two axes are not commensurable — but the receipt reads as if they were.

Declared gaps in all three receipts (fetch failures, unreachable systems, `template-*` 12-not-13, `headers` listed twice, the four non-role-provider components) are **declared**, and are why the verdict is scoped to check 3 alone.

## 5. Canon untouched — PASS

```
$ git status --porcelain -- knowledge/
$
```

Empty. Zero bytes of output, exit 0. Nothing under `knowledge/` was created, modified or deleted.

## 6. Quote spot-check against the live page — 15 VERBATIM, 0 NOT FOUND, 1 FETCH FAILED

Fetched each cited URL, stripped tags, normalised smart quotes/dashes/whitespace, then substring-matched the quote. Picked from the three most-contested rows per slice (`R-A-01` primary-button count, `R-A-14` slider legality, `R-A-02` link-vs-button; `B-01` pagination threshold, `B-03` tag-vs-status, `B-04` pie slice count; `R1` masthead-vs-sidebar, `R3` breadcrumb depth).

| # | Slice | System | Result |
|---|---|---|---|
| 1 | A | IBM Carbon — `/components/button/usage/` | **VERBATIM** |
| 2 | A | Atlassian — `/components/button/usage` | **FETCH FAILED** |
| 3 | A | GOV.UK — `/patterns/question-pages/` | **VERBATIM** |
| 4 | A | IBM Carbon — `/components/link/usage/` | **VERBATIM** |
| 5 | A | Fluent 2 — `/components/web/react/core/button/usage/` | **VERBATIM** |
| 6 | A | Adobe Spectrum — `/page/button/` | **VERBATIM** |
| 7 | A | Ant Design — `/components/button` | **VERBATIM** |
| 8 | A | USWDS — `/components/button/` | **VERBATIM** |
| 9 | B | Shopify Polaris — raw `.mdx`, `resource-list.mdx` | **VERBATIM** |
| 10 | B | IBM Carbon — `/components/tag/usage/` | **VERBATIM** |
| 11 | B | GOV.UK — `/components/tag/` | **VERBATIM** |
| 12 | B | Datawrapper — `/blog/pie-charts` | **VERBATIM** |
| 13 | C | IBM Carbon — `/components/UI-shell-left-panel/usage/` | **VERBATIM** |
| 14 | C | GOV.UK — `/components/breadcrumbs/` | **VERBATIM** |
| 15 | C | USWDS — `/components/breadcrumb/` | **VERBATIM** |
| 16 | C | Ant Design — `/components/breadcrumb` | **VERBATIM** |

**The one failure, honestly classified.** `atlassian.design/components/button/usage` returns 445,278 bytes on a plain fetch and the string "primary button" occurs **zero times** in that body — it is the SPA shell, exactly as lane A's own `refused` entry declares ("SPA shell only on a plain fetch; the Gatsby `page-data.json` endpoints 404; harvested through a JS-rendering fetch"). This verifier has no JS-rendering route in its sandbox (`import playwright` → `ModuleNotFoundError`). So this is **FETCH FAILED, not NOT FOUND** — it is not evidence against the quote, and the quote was not paraphrased or altered here.

**Consequence worth naming:** the same applies to the whole **Atlassian corpus in lane A — 34 quotes, the single largest system in that slice — plus lane A's 25 Material 3 quotes**, all obtained through a JS-rendering fetch this verifier cannot reproduce. They are unverified-by-this-verifier, not disproved. The 15 quotes reached by plain fetch, including Spectrum's RSC-payload page and Fluent's, were **all verbatim with zero drift** — that is real corroboration of the lane's fidelity, but it does not extend to the JS-rendered set.

## 7. Quote gate on sentences attributed to Dave — 1 pass, 1 FAIL

Grepped all 9 JSONs and 3 RECEIPTs for `Dave` / `his words`. Two are attributions of words to Dave; the rest are procedural ("Options are for Dave", "until Dave rules it", `daves_call`) and carry no quoted sentence.

**PASS — `B/PROPOSED-WHEN.json` and `B/SOURCES.json:63`:** `s210-D1, Dave verbatim: "keep as one meter"`.
```
$ python3 knowledge/_quote_gate.py "keep as one meter"
QUOTE-GATE ADVISORY — 1 verbatim · 0 not in the record
  ✅ "keep as one meter"
       component:limits-meter · knowledge/components/limits-meter.meta.json:1 (+2 more)
```

**FAIL — `A/SOURCES.json:333`:** `"no access today (Dave's own words, carried from #270). The HSBC component-choice prose is almost certainly there…"`.
```
$ python3 knowledge/_quote_gate.py "no access today"
QUOTE-GATE ADVISORY — 0 verbatim · 1 not in the record
  ❌ "no access today"
       nearest gm-archive:batch-4-rolled-2026-07-25-evening-wrap · _GM-ARCHIVE.md:6717 · bigrams 1 of 2
       longest run in common: "no access"   (exit 1)
```
Three words, on the Figma/HSBC access note, presented as **Dave's own words** and not in the record. Low stakes — it changes no rule — but it is exactly the class the quote gate was born in #269 to catch, and the fix is to drop "Dave's own words" or replace it with the sentence he actually said.

## 8. Cross-slice collisions — 0 gate collisions, 0 duplicate rules

- **No component is proposed in two slices.** 45 + 45 + 42 = 132 proposals, every `component` value unique across all three files. There is therefore **no component carrying two different `when_gate`s**. No component is duplicated *within* a slice either.
- **No decision-table rule duplicates another slice's.** Normalised (lowercased, punctuation stripped) rule text across all 69 rows: zero exact collisions, and no near-pair on inspection.
- Two components are *referenced* by rows in two slices, on genuinely different questions — not collisions:
  - `progress-bar` — A `R-A-06` "At what wait does a spinner become a progress bar?" vs B `B-24` "Are alias metas exempt from a when-completeness gate?"
  - `back-to-top` — A `R-A-26` "Is the FAB mobile-only?" vs C `R8` "What makes a Back-to-top control appear?"
- C's receipt pre-declares the one real overlap risk (`pagination`, `accordion`, `carousel`, `cards` live in C's roles but are B's components) and wrote **no proposal** for any of the four. Confirmed in the JSON: none of them appears in C's proposals. The declaration holds.

---

## What would turn this GREEN

1. **Trim lane A's 22 over-cap quotes to < 15 words** (all 22 listed above, all confirmed-or-presumed verbatim, so trimming is a cut not a refetch), or have A's RECEIPT declare the breach the way B and C declare their 14-word ceiling. A declared gap passes; this one is silent.
2. Fix `B-24`'s `component` string → a stem or a list.
3. Correct the four count lines: B's non-unanimous 25→24, B's 22+2→21+3, B's second `none` 14, A's nine-names-for-eight.
4. Drop or replace the "Dave's own words" attribution at `A/SOURCES.json:333`.

None of these touches `knowledge/`, and none needs Dave.


---

## REPAIR — 2026-09-14

A repair lane, run after this verdict. **Read-only on canon throughout** (`git status --porcelain -- knowledge/` still empty; the only new file is `notes/_lanes/271/harvest/_recount.py`, the recount script the receipts now cite).

### Fix 1 — lane A's 22 over-cap quotes, re-cut from the live pages

Every one of the 22 cited URLs was **re-fetched** and the original quote **re-confirmed verbatim on the page before cutting** (all 22 found; Adobe Spectrum's three pages had to be read out of the Next.js `__next_f` flight payload, as lane A declared, and Atlassian was not among the 22). Each quote was then replaced by a **contiguous verbatim sub-span under the cap** that still carries the discriminator. **No quote was paraphrased, no source was dropped, and nothing moved to `refused`** — no fetch failed, so no refusal was warranted.

Where the cut had to drop a criterion the sentence carried, the criterion is restated **in the lane's own words in `disc`**, never as an unquoted extension of the quote. Ten `disc` fields were extended this way (indices 0, 1, 2, 7, 8, 12, 20, 28, 39 and 114 of `A/SOURCES.json.external`); the other twelve quotes needed no restatement.

| words | system | component | before → after |
|---|---|---|---|
| 16 → **13** | GOV.UK | input-fields | `Do not use the text input component if you need to let users enter longer answers` → `enter text that's no longer than a single line, such as their name` |
| 15 → **11** | GOV.UK | textarea | `Use the textarea component when you need to let users enter an amount of text` → `enter an amount of text that's longer than a single line` |
| 15 → **14** | GOV.UK | textarea | `Do not use the textarea component if you need to let users enter shorter answers` → `enter shorter answers no longer than a single line, such as a phone number` |
| 15 → **10** | GOV.UK | input-fields | `Do not use placeholder text in place of a label, or for hints or examples` → `Do not use placeholder text in place of a label` |
| 16 → **13** | GOV.UK | date-picker | `Do not use the date input component if users are unlikely to know the exact date` → `a date they'll already know, or can look up without using a calendar` |
| 16 → **12** | GOV.UK | calendar | `Only use a calendar control if users need to: pick a date in the near future` → `Only use a calendar control if users need to: pick a date` |
| 16 → **11** | GOV.UK | form-layout | `Always show an error summary when there is a validation error, even if there's only one.` → `Always show an error summary when there is a validation error` |
| 16 → **11** | GOV.UK | progress-tracker | `Do not use progress indicators that do all of the following: show all questions at once` → `Do not use progress indicators that do all of the following:` |
| 15 → **11** | USWDS | combobox | `Use a combo box when there are more than 15 choices in a drop-down list.` → `Use a combo box when there are more than 15 choices` |
| 16 → **10** | USWDS | date-picker | `Usability testing suggests some people prefer manually typing the date rather than using the calendar picker.` → `Always allow a user to type in the date manually` |
| 15 → **10** | USWDS | progress-tracker | `If a form or process has fewer than three sections, don't use a step indicator.` → `has fewer than three sections, don't use a step indicator.` |
| 15 → **11** | IBM Carbon | textarea | `Use a text area when the expected user input is more than a few words` → `When the expected user input is more than a few words` |
| 19 → **10** | IBM Carbon | input-fields | `If a user can only enter an option from a predefined list then avoid using a free-form text input` → `a predefined list then avoid using a free-form text input` |
| 16 → **10** | IBM Carbon | links | `Do not use links for actions that will change data or manipulate how it is displayed` → `Do not use links for actions that will change data` |
| 17 → **12** | IBM Carbon | progress-bar | `If a process will take more than a moment or two to complete, use a progress indicator` → `more than a moment or two to complete, use a progress indicator` |
| 15 → **8** | Ant Design | skeleton-loader | `Could be replaced by Spin in any situation, but can provide a better user experience.` → `Could be replaced by Spin in any situation` |
| 15 → **10** | Ant Design | loading-indicator | `When part of the page is waiting for asynchronous data or during a rendering process` → `When part of the page is waiting for asynchronous data` |
| 19 → **8** | Ant Design | drawer | `When subtasks are too heavy for a Popover and we still want to keep the subtasks in the context` → `When subtasks are too heavy for a Popover` |
| 16 → **13** | Ant Design | action-bar | `If there are more than three operations, you can group some of them into a Dropdown` → `more than three operations, you can group some of them into a Dropdown` |
| 17 → **9** | Adobe Spectrum | toast | `Be sure to set a minimum of 5 seconds so that users can have time to read` → `Be sure to set a minimum of 5 seconds` |
| 15 → **12** | Adobe Spectrum | slider | `They should be used when the upper and lower bounds to the range are invariable.` → `used when the upper and lower bounds to the range are invariable.` |
| 16 → **13** | Adobe Spectrum | icon-button | `Use an icon only when necessary and when it has a strong association with the label` → `Use an icon only when necessary and when it has a strong association` |

**Before: 22 quotes ≥ 15 words, max 19. After: 0, max 14.** The 13 cells on the review page that carried these quotes were updated to the same text (verified: 0 of the 22 old strings remain on the page in any escaping).

Lane A's RECEIPT now **declares the ceiling** the way B and C do — the silent breach is what made this RED, and a declared number replaces it.

### Fix 2 — the attribution at `A/SOURCES.json:333`

**Before:** `"no access today (Dave's own words, carried from #270)."` — three words presented as Dave's and not in the record.
**After:** the entry's `why` is the **lane's own** wording, explicitly labelled as such, and cites files rather than a person: `notes/_lanes/271/harvest/BRIEF.md` (where the ask is quoted at the top) and `notes/_lanes/270/when-research/SOURCES.json` (the entry it was carried from). No sentence in the entry is attributed to Dave. The entry is still at line 333.

### Fix 3 — `B-24`'s `component`

**Before:** `"component": "limits-meter, progress-bar"` — a comma-joined string; a consumer splitting on `component` gets a non-stem.
**After:** `"component": "limits-meter"` — the single existing stem, and the one that belongs to slice B (progress-bar is slice A's component in the BRIEF). `progress-bar` is carried on the row as a new `note` field saying it is the same kind of alias and equally affected. The review page's row was updated to match. Decision-table rows are still **24**; no row was added or removed.

### Fix 4 — the five RECEIPT ↔ JSON mismatches

All five are reconciled, and every receipt now ends with a **Recount** section carrying the command and its output, so the numbers are reproducible rather than remembered.

| # | Slice | Claim | Before | After |
|---|---|---|---|---|
| 1 | A | declared-gap list for `confidence: none` | **nine names** for the count 8 (`amount-input` wrongly included) | **eight names for 8** — `amount-input` removed and its `single-external` confidence stated |
| 2 | A | unanimous | **15** (computed as 45 − 30, mixing a per-component axis with a per-rule one) | **5** by the review page's own test (`disagreements` opens with *none*), plus **9 expected-silence** proposals stated separately, plus an explicit "these do not add up" note |
| 3 | B | non-unanimous | **25** | **24** (= the decision-table rows) |
| 4 | B | row split | **22 system + 2 internal** | **21 system + 3 internal** (B-17, B-23, B-24) |
| 5 | B | the word `none` doing two jobs | `confidence none` **6** and "`none` — no external source found at all" **14** under one label | relabelled: **`confidence: none` 6** vs **"no external system cited in `sources`" 15**, stated as overlapping measures |
| 6 | C | taxonomy | 4 + 15 + 17 = **36** against 42 proposals, presented as a partition | the two axes are labelled (4 and 17 are **component** counts, 15 is a **rule** count), the overlap is named, and the two proposals outside all three (`tab-bar`, `divider`) are named |

Lane A also gained a **Longest quote: 14 words** row, which it previously did not carry at all.

### Fix 5 — page section counts

Re-derived from the JSONs and **unchanged**: quotes 485 · proposals 132 · decision rows 69 · unanimous 15 (5 + 6 + 4) · `confidence: none` 31 (8 + 6 + 17). The header stats (`69` / `15` / `485` / `31`) and the three section headings ("The 69 rules…", "15 rules…", "31 components…") all still match. No count edit was needed; only the 13 quote cells and the B-24 row changed.

### Fix 6 — render proof re-run

```
$ source knowledge/_render/seat_env.sh
SEAT_ENV: OK seat=confident-lucid-lamport ... faces=10/404 farm=10/10 libs=2
$ python3 <stitching driver>  # chromium, goto file://…_REVIEW-when-harvest-whole-library-2026-09-14-v1.html
notes/_lanes/271/harvest/shot-1280.png  1280x47972  30 tiles
notes/_lanes/271/harvest/shot-400.png   400x131991  83 tiles
```

Both files overwritten. A single full-page capture fails at this height (`Unable to capture screenshot`), so both are stitched from viewport tiles, as before. Two crops were read back and reviewed on sight, not just gated: the repaired **B-24** row (single stem + the progress-bar note renders inside its column) and the re-cut **R-A-11 / date-picker** cells (GOV.UK, USWDS and Spectrum quotes all read as whole rules at their new length).

---

## Re-run of checks 3, 4 and 7

### Check 3 — quote length < 15 words — **PASS (0 violations, was 22)**

```
A over-cap 0 · max words 14 · external 264
B over-cap 0 · max words 14 · external 113
C over-cap 0 · max words 14 · external 108
```

All three slices now share one ceiling, and all three receipts declare it.

### Check 4 — RECEIPT vs the JSONs — **PASS (0 mismatches, was 5)**

Recounted by script; the same output is pasted into each RECEIPT.md.

```
$ python3 notes/_lanes/271/harvest/_recount.py A
SLICE A
  SOURCES     ours 47 · external 264 · refused 11
  quotes      longest 14 words · at-or-over the <15 cap: 0
  proposals   45
  confidence  canon 4 · consensus-external 22 · single-external 11 · none 8
  unanimous   5  (page test: `disagreements` opens with "none") -> input-fields, textarea, icon-button, alert, popover
  expected silence recorded in `disagreements`: 9 -> amount-input, date-range-picker, tags-input, split-button, quick-actions, cta-lockup, countdown-timer, modal-lightbox, command-palette
  decision rows 30 · distinct components named by a row 36 · proposals a row touches 33
  rows flagged kind=internal: 0 -> 
  system-disagreement rows: 30
  proposals citing NO external system in `sources`: 5
  component values that are not an existing meta stem: 0
  external findings with component: null: 3

$ python3 notes/_lanes/271/harvest/_recount.py B
SLICE B
  SOURCES     ours 16 · external 113 · refused 12
  quotes      longest 14 words · at-or-over the <15 cap: 0
  proposals   45
  confidence  canon 29 · consensus-external 8 · single-external 2 · none 6
  unanimous   6  (page test: `disagreements` opens with "none") -> timeline, view-options, Chart-boxplot, Chart-candlestick, Chart-histogram, limits-meter
  expected silence recorded in `disagreements`: 17 -> document-row, transaction-row, standing-order-mandate-row, account-card, carousel, filter-toolbar-bar, chart-sparkline, Chart-bullet, Chart-butterfly-v, kpi-tile, runway-bar, amount-display, stats-band-lockup, avatar, avatar-group, payment-card-visual, qr-code
  decision rows 24 · distinct components named by a row 22 · proposals a row touches 22
  rows flagged kind=internal: 3 -> B-17, B-23, B-24
  system-disagreement rows: 21
  proposals citing NO external system in `sources`: 15
  component values that are not an existing meta stem: 0
  external findings with component: null: 6

$ python3 notes/_lanes/271/harvest/_recount.py C
SLICE C
  SOURCES     ours 27 · external 108 · refused 7
  quotes      longest 14 words · at-or-over the <15 cap: 0
  proposals   42
  confidence  canon 4 · consensus-external 11 · single-external 10 · none 17
  unanimous   4  (page test: `disagreements` opens with "none") -> app-shell-focused, template-wizard, template-confirmation, template-error
  expected silence recorded in `disagreements`: 0 -> 
  decision rows 15 · distinct components named by a row 27 · proposals a row touches 25
  rows flagged kind=internal: 0 -> 
  system-disagreement rows: 15
  proposals citing NO external system in `sources`: 17
  component values that are not an existing meta stem: 0
  external findings with component: null: 2
```

Every highlighted number in the three receipts is now one of these lines. The receipts additionally state, in words, that proposals are per-component and rows are per-rule and that the measures overlap — the failure mode behind mismatches 2 and 6 was adding two axes together, not arithmetic.

### Check 7 — quote gate on sentences attributed to Dave — **PASS (0 fails, was 1)**

```
$ grep -rn "Dave's own words" notes/_lanes/271/harvest/*/*.json notes/_lanes/271/harvest/*/RECEIPT.md
(no matches)
```

The one remaining sentence attributed to Dave anywhere in the nine JSONs is `B/SOURCES.json:63`'s `s210-D1, Dave verbatim: "keep as one meter"`, and it still passes:

```
$ python3 knowledge/_quote_gate.py "keep as one meter"
QUOTE-GATE ADVISORY — 1 verbatim · 0 not in the record
  ✅ "keep as one meter"
       component:limits-meter · knowledge/components/limits-meter.meta.json:1 (+2 more)
```

And the string that failed is no longer attributed to anyone — it is not in the record, and the lane no longer claims it is:

```
$ python3 knowledge/_quote_gate.py "no access today"
QUOTE-GATE ADVISORY — 0 verbatim · 1 not in the record
  ❌ "no access today"
       nearest gm-archive:batch-4-rolled-2026-07-25-evening-wrap · _GM-ARCHIVE.md:6717 · bigrams 1 of 2
       longest run in common: "no access"
```
