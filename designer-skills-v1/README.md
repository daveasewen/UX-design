# Design-system skills for Copilot (v1 — experimental)

A small set of **skills** that make your Copilot aware of our design system — its
components, tokens, and brand + accessibility standards — so what it helps you
build is on-brand and accessible from the start, and the new patterns you create
can be captured and shared.

It's **early and experimental** — poke at it, and tell us what's useful and what's
missing. It's here to support your work, not replace the craft.

## What's in the pack
Four skills:

- **generate-from-canon** — build a screen/component using only the design system;
  it flags gaps instead of inventing.
- **check-against-design-system** — review your work; flags invented components,
  hard-coded values, missing states.
- **usability-review** — an expert usability pass (Nielsen's 10 heuristics).
- **draft-a-new-pattern** — help create a *new* component/pattern that fits the
  system, packaged as a candidate to propose for the library.

Plus the **`knowledge/` folder** (the components, tokens and guidelines the skills
read) and the repo's **`AGENTS.md`** (always-on project context).

## Setup (to confirm against your existing skills)
1. Drop the four skill folders into your skills location — Copilot reads
   `.claude/skills/` and `.github/skills/`. **Use whichever your current skills
   already live in** so these sit alongside them.
2. Make sure the **`knowledge/` folder is in the repo** — the skills read from it
   (`knowledge/components/`, `knowledge/tokens/`, `knowledge/canon/`,
   `knowledge/snippets/`). Adjust the paths in the skills if your layout differs.
3. Keep **`AGENTS.md`** at the repo root.

## How to use
Describe your task in Copilot and it should pick the right skill, or invoke one by
name. Start with **generate-from-canon** for a screen, **check-against-design-system**
on something you've made, and **draft-a-new-pattern** when the system is missing
something.

## Honest caveats
- The **authoritative** compliance checks (real contrast maths, token fidelity,
  accessibility, icon provenance) run as executable gates in CI. The in-editor
  `check-against-design-system` applies the same rules as *guidance* so you catch
  drift early — it doesn't replace the CI gate run.
- New patterns from **draft-a-new-pattern** are **candidates for review**, not
  automatically part of the library — a human promotes them.

## Feedback
Tell us: which skills earned their place, where they got in the way, and — most
useful of all — what the system was **missing** when you tried to build something.
