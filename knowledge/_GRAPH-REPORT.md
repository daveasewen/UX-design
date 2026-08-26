# Knowledge graph — health report

> Generated derived view over `knowledge/` (Graphify-inspired; no external dependency). Regenerate after editing component metas or tokens: `python3 knowledge/tokens/_build_blast_radius.py`. Authored canon stays the source of truth; this is a generated dashboard.

**Totals:** 135 components · 1043 tokens defined · 131 tokens referenced by components · compliance: 38 rules x 133 components (38 SCs).

## God-nodes — highest token blast radius

Change one of these and the listed number of components is affected. Use before any token rebind/rename (esp. the Sutherland migration).

| Token | Blast | Example components |
|---|---|---|
| `text/default` | 106 | Accordion, Account card, Alert, Amount display, Amount input, Anchor nav… |
| `background/default` | 73 | Accordion, Account selector, Amount display, Anchor nav, App shell — doormat (mega-footer) nav, App shell — focused / full-page… |
| `tertiary/background/default` | 50 | Account card, Action bar, Anchor nav, App shell — doormat (mega-footer) nav, App shell — focused / full-page, App shell — multi-column… |
| `icon/default` | 46 | Accordion, App shell — doormat (mega-footer) nav, App shell — focused / full-page, App shell — multi-column, App shell — nav rail, App shell — side nav… |
| `border-radius/surface` | 43 | Alert, Anchor nav, App shell — doormat (mega-footer) nav, App shell — focused / full-page, App shell — multi-column, App shell — nav rail… |
| `focus/ring` | 39 | Anchor nav, App shell — doormat (mega-footer) nav, App shell — focused / full-page, App shell — multi-column, App shell — nav rail, App shell — side nav… |
| `text/secondary` | 38 | Account card, Amount display, Anchor nav, App shell — doormat (mega-footer) nav, App shell — focused / full-page, App shell — multi-column… |
| `border/subtle` | 37 | Accordion, Account card, Action bar, Amount display, Avatar, Avatar group… |
| `tertiary/background/hover` | 35 | Accordion, Anchor nav, App shell — doormat (mega-footer) nav, App shell — focused / full-page, App shell — multi-column, App shell — nav rail… |
| `divider/border/section` | 34 | Anchor nav, App shell — doormat (mega-footer) nav, App shell — focused / full-page, App shell — multi-column, App shell — nav rail, App shell — side nav… |
| `border-radius/control` | 33 | Amount input, App shell — doormat (mega-footer) nav, App shell — focused / full-page, App shell — multi-column, App shell — nav rail, App shell — side nav… |
| `elevation/functional` | 29 | Account selector, App shell — nav rail, Bar chart, Butterfly chart (horizontal), Butterfly chart (vertical), Card-header-lockup… |
| `form/border/default` | 29 | Account card, Account selector, App shell — split, Cascader, Combobox, Command palette… |
| `rag/success` | 29 | Account card, Amount input, Bar chart, Button, Card-header-lockup, Confirmation… |
| `rag/error` | 27 | Amount input, Bar chart, Combobox, Date picker, Date-range picker, Dropdown… |

## Token-group reach (components using each group)

| Group | Components |
|---|---|
| `text/` | 111 |
| `background/` | 73 |
| `tertiary/` | 63 |
| `border-radius/` | 61 |
| `icon/` | 48 |
| `rag/` | 47 |
| `form/` | 43 |
| `border/` | 40 |
| `divider/` | 40 |
| `focus/` | 39 |
| `elevation/` | 29 |
| `primary/` | 20 |
| `target/` | 20 |
| `data/` | 17 |
| `typography/` | 13 |
| `secondary/` | 13 |
| `surface/` | 12 |
| `overlay/` | 10 |
| `padding/` | 7 |
| `color/` | 7 |
| `progress/` | 6 |
| `layout/` | 6 |
| `alpha/` | 6 |
| `scale/` | 5 |
| `table/` | 5 |
| `scrollbar/` | 4 |
| `blur/` | 3 |
| `button/` | 3 |
| `step/` | 3 |
| `image/` | 2 |
| `border-width/` | 2 |
| `badge/` | 2 |
| `tabs/` | 2 |
| `timer/` | 1 |
| `gap/` | 1 |

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

912 of 1043 defined tokens are unreferenced at the component layer. **Expected** for primitives and scale steps (consumed via semantic aliases, not bound directly); worth scanning the *semantic* groups for genuinely-dead tokens. By group:

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
| `layout/` | 6 |
| `table/` | 6 |
| `tooltip/` | 6 |
| `size/` | 5 |
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
| `radius/` | 1 |
| `spacing/` | 1 |

> Method: token usage matched by scanning each meta's `tokens`/`subComponents`/`variants` blocks for exact store token paths (word-boundary safe). Misses any token referenced only in prose elsewhere; treat blast counts as a strong lower bound.
