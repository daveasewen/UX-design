# Knowledge graph — health report

> Generated derived view over `knowledge/` (Graphify-inspired; no external dependency). Regenerate after editing component metas or tokens: `python3 knowledge/tokens/_build_blast_radius.py`. Authored canon stays the source of truth; this is a generated dashboard.

**Totals:** 32 components · 639 tokens defined · 88 tokens referenced by components · compliance: 31 rules x 32 components (31 SCs).

## God-nodes — highest token blast radius

Change one of these and the listed number of components is affected. Use before any token rebind/rename (esp. the Sutherland migration).

| Token | Blast | Example components |
|---|---|---|
| `text/default` | 29 | Accordion, Avatar, Breadcrumbs, Button, Cards, Countdown timer… |
| `icon/default` | 20 | Accordion, Avatar, Button, Cards, Dropdown, Headers… |
| `text/reverse` | 15 | Avatar, Badge, Button, Cards, Dropdown, Hero… |
| `icon/default-reverse` | 14 | Avatar, Button, Cards, Dropdown, Hero, Input fields… |
| `background/default` | 13 | Accordion, Cards, Dropdown, Input fields, Modals, Navigations… |
| `text/disabled` | 10 | Avatar, Button, Dropdown, Input fields, Links, List items… |
| `icon/disabled` | 9 | Avatar, Badge, Button, Dropdown, Input fields, Links… |
| `tertiary/background/default` | 8 | Button, Cards, List items, Modals, Search field, Slider… |
| `color/primary` | 7 | Badge, Cards, Hero, Links, List items, Navigations… |
| `divider/border/subsection` | 7 | Divider, Dropdown, Input fields, Navigations, Pagination, Search field… |
| `elevation/functional` | 7 | Dropdown, Input fields, Navigations, Notifications, Search field, Tabs… |
| `form/border/default` | 7 | Dropdown, Input fields, Search field, Selection controls, Slider, Tags… |
| `tertiary/background/hover` | 7 | Accordion, Avatar, Button, Cards, Reorder, Slider… |
| `border/subtle` | 6 | Accordion, Avatar, Cards, Hero, Navigations, Slider |
| `divider/border/section` | 6 | Divider, Dropdown, List items, Pagination, Tabs, Tooltip |

## Token-group reach (components using each group)

| Group | Components |
|---|---|
| `text/` | 30 |
| `icon/` | 22 |
| `tertiary/` | 14 |
| `background/` | 13 |
| `divider/` | 9 |
| `form/` | 9 |
| `rag/` | 8 |
| `padding/` | 7 |
| `primary/` | 7 |
| `color/` | 7 |
| `elevation/` | 7 |
| `border/` | 6 |
| `typography/` | 6 |
| `secondary/` | 4 |
| `scrollbar/` | 3 |
| `blur/` | 3 |
| `overlay/` | 3 |
| `scale/` | 2 |
| `image/` | 2 |
| `border-width/` | 2 |
| `focus/` | 2 |
| `layout/` | 2 |
| `timer/` | 1 |
| `gap/` | 1 |
| `progress/` | 1 |
| `table/` | 1 |
| `tabs/` | 1 |
| `border-radius/` | 1 |

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

551 of 639 defined tokens are unreferenced at the component layer. **Expected** for primitives and scale steps (consumed via semantic aliases, not bound directly); worth scanning the *semantic* groups for genuinely-dead tokens. By group:

| Group | Unreferenced |
|---|---|
| `color/` | 139 |
| `data-vis/` | 90 |
| `typography/` | 33 |
| `icon/` | 28 |
| `gap/` | 27 |
| `rag/` | 22 |
| `padding/` | 20 |
| `tabs/` | 20 |
| `primary/` | 19 |
| `secondary/` | 19 |
| `tertiary/` | 19 |
| `elevation/` | 15 |
| `form/` | 15 |
| `text/` | 10 |
| `divider/` | 8 |
| `breakpoint/` | 6 |
| `motion/` | 6 |
| `table/` | 6 |
| `tooltip/` | 6 |
| `border/` | 5 |
| `blur/` | 4 |
| `image/` | 4 |
| `overlay/` | 4 |
| `progress/` | 4 |
| `scrollbar/` | 4 |
| `timer/` | 4 |
| `layout/` | 3 |
| `scale/` | 3 |
| `background/` | 2 |
| `border-width/` | 2 |
| `focus/` | 2 |
| `radius/` | 1 |
| `spacing/` | 1 |

> Method: token usage matched by scanning each meta's `tokens`/`subComponents`/`variants` blocks for exact store token paths (word-boundary safe). Misses any token referenced only in prose elsewhere; treat blast counts as a strong lower bound.
