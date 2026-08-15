# #176 — the step trackers inherit the roundels, and "ink" becomes a ruled principle

```
provenance: s176 · 2026-08-15
status: ruled — knowledge/_rulings.json § s176-D1, § s176-D2
```

*Spine entries: `GOOD-MORNING.md` ★ LATEST #176 · `_LIVE-STATE.md` ⏱ LATEST DELTA #176.
Ledger: `knowledge/_rulings.json` § `s176-D1`, § `s176-D2` (155 → 157).
Both-way: those entries cite this session; this dossier cites them.*

⚠ **DATE SEAM, DECLARED FIRST BECAUSE IT IS THE KIND OF THING THAT ROTS SILENTLY.** The session ran
on **2026-08-14** and both rulings carry that date. This wrap ran after midnight and every stamp it
writes is taken from `date` — **2026-08-15**. Neither date is wrong; the seam is written down rather
than smoothed, because a handoff that quietly harmonises two clocks is how a false inscription of
something as small as a date gets made.

---

## Why there are two rulings and not one

#175 ended with a *permission* and two *gaps*. It ruled that a continuous quantity is ink only and
that discrete steps **may** use colour, with Legacy definite and Mono/Console/Supercharge explicitly
undecided; and it ratified `#13110E` as the right black **for Supercharge** while leaving the general
principle — that "blackest ink" resolves per theme through the alias chain — **implied but not ruled**
(`s175-D1`(f), written into the entry as an open generalisation for the next session).

#176 closed both, in the order they were asked.

### `s176-D1` — the principle, and the value of asking about the hedge

Dave's own words carried the rule and a hedge inside the same sentence:

> "the simple rule for ink is the blackest ink that isn't pure black, to avoid halation. #13110E for
> SC / #1a1a1a for Mono and console I think, that might not be right / #333333 for Legacy"

The load-bearing method here is small and worth naming: **the hedge was resolved by verifying against
the token store BEFORE the read-back, not after it.** All four values were checked — Mono ink `mono/4`
**#1A1A1A** (R-D16); Console LOCKED = Mono on the DNA layers, therefore also **#1A1A1A** (R-D25);
Supercharge `warm/2` **#13110E** (the ADR-0014 anchor remap); Legacy body ink Grey 8 **#333333**
(col25-011) — and all four already matched what is shipped. So the read-back could tell him *"your
hedge is unnecessary, the store already agrees with you"* rather than asking him to re-decide values
he had already decided. He answered *"yes this is fine."*

**Nothing was enacted, because there was nothing to enact.** The ruling's whole content is the
principle plus its rationale — halation — neither of which had ever been written down. That is the
interesting part: the *values* had been derived correctly four separate times by four different
mechanisms, and the *reason* had never once been inscribed. The rule was living in the values.

### `s176-D2` — ruled by eye, off three pages, and the corrections are the record

This one was taken visually, over three live review pages, and the arc matters more than the endpoint.
The endpoint: `step/complete` **aliases `rag/success`** — the roundel chain — so themes inherit
wholesale (Mono #66CC8D, Console/SC #5DAC7B, mode-invariant). Dave: *"exactly the same system that we
use for the success roundels on all, they can just inherit then wholesale."*

The Legacy leg took four passes, and all four are recorded in the entry verbatim rather than
collapsed into the answer: *"the red"* → *"warning red"* → *"Legacy error, sorry my mistake"*
(#A8000B) → and then, **off the v1 page**, *"Use the primary red for Legacy"* — #DB0011, final. The
last correction only happened **because there was a rendered page to look at**. A list of hexes would
have shipped #A8000B.

The dark leg — white — **supersedes `s175-D1`'s Legacy red-both-modes, by his own word**: *"both are
true."* Same shape as #175's own supersession of the 2026-07-21 `$note`: the ruler disowning his
earlier reading is a different animal from an agent re-interpreting it, and the record says which
happened.

### The doctrine clause, which is the one that will outlive the colours

> "the intent/meaning is carried by the glyph a label, therefor the track and the roundels it is less
> important that they have Ally contrast. the label and the symbol must carry the contrast not the
> decoration."

This converts a two-session-old open finding — fill-on-track failing 3:1 in Legacy dark (1.75) and
Supercharge dark (2.38) — from *a defect awaiting a value change* into *a declared absence with a
ruled rationale*. The gated legs are the tick-on-fill and the label, and they all pass (5.22–8.77 and
12.63–17.45). The six sub-3:1 light fill cells are handled the same way.

★ **The general point: the finding did not get fixed and it did not get ignored — its GATED SCOPE was
ruled.** That is the third time this pattern has been used (`s134-D1`, `s151-D2`, `s160-D2`) and it is
now Dave's stated rationale rather than an inference from precedent.

---

## The finding: the Mono and Console steps painted nothing at HEAD

#175 minted `step/complete` and rebound the step components to it. Every gate was green. The showroom
regenerated. The ruling was, by every available check, enacted.

**And in Mono and Console the step indicators painted nothing at all**, because `canon.css`'s TOKENS
block had never been regenerated since the mint, so the token had **no `:root` definition to resolve
against**. A CSS custom property with no definition is not a parse error. It is not a lint failure.
It is a blank.

It was found by **measuring computed styles in a real browser** — the controller sub's work — and it
could not have been found any other way that was actually in place. The store said one thing, the
artefact said another, and every instrument we own reads the store.

★ **The lesson, and it is a general one: a ruling can be fully enacted in the STORE and wholly absent
from the ARTEFACT, and the two are checked by different instruments.** Cf. `no-gate-parses-the-artefact`
— which says the first gate should parse the artefact in the consumer's grammar. Here the consumer's
grammar is *the computed style of a rendered element*, and nothing parses that except a browser.

## The second finding: a selftest clause that could not fail

`gen_theme_cascade.py`'s selftest carried an **indentation defect**. A set of assertions sat inside a
wrong-scope `if`-branch — so they could only ever execute **after another assertion had already
failed**. On the passing path they were unreachable. They had been green for a session, and their
greenness meant nothing whatsoever.

It was fixed and mutation-proven (receipt 5 of the refinement sub). This is the purest instance of
`mutation-tests-the-clause-not-the-feature` we have recorded: the clause was correct, the tier was
correct, the wiring into `_build_all.py` was correct — and it was **unreachable**. The only thing that
distinguishes a passing test from an unreachable one is driving it to red on purpose.

## The third finding, declared against ourselves

The first attempt to inscribe `s176-D1` went through `json.dumps` and **reformatted the whole rulings
file — 549 lines churned**. It was caught by `git diff` before commit, reverted, and redone as a
textual tail insertion.

⚠ **That is a HIT on the serializer class, not a near-miss.** The standing rule
(`serializer-defaults-reformat-the-file`) says round-trip byte-identical **before** writing; the first
attempt did not. What worked was the *other* half of the discipline — reading the diff back — and it
is worth being honest that the class was caught by the check, not prevented by the rule.

## And the one this wrap declares against the inscription itself

`_governs.py --selftest` went from **7 fails to 14** when the two entries landed. This wrap measured
**both ends first-hand** rather than relaying either: `git show HEAD:knowledge/_rulings.json` written
over the working file → run → **7**; working file restored byte-identically and re-parsed (157
entries, tail `s176-D2`, `git diff --stat` unchanged) → run → **14**.

All seven new fails name `s176-D1`/`s176-D2`, in two shapes:
- evidence strings carrying **no `chat #<n>` / `commit ` pointer** — prose provenance where the
  resolver wants a legal form (the `honest-refusal-needs-a-legal-form` class, from the other side);
- **four contrast figures** (`8.77/8.77`, `5.22/17.40`, `6.34/6.34` ×2) that the anchor resolver reads
  as pointers and cannot resolve.

⛔ **This wrap did not repair them.** The entries are ratified record and they are Dave's; add-never-trim
outranks a green selftest, and a wrap sub editing the text of a ruling it did not author is exactly
the move the do-not-rule list exists to prevent. It is carried as the top mechanical residual instead.

---

## Where it leaves things

**Resolved:** the three undecided step-colour themes (by inheritance) · the per-theme-ink
generalisation (ruled) · the step-component fill-on-track contrast finding (by doctrine, as a declared
absence) · the ~15 lines of stale component prose (fixed) · the Legacy selftest mirror (written).

**Open, and the first two are Dave's:**
1. **The token-fork ledger baseline** — `_validate_token_forks` is red with 4 `--complete` forks
   against a 42-fork ledger. Declare, unify, or rule the baseline. Nothing was touched here.
2. **The seven new `_governs` fails** — repair is an edit to ratified record.
3. **There is still no `step/incomplete`** — the step components still bind `progress/incomplete`, and
   the asymmetry is visible in the manifests.
4. The full `_validate_state_contrast.py` population run, and the composite `_build_all.py` verdict,
   are **owed to CI** — this session was instructed not to run the build.

★ **And the dream pass is scheduled by Dave for after this session** — a dated sitting, not a queue row.
