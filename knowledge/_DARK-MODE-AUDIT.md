# Dark-mode coverage audit

> Which components re-theme correctly in dark mode. **LEAK** = binds a raw colour *primitive* directly (single-valued, no dark variant — a real defect; the P3 family). *flat* = binds a semantic token whose dark value equals its light value (frequently intentional — reverse text, RAG, brand red — confirm per case). Derived view over the colour stores + blast-radius; regenerate: `python3 knowledge/_build_dark_mode_audit.py`. Detail in `_DARK-MODE-AUDIT.json`.

**Coverage:** 25/32 components clean · 7 leak a primitive. Store: 111 semantic colour tokens (light+dark), 43 flat (dark==light), 124 primitives.

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
| Avatar | ✅ clean | — | `icon/default-reverse`, `image/opacity/default`, `image/opacity/disabled`, `text/reverse` |
| Badge | 🔴 LEAK | `color/primary` | `text/reverse` |
| Breadcrumbs | ✅ clean | — | — |
| Button | ✅ clean | — | `icon/default-reverse`, `rag/success`, `tertiary/background/default`, `tertiary/background/disabled`, `text/reverse` |
| Cards | 🔴 LEAK | `color/primary` | `icon/default-reverse`, `tertiary/background/default`, `text/reverse` |
| Countdown timer | ✅ clean | — | — |
| Divider | ✅ clean | — | — |
| Dropdown | ✅ clean | — | `icon/default-reverse`, `rag/error`, `text/reverse` |
| Headers | ✅ clean | — | — |
| Hero | 🔴 LEAK | `color/grey/transparent/white-75`, `color/primary` | `icon/default-reverse`, `text/reverse` |
| Input fields | ✅ clean | — | `icon/default-reverse`, `rag/error`, `text/reverse` |
| Links | 🔴 LEAK | `color/primary` | `icon/default-reverse`, `text/reverse` |
| List items | 🔴 LEAK | `color/primary` | `icon/default-reverse`, `image/opacity/default`, `image/opacity/disabled`, `rag/success`, `tertiary/background/default`… |
| Loading indicator | ✅ clean | — | `icon/default-reverse`, `text/reverse` |
| Modals | ✅ clean | — | `icon/default-reverse`, `overlay/version1`, `text/reverse` |
| Navigations | 🔴 LEAK | `color/black`, `color/primary`, `color/white` | `overlay/version1` |
| Notifications | ✅ clean | — | `icon/default-reverse`, `rag/error`, `rag/information`, `rag/success`, `rag/text/on-dark`… |
| Pagination | ✅ clean | — | — |
| Progress tracker | ✅ clean | — | — |
| Quick actions | ✅ clean | — | — |
| Reorder | ✅ clean | — | `rag/success` |
| Search field | ✅ clean | — | `tertiary/background/default`, `text/reverse` |
| Selection controls | ✅ clean | — | `icon/default-reverse`, `rag/error`, `text/reverse` |
| Slider | ✅ clean | — | — |
| Status indicator | ✅ clean | — | `rag/error`, `rag/success`, `rag/warning` |
| Table | ✅ clean | — | — |
| Tabs | 🔴 LEAK | `color/primary` | `tertiary/background/default`, `text/reverse` |
| Tags | ✅ clean | — | `text/reverse` |
| Tooltip | ✅ clean | — | — |
| Video player | ✅ clean | — | `icon/default-reverse` |
| View options | ✅ clean | — | `icon/default-reverse`, `tertiary/background/default`, `tertiary/text/pressed` |

> *flat* tokens are not necessarily wrong — `icon/default-reverse`, `text/reverse`, `rag/*` and brand reds are designed to read the same on their fixed surfaces in both modes. They're listed so a reviewer can confirm none is an unthemed surface that *should* darken (e.g. check `tertiary/background/*`).
