# Knowledge graph — health report

> Generated derived view over `knowledge/` (Graphify-inspired; no external dependency). Regenerate after editing component metas or tokens: `python3 knowledge/tokens/_build_blast_radius.py`. Authored canon stays the source of truth; this is a generated dashboard.

**Totals:** 91 components · 1033 tokens defined · 119 tokens referenced by components · compliance: 31 rules x 91 components (35 SCs).

## God-nodes — highest token blast radius

Change one of these and the listed number of components is affected. Use before any token rebind/rename (esp. the Sutherland migration).

| Token | Blast | Example components |
|---|---|---|
| `text/default` | 75 | Accordion, Account card, Alert, Amount display, Amount input, Anchor nav… |
| `background/default` | 49 | Accordion, Account selector, Amount display, Anchor nav, Avatar group, Bar chart… |
| `icon/default` | 33 | Accordion, Avatar, Avatar group, Button, Cards, Combobox… |
| `elevation/functional` | 26 | Account selector, Bar chart, Butterfly chart (horizontal), Butterfly chart (vertical), Combo chart, Combobox… |
| `tertiary/background/default` | 25 | Account card, Action bar, Anchor nav, Button, Cards, Command palette… |
| `border-radius/surface` | 22 | Alert, Anchor nav, Banner, Combo chart, Combobox, Command palette… |
| `tertiary/background/hover` | 22 | Accordion, Anchor nav, Avatar, Avatar group, Button, Cards… |
| `border/subtle` | 21 | Accordion, Account card, Action bar, Amount display, Avatar, Avatar group… |
| `rag/error` | 21 | Amount input, Bar chart, Combobox, Date picker, Date-range picker, Dropdown… |
| `elevation/border` | 19 | Account selector, Bar chart, Butterfly chart (horizontal), Butterfly chart (vertical), Combo chart, Combobox… |
| `rag/success` | 19 | Account card, Amount input, Bar chart, Button, Confirmation, Coverage / runway bar… |
| `focus/ring` | 18 | Anchor nav, Avatar group, Combobox, Command palette, Document row, Footer… |
| `form/border/default` | 18 | Account card, Account selector, Combobox, Command palette, Data grid, Dropdown… |
| `text/reverse` | 18 | Action bar, Avatar, Badge, Button, Cards, Confirmation… |
| `text/secondary` | 18 | Account card, Amount display, Anchor nav, Cards, Command palette, Confirmation… |

## Token-group reach (components using each group)

| Group | Components |
|---|---|
| `text/` | 79 |
| `background/` | 49 |
| `tertiary/` | 37 |
| `icon/` | 35 |
| `border-radius/` | 35 |
| `rag/` | 32 |
| `elevation/` | 26 |
| `border/` | 24 |
| `form/` | 24 |
| `divider/` | 18 |
| `focus/` | 18 |
| `data/` | 15 |
| `typography/` | 13 |
| `primary/` | 11 |
| `secondary/` | 9 |
| `padding/` | 7 |
| `color/` | 7 |
| `target/` | 7 |
| `overlay/` | 6 |
| `scale/` | 4 |
| `progress/` | 4 |
| `scrollbar/` | 3 |
| `blur/` | 3 |
| `button/` | 3 |
| `layout/` | 3 |
| `step/` | 3 |
| `image/` | 2 |
| `border-width/` | 2 |
| `table/` | 2 |
| `surface/` | 2 |
| `timer/` | 1 |
| `gap/` | 1 |
| `alpha/` | 1 |
| `tabs/` | 1 |

## Deprecated tokens still bound (migration worklist)

Components whose `tokens` block still references a `(depricate)` token (count = mentions). See `tokens/_manifests/depricate-replacement-map.json` `$usage_audit` for the rebind targets and `_DESIGN-SYSTEM-GAPS.md` for blockers.

| Component | (depricate) refs |
|---|---|
| Avatar | 6 |
| Tags | 6 |
| Quick actions | 5 |
| Selection controls | 5 |
| Links | 4 |
| Button | 3 |
| Headers | 3 |
| Pagination | 3 |
| View options | 3 |
| Divider | 2 |
| Input fields | 2 |
| Badge | 1 |
| Cards | 1 |
| List items | 1 |
| Navigations | 1 |
| Notifications | 1 |
| Search field | 1 |
| Slider | 1 |
| Status indicator | 1 |

## Orphans — defined tokens not referenced by any component meta

914 of 1033 defined tokens are unreferenced at the component layer. **Expected** for primitives and scale steps (consumed via semantic aliases, not bound directly); worth scanning the *semantic* groups for genuinely-dead tokens. By group:

| Group | Unreferenced |
|---|---|
| `color/` | 245 |
| `data-vis/` | 90 |
| `rag/` | 64 |
| `button/` | 63 |
| `data/` | 53 |
| `typography/` | 42 |
| `surface/` | 35 |
| `gap/` | 27 |
| `tabs/` | 26 |
| `alpha/` | 23 |
| `primary/` | 19 |
| `secondary/` | 19 |
| `tertiary/` | 18 |
| `text/` | 17 |
| `icon/` | 16 |
| `elevation/` | 15 |
| `form/` | 15 |
| `motion/` | 12 |
| `component/` | 11 |
| `padding/` | 10 |
| `border-radius/` | 9 |
| `editorial/` | 9 |
| `divider/` | 8 |
| `border/` | 7 |
| `breakpoint/` | 6 |
| `table/` | 6 |
| `tooltip/` | 6 |
| `blur/` | 4 |
| `image/` | 4 |
| `overlay/` | 4 |
| `progress/` | 4 |
| `scrollbar/` | 4 |
| `step/` | 4 |
| `timer/` | 4 |
| `badge/` | 3 |
| `scale/` | 3 |
| `background/` | 2 |
| `border-width/` | 2 |
| `focus/` | 2 |
| `layout/` | 1 |
| `radius/` | 1 |
| `spacing/` | 1 |

> Method: token usage matched by scanning each meta's `tokens`/`subComponents`/`variants` blocks for exact store token paths (word-boundary safe). Misses any token referenced only in prose elsewhere; treat blast counts as a strong lower bound.
