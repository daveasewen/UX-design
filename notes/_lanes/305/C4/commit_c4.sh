# #305 C4 - door run. Paths in the paths file, each checked changed-or-untracked first.
cd "$(dirname "$0")/../../../.." || exit 1
LOG=${1:-notes/_lanes/305/C4/_gitcommit-C4.log}
MSG=${2:-notes/_lanes/305/C4/_msg-C4.txt}
PF=${3:-notes/_lanes/305/C4/paths-c4.txt}
mapfile -t P < "$PF"
SESSION_N=305 bash knowledge/_git_commit.sh --reconciled --quiet=$LOG "$MSG" "${P[@]}"
echo "EXIT=$?"
