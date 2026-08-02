# Governing records — the standing register of Dave-owed close conditions

provenance: #87 · 2026-08-02
status: ruled — `notes/_MEMENTO-DECISIONS.md` § ★ #86-D1/D2 (Dave: "Yes, firm — record them")

**Contract (declared at birth — splitting never buys headroom):** this file is a STANDING register,
not an archive and not a worklist. One row per governing item — a live value or behaviour running
today on a choice Dave never made. A row leaves ONLY when its `closes_when` fires (Dave's word),
and the closure is inscribed in the owning ledger first, then the row is marked ✅ CLOSED here with
a pointer (marked, never deleted — the register is also the record of what was once open). New rows
enter only with a `closes_when` on the way in. Source of truth for the birth cohort:
`reviews/TRIAGE-BANKRUPTCY-2026-08-02-v1.html` (+ .REVIEW pair), 19/19 ratified at #86.
⚠ Counts in this file are NOT typed summaries — the row count IS the count; probe it, don't quote it.

| id | Item (live location) | closes_when | status |
|---|---|---|---|
| G1 | Worklist-index cap `DOFIRST_INDEX_TK_MAX = 700` (`_capture_gate.py:1403`, agent-picked stopgap over measured 531 real) | Dave ratifies 700 or names his own number | OPEN |
| G2 | `TAPE_TO_BILL = 1.57` at n=2 (`_capture_gate.py:371`; `RATIO_FIRM_N = 4` per ds-021 (c)) | 4 measured pairs logged, then Dave rules firm-or-retire | OPEN |
| G3 | `retired_unit_prose_audit` tier = WARN (`_capture_gate.py:2078, 2098`, agent-picked) | Dave rules warn vs block | OPEN |
| G4 | GM §C measured 191 > 150 warn cap (`_capture_gate.py:2864`, `_gm_usage.py:517`) | Dave picks OFFLOAD / TRIM / KEEP | OPEN |
| G5 | Four advisory size caps as a set (`_capture_gate.py:4843–4858`: `CORPUS_BUDGET_TK 36000` · chain-region pair (4917, 6417) · `BANNER_BUDGET_FALLBACK_TK` · `SECTION_A_WARN_TK 4500`) — all in the old unit | Re-measured in real (G9 first), then Dave ratifies the set in one pass | OPEN — blocked on G9 |
| G6 | `DEFER_STREAK = 6` (`_gm_usage.py:353`) + `USAGE_HISTORY_BLOCKING = False` | Dave rules the streak number + per-candidate OFFLOAD/TRIM/KEEP calls | OPEN |
| G7 | Which end of an archive is "newest" (strata oldest-first · archives newest-first; `_capture_gate.py:268`, ledger:662, 687; tension: [[unkeyed-gate-vs-roll2f-tension]]) | Dave names the convention — one sentence | OPEN |
| G8 | Dormant % band `BAND_FLOOR/HARD_STOP/MARKED_MAX = 45/60/63` (`_capture_gate.py:135–137`, DORMANT, forked #58) | Dave says retire or pin | OPEN |
| G9 | ds-023 re-measurement programme — every old-unit ceiling tightened ~1.55×; re-measure each on its artefact in real, restamp with provenance, never convert (ledger:1764) | Dave rules the programme | OPEN |
| G10 | The "70%/95%" stray band (GM:36 — matches neither retired 45/60/63 nor #56's replacement; no provenance repo-wide; FENCED) | Dave rules provenance or strikes it | OPEN |
| G11 | DS-018 recessive value — four candidate greys incl. `#9D9D9D`, explicitly not a recommendation (`_DS-IMPROVEMENTS.md:939`; review `reviews/DS-018-DISABLED-STATE-2026-07-27-v1.REVIEW.html`) | Dave picks the recessive value | OPEN |
| G12 | Charter §4b tone-of-voice temperature map, PROVISIONAL 2026-07-02 (`_FIXED-FLEX-CHARTER.md:55–71`; live from `guidelines/tone-of-voice.md:114`) | tov-016 review lands, or Dave ratifies the mapping as-is | OPEN |
| G13b | `menu-search` combined glyph, PROVISIONAL 2026-07-16 (`_ICON-GAPS.md`; the surviving half of G13 — crescent half CLOSED by #86-D2) | Dave approves the glyph | OPEN |
| G14 | Icon-button dark bindings — reuses Button's on-light/on-dark verbatim (`icon-button.meta.json:68`; parent: SC dark, ADR-0014) | Dave rules the SC-dark bindings | OPEN |
| G15 | DV-D13 donut centre figure + `st.visible[id]=true` release wiring (agent's calls; `_REVIEW-SIGNOFF.md` backlog) | Dave's sign-off eye | OPEN |
| G16 | The `_proforma/_DATAVIZ-DECISIONS.md:567` enactment call (agent's, not Dave's) | Dave ratifies or reverses | OPEN |
| G17 | RAG status manifestation (`reviews/RAG-STATUS-MANIFESTATION-2026-07-19-v1`; ⚠ live-render status UNVERIFIED at #86, declared residual) | Dave's canon pick — A / A+B / A+B+C | OPEN |

**PILE 3 — protected class, NOT records here and NOT archived (ruled #86-D3):** molecules pack
(#66 enacts pending) · radius/corner tuner ("return SOON") · #84-D1 successor instrument.
Ruled-but-unenacted lives in its own ledgers/`_REVIEW-SIGNOFF.md`; this register must not annex it.

**The archive counterpart:** `knowledge/_BANKRUPTCY-ARCHIVE.md` — items there return only when
named, each gaining a row HERE (with `closes_when`) on the way back in.
