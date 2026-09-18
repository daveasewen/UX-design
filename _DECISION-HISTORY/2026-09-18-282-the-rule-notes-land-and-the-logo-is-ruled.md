# #282 — the rule notes land, the logo is ruled, and the graph's philosophy is put

provenance: 282 · 2026-09-18
status: observed

*The WHY and HOW of session #282. The WHAT lives in `knowledge/_rulings.json` §§ `s282-D1`…`s282-D6`,
in `_LIVE-STATE.md`'s ⏱ LATEST DELTA for #282, and on `GOOD-MORNING.md`'s ★ LATEST banner; this file
holds the arc those three cannot carry — the dead ends, the corrections, and the two ideas Dave liked
that are deliberately NOT rulings.*

**Both-way links.** Spine: `_LIVE-STATE.md` § ⏱ LATEST DELTA — 2026-09-18 (#282). Ledger:
`knowledge/_rulings.json` §§ `s282-D1`…`s282-D6`. Handoff:
`_HANDOFF-133-the-rule-notes-land-and-the-logo-is-ruled.md`. His words:
`notes/_lanes/282/DAVE-RULINGS-2026-09-17.md`. Filed reports:
`notes/_subreports/2026-09-17-282-RN-rule-notes-land.md` ·
`notes/_subreports/2026-09-17-282-LR-logo-review.md` ·
`notes/_subreports/2026-09-18-282-LL-logo-land.md` · this wrap's own
`notes/_subreports/2026-09-18-282-W-wrap.md`.

---

## 1. The session opened owing fifteen answers and closed having asked for fifteen more

#281 ended by filing Dave's fifteen notes about the rules rather than enacting them, on the strength
of its own last ruling (`s281-D6`: *a rule NOTE is not a rule EDIT*). That is a restraint with a
cost — it leaves fifteen questions sitting in a dated file where nobody reads them — and #282's first
move was the method that has now worked three days running: **turn the file into a page with a
recommendation on every row, and take the answer whole.**

The page (`notes/_lanes/282/rule-notes/RULE-NOTES-2026-09-17.html`, conductor `256e4cf`) carried, per
row, his note VERBATIM, the rule's stored text, a recommendation, and one sentence on what would
change if the recommendation were taken. His export came back at 19:10Z with **14 of 15 on the
recommendation**. Lane RN then enacted them as `s282-D1`: **eleven guideline edits in his own words
across eight files**, plus two second `restsOn` edges (73 → 75).

**The why that matters:** the eleven edits are his sentences, not paraphrases of them. `s281-D6` had
established that a note is not an edit; `s282-D1` establishes the other half — **a note BECOMES an
edit when he says so, and the edit carries his wording**. The two rulings are one mechanism read from
both ends.

**What did not land, and it is the interesting one.** `col26-012` came back *"Discuss first"* — the
single row of fifteen he did not take. It is not a rejection and it is not a deferral; it is him
asking for a conversation about a rule, which is exactly the shape `aid-009`'s *"too boolean"* note
took at #281. **Two rows in two sessions have now asked to talk about the rule rather than the link.**
That is a pattern about the rule corpus, not about the export mechanism, and it is carried to #283 as
his.

## 2. The eye-check was never open, and the record was wrong about whose item it was

The carry set and three consecutive handoffs said *"the eye-check of the six matrix cells is asked and
unanswered"*. At #282 Dave answered it with *"sorry I though this was settled"* — and he was right. It
**was** settled, by `s280-D1`, which gave him all six cells with force as the default. The conductor
had been carrying an expectation that one of the cells (Floors or Orbits) would be dropped on sight,
and had written that expectation into the record in the grammar of an open question.

**The lesson, and it is this session's about its own record: a carry that only the conductor wants is
not Dave's open item.** The carry survived three wraps because the EXIT CHECK tests PRESENCE — is the
item homed in a standing section? — and has no test for whether the item was ever his. `s271-D4`
already commands that an open item be written as **the question it is**; this is the sibling failure,
an item written as a question that was never asked. Closed at `6bac5e4`, `W-280lm` done, and struck in
`_CARRIES.md` and `knowledge/_REVIEW-SIGNOFF.md` with its receipt rather than deleted.

## 3. The logo review, parked since #277, was given — and two of its four rulings were wrong first

Dave had asked for the logo review by name twice. Lane LR built it (`4c536a3`): **12 lockups measured,
3 exporter defects named, 6 questions put**. His export at 08:20Z answered **9, left 3 moot, and
carried four notes**. Four rulings came out of it, and **two of them were corrected within one
commit**:

- **`s282-D3`** first cut the size scale at **32–56**. Corrected at `c143a1b` to **24 · 28 · 32 · 36 ·
  40**, by RAW HEIGHT and width. The first cut is **named inside the ruling** rather than erased.
- **`s282-D6`** first put horizontal clear space on the **lockup's** width. Corrected at `6df8b64` to
  the **LOGOMARK's** width, on the open side by alignment. Same treatment: the superseded cut is named
  in place.

**Why this is recorded as a finding and not as an embarrassment.** Both corrections show in
`git show --numstat` as `3  3` and `2  2` — the only two spans of the session with deletions in them,
and both are a ruling amending its own text. A record that hid the first cut would read as though the
answer arrived whole. It did not: it arrived, was shown to him, and moved. The amendment-in-place is
the honest form, and the numstat is the receipt.

**`s282-D4` is the one that removed work rather than adding it.** The identifier lockup was SCRAPPED —
eight variants, `_logo_nodes.json` 12 → 8 nodes, the files held in a gitignored `_to_delete/`
directory rather than deleted outright. **`s282-D5`** then landed the review as **ONE** guideline
(`logos.md`), with Apollo's decisions explicitly overriding the refresh, and bound the eight surviving
nodes: 27 → 33 edges. Lane LL widened `governedBy` from declared-null-only to do it and **declared
that widening as ruling-shaped and its own call** rather than burying it — the right instinct, and the
reason it is visible here.

## 4. The graph's philosophy was put, and the answer is an idea he liked — not a ruling

Two of Dave's sentences this session are the largest thing in it and **neither is inscribed**:

> *"what harm is there to an agent having the principle as guidance … make it the hyper-designer I'm
> aiming for"*

> *"other modes that aren't so strict … form opinions instead of simply following a rules decision
> tree"*

The first is about the **121 principles no rule reaches**. The second is about whether the graph is a
decision tree at all. The conductor's answer put them together: expose **all 145 principles with grade
and misreadings** behind a theory door (which gives #130's long-parked thirteenth verb an actual use),
and put **strictness on the GRADE, not on the mode** — three postures, **obey / weigh / argue**, where
an agent's opinion must cite an edge and is therefore gradeable. His reply: *"this all sounds great, I
really like this idea"*.

⛔ **That is enthusiasm, not a ruling, and the distinction is load-bearing.** The `s271-D4` shape says
an open item written as a state of the world is false the moment he speaks; the mirror risk here is an
idea written as a ruling because he liked it. **ONE page when he asks for it, and not before.**

**The third dial is the same discipline from the other side.** His frame — *"three dials we can use to
tune the designers experience"* — has **layers** (foundations + a11y + regulation as the floor) as dial
1. The tone-of-voice temperature map was offered as dial 2 and **refused**: *"no dial 2 isn't right.
I'll take a look"*. The third is unknown. **Three dials with one filled, one refused and one unknown is
the honest state**, and inventing a candidate for the third would be defaulting an absence into a
number in prose form.

## 5. The wall was hit a third time, and this time the gauge was not read at all

FILL closed at **337,559 real over 141 turns** — the **256,000 hard line breached by 81,559**, the
third breach on the record after #277 and #281, and larger than the other two put together. #281's
finding about itself was that the gauge was read every turn and overruled every turn. **#282's is one
worse: the conductor did not gauge at all between the logo review landing and the horizontal
clear-space ruling, and cut two Opus lanes past the wall.**

Dave's own words closed the day: *"whats the context temp like, can we squeeze it in?"* — answered no —
then *"ouch, better wrap"*.

**What this arc says, across three sessions.** At #277 the wall was crossed under pressure. At #281 it
was crossed with the instrument in hand, read and overruled — *an instrument that is read and then
overruled every turn is performing the function of a log, not of a gauge*. At #282 it was crossed with
the instrument not consulted. **The failure mode is migrating away from the instrument, which is the
opposite of what a third breach should produce**, and the ruling-shaped question the last three wraps
have each put — *what should a session DO at the hard wall?* — is now asked with three data points
behind it instead of one.

## 6. What this wrap got wrong about the brief, and published rather than smoothed

The wrap brief is the conductor's declaration and this seat's job is to measure, not to restate. Three
figures disagree, and all three readings are published on both surfaces:

| the brief DECLARES | this seat MEASURES | how |
|---|---|---|
| 14 commits | **13** | `git log --oneline 8591829..HEAD \| wc -l` |
| three amended-in-place `N N` spans | **two** (`c143a1b` 3 3, `6df8b64` 2 2) | `git show --numstat` on all thirteen commits; the other eleven touch `_rulings.json` not at all |
| Rules index 470 → **474**, BLOCKING 59 → **62** | **470 → 473**, BLOCKING **59 → 61** | `_rule_nodes.json` at `8591829` vs now, counting `type == "rule"` |

`restsOn` 73 → 75, logo nodes 12 → 8, logo edges 27 → 33 and explorer 1.25 → 1.26 all agree with the
brief exactly. **None of the brief's figures is rewritten** — a declaration and a measurement are two
objects, and the wrap that quietly replaces one with the other destroys the only evidence that they
ever differed.

## 7. Resolved state, and what is still open

**Resolved.** Six rulings inscribed and verified by span (613 → 619). Eleven guideline edits in his
words. One logo guideline. The identifier lockup out of the tree. The eye-check closed and its carry
struck. Thirteen commits, all pushed before this ritual opened.

**Open, and every one of them written as the question it is.** The 40 per-size logo masters (#283's
first move, fully specified) · the third dial · the theory door and the three postures · `col26-012` ·
`W-282a`, `W-282b`, `W-282ll` · the git-lock runbook line, owed and his · the four generator footguns
that would undo today's work if run · what a session should DO at the hard wall, now on its third
breach.
