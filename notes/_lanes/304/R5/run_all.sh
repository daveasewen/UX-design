#!/usr/bin/env bash
# R5 — re-run the whole probe in one go, each script under the write audit; log to RUN-LOG.txt.
# Needs: python3 (seat, 3.10, jsonschema 3.2) and $HOME/.r5venv (jsonschema 4.23) — see NOTES.md.
set -u
cd "$(dirname "$0")/../../../.."          # repo root
L=notes/_lanes/304/R5
export PYTHONDONTWRITEBYTECODE=1
VPY="$HOME/.r5venv/bin/python"
{
echo "run_utc: $(date -u +%FT%TZ)  head: $(git --no-optional-locks rev-parse --short=8 HEAD)"
echo "inputs sha256:"
sha256sum knowledge/_rulings.json knowledge/when-fields.json knowledge/shapes.json knowledge/roles.json knowledge/chart-intents.json knowledge/components/meta.schema.json showroom/index.json knowledge/_validate_a11y.py knowledge/_a11y_target.py knowledge/_compose_slice.py | sed 's/^/  /'
echo "  metas(concat)    $(cat $(ls knowledge/components/*.meta.json | sort) | sha256sum | cut -c1-64)"
echo "  snippets(concat) $(cat $(ls knowledge/snippets/*.reference.html | sort) | sha256sum | cut -c1-64)"
echo "  newest meta: $(ls -t --time-style=+%FT%T -l knowledge/components/*.meta.json | head -1 | awk '{print $6, $7}')"
echo "--- 5a catalogue";          python3 $L/write_audit.py $L/gen_catalogue.py
echo "--- 5a A2UI validation";    "$VPY" $L/write_audit.py $L/validate_a2ui.py
echo "--- 5a harness mutations"; "$VPY" $L/write_audit.py $L/validate_mutations.py
echo "--- 5a levels";             python3 $L/write_audit.py $L/summarise_catalogue.py
echo "--- 5b gate in memory";     "$VPY" $L/write_audit.py $L/gate_mem.py
echo "--- 5c when-evaluator";     python3 $L/write_audit.py $L/when_eval.py
echo "--- 5c what-if";           python3 $L/write_audit.py $L/when_whatif.py
echo "outputs sha256:"; sha256sum $L/catalogue-all.json $L/catalogue-dashboard.json | sed 's/^/  /'
} 2>&1 | tee $L/RUN-LOG.txt
