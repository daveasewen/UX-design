# Handoff — component-by-component interaction review (next session)

**Title this chat: "Component interaction review — gallery one-by-one"**

Fresh chat to avoid context rot. All state is in memory + the files below.
**Read first:** `MEMORY.md` → [[gallery-and-gap-pattern-frontier]] → [[composition-layer-canon-css]], then this.

---

## Where we are (exec summary)

The canon composition layer is built and every automated gate is green. The thing left is the
**visual / interaction layer the gates can't judge** — Dave is reviewing the **canon gallery** and seeing:

- some **interaction decisions missing** (motion / state behaviour not carried into a component),
- some components **incomplete or missing**,
- some that just need **finesse** (polish).

The plan is to **go through the gallery component-by-component**, fix each, re-render, re-gate.

## Next steps

1. Open the gallery: `knowledge/_fitness-test/canon-gallery.canon.html` (every reviewed component, light/dark
   toggle, interactive ones shown in a representative state). Go component-by-component **with Dave driving** —
   he points at the issue, we fix the **snippet** (source of truth), regenerate, re-render, re-gate.
2. For each fix: edit `snippets/<Name>.reference.html` → `python3 knowledge/canon/gen_canon_components.py`
   → render via the chromium setup → `python3 knowledge/_validate_screen.py --render`.
3. After the review: **build the 5 remaining gap-patterns** as gated components (Dave chose all 5) following the
   **account-card** template: summary (key/value), tab-bar (bottom nav), action-bar, eyebrow, confirmation/success.
4. Keep the journey + gallery passing the gate after every change.

---

## What's built (the durable assets)

- **`knowledge/canon/canon.css`** — the single composition layer. 3 parts:
  generated token spine (`canon/gen_canon_tokens.py` from `tokens/*.json`) + hand alias/utility/journey-pattern
  layer + AUTO-COMPONENTS (`canon/gen_canon_components.py`, **33** `.cn-*` components generated VERBATIM from the
  snippets incl. ~196 decision comments). Never hand-edit the AUTO blocks — edit the snippet + regenerate.
- **Generators** (idempotent, in `knowledge/canon/`): `gen_canon_tokens.py`, `gen_canon_components.py`
  (now globs snippets → auto-picks new ones). `knowledge/gen_gallery.py` builds the gallery.
- **Gates** (verification = enforcement):
  - `knowledge/_validate_screen.py [--render]` — runs a composed screen through the WHOLE pipeline
    (compose + icon-source + a11y + rendered state-contrast). **Use this on every screen/gallery change.**
  - `knowledge/_validate_compose.py` — quick structural-only check.
  - snippet-level: `_validate_snippets.py` (token fidelity/ARIA/contrast/focus), `_validate_icons.py`
    (HARD gate, library-icon byte-match), `_validate_a11y.py`, `_validate_state_contrast.py` (rendered hover/
    pressed), `_validate_coverage.py` (meta↔snippet), `_validate_dark_surfaces.py`.
- **Composed screens** in `knowledge/_fitness-test/`: `payments-journey.canon.html` (4 screens, audited +
  gate-passing), `canon-gallery.canon.html` (all 32 + the interactive-shown fix).
- **account-card** = first promoted gap-pattern: `snippets/Account-card.reference.html` +
  `components/account-card.meta.json` (draft, REVIEW-flagged). Journey uses `.cn-account-card`.

## How to render (CRITICAL — visual review needs this)

Chromium works in the sandbox with the libXdamage workaround (download is otherwise blocked):
```
# one-time: fetch the missing lib
cd /sessions/.../mnt/outputs && mkdir -p libs && cd libs
apt-get download libxdamage1 && dpkg-deb -x libxdamage1*.deb x && cp x/usr/lib/*/libXdamage.so.1* .
# then for every render:
export PLAYWRIGHT_SKIP_VALIDATE_HOST_REQUIREMENTS=1
export LD_LIBRARY_PATH="/sessions/.../mnt/outputs/libs:$LD_LIBRARY_PATH"
```
**Always render + look** — every issue this session (contrast, dark-mode, radio, icons) was visual and passed
the static gates. Don't trust green gates alone for visual correctness.

## The review task — what to look for, per component

- **Missing interaction decisions**: did the component carry its motion / hover / pressed / focus / open-close
  behaviour, or just the static look? (e.g. scale-physics on buttons, the tab indicator slide, accordion expand.)
- **Incomplete / missing**: states or variants not present; a sub-part dropped in composition.
- **Finesse**: spacing, hierarchy, proportions, colour nuance — the design-quality layer.
- Method: fix the **snippet** (it's the gated source of truth, regenerates into canon), not canon.css directly.

## Queued after the review — 5 gap-patterns → gated components

Follow the account-card pattern exactly: `snippets/<Name>.reference.html` (theme blocks with token-matched
values, `#token-manifest`, full states, reduced-motion, library icons via `<use>`) + `components/<name>.meta.json`
(REVIEW-flag the design calls) → gates → regenerate → swap the journey's `c-*` for the new `.cn-*` → gate.
Components: **summary, tab-bar, action-bar, eyebrow, confirmation/success**. (account-card already done.)

## Don't redo

All 32 snippets pass the gates as-is (treat them as correct unless the review finds otherwise). canon.css token
spine + component layer are generated and idempotent. The journey is audited + faithful. The gallery is generated.
