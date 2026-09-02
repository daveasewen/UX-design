# `#237`-`T` — tensions as nodes: how they get settled, and whether that costs more than it saves

session: `#237` · 2026-09-02
window: Fable conductor, lane T (schema exploration + one HTML review)
sub index: `T`
brief: `notes/_briefs/2026-09-02-237-T-tensions-schema-brief.md`
tokens: `UNMEASURED — no message.usage at a sub's seat`. SHAPE: 19 tool calls · 2 derivation scripts written and run over `tensions.json` · 3 render attempts (1 caught a real defect, 1 a clip-space error, 1 clean) · 7 PNGs, 6 read back by eye · 0 writes outside this lane's three permitted paths · no git, no `_rulings.json`, no `_state.json`.

## VERDICT

All five deliverables are **DONE**. The sort is derived by two printed rules over `tensions.json` and lands **6 settled-by-obligation · 3 resolved-here · 21 open**; the obligation rule runs first and takes two rows that also cite a ruling. Of the 21 open, **4 become questions and 17 default-and-declare — and all four questions are CONDITIONAL, so the standing grill grows by zero.** That is comfortably under the brief's ~5 threshold, but it is not the whole answer: **the cost moved rather than vanished.** The grill's `Defaults used:` line was built for six answers and would carry twenty-one. Question fatigue is not the risk here; declaration fatigue is, and that is the honest "more problems than we solve" finding.

On the schema, the evidence is one-sided and mechanical rather than aesthetic: **13 of the 30 tensions have at least one side that is not a principle at all** — free text ("information density on a dashboard"), a product requirement ("four-theme flexibility"), an architecture ("the generation chain"), and in `tn-16` a *ruling* (`s116-D1`). An edge needs a node at both ends, so those 13 produce **zero edges**. Separately, the sort proved **sensitive to which field it reads**: taking `apollo_touch` as a resolution moves the counts to 6·9·15, and four of those six would close *wrongly*, because `apollo_touch` conflates *resolves*, *explains* (`s237-D5`), *challenges* and *merely touches* in one slot. I recommend nodes and say why, but the recommendation is Dave's to accept or refuse — **nothing in this lane is ruled**, and every proposed default is marked `proposed`.

COUNTS: tensions `30` · settled-by-obligation `6` · resolved-here `3` · open `21` · of open: questions `4` / default-and-declare `17` · pitfalls `8` · ruling-shaped `5` · UNPROVEN `6`

*(Template COUNTS terms, also parsed: findings `12` · ruling-shaped `5` · UNPROVEN `6`.)*

## What was done

**Ground.** `tensions.json` (all 30, read in full); `2026-09-02-236-R1-principles-survey.md` §3 and §5a; `principle-register.json` (145 rows, the `grade` field is what the sort keys on); `knowledge/_rulings.json` (321 rulings — `s237-D1`…`s237-D10` read in full); `apollo-spider/skills/grill-me/SKILL.md` and its `brief-template.md`; `notes/_subreports/_TEMPLATE.md` (copied, not edited); the vocabulary probe below.

**Region 1 — the sort.** `assets/2026-09-02-237-T-tensions-schema/_derive_sort.py` prints its rules and writes `tension-sort.json`.

**Region 2 — the open table.** `_derive_open_table.py` prints RULE K and RULE D and writes `open-tensions.json`.

**Region 3 — the two readings.** `_REVIEW-tensions-schema-2026-09-02-v1.html` at repo root, built with the `swiss-design-system` skill. Rendered light and dark at 1440 and probed at 390.

**Region 4 and 5 —** the consequence register and the five questions, in the HTML and below.

**Written:** the review HTML at repo root, this report, and seven files in `notes/_subreports/assets/2026-09-02-237-T-tensions-schema/`. **Nothing else changed.**

## THE SORT — the rules, then the counts

```
R-OBLIGATION  at least one party id resolves to a principle-register row whose grade is
              "L", which s237-D1 names OBLIGATION.  APPLIED FIRST (s237-D2).      ->  6
R-RESOLVED    the how_it_resolves prose cites a ruling id s<N>-D<N> that is present
              in knowledge/_rulings.json.                                          ->  3
R-OPEN        the complement.                                                      -> 21
```

| bucket | n | ids |
|---|---|---|
| settled-by-obligation | **6** | `tn-15` `tn-16` `tn-19` `tn-20` `tn-25` `tn-29` |
| resolved-here | **3** | `tn-07` `tn-17` `tn-27` |
| open | **21** | the remaining 21 |

**What "settled by an obligation" means, in our words.** An obligation is a rule written by someone outside this house — a WCAG success criterion, a DSA article, an FCA rule, an EAA/EN 301 549 requirement. `s237-D2` makes it a node *type* that no principle can outrank. So when one side of a tension is an obligation, **the tension is not a trade and there is nothing to weigh: the obligation wins by construction.** What survives is not a choice but a **route** — the mediating variable stops deciding *who wins* and starts deciding *how you comply*. Brand does not lose an argument to contrast; brand changes its size, weight or ground until it complies.

The six, with the obligation party's own statement (≤15 words) and the route:

| id | obligation party | its clause | the route |
|---|---|---|---|
| `tn-15` | `pr-wcag-1-4-3` | "Text must meet a minimum contrast ratio against its background." | background-keyed colour — `s151-D1` resolves one semantic red per ground |
| `tn-16` | `pr-wcag-2-5-5` | "Pointer targets are at least 44 by 44 CSS pixels." | split by object class, declare the exemption (`s234-D3` + `s116-D1`) |
| `tn-19` | `pr-dsa25` | "…must not deceive, manipulate, or impair users' ability to decide freely." | persuasion only where the thing shown is true and the action reversible |
| `tn-20` | `pr-fca-consumer-understanding` | "Communications must equip customers to make effective, timely and properly informed decisions." | layer disclosure at the decision moment |
| `tn-25` | `pr-anti-preselection` | "ANTI-PRINCIPLE: Pre-ticking an option the user did not choose." | grade the slot — defaults legal on preferences, prohibited on consent |
| `tn-29` | `pr-wcag-2-4-13` | "The focus indicator must meet minimum area and contrast requirements." | focus is a first-class token from the start |

**Which rule wins where both apply.** `tn-15` and `tn-16` are in both buckets: each has an obligation party *and* cites a ruling in `how_it_resolves`. **Obligation wins**, by `s237-D2` — a ruling cannot settle a thing an obligation has already settled. What the ruling supplies is the *route*: `s151-D1` is how `tn-15` complies, `s116-D1` and `s234-D3` are how `tn-16` complies. That is exactly why R-OBLIGATION runs first.

**Resolved in this house — the tension points, it never restates.** Each id was probed and is present; `ADR-0017` (write-once) says the tension carries the pointer and the ruling keeps the words.

| id | ruling | its `ruled` line, first 15 words |
|---|---|---|
| `tn-07` | `s116-D1` | "Data marks are held to the 24x24 WCAG 2.5.8 dense-case MINIMUM - exempt from the …" |
| `tn-17` | `s202-D1` | "THE SQUARE THEMES INHERIT CONSOLE'S TUNED SEGMENTED DIMENSIONS, AND THE MINT IS BASE-TIER. Dave ruled …" |
| `tn-27` | `s234-D6` | "THE QUALITY RUBRIC BINDS TO THE ARTEFACT THROUGH THE ONE PATH-TAKING GATE - _validate_screen.py <path> …" |

## THE 21 OPEN — four fields each, all FLOATED

**RULE K (knowable)** matches the mediating variable against the grill's six, plus a *named standing rule* where the answer is a property of the artefact or the pipeline rather than of the client. **RULE D (disposition)** is a two-clause test: a conservative standing answer exists **and** a wrong answer is recoverable in the edit pass. Both true → `DEFAULT+DECLARE`. True with a named trigger → `DEFAULT+CONDITIONAL`. Neither → `ASK-AT-GRILL`.

The full table with every proposed default is `assets/…/open-tensions.json` and is rendered in the HTML. The four that ask:

| id | proposed factory default | ask-when | the question, in the designer's words |
|---|---|---|---|
| `tn-01` | Converge on mechanism, diverge on signal — one brand moment per view. | Q4 names a brand mandate that changes a **mechanism**, not a signal | *"Your brand asks for a non-standard control here — may we keep standard behaviour and carry the brand in the signal instead?"* |
| `tn-08` | Nothing blocks; status accretes where the user chooses to look. | the brief or the data names an irreversible or time-critical event **and** the screen carries a notification surface | *"Which of these events must stop someone mid-task — and which can wait until they look?"* |
| `tn-11` | Rank by expected cost, not frequency. | Q6 was **skipped** and the surface handles money, eligibility, health or identity | *"You skipped the fixed/off-limits question and this screen handles money — is there a regulatory requirement it has to meet?"* |
| `tn-21` | Rank encodings by accuracy; record the cost when brand overrides. | Q4 names a chart style that lowers the encoding rank | *"Your brand chart style reads less accurately than the plain one — is this for deciding, or for communicating?"* |

**The headline.** Of 21 open: **4 become questions, 17 default-and-declare.** All four are conditional on an answer the grill already collects, so **the standing six-question grill grows by zero**. Four is under the brief's ~5 threshold.

**But say the rest plainly.** The count that grew is the *declaration*, not the question list: **21 standing default lines** would join a `Defaults used:` field whose template carries one line per skipped answer and was written for six. A declaration nobody reads fails in the same way a question nobody answers does. That is deliverable 5's fourth question.

RULE K found **four** rows that no grill question reaches — `tn-08`, `tn-21`, `tn-22`, `tn-26` — and two of them still default, because the answer lives in a ruling already made (`tn-22` → `s217-D8`) or in a check on the artefact (`tn-26`). RULE K and RULE D disagreeing there is honest and informative: *not knowable* is not the same as *needs asking*.

## Findings

1. **The sort is 6 · 3 · 21, derived.** Both rules print beside their counts in `_derive_sort.py`; `tension-sort.json` carries the per-row working. Every cited ruling id resolves — `CITED RULING IDS ABSENT: none`.
2. **The sort is sensitive to which field it reads, and this is the schema argument.** A variant rule that also scans `apollo_touch` moves six rows and gives **6 · 9 · 15**. Four of the six would close **wrongly**: `tn-01`'s `s151-D1` *explains* (the `s237-D5` relation), `tn-11`'s and `tn-14`'s rulings are *challenged by* the tension ("should carry consequence", "should be justified by … NOT by 7±2"), and `tn-08`'s `apollo_touch` says in its own words that the shell is ruled and the routing rule is not. Only `tn-02` and `tn-22` are genuine resolutions whose id sits in the wrong field. **`apollo_touch` is four link types in one slot.**
3. **13 of 30 tensions have a side that is not a principle node** — probe in `_derive_sort.py`'s successor block: `tensions where every side resolves to >=1 register principle: 17`. The other 13 hold free text, a product requirement, an architecture, or a ruling. **An edge needs a node at both ends; those 13 produce zero edges.** 24 pairwise edges exist in total against 30 nodes plus 50 party links.
4. **`tn-19` is four principles in two side fields, and `side_b` is a comma list crammed into one string.** As edges that is six pairwise links, three of which (`social-proof ↔ goal-gradient` and its two siblings) assert pulls that do not exist. Cut it to three and the fact that the three persuasion principles are *one side* is lost.
5. **Vocabulary collision, the `s202` class — confirmed, not suspected.** Probe: 43 hits for `tension` across the four knowledge files. In `s143-D1` Dave ruled that four `$status` **tension** flags "must be downgraded from TENSION to CROSS-REFERENCE — they are not conflicts." In `_KNOWLEDGE-USAGE-ENTITIES.json` a tension is an unreconciled disagreement between two source documents, queued at ingestion. **R1's tensions are neither**: they are permanent pulls between two true things and can never be downgraded away. `default` carries two senses already — the shipped starting value inside a ruled option set (`s219-D3`: "GENERATION SHIPS DEFAULTS, EDIT PICKS WITHIN THE RAILS") and the grill's value-used-because-you-skipped. A factory default for a tension would be a third.
6. **`tn-25` lands in the obligation bucket by derivation, which is the right answer to the consent trap.** `pr-anti-preselection` is grade L. So the factory is *never permitted* to mint a default there — the pitfall the brief named is closed by the sort itself, not by a warning.
7. **A dangling party id.** `tn-28` names `pr-info-scent`; the register holds `pr-information-scent`. It resolves to nothing. The derivation caught it because it looks ids up; a hand-typed import would have carried it in silently — the dangling-var class, one graph over.
8. **`tn-16` puts a ruling on one side of a tension.** `side_b` is "dense financial tables and `s116-D1` data marks". Whatever the schema is, a party may be a principle, an obligation, a ruling, or a plain phrase.
9. **The sort has a clock.** `s237-D4` was inscribed this morning, *after* `tensions.json` was generated, and it substantially answers `tn-30` (pointer-only families, generator refusal). Any sort of this data is true as of a moment — `s129-D5`, conclusions are debt.
10. **Grill fit.** The tension→default mechanism maps onto the shipped `Skipped:` / `Defaults used:` lines rather than replacing them, and onto the skill's own promise that it "will not quietly pick for you and say nothing". The mechanism exists; it is the *volume* that is new.
11. **The render env's stored `fonts.conf` hardcodes another session's mount path** (`determined-affectionate-euler`), so it resolves to nothing at this seat — the fifth-stratum hollow-directory shape, one file over. Fixed by generating a per-seat fontconfig in the same bash call. **The runbook's SEVENTH STRATUM otherwise held**, and it is now driven from a second seat, which its own provenance note said it had not been.
12. **The first render caught a real page defect.** At 390 the document measured `scrollWidth 660` against `clientWidth 390`. Cause: grid children default to `min-width:auto` and cannot shrink below the 640px table inside them — the `overflow-x:auto` wrapper was never reached. Fixed at the cause (`min-width:0` on every grid child) rather than masked with `overflow:hidden`. Re-probed: **1440 → 1440/1440 OK; 390 → 390/390 OK, both themes.**

## THE "MORE PROBLEMS THAN WE SOLVE" REGISTER (8, consequences replayed — `#165`)

| | risk | mitigation | owner |
|---|---|---|---|
| **a** | A tension store becomes a **second rulings store** — 30 retrievable judgement objects beside 321 rulings. | Point, never restate (`ADR-0017`); status **DERIVED**, never typed (`s237-D9`); retrieval returns the ruling first. Note the edge reading makes this *structurally impossible* rather than merely mitigated — that is its strongest argument. | retrieval layer |
| **b** | A factory default **silently pre-empts a consent or legal choice** — `tn-25` is the live one, the DSA line. | Already closed by the sort: `pr-anti-preselection` is an obligation, so the factory may not default there at all. Grade the slot, not the mechanism. | the generator's default-minting path |
| **c** | The grill grows by up to 30 questions. | Ask-when. Derived: **0** new standing questions, 4 conditional. **The residual is real and lands elsewhere: 21 declaration lines in a field built for six.** | the grill skill — unresolved, question 4 below |
| **d** | A triple split into edges that then disagree. | `tn-03` → 3 edges, `tn-19` → 6, each holding a copy of one mediating variable. Either the node reading, or one canonical edge with the rest *generated* from it. | the schema decision itself |
| **e** | **Vocabulary** — "tension" and "default" already mean things (finding 5). | Rename before anything is generated. The `s202` "switch" case is the precedent: a collision costs one decision now or a rebuild later. | Dave, before P1 |
| **f** | A default that **contradicts a shipped pack rule**. | Probed against the rulings named in the data: `tn-22`'s default restates `s217-D8` (so it must *point* instead), `tn-15`/`tn-16` route *through* `s151-D1` and `s116-D1` rather than against them. Standing rule: no proposed default may restate a ruling. **UNPROVEN:** not every default was grepped against every rule in `apollo-spider/`. | a gate at generation time |
| **g** | An open tension with no ask-when and no default is **immortal** (the `_state.py` lesson). | All 21 rows carry a close condition. `never` in the ask-when column means *closed by the default*, not *unclosable*. A row with neither should fail the build. | the tension generator |
| **h** | Hand-typed tension nodes are a **copy chain** (`s234-D1`). | Name the generator: `tensions.json` is the source and the two scripts in this lane's assets are its working shape — a sort keyed on the principle register's own `grade` and on `_rulings.json` membership, re-derived every build. It already caught a dangling id (finding 7) that a typed import would have swallowed. | the P1 build |

## RULING-SHAPED QUESTIONS

⛔ **MANDATORY SECTION.** Nothing below is decided. Each is Dave's.

1. **Edges or nodes?** (a) a typed edge between two principles carrying the mediating variable; (b) its own node type with N parties and typed links out. *Recommend **(b), nodes*** — because 13 of the 30 have a side that is not a principle and would produce no edge at all, and because the single untyped ruling slot an edge affords is exactly what would silently close four open questions (finding 2). The edge reading's real virtue is named and not dismissed: it makes consequence (a) structurally impossible.
2. **Who settles the open ones?** (a) a manual sitting where Dave rules 21; (b) derived defaults, Dave ruling only the ask-when list; (c) derived defaults with no ruling until one bites. *Recommend **(b)*** — it puts **4** decisions in front of him instead of 21, and the four are the ones where a wrong default is expensive.
3. **Does "tension" keep its name?** *Recommend renaming* — finding 5 is a confirmed `s202`-class collision with a ruling (`s143-D1`) already using the word for something that can be downgraded away.
4. **Does the declaration get a cap?** 21 default lines into a `Defaults used:` field built for six. (a) declare all; (b) declare only defaults that bent away from the conservative side; (c) declare on demand. *Recommend **(b)***.
5. **Which field carries a ruling link, and is it typed?** `apollo_touch` currently mixes *resolves*, *explains* (`s237-D5`), *challenges* and *touches*. *Recommend typed links and a generator that refuses an untyped one* — the sort moves 6·3·21 → 6·9·15 on this one choice.

## UNPROVEN / CLAIMED (ADR-0016)

- **UNPROVEN:** the 17 default-and-declare rows were checked against the rulings *named in `tensions.json`*, not against every rule in `apollo-spider/` — price to prove: a grep pass per default over the pack's `SKILL.md` set and `DESIGN-CONTRACT.md`, ~8–10K.
- **UNPROVEN:** RULE D's two-clause test is this lane's own and is applied by judgement, not machine-derived. The *inputs* are printed; the disposition is not a measurement. Price: Dave's eye, not a probe.
- **UNPROVEN:** whether a store can express edge properties or reification at all depends on the graph store P1 picks, which is not chosen. Price: the P1 store decision.
- **UNPROVEN:** the `Defaults used:` capacity claim is inferred from `brief-template.md`'s shape (one line per skipped answer), not from a real grill run carrying 21 lines. Price: one grill run.
- **UNPROVEN:** `pr-info-scent` is a *near-miss* for `pr-information-scent` by string similarity; R1's intent was not confirmed from its fetch receipts. Price: ~1K.
- **UNPROVEN:** the render used the mount env's face set and a canvas probe showed `"Helvetica Neue"` measuring differently from `sans-serif` (279.2 vs 302.4 px), so a distinct face resolved — but *which* face was not identified.
- **CLAIMED → now PROVEN:** the runbook's SEVENTH STRATUM carried a provenance warning that it "was NOT re-driven by the wrap sub that wrote it down". It was driven end-to-end at this seat today, with the per-seat fontconfig correction in finding 11.

## Evidence

`notes/_subreports/assets/2026-09-02-237-T-tensions-schema/` —
`_derive_sort.py` (the bucket rules, printed; run to reproduce 6·3·21) · `tension-sort.json` (per-row working, obligation grades, cited ids, the X-LITERAL cross-check) · `_derive_open_table.py` (RULE K and RULE D, printed) · `open-tensions.json` (all 21 with default, variable, knowable, ask-when, disposition) · `review-light-1440.png` and `review-dark-1440.png` (the two full-page renders, 1440×13675, read back by eye) · `crop-light-top.png` · `crop-dark-top.png` · `crop-light-readings.png` · `crop-dark-readings.png` · `crop-mobile-390.png` (legible section crops — the full-page PNGs downscale below reading size, so the eye-check was done on these).

Review page: `_REVIEW-tensions-schema-2026-09-02-v1.html` (repo root). Two-red law observed — `#DA1A00` on the light ground, `#F6604C` on the dark; the accent is ink only, never a fill, so the mono error ink camp (`s149-D1`) is not engaged. No horizontal scroll at 1440 or 390 in either theme, re-measured after the fix in finding 12.

REPLAY-THESE: `notes/_subreports/assets/2026-09-02-237-T-tensions-schema/open-tensions.json` (~3.5K — the 21 proposed defaults, the only place they exist in full) · `_REVIEW-tensions-schema-2026-09-02-v1.html` §"Two readings" (~4K — Dave rules question 1 by eye from it) · finding 2 and finding 5 above (~0.6K — the two findings that change the schema answer) · `_derive_sort.py` (~1.5K — re-run before quoting 6·3·21 in any later session; the sort has a clock, finding 9).
