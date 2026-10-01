# ADR-0013 — Component-type tier: shared VALUES and shared RULES (composition by retrieval)

**Status:** Accepted (Dave, 2026-07-21, in-chat — confirming all four firm recommendations, correctness-over-expedience stated as the deciding principle)
**Extends:** ADR-0008 (canonical core + adapters) · ADR-0010 (nullable flex slots) · ADR-0011 (four-theme override sets)
**Relates:** ADR-0009 (state-styling architecture — motion joins as tokens) · T-D9/T-D12 (type composites — the TYPE-side precedent this completes on the BOX side)

## Context

Atom retrieval was VALUE-level only: organisms bind the same tokens the atoms bind (colour roles,
radius roles, type composites) but re-implement the atoms' RULES locally. Surveyed 2026-07-21
(worker A's Phase-1 finding, sharpened by Dave to "retrieval must reach INSIDE organisms"):
**13/40 snippets carry a local button recipe; 7 carry Button's scale-press by copy; 4 press with
`translateY(1px)` instead — already-drifted physics (Selection-controls carries BOTH in one file).**
The interaction factors (`--btn-grow`/`--btn-press`) are LOCAL vars — not in the token store, not
theme-flexable (the pre-Phase-0 radius shape, again). Fanning ~50 Phase-2 components out on this
pattern duplicates sub-atoms ~50×; the radius ratchet just priced retro-fit at 21 files across three
sessions. The TYPE side already solved rule-sharing (T-D9 selector-list bindings + `type.css`
composites + the blast-radius gate); BOX/interaction had no equivalent. Dave's queued component-type
flex tier (`_FUTURE-STATE`, 2026-07-21) and the composition gap are one architecture question.

## Decision — four rulings, all firm

1. **Sequence.** The composition mechanism lands BEFORE Phase-2 fan-out.
2. **Mechanism = generated partials.** Atoms declare named rule-blocks; a generator injects them
   into consuming snippets between AUTO-PARTIAL markers (provenance comment per injected block);
   a `--check` sync gate fails the build on divergence. Snippets stay self-contained and
   source-of-truth — the existing projector contract extended from values to RULES. Runtime
   class-sharing is REJECTED inside the KB (it inverts source-of-truth: snippets would consume
   generated canon); that pattern belongs at the ADR-0008 adapter boundary. The component machine
   remains the horizon; partials are its parts bin. A **ratchet-style gate** (census → advisory →
   blocking, the proven radius pattern) makes local re-implementation of a registered partial's
   rule a build failure — gate the condition, don't patch instances.
3. **One registry, both halves.** `knowledge/component-types.json`: group → members + parameter
   tokens + rule partials. Resolution adds ONE hop to the existing alias-aware chain:
   **component → type-group → semantic role → default** (`gen_theme_cascade` already resolves
   alias chains). First population: `button-family` with motion tokens (press-grow / press-scale
   lifted from the local vars) — zero visual change in Mono; reduced-motion overrides ride INSIDE
   the press-physics partial, never per-file. Mono stays simple; the tier serves other themes and
   above all the generator (Dave: "mono doesn't really need this flexibility, but others might,
   and the generator will"). Groups accrete from OBSERVED duplication, not speculation
   (segmented-controls radius joins when observed). Every new gate ships with a selftest (ds-008's
   lesson).
4. **`gen_canon_components` joins `_build_all`** — regenerate-always + `--check`, the same contract
   as every other projector, so snippet RULE-text changes self-heal into canon. Closes Phase-1's
   silent-divergence finding.

## Consequences

- **Build session** (fresh, SERIAL, clean-room — the Phase-0 precedent; Fable solo): registry +
  partial generator + gates (+ selftests) + the §4 wiring + ds-008/ds-009 fixes + proof
  migrations **Button → Modals** (in-sync copy) **→ Progress-tracker** (drifted — Back/Next press
  visibly changes `translateY`→scale: Dave's eyeball owed) **→ Icon-button** (lock-step atom).
  **Exit gate:** change a factor once in Button and every consumer moves; no local recipe remains
  in the proofs; build green with the new gates blocking.
- **✅ BUILT 2026-07-22 (the clean-room ran end-to-end; build 45→51 green).** Registry
  `knowledge/component-types.json` (path-addressable token store + `$members`/`$partials`) ·
  `gen_component_partials.py` (injection + contracts + `--check`, selftest) · `_validate_partials.py`
  ratchet (0 strict / 32-rule census = the accretion worklist) · `gen_canon_components` wired
  regenerate-always + determinism `--check` · ds-008/ds-009 fixed (radius HTML-comment strip;
  consult corpus DISCOVERED by glob + zero-yield fails the build) · all four proofs migrated ·
  responsive-stepper collapse folded into Progress-tracker (dots resurrected from `273d18c~1`,
  grid-corrected 13px→12px/4px) · **exit gate passed BOTH halves** (value dial 2→6: four consumers
  moved, both modes; source rule-text probe: three consumers moved; clean reverts).
  **Amendment absorbed mid-build — B-D7 (Dave):** the first population's factors are NOT the lifted
  1.04/0.95 — the Icon-button size-scoped model became the family canon (`motion/press/travel` 2px
  pixel-true + `darken` 0.94, `scale(calc(1 ± travel/--phys-size))`), and **motion is a THEME DIAL**
  (Legacy + Supercharge override sets zero it; pure CSS, tunable later). Ledger: `_BUTTON-DECISIONS.md`
  B-D7. Dave's eyeball owed: Button/Modals calm down · Progress-tracker press + stepper · Legacy/SC
  movement-free.
- **Phase-2 fan-out inherits the mechanism:** new organisms declare membership + consume partials,
  never re-type sub-atoms.
- The queued responsive-stepper collapse (Tranche-1 canon dots, `273d18c~1`) folds into canon
  Progress-tracker when its migration runs.

## Addendum 2026-10-01 — ruling 4 is reversed by `s311-D3`; the reversal is enacted in phase 2, not today

**Status of this addendum:** RECORDED by #312 lane L1 (the schema lane, `s311-D4`). It records a ruling
already made; it enacts nothing. Ruling 4 above still describes the tree as it stands at this commit.

**The ruling (Dave, #311, Thu 2026-10-01 11:10 BST, by click on the proposal page
`notes/_PROPOSAL-311-apollo-for-other-libraries-2026-10-01-v1.html`, call 1 "The snippets' job", verbatim:
"Fixture, generated from the spec (the recommendation)"; comment: none; page note: "This cool, lets get it
done"; export saved at `notes/_lanes/311/DAVE-RULINGS-2026-10-01-1110-apollo-for-other-libraries.md`;
inscribed as `s311-D3` at `2fbc8184`).** The snippet becomes a FIXTURE generated from the spec, no longer
the source the compiler reads. Each `knowledge/snippets/*.reference.html` becomes the HTML+CSS emitter's
output for a documented example, rendered from the meta plus a `components/<slug>.css` and a
`behaviour/<slug>.js`, committed, viewed in the showroom, read unchanged by the ~35 gates that read snippets
today, and ruled on by Dave's eye. A round-trip gate (`_validate_roundtrip.py`) refuses any emitter whose
output does not match the committed snippet byte for byte.

**What it reverses here.** Ruling 4 ("`gen_canon_components` joins `_build_all` — regenerate-always +
`--check` … so snippet RULE-text changes self-heal into canon") rests on the premise that the snippet is
the source of truth and canon is projected from it. Under `s311-D3` the direction flips for every
component in a converted cohort: the META (with `s311-D4`'s four fields — `anatomy`, `states`, `emits`,
`bindings`) plus `components/<slug>.css` and `behaviour/<slug>.js` are the source; the snippet is their
generated output; `gen_canon_components` and `gen_theme_cascade` read the new sources. The same ruling
reverses the "snippets are the source of truth" docstrings in `knowledge/canon/gen_canon_components.py`
(lines 3–7) and `knowledge/gen_component_partials.py` (lines 9–11). Rulings 1–3 (sequence, generated
partials, the one registry) stand: the partials and the registry are inputs the emitter consumes, not a
mechanism the reversal removes.

**When it takes effect — cohort by cohort in phase 2, never all at once (`s311-D9`).** Phase 1 (now,
`s311-D4`) adds the four fields to `knowledge/components/meta.schema.json` and drafts them from the
snippets with a `$extracted` marker; it edits no snippet and changes no generator's output. Phase 2 moves
each cohort's CSS and script out of its snippets, re-feeds the compiler and regenerates the snippets as
fixtures behind the round-trip gate (byte-equal snippet, byte-equal `AUTO-COMPONENTS` block, the 35
snippet gates green on the generated files). The first cohort is the five M2 sampled — button, tabs,
table, date-picker, metric — plus ten interactive neighbours (Dave, #312, 12:51, `notes/_lanes/312/DAVE-RULINGS-2026-10-01-1251-wave-2-calls.md`; the list with meta ids is
at `notes/_lanes/312/L/COHORT-ONE.md`). Until a cohort has passed the round-trip gate, ruling 4 and both
docstrings remain TRUE for it, which is why neither docstring is edited today. Each phase-2 cohort commit
updates this addendum with the cohort's name and landing sha; when every cohort has converted, ruling 4 is
tombstoned in place and the docstrings rewritten, in that same commit.

**Related:** `s311-D3` (the reversal) · `s311-D4` (the spec lives in the meta) · `s311-D9` (order and
start) · ADR-0008 decision 3 (adapters — `s311-D7` makes the adapter an `adapters/<lib-id>.json` manifest)
· `notes/_lanes/311/M/M2-COMPILER-DEPENDENCIES.md` (the measurement the proposal rests on).
