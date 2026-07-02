# Dark-mode coverage audit

> Which components re-theme correctly in dark mode. **LEAK** = binds a raw colour *primitive* directly (single-valued, no dark variant — a real defect; the P3 family). *flat* = binds a semantic token whose dark value equals its light value (frequently intentional — reverse text, RAG, brand red — confirm per case). Derived view over the colour stores + blast-radius; regenerate: `python3 knowledge/_build_dark_mode_audit.py`. Detail in `_DARK-MODE-AUDIT.json`.

**Coverage:** 31/38 components clean · 7 leak a primitive. Store: 116 semantic colour tokens (light+dark), 42 flat (dark==light), 124 primitives.

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
| Account card | ✅ clean | — | `rag/success`, `rag/warning` |
| Action bar | ✅ clean | — | `primary/background/default`, `primary/background/hover`, `text/reverse` |
| Avatar | ✅ clean | — | `icon/default-reverse`, `image/opacity/default`, `image/opacity/disabled`, `text/reverse` |
| Badge | 🔴 LEAK | `color/primary` | `primary/background/default`, `text/reverse` |
| Breadcrumbs | ✅ clean | — | — |
| Button | ✅ clean | — | `icon/default-reverse`, `primary/background/default`, `primary/background/hover`, `rag/success`, `text/reverse` |
| Cards | 🔴 LEAK | `color/primary` | `icon/default-reverse`, `text/reverse` |
| Confirmation | ✅ clean | — | `primary/background/default`, `primary/background/hover`, `rag/success`, `text/reverse` |
| Countdown timer | ✅ clean | — | — |
| Divider | ✅ clean | — | — |
| Dropdown | ✅ clean | — | `form/background/default`, `icon/default-reverse`, `text/reverse` |
| Eyebrow | ✅ clean | — | — |
| Headers | ✅ clean | — | — |
| Hero | 🔴 LEAK | `color/grey/transparent/white-75`, `color/primary` | `icon/default-reverse`, `primary/background/default`, `text/reverse` |
| Input fields | ✅ clean | — | `form/background/default`, `icon/default-reverse`, `text/reverse` |
| Links | 🔴 LEAK | `color/primary` | `icon/default-reverse`, `primary/background/default`, `text/reverse` |
| List items | 🔴 LEAK | `color/primary` | `icon/default-reverse`, `image/opacity/default`, `image/opacity/disabled`, `rag/success`, `text/reverse` |
| Loading indicator | ✅ clean | — | `icon/default-reverse`, `text/reverse` |
| Modals | ✅ clean | — | `icon/default-reverse`, `overlay/version1`, `primary/background/default`, `text/reverse` |
| Navigations | 🔴 LEAK | `color/black`, `color/primary`, `color/white` | `overlay/version1`, `primary/border/default` |
| Notifications | ✅ clean | — | `icon/default-reverse`, `rag/success`, `rag/text/on-dark`, `rag/text/on-light`, `rag/warning` |
| Pagination | ✅ clean | — | `form/background/default` |
| Progress tracker | ✅ clean | — | `progress/complete` |
| Quick actions | ✅ clean | — | — |
| Reorder | ✅ clean | — | `rag/success` |
| Search field | ✅ clean | — | `form/background/default`, `text/reverse` |
| Selection controls | ✅ clean | — | `form/background/default`, `icon/default-reverse`, `text/reverse` |
| Slider | ✅ clean | — | — |
| Status indicator | ✅ clean | — | `rag/success`, `rag/warning` |
| Summary | ✅ clean | — | — |
| Tab-bar | ✅ clean | — | — |
| Table | ✅ clean | — | — |
| Tabs | 🔴 LEAK | `color/primary` | `tabs/active`, `text/reverse` |
| Tags | ✅ clean | — | `text/reverse` |
| Tooltip | ✅ clean | — | — |
| Video player | ✅ clean | — | `icon/default-reverse`, `overlay/version2`, `primary/background/default` |
| View options | ✅ clean | — | `icon/default-reverse`, `tertiary/text/pressed` |

> *flat* tokens are not necessarily wrong — `icon/default-reverse`, `text/reverse`, `rag/*` and brand reds are designed to read the same on their fixed surfaces in both modes. They're listed so a reviewer can confirm none is an unthemed surface that *should* darken (e.g. check `tertiary/background/*`).
