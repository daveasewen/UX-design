# #236 — LANE R1: THE PRINCIPLES SURVEY — sources, evidence grades, contradictions

*Written 2026-09-02 by the Fable conductor. ONE Opus research sub (web + repo read; NO repo writes outside `notes/_subreports/`). Report files at `notes/_subreports/2026-09-02-236-R1-principles-survey.md` per `s218-D7`; evidence beside it at `notes/_subreports/assets/2026-09-02-236-R1-principles-survey/`; chat gets a STUB. Parent programme: "the designer's brain" — Dave's #235 candidate "KG as a designer's brain", opened at #236 with https://lawsofux.com/ as source 1.*

## WHY THIS LANE EXISTS (Dave's words, #236 opener)

> "I want you to do some research first rather than just use this site alone, lets find more principle, laws etc and validate them, i want the brain to be powerful. I think that we might also find contradictions in all these rules and principles so it need rigour."

The knowledge graph today holds tokens, patterns, behaviours and rulings — the WHAT. It holds **no** UX law, heuristic or psychological principle — the WHY (probed #236: grep of `knowledge/_rulings.json`, `_consult-lexicon.json`, `_KNOWLEDGE-USAGE-ENTITIES.json`, `notes/_briefs/` → no Fitts/Hick/Nielsen/heuristic node). This lane gathers the raw material for that layer and grades it. **It does not build the layer** — the node shape, the taxonomy names and which principles enter are Dave's, decided against the plan that follows this report.

## THE DELIVERABLE (all five, or say which is UNPROVEN and why)

1. **A SOURCE REGISTER** — `assets/…/source-register.json` + a table in the report. One row per source FAMILY: name · author/steward · year (first + latest revision) · canonical URL (FETCHED, not recalled) · what it is (law set / heuristic set / legal standard / catalogue / single principle) · item count · licence (quoted from the page) · relevance to Apollo (one line). Start from the candidate list below; **find at least eight more families the list does not name** and say how you found them.

2. **A PRINCIPLE REGISTER** — `assets/…/principle-register.json` + a table. One row per principle (target ≥ 80 rows; Laws of UX alone is 30). Fields: our-words statement (≤ 25 words, NEVER the source's wording) · source family · originator + year · **evidence grade** (see the ladder below) · the strongest primary study or refutation you could FETCH, with URL · scope conditions (what population / device / task it was shown on) · known misreadings.

3. **THE EVIDENCE LADDER, APPLIED.** Grade every principle:
   - **A — quantitative law**, replicated, with a predictive model (Fitts 1954, Hick–Hyman, Accot–Zhai steering).
   - **B — replicated experimental effect** (Von Restorff; serial position; peak-end; aesthetic-usability — Kurosu & Kashimura 1995 / Tractinsky et al. 2000).
   - **C — expert heuristic with wide practitioner consensus, thin direct experiment** (Nielsen's 10; Norman's principles; Shneiderman's rules; GOV.UK principles).
   - **D — contested, misapplied or folk** (Miller's 7±2 as applied to menus — Cowan's 4±1 and Miller's own caveat; the Doherty threshold's 1982 evidence base; choice overload after Scheibehenne et al. 2010's meta-analysis; the "three-click rule" after Porter 2003; the F-pattern as a design rule).
   - **L — legal or regulatory requirement, not a heuristic** (WCAG 2.2 / EN 301 549 / European Accessibility Act 2025; UK FCA Consumer Duty "consumer understanding" outcome; PSD2/SCA friction rules where they touch UI). A designer's brain must know the difference between "wise" and "mandatory".
   Where a grade is arguable, say why and give the alternative grade — do not smooth.

4. **THE TENSION MATRIX** — `assets/…/tensions.json` + a table. Every pair (or triple) of principles that pull opposite ways, with the **mediating variable** that decides which wins (user expertise · frequency of use · task criticality · regulatory context · brand · device). Minimum twenty. Seeds: Jakob's Law vs Von Restorff / brand distinctiveness · Hick's Law vs Tesler's Law (complexity is conserved — where does it go?) · aesthetic-usability vs honesty (aesthetics masking usability defects — Yablonski's own caveat) · Doherty <400 ms vs Nielsen's 0.1/1/10 s vs the labour illusion (Buell & Norton 2011) · Postel's Law vs strict validation and security · peak-end vs consistency of investment · Fitts (big, near targets) vs information density · flow vs notification/selective attention · goal-gradient vs Zeigarnik · paradox of the active user vs onboarding tours · Pareto vs long-tail needs · Occam vs Tesler · choice overload vs autonomy and its own contested evidence. **Contradictions are the finding, not a defect — list them raw.**

5. **APOLLO TOUCHPOINTS + IDEAS SURFACED** — two short sections. (a) Ten existing Apollo rulings or patterns that a principle explains or challenges — e.g. the two-red law (one thing differs, Von Restorff; but ALSO contrast law, grade L), keylines hugging modules (Common Region), bento module counts (chunking, NOT Miller), chart hover latency (Doherty vs Nielsen). Read them from `knowledge/_rulings.json` and `knowledge/component-types.json`; quote the id you matched. PROPOSE the mapping, never inscribe it. (b) **Ideas for other tasks** the research surfaced — Dave's standing instruction at #236: *"and ideas for other tasks, lets not miss that."* One line each, with what it depends on.

## GROUND FIRST (~20 min, before searching)

`knowledge/_rulings.json` (grep `s151-D1`, `s149-D1`, `s217`, `s220`, `s234-D1`…`D6` for the rulings the touchpoints section names) · `knowledge/component-types.json` (the pattern vocabulary) · `notes/_briefs/2026-09-02-234-v106-brief.md` (the generation-chain principle: KG = brain, consumers DERIVED — your register is raw material for KG nodes, so shape the JSON so a generator could read it) · `notes/_subreports/_TEMPLATE.md` (copy it; never write into it) · `notes/_subreports/2026-09-02-235-L1-receipt-gate.md` (a filed report done right — match its rigour).

## CANDIDATE SOURCE FAMILIES (a starting list, NOT the register — verify each, drop what does not hold, add what is missing)

Laws of UX (Yablonski; 30; **CC BY-NC-ND 4.0 — no derivatives, non-commercial: own words only, cite the page**) · Nielsen's 10 usability heuristics (NN/g, 1994/2020) · Norman, *The Design of Everyday Things* principles (affordance, signifier, feedback, constraint, mapping, consistency, discoverability) · Gestalt principles (Wertheimer 1923; Koffka) · Shneiderman's Eight Golden Rules · Tognazzini's First Principles of Interaction Design · ISO 9241-110 dialogue principles + ISO 9241-210 · Gerhardt-Powals cognitive engineering principles (1996) · WCAG 2.2 (POUR) · EN 301 549 · European Accessibility Act (in force June 2025) · UK FCA Consumer Duty (PS22/9) · deceptive-design / dark-pattern taxonomies (Brignull; Gray et al. 2018; OECD 2022) as ANTI-principles · Nielsen's response-time limits (1993) · Cowan 2001 working-memory capacity · Fitts 1954 + MacKenzie's Shannon formulation + touch-target guidance (Apple HIG 44 pt, Material 48 dp, WCAG 2.5.8 24 px) · Hick 1952 / Hyman 1953 · Accot–Zhai steering law 1997 · Kahneman & Tversky / cognitive-bias catalogues (Wikipedia list; Benson's codex) · Fogg Behaviour Model · Cialdini's persuasion principles (flag the ethics line) · GOV.UK Design Principles + Service Manual · Apple Human Interface Guidelines principles · Material Design principles · Tufte / Cleveland & McGill / Few for data visualisation (Apollo's charts pillar) · Bringhurst / Butterick typography rules (measure 45–75 characters, etc.) · Krug, *Don't Make Me Think* · Weinschenk, *100 Things Every Designer Needs to Know About People* · Buell & Norton 2011 (labour illusion) · Porter 2003 (three-click rule refutation) · Iyengar & Lepper 2000 vs Scheibehenne, Greifeneder & Todd 2010 (choice overload).

## METHOD RULES (rigour is the brief)

- **Every citation is FETCHED in this lane and quoted** (one line, ≤ 15 words, in quotation marks, with the URL). A source you could not fetch is `UNPROVEN: could not fetch <url>` — never a memory citation. [[feedback-measuring-tool-must-not-guess]]
- **Primary over secondary.** For grades A/B name the study; for C name the steward's page; for L quote the clause number.
- **Our words, always.** Yablonski's text is ND-licensed; NN/g is copyrighted. Statements are yours, ≤ 25 words. Quotes only as receipts.
- **Name what you did NOT cover** in a closing section — a declared gap passes, a silent one fails.
- **Hunt refutations as hard as confirmations.** For every grade A/B principle, search "<principle> replication" and "<principle> criticism" and record what came back, even when nothing did (an unrun search ≡ an absent record).

## DO NOT RULE

No node schema, no taxonomy names beyond the ladder letters above (they are the conductor's working labels, not canon), no decision on which principles ENTER the graph, no edits to `knowledge/` or any canon file, no licence policy beyond what is stated here, no re-wording of any `s2xx-D*`. You PROPOSE in the report; Dave rules against the plan.

## FILING

Copy `notes/_subreports/_TEMPLATE.md`; `sub index` = `R1`; `brief:` = this file. Counts line: **families N · principles N · graded A/B/C/D/L = n/n/n/n/n · tensions N · touchpoints N · ideas N · UNPROVEN N.** Close with **REPLAY-THESE** (≤ 7 lines the conductor must read verbatim). Token spend: `UNMEASURED — no message.usage at a sub's seat`, plus the SHAPE (tool calls, fetches, pages read).

## PITFALLS (consequences replayed, #165)

- **A hallucinated citation poisons the whole register** — one invented DOI and Dave cannot trust any row. Fetch or mark UNPROVEN. This is the single most likely failure of a research sub.
- **Copying licensed wording turns a knowledge asset into a liability** for a commercial bank. Own words; quotes as receipts only.
- **A heuristic graded as a law becomes a false constraint in the generator** — the grade is the product; when in doubt, grade DOWN and say why.
- **Smoothing a contradiction hides the exact judgment the brain needs** — the tension AND its mediator are the value.
- **Scope creep into building** — no JSON in `knowledge/`, no schema. Raw material only.
- **Big page dumps** — fetch with a character cap; never read a 100 KB page into context whole. [[sandbox-call-boundary-kills]] applies to the shell (~178 s per call).
- **An unmatched grep is not an absence** — when you say Apollo "has no" something, name the probe and quote the empty result.
- **The report is the authority; the stub copies it** — every figure in your closing message is copied off the file.
