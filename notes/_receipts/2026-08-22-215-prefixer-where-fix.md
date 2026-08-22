# Receipt — #215: the absorb prefixer made specificity-neutral, and G2 built

**Date** 2026-08-22 · **Session** #215 · **Lane** Opus build sub, s204-D1 topology
**Ruling in force** Dave, #215: *"always real fixes never patches, they just get lost."*
**Deliverables** W-100 (prefixer cause fix) · W-101 (G2, the `--computed` render leg)

---

## 1 · The headline

`48 -> 0`. The 48 cascade-dead ds-005 descender overrides in `canon.css` are gone, and they are gone
because the two SCOPE CLASSES stopped contributing specificity — not because 48 override selectors
were rewritten. The shrink-only ratchet has been lowered to the measured `0`, which makes the
specificity leg effectively blocking from now on.

The route there had one turn nobody had priced, and it is the finding of the day:

| step | measured cascade-dead in canon.css |
|---|---|
| before anything (#214 allowance) | **48** |
| after `:where(.cn-<scope>)` in the absorb prefixer, ALONE | **49** ⟵ *went UP* |
| after `:where(.canon)` on the global leading-trim rule too | **0** |

**Two inflators were masking each other.** Fixing only the generated one moved every dead override
off the per-component trim and onto the hand-authored `.canon :is(…)` default, which had always been
the larger dominator and had never been visible while the component copy was even more specific.

---

## 2 · What changed

### 2.1 `knowledge/canon/gen_canon_components.py` — `prefix_selector()`

The absorb prefixer now emits `:where(.cn-<scope>)` where it emitted `.cn-<scope>`. Both branches
(the plain one and the leading-global-root-ancestor one) are wrapped; **nothing authored is ever
wrapped.** `:where(X) Y` matches exactly the elements `X Y` matches, so component containment is
byte-for-byte unchanged — only the specificity the scaffolding was silently lending goes away.

Why it mattered, from the file itself:

```
snippet trim  :is(…,input[type=text],…):not(:has(svg))                     (0,1,2)
canon   trim  .cn-x :is(…,.cn-x input[type=text],…):not(:has(svg))         (0,3,2)   +2 classes
snippet ovr   .sn .sn-label                                                (0,2,0)
canon   ovr   .cn-x .sn .sn-label                                          (0,3,0)   +1 class
```

The trim collected TWO because `sel.split(",")` splits inside `:is(…)` as well, so the prefix landed
on the `:is()` ARGUMENTS too. The trim gained one class more than the override did, so a ds-005
repair that WINS in the reviewed snippet LOST in canon. A ~30-line comment block above the function
records this and refuses a future revert by name.

### 2.2 `knowledge/canon/canon.css` — two hand-authored rules

Same principle, same cause, second site. `.canon` is a root MARKER — it says where the stylesheet
applies; it is not an authoring decision and must not decide which authored rule beats which.

* the global **leading-trim** rule: `.canon :is(button,a,label,…)` → `:where(.canon) :is(…)`.
  It was lifting a DEFAULT to `(0,2,2)`, above every two-class ds-005 override in the file. Now
  `(0,1,2)` — a base default any authored override can beat, which is what a default is for.
* the **heading margin reset**: `.canon :where(h1,h2,h3,h4,p){margin:0}` → `:where(.canon) :where(…)`.
  See §5 — this one is a regression *I* introduced and then measured out.

Both carry an inline `#215` comment explaining the reasoning and a ⛔ against unwrapping.

### 2.3 `knowledge/_validate_descender_clip.py`

* `SPECIFICITY_RATCHET["canon/canon.css"]`: **48 → 0**, with the measurement quoted beside it.
* The comment block above it rewritten: it used to say the repair was a 48-selector cross-file class
  remedy and therefore Dave's call. It was not; it was two scaffolding classes. That is now recorded.
* The at-allowance message no longer says *"NOT a pass: these labels clip today"* when the allowance
  is `0` — an honest verdict line at zero (`✓ SPECIFICITY RATCHET AT ZERO`).
* New `--computed` entry point that hands off to G2 (§4).

### 2.4 `knowledge/_validate_descender_computed.py` — NEW (G2)

See §4.

### 2.5 Regeneration

The full ordered serial was run, in order, twice (once after each canon.css edit) — never
`_build_all.py`:

```
gen_token_ramp.py         0 file(s) synced, 147 already in sync
gen_canon_components.py   generated 135 components -> .cn-<scope>   (2nd pass: no change, in sync)
gen_snippet_tokens.py     4730 manifest bindings, 135 snippets + 9 tranches, 0 projected
gen_theme_cascade.py      no change (in sync)
gen_showroom.py           135 page(s) + index (0 written, 0 orphan(s) pruned)
```

Determinism guards, both green:

```
gen_canon_components --check OK — 135 components in sync.
gen_showroom --check OK — 135 page(s) + index in sync.
```

---

## 3 · Driven BOTH WAYS on the real artefact

Two of the 48, on the real `canon.css`, through the gate's own resolver — with the `:where()`
wrappers reverted in memory as the mutation arm. Verbatim output:

```
FIXED (as committed):    0 cascade-dead override(s)
   :where(.cn-sidebar-nav) .sn .sn-label                   DEAD=False
   :where(.cn-transaction-row) .ldg-desc .ldg-ref          DEAD=False

REVERTED (mutation arm): 38 cascade-dead override(s)
   .cn-sidebar-nav .sn .sn-label                           DEAD=True
   .cn-transaction-row .ldg-desc .ldg-ref                  DEAD=True

DRIVEN BOTH WAYS: PASS
```

⚠ The reverted arm reports **38**, not 48: it reverts the wrappers on an already-regenerated file,
which is not byte-identical to the #214 state. **48 is the number measured on the pre-change file at
the top of this session** and is the one the ratchet moved from. The arm's job is the DIRECTION and
the two named cases, and both flip.

And the same two cases in the browser, not the resolver — from the G2 `--bite` runs (§4.3):

```
sidebar-nav · `.sn .sn-label` [0] 'text-box-edge': snippet computes 'text' but canon computes
  'cap alphabetic' (label 'Overview', heights 21 vs 11.56px)
transaction-row @480px · `.ldg-desc .ldg-ref` [4] 'text-box-edge': snippet computes 'text' but
  canon computes 'cap alphabetic' (label 'Brought forward from May', heights 0 vs 10.13px)
```

`21px` vs `11.56px` is the clip, in pixels, on a real label. With the fix in place both compute
`text` on both sides.

---

## 4 · G2 — the `--computed` render leg

`python3 knowledge/_validate_descender_clip.py --computed [--range A:B | --resume | --bite <slug>]`
(implemented in `knowledge/_validate_descender_computed.py`, 441 lines).

### 4.1 What it actually proves

Legs 1 and 2 of the descender gate are ARITHMETIC: leg 1 asks whether the override STRING exists,
leg 2 asks whether a resolver *written in that same file* thinks it wins. A resolver is a model of
the cascade, not the cascade. G2 loads real pages in headless Chromium and reads
`getComputedStyle` — Chromium's own cascade resolution — on the actual label elements the overrides
name, at **two viewports** (1180px and 480px).

Two pages per component, both `goto file://…`:

* **SNIPPET** — `knowledge/snippets/<Name>.reference.html`, the reviewed artefact, untouched.
* **CANON** — a harness staged in `TMPDIR`: `type.css` + `canon.css`, then the snippet's own
  `<body>` markup VERBATIM inside `<div class="canon"><div class="cn-<slug>">`. The markup is
  COPIED from the approved artefact, never re-drawn.

The work list is derived from `canon.css` itself, so a component that gains an override tomorrow
joins the run without anyone remembering to add it.

**The failing assertion is the COMPARISON**: canon must compute the same `text-box-edge` as the
reviewed snippet, same element, same width. That is precisely what the absorb prefixer is supposed
to preserve and precisely what it was breaking.

### 4.2 GREEN

```
font probe (canvas, 40px 'Handgloves 12345'): target=346.88 alias1=346.88 alias2=346.88
  control=375.39 missing=301.07 -> DISCRIMINATES

G2 PASS — 550 label-read(s) driven in Chromium across 25 component(s) at 1180px, 480px;
every ds-005 override computes in canon exactly what it computes in its reviewed snippet.
```

### 4.3 RED — driven twice, before the green was trusted

`--bite <slug>` stages a TEMP copy of `canon.css` with that slug's `:where()` wrappers reverted (the
repo copy is never touched) and requires the run to catch it.

```
--bite sidebar-nav
G2 --bite FAIL — 16 rendered mismatch(es) across 1 component(s)
✓ MUTATION ARM PASS — the reverted scope was CAUGHT in the rendered cascade (16 mismatch(es)).
  G2 can fail, so its green means something.

--bite transaction-row
G2 --bite FAIL — 32 rendered mismatch(es) across 1 component(s), 32 label-read(s) driven at 1180px, 480px
✓ MUTATION ARM PASS — the reverted scope was CAUGHT in the rendered cascade (32 mismatch(es)).
```

### 4.4 Two things driving the REAL files taught G2 (both fold into it as code + comment)

* **`text-box-trim` legitimately differs between the two sides.** `File-upload.reference.html`
  carries no leading-trim rule of its own, so it computes `none`, while canon's global
  `.canon :is(…)` trims the same label. Edge is `text` on both sides — descender-safe, no defect.
  G2's first cut FAILED on this. A gate reporting a difference it has no rule against is a gate that
  will be waived. Now a NOTE.
* **"canon is trimmed AND computes `cap alphabetic`" is not a sound failure either.** Several ds-005
  overrides live inside an `@media`/`@container` arm (`App-shell-nav-rail`'s `.sh-rail .sn-label`),
  so at a width where that arm is out of force the label computes `cap alphabetic` on BOTH sides, by
  design — and several of those are the sr-only clip-path form with nothing visible to clip. G2's
  second cut FAILED on 10 of these. Now a NOTE, and answered properly by driving two viewports
  instead of one.

Both were only visible because G2 was driven on the real tree rather than a fixture.

### 4.5 Sandbox rules obeyed (each has burned a prior session)

`set_content()` never used — always `goto file://`. `document.fonts.check()` never used — the canvas
probe with two controls is the precondition, and it DISCRIMINATED (target 346.88 ≠ missing 301.07 ≠
control 375.39, matching the runbook's ~347 table). Transitions settled by an injected
`*{transition:none;animation:none}` present in the document BEFORE the first read. `--range`/
`--resume` chunking with a JSON bank in `TMPDIR`. Scratch in `/var/tmp`. Font symlink FARM, not a
repo `<dir>`: `ls -a knowledge/assets/fonts/_desktop/TTF/ | grep -c '^\.uuid'` → **0**, and
`git status --untracked-files=all` shows no stray.

---

## 5 · CONSEQUENCES / PITFALLS

**1 · A cause fix can move a defect rather than remove it, and the count can go UP.**
`:where()` on the prefixer alone: 48 → 49. Had the run stopped at "I fixed the prefixer, re-run the
gate", it would have reported a REGRESSION and looked like the fix was wrong. Two inflators were
masking each other. ⇒ *When a specificity fix moves the count the wrong way, read WHICH RULE the
survivors now lose to — the binding competitor changes.*

**2 · Lowering a scope class's specificity is not free — it can hand rules to a base reset.**
Making the component scope zero-specificity dropped every generated rule by one class. A sweep of
all 8,439 AUTO rules against all 70 hand-authored rules earlier in the file for shared properties
found **one real flip class: 43 `:where(.cn-x) h1..h4/p{margin:…}` rules now losing to
`.canon :where(h1,h2,h3,h4,p){margin:0}`** — i.e. component heading margins would have silently
collapsed to zero across the showroom. Fixed at the same cause (`:where(.canon)` on the reset) and
re-swept: **0 flip classes remaining.** ⇒ *Any change to a scope's specificity needs a whole-file
flip sweep, not just the gate that motivated it. The gate you are fixing only watches its own
property.*

**3 · The comma-shred in `prefix_selector` is STILL THERE and is a MATCHING defect, not just a
specificity one — see OPEN-TO-DAVE below.** `:where()` neutralised its specificity cost but not its
semantics.

**4 · Two ratchets look similar and only one moved.** `_validate_type_composites.py` still reports
**1,097** — unchanged, pre-existing, not this lane's. It is a red on the default run and always was.

**5 · A comparison gate must be scoped to what the rule actually forbids.** G2 failed twice on
correct CSS before its assertion was right (§4.4). A gate that fails on legitimate difference gets
waived, and a waived gate is worse than no gate.

**6 · The G2 harness renders the snippet's `<body>` with scripts stripped.** State-only elements a
demo script would instantiate are never driven; they are listed by name in the run output as
*"not instantiated in static markup, not driven"*. Declared, not hidden.

**7 · G2 needs a staged browser, so it is a SEPARATE invocation and is deliberately NOT wired into
the default build-mode run.** A gate that cannot pass in one environment must not sit where it will
be silently skipped. An undriveable environment makes G2 REFUSE loudly; it never returns a pass.

**8 · UNPROVEN BY SCOPE, DECLARED.** G2 drives light mode only, at 1180px and 480px, with demo
scripts stripped. Dark mode, the other three Apollo themes, other breakpoints, and script-driven
states are UNDRIVEN. No PNG was read this lane — the assertion is numeric.

---

## 6 · OPEN TO DAVE

**OPEN-TO-DAVE #215-a — the absorb prefixer still shreds `:is()` argument lists, and that is a
MATCHING bug, not a specificity one.** `prefix_selector` splits on EVERY comma, including commas
inside `:is(…)`, so the snippet's

```
:is(button, a, label, span, …, input[type=text], …):not(:has(svg))
```

becomes, in canon,

```
:where(.cn-x) :is(button, :where(.cn-x) a, :where(.cn-x) label, …)
```

Every argument after the first now requires a `.cn-x` ancestor *inside* `.cn-x`, which never exists.
**So the per-component leading-trim rule only ever matched `button`** — every other element in that
`:is()` list has been unreachable in canon since the prefixer was written. Today's fix makes it
specificity-harmless; it does not make it correct.

Fixing it (splitting only at nesting depth 0) would make those trim rules start matching elements
they have never matched, which CHANGES RENDERING across 135 components. That is a visual change on
gated canon and it is not mechanically derivable from anything ruled. **Not done. Dave's call.**

Note the mitigation: the global `:where(.canon) :is(…)` rule already applies the trim correctly at
document level, so the practical effect is duplication, not absence — but that is an argument, not a
measurement, and it has not been render-proven either way.

**OPEN-TO-DAVE #215-b — `:where(.canon)` on two hand-authored rules is a change to gated canon
outside the AUTO markers.** It is the same cause as the generator fix, it is matching-identical, and
without it the count does not move. Flagged for ratification rather than assumed.

---

## 7 · Files touched

| path | change |
|---|---|
| `knowledge/canon/gen_canon_components.py` | `prefix_selector` emits `:where(.cn-<scope>)`; ~30-line cause comment |
| `knowledge/canon/canon.css` | `:where(.canon)` on the leading-trim rule + the heading-margin reset; regenerated AUTO-COMPONENTS |
| `knowledge/_validate_descender_clip.py` | ratchet 48 → 0; comment block rewritten; honest zero verdict; `--computed` entry |
| `knowledge/_validate_descender_computed.py` | NEW — G2 |
| `notes/_receipts/2026-08-22-215-prefixer-where-fix.md` | this receipt |
| `knowledge/_state.json` | rows W-100, W-101 |

Not committed — the tree is left dirty for the conductor.

---

## CORRECTION — ADDED #215, same session, BY ADDITION (the claim above stands as written history)

⛔ **OPEN-TO-DAVE item 1 ("the :is() split is a MATCHING bug — the leading-trim rule has only
ever matched `button`") is DISPROVEN BY DRIVING, and is WITHDRAWN.** Computed-style probe in
headless Chromium against the REAL canon, `.cn-button` wrapper holding `button` + `a` + `span`,
BOTH eras — today's `:where()` file and the pre-#215 form from `161db61`:
`text-box-trim` = `trim-both` on ALL THREE elements, in BOTH files. The reasoning error:
`:is(button, .cn-x a)` under an outer `.cn-x` scope does not demand a SECOND `.cn-x` ancestor —
the same ancestor satisfies both. Redundant, not broken. What remains is COSMETIC: argument
bloat, plus a theoretical edge if an `:is()` argument ever starts with `html`/`:root` (none do
today). No rendering change exists for Dave to rule on; the tidy-up is an ordinary low row.
Probe artefacts: /var/tmp/isbug.html · isbug-old.html (session-scratch, not homed — the method
is restated here in full so the probe re-derives).
