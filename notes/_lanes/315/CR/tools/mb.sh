set -euo pipefail
S=/home/claude/cr/cand; C=$S/clone; export PYTHONDONTWRITEBYTECODE=1; cand=$(cat $S/CANDIDATE_SHA)
(cd "$C" && python3 - "$S" "$cand" <<'PY'
import sys, json, os; sys.path.insert(0, "knowledge/_release")
import _gen_pack_manifest as G
S, sha = sys.argv[1], sys.argv[2]
order = open(os.path.join(S, "probe/_gates.txt")).read().split()
chunks = [json.load(open(os.path.join(S, "probe", os.path.basename(p) + ".json"))) for p in order]
assert all(c["commit"] == sha and c["differential_arm"] == "ARMED" for c in chunks)
gates = [g for c in chunks for g in c["gates"]]
probe = dict(commit=sha, timeout_s=chunks[0]["timeout_s"], differential_arm="ARMED", full_stage=chunks[0]["full_stage"], gates=gates)
open(G.PROBE_PATH, "w").write(G.canonical(probe))
import collections; print("probe merged:", len(gates), dict(collections.Counter(g["verdict"] for g in gates)))
PY
)
(cd "$C" && python3 knowledge/_release/_gen_pack_manifest.py --manifest --commit "$cand") 2>&1 | tail -8
