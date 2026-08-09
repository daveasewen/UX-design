# #136 — the three-axis model: Dave's bemusement becomes the fork-ban ruling

```
provenance: wrap-sub #136 · 2026-08-09
status: ruled (pointer: knowledge/_rulings.json § s136-D1)
```

Spine entry: `_LIVE-STATE.md` § ⏱ LATEST DELTA (#136) · Banner: `GOOD-MORNING.md` ★ LATEST #136 ·
Ledger: `knowledge/_rulings.json` (`s136-D1`) · Predecessor arc:
`_DECISION-HISTORY/2026-08-08-135-*.md` (#135, not yet filed — the shell/hierarchy requirement,
`s135-D1`…`s135-D4`).

⚠ **Written by the wrap sub, one day after the session it records** (session ran 2026-08-08 Sat;
this capture ran 2026-08-09 Sun, per `date` — a scheduled dream-pass fire landed in between and is
recorded separately in `_LIVE-STATE.md`'s "Last refreshed" chain). Reconstructed from the
conductor's session facts and the ruled record, not from a transcript this sub read directly —
declared, not laundered as first-hand.

---

## Why this session existed

#135 closed with three research alignments FLOATED but not ruled — DTCG wire format, Figma-Slots
semantics for shells, and a fork-ban gate — plus Dave's 16 low-confidence tier-map rows still
awaiting his eye. #136 opened to put those alignments in front of Dave as an actual ruling
candidate, not as three separate asks.

## How the thinking moved

**Dave's bemusement, first.** The three floated items, presented as three separate questions,
didn't land as three separate questions to him — the shape of "how does a component vary" was the
real thing underneath all three, and he pushed back on being asked to rule fragments of one idea.

**Four-question decomposition.** The conductor broke "how does a component vary" into the four
questions that would later become the ruling's four clauses: where do raw values live (parameters),
what happens when a node needs a different look (variants), how does content get into a
container (slots), and is there anything outside those three (the fork question).

**Three-axis synthesis.** The answer to all four turned out to be one model, not four separate
rules: every node — atom, molecule, organ, shell — flexes on exactly three orthogonal axes, and
nothing legitimate happens off those three axes. This reframed the #135 floated items as
consequences of the model rather than as separate open questions:
- DTCG wire format becomes the answer to "how is a parameter's spine binding written down" (axis A).
- Figma-Slots semantics for shells becomes the definition of axis C directly — a shell is just
  "any node with ≥1 slot."
- The fork-ban gate becomes axis D — not a new idea, but the model's own boundary stated as a rule.

**Ruled whole, via controller export.** Dave ruled all four clauses together off
`reviews/RULING-CANDIDATE-three-axis-2026-08-08-s136-v1.html`, exporting his verdicts verbatim to
`reviews/THREE-AXIS-VERDICTS-2026-08-08-s136.json` — no amendments to any clause. This is `s136-D1`
in `knowledge/_rulings.json`, status **RULED NOT ENACTED**.

**The demo, and why it's worth keeping.** `reviews/THREE-AXIS-DEMO-2026-08-08-s136-v1.html` was
built as a live, interactive walkthrough of the mechanism (parameters/variants/slots, manipulable)
rather than a static explainer. Dave's own words: visuals help him embed concepts. This is recorded
as a pattern to reuse for future ruling candidates, not a one-off nicety.

**#67-D2 reconciliation — a loose end, closed as inferred, not ruled.** The conductor's analysis
was that #67-D2 (title = mandatory slot content, composite-typed) sits consistently alongside
`s136-D1` with no disruption. Dave said "cool" to this — read as agreement in direction, but this
is explicitly **not** a ruling with the same weight as `s136-D1`, because "cool" was not put to him
as an export or a firm readback. Status: **inferred/agreed direction, not ruled.**

## What's ruled vs what's floated (do not conflate the two)

| item | status |
|---|---|
| `s136-D1` — the three-axis model, all four clauses | **RULED**, `knowledge/_rulings.json` § `s136-D1` |
| #67-D2 reconciliation (title = mandatory slot content) | **inferred/agreed**, not ruled — Dave said "cool," not exported/confirmed |
| Clause-A copy refinement (text params vs labels vs body-copy-as-slot-content) | **FLOATED**, conductor offered to record it, Dave never said yes — readback owed #137 |
| The 16 tier-map rows | **ALL OPEN**, parked to #137 — Dave ruled none of them; controller built and ready |
| Mono no-border extension (carried from #134/#135) | **still FLOATED**, untouched this session, readback owed |

## What's still open

Enactment of `s136-D1` is unstarted: the slots-key rollout in `meta.json`, a `props.binds` audit
across the existing corpus, a DTCG re-encode of the token spine, and building the fork-ban gate
itself. These four are #137's first-build-lane candidates, named on the #136 banner's residual line.

The 16 tier-map rows have a controller built and render-verified
(`reviews/TIER-MAP-CONTROLLER-2026-08-08-s136-v1.html`), but nothing about them is decided — that
controller's export is the mechanism, not a substitute for Dave actually using it.

## Session mechanics, for the record

Boot 55,057 real — another datapoint inside the ruled 54,859±1,178 band, never corrected into it.
FILL at the last mid-lane check-in was 124,287; the wrap opened around 145K against the stop line
150,929 — below the line. No build subs ran this session; the wrap sub was the only delegation.
Quota panel was asked for at the opener and not given by Dave this session — recorded as unpolled,
not assumed comfortable.

One process finding worth keeping: the conductor's own probe first reported "28 flagged rows" for
the tier-map controller, which turned out to be a regex artefact — it was matching the substring
"low" inside "flow" in pattern ids. The re-verified, correct count is 16. Filed as a live instance
of [[unmatched-grep-is-not-an-absence]] / a matched-probe-is-not-a-measurement class: the first
count looked authoritative and was wrong.

A second, smaller finding: a sandbox drive-test click on the tier-map controller does **not**
pre-populate Dave's own browser's localStorage — picks are per-browser, live. Recorded so a future
session doesn't assume the controller is pre-seeded from sandbox testing.
