# Brief — deck v9 — the recut on Dave's seven beats, with the three drawings — #289 — 2026-09-20

One lane. Source: `notes/_DEMO-SLIDES-apollo-2026-09-19-v8.html` (11 slides; read lines 1–~700 for CSS + slides, and the
script from there: fly-through §1, gearbox §3 with its IntersectionObserver `io3` on `#s3` and its print `snap()` to
`#gbPrint`). Output: `notes/_DEMO-SLIDES-apollo-2026-09-20-v9.html`. Do not touch v8. No commit.

Dave's words are the copy. They are in `notes/_lanes/289/DAVE-RULINGS-2026-09-20.md` (beats 1–7, and the premise). The
proposal that orders them is `notes/_PROPOSAL-apollo-story-2026-09-20-v2.html` (its "Seven beats · his words" section is the
tidied text — use THAT wording, spelling tidied, nothing reworded). Slides speak; keep each to what a person says aloud.

## Running order — 12 slides

| # | id | slide | drawing | notes |
|---|----|-------|---------|-------|
| 1 | s1 | Title | fly-through (as is) | VERBATIM from v8, byte for byte except the pagenum |
| 2 | s2 | The strip | kgPrint2 (as is) | chapters: 1 Why now · 2 The line · 3 The robots · 4 The inventory · 5 The assembly engineer · 6 The inspector · 7 The build · 8 The ask. Head: "A custom shop that builds at the speed of a car plant." |
| 3 | s3 | Why now — the premise | — | NEW, dark. Label "Why now". His words tidied: "Dev got fast. Build fast, test with real, shippable code. Design became the bottleneck. So we asked: how do we speed up design?" Foot: "That question was the first experiment." |
| 4 | s4 | The line | GEARBOX (move v8's `#gb` canvas + `#gbPrint` here; re-point `io3`, the print snap and the CSS `#s3 …` rules to `#s4`) | Label "The line". h2 "An assembly line is only as fast as its parts bin, the skill of the assembly engineer, and the rigour of QC." Lead: "Ours: a parts bin that is too small, engineers with dramatically different skill levels, and QC that is rigorous but slow." Body: "No one has the full picture. Missing parts are machined all the time, by engineers without the skills to do so. The builds are unreliable and they go back down the line to be repaired." |
| 5 | s5 | The robots | — | NEW, grey. Label "The robots". h2 "We introduced robots into the plant. **The results were underwhelming.**" Lead: "Where the inventory was empty the robots tried to machine the parts — and they simply don't have the skills or knowledge for this." Body: "We watched our designers do exactly what the machine did. The problem was always there. Trying to automate it is what made it obvious." Foot: "June–July 2026: one brief, two arms — governed and ungoverned — both on Opus." |
| 6 | s6 | The inventory | BOOKS (new canvas `#bk`, from `notes/_lanes/289/illustration/books.html`) | Label "The inventory · what she builds with". h2 "**36 → 137.** Now there is no need to machine parts." Lead: "First we focused on the inventory: 125 components, 12 templates, 8 foundations — 101 new — each one in code, built to our design and accessibility standards." `.switch` "Switch to the library". Foot: "Source: showroom/index.json, read 2026-09-19. Growing." |
| 7 | s7 | The assembly engineer | BRAIN (new canvas `#br`, from `notes/_lanes/289/illustration/brain.html`) | Label "The assembly engineer · what she knows". h2 "A custom shop that builds **at the speed of a car plant.**" Lead: "Each product is custom designed and built — so we needed the knowledge of a designer and an assembly engineer embedded in the system too." Body: "Standards, accessibility, rulings, governance, usage and theory — all in one graph, retrieved when needed, and with each build comes a record of account." `.switch` "Switch to the knowledge-graph explorer". Foot: "4,820 nodes · 8,648 edges · explorer builder 1.27, 2026-09-19." |
| 8 | s8 | The inspector | — | dark. Label "The inspector · QC". h2 "QC is always **the final check.**" Lead: "Quality is built into the parts and the assembly is powered by a vast knowledge base — and the inspector still checks every build." Body: "Corrections are executed by the inspector, not sent back down the line." |
| 9 | s9 | The build | — | dark, re-cut of v8 s8. Label "The build". h2 "**Live build.**" Lead: "One cold, repeatable testing prompt. The build, the inspection and the final product roll off the line." `.switch` "Switch to the editor". Foot: "Live and unedited, with the recording as the fallback." |
| 10 | s10 | What she is made of | — | grey, v8 s9 re-labelled with his names: The inventory · The assembly engineer · The inspector (3 columns; keep the `#s9 .grid4{3 cols}` rule, re-pointed). |
| 11 | s11 | The ask | — | v8 s10 with the `.draft` stamp; ask text: "Help and support to develop it further." One line under: "The ask is Dave's, with his colleagues — open." Research paragraph kept. |
| 12 | s12 | Close | — | v8 s11 verbatim (count 4,820 · 8,648); re-point the `#s11 .close-line/.count` rules to `#s12`. |

## The two new canvases
- Each becomes a `<div class="draw rv d2"><canvas id="bk"></canvas><img id="bkPrint" alt=""></div>` inside the slide's
  `.inner`, laid out like s3's gearbox is in v8 (type left, drawing right; reuse the `#s3 .inner/.type/.draw` CSS by
  generalising the selectors to `#s4, #s6, #s7`).
- Port the drawing code from the two illustration pages into the deck's script as two more IIFEs, in the gearbox's
  pattern: draw only while the slide is in view (IntersectionObserver), same mouse orbit, and a `snap()` that bakes the
  resting frame to the `<img>` for print (copy the gearbox's snap/print approach; the print CSS hides the canvas and
  shows the img). Drop each illustration page's caption/scale-bar text. Keep their resting views.
- The three drawings must share the card treatment (white card, same border/inset as the gearbox's `.draw`).

## Rules
1. No invented figures. Every number above is sourced (36 is Dave's word for the Figma count; 125/12/8/137 from
   showroom/index.json; 4,820/8,648 from the strand map §s4; 101 = 137−36).
2. Keep `rv d1…d5` on revealed elements. `pagenum` = `NN / 12`.
3. Render check at the end: playwright (`export LD_LIBRARY_PATH=$HOME/.local/lib`), 1440×810, every slide screenshot to
   `notes/_lanes/289/deck/render-v9/sNN.png`, zero page errors, zero overflow, and the three canvases visibly drawn
   (not blank) — LOOK at s4, s6, s7. Also a print-mode screenshot of s6 and s7 proving the baked images appear.
4. Report: `notes/_subreports/2026-09-20-289-D1-deck-v9.md` (<60 lines): what moved, what is new, what you were unsure
   of. Reply with a 10-line summary.
