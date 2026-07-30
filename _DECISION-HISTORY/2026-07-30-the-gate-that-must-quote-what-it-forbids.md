# The gate that must quote what it forbids — and the check that had been dark for want of one word

```
provenance: session-51 · 2026-07-30
status: observed
```

**Spine entry:** `notes/_MEMENTO-DECISIONS.md` § ★ #51 (the rulings and the WHY).
**This file:** how the thinking moved, including the two places it went wrong first.

---

## What the session was asked for

#50's forward title specified open 25 in full: build `BARE_TOKEN_RE` — *"fail on a
number-shaped token count in GM/LS with no unit word adjacent, same shape as
`CHAIN_STAMP_RE`, WITH a scope control and a proof BOTH ways."* It also carried an
explicit warning not to take open 24 (the self-reference ban) blind, and a follow-on
step: when the gate lands, cut the `tape`/`bill` mnemonic from the chain.

Dave scoped it at the opener to **the gate only** — no mnemonic cut, no open 24 —
on a quota reading of 78% shared / 82% Fable with 10h39 to reset. The reduction was
made to protect the wrap, on the measured precedent that the wrap is what runs dry.

---

## Finding 1 — the spec named a surface that does not exist

The spec says "GM/LS". Before writing the scope, I measured whether
`_LIVE-STATE.md` carries a `size:` stamp. **It does not.** There is no LS surface for
this check to bind to.

The tempting move was to invent one — widen the check to LS body prose so the gate
could claim to cover what the spec said. That would have been a check whose scope was
chosen to satisfy a sentence rather than to match a defect, and GM's body is full of
true dated records of what things measured; a stamp ban loose in body prose forges
defects out of correct history. That is `CHAIN_STAMP_RE`'s own scoping lesson at
`:2369`, where `GOOD-MORNING.md:488` really does carry a true `~4.1K tape` record.

⇒ The gate is **GM-stamp-scoped because that is where the stamp is**, and the comment
says so, including the re-point trigger if LS ever grows one. *Report the measurement,
never prescribe the region* — and never invent a surface to satisfy a spec.

## Finding 2 — ★★ the gate must quote the thing it forbids, and that is not a defect

The self-bite control was written on Dave's warning: feed the gate's own warning text
back through its own regex, assert it comes back clean. **It fired on the first run.**

It was right to. Bite 2 of the same suite *requires* the warn to quote the offending
figure — a gate that will not name what it found teaches nothing and gets routed
around. So the message necessarily contains a bare figure. The regex sees a match and
cannot tell that the message is **mentioning** one rather than **using** one.

The easy green was to launder the message — drop the quote, watch the control pass.
That would have satisfied the control by breaking the bite above it: a false fix that
reads as a pass, and one that silently guts the gate while looking like tidying.

★ **The finding: a syntactic ban cannot distinguish use from mention, so it can never
be made safe by being made cleverer. What makes it safe is SCOPE.** The check reads
`stamp.group(1)` and nothing else, so its own output is unreachable by construction.

⇒ The control was replaced by the two tests that actually bear on safety:
**(a)** an INVERTED bite — the message must *still* contain a matchable figure, so
that a future "fix" which deletes the quotation trips a failure instead of reading
green; **(b)** the real property — pasted into a stamp, the gate's own words *should*
flag, because an exemption for the gate's own prose is how a rule stops applying to
the thing that wrote it.

This is open 24's shape one level down, which is why open 24 stayed untouched: the
same argument says a self-measurement ban will bite the sentence carrying it, and
scope cannot save that one, because the sentence *is* in scope.

## Finding 3 — ★★ the missing word had disarmed an existing check

Run live, the new gate named two figures in GM's stamp: `§A **4.2K (EXEMPT)**` and
`corpus **58.7K**`. Both were then measured — §A at 4,208 tape, corpus at 58,658 —
so the unit was **proven** rather than copied from the neighbouring field.

Checking what the remedy would touch turned up the thing that justifies the whole job:
`SIZE_A_RE` requires a unit word after the §A figure (`§A …K (tape|tk)`). The stamp
had none. **The §A stamp validation has been dark** — matching nothing, and its
silence read as "nothing to check" rather than "the check cannot fire."

⇒ The missing unit word was never only a readability defect. It had disarmed a
neighbouring gate, invisibly, for as long as the stamp has been written that way.
[[unmatched-grep-is-not-an-absence]] and [[silent-lookup-failure-class]] in one
artefact — and the strongest possible argument for the tier being WARN-and-discharged
rather than left to accumulate.

Discharge was **by addition**: two words, +2 tape, both units measured first. Nothing
was cut, no figure changed, and `SIZE_A_RE` now matches.

## Finding 4 — ⚠ the chain is over its warn while the headline says it is under

`_CHAIN.md` measured **5,043 tape** at this session's open, against a 4,917 warn:
**+126 over**. #50's ★ LATEST banner leads with *"4,401 tape = 516 UNDER its warn."*

#50's banner does say, further down, that the relief was spent — the claim was true
when written. But "516 under" is the figure a reader carries away, and it has not been
true since that wrap ended. [[assertion-propagation-gap]]: a claim that was true at
inscription is never chased, because nothing flips.

Not chased here either — it is named, measured, and left for Dave, because the remedy
is a cut and cuts are not made in the same motion as the finding.

---

## Where the thinking went wrong first

**The control that tested the wrong string.** Test 4(b) pasted `msg[:80]` into a
stamp — a slice that stops *before* the quoted figure. It failed, and the failure had
nothing to do with the property under test. A control that tests the wrong string is
not a control; the window is now taken around the regex's own match.
[[attribute-the-diff]], on my own test.

**An f-string that could not compile.** A probe used a conditional expression inside an
f-string replacement field. Trivial, caught by the interpreter, recorded because the
error count is kept honestly rather than filtered for interest.

## Resolved state

`BARE_TOKEN_RE` + `selftest_bare_token` (seven controls) built, wired into the runner,
green, and **mutation-tested** — three mutants (dead check · lookahead deleted · `K`
requirement dropped) each caught, so the green is not vacuous. Live gate silent on
open 25 after a discharge by addition.

## Still open

- **Open 25 is DISCHARGED as specified — but the mnemonic cut it was meant to buy was
  not taken** (Dave's scoping). The `tape`/`bill` mnemonic stays in the chain; its
  checker now exists, so the cut is available to a later session.
- **Open 24 untouched, deliberately**, and Finding 2 is the argument for why it is
  harder than open 23 rather than easier.
- **Open 26 (whose tokenizer) untouched** — Dave's, unruled, largest blast radius.
- **The chain is +126 over warn.** Named, not chased.
- **2f still blocked (open 7); stack now TWELVE.** Declared, not forged.
