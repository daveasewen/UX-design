# Brief — deck v8, first draft — #289 — 2026-09-19

Three lanes, one deck. Each lane writes ONE fragment file of `<section class="slide …">` blocks and files a
sub-report. The conductor merges the fragments into `notes/_DEMO-SLIDES-apollo-2026-09-19-v8.html`.

## The source deck
`notes/_DEMO-SLIDES-apollo-2026-09-12-v7.html` — 11 slides `s1…s11`, CSS at lines 7–365, slides at 373–568,
fly-through and reveal scripts from 569. READ lines 1–568 in full before writing. Use ONLY the classes that
CSS already defines (`.slide`, `.dark`, `.grey`, `.inner`, `.type`, `.label`, `.lead`, `.body`, `.foot`,
`.rv d1…d5`, `.nums/.cell/.fig`, `.score/.axes`, `.kpi`, `.grid4`, `.chapters`, `.switch`, `.ask`,
`.close-line`, `.count`, `.pagenum`, `.draw`). If a slide truly needs a new rule, put it in ONE
`<style data-lane="G?">` block at the top of your fragment, scoped under that slide's id, ≤ 25 lines.

## Dave's words — quote, never paraphrase (`notes/_lanes/289/DAVE-RULINGS-2026-09-19.md`, and his board
`notes/_lanes/289/DAVE-ARC-BOARD-2026-09-19.png` — look at it)
- The arc: "a set of problem statements (not literal) how they are broken down - light RCA, a solution and
  its constituent parts … this isn't rigid … what we craft around it is ours."
- Board: problems Speed · Consistency · Quality → Speed: governance process, 2-stage process (Figma + code
  library) · All (consistency, fed by all three): small component library, lack of design standards and
  accessibility knowledge, low/variable skills · Quality: lack of data and research, AI generation quality
  (slop) → "Introduce AI to build solutions" → Apollo: gates and evals · full library in code · a graph
  that holds all the tokens, components, standards and compliance · research graph?
- "the research part is something another group is working on, i may be helping them with it but it is
  definitely a problem we have to solve."
- "we have two very interesting artefacts to show, the component library and the explorer, and after -
  hopefully - a build from it."
- "I actually like the parts bin, because people just 'get it' so lets think about how we can get it in
  there, maybe we also have another analogy for the engine or brain, I think of Apollo as a capable
  designer that knows the library, compliance, code, snippets, patterns, context, rulings, artefacts,
  assets, guidelines, Ally rules, governance, regs, usage, UX theory etc... etc... better than any human can"
- "keep the opening slide as it is" — s1 is copied VERBATIM, byte for byte.
- The 25th is an INTERNAL audience, "still very important". Rice-grade rigour, internal room.

## The narrative the conductor proposed and Dave went with ("lets see what the first draught is like")
The parts bin is the PROBLEM (the before: a bin of parts nobody knows end to end → slow, inconsistent,
quality is luck = the three problems in one picture). The DESIGNER is the answer to the bin: Apollo is a
designer who has read everything; the bin doesn't change, what changes is that someone finally knows it.
The two artefacts are her evidence: the LIBRARY (what she builds with), the EXPLORER (what she knows — the
long list is spoken as what she knows, never shown as a list), then the BUILD (what she does with it).
Gates and evals = how you check her work, a beat inside the build / one line on the system slide, not a
fourth part. RESEARCH = on the ask slide, a named problem another group owns, Dave alongside, stated as
owed not solved. Caution ruled: say "knows more than any one human can hold", never "better than any
human" — the build earns the rest.

## The v8 running order (13 slides) and who writes what
| # | id  | slide | lane |
|---|-----|-------|------|
| 1 | s1  | Title — VERBATIM from v7 | G1 |
| 2 | s2  | The strip — rewritten chapters for this arc (keep `kgPrint2`, `.chapters`) | G1 |
| 3 | s3  | The parts bin — kept (keep `<canvas id="gb">` + `gbPrint`), copy re-aimed so the bin IS the three problems | G1 |
| 4 | s4  | NEW · The breakdown (light RCA) — Dave's board as a slide: three problems, what sits under each, the grey "All" insight (consistency is what the other two produce) | G1 |
| 5 | s5  | NEW · The turn — "a designer who knows the bin". One sentence slide. | G1 |
| 6 | s6  | NEW · The library — what she builds with. Facts from the repo only (showroom, canon, component count; cite the file you read). | G2 |
| 7 | s7  | The explorer — what she knows. Re-cut of v7 s9. Figures: 4,820 nodes · 8,648 edges (current explorer, per the strand map; v7's 2,837/4,902 is STALE). Keep `.switch`. | G2 |
| 8 | s8  | The build — re-cut of v7 s7 holding card; gates-and-evals as the beat that checks her work. Keep `.switch`. | G2 |
| 9 | s9  | What she is made of — re-cut of v7 s8 (canon · gates · runbooks · host agent). | G2 |
| 10| s10 | The proof we own — v7 s5 before/after, kept, re-labelled as "after the build, what we measured". | G3 |
| 11| s11 | The claim + KPIs — v7 s4 and s6 folded into ONE slide if it fits, else keep both (then 14 slides; say so). | G3 |
| 12| s12 | The ask — v7 s10 re-cut for an INTERNAL room (no "your published 15%" second-person to a sponsor); RESEARCH named here, another group's, Dave alongside. Keep the `.draft` stamp: the ask is Dave's and not ruled. | G3 |
| 13| s13 | Close — v7 s11, count updated to 4,820 · 8,648. | G3 |

## Rules
1. `pagenum` text is `NN / 13` — write it; the conductor renumbers if the count moves.
2. Labels: drop "Plot point NN". Use short chapter labels ("The problem", "The turn", "The evidence · 1 of 3").
3. NO invented figures. Every number either comes from v7 (and is still true — check) or from a file you read
   at this seat, named in your report. When unsure, write the sentence without the number.
4. Keep `rv d1…d5` reveal classes on every revealed element; the script depends on them.
5. Keep ids `kgPrint`, `kgPrint2`, `gb`, `gbPrint` exactly where v7 has them (G1 only).
6. Writing: Dave's register — short, plain, landmarked, one idea per slide, no bullets on slides except
   the strip's `.chapters`. Sentences a person can say out loud.
7. Output: `notes/_lanes/289/deck/G<n>.html` — ONLY the `<section>` blocks (and the one optional scoped
   `<style>`), no html/head/body. Then the report:
   `notes/_subreports/2026-09-19-289-G<n>-deck-v8.md` — what you wrote, every fact and its source file,
   what you were unsure of, what you left for Dave. Under 60 lines.
8. Do not touch v7. Do not touch any other file. Do not commit.
