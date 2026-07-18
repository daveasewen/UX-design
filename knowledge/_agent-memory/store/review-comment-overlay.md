---
name: review-comment-overlay
description: "BUILT 2026-07-16 (Dave's idea): reusable in-interface review-comment tool. Click a component in a REVIEW copy → pin an in-memory comment → Export → a structured numbered edit-prompt (with section, component, selector, target file) to paste back. Lives in knowledge/_review/ (overlay + injector); keeps out of the gated _proforma glob. Spin-off = review tooling."
metadata:
  node_type: memory
  type: project
---

**What it is:** an in-interface commenting layer for the pro-forma review files, so Dave marks up changes *on the component*
instead of screenshots+prose, then exports a ready-to-run edit prompt. Dave's ask (2026-07-16): *"this review template should
include the ability to add comments so I can make them directly on the interface, and… turn that into the prompt we need to make
the edits."* Decision: *"build it now, make it a reusable template, I don't care if it's in memory / an html artifact / a skill."*
Extends [[review-preview-html]] (always review as live HTML) and is a [[spin-off-candidates]] (review tooling).

**Where it lives:** `knowledge/_review/`
- `_review-overlay.html` — the self-contained overlay (style+script, all `rv-`-prefixed). No deps, **no browser storage**
  (comments live in memory; the Export IS the save). Single source of truth.
- `_make_review.py` — injector: `python3 knowledge/_review/_make_review.py knowledge/_proforma/<file>.html` →
  writes `knowledge/_review/<stem>-REVIEW.html` with the overlay stamped in before `</body>`, plus `<meta rv-doc>` /
  `<meta rv-file>` so the exported prompt names the tranche + exact target file. Re-running restrips+reinjects (idempotent).
- `<stem>-REVIEW.html` — the review copy Dave opens. **Kept OUT of `_proforma/`** on purpose: the component gates glob
  `_proforma/*.html` non-recursively, so review copies in `_review/` are never scanned (the overlay CSS uses raw px chrome).

**Overlay UX:** a bottom-right **Review** toggle (turns crosshair + hover-outline on) → click any component → composer popover
(shows `[Section] descriptor`) → Save pins a numbered red marker + a right-side Comments panel (Reveal / Edit / Delete each).
**Export prompt** modal → Copy to clipboard / Download .md. Clicks are captured in review mode so host nav/handlers don't fire.
Markers reposition on scroll/resize. Verified headlessly (playwright): activate → 2 pins → export, 0 console errors.

**Export format** (paste straight back to me):
```
# Tranche 7 — review edits (N)
Apply the following change requests to `knowledge/_proforma/Tranche-7-interactive.html`. …
1. [Global header] Accounts (a.navlink)
   - <Dave's comment>
   - selector: `#gheader-demo > div.gheader-bar > nav.gheader-primary > a.navlink`
```
Section is read from the nearest `section[aria-labelledby]` heading; descriptor from aria-label/text (+ tag.class); plus a
short DOM-path selector to disambiguate.

**Reusable across all tranches** — run the injector on any interactive file. **Promotion idea (future):** wrap as a `/review`
skill, and/or add a build step that regenerates all `_review/*-REVIEW.html` after each tranche edit. See [[proforma-programme]], [[nav-pattern-catalog]].
