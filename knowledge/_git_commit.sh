#!/usr/bin/env bash
# _git_commit.sh — the sandbox commit dance, mechanised.
# provenance: lane session 2026-07-26 (dream-pass P2, Dave ruled accept-enact-now) · status: ruled
#
# WHY: 5 of 7 commit-running sessions (3 of 5 at ruling; #36 + #41 since) reconstructed the clear·stage·clear·commit·clear sequence
# from memory under wrap-time heat and hit the lock failure first (dream-pass P2 evidence).
# Per feedback-gate-dont-patch: make the condition mechanical, not another prose reminder.
# The sandbox delete-guard means locks can only be MOVED (mv), never rm'd — see the runbook.
#
# USAGE:  bash knowledge/_git_commit.sh --reconciled <msgfile>
#   <msgfile>      commit message file — UNIQUE name, in a session-owned dir (outputs/), never /tmp
#   --reconciled   you have run `git status --short` and can name WHY every dirty path exists
#                  (runbook step 0.5 — the script cannot do this judgment for you)
# The script REFUSES to stage while any .git/*.lock exists, and never runs rm inside .git.

set -u
cd "$(dirname "$0")/.." || exit 1

RECONCILED=0
MSGFILE=""
for a in "$@"; do
  case "$a" in
    --reconciled) RECONCILED=1 ;;
    *) MSGFILE="$a" ;;
  esac
done

clear_locks() {
  mkdir -p _to_delete/_stale_locks
  for L in $(find .git -name '*.lock' 2>/dev/null); do
    mv "$L" "_to_delete/_stale_locks/$(basename "$L").$(date +%s%N)" || true
  done
}

fail() { echo "✗ $1" >&2; exit 1; }

[ -n "$MSGFILE" ] || fail "no msgfile given. Usage: _git_commit.sh --reconciled <msgfile>"
[ -s "$MSGFILE" ] || fail "msgfile '$MSGFILE' missing or empty (stale-msgfile trap — see runbook gotchas)"
echo "— msgfile head: $(head -1 "$MSGFILE")"

if [ "$RECONCILED" -ne 1 ]; then
  echo "✗ refusing to stage: run 'git status --short', account for EVERY dirty path (step 0.5),"
  echo "  then re-run with --reconciled. Dirty paths now:"
  git status --short
  exit 1
fi

# chain-staleness gate — this is the seam that actually reads disk state. _gen_chain.py --check's
# OTHER caller (_build_all.py) runs it immediately AFTER regenerating the file, so it can only ever
# catch nondeterminism in build(), never a chain left stale by a hand-edit to GOOD-MORNING.md /
# _LIVE-STATE.md that was never regenerated — the #32 defect, which is what actually landed at the
# #56 wrap (stale chain, clean tree, committed). Refuse loudly; do NOT auto-regenerate here — that
# would stage a file this session never showed you.
# ⛔ CORRECTED #58b, found by the probe worker: this line used to re-assert "_CHAIN.md is STALE" and
# name "regenerate it" as the remedy, on ANY non-zero exit — so when --check refused because its
# TOKEN MEASURER was degraded (tiktoken absent / encoding file unreachable), the honest message it
# had just printed was immediately overridden here by a WRONG CAUSE and a WRONG REMEDY, at the one
# seam that blocks. ★ A WRAPPER MUST NOT RESTATE A CAUSE IT DID NOT DETERMINE. The check owns the
# diagnosis and has already printed it; this layer owns only the consequence — nothing was staged.
python3 knowledge/_gen_chain.py --check ||
  fail "_gen_chain.py --check REFUSED (exit non-zero) — its message is printed directly above and it is the authority on the cause; this script does not second-guess it. Nothing has been staged. If it named STALENESS, run: python3 knowledge/_gen_chain.py — then re-run this script. If it named a DEGRADED MEASUREMENT, regenerating will NOT help: fix tiktoken first (pip install tiktoken --break-system-packages) and re-run."
echo "— chain fresh (_gen_chain.py --check passed)"

# clear · stage · clear · commit · clear
clear_locks
find .git -name '*.lock' | grep -q . && fail "lock survived the mv-aside — do NOT stage; investigate"

git add -A 2>/dev/null
git diff --cached --name-only | sed 's/^/  staged: /'
git diff --cached --quiet && fail "nothing staged — empty commit refused"

clear_locks

BEFORE=$(git rev-parse HEAD)
git -c user.name="Claude" -c user.email="claude@anthropic.com" commit -F "$MSGFILE" 2>&1 |
  grep -v 'unable to unlink' || true
AFTER=$(git rev-parse HEAD)
[ "$BEFORE" != "$AFTER" ] || fail "HEAD did not advance — commit did not land"
echo "— committed: $(git log --oneline -1)"
git log -1 --format=%s | head -1 | grep -qF "$(head -1 "$MSGFILE" | cut -c1-40)" ||
  echo "⚠ HEAD message does not match msgfile head — CHECK for the stale-msgfile trap"

# last action: clear the lock git just respawned; no git command after this
clear_locks
echo "✓ done — locks clear, safe for Dave to push via GitHub Desktop"
