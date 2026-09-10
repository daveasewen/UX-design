# #266 — the KG explorer, born and iterated eight times in one day, and the pivot to the demo

```
provenance: 266 · 2026-09-10
status: observed
```

*The WHY and HOW of 2026-09-10. The WHAT lives on `GOOD-MORNING.md`'s ★ LATEST #266 banner, in
`_LIVE-STATE.md`'s ⏱ LATEST DELTA, in the twelve commits `f277431..6d3b61e`, and in the four lane
reports `notes/_lanes/2026-09-10-266-{T,K,R,V}-*.md`. Both-way links: the banner and the delta name
this file; this file names them. ⛔ **NOTHING HERE IS A RULING.** Dave ruled nothing today in the
`_rulings.json` sense — the store stands at 441 entries, unchanged since #265.*

---

## 1 — The session opened on a carry and Dave took it off the table in one sentence

#265 handed forward, as its proposed lead, the four ungraded `-active` glyphs (balance-transfer,
tax, workspace, digital-statements) sitting on `notes/_REVIEW-264-active-glyphs-2.html`, plus
`global-money`, which the #264 second pass proved is one connected ink piece and therefore a drawing
problem rather than a derivation one.

Dave's answer, verbatim: ***"forget about these for now the glyph work is for another time when I
have capacity, our focus is Apollo and the demo/presentation"***.

⚠ **The distinction that matters for the record: this is a PARK, not a ruling and not a strike.**
Nothing about the four glyphs was decided — they are still ungraded, the review page is still live,
and `global-money` still needs drawing. What changed is priority, by his word, and the carry moves
forward marked PARKED with his sentence attached. A carry that is silently dropped and a carry that
is parked by name look identical one session later, which is why the sentence is inscribed here and
on the carry rather than summarised as "deprioritised".

## 2 — The demo brief, in his words, because a paraphrase would lose the shape

The whole day turned on this. The audience is **David Rice, HSBC's Chief AI Officer**
(`notes/_DEMO-PREP-david-rice-hsbc.html`; ⚠ the #257 hook is the standing correction that this
audience is Rice and NOT "Sutherland", which is a React library). Length **15–20 minutes**. Five
beats, his numbering:

1. intro
2. goal, practical benefits, predicted KPIs — ***"compressing a 6 month project into N weeks"***
3. run the demo; the dead-air talk while it builds is *what inspired the idea* and *how it developed*
4. a simplified explanation of the system — ***"he will be very interested in the KG"***
5. ambition, requirements, and the sponsorship ask

On format: ***"no deck as such… slides but not much words. Diagrams, animated and interactive,
KPIs"***. On provenance: ***"We have a lot of docs and a few presentations… we should trawl through
analyse them… create a timeline"***. And the framing device is his own, not the repo's — a car
plant and a gearbox; it appears nowhere in the corpus, so it is recorded here as HIS.

⛔ **His N is not a number yet.** *"a 6 month project into N weeks"* is carried with the N unfilled.
Inventing one would be a fabricated KPI in the one artefact a CAIO is most likely to test.

## 3 — Three research lanes, because the brief asked three separate questions

Run as Opus lanes, read-only, filed in `notes/_lanes/` (the #260 home for lane fragments, not
`knowledge/_tmp/`):

- **T — the evolution timeline** (`2026-09-10-266-T-timeline-trawl.md`). The trawl he asked for:
  what exists in docs and decks, and what a timeline built from them would say.
- **K — the KG diagram and the decks** (`2026-09-10-266-K-kg-and-decks.md`). Its central finding is
  an absence, and the absence is why the day went the way it did: **the only prior picture of a
  knowledge graph in this repo is the July compliance diagram; the component KG has never been
  drawn at all.** Its recommendation was a new, self-contained page rather than a slide.
- **R — how good is v1.0.9 for Friday** (`2026-09-10-266-R-v109-rating.md`). Verdict
  **SHIP-WITH-CAVEAT**: every release gate that exists passes at HEAD, and the missing thing is not
  a gate — **the frozen prompt has never been driven against v1.0.9**. Its recommendation is a
  sixth cold run before the Friday decision, keeping the two live defects (F01/F02) off camera and
  demoing in the light theme.

⚠ **R's verdict is a recommendation and remains one.** Whether v1.0.9 is cut without that cold run
is Dave's, and it is carried unruled.

## 4 — The plot points: accepted in principle, and that is exactly as far as it went

Twelve slides, roughly eighteen minutes, proposed in chat against his five beats. He accepted the
shape in principle. ⛔ **No run-of-show page was written**, so there is no script, no per-slide
timing, and no dead-air script — the thing that would actually be used on Friday does not exist
yet. It is #267's second item, and it is named as NOT DONE rather than as accepted-and-therefore-
handled, because "accepted in principle" is the state most likely to be misread next session as
finished.

## 5 — The KG explorer: born at 08:37, eight versions by 13:19

This was not planned. Lane K's finding — *the component KG has never been drawn* — turned beat 4 of
the demo from a slide problem into a build problem, and the build ran all day:

| v | commit | what changed, and why |
|---|---|---|
| 1.0 | `f277431` | born: `knowledge/_build_kg_explorer.py` + `knowledge/_kg_explorer.template.html` → `notes/_KG-EXPLORER.html`. Sector dig, 3D, path, orphans and islands. |
| 1.1 | `06d5724` | the scrub line: `knowledge/_kg_history.py` + `_kg_history.json` — **51 daily snapshots, 2026-05-31 → 2026-09-09**, taken with `git archive` and the SAME `extract()` the live build uses, so the past and the present are measured by one instrument rather than two. |
| 1.2 | `a745004`, `7a78f62` (lane V report), `12808fd` (polish) | governance and guidelines layers, added as two chip-gated families. The polish is the interesting half: the layers now **load OFF**, so the page still opens as v1.1 — and a 43-label slug fix. Two follow-ups moved the scrub line under the legend (`db88a78`, `92ed3bf`) once three chip rows overlapped it. |
| 1.3 | `05d6097` | spin re-arm, theme toggle, search fly-to, edge grow. A drag-release had been killing the frame loop; `mouseup` + `visibilitychange` re-arm it. |
| 1.4 | `80266f8` | **THE STALL, FOUND AND MEASURED.** A node passing behind the 3D camera produced a radius that made `arc()` throw, and the exception killed the frame loop — so the symptom was "the spin stops", several layers away from the cause. |
| 1.5 | `f9fe342` | depth of field: five depth bands, 3D only, off by default. |
| 1.6 | `9ee4fb7` | Depth → Macro cycle, cross-fade bands, sharp halo. |
| 1.7 / 1.8 | `6d3b61e` | **the vanishing dots.** Two causes, both measured: label plates and halos were painting over neighbouring dots, so halo dots now draw above labels; and the 3D halo was a **sphere**, so neighbours in line with the camera hid behind the focus — it is now a **ring in the camera plane** that turns with the camera. A sweep over 24 angles × 3 digs took wrong-colour centres from **46/672 → 25/672**. |

★ **The method that made this fast is worth keeping: every fix was driven and swept, not eyeballed.**
The v1.8 commit message carries its own before/after counts. ⚠ **And the two imperfections that
remain are declared rather than smoothed:** the residual 25/672 are dense-fan dot-on-dot overlaps
(the Button dig), and the depth-of-field edge born-dates are approximate.

## 6 — What the graph actually measures, and one disagreement named rather than averaged

Re-running `knowledge/_build_kg_explorer.py` at HEAD `6d3b61e` prints:

```
base (live): 889 nodes / 1176 relations / 137 components
extra: 1882 nodes / 3530 edges · mentions 284 derived · appliesTo matched 826 unmatched 0
whole page: nodes 2780 · edges 4828 · islands 8 · orphans 2 · snaps 51
proposedType: corrects 5 · retires 13 · supersedes 14 · extends 8 · enacts 12 · refines 3 ·
              confirms 8 · overrides 12 · narrows 3   (= 78)
```

⚠ **The conductor's wrap brief carried 1,261 relations and 2,771 / 4,791 for the layered figures;
the generator re-run at HEAD reads 1,176 and 2,780 / 4,828. Both readings are named and no third
number is invented** [[measure-dont-convert-units]] — the generator's own output at HEAD is what
this record leads with, because it is the one that can be re-taken with a single command. 441
rulings, 38 SCs and 826 matched `appliesTo` with **0 unmatched** are the figures both agree on.

Two findings fell out of the build and neither is repaired:

- **Two orphans** — `pattern:site-end-matter` and `pattern:utility-navigation` — are **stale
  registrations left by Footer's #261 redesign**. ⛔ The registry is addition-only; removing a
  registration is Dave's.
- **Eight islands**: Document row (10), Secure entry (9), Hero variants (8), Rating (7), auth
  template (7), Transfer list (7), Command palette (6), Anchor nav (6). Wiring them is a lane's
  work and is carried, not done.
- **78 derived `mentions` carry a `proposedType`** and are published for ratification at
  `notes/_PROPOSED-266-ruling-edges.html`. ⛔ **Proposed, not applied** — the edge types are Dave's
  to ratify, and the page exists precisely so that a generator's guess cannot become a fact by
  sitting in a graph unchallenged.

## 7 — The defect the day ended on, and why nothing was fixed

Dave, last: ***"now 3d is broken when we dig deeper"***. The conductor's headless probe — search →
follow → Depth 2 → follow — **reproduced nothing**. ⛔ **That is not evidence the defect does not
exist**; it is evidence the probe did not hit it. The honest next step is his screenshot at #267's
opener, and the defect is carried as OPEN with the failed reproduction attached so the next seat
does not re-run the same probe and read its silence as a pass [[unmatched-grep-is-not-an-absence]].

## 8 — The gauge, recorded plainly because it is a breach

**FILL 304,364 real at the wrap call** — past the `s260-D2` delegated line of 180,000 **and past the
200,000 working wall**. ⛔ **This is a BREACH and it is written as one.** The cause is measurable
rather than mysterious: **131 turns at roughly 2K each**, a visual-iteration loop (render, look,
adjust) whose per-turn cost is small enough that no single turn ever looked like the moment to stop.
★ **The lesson is the shape, not the number: a loop of cheap turns hides a breach from the very
instrument that would catch an expensive one.** `_checkin.py` at every seam is the standing rule and
it was not what failed — the loop simply never presented a seam.

**Boot 70,442 real** — 442 over the 70,000 shrink-only literal, and the **second consecutive
breach** after #265's 70,260. The literal does not move (`s240-D2` / `s241-D1`), so the commit is
made in the #243 form rather than the gate being routed around.

**Sub spend is PARTIAL and therefore no `subs` line is written.** Lane K measured 127,207 and lane V
175,198; lanes T and R were not captured by the conductor, and this wrap seat cannot read its own
spend. ⛔ A total across two measured and two unknown lanes would be a number pretending to be a
measurement, and the gauge-log contract says absence is legal while a wrong figure is not
[[feedback-measuring-tool-must-not-guess]].

## 9 — Resolved state, and what is still open

**Resolved:** the KG has a picture, and it is interactive, historical and self-contained — the thing
lane K said did not exist. Twelve commits, all pushed. Dave's own reactions are on the record
because they are the acceptance test that matters for a demo artefact: ***"this is pretty
awsome"*** · ***"this is fucking awesome!... you have outdone yourself"*** · ***"Honestly every
presentation and demo I give this is the show-stopper usually"*** · ***"I really really love
this"***.

**Open, all his:** the 3D dig defect (his screenshot first) · the run-of-show page · whether v1.0.9
is cut without a sixth cold run · the 78 proposed edge types · the two orphan registrations · the 8
islands · the four parked glyphs and `global-money` · the thirteen #265 lane RSQs ·
`DECLARED_EDGE_TYPES` · the two `_PROPOSED-263.html` defects · #241's midnight-wrap question · his
own N in *"a 6 month project into N weeks"* · and whether `_build_kg_explorer.py` and
`_kg_history.py` join the capture ritual.
