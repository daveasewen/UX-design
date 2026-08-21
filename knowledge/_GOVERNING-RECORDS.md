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
| G1 | Worklist-index cap `DOFIRST_INDEX_TK_MAX = 700` (`_capture_gate.py:1403`, agent-picked stopgap over measured 531 real) | Dave ratifies 700 or names his own number | ✅ **PARKED #212** — `s212-D5` (ratified at 700 and parked as a set with G2+G6). ⚠ **Park is CONDITIONAL: returns to Dave the first time a gate fails on it, with the live failure attached.** |
| G2 | `TAPE_TO_BILL = 1.57` at n=2 (`_capture_gate.py:371`; `RATIO_FIRM_N = 4` per ds-021 (c)) | 4 measured pairs logged, then Dave rules firm-or-retire | ✅ **PARKED #212** — `s212-D5` (ratified at 1.57 and parked as a set with G1+G6). ⚠ Conditional park; **G2's own firm-or-retire-at-n=4 rule survives the park unchanged.** |
| G3 | `retired_unit_prose_audit` tier = WARN (`_capture_gate.py:2078, 2098`, agent-picked) | Dave rules warn vs block | ✅ **CLOSED #161** — `s161-D2` (WARN ratified provisionally), superseded by `s163-D1` (#163) which flipped it to **BLOCK**. ⚠ **Marked at the #212 wrap, not at #161: this row read OPEN for 51 sessions after its own closure** — register-vs-store join gap, reported in `notes/_MEMENTO-DECISIONS.md` § ★ #212 finding 3. |
| G4 | GM §C measured 191 > 150 warn cap (`_capture_gate.py:2864`, `_gm_usage.py:517`) | Dave picks OFFLOAD / TRIM / KEEP | OPEN — remedy RULED **OFFLOAD** (`s212-D6`, #212), enactment rowed `W-99b`. ⛔ **The 150 cap is NOT re-dialled by that ruling.** Closes when §C measures back under its warn cap (187 charged lines at the #212 wrap). |
| G5 | Four advisory size caps as a set (`_capture_gate.py:4843–4858`: `CORPUS_BUDGET_TK 36000` · chain-region pair (4917, 6417) · `BANNER_BUDGET_FALLBACK_TK` · `SECTION_A_WARN_TK 4500`) — all in the old unit | Re-measured in real (G9 first), then Dave ratifies the set in one pass | ✅ **CLOSED #212** — `s212-D11` (the four caps ratified at the measured restamps: corpus 55700 · chain (7700, 10000) · banner fallback (6400, 7800) · §A 7200). Enacted in `_capture_gate.py` the same session, with the M8 fixture-derivation class fix. ⚠ **Riders NOT closed, rowed `W-99d`:** the `bill_of()` 1.57× repair and the re-PICK of `SIZE_BUDGET` 8000 / `TITLE_CAP_TAPE` 120. |
| G6 | `DEFER_STREAK = 6` (`_gm_usage.py:353`) + `USAGE_HISTORY_BLOCKING = False` | Dave rules the streak number + per-candidate OFFLOAD/TRIM/KEEP calls | ✅ **PARKED #212** — `s212-D5` (ratified at 6 / False and parked as a set with G1+G2). ⚠ Conditional park; returns on the first live gate failure. |
| G7 | Which end of an archive is "newest" (strata oldest-first · archives newest-first; `_capture_gate.py:268`, ledger:662, 687; tension: [[unkeyed-gate-vs-roll2f-tension]]) | Dave names the convention — one sentence | ✅ **CLOSED #161** — `s161-D3` (convention ratified as-is). ⚠ **Marked at the #212 wrap, not at #161** — same join gap as G3. |
| G8 | Dormant % band `BAND_FLOOR/HARD_STOP/MARKED_MAX = 45/60/63` (`_capture_gate.py:135–137`, DORMANT, forked #58) | Dave says retire or pin | ✅ **CLOSED #161** — `s161-D1` (retire completely; confirms `#74-D3`). ⚠ **Marked at the #212 wrap, not at #161** — same join gap as G3. |
| G9 | ds-023 re-measurement programme — every old-unit ceiling tightened ~1.55×; re-measure each on its artefact in real, restamp with provenance, never convert (ledger:1764) | Dave rules the programme | ✅ **CLOSED #212** — `s212-D7` (programme RULED RUN, delegated). Executed the same session by an Opus sub, every cap measured in real via the gates' own extractors with baselines reproduced exactly at their ruling commits; receipt `notes/_receipts/2026-08-21-212-g9-ds023-remeasurement.md`. Ratification was G5's and is done. |
| G10 | The "70%/95%" stray band (GM:36 — matches neither retired 45/60/63 nor #56's replacement; no provenance repo-wide; FENCED) | Dave rules provenance or strikes it | ✅ **CLOSED #212** — `s212-D4` (STRUCK on Dave's word). ⚠ **The literal was already absent from `GOOD-MORNING.md` when the ruling was inscribed** (probed at the #212 wrap, `grep -c` = 0); the strike rides on the ruling and this closure, and **no edit was manufactured to produce an enactment**. |
| G11 | DS-018 recessive value — four candidate greys incl. `#9D9D9D`, explicitly not a recommendation (`_DS-IMPROVEMENTS.md:939`; review `reviews/DS-018-DISABLED-STATE-2026-07-27-v1.REVIEW.html`) | Dave picks the recessive value | ✅ **CLOSED #212** — `s212-D1` (recessive grey **`#9D9D9D`**). ⚠ Enactment is separate and rowed `W-99`; the light/dark pairing question raised at the ruling was probed and **DISCHARGED by the evidence amend** (the settled B-D4 block already carries the pair). |
| G12 | Charter §4b tone-of-voice temperature map, PROVISIONAL 2026-07-02 (`_FIXED-FLEX-CHARTER.md:55–71`; live from `guidelines/tone-of-voice.md:114`) | tov-016 review lands, or Dave ratifies the mapping as-is | ✅ **CLOSED #212** — `s212-D3` (temperature map RATIFIED as-is, unchanged, after seven weeks live). Stamps enacted the same session: `_FIXED-FLEX-CHARTER.md` §4b + `guidelines/tone-of-voice.md` tov-016, PROVISIONAL → RATIFIED. Release packs untouched. |
| G13b | `menu-search` combined glyph, PROVISIONAL 2026-07-16 (`_ICON-GAPS.md`; the surviving half of G13 — crescent half CLOSED by #86-D2) | Dave approves the glyph | ✅ **CLOSED #212** — `s212-D9` (the designed Figma Neo-net glyph, node 2785:97115, APPROVED — Dave: *"good"*). Asset `knowledge/assets/icons/menu-search.svg`; consumer `knowledge/_proforma/Masthead-interactive.html`. |
| G14 | Icon-button dark bindings — reuses Button's on-light/on-dark verbatim (`icon-button.meta.json:68`; parent: SC dark, ADR-0014) | Dave rules the SC-dark bindings | ✅ **PARKED #212** — `s212-D8` (parked under its parent, SC dark / ADR-0014). ⚠ **Un-parks AUTOMATICALLY into the SC-dark sitting**; until then icon-button keeps reusing Button's on-light/on-dark verbatim. |
| G15 | DV-D13 donut centre figure + `st.visible[id]=true` release wiring (agent's calls; `_REVIEW-SIGNOFF.md` backlog) | Dave's sign-off eye | OPEN — a dedicated sitting is rowed `W-99c` (#212, Dave: he wants to get into the donut pair with G16). |
| G16 | The `_proforma/_DATAVIZ-DECISIONS.md:567` enactment call (agent's, not Dave's) | Dave ratifies or reverses | OPEN — a dedicated sitting is rowed `W-99c` (#212, paired with G15). |
| G17 | RAG status manifestation (`reviews/RAG-STATUS-MANIFESTATION-2026-07-19-v1`; ⚠ live-render status UNVERIFIED at #86, declared residual) | Dave's canon pick — A / A+B / A+B+C | ✅ **CLOSED #212** — `s212-D2` (canon pick **A+B+C**, judged on the live render iframed in `reviews/REVIEW-212-rule-now-v1.html`, which also answers the #86 unverified-live-render caveat). Enactment rowed `W-99a`. |

**PILE 3 — protected class, NOT records here and NOT archived (ruled #86-D3):** molecules pack
(#66 enacts pending) · radius/corner tuner ("return SOON") · #84-D1 successor instrument.
Ruled-but-unenacted lives in its own ledgers/`_REVIEW-SIGNOFF.md`; this register must not annex it.

⚠ **FOUND AT THE #212 WRAP AND REPORTED, NOT REPAIRED:** `G18` (the G3 revisit — *"warn but lets return
to this soon, I dont want any loose ends"*) exists as a row in `knowledge/_state.json` and has **no row
here**, so the register has never carried it. It is recorded as closed in the store (`s163-D1`, #163).
⛔ **No row is added retroactively** — new rows enter only with a `closes_when` on the way in, and this
one is already closed; the honest act is to name the gap. The class — **register and store can disagree
and nothing joins them** — is written up in `notes/_MEMENTO-DECISIONS.md` § ★ #212, finding 3.

**The archive counterpart:** `knowledge/_BANKRUPTCY-ARCHIVE.md` — items there return only when
named, each gaining a row HERE (with `closes_when`) on the way back in.
