# Receipt — #213 TEMPLATE-REPAIR lane · the Template-* snippet family, two measured defects

> ⛔ **DATED PERIOD RECORD, NOT A LIVE HOME.** Nothing here is a ruling. Open choices are marked
> **PROPOSED-not-ruled** and are Dave's. The store (`knowledge/_state.json`, `knowledge/_rulings.json`)
> stays the one live home; this lane wrote to neither, ran no git command, and touched no shared state.
> ⚠ Some evidence lives outside the repo — marked `(NON-REPO: …)` per `s191-D2`.

| governance | value |
|---|---|
| lane | TEMPLATE-REPAIR (Opus work sub), session #213 |
| brief | `notes/_briefs/2026-08-21-213-mine-burn-fanout-brief-v1.md` (FENCES + PITFALLS binding) |
| files edited | 4 snippet sources only — see § THE REPAIR |
| canon.css | **NOT regenerated in the working tree** (three other lanes touched it today). All canon proofs ran in a scratch tree. |

---

## 1 · PREMISE TABLE — every claim in the brief re-probed before building

| # | premise as briefed | probe run | result | verdict |
|---|---|---|---|---|
| P1 | `_validate_property_resolves.py --strict` exits 1 with 12 failures across four Template-* snippets | `python3 knowledge/_validate_property_resolves.py --strict; echo $?` | `property-resolves gate (C2): 147 file(s), 12 failure(s)` · exit **1** | ✅ CONFIRMED, exactly 12 |
| P2 | `_validate_token_forks.py` exits 2, "unbalanced `}`" | `python3 knowledge/_validate_token_forks.py; echo $?` | `FAIL … canon.css: unbalanced '}' at line 15409` · exit **2** | ✅ CONFIRMED as a class; ⚠ **line was 15409, not the briefed 15374** |
| P3 | orphan blocks at `Template-confirmation.reference.html:193` and `Template-error.reference.html:182` | `grep -n "^    display:inline-flex"` | confirmation **193** ✓ · error **182** ✓ | ✅ CONFIRMED, both exact |
| P4 | carried into canon.css at `:15374` and `:16919` | `sed -n '15395,15415p' knowledge/canon/canon.css` | ONE mangled rule at **15409**; no second site — the error-template orphan never produced a *second* unbalanced brace because the gate aborts at the first | ⚠ **PARTLY FALSE.** One crash site, not two. The gate exits at the first imbalance and never reaches the second. |
| P5 | "E3's receipt says restore-selector vs delete is a design call" | read the file headers at the defect sites | the #210 wave **wrote its intent down in prose beside the defect** — the call is decidable from the artefact, not open | ✅ RESOLVED BY EVIDENCE, see § 3 |
| P6 | the two defects may share a root cause | see § 3 | **they do** | ✅ same class, evidenced |

⚠ **Line numbers drift.** P2/P4's briefed numbers were already stale by the time this lane opened
(the brief said so — "re-probe, don't trust"). Every number in this receipt is today's measurement.

---

## 2 · THE DEFECTS, QUOTED

### Defect 2 — the orphan tail (the `unbalanced '}'`)

`knowledge/snippets/Template-confirmation.reference.html:192-193` (pre-repair), and the byte-identical
pair at `Template-error.reference.html:181-182`:

```css
  .confirm__actions{ display:flex; flex-direction:column; gap:12px; width:100%; margin-top:12px; }
    display:inline-flex; align-items:center; justify-content:center; transition:background var(--ease), filter var(--press); }
```

The second line is the **tail of a rule whose selector was deleted**. Its identity is not a guess —
the file header six lines above names the deletion, verbatim:

> *"minus its two raw font declarations and minus its own `.confirm .btn` ladder (this page uses the
> Button ATOM; carrying a second ladder would fork it)"*

The ladder's selector and leading declarations were removed; its **last continuation line and closing
brace were left behind**.

**What the generator then did with it** — `knowledge/canon/gen_canon_components.py`'s `walk()` sees a
non-`@`, non-comment token, so it searches forward for the next `{` and reads everything up to it as a
**selector list**. `prefix_selector()` comma-splits that and scopes each part. Emitted at
`knowledge/canon/canon.css:15409`:

```css
.cn-template-confirmation display:inline-flex; align-items:center; justify-content:center; transition:background var(--ease), .cn-template-confirmation filter var(--press); }
```

⚠ **BLAST RADIUS BEYOND THE BRACE — a finding the brief did not carry.** Because the swallowed span ran
all the way to the *next* `{`, it consumed the `@keyframes pop` header too, so that rule was emitted
**un-namespaced** into global canon.css at `:15414` — the generator's per-component keyframe namespacing
was silently bypassed for it. Every other component's `pop` is namespaced (`cn-confirmation-pop`,
`cn-template-wizard-pop`), so this one bare `@keyframes pop` sat in the global namespace. No collision
today (`grep -c "@keyframes pop{"` → **1**), but the guard was off. After repair it emits correctly as
`@keyframes cn-template-confirmation-pop` with its consumer rewritten to match
(`canon.css:15413` / `:15415` in the scratch regen).

### Defect 1 — the 12 unresolved properties (ds-018 silent-lookup class)

Verbatim from the gate:

```
❌ FAIL knowledge/snippets/Template-confirmation.reference.html: `--error` referenced 1× with no fallback and declared nowhere this file can reach …
❌ FAIL knowledge/snippets/Template-confirmation.reference.html: `--error-tint` …
❌ FAIL knowledge/snippets/Template-confirmation.reference.html: `--fborder` …
❌ FAIL knowledge/snippets/Template-confirmation.reference.html: `--header` …
❌ FAIL knowledge/snippets/Template-empty.reference.html: `--header` …
❌ FAIL knowledge/snippets/Template-error.reference.html: `--fborder` · `--header` · `--success` …
❌ FAIL knowledge/snippets/Template-settings.reference.html: `--header` · `--success-tint` · `--warning` · `--warning-tint` …
```

The 12 sort into exactly three shapes:

| shape | vars | referenced by | the file's theme block |
|---|---|---|---|
| **(a) demo chrome** | `--header` ×4, `--fborder` ×2 | `.demo-bar` / `.demo-bar button` — the block labelled *"DEMO CHROME below this line. NOT the template."* | never declared them; the sibling templates that DO have tables (`Template-dashboard`, `-report`, `-list-index`) declare both |
| **(b) a chip state the page does not have** | `--error`, `--error-tint` (confirmation); `--success-tint`, `--warning`, `--warning-tint` (settings) | `.status.err` / `.status.ok` + `.status.warn` | deliberately declares the *other* RAG tokens and not these |
| **(c) a roundel the page does not have** | `--success` (error) | `.confirm .success{ fill:var(--success) }` | header says, verbatim: *"⛔ AND NOTE WHAT IS ABSENT: there is NO rag/\* token in this file at all."* |

Markup probe (`grep -n 'class="status …' / 'class="[^"]*\bsuccess\b'`) — the decisive evidence for (b)/(c):

- `Template-confirmation` markup carries `class="status warn"` (`:379`) and `class="success"` (`:326`). **No `status err`.**
- `Template-settings` markup carries `class="status inf"` (`:745`). **No `status ok`, no `status warn`.**
- `Template-error` markup carries **no `.success` at all** — and composition rule 6 in that same file says why, in the author's own words: *"the decorative anchor glyph — Empty-state's treatment (48px, 0.4 ink, aria-hidden), NOT Confirmation's 56px RAG roundel. The reason is in the file header and it is deliberate."*

---

## 3 · ROOT-CAUSE VERDICT — **YES, one class, two manifestations**

**The #210 wave performed its subtractions in the PROSE and not in the FILE.**

Every Template-* snippet is a hand-carry: blocks lifted from source components, with a header comment
stating what was carried and what was left out. The defect class is that the *leaving-out* was written
down and not executed:

- **Defect 2** is the residue of a subtraction the header **announces** (`minus its own .confirm .btn
  ladder`) — the selector went, the tail stayed.
- **Defect 1(c)** is a subtraction the header **announces twice** (`NO rag/* token in this file at all`
  + composition rule 6) and never performs — the rule stayed, its token went.
- **Defect 1(b)** is a whole chip block carried for markup states the page does not have, past a theme
  block that was hand-trimmed to the states it *does* have.
- **Defect 1(a)** is a chrome block carried past a theme block trimmed of the two tokens it consumes.

The proximity is the proof, not an inference: in `Template-error` the deleted-selector tail (`:182`) and
the orphaned-token rule (`:178`) are **four lines apart, inside the same carried block, under the same
header comment**. They are one editing gesture, seen from two gates.

**Consequence for the brief's framing:** the two reports are not two bugs to fix separately. The single
question at every site is *"the header says this was subtracted — was it?"*, and that question decides
restore-vs-delete without a design call at four of the six sites.

---

## 4 · THE REPAIR — snippet sources only, `canon.css` never hand-touched

The rule applied uniformly, and stated so it can be checked:

> **If the file's own header says the thing was removed → finish removing it.
> If the markup does not use it and the theme block deliberately lacks its token → delete the dead rule.
> If it IS live and a sibling in the same family already declares the token → declare it, copying the
> sibling's value verbatim.**

| file | edit | which rule | evidence it is right |
|---|---|---|---|
| `knowledge/snippets/Template-confirmation.reference.html` | deleted the orphan tail at `:193` | header-says-removed | file header names the `.confirm .btn` ladder deletion |
| ″ | deleted `.status.err{…}` (replaced by a comment recording why) | dead-rule | no `status err` in markup; theme block declares no `--error`/`--error-tint` |
| ″ | added `--header:#F0F0F0; --fborder:#808080;` (light) / `#1F1F1F; #808080` (dark) + both manifest entries | live-chrome | values verbatim from `Template-dashboard.reference.html:148,201` |
| `Template-error.reference.html` | deleted the orphan tail at `:182` | header-says-removed | same header clause |
| ″ | deleted `.confirm .success{…fill:var(--success)}` | dead-rule | no `.success` in markup; header: *"NO rag/\* token in this file at all"*; composition rule 6 |
| ″ | added `--header`/`--fborder` light+dark + manifest entries | live-chrome | as above; **neither is a rag token, so the header's absence claim still holds** |
| `Template-empty.reference.html` | added `--header` light+dark + manifest entry | live-chrome | file already declared `--fborder` + its manifest entry — this completes a pattern it was already following |
| `Template-settings.reference.html` | deleted `.status.ok` and `.status.warn` | dead-rule | markup carries only `status inf`; theme block declares `--info`/`--info-tint` only |
| ″ | added `--header` light+dark + manifest entry | live-chrome | as above |

Every deletion left a **comment in its place** naming what was removed and why, so the next carry cannot
repeat the gesture blind.

### ✅ The values were not invented — the generator confirmed them independently

`gen_snippet_tokens.py` regenerates every theme-block value FROM `knowledge/tokens/*.json` via each
snippet's own manifest. Run against the repaired tree:

```
gen_snippet_tokens: 4730 manifest bindings across 135 snippets + 9 tranches;
0 value(s) projected; 0 canon.css literal(s) projected.
OK — snippets + tranches + canon.css in sync with tokens.
```

**`0 value(s) projected`** = the hand-typed `#F0F0F0` / `#1F1F1F` / `#808080` are byte-identical to what
`table/header/background` and `form/border/default` resolve to from the store. `_validate_snippets.py`
(the fidelity gate) exits **0**.

---

## 5 · PROOFS

### 5.1 Both gates, before → after (working tree, snippet-scope gate)

| gate | before | after |
|---|---|---|
| `_validate_property_resolves.py --strict` | exit **1** — `147 file(s), 12 failure(s)` | exit **0** — `147 file(s), 0 failure(s)` |
| `_validate_token_forks.py` (needs canon regen; scratch) | exit **2** — `unbalanced '}' at line 15409` | exit **1** — parses cleanly, reports 5 pre-existing forks (§ 6.1) |

### 5.2 Scratch-tree regen — the working tree's canon.css was never written

`/tmp/tplrepair` = the repo's `knowledge/` tree minus `assets/` (36 MB), sandbox-local.
`(NON-REPO: sandbox /tmp/tplrepair — proof workspace, not deliverable)`

After the full ordered serial (`gen_canon_components` → `gen_snippet_tokens` → `gen_theme_cascade`):

```
CANON_DETERMINISM (gen_canon_components.py --check)  = 0
CASCADE_CHECK     (gen_theme_cascade.py --check)     = 0
property-resolves gate (C2): 147 file(s), 0 failure(s)
brace balance across canon.css: open 7785  close 7785
dangling var() with no fallback, never declared, whole of canon.css: ['--sc', '--uf', '--undefined']   ← none from this lane
@keyframes cn-template-confirmation-pop        ← namespacing restored (canon.css:15413)
.cn-template-confirmation{ --header: var(--table-header-background); --fborder: var(--form-border-default); }   ← canon.css:15307-15308
```

### 5.3 A pre-repair COUNTERFACTUAL tree, to attribute every red

`/tmp/tplbase` — the same tree with all four files reverted to their pre-repair state.
It reproduces the reported defect exactly: `147 file(s), 12 failure(s)`, and after its own canon regen,
`_validate_token_forks.py` exits **2** at `line 15409`. **This attributes the crash entirely to the two
orphan tails** — freshly generated from pre-repair sources, the same crash, the same line.

Four other gates are red in **both** trees. Output diffed byte-for-byte:

| gate | baseline | repaired | verdict |
|---|---|---|---|
| `_validate_radius.py` | 1 | 1 | **OUTPUT IDENTICAL** — pre-existing |
| `_validate_type_composites.py` | 1 | 1 | **OUTPUT IDENTICAL** — pre-existing |
| `_validate_compose.py` | 1 | 1 | **OUTPUT IDENTICAL** — pre-existing |
| `_validate_assertions.py` | 1 | 1 | identical but for the tmp path in the traceback — pre-existing |

### 5.4 The driven render — 159 checks, four themes, both modes

Harness (NON-REPO: `/tmp/tplrepair/drive_template_repair.py`), run per `_RUNBOOK-render-verify.md`
with a fresh `s213e4` symlink font farm.

**Font asserted with two controls, inside the measured frame (#138 discipline — `fonts.check()` lies):**

```
{'target': 347, 'alias': 347, 'ctl_real': 375, 'ctl_none': 301}
```
Target == alias, and both differ from the DejaVu control **and** the nonexistent-face control. The real
licensed cut is on the page.

- **Part A** — the four repaired snippet sources, light + dark: `--header`/`--fborder` RESOLVE;
  `.demo-bar` background **equals the token AS A COLOUR** (240,240,240 / 31,31,31); button border
  equals (128,128,128); background is neither transparent nor `currentColor` (the two ds-018 initial
  values). Confirmation's roundel fill is not black and its entrance animation is still bound
  (namespacing survived). `Template-error` carries **0** `.success` elements and **>0** anchor glyphs.
- **Part B** — the scratch-regenerated `canon.css`, **FOUR apollo themes × light + dark** (mono ·
  legacy · console · supercharge): in all 8 cells, for all 4 template scopes, `--header` and `--fborder`
  resolve on the canon scope and the demo bar's background is delivered rather than initial.
  Supercharge takes its warm-ramp values (`--header:#DFDEDC` light / `#2A2621` dark;
  `--fborder:#524842`) — proving the tokens travel the DNA tier correctly, not just mono.

```
checks run: 159   failures: 0
bite arms that could NOT fail: 0
```

Two crops read (NON-REPO: `outputs/tplrepair-confirmation-light.png`, `outputs/tplrepair-error-dark.png`;
smallest crop carrying the verdict, per `_RUNBOOK-context-gauge.md` § PRICE THE INSTRUMENT). Both correct:
demo bar grey in light / near-black in dark with grey-bordered buttons, green roundel with white tick,
error page showing the Empty-state anchor glyph and no roundel.

### 5.5 EVERY FIX SHOWN ABLE TO FAIL (#104 / #171 — drive the thing)

Five mutants. **One of them caught my own instrument first**, which is the point of the exercise:

| # | mutation | expected | observed |
|---|---|---|---|
| M1 | re-insert the orphan tail in `Template-confirmation`, regen canon | forks gate exits 2 | ✅ `unbalanced '}' at line 15411` · exit **2** |
| M1′ | revert M1, regen | exits 1, no crash | ✅ exit **1** |
| M2 | drop `--header`/`--fborder` from the **light** block only | gate reds | ❌ **STAYED GREEN — the mutant was too weak.** The gate is file-scope by construction (its own docstring: *"CANNOT see per-SELECTOR scope"*), so the dark declaration still satisfied it. |
| M2b | drop them from **both** blocks | gate reds | ✅ exit **1**, names `--fborder` and `--header` in `Template-error` |
| M3 | restore the deleted `.status.err` rule | gate reds | ✅ exit **1**, names `--error` and `--error-tint` in `Template-confirmation` |

**Render bites — the ds-018 and #184 symptoms reproduced live, in the browser:**

| bite | observed |
|---|---|
| revoke `--header` in-frame | `.demo-bar` background → `rgba(0, 0, 0, 0)` — the *initial* value, exactly ds-018's shape |
| revoke `--fborder` in-frame | button border → `rgb(26, 26, 26)` — **`currentColor`, i.e. full ink**, the identical 13×-contrast signature ds-018 was named for |
| revoke `--success` in-frame | roundel fill `rgb(102, 204, 141)` → **`rgb(0, 0, 0)`** — the #184 SILENT BLACK class, demonstrated |

⚠ **M2 is the honest headline of this section.** A green run of the property-resolves gate does **not**
mean both modes are declared — it means *at least one place in the file* declares the name. A
light-only or dark-only omission passes it. That is published in the gate's own docstring; it is
restated here because this lane nearly banked a proof that could not fail.

---

## 6 · RESIDUALS AND FINDINGS — declared, not fixed

### 6.1 ⚠ FIXING THE BRACE UNMASKS FIVE FORK FAILURES. The conductor must expect this.

`_validate_token_forks.py` **crashes at the first unbalanced brace and reports nothing else**. With the
brace repaired it parses the whole file and goes:

**exit 2 (crash, zero forks reported) → exit 1 (5 forks not in the ledger).**

```
FORK  --l-min     mono/any   canon.css:11980 .cn-layout-utilities .l-grid  ×  canon.css:17812 .cn-template-report .tpl-stats
FORK  --min-pri   mono/any   canon.css:5405  .cn-app-shell-split .sp       ×  canon.css:14216 .cn-splitter .sp
FORK  --min-sec   mono/any   canon.css:5406  .cn-app-shell-split .sp       ×  canon.css:14217 .cn-splitter .sp
FORK  --move      mono/any   canon.css:2561  .cn-tabs                      ×  canon.css:17887 .cn-template-settings
FORK  --panel     supercharge/dark  canon.css:23575 .cn-app-shell-multi-column × canon.css:23604 .cn-app-shell-nav-rail
```

**None is introduced by this lane** — proven by the counterfactual tree, where the same five appear the
moment the brace is repaired there too, and by name: this lane touched only `--header` and `--fborder`,
neither of which appears above.

★ **These are five LOCAL-VAR COLLISIONS — the count and the shape match Lane E3's `W-59` charter
("rename the 5 ledgered local-var collisions") exactly, and two of the five sit in Template scopes
(`.cn-template-report`, `.cn-template-settings`).** This lane did not touch them; `W-59` is E3's row.
**Worth the conductor's eye: `W-59`'s ledger and this gate's live output may be the same five, which
would mean E3's renames turn this gate green.** Stated as an observation with its probe, **not** a
claim about E3's ledger, which this lane did not read.

**Practical consequence:** after the serial regen, `_validate_token_forks.py` will be **RED at exit 1**,
not green. That is progress (a crash became a report), but a wrap that expects green will be surprised.

### 6.2 ⚠ Demo chrome reaches canon.css — 24 rules, and it is why this lane had to declare table tokens

`.demo-bar` is **not** in `gen_canon_components.py`'s `DROP_FIRST` tuple
(`"body", "html", "*", ".demo-controls", ".cap", ".stateLabel"`), and `".demo-bar".startswith(".demo-controls")`
is False — so `grep -c "demo-bar" knowledge/canon/canon.css` → **24**. Blocks the snippets label
*"DEMO CHROME … NOT the template"* ship inside the canon component layer.

This is the reason the (a)-shape repair had to be *declare* rather than *delete*: with demo chrome in
canon, deleting the declaration would leave `var(--header)` dangling **in canon.css**, which is the #184
silent-black class. Declaring it was the safe move. **The cleaner fix is upstream and is not this lane's
to make** — see PROPOSED-2.

### 6.3 ⚠ `_validate_assertions.py` CRASHES (a crash is not a fail)

Identical traceback in both trees, so **not caused by this lane**:

```
File ".../_validate_assertions.py", line 370, in selftest
    assert ok, "file_contains must find a present needle"
AssertionError: file_contains must find a present needle
```

Honest scope: both trees carry *today's* other-lane edits, so this receipt can say the crash is
**not mine**. It cannot say whether it predates today. Named for whoever owns that gate.

### 6.4 ⬛ UNPROVEN BY SCOPE, declared

- The **four-theme** proof (Part B) drives `--header` / `--fborder` / demo-bar delivery. It does **not**
  re-prove the whole Template family's appearance per theme; that was never this lane's scope.
- The snippet reference pages are **two-mode** (`light`/`dark` on `<body>`), not four-theme. "Four
  themes" was proven against **canon.css**, which is where the apollo layer lives. Stated plainly rather
  than claimed for both surfaces.
- ⚠ **`data-theme` sits on `<body>`, not `<html>`, in these snippets.** The first harness set it on
  `documentElement` and every dark cell silently returned the **light** value — four false REDs that
  looked like a repair defect. Recorded because the next render lane will hit it.

---

## 7 · PROPOSED — NOT RULED. Dave's.

**PROPOSED-1 · delete-vs-declare at the six repair sites.**
This lane read the #210 wave's intent off the file headers and the markup, and chose **delete** wherever
the header announced a subtraction or the markup lacked the state (four sites), **declare** wherever the
block is live and a sibling already declares the token (two vars, four files). The alternative reading
at the two chip sites is:

> add `--error`/`--error-tint` to `Template-confirmation` and `--success-tint`/`--warning`/`--warning-tint`
> to `Template-settings`, copied verbatim from `Template-dashboard.reference.html:164,212`, keeping the
> chip blocks whole so the templates carry all four RAG states whether or not the demo markup shows them.

Reason this lane did **not** take it: each of those theme blocks opens with *"Every value COPIED from the
source snippet named beside it. **Nothing is new.**"* — adding a RAG value those files deliberately omit
would be new, and `Template-confirmation`'s light `--error` would additionally land on the **two-red law**
(`s151-D1`: `#DA1A00` on white, `#F6604C` else), which is Dave's and untouchable. Deleting a dead rule
raises no colour question at all. **If Dave prefers whole chip blocks, the swap is four lines and the
two-red question comes with it.**

**PROPOSED-2 · the class fix, upstream: drop demo chrome at the harvester.**
Adding `".demo-"` to `gen_canon_components.py`'s `DROP_FIRST` would stop all 24 demo-chrome rules
reaching canon.css, after which no template would need to declare a table token for a table it does not
have. **Not done here** — it changes canon output for components beyond this lane's four and is exactly
the kind of cross-cutting generator change the brief fences. Priced **S**.

**PROPOSED-3 · make the generator refuse an orphan, instead of emitting garbage.**
`walk()` silently turned a stray declaration into a selector list, produced unbalanced CSS **and**
bypassed keyframe namespacing. `gen_canon_components.py` already carries this exact lesson in its own
comments for a different species (*"FIX THE CLASS AT THE EMITTER: no authored string can close the
comment it is written into"*, ds-039 second species, #213). The same principle says a `('decl', …)` at
rule position, or a selector candidate containing `;` or `{`-less `}`, should **fail loud and named**
rather than emit. Priced **S**. It would have caught this at #210 instead of at #213. **Dave's call —
it is a new refusal in a generator three lanes are running today.**

**PROPOSED-4 · the `--header`/`--fborder` token binding for non-table templates.**
This lane bound `--header` → `table/header/background` and `--fborder` → `form/border/default`, copying
`Template-dashboard`. For a confirmation or error page that has neither a table nor a form, those paths
are borrowed rather than semantic. If Dave wants demo chrome bound to something honest, the binding is
one line per manifest — but a new semantic path is a token decision and is his.

---

## 8 · SERIAL STEPS THIS WORK OBLIGATES (conductor's, per `_build_all.py` order)

Snippet sources changed **and** their `#token-manifest` `vars` maps gained entries, so three ordered
generator steps are obligated. Order is `_build_all.py`'s, not invented — the memory hook
*"Regen serial set is ORDERED"* records ~6 CI reds paid at #210 for missing exactly this:

| order | step | why this lane obligates it | proven in scratch |
|---|---|---|---|
| `_build_all` :211 | `python3 knowledge/canon/gen_canon_components.py` | **MANDATORY** — the repair reaches canon.css only through this. Without it canon keeps the mangled rule and the forks gate keeps exiting 2. | ✅ `--check` exits 0 after |
| :219 | `python3 knowledge/gen_snippet_tokens.py` | manifest consumer; **no-op for these edits** (`0 value(s) projected`) but it is in the serial | ✅ exits 0, no file changed |
| :224 | `python3 knowledge/canon/gen_theme_cascade.py` | **MANDATORY** — the 6 new manifest bindings need their `[data-apollo-theme]` overrides. It writes **12 new lines** (supercharge `--header:#DFDEDC`/`#2A2621`, `--fborder:#524842` across the four scopes). CI runs it as `--check`, so skipping it is a guaranteed red. | ✅ `--check` exits 0 after |

**No registry, `MIGRATED_SNIPPETS`, `CATEGORIES` or spine step is obligated** — no snippet was added,
renamed or migrated; four existing files were edited in place.

**No store row is obligated for this receipt** — probed, not assumed: `knowledge/_gate_doc_rows.py:48`
reads `PATTERNS = ["notes/_briefs", "_BRIEF-"]`, so the #185 doc-row gate's population is briefs, not
`notes/_receipts/*`. This file falls outside it.

⚠ **Expect `_validate_token_forks.py` RED at exit 1 after the serial** (§ 6.1). It is a *report*
replacing a *crash*, and the five it names belong to `W-59`, not here.

---

## 9 · FENCES OBSERVED

- ⛔ **No git command of any kind** was run — not `status`, not `diff`, not `add`. Baselines were
  reconstructed by inverse text patch in a scratch tree, precisely to avoid `git checkout`
  (`specimen-starts-from-reference` runbook step 0, sub git-checkout ban).
- ⛔ **No shared state touched**: `GOOD-MORNING.md`, `_LIVE-STATE.md`, `_CHAIN.md`, `MEMORY.md`,
  `knowledge/_state.json`, `knowledge/_rulings.json`, `_lanes.json`, registries and spine — all unread
  for write and unwritten.
- ⛔ **`knowledge/canon/canon.css` was NOT regenerated in the working tree.** Every canon proof ran in
  `/tmp/tplrepair` / `/tmp/tplbase`. Three other lanes' canon edits today are untouched by this lane.
- ⛔ **Nothing here is a ruling.** Four open choices are marked PROPOSED in § 7.
- Files written by this lane: the four snippet sources listed in § 4, and this receipt.
