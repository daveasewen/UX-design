# Handoff — Apollo mono · Tranche 7 (Navigation) + review tooling · 2026-07-16

**Read this + `_LIVE-STATE.md` to start cold.** Everything below is committed to disk in the repo;
Dave commits/pushes via **GitHub Desktop** (never Claude). Work happens in `/tmp/fix` (cloud), gated + rendered,
then written back via SendUserFile → device_commit_files.

## ⏭ FIRST TASK next session — build the unified switchable **Masthead** (spec at the bottom)
Then, in order of readiness: **Tranche 8** · the **type-token system** (blocked on Dave's Figma file).

---

## What shipped this session (all LIVE, all four gates green)

**Tranche 6 — Text entry & forms**: built + review-fixed with Dave (border-as-state-channel; uniform 51px field
height every state; real error triangle; no size/layout jumps). LIVE.

**Tranche 7 — Navigation**: built, then **aligned to the CDC HSBC Figma frames** (`CDC_Navigation_UI_Patterns`,
file key `wlvhMFXSoDAmehMjdbzRil`; node `216:5182` top-nav bar, `216:5505` content-heavy mega). One file:
`knowledge/_proforma/Tranche-7-interactive.html`. Sections: Popover/NavToggle · Global header · Side nav ·
Mega menu (cols / featured-content-heavy / tabbed-vertical / **tabbed-horizontal**) · Drawer + NavAccordion.
Fixes applied this session (via the review tool, in batches):
- **Global header**: active underbar sits on the container's **bottom edge**, contents vertically centred;
  **in-header search** revealed from the search icon (+ **clear icon**, CSS-shown only when there's text);
  **bottom-only border**; fixed the odd icon sizing (root cause: `.ib.navtoggle` inherited the text-toggle's
  side padding → glyph squashed 20→10px; fix = `.ib.navtoggle{padding:0}`); account glyph swapped `i-avatar`→`i-user`;
  priority+ breakpoints raised to **760 / 600** so links never overflow into the utility icons.
- **Side nav**: rows now match the **hamburger drawer** (borderless full-width rows, left-aligned labels, no button
  border; same open styling for both); collapsing to the **rail also collapses open submenus** (no overflow).
- **Burger drawer** content = **same as the Side nav** (Overview · Statements · Payments · Support).
- **Mega menu**: reveal is now **pure CSS** (grid `0fr→1fr` on `.megamenu`, clipping a block `.mm-clip` wrapper so
  it collapses fully to 0 — the old version left a 41px min-content sliver = the "jump"); **no underlines** on any
  nav links (hover keeps the surface tint); **content-heavy** featured variant with the divided **Journeys** icon-rail;
  new **horizontal-tabs** variant (multi-column panels that wrap responsively); headings **de-capitalised**
  (all-caps rule — removed `text-transform:uppercase` from `.menugroup-h` and `.grouplbl`); **masthead bottom-border-only**.
- Mono translation confirmed everywhere: red active indicator → **2px ink underbar** (mode-governed; red returns
  automatically in Apollo UI / SC).

**Review-comment tool (NEW, reusable spin-off)** — `knowledge/_review/`:
- `_review-overlay.html` = self-contained comment layer (toggle Review mode → click a component to pin an in-memory
  comment → panel to manage → **Export** a numbered edit-prompt with section + selector; copy/download). No browser
  storage (export is the save). `rv-`-prefixed, isolated from the host page & the gates.
- `_make_review.py` = injector: `python3 knowledge/_review/_make_review.py <tranche.html>` → writes
  `knowledge/_review/<stem>-REVIEW.html` (kept OUT of `_proforma/` so the component gates never scan it).
- This is how Dave now feeds edits: he marks up the REVIEW copy and pastes the exported prompt back. Worked great —
  three review rounds this session came in this way. Regenerate the REVIEW copy after each batch of edits.

## Files & workflow
- Component: `knowledge/_proforma/Tranche-7-interactive.html` (icon-manifest sprite; 44+ real icons).
- Gates (run from `knowledge/`): `_proforma/_check_proforma.py <file>` (single-file) · `_validate_proforma.py`
  (universal) · `_validate_css_governed.py` (**DEF-003**, no JS-driven motion) · `_validate_no_hardcode.py`
  (**DEF-004**, no raw px in spacing/border-stroke/radius). All four must be green; wired into `_build_all.py`.
- Verify visually with playwright chromium at `/opt/pw-browsers/chromium` (device_scale_factor 2). Measure computed
  styles for animation-immune checks. Drive responsive via `document.getElementById('frame').style.setProperty('--fw', …)`.
- Bridge is **flaky** — the `mcp__remote-devices__*` write tools can drop mid-session (get_device_info stays up).
  If GitHub Desktop throws "a lock file already exists", `mv` `.git/index.lock` into `_to_delete/` (bridge blocks unlink).

## Rules to hold (non-negotiable)
- **Apollo mono**: monochrome, near-black `#1A1A1A`, colour = MEANING only (RAG), square corners. One skeleton, N token modes.
- **Tokenise everything** (DEF-004) so a MODE can override it; geometry/dimensions are a separate axis (not gated).
- **JS minimum — CSS is the default** (Dave, reaffirmed 2026-07-16). Motion is CSS-only (DEF-003); JS only for genuine
  behaviour (disclosure open/close, focus mgmt, keyboard, tab selection). Never animate styles in JS.
- **No ALL-CAPS** (`text-transform:uppercase` banned); labels sentence case.
- **Never invent icons** — real assets under `knowledge/assets/icons/` + declare every `<symbol>` in `#icon-manifest`.
- **Reuse calibration = collaborative**: ASK Dave what he values before deciding mine-vs-fresh; verify facts, ask on taste.
- **Comms**: Dave is dyslexic + time-poor → exec-summary first + numbered next-steps; provide paste-ready commit lines.
- **Mode-2 routing** default-on (delegate mechanical work to cheaper models, announce) — but precise visual-matching /
  design-judgment work stays on the main model.

---

## 🎯 #4 SPEC — Unified switchable **Masthead** (build first)

**Insight (Dave, 2026-07-16):** the **Global header** (exposed L1 + utility) and the **content-heavy masthead**
(brand + hamburger → mega) are **not two components — they're one masthead pattern with different switches.** Build a
single parameterised `.masthead` organism plus a **control row of switches** that reconfigures one live instance across
use-cases, and **dedupe**: fold the current separate `Global header` and mega-`.mm-masthead` demos into it.

**Parameters (the "logical set" Dave asked for):**
- **Nav reveal mode**: `exposed` (L1 links inline — CDC Frame 1) · `mega` (a trigger opens a mega panel — CDC Frame 2,
  incl. the **exposed-header-that-invokes-a-mega** variation Dave specifically wants) · `minimal` (brand + utility only).
- **Utility toggles**: search on/off · account on/off.
- **Responsive collapse** (priority+ → hamburger drawer) stays automatic underneath, as now.

**Requirements:**
- Mono tokens throughout; **CSS-only motion** (reuse the fixed `grid`/`.mm-clip` mega reveal); real icons.
- a11y: disclosure pattern (`aria-expanded`/`aria-controls`), `aria-current="page"` + ink underbar for current,
  Esc-close+return-focus, modal drawer traps focus.
- The switch UI = a small segmented/toggle control row (behaviour JS fine; **no motion JS**). Consider a `data-mode`
  attribute on `.masthead` driving CSS for the mode, so switching is mostly declarative.
- Keep the active indicator mono (ink underbar); red is a mode concern, not baked in.
- All four gates green; render-verify each mode + the responsive collapse.

**Nice-to-have:** expose the same parameters as the eventual component API (this is a strong "one component, many
use-cases" proof for the pro-forma factory story).

---

## Backlog (after the masthead)
- **Type-token system** — BLOCKED on Dave's Figma file. 3 responsive scales × 9 sizes each + line-heights, 4px-grid
  aligned → distilled into **2 labelling-style sets** (multiline/editorial + UI). Same Figma file carries **new colour
  tokens for all 3 modes**. On arrival: restore placeholder **leading-trim** (also fixes the off-grid 51px field height →
  on-grid) and apply type tokens across the pro-forma. See memory `type-system-tokens`.
- **Tranche 8**: BottomTabBar + More · InPageNav / scroll-spy · FooterNav · RelatedLinks/Cards · Journey **Stepper**.
- **Legacy libraries** build-out (noted, later).
- Smaller ideas: asset/icon **metadata + catalog** (`_icon-index.json` + gallery) · git **post-commit staleness hook** ·
  extend DEF-003 to scan snippets · **glyph-geometry** icon gate (compare drawn glyph to the asset, not just filename) ·
  promote the review tool to a **skill**.

## Memory / ledger pointers
`proforma-programme` · `apollo-mono` · `nav-pattern-catalog` · `cdc-nav-alignment` · `type-system-tokens` ·
`review-preview-html` · `feedback-reuse-calibration` · `git-push-method` · `_LIVE-STATE.md` (root).
