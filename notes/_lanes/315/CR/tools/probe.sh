set -euo pipefail
S=/home/claude/cr/cand; C=$S/clone; export PYTHONDONTWRITEBYTECODE=1
cand=$(cat $S/CANDIDATE_SHA)
mkdir -p "$S/probe"
(cd "$C" && python3 - "$cand" > "$S/probe/_gates.txt" <<'PY'
import sys; sys.path.insert(0, "knowledge/_release")
import _gen_pack_manifest as G
sha = sys.argv[1]; paths = G.tree_paths(sha); tbl = G.groups(); gates = []
for p in paths:
    for g in tbl:
        if g["match"](p):
            if g["key"] == "gates": gates.append(p)
            break
print("\n".join(sorted(gates)))
PY
)
N=$(wc -l < "$S/probe/_gates.txt"); echo "gates: $N"
while read -r gp; do
  b="$(basename "$gp")"; [ -f "$S/probe/$b.json" ] && continue
  (cd "$C" && python3 knowledge/_release/_gen_pack_manifest.py --probe --commit "$cand" --only "$b" --probe-stage "$S/probestage" --full-stage "$S/full" --out "$S/probe/$b.json.tmp" >/dev/null) && mv "$S/probe/$b.json.tmp" "$S/probe/$b.json"
done < "$S/probe/_gates.txt"
echo "PROBE COMPLETE: $(ls "$S/probe"/*.json | wc -l)/$N gates"
