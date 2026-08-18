# #200 — the derivation moved to mint time, and the scope narrowed to console

```
provenance: 200 · 2026-08-18
status: observed
```

*The narrative dossier for session #200 (capture-ritual step 1b). The WHAT lives in
`GOOD-MORNING.md`'s ★ LATEST banner, `_LIVE-STATE.md`'s ⏱ LATEST delta, and
`knowledge/_rulings.json` § `s200-D1` … `s200-D4`. This file holds the WHY and HOW.
Written by the DELEGATED wrap sub; every sha here is read back from `git log`, never from
the brief this sub was given.*

Both-way links: `GOOD-MORNING.md` ★ LATEST #200 · `_LIVE-STATE.md` ⏱ LATEST DELTA #200 ·
`knowledge/_rulings.json` `s200-D1`/`s200-D2`/`s200-D3`/`s200-D4` ·
`_PROPOSAL-size-ramp-theme-modes-2026-08-18-v1.md` (`W-38`) ·
`knowledge/_REVIEW-SIGNOFF.md` (the three new review rows).

---

## 1. The session opened by closing two things, not by asking about them

#199 handed forward two items and both were addressed to Dave's eye: the radius/corner tuner and
the Group B hover page. His first line closed both — *"I've approved the corner radius already,
and the hover ruling"* — which is worth recording for its shape rather than its content. The
handoff had framed them as open questions; they were already answered on his side, and the only
reason the record could not see that is that a ruling delivered in chat is invisible until a
session inscribes it. **The residual list was correct about the state of the REPO and wrong about
the state of DAVE.** Nothing was mis-handled here, but it is the same distance that
[[premise-ages-faster-than-rule]] keeps naming, arriving from the human side of the seam.

## 2. Why the derivation went to mint time rather than render time

The obvious build for "cards derive padding from radius, the thumb is container minus padding" is
a live derivation — CSS `calc()`, or a resolver at render. Dave ruled the opposite: the generator
mints **concrete values** into the token store and nothing derives at render (`s200-D1`).

The reasoning that carried it is the same one the repo has already paid for twice. A live
derivation is a rule with no artefact, and this project's gates read artefacts — a value that only
exists at render time is a value no gate can parse, which is exactly the class
[[no-gate-parses-the-artefact]] was written about, and exactly how a dangling dataviz var renders
silent black past thirteen gates. Minting produces a number on disk that a token gate can see, a
diff can show, and a reviewer can argue with. The cost is real and is now debt: **the values are
only correct as of the last mint**, so a theme added later without a re-run inherits nothing and
fails quietly. That is written into the banner's pitfalls rather than left as a property of the
design.

The sub-rules fell out of the same decision: all padding steps are 2px so the 4px grid survives
halving, and the thumb is defined as `container − padding` rather than as its own number, so the
two can never drift apart in the store.

## 3. The narrowing, and what it left behind

The mint list was read off the derive specimen (`s200-D2`). Mid-turn, Dave narrowed the scope in
two words — *"for console"* (`s200-D3`) — and that is the decision the rest of the session bends
around.

The narrowing was correct on its own terms. The three other themes derive **negative raw thumbs**
at their square radii, so minting them would have required a floor rule that nobody had ruled, and
inventing one to satisfy a generator is how a picked constant becomes a fact. So mono, legacy and
supercharge stay proposal-only and the floor-precedence question is open and Dave's.

But the narrowing has a consequence the session did not resolve and this wrap will not smooth:
console now carries **two segmented grammars at once**. The earlier padding-first mint
(container 20, thumbs 18/16/14 under `small`/`medium`/`large`) is still in the overrides, and the
`s200-D4` dimension-first mint (container 8, thumb 6 under `s`) sits beside it. A consumer that
globs the segmented tokens gets **four thumbs across two systems**, and no document says which
wins. This is declared debt, created knowingly, and it is residual ① into #201 because it is the
first thing a consumer trips on.

## 4. `s200-D4` is a read-back, and the record says so

The `36 / 2 / 8 → thumb 6` scale plus a `min-hit-area` of 44 is recorded as ruled because Dave
ruled it — but the wording in the store is **the conductor's read-back of his words**, and his
veto is open. That distinction is preserved deliberately rather than tidied away: a read-back
presented as a verbatim ruling is a small confident false inscription, and this project's cheapest
recurring defect is a claim that reads more settled than it is
[[feedback-readback-sensation-not-mechanism]].

The naming went the other way and is settled: Dave **vetoed** `scale-1..4` and ruled `xs`/`s`/`m`/`l`
in chat, and the conductor edited the labels into tuner v3 in the same beat.

The 44 has a matching honesty problem, named as pitfall (c): it is a number in a file that **no
gate reads**. A 36px target ships clean today. Minting a token is not enforcing a rule
[[instrument-without-a-consumer]], and the token being present is not evidence the rule holds.

## 5. The instinct that was recorded and not ruled

Dave surfaced a master size ramp — 24-32-40-44-48 — with pair classes (x-small 24+32, small 32+40,
med 40+44, large 44+48) and the idea of **sizing as a mode per theme**. He was explicit about its
status: *"not sure right now, I'm working in instinct, lets record these shapes tho."*

So it is homed as a proposal with a store row (`W-38`) and nothing more. The temptation at a wrap
is to promote a shape that is obviously going somewhere; the rule that forbids it is the one that
exists because a promotion carrying a stale premise has already cost this project sessions. He
also named the wider frame — the whole mechanism is groundwork for a future **theme generator**
side project — which is context for #201's reader and not a commitment.

## 6. What the wrap itself found

Two mechanical things are worth banking.

**The stale-queue gate was driven on both sides of the roll for the first time since #198.** #199
declared its PRE-roll baseline missing rather than reconstructing it, and this wrap captured it
before touching the mover: PASS, 7 items, blocking, rc=0 — identical after the 2c/2d/2f moves
landed. **Survival across a moving roll is now proven three times and detection is still observed
zero times.** The declared gap closes; the real question does not.

**The subs figure in the wrap brief did not add up.** The brief listed five measured figures and a
four-item sum, and said so — it flagged the discrepancy and told this sub to compute it. Summed
here: 65,515 + 54,069 + 81,496 + 64,141 + 49,765 = **314,986, n=5**. Banking it because the failure
mode it avoided is the ordinary one: a carried total is not a measurement, and the only defence is
re-adding the parts [[measure-dont-convert-units]].

## 7. Resolved state, and what is still open

**Resolved:** derivation is mint-time (`s200-D1`); the mint list came off the specimen (`s200-D2`);
scope is console only (`s200-D3`); the `s` scale and hit-area token are minted (`s200-D4`); the
scale labels are `xs`/`s`/`m`/`l`; #199's two residuals are consumed by Dave's own line.

**Open, and every one of them is on the residual list:** the mixed segmented grammar's arbitration ·
the untuned `xs`/`m`/`l` values (Dave's, on tuner v3) · enforcement for the 44 · a render proof and
a parsing gate for the new tokens · the `W-38` pair semantics · the card formula `max(radius,8)`
snap-2 · square-theme floor precedence · tuner v1's stale pre-enactment numbers · `data-mark`.

⛔ Nothing in this file rules anything. It records why the session moved the way it did.
