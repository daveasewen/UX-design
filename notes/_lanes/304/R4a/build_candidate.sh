#!/usr/bin/env bash
# R4a — build the Spider v1.0.14 CANDIDATE pack in a SCRATCH clone. Never touches the repo, its index,
# its refs or apollo-spider/dist. Not a release: no ratification, no frozen-release gate, no push.
#
# WHY A CLONE. The pack builder reads a NAMED COMMIT through git archive (never the working tree), and
# the reader + Constitution ship only when VERSION >= READER_SHIPS_FROM ("v1.0.14", s279-D1). So the
# candidate is: <base commit> + the working-tree skill(s) + VERSION/MEMENTO_CUT_VERSION = v1.0.14 and the
# four Gumdrop/FIRST-SESSION literals swept, committed IN THE CLONE ONLY with fixed dates (deterministic).
# The clone borrows the repo's objects read-only (git clone --shared); its own commit writes only into
# the clone's object store.
#
# USAGE (at Dave's seat, one step per call — each step fits the 180 s cap; probe is resumable):
#   bash notes/_lanes/304/R4a/build_candidate.sh prep  [BASE_SHA]   # clone + overlay + candidate commit
#   bash notes/_lanes/304/R4a/build_candidate.sh full                # git-archive full stage (differential arm)
#   bash notes/_lanes/304/R4a/build_candidate.sh probe               # repeat until it prints PROBE COMPLETE
#   bash notes/_lanes/304/R4a/build_candidate.sh manifest            # merge probe chunks -> manifest
#   bash notes/_lanes/304/R4a/build_candidate.sh bake                # build-designer-pack.sh --dry-run -> zip
#   bash notes/_lanes/304/R4a/build_candidate.sh check               # --check + pack-docs --strict + counts
# Output: $S/out/Apollo-Spider-v1.0.14.zip  (S defaults to $HOME/r4a-scratch/cand)
set -euo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../.." && pwd)"
S="${R4A_SCRATCH:-$HOME/r4a-scratch/cand}"
C="$S/clone"
OVERLAY=("apollo-spider/skills/generate-from-canon/SKILL.md")
LITERALS=("apollo-spider/FIRST-SESSION.md" "apollo-spider/gumdrop/_state.json"
          "apollo-spider/gumdrop/runbooks/_RUNBOOK-capture-ritual.md"
          "apollo-spider/gumdrop/runbooks/_RUNBOOK-context-gauge.md")
export PYTHONDONTWRITEBYTECODE=1
step="${1:-}"; shift || true
gen() { (cd "$C" && python3 knowledge/_release/_gen_pack_manifest.py "$@"); }
cand() { cat "$S/CANDIDATE_SHA"; }

case "$step" in
prep)
  BASE="${1:-$(git -C "$REPO" --no-optional-locks rev-parse HEAD)}"
  AVAIL=$(df -Pk "$HOME" | awk 'NR==2{print $4}')
  [ "$AVAIL" -gt 2600000 ] || { echo "REFUSED: under 2.6 GB free on \$HOME ($AVAIL KB)"; exit 2; }
  rm -rf "$S"; mkdir -p "$S"
  git clone --quiet --shared --no-checkout "$REPO" "$C"
  git -C "$C" sparse-checkout init --no-cone
  printf '/*\n!/notes/_lanes/\n!/apollo-spider/dist/\n!/notes/_subreports/\n' > "$C/.git/info/sparse-checkout"
  git -C "$C" checkout --quiet "$BASE"
  for f in "${OVERLAY[@]}"; do cp "$REPO/$f" "$C/$f"; done
  sed -i 's/^VERSION = "v1\.0\.13"/VERSION = "v1.0.14"/; s/^MEMENTO_CUT_VERSION = "v1\.0\.13"/MEMENTO_CUT_VERSION = "v1.0.14"/' \
      "$C/knowledge/_release/_gen_pack_manifest.py"
  grep -q '^VERSION = "v1.0.14"' "$C/knowledge/_release/_gen_pack_manifest.py" || { echo "REFUSED: VERSION literal not found"; exit 2; }
  for f in "${LITERALS[@]}"; do sed -i 's/Apollo-Spider-v1\.0\.13/Apollo-Spider-v1.0.14/g; s/Gumdrop v1\.0\.13/Gumdrop v1.0.14/g' "$C/$f"; done
  D="$(git -C "$C" show -s --format=%cI "$BASE")"
  git -C "$C" add -A -- "${OVERLAY[@]}" knowledge/_release/_gen_pack_manifest.py "${LITERALS[@]}"
  GIT_AUTHOR_DATE="$D" GIT_COMMITTER_DATE="$D" git -C "$C" -c user.name="R4a scratch" \
      -c user.email="r4a@scratch.invalid" commit --quiet -m "R4a SCRATCH candidate v1.0.14 over ${BASE:0:8} (not a release)"
  git -C "$C" rev-parse HEAD > "$S/CANDIDATE_SHA"; echo "$BASE" > "$S/BASE_SHA"
  git -C "$C" show --stat --format='candidate %H over %P' HEAD | head -12
  ;;
full)
  rm -rf "$S/full"; mkdir -p "$S/full"
  git -C "$C" archive "$(cand)" | tar -x -C "$S/full"
  du -sh "$S/full" | cut -f1
  ;;
probe)
  mkdir -p "$S/probe"
  (cd "$C" && python3 - "$(cand)" > "$S/probe/_gates.txt" <<'PY'
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
  T0=$(date +%s); N=$(wc -l < "$S/probe/_gates.txt")
  while read -r gp; do
    b="$(basename "$gp")"; [ -f "$S/probe/$b.json" ] && continue
    [ $(( $(date +%s) - T0 )) -gt ${R4A_CHUNK:-110} ] && { echo "chunk done: $(ls "$S/probe"/*.json 2>/dev/null | wc -l)/$N — run probe again"; exit 0; }
    gen --probe --commit "$(cand)" --only "$b" --probe-stage "$S/probestage" --full-stage "$S/full" \
        --out "$S/probe/$b.json.tmp" >/dev/null && mv "$S/probe/$b.json.tmp" "$S/probe/$b.json"
  done < "$S/probe/_gates.txt"
  echo "PROBE COMPLETE: $(ls "$S/probe"/*.json | wc -l)/$N gates"
  ;;
manifest)
  (cd "$C" && python3 - "$S" "$(cand)" <<'PY'
import sys, json, os; sys.path.insert(0, "knowledge/_release")
import _gen_pack_manifest as G
S, sha = sys.argv[1], sys.argv[2]
order = open(os.path.join(S, "probe/_gates.txt")).read().split()
chunks = [json.load(open(os.path.join(S, "probe", os.path.basename(p) + ".json"))) for p in order]
assert all(c["commit"] == sha and c["differential_arm"] == "ARMED" for c in chunks)
gates = [g for c in chunks for g in c["gates"]]
assert [g["path"] for g in gates] == order, "probe chunks do not cover the gate set in order"
probe = dict(commit=sha, timeout_s=chunks[0]["timeout_s"], differential_arm="ARMED",
             full_stage=chunks[0]["full_stage"], gates=gates)
open(G.PROBE_PATH, "w").write(G.canonical(probe))
import collections; print("probe merged:", len(gates), dict(collections.Counter(g["verdict"] for g in gates)))
PY
  )
  gen --manifest --commit "$(cand)"
  ;;
bake)
  rm -rf "$S/out"
  (cd "$C" && bash apollo-spider/build-designer-pack.sh --dry-run --commit "$(cand)" --out-dir "$S/out") 2>&1 | tee "$S/bake.log" | tail -25
  ;;
check)
  Z="$S/out/Apollo-Spider-v1.0.14.zip"
  gen --check "$Z" --commit "$(cand)" 2>&1 | tail -6 || true
  python3 "$C/knowledge/_release/_gate_pack_docs.py" --stage "$S/out/Apollo-Spider-v1.0.14" --strict 2>&1 | tail -8 || true
  python3 - "$Z" <<'PY'
import sys, zipfile, json
z = zipfile.ZipFile(sys.argv[1]); n = z.namelist(); root = n[0].split("/")[0]
has = lambda p: (root + "/" + p) in n
metas = [x for x in n if x.startswith(root + "/knowledge/components/") and x.endswith(".meta.json")]
cnt = {"provides": 0, "when": 0, "obeys": 0}
for m in metas:
    d = json.loads(z.read(m))
    cnt["provides"] += bool(d.get("provides")); cnt["when"] += bool(d.get("when"))
    cnt["obeys"] += bool((d.get("edges") or {}).get("obeys"))
rul = json.loads(z.read(root + "/knowledge/_rulings.json"))["rulings"] if has("knowledge/_rulings.json") else []
print(json.dumps({"files": len(n), "reader": has("knowledge/_compose_slice.py"), "rulings": len(rul),
  "brain_files": sum(1 for x in n if x.startswith(root + "/knowledge/brain/")),
  "ux_principle_nodes": has("knowledge/_ux_principle_nodes.json"), "metas": len(metas), **cnt,
  "skill_splices_template": b"edit it down" in z.read(root + "/skills/generate-from-canon/SKILL.md")}))
PY
  sha256sum "$Z"
  ;;
*) sed -n '2,20p' "${BASH_SOURCE[0]}"; exit 2 ;;
esac
