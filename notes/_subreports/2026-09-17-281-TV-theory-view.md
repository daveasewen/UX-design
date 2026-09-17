# `#281`-`TV` — the Theory view: the 14 citation lines are drawn, and the triad is named

session: `#281` · 2026-09-17
window: lane TV — the theory view
sub index: `TV`
brief: `notes/_lanes/281/theory-view/BRIEF.md`
tokens: `~180,000` — the difference between the remaining-budget counter reported to this lane at
its first tool call and at its last. `CLAIMED`, not `message.usage`: the seat does not hand
`message.usage` to a lane, so this is the closest honest reading available, and it is a budget
delta, which includes re-read context, not only new tokens.

## VERDICT

DONE. Two rulings inscribed and both enacted in one version. **s281-D4**: the 14 authored `obeys`
lines from a component meta to a `ux:` principle — held and drawn by nothing since 1.21 — are drawn
in the THIRD VIEW under their own chip, `cited by a design`, beside the UX principles and their
polarities. They are explanation, not obligation, so **Design governance keeps its three
provenances and no fourth sub-chip was added**; the `held` flag clears on all 14 and becomes
`cited`; the designer's own `$why` sentence now rides the edge and reads in INSPECT's ↔ door; and
**force by grade is not ruled** — these 14 are the hand-authored seed, and that question waits on
lane RO's rule→principle lines. **s281-D5**: the triad is **SYSTEM · GOVERNANCE · THEORY**, three
one-word nouns with a verb line under each; the Constitution keeps its name and is still not a
view; labels only — no fam key, node id or edge type moves, and the view ids `system`/`design`/
`explain` are untouched. Explorer **1.24**. The orphan census's set 08 `obeys-ux` goes **4 → 0** at
every-chip-on and the four principles gain degree 8 / 4 / 8 / 6.

The default canvas md5 DID move, and the brief asked which pixel. It was not the label rename. Two
causes, both measured and separated below: 75 pixels from the ghost stroke of the 14 undrawn lines
changing colour, and the rest from this lane's own two rulings entering the Constitution's column.

COUNTS: findings `5` · ruling-shaped `2` · UNPROVEN `3`

## What was done

1. **`s281-D4` and `s281-D5` inscribed** — `knowledge/_rulings.json`, textual span insert,
   `git diff --numstat` = `47  0`. 610 rulings → 612.
2. **The builder.** `knowledge/_build_kg_explorer.py`:
   - `hold_obeys_ux()` → `cite_obeys_ux()`. Same predicate, same 14 edges, different verdict: it
     pops `held`/`heldWhy` and writes `cited:true` + `citedWhy`. The HELD machinery is left
     standing and unused — it is the right shape for the next unanswered question, and `held` is
     still reported into the page's `extra` so the legend's held row is a *measured* absence.
   - The meta reader takes **`$why`**. It took `$note` only, so 168 authored sentences reached
     storage and stopped there. `$why` is carried in the edge's own `why` field, not folded into
     `note`: a note annotates a link, a `$why` is the reason for it. Measured scope — `$why` occurs
     on `obeys` and on nothing else, 168 times, and no entry carries both a `$why` and a `$note`,
     so nothing already read is displaced.
   - `BAND_NAME` renamed. One dict feeds all four furniture sets, so the rename lands once.
   - `VERSION` 1.24 with a paragraph in the house style.
3. **The template.** `knowledge/_kg_explorer.template.html`: the `uxcited` chip and its three
   predicates, the `VIEWS` labels and verb lines, the legend prose, and INSPECT's two new rows.
   Every occurrence of the old labels is listed in Finding 5.
4. **Proof** — the census re-run, two coordinate diffs, the md5 forensics, eight shots and a driven
   INSPECT pass, all below. Page errors `[]` everywhere.

Files changed: `knowledge/_rulings.json` (span insert, `47  0`) · `knowledge/_build_kg_explorer.py`
· `knowledge/_kg_explorer.template.html` · `notes/_KG-EXPLORER.html` (rebuilt) ·
`notes/_lanes/281/theory-view/*` · this report.

## Findings

1. **The 14 lines could not simply be given a family, and that is the shape of the ruling.** The
   page's draw gate is `EON`, which reads the edge's family and asks whether *that* chip is on.
   `obeys`'s family is `guidelinerules` — the HSBC `rule:` chip — and it is the right filing: 154 of
   the 168 `obeys` lines are a component obeying an HSBC rule. If the 14 had been gated the same
   way, reading a designer's *reason* would have cost you turning on the *obligation* chip, which is
   the opposite of what s281-D4 says. So `EON` asks a `cited` line for `famOn.uxcited` **instead
   of** its storage family:
   `const EON=e=>(UXC(e)?famOn.uxcited:famOn[EFAM(e)])&&(!DR(e)||famOn.designrulings)&&!e.held;`
   The storage family is untouched and INSPECT still names it; only the chip that gates the line
   and the colour it is stroked in follow the view it is drawn in (`EDRAWF`). Both ends must still
   be on the stage, as for every edge — so the UX-principles chip puts the dots there and this chip
   puts the lines between them. That is exactly the `designrulings` shape, one view along.
2. **A 14-line disagreement between the header and the canvas, inherited from 1.21, is closed.**
   `recount()` counted an edge by `famOK(e)` — the edge's own `fam` — and the 14 carry none, so
   they were counted in the header whenever both ends were visible while the canvas (which read
   `held`) drew none of them. At the page defaults that was 1,642 relations for 1,384 drawn lines,
   14 of which no setting could produce. `UXCON(e)` now gates the count the same way `EON` gates
   the picture. **The header at the page defaults reads 1,642 → 1,628 and that is the fix, not a
   loss**: the 14 come back the moment their chip is on. The four `ux:` dots they land on are BASE
   nodes (minted by the meta reader before the UX family pass), which is why they were counted at
   the defaults at all, and why they are among the 111 dark dots there.
3. **`chipF` had to stop counting them, or the HSBC chip would claim 168 and draw 154.** A cited
   line is counted in its own chip and nowhere else — the same rule 1.21 applied to a held line.
   `ETYPES()` became a Set, because `obeys` is now one storage type drawn under two chips and would
   otherwise be named twice when both are on.
4. **The default canvas md5 moved, and neither cause is the label rename.**
   `notes/_lanes/281/theory-view/_whymd5.py` serves the two pages side by side, hashes the DRAW SET
   (every node and edge the page would draw, sorted), reads `fit()`'s own transform, counts the
   GHOST layer and diffs the two canvases' `ImageData` pixel by pixel.
   - **Cause (1), the code alone** — HEAD's 1.23 against the pre-inscribe 1.24 build
     (`whymd5-code-only.json`): draw set identical, view transform identical to six decimals
     (`k=0.278656 x=-652.35 y=6.64`), painted node set identical, **75 pixels of 653,976 differ**,
     all inside `x 271…312 · y 393…464`. The canvas does not skip an edge whose chip is off — it
     paints it at alpha 0.04, the "faint halo round the hub" of 1.16 — and 14 of those 189 ghosts
     changed stroke from `guidelinerules` green to `uxprinciples` plum, because `EDRAWF` reads the
     view a line is drawn in. The legend also lost 33px of height (`606 → 573`: one shorter label,
     one extra chip, the held row gone) and `fit()` settled on **the same transform anyway**, so
     the re-fit everyone would guess at is measured and ruled out.
   - **Cause (2), and the larger** — the pre-inscribe build against the shipped one
     (`whymd5-rulings-only.json`): **75,638 pixels**, across the whole canvas. This lane inscribed
     two rulings, so the Constitution gained 17 nodes (2 `ruling:` + 15 `evidence:`) and
     `place_extra` re-solved that family's own column. Those nodes are not *drawn* at the defaults —
     their chip is off — but `dot()` paints an off-chip node at alpha 0.05, so the faint
     Constitution haze moves with them. **Both md5s, published:** default canvas
     `44e9586896537f9fd13f75735bf557a5` (1.23) → `d25c355e274d7cb506aaa310fa5bbe8e` (1.24, code
     only) → `b33ff55a7a51…` (1.24 as shipped). The drawn picture is identical in all three: 1,050
     nodes, 1,384 lines, the same ids.
5. **Every `Explanation` / `Design governance` occurrence, and what was done with it.** Grepped
   across the template and the builder at HEAD:

   | file · line (at HEAD) | occurrence | what was done |
   |---|---|---|
   | `_kg_explorer.template.html:97` | CSS comment, "DESIGN GOVERNANCE's three provenance sub-chips" | reworded to GOVERNANCE's, with a note that the box was renamed and the class names are not |
   | `…:331` | comment, "the Explanation view's own" | reworded to "the THEORY view's own", with the view id `explain` named as untouched |
   | `…:358` | `VIEWS` — `name:'Design governance'` | → `'Governance'`; `say` → "…the agent obeys **here**" |
   | `…:359` | `VIEWS` — `name:'Explanation'` | → `'Theory'`; `say` → "why — the agent consults **here**"; gains `cited:true` |
   | `…:446` | comment, "counted … under the Explanation chip" | → "under the Theory chip" |
   | `…:811` | legend prose, "One graph, three views" — both labels | paragraph rewritten: the triad, the new chip, s281-D4's terms, and the force-by-grade limit said in words |
   | `…:812` | legend prose, "a ruling enters Design governance only by…" | → "enters Governance only by…" |
   | `_build_kg_explorer.py:565` | `BAND_NAME` — both labels | → `'Theory'` / `'Governance'`; one dict, four furniture sets |
   | `_build_kg_explorer.py:813` | `HELD_WHY`, "s277-D8 fixed Design governance at three provenances…" | HELD_WHY rewritten generic (it no longer describes this branch); the clause moves into `CITED_WHY`, saying Governance **stays** at three |
   | `_build_kg_explorer.py:29` | the `VERSION` history, 1.15–1.22 | **left alone.** A shipped version's own note is a record of what that version said, not a label the page renders |

   In the built page the two strings survive **only as data**: the text of `s277-D8` and of this
   lane's own two rulings (which quote Dave verbatim — "The Explanation view — a 'cited by a
   design' chip beside the polarities"), and a `refutation_probe` sentence on several Gestalt
   principles that uses the ordinary English word. No UI label says either. A ruling's own words are
   not rewritten by a later ruling.

## RULING-SHAPED QUESTIONS

1. **Does force follow grade?** Deliberately NOT ruled here, on the chat's own terms: the 14 are
   the hand-authored seed of applicability, and the question — whether a high-graded principle binds
   a design that has not cited it — belongs after lane RO's `restsOn` lines land, because that is
   when a rule's reason becomes walkable. Nothing in 1.24 derives a scope or promotes a principle.
   The shape it would take: a second, derived sub-chip beside this one, dashed, because it would be
   *inferred* and not authored. **Recommend leaving it until `restsOn` has an export.**
2. **Should the ghost layer follow the drawn family or the storage family?** 1.24 answers "the
   drawn family" by implication (Finding 4, cause 1) and it is 75 pixels wide. The argument for it:
   a ghost's colour is the reader's only clue which chip would turn the line on, and that chip is
   now the Theory one. The argument against: a ghost is not drawn, so its colour arguably belongs
   to the record rather than the picture, and keeping it would have left the default canvas
   byte-identical. **Recommend as shipped**, but it is one line (`EDRAWF` → `EFAM` in the ghost
   branch) if Dave wants the default canvas frozen instead.

## UNPROVEN / CLAIMED (ADR-0016)

- **UNPROVEN: the dark colour scheme.** Every shot is `color_scheme='light'`, as the brief asked.
  The new chip takes `--f-uxprinciples`, which has a dark-mode value (`#E68ABF`) alongside every
  other family token, so it is expected to follow; not photographed. Price: the same pass with
  `color_scheme='dark'`, ~3 min.
- **UNPROVEN: the 3D cells and the shells layout.** `BAND_NAME` feeds plates, rings and shells as
  well as bands, and the builder PRINTS all four renamed (`Theory … Governance … System … The
  Constitution`, in the build log and in `shots-after.json`'s `plateNames`/`ringNames`/
  `shellNames`), but only strata-2D was photographed. Price: four more cells, ~4 min.
- **UNPROVEN: the chip's behaviour under a dig and a shortest path.** `applyFocus`'s `nb` and
  `shortestPath` both gate on `EON`, so they follow by construction, and the aside's relation
  groups were checked in the driven pass — but no dig was driven onto one of the four principles.
  Price: one driven pass, ~2 min.
- **CLAIMED:** the token figure in the header — see the note there.
- **DECLARED, not a defect:** `Object.keys(localStorage)` is `['kg-theme']` in every shot, before
  and after; `applyTheme()` has written it since v1.16.
- **DECLARED:** the header's relations count at the page defaults moves 1,642 → 1,628. That is
  Finding 2 and it is the fix, not a regression.
- **DECLARED:** the baked coordinates of the `governance` family move — 2,189 nodes, every key —
  and no other family's move at all (`base`, `uxprinciples`, `guidelines`, `guidelinerules`,
  `assets` are byte-identical). The cause is this lane's own two rulings entering the record, not
  the code: the 1.23 → pre-inscribe-1.24 diff is byte-identical on **every** family and every key,
  with the node ids and the edge multiset identical. Both diffs are filed.

## Evidence

`notes/_lanes/281/theory-view/` —
- `inscribe_s281_D4_D5.py` — the span inserter; idempotent, refuses on a changed file tail, asserts
  the result parses and that no ruling id is duplicated. `47  0`, 612 rulings.
- `_recensus.py` · `facts-before.json` · `facts-after.json` — lane OC's set-08 predicate re-run
  against one page, with the chip vocabulary parsed out of the template rather than retyped, and
  1.24's `cited` gate modelled. The "before" row is taken with HEAD's page **and** HEAD's template.

  | setting | drawn before | drawn after | dark before | dark after | set 08 `obeys-ux` |
  |---|---|---|---|---|---|
  | page defaults | 1,384 | 1,384 | 111 | 111 | 4 → 4 (chip off by default) |
  | every chip on | 4,906 | **4,920** | 8 | 8 | **4 → 0**, 14 lines drawn |
  | + Constitution | 8,271 | **8,306** | 8 | 8 | **4 → 0**, 14 lines drawn |

  Flags on the page: `held 14 → 0` · `cited 0 → 14` · `why 0 → 168`. The four principles are
  `ux:pr-fitts`, `ux:pr-graphical-perception`, `ux:pr-hick`, `ux:pr-speed-accuracy`, and their
  degree with the chip on is 8 / 4 / 8 / 6 (`shots-after.json`, `citedEndDegree`).
- `coords-code-only.json` — 1.23 → 1.24 **before** the inscription: node ids identical, edge
  multiset identical, **every one of the fourteen baked coordinate keys byte-identical for every
  family**. Nothing this lane's code does enters the layout.
- `coords-rulings.json` — the same diff across the inscription: only `governance` moves, 2,189
  nodes, and it must — `place_extra` solves each family's column on its own.
- `_whymd5.py` · `whymd5-code-only.json` · `whymd5-rulings-only.json` · `whymd5.json` — Finding 4,
  the draw set / transform / ghost / pixel forensics. The before page is copied into the served root
  for the run and removed in a `finally`.
- `shots.py` · `shots/shots-after.json` · `shots/shots-before.json` · `shots/*.png` — eight 1280
  light shots of the after page (six cells + a legend clip + the driven INSPECT), plus the same
  cells against HEAD's page, served by `knowledge/_serve_explorer.py` on 127.0.0.1. Never driven
  except the INSPECT pass and the phone sheet's one click to open it. Page errors `[]` in all of
  them. The cells: `default` (force-2D, the shipped defaults) · `citedon` (the new chip on) ·
  `uxonly` (the family chip alone, so the chip's own contribution is isolated) · `strata` (the three
  renamed bands with the 14 lines crossing Theory → System) · `allchips` · `phone` (390×844, the
  bottom sheet open) · the legend clip · the edge's INSPECT door.
  View headings scraped off the rendered page: `SYSTEM · GOVERNANCE · THEORY · THE CONSTITUTION`,
  with `what exists — the agent chooses here` / `what a design must or should do — the agent obeys
  here` / `why — the agent consults here`. Band names: `Theory · Governance · System · The
  Constitution`, and the same four on the plates, the rings and the shells.
  The driven INSPECT row, scraped not asserted: family `guidelinerules`; **cited by a design** —
  "drawn in the THEORY view, under its own chip cited by a design"; **why — the designer's own
  words** — "ctkb-014's ≥44×44 over the entire container, and ctkb-005's fixed side padding, set
  target size directly."

REPLAY-THESE: `notes/_lanes/281/theory-view/facts-before.json` + `facts-after.json` (~2k tk) ·
`notes/_lanes/281/theory-view/whymd5-code-only.json` (~1k tk) ·
`notes/_lanes/281/theory-view/shots/shots-after.json` (~3k tk)
