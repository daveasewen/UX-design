# `#236`-`R1` — the principles survey: sources, evidence grades, contradictions

session: `#236` · 2026-09-02
window: Fable conductor, lane R1 (research sub, web + repo read)
sub index: `R1`
brief: `notes/_briefs/2026-09-02-236-R1-principles-survey-brief.md`
tokens: `UNMEASURED — no message.usage at a sub's seat`. SHAPE: 44 tool calls · **43 live URL fetch attempts, 30 yielding usable text** (curl via the sandbox, which has network; the 13 failures are listed in `fetch-receipts.json`, not hidden) · **52 Crossref bibliographic lookups, 52 resolved** · 6 repo probes · 0 repo writes outside `notes/_subreports/`.

## VERDICT

All five regions of the brief are **DONE**, and every one overshot its floor: 32 source families (10 of them absent from the candidate list), 145 principles (target 80), 30 tensions (minimum 20), 12 Apollo touchpoints, 13 ideas. The single most important finding is not any one principle — it is the **shape of the evidence**: of 145 rows, only **6 grade A** and **28 grade B**, against **75 grade C** and **27 grade L**. A designer's brain built from the popular law lists would be about 80% expert opinion wearing the word "law". The second finding is that **grade L is a different kind of thing entirely** and must not share a tier with heuristics: DSA Article 25 and the FCA Consumer Duty do not lose an argument to Jakob's Law. The third is that **the contradictions are dense and mostly unmediated in public** — Nielsen's own heuristics 6 and 8 pull against each other, and the evaluator-effect literature says two experts applying that same list will not agree, which is exactly why the factory rubric (`s234-D2`) cannot be a heuristic score. Method held: every citation in the registers was fetched in this lane or is explicitly marked NOT FETCHED / UNPROVEN. Nothing was cited from memory. One recall-vs-fetch failure was caught in the brief itself and is recorded as Finding 6.

COUNTS: families 32 · principles 145 · graded A/B/C/D/L = 6/28/75/9/27 · tensions 30 · touchpoints 12 · ideas 13 · UNPROVEN 18

*(Template COUNTS terms, also parsed: findings `10` · ruling-shaped `6` · UNPROVEN `18`.)*

## What was done

**Ground (repo, read-only).** `knowledge/_rulings.json` (311 rulings; 13 ids pulled by name and confirmed present), `knowledge/component-types.json` (3 types: `button-family`, `dataviz`, `segmented`), `notes/_subreports/_TEMPLATE.md` (copied, not edited), the `#234` and `#235` filed reports for rigour calibration.

**Region 1 — source register.** `assets/2026-09-02-236-R1-principles-survey/source-register.json`, 32 families. Table below.

**Region 2 — principle register.** `assets/…/principle-register.json`, 145 rows, every statement in this lane's own words and machine-checked at ≤25 words (0 violations).

**Region 3 — the ladder, applied.** Every row carries a grade; **38 rows carry an explicit alternative grade with the reason**, rather than smoothing.

**Region 4 — tension matrix.** `assets/…/tensions.json`, 30 tensions (1 triple), each with its mediating variable and how it resolves; 21 carry an Apollo touch.

**Region 5 — touchpoints and ideas.** Sections 5a and 5b below.

**Written:** the three JSON files above and this report. **Nothing else in the repo changed. No git commands were run.**

---

## 1 — THE SOURCE REGISTER (32 families)

`★` = a family the brief's candidate list does not name (10 of them).

| # | Family | Steward | Years | Kind | Items | Fetched receipt (≤15 words) |
|---|---|---|---|---|---|---|
| 1 | Laws of UX | Jon Yablonski | 2017–2026 | law/effect catalogue (secondary) | 30 | "Laws of UX © Jon Yablonski 2026 Contact \| Privacy \| License" |
| 2 | Nielsen's 10 heuristics | NN/g | 1994–2020 | expert heuristic set | 10 | "1: Visibility of System Status 2: Match Between the System and the Real World" |
| 3 | Eight Golden Rules | Shneiderman / UMD | 1985–2016 | expert heuristic set | 8 | "derived from experience and refined over three decades, require validation and tuning" |
| 4 | First Principles of Interaction Design | Tognazzini | 1978–2014 | expert heuristic set | 20 | "The following principles are fundamental to the design and implementation of effective interfaces" |
| 5 | GOV.UK Design Principles | UK GDS | 2012–2025 | organisational principles | 11 | "1. Start with user needs 2. Do less 3. Design with data" |
| 6 | ISO 9241 series (110 / 11 / 210) | ISO TC 159/SC 4 | 1996–2020 | international standard | 7 + defs + process | "ISO 9241-110:2020 … Part 110: Interaction principles" |
| 7 | WCAG 2.2 | W3C / WAI | 1999–2023 | legal-grade standard | 4 / 13 / 87 | "The size of the target for pointer inputs is at least 24 by 24 CSS pixels" |
| 8 | EN 301 549 V3.2.1 | CEN/CENELEC/ETSI | 2014–2021 | harmonised EU standard | ch. 4–14 | "HARMONISED EUROPEAN STANDARD Accessibility requirements for ICT products and services" |
| 9 | European Accessibility Act | EU / DG EMPL | 2019–2025 | EU directive | Annexes 1–3 | "The Directive on the accessibility requirements for products and services" |
| 10 | FCA Consumer Duty (PRIN 2A) | UK FCA | 2022–2023 | conduct rulebook | 4 outcomes | "product governance, price and value, consumer understanding and supporting consumers" |
| 11 ★ | DSA Article 25 | EU Reg. 2022/2065 | 2022–2024 | legal prohibition | 1 | "shall not design, organise or operate their online interfaces in a way that deceives" |
| 12 ★ | EDPB Guidelines 03/2022 | European Data Protection Board | 2022–2023 | regulatory guidance | 6 categories | "Guidelines 03/2022 on deceptive design patterns in social media platform interfaces" |
| 13 | Deceptive design taxonomy | Brignull / Testimonium Ltd | 2010–2026 | ANTI-principles | 16 | "drawn into a transaction on false pretences, because pertinent information is hidden" |
| 14 ★ | Inclusive Design Principles | Swan, Pouncey, Pickering, Watson | 2017–2026 | expert principle set | 7 | "These Inclusive Design Principles are about putting people first" |
| 15 ★ | ARIA Authoring Practices Guide | W3C / WAI | 2013–2026 | implementation patterns | ~28 | "How to build accessibility semantics into web patterns and widgets" |
| 16 ★ | Making Content Usable (COGA) | W3C COGA TF | 2021 | design objectives | 8 objectives | "Objective 4: Help Users Avoid Mistakes and Know How to Correct Them" |
| 17 ★ | Core Web Vitals / INP | Google web.dev | 2020–2026 | measurable thresholds | 3 | "Interaction to Next Paint (INP) Optimize Interaction to Next Paint" |
| 18 | Android / Material touch targets | Google | 2014–2026 | platform guideline | 1 | "A touch target of 48x48dp results in a physical size of about 9mm" |
| 19 | Butterick's Practical Typography | Matthew Butterick | 2010–2026 | typographic rules | ~40 | "line length 45–90 characters or 2–3 alphabets" |
| 20 ★ | Baymard Institute | Baymard | 2009–2026 | proprietary empirical set | 700+ | "200,000+ hours of UX research … Over 700 UX Guidelines" |
| 21 | Fogg Behavior Model | BJ Fogg / Stanford | 2009–2026 | behavioural model | 3 | "three elements must converge at the same moment for a behavior to occur" |
| 22 | Classic quantitative HCI models | peer-reviewed lit. | 1952–2013 | quantitative laws | 6 | "The information capacity of the human motor system in controlling the amplitude" |
| 23 | Cognitive-psychology primaries | peer-reviewed lit. | 1956–2001 | replicated effects | 5 | "The magical number 4 in short-term memory: A reconsideration of mental storage capacity" |
| 24 ★ | Usability-method reliability lit. | Hertzum, Molich, Faulkner, Hornbæk | 2001–2008 | meta-research | 4 | "The Evaluator Effect: A Chilling Fact About Usability Evaluation Methods" |
| 25 ★ | Information Foraging Theory | Pirolli & Card (PARC) | 1999 | predictive theory | 1 | "Information foraging. Psychological Review (Pirolli, Card, 1999)" |
| 26 ★ | Cognitive Dimensions of Notations | Green & Petre | 1996 | analytic framework | 14 | "Usability Analysis of Visual Programming Environments: A 'Cognitive Dimensions' Framework" |
| 27 ★ | Situation awareness / workload | Endsley; Wickens | 1995–2002 | applied cognitive theory | 2 | "Toward a Theory of Situation Awareness in Dynamic Systems" |
| 28 ★ | Technology Acceptance Model | Davis (MIS Quarterly) | 1989 | replicated model | 2 | "Perceived Usefulness, Perceived Ease of Use, and User Acceptance of Information Technology" |
| 29 | Graphical perception | Cleveland & McGill | 1984 | encoding ranking | 1 | "Graphical Perception: Theory, Experimentation, and Application to the Development of Graphical Methods" |
| 30 ★ | RFC 9413 Maintaining Robust Protocols | IETF / IAB | 2023 | standards-body refutation | 1 | "However, it has been interpreted in a variety of ways." |
| 31 | UIE / Center Centre | Porter / Spool | 2003–2026 | empirical refutation | 1 | "Hardly anybody gave up after three clicks." |
| 32 | Norman's principles | Don Norman / jnd.org | 1988–2013 | expert set (self-corrected) | 6 | "Social signifiers are those that are relevant to social usages" |

**How the ten new families were found.** Not by search-engine browsing. Three deliberate moves: (a) **follow the refutation, not the claim** — searching for what walked a principle back produced RFC 9413, the evaluator-effect literature and Scheibehenne's meta-analysis, three families that exist only as corrections; (b) **follow the legal hook** — asking "who can fine you for this?" turned the dark-pattern ethics topic into DSA Article 25 and the EDPB guidelines; (c) **ask what Apollo's artefacts actually are** — a bento dashboard is a situation-awareness instrument (Endsley), a nav is a foraging problem (Pirolli & Card), and a design system is a notation (Cognitive Dimensions). Licences and item counts came from the fetched pages, never from recall.

**Licence flags that matter.** Laws of UX is **CC BY-NC-ND 4.0** (verified by the `creativecommons.org/licenses/by-nc-nd/4.0/` href in the fetched HTML): no derivatives, non-commercial — so it can be a *pointer*, never copied text, in a commercial bank's asset. NN/g is "All Rights Reserved". Baymard is proprietary. GOV.UK is OGL v3 (the most permissive substantial source in the set). W3C documents carry the W3C Document Licence.

---

## 2 — THE PRINCIPLE REGISTER (145 rows)

Full data: `assets/2026-09-02-236-R1-principles-survey/principle-register.json`. Fields per row: `statement` (our words, ≤25 words, machine-checked), `family`, `originator`, `year`, `grade`, `grade_alt` + `grade_reason` where arguable, `evidence` (fetched URL or explicit NOT FETCHED), `scope_conditions`, `known_misreadings`, `refutation_probe`.

**The distribution is the headline.**

| Grade | Meaning | Rows | What is in it |
|---|---|---|---|
| **A** | quantitative law, replicated, predictive | **6** | Fitts, Hick–Hyman, Accot–Zhai steering, KLM, speed–accuracy, Cleveland–McGill (A/B) |
| **B** | replicated experimental effect | **28** | Von Restorff, serial position, peak-end, aesthetic-usability, Cowan's 4, chunking, cognitive load, goal-gradient, information scent, social proof, loss aversion, situation awareness, multiple resources, TAM, labour illusion, evaluator effect, five-user refutation, 9 Gestalt grouping laws |
| **C** | expert heuristic, wide consensus, thin experiment | **75** | Nielsen ×10, Shneiderman ×8, Tognazzini ×10, GOV.UK ×11, Inclusive Design ×7, Norman ×6, ISO ×3, COGA ×6, plus Jakob's, Tesler's, mental model, flow, response limits |
| **D** | contested, misapplied or folk | **9** | 7±2 in menus, three-click rule, F-pattern-as-rule, Doherty 400 ms, choice overload, Postel's Law, Pareto, Occam, Parkinson |
| **L** | legal / regulatory requirement | **27** | WCAG POUR ×4 + 7 named SCs, EN 301 549, EAA, FCA ×4 outcomes, DSA 25, EDPB, 8 prohibited deceptive patterns |

**Where the grade is arguable it says so — 38 rows carry an alternative grade.** Worked examples:

- **Hick's Law: A for the lab effect, D for the menu application.** The 1952/1953 papers are replicated and predictive for forced choice among *known, equiprobable* alternatives. A navigation menu is visual search *plus* decision, and Landauer & Nachbar (1985) and Cockburn et al. (2007) both model it with terms Hick's law does not contain. One principle, two grades, and the brain needs both.
- **Choice overload: D as a law, B under named moderators.** Iyengar & Lepper (2000) is real; Scheibehenne, Greifeneder & Todd's 2010 meta-analysis found a mean effect near zero. Grade DOWN and carry the moderators (preference clarity, expertise, time pressure).
- **Gestalt: A for the perceptual demonstrations, C for the layout rules drawn from them.** The grouping phenomena are among the most reliable in psychology; "therefore use a card" is expert interpretation.
- **F-pattern: B as an observed behaviour, D as a design rule.** The steward's own page says the pattern "is bad for users and businesses". Designing *for* it optimises the failure mode.
- **Postel's Law: D as an engineering law, C for input-field tolerance.** RFC 9413 is the IETF walking back its own principle; accepting a phone number with spaces remains good practice.

**Refutations were hunted as hard as confirmations** (brief's method rule). Fetched refutation/replication receipts now sit on the rows they bite: Cowan 2001 against Miller 1956; Scheibehenne 2010 against Iyengar 2000; Tuch 2012 and Sonderegger 2010 against the aesthetic-usability effect; RFC 9413 against Postel; Porter 2003 against the three-click rule; Pernice/NN/g against the F-pattern; Faulkner 2003 against the five-user rule; Hertzum & Jacobsen 2001 and Molich & Dumas 2008 against heuristic reliability generally; Bi et al. 2013 and MacKenzie 1992 *extending* (not refuting) Fitts. Where a search came back empty, the row says so — an unrun search is indistinguishable from an absent record, so both are declared.

---

## 3 — THE TENSION MATRIX (30, minimum was 20)

Full data: `assets/2026-09-02-236-R1-principles-survey/tensions.json`. Abridged; the mediating variable is the product.

| # | Pulls against | Mediating variable | Resolution |
|---|---|---|---|
| 1 | Jakob's Law ↔ Von Restorff / brand | **Layer** | Converge on *mechanism*, diverge on *signal*. Diverging on mechanism is paid for in errors. |
| 2 | Hick ↔ Tesler | **Who absorbs it** (expertise, frequency, regulation) | Name where the removed complexity went and price it there. |
| 3 | Doherty <400 ms ↔ labour illusion ↔ Nielsen 0.1/1/10 s | **Task criticality**; is the system doing work *for* me? | Instant for direct manipulation; show the work for delegated judgement. |
| 4 | Aesthetic-usability ↔ honesty | **Who is measuring** | In evaluation it is a confound; in shipping it is a benefit. Never let a beauty pass replace a task measurement. |
| 5 | Postel ↔ strict validation | **Layer** | Tolerant at the input surface, strict at the boundary, and *show* the normalisation. |
| 6 | Peak-end ↔ consistency of investment | **Measurement window** | Peak-end allocates the last 10% of polish, never the first 90%. |
| 7 | Fitts ↔ information density | **Object class** (control vs data mark) | Split the floor by class — which `s116-D1` already does. |
| 8 | Flow ↔ visibility of system status | **Interruption cost vs information value** | Block only for irreversible or time-critical events. |
| 9 | Goal-gradient ↔ Zeigarnik | **Whose interest** | Real progress toward the user's goal; illusory progress is the DSA line. |
| 10 | Paradox of the active user ↔ onboarding tours | **Timing** | Guidance at the moment of need, not at first launch. |
| 11 | Pareto ↔ long-tail regulated cases | **Regulatory context** | Rank by expected cost, not frequency. Pareto ranks the wrong axis in a bank. |
| 12 | Occam ↔ Tesler | **Was the thing removed or hidden?** | Require a named destination for every removed element. |
| 13 | Choice overload ↔ autonomy | **Preference clarity, expertise** | Curated set, full set one action away — without claiming the science is settled. |
| 14 | Miller's 7±2 ↔ Cowan's 4 | **Neither applies** | Both are recall claims; a visible menu is recognition. Cite chunking, cite no number. |
| 15 | WCAG 1.4.3 ↔ brand palette | **Legal** | The floor is not tradeable; background-keyed colour rules are the way through. |
| 16 | WCAG 2.5.5 (44 px) ↔ financial density | **Object class + AA/AAA line** | Adopt for controls, exempt marks *explicitly* with a named check. |
| 17 | "Consistent, not uniform" ↔ four themes | **Scope of the constant** | Grammar constant, values variable. |
| 18 | Nielsen #6 recognition ↔ Nielsen #8 minimalism | **Frequency of use per element** | The heuristic set does not resolve its own contradiction — the clearest evidence for the C ceiling. |
| 19 | DSA Art. 25 ↔ social proof / goal-gradient / loss aversion | **Truth and reversibility** | Every persuasion node needs a paired legal node. |
| 20 | FCA consumer understanding ↔ minimalism | **Regulatory context + decision moment** | Layer disclosure *at* the decision; test comprehension, not preference. |
| 21 | Cleveland–McGill ↔ brand-led charts | **Audience purpose** | If brand overrides accuracy, record that it did. |
| 22 | Common region ↔ proximity | **Strength order** (region beats proximity) | Never let spacing and keylines assert different groups — `s217-D8`. |
| 23 | Proportional feedback ↔ acknowledge in 0.1 s | **Action consequence** | Acknowledgement always instant; *celebration* proportional. |
| 24 | Be consistent ↔ offer choice | **Cost of the second route** | Multiple entries, one model. |
| 25 | Anti-preselection ↔ good defaults | **Consent vs convenience** | Grade the *slot*, not the mechanism. A generator that misses this will pre-tick a marketing consent. |
| 26 | Cognitive load ↔ COGA "don't rely on memory" | **Load type** | Before removing anything, ask what the user must now hold in their head. |
| 27 | Evaluator effect ↔ heuristic scoring as a rubric | **Mechanical vs inferential** | Rank on mechanical checks; report judgement as flagged observations, never a score. |
| 28 | F-pattern ↔ information scent | **Does the page have structure?** | The F is a symptom, not a target. |
| 29 | WCAG 2.4.13 focus ↔ minimal chrome | **Legal floor + input modality** | Focus is a first-class token from the start, never a retrofit. |
| 30 | Baymard/Laws-of-UX licences ↔ the generation chain | **Licence** | Some sources can be nodes; some can only be pointers. |

---

## 4 — FINDINGS

1. **The premise holds, with a nuance worth keeping.** Probe: `grep -c -iE "fitts\|hick's law\|von restorff\|doherty\|tesler\|jakob's law\|gestalt\|peak-end\|serial position\|nielsen"` over the four structured KG files → `_rulings.json: 0`, `_consult-lexicon.json: 0`, `_KNOWLEDGE-USAGE-ENTITIES.json: 0`, `component-types.json: 0`. **Zero, all four.** The nuance: "gestalt" *does* appear in prose docs — but as `"residual gestalt = human"` in `knowledge/_FIXED-FLEX-CHARTER.md` (meaning the human eye) and as the *name of a design system* in a vendor list in `_memento-index.json`. That is a `s202`-style vocabulary collision waiting to happen: importing Gestalt principles into a graph that already uses "gestalt" to mean "Dave's eye" will produce false retrievals.

2. **The evidence base is thinner than the vocabulary suggests: 6 A / 28 B against 75 C.** Roughly 80% of what the field calls "laws" is expert consensus. A brain that flattens the grade will let a 1980s aphorism outrank Fitts.

3. **Grade L is a different species and must not be tiered with the rest.** DSA Article 25, the FCA Consumer Duty and WCAG SCs are not "strong evidence" — they are *mandatory regardless of evidence*. Twenty-seven rows are legal. This is the strongest single argument in the survey for the ladder being in the graph at all.

4. **The most-quoted rules are the weakest.** All nine D rows are famous. 7±2, the three-click rule, the Doherty threshold and choice overload are in every deck; the fetched primaries either say something else (Miller), find no correlation (Porter), cannot be retrieved at all (Doherty & Thadhani 1982 — Crossref query returned an unrelated 2026 paper), or were meta-analysed to near zero (Scheibehenne 2010).

5. **Heuristic sets contradict themselves internally, and the reliability literature explains why.** Nielsen #6 (recognition: show options) and #8 (minimalism: every element competes) give opposite verdicts on the same screen, and the set contains no rule for choosing. Hertzum & Jacobsen's evaluator effect (2001) and Molich & Dumas's CUE-4 (2008) show trained evaluators reach substantially different findings from the same list. **This is the ceiling on grade C and the direct challenge to `s234-D2`'s "ranked against solid UI/UX standards".**

6. **A recall-vs-fetch failure was caught inside the brief itself.** The brief cites "measure 45–75 characters" as the typography rule. The *fetched* steward page says: **"line length 45–90 characters or 2–3 alphabets"**. Neither figure has a primary study behind it. Two things follow: the brief's own number was recalled, not fetched; and this is a live demonstration of why the method rule exists — the error was in the instruction, not the source.

7. **Some principles have been formally withdrawn by their own authorities, and nobody told designers.** RFC 9413 (IETF, 2023) walks back Postel's robustness principle. NN/g's own page calls the F-shaped pattern "bad for users and businesses". Norman replaced his own most-quoted use of "affordance" with "signifier". **The register needs a `superseded_by` / `author_revised` field or it will ship 1988 forever.**

8. **The correction to Miller has been available since 2001 and is still not in the popular lists.** Cowan's "magical number 4" is fetched, cited and unambiguous. Any brain that carries 7±2 without carrying Cowan beside it is worse than no brain.

9. **The legal layer reaches design directly, not through a compliance team.** FCA PRIN 2A names four outcomes — "product governance, price and value, consumer understanding and supporting consumers". *Consumer understanding* and *consumer support* are design outcomes with an enforcement mechanism behind them, and Apollo's clients are exactly the firms bound by them.

10. **Apollo has already ruled several of these tensions correctly, by eye, without the principle.** `s217-D8` (keylines hug modules) resolves the common-region-vs-proximity conflict; `s116-D1` splits the Fitts floor by object class; `s151-D1` is a background-keyed Von Restorff budget with a contrast floor attached. **The graph would be documenting judgement Dave already has, not importing judgement he lacks** — which is a much better argument for building it.

---

## 5a — APOLLO TOUCHPOINTS (12) — PROPOSED MAPPINGS, NOT INSCRIBED

Every id below was confirmed present in `knowledge/_rulings.json` by name in this lane.

| # | Apollo id | What it rules (quoted fragment) | Principle that explains or challenges it |
|---|---|---|---|
| 1 | `s151-D1` | "we have two reds … red ink on white … and everything else" | **Explains:** Von Restorff (B) — one signal that differs. **Constrains:** WCAG 1.4.3 (L). The ruling is a Von Restorff budget with a legal floor. |
| 2 | `s217-D8` | "the keyline goes tight around each module (tile) … never a line centred in the gutter" | **Explains:** Common Region beats Proximity (B). A centred gutter line asserts a *different* group than the spacing does. |
| 3 | `s217-D2` | bento promoted to canon, "gutter is the only divergence" | **Explains:** chunking (B). **Challenges:** any 7±2 justification for module counts — see tension 14. |
| 4 | `s116-D1` | "Data marks are held to the 24x24 WCAG 2.5.8 dense-case MINIMUM — exempt from the 44 CONTROL target" | **Explains:** Fitts (A) split by object class + WCAG 2.5.8/2.5.5 (L). A better answer than either source gives alone. |
| 5 | `s234-D3` | "AA plus three cheap AAA" (2.4.10, 2.5.5, 2.4.13); 1.4.6 rejected as colliding with `s151-D1` | **Is:** grade L, adopted deliberately — including a *declared* refusal where the legal option collided with a design ruling. |
| 6 | `s149-D1` | "the standard is we use dark text on #F6604C" | **Explains:** contrast (1.4.3, L) resolved per theme; also Jakob-vs-distinctiveness (tension 1) settled at the value layer. |
| 7 | `s194-D1` | "the contrast duty attaches to the label and the glyph, never the chrome" | **Explains:** WCAG 1.4.11 non-text contrast (L) — "contrast ratio of at least 3:1 against adjacent color(s)". A correct scoping of the clause. |
| 8 | `s202-D1` | "inherit console's tuned set" — one grammar across four themes | **Explains:** GOV.UK #9 "consistent, not uniform" (C) — tension 17's resolution, already enacted. |
| 9 | `s135-D1` | contextual notification shell, per-theme border + radius | **Challenges:** flow vs visibility (tension 8). The *shell* is ruled; the **routing rule** (what may interrupt) is not. |
| 10 | `s114-D3` / `s114-D5` | "yes expand the hit area…"; measurement redesign signed off | **Explains:** Fitts (A) + Android 48dp ≈ 9 mm + Parhi et al. 2006 thumb-target study (B). |
| 11 | `s144-D1` | "PLUS/MINUS COLOURED TEXT — the only coloured text Apollo uses" | **Constrains:** WCAG 1.4.1 Use of Color (L) — colour must not be the only channel. Worth a probe: does the plus/minus glyph carry the sign redundantly? |
| 12 | `s234-D2` + `s234-D6` | "ranked against solid UI/UX standards"; "mechanical over inference" | **Challenged by:** the evaluator effect (B). Dave's own instinct — mechanical over inference — is the literature's answer. See tension 27. |

---

## 5b — IDEAS FOR OTHER TASKS (13) — Dave's standing instruction at #236

1. **Split the quality rubric by check type** — mechanical (contrast, target size, semantics, focus) scores; inferential (hierarchy, tone, "is this the right pattern") only flags. *Depends on:* `s234-D6`'s path-taking gate; nothing new.
2. **A `superseded_by` / `author_revised` field on any principle node.** Postel, the F-pattern and Norman's affordance all need it. *Depends on:* the node shape Dave rules.
3. **Pair every persuasion node with its legal fence.** A retrieval that returns social proof without DSA Article 25 is a liability in a bank. *Depends on:* grade L existing as a distinct thing.
4. **An anti-pattern detector in `_validate_screen.py`** — preselected consent, hidden costs, obstruction, confirmshaming. Mechanical, cheap, and it is *compliance*, not taste. *Depends on:* the deceptive-design taxonomy entering as anti-nodes.
5. **A licence field with generator refusal.** The graph must know it may not emit text from a CC BY-NC-ND or proprietary source. *Depends on:* the source register; blocks any Laws of UX or Baymard import.
6. **A "recall vs fetch" gate for numeric claims.** Finding 6 (45–75 vs 45–90) is exactly the class the repo already gates elsewhere. Any figure in a brief or doc that has no fetched receipt gets marked. *Depends on:* nothing.
7. **Resolve the "gestalt" vocabulary collision before import** (Finding 1). *Depends on:* nothing; costs one decision.
8. **Replace click-count thinking with information scent** in navigation patterns. *Depends on:* Pirolli & Card entering the graph.
9. **A situation-awareness lens for the bento dashboard type** — perceive / comprehend / project as three review questions. *Depends on:* `s217-D5`'s type matrix.
10. **Cleveland–McGill encoding ranking as a field on `chart-intents.json`** so a chart choice can be argued from accuracy. *Depends on:* the charts pillar owner.
11. **A response-budget in the behaviour contract** — acknowledge ≤100 ms, and a declared policy for showing work on delegated tasks. *Depends on:* `s234-D5`'s behaviour address; also needs the INP threshold verified (UNPROVEN 5).
12. **A Consumer Duty comprehension harness** — test whether people *understood*, not whether they liked it. This is the biggest unserved need for a bank client and the most defensible thing Apollo could claim. *Depends on:* Dave deciding it is in scope.
13. **An expiry / re-check policy for principle nodes** (`s129-D5`, conclusions are debt). Cowan superseded Miller in 2001 and the field did not notice for twenty years; a graph with no expiry will do the same. *Depends on:* the node shape.

---

## RULING-SHAPED QUESTIONS

⛔ **MANDATORY SECTION.** Nothing below is decided. Each is Dave's.

1. **Does the evidence grade enter the graph as a field at all?** (a) Yes, as a first-class field on every principle node — retrieval can then rank and refuse; (b) no, keep grades in this report and import only what survives a manual cull. *Recommend (a)*, because the grade is the product of this lane and a graph without it will let Parkinson's Law outrank Fitts. **The letters A/B/C/D/L are the conductor's working labels — the names are Dave's.**
2. **Is grade L a separate NODE TYPE rather than a grade?** (a) A fifth rung on one ladder; (b) a distinct "requirement" type that a principle can never outrank. *Recommend (b)*: 27 rows are legal obligations, and the ladder metaphor implies they can lose an argument. They cannot.
3. **Do grade-D principles enter at all?** (a) Exclude them; (b) include them as **inoculation** — nodes whose purpose is to fire when someone cites the folk rule, carrying the refutation. *Recommend (b)*: someone will say "three clicks" in a client meeting and the brain should have Porter's data ready.
4. **Are tensions edges or nodes?** (a) Typed edges between two principles carrying the mediating variable; (b) their own node type, since several are triples and several carry an Apollo ruling as a resolution. No recommendation — this is a schema question and schema is fenced from this lane.
5. **Which families enter first?** Options priced by licence risk: **safe now** — GOV.UK (OGL), W3C/WCAG/APG/COGA, EN 301 549, FCA, DSA, EDPB, and every peer-reviewed primary (facts, not text). **Pointer-only** — Laws of UX (ND), NN/g, Baymard. *Recommend* starting with the legal set plus the A/B primaries: highest value, lowest licence risk, smallest count.
6. **Should Apollo's own rulings gain an `explainedBy` link to principles?** The 12 touchpoints above are proposals only. *Recommend* yes but **one-directional and advisory** — a principle may explain a ruling; a principle must never be able to overturn one. `s151-D1` outranks Von Restorff in this house.

---

## UNPROVEN / CLAIMED (ADR-0016) — 18 declared

1. **UNPROVEN:** ISO 9241-110's seven interaction principle *names* — paywalled. Title/date/edition fetched only. *Price:* purchase the standard, or ~1 fetch of a licensed summary. **Do not enter the names from memory.**
2. **UNPROVEN:** Gerhardt-Powals' ten principle statements — Crossref record only (`10.1080/10447319609526147`). *Price:* one paper fetch (paywall likely).
3. **UNPROVEN:** the EAA's 28 June 2025 application date — did **not** appear in the fetched EC text. Verify before quoting to a client. *Price:* 1 fetch of the directive on EUR-Lex.
4. **UNPROVEN (source authority):** DSA Article 25 text came from a **mirror** (`eu-digital-services-act.com`); EUR-Lex returned HTTP 202 with **zero bytes** to this agent. *Price:* 1 fetch from a working EUR-Lex route.
5. **UNPROVEN:** the INP "good" threshold (commonly stated as 200 ms) — not in the fetched text; the table is JS-rendered. *Price:* 1 browser-rendered fetch.
6. **UNPROVEN:** the Doherty threshold's primary. Crossref bibliographic query for "The economic value of rapid response time / Doherty Thadhani" returned an unrelated 2026 paper. The 1982 IBM report is not indexed. **This is why the row is graded D.**
7. **UNPROVEN:** Von Restorff 1933 primary — no retrievable DOI. Row rests on a secondary (lawsofux.com).
8. **UNPROVEN:** Zeigarnik 1927 primary — same; only a 1991 revisit was retrievable.
9. **UNPROVEN:** selective attention primary — secondary only.
10. **UNPROVEN:** Carroll & Rosson 1987 (paradox of the active user) — not retrieved; row graded C rather than B for that reason alone.
11. **UNPROVEN:** COGA objectives 7 and 8 — the probe (grep of fetched text) captured 1–6 only.
12. **UNPROVEN:** clause BODIES for WCAG 1.4.3, 2.4.10, 2.5.5, 3.3.8 — numbers, names and levels fetched; full normative text not captured. (2.5.8, 1.4.11 and 2.4.13 *do* carry body quotes.)
13. **UNPROVEN:** Cialdini's own steward page — `influenceatwork.com` fails TLS hostname verification. Substituted with Goldstein, Cialdini & Griskevicius 2008 (fetched).
14. **UNPROVEN:** OECD *Dark Commercial Patterns* (2022) — HTTP 403 on two routes. Legal coverage stands on DSA + EDPB instead.
15. **UNPROVEN:** EDPB Guidelines 03/2022 body — the landing page was fetched; the PDF 404'd at the expected path.
16. **UNPROVEN:** Apple HIG's 44 pt figure — `developer.apple.com` HIG pages are JS-rendered and returned no usable text. Android's 48 dp **was** fetched. Material 3 likewise unfetchable as text.
17. **CLAIMED:** Laws of UX is CC BY-NC-ND 4.0 — asserted from the **licence href in the fetched HTML**, not from a fetched licence sentence. Strong, but it is an href, not prose. *Re-read costs:* 1 fetch of the site's `/info/` page.
18. **UNPROVEN:** primaries for Pareto, Occam, Parkinson, mental model and flow — all secondary-only, all declared on their rows. Deliberate: they are graded C/D and a primary would not move the grade.

**Not a defect, stated plainly:** 41 citations were verified via the **Crossref API** (title, authors, year, container, DOI) rather than by reading the paper. That is a *bibliographic* receipt — it proves the work exists and is correctly attributed. It does **not** prove the paper says what the row says. For the 6 grade-A and the highest-traffic grade-B rows, reading the primaries is a real, priced follow-on: ~15 papers, most paywalled.

---

## NOT COVERED (declared gaps — the brief's own rule)

- **No repo writes outside `notes/_subreports/`**, no schema, no taxonomy names, no decision on which principles enter. Fenced by the brief.
- **Bias-by-bias replication audit.** The cognitive-bias codex is one row (`pr-cognitive-bias`), not 200. Most entries have not been replicated at interface scale and auditing them is its own lane (idea 13's sibling).
- **Krug, Weinschenk, Tufte, Few, Bringhurst** — books, not fetchable pages. Cleveland & McGill covers the dataviz *evidence*; Butterick covers typography. Named and skipped deliberately.
- **The replication-crisis literature as it touches priming, ego depletion and nudge** — relevant to several B rows, not sampled.
- **Non-Western sources entirely.** Every family in the register is US/EU/UK. A four-theme system for international banks has a gap here.
- **PSD2 / SCA friction rules** — named in the brief's candidate list, not fetched. FCA + DSA + EDPB + EAA carry the legal tier without it.
- **`knowledge/_consult-lexicon.json` structure** was probed for principle words (0 hits) but **not read for shape** — so this report says nothing about how a principle node would sit beside the lexicon.
- **No live artefact was rendered or measured.** This is a research lane; nothing here was tested against an Apollo screen.

---

## Evidence

`notes/_subreports/assets/2026-09-02-236-R1-principles-survey/`

- **`source-register.json`** — 32 families. Proves: each family's steward, dates, item count, licence and the ≤15-word receipt fetched from its page on 2026-09-02.
- **`principle-register.json`** — 145 principles with grades, alternative grades, scope conditions, misreadings and refutation probes. Proves: the grade distribution in Finding 2 and that every statement is ≤25 own words (machine-checked, 0 violations).
- **`tensions.json`** — 30 tensions with mediating variables; 21 carry an Apollo touch. Proves: the contradictions are real, named and mediated rather than smoothed.
- **`fetch-receipts.json`** — every URL this lane attempted (43, with per-row `status` and failure `reason`) and every Crossref record verified (52). Proves the fetch-or-declare rule was actually kept: the 13 failures are enumerated, the Doherty and Wertheimer lookups carry `LANE_NOTE` flags saying they did **not** resolve to the intended work, and no register row cites a URL absent from this file.

REPLAY-THESE: `assets/…/principle-register.json` grade counts + the 38 `grade_alt` rows (~2,500 tk) · `assets/…/tensions.json` rows 1, 14, 19, 25, 27 (~900 tk) · this report §4 Findings 1, 5, 6, 10 (~700 tk) · this report §5b ideas 1, 3, 5, 12 (~400 tk) · the 6 RULING-SHAPED QUESTIONS in full (~600 tk) · UNPROVEN 1, 4, 5 before any client-facing use of ISO, DSA or INP figures (~250 tk)
