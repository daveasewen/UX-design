# Good morning, Dave ☕

*Session briefing — written end of 2026-07-02, evening session ("Rulings day — desk
decisions before the meter"). Supersedes the day-session briefing; carried items below.*

## The session in one line

The whole desk got cleared in one sitting — five carried rulings closed (one dissolved on
receipts), the rag roundel policy ruled + enacted + visually passed, the dual-live palette
policy enacted, and Input-fields took three review fixes — 8 commits, every gate green,
and the only thing left undone is the push itself.

## What changed

1. **All-caps ENACTED, gate promoted.** Canon-wide sweep (14 snippets + gallery chrome,
   caps tracking removed with it), advisory signals 18 → 0, check moved advisory →
   blocking (snippet gate check 4, acronym exemption, bite-tested ×2 — suite now 16/16).
2. **Univers Next DISSOLVED.** type26-001's premise was wrong — the store already carries
   "Univers Next for HSBC" (since the Figma re-base) and all 45 snippet stacks match.
   Resolved with receipts; only residual is a Sutherland fixture spot-check at next touch.
3. **Text-on-gradient PARKED** to the finessing pass, docketed with mot-007 (the "too
   expressive" family). Interim discipline: no gradient-hero generation; gradient surfaces
   are text-free until ruled.
4. **RAG ROUNDEL POLICY ruled + enacted + PASSED review.** Roundel ≥3:1 · internal mark
   ≥4.5:1 · dark = white shape + black mark (supersedes the 06-24 interim). Amber roundel
   EXEMPT in light (convention; its #333 mark carries at 7.47). Fixes landed: Notifications
   success mark → white, inline amber mark → #333, Input-fields rag symbols de-hardcoded,
   Confirmation dark glyph → white via driftAllow. New advisory `_ICON-CONTRAST-DELTA.md`
   (build step 12/18) sizes everything: 0 fails on active treatments.
5. **Dual-live palettes ENACTED.** The 50 supporting primitives moved from the holding pen
   into colour.json (`color/supporting/*`, receipts kept) — preferred for new work; legacy
   `data-vis/*` annotated old-projects-only. Series assignment untouched — still V7.
6. **Input-fields review fixes (your eyes, live HTML):** tail icons now real buttons
   ("icons in an input are usually clickable"), dark error border full red (white border
   no longer overlays the red bar), text true-centred at rest (10/10; off-centre while
   active is accepted — the text never moves). Component flagged **supercharge** candidate.
7. **"Supercharge" recorded** = your codename for the brand-uplift component rework.
   Rule applied: canon stays valid, but no over-polishing what the uplift will replace.

## On your desk (fastest first)

- **Push.** 22 commits local-only — `git push origin master` (the sandbox has no GitHub
  creds; palette provenance you already ruled keep).
- **Carried:** V6 proposals · V7 series pick (palette primitives are now live, so this is
  the natural next colour decision) · colleague chase (calibration = #1 unlock) ·
  ADR-0005 wider provenance ruling · icon-016/017 size tensions.
- **Small, whenever:** formally promote the 4.5 icon threshold to blocking (evidence: cost
  0) — deferred to supercharge alongside mark tokenisation, but it's a 5-minute yes if you
  want it sooner.

## The register

`knowledge/guidelines/_RECONCILIATION.md` — 11 open items (was 12; type26-001 dissolved).
icon-015's tail narrowed to gate-promotion + mark-tokenisation, deferred to supercharge.

## Queue next (when ingestion resumes)

Web foundations · app foundations · accessibility trio (hub + neurodiversity +
communication) · typefaces + creative-headlines subpages · logos/photography/hexagons
2026 · tone of voice (register shaping).

## The window (Fable metered from the 7th)

Rulings are cheap when the evidence is pre-computed — tonight proved the pattern (advisory
check first, decide on numbers). Judgment-dense remainder: calibration (if materials land),
G2 compiler spec, V7 series assignment, the finessing pass (mot-007 + type26-015 together).
One papercut for the robustness list: sandbox Chromium wouldn't launch (missing system
libs, no root) — the render path needs the tool to own it.
