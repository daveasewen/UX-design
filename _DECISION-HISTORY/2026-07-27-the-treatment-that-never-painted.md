# The treatment that never painted — ds-018 confirmed as instance five, and the proof that would have been green forever

provenance: apollo-sds-2026-07-27-8 · 2026-07-27
status: observed

*Session #8, Monday 2026-07-27, Opus 5 solo self-conducting, effort MAX. The window opened to
discharge one owed render-proof and diagnose one logged defect in a single harness spin-up. It
discharged neither: the diagnosis landed conclusively, and the proof turned out to be unattainable
as written. Nothing was built, by Dave's ruling at the fork. Spine entry: `_LIVE-STATE.md` ⏱ LATEST
2026-07-27 #8 · defects: `knowledge/_DS-IMPROVEMENTS.md` **ds-018 CONFIRMED** + **ds-019 NEW**.*

---

## 1 · What the window was for, and why the pairing was right

Session #7 left DV-D17 enacted and DOM-proven — 108/108 on the members suite, 27/27 on the donut
exemplar, three neutered controls each going red on the right checks — with the render in the licensed
cut deliberately owed. In the same handoff sat ds-018: Dave had reported by eye that the legend's
disabled `Reset` renders at its hover treatment. Both live on the same component, the same page, the
same two widths. Doing them separately pays the harness cost twice for nothing, so the handoff paired
them, and that judgement held: the harness came up once and answered both questions.

It is worth recording that the runbook worked verbatim again, from a cold sandbox. pip to the shared
mount → TLS env → `chromium-headless-shell` (the installer's non-zero exit after a successful download
is the expected host-validation failure, and the cache was there) → eleven libs via `apt-get download`
→ fonts with the two-alias fontconfig → render. No new steps, no re-diagnosis. The one thing worth
folding back is small: `PLAYWRIGHT_BROWSERS_PATH` pointed at the outputs mount now throws
`EPERM: operation not permitted, rmdir '__dirlock'` at the end of the install. It is the same species
as the host-validation exit — **a failure message that follows a success** — and the correct read is
the same: check the cache, proceed.

## 2 · ds-018: the hypothesis was right, and the reason it was right is stronger than the measurement

The ds-018 entry did something valuable: it stated a hypothesis **as** a hypothesis, named the competing
explanation, and forbade choosing between them by reading CSS. Two causes could produce an ink border on
a disabled control — the token resolving to an ink-ish value (a token-value bug), or the token failing to
resolve at all (invalid at computed-value time → `currentColor` → ink, a lookup bug). They look identical
on screen and have completely different fixes.

`getComputedStyle` on the disabled Reset, four contexts, font assert passed in each:

```
--border-disabled   →  ""                ← does not resolve
--text-disabled     →  ""                ← does not resolve
--ink               →  #1A1A1A           ← resolves; the context is not broken
border-color        →  rgb(26, 26, 26)   ← currentColor = ink = the hover value
color               →  rgb(26, 26, 26)
```

The lookup cause is confirmed and the token-value cause is eliminated. But the source census is what
makes it conclusive rather than merely measured: `--border-disabled` is declared **29 times in
`canon.css`, on ten form-component scopes and their theme twins, and on no chart scope and no `:root`**.
The four chart snippets that consume it declare it zero times. **It is a form-tier token being read from
a dataviz-tier scope.** It has never resolved on a chart, in any theme, at any width, since the rule
landed — and every gate was green the whole time.

Two things follow that the original entry could not have known. First, `--text-disabled` fails in the
same breath; it is masked because `color` is an inherited property, so the failure lands on ink, which
*reads* plausible. A fix aimed only at `border-color` would leave a second silent lookup in place.
Second, the gate candidate the entry proposed — *no control's disabled treatment may resolve to its
hover treatment* — is correct but downstream. The cheaper, wider gate is **fail loud when a declaration
references a custom property that resolves nowhere in its own scope**, which is the same
*fail-loud-on-unknown* shape already ratified for `dv-vocab` and proposed for ds-016.

This is **instance five** of the silent-lookup class, as predicted: ds-010, ds-013, the black chart
keys, ds-016, and now this. The prediction being right is not the interesting part. The interesting
part is that the entry was written to make being right *checkable*, and that is what let a hypothesis
become a finding in one measurement instead of an argument.

## 3 · The finding nobody was looking for: a rule that matches and does not paint

DV-D17's acceptance test, as the handoff specified it, was: after isolate-then-check-on, confirm no
`.dv-legrow` resolves the `.is-solo` treatment — ink border plus a 6% ink fill. The probe ran the
gesture chain (dim a spare first, so `visible[]` is not all-on; isolate row 0; check a blank swatch to
release) and asserted exactly that.

It passed. It also could not have failed.

Applying `.is-solo` directly, with no behaviour code involved at all:

```
element matches '.dv-legrow.is-solo'  →  TRUE
  declaring: border-color: var(--ink); background: color-mix(in srgb, var(--ink) 6%, transparent)
--ink  on the row →  #1A1A1A        --line on the row →  #E1E1E1
computed border-color →  rgb(225, 225, 225)   ← --line. The declaration did not win.
computed background   →  oklab(0 0 0 / 0)     ← fully transparent, not 6% ink
CONTROL: the same mix, literal, on a sibling div in the same subtree
                      →  color(srgb 0.101961 0.101961 0.101961 / 0.06)   ← the mix is fine
```

The selector matches. The variables resolve. The colour function is valid three inches away in the same
subtree. And **both declarations are overridden**. The rule census run against the element enumerated
only selectors whose text contains `dv-legrow` — four, none of which can beat `.dv-legrow.is-solo` at
(0,2,0) — so **whatever wins does not contain that string**. A `:is()`/`:where()` list, a descendant
selector through `.dv-leg > li` or `#cb4-legend li`, an `!important`, an inline or animated value: all
plausible, none checked. Naming it is the next step and it should not be guessed.

The consequence is the reason this stopped the window. **The isolate treatment has never been visible**,
so the assertion DV-D17 owed is permanently true for reasons that have nothing to do with DV-D17, and
would have stayed true through a complete revert of the fix. A green run of that probe means nothing.
DV-D17 stays **enacted, DOM-proven, render-owed** — the render cannot be discharged until the thing it
is supposed to observe actually paints.

There is a second-order question here that is Dave's, not the agent's: if the treatment has never
painted, the screenshot that produced DV-D17 showed *something*, and it is worth knowing what. Either
the symptom came from a context not yet probed, or the treatment worked once and regressed silently.
Logged, not chased.

## 4 · The probe's own false green, which is the transferable part

The first run printed **24 checks · 0 failures**.

That was wrong, and it was wrong in the direction that reads as done. The probe carried a positive
control precisely to stop a vacuous pass: after isolating, the solo row's computed paint must *differ*
from its baseline, or the probe is blind and every later assertion is empty. The control compared the
computed strings. The solo background serialises as `oklab(0 0 0 / 0)`; the baseline serialises as
`rgba(0, 0, 0, 0)`. **Textually different. Visually identical — both are fully transparent.** The
control saw a difference, reported a difference, and passed.

It was caught by eye, reading the JSON dump, because `border: rgb(225,225,225)` on a row that was
supposed to be showing an ink border did not look right. Not by the check. The check was satisfied.

Two lessons, and the second is the uncomfortable one.

**Comparing computed colours requires comparing them as colours** — parse to r/g/b/a and compare
numerically — never as strings. CSS serialisation is not canonical across colour functions, and any
control that can pass on a serialisation difference is not a control.

And: this happened *inside the probe written specifically to honour* the standing rule that says
**assume your probe is wrong in the direction that reads as green**. The rule was known, quoted in the
file's own docstring, and designed for. It still did not prevent the failure it names, because the
failure arrived one level below where the rule was being applied — the control was checked for
existence, not for sensitivity. That is the same shape as session #7's finding that a conformance suite
goes stale like prose, and the same shape as ds-018 and ds-019 themselves: **the instrument was
present, correct-looking, and not measuring what it claimed.** Five sessions running, the bite-the-bite
discipline has caught a real defect; this session it caught one in itself.

## 5 · The fork, and why it went to Dave

At the finding the throttle fired as designed: an unplanned discovery, stop, re-price, put the fork to
Dave rather than decide it from inside the sunk cost. Fill was ~48%. Naming the overriding rule was
priced at ~8% — landing ~61%, over the band and into the ring-fenced reserve. Fixing it was unbounded
from there, with the added constraint that `dv-legend.js` has 54 bytes of headroom and the dataviz
group page budget is at 90%, so anything touching behaviour hits the ADR-0015 gate.

Dave chose **log and stop**. The reasoning that supports it is the perishable-allowance logic ruled in
session #5: behind pace, more windows beat longer ones, and a new window is a refill rather than a
penalty. The cold-read fee is real but bounded; pushing a poorly-understood defect into Red is not.

What the window bought, therefore, is not code. It is that **two defects moved from hypothesis to
measurement**, one of them previously unknown, and that **a proof which would have certified the wrong
thing was stopped before it certified it**. That is a reasonable trade for a window, and it is only
visible as a trade if the pricing is written down, which is why it is.

## 6 · Resolved / still open

**Resolved.** ds-018's cause is named, measured in four contexts, and its competing explanation is
eliminated; the fix belongs in the generator plus a gate, and is scoped wider than the reported symptom
because `--text-disabled` fails alongside `--border-disabled`. The render harness is proven working
again from cold, with one new pothole banked.

**Open.** ds-019's overriding rule is unnamed — that is the single next step, and it is cheap and
bounded. DV-D17's render-proof stays owed and must not be marked discharged on the current probe.
Neither gate is built. Whether the DV-D17 screenshot came from an unprobed context or a silent
regression is unanswered and belongs to Dave. Everything carried in from #7 — the per-member behaviour
opt-in schema question, ds-016, the `CTRL` sweep, call (4), ds-012, DV-D16/D18, the fifteen-item ruling
batch — is untouched.
