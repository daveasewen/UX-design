---
name: common-toolkit-survey
description: "Common Toolkit pass — TRANCHE 1 FULLY COMPLETE (4 families + FOUNDATIONS delta, register 462); ctkn-019 RULED + ctkb-015 DEFERRED 2026-07-03 (6 commits to push); next = tranche 2 (Dropdown ×4 first); Figma recipe incl. U+2028 fix + capture-loss lesson"
metadata: 
  node_type: memory
  type: project
  originSessionId: 30cbdb47-f36a-4d78-b477-0edc1c264671
---

Common Toolkit rigorous pass, state as of 2026-07-03 eve:

**Access recipe (hard-won):** toolkit FILE key = `mI8hvIkV98nquoqWzKh5Kn` (Dave's
Gaps-and-edits branch `Cgbtrmfp15ruNFkIAClpkI` is the ruled source for edits, but it
exposes only a Cover page). Remote `get_metadata` lists ONLY the Cover for the main
file too (lazy loading) — enumerate via the desktop bridge instead: `use_figma`
read-only (`figma.root.children`; NO `loadAllPagesAsync`, unsupported; `return` a
string, console.log is swallowed). Bridge intermittently drops large text
extractions (ERR_HTTP2_PROTOCOL_ERROR, node-specific) → CAUSE FOUND 2026-07-03:
text nodes containing U+2028 kill the transport deterministically; hex-escape
non-ASCII in the extraction script and the same node passes (screenshot fallback
rarely needed now). Component-key → node: `figma.importComponentSetByKeyAsync(key)`
resolves library sets living on unenumerated pages. Library search: single nouns
only, ~20-result cap, sample-not-census.

**Census:** 55 pages — FOUNDATIONS ×11 guideline pages (breakpoints/type/spacing/
colour/dark/image/icons/elevation/logos/hexagons — "lots of guidelines", need own
tranche) + ELEMENTS & PATTERNS ×40 families + ANIMATIONS ×2. In
`knowledge/_COMMON-TOOLKIT-SURVEY.md` with hygiene deltas td-001…005 (On white:
register break · stale "Day:" descriptions · guide frames publishable · page typo
"Condextual help" · lorem-ipsum stubs in shipped guidance).

**RULED 2026-07-03 (Dave):** Q1 adopt the 4-way Notification split (canon
Notifications → global/inline/contextual/snackbar at its ★ touch; same logic to
test on Dropdown ×4) · Q2 platform variants = RECORDED out-of-scope (web-first,
appf-008 kin) · Q3 Carousel queued via gap-pattern pipeline (aid-010 binds on
arrival).

**Tranche 1:** ✅ Links family DISTILLED → `guidelines/common-toolkit-links.md`
ctkl-001…023 (register 404, commit 54ed528). Headlines: 44-target receipted at
component level WITH inline exception verbatim (→ [[tier2-ingestion-progress]]
aid-009) · CA-6 external-link build spec sourced (end-of-text icon, part of link) ·
arrow-sizing numerics x-height/cap-height by font tier · canon gaps: back link,
expander, anchor links, add/remove (→ Input-fields supercharge), download
microcopy · canon EXCEEDS toolkit on focus (keep). Entry-tier lesson: candidates
enter as [ADVISORY — blocking candidate…], never [BLOCKING…] (ADR-0005 §5;
mis-tagging inflates the BLOCKING count in the index).

✅ Notifications family DISTILLED 2026-07-03 →
`guidelines/common-toolkit-notifications.md` ctkn-001…028 (register 404→421,
commit 49e1235, Dave to push). Canon meta already 1:1 (06-24 rebuild was from this
node set) — value was the RULES layer: severity stacking order + 1px/8px stack
numerics · placement contracts (global ABOVE masthead / contextual below page
title / snackbar ≤6 cols centred, elevated above modals+nav) · snackbar 4–10s,
timeout=fade vs manual=instant · four RAG copy registers incl. exact form-error
title string · aid-009 receipt #3 with NEW hit-area COVERAGE clauses (what the
target covers, per component) · SR announcement strings. ctkn-019 📌 RULED (Dave,
2026-07-03): 'Please' banned per-instruction, allowed ONLY in the exact standard
form-error title (ctkn-020); politeness lint unblocked, copy-035's optional-please
narrowed for error contexts. CORRECTION: toolkit
"Alert" ≠ notification — it's the bell TRIGGER (Size×Active×Badge) + Add Alert →
canon-lacks item 7 (Masthead adjacency). No OL/OD pairing for this family (canon
exceeds on dark). The 4 Standard frames carry REAL create.hsbc text (richer than
Links; lorem only at Form errors — td-005 extended; td-006 = snackbar set
description debris).

✅ Tags+Chips DISTILLED → `common-toolkit-tags-chips.md` ctkt-001…032 (register
444, commit a8242aa). Chips live on the SELECTION CONTROLS page. Two NEW contract
classes: SHARED 44px target band for grouped tag links (12+20+12, adjacent rows
share the 12px band — speaks to the sub-44 revisit pile) + no-layout-shift select
(padding reserves tick width). tag↔pill↔button misuse boundary sourced ·
verb-polarity copy split by chip type · td-007 (Pills/Chips 3-way naming) ·
td-008 (desc debris ×2) · td-009 (duplicate Tags Standard frames) · td-010
(REVERSE vintage: standard documents state ladders the sets never received —
set-census alone under-counts criteria).

✅ Buttons rank-ladder DISTILLED → `common-toolkit-buttons.md` ctkb-001…019
(register 458, commit a58fd22). Quaternary = app-std "Undecorated" (browser std
omits rank 4, td-011) · cardinality: ONE primary and/or ONE secondary per page,
never same group · 8px + primary-first · always rectangular · app "button
activity" pattern = contract for processing/"sucess (app)" variants (td-012
typo) · primary Large UNDOCUMENTED (td-013) · copy lints ≤5 words /
Continue-not-Next / banned generics · aid-009 receipt #6 + name-matches-label ·
"Figma note" instructs soft-return overflow fixes = the U+2028 PROVENANCE.
ctkb-015 📌 DEFERRED (Dave, 2026-07-03): REVIEW stays open — probe the
create.hsbc button standard at channels ingestion for a third source before
fixing the rank-choice heuristic; Button ★ stays gated.

✅ FOUNDATIONS delta pass DONE → `common-toolkit-foundations.md` ctkf-001…014
(register 462, commit 5c18dfd). TRIAGE: tranche was already ⅔-ingested (06-17
Figma batch + 07-02 create.hsbc) — delta-only discipline held (4 indexed). NEW:
masthead-FLYOUT 4-col grid + masthead/footer fluid-XL variant (Headers/Nav
input) · email 6-col grid · 12px=legal-only + medium-weight-paragraph ban ·
2 dark-mode clauses the 06-17 summary DROPPED (light-bleed, extra negative
space) → capture-loss risk: consider re-grepping other 06-17 files vs sources.
ds-001 SOURCE-complete (brand collection has dark RAG TINTS but NO dark solid
accents). Icons CHANGE LOG: live monthly maintenance to 2026-04 vs guides
frozen May 2023 (td-002's cleanest exhibit); mastheadHide/Show + sidePanel
icon vocab for Headers/Nav. td-014/015.

**TRANCHE 1 FULLY COMPLETE** (4 component families + FOUNDATIONS; register
389→462; aid-009 receipted on all five families with per-component coverage
clauses). NEXT: tranche 2 — Dropdown ×4 (Q1-split logic to test) · Input Field
+ Date picker · Progress/Loading · Table header configs. See
[[component-review-program]] · [[fixed-flex-charter]].
