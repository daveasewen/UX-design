# #289 H2 — the library build-out, as a story the record can back

provenance: 289 · 2026-09-19 · narrative sub-report for the deck
Legend: **[HIS WORD]** Dave verbatim, file+line · **[RULED]** a ruling or dated decision record · **[READING]** mine, marked as such.

## 0. The sentence this serves

**[HIS WORD]** `notes/_lanes/289/DAVE-RULINGS-2026-09-19.md:96` — *"Some context, the original library had only 36 components, we built out the rest and the reason was that the initial results were underwhelming and that was the point of realisation that it cant be automated without the inventory, it also was the realisation that our designers were re-creating or inventing components where the gaps were."*

⚠ **On "36".** The record has no 36. It has **32** reviewed (`notes/_STRATEGY-KICKOFF.md:73`, 2026-06-20, his own words); **~38** at the build-out proposal (`knowledge/_COMPONENT-LIBRARY-TARGET.md:17` — *"**~38** | 32 reviewed + 5 gap-patterns + account-card"*); **40 gated canon** (`_BUILDOUT-STRATEGY-2026-07-21.md:19`); today **137** snippets / 138 metas. **[READING]** 36 is his recollection of a figure that moved 32→40 in three weeks. For the deck: say *"about three dozen"*, or 32 → 137 — not 36 → 137 — unless he wants his own number kept.

## 1. The realisation — 2026-06-30, the SME-Payments fitness tests

**[RULED]** Four screens, one brief, four registers — sober → desktop → Swiss → portfolio (`knowledge/_FIXED-FLEX-CHARTER.md:3`).

**[RULED]** What came out, in the record's own words — `knowledge/_COMPONENT-GAPS.md:13`: *"Exposed by the portfolio run — **the canon was silent in exactly the places it had to invent**."* Three named inventions (same file, 17–19): the run **invented charcoals** (`#0E1014`…) with no light-mode dark-band role; the **waterfall / runway / proportional bars were invented** — no chart components, no named series; it **re-invented its easings** — motion tokens were component-scoped, not global.

**[RULED]** And from the earlier cold run, `knowledge/_COMPONENT-LIBRARY-TARGET.md:23`: *"when a part is missing, the model invents (the cold-B run **fabricated account numbers + status chips** to fill a table it needed) — that's where drift and 'needs a tidy' come from."*

**[READING]** The output was not broken; it was *plausible and off-canon*, which is worse — it looked finished and was full of parts nobody had ruled. The charter's diagnosis is two-dialled (`_FIXED-FLEX-CHARTER.md:13`): the canon dial was *"strong below the component line, **silent above it**"*. Silence above the component line is where invention happens.

## 2. The decision — 2026-07-01, and what the library is FOR

**[RULED]** `knowledge/_COMPONENT-LIBRARY-TARGET.md` (2026-07-01) is the decision record: *"a **comprehensive** component library makes the engine reliable for the bulk grunt work … and — because more components means more valid combinations — it produces **natural UX variance**."* Three stated purposes (23–27):

1. **Standard mode / the grunt work** — *"the engine retrieves the right part for almost any screen … **Coverage removes the reason to invent**."* ← this is his "can't be automated without the inventory".
2. **Ideation mode** — creativity as *"a deliberate, tuned setting … on top of a solid base, not a substitute for it."*
3. **The variance bonus** — more parts = more valid compositions = on-brand variance for free.

**[RULED]** The sizing benchmark (13–21): mature systems carry **~65–70 base components** (Material ~40, Ant ~65, Carbon 67, Untitled UI ~50–60 base → 10,000+ variants). *"we're at roughly half a comprehensive base library."*

**[RULED]** The principle the inventory serves — `_FIXED-FLEX-CHARTER.md:24`: *"**Recall is not allowed (recall drifts; retrieval can't).**"*

## 3. Designers inventing where the gaps were

**[READING]** The record documents the *machine* inventing at the gaps forensically (§1). It carries **no dated finding that human designers were re-creating components** — that half of his sentence is his own observation of the practice and has no file behind it. Say it as his, not as a measurement. Three records show the same mechanism at other grains:

- **[RULED]** An invention walked into the backlog. `knowledge/snippets/Runway-bar.reference.html:308`: *"Itinerary row 94 originates in a **TEST FIXTURE, not a product need** … That invention was logged as a gap, promoted into `_COMPONENT-LIBRARY-TARGET.md` line 104, and became the itinerary row … **WHETHER IT SHOULD EXIST AT ALL IS DAVE'S FIRST DECISION.**"*
- **[RULED]** Duplicates hide from probes. `knowledge/_REVIEW-SIGNOFF.md:300`: *"Row 91 Transaction/ledger row was NOT built — it is a **DUPLICATE** of a component Dave already promoted … **a slug-shaped probe cannot see a component that ships as a VARIANT of another**."*
- **[RULED]** Figma/code divergence is structural. `notes/_lanes/2026-09-10-267-N-canon-divergence.md`: **20 of 137** snippets had classes styled only in their own `<style>` and absent from generated `canon.css` — *"a designer obeying compose-from-canon got an unstyled sidebar."* Cause: **one stale generator**, not twenty rots; the whole list closed on a single regen. **[READING]** Deck line: divergence is a *generation* problem, and one inventory makes it a one-command fix.

## 4. What "Sutherland" is

**[RULED]** Sutherland is **HSBC's React component library** — the code library the canon binds *into*. Never a person, never the audience. The correction is on the record: `notes/_briefs/2026-09-08-257-delegated-wrap-brief.md:13` — **[HIS WORD]** *"where do you get the idea that this has anything to do with Sutherland? The demo is to David Rice at HSBC"*. The #246 dossier keeps its wrong line visible under a ⚠ CORRECTED block rather than deleting it.

**[RULED]** The relation is hub-and-spoke — `knowledge/_RUNBOOK-onboard-code-library.md` (2026-06-22, a Dave decision): **HUB = the Figma node identity**, the only library-independent key; **each code library = a SPOKE** under `codeBindings` (`sutherland-react`); names map *through* the node and are *"never normalised to a winner"*.

**[RULED]** `notes/RUNBOOK-end-to-end-proof.md:75-78`: *"When Sutherland lands — stations ① (spec) and ③ (gate) don't change … only the **materials** at ② swap: gated snippets → Sutherland React components. Your finesse + token fixes flow back **into** Sutherland (it has neither nailed yet)."* **[READING]** The strongest slide in this strand: the 137 are not a rival library, they are the proof harness and the feedstock for HSBC's real one.

## 5. The arc, four turning points

1. **June 2026 — the inherited kit.** ~32–38 reviewed components off the HSBC Common Toolkit. **[HIS WORD]** the plan then was depth, not breadth — *"systematically refine all 32 components to the Tabs bar"* (`notes/_STRATEGY-KICKOFF.md:73`).
2. **30 June — the underwhelming run.** Four registers, one brief. The canon *"was silent in exactly the places it had to invent"*; charcoals, chart bars, easings and account numbers all fabricated. **[READING]** The realisation is not *"the AI is bad"* — it is **"there was nothing to retrieve."**
3. **1–21 July — the decision, then the method.** `_COMPONENT-LIBRARY-TARGET.md` sets the target and the reason (*"Coverage removes the reason to invent"*). `_BUILDOUT-STRATEGY-2026-07-21.md` sets the sequence — **harness and gates first, then fan out**, because *"parallelising before the base is correct multiplies errors, not output"*: 40 gated components, four themes, a generated showroom, 38 blocking gates.
4. **5 Sept — the library dictates.** `_DECISION-HISTORY/2026-09-05-246-the-library-dictates.md` §4: four dashboards, two models × blind/sighted, all four the same specimen arrangement. *"The model changed what broke, not what was composed … **A builder with nothing to decide with ships the specimen.**"* Named causes: **470 rules and zero about composition**; `behaviour` typed on **20 of 137** metas. **[READING]** The bookend — at ~36 the machine invented because parts were missing; at 137 it shipped the specimen because *judgement* was missing. Inventory was necessary and not sufficient, which is precisely why the next box on his board is the brain, not more parts.

**[READING] The presenter's line:** *We didn't build 137 components because we like components. We built them because the first outputs were plausible, off-brand and full of parts nobody had ruled — and because our designers were filling the same gaps the same way, by hand.*
