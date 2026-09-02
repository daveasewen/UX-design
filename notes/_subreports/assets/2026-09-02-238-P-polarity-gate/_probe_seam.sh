#!/usr/bin/env bash
# #238-P — drive the polarity gate's COMMIT-SEAM block DIRECTLY (the live lines of
# knowledge/_git_commit.sh, extracted verbatim between its marker and its closing `fi`), three ways:
#   (a) on the real home           -> green
#   (b) on a mutated COPY of the real home (an UNTYPED link on pl-03), pointed at through
#       POLARITY_BRAIN_DIR          -> red, refusal NAMED, fail() fires
#   (c) the same mutant under POLARITY_ACK  -> DECLARED gap, named
# No git command is run; the block is executed in a throwaway bash with fail() defined.
# Usage: bash notes/_subreports/assets/2026-09-02-238-P-polarity-gate/_probe_seam.sh   (from the repo root)
set -u
cd "$(dirname "$0")/../../../.." || exit 1
SCR="${TMPDIR:-/dev/shm}/p238-seam-$$"
mkdir -p "$SCR"
BLK=$(awk '/^# ── POLARITY GATE — s238-D7/{f=1} f{print} f&&/^fi$/{exit}' knowledge/_git_commit.sh)
[ -n "$BLK" ] || { echo "✗ the seam block marker was not found in knowledge/_git_commit.sh"; exit 1; }
echo "== extracted seam block: $(printf '%s\n' "$BLK" | grep -c '') lines, live lines:"
printf '%s\n' "$BLK" | grep -v '^#'
{
  echo 'set -u'
  echo 'fail() { echo "✗ $1" >&2; exit 1; }'
  printf '%s\n' "$BLK"
  echo 'echo "SEAM-BLOCK-EXIT-0"'
} > "$SCR/probe.sh"

echo; echo "== (a) real home"
bash "$SCR/probe.sh" 2>&1 | tail -2; RA=${PIPESTATUS[0]}; echo "rc=$RA"

cp -r knowledge/brain "$SCR/brain"
python3 - "$SCR/brain/polarities.json" <<'EOF'
import json, sys
p = sys.argv[1]; o = json.load(open(p))
o["polarities"][2]["links"].append({"ref": "s116-D1"})      # UNTYPED link on pl-03
json.dump(o, open(p, "w"), indent=1, ensure_ascii=False)
EOF
echo; echo "== (b) mutated copy (untyped link on pl-03) via POLARITY_BRAIN_DIR"
POLARITY_BRAIN_DIR="$SCR/brain" bash "$SCR/probe.sh" 2>&1 | grep -E "REFUSED|✗|SEAM" | cut -c1-200; RB=${PIPESTATUS[0]}; echo "rc=$RB"

echo; echo "== (c) the same mutant under the DECLARED hatch"
POLARITY_BRAIN_DIR="$SCR/brain" POLARITY_ACK="probe: declared gap" bash "$SCR/probe.sh" 2>&1 | tail -2; RC=${PIPESTATUS[0]}; echo "rc=$RC"
rm -rf "$SCR"
echo
if [ "$RA" -eq 0 ] && [ "$RB" -eq 1 ] && [ "$RC" -eq 0 ]; then
  echo "✓ seam block proven both ways + hatch: (a) rc 0 · (b) rc 1 named · (c) rc 0 declared"; exit 0
fi
echo "✗ seam probe FAILED: rc (a)=$RA (b)=$RB (c)=$RC"; exit 1
