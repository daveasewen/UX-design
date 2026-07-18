---
name: review-preview-html
description: "Preference — when presenting component work for review, always surface the live HTML fitness-test as the preview, not PNG screenshots"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: cd98102c-f188-43e0-8a47-97646be8c5c7
---

**RULE (Dave, 2026-06-24):** when presenting a component for review, the preview Dave wants is ALWAYS the live HTML file (the `_fitness-test/*.html`), presented via `present_files` — NOT PNG screenshots. The interactive HTML (toggle theme, drag width slider, hover/focus/press) is far more useful for review than static images.

**Why:** he can actually exercise states, theming and reflow himself; PNGs are lossy and can't show interaction. Said explicitly after PNG-led presentations for Button/Links/Tags.

**How to apply:** still render PNGs if useful for MY OWN verification (the gate-blindspot visual backstop — I view them to catch defects), but the thing I PRESENT to Dave is the HTML. Lead with the HTML card. Relates to [[component-review-program]], [[gate-blindspot-state-contrast]] (render-for-verification stays), [[comms-style-exec-summary]].
