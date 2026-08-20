# Knowledge graph — health report

> Generated derived view over `knowledge/` (Graphify-inspired; no external dependency). Regenerate after editing component metas or tokens: `python3 knowledge/tokens/_build_blast_radius.py`. Authored canon stays the source of truth; this is a generated dashboard.

**Totals:** 119 components · 1033 tokens defined · 131 tokens referenced by components · compliance: 35 rules x 91 components (35 SCs).

## God-nodes — highest token blast radius

Change one of these and the listed number of components is affected. Use before any token rebind/rename (esp. the Sutherland migration).

| Token | Blast | Example components |
|---|---|---|
| `text/default` | 96 | Accordion, Account card, Alert, Amount display, Amount input, Anchor nav… |
| `background/default` | 63 | Accordion, Account selector, Amount display, Anchor nav, App shell — multi-column, App shell — side nav… |
| `icon/default` | 41 | Accordion, App shell — multi-column, App shell — side nav, App shell — top / stacked nav, Avatar, Avatar group… |
| `tertiary/background/default` | 40 | Account card, Action bar, Anchor nav, App shell — multi-column, App shell — side nav, App shell — top / stacked nav… |
| `border-radius/surface` | 35 | Alert, Anchor nav, App shell — multi-column, App shell — side nav, App shell — top / stacked nav, Banner… |
| `focus/ring` | 35 | Anchor nav, App shell — multi-column, App shell — side nav, App shell — top / stacked nav, Avatar group, Calendar… |
| `border/subtle` | 33 | Accordion, Account card, Action bar, Amount display, Avatar, Avatar group… |
| `tertiary/background/hover` | 31 | Accordion, Anchor nav, App shell — multi-column, App shell — side nav, App shell — top / stacked nav, Avatar… |
| `text/secondary` | 30 | Account card, Amount display, Anchor nav, App shell — multi-column, App shell — side nav, App shell — top / stacked nav… |
| `divider/border/section` | 27 | Anchor nav, App shell — multi-column, App shell — side nav, App shell — top / stacked nav, Cascader, Combobox… |
| `elevation/functional` | 27 | Account selector, Bar chart, Butterfly chart (horizontal), Butterfly chart (vertical), Cascader, Combo chart… |
| `form/border/default` | 27 | Account card, Account selector, Cascader, Combobox, Command palette, Data grid… |
| `rag/success` | 27 | Account card, Amount input, Bar chart, Button, Confirmation, Coverage / runway bar… |
| `border-radius/control` | 26 | Amount input, App shell — multi-column, App shell — side nav, App shell — top / stacked nav, Calendar, Cascader… |
| `rag/error` | 26 | Amount input, Bar chart, Combobox, Date picker, Date-range picker, Dropdown… |

## Token-group reach (components using each group)

| Group | Components |
|---|---|
| `text/` | 100 |
| `background/` | 63 |
| `tertiary/` | 53 |
| `border-radius/` | 52 |
| `icon/` | 43 |
| `rag/` | 42 |
| `form/` | 38 |
| `border/` | 36 |
| `focus/` | 35 |
| `divider/` | 32 |
| `elevation/` | 27 |
| `data/` | 16 |
| `target/` | 16 |
| `primary/` | 14 |
| `typography/` | 13 |
| `secondary/` | 12 |
| `overlay/` | 8 |
| `padding/` | 7 |
| `surface/` | 7 |
| `color/` | 7 |
| `layout/` | 6 |
| `scale/` | 5 |
| `progress/` | 5 |
| `table/` | 4 |
| `scrollbar/` | 4 |
| `blur/` | 3 |
| `button/` | 3 |
| `alpha/` | 3 |
| `step/` | 3 |
| `image/` | 2 |
| `border-width/` | 2 |
| `tabs/` | 2 |
| `timer/` | 1 |
| `gap/` | 1 |
| `badge/` | 1 |

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

902 of 1033 defined tokens are unreferenced at the component layer. **Expected** for primitives and scale steps (consumed via semantic aliases, not bound directly); worth scanning the *semantic* groups for genuinely-dead tokens. By group:

| Group | Unreferenced |
|---|---|
| `color/` | 245 |
| `data-vis/` | 90 |
| `rag/` | 64 |
| `button/` | 63 |
| `data/` | 49 |
| `typography/` | 42 |
| `surface/` | 34 |
| `gap/` | 27 |
| `tabs/` | 24 |
| `alpha/` | 20 |
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
| `editorial/` | 9 |
| `border-radius/` | 8 |
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
| `scale/` | 3 |
| `background/` | 2 |
| `badge/` | 2 |
| `border-width/` | 2 |
| `focus/` | 2 |
| `layout/` | 1 |
| `radius/` | 1 |
| `spacing/` | 1 |

> Method: token usage matched by scanning each meta's `tokens`/`subComponents`/`variants` blocks for exact store token paths (word-boundary safe). Misses any token referenced only in prose elsewhere; treat blast counts as a strong lower bound.
