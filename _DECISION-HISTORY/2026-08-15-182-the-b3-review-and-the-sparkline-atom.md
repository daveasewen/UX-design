# #182 — the B3 grades review settled, the sparkline reduced to an atom, and a false claim caught

provenance: 182 · 2026-08-15
status: observed

*Companion record to `GOOD-MORNING.md`'s ★ LATEST banner for #182 and `_LIVE-STATE.md`'s ⏱ LATEST
delta. The banner holds the WHAT; this file holds the WHY and HOW. ⚠ Every gauge figure, every Dave
quotation and every build receipt below is **RELAYED by the conductor** — this dossier was written by
the delegated wrap sub, which cannot measure the conductor's window or read its transcript, and did
not run the builds it records.*

---

## 0. The shape of the session

The #181 handoff pointed at one thing — the B3 grades review, held over on arithmetic — and #182 did
it first, then spent the rest of the window on DV-J2b, the sparkline. Three rulings came out of it
(`s182-D1`, `s182-D2`, `s182-D3`), all inscribed **in-window by the conductor** via
`knowledge/_inscribe_ruling.py`, all read and quoted (never paraphrased) by this wrap.

The most interesting thing that happened, though, was neither of those lanes. It was a **correction to
our own record**, and it is written first here because it is the part with a general lesson.

---

## 1. The finding: "the Monday dream-pass slot is RULED BUT STILL UNSCHEDULED" was FALSE

The #181 banner carried, in bold, that the weekly dream-pass slot had been *"offered TWICE now and
answered neither time; an unanswered offer is not a licence, so NOTHING was scheduled"* — and drew a
consequence from it, that `s179-D1`'s return-with-numbers window had therefore never opened.

Dave caught it. The scheduler was then listed live (`list_scheduled_tasks`) and it says:
**`memento-dream-pass`, Sundays 07:10, ENABLED, lastRun 2026-08-15 07:13, nextRun 2026-08-16.** The
task exists, it is enabled, and it has already run. Dave had also run a manual pass on 08-15.

**Why the false claim survived two sessions.** Every other "is this real?" claim in this project has a
verification habit attached to it: a repo claim is checked against `git log` or a real run, a ruling is
checked against `_rulings.json`, a build is checked against a gate's exit code. A claim about the
**scheduler** had no such habit, so it was carried the way beliefs are carried — repeated verbatim from
the previous banner, growing more confident with each repetition, and used to derive a second claim (the
unopened counting window) which was also false. This is the [[assertion-propagation-gap]] class in its
purest form: nothing could chase it because nothing was ever true-then-false; it was simply never
checked.

**The class rule Dave and the conductor stated in chat, and the reason it is here rather than only on a
rolling banner:** *any claim that something is UNSCHEDULED must cite a scheduler-list run, exactly as a
repo claim cites `git log`.* An unrun `list_scheduled_tasks` is indistinguishable from an absent
schedule [[unrun-search-indistinguishable-from-absent-record]]. The conductor corrected the memory hook
in-window (`borrowed-instruments-brief.md`), and the correction is inscribed into `s182-D1`'s own
evidence array rather than left on a banner that will roll.

---

## 2. `s182-D1` — the B3 grades review: four calls, one of them reopened and amended live

The review ran off a deck, `_REVIEW-B3-grades-2026-08-15-v1.html`, built to the standing pattern:
**the page writes nothing**, it compiles taps into one paste-able ruling message which Dave pastes
back. He pasted all four picks, and then did the thing that makes review pages worth building — he
**reopened call 1**, saying it might be wrong.

Call 1 as first ruled was "commission more probe kinds". The alternatives were put to him in full — an
authoring convention, expiry dates, triage down to the starred/blocked 49 — and he came back with
*"no i think you are right"*, landing on the **parked** shape instead. The ruled position:

- **UNPROVABLE is an honest register, not a defect.** 109 of 122 hooks grade UNPROVABLE because most
  hooks encode judgment, and judgment has no probeable token. Building probes to move that number would
  be building an instrument to flatter a statistic.
- **Commissioning is parked behind the first-cycle numbers.** No probes get built until the
  return-with-numbers shows grades actually changing retrieval decisions. If they earn their keep,
  commissioning is scoped to the **starred/blocked subset (49)**, never all 122.
- **In force immediately, and this is the half that costs nothing to adopt: the probe-shaped-hooks
  AUTHORING CONVENTION.** A new memory hook making a *mechanical* claim must carry the backticked path
  or quotable line that makes it probeable. Judgment-shaped hooks stay honestly UNPROVABLE.

Calls 2–4 needed no build: the **30-day AGING threshold stays an explicit placeholder** (picked, not
derived — derive it from cycle data); the **boot alert stands as built** (counts only, STALE listed by
name, measured surface 105 real per check-in and ~40 real per listed entry); and the
**return-with-numbers counting window opens at the first SCHEDULED pass, 2026-08-16 07:10** — the
08-15 manual pass explicitly does not count.

★ The shape worth keeping: **a park with a return condition, ratified against a measurement that was
allowed to stay uncomfortable.** Nothing was built to make 109/122 look better.

---

## 3. `s182-D2` — the sparkline is an atom, alone

DV-J2b was picked up by the first build sub, which immediately found something the lane receipt did not
say: **the markup and CSS already existed and had since before #116.** The lane receipt was STALE. The
sub added a table-hook `extraContract`, refused four mutations, and render-proved the result.

Then Dave looked at the render proofs, and ruled in three beats, each a refinement of the last:

1. *"this doesn't need a title as it will usually live in a card"*
2. *"this is just an atom"* — it lives in a card slot or a standard card design; composition is built
   later from slot + atoms
3. final form: *"the sparkline is an atom alone, the table cta can be optional in the trend card
   component"*

So the second sub **stripped** what the first had built: the `<details>` table disclosure went entirely
— markup, CSS, and the `extraContract` added an hour earlier. Snippet 29,836 → 29,056 B. The table
affordance survives as an **optional element of a future trend-card component**, and when built it takes
the **icon-button** form, not a "View as table" label — his reasoning being that a sparkline sits beside
a headline figure, it is not an analysis tool, so no label in most cases (the accessible name survives
as `aria-label`).

⬛ **FLOATED, NOT RULED, and it must never be laundered:** the trend-card component itself. His words
were *"might be a partially built trend card with option, I haven't decided yet"*
[[feedback-dont-launder-a-premise-into-a-ruling]].

**The machinery this produced, which is the durable half.** Stripping a mandatory partial out of a
component is exactly the kind of edit that should not be quietly possible. So the sub added a
**`markupExempt` clause to `gen_component_partials.py`** (+25 lines): a mandatory partial may be absent
**only by named-reason exemption**. Four drives were refused by it. ⚠ **Declared gap, honestly:** the
clause has **no durable selftest bite** — it was driven, it refused, and nothing in the gate chain will
notice if it stops refusing tomorrow [[instrument-without-a-consumer]].

---

## 4. `s182-D3` — the stroke is semantic, and the picker died of it

The tuner had been built (v1) with a **37-chip colour picker**, on the assumption that the sparkline
stroke was a pick from the series ramp. Dave's ruling deleted the question rather than answering it:
*"the rules for colours should just follow the red and green ink colours for all themes."* Read back,
confirmed: *"the read-back is correct."*

So the stroke derives from **trend direction + background**, never from a ramp pick:

- **down** = the ruled red ink, background-keyed per the two-red law `s151-D1` — `#DA1A00` on white,
  `#F6604C` else
- **up** = the green that mirrors it, `s155-D1` — `#137F3C` / `#66CC8D`
- **flat/neutral**, verbatim: *"the default ink near-black colours are fine for the neutrals, white on
  dark"* — `#1A1A1A` on light, white on dark

Identical keying across all four themes, and that generalisation is a **measurement, not an assumption**:
the sub checked all three theme override files and found **zero data/series entries**, so per-theme
keying reduces to background keying.

⛔ **No value was minted anywhere.** Every ink named is already ruled. The consequence for the tuner was
that its headline feature became moot: v2 (31,509 B) **removes the picker entirely** and renders the
semantic strokes live in both directions, leaving **scaling as the only open decision**.

⚠ **And there is a scope collision, which is Dave's to reconcile, not this wrap's:** `s151-D1` and
`s149-D1` are inscribed **MONO ONLY**, and `s182-D3` keys the same inks across **all four themes**.
Both readings are defensible from the text. It is carried as an open item, unresolved, deliberately.

---

## 5. The finding inside the build: which gate actually caught the two-red mutation

The third sub mutated the two-red law inside the sparkline stroke and expected `dv-016` to catch it. It
did not. **`_validate_snippets` caught it — via manifest drift**, not via a colour rule.

That distinction matters more than the green does. The mutation was caught because the snippet no longer
matched its manifest, i.e. by an accounting check, not by a semantic one. **A semantic stroke with no
manifest binding would be unguarded** — which is a real gate-gap, and it is **declared and NOT built**,
per `s172-D3`'s observed-failure rule: the finding gets written down, the instrument does not get built
in the same breath [[green-tests-cannot-see-scope]].

Type debt moved 1,101 → 1,099 in passing, and the ratchet **rewrote `_type_ratchet.json` wholesale** as
a machine reformat — declared here so a reader of the diff does not read intent into whitespace
[[serializer-defaults-reformat-the-file]].

---

## 6. Where this leaves things

**Settled:** the four B3 calls; the sparkline atom's shape; the sparkline stroke rule; the false
"unscheduled" claim, corrected at its source and in a ruling's evidence array.

**Open, and Dave's:** the **scaling** decision at tuner v2 (the natural #183 opener) · the **MONO-ONLY
scope rider** reconciliation between `s151-D1`/`s149-D1` and `s182-D3` · the **trend card**, floated
only.

**Open, and ours, declared not built:** the `markupExempt` clause's missing selftest bite · the
unguarded semantic-stroke/manifest-binding gap · the dormant `dv-behaviour` table module now sitting in
canon with no consumer (culling it is canon-level blast radius) · a pre-existing dashoffset/endpoint
render artefact, attributed with a control and **not** a regression from this session's work.

Both-way links: `GOOD-MORNING.md` ★ LATEST #182 · `_LIVE-STATE.md` ⏱ LATEST delta #182 ·
`knowledge/_rulings.json` § `s182-D1` / `s182-D2` / `s182-D3`.
