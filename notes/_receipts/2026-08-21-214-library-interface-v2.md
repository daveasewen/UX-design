# Receipt — the component library gets an interface (#214, LANE L)

**Session:** #214 · **Date:** 2026-08-21 · **Author:** Opus build sub
**Status:** ⛔ PROPOSED, NOT RULED. No commit, no ruling, no store/GM/LS/chain edit.
**Dave's ask, verbatim:** *"On the library file I'd like to improve the interface, I'd like the
controls to be in the true header and the component pages don't need the review overlay, its just
clutter. Can I have a search at the top of the menu. Type filters, atom, molecule, organism,
lock-up, shell, template etc... And any other finding mechanism that might be appropriate. All the
components must be interactively working. i need to see how the side menu behaves for instance."*

---

## What "the library file" was — and which one this is

Three candidates existed. Named, so the pick is checkable:

| Candidate | What it is | Verdict |
|---|---|---|
| **`showroom/index.html`** | The generated, browsable component library, RULED by Dave 2026-07-21, written by `knowledge/gen_showroom.py`. 135 components, category tree, no controls of its own. | **THIS ONE.** Newest, ruled, and the only one that browses the whole library. |
| `reviews/REVIEW-213-wave-components-four-theme-v1.html` | A REVIEW surface over 43 wave-3–6 components, with its own question prose + decision controls. | Not the library. **Untouched**, as briefed. |
| `reviews/ITINERARY-*-v3.html` | A build-status ledger, not a browser. | Not the library. |

v1 stays exactly where it is: **`showroom/index.html` is not modified by this lane** (byte-identical
after regeneration — verified, 0 writes to it in every `gen_showroom.py` run below). The new
interface is a **new versioned artefact** beside it (ADR-0017).

## What was built

| Artefact | Kind |
|---|---|
| `knowledge/_render/gen_library_214.py` | **NEW generator** (the deliverable — ds-018: the fix lands in the generator) |
| `reviews/LIBRARY-2026-08-21-v2.html` | its output: the v2 library browser, 135 components |
| `knowledge/gen_showroom.py` | **EXTENDED**: `#chrome=0` embed mode (below). 135 showroom pages regenerated |
| `reviews/outputs/library-v2-1500.png`, `…-820.png` | render evidence, wide + narrow |

## Dave's five asks, and where each one landed

1. **Controls in the TRUE header.** v1 carried a title and a count only; every control lived on the
   embedded component page's own bar — two stacked bars, and none of them the library's. v2 owns
   **theme (4) · light/dark · width · Replay · Open ↗** in one page header, plus a live "what you
   are looking at" name. The pane's own bar is hidden.
2. **No review overlay on component pages.** New embed mode in `gen_showroom.py`: a component page
   opened with `#chrome=0` hides its own bar **and cuts the review-overlay block out of the payload
   before srcdoc** (the payload is split at `<!-- APOLLO-REVIEW-OVERLAY -->`, which is the last
   thing injected, so nothing else is lost). Drive-tested: `#rv-fab` count in the pane = **0**.
   ⚠ **Opt-OUT, not deleted** — `REVIEW-213` iframes the same pages and wants its comment pins.
   Swap point if Dave rules the overlay gone everywhere: `gen_showroom.py` `initFromHash`, flip to
   `h.chrome!=='1'` (one line), then REVIEW-213's generator must pass `chrome=1`.
3. **Search at the top of the menu.** Substring over **name + slug + purpose prose + aliases**, at
   the top of the sidebar, sticky. `/` or `⌘K` focuses it, `Esc` clears, `Enter` opens the first
   hit. Each row shows *why* it matched when the match was indirect (`"spinner"`, `in purpose`).
4. **Type filters.** Multi-select facet chips over the levels, each with its live count, plus a
   second facet — **Ships behaviour** (89 of 135) — and a live `n of 135 shown` + Clear all.
5. **Interactive components.** Every pane is an `<iframe>` at the component's **own generated
   showroom page**, which srcdoc-mounts the gated reference snippet verbatim. Nothing is re-drawn
   ([[specimen-starts-from-reference]]); scripts run.

**Other finding mechanisms** (research doc §c, in rank order): aliases ✅ · facet chips ✅ ·
category tree ✅ · recently-opened ✅ · deep links (`#c=slug&theme=…&m=…`) ✅ · result counts ✅.
**Not built:** thumbnail grid (§c.6, the highest-value one left — needs a screenshot pipeline per
component), status/release-phase facet (§c.5 — needs a ruled status vocabulary), related-components
cross-links (§c.7 — `relationships` exists in every meta.json, so this is cheap next).

## ⚠ The level word-set is UNPICKED — where the swap point is

Dave has not chosen (three candidates: research doc §d). **One config array is the whole surface:**

```python
# knowledge/_render/gen_library_214.py
LEVELS = [{"key":"atom","label":"Atom"}, … {"key":"template","label":"Template"}]
```

`key` is derived and never shown; `label` is the only thing on the face of the page. Both
alternative word-sets are written in a comment beside it. Swap the labels, regenerate, done — no
other line in the generator names a level word. **This lane rules nothing about the names.**

**Derivation is MECHANICAL, never hand-tagged** (`level_of()`), and it covers **135 of 135** —
zero unfiled, zero missing meta:

| Source | Rule | n |
|---|---|---|
| `meta.json` `$layer: "2 Shell"` | shell | 7 |
| `$layer: "2 Template"` | template | 11 |
| `$layer: "2 Lock-up"` | lock-up | 9 |
| `meta.json` `category` | atom / molecule / organism | 18 / 57 / 33 |
| slug shape (`app-shell-*`, `template-*`, `*-lockup`) | fallback only | 0 used |
| nothing matched | **"Unfiled"** — a gap shows as a gap | 0 |

*(The itinerary snapshot `reviews/ITINERARY-STATUS-2026-08-21-v3.json` carries the same Layer-2
split in its `layer` field and agrees row-for-row with the meta files on all 27 Layer-2 artefacts;
the meta files are used because they cover the Layer-1 split too, which the itinerary does not.)*

## The alias table

68 aliases → 68 real slugs, **every target asserted to exist by the selftest** (bite 1: a dead alias
fails the build). Seeded from the components actually present. A sample:
`select|picker → dropdown` · `spinner|loader|throbber → loading-indicator` ·
`snackbar|flash → toast` · `dialog|modal → modals` · `sheet|off-canvas|side panel → drawer` ·
`checkbox|radio|toggle|switch → selection-controls` · `typeahead|autocomplete → combobox` ·
`datagrid → data-grid` · `datatable|grid → table` · `hamburger|side menu|nav drawer → sidebar-nav` ·
`omnibox|cmd-k|quick open → command-palette` · `facepile|avatar stack → avatar-group` ·
`shuttle|dual list → transfer-list` · `otp|pin|password → secure-entry` · `gauge → meter` ·
`speed dial → fab` · `metric → stat-card` · `kpi → kpi-tile`.

## Evidence — DRIVEN, not asserted (headless chromium, file://, 2026-08-21)

`24 of 25` checks passed. The one failure is a finding about a **component**, not the library.

* **Search** — substring narrows (135→1); `dropdown` resolves to Dropdown; `spinner` resolves to
  **exactly** `loading-indicator` and the row shows the alias that matched; clear restores 135.
* **Facets** — Shell → 7; Shell+Template → 18 (multi-select); Clear all → 135; behaviour facet is
  a real subset (89).
* **Embed mode** — pane's own `<header>` **not visible**; `body.embed` present; **`#rv-fab` = 0**
  (the review overlay is gone); component body mounted.
* **PER THEME** — `mono · legacy · console · supercharge` each read back off the pane's
  `html[data-apollo-theme]` after a header click; `body[data-theme]` reads `dark` after Dark.
  The mechanism is fragment assignment on `iframe.src` — same document, **no reload**, the same
  broadcast REVIEW-213 uses.
* **Live behaviour** — App-shell-side-nav's rail toggle flips `aria-expanded` on click; Tabs
  switches the selected tab on click. **No uncaught page errors.**
* Renders at 1500px and 820px (responsive stack) attached in `reviews/outputs/`.
* `node --check` on both inline scripts (library page, showroom page) — clean.

**Gate verdicts:** `gen_showroom.py --check` **OK** (135 pages + index in sync) ·
`gen_showroom.py --selftest` **OK, 16 bites** (5 new, pinning the embed contract, including one
that fails if the overlay ever becomes opt-IN and silently breaks REVIEW-213) ·
`gen_library_214.py --selftest` **OK, 9 bites** · `probe_dup_ids` **findings=0** ·
`probe_container_self_query` **findings=0** · `probe_dangling_var_text` **findings=0**.

**Gate glob scope:** `reviews/LIBRARY-*.html` enters **no gate's default glob**
(`probe_dup_ids` defaults to `reviews/REVIEW-*.html`; the other two take an explicit `--glob`).
The three probes above were run against it **by hand**. `knowledge/_render/gen_library_214.py` is
**not wired into `_build_all.py`** — that is a conductor/Dave call, not a sub's.

## Residuals — priced, not hidden

1. **46 of 135 components ship no behaviour script.** Not a library defect — the snippet has
   nothing to run. Named in the generator's stdout; includes `sidebar-nav` (0 lines — the
   *component* draws its states statically; the *shell* that composes it does have the toggle),
   `command-palette` (0 — a keyboard-summoned surface with no keyboard wiring),
   `app-shell-focused`, `navigations`, and every lock-up. Replay is **disabled with a reason** on
   those rows rather than silently inert.
2. **Clicking a destination in a side nav does not move `aria-current`.** Measured in
   App-shell-side-nav: `aria-current="page"` is authored statically and the snippet's JS wires the
   rail toggle only. Real, and it belongs to the component.
3. **The library chrome itself is light-only.** Light/dark drives the *pane*, as v1 did. A dark
   chrome is a design question, not a bug fix.
4. **135 WARN-tier fragment misses** from `probe_dup_ids` — the tree's `href="#c=<slug>"` deep
   links, which JS handles. WARN-tier, findings=0.
5. **`showroom/` was regenerated twice** because a concurrent #214 lane was editing snippets mid-run
   (descender-clip repair). **Re-run `python3 knowledge/gen_showroom.py` after that lane lands** or
   the build gate goes red on their snippets, not on this change.
6. **This document and `reviews/LIBRARY-2026-08-21-v2.html` have no store row**
   ([[forgotten-document]] class). Owed at the conductor's wrap — subs do not write the store.
7. `showroom/index.html` (v1) is untouched and still the RULED library. Whether v2 **replaces** it —
   i.e. whether `gen_showroom.py`'s index template should become this — is **Dave's call**, not
   this lane's.
