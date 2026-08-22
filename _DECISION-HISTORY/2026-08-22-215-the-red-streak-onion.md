# #215 — the desk cleared, and the red streak peeled at cause

```
provenance: 215 · 2026-08-22
status: observed
```

*Narrative dossier (ritual step 1b). The WHAT lives in `knowledge/_rulings.json` §
`s215-D1`…`s215-D5`, the receipts, and `GOOD-MORNING.md`'s ★ LATEST banner. This file holds the
WHY and HOW — the arc, the dead ends, the corrections. Both-way links: spine entry =
`_LIVE-STATE.md` ⏱ LATEST DELTA #215; ledger = `knowledge/_rulings.json` § `s215-D1`…`s215-D5`.*

*Written by the delegated Opus wrap sub from the conductor's brief
(`notes/_briefs/2026-08-22-215-wrap-brief.md`), the receipts, the store and `git log` — never
from the chat transcript, which this seat cannot read.*

---

## 1 · The shape of the day: a desk-clearing, then an onion

The session opened as a decision sitting and became a repair session. Five rulings landed in the
first two hours — the forced ID widening, the itinerary adoption, `P8`, the level ladder, the
five findability decisions — and each one turned immediately into an enactment commit rather than
a queued row. That is the part worth recording: **`s215-D1` was ruled and `ID_RE` was widened in
the same commit; `s215-D3` was ruled and `MODEL-ROUTING.md` was amended in the same commit.** The
#213 lesson — *"a ruling can sit unbuilt for a session and still be cheap to enact; what it costs
is the declaration every wrap in between"* — was applied the session after it was written.

What made the rest of the day is that CI had been red for twenty consecutive runs, and the reds
were not one defect. They were a stack, each hidden behind the one above it:

| layer | what it actually was | where it was fixed |
|---|---|---|
| `[45]` | canon determinism | `997e40c` |
| gates | three scripts with no help gate (#158 write-by-default class) | `997e40c` · `2a61618` · `4108f16` |
| index | stale `_memento-index.json` | `1b08f68` |
| radius / wiring / forks | `W-90` radius unbound, a wiring exemption unnamed, two undeclared forks | `6a9be36` |
| `ds-018` | a dangling var, the last one standing | `e645df2` |

**No layer could be seen until the one above it was gone.** That is the general form of a red
streak and it is why "fix the top red and re-run" is not a slower version of the right method —
it *is* the right method, provided each fix is at cause. Every one of the five carries its
receipt in its own commit message, which was Dave's instruction of the day, given in chat and now
a standing memory hook: **"always real fixes never patches, they just get lost."**

CI **#413 GREEN on `e645df2`** is the first green in twenty runs. ⚠ That verdict is the
conductor's read-back, quoted from his brief; the wrap seat cannot reach CI and does not claim to
have seen it.

---

## 2 · The finding of the day: two inflators masking each other

`W-100` was briefed as a simple cause-fix. The `canon.css` absorb prefixer emits a scope class,
and `#214` had measured **48 cascade-dead `ds-005` descender overrides** — repairs that win in a
reviewed snippet and lose in canon, because the prefixer is not specificity-preserving. The fix is
one character-class change: emit `:where(.cn-<scope>)` instead of `.cn-<scope>`, so the
scaffolding stops lending specificity while matching exactly the same elements.

It was run, and the count went **UP**:

| step | measured cascade-dead in `canon.css` |
|---|---|
| before anything (#214's allowance) | **48** |
| after `:where(.cn-<scope>)` in the prefixer, ALONE | **49** — *up* |
| after `:where(.canon)` on the global leading-trim rule too | **0** |

The reading is not "the fix failed". It is that **there were two dominators, and the larger one
had never been visible** because the per-component copy was even more specific than it. Removing
the smaller one moved every dead override onto the hand-authored `.canon :is(…)` default, which
had been sitting under it the whole time.

★ **The lesson is about measurement discipline, not about CSS.** A half-fix that moves a metric
the wrong way is the metric doing its job. Had the sub stopped at 48 → 49 and reverted, or
stopped at "the fix is right, the number is noise", the artefact would have shipped worse with
every gate green. **Two dominators can hide each other, and only re-measuring after each
individual change separates them.**

The ratchet was then lowered from 48 to the measured **0**, which makes the specificity leg
effectively blocking from here on — a shrink-only ratchet at zero cannot silently re-admit the
class.

Beside it, **G2 was built**: the `--computed` render leg of the descender gate, `getComputedStyle`
in headless Chromium. `#214` had priced it and named it as the only instrument that would prove
the FEATURE rather than the clause. It is now built — and its scope is declared narrow (light
mode, two widths; dark, the other three themes and the script states are undriven), because a leg
that proves one arm and is described as proving the gate is the same defect one level up.

---

## 3 · A receipt caught false, by driving, before it calcified

The prefixer receipt shipped with an open-to-Dave item asserting that the `:is()` split was a
**matching bug** — that the leading-trim rule had only ever matched `button`, and that `a` and
`span` inside a component had silently never been trimmed. If true, that is a real rendering
defect across the library and a genuine question for Dave.

It was driven instead of believed. A computed-style probe in headless Chromium against the real
canon, a `.cn-button` wrapper holding `button` + `a` + `span`, run against **both eras** — today's
`:where()` file and the pre-#215 form recovered at `161db61`:

> `text-box-trim` = `trim-both` on **all three elements**, in **both files**.

The reasoning error is small and instructive: `:is(button, .cn-x a)` sitting under an outer
`.cn-x` scope does not demand a *second* `.cn-x` ancestor — the same ancestor satisfies both arms.
**Redundant, not broken.** What is left is cosmetic argument bloat plus a theoretical edge if an
`:is()` argument ever began with `html` or `:root`, which none does today. There is no rendering
change for Dave to rule on, and the tidy-up dropped from an open question to a low row.

The correction was appended **by addition**: the original claim stands as written history, with
the retraction beneath it and its method restated in full so the probe re-derives without the
scratch artefacts. A correction that overwrites the claim it corrects destroys the only evidence
that the claim was ever made.

---

## 4 · The library stopped being a review page and became the door

`s215-D4` and `s215-D5` are two rulings that read as taxonomy and are really about findability.
`#214`'s research had found the industry consensus is Foundations / Tokens / Components / Patterns
— **not** atomic-as-navigation — and that aliases, facets and search beat taxonomy for actually
finding a component. Dave ruled the ladder (**Foundations · Tokens**, then **Primitives (if
needed) / Element / Pattern / Block / Shell / Template**) and then, in the same breath, replaced
the facet chips with two tabs: *"Instead of filters can I just have two tabs usage and type"*.

Then all five findability decisions in one word — *"do them all"*. The consequential one is the
first: **v2 REPLACES `showroom/index.html`.** Two indexes drift; the way you stop them drifting is
to have one. That made a generator question out of a design question — `gen_showroom.py`'s index
assembly had to be *removed*, and `PROTECTED = {"index.html"}` added so the orphan prune could not
delete the library it no longer generates.

The chrome then went Swiss, against the skill contract, with **both project substitutions declared
on the face of the receipt** rather than quietly applied: the skill's accent `#DB0011` is not the
red on white here (`s151-D1`, the two-red law, gives `#DA1A00`), and the skill's `--black:
#000000` is not this project's ink (`#1A1A1A`, blackest-not-pure-black). Selftest bite 25 proves
neither skill value appears anywhere in the page. **A design system applied over another design
system needs its conflicts named, not resolved silently** — the substitutions are standing law,
and law that is applied without being cited is indistinguishable from a worker's preference.

---

## 5 · Two small class-fixes that were the day's cheapest wins

**Directory-address doc rows.** The doc-row gate wanted a store row per new document, and six nav
screenshots arrived as a set. Six rows would have been noise hiding signal. The fix: a `home`
ending in `/` rows every file beneath it — one row (`W-106`) for the directory, with the capture
provenance in the owning document. The gate's directory arm was driven both ways before the row
was minted.

**The `s215-D1` grandfather clause.** The obvious repair for eight ids that no longer match a
regex is to rename the ids. It was rejected, and the reason is `ADR-0017`: **ids are addresses.**
`W-99za`…`W-99zh` are cited across receipts, briefs and rolled banners; renaming them would leave
every citation pointing at nothing, and the archive is verbatim and cannot be rewritten to follow.
So the regex widened and the stopgaps stand as written. **Widening a matcher is cheap; rewriting
history is not available.**

---

## 6 · Where the gauge sat, and what it does and does not license

Boot ran **60,248 real**, which is **2,345 OVER** the `s208-D1` band (55,595–57,903, read at
source from `knowledge/_gauge_tokens.py:178-179`). It was declared at the opener and **not
corrected into the constant** — re-basing is Dave's, and his `s208-D1` rider binds any proposal to
carry a boot-REDUCTION option beside it.

FILL crossed the **150,929** advisory and the **200,000** working line, both declared live in
chat at the 251,090 check-in. This is the first session to run the `s214-D1` conditional band in
anger with its conditions actually tested rather than asserted: the recall probe was quizzed
**blind** and came back **GREEN 4/4** (`knowledge/_probe/session-215.json`, re-read first-hand at
the wrap: `"verdict": "GREEN"`, `"missed": []`); post-crossing work was mechanical and
receipt-backed; and every ruling predates the crossing. **The band held, and it held because the
conditions were checkable.**

This wrap writes the **second** `s214-D5` hand-over row, which is the `n≥2` the `s214-D4` advisory
re-derivation was staged on. ⛔ The condition being **met** is not the line being **armed**.
Arming it is an opener announcement and it is the conductor's, at #216; `150,929` remains in
force until he makes it. A wrap sub that recorded a met condition and then acted on it would be
laundering a premise into a ruling.

---

## 7 · What is resolved, and what is still open

**Resolved this session:** the `W-` id space (`s215-D1`) · the itinerary as a desk item
(`s215-D2`) · `P8`, carried unruled since #212 (`s215-D3`) · the level word-set and the two
library-v2 calls (`s215-D4`/`s215-D5`) · the `canon.css` 48 (`48 → 0`, at cause) · G2's existence
· the matching-bug claim (disproven, withdrawn) · the twenty-run red streak.

**Still open, and most of it is Dave's:** every PROPOSED-FOR-DAVE set the library and taxonomy
work produced (16 usage-group assignments, the Charts→Data-display fold, the status derivation
rule, grey-4 decorative numerals at 2.01:1, related-cluster membership, the empty Foundations and
Tokens tiers, the 12 PFD rows over 41 components) · the REVIEW-213 tranche sittings, 172 questions
· `ds-005`'s missing `_rulings.json` row · the stop-line / wall / boot-band re-base · G2's undriven
scope · five priced-not-built instruments, two of which are now on their third and fourth session
of being carried.

⚠ And one dependency that is not the repo's: the chromium libs at `/var/tmp/chromelibs-s213e2`
belong to session #213. The re-extract recipe is now the fourth stratum of
`knowledge/_RUNBOOK-render-verify.md`, which also records the adjudication that the **#125 TLS
reading is environment-dependent** — both #125 subs were telling the truth about their own
sessions, and `NODE_EXTRA_CA_CERTS` is what separates them. A contradiction that stood three
sessions turned out to be two correct readings of two different environments.
