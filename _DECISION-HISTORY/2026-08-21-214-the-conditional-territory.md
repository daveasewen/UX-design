# #214 — the conditional territory: how "can we have more room?" came back as "only under conditions, and only while a probe says so"

provenance: 214 · 2026-08-21
status: observed

*Both-way links: spine entry `_LIVE-STATE.md` § ⏱ LATEST DELTA #214 · rulings
`knowledge/_rulings.json` § `s214-D1`…`s214-D6` · briefs
`notes/_briefs/2026-08-21-214-context-territory-strategy-v1.md` (row `W-99x`) and
`notes/_briefs/2026-08-21-214-conditional-band-200-256-proposal-v1.md` (row `W-99y`).
This dossier holds the WHY and HOW; the rulings store holds the WHAT. Nothing here is a ruling.*

---

## The arc, in one paragraph

Dave opened by asking how much more of the main context window a wrap offload might buy, and what
else could expand the working territory. The obvious answer — *move the line up* — was available,
cheap, and would have been the third time in six sessions that a constant moved because the system
was complaining. It was not the answer given. Instead the day produced a **conditioned territory**:
a band that is legal only for a certain KIND of work, only when its crossing is announced, and only
while an instrument that can independently fail says recall is intact. Six rulings landed
(`s214-D1`…`s214-D6`), the instrument was built and driven live three times, and **not one constant
moved**.

## Finding 1 — the question was about room, and room is not a line

The strategy brief (`W-99x`) mined the delegated-wrap gain and found it real but bounded: a delegated
wrap buys roughly **35–45K real of window per session** — the in-window wrap band (42,434 / 44,211 /
49,071, n=3) minus the hand-over cost (3,622–9,948, n=3). That number matters less than what it
exposed: **the advisory line 150,929 = 200,000 − 49,071 charges every session for a ritual that is no
longer run in-window.** The advisory was pricing a wrap that had been delegated for fifteen
consecutive sessions.

The temptation here is obvious and it is the trap Dave's own `s208-D1` rider was written to catch:
*"I don't want to move the goals just so the system stops complaining."* So the re-derivation was
ruled (`s214-D4`) and then **STAGED** — it enters force only once the new cost field carries **n≥2**
fresh measurements. Until then `150,929` stands. A derivation is not a measurement, and the ruling
says so in its own text.

## Finding 2 — the re-source check changed the shape of the answer, not just its confidence

Before proposing anything about 200K vs 256K, the stored justification was re-sourced against four
web sources. Two things came back. The stored 93%/76% recall figures turned out to be **Opus 4.6's
MRCR v2 numbers** — still the consensus gradient, so the shape held. But the new finding was
sharper: **recall is version-volatile.** Opus 4.7 was reported at ~32% at 1M against 4.6's ~78% — a
trade-press figure, so the *shape* is what was leaned on, not the digits.

That single fact is what turned a "raise the line" proposal into a "condition the band" proposal.
If recall can regress between model versions on the same seat, then **no static line is safe**,
and a bigger static line is strictly worse than a smaller one. The only honest way to use the
territory between 200K and 256K is to have something that can *notice* when it stops being usable.

## Finding 3 — the three conditions, and why each one is load-bearing

`s214-D1` makes the 200–256K band legal only under all three:

1. **WORK-TYPE.** Mechanical, receipt-backed, instrument-verified work only. Judgment and inscription
   work — rulings, wrap synthesis, decision read-backs — is *illegal in-band* and either delegates to
   a fresh sub or waits. Classification happens **before** entering the band, and anything
   unclassifiable is judgment by default. The default direction is the whole safety property: an
   ambiguous case falls to the safe side without anyone deciding.
2. **DECLARATION.** The crossing is announced in chat at the crossing and recorded at the wrap. This
   is the #209–#213 precedent generalised: a declared gap passes where a silent one fails, because
   the declaration is what makes the gap *reviewable*.
3. **PROBE.** The band is legal only while the recall probe is green. **One miss closes the band for
   the session and judgment work stops immediately.**

And `s214-D2` closes the obvious next question before it is asked: **256,000 stays the unqualified
wall.** The probe may only ever *close* the band, never widen past the wall — widening would require
published measurement on the current model, and none exists.

## Finding 4 — the probe had to be able to fail, and it had to fail honestly

The design problem with a self-administered recall quiz is that the examinee can cheat without
meaning to: re-read the transcript, find the answer, report green. The fix is that **answers exist on
disk only as salted sha256**, so the plaintext lives nowhere but the window. Re-reading the store
cannot produce an answer; re-reading the transcript is a defect the design makes
detectable-by-honesty, and the rule is printed in the tool's own output rather than left in a
runbook.

`s214-D3` also required **mutation proof both ways** before "enacted" could be claimed — a
deliberately wrong answer must go red, a correct one green — and required that it **run this session
on real data, never shipped dark**. Both held: planted at open, quizzed blind three times, **GREEN
4/4 at ~62K, at 279,007 and at 315,136 FILL**. That is the first in-anger data the instrument has,
and it is the reason the day's own stop-line overshoot is a *conditioned crossing* rather than an
unexplained one.

Two honest limits are recorded rather than smoothed. **`_checkin.py` was deliberately not wired** —
probe status is not re-derivation-stable across the seam digest, which is a design property, not a
missing wire; Option A (the conductor runs `--status` beside the check-in) is in force and Option B
is priced and Dave's. And **n=4 and the fact difficulty are PICKED, uncalibrated** — a green at n=4
is weaker evidence than a green at n=12, and saying so is cheaper than discovering it later.

## Finding 5 — the schema hole that #212 named, and the field that closes it

#212's mining had found something embarrassing: there was **no conductor-side delegated-wrap cost
field at all** in `notes/_GAUGE-LOG.md`. Fifteen delegated wraps had run and none had recorded what
the hand-over cost, which is exactly the number `s214-D4`'s staging depends on.

`s214-D5` orders the field into existence — brief-cut · sub-cut · delta · replay, **each measured or
declared `unobservable (<reason>)`, never omitted silently and never guessed** — and enacts it as a
*template requirement in the capture-ritual runbook*, so the obligation travels with the ritual
rather than with anyone's memory. This wrap wrote its first row. The instrument-without-a-consumer
failure mode is explicitly avoided: the consumers are named (the `s214-D4` staging check and the
re-base sitting), and both are human-read, which is stated rather than dressed up as a gate.

The second instrument, `knowledge/_boot_remeasure.py`, discharges a warning that had stood
**unactioned for about 72 sessions** at `_gauge_tokens.py:104`. It counts in cl100k tape, which is a
PROXY unit — the first log row (`_CHAIN.md` 13,839 tape · `MEMORY.md` 5,858 tape) is useful for shape
and delta and is never to be summed with a real figure.

*(A small, instructive coda: on its first wrap-gate run the new script was caught as an
**unregistered measurer** by the ds-021 (C) bite — precisely the birth-catch that bite exists for.
Registering it as `estimate-only` mirrored the declaration its own store row already carried; nothing
was upgraded or converted. A gate that catches the instrument shipped in the same session that ruled
the gate's family is the cheapest possible version of that catch.)*

## Finding 6 — the boot-reduction pair, or: a cheaper boot moves the ROOM, never the LINE

`s208-D1`'s rider says a re-base proposal must arrive **with a boot-reduction option priced beside
it**. `s214-D6` takes that option rather than merely acknowledging it, and the pair is deliberately
unglamorous:

- **Banner discipline.** `_CHAIN.md` measured **21,323 real at #213**, doubled since #109, and the
  chain *is* mostly the ★ LATEST banner. Every wrap brief now carries a clause aiming it back at its
  ~10–12K era. The clause's wording is the interesting part: **SHORTER, never
  decide-what-to-drop.** A wrap sub compresses *girth* — tighter sentences, pointers instead of
  restatement — and never omits an item, a carry, a declared skip or a receipt name. The
  justification is structural: roll-to-archive already preserves every prior banner verbatim, so
  nothing is ever lost by writing the new one tight, whereas a sub given licence to *choose* what
  matters will eventually choose wrong and no one will be able to tell.
- **`MEMORY.md` compaction at owed openers**, on the established #140/#147/#153/#177 mechanics — trim
  hooks to overflow files, never delete memory files. Run this session by the conductor: 21.2KB →
  17.6KB, `hook-overflow-2026-08-21` created, 8 entries moved.

Priced at ~11–14K real per session recovered. Per the arithmetic re-confirmed at `s214-D4`: **a
cheaper boot moves the ROOM, never the LINE.**

## What the rest of the day did, briefly, because it was not all gauge work

Three engineering findings landed beside the rulings and each is a familiar class in a new organ.

**The itinerary generator's Layer-2 shortcut** (`7f32e34`) was fixed at cause: `resolve()` had been
early-returning rows 97–124, and its `LAYER2_NOTE` premise was contradicted by its own output. The
repair replaced the shortcut with a mechanical family/direct/tokens ladder in which an ambiguous case
resolves to **UNRESOLVED and is never invented** (zero were needed), and regenerated the note *from
measurement* rather than re-typing it — the stale-twice-⇒-generate rule applied to a comment. Rotten
arm-2 fixtures were replaced by a derived arm that cannot rot. Orphans **28 → 1**.

**The descender class** (`0360a88`, `4ad4cef`) inverted its own suspicion. `ds-005` was not regressed
and the components were fully tokenised; the failure was **specificity** — 18 dead overrides across 9
snippets and 6 review components, invisible because the gate compared *authored selector strings*
rather than *computed edges*. This is the general form of "no gate parses the artefact": a file could
carry the override, never apply it, and pass. G1, the specificity leg, was built, catches 18/18, and
the 18 selectors were repaired on Dave's nod — including `Sidebar-nav`, which `ds-005`'s own fence
guards against being "fixed". What it surfaced is now his: `canon.css` carries **48 of its own**,
because the `.cn-` absorb prefixer is not specificity-preserving and inflates trim `(0,1,2)→(0,3,2)`
against an override's `+1 class` — **a repair that wins in a snippet loses in canon**. G2, the
`--computed` render leg, is priced-not-built and is the only thing that would prove the feature
rather than the clause.

**LIBRARY v2** shipped with a true header, search + 68 aliases + cmd-K, level facet chips at a config
swap point and 135 components, plus a `#chrome=0` embed mode added to `gen_showroom.py` as an
**opt-OUT** so REVIEW-213 keeps its pins. Driving it produced its own findings, named not repaired:
side-nav `aria-current` is authored static, and **46 of 135 snippets ship no behaviour JS**.

## The resolved state, and what is still open

**Resolved:** the band exists and is conditioned; the wall is re-confirmed; the probe exists, is
mutation-proven and has real data; the advisory re-derivation is ruled but staged; both gauge
instruments exist; the boot-reduction pair is enacted; the itinerary shortcut and the descender
specificity class are fixed with gates behind them.

**Open, and most of it is Dave's:** the REVIEW-213 tranche plan · the `canon.css` 48-selector class ·
the level word-set and whether LIBRARY v2 replaces `showroom/index.html` · row-124 scope and the 27
off-ratchet snippets · `ds-005`'s missing rulings-store row · `P8` · the stop-line / wall / boot-band
re-base sitting, which now has its priced boot-reduction option in hand · and the
self-contained-snippet vs shared-core architecture question, surfaced in chat and homed at this
wrap because it had no repo home at all.

**And one that stopped being deferrable.** The `W-` id stopgap ran past `z` into two-letter suffixes,
and the store gate now **FAILS**: eight refused ids (`W-99za`…`W-99zh`) plus two unresolvable homes.
The scheme-widening call has been Dave's for two sessions; every row minted while it waits is a row
that fails its own gate. It is no longer a preference — it is a red.
