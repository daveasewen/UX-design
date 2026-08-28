# #221 — the repair wave: the #220 audit findings enacted, six lanes

provenance: 0e8349e6-c419-479b-91b7-cb694b8b036b · 2026-08-28
status: observed

*Spine entry: `GOOD-MORNING.md` ★ LATEST #221 · `_LIVE-STATE.md` ⏱ LATEST delta #221.
Ledger: no ruling was inscribed this session — `knowledge/_rulings.json` carries no `s221-*` id,
read at this wrap. Commit: `2d375c6`. Filed reports: `notes/_subreports/2026-08-27-221-lane{A,B,C,D}.md`
· `-verify.md` · `-mono-specimen.md`. Divvy: `notes/_briefs/2026-08-27-221-repair-wave-divvy.md`.*

---

## Why this session existed at all

#220 spent its last hours doing something the project had not done before: **driving its own
machinery instead of reading it.** Six audit lanes ran the gates rather than trusting their
banners, and the result was uncomfortable — CI red at its first step for two sessions, eight
false greens, a BLOCKING gate with no reachable FAIL path, four things blocking a designer's
first hour in a pack we had already shipped. #220 repaired **none** of it, deliberately: the
wrap fenced every finding as a next-session lane so that the audit's own credibility did not
depend on the auditor also being the surgeon.

So #221 opened with an unusually clean brief — a findings list with receipts, and nothing to
discover. The interesting part turned out not to be the repairs. It was **what the brief got
wrong**, and what a gate did on its first day alive.

---

## Finding 1 — the divvy brief carried two stale premises, and Lane D found them

The conductor cut the four-lane divvy from the #220 audit reports and from chain carries. That
is the normal, cheap move. It is also exactly the move
[[premise-ages-faster-than-rule]] warns about, and this time the warning was earned twice over.

**Lane D replayed all six of its items at HEAD before touching anything — and four of the six
were ALREADY BUILT**, at #218's gates wave and #211's `W-92` lane. One of the four had been
built *because the same brief text was handed to that session too*: the #221 divvy re-issued the
#218 gates-wave brief nearly verbatim without replaying it. Only one of six (the regen-serial
check) had never existed.

The second stale premise was smaller and the same shape: the divvy's GLOBAL PITFALLS section
warned about a capture-gate write-door that was **FALSE at HEAD** — closed at #218, with
`--build` made the sole writer.

**What this costs, and why it is filed as the conductor's miss rather than Lane D's win.** A lane
that spends its first third disproving its own brief is a lane that did not spend that third
repairing anything. Lane D's report says so plainly, and it is right to. The general lesson is
not "check your premises" — everyone already says that. It is narrower and more actionable:
**a brief assembled from carries inherits the carries' age, and a carry's age is invisible
inside the brief.** The age brackets exist on banners for precisely this reason and the divvy
had none.

This is digested at the #222 opener rather than ruled here.

## Finding 2 — an instrument with a consumer on day one

Lane B built `knowledge/_render/_gate_fallback_drift_221.py`: every `var(--token,#literal)`
fallback in the generator glob, checked against what canon actually answers for that token.
ADVISORY at birth, like the other four.

It then **fired in-session, on a file that did not exist when it was written.** The mono-specimen
lane created `knowledge/_render/gen_mono_gallery_221.py` mid-verification; the verifier ran the
new gate against the new file and got `rc=1`:

```
⛔ DRIFTED knowledge/_render/gen_mono_gallery_221.py ::
   var(--surface-subtle,#F3F3F3) — canon answers #1F1F1F, #2A2621, #DFDEDC, #F0F0F0
```

`#F3F3F3` was the exact stale fallback value that same wave had just repaired across seven other
generators. The conductor re-derived the correct value (`#F0F0F0`), regenerated the page, and the
gate went green — verified again at this wrap, `0 drifted`.

**Why this is worth a dossier paragraph.** The standing complaint in this repo is
[[instrument-without-a-consumer]] — gates that are built, declared, and never cross a real
input, so they cannot fail and therefore cannot be trusted. This one crossed a real input within
hours of birth, caught a defect a human had just re-introduced by hand, and the repair was a
re-derivation rather than a typed constant. That is the whole argument for advisory-at-birth
instruments made concrete: it reported, a human read it, and nothing was blocked to get there.

## Finding 3 — the verifier's single red is a report defect, not an instrument defect

The adversarial verifier re-drove every `REPLAY-THESE` item in all four lane reports at the same
HEAD each lane measured (`9dbf413`): **82 green · 1 red · 9 could-not-run**, all four cross-lane
seams green.

The one red is worth naming precisely because of what it is *not*. Lane D's replay prose says
"flip each tier and expect 1 each"; measured, `REGEN_SERIAL_BLOCKING=True` produces 1 failure as
claimed, but `SHARED_HELPER_BLOCKING=True` produces **3** — and all three are coherent tier-pin
arms. **The instrument is stricter than its own description.** The defect is the report's
expected figure; both directions still hold (flip fires, restore clears).

The nine could-not-runs are graded COULD-NOT-RUN and never green — CI read-back (`gh` absent),
the `_build_all.py` step (fenced), playwright legs, a live VS Code bridge. An honest
could-not-run is the point of an adversarial seat; a seat that converts them to passes is worse
than no seat.

## Finding 4 — Dave's conditional was a conditional, and both halves were true

His sentence, verbatim: *"there are no rounded corners in mono but I think they share the same
neutral ramp so the colours can be the same if this is true."*

Two factual premises, and the specimen lane checked both rather than acting on the conclusion:
neutral/5 resolves `#313131` **byte-identical** in mono and console; mono's
`--border-radius-container` resolves **0 in both modes**, console's 20px being the `#199`
override. Both TRUE at HEAD, computed by the page's own chips rather than typed into it.

`reviews/MONO-GALLERY-DEFAULT-2026-08-27-v1.html` shows console's ruled default beside the mono
candidate beside mono today, light and dark. **Nothing was ruled.** `s220-D2` left mono expressly
open and it stays open — `knowledge/_rulings.json` carries no `s221-D1`, read at this wrap and
not assumed.

The discipline here is the one from [[feedback-mock-the-readings-before-building]]: a conditional
sentence from Dave is a *question with a testable premise*, not an instruction. Verifying the
premise and drawing the candidate costs one lane; guessing the conclusion costs a day.

## Finding 5 — three things in the fork table are Dave's eye, and one of them the law does not name

Lane B's fork triage surfaced **29 real-defect candidates**, quoted with `file:line`. Three are
flagged for Dave specifically and none were touched:

1. **`--err` carries a THIRD red.** `:root` resolves `#f6604c`; `.cn-notifications` declares
   `#a8000b`. `s151-D1` names `#DA1A00` and `#F6604C` and **only** those. `#a8000b` is neither —
   so the two-red law does not name it, and a lane may not name it either.
2. **`--ter-border` supercharge resolves `#000000`** — pure black, against the standing
   *blackest, not pure black* ink rule.
3. **`--pri` is a vocabulary collision**, not a colour fork: a hex in one scope, `50%` in
   another. [[vocabulary-collision-switch-202]]

The classifier declares its own blind spot — it reads `declared`/`resolved` from the gate's JSON
and does not model selector specificity, so "different scope" is a *string* distinction. Declared,
not smoothed.

## Finding 6 — the gauge crossing was declared BEFORE it happened

#220's recorded miss was a **silent** crossing: the conductor went past the armed ~190,000
advisory mid-bake and named it late, when Dave asked "how hot". The correction was written into
#220's own banner as pitfall (d).

This session enacted the remedy. FILL crossed the armed 190,000 advisory and the 200,000 working
line during the commit train, and the crossing was **DECLARED IN CHAT BEFORE IT HAPPENED**. The
~15M platform window made it safe; that is evidence FOR the pending `s208-D1` re-base and has
never been a licence.

Boot measured **69,692 real** — out of the `s208-D1` band (55,595–57,903) by **11,789**, the
**ELEVENTH consecutive** out-of-band reading, declared at the opener and logged once. Eleven
consecutive readings is no longer drift; it is a constant describing a seat that no longer
exists. The re-base is Dave's, and his own rider binds: it arrives with a **boot-REDUCTION**
option priced beside it.

---

## Where it landed, and what is still open

The whole wave is **one reconciled commit, `2d375c6`** — the repairs, the five new advisory
instruments, the six filed reports, twelve store rows `W-227`…`W-238`.

**Still open, and every one of them is Dave's or a next lane's:** mono's one word · his eye on
the mono candidate page · the 97 open sitting calls and 25 candidates, unchanged · the
`s208-D1` re-base · the 29 fork candidates and the third red · Lane C's F9 handoff
(`apollo-spider/gumdrop/_state.py` is a byte-identical twin of `knowledge/_state.py` with no
comparing gate) · Lane A's residual CI causes, two of them ruling-shaped · the CI read-back
queue, still blocked at Dave's GitHub sign-in · the five advisory instruments' promote-or-park.

**Nothing was ruled at this session.** No constant, band, advisory, stop line, wall or lane was
moved, and no row of Dave's was closed, reworded or re-scoped.
