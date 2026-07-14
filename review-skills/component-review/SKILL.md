---
name: component-review
description: Render reviewed components as a Swiss-styled HTML review gallery — every component shown in LIGHT and DARK side by side, carefully labelled, from the design system's own reviewed snippets and canon.css. Includes a DIFF mode that puts two versions before/after (per theme) so iterative changes are obvious at a glance. Use to produce, review, and sign off components, and to review a round of changes.
---

# Component review

Produces a **single self-contained HTML gallery** for reviewing components. Every
component is shown **light and dark at the same time**, side by side and labelled,
built from its *own reviewed snippet* wrapped in its `.cn-<slug>` scope over
`canon.css` — so what you review is exactly what the gated snippet renders, in both
themes, on one page.

Two modes:
- **Review** (default) — all components (or a subset), each Light | Dark.
- **Diff** — two versions before/after in a 2×2 (Before·Light / After·Light /
  Before·Dark / After·Dark), each component flagged **Changed / New / Removed /
  Unchanged**, with a "show changed only" toggle. For iterative sign-off.

## Why it can show both themes on one page
`canon.css` re-declares its semantic aliases on `:root, [data-theme="light"],
[data-theme="dark"]`, so the theme can live on a **wrapper element**, not just
`<html>`. Each pane carries its own `data-theme`, so light and dark resolve
correctly against a **single** inlined `canon.css` — no iframes, no duplication of
the stylesheet.

## Use it
Run the generator from anywhere; point it at the snippets + canon.css.

```bash
# all reviewed components, light + dark:
python3 gen_component_review.py \
  --snippets knowledge/snippets --canon knowledge/canon/canon.css \
  --out component-review.html --subject "Canon components" --date 2026-07-14

# just a few:
python3 gen_component_review.py --only Button,Accordion,Modals  ... 

# review a round of changes (before vs after — each a snippets dir):
python3 gen_component_review.py \
  --diff path/to/OLD-snippets path/to/NEW-snippets \
  --canon knowledge/canon/canon.css \
  --out component-review-diff.html --subject "Badge iteration"
```

`canon.css` is **inlined** into the output, so the file shares with no setup.
Change detection in diff mode is by normalised snippet content (whitespace-insensitive).

## What it does under the hood (so you can trust the output)
- Takes each component's `*.reference.html` snippet, strips the demo `<script>` and
  `demo-controls`, and renders the demo body in its `.cn-<slug>` scope.
- Reveals interactive components (dropdown, accordion, tabs, modal, tooltip) in a
  **representative shown state** for visual review — the same philosophy as the
  canon gallery. Drive real behaviour from the component's own script on a real screen.
- **Namespaces every internal `id` and its references** (`for`, `aria-controls`,
  `aria-labelledby`, …) per pane, so the light/dark (and before/after) copies never
  collide — while **sprite `<use href="#…">` refs are preserved** so icons still resolve.

## Procedure for a review
1. Generate the gallery (Review mode) against the current snippets.
2. **Render and look at both themes** — every real defect to date was visual and passed
   the static gates. Check contrast, dark-mode surfaces, focus, labelling.
3. Record findings in a **review-dossier** (sibling skill) if you want a shareable
   write-up with severities and plain-language notes.
4. For an iteration: keep the previous snippets, generate **Diff mode** old→new, flip
   "show changed only", and sign off just what moved.

## Output
One self-contained `*.html` gallery. Review mode = Light | Dark per component.
Diff mode = Before/After × Light/Dark, changed items flagged and filterable.

## Notes
- This is a **visual** review surface. Authoritative contrast/token/a11y checks run as
  the executable gates in CI; this is where a human *looks*.
- Pairs with **review-dossier** (write up what you found) and the **swiss-design-system**
  skill (the shared house style).

*Experimental.*
