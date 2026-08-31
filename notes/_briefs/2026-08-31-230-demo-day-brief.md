# #230 brief — DEMO DAY: Dave presents Apollo live in VS Code + Copilot, 2026-09-01

provenance: 230 · 2026-08-31
status: floated
row: W-308 (deadline 2026-09-01 — the store's first deadline-bearing row)

**Dave's words, #230 (2026-08-31):** "remember I have to present Apollo tomorrow and I want it
to be tight" · "I am presenting Apollo working in VS code with co-pilot … I really think we can
get to my result quicker" · "We need to get this done, it is a priority … I need time to test
it. No mistakes, lets do everything right, slow is smooth and smooth is fast" · "the
presentation is the priority, but fix any dependencies first i want it to run smooth".

## What the demo is

The W-304 cold-start acceptance shape, live, in front of internal stakeholders: a dashboard
prompted in VS Code + Copilot with the Apollo pack installed, reaching the result Dave's own
test run took ~5 rounds of fettling to reach. Audience register: internal — progress,
capability, roadmap. ⚠ Public-positioning fence applies: abstract framing ("lovable on
rails", Discover/Create/Craft/Dispatch), never gate/token mechanics.

## ⛔ PREMISE CORRECTION — Dave, #230 (2026-08-31), verbatim

> "the design I provided shouldn't be regarded as 'good' apart from visually good, it is
> what I want to get to as soon as possible but the code will be a mess because it was vibed
> without using the design skill initially. It was just a prompt with a few rounds after."

> And, same session: "look it should just be created from the components … i've already
> explained this."

**The mechanism, restated so it cannot drift:** the demo dashboard is ASSEMBLED FROM THE
COMPONENTS — the shipped contract's own words (`apollo-spider/cold-start/DESIGN-CONTRACT.md`,
in v1.0.4): *"Copy the markup. Component HTML comes from `knowledge/snippets/`, never from
memory"* · *"Never invent. If the system does not have it, stop and name the gap"* ·
*"Dashboards are bento-first."* Every rehearsal grade and every triage adoption serves THAT
path. A gap between the components and his target look is closed IN THE COMPONENTS, never by
freestyle markup.

**What this changes:** `dashboards/international-banking-dashboard.canon.html` is the VISUAL
standard only. Its code is explicitly disowned — nothing in it is ported, copied, or treated
as an example. "Reach Dave's result" = reach THAT LOOK via the clean path (canon tokens,
components, the regen serial). The regen-diff's "8 dave-improvements" are visual intents
canon lacks, to be implemented canon-side from scratch, never lifted from his file. The
same fence applies to the 8 GPT-modified files in his pack copy: treat as findings, re-derive
any fix properly.

## The evidence base (do not rebuild any of it)

- **His test run** (2026-08-29, corp machine, Copilot/GPT-Sol, cold, no skills):
  `dashboards/international-banking-dashboard.canon.html` — the standard to reach.
- **The diff**: `notes/_subreports/2026-08-30-227-dashboard-regen-diff.md` — 25 findings
  (3 generation defects · 14 canon gaps · 8 Dave-improvements). Compare page
  `reviews/DASHBOARD-REGEN-COMPARE-2026-08-30-v1.html`; decision surface
  `reviews/DASHBOARD-DIFF-DECISIONS-2026-08-30-v1.html` (32 cards, unworked).
- **The forensics**: `notes/_subreports/2026-08-29-224-copilot-forensics.md` — he tested
  v1.0.2; encoder fallback PROVEN working; "token count didn't work" = the never-shipped
  session gauge (vocabulary collision); GPT's fix = 3-key `.vscode/settings.json` telemetry
  tap. **Port-back landed: v1.0.4 ships the settings file + corrected runbook.**
- **The pack**: v1.0.4 CUT + RATIFIED (`s228-D4`), carries the cold-start group
  (DESIGN-CONTRACT.md 30 lines + projections + placement checker + report template).
- **The ruling**: `s229-D1` — the formal acceptance test (W-304) runs only after Dave is
  happy with design results. The demo is Dave's own act and does not close W-304.

## The plan (this session)

1. Triage lane (Opus): rank the 32 cards + 25 findings by "blocks a cold seat reaching his
   dashboard"; produce a decision page with a recommended demo-blocking ADOPT subset.
   Decision surface only — adoption is Dave's.
2. Dave rules on the subset; enact lane lands the adoptions with the full regen serial.
3. Rehearsal: cold-ish dry-run against the pack (declared approximation of W-304 — not
   Copilot, not genuinely cold; it measures remaining fettling distance, it proves nothing
   about W-304).
4. Dave's own test window on his machine — protected time, the last beat of the day.

## Pitfalls — replayed

- His 8 improvements exist only in HIS pack copy and the rescued artefact — the shipped
  v1.0.4 does NOT carry them; if adopted they need the full ordered regen serial, ramp first.
- One cold run is an anecdote, not a measurement (W-304 brief) — the rehearsal is demo prep,
  not the acceptance test.
- A mint assert proves VALUES, never CONSUMPTION — any adopted canon change wants an eye on a
  render, not just green gates.
- Corp machine: tiktoken blocked is EXPECTED and fine (purepy fallback proven); the gauge now
  reads via `.vscode/settings.json` — verify the settings file survives his pack install.
- Nothing survives a tool-call boundary; render-verify per the receipted mount-side recipe.
