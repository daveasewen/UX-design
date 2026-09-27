# #305 C2 - wave two door run. Paths in paths-c2.txt, each checked changed-or-untracked first.
cd "$(dirname "$0")/../../../.." || exit 1
LOG=${1:-notes/_lanes/305/C2/_gitcommit-C2.log}
MSG=${2:-notes/_lanes/305/C2/_msg-C2.txt}
PF=${3:-notes/_lanes/305/C2/paths-c2.txt}
mapfile -t P < "$PF"
SESSION_N=305 bash knowledge/_git_commit.sh --reconciled --quiet=$LOG "$MSG" "${P[@]}"
echo "EXIT=$?"
