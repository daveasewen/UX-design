# Knowledge graph — health report

> Generated derived view over `knowledge/` (Graphify-inspired; no external dependency). Regenerate after editing component metas or tokens: `python3 knowledge/tokens/_build_blast_radius.py`. Authored canon stays the source of truth; this is a generated dashboard.

**Totals:** 54 components · 926 tokens defined · 102 tokens referenced by components · compliance: 31 rules x 54 components (31 SCs).

## God-nodes — highest token blast radius

Change one of these and the listed number of components is affected. Use before any token rebind/rename (esp. the Sutherland migration).

| Token | Blast | Example components |
|---|---|---|
| `text/default` | 45 | Accordion, Account card, Alert, Amount display, Amount input, Avatar… |
| `icon/default` | 22 | Accordion, Avatar, Button, Cards, Dropdown, Headers… |
| `background/default` | 17 | Accordion, Account selector, Amount display, Cards, Dropdown, Input fields… |
| `text/reverse` | 17 | Action bar, Avatar, Badge, Button, Cards, Confirmation… |
| `tertiary/background/default` | 16 | Account card, Action bar, Button, Cards, Drawer, Icon button… |
| `icon/default-reverse` | 15 | Avatar, Button, Cards, Dropdown, Hero, Icon button… |
| `border/subtle` | 14 | Accordion, Account card, Action bar, Amount display, Avatar, Cards… |
| `elevation/functional` | 13 | Account selector, Drawer, Dropdown, Input fields, Modal lightbox, Navigations… |
| `tertiary/background/hover` | 13 | Accordion, Avatar, Button, Cards, Confirmation, Icon button… |
| `typography/font-family/default` | 13 | Account card, Action bar, Amount display, Avatar, Badge, Breadcrumbs… |
| `rag/success` | 11 | Account card, Amount input, Button, Confirmation, Form layout, List items… |
| `icon/disabled` | 10 | Avatar, Badge, Button, Dropdown, Icon button, Input fields… |
| `rag/error` | 10 | Amount input, Dropdown, Form layout, Input fields, Notifications, Secure entry… |
| `text/disabled` | 10 | Avatar, Button, Dropdown, Input fields, Links, List items… |
| `form/border/default` | 9 | Account card, Account selector, Dropdown, Input fields, Search field, Selection controls… |

## Token-group reach (components using each group)

| Group | Components |
|---|---|
| `text/` | 48 |
| `tertiary/` | 25 |
| `icon/` | 24 |
| `background/` | 17 |
| `rag/` | 16 |
| `border/` | 14 |
| `typography/` | 13 |
| `elevation/` | 13 |
| `border-radius/` | 12 |
| `form/` | 11 |
| `divider/` | 10 |
| `primary/` | 9 |
| `padding/` | 7 |
| `secondary/` | 7 |
| `color/` | 7 |
| `overlay/` | 5 |
| `scale/` | 3 |
| `scrollbar/` | 3 |
| `blur/` | 3 |
| `focus/` | 3 |
| `image/` | 2 |
| `border-width/` | 2 |
| `button/` | 2 |
| `layout/` | 2 |
| `data/` | 1 |
| `timer/` | 1 |
| `gap/` | 1 |
| `progress/` | 1 |
| `table/` | 1 |
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

824 of 926 defined tokens are unreferenced at the component layer. **Expected** for primitives and scale steps (consumed via semantic aliases, not bound directly); worth scanning the *semantic* groups for genuinely-dead tokens. By group:

| Group | Unreferenced |
|---|---|
| `color/` | 241 |
| `data-vis/` | 90 |
| `button/` | 64 |
| `rag/` | 46 |
| `typography/` | 42 |
| `data/` | 40 |
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
| `border/` | 8 |
| `divider/` | 8 |
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
