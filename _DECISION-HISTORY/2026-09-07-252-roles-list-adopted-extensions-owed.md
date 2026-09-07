# 2026-09-07 · #252 — the roles list adopted whole, and the three extensions Dave asked us not to forget

provenance: 252 · 2026-09-07
status: observed

*The WHY and HOW. The WHAT lives in `_LIVE-STATE.md`'s ⏱ LATEST DELTA #252, `GOOD-MORNING.md`'s
★ LATEST banner, `knowledge/_rulings.json` § `s252-D1`, `knowledge/roles.json`, and
`_HANDOFF-252-lanes-cold.md` (the three lane briefs this session wrote and did not fire).
Both-way links: spine → this file (the ⏱ delta's WHY/HOW line); this file → the ledger entries
named above. Sibling: `_DECISION-HISTORY/2026-09-06-251-strip-orients-card-details.md`, whose
`s251-D15` working shape — Claude authors, Dave vetoes — is the shape this whole day ran on.*

---

## 1. Why a REVIEW page and not a build

`s251-D15` had already ruled the working shape at the post-wrap sitting: **Claude authors one page
per batch, Dave strikes what is wrong.** The roles list was the first thing that shape was applied
to, and the choice mattered: the `provides` vocabulary is an ADDRESS SET — every later `$composes`
tag, every `not-with`, every validator resolution points into it — so a slug invented by a build
lane mid-flight would have become canon by accident. Authoring it as a page first put the whole
vocabulary in front of Dave in one sitting, at a moment when striking a slug cost nothing.

The page is `reviews/ROLES-REVIEW-2026-09-07-v1.html` (26,363 B, swiss): twelve roles, the
membership for each, 137 metas placed, 25 first-pass covered, and a §14 that put **six authoring
calls** to Dave by number.

## 2. What Dave actually said, and what it did NOT settle

Verbatim: *"Okay these look great, go for it, qq, might we extend this in the future or do you
think this is as much as we need?"*

Two things are true of that sentence and they pull in different directions.

**(a) Nothing was struck.** No slug renamed, no membership contested, no §14 call answered
against the page. That is an adoption of the page as it stands, and it is what `s252-D1` records:
twelve slugs, the membership, the six calls and the placed-not-provider set *exactly as the v1
page lays them out*, with one home — `knowledge/roles.json`, built on the `chart-intents.json`
pattern — and a thirteenth role reserved to Dave.

**(b) The question is not a ruling.** *"Might we extend this?"* is a question, and the honest
answer given in chat named three expected extensions: **input sub-roles** when forms are authored
(the non-factory modes of `s251-D7`), **media/identity** for marketing pages, and
**needs-attention** if Dave ever names that molecule as a role of its own. Dave's reply — *"maybe
not this so neither of us forgets"* — is a CARRY, not a decision. He did not adopt the three; he
asked that they not be lost. They are therefore written three times: in `s252-D1`'s own text as
EXPECTED-not-forbidden, in `roles.json`'s `$extension` field, and on the `_CARRIES.md`
`## residual → #253` line at age 0.

⚠ The distinction is the whole point of this section. A wrap that read *"go for it"* as covering
the extensions would have handed #253 a thirteen-slug vocabulary nobody ruled.

## 3. Why the premise probe ran before the lanes were briefed, and what it killed

`MODEL-ROUTING.md` rule 7 (the #250 working shape) says the adversary goes to the BRIEF. Applied
to the 25-meta pass, the probe found four things that would each have reddened the tree on
arrival:

1. **`knowledge/components/meta.schema.json` is `additionalProperties: false`, and NINE scripts
   enforce it.** Any lane that wrote `provides` or `answers` onto a meta before the schema learned
   those words would have taken every gate red at the moment its first file landed. That single
   finding is why the wave order in `_HANDOFF-252-lanes-cold.md` is **C alone first, then A and B
   together** — a sequencing constraint discovered by reading the schema, not by running a lane.
2. **No consumer of the eight terms exists anywhere.** The grep is clean: the only match for the
   word "span" is `_validate_descender_clip.py`, unrelated. So the validator IS the first
   consumer, and every lane brief has to say so [[instrument-without-a-consumer]] — otherwise the
   pass would ship tags that nothing reads and the gate would report green over them.
3. **`intent` already sits on 15 of the 25 metas** (all 14 charts, plus one). That makes the
   `answers`-vs-`intent` question real rather than theoretical, and it is the reason the handoff
   proposes `answers` as a NEW field whose value equals `intent` verbatim on charts, with the
   resolver asserting equality — **a strikeable proposal, not a decision.** Every "call" in that
   file is the same shape.
4. **`roles.json`'s provider lists are MEMBERSHIP; the priorities and `when` clauses on the review
   page are ILLUSTRATIVE.** The metas become the source when they are authored, and the validator
   then cross-checks the two. Writing this down was what stopped the page's illustrative numbers
   from being copied into canon as if they were ruled.

## 4. Why the lanes did not fire — and the cause, not the excuse

The lanes were briefed and never run. The stated cause is measured: FILL reached **150,302 real**
against the **150,929** advisory, with 42 turns and a boot of 69,526. The mechanism was not the
work — it was the ARTEFACT: the harness re-echoed the 26 KB review page into context **three
times**. A page authored for Dave to read costs the conductor its own bytes every time it crosses
a tool boundary, and that cost is invisible in the plan because the plan prices the WORK.

⚠ This is the #239 route-price class in a new costume (there it was three doc URLs at ≈35,000
real; here it is one review page, three times). The general form worth carrying: **an artefact
authored for a human is priced as a deliverable and paid for as context.**

The correct response was to STOP and write the briefs down cold, which is what
`_HANDOFF-252-lanes-cold.md` is: the probe's findings, the three lane bodies, the verifier pairing
and the wave order, so #253 fires them at its opener with no re-thinking. That file OUTRANKS
`_CHAIN.md` for #253 and is deleted at the #253 wrap — the same contract
`_HANDOFF-251-post-wrap-sitting.md` carried into this one, and which this wrap discharged and
deleted as instructed.

## 5. What is still open when this file lands

- The six §14 calls, the `answers`-vs-`intent` field call, the `when` predicate's field list, the
  `shape` vocabulary, rails for non-factory modes (`s251-D7`) and whether Chart-bullet belongs in
  `headline-metric` — **all Dave's, all recorded as OPEN, none decided at this wrap.**
- The three role extensions, carried verbatim at his own request.
- The boot-ceiling arm, still red on #247 and #248 and now discharged for #249 — see the ⏱ delta.

---

*Both-way link: `_LIVE-STATE.md` ⏱ LATEST DELTA #252 → this file. Ledger: `knowledge/_rulings.json`
§ `s252-D1`. Register: `knowledge/_REVIEW-SIGNOFF.md` (the roles review's row).*
