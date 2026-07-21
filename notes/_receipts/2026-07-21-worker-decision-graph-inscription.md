# 2026-07-21 — worker: decision-graph edge inscription (ADR-0012, seed → ledgers)

Mechanical inscription pass following the Fable audit's judgment (`notes/_decision-graph-seed-2026-07-21.json`,
70 nodes / 92 edges, DO NOT edit — untouched). Task: implement `parse_inline_edges()` + a verify/diff mode in
`knowledge/_build_decision_graph.py`, then inscribe the seed's edges as inline `Edges:` lines in their home
ledgers, per ADR-0012 §3/§7.

## Task A — parser + `--verify`

`knowledge/_build_decision_graph.py`:
- **`parse_inline_edges()` implemented** (was a stub returning `[]`). Scans the 4 decision ledgers
  (`_RAG-DECISIONS.md`, `_TYPE-DECISIONS.md`, `_BUTTON-DECISIONS.md`, `_DATAVIZ-DECISIONS.md`) plus every
  `docs/decisions/ADR-*.md` for literal `Edges: type(target, k=v) · …` lines, attributing each to the node
  whose heading/bullet the line sits under. Handles: nested parens inside qualifier values (T-D8's claim
  carries `(80% kills (d))`), a qualifier value that itself contains a comma (R-D20's claim `"red = mode-
  stable, one value light+dark"`) — done by locating qualifier boundaries via the known key set
  (`scope|claim|resolution|reason|ref`) rather than a blind comma-split — and DataViz's flat bullet-list
  node style (`- **DV-D01 · …**`) alongside the `## R-Dn —` heading style used elsewhere.
- **`--verify` / `--diff` mode added**, wired into `__main__`. Diffs the inline-parsed edge set against the
  seed by `(from, type, to)` + all five qualifiers, reports seed-only and inline-only edges, exits non-zero
  on any mismatch (mirrors `--strict`'s honesty model — this IS the acceptance test per ADR-0012 §7).
- **Bug found + fixed while wiring this in:** `main()` was concatenating `seed_edges + parse_inline_edges()`
  unconditionally. Once inscription is live this double-counts every inscribed edge (each exists in both the
  seed and the ledger now) — first full-build run showed **157 edges** instead of 92. Fixed by merging on the
  same key used for `--verify` (inline wins on an exact-key collision, which is a no-op since matched edges
  are identical); `_build_decision_graph.py` (no-arg) now reports **70 nodes · 92 edges · 0 gate warnings**.

## Task B — inscription

Added **61 new `Edges:` lines across 36 nodes** (R-D21's line was already there from the Fable session — not
duplicated):
- `knowledge/_proforma/_RAG-DECISIONS.md` — R-D2, R-D3, R-D4, R-D5, R-D6.A, R-D6.A2, R-D7, R-D8, R-D9, R-D10,
  R-D11, R-D12.A, R-D12.B, R-D13, R-D14, R-D15, R-D16, R-D17, R-D18, R-D19, R-D20 (22 lines incl. R-D21).
- `knowledge/_proforma/_TYPE-DECISIONS.md` — T-D3, T-D8, T-D9, T-D10, T-D12, T-D13, T-D14 (7 lines).
- `knowledge/_proforma/_BUTTON-DECISIONS.md` — B-D1, B-D2, B-D3, B-D5, B-D6 (5 lines).
- `knowledge/_proforma/_DATAVIZ-DECISIONS.md` — DV-D01, DV-D04, DV-D06 (3 lines, as an indented continuation
  under each bullet).
- **Minimal disambiguation tags added** (content unchanged, just an ID label appended to the existing
  heading text so the parser — and a human — can attribute the sub-ruling correctly): RAG's `### Ruling A`
  / `### Ruling A′` under R-D6 → `(R-D6.A)` / `(R-D6.A2)`; `### Ruling A` / `### Ruling B` under R-D12 →
  `(R-D12.A)` / `(R-D12.B)`. R-D6.B carries no outbound seed edges, so its heading was left untouched.

All 61 lines transcribed verbatim from the seed (qualifier values unedited, order normalised to
`scope, claim, resolution, reason, ref` to match the generator's own `fmt_edge()` convention — order doesn't
change meaning and the R-D21 precedent only had one qualifier per call, so there was no existing convention
to break).

## Task C — verify

- **`--verify`: 65/92 edges matched, ZERO inline-only (invented/mistyped) edges.** 27 remain seed-only —
  see "Stopped on" below; they are not a defect, they're the two judgment calls the task asked me to flag
  rather than resolve.
- **`--selftest`: PASS** (gate still bites on unresolved/open/orphan, stays green on queued/diverges-from).
- **`_build_all.py`: green, 38/38** (`decision-graph` is step 11/38, advisory). Re-ran after the merge-vs-
  concatenate fix; no other step affected.

## Stopped on (genuine judgment calls — not guessed)

**1. Seven ADRs (18 edges) — already native, didn't double-inscribe.** Every single ADR-sourced seed edge
(ADR-0006/7/8/9/10/11/12, 18 edges total) is already expressed in that ADR's own header via `**Extends:**` /
`**Relates:**` — e.g. ADR-0006's header already reads `Extends: ADR-0005`, matching the seed's
`refines(ADR-0005)` exactly. Per the docstring ("source files are NOT rewritten to conform... the parser
normalises") adding a redundant `Edges:` line to these headers risked exactly the double-count the task
flagged as a stop condition. I did NOT add them. I also deliberately did **not** teach `parse_inline_edges()`
to read the native `Extends:`/`Relates:` syntax via the alias map as an alternative — ADR-0012's own header
(multi-line, with a `**Status:**` parenthetical that name-drops R-D2/R-D7/R-D21 in prose) showed that a
naive regex over "the whole header block" would misattribute those in-prose mentions as graph edges. Making
that safe needs a real per-field parse (only extract IDs from the `Extends:`/`Relates:` segments, never from
`Status:` prose) — a second piece of judgment I didn't want to guess my way through under a receipt.
**Net effect:** these 18 show as "seed but not inscribed" in `--verify` — they're covered by existing prose,
just not by the new machine-checkable grammar. Your call: (a) leave as-is (native syntax is the ADR home,
full stop), or (b) have a future pass teach the parser to read `Extends:`/`Relates:` per-field so `--verify`
goes fully green.

**2. Nine edges (8 from-nodes) with no home among the five routing prefixes.** `CHARTER.S9`, `DEF-006`,
`TYPE:2026-07-18:sat-ceiling` (×2), and five guideline-REVIEW-rule-sourced `conflicts-with` edges
(`ill-007`, `mot-007`, `ctkb-015`, `type26-015`, `webf-032`) all have a `from` that isn't `R-D*`/`T-D*`/
`B-D*`/`DV-D*`/`ADR-*` — the task's routing table doesn't cover them, and ADR-0012 §3 explicitly says REVIEW
rules are "not re-authored" (their edges live on the ledger/ADR side, not inside `_RECONCILIATION.md`) and
anchors are "minted at edge-authoring time" into ledger prose at need — neither of which tells me which
existing file/paragraph is the right home for e.g. `CHARTER.S9`'s `supersedes(ADR-0006, claim=cool-warm-hot
register framing)`. Left uninscribed rather than invent a location. These 9 are the other component of the
27 `--verify` reports as seed-only.

**Nothing else was ambiguous** — the remaining 61 edges had one unambiguous ledger entry each, and none of
the seed's structural targets resolved to a missing node (`--strict` is clean).

## Files touched

- `knowledge/_build_decision_graph.py` — `parse_inline_edges()` implemented, `--verify`/`--diff` mode added,
  `main()` edge-merge bug fixed.
- `knowledge/_proforma/_RAG-DECISIONS.md`, `_TYPE-DECISIONS.md`, `_BUTTON-DECISIONS.md`,
  `_DATAVIZ-DECISIONS.md` — 61 `Edges:` lines + 4 disambiguation tags, no other text changed.
- Generated (by the build, not hand-edited): `knowledge/_DECISION-GRAPH.md`, `knowledge/_decision-graph.json`,
  plus the usual `_build_all.py` regen artifacts.

## Did not touch

The seed JSON, `GOOD-MORNING.md`, `_LIVE-STATE.md`, memory, or git (tree left dirty for the conductor, per
brief).

---

## Finishing pass (2026-07-21, later same day) — the last 27 edges, per Dave's two rulings

Picked up exactly where the first pass stopped (its "Stopped on" §1/§2 above, 18 + 9 edges). Dave ruled both
open judgment calls; this pass is mechanical transcription against those rulings, not new judgment.

### RULING 1 — 18 ADR→ADR/R-D edges → native `**Extends:**`/`**Relates:**` header fields

Checked all 7 ADRs' current header text against the seed's exact per-ADR target list before touching anything:

- **ADR-0006, ADR-0007, ADR-0008, ADR-0009, ADR-0012 — already exactly matched the seed, zero edits.** Their
  `**Extends:**`/`**Relates:**` fields already carried precisely the seed's targets (ADR-0012's `**Extends:**
  ADR-0007` was already there, per the brief's "verify, don't duplicate" instruction).
- **ADR-0010 and ADR-0011 — found a real discrepancy, resolved per the ruling's own literal example text.**
  - `ADR-0010`'s `**Extends:**` field carried an extra `, ADR-0004 (WCAG 2.2 AA floor)` beyond the seed's two
    targets (`ADR-0009`, `R-D15`). The ruling's own worked example ("e.g. ADR-0010 header gets `**Extends:**
    ADR-0009 · R-D15`") gives the exact desired field text, which excludes ADR-0004 — so I trimmed it. The
    AA-floor relationship isn't lost: ADR-0010's own body already states it explicitly ("**5. AA remains
    invariant (ADR-0004).**", Decision item 5).
  - `ADR-0011`'s `**Relates:**` field carried an extra `, R-D17 + \`_validate_legacy_leak.py\` (Legacy-colour
    leakage gate)` beyond the seed's one target (`R-D19`). Seed only assigns the R-D17 relation to ADR-0010,
    not ADR-0011 (which already carries all 4 of its `refines` targets correctly). Trimmed to just R-D19; the
    R-D17/leak-gate relationship is still discussed in ADR-0011's own "theme-provenance gate" section.
  - **Flagging this rather than silently doing it:** both fields, as originally written, would have parsed
    into edges NOT in the seed (an "invented" edge by `--verify`'s own definition) — the seed is the audited
    source of truth (ADR-0012 §7), and Dave's own worked example already specified the corrected text, so I
    trimmed rather than stopping. If the ADR-0004/R-D17 mentions were meant to stay as *additional* untyped
    relations, they can be re-added as prose outside the Extends/Relates field (they don't need the formal
    edge grammar to be documented — both are still stated in body prose).
- **Parser**: `knowledge/_build_decision_graph.py` — `_parse_adr_file` rewritten. New `_adr_header_text()`
  collects the header paragraph (all lines after the `# ADR-00NN` title up to the first blank line — handles
  ADR-0012's 7-line soft-wrapped header the same as a one-liner). New `_parse_adr_header_fields()` regexes
  `EXTENDS_FIELD_RE`/`RELATES_FIELD_RE` capture ONLY the text between a field's own bold label and the next
  bold label (`**Relates:**`/`**Method:**`/`**Status:**`) or end of paragraph — never the whole header block —
  so `**Status:**` prose that name-drops R-D2/R-D7/R-D21 (ADR-0012's own header does this) is structurally out
  of scope, not filtered by a keyword blocklist. `HEADER_ID_RE` (new: `ADR_TOKEN` ∪ extended `NODE_TOKEN`)
  pulls every recognised ID out of each field's captured text; `Extends` → `refines`, `Relates` → `relates`.
  The old body-only `Edges:`-line scan is kept (for symmetry / future edge types the header grammar can't
  express), now running alongside the header-field parse rather than instead of it.

### RULING 2 — 9 non-ledger edges, inscribed at each node's own source file

Grepped each `from` id first to find its real home, then added an `Edges:` line right under/after the rule,
same grammar and format as the ledger lines (verbatim qualifiers, `note=` fields dropped — confirmed against
the 36 already-inscribed lines from the first pass that `note` is seed-commentary, not a parsed qualifier;
`QUAL_KEYS` only recognises `scope|claim|resolution|reason|ref`, and letting `note=` through the "to" field
capture would have corrupted the target string).

- **`CHARTER.S9` → `knowledge/_FIXED-FLEX-CHARTER.md`.** Home = "## 9. Register = an inference ramp" (the
  section ADR-0006's own header amendment names as the thing that superseded its cool-warm-hot framing).
  Minted `(CHARTER.S9)` on the heading (same convention as the first pass's `(R-D6.A)` tags); added
  `Edges: supersedes(ADR-0006, claim=cool-warm-hot register framing)` at the end of the section, before the
  `### 9a.` subsection starts.
- **`DEF-006` → `knowledge/_proforma/_TYPE-DECISIONS.md`, "Rule 3" section.** This section's own prose already
  states the seed's `reason=` text almost verbatim ("DEF-005 exempts an intrinsic square… DEF-006 does NOT
  mirror that exemption… the divergence is intended"). Minted `(DEF-006)` on the heading; added
  `Edges: diverges-from(DEF-005, reason=…)` (verbatim from seed) after the paragraph.
- **`TYPE:2026-07-18:sat-ceiling` → same file, "Q-new ANSWERED" section.** Minted
  `(TYPE:2026-07-18:sat-ceiling)` on the heading; added
  `Edges: supersedes(TYPE:2026-07-18:badge-A8000B) · refines(col26-020)`. (`TYPE:2026-07-18:badge-A8000B` is
  only ever a target in this pass, not a `from`, so it needed no anchor of its own — the gate's
  `conflicts-with`-only orphan exemption doesn't apply here, but both targets already resolve: the badge-ID
  contains `:` and `col26-020` matches `RULE_ID`, so neither trips `orphan-target`.)
- **`ctkb-015` → `knowledge/guidelines/common-toolkit-buttons.md`** (canonical guideline copy, not the
  `designer-skills-v1/` distributed copy). Rule already carries a `{#ctkb-015}` anchor; added
  `Edges: conflicts-with(app-inline-button-standard, resolution=deferred, ref=Dave 2026-07-03 — probe
  create.hsbc at channels ingestion)` on the next line, same indent as the rule's own continuation lines.
- **`ill-007` → `knowledge/guidelines/illustration-standards.md`.** `Edges:
  conflicts-with(colour-standards-2026, resolution=ruled)`.
- **`mot-007` → `knowledge/guidelines/motion-standards.md`.** `Edges: conflicts-with(canon-spring-physics,
  resolution=deferred)`.
- **`type26-015` → `knowledge/guidelines/typography-standards-2026.md`.** `Edges:
  conflicts-with(CHARTER.S4-gradients, resolution=parked, ref=component-finessing pass, with mot-007)` — the
  `ref` value's embedded comma is handled the same way R-D20's claim text was in the first pass (qualifier
  boundaries located by known key set, not a blind comma-split).
- **`webf-032` → `knowledge/guidelines/web-foundations.md`.** `Edges: conflicts-with(4px-base-unit-standard,
  resolution=interim, ref=toolkit-wins stance)`.

**Parser extension:** `NODE_TOKEN` widened to recognise the three minted anchor shapes (`CHARTER\.\w+`,
`DEF-\d+`, `TYPE:[\w:.-]+`) alongside the original `R-D*`/`T-D*`/`B-D*`/`DV-D*`. `_scan_current_node` gained an
`ANCHOR_HASH_RE` check (`\{#id\}` at end of line) so guideline-file `{#id}` bullets are recognised as node
homes the same way ledger `##`/`###` headings already were. New `EXTRA_INLINE_FILES` list (charter + the 5
guideline files) is scanned via the existing generic `_parse_ledger_file` walker — no new parsing code needed,
it was already file-agnostic. `_TYPE-DECISIONS.md` needed no new file entry (already in `LEDGER_FILES`).

**Bug caught while wiring `ANCHOR_HASH_RE` in:** the first version matched `{#id}` anywhere on a line, which
fired on the ledgers' own mid-prose citations of *other* rules — `` `{#dv-017}` ``, `` `{#icon-011}` `` etc.
appear backtick-wrapped inside R-D3/R-D5/R-D6.A/R-D6.A2's own text (e.g. R-D3: "`{#dv-017}`(a) permits
red/green…"), never as the line's last token. First `--verify` run after adding the check showed 9 edges
mis-attributed (R-D3's edges landing on `dv-017`, R-D6.A's on `icon-013`, etc. — swapped from/to). Fixed by
anchoring the regex to end-of-line (`\{#id\}\s*$`), which matches every genuine guideline-rule anchor (all 5
confirmed end-of-line in their source) but excludes every mid-sentence ledger citation. Same class of trap as
the ADR Status-prose one — a second reminder that `{#id}`/`(ID)` shapes need a *positional* guard, not just a
pattern match.

### Task C — verify

- **`--verify`: 92/92 matched, ZERO seed-only, ZERO inline-only. `decision graph --verify: seed 92 edges ·
  inscribed 92 edges parsed · 92 matched … ZERO mismatch — inscribed corpus == seed.`**
- **`--selftest`: PASS** (unresolved/open/orphan still fire; queued/diverges-from still green).
- **No-arg build: `decision graph: 70 nodes, 92 edges -> knowledge/_DECISION-GRAPH.md`, 0 gate warnings.**
  `--strict` also exits 0 clean.
- **`_build_all.py`: green, 38/38 steps ran, exit 0** — `✅ all generators ran and the integrity + contrast
  gates passed.` (integrity: 0 errors, 3 warnings, pre-existing and unrelated to this pass).

### Files touched (finishing pass)

- `knowledge/_build_decision_graph.py` — `_parse_adr_file` rewritten (header-field parser), `_scan_current_node`
  gained the end-of-line `{#id}` anchor check, `NODE_TOKEN`/new regex constants, new `EXTRA_INLINE_FILES` list.
- `docs/decisions/ADR-0010-token-schema-nullable-flex-slots.md` — `**Extends:**` field trimmed (see Ruling 1).
- `docs/decisions/ADR-0011-four-theme-token-architecture.md` — `**Relates:**` field trimmed (see Ruling 1).
- `knowledge/_FIXED-FLEX-CHARTER.md` — minted `(CHARTER.S9)`, added its `Edges:` line.
- `knowledge/_proforma/_TYPE-DECISIONS.md` — minted `(DEF-006)` and `(TYPE:2026-07-18:sat-ceiling)`, added
  their `Edges:` lines.
- `knowledge/guidelines/common-toolkit-buttons.md`, `illustration-standards.md`, `motion-standards.md`,
  `typography-standards-2026.md`, `web-foundations.md` — one `Edges:` line each (ctkb-015/ill-007/mot-007/
  type26-015/webf-032).
- Generated (by the build, not hand-edited): `knowledge/_DECISION-GRAPH.md`, `knowledge/_decision-graph.json`,
  plus the usual `_build_all.py` regen artifacts.

### Did not touch (finishing pass)

The seed JSON, `GOOD-MORNING.md`, `_LIVE-STATE.md`, memory, or git — tree left dirty for the conductor, per
brief. Nothing was guessed: the one real judgment call (ADR-0010/0011 field trims) had its exact resolution
already spelled out in the ruling's own worked example, so it's recorded above as a flagged action, not a
silent one.
