<!-- GEN-BRIEF BEGIN TITLE-GOVERNANCE · owner=machine · sha256=cec73511437f3da7dfac99cd487c5fb56808ee131a9a8836ab3d55f9e3a15b19 · writer=knowledge/gen_brief.py -->
# PM brief — lane `lane-2-apollo-charts` (Apollo charts)

> ⛔ **THIS FILE IS A DATED PERIOD RECORD, NOT A LIVE HOME.** It was minted at `2026-08-20T18:11:09+01:00` by `knowledge/gen_brief.py`.
> **The store stays the one live home** (`knowledge/_state.json`, `knowledge/_rulings.json`). ADR-0017 / [[write-once-principle-floated-192]]: nothing in this brief may be cited as the source of a live fact — re-ask the store.
> **Nothing generated here is a ruling.** Only `knowledge/_inscribe_ruling.py` writes `knowledge/_rulings.json`, and only on Dave's word.

| governance | value |
|---|---|
| ruling this brief serves | `s204-D1` item 4 (mint-time brief generation) |
| programme brief | `notes/_briefs/2026-08-19-207-w46-three-scoped-proposals-v1.md` § PROPOSAL 2 |
| generator | `knowledge/gen_brief.py` — run `python3 knowledge/gen_brief.py --regions` to see exactly what it overwrites |
| this artefact | `notes/_briefs/2026-08-20-210-wave4-heavy7-fanout-brief-v1.md` |
| lane record | `knowledge/_lanes.json` → `lane-2-apollo-charts` · state `active` |
| lane born | #20 · 2026-07-28 (M-codes retired at the split) |
| lane until | born blocked, UNBLOCKED #25 (lane 1 landed) — lands when DV-J1/DV-J2 + the §C·1 strands ship (keys minted #26, Dave: J = Job; was ex-M4a/ex-M4b) |
| repo HEAD at mint | `9c00e94 after #210 2026-08-20 — the generated _ASSERTIONS.md mirror re-derived off the re-based ASSERT-009` |

**Lane sequence, as the lane record has it** (state is the record's word, not a reading of it):

- `landed` — DV-J2 — chart-table-toggle accretion, SCATTER HALF (was ex-M4b)
- `superseded` — DV-J2b — sparkline toggle markup + CSS (JS already injected, dormant)
- `landed` — DV-J1 — table-idiom unification (was ex-M4a)
- `queued` — §C·1 strands (a)–(d) — chart expansion · wave 3 · templates/shells · enact window
<!-- GEN-BRIEF END TITLE-GOVERNANCE -->

<!-- GEN-BRIEF BEGIN THE-JOB · owner=human · sha256=NONE-HUMAN-OWNED · writer=none -->
## THE JOB — human-owned

WAVE 4: build the heavy 7 — the components #209's wave-3 divvy deliberately deferred (fanout brief line 35): **calendar · tree · cascader · carousel · qr-code · splitter · image-block**. Premise re-probed at #210 mint: none of the seven exists in `knowledge/snippets/` (grep count 0). Library goes 100 → 107 if all land.

Dave's word authorising this wave, #210 in chat: *"still loads of tokens … maybe we should do something heavier or long running."*

THREE LANES, conductor's divvy:
- **Lane A (Opus): calendar + tree** — the two structurally deepest (date grid semantics; recursive disclosure).
- **Lane B (Opus): cascader + splitter + qr-code** — cascader relates to tree but is a selection control; splitter is an interaction pattern; qr-code's matrix must be a REAL encoding rendered as SVG rects, never an invented texture (state the encoded string in the specimen prose).
- **Lane C (Sonnet): carousel + image-block** — the presentational pair.

Each lane: `knowledge/snippets/<Name>.reference.html` + `knowledge/components/<name>.meta.json`, NEW FILES ONLY, per the wave-3 Lane A precedent (receipt `notes/_receipts/2026-08-20-209-wave3-laneA-fintech-rows.md` — read it for the claim-table form and the leading-trim probe). Everything PROPOSED, nothing registered, nothing promoted.
<!-- GEN-BRIEF END THE-JOB -->

<!-- GEN-BRIEF BEGIN PREMISE-TABLE · owner=machine · sha256=0efd95b8f021c622866b04054d2500f40369ea7c177166108db104105c44976b · writer=knowledge/gen_brief.py -->
## PREMISE TABLE — every row was RE-MEASURED at mint

⛔ **No row carries a summary word.** Each row prints the COMMAND, the RETURN CODE, the TIMESTAMP and the probe's own last line VERBATIM. A row a reader cannot re-run is a claim, not a measurement (`s182-D1`, [[measure-dont-convert-units]]). Read the rc; do not read a mood into it.

Population: every probe in `knowledge/_probe_registry/manifest.jsonl` — probes whose `environment` is `sandbox` were RUN; every other probe is a DECLARED, NOT-RUN row.

| probe | command | rc | timestamp | wall | the probe's own last line |
|---|---|---|---|---|---|
| `P-1` | `python3 knowledge/_probe_registry/probe_meta_schema.py --check` | `0` | `2026-08-20T18:11:10+01:00` | 0.21s | PROBE P-1 — findings=0 |
| `P-2` | `python3 knowledge/_probe_registry/probe_dup_ids.py --check` | `0` | `2026-08-20T18:11:10+01:00` | 0.18s | PROBE P-2 — findings=0 |
| `P-3` | `python3 knowledge/_probe_registry/probe_dangling_var_pixel.py --check` | `NOT RUN AT MINT` | `2026-08-20T18:11:09+01:00` | — | NOT RUN AT MINT — environment `sandbox-render`. This probe cannot be asked in a plain shell; see `s204-D1` item 5 (the CI pixel leg). A DECLARED GAP, never an omission. |
| `P-4` | `python3 knowledge/_probe_registry/probe_premise_store.py --check` | `1` | `2026-08-20T18:11:10+01:00` | 0.11s | PROBE P-4 — findings=2 |
| `P-5` | `python3 knowledge/_probe_registry/probe_stale_figure.py --check` | `0` | `2026-08-20T18:11:10+01:00` | 0.29s | PROBE P-5 — findings=0 |
| `P-6` | `python3 knowledge/_probe_registry/probe_input_trim_enactment.py --check` | `NOT RUN AT MINT` | `2026-08-20T18:11:09+01:00` | — | NOT RUN AT MINT — environment `sandbox-render`. This probe cannot be asked in a plain shell; see `s204-D1` item 5 (the CI pixel leg). A DECLARED GAP, never an omission. |

**How to read an rc**, in this repo's ruled vocabulary: `0` the probe ran and reported `findings=0` · `1` the probe ran and MEASURED something · `77` COULD-NOT-ASK (`s193-D1`, `knowledge/_could_not_ask.py`) — the probe could not reach its input and said so; that is a third verdict, not a pass and not a failure.
⚠ A green premise table means THESE PROBES RAN. It does not mean the tree is clean [[green-tests-cannot-see-scope]] — every probe's `blind` field in the manifest names what it cannot see, and free hunting is still owed.
<!-- GEN-BRIEF END PREMISE-TABLE -->

<!-- GEN-BRIEF BEGIN OPEN-ITEMS · owner=machine · sha256=14902a5365cc30682bac7de1c84c815137d6b6530a3c5cd6e65af9e3a110bbac · writer=knowledge/gen_brief.py -->
## OPEN ITEMS — read from `knowledge/_state.json` at mint

Counts are GENERATED, never typed: **91 items total · 63 live · 58 open · 1 blocked · 4 parked**, measured at `2026-08-20T18:11:09+01:00`.

| id | owner | state | condition | title |
|---|---|---|---|---|
| `G1` | dave | open | stated | Worklist-index cap DOFIRST_INDEX_TK_MAX = 700 (_capture_gate.py:1403,… |
| `G10` | dave | open | stated | The "70%/95%" stray band (GM:36 |
| `G11` | dave | open | stated | DS-018 recessive value |
| `G12` | dave | open | stated | Charter §4b tone-of-voice temperature map, PROVISIONAL 2026-07-02… |
| `G13b` | dave | open | stated | menu-search combined glyph, PROVISIONAL 2026-07-16 (_ICON-GAPS.md; the… |
| `G14` | dave | open | stated | Icon-button dark bindings |
| `G15` | dave | open | stated | DV-D13 donut centre figure + st.visible[id]=true release wiring… |
| `G16` | dave | open | stated | The _proforma/_DATAVIZ-DECISIONS.md:567 enactment call (agent's, not… |
| `G17` | dave | open | stated | RAG status manifestation… |
| `G2` | dave | open | stated | TAPE_TO_BILL = 1.57 at n=2 (_capture_gate.py:371; RATIO_FIRM_N = 4 per… |
| `G4` | dave | open | stated | GM §C measured 191 > 150 warn cap (_capture_gate.py:2864,… |
| `G5` | dave | blocked | stated | Four advisory size caps as a set (_capture_gate.py:4843–4858 |
| `G6` | dave | open | stated | DEFER_STREAK = 6 (_gm_usage.py:353) + USAGE_HISTORY_BLOCKING = False |
| `G9` | dave | open | stated | ds-023 re-measurement programme |
| `W-01` | claude | open | UNCONDITIONED | ds-018 C2 follow-through |
| `W-02` | claude | open | UNCONDITIONED | dv-legend/dv-behaviour CEILING |
| `W-03` | claude | open | UNCONDITIONED | ds-012(b) gutter-relative plot area |
| `W-04` | claude | open | UNCONDITIONED | DV-D16 floating growth |
| `W-05` | claude | open | UNCONDITIONED | Instrument-fit remainder |
| `W-06` | claude | open | UNCONDITIONED | ds-016, UNRULED |
| `W-07` | claude | open | UNCONDITIONED | ds-017, UNRULED |
| `W-08` | claude | open | UNCONDITIONED | STILL OWED, unchanged, none superseded |
| `W-09` | claude | open | UNCONDITIONED | DELEGATION TOPOLOGY, UNSCOPED |
| `W-0b` | claude | open | UNCONDITIONED | ★★ ENCODE BEFORE THE WAVE |
| `W-0c` | dave | open | UNCONDITIONED | NEXT BUILD CANDIDATES |
| `W-0d` | dave | open | UNCONDITIONED | ✅ THE #67 ENACT WAVE |
| `W-10` | claude | open | UNCONDITIONED | ✅ PER-GATE TEST PLAN |
| `W-11` | claude | open | UNCONDITIONED | THE 2c-ROLL / INDEX-VOCABULARY DEADLOCK |
| `W-12` | claude | open | UNCONDITIONED | THE #57 1b DOSSIER |
| `W-13` | claude | open | UNCONDITIONED | /tmp RUNBOOK EXPOSURE, UNFIXED |
| `W-14` | dave | open | UNCONDITIONED | ⬛ DAVE'S FOUNDING PRINCIPLE |
| `W-15` | dave | open | UNCONDITIONED | LEDGER § ★ #59 |
| `W-16` | dave | open | UNCONDITIONED | UNHOMED PAIR, copied up at the #78 2c EXIT CHECK |
| `W-17` | claude | open | stated | Memento close-out: rebuild parts 4-5 (GM archive, rolls retired, boot shrink) |
| `W-34` | dave | parked | stated | Apollo-on-Claude architecture brief awaits Dave's sitting (5 decisions) |
| `W-35` | claude | open | stated | #194 divvy plan for parallel windows (sole-committer rule) |
| `W-38` | dave | open | stated | Size-ramp + per-theme size modes proposal (FLOATED, Dave's instinct, #200) |
| `W-41` | dave | open | stated | #203 delegated-wrap brief (DO-NOT-RULE list + session facts for the Opus wrap sub) |
| `W-42` | claude | open | stated | #204 PM-topology trial brief (Fable judgment-only; Opus build-PM + adversarial verifier-PM) - ruled s203-D2 |
| `W-43` | claude | open | stated | #204 build-PM brief (four build lanes + lane-1 CI repair, under the s203-D2 PM-topology trial) |
| `W-44` | claude | open | stated | Mechanisation item 1 (s204-D1, BUILD NEXT): schema d claim/challenge JSONL + generated join + evidence linter |
| `W-45` | claude | open | stated | Mechanisation item 2 (s204-D1, BUILD NEXT): verifier probe registry + twice-caught promotion rule |
| `W-46` | claude | open | stated | Mechanisation items 3/4/5 scope-and-plan lane (s204-D1 - scope only, never build) |
| `W-47` | claude | open | stated | #204 delegated-wrap brief (session facts + DO-NOT-RULE list for the Opus wrap sub) |
| `W-48` | claude | open | stated | The verifier probe registry (built #206 under W-45): manifest + caught ledger + twice-caught promotion rule |
| `W-49` | claude | open | stated | #206 W-45 build receipt + claim table (notes/_claims/206-w45-claims.jsonl) |
| `W-50` | claude | open | stated | #206 W-45 build-PM brief (conductor-minted) |
| `W-51` | dave | open | stated | #207 addendum: Dave's critique of the #206 record (promotion vocabulary open; candidature homed) |
| `W-52` | claude | open | stated | #207 W-46 scope-PM brief (conductor-minted) |
| `W-53` | dave | open | stated | #207 W-46 three scoped proposals (items 3/4/5) — returning to Dave |
| `W-54` | claude | open | stated | #207 delegated-wrap brief (conductor-minted) |
| `W-55` | claude | open | stated | #185 Memento close-out plan (the PLAN DOCUMENT itself, conductor-minted row) |
| `W-56` | claude | open | stated | #208 delegated-wrap brief (conductor-minted, homed by the wrap sub) |
| `W-57` | claude | open | stated | gen_brief.py BUILT (W-46 proposal 2) + its first-drive demo brief |
| `W-58` | dave | parked | stated | payment-card-visual needs an INTENT word - parked #209, follow-up owed |
| `W-59` | claude | open | stated | rename the 5 ledgered local-var collisions to component-local names - the class fix behind Dave's #209 fork sanction |
| `W-62` | claude | open | stated | #209 wave-3 fan-out brief (gen_brief FIRST PRODUCTION MINT) + the three lane receipts |
| `W-63` | dave | open | stated | wave-3 NINE components BUILT PROPOSED-NOT-RULED - Daves eye owed (incl. two existence questions) |
| `W-64` | dave | open | stated | Dave's eye on the two #209 EXISTENCE questions - the side-by-side review page is the surface |
| `W-65` | dave | parked | stated | transaction system forensic revisit - molecule (transaction-row) to ledger organism, PARKED on Dave's word #210 |
| `W-66` | dave | open | stated | two #210 spacing fixes PROPOSED - Time-picker label descender clearance (4px->8px) and Data-grid state switcher margin (0->28px) |
| `W-67` | dave | parked | stated | FLOATED: minimum spacing rule for text collisions where line-height trim is active (real or padding-faked line-height) |
| `W-70` | dave | open | stated | The four progressbar-improvising snippets: do they CONSUME Meter? (named as future work by the #210 impacts memo, deliberately unscoped) |

### DECLARED DEBT — 19 item(s) are `condition: UNCONDITIONED`

These are the frozen legacy set: items opened without a stated close condition. They are PRINTED, never omitted — a declared gap passes, a silent one fails. An agent may not invent Dave's close conditions.

`W-01` · `W-02` · `W-03` · `W-04` · `W-05` · `W-06` · `W-07` · `W-08` · `W-09` · `W-0b` · `W-0c` · `W-0d` · `W-10` · `W-11` · `W-12` · `W-13` · `W-14` · `W-15` · `W-16`
<!-- GEN-BRIEF END OPEN-ITEMS -->

<!-- GEN-BRIEF BEGIN DO-NOT-RULE · owner=machine · sha256=62090f6d9ec98dcdbb6c674efbbb4318d549b146e6bc48ecb92f00a5ffa6143d · writer=knowledge/gen_brief.py -->
## DO-NOT-RULE — generated half

⛔ **`by: Dave` IS NOT USED AS A FILTER, and that is a correction to `s204-D1`'s own item-4 wording.** Measured at mint over `knowledge/_rulings.json`: **Dave=211** across 211 rulings. A field with one value selects everything and is therefore not a filter (#207 finding (b)).

The two generated sources are:

**1 · Store items `state=open` AND `owner=dave` — 26 item(s):**

| id | condition | title |
|---|---|---|
| `G1` | stated | Worklist-index cap DOFIRST_INDEX_TK_MAX = 700 (_capture_gate.py:1403,… |
| `G10` | stated | The "70%/95%" stray band (GM:36 |
| `G11` | stated | DS-018 recessive value |
| `G12` | stated | Charter §4b tone-of-voice temperature map, PROVISIONAL 2026-07-02… |
| `G13b` | stated | menu-search combined glyph, PROVISIONAL 2026-07-16 (_ICON-GAPS.md; the… |
| `G14` | stated | Icon-button dark bindings |
| `G15` | stated | DV-D13 donut centre figure + st.visible[id]=true release wiring… |
| `G16` | stated | The _proforma/_DATAVIZ-DECISIONS.md:567 enactment call (agent's, not… |
| `G17` | stated | RAG status manifestation… |
| `G2` | stated | TAPE_TO_BILL = 1.57 at n=2 (_capture_gate.py:371; RATIO_FIRM_N = 4 per… |
| `G4` | stated | GM §C measured 191 > 150 warn cap (_capture_gate.py:2864,… |
| `G6` | stated | DEFER_STREAK = 6 (_gm_usage.py:353) + USAGE_HISTORY_BLOCKING = False |
| `G9` | stated | ds-023 re-measurement programme |
| `W-0c` | UNCONDITIONED | NEXT BUILD CANDIDATES |
| `W-0d` | UNCONDITIONED | ✅ THE #67 ENACT WAVE |
| `W-14` | UNCONDITIONED | ⬛ DAVE'S FOUNDING PRINCIPLE |
| `W-15` | UNCONDITIONED | LEDGER § ★ #59 |
| `W-16` | UNCONDITIONED | UNHOMED PAIR, copied up at the #78 2c EXIT CHECK |
| `W-38` | stated | Size-ramp + per-theme size modes proposal (FLOATED, Dave's instinct, #200) |
| `W-41` | stated | #203 delegated-wrap brief (DO-NOT-RULE list + session facts for the Opus wrap sub) |
| `W-51` | stated | #207 addendum: Dave's critique of the #206 record (promotion vocabulary open; candidature homed) |
| `W-53` | stated | #207 W-46 three scoped proposals (items 3/4/5) — returning to Dave |
| `W-63` | stated | wave-3 NINE components BUILT PROPOSED-NOT-RULED - Daves eye owed (incl. two existence questions) |
| `W-64` | stated | Dave's eye on the two #209 EXISTENCE questions - the side-by-side review page is the surface |
| `W-66` | stated | two #210 spacing fixes PROPOSED - Time-picker label descender clearance (4px->8px) and Data-grid state switcher margin (0->28px) |
| `W-70` | stated | The four progressbar-improvising snippets: do they CONSUME Meter? (named as future work by the #210 impacts memo, deliberately unscoped) |

**2 · Rulings carrying a non-empty `open` field — 18 of 211:**

| ruling | ruled | what is still open, in the ruling's own words |
|---|---|---|
| `s142-D1` | #142 | tooltip.tip unruled; enactment (binds into metas + DTCG deferral updates) NOT in this ruling - #143 |
| `s143-D1` | #143 | the amount-display.sign colour VALUES (rag.success/rag.error rungs) are not adjusted by this ruling - the a11y adjustment is OPEN, residual to #144 |
| `s144-D1` | #144 | ["CLOSED BY s145-D1 (Dave, #145) - the name is rag/<severity>-ink; minted rag/error-ink + rag/success-ink. ORIGINAL TEXT, kept: RUNG NAME UNRULED - rag.<hue>-text vs rag.<hue>-ink. Precedent: rag.text.on-information was minted at s131-D1 as a severity-specific ink slot, so minting an ink rung has form. Dave's.", "NO DARK 'SELECTED ROW' TOKEN EXISTS in knowledge/tokens/ - light has the full set;… |
| `s145-D1` | #145 | ['THE SUCCESS-INK LEG HAS NO BINDING SITE. amount-display.sign\'s enum is ["none","negative"] - there is NO positive value (#143 finding 5, never closed). rag/success-ink is minted and consumable but nothing consumes it yet. Dave\'s to rule: add a positive enum value, or leave the rung ahead of its consumer.', "CARRIED UNCHANGED FROM s144-D1, not touched by this ruling: the dark 'selected row' … |
| `s146-D1` | #146 | ['full 110-step _build_all.py run never driven end-to-end this session (no --range/--resume; call-wall) - routes proven by check_routes, steps proven standalone', "_validate_kg.py freshness check observed FLAKY: 2 red runs (14 metas 'DRIFTED') then 8+ green, cause UNATTRIBUTED; hash-seed ruled out across 5 seeds; disk 85% with ENOSPC history is the suspect, UNPROVEN", "gen_snippet_tokens.py wri… |
| `s149-D1` | #149 | ["dark-mode red-text policy P1/P2/P3 from v2 - unruled, narrowed by (2)'s dark mark pick", "v3's D4-a glyph/bare-role follow question - MOOT for mono (fill stays put) but s130-D4 still names #B92F1E for any non-mono consumer", "v4's reach question: radio dot / switch / indeterminate dash - does 'marks' cover them", 'box border: rung or #F6604C (v3 D5-a)'] |
| `s151-D1` | #151 | ['green (success) leg: the monetary green analog - values unminted, presumed to follow the same background-keyed fork', "switch / indeterminate dash: presumed covered by 'atoms' - read back for confirmation, not yet Dave's word", 'box border: rung or #F6604C (v3 D5-a) - carried, untouched', "gate vocabulary design for 'colour alone must not carry meaning' - proposal owed to Dave this session"] |
| `s151-D2` | #151 | ['hover wash symmetry: light #F0F0F0 vs dark #232323 predate this tint-symmetric framing - unexamined, not ruled', 'the s151-D1 open items carry unchanged (green leg, switch/dash read-back, box border)'] |
| `s151-D3` | #151 | ['green/success-ink background-keyed scope: proposed, put to Dave, NOT yet answered - do not launder into a ruling', 'star 1.66 root cause verification before enacting (2)', 'carried: box border, hover-wash scoping/symmetry, Chart-bar/Reorder gate gap, err-msg class vs two-red law, neutral-ramp seat of the s151-D2 note'] |
| `s152-D1` | #152 | ["the exact remedy shape (skip vs re-key against the painted ancestor background) is the implementer's, within the ruled constraint", 'whether any other snippet in the 75 hits the same class - unmeasured'] |
| `s154-D1` | #154 | ['the derived cap itself (D4 (a)) is untouched - leanness pressure on future banners stands', 'whether the analogous 2d delta-stack check shares the class at LATEST+2 minimum - unexamined this window'] |
| `s155-D1` | #155 | ['the two green hex values - CLOSED by the #155 amendment above: #137F3C-on-white / #66CC8D-else, resolved by Dave via s144-D1; no picker needed', 'whether success/positive monetary values are the only green text seat, mirroring the red monetary rider - assumed yes by symmetry, not separately confirmed'] |
| `s157-D1` | #157 | ['no rendered specimen carries sign=positive yet - the showroom/snippet seat is unbuilt; the bind resolves but nothing consumes it visually', 's143-D1(B) a11y colour-VALUE adjustment (residual #144) still applies to both sign legs'] |
| `s157-D2` | #157 | ["palette NAMES are Dave's (mono / legacy / console-supercharge are placeholders)", 'whether the gate verifies ratified override files in place (ADD-never-trim preserved) or the overrides become generated - migration mechanics to be priced at #158', "s157-D1 note: Dave approved the mono green seat in-window ('for mono it's perfect'); the none-unbound delta stands unvetoed"] |
| `s158-D1` | #158 | ["DECLARED DIFF, the only one, and it is NOT a hand-edit: supercharge --form-background-pressed / --chip-pressed read #524842 on disk, #AA9B92 generated. PROVENANCE FOUND, not guessed - #524842 is warm/8, the value the light leg of form/background/pressed had when it aliased color/neutral/8 (commit 43cb3dd, ADR-0014 build, 2026-07-22, generated output). s151-D2 re-aliased that light leg to colo… |
| `s158-D2` | #158 | ["'negative' is NOT re-keyed and this is DECLARED, not overlooked: it still binds rag.error. The symmetric move to rag.error-ink is strongly implied by s151-D1 (which names rag/error-ink as the red TEXT/atom fork), but s157-D1 states 'negative: rag.error unchanged' as an enacted verdict of Dave's, so re-keying it would be ruling on his behalf. OPEN ITEM FOR DAVE - the negative seat's canonical … |
| `s158-D3` | #158 | ['The gate proves the address EXISTS, never that it is the RIGHT rung (its own declared blind spot). No specimen was rendered this session, so the VISUAL consequence of the re-key is UNPROVEN - same priced TODO s158-D2 carries.', "Both seats now sit on MONO-ONLY rungs. What a NON-MONO theme renders for coloured monetary text is still unruled - the palette files declare the -ink absence explicit… |
| `s158-D4` | #158 | ["Palette NAMES are still Dave's - console-supercharge.json says so on its own face (FILE NAME IS A PLACEHOLDER).", 'The 36 hexes were never re-rendered this session: the byte-identical canon.css proves the EMISSION is unchanged, not that any theme was looked at. No visual re-check was performed.'] |

⚠ **THIS LIST IS NOT COMPLETE AND CANNOT BE.** It sees two stores. It cannot see memory hooks, a ruling Dave made in chat that is not yet inscribed, or a lane-specific do-not-rule item nobody has written into a store. That is what the human-appended block below is for — and a generated list that silently loses an entry is worse than a hand list, because nobody notices the gap.
<!-- GEN-BRIEF END DO-NOT-RULE -->

<!-- GEN-BRIEF BEGIN DO-NOT-RULE-APPEND · owner=human · sha256=NONE-HUMAN-OWNED · writer=none -->
## DO-NOT-RULE — human-appended half

*The generated half above sees two stores. Everything else goes here: the lane-specific items, the questions already put to Dave, the vocabulary calls, the choices a sub must return rather than settle. HUMAN-OWNED — carried byte-for-byte across re-mint.*

- **Every fintech/domain semantic is PROPOSED, never decided** (the Kpi-tile precedent `s182-D2`; wave-3 Lane A form).
- **No colour is invented anywhere**: existing tokens only; mono on all indicator forms; the two-red law (`s151-D1`) and mono error ink camp (`s149-D1`) untouched; no RAG on anything meter-like.
- **The leading-trim block is the CURRENT one** — byte-identical to `Command-palette.reference.html` line 36 (probe form in wave-3 Lane A receipt claim 4).
- **No `intent` field** on any meta (`W-58` parked). **No registration**: `CATEGORIES`, `MIGRATED_SNIPPETS`, `component-types.json`, canon.css, `_rulings.json`, git — all conductor's/Dave's.
- **qr-code**: the matrix must be a real QR encoding (state the encoded string); no invented texture. If a genuine encoding cannot be produced and verified in-lane, REFUSE that member loud and named — a plausible-looking fake is the #202 defect at its worst.
- **calendar vs Date-picker**: Date-picker EXISTS — calendar is the standalone month-grid organism, not a re-draw of Date-picker's popover; borrow its atoms where they fit and state the relationship in the meta as PROPOSED.
- **cascader vs Tree/Multi-select**: state the relationship in the meta as PROPOSED, do not adjudicate overlap (the sidebar-nav precedent — that adjudication is Dave's).
- **Width is the container's** (`s210-D3` for meters — apply the same discipline as convention): no fixed max-width baked into a molecule's own class; demo chrome legibly commented.
- **New titles/labels use type composites** (`.t-cm-*`/`.t-ed-*`); the debt figure (1,097) may not grow.
- **Icons**: byte-matched from `knowledge/assets/icons/` only, never drawn (wave-3 claim-14 form).
<!-- GEN-BRIEF END DO-NOT-RULE-APPEND -->

<!-- GEN-BRIEF BEGIN FENCES-ENVIRONMENT · owner=machine · sha256=758c6626c2369cbe7349a8bbb82901242d4937aea364061e73a0f3e1d2303c98 · writer=knowledge/gen_brief.py -->
## FENCES + ENVIRONMENT — extracted at mint

### Environment, measured

| fact | value | how it was taken |
|---|---|---|
| minted at | `2026-08-20T18:11:09+01:00` | the generator's clock |
| python | `3.10.12` | `sys.version.split()[0]` |
| platform | `linux` | `sys.platform` |
| repo root | `/sessions/quirky-brave-edison/mnt/UX-design` | resolved from `knowledge/gen_brief.py` |
| HEAD | `9c00e94` | `git rev-parse --short HEAD` (rc=0) |
| dirty paths | `0` | `git status --short` (rc=0) |

⚠ **Sandbox warts that bite every sub, replayed:** nothing survives a tool-call boundary (~45s wall) — chunk long builds; `/tmp` may be full, scratch in `/var/tmp`; `git checkout -- <path>` cannot restore a file on this mount (`git show HEAD:<path> > <path>` is the working revert); `rm` inside `.git` is denied, `mv` is not.

### Runbooks in the tree

| runbook | bytes | mtime |
|---|---|---|
| `knowledge/_RUNBOOK-capture-ritual.md` | 51376 | 2026-08-16T21:02:36 |
| `knowledge/_RUNBOOK-compose-from-canon.md` | 7598 | 2026-07-18T21:30:43 |
| `knowledge/_RUNBOOK-consult.md` | 7216 | 2026-08-15T14:06:38 |
| `knowledge/_RUNBOOK-context-gauge.md` | 69554 | 2026-08-16T18:36:00 |
| `knowledge/_RUNBOOK-criteria-contract.md` | 2407 | 2026-07-14T12:01:09 |
| `knowledge/_RUNBOOK-decision-audit.md` | 10821 | 2026-07-05T09:31:21 |
| `knowledge/_RUNBOOK-densify-adversarial.md` | 4724 | 2026-07-19T16:04:26 |
| `knowledge/_RUNBOOK-dream-pass.md` | 8856 | 2026-08-16T13:09:24 |
| `knowledge/_RUNBOOK-external-claims.md` | 1431 | 2026-08-06T18:05:19 |
| `knowledge/_RUNBOOK-gated-component.md` | 4232 | 2026-06-30T07:42:58 |
| `knowledge/_RUNBOOK-git-commit.md` | 16253 | 2026-08-19T18:49:46 |
| `knowledge/_RUNBOOK-onboard-code-library.md` | 3922 | 2026-06-22T14:09:07 |
| `knowledge/_RUNBOOK-parallel-conductor.md` | 13596 | 2026-08-18T21:30:11 |
| `knowledge/_RUNBOOK-reconcile-dark-tokens.md` | 2458 | 2026-06-20T13:30:28 |
| `knowledge/_RUNBOOK-render-verify.md` | 26868 | 2026-08-17T07:44:51 |
| `knowledge/_RUNBOOK-review-doc.md` | 2456 | 2026-08-01T13:23:09 |
| `knowledge/_RUNBOOK-toolkit-tranche.md` | 7814 | 2026-08-15T13:22:24 |

### ⛔ lines extracted from the declared runbook subset

Glob: `_RUNBOOK-git-commit.md · _RUNBOOK-parallel-conductor.md · _RUNBOOK-render-verify.md · _RUNBOOK-capture-ritual.md` — a DECLARED subset of the 17 runbooks above, not all of them. Each line is quoted VERBATIM with its `path:line` so it can be re-read in place; the per-runbook count says how many were found and how many are shown.

**`knowledge/_RUNBOOK-git-commit.md`** — 3 ⛔ line(s) found, 3 shown:

- `knowledge/_RUNBOOK-git-commit.md:85` — ⛔ **AND THE MSGFILE HEADLINE MUST NOT CARRY A SESSION PREFIX OF ITS OWN** — neither
- `knowledge/_RUNBOOK-git-commit.md:94` — 4b. *(Optional sweep — dream-pass P8, 2026-07-26. ⛔ **CORRECTED #41 — this step used to route the job
- `knowledge/_RUNBOOK-git-commit.md:138` — - **`_to_delete/` is gitignored.** ⛔ **CORRECTED #41 — the old text here read *"the bridge can't empty

**`knowledge/_RUNBOOK-parallel-conductor.md`** — 6 ⛔ line(s) found, 6 shown:

- `knowledge/_RUNBOOK-parallel-conductor.md:65` — ⛔ **READ THE FENCE FIRST, BECAUSE IT IS DAVE'S CONDITION AND NOT A CAVEAT.** His concern, verbatim:
- `knowledge/_RUNBOOK-parallel-conductor.md:69` — exactly as ruled. ⛔ **No existing check may be removed, relaxed, skipped, narrowed or "simplified" by
- `knowledge/_RUNBOOK-parallel-conductor.md:87` — - **(b) VERIFICATION IS TARGETED.** Prove **the seam THIS deliverable creates**. ⛔ Not *"verify
- `knowledge/_RUNBOOK-parallel-conductor.md:91` — control [[mutation-tests-the-clause-not-the-feature]]. ⛔ **No checkers checking checkers beyond
- `knowledge/_RUNBOOK-parallel-conductor.md:120` — name in its report. ⛔ **Explicitly NOT a new gate** (`s172-D3`): this is the cheapest `s129-D5`
- `knowledge/_RUNBOOK-parallel-conductor.md:126` — 0. ⛔ **NEVER run `git checkout`/`git restore` on a path while the tree carries uncommitted work**

**`knowledge/_RUNBOOK-render-verify.md`** — 2 ⛔ line(s) found, 2 shown:

- `knowledge/_RUNBOOK-render-verify.md:50` — ⛔ **THE `<dir>`→REPO ELEMENT ON THIS LINE AND LINE 42 IS SUPERSEDED — see § SYMLINK FARM (#138) below.**
- `knowledge/_RUNBOOK-render-verify.md:150` — ⛔ **THIS RUNBOOK WAS DECLARED DEAD BY A SESSION THAT NEVER OPENED IT — RE-VERIFIED WORKING #124.**

**`knowledge/_RUNBOOK-capture-ritual.md`** — 9 ⛔ line(s) found, 6 shown:

- `knowledge/_RUNBOOK-capture-ritual.md:22` — (~50–52 at today's 8–10 point wraps; `_RUNBOOK-context-gauge.md` § ds-023). ⛔ **60 IS WHERE THE WRAP
- `knowledge/_RUNBOOK-capture-ritual.md:144` — corpus runs at **3.53 bytes/token**, not the customary 4 — its ★ ⚠ ⛔ · — load makes it ~13% denser,
- `knowledge/_RUNBOOK-capture-ritual.md:160` — ⛔ **THE OPS FILE IS A MSGFILE — GIVE IT A UNIQUE NAME AND ASSERT IT EXISTS BEFORE THE MOVER READS IT.**
- `knowledge/_RUNBOOK-capture-ritual.md:203` — ⛔ **A RETRACTED CARRY IS STRUCK, NEVER RE-TYPED — ruled `s183-D1` (dream pass 8, P2).**
- `knowledge/_RUNBOOK-capture-ritual.md:213` — ⛔ **AND THE RETRACTION MUST CITE ITS RECEIPT — ruled `s188-D2` (#188), a STRENGTHENING
- `knowledge/_RUNBOOK-capture-ritual.md:358` — - ⛔ **ABSENT IS LEGAL, AND ABSENCE IS NEVER DEFAULTED.** A wrap with no sub figures — no subs,

### ⛔ WHAT THIS GENERATOR CANNOT SEE

It rules only as wide as what it reads [[gate-glob-scope-rule]]: `knowledge/_state.json`, `knowledge/_rulings.json`, `knowledge/_lanes.json`, `knowledge/_probe_registry/manifest.jsonl` and `knowledge/_RUNBOOK-*.md`. **Memory hooks live outside the repo entirely. A ruling made in chat and not yet inscribed is invisible. Anything a human knows and has not written into a store is invisible.** Treat every region below as a floor, not a ceiling.
<!-- GEN-BRIEF END FENCES-ENVIRONMENT -->

<!-- GEN-BRIEF BEGIN RETURN-CONTRACT · owner=human · sha256=NONE-HUMAN-OWNED · writer=none -->
## RETURN CONTRACT — human-owned

Each lane owes back, in its report: **(1)** file list with byte sizes; **(2)** a claim table in the wave-3 Lane A receipt form — every claim carries a re-runnable probe exactly as written and its verdict, false-probe warnings included; **(3)** what was DRIVEN in a real browser (headless Chromium, `goto("file://…")` only, light AND dark, screenshots looked at) with measured numbers, not assertions; **(4)** gate outputs VERBATIM (grid · snippets · a11y · descender-clip · type-composites before/after · meta schema · binds-resolve with the expected check-D declaration for unregistered snippets); **(5)** a receipt file `notes/_receipts/2026-08-20-210-wave4-lane<X>-*.md` with a store doc-row minted at creation; **(6)** `$decisionsForDave` — every open design question named, none answered; **(7)** what stays UNPROVEN, declared not smoothed. NO commits — the conductor commits; NO store rows beyond the receipt doc-row (the conductor mints the wave row).
<!-- GEN-BRIEF END RETURN-CONTRACT -->
