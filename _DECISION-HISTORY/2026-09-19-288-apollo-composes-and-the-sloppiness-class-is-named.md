# #288 — Apollo composes, not traces; and he names the defect class

provenance: 288 · 2026-09-19
status: observed

*The narrative dossier for session #288 (ritual step 1b) — the WHY and HOW, not the what. The terse
records hold the what: the ★ LATEST banner in [`GOOD-MORNING.md`](../GOOD-MORNING.md), the ⏱ LATEST
DELTA in [`_LIVE-STATE.md`](../_LIVE-STATE.md), the carry set in
[`_CARRIES.md`](../_CARRIES.md) § `residual → #289`, and the handoff
[`_HANDOFF-139-apollo-composes-and-the-sloppiness-class-is-named.md`](../_HANDOFF-139-apollo-composes-and-the-sloppiness-class-is-named.md).
His words, verbatim and never paraphrased: [`notes/_lanes/288/DAVE-RULINGS-2026-09-19.md`](../notes/_lanes/288/DAVE-RULINGS-2026-09-19.md).
The five filed lane reports are cited by path in §9.*

---

## 1 · The session was built to answer three orders and ended up answering a fourth question nobody had asked

#288 opened on `_HANDOFF-138`'s three moves — the strand map and the Friday-25th path, the bento
spacing review with the `s219-D3` arm built, and the template quality review. Four Opus lanes were
cut in one wave and all four landed. That is the boring half of the story and it is worth one
paragraph.

The interesting half is what happened when the work was shown to him. He looked at the showroom
template — the artefact that three of the four lanes had been circling all morning — and did not
comment on its gutters. He challenged the premise of the entire one-shot path:

> there is a definitely a problem here, 2 actually, the template is a bit wonky and it's basically
> copied by the AI, what is the point of building the KG if the agent just traces an existing file,
> its very safe but 1. its of average quality anyway... its okay but not great 2. what was the point
> of building the system if it just traces from existing examples???
>
> the results with VS co-pilot are pretty much identical to this, this isn't Apollo its a dot-to-dot
> book

**Why this matters more than any of the four lanes' findings:** every gate, every ruling and every
generator in this repo answers the question *"is the output correct?"* His question is *"is the
output ours?"* — and the two come apart exactly where a builder is rewarded for copying. The
mechanism was already in the record and nobody had read it that way: **the #230 "zero invented
markup" pass condition rewards tracing.** A builder that splices the template byte-identically
scores perfectly against it. The pass condition was written to stop invention; it also, silently,
stops composition.

## 2 · The probe was the right shape because it removed a variable rather than adding an argument

The obvious response to *"it just traces"* is an argument about whether it traces. The response
taken was to make tracing impossible and look at what came out: one Opus lane, a cold one-shot,
the template **unreachable**, two renders side by side, nothing in the repo changed.

That shape has a property worth naming: **it cannot be won by rhetoric.** Either the composed page
is recognisably Apollo or it is not, and Dave decides by eye. The lane's job was to make the eye
test possible and to print its own limits on the sheet — which it did, including the one that most
weakens it (§4).

## 3 · His verdict split the question in two, and the split is the finding

> so better is someways and worse in others, its more interesting and complete page , but its more
> sloppy .
>
> I'll create a test brief for these tests.
>
> we need to do something about the sloppiness and, its all about alignment spacing and dimensions,
> this looks like its working the way I'd have expected, at least it's diverged from the tamplete

**Two verdicts in one message, and they point opposite ways.** The METHOD is endorsed — *"diverged
from the template"*, *"working the way I'd have expected"*. The EXECUTION is not — *"more sloppy"*.
Collapsing them into one verdict would have lost whichever half was inconvenient, so the record
keeps both, separately, and the handoff says so in its own headline.

**And he named the defect class himself: alignment, spacing, dimensions.** That is worth more than
any list a lane could have produced, because a named class is testable and a list of complaints is
not. What the conductor saw on the render — dead space under sparklines, a half-empty table card
against a full-height neighbour, two bottom cards not sharing an edge, a filter bar narrower than
its table, gutters differing between rows — is recorded **as the conductor's reading**, beside his
class, never as his words. The same discipline #287 used on the gutters framing.

**The third sentence is the one that binds a future session: *"I'll create a test brief for these
tests."*** That is owed by Dave and no lane may write it. It is also the direct answer to §4.

## 4 · The lane found the hole in its own comparison and printed it on the sheet

The probe was supposed to run the frozen demo prompt. **It could not be found.** The lane searched
`_memento_search.py` (and `--all`), the #229 cold-start acceptance brief, the #230 demo-day brief,
the #258 demo-fence brief, and grepped the repo for the prompt's own distinctive phrases. Every
brief **describes** the test — #229's *"a dashboard ask phrased the way a designer would ask it"* —
and **none carries the text.**

So the probe ran on a fallback brief invented for the lane, and the traced template it was compared
against had been built at an earlier session against a *different* ask (a business-banking account
overview). ⇒ **The two pages answer different briefs, and the comparison is therefore about HOW each
was made, never about which answers a shared ask better.**

**This is the part of the session that most deserves the dossier rather than a ledger line.** A lane
that prints the limit of its own comparison is the reason his verdict can be trusted as a verdict on
the method. A lane that quietly used the fallback and reported a clean A/B would have produced the
same page and a worse fact. And the gap it exposes — a "frozen" prompt that lives nowhere — is
exactly what his *"I'll create a test brief"* closes.

## 5 · The arm was built and it still does not settle the thing it was built to settle

Lane A built the `s219-D3` generation arm: `knowledge/canon/gen_bento_role_vars.py`, 289 lines, the
**first consumer** of `knowledge/_render/_bento_edit_rails.json` — a file that had declared itself
`$groundwork_only` in its own header and sat un-consumed for sixty-nine sessions. It cross-checks the
manifest against the owner the file itself names, parses Dave's own receipt rather than typing the
values, and **refuses by name on a divergence instead of picking silently**. The markers go *before*
`AUTO-THEMES START` because `gen_theme_cascade.py` rebuilds everything after that marker and would
destroy a later block without a word — and that is asserted by the generator's own selftest, not
remembered.

**And then the interesting part: it does not answer Mono's 0.** The outer (structural) gutter has
two readings — the token `layout/bento/gutter` at 0/24/24/0 (`s217-D2`) and the role defaults at
40/24/40/24 — and the arm delivers the second *because that is the file `s219-D3` names*, not because
anyone chose. The inner gutter has three (canon's literal `1px`, `subSpacing` 4/4/4/2, the template's
pinned 4). Supercharge's 0 is inherited from a table and was never decided by anybody.

**The lane declared its pick and picked no winner.** That is the correct move under Dave's #287
correction — outer and inner are two deliberate quantities, not a contradiction — and it is why
"the arm is built" cannot be written as "the spacing question is closed".

## 6 · Why nothing was struck, and why that is a decision rather than an omission

Exactly one thing #288 closed can be receipted: the arm is built. The carry that names it reads
**"MONO'S 0 IS DOUBTED AND THE `s219-D3` GENERATION ARM IS TO BE BUILT"**.

`s183-D1` strikes a **headline**, not a clause of one. The first half of that headline is still true:
`s217-D2` still rules the value 0 for mono and Dave ruled nothing on it today. Striking would delete
a true claim in order to record a true one. ⇒ **the discharge is said in a new carry item instead** —
the identical move #287 made for the connector-lever item, and for the reason `s271-D4` states in its
own words: *"a strike that is wrong is worse than an item that is merely stale."*

**The general shape, because it keeps recurring:** when a session closes half of a carry, the carry
does not move; a new item records the half. Two wraps in a row have now met this and answered it the
same way, which is starting to look like a rule rather than a judgment — and whether it becomes one
is Dave's.

## 7 · The probe measured three things no gate in this tree can see

Not findings about the page — findings about the system, each taken on a live render:

1. **Canon's own instance-dial recipe loses silently.** Canon instructs *"declare instance dials as
   `.c-bento.my-wall{…}`"* at specificity (0,2,0). The rule that restores the outer gutter for a
   bento-of-bentos is `:has()`-lifted to (0,4,0). Measured: a bare `.c-bento.wall-ops{--bento-gutter:40px}`
   had **no effect** and the wall rendered at **0px, not 40**. A builder following canon's own
   instruction loses the ruled spacing and nothing says so.
2. **Canon clips silently.** A 694px list stretched a row to 791px inside a wall canon fixes at
   320px, and `overflow:hidden` swallowed it — **no DOM symptom, `pageErrors: []`**.
3. **No gate reads the composition of a page that LINKS `canon.css`.** `_validate_composition.py`
   reads the grammar from the artefact's own `@container` blocks, so the orphan-cell arithmetic
   `DP-16` and `s249-D5` rest on is uncheckable there. Every composed screen in the tree so far has
   been self-contained; this is the first one that links canon, and it fell straight through.

**The common shape of all three is the one worth carrying: a failure with no symptom.** Each is a
correct-looking page, a green console, and a value that never landed. That is the class that survives
longest, and none of the three is fixed or ruled — every one is a generator or gate change.

## 8 · Corrections and things that went the wrong way

- **Four of the five filed lane reports carry no `RULING-SHAPED QUESTIONS` heading**, which
  `s218-D7` clause 4 makes mandatory. The *content* is present in all five under other names —
  *WHAT IS NOT DONE*, *WHAT I COULD NOT ESTABLISH*, *Gaps*, *Decision pack*. What is missing is the
  **name** the gate and the next reader look for. Not repaired here: a wrap does not edit another
  seat's filed report, which is dated history (`ADR-0017` / `s192-D1`).
- **Lane A ran `git stash push`** against the standing rule that git writes belong to the commit
  lane — and declared it itself, with the evidence that no stash entry was created and the tree was
  intact. A judgment named in a report is one the conductor can correct; one discovered at the wrap
  is one he inherits.
- **`knowledge/_render/seat_env.sh` globs a playwright path 1.63 no longer ships.** Lane B
  symlinked around it and rendered; lane T could not render at all and said so rather than
  reporting a CSS reading as a rendered one. A render seat that works only when the lane improvises
  is not a render seat. One line owed, not done.
- **#288 has no lane commit.** #287's report named the cause of its own clean single-invocation
  commit — a commit lane that reads the prior lane's report first — and #288 did not repeat the
  shape, so every gate was driven green at the wrap seat under wrap heat instead.

## 9 · Resolved state, and what is still open

**Resolved:** the `s219-D3` arm exists and is consumed; the strand map exists and every path on it
resolves; the four themes are rendered side by side for his eye; the template's quality is measured
rather than felt.

**Open, and all of it his:** what the one-shot generates FROM and what becomes of the #230 pass
condition · the test brief he will write · the deck's new structure, on which Wave 2 is blocked ·
which event Friday 2026-09-25 is · the outer and inner gutters · lane T's six questions · the Swiss
skill as a taste layer, parked by his own word with *"don't let me forget this"*. **No ruling was
inscribed and `knowledge/_rulings.json` stays at 622.**

**Both-way links.** Spine: `_LIVE-STATE.md` ⏱ LATEST DELTA #288. Ledger: none — nothing was
inscribed. Handoff: `_HANDOFF-139-apollo-composes-and-the-sloppiness-class-is-named.md`. Carry set:
`_CARRIES.md` § `residual → #289`. His words: `notes/_lanes/288/DAVE-RULINGS-2026-09-19.md`.
Filed reports: `notes/_subreports/2026-09-19-288-M-strand-map.md` ·
`notes/_subreports/2026-09-19-288-B-bento-renders.md` ·
`notes/_subreports/2026-09-19-288-A-s219-d3-arm.md` ·
`notes/_subreports/2026-09-19-288-T-template-quality.md` ·
`notes/_subreports/2026-09-19-288-P-composition-probe.md` ·
`notes/_subreports/2026-09-19-288-W2-wrap.md`.
