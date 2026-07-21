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
- **Phase-2 fan-out inherits the mechanism:** new organisms declare membership + consume partials,
  never re-type sub-atoms.
- The queued responsive-stepper collapse (Tranche-1 canon dots, `273d18c~1`) folds into canon
  Progress-tracker when its migration runs.
