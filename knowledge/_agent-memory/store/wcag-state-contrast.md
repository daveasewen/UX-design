---
name: wcag-state-contrast
description: "Dave's rule for judging interactive-state differentiation (hover/active/pressed) against WCAG when reviewing components"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 92c69cca-fca7-4999-a3d7-517fe5550c6c
---

When reviewing a component's interactive states for accessibility, apply this (Dave, 2026-06-17): WCAG requires a **fair amount of contrast between states**, and a **single colour change is not sufficient** to differentiate a state. **Active/pressed is more important than hover** and warrants stronger differentiation.

**Why:** colour-only state changes can fail users with low vision / colour-vision deficiency; meaningful state change should be conveyed by more than one cue.

**How to apply:** when assessing component state tokens (e.g. in `*.meta.json` accessibility/anti-patterns), don't flag a "heavy" state change as wrong if it stacks multiple cues — that's the point. E.g. the [[promenaut-project-status]] Accordion pressed state uses background colour + a second colour change + an icon change; that's WCAG-aligned, not over-engineered (Dave acknowledged it may be revisited but it isn't a defect). Conversely, DO flag states that differ by a single colour change only, especially active/pressed.
