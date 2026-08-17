# Knowledge graph — health report

> Generated derived view over `knowledge/` (Graphify-inspired; no external dependency). Regenerate after editing component metas or tokens: `python3 knowledge/tokens/_build_blast_radius.py`. Authored canon stays the source of truth; this is a generated dashboard.

**Totals:** 76 components · 1016 tokens defined · 112 tokens referenced by components · compliance: 31 rules x 75 components (31 SCs).

## God-nodes — highest token blast radius

Change one of these and the listed number of components is affected. Use before any token rebind/rename (esp. the Sutherland migration).

| Token | Blast | Example components |
|---|---|---|
| `text/default` | 60 | Accordion, Account card, Alert, Amount display, Amount input, Avatar… |
| `background/default` | 38 | Accordion, Account selector, Amount display, Bar chart, Box plot, Bullet chart… |
| `icon/default` | 25 | Accordion, Avatar, Button, Cards, Dropdown, File upload… |
| `elevation/functional` | 22 | Account selector, Bar chart, Butterfly chart (horizontal), Butterfly chart (vertical), Combo chart, Date picker… |
| `text/reverse` | 18 | Action bar, Avatar, Badge, Button, Cards, Confirmation… |
| `tertiary/background/default` | 17 | Account card, Action bar, Button, Cards, Drawer, Icon button… |
| `border/subtle` | 16 | Accordion, Account card, Action bar, Amount display, Avatar, Cards… |
| `rag/error` | 16 | Amount input, Bar chart, Date picker, Date-range picker, Dropdown, File upload… |
| `elevation/border` | 15 | Account selector, Bar chart, Butterfly chart (horizontal), Butterfly chart (vertical), Combo chart, Date picker… |
| `icon/default-reverse` | 15 | Avatar, Button, Cards, Dropdown, Hero, Icon button… |
| `rag/success` | 15 | Account card, Amount input, Bar chart, Button, Confirmation, File upload… |
| `tertiary/background/hover` | 15 | Accordion, Avatar, Button, Cards, Confirmation, Data grid… |
| `data/series/1` | 13 | Bar chart, Box plot, Bullet chart, Butterfly chart (horizontal), Butterfly chart (vertical), Combo chart… |
| `typography/font-family/default` | 13 | Account card, Action bar, Amount display, Avatar, Badge, Breadcrumbs… |
| `form/border/default` | 12 | Account card, Account selector, Data grid, Dropdown, File upload, Input fields… |

## Token-group reach (components using each group)

| Group | Components |
|---|---|
| `text/` | 64 |
| `background/` | 38 |
| `tertiary/` | 27 |
| `icon/` | 27 |
| `rag/` | 23 |
| `elevation/` | 22 |
| `border-radius/` | 21 |
| `border/` | 19 |
| `form/` | 17 |
| `data/` | 15 |
| `typography/` | 13 |
| `divider/` | 10 |
| `secondary/` | 9 |
| `primary/` | 9 |
| `padding/` | 7 |
| `color/` | 7 |
| `overlay/` | 5 |
| `scale/` | 4 |
| `focus/` | 4 |
| `scrollbar/` | 3 |
| `blur/` | 3 |
| `progress/` | 3 |
| `step/` | 3 |
| `image/` | 2 |
| `border-width/` | 2 |
| `table/` | 2 |
| `button/` | 2 |
| `layout/` | 2 |
| `timer/` | 1 |
| `gap/` | 1 |
| `target/` | 1 |
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

904 of 1016 defined tokens are unreferenced at the component layer. **Expected** for primitives and scale steps (consumed via semantic aliases, not bound directly); worth scanning the *semantic* groups for genuinely-dead tokens. By group:

| Group | Unreferenced |
|---|---|
| `color/` | 241 |
| `data-vis/` | 90 |
| `rag/` | 66 |
| `button/` | 64 |
| `data/` | 53 |
| `typography/` | 42 |
| `surface/` | 36 |
| `gap/` | 27 |
| `tabs/` | 26 |
| `alpha/` | 24 |
| `primary/` | 19 |
| `secondary/` | 19 |
| `tertiary/` | 18 |
| `text/` | 17 |
| `icon/` | 16 |
| `elevation/` | 15 |
| `form/` | 15 |
| `motion/` | 12 |
| `component/` | 11 |
| `editorial/` | 9 |
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
| `step/` | 4 |
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
