# 2026-09-06 · #251 — the strip orients, the card details: how a four-option question got answered with a pattern, and why the answer arrived unguarded

provenance: 251 · 2026-09-06
status: observed

*The WHY and HOW. The WHAT lives in `_LIVE-STATE.md`'s ⏱ LATEST DELTA #251, `GOOD-MORNING.md`'s
★ LATEST banner, `knowledge/_rulings.json` § `s251-D1` / § `s251-D2`, and the three filed lane
reports. Both-way links: spine → this file (the ⏱ delta's WHY/HOW line); this file → the ledger
entries named above. Sibling: `_DECISION-HISTORY/2026-09-06-250-adversary-at-the-brief.md`, whose
rule 7 is the method this day ran on.*

---

## 1. Why the day opened on prose, not on the queue

Dave asked for the three open items **in plain prose** before anything was shown to him. That is a
small request with a large consequence: it forced the conductor to state the DP-08 fork as a
sentence rather than as a menu, and a sentence is checkable in a way a menu is not. The menu form
(*A / B2 / C*) had already been built at #249 and sat in `outputs/w2-debt/dp08/` as four renders.
When Dave said *"DP-08 A+B. -- show me the varients"*, the renders were shown — and the conductor
did the thing rule 7 asks for at a brief: it named **four rubs** against the obvious reading of
"A with the Needs-attention card" rather than accepting the instruction and building.

The four rubs were: Undrawn is a STATE and not a DP-10 action, so putting it in Needs-attention
corrupts that surface's grammar; A and B together **double-report** the same fact in two places;
the band would carry a **four-tile row** where the canon rule may say otherwise; and B2's **rail
order** was an unproven premise below 1440.

## 2. Why the answer is a pattern and not an option — and why that matters

Dave did not pick from the menu. He answered with a relationship:

> *"the thing is I like the strip, its very important, this is a good pattern, but it need the
> coordinate with the needs attention pattern. So the user sees the strip and it orientates them
> to pay attention towards the detail"*

and then, unprompted, supplied the mechanism:

> *"this is good, teh user might even click on teh chip and it anchor links to the needs attention
> panel, this makes sense to me"*

That is `s251-D1`. The distinction is not pedantic. An OPTION is a thing you build once; a PATTERN
is a thing every future surface has to obey, and it can be broken by an edit that no one thinks of
as touching DP-08. The double-report rub dissolved into a sub-ruling — `s251-D2`, one shared count
in the strip's own words, *"14 payments · 5 need you"* — and the Undrawn rub was settled the way
the grammar wanted: strip-only.

## 3. Why the premise probe went first again, and what it caught

Rule 7 (`MODEL-ROUTING.md`, born #250, still not a ruling) says: adversary at the BRIEF, verifier
only at CANON. The probe lane tested the ruling's premises before a builder touched the library.

Three premises held. The four-tile row is real and the page rule out-specifies canon (the band is
4/4/4, and a mutation caught it). B2's rail order holds at 1440 — first-chart y **678.6** against
**913.7** — and goes equal two-up at 1100. The byte budget survives: prototype **1,753**, page
**14,801 of 34,816**.

The third of those is the interesting one, because it changes what the ruling MEANS. Below 1440 the
Needs-attention card sits at 1112 or 1242 and the geometric relationship — "the strip is above, the
detail is below" — stops carrying the message. **The ANCHOR carries it instead.** Dave had already
said so (*"click on teh chip and it anchor links"*) without having the measurement; the probe turned
his instinct into the load-bearing half of the build.

And then the probe found the thing that would have shipped: **option A's chip pointed at `#p2` —
the Payments TAB — and the Needs-attention card had no `id` at all.** The artefact the ruling was
made ON did not contain the link the ruling is about. A verifier at the end would have found this
too, but only after a lane had built on top of it.

## 4. Why the build stopped twice instead of improvising

Two moments in the BUILD lane are worth recording as method rather than as outcome.

**It refused to trim DP-20.** The finished canon page reads **26 carriers, 9 above the fold at
1440** — worse than the #249 specimen's 5, partly because the strip's chips ARE carriers and partly
because the canon page is SHORTER, which raises the density above the fold. The budget is three.
The lane reported it and did not act, because *what counts as a carrier* and *how many the fold may
hold* is the DP-20 budget's own question, and no gate in the repo fails on a carrier count. A lane
that trims to make a number look right has changed a design rule by stealth.

**It named what canon does not have.** Canon has no `#p1` tabpanel, so the lane proved the
equivalent rather than inventing one. And canon never had "Undrawn facilities" — it has
`Available overdraft`. The lane mapped the two, which the verifier later ruled legitimate
(`s247-D3` names that tile).

## 5. The one thing that went wrong, and why it is a different KIND of error

While mapping that tile the lane **pasted the specimen's numbers** — `$120.0m`, `$2.7m`,
`40% drawn` — into a template whose own facts are `£25,000.00` and `None used`.

This is not a wrong number. A wrong number is visible to anyone who checks arithmetic. A **pasted**
number is a true fact from a different document wearing this document's clothes: it is internally
consistent, it renders correctly, it passes every gate, and only a reader who knows what canon
actually says can see it. The currency was the tell — the verifier counted **7 `£` against 2 `$`**
and isolated `40% drawn` as the invented fact against canon's `None used`.

The conductor restored canon's own facts by hand: `Available overdraft £25,000.00 · None used ·
Limit reviewed 4 Aug`, head row `£9,840.55`, **`$` count 0** outside comments and meta, both gates
re-run, six renders re-run.

## 6. Why a GREEN build can still be an unguarded one

The verifier's NEW 21 is the finding that outranks the build. Delete `id="dp08-na"` and the chip is
dead — `dp08-anchor.js` finds no target, nothing scrolls — and **`_validate_behaviour.py` and
`gen_component_partials.py --check` both still exit 0.**

So the correspondence `s251-D1` is entirely ABOUT is invisible to every gate that guards the file it
lives in. This is `V-MUT-5`'s shape a second time (there, the page byte sum trusts a `consumes`
declaration it never reads), but it is the first time the unguarded thing is a **ruling's own
subject** rather than a cap's arithmetic. The verifier added three more of the same family in one
sitting: `--mutate` bites only `dv-behaviour` and cannot touch the new partial the gate nevertheless
measures (NEW 22); an OVER-declared `consumes` passes the byte gate (NEW 23); and three columns
produce rows `[3, 1]` with voids of 920/693/507 px while `s249-D5` — *"No ragged layouts"*, Dave's
own words — has no mechanical consumer at all (NEW 24).

★ The pattern across all four: **we are good at gating quantities and bad at gating relationships.**
Bytes, counts and physics have gates. "This points at that", "this is what that declares", "no row
is ragged" do not. Every one of them is a definition question before it is a build question, which
is why they go to Dave rather than into a commit.

## 7. A lock came off, and a standing claim was retired

The wrap's own commit was blocked at #251 by a 0-byte `.git/index.lock` left by a lane at 15:07.
`rm` returned *Operation not permitted* from the sandbox. Previous sessions recorded this state as
**untouchable from inside** and worked around it. Dave enabled deletion through the Cowork prompt
and the lock went — the first time a lane-left lock has been cleared from within the sandbox. The
"untouchable" claim is retired, with its receipt, in `_CARRIES.md`'s strays carry.

## 8. What is resolved, and what is still open

**Resolved:** DP-08's *"in combination?? maybe?"*, open since #249, is ruled (`s251-D1`, `s251-D2`),
built into canon, gated green, rendered six ways, and pushed at `fc1209b`. The invented fact is
undone. The push backlog carried since #244 is gone.

**Open, and Dave's:** the DP-20 carrier budget against 26/9 · a guard for the strip→card link ·
the `consumes` cross-check (now with an over-declaration face beside it) · a definition of a ragged
row so `s249-D5` can be gated · legibility (ADR-0015 A1 vs A3) · the ceiling arm, still red on
#247/#248/#249 while #250 and #251 both read UNDER · and the midnight-wrap stamp, which this wrap's
2d EXIT CHECK found had no standing home at all and copied into `_CARRIES.md` at its true age of 10.
