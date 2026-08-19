# Receipt — #203 Wave 3b, Lane G · the canon dark-drop repair

*Worker receipt per `_BRIEF-wave3b-verified-work-2026-08-19-v1.md` (Lane G) and the base brief it
extends. Written 2026-08-19 against HEAD `ec2336d`. Opus work sub, maximum reasoning effort.*
*⛔ **Nothing here is a ruling.** No commit, no push, no `git checkout/restore/stash`, no `_build_all.py`.*
*`knowledge/_rulings.json`, `knowledge/tokens/*`, `GOOD-MORNING.md`, `_LIVE-STATE.md`, `MEMORY.md`,
`_DS-IMPROVEMENTS.md` untouched.*

**Context gauge — declared, with its defect named.** `_checkin.py --no-rehearse --no-grades --no-block
--window 200000` reads the **newest mounted transcript**, which in a parallel run is the **conductor's**,
not this sub's (165 records, last record 651 s / 11 min stale — a sub's own turns are not in it). Its
headline (195,220 real MEASURED / FILL 145,808 real / boot 56,488) is therefore **the conductor's number,
not Lane G's**, and I will not present it as mine. `[[measuring-tool-must-not-guess]]` — UNKNOWN is never
defaulted. Lane G's own spend is **unmeasured by instrument**; rough self-read: ~20 tool calls, one long
lane, no call-boundary kills, no chunking failures.

---

## Step 0 — the premise, verified first-hand (the brief's hardened §1)

| Claim inherited | Verified? | Probe, named and quoted |
|---|---|---|
| HEAD is `ec2336d` | ✅ | `git log --oneline -1` → `ec2336d #202 2026-08-18 …` |
| `gen_canon_components.py:76` carries the drop test | ✅ | file read; line was `if first in (":root",) or first.startswith("[data-theme"): return True` |
| **33 rules dropped across 19 snippets** (Lane C finding 1) | ✅ **TRUE — reproduced independently** | `/var/tmp/s203g/probe.py`, walking every snippet's `<style>` with **the generator's own `walk()`**, not a fresh regex: `TOTAL … 33 · SNIPPETS affected: 19 of 76` |
| …and the per-component split matches Lane C's | ✅ exactly | 4 Notifications · 3 Form-layout · 3 Input-fields · 2 each Amount-input/Date-picker/Date-range-picker/Secure-entry/Stepper/Textarea/Time-picker · 1 each ×8 charts + File-upload |
| the ancestors are all `[data-theme="dark"]` | ✅ (new fact) | probe's ancestor histogram: `{'[data-theme="dark"]': 33}` — **no light-mode component rule was ever dropped**, so light is a free control |
| `prefix_selector` already holds a root ancestor at the front | ✅ | file read, lines 84-99 + its own comment; the capability existed, the **ordering** defeated it |

A carried COUNT is a claim and it ages `[[premise-ages-faster-than-rule]]` — this one did not. It measured
33 on the nose, from a different instrument than the one that first found it.

---

## The repair — `knowledge/canon/gen_canon_components.py` (the one file I edited)

A **discrimination**, not a new value. The drop test now judges a root-anchored selector **by its
descendant**:

```python
ROOT_ANCESTOR = re.compile(r'^((?::root|html)(?:\[[^\]]*\])*|\[[^\]]*\])\s+(.+)$')

def is_harness(sel):
    first = sel.split(",")[0].strip()
    if first in (":root",): return True
    m = ROOT_ANCESTOR.match(first)
    if m: return is_harness(m.group(2))              # judge by the DESCENDANT
    if first.startswith("[data-theme"): return True  # BARE [data-theme=…]{--v:…} = harness vars
    …unchanged…
```

- **no descendant** ⇒ still a harness var block ⇒ still dropped.
- **has a descendant** ⇒ a reviewed component rule ⇒ kept, and handed to `prefix_selector`, which
  already knows to keep the ancestor at the FRONT (`[data-theme="dark"] .cn-x .foo`, never the
  unmatchable `.cn-x [data-theme="dark"] .foo`).
- The regex is deliberately the **same shape** as `prefix_selector`'s, so the two cannot drift apart.
- Recursion terminates: each step strips a prefix, the string strictly shrinks.

### Regression measured in BOTH directions, not just the happy one

`/var/tmp/s203g/delta.py` runs the OLD predicate and the NEW one over every rule in every snippet:

```
DROPPED -> KEPT (the repair):   33
KEPT -> DROPPED (regression risk): 0
```

**0 regressions.** The `:root[data-modality="pointer"] .box` family (the input-modality ring
suppression the `prefix_selector` comment cites) was checked explicitly — still kept.

---

## Mutation test — the CLAUSE, and then the FEATURE

`[[mutation-tests-the-clause-not-the-feature]]`: a green test proves nothing until you have watched it
go red. `/var/tmp/s203g/mutation.py`, rc **0**, all six arms:

| arm | result |
|---|---|
| BASELINE — repaired clause live, dark rule present in the generated partial | **PASS** |
| **MUTANT 1** — descendant-discrimination killed (the shipped defect restored) ⇒ `[data-theme="dark"] .cn-secure-entry .se-msg .ic` **VANISHES** | **PASS** (the test can fail) |
| **MUTANT 2** — bare-`[data-theme]` guard killed ⇒ harness var block **LEAKS** into the partial | **PASS** |
| MUTANT 2 control — that leak is **absent** from the repaired build | **PASS** |
| **MUTANT 3** — `prefix_selector`'s front-hold killed ⇒ selector becomes the unmatchable `.cn-secure-entry [data-theme="dark"] …` | **PASS** |
| MUTANT 3 control — that shape is **absent** from the repaired build | **PASS** |

Mutant 2 matters as much as mutant 1: it proves the fix did not simply *stop dropping things*. Both
halves of the discrimination are load-bearing and independently killable.

---

## Regeneration — the diff is exactly the repair, and nothing else

```
python3 knowledge/canon/gen_canon_components.py          -> generated 76 components, rc 0
python3 knowledge/canon/gen_canon_components.py --check  -> OK — 76 components in sync, rc 0   (determinism guard, ADR-0013 ruling 4)
```

Byte-diff of `canon.css` against a pre-run snapshot (`/var/tmp/s203g/canon-before.css`):

| measurement | value |
|---|---|
| lines **added** | **33** |
| lines **removed** | **0** |
| added lines NOT matching `^\[data-theme="dark"\] \.cn-` | **0** |
| harness var-override blocks `^\[data-theme="dark"\] \.cn-x{` | **14 before, 14 after** — unchanged |
| component dark rules `^\[data-theme="dark"\] \.cn-x <descendant>` | **0 before → 33 after** |
| unmatchable `\.cn-… \[data-theme` shapes anywhere in canon | **0** |
| per-component split of the 33 | **identical to the pre-fix measurement**, component for component |

A surgical, fully-attributed diff. Not one existing byte moved.

---

## Every `--check` generator, swept — and a NEW machinery finding

| generator | rc | reading |
|---|---|---|
| `gen_canon_components --check` | **0** at my run | in sync — see the ⚠ staleness note below |
| `gen_canon_tokens` | 0 | **⛔ has NO `--check` contract — it WROTE `canon.css` regardless.** Verified harmless: the 33 survived and the whole-file diff stayed at exactly 33 |
| `gen_theme_cascade --check` | 0 | 228 override paths, 209 component projections in sync |
| `gen_component_partials --check` | 0 | all AUTO-PARTIAL blocks in sync, contracts hold |
| `gen_dashboard --check` | **1** | OUT OF SYNC. **Not caused by this lane** — it derives from the stores and live gate results, which five sibling lanes are moving. Left to the conductor; the dashboard is shared and its ranking is Dave's eye `[[home-pointer-rot-class]]` |
| `gen_gallery` | 0 | **⛔ NO `--check` contract — WROTE.** Re-synced `knowledge/_fitness-test/canon-gallery.canon.html`: it was **badly stale at HEAD, 39 component scopes of 76; now 77**. +3720/−103 lines. That staleness pre-dates me |
| `gen_kg_edges` | 0 | **⛔ NO `--check` contract** |
| `gen_radius_derive --check` | 0 | proposal matches recomputation, 4 themes |
| `gen_runbook_index` | 0 | **⛔ NO `--check` contract — WROTE.** Diff is one line: `last generated 2026-08-17` → `2026-08-19` |
| `gen_showroom --check` | 0 | 76 pages + index in sync |
| `gen_snippet_tokens --check` | 0 | 2412 bindings, 0 values would change |
| `gen_token_ramp --check` | 0 | 0 drifted, 88 in sync |
| `gen_gardener_controller --check` | 2 | argparse: `unrecognized arguments: --check` — **fails LOUD, which is correct** |
| `guidelines/gen_rules_index --check` | 1 | crash: swallowed `--check` as a **path** → `FileNotFoundError: '--check/_rules-index.md'` |

### ⛔ FINDING (new, mine) — `--help` was gated in #158; `--check` never was

`_helpgate.py` closed the write-by-default class for `--help`, and `_validate_help_gate.py` keeps it
closed (rc 0, 146 scripts). **`--check` has no equivalent contract.** Measured: **4 of 13 generators —
`gen_canon_tokens`, `gen_gallery`, `gen_runbook_index`, `gen_kg_edges` — contain no `--check` string at
all and write unconditionally**; `gen_rules_index` mis-parses it into a path and crashes. So the base
brief's own instruction to component lanes — *"`--check` (read-only) is fine"* — **is false for five of
these scripts**, and a lane obeying the fence can dirty shared artefacts believing it is reading.
This is `[[instrument-without-a-consumer]]` in its other polarity: a *contract* nobody enforces.
**PROPOSED #203 → `_DS-IMPROVEMENTS.md`** (conductor merges; ⛔ I may not edit it): a `check_gate`
sibling to `help_gate`, plus an AST gate in the shape of `_validate_help_gate.py`.

---

## Gates run — every rc, with attribution

Chosen because they are the gates that could plausibly *see* a 33-rule addition to `canon.css` or an
edit to a generator. All whole-population (no gate's glob reaches `reviews/` — `[[gate-glob-scope-rule]]`).

| gate | rc | reading |
|---|---|---|
| `_validate_help_gate.py` | **0** | 146 scripts; my edited generator still answers `--help` before it can write |
| `_validate_no_hardcode.py` | **0** | 11 tranche files — the 33 recovered rules carry literal `#FFFFFF`/`#000000`, and the gate accepts them (they are the snippets' own reviewed values, carried VERBATIM by design) |
| `_validate_css_governed.py` | **0** | 11 tranche files |
| `_validate_dark_surfaces.py` | **0** | 0 flat-white failures, 9 annotated exceptions |
| `_validate_screen.py` | **0** | **PASS** — this is the gate that governs the regenerated gallery |
| `_validate_partials.py` | **0** | 0 strict fails, 32 census rules |
| `_validate_property_resolves.py` | **0** | 93 files, 0 failures |
| `_validate_theme_provenance.py` | **0** | ADVISORY; 38 hardcoded foreign-theme hexes in 110 Mono files — pre-existing, unchanged by me |
| `_validate_snippets.py` · `_validate_a11y.py` · `_validate_type_composites.py` | — | **NOT RUN — declared gap.** They read `knowledge/snippets/*`, which **five sibling lanes are actively editing right now** (see residuals). Any number I took would be theirs, not mine, and running them appends to shared audit artefacts. Left to the conductor at reconcile. Lane C's readings at HEAD stand: snippets rc 1 (18 pre-existing `--pri-hover` DRIFT), a11y rc 0, type-composites 1097 |
| `_validate_state_contrast.py` | — | **NOT RUN — declared gap.** Exceeds the call cap on 76 snippets; a filtered run overwrites the tracked audit artefact |
| `_validate_radius.py` | — | not run — `MIGRATED_SNIPPETS` is ⛔ shared and I added no snippet |
| `_build_all.py` | — | ⛔ **NOT RUN**, per the fence |

**My own review page, hand-probed** (no gate's glob reaches it): **0 raw `font-size`**, **0 raw `font:`
shorthand**, 1021 `.t-cm-*`/`.t-ed-*` composite uses, **0 `border-radius` declarations** (square by
default), `min-height:44px` on every control in the switcher, `:focus-visible` outline present.

---

## The review surface — `reviews/REVIEW-203-canon-dark-repair-before-after-v1.html`

562 KB, self-contained, **38 panes across 19 components**, before vs after, with a live four-theme +
light/dark controller `[[feedback-live-controller]]`.

**Both sides are DERIVED, never hand-authored.** `[[specimen-starts-from-reference]]`:

1. **The specimens are copied**, not re-drawn — each pane is the `<section class="g-item">` body from
   the regenerated `canon-gallery.canon.html`, which is itself each reviewed snippet's own demo markup.
   All 19 found; none improvised.
2. **The BEFORE column is the shipped behaviour, byte-derived.** Every rule mentioning
   `[data-theme="dark"]` was harvested from the **pre-fix `canon.css` snapshot** with the generator's own
   `walk()` (228 rules, `@media` wrappers preserved) and re-keyed `dark` → `darkbefore`. The 33 repaired
   rules are absent from that column **by construction — the snapshot never had them.** Nothing is
   reconstructed by hand, so nothing can be wrong by hand.
3. **The AFTER column is the live `canon.css`**, linked. Both columns share one identical base cascade —
   provable, because the diff between the two canon files is 33 additions and 0 removals.
4. Three transforms, each declared: the SVG sprite hoisted once per page; the gallery's own `g-name`
   caption dropped (the page supplies its own heading); every id namespaced `<id>--<component>-<side>`.

### Two defects in my own page, caught by parsing the output in its own grammar

The first build passed by eye and **failed the parse** `[[no-gate-parses-the-artefact]]`:

- **25 dangling ARIA references.** `aria-labelledby` / `aria-describedby` are **space-separated token
  lists**; my first namespacing regex matched a whole attribute value against a single id, so every
  multi-token reference was left behind pointing at an id that had just been renamed. Fixed by
  tokenising the value. **This is the exact class the repair itself is about** — a test that reads the
  first thing and calls it the whole thing.
- **14 duplicate ids**, inherited: the gallery source carries **21 cross-section duplicate ids** of its
  own. Fixed by namespacing per *component*, not just per side — this page is now cleaner than the
  artefact it copied. (⚠ **The gallery's 21 duplicates are a real pre-existing defect, surfaced, not
  fixed** — it is a generated shared artefact and `gen_gallery.py` is not mine to redesign.)
- `data-for` (a behaviour hook) is namespaced too, so the panes stay self-consistent. **Behaviour
  `<script>` blocks are NOT carried** — the surface is a visual compare; declared, not silent.

**Final parse: 449 ids, 0 duplicates, 0 dangling refs or fragments, 38 panes, 19 `.cn-` scopes.**

---

## Render proof — the FEATURE driven, `goto("file://…")`, never `set_content()`

Font asserted **with controls, never `fonts.check()`** (canvas, 40px `Handgloves 12345`) — matches the
runbook's recorded table exactly:

| probe | width | reading |
|---|---|---|
| `HSBC_MtUnivers_Latin` | **347** | the real cut |
| `"Univers Next HSBC"` (type.css `--uf`) | **347** | alias lands |
| `"Univers Next for HSBC"` (snippet `--font`) | **347** | alias lands |
| `DejaVu Sans` — control | 375 | genuinely different face |
| nonexistent face — control | 301 | default fallback |

Console errors: **none**. `.uuid` fontconfig strays in the TTF dir: **0** (symlink farm `/var/tmp/fonts-s203G`, #138 recipe verbatim).

### The whole repair driven, rule by rule, on rendered geometry

`/var/tmp/s203g/sweep.py` walks all **33** recovered rules, finds their targets in both columns and
diffs the *computed* style:

```
RULES: 33 | measurably CHANGED the render: 22
        | matched but no computed diff: 9  | no matching element in the demo: 2
```

- **22 changed outright.** Worked examples, computed, not read off a stylesheet:
  - `Input-fields .err-msg .ic` — `rgb(246,96,76)` → `rgb(255,255,255)`
  - `Form-layout .fl-msg .ic` — `rgb(246,96,76)` → `rgb(255,255,255)`
  - `Notifications .note.tint` — `--mark: #260005` → `#000000`
  These are the **mono error ink camp** (`s149-D1`/`s194-D1`) reaching dark mode for the first time.
- **8 of the 9 "no diff" are the chart `:hover` rules** — a non-hovered element cannot show them. So I
  **drove the hover**: `Chart-bar rect.dv-series:hover` filter **`brightness(1.12)` → `brightness(1.22)`**.
  One clause, identical across all 8 charts. That is 30 of 33 proven live.
- **1 genuine no-op**: `Form-layout .fl-summary .fl-sumtitle{color:…}` computes white in both columns —
  another rule already supplies it. Recovered correctly, changes nothing. **Said plainly, not hidden.**
- **2 have no target**: `Stepper .st-group.is-error …` — the gallery demo carries no error-state stepper.
  ⬛ **UNPROVEN BY DEMO COVERAGE, declared.**

### Controls, so the page cannot lie

- **Light mode**: identical computed values in both columns — as it must be, since all 33 rules are
  `[data-theme="dark"]`. If light had differed, the harness would be lying.
- **Page background**: identical in both columns — the base cascade really is shared.
- **Supercharge dark ground** = `rgb(19,17,14)` — the theme cascade is live on the page (Lane C's control).
- **Responsive**: `.grid` collapses to a single 590 px column at 480 px — stacks, does not squeeze.
- **Seen, at 1400 px and 480 px.** The Input-fields crop is the one to look at: in BEFORE the section
  heading (`.uic`) is dark-on-dark and effectively **invisible**, and the error field's border is white;
  in AFTER the heading reads white and the error border is red. That is what 33 missing rules look like.

---

## Residuals — declared, not glossed

- ⚠⚠ **`gen_canon_components --check` is RED again as I close, and it is NOT my change.** Sibling lanes
  have since edited 9 snippets and added 7 new ones. Measured, so the conductor does not have to guess:
  a re-run would **ADD 596 lines, REMOVE 0**, and the dark-descendant count goes **33 → 39** — the repair
  immediately pays forward, catching 6 more such rules in the brand-new snippets. **0 removals proves my
  33 survive a re-run.** ⛔ I deliberately did **not** regenerate again: it would bake other lanes'
  in-flight, ungated snippets into a shared artefact and be stale again within minutes. **The conductor
  must re-run `gen_canon_components.py` at reconcile** (base brief §4 already says so). The **repair
  lives in the generator and is permanent**; the canon regeneration is a point-in-time proof.
- ⚠ **Running the generators and gates modified tracked shared files** — `_A11Y-GATE.md`,
  `_ICON-SOURCE-AUDIT.md`, `_PARTIALS-GATE.md`, `_REVIEW-SIGNOFF.md`, `_SCREEN-GATE.md`,
  `_SNIPPET-AUDIT.md`, `_THEME-PROVENANCE-GATE.md`, `_graph-mark-observations.jsonl`, `_RUNBOOKS.md`,
  `canon-gallery.canon.html`. I did **not** restore them: `git checkout/restore` is ⛔ banned and is
  exactly how #202's sub destroyed uncommitted work. **Five lanes are live in this tree, so I cannot
  attribute these to myself alone and will not claim to. Conductor: reconcile each path deliberately —
  do not blind `git add -A`.**
- ⚠ **`notes/_REHEARSAL-LOG.jsonl` has 16 appended `rehearse` rows.** I ran `_checkin.py` with
  `--no-rehearse` precisely to avoid this; the rows are almost certainly siblings' and the conductor's.
  **Unattributable, declared.**
- **My PNGs** are in `_to_delete/s203G-render/` — verified **gitignored** (`.gitignore:25`), so they
  cannot dirty the tree. Not deleted: the sandbox cannot `rm`, and cleanup must be a same-mount `mv`.
- ⬛ **UNPROVEN BY SCOPE:** I did not check whether `reviews/REVIEW-203-INDEX-2026-08-19-v1.html` lists
  my page. It is a shared file outside my fence — **conductor should add the row.**
- ⬛ **UNPROVEN BY SCOPE:** whether the 6 additional dark rules in the new sibling snippets are correct;
  I only measured that the repaired generator now carries them.
- **Throwaway scripts** live in `/var/tmp/s203g/` (probe · delta · mutation · build_review · sweep ·
  hover · render). **0 instrument added to the repo** — nothing here is a thing the repo must carry.

---

## For the conductor to merge

1. **`_DS-IMPROVEMENTS.md`** — the **`--check` contract gap** (new, mine): 4 of 13 generators have no
   `--check` string and write unconditionally; a 5th crashes on it. Remedy in the shape of #158's
   `help_gate` + `_validate_help_gate.py`.
2. **`_DS-IMPROVEMENTS.md`** — Lane C's finding 1(b), still **OPEN and untouched by me**: no gate parses
   the generated partial in its own grammar and diffs it against the source snippet. That absence is
   *why* 33 rules could vanish with six gates green `[[no-gate-parses-the-artefact]]`. The detector is
   cheap — `/var/tmp/s203g/probe.py` is ~25 lines and already does the parse. ⛔ Not built here: a new
   shared instrument is the conductor's / Dave's to site and wire (Lane L was fenced the same way).
3. **`gen_gallery.py` was 39 of 76 components stale at HEAD**, and it also emits **21 duplicate ids**.
   Both pre-date this session. Surfaced, not fixed.
4. **Re-run `gen_canon_components.py` at reconcile** — see residual 1. Non-optional.
5. **Add `REVIEW-203-canon-dark-repair-before-after-v1.html` to the REVIEW-203 index.**
6. **No CATEGORIES entry, no token proposal, no snippet, no meta** — this lane added none.

## Decisions needed from Dave

| # | Decision | Default if he says nothing |
|---|---|---|
| 1 | **Accept the repaired drop test?** 33 reviewed dark-mode rules now reach `canon.css`; 30 proven live on screen, 1 no-op, 2 untargeted by the demo. Review page is the eye-check | the fix stands in the working tree, uncommitted |
| 2 | **Gate the class** — a snippet-vs-generated-partial parse gate. Without it the next silent drop is invisible again | no gate; the next one goes unseen |
| 3 | **A `--check` contract for generators** (4 write regardless). This one bit the *brief itself*: it told six lanes `--check` was read-only | lanes keep dirtying shared artefacts believing they are reading |
| 4 | `Stepper`'s error state has **no gallery demo** — add one, or accept 2 rules that no render can prove? | 2 rules stay UNPROVEN by demo coverage |
| 5 | `Form-layout .fl-summary .fl-sumtitle` recovers a rule that **changes nothing** — leave it, or drop it from the snippet? | dead rule carried forward |

## Friction log

1. **The strongest instrument was the generator's own parser.** Re-measuring the 33 with `walk()` rather
   than a fresh regex is what made the count trustworthy — a second regex would have been a second
   opinion, not a confirmation.
2. **A one-directional regression check would have shipped a hole.** Measuring `KEPT → DROPPED` as well
   as `DROPPED → KEPT` is what let me say "0 regressions" rather than "I didn't notice any".
3. **Mutating the OTHER half of the clause mattered as much as mutating the broken half.** Mutant 2
   proves the fix did not simply stop dropping things.
4. **My own page failed its own parse after passing my eye** — 25 dangling ARIA refs, from treating a
   space-separated token list as a single value. The same species of "read the first thing, call it the
   whole thing" as the bug I was fixing. Caught only because I parsed the artefact in its grammar.
5. **`--check` is not read-only, and the brief said it was.** Three generators wrote during a sweep whose
   entire purpose was to *not* write. A carried instruction ages like a carried count.
6. **A sub cannot measure its own context** — `_checkin.py` reads the newest *mounted* transcript, which
   in a parallel run belongs to the conductor. Reporting that number as mine would have been a confident
   false inscription. Priced TODO for whoever owns the instrument.
7. **`/var/tmp` farms all survived** (`pw-browsers-s197`, `chromelibs`, `pylibs-s203e`) — no download
   needed, runbook worked verbatim, ~2 calls to first pixel.
