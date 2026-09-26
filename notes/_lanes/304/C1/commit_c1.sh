cd "$(dirname "$0")/../../../.." || exit 1
LOG=${1:-notes/_lanes/304/C1/_gitcommit-C1.log}
SESSION_N=304 bash knowledge/_git_commit.sh --reconciled --quiet=$LOG notes/_lanes/304/C1/_msg-C1.txt \
 .gitignore \
 knowledge/_bite_goal.py knowledge/_bite_kg_edge_proposal.py knowledge/_build_kg_explorer.py knowledge/_gen_ruling_edges_from_recs.py knowledge/_kg_history.py \
 knowledge/_render/verify_demo_slides_268.py knowledge/_render/verify_demo_slides_268_v3.py knowledge/_render/verify_demo_slides_268_v5.py \
 knowledge/_render/verify_demo_slides_268_v6.py knowledge/_render/verify_demo_slides_268_v7.py knowledge/_render/verify_demo_slides_268_v74_gearbox.py knowledge/_render/verify_demo_slides_268_v75_gearbox.py \
 knowledge/_rulings.json \
 knowledge/components/navigations.meta.json knowledge/components/sidebar-nav.meta.json knowledge/components/tab-bar.meta.json \
 knowledge/snippets/Navigations.reference.html knowledge/snippets/Sidebar-nav.reference.html knowledge/snippets/Tab-bar.reference.html \
 showroom/navigations.html showroom/sidebar-nav.html showroom/tab-bar.html \
 knowledge/canon/_type-bindings.json knowledge/_TYPE-BLAST-GATE.md knowledge/_git_commit.sh knowledge/_test_git_commit.py \
 knowledge/tokens/_blast-radius.json knowledge/_GRAPH-REPORT.md knowledge/_assertions.json knowledge/README.md \
 knowledge/_state.json knowledge/_state.py \
 _CHAIN.md reviews/MEMENTO-SCHEMATIC-2026-08-07-v2.html knowledge/_memento-index.json knowledge/_graph-mark-observations.jsonl notes/_RULINGS.html \
 notes/_PROPOSAL-apollo-mcp-2026-09-26-v1.html notes/_PROPOSAL-apollo-mcp-2026-09-26-v2.html notes/_PLAN-304-roadmap-and-weekend-runs-2026-09-26-v1.html \
 notes/_DECIDE-304-ci-calls-2026-09-26-v1.html notes/_DECIDE-304-delivery-shape-2026-09-26-v1.html notes/_DECIDE-304-housekeeping-and-lines-2026-09-26-v1.html \
 notes/_DECIDE-304-schema-2026-09-26-v1.html notes/_DECIDE-304-uncertain-stamps-2026-09-26-v1.html notes/_DECIDE-304-when-rules-2026-09-26-v1.html \
 notes/_subreports/2026-09-26-304-M-apollo-mcp-proposal.md notes/_subreports/2026-09-26-304-A1-proposals-inventory.md notes/_subreports/2026-09-26-304-A2-open-work-analysis.md \
 notes/_subreports/2026-09-26-304-A3-future-state.md notes/_subreports/2026-09-26-304-A4-health-and-dependencies.md notes/_subreports/2026-09-26-304-F-roadmap-plan.md \
 notes/_subreports/2026-09-26-304-R1-ci-sees-to-146.md notes/_subreports/2026-09-26-304-R2-store-tells-the-truth.md notes/_subreports/2026-09-26-304-R5-mcp-probe.md \
 notes/_subreports/2026-09-26-304-R6a-decision-pages.md notes/_subreports/2026-09-26-304-R6b-decision-pages.md notes/_subreports/2026-09-26-304-V1-verifier-wave-one.md \
 notes/_subreports/2026-09-26-304-C1-commit-seat-wave-one.md \
 notes/_lanes/304/A1 notes/_lanes/304/A2 notes/_lanes/304/A3 notes/_lanes/304/A4 notes/_lanes/304/F notes/_lanes/304/M \
 notes/_lanes/304/R1 notes/_lanes/304/R2 notes/_lanes/304/R5 notes/_lanes/304/R6a notes/_lanes/304/R6b \
 notes/_lanes/304/C1/mint_304.py notes/_lanes/304/C1/commit_c1.sh notes/_lanes/304/C1/step1-restore12.log notes/_lanes/304/C1/step1-verify.log \
 notes/_lanes/304/C1/step3-mint.log notes/_lanes/304/C1/step4-regen.log
echo "EXIT=$?"
