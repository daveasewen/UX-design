# #305 D1 - door run. Paths in the paths file, each checked changed-or-untracked first.
cd "$(dirname "$0")/../../../.." || exit 1
LOG=${1:-notes/_lanes/305/D1/_gitcommit-D1.log}
MSG=${2:-notes/_lanes/305/D1/_msg-D1.txt}
PF=${3:-notes/_lanes/305/D1/paths-d1.txt}
mapfile -t P < "$PF"
SESSION_N=305 bash knowledge/_git_commit.sh --reconciled --quiet=$LOG "$MSG" "${P[@]}"
echo "EXIT=$?"
