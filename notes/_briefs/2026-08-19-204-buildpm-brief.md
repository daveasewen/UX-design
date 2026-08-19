# Brief — #204 BUILD-PM (Opus), PM-topology trial under `s203-D2`

*Cut by the FABLE conductor at #204, 2026-08-19, off first-hand probes (not the banner).
Read `_BRIEF-204-pm-topology-trial-2026-08-19-v1.md` §"The topology under trial" first —
you are the BUILD-PM it describes. Dave ruled the wave scope in chat this session:
"CI repair + P2 gaps".*

## Your seat

You orchestrate and build; you do NOT judge. You may spawn Opus worker subs if the Agent
tool is available from your seat; if it is not, run the lanes serially yourself and DECLARE
that the sub-orchestration limb of the trial was unavailable — never simulate it.

## STEP-0 — MANDATORY PREMISE TABLE, PER LANE, BEFORE ANY BUILD

Every factual claim in this brief gets a row: claim · probe you ran · CONFIRMED/FALSE.
#203 proved a brief's premise can be five weeks stale for six lanes at once. If a premise
is FALSE, pivot in-fence to measurement and findings — do not build on it.

## LANE 1 — CI repair (get the gates job green on the survey step)

CI run 32239404300 on head `3a88777`: render GREEN, gates RED. THE FULL FAILURE SET (4):

- `[3]` `python3 knowledge/tokens/_build_blast_radius.py --check` → exit 1, "2 file(s) out of sync with a fresh compute()"
- `[13]` `python3 knowledge/_capture_gate.py --selftest` → exit 1
- `[110]` `python3 knowledge/_build_graph_mention_map.py --check` → exit 1
- `[114]` `python3 knowledge/_gen_chain.py --selftest` → exit 1, "materially smaller than GOOD-MORNING.md (21,237 vs 51,204 tape, <40%)"

Working hypothesis (VERIFY, don't trust): regeneration debt from #203's nine new components
landing without `_build_all.py`. Reproduce each locally first, fix the regeneration, re-run
the exact CI command. ⛔ HAZARDS:
- NEVER run `_build_all.py` single-process (~49s vs the ~45s call kill; a partial run
  strands the tree — docstring lines 5–21). Use its documented `--range/--resume` chunking
  ONLY if a full pass is genuinely required; prefer targeted regeneration per failing step.
- `pip install tiktoken --break-system-packages` first (already installed this session).
- If a fix requires PICKING a threshold (e.g. the `[114]` <40% ratio) or any judgment call:
  STOP on that item, record it in the claim table as UNPROVEN with the decision named.
  The `[114]` fail may be structural (GM grew at #203) — measure whether regeneration
  alone clears it before touching any constant. ⛔ Constants are not yours to move.

## LANE 2 — the 7 TRUE P2 gaps (Layer 1)

Source: `reviews/ITINERARY-STATUS-2026-08-19-v1.json` `$true_gaps` ∩ priority P2 —
probed first-hand by the conductor this session:

75 Popconfirm (Feedback & status) · 81 Footer (Layout) · 82 Grid/stack utilities (Layout) ·
91 Transaction/ledger row (Fintech) · 92 Statement/document row (Fintech) ·
93 Payment-card visual (Fintech) · 94 Coverage/runway bar (Fintech)

⚠ The #203 banner says "8 P2"; the JSON yields 7. Note it in the claim table; build off the JSON.

Per component, in order:
1. Step-0 probe: does a snippet/meta already exist (`ls knowledge/snippets/`)? Does the
   store rule on it (`python3 knowledge/_memento_search.py "<name>"` AND grep
   `knowledge/_rulings.json`)? Does it overlap an existing component (the Sidebar-nav-vs-
   Navigations class)? Record the probes.
2. Build following the #203 wave-3b pattern — receipts at
   `notes/_receipts/2026-08-19-203-wave3b-lane[G-L]-*.md` are the reference for shape:
   snippet + meta + four-theme cascade (mono · legacy · console · supercharge, test PER
   THEME) + registry entries (`MIGRATED_SNIPPETS`, `CATEGORIES`) + a four-theme review
   spread `reviews/REVIEW-204-<slug>-four-themes-v1.html`. ★ Specimens COPY approved
   artefacts, never re-draw from memory.
3. Anything Dave has not ruled ships marked PROPOSED in snippet header, meta and review
   page (the Kpi-tile precedent). Fintech rows especially: semantics are his.
4. Gates after each component and at close: `_validate_snippets`, `_validate_a11y`,
   `_validate_radius`, `_validate_coverage`, `_validate_icons` — record rc verbatim.
5. New docs get a store row at creation (`knowledge/_state.py` — the forgotten-document
   class) and go in `knowledge/_REVIEW-SIGNOFF.md`.

## FENCES (all standing, none waived)

- ⛔ DO-NOT-RULE: the two-red Stat-card/Kpi-tile seam · hit-area gate promotion ·
  the itinerary xlsx retirement · the segmented type-scale binding · Kpi-tile's status ·
  the 44-enforcement record split · any threshold/constant · anything tagged DAVE'S.
- ⛔ NEVER write `knowledge/_rulings.json` (only the conductor's `_inscribe_ruling.py` may).
- ⛔ NO commits, NO push, NO `git checkout` of any path (the #202 specimen ban).
- ⛔ NEW FILES ONLY for components; existing files touched only where the runbook pattern
  requires (registries, generated outputs) — list every touched path in the claim table.
- ⛔ Do not touch the frozen `reviews/ITINERARY-2026-07-14-*` files, `GOOD-MORNING.md`,
  `_CHAIN.md`, `_LIVE-STATE.md`, memory stores.
- `s202-D3`: any question you surface as OPEN must carry the store search that failed to
  settle it (query + hits verbatim).
- Two-red law (`s151-D1`) and mono error ink camp (`s149-D1`) are FIRM — new components
  conform, never reinterpret.

## OUTPUT — the claim table (your whole deliverable to Fable)

Write `notes/_receipts/2026-08-19-204-buildpm-claim-table.md`: ONE row per claim —
`id | claim | evidence pointer (command + rc / file path) | PROVEN / MEASURED / CLAIMED / UNPROVEN`.
Every gate rc, every touched path, every premise-table verdict, every declared stop.
Plus per-lane receipts in `notes/_receipts/2026-08-19-204-*.md`.

## CONSEQUENCES / PITFALLS SECTION — MANDATORY (Dave #165)

End the claim table with what could bite: what you did not run, what a green cannot see,
what the verifier should attack first.

## Report your token spend and n= workers in your final message.
