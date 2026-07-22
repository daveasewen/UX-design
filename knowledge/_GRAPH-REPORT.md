# Knowledge graph — health report

> Generated derived view over `knowledge/` (Graphify-inspired; no external dependency). Regenerate after editing component metas or tokens: `python3 knowledge/tokens/_build_blast_radius.py`. Authored canon stays the source of truth; this is a generated dashboard.

**Totals:** 64 components · 926 tokens defined · 104 tokens referenced by components · compliance: 31 rules x 64 components (31 SCs).

## God-nodes — highest token blast radius

Change one of these and the listed number of components is affected. Use before any token rebind/rename (esp. the Sutherland migration).

| Token | Blast | Example components |
|---|---|---|
| `text/default` | 54 | Accordion, Account card, Alert, Amount display, Amount input, Avatar… |
| `background/default` | 25 | Accordion, Account selector, Amount display, Bar chart, Cards, Data grid… |
| `icon/default` | 24 | Accordion, Avatar, Button, Cards, Dropdown, File upload… |
| `text/reverse` | 18 | Action bar, Avatar, Badge, Button, Cards, Confirmation… |
| `elevation/functional` | 16 | Account selector, Date picker, Date-range picker, Drawer, Dropdown, Input fields… |
| `rag/error` | 16 | Amount input, Bar chart, Date picker, Date-range picker, Dropdown, File upload… |
| `tertiary/background/default` | 16 | Account card, Action bar, Button, Cards, Drawer, Icon button… |
| `border/subtle` | 15 | Accordion, Account card, Action bar, Amount display, Avatar, Cards… |
| `icon/default-reverse` | 15 | Avatar, Button, Cards, Dropdown, Hero, Icon button… |
| `tertiary/background/hover` | 14 | Accordion, Avatar, Button, Cards, Confirmation, Data grid… |
| `rag/success` | 13 | Account card, Amount input, Bar chart, Button, Confirmation, File upload… |
| `typography/font-family/default` | 13 | Account card, Action bar, Amount display, Avatar, Badge, Breadcrumbs… |
| `form/border/default` | 11 | Account card, Account selector, Data grid, Dropdown, File upload, Input fields… |
| `border-radius/control` | 10 | Amount input, Data grid, Date picker, Date-range picker, File upload, Form layout… |
| `border-radius/surface` | 10 | Alert, Banner, Date picker, Date-range picker, Empty state, Popover… |

## Token-group reach (components using each group)

| Group | Components |
|---|---|
| `text/` | 58 |
| `tertiary/` | 26 |
| `icon/` | 26 |
| `background/` | 25 |
| `rag/` | 22 |
| `border-radius/` | 18 |
| `border/` | 17 |
| `form/` | 16 |
| `elevation/` | 16 |
| `typography/` | 13 |
| `divider/` | 10 |
| `primary/` | 9 |
| `secondary/` | 8 |
| `padding/` | 7 |
| `color/` | 7 |
| `data/` | 5 |
| `overlay/` | 5 |
| `scale/` | 3 |
| `scrollbar/` | 3 |
| `blur/` | 3 |
| `focus/` | 3 |
| `image/` | 2 |
| `border-width/` | 2 |
| `table/` | 2 |
| `button/` | 2 |
| `layout/` | 2 |
| `progress/` | 2 |
| `timer/` | 1 |
| `gap/` | 1 |
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

822 of 926 defined tokens are unreferenced at the component layer. **Expected** for primitives and scale steps (consumed via semantic aliases, not bound directly); worth scanning the *semantic* groups for genuinely-dead tokens. By group:

| Group | Unreferenced |
|---|---|
| `color/` | 241 |
| `data-vis/` | 90 |
| `button/` | 64 |
| `rag/` | 46 |
| `typography/` | 42 |
| `data/` | 39 |
| `surface/` | 36 |
| `gap/` | 27 |
| `tabs/` | 26 |
| `primary/` | 19 |
| `secondary/` | 19 |
| `tertiary/` | 18 |
| `text/` | 17 |
| `icon/` | 16 |
| `elevation/` | 15 |
| `form/` | 15 |
| `motion/` | 12 |
| `divider/` | 8 |
| `border/` | 7 |
| `breakpoint/` | 6 |
| `padding/` | 6 |
| `table/` | 6 |
| `tooltip/` | 6 |
| `blur/` | 4 |
| `image/` | 4 |
| `overlay/` | 4 |
| `progress/` | 4 |
| `scrollbar/` | 4 |
| `timer/` | 4 |
| `badge/` | 3 |
| `layout/` | 3 |
| `scale/` | 3 |
| `background/` | 2 |
| `border-width/` | 2 |
| `focus/` | 2 |
| `radius/` | 1 |
| `spacing/` | 1 |

> Method: token usage matched by scanning each meta's `tokens`/`subComponents`/`variants` blocks for exact store token paths (word-boundary safe). Misses any token referenced only in prose elsewhere; treat blast counts as a strong lower bound.
