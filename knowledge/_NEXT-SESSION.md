# Start here next session — open threads + framing

## ✅ UPDATE 2026-06-20 (autonomous day — coverage now 32/32, a11y gated)
Three autonomous runs landed, all gate-verified, build green (now **6 gates**: dark-surface, snippet,
**a11y**, **coverage**, integrity, schema; **32/32 snippets + metas**):
1. **`text/secondary` token** added (#545454 / #9B9B9B, review-tagged) + adopted in List items, Cards; focus
   ring token-tracked in 5 more snippets. Literal sweep otherwise clean.
2. **WCAG pass** — `_A11Y-AUDIT.md`: added `prefers-reduced-motion` to 28 snippets, 24px hit-area expanders
   on Tags/Tooltip (2.5.8), and a **new enforcement gate** `_validate_a11y.py` (reduced-motion = hard fail;
   bite-tested). 1.4.1 Use-of-Color audited → all PASS; rule written into `digital-accessibility-standards.md`.
3. **Table built** — was the one missing component; `Table.reference.html` semantic/scope/caption/tokens, gated.
   Coverage is now **32/32 real components** (EXAMPLE-button is just a template).

**Everything needing your eyes is in `_VISUAL-CHECK-QUEUE.md`** (V1 text/secondary values, V2 four baseline
organisms, V3 screen-reader/keyboard pass, V4 zoom/reflow, V5 Table sort+reflow). Consolidated open items
in `_FINDINGS-INDEX.md §6`. Nothing is mid-flight.



Captured end of 2026-06-19 (a long, productive day). **Priority is deliberately NOT set** — decide it together at the start of the next session. The work has been a mix of *convergent* build and *divergent* exploration; the first job tomorrow is to name what we do next and how we split those.

## ⭐ Tomorrow's first task — clarify direction
Today blended two modes that want different treatment:
- **Convergent** (codify + verify): 11 gated component snippets, the 4 build gates, the dark-token reconciliation, `text/on-inverse`.
- **Divergent** (explore, don't codify yet): the motion tiers, chip/cross tactile, the icon weight + fake-weight investigation.
Decide: what's the next chunk, and how much of the session is convergent vs divergent? Dave drives this.

## Principles to keep (from the "Open Skills" reflection — this is the thing that must stick)
1. **Verification = enforcement, not a nudge.** Our gates *withhold "done"* by exiting non-zero — that's strictly stronger than a procedure that merely *asks* the agent to verify. Keep new definitions-of-done executable, not prose.
2. **Keep the convergent/divergent line bright.** Gate canon; **never gate exploration**. Codifying divergent work too early kills the surprise that produces the good ideas (the fake-weight trick only existed because motion was still loose).
3. **Procedural debt is real and we're accruing it.** We have the *artifacts* but not the *method written down*. Decisions are scattered across snippets, four `_*.md` docs, meta `$finding`/`$darkDecision` notes, memory, and chat history that will compost.

## Action items (priority TBD tomorrow)
- **Write the method down as runbooks** — "build a gated component" and "reconcile a dark token group". These currently live only in-session; a cold-start agent couldn't reproduce them from the repo. *(Highest-leverage per the reflection.)*
- **Consolidation / garbage-collection pass** — fold scattered findings + chat decisions into the metas; cross-link/prune the `_*.md` docs; **do not add more docs**. Curation is now part of the job.
- **Motion review** — walk `_PROMOTION-QUEUE.md`: tokenise approved treatments (Refined button, dropdown V2 accent, tactile cross), decide what gets promoted to canon.
- **Standing canon backlog** — remaining gated components; focus-adoption sweep across the other metas; fitness fixes #6 (overflow/guideline map), #7 (tabs hover/pressed tokens), #8 (angular rule); Figma dark write-back (needs Dave's go-ahead); Sutherland migration when its JSON lands (snippets become its acceptance fixtures).

## Upstream / discovery phase — the step BEFORE building (new, Dave, end of day)
There's a whole phase before component work that we haven't built: **PRD → research → success/failure criteria & states.** This is the front-end of the pipeline.
- The **success/failure criteria + states are the definition-of-done, defined up front** — they become the enforcement targets the build gates check against downstream. Direct line to principle #1 (verification = enforcement): define the proof first, then the gates hold the work to it.
- Maps cleanly onto convergent/divergent: **brainstorm** (divergent discovery/ideation) → **grill-me** (convergent pressure-test / interrogate the idea) → **PRD + criteria** (the codified contract).
- **Seed from the `superpowers` repo skills:** `brainstorm` (divergent) and `grill-me` (convergent critique) as starting points — adapt as seeds, don't adopt wholesale.
- **Explore Code Connect** (Figma ↔ code component mapping) — revisit. Earlier parked to the Sutherland phase, but worth scoping now: it's the link between the design source, our gated snippets, and future Sutherland components.

## Pointers (don't duplicate — these hold the detail)
`_PROMOTION-QUEUE.md` (canon/exploration model + motion queue) · `_MOTION-THEMES.md` (the 6-theme family) · `_BRAND-REFRESH-DIRECTION.md` (future, fenced; icon-weight routes) · `_FITNESS-TEST-tabs.md` (the original gap report) · `README.md` (build + gates).
