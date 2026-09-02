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

Run:  python3 knowledge/_build_all.py                # FULL build — deliberate, NO argv
      python3 knowledge/_build_all.py --selftest     # no step runs, nothing is written
      python3 knowledge/_build_all.py --range A-B    # chunked pass, steps A..B (#148)
      python3 knowledge/_build_all.py --resume [N]   # continue a chunked pass (default N=15)

ARGV IS A CONTRACT (#208). Those four forms are the whole of it. An unknown argument is
REFUSED — loud, named, rc=2, nothing built — never treated as "no flags given", which is
spelled "build everything". #204 ran the full build BY ACCIDENT exactly that way. `-h` /
`--help` are answered earlier, by `_helpgate.help_gate`, and never reach the contract.

Exits non-zero if EITHER gate fails: the integrity lint (step 8, any ERROR) or
the contrast audits (steps 6-7, any non-allowlisted token below its dark-mode
threshold). Both run to completion first so every report is fresh. This is the
single command to trust the knowledge base after editing metas or tokens.
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
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
    # #158 — the GENERATORS-WRITE-BY-DEFAULT class (born #150, homed in _FUTURE-STATE.md
    # at #153, (n+1)th instance at #157 when `gen_showroom.py --help` REWROTE showroom/).
    # A runtime write-probe measured 52 scripts that attempted a repo write on a bare
    # --help, 14 of them at MODULE level. The remedy is one guard line per entry point
    # (knowledge/_helpgate.py); THIS gate is what keeps it there, and it runs EARLY so a
    # regression is reported before any generator in this list has written anything.
    ("help-gate — no entry point may write before it reads argv (#158 class gate)",
     "_validate_help_gate.py"),
    ("help-gate selftest — 5 mutation bites (#158 class gate)",
     "_validate_help_gate.py", ["--selftest"]),
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
    # ⚠ #218: `--build` is now MANDATORY here. `_capture_gate.py` gained an argv contract (the
    # #158 write-by-default class, both legs) and a BARE invocation is REFUSED with exit 2 —
    # the step ID (the routing key) is unchanged, only the stated intention is now explicit.
    ("capture/provenance gate — status+provenance on new notes+dossiers (Memento §4.1)",
     "_capture_gate.py", ["--build"]),
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
    # #165: THE WORKLIST STORE GATE HAD NO ROUTE ROW AND NO STEPS ENTRY — `_state.py::check()`
    # and its 12-bite selftest have existed since #88 and ran ONLY by hand. Same class as the
    # #158 help-gate omission #164 caught: an instrument without a consumer cannot fail
    # [[instrument-without-a-consumer]]. Wired now, with the new optional `priority_override`
    # presence gate (#165) riding the same pair. Measured green standalone before wiring
    # (rc=0 both arms). The #165 wiring declared a ROUTING SPLIT — selftest ABORT, store gate
    # GATE — on the argument that the gate's reds are DAVE'S DATA and a build he must fix
    # before it completes is a gate making his ruling for him.
    # ⛔ REVERSED BY DAVE (#166 replay): FAIL LOUD. Both arms are now ABORT. The argument above
    # was wrong in its premise, not its principle: the gate does NOT red on the 19 declared
    # legacy items (that debt is DECLARED and passes by design), so the only thing that can
    # turn it red is a NEW malformed item — a schema violation an agent wrote, not a decision
    # Dave owes. A GATE-routed red prints its remedy 80 steps from the end and is read as
    # weather; an ABORT stops the build at the item [[a-crash-is-not-a-fail]].
    ("worklist store gate — open items state what would close them; optional "
     "priority_override is Dave's (#88 store, wired #165)", "_state.py"),
    ("worklist store selftest — schema presence gates incl. priority_override / deadline / "
     "effort (#165, extended #166)",
     "_state.py", ["--selftest"]),
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
    # WIRED #158, the same pass it was built (s157-D2). Sits next to the state-snap gate on
    # purpose: both hold an ADR-0014 "declare what you consume" join — neutralRamp there,
    # ragPalette here. The defect it closes had NO instrument at all: 12 hex-identical RAG
    # keys duplicated across two ratified override files with nothing declaring the sharing.
    # WIRED #196, the same pass it was built (brief
    # `notes/_briefs/2026-08-17-196-stale-queue-gate-brief.md`, Dave: "a proper fix,
    # thorough and tested"). Re-measures every §C·1 queue item's stated work-state
    # against disk and git, so a prose claim cannot outlive reality again (STEP 2 read
    # "open" for twelve sessions after `df44e51` landed it). Routed ADVISORY — the
    # findings are Dave's queue, and the gate shipped WARN by his ruling (flipped BLOCKING #198, f0ab051, s197-D1 condition met); the SELFTEST is
    # ABORT, because a stale-queue gate that has stopped biting is a silent instrument.
    ("stale-queue gate — §C·1 qprobe claims re-measured vs disk + git (BLOCKING, #198)",
     "_validate_queue_fresh.py"),
    ("stale-queue selftest — 13 bites incl. both mutation directions + scope (#196)",
     "_validate_queue_fresh.py", ["--selftest"]),
    ("palette-tier gate — every theme names a palette per family, no divergent hand-carry (s157-D2)", "_validate_palette_tier.py"),
    ("palette-tier selftest — 10 mutation bites (s157-D2)", "_validate_palette_tier.py", ["--selftest"]),
    ("radius gate — no hardcoded border-radius; shape is a theme flex slot (ADR-0010)", "_validate_radius.py"),
    ("showroom sync — generated component library (RULED 2026-07-21)", "gen_showroom.py", ["--check"]),
    ("showroom URL-rebase selftest — the srcdoc base-URL trap (2026-07-27)", "gen_showroom.py", ["--selftest"]),
    # WIRED #165, the same pass it was built (brief `_BRIEF-progress-dashboard-2026-08-13-v1.md`,
    # ruled by Dave #164). Sits beside the showroom pair on purpose — SAME LAW: generated from
    # the stores, never hand-edited, so `--check` red means "the page disagrees with the stores
    # or with a live gate", never "a day has passed" (the generator carries no clock).
    # Routed GATE, mirroring `gen_showroom.py --check`: a stale REPORT is not a broken system,
    # and the remedy is one command. ⚠ The route row below is what makes this step legal —
    # a STEPS entry with no ROUTE_ROWS row aborts every full build above step 1 (#119/#164).
    ("dashboard sync — generated progress dashboard (RULED #164, built #165)", "gen_dashboard.py", ["--check"]),
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
    # WIRED #209: the wiring gate named it ORPHAN once the state-snap fix let CI's build reach
    # this depth (the un-masking chain: [52] green → wiring gate fires). Built #203 as the 44px
    # minimum-hit-area consumer; browser-bound, so in a plain environment it exits 77
    # COULD-NOT-ASK (legal form granted #209) and the build continues DECLARED; where a browser
    # is staged it measures rendered geometry for real. ADVISORY per its own tier — no --strict.
    ("hit-area gate — 44px minimum, rendered geometry (ADVISORY, built #203, wired #209)",
     "_validate_hit_area.py", ["--all"]),
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
    #
    # ⛔⛔ CORRECTED AGAIN AT #127 — AND THAT IS THE FINDING, NOT THE CORRECTION.
    # The paragraph ABOVE is now false in its turn: the ~32 FALSE failures were FIXED at #127
    # (effBg now composites the browser's own hit stack; before/after proved the delta is
    # exactly 32 removed, 0 added, and all 4 REAL failures survive with identical ratios).
    # Coverage also went 38 -> 75 snippets once the out[3] overwrite became an insert.
    # ⚠ THIS COMMENT HAS NOW GONE FALSE TWICE, IN TWO CONSECUTIVE SESSIONS, INSIDE THE FILE
    # THAT ENFORCES THE RULE AGAINST EXACTLY THIS. The standing remedy for a claim that goes
    # stale twice is GENERATE IT, DO NOT RE-STAMP IT (s125-D1's precedent: a typed figure that
    # rotted twice was replaced by an AST reader plus permanent bites). A THIRD hand-correction
    # is the move that ruling exists to forbid — so this stratum is left as EVIDENCE and the
    # remedy is raised to Dave rather than taken here. [[no-gate-parses-the-artefact]]
    # CURRENT POSITION, #127: RED on Dave's 4 real failures ONLY (14 records across variants).
    ("state-contrast gate — driven hover/pressed, light+dark (un-exempted #125)",
     "_validate_state_contrast.py"),
    # WIRED #127. Precedent, stated in this same file: "a selftest not in STEPS is a gate that
    # does not run." 19 arms, incl. the boundary bite that catches a "fix" which stops failing
    # by ceasing to report. ⚠ Like the gate row above it, this row NEEDS A BROWSER —
    # knowledge/_tests/test_gates.py:23 still correctly excludes both from CI's static suite.
    ("state-contrast gate selftest — paint stack, report arithmetic, named args",
     "_validate_state_contrast.py", ["--selftest"]),
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
    # #139: two orphan gates wired — _validate_wiring.py named both ORPHAN (a gate that
    # does not run cannot fail; the #133 fifth-medium gate had been an orphan since built).
    ("KG edge parse-gate + s135-D4 resolutions-consumed check", "_validate_kg.py"),
    ("KG edge gate selftest (6 bites)", "_validate_kg.py", ["--selftest"]),
    ("Token fork-ban gate — undeclared same-scope forks (s136-D1 lane, #139)", "_validate_token_forks.py"),
    ("Token fork-ban selftest (2-direction)", "_validate_token_forks.py", ["--selftest"]),
    # #146: THREE gates wired in one pass, all the same class (instrument-without-a-consumer,
    # layered): (a) the four #139 STEPS entries above landed with NO ROUTE_ROWS rows, so
    # check_routes() ABORTED every build since #139 — the runner itself was the dead
    # instrument, which is why (b) _validate_binds_ratchet.py and _validate_dtcg.py
    # (both #141) sat as wiring-gate ORPHANS for 5 sessions with nobody told: the wiring
    # gate runs INSIDE the runner that refused to start. (c) is the new #146 gate itself.
    ("binds shrink-only ratchet (s136-D1 axis A; built #141, wired #146)",
     "_validate_binds_ratchet.py"),
    ("DTCG spine conformance gate (s141-D1 axis A; built #141, wired #146)",
     "_validate_dtcg.py"),
    ("binds-resolve gate — manifest presence + address→store resolution (#146)",
     "_validate_binds_resolve.py"),
    ("binds-resolve selftest — 5 bites incl. any-store clause (#146)",
     "_validate_binds_resolve.py", ["--selftest"]),
    # s195-D1 (Dave's word "wire it", #195): the chart-intent address layer. The vocabulary is
    # ADOPTED (FT), lives ONCE in chart-intents.json (ADR-0017); this gate is resolution only.
    ("chart-intent resolve gate — meta intent address → chart-intents.json (BLOCKING s195-D1)",
     "_validate_intent_resolve.py"),
    ("chart-intent resolve selftest — 4 bites incl. list case + absent store (s195-D1)",
     "_validate_intent_resolve.py", ["--selftest"]),
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
    # ds-0NN (priced #184, built #190): C2 reads <style>/style="" USES. A chart's colours
    # live in SVG PRESENTATION ATTRIBUTES, which no gate parsed — a dangling fill="var(--x)"
    # painted SILENT BLACK past thirteen of thirteen gates. This gate parses the markup.
    # BLOCKING since s191-D3 (#191, Dave's word) — was ADVISORY-on-purpose #190 awaiting his call.
    ("dataviz var-resolution gate — markup fill/stroke var() per theme (BLOCKING s191-D3, ds-0NN #184)",
     "_gate_dataviz_vars.py"),
    ("dataviz var-resolution gate selftest — 8 arms incl. alias chain + missing target (ds-0NN)",
     "_gate_dataviz_vars.py", ["--selftest"]),
    # THE MIRROR OF THE TWO ABOVE (built #219 lane 5). C2 and the dataviz gate both ask "does
    # this USE resolve?". Nothing asked "is this MINT read?" — so a token minted with a value
    # Dave ruled, consumed by nothing, was invisible to all 13+ gates. #219 found two live cases
    # by hand (the s202-D1 segmented radii, dark for 17 sessions; --padding-card-internal).
    # ADVISORY ON PURPOSE and it must stay so: a forgotten wire and a deliberately-reserved slot
    # wear the same shape, and no presence test can separate them. Promotion needs a
    # $consumer/$reserved declaration on the token, and is DAVE'S WORD, not a builder's pick.
    ("minted-token consumption inventory — declared-but-never-read (ADVISORY, built #219)",
     "_gate_minted_consumption.py"),
    ("minted-consumption selftest — 10 arms incl. both false-positive mutants (#219)",
     "_gate_minted_consumption.py", ["--selftest"]),
    # THE SAME CLASS FROM THE OTHER END (built #219 lane 6, wired at the #219 seam-3 reconcile).
    # The UA sheet's `[hidden]{display:none}` is specificity (0,1,0); any author `display:` rule
    # that matches the same element and is not beaten WINS, so the element PAINTS while `hidden`
    # tells assistive tech it is gone. #218 W3 F1 drove the consequence in a real snippet and
    # s218-D5 cl.3 fixed that ONE instance while putting the repo-wide sweep on the gates backlog.
    # This is the sweep. ADVISORY ON PURPOSE: the matcher grades subject compounds and IGNORES
    # combinators, so it can name a pair that cannot collide in the rendered DOM — the correct
    # bias for triage, and the exact reason its findings are TRIAGE INPUT and not repairs.
    # Promotion to blocking is DAVE'S WORD (ADR-0005 §5 — it must survive real use first).
    ("hidden-attr vs author-display sweep — painted while hidden (ADVISORY, built #219)",
     "_validate_hidden_display.py"),
    ("hidden-attr display selftest — 16 bites incl. the real #218 mutant (#219)",
     "_validate_hidden_display.py", ["--selftest"]),
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
    # WIRED #127 — Dave's call at the opener. The Memento schematic v2: one generated HTML
    # diagram of the six subsystems (chain · store · search · marks · gates · package), every
    # figure read off disk at generation time. v1 was HAND-AUTHORED, referenced by no generator,
    # and asserted "27 blocking validators in a 55-step build" against a disk of 30 and 98 — it
    # is KEPT and TOMBSTONED (Dave's #125 disposition), not corrected and not deleted.
    # ★ The artefact computes, per panel, WHICH of these steps re-check it, and renders a red
    # "NOTHING RE-CHECKS THIS" where the answer is none. Until this row existed it fired that
    # about ITSELF — which is the whole argument for the row. Build-step counts come from
    # _gen_chain._steps_in, the function itself and never a copy (one slicer, s125-D1).
    ("memento schematic — the six subsystems, generated from the file inventory (#127)",
     "_gen_schematic.py"),
    ("memento schematic determinism check — a stale diagram publishes a PREVIOUS tree (#127)",
     "_gen_schematic.py", ["--check"]),
    ("memento schematic selftest — figure provenance, caption geometry, self-recheck (#127)",
     "_gen_schematic.py", ["--selftest"]),
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
    # #193: the COULD-NOT-ASK convention (exit 77 + a marked line) is read by `_build_survey.py`
    # and written by four gates. Its own bites are wired HERE because a selftest nothing runs is
    # the [[instrument-without-a-consumer]] class — and this one guards the exact codes every
    # consumer branches on. APPENDED, never inserted: step indices are quoted in comments,
    # commit messages and the CI notes, and renumbering them would silently invalidate all of it.
    ("integrity lint (gate)", "_build_integrity.py"),
    ("could-not-ask convention selftest (#193 — the third verdict's exit code + marker)",
     "_could_not_ask.py", ["--selftest"]),
    # ── #208 · W-44 + W-45 WIRED, the `s204-D1` precondition MET ────────────────────────────
    # `s204-D1` held both instruments OUT of this file and CI *until driven in >= 1 real
    # verifier wave*. That wave ran this session: three PM claim tables (55 rows) and a
    # 55-challenge adversarial run, 51 CONFIRMED / 2 CONTRADICTED, receipt at
    # `notes/_receipts/2026-08-19-208-verifier-wave.md`. Dave ruled the wiring.
    # ⚠ APPENDED, never inserted (see the note above) — and EVERY one of these three carries a
    # ROUTE_ROWS row landing in the SAME edit: a STEPS entry with no route aborts every full
    # build above step 1 (the #119/#164 class, recorded four times in the route table).
    #
    # W-45 · the probe registry. Drives every historically-found defect class as a SCRIPT so
    # the next verifier does not re-derive the hunt from memory. ADVISORY, deliberately:
    # promoting any probe to a BLOCKING build gate is DAVE'S (derivation governance, and the
    # registry's own docstring says so) — wiring it as a gate here would make that ruling for
    # him. What this step buys today is that the probes RUN on every build instead of only when
    # a verifier remembers them. ⚠ A probe that REFUSES (77 + a `COULD-NOT-ASK:` line, e.g. P-3
    # needs playwright, absent in the sandbox and present in the CI `render` job) is printed in
    # its own block and does NOT fail the run — the #193 three-verdict convention.
    ("probe registry — every historically-found defect class, re-driven (W-45, advisory)",
     "_probe_registry/_registry.py", ["--run"]),
    # W-44 · the evidence linter over EVERY claim/challenge table. `s182-D1` conformance plus
    # the #208 expected-OBSERVATION sampler (an exit code is not an observation).
    # ADVISORY, and the reason is measured, not assumed: at wiring time the four #208 tables
    # are clean but the FROZEN #204/#206/#207 tables carry 6 lint failures and 3 rc mismatches
    # between them. Under ADR-0017 history is frozen, so those rows are not mine to rewrite,
    # and a gate born red is a gate that gets switched off (the #79 lesson, quoted above).
    # ⬛ FLIPPING THIS TO BLOCKING IS DAVE'S, once the historical residual is triaged.
    ("claim-table evidence linter — s182-D1 tokens + expected observations (W-44, advisory)",
     "_validate_evidence.py", ["notes/_claims"]),
    # Wave 1's punted item 4. `_governs.py --selftest` already has a consumer — `_capture_gate`
    # runs its matcher as the trigger-index arm at [12]/[13] — so this is LEGIBILITY: when the
    # matcher breaks, the build says `_governs`, not `capture gate, somewhere inside`. #208
    # spent a whole wave re-deriving exactly that diagnosis from a red [13].
    ("governs matcher selftest — the [12]/[13] trigger-index arm, named (#208 legibility)",
     "_governs.py", ["--selftest"]),
    # ---- THE RELEASE LANE (#219 R2, s219-D4(3) "CI both halves") ------------------------------
    # The survey asks the COMMITTED tree, which is exactly the right question for a freeze rule:
    # `s114-D4` says a shipped release does not move, and until #219 NOTHING checked it. Three
    # gates, and the blocking/advisory split is the house rule applied literally — a MECHANICAL
    # determinism check BLOCKS; anything PROMOTION-flavoured advises, because promotion is Dave's
    # word (`s219-D4(2)`: the release is his, not the script's, and not a gate's).
    #
    # ⚠ EACH OF THESE TAKES `--check` DELIBERATELY. `_build_survey.py` only RUNS a step whose
    # every argument is in its NON_MUTATING set (`--check` / `--selftest`) — a step with NO
    # arguments is treated as mutating and merely LISTED. These three write nothing, so they are
    # spelled `--check` in order to be ASKED rather than listed. The same trap the W-44 note
    # records one step above, from the other side.
    ("frozen-release gate — v1/v2 and any baked Spider surface may not move without a version bump "
     "(BLOCKING, s114-D4, built #219)",
     "_release/_gate_frozen_release.py", ["--check"]),
    ("frozen-release selftest — 11 bites on a fixture repo incl. the laundering mutant (#219)",
     "_release/_gate_frozen_release.py", ["--selftest"]),
    # The v2 receipt's own words for the class this ends: "v1's copy-list had gone stale — never
    # shipped canon/type.css nor tokens/themes/". A generated ship list is only better than a
    # typed one while something re-generates it and COMPARES.
    ("pack ship-list audit — the manifest is byte-identical to a fresh generation at its own "
     "commit (BLOCKING, built #219)",
     "_release/_gate_release_audit.py", ["--check"]),
    ("release-audit selftest — manifest compare + the pack arm's resting refusal (#219)",
     "_release/_gate_release_audit.py", ["--selftest"]),
    # The pack-side half. It is never run here, which is precisely why it needs a gate here.
    ("pack-side CI template — parses, ships what it calls, hides nothing (BLOCKING, built #219)",
     "_release/_gate_ci_template.py", ["--check"]),
    ("pack-side CI template selftest — 10 mutants incl. a smuggled continue-on-error (#219)",
     "_release/_gate_ci_template.py", ["--selftest"]),
    # A BAKED PACK is audited against the manifest and against the commit's own blobs. Its
    # RESTING STATE is a REFUSAL (77 + the marked line): nothing is baked, because the release is
    # Dave's word. The survey counts a refusal as the third verdict and excludes it from its exit
    # code, which is how this can be BLOCKING today without being born red.
    ("baked-pack audit — a zip in apollo-spider/dist/ must match the manifest (BLOCKING; "
     "refuses while nothing is baked) (#219)",
     "_release/_gate_release_audit.py", ["--pack"]),
    # ADVISORY ON PURPOSE, and it must stay so. A manifest generated at an older commit than HEAD
    # means a pack cut now would ship older content. That is a real fact and NOT a defect —
    # cutting from an older commit is a legitimate choice, and ⬛ WHEN TO RE-CUT IS DAVE'S
    # (s219-D4(2)). Blocking on it would be a gate making his release decision for him.
    ("pack ship-list drift — how far behind HEAD the manifest is (ADVISORY, ⬛ re-cutting is "
     "Dave's) (#219)",
     "_release/_gate_release_audit.py", ["--drift"]),
    # ── #238 lane P · THE POLARITY GATE (s238-D7) ──────────────────────────────────────────────
    # APPENDED, never inserted (the note at #193 above: step indices are quoted elsewhere). A CHECK,
    # not a regen: it reads knowledge/brain/ (the polarity home, s238-D1) and knowledge/_rulings.json,
    # both of which no step in the regen serial writes, so its position against that serial is
    # free and it sits last. Five refusals (dangling ref · untyped link · judgement field · authored
    # edge file · typed status), then a CONTENT freshness check of the three derived files under
    # knowledge/brain/_generated/ (status with a clock, s238-D3; edges, a derived view, s238-D1;
    # the s238-D5 defaults declaration). Routed GATE like its --check siblings: red + remedy at the
    # end, never a silent pass. The selftest is ABORT, like every sibling selftest here: a refusal
    # that has stopped biting is a silent instrument. The same `--check` runs at the commit seam
    # (_git_commit.sh), which is what makes it a consumer of every commit (s238-D7's last sentence).
    # ⚠ The route rows land in the SAME edit as these two entries (the (a)-class omission, recorded
    # four times above).
    ("polarity gate — five refusals + content-fresh derived status/edges/declaration "
     "(BLOCKING, s238-D7, built #238)",
     "_validate_polarities.py", ["--check"]),
    ("polarity gate selftest — control + every refusal arm on a copy of the real rows (s238-D7)",
     "_validate_polarities.py", ["--selftest"]),
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
_DASHBOARD = "\n❌ dashboard sync failed (exit {code}) — dashboard/index.html is stale against the stores (_state.json / _rulings.json / the ratchets / _CHAIN.md) or against a live gate result. The dashboard REPORTS, it never repairs: if a number is wrong the STORE is wrong. Run: python3 knowledge/gen_dashboard.py"
_DATAVIZ = "\n❌ DataViz chart gate failed (exit {code}) — see knowledge/_DATAVIZ-GATE.md"
STATE_CONTRAST_AUDIT = os.path.join(HERE, "_STATE-CONTRAST-AUDIT.md")
_SC_REFUSAL_LINE = "- ⛔ StateContrastParseError"
_SC_SNIPPET_LINE = "## "


def state_contrast_caveat(path=STATE_CONTRAST_AUDIT):
    """✅ `s129-D2` — THE PARSE CAVEAT IN THE STATE-CONTRAST REMEDY IS GENERATED, NOT TYPED.

    The sentence this replaces — "the validator's parse() cannot read color(srgb ...)
    backgrounds (every color-mix() hover), and mis-reports those as ~1:1" — was TRUE when
    written at #125, went FALSE later the same session when `s125-D3` landed, and was still
    on disk at #127, which measured 0 parse refusals across all 75 snippets and DELIBERATELY
    DID NOT RE-STAMP IT: the standing remedy for a claim that goes stale twice is GENERATE
    IT, and a third hand-correction is the move `s125-D1` exists to forbid. This function is
    that generation, and Dave ruled it at #129.

    It reads the ARTEFACT, in the artefact's own grammar — the same discipline `verify_report`
    applies inside the validator — and never a summary, a comment or a memory of a run.
    [[no-gate-parses-the-artefact]] [[gate-dont-patch]]

    ⚠ IT MUST NEVER RAISE. A remedy string is built at import time, on the failure path of a
    build; a caveat generator that crashes would take down the routing table that carries it.
    Anything it cannot measure it SAYS it cannot measure — an UNKNOWN is never defaulted to
    zero, because "0 refusals" and "I could not look" are opposite advice to the reader
    [[feedback-measuring-tool-must-not-guess]].
    """
    try:
        with open(path, encoding="utf-8") as f:
            lines = f.read().split("\n")
    except OSError as e:
        return (" ⚠ PARSE-REFUSAL COUNT UNMEASURED — knowledge/_STATE-CONTRAST-AUDIT.md could "
                f"not be read ({e.__class__.__name__}). Re-run the gate before judging any "
                "reading; this caveat is GENERATED from the artefact and there was no artefact.")
    refusals = sum(1 for l in lines if l.startswith(_SC_REFUSAL_LINE))
    snippets = sum(1 for l in lines if l.startswith(_SC_SNIPPET_LINE))
    if refusals:
        return (f" ⚠ {refusals} PARSE REFUSAL(s) in the artefact covering {snippets} snippet(s) "
                "— `StateContrastParseError`. Those elements are HOLES, not passes and not "
                "failures, and a ~1:1 reading near one may be an unread colour rather than a "
                "design defect. Verify the reading first (s125-D3).")
    return (f" ✅ 0 parse refusals measured across the {snippets} snippet(s) in the artefact, so "
            "a low reading here is a REAL measurement, not the pre-s125-D3 parse artefact. "
            "This sentence is GENERATED from knowledge/_STATE-CONTRAST-AUDIT.md at import "
            "time (s129-D2) — if it is wrong, the artefact is wrong.")


_PKGDELTA = "\n❌ memento-package delta-audit failed (exit {code}) — a package copy has drifted from its knowledge/ source, the two in-package copies disagree, an unknown file appeared in a machinery/ folder, or a shim-ported function/constant changed since its declared provenance commit. See memento-package/_PACKAGE-SPEC.md:13-14 (Dave's #64 boundary ruling: copies only, every copy delta-audited). Run: python3 knowledge/_validate_package_delta.py"

ROUTE_ROWS = [
    # (exact step label, kind, remedy template) — remedy text unchanged from the old cascade.
    # ✅ #164: the two #158 help-gate STEPS landed with NO ROUTE_ROWS rows — the exact
    # (a)-class omission the note at the four #139 entries records. ABORT like every
    # other gate+selftest pair: a write-before-argv regression must stop the build.
    ("help-gate — no entry point may write before it reads argv (#158 class gate)", ABORT, None),
    ("help-gate selftest — 5 mutation bites (#158 class gate)", ABORT, None),
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
    # ⛔ #166, DAVE'S RULING: GATE → ABORT. Both worklist arms now stop the build.
    # ⚠ The remedy string this row used to carry is NOT lost by the flip — ABORT rows carry
    # None by contract, and `_state.py` already prints every failure with the item id and the
    # offending value quoted [[gate-must-quote-what-it-forbids]]. What it said, for the record:
    #   "_state.json has an item with no checkable close condition outside the frozen legacy
    #    set, a malformed id/owner/state, or a `priority_override` that is not an integer rank
    #    in 1..999. Run: python3 knowledge/_state.py"  (+ now: a `deadline` that is not an ISO
    #    date, or an `effort` outside S/M/L).
    ("worklist store gate — open items state what would close them; optional "
     "priority_override is Dave's (#88 store, wired #165)", ABORT, None),
    ("worklist store selftest — schema presence gates incl. priority_override / deadline / "
     "effort (#165, extended #166)",
     ABORT, None),
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
    ("dashboard sync — generated progress dashboard (RULED #164, built #165)", GATE, _DASHBOARD),
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
    # #209: route row landed in the SAME edit as its STEPS entry — the (a)-class omission
    # this very list documents twice (#139, #164) and which run 32342067185 reproduced
    # anyway because the first edit carried the step WITHOUT the route. ADVISORY per the
    # instrument's own declared tier; rc=77 HARNESS UNAVAILABLE is a declared refusal upstream.
    ("hit-area gate — 44px minimum, rendered geometry (ADVISORY, built #203, wired #209)",
     ADVISORY, None),
    ("wiring gate — no orphaned validators (#118 seam)", GATE,
     "\n❌ wiring gate failed (exit {code}) — a _validate_*.py is on disk with no STEPS entry and no named exemption; wire it or exempt it BY NAME (knowledge/_validate_wiring.py)"),
    ("wiring gate selftest — 4 bites", ABORT, None),
    ("compose gate (orphan wired #119)", GATE,
     "\n❌ compose gate failed (exit {code}) — see knowledge/_validate_compose.py"),
    ("screen gate — compose+icons+a11y over fitness fixtures (re-wired #120)", GATE,
     "\n❌ screen gate failed (exit {code}) — a _fitness-test canon fixture fails compose/icon-source/a11y; see knowledge/_validate_screen.py output"),
    ("state-contrast gate — driven hover/pressed, light+dark (un-exempted #125)", GATE,
     "\n❌ state-contrast gate failed (exit {code}) — a driven hover/pressed state measures below 4.5:1 (large 3.0:1) in light or dark; see knowledge/_STATE-CONTRAST-AUDIT.md."
     + state_contrast_caveat()),
    # ✅ #129 — THE DECISION RAISED AT #127 CAME BACK AS `s129-D2`, AND THE ANSWER WAS GENERATE.
    # What used to sit here was a hand-typed caveat ("parse() cannot read color(srgb ...) ...
    # mis-reports those as ~1:1"), true at #125, false by the end of that same session once
    # s125-D3 landed, and STILL ON DISK at #127 — a THIRD instance, in a THIRD place, of the
    # claim-gone-false class this file documents twice above. #127 refused to hand-correct it a
    # third time and left it as EVIDENCE with the question raised to Dave. He ruled: the caveat
    # is now COMPUTED by state_contrast_caveat() from the artefact itself, at import time.
    # ⚠ THE COMMENT BLOCK ABOVE THIS ROW IS STILL STRATIFIED AND STILL PARTLY FALSE BY DATE,
    # AND THAT IS DELIBERATE — it is the RECORD of how the class was found, corrected twice and
    # finally removed from human hands. It is not the remedy any longer; the remedy is a
    # function, and a function cannot go stale without the artefact going stale with it.
    ("state-contrast gate selftest — paint stack, report arithmetic, named args", ABORT, None),
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
    ("dataviz var-resolution gate — markup fill/stroke var() per theme (BLOCKING s191-D3, ds-0NN #184)", GATE,
     "\n❌ dataviz var-resolution gate failed (exit {code}) — a chart colour var() resolves in NO theme and would render SILENT BLACK (s191-D3, promoted from advisory on Dave's word #191). Run: python3 knowledge/_gate_dataviz_vars.py"),
    ("dataviz var-resolution gate selftest — 8 arms incl. alias chain + missing target (ds-0NN)", ABORT, None),
    # ADVISORY, deliberately — the inventory always exits 0; only an unrunnable inventory (exit 2)
    # would surface here. The SELFTEST is ABORT like its siblings: an inventory whose mutants stop
    # going red is a measuring tool that has quietly stopped measuring.
    ("minted-token consumption inventory — declared-but-never-read (ADVISORY, built #219)", ADVISORY, None),
    ("minted-consumption selftest — 10 arms incl. both false-positive mutants (#219)", ABORT, None),
    # ADVISORY, deliberately — the sweep always exits 0 and writes nothing; it is a triage
    # reader, not a repair. The SELFTEST is ABORT like its siblings: this one's mutant arm is
    # driven on the REAL #218 instance (delete Dave's ruled one-liner from Command-palette and
    # the original phantom option is re-named), so a green that stops going red on removal means
    # the instrument has quietly stopped measuring the clause it was built for.
    ("hidden-attr vs author-display sweep — painted while hidden (ADVISORY, built #219)", ADVISORY, None),
    ("hidden-attr display selftest — 16 bites incl. the real #218 mutant (#219)", ABORT, None),
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
    ("memento schematic — the six subsystems, generated from the file inventory (#127)", ABORT, None),
    ("memento schematic determinism check — a stale diagram publishes a PREVIOUS tree (#127)", ABORT, None),
    ("memento schematic selftest — figure provenance, caption geometry, self-recheck (#127)", ABORT, None),
    ("memento-package delta-audit — #64 boundary enforcement (#79)", GATE, _PKGDELTA),
    ("memento-package delta-audit selftest — mutation-tested, all 4 arms (#79)", GATE, _PKGDELTA),
    ("enactment register — is each ruling IN FORCE? (advisory, ADR-0016)", ADVISORY, None),
    ("instrument-fit selftest (advisory, ds-015)", ADVISORY, None),
    ("instrument fit — can the gate SEE the property? (advisory, ds-015)", ADVISORY, None),
    ("integrity lint (gate)", GATE,
     "\n❌ integrity gate failed (exit {code}) — see knowledge/_INTEGRITY-REPORT.md"),
    # #193: GATE, not ADVISORY. Four gates and the survey branch on the exact code and marker
    # this selftest asserts; if they drift apart, a refusal silently becomes a failure again (or,
    # far worse, a failure silently becomes a refusal) and the survey's exit stops meaning
    # anything. ⚠ The row landed WITH the step, in the same edit — a STEPS entry with no route is
    # the (a)-class omission recorded three times above, and `_gen_schematic --selftest` catches
    # it (it did, on this very change: "1 unrouted").
    ("could-not-ask convention selftest (#193 — the third verdict's exit code + marker)", GATE,
     "\n❌ could-not-ask convention selftest failed (exit {code}) — the refusal exit code or its "
     "`COULD-NOT-ASK:` marker has drifted from what _build_survey.py and four gates branch on. "
     "Run: python3 knowledge/_could_not_ask.py --selftest"),
    # #146: rows for the four #139 steps that landed in STEPS with no route — the gap that
    # aborted every build since #139 (check_routes raised UNKNOWN STEP ID before step 1).
    ("KG edge parse-gate + s135-D4 resolutions-consumed check", GATE,
     "\n❌ KG edge gate failed (exit {code}) — an edge fails parse in the consumer's grammar, or a s135-D4 resolution is unconsumed. Run: python3 knowledge/_validate_kg.py"),
    ("KG edge gate selftest (6 bites)", GATE,
     "\n❌ KG edge gate selftest failed (exit {code}) — python3 knowledge/_validate_kg.py --selftest"),
    ("Token fork-ban gate — undeclared same-scope forks (s136-D1 lane, #139)", GATE,
     "\n❌ token fork-ban gate failed (exit {code}) — an undeclared same-scope fork of a spine token. Declare it or unify. Run: python3 knowledge/_validate_token_forks.py"),
    ("Token fork-ban selftest (2-direction)", GATE,
     "\n❌ token fork-ban selftest failed (exit {code}) — python3 knowledge/_validate_token_forks.py --selftest"),
    # #146: the three gates wired this pass (see the STEPS comment for the layered-orphan story).
    ("binds shrink-only ratchet (s136-D1 axis A; built #141, wired #146)", GATE,
     "\n❌ binds ratchet failed (exit {code}) — meta-level binds coverage fell below the recorded floor (shrink-only debt). Never lower the floor; restore the binds or raise coverage. Run: python3 knowledge/_validate_binds_ratchet.py"),
    ("DTCG spine conformance gate (s141-D1 axis A; built #141, wired #146)", GATE,
     "\n❌ DTCG conformance failed (exit {code}) — a spine token breaks DTCG shape ($value/$type). Run: python3 knowledge/_validate_dtcg.py"),
    ("binds-resolve gate — manifest presence + address→store resolution (#146)", GATE,
     "\n❌ binds-resolve gate failed (exit {code}) — a reference.html lost its token-manifest, a manifest var no longer resolves, or a meta binds address points at nothing (renamed rung / untaught store). Run: python3 knowledge/_validate_binds_resolve.py"),
    ("binds-resolve selftest — 5 bites incl. any-store clause (#146)", GATE,
     "\n❌ binds-resolve selftest failed (exit {code}) — python3 knowledge/_validate_binds_resolve.py --selftest"),
    ("chart-intent resolve gate — meta intent address → chart-intents.json (BLOCKING s195-D1)", GATE,
     "\n❌ chart-intent resolve gate failed (exit {code}) — a meta's `intent` is not a key of chart-intents.json, or the store is absent (s195-D1; the vocabulary is ADOPTED, a new word enters only by Dave's ruling). Run: python3 knowledge/_validate_intent_resolve.py"),
    ("chart-intent resolve selftest — 4 bites incl. list case + absent store (s195-D1)", GATE,
     "\n❌ chart-intent resolve selftest failed (exit {code}) — python3 knowledge/_validate_intent_resolve.py --selftest"),
    # #196: the stale-queue pair. The row landed WITH the step, in the same edit — a STEPS
    # entry with no route aborts every full build above step 1 (the (a)-class omission
    # recorded three times above).
    # FLIPPED #198 on Dave's word: s197-D1 held the gate at WARN until it survived one
    # real banner roll — MET by the #197 roll (5b77cce, GOOD-MORNING.md:522). ADVISORY ->
    # GATE here and SEVERITY -> "blocking" in _validate_queue_fresh.py moved together;
    # neither alone is the promotion. GATE tier = red + remedy at the commit seam, NOT
    # ABORT. ⚠ The label string is a routing join key duplicated in STEPS — never edit it.
    ("stale-queue gate — §C·1 qprobe claims re-measured vs disk + git (BLOCKING, #198)", GATE,
     "\n❌ stale-queue gate failed (exit {code}) — a §C·1 queue item's stated state is contradicted by disk or git, or a live item carries no qprobe tail. Run: python3 knowledge/_validate_queue_fresh.py"),
    ("stale-queue selftest — 13 bites incl. both mutation directions + scope (#196)", ABORT, None),
    # #158: the named-palette tier (s157-D2). Routed GATE, not ADVISORY — the ruling makes
    # the sharing STRUCTURAL, so an undeclared or divergent palette is a defect, not a note.
    ("palette-tier gate — every theme names a palette per family, no divergent hand-carry (s157-D2)", GATE,
     "\n❌ palette-tier gate failed (exit {code}) — a theme declares no ragPalette/neutralRamp, a declaration dangles, a palette key is silently absent, a tint became palette-owned, or a theme's override set diverges from its palette. Run: python3 knowledge/_validate_palette_tier.py"),
    ("palette-tier selftest — 10 mutation bites (s157-D2)", GATE,
     "\n❌ palette-tier selftest failed (exit {code}) — python3 knowledge/_validate_palette_tier.py --selftest"),
    # #208 — the three W-44/W-45 rows, landing in the SAME edit as their STEPS entries. The
    # label strings are ROUTING JOIN KEYS duplicated verbatim in STEPS — never edit one alone.
    ("probe registry — every historically-found defect class, re-driven (W-45, advisory)",
     ADVISORY, None),
    ("claim-table evidence linter — s182-D1 tokens + expected observations (W-44, advisory)",
     ADVISORY, None),
    # ---- THE RELEASE LANE (#219 R2) — rows land in the SAME edit as the steps. A STEPS entry
    # with no ROUTE_ROWS row aborts every build above step 1 (#119/#164), and that omission has
    # now been recorded four times in this file; it is not going to be recorded a fifth.
    ("frozen-release gate — v1/v2 and any baked Spider surface may not move without a version bump "
     "(BLOCKING, s114-D4, built #219)", GATE,
     "\n❌ frozen-release gate failed (exit {code}) — a SHIPPED release moved. s114-D4: a release "
     "is explicit, versioned and Dave's word; you do not edit one, you cut a new one. The gate "
     "names every path that changed. If the move is deliberate, re-seed the ledger AND bump that "
     "release's `version` in the same commit — the laundering arm checks that you did. Run: "
     "python3 knowledge/_release/_gate_frozen_release.py --check"),
    ("frozen-release selftest — 11 bites on a fixture repo incl. the laundering mutant (#219)",
     ABORT, None),
    ("pack ship-list audit — the manifest is byte-identical to a fresh generation at its own "
     "commit (BLOCKING, built #219)", GATE,
     "\n❌ pack ship-list audit failed (exit {code}) — knowledge/_release/_pack_manifest.json is not "
     "what its generator produces at the commit it names. Either it was hand-edited (never do "
     "this — it is the stale-copy-list defect the generated manifest exists to end) or the generator moved under it. "
     "Regenerate: python3 knowledge/_release/_gen_pack_manifest.py --probe --commit <sha> && "
     "python3 knowledge/_release/_gen_pack_manifest.py --manifest --commit <sha>"),
    ("release-audit selftest — manifest compare + the pack arm's resting refusal (#219)",
     ABORT, None),
    ("pack-side CI template — parses, ships what it calls, hides nothing (BLOCKING, built #219)",
     GATE,
     "\n❌ pack-side CI template gate failed (exit {code}) — the workflow the pack hands a "
     "designer does not parse, calls a script the pack does not carry, ships a "
     "`continue-on-error`, or its README has lost the two promises it exists to make. This half "
     "of the CI is never run in this repo, so this gate is the only thing that asks. Run: "
     "python3 knowledge/_release/_gate_ci_template.py --check"),
    ("pack-side CI template selftest — 10 mutants incl. a smuggled continue-on-error (#219)",
     ABORT, None),
    ("baked-pack audit — a zip in apollo-spider/dist/ must match the manifest (BLOCKING; "
     "refuses while nothing is baked) (#219)", GATE,
     "\n❌ baked-pack audit failed (exit {code}) — a zip in apollo-spider/dist/ does not "
     "match the manifest or the commit's own blobs. The pack is what a designer downloads; if it "
     "and the ship list disagree, the ship list is not a description of anything. Re-bake from "
     "the named commit: bash apollo-spider/build-designer-pack.sh --check <zip> "
     "--commit <sha>"),
    ("pack ship-list drift — how far behind HEAD the manifest is (ADVISORY, ⬛ re-cutting is "
     "Dave's) (#219)", ADVISORY, None),
    ("governs matcher selftest — the [12]/[13] trigger-index arm, named (#208 legibility)", GATE,
     "\n❌ governs matcher selftest failed (exit {code}) — the ruling-to-path matcher that "
     "`_capture_gate.py --selftest` runs as its trigger-index arm ([12]/[13]) is broken or too "
     "loose. Run: python3 knowledge/_governs.py --selftest"),
    # ── #238 lane P · the polarity gate's two rows, landing in the SAME edit as its STEPS entries.
    # The label strings are ROUTING JOIN KEYS duplicated verbatim in STEPS — never edit one alone.
    ("polarity gate — five refusals + content-fresh derived status/edges/declaration "
     "(BLOCKING, s238-D7, built #238)", GATE,
     "\n❌ polarity gate failed (exit {code}) — a polarity node in knowledge/brain/polarities.json "
     "carries a ref that does not resolve, an untyped link, a judgement field, a typed status, or "
     "an authored file sits at a generated path — OR the derived files under "
     "knowledge/brain/_generated/ are stale against the home. The refusal is NAMED in the output "
     "above (R1..R5 / STALE-GENERATED / MISSING-GENERATED). Fix the node, or for staleness run: "
     "python3 knowledge/_validate_polarities.py --write   (s238-D7; the same --check runs at the "
     "commit seam)"),
    ("polarity gate selftest — control + every refusal arm on a copy of the real rows (s238-D7)",
     ABORT, None),
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
    # (d) `s129-D2` — THE STATE-CONTRAST CAVEAT IS GENERATED, AND THIS IS WHAT RE-CHECKS IT.
    # A permanent bite, on the s125-D1 precedent: the ruling is not "the sentence is currently
    # right", it is "no human types this sentence again". So the arm drives the generator over
    # synthetic artefacts and asserts the OUTPUT MOVES WITH THE INPUT — a re-typed constant
    # string would sail through arm (a) and die here.
    import tempfile as _tf
    _d = _tf.mkdtemp(prefix="sc-caveat-bite-")
    _clean = os.path.join(_d, "clean.md"); _dirty = os.path.join(_d, "dirty.md")
    with open(_clean, "w", encoding="utf-8") as fh:
        fh.write("## Alpha — ✅ clean\n\n## Beta — ✅ clean\n")
    with open(_dirty, "w", encoding="utf-8") as fh:
        fh.write("## Alpha — x\n" + _SC_REFUSAL_LINE + " [light/hover] cannot parse color: `oklab(1)` on a\n")
    c_clean, c_dirty = state_contrast_caveat(_clean), state_contrast_caveat(_dirty)
    c_gone = state_contrast_caveat(os.path.join(_d, "absent.md"))
    assert "0 parse refusals" in c_clean and "2 snippet(s)" in c_clean, \
        f"caveat did not read a clean artefact: {c_clean!r}"
    assert "1 PARSE REFUSAL(s)" in c_dirty, \
        f"caveat did not move with a refusal in the artefact — it is typed, not generated: {c_dirty!r}"
    assert c_clean != c_dirty, "the caveat is CONSTANT across opposite artefacts — s129-D2 has regressed"
    assert "UNMEASURED" in c_gone and "0 parse refusals" not in c_gone, \
        f"a missing artefact must read UNMEASURED, never as zero: {c_gone!r}"
    live = ROUTES["state-contrast gate — driven hover/pressed, light+dark (un-exempted #125)"][1]
    assert live.endswith(state_contrast_caveat()), \
        "the live remedy no longer ends in the GENERATED caveat — someone re-typed it (s129-D2)"
    print("  selftest (d): state-contrast caveat is GENERATED — moves with the artefact, "
          "refuses to read a missing artefact as zero, and the live remedy carries it ✓")
    # (e) #148 chunking: a chunked pass must be contiguous, same-code, same-HEAD — and every
    # violation refuses LOUD AND NAMED. Drives _validate_chunk directly (pure), with a
    # mutation control per clause so no clause can silently stop biting.
    ok = _validate_chunk({"next": 5, "steps_total": len(STEPS), "rc": 7, "head": "H"}, 5, len(STEPS), "H")
    assert ok == 7, f"accumulated gate rc must carry across chunks, got {ok!r}"
    assert _validate_chunk(None, 1, len(STEPS), "H") == 0
    for bad_state, bad_start, bad_head, must_name in [
        (None, 3, "H", "START at step 1"),
        ({"next": 5, "steps_total": len(STEPS), "rc": 0, "head": "H"}, 6, "H", "contiguous"),
        ({"next": 5, "steps_total": len(STEPS), "rc": 0, "head": "H"}, 5, "H2", "tree moved"),
        ({"next": 5, "steps_total": 1, "rc": 0, "head": "H"}, 5, "H", "code moved"),
    ]:
        try:
            _validate_chunk(bad_state, bad_start, len(STEPS), bad_head)
        except SystemExit as e:
            assert must_name in str(e), f"refusal must name its cause ({must_name!r}): {e}"
        else:
            raise AssertionError(f"selftest (e): illegal chunk ({must_name}) was accepted — the check cannot fail")
    try:
        _parse_range("banana", len(STEPS))
    except SystemExit:
        pass
    else:
        raise AssertionError("selftest (e): garbage --range accepted")
    print("  selftest (e): chunk coverage contract — carries rc, refuses gap/HEAD-move/code-move, loud and named ✓")
    # (f) #208 ARGV CONTRACT. Every arm here runs against check_argv/main only and EXITS
    # BEFORE any build step — the refusal path returns from main() above the first
    # subprocess.run, and the accept-arms never call main() at all. Both directions on the
    # real contract: unknown tokens MUST be refused, known flags MUST still be accepted.
    for bad_argv, must_name in [
        (["notes/_briefs/whatever.md"], "UNKNOWN ARGUMENT"),   # the #204 shape: a non-flag
        (["--wrap"], "UNKNOWN ARGUMENT"),                      # a flag from another script
        (["--selftest", "--nope"], "UNKNOWN ARGUMENT"),        # legal flag + junk is JUNK
        (["--range"], "REQUIRES a value"),                     # value-taking flag, no value
        (["--range", "1-3", "--resume"], "MUTUALLY EXCLUSIVE"),
    ]:
        why = check_argv(bad_argv)
        assert why and must_name in why, \
            f"selftest (f): {bad_argv!r} was ACCEPTED or refused unnamed — got {why!r}"
    for good_argv in [[], ["--selftest"], ["--range", "1-3"], ["--resume"], ["--resume", "5"],
                      ["--resume", "--selftest"]]:
        assert check_argv(good_argv) is None, \
            f"selftest (f): the contract rejected a KNOWN form {good_argv!r} — {check_argv(good_argv)}"
    # mutation control for (f): a guard that cannot refuse must be caught. Mutant premise =
    # "every token is known" (i.e. the pre-#208 behaviour, which looked at nothing).
    _orig = dict(ARGV_FLAGS)
    try:
        ARGV_FLAGS["notes/_briefs/whatever.md"] = 0
        assert check_argv(["notes/_briefs/whatever.md"]) is None, \
            "mutation setup failed — the mutant did not make the junk token legal"
    finally:
        ARGV_FLAGS.clear(); ARGV_FLAGS.update(_orig)
    assert check_argv(["notes/_briefs/whatever.md"]), \
        "selftest (f): the mutant was not restored — the guard is now permanently blind"
    # and the REFUSAL ITSELF, driven through main(): non-zero, and no step can have run
    # because main() returns on the line before check_routes().
    assert main(["--definitely-not-a-flag"]) == 2, \
        "selftest (f): main() did not refuse unknown argv with rc=2 — it fell through to the build"
    print("  selftest (f): #208 argv contract — 5 illegal forms refused NAMED, 6 legal forms "
          "accepted, mutation control bites, main() returns rc=2 before step 1 ✓")
    print(f"selftest PASS — exact-ID failure routing over {n} steps; unknown never defaulted (#77)")
    return 0


# ---- #148: chunked execution (--range / --resume) -----------------------------------------
# A single-process full pass (~49s) dies at the sandbox ~45s call wall, and ANY partial run
# strands the tree in the documented mid-build intermediate (docstring lines 5-21). The remedy
# is a COMPLETE pass COMPOSED of contiguous chunks: state carries coverage + HEAD + accumulated
# gate rc across calls, and the verdict is REFUSED unless coverage is exactly 1..len(STEPS).
# A chunked partial can therefore never print green — the asymmetry is the mechanism.
STATE_PATH = os.environ.get("BUILD_ALL_STATE", "/var/tmp/_build_all_state.json")  # root fs 85% full — /var/tmp by runbook


def _git_head():
    r = subprocess.run(["git", "-C", HERE, "rev-parse", "HEAD"], capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else "NO-GIT"


def _validate_chunk(state, start, total, head):
    """Refuses, loud and named, unless this chunk legally extends the pass.
    Returns the accumulated rc to carry forward. Pure — selftest-drivable."""
    if state is None:
        if start != 1:
            raise SystemExit(f"❌ CHUNK REFUSED: no state at {STATE_PATH} — a pass must START at step 1, not {start}")
        return 0
    if state.get("steps_total") != total:
        raise SystemExit(f"❌ CHUNK REFUSED: state was written for {state.get('steps_total')} steps, STEPS now has {total} — the code moved mid-pass; delete the state and restart from 1")
    if state.get("head") != head:
        raise SystemExit(f"❌ CHUNK REFUSED: state HEAD {state.get('head')!r} != repo HEAD {head!r} — the tree moved mid-pass; delete the state and restart from 1")
    if state.get("next") != start:
        raise SystemExit(f"❌ CHUNK REFUSED: coverage is contiguous-only — state expects step {state.get('next')}, you asked for {start}")
    return int(state.get("rc", 0))


def _load_state():
    if not os.path.exists(STATE_PATH):
        return None
    import json
    with open(STATE_PATH, encoding="utf-8") as fh:
        return json.load(fh)


def _save_state(next_step, total, rc, head):
    import json
    with open(STATE_PATH, "w", encoding="utf-8") as fh:
        json.dump({"next": next_step, "steps_total": total, "rc": rc, "head": head}, fh)


def _parse_range(spec, total):
    try:
        a, b = spec.split("-", 1)
        a, b = int(a), int(b)
    except ValueError:
        raise SystemExit(f"❌ --range REFUSED: {spec!r} is not A-B")
    if not (1 <= a <= b <= total):
        raise SystemExit(f"❌ --range REFUSED: {spec!r} outside 1-{total}")
    return a, b


# ---- #208: the ARGV CONTRACT -------------------------------------------------------------
# THE INCIDENT: at #204 a wrap ran the FULL BUILD BY ACCIDENT. main() read argv by
# membership test only (`"--selftest" in argv`, `"--range" in argv`), so ANY token it did not
# recognise was not rejected — it was not looked at. A non-flag argument was therefore taken
# as "no flags given", which is spelled "build everything". This is the same class the
# help-gate exists for (#158/#157: `gen_showroom.py --help` REWROTE showroom/ because there
# was no argv contract at all); the fix is the same shape — an EXPLICIT contract, and an
# unknown token refuses LOUD and NAMED instead of falling through to the expensive default.
#
# The asymmetry is the point: the default path of this script is the most expensive and least
# reversible thing in the repo, so it must be reached DELIBERATELY (a bare, exactly-empty
# argv), never by a typo landing in the else-branch.
ARGV_FLAGS = {
    "--selftest": 0,       # no value
    "--range": 1,          # REQUIRES a value: A-B
    "--resume": "?",       # OPTIONAL integer value (chunk size, default 15)
}
ARGV_REMEDY = (
    "REMEDY — the whole contract, and nothing else is accepted:\n"
    "    python3 knowledge/_build_all.py                # FULL build (deliberate, no argv)\n"
    "    python3 knowledge/_build_all.py --selftest     # no step runs, nothing is written\n"
    "    python3 knowledge/_build_all.py --range A-B    # chunked pass, steps A..B\n"
    "    python3 knowledge/_build_all.py --resume [N]   # continue a chunked pass\n"
    "  If you meant the full build, run it with NO arguments at all — this script will not\n"
    "  infer it from an argument it does not understand (#204: that is how a wrap ran the\n"
    "  build by accident)."
)


def check_argv(argv):
    """Validate argv against ARGV_FLAGS. Returns None when legal; otherwise the NAMED
    reason, as a string. Pure: never builds, never writes, never exits — the caller
    decides. Kept separate from main() precisely so the selftest can bite it without
    going anywhere near a build step."""
    i = 0
    while i < len(argv):
        tok = argv[i]
        if tok not in ARGV_FLAGS:
            near = [f for f in ARGV_FLAGS if tok.lstrip("-")[:4] and tok.lstrip("-")[:4] in f]
            hint = f" (did you mean {' or '.join(near)}?)" if near else ""
            return (f"UNKNOWN ARGUMENT {tok!r}{hint} — known flags are "
                    f"{', '.join(sorted(ARGV_FLAGS))}")
        arity = ARGV_FLAGS[tok]
        if arity == 1:
            if i + 1 >= len(argv):
                return f"{tok} REQUIRES a value and none followed it"
            i += 2
        elif arity == "?":
            nxt = argv[i + 1] if i + 1 < len(argv) else None
            i += 2 if (nxt is not None and nxt not in ARGV_FLAGS and nxt.isdigit()) else 1
        else:
            i += 1
    if "--range" in argv and "--resume" in argv:
        return "--range and --resume are MUTUALLY EXCLUSIVE — one chunk contract per call"
    return None


def _refuse_argv(reason, argv):
    """The loud, named refusal. NOTHING is built and nothing is written."""
    print("=" * 72)
    print("❌ _build_all.py REFUSED — ARGV CONTRACT (#208 guard; the #204 accidental build)")
    print("=" * 72)
    print(f"  argv seen: {argv}")
    print(f"  reason:    {reason}")
    print("  ⛔ NOTHING WAS BUILT — no generator ran, no report was rewritten, no gate verdict")
    print("     was produced. This is a REFUSAL, not a build result: do not read it as green")
    print("     and do not read it as a gate failure.")
    print(ARGV_REMEDY)
    return 2


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    bad = check_argv(argv)          # #208: BEFORE anything — an unknown token never falls
    if bad:                         # through to the full build (see the note above)
        return _refuse_argv(bad, argv)
    if "--selftest" in argv:
        return selftest()          # short-circuits: the build loop below never runs
    check_routes()                 # fail loud BEFORE step 1 if STEPS and ROUTE_ROWS disagree
    total, head = len(STEPS), _git_head()
    start, end = 1, total
    chunked = False
    if "--range" in argv:
        chunked = True
        start, end = _parse_range(argv[argv.index("--range") + 1], total)
    elif "--resume" in argv:
        chunked = True
        st = _load_state()
        if st is None:
            raise SystemExit(f"❌ --resume REFUSED: no state at {STATE_PATH} — start with --range 1-N")
        start = st["next"]
        try:
            n = int(argv[argv.index("--resume") + 1])
        except (IndexError, ValueError):
            n = 15
        end = min(start + n - 1, total)
    if chunked:
        rc = _validate_chunk(_load_state(), start, total, head)
    else:
        rc = 0
    for i, step in enumerate(STEPS[start - 1:end], start):
        label, rel = step[0], step[1]
        extra_args = list(step[2]) if len(step) > 2 else []
        path = os.path.join(HERE, rel)
        print(f"\n=== [{i}/{len(STEPS)}] {label} — {rel} ===")
        r = subprocess.run([sys.executable, path] + extra_args)
        if r.returncode == 77:
            # #193 COULD-NOT-ASK (see knowledge/_could_not_ask.py): the step DECLARED an
            # input this environment cannot reach — a fact about the environment, not a
            # verdict about the tree. Counted and printed, never an abort; a silent skip
            # would be the defect, so the step's own first line has already named it.
            print(f"\n⊘ step '{label}' COULD-NOT-ASK (exit 77) — declared refusal, build continues")
            continue
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
                if chunked:
                    _save_state(i, total, rc, head)  # retry resumes AT the failed step
                    print(f"⚠ chunk state saved — resume retries step {i}")
                return r.returncode
    if chunked and end < total:
        _save_state(end + 1, total, rc, head)
        print(f"\n⚠ PARTIAL PASS — steps {start}-{end} of {total} ran; the tree is in the documented "
              f"mid-build intermediate. NO VERDICT until coverage reaches {total}. Next: --resume")
        return 0  # a clean partial exits 0; gate failures are CARRIED in state, not dropped
    if chunked:
        try:
            os.remove(STATE_PATH)
        except OSError:
            pass
        print(f"\n(composed pass: coverage 1-{total} contiguous at HEAD {head[:9]}, gate rc carried across chunks)")
    if rc == 0:
        print("\n✅ all generators ran and the integrity + contrast gates passed.")
    else:
        print("\n❌ build gate failed — see the reports above.")
    return rc


if __name__ == "__main__":
    sys.exit(main())
