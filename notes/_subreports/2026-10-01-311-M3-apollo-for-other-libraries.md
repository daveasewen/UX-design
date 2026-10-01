# #311 lane M3 — Apollo for other libraries: the proposal page

Lane M3 of session #311, Fable, Thu 2026-10-01. Inputs: lane M1's desk research (`notes/_lanes/311/M/M1-FINDINGS.md`, 38 sources) and lane M2's read-only measurement of the repo (`notes/_lanes/311/M/M2-COMPILER-DEPENDENCIES.md`). Both copied into the lane folder with this report.

## What was built

`notes/_PROPOSAL-311-apollo-for-other-libraries-2026-10-01-v1.html` — the proposal page, dave-voice, eight sections: the answer on one screen; what Apollo depends on today (M2's numbers, with a diagram of the build loop); what the field does (M1, sourced); the options for S1 (placements A, B, C) and for S2 (manifest, theme-only, replace); the recommended architecture (diagram, wide and tall); the phased plan with gates and rough lane sizes; seven calls with a decisions overlay; sources. Shell copied from the #311 B review page (styles, back link, Copy-as-text bar) with a new localStorage key `proposal-311-apollo-for-other-libraries-v1`; diagram conventions from the #304 Apollo-MCP proposal.

Verified at the seat with `notes/_lanes/311/M/verify_page.py` (ensure_env OK, RENDER_SHELL): side scroll 0 at 1440 and 390; eight calls; the wide diagrams scroll inside their own box at 390 and the architecture diagram swaps to a stacked tall variant; Copy as text returns every call with its choice, the recommendation marker and its comment, plus the page note; count reads "8 of 8 answered" after the probe. Screenshots in `notes/_lanes/311/M/shots/`. Three rounds of text-overflow fixes in the SVGs were made by eye from the renders.

## The recommendation, in short

Dave's two scenarios are separated on the page. S1 (Apollo's own components into React, Angular or plain HTML): placement A, at source. The meta becomes the declared spec and gains four fields (anatomy, states with transitions and keys, emits, bindings); per-component CSS and behaviour modules move out of the snippets; tokens go to DTCG 2025.10 with the Resolver Module; the compiler becomes emitters (E1 HTML+CSS re-fed, E2 Lit custom elements in light DOM, E3 generated React and Angular wrappers, E4 token exports, E5 the A2UI catalogue already specced for Launchpad route B). The snippets stay, as fixtures the emitters must match byte for byte, GOV.UK fixtures.json style. S2 (a client's existing library): an adapter manifest per library, Code Connect in shape, mapping roles and metas to their components, props and slots with typed holes, their tokens onto Apollo's semantic tokens, with a required unmapped list and a gate that refuses unbound parts on a composed screen.

Dave's "halfway there" is answered no: the compiler's input today is the snippets, so switching them out switches out 95% of canon.css, all markup and ~5,800 lines of behaviour; the metas hold the governing half (props, variants, roles, when, aria as prose), not the rendering half (anatomy 0, transitions 0, emitted events 0, 239 of 1,013 token entries bindable). Swapping in another library's HTML would make canon.css that library's theme (placement C).

Where he is challenged: the snippets are the acceptance test and what he rules on by eye, so they leave the pipeline only as input, never as oracle; the reversal undoes ADR-0013 ruling 4 and the docstring in gen_canon_components.py, so it is a ruling not a tidy-up; the tokens are the one part that is as easy as he hoped, and for a reason unrelated to the compiler.

## The calls on the page

1. The snippets' job (recommendation: fixture, generated from the spec).
2. Where the spec lives (in the meta, four new fields).
3. The second runtime (Lit custom elements, wrappers generated).
4. Light DOM or Shadow DOM (light DOM, styled by canon.css).
5. How Apollo meets a client's library, S2 (adapter manifest per library; Apollo governs, theirs renders).
6. Tokens to DTCG (now, one generator, extras under $extensions).
7. Order and start (phases 0, 1 and the S2 schema now; phase 2 after call 1; phases 3 and 4 later).

## Not done, by scope

No ruling inscribed; nothing in `knowledge/` edited; no push; no Project memory. The page is a proposal and waits for Dave's words on the seven calls.
