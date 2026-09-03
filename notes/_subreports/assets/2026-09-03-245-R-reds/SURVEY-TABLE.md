| step | command | working tree (33062c1 + lanes' edits) | CI proxy (bare clone @ 9628bae, --timeout 60) | first line of failure / refusal |
|---:|---|---|---|---|
| 1 | `compliance/_build_compliance_kg.py` | not asked (mutating) | not asked (mutating) |  |
| 2 | `tokens/_build_blast_radius.py` | not asked (mutating) | not asked (mutating) |  |
| 3 | `tokens/_build_blast_radius.py --check` | pass | pass |  |
| 4 | `tokens/_build_blast_radius.py --selftest` | pass | pass |  |
| 5 | `guidelines/gen_rules_index.py` | not asked (mutating) | not asked (mutating) |  |
| 6 | `gen_runbook_index.py` | not asked (mutating) | not asked (mutating) |  |
| 7 | `_validate_standing_instructions.py` | not asked (mutating) | not asked (mutating) |  |
| 8 | `_validate_help_gate.py` | not asked (mutating) | not asked (mutating) |  |
| 9 | `_validate_help_gate.py --selftest` | pass | pass |  |
| 10 | `_validate_assertions.py` | not asked (mutating) | not asked (mutating) |  |
| 11 | `_validate_assertions.py --selftest` | pass | pass |  |
| 12 | `_capture_gate.py --build` | not asked (mutating) | not asked (mutating) |  |
| 13 | `_capture_gate.py --selftest` | TIMEOUT@25s/120s → **pass** (exit 0, 156.9s, run alone after fix) | **FAIL → 77 after fix** | `M10: a 24-fat-line banner did not warn the chain — the budget does not bite on the one region the chain is made of` (clone, exit 1 in 8s); locally TIMEOUT at 25s/120s = mount I/O, full run exit 0 in 157s after fix |
| 14 | `_gauge_tokens.py --selftest` | pass | pass |  |
| 15 | `_roll_state.py --selftest` | pass | pass |  |
| 16 | `_test_git_commit.py --selftest` | pass | pass |  |
| 17 | `_gm_move.py --selftest` | pass | pass |  |
| 18 | `_gm_usage.py --selftest` | FAIL | FAIL | `session #218 testifies DIFFERENTLY in notes/_GAUGE-LOG.md and notes/_GAUGE-LOG.md — one of them is false and this reader cannot tell which. REFUSED.` |
| 19 | `_gen_lanes.py` | not asked (mutating) | not asked (mutating) |  |
| 20 | `_gen_lanes.py --check` | pass | pass |  |
| 21 | `_gen_lanes.py --selftest` | pass | pass |  |
| 22 | `_build_xref_index.py` | not asked (mutating) | not asked (mutating) |  |
| 23 | `_build_sutherland_fixtures.py` | not asked (mutating) | not asked (mutating) |  |
| 24 | `_build_states_probe.py` | not asked (mutating) | not asked (mutating) |  |
| 25 | `_state.py` | not asked (mutating) | not asked (mutating) |  |
| 26 | `_state.py --selftest` | pass | pass |  |
| 27 | `_build_decision_graph.py` | not asked (mutating) | not asked (mutating) |  |
| 28 | `_build_decision_graph.py --selftest` | pass | pass |  |
| 29 | `_build_live_state.py --selftest` | pass | pass |  |
| 30 | `_build_live_state.py` | not asked (mutating) | not asked (mutating) |  |
| 31 | `_validate_advisory.py` | not asked (mutating) | not asked (mutating) |  |
| 32 | `_build_review_queue.py` | not asked (mutating) | not asked (mutating) |  |
| 33 | `_build_dark_mode_audit.py` | not asked (mutating) | not asked (mutating) |  |
| 34 | `_build_surface_contrast_audit.py` | not asked (mutating) | not asked (mutating) |  |
| 35 | `_build_indicator_contrast_audit.py` | not asked (mutating) | not asked (mutating) |  |
| 36 | `_build_icon_contrast_delta.py` | not asked (mutating) | not asked (mutating) |  |
| 37 | `_validate_dark_surfaces.py` | not asked (mutating) | not asked (mutating) |  |
| 38 | `gen_component_partials.py --check` | pass | pass |  |
| 39 | `gen_component_partials.py --selftest` | pass | pass |  |
| 40 | `gen_token_ramp.py --check` | pass | pass |  |
| 41 | `gen_token_ramp.py --selftest` | pass | pass |  |
| 42 | `_validate_behaviour.py` | not asked (mutating) | not asked (mutating) |  |
| 43 | `_validate_behaviour.py --selftest` | pass | pass |  |
| 44 | `canon/gen_canon_components.py` | not asked (mutating) | not asked (mutating) |  |
| 45 | `canon/gen_canon_components.py --check` | pass | pass |  |
| 46 | `_validate_partials.py` | not asked (mutating) | not asked (mutating) |  |
| 47 | `_validate_partials.py --selftest` | pass | pass |  |
| 48 | `gen_snippet_tokens.py --check --quiet` | not asked (mutating) | not asked (mutating) |  |
| 49 | `_validate_snippets.py` | not asked (mutating) | not asked (mutating) |  |
| 50 | `canon/gen_theme_cascade.py --check` | pass | pass |  |
| 51 | `canon/gen_theme_cascade.py --selftest` | pass | pass |  |
| 52 | `_validate_state_snap.py` | not asked (mutating) | not asked (mutating) |  |
| 53 | `_validate_state_snap.py --selftest` | pass | pass |  |
| 54 | `_validate_queue_fresh.py` | not asked (mutating) | not asked (mutating) |  |
| 55 | `_validate_queue_fresh.py --selftest` | pass | pass |  |
| 56 | `_validate_palette_tier.py` | not asked (mutating) | not asked (mutating) |  |
| 57 | `_validate_palette_tier.py --selftest` | pass | pass |  |
| 58 | `_validate_radius.py` | not asked (mutating) | not asked (mutating) |  |
| 59 | `gen_showroom.py --check` | pass | pass |  |
| 60 | `gen_showroom.py --selftest` | pass | pass |  |
| 61 | `gen_dashboard.py --check` | FAIL | COULD-NOT-ASK | `gen_dashboard --check FAIL — dashboard/index.html is OUT OF SYNC` (committed render is session #228); clone: COULD-NOT-ASK (untracked `outputs/…` evidence) |
| 62 | `_validate_legacy_leak.py` | not asked (mutating) | not asked (mutating) |  |
| 63 | `_validate_theme_provenance.py` | not asked (mutating) | not asked (mutating) |  |
| 64 | `_validate_token_tiers.py` | not asked (mutating) | not asked (mutating) |  |
| 65 | `_validate_icons.py` | not asked (mutating) | not asked (mutating) |  |
| 66 | `_validate_a11y.py` | not asked (mutating) | not asked (mutating) |  |
| 67 | `_validate_a11y.py --selftest` | pass | pass |  |
| 68 | `_validate_hit_area.py --all` | not asked (mutating) | not asked (mutating) |  |
| 69 | `_validate_wiring.py` | not asked (mutating) | not asked (mutating) |  |
| 70 | `_validate_wiring.py --selftest` | pass | pass |  |
| 71 | `_validate_compose.py` | not asked (mutating) | not asked (mutating) |  |
| 72 | `_validate_screen.py` | not asked (mutating) | not asked (mutating) |  |
| 73 | `_validate_state_contrast.py` | not asked (mutating) | not asked (mutating) |  |
| 74 | `_validate_state_contrast.py --selftest` | COULD-NOT-ASK | COULD-NOT-ASK | `COULD-NOT-ASK: chromium would not launch on this box` (proof of record = `render` job, GREEN in #482) |
| 75 | `_validate_type_composites.py --ratchet` | not asked (mutating) | not asked (mutating) |  |
| 76 | `_validate_type_composites.py --selftest` | pass | pass |  |
| 77 | `_validate_coverage.py` | not asked (mutating) | not asked (mutating) |  |
| 78 | `_validate_proforma.py` | not asked (mutating) | not asked (mutating) |  |
| 79 | `_validate_css_governed.py` | not asked (mutating) | not asked (mutating) |  |
| 80 | `_validate_no_hardcode.py` | not asked (mutating) | not asked (mutating) |  |
| 81 | `_validate_grid.py` | not asked (mutating) | not asked (mutating) |  |
| 82 | `_validate_type_blast_radius.py` | not asked (mutating) | not asked (mutating) |  |
| 83 | `_validate_descender_clip.py` | not asked (mutating) | not asked (mutating) |  |
| 84 | `_validate_kg.py` | not asked (mutating) | not asked (mutating) |  |
| 85 | `_validate_kg.py --selftest` | pass | pass |  |
| 86 | `_validate_token_forks.py` | not asked (mutating) | not asked (mutating) |  |
| 87 | `_validate_token_forks.py --selftest` | pass | pass |  |
| 88 | `_validate_binds_ratchet.py` | not asked (mutating) | not asked (mutating) |  |
| 89 | `_validate_dtcg.py` | not asked (mutating) | not asked (mutating) |  |
| 90 | `_validate_binds_resolve.py` | not asked (mutating) | not asked (mutating) |  |
| 91 | `_validate_binds_resolve.py --selftest` | pass | pass |  |
| 92 | `_validate_intent_resolve.py` | not asked (mutating) | not asked (mutating) |  |
| 93 | `_validate_intent_resolve.py --selftest` | pass | pass |  |
| 94 | `_validate_dataviz.py` | not asked (mutating) | not asked (mutating) |  |
| 95 | `_validate_dataviz.py --selftest` | pass | pass |  |
| 96 | `_validate_property_resolves.py --strict` | not asked (mutating) | not asked (mutating) |  |
| 97 | `_validate_property_resolves.py --selftest` | pass | pass |  |
| 98 | `_gate_dataviz_vars.py` | not asked (mutating) | not asked (mutating) |  |
| 99 | `_gate_dataviz_vars.py --selftest` | pass | pass |  |
| 100 | `_gate_minted_consumption.py` | not asked (mutating) | not asked (mutating) |  |
| 101 | `_gate_minted_consumption.py --selftest` | pass | pass |  |
| 102 | `_validate_hidden_display.py` | not asked (mutating) | not asked (mutating) |  |
| 103 | `_validate_hidden_display.py --selftest` | pass | pass |  |
| 104 | `_validate_edge_extremity.py` | not asked (mutating) | not asked (mutating) |  |
| 105 | `compliance/_build_verification_edges.py` | not asked (mutating) | not asked (mutating) |  |
| 106 | `compliance/_import_axe_rules.py` | not asked (mutating) | not asked (mutating) |  |
| 107 | `_build_consult_index.py` | not asked (mutating) | not asked (mutating) |  |
| 108 | `_consult.py --selftest` | pass | pass |  |
| 109 | `_search_core.py --selftest` | pass | pass |  |
| 110 | `_build_memento_index.py` | not asked (mutating) | not asked (mutating) |  |
| 111 | `_build_memento_index.py --check` | pass | pass |  |
| 112 | `_build_memento_index.py --selftest` | pass | pass |  |
| 113 | `_memento_search.py --selftest` | pass | pass |  |
| 114 | `_build_graph_mention_map.py` | not asked (mutating) | not asked (mutating) |  |
| 115 | `_build_graph_mention_map.py --check` | pass | pass |  |
| 116 | `_build_graph_mention_map.py --selftest` | pass | pass |  |
| 117 | `_gen_chain.py` | not asked (mutating) | not asked (mutating) |  |
| 118 | `_gen_chain.py --check` | pass | pass |  |
| 119 | `_gen_chain.py --selftest` | pass | pass |  |
| 120 | `_gen_schematic.py` | not asked (mutating) | not asked (mutating) |  |
| 121 | `_gen_schematic.py --check` | COULD-NOT-ASK | COULD-NOT-ASK | `COULD-NOT-ASK: … committed page carries figures in ['real']; the only tier reachable HERE is tape (cl100k ESTIMATE)` |
| 122 | `_gen_schematic.py --selftest` | COULD-NOT-ASK | COULD-NOT-ASK | same key as [121] |
| 123 | `_validate_package_delta.py` | not asked (mutating) | not asked (mutating) |  |
| 124 | `_validate_package_delta.py --selftest` | FAIL | FAIL | `VERBATIM SET: memento-package/machinery/_gen_chain.py DIFFERS from knowledge/_gen_chain.py … 23 line(s) differ (sha256 9a133a837646 vs source 42e4887e89ba)` ×2 copies |
| 125 | `_build_enactment_register.py` | not asked (mutating) | not asked (mutating) |  |
| 126 | `_build_instrument_fit.py --selftest` | TIMEOUT@25s → **pass** @120s (29.1s) | pass | TIMEOUT at 25s only; alone at 120s: pass in 29.1s |
| 127 | `_build_instrument_fit.py` | not asked (mutating) | not asked (mutating) |  |
| 128 | `_build_integrity.py` | not asked (mutating) | not asked (mutating) |  |
| 129 | `_could_not_ask.py --selftest` | pass | pass |  |
| 130 | `_probe_registry/_registry.py --run` | not asked (mutating) | not asked (mutating) |  |
| 131 | `_validate_evidence.py notes/_claims` | not asked (mutating) | not asked (mutating) |  |
| 132 | `_governs.py --selftest` | pass | COULD-NOT-ASK | clone only: COULD-NOT-ASK (the three gitignored `ds-034/035` `outputs/…` pointers) |
| 133 | `_release/_gate_frozen_release.py --check` | pass | pass |  |
| 134 | `_release/_gate_frozen_release.py --selftest` | pass | pass |  |
| 135 | `_release/_gate_release_audit.py --check` | pass | pass |  |
| 136 | `_release/_gate_release_audit.py --selftest` | FAIL | FAIL | `the manifest reads version 'v1.0.5' and NO zip in dist/ carries it` — conductor-diagnosed, clears at the v1.0.6 cut |
| 137 | `_release/_gate_ci_template.py --check` | pass | pass |  |
| 138 | `_release/_gate_ci_template.py --selftest` | pass | pass |  |
| 139 | `_release/_gate_release_audit.py --pack` | not asked (mutating) | not asked (mutating) |  |
| 140 | `_release/_gate_release_audit.py --drift` | not asked (mutating) | not asked (mutating) |  |
| 141 | `_validate_polarities.py --check` | pass | pass |  |
| 142 | `_validate_polarities.py --selftest` | pass | pass |  |
