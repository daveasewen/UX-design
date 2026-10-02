#!/usr/bin/env bash
# CR #315: candidate v1.0.15 over BASE, adapted from notes/_lanes/304/R4a/build_candidate.sh (literals 14->15)
set -euo pipefail
REPO=/home/claude/apollo; S=/home/claude/cr/cand; C=$S/clone
BASE=853d7f56b
export PYTHONDONTWRITEBYTECODE=1
gen() { (cd "$C" && python3 knowledge/_release/_gen_pack_manifest.py "$@"); }
cand() { cat "$S/CANDIDATE_SHA"; }
LITERALS=("apollo-spider/FIRST-SESSION.md" "apollo-spider/gumdrop/_state.json" "apollo-spider/gumdrop/runbooks/_RUNBOOK-capture-ritual.md" "apollo-spider/gumdrop/runbooks/_RUNBOOK-context-gauge.md")
case "$1" in
prep)
  rm -rf "$S"; mkdir -p "$S"
  git clone --quiet --shared --no-checkout "$REPO" "$C"
  git -C "$C" sparse-checkout init --no-cone
  printf '/*\n!/notes/_lanes/\n!/apollo-spider/dist/\n!/notes/_subreports/\n' > "$C/.git/info/sparse-checkout"
  BASE=$(git -C "$REPO" rev-parse 853d7f56)
  git -C "$C" checkout --quiet "$BASE"
  sed -i 's/^VERSION = "v1\.0\.14"/VERSION = "v1.0.15"/; s/^MEMENTO_CUT_VERSION = "v1\.0\.14"/MEMENTO_CUT_VERSION = "v1.0.15"/' "$C/knowledge/_release/_gen_pack_manifest.py"
  grep -q '^VERSION = "v1.0.15"' "$C/knowledge/_release/_gen_pack_manifest.py"
  for f in "${LITERALS[@]}"; do sed -i 's/Apollo-Spider-v1\.0\.14/Apollo-Spider-v1.0.15/g; s/Gumdrop v1\.0\.14/Gumdrop v1.0.15/g' "$C/$f"; done
  D="$(git -C "$C" show -s --format=%cI "$BASE")"
  git -C "$C" add -A -- knowledge/_release/_gen_pack_manifest.py "${LITERALS[@]}"
  GIT_AUTHOR_DATE="$D" GIT_COMMITTER_DATE="$D" git -C "$C" -c user.name="CR scratch" -c user.email="cr@scratch.invalid" commit --quiet -m "CR #315 SCRATCH candidate v1.0.15 over ${BASE:0:8} (not a release)"
  git -C "$C" rev-parse HEAD > "$S/CANDIDATE_SHA"; echo "$BASE" > "$S/BASE_SHA"
  git -C "$C" show --stat --format='candidate %H over %P' HEAD | head -12 ;;
full) rm -rf "$S/full"; mkdir -p "$S/full"; git -C "$C" archive "$(cand)" | tar -x -C "$S/full"; du -sh "$S/full" ;;
esac
