# BRIEF — s175 · progress bars go to ink in all four themes

**Session #175 · 2026-08-14 · ONE OPUS SUB · conductor's window binds (FILL ~108K of a 150,929 stop line)**

⚠ **STEP 0 — VERIFY THE PREMISES BELOW BEFORE ACTING.** Every factual claim in this brief was
measured by the conductor at #175 open, but a premise ages faster than a rule. Re-verify HEAD,
the token values, and the snippet bindings first-hand. If a premise is stale, **say so and stop** —
do not repair the brief by inference.

Premises as measured: HEAD = `76b024c`, tree clean apart from `notes/_REHEARSAL-LOG.jsonl` and
`notes/_FLOAT-174-dave-ink-clarification.md` (untracked).

---

## 1. THE RULING YOU ARE ENACTING (Dave, live, #175)

Dave ruled, on a plain-prose read-back, in three exchanges:

> "Just use the default ink colours (blackest) for all the progress bars, all themes, no red."
> "specifically for progress bars we don't use colours in all four themes. the other ruling was a
> miscommunication. the only type of progress indicator that may use colour is the step tracker component"
> "This is two components that are treated separately but the designer can choose to have the desktop
> version, with circles, collapse into bar type as a responsive behavior. so there are three patterns.
> these will have colours in legacy for sure. Its undecided for teh other themes as yet."

**The rule is semantic, not visual — it turns on what is being measured, not what it looks like:**

| Pattern | Component(s) | Colour rule |
|---|---|---|
| Continuous quantity | `Progress-bar` | **INK ONLY, all four themes. RULED.** |
| Discrete steps, circles | `Progress-tracker`, `Stepper` | Colour **permitted**. Legacy **definite**. Mono/Console/Supercharge **UNDECIDED**. |
| Discrete steps, collapsed to a bar | same two, `@container (max-width:520px)` | Same as above — it is the same component in a responsive state. |

★ **Patterns 1 and 3 are the same SHAPE with opposite colour rules.** That is intended and Dave was
told. Do not "harmonise" them.

⛔ **"Permitted" is not "required".** The step components must come out of this build **visually
identical to how they go in, in every theme**. You are preserving their present values, not choosing
new ones. The three undecided themes stay parked.

---

## 2. THE CHANGE — EXACTLY THIS, NOTHING MORE

Measured present state of `progress/complete`:

- `knowledge/tokens/semantic-colour.json` → base: light `#1A1A1A`, dark `#FFFFFF`
  (`$alias` light `color/neutral/4`, dark `color/neutral/15`)
- `knowledge/tokens/themes/apollo-legacy.overrides.json:106` → `#DB0011` / `#DB0011`
- `knowledge/tokens/themes/apollo-supercharge.overrides.json:7` → `#B92F1E` / `#CC4333`
- `apollo-console.overrides.json` → no override (inherits base ink)

Three snippets bind it: `Progress-bar`, `Progress-tracker`, `Stepper`.

**Do:**

1. **Mint `step/complete`** in `semantic-colour.json`. Name is **DAVE'S, RATIFIED** — use exactly
   `step/complete`, do not improve it. Base values = the current `progress/complete` base
   (`#1A1A1A` / `#FFFFFF`, same aliases). Carry a `$note` recording: minted #175 by `s175-D1`;
   colour permitted for step indicators; Legacy definite; **Mono/Console/Supercharge UNDECIDED —
   present values are INHERITED, NOT RULED.**
2. **Move, do not copy, the two theme overrides** from `progress/complete` to `step/complete`:
   Legacy `#DB0011`/`#DB0011`, Supercharge `#B92F1E`/`#CC4333`. Preserve their `$note` provenance
   text and **append** the #175 supersession — never overwrite a ratified note
   (add, never trim).
3. **Delete** the now-empty `progress/complete` overrides from both theme files, so
   `progress/complete` resolves to the ink pair in all four themes.
4. **Rebind** `Progress-tracker.reference.html` and `Stepper.reference.html` so their `--complete`
   maps to `step/complete`. Their hardcoded per-theme block values must be updated to match what the
   token now resolves to — **which for them is unchanged in every theme.**
   `Progress-bar.reference.html` stays on `progress/complete` and is **not edited**.
5. Update the `$note` on `progress/complete` — the existing one quotes Dave's 2026-07-21 ruling
   *"in mono and console it should be black. the colours in legacy and supercharge are fine."*
   ⛔ **Do not delete that text.** Append: superseded #175, Dave's own words —
   *"the other ruling was a miscommunication."*

**NET RENDERED CHANGE, and this is the acceptance test:** `Progress-bar` only, Legacy and
Supercharge only, red → ink. **Every other component in every theme renders byte-identically.**

---

## 3. ⛔ GENERATOR FENCING — READ THIS TWICE

**This is the exact failure that defined #174.** Regenerating `canon.css` for a token change also ran
the theme-cascade generator, which stripped 25 unrelated `--status-*` declarations and deleted a
hand-written comment block — both of them deferred, Dave-owned items sitting on a do-not-rule list.
**A do-not-rule list names DECISIONS; it cannot fence a GENERATOR'S BLAST RADIUS.**

So, before you run any generator:

1. **Name which regions of `canon.css` each generator owns.** At least three do:
   `gen_theme_cascade.py`, `gen_canon_tokens.py`, `gen_canon_components.py`. Establish the region
   boundaries by reading the generators, not by guessing from marker comments.
2. **Snapshot `canon.css` at HEAD before you touch it.**
3. After regenerating, **diff it and account for EVERY HUNK BY NAME.** A hunk you cannot attribute to
   this token change is a finding — **report it, do not absorb it.**
4. If a generator moves something outside the regions this change owns, **stop and report.** Do not
   revert it silently either; the #174 lesson is that both smoothing and stripping hide the same thing.

⛔ **DO NOT RUN `knowledge/_build_all.py`.** A partial run strands the tree in a documented mid-build
intermediate, and a full single-process run exceeds the sandbox call cap (~49s vs ~45s). CI delivers
that verdict on push.

---

## 4. GATES — THE RUNBOOK OMITS HALF OF THESE, SO THEY ARE LISTED HERE

`knowledge/_RUNBOOK-gated-component.md` is 54 lines and does not list the icon gate, the type-composite
ratchet, the radius `MIGRATED_SNIPPETS` step, or the registry step. Run all of:

- snippet gate · a11y gate · radius (`_validate_radius.py`, strict) · coverage · icon gate
- type-composites ratchet — **shrink-only, debt 1101 may only go down**
- `--check` on: showroom · snippet-tokens · canon-components · component-partials · theme-cascade

⚠ **Baseline every gate at HEAD before your change.** Two of these were already red at HEAD at #174
and a naive read scored them as regressions. **`rc=$?` after a pipe reads the PIPE's status** — this
has produced a false green baseline before. Capture rc directly.

⚠ `_validate_state_contrast.py` over the full 76-snippet population **exceeds the ~178s call cap**.
Filter to the three affected snippets. If you run a filtered pass, it **overwrites the tracked
`knowledge/_STATE-CONTRAST-AUDIT.md`** — restore it byte-identical and say that you did.

---

## 5. RENDER PROOF

All three components × 4 themes × light/dark. **`goto("file://…")`, never `set_content()`** — it drops
`type.css` silently and `document.fonts.check` passes anyway. Assert the font by **canvas measurement
against two controls**, not `fonts.check()`.

Confirm by measured colour, not by eye:
- `Progress-bar` fill is the ink pair in **all four** themes.
- `Progress-tracker` and `Stepper` are **unchanged from HEAD in all four themes** — this is the
  important one; render HEAD as the control and compare.

★ **Expected side-effect, verify it:** the fill-on-track contrast failure on `Progress-bar`
(Legacy dark 1.75:1, Supercharge dark 2.38:1) should now clear 3:1 comfortably. **Measure it, don't
assume it.** Note that the same failing pair persists on the step components in Legacy — that is
correct and stays open, it is not yours to fix.

⚠ Render sandbox is fresh every session (~4 calls). `LD_LIBRARY_PATH` chromelibs —
see `_RUNBOOK-render-verify.md`. Nothing survives a tool-call boundary. Builds over ~45s wall must be
chunked.

---

## 6. ⛔ DO NOT RULE — each of these is Dave's or another lane's

- **The three undecided themes for step colour** (Mono, Console, Supercharge). Preserve, never choose.
- **The two-red law `s151-D1`** and **the mono error ink camp `s149-D1`** — both FIRM, both
  eye-approved. This change does not touch RAG and must not reach it.
- The `--status-*` strip and the `#168` comment block (`[45]`, `[50]`) — committed at `76b024c`,
  declared, **not adjudicated**.
- The fill-on-track contrast finding as it applies to the **step** components.
- `tooltip.tip` · base red 30 · priority/deadline/effort values · the 19 unconditioned items ·
  the G-series · the palette reshape · the rung name `-graphic` · the `progress-family` proposal ·
  the two stale inventory documents · the CI sweep blocking flip · the two `_governs.py` anchor repoints.
- `knowledge/_build_all.py` — **its `#166` label strings are JOIN KEYS. Do not edit, even cosmetically.**
- ⛔ **`knowledge/_rulings.json` — DO NOT TOUCH.** Inscription is the wrap's, by textual tail
  insertion. You are enacting, not recording.
- ⛔ **Build NO new instrument** — no gate, checker or harness. `s172-D3` binds: a new instrument needs
  an OBSERVED failure, and the appetite covers future briefs only. If you find one wanting, **queue it
  with a price and a named failure class.** The four-theme contrast checker is already queued and
  deliberately unbuilt; do not build it.

---

## 7. PITFALLS, REPLAYED

- **A token NAME is not an ADDRESS.** `progress/incomplete` has no override in any theme yet resolves
  differently in Supercharge, because its `$alias` targets `color/neutral/13` and Supercharge rebinds
  the neutral ramp warm. Nothing warns you. Resolve values per theme; never reason from the name.
- **The snippet gate is single-theme by construction** — `resolve()` reads only `semantic-colour.json`
  (the Mono base) and cannot see the Legacy/Supercharge legs. **Any four-theme claim must be computed
  by hand, outside the gate.** A single-theme green is not a green.
- **The icon gate fails SVG-based components silently** — `<circle>`-only shapes read as "shape-only
  icons"; the remedy `data-bespoke="why"` is in the gate's docstring, not the runbook. The step
  components use circles.
- **The default snippet shape trips the type ratchet** — the boilerplate `body{font-family:var(--font)}`
  is itself a TYPE-002 violation.
- **Serializer defaults reformat JSON.** These are hand-maintained token files. **Round-trip
  byte-identical before writing, and prefer textual insertion.** A reformatted `semantic-colour.json`
  is an unreviewable diff and will be rejected.
- **`rm`/`rmdir`/`unlink` may be denied on the repo mount.** `git checkout -- <file>` then fails;
  truncate-in-place (`cat HEAD-version > file`) is the working substitute. Ask before assuming you
  cannot do something — **grep the runbooks first.**
- **A crash is not a fail.** Parse helpers must fail loud and named. Declare any residual.

---

## 8. REPORT BACK — structure it exactly like this

1. **PREMISES** — which of §0's held, which were stale, first-hand.
2. **THE DIFF, HUNK BY HUNK** — every changed region of `canon.css` attributed by name to a generator
   and to this change. **Explicitly state whether anything moved that this change does not own.**
3. **GATES** — baseline rc at HEAD and rc after, per gate, rc captured directly not through a pipe.
4. **RENDER** — measured colours, 3 components × 4 themes × 2 modes, against a HEAD control.
   The contrast numbers before and after.
5. **WHAT YOU COULD NOT DO** — declared, priced, never smoothed. An honest UNPROVEN is a priced TODO;
   a CLAIMED lies.
6. **FRICTION LOG** — anything the runbook got wrong or omitted. This is a real deliverable; #174's
   friction log is why this brief exists.
7. **`machinery: N instrument / N feature`** — line count split.
8. **ANYTHING YOU DECLINED TO RULE** that you think Dave should see.

⚠ Do not commit. Do not push. The conductor wraps.
