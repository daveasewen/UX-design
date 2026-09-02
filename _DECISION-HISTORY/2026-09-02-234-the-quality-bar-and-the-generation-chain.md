# 2026-09-02 · #234 — the quality bar, and the generation chain that carries it

provenance: 234 · 2026-09-02
status: ruled — `knowledge/_rulings.json` § `s234-D1` · `s234-D2` · `s234-D3` · `s234-D4` · `s234-D5` · `s234-D6`

*Spine entry: `_LIVE-STATE.md` ⏱ LATEST DELTA #234 · `GOOD-MORNING.md` ★ LATEST #234.
Build half: `notes/_briefs/2026-09-02-234-v106-brief.md` (`W-343`). Research half:
`notes/_briefs/2026-09-02-234-quality-bar-research-brief.md` (`W-339`) and the three filed reports
`notes/_subreports/2026-09-02-234-rA-standards-bar.md` (`W-340`) ·
`…-rB-composition-rules.md` (`W-341`) · `…-rC-retrieval-contract.md` (`W-342`).
This file holds the WHY and HOW; the WHAT is in the ledger and the spine, and is not repeated here.*

---

## 1. A one-word close turned into a broader goal, and that was the session's actual hinge

The morning opened to discharge #233's banked pair: close `W-308`, inscribe *"it waits for 06"*.
Dave answered **"yes"** and both landed — `s234-D1`, and the row's `state: done` with `closed_by`
naming it. That should have been the whole beat.

It was not, because closing the demo row exposed the question the demo had been standing in for:
**what is the pack actually being graded against?** `s230-D1` had made the goal checkable in five
beats, but those beats were about the pack's own machinery. Dave's answer widened it in one
sentence — the output is ranked against **solid UI/UX standards, accessibility and code
standards, and it is dev-ready for wiring**, with **bento and behaviour in scope**. That became
`s234-D2`, written as an EXTENSION of `s230-D1` rather than a replacement, because the five beats
still hold and superseding them would have thrown away a working test to gain nothing.

**Why this is the hinge and not a preamble:** the previous session's diagnosis (*the pack has no
behaviour contract*) was a defect list. `s234-D2` turns it into an acceptance bar. Everything
after this point in the session is the attempt to make that bar mechanical rather than tasteful.

## 2. Three lanes, and why the cut fell where it did

The bar decomposes into three questions that do not share evidence, so they were cut into three
parallel Opus research subs rather than one deep one:

- **rA — the standards bar.** What does "ranked against UI/UX, a11y and code standards" mean in
  checks a gate can run? Returned a 34-criterion rubric with tiers **MACHINE / DRIVE / EYE**, and
  the finding that mattered most: the **artefact path runs three checks while ~30 gates are
  folder-bound**. The bar was never the problem; the *address* the bar is applied at was.
- **rB — composition rules.** When should things be grouped? Returned the observation that
  **nobody groups by content type** — groups form around a shared question — and that mature
  systems express composition as **parent/child RELATIONS** (Polaris' gap ladder, Carbon's
  tile-group same-size rule), not as a bento recipe. Also: **no mature system publishes a bento
  rule at all**, which is why #233's search for one kept coming back empty.
- **rC — the retrieval contract.** How does a generated screen prove which canon it actually
  read? Returned the decisive shape: external systems carry behaviour as an **ADDRESS beside the
  markup**, and **the contract must be the thing fetched, not a document trusted to have been
  read**.

**The dead end that shaped the cut:** #233 had proposed a `_validate_behaviour.py` arm. rA found
the name **already taken by ADR-0015** (the dataviz page-budget gate). A trivial collision, but it
forced the useful question — *what is the new gate's unit of work?* — and the answer (a PATH, not
a folder) is what `s234-D6` ended up ruling.

## 3. The four probes, and the one that changed a sentence

Every report was probed at the conductor's seat before any of it reached Dave, one claim each,
under the bounded-verification rule (`s172-D3`):

| probe | result | what it settled |
|---|---|---|
| rails `grep -c group` | **0** | the rails file genuinely has no grouping vocabulary — rB's premise holds |
| `_rules-index` consumers | **0 gate files** | 59 BLOCKING guideline rules with nothing reading them |
| snippets carrying `<script>` | **136/136** | the behaviour is already in the snippets; the skill just never says so |
| slots / behaviour / receipt as CONCEPTS in `SKILL.md` | **0** (one verb *"slot in"*) | the omission is total, not partial |

The fourth probe is why `s234-D5` is worded as an *address* rather than a *rule to copy JS*: if
136 of 136 snippets already carry their script, the fix is naming the address, not moving code.

**And one correction, recorded because it changes L1's price:** rA described
`_validate_advisory.py` as path-less. It is not — it takes `--root` and is **directory-bound**.
Re-pointing it at a single artefact is therefore a real change to that script, not a call-site
change. A sub's phrasing became a measurement only after it was driven
[[unmatched-grep-is-not-an-absence]].

## 4. "The KG as the brain" — the question that resolved D4, D5 and D6 at once

Dave's own framing, put as a worry: if rules reach up the whole chain — schema to rails to skill
to gate — is that the knowledge graph doing its job, or is it the same fact written four times?

The distinction that answered it, and the one durable idea of the session:

> **A rule reaching up the whole chain is VALID when the chain GENERATES, and a DEFECT when the
> chain COPIES.** One home · derived consumers · one gate · never the same fact twice.

That single test decided the shape of three rulings in a row:

- **`s234-D4`** — grouping gets **one home**, a typed `groupsWith` edge in the meta schema beside
  `mustNotNeighbour`. The rails dial, the SKILL.md rule and the gate are all **consumers generated
  from it**. `kpi` / `chart` / `rail` are re-cut as **role** names, because a name describing the
  content type is a copy of the content type; a name describing the role is the thing the edge
  actually encodes.
- **`s234-D5`** — behaviour gets **one home** too: meta owns a **typed declaration**, and the
  generator injects a snippet block, on the `#token-manifest` precedent. The skill's rule 2a sits
  *beside* rule 2 and never re-words it — a re-wording would be a second copy of rule 2.
- **`s234-D6`** — the rubric binds to the artefact through `_validate_screen.py <path>`, and the
  page carries a **RECEIPT the gate parses FIRST** [[no-gate-parses-the-artefact]]. Globs are
  **not widened**: widening a glob makes a folder-bound gate pretend to be path-bound, which is
  the copy chain again, wearing a gate's clothes.

**What was NOT ruled, and deliberately:** the role-name words themselves (`-lead` / `-evidence` /
`-context` are floated), and the new gate's name. Both are naming decisions, both are Dave's, and
proposing them inside a ruling would have laundered a suggestion into authority
[[feedback-dont-launder-a-premise-into-a-ruling]].

## 5. Where this leaves things

Resolved: the goal (`s234-D2`), the a11y bar (`s234-D3` — WCAG 2.2 AA plus 2.4.10 / 2.5.5 /
2.4.13, and expressly **not** 1.4.6, which would break the two-red law), the grouping home
(`s234-D4`), the behaviour address (`s234-D5`), the gate's binding (`s234-D6`), and `W-308`.

Still open, all Dave's: the role-name words · the new gate name · six ruling-shaped questions
(rA Q2 · rB Q3 · rB Q5 · rC Q1 · rC Q3 · rC Q4) · his remaining v1.0.5 observations · the three
row-height renders, which are a precondition to any row-height build and now carry a constraint
#233 did not know about — canon already ships fixed rows **and** a `minmax(unit,1fr)` floor at
different nesting levels (`canon.css:1091` vs `:1124`), so the renders must state which level
they vary.

Unproven and carried with prices, not smoothed: whether the two-red pairs survive a 7:1 contrast
bar (**~2K to prove**), and rB's C1–C10 conditions, which have **never been driven on the #233
artefact** and are therefore candidates, not measurements [[green-tests-cannot-see-scope]].
