# Dark-mode coverage audit

> Which components re-theme correctly in dark mode. **LEAK** = binds a raw colour *primitive* directly (single-valued, no dark variant — a real defect; the P3 family). *flat* = binds a semantic token whose dark value equals its light value (frequently intentional — reverse text, RAG, brand red — confirm per case). Derived view over the colour stores + blast-radius; regenerate: `python3 knowledge/_build_dark_mode_audit.py`. Detail in `_DARK-MODE-AUDIT.json`.

**Coverage:** 122/129 components clean · 7 leak a primitive. Store: 198 semantic colour tokens (light+dark), 68 flat (dark==light), 229 primitives.

## Primitive leaks — fix before dark mode

Each raw primitive bound directly, and the components binding it. Rebind to a semantic token that carries a dark value (see `_DESIGN-SYSTEM-GAPS.md` / `_REVIEW-QUEUE.md` token-rebind section).

| Primitive | Components | Note |
|---|---|---|
| `color/primary` | Badge, Cards, Hero, Links, List items, Navigations, Tabs | brand red #db0011 — for Tabs the indicator should be a semantic tabs/active (P3); for links/badges confirm dark-mode brand red |
| `color/grey/transparent/white-75` | Hero |  |
| `color/black` | Navigations |  |
| `color/white` | Navigations |  |

## Per-component

| Component | Status | Primitive leaks | Flat semantics (confirm) |
|---|---|---|---|
| Accordion | ✅ clean | — | — |
| Account card | ✅ clean | — | `form/border/default`, `rag/success`, `rag/warning` |
| Account selector | ✅ clean | — | `form/border/default` |
| Action bar | ✅ clean | — | `primary/background/default`, `primary/background/hover`, `text/reverse` |
| Alert | ✅ clean | — | — |
| Amount display | ✅ clean | — | — |
| Amount input | ✅ clean | — | `rag/error`, `rag/success` |
| Anchor nav | ✅ clean | — | `primary/border/default` |
| App shell — doormat (mega-footer) nav | ✅ clean | — | `overlay/version1`, `primary/border/default` |
| App shell — focused / full-page | ✅ clean | — | `primary/border/default` |
| App shell — multi-column | ✅ clean | — | `primary/border/default` |
| App shell — nav rail | ✅ clean | — | `primary/border/default` |
| App shell — side nav | ✅ clean | — | `overlay/version1`, `primary/border/default` |
| App shell — split | ✅ clean | — | `form/border/default`, `overlay/version1`, `primary/border/default` |
| App shell — top / stacked nav | ✅ clean | — | `overlay/version1`, `primary/border/default` |
| Avatar | ✅ clean | — | `icon/default-reverse`, `image/opacity/default`, `image/opacity/disabled`, `text/reverse` |
| Avatar group | ✅ clean | — | — |
| Badge | 🔴 LEAK | `color/primary` | `primary/background/default`, `text/reverse` |
| Banner | ✅ clean | — | `rag/text/on-dark`, `rag/text/on-information`, `rag/text/on-light`, `text/on-success` |
| Bar chart | ✅ clean | — | `data/series/1`, `data/series/3`, `rag/error`, `rag/information`, `rag/success`… |
| Box plot | ✅ clean | — | `data/series/1` |
| Breadcrumbs | ✅ clean | — | — |
| Bullet chart | ✅ clean | — | `data/series/1` |
| Butterfly chart (horizontal) | ✅ clean | — | `data/series/1`, `data/series/3` |
| Butterfly chart (vertical) | ✅ clean | — | `data/series/1`, `data/series/3` |
| Button | ✅ clean | — | `icon/default-reverse`, `primary/background/default`, `primary/background/hover`, `rag/success`, `text/reverse` |
| CTA-lockup | ✅ clean | — | — |
| Calendar | ✅ clean | — | — |
| Candlestick chart | ✅ clean | — | — |
| Card-header-lockup | ✅ clean | — | `rag/success` |
| Cards | 🔴 LEAK | `color/primary` | `icon/default-reverse`, `text/reverse` |
| Carousel | ✅ clean | — | `text/reverse` |
| Cascader | ✅ clean | — | `form/background/default`, `form/border/default` |
| Combo chart | ✅ clean | — | `data/series/1`, `data/series/2` |
| Combobox | ✅ clean | — | `form/background/default`, `form/border/default`, `rag/error` |
| Command palette | ✅ clean | — | `form/border/default`, `overlay/version1` |
| Confirmation | ✅ clean | — | `primary/background/default`, `primary/background/hover`, `rag/success`, `text/reverse` |
| Countdown timer | ✅ clean | — | — |
| Coverage / runway bar | ✅ clean | — | `rag/success`, `rag/warning` |
| Data grid | ✅ clean | — | `form/border/default`, `text/reverse` |
| Date picker | ✅ clean | — | `rag/error` |
| Date-range picker | ✅ clean | — | `rag/error` |
| Divider | ✅ clean | — | — |
| Document row | ✅ clean | — | — |
| Donut chart | ✅ clean | — | `data/series/1` |
| Drawer | ✅ clean | — | `overlay/version1` |
| Dropdown | ✅ clean | — | `form/background/default`, `form/border/default`, `icon/default-reverse`, `rag/error`, `text/reverse` |
| Empty state | ✅ clean | — | — |
| Eyebrow | ✅ clean | — | — |
| FAB | ✅ clean | — | — |
| Feature-grid-lockup | ✅ clean | — | — |
| File upload | ✅ clean | — | `form/border/default`, `rag/error`, `rag/success` |
| Filter-toolbar-bar | ✅ clean | — | `form/border/default` |
| Footer | ✅ clean | — | — |
| Form layout | ✅ clean | — | `rag/error`, `rag/success` |
| Grid / stack utilities | ✅ clean | — | — |
| Headers | ✅ clean | — | — |
| Hero | 🔴 LEAK | `color/grey/transparent/white-75`, `color/primary` | `icon/default-reverse`, `primary/background/default`, `text/reverse` |
| Histogram | ✅ clean | — | `data/series/1` |
| Icon button | ✅ clean | — | `icon/default-reverse` |
| Image block | ✅ clean | — | `form/border/default` |
| Input fields | ✅ clean | — | `form/background/default`, `form/border/default`, `icon/default-reverse`, `rag/error`, `text/reverse` |
| KPI tile | ✅ clean | — | `rag/error`, `rag/success` |
| Line chart | ✅ clean | — | `data/series/1` |
| Links | 🔴 LEAK | `color/primary` | `icon/default-reverse`, `primary/background/default`, `text/reverse` |
| List items | 🔴 LEAK | `color/primary` | `icon/default-reverse`, `image/opacity/default`, `image/opacity/disabled`, `rag/success`, `text/reverse` |
| Loading indicator | ✅ clean | — | `icon/default-reverse`, `text/reverse` |
| Meter | ✅ clean | — | `rag/success`, `rag/warning` |
| Modal lightbox | ✅ clean | — | `overlay/version1` |
| Modals | ✅ clean | — | `icon/default-reverse`, `overlay/version1`, `primary/background/default`, `text/reverse` |
| Multi-select | ✅ clean | — | `form/background/default`, `form/border/default`, `rag/error` |
| Navigations | 🔴 LEAK | `color/black`, `color/primary`, `color/white` | `overlay/version1`, `primary/border/default` |
| Notifications | ✅ clean | — | `icon/default-reverse`, `rag/error`, `rag/information`, `rag/success`, `rag/text/on-dark`… |
| Page-header-lockup | ✅ clean | — | `badge/background`, `rag/text/on-light` |
| Pagination | ✅ clean | — | `form/background/default` |
| Payment card visual | ✅ clean | — | `form/border/default`, `rag/success`, `rag/warning` |
| Pie chart | ✅ clean | — | `data/series/1` |
| Popconfirm | ✅ clean | — | — |
| Popover | ✅ clean | — | — |
| Progress tracker | ✅ clean | — | `rag/success`, `step/complete`, `step/on-complete` |
| QR code | ✅ clean | — | `surface/digital-black`, `text/reverse` |
| Quick actions | ✅ clean | — | — |
| Range slider | ✅ clean | — | `form/border/default` |
| Rating | ✅ clean | — | `form/border/default` |
| Reorder | ✅ clean | — | `rag/success` |
| Scatter plot | ✅ clean | — | `data/series/1` |
| Search field | ✅ clean | — | `form/background/default`, `form/border/default`, `text/reverse` |
| Section-heading-lockup | ✅ clean | — | `badge/background`, `primary/background/default`, `rag/text/on-light` |
| Secure entry | ✅ clean | — | `rag/error`, `rag/success` |
| Segmented control | ✅ clean | — | `form/border/default` |
| Selection controls | ✅ clean | — | `form/background/default`, `form/border/default`, `icon/default-reverse`, `rag/error`, `text/reverse` |
| Sidebar nav | ✅ clean | — | `primary/border/default` |
| Skeleton loader | ✅ clean | — | — |
| Slider | ✅ clean | — | `form/border/default` |
| Sparkline | ✅ clean | — | `data/series/1` |
| Splitter | ✅ clean | — | `form/border/default` |
| Stacked area chart | ✅ clean | — | `data/series/1`, `data/text/on-series` |
| Standing-order / mandate row | ✅ clean | — | `rag/information`, `rag/success`, `rag/warning` |
| Stat card | ✅ clean | — | `rag/error`, `rag/success` |
| Stats-band-lockup | ✅ clean | — | `primary/background/default` |
| Status indicator | ✅ clean | — | `rag/error`, `rag/success`, `rag/warning` |
| Stepper | ✅ clean | — | `rag/error`, `rag/success`, `step/complete`, `step/on-complete` |
| Summary | ✅ clean | — | — |
| Tab-bar | ✅ clean | — | — |
| Table | ✅ clean | — | — |
| Tabs | 🔴 LEAK | `color/primary` | `text/reverse` |
| Tags | ✅ clean | — | `form/border/default`, `text/reverse` |
| Tags input | ✅ clean | — | `form/background/default`, `form/border/default`, `rag/error` |
| Template confirmation | ✅ clean | — | `rag/success`, `rag/warning` |
| Template dashboard | ✅ clean | — | `data/series/1`, `form/border/default`, `rag/error`, `rag/information`, `rag/success`… |
| Template detail | ✅ clean | — | `rag/information`, `rag/success`, `rag/warning` |
| Template empty | ✅ clean | — | `form/border/default` |
| Template error | ✅ clean | — | — |
| Template list index | ✅ clean | — | `form/border/default`, `rag/error`, `rag/warning` |
| Template report | ✅ clean | — | `data/series/1` |
| Template settings | ✅ clean | — | `rag/error`, `rag/information` |
| Template — auth (log on / register / OTP) | ✅ clean | — | `rag/error`, `rag/success` |
| Template — create / edit form | ✅ clean | — | `rag/error`, `rag/success` |
| Template — multi-step wizard | ✅ clean | — | `rag/error`, `rag/success`, `step/complete`, `step/on-complete` |
| Textarea | ✅ clean | — | `rag/error` |
| Time picker | ✅ clean | — | `rag/error` |
| Timeline | ✅ clean | — | `form/border/default`, `rag/error`, `rag/information`, `rag/success`, `rag/warning` |
| Toast | ✅ clean | — | — |
| Tooltip | ✅ clean | — | — |
| Transaction / ledger row | ✅ clean | — | `rag/information`, `rag/success`, `rag/warning` |
| Transfer list | ✅ clean | — | `form/border/default` |
| Tree | ✅ clean | — | — |
| Video player | ✅ clean | — | `icon/default-reverse`, `overlay/version2`, `primary/background/default` |
| View options | ✅ clean | — | `form/border/default`, `icon/default-reverse`, `tertiary/text/pressed` |

> *flat* tokens are not necessarily wrong — `icon/default-reverse`, `text/reverse`, `rag/*` and brand reds are designed to read the same on their fixed surfaces in both modes. They're listed so a reviewer can confirm none is an unthemed surface that *should* darken (e.g. check `tertiary/background/*`).
