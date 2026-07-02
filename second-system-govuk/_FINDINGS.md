# Second-system run — GOV.UK · findings log

*Review decision #4 (2026-07-02): run one public system through the runbooks, timeboxed 2 days,
to split the engine from HSBC content. Started 2026-07-02. Public data only — clean under the
two-machine rule. Nothing in `knowledge/` is touched; this directory is the whole experiment.*

**The deliverable is this log, not the GOV.UK canon.** Every place the engine assumed HSBC is a
finding; each becomes a goal for multi-tenancy or gets accepted as intentional coupling.

## Status

- [x] Day 1a — token stores extracted to DTCG (`tokens/`): colour (10 palette groups + white),
      semantic-colour (20 functional aliases, 0 dangling), spacing (10 points), typography
      (GDS Transport + 7 responsive steps). Source: `govuk-frontend` npm package, `settings/*.scss`.
- [x] Day 1b — **5 gated snippets + metas** built per `_RUNBOOK-gated-component.md`:
      Button, Tag, Text-input, Error-summary, Details. All contrast pairs pre-checked
      with `_contrast_utils` (15/15 declared pairs pass; 2 correctly rejected — F7 + the
      decorative details rule).
- [x] Day 2 — gates in scope run green: **snippet gate 5/5** (one patch: themes from
      `system.json`, F4) and **a11y gate 5/5 (zero modifications)**. Out of scope by
      intention: coverage/integrity/contrast-audit gates presume full-canon structures
      (blast radius, xref, dark stores) that a 5-component probe doesn't have — running
      them would test canon *completeness*, not engine *portability*.

## Verdict (decision #4 — closed 2026-07-02, same day, under timebox)

**The engine generalises.** A second design system was onboarded from public code source
to gated, build-verified reference components in one session. The HSBC coupling is
shallow and enumerable: two themes (F4), Figma-shaped hub (F5), no alias resolution /
engine-specific store shape (F6) — each a small, named fix. The differentiated logic —
contrast enforcement, ARIA checks, focus rules, retrieval-not-recall — transferred
without edits and immediately caught real issues in both the target system (F7) and the
operator (F8). The "single-tenant HSBC" risk from the standing review is answered.

## Findings so far

### F1 — Provenance path asymmetry
HSBC entered via Figma variable exports (`tokens/_INGEST-NOTES.md`); GOV.UK enters via code
(scss in an npm package). The engine has no recorded ingestion path for code-source tokens —
this run creates the precedent. Ingestion is source-shaped, not system-shaped.

### F2 — HSBC assumptions hardcoded in engine scripts (grep, 2026-07-02)
- `knowledge/_validate_icons.py` — icon provenance tied to the HSBC icon library
- `knowledge/compliance/_build_compliance_kg.py` — HSBC references
- `knowledge/canon/gen_canon_tokens.py` — generator assumes the HSBC store shape/paths
- `knowledge/assets/logos/_export-logos.py`, `assets/icons/_export-icons.py` — HSBC asset pipelines
- `knowledge/tokens/typography.json` — Univers as the type primitive
Each needs either a parameter (system root) or an explicit "single-tenant by design" ruling.

### F3 — Structural differences GOV.UK forces the schema to face
- **Responsive modes**: GOV.UK type steps carry mobile/tablet(/desktop) values per step —
  same shape as HSBC's TScale problem (ingest note #8), so the "reference the step, not the px"
  rule generalises. Good sign.
- **Flat vs grouped tokens**: `white` is flat (#ffffff, no variants) while other colours are
  variant groups. DTCG handles it; alias resolution must too (hit and fixed in our extractor).
- **Legacy alias names** (`dark-grey` → black/tint-25 etc.) — GOV.UK keeps deprecated names
  mapped, HSBC deletes (`depricate` purge). Two different deprecation philosophies; the store
  needs to represent both.

### F4 — The gates assume two themes
`_validate_snippets.py` hardcodes `("light", "dark")` in the fidelity loop, the theme-block
requirement, and the contrast loop. GOV.UK has no dark theme. **Fix proposal (implemented in
the copy here):** each system declares `themes` in a `system.json`; the gate iterates the
declaration. One small patch; everything else ran unmodified.

### F5 — Hub identity is Figma-shaped
`provenance.figma_node` is the engine's immutable hub key (`_RUNBOOK-onboard-code-library.md`).
GOV.UK has no Figma node; its natural hub is package + path (`govuk-frontend` +
`components/button`). The hub model needs one more identity type: code-source. Flagged in all
three metas.

### F6 — Gates don't resolve DTCG aliases; the store shape is engine-specific
The validator resolves `token/path → {mode: hex}` directly — no `{palette.x.y}` alias
resolution, and mode-keyed values rather than DTCG `$value`. So a second system needs a
*generator* (DTCG source → resolved engine-shape store), mirroring `canon/gen_canon_tokens.py`.
Done here as a build step; should be a named, system-agnostic tool.

### F7 — The gate correctly bit GOV.UK's known focus weakness
Declared `focus/background` (yellow #FFDD00) on white as a ui pair: **1.35:1 — blocked.**
This is the documented reason GOV.UK's focus style pairs yellow with a black keyline. Runbook
step 3 applied cleanly to a foreign system: the failing pair is not declared; the black inset
shadow (19.59:1) is the gated indicator; yellow is decoration. The enforcement logic
generalises — it caught in seconds what GDS documents in prose.

### F8 — Recall drift caught twice, by the operator, mid-run
Writing the Button snippet I typed `#F3F2F1` / `#DBDAD9` (v4-era greys) from memory; the v5
store says `#F3F3F3` / `#CECECE`. Also nearly used `#00703c` for the green; v5 is `#0f7a52`.
Retrieval-not-recall (charter §5) is not just for generators — it catches *human/agent*
drift across design-system versions. The strongest cross-system validation of the thesis yet.

### F9 — Cosmetic: audit writer hardcodes "light+dark"
`_SNIPPET-AUDIT.md`'s pass line says "token fidelity (light+dark)" regardless of declared
themes. String only; checks are correct. Fix alongside F4.

## Method receipts
Runbooks in use: `_RUNBOOK-gated-component.md` (snippets) · `_RUNBOOK-onboard-code-library.md`
(read; not applicable — that's for consuming code libraries, not source systems; noted as a
runbook-coverage gap: **no runbook exists for "onboard a design system"** — this log drafts it).
