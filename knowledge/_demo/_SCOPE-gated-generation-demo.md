# Gated-generation demo — scope
*Strategy-chat owned. Documented 2026-06-20. Thin version built alongside this doc.*

## Purpose (one sentence)
Show colleagues and the boss a capability the bank doesn't have today: **generate a faithful screen AND prove it meets standards** — with the *verification* (the gates) as the visible hero, not the generation.

## Why this, why now
- Unblocked: needs neither Sutherland JSON nor the interview/questionnaire responses.
- Strategy-fit: demonstrates the moat (discovery→criteria→**enforcement**), not the commodity generator.
- Boss-legible: the rigor injected so far is invisible; this makes it visible in ~60 seconds.
- Figma Make is not in-house (agency only; bank procurement slow) — so "generate + verify, in-house, today" is a genuinely new capability, and useful evidence in any future procurement conversation.

## Audience
Non-expert colleagues + boss. They will not appreciate token fidelity or WCAG SCs in the abstract — they need to *see* a broken thing get caught.

## The one flow (scope IN)
1. Pick an **intent** (e.g. "payment confirmation screen") — scripted choices, not open NLU.
2. **Assemble** a screen from the *real* gated snippets (Header, Cards, Tabs, Button, etc.).
3. **Run gates** — show the 6 existing gates checking the output and passing.
4. **Naive toggle** — show an ungated/"vibes" version of the same screen (invented hex, missing ARIA, no reduced-motion) and the gates **failing** it, with the specific failures listed.
The contrast: same screen, one path proven correct, one path quietly broken.

## Scope OUT (hard boundaries — protects strategy + the days budget)
- No general/LLM generator — intent→layout is scripted/curated.
- No editor, no drag-drop, no Figma integration.
- No new gates, no re-tiering, no changes to canon snippets or `_validate_*.py` / `_build_all.py`.
- No Sutherland, no multi-screen journey (single screen only).
- The full multi-solution loop stays a *strategy* deliverable; this demo shows at most a gated/ungated pair, not the formal N-variant loop.

## Architecture
- Lives entirely in `knowledge/_demo/`. Nothing outside imports it.
- **Consumes canon read-only:** reads `snippets/*.reference.html` + their embedded `#token-manifest`.
- **Reuses the real gates** as source of truth. The thin HTML version runs a *subset* of checks client-side for live visual effect (contrast ratio, required-ARIA presence, reduced-motion presence) — **clearly labelled as mirroring the real Python gates**, which remain authoritative. Production version should shell out to the real `_validate_*.py`, not reimplement them.
- Exploration tier: **never gated as canon** (consistent with the `_fitness-test/` two-tier rule).

## Repo / process decision
- **No branch.** Both chats share one working tree on `master`; branching would switch the build chat's files mid-flight. Isolate by **directory** (`_demo/`) instead.
- Build stays green; commits touch only `_demo/`; flag if anything needs to reach into canon (it shouldn't).

## Success criteria
A colleague/boss watches it and, unprompted, gets: "it built the screen *and* caught N real problems the hand-rolled version shipped." Specifically:
- The gated screen renders faithfully from real token values.
- The naive version visibly fails ≥3 distinct gates with named reasons.
- No build breakage in the canon pipeline.

## Prune / promote (per Dave's v1 instinct)
Self-contained by design. After v1, decide: **promote** (wire to real Python gates, fold into the harness as the "render+verify" step) or **delete**. Either is a one-folder operation. Add to the v1 prune pass.
