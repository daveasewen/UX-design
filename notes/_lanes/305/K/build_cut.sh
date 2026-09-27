#!/usr/bin/env bash
# #305 K — the v1.0.14 cut rehearsed in a SCRATCH clone: R4a's recipe (notes/_lanes/304/R4a/build_candidate.sh)
# with three changes, nothing else: (1) the scratch lives under /var/tmp (the seat's $HOME has ~1.5 GB free,
# the recipe wants 2.6), (2) the overlay is K's working-tree cut edits copied from the mount instead of a sed in
# the clone (the version sweep, RATIFY_IDS "v1.0.14": "s305-D2", the stamp fix), (3) a `release` step that
# commits the RATIFIED manifest IN THE CLONE and runs --release there, then moves the frozen literal and seeds.
# ORIGINAL HEADER FOLLOWS.
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
S="${K_SCRATCH:-/var/tmp/k305/cand}"
C="$S/clone"
OVERLAY=("knowledge/_release/_gen_pack_manifest.py" "apollo-spider/build-designer-pack.sh"
         "apollo-spider/FIRST-SESSION.md" "apollo-spider/gumdrop/_state.json"
         "apollo-spider/gumdrop/runbooks/_RUNBOOK-capture-ritual.md"
         "apollo-spider/gumdrop/runbooks/_RUNBOOK-context-gauge.md")
export PYTHONDONTWRITEBYTECODE=1
step="${1:-}"; shift || true
gen() { (cd "$C" && python3 knowledge/_release/_gen_pack_manifest.py "$@"); }
cand() { cat "$S/CANDIDATE_SHA"; }

case "$step" in
prep)
  BASE="${1:-$(git -C "$REPO" --no-optional-locks rev-parse HEAD)}"
  mkdir -p "$(dirname "$S")"
  AVAIL=$(df -Pk "$(dirname "$S")" | awk 'NR==2{print $4}')
  [ "$AVAIL" -gt 2600000 ] || { echo "REFUSED: under 2.6 GB free at $(dirname "$S") ($AVAIL KB)"; exit 2; }
  rm -rf "$S"; mkdir -p "$S"
  git clone --quiet --shared --no-checkout "$REPO" "$C"
  git -C "$C" sparse-checkout init --no-cone
  printf '/*\n!/notes/_lanes/\n!/apollo-spider/dist/\n!/notes/_subreports/\n' > "$C/.git/info/sparse-checkout"
  git -C "$C" checkout --quiet "$BASE"
  for f in "${OVERLAY[@]}"; do cp "$REPO/$f" "$C/$f"; done
  grep -q '^VERSION = "v1.0.14"' "$C/knowledge/_release/_gen_pack_manifest.py" || { echo "REFUSED: VERSION literal not found"; exit 2; }
  D="$(git -C "$C" show -s --format=%cI "$BASE")"
  git -C "$C" add -A -- "${OVERLAY[@]}"
  GIT_AUTHOR_DATE="$D" GIT_COMMITTER_DATE="$D" git -C "$C" -c user.name="K305 scratch" \
      -c user.email="k305@scratch.invalid" commit --quiet -m "K305 SCRATCH cut v1.0.14 over ${BASE:0:8} (rehearsal, not the release commit)"
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
release)
  # rehearse the after-X half in the clone: commit the RATIFIED manifest + probe, --release, literal, seed, gates
  X="$(cand)"
  (cd "$C" && python3 -c "import json;m=json.load(open('knowledge/_release/_pack_manifest.json'));print(m['version'],m['commit'][:12],m['status'][:60])")
  D="$(git -C "$C" show -s --format=%cI "$X")"
  git -C "$C" add -A -- knowledge/_release/_pack_manifest.json knowledge/_release/_pack_gate_probe.json reviews/
  GIT_AUTHOR_DATE="$D" GIT_COMMITTER_DATE="$D" git -C "$C" -c user.name="K305 scratch" -c user.email="k305@scratch.invalid" \
      commit --quiet -m "K305 SCRATCH v1.0.14 manifest RATIFIED at ${X:0:12} (rehearsal)"
  git -C "$C" status --porcelain | head -5
  (cd "$C" && export TMPDIR=/var/tmp && bash apollo-spider/build-designer-pack.sh --release --commit "$X") 2>&1 | tee "$S/release.log" | tail -14
  ;;
seed)
  (cd "$C" && sed -i 's|    ("apollo-spider", \["apollo-spider/dist/"\], "v1.0.13",|    ("apollo-spider", ["apollo-spider/dist/"], "v1.0.14",|' knowledge/_release/_gate_frozen_release.py \
     && grep -c '"apollo-spider/dist/"\], "v1.0.14"' knowledge/_release/_gate_frozen_release.py \
     && python3 knowledge/_release/_gate_frozen_release.py --seed 2>&1 | tail -12)
  ;;
prep-real)
  # THE REAL CUT. After the commit seat has committed K's sweep as X on master: clone at X with NO overlay
  # and NO scratch commit, so the manifest, the zip and PROVENANCE name the real X. Then full, probe,
  # manifest, bake, check, release exactly as the rehearsal ran them.
  X="${1:?name the real cut commit X}"
  mkdir -p "$(dirname "$S")"
  AVAIL=$(df -Pk "$(dirname "$S")" | awk 'NR==2{print $4}')
  [ "$AVAIL" -gt 2600000 ] || { echo "REFUSED: under 2.6 GB free at $(dirname "$S") ($AVAIL KB)"; exit 2; }
  rm -rf "$S"; mkdir -p "$S"
  git clone --quiet --shared --no-checkout "$REPO" "$C"
  git -C "$C" sparse-checkout init --no-cone
  printf '/*\n!/notes/_lanes/\n!/notes/_subreports/\n' > "$C/.git/info/sparse-checkout"
  git -C "$C" checkout --quiet "$X"
  grep -q '^VERSION = "v1.0.14"' "$C/knowledge/_release/_gen_pack_manifest.py" || { echo "REFUSED: X does not carry VERSION v1.0.14"; exit 2; }
  git -C "$C" rev-parse HEAD > "$S/CANDIDATE_SHA"; echo "$X" > "$S/BASE_SHA"; echo "real cut commit $(cat "$S/CANDIDATE_SHA")"
  ;;
land)
  # Copy the real cut's outputs from the clone into the mount (after prep-real .. release). Never touches
  # any other zip in apollo-spider/dist/; refuses if v1.0.14 is already there.
  Z="$C/apollo-spider/dist/Apollo-Spider-v1.0.14.zip"; D="$REPO/apollo-spider/dist/Apollo-Spider-v1.0.14.zip"
  [ -f "$Z" ] || { echo "REFUSED: no released zip in the clone"; exit 2; }
  [ -e "$D" ] && { echo "REFUSED: $D exists"; exit 2; }
  for f in knowledge/_release/_pack_manifest.json knowledge/_release/_pack_gate_probe.json reviews/RELEASE-SPIDER-2026-08-26-v1.html; do cp "$C/$f" "$REPO/$f"; done
  cp "$Z" "$D"; sha256sum "$D"
  (cd "$REPO" && python3 knowledge/_review/_make_review.py reviews/RELEASE-SPIDER-2026-08-26-v1.html 2>&1 | tail -3)
  ;;
seed-real)
  # After the commit carrying the zip: move the frozen literal on the mount, seed, run the gate.
  (cd "$REPO" && export GIT_OPTIONAL_LOCKS=0 && python3 - <<'PY'
p = 'knowledge/_release/_gate_frozen_release.py'; s = open(p).read()
o = '    ("apollo-spider", ["apollo-spider/dist/"], "v1.0.13",'
assert s.count(o) == 1, 'frozen literal not at v1.0.13'
s = s.replace(o, "    # #305: v1.0.13 -> v1.0.14 with the v1.0.14 bake (s305-D2). Same fourth-home caveat as above;\n"
                 "    # bumped in the key commit, read back from the seed's printed table.\n" + o.replace('v1.0.13', 'v1.0.14'))
open(p, 'w').write(s)
PY
   python3 knowledge/_release/_gate_frozen_release.py --seed 2>&1 | tail -6)
  ;;
*) sed -n '2,20p' "${BASH_SOURCE[0]}"; exit 2 ;;
esac
