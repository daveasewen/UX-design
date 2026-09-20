# #289 H3 — the pair of agentic loops, and what they showed

provenance: 289 · 2026-09-20 · narrative sub-report for the deck
Legend: **[HIS WORD]** Dave verbatim, file+line · **[RULED]** a dated decision record · **[READING]** mine, marked as such.

## 0. The sentence this serves

Dave, today: *"this is the story about the experiments with a pair of agentic loops, its in the archive i think"*.

**[READING]** The record holds **two** A/B pairs, three weeks apart, and they are the same method at two grains. §1 is the component-grain pair; §2–3 is the screen-grain pair and is almost certainly the one he means, because it is the one whose verdict was *underwhelming*.

## 1. The first pair — Tabs, 2026-06-19 (component grain)

**[RULED]** `archive/SESSION-BRIEF-tabs-fitness-test.md:7-8` — build Tabs twice: **Route B**, *"using **only** the knowledge base … No live Figma, no outside design judgement"*, gap-logged live; then **Route A**, *"the best Tabs I can, unconstrained … This is 'what good looks like.'"* Route B locked its gap log *before* A ran (`knowledge/_fitness-test/route-b-gap-log.md:3`).

**[RULED]** Verdict, `knowledge/_FITNESS-TEST-tabs.md:7`: *"The KB drives a structurally correct, accessible-in-light-mode component — **and a dark-mode failure**"* — label and indicator **1.0:1, invisible**; craft was *"~90% my invention"*. Meta-finding, same file: *"the integrity gate **passed** a component that's broken in dark mode."*

**[READING]** This is where "passes the gate" and "is usable" were first measured apart. Model: not stated in the record.

## 2. The second pair — SME Payments, 2026-07-05 (screen grain, the underwhelming one)

Both arms ran on the **same SME-Payments contract** (`knowledge/_TEST-BRIEF-v2-sme-payments.md`), same figures, cold isolated passes.

- **Governed arm** — the §9 register ramp: three bands (sober / balanced / expressive) from one signed contract, *"generated in isolated parallel passes"*. Run first on **Sonnet**, then re-run whole on **Opus** after Dave found two real gaps and asked *"whether a build→review→correct loop exists (**it didn't**)"* (`_DECISION-HISTORY/2026-07-05-register-spread-and-restyle.md:10-21`). Artifacts: `knowledge/_fitness-test/register-spread-2026-07-05/` and `-opus/`.
- **Ungoverned arm** — Dave's own idea: *"Two cold **Opus** passes on the same SME Payments data, zero brand governance (no canon, no curbs, no a11y mandate, no component library)"*; **Variant A** with named influences (Linear/Stripe/Mercury/Ramp), **Variant B** *"'your own idea of award-winning' only"* (`knowledge/_fitness-test/register-spread-2026-07-05-diagnostic/_FINDINGS.md:3-7`).

**[RULED]** Result: cardinal curbs held **zero violations** in every governed band; but the ungoverned Variant B *"organised the whole screen around an idea ('time as the spine') … rather than a component checklist"* (same file, :22-24). Colour/type/radius gaps in the governed arm were *"expected and by design"*; the gap that mattered was **structural**.

**[RULED]** A **gravity fix** (named external references) was added and only the expressive band re-run on both models (`expressive-v2.html`) — motion mentions Sonnet 4→23, Opus 2→15 — *"**neither closed the expressive excitement gap**"* (`…2026-07-05-register-spread-and-restyle.md:80-83`).

## 3. Dave's verdict, and the hand-executed second loop

**[HIS WORD]** `_DECISION-HISTORY/2026-07-07-s9-root-cause-and-ruling.md:13-16` — *"the canon works but probably no better than an AI model tied to a component library. The layouts tend to be better and the extra 'assumptions' or gap fillers seem better when unconstrained... I expected something like: unconstrained with the right styling"*.

**[HIS WORD]** same file :28 — *"its just about crafting the rules I guess, i need to read through them"*. And :51 — *"is there a way we can build a trace to record what entities from the knowledge a cold run uses?"*

**[RULED]** So the ungoverned piece was hand-restyled onto canon (`without-influences-hsbc.html`) on **[HIS WORD]** *"if we style these using the HSBC primitives I'd be pretty happy"* (`…register-spread-2026-07-05.md:132-133`). That pass needed real repairs Dave, not the machine, caught: a bare-`:root` theme-alias trap, 3 invented icons, **4 real WCAG contrast failures** — **[HIS WORD]** *"did you put the restyle through the gates or use your own inference?"* (:161) and *"this would fail accessibility for a start"* (:175). Honest answer on record: *"inference, not gates"*.

**[RULED]** The record names the pair plainly (:43-46): *"no one has compared 'governed single-pass' vs 'generate-then-normalise two-pass' as a controlled pair on the same screen — everything so far is one lineage (unconstrained → hand-restyled) vs a different lineage (governed ramp, Sonnet+Opus) **that were never actually running the same experiment**."*

## 4. What was concluded

1. **[RULED]** The trace tool (built 2026-07-07, `knowledge/_trace_knowledge_usage.py`) settled the cause: governed lineages are **provenance-perfect** — 0 invented colours, ~200 canon token refs — *"yet flat"*; the diagnostic is 56 live hex / 219 local vars and violates 6 rules. **Freer layout and rule-honouring pull in opposite directions.** Tightening adherence cannot lift a ceiling already met.
2. **[RULED]** Root cause, same day → **the library stops at organism**: 38 components = 9 atoms / 23 molecules / 6 organisms, **zero templates or page shells**. *"Page composition has nothing to retrieve → flat layouts are structurally forced."* (`…2026-07-07-s9-root-cause-and-ruling.md:86-91`; `knowledge/_FINDINGS-s9-session-2026-07-07.md`.)
3. **[RULED]** Dave's ruling 2026-07-10 (:136-142): rule-tuning + inference-tiering **leads**; the double pass was *"not all that successful"* — *"an interesting hypothesis, no more"* — and becomes *"a component, not the architecture"*.
4. **[RULED]** Resurrection note, 2026-07-18, on the file itself: *"**RESURRECT (Dave): YES** — likely feeds the Creative and Explore modes of Apollo Create"* / *"the experiment chain is valuable for later evaluation"*.

## 5. The deck line

**[READING]** *We ran the same screen two ways: one that obeyed every rule, and one that obeyed none. The obedient one was flawless and flat. The free one composed better and broke four accessibility rules. The answer was not more discipline — it was that the library had nothing above a component for the obedient one to retrieve.*

## 6. Not established (looked, did not find)

- **The phrase "agentic loop" attached to these runs.** It appears once, elsewhere and later: `_retired/agent-memory-snapshot-2026-07-18/store/agentic-loop-gates-as-service.md` (Dave, 2026-07-14) — *"generator + verifier + iteration"*, with *"the repair loop is 'not built'"*. **[READING]** That is a *third* thing — the gates-as-a-service idea — not the pair; do not conflate them on a slide.
- **A rendered/blind-judged scorecard.** Every 2026-07-05 artifact carries the same caveat: *"no rendered visual check"*. The three-arm R1 experiment ruled on 2026-07-10 has no run record.
- **Which pair Dave means by "the archive".** Both live in archive-class locations (`archive/`, `_DECISION-HISTORY/` relocated verbatim 2026-07-18). Worth one question before the deck.
