# #305 C3 - wave three door run. Paths in the paths file, each checked changed-or-untracked first.
cd "$(dirname "$0")/../../../.." || exit 1
LOG=${1:-notes/_lanes/305/C3/_gitcommit-C3.log}
MSG=${2:-notes/_lanes/305/C3/_msg-C3.txt}
PF=${3:-notes/_lanes/305/C3/paths-c3.txt}
mapfile -t P < "$PF"
SESSION_N=305 bash knowledge/_git_commit.sh --reconciled --quiet=$LOG "$MSG" "${P[@]}"
echo "EXIT=$?"
