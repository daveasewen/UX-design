# #305 C1 - wave one door run. Paths in paths-c1.txt, each checked changed-or-untracked first.
cd "$(dirname "$0")/../../../.." || exit 1
LOG=${1:-notes/_lanes/305/C1/_gitcommit-C1.log}
MSG=${2:-notes/_lanes/305/C1/_msg-C1.txt}
PF=${3:-notes/_lanes/305/C1/paths-c1.txt}
mapfile -t P < "$PF"
SESSION_N=305 bash knowledge/_git_commit.sh --reconciled --quiet=$LOG "$MSG" "${P[@]}"
echo "EXIT=$?"
