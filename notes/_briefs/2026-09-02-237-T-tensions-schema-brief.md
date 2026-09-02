# #237 — LANE T: TENSIONS AS NODES — settle HOW they get settled, and prove it does not create more problems than it solves

*Conductor: Fable, #237. Sub: Opus. Filed report + one HTML review Dave rules from by eye. Session #237 is NOT this sub's to wrap or commit.*

## WHY THIS LANE EXISTS (Dave's words, #237)

On tensions as their own node type: *"okay this makes sense to me I think, lets talk further though."* · *"okay how do we settle these, do we go through and manually decide, or something else. explain 'or settled by an obligation'."* · *"Remember we are working on the factory mode as the baseline, we offload to the system as much as is reasonable."* · *"okay lets explore and nail this, we can get this wrong I don't want to cause more problems than we are trying to solve here."*

⛔ **Nothing here is ruled.** Dave has NOT said "nodes"; he has said the reasoning makes sense and asked for the exploration. The R1 tension table's "Resolution" column is the R1 sub's PROPOSAL, not a ruling. Rulings inscribed this morning that bind you: `s237-D1` (grade names REPLICATED · STUDIED · PRACTISED · DEBUNKED · OBLIGATION) · `s237-D2` (obligation is a node TYPE no principle can outrank) · `s237-D5` (explainedBy is one-directional, advisory) · `s237-D9` (a derived fact is never typed). Read them from `knowledge/_rulings.json` (the last ten entries).

## GROUND FIRST (~15 min)

1. `notes/_subreports/assets/2026-09-02-236-R1-principles-survey/tensions.json` — all 30, the data.
2. `notes/_subreports/2026-09-02-236-R1-principles-survey.md` § 3 (the abridged table) and § 5a (the 12 touchpoints).
3. `apollo-spider/skills/grill-me/` — how the shipped first phase asks, skips and DECLARES DEFAULTS ("Skipped:", "Defaults used:"). The tension→question idea must fit THIS, not replace it.
4. Vocabulary probe (the `s202` class): `grep -o -i -w "tension" knowledge/_rulings.json knowledge/_consult-lexicon.json knowledge/_KNOWLEDGE-USAGE-ENTITIES.json knowledge/_memento-index.json | wc -l` and read any hit — does "tension" already mean something in this house? Same for "default" as a noun in the pack.
5. `notes/_subreports/_TEMPLATE.md`.

## THE FIVE DELIVERABLES

**1. The sort — DERIVED, not decided.** Put every one of the 30 into exactly one bucket by a mechanical rule, and print the rule beside the count:
   - **Settled by obligation** — at least one party is an obligation node (WCAG clause, DSA article, FCA rule, EAA/EN 301 549). By `s237-D2` there is nothing to weigh: the obligation wins; the mediating variable becomes the ROUTE to compliance, not a choice. *This is what "settled by an obligation" means — write that sentence in the report in our words.*
   - **Resolved in this house** — the resolution cites an existing ruling id (`s116-D1`, `s217-D8`, …). PROBE each cited id exists in `_rulings.json` and quote its `ruled` line ≤ 15 words. The tension node POINTS at the ruling; it never restates it (write-once, ADR-0017).
   - **Open** — everything else.
   Counts per bucket. If a tension is a triple with an obligation party AND a ruling, say which rule wins and why (obligation first).

**2. Every OPEN tension, four fields — the factory-mode answer.** Dave's baseline is factory mode: offload to the system as much as is reasonable. So for each open tension:
   - **Factory default** — the system's standing answer, in our words, derived from R1's resolution column where it can be; marked `proposed` (it is a floated register, never canon until Dave rules).
   - **Mediating variable** — one phrase (from the data).
   - **Knowable by the factory?** — YES if the grill's six questions or the brief already capture it (theme, density, width, data, fixed/off-limits, brand); NO if only the designer can know it (task criticality, audience expertise, regulatory context, whose interest, brand intent).
   - **Ask-when** — the condition under which the factory must ASK rather than default; and the question in the designer's words, ONE line. If the factory can reasonably default, the row says `DEFAULT + DECLARE` (the grill's "Defaults used:" mechanism), not a question.
   Then the headline number: **of N open tensions, how many become questions and how many default-and-declare.** If it is more than ~5 questions, say so plainly — that is the "more problems than we solve" outcome.

**3. Two schema readings, side by side, on the SAME four tensions** — `tn-3` (a triple), `tn-19` (four parties, obligation-settled), `tn-7` (ruling-resolved), and one open one you pick. For EACH reading (edges vs nodes) show, concretely: what is stored (a JSON sketch, ≤ 15 lines); what "what pulls against Fitts?" returns; what "list the open questions for this task" returns; how a ruling→tension link is expressed; what happens to a triple. Render this as **one HTML review Dave rules from by eye**: `_REVIEW-tensions-schema-2026-09-02-v1.html` at repo root, built with the `swiss-design-system` skill (grid, hierarchy, navigable), light + dark (two-red law: `#DA1A00` on light, `#F6604C` on dark; mono error ink camp), no horizontal scroll at 1440 and 390. Render + read back both PNGs by eye via the mount-side render env (`outputs/_render-env-229/`, `TMPDIR=/dev/shm`, `goto("file://…")` never `set_content()`). If the render env is unavailable, say so and ship the HTML unrendered, DECLARED.

**4. The "more problems than we solve" register — consequences replayed (#165).** At least these, each with the mitigation and who owns it:
   (a) a tension store becoming a SECOND rulings store — mitigation: point, never restate; status DERIVED (`s237-D9` pattern), never typed;
   (b) a factory default that silently pre-empts a consent or legal choice — `tn-25` (anti-preselection) is the live example; the DSA line;
   (c) the grill growing by up to 30 questions — question fatigue; cap by ask-when;
   (d) a triple split into edges that then disagree with each other;
   (e) vocabulary: "tension" and "default" already meaning something (your probe in GROUND 4);
   (f) a default that contradicts a shipped pack rule — probe `apollo-spider/` rules for each default you propose (density floors `s116-D1`, keylines `s217-D8`, the two-red law `s151-D1`);
   (g) an open tension with no ask-when and no default is IMMORTAL (the `_state.py` lesson: every open thing needs a close condition);
   (h) generation-not-copy: if tension nodes are hand-typed into the graph, they are a copy chain (`s234-D1`); name what GENERATES them from `tensions.json`.

**5. Ruling-shaped questions for Dave (≤ 5)**, each with your recommendation and one-clause reason. The first must be: **edges or nodes** — say which, on the evidence of deliverable 3. The second: **who settles the open ones** — manual sitting (Dave rules N) vs derived defaults with Dave ruling only the ask-when list vs something else. Do not decide either.

## METHOD RULES

- **Derive before you decide.** Every bucket and count comes from a rule over `tensions.json`, printed with the count. A hand-sorted list is the defect.
- **Our words + ≤ 15-word quotes.** Rulings are quoted from `_rulings.json`, principles from R1's register, never from memory.
- **Register discipline.** Everything you propose is FLOATED. Say "proposed" on every default; never "the default is".
- **Dated history is not edited.** R1/R2/G reports, the plan v1, their assets — frozen. You write ONLY: the review HTML at repo root, `notes/_subreports/2026-09-02-237-T-tensions-schema.md`, and `notes/_subreports/assets/2026-09-02-237-T-tensions-schema/` (the sort as JSON, the open-tension table as JSON, the two PNGs, any probe receipts).
- **One heavy call at a time** — the sandbox kills at ~178 s; render steps individually.

## DO NOT RULE

- Edges vs nodes. Names of anything. Which tensions enter. Whether the grill changes. What the factory default IS for any tension — propose, never set.
- No writes to `knowledge/_rulings.json`, `knowledge/_state.json`, `_CARRIES.md`, `GOOD-MORNING.md`, `_LIVE-STATE.md`, memory, the plan, or `apollo-spider/`. No git. No `_build_all.py`. No `_gen_chain.py`.

## FILING

Copy `notes/_subreports/_TEMPLATE.md`; `sub index` = `T`; `brief:` = this file. Counts line: **tensions 30 · settled-by-obligation n · resolved-here n · open n · of open: questions n / default-and-declare n · pitfalls n · ruling-shaped n · UNPROVEN n.** Close with **REPLAY-THESE** (≤ 7 lines). Token spend: `UNMEASURED — no message.usage at a sub's seat`, plus the SHAPE. Return to the conductor a STUB only: report path, review HTML path, counts line, REPLAY-THESE.

## PITFALLS FOR THIS LANE ITSELF

1. **Building the likeliest reading.** Dave rules by eye between readings; ship BOTH schema readings at equal depth, not one polished and one sketched.
2. **Answering "who settles" by settling.** Your job is to show what derivation buys and what remains for Dave — and how many decisions that is. His decision load is the binding constraint in this house.
3. **A pretty review that hides the count.** The number of questions the grill would grow by is the finding; put it in the answer line of the HTML.
4. **Treating R1's resolutions as canon.** They are one sub's proposals from one morning.
