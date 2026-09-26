# Knowledge graph — health report

> Generated derived view over `knowledge/` (Graphify-inspired; no external dependency). Regenerate after editing component metas or tokens: `python3 knowledge/tokens/_build_blast_radius.py`. Authored canon stays the source of truth; this is a generated dashboard.

**Totals:** 137 components · 1043 tokens defined · 140 tokens referenced by components · compliance: 38 rules x 134 components (38 SCs).

## God-nodes — highest token blast radius

Change one of these and the listed number of components is affected. Use before any token rebind/rename (esp. the Sutherland migration).

| Token | Blast | Example components |
|---|---|---|
| `text/default` | 109 | Accordion, Account card, Alert, Amount display, Amount input, Anchor nav… |
| `background/default` | 74 | Accordion, Account selector, Amount display, Anchor nav, App shell — doormat (mega-footer) nav, App shell — focused / full-page… |
| `tertiary/background/default` | 51 | Account card, Action bar, Anchor nav, App shell — doormat (mega-footer) nav, App shell — focused / full-page, App shell — multi-column… |
| `icon/default` | 46 | Accordion, App shell — doormat (mega-footer) nav, App shell — focused / full-page, App shell — multi-column, App shell — nav rail, App shell — side nav… |
| `border-radius/surface` | 43 | Alert, Anchor nav, App shell — doormat (mega-footer) nav, App shell — focused / full-page, App shell — multi-column, App shell — nav rail… |
| `focus/ring` | 40 | Anchor nav, App shell — doormat (mega-footer) nav, App shell — focused / full-page, App shell — multi-column, App shell — nav rail, App shell — side nav… |
| `border/subtle` | 39 | Accordion, Account card, Action bar, Amount display, Avatar, Avatar group… |
| `text/secondary` | 37 | Account card, Amount display, Anchor nav, App shell — doormat (mega-footer) nav, App shell — focused / full-page, App shell — multi-column… |
| `divider/border/section` | 35 | Anchor nav, App shell — doormat (mega-footer) nav, App shell — focused / full-page, App shell — multi-column, App shell — nav rail, App shell — side nav… |
| `tertiary/background/hover` | 35 | Accordion, Anchor nav, App shell — doormat (mega-footer) nav, App shell — focused / full-page, App shell — multi-column, App shell — nav rail… |
| `border-radius/control` | 34 | Amount input, App shell — doormat (mega-footer) nav, App shell — focused / full-page, App shell — multi-column, App shell — nav rail, App shell — side nav… |
| `form/border/default` | 30 | Account card, Account selector, App shell — split, Cascader, Combobox, Command palette… |
| `elevation/functional` | 29 | Account selector, App shell — nav rail, Bar chart, Butterfly chart (horizontal), Butterfly chart (vertical), Card-header-lockup… |
| `rag/success` | 29 | Account card, Amount input, Bar chart, Button, Card-header-lockup, Confirmation… |
| `rag/error` | 27 | Amount input, Bar chart, Combobox, Date picker, Date-range picker, Dropdown… |

## Token-group reach (components using each group)

| Group | Components |
|---|---|
| `text/` | 114 |
| `background/` | 74 |
| `tertiary/` | 64 |
| `border-radius/` | 63 |
| `rag/` | 51 |
| `icon/` | 48 |
| `form/` | 44 |
| `border/` | 43 |
| `divider/` | 41 |
| `focus/` | 40 |
| `elevation/` | 29 |
| `primary/` | 21 |
| `target/` | 21 |
| `data/` | 19 |
| `typography/` | 13 |
| `secondary/` | 13 |
| `surface/` | 13 |
| `overlay/` | 10 |
| `scale/` | 7 |
| `padding/` | 7 |
| `color/` | 7 |
| `layout/` | 7 |
| `alpha/` | 7 |
| `progress/` | 6 |
| `table/` | 6 |
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

903 of 1043 defined tokens are unreferenced at the component layer. **Expected** for primitives and scale steps (consumed via semantic aliases, not bound directly); worth scanning the *semantic* groups for genuinely-dead tokens. By group:

| Group | Unreferenced |
|---|---|
| `color/` | 245 |
| `data-vis/` | 90 |
| `button/` | 63 |
| `rag/` | 61 |
| `data/` | 48 |
| `typography/` | 42 |
| `surface/` | 32 |
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
| `border/` | 6 |
| `breakpoint/` | 6 |
| `table/` | 6 |
| `tooltip/` | 6 |
| `size/` | 5 |
| `blur/` | 4 |
| `image/` | 4 |
| `layout/` | 4 |
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
