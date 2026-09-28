# #306 V - the regen serial (copied from U), T's regen.sh plus knowledge/gen_kg_titles.py --write (CI went red on it today, fe243c6c).
cd "$(dirname "$0")/../../../.." || exit 1
export GIT_OPTIONAL_LOCKS=0 PYTHONDONTWRITEBYTECODE=1
LOG=${1:?log path}; : > "$LOG"
run() { s=$(date +%s); out=$("$@" 2>&1); rc=$?; echo "$* rc=$rc ($(( $(date +%s)-s ))s) :: $(echo "$out" | grep -v '^\s*$' | tail -1 | cut -c1-220)" | tee -a "$LOG"; }
run python3 knowledge/gen_dashboard.py
echo "--- serial" | tee -a "$LOG"
run python3 knowledge/_render_rulings.py
run python3 knowledge/tokens/_build_blast_radius.py
run python3 knowledge/_build_memento_index.py
run python3 knowledge/_build_graph_mention_map.py
run python3 knowledge/gen_kg_titles.py --write
run python3 knowledge/_gen_chain.py
run python3 knowledge/_gen_schematic.py
echo "--- checks" | tee -a "$LOG"
run python3 knowledge/_render_rulings.py --check
run python3 knowledge/tokens/_build_blast_radius.py --check
run python3 knowledge/_build_memento_index.py --check
run python3 knowledge/_build_graph_mention_map.py --check
run python3 knowledge/gen_kg_titles.py --check
run python3 knowledge/_gen_chain.py --check
run python3 knowledge/_gen_schematic.py --check
