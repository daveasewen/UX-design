# RUNBOOK — Common Toolkit tranche (cheap-model session)

*Written by Fable 2026-07-03 so cheaper-model sessions can execute toolkit
tranches with minimum errors and maximum context. The method is proven across
tranche 1 (5 families, register 389→462). Follow it exactly; when in doubt,
FLAG, don't decide.*

## Session start

1. Open with the title convention: **"Title this chat: Toolkit tranche N — <families>"**.
2. Read, in order: this runbook · `_COMMON-TOOLKIT-SURVEY.md` (census + tranche
   status + td- log) · `guidelines/common-toolkit-buttons.md` (the FORMAT
   EXEMPLAR — mirror its structure exactly: bold rule → [DESTINY — rationale,
   xrefs] → `{#id}` anchor · Census section · Findings F1…Fn section).
3. `git status -sb` — note the ahead-count; Dave pushes, you NEVER push.

## Hard rules (non-negotiable)

- **Never rule a REVIEW.** Contradictions, tensions, judgment calls → tag
  `[REVIEW — …needs Dave's ruling]`, add to `_RECONCILIATION.md`, move on.
  Promotion and rulings are Dave's alone (derivation governance, 2026-07-03).
- **Entry tier**: new criteria enter as `[ADVISORY — blocking candidate: …]`,
  NEVER `[BLOCKING]` (ADR-0005 §5 — mis-tagging inflates the BLOCKING count).
  Default destiny when unsure = ADVISORY. RECORDED = context, not criteria.
- **Verbatim capture**: quote exact strings (title copy, error messages,
  numerics, px values, timings). The capture-loss lesson: paraphrase drops
  rules (the 06-17 dark-mode summaries lost 2 clauses). When in doubt, quote.
- **Ingestion only**: do not touch `canon/`, `canon.css`, snippets, gates, or
  metas. Canon deltas are RECORDED as findings, never enacted.
- **IDs**: one prefix per family file (taken: ctkl links · ctkn notifications ·
  ctkt tags/chips · ctkb buttons · ctkf foundations). Sequential ctkX-NNN,
  every rule gets a `{#ctkX-NNN}` anchor. Register count = previous + new IDs;
  update the survey's running total.
- **Three-place consistency**: every ID lands in (1) the family .md, (2)
  `guidelines/_rules-index.json` (`id`/`file`/`destiny`/`destinyFull`/`rule` —
  rule text verbatim incl. any 📌 note), (3) `_RECONCILIATION.md` **only if
  REVIEW**. Verify with grep before committing.
- **Hygiene deltas**: toolkit-internal defects (typos, description debris,
  vintage layering, duplicate frames) → td-NNN in the survey (next free:
  **td-016**). Log and move on — never fix the source.
- **Platform policy**: canon is web-first (Q2 ruling). App/iOS/Android clauses
  are RECORDED context, not binding criteria.
- **Commits**: one per family. Message: `ingest: Common Toolkit <family>
  (ctkX-001…NNN) — <headline>, register NNN`. Commit via `_git_commit.sh`.
  *(Paste-ready summary RETIRED — Dave, #63: Claude commits, Dave pushes.)*

## Figma access recipe (hard-won — do not rediscover)

- Toolkit FILE key `mI8hvIkV98nquoqWzKh5Kn`. Dave's "Gaps and edits" branch
  `Cgbtrmfp15ruNFkIAClpkI` is the RULED source, but it exposes only a Cover
  page — work from the main file.
- Remote `get_metadata` lazy-loads (returns Cover only). Enumerate via the
  desktop bridge: `use_figma` read-only, `figma.root.children`; NO
  `loadAllPagesAsync` (unsupported); `return` a string (console.log is
  swallowed).
- **U+2028 kills the bridge transport deterministically** (ERR_HTTP2_PROTOCOL_
  ERROR, node-specific). Hex-escape non-ASCII in every extraction script and
  the same node passes. (Provenance: the Buttons guide's own "Figma note"
  instructs the soft returns that cause it.)
- `figma.importComponentSetByKeyAsync(key)` resolves library sets living on
  unenumerated pages.
- Library search (`search_design_system`): single nouns, ~20-result cap —
  sample, not census. The page census in the survey is the ground truth.
- Fallback: `get_screenshot` per guide frame (rarely needed post-U+2028 fix).
- Guide frames (`00 <Component> guide`) are components (publishable, td-003) —
  they are the rule-bearing surfaces, plus the create.hsbc-text Standard frames.

## Per-family loop

1. Locate the family page, its `00 <Component> guide` frame(s), and Standard
   frames. Note frame nesting oddities (td- candidates).
2. Extract guide + standard text with the hex-escape script; screenshot only
   on failure.
3. Census the sets: variants × states, On Light/On Dark pairing, description
   fields (debris check), undocumented sets (td-013 kin). Remember td-010:
   docs can be AHEAD of sets — census both directions.
4. Reconcile vs the canon meta for the equivalent component: structure 1:1?
   canon-lacks / canon-exceeds → findings, not actions.
5. Distill the RULES layer to `guidelines/common-toolkit-<family>.md` in the
   Buttons-exemplar format. Rules first, census second, findings (F1…Fn) last.
6. **Capture-loss check**: re-grep the extracted source text for numerics and
   quoted strings; confirm each landed in the distilled file or is knowingly
   excluded.
7. Update `_rules-index.json` + `_RECONCILIATION.md` (REVIEWs only) + survey
   (✅ entry mirroring tranche-1 style + register count + new td- items).
8. Commit. Next family.

## Tranche 2 worklist (in order)

1. **Dropdowns** (`ctkd-`): native / single-select / filterable / multi-select
   (4 taxa — the Q1 four-way-split logic's SECOND TEST: does the
   Notifications-style split hold?) + Pagination dropdown ×2. Canon Dropdown
   is single-select only — 4-taxa split is canon-lacks item 5.
2. **Input Field + Date picker** (`ctki-`): Input fields page + date picker
   input-field vs modal split (S4). Supercharge adjacency — Input-fields ★
   deferred work lives there; RECORD, don't enact.
3. **Progress tracker + Progress indicator + Loading indicator** (`ctkp-`):
   Loading ships per-platform ×3 (Web/iOS/Android) — platform policy applies.
   Watch td-002 vintage ("Day: Progress Indicator" descriptions).
4. **Table** (`ctkta-`): first-row / first-col / row+col header configs.

Then STOP — tranche 3 (Headers ×3 + Masthead + Hero, with the ctkf flyout-grid
and masthead icon vocabulary as inputs) is a fresh session.

## Escalation triggers (flag for Dave, never decide)

- Source contradictions (guide vs standard vs sets) → REVIEW. Precedent:
  ctkb-015 stays open pending a third source; vintage layering is COMMON.
- Anything that implies changing canon, promoting a rule to BLOCKING, or
  deriving a lint.
- 44px/target-size clauses → cite aid-009 and capture COVERAGE wording
  verbatim (per-component receipts are the pattern; ctkt-011's shared-band
  recipe shows why exact wording matters).
- Copy/politeness rules → ctkn-019 is RULED ('Please' banned per-instruction,
  allowed only in the exact standard form-error title). Cite it; don't extend it.

## End of session

1. Verify: JSON valid (`python3 -c "import json; json.load(open('knowledge/
   guidelines/_rules-index.json'))"`) · every new ID greps in the family file
   + index · REVIEWs also in `_RECONCILIATION.md` · survey register count
   matches index count.
2. Update the survey tranche status; write a short GOOD-MORNING.md briefing
   (exec summary + numbered next steps — Dave is dyslexic and time-poor; keep
   it front-loaded).
3. List the commits for Dave to push (he pushes, terminal only). If rm fails
   with "Operation not permitted" on .git locks, request file-delete
   permission rather than declaring failure.

## Channels batch (separate cheap session — do NOT fold into a tranche)

create.hsbc channels pages + web/app design-toolkits.html (PLANNED — not yet built; the enumeration
skeleton) + the named create.hsbc standards the guides defer to
(banner/snackbar/pills/tags/buttons). Method: the Chrome fetch-all recipe
(gotchas in the 07-02 ingestion notes). The buttons standard probe there
feeds the open ctkb-015 ruling.
