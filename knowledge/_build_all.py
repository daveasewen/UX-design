#!/usr/bin/env python3
"""One-command rebuild of every derived view, in dependency order.

The generators must run in this order because later ones read earlier outputs:
  1. compliance/_build_compliance_kg.py      -> compliance/rules/, graph-index.json
                                                 (NOTE: this rewrites graph-index.json wholesale — any
                                                 verification{}/external_automatable_refs{} block from a
                                                 PRIOR run is gone after this step. Both must be rebuilt
                                                 fresh every run, in the order below.)
  2. tokens/_build_blast_radius.py           -> tokens/_blast-radius.json, _GRAPH-REPORT.md
  3. _build_xref_index.py                    -> _XREF-INDEX.json/.md   (needs 1 + 2)
  4. _build_review_queue.py                  -> _REVIEW-QUEUE.json/.md
  5. _build_dark_mode_audit.py               -> _DARK-MODE-AUDIT.json/.md (needs 2)
  6. _build_surface_contrast_audit.py        -> _TEXT-CONTRAST-AUDIT.json/.md (needs _contrast_utils)
  7. _build_indicator_contrast_audit.py      -> _INDICATOR-CONTRAST-AUDIT.json/.md (needs _contrast_utils)
  8. compliance/_build_verification_edges.py -> compliance/graph-index.json (verification block) + rules/*.json (verified_by)
                                                 (needs 1, 2 (blast-radius join), 6, 7 and the a11y gate — runs after all of them)
  9. compliance/_import_axe_rules.py         -> graph-index.json (external_automatable_refs) + rules/*.json
                                                 (needs 1 AND 8 — its "already wired" cross-check reads the
                                                 verification{} block, so it MUST run after step 8, not before.
                                                 Reads the vendored axe-core snapshot in compliance/_vendor/, no network.)
  10. _build_integrity.py                    -> _INTEGRITY-REPORT.md   (the gate; needs 3)

Run:  python3 knowledge/_build_all.py
Exits non-zero if EITHER gate fails: the integrity lint (step 8, any ERROR) or
the contrast audits (steps 6-7, any non-allowlisted token below its dark-mode
threshold). Both run to completion first so every report is fresh. This is the
single command to trust the knowledge base after editing metas or tokens.
"""
import subprocess, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
STEPS = [
    ("compliance knowledge graph", "compliance/_build_compliance_kg.py"),
    ("token blast-radius + graph report", "tokens/_build_blast_radius.py"),
    # #79 P6: _GRAPH-REPORT.md (+ its tokens/_blast-radius.json sibling) had NO reader —
    # write-only since 2026-06-18, an instrument without a consumer. --check recomputes
    # both outputs in memory and compares them BY CONTENT (never mtime) against what's on
    # disk. ⚠ Same limitation the codebase already accepts for _gen_chain.py's --check at
    # this position: the STEPS entry directly above just regenerated both files fresh in
    # this same process, so here --check can only prove compute() is DETERMINISTIC — it
    # cannot catch a report that drifted from source BETWEEN sessions (that needs a second
    # reader at the commit seam, out of scope for this add). Measured green 2026-08-02.
    ("token blast-radius + graph report — determinism/staleness check (#79 P6)",
     "tokens/_build_blast_radius.py", ["--check"]),
    ("token blast-radius + graph report selftest (#79 P6)",
     "tokens/_build_blast_radius.py", ["--selftest"]),
    ("guideline rules index (gate)", "guidelines/gen_rules_index.py"),
    ("runbook index (generated)", "gen_runbook_index.py"),
    ("standing-instructions reachability gate", "_validate_standing_instructions.py"),
    # Sibling to the above, and deliberately adjacent: that gate asks "is every standing
    # doc REACHABLE"; this one asks "is what we say still TRUE". A doc can be perfectly
    # reachable and perfectly wrong — which is how "the sandbox has no Univers" survived
    # 16 months while the fonts sat in the repo (Dave, 2026-07-18: "how do we fix this
    # permanently?"). Registry: _assertions.json.
    ("assertion veracity gate — claims that can rot", "_validate_assertions.py"),
    # #77 periphery: this selftest ALSO runs embedded in the gate step above (its __main__
    # runs selftest() before run() even without the flag), so it could already fail — but a
    # red was attributed to the GATE, not the instrument. Named arm per the _roll_state
    # precedent: a selftest not in STEPS is a gate that does not run. Measured green
    # standalone 2026-08-02 (EXIT=0) before wiring.
    ("assertion veracity selftest — verbs bite + registry well-formed (#77 periphery)",
     "_validate_assertions.py", ["--selftest"]),
    # Third sibling: reachable (above), true (above) — and now PROVENANCED. New notes/
    # dossiers must say who observed what, when, and at what standing (observed/inferred/
    # ruled/floated/standing) so a cold reader can weigh them without the authoring
    # session's context. Memento §4.1; rulings D1a/D2/D3 2026-07-26
    # (notes/_MEMENTO-DECISIONS.md). Repo-side only — the memory store is invisible to
    # gates BY RULING; wrap-time checks are `--wrap`, session-run, not wired here.
    ("capture/provenance gate — status+provenance on new notes+dossiers (Memento §4.1)", "_capture_gate.py"),
    ("capture/provenance selftest (Memento §4.1)", "_capture_gate.py", ["--selftest"]),
    # #79 P5: the counting path (cl100k exact fixtures), the cache (hit fidelity,
    # content-hash keying, corrupt-file robustness), and degraded-measurement honesty
    # (ds-025) all get bite-tested here -- the budget constants every wrap is graded
    # against sat on an UNBITTEN instrument (periphery inventory, 2026-08-02).
    # ✅ ARM C WAS RED FROM #79 AND IS CLOSED AT #80 -- RULED BY DAVE (#79-D1, *"make it
    # refuse"*, chosen over a louder estimate). count()'s crude-estimate fallback
    # (len(text)//4 on a tiktoken ImportError) now raises MeasurementRefused, loud AND
    # named. The change was PAIRED, as #79 said it had to be: the handler lives in
    # _capture_gate.py at the #53 floor call, so a refusal is reported as ONE named
    # failure instead of killing that 39+-check sweep ("a crash is not a fail").
    # ★ The seam itself is now tested, not just the two ends: _capture_gate.py::
    # selftest_gauge_refusal_seam() mutation-proves all three ways the pairing can rot
    # (handler removed / handler swallows / MeasurementRefused re-parented to
    # BaseException, which would let every `except Exception` keep compiling while
    # silently ceasing to catch). Each mutation bites with a DISTINCT named failure.
    ("gauge-tokens selftest -- counting path + cache + degraded-measurement honesty (#79 P5)",
     "_gauge_tokens.py", ["--selftest"]),
    # #77 (ruled Dave, R1–R4 — ledger § ★ #77): the roll-state MEASURER the roll-claim check
    # re-derives from at every --wrap. Its selftest proves the green control renders exactly,
    # every corrupted surface refuses NAMED, every OVER state bites. The measurer itself runs
    # at ritual time (its line is pasted into the banner); wired here so CI asks it — a
    # selftest not in STEPS is a gate that does not run (periphery inventory, 2026-08-02).
    ("roll-state measurer selftest (#77 T1)", "_roll_state.py", ["--selftest"]),
    # #78-D1 (P1): the commit seam itself — _git_commit.sh had no test and no runner while
    # being the seam every other check is delivered through (periphery inventory P1). The
    # harness runs the REAL script text in throwaway /tmp fixture repos (stubbed gate/chain/
    # spine-writer exits), pins the WARN/--wrap split, the lock dance, both T3 parse paths,
    # the #78-D3 `after #N` mid-session prefix, and the #78-D2 spine-writer consumer both
    # ways. Pure: never touches the real repo or .git. Measured green 2026-08-02 before wiring.
    ("commit-seam harness — _git_commit.sh fixture-repo arms (#78-D1 P1)",
     "_test_git_commit.py", ["--selftest"]),
    # M5 (brief §11, built 2026-07-28 #21): the hardened GM/LS mover the wrap ritual's
    # 2c/2d/2e moves route through. Its selftest is the proof its refusals FIRE — line-start
    # anchors · §A digest assert · imported caps (warn ≠ block) · no-op loud FAIL ·
    # all-or-nothing. The mover itself runs at ritual time, not in the build.
    ("GM/LS mover selftest — hardened move mechanics (M5)", "_gm_move.py", ["--selftest"]),
    # #23 (lane 1 step 2, ruled 2026-07-28): section-usage instrumentation. The selftest
    # proves the vocabulary refuses unregistered headings and the stratum probe FIRES;
    # the wrap-time probe itself lives in _capture_gate.py (--wrap), ADVISORY until O1′.
    ("section-usage instrumentation selftest (#23)", "_gm_usage.py", ["--selftest"]),
    # O1′ (ruled Dave 2026-07-28 #24, option-select ×4): lane records are DATA
    # (knowledge/_lanes.json); the LS §🛤 view is GENERATED between AUTO-LANES markers
    # (regenerate-always + determinism, the ADR-0013 ruling-4 shape); the selftest proves
    # every schema refusal FIRES (unknown state/field, dangling guard, stale block,
    # lane-order violation) + the routing-line contract. The wrap-time eager-line check
    # lives in _capture_gate.py::lane_routing_check (BLOCKING) and IMPORTS _gen_lanes.
    ("lane records — regenerate LS §🛤 view (O1′ #24)", "_gen_lanes.py"),
    ("lane records determinism check (O1′ #24)", "_gen_lanes.py", ["--check"]),
    ("lane records selftest — schema refusals + routing contract (O1′ #24)", "_gen_lanes.py", ["--selftest"]),
    ("cross-reference index", "_build_xref_index.py"),
    ("sutherland acceptance fixtures", "_build_sutherland_fixtures.py"),
    ("states-completeness probe (advisory)", "_build_states_probe.py"),
    # decision-graph runs FIRST so its parsed `_decision-graph.json` is fresh when the
    # _LIVE-STATE builder below consumes it to (re)generate the decision-node lifecycle
    # block (ADR-0007 part 2 — generation, not just the staleness gate).
    ("decision-graph — typed edges + conflict gate (advisory, ADR-0012)", "_build_decision_graph.py"),
    # #77 periphery: wired per the _roll_state precedent — the selftest existed and ran only
    # by hand. It is PURE (in-memory fixtures, no writes; __main__ short-circuits before
    # main()), so it sits safely between the builder above and the _LIVE-STATE consumer
    # below. Measured green standalone 2026-08-02 (EXIT=0) before wiring.
    ("decision-graph selftest — conflict gate bites on unresolved/open/orphan (ADR-0012, #77 periphery)",
     "_build_decision_graph.py", ["--selftest"]),
    # #78-D2: the spine-writer's selftest runs BEFORE the step that lets it write — splice
    # invariants, idempotency, named refusals, no-half-writes, mutation controls. Pure
    # (tempdir copies only; hashes the real spine before/after). Its blocking consumer
    # lives at the commit seam (_git_commit.sh, WARN/--wrap split); this STEPS entry is
    # so CI asks it too. Measured green 2026-08-02 before wiring.
    ("spine-writer selftest — splice invariants + no-half-writes (#78-D2)",
     "_build_live_state.py", ["--selftest"]),
    ("_LIVE-STATE staleness gate + lifecycle-block generation (advisory, ADR-0007)", "_build_live_state.py"),
    ("advisory signals — prose rules (advisory)", "_validate_advisory.py"),
    ("review queue", "_build_review_queue.py"),
    ("dark-mode coverage audit", "_build_dark_mode_audit.py"),
    ("text/icon contrast audit", "_build_surface_contrast_audit.py"),
    ("indicator/accent contrast audit", "_build_indicator_contrast_audit.py"),
    ("icon contrast delta — brand 4.5 vs 3 (advisory)", "_build_icon_contrast_delta.py"),
    ("dark-surface flatness gate", "_validate_dark_surfaces.py"),
    # ADR-0013 composition tier (2026-07-22): the RULE half of retrieval. Partial sync
    # fails loud on divergence (ruling 2 — manual regen preserves attribution); canon
    # components REGENERATE-ALWAYS then determinism-check (ruling 4 — snippet RULE-text
    # changes self-heal into canon; the --check catches non-idempotent generator bugs);
    # the ratchet makes local re-implementation of a registered partial a build failure.
    ("component-partials sync — AUTO-PARTIAL injection + contracts (ADR-0013)", "gen_component_partials.py", ["--check"]),
    ("component-partials selftest (ADR-0013)", "gen_component_partials.py", ["--selftest"]),
    # s121-D1: the FOURTH injection type — canon token-set atoms (alpha ramp, status-mark
    # map) distributed into standalone snippets/_proforma files. Closes the ds-018 C2
    # reachability class; the C2 gate below is promoted to --strict in the same session.
    ("token-set distribution sync — AUTO-TOKENS injection (s121-D1)", "gen_token_ramp.py", ["--check"]),
    ("token-set distribution selftest (s121-D1)", "gen_token_ramp.py", ["--selftest"]),
    # ADR-0015 (2026-07-23): behaviour partials — the dataviz interaction layer is ONE
    # hand-authored JS source injected between AUTO-BEHAVIOUR markers (sync rides the
    # partials --check above). This gate owns the PERFORMANCE CONTRACT on the source:
    # ≤16KB raw · no polling/network · single rAF-debounced resize · DEF-003 boundary.
    ("Behaviour contract gate — dv-behaviour size + banned patterns (ADR-0015)", "_validate_behaviour.py"),
    ("Behaviour contract selftest (ADR-0015)", "_validate_behaviour.py", ["--selftest"]),
    ("canon components — regenerate from snippets (ADR-0013 ruling 4)", "canon/gen_canon_components.py"),
    ("canon components determinism check (ADR-0013 ruling 4)", "canon/gen_canon_components.py", ["--check"]),
    ("partial re-implementation ratchet (ADR-0013)", "_validate_partials.py"),
    ("partial-ratchet selftest (ADR-0013)", "_validate_partials.py", ["--selftest"]),
    # Projection-sync gate (2026-07-21): snippets/tranches/canon literals must match the
    # token stores BY GENERATION. The tranches sat on pre-R-D20 Legacy error reds and
    # canon's .cn-button literals on pre-B-D values for a day+ because the projector only
    # ran manually and nothing checked — caught during Phase 0. This closes that hole.
    ("token projection sync — snippets/tranches/canon literals (gen_snippet_tokens)", "gen_snippet_tokens.py", ["--check", "--quiet"]),
    ("snippet gate", "_validate_snippets.py"),
    # Phase-0 theme layer (2026-07-21): the AUTO-THEMES cascade in canon.css must
    # regenerate byte-identically from tokens/themes/*.json + snippet manifests
    # (same spine principle as the token block — generated, so it cannot drift).
    ("theme cascade sync — [data-apollo-theme] layer (ADR-0011)", "canon/gen_theme_cascade.py", ["--check"]),
    # ADR-0014 (2026-07-22): selftests are WIRED so they cannot rot — the supercharge-empty
    # assertion sat stale-red for a day because --selftest only ran by hand.
    ("theme cascade selftest (ADR-0014)", "canon/gen_theme_cascade.py", ["--selftest"]),
    ("state-snap gate — opacity states snap to the active theme's ramp (ADR-0014)", "_validate_state_snap.py"),
    ("state-snap selftest (ADR-0014)", "_validate_state_snap.py", ["--selftest"]),
    ("radius gate — no hardcoded border-radius; shape is a theme flex slot (ADR-0010)", "_validate_radius.py"),
    ("showroom sync — generated component library (RULED 2026-07-21)", "gen_showroom.py", ["--check"]),
    ("showroom URL-rebase selftest — the srcdoc base-URL trap (2026-07-27)", "gen_showroom.py", ["--selftest"]),
    ("Legacy-colour leakage gate (Mono) — no Legacy-only colour in a Mono surface", "_validate_legacy_leak.py"),
    ("theme-provenance gate (ADR-0011/R-D19) — no foreign-theme hex in a Mono surface (advisory)", "_validate_theme_provenance.py"),
    ("token-tier gate (_STANDARDS.md §1)", "_validate_token_tiers.py"),
    ("icon-source gate", "_validate_icons.py"),
    ("a11y gate", "_validate_a11y.py"),
    # WIRED #116 (s114-D5): the target check was rebuilt MARKUP-DRIVEN, so it ships its
    # bite-test in the same pass — "every new gate ships one AND wires it". The clauses
    # are split DETECTION / DECORATION / REMEDIATION / HONESTY on purpose: #104's lesson
    # is that a mutation which only exercises detection never proves remediation. All 25
    # clauses were mutation-tested at #116; 16 mutations of _a11y_target.py, 16 killed.
    ("a11y target-measurement selftest (s114-D5)", "_validate_a11y.py", ["--selftest"]),
    # WIRED #119: #118 found the wiring seam — 29 validators on disk, 25 wired, 4 orphans,
    # each unwired for a DIFFERENT reason. Building is gated; wiring wasn't. This gate
    # asserts every _validate_*.py is in this list or exempt BY NAME with a reason.
    # 4 bites mutation-tested at #119 (both directions + stale/dangling exemption).
    ("wiring gate — no orphaned validators (#118 seam)", "_validate_wiring.py"),
    ("wiring gate selftest — 4 bites", "_validate_wiring.py", ["--selftest"]),
    # WIRED #119: pure oversight orphan from #118's table — green at both drives, zero risk.
    ("compose gate (orphan wired #119)", "_validate_compose.py"),
    # RE-WIRED #120: exempt as ROTTED since #118 — root cause was a drifted a11y.check()
    # call signature (3-tuple unpack vs the 6-tuple the s114-D5 rebuild returns), one-line
    # fix at _validate_screen.py:63, the only call site. Repaired + mutation-tested #120
    # (injected unguarded transition → named 2.3.3 FAIL, rc=1); exemption removed same pass.
    ("screen gate — compose+icons+a11y over fitness fixtures (re-wired #120)", "_validate_screen.py"),
    # WIRED #125 (s125-D2, Dave) — exempt as ENVIRONMENTAL since #120 on the grounds that the
    # chromium download was TLS-blocked in-sandbox. DISPROVEN by observation at #125: the
    # _RUNBOOK-render-verify.md recipe was followed literally, the headless-shell download
    # landed, chromium launched, and the validator ran and emitted output. The exemption had
    # read the installer's __dirlock/host-validation non-zero exit as a download refusal.
    # ⚠ TWO PRE-EXISTING DEFECTS FOUND IN THE VALIDATOR AT WIRING (the #125 wiring worker was
    # fenced to _validate_wiring.py + _build_all.py, so it could not repair them here):
    #   (1) its MEASURE parse() regex matched only rgba?(...), so a background Chromium
    #       serialises as color(srgb ...) — every color-mix() hover in canon.css — was skipped
    #       and treated as measured. White-on-#5F5F5F (6.4:1, a PASS) was reported as 1:1.
    #       ✅ FIXED LATER THE SAME SESSION by s125-D3: parse() reads color(srgb ...) AND
    #       REFUSES unreadable syntax by name (StateContrastParseError) instead of returning
    #       null. 20 false failures removed; 4 REAL ones surfaced (Dave's to rule).
    #   (2) `out[3] = <headline>` overwrites the FIRST snippet's "## " heading instead of
    #       inserting — provable in the committed artefact, which claims 38 snippets and
    #       contains 37 headings (Accordion's, alphabetically first, is the one eaten).
    #       ⛔ STILL OPEN — rolls to #126, with two additions measured at the #125 wrap: with
    #       ZERO snippets in scope the same line raises IndexError, and an unrecognised argv
    #       entry is silently taken as a snippet-name FILTER (there is no --selftest flag).
    # ⚠ CORRECTED AT THE #125 WRAP: this comment previously ended "THIS GATE WILL BE RED UNTIL
    # (1) IS FIXED", which went false inside its own session once s125-D3 landed — the exact
    # class #125 was convened to repair (a claim true when written, with nothing re-checking
    # it). CURRENT POSITION: the gate is RED, but on DIFFERENT grounds — 4 REAL contrast
    # failures awaiting Dave's ruling, plus ~32 FALSE ones from a THIRD, distinct defect:
    # effBg() walks ANCESTORS ONLY and cannot see an absolutely-positioned SIBLING painting the
    # selected pill (Segmented-control, Charts, View-options). That one is a GEOMETRY defect,
    # not a parse defect, and is deliberately unfixed — see _LIVE-STATE.md § OPEN.
    # Wired anyway because the ruled premise (it cannot run) is disproven and the wiring gate
    # admits no half-state; the bites themselves are Dave's to rule on.
    ("state-contrast gate — driven hover/pressed, light+dark (un-exempted #125)",
     "_validate_state_contrast.py"),
    # WIRED #119 at tier (b) SHRINK-ONLY RATCHET — Dave's ruling 2026-08-07. Baseline
    # 1,101 MEASURED at wiring (not copied), declared debt in _type_ratchet.json, may
    # only shrink. Risk named to Dave and accepted: shape of "a cap raised to clear its
    # own gate"; the difference claimed is shrink-only + declared-as-debt.
    ("type-composites ratchet — tier (b), debt 1101 shrink-only (Dave #119)",
     "_validate_type_composites.py", ["--ratchet"]),
    ("type-composites selftest", "_validate_type_composites.py", ["--selftest"]),
    ("coverage gate", "_validate_coverage.py"),
    ("pro-forma universal gate", "_validate_proforma.py"),
    ("pro-forma CSS-governed motion gate (DEF-003)", "_validate_css_governed.py"),
    ("pro-forma no-hardcode styling gate (DEF-004)", "_validate_no_hardcode.py"),
    ("4px-grid gate (DEF-005)", "_validate_grid.py"),
    ("type-binding blast-radius gate (canon/type.css)", "_validate_type_blast_radius.py"),
    ("descender-clip gate (ds-005) — truncating labels stay descender-safe", "_validate_descender_clip.py"),
    ("DataViz chart gate (semantic SVG + tokens + table spine)", "_validate_dataviz.py"),
    # WIRED 2026-07-27 (ds-014): this selftest already existed and ran only by hand, so nothing
    # proved dv-004 could fail — and it could not, on `stacked-column`. Exactly the rot the
    # ADR-0014 note below warns about. Unwired selftests are CLAIMED gates.
    ("DataViz gate selftest — bite-tests dv-004 + the dtype vocabulary (ds-014)", "_validate_dataviz.py", ["--selftest"]),
    # C2 (ds-018, RULED Dave 2026-07-27): "a declaration referencing a custom property that
    # resolves nowhere in its own scope is a build failure, not a silent fallback."
    # Ships ADVISORY only until its first-run backlog is cleared — see the script's __main__
    # for why, and promote with ["--strict"] the moment that list is empty.
    ("property-resolves gate C2 — silent-lookup class (BLOCKING, ds-018, promoted s121-D1)", "_validate_property_resolves.py", ["--strict"]),
    ("property-resolves gate C2 selftest — 4 bites + a bite-the-bite", "_validate_property_resolves.py", ["--selftest"]),
    ("reverse-text edge-extremity check {#col26-020} (advisory)", "_validate_edge_extremity.py"),
    ("compliance verification edges — applies_to vs verified_by (advisory)", "compliance/_build_verification_edges.py"),
    ("external automatable-check refs — axe-core import (advisory)", "compliance/_import_axe_rules.py"),
    # The consult read-side tool (reviews/CONSOLIDATION-AUDIT-2026-07-18.html §3): a
    # problem-domain query index over rules/rulings/assertions/gates/ADRs/defects/open
    # items, plus a CLI that answers "what governs X?" in one step. Index regenerates every
    # build so it cannot rot; the selftest is advisory until the tool has earned trust.
    ("consult index — problem-domain query surface", "_build_consult_index.py"),
    ("consult tool selftest (advisory)", "_consult.py", ["--selftest"]),
    # O2′ #25 (ruled Dave 2026-07-28, option-select ×3 all recommended): ONE retrieval
    # spine (_search_core.py), N doors — _consult.py (DS) + _memento_search.py (Memento).
    # Two-stage refs→fetch; the memento index regenerates every build so it cannot rot;
    # closed contracts REFUSE unknown structure (ds-016 class). The consult-receipt probe
    # (KG forcing function, ADVISORY) lives in _capture_gate.py and imports the core.
    ("search core selftest — two-stage engine + receipt format (O2′ #25)",
     "_search_core.py", ["--selftest"]),
    ("memento index — the Memento door's corpus (O2′ #25)", "_build_memento_index.py"),
    ("memento index determinism check (O2′ #25)", "_build_memento_index.py", ["--check"]),
    ("memento index selftest — contract refusals + determinism (O2′ #25)",
     "_build_memento_index.py", ["--selftest"]),
    ("memento search selftest — known-answer retrieval + fetch refusal (O2′ #25)",
     "_memento_search.py", ["--selftest"]),
    # #115 graph-candidates-pricing-brief, step 0: `_decision-graph.json` node ids and
    # `_memento-index.json` record ids have ZERO overlap — edges cannot be joined by id.
    # The mention map is the missing join (node-id -> record ids whose blob mentions it),
    # regenerated every build so it cannot rot; --check is the content-compared freshness
    # gate (never mtime), same shape as the memento index directly above. Runs AFTER the
    # memento index (needs its records) and after the decision graph (already fresh on
    # disk earlier in the run).
    ("graph mention map — the decision-graph/memento-index join (#115 step 0)",
     "_build_graph_mention_map.py"),
    ("graph mention map determinism check (#115 step 0)",
     "_build_graph_mention_map.py", ["--check"]),
    ("graph mention map selftest — hit/miss/refusal bites (#115 step 0)",
     "_build_graph_mention_map.py", ["--selftest"]),
    # ★ #41: the read chain as a FILE. Measured that morning: the contract prices the chain at
    # 3,838 tape and the opener paid 28,653 — because `Read` cannot read less than a file, so a
    # cold session buys all 18,434 tape of GOOD-MORNING.md to learn it should have stopped at
    # line 21. Five sessions called the chain CUT and every one paid full price for it.
    # Generated (never hand-authored) from `_capture_gate.chain_parts` — the SAME slicer the gate
    # measures with, so "the chain is N tape" and "here is the chain" cannot diverge.
    # ⚠ --check is BLOCKING here on purpose: this is the FIRST file a cold session reads and it
    # has no reason to doubt it, so a stale copy is the #32 defect with the blast radius maximised.
    # ⚠ BUT this position cannot actually catch that defect. The step directly above regenerates
    # _CHAIN.md from whatever GOOD-MORNING.md / _LIVE-STATE.md say RIGHT NOW, so by the time
    # --check runs here the file is fresh by construction — this can only ever catch
    # NONDETERMINISM in build() (two renders of the same input disagreeing), never a _CHAIN.md
    # left stale on disk by an edit to GM/LS that was never regenerated. That is precisely what
    # landed at the #56 wrap: a stale chain committed with a clean tree, because nothing between
    # "edit GM" and "commit" read this file. The disk-staleness reader now lives at the commit
    # seam instead — `knowledge/_git_commit.sh` runs `_gen_chain.py --check` itself, after the
    # --reconciled guard and before `git add -A`, where nothing regenerates the file in between
    # and a stale chain is still stale when it is read.
    ("read chain file — _CHAIN.md, the cold-start door (#41)", "_gen_chain.py"),
    ("read chain determinism check — stale _CHAIN.md serves a PREVIOUS session's record (#41)",
     "_gen_chain.py", ["--check"]),
    ("read chain selftest — verbatim terms + the CUT + refusal on a blank GM (#41)",
     "_gen_chain.py", ["--selftest"]),
    # #79: enforces Dave's #64 boundary ruling (memento-package/_PACKAGE-SPEC.md:13-14 —
    # "copies only, and every copy is delta-audited"). Nothing enforced this until
    # _gen_chain.py was found to have silently regressed 54 lines behind
    # knowledge/_gen_chain.py in BOTH in-package copies (the #73 title-block + stale-title
    # refusal — missing from the shipped package). Four arms: VERBATIM SET byte-compare
    # (_gen_chain.py/_memento_search.py/_search_core.py against knowledge/); the
    # _capture_gate.py SHIM's declared PROVENANCE (AST-hashed by name against its named
    # port commit — never line ranges, which the source file has already outgrown once);
    # the two in-package copies identical to each other; unknown files fail loud, named
    # (__pycache__ excluded by name, not by a blanket ignore).
    ("memento-package delta-audit — #64 boundary enforcement (#79)",
     "_validate_package_delta.py"),
    ("memento-package delta-audit selftest — mutation-tested, all 4 arms (#79)",
     "_validate_package_delta.py", ["--selftest"]),
    # ADR-0016 P1/P3 (2026-07-27, Dave ruled it a BUILD): the register asks the question no
    # other step asks — not "is the corpus self-consistent?" but "is this RULING LIVE in the
    # artefact Dave looks at?" Regenerates every build so it cannot rot. ADVISORY on purpose:
    # it reports 52 UNPROVEN on day one, and a gate that fails 52 rows gets switched off —
    # which is how we got here. Blocking once the register is green or deliberately waived
    # (the _validate_partials.py ratchet posture).
    ("enactment register — is each ruling IN FORCE? (advisory, ADR-0016)",
     "_build_enactment_register.py"),
    # ds-015 (2026-07-27): the register above asks "is there a check and can it fail?".
    # This asks the question ON TOP of it — "can that check OBSERVE the property its rule
    # names?" A check can be PROVEN and still measure a proxy. Selftest first, per the
    # standing rule that every new gate ships a bite AND wires it; the tool is ADVISORY
    # for the same reason the register is.
    ("instrument-fit selftest (advisory, ds-015)", "_build_instrument_fit.py", ["--selftest"]),
    ("instrument fit — can the gate SEE the property? (advisory, ds-015)",
     "_build_instrument_fit.py"),
    ("integrity lint (gate)", "_build_integrity.py"),
]

# ── Failure routing: EXACT step IDs, never substrings (#77 periphery finding) ──
# Remedies used to be routed by SUBSTRING match on the step label, and the cascade
# guessed: "consult index — problem-domain query surface" matched "surface" so a
# consult-index failure was reported as a dark-surface failure (wrong cause, wrong
# remedy); "token projection sync — snippets/…" and "canon components — regenerate
# from snippets" both matched "snippet" first, so the projection remedy written FOR
# that step was unreachable dead code; two advisory-labelled steps ("icon contrast
# delta", "theme-provenance") matched blocking branches and gated; the token
# blast-radius BUILDER matched the type-binding blast-radius GATE's remedy.
# Routing is now a table keyed on the EXACT step label. A step with no row — or a
# stale row for no step — fails LOUD AND NAMED before step 1 runs: a measuring
# tool must not guess; UNKNOWN is never defaulted.
GATE = "gate"          # print the remedy, record rc, keep running (every report stays fresh)
ADVISORY = "advisory"  # report and continue; never gates the build
ABORT = "abort"        # print and stop the build at this step

_CONTRAST = "\n❌ contrast gate failed (exit {code}) — see knowledge/_*-CONTRAST-AUDIT.md"
_PARTIALS = "\n❌ component-partials gate failed (exit {code}) — an AUTO-PARTIAL block is out of sync with its source atom, or a member breaks the registry contract (vars / matchValues / manifest binds). Run: python3 knowledge/gen_component_partials.py — registry: knowledge/component-types.json (ADR-0013)"
_BEHAVIOUR = "\n❌ behaviour-contract gate failed (exit {code}) — the dv-behaviour source breaks the ADR-0015 performance contract (size / banned pattern / resize discipline) or a member snippet carries an external script src. See knowledge/_BEHAVIOUR-GATE.md"
_CANON = "\n❌ canon components step failed (exit {code}) — .cn-* blocks diverged from the snippets or the generator is non-deterministic. Run: python3 knowledge/canon/gen_canon_components.py (ADR-0013 ruling 4)"
_RATCHET = "\n❌ partial ratchet failed (exit {code}) — a registry member re-implements a registered partial's rule locally. Consume the partial (AUTO-PARTIAL markers), never re-type the sub-atom. See knowledge/_PARTIALS-GATE.md (ADR-0013)"
_THEME = "\n❌ theme-cascade sync failed (exit {code}) — canon.css AUTO-THEMES is out of sync with tokens/themes/*.json (+ manifests). Run: python3 knowledge/canon/gen_theme_cascade.py"
_SHOWROOM = "\n❌ showroom sync failed (exit {code}) — showroom/ is stale against the snippets/tokens/cascade. Run: python3 knowledge/gen_showroom.py"
_DATAVIZ = "\n❌ DataViz chart gate failed (exit {code}) — see knowledge/_DATAVIZ-GATE.md"
_PKGDELTA = "\n❌ memento-package delta-audit failed (exit {code}) — a package copy has drifted from its knowledge/ source, the two in-package copies disagree, an unknown file appeared in a machinery/ folder, or a shim-ported function/constant changed since its declared provenance commit. See memento-package/_PACKAGE-SPEC.md:13-14 (Dave's #64 boundary ruling: copies only, every copy delta-audited). Run: python3 knowledge/_validate_package_delta.py"

ROUTE_ROWS = [
    # (exact step label, kind, remedy template) — remedy text unchanged from the old cascade.
    ("compliance knowledge graph", ABORT, None),
    ("token blast-radius + graph report", ABORT, None),  # was misrouted to the TYPE-BINDING blast-radius remedy
    ("token blast-radius + graph report — determinism/staleness check (#79 P6)", ABORT, None),
    ("token blast-radius + graph report selftest (#79 P6)", ABORT, None),
    ("guideline rules index (gate)", GATE,
     "\n❌ rules-index gate failed (exit {code}) — duplicate/missing/malformed rule IDs in guidelines/"),
    ("runbook index (generated)", ABORT, None),
    ("standing-instructions reachability gate", GATE,
     "\n❌ standing-instructions gate failed (exit {code}) — a standing doc is unreachable from GOOD-MORNING/_RUNBOOKS, or GOOD-MORNING has lost part of its structure. A rule nothing points to will not survive the next cold session."),
    ("assertion veracity gate — claims that can rot", ABORT, None),
    ("assertion veracity selftest — verbs bite + registry well-formed (#77 periphery)", ABORT, None),
    ("capture/provenance gate — status+provenance on new notes+dossiers (Memento §4.1)", ABORT, None),
    ("capture/provenance selftest (Memento §4.1)", ABORT, None),
    # ✅ #80: ADVISORY -> ABORT, PROMOTED BY DAVE. The #79 demotion was conditional on the
    # arm being BORN RED against an unruled defect: gating the whole build on something
    # nobody had decided would have been a gate making Dave's ruling for him. He ruled it
    # (#79-D1, *"make it refuse"*), #80 built the paired fix, and the arm is GREEN AT REST --
    # so promotion no longer risks a red build, and the flag and the fix move together as
    # the demotion note said they must.
    # ★ WHY ABORT AND NOT A LOUDER WARNING -- the same argument one level up: ADVISORY lets
    # a build COMPLETE while the context floor is UNKNOWN, which is the exact shape of the
    # defect #79-D1 just ruled out of count(). A gauge that cannot measure must stop the
    # thing that depends on it, not annotate it.
    # ⚠ THE COST, DECLARED: a machine without tiktoken now HARD-STOPS here. CI is unaffected
    # (.github/workflows/gates.yml installs tiktoken before the gates run); a cold sandbox is
    # NOT -- it pays one `pip install tiktoken --break-system-packages`, which is precisely
    # the remedy the refusal prints. That friction is the ruling working, not a side effect.
    ("gauge-tokens selftest -- counting path + cache + degraded-measurement honesty (#79 P5)", ABORT, None),
    ("roll-state measurer selftest (#77 T1)", ABORT, None),
    ("commit-seam harness — _git_commit.sh fixture-repo arms (#78-D1 P1)", ABORT, None),
    ("GM/LS mover selftest — hardened move mechanics (M5)", ABORT, None),
    ("section-usage instrumentation selftest (#23)", ABORT, None),
    ("lane records — regenerate LS §🛤 view (O1′ #24)", ABORT, None),
    ("lane records determinism check (O1′ #24)", ABORT, None),
    ("lane records selftest — schema refusals + routing contract (O1′ #24)", ABORT, None),
    ("cross-reference index", ABORT, None),
    ("sutherland acceptance fixtures", ABORT, None),
    ("states-completeness probe (advisory)", ADVISORY, None),
    ("decision-graph — typed edges + conflict gate (advisory, ADR-0012)", ADVISORY, None),
    ("decision-graph selftest — conflict gate bites on unresolved/open/orphan (ADR-0012, #77 periphery)", ABORT, None),
    ("spine-writer selftest — splice invariants + no-half-writes (#78-D2)", ABORT, None),
    ("_LIVE-STATE staleness gate + lifecycle-block generation (advisory, ADR-0007)", ADVISORY, None),
    ("advisory signals — prose rules (advisory)", ADVISORY, None),
    ("review queue", ABORT, None),
    ("dark-mode coverage audit", ABORT, None),  # was misrouted to the COVERAGE-gate remedy
    ("text/icon contrast audit", GATE, _CONTRAST),
    ("indicator/accent contrast audit", GATE, _CONTRAST),
    ("icon contrast delta — brand 4.5 vs 3 (advisory)", ADVISORY, None),  # was misrouted to the BLOCKING contrast branch
    ("dark-surface flatness gate", GATE,
     "\n❌ dark-surface gate failed (exit {code}) — see knowledge/_DARK-SURFACE-AUDIT.md"),
    ("component-partials sync — AUTO-PARTIAL injection + contracts (ADR-0013)", GATE, _PARTIALS),
    ("component-partials selftest (ADR-0013)", GATE, _PARTIALS),
    ("token-set distribution sync — AUTO-TOKENS injection (s121-D1)", GATE,
     "\n❌ token-set distribution failed (exit {code}) — an AUTO-TOKENS block is out of sync with its canon.css TOKENS source atom (alpha ramp / status-mark map). Run: python3 knowledge/gen_token_ramp.py (s121-D1)"),
    ("token-set distribution selftest (s121-D1)", GATE,
     "\n❌ gen_token_ramp selftest failed (exit {code}) — knowledge/gen_token_ramp.py --selftest (s121-D1)"),
    ("Behaviour contract gate — dv-behaviour size + banned patterns (ADR-0015)", GATE, _BEHAVIOUR),
    ("Behaviour contract selftest (ADR-0015)", GATE, _BEHAVIOUR),
    ("canon components — regenerate from snippets (ADR-0013 ruling 4)", GATE, _CANON),  # was misrouted to the SNIPPET remedy ("snippets" in the label)
    ("canon components determinism check (ADR-0013 ruling 4)", GATE, _CANON),
    ("partial re-implementation ratchet (ADR-0013)", GATE, _RATCHET),
    ("partial-ratchet selftest (ADR-0013)", GATE, _RATCHET),
    ("token projection sync — snippets/tranches/canon literals (gen_snippet_tokens)", GATE,
     "\n❌ token projection out of sync (exit {code}) — a store value changed without re-projection (or a manifest path is unresolvable). Run: python3 knowledge/gen_snippet_tokens.py"),  # this remedy was DEAD CODE — "snippet" matched first
    ("snippet gate", GATE,
     "\n❌ snippet gate failed (exit {code}) — see knowledge/_SNIPPET-AUDIT.md"),
    ("theme cascade sync — [data-apollo-theme] layer (ADR-0011)", GATE, _THEME),
    ("theme cascade selftest (ADR-0014)", GATE, _THEME),
    ("state-snap gate — opacity states snap to the active theme's ramp (ADR-0014)", ABORT, None),
    ("state-snap selftest (ADR-0014)", ABORT, None),
    ("radius gate — no hardcoded border-radius; shape is a theme flex slot (ADR-0010)", GATE,
     "\n❌ radius gate failed (exit {code}) — a hardcoded border-radius literal on a strict surface. Shape is theme-flexed (ADR-0010): bind var(--border-radius-default); 50%/999px circle+pill idioms are exempt. See knowledge/_RADIUS-GATE.md"),
    ("showroom sync — generated component library (RULED 2026-07-21)", GATE, _SHOWROOM),
    ("showroom URL-rebase selftest — the srcdoc base-URL trap (2026-07-27)", GATE, _SHOWROOM),
    ("Legacy-colour leakage gate (Mono) — no Legacy-only colour in a Mono surface", GATE,
     "\n❌ Legacy-colour leakage gate failed (exit {code}) — a Mono surface resolves to a Legacy-only colour (e.g. the success teal #00847F). Rebind onto the R-D14 token (rag/*-background / -glyph); do NOT add the hex to exceptions. See knowledge/_LEGACY-LEAK-GATE.md"),
    ("theme-provenance gate (ADR-0011/R-D19) — no foreign-theme hex in a Mono surface (advisory)", ADVISORY, None),  # was misrouted to the BLOCKING dark-surface branch
    ("token-tier gate (_STANDARDS.md §1)", GATE,
     "\n❌ token-tier gate failed (exit {code}) — a component references a primitive, or a $value drifted from its $alias; see knowledge/_TOKEN-TIER-AUDIT.md"),
    ("icon-source gate", GATE,
     "\n❌ icon-source gate failed (exit {code}) — see knowledge/_ICON-SOURCE-AUDIT.md"),
    ("a11y gate", GATE, "\n❌ a11y gate failed (exit {code}) — see knowledge/_A11Y-GATE.md"),
    # ⚠ #119 FOUND: this row was MISSING since the step was registered at #116 — check_routes
    # aborted every full build before step 1, so the full build cannot have run since. The
    # wiring-seam class again: registered but unroutable. Added #119, declared in the chain.
    ("a11y target-measurement selftest (s114-D5)", ABORT, None),
    ("wiring gate — no orphaned validators (#118 seam)", GATE,
     "\n❌ wiring gate failed (exit {code}) — a _validate_*.py is on disk with no STEPS entry and no named exemption; wire it or exempt it BY NAME (knowledge/_validate_wiring.py)"),
    ("wiring gate selftest — 4 bites", ABORT, None),
    ("compose gate (orphan wired #119)", GATE,
     "\n❌ compose gate failed (exit {code}) — see knowledge/_validate_compose.py"),
    ("screen gate — compose+icons+a11y over fitness fixtures (re-wired #120)", GATE,
     "\n❌ screen gate failed (exit {code}) — a _fitness-test canon fixture fails compose/icon-source/a11y; see knowledge/_validate_screen.py output"),
    ("state-contrast gate — driven hover/pressed, light+dark (un-exempted #125)", GATE,
     "\n❌ state-contrast gate failed (exit {code}) — a driven hover/pressed state measures below 4.5:1 (large 3.0:1) in light or dark; see knowledge/_STATE-CONTRAST-AUDIT.md. ⚠ #125: verify the reading before treating it as a design defect — the validator's parse() cannot read color(srgb ...) backgrounds (every color-mix() hover), and mis-reports those as ~1:1."),
    ("type-composites ratchet — tier (b), debt 1101 shrink-only (Dave #119)", GATE,
     "\n❌ type-composites ratchet failed (exit {code}) — NEW violation(s) above the declared debt in knowledge/_type_ratchet.json; the ratchet only shrinks (s119-D1). Fix the new violations; do NOT raise the baseline."),
    ("type-composites selftest", ABORT, None),
    ("coverage gate", GATE, "\n❌ coverage gate failed (exit {code}) — see knowledge/_COVERAGE-GATE.md"),
    ("pro-forma universal gate", GATE,
     "\n❌ pro-forma universal gate failed (exit {code}) — see knowledge/_PROFORMA-GATE.md"),
    ("pro-forma CSS-governed motion gate (DEF-003)", GATE,
     "\n❌ pro-forma CSS-governed motion gate failed (exit {code}) — see knowledge/_CSS-GOVERNED-GATE.md"),
    ("pro-forma no-hardcode styling gate (DEF-004)", GATE,
     "pro-forma no-hardcode styling gate failed (exit {code}) — see knowledge/_NO-HARDCODE-GATE.md"),
    ("4px-grid gate (DEF-005)", GATE,
     "\n❌ 4px-grid gate (DEF-005) failed (exit {code}) — off-grid layout value(s); see _validate_grid.py output"),
    ("type-binding blast-radius gate (canon/type.css)", GATE,
     "\n❌ type-binding blast-radius gate failed (exit {code}) — a global type-composite selector is unregistered or its blast radius escaped; see knowledge/_TYPE-BLAST-GATE.md"),
    ("descender-clip gate (ds-005) — truncating labels stay descender-safe", GATE,
     "\n❌ descender-clip gate (ds-005) failed (exit {code}) — a truncating label (text-overflow:ellipsis) lacks `text-box-edge:text text`, so cap-alphabetic trim will clip its descenders (g/y/p/q). This is NOT a stray override to remove — the override IS the fix; add it. See _validate_descender_clip.py + _DS-IMPROVEMENTS.md ds-005."),
    ("DataViz chart gate (semantic SVG + tokens + table spine)", GATE, _DATAVIZ),
    ("DataViz gate selftest — bite-tests dv-004 + the dtype vocabulary (ds-014)", GATE, _DATAVIZ),
    ("property-resolves gate C2 — silent-lookup class (BLOCKING, ds-018, promoted s121-D1)", GATE,
     "\n❌ property-resolves gate C2 failed (exit {code}) — a var() resolves to NOTHING and the property silently takes its INITIAL value (ds-018). knowledge/_validate_property_resolves.py — if the name is an --alpha-*/--mark token, run: python3 knowledge/gen_token_ramp.py"),
    ("property-resolves gate C2 selftest — 4 bites + a bite-the-bite", ABORT, None),
    ("reverse-text edge-extremity check {#col26-020} (advisory)", ADVISORY, None),
    ("compliance verification edges — applies_to vs verified_by (advisory)", ADVISORY, None),
    ("external automatable-check refs — axe-core import (advisory)", ADVISORY, None),
    ("consult index — problem-domain query surface", ABORT, None),  # THE #77 misroute: "surface" matched the dark-surface branch
    ("consult tool selftest (advisory)", ADVISORY, None),
    ("search core selftest — two-stage engine + receipt format (O2′ #25)", ABORT, None),
    ("memento index — the Memento door's corpus (O2′ #25)", ABORT, None),
    ("memento index determinism check (O2′ #25)", ABORT, None),
    ("memento index selftest — contract refusals + determinism (O2′ #25)", ABORT, None),
    ("memento search selftest — known-answer retrieval + fetch refusal (O2′ #25)", ABORT, None),
    ("graph mention map — the decision-graph/memento-index join (#115 step 0)", ABORT, None),
    ("graph mention map determinism check (#115 step 0)", ABORT, None),
    ("graph mention map selftest — hit/miss/refusal bites (#115 step 0)", ABORT, None),
    ("read chain file — _CHAIN.md, the cold-start door (#41)", ABORT, None),
    ("read chain determinism check — stale _CHAIN.md serves a PREVIOUS session's record (#41)", ABORT, None),
    ("read chain selftest — verbatim terms + the CUT + refusal on a blank GM (#41)", ABORT, None),
    ("memento-package delta-audit — #64 boundary enforcement (#79)", GATE, _PKGDELTA),
    ("memento-package delta-audit selftest — mutation-tested, all 4 arms (#79)", GATE, _PKGDELTA),
    ("enactment register — is each ruling IN FORCE? (advisory, ADR-0016)", ADVISORY, None),
    ("instrument-fit selftest (advisory, ds-015)", ADVISORY, None),
    ("instrument fit — can the gate SEE the property? (advisory, ds-015)", ADVISORY, None),
    ("integrity lint (gate)", GATE,
     "\n❌ integrity gate failed (exit {code}) — see knowledge/_INTEGRITY-REPORT.md"),
]


def _build_routes():
    routes = {}
    for label, kind, remedy in ROUTE_ROWS:
        if label in routes:
            raise SystemExit(f"❌ ROUTING TABLE DEFECT: step ID {label!r} has more than one route row")
        assert (remedy is not None) == (kind == GATE), \
            f"route for {label!r}: GATE rows carry remedy text; ADVISORY/ABORT rows carry None"
        routes[label] = (kind, remedy)
    return routes


ROUTES = _build_routes()


def route(label, routes=None):
    """Exact-ID lookup. UNKNOWN is never defaulted — fail loud and named (#77)."""
    routes = ROUTES if routes is None else routes
    if label not in routes:
        raise SystemExit(
            f"❌ UNKNOWN STEP ID: {label!r} has no route in ROUTE_ROWS (_build_all.py). "
            "Every STEPS entry needs an exact-label row — substring guessing was removed (#77); "
            "a measuring tool must not guess."
        )
    return routes[label]


def check_routes(routes=None):
    """Every registered step resolves to exactly one route; no stale route rows for
    steps that no longer exist. Runs BEFORE step 1 of every build — a table gap
    aborts the build loud and named instead of guessing at failure time."""
    routes = ROUTES if routes is None else routes
    labels = [s[0] for s in STEPS]
    for label in labels:
        route(label, routes)
    orphans = sorted(set(routes) - set(labels))
    if orphans:
        raise SystemExit(f"❌ ROUTING TABLE DEFECT: route row(s) for unregistered step(s): {orphans!r}")
    return len(set(labels))


def selftest():
    """--selftest short-circuits in __main__ BEFORE the build loop: no step runs,
    nothing is regenerated or written. Arms: (a) completeness — every registered
    step ID resolves to exactly one route; (b) an unknown ID refuses loud and
    named; (c) mutation control — proof that (a) can go red."""
    # (a) every registered step ID resolves to exactly one route
    n = check_routes()
    for label, (kind, remedy) in ROUTES.items():
        assert kind in (GATE, ADVISORY, ABORT), f"route for {label!r}: unknown kind {kind!r}"
        if kind == GATE:
            assert "{code}" in remedy, f"GATE remedy for {label!r} lost its {{code}} slot"
    print(f"  selftest (a): {n} registered step ID(s), each resolves to exactly one route ✓")
    # (b) an unknown ID refuses, loud and named — never a silent default
    probe = "no-such-step (#77 probe)"
    try:
        route(probe)
    except SystemExit as e:
        assert probe in str(e) and "UNKNOWN STEP ID" in str(e), f"refusal must NAME the id: {e}"
    else:
        raise AssertionError("selftest (b): unknown step ID was routed without refusing")
    print("  selftest (b): unknown step ID refuses, loud and named ✓")
    # (c) mutation control: drop one REAL route and prove arm (a) goes red
    victim = STEPS[0][0]
    mutant = {k: v for k, v in ROUTES.items() if k != victim}
    try:
        check_routes(routes=mutant)
    except SystemExit as e:
        assert victim in str(e), f"mutant refusal must name the missing step: {e}"
    else:
        raise AssertionError("selftest (c): completeness stayed green with a route removed — the check cannot fail")
    print(f"  selftest (c): mutation control — dropping the route for {victim!r} turns (a) red ✓")
    print(f"selftest PASS — exact-ID failure routing over {n} steps; unknown never defaulted (#77)")
    return 0


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if "--selftest" in argv:
        return selftest()          # short-circuits: the build loop below never runs
    check_routes()                 # fail loud BEFORE step 1 if STEPS and ROUTE_ROWS disagree
    rc = 0
    for i, step in enumerate(STEPS, 1):
        label, rel = step[0], step[1]
        extra_args = list(step[2]) if len(step) > 2 else []
        path = os.path.join(HERE, rel)
        print(f"\n=== [{i}/{len(STEPS)}] {label} — {rel} ===")
        r = subprocess.run([sys.executable, path] + extra_args)
        if r.returncode != 0:
            kind, remedy = route(label)
            if kind == GATE:
                # Gating steps run to the end (so you get every report) then the
                # build exits non-zero.
                print(remedy.format(code=r.returncode))
                rc = rc or r.returncode
            elif kind == ADVISORY:
                # advisory steps never gate/abort — they report and the build continues
                print(f"\n⚠ advisory step '{label}' reported findings (exit {r.returncode}) — non-gating")
            else:  # ABORT
                print(f"\n❌ step '{label}' failed (exit {r.returncode}) — aborting")
                return r.returncode
    if rc == 0:
        print("\n✅ all generators ran and the integrity + contrast gates passed.")
    else:
        print("\n❌ build gate failed — see the reports above.")
    return rc


if __name__ == "__main__":
    sys.exit(main())
