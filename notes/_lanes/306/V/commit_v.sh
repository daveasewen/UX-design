# #306 V - the commit door run (copied from U). Paths in a paths file, each checked changed-or-untracked first.
cd "$(dirname "$0")/../../../.." || exit 1
LOG=${1:?log}; MSG=${2:?msgfile}; PF=${3:?pathsfile}
export GIT_OPTIONAL_LOCKS=0
mapfile -t P < "$PF"
CHG=$( { git --no-optional-locks diff --name-only HEAD; git --no-optional-locks ls-files --others --exclude-standard; } | sort -u)
bad=0; for p in "${P[@]}"; do grep -qxF "$p" <<<"$CHG" || { echo "NOT changed/untracked: $p"; bad=1; }; done
[ $bad = 0 ] || { echo "REFUSED: a named path is neither changed nor untracked"; exit 3; }
echo "paths checked: ${#P[@]} of ${#P[@]} changed-or-untracked"
SESSION_N=306 bash knowledge/_git_commit.sh --reconciled --quiet=$LOG "$MSG" "${P[@]}"
echo "EXIT=$?"
