# Good morning, Dave ☕

*Session briefing — written end of 2026-07-05, session "§9 worked spread — SME Payments register
run, Opus re-test, restyle + audit." Read this, then `_LIVE-STATE.md` (OPEN → "What does the §9
spread actually reveal?"), then decide if the NEXT session is the dedicated §9 session or something
else.*

## The session in one line

Ran the §9 spread all the way through (gravity fix → pure-inference diagnostic → hand-restyle onto
HSBC canon → real bug/a11y fixes, each one caught by you asking a pointed question, not by me
self-checking) — and your verdict at the end wasn't "converged," it was "confused." That confusion
is real and load-bearing: it's now the top OPEN item, and you've asked for a session dedicated
just to working out what it means, separate from continuing to iterate the prompt.

## What landed this session

- **Gravity-fix re-run + pure-inference diagnostic** (both already summarised in prior sessions):
  sourced 5 external references (Linear/Stripe/Mercury/Ramp/award-fintech), re-ran expressive-v2 on
  both models, then ran a zero-curb diagnostic (with/without those references) to find the ceiling.
- **You picked `without-influences.html`** (the diagnostic piece with the strongest organising
  idea — "today's arc" day-timeline + horizontal scheduled-payments timeline) and asked for it
  restyled onto HSBC primitives.
- **Built the restyle, then you caught three real problems in a row, each by looking, not by
  trusting my report:**
  1. A screenshot showed the hero balance number effectively invisible — root cause was a
     `:root`-only token-alias block freezing to the light theme (exactly the trap canon.css
     documents at its own line 495-496). Fixed.
  2. You asked directly: **"did you put this through the gates or use your own inference?"**
     Answer: inference, not gates — confirmed no `_SCREEN-GATE.md` existed and the file wasn't
     even named `*.canon.html` so the default gate glob would've missed it either way. Ran
     `_validate_screen.py` for real: **FAIL** (2 hex-in-comments, 3 hand-drawn icons that weren't
     library-sourced). Fixed both, re-ran: **PASS**.
  3. You said **"this would fail accessibility for a start."** Ran the `design:accessibility-review`
     skill + computed real WCAG contrast ratios against canon's actual dark-theme hex values (the
     gate's own a11y check only covers reduced-motion/target-size — a false-confidence gap, same
     shape as the earlier state-contrast blind spot). Found 4 genuine 1.4.3 failures, all inside my
     own hand-invented tint compositions, not canon's reviewed patterns — worst was 2.92:1 (needs
     4.5:1). Fixed all 4 with real numbers verified, plus closed a modal keyboard-trap gap found in
     the same pass. Re-ran gate: **PASS**.
- **Then your actual verdict, unprompted, after all of that:** "the canon works but probably no
  better than an AI model tied to a component library. The layouts tend to be better and the extra
  'assumptions' or gap fillers seem better when unconstrained... I expected something like:
  unconstrained with the right styling." You want a session dedicated to working this out, and
  flagged we're stuck on the seaworthiness plan's §9 parallel-track line. You also said, live: **"its
  just about crafting the rules I guess, i need to read through them"** — your own current working
  hypothesis, not yet confirmed.

## On your desk

- **The reading you said you want to do:** `_FIXED-FLEX-CHARTER.md` §9 (the ramp definition) and
  `_TEST-BRIEF-v2-sme-payments.md` §2 (the actual per-band instructions, including the gravity
  block) — these are the exact rules behind everything generated this session.
- **The alternative hypothesis, for when you get there:** memory `generation-mechanism-ideas` Idea 2
  ("generate-then-normalise," parked 2026-07-01) describes almost exactly what happened by accident
  this session (diagnostic → hand-restyle-and-fix). Worth weighing against "it's just the rules."
- Everything committed this session, ready to push via GitHub Desktop.

## Queue next (fresh session, dedicated — per your ask)

1. **"What does the §9 spread actually reveal?"** — full framing in `_LIVE-STATE.md` OPEN section.
   Two live hypotheses to weigh, unranked: (a) rule/prompt-crafting quality — fixable by better
   instructions, no architecture change; (b) a structural ceiling — one governed pass may just cap
   out below a two-pass "generate free, then constrain+verify" pipeline (which is what actually
   worked this session, unplanned). Nobody has run these as a genuinely controlled comparison yet.
   **Build the knowledge-usage trace as PREP TOOLING inside this same session** (your ask, end of
   this session, agreed to fold in rather than build separately): a self-reported "sources" manifest
   per cold run + an automatic verification pass against the real artifact (extends
   `_validate_icons.py`'s byte-match technique + `_build_xref_index.py`'s existing token/guideline
   map) — gives real, comparable data on what each lineage (governed vs gravity-fix vs diagnostic)
   actually retrieved vs invented, which is close to a direct empirical answer to the question above.
2. Ingestion Phase 1 (Sutherland migration) still queued whenever you want to bank it — not
   cancelled, just still not this.
3. Off critical path unless you say: D2 novel-screen (waiting on colleague), toolkit tranche 2,
   harness-modes exploration, TOV spin-off, ADR-0004 ops follow-ups.

> Next-session opener: **"Title this chat: <pick one>."** Read GOOD-MORNING → `_LIVE-STATE.md` OPEN
> entry → charter §9 + test-brief §2 if doing the dedicated §9 session; → `_SEAWORTHINESS-PLAN_2026-07-05.md`
> if picking up Phase 1 instead (§9 track is paused there, not next-in-line).
